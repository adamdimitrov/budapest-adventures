#!/usr/bin/env python3
"""Add the "questions travellers ask" box to the 4 market cards (mcard-1..4) on
budapest-christmas-markets.html. Those cards sit above the listicle card region (they describe the
markets, not bookable products), so the kit generator does not build them; the kit's house rule
still wants 5 questions on every bpa-card. Facts are the ones each market card already shows.
Idempotent: replaces an existing box.

    python3 scripts/christmas_market_card_faq.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "budapest-christmas-markets.html")

FAQ = {
    "mcard-1": [
        ("When is it open?", "13 Nov 2026 to 1 Jan 2027: 11:00–22:00 Mon to Thu and Sun, 11:00–23:00 Fri and Sat."),
        ("Is it open at Christmas and New Year's Eve?", "Yes: 24 Dec 11:00–15:00, 25–26 Dec 11:00–20:00, 31 Dec 11:00–03:00 and 1 Jan 11:00–18:00."),
        ("When is the light show?", "The 3D projection on the Basilica facade runs every afternoon from 17:30, repeated every half hour."),
        ("How much is mulled wine?", "1,500 Ft; a plain lángos is 2,400 Ft, and every main kitchen keeps one dish at 1,600 Ft."),
        ("When is it least crowded?", "On a weekday before 17:00. Friday and Saturday evenings are the busiest."),
    ],
    "mcard-2": [
        ("When is it open?", "13 Nov to 31 Dec 2026: 11:00–21:00 Mon to Thu and Sun, 11:00–22:00 Fri and Sat."),
        ("Is it open at Christmas?", "Short hours: 24 Dec 10:00–14:00, 25–26 Dec 12:00–18:00, and 31 Dec 11:00–03:00 with the New Year's Eve party on the square."),
        ("Is the mini train free?", "Yes: Mon to Fri 14:00–20:00, Sat and Sun 11:00–20:00. It does not run on 25 Dec."),
        ("How much is the food?", "Cheese and sour cream lángos 3,200 Ft, goulash in a bread bowl 5,700 Ft, roasted chestnuts 3,000 Ft; several stalls also sell 1,600 Ft dishes."),
        ("When do the craft stalls leave?", "After 28 Dec, together with the mini train."),
    ],
    "mcard-3": [
        ("When is it open?", "27 Nov 2026 to 3 Jan 2027, every day 09:00–20:00."),
        ("Is it open at Christmas?", "24 Dec 09:00–12:00 and 1 Jan 12:00–20:00. Hours for 25, 26 and 31 Dec are not listed."),
        ("When are the Advent candles lit?", "At 16:00 on 29 Nov, 6, 13 and 20 Dec, followed by concerts at the Budavári Városháza."),
        ("How do I get up the hill?", "Bus 16 from Deák Ferenc tér to Szentháromság tér, or the Budavári Sikló funicular from Clark Ádám tér. Walking up from the Chain Bridge is steep and cobbled."),
        ("Can I go in the evening?", "Only until 20:00, earlier than the Pest markets."),
    ],
    "mcard-4": [
        ("When is it open?", "27 Nov to 23 Dec 2026: Mon to Thu 14:00–21:00, Fri 14:00–22:00, Sat 10:00–22:00, Sun 10:00–21:00."),
        ("Is it open at Christmas?", "No. It closes on 23 Dec and is not open on 24, 25, 26 or 31 Dec."),
        ("Is the ice rink free?", "Yes: free skating on Fő tér from 27 Nov to 31 Jan, Sun to Thu 08:00–21:00, Fri and Sat 08:00–22:00. Skates can be rented."),
        ("How do I get there?", "HÉV H5 from Batthyány tér (M2) to Szentlélek tér, about 25 minutes from the Basilica."),
        ("Is it good for kids?", "Yes: free skating, a gingerbread house with St Nicholas and fewer tourists than in the centre."),
    ],
}


def box(items):
    return ('<details class="fbm-faq"><summary>❓ 5 questions travellers ask <span class="fbm-faq-chev" aria-hidden="true">▾</span>'
            '</summary><div class="fbm-faq-body">'
            + "".join(f'<div class="fbm-qa"><div class="fbm-q">{q}</div><div class="fbm-a">{a}</div></div>' for q, a in items)
            + "</div></details>")


def main():
    s = open(PAGE, encoding="utf-8").read()
    for cid, items in FAQ.items():
        i = s.find(f'id="{cid}"')
        m = re.compile(r'<div class="bpa-best-for bpa-pickskip">.*?</div>(\n?<details class="fbm-faq">.*?</details>)?', re.S).search(s, i)
        ps = re.match(r'<div class="bpa-best-for bpa-pickskip">.*?</div>', m.group(0), re.S).group(0)
        s = s[:m.start()] + ps + "\n" + box(items) + s[m.end():]
    open(PAGE, "w", encoding="utf-8").write(s)
    print("market cards: questions box on", len(FAQ), "cards")


if __name__ == "__main__":
    main()
