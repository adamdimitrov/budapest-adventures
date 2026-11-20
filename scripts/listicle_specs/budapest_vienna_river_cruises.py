# -*- coding: utf-8 -*-
"""Upgrade spec for budapest-vienna-river-cruises.html (scripts/listicle_upgrade.py).

Facts and fares from the page's own reviews and quick facts (TourRadar listings). Nothing tested.
Ratings are operator ratings: the popover says so in its heading.
"""

PAGE = {
    "noun": "cruises",
    "filter_aria": "Filter Budapest to Vienna cruises",
    "filters": [
        {"label": "Trip", "chips": [("xmas", "🎄 Christmas markets"), ("summer", "☀️ Spring &amp; summer"),
                                     ("budvie", "➡️ One way Budapest to Vienna")]},
        {"label": "Included", "chips": [("drinks", "🥂 Drinks included"), ("tips", "💵 Tips included")]},
        {"label": "Budget", "chips": [("under2k", "💲 Under $2,000")]},
    ],
}

NOTE = "Per person in a twin cabin, 2 sharing. Fares change by date; the final price shows before you pay."


def card(per_day, faq, rows, extra_trust):
    return {"fold_note": True, "via": "Booked securely via TourRadar", "faq": faq,
            "price": {"sub": "per person, 2 sharing", "rows": rows, "note": NOTE},
            "trust": [f"<b>About {per_day}</b> per day", extra_trust]}


def r(date, price):
    return {"label": date, "price": price}


CARDS = {
    "card-1": card("$172", [
        ("Which date is cheapest?",
         "8 December 2026 at $859, then 16 December at $921. Early dates cost more: $1,621 on 30 November."),
        ("Where does it start and end?",
         "In Vienna. It sails to Budapest and Bratislava and back, so Budapest is a stop, not the finish."),
        ("Which drinks are included?",
         "Draft beer, house wine, soft drinks, water, coffee and tea by the glass, a welcome and farewell cocktail and a Captain's Dinner."),
        ("Are the excursions included?",
         "City tours of Vienna and Budapest and a Bratislava walk are free when at least 10 guests speak the same language."),
        ("What is extra?",
         "Tips (about €7 per person per day), transfers and insurance."),
    ], [r("8 Dec 2026", "$859"), r("16 Dec 2026", "$921"), r("12 Dec 2026", "$1,151"), r("4 Dec 2026", "$1,446"),
        r("30 Nov 2026", "$1,621"), r("4 Dec 2027", "$1,348")], "<b>Beer and wine</b> by the glass included"),
    "card-2": card("$346", [
        ("Which direction is cheaper?",
         "Vienna to Budapest: $1,731 on 20 Nov 2027 and $2,223 on 28 Nov 2026, against $2,985 for Budapest to Vienna on 24 Nov 2026."),
        ("What is included?",
         "All tips, airport transfers and port taxes, wine, beer and soft drinks with lunch and dinner, guided tours in all three cities and a folklore dinner in Budapest."),
        ("Is there a minimum age?",
         "Yes, 12."),
        ("How big is the ship?",
         "An Emerald Star-Ship (Astra, Luna or Destiny) for up to 182 guests."),
        ("Does it visit the Wachau or Melk?",
         "No. It covers Budapest, Bratislava and Vienna only."),
    ], [r("Vienna → Budapest, 20 Nov 2027", "$1,731"), r("Vienna → Budapest, 28 Nov 2026", "$2,223"),
        r("Budapest → Vienna, 24 Nov 2026", "$2,985"), r("Budapest → Vienna, 18 Dec 2028", "$1,890")],
        "<b>Tips and transfers</b> included"),
    "card-3": card("$561", [
        ("Why pay more than for #1 or #2?",
         "For Melk Abbey and the Wachau Valley, which #1 and #2 skip, and the best operator rating of the Christmas cruises."),
        ("When is it cheapest?",
         "In 2027: $3,365 on 26 Nov and 8 Dec 2027, against $4,114 on 24 Nov 2026."),
        ("Are there extra charges?",
         "About $180 per person in upfront charges at booking, and tips are not listed as included."),
        ("Which drinks are included?",
         "Wine, beer or soft drinks with lunch and dinner, a happy hour every evening, and free Wi-Fi."),
        ("Can children come?",
         "Yes, from age 8."),
    ], [r("24 Nov 2026", "$4,114"), r("26 Nov 2027", "$3,365"), r("8 Dec 2027", "$3,365"), r("25 Nov 2028", "$3,399")],
        "<b>Happy hour</b> every evening"),
    "card-4": card("$221", [
        ("Where does it end?",
         "In Passau, a train ride from Vienna or Munich. Some dates run the other way, from Passau to Budapest."),
        ("How much Budapest do I get?",
         "Two days: an evening cruise past the illuminated city, then a city tour and the Danube Bend (Szentendre, Visegrád and Esztergom)."),
        ("Which drinks are included?",
         "Wines with dinner (not at lunch), and coffee and tea around the clock."),
        ("Which date is cheapest?",
         "15 August 2027 at $1,767, then 3 July at $1,865."),
        ("Can I cycle?",
         "Yes. The AMADEUS ships carry bicycles for exploring on your own."),
    ], [r("22 May 2027", "$2,457"), r("19 Jun 2027", "$2,168"), r("3 Jul 2027", "$1,865"), r("15 Aug 2027", "$1,767"),
        r("2 Sep 2027", "$2,114")], "<b>Port taxes</b> and city tours included"),
    "card-5": card("$282", [
        ("Are drinks really included?",
         "Yes, on board all week, from the captain's welcome cocktail to the last night. Drinks during excursions or transfers are not."),
        ("Which airport do I fly into?",
         "Vienna for both flights: the cruise starts and ends there."),
        ("How is this cruise rated?",
         "This exact cruise rates 4.4 from 20 reviews."),
        ("Which dates are there?",
         "One departure is listed so far: 22 June 2027 at $2,258."),
        ("Where does it stop?",
         "Melk and Dürnstein in the Wachau, Bratislava, a full day in Budapest, then free time in Esztergom on the way back."),
    ], [r("22 Jun 2027", "$2,258")], "<b>Drinks included</b> on board"),
    "card-6": card("$458", [
        ("How much cycling is there?",
         "Guided e-bike tours over Danube Island, the Lobau and the Prater (34 km) and up to the Leopoldsberg with Klosterneuburg Abbey."),
        ("How big are the groups?",
         "8 to 20 riders, adults only."),
        ("What is extra?",
         "Helmets, gratuities and bicycle insurance."),
        ("Where does it start?",
         "In Passau, and it ends there too."),
        ("What do I see in Hungary?",
         "Esztergom's Castle Hill and basilica, and a day in Budapest with access to the Parliament."),
    ], [r("29 May 2027", "$3,663"), r("26 Jun 2027", "$3,810"), r("7 Aug 2027", "$3,810"), r("18 Sep 2027", "$3,663")],
        "<b>8 to 20</b> riders per group"),
}
