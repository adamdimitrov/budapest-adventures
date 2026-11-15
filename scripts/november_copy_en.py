# -*- coding: utf-8 -*-
"""EN copy for /things-to-do-budapest-november. Facts: scripts/november_data.py. No em dashes."""

LANG = "en"
SLUG = "things-to-do-budapest-november"
PATH = "/things-to-do-budapest-november"
SLUG_CSS = "things-to-do-budapest-november"
TITLE_TAG = "Things to Do in Budapest in November 2026 (Local's Picks)"
H1 = "8 Best Things to Do in Budapest in November 2026"
H1_MUTED = "(Night Cruises, Hot Pools and Market Openings)"
CRUMB = "Things to Do in Budapest in November"
META = ("What to do in Budapest in November 2026: night cruises from 16:20, hot outdoor pools, "
        "a vampire night walk, food tours and the Christmas market opening dates. From €12.")
KICKER = "November 2026 Planner"
AUTHOR_ROLE = "8 Picks • 7 Personally Tested • Dates &amp; Daylight"
UPDATED = "Last updated"
UPDATED_DATE = "Nov 15, 2026"

UI = dict(
    check="Check Availability →", book_site="Check Availability →", read="Read Review ↓",
    free_cxl="Free cancellation", instant="Instant QR", cxl24="Free 24h Cancellation",
    direct_trust="Booked on the operator's own site",
    reviews_one="{n} reviews · 1 site", reviews_many="{n} reviews · {k} sites",
    rating_on="Rating on 1 booking site", rating_many="Ratings on {k} booking sites, each for this exact product",
    no_rating="New listing", tested="✓ Personally Tested",
    pick="✓ Pick it", skip="✕ Skip it", pros="Pros:", cons="Cons:", summary="Summary &amp; Review", overview="Overview",
    live="Official Tickets &amp; Live Availability", book_dates="Check Dates &amp; Book Tickets",
    best_price="Best Price Guaranteed • Instant Confirmation", qf="Quick Facts",
    perk_qr="Instant Smartphone QR Voucher", perk_refund="Full Refund up to 24h Before",
    perk_direct="Booked directly with the operator",
    breakdown_h="Detailed Breakdown: 8 Things to Do in Budapest in November",
    breakdown_sub="Ranked • All reviews open by default • Click to collapse/expand",
    expand="Expand All", collapse="Collapse All",
    contents="Contents (8)", all_items="All 8 November Picks", jump="Jump to a November Pick",
    toc_deck="Top 8 November Picks", toc_breakdown="Detailed Breakdown (8 Picks)",
    filter_all="All", filter_label="Show:",
    filters=[("river", "On the Danube"), ("bath", "Thermal baths"), ("dark", "After dark"),
             ("food", "Food &amp; dinner"), ("u40", "Under €40")],
    per_person="per person", home="Home", by="By", founder="Founder &amp; Budapest Local",
    faq_h="Frequently Asked Questions", from_price="From €{p}",
)

