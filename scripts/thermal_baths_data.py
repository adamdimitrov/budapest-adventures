"""Card data for /thermal-baths-budapest (EN), rebuilt 14 November 2026.

Every hour, price, temperature and rule below was checked in Chrome on 14 November 2026:
official bath sites for hours, desk prices, pools and rules; the GetYourGuide, Tiqets and
Viator listings for ticket prices (booking calendar for Thursday 19 November 2026), what
the ticket includes and ratings; Google Maps for the Veli Bej rating. Gellért (closed
since 1 October 2025, reopening expected in 2028) and Király (closed indefinitely) were
dropped. Personally tested (user, 14 Nov 2026): Széchenyi, Rudas, Palatinus, Dandár.
"""

GYG = ("https://www.getyourguide.com/budapest-l29/{slug}/?partner_id=YS414AJ"
       "&utm_medium=online_publisher&cmp=en-thermal-baths-{placement}-{key}&mkt_cmp=true")
TIQETS = "https://www.tiqets.com/en/things-to-do-in-budapest-c68199/{slug}/?partner=thecruisedetective.com-176436"
VIATOR = ("https://www.viator.com/tours/Budapest/{slug}?pid=P00072830&mcid=42383&medium=link"
          "&campaign=en-thermal-baths-rating-{key}")
MAPS = "https://www.google.com/maps/search/?api=1&query={q}"
CDN = "/assets/cdn/60e43c7d6d05b671dff0dc1a/"
NEW = "/assets/thermal-baths-2026/"

OFFICIAL_NOTE = "Checked on the official site on 14 November 2026; hours change by season and holidays."
GYG_NOTE = "Checked on the booking calendar for Thursday 19 November 2026."


def pill(icon, label, pop, note=None, cls=""):
    extra = (' ' + cls) if cls else ''
    n = '<span class="bpa-lang-note">%s</span>' % note if note else ''
    return ('<details class="bpa-lang%s"><summary class="bpa-sp">%s <span class="bpa-lang-label">%s</span>'
            '<span class="bpa-lang-chev" aria-hidden="true">▾</span></summary><div class="bpa-lang-pop">%s%s</div></details>'
            % (extra, icon, label, pop, n))


def chip(text):
    return '<span class="bpa-sp">%s</span>' % text


def maps_link(q, text):
    import urllib.parse
    return ('<a href="%s" rel="nofollow noopener" target="_blank">%s</a>'
            % (MAPS.format(q=urllib.parse.quote_plus(q)).replace("&", "&amp;"), text))


CARDS = []

