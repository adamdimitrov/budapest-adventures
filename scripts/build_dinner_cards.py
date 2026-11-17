#!/usr/bin/env python3
"""Rebuild the EN dinner cruises page (best-dinner-cruises-budapest.html) with the river-page card system.

Repeatable from scratch: it always starts from the page as committed at BASE (the last hand-built
version) and takes the shared card/filter/finder CSS and JS from the river page at the same commit,
so running it twice gives the same output. Never hand-edit the output; change the data below and rerun:

    python3 scripts/build_dinner_cards.py && python3 scripts/sync_layout.py

What it ports from the river page (scripts/build_river_cards.py):
- AI cruise finder ("Cruise finder") inside the filter box, page=best-dinner-cruises-budapest
- Baymard filter box: Occasion / What's included / Practical / Budget & proof, live counts,
  "More filters (N)" on phones; review sections get the same data-cat as their card
- date row: sunset, "City lit up <dusk> to 22:00", board about 20 min before sunset
- cards: thumbnails, fixed pill order (asserted), every pill a dropdown, "5 questions travellers ask",
  price dropdown with all ticket prices, verified booking box per seller, sticky trust follows the card
- review headers use the card's rating component; FAQPage built from the card questions

Facts were checked on 17 November 2026 on each seller's own page: legenda.hu (via the river page data),
budapestrivercruise.eu (Dinner & Lights, Folk & Operetta), silver-line.hu/faq, GetYourGuide t1593, t408084, t401526,
t494832 and t54081. Guest-review themes: api/_knowledge/best-dinner-cruises-budapest.json.
"""
import html as H
import json
import re
import subprocess
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "1ffa87fd6"  # last hand-built dinner page + finished river page
PAGE = "best-dinner-cruises-budapest.html"
URL = "https://www.budapestadventures.com/best-dinner-cruises-budapest"
E = H.escape


def git_show(path):
    return subprocess.run(["git", "show", f"{BASE}:{path}"], cwd=ROOT, check=True, capture_output=True, text=True).stdout


s = git_show(PAGE)
river = git_show("best-budapest-river-cruises.html")
assert s.count("€44") >= 5
s = s.replace("€44", "€40")  # goulash cruise: €40 on the listing (was €44, shown struck through in the price dropdown)


def rep(text, old, new, count=1, where=""):
    n = text.count(old)
    if n != count:
        raise SystemExit(f"[{where}] expected {count}x, found {n}x: {old[:100]!r}")
    return text.replace(old, new)


L, S, HK, SE, RD, G = ("cruise-1-legenda", "cruise-2-silverline-no-show", "cruise-5-hungaria-koncert",
                       "cruise-6-eurama", "cruise-7-unlimited-drinks", "cruise-8-goulash-langos")
# Legenda #1 and goulash last (owner's wish); Legenda and Silverline earn more, so they rank high but interleaved.
ORDER = [L, HK, S, SE, RD, G]
RANK = {L: ("bpa-gold", "🏆 #{n} Best Overall &amp; Most Romantic"), HK: ("bpa-silver", "🥈 #{n} Best Folk Show"),
        S: ("bpa-bronze", "🥉 #{n} Best Show Choice")}
SHORT = {L: "Legenda Candlelit Dinner Cruise", HK: "Hungária Koncert Dinner & Folk Show", S: "Silverline 4-Course Dinner Cruise",
         SE: "4-Course Dinner Cruise With Live Folk Music", RD: "River Diva Buffet Dinner Cruise", G: "Goulash & Lángos Cruise"}
SELLER = {L: "legenda", S: "silverline"}  # everything else books on GetYourGuide

# ------------------------------------------------------------------ timetables (for the date row / AI context)


def nd(nov, dec=None):
    return [{"from": "11-01", "to": "11-30", "times": nov}, {"from": "12-01", "to": "12-31", "times": dec or nov}]


TT = {
    L: ([{"from": "04-20", "to": "08-23", "times": ["19:45"]}, {"from": "08-24", "to": "04-19", "times": ["19:00"]}], 150),
    HK: (nd(["19:00"]), 90),
    S: (nd(["19:00"]), 120),
    SE: (nd(["19:30"]), 120),
    RD: (nd(["19:30"], ["18:30"]), 150),
    G: (nd(["19:00"]), 90),
}

