#!/usr/bin/env python3
"""Build a noindex TEST page of the night cruises article.

It ports the approved Seine card design (thumbnail strip, exact price with a
price dropdown, "Personally tested" stamp, grouped combinable filters) and puts
the questions travellers keep asking in Budapest Facebook groups straight into
the top-10 card list:

- "When are you going?" month row in the filter box: every card then shows
  which of its listed sailings are fully lit, sunset-into-lights, or still daylight
- new filters: just views (no party, no dinner), good if you don't drink,
  party crowd, open-air deck, heated indoor, about 1 hour
- two new pill dropdowns per card: atmosphere ("relaxing or booze cruise?")
  and dock ("which dock should I pick?")

Usage: build_night_fb_test.py best-night-cruises-budapest.html best-night-cruises-budapest-test.html
"""
import html as H
import json
import re
import sys

SRC, OUT = sys.argv[1], sys.argv[2]
SEINE = sys.argv[3] if len(sys.argv) > 3 else None
s = open(SRC, encoding="utf-8").read()


def rep(text, old, new, count=1, where=""):
    n = text.count(old)
    if n != count:
        raise SystemExit(f"[{where}] expected {count}x, found {n}x: {old[:100]!r}")
    return text.replace(old, new)


# ------------------------------------------------------------------ card data
# times = listed evening sailings (from each card's own time dropdown), dur = minutes
CARDS = {
    1: dict(cat="tested calm nodrink opendeck heated hour", dur=60,
            times=[f"{h:02d}:{m:02d}" for h in range(16, 22) for m in (0, 20, 40)
                   if "16:20" <= f"{h:02d}:{m:02d}" <= "21:00"], every="every 20 min",
            tt=[{"from": "11-23", "to": "12-31", "times": ["15:40"] + [f"{h:02d}:{m:02d}" for h in range(16, 22) for m in (0, 20, 40)
                   if "16:20" <= f"{h:02d}:{m:02d}" <= "21:00"]}],
            vibe=("🙂", "Calm sightseeing",
                  "Seated sightseeing with a 30-language audio guide on headsets, not a party boat.",
                  "Open-air seats at the back of the top deck, heated cabin below. The welcome drink can be a soft drink or water, so non-drinkers pay for nothing they skip."),
            dock=("Vigadó tér, Dock 7",
                  "Pest side, 2 minutes from Vörösmarty tér and the top of Váci utca.",
                  "Covered floating dock with restrooms and a rooftop waiting area.")),
    2: dict(cat="tested unlimited party opendeck hour", dur=75,
            times=["15:30", "15:45", "17:15", "18:45", "22:15", "22:30", "23:00"],
            vibe=("🎉", "Cocktail-party feel",
                  "Lively, not a quiet sightseeing hour.",
                  "On my cruise the commentary was hard to hear over the party noise. Open top deck plus two indoor decks; board early for the best top-deck spots. Lemonade is self-service, so non-drinkers are covered too."),
            dock=("3 docks to choose from",
                  "Akadémia 3 is by the Chain Bridge, best from Parliament or the Basilica. Vigadó 8/A is by Vörösmarty tér, best from Váci utca. Carl Lutz rakpart Dock 0 is further north on the Pest bank.",
                  "Pick the dock when you choose your time slot.")),
    3: dict(cat="tested calm nodrink opendeck heated hour under20", dur=60,
            times=["16:00", "17:30", "19:00", "20:30"],
            vibe=("🎹", "Quiet and historic",
                  "Classical piano plays between the narration on a historic paddle steamer.",
                  "Open-air panorama deck at the front, heated indoor area in winter. The welcome glass is prosecco or orange juice."),
            dock=("Dock 10, Elizabeth Bridge",
                  "Pest side next to Elizabeth Bridge, a short walk from Ferenciek tere metro.",
                  "No baby strollers and no wheelchair access on board.")),
    4: dict(cat="tested dinner nodrink opendeck heated", dur=150, times=["19:00"],
            vibe=("🕯️", "Romantic and quiet",
                  "Candlelit tables for two along the windows, a pianist and singer, no loud folk show.",
                  "Open top deck for photos at any point of the evening. Not for children under 3, and there is no vegan menu."),
            dock=("Vigadó tér, Dock 7",
                  "Pest side, 2 minutes from Vörösmarty tér and the top of Váci utca.",
                  "Legenda's covered dock has restrooms, so you can wait out of the rain.")),
    5: dict(cat="dinner unlimited opendeck", dur=150, times=["19:30"],
            vibe=("🎻", "All-inclusive evening",
                  "A seasonal buffet, unlimited drinks served to your table and live music in the Grand Salon.",
                  "After dinner you can go up to the rooftop deck, weather permitting."),
            dock=("Akadémia 3",
                  "Pest side by the Chain Bridge, best if you stay near Parliament, the Basilica or Széchenyi tér.",
                  "Bring a passport or ID card with the voucher.")),
    6: dict(cat="calm nodrink opendeck heated hour under20", dur=50,
            times=["16:10", "17:20", "18:30", "19:40", "20:50"],
            vibe=("🧺", "Relaxed, bring your own",
                  "A small boat with at most 150 guests, and everyone gets a rooftop seat.",
                  "No bar on board: bring your own drinks, alcohol-free included. The rooftop gets cold in November, so bring layers; the heated cabin is open to all."),
            dock=("Várkert Bazár, Buda side",
                  "Below the Castle on the Buda bank, the easy pick if you stay in Buda.",
                  "Most other boats leave from the Pest bank, so check which side you are on.")),
    7: dict(cat="tested dinner opendeck", dur=120, times=["19:00"],
            vibe=("🍷", "Intimate dinner",
                  "Dinner on the upper deck at 2 or 4-person tables; it never felt overcrowded.",
                  "Pick the no-show option for background music only. For night photos step out to the open bow or stern: the cabin lights reflect in the glass."),
            dock=("Dock 11, Elizabeth Bridge",
                  "Pest side next to Elizabeth Bridge, a short walk from Ferenciek tere metro.",
                  "Same boat and menu for all 3 show options.")),
    8: dict(cat="unlimited party opendeck heated hour under20", dur=75,
            times=["18:00", "19:30", "21:00"],
            vibe=("🎶", "Lively rooftop",
                  "Guests keep mentioning the music and the friendly crew.",
                  "Everyone has a seat on the heated lower deck; rooftop seats are first come, first served. Soft drinks and homemade lemonade are included."),
            dock=("Petőfi tér 9",
                  "Pest bank between Elizabeth Bridge and Vigadó tér, an easy walk from Váci utca.",
                  "Arrive 15 minutes early: boarding closes 5 minutes before departure.")),
    9: dict(cat="unlimited party hour", dur=60, times=["16:30", "19:30", "21:00"],
            vibe=("🍾", "Pre-party",
                  "Party songs from the loudspeakers, pitched as a warm-up before a night out.",
                  "Adults only: under-18s are not allowed, and it is not for pregnant guests."),
            dock=("Dock 11, Elizabeth Bridge",
                  "Pest side next to Elizabeth Bridge, a short walk from Ferenciek tere metro.",
                  "The upper deck is the spot for photos of the lit-up Parliament.")),
    10: dict(cat="tested calm nodrink heated hour under20", dur=60,
             times=["16:30", "17:00", "17:20", "18:20", "18:40", "19:40", "20:00", "21:00", "21:15"],
             vibe=("🙂", "No-frills sightseeing",
                   "A plain sightseeing hour with no drink included.",
                   "Heated main deck. The upper deck costs €5 more and has a roof with columns that block part of the view. Infants up to 3 ride free."),
             dock=("Dock 11, Elizabeth Bridge",
                   "Pest side next to Elizabeth Bridge, a short walk from Ferenciek tere metro.",
                   "Comfortable indoor meeting point.")),
}

