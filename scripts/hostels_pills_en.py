# -*- coding: utf-8 -*-
"""Dropdown content for the 4 spec pills on each /best-hostels-budapest card (EN).

PILLS[n] = 4 tuples (emoji, lead, text, note), in the same order as HOSTELS[n-1]['specs'].
Facts come only from hostels_data_en.py (Adam's stays for #1-9, checked facts for #10).
The Hive (#10) is never written in the first person. No em dashes.
"""

PILLS = {
  1: [  # Maverick Central Market
    ("🛏️", "Curtain on every bed.", "Modern dorms with privacy curtains and large lockers, so even a full room feels calm.", "Lock your valuables: I had a pullover stolen during my stay."),
    ("🌇", "A guest terrace up top.", "Social without being a party hostel: easy to meet people in the evening, then sleep.", "Crowd: solo travelers, long-stayers and remote workers."),
    ("🤫", "Lónyay utca, District IX.", "A smaller side street away from the District VII party streets. Street noise was minimal across my 30 nights.", "Kálvin tér (M3, M4) and Fővám tér (M4, trams 2, 47, 49) are a short walk."),
    ("💶", "30 nights for €280.", "That's about €9.33 a night in March, the best long-stay value I've found in central Budapest.", "Dorms from about €10 on near dates, privates from €28."),
  ],
  2: [  # Onefam Budapest
    ("🎯", "Something every day.", "Free daytime activities, then drinking games at the bar in the evening. The staff pull everyone in.", "Easiest place on this list to arrive solo and leave with a crew."),
    ("🍻", "Pub crawls into the ruin bars.", "The hostel party winds down around 11 PM to midnight, then the group heads out to the Jewish Quarter.", "No curfew; check-in 15:00 to 23:00."),
    ("🪪", "Strictly 18 to 39.", "Only guests aged 18 to 39 can stay, which keeps the crowd young and social.", "Over 39? Maverick has the social side without the age limit."),
    ("🚇", "4 minutes to Deák Ferenc tér.", "M1, M2, M3 and the 100E airport bus, from Rumbach Sebestyén utca 6.", "Walking distance home from the bars."),
  ],
  3: [  # Avenue Hostel
    ("🥐", "Breakfast included.", "Plus discounted dinners. With Hungary's food prices, the meals save you more per day than the bed costs.", "When I stayed, the dinner discount came with a small minimum bar spend."),
    ("🛏️", "Curtained bunks.", "My 10-bed room had curtained beds but was the weak spot. The 4, 8 and 12-bed rooms are nicer for a few euros more.", "Padlocks aren't included: bring one or buy one for about €3."),
    ("🚋", "Night trams at the door.", "M1 and the 24 hour trams 4 and 6 stop right outside, so getting home at 3 AM is easy.", "The flip side: trams pass all night. Bring earplugs."),
    ("📍", "Oktogon tér 4, District VI.", "On the Andrássy út and Grand Boulevard junction, walkable to the center.", "Reception open 24/7, check-in 14:00 to midnight."),
  ],
  4: [  # Flow Spaces
    ("💻", "A real work area.", "The lounge has a laptop-friendly work area, the best setup here for remote work.", "Social but calm: think college dorm, not bar crawl HQ."),
    ("🔒", "Padlock included.", "Your storage box comes with a free padlock, no €3 extra like elsewhere.", "Front desk staffed 24/7."),
    ("🛏️", "Pods with everything.", "Each bed has a privacy curtain, power socket, lamp, item tray and storage box.", "Rooms are tight: little space when everyone unpacks."),
    ("🏛️", "Gönczy Pál utca 2.", "One building from the Central Market Hall, a few minutes' walk to the Danube.", "3rd floor, no elevator. Fővám tér (M4, trams 2, 47, 49) is close."),
  ],
  5: [  # a&o Budapest City
    ("🤫", "Budget hotel calm.", "Simple, quiet, clean rooms with few hostel-style mixers, built for sleeping well.", "Suits couples, families and anyone who wants privacy."),
    ("🚿", "A mind-blowing shower.", "In a simple, quiet and clean room, the shower stood out.", "Linens and towels cost extra: 1,150 HUF (about €3)."),
    ("💻", "Laptop-friendly lounge.", "A superb work area in the lounge, and reception kept my laptop in secure storage while I was out.", "Optional hotel-style breakfast for about €8."),
    ("🚪", "Privates for 2 or more.", "Private rooms alongside the dorms, with a 24 hour reception for check-in at any time.", "Csengery utca 11, a few minutes from Oktogon (M1, trams 4 and 6)."),
  ],
  6: [  # Wombat's City Hostel
    ("🚿", "Bathroom in every room.", "Every room is en-suite with air conditioning, so no corridor queues for the shower.", "Clean but ordinary: don't book it for design."),
    ("🛏️", "Personal bed curtains.", "For a party hostel it's quiet at night. I slept well.", "Free security lockers."),
    ("🍸", "A social hostel bar.", "Easy to meet people at the hostel bar, then the Gozsdu Udvar bars are steps away.", "The international crowd was the best part of my stay."),
    ("📍", "Király utca 20.", "A 3 minute walk to Deák Ferenc tér (M1, M2, M3 and the 100E airport bus).", "Check-in 14:00 to 23:00, check-out by 10:00."),
  ],
  7: [  # Central Market Hall Zen Hostel
    ("🛋️", "A real living room.", "The sofa is where everyone ends up chatting, with board games during the day.", "If you like a cozy, homely feel, this is heaven."),
    ("🏠", "Small and personal.", "One friendly host ran the whole hostel when I stayed. She's the reason for the 9/10 ratings.", "No lockable stash and no desk with sockets."),
    ("☕", "Free all day.", "Self-service tea and coffee through the day, served in the living room.", "Check-in 14:00 to 21:00 only: late arrivals should book elsewhere."),
    ("🏛️", "Vámház körút 5.", "Next to the Central Market Hall and Liberty Bridge, a few minutes from the Danube.", "Fővám tér (M4, trams 2, 47, 49) is at the door."),
  ],
  8: [  # Adagio Hostel 2.0 Basilica
    ("⛪", "Views of St. Stephen's Basilica.", "At the start of Andrássy út, a few minutes' walk from the Basilica, the Opera and Deák Ferenc tér.", "Best base on this list for sightseeing on foot."),
    ("🚿", "Your own bathroom.", "Dorms and doubles with private bathrooms; mine was excellent and clean.", "Privates from about €22."),
    ("☕", "Free tea, coffee and linen.", "Self-service tea and coffee and fully equipped guest kitchens, per the hostel.", "Calm, not social: no events or personal touch."),
    ("📍", "Andrássy út 2, 1st floor.", "Bajcsy-Zsilinszky út (M1) at the door, Deák Ferenc tér (M1, M2, M3) a short walk.", "Main road: ask for a courtyard-side room. One flight of stairs, no elevator."),
  ],
  9: [  # Das Nest Budapest
    ("🏠", "A rooftop loft apartment.", "Renovated and intimate, it feels like staying at a friend's place.", "4 and 6-bed mixed or female-only dorms, plus a private double."),
    ("🗺️", "Tips you won't find online.", "The hosts gave me bar, restaurant and festival tips that weren't in any guidebook.", "Friendly, welcoming staff."),
    ("🍳", "Fully equipped kitchen.", "Cook your own meals and save on Budapest's restaurant prices.", "It was cash only when I stayed: bring forints just in case."),
    ("📍", "Akácfa utca 10, District VII.", "In the nightlife district, near the top sights and the ruin bars.", "Trams 4 and 6 at Wesselényi utca. Pack earplugs for weekend nights."),
  ],
  10: [  # The Hive Party Hostel (not stayed in: no first person)
    ("🌇", "Guests-only rooftop bar.", "Happy hour every day from 4 to 7 PM.", "300+ beds, open since 2015, per the hostel."),
    ("🍻", "A party every night.", "Daily pub crawls, plus bingo crawls, SPArties and party boats run by the hostel.", "Guests mention noise from the club downstairs."),
    ("🔞", "Strictly 18 and over.", "Built for nights out, not early mornings.", "Check-in 15:00 to midnight; pay by cash or card."),
    ("📍", "Dob utca 19, District VII.", "A short walk to Gozsdu Udvar and Szimpla Kert.", "Astoria (M2) and Deák Ferenc tér (M1, M2, M3) a few minutes away."),
  ],
}
