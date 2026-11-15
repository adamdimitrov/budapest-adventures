# -*- coding: utf-8 -*-
"""EN copy for /things-to-do-budapest-december. Facts: scripts/december_data.py. No em dashes."""

LANG = "en"
SLUG = "things-to-do-budapest-december"
PATH = "/things-to-do-budapest-december"
SLUG_CSS = "things-to-do-budapest-december"
TITLE_TAG = "Things to Do in Budapest in December 2026 (Local's Picks)"
H1 = "11 Best Things to Do in Budapest in December 2026"
H1_MUTED = "(Christmas, Baths and Holiday Hours)"
CRUMB = "Things to Do in Budapest in December"
META = ("What to do in Budapest in December 2026: Christmas dinner cruises, outdoor thermal pools, "
        "market tours, the Nutcracker and what is open on 24-26 and 31 December. From €12.")
KICKER = "December 2026 Planner"
AUTHOR_ROLE = "11 Picks • 4 Personally Tested • Holiday Hours"
UPDATED = "Last updated"
UPDATED_DATE = "Nov 15, 2026"

UI = dict(
    check="Check Availability →", book_site="Check Availability →", read="Read Review ↓",
    free_cxl="Free cancellation", instant="Instant QR", cxl24="Free 24h Cancellation",
    direct_trust="Booked on the operator's own site",
    reviews_one="{n} reviews · 1 site", reviews_many="{n} reviews · {k} sites",
    rating_on="Rating on 1 booking site", rating_many="Ratings on {k} booking sites, each for this exact product",
    no_rating="🎄 Christmas-only sailing", tested="✓ Personally Tested",
    pick="✓ Pick it", skip="✕ Skip it", pros="Pros:", cons="Cons:", summary="Summary &amp; Review", overview="Overview",
    live="Official Tickets &amp; Live Availability", book_dates="Check Dates &amp; Book Tickets",
    best_price="Best Price Guaranteed • Instant Confirmation", qf="Quick Facts",
    perk_qr="Instant Smartphone QR Voucher", perk_refund="Full Refund up to 24h Before",
    perk_direct="Booked directly with the operator",
    breakdown_h="Detailed Breakdown: 11 Things to Do in Budapest in December",
    breakdown_sub="Ranked • All reviews open by default • Click to collapse/expand",
    expand="Expand All", collapse="Collapse All",
    contents="Contents (11)", all_items="All 11 December Picks", jump="Jump to a December Pick",
    toc_deck="Top 11 December Picks", toc_breakdown="Detailed Breakdown (11 Picks)",
    filter_all="All", filter_label="Show:",
    filters=[("xmas", "Christmas specials"), ("river", "On the Danube"), ("bath", "Thermal baths"),
             ("food", "Food &amp; markets"), ("u40", "Under €40")],
    per_person="per person", home="Home", by="By", founder="Founder &amp; Budapest Local",
    faq_h="Frequently Asked Questions", from_price="From €{p}",
)

