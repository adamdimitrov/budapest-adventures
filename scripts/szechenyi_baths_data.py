"""Card data for /szechenyi-baths-budapest (EN only), built 15 November 2026.

Bath facts (hours, desk prices, pools, rules) are from szechenyifurdo.hu, checked 14 November 2026
for /thermal-baths-budapest (see scripts/thermal_baths_data.py). Ticket products, prices, ratings,
inclusions and cancellation terms were rechecked on the live listings on 15 November 2026; option
prices for the day ticket are from the booking calendar for Thursday 19 November 2026 and for
Sparty from Saturday 21 November 2026. The user personally visited Széchenyi (14 Nov 2026).
"""
import urllib.parse

import bath_hub_nav

GYG = ("https://www.getyourguide.com/budapest-l29/{slug}/?partner_id=YS414AJ"
       "&utm_medium=online_publisher&cmp=en-szechenyi-{placement}-{key}&mkt_cmp=true")
TIQETS = "https://www.tiqets.com/en/things-to-do-in-budapest-c68199/{slug}/?partner=thecruisedetective.com-176436"
VIATOR = "https://tp.media/r?campaign_id=47&marker=404154&p=1922&sub_id=en-szechenyi-rating-{key}&trs=204442&u=https%3A%2F%2Fwww.viator.com%2Ftours%2FBudapest%2F{slug}"
MAPS = "https://www.google.com/maps/search/?api=1&query={q}"
CDN = "/assets/cdn/60e43c7d6d05b671dff0dc1a/"
CHECK = "15 November 2026"
GYG_NOTE = "Checked on the booking calendar for Thursday 19 November 2026."
SPARTY_SLUG = "budapest-the-ultimate-late-night-spa-party-ticket-t386559"


def pill(icon, label, pop, note=None, cls=""):
    extra = (' ' + cls) if cls else ''
    n = '<span class="bpa-lang-note">%s</span>' % note if note else ''
    return ('<details class="bpa-lang%s"><summary class="bpa-sp">%s <span class="bpa-lang-label">%s</span>'
            '<span class="bpa-lang-chev" aria-hidden="true">▾</span></summary><div class="bpa-lang-pop">%s%s</div></details>'
            % (extra, icon, label, pop, n))


def maps_link(q, text):
    return ('<a href="%s" rel="nofollow noopener" target="_blank">%s</a>'
            % (MAPS.format(q=urllib.parse.quote_plus(q)).replace("&", "&amp;"), text))


P = {k: CDN + v for k, v in dict(
    hero="63c12f890d9668187cda50a6_1_Sz%C3%A9chenyi%20Thermal%20Bath.webp",
    outdoor="64b7a8d6a973a0c983a7095a_11Szechenyi-bath-ourdoor-pool.avif",
    lap="64b7a8c8c9fdf77e1c5197bf_10-Szechenyi-bath-outdoor-lap-pool.avif",
    indoor1="64b7b108d4bc082efa13bf83_12-Szechenyi-bath-indoor-pool-1.avif",
    indoor3="64b7b1876a1ea8dedc6fb379_14-Szechenyi-bath-indoor-pool-3.avif",
    sauna="64b7b4187c0010e65f20f953_15-Szechenyi-bath-aroma-sauna.avif",
    entrance="64b6a6449efb8b06f9af724c_01-Szechenyi-bath-entrance.webp",
    office="64b6a69a5ab0f3b16f839aa2_02-Szechenyi-bath-ticket-office.webp",
    validation="64b6a6b19f9458bcf5a7b66c_03-Szechenyi-bath-online-ticket-validation.webp",
    lockers="64b7a540343999e752fcbdd0_05-Szechenyi-bath-locker-room.webp",
    cabins7="64b6b6d1658a3dbbd26c7205_07-Szechenyi-bath-cabins.avif",
    cabins="64b6b7ed2c5ca7263d3ae36e_08-Szechenyi-bath-cabins.avif",
    bring="64b6bcf22c5ca7263d424207_09-Szechenyi-bath-what-to-bring.avif",
).items()}

