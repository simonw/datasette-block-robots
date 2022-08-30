from pluggy import HookspecMarker

hookspec = HookspecMarker("datasette")


@hookspec
def block_robots_extra_lines(datasette):
    "A list of extra lines to be added to /robots.txt"
