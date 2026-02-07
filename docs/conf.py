from __future__ import annotations

import os
import sys
from typing import List


# -- Path setup -------------------------------------------------------------

PROJECT_ROOT: str = os.path.abspath("..")
sys.path.insert(0, PROJECT_ROOT)


# -- Project information ----------------------------------------------------

project: str = "quant-kit"
author: str = "Lorenzo Santarsieri"
release: str = "0.1.0"


# -- General configuration --------------------------------------------------

extensions: List[str] = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]

templates_path: List[str] = ["_templates"]

exclude_patterns: List[str] = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "**tests**",
]

source_suffix = ".rst"

# IMPORTANT:
# Do NOT set master_doc.
# Default "index" is correct when building from docs/


# -- HTML output ------------------------------------------------------------

html_theme: str = "pydata_sphinx_theme"

html_theme_options = {
    "secondary_sidebar_items": [],
}

html_static_path: List[str] = ["_static"]
