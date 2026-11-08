#!/usr/bin/env python3
"""
MASTER HUNGARIAN LUXURY EDITORIAL COMPILER
Translates and compiles 100% native Hungarian pages for Budapest Adventures:
1. hu/index.html (Homepage)
2. hu/setahajozas-a-dunan-budapest/index.html (River guide)
3. hu/setahajozas-a-dunan-vacsoraval/index.html (Dinner guide)

Eliminates all English fragments, enforces Luxury Editorial System architecture,
restores canonical Pros & Cons rich-text grid structure, and preserves 100% affiliate tracking links.
"""

import os
import sys
import re
import json
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.hungarian_subpoints_data import (
    RIVER_SUBPOINTS,
    DINNER_SUBPOINTS,
    QF_LABELS_HU,
    QF_CHIPS_HU,
    QF_BADGES_HU,
    QF_VALS_HU
)

BASE_DIR = '/Users/adamdimitrov/Development/budapest-adventures'

def localize_navbar_and_menu(soup):
    """Localizes the header, mega-menu dropdowns, direct links, and mobile drawer to Hungarian."""
    # 1. Dropdown button
    dropdown_btn = soup.find('button', class_='ltt-dropdown-btn')
    if dropdown_btn:
        span = dropdown_btn.find('span')
        if span:
            span.string = "Dunai Hajózás"
            
    # 2. Mega menu headers
    mega_heads = soup.find_all(class_='ltt-mega-head')
    if len(mega_heads) >= 1:
        mega_heads[0].string = "DUNAI SÉTAHAJÓK"
    if len(mega_heads) >= 2:
        mega_heads[1].string = "LÁTNIVALÓK ÉS FÜRDŐK"
        
    # 3. Mega menu items
    mega_items = soup.find_all(class_='ltt-mega-item')
    mega_translations = {
        '/best-budapest-river-cruises': ('10 Legjobb Dunai Sétahajó', 'Helyszínen tesztelt nappali és esti hajók', '/hu/setahajozas-a-dunan-budapest'),
        '/best-dinner-cruises-budapest': ('7 Legjobb Vacsorahajó', '4 fogásos vacsorák, folklór és élő zongora', '/hu/setahajozas-a-dunan-vacsoraval'),
        '/unlimited-prosecco-cruises-budapest': ('Korlátlan Prosecco Hajók', 'Korlátlan pezsgőfogyasztás és zene', '/unlimited-prosecco-cruises-budapest'),
        '/best-night-cruises-budapest': ('Legjobb Éjszakai Hajók', 'Esti utak kivilágított Parlamenttel', '/best-night-cruises-budapest'),
        '/best-private-boat-tours-budapest': ('Privát Hajóbérlés', 'Exkluzív dunai jachtok és vízi taxik', '/best-private-boat-tours-budapest'),
        '/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest': ('Legenda Gyertyafényes Teszt', 'Budapest első számú vacsorahajója', '/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest'),
        '/budapest-card-is-it-worth-it': ('Budapest Kártya Kalkulátor', 'Interaktív kalkulátor 94 látnivalóval', '/budapest-card-is-it-worth-it'),
        '/thermal-baths-budapest': ('8 Legjobb Termálfürdő', 'Széchenyi, Gellért, Rudas és Lukács', '/thermal-baths-budapest'),
        '/best-walking-tours-budapest': ('Legjobb Gyalogtúrák', 'Várnegyed és Zsidó Negyed gasztroséták', '/best-walking-tours-budapest'),
        '/best-hostels-budapest': ('Legjobb Hostelek Budapesten', 'Közösségi és boutique szállások', '/best-hostels-budapest'),
    }
    
    for item in mega_items:
        href = item.get('href', '')
        for k, (t_title, t_desc, t_href) in mega_translations.items():
            if href == k or href == t_href:
                item['href'] = t_href
                st = item.find('strong')
                if st: st.string = t_title
                p = item.find('p')
                if p: p.string = t_desc
                break

    # 4. Direct nav links
    nav_links = soup.find_all(class_='ltt-nav-link')
    for nl in nav_links:
        if 'ltt-dropdown-btn' in nl.get('class', []):
            continue
        txt = nl.text.strip()
        if txt in ['River Cruises', 'Dunai Sétahajók']:
            nl.string = 'Dunai Sétahajók'
            nl['href'] = '/hu/setahajozas-a-dunan-budapest'
        elif txt in ['Dinner Cruises', 'Vacsorahajók']:
            nl.string = 'Vacsorahajók'
            nl['href'] = '/hu/setahajozas-a-dunan-vacsoraval'
        elif txt in ['Budapest Card', 'Budapest Kártya']:
            nl.string = 'Budapest Kártya'
            nl['href'] = '/budapest-card-is-it-worth-it'
        elif txt in ['About', 'Rólunk']:
            nl.string = 'Rólunk'
            nl['href'] = '/about'
        elif txt in ['Contact', 'Kapcsolat']:
            nl.string = 'Kapcsolat'
            nl['href'] = '/contact'

    # 5. Mobile Drawer
    drawer = soup.find(class_='ltt-mobile-drawer')
    if drawer:
        labels = drawer.find_all(class_='ltt-mobile-label')
        if len(labels) >= 1: labels[0].string = "Dunai Hajózás & Kalauzok"
        if len(labels) >= 2: labels[1].string = "Látnivalók & Fürdők"
        if len(labels) >= 3: labels[2].string = "Szerkesztőség"
        
        m_links = drawer.find_all(class_='ltt-mobile-link')
        for ml in m_links:
            href = ml.get('href', '')
            span = ml.find('span')
            
            if '/best-budapest-river-cruises' in href or '/hu/setahajozas-a-dunan-budapest' in href:
                ml['href'] = '/hu/setahajozas-a-dunan-budapest'
                if span: span.string = '10 Legjobb Dunai Sétahajó'
                b = ml.find_all('span')
                if len(b) > 1: b[1].string = 'LEGJOBB'
            elif '/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest' in href:
                if span: span.string = 'Legenda Gyertyafényes Teszt'
            elif '/best-dinner-cruises-budapest' in href or '/hu/setahajozas-a-dunan-vacsoraval' in href:
                ml['href'] = '/hu/setahajozas-a-dunan-vacsoraval'
                if span: span.string = '7 Legjobb Vacsorahajó'
            elif '/unlimited-prosecco-cruises-budapest' in href:
                if span: span.string = 'Korlátlan Prosecco Hajók'
            elif '/best-night-cruises-budapest' in href:
                if span: span.string = 'Legjobb Éjszakai Hajók'
            elif '/best-private-boat-tours-budapest' in href:
                if span: span.string = 'Privát Hajóbérlés'
            elif '/budapest-card-is-it-worth-it' in href:
                if span: span.string = 'Budapest Kártya Kalkulátor'
                b = ml.find_all('span')
                if len(b) > 1: b[1].string = 'INTERAKTÍV'
            elif '/thermal-baths-budapest' in href:
                if span: span.string = '8 Legjobb Termálfürdő'
            elif '/best-walking-tours-budapest' in href:
                if span: span.string = 'Legjobb Gyalogtúrák'
            elif '/best-hostels-budapest' in href:
                if span: span.string = 'Legjobb Hostelek Budapesten'
            elif '/about' in href:
                if span: span.string = 'Rólunk és Etikai Kódex'
            elif '/contact' in href:
                if span: span.string = 'Kapcsolat'


def localize_footer(soup):
    """Localizes the footer brand description, columns, popular links, copyright and taglines."""
    footer = soup.find('footer') or soup.find(class_='footer-dark')
    if not footer:
        return
        
    brand_desc = footer.find(class_='footer-brand-desc') or footer.find(class_='footer-paragraph')
    if brand_desc:
        brand_desc.string = (
            "A dunai sétahajók és vacsorahajók független, helyszíni tesztelése. "
            "Budapesten élve saját költségünkön váltunk jegyet, teszteljük az audio guide-okat "
            "és ellenőrizzük az összes kikötőt, hogy Ön elkerülje a turistacsapdákat."
        )
        
    col_titles = footer.find_all(class_=lambda c: c and ('footer-col-title' in c or 'footer-link-title' in c))
    if len(col_titles) >= 1:
        col_titles[0].string = "Kiemelt Budapesti Kalauzok"
    if len(col_titles) >= 2:
        col_titles[1].string = "Megbízhatóság és Vállalat"
        
    footer_links = footer.find_all('a', class_=lambda c: c and ('footer-link-item' in c or 'footer-link-3' in c))
    for fl in footer_links:
        href = fl.get('href', '')
        if href in ['/best-budapest-river-cruises', '/hu/setahajozas-a-dunan-budapest']:
            fl.string = '10 Legjobb Dunai Sétahajózás'
            fl['href'] = '/hu/setahajozas-a-dunan-budapest'
        elif href in ['/best-dinner-cruises-budapest', '/hu/setahajozas-a-dunan-vacsoraval']:
            fl.string = '7 Legjobb Dunai Vacsorahajó'
            fl['href'] = '/hu/setahajozas-a-dunan-vacsoraval'
        elif href == '/budapest-card-is-it-worth-it':
            fl.string = 'Budapest Kártya Kalkulátor (2026)'
        elif href == '/thermal-baths-budapest':
            fl.string = '8 Legjobb Budapesti Termálfürdő'
        elif href == '/best-night-cruises-budapest':
            fl.string = 'Legjobb Éjszakai Sétahajók'
        elif href == '/unlimited-prosecco-cruises-budapest':
            fl.string = 'Korlátlan Prosecco Hajóutak'
        elif href == '/best-private-boat-tours-budapest':
            fl.string = 'Legjobb Privát Hajótúrák'
        elif href == '/best-walking-tours-budapest':
            fl.string = 'Legjobb Budapesti Gyalogtúrák'
        elif href == '/best-hostels-budapest':
            fl.string = 'Legjobb Hostelek Budapesten'
        elif href == '/about':
            fl.string = 'Adam Dimitrovról'
        elif href in ['/about#ethics', '/about#methodology']:
            fl.string = '5 Pontos Etikai Chartánk'
        elif href == '/about#manifesto':
            fl.string = 'Függetlenségi Manifesztum'
        elif href == '/contact':
            fl.string = 'Kapcsolat a Szerkesztőséggel'
            
    legal = footer.find(class_='legal-wrapper')
    if legal:
        divs = legal.find_all(class_='legal-text') or legal.find_all('div')
        if len(divs) >= 1:
            divs[0].string = "© 2026 BudapestAdventures.com. Minden jog fenntartva."
        if len(divs) >= 2:
            divs[1].string = "Személyesen, inkognitóban tesztelve Budapesten • 100% névtelen foglalások • Nulla szponzorált PR-út"


def apply_qf_translations(soup, dcard):
    """Localizes the Quick Facts widget, badge, labels, values, and amenity chips to Hungarian."""
    for qf in dcard.find_all(class_='qf1-wrap'):
        title = qf.find(class_='qf1-title')
        if title:
            title.string = "Gyors Tények — Helyszíni Adatlap"
        badge = qf.find(class_='qf1-badge')
        if badge:
            btxt = badge.get_text(strip=True)
            if btxt in QF_BADGES_HU:
                badge.string = QF_BADGES_HU[btxt]
        for row in qf.find_all(class_='qf1-row'):
            lbl = row.find(class_='qf1-label')
            if lbl:
                ltxt = lbl.get_text(strip=True)
                if ltxt in QF_LABELS_HU:
                    lbl.string = QF_LABELS_HU[ltxt]
            val = row.find(class_='qf1-val')
            if val:
                vtxt = val.get_text(strip=True)
                if vtxt in QF_VALS_HU:
                    val.string = QF_VALS_HU[vtxt]
        for chip in qf.find_all(class_='qf1-chip'):
            ctxt = chip.get_text(strip=True)
            if ctxt in QF_CHIPS_HU:
                chip.string = QF_CHIPS_HU[ctxt]


def apply_subpoints_translations(soup, dcard, card_idx, subpoints_dict):
    """Translates onboard walkthrough, audio guide, dining, and operator subpoints."""
    if card_idx not in subpoints_dict:
        return
    c_dict = subpoints_dict[card_idx]
    for sp in dcard.find_all(class_='ltt-sp-card'):
        h4 = sp.find('h4')
        h4_txt = h4.get_text(strip=True) if h4 else ''
        if h4_txt in c_dict:
            data = c_dict[h4_txt]
            if h4:
                h4.string = data.get('h4', h4_txt)
            if 'lis' in data:
                sp_lis = sp.find_all('li')
                for i, (title, desc) in enumerate(data['lis']):
                    if i < len(sp_lis):
                        target_li = sp_lis[i]
                        target_li.clear()
                        st = soup.new_tag('strong')
                        st.string = title
                        target_li.append(st)
                        target_li.append(f" {desc}")
            if 'ps' in data:
                sp_ps = sp.find_all('p')
                for i, p_txt in enumerate(data['ps']):
                    if i < len(sp_ps):
                        sp_ps[i].string = p_txt
                    else:
                        new_p = soup.new_tag('p')
                        new_p.string = p_txt
                        sp.append(new_p)


def create_pro_con_html(soup, pros_list, cons_list):
    """Builds the canonical Luxury Editorial Pros & Cons grid box with .w-richtext and <ul><li>."""
    wrapper = soup.new_tag('div', **{'class': 'pro-con-box-wrapper'})
    grid = soup.new_tag('div', **{'class': 'w-layout-grid grid-15'})
    wrapper.append(grid)
    
    # Pro Cell
    pro_cell = soup.new_tag('div', **{'class': 'pro-con-box-pro-cell', 'data-wf-pbl': 'layout-grid-1x2-vertical'})
    pro_rich = soup.new_tag('div', **{'class': 'pro-con-box-pro-cell-rich-text-block w-richtext'})
    h3_pro = soup.new_tag('h3')
    st_pro = soup.new_tag('strong')
    st_pro.string = "Előnyök:"
    h3_pro.append(st_pro)
    pro_rich.append(h3_pro)
    
    ul_pro = soup.new_tag('ul', **{'role': 'list'})
    for title, desc in pros_list:
        li = soup.new_tag('li')
        st = soup.new_tag('strong')
        st.string = title
        li.append(st)
        li.append(f" — {desc}")
        ul_pro.append(li)
    pro_rich.append(ul_pro)
    pro_cell.append(pro_rich)
    grid.append(pro_cell)
    
    # Con Cell
    con_cell = soup.new_tag('div', **{'class': 'pro-con-box-con-cell', 'data-wf-pbl': 'layout-grid-1x2-vertical'})
    con_rich = soup.new_tag('div', **{'class': 'pro-con-box-con-cell-rich-text-block w-richtext'})
    h3_con = soup.new_tag('h3')
    st_con = soup.new_tag('strong')
    st_con.string = "Hátrányok:"
    h3_con.append(st_con)
    con_rich.append(h3_con)
    
    ul_con = soup.new_tag('ul', **{'role': 'list'})
    for title, desc in cons_list:
        li = soup.new_tag('li')
        st = soup.new_tag('strong')
        st.string = title
        li.append(st)
        li.append(f" — {desc}")
        ul_con.append(li)
    con_rich.append(ul_con)
    con_cell.append(con_rich)
    grid.append(con_cell)
    
    return wrapper



