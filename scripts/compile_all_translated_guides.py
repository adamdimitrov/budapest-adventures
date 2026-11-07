#!/usr/bin/env python3
"""
MASTER TRANSLATED DESTINATION GUIDE COMPILER — BUDAPEST ADVENTURES
Compiles static multi-language directory architecture across all 21 foreign languages (+ English = 22):
- Homepage: /{lang}/index.html
- River Cruises: /{lang}/{river_slug}/index.html
- Dinner Cruises: /{lang}/{dinner_slug}/index.html

Enforces 100% design parity with English Luxury Editorial System:
- Canonical card architecture without spec pills
- 4-Bento review cards, quick facts, photo sliders, mobile drawer
- 100% affiliate tracking link preservation (partner=38585 / TourCMS / Tiqets)
- Fast, pure static HTML on Vercel (Zero Webflow, Zero Linguana)
"""

import os
import re
import sys
import json
from bs4 import BeautifulSoup

BASE_DIR = '/Users/adamdimitrov/Development/budapest-adventures'
CACHE_DIR = os.path.join(BASE_DIR, 'data', 'harvested_html')

LANGS = ['hu', 'ro', 'ja', 'it', 'fr', 'pl', 'cs', 'hr', 'ru', 'el', 'bg', 'es', 'sr', 'he', 'pt', 'sk', 'tr', 'uk', 'de', 'ko', 'nl']

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
    'nl': {'home': '', 'river': 'beste-boedapest-riviercruises', 'dinner': 'beste-diner-cruises-boedapest'}
}

# UI Microcopy
COMMON_UI = {
    'hu': {'btn_check': 'Szabad időpontok ellenőrzése →', 'read_review': 'Értékelés elolvasása ↓', 'best_overall': 'Legjobb Választás', 'pros': 'Előnyök:', 'cons': 'Hátrányok:', 'from_price': 'Ár:'},
    'ro': {'btn_check': 'Verifică disponibilitatea →', 'read_review': 'Citește recenzia ↓', 'best_overall': 'Cea Mai Bună Alegere', 'pros': 'Pro:', 'cons': 'Contra:', 'from_price': 'De la'},
    'it': {'btn_check': 'Verifica disponibilità →', 'read_review': 'Leggi recensione ↓', 'best_overall': 'Migliore Scelta', 'pros': 'Pro:', 'cons': 'Contro:', 'from_price': 'Da'},
    'fr': {'btn_check': 'Vérifier les disponibilités →', 'read_review': 'Lire l\'avis ↓', 'best_overall': 'Meilleur Choix', 'pros': 'Points forts :', 'cons': 'Points faibles :', 'from_price': 'À partir de'},
    'de': {'btn_check': 'Verfügbarkeit prüfen →', 'read_review': 'Rezension lesen ↓', 'best_overall': 'Gesamtsieger', 'pros': 'Vorteile:', 'cons': 'Nachteile:', 'from_price': 'Ab'},
    'es': {'btn_check': 'Consultar disponibilidad →', 'read_review': 'Leer reseña ↓', 'best_overall': 'Mejor Opción', 'pros': 'Pros:', 'cons': 'Contras:', 'from_price': 'Desde'},
    'pl': {'btn_check': 'Sprawdź dostępność →', 'read_review': 'Przeczytaj recenzję ↓', 'best_overall': 'Najlepszy Wybór', 'pros': 'Zalety:', 'cons': 'Wady:', 'from_price': 'Od'},
    'cs': {'btn_check': 'Ověřit dostupnost →', 'read_review': 'Přečíst recenzi ↓', 'best_overall': 'Nejlepší Volba', 'pros': 'Klady:', 'cons': 'Zápory:', 'from_price': 'Od'},
    'ja': {'btn_check': '空き状況を確認する →', 'read_review': 'レビューを読む ↓', 'best_overall': 'ベスト評価', 'pros': 'メリット:', 'cons': 'デメリット:', 'from_price': '料金:'},
    'nl': {'btn_check': 'Beschikbaarheid controleren →', 'read_review': 'Lees beoordeling ↓', 'best_overall': 'Beste Keuze', 'pros': 'Voordelen:', 'cons': 'Nadelen:', 'from_price': 'Vanaf'}
}

def get_ui(lang, key, default):
    return COMMON_UI.get(lang, {}).get(key, default)

def extract_meta_and_headings(harvested_path):
    if not os.path.exists(harvested_path):
        return None
    soup = BeautifulSoup(open(harvested_path, 'r', encoding='utf-8').read(), 'html.parser')
    
    title = soup.title.string.strip() if soup.title and soup.title.string else ''
    meta_desc = ''
    m = soup.find('meta', {'name': 'description'})
    if m and m.get('content'):
        meta_desc = m['content'].strip()
    
    h1 = soup.find('h1')
    h1_text = h1.text.strip() if h1 else ''
    
    # Extract headings
    h2s = [h2.text.strip() for h2 in soup.find_all('h2') if h2.text.strip()]
    return {
        'title': title,
        'description': meta_desc,
        'h1': h1_text,
        'h2s': h2s
    }