# ---------------------------------------------------------------- cards
C = {}
C["legenda-evening"] = dict(
    rank="🏆 #1 Best November Evening", title="Danube Legend Evening Cruise With Welcome Drink",
    dur="1 Hour", place="Dock 7, Vigadó tér", map="Legenda City Cruises Dock 7 Budapest",
    psub="per adult • every 20 min from 16:20",
    tested_pop="<strong>I rode this cruise myself.</strong> Most of the photos are my own, taken on Legenda's boats.",
    pills=[("🕒", "Every 20 min · 16:20 to 21:00",
            "<strong>Until 22 November:</strong> every 20 minutes from 16:20 to 21:00. <strong>From 23 November:</strong> an extra 15:40 sailing, then every 20 minutes from 16:20 to 21:00. About 1 hour. From Legenda's 2026 timetable."),
           ("🌆", "Lit up from the first sailing", "Sunset is at 16:07 on 15 November and 15:55 on 30 November, so even the 16:20 boat sails past a lit Parliament and Castle."),
           ("🥂", "1 drink included", "One glass of champagne, wine, beer, a soft drink or mineral water. Free wifi on board."),
           ("🎧", "30-language audio guide", "Film and audio guide on your own headset in 30 languages, including English, German, Spanish, Italian, French and Hungarian."),
           ("🎟️", "€25 · kids under 10 free", "€25 adult, €22.50 student, €17.50 children 10 to 14, free under 10.")],
    pick="for the lit-up Danube in one hour, any November evening, with the clearest audio guide on the river.",
    skip="on a tight budget: €25 is more than most sightseeing boats charge.",
    pros=["Sails every 20 minutes from 16:20, so it fits any evening plan",
          "The whole cruise is in the dark in November: every sight is lit",
          "Covered floating dock with restrooms, useful on a cold, wet night"],
    cons=["Pricier than the no-frills boats", "You can't choose which Legenda boat you get"],
    body="""<p>November is the month the Danube cruise gets better, not worse. <strong>The sun sets at 16:07 in mid-November</strong>, so Legenda's first evening boat at <strong>16:20</strong> already sails past a lit Parliament and Buda Castle, and you are back on the embankment before 17:30 with the whole evening ahead.</p>
<p>I've ridden this cruise myself. It is a one-hour loop with a welcome drink and the best audio guide on the river: a film and commentary on your own headset in 30 languages. From <strong>23 November</strong> Legenda adds a <strong>15:40</strong> sailing that catches the last light.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> as your first evening in Budapest: it shows you the city lit up in an hour and leaves the night free for dinner.</p>
<p><strong>Skip it</strong> if you want to eat on the water: book <a href="#item-3-legenda-candlelit-dinner">Legenda's candlelit dinner</a> instead, from the same dock. All night cruises side by side: <a href="/best-night-cruises-budapest">best night cruises in Budapest</a>.</p>
<h3>Meeting Point</h3>
<p>🗺️ <strong>Meeting Point: </strong>Legenda, Jane Haining rakpart 7, Dock 7 (Vigadó tér), Pest side.<br/>🚋 <strong>Public Transport:</strong> Tram 2 to Vigadó tér, or M1 to Vörösmarty tér.</p>""",
    qf_badge="Danube by night", qf=[("Departures", "Until 22 Nov: every 20 min 16:20 to 21:00 · from 23 Nov: also 15:40"), ("Duration", "About 1 hour"),
        ("Price", "€25 adult · €22.50 student · €17.50 child 10 to 14 · free under 10"), ("Included", "1 drink, 30-language audio guide, wifi"),
        ("Pier", "Dock 7, Vigadó tér")],
    chips=[("yes", "✓ Dark From the First Sailing"), ("yes", "✓ Drink Included"), ("yes", "✓ 30 Languages"), ("no", "✕ Not the Cheapest")],
    perks=["Pier: <strong>Dock 7</strong>", "First evening boat: <strong>16:20</strong>"],
    desc="One-hour evening Danube cruise with a welcome drink and 30-language audio guide, every 20 minutes from 16:20.",
)
C["szechenyi"] = dict(
    rank="#2 Best Bath in the Cold", title="Széchenyi Thermal Bath", dur="Half Day", place="City Park",
    map="Széchenyi Thermal Bath Budapest", psub="per adult • Mon to Thu morning pass",
    tested_pop="<strong>I visited Széchenyi myself.</strong> Most of the photos on this card are my own.",
    pills=[("🕒", "Open to 22:00 on Fridays", "<strong>Mon to Thu</strong> 7:00 to 20:00, <strong>Fri</strong> 7:00 to 22:00, <strong>Sat and Sun</strong> 8:00 to 20:00."),
           ("♨️", "Outdoor pools at 36-38 °C", "Outdoor thermal pool 36 to 38 °C, adventure pool 32 to 34 °C and swimming pool 26 to 28 °C, all open in November."),
           ("🎟️", "Morning pass €39", "Morning pass with locker, entry 7:00 to 9:00, Mon to Thu: €39. Weekday pass €46, with a private cabin €50. "
            "At the desk: 13,200 HUF Mon to Thu, 14,800 HUF Fri to Sun."),
           ("🎉", "Sparty on Saturdays", "The Saturday night pool party starts at 21:30. 18+ only, and the ticket is non-refundable.")],
    pick="for the November picture of Budapest: hot outdoor pools steaming in cold air.",
    skip="if you hate crowds: weekend afternoons are busy, so come at opening on a weekday.",
    pros=["Three outdoor pools open in November, the hottest at 36 to 38 °C",
          "Open until 22:00 on Fridays, after dark from 16:00", "Metro stop at the entrance"],
    cons=["The busiest bath in town", "Booking-site tickets cost more than the desk"],
    body="""<p>Cold air is what makes Széchenyi. In November it is around <strong>9 °C by day and 3 °C at night</strong>, and the outdoor thermal pool is <strong>36 to 38 °C</strong>, so the steam rises off the water under the yellow neo-baroque facade. Come at about 15:30 and you swim from daylight into dusk.</p>
<p>I've been to Széchenyi myself. On <strong>Fridays it stays open until 22:00</strong>, the best night of the week for a bath after dark.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> for your first Budapest bath. The <strong>€39 morning pass</strong> (Mon to Thu, entry by 9:00) is the best value.</p>
<p><strong>Skip it</strong> if you want something calmer and older: book <a href="#item-4-rudas-thermal-bath">Rudas</a>. All six baths compared: <a href="/thermal-baths-budapest">best thermal baths in Budapest</a>.</p>
<h3>Getting There</h3>
<p>🚇 <strong>Metro:</strong> M1 to Széchenyi fürdő, the station is at the entrance.<br/>🎒 <strong>Bring:</strong> Swimsuit, flip-flops and a towel. Walk fast from the indoor halls to the outdoor pools.</p>""",
    qf_badge="City Park", qf=[("Hours", "Mon to Thu 7:00 to 20:00 · Fri to 22:00 · Sat and Sun 8:00 to 20:00"),
        ("Ticket", "Morning pass €39 · weekday pass €46 · with cabin €50"),
        ("Outdoor Pools", "36-38 °C thermal · 32-34 °C adventure · 26-28 °C swimming"), ("Metro", "M1 Széchenyi fürdő")],
    chips=[("yes", "✓ Outdoor Pools in November"), ("yes", "✓ Open to 22:00 Fri"), ("yes", "✓ Free Cancellation"), ("no", "✕ Crowded Weekends")],
    perks=["Area: <strong>City Park</strong>", "Pools: <strong>3 outdoor</strong>"],
    desc="Ticket to Széchenyi Thermal Bath with outdoor thermal pools at 36 to 38 °C, open all autumn and winter.",
)
C["legenda-dinner"] = dict(
    rank="#3 Best Dinner Cruise", title="Candlelit 4-Course Dinner Cruise With Live Music",
    dur="2.5 Hours", place="Dock 7, Vigadó tér", map="Legenda City Cruises Dock 7 Budapest",
    psub="per adult • daily at 19:00",
    tested_pop="<strong>I took this cruise myself.</strong> The photos and video in my full review are my own.",
    pills=[("🕒", "Daily · 19:00", "Departs <strong>every evening at 19:00</strong> in November. About 2.5 hours on Legenda's glass-roofed panorama boat."),
           ("🍽️", "4 courses, à la carte", "You choose every course at your table from the menu. Children 3 to 12 get a 3-course kids' menu for €84."),
           ("🎶", "Live music", "Live music all evening, a welcome drink and candlelit tables."),
           ("🍷", "Drinks extra", "Apart from the welcome drink, drinks are paid on board.")],
    pick="for a romantic, served dinner with the lit-up Parliament from your table.",
    skip="if you want drinks included in the price: they are paid on board.",
    pros=["Served 4-course dinner, ordered at the table, not a buffet",
          "Glass-roofed boat: warm inside, view from every seat",
          "Sails every evening at 19:00"],
    cons=["€110 per adult", "Drinks are extra"],
    body="""<p>A November evening is long: dark before 16:30, and nothing outdoors tempts you after 19:00. That is the case for a <strong>2.5-hour dinner on the Danube</strong>, and Legenda's candlelit cruise is the one I'd book. It is a <strong>served 4-course à la carte dinner</strong> with live music on a glass-roofed boat, so you stay warm and still see the lit Parliament, Castle and bridges the whole way.</p>
<p>I've taken this cruise myself. What sets it apart from the buffet boats is the pace: you order each course at the table and nobody rushes you.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> for a date night or an anniversary. Kids 3 to 12 eat from a 3-course menu for €84.</p>
<p><strong>Skip it</strong> if €110 is more than you want to spend: <a href="#item-6-silverline-dinner-cruise">Silverline's 4-course dinner</a> starts at €77. All six compared: <a href="/best-dinner-cruises-budapest">best dinner cruises in Budapest</a>.</p>
<h3>Meeting Point</h3>
<p>🗺️ <strong>Meeting Point: </strong>Legenda, Dock 7, Vigadó tér (Pest side).<br/>🚋 <strong>Public Transport:</strong> Tram 2 to Vigadó tér, or M1 to Vörösmarty tér.</p>""",
    qf_badge="Danube dinner", qf=[("Departure", "Daily at 19:00"), ("Duration", "About 2.5 hours"),
        ("Price", "€110 adult · €84 children 3 to 12"), ("Food", "4-course à la carte dinner (kids: 3 courses)"),
        ("Included", "Cruise, welcome drink, live music, dinner"), ("Not Included", "Other drinks"), ("Pier", "Dock 7, Vigadó tér")],
    chips=[("yes", "✓ Served at Your Table"), ("yes", "✓ Live Music"), ("yes", "✓ Heated Glass Roof"), ("no", "✕ Drinks Extra")],
    perks=["Pier: <strong>Dock 7</strong>", "Departure: <strong>19:00</strong>"],
    desc="Candlelit 4-course à la carte dinner cruise with live music on the Danube, daily at 19:00.",
)
C["rudas"] = dict(
    rank="#4 Best Night Bath", title="Rudas Thermal Bath With 3-Course Meal", dur="3-4 Hours", place="Elizabeth Bridge",
    map="Rudas Thermal Bath Budapest", psub="per adult • bath + 3-course meal",
    tested_pop="<strong>I visited Rudas myself.</strong> I've sat in the rooftop pool and the Turkish bath described here.",
    pills=[("🌙", "Night bathing Fri and Sat", "<strong>Night bathing</strong> on Friday and Saturday from 22:00 to 3:00 (online tickets only, sold separately). "
            "Wellness hours: Mon 6:00 to 22:00, Tue to Sun 6:00 to 20:00."),
           ("🏊", "Rooftop pool 36 °C", "A 36 °C panorama pool on the roof with a Danube view, plus six Turkish pools from 16 to 42 °C under a 16th-century dome."),
           ("🍽️", "3-course meal included", "This ticket bundles a day pass with a 3-course meal at Rudas Bistro: wellness + coffee €74.99, wellness + wine €76.99, Turkish bath + wellness €84.99."),
           ("🚻", "Check the day", "The Turkish bath has single-sex days: men only Mon, Thu and Fri 6:00 to 10:45 and all Wed; women only Tue. Mixed on weekends."),
           ("🔞", "14+ only", "Children under 14 are not admitted, and the bath has no step-free access at the moment.")],
    pick="for a hot rooftop pool over the Danube on a dark November afternoon, and the Ottoman dome below it.",
    skip="with kids under 14, or if you want a plain bath ticket without the meal.",
    pros=["Rooftop hot pool with a river view, best after dark", "16th-century Turkish bath under a stone dome", "Night bathing on Friday and Saturday"],
    cons=["Single-sex days in the Turkish part", "No children under 14"],
    body="""<p>Rudas is my pick for a grey November day. The <strong>rooftop pool is 36 °C</strong> and looks across the Danube to the Parliament and the bridges, which light up just after 16:00. Downstairs, the <strong>Turkish bath under a 16th-century dome</strong> has six pools from 16 to 42 °C. On <strong>Friday and Saturday it reopens for night bathing from 22:00 to 3:00</strong>.</p>
<p>I've been to Rudas myself. Go in mid-afternoon, watch the lights come on from the roof, then eat the 3-course meal that comes with this ticket.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> if you've done Széchenyi, or want a smaller, older bath with the best view in town.</p>
<p><strong>Skip it</strong> if you're a mixed couple on a single-sex day for the Turkish part (check the pill above), or with children.</p>
<h3>Getting There</h3>
<p>🚋 <strong>Public Transport:</strong> Tram 19 or 41, or bus 7, to Rudas fürdő at the Buda end of Elizabeth Bridge.</p>""",
    qf_badge="Elizabeth Bridge", qf=[("Hours", "Wellness Mon 6:00 to 22:00, Tue to Sun 6:00 to 20:00"),
        ("Night Bathing", "Fri and Sat 22:00 to 3:00 (separate online ticket)"), ("Ticket", "Day pass + 3-course meal from €74.99"),
        ("Rooftop Pool", "36 °C"), ("Age", "14+"), ("Transport", "Tram 19, 41 · bus 7")],
    chips=[("yes", "✓ Rooftop Hot Pool"), ("yes", "✓ Meal Included"), ("yes", "✓ Night Bathing Weekends"), ("no", "✕ Single-Sex Days")],
    perks=["Area: <strong>Elizabeth Bridge</strong>", "Rooftop: <strong>36 °C</strong>"],
    desc="Rudas Thermal Bath day pass with a 3-course meal, rooftop panorama pool and Ottoman Turkish bath.",
)
C["vampire"] = dict(
    rank="#5 Best After-Dark Walk", title="Buda Castle Vampires and Myths Night Walk", dur="2 Hours", place="Clark Ádám tér",
    map="Clark Adam ter Budapest", psub="per person • starts 20:00",
    tested_pop="<strong>I took this tour myself</strong>, on the 20:00 English walk.",
    pills=[("🕗", "Starts at 20:00", "On Saturday 21 November the English walk starts at <strong>20:00</strong>. About 2 hours."),
           ("🧛", "Folklore, not dates", "About ten stories of vampires, ghosts and Eastern European myths, told around the Castle District courtyards, Matthias Church and Fisherman's Bastion."),
           ("🪜", "Uphill start", "A 5 to 10 minute stair climb up Castle Hill from Clark Ádám tér. The funicular is an option for €10 extra."),
           ("👥", "Groups of 20 to 25", "My group was 20 to 25 people. English, German and Spanish walks are listed. Ages 10+.")],
    pick="for a November evening outdoors that is better in the dark: Castle Hill by lamplight with a storyteller.",
    skip="if you want history and dates: this is folklore and theatre.",
    pros=["Made for the dark: the Castle District is empty and lit at night", "€20 for 2 hours with a storyteller guide", "Rated 4.6 by more than 4,600 guests"],
    cons=["Stairs at the start", "The second half can feel repetitive"],
    body="""<p>Most walking tours lose to November: by 16:00 it is dark and cold. This one is built for it. It starts at <strong>20:00 at Clark Ádám tér</strong>, climbs Castle Hill and spends <strong>two hours on vampire, ghost and folk tales</strong> in the empty, lamp-lit courtyards around Matthias Church and Fisherman's Bastion.</p>
<p>I've done this walk myself. Our guide had a background in improv theatre, and the first half was gripping. After six or seven tales it got a little repetitive, but the setting carries it.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> for the night after your cruise, or with teenagers (ages 10+).</p>
<p><strong>Skip it</strong> if you want facts and dates: the <a href="#item-8-buda-castle-walking-tour">morning Castle District walk</a> covers the history for €12. More walks compared: <a href="/best-walking-tours-budapest">best walking tours in Budapest</a>.</p>
<h3>Meeting Point</h3>
<p>🗺️ <strong>Meeting Point: </strong>Clark Ádám tér, next to the Kilometer Zero stone by the funicular.<br/>🚌 <strong>Public Transport:</strong> Bus 16, 105 or 178 from Deák Ferenc tér or Erzsébet tér, or walk across the Chain Bridge.</p>""",
    qf_badge="Castle District", qf=[("Start", "20:00 (English, Sat 21 Nov)"), ("Duration", "About 2 hours"), ("Price", "From €20 / person"),
        ("Route", "Castle District courtyards, Matthias Church, Fisherman's Bastion"), ("Age", "10+"),
        ("Meeting Point", "Clark Ádám tér, by Kilometer Zero")],
    chips=[("yes", "✓ Built for the Dark"), ("yes", "✓ Under €40"), ("yes", "✓ Free Cancellation"), ("no", "✕ Stairs at the Start")],
    perks=["Start: <strong>Clark Ádám tér</strong>", "Time: <strong>20:00</strong>"],
    desc="Two-hour night walk through Buda Castle District with vampire and folk tales, from €20.",
)
C["silverline"] = dict(
    rank="#6 Best Value Dinner Cruise", title="Dinner &amp; Lights 4-Course Dinner Cruise", dur="2 Hours", place="Dock 11",
    map="Silverline Cruises Dock 11 Budapest", psub="per adult • 19:00",
    tested_pop="<strong>I took Silverline's dinner cruise myself</strong>, from Dock 11.",
    pills=[("🕒", "19:00 · 2 hours", "Departs at <strong>19:00</strong>, about 2 hours. Boarding opens 45 minutes before; arrive 30 minutes early."),
           ("🍽️", "4-course served menu", "1 starter, 2 soups, 4 mains (walnut cod, pork tenderloin, curry lamb chops or a vegetarian sweet potato boat) and 3 desserts."),
           ("🎭", "Show option", "Dinner &amp; Lights has background music. The same boat and menu with a folk and operetta show costs from €91."),
           ("🪟", "Window seat +€15", "A guaranteed window seat costs €15 more per person. One welcome drink is included; other drinks are paid on board."),
           ("🌱", "Diet requests", "A vegetarian main is on the menu. Gluten-free, lactose-free and vegan dishes on request in advance.")],
    pick="for a served 4-course dinner on the Danube at €33 less than Legenda.",
    skip="if you want a window guaranteed at the base price: it is €15 extra.",
    pros=["4-course served dinner from €77", "Vegetarian main, and vegan on request", "Option to add a folk and operetta show"],
    cons=["Window seat costs extra", "Drinks beyond the welcome drink are extra"],
    body="""<p>If the dinner cruise is the plan but €110 feels steep, this is the swap. Silverline's <strong>Dinner &amp; Lights</strong> is a <strong>served 4-course dinner</strong> (walnut cod, pork tenderloin, lamb chops or a vegetarian main) on a <strong>2-hour cruise at 19:00</strong>, from <strong>€77</strong>.</p>
<p>I've done Silverline's dinner cruise myself. Pay the <strong>€15 for a window seat</strong>: in November you spend the whole cruise in the dark, and the view is half of what you're paying for.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> for a dinner cruise on a mid-range budget, or with a vegetarian in the group.</p>
<p><strong>Skip it</strong> for a special occasion: <a href="#item-3-legenda-candlelit-dinner">Legenda's candlelit cruise</a> is the more polished evening.</p>
<h3>Meeting Point</h3>
<p>🗺️ <strong>Meeting Point: </strong>Silverline, Jane Haining rakpart, Dock 11, by Elizabeth Bridge (Pest side).<br/>🚋 <strong>Public Transport:</strong> Tram 2, or M1 to Vörösmarty tér.</p>""",
    qf_badge="Danube dinner", qf=[("Departure", "19:00"), ("Duration", "About 2 hours"), ("Price", "From €77 · window seat +€15"),
        ("Food", "4-course served menu"), ("Included", "Cruise, dinner, welcome drink"), ("Pier", "Dock 11, Jane Haining rakpart")],
    chips=[("yes", "✓ Served 4 Courses"), ("yes", "✓ Vegetarian Main"), ("no", "✕ Window Seat Extra")],
    perks=["Pier: <strong>Dock 11</strong>", "Departure: <strong>19:00</strong>"],
    desc="Two-hour 4-course dinner cruise on the Danube at 19:00 from €77.",
)
C["foodapest"] = dict(
    rank="#7 Best Food Tour", title="Market to Tavern Food Tour With Wine", dur="3 Hours", place="Central Market Hall",
    map="Central Market Hall Budapest", psub="per person • 11:30 market tour",
    pills=[("🏛️", "Market + tavern", "Starts in the Central Market Hall, then a bakery and two local restaurants. The last stop is the wine tasting."),
           ("🍽️", "12+ tastings", "Cold cuts, pickles, goulash, lángos, chimney cake and a Hungarian dessert: enough to count as lunch."),
           ("🕒", "11:30 or 17:00", "The 11:30 market tour is €69. A 17:00 evening tour (street food, wine, pálinka and craft beer, no market) is €79."),
           ("🍷", "Wine and pálinka", "A Hungarian wine tasting at the final restaurant and a homemade pálinka along the way. Alcohol-free swaps available.")],
    pick="for a cold November midday spent mostly indoors, eating your way from the market to a tavern.",
    skip="if you have a dinner cruise the same evening and a small appetite.",
    pros=["Rated 4.9 by nearly 700 guests", "Mostly indoors, which matters in November", "Enough food to replace a meal"],
    cons=["3 hours on your feet", "The evening option skips the market hall"],
    body="""<p>November is market-hall weather. This tour starts in the <strong>Central Market Hall</strong> at <strong>11:30</strong>, works through <strong>12+ tastings</strong> (goulash, lángos, chimney cake, cold cuts) in a bakery and two local restaurants, and ends with a <strong>Hungarian wine tasting</strong>. Most of the 3 hours are spent indoors, and you finish in the early afternoon with daylight left for a bath.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> on your first full day: you'll know what to order for the rest of the trip. The 11:30 tour costs €69.</p>
<p><strong>Skip it</strong> if your evening is a dinner cruise and you eat light. Nine food tours compared: <a href="/best-food-tours-budapest">best food tours in Budapest</a>.</p>
<h3>Meeting Point</h3>
<p>🗺️ <strong>Meeting Point: </strong>Central Market Hall, Fővám tér (the exact spot is in your voucher).<br/>🚇 <strong>Public Transport:</strong> M4 to Fővám tér, or tram 2, 47 or 49.</p>""",
    qf_badge="Food + wine", qf=[("Start Times", "11:30 market tour · 17:00 evening tour (no market)"), ("Duration", "About 3 hours"),
        ("Price", "€69 (11:30) · €79 (17:00)"), ("Food", "12+ tastings"), ("Drinks", "Wine tasting, pálinka"), ("Start", "Central Market Hall, Fővám tér")],
    chips=[("yes", "✓ Mostly Indoors"), ("yes", "✓ Wine Included"), ("yes", "✓ Free Cancellation")],
    perks=["Start: <strong>Market Hall</strong>", "Tastings: <strong>12+</strong>"],
    desc="Three-hour Budapest food tour from the Central Market Hall to a local tavern with 12+ tastings and wine.",
)
C["castle"] = dict(
    rank="#8 Best Morning Walk", title="Buda Castle District Walking Tour", dur="2 Hours", place="Szentháromság tér",
    map="Szentháromság tér Budapest", psub="per person • 2 hours",
    tested_pop="<strong>I took this tour myself.</strong>",
    pills=[("🏰", "Castle Hill in 2 hours", "Matthias Church, Fisherman's Bastion and the old streets of the Castle District with a guide."),
           ("☀️", "Go before 14:00", "With sunset at about 16:00, a morning slot gives you the river views in daylight."),
           ("🎄", "Budavári Advent from 27 Nov", "From 27 November the Budavári Advent market fills Szentháromság tér, right where the tour starts."),
           ("💶", "From €12", "The cheapest guided activity on this list.")],
    pick="for a cheap, guided morning on Castle Hill while the light is good.",
    skip="for the afternoon: by 15:30 the light is going.",
    pros=["€12 for a 2-hour guided walk", "Rated 4.6 by more than 2,400 guests", "Best views over the river in daylight"],
    cons=["Outdoors for 2 hours in the cold", "Church interiors are extra"],
    body="""<p>Castle Hill is a daylight job in November. This <strong>2-hour guided walk for €12</strong> covers Matthias Church, Fisherman's Bastion and the old Castle District streets, starting on Szentháromság tér.</p>
<p>I've taken this tour myself. Book a morning slot, then come back after dark for the lit Bastion, which is free, or for the <a href="#item-5-vampire-night-walk">vampire night walk</a>.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> on a dry morning for the history and the best views over the river.</p>
<p><strong>Skip it</strong> if you only want the views: the Bastion's lower terraces are free to walk.</p>
<h3>Meeting Point</h3>
<p>🗺️ <strong>Meeting Point: </strong>Szentháromság tér, by Matthias Church.<br/>🚌 <strong>Public Transport:</strong> Bus 16 from Deák Ferenc tér, or the Castle Hill funicular from Clark Ádám tér.</p>""",
    qf_badge="Castle District", qf=[("Duration", "2 hours"), ("Price", "From €12 / person"), ("Route", "Matthias Church, Fisherman's Bastion, Castle District"),
        ("Best Time", "Morning, before 14:00"), ("Transport", "Bus 16, Castle Hill funicular")],
    chips=[("yes", "✓ Cheapest Pick"), ("yes", "✓ Free Cancellation"), ("no", "✕ Outdoors in the Cold")],
    perks=["Start: <strong>Szentháromság tér</strong>", "Duration: <strong>2 Hours</strong>"],
    desc="Two-hour guided walking tour of the Buda Castle District from €12.",
)