# Plain span pills -> dropdowns (facts from each card's own review and spec box).
# key = the span's visible label (after the emoji)
PILLS = {
    1: {"Welcome Drink": ("1 drink included: champagne, wine, beer, a soft drink or mineral water.",
                          "In summer you get a free lemonade on top. More drinks at the bar on board.")},
    2: {"Unlimited Prosecco, Spritzers &amp; Beer": (
        "Unlimited for 75 minutes: Hungarian sparkling wine, Aperol, Hugo, Rossini and Limoncello spritzers, beer, lemonade and lemon-mint water.",
        "You start with a welcome glass of sparkling wine; refills at the bar. Food costs extra.")},
    3: {"Welcome Drink": ("1 drink included: a glass of prosecco or orange juice.",
                         "When I tested it, water and beer were offered too.")},
    4: {"4-Course Dinner": ("4 courses picked from the menu at the table: starter, soup, main course and dessert.",
                            "Children 3 to 12 get 3 courses. No vegan menu, and not for food allergies."),
        "Welcome Drink": ("1 drink included: champagne, wine, beer, a soft drink or mineral water.",
                          "Every other drink is paid on board."),
        "Live Music": ("A pianist and singer play lounge music all evening.",
                       "Quiet enough to talk: no loud folk show.")},
    5: {"Seasonal Buffet": ("A seasonal buffet by Executive Chef Viktor Moldován: starters, mains, sides, vegetarian dishes and desserts.",
                            "Flag dietary needs when you book."),
        "Live Music": ("Live music in the Grand Salon through the evening.",
                       "There is no sightseeing commentary, just an English-speaking host.")},
    6: {"Bring Your Own Drinks": ("No drink included and no bar on board: bring your own drinks and snacks.",
                                  "Wine, beer or alcohol-free, your choice, with no bar prices or queues."),
        "Guaranteed Rooftop Seat": ("Every guest gets a seat on the open rooftop; at most 150 on board.",
                                    "The heated cabin downstairs is open to everyone if it rains or gets cold.")},
    7: {"4-Course Dinner": ("4 courses, picked from 1 appetizer, 2 soups, 3 mains and 3 desserts.",
                            "A vegetarian option is available."),
        "Welcome Prosecco": ("1 drink included: a welcome glass of Prosecco.",
                             "Every other drink is paid on board.")},
    9: {"Unlimited Prosecco": ("Unlimited prosecco for the whole 60 minutes.",
                               "Only prosecco is unlimited; snacks are for sale, and you can't bring your own food or drinks.")},
    10: {"Upper Deck +€5": ("The panoramic upper deck costs €5 more.",
                            "It has a roof with columns that block part of the view.")},
}
NEW_DRINK = {10: ("🥤", "No drink included", "No drink in the ticket price: even water costs extra.",
                  "There is a bar on board.")}

