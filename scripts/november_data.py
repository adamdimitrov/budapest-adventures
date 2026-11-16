# -*- coding: utf-8 -*-
"""Facts for "Things to Do in Budapest in November" (EN + HU), 15 Nov 2026.

Products: read on the live listings on 15 Nov 2026 in Chrome.
  - Legenda Danube Legend: legenda.hu/en/danube-legend (25 EUR adult, 22.50 student,
    17.50 child 10-14, free 0-9) and legenda.hu/en/timetable (evening cruises
    25 Oct-22 Nov: 16:20 to 21:00 every 20 min; 23 Nov-31 Dec: 15:40 added).
    GYG t105820: 4.5, 10,999 reviews. Viator / Tripadvisor counts as recorded
    for this exact product in scripts/night_cruises_data.py (14 Nov 2026).
  - Legenda candlelit dinner: legenda.hu/en/candlelit-dinner-cruise (110 EUR,
    kids 3-12 84 EUR), timetable 19:00 daily.
  - Silverline Dinner & Lights: budapestrivercruise.eu/product/dinner-lights (from 77 EUR,
    window seat +15 EUR). Ratings as in scripts/dinner_cruises_2026_data.py.
  - GYG pages (from price and rating on the product page): Szechenyi t4139 from 39 EUR,
    4.3 (29,228); Rudas t233617 from 75 EUR (calendar price 74.99), 4.2 (1,422);
    Vampires night tour t59444 from 18 EUR (sale price, 20 EUR struck through), 4.6 (4,644),
    Sat 21 Nov start 20:00; Foodapest t808482 from 62 EUR (sale price, 69 EUR struck through),
    4.9 (679), starts 11:30 (market tour) and 17:00 (evening tour, no market, costs more);
    GYG shows "From <old> <new>": the second, lower figure is the bookable from-price (16 Nov 2026); Buda Castle walk t157275 from 12 EUR, 4.6 (2,418).

Personally tested (as marked on the user's other pages): Legenda Danube Legend and
candlelit dinner, Silverline dinner, Szechenyi, Rudas, the vampire night walk and
the Buda Castle District walk. Foodapest is NOT tested.

Events and seasonal facts (read 15 Nov 2026):
  - Christmas markets: scripts/christmas_markets_data.py (organisers' sites, 14-15 Nov).
  - City Park Ice Rink: mujegpalya.hu, "planned" opening 20 November.
  - Bonjour Monsieur Gauguin: szepmuveszeti.hu, 30 Oct 2026 - 28 Feb 2027, Tue-Sun 10-18, closed Mon.
  - Art Weekend Budapest: 27-29 Nov 2026, free, walks need registration (welovebudapest / artrabbit listings).
  - Lumina Park: luminapark.hu, Palatinus on Margaret Island, 16:30-21:00, closed Mondays,
    normal ticket 5,000 HUF Mon-Thu, 5,300 HUF Fri-Sun.
  - Sunrise / sunset: timeanddate.com, Budapest, November 2026.
  - Climate: HungaroMet (met.hu), Budapest-Pestszentlorinc, 1991-2020 normals for November.
No em dashes in this file (house rule).
"""

GYG = ("https://www.getyourguide.com/budapest-l29/{slug}/?partner_id=YS414AJ&amp;utm_medium=online_publisher"
       "&amp;cmp=november-{cmp}&amp;mkt_cmp=true")
SILVER = "https://budapestrivercruise.eu/product/{slug}/?code=bpadventures"
LEGENDA_DL = "https://legenda.hu/en/ticket-purchase?partner=38585"
LEGENDA_DINNER = "https://legenda.hu/en/ticket-purchase?partner=38585"

# (site, score, count, link-or-None). Links only when the card books through GYG.
PRODUCTS = [
    dict(key="legenda-evening", src=("best-night-cruises-budapest.html", "Danube Legend Evening Cruise"), n_photos=8,
         href=LEGENDA_DL, via="direct", op="Legenda City Cruises", cats="river dark u40",
         tested=True, price=25,
         ratings=[("gyg", 4.5, 10999, None), ("viator", 4.3, 4255, None), ("tripadvisor", 4.3, 2294, None)]),
    dict(key="szechenyi", src=("thermal-baths-budapest.html", "t4139"), n_photos=8,
         href=GYG.format(slug="szechenyi-spa-full-day-entrance-pass-t4139", cmp="szechenyi"), via="gyg",
         op="Széchenyi Bath", cats="bath u40", tested=True, price=39,
         ratings=[("gyg", 4.28, 29228, "self"), ("tiqets", 4.4, 1200, None), ("viator", 3.8, 2300, None)]),
    dict(key="legenda-dinner", src=("best-dinner-cruises-budapest.html", "4-Course Romantic Candlelit Dinner Cruise"), n_photos=10,
         href=LEGENDA_DINNER, via="direct", op="Legenda City Cruises", cats="river dark food",
         tested=True, price=110,
         ratings=[("gyg", 4.712, 2432, None), ("viator", 4.7, 2056, None), ("tripadvisor", 4.6, 1005, None)]),
    dict(key="rudas", src=("thermal-baths-budapest.html", "t233617"), n_photos=9,
         href=GYG.format(slug="budapest-rudas-turkish-bath-spa-day-pass-3-course-meal-t233617", cmp="rudas"), via="gyg",
         op="Rudas Bath", cats="bath dark food", tested=True, price=74.99,
         ratings=[("gyg", 4.19, 1422, "self")]),
    dict(key="vampire", src=("best-walking-tours-budapest.html", "t59444"), n_photos=6,
         href=GYG.format(slug="budapest-the-legendary-vampires-at-the-castle-s-court-t59444", cmp="vampire-walk"), via="gyg",
         op="Mysterium Tours", cats="dark u40", tested=True, price=18,
         ratings=[("gyg", 4.6, 4644, "self")]),
    dict(key="silverline", src=("best-dinner-cruises-budapest.html", "dinner-lights/"), n_photos=10,
         href=SILVER.format(slug="dinner-lights"), via="direct", op="Silverline Cruises", cats="river dark food",
         tested=True, price=77,
         ratings=[("gyg", 4.428, 1479, None), ("viator", 4.7, 577, None), ("tripadvisor", 4.7, 482, None)]),
    dict(key="foodapest", src=("best-food-tours-budapest.html", "t808482"), n_photos=5,
         href=GYG.format(slug="budapest-food-tour-market-to-tavern-14-tasters-wines-t808482", cmp="food-tour"), via="gyg",
         op="Foodapest", cats="food", tested=False, price=62,
         ratings=[("gyg", 4.86, 679, "self")]),
    dict(key="castle", src=("best-walking-tours-budapest.html", "t157275"), n_photos=6,
         href=GYG.format(slug="budapest-classic-buda-castle-walking-tour-t157275", cmp="castle-walk"), via="gyg",
         op="Tourist Angel", cats="u40", tested=True, price=12,
         ratings=[("gyg", 4.58, 2418, "self")]),
]

SITE_NAME = {"gyg": "GetYourGuide", "viator": "Viator", "tripadvisor": "Tripadvisor", "tiqets": "Tiqets"}

# timeanddate.com, Budapest, November 2026: date, sunrise, sunset, day length
SUN = [("1 Nov", "6:27", "16:26", "9 h 59 min"), ("15 Nov", "6:48", "16:07", "9 h 19 min"),
       ("30 Nov", "7:09", "15:55", "8 h 46 min")]
# HungaroMet, Budapest-Pestszentlorinc, November, 1991-2020
CLIMATE = dict(mean=5.9, high=9.4, low=3.1, rain_mm=48)
