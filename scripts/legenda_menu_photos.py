#!/usr/bin/env python3
"""Legenda's official dish photos (from legenda.hu dinner_menu.pdf) in Legenda's menu
on /best-dinner-cruises-budapest and all its translations, as a compact photo grid
(3 columns, 2 on phones). Placed by course + position, so it works in every language.

Covers both Legenda menus on each page: the detail-section carte and the
#dc-menu-legenda modal template. Idempotent: re-running strips and re-adds.
    python3 scripts/legenda_menu_photos.py          # apply
    python3 scripts/legenda_menu_photos.py --check  # exit 1 if a page is missing photos
"""
import html, re, subprocess, sys

A = "/assets/best-dinner-cruises-budapest/legenda-menu/legenda-dinner-menu-"
# Legenda candlelit menu, in menu order. None = no official photo (salmon, both soups).
PHOTOS = {
    "starter": ["scallop", "goose-liver", None, "goat-cheese-mousse", "beef-tartare", "chicken-brie-salad"],
    "soup": [None, None],
    "main": ["trout", "pork-shoulder", "duck-breast", "beef-confit", "cauliflower-steak", "tuna-steak"],
    "dessert": ["panna-cotta", "cheesecake", "chocolate-cake"],
}
N = sum(1 for v in PHOTOS.values() for k in v if k)

CSS = """<style id="dc-menu-photos-css">
.dc-pm .sec:has(.dc-dish-photo){display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px 10px;align-items:start}
.dc-pm .sec:has(.dc-dish-photo) h4{grid-column:1/-1;margin-bottom:0}
.dc-pm .sec:has(.dc-dish-photo) .ou{display:none}
.dc-pm .sec:has(.dc-dish-photo) .dish{margin:0;font-size:13px;line-height:1.3}
.dc-pm .dish .dc-dish-photo{display:block;width:100%;height:auto;aspect-ratio:4/3;object-fit:cover;border-radius:6px;margin:0 0 6px;border:1px solid #eadfca;background:#fff}
.dc-pm .sec:has(.dc-dish-photo) .dish:not(:has(.dc-dish-photo))::before{content:"\\1F37D";display:flex;align-items:center;justify-content:center;width:100%;aspect-ratio:4/3;box-sizing:border-box;margin:0 0 6px;border-radius:6px;border:1px dashed #d9c79e;background:#fdf8ec;font-size:22px;opacity:.7}
@media (max-width:600px){
.ltt-bento-group-body>.dc-carte-wrap:has(.dc-pm){margin-left:-12px;margin-right:-12px}
.dc-carte.dc-pm{padding:20px 10px}
.dc-carte.dc-pm::before{display:none}
.dc-pm .sec:has(.dc-dish-photo){grid-template-columns:1fr 1fr;gap:12px 8px}
.dc-pm .sec:has(.dc-dish-photo) .dish{font-size:12.5px;line-height:1.25}
.dc-pm .sec:has(.dc-dish-photo) .dish .pair{font-size:10.5px}
.dc-pm .sec:has(.dc-dish-photo) .dish:not(:has(.dc-dish-photo))::before{font-size:18px}
}
</style>"""

DISH = re.compile(r'<div class="dish([^"]*)" data-diet="([^"]*)">(.*?)</div>', re.S)
SEC = re.compile(r'(<div class="sec" data-sec="([^"]+)">)(.*?)(?=<div class="sec"|$)', re.S)


def do_carte(blk, path):
    blk = re.sub(r'<img class="dc-dish-photo"[^>]*>', "", blk)
    blk = blk.replace(" dc-pm", "", 1)

    def fix_sec(m):
        head, key, body = m.group(1), m.group(2), m.group(3)
        if key not in PHOTOS:
            return m.group(0)
        dishes = list(DISH.finditer(body))
        assert len(dishes) == len(PHOTOS[key]), (path, key, len(dishes))
        out, last = [], 0
        for d, photo in zip(dishes, PHOTOS[key]):
            out.append(body[last:d.start()])
            img = ""
            if photo:
                name = html.unescape(re.sub(r"<span.*", "", d.group(3), flags=re.S)).strip()
                img = (f'<img class="dc-dish-photo" src="{A}{photo}.webp" alt="Legenda: {html.escape(name, quote=True)}" '
                       f'width="800" height="534" loading="lazy" decoding="async">')
            out.append(f'<div class="dish{d.group(1)}" data-diet="{d.group(2)}">{img}{d.group(3)}</div>')
            last = d.end()
        out.append(body[last:])
        return head + "".join(out)

    blk = SEC.sub(fix_sec, blk)
    return re.sub(r'<div class="dc-carte on', '<div class="dc-carte on dc-pm', blk, count=1)


def process(path):
    s = open(path, encoding="utf-8").read()
    starts = [m.start() for m in re.finditer(r'<div class="dc-carte on[^"]*"', s)]
    done = 0
    for a in reversed(starts):
        b = s.index('<div class="foot">', a)
        blk = s[a:b]
        if "Legenda" not in blk[:400] or 'data-sec="starter"' not in blk:
            continue
        s = s[:a] + do_carte(blk, path) + s[b:]
        done += 1
    assert done == 2, (path, done)
    s = re.sub(r'<style id="dc-menu-photos-css">.*?</style>', "", s, flags=re.S)
    s = s.replace("</head>", CSS + "</head>", 1)
    return s


def pages():
    out = subprocess.check_output(["git", "grep", "-l", 'id="dc-menu-legenda"', "--", "*.html"], text=True).split()
    return [p for p in out if "-test" not in p]


if __name__ == "__main__":
    check = "--check" in sys.argv
    bad = 0
    for p in pages():
        new = process(p)
        cur = open(p, encoding="utf-8").read()
        if check:
            n = cur.count('class="dc-dish-photo"')
            if n != 2 * N:
                print("missing photos:", p, n); bad += 1
        elif new != cur:
            open(p, "w", encoding="utf-8").write(new)
        if not check:
            print(p, new.count('class="dc-dish-photo"'))
    sys.exit(1 if bad else 0)
