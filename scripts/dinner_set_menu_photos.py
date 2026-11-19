#!/usr/bin/env python3
"""Dish photos in the set-menu cartes on /best-dinner-cruises-budapest and all translations:
Hungária Koncert (menus A/B/C), Budapest Sightseeing (4 set menus), the Goulash & Lángos supper
and Silverline (one dessert, from our own test dinner). On the EN page only, each of those cards'
Food box also gets a Legenda-style photo button (thumbnails + "N dish photos" + Full menu).

Photos are the operators' own listing photos (GetYourGuide galleries), cropped to one dish each,
only where the plate clearly is the menu dish. Placed by carte tier + course + position, so it
works in every language. Covers the breakdown cartes and the modal templates. Idempotent.
    python3 scripts/dinner_set_menu_photos.py          # apply
    python3 scripts/dinner_set_menu_photos.py --check  # exit 1 if a page is missing photos
Legenda (à la carte grid) is handled by scripts/legenda_menu_photos.py.
"""
import html, re, subprocess, sys

A = "/assets/best-dinner-cruises-budapest/menu-photos/"
# (brand prefix, data-tier) -> {course: [photo per dish position, None = no photo]}
MAP = {
    ("Hungária Koncert", "a"): {"starter": ["hk-starter-dips"], "soup": ["gl-goulash-soup"], "main": ["hk-pork-tenderloin"], "dessert": ["hk-somloi-galuska"]},
    ("Hungária Koncert", "b"): {"starter": ["hk-starter-dips"], "main": ["hk-chicken-paprikash"], "dessert": ["hk-somloi-galuska"]},
    ("Hungária Koncert", "c"): {"starter": ["hk-starter-dips"], "main": ["hk-pasta-marinara"], "dessert": ["hk-somloi-galuska"]},
    ("Hungária Koncert", "light"): {"soup": ["gl-goulash-soup"]},
    ("Budapest Sightseeing", "m1"): {"soup": ["ss-goulash-soup"], "main": ["ss-roast-duck"]},
    ("Budapest Sightseeing", "m2"): {"main": ["ss-veal-stew"]},
    ("Budapest Sightseeing", "veg"): {"main": ["ss-goat-cheese"]},
    ("Budapest Sightseeing", "m4"): {"main": ["ss-chicken-paprikash"]},
    # Silverline (GYG listing photos, current menu): panzanella, beef ragout soup, cod, sweet potato, lemon curd
    ("Silverline", "all"): {"starter": ["sl-panzanella"], "soup": ["sl-beef-ragout-soup", None],
                            "main": ["sl-walnut-cod", None, None, "sl-sweet-potato"],
                            "dessert": ["sl-coriander-lemon-curd", None, None]},
    # River Diva winter buffet (EN only; translations still carry an older buffet): sections are all
    # data-sec="x", so they are keyed by index. #3 = mains, Korean-style fried chicken thigh is 5th.
    ("River Diva", "buffet"): {"#3": [None, None, None, None, "rd-korean-chicken", None, None]},
}
EN_ONLY = {("River Diva", "buffet")}
# River Diva: a buffet gallery at the top of its carte (EN only)
BUFFET = ["rd-buffet-salmon", "rd-buffet-croquettes", "rd-buffet-chicken-rice", "rd-buffet-line"]
# Food-box photo button (EN page only): data-dc-menu -> thumbnails in display order (all photos of that menu)
TEASER = {
    "hk": ["hk-pork-tenderloin", "hk-chicken-paprikash", "hk-pasta-marinara", "hk-somloi-galuska", "hk-starter-dips", "gl-goulash-soup"],
    "seesight": ["ss-roast-duck", "ss-veal-stew", "ss-goat-cheese", "ss-chicken-paprikash", "ss-goulash-soup"],
    "goulash": ["gl-goulash-soup"],
    "silverline": ["sl-walnut-cod", "sl-sweet-potato", "sl-panzanella", "sl-coriander-lemon-curd", "sl-beef-ragout-soup"],
    "diva": ["rd-buffet-salmon", "rd-buffet-croquettes", "rd-korean-chicken", "rd-buffet-line", "rd-buffet-chicken-rice"],
}
TEASER_WORD = {"diva": "buffet photo"}
EN = "best-dinner-cruises-budapest.html"
CSS = """<style id="dc-set-photos-css">
.dc-pms .dish .dc-dish-photo{display:block;width:min(300px,100%);height:auto;aspect-ratio:4/3;object-fit:cover;border-radius:6px;margin:6px auto 6px;border:1px solid #eadfca;background:#fff}
@media (max-width:600px){.dc-pms .dish .dc-dish-photo{width:min(260px,100%)}}
@media (min-width:601px){.dc-food-photos .th.n1{grid-template-columns:72px}.dc-food-photos .th.n2{grid-template-columns:repeat(2,72px)}.dc-food-photos .th.n3{grid-template-columns:repeat(3,72px)}}
.dc-buffet-pics{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:14px 0 4px}
.dc-buffet-pics img{display:block;width:100%;height:auto;aspect-ratio:4/3;object-fit:cover;border-radius:6px;border:1px solid #eadfca}
@media (max-width:600px){.dc-food-photos.one{display:flex;align-items:center;gap:12px}.dc-food-photos.one .th{grid-template-columns:72px;flex:0 0 auto}.dc-food-photos.one .tx{flex-direction:column;align-items:flex-start;gap:3px;margin-top:0}}
</style>"""


