# -*- coding: utf-8 -*-
"""Upgrade spec for best-food-tours-budapest.html (scripts/listicle_upgrade.py).

Facts from the page's own reviews and quick facts. Nothing tested.
"""

PAGE = {
    "noun": "tours",
    "filter_aria": "Filter food tours",
    "filters": [
        {"label": "Type", "chips": [("walk", "🚶 Walking food tour"), ("class", "👩‍🍳 Hands-on class")]},
        {"label": "Area &amp; time", "chips": [("market", "🏛️ Great Market Hall"), ("jewish", "🕍 Jewish Quarter"),
                                                ("evening", "🌙 Evening")]},
        {"label": "Price", "chips": [("u55", "💶 Under €55"), ("c55", "💳 €55 to €70"), ("c70", "💎 €70+")]},
    ],
}

NOTE = "Free cancellation up to 24 hours before. Prices change by date; the final price shows before you pay."
NEW = {"meta": "✨ New listing · no reviews yet"}


def B(pick, skip):
    return {"pick_html": pick, "skip_html": skip}


def price(rows):
    return {"sub": "per person", "rows": rows, "note": NOTE}


CARDS = {
    "card-1": {
        "best_for": B("for first-timers who want the classics in one go: Great Market Hall, goulash, lángos, chimney cake and a wine tasting.",
                      "if you would rather spend the evening in the Jewish Quarter's bars: that is the Carpe Diem tour."),
        "faq": [
            ("What do we taste?", "12+ tastings: cold cuts and pickles at the market, goulash, lángos, chimney cake and a Hungarian dessert."),
            ("Which drinks are included?", "Homemade pálinka and a wine tasting at the last stop. An alcohol-free substitute is available."),
            ("Where does it start?", "At the Central Market Hall (Fővám tér). There are 2 start options depending on your slot; the exact spot is in your voucher."),
            ("Is hotel pickup included?", "No, you meet at the start point."),
            ("Are tips included?", "No, tips for the guide are extra."),
        ],
        "price": price([{"label": "Adult", "small": "3 hours, 12+ tastings", "price": "€62"}]),
    },
    "card-2": {
        "best_for": B("for an evening-style walk through the Jewish Quarter's bar district with a proper sit-down plate, for the lowest price of the big tours.",
                      "if you eat gluten-free or vegan, or you want the Great Market Hall: this tour never goes there."),
        "faq": [
            ("Is it the same tour as Carpe Diem's famous listing?", "Same operator, start point and 4-stop format as its 1,690-review listing (€62), for €53."),
            ("What do we eat?", "Traditional soup and lángos, then chicken paprikash, and somlói trifle cake to finish."),
            ("Which drinks are included?", "Three: pálinka, a Dreher beer and sweet Tokaji wine. Alcohol-free on request."),
            ("Can I eat gluten-free or vegan?", "Not yet. Vegetarian is possible, with fewer choices."),
            ("Where does it start?", "Kazinczy utca 29-31 in District VII, by the Kazinczy Street Synagogue. Astoria (M2) or Deák Ferenc tér are a 5-minute walk."),
        ],
        "price": price([{"label": "Adult", "small": "this listing", "price": "€53"},
                        {"label": "Same tour", "small": "main listing", "price": "€62"}]),
    },
    "card-3": {
        "best_for": B("for big eaters who want the most separate tastings and a long 45-minute look around the Great Market Hall.",
                      "if you prefer a proven tour with hundreds of reviews: #1 covers the same ground with a longer record."),
        "faq": [
            ("How long in the market?", "About 45 minutes inside the Great Market Hall, the longest of any tour here."),
            ("What do we taste?", "20+ tastings: beef goulash, lángos, chimney cake, cold cuts, homemade pickles and local desserts."),
            ("Which drinks are included?", "Homemade pálinka and other local drinks."),
            ("Where does it end?", "At Ferenciek tere, a short walk from Váci utca and the river."),
            ("Are tips included?", "No, tips for the guide are extra."),
        ],
        "price": price([{"label": "Adult", "small": "3 hours, 20+ tastings", "price": "€62"}]),
    },
    "card-4": {
        "best_for": B("for your first evening in Budapest: a guided walk through the lit-up centre that ends with a sit-down goulash meal.",
                      "if your main goal is the Great Market Hall, which is closed by evening: book #1 or #3 instead."),
        "faq": [
            ("When does it run?", "In the evening, so it replaces dinner on your first night."),
            ("What do we eat?", "10+ tasters and a traditional tavern meal of goulash."),
            ("Which drinks are included?", "A welcome pálinka. An alcohol-free substitute is available."),
            ("What do I take home?", "A recipe and a list of restaurant recommendations for the rest of your trip."),
            ("Where do we meet?", "In central Pest; the exact spot is in your voucher. It is walkable from Deák Ferenc tér."),
        ],
        "price": price([{"label": "Adult", "small": "3 hours, evening", "price": "€61"}]),
    },
    "card-5": {
        "best_for": B("for couples and foodies who would rather cook paprikash than just eat it, with a market shop first.",
                      "if you only have a couple of hours: the class takes 3 to 4."),
        "faq": [
            ("What do we cook?", "A Hungarian main course and a dessert, with a local chef talking you through it."),
            ("Is there a market visit?", "Yes, it starts with a guided walk through the Central Market Hall, then moves to the Foodapest kitchen nearby."),
            ("Which drinks are included?", "A wine pairing with what you cooked and a Hungarian spirit tasting. Alcohol-free substitute available."),
            ("What do I take home?", "A recipe booklet and a vintage paprika gift."),
            ("How long is it?", "3 to 4 hours, so it uses most of a morning or afternoon."),
        ],
        "price": price([{"label": "Adult", "small": "class, market tour, wine", "price": "€90"}]),
    },
    "card-6": {
        "best_for": B("for families with kids, rainy afternoons and anyone who wants a food experience for €20 in about an hour.",
                      "if you want savoury Hungarian food or wine: it is one sweet, not a meal."),
        "faq": [
            ("What do we make?", "Your own kürtőskalács: you roll, wrap and bake the spiral chimney cake, then choose your toppings."),
            ("How long is it?", "65 minutes, easy to fit around a cruise or a museum."),
            ("What is included?", "All ingredients, an apron, toppings, coffee or tea and a certificate."),
            ("Is it good for kids?", "Yes, it is the most family-friendly food experience on this page."),
            ("Where is it?", "Ipar utca 11 in District IX: Boráros tér (trams 2, 4, 6) or Corvin-negyed (M3), then a short walk."),
        ],
        "price": price([{"label": "Per person", "small": "65 minutes", "price": "€20"}]),
    },
    "card-7": {
        "ratings": NEW,
        "best_for": B("for budget travellers who want a full meal on a guided walk and don't mind a new tour with no reviews yet.",
                      "if you want drinks included or a proven track record: #2 is €8 more with 3 drinks."),
        "faq": [
            ("Why is it so cheap?", "It is on sale for €45 instead of the listed €90."),
            ("Is it a full meal?", "Yes, it is sized as a full meal across 4+ stops in 3 hours."),
            ("Which drinks are included?", "Water and one alcoholic drink. Extra food and drinks cost extra."),
            ("How big is the group?", "It is a small-group tour."),
            ("Where do we meet?", "In central Pest; the exact spot is in your voucher."),
        ],
        "price": price([{"label": "Adult", "small": "sale price", "price": "€45"},
                        {"label": "Listed price", "price": "<s>€90</s>"}]),
    },
    "card-8": {
        "ratings": NEW,
        "best_for": B("for groups who want the guide to speak German, French, Italian or Spanish, not just English.",
                      "if everyone is fine in English: #1 and #3 do the market better and have hundreds of reviews."),
        "faq": [
            ("Which languages?", "English, German, French, Italian and Spanish, the only food tour here with all five."),
            ("What do we taste?", "Cheeses, cured meats, Hungarian sausages, pastries, lángos and chimney cake."),
            ("Are drinks included?", "The guide explains paprika, wine and pálinka, but drinks are not clearly listed as included."),
            ("Where do we meet?", "At the Central Market Hall, Fővám tér (M4 or trams 2, 47, 49)."),
            ("What else do I get?", "Personal food and restaurant tips for the rest of your stay."),
        ],
        "price": price([{"label": "Adult", "small": "2.5 hours", "price": "€60"}]),
    },
    "card-9": {
        "best_for": B("for return visitors who have seen the Great Market Hall and want the local Lehel Market plus a bit of live folk music.",
                      "if it's your first trip or you want to eat a lot: #1 is €23 cheaper with twice the tastings."),
        "faq": [
            ("Which markets do we visit?", "The Great Market Hall, then Lehel Market, where locals actually shop."),
            ("Is there music?", "Yes, a short folk music performance by your licensed guide, plus a visit to a historic café."),
            ("How much do we eat?", "5+1 traditional tastings: it is more about the story than a full stomach."),
            ("Is transport included?", "No. Bring a public transport ticket for the tram and metro ride between the halls."),
            ("Where does it end?", "At József nádor tér."),
        ],
        "price": price([{"label": "Adult", "small": "3 hours", "price": "€85"}]),
    },
}
