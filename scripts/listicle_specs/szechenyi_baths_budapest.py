# -*- coding: utf-8 -*-
"""Upgrade spec for szechenyi-baths-budapest.html: questions from the page's own Quick Facts tables.
Card 1 keeps its tested stamp (Széchenyi is personally tested, as on the thermal baths page)."""
import importlib.util
import os

_s = importlib.util.spec_from_file_location("_quickfacts", os.path.join(os.path.dirname(os.path.abspath(__file__)), "_quickfacts.py"))
_q = importlib.util.module_from_spec(_s)
_s.loader.exec_module(_q)

PAGE_FILE = "szechenyi-baths-budapest.html"
PAGE, CARDS = _q.build(PAGE_FILE, _q.anchors(PAGE_FILE), "tickets", [
    {"label": "Ticket type", "chips": [("day", "🎟️ Day tickets"), ("night", "🎉 Night party"), ("upgrade", "💎 Upgrades")]},
])
CARDS["card-1"]["tested"] = True
# card 5 has only 4 quick facts; the fifth question uses its own Pick/Skip line
CARDS["card-5"]["faq"].insert(1, ("Is it worth it on a weekday?",
                                   "Not really: the regular day ticket also skips the cashier at the validation machines and costs €13 less. "
                                   "Fast track pays off on weekend and holiday afternoons, when the main entrance queues."))
for _c in CARDS.values():
    _c["drop_rating_note"] = True
