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
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import scripts.build_hungarian_pages as bhp
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


NAV_I18N = {
    'de': {'dropdown': 'Donau-Schifffahrten', 'head_cruises': 'DONAU-SCHIFFFAHRTEN', 'head_attractions': 'SEHENSWÜRDIGKEITEN & BÄDER', 'river': 'Donau-Schifffahrten', 'dinner': 'Abendessen-Schifffahrten', 'card': 'Budapest Card', 'about': 'Über uns', 'contact': 'Kontakt', 'footer_flagship': 'Wichtige Budapest-Guides', 'footer_trust': 'Vertrauen & Unternehmen', 'footer_copy': '© 2026 BudapestAdventures.com. Alle Rechte vorbehalten.'},
    'fr': {'dropdown': 'Croisières Danube', 'head_cruises': 'CROISIÈRES SUR LE DANUBE', 'head_attractions': 'ATTRACTIONS & BAINS', 'river': 'Croisières Promenade', 'dinner': 'Dîners Croisières', 'card': 'Budapest Card', 'about': 'À propos', 'contact': 'Contact', 'footer_flagship': 'Guides Phares de Budapest', 'footer_trust': 'Confiance & Entreprise', 'footer_copy': '© 2026 BudapestAdventures.com. Tous droits réservés.'},
    'es': {'dropdown': 'Cruceros Danubio', 'head_cruises': 'CRUCEROS POR EL DANUBIO', 'head_attractions': 'ATRACCIONES Y BALNEARIOS', 'river': 'Cruceros Paseo', 'dinner': 'Cruceros con Cena', 'card': 'Budapest Card', 'about': 'Sobre nosotros', 'contact': 'Contacto', 'footer_flagship': 'Guías Principales de Budapest', 'footer_trust': 'Confianza y Empresa', 'footer_copy': '© 2026 BudapestAdventures.com. Todos los derechos reservados.'},
    'it': {'dropdown': 'Crociere Danubio', 'head_cruises': 'CROCIERE SUL DANUBIO', 'head_attractions': 'ATTRAZIONI E TERME', 'river': 'Crociere Panoramiche', 'dinner': 'Crociere con Cena', 'card': 'Budapest Card', 'about': 'Chi siamo', 'contact': 'Contatti', 'footer_flagship': 'Guide Principali di Budapest', 'footer_trust': 'Affidabilità & Azienda', 'footer_copy': '© 2026 BudapestAdventures.com. Tutti i diritti riservati.'},
    'ro': {'dropdown': 'Croaziere Dunăre', 'head_cruises': 'CROAZIERE PE DUNĂRE', 'head_attractions': 'ATRACȚII & BĂI TERMALE', 'river': 'Croaziere pe Dunăre', 'dinner': 'Croaziere cu Cină', 'card': 'Budapest Card', 'about': 'Despre noi', 'contact': 'Contact', 'footer_flagship': 'Ghiduri de Top în Budapesta', 'footer_trust': 'Încredere & Companie', 'footer_copy': '© 2026 BudapestAdventures.com. Toate drepturile rezervate.'},
    'pl': {'dropdown': 'Rejsy po Dunaju', 'head_cruises': 'REJSY PO DUNAJU', 'head_attractions': 'ATRAKCJE I TERMY', 'river': 'Rejsy Widokowe', 'dinner': 'Rejsy z Kolacją', 'card': 'Budapest Card', 'about': 'O nas', 'contact': 'Kontakt', 'footer_flagship': 'Główne Przewodniki po Budapeszcie', 'footer_trust': 'Zaufanie i Informacje', 'footer_copy': '© 2026 BudapestAdventures.com. Wszelkie prawa zastrzeżone.'},
    'cs': {'dropdown': 'Plavby po Dunaji', 'head_cruises': 'PLAVBY PO DUNAJI', 'head_attractions': 'PAMÁTKY A LÁZNĚ', 'river': 'Vyhlídkové Plavby', 'dinner': 'Plavby s Večeří', 'card': 'Budapest Card', 'about': 'O nás', 'contact': 'Kontakt', 'footer_flagship': 'Hlavní Průvodci Budapeští', 'footer_trust': 'Důvěryhodnost a Společnost', 'footer_copy': '© 2026 BudapestAdventures.com. Všechna práva vyhrazena.'},
    'sk': {'dropdown': 'Plavby po Dunaji', 'head_cruises': 'PLAVBY PO DUNAJI', 'head_attractions': 'PAMIATKY A KÚPELE', 'river': 'Vyhliadkové Plavby', 'dinner': 'Plavby s Večerou', 'card': 'Budapest Card', 'about': 'O nás', 'contact': 'Kontakt', 'footer_flagship': 'Hlavné Sprievodce Budapešťou', 'footer_trust': 'Dôveryhodnosť a Spoločnosť', 'footer_copy': '© 2026 BudapestAdventures.com. Všetky práva vyhradené.'},
    'nl': {'dropdown': 'Donau Cruises', 'head_cruises': 'DONAU RIVIERCRUISES', 'head_attractions': 'ATTRACTIES & BADEN', 'river': 'Riviercruises', 'dinner': 'Diner Cruises', 'card': 'Budapest Card', 'about': 'Over ons', 'contact': 'Contact', 'footer_flagship': 'Belangrijkste Boedapest Gidsen', 'footer_trust': 'Vertrouwen & Bedrijf', 'footer_copy': '© 2026 BudapestAdventures.com. Alle rechten voorbehouden.'},
    'pt': {'dropdown': 'Cruzeiros Danúbio', 'head_cruises': 'CRUZEIROS NO DANÚBIO', 'head_attractions': 'ATRAÇÕES E TERMAS', 'river': 'Cruzeiros no Danúbio', 'dinner': 'Cruzeiros com Jantar', 'card': 'Budapest Card', 'about': 'Sobre nós', 'contact': 'Contato', 'footer_flagship': 'Principais Guias de Budapeste', 'footer_trust': 'Confiança e Empresa', 'footer_copy': '© 2026 BudapestAdventures.com. Todos os direitos reservados.'},
    'ja': {'dropdown': 'ドナウ川クルーズ', 'head_cruises': 'ドナウ川クルーズ', 'head_attractions': '観光名所＆温泉', 'river': 'リバークルーズ', 'dinner': 'ディナークルーズ', 'card': 'ブダペストカード', 'about': '運営情報', 'contact': 'お問い合わせ', 'footer_flagship': 'ブダペスト主要ガイド', 'footer_trust': '信頼と運営方針', 'footer_copy': '© 2026 BudapestAdventures.com. All rights reserved.'},
    'hr': {'dropdown': 'Krstarenja Dunavom', 'head_cruises': 'KRSTARENJA DUNAVOM', 'head_attractions': 'ATRAKCIJE & TOPLICE', 'river': 'Panoramska Krstarenja', 'dinner': 'Krstarenja s Večerom', 'card': 'Budapest Card', 'about': 'O nama', 'contact': 'Kontakt', 'footer_flagship': 'Vodeći Vodiči kroz Budimpeštu', 'footer_trust': 'Povjerenje & Tvrtka', 'footer_copy': '© 2026 BudapestAdventures.com. Sva prava pridržana.'},
    'ru': {'dropdown': 'Круизы по Дунаю', 'head_cruises': 'КРУИЗЫ ПО ДУНАЮ', 'head_attractions': 'ДОСТОПРИМЕЧАТЕЛЬНОСТИ И КУПАЛЬНИ', 'river': 'Прогулочные Круизы', 'dinner': 'Круизы с Ужином', 'card': 'Budapest Card', 'about': 'О нас', 'contact': 'Контакты', 'footer_flagship': 'Главные Гиды по Будапешту', 'footer_trust': 'Доверие и Компания', 'footer_copy': '© 2026 BudapestAdventures.com. Все права защищены.'},
    'el': {'dropdown': 'Κρουαζιέρες Δούναβη', 'head_cruises': 'ΚΡΟΥΑΖΙΕΡΕΣ ΣΤΟΝ ΔΟΥΝΑΒΗ', 'head_attractions': 'ΑΞΙΟΘΕΑΤΑ & ΛΟΥΤΡΑ', 'river': 'Κρουαζιέρες Περιήγησης', 'dinner': 'Κρουαζιέρες με Δείπνο', 'card': 'Budapest Card', 'about': 'Σχετικά', 'contact': 'Επικοινωνία', 'footer_flagship': 'Κορυφαίοι Οδηγοί Βουδαπέστης', 'footer_trust': 'Εμπιστοσύνη & Εταιρεία', 'footer_copy': '© 2026 BudapestAdventures.com. Με επιφύλαξη παντός δικαιώματος.'},
    'bg': {'dropdown': 'Круизи по Дунав', 'head_cruises': 'КРУИЗИ ПО ДУНАВ', 'head_attractions': 'ЗАБЕЛЕЖИТЕЛНОСТИ И БАНИ', 'river': 'Панорамни Круизи', 'dinner': 'Круизи с Вечеря', 'card': 'Budapest Card', 'about': 'За нас', 'contact': 'Контакти', 'footer_flagship': 'Водещи Пътеводители за Будапеща', 'footer_trust': 'Доверие и Компания', 'footer_copy': '© 2026 BudapestAdventures.com. Всички права запазени.'},
    'sr': {'dropdown': 'Krstarenja Dunavom', 'head_cruises': 'KRSTARENJA DUNAVOM', 'head_attractions': 'ATRAKCIJE & BANJE', 'river': 'Panoramska Krstarenja', 'dinner': 'Krstarenja sa Večerom', 'card': 'Budapest Card', 'about': 'O nama', 'contact': 'Kontakt', 'footer_flagship': 'Glavni Vodiči kroz Budimpeštu', 'footer_trust': 'Poverenje & Kompanija', 'footer_copy': '© 2026 BudapestAdventures.com. Sva prava zadržana.'},
    'he': {'dropdown': 'שייט על הדנובה', 'head_cruises': 'שייט על הדנובה', 'head_attractions': 'אטרקציות ומרחצאות', 'river': 'שייט סיור', 'dinner': 'שייט עם ארוחת ערב', 'card': 'כרטיס בודפשט', 'about': 'אודות', 'contact': 'צור קשר', 'footer_flagship': 'מדריכי הדגל של בודפשט', 'footer_trust': 'אמינות והחברה', 'footer_copy': '© 2026 BudapestAdventures.com. כל הזכויות שמורות.'},
    'tr': {'dropdown': 'Tuna Nehri Turları', 'head_cruises': 'TUNA NEHRİ TURLARI', 'head_attractions': 'GEZİLECEK YERLER VE KAPLICALAR', 'river': 'Nehir Gezi Turları', 'dinner': 'Akşam Yemekli Turlar', 'card': 'Budapest Card', 'about': 'Hakkımızda', 'contact': 'İletişim', 'footer_flagship': 'Öne Çıkan Budapeşte Rehberleri', 'footer_trust': 'Güvenilirlik ve Şirket', 'footer_copy': '© 2026 BudapestAdventures.com. Tüm hakları saklıdır.'},
    'uk': {'dropdown': 'Круїзи по Дунаю', 'head_cruises': 'КРУЇЗИ ПО ДУНАЮ', 'head_attractions': 'ВИЗНАЧНІ МІСЦЯ ТА КУПАЛЬНІ', 'river': 'Оглядові Круїзи', 'dinner': 'Круїзи з Вечерею', 'card': 'Budapest Card', 'about': 'Про нас', 'contact': 'Контакти', 'footer_flagship': 'Головні Гіди по Будапешту', 'footer_trust': 'Довіра та Компанія', 'footer_copy': '© 2026 BudapestAdventures.com. Всі права захищені.'},
    'ko': {'dropdown': '다뉴브강 크루즈', 'head_cruises': '다뉴브강 유람선', 'head_attractions': '관광명소 & 온천', 'river': '유람선 투어', 'dinner': '디너 크루즈', 'card': '부다페스트 카드', 'about': '소개', 'contact': '문의하기', 'footer_flagship': '부다페스트 주요 여행 가이드', 'footer_trust': '신뢰 & 운영 정책', 'footer_copy': '© 2026 BudapestAdventures.com. All rights reserved.'}
}

