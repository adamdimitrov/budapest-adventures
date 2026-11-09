import re

with open("/Users/adamdimitrov/Development/budapest-adventures/river.html") as f:
    r_html = f.read()

sliders = re.findall(r"<div[^>]*class=\"[^\"]*slider-2[^\"]*\"[^>]*>(.*?)</div>\s*</div>\s*</div>", r_html, re.DOTALL)
cruises_imgs = []
for s in sliders:
    imgs = re.findall(r"<img[^>]*src=\"([^\"]+)\"", s)
    cruises_imgs.append(imgs)

BPA_CDN = "/assets/cdn/60e43c7d6d05b671dff0dc1a/"
cleaned_imgs = []
for group in cruises_imgs:
    grp_cleaned = []
    for u in group:
        if u.startswith(BPA_CDN):
            grp_cleaned.append(u[len(BPA_CDN):])
        else:
            grp_cleaned.append(u)
    cleaned_imgs.append(grp_cleaned)

with open("/Users/adamdimitrov/Development/budapest-adventures/build_river_deck.py") as f:
    brd = f.read()

start_cruises = brd.find("cruises = [")
end_cruises = brd.find("\n]\n", start_cruises) + 3
cruises_data = eval(brd[start_cruises:end_cruises].split("=", 1)[1])

cards = []
for i, c in enumerate(cruises_data):
    imgs = cleaned_imgs[i]
    hero = imgs[0]
    more = ",".join(imgs[1:])
    tot = len(imgs)
    
    badge_cls = c["badge_cls"]
    badge_txt = c["badge"]
    badge_html = f'<span class="bpa-rank-tag {badge_cls}">{badge_txt}</span>'
    
    chan_html = ""
    for ch, score, revs in c["channels"]:
        chan_html += f'<div class="bpa-channel-item"><i class="bpa-ic-{ch}" title="{ch.upper()}"></i><strong>{score}</strong><span>{revs}</span></div>'
        
    specs_html = "".join([f'<span class="bpa-spec-pill">{sp}</span>' for sp in c["specs"]])
    
    hero_url = hero if hero.startswith("http") else (BPA_CDN + hero)
    title = c["title"]
    kicker = c["kicker"]
    url = c["url"]
    stars = c["stars"]
    score = c["score"]
    reviews = c["reviews"]
    best_for = c["best_for"]
    price = c["price"]
    price_sub = c["price_sub"]
    anchor = c["anchor"]
    
    card = f"""<div class="bpa-card"><div class="bpa-main"><div class="bpa-media">{badge_html}<button type="button" class="bpa-nav-arrow prev" onclick="bpaSlide(this,-1)">‹</button><button type="button" class="bpa-nav-arrow next" onclick="bpaSlide(this,1)">›</button><span class="bpa-counter-pill">1 / {tot}</span><div class="bpa-slider" data-more="{more}" onscroll="bpaCount(this)"><img src="{hero_url}" alt="{title}"></div></div><div class="bpa-info"><div class="bpa-kicker">{kicker}</div><a href="{url}" target="_blank" rel="sponsored noopener" class="bpa-headline">{title}</a><div class="bpa-proof-bar"><span class="bpa-gold-stars">{stars}</span><span class="bpa-score-text">{score}</span><span class="bpa-count-muted">{reviews}</span><span class="bpa-verified-chip">✓ Verified</span></div><div class="bpa-channels">{chan_html}</div><div class="bpa-specs-row">{specs_html}</div><div class="bpa-best-for">🎯 <strong>Best For:</strong> {best_for}</div></div><div class="bpa-cta-cell"><div><div class="bpa-price-num">{price}</div><div class="bpa-price-sub">{price_sub}</div></div><a href="{url}" target="_blank" rel="sponsored noopener" class="bpa-book-button">Book Now →</a><a href="{anchor}" class="bpa-sublink">Read Full Review ↓</a></div></div></div>"""
    cards.append(card)

deck_html = f"""<div class="bpa-deck-wrap"><div class="bpa-section-header"><h2 class="bpa-section-title">Comparison — 10 Best Boat Tours &amp; River Cruises in Budapest (2026)</h2><p class="bpa-section-sub">Personally field-tested on the Danube • Verified prices, dock locations &amp; real photos</p></div>{"".join(cards)}</div><aside class="sticky-mobile-bar" id="sticky-bar" aria-label="Current Cruise Quick Reservation"><div class="sticky-inner"><div class="sticky-boat-info"><img id="sticky-thumb" src="{BPA_CDN}68f3738fe72bf6e25526e991_best-budapest-river-cruises-legenda-sightseeing-cruise-00025.avif" alt="Budapest Cruise" class="sticky-thumb-img"><div class="sticky-text"><div class="sticky-title-row"><span id="sticky-rank" class="sticky-rank-badge">🏆 #1 Best Overall</span><strong id="sticky-name">Legenda City Cruises</strong></div><div class="sticky-meta-row"><span id="sticky-price" class="sticky-price-tag">€20–25</span><span class="sticky-bullet">•</span><span id="sticky-desc" class="sticky-desc-text">Dock 7 • Welcome Drink Included</span></div></div></div><a id="sticky-cta-btn" href="https://legenda.hu/en?partner=38585" target="_blank" rel="sponsored noopener" class="btn-sticky-cta">Book Tickets →</a></div></aside>"""

with open("/Users/adamdimitrov/Development/budapest-adventures/build_final_deck.py") as f:
    bf = f.read()

s_css = bf.find("css = \"\"\"") + len("css = \"\"\"")
e_css = bf.find("\"\"\"", s_css)
css = bf[s_css:e_css]

s_js = bf.find("js = \"\"\"") + len("js = \"\"\"")
e_js = bf.find("\"\"\"", s_js)
js = bf[s_js:e_js]

full = css + deck_html + js
print("Full length with all 62 photos:", len(full))

# Minify CSS slightly if over 50,000 characters
min_css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
min_css = re.sub(r'\s+', ' ', min_css)
min_css = re.sub(r'\s*([\{\}\:\;\,])\s*', r'\1', min_css)

min_js = re.sub(r'//.*?\n', '', js)
min_js = re.sub(r'\s+', ' ', min_js)

full_min = min_css + deck_html + min_js
print("Minified full length:", len(full_min))

with open("/Users/adamdimitrov/Development/budapest-adventures/comparison_deck_10_river_cruises.html", "w") as out:
    out.write(full_min)

print("Saved comparison_deck_10_river_cruises.html successfully! Fits in 50k limit:", len(full_min) <= 50000)
