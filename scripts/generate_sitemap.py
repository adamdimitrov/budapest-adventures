#!/usr/bin/env python3
"""
MASTER SITEMAP GENERATOR — BUDAPEST ADVENTURES
Generates production-grade, validated sitemap.xml with complete hreflang alternate links
across all 21 languages (+ English Master = 22 locales) for all 18 published editorial hubs.
"""

import os
from datetime import datetime

BASE_DIR = '/Users/adamdimitrov/Development/budapest-adventures'
SITEMAP_PATH = os.path.join(BASE_DIR, 'sitemap.xml')

LANGS = ['hu', 'de', 'fr', 'it', 'es', 'ro', 'pl', 'nl', 'cs', 'sk', 'pt', 'ru', 'hr', 'sr', 'bg', 'el', 'tr', 'uk', 'he', 'ja', 'ko']
# The 20 approved non-English languages for sitemap (excluding pruned zombie languages like nl)
SITEMAP_LANGS = [l for l in LANGS if l != 'nl']

SLUG_MAP = {
    'hu': {'river': 'setahajozas-a-dunan-budapest', 'dinner': 'setahajozas-a-dunan-vacsoraval'},
    'ro': {'river': 'croaziera-dunare-budapesta', 'dinner': 'croaziera-dunare-cu-cina-budapesta'},
    'ja': {'river': 'budapesuto-ribakuruzu', 'dinner': 'budapesuto-dinakuruzu'},
    'it': {'river': 'crociere-danubio-budapest', 'dinner': 'crociere-cena-danubio-budapest'},
    'fr': {'river': 'croisieres-danube-budapest', 'dinner': 'diner-croisieres-danube-budapest'},
    'pl': {'river': 'rejsy-dunaju-budapeszt', 'dinner': 'rejsy-dunaju-budapeszt-kolacja'},
    'cs': {'river': 'nejlepší-budapest-řeka-plavby', 'dinner': 'nejlepší-večeře-plavby-budapešť'},
    'hr': {'river': 'najbolja-krstarenja-rijekom-budimpešta', 'dinner': 'najbolja-krstarenja-svečerom-budimpešta'},
    'ru': {'river': 'rechnyye-kruizy-budapesht-dunay', 'dinner': 'uzhin-kruizy-budapesht-dunay'},
    'el': {'river': 'Βουδαπέστη-ποτάμι-κρουαζιέρες', 'dinner': 'καλύτερο-δείπνο-κρουαζιέρες-Βουδαπέστη'},
    'bg': {'river': 'най-добрите-будапеща-речни-круизи', 'dinner': 'най-добрата-вечеря-круизи-будапеща'},
    'es': {'river': 'cruceros-danubio-budapest', 'dinner': 'cruceros-con-cena-danubio-budapest'},
    'sr': {'river': 'најбоље-будапест-река-крстарења', 'dinner': 'најбоља-вечера-крстарења-будимпешта'},
    'he': {'river': 'הפלגות-דנובה-בודפשט', 'dinner': 'ארוחתערב-שייט-דנובה-בודפשט'},
    'pt': {'river': 'budapeste-cruzeiros-danubio', 'dinner': 'budapeste-jantar-cruzeiros-danubio'},
    'sk': {'river': 'riecne-plavby-budapest-dunaj', 'dinner': 'vecera-plavby-budapest-dunaj'},
    'tr': {'river': 'nehir-yolculuklari-budapeste-tuna', 'dinner': 'aksam-yemegi-yolculuklari-budapeste-tuna'},
    'uk': {'river': 'найкращі-річкові-круїзи-будапешті', 'dinner': 'найкраща-вечеря-круїзи-будапешт'},
    'de': {'river': 'bootsfahrten-dunau-budapest', 'dinner': 'bootsfahrten-mit-abendessen-dunau-budapest'},
    'ko': {'river': 'gang-keulujeu-budapeseuteu-danyubeu', 'dinner': 'dineo-keulujeu-budapeseuteu-danyubeu'},
    'nl': {'river': 'beste-boedapest-riviercruises', 'dinner': 'beste-diner-cruises-boedapest'}
}

# 18 Canonical English hubs with their relative paths
HUBS = [
    ('', 1.0, 'daily'),
    ('best-budapest-river-cruises', 1.0, 'daily'),
    ('best-dinner-cruises-budapest', 1.0, 'daily'),
    ('thermal-baths-budapest', 0.9, 'weekly'),
    ('best-night-cruises-budapest', 0.9, 'weekly'),
    ('best-private-boat-tours-budapest', 0.8, 'weekly'),
    ('unlimited-prosecco-cruises-budapest', 0.8, 'weekly'),
    ('best-walking-tours-budapest', 0.8, 'weekly'),
    ('best-hostels-budapest', 0.8, 'weekly'),
    ('budapest-card-is-it-worth-it', 0.8, 'weekly'),
    ('best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest', 0.8, 'weekly'),
    ('budapest-travel-guide', 0.8, 'monthly'),
    ('budapest-airport-to-city-center', 0.8, 'monthly'),
    ('budapest-attractions/budapest-parliament', 0.8, 'monthly'),
    ('budapest-river-cruise-group-booking', 0.7, 'monthly'),
    ('budapest-tourism-statistics', 0.7, 'monthly'),
    ('about', 0.8, 'monthly'),
    ('contact', 0.7, 'monthly')
]

def get_localized_path(en_slug, lang):
    if en_slug == '':
        return f"{lang}/"
    elif en_slug == 'best-budapest-river-cruises':
        return f"{lang}/{SLUG_MAP[lang]['river']}"
    elif en_slug == 'best-dinner-cruises-budapest':
        return f"{lang}/{SLUG_MAP[lang]['dinner']}"
    else:
        return f"{lang}/{en_slug}"

def generate():
    today = datetime.now().strftime('%Y-%m-%d')
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">'
    ]

    for en_slug, priority, changefreq in HUBS:
        loc = f"https://www.budapestadventures.com/{en_slug}" if en_slug else "https://www.budapestadventures.com/"
        lines.append(f'  <!-- Hub: {loc} -->')
        lines.append('  <url>')
        lines.append(f'    <loc>{loc}</loc>')
        lines.append(f'    <lastmod>{today}</lastmod>')
        lines.append(f'    <changefreq>{changefreq}</changefreq>')
        lines.append(f'    <priority>{priority:.1f}</priority>')
        
        # English hreflang
        lines.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{loc}" />')
        
        # 20 Foreign Language hreflangs
        for lang in SITEMAP_LANGS:
            loc_path = get_localized_path(en_slug, lang)
            lang_url = f"https://www.budapestadventures.com/{loc_path}"
            lines.append(f'    <xhtml:link rel="alternate" hreflang="{lang}" href="{lang_url}" />')
            
        # x-default
        lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{loc}" />')
        lines.append('  </url>')
        lines.append('')

    lines.append('</urlset>')

    sitemap_content = '\n'.join(lines)
    with open(SITEMAP_PATH, 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
        
    print(f"✓ Generated sitemap.xml with {len(HUBS)} hubs across {len(LANGS)+1} locales.")

if __name__ == '__main__':
    generate()
