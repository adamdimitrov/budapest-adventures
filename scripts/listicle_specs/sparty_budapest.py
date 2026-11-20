# -*- coding: utf-8 -*-
"""Upgrade spec for sparty-budapest.html: questions from the page's own Quick Facts tables."""
import importlib.util
import os

_s = importlib.util.spec_from_file_location("_quickfacts", os.path.join(os.path.dirname(os.path.abspath(__file__)), "_quickfacts.py"))
_q = importlib.util.module_from_spec(_s)
_s.loader.exec_module(_q)

PAGE_FILE = "sparty-budapest.html"
PAGE, CARDS = _q.build(PAGE_FILE, _q.anchors(PAGE_FILE), "tickets", [
    {"label": "Type", "chips": [("sparty", "🎉 Sparty tickets"), ("alt", "🌙 Other night baths")]},
])
CARDS["card-3"]["cats"] = ["alt"]
CARDS["card-4"]["cats"] = ["alt"]