# ── 1 ─ Széchenyi (tested) ────────────────────────────────────────────────────────────
CARDS.append(dict(
    key="szechenyi", anchor="item-1-szechenyi", cat="tested", tested=True,
    rank="🏆 #1 Best Overall", color="bpa-gold",
    area="City Park, District XIV", time="Half Day", transport="M1 Széchenyi fürdő",
    maps_q="Széchenyi Gyógyfürdő Állatkerti körút 9-11 Budapest",
    title="Széchenyi Thermal Bath", short="Széchenyi Thermal Bath",
    book="gyg", gyg_slug="szechenyi-spa-full-day-entrance-pass-t4139",
    ratings=[("GetYourGuide", 4.2808, 29207, "gyg", None),
             ("Tiqets", 4.4, 1252, "tiqets", "tickets-for-szechenyi-spa-full-day-entry-p974376"),
             ("Viator", 3.8, 2393, "viator", "Private-Entrance-to-Szechenyi-Spa-in-Budapest-with-Optional-Massage/d499-5808SZECHENYI")],
    price="39", psub="per adult · Mon–Thu, entry by 9:00", via="GetYourGuide",
    trust=["✓ Free cancellation up to 24 hours before", "✓ Reserve now, pay later"],
    tested_pop="<strong>I visited Széchenyi myself.</strong> Most of the photos on this card are my own. Every price, hour and temperature was rechecked on the official site on 14 November 2026.",
    photos=[CDN + p for p in [
        "63c12f890d9668187cda50a6_1_Sz%C3%A9chenyi%20Thermal%20Bath.webp",
        "64b7a8d6a973a0c983a7095a_11Szechenyi-bath-ourdoor-pool.avif",
        "64b7a8c8c9fdf77e1c5197bf_10-Szechenyi-bath-outdoor-lap-pool.avif",
        "64b7b108d4bc082efa13bf83_12-Szechenyi-bath-indoor-pool-1.avif",
        "64b7b1876a1ea8dedc6fb379_14-Szechenyi-bath-indoor-pool-3.avif",
        "64b7b4187c0010e65f20f953_15-Szechenyi-bath-aroma-sauna.avif",
        "64b6a6449efb8b06f9af724c_01-Szechenyi-bath-entrance.webp",
        "64b6a69a5ab0f3b16f839aa2_02-Szechenyi-bath-ticket-office.webp",
        "64b6a6b19f9458bcf5a7b66c_03-Szechenyi-bath-online-ticket-validation.webp",
        "64b7a540343999e752fcbdd0_05-Szechenyi-bath-locker-room.webp",
        "64b6b7ed2c5ca7263d3ae36e_08-Szechenyi-bath-cabins.avif",
        "64b6bcf22c5ca7263d424207_09-Szechenyi-bath-what-to-bring.avif"]],
    alt="Széchenyi Thermal Bath",
    pills=[
        pill("🕒", "Daily · 7:00–20:00",
             "<strong>Mon–Thu</strong> 7:00–20:00 · <strong>Fri</strong> 7:00–22:00 · <strong>Sat–Sun</strong> 8:00–20:00. "
             "8 December 2026: closes at 16:00. 18 December 2026 to 6 January 2027: opens at 8:00. "
             "25 and 26 December and 1 January: opens at 10:00.",
             OFFICIAL_NOTE, "bpa-time"),
        pill("🏊", "3 outdoor + 15 indoor pools",
             "<strong>Outdoor:</strong> swimming pool 26–28 °C, thermal pool 36–38 °C, adventure pool 32–34 °C. "
             "<strong>Indoor:</strong> medicinal pools 28–40 °C and plunge pools at 18 °C and 40 °C.",
             "Temperatures from szechenyifurdo.hu; the pool count is from the ticket listings."),
        pill("🎟️", "Locker or cabin",
             "<strong>GetYourGuide (Thu 19 Nov 2026):</strong> Morning Pass with locker, entry 7:00–9:00, €39 · "
             "Weekday Pass with locker €46 · Weekday Pass with private cabin €50. "
             "<strong>At the desk (2026):</strong> locker ticket 13,200 HUF Mon–Thu, 14,800 HUF Fri–Sun, 15,800 HUF in peak periods; cabin +1,000 HUF.",
             "Desk prices from szechenyifurdo.hu/arak-2026."),
        pill("🎉", "Sparty on Saturdays",
             "<strong>Sparty</strong> is the Saturday night pool party at Széchenyi: from €73 on GetYourGuide (start 21:30), "
             "or €100 with two drink coupons. 18+ only and <strong>non-refundable</strong>. "
             "<a href=\"{sparty}\" rel=\"nofollow sponsored noopener\" target=\"_blank\">See Sparty tickets →</a>",
             "Checked on the booking calendar for Saturday 21 November 2026."),
    ],
    pick="for the classic Budapest bath: big outdoor pools in a yellow neo-baroque palace, open until 22:00 on Fridays.",
    skip="if you want quiet: it gets busy from late morning, so come at 7:00 on a weekday or pick Lukács or Veli Bej.",
    pros=[("Outdoor pools all year", "An outdoor thermal pool at 36–38 °C, an adventure pool at 32–34 °C and a 26–28 °C swimming pool, open in winter too."),
          ("Huge choice inside", "The listings count 15 indoor pools, plus five saunas from 50 to 90 °C and three steam cabins."),
          ("Cheap early start", "Mon–Thu entry before 9:00 is €39 on GetYourGuide, or 10,500 HUF at the desk."),
          ("Late Fridays", "Open until 22:00 on Fridays, and the Sparty pool party runs on Saturday nights.")],
    cons=[("Crowds", "It is the most-reviewed bath on GetYourGuide; by late morning the outdoor pools are packed."),
          ("Online tickets cost more", "The weekday locker ticket is €46 on GetYourGuide against 13,200 HUF at the desk, though GetYourGuide lets you cancel for free."),
          ("Bring your own kit", "Towels and flip-flops are not included; the desk sells a towel for 6,900 HUF and slippers for 4,200 HUF.")],
    summary_q=("Is Széchenyi worth it?",
               "Yes, for a first visit. It is the biggest and most photogenic bath in Budapest. Go early on a weekday to avoid the crowds."),
    summary=["Széchenyi is the bath most visitors picture: three outdoor pools steaming in front of a yellow neo-baroque palace in City Park. "
             "It is also the busiest. My best advice from my own visit: arrive between 7:00 and 10:00 on a weekday.",
             "Based on <strong>29,000+ GetYourGuide reviews</strong> (4.3 out of 5), visitors love the outdoor pools in winter and the architecture. "
             "The most common complaints are crowds later in the day and the price of booking-site tickets."],
    quotes=[("A great way to spend a day in Budapest.", "GetYourGuide", "November 2026"),
            ("Go in the morning when there are still few people and the baths are clean.", "GetYourGuide", "November 2026"),
            ("Outside pools were especially atmospheric in the rain", "GetYourGuide", "November 2026")],
    getthere=[
        "📍 " + maps_link("Széchenyi Gyógyfürdő Állatkerti körút 9-11 Budapest", "Állatkerti körút 9-11, 1146 Budapest (City Park)"),
        "🚇 Take <strong>metro M1</strong> to <strong>Széchenyi fürdő</strong>; the entrance is about a 2-minute walk.",
        "🎟️ Day tickets are sold and checked on the <strong>swimming-pool side</strong> (Állatkerti körút).",
    ],
    spcards=[
        ("Entrance &amp; Tickets", CDN + "64b6a69a5ab0f3b16f839aa2_02-Szechenyi-bath-ticket-office.webp",
         "Day tickets enter on the swimming-pool side. Booking-site tickets are validated at self-service machines at the entrance, so you skip the cashier queue."),
        ("Lockers &amp; Cabins", CDN + "64b7a540343999e752fcbdd0_05-Szechenyi-bath-locker-room.webp",
         "A standard ticket includes a locker in the gender-separated changing area. You get a plastic wristwatch that opens it (3,000 HUF if lost). A private cabin costs 1,000 HUF extra."),
        ("Outdoor Pools", CDN + "64b7a8d6a973a0c983a7095a_11Szechenyi-bath-ourdoor-pool.avif",
         "Three outdoor pools: the thermal pool (36–38 °C), the adventure pool with its whirlpool (32–34 °C) and the swimming pool (26–28 °C, 910 m²)."),
        ("Indoor Pools", CDN + "64b7b108d4bc082efa13bf83_12-Szechenyi-bath-indoor-pool-1.avif",
         "The indoor wings hold medicinal pools from 28 to 40 °C and plunge pools at 18 °C and 40 °C."),
        ("Saunas &amp; Steam", CDN + "64b7b4187c0010e65f20f953_15-Szechenyi-bath-aroma-sauna.avif",
         "Volcano sauna 70–80 °C, Dante and Phoenix saunas 80–90 °C, two aroma saunas 50–55 °C, three steam cabins 50–60 °C and a salt room at 35–40 °C."),
        ("What to Bring", CDN + "64b6bcf22c5ca7263d424207_09-Szechenyi-bath-what-to-bring.avif",
         "Swimsuit, towel and flip-flops. If you forget them, the desk sells a towel (6,900 HUF), slippers (4,200 HUF) and a swim cap (2,100 HUF)."),
        ("Night Bathing &amp; Sparty", None,
         "Open until 22:00 on Fridays. Sparty, the Saturday night pool party, is sold separately (18+, from €73, non-refundable)."),
    ],
    qf=[("Opening Hours", "Mon–Thu 7:00–20:00 · Fri 7:00–22:00 · Sat–Sun 8:00–20:00 (checked 14 Nov 2026)"),
        ("Desk Prices 2026", "Locker ticket 13,200 HUF Mon–Thu / 14,800 HUF Fri–Sun / 15,800 HUF peak · before 9:00: 10,500 / 11,800 HUF · cabin +1,000 HUF"),
        ("GetYourGuide Ticket", "Morning Pass with locker €39 · Weekday Pass with locker €46 · with private cabin €50 (Thu 19 Nov 2026); free cancellation up to 24 hours before"),
        ("Pools &amp; Temperatures", "3 outdoor (26–28, 32–34, 36–38 °C) + 15 indoor (28–40 °C, plunge pools 18 and 40 °C)"),
        ("Saunas &amp; Steam", "5 saunas (50–90 °C), 3 steam cabins (50–60 °C), salt room (35–40 °C)"),
        ("Towels &amp; Robes", "Not included; towel 6,900 HUF and robe 12,600 HUF sold at the desk"),
        ("Age Limit", "The GetYourGuide ticket is not suitable for children under 14"),
        ("Address", "Állatkerti körút 9-11, 1146 Budapest"),
        ("Nearest Transport", "Metro M1, Széchenyi fürdő")],
    amen=[("yes", "Outdoor Pools"), ("yes", "Indoor Pools"), ("yes", "Thermal Water"), ("yes", "Sauna"),
          ("yes", "Steam Room"), ("yes", "Massage"), ("yes", "Café &amp; Restaurant")],
))

