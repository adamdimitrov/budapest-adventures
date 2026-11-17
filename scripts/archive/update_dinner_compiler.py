import re

with open('/Users/adamdimitrov/Development/budapest-adventures/scripts/master_dinner_multilingual_compiler.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add imports & DOCK_TERMS
if 'from dinner_spec_chips_i18n import DINNER_SPEC_CHIPS_I18N' not in code:
    import_insert = '''from dinner_spec_chips_i18n import DINNER_SPEC_CHIPS_I18N

DOCK_TERMS = {
    'hu': 'Kikötő', 'de': 'Anleger', 'fr': 'Quai', 'es': 'Muelle',
    'it': 'Molo', 'nl': 'Steiger', 'pl': 'Przystań', 'ro': 'Pontonul',
    'cs': 'Přístaviště', 'sk': 'Prístavisko', 'hr': 'Pristanište',
    'sr': 'Пристаниште', 'bg': 'Кей', 'ru': 'Причал', 'uk': 'Причал',
    'el': 'Αποβάθρα', 'tr': 'İskele', 'pt': 'Cais', 'he': 'רציף',
    'ja': '桟橋', 'ko': '선착장'
}
'''
    code = code.replace('from dinner_toc_i18n import DINNER_TOC_I18N', f'from dinner_toc_i18n import DINNER_TOC_I18N\n{import_insert}')

# 2. Update load_combined_walkthrough to include bento1 paragraphs
old_load = '''def load_combined_walkthrough():
    """Loads and combines walkthrough data from the 3 group JSON files."""
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
    return combined'''

new_load = '''def load_combined_walkthrough():
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
            
    return combined'''

code = code.replace(old_load, new_load)

# 3. Update localize_deck_cards for dock name, spec chips, and vchip
old_deck_dock = '''            if map_link:
                dock_name = map_link.get_text(strip=True)
                map_href = map_link.get('href', '')'''

new_deck_dock = '''            if map_link:
                dock_name = map_link.get_text(strip=True)
                dock_term = DOCK_TERMS.get(lang, 'Dock')
                dock_name = re.sub(r'\\bDock\\b', dock_term, dock_name, flags=re.IGNORECASE)
                map_href = map_link.get('href', '')'''

code = code.replace(old_deck_dock, new_deck_dock, 1)

old_deck_cta_end = '''            sublink = cta_cell.find(class_='bpa-sublink')
            if sublink and ui.get('read_review'):
                sublink.string = ui['read_review']'''

new_deck_cta_end = '''            sublink = cta_cell.find(class_='bpa-sublink')
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
            vc.string = ui.get('tested', '✓ Personally Tested')'''

code = code.replace(old_deck_cta_end, new_deck_cta_end, 1)

# 4. Update details cards for dock name in summary kicker
old_details_dock = '''            if kicker_el:
                map_link = kicker_el.find('a', class_='bpa-kicker-map-link')
                if map_link:
                    dock_name = map_link.get_text(strip=True)
                    map_href = map_link.get('href', '')'''

new_details_dock = '''            if kicker_el:
                map_link = kicker_el.find('a', class_='bpa-kicker-map-link')
                if map_link:
                    dock_name = map_link.get_text(strip=True)
                    dock_term = DOCK_TERMS.get(lang, 'Dock')
                    dock_name = re.sub(r'\\bDock\\b', dock_term, dock_name, flags=re.IGNORECASE)
                    map_href = map_link.get('href', '')'''

code = code.replace(old_details_dock, new_details_dock, 1)

# 5. Bento 1 paragraphs injection in details cards
old_bento1_bq = '''                    elif '💡' in btxt or 'undercover' in btxt.lower():
                        if c_idx == 0 and 'legenda' in undercover_dict:
                            bq.string = undercover_dict['legenda']
                        elif c_idx == 3 and 'piano' in undercover_dict:
                            bq.string = undercover_dict['piano']'''

new_bento1_bq = '''                    elif '💡' in btxt or 'undercover' in btxt.lower():
                        if c_idx == 0 and 'legenda' in undercover_dict:
                            bq.string = undercover_dict['legenda']
                        elif c_idx == 3 and 'piano' in undercover_dict:
                            bq.string = undercover_dict['piano']

                # Inject localized Bento 1 review paragraphs
                bento1_paras = walkthrough.get('bento1_paragraphs', [])
                if bento1_paras and c_idx < len(bento1_paras):
                    c_paras = bento1_paras[c_idx]
                    rt = bg.find(class_='w-richtext')
                    if rt:
                        rt_ps = rt.find_all('p')
                        for p_idx, p_elem in enumerate(rt_ps):
                            if p_idx < len(c_paras):
                                p_text = c_paras[p_idx]
                                p_elem.clear()
                                p_frag = BeautifulSoup(p_text, 'html.parser')
                                p_elem.append(p_frag)'''

code = code.replace(old_bento1_bq, new_bento1_bq, 1)

# 6. Bento 4 dock localization in transit lines
old_bento4_meet = '''                transit_lis = bg.find_all('li')
                card_key = f"card_{c_idx+1}"'''

new_bento4_meet = '''                transit_lis = bg.find_all('li')
                card_key = f"card_{c_idx+1}"
                dock_term = DOCK_TERMS.get(lang, 'Dock')'''

code = code.replace(old_bento4_meet, new_bento4_meet, 1)

# 7. Meta tags fallback and global vchip
old_meta = '''    for og_t in soup.find_all('meta', property=lambda p: p and 'title' in p):
        if pm.get('og_title'): og_t['content'] = pm['og_title']
    for og_d in soup.find_all('meta', property=lambda p: p and 'description' in p):
        if pm.get('og_desc'): og_d['content'] = pm['og_desc']
    for tw_t in soup.find_all('meta', attrs={'name': lambda n: n and 'title' in n}):
        if pm.get('og_title'): tw_t['content'] = pm['og_title']
    for tw_d in soup.find_all('meta', attrs={'name': lambda n: n and 'description' in n}):
        if pm.get('og_desc'): tw_d['content'] = pm['og_desc']'''

new_meta = '''    page_title = pm.get('og_title') or pm.get('title')
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
        vc.string = tested_label'''

code = code.replace(old_meta, new_meta, 1)

with open('/Users/adamdimitrov/Development/budapest-adventures/scripts/master_dinner_multilingual_compiler.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("master_dinner_multilingual_compiler.py updated successfully!")