ANCHORS = {"legenda-evening": "item-1-legenda-evening-cruise", "szechenyi": "item-2-szechenyi-thermal-bath",
           "legenda-dinner": "item-3-legenda-candlelit-dinner", "rudas": "item-4-rudas-thermal-bath",
           "vampire": "item-5-vampire-night-walk", "silverline": "item-6-silverline-dinner-cruise",
           "foodapest": "item-7-foodapest-food-tour", "castle": "item-8-buda-castle-walking-tour"}


def A(k):
    return "#" + ANCHORS[k]


LEAD = f"""<p>In mid-November <strong>the sun sets at 16:07</strong>, and by 30 November at 15:55. Most guides treat that as the downside of the month. I'd plan around it: Budapest's best sights are its lit-up ones, and in November they are lit before you've finished your afternoon coffee.</p>
<p>Below are the 8 things I'd book for November, 7 of them done myself, plus the <a href="#november-dates">dates that change your plans</a> (the Christmas markets open on 13 and 27 November) and the <a href="#free-things">free evenings</a>. Only one evening? Book <a href="{A('legenda-evening')}"><strong>Legenda's evening cruise</strong></a> (€25, every 20 minutes from 16:20).</p>"""

PICKS_H = "Quick Picks for November"
PICKS = [("Your first evening", "legenda-evening", "€25, one hour, every 20 minutes from 16:20"),
         ("Hot pools in cold air", "szechenyi", "from €39, open until 22:00 on Fridays"),
         ("A romantic dinner on the river", "legenda-dinner", "€110, 19:00 daily, served 4 courses"),
         ("A bath with a view after dark", "rudas", "rooftop pool at 36 °C, night bathing Fri and Sat"),
         ("Something to do at 20:00", "vampire", "€20, two hours of folk tales on Castle Hill"),
         ("A dinner cruise for less", "silverline", "from €77, 4 courses at 19:00"),
         ("A rainy midday", "foodapest", "€69, mostly indoors, 12+ tastings"),
         ("On a budget", "castle", "€12 guided walk on Castle Hill")]

