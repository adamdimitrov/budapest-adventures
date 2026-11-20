# -*- coding: utf-8 -*-
"""Upgrade spec for best-day-trips-from-budapest.html (scripts/listicle_upgrade.py).

Facts from the page's own reviews and quick facts. Nothing tested.
"""

PAGE = {
    "noun": "day trips",
    "filter_aria": "Filter day trips",
    "filters": [
        {"label": "Length", "chips": [("half", "🕐 Half day"), ("full", "🗓️ Full day"), ("two", "🌍 Two countries")]},
        {"label": "Extras", "chips": [("pickup", "🚐 Hotel pickup"), ("small", "👥 Max 8 guests"), ("meal", "🍽️ Food included"),
                                       ("boat", "⛴️ Boat back (summer)")]},
        {"label": "Price", "chips": [("u100", "💶 Under €100"), ("u160", "💳 €100 to €160"), ("o160", "💎 Over €160")]},
    ],
}

NOTE = "Free cancellation up to 24 hours before. Prices change by date; the final price shows before you pay."


def price(rows, extra=""):
    return {"sub": "per person", "rows": rows, "note": (extra + " " + NOTE).strip()}


def row(label, p, small=None):
    d = {"label": label, "price": p}
    if small:
        d["small"] = small
    return d


CARDS = {
    "card-1": {
        "faq": [
            ("How big is the group?", "7 guests at most, in a Mercedes minibus, so the stops run at your pace."),
            ("How much walking is there?", "A 4.6 km, 75-minute downhill trail through the Danube-Ipoly National Park that ends at Visegrád Castle. Not for children under 8 or anyone unsteady on muddy paths."),
            ("What is not included?", "The castle ticket (€8 for adults) and lunch at the forest restaurant, where you pay for what you order."),
            ("Can I stay longer in Szentendre?", "Yes. The minibus leaves at 17:00; stay on and take the public boat or the HÉV back on your own."),
            ("Where do we meet?", "At the main entrance of St. Anne's Church, Batthyány tér, at 09:00. Look for the driver holding a Rubik's Cube."),
        ],
        "price": price([row("Adult", "€96", "8 to 9 hours"), row("Visegrád Castle", "€8", "paid on the day")]),
    },
    "card-2": {
        "faq": [
            ("Which towns does it cover?", "Visegrád, Esztergom and Szentendre in 9 hours, the lowest price for all three."),
            ("Is the boat back included?", "From May to September, Thursday to Sunday, yes. Otherwise, or when the river is too high or low, you return by coach."),
            ("Is lunch included?", "No, and neither is the Visegrád Castle ticket. The lunch version is #9."),
            ("Which language?", "Bilingual English and Spanish commentary, in a coach-size group."),
            ("Where do we meet?", "Báthory utca 19 in District V: Kossuth Lajos tér (M2) or Arany János utca (M3), then 5 minutes on foot."),
        ],
        "price": price([row("Adult", "€85", "9 hours")]),
    },
    "card-3": {
        "faq": [
            ("How long is the day?", "About 10 hours door to door, roughly half of it on the road."),
            ("What do we see?", "Esztergom Basilica, a photo stop in Štúrovo (Slovakia), the Akarattya cliff viewpoint, Tihany Abbey and free time in Balatonfüred."),
            ("Is there hotel pickup?", "Yes, from your hotel or apartment in Budapest; the exact time and driver contact arrive the day before."),
            ("Do I need ID?", "Yes, a passport or ID card for the Slovakia stop."),
            ("Can I swim in the lake?", "Not really: it is a sightseeing day. For a beach day, take the train to Balatonfüred and stay put."),
        ],
        "price": price([row("Adult", "€83", "max 8 guests")], "Meals not included."),
    },
    "card-4": {
        "faq": [
            ("What do we see in Bratislava?", "A guided old-town walk (St. Michael's Gate, the Main Square, the Blue Church) and Bratislava Castle."),
            ("And in Vienna?", "A guided walk past the Hofburg, St. Stephen's Cathedral, the Opera and the Ringstrasse, then free time."),
            ("Can I end the tour in Vienna?", "Yes, with your luggage, which turns your transfer to Austria into a sightseeing day."),
            ("How long is it?", "12.5 to 13 hours, roughly 6 of them on the motorway."),
            ("What do I need?", "A passport or EU ID card for the border crossings. Meals are not included."),
        ],
        "price": price([row("Adult", "€189", "pickup anywhere in Budapest")]),
    },
    "card-5": {
        "faq": [
            ("How far is Etyek?", "About 30 minutes each way, so most of the 4 to 5 hours is spent tasting."),
            ("What is included?", "2 family wineries with 4 wines each, snacks in the cellar and a home-cooked meal at one of the farms."),
            ("Can I eat vegetarian or gluten-free?", "Yes, on request."),
            ("What is extra?", "Coffee, soft drinks and tips."),
            ("Does it always run?", "It needs at least 2 guests; otherwise you are offered another date. Pickup is from selected central hotels."),
        ],
        "price": price([row("Adult", "€85", "4 to 5 hours, meal included")]),
    },
    "card-6": {
        "faq": [
            ("What is Gödöllő?", "The palace where Empress Elisabeth (Sissi) spent her summers, billed as the second-largest Baroque chateau in the world."),
            ("Is the palace tour guided?", "Yes, with skip-the-line entry, plus a walk in the park."),
            ("How long does it take?", "3.5 hours, ending at the InterContinental hotel in the centre."),
            ("Can I do it myself?", "Yes: the H8 HÉV from Örs vezér tere takes about 45 minutes, and a palace ticket costs a fraction of the tour price."),
            ("Which languages?", "English, German, Spanish, French and Italian. It is not suitable for wheelchair users."),
        ],
        "price": price([row("Adult", "€60", "3.5 hours")], "Food and drinks not included."),
    },
    "card-7": {
        "faq": [
            ("What is included?", "A private guide and car door to door, the Eger Castle ticket, motorway and parking fees."),
            ("How long in Eger?", "About 5 hours: the castle, the minaret, the old town and the Valley of the Beautiful Women cellars."),
            ("Is the wine included?", "No, wine tasting and meals are paid on the spot."),
            ("Which languages?", "English, German or Hungarian."),
            ("Is there a cheaper way?", "Direct trains from Keleti reach Eger in about 2 hours, and the cellars are a short taxi ride from the centre."),
        ],
        "price": price([row("Per person", "€255", "private, 8 hours")]),
    },
    "card-8": {
        "faq": [
            ("Can I swim in Hévíz in winter?", "Yes. The lake stays around 25 to 36 °C through the year, cooler in winter."),
            ("What is included?", "The return transfer, the Lake Hévíz entry ticket and a local English-speaking guide."),
            ("How long at the lake?", "About 3 hours; roughly 5 of the 8 hours are travel."),
            ("Where do we meet?", "At Népliget long-distance bus station (M3), not your hotel."),
            ("Who can come?", "Ages 16+, in groups of up to 4. Bring a swimsuit, towel and flip-flops."),
        ],
        "price": price([row("Adult", "€155", "lake entry included")], "Food not included."),
    },
    "card-9": {
        "faq": [
            ("What is different from #2?", "A 3-course Hungarian lunch in Visegrád and a guide in five languages, for €24 more."),
            ("Is the boat back included?", "Friday to Sunday from 1 May to 27 September. Other departures return by coach."),
            ("Which languages?", "English, Spanish, French, German or Italian."),
            ("Do I need ID?", "Yes: the tour crosses the Mária Valéria Bridge into Slovakia."),
            ("Is there hotel pickup?", "Yes, as an option. Otherwise meet at the Eurama office 30 minutes before departure."),
        ],
        "price": price([row("Adult", "€109", "lunch included")]),
    },
    "card-10": {
        "faq": [
            ("How much free time is there?", "About 2.5 hours in Bratislava and 2.5 hours in Vienna."),
            ("What is guided in Vienna?", "A walk through the Belvedere Gardens (about 30 minutes) and a 30-minute orientation drive around the Ringstrasse."),
            ("Are there extra costs?", "No mandatory ones beyond food: all visits on the guided parts are free."),
            ("Is there hotel pickup?", "Yes, anywhere in Budapest; the exact time is confirmed the day before."),
            ("What do I need?", "A passport or EU ID card for the border crossings."),
        ],
        "price": price([row("Adult", "€177", "about 12 hours")], "Meals not included."),
    },
    "card-11": {
        "faq": [
            ("How far is Páty?", "About 20 minutes from Budapest, so the trip takes 3 hours in all."),
            ("What do we taste?", "4 wines at each of 1 or 2 cellars, poured by the winemakers, one known for organic wine."),
            ("Is food included?", "A tapas plate of local ham, sausage, cheese and olives at the last cellar."),
            ("Who can come?", "Adults only (18+), at least 2 guests, at most 8."),
            ("Where do we meet?", "Al Habtoor Palace, Erzsébet tér 9-10 (Deák Ferenc tér)."),
        ],
        "price": price([row("Adult", "€96", "3 hours")]),
    },
    "card-12": {
        "faq": [
            ("What happens at the horse show?", "Csikós horsemen crack whips, make horses lie down on command and ride standing on two galloping horses."),
            ("What else is included?", "A farm tour with grey cattle and Racka sheep, a 15-minute carriage ride, and goulash and strudel with a shot of pálinka."),
            ("Can I eat vegetarian?", "Yes, if you tell the guide in advance; the default menu is meat."),
            ("Is it good with kids?", "Yes, and it is wheelchair accessible. Groups are 7 at most."),
            ("Where do we meet?", "Batthyány tér 7 on the Buda side (M2 or H5 HÉV)."),
        ],
        "price": price([row("Adult", "€115", "5 hours, lunch included")]),
    },
    "card-13": {
        "faq": [
            ("Do we come back by boat?", "On Friday, Saturday and Sunday tours from 1 May to 27 September. Tuesday tours and all tours out of season return by coach."),
            ("What does the guide show?", "Szentendre's Baroque centre and galleries, with free time for cafés and the Marzipan Museum."),
            ("Which languages?", "Spanish, English, French, German and Italian."),
            ("Can I go on my own?", "Yes: the H5 HÉV from Batthyány tér takes about 40 minutes for a few euros."),
            ("Is there hotel pickup?", "Yes, as an option. Otherwise meet at the Eurama office 30 minutes before departure."),
        ],
        "price": price([row("Adult", "€70", "4 hours")], "Food not included."),
    },
}
