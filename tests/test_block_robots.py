from datasette.app import Datasette
import pytest
import httpx


@pytest.mark.asyncio
async def test_robots_txt():
    app = Datasette([], memory=True).app()
    async with httpx.AsyncClient(app=app) as client:
        response = await client.get("http://localhost/robots.txt")
        assert 200 == response.status_code
        assert "text/plain; charset=utf-8" == response.headers["content-type"]
        assert "User-agent: *\nDisallow: /" == response.text