def localize_buy_card(soup, buy_card, card_title=None):
    """Localizes an ltt-buy-card element: badge, price sub, perks, duration, dock, button, trust."""
    # 1. Badge
    badge = buy_card.find(class_='ltt-buy-card-badge')
    if badge:
        for span in badge.find_all('span'):
            if 'ltt-live-dot' not in span.get('class', []):
                span.string = "Hivatalos Jegyek & Élő Elérhetőség"
                
    # 2. Price sub
    psub = buy_card.find(class_='ltt-buy-price-sub')
    if psub:
        ptxt = psub.get_text()
        if 'per adult' in ptxt.lower():
            psub.string = "/ felnőtt"
        elif 'free cancellation' in ptxt.lower():
            psub.string = "Ingyenes lemondás"
            
    # 3. Title
    if card_title:
        title_el = buy_card.find(class_='ltt-buy-card-title')
        if title_el:
            title_el.string = card_title

    # 4. Perks
    perk_dock_map = {
        'Dock 7 (Vigadó tér)': '7-es kikötő (Vigadó tér)',
        'Margaret Bridge Dock': 'Margit híd kikötő',
        'Dock 10 (Erzsébet Bridge)': '10-es kikötő (Erzsébet híd)',
        'Dock 42 (Szent István Park)': '42-es kikötő (Szent István park)',
        'Dock 11 (Elizabeth Bridge)': '11-es kikötő (Erzsébet híd)',
        'Dock 3 (Akadémia)': '3-as kikötő (Akadémia)',
        'Vigadó tér Dock 5': 'Vigadó tér 5-ös kikötő',
        'Dock 7': '7-es kikötő',
        'Dock 11': '11-es kikötő',
        'Dock 3 (Gróf Széchényi)': '3-as kikötő (Gróf Széchenyi)',
        'Dock 6 (Jane Haining rkp.)': '6-os kikötő (Jane Haining rkp.)',
        'Jane Haining Dock 6': '6-os kikötő (Jane Haining rakpart)',
        'Dock 8A / Dock 11': '8A / 11-es kikötő',
        'Dock 8A': '8A kikötő'
    }
    
    perk_duration_map = {
        '60–70 Mins': '60–70 perc',
        '75–85 Mins': '75–85 perc',
        '60 Mins': '60 perc',
        '60–75 Mins': '60–75 perc',
        '75 Mins': '75 perc',
        '80 Mins': '80 perc',
        '90 Mins': '90 perc',
        '90–120 Mins': '90–120 perc',
        '120 Mins': '120 perc',
        '135 Mins': '135 perc',
        '150 Mins': '150 perc',
        '2.5 Hours': '2,5 óra',
        '90 Min': '90 perc',
        'All-Day Pass': 'Egész napos jegy'
    }
    
    for perk in buy_card.find_all(class_='ltt-buy-perk'):
        txt = perk.get_text()
        if 'Instant Smartphone QR Voucher' in txt:
            perk.string = "Azonnali mobiljegy (QR-kód)"
        elif 'Full Refund up to 24h Before' in txt:
            perk.string = "24 órás ingyenes lemondás"
        elif 'Departure:' in txt or 'Indulás:' in txt:
            st = perk.find('strong')
            st_txt = st.get_text(strip=True) if st else ''
            hu_dock = perk_dock_map.get(st_txt, st_txt)
            perk.clear()
            perk.append("Indulás: ")
            new_st = soup.new_tag('strong')
            new_st.string = hu_dock
            perk.append(new_st)
        elif 'Duration:' in txt or 'Időtartam:' in txt:
            st = perk.find('strong')
            st_txt = st.get_text(strip=True) if st else ''
            hu_dur = perk_duration_map.get(st_txt, st_txt)
            perk.clear()
            perk.append("Időtartam: ")
            new_st = soup.new_tag('strong')
            new_st.string = hu_dur
            perk.append(new_st)
            
    # 5. Button
    for cta in buy_card.find_all(class_='ltt-buy-cta-btn'):
        cta.string = "Foglalás most →"
        
    # 6. Trust
    trust = buy_card.find(class_='ltt-buy-card-trust')
    if trust:
        span = trust.find('span')
        if span:
            span.string = "Legjobb árgarancia • Azonnali visszaigazolás"


def localize_css_reviews(soup):
    """Replaces English 'Collapse Review' and 'Read Review' in CSS rules."""
    for style in soup.find_all('style'):
        if style.string:
            s = style.string
            s = s.replace('content: "Collapse Review";', 'content: "Értékelés összecsukása";')
            s = s.replace("content: 'Collapse Review';", 'content: "Értékelés összecsukása";')
            s = s.replace('content: "Read Review";', 'content: "Értékelés elolvasása";')
            s = s.replace("content: 'Read Review';", 'content: "Értékelés elolvasása";')
            style.string.replace_with(s)


def localize_proof_chips(soup):
    """Replaces ALL occurrences of 'Personally Tested' across proof badges, mobile chips, and text."""
    for tag in soup.find_all(class_=['bpa-vchip', 'bpa-proof-mobile']):
        if 'Personally Tested' in tag.get_text():
            tag.string = "✓ Személyesen tesztelve"
            
    for tag in soup.find_all(True):
        if tag.name not in ['script', 'style'] and tag.string and 'Personally Tested' in tag.string:
            tag.string = tag.string.replace('✓ Personally Tested', '✓ Személyesen tesztelve').replace('Personally Tested', '✓ Személyesen tesztelve')


def localize_breakdown_section(soup, cruise_type):
    """Localizes the Detailed Breakdown section header, subtitle, accordion controls, and TOC."""
    # 1. Heading
    for h2 in soup.find_all(['h2', 'h3']):
        htxt = h2.get_text()
        if 'Detailed Breakdown' in htxt or 'Részletes Elemzés' in htxt or 'Részletes Értékelés' in htxt:
            if cruise_type == 'river':
                h2.string = "Részletes Értékelés — 10 Legjobb Budapesti Sétahajózás"
            else:
                h2.string = "Részletes Értékelés — 7 Legjobb Budapesti Vacsorahajó"
    
    # Check by class bpa-breakdown-heading
    for bh in soup.find_all(class_='bpa-breakdown-heading'):
        if cruise_type == 'river':
            bh.string = "Részletes Értékelés — 10 Legjobb Budapesti Sétahajózás"
        else:
            bh.string = "Részletes Értékelés — 7 Legjobb Budapesti Vacsorahajó"
                
    # 2. Subtitle
    for sub in soup.find_all(class_='bpa-breakdown-sub'):
        sub.string = "Személyesen tesztelve • Minden értékelés nyitva • Kattintson a kinyitáshoz/becsukáshoz"
    for p in soup.find_all('p'):
        ptxt = p.get_text()
        if 'Personally field-tested' in ptxt or 'Személyesen tesztelve • Minden értékelés nyitva' in ptxt:
            p.string = "Személyesen tesztelve • Minden értékelés nyitva • Kattintson a kinyitáshoz/becsukáshoz"
            
    # 3. Accordion controls
    for btn in soup.find_all(class_='bpa-acc-ctrl-btn'):
        btxt = btn.get_text().strip()
        if btxt in ['Expand All', 'Mindet kinyit']:
            btn.string = "Mindet kinyit"
        elif btxt in ['Collapse All', 'Mindet becsuk']:
            btn.string = "Mindet becsuk"
            
    # 4. Table of Contents titles
    for toc_label in soup.find_all(class_=['title-small-3', 'title-small-6', 'ltt-toc-title']):
        toc_label.string = "Tartalomjegyzék"
    for div in soup.find_all(['div', 'span', 'p']):
        if div.string and 'table of contents' in div.string.strip().lower():
            div.string = "Tartalomjegyzék"


def insert_rubin_group_how_to_get_there(soup, dcard):
    """Ensures Rubin Group (Card #2) has complete '📍 Kikötő, Beszállás és Megközelítés' Bento section."""
    has_pier = any('Megközelítés' in bg.get_text() or 'Hogyan Juthat El' in bg.get_text() for bg in dcard.find_all('details', class_='ltt-bento-group'))
    if not has_pier:
        bentos = dcard.find_all('details', class_='ltt-bento-group')
        if len(bentos) >= 1:
            new_bg = soup.new_tag('details', **{'class': 'ltt-bento-group', 'open': ''})
            summary = soup.new_tag('summary', **{'class': 'ltt-bento-group-head'})
            title_span = soup.new_tag('span', **{'class': 'ltt-bento-group-title'})
            title_span.string = "📍 Kikötő, Beszállás és Megközelítés"
            summary.append(title_span)
            
            right_span = soup.new_tag('span', **{'class': 'ltt-bento-right'})
            pill_span = soup.new_tag('span', **{'class': 'ltt-mini-pill'})
            pill_span.string = "Kikötőtérkép"
            right_span.append(pill_span)
            chev_span = soup.new_tag('span', **{'class': 'ltt-bento-chev'})
            chev_span.string = "▾"
            right_span.append(chev_span)
            summary.append(right_span)
            new_bg.append(summary)
            
            body = soup.new_tag('div', **{'class': 'ltt-bento-group-body'})
            subpoints = soup.new_tag('div', **{'class': 'ltt-sub-points'})
            sp_card = soup.new_tag('div', **{'class': 'ltt-sp-card'})
            
            h4 = soup.new_tag('h4')
            h4.string = "Hogyan Juthat El a Kikötőbe & Beszállási Tudnivalók"
            sp_card.append(h4)
            
            ul = soup.new_tag('ul', **{'role': 'list'})
            
            li1 = soup.new_tag('li')
            st1 = soup.new_tag('strong')
            st1.string = "📍 Találkozási pont a térképen:"
            li1.append(st1)
            li1.append(" ")
            a1 = soup.new_tag('a', href="https://maps.google.com/?q=Szent+Istv%C3%A1n+park+5+Budapest", target="_blank", rel="noopener noreferrer")
            a1.string = "Budapest, Szent István park 5, 1137 (Margit híd északi ponton)"
            li1.append(a1)
            ul.append(li1)
            
            li2 = soup.new_tag('li')
            st2 = soup.new_tag('strong')
            st2.string = "Kiesőbb beszállási pont:"
            li2.append(st2)
            li2.append(" A kikötő a Margit hídtól északra található, ami kissé távolabb esik a központi Vigadó téri mólóktól, ezért célszerű 15–20 perccel korábban indulni.")
            ul.append(li2)
            
            li3 = soup.new_tag('li')
            st3 = soup.new_tag('strong')
            st3.string = "Megközelítés villamossal:"
            li3.append(st3)
            li3.append(" Szálljon fel a 2-es vagy 4/6-os villamosra a Jászai Mari térig. Onnan sétáljon 500 métert észak felé a Duna-parti sétányon a Szent István park magasságáig, amíg meg nem látja a piros „0”-s jelzésű beszállóhidat.")
            ul.append(li3)
            
            sp_card.append(ul)
            subpoints.append(sp_card)
            body.append(subpoints)
            new_bg.append(body)
            
            bentos[0].insert_after(new_bg)


def localize_dinner_decision_guide(soup):
    """Localizes the editorial decision guide at the bottom of the dinner cruises article."""
    sec = soup.find(id='dinner-cruise-decision-guide')
    if not sec:
        return
    badge = sec.find(class_='ltt-sec-badge')
    if badge:
        badge.string = "HELYSZÍNI TESZTELÉSI MÓDSZERTAN"
    title = sec.find(class_='ltt-sec-title')
    if title:
        title.string = "Hogyan Válassza Ki a Megfelelő Dunai Vacsorahajót?"
    sub = sec.find(class_='ltt-sec-subtitle')
    if sub:
        sub.string = "Négy kulcsfontosságú szempont, amelyet a budapesti vacsorahajók saját költségen végzett, névtelen tesztelése során vizsgálunk."
        
    cards = sec.find_all(class_='ltt-card')
    card_data = [
        ("Friss Fedélzeti Konyha vs. Előre Készített Catering", [
            "A vezető hajótársaságok, mint például a Legenda, saját fedélzeti konyhájukban, frissen készítik el a meleg ételeket rendelésre, míg a tömegturizmusra épülő büféhajók központi catering üzemekből szállított, melegen tartott tálcákból szolgálnak ki.",
            "Minden tesztelés során szigorúan ellenőrizzük az ételek hőmérsékletét, ízvilágát és a fogások felszolgálásának ütemezését."
        ]),
        ("Ablak Melletti Kilátás vs. Belső Asztalok", [
            "A kétszintes, zárt hajókon a középső folyosó menti asztalokról a kilátást zavarhatja az ablakokon tükröződő belső világítás és a többi utas. A Legenda hajlított üvegpanorámás szalonja azonban minden üléssorból akadálytalan kilátást nyújt a folyóra."
        ]),
        ("Akusztikai Egyensúly: Lounge vs. Zenés Műsor", [
            "Döntse el, hogy meghitt, romantikus beszélgetésre vágyik gyertyafénynél (a Legenda diszkrét lounge duójával), vagy élénk, lendületes kulturális szórakozást keres (a Silverline zongorapárbajával és folklór operett előadásával)."
        ]),
        ("Díszkivilágítás Időzítése & Indulási Kikötők", [
            "Ősszel és télen a korábbi, 19:00 órás járatok már teljes díszkivilágítás mellett hajóznak. Nyáron (júniustól augusztusig) a szürkület csak 20:45 körül áll be, így ekkor a 20:30–21:00 közötti indulási időpont az optimális választás."
        ])
    ]
    for idx, c in enumerate(cards):
        if idx < len(card_data):
            ctitle, cpars = card_data[idx]
            h3 = c.find(class_='ltt-card-title')
            if h3: h3.string = ctitle
            body = c.find(class_='ltt-card-body')
            if body:
                body.clear()
                for p_text in cpars:
                    p = soup.new_tag('p')
                    p.string = p_text
                    body.append(p)


