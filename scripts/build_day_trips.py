#!/usr/bin/env python3
"""Build /best-day-trips-from-budapest (EN only), 2026-11-15.

Template: best-walking-tours-budapest.html (head, menu, footer, deck/breakdown
CSS and JS are reused; hero, deck, guide, breakdown, FAQ, sticky bar and JSON-LD
are replaced).

All 13 trips come from live GetYourGuide product pages read on 2026-11-15:
rating, review count and lowest price from each page's structured data;
duration, inclusions, meeting point and group size from the product page.
None of them is personally tested: no "tested" chips, no author review.
Photos are the operators' listing photos, stored under /assets/day-trips-2026/.

"Time at the destination" is an estimate: listed duration minus typical
driving time between Budapest and the stops. It is labelled as approximate.

Re-runnable: always rebuilds from the walking tours template.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import hashlib  # noqa: E402
from build_walking_tours_10 import gyg_icon  # noqa: E402
from day_trips_pills import ORDER, PILLS, PICKSKIP  # noqa: E402

TEMPLATE = ROOT / "best-walking-tours-budapest.html"
OUT = ROOT / "best-day-trips-from-budapest.html"
SLUG = "best-day-trips-from-budapest"
URL = f"https://www.budapestadventures.com/{SLUG}"
OLD_URL = "https://www.budapestadventures.com/best-walking-tours-budapest"
CHECKED = "15 November 2026"
CHECKED_SHORT = "Nov 15, 2026"
ISO = "2026-11-15"
IMG = "/assets/day-trips-2026"
OG_IMG = "https://www.budapestadventures.com/assets/day-trips-2026/danube-forest-01.webp"  # social cards need webp/jpg
GYG = "https://www.getyourguide.com/{path}/?partner_id=YS414AJ&amp;utm_medium=online_publisher&amp;cmp={cmp}&amp;mkt_cmp=true"

TITLE_TAG = "13 Best Day Trips from Budapest (2026): Time & Price Compared"
H1 = "The 13 Best Day Trips from Budapest in 2026"
H1_MUTED = "(Compared by Time on the Ground)"
CRUMB = "The 13 Best Day Trips from Budapest in 2026"
META = ("13 day trips from Budapest compared on hours at the destination vs on the road: "
        "Danube Bend, Lake Balaton, Eger, Hévíz, Vienna and Bratislava. From €60.")

TRIPS = [
    dict(
        anchor="item-1-danube-bend-forest-tour", operator="MazakEV", short_op="MazakEV",
        title="Danube Bend Forest Tour: Visegrád and Szentendre",
        path="visegrad-l1566/from-budapest-danube-bend-day-trip-with-visegrad-and-szentendre-t1470042",
        cmp="day-trips-danube-forest", score="4.9", count_exact=37, price=96,
        dur="8-9 Hours", dur_short="8 to 9 hours", place="Batthyány tér", map="Batthyány+tér+Budapest",
        cats="full u100 small", photos="danube-forest",
        alts=["Visegrád Castle above the Danube Bend in morning mist",
              "Stream on the forest trail in the Danube-Ipoly National Park",
              "Autumn colours at a forest stop on the way to Visegrád",
              "Leaf-covered royal hunting path through the Visegrád hills",
              "Small group taking a photo break on the forest walk"],
        specs=["Max 7 Guests", "⏱ 8-9 Hours", "75-Min Forest Walk", "Hotel Pickup Option"],
        best_for="Travellers who want the Danube Bend without a coach: a 75-minute forest walk to Visegrád Castle, then Szentendre, max 7 guests.",
        pros=["Max 7 guests in a Mercedes minibus, so stops run on your pace, not a coach timetable",
              "75-minute downhill forest walk ends right at Visegrád Castle, the best view of the bend",
              "Stay on in Szentendre and ride the boat or HÉV back on your own if you want more time"],
        cons=["Castle ticket (€8 adults) and lunch are extra",
              "Not for children under 8 or anyone who struggles on uneven, muddy trails"],
        body="""<p>Most Danube Bend tours show you Visegrád from a car park. This one makes you <strong>walk into it</strong>: a 4.6 km, <strong>75-minute downhill trail</strong> through the Danube-Ipoly National Park, on old royal hunting paths, that comes out at the castle gate with the whole bend below you.</p>
<p>After the castle there is lunch at a forest restaurant where locals eat (you pay what you order, and prices are lower than in Budapest), then free time in <strong>Szentendre</strong> with a hand-drawn map of the host's favourite spots. The minibus leaves Szentendre at 17:00. If you want sunset on the river, stay and take the public boat or the HÉV train back yourself.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> if you hate coach tours and want one quiet, active day out of the city. With 7 seats at most, it is the closest thing to a private trip at a group price.</p>
<p><strong>Skip it</strong> if you want a guide talking at every stop (the castle visit is self-guided after a short intro), or if walking 75 minutes on forest paths is a stretch.</p>
<h3>Meeting Point</h3>
<p>🗺️ <strong>Meeting Point: </strong>Main entrance of St. Anne's Church, Batthyány tér (on the Buda side), 09:00. Look for the driver holding a Rubik's Cube.<br/>🚇 <strong>Public Transport:</strong> Batthyány tér (M2 metro, H5 HÉV).</p>""",
        qf_badge="Visegrád + Szentendre",
        qf=[("Duration", "8 to 9 hours (minibus leaves Szentendre at 17:00)"), ("Price", "From €96 / person"),
            ("Group Size", "Max 7 guests"), ("Pickup", "Batthyány tér at 09:00, or hotel pickup"),
            ("Included", "Minibus transport, local host, self-guided forest walk, Szentendre map"),
            ("Not Included", "Visegrád Castle ticket (€8 adults, €4 students), lunch"),
            ("Time at Destinations", "About 6.5 hours"), ("Not Suitable For", "Children under 8, wheelchair users")],
        chips=[("yes", "✓ Max 7 Guests"), ("yes", "✓ Forest Walk to the Castle"), ("yes", "✓ Option to Stay Later"),
               ("no", "✕ Lunch Not Included"), ("no", "✕ Castle Ticket Extra")],
        perks=["Departure: <strong>Batthyány tér</strong>", "Group: <strong>Max 7</strong>"],
        road=1.5, ground=6.5,
        incl="Transport, host",
        desc="Small-group Danube Bend day trip with a 75-minute forest walk to Visegrád Castle and free time in Szentendre, max 7 guests.",
    ),
    dict(
        anchor="item-2-danube-bend-day-trip", operator="Cityrama Budapest Travel Agency", short_op="Cityrama",
        title="Danube Bend Day Trip: Visegrád, Esztergom and Szentendre",
        path="budapest-l29/danube-bend-tour-an-excursion-into-hungary-s-history-t759",
        cmp="day-trips-danube-bend", score="4.3", count_exact=669, price=85,
        dur="9 Hours", dur_short="9 hours", place="Báthory utca", map="Báthory+utca+19+Budapest",
        cats="full u100 boat", photos="danube-bend",
        alts=["Visegrád Citadel walls with the Danube Bend below",
              "Esztergom Basilica reflected in the Danube at dusk",
              "Colourful umbrellas over a Szentendre lane",
              "Esztergom Basilica, the largest church in Hungary",
              "Esztergom old town and basilica from a viewpoint"],
        specs=["All 3 Towns", "⏱ 9 Hours", "Boat Back (Summer)", "Cheapest Full Day"],
        best_for="The classic three-town loop at the lowest price: Visegrád, Esztergom and Szentendre in 9 hours, with a boat ride back on summer weekends.",
        pros=["Lowest price for all three Danube Bend towns in one day (€85)",
              "Return boat ticket included May to September (Thursday to Sunday)",
              "Central meeting point in District V, near Parliament"],
        cons=["Lunch and the Visegrád Castle ticket are extra",
              "Bilingual English and Spanish commentary; coach-size group"],
        body="""<p>This is the benchmark Danube Bend trip: <strong>Visegrád, Esztergom and Szentendre in 9 hours</strong> for €85, the lowest price for all three towns. You walk past the stones of the medieval royal residence in Visegrád, see <strong>Esztergom Basilica</strong> (the largest church in Hungary) with the view over to Slovakia, then finish with a stroll up Szentendre's lanes to a viewpoint over the river.</p>
