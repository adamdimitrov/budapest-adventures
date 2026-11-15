#!/usr/bin/env python3
"""Build /sparty-budapest (EN only) from the /thermal-baths-budapest shell.

Child page of the thermal baths hub, next to /szechenyi-baths-budapest and /rudas-baths-budapest.
Checked in Chrome on 15 November 2026:
  * GetYourGuide t386559 (Sparty): Basic with locker €73, Premium (2 drink coupons + recup) €100 for
    Sat 21 Nov 2026, 21:30; non-refundable; 18+; 4.15 (1,836). Next dates: 21, 28 Nov, 5, 12 Dec 2026.
  * spartybooking.com (official): Basic €69, Premium €85, Premium Plus €104, Express €135, VIP €199;
    1 beer = 1 coupon, 1 cocktail = 2 coupons.
  * GetYourGuide t1145839 (Széchenyi + Beer Spa): €125, 4.43 (104), free cancellation 24h, 18+, opens 10:00.
  * rudasfurdo.hu "Night above the city": Fri and Sat 22:00-3:00 (price 15,000 HUF, online, from the
    14 Nov hub check); Google Maps Rudas 4.3 (12,415).
Card renderers are reused from scripts/build_thermal_baths_2026.py. Run from the repo root:
    python3 scripts/build_sparty_page.py
"""
import copy
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SLUG = "sparty-budapest"
OUT = os.path.join(ROOT, SLUG + ".html")
SITE = "https://www.budapestadventures.com"
URL = SITE + "/" + SLUG
HUB = "/thermal-baths-budapest"
TODAY = "2026-11-15"
IMG = "/assets/sparty-2026/"
CHECK = "Checked on the booking calendar for Saturday 21 November 2026."
OFFICIAL_SPARTY = "https://spartybooking.com/"
RUDAS_NIGHT = "https://www.rudasfurdo.hu/en/offers/night-above-the-city"


def load_renderers():
    path = os.path.join(HERE, "build_thermal_baths_2026.py")
    with open(path, encoding="utf-8") as f:
        src = f.read()
    src = src.replace("""if 'id="item-2-rudas"' in SRC["page"]:""", "if False:")
    src = src.split('if __name__ == "__main__":')[0]
    ns = {"__file__": path, "__name__": "thermal_renderers"}
    exec(compile(src, path, "exec"), ns)
    return ns


R = load_renderers()
D = R["D"]
D.GYG = D.GYG.replace("cmp=en-thermal-baths-", "cmp=en-sparty-")
AFF_REL = R["AFF_REL"]
pill, maps_link = D.pill, D.maps_link
BASE = {c["key"]: c for c in D.CARDS}
_orig_buycard = R["buycard"]


def buycard(c):
    """Rudas night bathing is sold online on the official site, not at the desk."""
    html = _orig_buycard(c)
    if c.get("online_official"):
        html = (html.replace("Official Prices &amp; Opening Hours", "Official Online Tickets")
                .replace("See Official Prices", "See Night Bathing Tickets")
                .replace("No online booking: pay at the ticket desk", "Sold online on the official Rudas site")
                .replace("Sold only at the bath's ticket desk", "Online tickets only")
                .replace("Morning or afternoon session", "Friday and Saturday nights"))
    return html


R["buycard"] = buycard

SZ_ADDR = maps_link("Széchenyi Gyógyfürdő Állatkerti körút 9-11 Budapest", "Állatkerti körút 9-11, 1146 Budapest (Széchenyi Baths, City Park)")
SPARTY_PHOTOS = [IMG + p for p in ["sparty-szechenyi-night-01.avif", "sparty-lasers-02.avif", "sparty-stage-03.avif",
                                   "sparty-show-04.avif", "sparty-drinks-05.avif"]]
SPARTY_COMMON = dict(
    cat="sparty", tested=False, area="Széchenyi Baths, City Park", time="Sat 21:30–2:00", transport="M1 Széchenyi fürdő",
    maps_q="Széchenyi Gyógyfürdő Állatkerti körút 9-11 Budapest", book="gyg",
    gyg_slug="budapest-the-ultimate-late-night-spa-party-ticket-t386559",
    ratings=[("GetYourGuide", 4.1542, 1836, "gyg", None)], via="GetYourGuide", alt="Sparty pool party at the Széchenyi Baths",
    getthere=["📍 " + SZ_ADDR,
              "🚇 Take <strong>metro M1</strong> to <strong>Széchenyi fürdő</strong>, about 5 minutes from the city centre.",
              "🚕 Going home at 2:00: order a <strong>Bolt</strong> or an official taxi through an app. Guests report overpriced street taxis waiting at the exit."],
    quotes=[("Amazing party scene at the hot baths.", "GetYourGuide", "October 2026"),
            ("The fire show was brilliant", "GetYourGuide", "October 2026"),
            ("The drinks are very expensive though", "GetYourGuide", "June 2026")],
    amen=[("yes", "Outdoor Thermal Pools"), ("yes", "DJs &amp; Light Shows"), ("yes", "Bars"), ("yes", "Locker"),
          ("no", "Non-Refundable"), ("no", "No Under-18s")],
)
WHEN_PILL = pill("🕒", "Saturdays · 21:30–2:00",
                 "<strong>Every Saturday</strong> from 21:30 to 2:00, last entry at 1:00. "
                 "<strong>Next dates:</strong> 21 and 28 November, 5 and 12 December 2026.", CHECK, "bpa-time")