# ---------------------------------------------------------------- cards
C = {}
C["legenda"] = dict(
    rank="🏆 #1 Best December Dinner", title="Candlelit Dinner Cruise With Live Music",
    dur="2.5 Hours", place="Dock 7, Vigadó tér", map="Vigadó tér Dock 7 Budapest",
    psub="2.5 hours • 19:00, not on 24 Dec",
    tested_pop="<strong>I took this cruise myself.</strong> The photos are from Legenda's boat. "
               "Price and timetable rechecked on legenda.hu on 15 November 2026.",
    pills=[("🕒", "Daily · 19:00", "Sails <strong>every evening at 19:00</strong> from 23 November to 31 December 2026, <strong>except 24 December</strong> (daytime cruises only that day). "
            "2.5 hours on the glass-roofed panorama boat. From Legenda's timetable."),
           ("🍽️", "4-course à la carte", "You choose each course at the table from the menu. Children 3 to 12 get a 3-course kids' menu for €84. Drinks are paid on board."),
           ("🎶", "Live music", "Live music on board all evening, plus a welcome drink. Tables are set with candles."),
           ("🎄", "25, 26 and 31 Dec", "It sails at 19:00 on 25 and 26 December and on New Year's Eve, when many restaurants shorten their hours. On 24 December there is no dinner cruise.")],
    pick="for the most polished Danube dinner in December, any evening except Christmas Eve.",
    skip="if you want drinks included: they are paid on board.",
    pros=["Served 4-course dinner you order at the table, not a buffet",
          "Sails at 19:00 every evening to 31 December, Christmas Day included",
          "Glass-roofed boat: you see the lit-up Parliament from your seat"],
    cons=["Drinks are extra on board", "No dinner cruise on 24 December, and no Christmas-themed menu"],
    body="""<p>December is when a Danube dinner makes the most sense: it is <strong>dark by 16:00</strong>, the bridges and the Parliament are lit for hours, and the boat is warm. Legenda's candlelit cruise is the one I'd book. It is a <strong>served 4-course à la carte dinner</strong> with live music on a glass-roofed boat, and it sails <strong>every evening at 19:00 until 31 December</strong>, except Christmas Eve.</p>
<p>I've taken this cruise myself. What sets it apart from the buffet boats is the service: you order each course at your table, the pace is slow.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> for a date night or a calm family dinner on any December evening, including 25 and 26 December. Kids 3 to 12 eat from a 3-course menu.</p>
<p><strong>Skip it</strong> if you want an all-inclusive price: drinks are paid on board. For a menu written for Christmas Day, see <a href="#item-2-silverline-christmas-dinner">Silverline's 25 December dinner</a>.</p>
<h3>Meeting Point</h3>
<p>🗺️ <strong>Meeting Point: </strong>Legenda pier, Dock 7, Vigadó tér (Pest side).<br/>🚇 <strong>Public Transport:</strong> Vörösmarty tér (M1), tram 2 to Vigadó tér.</p>""",
    qf_badge="Danube dinner", qf=[("Departure", "Daily at 19:00, 23 Nov to 31 Dec 2026 (not 24 Dec)"), ("Duration", "2.5 hours"),
        ("Price", "€110 adult · €84 children 3 to 12"), ("Food", "4-course à la carte dinner (kids: 3 courses)"),
        ("Included", "Cruise, welcome drink, live music, dinner"), ("Not Included", "Drinks on board"),
        ("Pier", "Dock 7, Vigadó tér")],
    chips=[("yes", "✓ Served at Your Table"), ("yes", "✓ Live Music"), ("yes", "✓ Sails on 25, 26 and 31 Dec"), ("no", "✕ Drinks Extra")],
    perks=["Pier: <strong>Dock 7</strong>", "Departure: <strong>19:00</strong>"],
    desc="Candlelit 4-course à la carte dinner cruise with live music, sailing daily at 19:00 through December.",
)
C["silver-xmas"] = dict(
    rank="#2 Christmas Day Dinner", title="Christmas Day Dinner Cruise With Live Piano",
    dur="3 Hours", place="Dock 11", map="Jane Haining rakpart Dock 11 Budapest",
    psub="3 hours • 25 December only",
    pills=[("🎄", "25 Dec · 19:30", "Boarding at 19:00, departure 19:30, back at 22:30. Sold for <strong>25 December</strong>."),
           ("🍽️", "4-course Christmas menu", "Starter (burrata panzanella or goose liver pâté with Tokaji Aszú), beef ragout or seasonal soup, "
            "6 mains (cod, salmon lasagne, pork tenderloin, lamb rack and two vegan or gluten-free options), 3 desserts."),
           ("🎹", "Live piano", "Live piano and a singer on board, welcome drink, candlelit private table and a small Christmas gift."),
           ("🪟", "Window table +€55", "The base ticket is €155. A guaranteed window table costs €55 more (€210).")],
    pick="for a proper Christmas Day dinner with a festive menu and live piano.",
    skip="if you want a window table at the base price: it is €55 extra.",
    pros=["The only seated 4-course menu written for Christmas Day here",
          "Vegan and gluten-free choices for every course",
          "3 hours on the water, longer than most dinner cruises"],
    cons=["Only on 25 December", "Window tables cost €55 more"],
    body="""<p>If your Christmas dinner has to feel like Christmas, this is the one. Silverline sells it for <strong>25 December</strong>: a <strong>4-course festive menu</strong> (goose liver pâté with Tokaji Aszú, beef ragout soup, lamb rack or cod, apple pie trifle), <strong>live piano</strong>, a welcome drink and a small Christmas gift, over <strong>3 hours</strong> on the river.</p>
<p>I've done Silverline's regular dinner cruise from the same dock. The Christmas sailing swaps the standard menu for a festive one and adds the piano and singer.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> if you are in Budapest on Christmas Day and want the dinner to be the event. Every course has a vegan or gluten-free option.</p>
<p><strong>Skip it</strong> if your dates are flexible: <a href="#item-1-legenda-candlelit-dinner">Legenda</a> serves a similar 4-course dinner on almost every December evening for €110.</p>
<h3>Meeting Point</h3>
<p>🗺️ <strong>Meeting Point: </strong>Silverline, Dock 11, Jane Haining rakpart (Pest side). Arrive by 19:00.<br/>🚇 <strong>Public Transport:</strong> Vörösmarty tér (M1), tram 2.</p>""",
    qf_badge="25 December", qf=[("Date", "25 December 2026"), ("Times", "Boarding 19:00 · departure 19:30 · back 22:30"),
        ("Price", "€155 · window table €210"), ("Food", "4-course Christmas menu, 6 mains to choose from"),
        ("Included", "Cruise, welcome drink, dinner, live piano, Christmas gift"), ("Pier", "Dock 11, Jane Haining rakpart")],
    chips=[("yes", "✓ Christmas Menu"), ("yes", "✓ Live Piano"), ("yes", "✓ Vegan Options"), ("no", "✕ 25 Dec Only")],
    perks=["Pier: <strong>Dock 11</strong>", "Date: <strong>25 Dec</strong>"],
    desc="Christmas Day dinner cruise on the Danube with a 4-course festive menu, live piano and welcome drink.",
)
C["szechenyi"] = dict(
    rank="#3 Best Winter Bath", title="Széchenyi Thermal Bath", dur="Half Day", place="City Park",
    map="Széchenyi Thermal Bath Budapest", psub="per adult • Mon to Thu morning pass",
    tested_pop="<strong>I visited Széchenyi myself.</strong> Most photos are my own. Hours rechecked on the official site on 14 November 2026.",
    pills=[("🕒", "Holiday hours", "<strong>Mon to Thu</strong> 7:00 to 20:00, <strong>Fri</strong> 7:00 to 22:00, <strong>Sat and Sun</strong> 8:00 to 20:00. "
            "8 December: closes at 16:00. 18 December to 6 January: opens at 8:00. 25 and 26 December and 1 January: opens at 10:00."),
           ("♨️", "Outdoor pools at 36-38 °C", "Outdoor thermal pool 36 to 38 °C, adventure pool 32 to 34 °C, swimming pool 26 to 28 °C, all open in winter."),
           ("🎟️", "Morning pass €39", "Morning pass with locker, entry 7:00 to 9:00, Mon to Thu: €39. Weekday pass €46, with private cabin €50. "
            "At the desk: 13,200 HUF Mon to Thu, 15,800 HUF in peak periods."),
           ("🌆", "Go after dark", "Sunset is just before 16:00 in December. Steam over the outdoor pools under the lit yellow facade is the photo people come for.")],
    pick="for the classic December picture: hot outdoor pools steaming in the cold.",
    skip="if you hate crowds: holiday afternoons are busy, so go at opening.",
    pros=["Three outdoor pools open all winter, the hottest at 36 to 38 °C",
          "Open until 22:00 on Fridays", "Opens at 10:00 even on 25 and 26 December and 1 January"],
    cons=["Busiest bath in town over the holidays", "Booking-site tickets cost more than the desk"],
    body="""<p>The best December hour in Budapest is spent in an outdoor pool at <strong>36 to 38 °C</strong> while the air is near freezing. Széchenyi has three outdoor pools open all winter, and with sunset before 16:00 you get the steam, the lit yellow facade and the cold air on your face in the same late afternoon.</p>
<p>I've been to Széchenyi myself. It also keeps the most useful holiday hours: from <strong>18 December to 6 January it opens at 8:00</strong>, and on <strong>25 and 26 December and 1 January it opens at 10:00</strong>, when almost everything else in the city is shut.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> for your first bath, or for Christmas Day itself. The €39 morning pass (Mon to Thu, entry by 9:00) is the best value.</p>
<p><strong>Skip it</strong> if you want quiet: for a smaller Ottoman-era bath with a rooftop pool, book <a href="#item-5-rudas-thermal-bath">Rudas</a>.</p>
<h3>Getting There</h3>
<p>🚇 <strong>Metro:</strong> M1 to Széchenyi fürdő, the station is at the entrance.<br/>🎒 <strong>Bring:</strong> Swimsuit, flip-flops and a towel. Walk fast between the indoor halls and the outdoor pools.</p>""",
    qf_badge="City Park", qf=[("Hours", "Mon to Thu 7:00 to 20:00 · Fri to 22:00 · Sat and Sun 8:00 to 20:00"),
        ("Holidays", "18 Dec to 6 Jan opens 8:00 · 25, 26 Dec and 1 Jan opens 10:00 · 8 Dec closes 16:00"),
        ("Ticket", "Morning pass €39 · weekday pass €46 · with cabin €50"),
        ("Outdoor Pools", "36-38 °C thermal · 32-34 °C adventure · 26-28 °C swimming"), ("Metro", "M1 Széchenyi fürdő")],
    chips=[("yes", "✓ Outdoor Pools in Winter"), ("yes", "✓ Open on Christmas Day"), ("yes", "✓ Free Cancellation"), ("no", "✕ Crowded Afternoons")],
    perks=["Area: <strong>City Park</strong>", "Pools: <strong>3 outdoor</strong>"],
    desc="Full-day ticket to Széchenyi Thermal Bath with outdoor thermal pools open all winter.",
)
C["wonderland"] = dict(
    rank="#4 Best Market Tour", title="Christmas Market Tour With Tastings", dur="2.5 Hours", place="Hungarian State Opera",
    map="Hungarian State Opera Budapest Andrássy út 22", psub="per person • Every day in December",
    pills=[("🎄", "Basilica + Vörösmarty", "A guided walk through the two big central markets, Advent Bazilika and Vörösmarty tér, with stops for the best stalls."),
           ("🍷", "Tastings included", "Mulled wine and market treats are included, so you taste the classics without queuing at ten stalls."),
           ("📅", "Bookable all December", "Bookable every day from 1 to 31 December. Starts at the Hungarian State Opera on Andrássy út."),
           ("👥", "Small group", "Run by Budapest Urban Walks with a local guide; few reviews so far, all very high.")],
    pick="if it is your first evening and you want the markets explained, with the tastings paid for.",
    skip="if you just want to wander: both markets are free to enter.",
    pros=["Covers both central markets in one walk", "Tastings included in the price", "Bookable every day in December"],
    cons=["€90 for something you can partly do free", "Only a handful of reviews yet"],
    body="""<p>Budapest's two big Christmas markets are <strong>free and five minutes apart</strong>, and that is exactly why first-timers miss the good stalls: everything looks the same after the third mug of mulled wine. This tour walks you through <strong>Advent Bazilika and Vörösmarty tér</strong> with a local guide and pays for the tastings on the way.</p>
<p>It starts at the Opera on Andrássy út, which is handy if you have <a href="#nutcracker">Nutcracker tickets</a> the same evening.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> on your first evening in town, when a guide saves you an hour of guessing what to eat.</p>
<p><strong>Skip it</strong> if you are happy exploring alone: our <a href="/budapest-christmas-markets">Budapest Christmas markets guide</a> has the hours, prices and a walking route for free.</p>
<h3>Meeting Point</h3>
<p>🗺️ <strong>Meeting Point: </strong>Hungarian State Opera, Andrássy út 22.<br/>🚇 <strong>Public Transport:</strong> Opera (M1).</p>""",
    qf_badge="Advent Bazilika + Vörösmarty tér", qf=[("Duration", "2.5 hours"), ("Price", "From €90 / person"),
        ("Route", "Advent Bazilika and Vörösmarty Classic Xmas"), ("Included", "Local guide, tastings"),
        ("Dates", "Bookable every day 1 to 31 December"), ("Meeting Point", "Hungarian State Opera, Andrássy út 22")],
    chips=[("yes", "✓ Tastings Included"), ("yes", "✓ Both Central Markets"), ("yes", "✓ Free Cancellation"), ("no", "✕ Few Reviews Yet")],
    perks=["Start: <strong>Opera</strong>", "Markets: <strong>2</strong>"],
    desc="Guided walk through Budapest's two central Christmas markets with tastings included.",
)
C["rudas"] = dict(
    rank="#5 Best Night Bath", title="Rudas Thermal Bath With 3-Course Meal", dur="3-4 Hours", place="Elizabeth Bridge",
    map="Rudas Thermal Bath Budapest", psub="per adult • bath + 3-course meal",
    tested_pop="<strong>I visited Rudas myself.</strong> Hours and pool temperatures rechecked on rudasfurdo.hu on 14 November 2026.",
    pills=[("🌙", "Night bathing Fri and Sat", "<strong>Night bathing</strong> runs Friday and Saturday 22:00 to 3:00 (online tickets only, sold separately). "
            "Wellness hours: Mon 6:00 to 22:00, Tue to Sun 6:00 to 20:00. 8 December: closes at 16:00."),
           ("🏊", "Rooftop pool 36 °C", "Panorama pool on the roof at 36 °C with a Danube view, plus six Turkish pools from 16 to 42 °C under a 16th-century dome."),
           ("🍽️", "3-course meal", "This ticket bundles a day pass with a 3-course meal at the bath's restaurant, the only booking-site version of Rudas."),
           ("🚻", "Check the day", "The Turkish bath has men-only and women-only days. Mixed: Mon 11:00 to 22:00, Thu and Fri 11:00 to 20:00, Sat and Sun all day.")],
    pick="for a hot rooftop pool over the Danube on a cold night, and the Ottoman dome below it.",
    skip="if you want a plain entry ticket: this one includes a meal.",
    pros=["Rooftop hot pool with a river view", "16th-century Turkish bath under a stone dome", "Late night bathing on Friday and Saturday"],
    cons=["Men-only and women-only days in the Turkish part", "The booking-site ticket always includes a meal"],
    body="""<p>Rudas is the bath for a December night. The <strong>rooftop pool is 36 °C</strong> and looks across the Danube to the lit Parliament and bridges, and downstairs the <strong>Turkish bath under a 16th-century dome</strong> has six pools from 16 to 42 °C. On <strong>Friday and Saturday it reopens for night bathing from 22:00 to 3:00</strong>.</p>
<p>I've been to Rudas myself. Its rooftop pool is the best place I know to sit out a grey December afternoon. Tickets, prices and night bathing in detail: <a href="/rudas-baths-budapest">Rudas Baths Budapest</a>.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> if you've done Széchenyi or want something calmer and older. The meal makes it a full afternoon.</p>
<p><strong>Skip it</strong> if your day falls on a single-sex day for the Turkish bath and you are travelling as a couple: check the timetable in the pill above.</p>
<h3>Getting There</h3>
<p>🚋 <strong>Public Transport:</strong> Tram 19 or 41, or bus 7, to Rudas fürdő at the Buda end of Elizabeth Bridge.<br/>🌙 <strong>After night bathing:</strong> night buses 907 and 973.</p>""",
    qf_badge="Elizabeth Bridge", qf=[("Hours", "Wellness Mon 6:00 to 22:00, Tue to Sun 6:00 to 20:00"),
        ("Night Bathing", "Fri and Sat 22:00 to 3:00 (separate online ticket)"), ("Ticket", "Day pass + 3-course meal from €74.99"),
        ("Rooftop Pool", "36 °C"), ("Transport", "Tram 19, 41 · bus 7")],
    chips=[("yes", "✓ Rooftop Hot Pool"), ("yes", "✓ Meal Included"), ("yes", "✓ Night Bathing Weekends"), ("no", "✕ Single-Sex Days")],
    perks=["Area: <strong>Elizabeth Bridge</strong>", "Rooftop: <strong>36 °C</strong>"],
    desc="Rudas Thermal Bath day pass with a 3-course meal, rooftop panorama pool and Ottoman Turkish bath.",
)
C["mulled"] = dict(
    rank="#6 Cheapest Danube Hour", title="Danube Sightseeing Cruise With Unlimited Mulled Wine", dur="1 Hour", place="Dock 11",
    map="Jane Haining rakpart Dock 11 Budapest", psub="1 hour • Unlimited mulled wine",
    pills=[("🍷", "Unlimited mulled wine", "Five kinds poured for the whole hour: classic red, rosé-raspberry, apple-cinnamon and alcohol-free hot spiced orange among them."),
           ("🕒", "Evening sailings", "Three evening sailings on a typical December day: 18:00, 19:30 and 21:00. No sailings on 24 to 26 December."),
           ("🎧", "Audio guide app", "Free audio guide app for the sights along the way. No food on board, drinks only."),
           ("💶", "€21", "€21 per person, the lowest price for an hour on the Danube with drinks in December.")],
    pick="for a warm, cheap hour on the Danube between the market and dinner.",
    skip="for 24 to 26 December: it doesn't sail on those days.",
    pros=["€21 with unlimited mulled wine", "Three evening sailings, easy to fit around dinner", "Alcohol-free hot drinks too"],
    cons=["No sailings 24 to 26 December", "Drinks only, no food"],
    body="""<p>A full dinner cruise is two or three hours and €100 plus. If you just want <strong>the lit-up city from the water with a hot drink</strong>, this is the December shortcut: <strong>one hour, unlimited mulled wine, €21</strong>, from the same Silverline dock as the Christmas dinner.</p>
<p>There are usually three evening sailings (18:00, 19:30, 21:00), so it slots in after the <a href="/budapest-christmas-markets">Christmas markets</a> and before a late dinner.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> on a budget, or as a short add-on to an evening in the centre.</p>
<p><strong>Skip it</strong> on 24, 25 and 26 December, when it doesn't run. On Christmas Eve, the <a href="#item-7-hungaria-christmas-eve-cruise">Hungária Koncert cruise</a> sails instead.</p>
<h3>Meeting Point</h3>
<p>🗺️ <strong>Meeting Point: </strong>Silverline, Dock 11, Jane Haining rakpart.<br/>🚇 <strong>Public Transport:</strong> Vörösmarty tér (M1), tram 2.</p>""",
    qf_badge="Sightseeing + drinks", qf=[("Duration", "1 hour"), ("Price", "€21 / person"), ("Sailings", "Typically 18:00, 19:30, 21:00"),
        ("Drinks", "Unlimited mulled wine, alcohol-free hot drinks"), ("Not Running", "24, 25 and 26 December"), ("Pier", "Dock 11")],
    chips=[("yes", "✓ Unlimited Mulled Wine"), ("yes", "✓ Cheapest Cruise"), ("no", "✕ No Food"), ("no", "✕ Not 24 to 26 Dec")],
    perks=["Pier: <strong>Dock 11</strong>", "Duration: <strong>1 Hour</strong>"],
    desc="One-hour Danube sightseeing cruise with unlimited mulled wine, €21.",
)
C["hungaria"] = dict(
    rank="#7 Best on Christmas Eve", title="Christmas Eve Cruise With Folk Show and Open Bar", dur="1.5 Hours", place="Akadémia 2",
    map="Akadémia pier Budapest", psub="per person • 24 and 25 Dec",
    pills=[("🕖", "24 Dec · 19:00 or 21:30", "The Holiday Tasting Menu option sails at 19:00 and 21:30 on 24 and 25 December, 90 minutes each, €76."),
           ("🎂", "Board + Christmas cakes", "A charcuterie and cheese board with dips, fruit and nuts, then a Christmas cake buffet. A tasting, not a full dinner."),
           ("🍷", "Open bar", "Unlimited beer, wine and soft drinks for the whole cruise."),
           ("🎻", "Live music + folk show", "Live Hungarian music and a folk dance show on board.")],
    pick="for something festive on Christmas Eve, when the city closes early.",
    skip="if you want a full dinner: it is a tasting board and cake buffet.",
    pros=["One of the few things running on the evening of 24 December", "Open bar with beer, wine and soft drinks", "Folk show and live music"],
    cons=["A tasting board, not a meal", "Only 90 minutes"],
    body="""<p>From 2026, <strong>24 December is a public holiday in Hungary</strong> and shops have to close (restaurants and hotels may open). The markets shut in the early afternoon, so Christmas Eve evening is the hardest slot to fill. This cruise fills it: <strong>90 minutes on the Danube at 19:00 or 21:30</strong>, a charcuterie board and Christmas cake buffet, <strong>unlimited beer, wine and soft drinks</strong>, live music and a folk dance show.</p>
<p>It runs on Hungária Koncert's boat, the same one as its year-round dinner and folk show cruise.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> if you want Christmas Eve to feel like an occasion without a long sit-down dinner.</p>
<p><strong>Skip it</strong> if you're hungry: eat first (restaurants may open on 24 December), because Legenda's dinner cruise doesn't sail that night.</p>
<h3>Meeting Point</h3>
<p>🗺️ <strong>Meeting Point: </strong>Akadémia pier 2, near the Chain Bridge on the Pest side.<br/>🚋 <strong>Public Transport:</strong> Tram 2 to Széchenyi István tér.</p>""",
    qf_badge="24 and 25 December", qf=[("Dates", "24 and 25 December 2026"), ("Times", "19:00 to 20:30 or 21:30 to 23:00"),
        ("Price", "€76 / person (Holiday Tasting Menu)"), ("Food", "Charcuterie and cheese board, Christmas cake buffet"),
        ("Drinks", "Unlimited beer, wine, soft drinks"), ("Show", "Live music and folk dance"), ("Pier", "Akadémia 2")],
    chips=[("yes", "✓ Runs on Christmas Eve"), ("yes", "✓ Open Bar"), ("yes", "✓ Folk Show"), ("no", "✕ Not a Full Dinner")],
    perks=["Pier: <strong>Akadémia 2</strong>", "Date: <strong>24 Dec</strong>"],
    desc="Christmas Eve Danube cruise with a tasting board, Christmas cakes, open bar, live music and folk show.",
)
C["workshop"] = dict(
    rank="#8 Best Rainy-Day Pick", title="Chimney Cake (Kürtőskalács) Baking Workshop", dur="65 Minutes", place="Ipar utca 11",
    map="Ipar utca 11 Budapest 1095", psub="per person • Every day in December",
    pills=[("🧑‍🍳", "Bake your own", "You roll, wrap and bake your own chimney cake on the spit. Ingredients, tools and an apron are provided."),
           ("⏱️", "65 minutes", "Fits easily around a bath or a cruise. Bookable every day from 1 to 31 December."),
           ("🎄", "The market treat", "Kürtőskalács is the sweet you smell at every Christmas market stall. Here you learn how it is made, and eat it warm."),
           ("👨‍👩‍👧", "Good with kids", "Easy for children to do themselves, and you eat the result warm.")],
    pick="for a warm indoor hour with kids, or on a wet December afternoon.",
    skip="if you only want to eat one: every Christmas market sells them.",
    pros=["Under €20 for a hands-on hour", "Rated 4.9 by more than 1,700 guests", "Indoors, so weather doesn't matter"],
    cons=["Out of the centre in District IX", "Short: about an hour"],
    body="""<p>Every Christmas market in Budapest smells of <strong>kürtőskalács</strong>, the spit-roasted chimney cake. In this <strong>65-minute workshop</strong> you roll, wrap and bake your own, then eat it warm with your choice of topping. It is rated 4.9 by more than 1,700 guests, and it is indoors.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> with kids, or for a December afternoon when the drizzle rules out a walk. It costs from €19.56.</p>
<p><strong>Skip it</strong> if you just want a taste: a market stall is quicker. For a full evening of Hungarian food, see the <a href="#item-10-foodapest-food-tour">Foodapest tour</a>.</p>
<h3>Meeting Point</h3>
<p>🗺️ <strong>Meeting Point: </strong>Ipar utca 11, 1095 Budapest (District IX).<br/>🚇 <strong>Public Transport:</strong> Tram 2 or 24, or M3 to Corvin-negyed.</p>""",
    qf_badge="Hands-on baking", qf=[("Duration", "65 minutes"), ("Price", "From €19.56 / person"),
        ("Included", "Ingredients, tools, apron, your chimney cake"), ("Dates", "Bookable every day in December"), ("Address", "Ipar utca 11, District IX")],
    chips=[("yes", "✓ Indoors"), ("yes", "✓ Kid-Friendly"), ("yes", "✓ Free Cancellation"), ("no", "✕ Outside the Centre")],
    perks=["Address: <strong>Ipar utca 11</strong>", "Duration: <strong>65 Min</strong>"],
    desc="Hands-on 65-minute chimney cake (kürtőskalács) baking workshop in Budapest.",
)
C["castle"] = dict(
    rank="#9 Best Budget Pick", title="Buda Castle District Walking Tour", dur="2 Hours", place="Szentháromság tér",
    map="Szentháromság tér Budapest", psub="per person • 2 hours",
    tested_pop="<strong>I took this tour myself.</strong> Price and rating rechecked on the live listing on 15 November 2026.",
    pills=[("🏰", "Castle Hill in 2 hours", "Matthias Church, Fisherman's Bastion and the old streets of the Castle District with a guide."),
           ("🎄", "Budavári Advent", "From 27 November to 3 January the small Budavári Advent market fills Szentháromság tér, right where the tour starts."),
           ("🕯️", "Advent Sundays", "On the four Advent Sundays (29 Nov, 6, 13 and 20 Dec) a candle is lit on the square at 16:00."),
           ("💶", "From €12", "The cheapest guided activity on this list.")],
    pick="for a cheap, guided morning on Castle Hill before the light goes.",
    skip="if you want an evening activity: in December it is dark by 16:00.",
    pros=["€12 for a 2-hour guided walk", "Starts at the Budavári Advent market", "Rated 4.6 by 2,400+ guests"],
    cons=["Outdoors for 2 hours in the cold", "Church interiors are extra"],
    body="""<p>Castle Hill is a daylight job in December: the sun sets just before 16:00. This <strong>2-hour guided walk for €12</strong> covers Matthias Church, Fisherman's Bastion and the old Castle District streets, and it starts on Szentháromság tér, where the small <strong>Budavári Advent market</strong> runs from 27 November.</p>
<p>I've taken this tour myself. Book a morning slot, then stay for a mulled wine at the market by the church.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> on a dry morning for the best views over the river.</p>
<p><strong>Skip it</strong> for the afternoon: by 15:30 the light is going. Go back after dark for the lit Bastion instead, it is free.</p>
<h3>Meeting Point</h3>
<p>🗺️ <strong>Meeting Point: </strong>Szentháromság tér, by Matthias Church.<br/>🚌 <strong>Public Transport:</strong> Bus 16 from Deák Ferenc tér, or the Castle Hill funicular from Clark Ádám tér.</p>""",
    qf_badge="Castle District", qf=[("Duration", "2 hours"), ("Price", "From €12 / person"), ("Route", "Matthias Church, Fisherman's Bastion, Castle District"),
        ("Advent Market", "Budavári Advent, 27 Nov to 3 Jan, by Matthias Church"), ("Transport", "Bus 16, Castle Hill funicular")],
    chips=[("yes", "✓ Cheapest Pick"), ("yes", "✓ Starts at a Christmas Market"), ("no", "✕ Outdoors in the Cold")],
    perks=["Start: <strong>Szentháromság tér</strong>", "Duration: <strong>2 Hours</strong>"],
    desc="Two-hour guided walking tour of the Buda Castle District from €12.",
)
C["foodapest"] = dict(
    rank="#10 Best Food Tour", title="Market to Tavern Food Tour With Wine", dur="3 Hours", place="Central Market Hall",
    map="Central Market Hall Budapest", psub="per person • 12+ tastings",
    pills=[("🏛️", "Market + tavern", "Starts in the Central Market Hall, then a bakery and two local restaurants. The last stop is the wine tasting."),
           ("🍽️", "12+ tastings", "Lángos, goulash, sausages, cheese and pastries: enough to count as dinner."),
           ("🍷", "Hungarian wines", "Wine tasting at the end of the tour, plus a local drink along the way."),
           ("🕒", "Warm stops", "Most of the 3 hours is spent indoors, which matters in December.")],
    pick="for a December evening where dinner is the tour.",
    skip="if you plan a dinner cruise the same night: you won't be hungry.",
    pros=["Rated 4.9 by nearly 700 guests", "Enough food to replace dinner", "Mostly indoors"],
    cons=["3 hours on your feet", "Tight around a dinner cruise"],
    body="""<p>December is the month Hungarians eat heaviest, and the Central Market Hall is at its busiest. This tour starts there and works its way through <strong>12+ tastings</strong> (lángos, goulash, sausages, cheese) in a bakery and two local restaurants, ending with <strong>Hungarian wines</strong>. Most of the 3 hours are indoors.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> as your first or second evening: you'll know what to order for the rest of the trip.</p>
<p><strong>Skip it</strong> on a dinner cruise night. More options are in our <a href="/best-food-tours-budapest">Budapest food tours comparison</a>.</p>
<h3>Meeting Point</h3>
<p>🗺️ <strong>Meeting Point: </strong>Central Market Hall, Fővám tér (the exact spot is in your voucher).<br/>🚇 <strong>Public Transport:</strong> Fővám tér (M4), tram 2, 47 or 49.</p>""",
    qf_badge="Food + wine", qf=[("Duration", "About 3 hours"), ("Price", "From €62 / person"), ("Food", "12+ tastings"),
        ("Drinks", "Hungarian wine tasting"), ("Start", "Central Market Hall, Fővám tér")],
    chips=[("yes", "✓ Counts as Dinner"), ("yes", "✓ Wine Included"), ("yes", "✓ Mostly Indoors")],
    perks=["Start: <strong>Market Hall</strong>", "Tastings: <strong>12+</strong>"],
    desc="Three-hour Budapest food tour from the Central Market Hall to a local tavern with 12+ tastings and wine.",
)
C["nye"] = dict(
    rank="#11 Best New Year's Eve Party", title="New Year's Eve Cruise With DJ and Open Bar", dur="3 Hours", place="Dock 11",
    map="Jane Haining rakpart Dock 11 Budapest", psub="3 hours • 31 December",
    pills=[("🎆", "22:00 to 1:00", "Boarding 21:30, departure 22:00, midnight toast on the river, back at 1:00."),
           ("🍸", "Unlimited open bar", "Prosecco, wine, beer and soft drinks for the whole cruise."),
           ("🍢", "Finger food buffet", "Canapés, tapas, warm bites and mini desserts all night. No sit-down dinner."),
           ("🎧", "Live DJ", "Party music on a decorated catamaran. Built for mingling and dancing.")],
    pick="for midnight on the Danube with an open bar and a DJ.",
    skip="if you want a seated gala dinner: this is a standing party.",
    pros=["Midnight on the river with the city lit up", "Open bar all night", "Ends at 1:00, so you still reach the street parties"],
    cons=["€239 per person", "Finger food, not a dinner"],
    body="""<p>Budapest's New Year's Eve is a street party along the Grand Boulevard and the river, and the best seat for midnight is on the water. Silverline's party cruise <strong>leaves at 22:00 and is back at 1:00</strong>, with a <strong>DJ, finger food buffet and unlimited prosecco, wine and beer</strong>.</p>
<p>For seated gala dinners and cheaper options, see our full <a href="/new-years-eve-cruises-budapest">New Year's Eve cruises comparison</a>.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> if you want a party with drinks sorted and the midnight view.</p>
<p><strong>Skip it</strong> if you prefer to sit down for dinner, or to stay on the street for free.</p>
<h3>Meeting Point</h3>
<p>🗺️ <strong>Meeting Point: </strong>Silverline, Dock 11, Jane Haining rakpart. Boarding from 21:30.</p>""",
    qf_badge="31 December", qf=[("Date", "31 December 2026"), ("Times", "Boarding 21:30 · departure 22:00 · back 1:00"),
        ("Price", "From €239 / person"), ("Included", "Cruise, DJ, finger food buffet, unlimited prosecco, wine, beer, soft drinks"), ("Pier", "Dock 11")],
    chips=[("yes", "✓ Midnight on the Danube"), ("yes", "✓ Open Bar"), ("no", "✕ No Seated Dinner")],
    perks=["Pier: <strong>Dock 11</strong>", "Date: <strong>31 Dec</strong>"],
    desc="New Year's Eve party cruise on the Danube with DJ, finger food buffet and unlimited drinks.",
)