# ------------------------------------------------------------------ pills
# Fixed order on every card: 🕒 time · 🎧 guide or show · ♿ access & kids · 🥂 drinks · 🙂 vibe · 🌬️ deck & seating,
# then 1-2 pills unique to the cruise. Each entry: (kind, emoji, label, lead, note).
DOCK = {
    L: ("Vigadó tér, Dock 7", "Pest side, 2 minutes from Vörösmarty tér and the top of Váci utca. Legenda's covered dock has restrooms, so you can wait out of the rain."),
    HK: ("Akadémia 2", "Pest side, the second dock from the Chain Bridge towards Parliament. Look for the Gróf Széchenyi or Stadt Wien."),
    S: ("Dock 11, Elizabeth Bridge", "Jane Haining rakpart on the Pest side, next to Elizabeth Bridge. The boat sails south to Lágymányosi Bridge, then north to Margaret Bridge."),
    SE: ("Seesight Dock 6", "Pest embankment near Vigadó tér. A queue can form before boarding, so come early."),
    RD: ("Akadémia 3", "Pest side by the Chain Bridge. Bring a passport or ID card with your QR voucher."),
    G: ("Akadémia 2", "Pest side, the second dock from the Chain Bridge towards Parliament, on the historic Gróf Széchenyi."),
}
PILLS = {
    L: [("time", "🕒", "19:00 · 2.5 h", "Daily at 19:00 from late August to mid-April, 19:45 in summer.", "2.5 hours on board."),
        ("show", "🎶", "Pianist & singer", "A pianist and singer play lounge music all evening.", "Quiet enough to talk: no loud folk show."),
        ("access",),
        ("drinks", "🥂", "Welcome drink", "1 drink included: champagne, wine, beer, a soft drink or mineral water.", "Every other drink is paid on board."),
        ("vibe", "🕯️", "Romantic and quiet", "Candlelit tables for two along the windows, a pianist and singer, no loud folk show.",
         "10 of 70 recent guests booked it for a birthday, anniversary or engagement."),
        ("deck", "🌬️", "Open top deck", "The open top deck is free to use at any point of the evening.",
         "Seats can't be reserved, not even a window table: Legenda assigns the tables on board."),
        ("menu", "🍽️", "4 courses, 17 dishes", "Chosen at your table: 6 starters, 2 soups, 6 mains (trout, pork, duck, beef, cauliflower steak or tuna) and 3 desserts.",
         "Children 3 to 12 get 3 courses."),
        ("diet", "🌱", "Diet notes", "Gluten-free and lactose-free dishes are marked on the menu.", "No vegan menu, and it can't cater for food allergies.")],
    HK: [("time", "🕒", "19:00 · 1.5 h", "Departs at 19:00, back after 90 minutes.", "Arrive at least 15 minutes early."),
         ("show", "💃", "Rajkó folk show", "Musicians of the Rajkó Folk Orchestra play with a cimbalom, and folk dancers perform in costume.",
          "Guests say the band plays requests at the tables and the dancers come round for photos."),
         ("access",),
         ("drinks", "🥂", "Welcome drink", "1 welcome drink included.", "Other drinks are paid on board; a couple of guests suggest bringing change for tips."),
         ("vibe", "🎉", "Lively folk evening", "A show night more than a sightseeing cruise: dinner, live Rajkó music and costumed dancers.",
          "34 of 61 recent guests mention the dancers, 34 the music."),
         ("deck", "🌬️", "Deck for the views", "Guests say you can step out on deck to watch the lit-up city quietly.",
          "Guests who arrived 30 minutes early got a window table without booking one."),
         ("menu", "🍽️", "3 set menus", "Served at your table: dips to start, then Urban Classic (goulash soup, pork tenderloin), Paprika Mood (chicken paprikash) or Veggie Flow (vegetable soup, pasta marinara), and Somlói sponge cake.",
          "Some past dates served a buffet instead: 6 of 61 recent guests mention one."),
         ("ship", "🚢", "Historic ship", "An evening cruise on a historic ship, the Gróf Széchenyi or Stadt Wien.", "One guest calls it a well-kept vintage boat.")],
    S: [("time", "🕒", "19:00 · 2 h", "Departs at 19:00, timed to start around sunset; 2 hours.",
         "Boarding opens 45 minutes before; arrive at least 30 minutes early."),
        ("show", "🎭", "3 show options", "Dinner & Lights (no show, background music) from €77, or the Folk & Operetta Show with singers and folk dancers from €91.",
         "Same boat, same 4-course menu. Silverline also lists a Live Piano Show."),
        ("access",),
        ("drinks", "🥂", "Welcome drink", "1 welcome drink included: Prosecco on Dinner & Lights, champagne on the folk show.",
         "Other drinks are paid on board, and you can't bring your own. 2 of 31 recent guests wish more were included."),
        ("vibe", "🕯️", "Calm, sunset start", "A quiet dinner with background music on Dinner & Lights, timed to start around sunset.",
         "18 of 31 recent guests praise the staff, many naming their waiter."),
        ("deck", "🪟", "Window seat +€15", "A window seat costs €15 more per person on Dinner & Lights, €25 on the Folk & Operetta show.",
         "Choose it when you book; one guest said the window table was worth it."),
        ("menu", "🍽️", "4-course menu", "Panzanella with pear and burrata, then a choice of 2 soups, 4 mains (walnut cod, pork tenderloin, curry lamb chops or a vegetarian sweet potato boat) and 3 desserts.",
         "Same menu on every option."),
        ("diet", "🌱", "Veg, GF & LF", "A vegetarian main is on the menu, and most dishes are made with gluten-free and/or lactose-free ingredients.",
         "No allergen-free kitchen; tell Silverline about special diets in advance.")],
    SE: [("time", "🕒", "19:30 · 2 h", "Departs at 19:30; about 2 hours.", "One guest found a long queue at boarding, so come early."),
         ("show", "🎻", "Folk music & dance", "Live music by the Hungarian Ökrös Band and a live folklore performance.",
          "Guests call it lively but not too loud to talk."),
         ("access",),
         ("drinks", "🥂", "Welcome Prosecco", "A welcome glass of Prosecco.", "Extra drinks are bought on board; you can't bring your own."),
         ("vibe", "🙂", "Warm folk evening", "A 4-course dinner with live folk music and dancers, pitched as a romantic evening.",
          "39 of 52 recent guests talk about the food, most of them positively."),
         ("deck", "🌬️", "Step out on deck", "Guests say you can go out on deck for photos at any point.", "Inside stays warm on a cold November night."),
         ("menu", "🍽️", "4 menus to pick", "Table service, 4 courses: Roast Duck (duck liver pâté, goulash soup, roast duck leg, strudel), Veal Stew, Poultry (chicken paprika) or Vegetarian (grilled goat's cheese, Gundel pancake).",
          "Kids' menus are listed on some dates.")],
    RD: [("time", "🕒", "19:30 · 2.5 h", "Departs at 19:30 in November, 18:30 in December; about 2.5 hours.",
          "Arrive 20 to 30 minutes early with your QR voucher and ID."),
         ("show", "🎶", "Live music", "Live music in the Grand Salon all evening; guests mention violin and saxophone.",
          "No sightseeing commentary, just an English-speaking host."),
         ("access",),
         ("drinks", "🍸", "Unlimited drinks", "Included all evening: cocktails, spirits, Prosecco, wine, beer, soft drinks and water, served to your table.",
          "25 of 64 recent guests mention the unlimited drinks."),
         ("vibe", "🎻", "All-inclusive evening", "A seasonal buffet, unlimited drinks and live music, so nothing to pay on board.",
          "Guests say it works even in pouring rain."),
         ("deck", "🌬️", "Rooftop after dinner", "After dinner the rooftop deck opens, weather permitting.", "Tables and window seats can't be guaranteed."),
         ("menu", "🍽️", "Seasonal buffet", "Buffet stations by Executive Chef Viktor Moldován: starters, mains, sides, vegetarian dishes and desserts.",
          "The winter menu (26 Nov to 25 Dec 2026) includes bean goulash, duck breast, venison ragout and pike-perch."),
         ("diet", "🌱", "Diet notes", "Vegetarian buffet options, and vegan dishes are marked on the menu.",
          "Tell the operator about gluten-free or other needs in advance.")],
    G: [("time", "🕒", "19:00 sharp · 1.5 h", "Departs exactly at 19:00; boarding from 18:30.", "90 minutes on the Danube."),
        ("show", "🎻", "Live Rajkó music", "Live entertainment by the Rajkó Folk Ensemble.", "2 of 30 recent guests saw only the musicians and no dancers."),
        ("access",),
        ("drinks", "🥂", "Prosecco or juice", "1 welcome drink: Prosecco or juice.", "Other drinks are paid on board."),
        ("vibe", "🙂", "Casual supper", "A light Hungarian supper with live folk music, not a full dinner.",
         "21 of 30 recent guests talk about the food, nearly all positively."),
        ("deck", "🪑", "Assigned seats", "Seats are assigned, so there is no rush to board.", "One guest was seated in a smaller dining room downstairs."),
        ("menu", "🥣", "Goulash and/or lángos", "Three options from €40: a bowl of goulash soup, a crispy lángos, or both, served at your table.",
         "A vegetarian soup substitute is available, and the lángos is vegetarian.")],
}
KINDS_FIXED = ["time", "show", "access", "drinks", "vibe", "deck"]

