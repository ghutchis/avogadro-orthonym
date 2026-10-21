#  This source file is part of the Avogadro project
#  This source code is released under the 3-Clause BSD License, (see "LICENSE").
#  https://github.com/ghutchis/avogadro-orthonym/

"""Dispatch feature identifier to the appropriate handler."""

import json
import sys


def run(args):
    avo_input = json.load(sys.stdin)
    output = None

    match args.feature:
        case "name":
            from .naming import orthonym_name
            output = orthonym_name(avo_input)

    if output is not None:
        print(json.dumps(output))