def build_hungarian_home():
    print("Compiling Hungarian Homepage (hu/index.html)...")
    en_path = os.path.join(BASE_DIR, 'index.html')
    out_path = os.path.join(BASE_DIR, 'hu', 'index.html')
    
    soup = BeautifulSoup(open(en_path, 'r', encoding='utf-8').read(), 'html.parser')
    
    # 1. Metadata
    if soup.title:
        soup.title.string = "Budapesti Dunai Hajózás & Útikalauzok | Helyszínen Tesztelve (2026)"
    m_desc = soup.find('meta', {'name': 'description'})
    if m_desc:
        m_desc['content'] = "Független, helyszínen tesztelt dunai sétahajó és budapesti útikönyvek. Nappali és éjszakai hajóutak, gyertyafényes vacsorahajók, fürdők és rejtett költségek feltárása."
    og_title = soup.find('meta', {'property': 'og:title'})
    if og_title and soup.title: og_title['content'] = soup.title.string
    tw_title = soup.find('meta', {'name': 'twitter:title'})
    if tw_title and soup.title: tw_title['content'] = soup.title.string
    og_desc = soup.find('meta', {'property': 'og:description'})
    if og_desc and m_desc: og_desc['content'] = m_desc['content']
    tw_desc = soup.find('meta', {'name': 'twitter:description'})
    if tw_desc and m_desc: tw_desc['content'] = m_desc['content']
    can = soup.find('link', {'rel': 'canonical'})
    if can:
        can['href'] = "https://www.budapestadventures.com/hu/"
        
    html_tag = soup.find('html')
    if html_tag:
        html_tag['lang'] = 'hu'
        
    # Schema JSON-LD localization
    for s in soup.find_all('script', type='application/ld+json'):
        if s.string:
            s_txt = s.string
            s_txt = s_txt.replace('"inLanguage": "en"', '"inLanguage": "hu"')
            s_txt = s_txt.replace("10 Best River Cruises in Budapest in 2026 (Personally Tested)", "10 Legjobb Dunai Sétahajózás Budapesten 2026-ban (Személyesen Tesztelve)")
            s_txt = s_txt.replace("Experience Budapest's top-rated river cruises in 2026. Explore our personally vetted selection of day and night cruises in Budapest, featuring picturesque sightseeing cruises, dinner cruises, and lively booze cruises.", "Fedezze fel Budapest legjobb dunai sétahajóit 2026-ban. Személyesen tesztelt nappali, naplementés és éjszakai városnéző hajóutak, audio guide-ok és árak összehasonlítása.")
            s.string.replace_with(s_txt)

    localize_css_reviews(soup)
    localize_breakdown_section(soup, 'river')
        
    # 2. Navbar & Mega-Menu
    localize_navbar_and_menu(soup)
            
    # 3. Hero
    eyebrow = soup.find(class_='ltt-hero-eyebrow')
    if eyebrow:
        eyebrow.string = "HELYSZÍNEN TESZTELT DUNAI HAJÓZÁS ÉS BUDAPESTI ÚTIKALAUZOK • 2026-OS SZEZON"
        
    h1 = soup.find(class_='ltt-hero-title')
    if h1:
        h1.string = "Független, Helyszínen Tesztelt Dunai Sétahajó Értékelések Igényes Utazóknak"
        
    sub = soup.find(class_='ltt-hero-sub')
    if sub:
        sub.string = "Saját költségen tesztelt nappali, naplementés és esti dunai sétahajók, gyertyafényes vacsorák és budapesti útiterv-kalkulátorok. Helyi tapasztalat, rejtett költségek feltárása és közvetlen hajótársasági foglalás."
        
    # Stats strip
    labels = soup.find_all(class_='ltt-stat-label')
    stat_hu = [
        "Saját Költséges Tesztelés",
        "Hajótársaság Felmérve",
        "Helyszíni Hajózási Audit"
    ]
    for idx, lbl in enumerate(labels[:3]):
        lbl.string = stat_hu[idx]
        
    # Section header
    sec_title = soup.find(class_='ltt-dir-title')
    if sec_title:
        sec_title.string = "Budapesti Élmény- & Útikalauzok (2026)"
    sec_sub = soup.find(class_='ltt-dir-sub')
    if sec_sub:
        sec_sub.string = "Független, helyszínen felmért kalauzok a Duna hajózásához, gasztronómiájához és a város felfedezéséhez."
        
    # 4. Guide Cards (9 Cards - enforce NO spec pills per directive!)
    cards_hu = [
        {
            'tag': '🏆 FŐ ÚTIKALAUZ',
            'kicker': 'BUDAPESTI DUNA • 10 HAJÓTÁRSASÁG TESZTELVE',
            'title': '10 Legjobb Dunai Sétahajózás Budapesten (2026-os Részletes Teszt)',
            'excerpt': "A Legenda City Cruises üvegpanorámás, 30 nyelvű audio guide-os hajóitól a hangulatos esti boutique sétahajókig. Részletes indulási kikötőtérkép a Vigadó térnél, italfogyasztási opciók és objektív összehasonlítás.",
            'price': '€14 / fő-től',
            'btn': 'Kalauz Elolvasása →',
            'href': '/hu/setahajozas-a-dunan-budapest'
        },
        {
            'tag': '🍷 GYERTYAFÉNYES VACSORA',
            'kicker': 'ESTI GASZTRO • 7 HAJÓ TESZTELVE',
            'title': '7 Legjobb Dunai Vacsorahajó Budapesten (Személyesen Tesztelve)',
            'excerpt': "A Legenda 4 fogásos gyertyafényes lounge vacsorájától a Silverline élő zongorapárbajos és folklór operett műsoráig: ételek minősége, menüválaszték és a kivilágított Parlament panorámája.",
            'price': '€74 / fő-től',
            'btn': 'Kalauz Elolvasása →',
            'href': '/hu/setahajozas-a-dunan-vacsoraval'
        },
        {
            'tag': '✨ ÉJSZAKAI FÉNYEK',
            'kicker': 'KIVILÁGÍTOTT DUNA • 10 ÚTVONAL TESZTELVE',
            'title': 'A 10 Legjobb Esti és Éjszakai Sétahajózás Budapesten',
            'excerpt': "Naplementére és az esti díszkivilágításra időzítve. Fűtött panorámaszalonok és nyitott felső fedélzetek a Budai Vár és a Parlament akadálytalan éjszakai fotózásához.",
            'price': '€14 / fő-től',
            'btn': 'Kalauz Elolvasása →',
            'href': '/best-night-cruises-budapest'
        },
        {
            'tag': '🛥️ PRIVÁT BÉRLÉS',
            'kicker': 'VIP & CSOPORTOK • 5 PRIVÁT HAJÓ ÉRTÉKELVE',
            'title': '5 Legjobb Privát Hajótúra és Vízi Taxi Budapesten',
            'excerpt': "Autentikus velencei stílusú mahagóni vízi taxiktól a luxus privát jachtokig saját kapitánnyal, nyitott pezsgőbárral és egyéni beszállási lehetőségekkel.",
            'price': '€180 / hajó-tól',
            'btn': 'Kalauz Elolvasása →',
            'href': '/best-private-boat-tours-budapest'
        },
        {
            'tag': '🥂 KORLÁTLAN PROSECCO',
            'kicker': 'KORLÁTLAN ITALOK • 4 HAJÓ TESZTELVE',
            'title': 'Prosecco Hajó Budapest: A 4 Legjobb Korlátlan Italos Sétahajó',
            'excerpt': "Kitöltési sebesség, itallimit és hangulat összehasonlítása: laza naplementés pezsgőzés, Aperol Spritz és éjszakai bulihajók őszinte tesztje.",
            'price': '9 900 Ft / fő-től (€24)',
            'btn': 'Kalauz Elolvasása →',
            'href': '/hu/korlátlan-prosecco-hajóutazások-budapest'
        },
        {
            'tag': '♨️ TÖRTÉNELMI FÜRDŐK',
            'kicker': 'BUDAPESTI FÜRDŐK • 8 TESZTELT TERMÁL',
            'title': '8 Legjobb Budapesti Termálfürdő (Értékelve & Rangsorolva)',
            'excerpt': "A Széchenyi, Gellért, Rudas tetőtéri panorámamedencéje és a Lukács összehasonlítása: látogatottsági csúcsok, öltözők és jegyárak.",
            'price': '€28 / belépő-től',
            'btn': 'Kalauz Elolvasása →',
            'href': '/thermal-baths-budapest'
        },
        {
            'tag': '🚶 HELYI TÚRÁK',
            'kicker': 'VÁROSNÉZÉS • 6 TÚRA ÉRTÉKELVE',
            'title': '6 Legjobb Budapesti Gyalogos és Zsidó Negyed Gasztrotúra',
            'excerpt': "Romkocsma kulináris kóstolóktól a Várnegyed történelmi építészeti sétáiig engedéllyel rendelkező helyi idegenvezetőkkel.",
            'price': '€20 / fő-től',
            'btn': 'Kalauz Elolvasása →',
            'href': '/best-walking-tours-budapest'
        },
        {
            'tag': '💳 ÉRTÉKKALKULÁTOR',
            'kicker': 'INTERAKTÍV ESZKÖZ • 94 LÁTNIVALÓ AUDITÁLVA',
            'title': 'Budapest Kártya: Megéri? (2026-os Interaktív Kalkulátor)',
            'excerpt': "Számolja ki, hogy a hivatalos városkártyával valóban spórol-e. Hasonlítsa össze egyéni városnéző útitervét a hivatalos 2026-os múzeum- és fürdőárakkal.",
            'price': '€33-tól (24h–120h)',
            'btn': 'Kalkulátor Megnyitása →',
            'href': '/budapest-card-is-it-worth-it'
        },
        {
            'tag': '🛏️ PÉNZTÁRCABARÁT SZÁLLÁS',
            'kicker': 'SZÁLLÁSBUDAPEST • 10 HOSTEL AUDITÁLVA',
            'title': '10 Legjobb Hostel Budapesten (Személyesen Tesztelve)',
            'excerpt': "A VII. kerületi pörgős party hostelektől a digitális nomádoknak és egyéni utazóknak szánt csendes boutique kapszulahotelekig.",
            'price': '€15 / éj-től',
            'btn': 'Kalauz Elolvasása →',
            'href': '/best-hostels-budapest'
        }
    ]
    
    guide_cards = soup.find_all(class_=lambda c: c and ('ltt-guide-card' in c or 'ltt-guide-featured' in c))
    for idx, card in enumerate(guide_cards[:9]):
        cdata = cards_hu[idx]
        card['href'] = cdata['href']
        
        tag = card.find(class_='ltt-guide-tag')
        if tag: tag.string = cdata['tag']
        
        kicker = card.find(class_='ltt-guide-kicker')
        if kicker: kicker.string = cdata['kicker']
        
        title = card.find(class_='ltt-guide-title')
        if title: title.string = cdata['title']
        
        excerpt = card.find(class_='ltt-guide-excerpt')
        if excerpt: excerpt.string = cdata['excerpt']
        
        price = card.find(class_='ltt-guide-price') or card.find(class_='ltt-guide-price-val')
        if price: price.string = cdata['price']
        
        price_label = card.find(class_='ltt-guide-price-label')
        if price_label: price_label.string = 'Ár:'
        
        btn = card.find(class_='ltt-guide-btn')
        if btn: btn.string = cdata['btn']
        
    # 5. Manifesto Card
    man_h3 = soup.find(class_='ltt-manifesto-h3')
    if man_h3:
        man_h3.string = "Miért alakítottuk át a dunai hajózás értékelését"
    man_p = soup.find(class_='ltt-manifesto-p')
    if man_p:
        man_p.string = "A legtöbb utazási oldal általános promóciós leírásokat másol. Mi névtelenül, saját pénzből jegyet váltunk, felszállunk a hajókra, megkóstoljuk a menüt, teszteljük az audio guide-okat és fotózzuk a valós kilátást."
    man_btn = soup.find(class_='ltt-manifesto-btn')
    if man_btn:
        man_btn.string = "Olvassa el teljes módszertanunkat →"
        
    # 6. Author Bio Card (.ltt-author-box)
    author_box = soup.find(class_='ltt-author-box')
    if author_box:
        auth_role = author_box.find(class_='ltt-author-role')
        if auth_role:
            auth_role.string = "Alapító & Vezető Dunai Hajózási Szakértő"
            
        vbadges = author_box.find_all(class_='ltt-vbadge')
        badge_texts = [
            "✓ Helyszíni Dunai Auditok",
            "✓ 40+ Tesztelt Budapesti Hajó",
            "✓ Budapesti Születésű Utazási Szakíró"
        ]
        for b_idx, vb in enumerate(vbadges[:3]):
            vb.string = badge_texts[b_idx]
            
        bio = author_box.find(class_='ltt-author-bio')
        if bio:
            bio.string = (
                "Adam Dimitrov azért alapította a Budapest Adventurest, hogy szigorú, "
                "független értékeléseket nyújtson az utazóknak a dunai sétahajókról és budapesti élményekről. "
                "Budapesten élve személyesen vizsgálja az asztalok elhelyezkedését, a menetrend megbízhatóságát, "
                "az audiokommentár pontosságát és a beszállási logisztikát, hogy Ön minden alkalommal a megfelelő hajót válassza."
            )
            
        links_div = author_box.find(class_='ltt-author-links')
        if links_div:
            a_link = links_div.find('a')
            if a_link:
                a_link.string = "Tudjon meg többet tesztelési módszertanunkról és történetünkről →"
                a_link['href'] = "/about"
        
    # 6b. Schema JSON-LD localization & proof chips
    for s in soup.find_all('script', type='application/ld+json'):
        if s.string:
            s_txt = s.string
            s_txt = s_txt.replace("10 Best Danube River Cruises in Budapest (Personally Tested)", "10 Legjobb Dunai Sétahajózás Budapesten (Személyesen Tesztelve)")
            s_txt = s_txt.replace("10 Best Hostels in Budapest (Personally Tested)", "10 Legjobb Hostel Budapesten (Személyesen Tesztelve)")
            s_txt = s_txt.replace("7 Best Budapest Dinner Cruises on the Danube", "7 Legjobb Dunai Vacsorahajó Budapesten (Személyesen Tesztelve)")
            s_txt = s_txt.replace("Top Tested Danube River Cruises in Budapest (2026)", "Helyszínen Tesztelt Dunai Sétahajók Budapesten (2026)")
            s_txt = s_txt.replace("Independent field-tested reviews of Budapest Danube river cruises, dinner cruises, thermal baths, and local travel guides.", "Független, helyszínen tesztelt dunai sétahajó és budapesti útikönyvek.")
            s.string.replace_with(s_txt)
            
    localize_proof_chips(soup)

    # 7. Localized Footer
    localize_footer(soup)
        
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Hungarian Homepage saved to {out_path}")