ADDRESS = maps_link("Széchenyi Gyógyfürdő Állatkerti körút 9-11 Budapest", "Állatkerti körút 9-11, 1146 Budapest (City Park)")
METRO = "🚇 Take <strong>metro M1</strong> (the little yellow line from Vörösmarty tér) to <strong>Széchenyi fürdő</strong>; the entrance is about a 2-minute walk."
HOURS_POP = ("<strong>Mon–Thu</strong> 7:00–20:00 · <strong>Fri</strong> 7:00–22:00 · <strong>Sat–Sun</strong> 8:00–20:00. "
             "8 December 2026: closes at 16:00. 18 December 2026 to 6 January 2027: opens at 8:00. "
             "25 and 26 December and 1 January: opens at 10:00.")
OFFICIAL_NOTE = "From szechenyifurdo.hu, checked 14 November 2026; hours change on holidays."
AMEN_DAY = [("yes", "Outdoor Pools"), ("yes", "Indoor Pools"), ("yes", "Sauna"), ("yes", "Steam Room"),
            ("no", "Towel Included"), ("no", "Flip-flops Included")]

CARDS = []

# ── 1 ─ Day ticket with upgrades (t4139) ─────────────────────────────────────────────
CARDS.append(dict(
    key="day-ticket", anchor="item-1-day-ticket", cat="day", tested=True,
    rank="🏆 #1 Best Overall", color="bpa-gold",
    area="City Park, District XIV", time="Half Day", transport="M1 Széchenyi fürdő",
    maps_q="Széchenyi Gyógyfürdő Állatkerti körút 9-11 Budapest",
    title="Széchenyi Day Ticket (Locker or Cabin)", short="Széchenyi Day Ticket",
    book="gyg", gyg_slug="szechenyi-spa-full-day-entrance-pass-t4139",
    ratings=[("GetYourGuide", 4.2808, 29228, "gyg", None),
             ("Tiqets", 4.4, 1252, "tiqets", "tickets-for-szechenyi-spa-full-day-entry-p974376"),
             ("Viator", 3.8, 2393, "viator", "Private-Entrance-to-Szechenyi-Spa-in-Budapest-with-Optional-Massage/d499-5808SZECHENYI")],
    price="39", psub="per adult · Morning Pass, entry 7:00–9:00", via="GetYourGuide",
    trust=["✓ Free cancellation up to 24 hours before", "✓ Reserve now, pay later"],
    tested_pop="<strong>I visited Széchenyi myself</strong> on this kind of ticket. Most of the photos here are my own.",
    photos=[P[k] for k in ("hero", "outdoor", "lap", "validation", "lockers", "cabins", "indoor1", "indoor3", "sauna", "bring")],
    alt="Széchenyi Thermal Bath day ticket",
    pills=[
        pill("🎟️", "3 ticket options",
             "<strong>Morning Pass</strong> with locker, entry 7:00–9:00: €39 · <strong>Weekday Pass</strong> with locker: €46 · "
             "<strong>Weekday Pass</strong> with private cabin: €50. You stay as long as you like on the day.", GYG_NOTE),
        pill("🕒", "Fri open to 22:00", HOURS_POP, OFFICIAL_NOTE, "bpa-time"),
        pill("🔐", "Locker vs cabin",
             "<strong>Locker:</strong> a numbered locker in the shared, gender-separated changing room, opened with a wristband (3,000 HUF if lost). "
             "<strong>Cabin:</strong> a lockable changing booth for you (or two of you) where you also leave your things; €4 more online, 1,000 HUF more at the desk.",
             "From szechenyifurdo.hu and the ticket listing."),
        pill("🚪", "Skips the cashier",
             "Booked tickets open the turnstile at the self-service validation machines by the swimming-pool entrance, so you walk past the cashier queue.",
             "From the ticket listing and my own visit."),
    ],
    pick="for a normal day at Széchenyi: all 18 pools, saunas and steam rooms, a free-cancellation ticket, and the €39 early slot if you can be in the water before 9:00.",
    skip="if you only care about the lowest price and do not mind queueing: the desk sells the same weekday locker ticket for 13,200 HUF.",
    pros=[("Cheapest early start", "The Morning Pass is €39 with entry between 7:00 and 9:00, when the outdoor pools are at their emptiest."),
          ("Free cancellation", "Cancel up to 24 hours before for a full refund, and pay later; the desk ticket is a same-day purchase."),
          ("No cashier queue", "The QR ticket goes straight to the validation machines at the entrance."),
          ("Whole bath, all day", "Every pool, sauna and steam cabin is included; you leave when you want.")],
    cons=[("Costs more than the desk", "€46 online for the weekday locker ticket against 13,200 HUF (about €34) at the desk."),
          ("No towel or flip-flops", "Bring your own or buy them inside: towel 6,900 HUF, slippers 4,200 HUF."),
          ("Not for under-14s", "The booked ticket is not suitable for children under 14.")],
    summary_q=("Should I book Széchenyi online or pay at the door?",
               "Book online if you want free cancellation, no cashier queue or the €39 early slot. Pay at the desk if you are going on a weekday afternoon and want the lowest price."),
    summary=["This is the ticket most people need: a full day in Széchenyi with a locker or a private cabin. "
             "The trick is the <strong>Morning Pass</strong>. At €39 with entry before 9:00, it is the cheapest booked ticket, and the steaming outdoor pools are close to empty at that hour.",
             "Choose the <strong>cabin</strong> (€50) if you are two and want to change in private and keep your bags together. "
             "The shared locker rooms are fine, but they get busy at weekends."],
    quotes=[("A great way to spend a day in Budapest.", "GetYourGuide", "November 2026"),
            ("Go in the morning when there are still few people and the baths are clean.", "GetYourGuide", "November 2026"),
            ("Outside pools were especially atmospheric in the rain", "GetYourGuide", "November 2026")],
    getthere=["📍 " + ADDRESS, METRO,
              "🎟️ Enter on the <strong>swimming-pool side</strong> (Állatkerti körút) and scan your ticket at the machines."],
    spcards=[
        ("Entrance &amp; Validation", P["validation"],
         "Booked tickets are scanned at self-service machines on the swimming-pool side, so you skip the cashier window."),
        ("Lockers", P["lockers"],
         "Shared, gender-separated changing rooms with numbered lockers. Your wristband opens your locker and the turnstiles."),
        ("Private Cabins", P["cabins"],
         "A lockable booth for one or two people. Worth the extra €4 if you carry a bag or want to change in private."),
        ("Outdoor Pools", P["outdoor"],
         "Thermal pool 36–38 °C, adventure pool with whirlpool 32–34 °C, and the 26–28 °C swimming pool."),
        ("Indoor Pools &amp; Saunas", P["indoor1"],
         "Medicinal pools from 28 to 40 °C, plunge pools at 18 and 40 °C, five saunas from 50 to 90 °C and three steam cabins."),
    ],
    qf=[("Ticket Options", "Morning Pass with locker €39 (entry 7:00–9:00) · Weekday Pass with locker €46 · with private cabin €50"),
        ("Desk Price 2026", "Locker 13,200 HUF Mon–Thu, 14,800 HUF Fri–Sun · before 9:00: 10,500 / 11,800 HUF · cabin +1,000 HUF"),
        ("Opening Hours", "Mon–Thu 7:00–20:00 · Fri 7:00–22:00 · Sat–Sun 8:00–20:00"),
        ("Cancellation", "Free up to 24 hours before"),
        ("Age Limit", "Not suitable for children under 14"),
        ("Address", "Állatkerti körút 9-11, 1146 Budapest")],
    amen=AMEN_DAY,
))

