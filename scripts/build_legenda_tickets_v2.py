#!/usr/bin/env python3
"""Build /legenda-cruise-tickets-v2: the mockup-style redesign of the Legenda tickets page,
with a Legenda vs OTAs price matrix. noindex + canonical to v1 while we compare.

OTA facts checked 14 Nov 2026: Viator d499-35015P1/P2/P4, Tiqets p1114615 (Legenda option),
Klook 112272 / 112819 (all EUR).

Run: python3 scripts/build_legenda_tickets_v2.py
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_legenda_tickets as v1  # noqa: E402
from build_legenda_tickets import (CHECKED, FAQ, GYG_BELLA, GYG_DINNER, GYG_LEGEND, IMG, LEG_HOME,  # noqa: E402,F401
                                   PHOTOS, ROOT)

OUT = "legenda-cruise-tickets-v2.html"

CSS = """<style id="bpa-tickets-css">
.lt-page{font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;color:#0f172a;background:#f8fafc;line-height:1.5}
.lt-page *{box-sizing:border-box}
.lt-page h1,.lt-page h2,.lt-page h3{font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;text-align:left;color:inherit}
.lt-page a{color:#0284c7}
.lt-wrap{max-width:1120px;margin:0 auto;padding:0 24px}
.lt-hero{background:#0a192f;color:#fff;padding:20px 0 48px}
.lt-hero .lt-wrap{display:flex;flex-direction:column;gap:20px}
.lt-bc{margin:0;font-size:13px;color:#94a3b8}
.lt-bc a{color:#94a3b8!important;text-decoration:none}
.lt-bc a:hover{color:#fff!important}
.lt-hero h1{margin:0!important;font-size:clamp(30px,4.4vw,48px)!important;line-height:1.1!important;font-weight:800!important;letter-spacing:-.02em;max-width:880px;color:#fff!important;-webkit-text-fill-color:#fff;background:none!important;font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif!important;text-align:left!important}
.lt-pills{display:flex;flex-wrap:wrap;gap:10px;font-size:13px}
.lt-pill{background:rgba(255,255,255,.08);color:#e2e8f0;padding:6px 12px;border-radius:999px}
.lt-pill a{color:#e2e8f0!important}
.lt-pill-ok{background:rgba(16,185,129,.16);color:#6ee7b7;font-weight:600}
.lt-answer{background:#fff;color:#0f172a;border-radius:16px;padding:24px;display:flex;flex-wrap:wrap;gap:24px;align-items:center;margin-top:8px}
.lt-answer-txt{flex:999 1 420px;min-width:0;display:flex;flex-direction:column;gap:8px}
.lt-answer-txt p{margin:0;font-size:18px;line-height:1.5}
.lt-answer-cta{flex:1 1 230px;display:flex;flex-direction:column;gap:8px}
.lt-kicker{font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#059669}
.lt-small{font-size:12px;color:#64748b;text-align:center}
.lt-main{padding:48px 0 64px}
.lt-main .lt-wrap{display:flex;flex-direction:column;gap:56px}
.lt-sec{display:flex;flex-direction:column;gap:16px}
.lt-sec h2{margin:0!important;font-size:28px!important;line-height:1.2!important;font-weight:800!important;letter-spacing:-.01em;text-align:left!important;font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif!important}
.lt-sec>p,.lt-lead{margin:0;color:#475569;font-size:15px;line-height:1.6}
.lt-btn{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:0 18px;border-radius:10px;font-weight:700;font-size:15px;text-decoration:none!important;text-align:center;line-height:1.2}
.lt-btn-gold{background:#dfa732;color:#0a192f!important}.lt-btn-gold:hover{background:#b88214}
.lt-btn-out{background:#fff;border:1.5px solid #cbd5e1;color:#0a192f!important}.lt-btn-out:hover{border-color:#0a192f}
.lt-notice{margin:0;background:#fff7ed;border:1px solid #fed7aa;border-radius:12px;padding:14px 18px;font-size:15px;line-height:1.55;color:#7c2d12}
.lt-scroll{overflow-x:auto;-webkit-overflow-scrolling:touch;background:#fff;border:1px solid #e2e8f0;border-radius:16px}
.lt-table{width:100%;border-collapse:collapse;min-width:720px;margin:0}
.lt-table th{font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:#475569;text-align:left;padding:14px 16px;background:#f1f5f9;border-bottom:1px solid #e2e8f0;font-weight:600}
.lt-table td{padding:16px;border-bottom:1px solid #e2e8f0;vertical-align:middle;font-size:15px;color:#0f172a}
.lt-table tr:last-child td{border-bottom:0}
.lt-table td.lt-r{text-align:right}
.lt-sub{display:block;font-size:13px;color:#64748b;margin-top:2px}
.lt-same{display:inline-block;background:#ecfdf5;color:#047857;font-weight:700;padding:4px 10px;border-radius:8px}
.lt-muted{color:#64748b}
.lt-note{margin:0;font-size:13px;color:#64748b;line-height:1.6}
.lt-grid3{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}
.lt-card{background:#fff;border:1px solid #e2e8f0;border-radius:16px;padding:24px;display:flex;flex-direction:column;gap:12px}
.lt-card.lt-pick{border:2px solid #dfa732}
.lt-tag{font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#0284c7}
.lt-pick .lt-tag{color:#92400e}
.lt-card h3{margin:0;font-size:20px;line-height:1.3;font-weight:700}
.lt-card p{margin:0;color:#475569;line-height:1.6;font-size:15px}
.lt-card .lt-btn{margin-top:auto}
.lt-facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}
.lt-fact{background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:18px;display:flex;flex-direction:column;gap:4px}
.lt-fact-l{font-size:12px;color:#64748b;font-weight:600;text-transform:uppercase;letter-spacing:.06em}
.lt-fact-v{font-size:16px;font-weight:600;line-height:1.4}
.lt-fact-s{font-size:13px;color:#475569;line-height:1.5}
.lt-photos{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.lt-photos img{width:100%;height:220px;object-fit:cover;border-radius:14px;display:block}
.lt-faq{display:flex;flex-direction:column;gap:10px}
.lt-faq details{border:1px solid #e2e8f0;border-radius:12px;background:#fff;padding:0 20px}
.lt-faq summary{cursor:pointer;font-weight:600;font-size:16px;padding:18px 0;color:#0f172a}
.lt-faq details p{margin:0 0 18px;color:#334155;line-height:1.6;font-size:15px}
.lt-hub{background:#0a192f;color:#fff;border-radius:16px;padding:28px;display:flex;flex-wrap:wrap;gap:20px;align-items:center;justify-content:space-between}
.lt-hub-txt{flex:999 1 380px;min-width:0;display:flex;flex-direction:column;gap:6px}
.lt-hub h2{margin:0;font-size:22px;font-weight:800;color:#fff}
.lt-hub p{margin:0;color:#cbd5e1;font-size:15px;line-height:1.6}
.lt-hub .lt-btn{flex:1 1 220px}
.lt-matrix{min-width:860px}
.lt-rowhl td{background:#f8fafc}
.lt-verdict{background:#fff;border:2px solid #10b981;border-radius:16px;padding:20px 22px;display:flex;flex-direction:column;gap:6px}
.lt-verdict p{margin:0;font-size:16px;line-height:1.6}
@media (max-width:600px){.lt-wrap{padding:0 16px}.lt-answer{padding:20px}.lt-answer-txt p{font-size:16px}.lt-sec h2{font-size:24px}.lt-photos{grid-template-columns:1fr 1fr}.lt-photos img{height:140px}.lt-photos img:nth-child(3){display:none}}
</style>"""


def body():
    photos = "".join(f'<img src="{IMG}{f}" alt="{a}" width="600" height="400" loading="lazy" decoding="async">'
                     for f, a in PHOTOS)
    faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQ)
    return f"""{CSS}
<div class="lt-page">
<section class="lt-hero"><div class="lt-wrap">
<nav aria-label="Breadcrumb" class="lt-bc"><a href="/">Home</a> / <a href="/best-budapest-river-cruises">River cruises</a> / Legenda cruise tickets</nav>
<h1>Legenda Cruise Tickets Budapest 2026: Prices, Times &amp; Where to Buy</h1>
<div class="lt-pills">
<span class="lt-pill lt-pill-ok">Prices checked: {CHECKED}</span>
<span class="lt-pill">Official site vs 4 booking sites</span>
<span class="lt-pill">3 cruises compared</span>
<span class="lt-pill">By <a href="/about">Adam Dimitrov</a>, local Budapest guide</span>
</div>
<div class="lt-answer">
<div class="lt-answer-txt">
<span class="lt-kicker">Short answer</span>
<p>A Legenda adult ticket costs <strong>€20</strong> for the daytime Duna Bella cruise, <strong>€25</strong> for the evening Danube Legend cruise and <strong>€110</strong> for the Candlelit Dinner Cruise. GetYourGuide, Viator, Tiqets and Klook all charge exactly the same.</p>
<p>Buy on <strong>GetYourGuide</strong> for free cancellation up to 24 hours before. Buy on <strong>legenda.hu</strong> if you are a student or have kids aged 10 to 14: the official site lists lower prices for them.</p>
</div>
<div class="lt-answer-cta">
<a class="lt-btn lt-btn-gold" href="{GYG_LEGEND}" rel="sponsored noopener" target="_blank">Evening cruise, €25</a>
<a class="lt-btn lt-btn-out" href="{LEG_HOME}" rel="sponsored noopener" target="_blank">Student &amp; kids prices on legenda.hu</a>
<span class="lt-small">Instant mobile ticket</span>
</div>
</div>
</div></section>

<main class="lt-main"><div class="lt-wrap">
<p class="lt-notice"><strong>Route change right now:</strong> because of the very low Danube water level, Legenda's daytime cruises cannot dock at Margaret Island and currently follow the evening route. Notice on legenda.hu, still up on {CHECKED}.</p>

<section class="lt-sec">
<h2 id="legenda-ticket-prices">Legenda ticket prices: official site vs every booking site</h2>
<p>We checked the three Legenda cruises on the official site and on the four big booking sites. The adult price is identical everywhere, so you cannot save by shopping around. What changes is the cancellation policy and which tickets each site sells.</p>
<div class="lt-scroll"><table class="lt-table lt-matrix">
<thead><tr><th>Cruise</th><th>legenda.hu</th><th>GetYourGuide</th><th>Viator</th><th>Tiqets</th><th>Klook</th></tr></thead>
<tbody>
<tr><td><strong>Duna Bella</strong> (daytime)<span class="lt-sub">1h10 · audio guide · 1 drink + lemonade</span></td><td><strong>€20</strong></td><td><strong>€20</strong><span class="lt-sub">4.6 (4,428)</span></td><td><strong>€20</strong><span class="lt-sub">4.5 (1,097)</span></td><td><strong>€20</strong><span class="lt-sub">4.9 (11) · inside a combined listing</span></td><td class="lt-muted">Not sold</td></tr>
<tr><td><strong>Danube Legend</strong> (evening)<span class="lt-sub">1 hour · film and audio guide · 1 drink</span></td><td><strong>€25</strong></td><td><strong>€25</strong><span class="lt-sub">4.5 (10,998)</span></td><td><strong>€25</strong><span class="lt-sub">4.3 (4,255)</span></td><td class="lt-muted">Not sold</td><td><strong>€25</strong><span class="lt-sub">4.6 (454)</span></td></tr>
<tr><td><strong>Candlelit Dinner Cruise</strong><span class="lt-sub">2h30 · 4-course à la carte · live music</span></td><td><strong>€110</strong></td><td><strong>€110</strong><span class="lt-sub">4.7 (2,432)</span></td><td><strong>€110</strong><span class="lt-sub">4.5 (2,056)</span></td><td class="lt-muted">Not sold</td><td><strong>€110</strong><span class="lt-sub">4.7 (37)</span></td></tr>
<tr class="lt-rowhl"><td><strong>Free cancellation</strong></td><td>No refund; rebook in person at the pier</td><td><span class="lt-same">Up to 24h</span></td><td><span class="lt-same">Up to 24h</span></td><td>Depends on option</td><td><span class="lt-same">Up to 24h</span></td></tr>
<tr class="lt-rowhl"><td><strong>Student and youth prices</strong></td><td><span class="lt-same">Listed</span></td><td class="lt-muted">At checkout</td><td>Kids rates</td><td class="lt-muted">At checkout</td><td class="lt-muted">At checkout</td></tr>
<tr><td></td><td><a class="lt-btn lt-btn-out" href="{LEG_HOME}" rel="sponsored noopener" target="_blank">legenda.hu</a></td><td><a class="lt-btn lt-btn-gold" href="{GYG_LEGEND}" rel="sponsored noopener" target="_blank">GetYourGuide</a></td><td></td><td></td><td></td></tr>
</tbody></table></div>
<p class="lt-note">Adult prices in EUR, checked on {CHECKED} on legenda.hu and on the Legenda listings of each site (GetYourGuide, Viator, Klook: run by Legenda; Tiqets: Legenda's daytime option inside its "Budapest: Sightseeing Cruise" listing). Ratings are each site's own score and review count. We may earn a commission from legenda.hu and GetYourGuide, at no extra cost to you.</p>
<div class="lt-verdict"><span class="lt-kicker">Our verdict</span><p><strong>Same price on all five sites.</strong> Book on GetYourGuide (or Viator / Klook) if your plans might change: all three refund up to 24 hours before. Book on legenda.hu if you are a student or have kids aged 10 to 14, since the discounted prices are listed there up front.</p></div>
</section>

<section class="lt-sec">
<h2 id="official-site-vs-getyourguide">Official site or booking site: the difference</h2>
<p>The price is the same, so the choice comes down to the terms.</p>
<div class="lt-scroll"><table class="lt-table">
<thead><tr><th></th><th>legenda.hu (official)</th><th>GetYourGuide</th></tr></thead>
<tbody>
<tr><td><strong>Adult price</strong></td><td>€20 / €25 / €110</td><td>€20 / €25 / €110</td></tr>
<tr><td><strong>Cancellation</strong></td><td>Can be moved to another day and time if there is space, in person at the pier only</td><td><span class="lt-same">Full refund up to 24h before</span></td></tr>
<tr><td><strong>Pay later</strong></td><td class="lt-muted">Not offered</td><td>Reserve now, pay later</td></tr>
<tr><td><strong>Student and child prices</strong></td><td><span class="lt-same">Students €18 / €22.50, kids 10 to 14 €14 / €17.50, under 10 free</span></td><td class="lt-muted">See ticket options at checkout</td></tr>
<tr><td><strong>Best for</strong></td><td>Students and families with kids 10 to 14</td><td>Anyone whose plans might change</td></tr>
</tbody></table></div>
<p class="lt-note">Cancellation terms from Legenda's FAQ page and the GetYourGuide listings, {CHECKED}.</p>
</section>

<section class="lt-sec">
<h2 id="which-legenda-ticket">Which Legenda ticket should you buy?</h2>
<div class="lt-grid3">
<div class="lt-card"><span class="lt-tag">Daytime · €20</span><h3>Duna Bella</h3><p>A 1h10 daytime loop with a drink and a glass of Duna Bella lemonade. When the water is high enough you can get off for 45 minutes on Margaret Island and take a later boat back.</p><a class="lt-btn lt-btn-gold" href="{GYG_BELLA}" rel="sponsored noopener" target="_blank">€20 on GetYourGuide</a></div>
<div class="lt-card lt-pick"><span class="lt-tag">Evening · €25 · most reviewed</span><h3>Danube Legend</h3><p>One hour after dark past the lit-up Parliament and Buda Castle, with a film and audio guide in 30 languages and one drink. Boats leave every 20 minutes, so it is easy to fit in.</p><a class="lt-btn lt-btn-gold" href="{GYG_LEGEND}" rel="sponsored noopener" target="_blank">€25 on GetYourGuide</a></div>
<div class="lt-card"><span class="lt-tag">Dinner · €110</span><h3>Candlelit Dinner Cruise</h3><p>2h30 on the glass-roofed panorama boat with a 4-course à la carte dinner, welcome drink and live music. Other drinks are paid on board. <a href="/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest">Read our review</a>.</p><a class="lt-btn lt-btn-gold" href="{GYG_DINNER}" rel="sponsored noopener" target="_blank">€110 on GetYourGuide</a></div>
</div>
</section>

<div class="lt-photos">{photos}</div>

<section class="lt-sec">
<h2 id="student-and-child-prices">Student and child prices</h2>
<div class="lt-scroll"><table class="lt-table">
<thead><tr><th>Ticket</th><th>Duna Bella (day)</th><th>Danube Legend (evening)</th></tr></thead>
<tbody>
<tr><td>Adult</td><td>€20</td><td>€25</td></tr>
<tr><td>Student (valid ID at boarding)</td><td>€18</td><td>€22.50</td></tr>
<tr><td>Child 10 to 14</td><td>€14</td><td>€17.50</td></tr>
<tr><td>Child 0 to 9</td><td><span class="lt-same">Free</span></td><td><span class="lt-same">Free</span></td></tr>
</tbody></table></div>
<p class="lt-note">Dinner cruise: Exclusive Dinner Package €110, Kid's Dinner Package (3 to 12 years) €84. Source: legenda.hu/en/prices, {CHECKED}. Groups of 20 or more: see our <a href="/budapest-river-cruise-group-booking">group cruise booking</a> page.</p>
</section>

<section class="lt-sec">
<h2 id="timetable">Legenda timetable this season</h2>
<div class="lt-scroll"><table class="lt-table">
<thead><tr><th>Dates</th><th>Duna Bella (day)</th><th>Danube Legend (evening)</th><th>Dinner cruise</th></tr></thead>
<tbody>
<tr><td>25 Oct to 22 Nov 2026</td><td>11:00, 12:30, 14:00, 15:30</td><td>Every 20 min, 16:20 to 21:00</td><td>19:00</td></tr>
<tr><td>23 Nov to 31 Dec 2026</td><td>11:00, 12:30, 14:00, 15:30</td><td>15:40, then every 20 min 16:20 to 21:00</td><td>19:00</td></tr>
</tbody></table></div>
<p class="lt-note">The 15:30 daytime sailing never stops at Margaret Island. On 24 December only the 11:00, 12:30, 14:00 and 15:30 sailings run. In summer (22 May to 23 July) daytime boats leave every 45 minutes from 10:15 and the dinner cruise leaves at 19:45. Source: legenda.hu/en/timetable, {CHECKED}.</p>
</section>

<section class="lt-sec">
<h2 id="what-is-included">What your ticket includes</h2>
<div class="lt-facts">
<div class="lt-fact"><span class="lt-fact-l">Duna Bella · €20</span><span class="lt-fact-v">1h10 daytime cruise</span><span class="lt-fact-s">30-language audio guide, 1 drink (champagne, wine, beer, soft drink or water), 1 Duna Bella lemonade, free Wi-Fi. Optional 45 min on Margaret Island when water levels allow.</span></div>
<div class="lt-fact"><span class="lt-fact-l">Danube Legend · €25</span><span class="lt-fact-v">1-hour evening cruise</span><span class="lt-fact-s">Film and audio guide in 30 languages, 1 drink (champagne, wine, beer, soft drink or water), free Wi-Fi.</span></div>
<div class="lt-fact"><span class="lt-fact-l">Candlelit Dinner · €110</span><span class="lt-fact-v">2h30 dinner cruise</span><span class="lt-fact-s">Welcome drink, live music, 4-course à la carte dinner (kids: 3-course menu). Other drinks are paid on board.</span></div>
<div class="lt-fact"><span class="lt-fact-l">Departure pier</span><span class="lt-fact-v">Dock 7, Jane Haining rakpart</span><span class="lt-fact-s">1052 Budapest, Pest side below Vigadó tér. <a href="https://maps.google.com/?q=Legenda+City+Cruises+Dock+7+Budapest" rel="noopener" target="_blank">Open in Maps</a></span></div>
<div class="lt-fact"><span class="lt-fact-l">Metro</span><span class="lt-fact-v">M1 (yellow) to Vörösmarty tér</span><span class="lt-fact-s">Walk to Vigadó tér, go down the stairs, cross at the lights, turn left and walk about 50 m.</span></div>
<div class="lt-fact"><span class="lt-fact-l">Book ahead?</span><span class="lt-fact-v">Recommended, not required</span><span class="lt-fact-s">Sightseeing boats run often. The dinner cruise sails once a night, so book that one early.</span></div>
</div>
</section>

<section class="lt-sec">
<h2 id="faq">Legenda tickets: FAQ</h2>
<div class="lt-faq">{faq}</div>
</section>

<section class="lt-hub">
<div class="lt-hub-txt"><h2>Not set on Legenda?</h2><p>We compared 10 Budapest river cruises side by side: price, drinks, route and ratings.</p></div>
<a class="lt-btn lt-btn-gold" href="/best-budapest-river-cruises">Compare all river cruises</a>
</section>

<p class="lt-note">Prices are adult prices in EUR, checked on {CHECKED} on legenda.hu and GetYourGuide. Budapest Adventures is independent and may earn a commission from bookings on either site.</p>
</div></main>
</div>"""


def main():
    s = open(os.path.join(ROOT, v1.OUT), encoding="utf-8").read()
    a = s.find('<div class="ltt-hero-wrap">')
    b = s.find('<style id="bpa-new-footer"')
    assert 0 < a < b
    s = s[:a] + body() + s[b:]
    s = s.replace('<meta charset="utf-8"/>', '<meta charset="utf-8"/><meta content="noindex, follow" name="robots"/>', 1)
    s = re.sub(r'<link href="[^"]*" hreflang="[^"]*" rel="alternate"/>', "", s)
    assert "—" not in body()
    with open(os.path.join(ROOT, OUT), "w", encoding="utf-8") as fh:
        fh.write(s)
    print("wrote", OUT, len(s))


if __name__ == "__main__":
    main()