PAY_PILL = pill("💳", "Bars: SpartyPay only",
                "The bars take <strong>SpartyPay cards only</strong>, no bank cards. The first top-up is <strong>20,000 HUF</strong>, "
                "including a 3,000 HUF card deposit, and you top up with cash. Drinks come in a reusable cup: 700 HUF, 350 HUF back when you return it.",
                "From the ticket listing, 15 November 2026.")
AGE_PILL = pill("🔞", "18+ · non-refundable",
                "Adults only (ID required). Sparty tickets cannot be cancelled or refunded, so book once your Saturday is fixed.", CHECK)


def qf_sparty(ticket_row):
    return [("Dates &amp; Times", "Every Saturday 21:30–2:00, last entry 1:00 · next: 21, 28 Nov, 5, 12 Dec 2026"),
            ("Ticket (this card)", ticket_row),
            ("Official Ticket Tiers", "Basic €69 · Premium €85 · Premium Plus €104 · Express €135 · VIP €199 (spartybooking.com, 21 Nov 2026)"),
            ("Drink Coupons", "1 beer = 1 coupon · 1 cocktail = 2 coupons"),
            ("Bar Payment", "SpartyPay card only, first top-up 20,000 HUF incl. 3,000 HUF deposit, top up with cash"),
            ("Pool Temperature", "34–38 °C outdoor thermal water"),
            ("Age Limit", "18+, ID required"),
            ("Cancellation", "Non-refundable"),
            ("Address", "Állatkerti körút 9-11, 1146 Budapest"),
            ("Nearest Transport", "Metro M1, Széchenyi fürdő")]


CARDS = []
CARDS.append(dict(SPARTY_COMMON,
    key="sparty-basic", anchor="item-1-sparty-basic", rank="🎉 #1 Best Value Sparty Ticket", color="bpa-gold",
    title="Sparty Basic Ticket (Entry + Locker)", short="Sparty Basic Ticket",
    price="73", psub="per adult · entry + locker", trust=["✓ Locker included", "✓ Live guidance in English"],
    photos=SPARTY_PHOTOS,
    pills=[WHEN_PILL,
           pill("🎟️", "Entry + locker",
                "<strong>Basic ticket, €73:</strong> Sparty entry and a wardrobe-type locker (120 × 30 × 65 cm). "
                "Towels and flip-flops are not included, and flip-flops are mandatory.", CHECK),
           PAY_PILL, AGE_PILL],
    pick="if you want the party and will buy your own drinks: <strong>entry plus a locker for €73</strong>, with DJs, lasers and fire shows around 34–38 °C outdoor pools.",
    skip="if your Saturday might change: the ticket is non-refundable. Pick Rudas night bathing on a Friday or the Beer Spa instead.",
    pros=[("Open-air pool party", "Techno, lasers, fire shows and circus artists around the outdoor pools of the Széchenyi Baths."),
          ("Warm water in winter", "The outdoor pools are 34–38 °C, so Sparty runs in November and December too."),
          ("Locker included", "A wardrobe-type locker comes with the ticket."),
          ("Easy to reach", "Metro M1 to Széchenyi fürdő, about 5 minutes from the centre.")],
    cons=[("Non-refundable", "No cancellation or refund on any Sparty ticket."),
          ("Pricey drinks", "Guests report cocktails at about 6,300 HUF, paid only by a SpartyPay card topped up with cash."),
          ("Deep pool", "The pool is about shoulder-deep, so dancing is easiest near the steps."),
          ("Bring your own kit", "Towels and flip-flops are not included.")],
    summary_q=("Is Sparty worth it?",
               "Yes, if you want one big night out in a thermal bath. Basic is the right ticket if you plan to drink more than a couple of beers."),
    summary=["Sparty turns the Széchenyi Baths into an open-air club every Saturday night: DJs, lasers, fire shows and circus artists "
             "around steaming 34–38 °C pools under the yellow palace. It runs from 21:30 to 2:00, and the last entry is at 1:00.",
             "The shows and the setting are the highlight. The two things to plan for are drink prices and the cash-only SpartyPay system."],
    spcards=[("The Party", IMG + "sparty-lasers-02.avif",
              "Techno, lasers and circus artists around the outdoor pools from 21:30 to 2:00. Last entry is at 1:00."),
             ("The Pools", IMG + "sparty-szechenyi-night-01.avif",
              "You party in the 34–38 °C outdoor thermal pools. They are about shoulder-deep, so the steps are the best place to dance."),
             ("Drinks &amp; SpartyPay", IMG + "sparty-drinks-05.avif",
              "Bars take SpartyPay cards only: first top-up 20,000 HUF (3,000 HUF deposit included), cash top-ups. Cups cost 700 HUF, 350 HUF back."),
             ("The Shows", IMG + "sparty-show-04.avif",
              "Costumed performers, fire shows and circus acts around the pools through the night. Bring swimwear, a towel, flip-flops and ID.")],
    qf=qf_sparty("Basic with locker, €73 (21 Nov 2026)"),
))
CARDS.append(dict(SPARTY_COMMON,
    key="sparty-premium", anchor="item-2-sparty-premium", rank="🍹 #2 Sparty With Drinks", color="bpa-silver",
    title="Sparty Premium Ticket (Entry + 2 Drinks)", short="Sparty Premium Ticket",
    price="100", psub="per adult · entry, locker, 2 drink coupons", trust=["✓ 2 drink coupons + cup", "✓ Locker included"],
    photos=[SPARTY_PHOTOS[4]] + SPARTY_PHOTOS[:4],
    pills=[WHEN_PILL,
           pill("🍹", "2 drink coupons",
                "<strong>Premium ticket, €100:</strong> entry, a locker, <strong>2 drink coupons</strong> and a reusable cup. "
                "1 beer = 1 coupon, 1 cocktail = 2 coupons.", CHECK),
           PAY_PILL, AGE_PILL],
    pick="if you only want a drink or two: the <strong>2 coupons (2 beers or 1 cocktail)</strong> mean you can skip loading 20,000 HUF onto a SpartyPay card.",
    skip="if you plan to drink more than two beers: you will need a SpartyPay card anyway, so Basic plus a top-up is simpler.",
    pros=[("Drinks sorted", "2 coupons and a reusable cup are included, so you can go straight to the bar."),
          ("No card top-up for light drinkers", "Two beers or one cocktail without loading 20,000 HUF onto a SpartyPay card."),
          ("Same party", "Same entry, locker, pools and shows as the Basic ticket.")],
    cons=[("Non-refundable", "No cancellation or refund on any Sparty ticket."),
          ("Coupons go fast", "A cocktail costs 2 coupons, so the coupons cover one cocktail."),
          ("€27 more than Basic", "Worth it only if the coupons replace a card top-up you would not otherwise use.")],
    summary_q=("Is the Sparty Premium ticket worth it?",
               "Only for light drinkers. The coupons cover 2 beers or 1 cocktail; anyone drinking more needs a SpartyPay card anyway."),
    summary=["Premium is the same night as Basic: entry, a locker, the pools and the shows. The difference is 2 drink coupons and a reusable cup.",
             "The coupons are the cheapest way to have one or two drinks, because the bars otherwise ask for a SpartyPay card with a first top-up of 20,000 HUF."],
    spcards=[("Drink Coupons", IMG + "sparty-drinks-05.avif",
              "2 coupons and a reusable cup. 1 beer = 1 coupon, 1 cocktail = 2 coupons."),
             ("The Party", IMG + "sparty-stage-03.avif",
              "DJs, lasers, fire shows and circus artists around the outdoor pools from 21:30 to 2:00."),
             ("The Pools", IMG + "sparty-szechenyi-night-01.avif",
              "34–38 °C outdoor thermal pools in front of the lit-up palace. Bring swimwear, a towel, flip-flops and ID.")],
    qf=qf_sparty("Premium: entry, locker, 2 drink coupons, cup, €100 (21 Nov 2026)"),
))

