#!/usr/bin/env python3
"""Build /best-pub-crawls-budapest (EN only) from the walking-tours page shell, 2026-11-15.

Facts come from the live GetYourGuide product pages read on 2026-11-15 in Chrome:
rating and review count from each page's structured data, the lowest bookable
adult price, a Friday 20 November 2026 availability sample (start times and
prices), inclusions, venue lists and meeting points. None of these crawls were
personally tested: no "tested" claims, no author review in JSON-LD.

Duplicate listings left out (same meeting point, start times, guides or venues
as a listing we kept): t1162545 (= t1068003), t1514577 and t1540470 (Party Deck
family, = t694395). t696959 is the private version of t470234 and is linked
from that card. Photos are the operators' listing photos in /assets/pub-crawls-2026/.

Re-runnable: always rebuilds the page from best-walking-tours-budapest.html.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "best-walking-tours-budapest.html"
PAGE = ROOT / "best-pub-crawls-budapest.html"
SITE = "https://www.budapestadventures.com"
SLUG = "best-pub-crawls-budapest"
URL = f"{SITE}/{SLUG}"
GYG = "https://www.getyourguide.com/budapest-l29/{slug}/?partner_id=YS414AJ&amp;utm_medium=online_publisher&amp;cmp={cmp}&amp;mkt_cmp=true"
REL = 'rel="nofollow sponsored noopener"'
CHECKED = "15 November 2026"
CHECKED_SHORT = "Nov 15, 2026"
IMG = "/assets/pub-crawls-2026"

TITLE = "6 Best Pub Crawls in Budapest: Ruin Bar Tours Compared (2026)"
H1 = 'The 6 Best Pub Crawls and Ruin Bar Tours in Budapest in 2026 <span class="ltt-h1-muted">(From €2)</span>'
H1_PLAIN = "The 6 Best Pub Crawls and Ruin Bar Tours in Budapest in 2026"
DESC = ("Budapest's 6 best pub crawls side by side: what a €2 ticket covers vs €25, start times, "
        "which ruin bars and clubs, how late they end and who each one suits.")

PRIVATE_OEI = GYG.format(slug="private-pub-crawl-berlin-with-vip-entry-t696959", cmp="pub-crawls-original-private")

CRAWLS = [
    dict(
        n=1, anchor="item-1-ruin-bar-pub-crawl", rank="🏆 #1 Best Overall", gold=True,
        operator="RuinBarCrawlBudapest", short_op="RuinBarCrawl",
        title="Pub Crawl &amp; Ruin Bar Tour with Free Shots &amp; VIP Entry",
        slug="budapest-pub-crawl-ruin-bar-tour-free-shots-vip-entry-t1068003", cmp="pub-crawls-ruinbarcrawl",
        score="4.9", count="3,813", count_exact=3813, rating=4.88, price=2, price_txt="From €2",
        dur="5 to 5.5 Hours", dur_short="5 to 5.5 hours", place="Erzsébet körút 36", map="Erzsébet+körút+36+Budapest",
        cats="u10 party late", photos="ruinbarcrawl", nphotos=6,
        alts=["Pub crawl guests in a vaulted Budapest ruin bar cellar",
              "Friends dancing on a Budapest ruin bar crawl",
              "Large pub crawl group on Erzsébet körút at night",
              "Pub crawl group photo by the Danube at night",
              "Crawl group outside a District VII bar",
              "Pub crawl group gathering at the meeting point"],
        specs=[("🍻", "4-5 Venues", "Pubs, ruin bars, then a club.", "Icebreakers at the start, drinking games along the way.", "The route changes with opening hours and crowds."),
              ("⏱", "5 to 5.5 Hours", "Starts 21:10, 21:40 or 22:20.", "The 21:10 start ends around 02:10, the 22:20 start around 03:20, inside a club you can stay in.", "The 5.5-hour version starts at 21:40."),
              ("🥃", "Shot at Every Venue", "Free: a welcome shot at every venue.", "Every other drink you buy at the bar.", "Food is not included."),
              ("🎟️", "VIP Club Entry", "Fast-track entry", "at Instant-Fogas, Füge Udvar, La Siesta and Humbák, through a separate entrance.", "Useful on Friday and Saturday, when the club queues are longest.")],
        best_for="Solo travellers and first-timers who want the biggest, busiest crawl in town: a shot at every stop and no queue at the club.",
        pros=["A welcome shot at every venue, plus VIP entry at Instant-Fogas, Füge Udvar, La Siesta and Humbák",
              "Three start times (21:10, 21:40, 22:20), so dinner first is easy",
              "Budapest's most-reviewed crawl, and the guides take photos for you"],
        cons=["Shots are the only free drinks: every beer and cocktail is on you",
              "The €2 price is not every night: €8.50 on the Friday we checked",
              "It's a crowd, not a cosy bar tour"],
        body="""<p>This is the crawl most people in Budapest end up on, and the numbers explain why: <strong>4.9 from 3,813 reviews</strong> and a ticket from <strong>€2</strong>. You meet on <strong>Erzsébet körút</strong>, do a round of icebreakers, then move through <strong>4 to 5 venues</strong>: pubs, ruin bars and a club to finish.</p>
<p>What the ticket buys: a <strong>welcome shot at every venue</strong>, <strong>VIP fast-track entry</strong> at Instant-Fogas, Füge Udvar, La Siesta and Humbák, drinking games and digital photos. What it doesn't: food, and every other drink you order. The official part runs <strong>5 to 5.5 hours</strong>, so a 21:10 start ends around 02:10 and the 22:20 start around 03:20, inside a club you can stay in.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> if you're travelling solo or it's your first night in town: the group is big, international and loud, and the guides do the planning. Reviewers keep naming the guides, not the bars, which tells you what you're paying for.</p>
<p><strong>Skip it</strong> if you want quiet ruin bar courtyards and a proper drink. The <a href="#item-5-hidden-bars-cocktail-crawl">cocktail crawl</a> is the opposite night.</p>
<h3>Meeting Point</h3>
<p>🗺️ <strong>Meeting Point: </strong>Erzsébet körút 36, 1073 Budapest (District VII).<br/>🚇 <strong>Public Transport:</strong> Tram 4 or 6 to Wesselényi utca / Erzsébet körút, or M2 to Blaha Lujza tér.</p>""",
        qf_badge="Erzsébet körút (District VII)",
        qf=[("Duration", "5 or 5.5 Hours"), ("Price", "From €2 / person (€8.50 on Fri 20 Nov 2026)"),
            ("Start Times", "21:10, 21:40 or 22:20 (the 5.5-hour version starts at 21:40)"),
            ("Meeting Point", "Erzsébet körút 36, 1073 Budapest"),
            ("Venues", "4 to 5 pubs, ruin bars and a club"),
            ("Included", "Welcome shot at every venue, VIP entry, drinking games, digital photos"),
            ("Not Included", "Food and any other drinks"),
            ("Age", "18+, bring a passport or ID card"),
            ("Private Option", "For groups of 10 or more")],
        chips=[("yes", "✓ Shot at Every Venue"), ("yes", "✓ VIP Club Entry"), ("yes", "✓ Photos Included"),
               ("no", "✕ Other Drinks Extra"), ("no", "✕ Under 18s")],
        perks=["Start: <strong>21:10 to 22:20</strong>", "Duration: <strong>5 to 5.5 Hours</strong>"],
        desc="Budapest's most-reviewed ruin bar crawl: 4-5 venues, a shot at each and VIP club entry.",
    ),
    dict(
        n=2, anchor="item-2-highest-rated-pub-crawl", rank="#2 Highest Rated",
        operator="Budapest Nightlife Tours", short_op="Budapest Nightlife Tours",
        title="Ruin Bars Pub Crawl with Free Shots &amp; VIP Entry",
        slug="budapest-nighttime-ruin-bars-crawl-with-6-shots-vip-entry-t1220969", cmp="pub-crawls-nightlife",
        score="5.0", count="1,657", count_exact=1657, rating=4.96, price=2.18, price_txt="From €2.18",
        dur="5.5 Hours", dur_short="5.5 hours", place="Erzsébet körút 19", map="Erzsébet+körút+19+Budapest",
        cats="u10 party late", photos="nightlife", nphotos=7,
        alts=["Pub crawl group outside Füge Udvar ruin bar, Budapest",
              "Crowded dance floor on the Budapest ruin bar crawl",
              "Dancing in a vaulted Budapest ruin bar",
              "Pub crawl group outside Humbák Borkápolna",
              "Dancers on stage in a Budapest party bar",
              "Friends in party masks on the ruin bar crawl",
              "Crawl guests in sunglasses at the final club"],
        specs=[("🍻", "3-4 Bars + Club", "Route pool:", "Humbák Borkápolna, Stifler Ház, Doboz, La Siesta, Lámpás and Blue Bird Karaoke Rooms, ending at Instant.", "Stops rotate from night to night."),
              ("⏱", "5.5 Hours", "Starts 21:00, 21:30 or 22:00.", "Ends around 02:30 to 03:30.", "Fri 20 Nov 2026: €2.18 at 21:00 or 22:00, €4 at 21:30."),
              ("🥃", "Welcome + Club Shots", "Free drinks:", "a welcome shot at the first ruin bar, then free shots at the club.", "Other drinks and food are extra."),
              ("⭐", "Rated 5.0", "5.0 from 1,657 reviews.", "Guests mention guides who keep the group together between bars.", "Rating checked on 15 November 2026.")],
        best_for="Anyone who wants the best-reviewed big crawl: a welcome shot, 3-4 bars, then VIP club entry with free shots, for about €2.",
        pros=["The top rating of any big Budapest crawl: 5.0 from 1,657 reviews",
              "Cheap on a Friday too: €2.18 (21:00 or 22:00) or €4 (21:30)",
              "Birthday and hen groups get a surprise extra"],
        cons=["Fewer bars than #1: 3-4 plus the club",
              "Free drinks are the welcome shot and the shots at the club"],
        body="""<p>Same price bracket as #1, smaller route, better score: <strong>5.0 from 1,657 reviews</strong>. You meet at <strong>Erzsébet körút 19</strong>, get a <strong>welcome shot</strong> at the first ruin bar, play a few games, and hop through <strong>3 to 4 bars</strong> before finishing at a club with <strong>VIP fast-track entry and free shots</strong>.</p>
