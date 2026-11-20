#!/usr/bin/env python3
"""Expand /best-walking-tours-budapest (EN) from 6 to 10 tours, 2026-11-14.

New cards #7-#10 come from live GetYourGuide product pages read on 2026-11-14
(rating, review count and lowest price from each page's structured data;
itinerary, inclusions and meeting points from the product description).
They are NOT personally tested: no "Personally Tested" chip, no author review
in JSON-LD. Photos are the operators' listing photos, stored under
/assets/walking-tours-2026/.

Also moves the FAQ out of card #6's body to after the last card.
Run once on the 6-card page.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "best-walking-tours-budapest.html"
URL = "https://www.budapestadventures.com/best-walking-tours-budapest"
GYG = "https://www.getyourguide.com/budapest-l29/{slug}/?partner_id=YS414AJ&amp;utm_medium=online_publisher&amp;cmp={cmp}&amp;mkt_cmp=true"

TOURS = [
    dict(
        n=7, anchor="item-7-budapest-food-tour", rank="#7 Carpe Diem Tours", operator="Carpe Diem Tours",
        short_op="Carpe Diem", title="Budapest Food Walking Tour: Eat, Sip and Explore",
        slug="budapest-food-walking-tour-eat-sip-explore-like-a-local-t519670", cmp="walking-tours-food",
        score="4.8", count="1690", count_exact=1690, rating=4.799, price=62, price_txt="From €62",
        dur="2.5 Hours", dur_short="2.5 hours", place="Kazinczy utca", map="Kazinczy+utca+29+Budapest",
        cats="c20 long pest", photos="food-tour", photo_order=[1, 2, 5, 4, 3],
        alts=["Lángos and a Dreher beer on the Budapest food walking tour",
              "Food tour group outside a District VII street food bar",
              "Food tour group in a Jewish Quarter ruin bar courtyard",
              "Two guests toasting with Hungarian beer on the food tour",
              "Local foodie guide explaining Hungarian dishes in District VII"],
        specs=["Food Tour", "⏱ 2.5 Hours Walk", "4 Eateries", "3 Drinks"],
        best_for="Food lovers and first-timers: lángos, chicken paprikash and somlói cake with pálinka and Tokaji, in 2.5 hours.",
        pros=["4 food stops with a set menu: lángos, chicken paprikash, somlói trifle and more",
              "3 drinks included (pálinka, Dreher beer, sweet Tokaji wine), alcohol-free on request",
              "Covers the Jewish Quarter and Andrássy Avenue, so it doubles as a sightseeing walk"],
        cons=["No gluten-free or vegan menu yet (vegetarian is possible)",
              "Not suitable for wheelchair users"],
        body="""<p>This is the walking tour that replaces dinner. Over <strong>2.5 hours</strong> a local foodie guide takes you through <strong>District VII</strong>, Budapest's old Jewish Quarter and today its busiest nightlife street, and feeds you at <strong>four local eateries</strong> along the way.</p>