# Access and kids pill (third in the fixed Seine order). None = not stated on the listing yet.
ACCESS = {
    1: ("👶", "Under 10 free", "Children under 10 ride free; 10 to 14 pay €17.50.", "Step-free access: not stated on the listing yet."),
    2: ("♿", "Access: to check", "Kids prices and step-free access are not stated on the listing yet.", ""),
    3: ("♿", "No strollers or wheelchairs", "Baby strollers are not allowed and the boat is not wheelchair accessible.", "Kids prices: not stated on the listing yet."),
    4: ("👶", "Kids 3-12 €84 · not step-free", "Children 3 to 12 pay €84 for 3 courses; not suitable for children under 3.", "Not wheelchair accessible."),
    5: ("♿", "Access: to check", "Kids prices and step-free access are not stated on the listing yet.", "Pets are not allowed; assistance dogs are."),
    6: ("♿", "Not step-free · pets OK", "Not suitable for wheelchair users.", "Pets are allowed on board. Kids prices: not stated on the listing yet."),
    7: ("♿", "Not step-free", "Not wheelchair accessible.", "Kids prices: not stated on the listing yet."),
    8: ("♿", "Not step-free", "Not wheelchair accessible.", "Kids prices: not stated on the listing yet."),
    9: ("🔞", "18+ only", "Under-18s are not allowed.", "Not suitable for pregnant guests."),
    10: ("👶", "Under 4 free", "Infants up to 3 ride free.", "Step-free access: not stated on the listing yet."),
}
# Price dropdown rows: (label, small, price). "verify" = still to check on the listing.
KIDS = {
    1: ([("Student", "", "€22.50"), ("Child", "10-14", "€17.50"), ("Under 10", "", "Free")], ("2 adults + 2 kids (10-14)", "€85")),
    4: ([("Child", "3-12, 3 courses", "€84"), ("Under 3", "", "Not allowed")], ("2 adults + 2 kids (3-12)", "€388")),
    9: ([("Under 18", "", "Not allowed")], None),
    10: ([("Infant", "0-3", "Free"), ("Kids 4+", "", "verify")], None),
}

E = H.escape


def pill(emoji, label, lead, note, cls=""):
    return (f'<details class="bpa-lang {cls}"><summary class="bpa-sp">{emoji} <span class="bpa-lang-label">{E(label)}</span>'
            f'<span class="bpa-lang-chev" aria-hidden="true">▾</span></summary><div class="bpa-lang-pop"><strong>{E(lead)}</strong> '
            f'{E(note)}</div></details>')


