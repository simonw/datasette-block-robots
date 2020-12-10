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


LITERAL = """
User-agent: *
Disallow: /
User-agent: Bingbot
User-agent: Googlebot
Disallow:
""".strip()


@pytest.mark.asyncio
async def test_literal():
    app = Datasette(
        [],
        memory=True,
        metadata={"plugins": {"datasette-block-robots": {"literal": LITERAL}}},
    ).app()
    async with httpx.AsyncClient(app=app) as client:
        response = await client.get("http://localhost/robots.txt")
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/plain; charset=utf-8"
        assert response.text == LITERAL


@pytest.mark.asyncio
async def test_literal_prevent_literal_and_disallow_at_same_time():
    ds = Datasette(
        [],
        memory=True,
        metadata={
            "plugins": {"datasette-block-robots": {"literal": LITERAL, "disallow": "/"}}
        },
    )
    with pytest.raises(AssertionError):
        await ds.invoke_startup()