# label, wheelchair, stroller/infant note, kids
ACCESS = {
    L: ("No wheelchair access", (False, "not wheelchair accessible"), "€84 for ages 3-12 (3 courses); not for children under 3"),
    HK: ("Kids 6 and under free", (None, "not stated on the listing: ask the operator before you book"),
         "free for 6 and under (add them to the booking); child (7-12), student (13-25) and senior (66+) tickets"),
    S: ("No wheelchair access", (False, "no wheelchair access"), "infant tickets don't include dinner (order on board); alcohol only from 18; service dogs only"),
    SE: ("No wheelchair access", (False, "not suitable for wheelchair users; no electric or non-folding wheelchairs"),
         "under 3 free if not eating (tell the operator so they can set a seat)"),
    RD: ("Wheelchair OK", (True, "wheelchair-accessible boat"), "free under 4, full price for 4-17"),
    G: ("No wheelchair access", (False, "not suitable for wheelchair users"), "child prices shown when you pick a date"),
}

# price shown by default (evening / dinner price), sub label, dropdown rows, family total
PRICE = {
    L: ("€110", "per adult", [("Child", "3-12, 3 courses", "€84"), ("Under 3", "", "Not allowed")], ("2 adults + 2 kids (3-12)", "€388")),
    HK: ("€67", "per adult", [("Regular price", "", "<s>€79</s>"), ("Age 6 and under", "add to the booking", "Free"),
                              ("Child 7-12, student, senior", "", "At checkout")], None),
    S: ("€77", "per adult", [("Folk &amp; Operetta Show", "same menu", "€91"), ("Window seat", "Dinner &amp; Lights", "+€15"),
                             ("Window seat", "Folk &amp; Operetta", "+€25")], None),
    SE: ("€66", "per adult", [("Under 3", "not eating", "Free")], None),
    RD: ("€99", "per adult", [("Child", "4-17", "€99"), ("Under 4", "", "Free")], ("2 adults + 2 kids (4-17)", "€396")),
    G: ("€40", "per person", [("Regular price", "", "<s>€44</s>"), ("Goulash, lángos or both", "", "Same price")], None),
}

# "5 questions travellers ask": my tests, the pills and recent guest reviews (api/_knowledge/best-dinner-cruises-budapest.json)
EDGE_QA = {
    L: [("Good for a special occasion?", "Yes: 10 of 70 recent guests booked it for a birthday, anniversary or engagement."),
        ("Is the food good?", "55 of 70 recent guests talk about the food, nearly all positively. I chose from 17 dishes on my test dinner."),
        ("Is it loud?", "No. A pianist and singer play lounge music, quiet enough to talk. There is no loud folk show."),
        ("Can I reserve a window table?", "No. Legenda doesn't take seat or table requests, whatever you book: tables are assigned on board."),
        ("Can I cancel or change the date?", "Booked direct with Legenda, cancellation is free up to 72 hours before. Legenda can also move your ticket to another day at its pier, if seats are free.")],
    HK: [("Is the food good?", "44 of 61 recent guests talk about the food, almost all positively. 2 found it lukewarm or a bit dry."),
         ("Show or sightseeing?", "A show night. The band plays requests at the tables and the dancers come round for photos; you can step out on deck to watch the city."),
         ("Set menu or buffet?", "The listing shows three set menus served at your table. 6 of 61 recent guests had a buffet on their date."),
         ("Can kids come?", "Yes. Children 6 and under go free but must be added to the booking. Families say kids got to dance with the dancers."),
         ("How early should I arrive?", "At least 15 minutes. Guests who came 30 minutes early got a window table without booking one.")],
    S: [("Which option should I book?", "Dinner &amp; Lights (€77) for a quiet dinner and the views, or the Folk &amp; Operetta Show (€91) for singers and folk dancers. Same boat, same menu."),
        ("Are drinks included?", "Only the welcome drink. 2 of 31 recent guests wish more were included at this price."),
        ("Is the window seat worth it?", "It costs €15 extra on Dinner &amp; Lights. One recent guest said the window table was worth the money."),
        ("Can I cancel or change the date?", "Yes, free up to 24 hours before departure when you book direct with Silverline. Within 24 hours there is no refund."),
        ("When should I arrive?", "Boarding opens 45 minutes before the 19:00 departure. Arrive at least 30 minutes early.")],
    SE: [("Is the food good?", "39 of 52 recent guests talk about the food, mostly positively; a few call it fine rather than special."),
         ("Can I go outside?", "Yes. Guests say you can step out on deck for photos of the lit-up Parliament at any point."),
         ("Is the music loud?", "No. Guests call the folk music and dancing lively but not too loud to talk."),
         ("Is there a vegetarian menu?", "Yes, one of the four menus is vegetarian: grilled goat's cheese, then a Gundel pancake to finish."),
         ("What about boarding?", "One guest found a long queue at Dock 6, so come early.")],
    RD: [("Is the food good?", "53 of 64 recent guests talk about the food, almost all positively. One said it could have been hotter."),
         ("What if it rains?", "Guests say it works even in pouring rain: dinner and music are indoors."),
         ("Is there live music?", "Yes, violin and saxophone in the Grand Salon. 21 of 64 recent guests mention it."),
         ("Is there sightseeing commentary?", "No. An English-speaking host runs the evening, but there is no commentary."),
         ("What should I bring?", "A passport or ID card along with your QR voucher.")],
    G: [("Is it a full dinner?", "No, a light supper: a bowl of goulash, a lángos, or both, with a welcome drink."),
        ("Is there a dance show?", "Not always. The Rajkó Folk Ensemble plays; 2 of 30 recent guests saw only the musicians."),
        ("Vegetarian?", "Yes. There is a vegetarian soup substitute, and the lángos is vegetarian."),
        ("When should I arrive?", "Boarding opens at 18:30 and the boat leaves at exactly 19:00. Seats are assigned."),
        ("Is it good value?", "It is the cheapest way to eat on the Danube here, from €40 with live music and a drink.")],
}