rudas = copy.deepcopy(BASE["rudas"])
CARDS.append(dict(
    key="rudas-night", anchor="item-3-rudas-night", cat="", tested=False,
    rank="🌙 #3 Best Late-Night Soak", color="bpa-bronze",
    area="Elizabeth Bridge, Buda", time="Fri &amp; Sat 22:00–3:00", transport="Tram 19, 41 · Bus 7",
    maps_q="Rudas Gyógyfürdő Döbrentei tér 9 Budapest",
    title="Rudas Night Bathing", short="Rudas Night Bathing",
    book="official", online_official=True, official_url=RUDAS_NIGHT,
    ratings=[("Google", 4.2846, 12415, "google", D.MAPS.format(q="Rudas+Gy%C3%B3gyf%C3%BCrd%C5%91+D%C3%B6brentei+t%C3%A9r+9+Budapest"))],
    price=None, price_label="15,000 HUF", price_huf="15000", psub="per adult · online ticket",
    via="rudasfurdo.hu (online only)", trust=["✓ Open until 3:00", "✓ Fridays and Saturdays"],
    photos=rudas["photos"], alt="Rudas Thermal Bath",
    pills=[pill("🕒", "Fri &amp; Sat · 22:00–3:00",
                "<strong>Every Friday and Saturday night</strong> from 22:00 to 3:00, with mixed bathing.",
                "From rudasfurdo.hu, 15 November 2026.", "bpa-time"),
           pill("🏛️", "Turkish bath + rooftop bar",
                "The 450-year-old <strong>Turkish bath</strong> with six pools at different temperatures, the swimming pool, "
                "the wellness area and a <strong>cocktail bar on the roof</strong>.", "From rudasfurdo.hu."),
           pill("🎟️", "15,000 HUF online",
                "Night bathing tickets cost <strong>15,000 HUF</strong> and are sold online only on rudasfurdo.hu.",
                "Checked on the official site on 14 November 2026."),
           pill("🔞", "14+ · not step-free",
                "Children under 14 are not admitted. The bath currently cannot receive guests with reduced mobility.", "From rudasfurdo.hu.")],
    pick="if you want a late soak without the party: the <strong>Ottoman Turkish bath until 3:00</strong> with a cocktail bar on the roof, on Fridays as well as Saturdays.",
    skip="if you want DJs and a crowd: it is a bath night, not a pool party.",
    pros=[("Friday option", "Open on Friday and Saturday nights, so it works when Sparty does not."),
          ("Historic setting", "The 450-year-old Turkish bath with pools at six temperatures."),
          ("Rooftop cocktail bar", "A bar on the roof above the Danube."),
          ("Cheaper than Sparty", "15,000 HUF online, about the price of a Basic Sparty ticket.")],
    cons=[("No party", "No DJs or shows; it is a calm night soak."),
          ("Online only", "Night tickets are sold on rudasfurdo.hu, not at the desk."),
          ("Not for everyone", "No children under 14 and no step-free access.")],
    summary_q=("Is Rudas night bathing a good Sparty alternative?",
               "Yes, if you want the night-time bath without the club. It also runs on Fridays."),
    summary=["Rudas opens its Turkish bath, swimming pool and wellness area every Friday and Saturday night from 22:00 to 3:00, "
             "with a cocktail bar on the roof. It is the calm, grown-up version of a night at the baths.",
             "I have bathed at Rudas myself in the daytime; the rooftop pool looks straight over the Danube."],
    quotes=rudas["quotes"][:2], getthere=rudas["getthere"], spcards=rudas["spcards"][:3],
    qf=[("Night Bathing", "Fri and Sat 22:00–3:00, mixed (rudasfurdo.hu, 15 Nov 2026)"),
        ("Price", "15,000 HUF, online only (checked 14 Nov 2026)"),
        ("What Is Open", "Turkish bath, swimming pool, wellness area, rooftop cocktail bar"),
        ("Age Limit", "14+"),
        ("Address", "Döbrentei tér 9, 1013 Budapest"),
        ("After Midnight", "Night buses 907 and 973")],
    amen=[("yes", "Turkish Bath"), ("yes", "Swimming Pool"), ("yes", "Rooftop Bar"), ("yes", "Thermal Water"),
          ("no", "No Children Under 14"), ("no", "Not Wheelchair Accessible")],
))