# DATA FOR 10 RIVER CRUISES
# ==============================================================================
# HUNGARIAN SPECS & FLOATING BAR LOCALIZATION
# ==============================================================================
HU_SPECS_MAP = {
    # Durations
    '60–70 Mins': '⏱️ 60–70 perc',
    '75–85 Mins': '⏱️ 75–85 perc',
    '60 Mins': '⏱️ 60 perc',
    '75 Mins': '⏱️ 75 perc',
    '80 Mins': '⏱️ 80 perc',
    '90 Mins': '⏱️ 90 perc',
    '120 Mins': '⏱️ 120 perc',
    '135 Mins': '⏱️ 135 perc',
    '150 Mins': '⏱️ 150 perc',
    '⏱ 2.5 Hours': '⏱️ 2,5 óra',
    '⏱ 2.0–2.5 Hours': '⏱️ 2,0–2,5 óra',
    '⏱ 2.5–3.0 Hours': '⏱️ 2,5–3,0 óra',
    '⏱ 2.0 Hours': '⏱️ 2,0 óra',
    
    # Audio & Commentary
    '30-Language Audio Guide': '🎧 30 nyelvű audioguide',
    '30-Lang Audio': '🎧 30 nyelvű audioguide',
    'Audio Guide': '🎧 Audioguide',
    'App Audio': '📱 Applikációs audio',
    
    # Drinks & Dining
    '1 Welcome Drink': '🥂 1 üdvözlőital',
    'Welcome Drink': '🥂 Üdvözlőital',
    'Optional Drink': '🥂 Opcionális ital',
    'Welcome Champagne': '🥂 Üdvözlő pezsgő',
    'Welcome Prosecco': '🥂 Üdvözlő prosecco',
    '1 Drink Included': '🥂 1 ital a jegyben',
    '1 Drink': '🥂 1 ital',
    '2 Drinks': '🥂 2 ital',
    '2 Cocktails': '🍸 2 koktél',
    '2 Fresh Cocktails': '🍸 2 prémium koktél',
    'Unlimited Prosecco': '🥂 Korlátlan prosecco',
    'Unlimited Beer': '🍺 Korlátlan sör & üdítő',
    'Unlimited Wine & Beer': '🍷 Korlátlan bor & sör',
    'Wine Package': '🍷 Borcsomag',
    'Wine & Beer Tasting': '🍷 Bor- és sörkóstolás',
    'Full Bar': '🍸 Teljes fedélzeti bár',
    'Whole Pizza': '🍕 Egész meleg pizza',
    'Fresh Pizza': '🍕 Friss pizza',
    '12-Course Buffet': '🍽️ 12 fogásos svédasztal',
    '4-Course Fine Dining': '🍽️ 4 fogásos gourmet vacsora',
    '4-Course Gourmet': '🍽️ 4 fogásos gourmet',
    '4-Course Plated': '🍽️ 4 fogásos felszolgált menü',
    '4-Course Dinner': '🍽️ 4 fogásos vacsora',
    'Dinner Cruise': '🍽️ Vacsorahajó',
    
    # Music & Entertainment
    'Live Piano Duel': '🎹 Élő zongorapárbaj show',
    'Dual Grand Piano Duel': '🎹 Élő zongorapárbaj show',
    'Live Salon Music': '🎵 Élő szalonzene',
    'Background Music Only': '🎵 Kellemes háttérzene',
    'Live Acoustic Music': '🎸 Élő akusztikus zene',
    'Live Gypsy Music': '🎻 Élő cigányzene & tánc',
    'Live Gypsy Band & Dancers': '🎻 Élő cigányzenekar & táncosok',
    'Gypsy String Quartet': '🎻 Élő vonós cigányzenekar',
    'Live Folk Show': '💃 Élő folklórműsor',
    'Live Folk Trio': '🎻 Élő népzenei trió',
    'Folk Dance & Operetta': '💃 Folklór és operett műsor',
    'Folklore & Operetta': '💃 Folklór és operett műsor',
    'Folk Violin': '🎻 Élő népzene',
    'Upbeat Vibe': '✨ Koktélparti hangulat',
    'Candlelit Ambiance': '🕯️ Gyertyafényes hangulat',
    
    # Ship & Route
    'Full Danube Circuit': '🏛️ Teljes dunai körút',
    'Danube Loop': '🏛️ Teljes dunai körút',
    'Danube Route': '🏛️ Teljes dunai útvonal',
    'Night Route': '✨ Éjszakai útvonal',
    'Night Views': '✨ Éjszakai panoráma',
    'Parliament Views': '🏛️ Parlamenti panoráma',
    'Open Top Deck': '🌤️ Nyitott fedélzet',
    'Open Deck': '🌤️ Nyitott fedélzet',
    'Double-Decker': '🛳️ Kétszintes panorámahajó',
    'Historic Steamer': '⚓ 19. századi gőzhajó',
    '1847 Steamer': '⚓ 1847-es nosztalgia gőzhajó',
    'Steamer': '⚓ Történelmi gőzhajó',
    'Paddle Wheel': '⚙️ Lapátkerekes meghajtás',
    'Historic Salon': '🏛️ Patinás belső szalon',
    'Onboard Museum': '🏛️ Fedélzeti múzeum',
    'Budget Friendly': '💶 Pénztárcabarát',
    'Budget Fare': '💶 Kedvező jegyár',
    '40% Off Legenda': '💶 40%-kal olcsóbb',
    'Central Pier': '📍 Belvárosi kikötő',
    'Dock 11': '📍 11-es kikötő',
    'Hop-On Hop-Off': '🎟️ Hop-On Hop-Off körjárat',
    'Margaret Island': '🌳 Margitszigeti megálló',
    'Sunset Timing': '🌅 Naplementés menetrend',
    'Sunset Sailing': '🌅 Naplementés indulás',
    'Daytime Sightseeing': '☀️ Nappali városnézés',
    'Private Table': '🥂 Privát asztal garantált'
}

HU_RIVER_SHORT_TITLES = [
    "Legenda Városnéző Sétahajó 30 Nyelvű Audióval & Itallal",
    "Rubin Group Korlátlan Prosecco & Aperol Hajóút",
    "Kisfaludy Autentikus 19. Századi Lapátkerekes Gőzhajó",
    "Portum Lines Modern Sétahajó + Üdvözlőital",
    "Silverline Fapados Belvárosi Városnéző Hajóút",
    "Silverline Naplementés Hajózás 2 Friss Koktéllal",
    "Silverline Pizzás Hajózás Korlátlan Sörrel & Üdítővel",
    "Hungária Koncert 12 Fogásos Büfévacsora & Folklór Show",
    "Hungária Koncert Folklór Italos Hajóút Élő Hegedűvel",
    "Mahart PassNave Hop-On Hop-Off Dunai Körjárat"
]

HU_DINNER_SHORT_TITLES = [
    "Legenda 4 Fogásos Romantikus Gyertyafényes Vacsorahajó Élő Zenével",
    "Silverline 4 Fogásos Vacsorahajó Élő Zene Nélkül",
    "Silverline 4 Fogásos Vacsorahajó Folklór Operett Műsorral",
    "Silverline 4 Fogásos Vacsorahajó Élő Zongorapárbaj Show-val",
    "Hungária Koncert 12 Fogásos Svédasztalos Vacsorahajó & Folklór",
    "Eurama 4 Fogásos Vacsorahajó Klasszikus Cigányzenével",
    "Silverline 4 Fogásos Vacsorahajó Élőzenével és Korlátlan Itallal"
]

def localize_floating_bar(soup, cruise_type, total_count, short_titles, toc_deck_label, toc_breakdown_label):
    bar = soup.find(id='sticky-bar')
    if bar:
        toc_btn = bar.find(id='hybridTocBtn')
        if toc_btn:
            span = toc_btn.find('span')
            if span:
                span.string = f"Mind a {total_count} dunai {'sétahajó' if cruise_type == 'river' else 'vacsorahajó'}"
                
        top_btn = bar.find(class_='hybrid-top-btn')
        if top_btn:
            span = top_btn.find('span')
            if span: span.string = "Fel"
            
        s_rank = bar.find(id='sticky-rank')
        if s_rank: s_rank.string = "#1 VÁLASZTÁS"
        
        s_name = bar.find(id='sticky-name')
        if s_name and short_titles: s_name.string = short_titles[0]
        
        s_trust = bar.find(class_='hybrid-active-trust')
        if s_trust: s_trust.string = "24 órás ingyenes lemondás"
        
        s_btn = bar.find(id='sticky-cta-btn')
        if s_btn: s_btn.string = "Foglalás most →"
        
    sheet = soup.find(id='hybridSheet')
    if sheet:
        stitle = sheet.find(class_='hybrid-sheet-title')
        if stitle:
            stitle.string = f"Ugrás a tesztelt budapesti {'sétahajókhoz' if cruise_type == 'river' else 'vacsorahajókhoz'}"
            
    # Update window.LTT_PAGE_CONFIG script tag
    for s in soup.find_all('script'):
        if s.string and 'window.LTT_PAGE_CONFIG' in s.string:
            cfg = {
                "deckId": "budapest-river-cruise-deck" if cruise_type == 'river' else "budapest-dinner-cruise-deck",
                "tocDeckLabel": toc_deck_label,
                "tocBreakdownLabel": toc_breakdown_label,
                "pickLabel": "VÁLASZTÁS",
                "btnText": "Foglalás most →",
                "shortTitles": short_titles
            }
            s.string = f"window.LTT_PAGE_CONFIG = {json.dumps(cfg, ensure_ascii=False)};"
            break


RIVER_PROS_CONS = [
    # Card 1 (Legenda)
    ([
        ("A Legjobb Összességében", "Ez a sétahajózás mindent tartalmaz a tökéletes városnézéshez."),
        ("Üdvözlőital a Jegyárban", "Választható pezsgő, minőségi bor, sör, üdítő vagy ásványvíz."),
        ("Kiváló Hajók", "Modern, tágas és kifogástalanul karbantartott hajók, mindkét fedélzetről páratlan kilátással."),
        ("Prémium Audio Guide", "Kristálytiszta hangminőség egyéni fejhallgatón keresztül, 30 választható nyelven."),
        ("Teljes Dunai Útvonal", "Lefedi az összes kiemelt látnivalót a Margitszigettől a Nemzeti Színházig és Művészetek Palotájáig."),
        ("Családbarát Kedvezmények", "0–9 éves korig ingyenes, 10–14 éves korig 50% kedvezmény a jegyárból.")
    ], [
        ("Magasabb Árkategória", "Kissé drágább az átlagos hajójegyeknél, de a nyújtott prémium minőség és kényelem bőségesen kárpótol érte."),
        ("Szezonális Ingyenes Limonádé", "Az ingyenes házi limonádé kizárólag a nyári főszezonban érhető el a felső teraszon."),
        ("Fejhallgató Kényelem", "A vezetékes fejhallgatók zsinórja magas utasok számára néha feszes lehet ülve.")
    ]),
    # Card 2 (Rubin Group)
    ([
        ("#1 Legkedvezőbb Árú Korlátlan Italos Hajóút", "Budapest legköltséghatékonyabb korlátlan prosecco hajóútja a Dunán."),
        ("Kiváló Rendezvényhajó", "Hangulatos szabadtéri felső kilátóterasz és két elegáns belső fedélzet koktélparti atmoszférával."),
        ("Valóban Korlátlan Italfogyasztás", "A figyelmes felszolgálók folyamatosan újratöltik a minőségi proseccót és a frissítő limonádét."),
        ("Kényelmes 75 Perces Menetidő", "Több mint elegendő idő az italok élvezetére és a kivilágított budapesti panoráma megcsodálására.")
    ], [
        ("Középszerű Opcionális Ételtál", "A 10 eurós feláras hidegtál minősége átlagos, nem éri el a gourmet színvonalat."),
        ("Kiesőbb Kikötői Indulópont", "A Margit hídhoz közeli kikötő kissé távolabb esik a belvárosi Vigadó téri fő sétánytól."),
        ("Hangszórós Audiokalauz Zaja", "A társasági zsongás és zene miatt a hangszórókból szóló ismertető nehezebben hallható.")
    ]),
    # Card 3 (Kisfaludy Steamboat)
    ([
        ("Autentikus 19. Századi Gőzhajó", "Az egyetlen történelmi stílusú, faborítású nosztalgiahajó a Dunán (az 1846-os Kisfaludy replikája)."),
        ("Fedélzeti Múzeumi Kiállítás", "Az alsó szalonban gazdag kiállítás mutatja be a 19. századi dunai gőzhajózás aranykorát."),
        ("Üdvözlőital a Jegyárban", "A jegy tartalmaz egy pohár pezsgőt, magyar bort, sört vagy üdítőt beszálláskor."),
        ("Központi 10-es Kikötő", "Közvetlenül a fehér Erzsébet híd pesti hídfőjétől indul a Duna-korzón.")
    ], [
        ("Kisebb Nyitott Fedélzeti Férőhely", "A lapátkerekes kialakítás miatt a korlát melletti külső helyek gyorsabban megtelnek."),
        ("Hangszórós Idegenvezetés", "A narráció a központi hangszórókból szól, nem egyéni fejhallgatón keresztül.")
    ]),
    # Card 4 (Portum Lines)
    ([
        ("Kiváló Ár-Érték Arány", "40–50%-kal kedvezőbb árú, mint a Legenda, miközben modern, tiszta és minőségi hajózási élményt nyújt."),
        ("Fiatalos, Lendületes Légkör", "Kellemes, modern atmoszféra háttérzenével és barátságos kiszolgálással."),
        ("Minőségi Üdvözlőital", "Választható behűtött prosecco, szezonális koktél, forralt bor vagy üdítő."),
        ("Modern, Kétszintes Hajó", "Jól karbantartott belső panorámaszalon és tágas felső nyitott fedélzet.")
    ], [
        ("Szent Gellért Téri Indulás", "A budai 0-s kikötőből indul a Gellért térnél, így a pesti belvárosból át kell sétálni a Szabadság hídon."),
        ("Csúcsidőben Zsúfolt Lehet", "Népszerű járatain a felső terasz hamar megtelik a főszezonban."),
        ("Korlátozott Külső Asztalok", "A felső fedélzeti asztalok érkezési sorrendben foglalhatók el.")
    ]),
    # Card 5 (Silverline No-Frills)
    ([
        ("Központi 11-es Kikötői Beszállás", "Közvetlenül az Erzsébet híd pesti lábánál, lépésekre a Váci utcától és a 2-es villamostól."),
        ("Alacsony Jegyár", "Minden felesleges extrát elhagyva a 60 perces városnéző jegy már €12–14 között elérhető."),
        ("Sűrű Menetrend", "Egész nap folyamatosan indul 11:00 és 22:00 között."),
        ("Tágas Kétszintes Hajó", "Nagy befogadóképességű katamarán nyitott felső kilátófedélzettel.")
    ], [
        ("Nincs Üdvözlőital", "Még az ásványvízért is külön fizetni kell a fedélzeti büfében."),
        ("Csak Letölthető Applikációs Audio Guide", "Nincs beépített fejhallgató, az ismertető saját okostelefonon és mobilneten érhető el.")
    ]),
    # Card 6 (Silverline Cocktails)
    ([
        ("Két Teljes Méretű Koktél a Jegyben", "2 frissen kevert klasszikus koktél (Mojito, Pina Colada, Cuba Libre, Tequila Sunrise) jár személyenként."),
        ("Teljes 60–80 Perces Útvonal", "A Margit hídtól a Nemzeti Színházig a teljes budapesti panorámaszakaszt bejárja."),
        ("Kényelmes Katamarán Szalon", "Párnázott belső boxok és szellős nyitott felső terasz a kilátáshoz."),
        ("Központi Petőfi Téri Kikötő", "Kényelmesen megközelíthető a belvárosból.")
    ], [
        ("Nincs Történelmi Idegenvezetés", "Kifejezetten hangulatos koktélozós, zenés estére tervezték, nem városnéző túrára."),
        ("Nyitott Sorban Állás", "A 11-es ponton várakozóhelye eső és erős nap ellen nem fedett.")
    ]),
    # Card 7 (Silverline Pizza & Beer)
    ([
        ("Korlátlan Sör- és Üdítőfogyasztás", "A 75 perces út alatt korlátlan csapolt sör, Pepsi termékek és ásványvíz."),
        ("Friss Meleg Pizza az Asztalhoz", "Választható sonkás, szalámis, négysajtos, magyaros vagy margherita pizza."),
        ("Laza, Vidám Társasági Hangulat", "Kiváló baráti társaságoknak, egyetemistáknak és fiatal pároknak a vacsora előtti alapozáshoz.")
    ], [
        ("Kompakt Sütőben Melegített Pizza", "A hajókonyha kompakt villanysütőiben sül, nem fatüzelésű pizzériában."),
        ("Belső Ablakoszlopok", "Néhány lenti asztal látószögét szerkezeti oszlopok zavarhatják; étkezés után érdemes a tetőre menni fotózni.")
    ]),
    # Card 8 (Hungaria Koncert Dinner Cruise)
    ([
        ("Gazdag Svédasztalos Büfékínálat", "Tradicionális magyaros melegételek és hidegtálak korlátlan fogyasztással."),
        ("Két Ajándék Üdvözlőital", "Egy pohár pezsgő beszálláskor és egy választható ital az étkezéshez."),
        ("Élő Folklórest & Cigányzene", "Elismert néptáncosok és autentikus hegedűművészek élő előadása a szalonban."),
        ("Teljes Dunai Körút", "Hosszú, 90 perces menetidő a Margitszigettől a Művészetek Palotájáig.")
    ], [
        ("Kevésbé Ideális Fotózásra", "A belső szalonra és a műsorra fókuszál, a nyitott kilátóterület korlátozottabb."),
        ("Büfé Jellegű Gasztronómia", "Bőséges és finom, de nem prémium fine dining tányérszerviz.")
    ]),
    # Card 9 (Hungaria Koncert Drinks Cruise)
    ([
        ("Élő Népi Hegedűtrió", "Autentikus magyar vonószene, a koncert végén közönségkérésekkel."),
        ("Klasszikus Századfordulós Gőzös Hangulat", "A patinás Gróf Széchenyi díszes faborítású szalonjában hajózik."),
        ("Változatos Itallehetőségek", "Választható borkóstoló, minőségi kézműves sörök vagy koktélok."),
        ("Akadémia Kikötő a Parlament Mellett", "Közvetlenül a Lánchíd és az Országház közötti 3-as mólóról indul.")
    ], [
        ("Közös Hajó a Vacsorázó Vendégekkel", "A csak italt fogyasztó utasok az alsó fedélzeten ülnek, miközben a felső szinten vacsoráznak."),
        ("90 Perces Menetidő", "Nyugodtabb, lassabb tempójú hajózás.")
    ]),
    # Card 10 (Duna Cruises / Mahart)
    ([
        ("A Legolcsóbb Dunai Hajójegy", "Ideális a legalacsonyabb költségvetéssel utazóknak."),
        ("Központi Vigadó Téri Kikötés", "Közvetlenül a belvárosi pesti rakpartról indul."),
        ("Egyszerű Panorámaút", "Alapszintű 60 perces városnézés felesleges sallangok nélkül.")
    ], [
        ("Puritán Fedélzeti Kényelem", "Egyszerű, kopottabb berendezés és kemény műanyag ülések."),
        ("Nincs Ingyenes Ital vagy Audio Guide", "Semmilyen kiegészítő szolgáltatást nem tartalmaz a jegyár."),
        ("Gyakran Zsúfolt Diákcsoportokkal", "A nagy befogadóképesség miatt gyakran iskolás csoportok töltik meg a fedélzetet.")
    ])
]


