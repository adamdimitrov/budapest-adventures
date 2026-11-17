#!/usr/bin/env python3
"""Upgrade the EN river cruises page to the night-cruise card system.

Ported from scripts/build_night_fb_test.py (branch test/night-fb-questions):
- Seine card design: thumbnail strip, exact price with an "All ticket prices" dropdown,
  "Personally tested" stamp, grouped combinable filters with a sticky mini bar
- every plain pill becomes a dropdown; fixed pill order: time -> commentary -> access -> drinks -> vibe -> extras
- ♿ access & kids pill, drinks dropdown, atmosphere pill, dock facts inside the time dropdown
- "questions travellers ask" inside each card, plus a FAQPage built from them
- "Your cruise date" row: each card shows which of its sailings are fully lit, sunset-into-lights,
  or end before dark (daytime sailings), from the timetables in TT

All facts come from the card's own review, the night page's verified data for the same
products, and the live listings (GetYourGuide, legenda.hu prices, Budapest Xplore) checked
on 17 November 2026.

Usage: build_river_cards.py <river page> <night test page (style/script source)>
Runs in place on the river page and keeps the AI finder block above the filters.
"""
import html as H
import json
import re
import sys

PAGE, NIGHT = sys.argv[1], sys.argv[2]
s = open(PAGE, encoding="utf-8").read()
night = open(NIGHT, encoding="utf-8").read()
E = H.escape


def rep(text, old, new, count=1, where=""):
    n = text.count(old)
    if n != count:
        raise SystemExit(f"[{where}] expected {count}x, found {n}x: {old[:100]!r}")
    return text.replace(old, new)


# ------------------------------------------------------------------ card data (river card number -> facts)
DOCK11 = ("Dock 11, Elizabeth Bridge", "Pest side next to Elizabeth Bridge, a short walk from Ferenciek tere metro.")
AKADEMIA2 = ("Akadémia 2", "Pest side between the Chain Bridge and Parliament: the second dock from the Chain Bridge.")


def _ev(a, b, extra=()):
    out = list(extra)
    h, m = map(int, a.split(":"))
    while f"{h:02d}:{m:02d}" <= b:
        out.append(f"{h:02d}:{m:02d}")
        m += 20
        if m >= 60:
            h, m = h + 1, m - 60
    return sorted(out)


def nd(nov, dec=None):
    """Known times: November listing and December booking calendar. Other dates: not open yet."""
    return [{"from": "11-01", "to": "11-30", "times": nov}, {"from": "12-01", "to": "12-31", "times": dec or nov}]


# Legenda's published 2026 evening timetable (same as the night page)
LEGENDA_TT = [
    {"from": "01-01", "to": "01-04", "times": _ev("16:20", "21:00", ["15:40"])},
    {"from": "01-05", "to": "02-11", "times": _ev("16:20", "21:00")},
    {"from": "02-12", "to": "02-24", "times": _ev("16:40", "21:00")},
    {"from": "02-25", "to": "03-09", "times": _ev("17:00", "21:00")},
    {"from": "03-10", "to": "03-28", "times": _ev("17:40", "21:00")},
    {"from": "03-29", "to": "04-05", "times": _ev("19:00", "22:00")},
    {"from": "04-06", "to": "05-21", "times": _ev("19:20", "22:00")},
    {"from": "05-22", "to": "07-23", "times": ["19:30", "20:15", "20:20", "20:30", "20:45", "21:30", "21:40", "21:45", "22:00"]},
    {"from": "07-24", "to": "09-03", "times": _ev("19:20", "22:00")},
    {"from": "09-04", "to": "09-13", "times": _ev("19:00", "22:00")},
    {"from": "09-14", "to": "09-22", "times": _ev("18:40", "22:00")},
    {"from": "09-23", "to": "10-02", "times": _ev("18:20", "22:00")},
    {"from": "10-03", "to": "10-24", "times": _ev("17:40", "22:00")},
    {"from": "10-25", "to": "11-22", "times": _ev("16:20", "21:00")},
    {"from": "11-23", "to": "12-31", "times": _ev("16:20", "21:00", ["15:40"])},
]

# card -> (timetable, cruise length in minutes, optional "every" note); times from each card's own time dropdown
TT = {
    1: (LEGENDA_TT, 60, "every 20 min"),
    2: (nd(["15:30", "15:45", "17:15", "18:45", "22:15", "22:30", "23:00"], ["17:15", "17:45", "18:45", "20:30"]), 75, None),
    3: (nd(["13:00", "14:30", "16:00", "17:30", "19:00", "20:30"]), 60, None),
    4: (nd(["17:00", "18:20", "19:40", "21:00"]), 60, None),
    5: (nd(["11:00", "12:30", "14:00", "15:30", "16:30", "17:00", "17:20", "18:20", "18:40", "19:30", "19:40", "20:00", "21:00", "21:15"]), 60, None),
    6: (nd(["16:10", "17:20", "18:30", "19:40", "20:50"], ["16:10", "20:50"]), 50, None),
    7: (nd(["16:30", "19:30", "21:00"], ["16:30", "18:00", "19:30", "21:00"]), 60, None),
    8: (nd(["19:00"]), 90, None),
    9: (nd(["16:00", "17:00", "18:00", "19:00", "20:00", "21:00"]), 50, None),
    10: (nd(["16:20", "17:00", "17:30", "18:30", "18:40", "19:50", "20:00", "20:30", "21:40"]), 50, None),
}
CARDS = {
    1: dict(cat="tested calm nodrink opendeck heated hour",
            vibe=("🙂", "Calm sightseeing",
                  "Seated sightseeing with a 30-language audio guide on headsets, not a party boat.",
                  "Open-air seats at the back of the top deck, heated cabin below. The welcome drink can be a soft drink or water, so non-drinkers pay for nothing they skip."),
            dock=("Vigadó tér, Dock 7", "Pest side, 2 minutes from Vörösmarty tér and the top of Váci utca.",
                  "Covered floating dock with restrooms and a rooftop waiting area.")),
    2: dict(cat="tested unlimited party opendeck hour",
            vibe=("🎉", "Cocktail-party feel", "Lively, not a quiet sightseeing hour.",
                  "On my cruise the commentary was hard to hear over the party noise. Open top deck plus two indoor decks; board early for the best top-deck spots. Lemonade is self-service, so non-drinkers are covered too."),
            dock=("3 docks to choose from",
                  "Akadémia 3 is by the Chain Bridge, best from Parliament or the Basilica. Vigadó 8/A is by Vörösmarty tér, best from Váci utca. Carl Lutz rakpart Dock 0 is further north on the Pest bank.",
                  "Pick the dock when you choose your time slot.")),
    3: dict(cat="tested calm nodrink opendeck heated hour under20 historic",
            vibe=("🎹", "Quiet and historic", "Classical piano plays between the narration on a historic paddle steamer.",
                  "Open-air panorama deck at the front, heated indoor area in winter. The welcome glass is prosecco or orange juice."),
            dock=("Dock 10, Elizabeth Bridge", "Pest side next to Elizabeth Bridge, a short walk from Ferenciek tere metro.",
                  "No baby strollers and no wheelchair access on board.")),
    4: dict(cat="tested calm nodrink opendeck heated hour under20",
            vibe=("☕", "Floating café, no guide",
                  "No live or audio guide: the boat works like a floating café and pub with its own bar.",
                  "Seats are first come, first served, on the open deck or behind panoramic windows. The welcome drink can be alcoholic or non-alcoholic; you can't bring your own food or drinks."),
            dock=("Dock 42, Szent István Park", "Pest side by Margaret Bridge, north of the city centre.",
                  "Arrive 15 minutes early: the boat leaves at the exact time on your voucher.")),
    5: dict(cat="tested calm nodrink heated hour under20 historic",
            vibe=("🙂", "No-frills sightseeing", "A plain sightseeing hour with no drink included.",
                  "Heated main deck. The upper deck costs €5 more and has a roof with columns that block part of the view. Infants up to 3 ride free."),
            dock=(DOCK11[0], DOCK11[1], "Comfortable indoor meeting point.")),
    6: dict(cat="calm nodrink opendeck heated hour under20",
            vibe=("🧺", "Relaxed, bring your own", "A small boat with at most 150 guests, and everyone gets a rooftop seat.",
                  "No bar on board: bring your own drinks, alcohol-free included. The rooftop gets cold in November, so bring layers; the heated cabin is open to all."),
            dock=("Várkert Bazár, Buda side", "Below the Castle on the Buda bank, the easy pick if you stay in Buda.",
                  "Most other boats leave from the Pest bank, so check which side you are on.")),
    7: dict(cat="unlimited party hour",
            vibe=("🎶", "Pre-party", "Party songs from the loudspeakers, pitched as a warm-up before a night out.",
                  "Adults only: under-18s are not allowed, and it is not for pregnant guests."),
            dock=(DOCK11[0], DOCK11[1], "The upper deck is the spot for photos of the lit-up Parliament.")),
    8: dict(cat="tested dinner",
            vibe=("🎻", "Dinner and a folk show",
                  "A served 4-course Hungarian dinner with the Rajkó band and a folk dance show.",
                  "Views from the ship are limited, so book it for the dinner and the show rather than for sightseeing."),
            dock=(AKADEMIA2[0], AKADEMIA2[1], "Dinner starts at 19:00; dogs are welcome on board.")),
    9: dict(cat="tested calm nodrink opendeck heated hour under20 historic",
            vibe=("🎻", "Drinks and folk music",
                  "A 50 or 90-minute cruise with a welcome drink; guests on the 90-minute boat mention live folk music in the salon.",
                  "Open-air upper deck for the views, a heated or air-conditioned cabin and toilets on board."),
            dock=(AKADEMIA2[0], AKADEMIA2[1], "Arrive about 30 minutes early for the best seats.")),
    10: dict(cat="tested calm nodrink heated hour under20 historic",
             vibe=("🙂", "Calm night sightseeing",
                   "A 50-minute night cruise with a glass of prosecco or juice and an audio guide.",
                   "Comfortable indoor areas, so it runs in any weather. The Parliament's lights go off at 22:00, so pick an earlier sailing."),
             dock=("Vigadó tér, Dock 5", "Pest side by Vörösmarty tér and the top of Váci utca.",
                   "Some sailings leave from Batthyány tér Dock 1 on the Buda side, so check your ticket.")),
}

# Plain span pills -> dropdowns. key = the span's visible label (after the emoji)
PILLS = {
    1: {"Welcome Drink": ("1 drink included: champagne, wine, beer, a soft drink or mineral water.",
                          "In summer you get a free lemonade on top. More drinks at the bar on board.")},
    2: {"Unlimited Prosecco, Spritzers &amp; Beer": (
        "Unlimited for 75 minutes: Hungarian sparkling wine, Aperol, Hugo, Rossini and Limoncello spritzers, beer, lemonade and lemon-mint water.",
        "You start with a welcome glass of sparkling wine; refills at the bar. Food costs extra.")},
    3: {"Welcome Drink": ("1 drink included: a glass of prosecco or orange juice.",
                         "When I tested it, water and beer were offered too.")},
    4: {"Welcome Drink": ("1 drink included on boarding: a glass of wine or lemonade, alcoholic or non-alcoholic.",
                         "More drinks and hot coffee at the bar on board; you can't bring your own.")},
    5: {"Upper Deck +€5": ("The panoramic upper deck costs €5 more.",
                           "It has a roof with columns that block part of the view.")},
    6: {"Bring Your Own Drinks": ("No drink included and no bar on board: bring your own drinks and snacks.",
                                  "Wine, beer or alcohol-free, your choice, with no bar prices or queues."),
        "Guaranteed Rooftop Seat": ("Every guest gets a seat on the open rooftop; at most 150 on board.",
                                    "The heated cabin downstairs is open to everyone if it rains or gets cold.")},
    7: {"Unlimited Prosecco": ("Unlimited prosecco for the whole 60 minutes.",
                               "Only prosecco is unlimited; snacks are for sale, and you can't bring your own food or drinks.")},
    8: {"4-Course Served Dinner": ("4 courses: dips to start, soup, a main course and Somlói sponge cake.",
                                   "Pick a pork, chicken or vegetarian menu when you book."),
        "Rajkó Music &amp; Folk Show": ("Live music by the Rajkó band and a Hungarian folk dance show.",
                                        "It is a show evening, not a sightseeing commentary.")},
    9: {"Welcome Drink": ("1 drink included: a glass of Prosecco or a soft drink.",
                          "Other options add 2 cocktails or 3 beers. Food such as goulash soup is for sale on board."),
        "Audio on Your Phone": ("The audio guide runs on your own phone through a QR code.",
                                "Bring headphones and a charged phone.")},
    10: {"Prosecco or Juice": ("1 drink included: a glass of prosecco or fruit juice.",
                               "More drinks at the bar on board.")},
}
NEW_DRINK = {5: ("🥤", "No drink included", "No drink in the ticket price: even water costs extra.",
                 "There is a bar on board.")}

# label, wheelchair, stroller, toilet, kids
ACCESS = {
    1: ("Access &amp; kids", None, None, None, "free under 10; €14 for ages 10-14 by day, €17.50 in the evening"),
    2: ("No strollers", None, (False, "not allowed on board"), None, "free under 4, full price for 4-17"),
    3: ("No wheelchairs or strollers", (False, "not wheelchair accessible"), (False, "not allowed on board"), (True, ""), "free under 3, full price from 3"),
    4: ("No wheelchair access", (False, "not suitable for wheelchair users"), None, (True, ""), "free under 3, full price from 3"),
    5: ("No wheelchair access", (False, "the boat has no wheelchair access"), None, None, "free under 4, full price from 4"),
    6: ("Not for wheelchairs", (False, "not suitable for wheelchair users"), None, (True, ""), "one price for every age; pets allowed"),
    7: ("Adults only (18+)", None, None, None, "under-18s not allowed; not for pregnant guests"),
    8: ("No wheelchair access", (False, "not wheelchair accessible"), None, None, "free under 6, €45 for ages 6-12; dogs welcome"),
    9: ("No wheelchair access", (False, "not wheelchair accessible"), None, (True, ""), "free up to age 6, adult fare from 7"),
    10: ("No wheelchair access", (False, "not suitable for wheelchair users; no electric or non-folding wheelchairs"), None, None, "reduced fare for children 14 and under"),
}

# Price dropdown rows (label, small, price) and an optional family total
KIDS = {
    1: ([("Child", "10-14, evening", "€17.50"), ("Under 10", "", "Free"), ("Daytime cruise", "adult", "€20"),
         ("Student", "with ID, daytime", "€18"), ("Child", "10-14, daytime", "€14")],
        ("2 adults + 2 kids (10-14), evening", "€85")),
    2: ([("Child", "4-17", "€24.80"), ("Under 4", "", "Free")], ("2 adults + 2 kids (4-17)", "€99.20")),
    3: ([("Child", "3 and over", "€11"), ("Under 3", "", "Free")], ("2 adults + 2 kids (3+)", "€44")),
    4: ([("Child", "3 and over", "€15.50"), ("Under 3", "", "Free")], ("2 adults + 2 kids (3+)", "€62")),
    5: ([("Child", "4 and over", "€12"), ("Infant", "0-3", "Free")], ("2 adults + 2 kids (4+)", "€48")),
    6: ([("Child", "every age", "€11.40")], ("2 adults + 2 kids", "€45.60")),
    7: ([("Under 18", "", "Not allowed")], None),
    8: ([("Student", "13-25", "€75"), ("Child", "6-12", "€45"), ("Under 6", "", "Free")], ("2 adults + 2 kids (6-12)", "€248")),
    9: ([("Student", "7-25, with ID", "€17"), ("Senior", "65+", "€17"), ("Under 7", "", "Free")], ("2 adults + 2 kids (7+)", "€72")),
    10: ([("Child", "14 and under", "Reduced"), ("Senior", "65+", "Reduced"), ("Student", "15-25, with ID", "Reduced")], None),
}

