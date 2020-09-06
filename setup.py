from setuptools import setup
import os

VERSION = "0.3"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-block-robots",
    description="Datasette plugin that blocks all robots using robots.txt",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/datasette-block-robots",
    project_urls={
        "Issues": "https://github.com/simonw/datasette-block-robots/issues",
        "CI": "https://github.com/simonw/datasette-block-robots/actions",
        "Changelog": "https://github.com/simonw/datasette-block-robots/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["datasette_block_robots"],
    entry_points={"datasette": ["block_robots = datasette_block_robots"]},
    install_requires=["datasette>=0.45"],
    extras_require={"test": ["pytest", "pytest-asyncio", "httpx"]},
    tests_require=["datasette-block-robots[test]"],
)