ANCHORS = {"legenda": "item-1-legenda-candlelit-dinner", "silver-xmas": "item-2-silverline-christmas-dinner",
           "szechenyi": "item-3-szechenyi-thermal-bath", "wonderland": "item-4-christmas-market-tour",
           "rudas": "item-5-rudas-thermal-bath", "mulled": "item-6-mulled-wine-cruise",
           "hungaria": "item-7-hungaria-christmas-eve-cruise", "workshop": "item-8-chimney-cake-workshop",
           "castle": "item-9-buda-castle-walking-tour", "foodapest": "item-10-foodapest-food-tour",
           "nye": "item-11-new-years-eve-cruise"}


def A(k):
    return "#" + ANCHORS[k]


LEAD = f"""<p>In December, Budapest's day is <strong>8.5 hours long and the sun sets just before 16:00</strong>. That changes how you plan: sights in the morning, then a long evening of lit-up bridges, hot outdoor pools and Christmas markets. From 2026, <strong>24 December is also a public holiday</strong>, and most shops close for the day.</p>
<p>Below are the 11 things I'd book for December, 4 of them done myself, ranked for a winter trip, plus the <a href="#holiday-hours">holiday opening hours</a>, the <a href="#nutcracker">Nutcracker dates</a> and the free things worth your evening. Only one evening? Book <a href="{A('legenda')}"><strong>Legenda's candlelit dinner cruise</strong></a> (€110, 19:00 every night except 24 December).</p>"""