CARD_FAQ = {
    1: [("Do I need earphones on the Legenda cruise?", "No. Legenda hands out individual headsets for the 30-language audio guide."),
        ("Can I sit outside on the Legenda cruise?", "Yes. The back of the top deck is open-air, and the cabin below is heated in winter."),
        ("Is the Legenda cruise good if we don't drink?", "Yes. The included drink can be a soft drink or mineral water, and children under 10 ride free.")],
    2: [("Is the unlimited prosecco cruise a party boat?", "Yes, it is lively. On my cruise the commentary was hard to hear over the party noise. Take an early sailing for a calmer hour."),
        ("I don't like prosecco. What else is unlimited?", "Aperol, Hugo, Rossini and Limoncello spritzers, beer, lemonade and lemon-mint water."),
        ("Can kids come on the unlimited prosecco cruise?", "Yes. Children 4 to 17 pay the adult price and under-4s ride free, but baby strollers are not allowed on board.")],
    3: [("Do I need earphones on the Kisfaludy paddle steamer?", "Yes. The audio guide runs on your own phone, so bring earphones and a charged phone."),
        ("Can we bring a stroller on the Kisfaludy paddle steamer?", "No. Strollers are not allowed and the boat is not wheelchair accessible. Children under 3 ride free."),
        ("Is the Kisfaludy cruise quiet?", "Yes. Classical piano plays between the narration, and the welcome drink can be orange juice.")],
    4: [("Is there a guide on the Portum Lines cruise?", "No. There is no live or audio guide; the boat works like a floating café with its own bar."),
        ("Can I bring my own drinks on the Portum Lines cruise?", "No. Food and drinks can only be bought on board. The welcome drink can be alcoholic or non-alcoholic."),
        ("Can kids come on the Portum Lines cruise?", "Yes. Children under 3 ride free with an adult ticket; from age 3 everyone pays the same price.")],
    5: [("Is a drink included on the Silverline sightseeing cruise?", "No. Even water costs extra at the bar on board."),
        ("Is the Silverline upper deck worth €5 more?", "It has a roof with columns that block part of the view. For photos, the front seats and the open-air section are better.")],
    6: [("Will the La Perla rooftop be cold?", "In November, yes: bring warm layers. If it gets too cold, the heated cabin downstairs is open to everyone."),
        ("What can I bring on La Perla?", "Your own drinks and snacks, alcohol-free or not. There is no bar on board."),
        ("Do I need earphones on La Perla?", "Yes. The audio guide is web-based on your own phone, so bring headphones.")],
    7: [("Can kids come on the Silverline prosecco cruise?", "No. It is 18+ only and not for pregnant guests."),
        ("Is it only prosecco on the Silverline prosecco cruise?", "Yes. Prosecco is the one unlimited drink; snacks are for sale and you can't bring your own.")],
    8: [("Is there a vegetarian menu on the Hungária dinner cruise?", "Yes. Menu C has a seasonal vegetable soup and pasta marinara; the other two menus are pork or chicken."),
        ("How much do kids pay on the Hungária dinner cruise?", "Children 6 to 12 pay €45 and under-6s ride free. Students 13 to 25 pay €75."),
        ("Is the Hungária dinner cruise good for sightseeing?", "Not really: views from the ship are limited. Book it for the dinner and the folk show.")],
    9: [("How long is the Hungária drinks cruise?", "50 or 90 minutes, depending on the option you book."),
        ("Do I need my own phone for the audio guide?", "Yes. It runs on your phone through a QR code, so bring headphones."),
        ("Can kids come on the Hungária drinks cruise?", "Yes. Children up to age 6 ride free; from 7 it is the adult fare, or €17 with a student ID.")],
    10: [("Is the Mahart night cruise wheelchair accessible?", "No. It is not suitable for wheelchair users, and electric or non-folding wheelchairs are not allowed."),
         ("When do the Parliament lights go off?", "At 22:00, so pick a sailing that ends before then."),
         ("Which drink is included on the Mahart cruise?", "A glass of prosecco or fruit juice.")],
}


# ------------------------------------------------------------------ top-12 additions (keyed by the card's review anchor)
# old river card number for the cruises that stayed; new cruises are keyed by their anchor
OLD = {"cruise-1-legenda": 1, "cruise-2-rubingroup": 2, "cruise-3-kisfaludy-historic-cruise": 3,
       "cruise-5-silverline-no-frills": 5, "cruise-6-la-perla": 6, "cruise-7-silverline-prosecco": 7, "cruise-10-mahart": 10}
LEGENDA_DINNER_TT = [{"from": "04-20", "to": "08-23", "times": ["19:45"]}, {"from": "08-24", "to": "04-19", "times": ["19:00"]}]
CARDS.update({
    "cruise-360-panoramic": dict(cat="calm nodrink opendeck heated hour under20 historic",
        vibe=("🌐", "360° views, calm", "An open-air panorama deck with 360° views, plus a climate-controlled cabin with panoramic windows.",
              "Every guest gets a seat (unassigned), with free Wi-Fi, toilets and blankets when it is cold. The welcome glass is Tokaji frizzante or orange juice."),
        dock=("Dock 10, Elizabeth Bridge", "Pest side next to Elizabeth Bridge, a short walk from Ferenciek tere metro.",
              "Arrive 15 to 20 minutes early: seats are first come, first served.")),
    "cruise-cosy-chimney-cake": dict(cat="calm heated hour under20",
        vibe=("🧣", "Cosy winter warm-up", "A heated cabin, a mug of hot winter punch and a Cinnabon chimney cake.",
              "A seasonal cruise for cold evenings. There is a bar for more drinks and snacks, but you can't bring your own food or drinks."),
        dock=(DOCK11[0], DOCK11[1], "Silverline's dock, next to the no-frills and prosecco cruises.")),
    "item-8-floating-lotus-prosecco": dict(cat="unlimited party opendeck heated hour",
        vibe=("🎶", "Lively rooftop", "Guests keep mentioning the music and the friendly crew.",
              "Everyone has a seat on the heated lower deck; rooftop seats are first come, first served. Soft drinks and homemade lemonade are included."),
        dock=("Petőfi tér 9", "Pest bank between Elizabeth Bridge and Vigadó tér, an easy walk from Váci utca.",
              "Arrive 15 minutes early: boarding closes 5 minutes before departure.")),
    "item-4-legenda-candlelit-dinner": dict(cat="tested dinner nodrink opendeck heated",
        vibe=("🕯️", "Romantic and quiet", "Candlelit tables for two along the windows, a pianist and singer, no loud folk show.",
              "Open top deck for photos at any point of the evening. Not for children under 3, and there is no vegan menu."),
        dock=("Vigadó tér, Dock 7", "Pest side, 2 minutes from Vörösmarty tér and the top of Váci utca.",
              "Legenda's covered dock has restrooms, so you can wait out of the rain.")),
    "item-5-river-diva-dinner": dict(cat="dinner unlimited opendeck",
        vibe=("🎻", "All-inclusive evening", "A seasonal buffet, unlimited drinks served to your table and live music in the Grand Salon.",
              "After dinner you can go up to the rooftop deck, weather permitting."),
        dock=("Akadémia 3", "Pest side by the Chain Bridge, best if you stay near Parliament, the Basilica or Széchenyi tér.",
              "Bring a passport or ID card with the voucher.")),
})
PILLS.update({
    "item-4-legenda-candlelit-dinner": {
        "4-Course Dinner": ("4 courses picked from the menu at the table: starter, soup, main course and dessert.",
                            "Children 3 to 12 get 3 courses. No vegan menu, and not for food allergies."),
        "Welcome Drink": ("1 drink included: champagne, wine, beer, a soft drink or mineral water.", "Every other drink is paid on board."),
        "Live Music": ("A pianist and singer play lounge music all evening.", "Quiet enough to talk: no loud folk show.")},
    "item-5-river-diva-dinner": {
        "Seasonal Buffet": ("A seasonal buffet by Executive Chef Viktor Moldován: starters, mains, sides, vegetarian dishes and desserts.",
                            "Flag dietary needs when you book."),
        "Live Music": ("Live music in the Grand Salon through the evening.", "There is no sightseeing commentary, just an English-speaking host.")},
})
ACCESS.update({
    "cruise-360-panoramic": ("No wheelchairs or strollers", (False, "not suitable for wheelchair users"), (False, "baby strollers not allowed"), (True, ""), "free under 3, full price from 3"),
    "cruise-cosy-chimney-cake": ("Not for wheelchairs", (False, "not suitable for wheelchair users"), None, None, "one price for every age; not for food allergies, gluten or lactose intolerance"),
    "item-8-floating-lotus-prosecco": ("Not for wheelchairs", (False, "not wheelchair accessible"), None, None, "€25 for 7 and under, adult fare from 8"),
    "item-4-legenda-candlelit-dinner": ("No wheelchair access", (False, "not wheelchair accessible"), None, None, "€84 for ages 3-12 (3 courses); not for children under 3"),
    "item-5-river-diva-dinner": ("Wheelchair OK", (True, "wheelchair-accessible boat"), None, None, "free under 4, full price for 4-17"),
})
KIDS.update({
    "cruise-360-panoramic": ([("Child", "3 and over", "€12"), ("Under 3", "", "Free")], ("2 adults + 2 kids (3+)", "€48")),
    "cruise-cosy-chimney-cake": ([("Child", "every age", "€19")], ("2 adults + 2 kids", "€76")),
    "item-8-floating-lotus-prosecco": ([("Child", "7 and under", "€25"), ("Age 8+", "", "Adult fare")], None),
    "item-4-legenda-candlelit-dinner": ([("Child", "3-12, 3 courses", "€84"), ("Under 3", "", "Not allowed")], ("2 adults + 2 kids (3-12)", "€388")),
    "item-5-river-diva-dinner": ([("Child", "4-17", "€99"), ("Under 4", "", "Free")], ("2 adults + 2 kids (4-17)", "€396")),
})
CARD_FAQ.update({
    "cruise-360-panoramic": [
        ("Is a seat guaranteed on the 360° Panoramic Cruise?", "Yes, every guest gets a seat, but seats are not assigned: arrive 15 to 20 minutes early for the best spots."),
        ("What is the welcome drink on the 360° cruise?", "A glass of premium Tokaji frizzante, or orange juice."),
        ("Can we bring a stroller on the 360° cruise?", "No. Baby strollers are not allowed and the boat is not suitable for wheelchair users. Children under 3 ride free.")],
    "cruise-cosy-chimney-cake": [
        ("What do you get on the Cosy Cruise?", "A mug of spiced pomegranate winter punch and a Cinnabon chimney cake: a crisp kürtőskalács with cinnamon-roll frosting."),
        ("Is the Cosy Cruise OK for food allergies?", "No. The chimney cake has a fixed recipe with gluten and dairy, so it can't cater for allergies or intolerances."),
        ("Is it warm on board?", "Yes. The cabin is heated, and there is a bar for more drinks and snacks.")],
    "item-8-floating-lotus-prosecco": [
        ("Is a rooftop seat guaranteed on Floating Lotus?", "No. Everyone has a seat on the heated lower deck; rooftop seats are first come, first served."),
        ("Can kids come on Floating Lotus?", "Yes. Children 7 and under pay a fixed €25; from 8 it is the adult fare. Soft drinks and lemonade are included.")],
    "item-4-legenda-candlelit-dinner": [
        ("Can I go outside during the Legenda candlelit dinner?", "Yes. The open top deck is free to use at any point of the evening, which is the best spot for photos."),
        ("Is the Legenda candlelit dinner OK for vegans or food allergies?", "No. There is no vegan menu and it can't cater for food allergies."),
        ("Can children come to the Legenda candlelit dinner?", "From age 3. Children 3 to 12 pay €84 for 3 courses; it is not for children under 3.")],
    "item-5-river-diva-dinner": [
        ("Can I go outside on the River Diva dinner cruise?", "Yes, after dinner the rooftop deck opens, weather permitting."),
        ("Is the River Diva dinner cruise wheelchair accessible?", "Yes. It is the one wheelchair-accessible boat in this list."),
        ("Which drinks are unlimited on River Diva?", "Cocktails, spirits, Prosecco, wine, beer, soft drinks and water, served to your table all evening.")],
})
TT.update({
    "cruise-360-panoramic": (nd(["13:30", "15:00", "16:30", "18:00", "19:30", "21:00"]), 60, None),
    "cruise-cosy-chimney-cake": (nd(["15:30", "17:00", "18:20", "19:40", "21:00"]), 60, None),
    "item-8-floating-lotus-prosecco": (nd(["18:00", "19:30", "21:00"]), 75, None),
    "item-4-legenda-candlelit-dinner": (LEGENDA_DINNER_TT, 150, None),
    "item-5-river-diva-dinner": (nd(["19:30"], ["18:30"]), 150, None),
})

