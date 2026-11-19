# -*- coding: utf-8 -*-
"""Upgrade spec for best-hostels-budapest.html (scripts/listicle_upgrade.py).

Facts from the page's own reviews and quick facts (prices for near dates checked 14 Nov 2026).
Personally tested: 9 of 10 (I stayed in all but The Hive, which is marked as not stayed in).
"""

PAGE = {
    "noun": "hostels",
    "filter_aria": "Filter hostels",
    "filters": [
        {"label": "Trip style", "chips": [("party", "🎉 Social &amp; party"), ("quiet", "😴 Quiet sleep"),
                                           ("nomad", "💻 Digital nomads")]},
        {"label": "Rooms &amp; extras", "chips": [("private", "🛏️ Private rooms"), ("kitchen", "🍳 Guest kitchen")]},
        {"label": "Budget &amp; proof", "chips": [("budget", "💶 €11 or less"), ("tested", "✓ Personally tested")]},
    ],
}

NOTE = "Lowest price for near dates, checked 14 Nov 2026; prices change by date and the final price shows before you pay."
VIA = "Booked securely via Hostelworld"
SUB = "dorm bed per night"


def tested(name, what, anchor):
    return {"chip": "✓ Personally Tested",
            "pop_html": f"<strong>I stayed at {name} myself.</strong> Everything on this card comes from my own stay."
                        f'<span class="bpa-lang-note">What I checked: {what}. <a href="#{anchor}">Full review ↓</a></span>'}


def price(rows):
    return {"sub": SUB, "rows": rows, "note": NOTE}