DATES_H = "November 2026 Dates That Change Your Plans"
DATES_INTRO = "Two things happen in the second half of November: the Christmas season opens, and the evening timetables shift. Here is what starts when."
DATES_COLS = ["Date", "What", "Why it matters"]
DATES_ROWS = [
    ("13 Nov", "Advent Bazilika and Vörösmarty tér Christmas markets open", "The two big central markets run from now, free to enter. <a href=\"#christmas-markets-november\">Hours below</a>."),
    ("20 Nov", "City Park Ice Rink planned opening", "The rink in front of Vajdahunyad Castle plans to open on 20 November; tickets on its own site, mujegpalya.hu."),
    ("23 Nov", "Legenda adds a 15:40 evening cruise", f"Until 22 November the first evening boat is 16:20. From 23 November there is also a 15:40 sailing. <a href=\"{A('legenda-evening')}\">See the cruise</a>."),
    ("27 Nov", "Budavári Advent and Advent Óbudán open", "The Castle Hill market and the Óbuda market open, and Óbuda's free ice rink on Fő tér starts the same day."),
    ("27-29 Nov", "Art Weekend Budapest", "Galleries, studios and project spaces open their doors across the city. Free; the guided walks need registration."),
    ("All month", "Bonjour Monsieur Gauguin", "The Gauguin exhibition at the Museum of Fine Arts runs from 30 October 2026 to 28 February 2027. Tuesday to Sunday 10:00 to 18:00, closed on Mondays."),
    ("All month", "Lumina Park", "A walk-through light park at Palatinus on Margaret Island, 16:30 to 21:00, closed on Mondays. Tickets from 5,000 HUF."),
]
DATES_NOTE = "Dates from the organisers' own sites. The ice rink date is a planned opening and can move with the weather."

