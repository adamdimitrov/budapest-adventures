# -*- coding: utf-8 -*-
"""Upgrade spec for best-walking-tours-budapest.html (scripts/listicle_upgrade.py).

Facts from the page's own reviews and quick facts. Cards 1-6 keep the tested stamp: their reviews on
this page are written from the author's own tour ("This review is based on my personal experience").
"""

PAGE = {
    "noun": "tours",
    "filter_aria": "Filter walking tours",
    "filters": [
        {"label": "Price", "chips": [("free", "🆓 Free (tips)"), ("u15", "💶 Under €15"), ("c20", "💳 €20+")]},
        {"label": "Area", "chips": [("castle", "🏰 Buda Castle"), ("pest", "🏛️ Pest side"), ("both", "🌉 Both sides")]},
        {"label": "Length", "chips": [("short", "⏱️ 2 hours or less"), ("long", "🚶 Over 2 hours")]},
    ],
}


def note(t):
    return f'<span class="bpa-lang-note">{t}</span>'


def P(emoji, label, pop, time=False):
    return {"cls": "bpa-lang bpa-time" if time else "bpa-lang", "emoji": emoji, "label": label, "pop_html": pop}


def tested(what, anchor):
    return {"chip": "✓ Personally Tested",
            "pop_html": f"<strong>I took this tour myself.</strong> {what}"
                        f'<span class="bpa-lang-note"><a href="#{anchor}">Full review ↓</a></span>'}


FREE_NOTE = "Free cancellation up to 24 hours before."


def price(main_rows, note_text=FREE_NOTE):
    return {"sub": "per person", "rows": main_rows, "note": note_text}