BEER = [IMG + p for p in ["beer-spa-tub-01.avif", "beer-spa-tap-02.avif", "beer-spa-room-03.avif", "beer-spa-szechenyi-04.avif"]]
CARDS.append(dict(
    key="beer-spa", anchor="item-4-beer-spa", cat="", tested=False,
    rank="🍺 #4 Best Daytime Alternative", color="bpa-slate",
    area="Széchenyi Baths, City Park", time="3 Hours", transport="M1 Széchenyi fürdő",
    maps_q="Széchenyi Gyógyfürdő Kós Károly sétány 1 Budapest",
    title="Széchenyi Bath Ticket + Beer Spa", short="Széchenyi + Beer Spa",
    book="gyg", gyg_slug="beer-spa-with-optional-szechenyi-bath-tickets-t1145839",
    ratings=[("GetYourGuide", 4.43, 104, "gyg", None)],
    price="125", psub="per adult · bath + 45-min beer spa", via="GetYourGuide",
    trust=["✓ Free cancellation up to 24 hours before", "✓ Reserve now, pay later"],
    photos=BEER, alt="Beer Spa at the Széchenyi Baths",
    pills=[pill("🍺", "Unlimited draught beer",
                "A <strong>45-minute private beer spa soak</strong> in a wooden tub with <strong>unlimited Hungarian draught beer</strong> "
                "from your own tap, plus a <strong>full-day fast-track Széchenyi ticket</strong> and a private changing cabin.", CHECK),
           pill("🕒", "From 10:00 · 3 hours",
                "The Beer Spa opens at 10:00; arrive 20 minutes before your slot. Plan about 3 hours with the bath.", CHECK, "bpa-time"),
           pill("✅", "Free cancellation",
                "Free cancellation up to 24 hours before, and you can reserve now and pay later.", CHECK),
           pill("🔞", "18+",
                "Adults only. Towels cost 5,000 HUF on site; bring your own slippers.", CHECK)],
    pick="if Saturday night does not fit or you want a refundable booking: <strong>a full day at Széchenyi plus 45 minutes of unlimited beer</strong> in a private tub.",
    skip="if you want a night out: the Beer Spa opens at 10:00 and it is a private tub, not a party.",
    pros=[("Unlimited beer", "Self-poured draught beer from your own tap for 45 minutes."),
          ("Full day at Széchenyi", "A fast-track day ticket and a private changing cabin are included."),
          ("Flexible", "Free cancellation up to 24 hours before.")],
    cons=[("Daytime only", "Opens at 10:00; no night sessions on this ticket."),
          ("Pricey", "€125, more than a Sparty ticket."),
          ("Extras cost more", "Towels are 5,000 HUF on site; bring your own slippers.")],
    summary_q=("Is the Beer Spa a good alternative to Sparty?",
               "Yes, for a fun daytime version with drinks included and free cancellation. It is not a party."),
    summary=["The Beer Spa combines a full-day fast-track Széchenyi ticket with a 45-minute private soak in a wooden tub of thermal water "
             "infused with hops and malt, with unlimited draught beer from your own copper tap.",
             "It is a relaxed, fun soak rather than a party, and it ends with the rest of the day free in the Széchenyi pools."],
    quotes=[("the beer spa was very calming and it was fun to have draft beer on tap right next to us", "GetYourGuide", "October 2026")],
    getthere=["📍 " + maps_link("Széchenyi Gyógyfürdő Kós Károly sétány 1 Budapest", "Széchenyi main entrance (Gate 1), Kós Károly sétány 1, 1146 Budapest"),
              "🚇 Take <strong>metro M1</strong> to <strong>Széchenyi fürdő</strong>.",
              "➡️ Inside the main hall, turn left into the corridor to the Beer Spa reception; skip the information desk."],
    spcards=[("Beer Tub", IMG + "beer-spa-tub-01.avif", "A 45-minute soak in a handcrafted wooden tub of thermal water with hops, malt and beer salts."),
             ("Your Own Tap", IMG + "beer-spa-tap-02.avif", "Unlimited Hungarian draught beer from a copper tap next to your tub."),
             ("Széchenyi All Day", IMG + "beer-spa-szechenyi-04.avif", "A full-day fast-track entry to the Széchenyi Baths is included.")],
    qf=[("Ticket", "Full-day fast-track Széchenyi entry + 45-min private beer spa + unlimited draught beer + private cabin, €125"),
        ("Opening", "From 10:00, arrive 20 minutes early"),
        ("Cancellation", "Free up to 24 hours before"),
        ("Age Limit", "18+"),
        ("Towels", "Not included, 5,000 HUF on site"),
        ("Meeting Point", "Széchenyi main entrance, Gate 1, Kós Károly sétány 1")],
    amen=[("yes", "Unlimited Beer"), ("yes", "Private Cabin"), ("yes", "Thermal Water"), ("yes", "Free Cancellation"),
          ("no", "Daytime Only"), ("no", "No Under-18s")],
))