# Fact-checked filter tags (17 Nov 2026)
#  romantic: candlelit or pitched as romantic by the seller | folk: live Hungarian folk music | kids: a free or child fare confirmed
#  served: 4-course dinner served at the table | buffet | unlimited: unlimited drinks in the price | supper: light meal, not a dinner
#  vegan: vegan dishes marked or on request | deck: open deck confirmed (seller or guests) | short: 90 minutes
#  wheelchair: confirmed wheelchair-accessible boat | under70: adult price under €70 | tested: I rode it
FILTER_CATS = {
    L: "romantic kids served deck tested",
    HK: "folk kids served deck short under70 tested",
    S: "romantic folk served vegan tested",
    SE: "romantic folk kids served deck under70",
    RD: "kids buffet unlimited vegan deck wheelchair",
    G: "folk supper short under70",
}

# Booking terms per seller (bold promise + lighter detail). Owner's rule: free cancellation is always one of the promises.
#  GetYourGuide listings: "Free cancellation: cancel up to 24 hours in advance for a full refund"; "Reserve now and pay later".
#  Legenda direct: free cancellation confirmed by the owner (a Legenda partner), 72 h for dinner cruises (24 h for sightseeing);
#    Legenda FAQ: tickets can be moved to another day at the pier, subject to availability.
#  Silverline direct: silver-line.hu/faq (checked 17 Nov 2026): "Cancelling or modifying a reservation 24 hours before departure -
#    100% of the amount is to be refunded"; within 24 h not refundable. (Their T&C mentions a 10% fee; the owner chose the FAQ.)
TRUST = {
    "gyg": ["<b>Pay nothing today</b>, pay closer to the date", "<b>Free cancellation</b> up to 24 h before, full refund"],
    "legenda": ["<b>Change your date</b> at the Legenda pier", "<b>Free cancellation</b> up to 72 h before, full refund"],
    "silverline": ["<b>Free date change</b> up to 24 h before", "<b>Free cancellation</b> up to 24 h before, full refund"],
}  # exactly 2 per card, free cancellation always 2nd (owner's rule)
REVIEW_TERMS = {  # (buy-card perk, buy-card trust line, quick-facts cancellation row)
    "gyg": ("Free cancellation up to 24 h", "Free cancellation up to 24 hours before", "Free cancellation up to 24 hours before; pay nothing today"),
    "legenda": ("Free cancellation up to 72 h", "Free cancellation up to 72 hours before",
                "Free cancellation up to 72 hours before; date change at the Legenda pier, if seats are free"),
    "silverline": ("Free cancellation up to 24 h", "Free cancellation or date change up to 24 hours before",
                   "Free cancellation or date change up to 24 hours before departure; no refund within 24 hours"),
}


# ------------------------------------------------------------------ helpers
def pill(emoji, label, lead, note, cls=""):
    return (f'<details class="bpa-lang {cls}"><summary class="bpa-sp">{emoji} <span class="bpa-lang-label">{label}</span>'
            f'<span class="bpa-lang-chev" aria-hidden="true">▾</span></summary><div class="bpa-lang-pop"><strong>{lead}</strong> {note}</div></details>')


def access_pill(anc):
    lab, wc, kids = ACCESS[anc]
    mark = {True: '<span class="cd-yes">✓</span>', False: '<span class="cd-no">✕</span>', None: '<span class="cd-ask">ⓘ</span>'}[wc[0]]
    rows = (f'<span class="bpa-lang-note">♿ <b>Wheelchair:</b> {mark} {wc[1]}</span>'
            f'<span class="bpa-lang-note">🎟️ <b>Kids:</b> {kids}</span>')
    return (f'<details class="bpa-lang cd-access"><summary class="bpa-sp">♿ <span class="bpa-lang-label">{lab}</span> '
            f'<span class="bpa-lang-chev">▾</span></summary><div class="bpa-lang-pop">{rows}</div></details>')


def build_pills(anc):
    data = PILLS[anc]
    kinds = [p[0] for p in data]
    assert kinds[:6] == KINDS_FIXED and 1 <= len(kinds) - 6 <= 2, (anc, kinds)  # fixed pill order
    out = []
    for p in data:
        k = p[0]
        if k == "access":
            out.append(access_pill(anc))
        elif k == "time":
            d = DOCK[anc]
            note = p[4] + f'<span class="bpa-lang-note"><b>📍 {d[0]}:</b> {d[1]}</span>'
            out.append(pill(p[1], p[2], p[3], note, "bpa-time"))
        else:
            out.append(pill(p[1], p[2], p[3], p[4], "fbm-vibe" if k == "vibe" else ""))
    return out


def thumbs(media):
    imgs = re.findall(r"<img\b[^>]*>", media)
    out = []
    for i, im in enumerate(imgs):
        src = (re.search(r'\sdata-src="([^"]+)"', im) or re.search(r'\ssrc="([^"]+)"', im)).group(1)
        small = re.sub(r"(\.\w+)$", r"-p-500\1", src)
        if (ROOT / urllib.parse.unquote(small.lstrip("/"))).exists():
            src = small
        cls = "cd-thumb" + (" is-on" if i == 0 else "") + (" is-hid" if i > 4 else "")
        more = f' data-more="+{len(imgs) - 4}"' if i == 4 and len(imgs) > 5 else ""
        out.append(f'<button type="button" class="{cls}" data-i="{i}"{more} aria-label="Show photo {i + 1} of {len(imgs)}">'
                   f'<img src="{src}" alt="" loading="lazy" decoding="async" width="80" height="60"></button>')
    return '<div class="cd-thumbs" aria-label="Photo thumbnails">' + "".join(out) + "</div>"