<p>The route rotates, but the pool on the listing reads like a District VII greatest hits: <strong>Humbák Borkápolna, Stifler Ház, Doboz, La Siesta, Lámpás, Blue Bird Karaoke Rooms</strong> and <strong>Instant</strong> to end. The night runs <strong>5.5 hours</strong>: start at 21:00 and you're officially done around 02:30.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> if you're choosing on reviews alone, or you're a pair of friends who want a ready-made group without the 30-plus crowds. Guests mention guides who keep everyone together between bars.</p>
<p><strong>Skip it</strong> if you want as many venues as possible in one night: <a href="#item-3-late-start-pub-crawl">Party Deck</a> does 5 to 6.</p>
<h3>Meeting Point</h3>
<p>🗺️ <strong>Meeting Point: </strong>Erzsébet körút 19, 1073 Budapest (private groups meet at Erzsébet körút 15).<br/>🚇 <strong>Public Transport:</strong> Tram 4 or 6 to Wesselényi utca / Erzsébet körút.</p>""",
        qf_badge="Erzsébet körút (District VII)",
        qf=[("Duration", "5.5 Hours"), ("Price", "From €2.18 / person (€2.18 or €4 on Fri 20 Nov 2026)"),
            ("Start Times", "21:00, 21:30 or 22:00"),
            ("Meeting Point", "Erzsébet körút 19, 1073 Budapest"),
            ("Venues", "3 to 4 bars, then a club"),
            ("Included", "Welcome shot, VIP club entry with free shots, photos"),
            ("Not Included", "Food and other drinks"),
            ("Age", "18+, bring ID (a copy is accepted)"),
            ("Private Option", "For groups of 10 or more")],
        chips=[("yes", "✓ Rated 5.0"), ("yes", "✓ VIP Club Entry"), ("yes", "✓ Birthday Surprise"),
               ("no", "✕ Other Drinks Extra")],
        perks=["Start: <strong>21:00 to 22:00</strong>", "Duration: <strong>5.5 Hours</strong>"],
        desc="Top-rated ruin bar crawl: welcome shot, 3-4 bars and VIP club entry with free shots.",
    ),
    dict(
        n=3, anchor="item-3-late-start-pub-crawl", rank="#3 Best Late Start",
        operator="Party Deck", short_op="Party Deck",
        title="Strangers-to-Friends Ruin Pub Tour: VIP Entry, Games &amp; Shots",
        slug="budapest-guided-pub-tour-to-ruin-bars-with-games-6-shots-t694395", cmp="pub-crawls-partydeck",
        score="4.8", count="2,514", count_exact=2514, rating=4.80, price=2, price_txt="From €2",
        dur="5 to 6 Hours", dur_short="5 to 6 hours", place="Dohány utca 35", map="Dohány+utca+35+Budapest",
        cats="u10 party late", photos="partydeck", nphotos=7,
        alts=["Party Deck pub crawl group in a long ruin bar cellar",
              "Packed Budapest bar on the Party Deck crawl",
              "Drinking games at the first bar of the crawl",
              "Friends laughing on a Budapest ruin pub tour",
              "Pinball machines in a Budapest ruin bar",
              "Pub crawl group photo outside the meeting point",
              "Neon-lit bar stage on the Budapest crawl"],
        specs=[("🍻", "5-6 Venues", "From a pool of 10+:", "Doboz, Füge Udvar, KAZI, Humbák, Vörös Neon, La Siesta and Instant-Fogas (VIP entry).", "The route is picked each night by crowds and events."),
              ("⏱", "5 or 6 Hours", "22:00 start (5 hours) or 21:00 start (6 hours).", "Both end around 03:00.", "Fri 20 Nov 2026: €2 for the 22:00 start, €6 for 21:00."),
              ("🥃", "Tequila, Vodka, Pálinka", "Shots included", "along the route, plus drinking games at the first bar.", "The 1-hour open bar (long drinks, wine, beer) is a paid extra."),
              ("🗣️", "English + Spanish", "Guides speak English and Spanish.", "You join a WhatsApp group at check-in with the route and map links.", "Local rules stop hosts guiding groups on the street.")],
        best_for="Late arrivals and people who want the longest night: join at 22:00 after dinner, or do the 6-hour version from 21:00.",
        pros=["A 22:00 start for people with dinner plans (€2 on the Friday we checked)",
              "Real shots included: tequila, vodka and pálinka",
              "The most venues of any crawl here: 5 to 6, and Spanish-speaking guides too"],
        cons=["The 1-hour open bar is a paid extra, not in the base price",
              "Hosts can't lead the group on the street: you follow the route on WhatsApp"],
        body="""<p>Party Deck solves the most common pub crawl problem: you booked dinner for 20:00 and every crawl leaves at 21:00. Their <strong>5-hour option starts at 22:00</strong> (€2 on the Friday we checked), and the <strong>6-hour option starts at 21:00</strong> (€6). Either way you finish around 03:00.</p>