<p>From <strong>May to September, Thursday to Sunday</strong>, the return leg is by boat and the ticket is included. Outside those dates, or when the river is too high or low, you come back by coach.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> if you want to tick off the whole Danube Bend on a budget and don't mind a bigger group. On a summer weekend the boat back alone is worth a good part of the price.</p>
<p><strong>Skip it</strong> if you want lunch sorted (it isn't included, see <a href="#item-9-danube-bend-with-lunch">the lunch version</a>) or a small group (see <a href="#item-1-danube-bend-forest-tour">the forest tour</a>).</p>
<h3>Meeting Point</h3>
<p>🗺️ <strong>Meeting Point: </strong>Báthory utca 19, 1054 Budapest (District V).<br/>🚇 <strong>Public Transport:</strong> Kossuth Lajos tér (M2) or Arany János utca (M3), then a 5-minute walk.</p>""",
        qf_badge="Visegrád + Esztergom + Szentendre",
        qf=[("Duration", "9 hours"), ("Price", "From €85 / person"),
            ("Language", "English and Spanish (bilingual guide)"),
            ("Meeting Point", "Báthory utca 19, 1054 Budapest"),
            ("Included", "Guide, air-conditioned transport, boat ticket back (May to Sept, Thu to Sun)"),
            ("Not Included", "Visegrád Castle ticket, lunch, tips"),
            ("Time at Destinations", "About 6 hours"), ("Return", "Boat in season, otherwise coach")],
        chips=[("yes", "✓ All 3 Danube Bend Towns"), ("yes", "✓ Boat Back in Summer"),
               ("no", "✕ Lunch Not Included"), ("no", "✕ Castle Ticket Extra")],
        perks=["Departure: <strong>Báthory utca</strong>", "Duration: <strong>9 Hours</strong>"],
        road=3, ground=6, incl="Transport, guide, boat back (summer)",
        desc="Budget full-day Danube Bend tour to Visegrád, Esztergom and Szentendre with a boat ride back on summer weekends.",
    ),
    dict(
        anchor="item-3-lake-balaton-tihany", operator="Blueridge s. r. o.", short_op="Blueridge",
        title="Lake Balaton and Tihany Day Trip with Esztergom",
        path="szekesfehervar-l157735/from-budapest-lake-balaton-tihany-day-trip-with-esztergom-t1305591",
        cmp="day-trips-balaton", score="4.6", count_exact=159, price=83,
        dur="About 10 Hours", dur_short="About 10 hours", place="Your hotel", map="",
        cats="full u100 pickup small", photos="balaton",
        alts=["Tihany Abbey above Lake Balaton",
              "Rose garden walkway with a view of Lake Balaton",
              "Friends having coffee on the Balatonfüred lakeside",
              "Wooden lookout tower over Lake Balaton at sunset",
              "Small group at the Tihany Abbey viewpoint"],
        specs=["Max 8 Guests", "⏱ About 10 Hours", "Hotel Pickup", "Slovakia Photo Stop"],
        best_for="Seeing Lake Balaton and Tihany in one day with hotel pickup and max 8 guests, plus Esztergom Basilica on the way.",
        pros=["Hotel pickup and drop-off anywhere in Budapest, max 8 guests",
              "Tihany Abbey, a lake viewpoint and free time in Balatonfüred in one day",
              "Esztergom Basilica and a photo stop in Slovakia on the way"],
        cons=["Long day: about 10 hours, roughly half of it on the road",
              "Meals not included; bring ID for the Slovakia stop"],
        body="""<p>Lake Balaton is too far for public transport to make a comfortable day trip with Tihany in it, which is why this is one of the few tours where <strong>the car is the point</strong>. A driver-guide collects you from your hotel, and with <strong>8 guests at most</strong> the stops flex around the group.</p>
<p>The route is long: Esztergom Basilica first, a quick hop over the bridge to Štúrovo in Slovakia for the classic basilica photo, then down to the lake for the Akarattya cliff viewpoint, <strong>Tihany Abbey</strong> on its peninsula and <strong>free time on the Balatonfüred promenade</strong>. Plan on about 10 hours door to door.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> if Balaton is on your list and you have one day for it. Hotel pickup and a small group make the long drive easy.</p>
<p><strong>Skip it</strong> if you want a lake day to swim and lie down: you see a lot, but you spend around 5 hours in the car. In that case take the train to Balatonfüred and stay put.</p>
<h3>Pickup</h3>
<p>🚐 <strong>Pickup:</strong> From your hotel or apartment in Budapest. Exact time and driver contact arrive the day before.<br/>🪪 <strong>Bring:</strong> Passport or ID card for the Slovakia stop.</p>""",
        qf_badge="Esztergom + Tihany + Balatonfüred",
        qf=[("Duration", "Listed as 8 hours; about 10 hours door to door with traffic"), ("Price", "From €83 / person"),
            ("Group Size", "Max 8 guests"), ("Pickup", "Hotel pickup and drop-off in Budapest"),
            ("Included", "Driver-guide, transport, bottled water, local snacks, Esztergom Basilica visit"),
            ("Not Included", "Meals and drinks"), ("Time at Destinations", "About 5 hours"),
            ("Bring", "Passport or ID card (Slovakia stop)")],
        chips=[("yes", "✓ Hotel Pickup"), ("yes", "✓ Max 8 Guests"), ("yes", "✓ 3 Regions in 1 Day"),
               ("no", "✕ Meals Not Included"), ("no", "✕ Long Day in the Car")],
        perks=["Pickup: <strong>Your hotel</strong>", "Group: <strong>Max 8</strong>"],
        road=5, ground=5, incl="Hotel pickup, guide, water, snacks",
        desc="Small-group day trip from Budapest to Lake Balaton, Tihany Abbey and Balatonfüred, with Esztergom Basilica and hotel pickup.",
    ),
    dict(
        anchor="item-4-bratislava-vienna", operator="Blueridge s. r. o.", short_op="Blueridge",
        title="Bratislava and Vienna Full-Day Guided Tour",
        path="vienna-l7/from-budapest-bratislava-vienna-full-day-guided-tour-t1214396",
        cmp="day-trips-bratislava-vienna", score="4.8", count_exact=357, price=189,
        dur="12.5-13 Hours", dur_short="12.5 to 13 hours", place="Your hotel", map="",
        cats="two o160 pickup small", photos="vienna-bratislava",
        alts=["Bratislava old town and St. Martin's Cathedral from above",
              "Vienna City Hall in autumn",
              "Horse statue outside a Vienna museum on the Ringstrasse",
              "Bratislava Castle above the old town",
              "Bratislava Castle lit up at dusk over the Danube"],
        specs=["2 Capitals", "⏱ 12.5-13 Hours", "Hotel Pickup", "End in Vienna Option"],
        best_for="Two capitals in one long day with a small group, a guide in both cities and the option to end in Vienna with your luggage.",
        pros=["Guided walks in both Bratislava (old town and castle) and Vienna (Hofburg, St. Stephen's, the Ring)",
              "Pickup from any accommodation in Budapest; small group",
              "You can end the tour in Vienna with your luggage, handy if you travel on"],
        cons=["12.5 to 13 hours, with roughly 6 of them on the motorway",
              "Meals not included"],
        body="""<p>If you only have one day for <strong>Vienna and Bratislava</strong>, this is the most flexible way to do both. The day starts with a guided walk through <strong>Bratislava's old town</strong> (St. Michael's Gate, the Main Square, the Blue Church) and up to <strong>Bratislava Castle</strong>, with views over three countries. In the afternoon a guided walk in Vienna covers the <strong>Hofburg, St. Stephen's Cathedral, the Opera and the Ringstrasse</strong>, then you get free time.</p>
<p>Two details set it apart: pickup from <strong>any accommodation in Budapest</strong>, and the option to <strong>end the tour in Vienna with your luggage</strong>, which turns your transfer to Austria into a sightseeing day.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> if you want two new capitals ticked off with someone else driving, or you are moving on to Vienna anyway.</p>
<p><strong>Skip it</strong> if you only care about Vienna: the train gets you there in about 2 hours 40 minutes and gives you far more hours in the city for less money (see the DIY section above).</p>
<h3>Pickup</h3>
<p>🚐 <strong>Pickup:</strong> Any hotel, Airbnb or apartment in Budapest. Guide contact details arrive the day before.<br/>🪪 <strong>Bring:</strong> Passport or EU ID card for the border crossings.</p>""",
        qf_badge="Bratislava + Vienna",
        qf=[("Duration", "12.5 to 13 hours"), ("Price", "From €189 / person"),
            ("Pickup", "Any accommodation in Budapest"), ("Group", "Small group or private"),
            ("Included", "English-speaking driver-guide, transport, water, snacks"),
            ("Not Included", "Meals, personal expenses"), ("Time at Destinations", "About 6.5 hours"),
            ("Extras", "Optional Győr stop; option to end in Vienna with luggage; wheelchair accessible")],
        chips=[("yes", "✓ Hotel Pickup"), ("yes", "✓ Guided in Both Cities"), ("yes", "✓ End in Vienna Option"),
               ("no", "✕ Meals Not Included"), ("no", "✕ 12+ Hour Day")],
        perks=["Pickup: <strong>Your hotel</strong>", "Duration: <strong>12.5-13 Hours</strong>"],
        road=6, ground=6.5, incl="Hotel pickup, guide, water, snacks",
        desc="Small-group full-day tour from Budapest to Bratislava and Vienna with guided walks in both capitals and hotel pickup.",
    ),
    dict(
        anchor="item-5-etyek-wine-tour", operator="City & Wine Ltd", short_op="City &amp; Wine",
        title="Half-Day Etyek Countryside Wine Tour with Meal",
        path="budapest-l29/from-budapest-half-day-countryside-wine-tour-with-meal-t72950",
        cmp="day-trips-etyek-wine", score="4.8", count_exact=834, price=85,
        dur="4-5 Hours", dur_short="4 to 5 hours", place="Central hotels", map="",
        cats="half u100 pickup meal", photos="etyek",
        alts=["Winemaker pouring white wine at an Etyek tasting",
              "Guests at a long table on an Etyek winery terrace",
              "Wine poured into a carafe during the Etyek tasting",
              "Group tasting wine in an Etyek garden",
              "Etyek winery building with lavender in front",
              "Wine drawn from the barrel in an Etyek cellar"],
        specs=["8 Wines", "⏱ 4-5 Hours", "Home-Cooked Meal", "30 Min from Budapest"],
        best_for="A half day of Hungarian wine with almost no driving: 2 family wineries, 8 wines and a home-cooked meal, 30 minutes from Budapest.",
        pros=["Only about 30 minutes each way, so most of the 4 to 5 hours is spent tasting",
              "2 family wineries with 4 wines at each, plus snacks and a home-cooked meal",
              "Pickup from selected central hotels; vegetarian and gluten-free on request"],
        cons=["Coffee, soft drinks and tips are extra",
              "Runs with a minimum of 2 guests (otherwise you are offered another date)"],
        body="""<p>Etyek is Budapest's closest wine region, <strong>about 30 minutes</strong> out of the city, which makes this the day trip with the best ratio of glass time to road time. You visit <strong>2 family-owned boutique wineries</strong>, taste <strong>4 wines at each</strong> with snacks in the cellar, and finish with a <strong>home-cooked meal</strong> at one of the farms.</p>