# ── 2 ─ Rudas (tested) ────────────────────────────────────────────────────────────────
CARDS.append(dict(
    key="rudas", anchor="item-2-rudas", cat="tested", tested=True,
    rank="🕌 #2 Best Turkish Bath &amp; Rooftop", color="bpa-silver",
    area="Elizabeth Bridge, District I", time="3–4 Hours", transport="Tram 19, 41 · Bus 7",
    maps_q="Rudas Gyógyfürdő Döbrentei tér 9 Budapest",
    title="Rudas Thermal Bath", short="Rudas Thermal Bath",
    book="gyg", gyg_slug="budapest-rudas-turkish-bath-spa-day-pass-3-course-meal-t233617",
    ratings=[("GetYourGuide", 4.1941, 1422, "gyg", None)],
    price="74.99", psub="per adult · bath + 3-course meal", via="GetYourGuide",
    trust=["✓ Free cancellation up to 24 hours before", "✓ Includes a 3-course meal"],
    tested_pop="<strong>I visited Rudas myself.</strong> Every price, hour and pool temperature on this card was rechecked on rudasfurdo.hu on 14 November 2026.",
    photos=[CDN + p for p in [
        "63c12fda4ee7c50a6cee3178_3_1%20Rudas%20Thermal%20Bath.webp",
        "64d4e6d882d74213380c1f24_Rudas-thermal-bath%20(11).webp",
        "64d4e674b2871f3b832c1681_Rudas-thermal-bath%20(15).webp",
        "64d4e7021d502805c7a7c112_Rudas-thermal-bath%20(18).webp",
        "64d4e74e82fd0ed0adc4f09c_Rudas-thermal-bath%20(2).webp",
        "64d4e65e09406b071f265969_Rudas-thermal-bath%20(14).webp",
        "64d4e6a5a89136c45fd1d9fc_Rudas-thermal-bath%20(20).webp",
        "64d4e69c6efb73a26f9877f6_Rudas-thermal-bath%20(19).webp",
        "64d4e79648d7f0b7f7ac4062_Rudas-thermal-bath%20(8).webp"]],
    alt="Rudas Thermal Bath",
    pills=[
        pill("🕒", "Daily · 6:00–20:00",
             "<strong>Wellness:</strong> Mon 6:00–22:00, Tue–Sun 6:00–20:00. <strong>Night bathing:</strong> Fri and Sat 22:00–3:00 "
             "(15,000 HUF, online tickets only). 8 December 2026: closes at 16:00.",
             OFFICIAL_NOTE, "bpa-time"),
        pill("🚻", "Men / women days",
             "<strong>Turkish bath, men only:</strong> Mon, Thu and Fri 6:00–10:45, Wed 6:00–20:00. "
             "<strong>Women only:</strong> Tue 6:00–20:00. <strong>Mixed:</strong> Mon 11:00–22:00, Thu and Fri 11:00–20:00, Sat and Sun 6:00–20:00.",
             "From the official timetable on rudasfurdo.hu."),
        pill("🏊", "Rooftop pool 36 °C",
             "<strong>Panorama pool</strong> on the roof at 36 °C. <strong>Turkish bath:</strong> six pools at 16, 28, 30, 33, 36 and 42 °C. "
             "<strong>Wellness:</strong> pools at 11, 32, 36 and 42 °C. <strong>Swimming pool:</strong> 29 °C.",
             "From rudasfurdo.hu."),
        pill("🎟️", "What the ticket includes",
             "The GetYourGuide ticket is a <strong>day pass plus a 3-course meal</strong> at Rudas Bistro: wellness + coffee €74.99, "
             "wellness + wine €76.99, Turkish bath + wellness + coffee €84.99. "
             "<strong>At the desk:</strong> all zones 12,000 HUF Mon–Thu, 15,000 HUF Fri–Sun, without a meal.",
             GYG_NOTE),
        pill("🔞", "14+ · not step-free",
             "Children under 14 are not admitted. The bath currently cannot receive guests with reduced mobility for technical reasons.",
             "From rudasfurdo.hu, 14 November 2026."),
    ],
    pick="for an Ottoman-era Turkish bath under a stone dome plus a rooftop hot pool with a Danube view, and for night bathing on weekends.",
    skip="if you travel with kids under 14, need step-free access, or only want a bath ticket without the meal.",
    pros=[("Rooftop panorama pool", "A 36 °C pool on the roof with views over the Danube; my favourite in the cold months."),
          ("Real Turkish bath", "Six pools from 16 to 42 °C under the Ottoman dome, on separate men-only and women-only days."),
          ("Night bathing", "Friday and Saturday from 22:00 to 3:00 (15,000 HUF, online only)."),
          ("Meal included", "The GetYourGuide ticket adds a 3-course meal at Rudas Bistro, and reviewers rate the food highly.")],
    cons=[("Confusing layout", "Reviewers find it hard to move between the wellness area, the Turkish bath and the rooftop."),
          ("Crowded at peak times", "Some reviewers call the bath overcrowded, especially the rooftop pool."),
          ("Only a meal package online", "No booking site sells a plain entry ticket; the desk price is 12,000 HUF on weekdays."),
          ("Not for everyone", "No children under 14 and currently no access for guests with reduced mobility.")],
    summary_q=("Is Rudas better than Széchenyi?",
               "For atmosphere, often yes: the Ottoman Turkish bath and the rooftop pool are unique. For a family day out, no: Rudas admits no under-14s."),
    summary=["What makes Rudas unique is the rooftop panorama pool, which looks over the Danube towards Gellért Hill. It is lovely to soak in it in the grim winter months. "
             "The other highlight is the Ottoman Turkish bath with its octagonal pool under a stone dome, which has men-only and women-only days.",
             "Based on <strong>1,400+ GetYourGuide reviews</strong> (4.2 out of 5), visitors praise the Turkish bath, the views and the food at Rudas Bistro. "
             "The recurring complaints are crowds and a confusing layout."],
    quotes=[("Fun experience and beautiful views when you're in the upper pool.", "GetYourGuide", "November 2026"),
            ("Brilliant bathhouse, especially the Turkish one with the sandstone columns", "GetYourGuide", "October 2026"),
            ("The bath is overcrowded and tourist trap.", "GetYourGuide", "October 2026")],
    getthere=[
        "📍 " + maps_link("Rudas Gyógyfürdő Döbrentei tér 9 Budapest", "Döbrentei tér 9, 1013 Budapest (Buda end of Elizabeth Bridge)"),
        "🚋 <strong>Tram</strong> 19, 41, 56 or 56A, or <strong>bus</strong> 7, 8E, 108E, 110 or 112 to the Buda end of Elizabeth Bridge.",
        "🌙 After night bathing: night buses 907 and 973.",
    ],
    spcards=[
        ("Rooftop Panorama Pool", CDN + "64d4e6d882d74213380c1f24_Rudas-thermal-bath%20(11).webp",
         "The 36 °C rooftop pool looks over the Danube and Gellért Hill. Perfect when it is raining or snowing."),
        ("Turkish Bath", CDN + "64d4e7021d502805c7a7c112_Rudas-thermal-bath%20(18).webp",
         "Six pools at 16, 28, 30, 33, 36 and 42 °C, including the octagonal pool under the Ottoman dome. Check the men-only and women-only timetable before you go."),
        ("Wellness Pools", CDN + "64d4e674b2871f3b832c1681_Rudas-thermal-bath%20(15).webp",
         "The wellness section has pools at 11, 32, 36 and 42 °C, and the swimming pool is 29 °C."),
        ("Saunas &amp; Steam", None,
         "Wellness side: two Finnish saunas (90–100 °C and 60–70 °C), an aroma sauna, a steam cabin and a salt room. Turkish side: three Finnish saunas and a steam room."),
        ("Lockers &amp; Cabins", CDN + "64d4e69c6efb73a26f9877f6_Rudas-thermal-bath%20(19).webp",
         "A regular ticket includes a locker. A private cabin costs 1,000 HUF extra at the desk."),
        ("Drinking Hall", CDN + "64d4e79648d7f0b7f7ac4062_Rudas-thermal-bath%20(8).webp",
         "The drinking fountain is open Tue and Thu 10:00–14:00. Photo: rudasfurdo.hu."),
        ("Night Bathing", None,
         "Friday and Saturday 22:00–3:00. Tickets are sold online only: 15,000 HUF (18,000 HUF on 1 and 2 January 2027)."),
        ("Food &amp; Drink", None,
         "Rudas Bistro and Rudas Café are inside the bath. The GetYourGuide ticket includes a 3-course meal at the bistro."),
    ],
    qf=[("Opening Hours", "Wellness Mon 6:00–22:00, Tue–Sun 6:00–20:00 · night bathing Fri and Sat 22:00–3:00 (checked 14 Nov 2026)"),
        ("Men / Women Only", "Men: Mon, Thu, Fri 6:00–10:45 and Wed all day · Women: Tue all day · Mixed: weekends"),
        ("Desk Prices 2026", "All zones 12,000 HUF Mon–Thu / 15,000 HUF Fri–Sun / 16,000 HUF peak · Turkish bath only (Mon, Thu, Fri until 10:45) 8,000 HUF"),
        ("GetYourGuide Ticket", "Day pass + 3-course meal: from €74.99 (Thu 19 Nov 2026); free cancellation up to 24 hours before"),
        ("Pools &amp; Temperatures", "Turkish bath 6 pools (16–42 °C) · wellness 4 pools (11–42 °C) · rooftop 36 °C · swimming pool 29 °C"),
        ("Saunas &amp; Steam", "6 Finnish saunas, aroma sauna, steam cabin, steam room, salt room"),
        ("Towels &amp; Robes", "Not included; towel 6,900 HUF and robe 12,600 HUF sold at the desk"),
        ("Age Limit", "No children under 14"),
        ("Address", "Döbrentei tér 9, 1013 Budapest"),
        ("Nearest Transport", "Tram 19, 41, 56, 56A · Bus 7, 8E, 108E, 110, 112")],
    amen=[("yes", "Rooftop Panorama Pool"), ("yes", "Indoor Pools"), ("yes", "Thermal Water"), ("yes", "Sauna"),
          ("yes", "Steam Room"), ("yes", "Massage"), ("yes", "Café &amp; Restaurant"),
          ("no", "Not Wheelchair Accessible"), ("no", "No Children Under 14")],
))

