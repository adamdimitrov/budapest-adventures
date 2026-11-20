"""Menu modal data for /best-dinner-cruises-budapest (restored 14 November 2026).

Each deck card gets a "Food" row (level meter, course strip, course dots) whose
"Full menu" button opens the #dc-modal bottom sheet with a <template id="dc-menu-*">.

Cards 1 to 3 (tested) reuse the menu cartes from their detailed breakdown, so the
modal and the breakdown always show the same verified menu. Cards 4 to 6 have no
carte in the breakdown; their menus below were read from the operators' current
published menu options on 14 November 2026.

OPTS lists separately bookable variants (own price or own link). A variant with
link=None is shown greyed out as "Not bookable now".
"""

SL = "https://budapestrivercruise.eu/product/{slug}/?code=bpadventures"
SRC_NOTE = "Source: operator&rsquo;s published menu options, checked Nov 14, 2026"


def dots(spec):
    """'..v' -> three dots, the last one vegetarian."""
    return "".join('<i class="%s"></i>' % ("v" if ch == "v" else "") for ch in spec)


def course(label, sec, spec):
    n = len(spec)
    return ('<button aria-label="%s: %d choice%s" class="dc-c" data-sec="%s" type="button"><b>%s</b>'
            '<span class="dc-dots">%s</span><em>%d</em></button>' % (label, n, "" if n == 1 else "s", sec, label, dots(spec), n))


def buf(label, cls=""):
    inner = '<i class="inf%s">%s</i>' % ((" " + cls) if cls else "", "🍸 ∞" if cls == "bar" else "∞")
    return '<span class="dc-c dc-buf"><b>%s</b><span class="dc-dots">%s</span></span>' % (label, inner)


ARROW = '<span class="dc-arrow">›</span>'
LEVEL = {1: "Light supper", 2: "Full dinner", 3: "Fine dining"}


def food(menu_id, level, lvl_text, strip, dna, sets=None):
    sep = '<span class="sep">›</span>'
    strip_html = sep.join(strip) if isinstance(strip, list) else strip
    sets_html = ""
    if sets:
        sets_html = ('<div class="dc-sets"><span class="dc-sets-lbl">Pick a set menu</span>%s</div>'
                     % "".join('<button class="dc-set%s" data-go="%s" type="button">%s</button>'
                               % (" veg" if veg else "", go, label) for go, label, veg in sets))
    return ('<div class="dc-food"><div class="dc-food-head"><span class="dc-food-lbl">🍽️ Food</span>'
            '<span aria-hidden="true" class="dc-meter" data-l="%d" title="Food level %d of 3: %s"><i></i><i></i><i></i></span>'
            '<span class="dc-food-tier" data-l="%d">%s</span><span class="dc-food-lvl">%s</span>'
            '<button aria-haspopup="dialog" class="dc-food-btn" data-dc-menu="%s" type="button">Full menu ↗</button></div>'
            '<div class="dc-food-strip">%s</div><div class="dc-dna">%s</div>%s</div>'
            % (level, level, LEVEL[level], level, LEVEL[level], lvl_text, menu_id, strip_html, dna, sets_html))


def dish(text, veg=False, sm=False):
    tag = '<span class="dc-tag veg">Veg</span>' if veg else ""
    return '<div class="dish%s" data-diet="%s">%s%s</div>' % (" sm" if sm else "", "veg" if veg else "", text, tag)


def sec(sec_id, title, dishes):
    return '<div class="sec" data-sec="%s"><h4>%s</h4>%s</div>' % (sec_id, title, '<div class="ou">or</div>'.join(dishes) if sec_id != "x" else "".join(dishes))


def carte(tier, on, brand, h3, price, secs, foot, link, nveg):
    return ('<div class="dc-carte%s" data-ngf="0" data-nveg="%d" data-tier="%s"><div class="brand">%s</div><h3>%s</h3>'
            '<div class="price">%s</div><div class="dc-hl-count"></div>%s<div class="foot">%s</div>'
            '<a class="cta" href="%s" rel="nofollow sponsored noopener" target="_blank">Book this menu →</a>'
            '<div class="src">%s</div></div>'
            % (" on" if on else "", nveg, tier, brand, h3, price, "".join(secs), foot, link, SRC_NOTE))


def tiers(tabs):
    return '<div class="dc-tier" role="group" aria-label="Menu options">%s</div>' % "".join(
        '<button class="%s" data-t="%s" type="button">%s</button>' % ("on" if i == 0 else "", t, label)
        for i, (t, label) in enumerate(tabs))


