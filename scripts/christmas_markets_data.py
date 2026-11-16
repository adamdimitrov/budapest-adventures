# -*- coding: utf-8 -*-
"""Facts for the Budapest Christmas Markets 2026 page (all languages).

Copy lives in scripts/christmas_markets_copy_<lang>.py; the builder is
scripts/build_christmas_markets.py. Change a fact here, then rerun the builder.

Every market fact below was read on 14-15 Nov 2026 from the organiser's own
website (see "sources"). Food prices are not published by the organisers; the
2026 figures come from the organisers' opening statement quoted by Hungarian
media (MTI) and from on-site price checks published on 13 Nov 2026, as noted
per price. Product facts were read on the GetYourGuide / Viator / Silverline
listing and the GetYourGuide booking calendar (December 2026) on 15 Nov 2026.
No em dashes in this file (house rule).
"""
import math

CHECKED = "2026-11-15"

GYG = "https://www.getyourguide.com/budapest-l29/{slug}/?partner_id=YS414AJ&utm_medium=online_publisher&cmp=xmas-markets-{cmp}&mkt_cmp=true"
VIATOR = "https://tp.media/r?campaign_id=47&marker=404154&p=1922&sub_id=xmas-markets-{cmp}&trs=204442&u=https%3A%2F%2Fwww.viator.com%2Ftours%2FBudapest%2F{slug}"