# ── 3 ─ Lukács (not tested) ───────────────────────────────────────────────────────────
CARDS.append(dict(
    key="lukacs", anchor="item-3-lukacs", cat="", tested=False,
    rank="🌿 #3 Best Local Bath", color="bpa-bronze",
    area="Buda, District II", time="2–3 Hours", transport="Tram 4, 6, 17, 19",
    maps_q="Lukács Gyógyfürdő Frankel Leó út 25-29 Budapest",
    title="Lukács Thermal Bath", short="Lukács Thermal Bath",
    book="gyg", gyg_slug="budapest-lukacs-thermal-bath-full-day-spa-ticket-t439700",
    ratings=[("GetYourGuide", 3.9772, 365, "gyg", None),
             ("Tiqets", 4.1, 27, "tiqets", "tickets-for-budapest-lukacs-thermal-bath-p1053009"),
             ("Viator", 3.7, 41, "viator", "Budapest-Lukacs-Thermal-Bath-Full-Day-Admission/d499-5808P201")],
    price="33", psub="per adult · full day", via="GetYourGuide",
    trust=["✓ Free cancellation until the day before", "✓ Reserve now, pay later"],
    photos=[CDN + "63c12ff6ce1b4b5efd14b0fb_5_Luk%C3%A1cs%20Thermal%20Bath.webp",
            NEW + "lukacs-outdoor-pool-04.avif",
            CDN + "64d4e8f7b533d16e8b2d5fdc_Lukacs-thermal-bath%20(2).webp",
            CDN + "64d4e84b26762fdfb9cbb893_Lukacs-thermal-bath%20(5).webp",
            CDN + "64d4e92988143c95074f1bf5_Lukacs-thermal-bath%20(3).webp",
            CDN + "64d4e9500da218e95c8c6206_Lukacs-thermal-bath%20(7).webp",
            NEW + "lukacs-courtyard-01.avif",
            NEW + "lukacs-courtyard-plaques-02.avif",
            NEW + "lukacs-hall-03.avif",
            CDN + "64d4e96a1d502805c7aa86c8_Lukacs-thermal-bath%20(12).webp"],
    alt="Lukács Thermal Bath",
    pills=[
        pill("🕒", "Daily · 7:00–19:00",
             "<strong>Mon, Wed–Sun</strong> 7:00–19:00 · <strong>Tue</strong> 7:00–22:00. The online ticket has a 9:00–17:00 window for Thu 19 Nov.",
             OFFICIAL_NOTE, "bpa-time"),
        pill("🏊", "Medicinal pools 32–40 °C",
             "<strong>Indoor medicinal pools</strong> at 32, 36 and 40 °C, a 20 °C cold pool and a 20 °C Kneipp foot path. "
             "<strong>Outdoor:</strong> adventure pool 33–35 °C and swimming pools at 22 and 26 °C.",
             "From lukacsfurdo.hu."),
        pill("🎟️", "Cabin or locker",
             "The GetYourGuide ticket is a full-day entry with a cabin or locker, depending on availability: €33. "
             "<strong>At the desk (2026):</strong> 7,000 HUF Mon–Thu, 8,000 HUF Fri–Sun; sauna world +1,300 HUF.",
             GYG_NOTE),
        pill("🔞", "14+ · partial closures",
             "Children under 14 are not admitted. The wheelchair lifts are out of order for technical reasons, and the private tub service is closed for renovation.",
             "From lukacsfurdo.hu, 14 November 2026."),
    ],
    pick="for a smaller bath with strong medicinal pools, open until 22:00 on Tuesdays.",
    skip="if you want grand architecture or a party feel, or if you travel with kids under 14.",
    pros=[("Medicinal pools", "Indoor pools at 32, 36 and 40 °C, with a cold pool and a Kneipp path at 20 °C."),
          ("Cabin or locker included", "The GetYourGuide ticket includes a cabin or a locker for the full day."),
          ("Good value at the desk", "7,000 HUF on weekdays, about half the Széchenyi price."),
          ("Late Tuesday", "Open until 22:00 every Tuesday.")],
    cons=[("Confusing layout", "Reviewers say you need to walk around to find the thermal pools."),
          ("Mixed ratings", "3.7 to 4.1 out of 5 across the three booking sites, the lowest scores in this list."),
          ("Facilities under repair", "The wheelchair lifts are out of order and the private tubs are closed for renovation.")],
    summary_q=("Is Lukács a good alternative to Széchenyi?",
               "Yes, if you want thermal water without the crowds. It is smaller and plainer, and closer to a local bath than a tourist sight."),
    summary=["Lukács is a Buda bath with a long courtyard, a set of indoor medicinal pools and outdoor swimming pools. "
             "It is smaller and plainer than Széchenyi and Rudas.",
             "Based on <strong>430+ reviews</strong> across GetYourGuide, Tiqets and Viator (about 4 out of 5), reviewers praise the friendly staff. "
             "The most common complaint is a confusing layout."],
    quotes=[("I enjoyed my time at the spa! Everyone was friendly", "GetYourGuide", "October 2026"),
            ("the layout was slightly confusing, you have to have a good walk around to find the thermal baths", "GetYourGuide", "October 2026")],
    getthere=[
        "📍 " + maps_link("Lukács Gyógyfürdő Frankel Leó út 25-29 Budapest", "Frankel Leó út 25-29, 1023 Budapest"),
        "🚋 <strong>Tram</strong> 4, 6, 17 or 19, <strong>bus</strong> 9 or 109, or the <strong>HÉV</strong> suburban train to Margit híd, budai hídfő.",
        "⚠️ Veli Bej is on the same street; do not mix them up.",
    ],
    spcards=[
        ("Courtyard", NEW + "lukacs-courtyard-01.avif",
         "The entrance leads through a long, tree-lined courtyard. Photo: Christo, CC BY-SA 4.0, Wikimedia Commons."),
        ("Outdoor Pools", NEW + "lukacs-outdoor-pool-04.avif",
         "An adventure pool at 33–35 °C with jets and two swimming pools at 22 and 26 °C. Photo: ParisSharing, CC BY 2.0, Wikimedia Commons."),
        ("Indoor Medicinal Pools", CDN + "64d4e92988143c95074f1bf5_Lukacs-thermal-bath%20(3).webp",
         "Medicinal pools at 32, 36 and 40 °C, a 20 °C cold pool and a 20 °C Kneipp foot path."),
        ("Saunas &amp; Steam", None,
         "Finnish sauna 80–90 °C, herbal sauna 60–62 °C, dry steam room 60–90 °C and a steam cabin 40–50 °C. The sauna world costs 1,300 HUF extra at the desk."),
        ("Cabins", CDN + "64d4e96a1d502805c7aa86c8_Lukacs-thermal-bath%20(12).webp",
         "A private cabin costs 1,000 HUF extra at the desk; the GetYourGuide ticket gives a cabin or a locker depending on availability."),
        ("Historic Halls", NEW + "lukacs-hall-03.avif",
         "Columned halls connect the sections of the bath. Photo: Globetrotter19, CC BY-SA 4.0, Wikimedia Commons."),
    ],
    qf=[("Opening Hours", "Mon, Wed–Sun 7:00–19:00 · Tue 7:00–22:00 (checked 14 Nov 2026)"),
        ("Desk Prices 2026", "7,000 HUF Mon–Thu / 8,000 HUF Fri–Sun · sauna world +1,300 HUF · last 2 hours on weekdays 3,800 HUF"),
        ("GetYourGuide Ticket", "Full day with cabin or locker: €33 (Thu 19 Nov 2026); free cancellation until the day before"),
        ("Pools &amp; Temperatures", "Indoor 32, 36, 40 °C · cold pool 20 °C · outdoor adventure pool 33–35 °C · swimming pools 22 and 26 °C"),
        ("Saunas &amp; Steam", "Finnish sauna, herbal sauna, dry steam room, steam cabin"),
        ("Towels &amp; Robes", "Not included; towel 6,900 HUF and robe 12,600 HUF sold at the desk"),
        ("Age Limit", "No children under 14"),
        ("Address", "Frankel Leó út 25-29, 1023 Budapest"),
        ("Nearest Transport", "Tram 4, 6, 17, 19 · Bus 9, 109 · HÉV")],
    amen=[("yes", "Outdoor Pools"), ("yes", "Indoor Pools"), ("yes", "Thermal Water"), ("yes", "Sauna"),
          ("yes", "Steam Room"), ("no", "Wheelchair Lifts Out of Order"), ("no", "No Children Under 14")],
))

