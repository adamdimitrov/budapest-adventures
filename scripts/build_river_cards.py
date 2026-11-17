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
    1: ([("Student", "with ID", "€18"), ("Child", "10-14", "€14"), ("Under 10", "", "Free"), ("Evening cruise", "adult", "€25")],
        ("2 adults + 2 kids (10-14), daytime", "€68")),
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
FAQ_ORDER = []
CAT_BY_ANCHOR = {}


def pill(emoji, label, lead, note, cls=""):
    return (f'<details class="bpa-lang {cls}"><summary class="bpa-sp">{emoji} <span class="bpa-lang-label">{E(label)}</span>'
            f'<span class="bpa-lang-chev" aria-hidden="true">▾</span></summary><div class="bpa-lang-pop"><strong>{E(lead)}</strong> '
            f'{E(note)}</div></details>')


def access_pill(key):
    lab, wc, st, wc2, kids = ACCESS[key]
    mark = lambda v: '<span class="cd-yes">✓</span>' if v else '<span class="cd-no">✕</span>'
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
    CAT_BY_ANCHOR[anc] = CARDS[key]["cat"]
    c = s[st:ends[n]]
    d = CARDS[key]
    c = re.sub(r'data-cat="[^"]*"', f'data-cat="{d["cat"]}"', c, count=1)
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
    faq = (f'<details class="fbm-faq"><summary>❓ {len(qa)} questions travellers ask <span class="fbm-faq-chev" aria-hidden="true">▾</span></summary>'
           f'<div class="fbm-faq-body">' + "".join(f'<div class="fbm-qa"><div class="fbm-q">{E(q)}</div><div class="fbm-a">{E(a)}</div></div>' for q, a in qa)
           + "</div></details>")
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
     "    used=true; lastText=text; ga('ai_finder_search',{search_term:text.slice(0,100)});\n"),
    ("fetch('/api/cruise-finder?page=best-budapest-river-cruises&q='+encodeURIComponent(text))",
     "fetch('/api/cruise-finder?page=best-budapest-river-cruises&q='+encodeURIComponent(text)+context())"),
    ("if(e.target.id==='bpa-ai-reset'){ clearAI(); out.hidden=true; q.value=''; }",
     "if(e.target.id==='bpa-ai-reset'){ clearAI(); out.hidden=true; q.value=''; lastText=''; }"),
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
    '<div class="cd-frow fbm-mrow"><span class="cd-flab fbm-mhead">🌇 When are you cruising?</span>'
    '<div class="fbm-days" role="group" aria-label="Pick your cruise date">'
    '<button type="button" class="fbm-day is-on" data-day="0" aria-pressed="true">Tonight</button>'
    '<button type="button" class="fbm-day" data-day="1" aria-pressed="false">Tomorrow</button>'
    '<button type="button" class="fbm-day" data-day="sat" aria-pressed="false">Saturday</button>'
    '<label class="fbm-day fbm-other">📅 <span>Other date</span><input type="date" id="fbm-date" aria-label="Pick another cruise date"></label>'
    '</div><span class="fbm-mnote" id="fbm-mnote"></span></div>'
    '<div class="cd-frow"><span class="cd-flab">Who is coming</span><div class="cd-fchips">'
    + btn("nodrink", "🥤 Good if you don't drink") + btn("party", "🎉 Party crowd") + "</div></div>"
    '<div class="cd-frow"><span class="cd-flab">The trip</span><div class="cd-fchips">'
    + btn("calm", "🌃 Just views, no party, no dinner") + btn("historic", "🏛️ Sightseeing commentary") + btn("dinner", "🍽️ Dinner")
    + btn("unlimited", "🍾 Unlimited drinks") + btn("opendeck", "☀️ Open-air deck") + btn("heated", "🔥 Heated indoor")
    + btn("hour", "⏱️ About 1 hour") + "</div></div>"
    '<div class="cd-frow"><span class="cd-flab">Budget &amp; proof</span><div class="cd-fchips">'
    + btn("tested", "✓ Personally tested") + btn("under20", "💶 Under €20") + "</div></div>"
    '<div class="cd-ffoot"><span class="cd-fcount" aria-live="polite">Showing <b>13</b> of 13 cruises</span>'
    '<div class="cd-fapplied"></div><button type="button" class="cd-fclear" hidden onclick="lttFilterCruises(\'all\')">Clear all</button></div></div>'
)
fb_start = s.index('<div class="ltt-integrated-filter-bar">')
end_marker = "Historic &amp; Sightseeing (4)</button>\n</div>\n\n</div>"
fb_end = s.index(end_marker, fb_start) + len(end_marker)
s = s[:fb_start] + finder + "\n" + fbox + s[fb_end:]

mini = ('<div class="cd-fmini" aria-hidden="true"><div class="cd-fmini-in"><button type="button" class="cd-fmini-btn" '
        'onclick="cdFiltersJump()">⚙️ Filters <span class="cd-fmini-n" hidden></span></button><span class="cd-fmini-res">'
        '<b>13</b> of 13 cruises</span></div></div>')
s = rep(s, '<div class="bpa-deck-wrap" id="ltt-cards-deck">', '<div class="bpa-deck-wrap" id="ltt-cards-deck">' + mini, where="mini")

# ------------------------------------------------------------------ FAQPage from the in-card questions
jm = re.search(r'(<script id="ltt-schema-jsonld" type="application/ld\+json">)(.*?)(</script>)', s, re.S)
data = json.loads(jm.group(2))
node = {"@type": "FAQPage", "@id": "https://www.budapestadventures.com/best-budapest-river-cruises#faq",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                       for n in FAQ_ORDER for q, a in CARD_FAQ[n]]}
data.setdefault("@graph", []).append(node)
s = s.replace(jm.group(0), jm.group(1) + json.dumps(data, ensure_ascii=False) + jm.group(3))

# ------------------------------------------------------------------ assets copied from the night page
def block(tag, i):
    return re.search(r'<%s id="%s"[^>]*>.*?</%s>' % (tag, i, tag), night, re.S).group(0)


css = block("style", "cd-cards-css") + block("style", "cd-tested-css") + block("style", "cd-filters-css") + block("style", "fbm-css")
js = block("script", "cd-cards-js") + block("script", "cd-filters-js") + block("script", "fbm-js")
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
  mark(inp.value||dayFor(0));
})();
</script>"""
s = rep(s, "</head>", css + "</head>", where="css")
k = s.rfind("</body>")
s = s[:k] + js + s[k:]
open(PAGE, "w", encoding="utf-8").write(s)
print("ok", PAGE, len(s))