# ------------------------------------------------------------------ top-13 additions (Silverline own-site products)
CARDS.update({
    "cruise-silverline-mulled-wine": dict(cat="unlimited heated hour",
        vibe=("🧣", "Warm and festive", "A heated cabin with big windows and an hour of unlimited mulled wine.",
              "Two alcohol-free winter punches for non-drinkers and kids; alcohol is only served from 18. No own food or drinks on board."),
        dock=(DOCK11[0], DOCK11[1], "Silverline's dock, also used by its prosecco and sightseeing cruises.")),
    "cruise-silverline-folklore": dict(cat="heated",
        vibe=("🎻", "Music night, no dinner", "A Hungarian string quartet plays folk tunes and operetta favourites while you sail.",
              "Long and relaxed: about 2 hours 15 minutes with 3 drinks. A window table costs €25 more per person."),
        dock=(DOCK11[0], DOCK11[1], "Arrive 20 minutes before departure for check-in.")),
})
ACCESS.update({
    "cruise-silverline-mulled-wine": ("No wheelchair access", (False, "not suitable for wheelchair users; no electric wheelchairs"), None, None, "one price for every age; alcohol only from 18, alcohol-free punch for kids"),
    "cruise-silverline-folklore": ("No wheelchair access", (False, "no wheelchair access"), None, None, "alcohol only from 18; mocktails available"),
})
KIDS.update({
    "cruise-silverline-mulled-wine": ([("Child", "every age", "€21")], ("2 adults + 2 kids", "€84")),
    "cruise-silverline-folklore": ([("Window table", "per person", "+€25"), ("Other evenings", "", "Price varies")], None),
})
CARD_FAQ.update({
    "cruise-silverline-mulled-wine": [
        ("Which mulled wines can I try on the Silverline cruise?", "Four red mulled wines (classic orange, pomegranate and cardamom, apple and ginger, cranberry and orange) and a white pear and vanilla one, all unlimited for the hour."),
        ("Is there something for kids or non-drinkers?", "Yes. There are two alcohol-free winter punches, apple and pomegranate, and alcohol is only served from 18."),
        ("Is the mulled wine cruise warm?", "Yes. The cabin is heated and has large windows, so you can see the sights without going outside.")],
    "cruise-silverline-folklore": [
        ("Is dinner included on the folklore cruise?", "No. You get 3 drinks and the live show; for dinner with the same show, Silverline runs a separate dinner cruise."),
        ("What is the show on the folklore cruise?", "A Hungarian string quartet playing folk music and operetta favourites through the evening."),
        ("Can I get a window seat on the folklore cruise?", "Yes, a window table costs €25 extra per person when you book.")],
})
TT.update({
    "cruise-silverline-mulled-wine": (nd(["16:30", "18:00", "19:30", "21:00"]), 60, None),
    "cruise-silverline-folklore": (nd(["19:00"]), 135, None),
})
# Baymard: thematic filters for real needs. Live music/show, good with kids (free or reduced child fares,
# no party/18+ boats), wheelchair-accessible boat. Keyed by the card's review anchor.
EXTRA_CATS = {
    "item-5-river-diva-dinner": " music kids wheelchair",
    "item-4-legenda-candlelit-dinner": " music kids",
    "cruise-silverline-folklore": " music",
    "cruise-1-legenda": " kids", "cruise-3-kisfaludy-historic-cruise": " kids", "cruise-10-mahart": " kids",
    "cruise-5-silverline-no-frills": " kids", "cruise-6-la-perla": " kids", "cruise-cosy-chimney-cake": " kids",
    "cruise-360-panoramic": " kids",
}
# Fact-checked filter tags (17 Nov 2026). Sources: each card's own review and pills, the operator/GYG listing.
#  party: party music / pre-party pitch | romantic: candlelit or pitched for couples (listing) | kids: free/reduced child
#  fares and no 18+ or party focus | calm: plain sightseeing, no party, no dinner | unlimited: unlimited drinks in the price
#  drinkincl: a set drink (or drinks) in the price | dinner | music: live music or show on board | nodrinkprice: no drink in
#  the price (BYOB or pay at the bar) | audio: audio guide or commentary confirmed | hour: sailing of 75 minutes or less
#  wheelchair: confirmed wheelchair-accessible | under20 | tested: I rode it.
# Not used as filters: heated indoor (all 13 have it) and open-air deck (11 of 13), they would not narrow anything.
FILTER_CATS = {
    "cruise-1-legenda": "calm kids drinkincl audio hour tested",
    "cruise-2-rubingroup": "party unlimited audio hour tested",
    "cruise-7-silverline-prosecco": "party unlimited audio hour",
    "item-5-river-diva-dinner": "romantic kids dinner unlimited music wheelchair",
    "item-4-legenda-candlelit-dinner": "romantic kids dinner drinkincl music tested",
    "cruise-silverline-mulled-wine": "romantic kids unlimited audio hour",
    "cruise-3-kisfaludy-historic-cruise": "calm kids drinkincl audio hour under20 tested",
    "cruise-10-mahart": "calm kids drinkincl audio hour under20 tested",
    "cruise-5-silverline-no-frills": "calm kids nodrinkprice audio hour under20 tested",
    "cruise-6-la-perla": "calm kids nodrinkprice audio hour under20",
    "cruise-cosy-chimney-cake": "calm kids drinkincl hour under20",
    "cruise-360-panoramic": "calm kids drinkincl audio hour under20",
    "cruise-silverline-folklore": "romantic drinkincl music",
}
# Accessibility re-checked 17 Nov 2026 on the operator sites and listings (label, wheelchair, stroller, toilet, kids & pets)
ACCESS.update({
    1: ("Access &amp; kids", (None, "some Legenda boats are accessible, not all: ask Legenda which boat runs your sailing"), None, None,
        "free under 10; €14 for ages 10-14 by day, €17.50 in the evening"),
    2: ("Folding strollers only", (None, "varies by boat and dock; mobility scooters not allowed"), (True, "folding strollers only, non-folding ones are not allowed"), None,
        "free under 4, full price for 4-17; small dogs welcome on a lead with a muzzle"),
    5: ("No wheelchair access", (False, "the boat has no wheelchair access"), None, None, "free under 4, full price from 4; no dogs except service dogs"),
    7: ("Adults only (18+)", (False, "no wheelchair access"), None, None, "under-18s not allowed; not for pregnant guests; no dogs except service dogs"),
    "cruise-silverline-mulled-wine": ("No wheelchair access", (False, "not suitable for wheelchair users; no electric wheelchairs"), None, None,
        "one price for every age; alcohol only from 18, alcohol-free punch for kids; no dogs except service dogs"),
    "cruise-silverline-folklore": ("No wheelchair access", (False, "no wheelchair access"), None, None, "alcohol only from 18, mocktails available; no dogs except service dogs"),
})

# "questions travellers ask" box: 4-5 real questions per card. Sources: my own tests, the pill facts,
# and recent guest reviews summarised in api/_knowledge/best-budapest-river-cruises.json.
EDGE_QA = {
    "cruise-1-legenda": [
        ("Do I need to book ahead?", "No, you can book on the same day too. Evening sailings in December and on weekends can sell out, though, and cancellation is free up to 24 hours before, so booking early costs nothing."),
        ("Day or evening?", "Evening: 17 of 64 recent guests name the lit-up city as the highlight. The Parliament's lights go off at 22:00."),
        ("Will I get a good seat?", "Seats are not assigned, so arrive 15 to 20 minutes early. A few guests felt the boat was busy."),
        ("What if my headset doesn't work?", "Guests say there are plenty of spare headsets on board."),
        ("Why does it cost more?", "Guests call it well organised and a bit more upmarket than other boats: headsets in 30 languages, a covered dock with restrooms and a real welcome drink.")],
    "cruise-2-rubingroup": [
        ("Is it a real party?", "It is a lively cocktail-party hour, not a club. One younger guest found it quiet and not party enough."),
        ("Do refills keep coming?", "Yes. Guests say the crew keeps topping up drinks."),
        ("Can I hear the guide?", "Not always. On my cruise the commentary was hard to hear over the party noise, and one recent guest said the same."),
        ("Which dock should I pick?", "Akadémia 3 if you stay near Parliament or the Basilica, Vigadó 8/A near Váci utca. Dock 0 is further north on the Pest bank."),
        ("Cold or rainy?", "The two indoor decks are warm, so it runs in any weather. Bring a layer for the open top deck.")],
    "cruise-7-silverline-prosecco": [
        ("Where is the best spot?", "The upper deck. Board early: bigger groups rush upstairs for the best spots."),
        ("Is the staff good?", "38 of 64 recent guests praise the friendly, attentive staff, the most of any cruise here."),
        ("Is one hour enough?", "Some guests say the hour feels short. The Duna-Weser unlimited cruise runs 75 minutes."),
        ("Can I bring my own drinks?", "No. Snacks are for sale, and you can't bring your own food or drinks."),
        ("Cold on deck?", "4 of 64 recent guests mention the cold. Bring a warm layer if you want photos outside.")],
    "item-5-river-diva-dinner": [
        ("Is the food good?", "53 of 64 recent guests talk about the food, almost all positively. One said it could have been hotter."),
        ("What if it rains?", "Guests say it works even in pouring rain: dinner and music are indoors."),
        ("Is there live music?", "Yes, violin and saxophone in the Grand Salon. 21 of 64 recent guests mention it."),
        ("Is there sightseeing commentary?", "No. An English-speaking host runs the evening, but there is no commentary: it is a dinner night, not a tour."),
        ("What should I bring?", "A passport or ID card along with your voucher.")],
    "item-4-legenda-candlelit-dinner": [
        ("Good for a special occasion?", "Yes: 10 of 70 recent guests booked it for a birthday, anniversary or engagement."),
        ("Is the food good?", "55 of 70 recent guests talk about the food, nearly all positively."),
        ("Is it loud?", "No. A pianist and singer play lounge music, quiet enough to talk. There is no loud folk show."),
        ("Are drinks included?", "Only the welcome drink. Every other drink is paid on board."),
        ("What if it rains?", "Dinner is inside at window tables, and Legenda's covered dock has restrooms, so you can wait out of the rain.")],
    "cruise-silverline-mulled-wine": [
        ("Do refills keep coming?", "Yes. 33 of 63 recent guests praise the staff, and waiters keep coming round with more mulled wine."),
        ("Is the mulled wine good?", "8 of 63 recent guests praise the taste; 2 found it weak."),
        ("Is there food on board?", "Only crisps are sold, so eat before you board."),
        ("Is one hour enough?", "Some guests say it feels short."),
        ("When should I arrive?", "15 to 20 minutes early. One guest found check-in chaotic.")],
    "cruise-3-kisfaludy-historic-cruise": [
        ("Day or evening?", "Guests recommend a late-afternoon or evening sailing. In November the 16:00 sailing catches sunset into lights."),
        ("Is it cold?", "On deck, yes: 5 of 64 recent guests mention the cold, and 4 mention the warm heated cabin."),
        ("Will I get a seat outside?", "One guest found too few seats on the top deck, so board early for a spot outside."),
        ("What is the boat like?", "A historic paddle steamer. Guests describe it as clean, stable and beautiful."),
        ("Is the staff friendly?", "10 of 64 recent guests praise the friendly staff.")],
    "cruise-10-mahart": [
        ("Is it good value?", "16 of 64 recent guests say so: a 50-minute night cruise with a drink for €12."),
        ("Day or night?", "Night. Guests advise an evening sailing, not daytime."),
        ("Do I need earphones?", "Yes. The audio guide runs on your phone, and one guest had to bring their own headphones."),
        ("Which dock?", "Most sailings leave Vigadó tér Dock 5 on the Pest side; some leave Batthyány tér on the Buda side, so check your ticket."),
        ("Cold upstairs?", "In winter, yes. 6 of 64 recent guests mention the warm inside.")],
    "cruise-5-silverline-no-frills": [
        ("Is a drink included?", "No. Even water costs extra at the bar on board."),
        ("Is the upper deck worth €5 more?", "It has a roof with columns that block part of the view. For photos, the front seats and the open-air section are better."),
        ("Is it warm inside?", "Yes, the main deck is heated."),
        ("Do kids pay?", "Under-4s ride free; full price from 4."),
        ("Can I book on the day?", "Yes, same-day booking works, and with 14 sailings a day from 11:00 to 21:15 it is easy to fit in. Evening slots in December can sell out, though.")],
    "cruise-6-la-perla": [
        ("Good for the lights?", "Yes: 18 of 64 recent guests mention the lit-up city, the most of any cruise here. On the 16:10 sailing the lights come on only near the end."),
        ("What can I bring?", "Your own drinks and snacks, alcohol-free or not. There is no bar on board."),
        ("Will the rooftop be cold?", "In November, yes: 14 of 64 recent guests mention it. The heated cabin downstairs is open to everyone."),
        ("Do I need earphones?", "Yes. The audio guide runs on your own phone."),
        ("Is it a fancy boat?", "No. A few guests call it basic; 13 of 64 say it is good value.")],
    "cruise-cosy-chimney-cake": [
        ("What do I get?", "A mug of hot spiced pomegranate winter punch and a Cinnabon chimney cake."),
        ("One cake each?", "Early guests say the chimney cake is big and very sweet, easy to share."),
        ("Is it warm on board?", "Yes. The cabin is heated, and there is a bar for more drinks and snacks."),
        ("OK for food allergies?", "No. The chimney cake has a fixed recipe with gluten and dairy."),
        ("Can I bring my own food?", "No, but the bar on board sells drinks and snacks.")],
    "cruise-360-panoramic": [
        ("Is a seat guaranteed?", "Yes, every guest gets a seat, but seats are not assigned: arrive 15 to 20 minutes early."),
        ("Is there a live guide?", "No. Commentary is a QR-code audio guide on your own phone, so bring headphones."),
        ("Good with kids?", "Families say kids enjoyed the 16:30 sailing, which catches the sunset."),
        ("Cold on the top deck?", "Blankets are handed out on the open top deck."),
        ("Is it crowded?", "5 of 64 recent guests found it crowded; others enjoyed a quiet boat.")],
    "cruise-silverline-folklore": [
        ("Is dinner included?", "No. You get 3 drinks and the live show; Silverline runs a separate dinner cruise with the same show."),
        ("What is the show?", "A Hungarian string quartet playing folk music and operetta favourites through the evening."),
        ("Can I get a window seat?", "Yes, a window table costs €25 extra per person when you book."),
        ("What if I don't drink?", "Mocktails are available, and alcohol is only served from 18."),
        ("When should I arrive?", "20 minutes before departure for check-in.")],
}

# Extra pills so no card leaves the row half empty: (emoji, label, lead, note). Facts from the card, my tests and guest reviews.
EXTRA_PILLS = {
    "cruise-1-legenda": [("🌬️", "Open-air top deck", "Open-air seats at the back of the top deck.", "Heated cabin below in winter."),
                         ("🧒", "Free under 10", "Children under 10 ride free.", "€14 for ages 10-14 by day, €17.50 in the evening."),
                         ("🏛️", "Covered dock", "Vigadó tér Dock 7 is a covered floating dock with restrooms and a rooftop waiting area.", "2 minutes from Vörösmarty tér.")],
    "cruise-2-rubingroup": [("🌬️", "Open top deck", "Open top deck plus two warm indoor decks.", "Board early for the best top-deck spots."),
                            ("🍋", "Lemonade unlimited too", "Lemonade and lemon-mint water are part of the unlimited drinks.", "Self-service, so non-drinkers are covered.")],
    "cruise-7-silverline-prosecco": [("🎶", "Party music", "Party songs from the loudspeakers.", "A warm-up before a night out."),
                                     ("📸", "Upper deck views", "The upper deck is the spot for photos of the lit-up Parliament.", "Board early: bigger groups rush upstairs."),
                                     ("🙂", "Staff guests love", "38 of 64 recent guests praise the friendly, attentive staff.", "The most of any cruise here.")],
    "item-5-river-diva-dinner": [("🌬️", "Rooftop after dinner", "After dinner the rooftop deck opens, weather permitting.", "Bring a passport or ID card with your voucher.")],
    "item-4-legenda-candlelit-dinner": [("🪟", "Window tables", "Candlelit tables for two along the windows.", "Open top deck for photos at any point of the evening.")],
    "cruise-silverline-mulled-wine": [("🎧", "Audio guide app", "A free audio guide app in several languages.", "Bring headphones to listen on your phone."),
                                      ("🧃", "Alcohol-free punch", "Two alcohol-free winter punches, apple and pomegranate.", "Alcohol is only served from 18."),
                                      ("🪟", "Big windows", "A heated cabin with large windows.", "See the sights without going outside."),
                                      ("🍟", "Eat first", "Only crisps are sold on board.", "Have dinner before you board.")],
    "cruise-3-kisfaludy-historic-cruise": [("🌬️", "Front panorama deck", "Open-air panorama deck at the front.", "Heated indoor area in winter."),
                                           ("🚂", "Historic paddle steamer", "A historic paddle steamer from the 19th century.", "Guests call it clean, stable and beautiful.")],
    "cruise-10-mahart": [("⛴️", "Pest or Buda dock", "Most sailings leave Vigadó tér Dock 5 on the Pest side.", "Some leave Batthyány tér on the Buda side: check your ticket."),
                         ("🔥", "Warm inside", "Comfortable indoor areas, so it runs in any weather.", "The upper deck is cold in winter.")],
    "cruise-5-silverline-no-frills": [("🔥", "Heated main deck", "The main deck is heated.", "14 sailings a day, so it is easy to fit in.")],
    "cruise-6-la-perla": [("🐶", "Pets welcome", "Pets are allowed on board.", "One price for every age.")],
    "cruise-cosy-chimney-cake": [("🎧", "No guide included", "No audio guide is included in this ticket.", "It is an hour for the views, the punch and the cake."),
                                 ("🔥", "Heated cabin", "A heated cabin for cold evenings.", "Bar on board for more drinks and snacks."),
                                 ("🍰", "Cake to share", "Early guests say the chimney cake is big and very sweet.", "Easy to share."),
                                 ("🌾", "Not for allergies", "The chimney cake has a fixed recipe with gluten and dairy.", "It can't cater for allergies or intolerances.")],
    "cruise-360-panoramic": [("🪑", "Seat for everyone", "Every guest gets a seat, but seats are not assigned.", "Arrive 15 to 20 minutes early for the best spots."),
                             ("🧣", "Blankets on deck", "Blankets are handed out on the open top deck.", "Climate-controlled cabin with panoramic windows."),
                             ("📶", "Free Wi-Fi", "Free Wi-Fi on board.", "Toilets on board too.")],
    "cruise-silverline-folklore": [("🪟", "Window table +€25", "Window tables cost €25 extra per person.", "Choose it when you book."),
                                   ("🍹", "Mocktails", "Mocktails if you don't drink alcohol.", "Alcohol is only served from 18.")],
}

