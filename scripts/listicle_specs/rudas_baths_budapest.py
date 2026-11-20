# -*- coding: utf-8 -*-
"""Upgrade spec for rudas-baths-budapest.html: questions from the page's own Quick Facts tables.
Cards 1-2 keep their tested stamp (Rudas is personally tested, as on the thermal baths page)."""
import importlib.util
import os

_s = importlib.util.spec_from_file_location("_quickfacts", os.path.join(os.path.dirname(os.path.abspath(__file__)), "_quickfacts.py"))
_q = importlib.util.module_from_spec(_s)
_s.loader.exec_module(_q)

PAGE_FILE = "rudas-baths-budapest.html"
PAGE, CARDS = _q.build(PAGE_FILE, _q.anchors(PAGE_FILE), "tickets", [
    {"label": "When", "chips": [("day", "☀️ Day"), ("night", "🌙 Night"), ("weekday", "📅 Weekdays"), ("weekend", "🗓️ Weekends")]},
    {"label": "Extras &amp; proof", "chips": [("meal", "🍽️ Includes a meal"), ("couples", "💑 Couples"),
                                              ("budget", "💶 Under €30"), ("tested", "✓ Personally tested")]},
])
for _c in ("card-1", "card-2"):
    CARDS[_c]["tested"] = True
for _c in CARDS.values():
    _c["drop_rating_note"] = True
