#!/usr/bin/env python3
"""Dish photos in the set-menu cartes on /best-dinner-cruises-budapest and all translations:
Hungária Koncert (menus A/B/C), Budapest Sightseeing (4 set menus) and the Goulash & Lángos supper.

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
    ("Hungária Koncert", "a"): {"starter": ["hk-starter-dips"], "main": ["hk-pork-tenderloin"], "dessert": ["hk-somloi-galuska"]},
    ("Hungária Koncert", "b"): {"starter": ["hk-starter-dips"], "main": ["hk-chicken-paprikash"], "dessert": ["hk-somloi-galuska"]},
    ("Hungária Koncert", "c"): {"starter": ["hk-starter-dips"], "main": ["hk-pasta-marinara"], "dessert": ["hk-somloi-galuska"]},
    ("Hungária Koncert", "light"): {"soup": ["gl-goulash-soup"]},
    ("Budapest Sightseeing", "m1"): {"soup": ["ss-goulash-soup"], "main": ["ss-roast-duck"]},
    ("Budapest Sightseeing", "m2"): {"main": ["ss-veal-stew"]},
    ("Budapest Sightseeing", "veg"): {"main": ["ss-goat-cheese"]},
    ("Budapest Sightseeing", "m4"): {"main": ["ss-chicken-paprikash"]},
}
CSS = """<style id="dc-set-photos-css">
.dc-pms .dish .dc-dish-photo{display:block;width:min(300px,100%);height:auto;aspect-ratio:4/3;object-fit:cover;border-radius:6px;margin:6px auto 6px;border:1px solid #eadfca;background:#fff}
@media (max-width:600px){.dc-pms .dish .dc-dish-photo{width:min(260px,100%)}}
</style>"""

DISH = re.compile(r'<div class="dish([^"]*)" data-diet="([^"]*)">(.*?)</div>', re.S)
SEC = re.compile(r'(<div class="sec" data-sec="([^"]+)">)(.*?)(?=<div class="sec"|$)', re.S)
CARTE = re.compile(r'<div class="dc-carte(?: dc-pms)?(?: on)?"[^>]*data-tier="([^"]+)"[^>]*>')


def do_carte(blk, plan, brand, path):
    blk = re.sub(r'<img class="dc-dish-photo"[^>]*>', "", blk)

    def fix_sec(m):
        head, key, body = m.group(1), m.group(2), m.group(3)
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
        plan = next((v for (bp, t), v in MAP.items() if brand.startswith(bp) and t == m.group(1)), None)
        if not plan:
            continue
        tag = m.group(0)
        if "dc-pms" not in tag:
            tag = tag.replace('class="dc-carte', 'class="dc-carte dc-pms', 1)
        blk = tag + do_carte(blk[len(m.group(0)):], plan, brand, path)
        s = s[:a] + blk + s[b:]
        n += sum(1 for v in plan.values() for k in v if k)
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
        cnt = new.count(f'src="{A}')
        if cnt != n or n < 19:
            print("unexpected photo count:", p, cnt, "planned", n); bad += 1
        if check:
            cur = open(p, encoding="utf-8").read()
            if cur.count(f'src="{A}') != n:
                print("missing photos:", p); bad += 1
        else:
            cur = open(p, encoding="utf-8").read()
            if new != cur:
                open(p, "w", encoding="utf-8").write(new)
    print("pages:", len(pages()), "problems:", bad)
    sys.exit(1 if bad else 0)
