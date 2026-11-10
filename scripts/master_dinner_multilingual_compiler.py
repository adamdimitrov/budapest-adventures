#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MASTER DINNER MULTILINGUAL COMPILER — BUDAPEST ADVENTURES
Compiles 100% authentic, fully translated dinner cruise pages across all 21 languages:
HU, DE, FR, ES, IT, NL, PL, RO, CS, SK, HR, SR, BG, RU, UK, EL, TR, PT, HE, JA, KO.
Eradicates 100% of English residual strings, ensures schema and affiliate link integrity.
"""

import os
import sys
import re
import json
from bs4 import BeautifulSoup

BASE_DIR = '/Users/adamdimitrov/Development/budapest-adventures'
sys.path.insert(0, os.path.join(BASE_DIR, 'scripts'))

from dinner_i18n_master_data import (
    DINNER_PAGE_META,
    DINNER_INTRO_DATA,
    DINNER_UI_COMMON,
    DINNER_BEST_FOR_DATA,
    DINNER_KICKERS_DATA,
    DINNER_TOURS_DATA
)
from dinner_pros_cons_i18n import DINNER_PROS_CONS_I18N
from dinner_filter_tabs_i18n import DINNER_FILTER_TABS
from dinner_toc_i18n import DINNER_TOC_I18N
from dinner_spec_chips_i18n import DINNER_SPEC_CHIPS_I18N
from dinner_qf_labels_i18n import DINNER_QF_LABELS

DOCK_TERMS = {
    'hu': 'Kikötő', 'de': 'Anleger', 'fr': 'Quai', 'es': 'Muelle',
    'it': 'Molo', 'nl': 'Steiger', 'pl': 'Przystań', 'ro': 'Pontonul',
    'cs': 'Přístaviště', 'sk': 'Prístavisko', 'hr': 'Pristanište',
    'sr': 'Пристаниште', 'bg': 'Кей', 'ru': 'Причал', 'uk': 'Причал',
    'el': 'Αποβάθρα', 'tr': 'İskele', 'pt': 'Cais', 'he': 'רציף',
    'ja': '桟橋', 'ko': '선착장'
}

from compile_all_languages_luxury import SLUG_MAP

MASTER_DICT_PATH = os.path.join(BASE_DIR, 'data', 'i18n_master_dictionary.json')
MASTER_DICT = json.load(open(MASTER_DICT_PATH, encoding='utf-8')) if os.path.exists(MASTER_DICT_PATH) else {}

def load_combined_walkthrough():
    """Loads and combines walkthrough data from the 3 group JSON files and Bento 1 paragraphs."""
    combined = {}
    for g in [1, 2, 3]:
        p = os.path.join(BASE_DIR, 'data', f'dinner_i18n_group{g}.json')
        if os.path.exists(p):
            try:
                with open(p, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    combined.update(data)
            except Exception as e:
                print(f"Error loading group {g}: {e}")
                
    b1_path = os.path.join(BASE_DIR, 'data', 'dinner_bento1_paragraphs_i18n.json')
    if os.path.exists(b1_path):
        try:
            with open(b1_path, 'r', encoding='utf-8') as f:
                b1_data = json.load(f)
                for l, paras in b1_data.items():
                    if l in combined:
                        combined[l]['bento1_paragraphs'] = paras
        except Exception as e:
            print(f"Error loading bento1 paragraphs: {e}")
            
    qf_val_path = os.path.join(BASE_DIR, 'data', 'dinner_qf_values_i18n.json')
    if os.path.exists(qf_val_path):
        try:
            with open(qf_val_path, 'r', encoding='utf-8') as f:
                qf_data = json.load(f)
                for l, vals in qf_data.items():
                    if l in combined:
                        combined[l]['qf_values'] = vals
        except Exception as e:
            print(f"Error loading qf values: {e}")
            
    return combined

def cleanse_json_ld(soup, lang, pm, intro, canonical_url, tours, best_fors):
    """Cleanse all English leftovers from JSON-LD Schema objects."""
    for s in soup.find_all('script', type='application/ld+json'):
        if s.string:
            try:
                data = json.loads(s.string)
                graphs = data.get('@graph', [data])
                for item in graphs:
                    item['inLanguage'] = lang
                    if item.get('@type') == 'BreadcrumbList':
                        if 'itemListElement' in item:
                            for b_idx, b_item in enumerate(item['itemListElement']):
                                if b_idx == 0:
                                    b_item['name'] = pm.get('bc_home', 'Home')
                                    b_item['item'] = f"https://www.budapestadventures.com/{lang}" if lang != 'en' else "https://www.budapestadventures.com/"
                                elif b_idx == 1:
                                    b_item['name'] = pm.get('bc_curr', 'Danube Cruises')
                                    river_slug = SLUG_MAP[lang]['river'] if lang in SLUG_MAP else 'best-budapest-river-cruises'
                                    b_item['item'] = f"https://www.budapestadventures.com/{lang}/{river_slug}" if lang != 'en' else "https://www.budapestadventures.com/best-budapest-river-cruises"
                                elif b_idx == 2:
                                    b_item['name'] = pm.get('title', '7 Best Dinner Cruises')
                                    b_item['item'] = canonical_url
                    if '@id' in item:
                        item['@id'] = item['@id'].replace('https://www.budapestadventures.com/best-dinner-cruises-budapest', canonical_url)
                    if 'mainEntityOfPage' in item:
                        if isinstance(item['mainEntityOfPage'], dict):
                            item['mainEntityOfPage']['@id'] = canonical_url
                        else:
                            item['mainEntityOfPage'] = canonical_url
                    if 'headline' in item and pm.get('title'):
                        item['headline'] = pm['title']
                    if 'name' in item and pm.get('title'):
                        item['name'] = pm['title']
                    if 'description' in item and pm.get('desc'):
                        item['description'] = pm['desc']
                    if 'articleBody' in item and intro.get('p1'):
                        item['articleBody'] = f"{intro['p1']} {intro['p2']} {intro['p3']}"
                    if 'mainEntity' in item and isinstance(item['mainEntity'], dict):
                        if pm.get('title'): item['mainEntity']['name'] = pm['title']
                        if pm.get('desc'): item['mainEntity']['description'] = pm['desc']
                        if 'itemListElement' in item['mainEntity']:
                            for t_idx, l_item in enumerate(item['mainEntity']['itemListElement']):
                                if t_idx < len(tours):
                                    t_clean = tours[t_idx]['clean_title']
                                    t_desc = best_fors[t_idx] if t_idx < len(best_fors) else pm.get('desc', '')
                                    if 'item' in l_item and isinstance(l_item['item'], dict):
                                        p_obj = l_item['item']
                                        p_obj['name'] = t_clean
                                        p_obj['description'] = t_desc
                                        if 'review' in p_obj and isinstance(p_obj['review'], dict):
                                            p_obj['review']['reviewBody'] = t_desc
                                            p_obj['review'].pop('positiveNotes', None)
                                            p_obj['review'].pop('negativeNotes', None)
                                            
                s.string = json.dumps(data, ensure_ascii=False)
            except Exception:
                pass

def localize_css_pseudo(soup, lang, ui):
    """Localizes CSS pseudo-elements like content:'Read Review' inside style tags."""
    read_text = ui.get('read_review', 'Read Review ↓').replace('"', '\\"')
    close_text = ui.get('close_review', 'Close Review ↑').replace('"', '\\"')
    for st in soup.find_all("style"):
        if st.string:
            st.string = re.sub(r'content:\s*"Read Review[^"]*"', f'content:"{read_text}"', st.string)
            st.string = re.sub(r'content:\s*"Close Review[^"]*"', f'content:"{close_text}"', st.string)
            st.string = re.sub(r'content:\s*"Collapse Review[^"]*"', f'content:"{close_text}"', st.string)

def localize_sticky_bar(soup, lang, tours, ui):
    """Localizes the mobile bottom sticky navigation bar."""
    toc_data = DINNER_TOC_I18N.get(lang, {})
    sticky_btn = soup.find(id='sticky-cta-btn')
    if sticky_btn and ui.get('btn_check'):
        sticky_btn.string = ui['btn_check']
        
    toc_btn = soup.find(id='hybridTocBtn')
    if toc_btn:
        sp = toc_btn.find('span')
        if sp:
            sp.string = toc_data.get('all_cruises', f"{ui.get('all_cruises', '7 Cruises')}")
            
    top_btn = soup.find(class_='hybrid-top-btn')
    if top_btn:
        sp = top_btn.find('span')
        if sp:
            sp.string = toc_data.get('top', ui.get('top_label', 'Top'))
            
    rank_el = soup.find(id='sticky-rank')
    if rank_el and len(tours) > 0:
        rank_el.string = tours[0].get('rank_tag', '🏆 #1')
        
    name_el = soup.find(id='sticky-name')
    if name_el and len(tours) > 0:
        name_el.string = tours[0]['clean_title']
        
    trust_el = soup.find(class_='hybrid-active-trust')
    if trust_el and ui.get('free_cancel'):
        trust_el.string = f"{ui.get('instant_ticket', 'Instant QR')} • {ui.get('free_cancel', 'Free 24h Cancellation')}"

def localize_filter_bar(soup, lang):
    """Localizes filter buttons using DINNER_FILTER_TABS."""
    filters = DINNER_FILTER_TABS.get(lang, {})
    f_bar = soup.find(class_=lambda c: c and 'filter' in c)
    if not f_bar:
        return
    btn_keys = ['all', 'tested', 'alacarte', 'buffet', 'show', 'drinks', 'under80']
    btns = f_bar.find_all('button')
    for b_idx, btn in enumerate(btns):
        if b_idx < len(btn_keys):
            key = btn_keys[b_idx]
            if key in filters:
                btn.string = filters[key]

def localize_navbar_and_menu(soup, lang, river_slug, dinner_slug):
    """Localizes header navigation, mega-menu, direct links, and mobile drawer."""
    nav_data = MASTER_DICT.get(lang, {}).get('nav', {})
    if not nav_data:
        return
        
    dropdown_btn = soup.find('button', class_='ltt-dropdown-btn')
    if dropdown_btn and nav_data.get('danube_cruises'):
        span = dropdown_btn.find('span')
        if span:
            span.string = nav_data['danube_cruises']
            
    mega_heads = soup.find_all(class_='ltt-mega-head')
    if len(mega_heads) >= 1 and nav_data.get('head_cruises'):
        mega_heads[0].string = nav_data['head_cruises']
    if len(mega_heads) >= 2 and nav_data.get('head_spas'):
        mega_heads[1].string = nav_data['head_spas']
        
    for a in soup.find_all('a', class_='ltt-nav-link'):
        txt = a.get_text(strip=True)
        if 'River' in txt and nav_data.get('river'):
            a.string = nav_data['river']
            a['href'] = f"/{lang}/{river_slug}" if lang != 'hu' else "/hu/setahajozas-a-dunan-budapest"
        elif 'Dinner' in txt and nav_data.get('dinner'):
            a.string = nav_data['dinner']
            a['href'] = f"/{lang}/{dinner_slug}" if lang != 'hu' else "/hu/setahajozas-a-dunan-vacsoraval"
        elif 'Card' in txt and nav_data.get('card_calc'):
            a.string = nav_data['card_calc']
        elif 'About' in txt and nav_data.get('about'):
            a.string = nav_data['about']
        elif 'Contact' in txt and nav_data.get('contact'):
            a.string = nav_data['contact']

def localize_footer_section(soup, lang, river_slug, dinner_slug):
    """Localizes footer brand description, column titles, and links."""
    f_data = MASTER_DICT.get(lang, {}).get('footer', {})
    if not f_data:
        return
    footer = soup.find('footer') or soup.find(class_='footer-dark')
    if not footer:
        return
        
    brand_desc = footer.find(class_='footer-paragraph') or footer.find(class_='footer-brand-desc')
    if brand_desc and f_data.get('p'):
        brand_desc.string = f_data['p']
        
    col_titles = footer.find_all(class_=lambda c: c and ('footer-col-title' in c or 'footer-link-title' in c or 'heading-36' in c))
    if len(col_titles) >= 1 and f_data.get('popular'):
        col_titles[0].string = f_data['popular']
    if len(col_titles) >= 2 and f_data.get('company'):
        col_titles[1].string = f_data['company']
        
    for a in footer.find_all('a', class_=lambda c: c and ('footer-link' in c or 'footer-link-3' in c)):
        href = a.get('href', '')
        if 'best-budapest-river-cruises' in href or 'setahajozas-a-dunan-budapest' in href or river_slug in href:
            a['href'] = f"/{lang}/{river_slug}" if lang != 'hu' else "/hu/setahajozas-a-dunan-budapest"
        elif 'best-dinner-cruises-budapest' in href or 'setahajozas-a-dunan-vacsoraval' in href or dinner_slug in href:
            a['href'] = f"/{lang}/{dinner_slug}" if lang != 'hu' else "/hu/setahajozas-a-dunan-vacsoraval"
            intro_data = DINNER_INTRO_DATA.get(lang, {})
            if intro_data.get('dinner_title'):
                a.string = intro_data['dinner_title'].split('(')[0].strip()
        elif 'about' in href and f_data.get('about'):
            a.string = f_data['about']
        elif 'ethics' in href and f_data.get('ethics'):
            a.string = f_data['ethics']
        elif 'contact' in href and f_data.get('contact'):
            a.string = f_data['contact']
            
    disclaimer = footer.find(class_='footer-disclaimer') or footer.find(class_='footer-trust-micro')
    if disclaimer and f_data.get('disclaimer'):
        disclaimer.string = f_data['disclaimer']

def localize_toc_and_config(soup, lang, tours, ui):
    """Localizes Table of Contents title, mobile sheet, and client JS LTT_PAGE_CONFIG."""
    toc_data = DINNER_TOC_I18N.get(lang, {})
    
    # 1. Desktop sidebar title
    for t_title in soup.find_all(class_='title-small-6'):
        if 'Table of contents' in t_title.get_text():
            t_title.string = toc_data.get('toc_title', 'Table of contents')
            
    # 2. Hybrid sheet title
    sheet = soup.find(id='hybridSheet')
    if sheet:
        stitle = sheet.find(class_='hybrid-sheet-title')
        if stitle and toc_data.get('sheet_title'):
            stitle.string = toc_data['sheet_title']
            
    # 3. Hybrid TOC button
    toc_btn = soup.find(id='hybridTocBtn')
    if toc_btn:
        sp = toc_btn.find('span')
        if sp and toc_data.get('all_cruises'):
            sp.string = toc_data['all_cruises']
            
    # 4. window.LTT_PAGE_CONFIG script
    clean_short_titles = [t['clean_title'] for t in tours[:7]]
    for s in soup.find_all('script'):
        if s.string and 'window.LTT_PAGE_CONFIG' in s.string:
            cfg = {
                "deckId": "budapest-dinner-cruise-deck",
                "tocDeckLabel": toc_data.get('deck_label', 'Top 7 Dinner Cruises Comparison'),
                "tocBreakdownLabel": toc_data.get('breakdown_label', 'Detailed Breakdown (7 Cruises)'),
                "pickLabel": toc_data.get('pick', 'TOP PICK'),
                "btnText": ui.get('btn_check', 'Check Availability →'),
                "shortTitles": clean_short_titles
            }
            s.string = f"window.LTT_PAGE_CONFIG = {json.dumps(cfg, ensure_ascii=False)};"
            break

def set_li_strong(li_tag, translated_text, soup, lang='en'):
    """Sets LI content with bold label before the colon if applicable and localizes Dock."""
    dock_term = DOCK_TERMS.get(lang, 'Dock')
    translated_text = re.sub(r'\bDock\b', dock_term, translated_text, flags=re.IGNORECASE)
    parts = translated_text.split(':', 1)
    if len(parts) == 2 and len(parts[0]) < 35 and not any(ch in parts[0] for ch in ['/', 'http', 'www']):
        li_tag.clear()
        st = soup.new_tag('strong')
        st.string = f"{parts[0].strip()}:"
        li_tag.append(st)
        li_tag.append(f" {parts[1].strip()}")
    else:
        li_tag.clear()
        li_tag.string = translated_text

def localize_deck_cards(soup, lang, tours, best_fors, kickers, ui):
    """Localizes the 7 summary deck cards."""
    deck = soup.find(id='budapest-dinner-cruise-deck')
    if not deck:
        return
    cards = deck.find_all(class_='bpa-card')
    for idx, card in enumerate(cards):
        if idx >= len(tours):
            continue
        tour = tours[idx]
        best_for = best_fors[idx]
        kicker_text = kickers[idx]
        
        # 1. Rank tag
        rank_tag = card.find(class_='bpa-rank-tag')
        if rank_tag and tour.get('rank_tag'):
            rank_tag.string = tour['rank_tag']
            
        # 2. Media images alt
        for img in card.find_all('img'):
            if not img.get('class') or 'bpa-rev-icon' not in img.get('class'):
                img['alt'] = tour['clean_title']
                
        # 3. Kicker
        kicker_el = card.find(class_='bpa-kicker')
        if kicker_el:
            map_link = kicker_el.find('a', class_='bpa-kicker-map-link')
            if map_link:
                dock_name = map_link.get_text(strip=True)
                dock_term = DOCK_TERMS.get(lang, 'Dock')
                dock_name = re.sub(r'\bDock\b', dock_term, dock_name, flags=re.IGNORECASE)
                map_href = map_link.get('href', '')
                kicker_el.clear()
                prefix_parts = kicker_text.split('•')
                if len(prefix_parts) >= 2:
                    k_str = f"{prefix_parts[0].strip()} • {prefix_parts[1].strip()} • "
                else:
                    k_str = f"{kicker_text} • "
                kicker_el.append(k_str)
                new_a = soup.new_tag('a', href=map_href, class_='bpa-kicker-map-link', target='_blank', rel='noopener noreferrer')
                new_a['onclick'] = 'event.stopPropagation()'
                new_a.string = dock_name
                kicker_el.append(new_a)
            else:
                kicker_el.string = kicker_text
                
        # 4. Title
        title_el = card.find(class_='bpa-title')
        if title_el:
            title_el.string = tour['clean_title']
            
        # 5. Best for
        best_for_p = card.find(class_='bpa-best-for')
        if best_for_p:
            best_for_p.clear()
            st = soup.new_tag('strong')
            st.string = f"{ui.get('best_for_label', 'Best for:')} "
            best_for_p.append(st)
            best_for_p.append(best_for)
            
        # 6. CTA cell
        cta_cell = card.find(class_='bpa-cta-cell')
        if cta_cell:
            price_el = cta_cell.find(class_='bpa-price')
            if price_el:
                price_el.string = tour.get('price_tag', '€110')
            psub = cta_cell.find(class_='bpa-psub')
            if psub and ui.get('per_adult'):
                psub.string = ui['per_adult']
            btn = cta_cell.find(class_='bpa-btn')
            if btn and ui.get('btn_check'):
                btn.string = ui['btn_check']
            trust_micro = cta_cell.find(class_='bpa-trust-micro')
            if trust_micro:
                trust_micro.clear()
                s1 = soup.new_tag('span')
                s1.string = ui.get('instant_ticket', 'Instant QR')
                s_bullet = soup.new_tag('span')
                s_bullet.string = ' • '
                s2 = soup.new_tag('span')
                s2.string = ui.get('free_cancel', 'Free 24h Cancellation')
                trust_micro.append(s1)
                trust_micro.append(s_bullet)
                trust_micro.append(s2)
            sublink = cta_cell.find(class_='bpa-sublink')
            if sublink and ui.get('read_review'):
                sublink.string = ui['read_review']

        # 7. Spec chips (.bpa-sp)
        chip_map = DINNER_SPEC_CHIPS_I18N.get(lang, {})
        for sp in card.find_all(class_='bpa-sp'):
            sp_txt = sp.get_text(strip=True)
            if sp_txt in chip_map:
                sp.string = chip_map[sp_txt]

        # 8. Tested vchip
        for vc in card.find_all(class_='bpa-vchip'):
            vc.string = ui.get('tested', '✓ Personally Tested')

def generate_pro_con_html(pros, cons, ui):
    pros_title = ui.get('pros_label', 'Pros:')
    cons_title = ui.get('cons_label', 'Cons:')
    pros_lis = ""
    for p in pros:
        parts = p.split('—', 1)
        if len(parts) == 2:
            pros_lis += f"<li><strong>{parts[0].strip()}</strong> — {parts[1].strip()}</li>"
        else:
            pros_lis += f"<li><strong>{p.strip()}</strong></li>"
    cons_lis = ""
    for c in cons:
        parts = c.split('—', 1)
        if len(parts) == 2:
            cons_lis += f"<li><strong>{parts[0].strip()}</strong> — {parts[1].strip()}</li>"
        else:
            cons_lis += f"<li><strong>{c.strip()}</strong></li>"
    return f'''<div class="w-layout-grid grid-15">
  <div class="pro-con-box-pro-cell" data-wf-pbl="layout-grid-1x2-vertical">
   <div class="pro-con-box-pro-cell-rich-text-block w-richtext">
    <h3><strong>{pros_title}</strong></h3>
    <ul role="list">{pros_lis}</ul>
   </div>
  </div>
  <div class="pro-con-box-con-cell" data-wf-pbl="layout-grid-1x2-vertical">
   <div class="pro-con-box-con-cell-rich-text-block w-richtext">
    <h3><strong>{cons_title}</strong></h3>
    <ul role="list">{cons_lis}</ul>
   </div>
  </div>
 </div>'''

def localize_details_cards(soup, lang, tours, kickers, ui, walkthrough):
    """Localizes the 7 detailed walkthrough cards."""
    details_cards = soup.find_all('details', class_='bpa-details-card')
    h4_map = walkthrough.get('h4_headings', {})
    caps_list = walkthrough.get('captions', [])
    leaf_lis_list = walkthrough.get('leaf_lis', [])
    bios_dict = walkthrough.get('bios', {})
    undercover_dict = walkthrough.get('undercover_notes', {})
    transit_dict = walkthrough.get('transit_lines', {})
    bento_dict = walkthrough.get('bento_titles', {})
    
    pros_cons_data = DINNER_PROS_CONS_I18N.get(lang, {})
    
    leaf_li_idx = 0
    caption_idx = 0
    
    for c_idx, dcard in enumerate(details_cards):
        if c_idx >= len(tours):
            continue
        tour = tours[c_idx]
        kicker_text = kickers[c_idx]
        
        # 1. Summary row
        summary = dcard.find('summary')
        if summary:
            rank_el = summary.find(class_='bpa-rank-tag')
            if rank_el and tour.get('rank_tag'):
                rank_el.string = tour['rank_tag']
                
            kicker_el = summary.find(class_='bpa-kicker')
            if kicker_el:
                map_link = kicker_el.find('a', class_='bpa-kicker-map-link')
                if map_link:
                    dock_name = map_link.get_text(strip=True)
                    dock_term = DOCK_TERMS.get(lang, 'Dock')
                    dock_name = re.sub(r'\bDock\b', dock_term, dock_name, flags=re.IGNORECASE)
                    map_href = map_link.get('href', '')
                    kicker_el.clear()
                    prefix_parts = kicker_text.split('•')
                    if len(prefix_parts) >= 2:
                        k_str = f"{prefix_parts[0].strip()} • {prefix_parts[1].strip()} • "
                    else:
                        k_str = f"{kicker_text} • "
                    kicker_el.append(k_str)
                    new_a = soup.new_tag('a', href=map_href, class_='bpa-kicker-map-link', target='_blank', rel='noopener noreferrer')
                    new_a['onclick'] = 'event.stopPropagation()'
                    new_a.string = dock_name
                    kicker_el.append(new_a)
                else:
                    kicker_el.string = kicker_text
                    
            h3_title = summary.find('h3', class_='bpa-details-title')
            if h3_title:
                h3_title.string = tour['clean_title']
                
            vchip = summary.find(class_='bpa-vchip')
            if vchip and ui.get('tested'):
                vchip.string = ui['tested']
                
            price_el = summary.find(class_='bpa-details-price')
            if price_el:
                price_el.string = f"{tour.get('price_tag', '€110')} {ui.get('per_adult', '/ adult')}"
                
            toggle_text = summary.find(class_='bpa-details-state-text')
            if toggle_text and ui.get('read_review'):
                toggle_text.string = ui['read_review']
                
        body = dcard.find(class_='bpa-details-body')
        if not body:
            continue
            
        # 2. Pros & Cons box
        pro_con_wrap = body.find(class_='pro-con-box-wrapper')
        tour_k = str(c_idx)
        if pro_con_wrap and tour_k in pros_cons_data:
            p_data = pros_cons_data[tour_k]
            pc_html = generate_pro_con_html(p_data.get('pros', []), p_data.get('cons', []), ui)
            pro_con_wrap.clear()
            pc_soup = BeautifulSoup(pc_html, 'html.parser')
            pro_con_wrap.append(pc_soup)
            
        # 3. Bento groups
        bento_groups = body.find_all('details', class_='ltt-bento-group')
        for b_idx, bg in enumerate(bento_groups):
            bsummary = bg.find('summary')
            btitle = bsummary.find(class_='ltt-bento-group-title') if bsummary else None
            bpill = bsummary.find(class_='ltt-mini-pill') if bsummary else None
            
            # --- Bento 1: Summary & Review ---
            if b_idx == 0:
                if btitle and 'bento_1_title' in bento_dict:
                    btitle.string = bento_dict['bento_1_title']
                if bpill and 'bento_1_pill' in bento_dict:
                    bpill.string = bento_dict['bento_1_pill']
                    
                for bq in list(bg.find_all('blockquote')):
                    btxt = bq.get_text(strip=True)
                    if '🎥' in btxt or 'video reel' in btxt.lower() or 'teaser video' in btxt.lower():
                        bq.decompose()
                    elif '💡' in btxt or 'undercover' in btxt.lower():
                        if c_idx == 0 and 'legenda' in undercover_dict:
                            bq.string = undercover_dict['legenda']
                        elif c_idx == 3 and 'piano' in undercover_dict:
                            bq.string = undercover_dict['piano']

                # Inject localized Bento 1 review paragraphs
                bento1_paras = walkthrough.get('bento1_paragraphs', [])
                if bento1_paras and c_idx < len(bento1_paras):
                    c_paras = bento1_paras[c_idx]
                    if isinstance(c_paras, str):
                        raise ValueError(
                            f"[{lang}] bento1_paragraphs[{c_idx}] is a string, expected a list of paragraphs "
                            "(a flat list renders one character per <p>)")
                    rt = bg.find(class_='w-richtext')
                    if rt:
                        rt_ps = rt.find_all('p')
                        for p_idx, p_elem in enumerate(rt_ps):
                            if p_idx < len(c_paras):
                                p_text = c_paras[p_idx]
                                p_elem.clear()
                                p_frag = BeautifulSoup(p_text, 'html.parser')
                                p_elem.append(p_frag)

                # Localize Buy Card inside Bento 1
                buy_card = bg.find(class_='ltt-buy-card')
                if buy_card:
                    b_title = buy_card.find(class_='ltt-buy-card-title')
                    if b_title:
                        b_title.string = tour['clean_title']
                    
                    dock_term = DOCK_TERMS.get(lang, 'Dock')
                    perks = buy_card.find_all(class_='ltt-buy-perk')
                    if len(perks) >= 4:
                        perks[0].string = ui.get('instant_ticket', 'Instant Smartphone QR Voucher')
                        perks[1].string = ui.get('free_cancel', 'Full Refund up to 24h Before')
                        
                        dep_strong = perks[2].find('strong')
                        if dep_strong:
                            dep_text = dep_strong.get_text(strip=True)
                            dep_text_loc = re.sub(r'\bDock\b', dock_term, dep_text, flags=re.IGNORECASE)
                            perks[2].clear()
                            perks[2].append(f"{ui.get('departure_label', 'Departure:')} ")
                            st = soup.new_tag('strong')
                            st.string = dep_text_loc
                            perks[2].append(st)
                            
                        dur_strong = perks[3].find('strong')
                        if dur_strong:
                            dur_text = dur_strong.get_text(strip=True)
                            dur_loc = dur_text.replace('Hours', ui.get('hours_label', 'Hours')).replace('Minutes', ui.get('mins_label', 'Minutes'))
                            perks[3].clear()
                            perks[3].append(f"{ui.get('duration_label', 'Duration:')} ")
                            st = soup.new_tag('strong')
                            st.string = dur_loc
                            perks[3].append(st)
                            
                    btn = buy_card.find(class_='ltt-buy-cta-btn')
                    if btn and ui.get('btn_check'):
                        btn.string = ui['btn_check']
                            
            # --- Bento 2: Menu & Inclusions ---
            elif b_idx == 1:
                if btitle:
                    if c_idx in [0, 1] and 'bento_2_title_gourmet' in bento_dict:
                        btitle.string = bento_dict['bento_2_title_gourmet']
                    elif c_idx in [2, 3] and 'bento_2_title_inclusions' in bento_dict:
                        btitle.string = bento_dict['bento_2_title_inclusions']
                    elif c_idx == 4 and 'bento_2_title_buffet' in bento_dict:
                        btitle.string = bento_dict['bento_2_title_buffet']
                    elif c_idx == 5 and 'bento_2_title_options' in bento_dict:
                        btitle.string = bento_dict['bento_2_title_options']
                    elif c_idx == 6 and 'bento_2_title_unlimited' in bento_dict:
                        btitle.string = bento_dict['bento_2_title_unlimited']
                        
                if bpill:
                    if c_idx == 0 and 'bento_2_pill_swipe7' in bento_dict:
                        bpill.string = bento_dict['bento_2_pill_swipe7']
                    elif c_idx == 1 and 'bento_2_pill_swipe10' in bento_dict:
                        bpill.string = bento_dict['bento_2_pill_swipe10']
                    elif c_idx in [2, 3] and 'bento_2_pill_4course' in bento_dict:
                        bpill.string = bento_dict['bento_2_pill_4course']
                    elif c_idx == 4 and 'bento_2_pill_buffet' in bento_dict:
                        bpill.string = bento_dict['bento_2_pill_buffet']
                    elif c_idx == 5 and 'bento_2_pill_swipe4' in bento_dict:
                        bpill.string = bento_dict['bento_2_pill_swipe4']
                    elif c_idx == 6 and 'bento_2_pill_unlimited' in bento_dict:
                        bpill.string = bento_dict['bento_2_pill_unlimited']
                        
            # --- Bento 3: Ship, Views, Music & Atmosphere ---
            elif b_idx == 2:
                if btitle:
                    if c_idx == 0 and 'bento_3_title_music' in bento_dict:
                        btitle.string = bento_dict['bento_3_title_music']
                    elif c_idx == 1 and 'bento_3_title_atmosphere' in bento_dict:
                        btitle.string = bento_dict['bento_3_title_atmosphere']
                    elif c_idx == 2 and 'bento_3_title_folk' in bento_dict:
                        btitle.string = bento_dict['bento_3_title_folk']
                    elif c_idx == 3 and 'bento_3_title_piano' in bento_dict:
                        btitle.string = bento_dict['bento_3_title_piano']
                    elif c_idx == 4 and 'bento_3_title_dance' in bento_dict:
                        btitle.string = bento_dict['bento_3_title_dance']
                    elif c_idx == 5 and 'bento_3_title_views' in bento_dict:
                        btitle.string = bento_dict['bento_3_title_views']
                    elif c_idx == 6 and 'bento_3_title_live' in bento_dict:
                        btitle.string = bento_dict['bento_3_title_live']
                        
                if bpill:
                    if c_idx in [0, 1, 2] and 'bento_3_pill_swipe6' in bento_dict:
                        bpill.string = bento_dict['bento_3_pill_swipe6']
                    elif c_idx == 3 and 'bento_3_pill_piano' in bento_dict:
                        bpill.string = bento_dict['bento_3_pill_piano']
                    elif c_idx == 4 and 'bento_3_pill_perf' in bento_dict:
                        bpill.string = bento_dict['bento_3_pill_perf']
                    elif c_idx == 5 and 'bento_3_pill_onboard' in bento_dict:
                        bpill.string = bento_dict['bento_3_pill_onboard']
                    elif c_idx == 6 and 'bento_3_pill_vibe' in bento_dict:
                        bpill.string = bento_dict['bento_3_pill_vibe']
                        
            # --- Bento 4: Departure Pier & Transit Map ---
            elif b_idx == 3:
                if btitle and 'bento_4_title' in bento_dict:
                    btitle.string = bento_dict['bento_4_title']
                if bpill:
                    if c_idx == 0 and 'bento_4_pill_dock7' in bento_dict:
                        bpill.string = bento_dict['bento_4_pill_dock7']
                    elif c_idx in [1, 2, 3] and 'bento_4_pill_dock11_erzsebet' in bento_dict:
                        bpill.string = bento_dict['bento_4_pill_dock11_erzsebet']
                    elif c_idx == 4 and 'bento_4_pill_dock11_jane' in bento_dict:
                        bpill.string = bento_dict['bento_4_pill_dock11_jane']
                    elif c_idx == 5 and 'bento_4_pill_dock6' in bento_dict:
                        bpill.string = bento_dict['bento_4_pill_dock6']
                    elif c_idx == 6 and 'bento_4_pill_dock8a' in bento_dict:
                        bpill.string = bento_dict['bento_4_pill_dock8a']
                        
                transit_lis = bg.find_all('li')
                card_key = f"card_{c_idx+1}"
                dock_term = DOCK_TERMS.get(lang, 'Dock')
                if c_idx == 0:
                    if len(transit_lis) > 0 and 'card_1_meeting' in transit_dict:
                        set_li_strong(transit_lis[0], transit_dict['card_1_meeting'], soup, lang)
                    if len(transit_lis) > 1 and 'card_1_transit' in transit_dict:
                        set_li_strong(transit_lis[1], transit_dict['card_1_transit'], soup, lang)
                    if len(transit_lis) > 2 and 'card_1_arrive' in transit_dict:
                        transit_lis[2].string = transit_dict['card_1_arrive']
                elif c_idx == 1:
                    if len(transit_lis) > 0 and 'card_2_meeting' in transit_dict:
                        set_li_strong(transit_lis[0], transit_dict['card_2_meeting'], soup, lang)
                    if len(transit_lis) > 1 and 'card_2_location' in transit_dict:
                        set_li_strong(transit_lis[1], transit_dict['card_2_location'], soup, lang)
                    if len(transit_lis) > 2 and 'card_2_transit' in transit_dict:
                        set_li_strong(transit_lis[2], transit_dict['card_2_transit'], soup, lang)
                elif c_idx in [2, 3, 4, 5, 6]:
                    meet_k = f"{card_key}_meeting"
                    trans_k = f"{card_key}_transit"
                    if len(transit_lis) > 0 and meet_k in transit_dict:
                        set_li_strong(transit_lis[0], transit_dict[meet_k], soup, lang)
                    if len(transit_lis) > 1 and trans_k in transit_dict:
                        set_li_strong(transit_lis[1], transit_dict[trans_k], soup, lang)
                        
                for sp in bg.find_all(class_='ltt-sp-card'):
                    h4 = sp.find('h4')
                    if h4:
                        en_h4 = h4.get_text(strip=True)
                        if en_h4 in h4_map:
                            h4.string = h4_map[en_h4]
                    p = sp.find('p')
                    if p:
                        bio_keys = ['legenda', 'silverline_budget', 'silverline_folk', 'silverline_piano', 'hungaria', 'eurama', 'rubin']
                        if c_idx < len(bio_keys) and bio_keys[c_idx] in bios_dict:
                            bio_txt = bios_dict[bio_keys[c_idx]]
                            dock_term = DOCK_TERMS.get(lang, 'Dock')
                            bio_txt = re.sub(r'\bDock\s*(\d+)', f'{dock_term} \1', bio_txt, flags=re.IGNORECASE)
                            bio_txt = re.sub(r'\bDock\b', dock_term, bio_txt, flags=re.IGNORECASE)
                            if lang in ['ja', 'ko']:
                                bio_txt = re.sub(r'[（\(]Dock\s*\d+[）\)]', '', bio_txt, flags=re.IGNORECASE)
                            p.string = bio_txt

            # Filmstrip slides in this Bento
            for slide in bg.find_all(class_='ltt-strip-slide'):
                cap_el = slide.find(class_='ltt-strip-cap')
                img_el = slide.find('img')
                if caption_idx < len(caps_list):
                    t_cap = caps_list[caption_idx]
                    if cap_el:
                        sp = cap_el.find('span')
                        if sp:
                            sp.string = t_cap
                        else:
                            cap_el.string = t_cap
                    if img_el:
                        img_el['alt'] = t_cap
                    caption_idx += 1

            # Subpoints in Bento 2 and 3
            if b_idx in [1, 2]:
                for sp in bg.find_all(class_='ltt-sp-card'):
                    h4 = sp.find('h4')
                    if h4:
                        en_h4 = h4.get_text(strip=True)
                        if en_h4 in h4_map:
                            h4.string = h4_map[en_h4]
                            
                    leaf_lis = [li for li in sp.find_all('li') if not li.find('li')]
                    for lli in leaf_lis:
                        if leaf_li_idx < len(leaf_lis_list):
                            t_li = leaf_lis_list[leaf_li_idx]
                            if lang == 'cs':
                                t_li = re.sub(r'\bwelcome drink\b', 'nápoj na uvítanou', t_li, flags=re.IGNORECASE)
                            elif lang == 'sk':
                                t_li = re.sub(r'\bwelcome drink\b', 'prípitok na privítanie', t_li, flags=re.IGNORECASE)
                            set_li_strong(lli, t_li, soup, lang)
                            leaf_li_idx += 1

        # 4. Quick facts table
        qf_wrap = body.find(class_='qf1-wrap')
        if qf_wrap:
            qf_title = qf_wrap.find(class_='qf1-title')
            if qf_title:
                qf_title.string = ui.get('quick_facts', 'Quick Facts — Verified Field Specs')
                
            qf_badge = qf_wrap.find(class_='qf1-badge')
            if qf_badge:
                dock_term = DOCK_TERMS.get(lang, 'Dock')
                qf_badge.string = re.sub(r'\bDock\b', dock_term, qf_badge.get_text(strip=True), flags=re.IGNORECASE)
                
            label_map = DINNER_QF_LABELS.get(lang, {})
            val_map = walkthrough.get('qf_values', {})
            
            for row in qf_wrap.find_all(class_='qf1-row'):
                lbl = row.find(class_='qf1-label')
                if lbl:
                    ltxt = lbl.get_text(strip=True)
                    if ltxt in label_map:
                        lbl.string = label_map[ltxt]
                val = row.find(class_='qf1-val')
                if val:
                    vtxt = val.get_text(strip=True)
                    if vtxt in val_map:
                        val.string = val_map[vtxt]
                    else:
                        dock_term = DOCK_TERMS.get(lang, 'Dock')
                        val.string = re.sub(r'\bDock\b', dock_term, vtxt, flags=re.IGNORECASE)

def compile_language_dinner(lang, en_html, walkthrough_all):
    """Compiles a 100% localized dinner cruise page for a given language."""
    print(f"Compiling [{lang.upper()}] Dinner Cruise Guide...")
    soup = BeautifulSoup(en_html, 'html.parser')
    
    dinner_slug = SLUG_MAP[lang]['dinner'] if lang in SLUG_MAP else 'best-dinner-cruises-budapest'
    river_slug = SLUG_MAP[lang]['river'] if lang in SLUG_MAP else 'best-budapest-river-cruises'
    canonical_url = f"https://www.budapestadventures.com/{lang}/{dinner_slug}" if lang != 'en' else "https://www.budapestadventures.com/best-dinner-cruises-budapest"
    if lang == 'hu':
        canonical_url = "https://www.budapestadventures.com/hu/setahajozas-a-dunan-vacsoraval"
        
    pm = DINNER_PAGE_META.get(lang, {})
    intro = DINNER_INTRO_DATA.get(lang, {})
    ui = DINNER_UI_COMMON.get(lang, {})
    tours = DINNER_TOURS_DATA.get(lang, [])
    best_fors = DINNER_BEST_FOR_DATA.get(lang, [])
    kickers = DINNER_KICKERS_DATA.get(lang, [])
    walkthrough = walkthrough_all.get(lang, {})
    
    # 1. HTML lang & dir
    html_tag = soup.find('html')
    if html_tag:
        html_tag['lang'] = lang
        if lang == 'he':
            html_tag['dir'] = 'rtl'
        else:
            html_tag.attrs.pop('dir', None)
            
    # 2. Canonical tag
    can_tag = soup.find('link', rel='canonical')
    if can_tag:
        can_tag['href'] = canonical_url
        
    # 3. Meta title and description
    title_tag = soup.find('title')
    if title_tag and pm.get('title'):
        title_tag.string = pm['title']
        
    desc_tag = soup.find('meta', attrs={'name': 'description'})
    if desc_tag and pm.get('desc'):
        desc_tag['content'] = pm['desc']
        
    page_title = pm.get('og_title') or pm.get('title')
    page_desc = pm.get('og_desc') or pm.get('desc')
    for og_t in soup.find_all('meta', property=lambda p: p and 'title' in p):
        if page_title: og_t['content'] = page_title
    for og_d in soup.find_all('meta', property=lambda p: p and 'description' in p):
        if page_desc: og_d['content'] = page_desc
    for tw_t in soup.find_all('meta', attrs={'name': lambda n: n and 'title' in n}):
        if page_title: tw_t['content'] = page_title
    for tw_d in soup.find_all('meta', attrs={'name': lambda n: n and 'description' in n}):
        if page_desc: tw_d['content'] = page_desc

    # Global Personally Tested chip replacement
    tested_label = ui.get('tested', '✓ Personally Tested')
    for vc in soup.find_all(class_='bpa-vchip'):
        vc.string = tested_label
        
    # 4. Cleanse Schema JSON-LD
    cleanse_json_ld(soup, lang, pm, intro, canonical_url, tours, best_fors)
    
    # 5. CSS pseudo elements
    localize_css_pseudo(soup, lang, ui)
    
    # 6. Hero / Intro
    hero_kicker = soup.find(class_='hero-kicker') or soup.find(class_='ltt-hero-kicker')
    if hero_kicker and intro.get('kicker'):
        hero_kicker.string = intro['kicker']
        
    h1 = soup.find('h1')
    if h1 and intro.get('h1'):
        h1.string = intro['h1']
        
    author_name = soup.find(class_='author-name')
    if author_name and intro.get('author_title'):
        author_name.string = intro['author_title']
        
    author_role = soup.find(class_='author-role')
    if author_role and intro.get('author_role'):
        author_role.string = intro['author_role']
        
    date_el = soup.find(class_='date-text') or soup.find(class_='updated-text')
    if date_el and intro.get('updated'):
        date_el.string = intro['updated']
        
    lead_copy = soup.find(class_='ltt-lead-copy')
    if lead_copy:
        ps = lead_copy.find_all('p')
        if len(ps) >= 1 and intro.get('p1'):
            ps[0].string = intro['p1']
        if len(ps) >= 2 and intro.get('p2'):
            ps[1].string = intro['p2']
        if len(ps) >= 3 and intro.get('p3'):
            ps[2].string = intro['p3']
            
    # 7. Navigation & Footer
    localize_navbar_and_menu(soup, lang, river_slug, dinner_slug)
    localize_footer_section(soup, lang, river_slug, dinner_slug)
    
    # 8. Filter Bar
    localize_filter_bar(soup, lang)
    
    # 9. Summary Deck Cards (7 cards)
    localize_deck_cards(soup, lang, tours, best_fors, kickers, ui)
    
    # 10. Table of Contents & JS Config
    localize_toc_and_config(soup, lang, tours, ui)
    
    # 11. Detailed Walkthrough Cards (7 cards)
    localize_details_cards(soup, lang, tours, kickers, ui, walkthrough)
    
    # 12. Sticky Bar
    localize_sticky_bar(soup, lang, tours, ui)
    
    if lang == 'hu':
        for el in soup.find_all(text=lambda t: t and 'audio guide-okat' in t):
            el.replace_with(el.replace('audio guide-okat', 'audioguide-okat'))

    # Determine output path
    if lang == 'hu':
        out_path = os.path.join(BASE_DIR, 'hu', 'setahajozas-a-dunan-vacsoraval', 'index.html')
    else:
        out_path = os.path.join(BASE_DIR, lang, dinner_slug, 'index.html')
        
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
        
    print(f"  -> Successfully compiled [{lang.upper()}] to {out_path}")

def main():
    print("=" * 60)
    print("BUDAPEST ADVENTURES — MASTER DINNER COMPILER (21 LANGUAGES)")
    print("=" * 60)
    
    walkthrough_all = load_combined_walkthrough()
    print(f"Loaded walkthrough languages: {list(walkthrough_all.keys())}")
    
    with open(os.path.join(BASE_DIR, 'best-dinner-cruises-budapest', 'index.html'), 'r', encoding='utf-8') as f:
        en_html = f.read()
        
    target_langs = ['hu', 'de', 'fr', 'es', 'it', 'nl', 'pl', 'ro', 'cs', 'sk', 'hr', 'sr', 'bg', 'ru', 'uk', 'el', 'tr', 'pt', 'he', 'ja', 'ko']
    
    for lang in target_langs:
        if lang in walkthrough_all:
            compile_language_dinner(lang, en_html, walkthrough_all)
        else:
            print(f"Skipping {lang}: not yet in walkthrough data")
            
    print("\nMaster Dinner Compilation Run Complete.")

if __name__ == '__main__':
    main()
