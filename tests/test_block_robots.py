from datasette.app import Datasette
import pytest
import httpx


@pytest.mark.asyncio
async def test_robots_txt():
    app = Datasette([], memory=True).app()
    async with httpx.AsyncClient(app=app) as client:
        response = await client.get("http://localhost/robots.txt")
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/plain; charset=utf-8"
        assert response.text == "User-agent: *\nDisallow: /"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "config,expected",
    [
        (None, "User-agent: *\nDisallow: /"),
        ({"disallow": "/foo"}, "User-agent: *\nDisallow: /foo"),
        (
            {"disallow": ["/foo", "/bar"]},
            "User-agent: *\nDisallow: /foo\nDisallow: /bar",
        ),
    ],
)
async def test_config_disallow(config, expected):
    app = Datasette(
        [], memory=True, metadata={"plugins": {"datasette-block-robots": config}}
    ).app()
    async with httpx.AsyncClient(app=app) as client:
        response = await client.get("http://localhost/robots.txt")
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/plain; charset=utf-8"
        assert response.text == expected