PICKS_H = "Quick Picks for December"
PICKS = [("A December dinner on the Danube", "legenda", "€110, 19:00 daily except 24 Dec, served 4 courses"),
         ("Christmas Day dinner", "silver-xmas", "€155, 25 December, festive menu and live piano"),
         ("Christmas Eve evening", "hungaria", "€76, 19:00 or 21:30, open bar and folk show"),
         ("Hot outdoor pools in the cold", "szechenyi", "from €39, open on 25 and 26 December"),
         ("A bath at night", "rudas", "rooftop pool, night bathing Fri and Sat"),
         ("The markets with a guide", "wonderland", "€90, tastings included"),
         ("On a budget", "mulled", "€21 cruise with unlimited mulled wine, or the €12 castle walk"),
         ("New Year's Eve", "nye", "€239, midnight on the river with an open bar")]

HOLIDAY_H = "What Is Open on 24-26 and 31 December"
HOLIDAY_INTRO = ("Hungary made <strong>24 December a public holiday</strong> on 3 November 2026, from this year on. "
                 "Shops must stay closed that day, except restaurants, hotels, flower and sweet shops, petrol stations and shops at stations and the airport. "
                 "25 and 26 December are public holidays as usual. Plan your meals and bookings around these hours:")
HOLIDAY_COLS = ["", "24 Dec", "25 Dec", "26 Dec", "31 Dec", "1 Jan"]
HOLIDAY_ROWS = [
    ("Shops", "Closed (holiday)", "Closed", "Closed", "Open", "Closed"),
    ("Advent Bazilika market", "11:00-15:00", "11:00-20:00", "11:00-20:00", "11:00-03:00", "11:00-18:00"),
    ("Vörösmarty tér market", "10:00-14:00", "12:00-18:00", "12:00-18:00", "11:00-03:00", "Closed"),
    ("Budavári Advent (Castle)", "09:00-12:00", "Closed", "Closed", "Closed", "12:00-20:00"),
    ("Széchenyi Bath", "From 8:00", "From 10:00", "From 10:00", "From 8:00", "From 10:00"),
    ("Legenda dinner cruise", "No dinner (day cruises)", "19:00", "19:00", "19:00", "-"),
    ("Nutcracker (Opera)", "11:00", "11:00", "11:00, 18:00", "13:00, 21:00", "-"),
]
HOLIDAY_NOTE = ("Market hours from the organisers' 2026 timetables; Széchenyi from its official holiday hours; "
                "closing times on 24 and 31 December can be shorter than usual, so check the bath's site on the day.")