<p>It starts casual, with a traditional soup and <strong>lángos</strong> (deep-fried flatbread), then moves to a sit-down plate of <strong>chicken paprikash</strong> and ends with <strong>somlói</strong>, a custard trifle cake, paired with sweet Tokaji wine. A shot of pálinka and a local Dreher beer come with it, so <strong>3 drinks are included</strong>.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> if you want Hungarian food explained by someone local, or you'd rather eat your way through the Jewish Quarter than read plaques. Guests keep saying the same thing: come hungry, the portions are big.</p>
<p><strong>Skip it</strong> if you eat gluten-free or vegan: the operator can't cater for that yet. Vegetarians are fine, with a smaller menu.</p>
<h3>Meeting Point</h3>
<p>🗺️ <strong>Meeting Point: </strong>Kazinczy utca 29-31, 1075 Budapest (District VII), by the Kazinczy Street Synagogue, where the tour also ends.<br/>🚇 <strong>Public Transport:</strong> Astoria (M2) or Deák Ferenc tér (M1, M2, M3), then a 5-minute walk.</p>""",
        qf_badge="Jewish Quarter (District VII)",
        qf=[("Duration", "2.5 Hours"), ("Price", "From €62 / person"),
            ("Language", "English (private group option available)"),
            ("Meeting Point", "Kazinczy utca 29-31, 1075 Budapest"),
            ("Tour Conclusion", "Kazinczy Street Synagogue"),
            ("What You Eat", "Traditional soup, lángos, chicken paprikash, somlói trifle cake"),
            ("Drinks Included", "3: pálinka, Dreher beer, sweet Tokaji wine (alcohol-free options)"),
            ("Accessibility", "Not suitable for wheelchair users")],
        chips=[("yes", "✓ 4 Eateries Included"), ("yes", "✓ 3 Drinks Included"), ("yes", "✓ Vegetarian Option"),
               ("no", "✕ No Gluten-Free or Vegan Menu"), ("no", "✕ Not Wheelchair Accessible")],
        perks=["Departure: <strong>Kazinczy utca</strong>", "Duration: <strong>2.5 Hours</strong>"],
        desc="Food walking tour of the Jewish Quarter with 4 eateries and 3 drinks included.",
    ),
    dict(
        n=8, anchor="item-8-communist-history-tour", rank="#8 Tourist Angel", operator="Tourist Angel",
        short_op="Tourist Angel", title="Communist History Tour with House of Terror Option",
        slug="budapest-house-of-terror-guided-tour-t389878", cmp="walking-tours-communism",
        score="4.8", count="220", count_exact=225, rating=4.76, price=50, price_txt="From €50",
        dur="2 Hours", dur_short="2 hours", place="Kossuth Lajos tér", map="Kossuth+Lajos+tér+Budapest",
        cats="c20 short pest", photos="communist-tour", photo_order=[1, 5, 2, 3, 4],
        alts=["House of Terror Museum on Andrássy Avenue, Budapest",
              "Guide with a small group outside the Hungarian Parliament",
              "Wall of victims' portraits at the House of Terror",
              "Tank in the atrium of the House of Terror Museum",
              "Hungarian Parliament, where the communist history walk begins"],
        specs=["Communism & 1956", "⏱ 2 Hours Tour", "Max 10 People", "Museum Ticket"],
        best_for="History lovers who want the Soviet era explained by a local, with a House of Terror or Retro Center ticket included.",
        pros=["Small group, limited to 10 people",
              "Museum ticket included: House of Terror or the Budapest Retro Center, depending on the option",
              "Guides share their own family's stories of life under communism"],
        cons=["The House of Terror option is a self-guided visit after the walk, and some rooms lack English text",
              "Meeting point depends on the option you pick"],
        body="""<p>Hungary spent <strong>45 years under Soviet occupation</strong>, and this tour shows you where that history still stands in central Budapest. Groups are <strong>limited to 10 people</strong>, led by a local guide trained in history.</p>
