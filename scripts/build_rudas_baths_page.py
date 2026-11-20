#!/usr/bin/env python3
"""Build /rudas-baths-budapest (EN only) from the /thermal-baths-budapest shell.

Every price, hour and rule below was checked in Chrome on 15 November 2026:
rudasfurdo.hu (opening hours, prices-2026, pools-and-saunas, available-services, offers),
tickets.rudasfurdo.hu (official online tickets), the GetYourGuide listing t233617
(booking calendar for Thursday 19 and Saturday 21 November 2026) and Google Maps.
Step-free access: rudasfurdo.hu, checked 14 November 2026 for the thermal baths hub.

Run from the repo root:
    python3 scripts/build_rudas_baths_page.py
It reads thermal-baths-budapest.html as the page shell (head, menu, card CSS/JS, footer)
and writes rudas-baths-budapest.html. Then run python3 scripts/sync_layout.py (menu, footer, search index).
"""
import json
import math
import os
import re
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from night_blocks import balanced, deck_card, details_card, all_spans  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "rudas-baths-budapest.html")
SLUG = "rudas-baths-budapest"
SITE = "https://www.budapestadventures.com"
URL = SITE + "/" + SLUG
TODAY = "2026-11-15"
TODAY_TXT = "15 November 2026"
HUB = "/thermal-baths-budapest"
SZE = "/szechenyi-baths-budapest"


def live(href):
    """True when the linked page exists in this checkout (sibling bath pages ship in their own PRs)."""
    return os.path.exists(os.path.join(ROOT, href.strip("/") + ".html"))


SZE_LINK = ', or go straight to <a href="%s">Széchenyi</a>' % SZE if live(SZE) else ""