<p>The winemakers pour themselves, so you hear how the wines are made from the people who make them. It is also the highest-rated trip here by volume: 4.8 from more than 800 reviews.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> if you want a relaxed afternoon in the countryside without losing a whole day, and you like wine more than sights.</p>
<p><strong>Skip it</strong> if you want famous wine names: Etyek is known for crisp whites and sparkling, not for Tokaji or Bull's Blood. For those, go to <a href="#item-7-eger-private-tour">Eger</a>.</p>
<h3>Pickup</h3>
<p>🚐 <strong>Pickup:</strong> Selected hotels in central Budapest. Contact the operator before the tour for the exact time and place.</p>""",
        qf_badge="Etyek wine region",
        qf=[("Duration", "4 to 5 hours"), ("Price", "From €85 / person"),
            ("Pickup", "Selected central Budapest hotels"),
            ("Included", "Minibus transfers, guide, 4 wines at each winery, snacks, 2-course home-cooked meal, water"),
            ("Not Included", "Coffee and soft drinks, tips"), ("Time at Destination", "About 3.5 hours"),
            ("Diets", "Vegetarian or gluten-free if requested in advance"), ("Minimum", "2 guests")],
        chips=[("yes", "✓ Meal Included"), ("yes", "✓ 8 Wines"), ("yes", "✓ Short Drive"),
               ("no", "✕ Pets Not Allowed")],
        perks=["Pickup: <strong>Central hotels</strong>", "Duration: <strong>4-5 Hours</strong>"],
        road=1, ground=3.5, incl="Pickup, guide, 8 wines, meal",
        desc="Half-day wine tour from Budapest to 2 family wineries in Etyek with 8 tastings and a home-cooked meal.",
    ),
    dict(
        anchor="item-6-godollo-sissi-palace", operator="Eurama Sightseeing City Tours Budapest", short_op="Eurama",
        title="Gödöllő Royal Palace (Sissi) Guided Tour",
        path="budapest-l29/royal-sissi-tour-from-budapest-t55693",
        cmp="day-trips-godollo", score="4.3", count_exact=1177, price=60,
        dur="3.5 Hours", dur_short="3.5 hours", place="Eurama office", map="",
        cats="half u100 pickup", photos="godollo",
        alts=["Gödöllő Royal Palace at sunset",
              "Gödöllő Royal Palace from the park",
              "Baroque facade of the Gödöllő palace",
              "Gödöllő Royal Palace and gardens from above",
              "Wings of the Gödöllő Royal Palace and lawn"],
        specs=["Palace Tour Included", "⏱ 3.5 Hours", "5 Languages", "Cheapest Trip"],
        best_for="Fans of Empress Elisabeth (Sissi) with a free morning: her summer palace with a guided tour, back in Budapest in 3.5 hours.",
        pros=["Cheapest trip on the list (€60) and only a morning or afternoon",
              "Guided tour of the palace included, with skip-the-line entry",
              "Ends in the city centre at the InterContinental hotel"],
        cons=["Only one sight; easy to do yourself by HÉV train",
              "Food and drinks not included; not for wheelchair users"],
        body="""<p>Gödöllő is where Empress Elisabeth, better known as <strong>Sissi</strong>, spent her summers, and its palace is billed as the second-largest Baroque chateau in the world. This trip is short and simple: a drive out, a <strong>guided tour of the restored royal rooms</strong> and a walk in the park, then back to the centre in <strong>3.5 hours</strong>.</p>
<p>At €60 it is the cheapest trip here, and it fits into half a day, so you can still do a bath or a river cruise in the evening.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> if Sissi is the reason you came, you want the guided version of the palace and you don't want to work out suburban trains.</p>
<p><strong>Skip it</strong> if you are happy on public transport: the H8 HÉV from Örs vezér tere gets you to Gödöllő in about 45 minutes, and a palace ticket costs a fraction of the tour price.</p>
<h3>Meeting Point</h3>
<p>🗺️ <strong>Meeting Point: </strong>The Eurama office in central Budapest (blue "Eurama Meeting Point" flag), 30 minutes before departure. Hotel pickup is available as an option.<br/>🏁 <strong>Ends:</strong> Hotel InterContinental Budapest, city centre.</p>""",
        qf_badge="Gödöllő",
        qf=[("Duration", "3.5 hours"), ("Price", "From €60 / person"),
            ("Language", "English, German, Spanish, French, Italian"),
            ("Meeting Point", "Eurama office, 30 minutes before departure (hotel pickup option)"),
            ("Included", "Royal Palace of Gödöllő tour, air-conditioned bus, live guide"),
            ("Not Included", "Hotel drop-off, food and drinks"), ("Time at Destination", "About 2 hours"),
            ("Accessibility", "Not suitable for wheelchair users")],
        chips=[("yes", "✓ Palace Ticket Included"), ("yes", "✓ Half Day"), ("yes", "✓ Hotel Pickup Option"),
               ("no", "✕ Not Wheelchair Accessible")],
        perks=["Meeting: <strong>Eurama office</strong>", "Duration: <strong>3.5 Hours</strong>"],
        road=1.5, ground=2, incl="Palace tour, transport, guide",
        desc="Half-day guided tour from Budapest to the Royal Palace of Gödöllő, summer home of Empress Elisabeth (Sissi).",
    ),
    dict(
        anchor="item-7-eger-private-tour", operator="BudapestPrivate", short_op="BudapestPrivate",
        title="Eger Private Tour: Castle, Old Town and Wine Cellars",
        path="budapest-l29/eger-countryside-culture-and-wine-8-hour-tour-t62239",
        cmp="day-trips-eger", score="5.0", count_exact=17, price=255,
        dur="8 Hours", dur_short="8 hours", place="Your hotel", map="",
        cats="full o160 pickup private", photos="eger",
        alts=["Vineyards and a wine press house near Eger",
              "Glasses of white and rosé wine at an Eger tasting",
              "Historic cannon in the Eger Castle exhibition",
              "Eger old town rooftops from the castle walls",
              "View over Eger and its cathedral from the castle"],
        specs=["Private Car", "⏱ 8 Hours", "Castle Ticket Included", "Wine Cellar Valley"],
        best_for="Couples and families who want Eger's castle, Baroque old town and the cellars of the Valley of the Beautiful Women, privately and door to door.",
        pros=["Private guide and car, door to door from your hotel",
              "Eger Castle ticket, motorway and parking fees included",
              "About 5 hours in Eger: castle, minaret, old town and the wine cellar valley"],
        cons=["Most expensive trip here (€255 per person)",
              "Wine tasting and meals are paid on the spot"],
        body="""<p>Eger is the town Hungarians drive to for a long weekend: a castle famous for holding off the Ottomans in 1552, a <strong>40-metre minaret</strong> (the northernmost in Europe), a Baroque centre and the <strong>Valley of the Beautiful Women</strong>, a horseshoe of wine cellars pouring Bull's Blood (Egri Bikavér).</p>
<p>This private tour drives you there in about <strong>1.5 hours</strong> and gives you a guide for the <strong>castle and its exhibition</strong> and the old town (main square, Minorite church, the cathedral and the Lyceum), before the cellars. The castle ticket is included; you pay for the wine and food as you go.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> if you want Eger done properly in one day, at your pace, without a coach. For two or more people, private with door-to-door transport is the comfortable way to cover 280 km round trip.</p>
<p><strong>Skip it</strong> if you are on a budget: direct trains from Keleti reach Eger in about 2 hours, and the cellars are a short taxi ride from the centre.</p>
<h3>Pickup</h3>
<p>🚗 <strong>Pickup:</strong> Door to door from your Budapest accommodation by private air-conditioned car.</p>""",
        qf_badge="Eger",
        qf=[("Duration", "8 hours"), ("Price", "From €255 / person"),
            ("Language", "English, German, Hungarian"), ("Group", "Private"),
            ("Included", "Private guide, door-to-door car, Eger Castle ticket, water, motorway and parking fees"),
            ("Not Included", "Other entrance fees, meals, wine tasting"),
            ("Time at Destination", "About 5 hours"), ("Drive", "About 1.5 hours each way")],
        chips=[("yes", "✓ Private Guide and Car"), ("yes", "✓ Castle Ticket Included"),
               ("no", "✕ Wine Tasting Extra"), ("no", "✕ Meals Not Included")],
        perks=["Pickup: <strong>Your hotel</strong>", "Group: <strong>Private</strong>"],
        road=3, ground=5, incl="Private car and guide, castle ticket",
        desc="Private 8-hour day trip from Budapest to Eger: castle, Baroque old town and the wine cellars of the Valley of the Beautiful Women.",
    ),
    dict(
        anchor="item-8-heviz-thermal-lake", operator="Zala", short_op="Zala",
        title="Hévíz Thermal Lake Day Trip",
        path="heviz-l105762/heviz-wellness-escape-thermal-lake-day-trip-from-budapest-t1066247",
        cmp="day-trips-heviz", score="4.8", count_exact=49, price=155,
        dur="8 Hours", dur_short="8 hours", place="Népliget", map="Népliget+bus+station+Budapest",
        cats="full u160 small", photos="heviz",
        alts=["Lake Hévíz bathhouse on stilts from above",
              "Steam rising from Lake Hévíz in the cold",
              "Lake Hévíz bathhouse in winter with snow",
              "Misty view over Lake Hévíz and the hills",
              "Steam around the Lake Hévíz pavilion roof"],
        specs=["Lake Ticket Included", "⏱ 8 Hours", "Max 4 Guests", "Warm All Year"],
        best_for="Spa lovers who want to swim in the world's largest natural thermal lake, with the ticket and a local guide sorted, max 4 people.",
        pros=["Entry to Lake Hévíz included, plus a local guide all day",
              "Tiny group: max 4 guests",
              "The lake stays warm year round (about 25 to 36°C, cooler in winter)"],
        cons=["Roughly 5 of the 8 hours are travel; about 3 hours at the lake",
              "Meets at Népliget bus station, not your hotel; no food included; 16+ only"],
        body="""<p>Lake Hévíz is the <strong>largest natural thermal lake in the world</strong>, and you can swim in it in November: the water stays around <strong>25 to 36°C</strong> through the year, cooler in winter, steaming on cold mornings. It is near the western end of Lake Balaton, roughly 2.5 hours from Budapest.</p>
