# -*- coding: utf-8 -*-
"""Upgrade spec for budapest-christmas-markets.html: questions from the page's own Quick Facts tables."""
import importlib.util
import os

_s = importlib.util.spec_from_file_location("_quickfacts", os.path.join(os.path.dirname(os.path.abspath(__file__)), "_quickfacts.py"))
_q = importlib.util.module_from_spec(_s)
_s.loader.exec_module(_q)

PAGE_FILE = "budapest-christmas-markets.html"
# No filters: the page's main deck holds the 4 market cards (not products), which the shared filter
# script would hide; the program cards sit in their own sections below each market.
PAGE, CARDS = _q.build(PAGE_FILE, _q.anchors(PAGE_FILE), "tours", [])