def rd(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()


SHELL = rd("thermal-baths-budapest.html")
RIVER = rd("best-budapest-river-cruises.html")

# ── links ────────────────────────────────────────────────────────────────────────────
GYG = ("https://www.getyourguide.com/budapest-l29/{slug}/?partner_id=YS414AJ"
       "&utm_medium=online_publisher&cmp=en-rudas-baths-{placement}-{key}&mkt_cmp=true")
GYG_SLUG = "budapest-rudas-turkish-bath-spa-day-pass-3-course-meal-t233617"
OFFICIAL_SHOP = "https://tickets.rudasfurdo.hu/partner/rudas"
OFFICIAL_PRICES = "https://www.rudasfurdo.hu/en/prices-2026"
OFFICIAL_HOURS = "https://www.rudasfurdo.hu/en/opening-hours"
MAPS = "https://www.google.com/maps/search/?api=1&query={q}"
MAPS_Q = "Rudas Gyógyfürdő Döbrentei tér 9 Budapest"
GOOGLE_URL = MAPS.format(q=urllib.parse.quote_plus("Rudas Thermal Bath Budapest"))
CDN = "/assets/cdn/60e43c7d6d05b671dff0dc1a/"
NEW = "/assets/rudas-baths-2026/"
P = {  # photos
    "roof_dusk": NEW + "rudas-rooftop-pool-dusk-01.avif",
    "roof_toast": NEW + "rudas-rooftop-pool-toast-03.avif",
    "bistro": NEW + "rudas-bistro-terrace-05.avif",
    "dome": NEW + "rudas-turkish-bath-dome-02.avif",
    "turk_pool": NEW + "rudas-turkish-bath-pool-04.avif",
    "roof_sunset": CDN + "63c12fda4ee7c50a6cee3178_3_1%20Rudas%20Thermal%20Bath.webp",
    "roof_day": CDN + "64d4e6d882d74213380c1f24_Rudas-thermal-bath%20(11).webp",
    "turkish": CDN + "64d4e7021d502805c7a7c112_Rudas-thermal-bath%20(18).webp",
    "wellness": CDN + "64d4e674b2871f3b832c1681_Rudas-thermal-bath%20(15).webp",
    "lockers": CDN + "64d4e69c6efb73a26f9877f6_Rudas-thermal-bath%20(19).webp",
    "cabins": CDN + "64d4e6a5a89136c45fd1d9fc_Rudas-thermal-bath%20(20).webp",
    "outside": CDN + "64d4e65e09406b071f265969_Rudas-thermal-bath%20(14).webp",
    "corridor": CDN + "64d4e74e82fd0ed0adc4f09c_Rudas-thermal-bath%20(2).webp",
    "drinking": CDN + "64d4e79648d7f0b7f7ac4062_Rudas-thermal-bath%20(8).webp",
}

BOOKING_NOTE = "Prices for Thursday 19 and Saturday 21 November 2026; they change by date."
OFFICIAL_NOTE = "From rudasfurdo.hu; hours change on holidays."
SHOP_NOTE = "Official online prices are in euros and move with the exchange rate and peak days."


def pill(icon, label, pop, note=None, cls=""):
    extra = (' ' + cls) if cls else ''
    n = '<span class="bpa-lang-note">%s</span>' % note if note else ''
    return ('<details class="bpa-lang%s"><summary class="bpa-sp">%s <span class="bpa-lang-label">%s</span>'
            '<span class="bpa-lang-chev" aria-hidden="true">▾</span></summary><div class="bpa-lang-pop">%s%s</div></details>'
            % (extra, icon, label, pop, n))


def maps_link(q, text):
    return ('<a href="%s" rel="nofollow noopener" target="_blank">%s</a>'
            % (MAPS.format(q=urllib.parse.quote_plus(q)).replace("&", "&amp;"), text))


GOOGLE_RATING = ("Google", 4.3, 12415, "google", GOOGLE_URL)  # Rudas Thermal Bath on Google Maps, 15 Nov 2026
GYG_RATING = ("GetYourGuide", 4.1941, 1422, "gyg", None)       # t233617, 15 Nov 2026

GETTHERE = [
    "📍 " + maps_link(MAPS_Q, "Döbrentei tér 9, 1013 Budapest (Buda end of Elizabeth Bridge)"),
    "🚋 <strong>Tram</strong> 19, 41, 56 or 56A, or <strong>bus</strong> 7, 8E, 108E, 110 or 112 to the Buda end of Elizabeth Bridge.",
    "🌙 After night bathing: night buses <strong>907</strong> and <strong>973</strong>.",
]

TESTED_POP = "<strong>I bathed at Rudas myself:</strong> the Turkish bath, the wellness area, the saunas and the rooftop pool."

CARDS = []

# ── 1 ─ Day pass + 3-course meal (GetYourGuide) ───────────────────────────────────────
CARDS.append(dict(
    key="meal", anchor="item-1-rudas-day-pass-meal", cat="tested meal day weekday weekend", tested=True,
    rank="🏆 #1 Best Overall: Bath + Meal", color="bpa-gold",
    area="Rudas, District I", time="Full Day", transport="Tram 19, 41 · Bus 7",
    title="Rudas Day Pass + 3-Course Meal", short="Day Pass + 3-Course Meal",
    book="gyg", ratings=[GYG_RATING],
    price="74.99", psub="per adult · Mon–Thu, wellness + meal", via="GetYourGuide",
    trust=["✓ Free cancellation up to 24 hours before", "✓ Reserve now, pay later"],
    photos=[P["roof_dusk"], P["roof_toast"], P["bistro"], P["dome"], P["turk_pool"],
            P["roof_day"], P["turkish"], P["wellness"], P["lockers"]],
    alt="Rudas Thermal Bath day pass with a 3-course meal",
    pills=[
        pill("🍽️", "6 weekday options",
             "<strong>Mon–Thu:</strong> wellness + coffee €74.99 · wellness + wine €76.99 · wellness + sparkling wine €84.99 · "
             "Turkish bath + wellness + coffee €84.99 · Turkish bath + wellness + wine or sparkling wine €94.99. "
             "<strong>Fri–Sun:</strong> one option, the All-Inclusive with fast-track entry, €129.90.",
             BOOKING_NOTE),
        pill("🕒", "Entry from 11:00",
             "Tickets are valid from 11:00. You pick a table time at Rudas Bistro and bathe before or after the meal until 20:00.",
             None, "bpa-time"),
        pill("🚻", "Turkish bath days",
             "The wellness options do <strong>not</strong> include the Turkish bath. The Turkish bath is co-ed on Mon from 11:00, "
             "Thu and Fri from 11:00 and all day Sat and Sun; <strong>women only on Tuesday</strong>, <strong>men only on Wednesday</strong>.",
             OFFICIAL_NOTE),
        pill("🔞", "14+ only", "Children under 14 are not admitted to Rudas."),
    ],
    pick="if you want the whole Rudas day in one booking: rooftop pool, saunas and a 3-course meal at Rudas Bistro with a Danube view, with free cancellation.",
    skip="if you only want to bathe: the official all-zones ticket is 12,000 HUF on weekdays, without the meal.",
    pros=[("A meal with a view", "A 3-course à la carte meal at Rudas Bistro, plus coffee and lemonade, wine or sparkling wine depending on the option. Reviewers rate the food highly."),
          ("Free cancellation", "Cancel up to 24 hours before for a full refund, and reserve now, pay later."),
          ("Weekend fast track", "The €129.90 weekend option includes fast-track entry and the Turkish bath."),
          ("All day in the bath", "Entry from 11:00 and you can stay until closing at 20:00.")],
    cons=[("Base price is wellness only", "€74.99 excludes the Turkish bath; adding it costs €10 more (€84.99)."),
          ("Weekends cost more", "Friday to Sunday there is only the €129.90 option."),
          ("Kit not included", "Towels, bathrobes and flip-flops are extra; the desk sells a towel for 6,900 HUF."),
          ("Busy rooftop", "The panorama pool holds 16 people, and reviewers often find it full.")],
    summary_q=("Is the Rudas meal package worth it?",
               "Yes, if you would eat at Rudas Bistro anyway. If you only want to bathe, the official desk ticket is cheaper."),
    summary=["This is the ticket for a slow Rudas day: soak in the wellness pools and the 36 °C rooftop pool, then sit down for a 3-course "
             "lunch or dinner at Rudas Bistro, which looks over the Danube and Elizabeth Bridge. On weekdays the cheapest option is "
             "<strong>€74.99 with coffee</strong>; pick an option with <strong>Turkish bath</strong> in the name if you want the Ottoman pools too.",
             "Guests love the food and the rooftop view. The recurring complaints are crowds on the rooftop and a layout that is "
             "hard to find your way around: the wellness area, the Turkish bath and the roof are separate sections."],
    quotes=[("The restaurant is amazing!!! Very friendly and professional service and wonderful tastes!", "Verified guest", "October 2026"),
            ("Fun experience and beautiful views when you're in the upper pool.", "Verified guest", "November 2026"),
            ("Great food and enjoyed it all but the Turkish bath area os a must do", "Verified guest", "September 2026")],
    spcards=[
        ("Rudas Bistro", P["bistro"],
         "The 3-course meal is served at Rudas Bistro inside the bath, with a Danube view. Choose your table time when you book; request dietary options before ordering."),
        ("Rooftop Panorama Pool", P["roof_dusk"],
         "36 °C, 90 cm deep and room for 16 people at a time, with a view over the Danube. Included in every option."),
        ("Turkish Bath", P["dome"],
         "Six pools from 28 to 42 °C plus a cold plunge pool under the 16th-century dome. Only in the options with Turkish bath in the name."),
        ("Wellness &amp; Saunas", P["wellness"],
         "Wellness pools at 32, 36 and 42 °C, a cold plunge pool and the sauna world: two Finnish saunas, an aroma sauna, a steam cabin and a salt cabin."),
    ],
    qf=[("Weekday Prices", "Wellness + meal from €74.99 · with Turkish bath from €84.99 · up to €94.99 with wine or sparkling wine (Thu 19 Nov 2026)"),
        ("Weekend Price", "All-Inclusive with fast-track entry, Turkish bath and meal: €129.90 (Sat 21 Nov 2026)"),
        ("Valid", "One day, entry from 11:00, bath open until 20:00"),
        ("Includes", "Bath ticket, 3-course à la carte meal, coffee and lemonade, wine or sparkling wine by option"),
        ("Not Included", "Towel, bathrobe, swimwear, swim cap, flip-flops (sold at the cash desk)"),
        ("Cancellation", "Free up to 24 hours before"),
        ("Age Limit", "14+"),
        ("Address", "Döbrentei tér 9, 1013 Budapest")],
    amen=[("yes", "3-Course Meal"), ("yes", "Rooftop Pool"), ("yes", "Saunas"), ("yes", "Free Cancellation"),
          ("no", "Turkish Bath in Base Option"), ("no", "Towel")],
))

# ── 2 ─ Official all-zones day ticket (desk or fast track) ───────────────────────────
CARDS.append(dict(
    key="day-ticket", anchor="item-2-rudas-day-ticket", cat="tested day weekday weekend", tested=True,
    rank="💰 #2 Best Value: Bath Only", color="bpa-silver",
    area="Rudas, District I", time="3–4 Hours", transport="Tram 19, 41 · Bus 7",
    title="Official All-Zones Day Ticket", short="All-Zones Day Ticket",
    book="official", official_url=OFFICIAL_SHOP, btn="Official Tickets →", ratings=[GOOGLE_RATING],
    price_label="12,000 HUF", price_huf="12000", psub="at the desk, Mon–Thu · fast track online from €45", via="rudasfurdo.hu",
    trust=["✓ Turkish bath, wellness and rooftop", "✓ Locker included"],
    photos=[P["roof_day"], P["turkish"], P["roof_sunset"], P["wellness"], P["lockers"], P["cabins"], P["outside"], P["corridor"]],
    alt="Rudas Thermal Bath all-zones day ticket",
    pills=[
        pill("🎟️", "Desk vs online",
             "<strong>At the desk:</strong> all zones 12,000 HUF Mon–Thu, 15,000 HUF Fri–Sun, 16,000 HUF on holidays and in high season. "
             "<strong>Fast track:</strong> 15,000 / 18,000 / 19,000 HUF; online €45–57 with entry 12:00–15:00 or 16:00–19:00 (not Tue or Wed). "
             "<strong>Weekend early bird:</strong> fast-track entry 8:00–9:00 Sat and Sun, €42–45 online.",
             SHOP_NOTE),
        pill("🔐", "Locker or cabin",
             "A locker is included. A private cabin is <strong>1,000 HUF</strong> extra, a safe 1,100 HUF; a lost wristband costs 3,000 HUF.",
             "From the 2026 price list on rudasfurdo.hu."),
        pill("🕒", "Daily · 6:00–20:00",
             "<strong>Wellness and Turkish bath:</strong> 6:00–20:00, Mon until 22:00. <strong>Sauna world:</strong> from 8:00. "
             "The cash desk closes one hour before closing, and you must leave the pools 20 minutes before. 8 December 2026: open until 16:00.",
             OFFICIAL_NOTE, "bpa-time"),
        pill("💳", "Budapest Card −20%", "Budapest Card holders get 20% off daily tickets at Rudas. <a href=\"/budapest-card-is-it-worth-it\">Is the Budapest Card worth it?</a>"),
    ],
    pick="if you want the full bath without a set meal: Turkish bath, wellness, saunas and the rooftop pool on one ticket, the cheapest full Rudas day.",
    skip="on a Tuesday or Wednesday if you want the Turkish bath and it is not your day: it is women-only on Tuesday and men-only on Wednesday.",
    pros=[("Cheapest full day", "12,000 HUF on weekdays for every zone, against €74.99 for the meal package."),
          ("Fast track online", "Book an entry window online and skip the cash desk queue (€45–57)."),
          ("Early weekend entry", "Weekend fast track from 8:00, before the rooftop fills up."),
          ("Budapest Card discount", "20% off daily tickets with a Budapest Card.")],
    cons=[("Desk queues", "Without fast track you queue at the cash desk, which can take a while at weekends."),
          ("Weekends cost more", "15,000 HUF Fri–Sun, 16,000 HUF on holidays."),
          ("Kit not included", "Towel 6,900 HUF, slippers 4,200 HUF and a swim cap (needed in the swimming pool) 2,100 HUF at the desk.")],
    summary_q=("Is it cheaper to buy Rudas tickets at the desk?",
               "Yes. The desk price is 12,000 HUF Mon–Thu for all zones. Online fast-track tickets cost a little more but fix your entry window and skip the queue."),
    summary=["This is the ticket I would buy for a first visit without lunch plans. It covers all three parts of Rudas: the "
             "<strong>Ottoman Turkish bath</strong>, the <strong>wellness area with the sauna world</strong> and the <strong>36 °C rooftop panorama pool</strong>, plus the 29 °C swimming pool.",
             "My advice from my own visit: go on a Monday, Thursday or Friday after 11:00 for the co-ed Turkish bath, or on a weekend morning with the 8:00 fast-track ticket. "
             "The rooftop pool holds only 16 people, so it is far nicer before the midday crowd."],
    quotes=[("Brilliant bathhouse, especially the Turkish one with the sandstone columns and masonry", "Verified guest", "October 2026"),
            ("Really good experience loved it but was really busy", "Verified guest", "October 2026")],
    spcards=[
        ("Entrance &amp; Cash Desk", P["outside"],
         "The entrance is on Döbrentei tér at the Buda end of Elizabeth Bridge. Cash desks close one hour before closing; Hungarian forints only for cash."),
        ("Lockers &amp; Cabins", P["lockers"],
         "Your ticket includes a locker in the shared changing room, opened with a wristband. A private cabin costs 1,000 HUF extra."),
        ("Turkish Bath", P["turkish"],
         "Six pools at 28, 30, 33, 36 and 42 °C plus a cold plunge pool, recommended 20 minutes at a time. Check the men/women timetable before you go."),
        ("Rooftop Panorama Pool", P["roof_day"],
         "36 °C with a view over the Danube; 16 people fit at once."),
        ("Swimming Pool", None,
         "29 °C, 20.5 m long and 80 to 180 cm deep. A swim cap is mandatory."),
        ("Drinking Hall", P["drinking"],
         "The drinking fountain is open Tuesday and Thursday 10:00–14:00."),
    ],
    qf=[("Desk Prices 2026", "All zones 12,000 HUF Mon–Thu / 15,000 HUF Fri–Sun / 16,000 HUF holidays and high season"),
        ("Fast Track", "15,000 / 18,000 / 19,000 HUF · online €45–57, entry 12:00–15:00 or 16:00–19:00, not Tue or Wed"),
        ("Weekend Early Bird", "Fast track, entry 8:00–9:00 Sat and Sun: 14,000 HUF (€42–45 online)"),
        ("Cabin", "+1,000 HUF · locker included"),
        ("Opening Hours", "Daily 6:00–20:00, Mon until 22:00 · saunas from 8:00"),
        ("Towel &amp; Robe", "Towel 6,900 HUF · bathrobe 12,600 HUF · slippers 4,200 HUF"),
        ("Age Limit", "14+"),
        ("Address", "Döbrentei tér 9, 1013 Budapest")],
    amen=[("yes", "Turkish Bath"), ("yes", "Rooftop Pool"), ("yes", "Saunas"), ("yes", "Swimming Pool"),
          ("yes", "Locker"), ("no", "Towel"), ("no", "Step-Free Access")],
))

# ── 3 ─ Night bathing (official) ─────────────────────────────────────────────────────
CARDS.append(dict(
    key="night", anchor="item-3-rudas-night-bathing", cat="night weekend", tested=False,
    rank="🌙 #3 Best at Night", color="bpa-bronze",
    area="Rudas, District I", time="22:00–3:00", transport="Night bus 907, 973",
    title="Rudas Night Bathing (Fri &amp; Sat)", short="Night Bathing",
    book="official", official_url=OFFICIAL_SHOP, btn="Official Tickets →", ratings=[GOOGLE_RATING],
    price="45", psub="per person online · Fri &amp; Sat 22:00–3:00", via="rudasfurdo.hu",
    trust=["✓ Turkish bath + rooftop pool", "✓ Co-ed both nights"],
    photos=[P["roof_sunset"], P["turkish"], P["roof_day"], P["wellness"]],
    alt="Rudas Thermal Bath night bathing",
    pills=[
        pill("🕒", "Fri &amp; Sat · 22:00–3:00",
             "Every Friday and Saturday night. Co-ed in all sections.", OFFICIAL_NOTE, "bpa-time"),
        pill("🏊", "Turkish bath + rooftop",
             "Includes the Turkish bath, the swimming pool, the wellness pools and the rooftop panorama pool, with a cocktail bar on the roof."),
        pill("🚫", "No saunas at night",
             "The sauna world and massages are closed during night bathing. Slippers are mandatory."),
        pill("🎟️", "€45–54 online",
             "€45 online for Saturday 21 November 2026. The 2026 price list gives 15,000 HUF; on 1 and 2 January 2027 it is 18,000 HUF.",
             SHOP_NOTE),
    ],
    pick="for the most memorable Rudas visit: the Ottoman pools and the rooftop pool after dark, with the lights of the bridges, co-ed on both nights.",
    skip="if saunas matter to you (closed at night) or you have an early start the next morning.",
    pros=[("Co-ed Turkish bath", "Unlike weekdays, everyone can use the Turkish bath at night."),
          ("City lights", "The rooftop pool looks over the lit-up Elizabeth Bridge and the Danube."),
          ("Same price as a weekend day", "€45–54 online, about the same as a weekend day ticket.")],
    cons=[("No saunas or massages", "The sauna world is closed during night bathing."),
          ("Late finish", "It ends at 3:00; you get home by night bus 907 or 973 or taxi."),
          ("Weekends only", "Friday and Saturday nights only.")],
    summary_q=("Is Rudas night bathing worth it?",
               "Yes, if you want an evening plan that is not a bar: the Turkish bath and the rooftop pool feel very different after dark. Skip it if you came for the saunas."),
    summary=["Night bathing turns Rudas into an evening out: the 16th-century Turkish bath lit up after dark, the rooftop pool above the "
             "Elizabeth Bridge lights and a cocktail bar on the roof. On Friday and Saturday nights all sections are <strong>co-ed</strong>, "
             "so couples and mixed groups can do the Turkish bath together.",
             "Buy the ticket on the official site and bring flip-flops: they are mandatory at night. The sauna world is closed, so if saunas "
             "are the point of your visit, come during the day."],
    quotes=[],
    spcards=[
        ("What Is Open", P["turkish"],
         "Turkish bath, swimming pool, wellness pools and the rooftop panorama pool. The sauna world and massages are closed."),
        ("Rooftop at Night", P["roof_sunset"],
         "The 36 °C panorama pool with a cocktail bar on the roof terrace."),
        ("Getting Home", None,
         "Night buses 907 and 973 stop at the bath; taxis wait on Döbrentei tér."),
    ],
    qf=[("Nights", "Friday and Saturday, 22:00–3:00"),
        ("Price", "€45–54 online (€45 on Sat 21 Nov 2026) · 15,000 HUF on the 2026 price list · 18,000 HUF on 1–2 January 2027"),
        ("Includes", "Turkish bath, swimming pool, wellness pools, rooftop panorama pool"),
        ("Closed at Night", "Sauna world and massages"),
        ("Bring", "Swimsuit, towel and flip-flops (mandatory)"),
        ("Age Limit", "14+"),
        ("Night Transport", "Night buses 907, 973")],
    amen=[("yes", "Turkish Bath"), ("yes", "Rooftop Pool"), ("yes", "Rooftop Bar"), ("yes", "Co-ed"),
          ("no", "Saunas"), ("no", "Massages")],
))

# ── 4 ─ Single-zone ticket (official) ────────────────────────────────────────────────
CARDS.append(dict(
    key="single-zone", anchor="item-4-rudas-single-zone", cat="budget day weekday", tested=False,
    rank="🪙 #4 Cheapest Way In", color="bpa-slate",
    area="Rudas, District I", time="2 Hours", transport="Tram 19, 41 · Bus 7",
    title="Turkish Bath or Wellness-Only Ticket", short="Single-Zone Ticket",
    book="official", official_url=OFFICIAL_SHOP, btn="Official Tickets →", ratings=[GOOGLE_RATING],
    price_label="8,000 HUF", price_huf="8000", psub="at the desk, Mon/Thu/Fri until 10:45 · €24 online Tue/Wed", via="rudasfurdo.hu",
    trust=["✓ One zone, full day", "✓ Upgrade at the desk"],
    photos=[P["turkish"], P["wellness"], P["roof_day"], P["drinking"]],
    alt="Rudas Turkish bath single-zone ticket",
    pills=[
        pill("🕒", "Which days",
             "<strong>Online, €24:</strong> Tuesday and Wednesday, Turkish bath <em>or</em> Wellness-Spa. "
             "<strong>At the desk, 8,000 HUF:</strong> Monday, Thursday and Friday until 10:45.",
             SHOP_NOTE, "bpa-time"),
        pill("🚻", "Men / women",
             "Turkish bath on <strong>Tuesday: women only</strong>; <strong>Wednesday: men only</strong>; Mon, Thu and Fri mornings until 10:45: men only.",
             OFFICIAL_NOTE),
        pill("➕", "Upgrade to all zones",
             "A supplement ticket adds the other zone: 4,000 HUF Mon–Thu, 7,000 HUF on Friday."),
    ],
    pick="for a short, cheap Ottoman soak: women on a Tuesday, men on a Wednesday or a weekday morning, or the Wellness-Spa ticket with the rooftop pool for anyone.",
    skip="if you want the Turkish bath and the rooftop pool together: the all-zones day ticket costs only 4,000 HUF more.",
    pros=[("Cheapest ticket", "8,000 HUF at the desk or €24 online."),
          ("Rooftop included in Wellness", "The Wellness-Spa ticket includes the swimming pool, the sauna world, the panorama pool and a locker."),
          ("Quieter days", "Single-gender days in the Turkish bath are calmer than co-ed weekends.")],
    cons=[("One zone only", "The Turkish bath ticket excludes the rooftop; the Wellness ticket excludes the Turkish bath."),
          ("Limited days", "Online only Tue and Wed; at the desk only weekday mornings until 10:45.")],
    summary_q=("What is the cheapest way into Rudas?",
               "A single-zone ticket: 8,000 HUF at the desk on Mon, Thu and Fri mornings, or €24 online on Tuesday and Wednesday."),
    summary=["If you only want the Turkish bath, you don't need an all-zones ticket. On <strong>Tuesday (women)</strong> and <strong>Wednesday (men)</strong> "
             "the Turkish bath ticket is €24 online, and on Monday, Thursday and Friday mornings until 10:45 it is 8,000 HUF at the desk (men only).",
             "The <strong>Wellness-Spa</strong> ticket at the same price is the better deal for most visitors: it includes the rooftop panorama pool, "
             "the swimming pool and the sauna world, just not the Turkish bath."],
    quotes=[],
    spcards=[
        ("Turkish Bath Ticket", P["turkish"],
         "The six thermal pools and three Finnish saunas (45, 55 and 72 °C) of the Turkish bath, plus a steam cabin."),
        ("Wellness-Spa Ticket", P["wellness"],
         "Swimming pool, wellness pools, the sauna world, the rooftop panorama pool and a locker. Not valid for the Turkish bath."),
    ],
    qf=[("Desk Price", "8,000 HUF, Mon, Thu and Fri until 10:45 (Turkish bath or wellness-spa)"),
        ("Online Price", "€24, Tuesday and Wednesday"),
        ("Supplement", "Other zone +4,000 HUF Mon–Thu, +7,000 HUF Fri"),
        ("Turkish Bath Rules", "Tue women only · Wed men only · Mon, Thu, Fri until 10:45 men only"),
        ("Age Limit", "14+")],
    amen=[("yes", "Turkish Bath or Wellness"), ("yes", "Locker"), ("no", "Both Zones")],
))

# ── 5 ─ Private panoramic bathing (official) ─────────────────────────────────────────
CARDS.append(dict(
    key="private", anchor="item-5-rudas-private-rooftop", cat="couples night", tested=False,
    rank="💍 #5 Best for Couples", color="bpa-slate",
    area="Rudas, District I", time="1 Hour", transport="Tram 19, 41 · Bus 7",
    title="Private Panoramic Bathing for Two", short="Private Rooftop Hour",
    book="official", official_url=OFFICIAL_SHOP, btn="Official Tickets →", ratings=[GOOGLE_RATING],
    price="117", psub="per person, 2 people minimum · 20:00–21:00", via="rudasfurdo.hu",
    trust=["✓ Rooftop pool to yourselves", "✓ Bottle of sparkling wine"],
    photos=[P["roof_sunset"], P["roof_day"]],
    alt="Rudas rooftop panorama pool private bathing",
    pills=[
        pill("🕒", "Tue–Sat · 20:00–21:00",
             "One hour on the rooftop, 20:00–21:00, Tuesday to Saturday. Arrive by 19:40.", OFFICIAL_NOTE, "bpa-time"),
        pill("🍾", "What is included",
             "Exclusive use of the panorama pool for 2 guests and a bottle of Hungarian sparkling wine. Bring slippers and towels."),
        pill("👥", "Up to 6 guests",
             "Up to 4 extra guests can be added at the bath; arrange it in advance with rudasinfo@budapestspas.hu."),
    ],
    pick="for a proposal, an anniversary or a birthday: the rooftop pool and the city lights to yourselves for an hour.",
    skip="if you also want the Turkish bath and the saunas: this is the rooftop pool only.",
    pros=[("No crowds", "The only way to have the 16-person rooftop pool to yourselves."),
          ("Sparkling wine included", "A bottle of Hungarian sparkling wine for the two of you.")],
    cons=[("Expensive per hour", "€117–147 per person for one hour."),
          ("Rooftop only", "No Turkish bath or saunas in the package.")],
    summary_q=("Can you rent the Rudas rooftop pool privately?",
               "Yes. The private panoramic bathing package gives two people the rooftop pool from 20:00 to 21:00, Tuesday to Saturday, with a bottle of sparkling wine."),
    summary=["The rooftop panorama pool is the most popular spot in Rudas and it holds only 16 people. This package gives it to the two of you for an hour "
             "after dark, with the lights of the Danube bridges and a bottle of Hungarian sparkling wine.",
             "Book it on the official site; the price is <strong>€117–147 per person</strong> depending on the date, for at least two people."],
    quotes=[],
    spcards=[
        ("The Rooftop Hour", P["roof_sunset"],
         "Exclusive access to the 36 °C panorama pool from 20:00 to 21:00. Arrive by 19:40."),
    ],
    qf=[("Price", "€117–147 per person, minimum 2 people"),
        ("When", "Tuesday to Saturday, 20:00–21:00 (arrive by 19:40)"),
        ("Includes", "1 hour of private rooftop pool access, a bottle of Hungarian sparkling wine"),
        ("Extra Guests", "Up to 4, arranged in advance with the bath"),
        ("Bring", "Slippers and towels")],
    amen=[("yes", "Private Rooftop Pool"), ("yes", "Sparkling Wine"), ("no", "Turkish Bath"), ("no", "Saunas")],
))


# ── shared bits from the reference page (same as build_thermal_baths_2026.py) ────────
_ref_card = deck_card(RIVER, "card-2")
ICON = {m.group(1): m.group(0) for m in re.finditer(r'<img alt="([^"]+)" class="bpa-rev-icon"[^>]*>', _ref_card)}
ICON["Google"] = '<img alt="Google" class="bpa-rev-icon" loading="lazy" src="/assets/cdn/60e43c7d6d05b671dff0dc1a/65350288cf6e222fd93f3743_google-icon.png"/>'
_ref_det = details_card(RIVER, "cruise-2-rubingroup")
LOCK_SVG = re.search(r'<svg fill="none"[^>]*>.*?</svg>', _ref_det, re.S).group(0)
SIZES = "(max-width: 767px) 420px, (max-width: 991px) 55vw, (max-width: 1439px) 49vw, 50vw"
PLACEHOLDER = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 500'%3E%3C/svg%3E"
AFF_REL = "nofollow sponsored noopener"


def fmt_count(n):
    if n >= 1000:
        v = math.floor(n / 100) / 10
        return ("%.1f" % v).rstrip("0").rstrip(".") + "k+"
    if n >= 20:
        return "%d+" % (n // 10 * 10)
    return str(n)


def fmt_total(n):
    if n >= 10000:
        return "%dk+" % (n // 1000)
    return fmt_count(n)


def wavg(r):
    tot = sum(x[2] for x in r)
    return sum(x[1] * x[2] for x in r) / tot, tot


def score1(s):
    return "%.1f" % (math.floor(s * 10 + 0.5) / 10)


def amp(u):
    return u.replace("&amp;", "&").replace("&", "&amp;")


def gyg(c, placement):
    return amp(GYG.format(slug=GYG_SLUG, placement=placement, key=c["key"]))


def book_url(c, placement):
    return gyg(c, placement) if c["book"] == "gyg" else amp(c["official_url"])


def book_rel(c):
    return AFF_REL if c["book"] == "gyg" else "nofollow noopener"


def price_txt(c):
    return "From €%s" % c["price"] if c.get("price") else "From %s" % c["price_label"]


def maps(q):
    return amp(MAPS.format(q=urllib.parse.quote_plus(q)))


def rate_block(c):
    avg, tot = wavg(c["ratings"])
    r = c["ratings"][0]
    site = r[0]
    inner = ('%s<span class="bpa-rev-site">%s</span><span class="bpa-rev-score">%s</span><span class="bpa-rev-count">(%s)</span>'
             % ("\n" + ICON[site], site, score1(r[1]), fmt_count(r[2])))
    if c["book"] == "gyg" and r[3] == "gyg":
        badge = ('<a class="bpa-rev-badge is-link" href="%s" rel="nofollow sponsored noopener" target="_blank">%s'
                 '<span class="bpa-rev-go" aria-hidden="true">→</span></a>' % (gyg(c, "rating"), inner))
        head = "Rating on GetYourGuide for this ticket"
        note = ""
    else:
        badge = '<span class="bpa-rev-badge is-static">%s</span>' % inner
        head = "Rating of Rudas Thermal Bath on Google Maps"
        note = '<span class="bpa-lang-note">The official tickets have no reviews of their own, so this is the bath&rsquo;s overall rating.</span>'
    meta = "%s reviews · %s" % (fmt_total(tot), site)
    return ('<div class="bpa-summary-reviews bpa-rate"><details class="bpa-lang bpa-rate-more"><summary class="bpa-rate-sum">'
            '<span class="bpa-stars" style="--r:%.2f" aria-hidden="true"></span><b class="bpa-rate-score">%s</b>'
            '<span class="bpa-rate-meta">%s</span><span class="bpa-lang-chev" aria-hidden="true">▾</span></summary>'
            '<div class="bpa-lang-pop"><strong>%s</strong><span class="bpa-rate-list">%s</span>%s</div></details></div>'
            % (avg, score1(avg), meta, head, badge, note))


def media(i, c):
    tag = '<span class="bpa-rank-tag %s">%s</span>' % (c["color"], c["rank"])
    arrows = ('<button aria-label="Previous photo" class="bpa-arrow prev" onclick="bpaSlide(this,-1)" type="button">‹</button>'
              '<button aria-label="Next photo" class="bpa-arrow next" onclick="bpaSlide(this,1)" type="button">›</button>')
    imgs = []
    for k, p in enumerate(c["photos"][:12]):
        if k == 0:
            extra = ' fetchpriority="high" loading="eager"' if i == 1 else ' loading="lazy"'
            imgs.append('<img alt="%s"%s height="534" sizes="%s" src="%s" width="800"/>' % (c["alt"], extra, SIZES, p))
        else:
            imgs.append('<img alt="%s" data-src="%s" decoding="async" height="534" loading="lazy" sizes="%s" src="%s" width="800"/>'
                        % (c["alt"], p, SIZES, PLACEHOLDER))
    slider = ('<div aria-label="Photo gallery %d" class="bpa-slider" onscroll="bpaCount(this)" tabindex="0">\n%s</div>'
              % (i, "\n".join(imgs)))
    return '<div class="bpa-media">\n%s\n%s<span class="bpa-pill">1 / %d</span>%s\n</div>' % (tag, arrows, len(imgs), slider)


def deck_html(i, c):
    tested_pill = proof = ""
    if c["tested"]:
        proof = '\n<div class="bpa-proof"><span class="bpa-vchip">✓ Personally Tested</span></div>'
        tested_pill = ('<details class="bpa-lang bpa-tested bpa-proof-mobile"><summary class="bpa-vchip bpa-proof-mobile">✓ Personally Tested'
                       '<span class="bpa-lang-chev" aria-hidden="true">▾</span></summary><div class="bpa-lang-pop">%s'
                       '<span class="bpa-lang-note">What I checked: pools, changing rooms, crowds and value for money. '
                       '<a href="#%s">Full review ↓</a></span></div></details>\n' % (TESTED_POP, c["anchor"]))
    kicker = ('%s • ⏱️ %s • <a class="bpa-kicker-map-link" href="%s" onclick="event.stopPropagation()" rel="noopener noreferrer" target="_blank">%s</a>'
              % (c["area"], c["time"], maps(MAPS_Q), c["transport"]))
    trust = "".join("<span>%s</span>" % t for t in c["trust"])
    btn = "Check Availability →" if c["book"] == "gyg" else c["btn"]
    via = ("Booked securely via " if c["book"] == "gyg" else "Official tickets at ") + c["via"]
    return f'''<div class="bpa-card" data-cat="{c["cat"]}" id="card-{i}">
<div class="bpa-main">
{media(i, c)}
<div class="bpa-info">
<div class="bpa-kicker">{kicker}</div>
<a class="bpa-title" href="{book_url(c, "card")}" rel="{book_rel(c)}" target="_blank">{c["title"]}</a>
<div class="bpa-reviews-line">
{rate_block(c)}{proof}
</div>
<div class="bpa-specs-row">
{tested_pill}{"".join(c["pills"])}
</div>
<div class="bpa-best-for bpa-pickskip"><span class="bpa-pick">✓ Pick it</span> {c["pick"]} <span class="bpa-skip">✕ Skip it</span> {c["skip"]}</div>
</div>
<div class="bpa-cta-cell">
<div>
<div class="bpa-price">{price_txt(c)}</div>
<div class="bpa-psub">{c["psub"]}</div>
</div>
<a class="bpa-btn" href="{book_url(c, "button")}" rel="{book_rel(c)}" target="_blank">{btn}</a>
<div class="bpa-via">{via}</div>
<div class="bpa-trust2">{trust}</div>
<a class="bpa-sublink" href="#{c["anchor"]}">Read Review ↓</a>
</div>
</div>
</div>'''


def det_header(c):
    proof = '\n<div class="bpa-proof"><span class="bpa-vchip">✓ Personally Tested</span></div>' if c["tested"] else ""
    return f'''<details class="bpa-details-card" data-cat="{c["cat"]}" id="{c["anchor"]}" open="">
<summary class="bpa-details-summary">
<div class="bpa-details-summary-content">
<div class="bpa-details-top-row">
<span class="bpa-rank-tag {c["color"]}">{c["rank"]}</span>
<div class="bpa-kicker">{c["area"]} • ⏱️ {c["time"]} • <span class="bpa-kicker-map-link">{c["transport"]}</span></div>
</div>
<h3 class="bpa-details-title">{c["title"]}</h3>
<div class="bpa-reviews-line">
{rate_block(c)}{proof}
</div>
</div>
<div class="bpa-details-right">
<span class="bpa-details-price">{price_txt(c)}</span>
<div class="bpa-details-toggle">
<span class="bpa-details-state-text"></span>
<span class="bpa-details-chevron">▾</span>
</div>
</div>
</summary>
<div class="bpa-details-body">
'''


def proscons(c):
    pros = "".join("<li><strong>%s:</strong> %s</li>" % p for p in c["pros"])
    cons = "".join("<li><strong>%s:</strong> %s</li>" % p for p in c["cons"])
    return ('<div class="pro-con-box-wrapper"><div class="w-layout-grid grid-15"><div class="pro-con-box-pro-cell" data-wf-pbl="layout-grid-1x2-vertical">'
            '<div class="pro-con-box-pro-cell-rich-text-block w-richtext"><h3><strong>Pros:</strong></h3><ul role="list">%s</ul></div></div>'
            '<div class="pro-con-box-con-cell" data-wf-pbl="layout-grid-1x2-vertical"><div class="pro-con-box-con-cell-rich-text-block w-richtext">'
            '<h3><strong>Cons:</strong></h3><ul role="list">%s</ul></div></div></div></div>' % (pros, cons))


def buycard(c):
    if c["book"] == "gyg":
        badge, cta, trustline = "Tickets &amp; Live Availability", "Check Dates &amp; Book Tickets", c["trust"][0].replace("✓ ", "")
        perks = ["Booked via %s" % c["via"], c["trust"][1].replace("✓ ", "")]
    else:
        badge, cta, trustline = "Official Tickets &amp; Prices", "Book on the Official Site", "Sold by the bath itself (rudasfurdo.hu)"
        perks = [t.replace("✓ ", "") for t in c["trust"]]
    perks += ["Address: <strong>Döbrentei tér 9, 1013 Budapest</strong>", "Suggested time: <strong>%s</strong>" % c["time"]]
    perk_html = "\n".join('<span class="ltt-buy-perk">%s</span>' % p for p in perks)
    return f'''<div class="ltt-buy-card">
<div class="ltt-buy-card-head">
<div class="ltt-buy-card-badge">
<span class="ltt-live-dot"></span>
<span>{badge}</span>
</div>
<div class="ltt-buy-card-price">
<span class="ltt-buy-price-val">{price_txt(c)}</span>
<span class="ltt-buy-price-sub">{c["psub"]}</span>
</div>
</div>
<div class="ltt-buy-card-body">
<div class="ltt-buy-card-info">
<h4 class="ltt-buy-card-title">{c["short"]}</h4>
<div class="ltt-buy-card-perks">
{perk_html}
</div>
</div>
<div class="ltt-buy-card-action">
<a class="ltt-buy-cta-btn" href="{book_url(c, "review")}" rel="{book_rel(c)}" target="_blank">
<span>{cta}</span>
<span class="ltt-cta-arrow">→</span>
</a>
<div class="ltt-buy-card-trust">
{LOCK_SVG}
<span>{trustline}</span>
</div>
</div>
</div>
</div>'''


def qf(c):
    rows = "\n".join('<div class="qf1-row"><div class="qf1-label">%s</div><div class="qf1-val">%s</div></div>' % r for r in c["qf"])
    chips = "\n".join('<span class="qf1-chip %s">%s %s</span>' % (k, "✓" if k == "yes" else "✕", t) for k, t in c["amen"])
    return f'''<div class="qf1-wrap">
<div class="qf1-title-row">
<h4 class="qf1-title">Quick Facts: Verified Ticket Specs</h4>
<span class="qf1-badge">{c["short"]}</span>
</div>
<div class="qf1-table">
{rows}
</div>
<div class="qf1-Validation-pills">
{chips}
</div>
</div>'''


def bento(title, pill_txt, body):
    return f'''<details class="ltt-bento-group" open="">
<summary class="ltt-bento-group-head">
<span class="ltt-bento-group-title">{title}</span>
<span class="ltt-bento-right">
<span class="ltt-mini-pill">{pill_txt}</span>
<span class="ltt-bento-chev">▾</span>
</span>
</summary>
<div class="ltt-bento-group-body">
{body}
</div>
</details>'''


def body_html(c):
    q, a = c["summary_q"]
    paras = "".join("<p>%s</p>" % p for p in c["summary"])
    quotes = ""
    if c["quotes"]:
        quotes = "<blockquote><strong>What visitors say:</strong><br/>%s</blockquote>" % "<br/>".join(
            "“%s” <em>(%s, %s)</em>" % qq for qq in c["quotes"])
    getthere = '<h3>How to Get There</h3><ul role="list">%s</ul>' % "".join("<li>%s</li>" % x for x in GETTHERE)
    summary = ('<div class="w-richtext"><blockquote>❓ <strong>%s</strong><br/>💡 %s</blockquote>%s%s%s</div>\n%s'
               % (q, a, paras, quotes, getthere, buycard(c)))
    cards = []
    for h, img, txt in c["spcards"]:
        im = '<img alt="Rudas Thermal Bath: %s" loading="lazy" src="%s"/>' % (h.replace("&amp;", "and"), img) if img else ""
        cards.append('<div class="ltt-sp-card"><h4>%s</h4>%s<ul role="list"><li>%s</li></ul></div>' % (h, im, txt))
    inside = '<div class="ltt-sub-points">\n%s\n</div>' % "\n".join(cards)
    label = "From My Visit" if c["tested"] else "From Official Info"
    return (proscons(c) + "\n" + bento("Summary &amp; Review Overview", "Overview", summary) + "\n"
            + bento("What This Ticket Gets You", label, inside) + "\n" + qf(c) + "\n")


def details_html(c):
    return det_header(c) + body_html(c) + "</div>\n</details>"


# ── page-level copy ──────────────────────────────────────────────────────────────────
N = len(CARDS)
TITLE = "Rudas Baths Budapest 2026: Tickets, Prices &amp; Night Bathing"
TITLE_TXT = "Rudas Baths Budapest 2026: Tickets, Prices & Night Bathing"
DESC = ("Rudas Baths tickets compared: desk 12,000 HUF vs €74.99 bath + meal, night bathing Fri and Sat 22:00 to 3:00, "
        "the men/women Turkish bath timetable and the rooftop pool.")
H1 = 'Rudas Baths Budapest: Which Ticket to Book in 2026 <span class="ltt-h1-muted">(Personally Tested)</span>'

LEAD = f'''<div class="ltt-lead-copy">
<p>Most visitors book Rudas online as a <strong>€74.99 bath + meal package</strong>, while the same bath costs <strong>12,000 HUF at the desk</strong> on a weekday. The bigger trap is the day: the Ottoman Turkish bath is <strong>women-only on Tuesdays and men-only on Wednesdays</strong>, and the 36 °C rooftop pool holds just 16 people at a time.</p>
<p>I bathed at Rudas myself, then compared the <strong>{N} ways to get in</strong> side by side: the day pass with a 3-course meal, the official day and fast-track tickets, <strong>Friday and Saturday night bathing (22:00 to 3:00)</strong>, the cheap single-zone ticket and a private rooftop hour for two.</p>
<p>Comparing baths? See <a href="{HUB}">all Budapest thermal baths</a>{SZE_LINK}.</p>
</div>'''


def count(tok):
    return sum(tok in c["cat"].split() for c in CARDS)


FILTERS = [("tested", "Personally Tested"), ("meal", "Includes a Meal"), ("night", "Night"),
           ("budget", "Under €30"), ("couples", "Couples"), ("weekend", "Weekends")]
PILLS = ('<div class="ltt-integrated-pills">\n'
         '<button class="ltt-tab-btn active" data-cat="all" onclick="lttFilterItems(\'all\', this)" type="button">All (%d)</button>\n' % N
         + "\n".join('<button class="ltt-tab-btn" data-cat="%s" onclick="lttFilterItems(\'%s\', this)" type="button">%s (%d)</button>'
                     % (k, k, lab, count(k)) for k, lab in FILTERS)
         + "\n</div>")

QUICK = f'''<div class="container w-container"><div class="w-richtext bpa-wt-guide">
<h2 id="which-rudas-ticket">Which Rudas Ticket Should You Book?</h2>
<ul>
<li><strong>Bath plus lunch or dinner, free cancellation:</strong> <a href="#item-1-rudas-day-pass-meal">Day Pass + 3-Course Meal</a> (from €74.99 Mon–Thu, €129.90 at weekends).</li>
<li><strong>The full bath for the least money:</strong> <a href="#item-2-rudas-day-ticket">All-Zones Day Ticket</a> (12,000 HUF at the desk Mon–Thu, fast track online from €45).</li>
<li><strong>An evening plan, co-ed Turkish bath:</strong> <a href="#item-3-rudas-night-bathing">Night Bathing</a> (Fri and Sat 22:00 to 3:00, €45–54 online).</li>
<li><strong>Just the Turkish bath, on a budget:</strong> <a href="#item-4-rudas-single-zone">Single-Zone Ticket</a> (8,000 HUF or €24).</li>
<li><strong>A proposal or anniversary:</strong> <a href="#item-5-rudas-private-rooftop">Private Rooftop Hour</a> (€117–147 per person, 20:00–21:00).</li>
</ul>
<h2 id="rudas-turkish-bath-men-women-timetable">Turkish Bath Timetable: Men, Women and Co-ed Days</h2>
<p>This decides your day more than anything else. Outside the times below, the wellness area, saunas and rooftop pool are co-ed every day.</p>
<div style="overflow-x:auto"><table class="bpa-rudas-table" style="width:100%;border-collapse:collapse;font-size:15px">
<thead><tr><th style="text-align:left;padding:8px;border-bottom:2px solid #e2e8f0">Day</th><th style="text-align:left;padding:8px;border-bottom:2px solid #e2e8f0">Turkish bath</th></tr></thead>
<tbody>
<tr><td style="padding:8px;border-bottom:1px solid #e2e8f0"><strong>Monday</strong></td><td style="padding:8px;border-bottom:1px solid #e2e8f0">Men only 6:00–10:45 · co-ed 11:00–22:00</td></tr>
<tr><td style="padding:8px;border-bottom:1px solid #e2e8f0"><strong>Tuesday</strong></td><td style="padding:8px;border-bottom:1px solid #e2e8f0">Women only 6:00–20:00</td></tr>
<tr><td style="padding:8px;border-bottom:1px solid #e2e8f0"><strong>Wednesday</strong></td><td style="padding:8px;border-bottom:1px solid #e2e8f0">Men only 6:00–20:00</td></tr>
<tr><td style="padding:8px;border-bottom:1px solid #e2e8f0"><strong>Thursday, Friday</strong></td><td style="padding:8px;border-bottom:1px solid #e2e8f0">Men only 6:00–10:45 · co-ed 11:00–20:00</td></tr>
<tr><td style="padding:8px;border-bottom:1px solid #e2e8f0"><strong>Saturday, Sunday</strong></td><td style="padding:8px;border-bottom:1px solid #e2e8f0">Co-ed 6:00–20:00</td></tr>
<tr><td style="padding:8px"><strong>Fri and Sat night</strong></td><td style="padding:8px">Co-ed 22:00–3:00 (night bathing)</td></tr>
</tbody></table></div>
<p>Co-ed sessions are in swimwear. Source: <a href="{OFFICIAL_HOURS}" rel="nofollow noopener" target="_blank">official opening hours</a>.</p>
<h2 id="rudas-desk-vs-online">Desk or Online: What Each Ticket Costs</h2>
<div style="overflow-x:auto"><table class="bpa-rudas-table" style="width:100%;border-collapse:collapse;font-size:15px">
<thead><tr><th style="text-align:left;padding:8px;border-bottom:2px solid #e2e8f0">Ticket</th><th style="text-align:left;padding:8px;border-bottom:2px solid #e2e8f0">Mon–Thu</th><th style="text-align:left;padding:8px;border-bottom:2px solid #e2e8f0">Fri–Sun</th></tr></thead>
<tbody>
<tr><td style="padding:8px;border-bottom:1px solid #e2e8f0">All zones, desk</td><td style="padding:8px;border-bottom:1px solid #e2e8f0">12,000 HUF</td><td style="padding:8px;border-bottom:1px solid #e2e8f0">15,000 HUF</td></tr>
<tr><td style="padding:8px;border-bottom:1px solid #e2e8f0">All zones, fast track</td><td style="padding:8px;border-bottom:1px solid #e2e8f0">15,000 HUF</td><td style="padding:8px;border-bottom:1px solid #e2e8f0">18,000 HUF</td></tr>
<tr><td style="padding:8px;border-bottom:1px solid #e2e8f0">Bath + 3-course meal</td><td style="padding:8px;border-bottom:1px solid #e2e8f0">from €74.99</td><td style="padding:8px;border-bottom:1px solid #e2e8f0">€129.90</td></tr>
<tr><td style="padding:8px;border-bottom:1px solid #e2e8f0">Night bathing</td><td style="padding:8px;border-bottom:1px solid #e2e8f0">-</td><td style="padding:8px;border-bottom:1px solid #e2e8f0">€45–54 (Fri, Sat)</td></tr>
<tr><td style="padding:8px;border-bottom:1px solid #e2e8f0">Single zone</td><td style="padding:8px;border-bottom:1px solid #e2e8f0">8,000 HUF or €24</td><td style="padding:8px;border-bottom:1px solid #e2e8f0">-</td></tr>
<tr><td style="padding:8px">Private cabin</td><td style="padding:8px">+1,000 HUF</td><td style="padding:8px">+1,000 HUF</td></tr>
</tbody></table></div>
<p>Holidays and high season: 16,000 HUF at the desk, 19,000 HUF fast track. The desk takes cards; for cash, Hungarian forints only.</p>
{{HUBNAV}}</div></div>
'''

SECTIONS = [
    ("rudas-know-before-you-go", "Rudas Baths: Know Before You Go", f'''
<h3>What to Bring</h3><p>Swimsuit, towel and flip-flops (mandatory at night), plus a swim cap if you want the swimming pool. None of the tickets include a towel. At the desk: towel 6,900 HUF, bathrobe 12,600 HUF, slippers 4,200 HUF, swim cap 2,100 HUF, swimsuit 6,300 HUF.</p>
<h3>Locker or Cabin?</h3><p>Every ticket includes a <strong>locker</strong> in a shared changing room, opened with a wristband (3,000 HUF if lost). A <strong>private cabin</strong> costs 1,000 HUF extra: worth it if you are two and want to change in private.</p>
<h3>Rooftop Pool</h3><p>The 36 °C panorama pool fits <strong>16 people</strong>. It fills up from late morning, so go early (weekend fast track from 8:00) or at night.</p>
<h3>Age Limit and Access</h3><p>Rudas does not admit <strong>children under 14</strong>, at any time. The bath is <strong>not step-free</strong>: for technical reasons it currently cannot receive guests with reduced mobility.</p>
<h3>Getting There</h3><p>Rudas is at Döbrentei tér 9, at the Buda end of Elizabeth Bridge. Take <strong>tram 19, 41, 56 or 56A</strong>, or <strong>bus 7, 8E, 108E, 110 or 112</strong>. From the Pest side it is a 10-minute walk across Elizabeth Bridge. After night bathing: night buses 907 and 973.</p>
<h3>Plan the Rest of Your Day</h3><p>Rudas is a 10-minute walk from the Pest side, so it pairs well with a <a href="/best-walking-tours-budapest">walking tour</a> in the morning or a <a href="/best-night-cruises-budapest">night cruise on the Danube</a> after your bath. If you hold a <a href="/budapest-card-is-it-worth-it">Budapest Card</a>, it takes 20% off Rudas day tickets. For more ideas, see the <a href="/best-things-to-do-budapest">best things to do in Budapest</a>.</p>
<h3>Holiday Hours</h3><p>On 8 December 2026 the bath closes at 16:00. On public holidays it follows weekend hours. The cash desk closes one hour before closing time.</p>'''),
    ("rudas-how-i-compared", "How I Compared Rudas Tickets", f'''
<p>I bathed at Rudas myself: Turkish bath, wellness area, saunas and the rooftop pool. For this page I rechecked every ticket on {TODAY_TXT}: the official price list, opening hours and pool temperatures on rudasfurdo.hu, the official online ticket shop, and the bath + meal package on its booking calendar for Thursday 19 and Saturday 21 November 2026.</p>
<p>The cards are ranked by who they suit best, not by commission: the official tickets link straight to the bath and earn this site nothing. Ratings are for the exact product where it has its own reviews; the official tickets show the bath's Google Maps rating.</p>'''),
]

FAQ = [
    ("How much is Rudas Baths in 2026?",
     "At the desk, an all-zones ticket is 12,000 HUF Monday to Thursday and 15,000 HUF Friday to Sunday (16,000 HUF on holidays). Fast track is 15,000 / 18,000 HUF. The bath + 3-course meal package starts at €74.99 on weekdays."),
    ("Is the Rudas Turkish bath men only?",
     "Only at certain times: men only on Wednesday all day and on Monday, Thursday and Friday until 10:45; women only on Tuesday. It is co-ed on Monday, Thursday and Friday afternoons, all weekend and during night bathing."),
    ("When is night bathing at Rudas?",
     "Every Friday and Saturday from 22:00 to 3:00. Tickets are €45–54 on the official site (15,000 HUF on the price list). The saunas are closed at night."),
    ("Can children go to Rudas Baths?",
     "No. Rudas does not admit children under 14. For a family visit, choose Palatinus, which has kids' pools."),
    ("Is Rudas wheelchair accessible?",
     "No. For technical reasons Rudas currently cannot receive guests with reduced mobility."),
    ("Should I book Rudas tickets online or buy at the desk?",
     "The desk is cheapest (12,000 HUF on weekdays). Book online if you want fast-track entry, free cancellation or the meal package, or for night bathing."),
    ("Is Rudas better than Széchenyi?",
     "For atmosphere and views, often yes: the Ottoman Turkish bath and the rooftop pool are unique. Széchenyi has bigger outdoor pools and more of them."),
]


def faq_html():
    cards = []
    for k, (q, a) in enumerate(FAQ):
        first = " first" if k == 0 else ""
        cards.append('<div class="cf-faq-plus-card"><div class="cf-faq-question-container-3%s"><div class="cf-faq-question-wrap">'
                     '<h3 class="cf-faq-questions-2">%s</h3><div class="cf-faq-icon-contain"><div class="cf-faq-line"></div>'
                     '<div class="cf-faq-line-vertical"></div></div></div></div><div class="cf-faq-answer-wrap-2">'
                     '<div class="cf-faq-content-2 w-richtext"><p>%s</p></div></div><div class="cf-bottom-line-2"></div></div>' % (first, q, a))
    return '<div class="cf-faq-container" id="faq"><h2 id="faq-rudas">Frequently Asked Questions</h2><div class="cf-faqs-container">%s</div></div>' % "".join(cards)


def editorial_html():
    secs = "".join('<section class="w-richtext" id="%s" style="margin-bottom: 48px;"><div class="container w-container"><h2>%s</h2><div class="w-richtext">%s\n</div></div></section>\n'
                   % (sid, h, body) for sid, h, body in SECTIONS)
    return '<div class="ltt-editorial-wrapper" role="main">\n%s%s\n</div>' % (secs, faq_html())


# ── shared "Budapest Bath Guides" block (copied from scripts/bath_hub_nav.py on article/thermal-baths-hub) ──

GUIDES = [
    ("hub", "/thermal-baths-budapest", "♨️", "All Budapest Thermal Baths",
     "6 open baths compared: prices, pools, crowds"),
    ("szechenyi", "/szechenyi-baths-budapest", "🏛️", "Széchenyi Baths Tickets",
     "Day ticket from €39, locker vs cabin, VIP and Beer Spa"),
    ("rudas", "/rudas-baths-budapest", "🕌", "Rudas Baths Tickets",
     "Turkish bath, rooftop pool, weekend night bathing"),
    ("sparty", "/sparty-budapest", "🎉", "Sparty Budapest",
     "Saturday night pool party at Széchenyi, from €73"),
]

CSS = ('<style id="bpa-hubnav-css">.bpa-hubnav{margin:8px 0 28px;padding:18px 18px 14px;border:1px solid #e2e8f0;'
       'border-radius:16px;background:#fafbfc}.bpa-hubnav-title{font-size:12px;font-weight:800;letter-spacing:1px;'
       'text-transform:uppercase;color:#855a00;margin:0 0 12px}.bpa-hubnav-grid{display:grid;'
       'grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px}.bpa-hubnav a.bpa-hubnav-item{display:flex;'
       'gap:10px;align-items:flex-start;padding:12px 14px;border:1px solid #e2e8f0;border-radius:12px;background:#fff;'
       'text-decoration:none!important;color:#0f172a!important;min-width:0}.bpa-hubnav a.bpa-hubnav-item:hover{'
       'border-color:#dfa732}.bpa-hubnav-item.is-current{border-color:#0f172a;box-shadow:inset 0 0 0 1px #0f172a}'
       '.bpa-hubnav-ico{font-size:20px;line-height:1.2}.bpa-hubnav-name{display:block;font-size:14.5px;font-weight:700;'
       'line-height:1.3}.bpa-hubnav-sub{display:block;font-size:12.5px;color:#64748b;line-height:1.35;margin-top:2px}'
       '</style>')

START = '<nav aria-label="Budapest bath guides" class="bpa-hubnav" id="bpa-hubnav">'


def hubnav_block(current, title="Budapest Bath Guides"):
    items = []
    for key, href, ico, name, sub in GUIDES:
        if key != current and not live(href):
            continue
        cur = key == current
        items.append('<a class="bpa-hubnav-item%s" href="%s"%s><span class="bpa-hubnav-ico" aria-hidden="true">%s</span>'
                     '<span><span class="bpa-hubnav-name">%s</span><span class="bpa-hubnav-sub">%s</span></span></a>'
                     % (" is-current" if cur else "", href, ' aria-current="page"' if cur else "", ico, name, sub))
    return '%s<p class="bpa-hubnav-title">%s</p><div class="bpa-hubnav-grid">%s</div></nav>\n' % (START, title, "".join(items))


def hubnav_strip(page):
    return re.sub(re.escape(START) + r".*?</nav>\n?", "", page, flags=re.S)


def hubnav_css(page):
    page = re.sub(r'<style id="bpa-hubnav-css">.*?</style>', "", page, flags=re.S)
    return page.replace("</head>", CSS + "\n</head>", 1)

HOVER_CSS = ('<style id="bpa-rudas-hover-css">'
             '.ltt-lead-copy a:not([class]):hover,.bpa-wt-guide a:not([class]):hover,.ltt-editorial-wrapper a:not([class]):hover,'
             '.bpa-details-card .w-richtext a:not([class]):hover,.bpa-lang-pop a:not([class]):hover,.ltt-breadcrumbs a:hover,'
             '.bpa-hubnav a.bpa-hubnav-item:hover,.bpa-hubnav a.bpa-hubnav-item:hover *{color:#9f6e0d!important}'
             '.bpa-hubnav a.bpa-hubnav-item:hover .bpa-hubnav-sub{color:#64748b!important}'
             '</style>')


# ── helpers ──────────────────────────────────────────────────────────────────────────
def no_em_dash(html):
    html = re.sub(r"\s*—\s*", ": ", html)
    return html.replace("&mdash;", ":")


def must_sub(pat, repl, html, count=1, flags=0):
    new, n = re.subn(pat, repl, html, count=count, flags=flags)
    if not n:
        raise ValueError("pattern not found: %s" % pat[:80])
    return new


def swap_block(html, start_pat, new, tag="div"):
    m = re.search(start_pat, html)
    if not m:
        raise ValueError("block not found: %s" % start_pat)
    end = balanced(html, m.start(), tag)
    return html[:m.start()] + new + html[end:]


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s).replace("&amp;", "&").replace("&rsquo;", "’")


def jsonld():
    items = []
    for pos, c in enumerate(CARDS, 1):
        avg, tot = wavg(c["ratings"])
        offer = {"@type": "Offer", "availability": "https://schema.org/InStock",
                 "url": book_url(c, "schema").replace("&amp;", "&")}
        if c.get("price"):
            offer.update(price=c["price"], priceCurrency="EUR")
        else:
            offer.update(price=c["price_huf"], priceCurrency="HUF")
        prod = {"@type": "Product", "name": strip_tags(c["title"]),
                "description": strip_tags(c["pick"]).capitalize(),
                "brand": {"@type": "Organization", "name": "Rudas Thermal Bath"},
                "offers": offer}
        if c["book"] == "gyg":
            prod["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": "%.2f" % avg, "bestRating": "5",
                                       "worstRating": "1", "reviewCount": str(tot)}
        if c["tested"]:
            prod["review"] = {
                "@type": "Review", "author": {"@type": "Person", "name": "Adam Dimitrov", "url": SITE + "/about"},
                "datePublished": TODAY, "reviewBody": strip_tags(c["pick"]).capitalize(),
                "positiveNotes": {"@type": "ItemList", "itemListElement": [
                    {"@type": "ListItem", "position": k, "name": strip_tags("%s: %s" % p)} for k, p in enumerate(c["pros"], 1)]},
                "negativeNotes": {"@type": "ItemList", "itemListElement": [
                    {"@type": "ListItem", "position": k, "name": strip_tags("%s: %s" % p)} for k, p in enumerate(c["cons"], 1)]}}
        items.append({"@type": "ListItem", "position": pos, "url": "%s#%s" % (URL, c["anchor"]), "item": prod})
    data = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "@id": URL + "#article",
         "mainEntityOfPage": {"@type": "WebPage", "@id": URL},
         "headline": TITLE_TXT, "description": DESC, "url": URL, "inLanguage": "en",
         "datePublished": TODAY, "dateModified": TODAY,
         "author": {"@type": "Person", "name": "Adam Dimitrov", "jobTitle": "Founder & Local Budapest Tester",
                    "url": SITE + "/about",
                    "image": "/assets/cdn/652d0405192ba076b04f74a3/652d0405192ba076b04f792e_Adam-dimitrov-portrait-75x75.webp"},
         "publisher": {"@type": "Organization", "name": "BUDAPEST ADVENTURES", "url": SITE,
                       "logo": {"@type": "ImageObject", "url": "/assets/budapest-adventures-logo.png"}},
         "image": [SITE + P["roof_dusk"], SITE + P["roof_sunset"]],
         "about": {"@type": "TouristAttraction", "name": "Rudas Thermal Bath",
                   "address": {"@type": "PostalAddress", "streetAddress": "Döbrentei tér 9", "postalCode": "1013",
                               "addressLocality": "Budapest", "addressCountry": "HU"}},
         "mainEntity": {"@type": "ItemList", "name": TITLE_TXT, "itemListOrder": "https://schema.org/ItemListOrderAscending",
                        "numberOfItems": N, "itemListElement": items}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Thermal Baths in Budapest", "item": SITE + HUB},
            {"@type": "ListItem", "position": 3, "name": "Rudas Baths", "item": URL}]},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
    ]}
    return json.dumps(data, ensure_ascii=False, indent=1).replace("—", ":")


