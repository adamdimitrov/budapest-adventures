#!/usr/bin/env python3
"""TEST ONLY: best-dinner-cruises-budapest-test.html = live page + Legenda's official
current-menu photos (from legenda.hu dinner_menu.pdf) appended to the Legenda food filmstrip.
Not for production until the photo use is settled with Legenda."""
import re
SRC, OUT = "best-dinner-cruises-budapest.html", "best-dinner-cruises-budapest-test.html"
P = "/assets/test/legenda-menu/legenda-dinner-menu-"
DISHES = [
    ("scallop", "Starter: great scallop with chili"),
    ("goose-liver", "Starter: cold goose liver with onion jam"),
    ("goat-cheese-mousse", "Veggie starter: goat cheese mousse, beetroot caviar, apple and sage chutney"),
    ("beef-tartare", "Starter: beef tartare, red onion, garlic cream"),
    ("chicken-brie-salad", "Starter: chicken breast, strawberry, rocket, rhubarb, brie"),
    ("trout", "Main: roasted trout, lemongrass sauce, pink peppercorn, rice pilaf"),
    ("pork-shoulder", "Main: pork shoulder, kápia pepper purée, oyster mushroom, baby corn"),
    ("duck-breast", "Main: rosemary duck breast, sweet potato bake, quince and fig"),
    ("beef-confit", "Main: beef confit, Dijon carrot purée, Brussels sprouts, bread dumpling"),
    ("cauliflower-steak", "Veggie main: cauliflower steak, curry, yogurt, pistachio"),
    ("tuna-steak", "Main: seared red tuna steak, caper butter, red onion purée, salad"),
    ("panna-cotta", "Dessert: panna cotta, forest fruit rose jam"),
    ("cheesecake", "Dessert: cheesecake, poppy seed, raspberry"),
    ("chocolate-cake", "Dessert: “Sweet dream” chocolate cake, strawberry ragout"),
]
s = open(SRC, encoding="utf-8").read()
assert s.count('name="robots"') == 0 or True
s = re.sub(r'<meta[^>]*name="robots"[^>]*/?>', "", s)
s = s.replace("<head>", '<head><meta name="robots" content="noindex, nofollow"/>', 1)

pill = "Menu + Swipe 7 Food Photos →"
assert s.count(pill) == 1
i = s.index(pill)
a = s.index('<div class="ltt-filmstrip-wrap">', i)
b = s.index('<div class="dc-carte-wrap">', a)
strip = s[a:b]
old = len(re.findall(r'class="ltt-strip-slide"', strip))
assert old == 7, old
total = old + len(DISHES)
strip = re.sub(r'<span class="ltt-strip-num">(\d+) / 7</span>', lambda m: f'<span class="ltt-strip-num">{m.group(1)} / {total}</span>', strip)
new = "".join(
    f'<div class="ltt-strip-slide"><span class="ltt-strip-num">{old + n} / {total}</span>'
    f'<img alt="Legenda candlelit dinner cruise current menu. {cap}" loading="lazy" src="{P}{key}.webp"/>'
    f'<div class="ltt-strip-cap"><span>Current menu. {cap} (photo: Legenda)</span></div></div>'
    for n, (key, cap) in enumerate(DISHES, 1))
last = strip.rindex('<div class="ltt-strip-slide">')
end = last
depth = 0
for m in re.finditer(r'<div\b|</div>', strip[last:]):
    depth += 1 if m.group(0) != "</div>" else -1
    if depth == 0:
        end = last + m.end(); break
strip = strip[:end] + new + strip[end:]
s = s[:a] + strip + s[b:]
s = s.replace(pill, f"Menu + Swipe {total} Food Photos →", 1)
open(OUT, "w", encoding="utf-8").write(s)
print("slides", total)
