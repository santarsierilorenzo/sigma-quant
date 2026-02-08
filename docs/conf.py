from __future__ import annotations

from typing import List
import sys
import os


PROJECT_ROOT: str = os.path.abspath("..")
sys.path.insert(0, PROJECT_ROOT)

project: str = "quant-kit"
author: str = "Lorenzo Santarsieri"
release: str = "0.1.0"

extensions: List[str] = [
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.mathjax",
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

html_theme = "sphinx_book_theme"

html_theme_options = {
    "repository_url": "",
    "use_edit_page_button": False,
    "use_repository_button": False,
    "home_page_in_toc": True,
}

html_static_path = ["_static"]