<p>The walk starts at the <strong>Parliament</strong> with the memorial to the victims of the dictatorship, then goes to <strong>Liberty Square</strong> and the Soviet memorial still in its original place, the windows where Cardinal Mindszenty lived in exile, the ventilation shafts of a <strong>Cold War nuclear bunker</strong>, and sites of the <strong>1956 revolution</strong>.</p>
<h3>Pick Your Option</h3>
<p><strong>Morning walk + Budapest Retro Center:</strong> after the walk, a 1-hour guided visit to a lighter, interactive museum of 1960s to 1980s daily life.<br/><strong>Afternoon walk + House of Terror:</strong> after the walk you visit the former secret police headquarters on your own, ticket included.<br/><strong>Guided House of Terror tour:</strong> the museum only, with the guide taking you from WWII to 1989.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> if the 20th century is why you came to Budapest, or you want the House of Terror with context instead of reading wall sheets. Pairs well with the free <a href="#item-3-ww2-jewish-quarter-tour">Jewish Quarter walk</a>.</p>
<p><strong>Skip it</strong> with young children: the House of Terror covers interrogation cells and deportations. On the self-guided option, consider the museum's audio guide.</p>""",
        qf_badge="Inner City & Andrássy út",
        qf=[("Duration", "2 Hours (Retro Center option adds a 1-hour visit)"), ("Price", "From €50 / person"),
            ("Group Size", "Small group, max 10 people"), ("Language", "English"),
            ("Meeting Point", "Depends on the option (walking options start at the Parliament)"),
            ("Museum Entry", "House of Terror or Budapest Retro Center ticket included"),
            ("Landmarks Visited", "Parliament, Liberty Square Soviet memorial, Cold War bunker shafts, 1956 sites")],
        chips=[("yes", "✓ Museum Ticket Included"), ("yes", "✓ Max 10 Guests"), ("yes", "✓ Skip the Ticket Queue"),
               ("no", "✕ Heavy Themes for Young Kids")],
        perks=["Group: <strong>Max 10 People</strong>", "Duration: <strong>2 Hours</strong>"],
        desc="Small-group communist history walk with House of Terror or Retro Center entry.",
    ),
    dict(
        n=9, anchor="item-9-private-walking-tour", rank="#9 Guydeez", operator="Guydeez",
        short_op="Guydeez", title="Private Custom Walking Tour with a Local Guide",
        slug="private-custom-tour-with-local-guide-budapest-t467353", cmp="walking-tours-private",
        score="4.7", count="110", count_exact=117, rating=4.69, price=40, price_txt="From €40",
        dur="2 to 8 Hours", dur_short="2 to 8 hours", place="Your hotel", map="Budapest",
        cats="c20 short long both", photos="private-tour", photo_order=[2, 1, 5, 4, 3],
        alts=["Private walking tour guests at Heroes' Square, Budapest",
              "Private tour group by the Chain Bridge and the Danube",
              "Private tour group inside a Budapest church",
              "Private tour guests stopping at a Budapest café",
              "Guide and guest resting on a private Budapest walking tour"],
        specs=["Private Guide", "⏱ 2 to 8 Hours", "Hotel Pickup", "Your Route"],
        best_for="Families, couples and slow walkers who want their own guide, their own pace and a route built around them.",
        pros=["Only your group: route, pace and length (2 to 8 hours) are up to you",
              "The guide meets you at your accommodation in the city",
              "Wheelchair-accessible; English, Spanish, French or Italian"],
        cons=["Price is per person, so it adds up for bigger groups",
              "Museum tickets, food and transport are extra"],
        body="""<p>Group walks follow a script. This one doesn't: you get a <strong>private local guide</strong>, pick the length (<strong>2 to 8 hours</strong>) and decide what you want to see, from the big sights to cafés and neighbourhoods tourists miss.</p>
<p>The guide <strong>meets you at your accommodation</strong> if it's in the city, the tour is <strong>wheelchair-accessible</strong>, and it runs in English, Spanish, French or Italian. The team can also help you book museum tickets if you want to go inside.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> for families with kids, older travellers who need breaks, or anyone who hates following a yellow umbrella with 30 strangers. Guests mention guides adapting the route to what they asked for.</p>
<p><strong>Skip it</strong> if you're on a budget: the free <a href="#item-4-pest-walking-tour">Inner City walk</a> covers the Pest highlights for a tip. And don't book 8 hours in one go: one guest clocked about 12 km on a full-day version.</p>""",
        qf_badge="Anywhere in Budapest",
        qf=[("Duration", "2 to 8 Hours (your choice)"), ("Price", "From €40 / person"),
            ("Group", "Private, your group only"), ("Languages", "English, Spanish, French, Italian"),
            ("Meeting Point", "Your accommodation (if in the city)"),
            ("Not Included", "Museum tickets, food and drinks, transport"),
            ("Accessibility", "Wheelchair-accessible")],
        chips=[("yes", "✓ Private Guide"), ("yes", "✓ Hotel Pickup"), ("yes", "✓ Wheelchair Accessible"),
               ("no", "✕ Tickets Not Included")],
        perks=["Pickup: <strong>Your Hotel</strong>", "Duration: <strong>2 to 8 Hours</strong>"],
        desc="Private, customisable walking tour with hotel pickup and a local guide.",
    ),
    dict(
        n=10, anchor="item-10-orientation-walking-tour", rank="#10 Tourist Angel", operator="Tourist Angel",
        short_op="Tourist Angel", title="3-Hour Orientation Walking Tour of Buda and Pest",
        slug="free-walking-tour-of-budapest-t13960", cmp="walking-tours-orientation",
        score="4.8", count="2360", count_exact=2367, rating=4.82, price=35, price_txt="From €35",
        dur="3 Hours", dur_short="3 hours", place="Szent István tér", map="Szent+István+tér+4+Budapest",
        cats="c20 long both", photos="orientation-tour", photo_order=[2, 1, 3],
        alts=["Orientation walking tour group at St. Stephen's Basilica",
              "Guests at a Buda viewpoint over the Danube and Parliament",
              "St. Stephen's Basilica, the meeting point of the orientation tour"],
        specs=["Buda + Pest", "⏱ 3 Hours Walk", "6 Languages", "Small Groups"],
        best_for="Your first day if you want Buda and Pest in one walk with a paid, smaller group: Basilica to Buda Castle in 3 hours.",
        pros=["Both sides of the river in one walk: Basilica, Parliament, Matthias Church, Buda Castle",
              "Runs in English, French, German, Italian, Russian and Spanish",
              "Private or small-group options"],
        cons=["Public transport across the Danube is optional and paid separately (about 2,000 HUF)",
              "3 hours on foot, with a climb on the Buda side"],
        body="""<p>The free walks on this list split the city in two: Pest one day, the Castle another. This tour does <strong>both sides of the Danube in 3 hours</strong>, which is why it's the most-reviewed tour in this comparison.</p>
<p>You meet at <strong>St. Stephen's Basilica</strong>, walk past the <strong>Parliament</strong>, cross to Buda and finish the loop at <strong>Matthias Church, Buda Castle and the Royal Palace</strong>. The guide covers history and how locals live now, and can tip you off on where to eat.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> if you have one or two days, want a smaller paid group instead of a free-tour crowd, or need a guide in French, German, Italian, Russian or Spanish.</p>
<p><strong>Skip it</strong> if you already plan the free <a href="#item-4-pest-walking-tour">Inner City walk</a> and the <a href="#item-5-buda-castle-walking-tour">Buda Castle tour</a>: together they cover the same ground in more depth.</p>
<h3>Meeting Point</h3>
<p>🗺️ <strong>Meeting Point: </strong>Szent István tér 4, 1051 Budapest, in front of St. Stephen's Basilica.<br/>🚇 <strong>Public Transport:</strong> Bajcsy-Zsilinszky út (M1) or Deák Ferenc tér (M1, M2, M3), a 3-minute walk.</p>""",
        qf_badge="St. Stephen's Basilica (District V)",
        qf=[("Duration", "3 Hours"), ("Price", "From €35 / person"),
            ("Languages", "English, French, German, Italian, Russian, Spanish"),
            ("Meeting Point", "Szent István tér 4, 1051 Budapest"),
            ("Extra Cost", "Optional public transport, 4 tickets about 2,000 HUF"),
            ("Landmarks Visited", "St. Stephen's Basilica, Parliament, Matthias Church, Buda Castle, Royal Palace")],
        chips=[("yes", "✓ Buda and Pest in One Walk"), ("yes", "✓ 6 Languages"), ("yes", "✓ Private Option"),
               ("no", "✕ Transport Tickets Extra")],
        perks=["Departure: <strong>Szent István tér</strong>", "Duration: <strong>3 Hours</strong>"],
        desc="3-hour walking tour of Buda and Pest from St. Stephen's Basilica to Buda Castle.",
    ),
]

