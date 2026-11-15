"""Dropdown pills, Pick/Skip lines and photo order for /best-day-trips-from-budapest.

Every fact here comes from the trip's live listing (checked 2026-11-15), except
road times and train times, which are labelled as approximate.
"""

# photo order by selling power (source photo numbers 1..n)
ORDER = {
    "danube-forest": [1, 4, 5, 2, 3],
    "danube-bend": [1, 2, 4, 3, 5],
    "balaton": [1, 3, 5, 4, 2],
    "vienna-bratislava": [2, 4, 1, 3, 5],
    "etyek": [1, 2, 6, 5, 4, 3],
    "godollo": [1, 2, 3, 4, 5],
    "eger": [5, 2, 1, 4, 3],
    "heviz": [1, 2, 3, 5, 4],
    "danube-lunch": [1, 5, 4, 2, 3],
    "bratislava-vienna-free": [1, 4, 2, 3, 5],
    "paty": [1, 5, 2, 3, 4],
    "ranch": [2, 1, 4, 3, 5],
    "szentendre-half": [1, 4, 2, 5, 3],
}

# (pill label, dropdown html) per card number
PILLS = {
    1: [
        ("👥 Max 7 Guests", "<strong>Small group in a minibus.</strong> A Mercedes Vito people carrier with leather seats, 7 guests at most, so the day runs at the group's pace.<span class=\"bpa-lang-note\">Not for children under 8.</span>"),
        ("🥾 75-Min Forest Walk", "<strong>4.6 km, gently downhill</strong> on marked trails through the Danube-Ipoly National Park, following old royal hunting paths. It ends at Visegrád Castle.<span class=\"bpa-lang-note\">Easy for average fitness. Trails can be muddy or slippery, so wear proper shoes.</span>"),
        ("🕘 09:00 to 17:00", "<strong>Leaves Batthyány tér at 09:00.</strong> The minibus leaves Szentendre for Budapest at 17:00.<span class=\"bpa-lang-note\">Want sunset on the river? Stay in Szentendre and return on your own by public boat or HÉV.</span>"),
        ("🍽️ Lunch Not Included", "<strong>Lunch stop at a forest restaurant where locals eat.</strong> You order from the menu and pay yourself; prices are lower than in Budapest.<span class=\"bpa-lang-note\">Visegrád Castle ticket also extra: €8 adults, €4 students.</span>"),
    ],
    2: [
        ("🏰 All 3 Towns", "<strong>Visegrád, Esztergom and Szentendre</strong> in one day: the medieval royal residence, Hungary's largest church with a view over to Slovakia, then the artists' village.<span class=\"bpa-lang-note\">About 6 hours at the stops, about 3 on the road (approximate).</span>"),
        ("⛴️ Boat Back (Summer)", "<strong>May to September, Thursday to Sunday:</strong> the return to Budapest is by boat, ticket included.<span class=\"bpa-lang-note\">Out of season, or when the river is too high or low, you return by coach.</span>"),
        ("🗣️ English &amp; Spanish", "<strong>Bilingual guide:</strong> commentary in English and Spanish on the same tour."),
        ("💶 Lunch Extra", "<strong>Not included:</strong> lunch, the Visegrád Castle entrance ticket and tips.<span class=\"bpa-lang-note\">Want lunch sorted? The #9 lunch version includes a 3-course meal for €24 more.</span>"),
    ],
    3: [
        ("🚐 Hotel Pickup", "<strong>Pickup and drop-off at your hotel or apartment</strong> anywhere in Budapest. Exact time and driver contact arrive the day before."),
        ("👥 Max 8 Guests", "<strong>Small group</strong> in an air-conditioned people carrier with an English-speaking driver-guide. Water and local snacks included."),
        ("⏱ About 10 Hours", "<strong>Listed as 8 hours, about 10 door to door</strong> with traffic. Roughly half of it is driving (approximate).<span class=\"bpa-lang-note\">Optional stops (Székesfehérvár, a lookout tower) depend on time and the group.</span>"),
        ("🇸🇰 Slovakia Photo Stop", "<strong>Štúrovo, across the Mária Valéria Bridge,</strong> for the classic photo of Esztergom Basilica from the other bank.<span class=\"bpa-lang-note\">Bring a passport or ID card.</span>"),
    ],
    4: [
        ("🏛️ Guided in Both Cities", "<strong>Bratislava:</strong> old town (St. Michael's Gate, Main Square, Primate's Palace, Blue Church) and the castle. <strong>Vienna:</strong> Hofburg area, St. Stephen's Cathedral, the Ring and the Opera, then free time."),
        ("🚐 Hotel Pickup", "<strong>Pickup from any accommodation in Budapest</strong> (hotel, Airbnb). Guide contact details arrive the day before."),
        ("🧳 End in Vienna Option", "<strong>You can finish the tour in Vienna with your luggage</strong>, which turns your onward transfer into a sightseeing day."),
        ("⏱ 12.5-13 Hours", "<strong>A long day:</strong> about 6.5 hours in the two cities and roughly 6 on the road (approximate).<span class=\"bpa-lang-note\">Optional stop in Győr if you wish. Wheelchair accessible.</span>"),
    ],
    5: [
        ("🍷 8 Wines", "<strong>2 family-owned boutique wineries, 4 wines at each</strong>, tasted in the cellar with snacks and finger food, poured by the winemakers.<span class=\"bpa-lang-note\">Etyek is known for crisp whites and sparkling wine.</span>"),
        ("🍲 Home-Cooked Meal", "<strong>A home-cooked meal at one of the farms</strong> to finish: starter, main and dessert. Water included.<span class=\"bpa-lang-note\">Vegetarian or gluten-free if you ask in advance. Coffee and soft drinks extra.</span>"),
        ("🚐 Central Pickup", "<strong>Pickup from selected hotels in central Budapest</strong> by air-conditioned minibus. Contact the operator before the day for the exact time and place."),
        ("⏱ 30 Min Drive", "<strong>Etyek is about 30 minutes from Budapest</strong>, so most of the 4 to 5 hours is spent tasting, not driving.<span class=\"bpa-lang-note\">Runs with a minimum of 2 guests.</span>"),
    ],
    6: [
        ("👑 Palace Tour Included", "<strong>Guided tour of the restored Royal Palace of Gödöllő</strong>, Empress Elisabeth's (Sissi's) summer residence, plus a walk in the park.<span class=\"bpa-lang-note\">Skip-the-line entry.</span>"),
        ("⏱ 3.5 Hours", "<strong>Half a day:</strong> about 2 hours at the palace, the rest is the drive (approximate). Ends at the InterContinental hotel in the city centre."),
        ("🗣️ 5 Languages", "<strong>English, German, Spanish, French and Italian.</strong> The tour may be run by a bilingual guide."),
        ("🚆 DIY Option", "<strong>The H8 HÉV from Örs vezér tere</strong> reaches Gödöllő in about 45 minutes, and the palace is a short walk from the station.<span class=\"bpa-lang-note\">Book the tour for the guided palace visit without planning anything.</span>"),
    ],
    7: [
        ("🚗 Private Car", "<strong>Private guide and car, door to door</strong> from your Budapest accommodation. About 1.5 hours each way.<span class=\"bpa-lang-note\">Motorway and parking fees, water and all taxes included.</span>"),
        ("🏰 Castle Ticket Included", "<strong>Guided visit to Eger Castle</strong> and its history exhibition, famous for holding off the Ottomans in 1552, with views over the old town.<span class=\"bpa-lang-note\">Other entrance fees are extra.</span>"),
        ("🍷 Valley of the Beautiful Women", "<strong>Historic wine cellars</strong> pouring Eger's reds, whites and rosés, including Bull's Blood (Egri Bikavér).<span class=\"bpa-lang-note\">The tasting and meals are paid on the spot.</span>"),
        ("🗣️ EN · DE · HU", "<strong>Guided in English, German or Hungarian.</strong> Old town walk: main square, Minorite church, the cathedral, the Lyceum and the 40-metre minaret."),
    ],
    8: [
        ("🎟️ Lake Ticket Included", "<strong>Entry to Lake Hévíz</strong>, the world's largest natural thermal lake, plus a local English-speaking guide who helps with tickets and tips all day.<span class=\"bpa-lang-note\">Food, drinks, spa treatments and massages extra.</span>"),
        ("👥 Max 4 Guests", "<strong>Very small group:</strong> 4 guests at most.<span class=\"bpa-lang-note\">Not for children under 16 or pregnant women.</span>"),
        ("♨️ Warm All Year", "<strong>About 25 to 36°C year round</strong>, cooler in winter. The sauna is open all year; lockers and changing rooms at the lake.<span class=\"bpa-lang-note\">Bring a swimsuit, towel, flip-flops and a water bottle.</span>"),
        ("🚌 From Népliget", "<strong>Direct return transfer from Népliget bus station</strong> (M3 metro), not from your hotel.<span class=\"bpa-lang-note\">About 3 hours at the lake, about 5 on the road (approximate).</span>"),
    ],
    9: [
        ("🍽️ 3-Course Lunch", "<strong>A 3-course Hungarian lunch in Visegrád</strong> is included.<span class=\"bpa-lang-note\">Extra drinks are paid on the spot.</span>"),
        ("⛴️ Boat Back (Summer)", "<strong>Friday, Saturday and Sunday, 1 May to 27 September:</strong> the return to Budapest is by boat.<span class=\"bpa-lang-note\">Wednesday tours in spring and autumn, and all tours in low or high water, return by coach.</span>"),
        ("🗣️ 5 Languages", "<strong>English, Spanish, French, German and Italian.</strong> The tour may be run by a bilingual guide."),
        ("🇸🇰 Slovakia Hop", "<strong>A short visit to Slovakia over the Mária Valéria Bridge</strong> for the view back at Esztergom Basilica.<span class=\"bpa-lang-note\">Bring a passport or ID card.</span>"),
    ],
    10: [
        ("🕑 2.5h Free per City", "<strong>About 2.5 hours on your own in Bratislava and 2.5 in Vienna</strong>, after the guided parts: old town walk and castle in Bratislava, Belvedere Gardens and an orientation drive in Vienna."),
        ("🚐 Hotel Pickup", "<strong>Pickup and drop-off anywhere in Budapest.</strong> The exact time is confirmed the day before. Early start, late return."),
        ("💶 No Extra Fees", "<strong>All visits during the guided parts are free</strong>, so there are no mandatory extra charges. Water and small snacks included.<span class=\"bpa-lang-note\">Meals are not included.</span>"),
        ("🪪 Bring ID", "<strong>Passport or EU ID card required</strong> for the border crossings.<span class=\"bpa-lang-note\">Wheelchair accessible.</span>"),
    ],
    11: [
        ("🍷 4 Wines per Cellar", "<strong>1 or 2 wineries, at least 4 wines at each</strong>, tasted with the winemakers. One of them makes organic wine.<span class=\"bpa-lang-note\">The cellars date back as far as 1880.</span>"),
        ("🧀 Tapas Plate", "<strong>Olives, ham, sausages and cheeses</strong> from local farmers, served at the last cellar."),
        ("👥 Max 8 Guests", "<strong>Small group, 8 at most.</strong> Runs with a minimum of 2 guests.<span class=\"bpa-lang-note\">Adults only (18+).</span>"),
        ("⏱ 20 Min Drive", "<strong>Páty is about 20 minutes from Budapest.</strong> Meet at Erzsébet tér 9-10 (Deák Ferenc tér metro) and you are back 3 hours later."),
    ],
    12: [
        ("🐎 Horse Show", "<strong>The csikós horsemen's show:</strong> whip cracking, horses lying down on command, riding standing on two horses. Photos with the cowboys included."),
        ("🛞 Carriage Ride", "<strong>A 15-minute carriage ride</strong> around the farm, plus a guided tour of the stables. You meet grey cattle and Racka sheep, breeds only found in Hungary."),
        ("🍲 Goulash Lunch", "<strong>Goulash and strudel with a shot of pálinka</strong> (fruit brandy), included.<span class=\"bpa-lang-note\">The menu contains meat. Tell the guide in advance for a vegetarian meal.</span>"),
        ("👥 Max 7 Guests", "<strong>Small group, 7 at most</strong>, meeting at Batthyány tér 7. The ranch is about 60 km from Budapest.<span class=\"bpa-lang-note\">Wheelchair accessible.</span>"),
    ],
    13: [
        ("🎨 Guided Walk", "<strong>A guided walk through Szentendre's Baroque centre</strong>, with free time for galleries, cafés, souvenir shops and the Marzipan Museum."),
        ("⛴️ Boat Back (Summer)", "<strong>Friday, Saturday and Sunday tours, 1 May to 27 September:</strong> back to Budapest on the scheduled public boat.<span class=\"bpa-lang-note\">Tuesday tours, and all tours out of season, return by coach.</span>"),
        ("🗣️ 5 Languages", "<strong>Spanish, English, French, German and Italian.</strong> The tour may be run by a bilingual guide."),
        ("🚆 DIY Option", "<strong>The H5 HÉV from Batthyány tér</strong> reaches Szentendre in about 40 minutes for a few euros.<span class=\"bpa-lang-note\">The tour adds the guide and, on summer weekends, the boat ride back.</span>"),
    ],
}

