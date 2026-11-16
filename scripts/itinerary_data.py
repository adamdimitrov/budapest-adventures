# -*- coding: utf-8 -*-
"""Facts for the Budapest itinerary page (/budapest-travel-guide), 16 Nov 2026.

Every product fact is taken from the card or Quick Facts of the same product on
another BPA page, which were read on the live listings on 14-15 Nov 2026:
  - Legenda sightseeing cruise: best-budapest-river-cruises.html (tested, 4.4 from 17k+ on 3 sites).
  - Parliament ticket + audio guide (GYG t731430): best-things-to-do-budapest.html card;
    official prices and hours from budapest-parliament.html (HUF 7,000 EU/EEA, HUF 14,000 others,
    45-minute tour, 8:00 to 16:00 Nov to Mar, arrive 15 minutes early).
  - St Stephen's Basilica entry (GYG t655129): best-things-to-do-budapest.html card.
  - Buda Castle walking tour (GYG t157275): best-walking-tours-budapest.html (daily 14:00 and 14:30,
    2 hours, Trinity Square, €12); tested per scripts/december_data.py.
  - Pub crawl (GYG t1068003): best-pub-crawls-budapest.html (from €2, starts 21:10, 21:40 or 22:20,
    Erzsébet körút 36, welcome shot at every venue).
  - Foodapest Market to Tavern (GYG t808482): best-food-tours-budapest.html (€62, 3 hours,
    Central Market Hall, pálinka and a wine tasting).
  - Széchenyi morning pass (GYG t4139): szechenyi-baths-budapest.html and december_data.py
    (€39 entry 7:00 to 9:00 Mon to Thu, €46 after, M1 Széchenyi fürdő); tested.
  - Danube Bend day trip (GYG t1470042, MazakEV): best-day-trips-from-budapest.html (€96, 8-9 hours,
    Batthyány tér, 4.9 from 37).
  - Airport: budapest-airport-to-city-center.html (100E bus 2,200 HUF / €6).
No em dashes in this file (house rule).
"""

GYG = ("https://www.getyourguide.com/budapest-l29/{slug}/?partner_id=YS414AJ&amp;utm_medium=online_publisher"
       "&amp;cmp=itinerary-{cmp}&amp;mkt_cmp=true")
GYG_OTHER = ("https://www.getyourguide.com/{loc}/{slug}/?partner_id=YS414AJ&amp;utm_medium=online_publisher"
             "&amp;cmp=itinerary-{cmp}&amp;mkt_cmp=true")
LEGENDA = "https://legenda.hu/en/ticket-purchase?partner=38585"

SITE_NAME = {"gyg": "GetYourGuide", "viator": "Viator", "tiqets": "Tiqets", "tripadvisor": "Tripadvisor"}

# (site, score, count, link-or-None)
PRODUCTS = [
    dict(key="parliament", src=("best-things-to-do-budapest.html", "Parliament Guided Tour"), n_photos=8,
         href=GYG.format(slug="budapest-parliament-tour-with-audio-guide-opt-boat-tour-t731430", cmp="parliament"),
         via="gyg", op="Hungarian Parliament", cats="d1", tested=False, price=43,
         ratings=[("gyg", 4.5, 6600, "self")]),
    dict(key="basilica", src=("best-things-to-do-budapest.html", "6. St. Stephen"), n_photos=8,
         href=GYG.format(slug="budapest-st-stephen-s-basilica-entry-with-options-t655129", cmp="basilica"),
         via="gyg", op="St Stephen's Basilica", cats="d1", tested=False, price=12,
         ratings=[("gyg", 4.6, 15800, "self")]),
    dict(key="legenda", src=("best-budapest-river-cruises.html", "legenda.hu"), n_photos=10,
         href=LEGENDA, via="direct", op="Legenda City Cruises", cats="d1 eve", tested=True, price=20,
         ratings=[("gyg", 4.5, 10900, None), ("viator", 4.3, 4200, None)]),
    dict(key="food", src=("best-food-tours-budapest.html", "t808482"), n_photos=8,
         href=GYG.format(slug="budapest-food-tour-market-to-tavern-14-tasters-wines-t808482", cmp="food-tour"),
         via="gyg", op="Foodapest", cats="d2", tested=False, price=62,
         ratings=[("gyg", 4.9, 679, "self")]),
    dict(key="castle", src=("best-walking-tours-budapest.html", "t157275"), n_photos=8,
         href=GYG.format(slug="budapest-classic-buda-castle-walking-tour-t157275", cmp="castle-walk"),
         via="gyg", op="Buda Castle District", cats="d2", tested=True, price=12,
         ratings=[("gyg", 4.6, 2400, "self")]),
    dict(key="crawl", src=("best-pub-crawls-budapest.html", "t1068003"), n_photos=8,
         href=GYG.format(slug="budapest-pub-crawl-ruin-bar-tour-free-shots-vip-entry-t1068003", cmp="pub-crawl"),
         via="gyg", op="Ruin bar pub crawl", cats="d2 eve", tested=False, price=2,
         ratings=[("gyg", 4.9, 3800, "self")]),
    dict(key="szechenyi", src=("szechenyi-baths-budapest.html", "t4139"), n_photos=8,
         href=GYG.format(slug="szechenyi-spa-full-day-entrance-pass-t4139", cmp="szechenyi"),
         via="gyg", op="Széchenyi Bath", cats="d3", tested=True, price=39,
         ratings=[("gyg", 4.28, 29228, "self"), ("tiqets", 4.4, 1200, None), ("viator", 3.8, 2300, None)]),
    dict(key="daytrip", src=("best-day-trips-from-budapest.html", "t1470042"), n_photos=8,
         href=GYG_OTHER.format(loc="visegrad-l1566", slug="from-budapest-danube-bend-day-trip-with-visegrad-and-szentendre-t1470042", cmp="day-trip"),
         via="gyg", op="MazakEV", cats="d4", tested=False, price=96,
         ratings=[("gyg", 4.9, 37, "self")]),
]