N = len(CARDS)
N_SPARTY = sum(c["cat"] == "sparty" for c in CARDS)
SPARTY_URL = R["amp"](D.GYG.format(slug=CARDS[0]["gyg_slug"], placement="intro", key="sparty"))

def live(slug):
    """Link only to pages that exist in this checkout (main + this branch)."""
    return os.path.exists(os.path.join(ROOT, slug + ".html"))


def join_links(items):
    items = ['<a href="/%s">%s</a>' % (slug, text) for slug, text in items if live(slug)]
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + " or " + items[-1]


BATH_LINKS = join_links([("szechenyi-baths-budapest", "Széchenyi Baths guide"), ("rudas-baths-budapest", "Rudas Baths guide"),
                         (HUB.strip("/"), "best thermal baths in Budapest")])
NIGHT_LINKS = join_links([("best-night-cruises-budapest", "best night cruises in Budapest"),
                          ("best-pub-crawls-budapest", "best pub crawls in Budapest"),
                          ("best-food-tours-budapest", "best food tours in Budapest")])


# ── copy ─────────────────────────────────────────────────────────────────────────────
TITLE = "Sparty Budapest 2026: Tickets, Prices &amp; What to Know Before You Go"
TITLE_TXT = "Sparty Budapest 2026: Tickets, Prices & What to Know Before You Go"
DESC = ("Sparty is the Saturday night pool party at Budapest's Széchenyi Baths. Ticket prices, what each ticket includes, "
        "how paying for drinks works and next dates, checked 15 Nov 2026.")
H1 = 'Sparty Budapest: Tickets, Prices &amp; Tips <span class="ltt-h1-muted">(2026)</span>'

LEAD = f'''<div class="ltt-lead-copy">
<p><strong>Sparty</strong> turns the Széchenyi Baths into an open-air club every Saturday from <strong>21:30 to 2:00</strong>: DJs, lasers and fire shows around 34–38 °C pools. What catches first-timers out is not the ticket but the bar: drinks are paid only with a <strong>SpartyPay card topped up in cash</strong>, and every ticket is <strong>non-refundable</strong>.</p>
<p>Below are the <strong>two Sparty tickets</strong> compared on what you actually get for the money, plus two alternatives if Saturday does not work: <strong>Rudas night bathing</strong> (Fridays too, until 3:00) and the <strong>Széchenyi Beer Spa</strong>. Next Sparty nights: <strong>21 and 28 November, 5 and 12 December 2026</strong>.</p>
<p>Planning a daytime soak? See the {BATH_LINKS}. Making a night of it? Start with the {NIGHT_LINKS}.</p>
</div>'''

PILLS = f'''<div class="ltt-integrated-pills">
<button class="ltt-tab-btn active" data-cat="all" onclick="lttFilterItems('all', this)" type="button">All ({N})</button>
<button class="ltt-tab-btn" data-cat="sparty" onclick="lttFilterItems('sparty', this)" type="button">Sparty Tickets ({N_SPARTY})</button>
</div>'''

