# -*- coding: utf-8 -*-
"""Verified data + editorial copy for /best-hostels-budapest (EN).

Sources, checked 14 Nov 2026:
- Ratings, addresses, house rules, dorm/private "from" prices: Hostelworld property pages.
- Booking.com scores: Booking.com listing snippets.
- Pros/cons, summaries, prices paid: Adam's own stays (9 of 10). The Hive is not stayed in,
  so it carries no "tested" claim and only verified facts.
No em dashes anywhere in this file's copy.
"""

CHECKED = "14 Nov 2026"
CHECKED_ISO = "2026-11-14"

TP = ("https://tp.media/r?marker=404154.article-best-hostels-budapest-{slug}-{place}"
      "&amp;trs=204442&amp;p=3518&amp;u={u}&amp;campaign_id=93")
HIVE_U = "https%3A%2F%2Fwww.hostelworld.com%2Fhostels%2Fp%2F96091%2Fthe-hive-party-hostel-budapest%2F"
HIVE_LINK_CARD = TP.format(slug="the-hive", place="comparison-list", u=HIVE_U)
HIVE_LINK_REVIEW = TP.format(slug="the-hive", place="reviews", u=HIVE_U)

# order = ranking on the page
HOSTELS = [
  {
    "n": 1, "id": "section-1-maverick-urban-lodge", "old": "Maverick Urban Lodge",
    "name": "Maverick Central Market", "brand": "Maverick Hostels",
    "tag": "🏆 #1 Best Overall Hostel", "short": "Best overall",
    "area": "District IX, Central Market Hall", "area_q": "Lonyay+utca+31+Budapest",
    "address": "Lónyay utca 31, 1093 Budapest", "district": "IX",
    "hw": (9.2, 3037), "bk": (8.9, 5031),
    "dorm": 10, "private": 28, "checkin": "Check-in from 15:00, check-out by 11:00",
    "rules": "No curfew",
    "cats": "tested quiet nomad kitchen budget",
    "specs": ["Privacy Curtains", "Rooftop Terrace", "Quiet Side Street", "Long-Stay Value"],
    "best_for": "Solo travelers, digital nomads and long-stay backpackers who want a social hostel without party noise.",
    "skip_if": "you want a party hostel next to the ruin bars.",
    "trust": "Privates from €28",
    "transit": "Kálvin tér (M3, M4) and Fővám tér (M4, trams 2, 47, 49), both a short walk",
    "watch": "Crowded kitchen at peak times; lock your valuables",
    "noise": "Quiet",
    "pros": [
      ("Affordable", "Off-season dorm beds started at just €9 a night. I paid €280 for 30 nights in March."),
      ("Great for Long-Term Stays", "It feels like your own college dorm room, comfortable even for a month."),
      ("Great Location", "On a quieter street in the 9th district, yet central enough for nightlife and public transport."),
      ("Great Rooms", "Modern dorm setup with large lockers and privacy curtains."),
      ("Great Bathrooms", "Shared (or private) bathrooms are well maintained, clean and of high quality."),
      ("Low Noise", "Street noise is minimal because the hostel is on a smaller street."),
    ],
    "cons": [
      ("Kitchen", "Can feel cramped at peak times and the equipment needs replacing. It gets dirty fast, though they clean it daily. The fridge was constantly full and disorganized."),
      ("Theft", "I had a pullover and a box of nasal strips stolen. This can happen in any hostel, not just Maverick. <strong>Always put your valuables in secure storage</strong>."),
    ],
    "summary": [
      "<strong>Maverick Central Market is the place for comfort seekers on a short or long stay.</strong> It's like your own college dorm room, comfortable enough for month-long stays.",
      "It's not a <a href=\"#section-2-hostel-one\">party hostel</a>, but there are <strong>plenty of chances to be social</strong> and meet people.",
      "It's <strong>exceptional value for money</strong>: I stayed here for <strong>30 nights in March for €280</strong> (about €9.33 a night). Dorm beds start <strong>from about €10</strong> on near dates when I checked on " + CHECKED + ", and prices stay reasonable in high season for this quality.",
    ],
    "video": ("https://youtu.be/hJB53XdmJSY", "video review of Maverick Central Market"),
    "groups": [
      ("Rooms, Beds &amp; Sleep Quality", "rooms and beds", [
        ("Dorm Beds With Privacy Curtains", "<p>The dorms are set up in a <strong>modern style with privacy curtains and large lockers</strong>, so even a full room feels calm.</p>"),
        ("Quiet Nights", "<p>It sits on a <strong>smaller side street in the 9th district</strong>, away from the party streets of the 7th. Street noise was minimal during my 30 nights.</p>"),
        ("Real Long-Stay Value", "<p><strong>30 nights in March cost me €280.</strong> For a digital nomad base or a slow trip, I haven't found better value in central Budapest.</p>"),
      ]),
      ("Atmosphere &amp; Social Life", "common areas", [
        ("Social, Not a Party Hostel", "<p>It feels like a friendly university dorm. <strong>You meet people easily</strong> in the common areas without 4 AM shouting in the corridors.</p>"),
        ("Who You'll Meet", "<p>Solo travelers, long-stayers and remote workers. Perfect if you want company in the evening and a good night's sleep after.</p>"),
      ]),
      ("Facilities, Kitchen &amp; Bathrooms", "facilities", [
        ("Bathrooms", "<p>Shared and private bathrooms were <strong>clean and high quality</strong>, one of the best parts of my stay.</p>"),
        ("Kitchen Reality", "<p>The guest kitchen gets <strong>cramped at peak times</strong>, the equipment is tired and the fridge is always full. Label your food.</p>"),
        ("Lock Your Things", "<p>I had a pullover and a box of nasal strips stolen. <strong>Use the lockers</strong> for anything you'd miss.</p>"),
      ]),
    ],
    "chips": [("yes", "Privacy Curtains"), ("yes", "Rooftop Terrace"), ("yes", "Guest Kitchen"), ("yes", "24 Hour Reception"), ("yes", "Free Luggage Storage")],
    "tested": True,
  },
  {
    "n": 2, "id": "section-2-hostel-one", "old": "Hostel One",
    "name": "Onefam Budapest", "brand": "Onefam",
    "tag": "#2 Best Social Hostel for Solo Travelers", "short": "Best for solo travelers",
    "area": "District VII, Jewish Quarter", "area_q": "Rumbach+Sebestyen+utca+6+Budapest",
    "address": "Rumbach Sebestyén utca 6, 1075 Budapest", "district": "VII",
    "hw": (9.7, 6588), "bk": (9.4, 1048),
    "dorm": 14, "private": None, "checkin": "Check-in 15:00 to 23:00, check-out by 11:00",
    "rules": "Ages 18 to 39 only, no curfew",
    "cats": "tested party",
    "specs": ["Free Daily Activities", "Bar Crawls", "Ages 18 to 39", "Deák tér"],
    "best_for": "Solo travelers aged 18 to 39 who want an instant crew, daily activities and nights out.",
    "skip_if": "you are over 39, travel as a couple wanting privacy, or want early nights.",
    "trust": "Ages 18 to 39",
    "transit": "Deák Ferenc tér (M1, M2, M3 and the 100E airport bus), about a 4 minute walk",
    "watch": "Pricier than most; ages 18 to 39 only",
    "noise": "Lively until about midnight",
    "pros": [
      ("Best Party Hostel", "You'll have loads of fun with drinking games at the bar, partying in the ruin pubs afterward, or sightseeing during the day."),
      ("Organized Activities", "Onefam runs daytime and night activities (pub crawls, drinking games)."),
      ("Perfect Location", "Dead center in the Jewish Quarter, close to the 100E airport bus stop, the sights and the nightlife."),
      ("Great Rooms", "Spacious rooms with secure storage and lockers. Beds give you privacy and comfort."),
      ("Low Noise", "Noise levels are reasonable, with the party usually winding down around 11 PM to midnight."),
    ],
    "cons": [
      ("Lack of Bedside Storage", "There's no storage space on the bunks for earphones, wallets and phones."),
      ("Shower Issues", "The water temperature can fluctuate, and the lights switch off because of a badly placed sensor in the shower area."),
      ("Price", "Pricier than other Budapest hostels. The social life and party experience make it worth the extra cost."),
    ],
    "summary": [
      "<strong>Onefam Budapest is the best choice if you love socializing, making friends and partying.</strong>",
      "It costs more than most Budapest hostels, but you get your money's worth if you want an outgoing, social stay. Note the <strong>age limit of 18 to 39</strong>.",
    ],
    "video": ("https://youtu.be/e8HHIXO8d_8", "video review of Onefam Budapest"),
    "groups": [
      ("Rooms, Beds &amp; Sleep Quality", "rooms and beds", [
        ("Spacious Dorms, Secure Storage", "<p>Rooms are <strong>spacious with secure storage and lockers</strong>, and the beds give you privacy and comfort.</p>"),
        ("No Bedside Shelf", "<p>There's <strong>nowhere on the bunk to put your phone, earphones or wallet</strong>. Keep a small pouch.</p>"),
        ("When It Gets Quiet", "<p>The party usually <strong>winds down around 11 PM to midnight</strong>, then the crowd heads out to the ruin bars.</p>"),
      ]),
      ("Atmosphere &amp; Social Life", "common areas", [
        ("Instant Crew", "<p>If you arrive solo and want friends on easy mode, <strong>this is the one</strong>. The staff pull everyone in.</p>"),
        ("Day and Night Activities", "<p>Free daytime activities, then drinking games and <strong>pub crawls</strong> into the Jewish Quarter at night.</p>"),
      ]),
      ("Facilities, Bathrooms &amp; Location", "facilities", [
        ("Shower Quirks", "<p>Water temperature can fluctuate and a <strong>motion sensor turns the shower lights off</strong> mid-shower.</p>"),
        ("Jewish Quarter Base", "<p>A few minutes from <strong>Deák Ferenc tér and the 100E airport bus</strong>, and walking distance home from the bars.</p>"),
      ]),
    ],
    "chips": [("yes", "Free Daily Activities"), ("yes", "Hostel Bar"), ("yes", "24/7 Kitchen Access"), ("yes", "Free Security Lockers"), ("no", "Ages 18 to 39 Only")],
    "tested": True,
  },
  {
    "n": 3, "id": "section-3-avenue-hostel", "old": "Avenue Hostel",
    "name": "Avenue Hostel", "brand": "Avenue Hostel",
    "tag": "#3 Best Budget Hostel", "short": "Cheapest bed",
    "area": "District VI, Oktogon", "area_q": "Oktogon+ter+4+Budapest",
    "address": "Oktogon tér 4, 1061 Budapest", "district": "VI",
    "hw": (8.9, 9485), "bk": (8.6, 15668),
    "dorm": 8, "private": None, "checkin": "Check-in 14:00 to midnight, check-out by 11:00",
    "rules": "Ages 6 to 49, no curfew",
    "cats": "tested budget",
    "specs": ["Free Breakfast", "Privacy Curtains", "24/7 Trams", "Oktogon"],
    "best_for": "Budget travelers who want the cheapest central bed, free breakfast and cheap dinners.",
    "skip_if": "you are a light sleeper or want a social, personal vibe.",
    "trust": "Free breakfast",
    "transit": "Oktogon (M1 and the 24 hour trams 4 and 6) right outside",
    "watch": "Loud tram corner; bring earplugs",
    "noise": "Loud (tram junction)",
    "pros": [
      ("Best Value", "Off-season rates started at just €8 a night, including a free breakfast and a discounted dinner."),
      ("Money Saver", "Food prices are high in Hungary, so the free and discounted meals save you a lot."),
      ("Staff", "Helpful, efficient and available 24/7."),
    ],
    "cons": [
      ("Quality of Life", "The comfort, privacy and cleanliness of the 10-bed room I stayed in were mediocre."),
      ("No Free Padlock", "Padlocks aren't included for the room lockers, but you can buy one for about €3."),
      ("Impersonal", "No social atmosphere, personal touch or events, except in the dining area."),
      ("Loud", "It's next to a big intersection with trams passing by. Bring earplugs."),
    ],
    "summary": [
      "<strong>Avenue Hostel is the go-to for budget travelers who want to save on both the bed and meals in Budapest.</strong>",
      "Beds start <strong>from about €8</strong>, with a <strong>free breakfast</strong> and discounted dinners (with a small minimum bar spend when I stayed). With Hungary's high food prices, that adds up.",
      "It isn't luxury, but it's practical and cheap, a solid pick for budget-focused travelers.",
      "📝 <strong>Editor's note:</strong> the 10-bed \"veiled\" room I stayed in, and its shared bathrooms, were not great. The rest of the hostel has nicer 4, 8 and 12-bed rooms at a higher price, so the hostel deserves a kinder verdict than my room alone.",
    ],
    "video": ("https://youtu.be/JXyzhhnOo9I", "video review of Avenue Hostel"),
    "groups": [
      ("Rooms, Beds &amp; Sleep Quality", "rooms and beds", [
        ("Pick a Better Room", "<p>My 10-bed room was the weak spot. <strong>The 4, 8 and 12-bed rooms are nicer</strong> and worth the few extra euros.</p>"),
        ("Earplugs Are Mandatory", "<p>It sits on the <strong>Oktogon junction with trams passing all night</strong>. Light sleepers should look at Maverick or Zen.</p>"),
        ("Locker Padlock", "<p>Padlocks aren't included. <strong>Bring one</strong> or buy one at reception for about €3.</p>"),
      ]),
      ("Atmosphere &amp; Social Life", "common areas", [
        ("Practical, Not Personal", "<p>Don't expect events or a host who knows your name. <strong>The dining area is where people mix.</strong></p>"),
        ("Who It Suits", "<p>Students and long-trip backpackers counting every euro, who mostly use the hostel to sleep and eat.</p>"),
      ]),
      ("Meals, Facilities &amp; Location", "facilities", [
        ("Free Breakfast, Cheap Dinner", "<p>A <strong>free breakfast</strong> and discounted dinners are the real selling point. They save you more per day than the bed costs.</p>"),
        ("24/7 Staff and Transport", "<p>Reception is open 24/7, and <strong>M1 plus the 24 hour trams 4 and 6</strong> stop at the door.</p>"),
      ]),
    ],
    "chips": [("yes", "Free Breakfast"), ("yes", "Privacy Curtains"), ("yes", "24 Hour Reception"), ("yes", "Guest Kitchen"), ("no", "Bring a Padlock")],
    "tested": True,
  },
  {
    "n": 4, "id": "section-4-flow-spaces", "old": "Flow Spaces",
    "name": "Flow Spaces", "brand": "Flow Spaces",
    "tag": "#4 Best for Digital Nomads", "short": "Best for digital nomads",
    "area": "District IX, Central Market Hall", "area_q": "Gonczy+Pal+utca+2+Budapest",
    "address": "Gönczy Pál utca 2, 1093 Budapest", "district": "IX",
    "hw": (8.9, 4563), "bk": (8.3, 6820),
    "dorm": 10, "private": None, "checkin": "Check-in 15:00 to midnight, check-out by 11:00",
    "rules": "No curfew",
    "cats": "tested budget nomad kitchen",
    "specs": ["Coworking Space", "Free Padlock", "Pod Beds", "Market Hall"],
    "best_for": "Digital nomads and travelers who want a laptop-friendly lounge, pod beds and a sociable but calm vibe.",
    "skip_if": "you have heavy luggage (3rd floor, no elevator) or want private bathrooms.",
    "trust": "Coworking space",
    "transit": "Fővám tér (M4, trams 2, 47, 49) and Kálvin tér (M3, M4)",
    "watch": "Co-ed communal bathrooms; 3rd floor, no elevator",
    "noise": "Calm",
    "pros": [
      ("Staff", "Front desk available 24/7, with friendly and helpful reception staff."),
      ("Welcoming", "Social atmosphere, easy to meet other travelers."),
      ("Great Beds", "Curtains for privacy, a power socket, a lamp, an item tray and a storage box."),
      ("Secure Item Stash", "Free padlock included."),
      ("Work Area", "A lounge with a laptop-friendly work area."),
    ],
    "cons": [
      ("Bathrooms", "Bathrooms are co-ed and communal, with little privacy."),
      ("No Elevator", "The hostel is on the 3rd floor."),
      ("Hygiene", "My sheet had hairs on it although it was washed. The hostel is hygienic overall."),
      ("Packed Fridges", "I lost some food I bought."),
      ("Cramped Rooms", "There was little space to move around."),
    ],
    "summary": [
      "<strong>Flow Spaces blends a hostel's social life with a hotel's calm</strong>, ideal if you want a middle ground.",
      "The vibe is like a college dorm, a good fit for budget travelers who want balance. Dorm beds start <strong>from about €10</strong>.",
      "With a welcoming atmosphere, a <strong>quiet workspace</strong> and a well-equipped kitchen, it's a hostel worth considering.",
    ],
    "groups": [
      ("Rooms, Beds &amp; Sleep Quality", "rooms and beds", [
        ("Well-Equipped Pods", "<p>Each bed has a <strong>privacy curtain, socket, lamp, item tray and storage box</strong>, with a free padlock.</p>"),
        ("Tight Rooms", "<p>The rooms are <strong>cramped</strong>; there's little space to move when everyone is unpacking.</p>"),
      ]),
      ("Atmosphere &amp; Workspace", "common areas", [
        ("Laptop-Friendly Lounge", "<p>The lounge has a <strong>proper work area</strong> and the hostel lists a coworking space, the best setup here for remote work.</p>"),
        ("Social but Balanced", "<p>Easy to meet people, without party-hostel nights. Think college dorm, not bar crawl HQ.</p>"),
      ]),
      ("Facilities, Bathrooms &amp; Location", "facilities", [
        ("Bathrooms and Stairs", "<p>Bathrooms are <strong>co-ed and communal</strong>, and the hostel is on the <strong>3rd floor with no elevator</strong>.</p>"),
        ("Kitchen and Fridges", "<p>The kitchen is well equipped, but fridges get packed and <strong>I lost some food</strong>. Label everything.</p>"),
        ("Next to the Market Hall", "<p>The <strong>Central Market Hall is one building away</strong> and the Danube is a few minutes' walk.</p>"),
      ]),
    ],
    "chips": [("yes", "Coworking Space"), ("yes", "Free Padlock"), ("yes", "Privacy Curtains"), ("yes", "24 Hour Reception"), ("no", "No Elevator (3rd Floor)")],
    "tested": True,
  },
  {
    "n": 5, "id": "section-5-a-o-budapest-city-hostel", "old": "A&amp;O Budapest City Hostel",
    "name": "a&amp;o Budapest City", "brand": "a&amp;o Hostels",
    "tag": "#5 Best Hotel-Style Hostel", "short": "Best hotel-style stay",
    "area": "District VII, near Oktogon", "area_q": "Csengery+utca+11+Budapest",
    "address": "Csengery utca 11, 1074 Budapest", "district": "VII",
    "hw": (8.6, 504), "bk": (7.7, 5373),
    "dorm": 12, "private": None, "checkin": "Check-in and check-out at the 24 hour reception",
    "rules": "Families and groups welcome",
    "cats": "tested quiet private nomad",
    "specs": ["Quiet Rooms", "Great Shower", "Work Lounge", "Private Rooms"],
    "best_for": "Couples, families and anyone who wants a quiet, simple, clean room over a social scene.",
    "skip_if": "you want a social hostel or hate paying extra for linens.",
    "trust": "Private rooms",
    "transit": "Oktogon (M1, trams 4 and 6) and Vörösmarty utca (M1), a few minutes' walk",
    "watch": "Linens about €3 extra; bring a padlock",
    "noise": "Quiet",
    "pros": [
      ("Excellent Rooms", "Simple, quiet and clean room, with a mind-blowing shower."),
      ("Secure Storage", "They happily stored my laptop in the secure storage at reception."),
      ("Work Area", "The lounge has a superb laptop-friendly work area."),
    ],
    "cons": [
      ("Bed Linens and Towels", "Not free; they cost an extra 1,150 HUF (about €3)."),
      ("Item \"Cage\"", "A padlock is NOT included for the room's item cage."),
      ("Dirty Pillow", "My pillow could have used a replacement, but the hostel is hygienic overall."),
      ("Bland Breakfast", "A typical hotel breakfast for about €8 (optional)."),
    ],
    "summary": [
      "<strong>a&amp;o Budapest City is the go-to for budget travelers who value comfort and quiet over a buzzing social scene.</strong>",
      "Beds start <strong>from about €12</strong>, but remember the extra charge for linens (about €3).",
      "Despite small downsides like the pillow and the linen fee, the price and convenience make it a good pick for no-frills travelers who want a calm place and a workspace.",
    ],
    "groups": [
      ("Rooms, Beds &amp; Sleep Quality", "rooms and beds", [
        ("Quiet, Clean, Simple", "<p>A <strong>simple, quiet and clean room</strong> with a seriously good shower. Closer to a budget hotel than a hostel.</p>"),
        ("Budget the Extras", "<p><strong>Linens cost about €3</strong> and the item cage needs your own padlock. Bring both into your price comparison.</p>"),
      ]),
      ("Atmosphere &amp; Workspace", "common areas", [
        ("Calm Base, Not a Scene", "<p>Few hostel-style mixers. It suits travelers who want <strong>privacy and sleep</strong>, couples and families.</p>"),
        ("Laptop Lounge", "<p>The lounge has a <strong>superb laptop-friendly work area</strong>.</p>"),
      ]),
      ("Facilities &amp; Location", "facilities", [
        ("Secure Storage", "<p>Reception <strong>stored my laptop</strong> safely while I was out.</p>"),
        ("Breakfast", "<p>An <strong>optional hotel-style breakfast for about €8</strong>. Fine, nothing special.</p>"),
        ("Location", "<p>On Csengery utca, a few minutes' walk from <strong>Oktogon and Andrássy út</strong>.</p>"),
      ]),
    ],
    "chips": [("yes", "Quiet Rooms"), ("yes", "Private Rooms"), ("yes", "Work Lounge"), ("no", "Linens Extra (about €3)"), ("no", "Bring a Padlock")],
    "tested": True,
  },
  {
    "n": 6, "id": "section-6-wombat-s-city-hostel", "old": "Wombat's City Hostel",
    "name": "Wombat's City Hostel", "brand": "Wombat's",
    "tag": "#6 Best Low-key Party Hostel", "short": "Best low-key party hostel",
    "area": "District VI, Király utca", "area_q": "Kiraly+utca+20+Budapest",
    "address": "Király utca 20, 1061 Budapest", "district": "VI",
    "hw": (9.0, 14947), "bk": (8.4, 2575),
    "dorm": 11, "private": None, "checkin": "Check-in 14:00 to 23:00, check-out by 10:00",
    "rules": "No curfew",
    "cats": "tested party private",
    "specs": ["En-Suite Dorms", "Bed Curtains", "Hostel Bar", "Király utca"],
    "best_for": "Backpackers who want a social bar and nightlife on the doorstep, but still a good night's sleep.",
    "skip_if": "you want the cheapest bed or a hostel with real character.",
    "trust": "En-suite dorms",
    "transit": "Deák Ferenc tér (M1, M2, M3 and the 100E airport bus), a 3 minute walk",
    "watch": "Price is high for what you get",
    "noise": "Quiet inside",
    "pros": [
      ("Welcoming", "An easygoing social atmosphere, easy to meet people."),
      ("Not Noisy", "Quiet for a party hostel. You can get a good night's rest."),
      ("Staff", "Front desk available 24/7 and a secure luggage room."),
    ],
    "cons": [
      ("Price", "Prices could be more reasonable. I didn't feel the hostel offered anything special to justify them."),
    ],
    "summary": [
      "<strong>Wombat's City Hostel is a hub for young travelers who want Budapest's nightlife</strong>, with youthful energy and a laid-back vibe that make it an ideal low-key party hostel.",
      "It's priced above most Budapest hostels. Its location is a major selling point, but some facilities are ordinary: the bathrooms, for example, are clean but nothing more.",
      "The highlight was the guests: meeting and going out with interesting travelers from around the world more than made up for the minor issues.",
    ],
    "groups": [
      ("Rooms, Beds &amp; Sleep Quality", "rooms and beds", [
        ("En-Suite Rooms", "<p>Every room has an <strong>en-suite bathroom and air conditioning</strong>, and dorm beds have personal curtains, per the hostel.</p>"),
        ("Sleeps Better Than It Parties", "<p>For a party hostel it's <strong>quiet at night</strong>. I slept well.</p>"),
      ]),
      ("Atmosphere &amp; Social Life", "common areas", [
        ("Low-Key Party Crowd", "<p>Easy to meet people at the <strong>hostel bar</strong>, then the Gozsdu Udvar bars are steps away.</p>"),
        ("The Guests Make It", "<p>The international crowd was <strong>the best part of my stay</strong>.</p>"),
      ]),
      ("Facilities &amp; Location", "facilities", [
        ("Ordinary but Clean", "<p>Facilities are <strong>clean but ordinary</strong>; don't book it for design.</p>"),
        ("Central on Király utca", "<p>A few minutes from <strong>Deák Ferenc tér</strong>, the 100E airport bus and the Jewish Quarter nightlife.</p>"),
      ]),
    ],
    "chips": [("yes", "En-Suite Dorms"), ("yes", "Air Conditioning"), ("yes", "Hostel Bar"), ("yes", "24 Hour Reception"), ("yes", "Free Security Lockers")],
    "tested": True,
  },
  {
    "n": 7, "id": "section-7-zen-hostel", "old": "Zen Hostel",
    "name": "Central Market Hall Zen Hostel", "brand": "Zen Hostel",
    "tag": "#7 Best Quiet &amp; Homely Hostel", "short": "Best quiet, homely stay",
    "area": "District IX, Central Market Hall", "area_q": "Vamhaz+korut+5+Budapest",
    "address": "Vámház körút 5, 1093 Budapest", "district": "IX",
    "hw": (8.5, 510), "bk": (8.4, 1970),
    "dorm": 11, "private": 15, "checkin": "Check-in 14:00 to 21:00, check-out by 11:00",
    "rules": "Reception limited hours",
    "cats": "tested quiet private",
    "specs": ["Homely Vibe", "Small Hostel", "Free Tea &amp; Coffee", "Market Hall"],
    "best_for": "Introverts and slow travelers who want a small, cozy, home-like place by the Danube.",
    "skip_if": "you arrive late at night, need a locker, or need a desk with a socket.",
    "trust": "Check-in until 21:00",
    "transit": "Fővám tér (M4, trams 2, 47, 49), next to the Central Market Hall",
    "watch": "No late check-in; no lockable stash",
    "noise": "Quiet",
    "pros": [
      ("Staff", "One host ran the whole hostel when I stayed: friendly, helpful and upbeat. She's the reason it gets 9/10 ratings."),
      ("Welcoming", "You could strike up conversations anywhere. The living room sofa was a great place to chat."),
      ("Feels Like Home", "If you like a cozy, homely feel, this is heaven."),
    ],
    "cons": [
      ("No 24/7 Check-In", "The host left at 9 PM, and checking in took a long time."),
      ("Understaffed", "One person juggled too many tasks; she needed at least one more colleague."),
      ("Not Secure", "No lockable item stash available."),
      ("Not Nomad-Friendly", "No workspace with sockets."),
    ],
    "summary": [
      "<strong>Central Market Hall Zen Hostel is a lovely retreat if you want a small, cozy place that feels more like a home than a hostel.</strong>",
      "Prices are slightly above average for what you get, with dorm beds <strong>from about €11</strong>. Not the best value, but if you cherish a homey vibe and a location next to the Market Hall, it's worth it.",
    ],
    "groups": [
      ("Rooms &amp; Sleep Quality", "rooms and beds", [
        ("Small and Peaceful", "<p>A <strong>small hostel with a calm, home-like feel</strong>, no party crowd.</p>"),
        ("No Lockable Stash", "<p>There was <strong>no lockable storage</strong> when I stayed. Keep valuables on you or pick another hostel if that matters.</p>"),
      ]),
      ("Atmosphere &amp; Living Room", "common areas", [
        ("Living Room Conversations", "<p>The <strong>living room sofa</strong> is where everyone ends up chatting. Board games, tea and coffee through the day.</p>"),
        ("Not for Remote Work", "<p>No desk with sockets. <strong>Digital nomads should pick Flow Spaces or Maverick.</strong></p>"),
      ]),
      ("Check-In &amp; Location", "facilities", [
        ("Arrive Before 21:00", "<p>Check-in runs <strong>14:00 to 21:00</strong> and reception hours are limited. Late flight? Book elsewhere.</p>"),
        ("Next to the Market Hall", "<p>On Vámház körút by the <strong>Central Market Hall and Liberty Bridge</strong>, with M4 and tram 2 at Fővám tér.</p>"),
      ]),
    ],
    "chips": [("yes", "Homely Atmosphere"), ("yes", "Free Tea &amp; Coffee"), ("yes", "Next to Market Hall"), ("no", "Check-In Until 21:00"), ("no", "No Lockable Stash")],
    "tested": True,
  },
  {
    "n": 8, "id": "section-8-adagio-hostel-2-0-basilica", "old": "Adagio Hostel 2.0 Basilica",
    "name": "Adagio Hostel 2.0 Basilica", "brand": "Adagio Hostels",
    "tag": "#8 Best Location for Sightseeing", "short": "Best for sightseeing",
    "area": "District VI, Andrássy út", "area_q": "Andrassy+ut+2+Budapest",
    "address": "Andrássy út 2 (1st floor), 1061 Budapest", "district": "VI",
    "hw": (8.9, 2143), "bk": (8.5, 4410),
    "dorm": 11, "private": 22, "checkin": "Check-in 15:00 to midnight, check-out by 10:00",
    "rules": "No curfew",
    "cats": "tested budget quiet private",
    "specs": ["Basilica Views", "Private Bathrooms", "Free Tea &amp; Coffee", "Andrássy út"],
    "best_for": "Sightseers who want a calm, clean bed at the start of Andrássy út, steps from St. Stephen's Basilica.",
    "skip_if": "you want a social hostel or are sensitive to traffic noise.",
    "trust": "Steps from the Basilica",
    "transit": "Bajcsy-Zsilinszky út (M1) at the door, Deák Ferenc tér (M1, M2, M3) a short walk",
    "watch": "Traffic noise; no elevator (1st floor)",
    "noise": "Traffic noise",
    "pros": [
      ("Great Bathroom", "Excellent, clean private bathroom."),
      ("Excellent Location", "With views of St. Stephen's Basilica."),
      ("Peaceful", "Not as busy as some other hostels, so you get more privacy."),
    ],
    "cons": [
      ("Noisy", "Noise in my room was high because of the traffic."),
      ("No Elevator", "The hostel is on the first floor."),
      ("Impersonal", "No social atmosphere or personal touch."),
    ],
    "summary": [
      "<strong>Adagio 2.0 is your place if a good night's sleep in a clean, comfortable room matters most.</strong>",
      "It lacks a wow factor, but it does the basics right: a solid pick for budget, minimalist accommodation in a fantastic location.",
      "It won't burn a hole in your pocket either, with dorm beds <strong>from about €11</strong> and private rooms <strong>from about €22</strong> on near dates.",
    ],
    "groups": [
      ("Rooms &amp; Sleep Quality", "rooms and beds", [
        ("Clean Rooms, Great Bathroom", "<p>My room had an <strong>excellent, clean private bathroom</strong>. Dorms and doubles with private bathrooms are available.</p>"),
        ("Traffic Noise", "<p>Andrássy út is a main road and <strong>my room was noisy from traffic</strong>. Bring earplugs or ask for a courtyard-side room.</p>"),
      ]),
      ("Atmosphere", "common areas", [
        ("Calm, Not Social", "<p><strong>No social scene or personal touch.</strong> It's a quiet base for sightseeing, not a place to make friends.</p>"),
      ]),
      ("Facilities &amp; Location", "facilities", [
        ("Kitchen, Tea and Coffee", "<p>Guests can use the <strong>fully equipped kitchens</strong>, with free self-service tea and coffee and free linen, per the hostel.</p>"),
        ("First Floor, No Elevator", "<p>It's on the <strong>first floor of a palace building without an elevator</strong>, one flight of stairs.</p>"),
        ("Unbeatable for Sights", "<p>At the start of <strong>Andrássy út</strong>, a few minutes' walk from St. Stephen's Basilica, the Opera and Deák Ferenc tér.</p>"),
      ]),
    ],
    "chips": [("yes", "Basilica Views"), ("yes", "Guest Kitchen"), ("yes", "24 Hour Reception"), ("yes", "Free Tea &amp; Coffee"), ("no", "No Elevator (1st Floor)")],
    "tested": True,
  },
  {
    "n": 9, "id": "section-9-das-nest-budapest", "old": "Das Nest Budapest",
    "name": "Das Nest Budapest", "brand": "Das Nest",
    "tag": "#9 Best Small Homely Hostel", "short": "Best small, homely hostel",
    "area": "District VII, Jewish Quarter", "area_q": "Akacfa+utca+10+Budapest",
    "address": "Akácfa utca 10, 1072 Budapest", "district": "VII",
    "hw": (8.7, 1507), "bk": (8.4, 1474),
    "dorm": 15, "private": 17, "checkin": "Check-in 12:00 to 23:00, check-out by 11:00",
    "rules": "No curfew",
    "cats": "tested private kitchen",
    "specs": ["Homely Loft", "Local Tips", "Guest Kitchen", "Jewish Quarter"],
    "best_for": "Solo backpackers and small groups who want a cozy, apartment-style hostel with friendly hosts in the nightlife district.",
    "skip_if": "you need card payments, step-free access or silence on weekend nights.",
    "trust": "Privates from €17",
    "transit": "Wesselényi utca (trams 4 and 6) and Blaha Lujza tér (M2), a few minutes' walk",
    "watch": "Cash only when I stayed; weekend street noise",
    "noise": "Weekend street noise",
    "pros": [
      ("Central Location", "In the heart of Budapest, near the top attractions and nightlife."),
      ("Friendly Staff", "Welcoming and helpful, with great local recommendations."),
      ("Homely Atmosphere", "A cozy, intimate setup, great for socializing."),
      ("Well-Equipped Kitchen", "A fully stocked kitchen for guests."),
      ("Local Connections", "Tips for bars, restaurants and festivals you won't find on your own."),
    ],
    "cons": [
      ("Cash-Only Payments", "No credit cards when I stayed; cash only."),
      ("Potential Noise", "The busy nightlife can mean noise at night."),
      ("Limited Accessibility", "Not fully accessible for all disabilities."),
    ],
    "summary": [
      "<strong>Das Nest is ideal if you want a central Budapest stay with a cozy, social atmosphere.</strong> It's all about friendly service, a relaxed vibe and great local tips.",
      "It lacked conveniences like card payments when I stayed, but makes up for it with personal touches and a great location. It suits travelers who value budget-friendly comfort and socializing over luxury.",
      "Rooms: 4 or 6-bed mixed or female-only dorms and a private double. Dorm beds <strong>from about €15</strong>.",
    ],
    "groups": [
      ("Rooms &amp; Sleep Quality", "rooms and beds", [
        ("Small Dorms", "<p><strong>4 and 6-bed mixed or female-only dorms</strong> plus a private double. Small enough to feel personal.</p>"),
        ("Weekend Noise", "<p>It's in the nightlife district, so <strong>light sleepers should pack earplugs</strong> for Friday and Saturday.</p>"),
      ]),
      ("Atmosphere &amp; Social Life", "common areas", [
        ("Like a Friend's Apartment", "<p>The hostel describes itself as a <strong>renovated rooftop loft apartment</strong>, and that's how it feels: intimate and social.</p>"),
        ("Hosts With Local Tips", "<p>The staff gave me <strong>bar, restaurant and festival tips</strong> that weren't in any guidebook.</p>"),
      ]),
      ("Facilities &amp; Payment", "facilities", [
        ("Kitchen", "<p>A <strong>fully equipped guest kitchen</strong>, good for saving money on meals.</p>"),
        ("Bring Cash", "<p>It was <strong>cash only</strong> when I stayed. Check your booking terms and bring forints just in case.</p>"),
      ]),
    ],
    "chips": [("yes", "Homely Atmosphere"), ("yes", "Guest Kitchen"), ("yes", "Free Security Lockers"), ("yes", "Female-Only Dorms"), ("no", "Cash Only (at my stay)")],
    "tested": True,
  },
  {
    "n": 10, "id": "section-10-the-hive-party-hostel", "old": "Carpe Noctem Hostel",
    "name": "The Hive Party Hostel", "brand": "The Hive",
    "tag": "#10 Best Big Party Hostel", "short": "Biggest party hostel",
    "area": "District VII, Jewish Quarter", "area_q": "Dob+utca+19+Budapest",
    "address": "Dob utca 19, 1074 Budapest", "district": "VII",
    "hw": (9.0, 7023), "bk": None,
    "dorm": 13, "private": 20, "checkin": "Check-in 15:00 to midnight, check-out by 11:00",
    "rules": "Strictly 18+, no curfew",
    "cats": "party private",
    "specs": ["Rooftop Bar", "Daily Pub Crawls", "18+ Only", "Jewish Quarter"],
    "best_for": "18+ groups and solo partygoers who want a big, loud party hostel with a rooftop bar in the ruin bar district.",
    "skip_if": "you are a light sleeper, an early riser or want bed curtains.",
    "trust": "Strictly 18+",
    "transit": "Astoria (M2) and Deák Ferenc tér (M1, M2, M3), a few minutes' walk",
    "watch": "Noise from the club downstairs; no bed curtains",
    "noise": "Loud (party hostel)",
    "why": [
      ("Big Party Hostel", "300+ beds since 2015, with daily pub crawls, bingo crawls, SPArties and party boats, per the hostel."),
      ("Rooftop Bar", "A private rooftop bar for guests, with a daily happy hour from 4 to 7 PM."),
      ("Location", "In the ruin bar district, a short walk from Gozsdu Udvar and Szimpla Kert."),
      ("Practical", "24 hour reception, security lockers, and payment by cash or card."),
    ],
    "skip": [
      ("Noise", "The hostel itself warns light sleepers and early risers; guests mention noise from the club downstairs."),
      ("No Bed Curtains", "Adding privacy curtains is a common guest request."),
      ("Wi-Fi", "Weak Wi-Fi is a recurring guest complaint."),
      ("Age Limit", "Strictly 18 and over."),
    ],
    "summary": [
      "<strong>The Hive is Budapest's big, loud party hostel.</strong> With 300+ beds, a rooftop bar and a daily program of pub crawls, it's built for nights out, not early mornings.",
      "I added it as the party alternative to Onefam: the facts here come from the hostel's own information and guest feedback, checked on " + CHECKED + ". Dorm beds start <strong>from about €13</strong>.",
    ],
    "groups": [],
    "chips": [("yes", "Rooftop Bar"), ("yes", "Daily Pub Crawls"), ("yes", "24 Hour Reception"), ("yes", "Free Security Lockers"), ("no", "Strictly 18+")],
    "tested": False,
  },
]

