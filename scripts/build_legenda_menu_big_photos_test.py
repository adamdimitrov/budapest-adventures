#!/usr/bin/env python3
"""TEST ONLY: Legenda's official dish photos (legenda.hu dinner_menu.pdf) inside Legenda's
dropdown menu only (top card menu + Legenda detail section menu). noindex. Two compact layouts:
  best-dinner-cruises-budapest-test-menu.html       A: 2-column photo grid per course
  best-dinner-cruises-budapest-test-menu-list.html  B: list rows, small square photo left of the dish
"""
import re
SRC = "best-dinner-cruises-budapest.html"
P = "/assets/test/legenda-menu/legenda-dinner-menu-"
MENU = {"Great scallop": "scallop", "Cold goose liver": "goose-liver", "Goat cheese mousse": "goat-cheese-mousse",
        "Beef tartare": "beef-tartare", "Chicken breast, strawberry": "chicken-brie-salad", "Roasted trout": "trout",
        "Pork shoulder": "pork-shoulder", "Rosemary duck breast": "duck-breast", "Beef confit": "beef-confit",
        "Cauliflower steak": "cauliflower-steak", "Seared red tuna": "tuna-steak", "Panna cotta": "panna-cotta",
        "Cheesecake, poppy": "cheesecake", "“Sweet dream”": "chocolate-cake"}

CSS = {
"grid": """
.dc-pm .sec{display:grid;grid-template-columns:1fr 1fr;gap:14px 12px;align-items:start}
.dc-pm .sec h4{grid-column:1/-1;margin-bottom:0}
.dc-pm .sec .ou{display:none}
.dc-pm .dish{margin:0;font-size:14px;line-height:1.3}
.dc-pm .dish .dc-dish-photo{display:block;width:100%;height:auto;aspect-ratio:4/3;object-fit:cover;border-radius:6px;margin:0 0 6px;border:1px solid #eadfca;background:#fff}
""",
"list": """
.dc-pm .sec .ou{display:none}
.dc-pm .dish{display:flex;align-items:center;gap:12px;text-align:left;max-width:440px;margin:0 auto;padding:7px 0;border-top:1px solid #f1e8d6;font-size:15px;line-height:1.3}
.dc-pm .sec h4+.dish{border-top:0}
.dc-pm .dish:not(:has(.dc-dish-photo)){padding-left:84px}
.dc-pm .dish .dc-dish-photo{flex:0 0 72px;width:72px;height:72px;object-fit:cover;border-radius:8px;border:1px solid #eadfca;background:#fff}
.dc-pm .dish .pair{margin-top:3px}
""",
}
OUT = {"grid": "best-dinner-cruises-budapest-test-menu.html", "list": "best-dinner-cruises-budapest-test-menu-list.html"}

base = open(SRC, encoding="utf-8").read()
base = re.sub(r'<meta[^>]*name="robots"[^>]*/?>', "", base)
base = base.replace("<head>", '<head><meta name="robots" content="noindex, nofollow"/>', 1)


def addpics(block, variant):
    for start, key in MENU.items():
        pat = re.compile(r'(<div class="dish" data-diet="[^"]*">)(' + re.escape(start) + r'[^<]*)(.*?</div>)')
        src = f'{P}{key}-sq.webp' if variant == "list" else f'{P}{key}-800.webp'
        size = 'width="160" height="160"' if variant == "list" else 'width="800" height="534"'
        block, m = pat.subn(lambda mm: (
            f'{mm.group(1)}<img class="dc-dish-photo" src="{src}" alt="Legenda dinner cruise: {mm.group(2).strip()}" '
            f'{size} loading="lazy" decoding="async"/><span class="dc-dish-txt">{mm.group(2)}{mm.group(3)[:-6]}</span></div>'), block)
        assert m == 1, (start, m)
    return block.replace('<div class="dc-carte on"', '<div class="dc-carte on dc-pm"', 1)


for variant in ("grid", "list"):
    s = base
    for marker in ('id="dc-menu-legenda"', '<span class="ltt-bento-group-title">🍽️ Gourmet Dinner Menu'):
        a = s.index(marker); a = s.index('<div class="dc-carte on"', a); b = s.index('<div class="foot">', a)
        s = s[:a] + addpics(s[a:b], variant) + s[b:]
    s = s.replace("</head>", f'<style id="legenda-menu-photos-test">{CSS[variant]}</style></head>', 1)
    open(OUT[variant], "w", encoding="utf-8").write(s)
    print(variant, "photos:", s.count('class="dc-dish-photo"'))