SEASON_H = "December Weather and Daylight in Budapest"
SEASON_P = ("Expect <strong>around 5 °C by day and just below 0 °C at night</strong>, with about 7 days of rain or snow in the month "
            "and only about 49 hours of sunshine (1991-2020 averages). Snow on the ground is possible but not the rule. "
            "Pack a warm coat, a hat and shoes with grip for the cobbles on Castle Hill.")
SUN_COLS = ["Date", "Sunrise", "Sunset", "Daylight"]
SEASON_TIP = ("<strong>How to use the short days:</strong> outdoor sights from 9:00 to 15:00, a bath at dusk, "
              "then the markets, a cruise or the Opera after dark.")

FREE_H = "Free Things to Do in December"
FREE = [
    ("Walk the two central Christmas markets", "Advent Bazilika (Szent István tér) and Vörösmarty tér are free to enter and five minutes apart. "
     "The Basilica facade gets a 3D light show every 30 minutes from 17:30. Hours, prices and a walking route: "
     "<a href=\"/budapest-christmas-markets\">Budapest Christmas markets 2026</a>."),
    ("Skate on Óbuda's free rink", "The rink on Óbuda's Fő tér is free from 27 November to 31 January (Sun to Thu 8:00 to 21:00, Fri and Sat to 22:00). "
     "The big City Park Ice Rink in front of Vajdahunyad Castle plans to open on 20 November; tickets are sold on its own site."),
    ("See the Advent candles on Castle Hill", "On each Advent Sunday (29 November, 6, 13 and 20 December) a candle is lit at 16:00 on Szentháromság tér, by the Budavári Advent market."),
    ("Watch the light trams", "BKV runs trams and boats covered in lights every Advent. In 2025 they ran daily from 28 November to 6 January from about 16:00, except on 24 and 31 December; "
     "the 2026 timetable is announced on bkv.hu."),
    ("Walk the river after dark", "From the Pest embankment between the Chain Bridge and the Parliament you get the lit Castle, the bridges and the Parliament for free, from about 16:30."),
]

