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
# "14 dish photos" per language (path prefix; EN page has none)
PHOTOS_TXT = {
    "en": "{n} dish photos", "bg": "{n} снимки на ястията", "cs": "{n} fotek jídel", "de": "{n} Fotos der Gerichte",
    "el": "{n} φωτογραφίες πιάτων", "es": "{n} fotos de los platos", "fr": "{n} photos des plats",
    "he": "{n} תמונות של המנות", "hr": "{n} fotografija jela", "hu": "{n} ételfotó", "it": "{n} foto dei piatti",
    "ja": "料理の写真{n}枚", "ko": "요리 사진 {n}장", "nl": "{n} foto's van de gerechten", "pl": "{n} zdjęć dań",
    "pt": "{n} fotos dos pratos", "ro": "{n} fotografii cu preparatele", "ru": "{n} фото блюд",
    "sk": "{n} fotografií jedál", "sr": "{n} фотографија јела", "tr": "{n} yemek fotoğrafı", "uk": "{n} фото страв",
}

CSS = """<style id="dc-menu-photos-css">
.dc-pm .sec:has(.dc-dish-photo){display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px 10px;align-items:start}
.dc-pm .sec:has(.dc-dish-photo) h4{grid-column:1/-1;margin-bottom:0}
.dc-pm .sec:has(.dc-dish-photo) .ou{display:none}
.dc-pm .sec:has(.dc-dish-photo) .dish{margin:0;font-size:13px;line-height:1.3}
.dc-pm .dish .dc-dish-photo{display:block;width:100%;height:auto;aspect-ratio:4/3;object-fit:cover;border-radius:6px;margin:0 0 6px;border:1px solid #eadfca;background:#fff}
.dc-pm .sec:has(.dc-dish-photo) .dish:not(:has(.dc-dish-photo))::before{content:"\\1F37D";display:flex;align-items:center;justify-content:center;width:100%;aspect-ratio:4/3;box-sizing:border-box;margin:0 0 6px;border-radius:6px;border:1px dashed #d9c79e;background:#fdf8ec;font-size:22px;opacity:.7}
.dc-food-photos{display:block;width:100%;margin-top:10px;padding:8px;border:1px solid #e9d8ae;border-radius:12px;background:#fdf6e3;cursor:pointer;font:inherit;text-align:left;transition:border-color .2s,box-shadow .2s}
.dc-food-photos .th{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px}
.dc-food-photos .th span{position:relative;display:block;border-radius:8px;overflow:hidden;aspect-ratio:1;background:#fff;box-shadow:0 1px 3px rgba(60,40,10,.15)}
.dc-food-photos .th img{display:block;width:100%;height:100%;object-fit:cover;transition:transform .35s}
.dc-food-photos .th .more::after{content:attr(data-more);position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:rgba(28,25,23,.5);color:#fff;font-weight:800;font-size:17px;letter-spacing:.02em}
.dc-food-photos .tx{display:flex;align-items:center;justify-content:space-between;gap:8px;flex-wrap:wrap;margin-top:7px;padding:0 2px;font-size:13px;font-weight:800;color:#92400e;line-height:1.25}
.dc-food-photos .tx b{font-size:12.5px;font-weight:700;color:#0369a1;text-decoration:underline;white-space:nowrap}
.dc-food-photos:hover{border-color:#d9b867;box-shadow:0 4px 14px rgba(146,64,14,.12)}
.dc-food-photos:hover .th img{transform:scale(1.06)}
.dc-food-photos:hover .tx,.dc-food-photos:hover .tx b{color:#92400e}
.dc-food:has(.dc-food-photos) .dc-food-head .dc-food-btn{display:none}
@media (max-width:600px){
.dc-food-head .dc-food-lvl{order:9;flex-basis:100%}
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
    # photo teaser button at the bottom of Legenda's Food box (deck card)
    s = re.sub(r'<button class="dc-food-photos".*?</button>', "", s, flags=re.S)
    m = re.search(r'<button aria-haspopup="dialog" class="dc-food-btn" data-dc-menu="legenda" type="button">([^<]*)</button>', s)
    assert m, path
    label = m.group(1).replace("↗", "").strip()
    lang = path.split("/")[0] if "/" in path else "en"
    txt = PHOTOS_TXT[lang].format(n=N)
    dna = s.index('<div class="dc-dna">', m.end())
    end = s.index("</div>", dna) + 6
    keys = ("scallop", "goose-liver", "duck-breast", "panna-cotta")
    more = f' class="more" data-more="+{N - 3}"'
    thumbs = "".join(f'<span{more if i == 3 else ""}><img src="{A}{k}-tile.webp" alt="" width="240" height="240" loading="lazy" decoding="async"></span>'
                     for i, k in enumerate(keys))
    teaser = (f'<button class="dc-food-photos" data-dc-menu="legenda" aria-haspopup="dialog" type="button">'
              f'<span class="th" aria-hidden="true">{thumbs}</span><span class="tx"><span>📷 {txt}</span> <b>{label} ↗</b></span></button>')
    s = s[:end] + teaser + s[end:]
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
