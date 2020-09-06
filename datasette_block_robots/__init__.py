from datasette import hookimpl
from datasette.utils.asgi import Response


def robots_txt(datasette):
    config = datasette.plugin_config("datasette-block-robots") or {}
    literal = config.get("literal")
    if literal:
        return Response.text(literal)
    disallow = config.get("disallow")
    if isinstance(disallow, str):
        disallow = [disallow]
    if not disallow:
        disallow = ["/"]
    lines = ["User-agent: *"] + ["Disallow: {}".format(item) for item in disallow]
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
