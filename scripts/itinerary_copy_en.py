# -*- coding: utf-8 -*-
"""EN copy for /budapest-travel-guide (rebuilt as a 2, 3 or 4-day Budapest itinerary).
Facts: scripts/itinerary_data.py. No em dashes."""

LANG = "en"
SLUG = "budapest-travel-guide"
PATH = "/budapest-travel-guide"
SLUG_CSS = "budapest-travel-guide"
TITLE_TAG = "Budapest Itinerary: 3 Days (or 2 or 4) Planned by a Local, 2026"
H1 = "Budapest Itinerary: The 3-Day Plan a Local Would Follow"
H1_MUTED = "(2 and 4-Day Versions Too)"
CRUMB = "Budapest Itinerary (3 Days)"
META = ("A local's 3-day Budapest itinerary built around opening hours: Parliament and a night cruise, "
        "Castle Hill and ruin bars, baths before 9:00. Bookings from €190, plus 2 and 4-day plans.")
KICKER = "2026 Trip Planner"
AUTHOR_ROLE = "Day-by-Day Plan • 8 Bookings Compared • 3 Personally Tested"
UPDATED = "Last updated"
UPDATED_DATE = "Nov 16, 2026"

LEAD = """<p>Most Budapest itineraries get the order wrong. They send you up Castle Hill at midday, when it is busiest, and into Széchenyi in the afternoon, when the same locker ticket costs <strong>€46 instead of €39</strong> before 9:00.</p>
<p>I live here, so this plan is built around the hours: <strong>Pest and the Parliament on day 1</strong>, ending with a cruise after dark; <strong>Buda on day 2</strong>, with Castle Hill at sunset and the ruin bars after; <strong>the baths at opening on day 3</strong>. Everything worth booking comes to about <strong>€190 per person</strong>, and below each day you get the times, the walks between stops and what to skip.</p>
<p>Only have a weekend? Use the <a href="#two-days">2-day version</a>. Got a fourth day? Add the <a href="#day-4">Danube Bend</a>.</p>"""

UI = dict(
    check="Check Availability →", book_site="Check Availability →", read="Read Review ↓",
    free_cxl="Free cancellation", instant="Instant QR", cxl24="Free 24h Cancellation",
    direct_trust="Booked on the operator's own site",
    reviews_one="{n} reviews · 1 site", reviews_many="{n} reviews · {k} sites",
    rating_on="Rating on 1 booking site", rating_many="Ratings on {k} booking sites, each for this exact product",
    no_rating="No reviews yet", tested="✓ Personally Tested",
    pick="✓ Pick it", skip="✕ Skip it", pros="Pros:", cons="Cons:", summary="Summary &amp; Review", overview="Overview",
    live="Official Tickets &amp; Live Availability", book_dates="Check Dates &amp; Book Tickets",
    best_price="Best Price Guaranteed • Instant Confirmation", qf="Quick Facts",
    perk_qr="Instant Smartphone QR Voucher", perk_refund="Full Refund up to 24h Before",
    perk_direct="Booked directly with the operator",
    breakdown_h="Detailed Breakdown: What to Book for Each Day",
    breakdown_sub="In itinerary order • All reviews open by default • Click to collapse/expand",
    expand="Expand All", collapse="Collapse All",
    contents="Contents (8)", all_items="All 8 Bookings", jump="Jump to a Booking",
    toc_deck="What to Book, Day by Day", toc_breakdown="Detailed Breakdown (8 Bookings)",
    filter_all="All", filter_label="Show:",
    filters=[("d1", "Day 1: Pest"), ("d2", "Day 2: Buda"), ("d3", "Day 3: Baths"), ("d4", "Day 4: Danube Bend"),
             ("eve", "Evenings")],
    per_person="per person", home="Home", by="By", founder="Founder &amp; Budapest Local",
    faq_h="Frequently Asked Questions", from_price="From €{p}",
)

ANCHORS = {k: f"item-{i}-{k}" for i, k in enumerate(
    ["parliament", "basilica", "legenda", "food", "castle", "crawl", "szechenyi", "daytrip"], 1)}


def A(k):
    return "#" + ANCHORS[k]