def rows_html(num):
    rows = KIDS.get(num, ([("Kids", "age bands per listing", "verify")], None))[0]
    out = ""
    for lab, small, pr in rows:
        sm = f"<small>{E(small)}</small>" if small else ""
        cls = ' class="fbm-verify"' if pr == "verify" else ""
        out += f"<tr><td>{E(lab)}{sm}</td><td{cls}>{E(pr)}</td></tr>"
    return out


def total_html(num):
    t = KIDS.get(num, (None, None))[1]
    return f'<div class="cd-pdd-total"><span>{E(t[0])}</span><span>{E(t[1])}</span></div>' if t else ""


def thumbs(media):
    imgs = re.findall(r"<img\b[^>]*>", media)
    out = []
    for i, im in enumerate(imgs):
        src = re.search(r'\sdata-src="([^"]+)"', im) or re.search(r'\ssrc="([^"]+)"', im)
        src = src.group(1)
        ss = re.search(r'(?:data-)?srcset="([^"]+)"', im)
        if ss:  # smallest candidate
            src = ss.group(1).split(",")[0].strip().split(" ")[0]
        cls = "cd-thumb" + (" is-on" if i == 0 else "") + (" is-hid" if i > 4 else "")
        more = f' data-more="+{len(imgs) - 4}"' if i == 4 and len(imgs) > 5 else ""
        out.append(f'<button type="button" class="{cls}" data-i="{i}"{more} aria-label="Show photo {i + 1} of {len(imgs)}">'
                   f'<img src="{src}" alt="" loading="lazy" decoding="async" width="80" height="60"></button>')
    return '<div class="cd-thumbs" aria-label="Photo thumbnails">' + "".join(out) + "</div>"


starts = [m.start() for m in re.finditer(r'<div class="bpa-card" data-cat="[^"]*" id="card-\d+">', s)]
assert len(starts) == 10, len(starts)
ends = starts[1:] + [None]
new_cards = []
for n, st in enumerate(starts):
    num = n + 1
    c = s[st:ends[n]] if ends[n] else None
    if c is None:
        # last card: up to the close of its cta-cell block
        i = s.find('class="bpa-sublink"', st)
        i = s.find("</div>\n</div>\n</div>", i) + len("</div>\n</div>\n</div>")
        c = s[st:i]
    d = CARDS[num]
    # data-cat
    c = re.sub(r'data-cat="[^"]*"', f'data-cat="{d["cat"]}"', c, count=1)
    # gallery -> thumbnails
    mi = c.find('<div class="bpa-media">')
    ii = c.find('\n<div class="bpa-info">')
    media = c[mi:ii]
    c = c[:mi] + '<div class="cd-gal">' + media + thumbs(media) + "</div>" + c[ii:]
    # tested stamp: move the mobile tested dropdown into the proof slot
    tm = re.search(r'<details class="bpa-lang bpa-tested bpa-proof-mobile">.*?</details>', c, re.S)
    if tm:
        det = tm.group(0).replace("✓ Personally Tested", "Personally tested")
        det = det.replace('class="bpa-lang bpa-tested bpa-proof-mobile"', 'class="bpa-lang bpa-tested"').replace(
            'class="bpa-vchip bpa-proof-mobile"', 'class="bpa-vchip"')
        c = c.replace(tm.group(0), "")
        c = re.sub(r'<div class="bpa-proof">.*?</div>', f'<div class="bpa-proof">{det}</div>', c, count=1, flags=re.S)
    # pills: fixed order time -> commentary -> atmosphere -> dock -> extras
    sr = re.search(r'(<div class="bpa-specs-row">)(.*?)(</div>\n<div class="bpa-best-for)', c, re.S)
    body = sr.group(2)
    items = re.findall(r'<details class="bpa-lang[^"]*"[^>]*>.*?</details>|<span class="bpa-sp">.*?</span>', body, re.S)
    time = [x for x in items if "🕒" in x[:200]]
    comm = [x for x in items if "🎧" in x[:200]]
    rest = [x for x in items if x not in time and x not in comm]
    conv = []
    for x in rest:
        m = re.match(r'<span class="bpa-sp">(\S+) (.*?)</span>$', x, re.S)
        if m:
            lab = m.group(2)
            if num == 9 and lab == "18+ only":
                continue  # now the access pill
            lead, note = PILLS[num][lab]
            x = pill(m.group(1), H.unescape(lab), lead, note)
        conv.append(x)
    if num in NEW_DRINK:
        conv.insert(0, pill(*NEW_DRINK[num]))
    isdrink = lambda x: any(k in x[:160] for k in ("🥂", "🍾", "🍸", "🥤"))
    drinks = [x for x in conv if isdrink(x)]
    extra = [x for x in conv if not isdrink(x)]
    # dock facts go into the time dropdown instead of their own pill
    dk = d["dock"]
    if time:
        time[0] = time[0].replace("</div></details>",
                                  f'<span class="bpa-lang-note"><b>📍 {E(dk[0])}:</b> {E(dk[1])} {E(dk[2])}</span></div></details>', 1)
    v, a = d["vibe"], ACCESS[num]
    new = (time + comm + [pill(a[0], a[1], a[2], a[3], "fbm-access")] + drinks
           + [pill(v[0], v[1], v[2], v[3], "fbm-vibe")] + extra)
    tt = (d.get("tt") or []) + [{"from": "", "to": "", "times": d["times"]}]
    slot = (f"<div class=\"fbm-slot\" data-tt='{json.dumps(tt)}' data-dur=\"{d['dur']}\""
            + (f' data-every="{d["every"]}"' if d.get("every") else "") + "></div>")
    c = c.replace(sr.group(0), sr.group(1) + "\n" + "\n".join(new) + "\n</div>\n" + slot + "\n" + sr.group(3)[len("</div>\n"):])
    # price -> exact price + dropdown
    pm = re.search(r'<div class="bpa-price">(?:From )?(€[\d.,]+)</div>\s*<div class="bpa-psub">[^<]*</div>', c)
    p = pm.group(1)
    pdd = (f'<details class="cd-pdd"><summary><span class="cd-pdd-main">{p}</span><span class="cd-pdd-sub">per adult '
           f'<span class="cd-pdd-chev" aria-hidden="true">▾</span></span></summary><div class="cd-pdd-pop"><div class="cd-pdd-h">All ticket prices</div>'
           f'<table><tr><td>Adult</td><td>{p}</td></tr>' + rows_html(num) + '</table>' + total_html(num) +
           f'<div class="cd-pdd-note">Final price shown on the booking page before you pay.</div></div></details>')
    c = c.replace(pm.group(0), pdd)
    new_cards.append(c)

