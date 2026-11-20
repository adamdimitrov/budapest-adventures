# -*- coding: utf-8 -*-
"""Upgrade spec for best-things-to-do-budapest.html (scripts/listicle_upgrade.py).

A hub of 10 sights: each card features one bookable ticket (facts and ratings from
scripts/build_ttd_deck.py, read from each product page on 2026-11-13) and links to our own guide.
Pill, question and Pick/Skip text comes from the page's own write-up of each sight. No tested stamp.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PAGE = {
    "noun": "things to do",
    "filter_aria": "Filter things to do",
    "filters": [
        {"label": "Cost &amp; time", "chips": [("free", "🆓 Free"), ("paid", "🎟️ Paid tickets"), ("evening", "🌙 Evening"),
                                                ("indoor", "☔ Indoor / rainy day")]},
    ],
}

GYG = "https://www.getyourguide.com/budapest-l29/{}/?partner_id=YS414AJ&utm_medium=online_publisher&cmp=things-to-do-rating-{}&mkt_cmp=true"


def note(t):
    return f'<span class="bpa-lang-note">{t}</span>'


def P(emoji, label, pop, time=False):
    return {"cls": "bpa-lang bpa-time" if time else "bpa-lang", "emoji": emoji, "label": label, "pop_html": pop}


def gyg_rating(score, count, total, path, cmp, product):
    return {"stars": score, "score": score, "meta": f"{total} reviews · 1 site",
            "heading": f"Rating of the featured ticket: {product}",
            "sites": [{"kind": "link", "site": "GetYourGuide", "score": score, "count": f"({count})",
                       "url": GYG.format(path, cmp), "rel": "noopener nofollow sponsored", "target": "_blank"}]}


def B(pick, skip):
    return {"pick_html": pick, "skip_html": skip}


# Legenda's sightseeing cruise: the same 3-site rating the river cruise page shows for that ticket.
_river = json.load(open(os.path.join(ROOT, "data", "listicles", "best-budapest-river-cruises.json"), encoding="utf-8"))
LEGENDA = dict(_river["cards"][0]["reviews"]["ratings"])
LEGENDA["sites"] = [dict(x, kind="static") for x in LEGENDA["sites"]]   # books direct with Legenda: entries unlinked
for _x in LEGENDA["sites"]:
    for _k in ("url", "rel", "target"):
        _x.pop(_k, None)

CARDS = {
    "card-1": {
        "ratings": LEGENDA, "drop_extras": True, "via": "Booked direct with Legenda",
        "sublink": {"url": "/best-budapest-river-cruises", "text": "Compare 10 river cruises →"},
        "pills": [
            P("💶", "From €20", "<strong>Legenda's sightseeing cruise</strong> with an audio guide and a welcome drink, day or night sailings."),
            P("⏱️", "About 1 hour", "<strong>About an hour on the water</strong> past the Parliament, Buda Castle and Fisherman's Bastion.", True),
            P("📍", "Danube, between Buda &amp; Pest", "<strong>Boats leave from the Danube Promenade</strong> on the Pest side."
              + note("Many cruises add dinner or live music; a basic sightseeing cruise is enough.")),
        ],
        "best_for": B("for your first evening: after dark the Parliament, Buda Castle and the bridges are lit up and reflected in the river.",
                      "if you'd rather stay on land: the hop-on hop-off buses cover both banks, and the two big ones include a boat ride."),
        "faq": [
            ("Day or night?", "After dark, when the city is lit up and the lights reflect on the river."),
            ("What will I see?", "The Parliament, Buda Castle and Fisherman's Bastion from the water."),
            ("Do I need a dinner cruise?", "No. Many cruises offer dinner or live music, but a basic sightseeing cruise is enough to enjoy the views."),
            ("How much is it?", "From €20 for Legenda's sightseeing cruise with an audio guide and a welcome drink."),
            ("Which cruise should I book?", 'Compare them in our <a href="/best-budapest-river-cruises">10 best Danube cruises</a>.'),
        ],
        "price": {"sub": "per adult", "rows": [{"label": "Sightseeing cruise", "small": "day or night", "price": "€20"}]},
    },
    "card-2": {
        "ratings": gyg_rating("4.3", "29.2k", "29.2k", "szechenyi-spa-full-day-entrance-pass-t4139", "szechenyi",
                              "Széchenyi Spa Tickets with Optional Upgrades"),
        "drop_extras": True, "via": "Booked securely via GetYourGuide",
        "sublink": {"url": "/thermal-baths-budapest", "text": "Compare the thermal baths →"},
        "pills": [
            P("💶", "From €39", "<strong>Full-day spa ticket</strong> with optional upgrades."),
            P("⏱️", "2–3 hours", "<strong>Plan 2 to 3 hours</strong> for the outdoor pools and the indoor halls.", True),
            P("📍", "City Park, Pest", "<strong>In City Park</strong>, next to Vajdahunyad Castle (#9)."),
        ],
        "best_for": B("for the classic Budapest bath after a day of sightseeing: 18 indoor and outdoor pools fed by natural hot springs.",
                      "if you want a quiet, small bath: compare the other thermal baths first."),
        "faq": [
            ("How many pools are there?", "18, indoor and outdoor, fed by natural hot springs."),
            ("When should I go?", "After a day of sightseeing, when a long soak feels best."),
            ("What should I not miss?", "The outdoor pools, where locals play chess while they bathe."),
            ("How much is it?", "From €39 for a full-day spa ticket."),
            ("What is nearby?", "Vajdahunyad Castle, in the same City Park."),
        ],
        "price": {"sub": "full-day spa ticket", "rows": [{"label": "Full-day ticket", "price": "€39"}]},
    },
    "card-3": {
        "ratings": gyg_rating("4.5", "6.6k", "6.6k", "budapest-parliament-tour-with-audio-guide-opt-boat-tour-t731430", "parliament",
                              "Parliament Entry Ticket and Audio Guide"),
        "drop_extras": True,
        "sublink": {"url": "/budapest-parliament-tickets", "text": "Parliament tickets &amp; tips →"},
        "pills": [
            P("💶", "From HUF 7,000", "<strong>Official price for an EU/EEA adult.</strong>" + note("An entry ticket with audio guide is €43 online.")),
            P("⏱️", "About 45 minutes", "<strong>About 45 minutes</strong> inside with a guide.", True),
            P("📍", "Kossuth Square, Pest", "<strong>On Kossuth Square</strong>, by the Danube on the Pest side."),
        ],
        "best_for": B("for the Crown Jewels up close and the marble and gold halls of Hungary's neo-Gothic Parliament.",
                      "if you can't book ahead: guided tours often sell out."),
        "faq": [
            ("Do I need to book ahead?", "Yes. Guided tours often sell out, so book your tickets ahead of time."),
            ("What will I see inside?", "The Hungarian Crown Jewels, marble halls and gold decorations."),
            ("How long is the tour?", "About 45 minutes."),
            ("How much is it?", "From HUF 7,000 at the official EU/EEA adult price; an entry ticket with audio guide is €43 online."),
            ("Where is it?", 'On Kossuth Square, Pest. See our <a href="/budapest-parliament-tickets">Parliament tickets guide</a>.'),
        ],
        "price": {"sub": "official price, EU/EEA adult",
                  "rows": [{"label": "Official guided tour", "small": "EU/EEA adult", "price": "HUF 7,000"},
                           {"label": "Entry + audio guide", "small": "online", "price": "€43"}]},
    },
    "card-4": {
        "ratings": gyg_rating("4.7", "228", "228", "buda-castle-hill-tour-fisherman-s-bastion-matthias-church-t1320374", "bastion",
                              "Castle Hill Tour: Fisherman's Bastion &amp; Matthias Church"),
        "drop_extras": True, "via": "Booked securely via GetYourGuide",
        "sublink": {"url": "/best-walking-tours-budapest", "text": "Compare walking tours →"},
        "pills": [
            P("💶", "Free (upper towers paid)", "<strong>The lower terraces are free</strong>; the upper towers charge a fee."
              + note("A guided Castle Hill tour with Matthias Church starts from €39.")),
            P("⏱️", "30–60 minutes", "<strong>30 to 60 minutes</strong> for the terraces and photos.", True),
            P("📍", "Castle District, Buda", "<strong>Seven towers for the seven Magyar tribes</strong>, on Castle Hill."),
        ],
        "best_for": B("for the best panorama in Budapest: the Danube, the Parliament, St. Stephen's Basilica and the Chain Bridge.",
                      "in the middle of the day: go early in the morning or in the evening, when it is less crowded."),
        "faq": [
            ("Is it free?", "The lower terraces are free; the upper towers charge a fee."),
            ("When should I go?", "Early in the morning or in the evening, when it is less crowded."),
            ("What can I see from it?", "The Danube, the Parliament, St. Stephen's Basilica and the Chain Bridge."),
            ("Why seven towers?", "They represent the seven Magyar tribes."),
            ("Is there a guided tour?", "Yes: a Castle Hill tour of Fisherman's Bastion and Matthias Church from €39."),
        ],
        "price": {"sub": "guided tour from €39",
                  "rows": [{"label": "Lower terraces", "price": "Free"}, {"label": "Guided Castle Hill tour", "price": "€39"}]},
    },
    "card-5": {
        "ratings": gyg_rating("4.6", "2.4k", "2.4k", "budapest-classic-buda-castle-walking-tour-t157275", "castle",
                              "Buda Castle District Walking Tour"),
        "drop_extras": True, "via": "Booked securely via GetYourGuide",
        "sublink": {"url": "/best-walking-tours-budapest", "text": "Compare walking tours →"},
        "pills": [
            P("💶", "Free to walk", "<strong>Walking the district costs nothing.</strong>" + note("A guided walk starts from €12.")),
            P("⏱️", "Half a day", "<strong>Half a day</strong> with museums and cafés along the way.", True),
            P("📍", "Buda Castle Hill", "<strong>Buda Castle, Matthias Church and Fisherman's Bastion</strong> on cobblestone streets."),
        ],
        "best_for": B("for half a day of history on cobblestone streets, with Buda Castle, Matthias Church and Fisherman's Bastion in one walk.",
                      "if you want the stories behind it: a guided Castle District walk starts from €12."),
        "faq": [
            ("Is it free?", "Yes, walking around the Castle District costs nothing."),
            ("How long do I need?", "Half a day."),
            ("What will I see?", "Buda Castle, Matthias Church and Fisherman's Bastion, plus museums, cafés and views over the Danube and Pest."),
            ("What can I combine it with?", "Fisherman's Bastion, right next to Matthias Church."),
            ("Is there a guided walk?", "Yes, from €12."),
        ],
        "price": {"sub": "guided walk from €12",
                  "rows": [{"label": "On your own", "price": "Free"}, {"label": "Guided walk", "price": "€12"}]},
    },
    "card-6": {
        "ratings": gyg_rating("4.6", "15.8k", "15.8k", "budapest-st-stephen-s-basilica-entry-with-options-t655129", "basilica",
                              "St Stephen's Basilica Entry with Options"),
        "drop_extras": True, "via": "Booked securely via GetYourGuide",
        "pills": [
            P("💶", "From €12", "<strong>Church entry</strong>, with a dome option."),
            P("⏱️", "About 1 hour", "<strong>About an hour</strong>, including the dome climb.", True),
            P("📍", "District V, Pest", "<strong>In District V</strong>, named after Hungary's first king, St. Stephen."),
        ],
        "best_for": B("for the 360° view from the dome and Hungary's most sacred relic, St. Stephen's right hand.",
                      "if stairs are hard for you: the dome climb is 364 steps."),
        "faq": [
            ("How many steps to the dome?", "364, and the 360-degree view is worth every one."),
            ("What is the relic?", "St. Stephen's mummified right hand, Hungary's most sacred relic."),
            ("How much is it?", "From €12 for church entry, with a dome option."),
            ("Are there concerts?", "Yes, concerts are often held inside, and the acoustics are wonderful."),
            ("Who is it named after?", "St. Stephen, the first king of Hungary."),
        ],
        "price": {"sub": "church entry, dome option", "rows": [{"label": "Church entry", "small": "dome option", "price": "€12"}]},
    },
    "card-7": {
        "ratings": gyg_rating("4.8", "51.3k", "51.3k", "budapest-unlimited-prosecco-beer-and-aperol-spritz-cruise-t416276", "chain-bridge",
                              "Unlimited Prosecco Night Cruise"),
        "drop_extras": True, "via": "Booked securely via GetYourGuide",
        "sublink": {"url": "/best-night-cruises-budapest", "text": "Compare night cruises →"},
        "pills": [
            P("💶", "Free", "<strong>Walking across costs nothing.</strong>" + note("Seeing it from the water: a night cruise from €24.80.")),
            P("⏱️", "15–20 minutes", "<strong>A 15 to 20 minute walk</strong> from bank to bank.", True),
            P("📍", "Between Buda and Pest", "<strong>The first permanent bridge</strong> between Buda and Pest, guarded by stone lions."),
        ],
        "best_for": B("for a short walk with iconic views of Gellért Hill and both riverbanks, best at night when it is lit up.",
                      "if you only have daytime: the bridge and both banks look best after dark."),
        "faq": [
            ("Is it free?", "Yes, walking across costs nothing."),
            ("When should I go?", "At night, when the bridge is lit up and both sides of the city glow."),
            ("How long does it take?", "15 to 20 minutes."),
            ("Why is it famous?", "It was the first permanent bridge between Buda and Pest and remains a symbol of the city's unity."),
            ("Can I see it from the water?", "Yes: an unlimited prosecco night cruise passes it, from €24.80."),
        ],
        "price": {"sub": "night cruise from €24.80",
                  "rows": [{"label": "Walking across", "price": "Free"}, {"label": "Night cruise", "small": "unlimited prosecco", "price": "€24.80"}]},
    },
    "card-8": {
        "ratings": gyg_rating("4.9", "3.8k", "3.8k", "budapest-pub-crawl-ruin-bar-tour-free-shots-vip-entry-t1068003", "szimpla",
                              "Pub Crawl &amp; Ruin Bar Tour with Free Shots &amp; VIP Entry"),
        "drop_extras": True, "via": "Booked securely via GetYourGuide",
        "sublink": {"url": "/best-pub-crawls-budapest", "text": "Compare pub crawls →"},
        "pills": [
            P("💶", "Free entry", "<strong>No entry fee</strong>; you pay for your drinks." + note("A ruin bar pub crawl starts from €2.")),
            P("⏱️", "1–2 hours", "<strong>1 to 2 hours</strong>, best in the evening.", True),
            P("📍", "Jewish Quarter, District VII", "<strong>The original ruin pub</strong>, in an old abandoned building full of mismatched furniture."),
        ],
        "best_for": B("for the original ruin bar and a taste of Budapest's nightlife, best in the evening.",
                      "if you want a group to go out with: ruin bar pub crawls start from €2."),
        "faq": [
            ("Is entry free?", "Yes, you only pay for your drinks."),
            ("When should I go?", "In the evening."),
            ("What is a ruin pub?", "A bar set in an old, abandoned building, decorated with unique, mismatched furniture."),
            ("Is there a pub crawl?", 'Yes, from €2. Our <a href="/best-pub-crawls-budapest">pub crawl comparison</a> shows start times and which bars each visits.'),
            ("Where can I eat first?", "The Jewish Quarter food tour ends a few doors down on Kazinczy utca."),
        ],
        "price": {"sub": "ruin bar crawl from €2",
                  "rows": [{"label": "Entry", "price": "Free"}, {"label": "Pub crawl", "small": "from", "price": "€2"}]},
    },
    "card-9": {
        "ratings": {"meta": "🆓 Free grounds · nothing to book"},
        "drop_extras": True, "via": "Széchenyi Bath is next door",
        "sublink": {"url": "/thermal-baths-budapest", "text": "Compare the thermal baths →"},
        "pills": [
            P("💶", "Free grounds", "<strong>The grounds are free to walk.</strong>" + note("Széchenyi Bath next door: full-day ticket from €39.")),
            P("⏱️", "About 1 hour", "<strong>About an hour</strong> to explore the grounds.", True),
            P("📍", "City Park, Pest", "<strong>Built in 1896</strong> for the Millennial Exhibition, mixing Gothic, Renaissance and Baroque."),
        ],
        "best_for": B("for a relaxing hour in City Park, ideally paired with Széchenyi Bath next door.",
                      "if you want a real medieval castle: it was built in 1896 for an exhibition."),
        "faq": [
            ("Is it free?", "Yes, the grounds are free."),
            ("When was it built?", "In 1896, for Hungary's Millennial Exhibition."),
            ("What is there to do?", "Take a paddleboat on the pond in summer or ice skate on it in winter."),
            ("What can I combine it with?", "Széchenyi Bath, next door in City Park (full-day ticket from €39)."),
            ("What style is it?", "A mix of Gothic, Renaissance and Baroque."),
        ],
        "price": {"sub": "grounds are free",
                  "rows": [{"label": "Castle grounds", "price": "Free"}, {"label": "Széchenyi next door", "small": "full day", "price": "€39"}]},
    },
    "card-10": {
        "ratings": {"meta": "☕ No tickets needed"},
        "drop_extras": True,
        "sublink": {"url": "/budapest-travel-guide", "text": "Budapest travel guide →"},
        "pills": [
            P("💶", "Paid (pricey)", "<strong>The coffee is on the pricier side</strong>, but you pay for the room."),
            P("⏱️", "About 1 hour", "<strong>About an hour</strong> for a coffee and dessert.", True),
            P("📍", "Erzsébet körút, Pest", "<strong>Frescoed ceilings, marble columns, gold and chandeliers</strong>, like a royal palace."),
        ],
        "best_for": B("for a taste of luxury in what is known as the most beautiful café in the world.",
                      "if you want a bargain: the coffee is on the pricier side."),
        "faq": [
            ("Why go?", "For the atmosphere: it is known as the most beautiful café in the world."),
            ("Is it expensive?", "The coffee is on the pricier side, but worth it for the room alone."),
            ("How long should I stay?", "About an hour for a coffee and dessert."),
            ("Where is it?", "On Erzsébet körút in Pest."),
            ("What is it like inside?", "Frescoed ceilings, marble columns, gold accents and chandeliers."),
        ],
        "price": {"sub": "coffee and dessert", "note": "Pricier than most cafés; you pay for the atmosphere."},
    },
}

for _c in CARDS.values():
    _c.setdefault("price", {}).setdefault("note", "Prices from the featured ticket; the final price shows before you pay.")