def teaser(s, menu, keys):
    m = re.search(r'<button aria-haspopup="dialog" class="dc-food-btn" data-dc-menu="%s" type="button">([^<]*)</button>' % menu, s)
    assert m, menu
    label = m.group(1).replace("↗", "").strip()
    food_end = s.index('<div class="dc-dna">', m.end())
    food_end = s.index("</div>", food_end) + 6
    if s.startswith('<div class="dc-sets">', food_end):
        food_end = s.index("</div>", food_end) + 6
    n = len(keys); shown = keys[:4]
    more = f' class="more" data-more="+{n - 3}"'
    tiles = "".join(
        f'<span{more if (i == 3 and n > 4) else ""}><img src="{A}{k}-sq.webp" alt="" width="240" height="240" loading="lazy" decoding="async"></span>'
        for i, k in enumerate(shown))
    txt = f"{n} {TEASER_WORD.get(menu, 'dish photo')}" + ("s" if n != 1 else "")
    btn = (f'<button class="dc-food-photos{" one" if n == 1 else ""}" data-dc-menu="{menu}" aria-haspopup="dialog" type="button">'
           f'<span class="th n{len(shown)}" aria-hidden="true">{tiles}</span><span class="tx"><span>📷 {txt}</span> <b>{label} ↗</b></span></button>')
    return s[:food_end] + btn + s[food_end:]

DISH = re.compile(r'<div class="dish([^"]*)" data-diet="([^"]*)">(.*?)</div>', re.S)
SEC = re.compile(r'(<div class="sec" data-sec="([^"]+)">)(.*?)(?=<div class="sec"|$)', re.S)
CARTE = re.compile(r'<div class="dc-carte(?: dc-pms)?(?: on)?"[^>]*data-tier="([^"]+)"[^>]*>')


def do_carte(blk, plan, brand, path):
    blk = re.sub(r'<img class="dc-dish-photo"[^>]*>', "", blk)

    idx = [-1]

    def fix_sec(m):
        idx[0] += 1
        head, key, body = m.group(1), m.group(2), m.group(3)
        if key not in plan:
            key = f"#{idx[0]}"
        if key not in plan:
            return m.group(0)
        dishes = list(DISH.finditer(body))
        assert len(dishes) == len(plan[key]), (path, brand, key, len(dishes))
        out, last = [], 0
        for d, photo in zip(dishes, plan[key]):
            out.append(body[last:d.start()])
            img = ""
            if photo:
                name = html.unescape(re.sub(r"<span.*", "", d.group(3), flags=re.S)).strip()
                img = (f'<img class="dc-dish-photo" src="{A}{photo}.webp" alt="{html.escape(brand + ": " + name, quote=True)}" '
                       f'width="600" height="450" loading="lazy" decoding="async">')
            out.append(f'<div class="dish{d.group(1)}" data-diet="{d.group(2)}">{img}{d.group(3)}</div>')
            last = d.end()
        out.append(body[last:])
        return head + "".join(out)

    return SEC.sub(fix_sec, blk)


def process(path):
    s = open(path, encoding="utf-8").read()
    n = 0  # photos the matched cartes should carry
    for m in reversed(list(CARTE.finditer(s))):
        a = m.start(); b = s.index('<div class="foot">', a)
        blk = s[a:b]
        brand = re.search(r'class="brand">([^<·]*)', blk).group(1).strip()
        hit = next(((bp, t) for (bp, t) in MAP if brand.startswith(bp) and t == m.group(1)), None)
        if not hit or (hit in EN_ONLY and path != EN):
            continue
        plan = MAP[hit]
        tag = m.group(0)
        if "dc-pms" not in tag:
            tag = tag.replace('class="dc-carte', 'class="dc-carte dc-pms', 1)
        blk = tag + do_carte(blk[len(m.group(0)):], plan, brand, path)
        blk = re.sub(r'<div class="dc-buffet-pics">.*?</div>', "", blk, flags=re.S)
        if hit == ("River Diva", "buffet"):
            pics = "".join(f'<img src="{A}{k}.webp" alt="River Diva winter buffet" width="600" height="450" loading="lazy" decoding="async">' for k in BUFFET)
            blk = blk.replace('<div class="dc-hl-count"></div>', '<div class="dc-hl-count"></div><div class="dc-buffet-pics">' + pics + '</div>', 1)
        s = s[:a] + blk + s[b:]
        n += sum(1 for v in plan.values() for k in v if k)
    s = re.sub(r'<button class="dc-food-photos[^"]*" data-dc-menu="(?!legenda")[^"]*".*?</button>', "", s, flags=re.S)
    if path == EN:
        for menu, keys in TEASER.items():
            s = teaser(s, menu, keys)
    s = re.sub(r'<style id="dc-set-photos-css">.*?</style>', "", s, flags=re.S)
    s = s.replace("</head>", CSS + "</head>", 1)
    return s, n


def pages():
    out = subprocess.check_output(["git", "grep", "-l", 'id="dc-menu-hk"', "--", "*.html"], text=True).split()
    return [p for p in out if "-test" not in p]


if __name__ == "__main__":
    check = "--check" in sys.argv
    bad = 0
    for p in pages():
        new, n = process(p)
        cnt = new.count(f'class="dc-dish-photo" src="{A}')
        if cnt != n or n < 19:
            print("unexpected photo count:", p, cnt, "planned", n); bad += 1
        if check:
            cur = open(p, encoding="utf-8").read()
            if cur.count(f'class="dc-dish-photo" src="{A}') != n:
                print("missing photos:", p); bad += 1
        else:
            cur = open(p, encoding="utf-8").read()
            if new != cur:
                open(p, "w", encoding="utf-8").write(new)
    print("pages:", len(pages()), "problems:", bad)
    sys.exit(1 if bad else 0)
