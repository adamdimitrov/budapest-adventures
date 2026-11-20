# -*- coding: utf-8 -*-
"""Facts for "Things to Do in Budapest in December" (EN + HU), 15 Nov 2026.

Products (price, rating, what is included) were read on the live listings on
15 Nov 2026: GetYourGuide product pages (structured data), Silverline's own
product pages (budapestrivercruise.eu), Legenda's own pages (legenda.hu,
candlelit dinner page and timetable). Viator / Tiqets / Tripadvisor figures
are the per-product values recorded on 14-15 Nov 2026 in
scripts/christmas_markets_data.py, scripts/dinner_cruises_2026_data.py and
thermal-baths-budapest.html.

Personally tested (from the user's other pages): Legenda candlelit dinner
cruise, Széchenyi, Rudas, the Buda Castle District walking tour (t157275).
Silverline and Hungária Koncert were tested on their regular dinner cruises,
not on the Christmas menus, so those cards carry no "tested" mark.

Events (all read 15 Nov 2026):
  - Nutcracker dates: jegy.opera.hu ticket search (December 2026).
  - Christmas markets: scripts/christmas_markets_data.py (organisers' sites).
  - 24 December public holiday, shops closed: kormany.hu, 3 Nov 2026.
  - Széchenyi / Rudas hours: scripts/thermal_baths_data.py (official sites, 14 Nov).
  - City Park Ice Rink: mujegpalya.hu ("planned to start on 20 November").
  - Sunrise / sunset: timeanddate.com, Budapest, December 2026.
  - Climate: NOAA 1991-2020 normals for Budapest (WMO 12840), via Wikipedia.
No em dashes in this file (house rule).
"""

GYG = ("https://www.getyourguide.com/budapest-l29/{slug}/?partner_id=YS414AJ&amp;utm_medium=online_publisher"
       "&amp;cmp=december-{cmp}&amp;mkt_cmp=true")
SILVER = "https://budapestrivercruise.eu/product/{slug}/?code=bpadventures"
LEGENDA = "https://legenda.hu/en?partner=38585"

