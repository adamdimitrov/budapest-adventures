#!/usr/bin/env python3
"""
MASTER MULTILINGUAL PRIVATE BOATS COMPILER — BUDAPEST ADVENTURES
Compiles the perfected Luxury Editorial System layout (from best-private-boat-tours-budapest.html)
across all 21 localized private boat tours pages:
/{lang}/best-private-boat-tours-budapest/index.html

Strictly enforces:
1. 100% Design Parity with English Master (Luxury Editorial System):
   - Hero card (.ltt-clean-card)
   - 5 Comparison cards (.bpa-card) with authentic multi-photo sliders
   - Dunarama under Chain Bridge + top view + sunset on Card 2
   - Dedicated luxury yacht on Card 5
   - 5 Option C Bento Breakdown cards (details.bpa-details-card)
   - Desktop TOC & Mobile Bottom Sheet (#hybridSheet)
   - Floating Buy Bar (#sticky-bar)
   - Canonical 22-language switcher
2. 100% Native Content:
   - Native titles, pros, cons, and detailed summary paragraphs from harvested data
   - Localized UI microcopy from i18n_master_dictionary.json
3. Tracking Integrity:
   - Preserves partner=38585 on Legenda and full partner affiliate tags
"""

import os
import re
import sys
import json
from bs4 import BeautifulSoup

BASE_DIR = '/Users/adamdimitrov/Development/budapest-adventures'
CACHE_DIR = os.path.join(BASE_DIR, 'data', 'harvested_html')
DICT_PATH = os.path.join(BASE_DIR, 'data', 'i18n_master_dictionary.json')
MASTER_EN_PATH = os.path.join(BASE_DIR, 'best-private-boat-tours-budapest.html')

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
    'nl': {'home': '', 'river': 'beste-boedapest-riviercruises', 'dinner': 'beste-diner-cruises-boedapest'}
}

# Load dictionary
with open(DICT_PATH, 'r', encoding='utf-8') as f:
    I18N = json.load(f)

# Native tour title overrides for select languages
NATIVE_TOUR_TITLES = {
    'hu': [
        'A legjobb luxus privát hajóút',
        'Szintén nagyszerű luxus privát / vízi limuzin',
        'Sallangmentes / Legjobb ár-érték arányú privát hajóút',
        'Legjobb legénybúcsús hajó / Korlátlan italfogyasztás',
        'A Duna legluxusabb jachtja korlátlan pezsgővel'
    ],
    'de': [
        'Beste private Luxus-Yacht-Tour',
        'Ebenfalls großartig: Luxus-Wasserlimousine',
        'Kein Schnickschnack / Bester Preis-Leistungs-Bootstrip',
        'Bestes Partyboot für JGA / Unbegrenzte Getränke',
        'Luxuriöseste Yacht auf der Donau mit Champagner'
    ],
    'fr': [
        'Meilleure croisière privée en yacht de luxe',
        'Alternative d\'exception : Limousine des mers privée',
        'Sans fioritures / Meilleur rapport qualité-prix',
        'Meilleur bateau pour EVG/EVJF / Boissons à volonté',
        'Le yacht le plus luxueux du Danube avec champagne à volonté'
    ],
    'it': [
        'Miglior tour privato in yacht di lusso',
        'Altrettanto eccellente: Limousine d\'acqua privata',
        'Senza fronzoli / Miglior rapporto qualità-prezzo',
        'Miglior barca per addio al celibato / Drink illimitati',
        'Lo yacht più lussuoso sul Danubio con champagne illimitato'
    ],
    'es': [
        'El mejor paseo privado en yate de lujo',
        'Excelente opción: Limusina acuática privada',
        'Sin florituras / Mejor relación calidad-precio',
        'Mejor barco para despedidas de soltero / Bebidas ilimitadas',
        'El yate más lujoso del Danubio con champán ilimitado'
    ]
}