C1, C2, C3, C4 = CARDS
MID = f'''<div class="container w-container"><h2 id="sparty-quick-picks">Quick Picks: Which Ticket Is Right for You</h2>
<div class="w-richtext"><ul role="list">
<li>🎉 <strong>You want the party and will drink a few:</strong> <a href="#{C1["anchor"]}">Sparty Basic</a>, €73, then top up a SpartyPay card at the bar.</li>
<li>🍹 <strong>You want one cocktail or two beers:</strong> <a href="#{C2["anchor"]}">Sparty Premium</a>, €100, coupons included.</li>
<li>🌙 <strong>You are free on Friday, or want a calm night soak:</strong> <a href="#{C3["anchor"]}">Rudas night bathing</a>, 22:00–3:00.</li>
<li>🍺 <strong>You want drinks in the water but need a refundable booking:</strong> <a href="#{C4["anchor"]}">Széchenyi + Beer Spa</a>, daytime.</li>
</ul></div>
<h2 id="sparty-at-a-glance">Sparty at a Glance</h2>
<div class="w-richtext"><ul role="list">
<li>📅 <strong>When:</strong> every Saturday, 21:30–2:00, last entry 1:00. Next dates: 21 and 28 November, 5 and 12 December 2026.</li>
<li>📍 <strong>Where:</strong> the outdoor pools of the Széchenyi Baths, Állatkerti körút 9-11, metro M1 Széchenyi fürdő.</li>
<li>🎟️ <strong>Tickets:</strong> <a href="{SPARTY_URL}" rel="{AFF_REL}" target="_blank">Basic €73 or Premium €100</a>; the official site also sells Express and VIP tickets (up to €199).</li>
<li>💳 <strong>Drinks:</strong> SpartyPay card only, first top-up 20,000 HUF including a 3,000 HUF deposit, top-ups in cash. 1 beer = 1 coupon, 1 cocktail = 2 coupons.</li>
<li>🔞 <strong>Rules:</strong> 18+ with ID, flip-flops mandatory, no refunds.</li>
</ul></div></div>'''

GUIDE = f'''<div class="container w-container"><h2 id="sparty-tips">Sparty Tips: Before You Go</h2><div class="w-richtext">
<h3>Pick the Right Ticket</h3><p>Basic (€73) and Premium (€100) get you into the same party with a locker. Premium adds 2 drink coupons and a cup, which covers 2 beers or 1 cocktail. The official site sells the same tiers a little cheaper (Basic €69, Premium €85) plus Premium Plus (€104, 3 coupons), Express (€135, fast entry and a cabin) and VIP (€199, VIP bar and area).</p>
<h3>Bring Cash for the Bar</h3><p>No bank cards at the bars. Get a SpartyPay card first (first top-up 20,000 HUF, including a 3,000 HUF deposit) and top it up with cash. Drinks come in a reusable cup: 700 HUF, 350 HUF back when you return it.</p>
<h3>What to Bring</h3><p>Swimwear, a towel, flip-flops (mandatory) and a passport or ID card. Food, drinks, large bags and glass are not allowed.</p>
<h3>Getting Home</h3><p>Metro M1 stops running before 2:00, so plan a ride back. Order a Bolt or an official taxi through an app; guests report overpriced street taxis at the exit.</p>
<h3>No Refunds</h3><p>All Sparty tickets are non-refundable. If your Saturday is not fixed yet, Rudas night bathing (Fridays and Saturdays) or the Beer Spa (free cancellation) are safer bookings.</p>
</div>
<h2 id="sparty-how-we-checked">How We Checked</h2><div class="w-richtext">
<p>Ticket options, prices, dates and rules were checked on the booking calendar for Saturday 21 November 2026 and on the official Sparty site on 15 November 2026. Rudas night bathing hours were checked on rudasfurdo.hu the same day. I have bathed at Széchenyi and Rudas in person.</p>
<p>More guides: the {BATH_LINKS}, and for the rest of your night the {NIGHT_LINKS}.</p>
</div>'''

FAQ = [
    ("When is Sparty in Budapest?",
     "Every Saturday from 21:30 to 2:00 at the Széchenyi Baths, with last entry at 1:00. The next dates are 21 and 28 November and 5 and 12 December 2026."),
    ("How much are Sparty tickets?",
     "The Basic ticket with a locker is €73 and the Premium ticket with 2 drink coupons is €100 on the booking calendar for 21 November 2026. The official site sells Basic from €69 and VIP up to €199."),
    ("Can you get a refund on Sparty tickets?",
     "No. Sparty tickets are non-refundable. For a refundable option, book the Széchenyi Beer Spa, which has free cancellation up to 24 hours before."),
    ("How do you pay for drinks at Sparty?",
     "Only with a SpartyPay card. The first top-up is 20,000 HUF including a 3,000 HUF deposit, and you top up with cash; bank cards are not accepted at the bars."),
    ("What is the age limit for Sparty?",
     "18. Bring a passport or ID card."),
    ("Is there a night bath party on Fridays?",
     "Sparty is Saturdays only. On Fridays, Rudas has night bathing from 22:00 to 3:00, and Széchenyi is open until 22:00."),
]


def faq_html():
    cards = []
    for k, (q, ans) in enumerate(FAQ):
        first = " first" if k == 0 else ""
        cards.append('<div class="cf-faq-plus-card"><div class="cf-faq-question-container-3%s"><div class="cf-faq-question-wrap">'
                     '<h3 class="cf-faq-questions-2">%s</h3><div class="cf-faq-icon-contain"><div class="cf-faq-line"></div>'
                     '<div class="cf-faq-line-vertical"></div></div></div></div><div class="cf-faq-answer-wrap-2">'
                     '<div class="cf-faq-content-2 w-richtext"><p>%s</p></div></div><div class="cf-bottom-line-2"></div></div>' % (first, q, ans))
    return '<div class="cf-faqs-container">%s</div>' % "".join(cards)


must_sub, swap_block, no_em_dash = R["must_sub"], R["swap_block"], R["no_em_dash"]
all_spans = R["all_spans"]