# (site, score, count, link-or-None). Links only when the card books through GYG.
PRODUCTS = [
    dict(key="legenda", src=("christmas-cruises-budapest.html", "legenda.hu"), n_photos=10,
         href=LEGENDA, via="direct", op="Legenda City Cruises", cats="xmas river",
         tested=True, price=110,
         ratings=[("gyg", 4.712, 2432, None), ("viator", 4.7, 2056, None), ("tripadvisor", 4.6, 1005, None)]),
    dict(key="silver-xmas", src=("christmas-cruises-budapest.html", "budapest-christmas-dinner-cruise/"), n_photos=9,
         href=SILVER.format(slug="budapest-christmas-dinner-cruise"), via="direct", op="Silverline Cruises",
         cats="xmas river", tested=False, price=155, ratings=[]),
    dict(key="szechenyi", src=("thermal-baths-budapest.html", "t4139"), n_photos=8,
         href=GYG.format(slug="szechenyi-spa-full-day-entrance-pass-t4139", cmp="szechenyi"), via="gyg",
         op="Széchenyi Bath", cats="bath u40", tested=True, price=39,
         ratings=[("gyg", 4.28, 29228, "self"), ("tiqets", 4.4, 1200, None), ("viator", 3.8, 2300, None)]),
    dict(key="wonderland", src=("budapest-christmas-markets.html", "t444209"), n_photos=8,
         href=GYG.format(slug="budapest-wonderland-christmas-market-tour-with-treats-t444209", cmp="market-tour"), via="gyg",
         op="Budapest Urban Walks", cats="xmas food", tested=False, price=90,
         ratings=[("gyg", 4.90, 8, "self"), ("viator", 5.0, 15, None)]),
    dict(key="rudas", src=("thermal-baths-budapest.html", "t233617"), n_photos=9,
         href=GYG.format(slug="budapest-rudas-turkish-bath-spa-day-pass-3-course-meal-t233617", cmp="rudas"), via="gyg",
         op="Rudas Bath", cats="bath food", tested=True, price=74.99,
         ratings=[("gyg", 4.19, 1422, "self")]),
    dict(key="mulled", src=("christmas-cruises-budapest.html", "t1049575"), n_photos=9,
         href=SILVER.format(slug="unlimited-mulled-wine-cruise"), via="direct", op="Silverline Cruises",
         cats="xmas river u40", tested=False, price=21,
         ratings=[("gyg", 4.61, 264, None), ("viator", 4.5, 22, None)]),
    dict(key="hungaria", src=("christmas-cruises-budapest.html", "t1593"), n_photos=10,
         href=GYG.format(slug="15-hour-danube-cruise-dinner-with-live-music-t1593", cmp="xmas-eve"), via="gyg",
         op="Hungária Koncert", cats="xmas river", tested=False, price=76,
         ratings=[("gyg", 4.38, 2255, "self")]),
    dict(key="workshop", src=("best-food-tours-budapest.html", "t1151683"), n_photos=5,
         href=GYG.format(slug="budapest-traditional-chimney-cake-kurtoskalacs-workshop-t1151683", cmp="chimney-workshop"), via="gyg",
         op="Bespoke Adventure Makers", cats="food u40", tested=False, price=19.56,
         ratings=[("gyg", 4.87, 1740, "self"), ("viator", 5.0, 460, None)]),
    dict(key="castle", src=("best-walking-tours-budapest.html", "t157275"), n_photos=6,
         href=GYG.format(slug="budapest-classic-buda-castle-walking-tour-t157275", cmp="castle-walk"), via="gyg",
         op="Tourist Angel", cats="u40", tested=True, price=12,
         ratings=[("gyg", 4.58, 2418, "self")]),
    dict(key="foodapest", src=("best-food-tours-budapest.html", "t808482"), n_photos=5,
         href=GYG.format(slug="budapest-food-tour-market-to-tavern-14-tasters-wines-t808482", cmp="food-tour"), via="gyg",
         op="Foodapest", cats="food", tested=False, price=62,
         ratings=[("gyg", 4.86, 679, "self")]),
    dict(key="nye", src=("new-years-eve-cruises-budapest.html", "new-years-celebration-cruise"), n_photos=10,
         href=SILVER.format(slug="new-years-celebration-cruise"), via="direct", op="Silverline Cruises",
         cats="river", tested=False, price=239, ratings=[]),
]

SITE_NAME = {"gyg": "GetYourGuide", "viator": "Viator", "tripadvisor": "Tripadvisor", "tiqets": "Tiqets"}

# Nutcracker, Hungarian State Opera House, December 2026 (jegy.opera.hu, 15 Nov 2026)
NUTCRACKER = [
    ("1", "19:00"), ("3", "19:00"), ("5", "11:00"), ("5", "18:00"), ("6", "11:00"), ("6", "18:00"),
    ("8", "19:00"), ("10", "19:00"), ("12", "11:00"), ("12", "18:00"), ("14", "19:00"), ("15", "19:00"),
    ("17", "18:00"), ("19", "11:00"), ("21", "11:00"), ("21", "18:00"), ("22", "11:00"), ("22", "18:00"),
    ("24", "11:00"), ("25", "11:00"), ("26", "11:00"), ("26", "18:00"), ("27", "11:00"), ("28", "18:00"),
    ("29", "11:00"), ("29", "18:00"), ("31", "13:00"), ("31", "21:00"),
]

SUN = [("1 Dec", "7:10", "15:54", "8 h 45 min"), ("10 Dec", "7:20", "15:52", "8 h 32 min"),
       ("21 Dec", "7:28", "15:55", "8 h 27 min"), ("31 Dec", "7:31", "16:02", "8 h 31 min")]
CLIMATE = dict(high=5.1, low=-0.2, rain_days=6.8, rain_mm=38, sun_hours=49)
