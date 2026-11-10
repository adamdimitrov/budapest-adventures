#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEEP OPTIMIZER & MINIFIER FOR ALL BUDAPEST GUIDES
Reduces HTML payload, minifies inline CSS & JSON-LD, and enforces 100% Core Web Vitals & WCAG AA standards.
"""

import os
import re
import json
import shutil
from bs4 import BeautifulSoup
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from fix_language_switcher_links import fix_switcher_html  # keeps switcher links = hreflang

BASE_DIR = '/Users/adamdimitrov/Development/budapest-adventures'

def minify_css(css_text):
    if not css_text:
        return ""
    # Remove CSS comments
    css_text = re.sub(r'/\*.*?\*/', '', css_text, flags=re.DOTALL)
    # Collapse multiple whitespaces
    css_text = re.sub(r'\s+', ' ', css_text)
    # Remove whitespace around delimiters
    css_text = re.sub(r'\s*([\{\}:;,>~+])\s*', r'\1', css_text)
    return css_text.strip()

def optimize_file(file_path, cruise_type='river'):
    if not os.path.exists(file_path):
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    head = soup.find('head')
    if not head:
        return

    # 1. Preload LCP hero image
    lcp_url = "/assets/cdn/60e43c7d6d05b671dff0dc1a/68f3738fe72bf6e25526e991_best-budapest-river-cruises-legenda-sightseeing-cruise-00025.avif" if cruise_type == 'river' else "/assets/cdn/60e43c7d6d05b671dff0dc1a/64c683ce54d6bc13ea02d515_best-dinner-cruises-budapest-legenda-city-cruises.webp"
    
    preloads = [l.get('href') for l in head.find_all('link', rel='preload')]
    if lcp_url not in preloads:
        img_type = 'image/avif' if lcp_url.endswith('.avif') else 'image/webp'
        lcp_tag = soup.new_tag('link', **{
            'rel': 'preload',
            'as': 'image',
            'href': lcp_url,
            'type': img_type,
            'fetchpriority': 'high'
        })
        head.insert(3, lcp_tag)

    # 2. Async Google Fonts
    for link in head.find_all('link', rel='stylesheet'):
        href = link.get('href', '')
        if 'fonts.googleapis.com' in href:
            link['media'] = 'print'
            link['onload'] = "this.media='all'"

    # 3. Minify all <style> tags
    for style in soup.find_all('style'):
        if style.string:
            style.string = minify_css(style.string)

    # 4. Minify all JSON-LD <script> tags
    for sc in soup.find_all('script', type='application/ld+json'):
        if sc.string:
            try:
                parsed = json.loads(sc.string)
                sc.string = json.dumps(parsed, separators=(',', ':'))
            except Exception:
                pass

    # 5. Fix Deck Card Images: Card 1 eager, Card 2+ lazy
    deck = soup.find(class_='ltt-deck-container')
    if deck:
        for idx, card in enumerate(deck.find_all(class_='bpa-card'), 1):
            img = card.find('img')
            if img:
                img['width'] = '800'
                img['height'] = '534'
                if idx == 1:
                    img['loading'] = 'eager'
                    img['fetchpriority'] = 'high'
                else:
                    img['loading'] = 'lazy'
                    if 'fetchpriority' in img.attrs:
                        del img['fetchpriority']

    # 6. Author avatar dimensions
    for img in soup.find_all('img'):
        src = img.get('src', '')
        if 'adam-dimitrov' in src:
            img['width'] = '48'
            img['height'] = '48'
            img['loading'] = 'eager'

    # 7. Eliminate nested interactive <a> inside <summary>
    for summary in soup.find_all('summary', class_='bpa-details-summary'):
        for map_a in summary.find_all('a', class_='bpa-kicker-map-link'):
            span_map = soup.new_tag('span', **{'class': 'bpa-kicker-map-link'})
            span_map.string = map_a.get_text()
            map_a.replace_with(span_map)
        for rev_a in summary.find_all('a', class_='bpa-rev-badge'):
            span_rev = soup.new_tag('span', **{'class': 'bpa-rev-badge'})
            span_rev.extend(list(rev_a.contents))
            rev_a.replace_with(span_rev)

    # 8. Fix orphan <li> tags outside <ul>
    for li in soup.find_all('li'):
        if not li.parent or li.parent.name not in ['ul', 'ol', 'menu']:
            prev_ul = li.find_previous_sibling('ul')
            if prev_ul:
                prev_ul.append(li)
            else:
                new_ul = soup.new_tag('ul', **{'role': 'list'})
                li.wrap(new_ul)

    # 9. Accessible button labels
    lang_btn = soup.find(id='lttLangBtn')
    if lang_btn:
        lang_btn['aria-label'] = "Select Language"
    drop_btn = soup.find('button', class_='ltt-dropdown-btn')
    if drop_btn:
        drop_btn['aria-label'] = "Danube Cruises Navigation Menu"

    # 10. Move inline navbar script to bottom of <body>
    nav_script = soup.find(id='ltt-nav-script')
    if nav_script:
        body = soup.find('body')
        if body and nav_script.parent != body:
            nav_script.extract()
            body.append(nav_script)

    # 11. High-contrast overrides
    if not soup.find(id='ltt-accessibility-contrast-overrides'):
        contrast_style = soup.new_tag('style', id='ltt-accessibility-contrast-overrides')
        contrast_style.string = minify_css("""
