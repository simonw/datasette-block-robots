from datasette import hookimpl
from datasette.utils.asgi import Response
from datasette.utils import await_me_maybe
from datasette.plugins import pm
from . import hookspecs

pm.add_hookspecs(hookspecs)


async def robots_txt(datasette, request):
    config = datasette.plugin_config("datasette-block-robots") or {}
    literal = config.get("literal")
    disallow = []
    if literal:
        lines = literal.split("\n")
    else:
        disallow = config.get("disallow") or []
        if isinstance(disallow, str):
            disallow = [disallow]
        allow_only_index = config.get("allow_only_index")
        if allow_only_index:
            for database_name in datasette.databases:
                if database_name != "_internal":
                    disallow.append(datasette.urls.database(database_name))
        if not disallow:
            disallow = ["/"]
        lines = ["User-agent: *"] + ["Disallow: {}".format(item) for item in disallow]

    # Add lines generated by plugins
    for more_lines in pm.hook.block_robots_extra_lines(
        datasette=datasette, request=request
    ):
        more_lines = await await_me_maybe(more_lines)
        if more_lines:
            lines.extend(more_lines)

    return Response.text("\n".join(lines))


@hookimpl
def register_routes():
    return [
        (r"^/robots\.txt$", robots_txt),
    ]


@hookimpl
def startup(datasette):
    config = datasette.plugin_config("datasette-block-robots") or {}
    assert not (
        config.get("disallow") and config.get("literal")
    ), "datasette-block-robots cannot be configured with both disallow: and literal:"