CARDS = {
    "card-1": {
        "tested": tested("Maverick Central Market", "dorms, bathrooms, kitchen, noise and long-stay value",
                         "section-1-maverick-urban-lodge"),
        "faq": [
            ("Is Maverick a party hostel?",
             "No. It is social without party noise: you meet people easily in the common areas, without 4 AM shouting in the corridors."),
            ("Is it good for a long stay?",
             "Yes. I paid €280 for 30 nights in March, about €9.33 a night. Dorm beds start from about €10 on near dates."),
            ("Is it quiet at night?",
             "Yes. It is on Lónyay utca, a smaller side street in District IX, and street noise was minimal across my 30 nights."),
            ("What should I watch out for?",
             "The kitchen gets cramped at peak times and the fridge is always full. I had a pullover stolen, so use the large lockers."),
            ("How do I get there?",
             "Kálvin tér (M3, M4) and Fővám tér (M4, trams 2, 47, 49) are a short walk. Check-in from 15:00, check-out by 11:00, no curfew."),
        ],
        "price": price([{"label": "Dorm bed", "price": "€10"}, {"label": "Private room", "price": "€28"},
                        {"label": "My 30-night stay", "small": "March", "price": "€280"}]),
        "trust": ["<b>No curfew</b>, check-in from 15:00", "<b>Privacy curtains</b> and large lockers"],
    },
    "card-2": {
        "tested": tested("Onefam Budapest", "rooms, storage, showers, activities and noise", "section-2-hostel-one"),
        "faq": [
            ("Is there an age limit?",
             "Yes. Onefam takes guests aged 18 to 39 only."),
            ("What activities are included?",
             "Free daytime activities, then drinking games at the bar and pub crawls into the Jewish Quarter at night."),
            ("When does it get quiet?",
             "The party usually winds down around 11 PM to midnight, when the crowd heads out to the ruin bars."),
            ("What are the downsides?",
             "There is no shelf on the bunks for your phone or wallet, the shower temperature can fluctuate, and it costs more than most Budapest hostels."),
            ("How do I get there from the airport?",
             "Take the 100E airport bus to Deák Ferenc tér (also M1, M2, M3), about a 4-minute walk. Check-in runs 15:00 to 23:00."),
        ],
        "price": price([{"label": "Dorm bed", "price": "€14"}]),
        "trust": ["<b>Free daily activities</b> and pub crawls", "<b>No curfew</b>, ages 18 to 39"],
    },
    "card-3": {
        "tested": tested("Avenue Hostel", "my 10-bed room, meals, staff and noise", "section-3-avenue-hostel"),
        "faq": [
            ("What meals are included?",
             "A free breakfast, plus discounted dinners (with a small minimum bar spend when I stayed)."),
            ("Is it noisy?",
             "Yes. It sits on the Oktogon junction with trams passing all night, so bring earplugs."),
            ("Which room should I book?",
             "My 10-bed room was the weak spot. The 4, 8 and 12-bed rooms are nicer and worth the few extra euros."),
            ("Do I need a padlock?",
             "Yes. Padlocks are not included for the lockers; bring one or buy one at reception for about €3."),
            ("Who can stay?",
             "Ages 6 to 49. Check-in runs 14:00 to midnight, reception is open 24/7 and there is no curfew."),
        ],
        "price": price([{"label": "Dorm bed", "small": "breakfast included", "price": "€8"},
                        {"label": "Padlock", "small": "at reception", "price": "about €3"}]),
        "trust": ["<b>Free breakfast</b>, cheap dinners", "<b>24/7 reception</b>, no curfew"],
    },
    "card-4": {
        "tested": tested("Flow Spaces", "pod beds, bathrooms, kitchen and the work lounge", "section-4-flow-spaces"),
        "faq": [
            ("Is it good for remote work?",
             "Yes. The lounge has a laptop-friendly work area and the hostel lists a coworking space, the best setup on this list."),
            ("What do the beds have?",
             "A privacy curtain, a socket, a lamp, an item tray and a storage box, plus a free padlock."),
            ("Is there an elevator?",
             "No. The hostel is on the 3rd floor, so heavy luggage is a pain."),
            ("Are the bathrooms private?",
             "No. They are co-ed and communal, with little privacy."),
            ("Where is it?",
             "Gönczy Pál utca 2, next to the Central Market Hall: Fővám tér (M4, trams 2, 47, 49) and Kálvin tér (M3, M4)."),
        ],
        "price": price([{"label": "Dorm bed", "price": "€10"}]),
        "trust": ["<b>Free padlock</b> and curtained pods", "<b>24/7 reception</b>, no curfew"],
    },
    "card-5": {
        "tested": tested("a&amp;o Budapest City", "room, shower, secure storage and the work lounge",
                         "section-5-a-o-budapest-city-hostel"),
        "faq": [
            ("Is it good for couples and families?",
             "Yes. The rooms are simple, quiet and clean, there are private options, and families and groups are welcome."),
            ("Are linens included?",
             "No. Bed linen and towels cost an extra 1,150 HUF (about €3)."),
            ("Is breakfast included?",
             "No. An optional hotel-style breakfast costs about €8."),
            ("Do I need a padlock?",
             "Yes, for the item cage in the room; one is not included."),
            ("Can I leave my laptop?",
             "Yes. Reception stored my laptop safely in its secure storage, and the lounge has a good laptop-friendly work area."),
        ],
        "price": price([{"label": "Dorm bed", "price": "€12"},
                        {"label": "Linen and towel", "price": "1,150 HUF"},
                        {"label": "Breakfast", "small": "optional", "price": "about €8"}]),
        "trust": ["<b>24-hour reception</b>", "<b>Private rooms</b> for couples and families"],
    },
    "card-6": {
        "tested": tested("Wombat's City Hostel", "noise at night, the bar, rooms and facilities",
                         "section-6-wombat-s-city-hostel"),
        "faq": [
            ("Is it a party hostel?",
             "A low-key one. It is easy to meet people at the hostel bar and the Gozsdu Udvar bars are steps away, but it was quiet at night and I slept well."),
            ("Do rooms have their own bathroom?",
             "Yes. Every room has an en-suite bathroom and air conditioning, and dorm beds have personal curtains, per the hostel."),
            ("Is it good value?",
             "It is priced above most Budapest hostels, and the facilities are clean but ordinary. You pay for the location and the crowd."),
            ("What are the check-in times?",
             "Check-in 14:00 to 23:00, check-out by 10:00. There is no curfew."),
            ("How far is the airport bus?",
             "Deák Ferenc tér (M1, M2, M3 and the 100E airport bus) is a 3-minute walk."),
        ],
        "price": price([{"label": "Dorm bed", "price": "€11"}]),
        "trust": ["<b>En-suite rooms</b> with air conditioning", "<b>No curfew</b>, 24-hour reception"],
    },
    "card-7": {
        "tested": tested("Central Market Hall Zen Hostel", "check-in, the host, the living room and storage",
                         "section-7-zen-hostel"),
        "faq": [
            ("Can I check in late?",
             "No. Check-in runs 14:00 to 21:00 and reception hours are limited. With a late flight, book elsewhere."),
            ("Is there a locker?",
             "There was no lockable storage when I stayed, so keep valuables on you."),
            ("Can I work there?",
             "Not really: there is no desk with sockets. Digital nomads should pick Flow Spaces or Maverick."),
            ("What is the vibe?",
             "Small, peaceful and home-like. Everyone ends up chatting on the living room sofa, with free tea and coffee."),
            ("Where is it?",
             "Vámház körút 5, by the Central Market Hall and Liberty Bridge, with M4 and tram 2 at Fővám tér."),
        ],
        "price": price([{"label": "Dorm bed", "price": "€11"}, {"label": "Private room", "price": "€15"}]),
        "trust": ["<b>Free tea and coffee</b> all day", "<b>Check in by 21:00</b>"],
    },
    "card-8": {
        "tested": tested("Adagio Hostel 2.0 Basilica", "room, bathroom, traffic noise and location",
                         "section-8-adagio-hostel-2-0-basilica"),
        "faq": [
            ("Is it close to the sights?",
             "Yes. It is at the start of Andrássy út, a few minutes' walk from St. Stephen's Basilica, the Opera and Deák Ferenc tér."),
            ("Is it noisy?",
             "My room was noisy from traffic on Andrássy út. Bring earplugs or ask for a courtyard-side room."),
            ("Are there private bathrooms?",
             "Yes. Dorms and doubles with private bathrooms are available; mine was excellent and clean."),
            ("Is there an elevator?",
             "No. It is on the first floor of a palace building, one flight of stairs up."),
            ("Is there a kitchen?",
             "Yes: fully equipped kitchens with free self-service tea and coffee, and free linen, per the hostel."),
        ],
        "price": price([{"label": "Dorm bed", "price": "€11"}, {"label": "Private room", "price": "€22"}]),
        "trust": ["<b>Steps from the Basilica</b>", "<b>Free linen</b>, tea and coffee"],
    },
    "card-9": {
        "tested": tested("Das Nest Budapest", "rooms, kitchen, hosts' tips, payment and noise",
                         "section-9-das-nest-budapest"),
        "faq": [
            ("Can I pay by card?",
             "It was cash only when I stayed. Check your booking terms and bring forints just in case."),
            ("What rooms are there?",
             "4 and 6-bed mixed or female-only dorms and a private double."),
            ("Is it noisy?",
             "It is in the nightlife district, so light sleepers should pack earplugs for Friday and Saturday."),
            ("Is there a kitchen?",
             "Yes, a fully equipped guest kitchen, good for saving money on meals."),
            ("Is it accessible?",
             "Not fully: it is not accessible for all disabilities."),
        ],
        "price": price([{"label": "Dorm bed", "price": "€15"}, {"label": "Private double", "price": "€17"}]),
        "trust": ["<b>Female-only dorms</b> available", "<b>No curfew</b>, check-in 12:00 to 23:00"],
    },
    "card-10": {
        "faq": [
            ("Is it 18+ only?",
             "Yes. The Hive is strictly 18 and over."),
            ("Is it loud?",
             "Yes. The hostel itself warns light sleepers and early risers, and guests mention noise from the club downstairs."),
            ("What is on the party programme?",
             "Daily pub crawls, bingo crawls, SPArties and party boats, per the hostel, plus a rooftop bar with happy hour from 4 to 7 PM."),
            ("Do the beds have curtains?",
             "No. Privacy curtains are a common guest request."),
            ("Can I pay by card?",
             "Yes, cash or card. There is a 24-hour reception and security lockers."),
        ],
        "price": price([{"label": "Dorm bed", "price": "€13"}, {"label": "Private room", "price": "€20"}]),
        "trust": ["<b>Rooftop bar</b>, happy hour 4 to 7 PM", "<b>24-hour reception</b>, no curfew"],
    },
}

H = "/assets/hostels/"
CARDS["card-6"].update(photos_prepend=[H + "wombats-01.avif"], photos_add=[H + "wombats-%02d.avif" % i for i in range(2, 6)])
CARDS["card-7"].update(photos_add=[H + "zen-%02d.avif" % i for i in range(1, 4)])
CARDS["card-9"].update(photos_prepend=[H + "das-nest-01.avif"], photos_add=[H + "das-nest-%02d.avif" % i for i in range(2, 10)])
# the old single photo was a Szimpla ruin bar shot, not The Hive
CARDS["card-10"].update(photos_drop_old=True, photos_add=[H + "hive-%02d.avif" % i for i in range(1, 11)])

for _c in CARDS.values():
    _c.setdefault("via", VIA)
