from datasette import hookimpl
from datasette.utils.asgi import Response


async def robots_txt():
    return Response.text("User-agent: *\nDisallow: /")


@hookimpl
def register_routes():
    return [
        (r"^/robots\.txt$", robots_txt),
    ]