# ── 4 ─ Palatinus (tested) ────────────────────────────────────────────────────────────
CARDS.append(dict(
    key="palatinus", anchor="item-4-palatinus", cat="tested", tested=True,
    rank="👨‍👩‍👧 #4 Best for Families", color="bpa-slate",
    area="Margaret Island", time="Half Day", transport="Bus 26",
    maps_q="Palatinus Strandfürdő Soó Rezső sétány 1 Budapest",
    title="Palatinus Bath on Margaret Island", short="Palatinus Bath",
    book="gyg", gyg_slug="budapest-palatinus-spa-pools-full-day-admission-t439827",
    ratings=[("GetYourGuide", 4.3287, 470, "gyg", None),
             ("Viator", 3.5, 27, "viator", "Budapest-Palatinus-Bath-Full-Day-Admission/d499-5808P202")],
    price="27", psub="per adult · full day", via="GetYourGuide",
    trust=["✓ Free cancellation up to 24 hours before", "✓ Reserve now, pay later"],
    tested_pop="<strong>I visited Palatinus myself</strong> in summer. Every price, hour and pool temperature on this card was rechecked on palatinusstrand.hu on 14 November 2026.",
    photos=[CDN + p for p in [
        "64ba8e6b766876604f3f8c23_Palatinus-thermal-bath%20(17).webp",
        "64ba8f8fd37f8cd657bd715b_Palatinus-thermal-bath%20(8).webp",
        "64ba8fa2df86e673a1cc4b13_Palatinus-thermal-bath%20(14).webp",
        "64ba8ff83b619fe50e977ede_Palatinus-thermal-bath%20(16).webp",
        "64ba8fbc66506a1a5941c104_Palatinus-thermal-bath%20(15).webp",
        "64ba8fc9957c88e6a1b578d2_Palatinus-thermal-bath%20(18).webp",
        "64ba8ee0418a540aded598b6_Palatinus-thermal-bath%20(10).webp",
        "64ba9593957c88e6a1bb06fc_palatinus-indoor-pool.avif",
        "64ba8eba23c2ba332e4b9e7a_Palatinus-thermal-bath%20(20).webp",
        "64ba8f6ad6fe425eb963097a_Palatinus-thermal-bath%20(4).webp",
        "64ba8f7c93f64f70e3001a37_Palatinus-thermal-bath%20(5).webp",
        "64ba9954996fdf73d1ec3922_Palatinus-thermal-bath%20(13).webp"]],
    alt="Palatinus Bath on Margaret Island",
    pills=[
        pill("🕒", "Winter · 9:00–16:00",
             "<strong>Daily 9:00–16:00</strong> since 19 October 2026 (winter season).",
             OFFICIAL_NOTE, "bpa-time"),
        pill("🏊", "11 outdoor + 4 indoor pools",
             "<strong>Outdoor:</strong> wave pool 28 °C, swimming pool 26 °C, slide pool 26–28 °C, thermal pools 30–32 and 33–36 °C, adventure, beach, "
             "kids' and learner pools 30–36 °C. <strong>Indoor:</strong> medicinal pool 36 °C, kids' pool 32–34 °C, plunge pools 20–22 and 40–42 °C.",
             "From palatinusstrand.hu; not every outdoor pool runs in winter."),
        pill("👨‍👩‍👧", "Family tickets",
             "<strong>At the desk (2026):</strong> adult 3,800 HUF weekdays / 4,200 HUF weekends; child (3–14) 2,500 / 2,800 HUF; "
             "family ticket for 3 (at least 1 child) 7,600 / 8,400 HUF; for 4 (at least 2 children) 10,100 / 11,200 HUF.",
             "From palatinusstrand.hu/arak-2026."),
        pill("⚠️", "Winter limits",
             "The Finnish sauna is out of service from 14 November 2026, and a broken lift at the main entrance means wheelchair users cannot be received for now.",
             "From palatinusstrand.hu, 14 November 2026."),
    ],
    pick="for a summer day with kids: a wave pool, slides and lawns on Margaret Island, with family tickets.",
    skip="if you visit in winter for a long soak: it closes at 16:00, and the slides and many outdoor pools are a summer thing.",
    pros=[("Made for families", "Kids' pools indoors and out, family tickets and a wave pool."),
          ("Margaret Island setting", "Lawns and trees on an island in the Danube; easy to combine with a walk around the park."),
          ("Cheapest ticket in this list", "€27 on GetYourGuide, or 3,800 HUF at the desk on weekdays."),
          ("Same thermal water", "Thermal pools at 30–32 and 33–36 °C plus a 36 °C indoor medicinal pool.")],
    cons=[("Short winter hours", "From 19 October 2026 it is open only 9:00–16:00."),
          ("Summer crowds", "On my summer visit the wave pool and slide queues were long."),
          ("Small lockers, pricey food", "The standard lockers were small, and the food stalls were expensive for what you get.")],
    summary_q=("Is Palatinus worth it in winter?",
               "Only for a short visit. It is a summer strand first: in winter it closes at 16:00 and the Finnish sauna is currently out of service."),
    summary=["Palatinus has more of a beach vibe than a classic thermal bath. It sits on Margaret Island, where you can spend a whole day in the park, "
             "and in summer it is loved by locals and tourists alike.",
             "Based on <strong>490+ reviews</strong> on GetYourGuide and Viator, families like the kids' pools and the price. "
             "Short winter hours and summer queues are the common complaints."],
    quotes=[("If you're with young children this is the best place to experience thermal bath!", "GetYourGuide", "October 2026"),
            ("Amazing price, staff were so so helpful", "GetYourGuide", "September 2026")],
    getthere=[
        "📍 " + maps_link("Palatinus Strandfürdő Soó Rezső sétány 1 Budapest", "Soó Rezső sétány 1, 1007 Budapest (Margaret Island)"),
        "🚌 <strong>Bus 26</strong> from Nyugati pályaudvar or Árpád híd stops right outside.",
        "🚐 In the summer season the bath also runs its own minibus.",
    ],
    spcards=[
        ("Wave Pool", CDN + "64ba8f8fd37f8cd657bd715b_Palatinus-thermal-bath%20(8).webp",
         "The 28 °C wave pool is switched on at intervals and is the most fun pool here, but it gets crowded."),
        ("Kids' Pools", CDN + "64ba8fa2df86e673a1cc4b13_Palatinus-thermal-bath%20(14).webp",
         "A shallow outdoor kids' pool (30–32 °C) and an indoor one (32–34 °C) keep small children busy."),
        ("Adventure Pool", CDN + "64ba8ff83b619fe50e977ede_Palatinus-thermal-bath%20(16).webp",
         "Whirlpool, bubble benches and water jets at 30–32 °C."),
        ("Swimming Pool", CDN + "64ba8fbc66506a1a5941c104_Palatinus-thermal-bath%20(15).webp",
         "A 26 °C pool for laps."),
        ("Thermal Pools", CDN + "64ba8fc9957c88e6a1b578d2_Palatinus-thermal-bath%20(18).webp",
         "Two quieter thermal pools at 30–32 °C and 33–36 °C, ideal for a long soak."),
        ("Water Slides", CDN + "64ba8ee0418a540aded598b6_Palatinus-thermal-bath%20(10).webp",
         "The slide park belongs to the summer strand. In summer some slides had long queues."),
        ("Indoor Pools", CDN + "64ba9593957c88e6a1bb06fc_palatinus-indoor-pool.avif",
         "A 36 °C medicinal pool, a kids' pool and two plunge pools (20–22 °C and 40–42 °C). Photo: palatinusstrand.hu."),
        ("Lockers &amp; Cabins", CDN + "64ba8f6ad6fe425eb963097a_Palatinus-thermal-bath%20(4).webp",
         "Adult tickets include a locker; I found them small, so pack light. A cabin ticket costs 1,000 HUF."),
        ("Food &amp; Drink", CDN + "64ba9954996fdf73d1ec3922_Palatinus-thermal-bath%20(13).webp",
         "Food stalls serve lángos, burgers and cocktails. I found them quite expensive."),
    ],
    qf=[("Opening Hours", "Daily 9:00–16:00 in the winter season, since 19 Oct 2026 (checked 14 Nov 2026)"),
        ("Desk Prices 2026", "Adult 3,800 HUF weekdays / 4,200 HUF weekends · child 3–14: 2,500 / 2,800 HUF · family of 3: 7,600 / 8,400 HUF · cabin 1,000 HUF"),
        ("GetYourGuide Ticket", "Full day with cabin or locker: €27 (Thu 19 Nov 2026); free cancellation up to 24 hours before"),
        ("Pools &amp; Temperatures", "11 outdoor (26–36 °C, wave pool 28 °C) · 4 indoor (medicinal 36 °C, plunge 20–22 and 40–42 °C)"),
        ("Saunas &amp; Steam", "Steam cabin 40–50 °C, aroma sauna 50–60 °C · Finnish sauna out of service from 14 Nov 2026"),
        ("Towels", "Not included; towel 6,900 HUF sold at the desk"),
        ("Kids", "Family tickets and kids' pools; child ticket for ages 3–14"),
        ("Address", "Soó Rezső sétány 1, 1007 Budapest"),
        ("Nearest Transport", "Bus 26")],
    amen=[("yes", "Outdoor Pools"), ("yes", "Indoor Pools"), ("yes", "Thermal Water"), ("yes", "Steam Room"),
          ("yes", "Family-Friendly"), ("yes", "Café &amp; Food Stalls"), ("no", "Lift Out of Order")],
))

