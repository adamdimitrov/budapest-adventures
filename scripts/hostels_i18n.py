# -*- coding: utf-8 -*-
"""Shared builder for translated hostel data files (hostels_data_<lang>.py).

Facts (ids, names, ratings, prices, addresses, categories, video URLs) come from
hostels_data_en.py; a language file only supplies the translated text per hostel.
"""
from hostels_data_en import HOSTELS as _EN

_FACTS = ("n", "id", "name", "brand", "area_q", "district", "address", "street", "zip",
          "hw", "bk", "dorm", "private", "cats", "tested")


def build(texts, floor_label=None):
    """texts: list of 10 dicts (same order as EN) with the translated text keys.
    A 'video' key holds only the translated link label; the URL comes from EN."""
    assert len(texts) == len(_EN)
    out = []
    for e, t in zip(_EN, texts):
        h = {k: e[k] for k in _FACTS}
        t = dict(t)
        label = t.pop("video", None)
        if e.get("video"):
            assert label, "missing video label for #%d" % e["n"]
            h["video"] = (e["video"][0], label)
        if floor_label:
            h["address"] = h["address"].replace("(1st floor)", "(%s)" % floor_label)
        h.update(t)
        h.setdefault("groups", [])
        out.append(h)
    return out