# ---------------------------------------------------------------- street / zip for JSON-LD
for _h in HOSTELS:
    _parts = _h['address'].split(', ')
    _h['street'] = _parts[0].replace(' (1st floor)', '')
    _h['zip'] = _parts[-1].split(' ')[0]


def _areas(H, a):
    return (
        '<h3>District VII (Jewish Quarter): for nightlife</h3>\n'
        '<p>The ruin bars, Gozsdu Udvar and Szimpla Kert are here, and so are %s, %s and %s. Great for going out, <strong>worst for light sleepers</strong> on weekends.</p>\n'
        '<h3>District VI (Király utca, Andrássy út, Oktogon): central and connected</h3>\n'
        '<p>%s, %s and %s sit on the main boulevards with M1 and the 24 hour trams 4 and 6. Walkable to everything, but <strong>main-road traffic</strong> can be loud.</p>\n'
        '<h3>District IX (Central Market Hall): calmer, by the river</h3>\n'
        '<p>%s, %s and %s are next to the Central Market Hall, a few minutes from the Danube. My pick if you want <strong>quieter nights</strong> and still walk to the center.</p>\n'
        '<p>Flying in? Here is <a href="/budapest-airport-to-city-center">how to get from the airport to the city center</a>: the 100E bus stops at Deák Ferenc tér, a short walk from the District VI and VII hostels.</p>'
    ) % (a(H[2]), a(H[9]), a(H[10]), a(H[6]), a(H[8]), a(H[3]), a(H[1]), a(H[4]), a(H[7]))