# ---------------------------------------------------------------- markets
# coordinates are the market's centre point (used for the walking matrix)
MARKETS = [
    {
        "key": "basilica",
        "anchor": "market-advent-bazilika",
        "name": "Advent Bazilika",
        "place": "Szent István tér",
        "district": "V.",
        "address": "Szent István tér, 1051 Budapest",
        "map_q": "Szent István tér Budapest",
        "lat": 47.50080, "lng": 19.05390,
        "start": "2026-11-13", "end": "2027-01-01",
        "hours": {"mon_thu": "11:00-22:00", "fri_sat": "11:00-23:00", "sun": "11:00-22:00",
                  "dec24": "11:00-15:00", "dec25": "11:00-20:00", "dec26": "11:00-20:00",
                  "dec31": "11:00-03:00", "jan1": "11:00-18:00"},
        "close_fri": 23,
        "light_show": "17:30",          # 3D projection on the Basilica facade, daily, every 30 min
        "rink": None,                   # no rink listed on the official 2026 site
        "free_entry": True,
        "exhibitors": "nearly 100 (official intro text; another block on the same page says nearly 150)",
        "fixed_dish_huf": 1600,         # one 1,600 Ft dish at every main kitchen (organiser statement)
        "transport": "M3 Arany János utca, M1/M2/M3 Deák Ferenc tér, bus 9, trolleybus 72",
        "official": "https://adventbazilika.hu/",
        "official_hours": "https://adventbazilika.hu/nyitvatartas",
        "sources": ["https://adventbazilika.hu/nyitvatartas", "https://adventbazilika.hu/programok",
                    "https://www.penzcentrum.hu/vasarlas/20261101/budapest-karacsonyi-vasar-2026-indul-az-adventi-szezon-mutatjuk-a-helyszineket-a-nyitvatartast-es-a-programokat-1208076"],
    },
    {
        "key": "vorosmarty",
        "anchor": "market-vorosmarty-ter",
        "name": "Vörösmarty Classic Xmas",
        "place": "Vörösmarty tér",
        "district": "V.",
        "address": "Vörösmarty tér, 1051 Budapest",
        "map_q": "Vörösmarty tér Budapest",
        "lat": 47.49660, "lng": 19.05050,
        "start": "2026-11-13", "end": "2026-12-31",
        "crafts_until": "2026-12-28",   # craft stalls and the mini train last day
        "hours": {"mon_thu": "11:00-21:00", "fri_sat": "11:00-22:00", "sun": "11:00-21:00",
                  "dec24": "10:00-14:00", "dec25": "12:00-18:00", "dec26": "12:00-18:00",
                  "dec31": "11:00-03:00", "jan1": None},
        "close_fri": 22,
        "light_show": None,
        "rink": None,
        "train": {"mon_fri": "14:00-20:00", "sat_sun": "11:00-20:00", "dec24": "10:00-14:00"},  # free mini train
        "free_entry": True,
        "transport": "M1 Vörösmarty tér (at the square), M1/M2/M3 Deák Ferenc tér",
        "official": "https://vorosmartyclassicxmas.hu/",
        "official_hours": "https://vorosmartyclassicxmas.hu/nyitvatartas/",
        "sources": ["https://vorosmartyclassicxmas.hu/nyitvatartas/",
                    "https://www.vg.hu/turizmus/2026/11/karacsonyi-vasar-arak-vorosmarty-ter-budapest"],
    },
    {
        "key": "castle",
        "anchor": "market-budavari-advent",
        "name": "Budavári Advent",
        "place": "Szentháromság tér",
        "district": "I.",
        "address": "Szentháromság tér, 1014 Budapest (by Mátyás-templom)",
        "map_q": "Szentháromság tér Budapest",
        "lat": 47.50190, "lng": 19.03430,
        "start": "2026-11-27", "end": "2027-01-03",
        "hours": {"mon_thu": "09:00-20:00", "fri_sat": "09:00-20:00", "sun": "09:00-20:00",
                  "dec24": "09:00-12:00", "dec25": None, "dec26": None,
                  "dec31": None, "jan1": "12:00-20:00"},
        "close_fri": 20,
        "light_show": None,
        "candles": ["2026-11-29", "2026-12-06", "2026-12-13", "2026-12-20"],  # 16:00, Szentháromság tér
        "rink": None,
        "free_entry": True,
        "transport": "bus 16 from Deák Ferenc tér to Szentháromság tér, or Budavári Sikló (funicular) from Clark Ádám tér",
        "official": "https://maraikult.hu/budavari-advent/",
        "official_hours": "https://maraikult.hu/budavari-advent/",
        "sources": ["https://maraikult.hu/budavari-advent/"],
    },
    {
        "key": "obuda",
        "anchor": "market-advent-obudan",
        "name": "Advent Óbudán",
        "place": "Fő tér",
        "district": "III.",
        "address": "Fő tér, 1033 Budapest",
        "map_q": "Fő tér Óbuda Budapest",
        "lat": 47.54100, "lng": 19.04470,
        "start": "2026-11-27", "end": "2026-12-23",
        "hours": {"mon_thu": "14:00-21:00", "fri": "14:00-22:00", "sat": "10:00-22:00", "sun": "10:00-21:00",
                  "dec24": None, "dec25": None, "dec26": None, "dec31": None, "jan1": None},
        "close_fri": 22,
        "light_show": None,
        "rink": {"free": True, "start": "2026-11-27", "end": "2027-01-31",
                 "hours": "Sun-Thu 08:00-21:00, Fri-Sat 08:00-22:00", "school_mornings": "08:00-12:00 weekdays may be reserved for schools",
                 "dec24": "08:00-12:00", "dec25": "12:00-20:00", "dec31": "08:00-12:00", "jan1": "12:00-20:00"},
        "free_entry": True,
        "transport": "HÉV H5 to Szentlélek tér (from Batthyány tér, M2)",
        "official": "https://www.adventobudan.hu/",
        "official_hours": "https://www.adventobudan.hu/adventi-vasar-obuda-fo-teren/",
        "sources": ["https://www.adventobudan.hu/adventi-vasar-obuda-fo-teren/", "https://www.adventobudan.hu/irany-a-jeg/"],
    },
]