<p>The night covers <strong>5 to 6 ruin bars and clubs</strong> from a pool of more than ten: <strong>Doboz, Füge Udvar, KAZI, Humbák, Vörös Neon, La Siesta</strong> and <strong>Instant-Fogas</strong>, which gets VIP entry. Shots are proper ones: <strong>tequila, vodka and pálinka</strong>. A <strong>1-hour open bar</strong> (long drinks, wine and beer) is sold as an extra.</p>
<p>One thing to know: local rules stop the hosts guiding groups through the streets, so you <strong>scan a QR code at check-in to join a WhatsApp group</strong> with the bar names, timings and map links. The hosts party with you inside every bar. Anyone who turns up visibly drunk is turned away.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> if you're eating late, want the most bars for your money, or speak Spanish. Solo reviewers write about the group as much as the bars.</p>
<p><strong>Skip it</strong> if you want someone physically walking you between bars all night: <a href="#item-1-ruin-bar-pub-crawl">#1</a> and <a href="#item-2-highest-rated-pub-crawl">#2</a> feel more hand-held.</p>
<h3>Meeting Point</h3>
<p>🗺️ <strong>Meeting Point: </strong>JO&amp;JOE Budapest, Dohány utca 35, 1074 Budapest (District VII).<br/>🚇 <strong>Public Transport:</strong> M2 to Blaha Lujza tér or Astoria, then 5 minutes on foot.</p>""",
        qf_badge="Dohány utca (District VII)",
        qf=[("Duration", "5 or 6 Hours"), ("Price", "From €2 / person (€2 or €6 on Fri 20 Nov 2026)"),
            ("Start Times", "21:00 (6 hours) or 22:00 (5 hours)"),
            ("Meeting Point", "JO&amp;JOE Budapest, Dohány utca 35, 1074 Budapest"),
            ("Venues", "5 to 6 ruin bars and clubs, Instant-Fogas VIP entry"),
            ("Included", "Tequila, vodka and pálinka shots, drinking games, photos, VAT"),
            ("Not Included", "1-hour open bar (optional extra), food"),
            ("Languages", "English, Spanish"),
            ("Age", "18+, bring ID (a copy is accepted)")],
        chips=[("yes", "✓ 22:00 Late Start"), ("yes", "✓ 5-6 Venues"), ("yes", "✓ Spanish Guides"),
               ("no", "✕ Open Bar Costs Extra"), ("no", "✕ No Street Guiding")],
        perks=["Start: <strong>21:00 or 22:00</strong>", "Duration: <strong>5 to 6 Hours</strong>"],
        desc="Longest ruin bar crawl with a 22:00 late start, 5-6 venues and tequila, vodka and pálinka shots.",
    ),
    dict(
        n=4, anchor="item-4-irish-pub-start-crawl", rank="#4 Easiest Meeting Point",
        operator="Original Europe Tours", short_op="Original Europe Tours",
        title="Ruin Bar Pub Crawl with Entry Tickets &amp; VIP Club Entry",
        slug="budapest-ruin-bar-pub-crawl-with-nightlife-guide-t470234", cmp="pub-crawls-original",
        score="4.8", count="1,279", count_exact=1279, rating=4.76, price=19, price_txt="From €19",
        dur="5 Hours", dur_short="5 hours", place="Liszt Ferenc tér", map="Liszt+Ferenc+tér+11+Budapest",
        cats="p10 party", photos="original", nphotos=6,
        alts=["Pub crawl group on a District VII street at night",
              "Crawl guests gathered at the start of the night",
              "Pub crawl group with guide in a Budapest bar",
              "Group of friends on the Budapest pub crawl",
              "Crawl group in a Budapest ruin bar lounge",
              "Guests toasting in a Budapest cellar bar"],
        specs=[("🍺", "Starts in an Irish Pub", "Meet at Becketts Irish Bar,", "Liszt Ferenc tér 11, at 21:30.", "On New Year's Eve it meets at Klauzál utca 10."),
              ("⏱", "5 Hours", "21:30 to around 02:30.", "One start time every night.", "Not for guests over 70, per the operator."),
              ("🍻", "3 Bars + Club", "Listed route:", "Becketts, Doboz, La Siesta, Badabing, Füge Udvar, Place Bár, ending at Instant.", "Fast-track VIP entry at Instant-Fogas."),
              ("🎟️", "Entrance Fees Incl.", "Included:", "free shots, entrance fees and drinking games.", "The food stop is pay-as-you-go. Private version: €100 per group of up to 12 (Fri 20 Nov 2026).")],
        best_for="People who'd rather meet in a real pub than on a street corner, and groups of up to 12 who want the same night to themselves.",
        pros=["Meets at Becketts Irish Bar on Liszt Ferenc tér: easy to find, easy to wait in",
              "Free shots, drinking games, entrance fees and fast-track entry at Instant-Fogas",
              "Private version for your own group: €100 per group of up to 12 on the Friday we checked"],
        cons=["Costs more than the €2 crawls for a similar night (€19)",
              "The food stop is pay-as-you-go, not included",
              "Not for over-70s, per the operator"],
        body=f"""<p>The most traditional crawl on this list: one start time (<strong>21:30</strong>), one meeting point in a proper pub (<strong>Becketts Irish Bar, Liszt Ferenc tér 11</strong>), then <strong>3 bars and a nightclub</strong>. The listed route runs through <strong>Doboz, La Siesta, Badabing, Füge Udvar, Place Bár</strong> and <strong>Instant</strong>, with <strong>fast-track VIP entry at Instant-Fogas</strong>.</p>