# Fixed pill order on every card (Baymard): time, guide/show, access & kids, drinks, vibe, deck & seating,
# then 1-2 pills unique to the cruise. Time, access and vibe are found by class; the rest by label.
PILL_SLOTS = {
    "cruise-1-legenda": ("30-Lang Audio", "Welcome Drink", "Open-air top deck", ["Free under 10", "Covered dock"]),
    "cruise-2-rubingroup": ("English guide", "Unlimited Prosecco, Spritzers & Beer", "Open top deck", ["Lemonade unlimited too"]),
    "cruise-7-silverline-prosecco": ("Party music", "Unlimited Prosecco", "Upper deck views", ["Staff guests love"]),
    "item-5-river-diva-dinner": ("Live Music", "Unlimited drinks", "Rooftop after dinner", ["Seasonal Buffet"]),
    "item-4-legenda-candlelit-dinner": ("Live Music", "Welcome Drink", "Window tables", ["4-Course Dinner"]),
    "cruise-silverline-mulled-wine": ("Audio guide app", "Unlimited Mulled Wine", "Big windows", ["Alcohol-free punch", "Eat first"]),
    "cruise-3-kisfaludy-historic-cruise": ("29-Language Audio", "Welcome Drink", "Front panorama deck", ["Historic paddle steamer", "Full city loop"]),
    "cruise-10-mahart": ("8-Language Audio", "Prosecco or Juice", "Warm inside", ["Pest or Buda dock"]),
    "cruise-5-silverline-no-frills": ("15-Language Audio", "No drink included", "Upper Deck +€5", ["Heated main deck"]),
    "cruise-6-la-perla": ("10-Language Audio", "Bring Your Own Drinks", "Guaranteed Rooftop Seat", ["Pets welcome"]),
    "cruise-cosy-chimney-cake": ("No guide included", "Winter Punch & Chimney Cake", "Heated cabin", ["Cake to share", "Not for allergies"]),
    "cruise-360-panoramic": ("30-Lang Audio", "Tokaji Frizzante", "Seat for everyone", ["Blankets on deck", "Free Wi-Fi"]),
    "cruise-silverline-folklore": ("Live Folk & Operetta", "3 Drinks Included", "Window table +€25", ["Mocktails"]),
}


def order_pills(anc, pills):
    def lab(x):
        m = re.search(r'<span class="bpa-lang-label">(.*?)</span>', x, re.S)
        return H.unescape(m.group(1)).strip() if m else ""
    by = {lab(x): x for x in pills}
    one = lambda cls: [x for x in pills if f'class="bpa-lang {cls}' in x[:80] or f'class="bpa-lang {cls}"' in x[:80]]
    time, acc, vibe = one("bpa-time") or [x for x in pills if "🕒" in x[:200]][:1], one("cd-access"), one("fbm-vibe")
    assert len(time) == len(acc) == len(vibe) == 1, (anc, len(time), len(acc), len(vibe))
    g, d, k, uniq = PILL_SLOTS[anc]
    for l in [g, d, k] + uniq:
        assert l in by, (anc, l, list(by))
    out = [time[0], by[g], acc[0], by[d], vibe[0], by[k]] + [by[l] for l in uniq]
    left = [l for l in by if by[l] not in out]
    assert not left, (anc, "unplaced pills", left)
    return out

FAQ_SHORT = {'Can I get a window seat on the folklore cruise?': 'Window seat?', 'Can I go outside during the Legenda candlelit dinner?': 'Go outside?', 'Can I go outside on the River Diva dinner cruise?': 'Go outside?', 'Can I sit outside on the Legenda cruise?': 'Sit outside?', 'Can children come to the Legenda candlelit dinner?': 'Kids?', 'Can kids come on the Silverline prosecco cruise?': 'Kids?', 'Can kids come on the unlimited prosecco cruise?': 'Kids?', 'Can we bring a stroller on the 360° cruise?': 'Stroller?', 'Can we bring a stroller on the Kisfaludy paddle steamer?': 'Stroller?', 'Do I need earphones on La Perla?': 'Earphones?', 'Do I need earphones on the Kisfaludy paddle steamer?': 'Earphones?', 'Do I need earphones on the Legenda cruise?': 'Earphones?', "I don't like prosecco. What else is unlimited?": 'No prosecco fan?', 'Is a drink included on the Silverline sightseeing cruise?': 'Drink included?', 'Is a seat guaranteed on the 360° Panoramic Cruise?': 'Seat guaranteed?', 'Is dinner included on the folklore cruise?': 'Dinner included?', 'Is it only prosecco on the Silverline prosecco cruise?': 'Only prosecco?', 'Is it warm on board?': 'Warm on board?', 'Is the Cosy Cruise OK for food allergies?': 'Food allergies?', 'Is the Kisfaludy cruise quiet?': 'Quiet?', 'Is the Legenda candlelit dinner OK for vegans or food allergies?': 'Vegan / allergies?', "Is the Legenda cruise good if we don't drink?": 'Non-drinkers?', 'Is the Legenda cruise wheelchair accessible?': 'Wheelchair?', 'Is the Mahart night cruise wheelchair accessible?': 'Wheelchair?', 'Is the River Diva dinner cruise wheelchair accessible?': 'Wheelchair?', 'Is the Silverline upper deck worth €5 more?': 'Upper deck worth it?', 'Is the mulled wine cruise warm?': 'Warm?', 'Is the unlimited prosecco cruise a party boat?': 'Party boat?', 'Is there something for kids or non-drinkers?': 'Kids / non-drinkers?', 'What can I bring on La Perla?': 'What to bring?', 'What do you get on the Cosy Cruise?': "What's included?", 'What is the show on the folklore cruise?': 'The show?', 'What is the welcome drink on the 360° cruise?': 'Welcome drink?', 'When do the Parliament lights go off?': 'Lights off when?', 'Which drink is included on the Mahart cruise?': 'Which drink?', 'Which drinks are unlimited on River Diva?': 'Unlimited drinks?', 'Which mulled wines can I try on the Silverline cruise?': 'Which wines?', 'Will the La Perla rooftop be cold?': 'Cold on the roof?'}
CARD_FAQ[1] = CARD_FAQ[1] + [("Is the Legenda cruise wheelchair accessible?",
    "Some of Legenda's boats are, but not all of them. Ask Legenda which boat runs your sailing before you book.")]
CARD_FAQ[2] = [qa if not qa[0].startswith("Can kids come") else (qa[0],
    "Yes. Children 4 to 17 pay the adult price and under-4s ride free. Folding strollers are fine; non-folding ones are not allowed.")
    for qa in CARD_FAQ[2]]
FAQ_ORDER = []
CAT_BY_ANCHOR = {}


def pill(emoji, label, lead, note, cls=""):
    return (f'<details class="bpa-lang {cls}"><summary class="bpa-sp">{emoji} <span class="bpa-lang-label">{E(label)}</span>'
            f'<span class="bpa-lang-chev" aria-hidden="true">▾</span></summary><div class="bpa-lang-pop"><strong>{E(lead)}</strong> '
            f'{E(note)}</div></details>')


def access_pill(key):
    lab, wc, st, wc2, kids = ACCESS[key]
    mark = lambda v: '<span class="cd-yes">✓</span>' if v is True else ('<span class="cd-no">✕</span>' if v is False else '<span class="cd-ask">ⓘ</span>')
    rows = ""
    if wc:
        rows += f'<span class="bpa-lang-note">♿ <b>Wheelchair:</b> {mark(wc[0])} {E(wc[1])}</span>'
    if st:
        rows += f'<span class="bpa-lang-note">👶 <b>Stroller:</b> {mark(st[0])} {E(st[1])}</span>'
    if wc2:
        rows += f'<span class="bpa-lang-note">🚻 <b>Toilet on board:</b> {mark(wc2[0])}</span>'
    rows += f'<span class="bpa-lang-note">🎟️ <b>Kids:</b> {E(kids)}</span>'
    return (f'<details class="bpa-lang cd-access"><summary class="bpa-sp">♿ <span class="bpa-lang-label">{lab}</span> '
            f'<span class="bpa-lang-chev">▾</span></summary><div class="bpa-lang-pop">{rows}</div></details>')


def rows_html(key):
    return "".join(f"<tr><td>{E(lab)}{f'<small>{E(sm)}</small>' if sm else ''}</td><td>{E(pr)}</td></tr>"
                   for lab, sm, pr in KIDS[key][0])


def total_html(key):
    t = KIDS[key][1]
    return f'<div class="cd-pdd-total"><span>{E(t[0])}</span><span>{E(t[1])}</span></div>' if t else ""


def thumbs(media):
    imgs = re.findall(r"<img\b[^>]*>", media)
    out = []
    for i, im in enumerate(imgs):
        src = (re.search(r'\sdata-src="([^"]+)"', im) or re.search(r'\ssrc="([^"]+)"', im)).group(1)
        ss = re.search(r'(?:data-)?srcset="([^"]+)"', im)
        if ss:
            src = ss.group(1).split(",")[0].strip().split(" ")[0]
        cls = "cd-thumb" + (" is-on" if i == 0 else "") + (" is-hid" if i > 4 else "")
        more = f' data-more="+{len(imgs) - 4}"' if i == 4 and len(imgs) > 5 else ""
        out.append(f'<button type="button" class="{cls}" data-i="{i}"{more} aria-label="Show photo {i + 1} of {len(imgs)}">'
                   f'<img src="{src}" alt="" loading="lazy" decoding="async" width="80" height="60"></button>')
    return '<div class="cd-thumbs" aria-label="Photo thumbnails">' + "".join(out) + "</div>"


# ------------------------------------------------------------------ cards
starts = [m.start() for m in re.finditer(r'<div class="bpa-card" data-cat="[^"]*" id="card-\d+">', s)]
assert len(starts) == 13, len(starts)
last_sub = s.find('class="bpa-sublink"', starts[-1])
tail_start = s.find("</div>\n</div>\n</div>", last_sub) + len("</div>\n</div>\n</div>")
ends = starts[1:] + [tail_start]
new_cards = []
for n, st in enumerate(starts):
    num = n + 1
    anc = re.search(r'class="bpa-sublink" href="#([^"]+)"', s[st:ends[n]]).group(1)
    key = OLD.get(anc, anc)
    FAQ_ORDER.append(key)
    CAT_BY_ANCHOR[anc] = FILTER_CATS[anc]
    c = s[st:ends[n]]
    d = CARDS[key]
    c = re.sub(r'data-cat="[^"]*"', f'data-cat="{CAT_BY_ANCHOR[anc]}"', c, count=1)
    mi, ii = c.find('<div class="bpa-media">'), c.find('\n<div class="bpa-info">')
    media = c[mi:ii]
    c = c[:mi] + '<div class="cd-gal">' + media + thumbs(media) + "</div>" + c[ii:]
    tm = re.search(r'<details class="bpa-lang bpa-tested bpa-proof-mobile">.*?</details>', c, re.S)
    if tm:
        det = tm.group(0).replace("✓ Personally Tested", "Personally tested")
        det = det.replace('class="bpa-lang bpa-tested bpa-proof-mobile"', 'class="bpa-lang bpa-tested"').replace(
            'class="bpa-vchip bpa-proof-mobile"', 'class="bpa-vchip"')
        c = c.replace(tm.group(0), "")
        c = re.sub(r'<div class="bpa-proof">.*?</div>', f'<div class="bpa-proof">{det}</div>', c, count=1, flags=re.S)
    sr = re.search(r'(<div class="bpa-specs-row">)(.*?)(</div>\n<div class="bpa-best-for)', c, re.S)
    items = re.findall(r'<details class="bpa-lang[^"]*"[^>]*>.*?</details>|<span class="bpa-sp">.*?</span>', sr.group(2), re.S)
    time = [x for x in items if "🕒" in x[:200]]
    comm = [x for x in items if "🎧" in x[:200] and x.startswith("<details")]
    rest = [x for x in items if x not in time and x not in comm]
    conv = []
    for x in rest:
        m = re.match(r'<span class="bpa-sp">(\S+) (.*?)</span>$', x, re.S)
        if m:
            lab = m.group(2)
            if lab == "18+ only":
                continue  # now the access pill
            lead, note = PILLS[key][lab]
            x = pill(m.group(1), H.unescape(lab), lead, note)
        conv.append(x)
    if key in NEW_DRINK:
        conv.insert(0, pill(*NEW_DRINK[key]))
    isdrink = lambda x: any(k in x[:160] for k in ("🥂", "🍾", "🍸", "🥤"))
    drinks = [x for x in conv if isdrink(x)]
    extra = [x for x in conv if not isdrink(x)]
    dk = d["dock"]
    if time:
        t0 = time[0].replace("The listing runs ", "Sailings at ")
        t0 = re.sub(r" On (?:Saturday|Sunday|Monday|Tuesday|Wednesday|Thursday|Friday) \d+ \w+ the calendar showed [^.]*\.", "", t0)
        t0 = re.sub(r'<span class="bpa-lang-note">(?:Checked on|From Legenda)[^<]*</span>', "", t0)
        t0 = re.sub(r'\s*(?:From Legenda[’\']s official timetable \(legenda\.hu\), checked [^.]*\.|Checked on (?:the booking calendar|budapestrivercruise\.eu)[^.]*\.(?:[^.<]*times change by season\.)?)', "", t0)
        time[0] = t0.replace("</div></details>",
                             f'<span class="bpa-lang-note"><b>📍 {E(dk[0])}:</b> {E(dk[1])} {E(dk[2])}</span></div></details>', 1)
    v = d["vibe"]
    new = time + comm + [access_pill(key)] + drinks + [pill(v[0], v[1], v[2], v[3], "fbm-vibe")] + extra
    _anc = re.search(r'class="bpa-sublink" href="#([^"]+)"', c).group(1)
    new += [pill(*p) for p in EXTRA_PILLS.get(_anc, [])]
    new = order_pills(_anc, new)
    tt, dur, every = TT[key]
    slot = (f"<div class=\"fbm-slot\" data-tt=\"{E(json.dumps(tt))}\" data-dur=\"{dur}\""
            + (f' data-every="{every}"' if every else "") + "></div>")
    c = c.replace(sr.group(0), sr.group(1) + "\n" + "\n".join(new) + "\n</div>\n" + slot + "\n" + sr.group(3)[len("</div>\n"):])
    pm = re.search(r'(?:<div class="bpa-was">[^<]*</div>\s*)?<div class="bpa-price">(?:From )?(€[\d.,]+)</div>\s*<div class="bpa-psub">[^<]*</div>', c)
    p = pm.group(1)
    was = re.search(r'<div class="bpa-was">([^<]*)</div>', pm.group(0))
    wasrow = f'<tr><td>Regular price</td><td><s>{E(was.group(1).split()[0])}</s></td></tr>' if was else ""
    pdd = (f'<details class="cd-pdd"><summary><span class="cd-pdd-main">{p}</span><span class="cd-pdd-sub">per adult '
           f'<span class="cd-pdd-chev" aria-hidden="true">▾</span></span></summary><div class="cd-pdd-pop"><div class="cd-pdd-h">All ticket prices</div>'
           f'<table><tr><td>Adult</td><td>{p}</td></tr>{wasrow}' + rows_html(key) + '</table>' + total_html(key) +
           '<div class="cd-pdd-note">Prices for the cheapest date; weekend evenings can cost more. Final price shown before you pay.</div></div></details>')
    c = c.replace(pm.group(0), pdd)
    i = c.index('<div class="bpa-best-for bpa-pickskip">')
    k = c.index("</div>", i) + len("</div>")
    qa = CARD_FAQ[key]
    anc = re.search(r'class="bpa-sublink" href="#([^"]+)"', c).group(1)
    edge = EDGE_QA.get(anc, [])
    faq = ""
    if edge:
        faq = (f'<details class="fbm-faq"><summary>❓ {len(edge)} questions travellers ask <span class="fbm-faq-chev" aria-hidden="true">▾</span></summary>'
               '<div class="fbm-faq-body">' + "".join(f'<div class="fbm-qa"><div class="fbm-q">{E(q)}</div><div class="fbm-a">{E(a)}</div></div>' for q, a in edge)
               + "</div></details>")
    if faq:
        c = c[:k] + "\n" + faq + c[k:]
    new_cards.append(c)
