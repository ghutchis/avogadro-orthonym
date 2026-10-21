#  This source file is part of the Avogadro project
#  This source code is released under the 3-Clause BSD License, (see "LICENSE").
#  https://github.com/ghutchis/avogadro-orthonym/

"""Entry point for the avogadro-orthonym plugin."""

import argparse

from .run import run


def main():
    parser = argparse.ArgumentParser("avogadro-orthonym")
    parser.add_argument("feature")
    parser.add_argument("--lang", nargs="?", default="en")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    run(args)


def setup():
    """Download the OPSIN and centres jars Orthonym needs.

    Avogadro runs this once after installing the plugin, so naming works
    later without a network connection.
    """
    import sys

    from orthonym.jars import JarUnavailable, fetch_all

    try:
        fetch_all(verbose=True)
    except JarUnavailable as exc:
        print(f"avogadro-orthonym-setup: {exc}", file=sys.stderr)
        sys.exit(1)
