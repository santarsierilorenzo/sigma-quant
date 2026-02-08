from __future__ import annotations

from typing import List
import sys
import os


PROJECT_ROOT: str = os.path.abspath("..")
sys.path.insert(0, PROJECT_ROOT)

project = "Quant-Kit"
html_title = "Quant-Kit"
html_logo = "_static/logo.svg"
author: str = "Lorenzo Santarsieri"
release: str = "0.1.0"

extensions = [
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.mathjax",
    "sphinx_design",
]

autosummary_generate = True
autodoc_typehints = "none"

templates_path: List[str] = ["_templates"]

exclude_patterns: List[str] = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "**tests**",
]

source_suffix = ".rst"

html_theme = "breeze"

html_theme_options = {
    "sidebarwidth": 280,
    "show_nav_title": True,
}

html_static_path = ["_static"]

def setup(app) -> None:
    app.add_css_file("custom.css")