# rebuild: everything before card 1, the new cards, then the rest after the last card
i = s.find('class="bpa-sublink"', starts[-1])
tail_start = s.find("</div>\n</div>\n</div>", i) + len("</div>\n</div>\n</div>")
s = s[:starts[0]] + "".join(new_cards) + s[tail_start:]

# ------------------------------------------------------------------ filter box
def btn(cat, label):
    return (f'<button class="ltt-tab-btn" data-cat="{cat}" onclick="lttFilterCruises(\'{cat}\', this)" type="button" '
            f'aria-pressed="false">{label} <span class="cd-n"></span></button>')


fbox = (
    '<div class="ltt-integrated-filter-bar cd-fbox" id="cd-filters" role="group" aria-label="Filter cruises">'
    '<div class="cd-frow fbm-mrow"><span class="cd-flab">Your cruise date</span><div class="cd-fchips">'
    '<label class="fbm-msel"><span class="sr-only">Cruise date</span><input type="date" id="fbm-date" aria-label="Cruise date"></label>'
    '<span class="fbm-mnote" id="fbm-mnote"></span></div></div>'
    '<div class="cd-frow"><span class="cd-flab">Who is coming</span><div class="cd-fchips">'
    + btn("nodrink", "🥤 Good if you don't drink") + btn("party", "🎉 Party crowd") + "</div></div>"
    '<div class="cd-frow"><span class="cd-flab">The trip</span><div class="cd-fchips">'
    + btn("calm", "🌃 Just views, no party, no dinner") + btn("dinner", "🍽️ Dinner") + btn("unlimited", "🍾 Unlimited drinks")
    + btn("opendeck", "☀️ Open-air deck") + btn("heated", "🔥 Heated indoor") + btn("hour", "⏱️ About 1 hour") + "</div></div>"
    '<div class="cd-frow"><span class="cd-flab">Budget &amp; proof</span><div class="cd-fchips">'
    + btn("tested", "✓ Personally tested") + btn("under20", "💶 Under €20") + "</div></div>"
    '<div class="cd-ffoot"><span class="cd-fcount" aria-live="polite">Showing <b>10</b> of 10 cruises</span>'
    '<div class="cd-fapplied"></div><button type="button" class="cd-fclear" hidden onclick="lttFilterCruises(\'all\')">Clear all</button></div></div>'
)
fb_start = s.find('<div class="ltt-integrated-filter-bar">')
fb_end = s.find("Personally Tested (6)</button>\n</div>\n</div>", fb_start) + len("Personally Tested (6)</button>\n</div>\n</div>")
assert fb_start > 0 and fb_end > fb_start
s = s[:fb_start] + fbox + s[fb_end:]

