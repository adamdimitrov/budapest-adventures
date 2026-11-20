#!/usr/bin/env python3
"""Pills for cards that do not book through GetYourGuide (hostels, TourRadar river cruises,
Silverline, Legenda, Rudas, Veli Bej, Tiqets, GuruWalk), so they also reach 6-8 pills.

Every pill restates a fact that is already on the same card (its 5 questions, price box or
trust lines), written as a dropdown pill like on the river cruise card. Time and access pills
go first, the rest after the card's own pills.

    python3 scripts/manual_pills.py && python3 scripts/listicle.py build <page>.html ...
"""
import html
import importlib.util
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YES, NO, ASK = '<span class="cd-yes">✓</span>', '<span class="cd-no">✕</span>', '<span class="cd-ask">ⓘ</span>'


def P(emoji, label, lead, body="", kind=""):
    pop = f"<strong>{lead}</strong>" + (f" {body}" if body else "")
    return {"cls": "bpa-lang" + {"time": " bpa-time", "access": " cd-access", "vibe": " fbm-vibe", "": ""}[kind],
            "emoji": emoji, "label": html.escape(label, quote=False), "pop_html": pop}


def A(label, *notes):
    return {"cls": "bpa-lang cd-access", "emoji": "♿", "label": html.escape(label, quote=False),
            "pop_html": "".join(f'<span class="bpa-lang-note">{n}</span>' for n in notes)}


