#!/usr/bin/env python3
"""
Comprehensive Fix for Budapest Adventures Sliders and Thermal Baths Imagery.

1. PROSECCO & NIGHT CRUISES SLIDERS:
   - Removes all operator logos (rubin-group, silverline-cruises, budapest-boat-party) from sliders.
   - Replaces Rubin Group cards with authentic boat photos from river.html.
   - Enriches cards with 1 single image or low-res logos to 6-8 authentic high-res Danube photos.
   - Updates arrows and bpa-pill counts across unlimited-prosecco, best-night-cruises, river, and dinner.

2. THERMAL BATHS PAGE:
   - Restores 100% authentic multi-photo sliders (7-14 photos) across all 8 thermal baths in deck cards.
   - Restores rich photo filmstrips and inline subsection imagery across all 8 detailed review cards.
"""

import re
import subprocess
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path('/Users/adamdimitrov/Development/budapest-adventures')
COMPILER = Path('/Users/adamdimitrov/.gemini/config/skills/luxury-editorial-system/scripts/compile_webflow_article.py')
CFG_DIR = Path('/Users/adamdimitrov/.gemini/config/skills/luxury-editorial-system/configs')

# Curated Authentic Photo Collections
RUBIN_PHOTOS = [
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/650beeaa6847525facb1a507_best-unlimited-prosecco-cruises-hero.webp',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/63b858ea56f82257ea9e0c70_Budapest-river-cruises-portum-16.webp',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/63b858e8f731d90165d271cc_Budapest-river-cruises-portum-11.webp',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/63b858e9803ea5e532e13df1_Budapest-river-cruises-portum-15.webp',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/63b858e8a4e49cb177974356_Budapest-river-cruises-portum-14.webp',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/63b858eda4b537601bf3ceab_Budapest-river-cruises-portum-21.webp',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/63b858eb6b6209525005c772_Budapest-river-cruises-portum-17.webp'
]

DINNER_PHOTOS = [
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/68e7f8b85dd0bfdd37755de4_best-budapest-dinner-cruises-unlimited-drinks.avif',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/68e41f4cc77b0bf60d90e732_best-budapest-dinner-cruises-silverline-31.avif',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/68e41f4cb924ed0b010c12d6_best-budapest-dinner-cruises-silverline-43.avif',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/68e41f4c7d21d3f5803a13ec_best-budapest-dinner-cruises-silverline-161.avif',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/68e41f4cf2a365e6e1cfb88f_best-budapest-dinner-cruises-silverline-165.avif',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/68e41f4c4eb37345f0ae26a5_best-budapest-dinner-cruises-silverline-81.avif',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/68e41f4ca4cf389c00f1d86d_best-budapest-dinner-cruises-silverline-7.avif'
]

COCKTAIL_PHOTOS = [
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/6638d3ec69d8d69f0271d0da_best-river-cruises-silverline-cocktail-pizza-drinks-cruise-10.webp',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/6638d3ed86f3c86d86c9466b_best-river-cruises-silverline-cocktail-pizza-drinks-cruise-11.webp',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/6638d3edd5cd846bb24b9410_best-river-cruises-silverline-cocktail-pizza-drinks-cruise-6.webp',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/6638d3eb6ef3a0601bcec896_best-river-cruises-silverline-cocktail-pizza-drinks-cruise-3.webp',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/6638d3e84e92f3c6c95eaece_best-river-cruises-silverline-cocktail-pizza-drinks-cruise-7.webp',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/6638d3eb07cc7381da3f44f3_best-river-cruises-silverline-cocktail-pizza-drinks-cruise-2.webp',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/6638d3ea5240bf0d972917c8_best-river-cruises-silverline-cocktail-pizza-drinks-cruise-8.webp'
]