def head(page):
    page = must_sub(r"<title>.*?</title>", "<title>%s</title>" % TITLE, page, flags=re.S)
    for prop in ('property="og:title"', 'name="twitter:title"'):
        page = must_sub(r'<meta content="[^"]*" %s/>' % prop, '<meta content="%s" %s/>' % (TITLE, prop), page)
    for prop in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        page = must_sub(r'<meta content="[^"]*" %s/>' % prop, '<meta content="%s" %s/>' % (DESC, prop), page)
    for prop in ('property="og:image"', 'name="twitter:image"'):
        page = must_sub(r'<meta content="[^"]*" %s/>' % prop, '<meta content="%s%s" %s/>' % (SITE, SPARTY_PHOTOS[0], prop), page)
    page = must_sub(r'<meta content="[^"]*" property="og:url"/>', '<meta content="%s" property="og:url"/>' % URL, page)
    page = must_sub(r'<link href="[^"]*" rel="canonical"/>', '<link href="%s" rel="canonical"/>' % URL, page)
    page = re.sub(r'(<meta content=")[^"]*(" property="article:modified_time"/>)', r"\g<1>%sT00:00:00+00:00\2" % TODAY, page)
    page = re.sub(r'(<meta content=")[^"]*(" property="article:published_time"/>)', r"\g<1>%sT00:00:00+00:00\2" % TODAY, page)
    page = must_sub(r'<link as="image" fetchpriority="high" href="[^"]*"[^>]*rel="preload"[^>]*/>',
                    '<link as="image" fetchpriority="high" href="%s" rel="preload" type="image/avif"/>' % CARDS[0]["photos"][0], page)
    links = re.findall(r'<link href="[^"]*" hreflang="[^"]*" rel="alternate"/>', page)
    assert links, "no hreflang links"
    first = page.find(links[0])
    for l in links:
        page = page.replace(l, "", 1)
    en = '<link href="%s" hreflang="en" rel="alternate"/><link href="%s" hreflang="x-default" rel="alternate"/>' % (URL, URL)
    page = page[:first] + en + page[first:]
    page = must_sub(r"<script>const alternativeLanguagePages = .*?</script>",
                    "<script>const alternativeLanguagePages = %s</script>" % json.dumps({"en": URL}), page, flags=re.S)
    routes = [{"url": URL, "hreflang": "default", "isDefault": True, "subfolder": "", "langCode": "en"}]
    page = must_sub(r"<script>const LINGUANA_LANGUAGE_ROUTES = .*?</script>",
                    "<script>const LINGUANA_LANGUAGE_ROUTES = %s</script>" % json.dumps(routes), page, flags=re.S)
    return page


def hero(page):
    crumbs = ('<a href="/">Home</a>\n<span class="ltt-bc-sep">›</span>\n<a href="%s">Thermal Baths</a>\n'
              '<span class="ltt-bc-sep">›</span>\n<span class="ltt-bc-current">Sparty</span>' % HUB)
    page = must_sub(r'<a href="/">Home</a>\s*<span class="ltt-bc-sep">›</span>\s*<span class="ltt-bc-current">[^<]*</span>', crumbs, page)
    page = must_sub(r'<span class="ltt-hero-kicker-badge">[^<]*</span>', '<span class="ltt-hero-kicker-badge">Dates &amp; Prices Checked 15 Nov 2026</span>', page)
    page = must_sub(r'(<h1 class="ltt-editorial-h1">).*?(</h1>)', r"\1\n      %s\n\2" % H1, page, flags=re.S)
    page = must_sub(r'<div class="ltt-author-role">[^<]*</div>',
                    '<div class="ltt-author-role">Budapest Local • Sparty Tickets &amp; 2 Alternatives Compared • Checked 15 Nov 2026</div>', page)
    page = must_sub(r"<strong>Last updated</strong>: [^<]*<", "<strong>Last updated</strong>: Nov 15, 2026<", page)
    page = swap_block(page, r'<div class="ltt-lead-copy">', LEAD)
    page = swap_block(page, r'<div class="ltt-integrated-pills">', PILLS)
    return page


def body(page):
    deck = no_em_dash("\n".join(R["deck_html"](i, c) for i, c in enumerate(CARDS, 1)))
    dets = no_em_dash("".join(R["details_html"](i, c) for i, c in enumerate(CARDS, 1)))
    cs = all_spans(page, "card")
    page = page[:cs[0][0]] + deck + page[cs[-1][1]:]
    ds = all_spans(page, "details")
    page = page[:ds[0][0]] + dets + page[ds[-1][1]:]
    page = re.sub(r"<!-- #\d+: [^>]*-->\n?", "", page)
    page = re.sub(r"<blockquote><strong>What visitors say:</strong>.*?</blockquote>", "", page, flags=re.S)  # no review quotes
    page = swap_block(page, r'<div class="container w-container"><div class="w-richtext"><p>Every bath below', MID)
    page = must_sub(r'(<h2 class="bpa-breakdown-heading" id="desert-safaris-breakdown">)[^<]*(</h2>)',
                    r"\1Detailed Breakdown: Sparty Tickets &amp; Alternatives\2", page)
    page = must_sub(r'<p class="bpa-breakdown-sub">[^<]*</p>',
                    '<p class="bpa-breakdown-sub">%d options compared • All reviews open by default • Click to collapse/expand</p>' % N, page)
    a_ = page.find('<div class="container w-container"><h2 id="thermal-baths-know-before-you-go">')
    b_ = page.find('<div class="cf-faq-container" id="faq">')
    assert 0 < a_ < b_
    page = page[:a_] + GUIDE + page[b_:]
    page = swap_block(page, r'<div class="cf-faqs-container">', faq_html())
    return page