PAGES = {
    "best-hostels-budapest.json": {
        "card-1": [P("🕒", "Check-in 15:00", "Check-in from 15:00,", "check-out by 11:00, no curfew.", "time"),
                   P("🙂", "Social, not party", "You meet people easily in the common areas,", "without 4 AM shouting in the corridors.", "vibe"),
                   P("🍳", "Busy kitchen", "The kitchen gets cramped at peak times", "and the fridge is always full.")],
        "card-2": [P("🕒", "Check-in 15:00–23:00", "Check-in 15:00 to 23:00,", "no curfew.", "time"),
                   P("⚠️", "Bunk downsides", "No shelf on the bunks for your phone or wallet,", "the shower temperature can fluctuate, and it costs more than most Budapest hostels.")],
        "card-3": [P("🕒", "Check-in 14:00–00:00", "Check-in 14:00 to midnight,", "reception open 24/7, no curfew.", "time"),
                   A("Ages 6 to 49", f"🎟️ <b>Ages:</b> {YES} guests aged 6 to 49")],
        "card-4": [A("No elevator", f"♿ <b>Wheelchair:</b> {NO} 3rd floor, no elevator"),
                   P("🚻", "Shared bathrooms", "Co-ed, communal bathrooms", "with little privacy.")],
        "card-5": [P("🛏️", "Linen extra", "Bed linen and towels cost extra:", "1,150 HUF (about €3)."),
                   P("🍳", "Breakfast €8", "Optional hotel-style breakfast", "for about €8."),
                   P("🔒", "Bring a padlock", "A padlock is needed for the item cage", "in the room; one is not included.")],
        "card-6": [P("🕒", "Check-in 14:00–23:00", "Check-in 14:00 to 23:00,", "check-out by 10:00, no curfew.", "time"),
                   P("🎉", "Low-key party", "Easy to meet people at the bar,", "but quiet at night: I slept well.", "vibe"),
                   P("💶", "Pricier than most", "Priced above most Budapest hostels;", "clean but ordinary. You pay for the location and the crowd.")],
        "card-7": [P("🕒", "Check in by 21:00", "Check-in 14:00 to 21:00 only,", "with limited reception hours. With a late flight, book elsewhere.", "time"),
                   P("🔓", "No lockers", "There was no lockable storage when I stayed,", "so keep valuables on you."),
                   P("💻", "No work desk", "No desk with sockets:", "digital nomads should pick Flow Spaces or Maverick.")],
        "card-8": [A("One flight up", f"♿ <b>Wheelchair:</b> {NO} first floor of a palace building, no elevator"),
                   P("🔊", "Street-side noise", "My room was noisy from traffic on Andrássy út.", "Bring earplugs or ask for a courtyard-side room."),
                   P("🍳", "Full kitchen", "Fully equipped kitchens,", "free self-service tea and coffee and free linen, per the hostel.")],
        "card-9": [P("🕒", "Check-in 12:00–23:00", "Check-in 12:00 to 23:00,", "no curfew.", "time"),
                   A("Not fully accessible", f"♿ <b>Wheelchair:</b> {NO} not accessible for all disabilities"),
                   P("💵", "Bring cash", "It was cash only when I stayed.", "Check your booking terms and bring forints just in case."),
                   P("🚺", "Female-only dorms", "4 and 6-bed mixed or female-only dorms", "and a private double.")],
        "card-10": [P("🔊", "Loud", "The hostel itself warns light sleepers and early risers,", "and guests mention noise from the club downstairs.", "vibe"),
                    P("🛏️", "No bed curtains", "The beds have no privacy curtains,", "a common guest request."),
                    P("💳", "Cash or card", "Pay by cash or card.", "24-hour reception and security lockers.")],
    },
    "best-hop-on-hop-off-bus-budapest.json": {
        "card-1": [A("Wheelchair bus", f"♿ <b>Wheelchair:</b> {YES} the bus is wheelchair accessible",
                     f"🎟️ <b>Kids:</b> {YES} under 6 ride free, child price up to 18"),
                   P("🔄", "110-minute loop", "A full loop takes about 110 minutes.", "At peak times, start at stop 1."),
                   P("✅", "Free cancellation", "Free cancellation up to 2 days before.")],
        "card-2": [A("Wheelchair bus", f"♿ <b>Wheelchair:</b> {YES} buses are wheelchair accessible",
                     "🎟️ <b>Kids:</b> child price for ages 5 to 15"),
                   P("⚠️", "Non-refundable", "This ticket can't be cancelled.", "The flexible Big Bus ticket can be cancelled up to 24 hours before.")],
    },
    "best-things-to-do-budapest-with-kids.json": {
        "card-2": [A("No age limit stated", f"🎟️ <b>Kids:</b> {ASK} no minimum age or child price stated"),
                   P("✅", "Free cancellation", "Free cancellation up to 24 hours before.", "Mobile ticket."),
                   P("🐾", "No pets", "No pets,", "except guide dogs.")],
    },
    "best-walking-tours-budapest.json": {
        "card-3": [A("Wheelchair-friendly", f"♿ <b>Wheelchair:</b> {YES} outdoors and wheelchair-accessible"),
                   P("🗣️", "English (Spanish too)", "Academic-level commentary that needs good English;", "a Spanish tour runs too."),
                   P("🏁", "Ends at the synagogue", "Meets at Madách Imre út 2", "by the yellow umbrella, ends at the Dohány Street Synagogue.")],
        "card-4": [A("Wheelchair-friendly", f"♿ <b>Wheelchair:</b> {YES} the tour is wheelchair-friendly"),
                   P("👥", "About 30 people", "About 30 people on my tour,", "and it still worked well."),
                   P("🏁", "Ends at Vigadó tér", "Meets at Kossuth Lajos tér by the orange umbrella,", "ends at Vigadó tér on the Danube.")],
    },
    "budapest-amsterdam-river-cruises.json": {
        "card-1": [A("12+ only", f"🎟️ <b>Kids:</b> {NO} minimum age 12"),
                   P("🚢", "Emerald Sky, ~180 guests", "The Emerald Sky,", "for about 180 guests."),
                   P("🚲", "Guided e-bike tours", "Guided e-bike tours", "in Vienna, along the Danube and to Waterland.")],
        "card-2": [P("🧭", "Amsterdam → Budapest", "Sails Amsterdam to Budapest only", "in this listing."),
                   P("🚲", "E-bikes & Wi-Fi", "E-bike tours along the Danube and to Klosterneuburg Abbey,", "free Wi-Fi and bicycles."),
                   P("🗺️", "Some free-time ports", "Partially guided:", "some ports are free time.")],
        "card-3": [A("Adults only (18+)", f"🎟️ <b>Kids:</b> {NO} adults only, 18+"),
                   P("🚢", "163 guests, butlers", "A Scenic Space-Ship for up to 163 guests;", "the upper Balcony Suites come with a butler."),
                   P("🚲", "E-bikes & Wi-Fi", "Wi-Fi and e-bikes included,", "with return airport transfers.")],
        "card-4": [A("16+ only", f"🎟️ <b>Kids:</b> {NO} minimum age 16"),
                   P("✈️", "No transfers", "Transfers are not included,", "and neither are flights."),
                   P("📶", "Tips & Wi-Fi included", "Gratuities and Wi-Fi", "are included.")],
        "card-5": [P("💵", "≈$504 upfront", "About $504 per person in upfront charges at booking,", "and gratuities are not listed as included."),
                   P("🍷", "Wine with meals", "Wine, beer or soft drinks", "with lunch and dinner."),
                   P("📶", "Free Wi-Fi", "Free Wi-Fi", "on board.")],
        "card-6": [P("🎄", "Markets in most ports", "Christmas markets in nearly every port,", "including Vienna, Nuremberg and Cologne."),
                   A("12+ only", f"🎟️ <b>Kids:</b> {NO} minimum age 12"),
                   P("🚢", "Emerald Sun, Luna or Astra", "Sails late November and early December", "on the Emerald Sun, Luna or Astra.")],
        "card-7": [P("🗺️", "Tour in every port", "A guided tour in every port", "on a Viking Longship."),
                   P("🍽️", "41 meals", "14 breakfasts, 13 lunches and 14 dinners", "with beer, wine and soft drinks, plus free Wi-Fi."),
                   A("Adults only (18+)", f"🎟️ <b>Kids:</b> {NO} for adults, 18+")],
    },
    "budapest-vienna-river-cruises.json": {
        "card-1": [P("🔁", "Vienna round trip", "Starts and ends in Vienna;", "Budapest and Bratislava are stops."),
                   P("🗺️", "Free city tours", "City tours of Vienna and Budapest and a Bratislava walk are free", "when at least 10 guests speak the same language."),
                   P("🍽️", "Captain's Dinner", "A welcome and farewell cocktail", "and a Captain's Dinner.")],
        "card-2": [A("12+ only", f"🎟️ <b>Kids:</b> {NO} minimum age 12"),
                   P("🚢", "182 guests", "An Emerald Star-Ship (Astra, Luna or Destiny)", "for up to 182 guests."),
                   P("💃", "Folklore dinner", "Guided tours in all three cities", "and a folklore dinner in Budapest.")],
        "card-3": [P("💵", "≈$180 upfront", "About $180 per person in upfront charges at booking;", "tips are not listed as included."),
                   A("8+ only", f"🎟️ <b>Kids:</b> {YES} from age 8"),
                   P("📶", "Free Wi-Fi", "Free Wi-Fi,", "plus wine, beer or soft drinks with lunch and dinner.")],
        "card-4": [P("🏁", "Ends in Passau", "Ends in Passau,", "a train ride from Vienna or Munich. Some dates run the other way."),
                   P("🚲", "Bicycles on board", "The AMADEUS ships carry bicycles", "for exploring on your own."),
                   P("☕", "Coffee & tea 24/7", "Coffee and tea around the clock;", "wines with dinner, not at lunch.")],
        "card-5": [P("✈️", "Vienna round trip", "Starts and ends in Vienna:", "fly into Vienna both ways."),
                   P("🏙️", "Full day in Budapest", "Melk and Dürnstein in the Wachau, Bratislava,", "a full day in Budapest, then free time in Esztergom."),
                   P("🥂", "Captain's welcome", "From the captain's welcome cocktail to the last night;", "drinks on excursions are not included.")],
        "card-6": [A("Adults only", f"🎟️ <b>Kids:</b> {NO} adults only"),
                   P("🪖", "Helmet extra", "Helmets, gratuities and bicycle insurance", "cost extra."),
                   P("🏛️", "Parliament access", "A day in Budapest with access to the Parliament,", "plus Esztergom's Castle Hill and basilica.")],
    },
    "budapest-christmas-markets.json": {
        "card-4": [P("🕒", "About 60 minutes", "About 60 minutes", "on the water.", "time"),
                   A("Not step-free", f"♿ <b>Wheelchair:</b> {NO} not suitable for wheelchair users"),
                   P("☕", "2 hot soft drinks", "Unlimited mulled wine", "plus 2 non-alcoholic hot drinks.")],
    },
    "christmas-cruises-budapest.json": {
        "card-1": [A("Kids €20 off", f"🎟️ <b>Kids:</b> {YES} ages 4 to 12 get €20 off"),
                   P("🌱", "Vegan & gluten-free", "Every course has a vegan and a gluten-free choice,", "picked when you book."),
                   P("🪟", "Window table +€55", "A window table is €210 instead of €155.", "Only the welcome champagne is included; other drinks are paid on board.")],
        "card-6": [A("Kids €84", f"🎟️ <b>Kids:</b> {YES} Kids' Dinner Package for ages 3 to 12, €84"),
                   P("📅", "25 & 26 Dec", "At 19:00 on 25 and 26 December", "from Dock 7, Vigadó tér. No dinner cruise on Christmas Eve."),
                   P("✅", "Free cancellation", "Free cancellation up to 72 hours before,", "full refund.")],
        "card-9": [P("🌾", "Gluten & dairy", "The cake contains gluten and dairy,", "with no alternative."),
                   P("📅", "Until 23 Dec", "An Advent cruise:", "the calendar runs daily until 23 December."),
                   P("📍", "Dock 11", "Dock 11 on Jane Haining rakpart,", "a short walk from the Vörösmarty tér Christmas market.")],
    },
    "new-years-eve-cruises-budapest.json": {
        "card-1": [P("🍽️", "Gala: 5 courses", "Only the Gala Dinner (€340) is seated:", "5 courses you choose, live piano and a sparkling-wine toast in front of Parliament at midnight."),
                   P("🕛", "Midnight from €125", "The Midnight Booze Cruise:", "23:00, 90 minutes, €125, unlimited wine, sparkling wine, beer and soft drinks."),
                   P("🚶", "Arrive 30 min early", "Get to the pier at least 30 minutes before boarding:", "embankments get crowded and partly closed. Plan your way home after 01:00.")],
    },
    "rudas-baths-budapest.json": {
        "card-2": [A("14+ only", f"🎟️ <b>Kids:</b> {NO} 14+ only"),
                   P("🧖", "Saunas from 8:00", "Daily 6:00 to 20:00, Mondays until 22:00;", "saunas from 8:00."),
                   P("🩴", "Bring your kit", "Towel 6,900 HUF, bathrobe 12,600 HUF, slippers 4,200 HUF", "if you buy them at the desk.")],
        "card-3": [A("14+ only", f"🎟️ <b>Kids:</b> {NO} 14+ only"),
                   P("💆", "Saunas & massages", "The sauna world and massages", "are open at night."),
                   P("🩴", "Flip-flops mandatory", "Bring a swimsuit, a towel and flip-flops", "(mandatory).")],
        "card-4": [A("14+ only", f"🎟️ <b>Kids:</b> {NO} 14+ only"),
                   P("💶", "€24 online · 8,000 HUF desk", "€24 online on Tuesday and Wednesday;", "8,000 HUF at the desk Mon, Thu and Fri until 10:45."),
                   P("🧖", "One zone, full day", "Turkish bath or wellness spa,", "one zone for the full day.")],
        "card-5": [P("💶", "€117–147 per person", "€117 to €147 per person,", "minimum 2 people."),
                   P("🌇", "Private rooftop pool", "1 hour of private rooftop pool access", "with a bottle of Hungarian sparkling wine."),
                   P("🩴", "Bring slippers & towels", "Bring slippers and towels;", "arrive by 19:40.")],
    },
    "sparty-budapest.json": {
        "card-3": [P("🚌", "Night buses home", "Night buses 907 and 973", "get you home after 3:00."),
                   P("👫", "Mixed both nights", "Fridays and Saturdays, mixed,", "22:00 to 3:00."),
                   P("📍", "Döbrentei tér 9", "Döbrentei tér 9,", "at the Buda end of Elisabeth Bridge.")],
    },
    "thermal-baths-budapest.json": {
        "card-6": [P("🤫", "Calm and quiet", "Visitors consistently describe it as calm,", "with empty pools early in the morning.", "vibe"),
                   P("🚫", "Closed 12:00–15:00", "Mon–Tue 15:00 to 21:00; Wed–Sun 6:00 to 12:00 and 15:00 to 21:00.", "It closes every day from 12:00 to 15:00."),
                   P("🩴", "Towel & slippers to buy", "Towel 1,100 HUF and slippers 1,900 HUF", "at the desk.")],
    },
}