# ── deck food rows ───────────────────────────────────────────────────────────────────
FOOD = {
    "legenda-candlelit": food(
        "legenda", 3, "4-course à la carte · 17 dishes to pick from",
        ["Scallop or goose liver", "Sour-cherry soup", "Duck, beef or tuna", "Panna cotta"],
        ARROW.join([course("Starter", "starter", ".....v"), course("Soup", "soup", ".."),
                    course("Main", "main", "....v."), course("Dessert", "dessert", "...")])),
    "silverline-dinner": food(
        "silverline", 3, "4-course gourmet · same menu on all 3 cruises",
        ["Burrata panzanella", "Beef ragout soup", "Cod, pork, lamb or sweet potato", "Lemon curd"],
        ARROW.join([course("Starter", "starter", "."), course("Soup", "soup", ".."),
                    course("Main", "main", "...v"), course("Dessert", "dessert", "...")])),
    "hungaria-koncert-dinner": food(
        "hk", 2, "4-course set menu · pick A, B or C",
        ["Dip trio", "Goulash", "Széchenyi pork or paprikash", "Somlói galuska"],
        ARROW.join([course("Starter", "starter", "v"), course("Soup", "soup", "..v"),
                    course("Main", "main", "..v"), course("Dessert", "dessert", "v")]),
        sets=[("a", "A Urban Classic", False), ("b", "B Paprika Mood", False), ("c", "C Veggie Flow", True)]),
    "seesight-folk-dinner": food(
        "seesight", 2, "Served set menu · 4 to choose from",
        ["Pâté or aubergine cream", "Goulash, Újházi or pea soup", "Duck, veal, chicken or goat&rsquo;s cheese", "Strudel, Somlói or pancake"],
        ARROW.join([course("Starter", "starter", "...v"), course("Soup", "soup", "...v"),
                    course("Main", "main", "...v"), course("Dessert", "dessert", "...v")]),
        sets=[("m1", "Roast Duck", False), ("m2", "Veal Stew", False), ("veg", "Vegetarian", True), ("m4", "Poultry", False)]),
    "river-diva-buffet": food(
        "diva", 2, "Chef&rsquo;s buffet · go back for seconds",
        'Starters<span class="sep">›</span>Mains &amp; sides<span class="sep">›</span>Desserts<span class="mid">🍸 Open bar</span>',
        ARROW.join([buf("Starters"), buf("Mains"), buf("Soups"), buf("Veg", "v"), buf("Desserts")])
        + '<span class="dc-arrow">+</span>' + buf("Open bar", "bar")),
    "goulash-langos": food(
        "goulash", 1, "Goulash and/or lángos · not a full dinner",
        ["Goulash soup", "Lángos"],
        ARROW.join([course("Soup", "soup", "."), course("Lángos", "langos", "v")])),
}

# template id per card (cards 1 to 3 take their carte from the breakdown)
MENU_ID = {"legenda-candlelit": "legenda", "silverline-dinner": "silverline", "hungaria-koncert-dinner": "hk",
           "seesight-folk-dinner": "seesight", "river-diva-buffet": "diva", "goulash-langos": "goulash"}

# modal header/footer per card: (kicker, price, sub)
MODAL = {
    "legenda-candlelit": ("Legenda City Cruises", "€110", "Free cancellation up to 24h"),
    "silverline-dinner": ("Silverline Cruises", "From €77", "3 shows • €77 or €91"),
    "hungaria-koncert-dinner": ("Hungária Koncert", "From €67", "Free cancellation up to 24h"),
    "seesight-folk-dinner": ("Budapest Sightseeing", "From €66", "Free cancellation up to 24h"),
    "river-diva-buffet": ("River Diva", "€99", "Drinks included"),
    "goulash-langos": ("Hungária Koncert", "€44", "Free cancellation up to 24h"),
}


