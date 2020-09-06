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

Here's a demo of the plugin in action: https://sqlite-generate-demo.datasette.io/robots.txt

## Configuration

By default the plugin will block all access to the site, using `Disallow: /`.

You can instead block access to specific areas of the site by adding the following to your `metadata.json` configuration file:

```json
{
    "plugins": {
        "datasette-block-robots": {
            "disallow": ["/mydatabase"]
        }
    }
}
```
This will result in a `/robots.txt` that looks like this:

    User-agent: *
    Disallow: /mydatabase

You can also set the full contents of the `robots.txt` file using the `literal` configuration option. Here's how to do that if you are using YAML rather than JSON and have a `metadata.yml` file:

```yaml
plugins:
    datasette-block-robots:
        literal: |-
            User-agent: *
            Disallow: /
            User-agent: Bingbot
            User-agent: Googlebot
            Disallow:
```
This example would block all crawlers with the exception of Googlebot and Bingbot, which are allowed to crawl the entire site.

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