UI = {
    "url": "https://www.budapestadventures.com/best-hostels-budapest", "home": "Home", "home_url": "https://www.budapestadventures.com/",
    "about_url": "https://www.budapestadventures.com/about",
    "title": "10 Best Hostels in Budapest in 2026 (I Stayed in 9)",
    "h1_main": "10 Best Hostels in Budapest in 2026", "h1_muted": "(I Stayed in 9)",
    "meta": ("I stayed in 9 of Budapest's top hostels, including 30 nights at Maverick. "
             "Dorms from €8: the best party, quiet, budget and nomad picks, by area."),
    "breadcrumb": "Best Hostels in Budapest", "kicker_badge": "2026 Hostel Comparison",
    "author_line": 'By <a href="/about" target="_blank">Adam Dimitrov</a>, Founder &amp; Local Budapest Tester',
    "author_role": "Stayed in 9 of these 10 • Own photos &amp; video reviews",
    "last_updated": "<strong>Last updated</strong>: Nov 14, 2026",
    "job_title": "Founder & Local Budapest Tester",
    "intro": (
        '<p>Picking the wrong Budapest hostel costs you sleep, not money. Dorm beds in the center run <strong>€8 to €15 a night</strong>, '
        'but a party hostel in the Jewish Quarter and a quiet pod hostel by the Central Market Hall are two completely different trips.</p>\n'
        '<p>I <strong>stayed in 9 of the 10 hostels below</strong>, including <strong>30 nights at Maverick for €280</strong>, and compared them side by side '
        'on what decides the booking: noise at night, bed privacy, bathrooms, kitchen, age rules, the crowd and the real price per night.</p>\n'
        '<p>Use the filters to jump straight to party, quiet, budget, private-room or digital-nomad picks.</p>\n'),
    "filters": [("party", "🎉 Social &amp; Party"), ("quiet", "😴 Quiet Sleep"), ("budget", "💶 Under €11"),
                ("private", "🛏️ Private Rooms"), ("nomad", "💻 Digital Nomads"), ("kitchen", "🍳 Guest Kitchen")],
    "district_fmt": "%s District", "decimal": ".", "thousands": ",", "k": "k",
    "tested_chip": "✓ Personally Tested",
    "best_for_card": "Best For:", "best_for_summary": "Best for:", "skip_if": "Skip if",
    "from_eur": "From €%d", "eur": "€%d", "card_psub": "Dorm bed/night",
    "card_btn": "Check Prices &amp; Dates →", "read_review": "Read Review ↓",
    "pros": "Pros:", "cons": "Cons:", "why": "Why pick it:", "why_skip": "Why skip it:",
    "video": "Video:", "watch_my": "Watch my",
    "summary_title": "Summary &amp; Review", "summary_pill": "Overview",
    "swipe_photos": "Swipe %d Photos →", "one_photo": "1 Photo", "no_photo": "From my stay",
    "photo_alt": "%s: %s, photo from my stay", "prev_photo": "Previous photo", "next_photo": "Next photo",
    "buy_badge": "Live Prices &amp; Availability", "buy_sub": "Dorm bed per night • Checked " + CHECKED,
    "address_perk": "Address: <strong>%s</strong>", "privates_perk": "Private rooms from <strong>€%d</strong>",
    "buy_cta": "Check Dates &amp; Prices", "buy_trust": "Prices change by date; the final price shows before you pay",
    "qf": {"title": "Quick Facts: %s", "address": "Address", "dorm": "Dorm Beds", "transit": "Getting There", "checkin": "Check-In",
           "rules": "House Rules", "ratings": "Ratings", "watch": "Watch Out For",
           "dorm_fmt": "From €%d a night (checked " + CHECKED + ")", "priv_fmt": ", privates from €%d",
           "hw_fmt": "Hostelworld %s/10 (%s reviews)", "bk_fmt": ", Booking.com %s/10 (%s reviews)"},
    "breakdown_h2": "Detailed Reviews: 10 Best Hostels in Budapest",
    "breakdown_sub": "9 stayed in, 1 party pick on checked facts • Click to collapse or expand",
    "picks": [
        ("Best overall", 1, "Social without party noise, curtained beds, great bathrooms, and €280 for my 30-night stay."),
        ("Solo travelers (18 to 39)", 2, "Free daily activities and pub crawls make friends on easy mode. Over 39? Pick Maverick or Wombat's."),
        ("Party", 10, lambda H: 'The big, loud option with a rooftop bar in the ruin bar district. Want it more low-key? <a href="#%s">%s</a>.' % (H[6]['id'], H[6]['name'])),
        ("Cheapest bed", 3, "Beds from about €8 plus a free breakfast. Bring earplugs: it's on a tram junction."),
        ("Quiet sleep", 1, lambda H: 'A quiet side street in District IX. Also calm: <a href="#%s">%s</a> and <a href="#%s">%s</a>.' % (H[7]['id'], H[7]['name'], H[5]['id'], H[5]['name'])),
        ("Digital nomads", 4, "Laptop-friendly lounge and coworking space. Maverick is the long-stay alternative."),
        ("Couples &amp; families", 5, "Simple, quiet, clean rooms with private options. Budget about €3 for linens."),
        ("Sightseeing", 8, "At the start of Andrássy út, minutes from St. Stephen's Basilica and Deák tér."),
        ("Small &amp; homely", 9, "Feels like a friend's loft in the Jewish Quarter, with hosts full of local tips."),
    ],
    "sections": {
        "picks_badge": "Quick Picks", "picks_h2": "Best Hostel in Budapest by Traveler Type",
        "picks_sub": "The short answer for each kind of trip, based on my stays",
        "table_badge": "Side by Side", "table_h2": "Budapest Hostels Compared: Price, Noise and Catches",
        "table_sub": "Dorm prices and Hostelworld scores checked " + CHECKED + ". Noise and catches from my own stays (The Hive: guest feedback).",
        "table_cols": ["Hostel", "Best for", "Area", "Dorms from", "Hostelworld", "Noise at night", "Watch out for"],
        "areas_badge": "Areas", "areas_h2": "Where to Stay in Budapest for Hostels",
        "areas_sub": "All 10 are in central Pest. The district decides how loud your nights are.",
        "areas_body": _areas,
        "map_h2": "Map: Best Hostels in Budapest",
        "map_sub": 'The hostels on this list across Budapest\'s downtown districts (<a href="/best-walking-tours-budapest">7th Jewish Quarter</a>, 5th City Center, 6th Terézváros, and 9th Ferencváros)',
        "types_h2": "Budapest Hostel Types Explained",
    },
    "faq": [
        ('What is the best hostel in Budapest?',
         '<p><strong>Maverick Central Market</strong> is my best overall pick: social without party noise, curtained beds, great bathrooms and real long-stay value (I paid €280 for 30 nights in March). '
         'For a social trip pick <strong>Onefam Budapest</strong>; for the cheapest bed, <strong>Avenue Hostel</strong>.</p>'),
        ('What are the best hostels in Budapest for solo travelers?',
         '<p><strong>Onefam Budapest</strong> is the easiest place to make friends, with free daily activities and pub crawls, but it only takes guests aged <strong>18 to 39</strong>. '
         'Over 39, or want more sleep? <strong>Maverick Central Market</strong> and <strong>Wombat\'s City Hostel</strong> are social without the party pressure.</p>'),
        ('What are the best party hostels in Budapest?',
         '<p><strong>Onefam Budapest</strong> (social, daily bar crawls), <strong>The Hive Party Hostel</strong> (the big, loud one with a rooftop bar, strictly 18+) and '
         '<strong>Wombat\'s City Hostel</strong> (low-key party, quiet enough to sleep). All three are a short walk from the Jewish Quarter ruin bars.</p>'),
        ('Which Budapest hostels are best for a quiet night?',
         '<p><strong>Maverick Central Market</strong> (quiet side street), <strong>Central Market Hall Zen Hostel</strong> (small and homely) and <strong>a&amp;o Budapest City</strong> (hotel-style rooms). '
         'Avoid Avenue Hostel if you are a light sleeper: it\'s on the Oktogon tram junction.</p>'),
        ('How much does a hostel cost in Budapest?',
         '<p>On %s, dorm beds at these 10 hostels started at <strong>about €8 to €15 a night</strong> (Avenue from €8, Das Nest from €15), and private rooms from about €17 to €28. '
         'Prices rise on <strong>weekends, in summer (May to September), during Sziget Festival in August, the Christmas markets and New Year\'s Eve</strong>.</p>' % CHECKED),
        ('What is the best area to stay in Budapest for hostels?',
         '<p><strong>District VII (Jewish Quarter)</strong> for nightlife, <strong>District VI</strong> (Király utca, Andrássy út) for a central, well-connected base, and '
         '<strong>District IX</strong> by the Central Market Hall for quieter nights near the Danube.</p>'),
        ('Do Budapest hostels have age limits?',
         '<p>Some do. Per their house rules, <strong>Onefam Budapest takes guests aged 18 to 39</strong>, <strong>The Hive is strictly 18+</strong>, and <strong>Avenue Hostel accepts ages 6 to 49</strong>. Check the rules before you book.</p>'),
        ('Are hostels in Budapest safe?',
         '<p>Generally yes, but petty theft happens: I had a pullover and a box of nasal strips stolen at a hostel. <strong>Lock valuables in your locker</strong> and bring a padlock, since some hostels '
         '(Avenue, a&amp;o) don\'t include one. Flow Spaces gives you one for free.</p>'),
        ('What criteria did you use to choose the best hostels in Budapest?',
         '<p>I stayed in 9 of the 10 hostels and judged them on <strong>location, noise at night, cleanliness, bed comfort and privacy, facilities, the crowd and price</strong>. '
         'The Hive is included as a party pick based on checked facts and guest feedback, without a tested badge.</p>'),
        ('What should I bring with me to a hostel?',
         '<p><strong>Mandatory:</strong> earplugs and an eye mask. <strong>Basics:</strong> slippers, pajamas, phone charger, wet wipes, deodorant, toothbrush and toothpaste. '
         '<strong>Optional</strong> (check if your hostel includes them): towel, padlock, shampoo and shower gel.</p>'),
    ],
    "sticky_trust": "Dorm bed per night", "sticky_cta": "Check Prices →", "sheet_label": "Jump to a Budapest Hostel",
    "toc_breakdown": "Detailed Reviews (10 Hostels)",
    "szimpla_alt": "Szimpla Kert ruin bar, a short walk from The Hive on Dob utca",
    "szimpla_pill": "Szimpla Kert, 3 min walk",
    "collapse_label": "Collapse Review", "expand_label": "Read Review",
    "price_range": "From €%d per dorm bed",
}