def price_dd(anc):
    p, sub, rows, total = PRICE[anc]
    tr = "".join(f"<tr><td>{a}{f'<small>{b}</small>' if b else ''}</td><td>{c}</td></tr>" for a, b, c in rows)
    tot = f'<div class="cd-pdd-total"><span>{total[0]}</span><span>{total[1]}</span></div>' if total else ""
    first = "Adult<small>evening dinner</small>" if anc == L else ("Person" if anc == G else "Adult")
    return (f'<details class="cd-pdd"><summary><span class="cd-pdd-main">{p}</span><span class="cd-pdd-sub">{sub} '
            f'<span class="cd-pdd-chev" aria-hidden="true">▾</span></span></summary><div class="cd-pdd-pop"><div class="cd-pdd-h">All ticket prices</div>'
            f'<table><tr><td>{first}</td><td>{p}</td></tr>{tr}</table>{tot}'
            '<div class="cd-pdd-note">Prices for the cheapest date; weekend evenings can cost more. Final price shown before you pay.</div></div></details>')


def unlink_ratings(block):
    """Direct-booking cards (Legenda, Silverline) keep the OTA rating rows unlinked: the clicks should go to the direct link."""
    def fix(m):
        x = re.sub(r'<a class="bpa-rev-badge is-link" href="[^"]*" rel="[^"]*" target="_blank">', '<span class="bpa-rev-badge">', m.group(0))
        x = x.replace('<span class="bpa-rev-go" aria-hidden="true">→</span></a>', "</span>")
        assert "<a " not in x, "rating link left"
        return x
    return re.sub(r'<span class="bpa-rate-list">.*?</span></div></details>', fix, block, flags=re.S)


def div_end(src, start):
    depth = 0
    for m in re.finditer(r"<div\b|</div>", src[start:]):
        depth += 1 if m.group(0) == "<div" else -1
        if depth == 0:
            return start + m.end()
    raise ValueError("unbalanced div")


# ------------------------------------------------------------------ split cards and reviews
starts = [m.start() for m in re.finditer(r'<div class="bpa-card" data-cat="[^"]*" id="card-\d+">', s)]
assert len(starts) == 6, len(starts)
first = re.search(r'<!-- #\d+:[^\n]*-->\n$', s[:starts[0]]).start()
last_sub = s.find('class="bpa-sublink"', starts[-1])
tail = s.find("</div>\n</div>\n</div>", last_sub) + len("</div>\n</div>\n</div>")
cards = {}
for a, b in zip(starts, starts[1:] + [tail]):
    c = re.sub(r'\n?<!-- #\d+:[^\n]*-->\n?$', "\n", s[a:b])
    cards[re.search(r'class="bpa-sublink" href="#([^"]+)"', c).group(1)] = c.rstrip("\n") + "\n"

reviews, rev_a, rev_b = {}, None, None
for m in re.finditer(r'<details class="bpa-details-card"[^>]*id="([^"]+)"', s):
    st, depth = m.start(), 0
    for t in re.finditer(r"<(/?)details\b", s[st:]):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            en = s.index(">", st + t.start()) + 1
            break
    reviews[m.group(1)] = s[st:en]
    rev_a = st if rev_a is None else rev_a
    rev_b = en
assert set(cards) == set(reviews) == set(ORDER), (set(cards), set(reviews))


def rank(block, n, anc):
    if anc in RANK:
        cls, lab = RANK[anc]
        return re.sub(r'<span class="bpa-rank-tag [^"]*">[^<]*</span>', f'<span class="bpa-rank-tag {cls}">{lab.format(n=n)}</span>', block, count=1)
    return re.sub(r'(<span class="bpa-rank-tag[^"]*">[^<#]*)#\d+', lambda m: f"{m.group(1)}#{n}", block, count=1)


# ------------------------------------------------------------------ cards
new_cards, card_rating = [], {}
for n, anc in enumerate(ORDER, 1):
    c = cards[anc]
    kind = SELLER.get(anc, "gyg")
    c = re.sub(r'<div class="bpa-card" data-cat="[^"]*" id="card-\d+">', f'<div class="bpa-card" data-cat="{FILTER_CATS[anc]}" id="card-{n}">', c, count=1)
    c = rank(c, n, anc)
    # gallery thumbnails
    mi, ii = c.find('<div class="bpa-media">'), c.find('\n<div class="bpa-info">')
    media = c[mi:ii]
    c = c[:mi] + '<div class="cd-gal">' + media + thumbs(media) + "</div>" + c[ii:]
    # "Personally tested" as a dropdown next to the rating
    tm = re.search(r'<details class="bpa-lang bpa-tested bpa-proof-mobile">.*?</details>\n?', c, re.S)
    if tm:
        det = tm.group(0).strip().replace("✓ Personally Tested", "Personally tested")
        det = det.replace('class="bpa-lang bpa-tested bpa-proof-mobile"', 'class="bpa-lang bpa-tested"').replace('class="bpa-vchip bpa-proof-mobile"', 'class="bpa-vchip"')
        c = c.replace(tm.group(0), "")
        c = re.sub(r'<div class="bpa-proof">.*?</div>', f'<div class="bpa-proof">{det}</div>', c, count=1, flags=re.S)
    if kind != "gyg":
        c = unlink_ratings(c)
    cs = c.index('<div class="bpa-summary-reviews bpa-rate">')
    card_rating[anc] = c[cs:div_end(c, cs)]
    # pills in the fixed order + the hidden timetable slot for the AI finder
    sr = re.search(r'(<div class="bpa-specs-row">)(.*?)(</div>\n<div class="bpa-best-for)', c, re.S)
    tt, dur = TT[anc]
    slot = f'<div class="fbm-slot" data-tt="{E(json.dumps(tt))}" data-dur="{dur}"></div>'
    c = c.replace(sr.group(0), sr.group(1) + "\n" + "\n".join(build_pills(anc)) + "\n</div>\n" + slot + "\n" + sr.group(3)[len("</div>\n"):])
    # questions box under Pick/Skip
    i = c.index('<div class="bpa-best-for bpa-pickskip">')
    k = c.index("</div>", i) + len("</div>")
    qa = EDGE_QA[anc]
    assert len(qa) == 5, anc
    faq = (f'<details class="fbm-faq"><summary>❓ {len(qa)} questions travellers ask <span class="fbm-faq-chev" aria-hidden="true">▾</span></summary>'
           '<div class="fbm-faq-body">' + "".join(f'<div class="fbm-qa"><div class="fbm-q">{q}</div><div class="fbm-a">{a}</div></div>' for q, a in qa)
           + "</div></details>")
    c = c[:k] + "\n" + faq + c[k:]
    # price dropdown (evening / dinner price by default)
    pm = re.search(r'(?:<div class="bpa-was">[^<]*</div>\s*)?<div class="bpa-price">[^<]*</div>\s*<div class="bpa-psub">[^<]*</div>', c)
    c = c.replace(pm.group(0), price_dd(anc))
    # verified booking box
    c = re.sub(r'<div class="bpa-trust2">.*?</div>', '<div class="bpa-trust2">' + "".join(f"<span>{x}</span>" for x in TRUST[kind]) + "</div>", c, count=1, flags=re.S)
    new_cards.append(f"<!-- #{n}: {SHORT[anc]} -->\n" + c)