SEASON_H = "November Weather and Daylight in Budapest"
SEASON_P = ("Expect <strong>around 9 °C by day and 3 °C at night</strong>, a monthly average of 5.9 °C and about <strong>48 mm of rain</strong> "
            "(HungaroMet, 1991-2020 averages). It is grey more often than not, and it gets colder through the month. "
            "Pack a warm waterproof jacket and shoes with grip for the cobbles on Castle Hill.")
SUN_COLS = ["Date", "Sunrise", "Sunset", "Daylight"]
SEASON_TIP = ("<strong>How to use the short days:</strong> outdoor sights and the market hall from 9:00 to 14:00, "
              "a bath at dusk, then a cruise, dinner or a night walk after 16:30.")

XMAS_H = "Christmas Markets in November"
XMAS_P = ("You don't have to wait for December. The two big central markets <strong>opened on 13 November</strong>, and the Castle Hill and Óbuda markets open on "
          "<strong>27 November</strong>. All four are free to enter. The Basilica facade gets a 3D light show every 30 minutes from 17:30.")
XMAS_COLS = ["Market", "Dates", "Hours"]
XMAS_LINK = ("Stalls, food prices, walking times and a 1-evening route: <a href=\"/budapest-christmas-markets\">Budapest Christmas markets 2026</a>. "
             "Staying into December? See <a href=\"/things-to-do-budapest-december\">things to do in Budapest in December</a>.")

