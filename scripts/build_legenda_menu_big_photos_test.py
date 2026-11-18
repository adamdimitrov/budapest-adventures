#!/usr/bin/env python3
"""TEST ONLY: best-dinner-cruises-budapest-test-menu.html = live page + Legenda's official
dish photos (legenda.hu dinner_menu.pdf) at full width inside Legenda's dropdown menu only
(top card menu + Legenda detail section menu). No other placements. noindex."""
import re
SRC, OUT = "best-dinner-cruises-budapest.html", "best-dinner-cruises-budapest-test-menu.html"
P = "/assets/test/legenda-menu/legenda-dinner-menu-"
MENU = {"Great scallop": "scallop", "Cold goose liver": "goose-liver", "Goat cheese mousse": "goat-cheese-mousse",
        "Beef tartare": "beef-tartare", "Chicken breast, strawberry": "chicken-brie-salad", "Roasted trout": "trout",
        "Pork shoulder": "pork-shoulder", "Rosemary duck breast": "duck-breast", "Beef confit": "beef-confit",
        "Cauliflower steak": "cauliflower-steak", "Seared red tuna": "tuna-steak", "Panna cotta": "panna-cotta",
        "Cheesecake, poppy": "cheesecake", "“Sweet dream”": "chocolate-cake"}

s = open(SRC, encoding="utf-8").read()
s = re.sub(r'<meta[^>]*name="robots"[^>]*/?>', "", s)
s = s.replace("<head>", '<head><meta name="robots" content="noindex, nofollow"/>', 1)


def addpics(block):
    for start, key in MENU.items():
        pat = re.compile(r'(<div class="dish" data-diet="[^"]*">)(' + re.escape(start) + r")([^<]*)")
        block, m = pat.subn(lambda mm: (
            f'{mm.group(1)}<img class="dc-dish-photo" src="{P}{key}-800.webp" '
            f'srcset="{P}{key}-800.webp 800w, {P}{key}.webp 1200w" sizes="(max-width: 600px) 92vw, 520px" '
            f'alt="Legenda dinner cruise: {(mm.group(2) + mm.group(3)).strip()}" width="800" height="534" '
            f'loading="lazy" decoding="async"/>{mm.group(2)}{mm.group(3)}'), block)
        assert m == 1, (start, m)
    return block


for marker in ('id="dc-menu-legenda"', '<span class="ltt-bento-group-title">🍽️ Gourmet Dinner Menu'):
    a = s.index(marker); a = s.index('<div class="dc-carte on"', a); b = s.index('<div class="foot">', a)
    s = s[:a] + addpics(s[a:b]) + s[b:]

CSS = """<style id="legenda-menu-big-photos-test">
.dc-carte .dish .dc-dish-photo{display:block;width:100%;height:auto;aspect-ratio:3/2;object-fit:cover;border-radius:6px;margin:14px 0 8px;border:1px solid #eadfca;background:#f6efe1}
.dc-carte .ou{margin-top:12px}
.dc-wall .dc-carte .dish .dc-dish-photo{margin:10px 0 6px}
</style>"""
s = s.replace("</head>", CSS + "</head>", 1)
open(OUT, "w", encoding="utf-8").write(s)
print("photos:", s.count('class="dc-dish-photo"'))