def extract_private_tours(lang):
    """Extract all 5 tours with titles, pros, cons, and summaries from harvested HTML."""
    path = os.path.join(CACHE_DIR, lang, 'private_boats.html')
    if not os.path.exists(path):
        return []
    soup = BeautifulSoup(open(path, encoding='utf-8'), 'html.parser')
    
    tours = []
    for i in range(1, 6):
        h2 = soup.find(lambda el: el.name == 'h2' and el.get_text(strip=True).startswith(f'{i}.'))
        if not h2:
            continue
        full_title = h2.get_text(strip=True)
        clean_title = re.sub(r'^\d+\.\s*', '', full_title).strip()
        
        container = h2.find_parent('div', class_='w-container') or h2.parent.parent
        pros = []
        cons = []
        sums = []
        
        if container:
            for p in container.find_all(['p', 'li']):
                txt = p.get_text(strip=True)
                if any(ch in txt for ch in ['✔️', '✓']):
                    clean_p = txt.replace('✔️', '').replace('✓', '').strip()
                    if clean_p and clean_p not in pros:
                        pros.append(clean_p)
                elif any(ch in txt for ch in ['❌', '✗']):
                    clean_c = txt.replace('❌', '').replace('✗', '').strip()
                    if clean_c and clean_c not in cons:
                        cons.append(clean_c)
                elif len(txt) > 35 and not any(ch in txt for ch in ['✔️', '✓', '❌', '✗']):
                    if not any(k in txt for k in ['Klicken Sie hier', 'Cliquez ici', 'Haga clic', 'Clicca qui', 'GyG', 'GetYourGuide', 'Viator', 'partner_id']):
                        if txt not in sums:
                            sums.append(txt)
                            
        tours.append({
            'index': i,
            'full_title': full_title,
            'clean_title': clean_title,
            'pros': pros,
            'cons': cons,
            'summaries': sums[:4]
        })
    return tours

def create_pro_con_html(soup, pros, cons, pros_label="Pros:", cons_label="Cons:"):
    """Build canonical clean pro/con box matching Luxury Editorial System."""
    wrapper = soup.new_tag('div', **{'class': 'pro-con-box-wrapper'})
    grid = soup.new_tag('div', **{'class': 'w-layout-grid pro-con-box-grid'})
    wrapper.append(grid)
    
    # Pro Cell
    pro_cell = soup.new_tag('div', **{'class': 'pro-con-box-pro-cell'})
    pro_rich = soup.new_tag('div', **{'class': 'pro-con-box-pro-cell-rich-text-block w-richtext'})
    h3_pro = soup.new_tag('h3')
    st_pro = soup.new_tag('strong')
    st_pro.string = pros_label
    h3_pro.append(st_pro)
    pro_rich.append(h3_pro)
    
    ul_pro = soup.new_tag('ul', **{'role': 'list'})
    for p_item in pros:
        li = soup.new_tag('li')
        parts = p_item.split('–', 1) if '–' in p_item else p_item.split('—', 1)
        if len(parts) == 2:
            st = soup.new_tag('strong')
            st.string = parts[0].strip()
            li.append(st)
            li.append(f" — {parts[1].strip()}")
        else:
            li.string = p_item
        ul_pro.append(li)
    pro_rich.append(ul_pro)
    pro_cell.append(pro_rich)
    grid.append(pro_cell)
    
    # Con Cell
    con_cell = soup.new_tag('div', **{'class': 'pro-con-box-con-cell'})
    con_rich = soup.new_tag('div', **{'class': 'pro-con-box-con-cell-rich-text-block w-richtext'})
    h3_con = soup.new_tag('h3')
    st_con = soup.new_tag('strong')
    st_con.string = cons_label
    h3_con.append(st_con)
    con_rich.append(h3_con)
    
    ul_con = soup.new_tag('ul', **{'role': 'list'})
    for c_item in cons:
        li = soup.new_tag('li')
        parts = c_item.split('–', 1) if '–' in c_item else c_item.split('—', 1)
        if len(parts) == 2:
            st = soup.new_tag('strong')
            st.string = parts[0].strip()
            li.append(st)
            li.append(f" — {parts[1].strip()}")
        else:
            li.string = c_item
        ul_con.append(li)
    con_rich.append(ul_con)
    con_cell.append(con_rich)
    grid.append(con_cell)
    
    return wrapper

def localize_universal_links(soup, lang, river_slug, dinner_slug):
    """Rewrite all internal links so user stays in /{lang}/ across the whole site."""
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith(('http://', 'https://', 'mailto:', 'tel:', 'javascript:')):
            if 'legenda.hu' in href and 'partner=38585' not in href:
                sep = '&' if '?' in href else '?'
                a['href'] = f"{href}{sep}partner=38585"
            continue
        if href.startswith('#'):
            continue

        clean = href
        for l in LANGS:
            if clean.startswith(f"/{l}/"):
                clean = clean[len(l)+1:]
                break
            elif clean == f"/{l}":
                clean = "/"
                break

        if clean in ['/best-budapest-river-cruises', '/budapest-river-cruises', '/river', 'best-budapest-river-cruises']:
            a['href'] = f"/{lang}/{river_slug}"
        elif clean in ['/best-dinner-cruises-budapest', '/budapest-dinner-cruises', '/dinner', 'best-dinner-cruises-budapest']:
            a['href'] = f"/{lang}/{dinner_slug}"
        elif clean in ['/', '']:
            a['href'] = f"/{lang}/"
        elif clean in ['/about', 'about']:
            a['href'] = f"/{lang}/about"
        elif clean.startswith('/about#'):
            a['href'] = f"/{lang}/about{clean[6:]}"
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