# Market card photos: Wikimedia Commons, free licences, credited on the page (Sources section).
# (file in /assets/xmas-markets-2026/, author, licence, file page)
_EA = "Elekes Andor"
_C = "https://commons.wikimedia.org/wiki/File:"
MARKET_PHOTOS = {
    "basilica": [("market-basilica-%02d.avif" % i, _EA, "CC BY 4.0", _C + f) for i, f in enumerate([
        "Basilica_Christmas_Fair_2025_(2).jpg", "Basilica_Christmas_Fair_2025.jpg", "Basilica_Christmas_Fair_2025_(33).jpg",
        "Basilica_Christmas_Fair_2025_(20).jpg", "Basilica_Christmas_Fair_2025_(23).jpg", "Basilica_Christmas_Fair_2025_(21).jpg",
        "Basilica_Christmas_Fair_2025_(18).jpg", "Basilica_Christmas_Fair_2025_(46).jpg"], 1)],
    "vorosmarty": [("market-vorosmarty-%02d.avif" % i, _EA, "CC BY 4.0", _C + f) for i, f in enumerate([
        "V%C3%B6r%C3%B6smarty_Christmas_Fair_2025_(18).jpg", "V%C3%B6r%C3%B6smarty_Christmas_Fair_2025_(20).jpg",
        "V%C3%B6r%C3%B6smarty_Christmas_Fair_2025_(15).jpg", "V%C3%B6r%C3%B6smarty_Christmas_Fair_2025_(34).jpg",
        "V%C3%B6r%C3%B6smarty_Christmas_Fair_2025_(22).jpg", "V%C3%B6r%C3%B6smarty_Christmas_Fair_2025_(25).jpg",
        "V%C3%B6r%C3%B6smarty_Christmas_Fair_2025_(1).jpg", "V%C3%B6r%C3%B6smarty_Christmas_Fair_2025_(5).jpg"], 1)],
    "castle": [
        ("market-castle-01.avif", "Thaler Tamás", "CC BY-SA 4.0", _C + "MatyasTemplomFotoThalerTamas20162.JPG"),
        ("market-castle-02.avif", "Andrés Nieto Porras", "CC BY-SA 2.0", _C + "Views_from_Fisherman%27s_Bastion_toward_south._-_Budapest,_Hungary._-_62_365%C2%B2_Observador_(8262965486).jpg"),
        ("market-castle-03.avif", "Jorge Franganillo", "CC BY 2.0", _C + "Budapest_Fisherman%27s_Bastion_(54171700818).jpg"),
    ],
    "obuda": [
        ("market-obuda-01.avif", "Globetrotter19", "CC BY-SA 3.0", _C + "%C3%93buda_F%C5%91_Square_Ice_Rink._-_2016_Budapest.jpg"),
        ("market-obuda-02.avif", "Globetrotter19", "CC BY-SA 3.0", _C + "Town_Hall_in_F%C5%91_Square,_%C3%93buda,_2016_Budapest.jpg"),
    ],
}

# Markets we looked for and left out: no 2026 programme published by 15 Nov 2026
LEFT_OUT = ["Várkert Bazár", "Erzsébet tér"]

# ---------------------------------------------------------------- prices (HUF, 2026)
PRICES = {
    "mulled_wine": 1500,      # organisers' statement, both central markets (MTI, 13-14 Nov 2026)
    "langos_plain": 2400,     # organisers' statement
    "kids_menu_under": 1000,  # organisers' statement: kids' menu under 1,000 Ft
    "fixed_dish": 1600,       # Advent Bazilika: one 1,600 Ft dish at each main kitchen; Vörösmarty: 1,600 Ft offer dishes
    "langos_cheese": 3200,    # Vörösmarty tér, cheese and sour cream, on-site check (vg.hu, 13 Nov 2026)
    "goulash_bread": 5700,    # Vörösmarty tér, goulash in a bread bowl, on-site check (vg.hu)
    "chestnuts": 3000,        # Vörösmarty tér, roasted chestnuts, on-site check (vg.hu)
    "kurtos": None,           # no 2026 price published at opening
}
PRICE_SOURCES = [
    "https://www.okoshir.hu/2026/11/14/megnyilt-az-advent-bazilika-es-a-vorosmarty-classic-xmas-1500-forintba-kerul-a-forralt-bor/",
    "https://www.vg.hu/turizmus/2026/11/karacsonyi-vasar-arak-vorosmarty-ter-budapest",
]

# evening budgets per person, built only from the 2026 prices above
BUDGETS = [
    ("light", [("mulled_wine", 1), ("fixed_dish", 1)]),
    ("classic", [("mulled_wine", 2), ("langos_cheese", 1)]),
    ("hearty", [("mulled_wine", 2), ("goulash_bread", 1), ("chestnuts", 1)]),
]


def budget_total(items):
    return sum(PRICES[k] * n for k, n in items)


# ---------------------------------------------------------------- walking matrix
# straight-line distance x 1.3 street factor, at 80 m per minute; Castle Hill adds a climb
def walk_minutes(a, b):
    r = 6371000.0
    p1, p2 = math.radians(a["lat"]), math.radians(b["lat"])
    dp, dl = p2 - p1, math.radians(b["lng"] - a["lng"])
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    d = 2 * r * math.asin(math.sqrt(h)) * 1.3
    return int(round(d / 80.0)), int(round(d / 10.0) * 10)