# ── 2 ─ Sparty (t386559) ─────────────────────────────────────────────────────────────
CARDS.append(dict(
    key="sparty", anchor="item-2-sparty", cat="night", tested=False,
    rank="🎉 #2 Best Night Out", color="bpa-silver",
    area="City Park, District XIV", time="21:30–2:00", transport="M1 Széchenyi fürdő",
    maps_q="Széchenyi Gyógyfürdő Állatkerti körút 9-11 Budapest",
    title="Sparty: Saturday Night Pool Party at Széchenyi", short="Sparty Night Pool Party",
    book="gyg", gyg_slug=SPARTY_SLUG,
    ratings=[("GetYourGuide", 4.1542, 1836, "gyg", None)],
    price="73", psub="per person · Saturdays 21:30–2:00", via="GetYourGuide",
    trust=["✓ Locker included", "✓ Instant e-ticket"],
    photos=[P[k] for k in ("outdoor", "hero", "lap", "lockers", "entrance")],
    alt="Sparty night pool party at Széchenyi Thermal Bath",
    pills=[
        pill("🎟️", "€73 or €100",
             "<strong>Entry ticket</strong> with locker: €73 · <strong>Premium</strong> with two drink coupons: €100. "
             "Two coupons buy roughly one cocktail, so most people are better off with the basic ticket.",
             "Checked on the booking calendar for Saturday 21 November 2026."),
        pill("🕘", "Every Saturday",
             "Doors at <strong>21:30</strong>, last entry <strong>1:00</strong>, party ends at <strong>2:00</strong>. "
             "Techno, lasers, fire and circus acts around the outdoor pools at 34–38 °C.",
             "From the event listing, 15 November 2026."),
        pill("💳", "Bars take SpartyPay only",
             "No cards at the bars: you load a <strong>SpartyPay card</strong> with cash, first top-up 20,000 HUF including a 3,000 HUF deposit. "
             "Every drink needs a reusable cup (700 HUF, 350 HUF back). Cocktails run about 6,300 HUF.",
             "From the event listing and recent guest reviews."),
        pill("🔞", "18+ · non-refundable",
             "Adults only, ID required. Tickets cannot be cancelled or refunded, so book once your Saturday is fixed.",
             "From the event listing, 15 November 2026."),
    ],
    pick="for a Saturday night you will talk about: a rave in hot water under the open sky, with lights, fire shows and DJs in the most famous bath in Budapest.",
    skip="if you want to relax, are under 18, or your plans might change (no refunds); for a calm evening soak, take the day ticket on a Friday, when the bath stays open until 22:00.",
    pros=[("Nothing else like it", "Running since 1994, it is Budapest's original bath party, in 34–38 °C water."),
          ("Big production", "DJs, lasers, fire and circus performers around the outdoor pools."),
          ("Easy to reach", "Metro M1 to the door, 5 minutes from the city centre."),
          ("Locker included", "The ticket includes a locker in the changing rooms.")],
    cons=[("Non-refundable", "No cancellation at all, unlike the day tickets."),
          ("Expensive drinks", "Cocktails around 6,300 HUF, paid only by preloaded SpartyPay card."),
          ("Hard to dance", "The pool is shoulder-deep in places, so dancers crowd around the steps."),
          ("Crowded", "Reviewers mention lots of people and, for some women, unwanted attention.")],
    summary_q=("Is Sparty worth it?",
               "Yes, if you want a party. It is the most memorable night out in Budapest for groups and stag or hen weekends. If you want to relax, it is the wrong ticket."),
    summary=["Sparty turns Széchenyi's outdoor pools into a night club every Saturday from 21:30 to 2:00. "
             "The water stays at 34 to 38 °C, so it works in November as well as in July.",
             "Budget for drinks on top of the ticket. Bring cash to load the SpartyPay card, pick the €73 basic ticket, and order a <strong>Bolt</strong> or <strong>Uber</strong> home rather than the taxis waiting at the gate. "
             + ('For dates, dress code and every ticket type, see our full <a href="/sparty-budapest">Sparty Budapest guide</a>.'
                if bath_hub_nav.live("/sparty-budapest") else "")],
    quotes=[("Amazing party scene at the hot baths.", "GetYourGuide", "October 2026"),
            ("The music and lights were fab, the heat off the pool was fantastic too.", "GetYourGuide", "October 2026"),
            ("The drinks are very expensive though...", "GetYourGuide", "June 2026")],
    getthere=["📍 " + ADDRESS, METRO,
              "🌙 After 2:00 the metro is closed: order a Bolt or Uber rather than taking the taxis waiting at the gate."],
    spcards=[
        ("The Party", P["outdoor"],
         "DJs and light shows run around the outdoor thermal pools from 21:30; last entry is at 1:00."),
        ("Lockers &amp; Changing", P["lockers"],
         "Change and store your clothes in the regular changing rooms; a locker is included in every ticket."),
        ("Paying at the Bars", None,
         "Bars accept only the SpartyPay card, topped up with cash (20,000 HUF first load, 3,000 HUF of it a deposit). Drinks come in reusable cups at 700 HUF each."),
        ("What to Bring", P["bring"],
         "Swimwear, flip-flops (mandatory), a towel, cash and an ID or passport. No glass, food or large bags."),
    ],
    qf=[("Ticket Options", "Entry with locker €73 · Premium with two drink coupons €100 (Sat 21 Nov 2026)"),
        ("When", "Every Saturday, 21:30–2:00, last entry 1:00"),
        ("Cancellation", "Non-refundable"),
        ("Age Limit", "18+, ID required"),
        ("Payment at Bars", "SpartyPay card only, topped up in cash"),
        ("Address", "Állatkerti körút 9-11, 1146 Budapest")],
    amen=[("yes", "Outdoor Pools"), ("yes", "Locker"), ("yes", "Bars"), ("no", "Towel Included"), ("no", "Refunds")],
))

