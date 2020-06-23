# datasette-block-robots

[![PyPI](https://img.shields.io/pypi/v/datasette-block-robots.svg)](https://pypi.org/project/datasette-block-robots/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-block-robots?label=changelog)](https://github.com/simonw/datasette-block-robots/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-block-robots/blob/master/LICENSE)

Datasette plugin that blocks all robots using robots.txt

## Installation

Install this plugin in the same environment as Datasette.

    $ pip install datasette-block-robots

## Usage

Having installed the plugin, `/robots.txt` on your Datasette instance will return the following:

    User-agent: *
    Disallow: /

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-block-robots
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