TRANSIT = {  # point-to-point public transport for legs too long to walk (BKK lines, 15 Nov 2026)
    ("vorosmarty", "castle"): "bus 16 from Deák Ferenc tér",
    ("basilica", "castle"): "bus 16 from Deák Ferenc tér",
    ("vorosmarty", "obuda"): "M2 to Batthyány tér + HÉV H5 to Szentlélek tér",
    ("basilica", "obuda"): "M2 to Batthyány tér + HÉV H5 to Szentlélek tér",
    ("castle", "obuda"): "bus 16 to Batthyány tér + HÉV H5 to Szentlélek tér",
}

# ---------------------------------------------------------------- bookable programs
PRODUCTS = [
    {
        "key": "wonderland",
        "market": "basilica",
        "anchor": "program-1-christmas-market-tasting-tour",
        "rank_class": "bpa-gold",
        "operator": "Budapest Urban Walks",
        "brand": "Budapest Urban Walks",
        "pier": "Hungarian State Opera",
        "pier_map": "Hungarian State Opera Budapest Andrássy út 22",
        "book": GYG.format(slug="budapest-wonderland-christmas-market-tour-with-treats-t444209", cmp="wonderland"),
        "book_via": "gyg",
        "links": {"gyg": GYG.format(slug="budapest-wonderland-christmas-market-tour-with-treats-t444209", cmp="wonderland"),
                  "viator": VIATOR.format(slug="Budapest-Wonderland-A-Christmas-Market-Tour/d499-51057P14", cmp="wonderland")},
        "ratings": [("gyg", 4.90, 8), ("viator", 5.0, 15)],
        "price_from": 90, "price_high": 90, "unit": "person",
        "december": "every day 1-31 Dec bookable on the GetYourGuide calendar (checked 15 Nov 2026)",
        "images": ["wonderland-tasting-tour-%02d.avif" % i for i in range(1, 11)],
    },
    {
        "key": "chimney-tour",
        "market": "basilica",
        "anchor": "program-2-christmas-markets-chimney-cake-tour",
        "rank_class": "bpa-blue",
        "operator": "Living Local Hungary",
        "brand": "Living Local Hungary",
        "pier": "Károly krt. 1",
        "pier_map": "Károly körút 1 Budapest",
        "book": GYG.format(slug="budapest-christmas-markets-tour-with-chimney-cake-tasting-t546145", cmp="chimney-tour"),
        "book_via": "gyg",
        "links": {"gyg": GYG.format(slug="budapest-christmas-markets-tour-with-chimney-cake-tasting-t546145", cmp="chimney-tour")},
        "ratings": [("gyg", 4.28, 9)],
        "price_from": 49, "price_high": 49, "unit": "person",
        "december": "every day 1-31 Dec bookable (checked 15 Nov 2026)",
        "images": ["chimney-cake-markets-tour-%02d.avif" % i for i in range(1, 5)],
    },
    {
        "key": "market-cruise",
        "market": "vorosmarty",
        "anchor": "program-3-christmas-market-cruise",
        "rank_class": "bpa-emerald",
        "operator": "Floating Lotus",
        "brand": "CEE Gastro Group kft",
        "pier": "Dock 9, Petőfi tér",
        "pier_map": "Petőfi tér 9 Budapest Dock 9",
        "book": GYG.format(slug="budapest-christmas-market-cruise-with-unlimited-drinks-t1547619", cmp="market-cruise"),
        "book_via": "gyg",
        "links": {"gyg": GYG.format(slug="budapest-christmas-market-cruise-with-unlimited-drinks-t1547619", cmp="market-cruise")},
        "ratings": [],
        "price_from": 39, "price_high": 44, "unit": "person",
        "december": "bookable 1-31 Dec except 24 and 31 Dec (checked 15 Nov 2026)",
        "images": ["floating-christmas-market-cruise-%02d.avif" % i for i in range(1, 6)],
    },
    {
        "key": "mulled-cruise",
        "market": "vorosmarty",
        "anchor": "program-4-unlimited-mulled-wine-cruise",
        "rank_class": "bpa-slate",
        "operator": "Silverline Cruises",
        "brand": "Silverline Cruises",
        "pier": "Dock 11, Jane Haining rkp.",
        "pier_map": "Jane Haining rakpart Dock 11 Budapest",
        "book": "https://budapestrivercruise.eu/product/unlimited-mulled-wine-cruise/?code=bpadventures",
        "book_via": "direct",
        "links": {},  # direct Silverline link pays more: review entries stay unlinked
        "ratings": [("gyg", 4.61, 263), ("viator", 4.5, 22)],
        "price_from": 21, "price_high": 21, "unit": "person",
        "december": "bookable in December except 15 and 24-26 Dec on the GetYourGuide calendar of the same cruise (checked 15 Nov 2026)",
        "images": ["../xmas-2026/budapest-christmas-cruise-mulled-wine-%02d.avif" % i for i in range(1, 11)],
    },
    {
        "key": "castle-tour",
        "market": "castle",
        "anchor": "program-5-buda-castle-royal-cake-tour",
        "rank_class": "bpa-gold",
        "operator": "Tour X",
        "brand": "Tour X",
        "pier": "Hess András tér 1-3",
        "pier_map": "Hess András tér 1 Budapest",
        "book": GYG.format(slug="buda-castle-guided-walking-tour-with-royal-cake-tasting-t1262726", cmp="castle-cake"),
        "book_via": "gyg",
        "links": {"gyg": GYG.format(slug="buda-castle-guided-walking-tour-with-royal-cake-tasting-t1262726", cmp="castle-cake"),
                  "viator": VIATOR.format(slug="Gems-of-the-Budapest-Castle-District-Free-Walking-Tour/d499-5519866P1", cmp="castle-cake")},
        "ratings": [("gyg", 4.83, 388), ("viator", 5.0, 83)],
        "price_from": 16, "price_high": 20, "unit": "person",
        "december": "every day 1-31 Dec bookable (checked 15 Nov 2026)",
        "images": ["buda-castle-royal-cake-tour-%02d.avif" % i for i in range(1, 11)],
    },
    {
        "key": "obuda-tour",
        "market": "obuda",
        "anchor": "program-6-christmas-markets-walking-tour-obuda",
        "rank_class": "bpa-blue",
        "operator": "SzeRita",
        "brand": "SzeRita",
        "pier": "Budapest Eye, Erzsébet tér",
        "pier_map": "Budapest Eye Erzsébet tér",
        "book": GYG.format(slug="budapest-christmas-markets-walking-tour-t1551827", cmp="obuda-walk"),
        "book_via": "gyg",
        "links": {"gyg": GYG.format(slug="budapest-christmas-markets-walking-tour-t1551827", cmp="obuda-walk")},
        "ratings": [],
        "price_from": 18, "price_high": 20, "unit": "person",
        "december": "bookable 2-31 Dec (1 Dec closed), checked 15 Nov 2026; the Óbuda market itself closes on 23 Dec",
        "images": ["obuda-markets-walking-tour-%02d.avif" % i for i in range(1, 5)],
    },
    {
        "key": "workshop",
        "market": "food",
        "anchor": "program-7-chimney-cake-workshop",
        "rank_class": "bpa-emerald",
        "operator": "Bespoke Adventure Makers",
        "brand": "Bespoke Adventure Makers kft",
        "pier": "Ipar u. 11",
        "pier_map": "Ipar utca 11 Budapest 1095",
        "book": GYG.format(slug="budapest-traditional-chimney-cake-kurtoskalacs-workshop-t1151683", cmp="chimney-workshop"),
        "book_via": "gyg",
        "links": {"gyg": GYG.format(slug="budapest-traditional-chimney-cake-kurtoskalacs-workshop-t1151683", cmp="chimney-workshop"),
                  "viator": VIATOR.format(slug="Budapest-Traditional-Chimney-Cake-Kurtoskalacs-Workshop/d499-5628611P3", cmp="chimney-workshop")},
        "ratings": [("gyg", 4.87, 1733), ("viator", 5.0, 460)],
        "price_from": 20, "price_high": 24, "unit": "person",
        "december": "every day 1-31 Dec bookable (checked 15 Nov 2026)",
        "images": ["chimney-cake-workshop-%02d.avif" % i for i in range(1, 11)],
    },
]

SISTER = {  # the Christmas cruises page in each language (no translation: link the EN page)
    "en": "/christmas-cruises-budapest",
    "de": "/de/weihnachts-bootsfahrten-budapest",
    "es": "/es/cruceros-navidad-budapest",
    "fr": "/christmas-cruises-budapest",
    "it": "/christmas-cruises-budapest",
    "hu": "/christmas-cruises-budapest",
    "ro": "/christmas-cruises-budapest",
    "hr": "/hr/bozicna-krstarenja-budimpesta",
    "sr": "/christmas-cruises-budapest",
    "pl": "/christmas-cruises-budapest",
}


def weighted(ratings):
    n = sum(c for _, _, c in ratings)
    if not n:
        return None, 0
    return sum(r * c for _, r, c in ratings) / n, n
