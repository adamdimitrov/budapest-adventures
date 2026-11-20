#!/usr/bin/env python3
"""Things to do (EN): cards 2-25 get the river cruise card layout: 6-8 pills in two rows
(time, languages, access & kids, price, what you get, vibe, place), a map link in the kicker
and the cancellation / pay-later trust lines.

Every new fact comes from the card's own booking listing as read on 2026-11-19 (included vs
not included taken from the listing's tick/cross marks). Card 7 reuses the pills of the same
cruise (t416276) on best-night-cruises-budapest. Existing pills are kept word for word.

    python3 scripts/ttd_pills_2026_11.py && python3 scripts/listicle.py build best-things-to-do-budapest.html
"""
import html
import importlib.util
import json
import os
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "listicles", "best-things-to-do-budapest.json")
NIGHT = os.path.join(ROOT, "data", "listicles", "best-night-cruises-budapest.json")

KIND = {"time": " bpa-time", "access": " cd-access", "vibe": " fbm-vibe", "": ""}
YES, NO, ASK = '<span class="cd-yes">✓</span>', '<span class="cd-no">✕</span>', '<span class="cd-ask">ⓘ</span>'


def pill(emoji, label, lead, body="", kind="", notes=(), langs=None):
    pop = f"<strong>{lead}</strong>" + (f" {body}" if body else "")
    pop += "".join(f'<span class="bpa-lang-note">{n}</span>' for n in notes)
    p = {"cls": "bpa-lang" + KIND[kind], "emoji": emoji, "label": html.escape(label, quote=False), "pop_html": pop}
    if langs:
        p["data"] = {"langs": langs}
    return p


def access(label, wheel=None, stroller=None, kids=None):
    notes = []
    if wheel:
        notes.append(f"♿ <b>Wheelchair:</b> {wheel}")
    if stroller:
        notes.append(f"👶 <b>Stroller:</b> {stroller}")
    if kids:
        notes.append(f"🎟️ <b>Kids:</b> {kids}")
    return {"cls": "bpa-lang cd-access", "emoji": "♿", "label": html.escape(label, quote=False),
            "pop_html": "".join(f'<span class="bpa-lang-note">{n}</span>' for n in notes)}


def maplink(label, query):
    return {"url": "https://maps.google.com/?q=" + urllib.parse.quote_plus(query), "rel": "noopener noreferrer",
            "target": "_blank", "onclick": "event.stopPropagation()", "map": html.escape(label, quote=False)}


TRUST = ["<b>Free cancellation</b> up to 24 h before, full refund", "<b>Reserve now, pay later</b>: nothing to pay today"]

