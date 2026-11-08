#!/usr/bin/env python3
"""
MASTER SECONDARY PAGES COMPILER — BUDAPEST ADVENTURES
Compiles all 15 secondary editorial, attraction, and utility pages across all 21 languages:
- About: /{lang}/about/index.html
- Contact: /{lang}/contact/index.html
- Thermal Baths: /{lang}/thermal-baths-budapest/index.html
- Night Cruises: /{lang}/best-night-cruises-budapest/index.html
- Private Boats: /{lang}/best-private-boat-tours-budapest/index.html
- Unlimited Prosecco: /{lang}/unlimited-prosecco-cruises-budapest/index.html
- Walking Tours: /{lang}/best-walking-tours-budapest/index.html
- Hostels: /{lang}/best-hostels-budapest/index.html
- Budapest Card: /{lang}/budapest-card-is-it-worth-it/index.html
- Travel Guide: /{lang}/budapest-travel-guide/index.html
- Airport Transfer: /{lang}/budapest-airport-to-city-center/index.html
- Parliament: /{lang}/budapest-attractions/budapest-parliament/index.html (and alias)
- Group Booking: /{lang}/budapest-river-cruise-group-booking/index.html
- Tourism Statistics: /{lang}/budapest-tourism-statistics/index.html
- Candlelit Review: /{lang}/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest/index.html

Strictly enforces:
1. Universal link localization (ensures visitors stay in /{lang}/ across the whole site)
2. Affiliate tracking integrity (preserves Legenda partner=38585, TourCMS, Tiqets)
3. Cleans Linguana scripts / badge artifacts
4. Sets proper html lang and rtl direction for Hebrew (he)
"""

import os
import re
import sys
from bs4 import BeautifulSoup

BASE_DIR = '/Users/adamdimitrov/Development/budapest-adventures'
CACHE_DIR = os.path.join(BASE_DIR, 'data', 'harvested_html')

LANGS = ['hu', 'de', 'fr', 'it', 'es', 'ro', 'pl', 'nl', 'cs', 'sk', 'pt', 'ru', 'hr', 'sr', 'bg', 'el', 'tr', 'uk', 'he', 'ja', 'ko']

SLUG_MAP = {
    'hu': {'home': '', 'river': 'setahajozas-a-dunan-budapest', 'dinner': 'setahajozas-a-dunan-vacsoraval'},
    'ro': {'home': '', 'river': 'croaziera-dunare-budapesta', 'dinner': 'croaziera-dunare-cu-cina-budapesta'},
    'ja': {'home': '', 'river': 'budapesuto-ribakuruzu', 'dinner': 'budapesuto-dinakuruzu'},
    'it': {'home': '', 'river': 'crociere-danubio-budapest', 'dinner': 'crociere-cena-danubio-budapest'},
    'fr': {'home': '', 'river': 'croisieres-danube-budapest', 'dinner': 'diner-croisieres-danube-budapest'},
    'pl': {'home': '', 'river': 'rejsy-dunaju-budapeszt', 'dinner': 'rejsy-dunaju-budapeszt-kolacja'},
    'cs': {'home': '', 'river': 'nejlepší-budapest-řeka-plavby', 'dinner': 'nejlepší-večeře-plavby-budapešť'},
    'hr': {'home': '', 'river': 'najbolja-krstarenja-rijekom-budimpešta', 'dinner': 'najbolja-krstarenja-svečerom-budimpešta'},
    'ru': {'home': '', 'river': 'rechnyye-kruizy-budapesht-dunay', 'dinner': 'uzhin-kruizy-budapesht-dunay'},
    'el': {'home': '', 'river': 'Βουδαπέστη-ποτάμι-κρουαζιέρες', 'dinner': 'καλύτερο-δείπνο-κρουαζιέρες-Βουδαπέστη'},
    'bg': {'home': '', 'river': 'най-добрите-будапеща-речни-круизи', 'dinner': 'най-добрата-вечеря-круизи-будапеща'},
    'es': {'home': '', 'river': 'cruceros-danubio-budapest', 'dinner': 'cruceros-con-cena-danubio-budapest'},
    'sr': {'home': '', 'river': 'најбоље-будапест-река-крстарења', 'dinner': 'најбоља-вечера-крстарења-будимпешта'},
    'he': {'home': '', 'river': 'הפלגות-דנובה-בודפשט', 'dinner': 'ארוחתערב-שייט-דנובה-בודפשט'},
    'pt': {'home': '', 'river': 'budapeste-cruzeiros-danubio', 'dinner': 'budapeste-jantar-cruzeiros-danubio'},
    'sk': {'home': '', 'river': 'riecne-plavby-budapest-dunaj', 'dinner': 'vecera-plavby-budapest-dunaj'},
    'tr': {'home': '', 'river': 'nehir-yolculuklari-budapeste-tuna', 'dinner': 'aksam-yemegi-yolculuklari-budapeste-tuna'},
    'uk': {'home': '', 'river': 'найкращі-річкові-круїзи-будапешті', 'dinner': 'найкраща-вечеря-круїзи-будапешт'},
    'de': {'home': '', 'river': 'bootsfahrten-dunau-budapest', 'dinner': 'bootsfahrten-mit-abendessen-dunau-budapest'},
    'ko': {'home': '', 'river': 'gang-keulujeu-budapeseuteu-danyubeu', 'dinner': 'dineo-keulujeu-budapeseuteu-danyubeu'},
    'nl': {'home': '', 'river': 'beste-boedapest-riviercruises', 'dinner': 'beste-diner-cruises-budapest'}
}