def main():
    page = SHELL
    # cards
    deck = "\n".join(deck_html(i, c) for i, c in enumerate(CARDS, 1))
    dets = "".join(details_html(c) for c in CARDS)
    cs = all_spans(page, "card")
    page = page[:cs[0][0]] + deck + page[cs[-1][1]:]
    ds = all_spans(page, "details")
    page = page[:ds[0][0]] + dets + page[ds[-1][1]:]

    # head
    page = must_sub(r"<title>.*?</title>", "<title>%s</title>" % TITLE, page, flags=re.S)
    for prop in ('property="og:title"', 'name="twitter:title"'):
        page = re.sub(r'<meta content="[^"]*" %s/>' % prop, '<meta content="%s" %s/>' % (TITLE, prop), page)
    for prop in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        page = re.sub(r'<meta content="[^"]*" %s/>' % prop, '<meta content="%s" %s/>' % (DESC, prop), page)
    page = re.sub(r'(<meta content=")[^"]*(" property="article:modified_time"/>)', r"\g<1>%sT00:00:00+00:00\2" % TODAY, page)
    page = re.sub(r'(<meta content=")[^"]*(" property="article:published_time"/>)', r"\g<1>%sT00:00:00+00:00\2" % TODAY, page)
    for prop in ('property="og:image"', 'name="twitter:image"'):
        page = re.sub(r'<meta content="[^"]*" %s/>' % prop, '<meta content="%s%s" %s/>' % (SITE, P["roof_dusk"], prop), page)
    page = page.replace(SITE + "/thermal-baths-budapest", URL)  # canonical, og:url, hreflang en/x-default
    # EN only: drop every other language alternate and the language-route tables
    page = re.sub(r'<link href="[^"]*" hreflang="(?!en"|x-default")[^"]*" rel="alternate"/>', "", page)
    page = re.sub(r"const alternativeLanguagePages = \{.*?\}</script>",
                  'const alternativeLanguagePages = {"default": "%s"}</script>' % URL, page, count=1, flags=re.S)
    page = re.sub(r"const LINGUANA_LANGUAGE_ROUTES = \[.*?\];</script>",
                  'const LINGUANA_LANGUAGE_ROUTES = [{"url": "%s", "hreflang": "default", "isDefault": true, "subfolder": "", "langCode": "en"}];</script>' % URL,
                  page, count=1, flags=re.S)
    # preload of the old hero image
    page = re.sub(r'<link as="image" fetchpriority="high" href="[^"]*"', '<link as="image" fetchpriority="high" href="%s"' % CARDS[0]["photos"][0], page, count=1)

    # hero
    page = must_sub(r'<nav aria-label="Breadcrumb" class="ltt-breadcrumbs">.*?</nav>',
                    '<nav aria-label="Breadcrumb" class="ltt-breadcrumbs">\n<a href="/">Home</a>\n<span class="ltt-bc-sep">›</span>\n'
                    '<a href="%s">Thermal Baths</a>\n<span class="ltt-bc-sep">›</span>\n<span class="ltt-bc-current">Rudas Baths</span>\n</nav>' % HUB,
                    page, flags=re.S)
    page = must_sub(r'<span class="ltt-hero-kicker-badge">[^<]*</span>', '<span class="ltt-hero-kicker-badge">2026 Rudas Ticket Comparison</span>', page)
    page = must_sub(r'(<h1 class="ltt-editorial-h1">).*?(</h1>)', r'\1\n      %s\n\2' % H1, page, flags=re.S)
    page = must_sub(r'<div class="ltt-author-role">[^<]*</div>',
                    '<div class="ltt-author-role">Bathed at Rudas in Person • %d Tickets Compared</div>' % N, page)
    page = must_sub(r"<strong>Last updated</strong>: [^<]*<", "<strong>Last updated</strong>: Nov 15, 2026<", page)
    page = swap_block(page, r'<div class="ltt-lead-copy">', LEAD)
    page = swap_block(page, r'<div class="ltt-integrated-pills">', PILLS)

    # between deck and breakdown: quick picks, timetable, prices, hub links
    a = page.find('<div class="container w-container"><div class="w-richtext"><p>Every bath below')
    b = page.find('<div class="bpa-breakdown-top-bar" id="breakdown-header">')
    assert 0 < a < b, (a, b)
    page = page[:a] + QUICK.replace("{HUBNAV}", hubnav_block("rudas")) + page[b:]
    page = must_sub(r'(<h2 class="bpa-breakdown-heading" id="desert-safaris-breakdown">)[^<]*(</h2>)',
                    r"\1Detailed Breakdown: %d Rudas Baths Tickets\2" % N, page)
    page = must_sub(r'<p class="bpa-breakdown-sub">[^<]*</p>',
                    '<p class="bpa-breakdown-sub">Rudas personally tested • All reviews open by default • Click to collapse/expand</p>', page)

    # editorial + FAQ
    a = page.find('<div class="ltt-editorial-wrapper" role="main">')
    b = page.find('<footer class="footer-dark ltt-footer"')
    seg = page[a:b]
    end = a + balanced(seg, 0, "div")
    page = page[:a] + editorial_html() + page[end:]

    # runtime config, sticky bars
    cfg = {"deckId": "budapest-rudas-baths-deck", "tocDeckLabel": "%d Rudas Tickets" % N,
           "tocBreakdownLabel": "Detailed Breakdown (%d Tickets)" % N,
           "shortTitles": [c["short"] for c in CARDS]}
    page = must_sub(r"window\.LTT_PAGE_CONFIG = \{.*?\};", "window.LTT_PAGE_CONFIG = %s;" % json.dumps(cfg, ensure_ascii=False), page, flags=re.S)
    page = page.replace('id="budapest-thermal-baths-deck"', 'id="budapest-rudas-baths-deck"')
    c1 = CARDS[0]
    for tid, pid, bid in (("sticky-name", "sticky-price", "sticky-cta-btn"), ("hybridActiveTitle", "hybridActivePrice", "hybridActiveCta")):
        page = re.sub(r'(<span class="hybrid-active-title" id="%s">)[^<]*(</span>)' % tid, r"\g<1>%s\2" % c1["short"], page, count=1)
        page = re.sub(r'(<span class="hybrid-active-price" id="%s">)[^<]*(</span>)' % pid, r"\g<1>From €%s\2" % c1["price"], page, count=1)
        page = re.sub(r'(<a class="hybrid-cta-btn" href=")[^"]*(" id="%s")' % bid, r"\g<1>%s\2" % gyg(c1, "sticky"), page, count=1)
    page = re.sub(r"<span>All \d+ Thermal Baths</span>", "<span>All %d Rudas Tickets</span>" % N, page)
    page = re.sub(r'<span class="hybrid-active-trust">[^<]*</span>', '', page)
    page = page.replace("Jump to Tested Thermal Bath", "Jump to a Rudas Ticket")
    page = page.replace('aria-label="Jump to Bath Review"', 'aria-label="Jump to Ticket Review"')
    page = page.replace("' cruises matching '", "' tickets matching '")
    page = page.replace("cmp=en-thermal-baths-", "cmp=en-rudas-baths-")

    # JSON-LD
    i = page.find('id="ltt-schema-jsonld"')
    a = page.find(">", i) + 1
    b = page.find("</script>", a)
    page = page[:a] + jsonld() + page[b:]

    page = hubnav_css(page).replace("</head>", HOVER_CSS + "\n</head>", 1)
    page = page.replace("SYSTEM — UNIFIED", "SYSTEM: UNIFIED")
    page = re.sub(r"<!-- #\d+: [^>]*-->\n?", "", page)
    if os.path.exists(OUT) and 'href="/css/listicle-cards.css' in open(OUT, encoding="utf-8").read():
        # The page is on the shared listicle design now: cards come from data/listicles/<slug>.json
        raise SystemExit(f"{os.path.basename(OUT)} is built from data/listicles/; edit the card data instead")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(page)
    print("wrote", OUT, len(page))


if __name__ == "__main__":
    main()