# ── 3 ─ Beer Spa + bath ticket (t1145839) ────────────────────────────────────────────
CARDS.append(dict(
    key="beer-spa", anchor="item-3-beer-spa", cat="upgrade", tested=False,
    rank="🍺 #3 Best for Groups", color="bpa-bronze",
    area="City Park, District XIV", time="Full Day + 45 min", transport="M1 Széchenyi fürdő",
    maps_q="Thermal Beer Spa Széchenyi Kós Károly sétány 1 Budapest",
    title="Széchenyi Ticket + Beer Spa with Unlimited Beer", short="Széchenyi + Beer Spa",
    book="gyg", gyg_slug="beer-spa-with-optional-szechenyi-bath-tickets-t1145839",
    ratings=[("GetYourGuide", 4.4339, 104, "gyg", None)],
    price="125", psub="per person · bath day ticket included", via="GetYourGuide",
    trust=["✓ Free cancellation up to 24 hours before", "✓ Private cabin all day"],
    photos=[P[k] for k in ("indoor3", "cabins7", "hero", "outdoor", "sauna")],
    alt="Széchenyi Thermal Bath with beer spa",
    pills=[
        pill("🍺", "45 min, unlimited beer",
             "A <strong>45-minute soak</strong> in a wooden tub of thermal water with hops, malt and beer salts, with a tap of Hungarian draught beer beside you. Pour as much as you like during the session.",
             "From the ticket listing, 15 November 2026."),
        pill("🎟️", "Bath ticket included",
             "The price includes a <strong>full-day fast-track entry</strong> to Széchenyi and a <strong>private changing cabin</strong> for the whole day, so you stay on in the pools after the beer spa.",
             "From the ticket listing, 15 November 2026."),
        pill("🕙", "From 10:00",
             "The beer spa opens at 10:00; arrive 20 minutes before your slot for the briefing. Go straight to the BeerSpa reception, left of the main hall, not the bath's information desk.",
             "From the ticket listing, 15 November 2026."),
        pill("🔞", "18+", "Adults only. Towels are extra (5,000 HUF on site) and slippers are mandatory.", "From the ticket listing, 15 November 2026."),
    ],
    pick="for a group of friends or a couple who want a fun two-in-one: a private beer tub with your own tap, then the rest of the day in Széchenyi's pools, all on one free-cancellation ticket.",
    skip="if you do not drink beer or are under 18, or if you only want the bath: the plain day ticket costs a third of the price.",
    pros=[("Two experiences, one ticket", "Beer spa session plus a full-day Széchenyi entry with fast track."),
          ("Private cabin all day", "A lockable cabin is included, worth €4 on its own."),
          ("Truly unlimited beer", "Self-poured draught beer from your own tap for the whole 45 minutes."),
          ("Free cancellation", "Cancel up to 24 hours before for a full refund.")],
    cons=[("Pricey", "€125 per person against €46 for the plain weekday ticket."),
          ("Short session", "The beer spa itself lasts 45 minutes."),
          ("Small changing space", "A recent guest found the beer spa's changing area a little small.")],
    summary_q=("Is the Széchenyi beer spa worth it?",
               "For a group or a celebration, yes: you get the bath for the day plus a private beer tub. For a quiet solo soak, the plain day ticket is better value."),
    summary=["This combo adds a private <strong>beer spa</strong> inside Széchenyi to a full-day bath ticket. "
             "You soak in a wooden tub of warm thermal water with beer ingredients and pour your own draught beer, then spend the rest of the day in the regular pools.",
             "It is the most fun way to do Széchenyi with friends, and the free cancellation makes it an easy booking to hold for a group trip."],
    quotes=[("A really fun and relaxing experience", "GetYourGuide", "October 2026"),
            ("it was fun to have draft beer on tap right next to us!", "GetYourGuide", "October 2026"),
            ("A very novel way to spend an hour or so.", "GetYourGuide", "September 2026")],
    getthere=["📍 " + maps_link("Thermal Beer Spa Széchenyi Kós Károly sétány 1 Budapest", "Széchenyi main entrance, Kós Károly sétány 1, 1146 Budapest"),
              METRO,
              "🍺 Inside the main hall, turn left into the corridor to the <strong>BeerSpa reception</strong>."],
    spcards=[
        ("The Beer Tub", None,
         "A handcrafted wooden tub of thermal water with hops, malt and beer salts, plus your own draught tap for 45 minutes."),
        ("Private Cabin", P["cabins7"],
         "A private, lockable changing cabin for the whole day is included in the ticket."),
        ("The Bath Afterwards", P["outdoor"],
         "Your Széchenyi ticket is valid all day, so you go on to the outdoor and indoor pools after the session."),
    ],
    qf=[("Price", "€125 per person, bath day ticket and beer spa session included"),
        ("Session", "45 minutes, unlimited self-poured draught beer"),
        ("Includes", "Full-day fast-track Széchenyi entry, private changing cabin, host briefing"),
        ("Opening", "Beer spa from 10:00; arrive 20 minutes before your slot"),
        ("Cancellation", "Free up to 24 hours before"),
        ("Age Limit", "18+")],
    amen=[("yes", "Beer Spa"), ("yes", "Private Cabin"), ("yes", "Fast Track"), ("yes", "Outdoor Pools"), ("no", "Towel Included")],
))