PICKSKIP = {
    1: ("for a quiet, active Danube Bend day: a forest walk into Visegrád Castle, then Szentendre, with 7 guests at most.",
        "if you want a guide talking at every stop or can't walk 75 minutes on trails."),
    2: ("for all three Danube Bend towns at the lowest price, with a boat back on summer weekends.",
        "if you want lunch included or a small group."),
    3: ("if Lake Balaton and Tihany are on your list and you have one day: hotel pickup, max 8 guests.",
        "if you want a lake day to swim and relax: about 5 of the 10 hours are in the car."),
    4: ("for two capitals with a guide in both and the option to end in Vienna with your luggage.",
        "if you only care about Vienna: the train gives you more hours there for less."),
    5: ("for a relaxed half day of wine with almost no driving: 2 wineries, 8 wines and a meal.",
        "if you want famous names like Bull's Blood or Tokaji: go to Eger."),
    6: ("if Sissi is why you came and you want the guided palace without planning trains.",
        "if you're happy on the HÉV: the DIY trip costs a fraction of the price."),
    7: ("for Eger's castle, old town and wine cellars in one comfortable private day.",
        "on a budget: direct trains reach Eger in about 2 hours."),
    8: ("to swim in the world's largest natural thermal lake, even in winter, ticket sorted.",
        "if you just want a thermal bath: Budapest's baths give more pool time for less."),
    9: ("for a hassle-free Danube Bend day with lunch included and a guide in your language.",
        "if you prefer to pick where you eat or want a smaller group."),
    10: ("for both capitals with the most time on your own: about 2.5 hours free in each.",
         "if you want a guided walk through Vienna's centre: book #4 instead."),
    11: ("for a short, small-group wine outing that fits between lunch and dinner.",
         "if you want a full meal: the Etyek tour includes one for less."),
    12: ("with kids or animal lovers: horse show, carriage ride and goulash all included.",
         "if you'd rather see towns than countryside."),
    13: ("for a guided Szentendre half day with the boat back on a summer weekend.",
         "if you're fine on public transport: the HÉV does the same trip for a few euros."),
}
