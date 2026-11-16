# -*- coding: utf-8 -*-
"""Facts and copy for the private boat tours page (all languages).

Every number below was read from the live listing on 14 Nov 2026
(GetYourGuide product page + booking calendar for Wed 18 Nov and Sat 21 Nov 2026,
Viator product page). Change a fact here, then rerun scripts/build_private_boats.py.
"""

CHECKED = "2026-11-14"

GYG = "https://www.getyourguide.com/budapest-l29/{slug}/?partner_id=YS414AJ&utm_medium=online_publisher&cmp=private-cruises-{cmp}&mkt_cmp=true"
VIATOR = "https://tp.media/r?campaign_id=47&marker=404154&p=1922&sub_id=private-cruises-{cmp}&trs=204442&u=https%3A%2F%2Fwww.viator.com%2Ftours%2FBudapest%2F{slug}"

# ---------------------------------------------------------------- facts
PRODUCTS = [
    {
        "key": "portum-private",
        "anchor": "boat-1-portum-private",
        "cat": "small groups20",
        "rank_class": "bpa-gold",
        "operator": "Portum Lines",
        "brand": "Portum Lines Cruising",
        "pier": "Dock 42",
        "pier_map": "Dock 42 Szent István park Budapest",
        "address": "Dock 42 port, Szent István park, 1138 Budapest",
        "gyg": GYG.format(slug="budapest-1-hour-private-boat-cruise-t115605", cmp="portum-1h"),
        "viator": VIATOR.format(slug="Budapest-Private-Boat-Tour/d499-14765P5", cmp="portum-1h"),
        "ratings": [("gyg", 4.87, 52), ("viator", 3.3, 9)],
        "price_from": 225, "price_high": 275, "capacity": 20,
        "images": ["portum-private-boat-%d.webp" % i for i in range(1, 9)],
    },
    {
        "key": "dunarama",
        "anchor": "boat-2-dunarama-water-limo",
        "cat": "small luxury",
        "rank_class": "bpa-blue",
        "operator": "Dunarama",
        "brand": "Dunarama private cruise service",
        "pier": "Jane Haining rkp. 8a",
        "pier_map": "Jane Haining rakpart 8a Budapest",
        "address": "Jane Haining rkp. 8a, 1051 Budapest",
        "gyg": GYG.format(slug="luxury-danube-water-limousine-cruise-t123737", cmp="dunarama-water-limo"),
        "viator": VIATOR.format(slug="Cruise-on-the-Danube-with-DunaTaxi/d499-50946P2", cmp="dunarama-water-limo"),
        "ratings": [("gyg", 4.18, 12), ("viator", 4.6, 17)],
        "price_from": 580, "price_high": 580, "capacity": 10,
        "images": ["dunarama-water-limo-%d.webp" % i for i in range(1, 10)],
    },
    {
        "key": "portum-party",
        "anchor": "boat-3-portum-party-boat",
        "cat": "groups20 party",
        "rank_class": "bpa-emerald",
        "operator": "Portum Lines",
        "brand": "Portum Lines Cruising",
        "pier": "Dock 42",
        "pier_map": "Dock 42 Szent István park Budapest",
        "address": "Dock 42 port, Szent István park, 1138 Budapest",
        "gyg": GYG.format(slug="budapest-1-hour-party-boat-with-free-drinks-t342906", cmp="stag-party"),
        "viator": VIATOR.format(slug="One-hour-Hen-or-Stag-party-boat-with-free-drinks/d499-14765P15", cmp="stag-party"),
        "ratings": [("gyg", 4.96, 10), ("viator", 3.5, 6)],
        "price_from": 450, "price_high": 550, "capacity": 20,
        "images": ["portum-party-boat-%d.webp" % i for i in range(1, 7)],
    },
    {
        "key": "magical",
        "anchor": "boat-4-magical-budapest",
        "cat": "small groups20 party",
        "rank_class": "bpa-slate",
        "operator": "Magical Budapest",
        "brand": "Magical Budapest Small Group & Private Tours (Aquincum MM Kft)",
        "pier": None,
        "pier_map": None,
        "address": None,
        "gyg": GYG.format(slug="rent-your-own-private-boat-in-budapest-t1030505", cmp="magical-rent-boat"),
        "viator": None,
        "ratings": [],
        "price_from": 495, "price_high": 765, "capacity": 35,
        "images": ["magical-private-boat-%d.webp" % i for i in range(1, 11)],
    },
]


def weighted(ratings):
    n = sum(c for _, _, c in ratings)
    if not n:
        return None, 0
    return sum(r * c for _, r, c in ratings) / n, n