FREE_H = "Free Things to Do in November"
FREE = [
    ("Walk the river after dark", "From the Pest embankment between the Chain Bridge and the Parliament you get the lit Castle, the bridges and the Parliament for free, from about 16:30."),
    ("Walk the Christmas markets", "Advent Bazilika and Vörösmarty tér are free to enter and five minutes apart, open daily from 11:00. Watch the Basilica light show from 17:30."),
    ("Climb Castle Hill at night", "The Castle District and the lower terraces of Fisherman's Bastion are free and almost empty after dark."),
    ("Skate in Óbuda", "The rink on Óbuda's Fő tér is free from 27 November (Sunday to Thursday 8:00 to 21:00, Friday and Saturday to 22:00)."),
    ("Art Weekend Budapest", "On 27 to 29 November galleries and studios across the city open for free."),
]

MORE_H = "More November Ideas"
MORE = [
    ("Every night cruise compared", "Ten evening and night cruises side by side, 6 tested: <a href=\"/best-night-cruises-budapest\">best night cruises in Budapest</a>."),
    ("Every thermal bath compared", "Six baths with hours and prices, 4 tested: <a href=\"/thermal-baths-budapest\">best thermal baths in Budapest</a>."),
    ("The Parliament", "Guided tours run all year, and the building is lit at night: <a href=\"/budapest-parliament\">Budapest Parliament tickets and tips</a>."),
    ("Museums on rainy days", "Whether the Budapest Card pays off on a museum-heavy trip: <a href=\"/budapest-card-is-it-worth-it\">Budapest Card, is it worth it?</a>"),
    ("Year-round favourites", "The classics for any month: <a href=\"/best-things-to-do-budapest\">best things to do in Budapest</a>."),
]
DEC_LINK = ("Coming later? See <a href=\"/things-to-do-budapest-december\">things to do in Budapest in December</a>.")