NUT_H = "The Nutcracker at the Opera"
NUT_P = ("The Hungarian State Opera stages <strong>The Nutcracker</strong> almost every day in December: "
         "<strong>28 performances</strong> between 1 and 31 December 2026, including <strong>11:00 on Christmas Eve</strong> "
         "and two on New Year's Eve (13:00 and 21:00). Tickets are sold on the Opera's own site, "
         "<a href=\"https://jegy.opera.hu/\" rel=\"noopener\" target=\"_blank\">jegy.opera.hu</a>, and the weekend and holiday shows go first. "
         "No ticket? The 60-minute <strong>Opera House tour in English</strong> runs daily at 13:30, 15:00 and 16:30 when there is no rehearsal.")
NUT_DATES_LABEL = "All December 2026 dates:"

MORE_H = "More December Ideas"
MORE = [
    ("Christmas cruises compared", "All 9 Christmas cruises side by side, from €19 to €155: <a href=\"/christmas-cruises-budapest\">Christmas cruises in Budapest</a>."),
    ("Every thermal bath compared", "Six baths with winter hours and prices, 4 tested: <a href=\"/thermal-baths-budapest\">best thermal baths in Budapest</a>."),
    ("The Parliament", "Guided tours run through December, and the building is lit at night: <a href=\"/budapest-parliament\">Budapest Parliament tickets and tips</a>."),
    ("A day out of town", "Lake Hévíz stays warm in winter, steaming on cold mornings: <a href=\"/best-day-trips-from-budapest\">day trips from Budapest</a>."),
    ("Museums on cold days", "Whether the Budapest Card pays off on a museum-heavy trip: <a href=\"/budapest-card-is-it-worth-it\">Budapest Card, is it worth it?</a>"),
]
NOV_LINK = ("Coming earlier? See <a href=\"/things-to-do-budapest-november\">things to do in Budapest in November</a>.")

