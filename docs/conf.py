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

html_theme: str = "sphinx_rtd_theme"
html_static_path: List[str] = ["_static"]