# Per card: map link (label, query) and the pills in final order. "T", "P", "L" = the card's
# existing time, price and place pills (kept as they are).
CARDS = {
    "card-2": (("Széchenyi Bath, City Park", "Széchenyi Thermal Bath Budapest"), [
        "T",
        access("14+ only", wheel=f"{NO} not suitable for wheelchair users", kids=f"{NO} under 14 not allowed in the spa"),
        "P",
        pill("🔐", "Locker or cabin", "Entry plus a locker or a private cabin,", "depending on the option you pick. One entry, valid for the day."),
        pill("🩴", "Bring flip-flops & towel", "Slippers are mandatory and nothing can be rented:", "bring swimwear, a towel, flip-flops, a swimming cap and an ID card. Massages and food cost extra."),
        pill("🙂", "Big and social", "Budapest's largest thermal bath complex, 3 outdoor and 15 indoor pools in a 1913 Neo-Baroque building.", "Lively rather than quiet: compare the smaller baths if you want calm.", kind="vibe"),
        "L"]),
    "card-3": (("Parliament Visitor Centre", "Hungarian Parliament Visitor Centre Kossuth Lajos tér 1 Budapest"), [
        "T",
        pill("🎧", "26-language audio guide", "Audio guide languages:", "Arabic, Bulgarian, Chinese, Croatian, Czech, Dutch, English, French, German, Greek, Hebrew, Hungarian, Italian, Japanese, Korean, Polish, Portuguese, Romanian, Russian, Serbian, Slovak, Slovenian, Spanish, Turkish, Ukrainian and Vietnamese.",
             langs="ar bg zh hr cs nl en fr de el he hu it ja ko pl pt ro ru sr sk sl es tr uk vi"),
        "P",
        pill("👑", "Dome Hall & Crown", "45 minutes inside:", "the Main Staircase, the Hall of the Dome with the Holy Crown, the Assembly Hall and the History of the House exhibition, plus an audio tour of the square outside."),
        pill("🪪", "Bring your ID", "Passport or ID card required", "at the security check. Plan 15 minutes for check-in. No pets."),
        pill("🎧", "At your own pace", "Self-guided with headphones, no live guide on this ticket.", "Want a person to ask questions? The official guided tour is the live-guide option.", kind="vibe"),
        "L"]),
    "card-4": (("Zero Kilometre Stone", "Zero Kilometre Stone Clark Ádám tér Budapest"), [
        "T",
        pill("🗣️", "6 languages", "Live guide in", "English, German, Spanish, French, Italian or Hungarian.", langs="en de es fr it hu"),
        access("Not step-free", wheel=f"{NO} cobblestones, hills and stairs; wheelchairs and mobility scooters not recommended",
               stroller=f"{NO} strollers and large bags not allowed", kids="under 18s must come with an adult"),
        "P",
        pill("⛪", "Church or bunker upgrade", "Add a guided visit inside Matthias Church or the Hospital in the Rock nuclear bunker.", "Their entry is only included with the upgrade."),
        pill("🥾", "Hilly walk", "2.5 to 3.5 hours on foot over uneven cobblestones, inclines and stairs.", "Comfortable shoes; it runs in all weather.", kind="vibe"),
        "L"]),
    "card-5": (("Szentháromság tér", "Szentháromság tér Budapest"), [
        "T",
        pill("🗣️", "4 languages", "Live guide in", "English, French, German or Italian.", langs="en fr de it"),
        access("Wheelchair-friendly", wheel=f"{YES} listed as wheelchair-accessible"),
        "P",
        pill("👥", "Max 10 people", "Small group, limited to 10.", "A 2-hour guided walk past Matthias Church, Fisherman's Bastion and the Royal Palace courtyards."),
        pill("🎟️", "Entry fees extra", "The guide is included, entry tickets are not.", "Tips and hotel pickup are not included either."),
        pill("🌦️", "Rain or shine", "Cobbled streets, palace courtyards and river views;", "the walk runs in any weather.", kind="vibe"),
        "L"]),
    "card-6": (("Szent István tér 2", "St. Stephen's Basilica Szent István tér 2 Budapest"), [
        pill("🕒", "Church 9:00–17:45", "Church:", "Monday to Saturday 9:00 to 17:45, Sunday 13:00 to 17:45. <strong>Dome and treasury:</strong> daily 9:00 to 19:00. About an hour, including the dome climb.",
             kind="time", notes=("The box office closes 30 minutes before closing; arrive any time before that.",)),
        access("Not step-free", wheel=f"{NO} listed as not suitable for wheelchair users"),
        "P",
        pill("🎟️", "Skip the ticket queue", "Pre-reserved entry to the main church hall.", "Treasury, panoramic terrace or a guided tour come with the matching option."),
        pill("✋", "Holy Right relic", "St. Stephen's mummified right hand,", "Hungary's most sacred relic."),
        pill("⛪", "Working church", "A working church, not just a museum.", "On weekends, weddings can briefly close the main hall.", kind="vibe"),
        "L"]),
    "card-8": (("Szimpla Kert, Kazinczy utca", "Szimpla Kert Kazinczy utca 14 Budapest"), [
        "T",
        pill("🗣️", "English guides", "The pub crawl runs in English.", langs="en"),
        access("18+ only", kids=f"{NO} under 18 not allowed on the crawl; bring a passport or ID card"),
        "P",
        pill("🎟️", "VIP entry, 4 venues", "Fast-track entry", "to Instant-Fogas, Füge Udvar, La Siesta and Humbak."),
        pill("🥃", "Free shots", "A welcome shot at every venue,", "plus digital photos taken by the guide. Food is not included."),
        pill("🎉", "High-energy night", "A 5 to 5.5 hour party with games, built for meeting people.", "Drinking on the street is illegal in Budapest, so the drinks stay inside the bars.", kind="vibe"),
        "L"]),
    "card-9": (("Heroes' Square", "Hősök tere Budapest"), [
        "T",
        pill("🗣️", "English only", "The night walk runs in English.", langs="en"),
        access("16+, step-free", wheel=f"{YES} listed as wheelchair-accessible", kids=f"{NO} not for children under 16: the stories are dark"),
        "P",
        pill("🎭", "Actor-guide", "Real Hungarian true crime cases,", "told by an actor on a 105-minute walk through City Park after dark."),
        pill("🧥", "Dress for night", "Outdoors at night, whatever the weather.", "Food, drinks and weather gear are not included."),
        pill("🕯️", "Spooky storytelling", "Mystery, murder and drama in the dark park,", "not a history lecture.", kind="vibe"),
        "L"]),
    "card-10": (("Café Gerbeaud, Vörösmarty tér", "Café Gerbeaud Vörösmarty tér 7 Budapest"), [
        "T",
        pill("🗣️", "English", "The café walk runs in English.", langs="en"),
        "P",
        pill("🎓", "Art historian guide", "Led by an art historian:", "the guides are professors, historians, journalists and published authors."),
        pill("☕", "Grand cafés", "From Café Gerbeaud to the Museum Café,", "ending at the Art Nouveau Kazinczy Street Synagogue. 3 hours; the coffee and cake you order are paid separately."),
        pill("👥", "Max 8 people", "Small group, limited to 8,", "so there is room at the café table.", kind="vibe"),
        "L"]),
    "card-11": (("Dohány Street Synagogue", "Dohány Street Synagogue Dohány utca 2 Budapest"), [
        "T",
        pill("🗣️", "English guide", "Guided in English.", langs="en"),
        access("Not step-free", wheel=f"{NO} listed as not suitable for wheelchair users", kids="bring a passport or ID card; no large bags or pets"),
        "P",
        pill("🎟️", "3 entries included", "Entry to the Dohány Street Synagogue, the Jewish Museum and the Raoul Wallenberg Memorial Park,", "with fast-track entry.",
             notes=("The 4-hour option adds the Rumbach Synagogue and the Ghetto Wall exhibition.",)),
        pill("🕯️", "Moving, not light", "Holocaust memorial stops on a heritage walk:", "a quiet, respectful tour.", kind="vibe"),
        "L"]),
    "card-12": (("Great Market Hall", "Great Market Hall Fővám tér Budapest"), [
        "T",
        pill("🗣️", "English guide", "The food tour runs in English.", langs="en"),
        "P",
        pill("🍲", "12+ tasters", "Goulash, lángos, cold cuts, pickles, chimney cake and a Hungarian dessert,", "with a wine selection and a homemade spirit. Non-alcoholic swaps on request."),
        pill("🥗", "Veggie OK, no coeliac", "Vegetarian and vegan guests can join,", "but may not taste every item. Coeliac diets can't be catered for (cross-contamination)."),
        pill("👥", "Small, local group", "A 3-hour walk with a local guide, off the usual tourist track.", "The market is quieter on Sundays.", kind="vibe"),
        "L"]),
    "card-13": (("Dárda utca 2", "Dárda utca 2 Budapest"), [
        "T",
        pill("🗣️", "English guide", "Live guide in English.", langs="en"),
        access("No wheelchairs", wheel=f"{NO} not accessible for wheelchairs", stroller=f"{NO} strollers not allowed",
               kids="under 3 not permitted; not for claustrophobia or mobility issues"),
        "P",
        pill("🥶", "12°C inside", "It stays at 12°C (54°F) all year:", "bring a warm layer, closed shoes and clothes that can get dirty."),
        pill("👥", "Up to 25 people", "Groups of up to 25 on a 1.5 km paved, lit route.", "No phone signal underground, no filming."),
        pill("🔦", "Underground labyrinth", "Natural limestone caverns joined to 800-year-old cellars,", "once wine cellars, bomb shelters and a prison.", kind="vibe"),
        "L"]),
    "card-14": (("MonsteRoller, Bécsi utca 8", "Bécsi utca 8 Budapest"), [
        "T",
        pill("🗣️", "English guide", "Local guide in English.", langs="en"),
        access("14+ to drive", wheel=f"{NO} not for people with mobility impairments or pregnant women",
               kids="14+ to drive; 10+ on the back seat of a double-seater"),
        "P",
        pill("🛴", "Wide-wheel e-scooter", "A MonsteRoller, helmet, and a rain poncho and gloves when needed.", "Short training first, no licence required; top speed 25 km/h."),
        pill("👥", "Max 10 people", "Small groups of up to 10;", "larger groups are split."),
        pill("😄", "Fun, fast, no climb", "See more in less time, without the walk up the hill.", "Casual clothes; no high heels, skirts not advised.", kind="vibe"),
        "L"]),
    "card-15": (("St. Stephen's Basilica", "Szent István tér 1 Budapest"), [
        "T",
        pill("🗣️", "English, Spanish", "Licensed tour leader in", "English or Spanish (Italian on some dates).", langs="en es it"),
        access("Wheelchair-friendly", wheel=f"{YES} listed as wheelchair-accessible"),
        "P",
        pill("🎟️", "Basilica skip-the-line", "A skip-the-line Basilica visit inside and out,", "then the Shoes Memorial, the Chain Bridge and a finish at the Parliament. 2 hours."),
        pill("🏛️", "Parliament outside only", "The walk ends at the Parliament,", "but the Parliament ticket is not included."),
        pill("👥", "Small group", "Small group guaranteed,", "2 hours on foot through the centre.", kind="vibe"),
        "L"]),
    "card-16": (("Hungarian Parliament", "Kossuth Lajos tér Budapest"), [
        "T",
        pill("🗣️", "English guide", "Guide trained in history, in English.", langs="en"),
        "P",
        pill("🎟️", "Skip the ticket queue", "Your guide brings the museum ticket,", "so you skip the ticket office."),
        pill("☢️", "Cold War bunker stop", "The walk passes the Soviet memorial on Liberty Square", "and the vents of a secret Cold War nuclear bunker."),
        pill("🕯️", "Heavy themes", "Interrogation cells and the 1956 revolution:", "serious, not for young children.", kind="vibe"),
        "L"]),
    "card-17": (("Andrássy út 22", "Hungarian State Opera House Andrássy út 22 Budapest"), [
        "T",
        pill("🗣️", "5 languages", "Live guide in", "English, German, French, Italian or Spanish.", langs="en de fr it es"),
        access("Not step-free", wheel=f"{NO} listed as not suitable for wheelchair users"),
        "P",
        pill("🎶", "Mini concert", "A short live concert on the landing of the grand staircase", "at the end of the tour."),
        pill("🎟️", "Skip the ticket queue", "Interior visit with a live guide, 60 minutes.", "Lighting in the auditorium is sometimes dimmed."),
        pill("✨", "Gilded and grand", "Frescoes and the restored auditorium;", "tours can move to another date during rehearsals.", kind="vibe"),
        "L"]),
    "card-18": (("Báthory utca 19", "Báthory utca 19 Budapest"), [
        "T",
        pill("🗣️", "English, Spanish", "Live guide in English or Spanish;", "some tours run bilingual.", langs="en es"),
        access("Some stairs", wheel=f"{ASK} stairs in the Castle District: tell the operator in advance about mobility needs"),
        "P",
        pill("🚌", "Bus + walks", "3 hours by coach with a live guide:", "Heroes' Square, Elisabeth Bridge, the Castle District and the Basilica. Entrance fees and tips are extra."),
        pill("🙂", "Easy overview", "Both banks in 3 hours,", "with short walks off the bus. A good first day.", kind="vibe"),
        "L"]),
    "card-19": (("Zero Kilometre Stone", "Zero Kilometre Stone Clark Ádám tér Budapest"), [
        "T",
        pill("🗣️", "6 languages", "Live guide in", "English, German, Spanish, French, Italian or Hungarian.", langs="en de es fr it hu"),
        access("Not step-free", wheel=f"{NO} cobblestones, hills and stairs; wheelchairs and mobility scooters not recommended",
               stroller=f"{NO} strollers and large bags not allowed", kids="under 18s must come with an adult"),
        "P",
        pill("⛪", "Guided church visit", "Pick the Matthias Church upgrade", "for a guided visit inside; without it you see the church from outside."),
        pill("🥾", "Hilly walk", "2.5 to 3.5 hours on cobblestones and stairs.", "Comfortable shoes; it runs in all weather.", kind="vibe"),
        "L"]),
    "card-20": (("Döbrentei tér 9", "Rudas Baths Döbrentei tér 9 Budapest"), [
        "T",
        access("14+ only", wheel=f"{YES} listed as wheelchair-accessible", kids=f"{NO} under 14 not allowed in the spa"),
        "P",
        pill("🍽️", "3-course meal", "A 3-course à la carte meal or the chef's menu at Rudas Bistro,", "with a coffee, lemonade, wine or champagne on some options. You pick the table time; swim before or after."),
        pill("🧖", "Turkish bath option", "Full access adds the Ottoman Turkish bath;", "the Wellness ticket covers the panorama pool and saunas only."),
        pill("🩴", "Bring your kit", "Towels, robes, swimwear, flip-flops and the mandatory swim cap are not included", "and can't be rented, only bought at the desk."),
        pill("🌇", "Rooftop views", "The panorama pool looks over the Danube", "and the city: a bath with a view.", kind="vibe"),
        "L"]),
    "card-21": (("St. Stephen's Basilica", "Szent István tér 1 Budapest"), [
        "T",
        "P",
        pill("🎻", "Organ, vocals, flute", "Organist Miklós Teleki with Eleonóra Krusic and vocalist Kolos Kováts:", "Bach, Mozart, Verdi and more."),
        pill("🎟️", "Concert ticket", "The ticket is for the concert only.", "The dome and treasury are not part of it."),
        pill("🏛️", "Basilica acoustics", "Inside the neo-classical Basilica,", "whose acoustics the programme is built around."),
        pill("🕯️", "Calm evening", "A seated, quiet evening:", "a trio, not an orchestra.", kind="vibe"),
        "L"]),
    "card-22": (("Palatinus Strand", "Palatinus Strand Margaret Island Budapest"), [
        "T",
        access("Family-friendly", wheel=f"{YES} listed as wheelchair-accessible", kids="family-friendly pools and waterslides"),
        "P",
        pill("🔐", "Cabin or locker", "Full-day admission any day of the week", "with a cabin or a locker."),
        pill("🌊", "Pools & slides", "Thermal pools, waterslides, steam rooms and saunas.", "In winter the venue closes at 15:00."),
        pill("🩴", "Bring flip-flops", "Bring flip-flops and beachwear;", "no pets."),
        pill("🌳", "Island park day", "Green and relaxed:", "the pools sit inside a car-free park in the Danube.", kind="vibe"),
        "L"]),
    "card-23": (("Ipar utca 11", "Ipar utca 11 Budapest"), [
        "T",
        pill("🗣️", "English instructor", "Led by an English-speaking instructor.", langs="en"),
        access("Families welcome", kids="one adult needed for every 4 children; allergens: wheat, milk, nuts, orange and coconut in a small shared space"),
        "P",
        pill("🧑‍🍳", "Hands-on baking", "Ingredients, tools and an apron included.", "The dough is risen for you (it needs 75 minutes), so you roll, wrap and bake."),
        pill("🎓", "Cake + certificate", "Take home your chimney cake with toppings", "and a certificate. Coffee or tea included."),
        pill("😄", "Fun for all ages", "An easy, playful workshop", "for families, couples and friends.", kind="vibe"),
        "L"]),
    "card-24": (("Memento Park", "Memento Park Balatoni út Szabadkai utca Budapest"), [
        "T",
        access("Gravel paths", wheel=f"{NO} gravel paths may not suit wheelchair users"),
        "P",
        pill("🎬", "Spy film included", "Entry includes the film show on the former secret service", "in the Most Cheerful Barrack, and the exhibition under Stalin's Boots."),
        pill("🚗", "Sit in a Trabant", "An original Trabant to sit in", "for photos."),
        pill("🚌", "Transport not included", "Getting there is up to you:", "the ticket has no transport and no guide."),
        pill("🗿", "Open-air oddity", "Giant socialist statues in a field:", "part history lesson, part surreal photo stop.", kind="vibe"),
        "L"]),
    "card-25": (("Báthory utca 19", "Báthory utca 19 Budapest"), [
        "T",
        pill("🗣️", "English & Spanish", "Bilingual tour in English and Spanish.", langs="en es"),
        "P",
        pill("🏰", "Visegrád Castle ticket", "Visegrád Castle entry is included,", "with an air-conditioned coach and a live guide. Lunch and tips are extra."),
        pill("⛴️", "Boat back in summer", "May to September (Thursday to Sunday) you return by boat;", "otherwise, or when the water is too high or low, by coach."),
        pill("⛪", "Esztergom Basilica", "Hungary's largest cathedral and the Renaissance Bakócz Chapel,", "plus a Danube viewpoint towards Slovakia."),
        pill("🙂", "Long, easy day", "9 hours: about 6 at the stops and 3 on the road.", "Three towns without planning a thing.", kind="vibe"),
        "L"]),
}