FAQ = [
    ("Is Budapest worth visiting in November?",
     "Yes, if you plan around the dark. Days are short (sunset around 16:00) and often grey at about 9 °C, but the city is lit up early, "
     "the thermal baths' outdoor pools are at their best in cold air, and from 13 November the central Christmas markets are open."),
    ("What is the weather like in Budapest in November?",
     "Cool and often grey: about 9 °C by day and 3 °C at night, with around 48 mm of rain in the month (1991-2020 averages). "
     "The sun rises between 6:27 and 7:09 and sets between 16:26 and 15:55 over the month."),
    ("Are the Budapest Christmas markets open in November 2026?",
     "Yes. Advent Bazilika (Szent István tér) and Vörösmarty tér opened on 13 November 2026. Budavári Advent on Castle Hill and Advent Óbudán open on 27 November. "
     "All are free to enter. Details: <a href=\"/budapest-christmas-markets\">Budapest Christmas markets 2026</a>."),
    ("Are the thermal baths open in November?",
     "Yes, all year. Széchenyi's outdoor pools stay open (the thermal pool is 36 to 38 °C); it is open 7:00 to 20:00 Monday to Thursday, until 22:00 on Friday and 8:00 to 20:00 at weekends. "
     "Rudas has night bathing on Friday and Saturday from 22:00 to 3:00."),
    ("Do Danube cruises run in November?",
     f"Yes. <a href=\"{A('legenda-evening')}\">Legenda's evening cruise</a> sails every 20 minutes from 16:20 to 21:00, with an extra 15:40 boat from 23 November. "
     f"Dinner cruises sail at 19:00, such as <a href=\"{A('legenda-dinner')}\">Legenda's candlelit dinner</a> (€110) and <a href=\"{A('silverline')}\">Silverline's Dinner &amp; Lights</a> (from €77)."),
    ("What can I do in Budapest on a rainy November day?",
     f"Go to a thermal bath (Rudas's rooftop pool is warm in any weather), take the <a href=\"{A('foodapest')}\">Foodapest market tour</a>, which is mostly indoors, "
     "or see the Gauguin exhibition at the Museum of Fine Arts (Tuesday to Sunday, 10:00 to 18:00)."),
    ("When does the City Park Ice Rink open in 2026?",
     "The rink plans to open on 20 November 2026. The date can move with the weather, so check mujegpalya.hu before you go. Óbuda's smaller rink on Fő tér is free from 27 November."),
    ("What is there to do in Budapest in the evening in November?",
     f"It is dark from about 16:30, so evenings are long: a <a href=\"{A('legenda-evening')}\">one-hour night cruise</a>, a bath after dark (Széchenyi until 22:00 on Fridays), "
     f"the <a href=\"{A('vampire')}\">vampire night walk</a> at 20:00, the Christmas markets until 21:00 or later, or Lumina Park on Margaret Island."),
]