def localize_nav_and_footer_multilingual(soup, lang, slugs):
    river_slug = slugs['river']
    dinner_slug = slugs['dinner']
    
    # 1. Update hrefs to point to localized slugs
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href in ['/best-budapest-river-cruises', '/budapest-river-cruises']:
            a['href'] = f'/{lang}/{river_slug}'
        elif href in ['/best-dinner-cruises-budapest', '/budapest-dinner-cruises']:
            a['href'] = f'/{lang}/{dinner_slug}'
        elif href == '/':
            a['href'] = f'/{lang}/'

    # 2. Localize text if in NAV_I18N
    i18n = NAV_I18N.get(lang)
    if i18n:
        dropdown_btn = soup.find('button', class_='ltt-dropdown-btn')
        if dropdown_btn:
            span = dropdown_btn.find('span')
            if span and 'dropdown' in i18n:
                span.string = i18n['dropdown']
                
        mega_heads = soup.find_all(class_='ltt-mega-head')
        if len(mega_heads) >= 1 and 'head_cruises' in i18n:
            mega_heads[0].string = i18n['head_cruises']
        if len(mega_heads) >= 2 and 'head_attractions' in i18n:
            mega_heads[1].string = i18n['head_attractions']
            
        nav_links = soup.find_all(class_='ltt-nav-link')
        for nl in nav_links:
            if 'ltt-dropdown-btn' in nl.get('class', []):
                continue
            txt = nl.text.strip().lower()
            if 'river' in txt: nl.string = i18n.get('river', nl.text)
            elif 'dinner' in txt: nl.string = i18n.get('dinner', nl.text)
            elif 'card' in txt: nl.string = i18n.get('card', nl.text)
            elif 'about' in txt: nl.string = i18n.get('about', nl.text)
            elif 'contact' in txt: nl.string = i18n.get('contact', nl.text)
            
        footer = soup.find('footer') or soup.find(class_='footer-dark')
        if footer:
            col_titles = footer.find_all(class_=lambda c: c and ('footer-col-title' in c or 'footer-link-title' in c))
            if len(col_titles) >= 1 and 'footer_flagship' in i18n:
                col_titles[0].string = i18n['footer_flagship']
            if len(col_titles) >= 2 and 'footer_trust' in i18n:
                col_titles[1].string = i18n['footer_trust']
            if 'footer_copy' in i18n:
                legal = footer.find(class_='legal-wrapper')
                if legal:
                    divs = legal.find_all(class_='legal-text') or legal.find_all('div')
                    if len(divs) >= 1:
                        divs[0].string = i18n['footer_copy']

