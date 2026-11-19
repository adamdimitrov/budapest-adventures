# -*- coding: utf-8 -*-
"""Upgrade spec for best-private-boat-tours-budapest.html (scripts/listicle_upgrade.py).

Facts from scripts/private_boats_data.py and scripts/private_boats_copy_en.py (listings read on
14 Nov 2026, booking calendar for Wed 18 and Sat 21 Nov 2026). No card is personally tested.
"""

PAGE = {
    "noun": "boats",
    "filter_aria": "Filter private boats",
    "filters": [
        {"label": "Group", "chips": [("small", "👫 Couples &amp; small groups"), ("groups20", "👥 Up to 20 or more")]},
        {"label": "Occasion", "chips": [("luxury", "💎 Luxury boat"), ("party", "🍻 Stag, hen &amp; parties"),
                                         ("evening", "🌙 Late-evening start")]},
        {"label": "Drinks &amp; budget", "chips": [("drinks", "🥂 Drinks included"), ("under300", "💶 Under €300 a boat")]},
    ],
}

NOTE = "Price for the whole boat. Checked on the booking calendar for Wed 18 and Sat 21 Nov 2026; prices change by date and season."

CARDS = {
    "card-1": {
        "cats": ["small", "groups20", "under300"],
        "faq": [
            ("Can two people book the whole boat?",
             "Yes. The price is per boat, not per person, so a couple pays the same <strong>€225</strong> as a group of 20. Guests regularly book it for two."),
            ("Are drinks included?",
             "No. The bar on board sells drinks and snacks at your own cost, and bringing your own food or drinks is not allowed."),
            ("Can we sail after dark?",
             "Only early in winter: in mid-November the latest start on the calendar was 16:00, so plan around sunset."),
            ("Is there a guide on board?",
             "No. It is a slow sightseeing loop between Margaret Bridge and Elisabeth Bridge with a sound system, but no commentary."),
            ("How do we get to Dock 42?",
             "Take tram 2, 4 or 6 to Jászai Mari tér, then walk about 500 metres north along the river to the Dock 42 sign. It is north of Margaret Bridge, further out than the central piers."),
        ],
        "price": {
            "rows": [
                {"label": "Whole boat", "small": "Wed 18 Nov", "price": "€225"},
                {"label": "Whole boat", "small": "Sat 21 Nov", "price": "€275"},
                {"label": "Per person", "small": "group of 20, weekday", "price": "about €11"},
            ],
            "note": NOTE,
        },
    },
    "card-2": {
        "cats": ["small", "luxury", "drinks"],
        "faq": [
            ("Is the water limousine guided?",
             "No. Only a driver is on board and nobody explains the sights. If you want commentary, bring your own audio guide or pick a guided cruise."),
            ("What drinks are included?",
             "One glass of Hungarian sparkling wine (or a soft drink) each. Wine, champagne and beer from the fridge cost extra; pre-order anything special."),
            ("Can we go fast?",
             "Yes. Ask the driver to speed up for the thrill, or glide slowly past Parliament and the castle. Guests cannot drive the boat."),
            ("How many people fit?",
             "Up to 10 guests. The cruise is 50 minutes on the water, mainly between Margaret Bridge and Petőfi Bridge."),
            ("What happens in bad weather?",
             "The trip depends on the weather: if it is cancelled for weather up to 3 hours before, you get a new date or a refund. Confirmation can take up to 48 hours."),
        ],
        "price": {
            "rows": [
                {"label": "Whole boat", "small": "up to 10 guests", "price": "€580"},
                {"label": "Per person", "small": "group of 10", "price": "€58"},
            ],
            "note": "Same price on Wed 18 and Sat 21 Nov 2026 on the booking calendar; prices change by season.",
        },
    },
    "card-3": {
        "cats": ["groups20", "party", "drinks"],
        "faq": [
            ("Are drinks really unlimited?",
             "Yes for <strong>beer, house wine and house sparkling wine</strong> during the hour, plus <strong>one shot</strong> each. Spirits and cocktails are sold at the bar."),
            ("Can under-18s come?",
             "No. It is adults only, and not suitable for pregnant women or wheelchair users."),
            ("What is on board?",
             "A bar, sound system, music, party lights, heating, Wi-Fi and 220 V sockets, on a modern Dutch boat refitted for private events."),
            ("Can we party at night?",
             "Not in mid-November: the calendar showed hourly starts from 08:00 to 16:00 on Wed 18 Nov and 08:00 to 15:00 on Sat 21 Nov."),
            ("Where does it leave from?",
             "Dock 42 in Szent István park, the same dock as the Portum private boat. Take tram 2, 4 or 6 to Jászai Mari tér and walk about 500 metres north."),
        ],
        "price": {
            "rows": [
                {"label": "Whole boat", "small": "Wed 18 Nov", "price": "€450"},
                {"label": "Whole boat", "small": "Sat 21 Nov", "price": "€550"},
                {"label": "Per person", "small": "group of 20, weekday", "price": "€22.50"},
            ],
            "note": "Drinks included. " + NOTE,
        },
    },
    "card-4": {
        "cats": ["small", "groups20", "party", "evening"],
        "ratings": {"meta": "✨ New listing · no reviews yet"},
        "faq": [
            ("Can we rent a boat late at night?",
             "Yes. Pick any start between <strong>08:00 and 23:00</strong>. The city lights switch off at 22:00 in winter and 23:00 in summer."),
            ("Which boat should we pick?",
             "The classic cruiser takes up to 35 guests from €495; the boutique boat takes up to 12 from €675 and includes a welcome drink."),
            ("Can we add dinner or a guide?",
             "Yes, as paid extras: dinner and wine tasting on the boutique boat, and on either boat a private guide in English, French, German, Italian or Spanish, unlimited drinks, cocktails or a photographer."),
            ("Where do we board?",
             "There are two departure points, depending on the boat. The exact address appears when you choose an option; message the provider if you want a specific pier."),
            ("Can they set up a proposal?",
             "Yes. The operator organises surprise proposals, birthday parties, stag and hen parties and family reunions on board."),
        ],
        "price": {
            "rows": [
                {"label": "Classic boat", "small": "up to 35, Wed 18 Nov", "price": "€495"},
                {"label": "Classic boat", "small": "up to 35, Sat 21 Nov", "price": "€540"},
                {"label": "Boutique boat", "small": "up to 12, Wed 18 Nov", "price": "€675"},
                {"label": "Boutique boat", "small": "up to 12, Sat 21 Nov", "price": "€765"},
            ],
            "note": "Boat hire only; dinner, drinks and guide are extras. Prices include the 10% discount shown on 14 Nov 2026.",
        },
    },
}
