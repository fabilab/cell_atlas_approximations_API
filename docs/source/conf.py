# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# Early import forfeits the credit warning for atlasapprox
import os

os.environ["ATLASAPPROX_HIDECREDITS"] = "yes"

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Cell Atlas Approximations API"
copyright = "2023, Fabio Zanini"
author = "Fabio Zanini"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_tabs.tabs",
    "sphinx.ext.napoleon",
    "sphinx_gallery.gen_gallery",
]
sphinx_tabs_disable_tab_closing = True

templates_path = ["_templates"]
exclude_patterns = []

# -- Options for sphinx-gallery ----------------------------------------------
sphinx_gallery_conf = {
    "filename_pattern": "/.*.py",
    "examples_dirs": [
        "../gallery/python",
    ],
    "gallery_dirs": [
        "python/gallery",
    ],
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
