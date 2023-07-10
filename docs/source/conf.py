# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'RST: Decision Region Analysis'
copyright = '2023, Alexis Burgon'
author = 'Alexis Burgon'

import os
import sys
sys.path.insert(0,os.path.abspath(os.path.join("..","..")))
# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.coverage', 'sphinx.ext.napoleon','sphinx.ext.autosectionlabel']
autosectionlabel_prefix_document = True

autodoc_typehints = 'both'

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
html_theme_options = {
  'sidebar_width': '300px',
  'page_width':'1200px',
  'body_max_width':'auto',
  'github_button': 'true',
  'github_user': 'DIDSR',
  'github_repo': 'RST_Decision_Region_Analysis'
}
html_sidebars = {'**': ['globaltoc.html', 'relations.html', 'sourcelink.html', 'searchbox.html']}