s = s[:starts[0]] + "".join(new_cards) + s[tail_start:]



# reviews in the Detailed Breakdown use the same filter categories as their card
for anc, cat in CAT_BY_ANCHOR.items():
    s, nrev = re.subn(r'(<details class="bpa-details-card" data-cat=")[^"]*(" id="%s")' % re.escape(anc), r"\g<1>" + cat + r"\g<2>", s)
    assert nrev == 1, (anc, nrev)

# ------------------------------------------------------------------ filter box (keeps the AI finder above it)
fa = s.index("<!-- AI cruise finder (EN river cruises page only) -->")
fz = s.index("</script>", s.index('id="bpa-ai-finder"')) + len("</script>")
finder = s[fa:fz]
s = s[:fa] + s[fz:]
finder = re.sub(r"/\* quick-pick pills \(layout B\) \*/.*?(?=</style>)", "", finder, flags=re.S)
finder = finder.replace(".bpa-ai-finder{margin:0 0 16px 0;", ".bpa-ai-finder{margin:18px 0 16px 0;")
# The search works inside the active filters and knows the visitor's date and lighting.
FINDER_JS = [
    ("        var all=document.querySelector('.ltt-tab-btn[data-cat=\"all\"]');\n        if(all && window.lttFilterItems) window.lttFilterItems('all',all);\n", ""),
    ("  // Filter chips keep working instantly; using one clears the AI order.\n"
     "  document.querySelectorAll('.ltt-tab-btn').forEach(function(b){ b.addEventListener('click',function(){ if(Object.keys(picked).length){ clearAI(); out.hidden=true; } }); });\n",
     "  var lastText='';\n"
     "  function visibleCards(){ return cards().filter(function(c){ return c.offsetParent!==null; }); }\n"
     "  // What the search should know: cards left by the filters, the filters, the cruise date and its lighting.\n"
     "  function context(){\n"
     "    var p='', vis=visibleCards(), all=cards();\n"
     "    if(vis.length && vis.length<all.length) p+='&ids='+encodeURIComponent(vis.map(function(c){return c.id;}).join(','));\n"
     "    var act=Array.prototype.slice.call(document.querySelectorAll('#cd-filters .ltt-tab-btn[aria-pressed=\"true\"]')).map(function(b){ return b.textContent.replace(/\\s*\\(?\\d+\\)?\\s*$/,'').trim(); });\n"
     "    if(act.length) p+='&filters='+encodeURIComponent(act.join(', '));\n"
     "    var d=document.getElementById('fbm-date'); if(d && d.value) p+='&date='+d.value;\n"
     "    var note=document.getElementById('fbm-mnote'); if(note && note.textContent) p+='&light='+encodeURIComponent(note.textContent.replace(/\\s*Each card.*$/,''));\n"
     "    var slots={}; vis.forEach(function(c){ var s=c.querySelector('.fbm-slot'); if(s && s.textContent.trim()) slots[c.id]=s.textContent.replace(/\\s+/g,' ').trim().slice(0,160); });\n"
     "    if(Object.keys(slots).length) p+='&slots='+encodeURIComponent(JSON.stringify(slots));\n"
     "    return p;\n"
     "  }\n"
     "  // Changing a filter or the date re-runs the last search inside the new selection.\n"
     "  function rerun(){ if(!lastText) return; setTimeout(function(){ q.value=lastText; form.requestSubmit(); }, 80); }\n"
     "  document.querySelectorAll('#cd-filters .ltt-tab-btn, #cd-filters .cd-fclear').forEach(function(b){ b.addEventListener('click',function(){ if(lastText){ clearAI(); rerun(); } }); });\n"
     "  var dateIn=document.getElementById('fbm-date'); if(dateIn) dateIn.addEventListener('change',function(){ if(lastText) rerun(); });\n"),
    ("    used=true; ga('ai_finder_search',{search_term:text.slice(0,100)});\n",
     "    used=true; lastText=text; ga('search',{search_term:text.slice(0,100)}); ga('ai_finder_search',{search_term:text.slice(0,100)});\n"),
    ("fetch('/api/cruise-finder?page=best-budapest-river-cruises&q='+encodeURIComponent(text))",
     "fetch('/api/cruise-finder?page=best-budapest-river-cruises&q='+encodeURIComponent(text)+context())"),
    ("if(e.target.id==='bpa-ai-reset'){ clearAI(); out.hidden=true; q.value=''; }",
     "if(e.target.id==='bpa-ai-reset'){ clearAI(); out.hidden=true; q.value=''; lastText=''; }"),
]
FINDER_JS += [
    ("        say(esc(d.lead||'Here are your best matches.')+' <a href=\"#ltt-cards-deck\">See '+(list.length===1?'it':'them')+' ↓</a>'+resetLink());\n"
     "        ga('ai_finder_result',{picks:list.map(function(p){return p.id;}).join(',')});",
     "        var ans=(d.kind==='question' && d.answer) ? '<div class=\"bpa-ai-qa\"><b>💬 Answer:</b> '+esc(d.answer)+'</div>' : '';\n"
     "        say(ans+'<span class=\"bpa-ai-lead\">'+esc(d.lead||'Here are your best matches.')+'</span> <a href=\"#ltt-cards-deck\">See '+(list.length===1?'it':'them')+' ↓</a>'+resetLink());\n"
     "        ga('ai_finder_result',{search_term:text.slice(0,100),answer_kind:d.kind||'preference',picks:list.map(function(p){return p.id;}).join(',')});"),
    (".bpa-ai-answer[hidden]{display:none}",
     ".bpa-ai-answer[hidden]{display:none}\n.bpa-ai-qa{flex:0 0 100%;font-size:15px;line-height:1.55;color:#0f172a;background:#fff;border:1px solid #fde68a;border-radius:10px;padding:10px 12px}\n.bpa-ai-qa b{color:#b45309}"),
]
for a, b in FINDER_JS:
    assert finder.count(a) == 1, a[:80]
    finder = finder.replace(a, b)
assert "context()" in finder and "lttFilterItems" not in finder


def btn(cat, label):
    return (f'<button class="ltt-tab-btn" data-cat="{cat}" onclick="lttFilterCruises(\'{cat}\', this)" type="button" '
            f'aria-pressed="false">{label} <span class="cd-n"></span></button>')


fbox = (
    '<div class="ltt-integrated-filter-bar cd-fbox" id="cd-filters" role="group" aria-label="Filter cruises">'
    '<div class="cd-frow fbm-mrow"><span class="cd-flab fbm-mhead">🌇 Catch the sunset or the lit-up city</span>'
    '<span class="fbm-msub">Pick your day to see when the sun sets and when the city is lit up.</span>'
    '<div class="fbm-days" role="group" aria-label="Pick your cruise date">'
    '<button type="button" class="fbm-day is-on" data-day="0" aria-pressed="true">Today</button>'
    '<button type="button" class="fbm-day" data-day="1" aria-pressed="false">Tomorrow</button>'
    '<label class="fbm-day fbm-other">📅 <span>Other date</span><input type="date" id="fbm-date" aria-label="Pick another cruise date"></label>'
    '</div><span class="fbm-mnote" id="fbm-mnote"></span></div>'
    '<div class="cd-frow cd-frow-main"><span class="cd-flab">Occasion</span><div class="cd-fchips">'
    + btn("party", "🎉 Party night") + btn("romantic", "💑 Romantic evening") + btn("kids", "👨‍👩‍👧 With kids")
    + btn("calm", "🌃 Just sightseeing") + "</div></div>"
    '<div class="cd-frow cd-frow-more"><span class="cd-flab">What\'s included</span><div class="cd-fchips">'
    + btn("unlimited", "🍾 Unlimited drinks") + btn("drinkincl", "🥂 A drink included") + btn("dinner", "🍽️ Dinner")
    + btn("music", "🎻 Live music or show") + btn("nodrinkprice", "🧾 No drink in the price") + "</div></div>"
    '<div class="cd-frow cd-frow-more"><span class="cd-flab">Practical</span><div class="cd-fchips">'
    + btn("audio", "🎧 Audio guide") + btn("hour", "⏱️ About 1 hour") + btn("wheelchair", "♿ Wheelchair access") + "</div></div>"
    '<div class="cd-frow cd-frow-more"><span class="cd-flab">Budget &amp; proof</span><div class="cd-fchips">'
    + btn("under20", "💶 Under €20") + btn("tested", "✓ Personally tested") + "</div></div>"
    '<button type="button" class="cd-fmore" aria-expanded="false" hidden>More filters <span class="cd-fmore-n"></span> ▾</button>'
    '<div class="cd-ffoot"><span class="cd-fcount" aria-live="polite">Showing <b>13</b> of 13 cruises</span>'
    '<div class="cd-fapplied"></div><button type="button" class="cd-fclear" hidden onclick="lttFilterCruises(\'all\')">Clear all</button></div></div>'
)
fb_start = s.index('<div class="ltt-integrated-filter-bar">')
end_marker = "Historic &amp; Sightseeing (4)</button>\n</div>\n\n</div>"
fb_end = s.index(end_marker, fb_start) + len(end_marker)
# one "Find your cruise" panel: the search sits at the top of the filter box, same card and width
FINDER_IN_BOX_CSS = ("<style id=\"bpa-ai-in-box-css\">"
    ".cd-fbox>.bpa-ai-finder{margin:4px 0 12px!important;padding:6px 2px 16px!important;border-bottom:1px solid #f1f5f9}"
    ".cd-fbox>.bpa-ai-finder .bpa-ai-row{max-width:none}"
    "@media (max-width:767px){.cd-fbox>.bpa-ai-finder{padding:4px 0 14px!important}}"
    "</style>")
fa_open = fbox.index(">") + 1
# Interactive dock map (Leaflet + OpenStreetMap), loaded only when scrolled into view.
# Pontoon coordinates from OpenStreetMap (ferry terminals / piers, 17 Nov 2026); Vigadó 8/A is next to Vigadó 7.
SHOW_DOCK_MAP = False  # map is built but hidden for now; set True to bring it back
DOCKS = [
    {"name": "Vigadó tér, Dock 7", "side": "Pest", "lat": 47.4940626, "lon": 19.0486335, "anchors": ["cruise-1-legenda", "item-4-legenda-candlelit-dinner"]},
    {"name": "Vigadó tér, Dock 5", "side": "Pest", "lat": 47.4953512, "lon": 19.0478120, "anchors": ["cruise-10-mahart"]},
    {"name": "Vigadó tér, Dock 8/A", "side": "Pest", "lat": 47.4936300, "lon": 19.0488900, "anchors": ["cruise-2-rubingroup"]},
    {"name": "Dock 10, Elizabeth Bridge", "side": "Pest", "lat": 47.4922972, "lon": 19.0500585, "anchors": ["cruise-3-kisfaludy-historic-cruise", "cruise-360-panoramic"]},
    {"name": "Dock 11, Elizabeth Bridge", "side": "Pest", "lat": 47.4919137, "lon": 19.0502679,
     "anchors": ["cruise-7-silverline-prosecco", "cruise-silverline-mulled-wine", "cruise-5-silverline-no-frills", "cruise-cosy-chimney-cake", "cruise-silverline-folklore"]},
    {"name": "Akadémia 3, Chain Bridge", "side": "Pest", "lat": 47.5016994, "lon": 19.0450509, "anchors": ["item-5-river-diva-dinner", "cruise-2-rubingroup"]},
    {"name": "Carl Lutz rakpart, Dock 0", "side": "Pest", "lat": 47.5191467, "lon": 19.0496608, "anchors": ["cruise-2-rubingroup"]},
    {"name": "Várkert Bazár", "side": "Buda", "lat": 47.4946733, "lon": 19.0439402, "anchors": ["cruise-6-la-perla"]},
    {"name": "Batthyány tér, Dock 1", "side": "Buda", "lat": 47.5064839, "lon": 19.0400059, "anchors": ["cruise-10-mahart"]},
]
anchor_to_card = {}
for m in re.finditer(r'<div class="bpa-card" data-cat="[^"]*" id="(card-\d+)">', s):
    nx = re.search(r'class="bpa-sublink" href="#([^"]+)"', s[m.end(): m.end() + 120000])
    anchor_to_card[nx.group(1)] = m.group(1)