# ---------------------------------------------------------------- cards
C = {}
C["parliament"] = dict(
    rank="📅 Day 1 · Morning", title="Parliament Tour With Audio Guide", dur="45 Minutes",
    place="Kossuth Lajos tér", map="Hungarian Parliament Building Budapest Visitor Centre",
    psub="per adult • 45-minute tour",
    pills=[("🎟️", "Book a few days ahead",
            "<strong>You can only go inside on a 45-minute tour</strong>, and English slots sell out, days ahead from May to September and at weekends. "
            "The official price is HUF 7,000 for EU/EEA adults and HUF 14,000 for everyone else. <a href=\"/budapest-attractions/budapest-parliament\">Official tickets and tips →</a>"),
           ("🕘", "Take a 9:00 to 10:00 slot",
            "Open 8:00 to 16:00 from November to March (to 18:00 April to October). An early slot leaves the whole day free for the Basilica and the riverside. "
            "Arrive 15 minutes early for the airport-style security check."),
           ("🪪", "Bring your passport", "EU/EEA prices need ID at the door, and everyone goes through security, so carry only a small bag.")],
    pick="if you want the Holy Crown and the gilded staircase on a fixed slot, without hunting for official tickets.",
    skip="if you are an EU/EEA citizen and can plan ahead: the official ticket is HUF 7,000.",
    pros=["The only way inside, on a fixed time slot", "Audio guide in your language", "4.5 from 6,600+ reviews"],
    cons=["Costs more than the official non-EU ticket", "The route inside is fixed, 45 minutes"],
    body="""<p>Start day 1 where every postcard starts: the <strong>Parliament</strong>. You can only go inside on a <strong>45-minute guided tour</strong>, past the gilded main staircase and the Holy Crown, and English slots sell out, so this is the one thing on day 1 to book before you fly.</p>
<p>I like a <strong>9:00 or 10:00 slot</strong>: the security queue is short and you are done before the tour groups arrive. Afterwards walk round the back of the building to the riverside for the classic view across to Buda.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> if you want a guaranteed slot with an audio guide in your language. <strong>Skip it</strong> if you hold an EU/EEA passport and can book a few days ahead on the official site: see my <a href="/budapest-attractions/budapest-parliament">Parliament ticket guide</a>.</p>
<h3>Next Stop</h3>
<p>🚶 St Stephen's Basilica is about a 15-minute walk south-east through Szabadság tér.</p>""",
    qf_badge="Day 1 morning", qf=[("Duration", "45 minutes, fixed time slot"), ("Hours", "8:00 to 16:00 Nov to Mar · 8:00 to 18:00 Apr to Oct"),
        ("Official price", "HUF 7,000 EU/EEA · HUF 14,000 others"), ("Arrive", "15 minutes early for security"),
        ("Address", "Kossuth Lajos tér 1-3, 1055 Budapest")],
    chips=[("yes", "✓ Fixed Time Slot"), ("yes", "✓ Audio Guide"), ("no", "✕ Sells Out in Summer")],
    perks=["Area: <strong>Kossuth tér</strong>", "Tour: <strong>45 min</strong>"],
    desc="Hungarian Parliament entry with an audio guide, the first stop of day 1.",
)
C["basilica"] = dict(
    rank="📅 Day 1 · Late Morning", title="St Stephen's Basilica and the Dome", dur="About 1 Hour",
    place="Szent István tér", map="St Stephen's Basilica Budapest",
    psub="per adult • church entry, dome option",
    pills=[("🔭", "Climb the dome", "The dome terrace gives a <strong>360° view</strong> over Pest, the river and Buda Castle. It is the best view on the Pest side, and the reason to book."),
           ("🚶", "15 min from Parliament", "An easy walk from the Parliament through Szabadság tér. From the Basilica, the river and the Chain Bridge are about 10 minutes away."),
           ("🍰", "Lunch nearby", "The streets around the Basilica are full of cafés, so this is where day 1 lunch fits.")],
    pick="for the best view on the Pest side, between the Parliament and the river.",
    skip="if heights or stairs are a problem: the church itself is the free part to visit.",
    pros=["360° view from the dome", "Right on the walk from the Parliament to the river", "4.6 from 15,800+ reviews"],
    cons=["Stairs to the dome", "Busy at midday"],
    body="""<p>From the Parliament it is about a 15-minute walk to <strong>St Stephen's Basilica</strong>. Go inside, then take the dome: the terrace runs all the way round, so you see Pest's rooftops, the river and the castle on the hill you will climb tomorrow.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> for the view. <strong>Skip</strong> the dome if stairs are an issue and just see the church.</p>
<h3>Next Stop</h3>
<p>🍽️ Lunch around the Basilica, then a slow afternoon along the river to the Chain Bridge before the evening cruise.</p>""",
    qf_badge="Day 1", qf=[("Time needed", "About 1 hour"), ("Price", "From €12"), ("Highlight", "Dome terrace with a 360° view"),
        ("Walk", "About 15 minutes from the Parliament")],
    chips=[("yes", "✓ Best View in Pest"), ("yes", "✓ Free Cancellation"), ("no", "✕ Stairs to the Dome")],
    perks=["Area: <strong>District V</strong>", "Time: <strong>about 1 hour</strong>"],
    desc="St Stephen's Basilica entry with the dome view, day 1 of the itinerary.",
)
C["legenda"] = dict(
    rank="🏆 Day 1 · Evening (Must-Do)", title="Danube Night Cruise With Audio Guide &amp; Welcome Drink", dur="60-70 Minutes",
    place="Dock 7, Vigadó tér", map="Vigadó tér Dock 7 Budapest",
    psub="per adult • day or night sailings",
    tested_pop="<strong>I rode this cruise myself</strong> while testing 10 Budapest river cruises, and it is the one I would book. "
               "<a href=\"/best-budapest-river-cruise\">Why it won →</a>",
    pills=[("🌃", "Go after dark", "The point of a Danube cruise is the <strong>Parliament, Buda Castle and the bridges lit up</strong>. Take an evening departure, it is dark by about 16:00 in winter and after 20:30 in summer."),
           ("🎧", "30 languages", "Individual headsets with commentary in 30 languages, plus a welcome drink (champagne, wine, beer or soda)."),
           ("👶", "Kids under 10 free", "Free for children up to 9. Ages 10 to 14 pay €14 by day or €17.50 in the evening.")],
    pick="for the one hour that shows you the whole city lit up, at the best price of the big operators.",
    skip="if you want dinner on board: book a dinner cruise instead (see Day 3 evening).",
    pros=["Open top deck and a welcome drink", "Commentary in 30 languages", "Free cancellation up to 24 hours before"],
    cons=["Busy at the most popular evening slots", "No food on board"],
    body="""<p>End day 1 on the water. A <strong>one-hour evening cruise</strong> passes the lit-up Parliament you toured this morning, Buda Castle and every central bridge, and it is the single best hour in Budapest for a first visit.</p>
<p>I rode 10 Budapest cruises to rank them, and <strong>Legenda</strong> is the one I would book: an open top deck, a welcome drink and commentary in 30 languages on your own headset, from <strong>€20</strong>.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> for the classic night view. <strong>Skip it</strong> if you would rather eat on the river: the <a href="/best-dinner-cruise-budapest">best dinner cruise</a> fits day 3's evening better. Want drinks flowing? Compare the <a href="/unlimited-prosecco-cruises-budapest">unlimited prosecco cruises</a>.</p>
<h3>Meeting Point</h3>
<p>🗺️ Dock 7, Vigadó tér (Pest side), about 10 minutes on foot from the Basilica.<br/>🚇 Vörösmarty tér (M1) or tram 2.</p>""",
    qf_badge="Day 1 evening", qf=[("Duration", "60-70 minutes"), ("Pier", "Dock 7 (Vigadó tér), 1051 Budapest"),
        ("Included", "Welcome drink, audio guide in 30 languages"), ("Children", "Free up to 9 · ages 10-14 €14 day / €17.50 evening"),
        ("Cancellation", "Full refund up to 24 hours before")],
    chips=[("yes", "✓ Personally Tested"), ("yes", "✓ Welcome Drink"), ("yes", "✓ 30 Languages"), ("no", "✕ No Food")],
    perks=["Pier: <strong>Dock 7</strong>", "Duration: <strong>about 1 hour</strong>"],
    desc="One-hour Danube sightseeing cruise with a welcome drink and audio guide, the evening of day 1.",
)
C["food"] = dict(
    rank="📅 Day 2 · Morning", title="Market to Tavern Food Tour With Wine Tasting", dur="3 Hours",
    place="Central Market Hall", map="Central Market Hall Budapest",
    psub="per person • 3 hours",
    pills=[("🥘", "12+ tastings", "Cold cuts, pickles, goulash, lángos, chimney cake and a Hungarian dessert, starting in the <strong>Central Market Hall</strong> and ending in two local restaurants."),
           ("🍷", "Pálinka + wine tasting", "Homemade pálinka and a wine tasting are included (an alcohol-free substitute is available)."),
           ("🍽️", "This is lunch", "Book it and you do not need to plan lunch on day 2: it is a full meal spread over 3 hours.")],
    pick="to eat your way through Hungarian food with a local before you cross to Buda.",
    skip="if you only want a quick bite: walk the market hall yourself and buy lángos upstairs.",
    pros=["12+ tastings plus pálinka and wine", "Starts at the Central Market Hall, by Liberty Bridge", "4.9 from 679 reviews"],
    cons=["3 hours of the morning", "Hotel pickup not included"],
    body="""<p>Start day 2 hungry. The <strong>Central Market Hall</strong> is Budapest's best food stop, and the easiest way to understand it is with someone who eats there: Foodapest's tour starts in the hall and ends in two local restaurants, with <strong>12+ tastings</strong> and a wine tasting along the way.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> if food is part of why you came. <strong>Skip it</strong> if you prefer to graze on your own. Comparing options? See the <a href="/best-food-tours-budapest">9 best food tours in Budapest</a>.</p>""",
    qf_badge="Day 2 morning", qf=[("Duration", "3 hours"), ("Start", "Central Market Hall (2 start options)"),
        ("You eat", "Cold cuts, pickles, goulash, lángos, chimney cake, dessert"), ("Drinks", "Pálinka and a wine tasting"),
        ("Not included", "Hotel pickup, tips")],
    chips=[("yes", "✓ Lunch Covered"), ("yes", "✓ Wine Tasting"), ("yes", "✓ Free Cancellation")],
    perks=["Start: <strong>Central Market Hall</strong>", "Duration: <strong>3 hours</strong>"],
    desc="Food tour from the Central Market Hall to two local restaurants with a wine tasting, day 2 morning.",
)
C["castle"] = dict(
    rank="📅 Day 2 · Afternoon", title="Buda Castle District Walking Tour", dur="2 Hours",
    place="Trinity Square, Castle Hill", map="Szentháromság tér Budapest",
    psub="per person • daily 14:00 and 14:30",
    tested_pop="<strong>I took this walk myself.</strong> It covers the Royal Palace, Matthias Church and the Fisherman's Bastion ramparts in 2 hours. "
               "<a href=\"/best-walking-tours-budapest\">All 10 walking tours compared →</a>",
    pills=[("🕑", "14:00 or 14:30", "Daily in English at <strong>14:00 and 14:30</strong>, from Trinity Square in front of Matthias Church. It ends there too, ready for sunset at the Bastion."),
           ("🏰", "Palace, church, Bastion", "Royal Palace (Buda Castle), Matthias Church and the Fisherman's Bastion ramparts, with the stories you will not get from the signs."),
           ("🚌", "Bus 16 up the hill", "From Deák Ferenc tér, bus 16 crosses the Chain Bridge and climbs Castle Hill, the easy way up after the food tour.")],
    pick="for Castle Hill with context, ending right where you want to be at sunset.",
    skip="if you only want photos: the Bastion's lower terraces are free to walk.",
    pros=["Only €12 for 2 hours", "Ends at the Fisherman's Bastion for sunset", "4.6 from 2,400+ reviews"],
    cons=["Cobblestones and slopes", "Fixed afternoon start times"],
    body="""<p>Cross to Buda after lunch. <strong>Castle Hill</strong> is free to wander, but the 2-hour walk from Trinity Square explains what you are looking at: the <strong>Royal Palace</strong>, <strong>Matthias Church</strong> and the <strong>Fisherman's Bastion</strong>. I took it myself and it is the best €12 you will spend in Budapest.</p>
<p>The 14:00 start is the reason it fits here: you finish around 16:00 on the hill, and in the colder months that is <strong>sunset</strong>. Stay on the Bastion and watch the Parliament light up across the river.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> for your first afternoon in Buda. <strong>Skip it</strong> if you prefer to explore alone, and use the <a href="/best-walking-tours-budapest">walking tours comparison</a> for free tip-based options.</p>""",
    qf_badge="Day 2 afternoon", qf=[("Duration", "2 hours"), ("Price", "€12 per person"), ("Times", "Daily in English at 14:00 and 14:30"),
        ("Meeting point", "Szentháromság tér (Trinity Square, in front of Matthias Church)"),
        ("Sights", "Royal Palace, Matthias Church, Fisherman's Bastion ramparts")],
    chips=[("yes", "✓ Personally Tested"), ("yes", "✓ €12"), ("yes", "✓ Ends at Sunset Spot"), ("no", "✕ Cobblestones")],
    perks=["Start: <strong>Trinity Square</strong>", "Time: <strong>14:00</strong>"],
    desc="Two-hour Buda Castle District walking tour from Trinity Square, day 2 afternoon.",
)
C["crawl"] = dict(
    rank="🍻 Day 2 · Night", title="Ruin Bar Pub Crawl With Free Shots &amp; VIP Entry", dur="5 Hours",
    place="Erzsébet körút 36", map="Erzsébet körút 36 Budapest",
    psub="per person • starts 21:10, 21:40 or 22:20",
    pills=[("🥃", "A shot at every bar", "A welcome shot at every venue, VIP entry and drinking games across <strong>4 to 5 pubs, ruin bars and a club</strong>. Other drinks are paid at the bar."),
           ("🕘", "From 21:10", "Starts at 21:10, 21:40 or 22:20 from Erzsébet körút 36, in the Jewish Quarter where the ruin bars are."),
           ("🪪", "18+, bring ID", "You need a passport or ID card. Groups of 10 or more can book a private crawl.")],
    pick="if you want to see the ruin bars with a crowd and a guide who knows the doors.",
    skip="if you want a quiet drink: walk to Szimpla Kert yourself, entry is free.",
    pros=["From €2 with a shot at every venue", "Starts in the ruin bar district", "4.9 from 3,800+ reviews"],
    cons=["Drinks beyond the shots are extra", "A late, loud night"],
    body="""<p>Day 2 ends in the <strong>Jewish Quarter</strong>, Budapest's ruin bar district. You can walk to Szimpla Kert yourself (entry is free), but if you want a crowd and no planning, this crawl takes you through <strong>4 to 5 bars and a club</strong> with a shot at each, from about <strong>€2</strong>.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> for a big night out. <strong>Skip it</strong> for a calm drink. All the options, from €2 to a €25 crawl with 5 drinks, are in the <a href="/best-pub-crawls-budapest">pub crawl comparison</a>.</p>""",
    qf_badge="Day 2 night", qf=[("Duration", "5 or 5.5 hours"), ("Start", "21:10, 21:40 or 22:20"),
        ("Meeting point", "Erzsébet körút 36, 1073 Budapest"), ("Included", "Welcome shot at every venue, VIP entry, drinking games"),
        ("Age", "18+, bring ID")],
    chips=[("yes", "✓ From €2"), ("yes", "✓ Shot at Every Venue"), ("no", "✕ Other Drinks Extra")],
    perks=["Start: <strong>Erzsébet körút 36</strong>", "From: <strong>21:10</strong>"],
    desc="Budapest ruin bar pub crawl with a free shot at every venue, day 2 night.",
)
C["szechenyi"] = dict(
    rank="♨️ Day 3 · Morning", title="Széchenyi Thermal Bath Morning Pass", dur="Half Day", place="City Park",
    map="Széchenyi Thermal Bath Budapest", psub="per adult • entry 7:00 to 9:00, Mon to Thu",
    tested_pop="<strong>I have soaked at Széchenyi myself.</strong> All 5 ticket types are compared in my "
               "<a href=\"/szechenyi-baths-budapest\">Széchenyi tickets guide →</a>",
    pills=[("🕖", "In by 9:00 = €39", "The morning pass with a locker costs <strong>€39 if you enter 7:00 to 9:00, Monday to Thursday</strong>. "
            "The same weekday ticket is €46 after 9:00, and a private cabin €50. You can stay all day."),
           ("♨️", "Outdoor pools all year", "The outdoor thermal pool is 36 to 38 °C, open in winter too, so the cold-morning steam is part of the fun."),
           ("🚇", "M1 to the door", "Metro M1 to Széchenyi fürdő, the station is at the entrance. Bring a swimsuit, flip-flops and a towel.")],
    pick="for the classic Budapest bath, at the cheapest price and before the crowds.",
    skip="on a Friday to Sunday morning: the €39 early slot is Monday to Thursday only.",
    pros=["€7 cheaper before 9:00", "Outdoor pools at 36 to 38 °C all year", "Free cancellation up to 24 hours before"],
    cons=["Early start after a pub crawl night", "Busy by late morning"],
    body="""<p>Day 3 is the slow one, and it starts early on purpose. At <strong>Széchenyi</strong> the morning pass costs <strong>€39 if you are through the gate by 9:00</strong> (Monday to Thursday), against €46 for the same ticket later, and the outdoor pools are at their emptiest.</p>
<p>I've been to Széchenyi myself. Stay as long as you like, then walk out into <strong>City Park</strong>: Vajdahunyad Castle is next door and free, and Heroes' Square is at the end of the park.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> for your first Budapest bath. <strong>Skip it</strong> if you want something smaller and older: <a href="/rudas-baths-budapest">Rudas</a> has a rooftop pool and night bathing on Fridays and Saturdays. All six are compared in the <a href="/thermal-baths-budapest">thermal baths guide</a>.</p>""",
    qf_badge="Day 3 morning", qf=[("Ticket", "Morning pass €39 (entry 7:00-9:00, Mon-Thu) · weekday pass €46 · with cabin €50"),
        ("Pools", "18 pools, outdoor thermal pool 36-38 °C"), ("Metro", "M1 Széchenyi fürdő"),
        ("Bring", "Swimsuit, flip-flops, towel")],
    chips=[("yes", "✓ Personally Tested"), ("yes", "✓ €39 Before 9:00"), ("yes", "✓ Free Cancellation"), ("no", "✕ Mon-Thu Only")],
    perks=["Area: <strong>City Park</strong>", "Entry: <strong>7:00-9:00</strong>"],
    desc="Széchenyi Thermal Bath morning pass, entry before 9:00, day 3 of the itinerary.",
)
C["daytrip"] = dict(
    rank="🌲 Day 4 · Full Day", title="Danube Bend Day Trip: Visegrád and Szentendre", dur="8-9 Hours",
    place="Batthyány tér", map="Batthyány tér Budapest",
    psub="per person • 8-9 hours",
    pills=[("🏰", "Visegrád + Szentendre", "Visegrád's hilltop castle over the river bend and the painters' village of Szentendre, the classic Danube Bend pair."),
           ("🚐", "Small group", "A small-group trip from Batthyány tér on the Buda side, back in the early evening."),
           ("📊", "Compared 13 day trips", "Day trips were compared on hours at the destination against hours on the road. <a href=\"/best-day-trips-from-budapest\">See all 13 →</a>")],
    pick="for a fourth day out of the city, with the best view of the Danube anywhere.",
    skip="if you only have 3 days: the city itself is the better use of them.",
    pros=["Visegrád castle and Szentendre in one day", "4.9 from 37 reviews", "Meeting point on the Buda side"],
    cons=["A full day, 8-9 hours", "Small group, so it fills up"],
    body="""<p>With a fourth day, leave the city. Upstream the Danube turns sharply between wooded hills at <strong>Visegrád</strong>, and the view from the castle over the bend is the best river view in Hungary. This trip pairs it with <strong>Szentendre</strong>, a small baroque town of galleries and cobbled lanes.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> if you have a full spare day. <strong>Skip it</strong> on a 3-day trip. Lake Balaton, Eger and Vienna are compared in the <a href="/best-day-trips-from-budapest">13 best day trips from Budapest</a>.</p>""",
    qf_badge="Day 4", qf=[("Duration", "8-9 hours"), ("Price", "From €96"), ("Meeting point", "Batthyány tér (Buda side)"),
        ("Destinations", "Visegrád and Szentendre")],
    chips=[("yes", "✓ Small Group"), ("yes", "✓ Free Cancellation"), ("no", "✕ Full Day")],
    perks=["Start: <strong>Batthyány tér</strong>", "Duration: <strong>8-9 hours</strong>"],
    desc="Danube Bend day trip to Visegrád and Szentendre from Budapest, day 4 of the itinerary.",
)