# ── 4 ─ Palm House Pass (t441452) ────────────────────────────────────────────────────
CARDS.append(dict(
    key="palm-house", anchor="item-4-palm-house", cat="upgrade", tested=False,
    rank="🌴 #4 Best VIP Day", color="bpa-slate",
    area="City Park, District XIV", time="Full Day", transport="M1 Széchenyi fürdő",
    maps_q="Széchenyi Gyógyfürdő Állatkerti körút 9-11 Budapest",
    title="Széchenyi Palm House VIP Pass", short="Palm House VIP Pass",
    book="gyg", gyg_slug="budapest-szechenyi-thermal-bath-palm-house-pass-t441452",
    ratings=[("GetYourGuide", 4.2779, 30, "gyg", None)],
    price="110", psub="per person · robe, towel, cocktail", via="GetYourGuide",
    trust=["✓ Free cancellation up to 24 hours before", "✓ Fast-track entrance"],
    photos=[P[k] for k in ("indoor1", "cabins", "hero", "outdoor", "sauna")],
    alt="Széchenyi Thermal Bath Palm House",
    pills=[
        pill("🌴", "Private lounge",
             "Access to the <strong>Palm House</strong>, a glass-roofed relaxation area with lounge chairs and personal service, plus all the main pools.",
             "From the ticket listing, 15 November 2026."),
        pill("🧺", "Robe, towel, cap",
             "Includes a <strong>bathrobe and towel</strong> for the day, disposable slippers and a swim cap, so you can arrive with just a swimsuit.",
             "From the ticket listing, 15 November 2026."),
        pill("🍹", "Cocktail + fruit",
             "One cocktail (alcoholic or not), unlimited mineral water and a fruit bowl. Other drinks from the menu, paid by card.",
             "From the ticket listing, 15 November 2026."),
        pill("🔐", "Cabin + fast track",
             "A private cabin and entry through a separate fast-track entrance. Massages and hotel transfers are not included.",
             "From the ticket listing, 15 November 2026."),
    ],
    pick="for a slow, comfortable day at Széchenyi: a quiet lounge to retreat to between pools, a robe and towel waiting for you, and a cocktail included.",
    skip="if you mostly want the outdoor pools for a couple of hours; the €46 day ticket covers them and you can buy a towel inside.",
    pros=[("A place to retreat", "The Palm House lounge is the calm spot in the busiest bath in Budapest."),
          ("Nothing to pack", "Robe, towel, slippers and swim cap are provided."),
          ("Extras included", "A cocktail, unlimited mineral water and a fruit bowl."),
          ("Private cabin and fast track", "Separate entrance and your own changing cabin.")],
    cons=[("Expensive", "€110 against €50 for the cabin day ticket."),
          ("Same old building", "One guest notes worn tiles and crowds in the main bath; the lounge does not change that."),
          ("Few reviews", "Only 30 reviews so far, so less proof than the day ticket.")],
    summary_q=("What is the Széchenyi Palm House?",
               "A VIP relaxation area inside Széchenyi with lounge chairs, service, a drink and snacks. The pass includes it plus the normal bath, a cabin, a robe and a towel."),
    summary=["The Palm House pass is Széchenyi for people who hate packing and queueing. "
             "You get a separate entrance, a private cabin, a robe and towel, and a quiet lounge with a cocktail and fruit to come back to between the pools.",
             "It is good value only if you would have bought a towel and robe anyway (6,900 and 12,600 HUF at the desk) and plan to stay most of the day."],
    quotes=[("Palm house is well worth the extra money.", "GetYourGuide", "July 2026"),
            ("We were there from 10am until 5 and enjoyed the sauna, various pools and the outdoor pool.", "GetYourGuide", "July 2026")],
    getthere=["📍 " + ADDRESS, METRO,
              "🌴 Use the separate fast-track entrance shown on your ticket."],
    spcards=[
        ("Palm House Lounge", None,
         "Lounge chairs, personal service, a cocktail, mineral water and a fruit bowl, away from the crowds in the main pools."),
        ("Robe &amp; Towel", P["bring"],
         "Bathrobe, towel, disposable slippers and swim cap are provided for the day."),
        ("Private Cabin", P["cabins"],
         "Your own lockable changing cabin is included."),
    ],
    qf=[("Price", "€110 per person"),
        ("Includes", "Full-day ticket, Palm House lounge, private cabin, robe, towel, slippers, swim cap, 1 cocktail, mineral water, fruit bowl"),
        ("Not Included", "Massages, hotel pick-up and drop-off"),
        ("Entry", "Separate fast-track entrance"),
        ("Cancellation", "Free up to 24 hours before")],
    amen=[("yes", "VIP Lounge"), ("yes", "Robe &amp; Towel"), ("yes", "Private Cabin"), ("yes", "Drink Included"), ("no", "Massage")],
))