STAR_FULL = '<svg aria-hidden="true" viewbox="0 0 24 24"><path d="M11.9999 18.26L4.94691 22.208L6.52191 14.28L0.586914 8.792L8.61391 7.84L11.9999 0.5L15.3859 7.84L23.4129 8.792L17.4779 14.28L19.0529 22.208L11.9999 18.26Z"></path></svg>'


def stars_html(s, score):
    """Reuse the exact star markup of an existing card with the same rounding (4.9 -> 5 full, 4.6 -> 4.5)."""
    ref = "4.9" if float(score) >= 4.75 else "4.6"
    m = re.search(r'<span class="bpa-rev-score">' + re.escape(ref) + r'</span>(<span class="bpa-rev-stars">.*?</span>)', s, re.S)
    return m.group(1)


def gyg_icon(s):
    return re.search(r'<img alt="" class="bpa-rev-icon" loading="lazy" src="(data:image/png;base64,[^"]+)"/><span class="bpa-rev-score">4.4', s).group(1)


def deck_card(t, s):
    href = GYG.format(slug=t["slug"], cmp=t["cmp"])
    photos = [f'/assets/walking-tours-2026/{t["photos"]}-{k:02d}.webp' for k in t["photo_order"]]
    sizes = 'sizes="(max-width: 767px) 420px, (max-width: 991px) 55vw, (max-width: 1439px) 49vw, 50vw"'
    imgs = [f'<img alt="{t["alts"][0]}" height="534" loading="lazy" {sizes} src="{photos[0]}" width="800"/>']
    blank = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 500'%3E%3C/svg%3E"
    for p, a in zip(photos[1:], t["alts"][1:]):
        imgs.append(f'<img alt="{a}" data-src="{p}" decoding="async" loading="lazy" {sizes} src="{blank}"/>')
    specs = "\n".join(f'<span class="bpa-sp">{x}</span>' for x in t["specs"])
    badge = (f'<a class="bpa-rev-badge" href="{href}" onclick="event.stopPropagation()" rel="noopener nofollow sponsored" target="_blank">'
             f'<img alt="" class="bpa-rev-icon" loading="lazy" src="{gyg_icon(s)}"/><span class="bpa-rev-score">{t["score"]}</span>'
             f'{stars_html(s, t["score"])}<span class="bpa-rev-count">(+{t["count"]} reviews)</span></a>')
    kicker_place = (t["place"] if t["place"] == "Your hotel" else
                    f'<a class="bpa-kicker-map-link" href="https://www.google.com/maps/search/?api=1&amp;query={t["map"]}" onclick="event.stopPropagation()" rel="noopener noreferrer" target="_blank">{t["place"]}</a>')
    return f"""<div class="bpa-card" data-cat="{t['cats']}" id="card-{t['n']}">
<div class="bpa-main">
<div class="bpa-media">
<span class="bpa-rank-tag bpa-slate">{t['rank']}</span>
<button aria-label="Previous photo" class="bpa-arrow prev" onclick="bpaSlide(this,-1)" type="button">‹</button>
<button aria-label="Next photo" class="bpa-arrow next" onclick="bpaSlide(this,1)" type="button">›</button>
<span class="bpa-pill">1 / {len(photos)}</span>
<div aria-label="Photo gallery {t['n']}" class="bpa-slider" onscroll="bpaCount(this)" tabindex="0">
{chr(10).join(imgs)}
</div>
</div>
<div class="bpa-info">
<div class="bpa-kicker">{t['short_op']} • ⏱️ {t['dur']} • {kicker_place}</div>
<a class="bpa-title" href="{href}" rel="nofollow sponsored noopener" target="_blank">{t['title']}</a>
<div class="bpa-reviews-line">
<div class="bpa-summary-reviews"><div class="div-block-53">{badge}</div></div>
</div>
<div class="bpa-specs-row">
{specs}
</div>
<div class="bpa-best-for">
<strong>Best For:</strong> {t['best_for']}
              </div>
</div>
<div class="bpa-cta-cell">
<div>
<div class="bpa-price">{t['price_txt']}</div>
<div class="bpa-psub">{t['dur_short']} • Free cancellation</div>
</div>
<a class="bpa-btn" href="{href}" rel="nofollow sponsored noopener" target="_blank">Check Availability →</a>
<div class="bpa-trust-micro">
<span>Instant QR</span>
<span>•</span>
<span>Free 24h Cancellation</span>
</div>
<a class="bpa-sublink" href="#{t['anchor']}">Read Review ↓</a>
</div>
</div>
</div>
"""


