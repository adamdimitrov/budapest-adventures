#!/usr/bin/env python3
"""
HARVEST LIVE LINGUANA TRANSLATIONS FOR TOP 21 LANGUAGES
Scrapes and caches raw HTML and text assets from live budapestadventures.com before Linguana/Webflow DNS is cut.
"""

import os
import urllib.request
import urllib.parse
import json
import time

BASE_DIR = '/Users/adamdimitrov/Development/budapest-adventures'
CACHE_DIR = os.path.join(BASE_DIR, 'data', 'harvested_html')
os.makedirs(CACHE_DIR, exist_ok=True)

# 21 Languages map for core money hubs
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

def harvest():
    success_count = 0
    total_count = 0
    
    for lang, pages in SLUG_MAP.items():
        lang_dir = os.path.join(CACHE_DIR, lang)
        os.makedirs(lang_dir, exist_ok=True)
        
        for page_type, slug in pages.items():
            total_count += 1
            file_name = f"{page_type}.html"
            out_path = os.path.join(lang_dir, file_name)
            
            if os.path.exists(out_path) and os.path.getsize(out_path) > 10000:
                print(f"[CACHED] {lang}/{page_type}")
                success_count += 1
                continue
                
            url = f"https://www.budapestadventures.com/{lang}/{slug}" if slug else f"https://www.budapestadventures.com/{lang}/"
            encoded_url = urllib.parse.quote(url, safe=':/-')
            
            req = urllib.request.Request(
                encoded_url,
                headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
            )
            
            try:
                with urllib.request.urlopen(req, timeout=12) as resp:
                    if resp.status == 200:
                        html = resp.read().decode('utf-8', errors='ignore')
                        with open(out_path, 'w', encoding='utf-8') as f:
                            f.write(html)
                        print(f"[SAVED] {lang}/{page_type} ({len(html)} bytes)")
                        success_count += 1
                    else:
                        print(f"[HTTP {resp.status}] {lang}/{page_type} -> {url}")
            except Exception as e:
                print(f"[ERROR] {lang}/{page_type} -> {e}")
            
            time.sleep(0.1)

    print(f"\nHarvest Complete: {success_count}/{total_count} pages captured successfully.")

if __name__ == '__main__':
    harvest()
