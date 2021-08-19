from datasette.app import Datasette
import pytest
import httpx


@pytest.mark.asyncio
async def test_robots_txt():
    ds = Datasette([], memory=True)
    response = await ds.client.get("/robots.txt")
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
    ds = Datasette(
        [], memory=True, metadata={"plugins": {"datasette-block-robots": config}}
    )
    response = await ds.client.get("/robots.txt")
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
    ds = Datasette(
        [],
        memory=True,
        metadata={"plugins": {"datasette-block-robots": {"literal": LITERAL}}},
    )
    response = await ds.client.get("/robots.txt")
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


@pytest.mark.asyncio
async def test_allow_only_index():
    ds = Datasette(
        [],
        memory=True,
        metadata={"plugins": {"datasette-block-robots": {"allow_only_index": True}}},
    )
    response = await ds.client.get("/robots.txt")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/plain; charset=utf-8"
    assert response.text == "User-agent: *\nDisallow: /_memory"