# ---------------------------------------------------------------- guide sections
PLAN_H = "The 3-Day Budapest Itinerary at a Glance"
PLAN_COLS = ["Day", "Morning", "Afternoon", "Evening", "To book"]
PLAN_ROWS = [
    ["Day 1: Pest", f'<a href="{A("parliament")}">Parliament tour</a> (9:00 or 10:00)', f'<a href="{A("basilica")}">Basilica dome</a>, lunch, riverside to the Chain Bridge', f'<a href="{A("legenda")}">Night cruise</a> from Vigadó tér', "€75"],
    ["Day 2: Buda", f'<a href="{A("food")}">Food tour</a> from the Central Market Hall', f'<a href="{A("castle")}">Castle walk</a> at 14:00, sunset on the Bastion', f'<a href="{A("crawl")}">Ruin bars</a> from 21:10', "€76"],
    ["Day 3: Baths", f'<a href="{A("szechenyi")}">Széchenyi</a> by 9:00', "City Park, Vajdahunyad Castle, Heroes' Square, Andrássy út", 'Free, or a <a href="/best-dinner-cruise-budapest">dinner cruise</a>', "€39"],
]
PLAN_NOTE = "Per person, for the bookings in this plan only (no food, hotel or transport). Total: about €190 for 3 days."