# Mapping of file key to relative directory path inside /{lang}/
PAGE_TARGETS = {
    'about': 'about',
    'contact': 'contact',
    'thermal_baths': 'thermal-baths-budapest',
    'night_cruises': 'best-night-cruises-budapest',
    'private_boats': 'best-private-boat-tours-budapest',
    'unlimited_prosecco': 'unlimited-prosecco-cruises-budapest',
    'walking_tours': 'best-walking-tours-budapest',
    'hostels': 'best-hostels-budapest',
    'budapest_card': 'budapest-card-is-it-worth-it',
    'travel_guide': 'budapest-travel-guide',
    'airport_transfer': 'budapest-airport-to-city-center',
    'parliament': 'budapest-attractions/budapest-parliament',
    'group_booking': 'budapest-river-cruise-group-booking',
    'tourism_statistics': 'budapest-tourism-statistics',
    'candlelit_dinner': 'best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest'
}

def localize_html(raw_html, lang, page_slug):
    soup = BeautifulSoup(raw_html, 'html.parser')
    
    # 1. HTML tag attributes
    html_tag = soup.find('html')
    if html_tag:
        html_tag['lang'] = lang
        if lang == 'he':
            html_tag['dir'] = 'rtl'
        elif html_tag.has_attr('dir'):
            del html_tag['dir']

    # 2. Canonical URL
    target_canon = f"https://www.budapestadventures.com/{lang}/{page_slug}" if lang == 'hu' else f"https://www.budapestadventures.com/{page_slug}"
    canon = soup.find('link', rel='canonical')
    if canon:
        canon['href'] = target_canon
    else:
        new_canon = soup.new_tag('link', rel='canonical', href=target_canon)
        if soup.head:
            soup.head.append(new_canon)

    # 3. Clean Linguana scripts / badges
    for meta in soup.find_all('meta', attrs={'name': 'linguana-site-verification'}):
        meta.decompose()
    for s in soup.find_all('script'):
        src = s.get('src', '')
        if 'emrld.cc' in src or 'linguana' in src:
            s.decompose()

    # 4. Universal Link Localization
    slugs = SLUG_MAP.get(lang, {'river': 'best-budapest-river-cruises', 'dinner': 'best-dinner-cruises-budapest'})
    river_slug = slugs['river']
    dinner_slug = slugs['dinner']

    for a in soup.find_all('a', href=True):
        href = a['href']
        
        # Don't alter external, anchor, mailto, tel
        if href.startswith(('http://', 'https://', 'mailto:', 'tel:', '#', 'javascript:')):
            # Ensure Legenda tracking on outbound links
            if 'legenda.hu' in href and 'partner=38585' not in href:
                sep = '&' if '?' in href else '?'
                a['href'] = f"{href}{sep}partner=38585"
            continue

        # Strip any existing leading language prefix if duplicated
        clean = href
        for l in LANGS:
            if clean.startswith(f"/{l}/"):
                clean = clean[len(l) + 1:]
                break
            elif clean == f"/{l}":
                clean = "/"
                break

        # Map to localized slug
        if clean in ['/best-budapest-river-cruises', '/budapest-river-cruises', '/river']:
            a['href'] = f"/{lang}/{river_slug}"
        elif clean in ['/best-dinner-cruises-budapest', '/budapest-dinner-cruises', '/dinner']:
            a['href'] = f"/{lang}/{dinner_slug}"
        elif clean in ['/', '']:
            a['href'] = f"/{lang}/"
        elif clean in ['/about', 'about']:
            a['href'] = f"/{lang}/about"
        elif clean in ['/contact', 'contact']:
            a['href'] = f"/{lang}/contact"
        elif clean in ['/thermal-baths-budapest', 'thermal-baths-budapest']:
            a['href'] = f"/{lang}/thermal-baths-budapest"
        elif clean in ['/best-night-cruises-budapest', 'best-night-cruises-budapest']:
            a['href'] = f"/{lang}/best-night-cruises-budapest"
        elif clean in ['/best-private-boat-tours-budapest', 'best-private-boat-tours-budapest']:
            a['href'] = f"/{lang}/best-private-boat-tours-budapest"
        elif clean in ['/unlimited-prosecco-cruises-budapest', 'unlimited-prosecco-cruises-budapest']:
            a['href'] = f"/{lang}/unlimited-prosecco-cruises-budapest"
        elif clean in ['/best-walking-tours-budapest', 'best-walking-tours-budapest']:
            a['href'] = f"/{lang}/best-walking-tours-budapest"
        elif clean in ['/best-hostels-budapest', 'best-hostels-budapest']:
            a['href'] = f"/{lang}/best-hostels-budapest"
        elif clean in ['/budapest-card-is-it-worth-it', 'budapest-card-is-it-worth-it']:
            a['href'] = f"/{lang}/budapest-card-is-it-worth-it"
        elif clean in ['/budapest-travel-guide', 'budapest-travel-guide']:
            a['href'] = f"/{lang}/budapest-travel-guide"
        elif clean in ['/budapest-airport-to-city-center', 'budapest-airport-to-city-center']:
            a['href'] = f"/{lang}/budapest-airport-to-city-center"
        elif clean in ['/budapest-attractions/budapest-parliament', '/budapest-parliament', 'budapest-parliament']:
            a['href'] = f"/{lang}/budapest-attractions/budapest-parliament"
        elif clean in ['/budapest-river-cruise-group-booking', 'budapest-river-cruise-group-booking']:
            a['href'] = f"/{lang}/budapest-river-cruise-group-booking"
        elif clean in ['/budapest-tourism-statistics', 'budapest-tourism-statistics']:
            a['href'] = f"/{lang}/budapest-tourism-statistics"
        elif clean in ['/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest', '/candlelit-dinner-cruise-budapest', 'candlelit-dinner-cruise-budapest']:
            a['href'] = f"/{lang}/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest"
        elif clean.startswith('/'):
            a['href'] = f"/{lang}{clean}"
        else:
            a['href'] = f"/{lang}/{clean}"

    return str(soup)