# HARVESTED SUMMARY REVIEWS FOR RIVER CARDS
RIVER_SUMMARIES = {
    0: [ # Legenda
        "A Legenda folyami hajóútja a legteljesebb és legkifinomultabb városnéző élményt nyújtja Budapesten, minőségi üdvözlőitallal és 30 nyelven elérhető professzionális audio guide-dal.",
        "A hangos ismertető 30 nyelven érhető el: magyar, angol, német, francia, olasz, spanyol és számos egyéb nyelven. A hangminőség az egyéni fülhallgatóknak köszönhetően kristálytiszta.",
        "Modern és tágas panorámahajóik mindkét fedélzetről kiváló kilátást biztosítanak. Az útvonal a Margitszigettől a Nemzeti Színházig és a Müpáig terjedő ikonikus látnivalók mindegyikét érinti.",
        "A hajóút során a belső világítás le van kapcsolva, ami megszünteti a zavaró tükröződést a hatalmas panorámaüvegeken, így tökéletes éjszakai fotókat készíthet.",
        "Bár a jegyár a magasabb kategóriába tartozik, a kimagasló szolgáltatás és a hibátlan szervezés teljes mértékben igazolja az árát."
    ],
    1: [ # Rubin Group
        "A Rubin Group hajótúrája kiváló választás azoknak, akik megfizethető koktélparti hangulatot keresnek korlátlan prosecco és limonádé mellett. A figyelmes felszolgálók mindig készen állnak, hogy tele legyen a vendégek pohara.",
        "A felső fedélzetről lélegzetelállító 360°-os kilátás nyílik a városra a 75 perces folyami hajóút alatt, míg a két fedett fedélzet hangulatos és hívogató hangulatot kínál.",
        "Ami ennek a körútnak a kevésbé rózsás aspektusait illeti, az opcionális ételtál nem éri meg a 10 eurós felárat, és az audiokalauzt is nehezebb lehet hallani a társasági partizajtól. Ezenkívül a találkozási pont távolabb van a belvárosi Vigadó tértől, így az odajutás több időt igényelhet.",
        "Összességében, ha egy kellemes, kötetlen dunai hajózásra vágyik korlátlan italokkal és lenyűgöző esti panorámával, a Rubin Group hajókirándulása kiemelkedő ár-érték arányú választás."
    ],
    2: [ # Kisfaludy
        "Ez Budapest egyetlen sétahajózása, amely autentikus 19. századi történelmi élményt kínál az 1846-os Kisfaludy lapátkerekes gőzhajó hű replikájának fedélzetén.",
        "A hajóút egy választott üdvözlőitalt és igényes angol nyelvű audiokommentárt tartalmaz. Az alsó fedélzeten egy lenyűgöző hajózástörténeti múzeumi kiállítás tekinthető meg a reformkori dunai gőzhajózásról.",
        "A 60 perces út során kényelmesen megcsodálhatók a budapesti hidak és a Parlament a fa szalonok nosztalgikus eleganciájában."
    ],
    3: [ # Portum Lines
        "A Portum Lines hajózása kiváló és megfizethető alternatívája a Legendának: modern, tiszta és fiatalos hajójukon minőségi városnézésben lehet része 40-50%-kal alacsonyabb áron.",
        "A felszálláskor a vendégeket behűtött üdvözlőital fogadja (prosecco, forralt bor, koktél vagy üdítő). A kétszintes hajó tágas felső fedélzete nagyszerű kilátást biztosít a hidakra és a Várnegyedre.",
        "Tökéletes kompromisszum azoknak az utazóknak, akik prémium hangulatra vágynak baráti áron."
    ],
    4: [ # Silverline No-Frills
        "A Silverline fapados városnéző hajója kifejezetten a büdzsé-tudatos utazóknak készült: elhagyja a kötelező italokat és catering költségeket, így a legalacsonyabb áron kínál 75 perces dunai hajózást.",
        "A központi 11-es kikötőből (Petőfi tér / Erzsébet híd) induló katamarán tágas felső terasszal rendelkezik, ahonnan akadálytalanul fotózható a kivilágított Parlament.",
        "Ajánlott azoknak, akik egyszerűen csak a folyami panorámát szeretnék élvezni rejtett felárak nélkül."
    ],
    5: [ # Silverline Cocktails
        "Két frissen kevert, prémium koktéllal a kézben hajózni a naplementében az egyik leghangulatosabb esti program a Duna fővárosi szakaszán.",
        "A Silverline 80 perces koktélos hajóútja laza lounge zenével és kényelmes belső kanapékkal várja a párokat és társaságokat, miközben a Margit hídtól a Nemzeti Színházig bejárja a várost.",
        "Kiváló felvezetés egy budapesti éjszakai szórakozáshoz vagy vacsorához."
    ],
    6: [ # Silverline Pizza & Beer
        "Frissen sült meleg pizza az asztalhoz szervírozva, korlátlan csapolt sörrel és üdítővel kísérve: a Silverline pizzás hajója a laza, vidám társasági esték kedvence.",
        "A 75 perces hajóút során 5 különböző pizzatípus közül választhat, miközben a hajó a kivilágított Országház és a Budai Vár előtt halad el.",
        "Különösen népszerű egyetemisták, baráti társaságok és fiatal családok körében."
    ],
    7: [ # Hungaria Koncert Dinner
        "A Hungaria Koncert gazdag büfévacsorás hajóútja a tradicionális magyar gasztronómia és a népművészet legjavát egyesíti.",
        "Az utazók korlátlan svédasztalról válogathatnak a magyaros fogásokból (gulyásleves, pörköltek, rétesek), miközben díjnyertes néptáncosok és autentikus hegedűművészek élő műsorát élvezik.",
        "Hosszú, 90 perces menetidővel garantálja a teljes kikapcsolódást és a gazdag élményt."
    ],
    8: [ # Hungaria Koncert Drinks & Violin
        "Ha egy kellemes esti dunai hajózásra vágyik autentikus élő hegedűmuzsikával, de nem szeretne komplett vacsorát fogyasztani, ez a Hungaria Koncert italos hajótúra a legjobb választás.",
        "A vendégek a patinás Gróf Széchenyi díszes, századfordulós fa szalonjában kóstolhatnak minőségi borokat vagy kézműves söröket, miközben a népzenei trió a legszebb melódiákat játssza.",
        "Kifejezetten hangulatos, kulturális élmény a Parlament szomszédságából indulva."
    ],
    9: [ # Duna Cruises / Mahart
        "Budapest legolcsóbb belépő szintű dunai városnéző sétahajója, amely a legegyszerűbb, sallangmentes panorámaélményt nyújtja a Vigadó térről.",
        "Bár a fedélzeti kényelem és a felszereltség puritán, a 60 perces útvonal pontosan ugyanazokat az ikonikus látványosságokat mutatja meg, mint a drágább hajók.",
        "Ideális választás a legszigorúbb költségvetésből gazdálkodó hátizsákos utazóknak."
    ]
}