mini = ('<div class="cd-fmini" aria-hidden="true"><div class="cd-fmini-in"><button type="button" class="cd-fmini-btn" '
        'onclick="cdFiltersJump()">⚙️ Filters <span class="cd-fmini-n" hidden></span></button><span class="cd-fmini-res">'
        '<b>10</b> of 10 cruises</span></div></div>')
s = rep(s, '<div class="bpa-deck-wrap" id="ltt-cards-deck">', '<div class="bpa-deck-wrap" id="ltt-cards-deck">' + mini, where="mini")


# ------------------------------------------------------------------ FAQ (questions travellers ask in Budapest groups)
FAQ = [
    ("Do I need to book a Danube night cruise in advance?",
     "Weekend evenings and December sailings fill up first, so book a few days ahead. All 10 cruises on this page have free cancellation up to 24 hours before departure, so booking early costs you nothing if your plans change."),
    ("What time should I book to see Budapest lit up?",
     "It is fully dark about 35 minutes after sunset. In mid-November that means any sailing from about 16:50; in June you need a boat leaving after 21:30. Pick your date in the filter box above and every card shows which of its sailings are fully lit."),
    ("Which night cruise is best if we want views, not a party or a dinner?",
     "The Legenda Danube Legend cruise (€25) has the clearest commentary, with a 30-language guide on individual headsets. The Kisfaludy paddle steamer (€11) is the quiet, historic option with piano music between the narration. La Perla (€11.40) gives every guest a rooftop seat and lets you bring your own drinks. Tick \"Just views, no party, no dinner\" above to see only these."),
    ("Is the unlimited prosecco cruise relaxing or a booze cruise?",
     "It is lively. On the Duna-Weser prosecco boat the commentary was hard to hear over the party noise when I tested it, and Silverline's prosecco cruise plays party songs and is 18+ only. For a calmer hour with a drink, book an early sailing or the Legenda cruise instead."),
    ("I don't like prosecco. What else can I drink on the unlimited cruises?",
     "The Duna-Weser cruise also pours Aperol, Hugo, Rossini and Limoncello spritzers, beer and lemonade. Floating Lotus adds Hungarian wines, craft beer, Heineken, soft drinks and homemade lemonade. Silverline's prosecco cruise is prosecco only."),
    ("Which night cruise is good if we don't drink alcohol?",
     "Legenda's welcome drink can be a soft drink or mineral water, the Kisfaludy paddle steamer offers orange juice, and on La Perla you bring whatever you like. The unlimited cruises include lemonade, but you pay the unlimited-drinks price."),
    ("Which dock should I choose?",
     "Most boats leave from the Pest bank: Vigadó tér (Dock 7) by Vörösmarty tér, Akadémia 3 by the Chain Bridge, Petőfi tér 9, and Docks 10 and 11 by Elizabeth Bridge. La Perla is the only one here on the Buda side, at Várkert Bazár below the Castle. Pick the dock closest to your hotel; the dock for each cruise is in its time dropdown."),
    ("Can I go outside during a dinner cruise to see the views?",
     "Yes on all three dinner cruises here. Legenda's candlelit cruise has an open top deck you can use at any time, Silverline has open-air areas at the bow and stern, and River Diva opens its rooftop after dinner, weather permitting. Step outside for photos: the cabin lights reflect in the windows."),
    ("Is there a heated boat for a winter night cruise?",
     "Legenda, the Kisfaludy paddle steamer, La Perla, Floating Lotus, Silverline's sightseeing boat and the Legenda dinner boat all have heated indoor areas. Tick \"Heated indoor\" above to see them. La Perla's rooftop gets very cold in November, so bring layers."),
    ("Do I need earphones for the audio guide?",
     "Legenda hands out individual headsets. On the Kisfaludy paddle steamer, La Perla and Floating Lotus the audio guide runs on your own phone, so bring earphones and a charged phone."),
    ("Can children come on Budapest night cruises?",
     "Yes on most. On Legenda's sightseeing cruise children under 10 ride free, and the candlelit dinner is €84 for children 3 to 12. Silverline's prosecco cruise is 18+ only, and baby strollers are not allowed on the Kisfaludy paddle steamer."),
]
faq_html = ('<div class="w-richtext bpa-wt-faq"><h2 id="faq">Frequently Asked Questions</h2>' + "".join(
    f'<h3 class="cf-faq-questions-2">{E(q)}</h3><div class="cf-faq-answer-wrap-2"><div class="cf-faq-content-2 w-richtext"><p>{E(a)}</p></div></div>'
    for q, a in FAQ) + "</div>")