def main():
    print(f"Compiling secondary pages across {len(LANGS)} languages...")
    compiled_count = 0
    alias_count = 0

    for lang in LANGS:
        lang_dir = os.path.join(BASE_DIR, lang)
        os.makedirs(lang_dir, exist_ok=True)
        cached_lang_dir = os.path.join(CACHE_DIR, lang)

        for key, rel_path in PAGE_TARGETS.items():
            src_file = os.path.join(cached_lang_dir, f"{key}.html")
            if not os.path.exists(src_file):
                print(f"[MISSING] {lang}/{key}.html not found in cache")
                continue

            with open(src_file, 'r', encoding='utf-8') as f:
                raw_html = f.read()

            processed_html = localize_html(raw_html, lang, rel_path)
            
            # Destination path: /{lang}/{rel_path}/index.html
            out_dir = os.path.join(lang_dir, rel_path)
            os.makedirs(out_dir, exist_ok=True)
            out_file = os.path.join(out_dir, 'index.html')
            
            with open(out_file, 'w', encoding='utf-8') as f:
                f.write(processed_html)
            compiled_count += 1

            # Extra aliases for convenience
            if key == 'parliament':
                alias_dir = os.path.join(lang_dir, 'budapest-parliament')
                os.makedirs(alias_dir, exist_ok=True)
                with open(os.path.join(alias_dir, 'index.html'), 'w', encoding='utf-8') as f:
                    f.write(processed_html)
                alias_count += 1

    print("\n=======================================================")
    print(f"SECONDARY PAGES COMPILATION COMPLETE:")
    print(f"  Successfully compiled: {compiled_count} pages")
    print(f"  Aliases generated:     {alias_count} pages")
    print(f"  Total HTML files:      {compiled_count + alias_count}")
    print("=======================================================")

if __name__ == '__main__':
    main()