<p>At <strong>€19</strong> it costs more than the €2 crawls, and on paper you get a similar package: free shots, drinking games and <strong>entrance fees</strong>. The "Eat" in its name is a food stop where you buy your own. Where it earns its price is the meeting point: on a cold night, waiting in an Irish pub beats waiting on Erzsébet körút.</p>
<p><strong>For groups:</strong> the same team runs a <a href="{PRIVATE_OEI}" {REL} target="_blank">private pub crawl with VIP entry</a> (3 hours, shots, entrance fees, 4 bars and clubs). On Friday 20 November 2026 it was <strong>€100 for a group of up to 12</strong>, which beats most per-person prices once you're 6 or more. On 31 December there's a <strong>New Year's Eve crawl with a 1-hour open bar</strong>.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> if you're a group of friends or a couple who want a crawl with a fixed plan and a warm place to meet, or you're 6 to 12 people and want the private version.</p>
<p><strong>Skip it</strong> if price decides: <a href="#item-1-ruin-bar-pub-crawl">#1</a> gives you more venues for €2 on most nights.</p>
<h3>Meeting Point</h3>
<p>🗺️ <strong>Meeting Point: </strong>Becketts Irish Bar &amp; Restaurant, Liszt Ferenc tér 11, 1061 Budapest (New Year's Eve: Klauzál utca 10).<br/>🚇 <strong>Public Transport:</strong> M1 to Oktogon, or tram 4 or 6 to Oktogon, then 3 minutes on foot.</p>""",
        qf_badge="Liszt Ferenc tér (District VI)",
        qf=[("Duration", "5 Hours"), ("Price", "From €19 / person"),
            ("Start Time", "21:30"),
            ("Meeting Point", "Becketts Irish Bar, Liszt Ferenc tér 11, 1061 Budapest"),
            ("Venues", "3 bars and a nightclub (Instant-Fogas VIP)"),
            ("Included", "Free shots, entrance fees, drinking games, fast-track club entry"),
            ("Not Included", "Food and drinks, hotel pickup"),
            ("Private Version", "€100 per group of up to 12 (Fri 20 Nov 2026), 3 hours"),
            ("Age", "18 to 70, bring ID (a copy is accepted)")],
        chips=[("yes", "✓ Meets in a Pub"), ("yes", "✓ Entrance Fees Included"), ("yes", "✓ Private Group Option"),
               ("no", "✕ Food Not Included"), ("no", "✕ Over-70s")],
        perks=["Start: <strong>21:30</strong>", "Meet: <strong>Becketts Irish Bar</strong>"],
        desc="Classic ruin bar crawl from an Irish pub on Liszt Ferenc tér, with entrance fees and VIP club entry.",
    ),
    dict(
        n=5, anchor="item-5-hidden-bars-cocktail-crawl", rank="#5 Best Drinks Included",
        operator="Budapest Uncovered Tours", short_op="Budapest Uncovered",
        title="Hidden Bars and Cocktails Pub Crawl with Games",
        slug="budapest-hidden-bars-and-cocktails-pub-crawl-with-games-t1527002", cmp="pub-crawls-uncovered",
        score=None, count=None, count_exact=0, rating=None, price=25, price_txt="From €25",
        dur="3 Hours", dur_short="3 hours", place="Szervita tér", map="Szervita+tér+8+Budapest",
        cats="p10 drinks early", photos="uncovered", nphotos=6,
        alts=["Guests toasting with Hungarian drinks on a Budapest street",
              "Friends sharing drinks at a hidden Budapest bar",
              "Cheers with pálinka in a Budapest book bar",
              "Group with drinks in a vinyl-record bar",
              "Glasses raised in a toast on the cocktail crawl",
              "Night street toast on the hidden bars crawl"],
        specs=[("🍸", "Cocktail Crawl", "Hidden pubs and underground bars,", "with stories about Budapest's quirkier history between stops.", "Ends at a ruin bar on Klauzál utca."),
              ("⏱", "3 Hours", "20:00 to around 23:00.", "Early enough to keep going, or to be up for a morning tour.", "Fri 20 Nov 2026: €24.67."),
              ("🥂", "5 Drinks Included", "Pálinka, a tour cocktail, fröccs or beer, and 2 shots.", "The cocktail uses Hungarian ingredients and was made for this tour.", "Extra drinks are at your own cost."),
              ("📍", "Szervita tér Start", "Meet at Szervita tér 8", "(District V), 3 minutes from Deák Ferenc tér.", "Finish: Klauzál utca 25, District VII.")],
        best_for="Couples and anyone past the shots-and-club stage: five real drinks, hidden bars and city stories, done by 23:00.",
        pros=["5 drinks included: pálinka, a cocktail made for the tour, fröccs or beer, and 2 more shots",
              "Starts at 20:00, ends around 23:00 at a ruin bar on Klauzál utca",
              "A local guide with Budapest drinking history and stories between stops"],
        cons=["A new tour, so no guest reviews yet",
              "No club at the end",
              "Not for over-65s or wheelchair users, per the operator"],
        body="""<p>This is the one crawl here where the ticket price is mostly drinks. For <strong>€25</strong> you get <strong>five</strong>: a welcome <strong>pálinka</strong>, an <strong>original cocktail</strong> made for the tour with Hungarian ingredients, a <strong>fröccs</strong> (wine spritzer) or a beer, and <strong>two more shots</strong>. On a €2 crawl you'd be buying all of that at the bar.</p>
<p>The route is the opposite of the big party crawls: <strong>hidden pubs and underground bars</strong> in the city centre, stories about the stranger corners of Budapest's history between stops, a few drinking games, and a finish at a <strong>ruin bar on Klauzál utca</strong>. It starts at <strong>20:00</strong> and takes <strong>3 hours</strong>, so you're free by 23:00 to go to bed or keep going.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> if you're a couple or a small group who want to taste Hungarian drinks rather than chase shots, or you want a night out that leaves you fine for a morning tour.</p>
<p><strong>Skip it</strong> if the club is the point: there isn't one. Book <a href="#item-1-ruin-bar-pub-crawl">#1</a> or <a href="#item-3-late-start-pub-crawl">#3</a> instead.</p>
<h3>Meeting Point</h3>
<p>🗺️ <strong>Meeting Point: </strong>Szervita tér 8, 1052 Budapest (District V). <strong>Ends:</strong> Klauzál utca 25, 1072 Budapest.<br/>🚇 <strong>Public Transport:</strong> M1, M2 or M3 to Deák Ferenc tér, then 3 minutes on foot.</p>""",
        qf_badge="City Centre to District VII",
        qf=[("Duration", "3 Hours"), ("Price", "From €25 / person (€24.67 on Fri 20 Nov 2026)"),
            ("Start Time", "20:00"),
            ("Meeting Point", "Szervita tér 8, 1052 Budapest"),
            ("Finish", "Ruin bar at Klauzál utca 25, 1072 Budapest"),
            ("Drinks Included", "5: pálinka, tour cocktail, fröccs or beer, 2 shots"),
            ("Not Included", "Extra drinks, food"),
            ("Languages", "English, Hungarian"),
            ("Age", "18 to 65, bring photo ID")],
        chips=[("yes", "✓ 5 Drinks Included"), ("yes", "✓ Done by 23:00"), ("yes", "✓ Hidden Bars"),
               ("no", "✕ No Club"), ("no", "✕ Not Wheelchair Accessible")],
        perks=["Start: <strong>20:00</strong>", "Drinks: <strong>5 Included</strong>"],
        desc="3-hour hidden bars and cocktails crawl with 5 drinks included, from 20:00.",
    ),
    dict(
        n=6, anchor="item-6-private-stag-pub-crawl", rank="#6 Best for Stag Groups",
        operator="Hullar Holding", short_op="Hullar Holding",
        title="Private Pub Crawl with Shots and Club Entry",
        slug="budapest-private-pub-crawl-with-shots-and-club-entry-t1314203", cmp="pub-crawls-private",
        score=None, count=None, count_exact=0, rating=None, price=27, price_txt="From €27",
        dur="4 Hours", dur_short="4 hours", place="Pickup", map=None,
        cats="p10 private", photos="private", nphotos=6,
        alts=["Private pub crawl group at a Budapest bar table",
              "Stag group holding shots on a private Budapest crawl",
              "Private crawl group in a Budapest beer bar",
              "Group of friends under a bar terrace at night",
              "Guest drinking a shot under neon lights",
              "Hen group posing in a Budapest bar"],
        specs=[("🔒", "Private Crawl", "Only your group", "and a local guide, through 3-4 pubs and bars.", "The route is adapted to your group's vibe."),
              ("⏱", "4 Hours", "4 hours,", "start time set when you book.", "Ends with entry to a nightclub or a strip club."),
              ("👥", "Min. 8 People", "From €27 per person,", "so at least €216 for the group.", "Not bookable for fewer than 8."),
              ("🚐", "Pickup Included", "Pickup in a set pickup area,", "confirmed when you book.", "Other transport is not included.")],
        best_for="Stag and hen groups of 8 or more: your own guide, pickup, 4 rounds of shots, then a nightclub or a strip club.",
        pros=["Only your group, with pickup included",
              "4 rounds of party shots across 3-4 pubs and bars",
              "Ends with entry to a top nightclub or a strip club, your call"],
        cons=["Minimum 8 people",
              "A new tour, so no guest reviews yet",
              "Your group pays any noise or street fine it causes"],
        body="""<p>Big shared crawls are great for meeting strangers and useless for a stag do. This one is <strong>private</strong>: a local guide <strong>picks your group up</strong>, takes you through <strong>3 to 4 pubs and bars</strong> (ruin bars, party venues and local spots, adapted to your group), pours <strong>4 rounds of party shots</strong>, and finishes with <strong>entry to a top nightclub or a strip club</strong>.</p>
<p>It costs <strong>from €27 per person</strong> with a <strong>minimum of 8</strong>, and runs <strong>4 hours</strong>. The house rules are stricter than most: drinking on the street, public urination and noise can mean <strong>fines of up to €400</strong>, and if the operator is fined because of your group, your group pays it.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> for a stag, hen or birthday group of 8+ that wants its own guide and pickup, not 40 strangers.</p>
<p><strong>Skip it</strong> if you're fewer than 8, or you just want a private version of a normal crawl: the <a href="#item-4-irish-pub-start-crawl">#4 private option</a> was €100 for a whole group of up to 12 on the Friday we checked.</p>
<h3>Meeting Point</h3>
<p>🗺️ <strong>Pickup: </strong>included in a pickup area, confirmed when you book.<br/>🕒 <strong>Start time:</strong> set when you book.</p>""",
        qf_badge="Private, pickup included",
        qf=[("Duration", "4 Hours"), ("Price", "From €27 / person"),
            ("Group", "Private, minimum 8 people"),
            ("Pickup", "Included (pickup area confirmed on booking)"),
            ("Venues", "3 to 4 pubs and bars, then a nightclub or strip club"),
            ("Included", "4 rounds of party shots, club entry, local guide"),
            ("Not Included", "Transport, food"),
            ("Age", "18+, bring ID (a copy is accepted)")],
        chips=[("yes", "✓ Private Group"), ("yes", "✓ Pickup Included"), ("yes", "✓ 4 Rounds of Shots"),
               ("no", "✕ Minimum 8 People")],
        perks=["Group: <strong>Private, 8+</strong>", "Duration: <strong>4 Hours</strong>"],
        desc="Private stag and hen pub crawl with pickup, 4 rounds of shots and nightclub or strip club entry.",
    ),
]