s = rep(s, '<div class="ltt-editorial-wrapper" role="main"></div>', '<div class="ltt-editorial-wrapper" role="main">' + faq_html + "</div>", where="faq")
jm = re.search(r'(<script id="ltt-schema-jsonld" type="application/ld\+json">)(.*?)(</script>)', s, re.S)
data = json.loads(jm.group(2))
node = {"@type": "FAQPage", "@id": "https://www.budapestadventures.com/best-night-cruises-budapest#faq",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
if "@graph" in data:
    data["@graph"].append(node)
else:
    data = {"@context": "https://schema.org", "@graph": [data, node]}
s = s.replace(jm.group(0), jm.group(1) + json.dumps(data, ensure_ascii=False) + jm.group(3))

# ------------------------------------------------------------------ assets
seine = open(SEINE, encoding="utf-8").read()


def block(tag, i):
    return re.search(r'<%s id="%s"[^>]*>.*?</%s>' % (tag, i, tag), seine, re.S).group(0)


fbm_css = """<style id="fbm-css">
.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);border:0}
.fbm-mrow{background:#fffbeb;margin:0 -16px;padding:10px 16px!important;border-radius:14px 14px 0 0}
.fbm-msel input{appearance:auto;font:700 13px/1 'Plus Jakarta Sans',sans-serif;color:#0f172a;border:1px solid #cbd5e1;border-radius:9999px;padding:7px 12px;background:#fff;cursor:pointer}
.fbm-mnote{font:600 12.5px/1.35 'Plus Jakarta Sans',sans-serif;color:#92400e;align-self:center}
.fbm-slot{margin:2px 0 8px;padding:8px 10px;border-radius:10px;background:#f8fafc;border:1px solid #e2e8f0;font:500 13px/1.45 'Plus Jakarta Sans',sans-serif;color:#334155}
.fbm-slot b{color:#0f172a}
.fbm-slot .t{display:inline-block;padding:1px 6px;margin:1px 2px;border-radius:6px;font-weight:700;font-size:12.5px}
.fbm-slot .lit{background:#0a192f;color:#fde68a}
.fbm-slot .dusk{background:#fef3c7;color:#92400e}
.fbm-slot .day{background:#f1f5f9;color:#64748b}
.fbm-slot.is-none{background:#fff7ed;border-color:#fed7aa}
.fbm-src{display:block;margin-top:3px;font-size:11.5px;color:#64748b}
.fbm-verify{background:#fef3c7;color:#92400e!important;font-weight:700}
@media (max-width:767px){.fbm-mrow{margin:0 -12px;padding:10px 12px!important}}
</style>"""

fbm_js = r"""<script id="fbm-js">
(function(){
  /* Exact sunset and civil dusk (sun 6 degrees below the horizon) for Budapest on any date. */
  var LAT=47.4979, LNG=19.0402, R=Math.PI/180, DAY=864e5, J1970=2440588, J2000=2451545, OB=R*23.4397;
  function tj(d){return d.valueOf()/DAY-0.5+J1970;}
  function fj(j){return new Date((j+0.5-J1970)*DAY);}
  function sunAt(date,h){
    var lw=R*-LNG, phi=R*LAT, d=tj(date)-J2000, n=Math.round(d-0.0009-lw/(2*Math.PI));
    var ds=0.0009+lw/(2*Math.PI)+n, M=R*(357.5291+0.98560028*ds);
    var C=R*(1.9148*Math.sin(M)+0.02*Math.sin(2*M)+0.0003*Math.sin(3*M)), L=M+C+R*102.9372+Math.PI;
    var dec=Math.asin(Math.sin(OB)*Math.sin(L));
    var w=Math.acos((Math.sin(h*R)-Math.sin(phi)*Math.sin(dec))/(Math.cos(phi)*Math.cos(dec)));
    var a=0.0009+(w+lw)/(2*Math.PI)+n;
    return fj(J2000+a+0.0053*Math.sin(M)-0.0069*Math.sin(2*L));
  }
  var FMT=new Intl.DateTimeFormat('en-GB',{timeZone:'Europe/Budapest',hour:'2-digit',minute:'2-digit',hour12:false});
  var DFMT=new Intl.DateTimeFormat('en-GB',{timeZone:'Europe/Budapest',day:'numeric',month:'short'});
  function loc(d){return FMT.format(d);}
  function m(t){var p=t.split(':');return +p[0]*60+(+p[1]);}
  function hm(x){return ('0'+Math.floor(x/60)).slice(-2)+':'+('0'+(x%60)).slice(-2);}
  function span(t,c){return '<span class="t '+c+'">'+t+'</span>';}
  function md(iso){return iso.slice(5);}
  function inSeason(r,k){ if(!r.from) return true; return r.from<=r.to ? (k>=r.from&&k<=r.to) : (k>=r.from||k<=r.to); }
  function render(iso){
    var noon=new Date(iso+'T11:00:00Z');
    var SUN=loc(sunAt(noon,-0.833)), DARK=loc(sunAt(noon,-6)), sun=m(SUN), dark=m(DARK), name=DFMT.format(noon), key=md(iso);
    var note=document.getElementById('fbm-mnote');
    if(note) note.textContent='Sunset '+SUN+', fully dark by '+DARK+' on '+name+'. Each card shows which sailings are lit up.';
    document.querySelectorAll('.fbm-slot').forEach(function(el){
      var tt=JSON.parse(el.getAttribute('data-tt')||'[]'), dur=+el.getAttribute('data-dur');
      var row=null; tt.forEach(function(r){ if(!row && r.from && inSeason(r,key)) row=r; });
      if(!row) tt.forEach(function(r){ if(!row && !r.from) row=r; });
      if(!row){ el.innerHTML='📅 <b>'+name+':</b> no sailings in this season.'; el.classList.add('is-none'); return; }
      var times=row.times, lit=[],dusk=[];
      times.forEach(function(t){var a=m(t),b=a+dur; if(a>=dark-10) lit.push(t); else if(b>=dark+10&&a>=sun-45) dusk.push(t);});
      el.classList.toggle('is-none',!lit.length&&!dusk.length);
      var h, src=row.src?' <span class="fbm-src">'+row.src+'</span>':'';
      if(dur>=120&&times.length===1){
        var a=m(times[0]),b=a+dur,left=b-Math.max(a,dark);
        h=left>=15?('🌙 <b>'+name+':</b> dark from '+DARK+', so the last '+(left>=60?Math.floor(left/60)+' h'+(left%60?' '+left%60+' min':''):left+' min')+' of dinner ('+times[0]+' to '+hm(b)+') is under the lights.')
                :(b>sun?('🌇 <b>'+name+':</b> sunset ('+SUN+') happens during dinner; it is fully dark only after you dock ('+DARK+').')
                  :('☀️ <b>'+name+':</b> the cruise ends before sunset ('+SUN+').'));
      } else if(!lit.length&&!dusk.length){
        h='☀️ <b>'+name+':</b> the last sailing ('+times[times.length-1]+') ends before full dark ('+DARK+').';
      } else {
        h='';
        if(lit.length) h+='🌙 <b>Fully lit on '+name+':</b> '+(el.getAttribute('data-every')&&lit.length>3?span(lit[0],'lit')+' then every 20 min to '+span(lit[lit.length-1],'lit'):lit.map(function(t){return span(t,'lit');}).join(''));
        if(dusk.length) h+=(h?'<br>':'')+'🌇 <b>Sunset into lights:</b> '+dusk.map(function(t){return span(t,'dusk');}).join('');
      }
      el.innerHTML=h+src;
    });
  }
  var inp=document.getElementById('fbm-date'); if(!inp) return;
  var t=new Date(), iso=t.getFullYear()+'-'+('0'+(t.getMonth()+1)).slice(-2)+'-'+('0'+t.getDate()).slice(-2);
  inp.value=iso; inp.min=iso; render(iso);
  inp.addEventListener('change',function(){ if(inp.value) render(inp.value); });
})();
</script>"""

css = block("style", "cd-cards-css") + block("style", "cd-tested-css") + block("style", "cd-filters-css") + fbm_css
js = block("script", "cd-cards-js") + block("script", "cd-filters-js") + fbm_js
s = rep(s, "</head>", css + "</head>", where="css")
k = s.rfind("</body>")
s = s[:k] + js + s[k:]
s = rep(s, "<head>", '<head><meta name="robots" content="noindex,nofollow">', where="noindex")
open(OUT, "w", encoding="utf-8").write(s)
print("ok", OUT, len(s))