def details(t, s, lock_svg):
    href = GYG.format(slug=t["slug"], cmp=t["cmp"])
    photos = [f'/assets/walking-tours-2026/{t["photos"]}-{k:02d}.webp' for k in t["photo_order"]]
    badge = (f'<span class="bpa-rev-badge"><img alt="" class="bpa-rev-icon" loading="lazy" src="{gyg_icon(s)}"/>'
             f'<span class="bpa-rev-score">{t["score"]}</span>{stars_html(s, t["score"])}'
             f'<span class="bpa-rev-count">(+{t["count"]} reviews)</span></span>')
    pros = "".join(f"<li><strong>{x}</strong></li>" for x in t["pros"])
    cons = "".join(f"<li><strong>{x}</strong></li>" for x in t["cons"])
    slides = "".join(
        f'<div class="ltt-strip-slide"><img alt="{a}" loading="lazy" src="{p}"/><div class="ltt-strip-cap">'
        f'<span class="ltt-strip-num">{i} / {len(photos)}</span> <span>{a}</span></div></div>'
        for i, (p, a) in enumerate(zip(photos, t["alts"]), 1))
    perks = "\n".join(f'<span class="ltt-buy-perk">{x}</span>' for x in
                      ["Instant Smartphone QR Voucher", "Full Refund up to 24h Before"] + t["perks"])
    qf = "\n".join(f'<div class="qf1-row"><div class="qf1-label">{a}</div><div class="qf1-val">{b}</div></div>' for a, b in t["qf"])
    chips = "\n".join(f'<span class="qf1-chip {c}">{x}</span>' for c, x in t["chips"])
    return f"""<details class="bpa-details-card" data-cat="{t['cats']}" id="{t['anchor']}" open="">
<summary class="bpa-details-summary">
<div class="bpa-details-summary-content">
<div class="bpa-details-top-row">
<span class="bpa-rank-tag bpa-slate">{t['rank']}</span>
<div class="bpa-kicker">{t['short_op']} • ⏱️ {t['dur']} • <span class="bpa-kicker-map-link">{t['place']}</span></div>
</div>
<h3 class="bpa-details-title">{t['title']}</h3>
<div class="bpa-reviews-line">
<div class="bpa-summary-reviews"><div class="div-block-53">{badge}</div></div>
</div>
</div>
<div class="bpa-details-right">
<span class="bpa-details-price">{t['price_txt']}</span>
<div class="bpa-details-toggle">
<span class="bpa-details-state-text"></span>
<span class="bpa-details-chevron">▾</span>
</div>
</div>
</summary>
<div class="bpa-details-body">
<div class="pro-con-box-wrapper"><div class="w-layout-grid grid-15"><div class="pro-con-box-pro-cell" data-wf-pbl="layout-grid-1x2-vertical"><div class="pro-con-box-pro-cell-rich-text-block w-richtext"><h3><strong>Pros:</strong></h3><ul role="list">{pros}</ul></div></div><div class="pro-con-box-con-cell" data-wf-pbl="layout-grid-1x2-vertical"><div class="pro-con-box-con-cell-rich-text-block w-richtext"><h3><strong>Cons:</strong></h3><ul role="list">{cons}</ul></div></div></div></div>
<details class="ltt-bento-group" open="">
<summary class="ltt-bento-group-head">
<span class="ltt-bento-group-title">Summary &amp; Review</span>
<span class="ltt-bento-right">
<span class="ltt-mini-pill">Overview</span>
<span class="ltt-bento-chev">▾</span>
</span>
</summary>
<div class="ltt-bento-group-body">
<div class="w-richtext">{t['body']}<div class="ltt-filmstrip-wrap"><button aria-label="Previous photo" class="ltt-film-btn ltt-film-prev is-disabled" onclick="window.lttFilmSlide(this, -1)" type="button">‹</button><button aria-label="Next photo" class="ltt-film-btn ltt-film-next" onclick="window.lttFilmSlide(this, 1)" type="button">›</button><div aria-label="Filmstrip gallery {t['n']}" class="ltt-filmstrip" onscroll="window.lttFilmSync(this)" tabindex="0">{slides}</div></div></div>
<div class="ltt-buy-card">
<div class="ltt-buy-card-head">
<div class="ltt-buy-card-badge">
<span class="ltt-live-dot"></span>
<span>Official Tickets &amp; Live Availability</span>
</div>
<div class="ltt-buy-card-price">
<span class="ltt-buy-price-val">{t['price_txt']}</span>
<span class="ltt-buy-price-sub">{t['dur_short']} • Free cancellation</span>
</div>
</div>
<div class="ltt-buy-card-body">
<div class="ltt-buy-card-info">
<h4 class="ltt-buy-card-title">{t['title']}</h4>
<div class="ltt-buy-card-perks">
{perks}
</div>
</div>
<div class="ltt-buy-card-action">
<a class="ltt-buy-cta-btn" href="{href}" rel="noopener nofollow sponsored" target="_blank">
<span>Check Dates &amp; Book Tickets</span>
<span class="ltt-cta-arrow">→</span>
</a>
<div class="ltt-buy-card-trust">
{lock_svg}
<span>Best Price Guaranteed • Instant Confirmation</span>
</div>
</div>
</div>
</div>
</div>
</details>
<div class="qf1-wrap">
<div class="qf1-title-row">
<h4 class="qf1-title">Quick Facts</h4>
<span class="qf1-badge">{t['qf_badge']}</span>
</div>
<div class="qf1-table">
{qf}
</div>
<div class="qf1-Validation-pills">
{chips}
</div>
</div>
</div>
</details>
"""