FILTERS = """<div class="ltt-integrated-filter-bar smart-filter-bar">
<div class="ltt-integrated-pills">
<button class="ltt-tab-btn active" data-cat="all" data-label="All" onclick="lttFilterItems('all', this)" type="button">All <span class="ltt-cnt"></span></button>
<span class="ltt-filter-label sf-fl">Price:</span>
<button class="ltt-tab-btn" data-cat="u10" data-group="price" data-label="Under €10" onclick="lttFilterItems('u10', this)" type="button">Under €10 <span class="ltt-cnt"></span></button>
<button class="ltt-tab-btn" data-cat="p10" data-group="price" data-label="€10+" onclick="lttFilterItems('p10', this)" type="button">€10+ <span class="ltt-cnt"></span></button>
<span class="ltt-filter-label sf-fl">Night:</span>
<button class="ltt-tab-btn" data-cat="party" data-group="style" data-label="Bars + club" onclick="lttFilterItems('party', this)" type="button">Bars + club <span class="ltt-cnt"></span></button>
<button class="ltt-tab-btn" data-cat="drinks" data-group="style" data-label="Drinks included" onclick="lttFilterItems('drinks', this)" type="button">Drinks included <span class="ltt-cnt"></span></button>
<button class="ltt-tab-btn" data-cat="private" data-group="style" data-label="Private group" onclick="lttFilterItems('private', this)" type="button">Private group <span class="ltt-cnt"></span></button>
<span class="ltt-filter-label sf-fl">Start:</span>
<button class="ltt-tab-btn" data-cat="late" data-group="start" data-label="22:00 or later" onclick="lttFilterItems('late', this)" type="button">22:00 or later <span class="ltt-cnt"></span></button>
<button class="ltt-tab-btn" data-cat="early" data-group="start" data-label="By 20:00" onclick="lttFilterItems('early', this)" type="button">By 20:00 <span class="ltt-cnt"></span></button>
</div>
</div>"""

LEAD = f"""<div class="ltt-lead-copy">
<p>Every big Budapest pub crawl costs about <strong>€2</strong>, and that is the least useful number on the listing. What decides your night is <strong>what's actually free after the welcome shot</strong>, when it starts, how late it ends, and whether the bar you came for is even on the route: <strong>Szimpla Kert isn't named on the venue lists of the four biggest crawls</strong>.</p>
<p>Below are the 6 worth booking side by side, from the €2 party crawls to a <strong>€25 crawl with 5 drinks included</strong> and a private stag night, plus a free route if you'd rather do the ruin bars yourself. Prices, start times and meeting points checked on {CHECKED}.</p>
</div>"""

GUIDE = f"""<div class="w-richtext bpa-wt-guide">
<style>.bpa-pc-table-wrap{{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:8px 0 24px;border:1px solid #e2e8f0;border-radius:10px}}.bpa-pc-table{{width:100%;min-width:640px;border-collapse:collapse;font-size:14px;line-height:1.45}}.bpa-pc-table th{{background:#f8fafc;text-align:left;font-weight:700;color:#0f172a;border-bottom:2px solid #e2e8f0;padding:10px 12px}}.bpa-pc-table td{{border-bottom:1px solid #f1f5f9;padding:10px 12px;color:#334155;vertical-align:top}}.bpa-pc-table tr:last-child td{{border-bottom:0}}.bpa-pc-table caption{{caption-side:bottom;text-align:left;font-size:13px;color:#64748b;padding:8px 12px}}</style>
<h2 id="which-pub-crawl">Which Budapest Pub Crawl Should You Book?</h2>
<ul>
<li><strong>Solo, first night, want the biggest party:</strong> <a href="#item-1-ruin-bar-pub-crawl">Pub Crawl &amp; Ruin Bar Tour</a> (from €2, 4-5 venues, a shot at each).</li>
<li><strong>Booking on reviews alone:</strong> <a href="#item-2-highest-rated-pub-crawl">Ruin Bars Pub Crawl</a> (from €2.18, rated 5.0 from 1,657 reviews).</li>
<li><strong>Dinner first, crawl later:</strong> <a href="#item-3-late-start-pub-crawl">Party Deck</a> (22:00 start, 5-6 venues).</li>
<li><strong>Want to meet in a pub, not on a corner:</strong> <a href="#item-4-irish-pub-start-crawl">Original Europe Tours</a> (€19, Becketts Irish Bar, 21:30).</li>
<li><strong>Good drinks over cheap shots:</strong> <a href="#item-5-hidden-bars-cocktail-crawl">Hidden Bars and Cocktails crawl</a> (€25, 5 drinks included, 20:00 to 23:00).</li>
<li><strong>Stag or hen group of 8+:</strong> <a href="#item-6-private-stag-pub-crawl">Private pub crawl with pickup</a> (from €27 per person).</li>
<li><strong>Group of 6 to 12, normal night out:</strong> the <a href="#item-4-irish-pub-start-crawl">private version of #4</a> (€100 for the whole group on the Friday we checked).</li>
</ul>
<h2 id="what-2-euros-buys">What a €2 Ticket Really Covers (and What €25 Adds)</h2>
<p>The €2 crawls aren't a trick, but read them as <strong>a guide, a group and a queue-skip</strong>, not a drinks package. Across #1 to #3, the price covers a <strong>welcome shot</strong> (at every venue on #1, at the first bar and the club on #2), drinking games, photos and <strong>VIP fast-track entry at the club</strong>, usually Instant-Fogas. Every beer, cocktail and glass of wine after that is <strong>bought at the bar</strong>. Food is never included.</p>
<p>The €2 price also moves by date. On <strong>Friday 20 November 2026</strong>, #1 was <strong>€8.50</strong>, #2 was €2.18 or €4 depending on the start time, and #3 was €2 or €6. Still cheap, but check your own date before you plan around €2.</p>
<p>At <strong>€25</strong>, the <a href="#item-5-hidden-bars-cocktail-crawl">hidden bars crawl</a> flips the deal: <strong>5 drinks are included</strong> (pálinka, a tour cocktail, fröccs or beer, two shots), but there's no club and it ends at 23:00. If you'd drink four or five rounds anyway, that's where the €23 difference goes.</p>
<div class="bpa-pc-table-wrap"><table class="bpa-pc-table">
<caption>Prices are the lowest adult price, with a Friday 20 November 2026 sample. Checked {CHECKED}.</caption>
<thead><tr><th>Crawl</th><th>Price</th><th>Starts</th><th>Ends around</th><th>Free drinks</th><th>Club entry</th><th>Meet at</th></tr></thead>
<tbody>
<tr><td><a href="#item-1-ruin-bar-pub-crawl">#1 RuinBarCrawl</a></td><td>From €2 (Fri €8.50)</td><td>21:10, 21:40, 22:20</td><td>02:10 to 03:20</td><td>Shot at every venue</td><td>VIP, 4 venues</td><td>Erzsébet körút 36</td></tr>
<tr><td><a href="#item-2-highest-rated-pub-crawl">#2 Budapest Nightlife Tours</a></td><td>From €2.18 (Fri €2.18 to €4)</td><td>21:00, 21:30, 22:00</td><td>02:30 to 03:30</td><td>Welcome shot, shots at the club</td><td>VIP</td><td>Erzsébet körút 19</td></tr>
<tr><td><a href="#item-3-late-start-pub-crawl">#3 Party Deck</a></td><td>From €2 (Fri €2 to €6)</td><td>21:00 or 22:00</td><td>03:00</td><td>Tequila, vodka, pálinka shots</td><td>VIP Instant-Fogas</td><td>Dohány utca 35</td></tr>
<tr><td><a href="#item-4-irish-pub-start-crawl">#4 Original Europe Tours</a></td><td>From €19</td><td>21:30</td><td>02:30</td><td>Free shots</td><td>Fast-track, entrance fees incl.</td><td>Liszt Ferenc tér 11</td></tr>
<tr><td><a href="#item-5-hidden-bars-cocktail-crawl">#5 Budapest Uncovered</a></td><td>From €25</td><td>20:00</td><td>23:00</td><td>5 drinks incl. a cocktail</td><td>None, ends at a ruin bar</td><td>Szervita tér 8</td></tr>
<tr><td><a href="#item-6-private-stag-pub-crawl">#6 Private crawl</a></td><td>From €27 pp (min. 8)</td><td>Your booking</td><td>4 hours later</td><td>4 rounds of shots</td><td>Nightclub or strip club</td><td>Pickup</td></tr>
</tbody></table></div>
<h2 id="which-ruin-bars">Which Ruin Bars and Clubs Are on the Route?</h2>
<p>Routes rotate with opening hours and crowds, but the venue lists overlap heavily. <strong>Instant-Fogas</strong>, the huge multi-room ruin club on Akácfa utca, gets VIP entry on #1, #3 and #4, and #2 ends at Instant too. <strong>Füge Udvar, La Siesta, Doboz</strong> and <strong>Humbák</strong> show up on almost every list.</p>
<p><strong>Szimpla Kert</strong>, the ruin bar on every postcard, is on none of the venue lists for #1 to #4. It's free to walk into, so the easy fix is to go there first, around 20:00 when you can still move, then join a 21:30 or 22:00 crawl a few streets away.</p>
<h2 id="free-ruin-bar-route">Free Self-Guided Ruin Bar Route vs a Paid Crawl</h2>
<p>You don't need a tour to see the ruin bars: the best ones sit within a 10-minute walk of each other in District VII. A simple free route: <strong>Szimpla Kert</strong> (Kazinczy utca 14) for the famous courtyards, then <strong>Doboz</strong> (Klauzál utca 10), and finish at <strong>Instant-Fogas</strong> (Akácfa utca 49-51) if you want to dance.</p>
<p>Hungry first? The Jewish Quarter tour in our <a href="/best-food-tours-budapest">best food tours in Budapest</a> ends on Kazinczy utca, the same street as Szimpla, so dinner and the first ruin bar are a two-minute walk apart.</p>
<p><strong>Go self-guided</strong> if you're a couple who wants to look around, have two drinks and be in bed by midnight. <strong>Book a crawl</strong> if you're solo, want a group to go out with, or it's a Friday or Saturday and you'd rather skip the club queue: at €2, the ticket costs less than a beer in Szimpla.</p>
<p>Making a whole evening of it? Start on the river with an <a href="/unlimited-prosecco-cruises-budapest">unlimited prosecco cruise</a> or one of the <a href="/best-night-cruises-budapest">best night cruises</a>, then walk 15 minutes into District VII for a 21:30 or 22:00 crawl.</p>
<h2 id="same-crawl-two-listings">Same Crawl, Two Listings: What We Left Out</h2>
<p>Several Budapest crawls are sold more than once under different names. <strong>Ruin Bar Crawl, Karaoke, Free Shots &amp; VIP Entry</strong> shares #1's meeting point (Erzsébet körút 36), its 21:10 and 22:20 start times, its venues and even the guides named in reviews. <strong>Pub Crawl &amp; Ruin Bar Tour with 6 Shots</strong> and <strong>Social Ruin Pub Tour</strong> start from #3's meeting point at JO&amp;JOE with the same house rules. We kept the listing with the most reviews for each; if a twin is cheaper on your date, it's the same night out.</p>
<h2 id="before-you-go">Before You Go: Rules, ID and Getting Home</h2>
<ul>
<li><strong>18+ only, bring ID.</strong> Every crawl here asks for a passport or ID card; most accept a photo copy.</li>
<li><strong>No drinking on the street.</strong> Drinking outside, shouting or public urination can mean <strong>fines of up to €400</strong>. Crawls keep it inside the bars.</li>
<li><strong>Arrive sober-ish.</strong> Party Deck turns away anyone visibly drunk at check-in, and the others ban intoxication too.</li>
<li><strong>Pay at the bar.</strong> Beyond what's listed as included, you buy your own drinks, so carry a card or some forint.</li>
<li><strong>Getting home:</strong> tram 6 runs all night along the Grand Boulevard (Erzsébet körút), a few minutes' walk from every finish.</li>
</ul>
<p>Staying near the bars? Our pick of the <a href="/best-hostels-budapest">best hostels in Budapest</a> lists the social ones that run their own nights out. For daytime plans, see the <a href="/best-things-to-do-budapest">best things to do in Budapest</a>, or the free Jewish Quarter walk in our <a href="/best-walking-tours-budapest">best walking tours</a> to see the same streets by day.</p>
</div>"""