DAYS = [
    ("day-1", "Day 1: Pest, the Parliament and the River After Dark",
     f"""<p><strong>Morning.</strong> Be at the Parliament visitor centre 15 minutes before a <a href="{A("parliament")}">9:00 or 10:00 tour</a>. It lasts 45 minutes. Walk round to the riverside behind it for the view across to Buda.</p>
<p><strong>Late morning.</strong> About 15 minutes on foot through Szabadság tér brings you to <a href="{A("basilica")}">St Stephen's Basilica</a>. Climb the dome for the 360° view, then have lunch in the streets around it.</p>
<p><strong>Afternoon.</strong> Walk down to the river and along the Pest embankment to the Chain Bridge. Leave the castle for tomorrow; today you are looking at it.</p>
<p><strong>Evening.</strong> From Dock 7 at Vigadó tér, take the <a href="{A("legenda")}">one-hour night cruise</a>. You pass the Parliament lit up, then Buda Castle and the bridges. It is the best hour of the trip.</p>"""),
    ("day-2", "Day 2: Market, Castle Hill and the Ruin Bars",
     f"""<p><strong>Morning.</strong> Go hungry to the Central Market Hall by Liberty Bridge for the <a href="{A("food")}">market-to-tavern food tour</a>: 3 hours, 12+ tastings and a wine tasting. It covers lunch.</p>
<p><strong>Afternoon.</strong> Bus 16 from Deák Ferenc tér crosses the Chain Bridge and climbs Castle Hill. Be at Trinity Square for the <a href="{A("castle")}">14:00 castle walk</a>: the Royal Palace, Matthias Church and the Fisherman's Bastion in 2 hours.</p>
<p><strong>Sunset.</strong> Stay on the Fisherman's Bastion as the Parliament lights up across the river. The lower terraces are free.</p>
<p><strong>Night.</strong> Back in Pest, the <a href="{A("crawl")}">ruin bar crawl</a> starts at 21:10 from Erzsébet körút 36. Prefer a quiet drink? Szimpla Kert is free to walk into.</p>"""),
    ("day-3", "Day 3: Thermal Baths and City Park",
     f"""<p><strong>Morning.</strong> Take the M1 to Széchenyi fürdő and be through the gate by 9:00 for the <a href="{A("szechenyi")}">€39 morning pass</a> (Monday to Thursday). Soak as long as you like.</p>
<p><strong>Afternoon.</strong> Walk out into City Park: Vajdahunyad Castle is next door and free, Heroes' Square is at the end of the park, and Andrássy út leads you back towards the centre past the Opera.</p>
<p><strong>Evening.</strong> Your last night is the one for a long dinner. Book the <a href="/best-dinner-cruise-budapest">best dinner cruise</a> for a 4-course meal on the river, or keep it free and eat in the Jewish Quarter.</p>"""),
]

