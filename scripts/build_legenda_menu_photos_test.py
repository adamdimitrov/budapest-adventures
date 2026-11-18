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

# ---------------------------------------------------------------- top card (#1 Legenda)
CAP = dict(DISHES)
ci = s.index('id="card-1"'); cj = s.index('id="card-2"')
c = s[ci:cj]

# (5) card gallery: duck + scallop become photos 2 and 3
GAL = ["duck-breast", "scallop"]
a = c.index('<div aria-label="Photo gallery 1" class="bpa-slider"')
first = c.index("/>", c.index("<img", a)) + 2
lazy_ph = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 500'%3E%3C/svg%3E"
c = c[:first] + "".join(
    f' <img alt="Legenda candlelit dinner cruise current menu: {CAP[k].split(": ",1)[1]}" data-src="{P}{k}-800.webp" '
    f'decoding="async" height="534" loading="lazy" src="{lazy_ph}" width="800"/>' for k in GAL) + c[first:]
old_n = int(re.search(r'<span class="bpa-pill">1 / (\d+)</span>', c).group(1))
n = old_n + len(GAL)
c = c.replace(f'<span class="bpa-pill">1 / {old_n}</span>', f'<span class="bpa-pill">1 / {n}</span>', 1)
ta = c.index('<div class="cd-thumbs"'); tb = c.index("</div>", ta)
btns = re.findall(r'<button type="button" class="cd-thumb[^"]*"[^>]*>(<img[^>]*>)</button>', c[ta:tb])
assert len(btns) == old_n, (len(btns), old_n)
imgs = btns[:1] + [f'<img src="{P}{k}-t240.webp" alt="" loading="lazy" decoding="async" width="80" height="60">' for k in GAL] + btns[1:]
VIS = 5
out = []
for x, im in enumerate(imgs):
    cls = "cd-thumb" + (" is-on" if x == 0 else "") + (" is-hid" if x >= VIS else "")
    more = f' data-more="+{n - VIS + 1}"' if x == VIS - 1 else ""
    out.append(f'<button type="button" class="{cls}" data-i="{x}"{more} aria-label="Show photo {x + 1} of {n}">{im}</button>')
c = c[:ta] + '<div class="cd-thumbs" aria-label="Photo thumbnails">' + "".join(out) + c[tb:]

# (1) Food row: 4 plates under the course line
PICS = [("scallop", "starter", "Starter"), ("goose-liver", "starter", "Starter"), ("duck-breast", "main", "Main"), ("panna-cotta", "dessert", "Dessert")]
k = c.index('<div class="dc-dna">')
c = c[:k] + '<div class="dc-pics">' + "".join(
    f'<button type="button" class="dc-pic" data-sec="{sec}" aria-label="{CAP[d]}"><img src="{P}{d}-sq.webp" alt="{CAP[d]}" width="64" height="64" loading="lazy"/><span>{lab}</span></button>'
    for d, sec, lab in PICS) + '<button type="button" class="dc-pic dc-pic-more" data-sec="starter" aria-label="See all dishes with photos"><b>+10</b><span>dishes</span></button></div>' + c[k:]
s = s[:ci] + c + s[cj:]

# (4) full menu: photo next to each dish that has one (both Legenda menus)
MENU = {"Great scallop": "scallop", "Cold goose liver": "goose-liver", "Goat cheese mousse": "goat-cheese-mousse",
        "Beef tartare": "beef-tartare", "Chicken breast, strawberry": "chicken-brie-salad", "Roasted trout": "trout",
        "Pork shoulder": "pork-shoulder", "Rosemary duck breast": "duck-breast", "Beef confit": "beef-confit",
        "Cauliflower steak": "cauliflower-steak", "Seared red tuna": "tuna-steak", "Panna cotta": "panna-cotta",
        "Cheesecake, poppy": "cheesecake", "“Sweet dream”": "chocolate-cake"}
def addpics(block):
    for start, key in MENU.items():
        pat = re.compile(r'(<div class="dish" data-diet="[^"]*">)(' + re.escape(start) + ")")
        block, m = pat.subn(lambda mm: f'{mm.group(1)}<img class="dc-dish-img" src="{P}{key}-sq.webp" alt="" width="52" height="52" loading="lazy"/>{mm.group(2)}', block)
        assert m == 1, (start, m)
    return block.replace('<div class="dc-carte on" data-', '<div class="dc-carte on dc-has-pics" data-', 1)
for marker in ('id="dc-menu-legenda"', '<span class="ltt-bento-group-title">🍽️ Gourmet Dinner Menu'):
    a = s.index(marker); a = s.index('<div class="dc-carte on"', a); b = s.index('<div class="foot">', a)
    s = s[:a] + addpics(s[a:b]) + s[b:]

CSS = """<style id="legenda-menu-photos-test">
.dc-pics{display:flex;gap:8px;margin-top:8px;overflow-x:auto;scrollbar-width:none}
.dc-pics::-webkit-scrollbar{display:none}
.dc-pic{flex:0 0 64px;border:0;background:none;padding:0;cursor:pointer;text-align:center;font:inherit}
.dc-pic img{display:block;width:64px;height:64px;border-radius:10px;object-fit:cover;border:1px solid #eadfca;background:#fff}
.dc-pic span{display:block;font-size:11px;color:#6b645c;margin-top:3px;letter-spacing:.02em}
.dc-pic:hover img{border-color:#b88214}
.dc-pic:hover span{color:#92400e}
.dc-pic-more b{display:flex;align-items:center;justify-content:center;width:64px;height:64px;border-radius:10px;border:1px dashed #d9c79e;background:#fdf3d8;color:#92400e;font-size:15px}
.dc-carte .dish .dc-dish-img{display:block;width:52px;height:52px;border-radius:50%;object-fit:cover;margin:10px auto 4px;border:1px solid #eadfca;background:#fff;cursor:zoom-in;transition:transform .2s}
.dc-carte .dish .dc-dish-img.big{width:min(300px,100%);height:auto;border-radius:10px;cursor:zoom-out}
.dc-wall .dc-carte .dish .dc-dish-img{width:40px;height:40px}
</style>"""
JS = """<script>
document.addEventListener('click',function(e){
 var p=e.target.closest('.dc-pic');if(p){var f=p.closest('.dc-food'),b=f&&f.querySelector('.dc-dna .dc-c[data-sec="'+p.dataset.sec+'"]');if(b)b.click();return;}
 var i=e.target.closest('.dc-dish-img');if(i){e.preventDefault();e.stopPropagation();i.classList.toggle('big');}
},true);
</script>"""
s = s.replace("</head>", CSS + "</head>", 1).replace("</body>", JS + "</body>", 1)

open(OUT, "w", encoding="utf-8").write(s)
print("slides", total, "| card gallery", n)
