#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MASTER RIVER MULTILINGUAL COMPILER — BUDAPEST ADVENTURES
Compiles 100% authentic, fully translated river cruise pages across all 20 foreign languages:
DE, FR, ES, IT, NL, PL, RO, CS, SK, HR, SR, BG, RU, UK, EL, TR, PT, HE, JA, KO.
Also updates canonical English and Hungarian pages with the Dutch hreflang tag.
"""

import os
import sys
import re
import json
from bs4 import BeautifulSoup

BASE_DIR = '/Users/adamdimitrov/Development/budapest-adventures'
sys.path.insert(0, os.path.join(BASE_DIR, 'scripts'))

from river_i18n_master_data import (
    PAGE_META,
    AUTHOR_DATA,
    INTRO_DATA,
    FILTER_TABS_DATA,
    UI_COMMON,
    BEST_FOR_DATA,
    BREAKDOWN_HEADERS,
    RANK_BADGES
)
from subpoint_headings_i18n import SUBPOINT_HEADINGS
from i18n_translation_data import BUY_CARD_I18N
from compile_all_languages_luxury import extract_tour_content, SLUG_MAP
from quick_facts_i18n import QF_TITLES, QF_LABELS, QF_CHIPS, KICKER_UNITS
from spec_chips_i18n import SPEC_CHIPS_I18N
from river_pros_cons_expanded_i18n import EXPANDED_PROS_CONS_I18N

from river_walkthrough_data_i18n import (
    TOC_I18N,
    TIPS_EXTENDED_I18N,
    MISSING_7_LIS_I18N,
    ABOUT_PARAGRAPHS_I18N,
    SHIP_CAPTIONS_I18N,
    CARD_LEAF_INDEX_MAP
)

MASTER_DICT_PATH = os.path.join(BASE_DIR, 'data', 'i18n_master_dictionary.json')
MASTER_DICT = json.load(open(MASTER_DICT_PATH, encoding='utf-8')) if os.path.exists(MASTER_DICT_PATH) else {}

NL_HREFLANG_TAG = '<link href="https://www.budapestadventures.com/nl/beste-boedapest-riviercruises" hreflang="nl" rel="alternate"/>'

def ensure_nl_hreflang(soup):
    """Ensures hreflang='nl' is present in head alternate links."""
    existing_nl = soup.find('link', rel='alternate', hreflang='nl')
    if not existing_nl:
        nl_link = soup.new_tag('link', rel='alternate', hreflang='nl', href='https://www.budapestadventures.com/nl/beste-boedapest-riviercruises')
        hu_alt = soup.find('link', rel='alternate', hreflang='hu')
        if hu_alt:
            hu_alt.insert_before(nl_link)
        else:
            first_alt = soup.find('link', rel='alternate')
            if first_alt:
                first_alt.insert_before(nl_link)
            elif soup.head:
                soup.head.append(nl_link)

def cleanse_json_ld(soup, lang, pm, intro, canonical_url, tours=None, best_fors=None):
    """Cleanse all English leftovers from JSON-LD Schema objects."""
    if tours is None: tours = []
    if best_fors is None: best_fors = []
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
                                    b_item['item'] = f"https://www.budapestadventures.com/{lang}"
                                elif b_idx == 1:
                                    b_item['name'] = pm.get('bc_curr', 'River Cruises')
                                    b_item['item'] = canonical_url
                                elif b_idx == 2:
                                    b_item['name'] = pm.get('title', 'River Cruises')
                                    b_item['item'] = canonical_url
                    if '@id' in item:
                        item['@id'] = item['@id'].replace('https://www.budapestadventures.com/best-budapest-river-cruises', canonical_url)
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

def localize_sticky_bar(soup, lang, tours, buy_card_data, ui, rank_badges):
    """Localizes the mobile bottom sticky navigation bar."""
    toc_data = TOC_I18N.get(lang, {})
    sticky_btn = soup.find(id='sticky-cta-btn')
    if sticky_btn and ui.get('btn_check'):
        sticky_btn.string = ui['btn_check']
        
    toc_btn = soup.find(id='hybridTocBtn')
    if toc_btn:
        sp = toc_btn.find('span')
        if sp:
            sp.string = toc_data.get('all_cruises', f"{ui.get('overview', '10 Cruises')}")
            
    top_btn = soup.find(class_='hybrid-top-btn')
    if top_btn:
        sp = top_btn.find('span')
        if sp:
            sp.string = toc_data.get('top', ui.get('top_label', 'Top'))
            
    rank_el = soup.find(id='sticky-rank')
    if rank_el and len(rank_badges) > 0:
        rank_el.string = rank_badges[0]
        
    name_el = soup.find(id='sticky-name')
    if name_el and len(tours) > 0:
        name_el.string = tours[0]['clean_title']
        
    trust_el = soup.find(class_='hybrid-active-trust')
    if trust_el and buy_card_data.get('refund'):
        trust_el.string = buy_card_data['refund']

def localize_specs_row(soup, lang, ui):
    """Localizes spec pills in bpa-specs-row across all cards."""
    chips_dict = SPEC_CHIPS_I18N.get(lang, {})
    for row in soup.find_all(class_='bpa-specs-row'):
        for sp in row.find_all('span'):
            txt = sp.get_text(strip=True)
            if txt in chips_dict:
                sp.string = chips_dict[txt]
            elif 'Tested' in txt and ui.get('tested'):
                sp.string = ui['tested']

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
            a['href'] = f"/{lang}/{river_slug}"
        elif 'Dinner' in txt and nav_data.get('dinner'):
            a.string = nav_data['dinner']
            a['href'] = f"/{lang}/{dinner_slug}"
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
            a['href'] = f"/{lang}/{river_slug}"
            pm_data = PAGE_META.get(lang, {})
            if pm_data.get('title'):
                a.string = pm_data['title'].split('(')[0].strip()
        elif 'best-dinner-cruises-budapest' in href or 'setahajozas-a-dunan-vacsoraval' in href or dinner_slug in href:
            a['href'] = f"/{lang}/{dinner_slug}"
            intro_data = INTRO_DATA.get(lang, {})
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
    toc_data = TOC_I18N.get(lang, {})
    
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
    clean_short_titles = [t['clean_title'] for t in tours[:10]]
    for s in soup.find_all('script'):
        if s.string and 'window.LTT_PAGE_CONFIG' in s.string:
            cfg = {
                "deckId": "budapest-river-cruise-deck",
                "tocDeckLabel": toc_data.get('deck_label', 'Top 10 Cruises Comparison'),
                "tocBreakdownLabel": toc_data.get('breakdown_label', 'Detailed Breakdown (10 Cruises)'),
                "pickLabel": toc_data.get('pick', 'PICK'),
                "btnText": ui.get('btn_check', 'Check Availability →'),
                "shortTitles": clean_short_titles
            }
            s.string = f"window.LTT_PAGE_CONFIG = {json.dumps(cfg, ensure_ascii=False)};"
            break

def localize_all_blockquotes(soup, lang, ui):
    """Translates all tips/blockquotes and eliminates stray FAQ/video blockquotes."""
    tips_data = TIPS_EXTENDED_I18N.get(lang, {})
    tip_prefix = ui.get('tip_label', '💡 Tip: ')
    
    for bq in list(soup.find_all('blockquote')):
        btxt = bq.get_text(strip=True)
        if 'All cruises have a generous cancellation policy' in btxt or 'generous cancellation' in btxt.lower():
            bq.clear()
            bq.append(f"{tip_prefix}{tips_data.get('cancellation', '')}")
        elif 'best sightseeing and photo opportunities' in btxt or 'photo opportunities' in btxt.lower():
            bq.clear()
            bq.append(f"{tip_prefix}{tips_data.get('deck_view', '')}")
        elif 'loudspeaker audio' in btxt.lower() or 'All the other cruises offer loudspeaker' in btxt:
            bq.clear()
            bq.append(f"{tip_prefix}{tips_data.get('headphones', '')}")
        elif 'best open air seats go fast' in btxt or '15–20 minutes' in btxt:
            bq.clear()
            bq.append(f"{tip_prefix}{tips_data.get('arrival', '')}")
        elif 'share the same boat' in btxt.lower() or 'Pizza & Beer cruise and an Unlimited Drink cruise' in btxt:
            bq.clear()
            bq.append(f"{tip_prefix}{tips_data.get('silverline_shared', '')}")
        elif '❓' in btxt and any(q in btxt for q in ['buying food', 'Should I book', 'possible to reserve']):
            bq.decompose()
        elif '🎥' in btxt or 'Virtual tour:' in btxt:
            bq.decompose()

def localize_walkthrough_subpoints(soup, lang, harvested_lis, harvested_li_tags):
    """Deterministically translates all 10 cards' subpoint headings, leaf LIs, bios, and captions."""
    sub_headings = SUBPOINT_HEADINGS.get(lang, {})
    missing_lis = MISSING_7_LIS_I18N.get(lang, {})
    about_bios = ABOUT_PARAGRAPHS_I18N.get(lang, {})
    captions = SHIP_CAPTIONS_I18N.get(lang, {})
    
    details_cards = soup.find_all('details', class_='bpa-details-card')
    
    for c_idx, dcard in enumerate(details_cards):
        if c_idx not in CARD_LEAF_INDEX_MAP:
            continue
        card_map = CARD_LEAF_INDEX_MAP[c_idx]
        
        for sp in dcard.find_all(class_='ltt-sp-card'):
            h4 = sp.find('h4')
            en_h4 = h4.get_text(strip=True) if h4 else ''
            
            # 1. Translate H4 heading
            if h4 and en_h4 in sub_headings:
                h4.string = sub_headings[en_h4]
                
            # 2. Translate leaf LIs
            if en_h4 in card_map:
                indices = card_map[en_h4]
                leaf_lis = [li for li in sp.find_all('li') if not li.find('li')]
                for l_idx, harv_idx in enumerate(indices):
                    if l_idx < len(leaf_lis):
                        target_li = leaf_lis[l_idx]
                        if harv_idx in missing_lis:
                            translated_text = missing_lis[harv_idx]
                        elif harv_idx < len(harvested_lis):
                            translated_text = harvested_lis[harv_idx]
                        else:
                            translated_text = None
                            
                        if translated_text:
                            parts = translated_text.split(':', 1)
                            if len(parts) == 2 and len(parts[0]) < 25 and not any(ch in parts[0] for ch in ['/', 'http']):
                                target_li.clear()
                                st = soup.new_tag('strong')
                                st.string = f"{parts[0].strip()}:"
                                target_li.append(st)
                                target_li.append(f" {parts[1].strip()}")
                            else:
                                target_li.clear()
                                target_li.string = translated_text
                            
                # Special handling for Card 1 The Ship(s) intro parent li
                if c_idx == 0 and en_h4 == 'The Ship(s)':
                    first_ul = sp.find('ul')
                    if first_ul:
                        parent_li = first_ul.find('li')
                        if parent_li:
                            nested_ul = parent_li.find('ul')
                            if nested_ul:
                                intro_text = ""
                                if len(harvested_li_tags) > 2:
                                    for ch in harvested_li_tags[2].children:
                                        if getattr(ch, 'name', None) != 'ul':
                                            intro_text += ch.get_text(' ', strip=True) + ' '
                                intro_text = intro_text.strip()
                                
                                nested_ul.extract()
                                parent_li.clear()
                                st = soup.new_tag('strong')
                                st.string = intro_text
                                parent_li.append(st)
                                parent_li.append(nested_ul)
                            
            # 3. Translate paragraphs and figcaptions
            if 'About' in en_h4:
                p_tag = sp.find('p')
                if p_tag:
                    if c_idx == 1 and 'rubin' in about_bios:
                        p_tag.string = about_bios['rubin']
                    elif c_idx == 2 and 'kisfaludy' in about_bios:
                        p_tag.string = about_bios['kisfaludy']
                    elif c_idx == 3 and 'portum' in about_bios:
                        p_tag.string = about_bios['portum']
                    elif c_idx in [4, 5, 6] and 'silverline' in about_bios:
                        p_tag.string = about_bios['silverline']
                    elif c_idx in [7, 8] and 'hungaria' in about_bios:
                        p_tag.string = about_bios['hungaria']
                        
            # Ship prefixes in paragraphs (e.g. Ship: Gondola)
            for p in sp.find_all('p'):
                ptxt = p.get_text(strip=True)
                if 'Ship:' in ptxt:
                    ship_name = ptxt.replace('Ship:', '').strip()
                    p.clear()
                    st = soup.new_tag('strong')
                    st.string = f"{captions.get('prefix', 'Ship: ')}{ship_name}"
                    p.append(st)
                    
            # Figcaptions
            for fc in sp.find_all('figcaption'):
                fctxt = fc.get_text(strip=True)
                if 'Gondola' in fctxt and captions.get('gondola'):
                    fc.string = captions['gondola']
                elif 'Danube Legend' in fctxt and captions.get('legenda'):
                    fc.string = captions['legenda']
                elif 'Duna Bella' in fctxt and captions.get('dunabella'):
                    fc.string = captions['dunabella']

