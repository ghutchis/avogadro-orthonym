# avogadro-orthonym

An Avogadro 2 plugin that names the current molecule using
[Orthonym](https://github.com/Steinbeck-Lab/Orthonym)
([PyPI](https://pypi.org/project/orthonym/)), a rule-based IUPAC naming
engine aiming at the Preferred IUPAC Name.

It adds a single menu item under **Analyze → Properties → Orthonym Name…**
which names the molecule (via RDKit) and reports the IUPAC name and the
canonical SMILES in a dialog. The name is also stored on the molecule. When
Orthonym has no name for a structure, the dialog says so.

## Requirements

Orthonym checks its names with OPSIN and assigns CIP stereodescriptors with
centres, both Java programs.

- **Java** is provided by the plugin's pixi environment (conda-forge
  `openjdk`). If you set `JAVA_HOME` yourself, the plugin uses it as is.
- **Installing needs an internet connection.** Orthonym uses the OPSIN and
  centres jars. Avogadro runs `avogadro-orthonym-setup` after installing the
  plugin, which downloads them (checksum-verified) into
  `~/.cache/orthonym/jars`. After that, naming works offline. To fetch them
  again, run `pixi run avogadro-orthonym-setup` in the plugin directory.
- Starting the JVM adds a moment to each use of the menu item.

## Stereochemistry

The plugin passes the molecule read from Avogadro's SDF directly to Orthonym
(1.0.5 or later), with stereo taken from its 3D coordinates. Orthonym checks
that its SMILES keeps every atom and stereocentre, and reports an error rather
than naming the wrong stereoisomer.

## Citation

If you use this plugin, please cite Orthonym (Kohulan Rajan, Achim Zielesny,
Christoph Steinbeck). See the
[CITATION.cff](https://github.com/Steinbeck-Lab/Orthonym/blob/main/CITATION.cff)
in the Orthonym repository for the current reference and Zenodo record.

## Suggestions

Please submit suggestions, bugs, etc. on GitHub: https://github.com/ghutchis/avogadro-orthonym/issues
