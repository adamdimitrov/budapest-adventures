# -*- coding: utf-8 -*-
"""Upgrade spec for thermal-baths-budapest.html (scripts/listicle_upgrade.py).

Facts from the page's own breakdowns (official 2026 price lists, online prices for Thu 19 Nov 2026).
Personally tested (title: 4 of 6): Széchenyi, Rudas, Palatinus, Dandár.
"""

PAGE = {
    "noun": "baths",
    "filter_aria": "Filter thermal baths",
    "filters": [
        {"label": "Bath style", "chips": [("palace", "🏛️ Palace bath"), ("turkish", "🕌 Ottoman Turkish bath"),
                                           ("outdoor", "♨️ Outdoor hot pools")]},
        {"label": "Practical", "chips": [("late", "🌙 Open after 21:00"), ("quiet", "🤫 Fewer crowds"),
                                          ("kids", "👨‍👩‍👧 Kids allowed"), ("online", "🎟️ Book online")]},
        {"label": "Budget &amp; proof", "chips": [("under30", "💶 Under €30"), ("tested", "✓ Personally tested")]},
    ],
}

ONLINE = "Online price for Thu 19 Nov 2026; desk prices from the bath's 2026 price list."

CARDS = {
    "card-1": {
        "cats": ["palace", "outdoor", "late", "online", "tested"],
        "tested": True,
        "faq": [
            ("Is Széchenyi worth it?",
             "Yes, for a first visit. It is the biggest and most photogenic bath in Budapest. Go early on a weekday to avoid the crowds."),
            ("When is it least crowded?",
             "Between 7:00 and 10:00 on a weekday. By late morning the outdoor pools are packed."),
            ("Locker or cabin?",
             "A standard ticket includes a locker in the gender-separated changing area, opened with a plastic wristwatch (3,000 HUF if lost). A private cabin costs 1,000 HUF extra."),
            ("Are towels included?",
             "No. Bring a swimsuit, towel and flip-flops; the desk sells a towel for 6,900 HUF, slippers for 4,200 HUF and a swim cap for 2,100 HUF."),
            ("Can I bathe at night?",
             "It is open until 22:00 on Fridays. Sparty, the Saturday night pool party, is sold separately: 18+, from €73, non-refundable."),
        ],
        "price": {
            "rows": [
                {"label": "Morning Pass", "small": "locker, Mon–Thu entry 7:00–9:00", "price": "€39"},
                {"label": "Weekday Pass", "small": "locker", "price": "€46"},
                {"label": "Weekday Pass", "small": "private cabin", "price": "€50"},
                {"label": "At the desk", "small": "locker, Mon–Thu", "price": "13,200 HUF"},
                {"label": "At the desk", "small": "locker, Fri–Sun", "price": "14,800 HUF"},
            ],
            "note": ONLINE,
        },
    },
    "card-2": {
        "cats": ["turkish", "outdoor", "late", "online", "tested"],
        "tested": True,
        "faq": [
            ("Is Rudas better than Széchenyi?",
             "For atmosphere, often yes: the Ottoman Turkish bath and the rooftop pool are unique. For a family day out, no: Rudas admits no under-14s."),
            ("When are the men-only and women-only days?",
             "Men: Mon, Thu and Fri 6:00–10:45 and all day Wednesday. Women: all day Tuesday. Weekends are mixed."),
            ("Can I go at night?",
             "Yes, Friday and Saturday 22:00–3:00. Night tickets are sold online only: 15,000 HUF (18,000 HUF on 1 and 2 January 2027). Night buses 907 and 973 run afterwards."),
            ("What does this ticket include?",
             "A day pass plus a 3-course meal at Rudas Bistro, from €74.99. A plain entry ticket is only sold at the desk."),
            ("Can I bring children?",
             "No. There are no children under 14, and currently no access for guests with reduced mobility."),
        ],
        "price": {
            "rows": [
                {"label": "Day pass + 3-course meal", "price": "€74.99"},
                {"label": "At the desk", "small": "all zones, Mon–Thu", "price": "12,000 HUF"},
                {"label": "At the desk", "small": "all zones, Fri–Sun", "price": "15,000 HUF"},
                {"label": "Turkish bath only", "small": "Mon, Thu, Fri until 10:45", "price": "8,000 HUF"},
                {"label": "Night bathing", "small": "Fri–Sat 22:00–3:00, online only", "price": "15,000 HUF"},
            ],
            "note": ONLINE,
        },
    },
    "card-3": {
        "cats": ["late", "quiet", "online"],
        "ratings_patch": {"stars": "3.98", "score": "4.0", "meta": "430+ reviews · 3 sites",
                          "heading": "Average of 3 booking sites, weighted by number of reviews"},
        "add_sites": [{"kind": "static", "site": "Viator", "score": "3.7", "count": "(40+)"}],
        "faq": [
            ("Is Lukács a good alternative to Széchenyi?",
             "Yes, if you want thermal water without the crowds. It is smaller and plainer, closer to a local bath than a tourist sight."),
            ("How hot are the pools?",
             "Indoor medicinal pools at 32, 36 and 40 °C, a 20 °C cold pool, an outdoor adventure pool at 33–35 °C and swimming pools at 22 and 26 °C."),
            ("Is it open late?",
             "Until 22:00 every Tuesday. The other days it is open 7:00–19:00."),
            ("Is it step-free?",
             "Not right now: the wheelchair lifts are out of order and the private tubs are closed for renovation."),
            ("How do I find it?",
             "Frankel Leó út 25-29: tram 4, 6, 17 or 19, bus 9 or 109, or the HÉV to Margit híd, budai hídfő. Veli Bej is on the same street, so do not mix them up."),
        ],
        "price": {
            "rows": [
                {"label": "Full day", "small": "cabin or locker", "price": "€33"},
                {"label": "At the desk", "small": "Mon–Thu", "price": "7,000 HUF"},
                {"label": "At the desk", "small": "Fri–Sun", "price": "8,000 HUF"},
                {"label": "Last 2 hours", "small": "weekdays, desk", "price": "3,800 HUF"},
                {"label": "Sauna world", "small": "desk", "price": "+1,300 HUF"},
            ],
            "note": ONLINE,
        },
    },
    "card-4": {
        "cats": ["outdoor", "kids", "online", "under30", "tested"],
        "tested": True,
        "faq": [
            ("Is Palatinus worth it in winter?",
             "Only for a short visit. In winter it closes at 16:00, and the Finnish sauna is out of service from 14 Nov 2026."),
            ("What is there for kids?",
             "A shallow outdoor kids' pool (30–32 °C), an indoor one (32–34 °C) and a 28 °C wave pool; the slides open in summer. Child tickets are for ages 3–14."),
            ("Is it real thermal water?",
             "Yes: two thermal pools at 30–32 °C and 33–36 °C plus a 36 °C indoor medicinal pool."),
            ("How do I get there?",
             "Bus 26 from Nyugati pályaudvar or Árpád híd stops right outside. In summer the bath also runs its own minibus."),
            ("Are the lockers big?",
             "Adult tickets include a locker, but I found them small, so pack light. A cabin ticket costs 1,000 HUF."),
        ],
        "price": {
            "rows": [
                {"label": "Full day", "small": "cabin or locker", "price": "€27"},
                {"label": "At the desk", "small": "adult, weekdays / weekends", "price": "3,800 / 4,200 HUF"},
                {"label": "Child 3–14", "small": "desk, weekdays / weekends", "price": "2,500 / 2,800 HUF"},
                {"label": "Family of 3", "small": "desk, weekdays / weekends", "price": "7,600 / 8,400 HUF"},
            ],
            "note": ONLINE,
        },
    },
    "card-5": {
        "cats": ["outdoor", "late", "quiet", "online", "under30", "tested"],
        "tested": True,
        "faq": [
            ("Is Dandár worth visiting as a tourist?",
             "Yes, if you want a cheap, local bath and do not care about architecture. It is the opposite of Széchenyi."),
            ("How cheap is it at the desk?",
             "3,500 HUF on weekdays and 4,000 HUF at weekends; with the sauna and outdoor pools it is 4,500 / 5,000 HUF."),
            ("Does it have outdoor pools?",
             "Two outdoor pools at 36 and 38 °C, with a lawn and sun loungers."),
            ("When is it open late?",
             "Thursdays until 22:00. The other days it is open 9:00–19:00."),
            ("What can I pair it with?",
             "It is a stone's throw from the Zwack Unicum factory. Tram 2 or 24, or bus 23 or 54, take you there."),
        ],
        "price": {
            "rows": [
                {"label": "Full day", "small": "cabin or locker", "price": "€22"},
                {"label": "At the desk", "small": "thermal, weekdays / weekends", "price": "3,500 / 4,000 HUF"},
                {"label": "With sauna + outdoor", "small": "desk", "price": "4,500 / 5,000 HUF"},
                {"label": "Cabin", "small": "desk", "price": "+800 HUF"},
            ],
            "note": ONLINE,
        },
    },
    "card-6": {
        "cats": ["turkish", "quiet", "under30"],
        "faq": [
            ("How is Veli Bej different from Rudas?",
             "Both are Ottoman baths, but Veli Bej is smaller, quieter and cheaper, and you cannot book it online."),
            ("Can I book online?",
             "No. Tickets are sold only at the cashier, so just turn up."),
            ("When is it open?",
             "Mon–Tue 15:00–21:00; Wed–Sun 6:00–12:00 and 15:00–21:00. It closes every day from 12:00 to 15:00."),
            ("Is it crowded?",
             "Visitors consistently describe it as calm, with empty pools early in the morning."),
            ("Can children come?",
             "No under-14s, even with a parent."),
        ],
        "price": {
            "rows": [
                {"label": "Morning", "small": "Wed–Fri", "price": "5,700 HUF"},
                {"label": "Afternoon", "small": "Mon–Thu", "price": "6,700 HUF"},
                {"label": "Fri afternoon, Sat, Sun", "price": "7,200 HUF"},
                {"label": "Towel / slippers", "small": "desk", "price": "1,100 / 1,900 HUF"},
            ],
            "note": "Official desk prices; there is no online ticket.",
        },
    },
}