CARDS = {
    "card-1": {
        "tested": tested("The 20:00 English tour, led by Joe.", "item-1-vampire-walking-tour"),
        "pills": [
            P("🧛", "Vampire Folklore", "<strong>Eastern European myths about vampires, ghosts and the undead</strong>, told as an immersive storytelling show."
              + note("More dark folklore than historical facts.")),
            P("🕗", "2 Hours at Night", "<strong>Starts at 19:45 or 20:00</strong> at Clark Ádám tér, next to the Kilometer Zero stone." + note("Ages 10+."), True),
            P("🏮", "Lantern Walk", "<strong>Through the Castle District after dark</strong>, starting with a 5–10 minute climb up the stairs."
              + note("A funicular option costs €10 extra for anyone with mobility issues.")),
            P("🏰", "Buda Castle", "<strong>The Castle District at night</strong> is the stage for the stories." + note("Groups of about 20 to 25 when I went.")),
        ],
        "best_for": {"pick_html": "for an evening with a story: Castle District legends by lantern light, starting 19:45 or 20:00 (ages 10+).",
                     "skip_html": "if you want historical facts: after five or six of the ten tales the storytelling can feel repetitive."},
        "faq": [
            ("What time does it start?", "At 19:45 or 20:00, from Clark Ádám tér next to the Kilometer Zero stone, near the funicular entrance."),
            ("Can children come?", "Yes, from age 10."),
            ("Is there a lot of climbing?", "A 5–10 minute climb up the stairs to Castle Hill. A funicular option costs €10 extra."),
            ("How big is the group?", "About 20 to 25 people on my tour."),
            ("Is it a history tour?", "Not really. It is about the dark folklore of Budapest and Eastern Europe rather than historical facts."),
        ],
        "price": price([{"label": "Adult", "small": "2 hours", "price": "€18"}]),
    },
    "card-2": {
        "tested": tested("A 1.5-hour English cave tour.", "item-2-buda-cave-tour"),
        "pills": [
            P("🕳️", "Underground Cave", "<strong>A 3 km stretch of the caves under Castle Hill</strong>, reopened to the public in 2019."
              + note("Geology plus 800 years of human use: storage, prisons, war refuges and even 90s parties.")),
            P("⏱️", "1.5 Hours Tour", "<strong>1.5 hours with a guide.</strong> Meet at Szentháromság tér, then a 5-minute walk to the entrance." + note("Ages 3+."), True),
            P("⛑️", "Helmets &amp; Lamps", "<strong>Kitted out for the maze-like passages</strong>; free ponchos if you come in summer clothes."
              + note("Not accessible for people with mobility impairments.")),
            P("🪨", "Natural Cave", "<strong>10–12 °C inside all year.</strong> Wear warm clothes and shoes you don't mind getting dirty."
              + note("Look out for the spot where a mammoth left one of its teeth.")),
        ],
        "best_for": {"pick_html": "for rainy days and families (ages 3+): 1.5 hours in the natural caves under Castle Hill.",
                     "skip_html": "if anyone in your group has limited mobility: the cave is not accessible."},
        "faq": [
            ("How cold is it inside?", "10–12 °C all year. Wear warm clothes; free ponchos are handed out if you come in summer clothes."),
            ("What will I see?", "3 km of natural cave, the geology of how it formed, the spot where a mammoth left a tooth, and 800 years of human history."),
            ("Where do we meet?", "At Szentháromság tér, by the Trinity statue opposite Matthias Church. The entrance is a 5-minute walk."),
            ("Is it accessible?", "No, the cave is not accessible for people with mobility impairments."),
            ("Can young children come?", "Yes, from age 3."),
        ],
        "price": price([{"label": "Adult", "small": "1.5 hours", "price": "€17"}]),
    },
    "card-3": {
        "tested": tested("A 2.5-hour English walking tour.", "item-3-ww2-jewish-quarter-tour"),
        "pills": [
            P("🕍", "Jewish Heritage", "<strong>Jewish life in Hungary from medieval times to WWII</strong>, with synagogues and memorials to those who resisted the Nazi and Arrow Cross regimes."),
            P("⏱️", "2.5 Hours Walk", "<strong>2.5 hours</strong> from Madách Imre tér to the Dohány Street Synagogue." + note("Look for the yellow umbrella next to the Sissi statue."), True),
            P("👁️", "Synagogue View", "<strong>Ends at the Dohány Street Synagogue.</strong> The whole walk is outdoors."),
            P("💶", "Free / Tips", "<strong>Free to book; you tip the guide</strong> at the end." + note("Groups of 20 to 30.")),
        ],
        "best_for": {"pick_html": "for history lovers who want the full WWII story, free and on flat streets.",
                     "skip_html": "with young kids: the material is heavy and delivered at academic level."},
        "faq": [
            ("Is it really free?", "Yes. It is tip-based: you pay the guide what you think the tour was worth."),
            ("Where do we meet?", "Madách Imre út 2, by the yellow umbrella next to the Sissi statue. Any metro line or trams 47/49 to Deák Ferenc tér get you there."),
            ("Is it wheelchair accessible?", "Yes. The whole tour is outdoors and wheelchair-accessible."),
            ("How detailed is it?", "Very: academic-level commentary that needs good English (a Spanish tour runs too)."),
            ("Where does it end?", "At the Dohány Street Synagogue."),
        ],
        "price": price([{"label": "Tour", "price": "Free (tips)"}], "Tip-based; book a spot in advance. " + FREE_NOTE),
    },
    "card-4": {
        "tested": tested("A 2.25-hour English walking tour.", "item-4-pest-walking-tour"),
        "pills": [
            P("🏛️", "Inner City Tour", "<strong>Budapest's history in Pest:</strong> the Soviet era, the System Change after 1989 and today's controversies."),
            P("⏱️", "2.25 Hours Walk", "<strong>2.25 hours</strong> from Kossuth Lajos tér, by the Parliament, to Vigadó tér." + note("Look for the orange umbrella by the tram stop."), True),
            P("⛪", "St. Stephen", "<strong>Liberty Square, St. Stephen's Basilica and the Danube promenade</strong> are on the route."),
            P("💶", "Free / Tips", "<strong>Free to book; you tip the guide</strong> at the end." + note("About 30 people on my tour; wheelchair-friendly.")),
        ],
        "best_for": {"pick_html": "for your first morning in Budapest: Parliament to the Danube in 2.25 hours, free, all ages.",
                     "skip_html": "if you want a native English speaker: my guide was Hungarian, which also brought a real local view."},
        "faq": [
            ("Is it really free?", "Yes. It is tip-based: you pay the guide what you think the tour was worth."),
            ("Where do we meet?", "At Kossuth Lajos tér by the Parliament, next to the tram stop. Look for an orange umbrella."),
            ("Is it accessible?", "Yes, the tour is wheelchair-friendly."),
            ("How big is the group?", "About 30 people on my tour, and it still worked well."),
            ("Where does it end?", "At Vigadó tér on the Danube."),
        ],
        "price": price([{"label": "Tour", "price": "Free (tips)"}], "Tip-based; book a spot in advance. " + FREE_NOTE),
    },
    "card-5": {
        "tested": tested("A 2-hour English walking tour.", "item-5-buda-castle-walking-tour"),
        "pills": [
            P("🏰", "Buda Castle Walk", "<strong>The Royal Palace, Matthias Church and Fisherman's Bastion</strong> on the Castle District's cobblestone streets."),
            P("⏱️", "2 Hours Tour", "<strong>2 hours</strong> from Szentháromság tér, in front of the Trinity statue." + note("Bus 16 from Erzsébet tér goes up the hill."), True),
            P("🏯", "Fisherman Bastion", "<strong>Fisherman's Bastion and Matthias Church</strong>, the two classic Castle Hill stops."),
            P("👑", "Royal History", "<strong>Facts, not legends:</strong> a no-nonsense overview of the district's past."
              + note("Wheelchair accessible; about 25 people on my tour.")),
        ],
        "best_for": {"pick_html": "for Castle Hill by day on a budget: Matthias Church and Fisherman's Bastion for €12.",
                     "skip_html": "in a heat wave: it is 2 hours outdoors on the hill."},
        "faq": [
            ("Where do we meet?", "At Szentháromság tér, in front of the Trinity statue opposite Matthias Church."),
            ("What does it cover?", "The Royal Palace (Buda Castle), Matthias Church and Fisherman's Bastion."),
            ("Is it accessible?", "Yes, the whole tour is wheelchair accessible."),
            ("How big is the group?", "About 25 people on my tour; it never felt crowded."),
            ("Any tips?", "Prepare for the weather: on a hot day it is 2 hours in the sun."),
        ],
        "price": price([{"label": "Adult", "small": "2 hours", "price": "€12"}]),
    },
    "card-6": {
        "tested": tested("A 3-hour English tour.", "item-6-budapest-grand-city-tour"),
        "pills": [
            P("🚌", "Bus &amp; Walk Combo", "<strong>Air-conditioned coach plus short walks</strong> on both sides of the river."),
            P("⏱️", "3 Hours Tour", "<strong>3 hours</strong> from the Cityrama office at Báthory utca 19." + note("Metro M2 or M3, then a short walk."), True),
            P("🏛️", "Pest From the Coach", "<strong>Drives past</strong> the Opera House, City Park (Városliget) and Keleti station." + note("Mostly drive-bys on the Pest side.")),
            P("🗿", "Heroes Square", "<strong>A short stop at Heroes' Square</strong>, then up Castle Hill from the side opposite the Danube."
              + note("Not suitable for mobility-impaired travellers.")),
        ],
        "best_for": {"pick_html": "for one morning, the whole city: coach plus short walks from Heroes' Square to Castle Hill.",
                     "skip_html": "if you want depth: the Pest side is mostly seen from the bus."},
        "faq": [
            ("Is it a bus or a walking tour?", "Both: air-conditioned coach rides with short walks, the longest one in the Castle District."),
            ("Where do we meet?", "At the Cityrama & Gray Line office, Báthory utca 19 (metro M2 or M3)."),
            ("Is it accessible?", "No, it is not suitable for mobility-impaired travellers."),
            ("What is the highlight?", "The Castle District, reached from the side opposite the Danube."),
            ("Is it enough to see Budapest?", "It is a quick overview. For more depth, set aside a full day."),
        ],
        "price": price([{"label": "Adult", "small": "3 hours", "price": "€35"}]),
    },
    "card-7": {
        "pills": [
            P("🍲", "Food Tour", "<strong>Traditional soup, lángos, chicken paprikash and somlói trifle</strong> at four local eateries."
              + note("Vegetarian possible; no gluten-free or vegan menu yet.")),
            P("⏱️", "2.5 Hours Walk", "<strong>2.5 hours</strong> from Kazinczy utca 29-31, by the Kazinczy Street Synagogue, where it also ends.", True),
            P("🍽️", "4 Eateries", "<strong>Four stops</strong> through District VII and Andrássy Avenue, so it doubles as a sightseeing walk."
              + note("Come hungry: guests say the portions are big.")),
            P("🍷", "3 Drinks", "<strong>Pálinka, a Dreher beer and sweet Tokaji wine.</strong>" + note("Alcohol-free on request.")),
        ],
        "best_for": {"pick_html": "for food lovers and first-timers: lángos, chicken paprikash and somlói cake with pálinka and Tokaji, in 2.5 hours.",
                     "skip_html": "if you eat gluten-free or vegan: the operator can't cater for that yet."},
        "faq": [
            ("What do we eat?", "A traditional soup, lángos, chicken paprikash and somlói trifle cake."),
            ("Which drinks are included?", "Three: a shot of pálinka, a Dreher beer and sweet Tokaji wine. Alcohol-free options on request."),
            ("Can I eat gluten-free or vegan?", "Not yet. Vegetarians are fine, with a smaller menu."),
            ("Is it accessible?", "No, it is not suitable for wheelchair users."),
            ("Where does it start?", "Kazinczy utca 29-31 in District VII, by the Kazinczy Street Synagogue. Astoria (M2) or Deák Ferenc tér are a 5-minute walk."),
        ],
        "price": price([{"label": "Adult", "small": "2.5 hours, 4 stops, 3 drinks", "price": "€62"}]),
    },
    "card-8": {
        "pills": [
            P("🏛️", "Communism &amp; 1956", "<strong>Where 45 years of Soviet occupation still stands:</strong> the Soviet memorial on Liberty Square, Cardinal Mindszenty's windows, Cold War bunker shafts and 1956 sites."),
            P("⏱️", "2 Hours Tour", "<strong>2 hours</strong>, starting at the Parliament on the walking options." + note("The Retro Center option adds a 1-hour visit."), True),
            P("👥", "Max 10 People", "<strong>Small groups of up to 10</strong>, led by a local guide trained in history who shares family stories."),
            P("🎟️", "Museum Ticket", "<strong>House of Terror or Budapest Retro Center ticket included</strong>, depending on the option."
              + note("The House of Terror visit is self-guided, and some rooms lack English text.")),
        ],
        "best_for": {"pick_html": "for history lovers who want the Soviet era explained by a local, with a House of Terror or Retro Center ticket included.",
                     "skip_html": "with young children: the House of Terror covers interrogation cells and deportations."},
        "faq": [
            ("Which options are there?", "Morning walk + Budapest Retro Center (guided), afternoon walk + House of Terror (self-guided), or a guided House of Terror tour only."),
            ("How big are the groups?", "Up to 10 people."),
            ("Where do we meet?", "It depends on the option; the walking options start at the Parliament."),
            ("Is the House of Terror visit guided?", "Only on the guided museum option. After the afternoon walk you visit on your own; the museum's audio guide helps."),
            ("Is it suitable for children?", "Not for young ones: the themes are heavy."),
        ],
        "price": price([{"label": "Walk + museum ticket", "small": "from", "price": "€50"}]),
    },
    "card-9": {
        "pills": [
            P("🧑‍🏫", "Private Guide", "<strong>Only your group</strong>, in English, Spanish, French or Italian."),
            P("⏱️", "2 to 8 Hours", "<strong>You pick the length</strong>, from 2 to 8 hours." + note("One guest clocked about 12 km on a full-day version."), True),
            P("🏨", "Hotel Pickup", "<strong>The guide meets you at your accommodation</strong> if it is in the city."),
            P("🗺️", "Your Route", "<strong>You decide what to see</strong>, from the big sights to cafés and neighbourhoods tourists miss."
              + note("Wheelchair-accessible. Museum tickets, food and transport are extra.")),
        ],
        "best_for": {"pick_html": "for families, couples and slow walkers who want their own guide, their own pace and a route built around them.",
                     "skip_html": "on a budget or with a big group: the price is per person, so it adds up."},
        "faq": [
            ("How long can it be?", "2 to 8 hours, your choice. Don't book 8 hours in one go unless you like walking about 12 km."),
            ("Which languages?", "English, Spanish, French or Italian."),
            ("Where does it start?", "At your accommodation, if it is in the city."),
            ("Is it accessible?", "Yes, the tour is wheelchair-accessible."),
            ("What is not included?", "Museum tickets, food and drinks, and transport. The team can help book museum tickets."),
        ],
        "price": price([{"label": "Per person", "small": "private, from 2 hours", "price": "€40"}]),
    },
    "card-10": {
        "pills": [
            P("🌉", "Buda + Pest", "<strong>St. Stephen's Basilica, the Parliament, Matthias Church, Buda Castle and the Royal Palace</strong> in one loop."),
            P("⏱️", "3 Hours Walk", "<strong>3 hours on foot</strong> from Szent István tér 4, with a climb on the Buda side.", True),
            P("🗣️", "6 Languages", "<strong>English, French, German, Italian, Russian or Spanish.</strong>"),
            P("👥", "Small Groups", "<strong>Private or small-group options</strong>, instead of a free-tour crowd."
              + note("Optional public transport across the Danube costs about 2,000 HUF.")),
        ],
        "best_for": {"pick_html": "for your first day if you want Buda and Pest in one walk with a paid, smaller group: Basilica to Buda Castle in 3 hours.",
                     "skip_html": "if you already plan the free Inner City walk and the Buda Castle tour: together they cover the same ground in more depth."},
        "faq": [
            ("Which languages does it run in?", "English, French, German, Italian, Russian and Spanish."),
            ("Where do we meet?", "Szent István tér 4, in front of St. Stephen's Basilica. Bajcsy-Zsilinszky út (M1) or Deák Ferenc tér are a 3-minute walk."),
            ("Is transport included?", "No. The optional public transport across the river (4 tickets) costs about 2,000 HUF."),
            ("Is it hard going?", "It is 3 hours on foot, with a climb on the Buda side."),
            ("Can we go private?", "Yes, private and small-group options are offered."),
        ],
        "price": price([{"label": "Adult", "small": "3 hours", "price": "€35"}]),
    },
}