def compile_pages():
    print(f"Starting compilation for {len(LANGS)} languages...")
    
    en_river_html = open(os.path.join(BASE_DIR, 'river.html'), 'r', encoding='utf-8').read()
    en_dinner_html = open(os.path.join(BASE_DIR, 'dinner.html'), 'r', encoding='utf-8').read()
    en_home_html = open(os.path.join(BASE_DIR, 'index.html'), 'r', encoding='utf-8').read()
    
    compiled_count = 0
    
    for lang in LANGS:
        slugs = SLUG_MAP[lang]
        river_slug = slugs['river']
        dinner_slug = slugs['dinner']
        
        lang_dir = os.path.join(BASE_DIR, lang)
        os.makedirs(lang_dir, exist_ok=True)
        
        # 1. COMPILE RIVER GUIDE
        river_dir = os.path.join(lang_dir, river_slug)
        os.makedirs(river_dir, exist_ok=True)
        river_out = os.path.join(river_dir, 'index.html')
        
        harvested_river = os.path.join(CACHE_DIR, lang, 'river.html')
        river_data = extract_meta_and_headings(harvested_river)
        
        soup_river = BeautifulSoup(en_river_html, 'html.parser')
        
        # Update canonical
        can = soup_river.find('link', {'rel': 'canonical'})
        if can:
            can['href'] = f"https://www.budapestadventures.com/{lang}/{river_slug}"
            
        # Update meta & title
        if river_data and river_data['title']:
            if soup_river.title:
                soup_river.title.string = river_data['title']
        if river_data and river_data['description']:
            m = soup_river.find('meta', {'name': 'description'})
            if m:
                m['content'] = river_data['description']
        if river_data and river_data['h1']:
            h1 = soup_river.find('h1')
            if h1:
                h1.string = river_data['h1']
                
        # Localize CTAs
        btn_check_text = get_ui(lang, 'btn_check', 'Check Availability →')
        for btn in soup_river.find_all(class_='bpa-btn'):
            if 'Check Availability' in btn.text or '→' in btn.text:
                btn.string = btn_check_text
                
        with open(river_out, 'w', encoding='utf-8') as f:
            f.write(str(soup_river))
        compiled_count += 1
        
        # 2. COMPILE DINNER GUIDE
        dinner_dir = os.path.join(lang_dir, dinner_slug)
        os.makedirs(dinner_dir, exist_ok=True)
        dinner_out = os.path.join(dinner_dir, 'index.html')
        
        harvested_dinner = os.path.join(CACHE_DIR, lang, 'dinner.html')
        dinner_data = extract_meta_and_headings(harvested_dinner)
        
        soup_dinner = BeautifulSoup(en_dinner_html, 'html.parser')
        
        can_dinner = soup_dinner.find('link', {'rel': 'canonical'})
        if can_dinner:
            can_dinner['href'] = f"https://www.budapestadventures.com/{lang}/{dinner_slug}"
            
        if dinner_data and dinner_data['title']:
            if soup_dinner.title:
                soup_dinner.title.string = dinner_data['title']
        if dinner_data and dinner_data['description']:
            m = soup_dinner.find('meta', {'name': 'description'})
            if m:
                m['content'] = dinner_data['description']
        if dinner_data and dinner_data['h1']:
            h1 = soup_dinner.find('h1')
            if h1:
                h1.string = dinner_data['h1']
                
        for btn in soup_dinner.find_all(class_='bpa-btn'):
            if 'Check Availability' in btn.text or '→' in btn.text:
                btn.string = btn_check_text
                
        with open(dinner_out, 'w', encoding='utf-8') as f:
            f.write(str(soup_dinner))
        compiled_count += 1
        
        # 3. COMPILE LOCALIZED HOMEPAGE
        home_out = os.path.join(lang_dir, 'index.html')
        harvested_home = os.path.join(CACHE_DIR, lang, 'home.html')
        home_data = extract_meta_and_headings(harvested_home)
        
        soup_home = BeautifulSoup(en_home_html, 'html.parser')
        can_home = soup_home.find('link', {'rel': 'canonical'})
        if can_home:
            can_home['href'] = f"https://www.budapestadventures.com/{lang}/"
            
        if home_data and home_data['title']:
            if soup_home.title:
                soup_home.title.string = home_data['title']
        if home_data and home_data['description']:
            m = soup_home.find('meta', {'name': 'description'})
            if m:
                m['content'] = home_data['description']
                
        # Update cards links to point to localized slugs
        for a in soup_home.find_all('a', href=True):
            if a['href'] in ['/best-budapest-river-cruises', '/budapest-river-cruises']:
                a['href'] = f"/{lang}/{river_slug}"
            elif a['href'] in ['/best-dinner-cruises-budapest', '/budapest-dinner-cruises']:
                a['href'] = f"/{lang}/{dinner_slug}"
                
        with open(home_out, 'w', encoding='utf-8') as f:
            f.write(str(soup_home))
        compiled_count += 1
        
        print(f"✓ [{lang.upper()}] Compiled home, river ({river_slug}), and dinner ({dinner_slug})")

    print(f"\nCompilation Complete: {compiled_count} static pages compiled across {len(LANGS)} languages.")

if __name__ == '__main__':
    compile_pages()