def compile_language_river(lang, en_html):
    """Compiles a 100% localized river cruise page for a given language."""
    print(f"Compiling [{lang.upper()}] River Cruise Guide...")
    soup = BeautifulSoup(en_html, 'html.parser')
    
    river_slug = SLUG_MAP[lang]['river']
    canonical_url = f"https://www.budapestadventures.com/{lang}/{river_slug}"
    
    # Brand logo link
    brand = soup.find('a', class_='ltt-brand')
    if brand:
        brand['href'] = f'/{lang}'

    # 1. HTML tag
    html_tag = soup.find('html')
    if html_tag:
        html_tag['lang'] = lang
        if lang == 'he':
            html_tag['dir'] = 'rtl'
            
    # 2. Canonical & Hreflang
    can = soup.find('link', rel='canonical')
    if can:
        can['href'] = canonical_url
    ensure_nl_hreflang(soup)
    
    # 3. Meta Tags
    pm = PAGE_META.get(lang, {})
    if soup.title and pm.get('title'):
        soup.title.string = pm['title']
    m_desc = soup.find('meta', {'name': 'description'})
    if m_desc and pm.get('desc'):
        m_desc['content'] = pm['desc']
    for tag_name, prop_name in [('meta', 'property'), ('meta', 'name')]:
        og_t = soup.find(tag_name, {prop_name: 'og:title'})
        if og_t and pm.get('title'): og_t['content'] = pm['title']
        tw_t = soup.find(tag_name, {prop_name: 'twitter:title'})
        if tw_t and pm.get('title'): tw_t['content'] = pm['title']
        og_d = soup.find(tag_name, {prop_name: 'og:description'})
        if og_d and pm.get('desc'): og_d['content'] = pm['desc']
        tw_d = soup.find(tag_name, {prop_name: 'twitter:description'})
        if tw_d and pm.get('desc'): tw_d['content'] = pm['desc']

    # 3.5. Extract Harvested Tours & Harvested LIs
    harvested_river_path = os.path.join(BASE_DIR, 'data', 'harvested_html', lang, 'river.html')
    tours = extract_tour_content(harvested_river_path, 'river')
    if os.path.exists(harvested_river_path):
        h_soup = BeautifulSoup(open(harvested_river_path, encoding='utf-8'), 'html.parser')
        harvested_li_tags = h_soup.find_all('li')
        harvested_lis = [li.get_text(' ', strip=True) for li in harvested_li_tags]
    else:
        harvested_li_tags = []
        harvested_lis = []
    
    ui = UI_COMMON.get(lang, {})
    best_fors = BEST_FOR_DATA.get(lang, [])
    rank_badges = RANK_BADGES.get(lang, [])

    # Localize CSS Pseudo-Elements (Read Review / Close Review)
    style_tag = soup.find('style', id='ltt-dubai-safari-styles')
    if style_tag and style_tag.string:
        read_rev = ui.get('read_review', 'Read Review').replace(' ↓', '').replace('↓', '').strip()
        close_rev = ui.get('collapse_all', 'Close Review').strip()
        new_css = style_tag.string.replace('content:"Read Review"', f'content:"{read_rev}"')
        new_css = new_css.replace('content:"Close Review"', f'content:"{close_rev}"')
        style_tag.string = new_css

    # 4. JSON-LD Localization
    intro = INTRO_DATA.get(lang, {})
    cleanse_json_ld(soup, lang, pm, intro, canonical_url, tours, best_fors)

    # 5. Breadcrumbs
    for bc in soup.find_all(class_='ltt-breadcrumbs'):
        bc.clear()
        home_a = soup.new_tag('a', href=f'/{lang}')
        home_a.string = pm.get('bc_home', 'Home')
        sep = soup.new_tag('span', **{'class': 'ltt-bc-sep'})
        sep.string = '›'
        curr = soup.new_tag('span', **{'class': 'ltt-bc-current'})
        curr.string = pm.get('bc_curr', 'River Cruises')
        bc.append(home_a)
        bc.append(' ')
        bc.append(sep)
        bc.append(' ')
        bc.append(curr)

    # 6. Hero Kicker & H1
    badge = soup.find(class_='ltt-hero-kicker-badge')
    if badge and pm.get('kicker'):
        badge.string = pm['kicker']
    h1 = soup.find(class_='ltt-editorial-h1') or soup.find('h1')
    if h1 and pm.get('h1'):
        h1.string = pm['h1']

    # 7. Author Byline & Metadata
    auth = AUTHOR_DATA.get(lang, {})
    auth_line = soup.find(class_='ltt-author-line')
    if auth_line and auth.get('prefix'):
        auth_line.clear()
        auth_line.append(auth['prefix'])
        a_tag = soup.new_tag('a', href="/about")
        a_tag.string = "Adam Dimitrov"
        auth_line.append(a_tag)
        auth_line.append(f" — {auth.get('role', 'Budapest River Cruise Specialist')}")
        
    auth_role = soup.find(class_='ltt-author-role')
    if auth_role and auth.get('badge'):
        auth_role.string = auth['badge']
        
    tp = soup.find(class_='ltt-trust-pill')
    if tp and auth.get('updated'):
        tp.string = auth['updated']
    upd = soup.find(class_='ltt-updated-date')
    if upd and auth.get('updated'):
        upd.string = auth['updated']

    # 8. Lead Copy (3 Editorial Intro Paragraphs)
    lead = soup.find(class_='ltt-lead-copy')
    if lead and intro.get('p1'):
        fig = lead.find('figure')
        lead.clear()
        for pkey in ['p1', 'p2', 'p3']:
            if intro.get(pkey):
                p = soup.new_tag('p')
                p.string = intro[pkey]
                lead.append(p)
        if fig:
            lead.append(fig)

    # 9. Dinner Guide Callout Box & Editorial Bookmark Card
    bookmark = soup.find(class_='cd-editorial-bookmark') or soup.find(class_='cd-bookmark-wrapper')
    if bookmark:
        a_tag = bookmark if bookmark.name == 'a' else bookmark.find('a')
        if a_tag:
            dinner_slug = SLUG_MAP.get(lang, {}).get('dinner', 'best-dinner-cruises-budapest')
            a_tag['href'] = f"/{lang}/{dinner_slug}"
        t_el = bookmark.find(class_='cd-editorial-title')
        if t_el and intro.get('dinner_title'):
            t_el.string = intro['dinner_title']
        d_el = bookmark.find(class_='cd-editorial-desc')
        if d_el and intro.get('dinner_desc'):
            d_el.string = intro['dinner_desc']
        thumb_img = bookmark.find(class_='cd-editorial-thumb')
        if thumb_img:
            img = thumb_img.find('img')
            if img and intro.get('dinner_title'):
                img['alt'] = intro['dinner_title']

    dinner_callout = soup.find(class_='ltt-dinner-callout') or soup.find(class_='ltt-dinner-crosslink') or soup.find(class_='ltt-dinner-banner')
    if dinner_callout and intro.get('dinner_title'):
        title_el = dinner_callout.find(class_='ltt-dinner-title') or dinner_callout.find('h3') or dinner_callout.find('strong')
        if title_el:
            title_el.string = intro['dinner_title']
        sub_el = dinner_callout.find(class_='ltt-dinner-sub') or dinner_callout.find('p')
        if sub_el and intro.get('dinner_desc'):
            sub_el.string = intro['dinner_desc']

    # 10. Filter Tabs
    ftabs = FILTER_TABS_DATA.get(lang, {})
    flabel = soup.find(class_='ltt-filter-label')
    if flabel and ftabs.get('label'):
        flabel.string = ftabs['label']
    tab_btns = soup.find_all(class_='ltt-tab-btn')
    tab_keys = ['all', 'tested', 'under20', 'drinks', 'dinner', 'historic']
    for idx, btn in enumerate(tab_btns[:6]):
        k = tab_keys[idx]
        if ftabs.get(k):
            btn.string = ftabs[k]

    # 12. Top Deck Summary Cards (10 Cards: div.bpa-card)
    deck_cards = soup.find_all(class_='bpa-card')
    tested_chip_label = re.sub(r'\s*\(\d+\)', '', ftabs.get('tested', '✓ Personally Tested'))

    for idx, dcard in enumerate(deck_cards):
        if idx >= len(tours): break
        tdata = tours[idx]
        
        # Image alt attributes
        for img in dcard.find_all('img'):
            img['alt'] = tdata['clean_title']
        
        # Rank badge
        rank_badge = dcard.find(class_='bpa-rank-tag')
        if rank_badge and idx < len(rank_badges):
            rank_badge.string = rank_badges[idx]
            
        # Clean title
        title_el = dcard.find(class_='bpa-title')
        if title_el:
            title_el.string = tdata['clean_title']
            
        # Best For
        bf_el = dcard.find(class_='bpa-best-for')
        if bf_el and idx < len(best_fors):
            bf_el.clear()
            st = soup.new_tag('strong')
            st.string = ui.get('best_for_label', 'Best For: ')
            bf_el.append(st)
            bf_el.append(best_fors[idx])
            
        # Price label: div.bpa-psub or .bpa-card-price-sub
        psub = dcard.find(class_='bpa-psub') or dcard.find(class_='bpa-card-price-sub')
        if psub and ui.get('per_adult'):
            psub.string = ui['per_adult']

        # Tested vchip badge
        for vchip in dcard.find_all(class_='bpa-vchip'):
            if 'Personally Tested' in vchip.get_text():
                vchip.string = tested_chip_label

        # Kicker minutes & dock
        kicker = dcard.find(class_='bpa-kicker')
        if kicker:
            ku = KICKER_UNITS.get(lang, {})
            if ku.get('mins'):
                for child in list(kicker.children):
                    if isinstance(child, str):
                        new_child = child.replace(' Mins', ku['mins']).replace(' mins', ku['mins'])
                        child.replace_with(new_child)
            if ku.get('dock'):
                klink = kicker.find(class_='bpa-kicker-map-link')
                if klink and klink.string and 'Dock ' in klink.string:
                    klink.string = klink.string.replace('Dock ', ku['dock'])
            
        # CTA button
        btn = dcard.find(class_='bpa-btn')
        if btn and ui.get('btn_check'):
            btn.string = ui['btn_check']
            
        # Read review jump link
        jump = dcard.find(class_='bpa-sublink')
        if jump and ui.get('read_review'):
            jump.string = ui['read_review']
            
        # Trust micro
        for micro in dcard.find_all(class_='bpa-trust-micro'):
            spans = micro.find_all('span')
            if len(spans) >= 3:
                if ui.get('instant_qr'): spans[0].string = ui['instant_qr']
                if ui.get('official_pier'): spans[2].string = ui['official_pier']

    # 13. Detailed Breakdown Section Header & Expand/Collapse
    bd_headers = BREAKDOWN_HEADERS.get(lang, {})
    for bd_title in soup.find_all(class_='bpa-breakdown-heading'):
        if bd_headers.get('title'):
            bd_title.string = bd_headers['title']
    for bd_sub in soup.find_all(class_='bpa-breakdown-sub'):
        if bd_headers.get('sub'):
            bd_sub.string = bd_headers['sub']
        
    for ctrl_btn in soup.find_all(class_='bpa-acc-ctrl-btn'):
        btxt = ctrl_btn.get_text()
        if 'Expand All' in btxt and ui.get('expand_all'):
            ctrl_btn.string = ui['expand_all']
        elif 'Collapse All' in btxt and ui.get('collapse_all'):
            ctrl_btn.string = ui['collapse_all']

    # Table of Contents & window.LTT_PAGE_CONFIG
    localize_toc_and_config(soup, lang, tours, ui)

    # 14. 10 Details Cards (Pros, Cons, Bento tabs, Bento 0 body, Buy box)
    details_cards = soup.find_all('details', class_='bpa-details-card')
    buy_card_data = BUY_CARD_I18N.get(lang, {})

    for idx, dcard in enumerate(details_cards):
        if idx >= len(tours): break
        tdata = tours[idx]
        
        # Rank tag
        rank_tag = dcard.find(class_='bpa-rank-tag')
        badges = RANK_BADGES.get(lang, [])
        if rank_tag and idx < len(badges):
            rank_tag.string = badges[idx]

        # Details title
        d_title = dcard.find(class_='bpa-details-title')
        if d_title:
            d_title.string = tdata['clean_title']

        # Kicker minutes & dock
        kicker = dcard.find(class_='bpa-kicker')
        if kicker:
            ku = KICKER_UNITS.get(lang, {})
            if ku.get('mins'):
                for child in list(kicker.children):
                    if isinstance(child, str):
                        new_child = child.replace(' Mins', ku['mins']).replace(' mins', ku['mins'])
                        child.replace_with(new_child)
            if ku.get('dock'):
                klink = kicker.find(class_='bpa-kicker-map-link')
                if klink and klink.string and 'Dock ' in klink.string:
                    klink.string = klink.string.replace('Dock ', ku['dock'])

        # Buy card perks
        buy_card = dcard.find(class_='ltt-buy-card')
        if buy_card:
            ku = KICKER_UNITS.get(lang, {})
            for perk in buy_card.find_all(class_='ltt-buy-perk'):
                st = perk.find('strong')
                if st and st.string:
                    if ku.get('mins'):
                        st.string = st.string.replace(' Mins', ku['mins']).replace(' mins', ku['mins'])
                    if ku.get('dock') and 'Dock ' in st.string:
                        st.string = st.string.replace('Dock ', ku['dock'])

        # Tested vchip in details header
        for vchip in dcard.find_all(class_='bpa-vchip'):
            if 'Personally Tested' in vchip.get_text():
                vchip.string = tested_chip_label
                
        # Quick Facts Section (.qf1-wrap)
        qf_wrap = dcard.find(class_='qf1-wrap')
        if qf_wrap:
            qf_title = qf_wrap.find(class_='qf1-title')
            if qf_title and lang in QF_TITLES:
                qf_title.string = QF_TITLES[lang]
                
            qf_badge = qf_wrap.find(class_='qf1-badge')
            if qf_badge and qf_badge.string:
                ku = KICKER_UNITS.get(lang, {})
                if ku.get('dock') and 'Dock ' in qf_badge.string:
                    qf_badge.string = qf_badge.string.replace('Dock ', ku['dock'])
                    
            lbl_map = QF_LABELS.get(lang, {})
            for row in qf_wrap.find_all(class_='qf1-row'):
                lbl = row.find(class_='qf1-label')
                if lbl:
                    ltxt = lbl.get_text(strip=True)
                    if ltxt in lbl_map:
                        lbl.string = lbl_map[ltxt]
                val = row.find(class_='qf1-val')
                if val and val.string:
                    ku = KICKER_UNITS.get(lang, {})
                    if ku.get('mins'):
                        val.string = val.string.replace(' Minutes', ku['mins']).replace(' minutes', ku['mins']).replace(' Mins', ku['mins'])
                        
            chip_map = QF_CHIPS.get(lang, {})
            for chip in qf_wrap.find_all(class_='qf1-chip'):
                ctxt = chip.get_text(strip=True)
                if ctxt in chip_map:
                    chip.string = chip_map[ctxt]
            
        # Update images inside details card with localized subpoint headings
        sub_headings = SUBPOINT_HEADINGS.get(lang, {})
        for sp in dcard.find_all(class_='ltt-sp-card'):
            h4 = sp.find('h4')
            en_h4 = h4.get_text(strip=True) if h4 else ''
            loc_h4 = sub_headings.get(en_h4, en_h4)
            for img in sp.find_all('img'):
                if loc_h4:
                    img['alt'] = f"{tdata['clean_title']} — {loc_h4}"
                else:
                    img['alt'] = tdata['clean_title']

        # Pros & Cons replacement with native labels and content (zero English specs leak)
        exp_dict = EXPANDED_PROS_CONS_I18N.get(lang, {}).get(idx) or EXPANDED_PROS_CONS_I18N.get(lang, {}).get(str(idx))
        if exp_dict:
            pros = exp_dict['pros']
            cons = exp_dict['cons']
        else:
            def is_spec(s):
                sl = s.lower()
                return any(k in sl for k in [
                    'onboard wi-fi', 'wi-fi:', 'open air deck', 'deck:', 'air conditioning', 'conditioning:',
                    'smoking:', 'wheelchair accessible', 'baby stroller', 'pets allowed',
                    'discount:', 'centrally located'
                ])
            pros = [p for p in tdata['pros'] if not is_spec(p)]
            cons = [c for c in tdata['cons'] if not is_spec(c)]
            if not pros:
                pros = [tdata['clean_title']]
            if not cons:
                cons = [ui.get('reserve_early', "Popular departures may sell out quickly.")]
        
        pro_con_box = dcard.find(class_='pro-con-box-wrapper')
        if pro_con_box:
            new_box = soup.new_tag('div', **{'class': 'pro-con-box-wrapper'})
            grid = soup.new_tag('div', **{'class': 'w-layout-grid grid-15'})
            new_box.append(grid)
            
            pro_cell = soup.new_tag('div', **{'class': 'pro-con-box-pro-cell', 'data-wf-pbl': 'layout-grid-1x2-vertical'})
            pro_rich = soup.new_tag('div', **{'class': 'pro-con-box-pro-cell-rich-text-block w-richtext'})
            h3_pro = soup.new_tag('h3')
            st_pro = soup.new_tag('strong')
            st_pro.string = ui.get('pros', 'Pros:')
            h3_pro.append(st_pro)
            pro_rich.append(h3_pro)
            ul_pro = soup.new_tag('ul', **{'role': 'list'})
            for p_text in pros:
                li = soup.new_tag('li')
                li.string = p_text
                ul_pro.append(li)
            pro_rich.append(ul_pro)
            pro_cell.append(pro_rich)
            grid.append(pro_cell)
            
            con_cell = soup.new_tag('div', **{'class': 'pro-con-box-con-cell', 'data-wf-pbl': 'layout-grid-1x2-vertical'})
            con_rich = soup.new_tag('div', **{'class': 'pro-con-box-con-cell-rich-text-block w-richtext'})
            h3_con = soup.new_tag('h3')
            st_con = soup.new_tag('strong')
            st_con.string = ui.get('cons', 'Cons:')
            h3_con.append(st_con)
            con_rich.append(h3_con)
            ul_con = soup.new_tag('ul', **{'role': 'list'})
            for c_text in cons:
                li = soup.new_tag('li')
                li.string = c_text
                ul_con.append(li)
            con_rich.append(ul_con)
            con_cell.append(con_rich)
            grid.append(con_cell)
            
            pro_con_box.replace_with(new_box)

        # Bento Tabs Localization
        bento_groups = dcard.find_all('details', class_='ltt-bento-group')
        for bg in bento_groups:
            head = bg.find('summary')
            if not head: continue
            btitle = head.find(class_='ltt-bento-group-title')
            bmeta = head.find(class_='ltt-bento-group-meta')
            if btitle:
                btxt = btitle.text.strip()
                if any(w in btxt for w in ['Summary', 'Zusammenfassung', 'Résumé', 'Resumen', 'Sommario', 'Overzicht', 'Przegląd', 'Prezentare', 'Přehled', 'Prehľad', 'Pregled', 'Преглед', 'Обзор', 'Επισκόπηση', 'Özet', 'סקירה', '概要', '개요']):
                    btitle.string = f"🏆 {ui.get('overview', 'Summary & Review')}"
                    if bmeta and ui.get('overview'): bmeta.string = f"{ui['overview']} ▾"
                elif any(w in btxt for w in ['Pier', 'Boarding', 'Anlegestelle', 'Quai', 'Muelle', 'Molo', 'Steiger', 'Przystań', 'Ponton', 'Mólo', 'Dok', 'Док', 'Кей', 'Причал', 'Αποβάθρα', 'İskele', 'Cais', 'רציף', '乗り場', '선착장']):
                    btitle.string = f"📍 {ui.get('map_label', 'Pier, Boarding & Map')}"
                    if bmeta and ui.get('map_label'): bmeta.string = f"{ui['map_label']} ▾"
                elif any(w in btxt for w in ['Ship', 'Deck', 'Schiff', 'Bateau', 'Barco', 'Nave', 'Schip', 'Statek', 'Nava', 'Loď', 'Brod', 'Брод', 'Кораб', 'Теплоход', 'Πλοίο', 'Gemi', 'Navio', 'ספינה', '船', '선박']):
                    btitle.string = f"🛳️ {ui.get('walkthrough', 'The Ship & Deck')}"
                    if bmeta and ui.get('walkthrough'): bmeta.string = f"{ui['walkthrough']} ▾"
                elif any(w in btxt for w in ['Audio', 'Operator', 'Service', 'Guide', 'Reederei', 'Compagnie', 'Naviera', 'Armator', 'Operat']):
                    btitle.string = f"🎧 {ui.get('audio_op', 'Audio Guide & Services')}"
                    if bmeta and ui.get('audio_op'): bmeta.string = f"{ui['audio_op']} ▾"

        # Bento 0 Summary Body
        if len(bento_groups) >= 1 and tdata['summaries']:
            b0_body = bento_groups[0].find(class_='ltt-bento-group-body')
            if b0_body:
                rich = b0_body.find(class_='w-richtext')
                if not rich:
                    rich = soup.new_tag('div', **{'class': 'w-richtext'})
                    b0_body.clear()
                    b0_body.append(rich)
                else:
                    rich.clear()
                for p_text in tdata['summaries']:
                    p = soup.new_tag('p')
                    p.string = p_text
                    rich.append(p)

        # Buy Box / Official Ticket Card Localization
        buy_card = dcard.find(class_='ltt-buy-card')
        if buy_card and buy_card_data:
            badge_span = buy_card.find(class_='ltt-buy-card-badge')
            if badge_span:
                text_span = [s for s in badge_span.find_all('span') if 'ltt-live-dot' not in s.get('class', [])]
                if text_span and buy_card_data.get('badge'):
                    text_span[0].string = buy_card_data['badge']
                    
            title_h4 = buy_card.find(class_='ltt-buy-card-title')
            if title_h4:
                title_h4.string = tdata['clean_title']
                
            psub_el = buy_card.find(class_='ltt-buy-price-sub')
            if psub_el and buy_card_data.get('per_adult'):
                psub_el.string = buy_card_data['per_adult']
                
            btn_el = buy_card.find(class_='ltt-buy-cta-btn')
            if btn_el and buy_card_data.get('btn'):
                btn_el.string = buy_card_data['btn']
                
            trust_div = buy_card.find(class_='ltt-buy-card-trust')
            if trust_div:
                sp_trust = trust_div.find('span')
                if sp_trust and buy_card_data.get('trust'):
                    sp_trust.string = buy_card_data['trust']
                    
            for perk in buy_card.find_all(class_='ltt-buy-perk'):
                p_txt = perk.get_text()
                if 'QR' in p_txt and buy_card_data.get('qr'):
                    perk.string = buy_card_data['qr']
                elif 'Refund' in p_txt and buy_card_data.get('refund'):
                    perk.string = buy_card_data['refund']
                elif 'Departure:' in p_txt and buy_card_data.get('departure'):
                    strong = perk.find('strong')
                    strong_txt = strong.get_text() if strong else ''
                    perk.clear()
                    perk.append(f"{buy_card_data['departure']} ")
                    st = soup.new_tag('strong')
                    st.string = strong_txt
                    perk.append(st)
                elif 'Duration:' in p_txt and buy_card_data.get('duration'):
                    strong = perk.find('strong')
                    strong_txt = strong.get_text() if strong else ''
                    perk.clear()
                    perk.append(f"{buy_card_data['duration']} ")
                    st = soup.new_tag('strong')
                    st.string = strong_txt
                    perk.append(st)

    # 15. Deterministic Walkthrough Subpoints & Blockquotes Localization
    localize_walkthrough_subpoints(soup, lang, harvested_lis, harvested_li_tags)
    localize_all_blockquotes(soup, lang, ui)

    # 16. Header, Specs, Sticky bar, Footer
    dinner_slug = SLUG_MAP[lang]['dinner']
    localize_navbar_and_menu(soup, lang, river_slug, dinner_slug)
    localize_specs_row(soup, lang, ui)
    localize_sticky_bar(soup, lang, tours, buy_card_data, ui, rank_badges)
    localize_footer_section(soup, lang, river_slug, dinner_slug)

    # 17. Sanitize Language-Specific Residual Phrases
    leak_fixes = {
        'cs': [('Welcome Drink', 'Uvítací nápoj'), ('welcome drink', 'uvítací nápoj')],
        'sk': [('Welcome Drink', 'Uvítací nápoj'), ('welcome drink', 'uvítací nápoj')],
        'ru': [("Silverline's audio guide", "аудиогид Silverline")],
        'el': [("Inaudible Audio Guide", "Δυσδιάκριτος ακουστικός οδηγός")]
    }
    if lang in leak_fixes:
        for old_t, new_t in leak_fixes[lang]:
            for node in list(soup.find_all(text=lambda t: t and old_t in t)):
                node.replace_with(node.replace(old_t, new_t))

    # 18. Preserve Affiliate Links
    for a in soup.find_all('a', href=True):
        href = a['href']
        if 'legenda.hu' in href and 'partner=38585' not in href:
            sep = '&' if '?' in href else '?'
            a['href'] = f"{href}{sep}partner=38585"
        if 'budapestxplore.com' in href and 'affi=6876' not in href:
            sep = '&' if '?' in href else '?'
            a['href'] = f"{href}{sep}affi=6876"

    return str(soup)