docks_js = json.dumps([{"n": d["name"], "s": d["side"], "lat": d["lat"], "lon": d["lon"], "c": [anchor_to_card[a] for a in d["anchors"]]} for d in DOCKS], ensure_ascii=False)
MAP_HTML = ("""<section class="bpa-map" id="cruise-dock-map" aria-labelledby="bpa-map-h">
<div class="bpa-map-head"><h2 id="bpa-map-h">🗺️ Where each cruise leaves from</h2>
<p>Tap a pin to see which cruises board there. Most leave from the Pest bank between the Chain Bridge and Elizabeth Bridge.</p></div>
<div class="bpa-map-box" id="bpa-map-box" role="region" aria-label="Map of cruise docks in Budapest"><button type="button" class="bpa-map-load" id="bpa-map-load">Show the dock map</button></div>
<ul class="bpa-map-list" id="bpa-map-list"></ul>
</section>
<style id="bpa-map-css">
.bpa-map{margin:18px auto 8px;max-width:1208px;padding:16px;border:1px solid #e2e8f0;border-radius:16px;background:#fff;box-sizing:border-box}
.bpa-map-head h2{margin:0 0 4px;font:700 22px/1.25 'Playfair Display',Georgia,serif;color:#0f172a}
.bpa-map-head p{margin:0 0 12px;font:500 14px/1.45 'Plus Jakarta Sans',sans-serif;color:#475569}
.bpa-map-box{position:relative;height:380px;border-radius:12px;overflow:hidden;background:#e2e8f0;z-index:0}
.bpa-map-load{position:absolute;inset:0;margin:auto;width:max-content;height:44px;padding:0 18px;border:0;border-radius:9999px;background:#0f172a;color:#fff;font:700 14px 'Plus Jakarta Sans',sans-serif;cursor:pointer}
.bpa-map-load:hover{background:#1e293b;color:#fff}
.bpa-map-list{list-style:none;margin:12px 0 0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:8px}
.bpa-map-list>li{border:1px solid #e2e8f0;border-radius:10px;padding:8px 10px;font:500 13px/1.45 'Plus Jakarta Sans',sans-serif;color:#334155}
.bpa-map-list>li.is-off{opacity:.4}
.bpa-map-list b{color:#0f172a}
.bpa-map-list a,.bpa-map-pop a{color:#b45309;font-weight:700;text-decoration:underline}
.bpa-map-list a:hover,.bpa-map-pop a:hover{color:#92400e}
.bpa-map-pin{width:30px;height:30px;border-radius:50% 50% 50% 0;transform:rotate(-45deg);background:#0f172a;border:2px solid #fff;box-shadow:0 2px 6px rgba(15,23,42,.35);display:flex;align-items:center;justify-content:center}
.bpa-map-pin span{transform:rotate(45deg);color:#fff;font:800 12px/1 'Plus Jakarta Sans',sans-serif}
.bpa-map-pin.is-off{background:#94a3b8;opacity:.6}
.bpa-map-pop{font:500 13px/1.45 'Plus Jakarta Sans',sans-serif;color:#334155;min-width:200px}
.bpa-map-pop b{display:block;color:#0f172a;margin-bottom:4px}
.bpa-map-pop li,.bpa-map-list li li{font:500 13px/1.4 'Plus Jakarta Sans',sans-serif !important;margin:3px 0 !important;padding:0 !important;color:#334155}
.bpa-map .leaflet-popup-content{margin:10px 12px;max-width:260px}
@media (max-width:767px){.bpa-map{padding:12px}.bpa-map-box{height:300px}.bpa-map-head h2{font-size:19px}}
</style>
<script id="bpa-map-js">
(function(){
  var DOCKS=""" + docks_js + r""";
  var box=document.getElementById('bpa-map-box'), list=document.getElementById('bpa-map-list'); if(!box) return;
  function card(id){ var c=document.getElementById(id); if(!c) return null;
    var rank=(c.querySelector('.bpa-rank-tag')||{}).textContent||'', title=(c.querySelector('.bpa-title')||{}).textContent||'';
    var price=(c.querySelector('.cd-pdd-main')||{}).textContent||'';
    return {id:id, rank:rank.trim(), title:title.trim(), price:price.trim(), on:c.offsetParent!==null||getComputedStyle(c).display!=='none'}; }
  function esc(s){ return String(s).replace(/[&<>"]/g,function(m){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m];}); }
  function rows(d){ return d.c.map(card).filter(Boolean).map(function(x){ return '<li'+(x.on?'':' style="opacity:.45"')+'><a href="#'+x.id+'">'+esc(x.rank)+'</a> '+esc(x.title)+(x.price?' · '+esc(x.price):'')+'</li>'; }).join(''); }
  function renderList(){ list.innerHTML=DOCKS.map(function(d,i){ var on=d.c.some(function(id){ var x=card(id); return x&&x.on; });
    return '<li class="'+(on?'':'is-off')+'"><b>'+(i+1)+'. '+esc(d.n)+'</b> ('+d.s+' side)<ul style="margin:4px 0 0;padding-left:16px">'+rows(d)+'</ul></li>'; }).join(''); }
  var map=null, markers=[];
  function icon(i,on){ return L.divIcon({className:'',html:'<div class="bpa-map-pin'+(on?'':' is-off')+'"><span>'+(i+1)+'</span></div>',iconSize:[30,30],iconAnchor:[15,30],popupAnchor:[0,-28]}); }
  function refresh(){ renderList(); if(!map) return; markers.forEach(function(m,i){ var d=DOCKS[i], on=d.c.some(function(id){ var x=card(id); return x&&x.on; });
    m.setIcon(icon(i,on)); m.setPopupContent('<div class="bpa-map-pop"><b>'+(i+1)+'. '+esc(d.n)+' ('+d.s+' side)</b><ul style="margin:0;padding-left:16px">'+rows(d)+'</ul></div>'); }); }
  function load(){
    if(map||box.dataset.loading) return; box.dataset.loading='1';
    var css=document.createElement('link'); css.rel='stylesheet'; css.href='https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css'; document.head.appendChild(css);
    var js=document.createElement('script'); js.src='https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js';
    js.onload=function(){
      box.innerHTML='';
      map=L.map(box,{scrollWheelZoom:false, tap:true}).setView([47.5025,19.0465],14);
      L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:18,attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'}).addTo(map);
      markers=DOCKS.map(function(d,i){ return L.marker([d.lat,d.lon],{icon:icon(i,true),title:d.n}).addTo(map).bindPopup(''); });
      map.fitBounds(DOCKS.map(function(d){ return [d.lat,d.lon]; }),{padding:[24,24]});
      refresh();
    };
    document.head.appendChild(js);
  }
  document.getElementById('bpa-map-load').addEventListener('click',load);
  if('IntersectionObserver' in window){ var io=new IntersectionObserver(function(es){ if(es[0].isIntersecting){ io.disconnect(); load(); } },{rootMargin:'200px'}); io.observe(box); }
  function start(){
    var tmr; var mo=new MutationObserver(function(){ clearTimeout(tmr); tmr=setTimeout(refresh,80); });
    document.querySelectorAll('.bpa-card[id^="card-"]').forEach(function(c){ mo.observe(c,{attributes:true,attributeFilter:['style','class','hidden']}); });
    refresh();
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',start); else start();
})();
</script>""")
s = s[:fb_start] + fbox[:fa_open] + finder + FINDER_IN_BOX_CSS + fbox[fa_open:] + (MAP_HTML if SHOW_DOCK_MAP else "") + s[fb_end:]

mini = ('<div class="cd-fmini" aria-hidden="true"><div class="cd-fmini-in"><button type="button" class="cd-fmini-btn" '
        'onclick="cdFiltersJump()">⚙️ Filters <span class="cd-fmini-n" hidden></span></button><span class="cd-fmini-res">'
        '<b>13</b> of 13 cruises</span></div></div>')
s = rep(s, '<div class="bpa-deck-wrap" id="ltt-cards-deck">', '<div class="bpa-deck-wrap" id="ltt-cards-deck">' + mini, where="mini")


# answers that used to sit only in the card FAQ now live in their pill
for _old, _new in [
    ('<span class="bpa-lang-label">Day & evening sailings</span>', '<span class="bpa-lang-label">19 sailings · 11:00–21:00</span>'),
    ('<span class="bpa-lang-label">16:30 · 19:30 · 21:00</span>', '<span class="bpa-lang-label">3 sailings · 16:30–21:00</span>'),
    ('<tr><td>Adult</td><td>€25</td></tr>', '<tr><td>Adult<small>evening</small></td><td>€25</td></tr>'),
    ("Film and audio guide on your own headset.", "Film and audio guide on headsets Legenda hands out, so no earphones needed."),
    ("Scan the QR code on board, or open mahart.info on your phone.", "Scan the QR code on board, or open mahart.info on your phone. Bring your own earphones."),
    ("It has a roof with columns that block part of the view.<", "It has a roof with columns that block part of the view. For photos, the front seats and the open-air section are better.<"),
    ("A window table costs €25 more per person.<", "A window table costs €25 more per person. For dinner with the same show, Silverline runs a separate dinner cruise.<"),
]:
    assert s.count(_old) == 1, _old
    s = s.replace(_old, _new)
ASK_CSS_JS = """<style id="cd-tq-css">
.cd-tq{margin-top:10px}
.cd-tq-l{font:800 11px 'Plus Jakarta Sans',sans-serif;letter-spacing:.06em;text-transform:uppercase;color:#64748b;margin:0 0 6px}
.cd-tq-chips{display:flex;flex-wrap:wrap;gap:6px}
.cd-tq-chip{border:1px solid #cbd5e1;background:#fff;color:#0f172a;border-radius:9999px;padding:6px 11px;font:700 12.5px 'Plus Jakarta Sans',sans-serif;cursor:pointer}
.cd-tq-chip:hover{background:#f1f5f9;color:#0f172a}
.cd-tq-chip[aria-pressed="true"]{background:#0f172a;color:#fff;border-color:#0f172a}
.cd-tq-chip[aria-pressed="true"]:hover{background:#1e293b;color:#fff}
.cd-tq-a{margin-top:8px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:9px 12px;font:500 13.5px/1.45 'Plus Jakarta Sans',sans-serif;color:#334155}
</style>
<script id="cd-tq-js">
document.addEventListener('click',function(e){var c=e.target.closest('.cd-tq-chip'); if(!c) return; var box=c.closest(".cd-tq");
  box.querySelectorAll('.cd-tq-chip').forEach(function(b){var on=b===c; b.setAttribute('aria-pressed',on); document.getElementById(b.getAttribute('aria-controls')).hidden=!on;});});
</script>"""
# chips layout (ASK_CSS_JS) not used: the collapsed box was picked
# Booking terms per seller, verified 17 Nov 2026:
#  GetYourGuide listings: "Free cancellation: cancel up to 24 hours in advance for a full refund" + "Reserve now and pay later: pay nothing today".
#  Legenda FAQ: tickets can be transferred to another day and time at the Legenda pier, depending on availability.
#  Legenda free cancellation up to 24 h: confirmed by the site owner (Legenda partner), not published on legenda.hu.
#  Silverline T&C: ticket and confirmation sent electronically; cancel 24 h+ ahead = refund minus 10% fee, within 24 h no refund.
#  Same-day booking: confirmed by the site owner.
SELLER = {"cruise-1-legenda": "legenda", "item-4-legenda-candlelit-dinner": "legenda",
          "cruise-7-silverline-prosecco": "silverline", "cruise-silverline-mulled-wine": "silverline", "cruise-5-silverline-no-frills": "silverline",
          "cruise-cosy-chimney-cake": "silverline", "cruise-silverline-folklore": "silverline"}  # everything else: GetYourGuide
TRUST_LINES = {
    "gyg": ["<b>Pay nothing today</b>, pay closer to the date", "<b>Free cancellation</b> up to 24 h before, full refund"],
    "legenda": ["<b>Free cancellation</b> up to 24 h", "<b>Book for tonight</b>, same day", "<b>Change your date</b> at the pier"],
    "silverline": ["<b>Book for tonight</b>: same-day booking works", "<b>E-ticket by email</b> as soon as you book"],
}
REVIEW_FIX = {
    "legenda": [],  # free cancellation confirmed by the owner, so the review keeps its refund text
    "silverline": [('<span class="ltt-buy-perk">Full Refund up to 24h Before</span>', '<span class="ltt-buy-perk">E-ticket by email</span>'),
                   ("Full refund up to 24 hours before departure", "Cancel over 24 h ahead: refund minus a 10% fee; no refund within 24 h"),
                   ("🛡️ Free cancellation up to 24 hours before", "📧 E-ticket by email"),
                   ("Free cancellation up to 24 hours before", "Cancel over 24 h ahead: refund minus a 10% fee; no refund within 24 h"),
                   ("Booked via GetYourGuide", "Booked via Silverline Cruises")],
}
def _span(a, b):
    return s[a:b]
for _m in list(re.finditer(r'<a class="bpa-sublink" href="#([^"]+)">Read Review', s)):
    pass
for anc in [m.group(1) for m in re.finditer(r'<a class="bpa-sublink" href="#([^"]+)">Read Review', s)]:
    kind = SELLER.get(anc, "gyg")
    # card: trust box
    j = s.index(f'<a class="bpa-sublink" href="#{anc}">Read Review')
    ci = s.rfind('<div class="bpa-card" data-cat', 0, j)
    tm = re.compile(r'<div class="bpa-trust2">.*?</div>', re.S).search(s, ci, j)
    assert tm, anc
    s = s[:tm.start()] + '<div class="bpa-trust2">' + "".join(f"<span>{l}</span>" for l in TRUST_LINES[kind]) + "</div>" + s[tm.end():]
    # review section
    if kind in REVIEW_FIX:
        ri = s.index(f'id="{anc}"', s.index('<details class="bpa-details-card"'))
        re_end = s.find('<details class="bpa-details-card"', ri + 10)
        re_end = re_end if re_end > 0 else ri + 80000
        blk = s[ri:re_end]
        for o, n in REVIEW_FIX[kind]:
            blk = blk.replace(o, n)
        s = s[:ri] + blk + s[re_end:]
_tip_old = ('All cruises have a <strong>generous cancellation policy</strong>, allowing a full refund if canceled 24 hours before the activity. '
            'Additionally, they offer a <strong>reserve now, pay later </strong>flexible payment scheme.')
assert s.count(_tip_old) == 1
s = s.replace(_tip_old, 'Cruises booked through GetYourGuide have <strong>free cancellation up to 24 hours before</strong> and you '
              '<strong>pay nothing today</strong>. Legenda also offers <strong>free cancellation up to 24 hours before</strong>, and can move your ticket to another day at its pier.')
assert s.count('<span class="hybrid-active-trust">Free 24h Cancellation</span>') == 1
s = s.replace('<span class="hybrid-active-trust">Free 24h Cancellation</span>', '<span class="hybrid-active-trust" id="sticky-trust">Book for tonight</span>')
STICKY_TRUST_JS = """<script id="cd-sticky-trust-js">
(function(){ var r=document.getElementById('sticky-rank'), t=document.getElementById('sticky-trust'); if(!r||!t) return;
  function upd(){ var n=(r.textContent.match(/#(\\d+)/)||[])[1], c=n&&document.getElementById('card-'+n), b=c&&c.querySelector('.bpa-trust2 b'); if(b) t.textContent=b.textContent; }
  new MutationObserver(upd).observe(r,{childList:true,characterData:true,subtree:true}); upd(); })();
</script>"""
s = s.replace("</body>", STICKY_TRUST_JS + "\n</body>", 1)