INTRO_OLD_P1 = "I took six of the city's most popular walking tours myself, two of them free (you tip the guide at the end).</p>"
INTRO_NEW_P1 = ("I took six of the city's most popular walking tours myself, two of them free (you tip the guide at the end), "
                "then added the four worth booking for a specific job: <strong>a food tour, communist history, a private guide "
                "and a 3-hour Buda and Pest loop</strong>.</p>")
INTRO_OLD_P2 = "<strong>price (free to €35)</strong>, length (1.5 to 3 hours), where you meet and who each one suits."
INTRO_NEW_P2 = "<strong>price (free to €62)</strong>, length (1.5 to 3 hours, private tours longer), where you meet and who each one suits."

PICKS_ANCHOR = '<li><strong>Only one morning and tired legs:</strong>'
PICKS_NEW = """<li><strong>Hungarian food and drinks:</strong> <a href="#item-7-budapest-food-tour">Food walking tour</a> (from €62, 2.5 hours, 4 eateries, 3 drinks).</li>
<li><strong>Communism and the Cold War:</strong> <a href="#item-8-communist-history-tour">Communist History tour</a> (from €50, 2 hours, max 10 people, museum ticket).</li>
<li><strong>Kids, older travellers or your own pace:</strong> <a href="#item-9-private-walking-tour">Private walking tour</a> (from €40 per person, 2 to 8 hours, hotel pickup).</li>
<li><strong>Buda and Pest in one walk, smaller group:</strong> <a href="#item-10-orientation-walking-tour">3-Hour Orientation tour</a> (€35, 6 languages).</li>
"""