# GetYourGuide cards that stay under 6 after scripts/fact_pills.py (run that first)
EXTRA = {
    "best-buda-castle-tours.json": {
        "card-9": [P("📍", "Starts at Clark Ádám tér", "The Castle Bus starts at Clark Ádám tér", "and runs on the upper level of Castle Hill."),
                   P("✅", "Free cancellation", "Free cancellation up to 24 hours before;", "reserve now, pay later.")]},
    "best-cave-tours-budapest.json": {
        "card-5": [P("📍", "Ensana, Margaret Island", "At Ensana Thermal Margaret Island,", "1007 Budapest."),
                   P("😷", "Not with a cold", "Not for anyone with a cold;", "a man-made salt room, not a cave you explore.")]},
    "best-day-trips-from-budapest.json": {
        "card-7": [P("⏱️", "About 5 h in Eger", "About 5 hours in Eger:", "the castle, the minaret, the old town and the Valley of the Beautiful Women cellars."),
                   P("🚆", "Train alternative", "Direct trains from Keleti reach Eger in about 2 hours;", "the cellars are a short taxi ride from the centre.")]},
    "best-hop-on-hop-off-bus-budapest.json": {
        "card-4": [P("🔄", "Up to 3 boardings", "One round with up to 3 boardings;", "it expires when you are back at Clark Ádám tér."),
                   P("🎙️", "No commentary", "No guide or commentary:", "the driver speaks English, but it is transport, not a tour."),
                   P("✅", "Free cancellation", "Free cancellation up to 24 hours before;", "reserve now, pay later.")],
        "card-6": [P("🍺", "Unlimited draught beer", "Hungarian draught beer for the whole hour.", "Prosecco is €13 a bottle, ordered a day ahead."),
                   P("🧍", "Solo-friendly", "Departures run regardless of numbers,", "and solo guests say they felt included.")]},
    "best-things-to-do-budapest-with-kids.json": {
        "card-7": [P("📍", "Paulay Ede u. 43", "Paulay Ede utca 43,", "1061 Budapest."),
                   P("✅", "Free cancellation", "Free cancellation up to 24 hours before;", "reserve now, pay later.")]},
    "best-walking-tours-budapest.json": {
        "card-10": [P("📍", "Meets at the Basilica", "Szent István tér 4, in front of St. Stephen's Basilica,", "3 minutes from Bajcsy-Zsilinszky út (M1) or Deák Ferenc tér."),
                    P("🚋", "Transport extra", "Public transport across the river is optional:", "4 tickets, about 2,000 HUF.")]},
    "new-years-eve-cruises-budapest.json": {
        "card-6": [A("Adults only", f"🎟️ <b>Age:</b> {NO} adults only"),
                   P("⛴️", "2 of 5 h on the water", "Only 2 of the 5 hours are on the water:", "check whether midnight is on the boat or at the dock."),
                   P("📍", "Dock 3/a", "Dock 3/a on Jane Haining rakpart.")]},
    "sparty-budapest.json": {
        "card-4": [P("📍", "Gate 1, Széchenyi", "Széchenyi main entrance, Gate 1,", "Kós Károly sétány 1. Arrive 20 minutes early."),
                   P("🧺", "Towel 5,000 HUF", "Towels are not included:", "5,000 HUF on site. Bring your own slippers.")]},
    "szechenyi-baths-budapest.json": {
        "card-3": [P("🔐", "Private cabin all day", "A private, lockable changing cabin for the whole day,", "plus full-day fast-track Széchenyi entry."),
                   P("⏰", "Arrive 20 min early", "Beer spa from 10:00:", "arrive 20 minutes before your slot.")]},
    "thermal-baths-budapest.json": {
        "card-2": [P("🍽️", "3-course meal", "A day pass plus a 3-course meal at Rudas Bistro,", "from €74.99. A plain entry ticket is only sold at the desk."),
                   P("🌙", "Night bathing Fri & Sat", "Friday and Saturday 22:00 to 3:00,", "online tickets only; night buses 907 and 973 afterwards.")],
        "card-3": [P("🌙", "Tuesdays until 22:00", "Open until 22:00 every Tuesday,", "7:00 to 19:00 the other days."),
                   P("📍", "Frankel Leó út 25-29", "Tram 4, 6, 17 or 19, bus 9 or 109, or the HÉV to Margit híd.", "Veli Bej is on the same street, so do not mix them up.")],
        "card-5": [P("🌙", "Thursdays until 22:00", "Open until 22:00 on Thursdays,", "9:00 to 19:00 the other days."),
                   P("🌞", "2 outdoor pools", "Two outdoor pools at 36 and 38 °C,", "with a lawn and sun loungers.")]},
}
for _pg, _cards in EXTRA.items():
    PAGES.setdefault(_pg, {}).update(_cards)


def main():
    spec = importlib.util.spec_from_file_location("kit_listicle", os.path.join(ROOT, "kit", "scripts", "listicle.py"))
    kit = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(kit)
    for page, cards in PAGES.items():
        path = os.path.join(ROOT, "data", "listicles", page)
        d = json.load(open(path))
        for c in d["cards"]:
            add = cards.get(c["id"])
            if not add or any(p.get("label") == add[0]["label"] for p in c["pills"]):
                continue   # nothing to add, or already added
            front = [p for p in add if "bpa-time" in p["cls"] or "cd-access" in p["cls"]]
            back = [p for p in add if p not in front]
            c["pills"] = (front + c["pills"] + back)[:8]
            assert len(c["pills"]) >= 6, (page, c["id"], len(c["pills"]))
        open(path, "w").write(kit.dumps(d) + "\n")
        print(page, [len(c["pills"]) for c in d["cards"]])


if __name__ == "__main__":
    main()