# ── 5 ─ Dandár (tested) ───────────────────────────────────────────────────────────────
CARDS.append(dict(
    key="dandar", anchor="item-5-dandar", cat="tested", tested=True,
    rank="💰 #5 Best Budget Bath", color="bpa-slate",
    area="Ferencváros, District IX", time="2 Hours", transport="Tram 2, 24",
    maps_q="Dandár Gyógyfürdő Dandár utca 3 Budapest",
    title="Dandár Thermal Bath", short="Dandár Thermal Bath",
    book="gyg", gyg_slug="budapest-dandar-thermal-bath-full-day-admission-t439882",
    ratings=[("GetYourGuide", 4.0053, 24, "gyg", None)],
    price="22", psub="per adult · full day", via="GetYourGuide",
    trust=["✓ Free cancellation up to 24 hours before", "✓ Reserve now, pay later"],
    tested_pop="<strong>I visited Dandár myself.</strong> Every price, hour and pool temperature on this card was rechecked on dandarfurdo.hu on 14 November 2026.",
    photos=[CDN + "63c6c9514fe8a2b24014ee27_7_Dand%C3%A1r%20Thermal%20Bath.webp",
            NEW + "dandar-outdoor-pools-04.avif",
            CDN + "64d4e9d0ff7680c0228646bd_Dandar-thermal-bath%20(8).webp",
            NEW + "dandar-indoor-pool-01.avif",
            CDN + "64d4e9f5506d10cbca02cdfa_Dandar-thermal-bath%20(3).webp",
            NEW + "dandar-steam-room-02.avif",
            CDN + "64d4ea02de2ee369a675e17e_Dandar-thermal-bath%20(1).webp",
            CDN + "64d4e9b7d60ebaf810e7eea7_Dandar-thermal-bath%20(6).webp",
            NEW + "dandar-facade-03.avif",
            CDN + "64d4ea144295725d07964e55_Dandar-thermal-bath%20(4).webp"],
    alt="Dandár Thermal Bath",
    pills=[
        pill("🕒", "Daily · 9:00–19:00",
             "<strong>Mon–Wed, Fri–Sun</strong> 9:00–19:00 · <strong>Thu</strong> 9:00–22:00.",
             OFFICIAL_NOTE, "bpa-time"),
        pill("🏊", "4 thermal pools",
             "<strong>Indoor:</strong> medicinal pools at 35 and 38 °C, a Finnish sauna and a cold plunge pool. "
             "<strong>Outdoor:</strong> pools at 36 and 38 °C with a lawn and sun loungers. The neck shower at the outdoor 38 °C pool is out of service for now.",
             "From dandarfurdo.hu."),
        pill("🎟️", "Cheapest desk price",
             "<strong>At the desk (2026):</strong> thermal ticket 3,500 HUF weekdays / 4,000 HUF weekends; with sauna world and outdoor pools 4,500 / 5,000 HUF; cabin 800 HUF. "
             "The GetYourGuide ticket is €22 for a full day with a cabin or locker.",
             "Desk prices from dandarfurdo.hu/arak-2026; GetYourGuide price for Thu 19 Nov 2026."),
        pill("🔞", "14+ only",
             "Only guests aged 14 and over are admitted.",
             "From dandarfurdo.hu."),
    ],
    pick="for the cheapest real thermal bath in Budapest, used mostly by locals, with outdoor hot pools.",
    skip="if you want grand architecture: Dandár is plain, and it is outside the tourist centre.",
    pros=[("Lowest price", "3,500 HUF at the desk on weekdays, the cheapest bath in this list."),
          ("Authentic local bath", "Reviewers note it is used mostly by Hungarians."),
          ("Outdoor hot pools", "Two outdoor pools at 36 and 38 °C with a lawn."),
          ("Late Thursday", "Open until 22:00 every Thursday.")],
    cons=[("Plain decor", "No palace, no dome: the building and pools are functional."),
          ("Booking-site markup", "The GetYourGuide ticket is €22 against 3,500 HUF at the desk; only 24 reviews so far."),
          ("Out of the centre", "In District IX, a tram ride from the main sights.")],
    summary_q=("Is Dandár worth visiting as a tourist?",
               "Yes, if you want a cheap, local bath and do not care about architecture. It is the opposite of Széchenyi."),
    summary=["Dandár is a little-known bath with no special charm for tourists, and its location outside the centre does not help. "
             "The decor is plain, but if you want an authentic bath where Hungarians hang out, this is the place.",
             "It is a stone's throw from the Zwack Unicum factory, so you can pair it with a visit there."],
    quotes=[("The Dandar spa is mostly used by Hungarians", "GetYourGuide", "March 2026"),
            ("A little confused upon entry, but easy enough to work out", "GetYourGuide", "August 2026")],
    getthere=[
        "📍 " + maps_link("Dandár Gyógyfürdő Dandár utca 3 Budapest", "Dandár u. 3, 1095 Budapest"),
        "🚋 <strong>Tram</strong> 2 or 24, or <strong>bus</strong> 23 or 54.",
    ],
    spcards=[
        ("Outdoor Pools", NEW + "dandar-outdoor-pools-04.avif",
         "Two outdoor pools at 36 and 38 °C, surrounded by a lawn with sun loungers. Photo: GetYourGuide listing."),
        ("Indoor Thermal Pools", NEW + "dandar-indoor-pool-01.avif",
         "Medicinal pools at 35 and 38 °C plus a cold plunge pool. Photo: GetYourGuide listing."),
        ("Sauna &amp; Steam", NEW + "dandar-steam-room-02.avif",
         "A Finnish sauna (official site); the listing photos also show a steam room. Photo: GetYourGuide listing."),
        ("Lockers &amp; Cabins", CDN + "64d4e9b7d60ebaf810e7eea7_Dandar-thermal-bath%20(6).webp",
         "A regular ticket includes a locker; a private cabin costs 800 HUF."),
        ("The Building", NEW + "dandar-facade-03.avif",
         "A brick bathhouse on Dandár utca. Photo: GetYourGuide listing."),
    ],
    qf=[("Opening Hours", "Mon–Wed, Fri–Sun 9:00–19:00 · Thu 9:00–22:00 (checked 14 Nov 2026)"),
        ("Desk Prices 2026", "Thermal ticket 3,500 HUF weekdays / 4,000 HUF weekends · with sauna and outdoor pools 4,500 / 5,000 HUF · cabin 800 HUF"),
        ("GetYourGuide Ticket", "Full day with cabin or locker: €22 (Thu 19 Nov 2026); free cancellation up to 24 hours before"),
        ("Pools &amp; Temperatures", "Indoor 35 and 38 °C + cold plunge pool · outdoor 36 and 38 °C"),
        ("Saunas &amp; Steam", "Finnish sauna"),
        ("Towels &amp; Robes", "Not included; towel 6,900 HUF and robe 12,600 HUF sold at the desk"),
        ("Age Limit", "14 and over only"),
        ("Address", "Dandár u. 3, 1095 Budapest"),
        ("Nearest Transport", "Tram 2, 24 · Bus 23, 54")],
    amen=[("yes", "Outdoor Pools"), ("yes", "Indoor Pools"), ("yes", "Thermal Water"), ("yes", "Sauna"),
          ("no", "No Children Under 14")],
))