s = s[:first] + "".join(new_cards) + s[tail:]

# ------------------------------------------------------------------ reviews
new_reviews = []
for n, anc in enumerate(ORDER, 1):
    r = reviews[anc]
    kind = SELLER.get(anc, "gyg")
    r = re.sub(r'(<details class="bpa-details-card" data-cat=")[^"]*"', r'\g<1>' + FILTER_CATS[anc] + '"', r, count=1)
    r = rank(r, n, anc)
    rs = r.index('<div class="bpa-summary-reviews bpa-rate">')
    r = r[:rs] + card_rating[anc] + r[div_end(r, rs):]  # same rating component as the card
    perk, trust, qf = REVIEW_TERMS[kind]
    r = rep(r, '<span class="ltt-buy-perk">Full Refund up to 24h Before</span>', f'<span class="ltt-buy-perk">{perk}</span>', where=anc)
    r = re.sub(r'(<div class="ltt-buy-card-trust">\s*<svg.*?</svg>\s*<span>)Free cancellation up to 24 hours before(</span>)',
               r"\g<1>" + trust + r"\g<2>", r, count=1, flags=re.S)
    r = re.sub(r'(<div class="qf1-label">Cancellation Policy</div>\s*<div class="qf1-val">)[^<]*', r"\g<1>" + qf, r, count=1)
    p = PRICE[anc][0]
    r = re.sub(r'<span class="bpa-details-price">[^<]*</span>', f'<span class="bpa-details-price">{p if anc == L else "From " + p}</span>', r, count=1)
    r = re.sub(r'<span class="ltt-buy-price-val">[^<]*</span>', f'<span class="ltt-buy-price-val">{p if anc == L else "From " + p}</span>', r, count=1)
    if anc == S:
        r = r.replace('<div class="qf1-val">Mobile voucher</div>', '<div class="qf1-val">E-ticket by email as soon as you book</div>')
    new_reviews.append(r)
# replace the review range in one go (the reviews are contiguous)
ra = s.index('<details class="bpa-details-card"')
last_anc = list(reviews)[-1]
rb = s.index(reviews[last_anc]) + len(reviews[last_anc])
assert s[ra:rb].count('<details class="bpa-details-card"') == 6
s = s[:ra] + "".join(new_reviews) + s[rb:]

# ------------------------------------------------------------------ copy fixes (verified 17 Nov 2026)
TEXT = [
    ("Updated 14 Nov 2026", "Updated 17 Nov 2026", 1),
    ("<strong>Last updated</strong>: Nov 14, 2026", "<strong>Last updated</strong>: Nov 17, 2026", 1),
    ("up to date as of 14 November 2026", "up to date as of 17 November 2026", 1),
    # unverified selling point (boat build) removed
    ("Operating custom-built all-glass panoramic vessels, they deliver", "They deliver", 1),
    ('<div class="qf1-val">From €66 (€73.80 on Sat 28 Nov 2026)</div>', '<div class="qf1-val">From €66; weekend evenings can cost more</div>', 1),
    ('<span class="hybrid-active-price" id="sticky-price">From €110</span>', '<span class="hybrid-active-price" id="sticky-price">€110</span>', 1),
    ('<span class="hybrid-active-trust">Free 24h Cancellation</span>', '<span class="hybrid-active-trust" id="sticky-trust">Free cancellation</span>', 1),
    ('data-sub="Free cancellation up to 24h" data-title="4-Course Romantic Candlelit', 'data-sub="Free cancellation up to 72h" data-title="4-Course Romantic Candlelit', 1),
    ('data-sub="3 shows • €77 or €91"', 'data-sub="Free cancellation up to 24h"', None),
    ('<div class="bpa-via">Booked securely via Silverline</div>', '<div class="bpa-via">via Silverline</div>', 1),
]
for old, new, cnt in TEXT:
    k = s.count(old)
    if not k or (cnt and k != cnt):
        raise SystemExit(f"text: expected {cnt or '1+'}x, found {k}x: {old[:80]!r}")
    s = s.replace(old, new)
s = rep(s, '<div class="qf1-val">€40 (all three options)</div>', '<div class="qf1-val">€40 (reduced from €44), all three options</div>', where="goulash qf")

# ------------------------------------------------------------------ intro (same pattern as the river page, PRs #182-184)
# Hook: the cruise that fits your evening, each option linked to its own guide; then the proof (what I rode, what I compared,
# where it was checked) and the two ways in (finder or ranking). The "Short on time?" callout goes, like on the river page.
INTRO_P1 = ('<p>The right Danube dinner cruise is the one that fits your evening: '
            '<strong><a href="/candlelit-dinner-cruise-budapest">a quiet candlelit dinner for two</a></strong>, '
            '<strong>a lively Hungarian folk show</strong>, '
            '<strong><a href="/unlimited-prosecco-cruises-budapest">a buffet with unlimited drinks</a></strong>, or '
            '<strong><a href="/best-budapest-river-cruises">a cheap goulash supper on a sightseeing loop</a></strong>. '
            'This page gets you to that table in under a minute.</p>')
INTRO_P2 = ('<p>To make the choice easy, <strong>I booked and ate on 3 of these dinner cruises myself</strong> '
            '(Legenda, Silverline and Hungária Koncert) and compared all 6 on what really matters: the menu, the show, drinks, seats, docks, '
            '<a href="/best-night-cruises-budapest">sunset times</a> and cancellation terms, checked on each seller\'s own page and in over 300 recent guest reviews. '
            'Describe your evening in the cruise finder below, or scroll straight to the ranking.</p>')