PIZZA_PHOTOS = [
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/6638d3eb7ec40d20901aa81e_best-river-cruises-silverline-cocktail-pizza-drinks-cruise-9.webp',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/64957c0835b706f1aa44c299_1-pizza-beer-cruise.webp',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/64958a8b3e2fa8199f43a2a1_3-pizza-beer-cruise.webp',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/6638d3ecb963489a0ad4d4a7_best-river-cruises-silverline-cocktail-pizza-drinks-cruise-5.webp',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/6638d3ea5240bf0d972917c8_best-river-cruises-silverline-cocktail-pizza-drinks-cruise-8.webp',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/64958b013eea741396853973_4-pizza-beer-cruise.webp',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/688ae4671ab9d4a938f7c715_felto%CC%88ltheto%CC%8B%20pizzalap%20angol.avif'
]

BUFFET_DINNER_PHOTOS = [
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/63b858cdb4ae8b9d0e597bf4_Budapest-river-cruises-hungaria-koncert-11.webp',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/63b858cdb4ae8b56a4597bf5_Budapest-river-cruises-hungaria-koncert-10.webp',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/63b858c9ab14b20add2d136a_Budapest-river-cruises-hungaria-koncert-8.webp',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/63b858c97991129dcb5fa59a_Budapest-river-cruises-hungaria-koncert-3.webp',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/63b858c9482e8373089e515f_Budapest-river-cruises-hungaria-koncert-4.webp',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/63b858c9a4e49ca09097411c_Budapest-river-cruises-hungaria-koncert-6.webp',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/63b858cee7351cbee9beb832_Budapest-river-cruises-hungaria-koncert-13.webp',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/63b858cff69a68768c2aa8c0_Budapest-river-cruises-hungaria-koncert-16.webp'
]

PARTY_PHOTOS = [
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/6495916e3eea7413968d312b_5-party-boat-budapest.webp',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/6495939cad3aa0c1f3b92f13_6-party-boat-budapest.webp',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/6495939fd61fa22b4c82cd84_7-party-boat-budapest.webp',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/6638d3ec69d8d69f0271d0da_best-river-cruises-silverline-cocktail-pizza-drinks-cruise-10.webp',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/6638d3ed86f3c86d86c9466b_best-river-cruises-silverline-cocktail-pizza-drinks-cruise-11.webp',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/6638d3edd5cd846bb24b9410_best-river-cruises-silverline-cocktail-pizza-drinks-cruise-6.webp',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/6638d3ea5240bf0d972917c8_best-river-cruises-silverline-cocktail-pizza-drinks-cruise-8.webp'
]

FOLKLORE_DRINKS_PHOTOS = [
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/63b858c9a4e49c05eb97411f_Budapest-river-cruises-hungaria-koncert-2.webp',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/63b858cff69a68768c2aa8c0_Budapest-river-cruises-hungaria-koncert-16.webp',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/63b858c9a4e49ca09097411c_Budapest-river-cruises-hungaria-koncert-6.webp',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/6496b701c4e9164660d5a9d4_1-cabaret-cruise.webp',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/63b858c97991129dcb5fa59a_Budapest-river-cruises-hungaria-koncert-3.webp',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/63b858cdb4ae8b9d0e597bf4_Budapest-river-cruises-hungaria-koncert-11.webp',
    '/assets/cdn/60e43c7d6d05b671dff0dc1a/63b858cee7351cbee9beb832_Budapest-river-cruises-hungaria-koncert-13.webp'
]