<p>This trip handles the awkward part: a direct transfer from <strong>Népliget</strong>, a local guide who sorts the tickets and points you to cafés, and the <strong>lake entry included</strong>. Groups are capped at 4.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> if you have already done Széchenyi and Gellért and want the one thermal experience Budapest can't give you: floating in a natural lake.</p>
<p><strong>Skip it</strong> if you just want a good thermal bath: you get far more pool time for less in the city (see <a href="/thermal-baths-budapest">Budapest's best thermal baths</a>). Here you spend about 3 hours in the water and 5 on the road.</p>
<h3>Meeting Point</h3>
<p>🗺️ <strong>Meeting Point: </strong>Népliget long-distance bus station, Budapest District IX.<br/>🚇 <strong>Public Transport:</strong> Népliget (M3).<br/>🎒 <strong>Bring:</strong> Swimsuit, towel, flip-flops. Lockers and changing rooms are at the lake.</p>""",
        qf_badge="Hévíz",
        qf=[("Duration", "8 hours"), ("Price", "From €155 / person"),
            ("Group Size", "Max 4 guests"), ("Meeting Point", "Népliget bus station, Budapest"),
            ("Included", "Return transfer, Lake Hévíz entry ticket, local English-speaking guide"),
            ("Not Included", "Food and drinks, spa treatments"), ("Time at Destination", "About 3 hours"),
            ("Not Suitable For", "Children under 16, pregnant women")],
        chips=[("yes", "✓ Lake Ticket Included"), ("yes", "✓ Max 4 Guests"), ("yes", "✓ Open All Year"),
               ("no", "✕ No Hotel Pickup"), ("no", "✕ Food Not Included")],
        perks=["Departure: <strong>Népliget</strong>", "Group: <strong>Max 4</strong>"],
        road=5, ground=3, incl="Transfer, guide, lake ticket",
        desc="Small-group day trip from Budapest to Lake Hévíz, the world's largest natural thermal lake, with entry included.",
    ),
    dict(
        anchor="item-9-danube-bend-with-lunch", operator="Eurama Sightseeing City Tours Budapest", short_op="Eurama",
        title="Full-Day Danube Bend Tour with 3-Course Lunch",
        path="budapest-l29/from-budapest-full-day-danube-bend-tour-with-lunch-t55698",
        cmp="day-trips-danube-lunch", score="4.2", count_exact=518, price=109,
        dur="9 Hours", dur_short="9 hours", place="Eurama office", map="",
        cats="full u160 pickup meal boat", photos="danube-lunch",
        alts=["Esztergom Basilica above the Danube at sunrise",
              "Esztergom and the Mária Valéria Bridge at sunset",
              "Rainbow umbrellas over a Szentendre street",
              "The Danube Bend and Visegrád hills from above",
              "Travellers photographing the Danube Bend from Visegrád"],
        specs=["Lunch Included", "⏱ 9 Hours", "5 Languages", "Boat Back (Summer)"],
        best_for="First-timers who want the whole Danube Bend with lunch, a guide in their language and a boat ride back on summer weekends.",
        pros=["3-course Hungarian lunch in Visegrád included",
              "Guided in English, Spanish, French, German or Italian; hotel pickup option",
              "Short hop into Slovakia over the Mária Valéria Bridge"],
        cons=["€24 more than the no-lunch version, with a bigger coach group",
              "Boat back only Friday to Sunday, 1 May to 27 September"],
        body="""<p>Same three towns as the <a href="#item-2-danube-bend-day-trip">budget Danube Bend trip</a>, with two upgrades: a <strong>3-course Hungarian lunch in Visegrád</strong> and a guide in five languages. You also cross the <strong>Mária Valéria Bridge into Slovakia</strong> for a look back at Esztergom Basilica, then see the bend from Visegrád hill and walk Szentendre's centre with the guide.</p>
<p>From <strong>1 May to 27 September</strong> the Friday, Saturday and Sunday departures come back to Budapest <strong>by boat</strong>. Wednesday departures in spring and autumn return by coach, as do all trips when the river is too high or low.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> if you want a hassle-free day where lunch is sorted and the guide speaks your language. Lunch for one in Visegrád easily costs a big part of the €24 difference.</p>
<p><strong>Skip it</strong> if you prefer to choose where you eat, or want a smaller group.</p>
<h3>Meeting Point</h3>
<p>🗺️ <strong>Meeting Point: </strong>The Eurama office in central Budapest (blue "Eurama meeting point" flag), 30 minutes before departure. Hotel pickup is available as an option.<br/>🪪 <strong>Bring:</strong> Passport or ID card.</p>""",
        qf_badge="Esztergom + Visegrád + Szentendre",
        qf=[("Duration", "9 hours"), ("Price", "From €109 / person"),
            ("Language", "English, Spanish, French, German, Italian"),
            ("Meeting Point", "Eurama office, 30 minutes before departure (hotel pickup option)"),
            ("Included", "Live guide, air-conditioned bus, 3-course lunch, boat back (Fri to Sun, 1 May to 27 Sept)"),
            ("Not Included", "Hotel drop-off, extra drinks"), ("Time at Destinations", "About 6 hours"),
            ("Accessibility", "Not suitable for wheelchair users")],
        chips=[("yes", "✓ Lunch Included"), ("yes", "✓ Boat Back in Summer"), ("yes", "✓ 5 Languages"),
               ("no", "✕ Not Wheelchair Accessible")],
        perks=["Meeting: <strong>Eurama office</strong>", "Lunch: <strong>Included</strong>"],
        road=3, ground=6, incl="Guide, transport, 3-course lunch, boat back (summer)",
        desc="Full-day guided Danube Bend tour from Budapest to Esztergom, Visegrád and Szentendre with a 3-course lunch.",
    ),
    dict(
        anchor="item-10-vienna-bratislava-free-time", operator="Blueridge s. r. o.", short_op="Blueridge",
        title="Vienna and Bratislava One-Day Trip with Free Time",
        path="vienna-l7/from-budapest-vienna-and-bratislava-day-trip-with-a-guide-t1230216",
        cmp="day-trips-vienna-bratislava", score="4.7", count_exact=344, price=177,
        dur="12 Hours", dur_short="12 hours", place="Your hotel", map="",
        cats="two o160 pickup small", photos="bratislava-vienna-free",
        alts=["Belvedere Palace reflected in its pond in Vienna",
              "Michael's Gate tower in Bratislava's old town",
              "Belvedere gardens in Vienna from above",
              "Horse carriage outside the Hofburg in Vienna",
              "Historic facades in Bratislava's old town"],
        specs=["2.5h Free per City", "⏱ 12 Hours", "Hotel Pickup", "No Extra Fees"],
        best_for="Travellers who want both capitals but prefer exploring alone: short guided parts, then about 2.5 hours of free time in each city.",
        pros=["About 2.5 hours of free time in both Bratislava and Vienna",
              "€12 cheaper than the other two-capital tour",
              "Hotel pickup and drop-off anywhere in Budapest; no mandatory extra charges"],
        cons=["Vienna's guided part is short: Belvedere gardens and an orientation drive",
              "Early start, late return; meals not included"],
        body="""<p>This is the two-capitals day for people who like to wander. In <strong>Bratislava</strong> you get a guided old-town walk and a visit to the castle, then <strong>about 2.5 hours on your own</strong> for lunch and coffee. In <strong>Vienna</strong> the guide walks you through the <strong>Belvedere Gardens</strong> (about 30 minutes) and gives a 30-minute orientation drive around the Ringstrasse, then you get another <strong>2.5 hours of free time</strong>.</p>
<p>All visits during the guided parts are free, so there are <strong>no mandatory extra costs</strong> beyond food.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> if you want the most time on your own in both cities and hotel pickup, at €177.</p>
<p><strong>Skip it</strong> if you want a guided walk in Vienna's centre: the <a href="#item-4-bratislava-vienna">Bratislava and Vienna tour</a> guides you past the Hofburg and St. Stephen's instead.</p>
<h3>Pickup</h3>
<p>🚐 <strong>Pickup:</strong> Anywhere in Budapest; exact time confirmed the day before.<br/>🪪 <strong>Bring:</strong> Passport or EU ID card for the border crossings.</p>""",
        qf_badge="Bratislava + Vienna",
        qf=[("Duration", "About 12 hours"), ("Price", "From €177 / person"),
            ("Pickup", "Hotel pickup and drop-off anywhere in Budapest"), ("Group", "Small group"),
            ("Included", "English-speaking guide, transport, water, snacks, all guided visits"),
            ("Not Included", "Meals, personal expenses"),
            ("Free Time", "About 2.5 hours in Bratislava and 2.5 hours in Vienna"),
            ("Time at Destinations", "About 7 hours")],
        chips=[("yes", "✓ Hotel Pickup"), ("yes", "✓ 5 Hours of Free Time"), ("yes", "✓ No Extra Fees"),
               ("no", "✕ Meals Not Included")],
        perks=["Pickup: <strong>Your hotel</strong>", "Duration: <strong>12 Hours</strong>"],
        road=5, ground=7, incl="Hotel pickup, guide, water, snacks",
        desc="Small-group day trip from Budapest to Bratislava and Vienna with guided highlights and about 2.5 hours of free time in each city.",
    ),
    dict(
        anchor="item-11-paty-wine-village", operator="Wine The Gap Kft.", short_op="Wine The Gap",
        title="Páty Wine Village Tour with Tastings",
        path="paty-l143933/from-budapest-paty-wine-village-tour-with-tastings-t345116",
        cmp="day-trips-paty-wine", score="4.9", count_exact=171, price=96,
        dur="3 Hours", dur_short="3 hours", place="Erzsébet tér", map="Erzsébet+tér+9+Budapest",
        cats="half u100 small meal", photos="paty",
        alts=["Old stone wine cellar in Páty with a green door",
              "Páty cellar row in the snow",
              "Red-painted wine cellar in Páty in winter",
              "Páty wine cellars under bare trees",
              "Arched stone cellar entrance in Páty"],
        specs=["Max 8 Guests", "⏱ 3 Hours", "Tapas Plate", "20 Min from Budapest"],
        best_for="A short, small-group wine outing: Páty's hobbit-like cellars 20 minutes from the city, 4 wines per cellar and a local tapas plate.",
        pros=["Just 3 hours and 20 minutes from the city: fits into an afternoon",
              "Max 8 guests, tastings with the winemakers themselves",
              "Tapas plate of local ham, sausage, cheese and olives included"],
        cons=["Adults only (18+), minimum 2 guests to run",
              "Shorter and pricier per hour than the Etyek tour"],
        body="""<p>Páty is a village <strong>20 minutes</strong> from Budapest with a lane of old earth-roofed cellars, some dug in the 1880s, that look straight out of the Shire. With a group of <strong>8 at most</strong>, you visit 1 or 2 wineries, one known for organic wine, and taste <strong>4 wines at each cellar</strong> with the winemaker.</p>
<p>The last cellar serves a <strong>tapas plate</strong> of olives, ham, sausage and cheese from local farms. Then you are back in the city 3 hours after you left.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> if you want a wine trip that fits between lunch and dinner, with a small group and winemakers who have time to talk.</p>
<p><strong>Skip it</strong> if you want a proper meal: the <a href="#item-5-etyek-wine-tour">Etyek tour</a> includes one, with more wineries, for less.</p>
<h3>Meeting Point</h3>
<p>🗺️ <strong>Meeting Point: </strong>Al Habtoor Palace Budapest, Erzsébet tér 9-10, 1051 Budapest.<br/>🚇 <strong>Public Transport:</strong> Deák Ferenc tér (M1, M2, M3).</p>""",
        qf_badge="Páty wine village",
        qf=[("Duration", "3 hours"), ("Price", "From €96 / person"),
            ("Group Size", "Max 8 guests (minimum 2)"), ("Meeting Point", "Erzsébet tér 9-10, 1051 Budapest"),
            ("Included", "Round-trip transfer, 4 wines at each cellar, tapas plate"),
            ("Time at Destination", "About 2.3 hours"), ("Age", "18+ only")],
        chips=[("yes", "✓ Max 8 Guests"), ("yes", "✓ Tapas Plate"), ("yes", "✓ Short Drive"),
               ("no", "✕ Adults Only")],
        perks=["Meeting: <strong>Erzsébet tér</strong>", "Group: <strong>Max 8</strong>"],
        road=0.7, ground=2.3, incl="Transfer, 4+ wines, tapas plate",
        desc="Three-hour small-group wine tour from Budapest to the old cellars of Páty with tastings and a local tapas plate.",
    ),
    dict(
        anchor="item-12-countryside-ranch-horse-show", operator="Licensed guide &amp; driver", short_op="Local guide",
        title="Countryside Ranch, Horse Show and Lunch",
        path="budapest-l29/from-budapest-hungarian-ranch-day-trip-with-horse-show-t432214",
        cmp="day-trips-ranch", score="4.9", count_exact=20, price=115,
        dur="5 Hours", dur_short="5 hours", place="Batthyány tér", map="Batthyány+tér+7+Budapest",
        cats="half u160 small meal", photos="ranch",
        alts=["Hungarian csikós horsemen driving a herd of horses",
              "Horseman riding standing on two horses at the ranch show",
              "Rider with a whip during the horse show",
              "Csikós in traditional dress with his horse lying down",
              "White horse in the ranch paddock"],
        specs=["Horse Show", "⏱ 5 Hours", "Max 7 Guests", "Goulash Lunch"],
        best_for="Families and animal lovers: a Hungarian cowboy horse show, a carriage ride and goulash on a working ranch, back in 5 hours.",
        pros=["Horse show, farm tour and a 15-minute carriage ride, all included",
              "Goulash and strudel lunch with a shot of pálinka included",
              "Max 7 guests; wheelchair accessible"],
        cons=["Meat menu by default (tell the guide in advance for vegetarian)",
              "Few reviews so far, though all strong"],
        body="""<p>Hungary's <strong>csikós</strong> horsemen are the reason people drive out to the plains, and this trip takes you to a working ranch about <strong>60 km from Budapest</strong> for their show: whip cracking, horses lying down on command and riders standing on two galloping horses.</p>
<p>After the show you tour the farm and stables, meet grey cattle and Racka sheep (breeds you only see in Hungary), take a <strong>15-minute carriage ride</strong> and sit down to <strong>goulash and strudel with a shot of pálinka</strong>. Groups are small, 7 at most, and you are back in about 5 hours.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> if you travel with kids or want something no city tour offers. Everything is included, so there is nothing to pay on the day.</p>
<p><strong>Skip it</strong> if you are vegetarian and can't warn the guide ahead, or you would rather see towns than countryside.</p>
<h3>Meeting Point</h3>
<p>🗺️ <strong>Meeting Point: </strong>Batthyány tér 7, 1011 Budapest (Buda side).<br/>🚇 <strong>Public Transport:</strong> Batthyány tér (M2 metro, H5 HÉV).</p>""",
        qf_badge="Hungarian countryside ranch",
        qf=[("Duration", "5 hours"), ("Price", "From €115 / person"),
            ("Group Size", "Max 7 guests"), ("Meeting Point", "Batthyány tér 7, 1011 Budapest"),
            ("Included", "Transport, guides, horse show, farm tour, 15-minute carriage ride, lunch, 1 pálinka"),
            ("Time at Destination", "About 3 hours"), ("Food", "Meat goulash and strudel; vegetarian on request"),
            ("Accessibility", "Wheelchair accessible")],
        chips=[("yes", "✓ Lunch Included"), ("yes", "✓ Horse Show Included"), ("yes", "✓ Max 7 Guests"),
               ("yes", "✓ Wheelchair Accessible")],
        perks=["Meeting: <strong>Batthyány tér</strong>", "Group: <strong>Max 7</strong>"],
        road=2, ground=3, incl="Transport, show, carriage ride, lunch",
        desc="Half-day trip from Budapest to a Hungarian countryside ranch with a horse show, carriage ride and goulash lunch.",
    ),
    dict(
        anchor="item-13-szentendre-half-day", operator="Eurama Sightseeing City Tours Budapest", short_op="Eurama",
        title="Szentendre Half-Day Tour",
        path="budapest-l29/szentendre-visegrad-tour-from-budapest-t55661",
        cmp="day-trips-szentendre", score="4.2", count_exact=392, price=70,
        dur="4 Hours", dur_short="4 hours", place="Eurama office", map="",
        cats="half u100 pickup boat", photos="szentendre-half",
        alts=["Szentendre main street with hanging lanterns",
              "Szentendre lane with a church tower",
              "Shops on a narrow Szentendre street",
              "Szentendre skyline reflected in the Danube",
              "Pink house with balconies in Szentendre"],
        specs=["Guided Walk", "⏱ 4 Hours", "Boat Back (Summer)", "5 Languages"],
        best_for="A guided half day in Szentendre's artists' village with a scheduled boat back to Budapest on summer weekends.",
        pros=["Guided walk through Szentendre's Baroque centre in 5 languages",
              "Public boat back to Budapest on Friday to Sunday tours (1 May to 27 September)",
              "Only half a day; hotel pickup available"],
        cons=["Szentendre is easy and much cheaper by HÉV train on your own",
              "Coach back on Tuesdays and out of season; food not included"],
        body="""<p>Szentendre, the <strong>artists' village</strong> at the start of the Danube Bend, is the easiest day out from Budapest. This half-day tour drives you there, walks you through the Baroque centre and its galleries and leaves you free time for cafés and the Marzipan Museum.</p>
<p>The best part runs only in summer: on <strong>Friday, Saturday and Sunday tours from 1 May to 27 September</strong> you sail back to Budapest on the scheduled public boat. Tuesday tours, and all tours out of season, return by coach.</p>
<h3>Who Should Book It</h3>
<p><strong>Pick it</strong> if you want a guide and a boat ride without planning anything, on a summer weekend.</p>
<p><strong>Skip it</strong> if you are comfortable on public transport. The <strong>H5 HÉV from Batthyány tér reaches Szentendre in about 40 minutes</strong> for a few euros, and on a weekday out of season this tour is basically that train ride with a guide.</p>
<h3>Meeting Point</h3>
<p>🗺️ <strong>Meeting Point: </strong>The Eurama office in central Budapest (blue "Eurama Meeting Point" flag), 30 minutes before departure. Hotel pickup is available as an option.</p>""",
        qf_badge="Szentendre",
        qf=[("Duration", "4 hours"), ("Price", "From €70 / person"),
            ("Language", "Spanish, English, French, German, Italian"),
            ("Meeting Point", "Eurama office, 30 minutes before departure (hotel pickup option)"),
            ("Included", "Live guide, bus there, boat back on Fri to Sun tours (1 May to 27 Sept)"),
            ("Not Included", "Hotel drop-off, food and drinks"), ("Time at Destination", "About 2.5 hours"),
            ("Accessibility", "Not suitable for wheelchair users")],
        chips=[("yes", "✓ Boat Back in Summer"), ("yes", "✓ Half Day"),
               ("no", "✕ Not Wheelchair Accessible")],
        perks=["Meeting: <strong>Eurama office</strong>", "Duration: <strong>4 Hours</strong>"],
        road=1.5, ground=2.5, incl="Guide, bus, boat back (summer)",
        desc="Half-day guided tour from Budapest to Szentendre with a public boat back on summer weekends.",
    ),
]

for i, t in enumerate(TRIPS, 1):
    t["n"] = i
    t["count"] = f"{t['count_exact']:,}"
    t["price_txt"] = f"From €{t['price']}"
    t["href"] = GYG.format(path=t["path"], cmp=t["cmp"])
    order = ORDER[t["photos"]]
    assert sorted(order) == list(range(1, len(t["alts"]) + 1)), t["photos"]
    t["photo_list"] = [f"{IMG}/{t['photos']}-{k:02d}.avif" for k in order]
    t["alts"] = [t["alts"][k - 1] for k in order]
    t["pills"] = PILLS[i]
    t["pick"], t["skip"] = PICKSKIP[i]
    t["rank"] = ("🏆 " if i == 1 else "") + f"#{i} {t['short_op']}"
    t["tag"] = {1: "bpa-gold", 2: "bpa-silver", 3: "bpa-bronze"}.get(i, "bpa-slate")
    t["per_hour"] = round(t["price"] / t["ground"])
    for p in t["photo_list"]:
        assert (ROOT / p.lstrip("/")).exists(), p

BLANK = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 500'%3E%3C/svg%3E"
SIZES = 'sizes="(max-width: 767px) 420px, (max-width: 991px) 55vw, (max-width: 1439px) 49vw, 50vw"'


def rating(t, s, where):
    """Star summary with a per-site dropdown (BPA standard). GYG entry links to the listing."""
    href = GYG.format(path=t["path"], cmp=t["cmp"].replace("day-trips-", "day-trips-rating-"))
    return (f'<div class="bpa-summary-reviews bpa-rate"><details class="bpa-lang bpa-rate-more"><summary class="bpa-rate-sum">'
            f'<span class="bpa-stars" style="--r:{t["score"]}" aria-hidden="true"></span><b class="bpa-rate-score">{t["score"]}</b>'
            f'<span class="bpa-rate-meta">{t["count"]} reviews · 1 site</span><span class="bpa-lang-chev" aria-hidden="true">▾</span></summary>'
            f'<div class="bpa-lang-pop"><strong>Rating on 1 booking site</strong><span class="bpa-rate-list">'
            f'<a class="bpa-rev-badge is-link" href="{href}" rel="nofollow sponsored noopener" target="_blank">'
            f'<img alt="GetYourGuide" class="bpa-rev-icon" loading="lazy" src="{gyg_icon(s)}"/><span class="bpa-rev-site">GetYourGuide</span>'
            f'<span class="bpa-rev-score">{t["score"]}</span><span class="bpa-rev-count">({t["count"]})</span><span class="bpa-rev-go">→</span></a>'
            f'</span></div></details></div>')


def pills(t):
    return "\n".join(f'<details class="bpa-lang"><summary class="bpa-sp"><span class="bpa-lang-label">{lab}</span>'
                     f'<span class="bpa-lang-chev" aria-hidden="true">▾</span></summary><div class="bpa-lang-pop">{pop}</div></details>'
                     for lab, pop in t["pills"])


def pickskip(t):
    return (f'<div class="bpa-best-for bpa-pickskip"><span class="bpa-pick">✓ Pick it</span> {t["pick"]} '
            f'<span class="bpa-skip">✕ Skip it</span> {t["skip"]}</div>')


def deck_card(t, s):
    first = (f'<img alt="{t["alts"][0]}" fetchpriority="high" height="534" loading="eager" {SIZES} src="{t["photo_list"][0]}" width="800"/>'
             if t["n"] == 1 else
             f'<img alt="{t["alts"][0]}" height="534" loading="lazy" {SIZES} src="{t["photo_list"][0]}" width="800"/>')
    imgs = [first] + [f'<img alt="{a}" data-src="{p}" decoding="async" loading="lazy" {SIZES} src="{BLANK}"/>'
                      for p, a in zip(t["photo_list"][1:], t["alts"][1:])]
    place = (t["place"] if not t["map"] else
             f'<a class="bpa-kicker-map-link" href="https://www.google.com/maps/search/?api=1&amp;query={t["map"]}" onclick="event.stopPropagation()" rel="noopener noreferrer" target="_blank">{t["place"]}</a>')
    return f"""<!-- #{t['n']}: {t['title']} -->
<div class="bpa-card" data-cat="{t['cats']}" id="card-{t['n']}">
<div class="bpa-main">
<div class="bpa-media">
<span class="bpa-rank-tag {t['tag']}">{t['rank']}</span>
<button aria-label="Previous photo" class="bpa-arrow prev" onclick="bpaSlide(this,-1)" type="button">‹</button>
<button aria-label="Next photo" class="bpa-arrow next" onclick="bpaSlide(this,1)" type="button">›</button>
<span class="bpa-pill">1 / {len(imgs)}</span>
<div aria-label="Photo gallery {t['n']}" class="bpa-slider" onscroll="bpaCount(this)" tabindex="0">
{chr(10).join(imgs)}
</div>
</div>
<div class="bpa-info">
<div class="bpa-kicker">{t['short_op']} • ⏱️ {t['dur']} • {place}</div>
<a class="bpa-title" href="{t['href']}" rel="nofollow sponsored noopener" target="_blank">{t['title']}</a>
<div class="bpa-reviews-line">
{rating(t, s, "deck")}
</div>
<div class="bpa-specs-row">
{pills(t)}
</div>
{pickskip(t)}
</div>
<div class="bpa-cta-cell">
<div>
<div class="bpa-price">{t['price_txt']}</div>
<div class="bpa-psub">{t['dur_short']} • Free cancellation</div>
</div>
<a class="bpa-btn" href="{t['href']}" rel="nofollow sponsored noopener" target="_blank">Check Availability →</a>
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
    pros = "".join(f"<li><strong>{x}</strong></li>" for x in t["pros"])
    cons = "".join(f"<li><strong>{x}</strong></li>" for x in t["cons"])
    n = len(t["photo_list"])
    slides = "".join(
        f'<div class="ltt-strip-slide"><img alt="{a}" loading="lazy" src="{p}"/><div class="ltt-strip-cap">'
        f'<span class="ltt-strip-num">{i} / {n}</span> <span>{a}</span></div></div>'
        for i, (p, a) in enumerate(zip(t["photo_list"], t["alts"]), 1))
    perks = "\n".join(f'<span class="ltt-buy-perk">{x}</span>' for x in
                      ["Instant Smartphone QR Voucher", "Full Refund up to 24h Before"] + t["perks"])
    qf = "\n".join(f'<div class="qf1-row"><div class="qf1-label">{a}</div><div class="qf1-val">{b}</div></div>' for a, b in t["qf"])
    chips = "\n".join(f'<span class="qf1-chip {c}">{x}</span>' for c, x in t["chips"])
    return f"""<details class="bpa-details-card" data-cat="{t['cats']}" id="{t['anchor']}" open="">
<summary class="bpa-details-summary">
<div class="bpa-details-summary-content">
<div class="bpa-details-top-row">
<span class="bpa-rank-tag {t['tag']}">{t['rank']}</span>
<div class="bpa-kicker">{t['short_op']} • ⏱️ {t['dur']} • <span class="bpa-kicker-map-link">{t['place']}</span></div>
</div>
<h3 class="bpa-details-title">{t['title']}</h3>
<div class="bpa-reviews-line">
{rating(t, s, "details")}
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
<a class="ltt-buy-cta-btn" href="{t['href']}" rel="nofollow sponsored noopener" target="_blank">
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


def A(n):
    return f"#{TRIPS[n - 1]['anchor']}"


LEAD = f"""<p>A 12-hour day trip from Budapest can mean 6 hours on a motorway. Most listings sell the total length, but what you are paying for is the <strong>time you actually spend at the castle, the lake or the wine cellar</strong>, and that ranges from about 2 hours to 7 depending on the trip.</p>
<p>So the 13 most popular day trips from Budapest are compared below on what decides the booking: <strong>hours on the ground vs hours on the road, price per destination hour, hotel pickup or meeting point, what is included</strong> (lunch, tickets, the boat back) and group size. You will also see when a <strong>train or HÉV ticket beats the tour</strong>. Only one free day? Take the <a href="#item-1-danube-bend-forest-tour"><strong>small-group Danube Bend forest tour</strong></a> (€96, max 7 guests).</p>"""

FILTERS = """<div class="ltt-integrated-filter-bar smart-filter-bar">
<div class="ltt-integrated-pills">
<button class="ltt-tab-btn active" data-cat="all" data-label="All" onclick="lttFilterItems('all', this)" type="button">All <span class="ltt-cnt"></span></button>
<span class="ltt-filter-label sf-fl">Length:</span>
<button class="ltt-tab-btn" data-cat="half" data-group="len" data-label="Half day" onclick="lttFilterItems('half', this)" type="button">Half day <span class="ltt-cnt"></span></button>
<button class="ltt-tab-btn" data-cat="full" data-group="len" data-label="Full day" onclick="lttFilterItems('full', this)" type="button">Full day <span class="ltt-cnt"></span></button>
<button class="ltt-tab-btn" data-cat="two" data-group="len" data-label="Two countries" onclick="lttFilterItems('two', this)" type="button">Two countries <span class="ltt-cnt"></span></button>
<span class="ltt-filter-label sf-fl">Price:</span>
<button class="ltt-tab-btn" data-cat="u100" data-group="price" data-label="Under €100" onclick="lttFilterItems('u100', this)" type="button">Under €100 <span class="ltt-cnt"></span></button>
<button class="ltt-tab-btn" data-cat="u160" data-group="price" data-label="€100 to €160" onclick="lttFilterItems('u160', this)" type="button">€100 to €160 <span class="ltt-cnt"></span></button>
<button class="ltt-tab-btn" data-cat="o160" data-group="price" data-label="Over €160" onclick="lttFilterItems('o160', this)" type="button">Over €160 <span class="ltt-cnt"></span></button>
<span class="ltt-filter-label sf-fl">Must have:</span>
<button class="ltt-tab-btn" data-cat="pickup" data-group="feat" data-label="Hotel pickup" onclick="lttFilterItems('pickup', this)" type="button">Hotel pickup <span class="ltt-cnt"></span></button>
<button class="ltt-tab-btn" data-cat="small" data-group="feat" data-label="Max 8 guests" onclick="lttFilterItems('small', this)" type="button">Max 8 guests <span class="ltt-cnt"></span></button>
<button class="ltt-tab-btn" data-cat="meal" data-group="feat" data-label="Food included" onclick="lttFilterItems('meal', this)" type="button">Food included <span class="ltt-cnt"></span></button>
<button class="ltt-tab-btn" data-cat="boat" data-group="feat" data-label="Boat back (summer)" onclick="lttFilterItems('boat', this)" type="button">Boat back (summer) <span class="ltt-cnt"></span></button>
</div>
</div>"""

HERO = f"""<div class="ltt-hero-wrap">
<div class="ltt-clean-card">
<div class="ltt-top-bar">
<nav aria-label="Breadcrumb" class="ltt-breadcrumbs">
<a href="/">Home</a>
<span class="ltt-bc-sep">›</span>
<span class="ltt-bc-current">{CRUMB}</span>
</nav>
<span class="ltt-hero-kicker-badge">2026 Side-by-Side Comparison</span>
</div>
<h1 class="ltt-editorial-h1">
      {H1} <span class="ltt-h1-muted">{H1_MUTED}</span>
</h1>
<div class="ltt-trust-bar">
<div class="ltt-author-cluster">
<div class="ltt-author-avatar-wrap">
<img alt="Adam Dimitrov" class="ltt-author-avatar" height="42" loading="eager" src="/assets/adam-dimitrov.webp" width="42"/>
</div>
<div class="ltt-author-meta">
<div class="ltt-author-line">
            By <a href="/about" target="_blank">Adam Dimitrov</a>, Founder &amp; Budapest Local
          </div>
<div class="ltt-author-role">13 Day Trips • Live Prices &amp; Inclusions</div>
</div>
</div>
<div class="ltt-trust-pills">
<span class="ltt-trust-pill paragraph-26"><strong>Last updated</strong>: {CHECKED_SHORT}</span>
</div>
</div>
<div class="ltt-lead-copy">
{LEAD}
</div>
{FILTERS}
</div>
</div>"""

PICKS = f"""<h2 id="which-day-trip">Which Day Trip from Budapest Should You Book?</h2>
<ul>
<li><strong>One free day, best all-rounder:</strong> <a href="{A(1)}">Danube Bend Forest Tour</a> (from €96, max 7 guests, forest walk to Visegrád Castle, then Szentendre).</li>
<li><strong>Danube Bend on a budget:</strong> <a href="{A(2)}">Danube Bend Day Trip</a> (from €85, all 3 towns, boat back on summer weekends).</li>
<li><strong>Danube Bend with lunch sorted:</strong> <a href="{A(9)}">Full-Day Danube Bend with Lunch</a> (from €109, 3-course lunch, 5 languages).</li>
<li><strong>Lake Balaton:</strong> <a href="{A(3)}">Balaton and Tihany Day Trip</a> (from €83, hotel pickup, max 8 guests).</li>
<li><strong>Vienna and Bratislava with a guide in both:</strong> <a href="{A(4)}">Bratislava and Vienna Full-Day</a> (from €189, option to end in Vienna).</li>
<li><strong>Vienna and Bratislava with more free time:</strong> <a href="{A(10)}">Vienna and Bratislava One-Day Trip</a> (from €177, about 2.5 hours free in each).</li>
<li><strong>Wine, half a day:</strong> <a href="{A(5)}">Etyek Wine Tour</a> (from €85, 8 wines and a meal) or <a href="{A(11)}">Páty Wine Village</a> (from €96, 3 hours, max 8).</li>
<li><strong>Famous wine and a castle, privately:</strong> <a href="{A(7)}">Eger Private Tour</a> (from €255 per person, door to door).</li>
<li><strong>Kids or animal lovers:</strong> <a href="{A(12)}">Countryside Ranch and Horse Show</a> (from €115, lunch included, 5 hours).</li>
<li><strong>A thermal lake, even in winter:</strong> <a href="{A(8)}">Hévíz Thermal Lake</a> (from €155, lake ticket included, max 4).</li>
<li><strong>Sissi fans, half a day:</strong> <a href="{A(6)}">Gödöllő Royal Palace</a> (from €60, palace tour included).</li>
</ul>"""


def table():
    rows = []
    for t in sorted(TRIPS, key=lambda x: x["per_hour"]):
        pick = "Hotel" if "pickup" in t["cats"].split() else "Meeting point"
        if t["n"] in (6, 9, 13):
            pick = "Meeting point (hotel option)"
        if t["n"] == 1:
            pick = "Meeting point (hotel option)"
        rows.append(f'<tr><td><a href="#{t["anchor"]}">{t["title"]}</a></td><td>{t["dur_short"]}</td>'
                    f'<td>~{t["ground"]:g} h</td><td>€{t["price"]}</td><td><strong>~€{t["per_hour"]}</strong></td>'
                    f'<td>{pick}</td><td>{t["incl"]}</td></tr>')
    return ('<div class="ltt-table-container"><table class="ltt-checklist-table"><thead><tr><th>Trip</th><th>Length</th>'
            '<th>At the destination</th><th>Price</th><th>Per destination hour</th><th>Start</th><th>Included</th></tr></thead><tbody>'
            + "".join(rows) + "</tbody></table></div>")


TIME = f"""<h2 id="time-on-the-ground">Time on the Ground vs Time on the Road</h2>
<p>The table sorts all 13 trips by <strong>price per hour you actually spend at the destination</strong>. Hours at the destination are estimated from the listed length minus the usual driving time, so treat them as approximate. What the price covers matters too: Hévíz includes the lake ticket, Etyek a meal and 8 wines.</p>
{table()}
<p>Three things stand out. <strong>The classic Danube Bend trips are the best value</strong> at roughly €14 to €18 per destination hour, because the three towns are close together. <strong>Hévíz and Eger cost the most per hour</strong>: Hévíz because 5 of its 8 hours are driving, Eger because it is private. And the <strong>two-capitals trips</strong> are long but efficient: about 6.5 to 7 hours in Bratislava and Vienna for the price.</p>"""

DIY = """<h2 id="diy-train-or-boat">When a Train or Boat Beats the Tour</h2>
<p>Some of these places are an easy public transport ride away. If you don't need a guide, here is when doing it yourself wins:</p>
<ul>
<li><strong>Szentendre:</strong> the <strong>H5 HÉV</strong> suburban train from Batthyány tér takes about 40 minutes and costs a few euros. Do it yourself unless you want the guided walk or the summer boat back.</li>
<li><strong>Vienna only:</strong> direct <strong>railjet trains from Keleti station</strong> take about 2 hours 40 minutes. An early train gives you 7 or 8 hours in Vienna, more than any tour. A tour only wins if you also want Bratislava the same day.</li>
<li><strong>Gödöllő:</strong> the <strong>H8 HÉV</strong> from Örs vezér tere takes about 45 minutes, and the palace is a short walk from the station.</li>
<li><strong>Eger:</strong> direct trains from Keleti take about 2 hours. Fine for the town; you will need a taxi or a long walk for the wine cellar valley.</li>
<li><strong>Danube Bend by boat:</strong> public boats run to Szentendre, Visegrád and Esztergom in summer only. Upstream is slow, so the smart move is coach or train out, boat back, which is exactly what the tours with a summer boat return do.</li>
</ul>
<p>Book the tour when the logistics are the hard part: <strong>Tihany and Lake Balaton in one day</strong>, <strong>Hévíz</strong> (no train, about 3 hours by bus), the <strong>ranch</strong>, the <strong>wine villages</strong> (someone else drives after 8 glasses), and <strong>all three Danube Bend towns</strong>, which public transport can't link in a day.</p>"""

BUYERS = f"""<div class="w-richtext bpa-wt-faq">
<h2 id="how-to-choose">How to Choose a Day Trip from Budapest</h2>
<h3>1. Check the season before you book a boat</h3>
<p>The boat rides back from the Danube Bend only run <strong>in summer</strong>: on the <a href="{A(2)}">budget Danube Bend trip</a> from May to September (Thursday to Sunday), on the <a href="{A(9)}">lunch version</a> and the <a href="{A(13)}">Szentendre half day</a> from 1 May to 27 September (Friday to Sunday). Low or high water also cancels them. In winter every Danube Bend tour returns by coach, so compare them on lunch, group size and price instead.</p>
<h3>2. Hotel pickup or meeting point</h3>
<p>Pickup saves you 20 to 40 minutes of getting to a meeting point before an early start. Five trips include it (<a href="{A(3)}">Balaton</a>, <a href="{A(4)}">both</a> <a href="{A(10)}">two-capital tours</a>, <a href="{A(7)}">Eger</a> and the <a href="{A(5)}">Etyek wine tour</a> from central hotels). The Eurama trips offer it as a paid option. <a href="{A(8)}">Hévíz</a> leaves from Népliget bus station, so allow time to get there.</p>
<h3>3. Group size changes the day more than the itinerary</h3>
<p>Coach tours keep a fixed timetable. With <strong>7 or 8 guests</strong> (forest tour, Balaton, Páty, the ranch) the guide can adjust stops, and you spend less time waiting for the group. <a href="{A(8)}">Hévíz</a> is capped at 4, <a href="{A(7)}">Eger</a> is private.</p>
<h3>4. Count what is included, not just the price</h3>
<p>The cheapest Danube Bend trip is €85 but lunch and the Visegrád Castle ticket are extra; the €109 version includes a 3-course lunch. The ranch (€115) and Etyek (€85) include food and everything on the program, so there is nothing to pay on the day. The two-capitals tours include no meals.</p>
<h3>5. Bring ID for anything near a border</h3>
<p>The Balaton trip and the Danube Bend lunch tour step into Slovakia, and both Vienna tours cross two borders. Take a <strong>passport or EU ID card</strong>.</p>
<p>Planning the rest of your stay? See the <a href="/best-things-to-do-budapest">best things to do in Budapest</a>, the <a href="/best-budapest-river-cruises">best Danube river cruises</a> for your evenings, the <a href="/best-walking-tours-budapest">best walking tours</a> for your first morning in the city, and the <a href="/best-food-tours-budapest">best food tours</a> if you would rather taste Hungary without leaving town. Everything else is in our <a href="/budapest-travel-guide">Budapest travel guide</a>.</p>
"""

FAQ = [
    ("What is the best day trip from Budapest?",
     f"For most first-time visitors it is the <strong>Danube Bend</strong>: Szentendre, Visegrád and Esztergom are under an hour apart, so you see the most for the least driving. The <a href=\"{A(1)}\">small-group forest tour</a> (from €96, max 7 guests) is the best-rated way to do it; the <a href=\"{A(2)}\">classic coach tour</a> is the cheapest at €85."),
    ("Can you do Vienna as a day trip from Budapest?",
     f"Yes. Direct trains from Keleti take about 2 hours 40 minutes, which gives you 7 or 8 hours in Vienna on your own. If you want Bratislava too, a guided tour with hotel pickup covers both in 12 to 13 hours from €177 (<a href=\"{A(10)}\">more free time</a>) or €189 (<a href=\"{A(4)}\">guided in both cities</a>)."),
    ("How do you get to Szentendre from Budapest?",
     "Take the <strong>H5 HÉV</strong> suburban train from Batthyány tér; it takes about 40 minutes. In summer you can come back by public boat on the Danube. A guided half-day tour costs from €70 and adds a guide and, on summer weekends, the boat back."),
    ("Is Lake Balaton worth a day trip from Budapest?",
     f"Yes, if you combine it with Tihany. The peninsula, its abbey and the lake views are the highlight, but they are hard to link by public transport in one day. The <a href=\"{A(3)}\">small-group Balaton and Tihany tour</a> (from €83, hotel pickup) covers Tihany, a lake viewpoint and Balatonfüred; plan on about 10 hours."),
    ("Can you swim in Lake Hévíz in winter?",
     f"Yes. The lake stays warm all year, about 25 to 36°C, cooler in winter, and the bathhouse and sauna stay open. The <a href=\"{A(8)}\">Hévíz day trip</a> (from €155) includes the lake ticket and a guide, but expect about 3 hours at the lake out of 8."),
    ("Do Danube Bend tours return by boat?",
     "Only in summer. Depending on the tour, the boat runs from May to September on Thursday to Sunday, or from 1 May to 27 September on Friday to Sunday. Outside those days, and when the water level is too high or low, tours return by coach."),
    ("Which day trips from Budapest include hotel pickup?",
     f"The <a href=\"{A(3)}\">Balaton and Tihany</a> trip, both <a href=\"{A(4)}\">Vienna</a> and <a href=\"{A(10)}\">Bratislava</a> tours and the <a href=\"{A(7)}\">Eger private tour</a> collect you from your accommodation; the <a href=\"{A(5)}\">Etyek wine tour</a> picks up at selected central hotels. Several others offer hotel pickup as an option."),
    ("What is the cheapest day trip from Budapest?",
     f"Among guided trips, the <a href=\"{A(6)}\">Gödöllő palace tour</a> is cheapest at €60 for 3.5 hours, palace tour included. For a full day, the <a href=\"{A(2)}\">Danube Bend day trip</a> at €85 is the best value. Cheapest of all is DIY: the HÉV to Szentendre costs a few euros."),
]


def faq_html():
    qa = "".join(f'<h3 class="cf-faq-questions-2">{q}</h3><div class="cf-faq-answer-wrap-2">'
                 f'<div class="cf-faq-content-2 w-richtext"><p>{a}</p></div></div>' for q, a in FAQ)
    return f'<h2 id="faq">Frequently Asked Questions</h2>{qa}'


METHOD = f"""<h2 id="how-we-compared">How We Compared These Day Trips</h2>
<p>Compared on {CHECKED} using live listings. For each of the 13 trips we read the current lowest price per adult, rating and review count, listed duration, what is and isn't included, meeting point or pickup, group size and seasonal rules (boat returns, age limits). Hours at the destination are our estimate: the listed length minus typical driving time between Budapest and the stops. We left out trips that start in Vienna or other cities, and private car hires without a fixed program. Prices change with the date and group size, so check the live price before you book.</p>
</div>"""


NO_RED_CSS = """<style id="bpa-no-red-hover">
/* no red hover: every link keeps its own colour or turns brand gold */
.ltt-lead-copy a:hover,.w-richtext a:hover,.bpa-wt-guide a:hover,.bpa-wt-faq a:hover,.ltt-checklist-table a:hover{color:#855a00 !important;background:transparent !important}
.bpa-title:hover{color:#855a00 !important}
.bpa-kicker-map-link:hover,.bpa-sublink:hover{color:#855a00 !important}
.bpa-btn:hover,.ltt-buy-cta-btn:hover,.hybrid-cta-btn:hover{color:#fff !important}
.bpa-lang-note a:hover{color:#855a00 !important}
</style>"""


def build():
    s = TEMPLATE.read_text()
    lock = re.search(r'<div class="ltt-buy-card-trust">\s*(<svg.*?</svg>)', s, re.S).group(1)

    # ---- head ----
    s = re.sub(r"<title>.*?</title>", f"<title>{TITLE_TAG}</title>", s, count=1)
    old_title = "10 Best Walking Tours in Budapest (Free & Paid, 2026)"
    old_desc = ("10 Budapest walking tours compared, 6 taken in person: free tip-based walks, castle caves, "
                "a food tour, communist history and private guides. From €12.")
    assert s.count(f'content="{old_desc}"') == 3
    s = s.replace(f'content="{old_desc}"', f'content="{META}"')
    s = s.replace(f'content="{old_title}"', f'content="{TITLE_TAG}"')
    s = re.sub(r'<link as="image" fetchpriority="high" href="[^"]+" rel="preload" type="image/webp"/>',
               f'<link as="image" fetchpriority="high" href="{TRIPS[0]["photo_list"][0]}" rel="preload" type="image/avif"/>', s, count=1)
    old_og = re.search(r'<meta content="([^"]+)" property="og:image"/>', s).group(1)
    s = s.replace(old_og, OG_IMG)
    # hreflang: EN only
    s = re.sub(r'<link href="[^"]+" hreflang="(?!en"|x-default")[^"]+" rel="alternate"/>', "", s)
    s = s.replace(f'"{OLD_URL}"', f'"{URL}"')

    # ---- own purged CSS copies without Webflow's red a:hover ----
    for href in re.findall(r'href="(/css/purged/best-walking-tours-budapest\.[^"]+\.css)"', s):
        css = (ROOT / href.lstrip("/")).read_text()
        css = re.sub(r'(?<![\w\-.#:\]])a:hover\{([^}]*)\}',
                     lambda m: "a:hover{" + ";".join(d for d in m.group(1).split(";")
                                                     if d.split(":")[0].strip() not in ("color", "background-color", "background-image", "opacity")) + "}",
                     css)
        assert not re.search(r"a:hover\{[^}]*(#ff421c|#f13657|#ff553340)", css), href
        base = href.split("best-walking-tours-budapest.")[1].rsplit(".", 2)[0]
        new = f"/css/purged/{SLUG}.{base}.{hashlib.sha1(css.encode()).hexdigest()[:10]}.css"
        for old_f in (ROOT / "css/purged").glob(f"{SLUG}.{base}.*.css"):
            old_f.unlink()
        (ROOT / new.lstrip("/")).write_text(css)
        s = s.replace(href, new)

    # ---- dropdown pills, star summary, pick/skip: CSS + JS from the night cruises page ----
    nc = (ROOT / "best-night-cruises-budapest.html").read_text()
    blocks = "".join(re.search(rf'<style id="{i}">.*?</style>', nc, re.S).group(0) for i in ("bpa-lang-css", "bpa-card2-css"))
    blocks += NO_RED_CSS
    s = s.replace("</head>", blocks + "</head>", 1)
    js = re.search(r'<script id="bpa-lang-js">.*?</script>', nc, re.S).group(0)
    s = s.replace("</body>", js + "</body>", 1)

    # ---- hero ----
    a = s.index('<div class="ltt-hero-wrap">')
    b = s.index('<div class="comparison-table">', a)
    s = s[:a] + HERO + s[b:]

    # ---- deck ----
    s = s.replace('id="budapest-walking-tours-deck"', 'id="budapest-day-trips-deck"')
    a = s.index('<div class="bpa-deck-wrap" id="ltt-cards-deck">') + len('<div class="bpa-deck-wrap" id="ltt-cards-deck">\n')
    end_marker = '</div>\n</div>\n</div></div><div class="blog-section-2">'
    b = s.index(end_marker, a)
    s = s[:a] + "".join(deck_card(t, s) for t in TRIPS) + s[b:]

    # ---- guide + breakdown + FAQ ----
    a = s.index('<div class="w-richtext bpa-wt-guide">')
    b = s.index('<style>.ltt-editorial-wrapper', a)
    breakdown_head = """<div class="bpa-breakdown-top-bar" id="breakdown-header">
<div>
<h2 class="bpa-breakdown-heading" id="day-trips-breakdown">Detailed Breakdown: 13 Best Day Trips from Budapest</h2>
<p class="bpa-breakdown-sub">Ranked • All reviews open by default • Click to collapse/expand</p>
</div>
<div class="bpa-acc-controls">
<button class="bpa-acc-ctrl-btn" onclick="toggleAllDetails(true)" type="button">Expand All</button>
<button class="bpa-acc-ctrl-btn" onclick="toggleAllDetails(false)" type="button">Collapse All</button>
</div>
</div>
"""
    content = ('<div class="w-richtext bpa-wt-guide">\n' + PICKS + "\n" + TIME + "\n" + DIY + "\n</div>\n\n"
               + breakdown_head + "".join(details(t, s, lock) for t in TRIPS)
               + BUYERS + faq_html() + METHOD + "\n</div>\n")
    s = s[:a] + content + s[b:]

    # ---- sticky bar + config ----
    t1 = TRIPS[0]
    s = re.sub(r'(<span class="hybrid-active-title" id="sticky-name">).*?(</span>)', rf"\g<1>{t1['title']}\g<2>", s, count=1)
    s = re.sub(r'(<span class="hybrid-active-price" id="sticky-price">).*?(</span>)', rf"\g<1>{t1['price_txt']}\g<2>", s, count=1)
    s = re.sub(r'(<a class="hybrid-cta-btn" href=")[^"]+(")', lambda m: m.group(1) + t1['href'] + m.group(2), s)
    s = re.sub(r'(<span class="hybrid-active-title" id="hybridActiveTitle">).*?(</span>)', rf"\g<1>{t1['short_op']}\g<2>", s, count=1)
    s = re.sub(r'(<span class="hybrid-active-price" id="hybridActivePrice">).*?(</span>)', rf"\g<1>{t1['price_txt']}\g<2>", s, count=1)
    s = s.replace("<span>Contents (10)</span>", f"<span>Contents ({len(TRIPS)})</span>")
    s = s.replace("<span>All 10 Walking Tours</span>", f"<span>All {len(TRIPS)} Day Trips</span>")
    s = s.replace("Jump to Tested Walking Tour", "Jump to a Day Trip")
    cfg = {"deckId": "budapest-day-trips-deck", "tocDeckLabel": "Top 13 Day Trips",
           "tocBreakdownLabel": "Detailed Breakdown (13 Day Trips)", "shortTitles": [t["title"] for t in TRIPS]}
    s = re.sub(r"window\.LTT_PAGE_CONFIG = \{.*?\};", "window.LTT_PAGE_CONFIG = " + json.dumps(cfg, ensure_ascii=False) + ";", s, count=1, flags=re.S)

    # ---- JSON-LD ----
    m = re.search(r'(<script id="ltt-schema-jsonld" type="application/ld\+json">)(.*?)(</script>)', s, re.S)
    old = json.loads(m.group(2))
    art_old = next(n for n in old["@graph"] if n["@type"] == "Article")
    lead_txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", LEAD)).strip()
    items = [{
        "@type": "ListItem", "position": t["n"], "url": f"{URL}#{t['anchor']}",
        "item": {"@type": "Product", "name": t["title"], "description": t["desc"],
                 "brand": {"@type": "Organization", "name": t["operator"].replace("&amp;", "&")},
                 "image": [f"https://www.budapestadventures.com{t['photo_list'][0]}"],
                 "aggregateRating": {"@type": "AggregateRating", "ratingValue": t["score"], "bestRating": "5",
                                     "worstRating": "1", "reviewCount": str(t["count_exact"])},
                 "offers": {"@type": "Offer", "price": str(t["price"]), "priceCurrency": "EUR",
                            "availability": "https://schema.org/InStock", "url": t["href"].replace("&amp;", "&")}},
    } for t in TRIPS]
    author = dict(art_old["author"])
    author["jobTitle"] = "Founder, Budapest Adventures"
    graph = [
        {"@type": "Article", "@id": f"{URL}#article", "mainEntityOfPage": {"@type": "WebPage", "@id": URL},
         "headline": H1, "description": META, "url": URL, "inLanguage": "en",
         "datePublished": ISO, "dateModified": ISO, "author": author, "publisher": art_old["publisher"],
         "image": [OG_IMG],
         "mainEntity": {"@type": "ItemList", "name": H1, "description": lead_txt,
                        "numberOfItems": len(TRIPS), "itemListElement": items}},
        {"@type": "BreadcrumbList", "@id": f"{URL}#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.budapestadventures.com/"},
            {"@type": "ListItem", "position": 2, "name": CRUMB, "item": URL}]},
        {"@type": "FAQPage", "@id": f"{URL}#faq", "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a_)}} for q, a_ in FAQ]},
    ]
    data = {"@context": "https://schema.org", "@graph": graph}
    s = s[:m.start(2)] + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + s[m.end(2):]

    assert "—" not in s, "em dash"
    assert "cmp=walking-tours" not in s and "Mysterium" not in s
    OUT.write_text(s)
    print("wrote", OUT.name, len(s))


if __name__ == "__main__":
    build()