def compile_private_boats_guide(lang, en_html):
    """Compile localized Private Boat Tours guide for a given language."""
    data = I18N.get(lang, I18N.get('en', {}))
    ui = data.get('ui', {})
    slugs = SLUG_MAP[lang]
    river_slug = slugs['river']
    dinner_slug = slugs['dinner']
    
    harvested_path = os.path.join(CACHE_DIR, lang, 'private_boats.html')
    tours = extract_private_tours(lang)
    
    soup = BeautifulSoup(en_html, 'html.parser')
    
    # 1. HTML lang & RTL
    html_tag = soup.find('html')
    if html_tag:
        html_tag['lang'] = lang
        if lang == 'he':
            html_tag['dir'] = 'rtl'
        elif html_tag.has_attr('dir'):
            del html_tag['dir']
            
    # 2. Canonical URL
    can = soup.find('link', {'rel': 'canonical'})
    if can:
        can['href'] = f"https://www.budapestadventures.com/{lang}/best-private-boat-tours-budapest"
        
    # 3. Title & Meta
    h_soup = BeautifulSoup(open(harvested_path, encoding='utf-8'), 'html.parser') if os.path.exists(harvested_path) else None
    
    # Page Title
    cards_data = data.get('cards', [])
    page_title = None
    if len(cards_data) > 3 and cards_data[3].get('title'):
        page_title = cards_data[3]['title']
    elif h_soup and h_soup.title:
        page_title = h_soup.title.text.strip()
        
    if soup.title and page_title:
        soup.title.string = f"{page_title} (2026) | Budapest Adventures"
        
    if h_soup:
        m_desc = h_soup.find('meta', {'name': 'description'})
        if m_desc and m_desc.get('content'):
            m_target = soup.find('meta', {'name': 'description'})
            if m_target:
                m_target['content'] = m_desc['content'].strip()

    # 4. Universal Navigation Links
    localize_universal_links(soup, lang, river_slug, dinner_slug)
    
    # 5. Language Switcher Label
    active_lang_lbl = soup.find(id='lttActiveLangLabel')
    if active_lang_lbl:
        active_lang_lbl.string = lang.upper()
        
    # Ensure language grid links point to /{l}/best-private-boat-tours-budapest
    for a in soup.select('.ltt-lang-item, .ltt-mobile-lang-chip'):
        l_code = a.get('data-lang')
        if l_code:
            if l_code == 'en':
                a['href'] = '/best-private-boat-tours-budapest'
            else:
                a['href'] = f"/{l_code}/best-private-boat-tours-budapest"
            if l_code == lang:
                a['class'] = a.get('class', []) + ['active']
            elif 'active' in a.get('class', []):
                a['class'] = [c for c in a['class'] if c != 'active']

    # 6. Hero Card (.ltt-clean-card)
    # H1
    h1 = soup.find('h1')
    if h1 and page_title:
        h1.string = page_title
        
    # Breadcrumbs
    bc = soup.find(class_='ltt-breadcrumb')
    if bc:
        links = bc.find_all('a')
        if len(links) >= 1:
            links[0].string = ui.get('home', 'Home')
            links[0]['href'] = f"/{lang}/"
        if len(links) >= 2:
            links[1].string = cards_data[0].get('title', 'Budapest River Cruises') if cards_data else 'Budapest River Cruises'
            links[1]['href'] = f"/{lang}/{river_slug}"
            
    # Filter Pills
    tab_all = soup.find(class_='ltt-tab-btn', attrs={'data-cat': 'all'})
    if tab_all:
        tab_all.string = f"{ui.get('all', 'All')} (5)"
    tab_tested = soup.find(class_='ltt-tab-btn', attrs={'data-cat': 'tested'})
    if tab_tested:
        tab_tested.string = f"{ui.get('personally_tested', '✓ Personally Tested')} (5)"

    # 7. Localize Buttons & Microcopy
    btn_check_text = ui.get('btn_check', 'Check Availability →')
    for btn in soup.find_all(class_='bpa-btn'):
        btn.string = btn_check_text
        
    read_rev_text = ui.get('read_review', 'Read Review ↓')
    for sublink in soup.find_all(class_='bpa-sublink'):
        sublink.string = read_rev_text

    proof_text = ui.get('personally_tested', '✓ Personally Tested')
    for vchip in soup.find_all(class_='bpa-vchip'):
        vchip.string = proof_text

    # Trust micro badges
    for micro in soup.find_all(class_='bpa-trust-micro'):
        spans = micro.find_all('span')
        if len(spans) >= 3:
            spans[0].string = ui.get('instant_qr', 'Instant QR')
            spans[2].string = ui.get('cancellation', 'Free 24h Cancellation')
            
    # 8. Localize Deck Comparison Cards (.bpa-card) & Details (.bpa-details-card)
    deck_cards = soup.select('#ltt-cards-deck .bpa-card')
    details_cards = soup.select('details.bpa-details-card')
    
    # Get tour titles
    tour_titles = NATIVE_TOUR_TITLES.get(lang, [])
    
    for idx, card in enumerate(deck_cards):
        t_data = tours[idx] if idx < len(tours) else None
        
        # Determine title
        t_title = None
        if idx < len(tour_titles):
            t_title = tour_titles[idx]
        elif t_data and t_data.get('clean_title'):
            t_title = t_data['clean_title']
            
        if t_title:
            c_title = card.find(class_='bpa-title')
            if c_title:
                c_title.string = t_title
                
        # Details card synchronization
        if idx < len(details_cards):
            d_card = details_cards[idx]
            
            # Summary title
            d_title = d_card.find(class_='bpa-details-title')
            if d_title and t_title:
                d_title.string = t_title
                
            # Pros & Cons
            if t_data and (t_data.get('pros') or t_data.get('cons')):
                old_procon = d_card.find(class_='pro-con-box-wrapper')
                if old_procon:
                    new_procon = create_pro_con_html(
                        soup, 
                        t_data.get('pros', []), 
                        t_data.get('cons', []),
                        pros_label=ui.get('pros', 'Pros:'),
                        cons_label=ui.get('cons', 'Cons:')
                    )
                    old_procon.replace_with(new_procon)
                    
            # Localize Bento summary text if available
            if t_data and t_data.get('summaries'):
                bento_sum = d_card.find(class_='ltt-bento-group')
                if bento_sum:
                    # Keep booking card, but replace p tags
                    p_tags = bento_sum.find_all('p')
                    for p_idx, p_tag in enumerate(p_tags):
                        if p_idx < len(t_data['summaries']):
                            p_tag.string = t_data['summaries'][p_idx]
                            
            # Localize Buy Card in details
            buy_card = d_card.find(class_='ltt-buy-card')
            if buy_card:
                buy_btn = buy_card.find(class_='bpa-btn')
                if buy_btn:
                    buy_btn.string = btn_check_text

    # 9. Localize Table of Contents
    toc = soup.find(id='toc')
    if toc:
        toc_title = toc.find(class_='toc-title')
        if toc_title:
            toc_title.string = ui.get('toc', 'Table of Contents')
        toc_links = toc.find_all('a', class_='tocitem')
        for idx, tlink in enumerate(toc_links):
            if idx < len(deck_cards):
                c_title_el = deck_cards[idx].find(class_='bpa-title')
                if c_title_el:
                    tlink.string = f"#{idx+1} {c_title_el.text.strip()}"
                    
    # 10. Localize Footer (.footer-dark)
    foot_data = data.get('footer', {})
    foot_p = soup.find('p', class_='footer-paragraph')
    if foot_p and foot_data.get('p'):
        foot_p.string = foot_data['p']
        
    for f_col in soup.find_all(class_='footer-link-column'):
        ftitle = f_col.find(class_='footer-link-title')
        if ftitle:
            if 'Flagship' in ftitle.text or 'Popular' in ftitle.text:
                ftitle.string = foot_data.get('popular', 'Popular Flagship Guides')
            elif 'Company' in ftitle.text or 'Trust' in ftitle.text:
                ftitle.string = foot_data.get('company', 'Company & Trust')

    return str(soup)

def main():
    print("=== Compiling Multilingual Private Boat Tours Guides (Luxury Editorial System) ===")
    
    with open(MASTER_EN_PATH, 'r', encoding='utf-8') as f:
        en_html = f.read()
        
    compiled_count = 0
    for lang in LANGS:
        out_dir = os.path.join(BASE_DIR, lang, 'best-private-boat-tours-budapest')
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, 'index.html')
        
        localized_html = compile_private_boats_guide(lang, en_html)
        
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(localized_html)
            
        compiled_count += 1
        print(f"✓ [{lang.upper()}] Compiled Luxury Private Boat Tours Guide -> {out_path}")
        
    print("\n=======================================================")
    print(f"PRIVATE BOATS MULTILINGUAL COMPILATION COMPLETE:")
    print(f"  Successfully compiled: {compiled_count} / {len(LANGS)} foreign languages")
    print("=======================================================")

if __name__ == '__main__':
    main()
