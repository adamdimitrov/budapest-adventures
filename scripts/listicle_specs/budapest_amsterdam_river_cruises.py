# -*- coding: utf-8 -*-
"""Upgrade spec for budapest-amsterdam-river-cruises.html (scripts/listicle_upgrade.py).

Facts and fares from the page's own reviews and quick facts (TourRadar listings). Nothing tested.
Ratings are operator ratings: the popover says so in its heading.
"""

PAGE = {
    "noun": "cruises",
    "filter_aria": "Filter Budapest to Amsterdam cruises",
    "filters": [
        {"label": "Included", "chips": [("allinc", "🥂 Drinks all day"), ("tips", "💵 Tips included")]},
        {"label": "Trip &amp; budget", "chips": [("winter", "🎄 Christmas markets"), ("family", "👨‍👩‍👧 Kids 8+ welcome"),
                                                  ("under5k", "💲 Under $5,000")]},
    ],
}

NOTE = "Per person in a twin cabin, 2 sharing. Fares change by date; the final price shows before you pay."


def card(per_day, faq, rows, extra_trust, **kw):
    d = {"fold_note": True, "via": "Booked securely via TourRadar", "faq": faq,
         "price": {"sub": "per person, 2 sharing", "rows": rows, "note": NOTE},
         "trust": [f"<b>About {per_day}</b> per day", extra_trust]}
    d.update(kw)
    return d


def r(date, price):
    return {"label": date, "price": price}


CARDS = {
    "card-1": card("$265", [
        ("Why is it the best value?",
         "Tips, airport transfers and port taxes are in the fare, so it beats the cheaper-looking #2 once you add tips there."),
        ("When does it sail?",
         "From Budapest in late February. The same cruise in reverse starts at $3,163 on 20 Feb 2027."),
        ("Which drinks are included?",
         "Wine, beer and soft drinks with lunch and dinner, not all day like #3 and #4."),
        ("Is there a minimum age?",
         "Yes, 12."),
        ("What is the ship like?",
         "The Emerald Sky, for about 180 guests, with guided e-bike tours in Vienna, along the Danube and to Waterland."),
    ], [r("Lowest fare", "$3,976"), r("22 Feb 2027", "$4,129"), r("18 Feb 2028", "$4,027"), r("2 Mar 2028", "$4,498")],
        "<b>Tips and transfers</b> included"),
    "card-2": card("$263", [
        ("Which direction does it sail?",
         "Amsterdam to Budapest only, in this listing."),
        ("Which date is cheapest?",
         "19 August 2027 at $3,941. 8 May 2027 is $4,637."),
        ("Are tips included?",
         "No. Add tips for crew and guides before you compare it with #1."),
        ("Which drinks are included?",
         "Wine and beer with lunch and dinner, plus free Wi-Fi and bicycles."),
        ("Is it fully guided?",
         "Partially: some ports are free time where others run a guided tour. E-bike tours along the Danube and to Klosterneuburg Abbey are included."),
    ], [r("8 May 2027", "$4,637"), r("17 May 2027", "$5,880"), r("19 Aug 2027", "$3,941")],
        "<b>E-bike tours</b> included"),
    "card-3": card("$350", [
        ("What does all-inclusive cover?",
         "Premium drinks all day, all tips on board and ashore, return airport transfers, Wi-Fi and e-bikes."),
        ("Is $5,244 a normal price?",
         "No, it is the 22 February 2027 sailing. In March the same cruise is $9,321 to $9,933."),
        ("Can children come?",
         "No, it is adults only (18+)."),
        ("How big is the ship?",
         "A Scenic Space-Ship for up to 163 guests; the upper Balcony Suites come with a butler."),
        ("What if I can't take the February date?",
         "Compare it with #4, which costs less than Scenic in spring and includes spirits too."),
    ], [r("22 Feb 2027", "$5,244"), r("9 Mar 2027", "$9,933"), r("23 Mar 2027", "$9,321")],
        "<b>Drinks, tips and transfers</b> included"),
    "card-4": card("$581", [
        ("Which drinks are included?",
         "Unlimited drinks including spirits, plus gratuities and Wi-Fi."),
        ("What is different on the route?",
         "It adds Rothenburg from Würzburg and Heidelberg from Frankfurt."),
        ("Which date is cheapest?",
         "13 June 2027 at $8,365. 2 and 30 May 2027 are $9,008."),
        ("Is there a minimum age?",
         "Yes, 16."),
        ("Are transfers included?",
         "No, and neither are flights."),
    ], [r("2 May 2027", "$9,008"), r("30 May 2027", "$9,008"), r("13 Jun 2027", "$8,365")],
        "<b>Unlimited drinks</b> incl. spirits"),
    "card-5": card("$495", [
        ("What is special about the cabins?",
         "Panorama Suites: the whole outer wall is a window that opens onto an open-air balcony, and the beds face the river."),
        ("Are there extra charges?",
         "About $504 per person in upfront charges at booking, and gratuities are not listed as included."),
        ("Which drinks are included?",
         "Wine, beer or soft drinks with lunch and dinner, a happy hour every evening, and free Wi-Fi."),
        ("Can children come?",
         "Yes, from age 8."),
        ("When does it sail?",
         "In summer 2027: $7,424 on 3 July and $7,721 on 28 May and 15 June."),
    ], [r("28 May 2027", "$7,721"), r("15 Jun 2027", "$7,721"), r("3 Jul 2027", "$7,424")],
        "<b>Happy hour</b> every evening"),
    "card-6": card("$289", [
        ("Which markets do I see?",
         "Christmas markets in nearly every port, including Vienna, Nuremberg and Cologne."),
        ("When does it sail?",
         "Late November and early December, on the Emerald Sun, Luna or Astra."),
        ("Is 2027 cheaper?",
         "Yes. 2026 sailings are $6,786 to $8,207; 22 November 2027 is $5,745, and the lowest advertised fare is $4,342."),
        ("What is included?",
         "All tips, airport transfers, and wine, beer and soft drinks with lunch and dinner."),
        ("Is there a minimum age?",
         "Yes, 12."),
    ], [r("Lowest fare", "$4,342"), r("25 Nov 2026", "$6,786"), r("2 Dec 2026", "$6,984"), r("22 Nov 2027", "$5,745")],
        "<b>Tips and transfers</b> included"),
    "card-7": card("$442", [
        ("Why is it so well known?",
         "It is the classic Grand European Tour, with a guided tour in every port on a Viking Longship."),
        ("What is included?",
         "14 breakfasts, 13 lunches and 14 dinners with beer, wine and soft drinks, free Wi-Fi and port taxes."),
        ("Are transfers included?",
         "Only if you book Viking's flights. Tips are not listed as included."),
        ("Can I book it from anywhere?",
         "No. Online booking isn't open in every country, so check your dates first."),
        ("When does it sail?",
         "November 2026, then from March 2027. It is for adults (18+)."),
    ], [r("From", "$6,633")], "<b>Port taxes</b> included"),
}
