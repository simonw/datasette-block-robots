from datasette import hookimpl
from datasette.app import Datasette
from datasette.plugins import pm
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


@pytest.mark.asyncio
async def test_extra_lines_plugin_hook():
    class TestPlugin:
        __name__ = "TestPlugin"

        @hookimpl
        def block_robots_extra_lines(self):
            return ["Extra line: 1", "Extra line: 2"]

    class TestPluginAsync:
        __name__ = "TestPluginAsync"

        @hookimpl
        def block_robots_extra_lines(self, datasette):
            async def inner():
                db = datasette.get_database()
                result = await db.execute("select 2 + 1")
                return ["Extra line: {}".format(result.single_value())]

            return inner

    pm.register(TestPlugin(), name="undo")
    pm.register(TestPluginAsync(), name="undo2")
    try:
        ds = Datasette([], memory=True)
        response = await ds.client.get("/robots.txt")
        assert response.status_code == 200
        lines = response.text.split("\n")
        for expected in (
            "Extra line: 1",
            "Extra line: 2",
            "Extra line: 3",
        ):
            assert expected in lines
    finally:
        pm.unregister(name="undo")
        pm.unregister(name="undo2")