META_DESC = ("I ate on 3 of Budapest's most popular Danube dinner cruises and compared all 6 side by side: menu, show, drinks, docks "
             "and sunset times. Find yours in 30 seconds with the cruise finder.")
ia = s.index('<div class="ltt-lead-copy">')
ib = s.index("</div>", ia) + len("</div>")
s = s[:ia] + '<div class="ltt-lead-copy">\n' + INTRO_P1 + "\n" + INTRO_P2 + "\n</div>" + s[ib:]
s, nco = re.subn(r'\n?<a class="bpdv-callout"[^>]*>.*?</a>', "", s, count=1, flags=re.S)
assert nco == 1, "callout"
old_desc = re.search(r'<meta content="([^"]*)" name="description"/>', s).group(1)
assert s.count(old_desc) >= 3, old_desc
s = s.replace(old_desc, H.escape(META_DESC, quote=True))
INTRO_LD = re.sub(r"<[^>]+>", "", INTRO_P1)

# ------------------------------------------------------------------ AI finder + filter box
fa = river.index("<!-- AI cruise finder")
fz = river.index("</script>", river.index('id="bpa-ai-finder"')) + len("</script>")
finder = river[fa:fz]
for a, b in [("<!-- AI cruise finder (EN river cruises page only) -->", "<!-- AI cruise finder (EN dinner cruises page) -->"),
             ("Show all 13 again", "Show all 6 again"),
             ("/api/cruise-finder?page=best-budapest-river-cruises&", "/api/cruise-finder?page=best-dinner-cruises-budapest&"),
             ("Describe it: “romantic, under €30” · or ask a question: “Is it cold on deck?”",
              "Describe it: “folk show, under €70” · or ask a question: “Is there a vegetarian menu?”")]:
    finder = rep(finder, a, b, where="finder")
in_box_css = re.search(r'<style id="bpa-ai-in-box-css">.*?</style>', river, re.S).group(0)


def btn(cat, label):
    return (f'<button class="ltt-tab-btn" data-cat="{cat}" onclick="lttFilterCruises(\'{cat}\', this)" type="button" '
            f'aria-pressed="false">{label} <span class="cd-n"></span></button>')


fbox = (
    '<div class="ltt-integrated-filter-bar cd-fbox" id="cd-filters" role="group" aria-label="Filter cruises">'
    + finder + in_box_css +
    '<div class="cd-frow fbm-mrow"><span class="cd-flab fbm-mhead">🌇 Catch the sunset or the lit-up city</span>'
    '<span class="fbm-msub">Pick your day to see when the sun sets and when the city is lit up.</span>'
    '<div class="fbm-days" role="group" aria-label="Pick your cruise date">'
    '<button type="button" class="fbm-day is-on" data-day="0" aria-pressed="true">Today</button>'
    '<button type="button" class="fbm-day" data-day="1" aria-pressed="false">Tomorrow</button>'
    '<label class="fbm-day fbm-other">📅 <span>Other date</span><input type="date" id="fbm-date" aria-label="Pick another cruise date"></label>'
    '</div><span class="fbm-mnote" id="fbm-mnote"></span></div>'
    '<div class="cd-frow cd-frow-main"><span class="cd-flab">Occasion</span><div class="cd-fchips">'
    + btn("romantic", "💑 Romantic evening") + btn("folk", "🎻 Hungarian folk music") + btn("kids", "👨‍👩‍👧 With kids") + "</div></div>"
    '<div class="cd-frow cd-frow-more"><span class="cd-flab">What\'s included</span><div class="cd-fchips">'
    + btn("served", "🍽️ 4-course served dinner") + btn("buffet", "🥘 Buffet") + btn("unlimited", "🍾 Unlimited drinks")
    + btn("supper", "🥣 Light supper") + btn("vegan", "🌱 Vegan options") + "</div></div>"
    '<div class="cd-frow cd-frow-more"><span class="cd-flab">Practical</span><div class="cd-fchips">'
    + btn("deck", "🌬️ Open deck") + btn("short", "⏱️ 90 minutes") + btn("wheelchair", "♿ Wheelchair access") + "</div></div>"
    '<div class="cd-frow cd-frow-more"><span class="cd-flab">Budget &amp; proof</span><div class="cd-fchips">'
    + btn("under70", "💶 Under €70") + btn("tested", "✓ Personally tested") + "</div></div>"
    '<button type="button" class="cd-fmore" aria-expanded="false" hidden>More filters <span class="cd-fmore-n"></span> ▾</button>'
    '<div class="cd-ffoot"><span class="cd-fcount" aria-live="polite">Showing <b>6</b> of 6 cruises</span>'
    '<div class="cd-fapplied"></div><button type="button" class="cd-fclear" hidden onclick="lttFilterCruises(\'all\')">Clear all</button></div></div>'
)
fb_start = s.index('<div class="ltt-integrated-filter-bar">')
fb_end_marker = "Personally Tested (3)</button>\n</div>\n</div>"
fb_end = s.index(fb_end_marker, fb_start) + len(fb_end_marker)
s = s[:fb_start] + fbox + s[fb_end:]
for cat in set(" ".join(FILTER_CATS.values()).split()):
    assert f'data-cat="{cat}"' in fbox, cat
mini = ('<div class="cd-fmini" aria-hidden="true"><div class="cd-fmini-in"><button type="button" class="cd-fmini-btn" '
        'onclick="cdFiltersJump()">⚙️ Filters <span class="cd-fmini-n" hidden></span></button><span class="cd-fmini-res">'
        '<b>6</b> of 6 cruises</span></div></div>')
s = rep(s, '<div class="bpa-deck-wrap" id="ltt-cards-deck">', '<div class="bpa-deck-wrap" id="ltt-cards-deck">' + mini, where="mini")

# ------------------------------------------------------------------ TOC / sticky config + JSON-LD
cfg = re.search(r'window\.LTT_PAGE_CONFIG = (\{.*?\});', s).group(1)
cfgd = json.loads(cfg)
cfgd["shortTitles"] = [SHORT[a] for a in ORDER]
s = s.replace(cfg, json.dumps(cfgd, ensure_ascii=False))

