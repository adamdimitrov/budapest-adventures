# -*- coding: utf-8 -*-
"""Upgrade spec for best-communist-tours-budapest.html: derived from scripts/articles/best-communist-tours-budapest.json (see _articles.py)."""
import importlib.util
import os

_s = importlib.util.spec_from_file_location("_articles", os.path.join(os.path.dirname(os.path.abspath(__file__)), "_articles.py"))
_a = importlib.util.module_from_spec(_s)
_s.loader.exec_module(_a)

PAGE, CARDS = _a.build("best-communist-tours-budapest")
PAGE["noun"] = "tours"
PAGE["filter_aria"] = "Filter tours"
