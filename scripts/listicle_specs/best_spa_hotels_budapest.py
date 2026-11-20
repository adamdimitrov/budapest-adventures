# -*- coding: utf-8 -*-
"""Upgrade spec for best-spa-hotels-budapest.html: derived from scripts/articles/best-shooting-ranges-budapest.json (see _articles.py)."""
import importlib.util
import os

_s = importlib.util.spec_from_file_location("_articles", os.path.join(os.path.dirname(os.path.abspath(__file__)), "_articles.py"))
_a = importlib.util.module_from_spec(_s)
_s.loader.exec_module(_a)

PAGE, CARDS = _a.build("best-spa-hotels-budapest")
PAGE["noun"] = "hotels"
PAGE["filter_aria"] = "Filter hotels"