TWO_H = "If You Only Have 2 Days in Budapest"
TWO_P = f"""<p>Keep day 1 exactly as it is: <a href="{A("parliament")}">Parliament</a>, <a href="{A("basilica")}">Basilica</a> and the <a href="{A("legenda")}">night cruise</a>. On day 2, start at <a href="{A("szechenyi")}">Széchenyi before 9:00</a>, take the M1 back to the centre and bus 16 up to Castle Hill for the <a href="{A("castle")}">14:00 castle walk</a>, then end in the ruin bars. You lose the food tour and the slow afternoon in City Park, and that is all. Bookings: about €130 per person.</p>"""

FOUR_H = "Day 4: The Danube Bend"
FOUR_P = f"""<p>A fourth day is best spent outside the city. The <a href="{A("daytrip")}">Danube Bend day trip</a> takes you to Visegrád castle above the river's sharp turn and to Szentendre's galleries and lanes, 8 to 9 hours from Batthyány tér for €96. If you would rather stay in town, add <a href="/rudas-baths-budapest">Rudas</a> for its rooftop pool, or plan around the <a href="/things-to-do-budapest-december">December</a> and <a href="/things-to-do-budapest-november">November</a> events.</p>"""

PRACTICAL_H = "Before You Go: Getting In, Where to Stay, What It Costs"
PRACTICAL = [
    ("Getting in from the airport", 'The 100E express bus costs 2,200 HUF (about €6) and runs to the centre around the clock. All the options are in the <a href="/budapest-airport-to-city-center">airport to city centre guide</a>.'),
    ("Where to stay", 'Stay in Pest, in District V or VII: every day of this plan starts within walking distance or one metro stop. On a budget, see the <a href="/best-hostels-budapest">best hostels in Budapest</a>.'),
    ("Getting around", "Walk inside the centre. For Castle Hill take bus 16, for Széchenyi the M1, and for the river views tram 2, which runs along the Pest embankment."),
    ("Budapest Card", 'Whether it pays off depends on your exact plan. Check it against this itinerary with the <a href="/budapest-card-is-it-worth-it">Budapest Card calculator</a>, which covers all 94 sights.'),
    ("Visiting in winter", 'Add the <a href="/budapest-christmas-markets">Christmas markets</a> to any evening from late November, and plan the night cruise early: it is dark by about 16:00.'),
    ("Longer river cruise", 'Starting or ending a longer river cruise here? The 15-day Danube and Rhine sailings are compared in <a href="/budapest-amsterdam-river-cruises">Budapest to Amsterdam river cruises</a>.'),
]

