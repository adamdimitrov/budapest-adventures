# -*- coding: utf-8 -*-
"""Facts + EN copy for the unlimited prosecco cruises page refresh.

Every number here was read from the live listing in Chrome on 14 Nov 2026
(availability/times for Saturday 28 Nov 2026). Sources are in SOURCES.
Only card "rubin-group" (GYG t416276) was personally tested.
No em dashes anywhere in copy.
"""

CHECKED = "14 November 2026"
CAL_DATE = "Saturday 28 November 2026"

GYG = "https://www.getyourguide.com/budapest-l29/"
VIATOR_AFF = "pid=P00072830&mcid=42383&medium=link&campaign="


def gyg(path, lang, placement, slug, mkt=True):
    u = f"{GYG}{path}/?partner_id=YS414AJ&utm_medium=online_publisher&cmp={lang}-prosecco-cruises-{placement}-{slug}"
    # mkt_cmp=true is required: without it GYG redirects partner links to a search page
    return u + "&mkt_cmp=true"


def viator(path, lang, slug):
    return f"https://www.viator.com/tours/Budapest/{path}?{VIATOR_AFF}{lang}-prosecco-cruises-rating-{slug}"


def maps(q):
    from urllib.parse import quote_plus
    return "https://www.google.com/maps/search/?api=1&query=" + quote_plus(q)