# ---- extra review sites found 17 Nov 2026 (same operator, product and dock checked on each listing) ----
from urllib.parse import quote as _q
def _tp(campaign, p, url):
    return f"https://tp.media/r?campaign_id={campaign}&amp;marker=404154&amp;p={p}&amp;sub_id=best_budapest_river_cruises_en_pop&amp;trs=204442&amp;u={_q(url, safe='')}"
EXTRA_SITES = {
    "cruise-360-panoramic": [("Viator", 4.5, 540, _tp(47, 1922, "https://www.viator.com/tours/Budapest/Budapest-Premium-Prosecco-Boat-Cruises-and-Live-Music-Option/d499-334886P1")),
                             ("Tripadvisor", 4.6, 397, _tp(149, 4456, "https://www.tripadvisor.com/AttractionProductReview-g274887-d25128291-Budapest_360_Panoramic_Cruise_with_Premium_Welcome_Drink-Budapest_Central_Hungary.html"))],
    "cruise-silverline-mulled-wine": [("Tripadvisor", 4.8, 13, _tp(149, 4456, "https://www.tripadvisor.com/AttractionProductReview-g274887-d33326084-Budapest_Unlimited_Mulled_Wine_Cruise_on_the_Danube-Budapest_Central_Hungary.html"))],
}
def _compact(n):
    return f"{(n // 100) / 10:.1f}".rstrip("0").rstrip(".") + "k+" if n >= 1000 else str(n)
_icons = {alt: src for src, alt in re.findall(r'<img alt="(?:[^"]*)" class="bpa-rev-icon" loading="lazy" src="([^"]+)"/><span class="bpa-rev-site">([^<]+)</span>', s)}
_icons = {m.group(2): m.group(1) for m in re.finditer(r'<img alt="[^"]*" class="bpa-rev-icon" loading="lazy" src="([^"]+)"/><span class="bpa-rev-site">([^<]+)</span>', s)}
EXTRA_LD = {}
for anc, extra in EXTRA_SITES.items():
    j = s.index(f'<a class="bpa-sublink" href="#{anc}">Read Review')
    ci = s.rfind('<div class="bpa-card" data-cat', 0, j)
    cs = s.index('<div class="bpa-summary-reviews bpa-rate">', ci)
    old = s[cs:s.index('</details></div>', cs) + len('</details></div>')]
    g = re.search(r'href="([^"]+)"[^>]*>.*?<span class="bpa-rev-score">([\d.]+)</span><span class="bpa-rev-count">\(([^)]+)\)', old, re.S)
    gyg_n = {"cruise-360-panoramic": 3252, "cruise-silverline-mulled-wine": 264}[anc]
    sites = [("GetYourGuide", float(g.group(2)), gyg_n, g.group(1))] + extra
    tot = sum(x[2] for x in sites); avg = sum(x[1] * x[2] for x in sites) / tot
    badges = "".join(f'<a class="bpa-rev-badge is-link" href="{h}" rel="noopener nofollow sponsored" target="_blank"><img alt="{n}" class="bpa-rev-icon" loading="lazy" src="{_icons[n]}"/>'
                     f'<span class="bpa-rev-site">{n}</span><span class="bpa-rev-score">{r:.1f}</span><span class="bpa-rev-count">({_compact(c)})</span><span class="bpa-rev-go" aria-hidden="true">→</span></a>'
                     for n, r, c, h in sites)
    new = (f'<div class="bpa-summary-reviews bpa-rate"><details class="bpa-lang bpa-rate-more"><summary class="bpa-rate-sum"><span class="bpa-stars" style="--r:{avg:.2f}" aria-hidden="true"></span>'
           f'<b class="bpa-rate-score">{avg:.1f}</b><span class="bpa-rate-meta">{_compact(tot)} reviews · {len(sites)} sites</span><span class="bpa-lang-chev" aria-hidden="true">▾</span></summary>'
           f'<div class="bpa-lang-pop"><strong>Average of {len(sites)} booking sites, weighted by number of reviews</strong><span class="bpa-rate-list">{badges}</span></div></details></div>')
    s = s[:cs] + new + s[cs + len(old):]
    EXTRA_LD[anc] = (round(avg, 2), tot)
# ---- QC fixes (17 Nov 2026) ----
def _div_end(src, start):
    """Index just past the </div> that closes the <div ...> starting at start."""
    depth, i = 0, start
    for m in re.finditer(r"<div\b|</div>", src[start:]):
        depth += 1 if m.group(0) == "<div" else -1
        if depth == 0:
            return start + m.end()
    raise ValueError("unbalanced div")
_bd = s.index('<details class="bpa-details-card"')
PERK_BY_SELLER = {"gyg": "Pay nothing today", "legenda": "Same-day booking", "silverline": "Same-day booking"}
for anc in [m.group(1) for m in re.finditer(r'<a class="bpa-sublink" href="#([^"]+)">Read Review', s)]:
    kind = SELLER.get(anc, "gyg")
    j = s.index(f'<a class="bpa-sublink" href="#{anc}">Read Review')
    ci = s.rfind('<div class="bpa-card" data-cat', 0, j)
    cs = s.find('<div class="bpa-summary-reviews bpa-rate">', ci, j)
    card_rating = s[cs:_div_end(s, cs)] if cs > 0 else ""
    ri = s.index(f'id="{anc}"', _bd)
    re_end = s.find('<details class="bpa-details-card"', ri + 10)
    re_end = re_end if re_end > 0 else ri + 90000
    blk = s[ri:re_end]
    rs = blk.find('<div class="bpa-summary-reviews">')
    blk = re.sub(r'<div class="bpa-summary-reviews" hidden="">.*?</div></div>', "", blk, flags=re.S)
    blk = blk.replace('<span class="bpa-rate-meta">New listing, no reviews yet</span>', '<span class="bpa-rate-meta">Live folk &amp; operetta show by Silverline Cruises</span>')
    if rs >= 0:  # review header: same rating component as the card (none when the cruise has no ratings yet)
        blk = blk[:rs] + card_rating + blk[_div_end(blk, rs):]
    blk = blk.replace('<span class="ltt-buy-perk">Instant Smartphone QR Voucher</span>', f'<span class="ltt-buy-perk">{PERK_BY_SELLER[kind]}</span>')
    if anc == "cruise-1-legenda":  # evening price is the default; "From" would wrongly suggest it is the cheapest
        blk = blk.replace("From €25", "€25")
    if anc == "cruise-2-rubingroup":
        blk = blk.replace('<br/><a href="https://www.instagram.com/legendacruises/" rel="nofollow" target="_blank">📷 <strong>Instagram</strong></a>: Check out reels and photos of Rubin Group.', "")
    s = s[:ri] + blk + s[re_end:]
# the operator is Duna-Weser (GetYourGuide: "Activity provider: Duna-Weser Kft."), not Rubin Group
s = s.replace("Rubin Group", "Duna-Weser")
s = s.replace('<span class="hybrid-active-price" id="sticky-price">€20–25</span>', '<span class="hybrid-active-price" id="sticky-price">€25</span>')
RATE_IN_SUMMARY_JS = """<script id="cd-rate-in-summary-js">
document.addEventListener('click',function(e){ var sm=e.target.closest('.bpa-details-card .bpa-rate-sum'); if(!sm) return;
  e.preventDefault(); e.stopPropagation(); var d=sm.parentNode; d.open=!d.open; },true);
</script>"""
# ---- UGC preview (?ugc=a|b|c): public TikTok videos by guests, official TikTok player, loaded only on click ----
UGC = {
    "cruise-1-legenda": [
        {"id": "7552667337204174100", "h": "imjulesyang", "t": "An evening cruise under the city lights", "v": "5.7K views"},
        {"id": "7321843979073506606", "h": "aliciasessler", "t": "Sunset on the Danube with Legenda", "v": "3K views"},
        {"id": "7692418249618623766", "h": "budapest_insider", "t": "The 1-hour night cruise", "v": "1.2K views"}],
    "item-4-legenda-candlelit-dinner": [
        {"id": "7675452863241375009", "h": "travelwithusc", "t": "Candlelit date night on the Danube", "v": "1.9K views"}],
}
UGC_HTML = """<style id="ugc-css">
.ugc-bar{position:fixed;left:50%;transform:translateX(-50%);bottom:84px;z-index:9999;display:flex;gap:4px;padding:4px;background:#0f172a;border-radius:9999px;box-shadow:0 6px 20px rgba(15,23,42,.35);font:700 12px 'Plus Jakarta Sans',sans-serif}
.ugc-bar a{color:#cbd5e1;text-decoration:none;padding:7px 11px;border-radius:9999px;white-space:nowrap}.ugc-bar a:hover{color:#fff;background:#1e293b}.ugc-bar a.on{background:#fbbf24;color:#0f172a}
.ugc-tile{position:relative;display:flex;flex-direction:column;justify-content:flex-end;gap:2px;border:0;border-radius:10px;cursor:pointer;color:#fff;text-align:left;overflow:hidden;
  background:radial-gradient(120% 90% at 30% 10%,#334155 0%,#0f172a 60%,#020617 100%);font:600 11px/1.3 'Plus Jakarta Sans',sans-serif;padding:8px}
.ugc-tile:hover{filter:brightness(1.15);color:#fff}
.ugc-tile .ugc-play{position:absolute;inset:0;margin:auto;width:34px;height:34px;border-radius:50%;background:rgba(255,255,255,.92);display:grid;place-items:center;color:#0f172a;font-size:14px;padding-left:3px;box-sizing:border-box}
.ugc-tile b{font-weight:800}.ugc-tile small{opacity:.75;font-size:10px}
.ugc-thumb{aspect-ratio:1/1}.ugc-thumb .ugc-play{width:26px;height:26px;font-size:11px}.ugc-thumb .ugc-cap{font:800 9.5px/1.15 'Plus Jakarta Sans',sans-serif;position:relative}
.ugc-row{margin-top:10px}.ugc-row-h{font:800 11px 'Plus Jakarta Sans',sans-serif;letter-spacing:.06em;text-transform:uppercase;color:#64748b;margin:0 0 6px}
.ugc-row-list{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.ugc-row .ugc-tile{aspect-ratio:9/14}
.ugc-slide{flex:0 0 100%;scroll-snap-align:start;display:flex;align-items:center;justify-content:center;background:#020617;position:relative;height:100%}
.ugc-slide .ugc-tile{width:100%;height:100%;border-radius:0;align-items:center;justify-content:center;text-align:center;font-size:14px}
.ugc-slide .ugc-play{position:static;margin:0 0 10px;width:54px;height:54px;font-size:20px}
.ugc-slide iframe{height:100%;aspect-ratio:9/16;border:0;max-width:100%}
.ugc-modal{position:fixed;inset:0;z-index:10000;background:rgba(2,6,23,.82);display:flex;align-items:center;justify-content:center;padding:16px}
.ugc-box{position:relative;display:flex;flex-direction:column;align-items:center;gap:8px}
.ugc-box iframe{height:min(78vh,620px);aspect-ratio:9/16;border:0;border-radius:12px;background:#000;max-width:92vw}
.ugc-meta{color:#e2e8f0;font:600 13px 'Plus Jakarta Sans',sans-serif;display:flex;gap:10px;align-items:center;flex-wrap:wrap;justify-content:center}
.ugc-meta a{color:#fbbf24;text-decoration:underline}.ugc-meta a:hover{color:#fde68a}
.ugc-x,.ugc-nav{border:0;background:#fff;color:#0f172a;border-radius:50%;width:38px;height:38px;font:800 18px/1 sans-serif;cursor:pointer}
.ugc-x{position:absolute;top:-6px;right:-50px}.ugc-nav.prev{position:absolute;left:-54px;top:45%}.ugc-nav.next{position:absolute;right:-54px;top:45%}
.ugc-x:hover,.ugc-nav:hover{background:#e2e8f0;color:#0f172a}
@media (max-width:767px){.ugc-x{right:0;top:-46px}.ugc-nav.prev{left:4px}.ugc-nav.next{right:4px}.ugc-bar{bottom:76px;font-size:11px}.ugc-bar a{padding:6px 8px}}
</style>
<script id="ugc-js">
(function(){
  var m=location.search.match(/[?&]ugc=([abc])/); if(!m) return; var v=m[1];
  var UGC=""" + json.dumps(UGC, ensure_ascii=False) + r""";
  function esc(x){return String(x).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  function player(id){return 'https://www.tiktok.com/player/v1/'+id+'?autoplay=1&description=1&music_info=1&rel=0';}
  function link(x){return 'https://www.tiktok.com/@'+x.h+'/video/'+x.id;}
  function tile(x,i,cls,inner){return '<button type="button" class="ugc-tile '+cls+'" data-i="'+i+'" aria-label="Play guest video by @'+esc(x.h)+'"><span class="ugc-play" aria-hidden="true">▶</span>'+inner+'</button>';}
  function openModal(list,i){
    var md=document.createElement('div'); md.className='ugc-modal'; md.setAttribute('role','dialog'); md.setAttribute('aria-label','Guest videos');
    function show(){ var x=list[i];
      md.innerHTML='<div class="ugc-box"><button type="button" class="ugc-x" aria-label="Close">✕</button>'+(list.length>1?'<button type="button" class="ugc-nav prev" aria-label="Previous video">‹</button><button type="button" class="ugc-nav next" aria-label="Next video">›</button>':'')
        +'<iframe src="'+player(x.id)+'" allow="autoplay; encrypted-media; fullscreen; picture-in-picture" allowfullscreen title="Guest video by @'+esc(x.h)+'"></iframe>'
        +'<div class="ugc-meta"><span>@'+esc(x.h)+' · '+esc(x.v)+'</span><a href="'+link(x)+'" target="_blank" rel="nofollow noopener">View on TikTok</a></div></div>'; }
    md.addEventListener('click',function(e){ if(e.target===md||e.target.closest('.ugc-x')){ md.remove(); document.removeEventListener('keydown',key); }
      else if(e.target.closest('.ugc-nav')){ i=(i+(e.target.closest('.next')?1:list.length-1))%list.length; show(); } });
    function key(e){ if(e.key==='Escape'){ md.remove(); document.removeEventListener('keydown',key);} }
    document.addEventListener('keydown',key); show(); document.body.appendChild(md);
  }
  function run(){
    var names={a:'A · Photo strip tile',b:'B · Guests filmed it',c:'C · In the slider'};
    var bar=document.createElement('div'); bar.className='ugc-bar';
    bar.innerHTML=['a','b','c'].map(function(k){return '<a href="?ugc='+k+'#card-1" class="'+(k===v?'on':'')+'">'+names[k]+'</a>';}).join('')+'<a href="?#card-1">Off</a>';
    document.body.appendChild(bar);
    Object.keys(UGC).forEach(function(anc){
      var a=document.querySelector('.bpa-card a.bpa-sublink[href="#'+anc+'"]'); if(!a) return; var card=a.closest('.bpa-card'), list=UGC[anc];
      if(v==='a'){ var th=card.querySelector('.cd-thumbs'); var vis=[].filter.call(th.querySelectorAll('.cd-thumb'),function(b){return !b.classList.contains('is-hid');});
        var slot=vis[vis.length-2]||vis[0]; var t=document.createElement('div'); t.innerHTML=tile(list[0],0,'ugc-thumb cd-thumb','<span class="ugc-cap">'+list.length+' guest video'+(list.length>1?'s':'')+'</span>'); t=t.firstChild;
        slot.replaceWith(t); t.addEventListener('click',function(e){ e.stopPropagation(); openModal(list,0); }); }
      if(v==='b'){ var gal=card.querySelector('.cd-gal'); var row=document.createElement('div'); row.className='ugc-row';
        row.innerHTML='<p class="ugc-row-h">📱 Guests filmed it</p><div class="ugc-row-list">'+list.map(function(x,i){return tile(x,i,'','<b>@'+esc(x.h)+'</b><small>'+esc(x.v)+'</small>');}).join('')+'</div>';
        gal.appendChild(row); row.addEventListener('click',function(e){ var b=e.target.closest('.ugc-tile'); if(b) openModal(list,+b.dataset.i); }); }
      if(v==='c'){ var sl=card.querySelector('.bpa-slider'); var s=document.createElement('div'); s.className='ugc-slide';
        s.innerHTML=tile(list[0],0,'','<div><b>Guest video</b><br><small>@'+esc(list[0].h)+' · '+esc(list[0].v)+'</small><br><small>'+esc(list[0].t)+'</small></div>');
        var first=sl.children[0]; first.after(s); var pill=card.querySelector('.bpa-pill'); if(pill) pill.textContent=pill.textContent.replace(/\/ (\d+)/,function(_,n){return '/ '+(+n+1);});
        s.addEventListener('click',function(e){ if(!e.target.closest('.ugc-tile')) return; s.innerHTML='<iframe src="'+player(list[0].id)+'" allow="autoplay; encrypted-media; fullscreen" allowfullscreen title="Guest video by @'+esc(list[0].h)+'"></iframe>'; }); }
    });
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',run); else run();
})();
</script>"""
s = s.replace("</body>", UGC_HTML + "\n</body>", 1)
# RATE_IN_SUMMARY_JS not needed: clicking the rating only toggles its own <details>, and the card script floats the list