def update_root_and_hu_hreflang():
    """Adds the Dutch hreflang tag into English master, river.html, and Hungarian river page."""
    paths = [
        os.path.join(BASE_DIR, 'best-budapest-river-cruises', 'index.html'),
        os.path.join(BASE_DIR, 'river.html'),
        os.path.join(BASE_DIR, 'hu', 'setahajozas-a-dunan-budapest', 'index.html')
    ]
    for p in paths:
        if os.path.exists(p):
            soup = BeautifulSoup(open(p, encoding='utf-8'), 'html.parser')
            ensure_nl_hreflang(soup)
            with open(p, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"✓ Added Dutch hreflang tag to: {os.path.relpath(p, BASE_DIR)}")

def compile_all_foreign_languages():
    """Compiles all 20 foreign languages."""
    langs = ['de', 'fr', 'es', 'it', 'nl', 'pl', 'ro', 'cs', 'sk', 'hr', 'sr', 'bg', 'ru', 'uk', 'el', 'tr', 'pt', 'he', 'ja', 'ko']
    
    en_path = os.path.join(BASE_DIR, 'best-budapest-river-cruises', 'index.html')
    en_html = open(en_path, encoding='utf-8').read()
    
    print(f"\n=======================================================")
    print(f"MASTER RIVER MULTILINGUAL COMPILATION: {len(langs)} LANGUAGES")
    print(f"=======================================================\n")
    
    success_count = 0
    for l in langs:
        river_slug = SLUG_MAP[l]['river']
        out_dir = os.path.join(BASE_DIR, l, river_slug)
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, 'index.html')
        
        compiled_html = compile_language_river(l, en_html)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(compiled_html)
        print(f"✓ [{l.upper()}] Written to {l}/{river_slug}/index.html ({len(compiled_html):,} bytes)")
        success_count += 1
        
    print(f"\n✓ Successfully compiled all {success_count} foreign language river cruise pages!")

if __name__ == '__main__':
    update_root_and_hu_hreflang()
    compile_all_foreign_languages()