def build_hungarian_river():
    print("Compiling Hungarian River Guide (hu/setahajozas-a-dunan-budapest/index.html)...")
    en_path = os.path.join(BASE_DIR, 'river.html')
    out_path = os.path.join(BASE_DIR, 'hu', 'setahajozas-a-dunan-budapest', 'index.html')
    
    soup = BeautifulSoup(open(en_path, 'r', encoding='utf-8').read(), 'html.parser')
    
    # 1. Head Metadata
    if soup.title:
        soup.title.string = "10 Legjobb Dunai Sétahajózás Budapesten 2026-ban (Személyesen Tesztelve)"
    m_desc = soup.find('meta', {'name': 'description'})
    if m_desc:
        m_desc['content'] = "Fedezze fel Budapest legjobb dunai sétahajóit 2026-ban. Személyesen tesztelt nappali, naplementés és éjszakai városnéző hajóutak, audio guide-ok és árak összehasonlítása."
    og_title = soup.find('meta', {'property': 'og:title'})
    if og_title and soup.title: og_title['content'] = soup.title.string
    tw_title = soup.find('meta', {'name': 'twitter:title'})
    if tw_title and soup.title: tw_title['content'] = soup.title.string
    og_desc = soup.find('meta', {'property': 'og:description'})
    if og_desc and m_desc: og_desc['content'] = m_desc['content']
    tw_desc = soup.find('meta', {'name': 'twitter:description'})
    if tw_desc and m_desc: tw_desc['content'] = m_desc['content']
    can = soup.find('link', {'rel': 'canonical'})
    if can:
        can['href'] = "https://www.budapestadventures.com/hu/setahajozas-a-dunan-budapest"
    html_tag = soup.find('html')
    if html_tag:
        html_tag['lang'] = 'hu'
        
    # Schema JSON-LD localization
    for s in soup.find_all('script', type='application/ld+json'):
        if s.string:
            s_txt = s.string
            s_txt = s_txt.replace('"inLanguage": "en"', '"inLanguage": "hu"')
            s_txt = s_txt.replace("10 Best River Cruises in Budapest in 2026 (Personally Tested)", "10 Legjobb Dunai Sétahajózás Budapesten 2026-ban (Személyesen Tesztelve)")
            s_txt = s_txt.replace("10 Best Danube River Cruises in Budapest (Personally Tested)", "10 Legjobb Dunai Sétahajózás Budapesten (Személyesen Tesztelve)")
            s_txt = s_txt.replace("Detailed Breakdown — 10 Best River Cruises in Budapest", "Részletes Értékelés — 10 Legjobb Budapesti Sétahajózás")
            s_txt = s_txt.replace("Experience Budapest's top-rated river cruises in 2026.", "Fedezze fel Budapest legjobb dunai sétahajóit 2026-ban.")
            s.string.replace_with(s_txt)

    localize_css_reviews(soup)
    localize_breakdown_section(soup, 'river')
        
    # 2. Navbar & Mega-Menu
    localize_navbar_and_menu(soup)

    # 3. Clean Card Hero
    for bc in soup.find_all(class_='ltt-breadcrumbs'):
        bc.clear()
        home_a = soup.new_tag('a', href='/hu/')
        home_a.string = 'Főoldal'
        sep = soup.new_tag('span', **{'class': 'ltt-bc-sep'})
        sep.string = '›'
        curr = soup.new_tag('span', **{'class': 'ltt-bc-current'})
        curr.string = 'Dunai Sétahajózás Budapesten'
        bc.append(home_a)
        bc.append(' ')
        bc.append(sep)
        bc.append(' ')
        bc.append(curr)
            
    badge = soup.find(class_='ltt-hero-kicker-badge')
    if badge:
        badge.string = "✓ 2026-OS HELYSZÍNEN TESZTELT ÖSSZEHASONLÍTÁS"
        
    h1 = soup.find(class_='ltt-editorial-h1')
    if h1:
        h1.string = "10 Legjobb Dunai Sétahajózás Budapesten 2026-ban (Személyesen Tesztelve)"
        
    author_line = soup.find(class_='ltt-author-line')
    if author_line:
        author_line.clear()
        author_line.append("Szerző: ")
        a_tag = soup.new_tag('a', href="/about")
        a_tag.string = "Adam Dimitrov"
        author_line.append(a_tag)
        author_line.append(" — Alapító & Vezető Kutató")
        
    author_role = soup.find(class_='ltt-author-role')
    if author_role:
        author_role.string = "Független helyszíni felmérések • Saját fotók és videók • Elfogulatlan értékelések"
        
    tp = soup.find(class_='ltt-trust-pill')
    if tp:
        tp.clear()
        st = soup.new_tag('strong')
        st.string = 'Frissítve'
        tp.append(st)
        tp.append(': 2026. november')
    updated = soup.find(class_='ltt-updated-date')
    if updated:
        updated.string = "Utoljára frissítve: 2026. november"
        
    lead = soup.find(class_='ltt-lead-copy')
    if lead:
        lead.clear()
        p1 = soup.new_tag('p')
        p1.string = "Túlterheltnek érzi magát a budapesti dunai sétahajó-lehetőségek sokaságától? A belvárosi Duna-parton tucatnyi hajótársaság kínál különböző útvonalakat, a fűtött üvegszalonos luxushajóktól az egyszerű büféhajókig."
        p2 = soup.new_tag('p')
        p2.string = "Minden hajót személyesen teszteltünk névtelen utasként, hogy megmutassuk a valóságot: beszállási logisztika, audio guide minőség, kilátás a fedélzetről és a valódi ár-érték arány."
        lead.append(p1)
        lead.append(p2)
        
    # Filter Pills
    filter_label = soup.find(class_='ltt-filter-label')
    if filter_label:
        filter_label.string = "Szűrés:"
        
    tab_btns = soup.find_all(class_='ltt-tab-btn')
    hu_tabs = [
        "Összes (10)",
        "✓ Személyesen tesztelve (5)",
        "🎧 Audio guide-dal (5)",
        "🥂 Üdvözlőitallal (6)",
        "🍷 Korlátlan ital (3)",
        "🏛️ Történelmi & Városnéző (4)"
    ]
    for idx, btn in enumerate(tab_btns[:6]):
        btn.string = hu_tabs[idx]
        
    # 4. 10 Deck Cards Localization
    cards_hu = [
        {
            'rank': '🏆 #1 Legjobb Választás',
            'kicker': 'Legenda City Cruises • ⏱️ 60–70 perc • 7-es kikötő (Vigadó tér)',
            'title': 'Budapesti Nappali vagy Éjszakai Sétahajózás Audio Guide-dal (30 Nyelven) & Üdvözlőitallal',
            'best_for': '🎯 Ideális választás: Első budapesti utazók, párok és családok, akik prémium panorámára vágynak.',
            'price': '€20–25'
        },
        {
            'rank': '🥂 #2 Legjobb Korlátlan Ital',
            'kicker': 'Rubin Group • ⏱️ 75–85 perc • Margit híd kikötő',
            'title': 'Budapesti Éjszakai Hajóút Korlátlan Italfogyasztással (Prosecco, Sör, Bor)',
            'best_for': '🎯 Ideális választás: Baráti társaságok és bulizni vágyók, akik korlátlan italokra vágynak naplemente után.',
            'price': '€25'
        },
        {
            'rank': '⚓ #3 Történelmi Gőzhajó',
            'kicker': 'Dunai Sétahajózási Kft. • ⏱️ 60 perc • 10-es kikötő (Erzsébet híd)',
            'title': 'Budapesti Városnéző Sétahajózás egy 19. Századi Autentikus Gőzhajón',
            'best_for': '🎯 Ideális választás: Történelemkedvelők és a vintage hajózás szerelmesei.',
            'price': '€10–32'
        },
        {
            'rank': '💶 #4 Legjobb Ár-Érték',
            'kicker': 'Portum Lines • ⏱️ 60 perc • 0-s kikötő (Szent Gellért tér)',
            'title': 'Budapesti Városnéző Hajóút Üdvözlőitallal (Portum Lines)',
            'best_for': '🎯 Ideális választás: Pénztárcabarát utazók, akik minőségi üdvözlőitalt keresnek.',
            'price': '€14'
        },
        {
            'rank': '💰 #5 Fapados Hajózás',
            'kicker': 'Silverline Cruises • ⏱️ 75 perc • 11-es kikötő (Petőfi tér)',
            'title': 'Sallangmentes Budapesti Folyami Hajóút (Silverline)',
            'best_for': '🎯 Ideális választás: Utazók, akik csak a dunai panorámát keresik extra költségek nélkül.',
            'price': '€12–14'
        },
        {
            'rank': '🍸 #6 Koktélos Hajóút',
            'kicker': 'Silverline Cruises • ⏱️ 80 perc • 11-es kikötő (Petőfi tér)',
            'title': 'Budapesti Városnéző Hajóút Két Prémium Koktéllal',
            'best_for': '🎯 Ideális választás: Koktélkedvelők és párok egy hangulatos esti Duna-parti koccintásra.',
            'price': '€32–37'
        },
        {
            'rank': '🍕 #7 Pizzás Hajózás',
            'kicker': 'Silverline Cruises • ⏱️ 75 perc • 11-es kikötő (Petőfi tér)',
            'title': 'Budapesti Folyami Hajóút Friss Pizzával és Üdvözlőitallal',
            'best_for': '🎯 Ideális választás: Családok és barátok egy laza vacsorára a Dunán.',
            'price': '€35–39'
        },
        {
            'rank': '🎻 #8 Büfévacsora & Folklór',
            'kicker': 'Hungaria Koncert • ⏱️ 90 perc • Akadémia kikötő',
            'title': 'Svédasztalos Vacsorahajó Élő Népzenével és Táncműsorral',
            'best_for': '🎯 Ideális választás: A magyar néptánc, élő cigányzene és a hagyományos ízek kedvelői.',
            'price': '€89'
        },
        {
            'rank': '🍷 #9 Bor & Kézműves Sör',
            'kicker': 'Hungaria Koncert • ⏱️ 90 perc • Akadémia kikötő',
            'title': 'Budapesti Éjszakai Hajóút Koktélokkal, Kézműves Sörrel vagy Borral',
            'best_for': '🎯 Ideális választás: Élő népzenei hangulat és minőségi magyar bor- és sörkóstolás.',
            'price': '€21–65'
        },
        {
            'rank': '🏷️ #10 Legolcsóbb Nappali Hajó',
            'kicker': 'Duna Cruises • ⏱️ 60 perc • Vigadó tér kikötő',
            'title': 'Budapesti Városnéző Hajóút Üdvözlőitallal (Duna Cruises)',
            'best_for': '🎯 Ideális választás: A legalacsonyabb jegyárat kereső nappali városnézők.',
            'price': '€12–18'
        }
    ]
    
    deck = soup.find(class_='ltt-deck-container')
    deck_cards = deck.find_all(class_='bpa-card') if deck else []
    for idx, card in enumerate(deck_cards[:10]):
        cdata = cards_hu[idx]
        rank_tag = card.find(class_='bpa-rank-tag')
        if rank_tag: rank_tag.string = cdata['rank']
        
        kicker = card.find(class_='bpa-kicker')
        if kicker: kicker.string = cdata['kicker']
        
        title = card.find(class_='bpa-title')
        if title: title.string = cdata['title']
        
        best_for = card.find(class_='bpa-best-for')
        if best_for: best_for.string = cdata['best_for']
        
        price = card.find(class_='bpa-price')
        if price: price.string = f"{cdata['price']} / fő"
        
        psub = card.find(class_='bpa-psub')
        if psub: psub.string = "/ felnőtt"
        
        btn = card.find(class_='bpa-btn')
        if btn: btn.string = "Foglalás most →"
        
        sublink = card.find(class_='bpa-sublink') or card.find(class_='bpa-jump-link')
        if sublink: sublink.string = "Értékelés elolvasása ↓"
        
        if idx >= 6:
            card['data-cat'] = card.get('data-cat', '').replace('tested', '').strip()
            for p in card.find_all(class_='bpa-proof') + card.find_all(class_='bpa-proof-mobile') + card.find_all(class_='bpa-vchip'):
                p.decompose()
        else:
            vchip = card.find(class_='bpa-vchip')
            if vchip: vchip.string = "✓ Személyesen tesztelve"
        
        trust = card.find(class_='bpa-trust-micro')
        if trust:
            trust.clear()
            s1 = soup.new_tag('span')
            s1.string = "Azonnali mobiljegy"
            s2 = soup.new_tag('span')
            s2.string = "•"
            s3 = soup.new_tag('span')
            s3.string = "24 órás ingyenes lemondás"
            trust.extend([s1, s2, s3])
            
        for sp in card.find_all(class_='bpa-sp'):
            stxt = sp.get_text(strip=True)
            for eng_k, hu_v in HU_SPECS_MAP.items():
                if eng_k in stxt:
                    sp.string = hu_v
                    break
        
    # 5. Table of Contents
    toc = soup.find(class_='ltt-toc-card')
    if toc:
        toc_title = toc.find(class_='ltt-toc-title')
        if toc_title: toc_title.string = "Tartalomjegyzék"
        toc_links = toc.find_all('a')
        for idx, tlink in enumerate(toc_links[:10]):
            tlink.string = f"#{idx+1} {cards_hu[idx]['title']}"
            
    # 6. Breakdown Header
    breakdown_h2 = soup.find(class_='bpa-breakdown-title')
    if breakdown_h2:
        breakdown_h2.string = "Részletes Elemzés — A 10 Legjobb Dunai Sétahajó Budapesten"
        
    # 7. Details Cards Localization (Pros/Cons & Bento content)
    details_cards = soup.find_all('details', class_='bpa-details-card')
    for idx, dcard in enumerate(details_cards[:10]):
        cdata = cards_hu[idx]
        if idx == 1:
            insert_rubin_group_how_to_get_there(soup, dcard)
        
        # Summary bar
        d_title = dcard.find(class_='bpa-details-title')
        if d_title: d_title.string = cdata['title']
        d_kicker = dcard.find(class_='bpa-kicker')
        if d_kicker:
            map_link = d_kicker.find(class_='bpa-kicker-map-link')
            parts = cdata['kicker'].rsplit('•', 1)
            if len(parts) == 2 and map_link:
                d_kicker.clear()
                d_kicker.append(parts[0].strip() + ' • ')
                d_kicker.append(map_link)
            else:
                d_kicker.string = cdata['kicker']
        d_price = dcard.find(class_='bpa-details-price')
        if d_price: d_price.string = f"{cdata['price']} / fő"
        
        if idx >= 6:
            for p in dcard.find_all(class_='bpa-proof') + dcard.find_all(class_='bpa-vchip'):
                p.decompose()
        
        # RESTORE CANONICAL PROS & CONS STRUCTURE
        pros, cons = RIVER_PROS_CONS[idx]
        old_pc = dcard.find(class_='pro-con-box-wrapper')
        if old_pc:
            new_pc = create_pro_con_html(soup, pros, cons)
            old_pc.replace_with(new_pc)
            
        # Mini pills & bento head labels
        bento_groups = dcard.find_all('details', class_='ltt-bento-group')
        for bg in bento_groups:
            head = bg.find('summary')
            if not head: continue
            
            pill = head.find(class_='ltt-mini-pill')
            if pill:
                ptxt = pill.text.strip()
                if ptxt == 'Overview': pill.string = 'Áttekintés'
                elif ptxt == 'Location Map': pill.string = 'Kikötőtérkép'
                elif ptxt == 'Onboard Walkthrough': pill.string = 'Fedélzeti Séta'
                elif ptxt == 'Audio & Operator': pill.string = 'Audio & Hajótársaság'
                
            btitle = head.find(class_='ltt-bento-group-title')
            if btitle:
                btxt = btitle.text.strip()
                if 'Summary & Review' in btxt or 'Összegzés' in btxt:
                    btitle.string = "🏆 Összegzés és Értékelés"
                elif 'Before the Cruise' in btxt or 'Kikötő' in btxt:
                    btitle.string = "📍 Kikötő, Beszállás és Térkép"
                elif 'During the Cruise' in btxt or 'A Hajó és' in btxt:
                    btitle.string = "🛳️ A Hajó és Fedélzet"
                elif 'Audio Guide Tested' in btxt or 'Audio Guide és' in btxt:
                    btitle.string = "🎧 Audio Guide és Szolgáltatások"

        # Populate Bento 0 (Summary) with authentic Hungarian text
        if len(bento_groups) >= 1 and idx in RIVER_SUMMARIES:
            b0_body = bento_groups[0].find(class_='ltt-bento-group-body')
            if b0_body:
                # Find or create w-richtext container
                rich = b0_body.find(class_='w-richtext')
                if not rich:
                    rich = soup.new_tag('div', **{'class': 'w-richtext'})
                    b0_body.clear()
                    b0_body.append(rich)
                else:
                    rich.clear()
                
                # Append authentic Hungarian paragraphs
                for p_text in RIVER_SUMMARIES[idx]:
                    new_p = soup.new_tag('p')
                    new_p.string = p_text
                    rich.append(new_p)

        # Bento 0 title
        if len(bento_groups) >= 1:
            b0_h4 = bento_groups[0].find('h4')
            if b0_h4: b0_h4.string = cdata['title']

        # Apply comprehensive subpoints and Quick Facts translations
        apply_subpoints_translations(soup, dcard, idx, RIVER_SUBPOINTS)
        apply_qf_translations(soup, dcard)

        # Localize buttons and map links
        for m_link in dcard.find_all(class_='bpa-kicker-map-link'):
            mtxt = m_link.get_text(strip=True)
            if mtxt in QF_BADGES_HU:
                m_link.string = QF_BADGES_HU[mtxt]
        for bc in dcard.find_all(class_='ltt-buy-card'):
            localize_buy_card(soup, bc, cdata['title'])
        for sl in dcard.find_all(class_=['bpa-sublink', 'bpa-jump-link']):
            sl.string = "Értékelés elolvasása ↓"

        # Translate tips and blockquotes, remove English FAQ blockquotes
        for bq in dcard.find_all('blockquote'):
            btxt = bq.text.strip()
            if 'All cruises have a generous cancellation policy' in btxt:
                bq.clear()
                bq.append("💡 ")
                st = soup.new_tag('strong')
                st.string = "Tipp:"
                bq.append(st)
                bq.append(" Minden hajóútra érvényes az ingyenes lemondási lehetőség, amellyel az indulás előtt 24 órával teljes visszatérítés igényelhető.")
            elif 'For the best sightseeing and photo opportunities' in btxt:
                bq.clear()
                bq.append("💡 ")
                st = soup.new_tag('strong')
                st.string = "Tipp:"
                bq.append(st)
                bq.append(" A legjobb fotózáshoz válasszon tágas felső nyitott fedélzetű hajót, ahol nem zavarják oszlopok vagy ablakkeretek a kilátást.")
            elif 'All the other cruises offer loudspeaker audio guides' in btxt:
                bq.clear()
                bq.append("💡 ")
                st = soup.new_tag('strong')
                st.string = "Tipp:"
                bq.append(st)
                bq.append(" A többi sétahajó hangszórós audiokalauzt használ, ami az utasok beszélgetése miatt gyakran nehezen érthető.")
            elif 'The best open air seats go fast' in btxt:
                bq.clear()
                bq.append("💡 ")
                st = soup.new_tag('strong')
                st.string = "Tipp:"
                bq.append(st)
                bq.append(" A legjobb felső fedélzeti helyek gyorsan megtelnek! Érdemes 15-20 perccel indulás előtt a kikötőbe érkezni.")
            elif '❓' in btxt and ('Is buying food' in btxt or 'Should I book' in btxt or 'Is it possible to reserve' in btxt):
                bq.decompose()

    # 8. Localized Mobile Drawer
    drawer = soup.find(class_='bpa-mobile-drawer')
    if drawer:
        d_name = drawer.find(class_='bpa-drawer-name')
        if d_name: d_name.string = "Legenda Városnéző Sétahajó"
        d_price = drawer.find(class_='bpa-drawer-price')
        if d_price: d_price.string = "€20-tól"
        d_btn = drawer.find(class_='bpa-drawer-btn')
        if d_btn: d_btn.string = "Foglalás most →"
        
    # 8b. Localized Floating Bar
    localize_floating_bar(soup, 'river', 10, HU_RIVER_SHORT_TITLES, 'Top 10 Sétahajó Összehasonlítás', 'Részletes Elemzés (10 Sétahajó)')

    # Global sweeps for any stray elements
    for bc in soup.find_all(class_='ltt-buy-card'):
        localize_buy_card(soup, bc)
    for sl in soup.find_all(class_=['bpa-sublink', 'bpa-jump-link']):
        sl.string = "Értékelés elolvasása ↓"
    localize_proof_chips(soup)
        
    # 9. Localized Footer
    localize_footer(soup)
        
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Hungarian River Guide saved to {out_path}")


# HARVESTED SUMMARY REVIEWS FOR DINNER CARDS