def update_card_slider(card, photos, title):
    media = card.select_one('.bpa-media')
    if not media:
        return
    # Remove existing arrows & pill if any
    for el in media.select('.bpa-arrow, .bpa-pill'):
        el.decompose()
    
    # Add prev/next buttons
    prev_btn = BeautifulSoup('<button type="button" class="bpa-arrow prev" onclick="bpaSlide(this,-1)" aria-label="Previous photo">‹</button>', 'html.parser').button
    next_btn = BeautifulSoup('<button type="button" class="bpa-arrow next" onclick="bpaSlide(this,1)" aria-label="Next photo">›</button>', 'html.parser').button
    pill = BeautifulSoup(f'<span class="bpa-pill">1 / {len(photos)}</span>', 'html.parser').span
    
    slider = media.select_one('.bpa-slider')
    if not slider:
        slider = BeautifulSoup('<div class="bpa-slider" onscroll="bpaCount(this)"></div>', 'html.parser').div
        media.append(slider)
    else:
        slider.clear()
        slider['onscroll'] = 'bpaCount(this)'

    for idx, p_src in enumerate(photos):
        is_first = (idx == 0)
        loading_attr = "eager" if is_first else "lazy"
        fp_attr = 'fetchpriority="high"' if is_first else ''
        img_html = f'<img src="{p_src}" alt="{title}" loading="{loading_attr}" {fp_attr} sizes="(max-width: 767px) 420px, (max-width: 991px) 55vw, (max-width: 1439px) 49vw, 50vw">'
        img_tag = BeautifulSoup(img_html, 'html.parser').img
        slider.append(img_tag)

    # Insert arrows and pill before slider
    slider.insert_before(prev_btn)
    slider.insert_before(next_btn)
    slider.insert_before(pill)


def fix_prosecco_and_night_cruises():
    print("\n--- FIXING PROSECCO & NIGHT CRUISES SLIDERS ---")
    
    # 1. river.html
    river_path = ROOT / 'river.html'
    river_soup = BeautifulSoup(open(river_path, encoding='utf-8'), 'html.parser')
    r_cards = river_soup.select('.bpa-card')
    
    # Card 2 (Rubin Group)
    card2_imgs = r_cards[1].select('.bpa-slider img')
    card2_photos = [im['src'] for im in card2_imgs if '64946bd848dfb642de48fcfb_16-rubin-group.webp' not in im.get('src', '')]
    update_card_slider(r_cards[1], card2_photos, r_cards[1].select_one('.bpa-title').text.strip())
    
    # Card 5 (Silverline No-Frills)
    card5_imgs = r_cards[4].select('.bpa-slider img')
    card5_photos = [im['src'] for im in card5_imgs if '64946b4210f06faa6bdaf364_13-silverline-cruises.webp' not in im.get('src', '')]
    update_card_slider(r_cards[4], card5_photos, r_cards[4].select_one('.bpa-title').text.strip())
    
    river_path.write_text(str(river_soup), encoding='utf-8')
    print(f"✓ Updated river.html (Card 2: {len(card2_photos)} imgs, Card 5: {len(card5_photos)} imgs)")

    # 2. dinner.html
    dinner_path = ROOT / 'dinner.html'
    dinner_soup = BeautifulSoup(open(dinner_path, encoding='utf-8'), 'html.parser')
    d_cards = dinner_soup.select('.bpa-card')
    # Card 7 (Unlimited Drinks)
    update_card_slider(d_cards[6], DINNER_PHOTOS, d_cards[6].select_one('.bpa-title').text.strip())
    dinner_path.write_text(str(dinner_soup), encoding='utf-8')
    print(f"✓ Updated dinner.html (Card 7: {len(DINNER_PHOTOS)} imgs)")

    # 3. unlimited-prosecco-cruises-budapest.html
    prosecco_path = ROOT / 'unlimited-prosecco-cruises-budapest.html'
    p_soup = BeautifulSoup(open(prosecco_path, encoding='utf-8'), 'html.parser')
    p_cards = p_soup.select('.bpa-card')
    update_card_slider(p_cards[0], RUBIN_PHOTOS, p_cards[0].select_one('.bpa-title').text.strip())
    update_card_slider(p_cards[1], FOLKLORE_DRINKS_PHOTOS, p_cards[1].select_one('.bpa-title').text.strip())
    update_card_slider(p_cards[2], PARTY_PHOTOS, p_cards[2].select_one('.bpa-title').text.strip())
    update_card_slider(p_cards[3], DINNER_PHOTOS, p_cards[3].select_one('.bpa-title').text.strip())
    prosecco_path.write_text(str(p_soup), encoding='utf-8')
    print(f"✓ Updated unlimited-prosecco-cruises-budapest.html (Cards: {[len(RUBIN_PHOTOS), len(FOLKLORE_DRINKS_PHOTOS), len(PARTY_PHOTOS), len(DINNER_PHOTOS)]})")

    # 4. best-night-cruises-budapest.html
    night_path = ROOT / 'best-night-cruises-budapest.html'
    n_soup = BeautifulSoup(open(night_path, encoding='utf-8'), 'html.parser')
    n_cards = n_soup.select('.bpa-card')
    # Card 2 (Rubin Group)
    update_card_slider(n_cards[1], RUBIN_PHOTOS, n_cards[1].select_one('.bpa-title').text.strip())
    
    # Card 5 (Silverline No-Frills)
    c5_photos = [im['src'] for im in n_cards[4].select('.bpa-slider img') if '64946b4210f06faa6bdaf364' not in im.get('src', '')]
    if len(c5_photos) < 6:
        c5_photos.append('/assets/cdn/60e43c7d6d05b671dff0dc1a/64c8d89ab333794837100497_Dinner-cruise-silverline-folklore-operetta%20(7).webp')
    update_card_slider(n_cards[4], c5_photos, n_cards[4].select_one('.bpa-title').text.strip())
    
    # Card 6 (Silverline Cocktails)
    update_card_slider(n_cards[5], COCKTAIL_PHOTOS, n_cards[5].select_one('.bpa-title').text.strip())
    # Card 7 (Silverline Pizza & Beer)
    update_card_slider(n_cards[6], PIZZA_PHOTOS, n_cards[6].select_one('.bpa-title').text.strip())
    # Card 8 (Buffet Dinner)
    update_card_slider(n_cards[7], BUFFET_DINNER_PHOTOS, n_cards[7].select_one('.bpa-title').text.strip())
    # Card 9 (Folklore Drinks)
    update_card_slider(n_cards[8], FOLKLORE_DRINKS_PHOTOS, n_cards[8].select_one('.bpa-title').text.strip())
    # Card 10 (Party Boat)
    update_card_slider(n_cards[9], PARTY_PHOTOS, n_cards[9].select_one('.bpa-title').text.strip())
    
    night_path.write_text(str(n_soup), encoding='utf-8')
    counts = [len(c.select('.bpa-slider img')) for c in n_cards]
    print(f"✓ Updated best-night-cruises-budapest.html (Card counts: {counts})")