def cartes(key, link):
    """Menu cartes for the cards without one in the breakdown (4 to 6)."""
    if key == "seesight-folk-dinner":
        b = "Budapest Sightseeing · Dock 6"
        p = "from €66 per person"
        f = "Choose your menu when booking • Welcome Prosecco included • Live Ökrös Band folk music &amp; dance"
        st, so, ma, de = "starter", "soup", "main", "dessert"
        return tiers([("m1", "Roast Duck"), ("m2", "Veal Stew"), ("veg", "Vegetarian 🌱"), ("m4", "Poultry")]) + "".join([
            carte("m1", True, b, "Traditional Menu · Roast Duck", p, [
                sec(st, "Starter", [dish("Duck liver pâté, Tokaji ice-wine raisins")]),
                sec(so, "Soup", [dish("Goulash soup")]),
                sec(ma, "Main course", [dish("Roast duck leg, onion crushed potatoes, stewed cabbage")]),
                sec(de, "Dessert", [dish("Apple &amp; sour-cherry strudel")])], f, link, 0),
            carte("m2", False, b, "Traditional Menu · Veal Stew", p, [
                sec(st, "Starter", [dish("Pâté")]),
                sec(so, "Soup", [dish("Újházi chicken soup")]),
                sec(ma, "Main course", [dish("Veal stew, egg noodles")]),
                sec(de, "Dessert", [dish("Somlói galuska (traditional sponge cake)")])], f, link, 0),
            carte("veg", False, b, "Vegetarian Menu", p, [
                sec(st, "Starter", [dish("Aubergine cream, garden vegetables", True)]),
                sec(so, "Soup", [dish("Green pea cream soup, coriander cottage-cheese dumplings", True)]),
                sec(ma, "Main course", [dish("Grilled goat&rsquo;s cheese, sweet potatoes, raspberry-vinegar salad", True)]),
                sec(de, "Dessert", [dish("Gundel pancake", True)])], f, link, 4),
            carte("m4", False, b, "Traditional Menu · Poultry", p, [
                sec(st, "Starter", [dish("Pâté")]),
                sec(so, "Soup", [dish("Újházi chicken soup")]),
                sec(ma, "Main course", [dish("Chicken paprikash, potato gratin")]),
                sec(de, "Dessert", [dish("Cheesecake, strawberry")])], f, link, 0),
        ])
    if key == "river-diva-buffet":
        return carte("buffet", True, "River Diva · Akadémia 3", "Winter Buffet (26 Nov to 25 Dec 2026)",
                     "€99 per person · drinks included", [
                         sec("x", "Welcome", [dish("Smoked aubergine cream", sm=True)]),
                         sec("x", "Starters &amp; salads", [dish("Citrus-smoked trout", sm=True), dish("Marinated salmon", sm=True),
                                                            dish("Caesar salad", sm=True), dish("Salad bar", True, True)]),
                         sec("x", "Soups", [dish("Bean goulash", sm=True), dish("Cream of cauliflower", True, True)]),
                         sec("x", "Mains", [dish("Chestnut-stuffed turkey roulade", sm=True), dish("Whole duck breast", sm=True),
                                            dish("Juniper venison ragout", sm=True), dish("Sage &amp; garlic pork roulade", sm=True),
                                            dish("Korean-style fried chicken thigh", sm=True), dish("Chicken fricassée", sm=True),
                                            dish("Pike-perch, Keszthely style", sm=True)]),
                         sec("x", "Desserts", [dish("Chestnut slice", sm=True), dish("Coffee opera slice", sm=True),
                                               dish("Sour-cherry tart", sm=True)]),
                         sec("x", "Unlimited bar · served to your table", [
                             dish("Cocktails: Aperol Spritz, Lillet Spritz, Negroni, Old Fashioned, Margarita, Cosmopolitan", sm=True),
                             dish("Gin &amp; tonic, spirits and mocktails", sm=True), dish("Paulus Secco and Hungarian wines", sm=True),
                             dish("Draught Dreher Gold, Asahi, Pilsner Urquell, alcohol-free beer", sm=True),
                             dish("Soft drinks &amp; water", sm=True)])],
                     "A selection from the winter buffet; vegan and vegetarian dishes are marked on board • Until 25 Nov the autumn menu is served • Live music",
                     link, 2)
    if key == "goulash-langos":
        return carte("light", True, "Hungária Koncert · Gróf Széchenyi", "Goulash &amp; Lángos Supper", "€44 per person, any option", [
            sec("soup", "Soup", [dish("Bowl of Hungarian goulash soup (vegetarian soup on request)")]),
            sec("langos", "Lángos", [dish("Fresh lángos, crispy fried flatbread", True)]),
            sec("x", "Included", [dish("Welcome Prosecco or juice", sm=True), dish("Live Rajkó folk musicians", sm=True),
                                  dish("90-minute cruise past Parliament", sm=True)])],
            "Book goulash, lángos or both (same price) • Departs 19:00 sharp from Akadémia 2 • Other drinks paid on board",
            link, 1)
    raise KeyError(key)


# ── separately bookable variants (deck + breakdown) ──────────────────────────────────
OPTS = {
    "silverline-dinner": [
        ("🕯️ Dinner &amp; Lights: no show", "Sunset departure • background music • upper deck", "€77", SL.format(slug="dinner-lights")),
        ("💃 Folk &amp; Operetta Show", "Operetta singers, folk dancers, csárdás lesson", "€91", SL.format(slug="budapest-danube-dinner-cruise")),
        ("🎹 Live Piano Show", "No bookable dates in Nov or Dec 2026", "€91", None),
    ],
}

OPTS_CSS = (".dc-opt-off{background:#f8fafc;border-color:#e2e8f0;cursor:default;opacity:.6}"
            ".dc-opt-off:hover{border-color:#e2e8f0}.dc-opt-off .dc-opt-price{color:#64748b}"
            ".dc-opt-off .dc-opt-price small{color:#64748b}"
            ".dc-modal-price{min-width:0;flex:0 1 auto}"
            ".dc-modal-cta:not(#dc-x):not(#dc-y){white-space:normal;text-align:center;flex:0 1 auto;max-width:62%}")


def opts_html(key, style=""):
    rows = []
    for name, meta, price, link in OPTS[key]:
        if link:
            rows.append('<a class="dc-opt" href="%s" onclick="event.stopPropagation()" rel="nofollow sponsored noopener" target="_blank">'
                        '<span class="dc-opt-name">%s</span><span class="dc-opt-meta">%s</span>'
                        '<span class="dc-opt-price">%s<small>Book →</small></span></a>' % (link, name, meta, price))
        else:
            rows.append('<div aria-disabled="true" class="dc-opt dc-opt-off">'
                        '<span class="dc-opt-name">%s</span><span class="dc-opt-meta">%s</span>'
                        '<span class="dc-opt-price">%s<small>Not bookable now</small></span></div>' % (name, meta, price))
    st = ' style="%s"' % style if style else ""
    return '<div class="dc-opts"%s>%s</div>' % (st, "".join(rows))
