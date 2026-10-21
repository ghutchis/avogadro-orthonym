#  This source file is part of the Avogadro project
#  This source code is released under the 3-Clause BSD License, (see "LICENSE").
#  https://github.com/ghutchis/avogadro-orthonym/

"""Generate an IUPAC name from the current molecule using Orthonym."""

import os
import sys
from pathlib import Path

from rdkit import Chem


def _ensure_java_home() -> None:
    """Point JAVA_HOME at the JDK bundled in this environment, if needed.

    Avogadro may run the environment's executable directly, without pixi
    activating the environment, so the conda ``openjdk`` activation script
    never sets JAVA_HOME.  A JAVA_HOME the user set is never overridden.
    """
    if os.environ.get("JAVA_HOME"):
        return
    prefix = Path(sys.prefix)
    # conda-forge openjdk: <prefix>/lib/jvm on Unix, <prefix>\Library\lib\jvm
    # on Windows (see its activate scripts)
    for candidate in (prefix / "lib" / "jvm", prefix / "Library" / "lib" / "jvm"):
        if candidate.is_dir():
            os.environ["JAVA_HOME"] = str(candidate)
            return


# Must happen before orthonym starts its JVM
_ensure_java_home()

import orthonym  # noqa: E402
from orthonym.errors import is_failure_name  # noqa: E402
from orthonym.jars import JarUnavailable  # noqa: E402


def _java_problem(exc: Exception) -> str | None:
    """Return a user-facing hint if ``exc`` is a Java / jar setup problem."""
    if isinstance(exc, JarUnavailable):
        return (
            "Orthonym needs two Java jars (OPSIN and centres) and could not "
            "find or download them. They are normally downloaded when the "
            "plugin is installed; reinstall it with an internet connection, "
            "or run `pixi run avogadro-orthonym-setup` in the plugin "
            "directory.\n\n"
            f"{exc}"
        )
    text = str(exc).lower()
    if "java" in text and ("jvm" in text or "not found" in text or "java_home" in text):
        return (
            "Orthonym could not start Java. The plugin's environment should "
            "provide it; if you set JAVA_HOME yourself, check that it points "
            f"to a working JDK.\n\n{exc}"
        )
    return None


def orthonym_name(avo_input: dict) -> dict:
    """Name the current molecule and store the name back on it.

    Avogadro always sends the full molecule as a ``cjson`` object alongside
    the requested ``sdf`` molblock.  We name the RDKit molecule read from
    the SDF directly (Orthonym 1.0.5+ accepts a Mol), then echo the molecule
    back with a ``name`` property added.  ``readProperties`` merges
    that property in place rather than rebuilding the molecule, so atoms,
    bonds and the undo history are left untouched.

    The echo is also what keeps a message-only response from being treated
    as an empty-molecule replacement by Avogadro.
    """
    output = {}

    # Echo the molecule back untouched; readProperties merges only the data
    # map (i.e. the name) instead of replacing atoms/bonds.
    cjson = avo_input.get("cjson")
    if isinstance(cjson, dict):
        cjson = dict(cjson)
        output["cjson"] = cjson
        output["moleculeFormat"] = "cjson"
        output["readProperties"] = True

    mol = Chem.MolFromMolBlock(avo_input.get("sdf", ""))
    if mol is None or mol.GetNumAtoms() == 0:
        output["error"] = "Could not interpret the molecule."
        return output

    # Only used for the messages shown to the user
    smiles = Chem.MolToSmiles(mol)

    try:
        # A ValueError here means the Mol's SMILES would lose stereo or
        # atoms; Orthonym's message says which check failed, so report it.
        name = orthonym.name_compound(mol)
    except Exception as exc:
        hint = _java_problem(exc)
        if hint:
            output["error"] = hint
        else:
            output["error"] = f"Could not name {smiles}:\n{exc}"
        return output

    # Orthonym returns a label such as "unknown organic compound" or
    # "inorganic compound (not supported)" when it has no name
    if is_failure_name(name):
        label = f" ({name})" if name else ""
        output["message"] = f"No name found for:\n{smiles}{label}"
        return output

    # Store the name on the molecule so Avogadro keeps and displays it.
    if isinstance(cjson, dict):
        cjson["name"] = name

    output["message"] = f"{name}\n\nSMILES: {smiles}"
    return output
