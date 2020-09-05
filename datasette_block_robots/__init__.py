from datasette import hookimpl
from datasette.utils.asgi import Response


def robots_txt(datasette):
    config = datasette.plugin_config("datasette-block-robots") or {}
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
