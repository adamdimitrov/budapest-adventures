# -*- coding: utf-8 -*-
"""Upgrade spec for new-years-eve-cruises-budapest.html (scripts/listicle_upgrade.py).

Facts from the page's own reviews, menus and quick facts (checked 10-13 Nov 2026). Nothing tested.
"""

PAGE = {
    "noun": "cruises",
    "filter_aria": "Filter New Year's Eve cruises",
    "filters": [
        {"label": "Type", "chips": [("dinner", "🍽️ Dinner"), ("party", "🎉 Party &amp; DJ")]},
        {"label": "Budget", "chips": [("budget", "💶 Under €250")]},
    ],
}


def note(t):
    return f'<span class="bpa-lang-note">{t}</span>'


CHECKED = "Prices checked 10 Nov 2026; they can change."
NEW = {"meta": "✨ New listing · no reviews yet"}

CARDS = {
    "card-1": {
        "no_ratings": True,
        "pill_pops": {
            0: "<strong>Celebration Party:</strong> unlimited prosecco, wine and beer from 22:00 to 01:00. <strong>Booze cruises:</strong> unlimited wine, sparkling wine, draught beer and soft drinks."
               + note("The Gala Dinner lists only a welcome cocktail and the midnight sparkling wine."),
            1: "<strong>A DJ on the Celebration Party.</strong> The Gala Dinner has live piano instead.",
            2: "<strong>Party: tapas and finger food,</strong> no seated dinner. <strong>Gala:</strong> 5 seated courses you choose. <strong>Booze cruises:</strong> drinks only.",
        },
        "faq": [
            ("What is the cheapest way to be on the water at midnight?",
             "The Midnight Booze Cruise: 23:00, 90 minutes, €125, with unlimited wine, sparkling wine, beer and soft drinks."),
            ("Is there a seated dinner?",
             "Only on the Gala Dinner (€340): 5 courses you choose, live piano and a sparkling-wine toast in front of Parliament at midnight."),
            ("Does the 60-minute cruise see midnight?",
             "No. The Evening Booze Cruise sails at 18:30, 20:00 or 21:30 and is back before midnight."),
            ("When should I get to the pier?",
             "At least 30 minutes before boarding: embankments get crowded and partly closed on New Year's Eve."),
            ("How do I get home?",
             "Plan your way home after 01:00 in advance."),
        ],
        "price": {"sub": "per person",
                  "rows": [{"label": "Evening Booze Cruise", "small": "60 min", "price": "€70"},
                           {"label": "Midnight Booze Cruise", "small": "23:00, 90 min", "price": "€125"},
                           {"label": "Celebration Party", "small": "22:00–01:00", "price": "€239"},
                           {"label": "Gala Dinner", "small": "20:00–01:00", "price": "€340"}],
                  "note": CHECKED},
        "trust": ["<b>Book direct</b> on Silverline's own site", "<b>Instant confirmation</b>"],
    },
    "card-2": {
        "pill_pops": {
            0: "<strong>Table-served 5-course gala:</strong> Menu A (red meat), B (poultry) or C (vegetarian), then a midnight buffet with korhely soup and lentil stew."
               + note("You email your menu choice to the operator after booking."),
            1: "<strong>Unlimited beer, wine and prosecco</strong> plus welcome sparkling wine, rare for a seated gala.",
            2: "<strong>Live music and a folk dance show by the Rajkó Ensemble</strong> on the Gróf Széchenyi, plus a raffle and a party.",
        },
        "faq": [
            ("What time does it start?",
             "It is a 6-hour program on 31 December. Confirm the exact times before you plan the evening."),
            ("How do I choose my menu?",
             "Pick Menu A (red meat), B (poultry) or C (vegetarian) and email it to the operator after booking."),
            ("Are drinks included?",
             "Yes: welcome sparkling wine and unlimited beer, wine and prosecco."),
            ("Is there food at midnight?",
             "Yes, a midnight buffet with korhely soup with smoked turkey, frankfurters and lentil stew."),
            ("Where do we board?",
             "Akadémia 2 ponton on Id. Antall József rakpart."),
        ],
        "price": {"sub": "per person", "rows": [{"label": "Gala dinner, show and drinks", "small": "6 hours", "price": "€360"}],
                  "note": CHECKED},
    },
    "card-3": {
        "pill_pops": {
            0: "<strong>Cold and hot snack buffet</strong> with a vegan option, on the Food &amp; Drinks option only."
               + note("Not a dinner. Only Drinks has no food."),
            1: "<strong>Unlimited</strong> local beer, wine, mulled wine, champagne and soft drinks, plus a glass of champagne.",
        },
        "faq": [
            ("What are the two options?",
             "Food &amp; Drinks (22:00, 4 hours, snack buffet) for €230, or Only Drinks (23:00, 2 hours)."),
            ("Is it an elegant gala?",
             "No. Portum itself describes it as a simple, informal party."),
            ("Where does it leave from?",
             "Dock 42 in Szent István park, north of the centre, so plan your trip there and back."),
            ("Can I cancel?",
             "Free cancellation up to 48 hours before departure in the operator's webshop."),
            ("Is it accessible?",
             "No, it is not suitable for wheelchair users. Bring warm clothing."),
        ],
        "price": {"sub": "per person",
                  "rows": [{"label": "Food &amp; Drinks", "small": "22:00, 4 hours", "price": "€230"}],
                  "note": CHECKED},
    },
    "card-4": {
        "ratings": NEW,
        "pill_pops": {
            0: "<strong>Buffet dinner:</strong> Hungarian classics, seasonal salads, roast turkey, duck confit, vegetarian options and desserts."
               + note("Shared tables; expect queues at the start."),
            1: "<strong>All-inclusive bar:</strong> beer, wine, sparkling wine and soft drinks.",
            2: "<strong>An international retro party with a DJ</strong>, and lentil soup with sausages at midnight.",
        },
        "faq": [
            ("When does boarding start?",
             "From 21:00 on 31 December, for a 5-hour program."),
            ("Where does it leave from?",
             "Port #1 at Jászai Mari tér (Millennium boats), 150 m from Margaret Bridge."),
            ("Is it table service?",
             "No, it is a buffet, so expect queues at the start."),
            ("What is served at midnight?",
             "A special midnight menu: lentil soup with sausages."),
            ("Does it have reviews?",
             "Not yet: it is a new listing."),
        ],
        "price": {"sub": "per person", "rows": [{"label": "Buffet, drinks and party", "small": "5 hours", "price": "€315"}],
                  "note": CHECKED},
    },
    "card-5": {
        "pill_pops": {
            0: "<strong>Unlimited drinks</strong> for the whole 5-hour event." + note("Strictly 18+."),
            1: "<strong>A live DJ and a photographer.</strong> Easy to meet people if you travel solo.",
            2: "<strong>A midnight snack buffet</strong>, not a dinner: eat before you board.",
        },
        "faq": [
            ("How long is it on the water?",
             "It is a 5-hour event with a 3-hour cruise."),
            ("Is there an age limit?",
             "Yes, 18+ only."),
            ("Is dinner included?",
             "No, only a midnight snack buffet."),
            ("Where does it leave from?",
             "The Akadémia 2 pontoon near the Chain Bridge."),
            ("How is it rated?",
             "Mixed: 3.8/5 from 13 reviews."),
        ],
        "price": {"sub": "per person", "rows": [{"label": "Party, drinks and snacks", "small": "5 hours", "price": "€200"}],
                  "note": CHECKED},
    },
    "card-6": {
        "ratings": NEW,
        "pill_pops": {
            0: "<strong>Unlimited beer, wine, soft drinks and coffee</strong>, plus a welcome drink.",
            1: "<strong>A DJ</strong> for the 3-hour dockside party after the 2-hour cruise.",
            2: "<strong>A glass of champagne</strong> and the Hungarian tradition of lentils at midnight."
               + note("Snacks only, no proper dinner."),
        },
        "faq": [
            ("How long is it on the water?",
             "Only 2 of the 5 hours. Check whether midnight is on the boat or at the dock."),
            ("Where does it leave from?",
             "Dock 3/a on Jane Haining rakpart."),
            ("Is dinner included?",
             "No: snacks plus the traditional lentil dish at midnight."),
            ("Is there an age limit?",
             "Yes, adults only."),
            ("Does it have reviews?",
             "Not yet: it is a new listing."),
        ],
        "price": {"sub": "per person", "rows": [{"label": "Cruise and dockside party", "small": "5 hours", "price": "€164"}],
                  "note": CHECKED},
    },
    "card-7": {
        "no_ratings": True,
        "pill_pops": {
            0: "<strong>A 5-course served gala dinner</strong> plus the traditional Hungarian midnight dinner.",
            1: "<strong>Unlimited</strong> Hungarian wines, beer, prosecco and soft drinks." + note("Premium drinks cost extra."),
            2: "<strong>A salon music band, a folk dance show</strong>, a DJ after midnight and a raffle on the Gróf Széchenyi.",
        },
        "faq": [
            ("What does €830 include?",
             "Transfer to the dock, a 5-course gala dinner, the midnight dinner, unlimited drinks and the entertainment."),
            ("How much of it is cruising?",
             "2 hours of the 6-hour program (19:00 to 01:00)."),
            ("Is it the same boat as the Hungaria Koncert gala?",
             "Yes, the Gróf Széchenyi. Hungaria Koncert's own New Year's Eve gala on it costs €360."),
            ("Is there a dress code?",
             "Smart casual."),
            ("Where is the meeting point?",
             "Dock 42 in Szent István park."),
        ],
        "price": {"sub": "per person", "rows": [{"label": "All-inclusive package", "small": "6 hours", "price": "€830"}],
                  "note": CHECKED},
    },
}