FAQ = [
    ("How much does a pub crawl in Budapest cost?",
     "The big party crawls start at about <strong>€2</strong> (€2 to €8.50 on a Friday), which covers the guide, shots, games and VIP club entry. "
     "A crawl with <strong>5 drinks included</strong> costs about <strong>€25</strong>, and a private stag crawl starts at €27 per person for 8 or more."),
    ("What is included in a €2 pub crawl in Budapest?",
     "A guide, a welcome shot (on some crawls one at every venue), drinking games, photos and <strong>fast-track entry to the club</strong> at the end, "
     "usually Instant-Fogas. Every other drink and all food you pay for at the bar."),
    ("What time do Budapest pub crawls start and finish?",
     "Most start between <strong>21:00 and 22:20</strong> and run 5 to 6 hours, so the organised part ends around <strong>02:00 to 03:30</strong> in a club you can stay in. "
     "The hidden bars and cocktails crawl starts at 20:00 and ends around 23:00."),
    ("Do Budapest pub crawls go to Szimpla Kert?",
     "Not usually. Szimpla Kert isn't on the venue lists of the four biggest crawls, which favour Instant-Fogas, Füge Udvar, La Siesta, Doboz and Humbák. "
     "Szimpla is free to enter, so visit it first and join a crawl afterwards."),
    ("Are pub crawls in Budapest good for solo travellers?",
     "Yes, that's who they're built for. The €2 crawls start with icebreakers and drinking games at the first bar, and reviewers who came alone write about the friends they made."),
    ("Is there an age limit on Budapest pub crawls?",
     "All of them are <strong>18+</strong> and ask for ID (most accept a copy). Two set upper limits too: the Liszt Ferenc tér crawl is for under-70s and the hidden bars crawl for under-65s."),
    ("Can I visit the ruin bars without a tour?",
     "Yes. Szimpla Kert (Kazinczy utca 14), Doboz (Klauzál utca 10) and Instant-Fogas (Akácfa utca 49-51) are all within a 10-minute walk in District VII. "
     "A crawl mainly adds a group, shots and a skip-the-queue entry at the club on busy nights."),
    ("Which Budapest pub crawl is best for a stag or hen party?",
     "For 8 or more, the <strong>private pub crawl with pickup</strong> (from €27 per person, 4 rounds of shots, nightclub or strip club entry). "
     "For 6 to 12 who want a normal crawl to themselves, the private version from Liszt Ferenc tér was €100 per group on the Friday we checked."),
    ("Is there a New Year's Eve pub crawl in Budapest?",
     "Yes. Party Deck runs a NYE night with 2 hours of unlimited drinks and VIP entry at Instant-Fogas, and the Liszt Ferenc tér crawl adds a 1-hour open bar on 31 December. "
     "Prefer the fireworks from the river? See our <a href=\"/new-years-eve-cruises-budapest\">New Year's Eve cruises in Budapest</a>."),
]

METHOD = f"""<h2 id="how-we-compared">How We Compared These Pub Crawls</h2>
<p>Compared on {CHECKED} using the live listings of Budapest's most-booked pub crawls and ruin bar tours. For each one we recorded the lowest adult price and a sample Friday (20 November 2026), every start time, the meeting point, the venue list, what is and isn't included, age limits and group options. Ratings and review counts are as shown on each listing on that date. Where two listings turned out to be the same crawl, we kept the one with more reviews. Prices change by date and season, so check yours before you book.</p>"""


def esc_attr(x):
    return x.replace('"', "&quot;")


def stars_html(s, score):
    ref = "4.9" if float(score) >= 4.75 else "4.6"
    return re.search(r'<span class="bpa-rev-score">' + re.escape(ref) + r'</span>(<span class="bpa-rev-stars">.*?</span>)', s, re.S).group(1)


def gyg_icon(s):
    return re.search(r'<img alt="" class="bpa-rev-icon" loading="lazy" src="(data:image/png;base64,[^"]+)"/><span class="bpa-rev-score">4.4', s).group(1)