FAQ = [
    ("Is 3 days enough for Budapest?",
     "Yes, for a first visit. Three days covers Pest and the Parliament, Buda's Castle Hill, a night cruise, a thermal bath and the ruin bars without rushing. With a fourth day, add a day trip to the Danube Bend."),
    ("What is the best order to see Budapest?",
     "Pest first, Buda second, baths last. Day 1 covers the Parliament, the Basilica and a night cruise; day 2 a food tour, Castle Hill at sunset and the ruin bars; day 3 Széchenyi at opening, when the morning pass is €39 instead of €46."),
    ("How much does 3 days in Budapest cost?",
     "The bookings in this plan come to about €190 per person: Parliament (€43), the Basilica (€12), a night cruise (€20), a food tour (€62), a castle walk (€12), a pub crawl (€2) and Széchenyi (€39). Food, drinks, hotel and transport are on top."),
    ("Can you see Budapest in 2 days?",
     "Yes. Day 1: Parliament, the Basilica and a night cruise. Day 2: Széchenyi before 9:00, the 14:00 Castle Hill walk and the ruin bars in the evening. Bookings come to about €130 per person."),
    ("Should I stay in Buda or Pest?",
     "Pest, in District V or VII. It is flatter, has most restaurants and bars, and every day of this itinerary starts within walking distance or one metro stop."),
    ("Do I need to book the Parliament in advance?",
     "Yes. You can only go inside on a 45-minute guided tour, and English slots sell out, often days ahead from May to September. Official tickets cost HUF 7,000 for EU/EEA adults and HUF 14,000 for everyone else."),
]

METHOD_H = "How I Planned This Itinerary"
METHOD = ("I live in Budapest and built this plan from the comparisons on this site: 10 river cruises, 6 thermal baths, "
          "10 walking tours, 9 food tours, 6 pub crawls and 13 day trips. For each day I picked the booking that fits the timing best, "
          "not the most expensive one, and checked opening hours, start times and meeting points so the days connect without backtracking. "
          "Three of the eight bookings (the night cruise, the castle walk and Széchenyi) I have done myself.")
