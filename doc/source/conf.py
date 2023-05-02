import pathlib
import subprocess

doxy_list = [
    "fri.Doxyfile",
    "lbr_fri_ros2.Doxyfile",  # lbr_fri_ros2.Doxyfile requires tagfile of fri.Doxyfile
]

for doxyfile in doxy_list:
    doxyfile_name = doxyfile.split(".")[0]

    # generate doxygen
    path = pathlib.Path(f"docs/doxygen/{doxyfile_name}")
    if not path.exists():
        path.mkdir(parents=True)  # this is the doxygen OUTPUT_DIRECTORY
    subprocess.run(f"doxygen {doxyfile}", shell=True)

    # convert doxygen to sphinx, source and build directory need
    # to follow https://boschglobal.github.io/doxysphinx/docs/getting_started.html#build
    subprocess.run(
        f"doxysphinx build . $READTHEDOCS_OUTPUT/html {doxyfile}", shell=True
    )

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "lbr_fri_ros2_stack"
copyright = "2023, mhubii"
author = "mhubii"
release = "1.0.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx_mdinclude", "sphinx_copybutton", "sphinx.ext.autosectionlabel"]

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
