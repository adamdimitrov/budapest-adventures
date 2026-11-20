# -*- coding: utf-8 -*-
"""Upgrade spec for best-hop-on-hop-off-bus-budapest.html (scripts/listicle_upgrade.py).

Facts from the page's own reviews and quick facts. Nothing tested. Cards 1 and 2 book through Tiqets,
so their review entries stay unlinked.
"""

PAGE = {
    "noun": "bus tours",
    "filter_aria": "Filter bus tours",
    "filters": [
        {"label": "Type", "chips": [("hoho", "🚌 Hop-on hop-off"), ("guided", "🎙️ Live guide"), ("fun", "🎉 Fun rides")]},
        {"label": "Good for", "chips": [("boat", "⛴️ Boat ride included"), ("castle", "🏰 Castle Hill"),
                                         ("kids", "👨‍👩‍👧 Kids"), ("party", "🍺 Party")]},
        {"label": "Price", "chips": [("u40", "💶 Under €40")]},
    ],
}


def price(sub, rows, note):
    return {"sub": sub, "rows": rows, "note": note}


CARDS = {
    "card-1": {
        "unlink_ratings": True, "drop_rating_note": True,
        "faq": [
            ("Is City Sightseeing better than Big Bus?", "For most visitors, by a small margin: the same adult prices, but the boat ride is included, cancellation is free up to 2 days before and the child price runs to age 18."),
            ("What does the ticket include?", "The bus on a 20-stop red route, a Danube boat ride, a 1-hour guided walking tour and a coupon booklet for attractions."),
            ("How long is a full loop?", "About 110 minutes. Start at stop 1 at peak times: one guest waited over an hour at a busy stop."),
            ("When is the walking tour?", "Once a day in English, at 11:00, so plan your first morning around it."),
            ("Do kids pay?", "Children up to 18 pay the child price, and under-6s ride free."),
        ],
        "price": price("per adult · 24 hours",
                       [{"label": "24 hours", "price": "€39"}, {"label": "48 hours", "price": "€44"},
                        {"label": "72 hours", "price": "€49"}, {"label": "Under 6", "price": "Free"}],
                       "48 hours costs €5 more than 24 hours, 72 hours another €5. Free cancellation up to 2 days before."),
    },
    "card-2": {
        "unlink_ratings": True, "drop_rating_note": True,
        "faq": [
            ("Is the Big Bus worth it?", "Yes for a 2 or 3 day ticket, when the cruise, the walk and the extra days bring it to about €16 to €22 a day. For one afternoon, public transport is better value."),
            ("How often do buses run?", "From 10:00 to 17:00, every 10 to 25 minutes on the official timetable."),
            ("What is included?", "21 stops, one Danube river cruise and a guided walking tour of Pest with every ticket length."),
            ("Can I cancel?", "Not this ticket. The flexible Big Bus ticket can be cancelled up to 24 hours before at the same price, with 30% off a cruise instead of a free one."),
            ("Is it accessible?", "Yes, the buses are wheelchair accessible, air-conditioned in summer and heated in winter."),
        ],
        "price": price("per adult · 1 day",
                       [{"label": "1 day", "price": "€39"}, {"label": "2 days", "small": "Essential", "price": "€44"}],
                       "Non-refundable ticket."),
    },
    "card-3": {
        "faq": [
            ("50 or 90 minutes?", "The 90-minute tour (€32): only the longer route sails to the Parliament, the best view on the river."),
            ("What happens on the tour?", "A drive past Andrássy Avenue, the Opera and Heroes' Square, then the bus rolls down a ramp and splashes into the Danube."),
            ("Is there a guide?", "Yes: live guiding in English and German, plus audio in 12 languages."),
            ("How often does it run in winter?", "Only 3 tours a day from November to March, so book ahead."),
            ("Is there a toilet on board?", "No, and it is not wheelchair accessible. Food and drinks are not allowed on board."),
        ],
        "price": price("per adult · 50 minutes",
                       [{"label": "50 minutes", "price": "€27"}, {"label": "90 minutes", "small": "sails to the Parliament", "price": "€32"}],
                       "Starts at Széchenyi István tér 7, Pest end of the Chain Bridge."),
    },
    "card-4": {
        "faq": [
            ("Is it worth €18?", "Yes if walking up Castle Hill is hard for you or it is very hot. If stairs are fine, walk or take bus 16."),
            ("How often does it run?", "Open-air electric buses about every 20 minutes from Clark Ádám tér."),
            ("Where does it stop?", "5 stops near Fisherman's Bastion, Matthias Church, the Royal Palace and the Hospital in the Rock."),
            ("How long is the ticket valid?", "One round with up to 3 boardings; it expires when you are back at Clark Ádám tér."),
            ("Is there commentary?", "No. The driver speaks English, but it is transport, not a guided tour."),
        ],
        "price": price("per adult · one round", [{"label": "Adult", "small": "up to 3 boardings", "price": "€18"}],
                       "Free cancellation up to 24 hours before."),
    },
    "card-5": {
        "faq": [
            ("Hop-on bus or this guided tour?", "This one if you have a morning and want context from a person. A 24-hour hop-on ticket is €4 more but gives you all day and a boat ride, with recorded commentary."),
            ("What does it cover?", "A Castle District walk, Elizabeth Bridge, the Central Market Hall, City Park, Heroes' Square, Andrássy Avenue and the Basilica."),
            ("Can I get off along the way?", "No, it runs on a fixed schedule."),
            ("Which language?", "A live guide; some departures are guided in two languages, which slows the commentary."),
            ("Where does it start?", "At the Cityrama office, Báthory utca 19 (M2 to Kossuth Lajos tér or M3 to Arany János utca)."),
        ],
        "price": price("per adult · 3 hours", [{"label": "Adult", "price": "€35"}], "Free cancellation up to 24 hours before."),
    },
    "card-6": {
        "faq": [
            ("BeerBus or E-BeerBus?", "BeerBus for couples, solo travellers and small groups (5 departures a day); E-BeerBus for groups of 4+ who want their own music or a private bus."),
            ("Is the beer really unlimited?", "Yes, Hungarian draught beer for the whole hour. Prosecco is €13 a bottle, ordered a day ahead."),
            ("Can I join on my own?", "Yes. Departures run regardless of numbers, and solo guests say they felt included."),
            ("What do we see?", "Drive-bys of Andrássy Avenue, the Opera, Heroes' Square, the Chain Bridge, Gellért Hill and the Parliament."),
            ("Where does it start and end?", "Starts at Bajcsy-Zsilinszky út 16 near the Basilica, ends at Nyugati tér."),
        ],
        "price": price("per person · 1 hour", [{"label": "Per person", "price": "€27"}, {"label": "Prosecco", "small": "per bottle, order ahead", "price": "€13"}],
                       "Free cancellation up to 24 hours before."),
    },
    "card-7": {
        "faq": [
            ("Is it good for a stag party?", "Yes, it is built for it. Split the private 60-minute bus (€360) between 12 friends and it is €30 each, with your own music."),
            ("How many people do we need?", "Shared tours only run with at least 4 participants."),
            ("Can bigger groups stay together?", "Yes: two buses (14 and 16 seats) can drive together, for up to about 30 people."),
            ("Is there a toilet break?", "Yes, a planned stop."),
            ("Are there rules?", "No costumes, no nudity, and the tour can end early without a refund after repeated warnings."),
        ],
        "price": price("per person · min. 4 people",
                       [{"label": "Shared tour", "small": "per person", "price": "€27"},
                        {"label": "Private bus", "small": "1 hour, whole group", "price": "€360"}],
                       "Starts at Heroes' Square, next to the Műcsarnok. Free cancellation up to 24 hours before."),
    },
}