def chrome(page):
    cfg = {"deckId": "budapest-thermal-baths-deck", "tocDeckLabel": "Sparty Tickets Compared",
           "tocBreakdownLabel": "Detailed Breakdown (%d Options)" % N, "shortTitles": [c["short"] for c in CARDS]}
    page = must_sub(r"window\.LTT_PAGE_CONFIG = \{.*?\};", "window.LTT_PAGE_CONFIG = %s;" % json.dumps(cfg, ensure_ascii=False), page, flags=re.S)
    c1 = CARDS[0]
    page = must_sub(r'(<span class="hybrid-active-title" id="sticky-name">)[^<]*(</span>)', r"\g<1>%s\2" % c1["short"], page)
    page = must_sub(r'(<span class="hybrid-active-price" id="sticky-price">)[^<]*(</span>)', r"\g<1>From €%s\2" % c1["price"], page)
    page = must_sub(r'(<a class="hybrid-cta-btn" href=")[^"]*(" id="sticky-cta-btn")', r"\g<1>%s\2" % R["book_url"](c1, "sticky"), page)
    page = must_sub(r"<span>All \d+ Thermal Baths</span>", "<span>All %d Options</span>" % N, page)
    page = page.replace("Jump to Tested Thermal Bath", "Jump to a Ticket")
    page = page.replace('aria-label="Jump to Bath Review"', 'aria-label="Jump to Ticket Review"')
    return page


def jsonld(page):
    i = page.find('id="ltt-schema-jsonld"')
    s = page.find(">", i) + 1
    e = page.find("</script>", s)
    data = json.loads(page[s:e])
    items = []
    for pos, c in enumerate(CARDS, 1):
        avg, tot = R["wavg"](c["ratings"])
        addr = R["strip_tags"](c["getthere"][0]).replace("📍 ", "")
        offer = {"@type": "Offer", "availability": "https://schema.org/InStock",
                 "url": R["book_url"](c, "schema").replace("&amp;", "&")}
        if c.get("price"):
            offer.update(price=c["price"], priceCurrency="EUR")
        else:
            offer.update(price=c["price_huf"], priceCurrency="HUF")
        items.append({"@type": "ListItem", "position": pos, "url": "%s#%s" % (URL, c["anchor"]), "item": {
            "@type": "Product", "name": R["strip_tags"](c["title"]), "description": R["strip_tags"](c["pick"]),
            "brand": {"@type": "Organization", "name": R["strip_tags"](c["short"])},
            "isRelatedTo": {"@type": "TouristAttraction", "name": R["strip_tags"](c["title"]), "address": addr},
            "aggregateRating": {"@type": "AggregateRating", "ratingValue": "%.2f" % avg, "bestRating": "5",
                                "worstRating": "1", "reviewCount": str(tot)},
            "offers": offer}})
    graph = []
    for node in data["@graph"]:
        t = node.get("@type")
        if t == "Article":
            node["@id"] = URL + "#article"
            node["mainEntityOfPage"] = {"@type": "WebPage", "@id": URL}
            node["url"] = URL
            node["headline"] = TITLE_TXT
            node["description"] = DESC
            node["datePublished"] = TODAY
            node["dateModified"] = TODAY
            node["about"] = {"@type": "TouristAttraction", "name": "Széchenyi Thermal Bath",
                             "address": "Állatkerti körút 9-11, 1146 Budapest"}
            node["image"] = [SPARTY_PHOTOS[0], SPARTY_PHOTOS[1]]
            node["mainEntity"] = {"@type": "ItemList", "name": "Sparty tickets and alternatives", "description": DESC,
                                  "numberOfItems": N, "itemListElement": items}
            graph.append(node)
        elif t == "BreadcrumbList":
            node["@id"] = URL + "#breadcrumb"
            node["itemListElement"] = [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Thermal Baths in Budapest", "item": SITE + HUB},
                {"@type": "ListItem", "position": 3, "name": "Sparty", "item": URL}]
            graph.append(node)
        elif t != "FAQPage":
            graph.append(node)
    graph.append({"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in FAQ]})
    data["@graph"] = graph
    out = json.dumps(data, ensure_ascii=False, indent=1).replace("—", ":")
    return page[:s] + out + page[e:]


def main():
    page = R["SRC"]["page"]
    page = jsonld(chrome(body(hero(head(page)))))
    page = page.replace("LUXURY EDITORIAL SYSTEM — UNIFIED", "LUXURY EDITORIAL SYSTEM: UNIFIED")
    content = re.sub(r'<header[^>]*class="[^"]*ltt-navbar.*?</header>', "", page, flags=re.S)  # menu: sync_layout.py
    leftovers = [w for w in ("What visitors say", "6 Best Thermal Baths", "Dandár", "Palatinus", "en-thermal-baths-", "—", "&mdash;")
                 if w in content]
    assert not leftovers, leftovers
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(page)
    print("wrote", OUT, len(page))


if __name__ == "__main__":
    main()