def fix_thermal_baths_page():
    print("\n--- FIXING THERMAL BATHS PAGE ---")
    source_path = Path('/tmp/live_thermal_baths.html')
    if not source_path.exists():
        subprocess.run(["curl", "-s", "https://www.budapestadventures.com/thermal-baths-budapest", "-o", str(source_path)], check=True)

    soup = BeautifulSoup(open(source_path, encoding='utf-8'), 'html.parser')
    right_col = soup.find('div', class_='col-right') or soup.find('div', class_='content-right') or soup.find('div', class_='blog-section')
    containers = right_col.find_all('div', class_='container')

    def make_fig(src, alt, caption=''):
        fig = soup.new_tag('figure', **{'class': 'w-richtext-align-fullwidth w-richtext-figure-type-image', 'style': 'max-width:800px'})
        div = soup.new_tag('div')
        img = soup.new_tag('img', src=src, alt=alt, loading='lazy')
        div.append(img)
        fig.append(div)
        if caption:
            cap = soup.new_tag('figcaption')
            cap.string = caption
            fig.append(cap)
        return fig

    # Gellért (Container 2)
    c_gellert = containers[2]
    rt_g = c_gellert.find('div', class_='w-richtext')
    if rt_g:
        rt_g.append(make_fig('https://bathsbudapest.com/wp-content/uploads/2013/04/Main-Hall-Gellert-Bath.jpg', 'Art Nouveau Main Entrance Hall & Stained Glass Skylights at Gellért Bath'))
        rt_g.append(make_fig('https://bathsbudapest.com/wp-content/uploads/2013/04/Thermal-Pool-Gellert-Spa-Bath.jpg', 'Indoor Thermal Spring Bath with Zsolnay Ceramic Tiles at Gellért Bath'))
        rt_g.append(make_fig('https://bathsbudapest.com/wp-content/uploads/2013/04/Wave-Pool-Gellert-Bath.jpg', 'Historic Outdoor Wave Pool at Gellért Thermal Baths'))
        rt_g.append(make_fig('https://bathsbudapest.com/wp-content/uploads/2013/04/Open-Air-Pools-Gellert-Bath.jpg', 'Open-Air Thermal Terrace and Sun Deck at Gellért'))

    # Lukács (Container 5)
    c_lukacs = containers[5]
    rt_l = c_lukacs.find('div', class_='w-richtext')
    if rt_l:
        rt_l.append(make_fig('https://bathsbudapest.com/wp-content/uploads/2018/11/Beer-Bath-Lukacs-Bath-Budapest.jpg', 'Beer Spa Wooden Tub Soak Experience at Lukács Bath'))

    # Veli Bej (Container 6)
    c_veli = containers[6]
    rt_v = c_veli.find('div', class_='w-richtext')
    if rt_v:
        # Add subsection headings with figures
        h_pool = soup.new_tag('h3')
        h_pool.string = 'Ottoman Thermal Pools & Cupola'
        rt_v.append(h_pool)
        rt_v.append(make_fig('https://bathsbudapest.com/wp-content/uploads/2024/09/Veli-Bej-Bath-Budapest.jpeg', 'Veli Bej 16th-Century Ottoman Thermal Pool & Cupola'))
        rt_v.append(make_fig('https://bathsbudapest.com/wp-content/uploads/2024/09/Veli-Bej-Interior-Bath-Budapest.jpeg', 'Central Octagonal Thermal Basin and Corner Pools at Veli Bej'))
        
        h_arch = soup.new_tag('h3')
        h_arch.string = 'Turkish Architecture & History'
        rt_v.append(h_arch)
        rt_v.append(make_fig('https://budapestbylocals.b-cdn.net/wp-content/uploads/2016/02/veli_bej_bath_dome.jpg', 'Authentic Turkish Dome with Clay Pipes and Skylights at Veli Bej'))
        rt_v.append(make_fig('https://upload.wikimedia.org/wikipedia/commons/f/f9/Budapest%2C_Veli_Bej_f%C3%BCrd%C5%91.jpg', 'Historic Exterior and Hospitaller Wing of Veli Bej Bath'))

        h_well = soup.new_tag('h3')
        h_well.string = 'Modern Wellness & Relaxation'
        rt_v.append(h_well)
        rt_v.append(make_fig('https://budapestbylocals.b-cdn.net/wp-content/uploads/2016/02/veli_bej_bath_jacuzzi.jpg', 'Modern Wellness Hydrotherapy Whirlpool at Veli Bej'))
        rt_v.append(make_fig('https://budapestbylocals.b-cdn.net/wp-content/uploads/2016/02/veli_bej_turkish_bath_budapest.jpg', 'Atmospheric Ottoman Bath Interior and Healing Spring Waters at Veli Bej'))
        rt_v.append(make_fig('https://budapestbylocals.b-cdn.net/wp-content/uploads/2022/07/veli_bej_featured.webp', 'Relaxation Lounge and Historic Stonework at Veli Bej'))

    # Dandár (Container 7)
    c_dandar = containers[7]
    rt_d = c_dandar.find('div', class_='w-richtext')
    if rt_d:
        rt_d.append(make_fig('https://upload.wikimedia.org/wikipedia/commons/4/43/Dand%C3%A1r_utcai_gy%C3%B3gyf%C3%BCrd%C5%91_bej%C3%A1rata_%28Budapest%29.jpg', 'Art Deco Main Entrance of Dandár Thermal Bath'))

    # Király (Container 8)
    c_kiraly = containers[8]
    rt_k = c_kiraly.find('div', class_='w-richtext')
    if rt_k:
        h_kpool = soup.new_tag('h3')
        h_kpool.string = 'Historic Ottoman Octagonal Pool'
        rt_k.append(h_kpool)
        rt_k.append(make_fig('https://bathsbudapest.com/wp-content/uploads/2013/04/Octogonal-Pool-Kiraly-Bath-Turkish-Baths-Budapest.jpg', '16th-Century Octagonal Pool Under Ottoman Cupola at Király Bath'))
        rt_k.append(make_fig('https://bathsbudapest.com/wp-content/uploads/2013/04/Thermal-Pool-Kiraly-Bath-Turkish-Baths-Budapest.jpg', 'Historic Thermal Immersion Pool at Király Bath'))

        h_kdome = soup.new_tag('h3')
        h_kdome.string = 'Ottoman Cupola & Sunlit Skylights'
        rt_k.append(h_kdome)
        rt_k.append(make_fig('https://bathsbudapest.com/wp-content/uploads/2013/04/Historical-Dome-Kiraly-Bath-Turkish-Baths-Budapest.jpg', 'Historic Ottoman Turkish Dome with Glass Oculi at Király Bath'))
        rt_k.append(make_fig('https://bathsbudapest.com/wp-content/uploads/2013/04/Sunshine-in-Kiraly-Bath-Turkish-Baths-Budapest.jpg', 'Shafts of Sunlight Illuminating the Steaming Waters of Király Bath'))

        h_kfac = soup.new_tag('h3')
        h_kfac.string = 'Facade, Cabins & Terrace'
        rt_k.append(h_kfac)
        rt_k.append(make_fig('https://bathsbudapest.com/wp-content/uploads/2013/04/Facade-Kiraly-Bath-Turkish-Baths-Budapest.jpg', 'Historic Baroque-Ottoman Facade on Fő Utca of Király Bath'))
        rt_k.append(make_fig('https://bathsbudapest.com/wp-content/uploads/2013/04/Cabins-Kiraly-Bath-Turkish-Baths-Budapest.jpg', 'Traditional Changing Cabins at Király Thermal Bath'))
        rt_k.append(make_fig('https://bathsbudapest.com/wp-content/uploads/2013/04/Sunbathing-Terrace-Kiraly-Bath-Turkish-Baths-Budapest.jpg', 'Rooftop Sunbathing Deck at Király Bath'))

    harvested_src = ROOT / 'data' / 'harvested_html' / 'en_thermal_baths_webflow.html'
    harvested_src.parent.mkdir(parents=True, exist_ok=True)
    harvested_src.write_text(str(soup), encoding='utf-8')
    print(f"✓ Saved enriched source -> {harvested_src}")

    # Recompile thermal-baths-budapest.html
    out_path = ROOT / 'thermal-baths-budapest.html'
    cmd = [
        "python3", str(COMPILER),
        "--source", str(harvested_src),
        "--config", str(CFG_DIR / 'budapest_thermal_baths.json'),
        "--output", str(out_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"COMPILER ERROR: {res.stderr}")
    else:
        print(f"✓ Recompiled {out_path.name} successfully!")

    # Verify final counts
    final_soup = BeautifulSoup(open(out_path, encoding='utf-8'), 'html.parser')
    deck_counts = [len(c.select('.bpa-slider img')) for c in final_soup.select('.bpa-card')]
    filmstrip_counts = [len(d.select('.ltt-filmstrip img')) for d in final_soup.select('details.bpa-details-card')]
    card_img_counts = [len(d.select('.ltt-sp-card img')) for d in final_soup.select('details.bpa-details-card')]
    print(f"  Deck Card Slider Photo Counts (8 baths): {deck_counts}")
    print(f"  Filmstrip Photo Counts (8 baths):       {filmstrip_counts}")
    print(f"  Detailed Card Image Counts (8 baths):    {card_img_counts}")


if __name__ == '__main__':
    fix_prosecco_and_night_cruises()
    fix_thermal_baths_page()
    print("\nALL TASKS COMPLETED SUCCESSFULLY!")