.ltt-mega-head{color:#475569!important;}
.ltt-mobile-label{color:#475569!important;}
.ltt-lang-item .lang-code-tag{color:#1e293b!important;background:#e2e8f0!important;}
.ltt-author-role{color:#475569!important;}
.bpa-psub{color:#475569!important;}
.bpa-best-for{color:#334155!important;}
.ltt-buy-price-sub{color:#cbd5e1!important;}
.ltt-bc-sep{color:#64748b!important;}
.bpa-card-price-sub{color:#475569!important;}
.ltt-gallery-badge{background:rgba(15,23,42,0.9)!important;color:#fff!important;}
.bpa-gallery,.bpa-gallery-viewport,.bpa-gallery-img{aspect-ratio:800/534!important;}
""")
        head.append(contrast_style)

    # 12. Save optimized file
    html_out = str(soup)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(fix_switcher_html(html_out, file_path))

    orig_len = len(html)
    new_len = len(html_out)
    diff = orig_len - new_len
    pct = (diff / orig_len) * 100 if orig_len else 0
    print(f"✓ Optimized {os.path.relpath(file_path, BASE_DIR)}: {orig_len} -> {new_len} bytes (-{diff} bytes, -{pct:.1f}%)")

def run():
    print("=== STARTING DEEP OPTIMIZATION & MINIFICATION ===")
    
    # English River
    optimize_file(os.path.join(BASE_DIR, 'river.html'), 'river')
    shutil.copy2(os.path.join(BASE_DIR, 'river.html'), os.path.join(BASE_DIR, 'best-budapest-river-cruises.html'))
    shutil.copy2(os.path.join(BASE_DIR, 'river.html'), os.path.join(BASE_DIR, 'best-budapest-river-cruises/index.html'))
    shutil.copy2(os.path.join(BASE_DIR, 'river.html'), os.path.join(BASE_DIR, 'budapest-river-cruises.html'))
    shutil.copy2(os.path.join(BASE_DIR, 'river.html'), os.path.join(BASE_DIR, 'budapest-river-cruises/index.html'))

    # English Dinner
    optimize_file(os.path.join(BASE_DIR, 'dinner.html'), 'dinner')
    shutil.copy2(os.path.join(BASE_DIR, 'dinner.html'), os.path.join(BASE_DIR, 'best-dinner-cruises-budapest.html'))
    shutil.copy2(os.path.join(BASE_DIR, 'dinner.html'), os.path.join(BASE_DIR, 'best-dinner-cruises-budapest/index.html'))
    shutil.copy2(os.path.join(BASE_DIR, 'dinner.html'), os.path.join(BASE_DIR, 'budapest-dinner-cruises.html'))
    shutil.copy2(os.path.join(BASE_DIR, 'dinner.html'), os.path.join(BASE_DIR, 'budapest-dinner-cruises/index.html'))

    # Hungarian Pages
    optimize_file(os.path.join(BASE_DIR, 'hu/setahajozas-a-dunan-budapest/index.html'), 'river')
    optimize_file(os.path.join(BASE_DIR, 'hu/setahajozas-a-dunan-vacsoraval/index.html'), 'dinner')

    print("=== DEEP OPTIMIZATION COMPLETE ===")

if __name__ == '__main__':
    run()