# ---------------------------------------------------------------------------
# Language-neutral facts (identical in all 16 languages)
# ---------------------------------------------------------------------------
CARDS = [
    {
        "slug": "rubin-group", "order": [10, 11, 12, 13, 5, 2, 14, 4, 1, 3, 8, 6], "anchor": "item-1-rubingroup", "tested": True,
        "cats": "tested prosecco sightseeing",
        "gyg_id": "t416276",
        "gyg_path": "budapest-unlimited-prosecco-beer-and-aperol-spritz-cruise-t416276",
        "operator": "Duna-Weser",
        "pier_maps": maps("Carl Lutz rakpart Dock 0 Budapest"),
        "price": "24.80", "price_label": "€24.80",
        "sites": [("GetYourGuide", 4.8, 51318, "gyg"),
                  ("Viator", 4.6, 3873, "viator:1-5-hours-evening-cruise-with-unlimited-Torley-sparkling-wine/d499-337865P1"),
                  ("Tripadvisor", 4.6, 2237, "ta")],
        "rank_color": "bpa-gold", "rank_emoji": "🏆",
        "photos": [
            "/assets/cdn/60e43c7d6d05b671dff0dc1a/650beeaa6847525facb1a507_best-unlimited-prosecco-cruises-hero.webp",
            "/assets/cdn/60e43c7d6d05b671dff0dc1a/63b858ea56f82257ea9e0c70_Budapest-river-cruises-portum-16.webp",
            "/assets/cdn/60e43c7d6d05b671dff0dc1a/63b858e8f731d90165d271cc_Budapest-river-cruises-portum-11.webp",
            "/assets/cdn/60e43c7d6d05b671dff0dc1a/63b858e9803ea5e532e13df1_Budapest-river-cruises-portum-15.webp",
            "/assets/cdn/60e43c7d6d05b671dff0dc1a/63b858e8a4e49cb177974356_Budapest-river-cruises-portum-14.webp",
            "/assets/cdn/60e43c7d6d05b671dff0dc1a/63b858eda4b537601bf3ceab_Budapest-river-cruises-portum-21.webp",
            "/assets/cdn/60e43c7d6d05b671dff0dc1a/63b858e92be2896fd573cf19_Budapest-river-cruises-portum-10.webp",
            "/assets/cdn/60e43c7d6d05b671dff0dc1a/63b858eb6b6209525005c772_Budapest-river-cruises-portum-17.webp",
            "/assets/cdn/60e43c7d6d05b671dff0dc1a/63b85c19bd509e80e2cfbd71_Budapest-river-cruises-legenda-1.webp",
            # 10-14: operator photos from the GYG product page (t416276), added to the own photos
        ] + [f"/assets/cdn/60e43c7d6d05b671dff0dc1a/prosecco-cruise-duna-weser-{i:02d}.avif" for i in range(1, 6)],
    },
    {
        "slug": "floating-lotus", "order": [1, 3, 2, 8, 6, 5, 9, 12, 10, 7, 4, 11], "anchor": "item-2-floating-lotus", "tested": False,
        "cats": "prosecco sightseeing",
        "gyg_id": "t1008035",
        "gyg_path": "budapest-lotus-cruise-with-unlimited-aperol-and-prosecco-t1008035",
        "operator": "Floating Lotus",
        "pier_maps": maps("Petőfi tér 9, 1052 Budapest"),
        "price": "17.50", "price_label": "€17.50",
        "sites": [("GetYourGuide", 4.6, 1777, "gyg")],
        "rank_color": "bpa-emerald", "rank_emoji": "💶",
        "photos": [f"/assets/cdn/60e43c7d6d05b671dff0dc1a/prosecco-cruise-floating-lotus-{i:02d}.avif" for i in range(1, 13)],
    },
    {
        "slug": "sip-and-sail", "order": [3, 1, 6, 5, 2, 4, 7, 8], "anchor": "item-3-sip-and-sail", "tested": False,
        "cats": "prosecco sightseeing",
        "gyg_id": "t508106",
        "gyg_path": "budapest-sip-sail-river-cruise-with-unlimited-prosecco-t508106",
        "operator": "Budapest Boat Party",
        "pier_maps": maps("Akadémia 2 ponton Budapest"),
        "price": "27", "price_label": "€27",
        "sites": [("GetYourGuide", 4.5, 920, "gyg"),
                  ("Viator", 4.6, 726, "viator:Budapest-Sunset-Danube-Cruise-with-Unlimited-Prosecco/d499-69242P4"),
                  ("Tripadvisor", 4.7, 610, "ta")],
        "rank_color": "bpa-blue", "rank_emoji": "🥂",
        "photos": [f"/assets/cdn/60e43c7d6d05b671dff0dc1a/prosecco-cruise-sip-and-sail-{i:02d}.avif" for i in range(1, 9)],
    },
    {
        "slug": "silverline-prosecco", "order": [2, 4, 3, 1, 5, 7, 10, 6, 9], "anchor": "item-4-silverline-prosecco", "tested": False,
        "cats": "prosecco sightseeing",
        "gyg_id": "t408167",
        "gyg_path": "budapest-sunset-cocktail-cruise-t408167",
        "operator": "Silverline Cruises",
        "pier_maps": maps("Silverline Cruises Dokk 11 Jane Haining rakpart Budapest"),
        "price": "27", "price_label": "€27",
        "sites": [("GetYourGuide", 4.5, 1044, "gyg"),
                  ("Viator", 4.4, 123, "viator:Gin-Tonic-Cocktail-Lounge-Cruise/d499-15186P48"),
                  ("Tripadvisor", 4.7, 87, "ta")],
        "rank_color": "bpa-slate", "rank_emoji": "⏱️",
        "photos": [f"/assets/cdn/60e43c7d6d05b671dff0dc1a/prosecco-cruise-silverline-{i:02d}.avif" for i in range(1, 11)],
    },
    {
        "slug": "dinner-drinks", "order": [3, 7, 6, 10, 9, 8, 2, 4, 11, 5, 12, 1], "anchor": "item-5-unlimited-drinks-dinner", "tested": False,
        "cats": "prosecco dinner",
        "gyg_id": "t494832",
        "gyg_path": "budapest-premium-dinner-cruise-live-music-unlimited-drinks-t494832",
        "operator": "Duna-Weser (River Diva)",
        "pier_maps": maps("Akadémia 3 ponton, Széchenyi rkp. 2, 1054 Budapest"),
        "price": "99", "price_label": "€99",
        "sites": [("GetYourGuide", 4.8, 2714, "gyg"),
                  ("Viator", 4.7, 62, "viator:Budapest-Festive-Dinner-Cruise-River-Diva-Exclusive/d499-337865P6"),
                  ("Tripadvisor", 4.7, 35, "ta")],
        "rank_color": "bpa-gold", "rank_emoji": "🍽️",
        "photos": [f"/assets/cdn/60e43c7d6d05b671dff0dc1a/prosecco-cruise-river-diva-{i:02d}.avif" for i in range(1, 13)],
        "mkt": True,
    },
    {
        "slug": "unlimited-cocktails", "order": [1, 8, 7, 5, 3, 2, 4, 9, 6, 10], "anchor": "item-6-unlimited-cocktails", "tested": False,
        "cats": "otherdrinks sightseeing", "extra": True,
        "gyg_id": "t781483",
        "gyg_path": "budapest-sightseeing-river-cruise-with-unlimited-cocktails-t781483",
        "operator": "Budapest Boat Party",
        "pier_maps": maps("Akadémia 2 ponton Budapest"),
        "price": "27", "price_label": "€27",
        "sites": [("GetYourGuide", 4.5, 1386, "gyg")],
        "rank_color": "bpa-slate", "rank_emoji": "🍹",
        "photos": [f"/assets/cdn/60e43c7d6d05b671dff0dc1a/prosecco-cruise-unlimited-cocktails-{i:02d}.avif" for i in range(1, 11)],
    },
    {
        "slug": "party-boat", "order": [1, 4, 2, 3, 8, 5, 6, 7, 9], "anchor": "item-7-party-boat", "tested": False,
        "cats": "otherdrinks party", "extra": True,
        "gyg_id": "t333211",
        "gyg_path": "budapest-boat-party-on-the-river-danube-with-drinks-t333211",
        "operator": "Budapest Boat Party",
        "pier_maps": maps("Akadémia 2 ponton Budapest"),
        "price": "62", "price_label": "€62",
        "sites": [("GetYourGuide", 4.1, 1235, "gyg"),
                  ("Viator", 4.9, 755, "viator:Danube-Beat-Boat-Party-Cruise/d499-69242P1"),
                  ("Tripadvisor", 4.9, 748, "ta")],
        "rank_color": "bpa-slate", "rank_emoji": "🎉",
        "photos": [f"/assets/cdn/60e43c7d6d05b671dff0dc1a/prosecco-cruise-danube-beat-party-{i:02d}.avif" for i in range(1, 10)],
    },
]

SOURCES = {
    "rubin-group": "https://www.getyourguide.com/budapest-l29/budapest-unlimited-prosecco-beer-and-aperol-spritz-cruise-t416276/",
    "floating-lotus": "https://www.getyourguide.com/budapest-l29/budapest-lotus-cruise-with-unlimited-aperol-and-prosecco-t1008035/",
    "sip-and-sail": "https://www.getyourguide.com/budapest-l29/budapest-sip-sail-river-cruise-with-unlimited-prosecco-t508106/",
    "silverline-prosecco": "https://www.getyourguide.com/budapest-l29/budapest-sunset-cocktail-cruise-t408167/",
    "dinner-drinks": "https://www.getyourguide.com/budapest-l29/budapest-premium-dinner-cruise-live-music-unlimited-drinks-t494832/",
    "unlimited-cocktails": "https://www.getyourguide.com/budapest-l29/budapest-sightseeing-river-cruise-with-unlimited-cocktails-t781483/",
    "party-boat": "https://www.getyourguide.com/budapest-l29/budapest-boat-party-on-the-river-danube-with-drinks-t333211/",
}