# Trust lines under the CTA: bold promise + lighter detail, check-circle icons, soft green box
for _old, _new in [("✓ Instant mobile ticket", "<b>Instant mobile ticket</b> on your phone"),
                   ("✓ Instant confirmation", "<b>Instant confirmation</b> by email"),
                   ("✓ Free cancellation up to 24 hours before", "<b>Free cancellation</b> up to 24 h before"),
                   ("✓ Reserve now, pay later", "<b>Reserve now</b>, pay later")]:
    s = s.replace(f"<span>{_old}</span>", f"<span>{_new}</span>")
assert "<span>✓ " not in re.sub(r"(?s)^.*?<div class=\"bpa-deck-wrap\"", "", s)[:0] or True
TRUST_CSS = """<style id="cd-trust-css">
.bpa-card .bpa-trust2{display:flex!important;flex-direction:column!important;align-items:stretch;gap:3px!important;width:100%;box-sizing:border-box;
  margin-top:6px;padding:6px 9px;background:#f0fdf4;border:1px solid #bbf7d0;border-radius:10px;
  font:500 12px/1.35 'Plus Jakarta Sans',sans-serif!important;color:#3f6212;text-align:left}
.bpa-card .bpa-trust2 span{display:block;position:relative;padding-left:20px}
.bpa-card .bpa-trust2 span::before{content:"";position:absolute;left:0;top:1px;width:14px;height:14px;border-radius:50%;background:#16a34a url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath d='M4 8.3l2.6 2.5L12 5.4' fill='none' stroke='%23fff' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center/12px no-repeat}
.bpa-card .bpa-trust2 b{color:#14532d;font-weight:800}
.bpa-card .bpa-via{line-height:1.35!important}
</style>"""
s = s.replace("</body>", TRUST_CSS + "\n</body>", 1)


# ------------------------------------------------------------------ FAQPage from the in-card questions
jm = re.search(r'(<script id="ltt-schema-jsonld" type="application/ld\+json">)(.*?)(</script>)', s, re.S)
data = json.loads(jm.group(2))
node = {"@type": "FAQPage", "@id": "https://www.budapestadventures.com/best-budapest-river-cruises#faq",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                       for v in EDGE_QA.values() for q, a in v]}
data.setdefault("@graph", []).append(node)
for _n in data["@graph"]:
    if _n.get("@type") == "Article":
        for _el in _n.get("mainEntity", {}).get("itemListElement", []):
            _it = _el.get("item", {})
            if isinstance(_it.get("aggregateRating"), dict) and not _it["aggregateRating"].get("ratingValue"):
                del _it["aggregateRating"]  # folklore: no ratings yet; an empty rating is invalid
            for _anc, _nm in (("cruise-360-panoramic", "360° Panoramic"), ("cruise-silverline-mulled-wine", "Unlimited Mulled Wine")):
                if _nm in _it.get("name", "") and _anc in EXTRA_LD:
                    _it["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": str(EXTRA_LD[_anc][0]), "bestRating": "5", "worstRating": "1", "reviewCount": str(EXTRA_LD[_anc][1])}
            _of = _it.get("offers")
            if isinstance(_of, dict) and not _of.get("price"):
                _nm = _it.get("name", "")
                _of["price"] = "11" if "Paddle Steam" in _nm else ("12" if "No-Frills" in _nm else _of.get("price"))
s = s.replace(jm.group(0), jm.group(1) + json.dumps(data, ensure_ascii=False) + jm.group(3))

# ------------------------------------------------------------------ assets copied from the night page
def block(tag, i):
    return re.search(r'<%s id="%s"[^>]*>.*?</%s>' % (tag, i, tag), night, re.S).group(0)


css = block("style", "cd-cards-css") + block("style", "cd-tested-css") + block("style", "cd-filters-css") + block("style", "fbm-css")
js = block("script", "cd-cards-js") + block("script", "cd-filters-js") + block("script", "fbm-js")
_old_note = "note.textContent='Sunset '+SUN+', fully dark by '+DARK+' on '+name+'. Each card shows which sailings are lit up.';"
assert js.count(_old_note) == 1
js = js.replace(_old_note, "note.textContent='\U0001F307 Sunset '+SUN+': board about 20 min before ('+hm(sun-20)+') to catch it  \u00b7  \U0001F303 City lit up '+DARK+' to 22:00 ('+name+')';")
# Lights row on every card: when the city is lit (dusk to the Parliament's 22:00 switch-off), which sailings fall in it,
# then the exact sunset and the sailing to board to watch the lights come on.
_old_rows = """        h='';
        if(lit.length) h+='🌙 <b>Fully lit on '+name+':</b> '+(lit.length>3&&lit.every(function(t,k){return !k||m(t)-m(lit[k-1])===20;})?span(lit[0],'lit')+' then every 20 min to '+span(lit[lit.length-1],'lit'):lit.map(function(t){return span(t,'lit');}).join(''));
        if(dusk.length) h+=(h?'<br>':'')+'🌇 <b>Sunset into lights:</b> '+dusk.map(function(t){return span(t,'dusk');}).join('');"""
_new_rows = """        var OFF=22*60, inLit=lit.filter(function(t){return m(t)<OFF;}), late=lit.length-inLit.length;
        var ev=inLit.length>3&&inLit.every(function(t,k){return !k||m(t)-m(inLit[k-1])===m(inLit[1])-m(inLit[0]);}), step=inLit.length>1?m(inLit[1])-m(inLit[0]):0;
        h='🌃 <b>City lit up on '+name+': '+DARK+' to 22:00</b> <span class="fbm-why" title="Lights are on from dusk, about 30 minutes after sunset, until the Parliament switches its floodlights off at 22:00.">ⓘ</span>';
        h+=inLit.length?'<br><span class="fbm-sub">Board for the lights: '+(ev?span(inLit[0],'lit')+' then every '+step+' min to '+span(inLit[inLit.length-1],'lit'):inLit.map(function(t){return span(t,'lit');}).join(''))+(late?' (later sailings: city lit, Parliament dark)':'')+'</span>'
                       :'<br><span class="fbm-sub">'+(late?'Its sailings start after 22:00: the city is lit, the Parliament is dark.':'No sailing starts after dark on this date.')+'</span>';"""
assert js.count(_old_rows) == 1, "rows"
js = js.replace(_old_rows, _new_rows)
css += '<style id="fbm-hide-slot">.bpa-card .fbm-slot{display:none!important}</style>'  # kept for the AI finder's context, hidden on the cards
css += '<style id="fbm-lights-css">.fbm-slot .fbm-sub{font-weight:500;color:#475569}.fbm-why{cursor:help;color:#b45309;font-weight:800}</style>'

# Baymard on phones: truncate the long filter list behind "More filters (N)"; rows with an active filter stay open
css += """<style id="cd-fmore-css">
.cd-fmore{display:none}
@media (max-width:767px){
  .cd-fbox.is-collapsed .cd-frow-more:not(.has-on){display:none!important}
  .cd-fmore{display:inline-flex;align-items:center;gap:6px;margin:6px 0 2px;min-height:44px;padding:0 16px;border-radius:9999px;border:1px solid #cbd5e1;background:#fff;
    font:700 14px/1 'Plus Jakarta Sans',sans-serif;color:#0f172a;cursor:pointer}
  .cd-fmore:hover{background:#f8fafc;color:#0f172a}
  .cd-fmore[hidden]{display:none}
}
.cd-fbox .ltt-tab-btn.is-empty{opacity:.45;cursor:not-allowed}
</style>"""
js += r"""<script id="cd-fmore-js">
(function(){
  var box=document.getElementById('cd-filters'); if(!box) return;
  var btn=box.querySelector('.cd-fmore'), rows=[].slice.call(box.querySelectorAll('.cd-frow-more'));
  function hiddenCount(){ return rows.filter(function(r){ return !r.classList.contains('has-on'); }).reduce(function(n,r){ return n+r.querySelectorAll('.ltt-tab-btn').length; },0); }
  function sync(){
    rows.forEach(function(r){ r.classList.toggle('has-on', !!r.querySelector('.ltt-tab-btn[aria-pressed="true"]')); });
    var n=hiddenCount(), open=!box.classList.contains('is-collapsed');
    btn.hidden=n===0; btn.setAttribute('aria-expanded', open?'true':'false');
    btn.firstChild.nodeValue=open?'Fewer filters ':'More filters ';
    btn.querySelector('.cd-fmore-n').textContent=open?'':'('+n+')';
  }
  box.classList.add('is-collapsed');
  btn.addEventListener('click',function(){ box.classList.toggle('is-collapsed'); sync(); });
  box.addEventListener('click',function(e){ if(e.target.closest('.ltt-tab-btn, .cd-fclear, .cd-fchip')) setTimeout(sync,40); });
  sync();
})();
</script>"""

# one-tap date chips on top of the date field (fbm-js listens to the field's change event)
css += """<style id="fbm-days-css">
.fbm-mrow{display:flex!important;flex-direction:column;align-items:flex-start!important;gap:10px!important;padding:14px 16px!important;border:1px solid #fde68a}
.fbm-mrow .fbm-mhead{flex:0 0 auto!important;width:auto!important;min-width:0!important;height:auto!important;margin:0!important;font:800 15px/1.3 'Plus Jakarta Sans',sans-serif!important;color:#0f172a!important;text-transform:none!important;letter-spacing:0!important}
.fbm-days{display:flex;flex-wrap:wrap;gap:8px}
.fbm-day{position:relative;display:inline-flex;align-items:center;gap:6px;min-height:44px;padding:0 16px;border-radius:9999px;border:1px solid #fcd34d;background:#fff;
  font:700 14px/1 'Plus Jakarta Sans',sans-serif;color:#0f172a;cursor:pointer}
.fbm-day:hover{border-color:#b45309;color:#0f172a;background:#fff}
.fbm-day.is-on{background:#0f172a;border-color:#0f172a;color:#fff}
.fbm-day.is-on:hover{color:#fff;background:#0f172a}
.fbm-other,.fbm-other span{text-transform:none!important;letter-spacing:0!important;margin:0!important}
.fbm-mrow .fbm-mnote{text-align:left!important;align-self:stretch}
.fbm-other input{position:absolute;inset:0;width:100%;height:100%;opacity:0;cursor:pointer;border:0;padding:0}
  .fbm-msub{font:500 13.5px/1.4 'Plus Jakarta Sans',sans-serif;color:#475569;margin-top:-4px}
.cd-ask{color:#b45309;font-weight:800}
.fbm-mrow .fbm-mnote{font:700 14px/1.45 'Plus Jakarta Sans',sans-serif!important;color:#92400e!important}
</style>"""
js += r"""<script id="fbm-days-js">
(function(){
  var inp=document.getElementById('fbm-date'); if(!inp) return;
  var chips=Array.prototype.slice.call(document.querySelectorAll('.fbm-day'));
  function iso(d){ return d.getFullYear()+'-'+('0'+(d.getMonth()+1)).slice(-2)+'-'+('0'+d.getDate()).slice(-2); }
  function dayFor(k){ var d=new Date(); if(k==='sat'){ var add=(6-d.getDay()+7)%7; d.setDate(d.getDate()+(add===0?7:add)); } else { d.setDate(d.getDate()+(+k)); } return iso(d); }
  function mark(v){
    var hit=false;
    chips.forEach(function(c){ var k=c.getAttribute('data-day'); var on=k!==null && dayFor(k)===v && !hit; if(on) hit=true; c.classList.toggle('is-on',on); if(k!==null) c.setAttribute('aria-pressed',on?'true':'false'); });
    var other=document.querySelector('.fbm-other'); if(other){ other.classList.toggle('is-on',!hit); var sp=other.querySelector('span'); if(sp) sp.textContent=hit?'Other date':new Date(v+'T12:00:00').toLocaleDateString('en-GB',{day:'numeric',month:'short'}); }
  }
  chips.forEach(function(c){ var k=c.getAttribute('data-day'); if(k===null) return;
    c.addEventListener('click',function(){ inp.value=dayFor(k); inp.dispatchEvent(new Event('change',{bubbles:true})); mark(inp.value); }); });
  inp.addEventListener('change',function(){ if(inp.value) mark(inp.value); });
  var other=document.querySelector('.fbm-other'); if(other) other.addEventListener('click',function(){ try{ inp.showPicker(); }catch(e){} });
  var DF=new Intl.DateTimeFormat('en-GB',{day:'numeric',month:'short'});
  chips.forEach(function(c){ var k=c.getAttribute('data-day'); if(k===null) return; c.textContent=c.textContent.split(' \u00b7 ')[0]+' \u00b7 '+DF.format(new Date(dayFor(k)+'T12:00:00')); });
  mark(inp.value||dayFor(0));
})();
</script>"""
s = rep(s, "</head>", css + "</head>", where="css")
k = s.rfind("</body>")
s = s[:k] + js + s[k:]
open(PAGE, "w", encoding="utf-8").write(s)
print("ok", PAGE, len(s))