FAQ_NEW = [
    ("Is there a food walking tour in Budapest?",
     "Yes. The <strong>Budapest Food Walking Tour</strong> (2.5 hours, from €62) stops at four eateries in the Jewish Quarter: "
     "lángos, chicken paprikash and somlói cake, with pálinka, beer and Tokaji wine included. It can't cater for gluten-free or vegan diets yet."),
    ("Can you book a private walking tour in Budapest?",
     "Yes. A <strong>private custom tour</strong> starts from €40 per person for 2 to 8 hours: the guide meets you at your "
     "accommodation and builds the route around what you want to see. Museum tickets and food are extra."),
]


def main():
    s = PAGE.read_text()
    assert 'id="card-7"' not in s, "already applied"

    lock = re.search(r'<div class="ltt-buy-card-trust">\s*(<svg.*?</svg>)', s, re.S).group(1)

    # 1) move FAQ out of card 6 body
    faq_start = s.find('<h2 id="faq-dup2">')
    faq_end = s.find('<div class="ltt-filmstrip-wrap">', faq_start)
    faq = s[faq_start:faq_end]
    s = s[:faq_start] + s[faq_end:]
    # add the two new FAQ entries before "Can you walk around Buda Castle for free?"
    q_anchor = '<h3 class="cf-faq-questions-2">Can you walk around Buda Castle for free?</h3>'
    assert q_anchor in faq
    new_q = "".join(f'<h3 class="cf-faq-questions-2">{q}</h3><div class="cf-faq-answer-wrap-2">'
                    f'<div class="cf-faq-content-2 w-richtext"><p>{a}</p></div></div>' for q, a in FAQ_NEW)
    faq = faq.replace(q_anchor, new_q + q_anchor)
    faq = faq.replace(
        "Private tours cost more.",
        "The food tour is from €62, the communist history tour from €50 (museum ticket included), and private tours from €40 per person.")
    faq = faq.replace("was my favourite of the six.", "was my favourite of the six I took.")

    # 2) deck cards after card 6
    c6 = s.find('<div class="bpa-card" data-cat="c20 long both" id="card-6">')
    c6_tail = '<a class="bpa-sublink" href="#item-6-budapest-grand-city-tour">Read Review ↓</a>\n</div>\n</div>\n</div>\n'
    deck_end = s.find(c6_tail, c6) + len(c6_tail)  # right after card 6, still inside #ltt-cards-deck
    assert c6 > 0 and deck_end > len(c6_tail)
    s = s[:deck_end] + "".join(deck_card(t, s) for t in TOURS) + s[deck_end:]

    # 3) breakdown sections after item 6, then the FAQ
    i6 = s.find('id="item-6-budapest-grand-city-tour"')
    qf6 = s.find('<div class="qf1-wrap">', i6)
    end6 = s.find("</details>", qf6) + len("</details>")
    block = "\n" + "".join(details(t, s, lock) for t in TOURS) + '<div class="w-richtext bpa-wt-faq">' + faq + "</div>"
    s = s[:end6] + block + s[end6:]

    # 4) counts and labels
    reps = [
        ("<title>6 Best Walking Tours in Budapest (Free & Paid, Tested 2026)</title>",
         "<title>10 Best Walking Tours in Budapest (Free & Paid, 2026)</title>", 1),
        ('content="6 Best Walking Tours in Budapest (Free & Paid, Tested 2026)"',
         'content="10 Best Walking Tours in Budapest (Free & Paid, 2026)"', 2),
        ('<span class="ltt-bc-current">The 6 Best Walking Tours in Budapest in 2026</span>',
         '<span class="ltt-bc-current">The 10 Best Walking Tours in Budapest in 2026</span>', 1),
        ("The 6 Best Walking Tours in Budapest in 2026: Free and Paid <span class=\"ltt-h1-muted\">(Personally Tested)</span>",
         "The 10 Best Walking Tours in Budapest in 2026: Free and Paid <span class=\"ltt-h1-muted\">(6 Personally Tested)</span>", 1),
        ("Detailed Breakdown: 6 Best Walking Tours in Budapest", "Detailed Breakdown: 10 Best Walking Tours in Budapest", 1),
        ('"tocDeckLabel": "Top 6 Walking Tours", "tocBreakdownLabel": "Detailed Breakdown (6 Walking Tours)"',
         '"tocDeckLabel": "Top 10 Walking Tours", "tocBreakdownLabel": "Detailed Breakdown (10 Walking Tours)"', 1),
        ('"Grand City Tour of Budapest"]};',
         '"Grand City Tour of Budapest", ' + ", ".join(json.dumps(t["title"]) for t in TOURS) + "]};", 1),
        ("<span>All 6 Walking Tours</span>", "<span>All 10 Walking Tours</span>", 1),
        ('<p class="bpa-breakdown-sub">Personally field-tested •', '<p class="bpa-breakdown-sub">#1 to #6 personally field-tested •', 1),
        ("<span>Contents (6)</span>", "<span>Contents (10)</span>", 1),
        ("<p>Two of the six are <strong>free, tip-based walks</strong>", "<p>Two of the ten are <strong>free, tip-based walks</strong>", 1),
        (INTRO_OLD_P1, INTRO_NEW_P1, 1),
        (INTRO_OLD_P2, INTRO_NEW_P2, 1),
        (PICKS_ANCHOR, PICKS_NEW + PICKS_ANCHOR, 1),
    ]
    for old, new, n in reps:
        assert s.count(old) == n, (old[:70], s.count(old))
        s = s.replace(old, new)

    old_desc = ("I took 6 Budapest walking tours myself: 2 free tip-based walks, the castle caves, "
                "a night vampire walk and more. Paid tours from €12, and who each one suits.")
    new_desc = ("10 Budapest walking tours compared, 6 taken in person: free tip-based walks, castle caves, "
                "a food tour, communist history and private guides. From €12.")
    assert s.count(f'content="{old_desc}"') == 3
    s = s.replace(f'content="{old_desc}"', f'content="{new_desc}"')

    # 5) JSON-LD
    m = re.search(r'(<script id="ltt-schema-jsonld" type="application/ld\+json">)(.*?)(</script>)', s, re.S)
    data = json.loads(m.group(2))
    for node in data["@graph"]:
        if node["@type"] == "Article":
            node["headline"] = "The 10 Best Walking Tours in Budapest in 2026: Free and Paid"
            node["description"] = new_desc
            lst = node["mainEntity"]
            lst["name"] = node["headline"]
            lst["description"] = re.sub(r"<[^>]+>", "", re.search(r'<div class="ltt-lead-copy">(.*?)</div>', s, re.S).group(1)).replace("\n", " ").strip()
            lst["numberOfItems"] = 10
            for t in TOURS:
                lst["itemListElement"].append({
                    "@type": "ListItem", "position": t["n"], "url": f"{URL}#{t['anchor']}",
                    "item": {
                        "@type": "Product", "name": t["title"], "description": t["desc"],
                        "brand": {"@type": "Organization", "name": t["operator"]},
                        "image": [f"https://www.budapestadventures.com/assets/walking-tours-2026/{t['photos']}-{t['photo_order'][0]:02d}.webp"],
                        "aggregateRating": {"@type": "AggregateRating", "ratingValue": t["score"], "bestRating": "5",
                                            "worstRating": "1", "reviewCount": str(t["count_exact"])},
                        "offers": {"@type": "Offer", "price": str(t["price"]), "priceCurrency": "EUR",
                                   "availability": "https://schema.org/InStock",
                                   "url": GYG.format(slug=t["slug"], cmp=t["cmp"]).replace("&amp;", "&")},
                    },
                })
        if node["@type"] == "BreadcrumbList":
            node["itemListElement"][-1]["name"] = "The 10 Best Walking Tours in Budapest in 2026"
        if node["@type"] == "FAQPage":
            qs = node["mainEntity"]
            for q, a in FAQ_NEW:
                qs.insert(len(qs) - 1, {"@type": "Question", "name": q,
                                        "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}})
            for q in qs:
                q["acceptedAnswer"]["text"] = q["acceptedAnswer"]["text"].replace(
                    "Private tours cost more.",
                    "The food tour is from €62, the communist history tour from €50 (museum ticket included), and private tours from €40 per person."
                ).replace("was my favourite of the six.", "was my favourite of the six I took.")
    s = s[:m.start(2)] + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + s[m.end(2):]

    assert "—" not in s
    if PAGE.exists() and 'href="/css/listicle-cards.css' in PAGE.read_text():
        # The page is on the shared listicle design now: cards come from data/listicles/<slug>.json
        # (scripts/listicle.py build). This older builder would undo that.
        raise SystemExit(f"{PAGE.name} is built from data/listicles/; edit the card data instead")
    PAGE.write_text(s)
    print("ok")


if __name__ == "__main__":
    main()