# DATA FOR 7 DINNER CRUISES
DINNER_PROS_CONS = [
    # Card 1 (Legenda Dinner)
    ([
        ("Prémium és Elegáns Atmoszféra", "Exkluzív, James Bond hangulatú vacsora gyertyafénnyel és panorámaablakokkal."),
        ("4 Fogásos Gourmet Vacsora", "Frissen tálalt ínyenc fogások felnőtteknek, 3 fogásos gyermekmenüvel."),
        ("Üdvözlőital a Jegyárban", "Egy pohár pezsgő, minőségi bor, sör, üdítő vagy ásványvíz beszálláskor."),
        ("Kiváló Pároknak és Évfordulókra", "Különálló 2 fős gyertyafényes asztalok közvetlenül a padlótól a mennyezetig érő ablakok mellett."),
        ("Kellemes Élő Zenei Műsor", "Zongorista és énekes duó igényes élő lounge előadása vacsora közben."),
        ("Bőséges 2,5 Órás Időtartam", "Kényelmes tempójú étkezés és teljes budapesti éjszakai dunai panoráma.")
    ], [
        ("Magasabb Árkategória", "A legdrágább vacsorahajó Budapesten, de a prémium minőség és élmény minden eurót megér."),
        ("További Italok Külön Fizetendők", "Az üdvözlőitalon felüli italok a fedélzeti bárból rendelhetők éttermi árakon.")
    ]),
    # Card 2 (Silverline No Show)
    ([
        ("Pénztárcabarát Elegancia", "A legkedvezőbb árú minőségi, 4 fogásos vacsorahajó Budapesten, kimagasló ár-érték aránnyal."),
        ("Gourmet Menüválaszték", "Kifinomult négyfogásos vacsora és egy pohár üdvözlő Prosecco."),
        ("Figyelmes Személyzet", "Gyors és előzékeny felszolgálás a vacsora teljes ideje alatt."),
        ("Meghitt, Nyugodt Hangulat", "A műsor hiánya miatt csendes, beszélgetésre és meghitt romantikára alkalmas légkör."),
        ("Teljes Budapesti Útvonal", "2 órás esti hajóút a Margit híd és a Müpa között."),
        ("Helyben Készített Friss Ételek", "Az ételeket a hajó saját konyhájában főzik.")
    ], [
        ("Nincs Élő Műsor", "Az alacsonyabb árért cserébe a szórakoztatást kellemes háttérzene adja élő előadás helyett."),
        ("Bizonyos Fogások Felárasak", "Egyes prémium főételek kiegészítő felárat igényelnek a helyszínen."),
        ("Kisebb Finomítási Lehetőségek", "Egyes köretek és desszertek minősége kissé elmarad a csúcsgasztronómiától.")
    ]),
    # Card 3 (Silverline Folk Operetta)
    ([
        ("4 Fogásos Gourmet Vacsora", "Hagyományos magyaros és nemzetközi fogások ízléses tálalásban."),
        ("Helyszíni Hajókonyha", "Frissen elkészített meleg ételek az asztalhoz felszolgálva."),
        ("Színvonalas Élő Folklór Műsor", "Autentikus néptáncosok és operetténekesek lendületes, díjnyertes színpadi előadása."),
        ("Kényelmes 2 Órás Menetidő", "Tökéletes egyensúly az étkezés, a kulturális show és a kivilágított Parlament csodálata között.")
    ], [
        ("Feszesebb Ülésrend", "A műsor miatt a táncparkett körül sűrűbben helyezkednek el az asztalok."),
        ("Hangosabb Műsoridőszak", "A dinamikus operettelőadás alatt a csendes beszélgetés kevésbé lehetséges.")
    ]),
    # Card 4 (Silverline Piano Battle)
    ([
        ("Gourmet 4 Fogásos Vacsora", "Ínyenc fogások választható húsos, halas és vegetáriánus menüvel."),
        ("Friss Ételek a Hajókonyhából", "Közvetlenül tálalás előtt helyben főzött ételek."),
        ("Látványos Élő Zongorapárbaj", "Két zongoraművész és énekes szórakoztató, humoros és lendületes zenei versengése."),
        ("2 Órás Esti Panoráma", "Gyönyörű rálátás az éjszakai kivilágított Budai Várra és Parlamentre.")
    ], [
        ("Interaktív, Lendületes Hangerő", "A show interaktív és hangosabb, kevésbé alkalmas csendes, suttogó romantikára."),
        ("Prémium Fogások Felára", "Egyes prémium ételek felárasak az étlapon.")
    ]),
    # Card 5 (Hungaria Koncert Buffet)
    ([
        ("Korlátlan Svédasztalos Büfé", "Bőséges választék klasszikus magyar ételekből (gulyás, pörkölt, rétes)."),
        ("Két Ajándék Üdvözlőital", "Alkoholos és alkoholmentes italok közül választható kezdés."),
        ("Autentikus Nosztalgikus Hangulat", "Századfordulós kabaré- és báltermi atmoszféra a Dunán."),
        ("Élő Néptánc és Cigányzene", "Díjnyertes népművészek élő fellépése népviseletben."),
        ("Teljes Dunai Útvonal", "A Margitszigettől a Nemzeti Színházig hajózik.")
    ], [
        ("Kevésbé Panorámafókuszú", "A szalon belső fókuszú, és a vacsorára valamint a műsorra összpontosít, kevesebb kilátóhellyel."),
        ("Büfé Jellegű Ételminőség", "Bőséges és ízletes, de tömegétkeztetés jellegű, nem egyedi tányérszerviz.")
    ]),
    # Card 6 (Eurama Folk Show)
    ([
        ("4 Fogásos Tradicionális Lakoma", "Klasszikus magyar ízek, vegetáriánus és speciális étrendű opciókkal."),
        ("Autentikus Cigányzenekar", "Hagyományos hegedű- és nagybőgőkíséret az asztalok között."),
        ("Ideális 1,5–2 Órás Időtartam", "Kompakt, feszes esti program a városnézés mellé."),
        ("360°-os Felső Kilátóterasz", "Kiváló fotózási pont az éjszakai városképhez."),
        ("Központi Vigadó Téri Kikötő", "Közvetlenül a pesti belváros szívéből indul.")
    ], [
        ("Lépcsős Beszállás", "A hajó kialakítása miatt mozgáskorlátozott vendégek számára nehezebb a megközelítés.")
    ]),
    # Card 7 (Silverline Unlimited Drinks)
    ([
        ("Korlátlan Italfogyasztási Csomag", "Korlátlan minőségi magyar borok, pezsgő, csapolt sör, üdítők és kávé a teljes 2,5 órás hajóúton."),
        ("Modern Panoráma Rendezvényhajó", "Hatalmas üvegablakok és tágas felső nyitott kilátóterasz a Parlament fotózásához."),
        ("4 Fogásos Felszolgált Gourmet Menü", "Friss kacsamell, marhapofa, lazac vagy vegetáriánus fogások a fedélzeti konyhából."),
        ("Elegáns Élő Akusztikus Zene", "Akusztikus gitár és ének duó kellemes, beszélgetést nem zavaró esti háttérzenével.")
    ], [
        ("Nincs Hagyományos Folklór Show", "Modern élőzenére fókuszál néptánc helyett."),
        ("Tömények Külön Fizetendők", "A korlátlan csomag a borokra, pezsgőre, sörre és üdítőkre érvényes; a röviditalok külön fizetendők.")
    ])
]

DINNER_SUMMARIES = {
    0: [ # Legenda Candlelit Dinner
        "Ha a legromantikusabb, legigényesebb vacsorás hajóutat keresi Budapesten, a Legenda City Cruises gyertyafényes estje a tökéletes választás. A hajótársaság kiemelkedő gasztronómiai élményt nyújt elegáns zongora- és énekkísérettel.",
        "A 4 fogásos gourmet vacsorát frissen tálalják fel az asztalokhoz. A hatalmas üvegpanorámás ablakok mellett elhelyezett, privát gyertyafényes asztalok páratlan rálátást biztosítanak a díszkivilágításban ragyogó Országházra és a Budai Várra.",
        "A bőséges 2,5 órás menetidő garantálja, hogy a vacsora ne legyen siettetve, és a vendégek meghitt hangulatban élvezhessék a főváros legszebb éjszakai látképét."
    ],
    1: [ # Silverline No Show Dinner
        "A növekvő utazási költségek idején a Silverline egy kifejezetten pénztárcabarát, mégis elegáns 4 fogásos vacsorahajózást hozott létre.",
        "Ezt úgy érték el, hogy a költséges színpadi műsor helyett kellemes háttérzenét biztosítanak, így a vendégek zavartalanul beszélgethetnek és élvezhetik a Dunára nyíló kilátást lényegesen alacsonyabb áron.",
        "A 2 órás hajóút a Margit híd és az Atlétikai Stadion között halad végig, így az összes ikonikus látnivaló megcsodálható."
    ],
    2: [ # Silverline Folk Operetta
        "Autentikus folklór vacsoraélményre vágyik a Dunán? A Silverline operett- és néptáncműsoros hajóútja kiváló kulturális szórakozást és ínyenc vacsorát kínál.",
        "A díjnyertes magyar néptáncosok és operetténekesek dinamikus, látványos előadása különleges hangulatot teremt a modern panorámaszalonban.",
        "A 4 fogásos gourmet menüben magyaros és nemzetközi ízek keverednek, amelyeket a hajókonyhán frissen készítenek el."
    ],
    3: [ # Silverline Piano Battle
        "Élvezze a lendületes élő zongorapárbajt vacsora közben a Duna hullámain! A Silverline zongorás vacsorahajója két virtuóz zongorista és egy elbűvölő énekesnő interaktív előadásával teszi emlékezetessé az estét.",
        "A humoros zenei csaták, a romantikus dallamok és az ismert világslágerek garantálják a jókedvet a 4 fogásos vacsora alatt.",
        "Pároknak és baráti társaságoknak egyaránt kiváló választás egy szórakoztató budapesti estéhez."
    ],
    4: [ # Hungaria Koncert Buffet
        "A Hungaria Koncert szervezi Budapest legnépszerűbb és legnagyobb forgalmú svédasztalos vacsorahajóját, amely élő népzenei és néptáncbemutatóval várja a vendégeket.",
        "A gazdag büféasztalról korlátlanul kóstolhatók meg a klasszikus magyar fogások a gulyástól a marhapörköltön át a házi rétesig.",
        "A szalonban elismert prímás vezette zenekar és hagyományos népviseletbe öltözött táncosok teremtenek békebeli magyaros mulatóhangulatot."
    ],
    5: [ # Eurama Gypsy Music
        "Tapasztalja meg a hagyományos cigányzene varázsát egy 4 fogásos elegáns vacsora kíséretében az Eurama rendezvényhajóján.",
        "A prímás és a vonószenekar közvetlenül az asztalok között játszik meghitt, autentikus dallamokat, miközben a hajó a pesti Vigadó térről indulva végighalad a kivilágított dunai szakaszon.",
        "A 360 fokos felső kilátófedélzetről vacsora után lélegzetelállító panoráma nyílik a Lánchídra és a Parlamentre."
    ],
    6: [ # Silverline Unlimited Drinks
        "Ha egy elegáns, 4 fogásos felszolgált vacsorára vágyik a Dunán anélkül, hogy az italok árával kellene számolnia, a Silverline korlátlan italos vacsorahajója az egyik legvonzóbb választás Budapesten.",
        "A legtöbb budapesti vacsorás hajóút csupán egyetlen üdvözlőitalt tartalmaz a jegyárban, így az étkezés végén jelentős italszámla keletkezhet. Ez a hajóút a teljes 2,5 órás út során korlátlan minőségi magyar borokat, pezsgőt, sört, üdítőt és kávét kínál.",
        "A River Diva modern rendezvényhajó hatalmas üvegpanorámás szalonja és tágas nyitott felső kilátóterasza akadálytalan kilátást nyújt a kivilágított Parlamentre és a dunai hidakra.",
        "Az esti hangulatot akusztikus gitár és ének duó teszi teljessé, amely kellemes, elegáns atmoszférát biztosít a társasági beszélgetés zavarása nélkül."
    ]
}


