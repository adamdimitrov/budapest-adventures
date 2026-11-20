# -*- coding: utf-8 -*-
"""Upgrade spec for best-cooking-classes-budapest.html: derived from scripts/articles/best-cooking-classes-budapest.json (see _articles.py)."""
import importlib.util
import os

_s = importlib.util.spec_from_file_location("_articles", os.path.join(os.path.dirname(os.path.abspath(__file__)), "_articles.py"))
_a = importlib.util.module_from_spec(_s)
_s.loader.exec_module(_a)

PAGE, CARDS = _a.build("best-cooking-classes-budapest")
PAGE["noun"] = "classes"
PAGE["filter_aria"] = "Filter classes"
