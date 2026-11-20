# -*- coding: utf-8 -*-
"""Upgrade spec for best-pub-crawls-budapest.html (scripts/listicle_upgrade.py).

Facts from the page's own reviews and quick facts (prices for Fri 20 Nov 2026). Nothing tested.
"""

PAGE = {
    "noun": "pub crawls",
    "filter_aria": "Filter pub crawls",
    "filters": [
        {"label": "Style", "chips": [("party", "🎉 Bars + club"), ("drinks", "🍸 Drinks included"), ("private", "🔒 Private group")]},
        {"label": "Start &amp; price", "chips": [("early", "🕗 By 20:00"), ("late", "🌙 22:00 or later"),
                                                  ("u10", "💶 Under €10"), ("p10", "💳 €10+")]},
    ],
}

NOTE = "Free cancellation up to 24 hours before. Prices change by night; the final price shows before you pay."
NEW = {"meta": "✨ New tour for 2026 · no reviews yet"}


def B(pick, skip):
    return {"pick_html": pick, "skip_html": skip}


def price(rows):
    return {"sub": "per person", "rows": rows, "note": NOTE}


CARDS = {
    "card-1": {
        "best_for": B("for solo travellers and first-timers who want the biggest, busiest crawl in town: a shot at every stop and no queue at the club.",
                      "if you want quiet ruin bar courtyards and a proper drink: the cocktail crawl is the opposite night."),
        "faq": [
            ("What time does it start?", "At 21:10, 21:40 or 22:20 from Erzsébet körút 36. The 21:10 start ends around 02:10, inside a club you can stay in."),
            ("Which drinks are included?", "A welcome shot at every venue. Every beer and cocktail is on you."),
            ("Where do we skip the queue?", "VIP fast-track entry at Instant-Fogas, Füge Udvar, La Siesta and Humbák."),
            ("Is it always €2?", "No: it was €8.50 on Friday 20 November 2026. Check your date."),
            ("How do I get there?", "Tram 4 or 6 to Wesselényi utca / Erzsébet körút, or M2 to Blaha Lujza tér."),
        ],
        "price": price([{"label": "Most nights", "small": "from", "price": "€2"},
                        {"label": "Friday 20 Nov", "price": "€8.50"}]),
    },
    "card-2": {
        "best_for": B("for anyone who wants the best-reviewed big crawl: a welcome shot, 3-4 bars, then VIP club entry with free shots, for about €2.",
                      "if you want as many venues as possible in one night: Party Deck does 5 to 6."),
        "faq": [
            ("How is it rated?", "5.0 from 1,657 reviews, the top rating of any big Budapest crawl."),
            ("What time does it start?", "At 21:00, 21:30 or 22:00. From 21:00 you are officially done around 02:30."),
            ("Which bars?", "3 to 4 from a pool including Humbák Borkápolna, Stifler Ház, Doboz, La Siesta and Lámpás, ending at Instant."),
            ("Which drinks are included?", "A welcome shot, and free shots with VIP entry at the club. Other drinks and food are extra."),
            ("Is there an age limit?", "18+; bring ID (a copy is accepted)."),
        ],
        "price": price([{"label": "Friday 20 Nov", "small": "21:00 or 22:00", "price": "€2.18"},
                        {"label": "Friday 20 Nov", "small": "21:30", "price": "€4"}]),
    },
    "card-3": {
        "best_for": B("for late arrivals and people who want the longest night: join at 22:00 after dinner, or do the 6-hour version from 21:00.",
                      "if you want someone physically walking you between bars all night: #1 and #2 feel more hand-held."),
        "faq": [
            ("What time does it start?", "The 5-hour option starts at 22:00 and the 6-hour option at 21:00. Either way you finish around 03:00."),
            ("Which shots are included?", "Proper ones: tequila, vodka and pálinka. A 1-hour open bar (long drinks, wine and beer) is a paid extra."),
            ("How many bars?", "5 to 6 from a pool of more than ten, with VIP entry at Instant-Fogas."),
            ("Does a host walk us between bars?", "No. Local rules stop that, so you follow the route in a WhatsApp group with bar names, timings and maps. The hosts party with you inside."),
            ("Is it in Spanish too?", "Yes, there are English and Spanish-speaking guides."),
        ],
        "price": price([{"label": "5 hours", "small": "22:00, Fri 20 Nov", "price": "€2"},
                        {"label": "6 hours", "small": "21:00", "price": "€6"}]),
    },
    "card-4": {
        "best_for": B("for people who'd rather meet in a real pub than on a street corner, and groups of up to 12 who want the same night to themselves.",
                      "if price decides: #1 gives you more venues for €2 on most nights."),
        "faq": [
            ("Where do we meet?", "At Becketts Irish Bar, Liszt Ferenc tér 11, at 21:30. On New Year's Eve it starts at Klauzál utca 10."),
            ("What is included?", "Free shots, drinking games, entrance fees and fast-track entry at Instant-Fogas."),
            ("Is food included?", "No. The food stop is pay-as-you-go."),
            ("Can we go private?", "Yes: €100 for a group of up to 12 on Friday 20 November 2026 (3 hours, shots, entrance fees, 4 bars and clubs)."),
            ("Is there an age limit?", "The operator says it is not for over-70s."),
        ],
        "price": price([{"label": "Adult", "small": "5 hours", "price": "€19"},
                        {"label": "Private group", "small": "up to 12, Fri 20 Nov", "price": "€100"}]),
    },
    "card-5": {
        "ratings": NEW,
        "best_for": B("for couples and anyone past the shots-and-club stage: five real drinks, hidden bars and city stories, done by 23:00.",
                      "if the club is the point: there isn't one. Book #1 or #3 instead."),
        "faq": [
            ("Which drinks are included?", "Five: a welcome pálinka, a cocktail made for the tour, a fröccs (wine spritzer) or a beer, and two more shots."),
            ("What time does it run?", "From 20:00 for 3 hours, so you are free by about 23:00."),
            ("Where does it start and end?", "Starts at Szervita tér 8 (Deák Ferenc tér is 3 minutes away), ends at a ruin bar on Klauzál utca 25."),
            ("Is there a club?", "No. It is hidden pubs and underground bars with history stories between stops."),
            ("Who can't join?", "Per the operator, it is not for over-65s or wheelchair users."),
        ],
        "price": price([{"label": "Adult", "small": "5 drinks included", "price": "€25"},
                        {"label": "Friday 20 Nov", "price": "€24.67"}]),
    },
    "card-6": {
        "ratings": NEW,
        "best_for": B("for stag and hen groups of 8 or more: your own guide, pickup, 4 rounds of shots, then a nightclub or a strip club.",
                      "if you're fewer than 8: the #4 private option was €100 for a whole group of up to 12."),
        "faq": [
            ("How many people do we need?", "At least 8. It is priced per person."),
            ("What is included?", "Pickup, a local guide, 4 rounds of party shots across 3 to 4 pubs and bars, and entry to a nightclub or a strip club."),
            ("What time does it start?", "You set it when you book; the pickup area is confirmed then too."),
            ("Are there house rules?", "Yes: drinking on the street, public urination and noise can mean fines of up to €400, and your group pays any fine it causes."),
            ("Is there an age limit?", "18+; bring ID (a copy is accepted)."),
        ],
        "price": price([{"label": "Per person", "small": "min. 8 people", "price": "€27"}]),
    },
}