METHOD_H = "How These Picks Were Chosen"
METHOD = ("Each card's price, start times, inclusions and rating were read on the live listing for that exact product, and Legenda's departures on its 2026 timetable. "
          "Market dates come from the organisers' own sites, bath hours from the official bath sites, sunrise and sunset from timeanddate.com "
          "and the climate figures from HungaroMet's 1991-2020 normals for Budapest. "
          "\"Personally Tested\" marks only the seven things I've done myself; the food tour is the one I haven't.")

HOMECARD = ("8 Best Things to Do in Budapest in November 2026", "")
MENU_SUB = "Night cruises, hot pools &amp; market openings"
MENU_TITLE = "Budapest in November"

_MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def DAY(d):
    return d


def DUR(c):
    return c


def _d(iso, year=False):
    y, m, d = (int(x) for x in iso.split("-"))
    return f"{d} {_MON[m - 1]}" + (f" {y}" if year else "")


def SPAN(a, b):
    return f"{_d(a)} to {_d(b, year=b[:4] != '2026')}"


def _h(v):
    return v.replace("-", " to ")


def HOURS(m):
    h = m["hours"]
    if "fri" in h:
        return f"Mon to Thu {_h(h['mon_thu'])} · Fri {_h(h['fri'])} · Sat {_h(h['sat'])} · Sun {_h(h['sun'])}"
    if h["mon_thu"] == h["fri_sat"] == h["sun"]:
        return f"Daily {_h(h['mon_thu'])}"
    return f"Sun to Thu {_h(h['mon_thu'])} · Fri and Sat {_h(h['fri_sat'])}"