FAQ = [
    ("Is Budapest worth visiting in December?",
     "Yes. December is one of the best months for Budapest: the Christmas markets run all month, the outdoor thermal pools are at their best in the cold, "
     "and the city is lit up from 16:00. Expect around 5 °C by day and short days, so plan sights in the morning and evenings for the markets, baths and river."),
    ("What is open in Budapest on Christmas Eve?",
     "From 2026, 24 December is a public holiday and shops are closed, except restaurants, hotels, flower and sweet shops and petrol stations. "
     "The Advent Bazilika market opens 11:00 to 15:00 and Vörösmarty tér 10:00 to 14:00. In the evening, "
     f"the <a href=\"{A('hungaria')}\">Hungária Koncert Christmas Eve cruise</a> sails at 19:00 and 21:30. "
     "Restaurants and hotels may open, but Legenda's dinner cruise does not sail on 24 December."),
    ("Are the thermal baths open at Christmas?",
     "Yes. Széchenyi opens at 10:00 on 25 and 26 December and 1 January, and at 8:00 from 18 December to 6 January. "
     "On 8 December it closes at 16:00. Rudas has night bathing on Friday and Saturday from 22:00 to 3:00."),
    ("Is there a Christmas dinner cruise on 25 December?",
     f"Yes. <a href=\"{A('silver-xmas')}\">Silverline's Christmas Day dinner cruise</a> (€155) sails on 25 December from 19:30 to 22:30 with a 4-course festive menu and live piano. "
     f"<a href=\"{A('legenda')}\">Legenda's candlelit dinner</a> (€110) also sails every evening in December except Christmas Eve, 25 December included."),
    ("When do the Budapest Christmas markets close?",
     "Advent Bazilika runs until 1 January 2027 and Vörösmarty tér until 31 December (its craft stalls until 28 December). "
     "Both stay open until 3:00 on New Year's Eve. The Óbuda market closes on 23 December, and Budavári Advent runs until 3 January."),
    ("What is the weather like in Budapest in December?",
     "Cold and often grey: about 5 °C by day and just below freezing at night, around 7 days of rain or snow and 49 hours of sunshine in the month. "
     "The sun rises around 7:20 and sets just before 16:00."),
    ("Is the Nutcracker on in Budapest in December 2026?",
     "Yes. The Hungarian State Opera has 28 Nutcracker performances from 1 to 31 December 2026, including 11:00 on 24 December and 13:00 and 21:00 on 31 December. "
     "Tickets are sold on jegy.opera.hu."),
    ("What can I do in Budapest on New Year's Eve?",
     f"The two central Christmas markets stay open until 3:00, the Opera plays the Nutcracker at 21:00, and party cruises sail at midnight, such as "
     f"<a href=\"{A('nye')}\">Silverline's New Year's Eve cruise</a> (22:00 to 1:00, €239). "
     "More options: <a href=\"/new-years-eve-cruises-budapest\">New Year's Eve cruises in Budapest</a>."),
]

METHOD_H = "How These Picks Were Chosen"
METHOD = ("Picked and checked on 15 November 2026. Each card's price, inclusions, times and rating were read on the live listing for that exact product. "
          "Market hours come from the organisers' 2026 timetables, Nutcracker dates from the Opera's ticket office, bath hours from the official bath sites, "
          "the 24 December rule from the government's announcement of 3 November 2026, sunrise and sunset from timeanddate.com and the climate figures from the 1991-2020 normals. "
          "\"Personally Tested\" marks only the four things I've done myself. Prices change with the date, so check the live price before you book.")

HOMECARD = ("Things to Do in December", "Christmas cruises, baths and holiday hours")
MENU_SUB = "Christmas cruises, baths &amp; holiday hours"
MENU_TITLE = "Budapest in December"


def NUT_DAY(d, t):
    return f"{d} Dec {t}"