# ── 6 ─ Veli Bej (not tested, no OTA ticket: official page) ───────────────────────────
CARDS.append(dict(
    key="veli-bej", anchor="item-6-veli-bej", cat="", tested=False,
    rank="🕌 #6 Best Quiet Ottoman Bath", color="bpa-slate",
    area="Buda, District II", time="2–3 Hours", transport="Tram 4, 6 · HÉV",
    maps_q="Irgalmasok Veli Bej Fürdője Árpád fejedelem útja 7 Budapest",
    title="Veli Bej Bath", short="Veli Bej Bath",
    book="official", official_url="https://www.irgalmasrend.hu/hu/velibej/araink",
    ratings=[("Google", 4.5, 3469, "google",
              "https://www.google.com/maps/search/?api=1&query=Irgalmasok+Veli+Bej+F%C3%BCrd%C5%91je+Budapest")],
    price_label="5,700 HUF", price=None, price_huf="5700",
    psub="per adult · Wed–Fri morning", via="the bath's ticket desk (no online booking)",
    trust=["✓ Pay at the desk", "✓ No booking needed"],
    photos=[CDN + "63c1302ece1b4bdfbf14b859_6_Veli%20Bej%20Thermal%20Bath.webp",
            NEW + "veli-bej-domes-01.avif",
            NEW + "veli-bej-domes-02.avif",
            NEW + "veli-bej-lounge-03.avif",
            NEW + "veli-bej-plaque-04.avif"],
    alt="Veli Bej Bath",
    pills=[
        pill("🕒", "6:00–12:00 · 15:00–21:00",
             "<strong>Mon–Tue</strong> 15:00–21:00 · <strong>Wed–Sun</strong> 6:00–12:00 and 15:00–21:00. Closed every day 12:00–15:00 to change the water. "
             "Cashier closes at 11:00 and 20:00. Closed on 23, 24 and 25 December 2026.",
             OFFICIAL_NOTE, "bpa-time"),
        pill("🏊", "Octagonal pool 36–38 °C",
             "<strong>Turkish bath:</strong> five pools, the octagonal central pool at 36–38 °C and four smaller pools at different temperatures. "
             "<strong>Wellness:</strong> two steam baths, Finnish sauna, infrared sauna, jacuzzi, Kneipp path and a 15 m pool at 32 °C.",
             "From the official Veli Bej pages on irgalmasrend.hu."),
        pill("🎟️", "Desk only",
             "<strong>No online tickets or booking</strong>: pay at the cashier. Morning 5,700 HUF (Wed–Fri); afternoon 6,700 HUF (Mon–Thu); "
             "Fri afternoon, Sat and Sun 7,200 HUF.",
             "From irgalmasrend.hu/hu/velibej/araink, 14 November 2026."),
        pill("🔞", "14+ only",
             "Under-14s are not admitted, even with a parent; bring an ID that shows the date of birth.",
             "From irgalmasrend.hu."),
    ],
    pick="for a quiet, authentic Ottoman bath under the old domes, without the crowds of Rudas.",
    skip="if you want to book online or bathe at midday: it is desk-only and closed 12:00–15:00.",
    pros=[("Ottoman octagonal pool", "A 36–38 °C central pool under the domes, with four smaller pools in side niches."),
          ("Calm", "Visitors consistently describe it as quiet, with empty pools early in the morning."),
          ("Full wellness area", "Two steam baths, a Finnish and an infrared sauna, a jacuzzi and a 32 °C pool.")],
    cons=[("No online booking", "Tickets are sold only at the cashier."),
          ("Split opening hours", "Closed 12:00–15:00 every day and closed on Monday and Tuesday mornings."),
          ("Small", "A handful of pools; for more variety, choose Széchenyi or Rudas.")],
    summary_q=("How is Veli Bej different from Rudas?",
               "Both are Ottoman baths, but Veli Bej is smaller, quieter and cheaper, and you cannot book it online."),
    summary=["Veli Bej is an Ottoman-era Turkish bath restored inside a modern building in Buda, run by the Brothers Hospitallers (Irgalmasrend). "
             "It is not a prime tourist destination, which is exactly why people choose it.",
             "Based on <strong>3,400+ Google reviews</strong> (4.5 out of 5), visitors consistently mention the calm and the Turkish pools. "
             "There is no booking-site ticket, so this card links to the official price page."],
    quotes=[("An Ottoman bathing experience that only allows 80 people (maximum) at a time, so it doesn't feel crowded.", "Google Maps", "October 2026"),
            ("It was very quiet, with several pools empty", "Google Maps", "May 2026"),
            ("The Turkish baths were amazing", "Google Maps", "June 2026")],
    getthere=[
        "📍 " + maps_link("Irgalmasok Veli Bej Fürdője Árpád fejedelem útja 7 Budapest", "Árpád fejedelem útja 7, 1023 Budapest (Budai Irgalmasrendi Kórház)"),
        "🚋 <strong>Tram</strong> 4 or 6, or the <strong>H5 HÉV</strong>, to Margit híd, budai hídfő; <strong>tram</strong> 17, 19 or 41 to Komjádi Béla utca; <strong>bus</strong> 9 or 109 to Császár-Komjádi uszoda.",
        "⚠️ Lukács is around the corner; do not mix them up.",
    ],
    spcards=[
        ("Ottoman Domes", NEW + "veli-bej-domes-01.avif",
         "The Ottoman domes sit inside a modern glass-and-concrete building. Photo: Christo, CC BY-SA 4.0, Wikimedia Commons."),
        ("Turkish Bath", NEW + "veli-bej-domes-02.avif",
         "The octagonal central pool is 36–38 °C, with four smaller pools of different temperatures in the side niches. Photo: Christo, CC BY-SA 4.0, Wikimedia Commons."),
        ("Wellness Area", NEW + "veli-bej-lounge-03.avif",
         "Two steam baths, a Finnish sauna, an infrared sauna, a jacuzzi, a Kneipp path and a 15 m pool at 32 °C (weekdays 15:00–21:00, all day at weekends). Photo: Firsttimeuser8, CC BY-SA 4.0, Wikimedia Commons."),
        ("History", NEW + "veli-bej-plaque-04.avif",
         "A historic stone plaque inside the bath. Photo: Firsttimeuser8, CC BY-SA 4.0, Wikimedia Commons."),
    ],
    qf=[("Opening Hours", "Mon–Tue 15:00–21:00 · Wed–Sun 6:00–12:00 and 15:00–21:00 · closed daily 12:00–15:00 (checked 14 Nov 2026)"),
        ("Desk Prices", "Morning 5,700 HUF (Wed–Fri) · afternoon 6,700 HUF (Mon–Thu) · Fri afternoon, Sat, Sun 7,200 HUF"),
        ("Online Ticket", "None: tickets are sold only at the cashier"),
        ("Pools &amp; Temperatures", "Turkish bath 5 pools (central pool 36–38 °C) · 15 m pool 32 °C · jacuzzi"),
        ("Saunas &amp; Steam", "2 steam baths, Finnish sauna, infrared sauna"),
        ("Towels", "Disposable towel 1,100 HUF and slippers 1,900 HUF sold at the desk"),
        ("Age Limit", "No under-14s, even with a parent"),
        ("Address", "Árpád fejedelem útja 7, 1023 Budapest"),
        ("Nearest Transport", "Tram 4, 6, 17, 19, 41 · Bus 9, 109 · HÉV H5")],
    amen=[("yes", "Indoor Pools"), ("yes", "Thermal Water"), ("yes", "Sauna"), ("yes", "Steam Room"),
          ("yes", "Massage"), ("no", "No Online Booking"), ("no", "No Children Under 14")],
))