def badge(t, s, link=True):
    href = GYG.format(slug=t["slug"], cmp=t["cmp"])
    inner = f'<img alt="" class="bpa-rev-icon" loading="lazy" src="{gyg_icon(s)}"/>'
    if t["score"]:
        inner += f'<span class="bpa-rev-score">{t["score"]}</span>{stars_html(s, t["score"])}<span class="bpa-rev-count">(+{t["count"]} reviews)</span>'
    else:
        inner += '<span class="bpa-rev-count">New tour for 2026</span>'
    if link:
        return f'<a class="bpa-rev-badge" href="{href}" onclick="event.stopPropagation()" rel="noopener nofollow sponsored" target="_blank">{inner}</a>'
    return f'<span class="bpa-rev-badge">{inner}</span>'


def photos(t):
    return [f'{IMG}/{t["photos"]}-{k:02d}.webp' for k in range(1, t["nphotos"] + 1)]


def tag(t):
    return f'<span class="bpa-rank-tag {"bpa-gold" if t.get("gold") else "bpa-slate"}">{t["rank"]}</span>'


def deck_card(t, s):
    href = GYG.format(slug=t["slug"], cmp=t["cmp"])
    ph = photos(t)
    sizes = 'sizes="(max-width: 767px) 420px, (max-width: 991px) 55vw, (max-width: 1439px) 49vw, 50vw"'
    first = 'fetchpriority="high" loading="eager"' if t["n"] == 1 else 'loading="lazy"'
    imgs = [f'<img alt="{t["alts"][0]}" {first} height="534" {sizes} src="{ph[0]}" width="800"/>']
    blank = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 500'%3E%3C/svg%3E"
    for p, a in zip(ph[1:], t["alts"][1:]):
        imgs.append(f'<img alt="{a}" data-src="{p}" decoding="async" loading="lazy" {sizes} src="{blank}"/>')
    specs = "\n".join(
        f'<details class="bpa-lang"><summary class="bpa-sp">{e} <span class="bpa-lang-label">{lab}</span>'
        f'<span class="bpa-lang-chev" aria-hidden="true">▾</span></summary><div class="bpa-lang-pop"><strong>{lead}</strong> {txt}'
        f'<span class="bpa-lang-note">{note}</span></div></details>'
        for e, lab, lead, txt, note in t["specs"])
    place = (t["place"] if not t["map"] else
             f'<a class="bpa-kicker-map-link" href="https://www.google.com/maps/search/?api=1&amp;query={t["map"]}" onclick="event.stopPropagation()" rel="noopener noreferrer" target="_blank">{t["place"]}</a>')
    return f"""<!-- #{t['n']}: {t['title']} -->
<div class="bpa-card" data-cat="{t['cats']}" id="card-{t['n']}">
<div class="bpa-main">
<div class="bpa-media">
{tag(t)}
<button aria-label="Previous photo" class="bpa-arrow prev" onclick="bpaSlide(this,-1)" type="button">‹</button>
<button aria-label="Next photo" class="bpa-arrow next" onclick="bpaSlide(this,1)" type="button">›</button>
<span class="bpa-pill">1 / {len(ph)}</span>
<div aria-label="Photo gallery {t['n']}" class="bpa-slider" onscroll="bpaCount(this)" tabindex="0">
{chr(10).join(imgs)}
</div>
</div>
<div class="bpa-info">
<div class="bpa-kicker">{t['short_op']} • ⏱️ {t['dur']} • {place}</div>
<a class="bpa-title" href="{href}" {REL} target="_blank">{t['title']}</a>
<div class="bpa-reviews-line">
<div class="bpa-summary-reviews"><div class="div-block-53">{badge(t, s)}</div></div>
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
<a class="bpa-btn" href="{href}" {REL} target="_blank">Check Availability →</a>
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
    ph = photos(t)
    pros = "".join(f"<li><strong>{x}</strong></li>" for x in t["pros"])
    cons = "".join(f"<li><strong>{x}</strong></li>" for x in t["cons"])
    slides = "".join(
        f'<div class="ltt-strip-slide"><img alt="{a}" loading="lazy" src="{p}"/><div class="ltt-strip-cap">'
        f'<span class="ltt-strip-num">{i} / {len(ph)}</span> <span>{a}</span></div></div>'
        for i, (p, a) in enumerate(zip(ph, t["alts"]), 1))
    perks = "\n".join(f'<span class="ltt-buy-perk">{x}</span>' for x in
                      ["Instant Smartphone QR Voucher", "Full Refund up to 24h Before"] + t["perks"])
    qf = "\n".join(f'<div class="qf1-row"><div class="qf1-label">{a}</div><div class="qf1-val">{b}</div></div>' for a, b in t["qf"])
    chips = "\n".join(f'<span class="qf1-chip {c}">{x}</span>' for c, x in t["chips"])
    return f"""<details class="bpa-details-card" data-cat="{t['cats']}" id="{t['anchor']}" open="">
<summary class="bpa-details-summary">
<div class="bpa-details-summary-content">
<div class="bpa-details-top-row">
{tag(t)}
<div class="bpa-kicker">{t['short_op']} • ⏱️ {t['dur']} • <span class="bpa-kicker-map-link">{t['place']}</span></div>
</div>
<h3 class="bpa-details-title">{t['title']}</h3>
<div class="bpa-reviews-line">
<div class="bpa-summary-reviews"><div class="div-block-53">{badge(t, s, link=False)}</div></div>
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
<span>Free Cancellation • Instant Confirmation</span>
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


def faq_html():
    qs = "".join(f'<h3 class="cf-faq-questions-2">{q}</h3><div class="cf-faq-answer-wrap-2"><div class="cf-faq-content-2 w-richtext"><p>{a}</p></div></div>'
                 for q, a in FAQ)
    return f'<div class="w-richtext bpa-wt-faq"><h2 id="faq-dup2">Frequently Asked Questions</h2>{qs}{METHOD}</div>'


def strip_tags(x):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", x)).replace("&amp;", "&").strip()


def jsonld():
    items = []
    for t in CRAWLS:
        prod = {"@type": "Product", "name": strip_tags(t["title"]), "description": t["desc"],
                "brand": {"@type": "Organization", "name": t["operator"]},
                "image": [f"{SITE}{photos(t)[0]}"],
                "offers": {"@type": "Offer", "price": str(t["price"]), "priceCurrency": "EUR",
                           "availability": "https://schema.org/InStock",
                           "url": GYG.format(slug=t["slug"], cmp=t["cmp"]).replace("&amp;", "&")}}
        if t["score"]:
            prod["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": t["score"], "bestRating": "5",
                                       "worstRating": "1", "reviewCount": str(t["count_exact"])}
        items.append({"@type": "ListItem", "position": t["n"], "url": f"{URL}#{t['anchor']}", "item": prod})
    graph = [
        {"@type": "Article", "@id": f"{URL}#article", "headline": H1_PLAIN, "description": DESC,
         "image": [f"{SITE}{photos(CRAWLS[0])[0]}"], "datePublished": "2026-11-15", "dateModified": "2026-11-15",
         "inLanguage": "en",
         "author": {"@type": "Person", "name": "Adam Dimitrov", "url": f"{SITE}/about"},
         "publisher": {"@type": "Organization", "name": "Budapest Adventures", "url": SITE,
                       "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/budapest-adventures-logo.png"}},
         "mainEntityOfPage": URL,
         "mainEntity": {"@type": "ItemList", "name": H1_PLAIN, "numberOfItems": len(CRAWLS), "itemListElement": items}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Things to Do", "item": f"{SITE}/best-things-to-do-budapest"},
            {"@type": "ListItem", "position": 3, "name": H1_PLAIN, "item": URL}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q,
                                             "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in FAQ]},
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))


def cut(s, start, end, new, start_after=0):
    a = s.find(start, start_after)
    assert a >= 0, start[:60]
    b = s.find(end, a)
    assert b >= 0, end[:60]
    return s[:a] + new + s[b:], a


