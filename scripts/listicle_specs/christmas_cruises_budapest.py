# -*- coding: utf-8 -*-
"""Upgrade spec for christmas-cruises-budapest.html (scripts/listicle_upgrade.py).

Facts from the page's own reviews, menus and quick facts (prices checked 10-13 Nov 2026). Nothing tested.
Silverline and Legenda book direct, so their review entries stay unlinked.
"""

PAGE = {
    "noun": "cruises",
    "filter_aria": "Filter Christmas cruises",
    "filters": [
        {"label": "Date", "chips": [("advent", "🎄 Before 24 Dec"), ("d24", "📅 24 Dec"), ("d25", "📅 25 Dec"),
                                     ("d26", "📅 26 Dec")]},
        {"label": "Type", "chips": [("dinner", "🍽️ Dinner"), ("nodinner", "🥂 No dinner"),
                                     ("drinks", "🍾 Unlimited drinks"), ("mulled", "🍷 Mulled wine")]},
        {"label": "Budget", "chips": [("u50", "💶 Under €50")]},
    ],
}


def note(t):
    return f'<span class="bpa-lang-note">{t}</span>'


CHECKED = "Prices checked 10-13 Nov 2026; they can change."

CARDS = {
    "card-1": {
        "pill_pops": {
            0: "<strong>You choose every course when you book:</strong> burrata panzanella or goose liver pâté, beef ragout or seasonal soup, then cod, salmon lasagne, pork, lamb or a vegan sweet potato main."
               + note("Vegan and gluten-free choices in every course."),
            1: "<strong>A pianist plays Christmas standards</strong> all evening on a new catamaran."
               + note("3 hours on the water, the longest Christmas dinner cruise in this list."),
            2: "<strong>A welcome glass of champagne</strong>, your own table and a small Christmas gift."
               + note("Other drinks are paid on board."),
        },
        "faq": [
            ("Can I book it for 24 December?",
             "The operator advertises 24 and 25 December, but only 25 December was offered in the booking form when I checked on 10 Nov 2026."),
            ("How much is a window table?",
             "€210 instead of €155, so €55 more per person. Children aged 4–12 get €20 off."),
            ("Are drinks included?",
             "Only the welcome champagne. Other drinks are paid on board."),
            ("What time does it board?",
             "Boarding at 19:00 at Dock 11 (Petőfi tér), sailing 19:30–22:30."),
            ("Can I eat vegan or gluten-free?",
             "Yes. Every course has a vegan and a gluten-free choice, picked when you book."),
        ],
        "price": {"sub": "per person, 25 Dec",
                  "rows": [{"label": "Christmas Day dinner", "price": "€155"},
                           {"label": "Window table", "price": "€210"},
                           {"label": "Child 4–12", "price": "€20 off"}],
                  "note": CHECKED},
        "trust": ["<b>Book direct</b> on Silverline's own site", "<b>Window seat</b> +€55"],
    },
    "card-2": {
        "pill_pops": {
            0: "<strong>A four-course festive Hungarian dinner</strong> with four main choices: roast duck, veal, chicken or vegetarian."
               + note("The full menu isn't published. Seating is first come, first served."),
            1: "<strong>Live folk music</strong> and a folk dance show in traditional costumes."
               + note("Pick it over Silverline if you want folk music instead of a piano."),
            2: "<strong>One welcome glass</strong> of sparkling wine." + note("Other drinks are extra."),
        },
        "faq": [
            ("Which dates does it sail?",
             "24 and 25 December were the only bookable dates when I checked on 10 Nov 2026."),
            ("What is on the menu?",
             "A four-course festive Hungarian dinner with roast duck, veal, chicken or a vegetarian main. The full menu isn't published."),
            ("Is it a proven cruise?",
             "It ran for the first time last Christmas. Its only two reviews, both 5/5, are from 25 and 26 December 2025."),
            ("Where do we board?",
             "Vigadó tér 6. Arrive 30 minutes early."),
            ("Can I cancel?",
             "Yes, for free up to 24 hours before."),
        ],
        "price": {"sub": "per person", "rows": [{"label": "Dinner, show and welcome drink", "small": "2 hours", "price": "€130"}],
                  "note": CHECKED},
    },
    "card-3": {
        "pill_pops": {
            0: "<strong>Unlimited mulled wine, prosecco and Aperol Spritz</strong>, including a hot Aperol Spritz, for the 75 minutes."
               + note("Unlimited alcohol is 18+ only."),
            1: "<strong>A market-style stall on board</strong> sells souvenirs, and the boat is decked out with garlands and lights."
               + note("Chimney cake (kürtőskalács) costs extra."),
            2: "<strong>A huge rooftop terrace</strong> for Parliament views." + note("QR audio guide included."),
        },
        "faq": [
            ("When does it sail?",
             "Through Advent plus 25 and 26 December, but not on 24 December. The listing photos show departures at 18:00, 19:30 and 21:00."),
            ("Is food included?",
             "No. Chimney cake is an optional extra."),
            ("Where does it leave from?",
             "Dock 9 at Petőfi tér, near Elisabeth Bridge."),
            ("Is it good before dinner?",
             "Yes. At 75 minutes it works best as a pre-dinner warm-up during Advent."),
            ("Does it have reviews?",
             "Not yet: it is new this season."),
        ],
        "price": {"sub": "per person", "rows": [{"label": "Adult", "small": "75 minutes, drinks included", "price": "€33"}],
                  "note": CHECKED},
    },
    "card-8": {
        "pill_pops": {
            0: "<strong>Unlimited Törley Prosecco</strong>, topped up at your table by crew walking round with bottles."
               + note("A few guests found the Prosecco average."),
            1: "<strong>Unlimited mulled wine</strong>, plus a self-service point with homemade lemonade."
               + note("No food: snacks are paid on board."),
            2: "<strong>Audio guide included</strong> on the 1-hour evening loop from Batthyány tér, opposite Parliament."
               + note("Alcohol is served 18+ only."),
        },
        "faq": [
            ("Does it sail at Christmas?",
             "Yes: on 25 December at 17:00, 18:30 and 20:30, and on 26 December. 24 December is closed."),
            ("How much is it?",
             "€33 in December. It drops to €20 on some November dates."),
            ("Where does it leave from?",
             "MAHART's Batthyány tér Dock 1 on the Buda side, opposite Parliament."),
            ("Is food included?",
             "No. Snacks are for sale on board."),
            ("When does it run in Advent?",
             "Wednesday to Sunday until 20 December, then daily from 21 December."),
        ],
        "price": {"sub": "per person in December",
                  "rows": [{"label": "December", "price": "€33"}, {"label": "Some November dates", "price": "€20"}],
                  "note": CHECKED},
    },
    "card-7": {
        "pill_pops": {
            0: "<strong>Five mulled wines</strong> (classic, rosé with raspberry, apple-cinnamon and more), refilled all cruise."
               + note("Reviewers say refills slow down on full sailings."),
            1: "<strong>Two non-alcoholic hot drinks</strong> are included too." + note("Alcohol is served 18+ only."),
            2: "<strong>Audio guide app</strong> for the 1-hour sightseeing loop, in a heated cabin with big windows.",
        },
        "faq": [
            ("Does it sail on Christmas Day?",
             "No. It runs through Advent and on 27–31 December, but not on 24, 25 or 26 December."),
            ("What is poured?",
             "Five mulled wines plus two non-alcoholic hot drinks, refilled for the whole hour."),
            ("Is food included?",
             "No, it is drinks only."),
            ("Is it warm on board?",
             "Yes: a heated cabin with big windows."),
            ("Where does it leave from?",
             "Dock 11 on Jane Haining rakpart (Petőfi tér)."),
        ],
        "price": {"sub": "per person", "rows": [{"label": "Adult", "small": "1 hour, unlimited mulled wine", "price": "€21"}],
                  "note": CHECKED},
    },
    "card-4": {
        "pill_pops": {
            0: "<strong>Soft open bar:</strong> house wine, tap beer, soft drinks, coffee and tea." + note("No spirits."),
            1: "<strong>One charcuterie board per two guests</strong> (no pork: cheeses, cold cuts, dips, fruit and nuts) and a Christmas cake buffet."
               + note("Not a dinner: eat before or after. Vegetarian board and gluten-free bread on advance request."),
            2: "<strong>Salon music by members of the Rajkó Orchestra</strong> and a folk dance show on the heritage paddle boat Gróf Széchenyi.",
        },
        "faq": [
            ("Does it sail on Christmas Eve?",
             "Yes, on 24 and 25 December at 19:00 or 21:30, one of the very few boats sailing that night."),
            ("Is dinner included?",
             "No. You get a tasting board per two guests and a Christmas cake buffet, so eat dinner before or after."),
            ("Which option do I book?",
             "The \"Holiday Tasting Menu\" option of Hungaria Koncert's folk dinner cruise, then 24 or 25 December."),
            ("Where do we board?",
             "Akadémia Dock 2 on Id. Antall József rakpart. Meet at the boat 30 minutes before."),
            ("How long is it?",
             "90 minutes, with shared seating on a first come, first served basis."),
        ],
        "price": {"sub": "per person, open bar included",
                  "rows": [{"label": "Early cruise", "small": "19:00–20:30", "price": "€76"},
                           {"label": "Late cruise", "small": "21:30–23:00", "price": "€76"}],
                  "note": CHECKED},
    },
    "card-5": {
        "pill_pops": {
            0: "<strong>Social dining at show-kitchen stations:</strong> go back as often as you like."
               + note("Shared, flowing dining rather than a seated, served dinner."),
            1: "<strong>Unlimited</strong> cocktails, Hungarian wines, prosecco, beer and mocktails.",
            2: "<strong>Live music</strong> on River Diva, Budapest's newest dinner boat.",
        },
        "faq": [
            ("Does it sail on 24 or 25 December?",
             "No. It sails on 26 December, and the Christmas menu in our menu box runs 26–30 December."),
            ("What is on the Christmas menu?",
             "Tokaji duck liver pâté, smoked Mangalica ham, Baja fisherman's soup, confit duck leg, chestnut-stuffed turkey roulade, wild boar stew and walnut and poppy-seed bejgli."),
            ("Are drinks included?",
             "Yes, unlimited: cocktails, Hungarian wines, prosecco and beer."),
            ("Is it a seated dinner?",
             "No. It is a shared, flowing buffet at show-kitchen stations."),
            ("Where does it leave from?",
             "From the Akadémia 3 pier."),
        ],
        "price": {"sub": "per person, drinks included",
                  "rows": [{"label": "Adult", "small": "from", "price": "€99"}],
                  "note": "Check the price for your date in the booking calendar. " + CHECKED},
    },
    "card-6": {
        "unlink_ratings": True,
        "pill_pops": {
            0: "<strong>17 dishes to choose from:</strong> 6 starters, 2 soups, 6 mains and 3 desserts, chosen on board."
               + note("Legenda's regular dinner menu, not a special Christmas one; the boat is decorated."),
            1: "<strong>Live lounge music</strong> for the 2.5-hour cruise, at your own candlelit table.",
            2: "<strong>A welcome drink</strong> is included." + note("Other drinks are extra."),
        },
        "faq": [
            ("Is there a dinner cruise on 24 December?",
             "No. On Christmas Eve Legenda only runs daytime sightseeing cruises (11:00, 12:30, 14:00 and 15:30)."),
            ("Is it a Christmas menu?",
             "No, it is Legenda's regular 4-course à la carte menu, but the boat is decorated and the price stays at €110."),
            ("What do children pay?",
             "The Kids' Dinner Package for ages 3–12 is €84."),
            ("When and where does it leave?",
             "At 19:00 on 25 and 26 December, from Dock 7 at Vigadó tér."),
            ("How does it compare with Silverline?",
             "It is €45 cheaper with a bigger choice of dishes, but 2.5 hours on the water instead of 3."),
        ],
        "price": {"sub": "per adult",
                  "rows": [{"label": "Adult", "price": "€110"}, {"label": "Child 3–12", "small": "kids' dinner package", "price": "€84"}],
                  "note": CHECKED},
        "trust": ["<b>Book direct</b> with Legenda", "<b>Free cancellation</b> up to 72 h before, full refund"],
    },
    "card-9": {
        "pill_pops": {
            0: "<strong>A kürtőskalács</strong> with brown sugar, cinnamon and a cream cheese and mascarpone frosting."
               + note("Contains gluten and dairy; there is no alternative."),
            1: "<strong>One mug of spiced pomegranate winter punch.</strong>" + note("One drink only, no refills."),
            2: "<strong>Eight sailings a day</strong> from 11:00 to 21:00, past Parliament, Buda Castle and the lit bridges.",
        },
        "faq": [
            ("Does it sail over Christmas?",
             "No. It is an Advent cruise: the calendar runs daily until 23 December."),
            ("What is included?",
             "One spiced pomegranate winter punch and one Cinnabon chimney cake."),
            ("Where does it leave from?",
             "Dock 11 on Jane Haining rakpart, a short walk from the Vörösmarty tér Christmas market."),
            ("Is there a gluten-free option?",
             "No. The cake contains gluten and dairy, and there is no alternative."),
            ("Does it have reviews?",
             "Not yet: it is new this season."),
        ],
        "price": {"sub": "per person", "rows": [{"label": "Adult", "small": "1 hour, drink and chimney cake", "price": "€19"}],
                  "note": CHECKED},
        "trust": ["<b>Book direct</b> on Silverline's own site", "<b>Runs until</b> 23 December"],
    },
}
