#!/usr/bin/env python3
"""
UPGRADE ALL BUDAPEST ADVENTURES LISTICLES TO 100% AUTHENTIC SLIDERS
Extracts authentic photos (combining comparison deck and review dossiers)
and updates .bpa-media across all 8 listicles.
"""

import sys
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path('/Users/adamdimitrov/Development/budapest-adventures')
SKILL_DIR = Path('/Users/adamdimitrov/.gemini/config/skills/luxury-editorial-system')
sys.path.insert(0, str(SKILL_DIR / 'scripts'))
from compile_webflow_article import extract_slider_images_from_webflow

ARTICLES = [
    ('river.html', None, 'River Cruises'),
    ('dinner.html', SKILL_DIR / 'sources' / 'budapest_dinner_cruises_webflow.html', 'Dinner Cruises'),
    ('best-night-cruises-budapest.html', None, 'Night Cruises'),
    ('best-private-boat-tours-budapest.html', None, 'Private Boats'),
    ('unlimited-prosecco-cruises-budapest.html', None, 'Unlimited Prosecco'),
    ('thermal-baths-budapest.html', None, 'Thermal Baths'),
    ('best-walking-tours-budapest.html', None, 'Walking Tours'),
    ('best-hostels-budapest.html', None, 'Hostels')
]

def upgrade_article_sliders(html_name: str, custom_src: Path, label: str):
    print(f"\nProcessing {label} ({html_name})...")
    page_path = ROOT / html_name
    page_soup = BeautifulSoup(open(page_path, 'r', encoding='utf-8'), 'html.parser')
    
    src_soup = BeautifulSoup(open(custom_src or page_path, 'r', encoding='utf-8'), 'html.parser')
    cards = page_soup.select('.bpa-card')
    num_cards = len(cards)
    print(f"  Found {num_cards} cards on disk.")
    
    slider_imgs = extract_slider_images_from_webflow(src_soup, num_items=num_cards)
    
    # Special handling for dinner.html Card 1 (Legenda): ensure legenda-candlelit-dinner.jpg is first
    if html_name == 'dinner.html' and slider_imgs and len(slider_imgs) > 0:
        legenda_img = page_soup.new_tag('img', src='/legenda-candlelit-dinner.jpg', alt='Legenda Candlelit Dinner Cruise')
        slider_imgs[0] = [legenda_img] + [img for img in slider_imgs[0] if 'legenda-candlelit-dinner.jpg' not in img.get('src', '')]
    
    extracted_counts = [len(x) for x in slider_imgs]
    print(f"  Extracted photo counts: {extracted_counts}")
    
    for idx, card in enumerate(cards):
        media = card.select_one('.bpa-media')
        if not media:
            continue
        
        rank_tag = media.select_one('.bpa-rank-tag')
        rank_tag_html = str(rank_tag) if rank_tag else ''
        
        imgs = slider_imgs[idx] if idx < len(slider_imgs) else []
        count = len(imgs)
        
        title_tag = card.select_one('.bpa-title')
        title_text = title_tag.get_text(strip=True) if title_tag else f'Attraction {idx+1}'
        alt = title_text.replace('"', '&quot;')
        
        imgs_rendered = []
        for i, img in enumerate(imgs):
            src = img.get('src', '')
            srcset = img.get('srcset', '')
            sizes = img.get('sizes', '(max-width: 767px) 420px, (max-width: 991px) 55vw, (max-width: 1439px) 49vw, 50vw')
            loading = 'eager' if (idx == 0 and i == 0) else 'lazy'
            fetchpriority = ' fetchpriority="high"' if (idx == 0 and i == 0) else ''
            srcset_attr = f' srcset="{srcset}"' if srcset else ''
            sizes_attr = f' sizes="{sizes}"' if sizes else ''
            imgs_rendered.append(f'<img src="{src}" loading="{loading}"{fetchpriority}{sizes_attr}{srcset_attr} alt="{alt}"/>')
        
        imgs_str = '\n                '.join(imgs_rendered)
        
        if count > 1:
            controls_html = f"""<button type="button" class="bpa-arrow prev" onclick="bpaSlide(this,-1)" aria-label="Previous photo">‹</button>
              <button type="button" class="bpa-arrow next" onclick="bpaSlide(this,1)" aria-label="Next photo">›</button>
              <span class="bpa-pill">1 / {count}</span>"""
            onscroll_attr = ' onscroll="bpaCount(this)"'
        else:
            controls_html = ''
            onscroll_attr = ''
        
        new_media_html = f"""<div class="bpa-media">
              {rank_tag_html}
              {controls_html}
              <div class="bpa-slider"{onscroll_attr}>
                {imgs_str}
              </div>
            </div>"""
        
        new_media_soup = BeautifulSoup(new_media_html, 'html.parser').select_one('.bpa-media')
        media.replace_with(new_media_soup)
    
    with open(page_path, 'w', encoding='utf-8') as f:
        f.write(str(page_soup))
    
    # Verify written file
    verify_soup = BeautifulSoup(open(page_path, 'r', encoding='utf-8'), 'html.parser')
    verified_counts = [len(c.select('.bpa-slider img')) for c in verify_soup.select('.bpa-card')]
    print(f"  ✓ Successfully updated {html_name}! Final slider counts: {verified_counts}")

def main():
    print("==================================================================")
    print("UPGRADING ALL BUDAPEST ADVENTURES LISTICLES TO 100% AUTHENTIC SLIDERS")
    print("==================================================================")
    for html_name, custom_src, label in ARTICLES:
        upgrade_article_sliders(html_name, custom_src, label)
    print("\nAll 8 Budapest Adventures Listicles Successfully Upgraded!")

if __name__ == '__main__':
    main()