def main():
    d = json.load(open(DATA))
    night = json.load(open(NIGHT))
    cruise = next(c for c in night["cards"] if "t416276" in c["cta"]["btn"]["url"])
    byc = {p["cls"].strip(): p for p in cruise["pills"]}
    cruise_p = {p["label"]: p for p in cruise["pills"]}
    CARDS["card-7"] = (("Chain Bridge", "Széchenyi Chain Bridge Budapest"), [
        "T", cruise_p["English guide"], byc["bpa-lang cd-access"], "P",
        cruise_p["Unlimited Prosecco &amp; Beer"], cruise_p["Open top deck"], byc["bpa-lang fbm-vibe"], "L"])

    for c in d["cards"][1:]:
        mp, plan = CARDS[c["id"]]
        old = c["pills"]
        T = next(p for p in old if "bpa-time" in p["cls"])
        L = next(p for p in old if p["emoji"] == "📍")
        P = next(p for p in old if p is not T and p is not L)
        new = []
        for x in plan:
            new.append({"T": T, "P": P, "L": L}[x] if isinstance(x, str) else x)
        assert 6 <= len(new) <= 8, (c["id"], len(new))
        c["pills"] = new
        # kicker: place, duration, map link
        k = [x for x in c["kicker"] if not isinstance(x, dict)]
        if k and not k[-1].startswith("⏱️"):
            k[-1] = "⏱️ " + k[-1]
        c["kicker"] = k + [maplink(*mp)]
        c["cta"].setdefault("trust", TRUST)

    # card 25: the listing includes the Visegrád Castle ticket (only lunch is extra)
    c25 = d["cards"][24]
    for p in c25["pills"]:
        p["pop_html"] = p["pop_html"].replace("Lunch and the Visegrád Castle ticket are extra.", "Lunch is extra; the Visegrád Castle ticket is included.")
    for f in c25["faq"]["items"]:
        if f["a"] == "No, and neither is the Visegrád Castle ticket.":
            f["a"] = "No, lunch is extra. The Visegrád Castle ticket is included."

    spec = importlib.util.spec_from_file_location("kit_listicle", os.path.join(ROOT, "kit", "scripts", "listicle.py"))
    kit = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(kit)
    open(DATA, "w").write(kit.dumps(d) + "\n")
    print("cards 2-25:", [len(c["pills"]) for c in d["cards"][1:]])


if __name__ == "__main__":
    main()