def main():
    s = TEMPLATE.read_text()
    lock = re.search(r'<div class="ltt-buy-card-trust">\s*(<svg.*?</svg>)', s, re.S).group(1)
    star_src = s  # star/icon markup lookups

    # --- head ---
    s = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", s, count=1)
    old_desc = re.search(r'<meta content="([^"]*)" name="description"/>', s).group(1)
    assert s.count(f'content="{old_desc}"') == 3
    s = s.replace(f'content="{old_desc}"', f'content="{esc_attr(DESC)}"')
    old_title = re.search(r'<meta content="([^"]*)" property="og:title"/>', s).group(1)
    s = s.replace(f'content="{old_title}"', f'content="{esc_attr(TITLE)}"')
    og = f"{SITE}{photos(CRAWLS[0])[0]}"
    s = re.sub(r'<meta content="[^"]*" property="og:image"/>', f'<meta content="{og}" property="og:image"/>', s)
    s = re.sub(r'<meta content="[^"]*" property="twitter:image"/>', f'<meta content="{og}" property="twitter:image"/>', s)
    s = re.sub(r'<meta content="[^"]*" name="twitter:image"/>', f'<meta content="{og}" name="twitter:image"/>', s)
    s = re.sub(r'<link as="image" fetchpriority="high" href="[^"]*" rel="preload" type="image/webp"/>',
               f'<link as="image" fetchpriority="high" href="{photos(CRAWLS[0])[0]}" rel="preload" type="image/webp"/>', s, count=1)
    s = re.sub(r'<link href="[^"]*" hreflang="[^"]*" rel="alternate"/>', "", s)
    s = re.sub(r'<link href="[^"]*" rel="canonical"/>',
               f'<link href="{URL}" rel="canonical"/><link href="{URL}" hreflang="en" rel="alternate"/>'
               f'<link href="{URL}" hreflang="x-default" rel="alternate"/>', s, count=1)
    s = re.sub(r'<meta content="https://www\.budapestadventures\.com/best-walking-tours-budapest" property="og:url"/>',
               f'<meta content="{URL}" property="og:url"/>', s)

    # --- hero ---
    s = re.sub(r'<span class="ltt-bc-current">.*?</span>', f'<span class="ltt-bc-current">{H1_PLAIN}</span>', s, count=1)
    s = s.replace('<span class="ltt-hero-kicker-badge">2026 Field-Tested Comparison</span>',
                  '<span class="ltt-hero-kicker-badge">2026 Side-by-Side Comparison</span>')
    s = re.sub(r'(<h1 class="ltt-editorial-h1">).*?(</h1>)', lambda m: f"{m.group(1)}\n      {H1}\n{m.group(2)}", s, count=1, flags=re.S)
    s = s.replace("Founder &amp; Local Budapest Tester", "Founder, Budapest Adventures")
    s = s.replace('<div class="ltt-author-role">Personally Field-Tested • Original Photos &amp; Videos</div>',
                  '<div class="ltt-author-role">Budapest Local • Prices and Start Times Checked</div>')
    s = re.sub(r"<strong>Last updated</strong>: [A-Za-z]{3} \d+, 2026", f"<strong>Last updated</strong>: {CHECKED_SHORT}", s, count=1)
    s, _ = cut(s, '<div class="ltt-lead-copy">', '<div class="ltt-integrated-filter-bar smart-filter-bar">', LEAD + "\n")
    a = s.find('<div class="ltt-integrated-filter-bar smart-filter-bar">')
    b = s.find("</div>\n</div>", a) + len("</div>\n</div>")
    s = s[:a] + FILTERS + s[b:]

    # --- deck ---
    s = s.replace('id="budapest-walking-tours-deck"', 'id="budapest-pub-crawls-deck"')
    a = s.find('<div class="bpa-deck-wrap" id="ltt-cards-deck">') + len('<div class="bpa-deck-wrap" id="ltt-cards-deck">\n')
    b = s.find('</div></div><div class="blog-section-2">', a)
    # deck ends with "</div>\n</div>\n" closing deck-wrap and deck container right before
    tail = "</div>\n</div>\n"
    b = s.rfind(tail, a, b)
    s = s[:a] + "".join(deck_card(t, star_src) for t in CRAWLS) + s[b:]

    # --- guide ---
    s, _ = cut(s, '<div class="w-richtext bpa-wt-guide">', '<div class="bpa-breakdown-top-bar" id="breakdown-header">', GUIDE + "\n\n")
    s = re.sub(r'(<h2 class="bpa-breakdown-heading" id="desert-safaris-breakdown">).*?(</h2>)',
               r"\1Detailed Breakdown: 6 Best Pub Crawls in Budapest\2", s, count=1)
    s = re.sub(r'<p class="bpa-breakdown-sub">.*?</p>',
               f'<p class="bpa-breakdown-sub">Compared on {CHECKED} • All reviews open by default • Click to collapse/expand</p>', s, count=1)

    # --- details + faq ---
    a = s.find('<details class="bpa-details-card"')
    b = s.find('<div class="w-richtext bpa-wt-faq">', a)
    c = s.find("\n</div>\n<style>.ltt-editorial-wrapper", b)
    assert a > 0 and b > a and c > b
    s = s[:a] + "".join(details(t, star_src, lock) for t in CRAWLS) + faq_html() + s[c:]

    # --- floating bars / runtime ---
    a = s.find('<script>\ndocument.addEventListener("DOMContentLoaded", () => {\n    const cruiseCards')
    b = s.find("</script>", a) + len("</script>")
    assert a > 0
    s = s[:a] + s[b:]
    first = CRAWLS[0]
    href1 = GYG.format(slug=first["slug"], cmp=first["cmp"])
    s = re.sub(r'(<span class="hybrid-active-title" id="hybridActiveTitle">).*?(</span>)', rf"\1{first['short_op']}\2", s)
    s = re.sub(r'(<span class="hybrid-active-price" id="hybridActivePrice">).*?(</span>)', rf"\1{first['price_txt']}\2", s)
    s = re.sub(r'(<a class="hybrid-cta-btn" href=")[^"]*(" id="hybridActiveCta")', lambda m: m.group(1) + href1 + m.group(2), s)
    s = re.sub(r'(<span class="hybrid-active-title" id="sticky-name">).*?(</span>)', lambda m: m.group(1) + first["title"] + m.group(2), s)
    s = re.sub(r'(<span class="hybrid-active-price" id="sticky-price">).*?(</span>)', rf"\1{first['price_txt']}\2", s)
    s = re.sub(r'(<a class="hybrid-cta-btn" href=")[^"]*(" id="sticky-cta-btn")', lambda m: m.group(1) + href1 + m.group(2), s)
    s = s.replace("<span>Contents (10)</span>", f"<span>Contents ({len(CRAWLS)})</span>")
    s = s.replace("<span>All 10 Walking Tours</span>", f"<span>All {len(CRAWLS)} Pub Crawls</span>")
    s = s.replace("Jump to Tested Walking Tour", "Jump to a Pub Crawl")
    s = s.replace('aria-label="Quick Cruise Navigation &amp; Booking"', 'aria-label="Quick Pub Crawl Navigation &amp; Booking"')
    s = s.replace('aria-label="Jump to Cruise Review"', 'aria-label="Jump to Pub Crawl Review"')
    cfg = {"deckId": "budapest-pub-crawls-deck", "tocDeckLabel": "Top 6 Pub Crawls",
           "tocBreakdownLabel": "Detailed Breakdown (6 Pub Crawls)", "shortTitles": [strip_tags(t["title"]) for t in CRAWLS]}
    s = re.sub(r"window\.LTT_PAGE_CONFIG = \{.*?\};", lambda m: "window.LTT_PAGE_CONFIG = " + json.dumps(cfg, ensure_ascii=False) + ";", s, count=1)

    # --- JSON-LD ---
    s = re.sub(r'(<script id="ltt-schema-jsonld" type="application/ld\+json">).*?(</script>)',
               lambda m: m.group(1) + jsonld() + m.group(2), s, count=1, flags=re.S)

    # spec-pill dropdowns: CSS + JS from the private boats page
    boats = (ROOT / "best-private-boat-tours-budapest.html").read_text()
    css = re.search(r'<style id="bpa-lang-css">.*?</style>', boats, re.S).group(0)
    js = re.search(r'<script id="bpa-lang-js">.*?</script>', boats, re.S).group(0)
    s = s.replace("</head>", css + "\n</head>", 1)
    i = s.rfind("</body>")
    s = s[:i] + js + "\n" + s[i:]

    assert "—" not in s, "em dash"
    PAGE.write_text(s)
    print("ok", len(s))


if __name__ == "__main__":
    main()