def compile_pages():
    print(f"Starting compilation for {len(LANGS)} languages...")
    
    en_river_html = open(os.path.join(BASE_DIR, 'river.html'), 'r', encoding='utf-8').read()
    en_dinner_html = open(os.path.join(BASE_DIR, 'dinner.html'), 'r', encoding='utf-8').read()
    en_home_html = open(os.path.join(BASE_DIR, 'index.html'), 'r', encoding='utf-8').read()
    
    compiled_count = 0
    
    for lang in LANGS:
        if lang == 'hu':
            bhp.build_hungarian_home()
            bhp.build_hungarian_river()
            bhp.build_hungarian_dinner()
            compiled_count += 3
            print("✓ [HU] Compiled Hungarian home, river, and dinner using master Luxury Editorial compiler")
            continue
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
                
        # Localize nav & footer
        localize_nav_and_footer_multilingual(soup_river, lang, slugs)
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
                
        # Localize nav & footer
        localize_nav_and_footer_multilingual(soup_dinner, lang, slugs)
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
                
        # Localize nav & footer
        localize_nav_and_footer_multilingual(soup_home, lang, slugs)
        with open(home_out, 'w', encoding='utf-8') as f:
            f.write(str(soup_home))
        compiled_count += 1
        
        print(f"✓ [{lang.upper()}] Compiled home, river ({river_slug}), and dinner ({dinner_slug})")

    print(f"\nCompilation Complete: {compiled_count} static pages compiled across {len(LANGS)} languages.")

if __name__ == '__main__':
    compile_pages()