jm = re.search(r'(<script id="ltt-schema-jsonld" type="application/ld\+json">)(.*?)(</script>)', s, re.S)
data = json.loads(jm.group(2))
art = next(x for x in data["@graph"] if x.get("@type") == "Article")
art["dateModified"] = "2026-11-17"
art["description"] = META_DESC
lst = art["mainEntity"]
lst["description"] = H.unescape(INTRO_LD)
by = {e["url"].split("#")[1]: e for e in lst["itemListElement"]}
items = []
for n, anc in enumerate(ORDER, 1):
    e = by[anc]
    e["position"] = n
    it = e["item"]
    lab = RANK.get(anc, (None, None))[1]
    it["description"] = re.sub(r"#\d+", f"#{n}", it.get("description", ""), count=1)
    if lab:
        it["description"] = re.sub(r"^(?:\S+ )?#\d+ [^:]+", H.unescape(lab.format(n=n)).split(" ", 1)[1], it["description"])
    it["offers"]["price"] = PRICE[anc][0].lstrip("€")
    ar = it.get("aggregateRating")
    if isinstance(ar, dict) and not (ar.get("ratingValue") and ar.get("reviewCount")):
        del it["aggregateRating"]
    items.append(e)
lst["itemListElement"] = items
data["@graph"].append({"@type": "FAQPage", "@id": URL + "#faq",
                       "mainEntity": [{"@type": "Question", "name": f"{SHORT[a]}: {H.unescape(q)}",
                                       "acceptedAnswer": {"@type": "Answer", "text": H.unescape(ans)}}
                                      for a in ORDER for q, ans in EDGE_QA[a]]})
s = s.replace(jm.group(0), jm.group(1) + json.dumps(data, ensure_ascii=False) + jm.group(3))

# ------------------------------------------------------------------ CSS / JS copied from the river page (already patched there)


def block(tag, i):
    return re.search(r'<%s id="%s"[^>]*>.*?</%s>' % (tag, i, tag), river, re.S).group(0)


css = "".join(block("style", i) for i in ("cd-cards-css", "cd-tested-css", "cd-filters-css", "fbm-css", "fbm-hide-slot",
                                          "fbm-lights-css", "cd-fmore-css", "fbm-days-css", "cd-trust-css"))
css += ('<style id="dc-rate-plain-css">.bpa-rev-badge:not(.is-link){cursor:default}</style>')
# no cd-sticky-trust-js: the sticky bar always shows "Free cancellation"
js = "".join(block("script", i) for i in ("cd-cards-js", "cd-filters-js", "fbm-js", "cd-fmore-js", "fbm-days-js"))
import sys as _sys, os as _os; _sys.path.insert(0, _os.path.dirname(__file__)); import gallery_fix; js = gallery_fix.patch(js)
# Price dropdown opens on hover like the pills (mouse only): hover opens, leaving closes, a click pins it open.
js += """<script id="cd-pdd-hover-js">
(function(){
  if(!(window.matchMedia && window.matchMedia('(hover: hover) and (pointer: fine)').matches)) return;
  document.querySelectorAll('.cd-pdd').forEach(function(d){
    var sum=d.querySelector('summary'), pinned=false, t=null;
    d.addEventListener('mouseenter',function(){ clearTimeout(t); if(!d.open){ pinned=false; d.open=true; } });
    d.addEventListener('mouseleave',function(){ if(pinned) return; t=setTimeout(function(){ d.open=false; },120); });
    sum.addEventListener('click',function(e){
      if(d.open && !pinned){ e.preventDefault(); pinned=true; return; }  // opened by hover: the click pins it
      pinned=!d.open;
    });
    d.addEventListener('toggle',function(){ if(!d.open) pinned=false; });
  });
})();
</script>"""
# "Peek C" (owner's pick, same code as the river page, feat/river-pill-peek e6496eb): when the #1 card scrolls into view,
# its first pill opens for 1.5 s and closes. Once per load, skipped if the visitor already opened a pill. No layout change.
js += """<script id="pill-peek-js">
/* Show that pills open: when the #1 card scrolls into view, its first pill opens for 1.5 s and closes. Once per load; skipped if the visitor already opened a pill. */
(function(){
  function run(){
    var card=document.getElementById('card-1'), sm=card&&card.querySelector('.bpa-specs-row .bpa-lang>summary'); if(!sm||!('IntersectionObserver' in window)) return;
    var touched=false; document.addEventListener('click',function(e){ if(e.isTrusted&&e.target.closest('.bpa-lang')) touched=true; },true);
    var io=new IntersectionObserver(function(es){ if(!es[0].isIntersecting) return; io.disconnect();
      setTimeout(function(){ if(touched) return; sm.click(); setTimeout(function(){ if(sm.parentNode.classList.contains('is-open')||sm.parentNode.open) sm.click(); },1500); },600); },{threshold:.6});
    io.observe(card);
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',run); else run();
})();
</script>"""
s = rep(s, "</head>", css + "</head>", where="css")
k = s.rfind("</body>")
s = s[:k] + js + "\n" + s[k:]

# ------------------------------------------------------------------ guards
body = re.sub(r"<script.*?</script>|<style.*?</style>", "", s, flags=re.S)
assert "—" not in re.sub(r"<[^>]+>", "", body), "em dash in copy"
for m in re.finditer(r'<a [^>]*href="(https://(?:www\.getyourguide\.com|legenda\.hu|budapestrivercruise\.eu)[^"]*)"[^>]*>', s):
    tag, url = m.group(0), m.group(1)
    if "getyourguide" in url:
        assert "mkt_cmp=true" in url, url
    if "legenda.hu" in url:
        assert url.endswith("?partner=38585"), url
    if "budapestrivercruise.eu" in url:
        assert url.endswith("?code=bpadventures"), url
    rel = re.search(r'rel="([^"]*)"', tag)
    assert rel and {"nofollow", "sponsored", "noopener"} <= set(rel.group(1).split()), tag[:160]
assert "0.0" not in re.findall(r'bpa-rate-score">([^<]*)', s)
for m in re.finditer(r'<div class="bpa-trust2">(.*?)</div>', s):  # exactly 2 promises, free cancellation 2nd
    spans = re.findall(r"<span>(.*?)</span>", m.group(1))
    assert len(spans) == 2 and spans[1].startswith("<b>Free cancellation</b>"), m.group(1)
assert not re.search(r"10% fee|Full refund up to 24 hours before departure", s)

(ROOT / PAGE).write_text(s, encoding="utf-8")
print("ok", PAGE, len(s))