# ── 5 ─ Fast Track with locker (t1443106) ────────────────────────────────────────────
CARDS.append(dict(
    key="fast-track", anchor="item-5-fast-track", cat="day", tested=False,
    rank="⚡ #5 Best for Busy Weekends", color="bpa-slate",
    area="City Park, District XIV", time="Half Day", transport="M1 Széchenyi fürdő",
    maps_q="Széchenyi Gyógyfürdő Állatkerti körút 9-11 Budapest",
    title="Széchenyi Fast Track Admission with Locker", short="Fast Track with Locker",
    book="gyg", gyg_slug="budapest-szechenyi-baths-fast-track-admission-with-locker-t1443106",
    ratings=[("GetYourGuide", 4.1185, 22, "gyg", None)],
    price="59", psub="per adult · fast-track entry + locker", via="GetYourGuide",
    trust=["✓ Free cancellation up to 24 hours before", "✓ Reserve now, pay later"],
    photos=[P[k] for k in ("lap", "entrance", "lockers", "indoor1", "sauna")],
    alt="Széchenyi Thermal Bath fast track entrance",
    pills=[
        pill("⚡", "Separate entrance",
             "Entry through a <strong>separate fast-track entrance</strong>, with a locker included. Useful on weekend and holiday afternoons, when the main entrance queues.",
             "From the ticket listing, 15 November 2026."),
        pill("🏊", "All pools + saunas",
             "Indoor and outdoor thermal pools, saunas and steam baths for the whole opening day.",
             "From the ticket listing, 15 November 2026."),
        pill("🕒", "Fri open to 22:00", HOURS_POP, OFFICIAL_NOTE, "bpa-time"),
    ],
    pick="for a Saturday, Sunday or holiday visit when you want the shortest possible wait at the door and a locker, with free cancellation.",
    skip="on weekdays: the regular day ticket also skips the cashier at the validation machines and costs €13 less.",
    pros=[("Shortest wait", "A separate entrance for fast-track tickets."),
          ("Locker included", "Store your things in a numbered locker."),
          ("Free cancellation", "Cancel up to 24 hours before.")],
    cons=[("Costs more", "From €59 against €46 for the weekday locker ticket."),
          ("Few reviews", "22 reviews so far."),
          ("No towel", "Towel and flip-flops are not included.")],
    summary_q=("Do I need a fast-track ticket for Széchenyi?",
               "Only on busy weekend or holiday afternoons. On weekday mornings, the regular booked ticket gets you in just as fast."),
    summary=["The fast-track ticket buys one thing: a separate entrance. On a weekday morning that is worth little, because booked day tickets already skip the cashier at the scanners.",
             "On a sunny Saturday afternoon or between Christmas and New Year, when the queue reaches the street, the extra €13 starts to make sense."],
    quotes=[("Everything was very well organized, from the booking to the thermal baths themselves.", "GetYourGuide", "September 2026"),
            ("The thermal baths are huge, and we really relaxed.", "GetYourGuide", "September 2026")],
    getthere=["📍 " + ADDRESS, METRO],
    spcards=[
        ("Fast-Track Entrance", P["entrance"], "A separate entrance for fast-track tickets, away from the main queue."),
        ("Lockers", P["lockers"], "A numbered locker in the shared changing rooms is included."),
    ],
    qf=[("Price", "From €59 per adult"),
        ("Includes", "Fast-track admission, day ticket, locker, all pools, saunas and steam baths"),
        ("Opening Hours", "Mon–Thu 7:00–20:00 · Fri 7:00–22:00 · Sat–Sun 8:00–20:00"),
        ("Cancellation", "Free up to 24 hours before")],
    amen=AMEN_DAY,
))