def build_hungarian_dinner():
    print("Compiling Hungarian Dinner Guide (hu/setahajozas-a-dunan-vacsoraval/index.html)...")
    en_path = os.path.join(BASE_DIR, 'dinner.html')
    out_path = os.path.join(BASE_DIR, 'hu', 'setahajozas-a-dunan-vacsoraval', 'index.html')
    
    soup = BeautifulSoup(open(en_path, 'r', encoding='utf-8').read(), 'html.parser')
    
    # 1. Head Metadata
    if soup.title:
        soup.title.string = "7 Legjobb Városnéző Vacsorahajó Budapesten 2026-ban (Személyesen Tesztelve)"
    m_desc = soup.find('meta', {'name': 'description'})
    if m_desc:
        m_desc['content'] = "A legfrissebb 2026-os értékelés a budapesti vacsorás hajóutakról. 4 fogásos gyertyafényes vacsorák, svédasztalos büfék és élő zenei műsorok összehasonlítása."
    og_title = soup.find('meta', {'property': 'og:title'})
    if og_title and soup.title: og_title['content'] = soup.title.string
    tw_title = soup.find('meta', {'name': 'twitter:title'})
    if tw_title and soup.title: tw_title['content'] = soup.title.string
    og_desc = soup.find('meta', {'property': 'og:description'})
    if og_desc and m_desc: og_desc['content'] = m_desc['content']
    tw_desc = soup.find('meta', {'name': 'twitter:description'})
    if tw_desc and m_desc: tw_desc['content'] = m_desc['content']
    can = soup.find('link', {'rel': 'canonical'})
    if can:
        can['href'] = "https://www.budapestadventures.com/hu/setahajozas-a-dunan-vacsoraval"
    html_tag = soup.find('html')
    if html_tag:
        html_tag['lang'] = 'hu'

    # Schema JSON-LD localization
    for s in soup.find_all('script', type='application/ld+json'):
        if s.string:
            s_txt = s.string
            s_txt = s_txt.replace('"inLanguage": "en"', '"inLanguage": "hu"')
            s_txt = s_txt.replace("7 Best Dinner Cruises in Budapest in 2026 (Personally Tested)", "7 Legjobb Városnéző Vacsorahajó Budapesten 2026-ban (Személyesen Tesztelve)")
            s_txt = s_txt.replace("7 Best Budapest Dinner Cruises on the Danube", "7 Legjobb Dunai Vacsorahajó Budapesten")
            s_txt = s_txt.replace("Detailed Breakdown — 7 Best Dinner Cruises in Budapest", "Részletes Értékelés — 7 Legjobb Budapesti Vacsorahajó")
            s_txt = s_txt.replace("Experience Budapest's top-rated river cruises in 2026.", "Fedezze fel Budapest legkiválóbb dunai vacsorahajóit 2026-ban.")
            s.string.replace_with(s_txt)

    localize_css_reviews(soup)
    localize_breakdown_section(soup, 'dinner')
        
    # 2. Navbar & Mega-Menu
    localize_navbar_and_menu(soup)

    # 3. Clean Card Hero
    for bc in soup.find_all(class_='ltt-breadcrumbs'):
        bc.clear()
        home_a = soup.new_tag('a', href='/hu/')
        home_a.string = 'Főoldal'
        sep = soup.new_tag('span', **{'class': 'ltt-bc-sep'})
        sep.string = '›'
        curr = soup.new_tag('span', **{'class': 'ltt-bc-current'})
        curr.string = 'Dunai Vacsorahajózás Budapesten'
        bc.append(home_a)
        bc.append(' ')
        bc.append(sep)
        bc.append(' ')
        bc.append(curr)
            
    badge = soup.find(class_='ltt-hero-kicker-badge')
    if badge:
        badge.string = "✓ 2026-OS HELYSZÍNEN TESZTELT GASZTRO & PANORÁMA AUDIT"
        
    h1 = soup.find(class_='ltt-editorial-h1')
    if h1:
        h1.string = "7 Legjobb Városnéző Vacsorahajó Budapesten 2026-ban (Személyesen Tesztelve)"
        
    author_line = soup.find(class_='ltt-author-line')
    if author_line:
        author_line.clear()
        author_line.append("Szerző: ")
        a_tag = soup.new_tag('a', href="/about")
        a_tag.string = "Adam Dimitrov"
        author_line.append(a_tag)
        author_line.append(" — Alapító & Vezető Kutató")
        
    author_role = soup.find(class_='ltt-author-role')
    if author_role:
        author_role.string = "Független helyszíni felmérések • Saját fotók és videók • Elfogulatlan értékelések"
        
    tp = soup.find(class_='ltt-trust-pill')
    if tp:
        tp.clear()
        st = soup.new_tag('strong')
        st.string = 'Frissítve'
        tp.append(st)
        tp.append(': 2026. november')
    updated = soup.find(class_='ltt-updated-date')
    if updated:
        updated.string = "Utoljára frissítve: 2026. november"
        
    lead = soup.find(class_='ltt-lead-copy')
    if lead:
        lead.clear()
        p1 = soup.new_tag('p')
        p1.string = "Romantikus vacsorára vágyik a Dunán, vagy egy látványos élőzenés folklórestet keres? A budapesti vacsorahajók között óriási a különbség: a Legenda prémium, frissen tálalt 4 fogásos gyertyafényes vacsorájától a nagy befogadóképességű svédasztalos büféhajókig."
        p2 = soup.new_tag('p')
        p2.string = "Minden hajót névtelen utasként teszteltünk: értékeltük az ételek minőségét, az asztalok elhelyezkedését az ablakok mellett, a zenei műsor hangerejét és a kivilágított Parlament esti panorámáját."
        lead.append(p1)
        lead.append(p2)
        
    filter_label = soup.find(class_='ltt-filter-label')
    if filter_label:
        filter_label.string = "Szűrés:"
        
    tab_btns = soup.find_all(class_='ltt-tab-btn')
    hu_tab_map = {
        'all': 'Összes (7)',
        'tested': '✓ Személyesen tesztelve (5)',
        'alacarte': '🍽️ Felszolgált menü (6)',
        'buffet': '🍱 Svédasztalos büfé (1)',
        'show': '🎵 Élőzene & Műsor (6)',
        'drinks': '🍷 Korlátlan ital (1)',
        'under80': '💶 80 € alatt (2)'
    }
    for btn in tab_btns:
        cat = btn.get('data-cat')
        if cat in hu_tab_map:
            btn.string = hu_tab_map[cat]
        
    # 4. 7 Dinner Deck Cards Localization
    cards_hu = [
        {
            'rank': '🏆 #1 Legjobb Romantikus Vacsora',
            'kicker': 'Legenda City Cruises • ⏱️ 150 perc • 7-es kikötő (Vigadó tér)',
            'title': '4 Fogásos Romantikus Gyertyafényes Hajós Vacsora Élő Lounge Zenével',
            'best_for': '🎯 Ideális választás: Párok, évfordulók és romantikus alkalmak, ahol a prémium gasztronómia és a nyugodt hangulat a cél.',
            'price': '€110'
        },
        {
            'rank': '🍽️ #2 Vacsora Show Nélkül',
            'kicker': 'Silverline Cruises • ⏱️ 135 perc • 11-es kikötő (Petőfi tér)',
            'title': '4 Fogásos Vacsorahajó Üdvözlőitallal, Show Nélkül',
            'best_for': '🎯 Ideális választás: Pénztárcabarát vacsorázók, akik csak a dunai panorámára és a finom ételekre vágynak műsor nélkül.',
            'price': '€74'
        },
        {
            'rank': '🎭 #3 Folklór Operett Show',
            'kicker': 'Silverline Cruises • ⏱️ 135 perc • 11-es kikötő (Petőfi tér)',
            'title': '4 Fogásos Gourmet Vacsorahajó Folklór Operett Show-val',
            'best_for': '🎯 Ideális választás: A hagyományos magyar kultúra, operett és a dinamikus színpadi előadások kedvelői.',
            'price': '€91'
        },
        {
            'rank': '🎹 #4 Zongorapárbaj Show',
            'kicker': 'Silverline Cruises • ⏱️ 135 perc • 11-es kikötő (Petőfi tér)',
            'title': '4 Fogásos Gourmet Vacsorahajó Zongorapárbaj Show-val és Énekessel',
            'best_for': '🎯 Ideális választás: Vidám párok és baráti társaságok, akik interaktív zenei élményre vágynak vacsora közben.',
            'price': '€91'
        },
        {
            'rank': '🥗 #5 Svédasztalos Büfé',
            'kicker': 'Hungaria Koncert • ⏱️ 120 perc • Akadémia kikötő',
            'title': 'Svédasztalos Hajós Vacsora Magyaros Néptáncműsorral',
            'best_for': '🎯 Ideális választás: Nagy étvágyú utazók és családok, akik korlátlan svédasztalt és autentikus néptáncot keresnek.',
            'price': '€79'
        },
        {
            'rank': '🎻 #6 Folklór & Cigányzene',
            'kicker': 'Eurama • ⏱️ 120 perc • Vigadó tér kikötő',
            'title': '4 Fogásos Vacsorahajó Folklór Show-val',
            'best_for': '🎯 Ideális választás: Turisták, akik kompakt 2 órás vacsorát és klasszikus cigányzenét szeretnének.',
            'price': '€90'
        },
        {
            'rank': '🥂 #7 Korlátlan Ital & Élőzene',
            'kicker': 'Silverline Cruises • ⏱️ 135 perc • 11-es kikötő (Petőfi tér)',
            'title': '4 Fogásos Vacsorahajó Élőzenével és Korlátlan Italfogyasztással',
            'best_for': '🎯 Ideális választás: Társaságok és ünneplők, akik nem szeretnének az italok árával számolni a vacsora során.',
            'price': '€99'
        }
    ]
    
    deck = soup.find(class_='ltt-deck-container')
    deck_cards = deck.find_all(class_='bpa-card') if deck else []
    for idx, card in enumerate(deck_cards[:7]):
        cdata = cards_hu[idx]
        rank_tag = card.find(class_='bpa-rank-tag')
        if rank_tag: rank_tag.string = cdata['rank']
        
        kicker = card.find(class_='bpa-kicker')
        if kicker: kicker.string = cdata['kicker']
        
        title = card.find(class_='bpa-title')
        if title: title.string = cdata['title']
        
        best_for = card.find(class_='bpa-best-for')
        if best_for: best_for.string = cdata['best_for']
        
        price = card.find(class_='bpa-price')
        if price: price.string = f"{cdata['price']} / fő"
        
        psub = card.find(class_='bpa-psub')
        if psub: psub.string = "/ felnőtt"
        
        btn = card.find(class_='bpa-btn')
        if btn: btn.string = "Foglalás most →"
        
        sublink = card.find(class_='bpa-sublink') or card.find(class_='bpa-jump-link')
        if sublink: sublink.string = "Értékelés elolvasása ↓"
        
        if idx in [5, 6]:
            card['data-cat'] = card.get('data-cat', '').replace('tested', '').strip()
            for p in card.find_all(class_='bpa-proof') + card.find_all(class_='bpa-proof-mobile') + card.find_all(class_='bpa-vchip'):
                p.decompose()
        else:
            vchip = card.find(class_='bpa-vchip')
            if vchip: vchip.string = "✓ Személyesen tesztelve"
        
        trust = card.find(class_='bpa-trust-micro')
        if trust:
            trust.clear()
            s1 = soup.new_tag('span')
            s1.string = "Azonnali mobiljegy"
            s2 = soup.new_tag('span')
            s2.string = "•"
            s3 = soup.new_tag('span')
            s3.string = "24 órás ingyenes lemondás"
            trust.extend([s1, s2, s3])
            
        for sp in card.find_all(class_='bpa-sp'):
            stxt = sp.get_text(strip=True)
            for eng_k, hu_v in HU_SPECS_MAP.items():
                if eng_k in stxt:
                    sp.string = hu_v
                    break
        
    # 5. Table of Contents
    toc = soup.find(class_='ltt-toc-card')
    if toc:
        toc_title = toc.find(class_='ltt-toc-title')
        if toc_title: toc_title.string = "Tartalomjegyzék"
        toc_links = toc.find_all('a')
        for idx, tlink in enumerate(toc_links[:7]):
            tlink.string = f"#{idx+1} {cards_hu[idx]['title']}"
            
    # 6. Breakdown Header
    breakdown_h2 = soup.find(class_='bpa-breakdown-title')
    if breakdown_h2:
        breakdown_h2.string = "Részletes Elemzés — A 7 Legjobb Dunai Vacsorahajó Budapesten"
        
    # 7. Details Cards Localization (Pros/Cons & Bento content)
    details_cards = soup.find_all('details', class_='bpa-details-card')
    for idx, dcard in enumerate(details_cards[:7]):
        cdata = cards_hu[idx]
        d_title = dcard.find(class_='bpa-details-title')
        if d_title: d_title.string = cdata['title']
        d_kicker = dcard.find(class_='bpa-kicker')
        if d_kicker:
            map_link = d_kicker.find(class_='bpa-kicker-map-link')
            parts = cdata['kicker'].rsplit('•', 1)
            if len(parts) == 2 and map_link:
                d_kicker.clear()
                d_kicker.append(parts[0].strip() + ' • ')
                d_kicker.append(map_link)
            else:
                d_kicker.string = cdata['kicker']
        d_price = dcard.find(class_='bpa-details-price')
        if d_price: d_price.string = f"{cdata['price']} / fő"
        
        if idx in [5, 6]:
            dcard['data-cat'] = dcard.get('data-cat', '').replace('tested', '').strip()
            for p in dcard.find_all(class_='bpa-proof') + dcard.find_all(class_='bpa-proof-mobile') + dcard.find_all(class_='bpa-vchip'):
                p.decompose()
        
        # RESTORE CANONICAL PROS & CONS STRUCTURE
        pros, cons = DINNER_PROS_CONS[idx]
        old_pc = dcard.find(class_='pro-con-box-wrapper')
        if old_pc:
            new_pc = create_pro_con_html(soup, pros, cons)
            old_pc.replace_with(new_pc)
            
        # Mini pills & bento head labels
        bento_groups = dcard.find_all('details', class_='ltt-bento-group')
        for bg in bento_groups:
            head = bg.find('summary')
            if not head: continue
            
            pill = head.find(class_='ltt-mini-pill')
            if pill:
                ptxt = pill.text.strip()
                if ptxt == 'Overview': pill.string = 'Áttekintés'
                elif ptxt == 'Location Map': pill.string = 'Kikötőtérkép'
                elif ptxt == 'Onboard Walkthrough': pill.string = 'Fedélzeti Séta'
                elif ptxt == 'Audio & Operator': pill.string = 'Gasztronómia & Részletek'
                
            btitle = head.find(class_='ltt-bento-group-title')
            if btitle:
                btxt = btitle.text.strip()
                if 'Summary & Review' in btxt or 'Összegzés' in btxt:
                    btitle.string = "🏆 Összegzés és Értékelés"
                elif 'Before the Cruise' in btxt or 'Kikötő' in btxt:
                    btitle.string = "📍 Kikötő, Beszállás és Térkép"
                elif 'During the Cruise' in btxt or 'A Hajó és' in btxt:
                    btitle.string = "🛳️ A Hajó és Fedélzet"
                elif 'Audio Guide Tested' in btxt or 'Gasztronómia' in btxt:
                    btitle.string = "🍽️ Menü és Szolgáltatások"

        # Populate Bento 0 (Summary) with authentic Hungarian text
        if len(bento_groups) >= 1 and idx in DINNER_SUMMARIES:
            b0_body = bento_groups[0].find(class_='ltt-bento-group-body')
            if b0_body:
                rich = b0_body.find(class_='w-richtext')
                if not rich:
                    rich = soup.new_tag('div', **{'class': 'w-richtext'})
                    b0_body.clear()
                    b0_body.append(rich)
                else:
                    rich.clear()
                
                for p_text in DINNER_SUMMARIES[idx]:
                    new_p = soup.new_tag('p')
                    new_p.string = p_text
                    rich.append(new_p)

        # Bento 0 title
        if len(bento_groups) >= 1:
            b0_h4 = bento_groups[0].find('h4')
            if b0_h4: b0_h4.string = cdata['title']

        # Apply comprehensive subpoints and Quick Facts translations
        apply_subpoints_translations(soup, dcard, idx, DINNER_SUBPOINTS)
        apply_qf_translations(soup, dcard)

        # Localize buttons and map links
        for m_link in dcard.find_all(class_='bpa-kicker-map-link'):
            mtxt = m_link.get_text(strip=True)
            if mtxt in QF_BADGES_HU:
                m_link.string = QF_BADGES_HU[mtxt]
        for bc in dcard.find_all(class_='ltt-buy-card'):
            localize_buy_card(soup, bc, cdata['title'])
        for sl in dcard.find_all(class_=['bpa-sublink', 'bpa-jump-link']):
            sl.string = "Értékelés elolvasása ↓"

        # Translate tips and blockquotes, remove English FAQ blockquotes
        for bq in dcard.find_all('blockquote'):
            btxt = bq.text.strip()
            if 'All cruises have a generous cancellation policy' in btxt:
                bq.clear()
                bq.append("💡 ")
                st = soup.new_tag('strong')
                st.string = "Tipp:"
                bq.append(st)
                bq.append(" Minden hajóútra érvényes az ingyenes lemondási lehetőség, amellyel az indulás előtt 24 órával teljes visszatérítés igényelhető.")
            elif '❓' in btxt and ('Is buying food' in btxt or 'Should I book' in btxt or 'Is it possible to reserve' in btxt):
                bq.decompose()

    # 8. Localized Mobile Drawer
    drawer = soup.find(class_='bpa-mobile-drawer')
    if drawer:
        d_name = drawer.find(class_='bpa-drawer-name')
        if d_name: d_name.string = "Legenda 4 Fogásos Gyertyafényes Vacsora"
        d_price = drawer.find(class_='bpa-drawer-price')
        if d_price: d_price.string = "€110"
        d_btn = drawer.find(class_='bpa-drawer-btn')
        if d_btn: d_btn.string = "Foglalás most →"
        
    # 8b. Localized Floating Bar
    localize_floating_bar(soup, 'dinner', 7, HU_DINNER_SHORT_TITLES, 'Top 7 Vacsorahajó Összehasonlítás', 'Részletes Elemzés (7 Vacsorahajó)')

    # Global sweeps for buy cards, sublinks, decision guide, proof chips
    for bc in soup.find_all(class_='ltt-buy-card'):
        localize_buy_card(soup, bc)
    for sl in soup.find_all(class_=['bpa-sublink', 'bpa-jump-link']):
        sl.string = "Értékelés elolvasása ↓"
    localize_dinner_decision_guide(soup)
    localize_proof_chips(soup)
        
    # 9. Localized Footer
    localize_footer(soup)
        
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Hungarian Dinner Guide saved to {out_path}")


if __name__ == '__main__':
    build_hungarian_home()
    build_hungarian_river()
    build_hungarian_dinner()
    try:
        from scripts.inject_language_switcher import inject_language_switcher_into_file
        inject_language_switcher_into_file(os.path.join(BASE_DIR, 'hu', 'index.html'))
        inject_language_switcher_into_file(os.path.join(BASE_DIR, 'hu', 'setahajozas-a-dunan-budapest', 'index.html'))
        inject_language_switcher_into_file(os.path.join(BASE_DIR, 'hu', 'setahajozas-a-dunan-vacsoraval', 'index.html'))
        print("✓ Injected canonical language switcher into Hungarian pages")
    except Exception as e:
        print(f"Warning: could not inject switcher: {e}")

