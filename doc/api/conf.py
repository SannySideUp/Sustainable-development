# -- Project information -----------------------------------------------------

project = 'Sustainable Development Project'
author = 'Johnny Chang'
release = '1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',      # allows .. automodule:: and docstring import
    'sphinx.ext.napoleon',     # supports Google/NumPy style docstrings
    'sphinx.ext.viewcode',     # adds "view source" links
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

html_theme = 'alabaster'
html_static_path = ['_static']

import os
import sys

# Get absolute path to project root (two levels up from conf.py)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
src_path = os.path.join(project_root, 'src')

# Add both project root and src to sys.path
sys.path.insert(0, project_root)
sys.path.insert(0, src_path)

autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
    'noindex': True,  # prevents duplicate indexing
}
