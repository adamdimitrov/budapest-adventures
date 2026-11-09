import re

with open('/Users/adamdimitrov/Development/budapest-adventures/scripts/master_dinner_multilingual_compiler.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add import DINNER_QF_LABELS
if 'from dinner_qf_labels_i18n import DINNER_QF_LABELS' not in code:
    code = code.replace(
        'from dinner_spec_chips_i18n import DINNER_SPEC_CHIPS_I18N',
        'from dinner_spec_chips_i18n import DINNER_SPEC_CHIPS_I18N\nfrom dinner_qf_labels_i18n import DINNER_QF_LABELS'
    )

# 2. Add loading qf_values in load_combined_walkthrough
old_b1_load = '''    b1_path = os.path.join(BASE_DIR, 'data', 'dinner_bento1_paragraphs_i18n.json')
    if os.path.exists(b1_path):
        try:
            with open(b1_path, 'r', encoding='utf-8') as f:
                b1_data = json.load(f)
                for l, paras in b1_data.items():
                    if l in combined:
                        combined[l]['bento1_paragraphs'] = paras
        except Exception as e:
            print(f"Error loading bento1 paragraphs: {e}")'''

new_b1_load = '''    b1_path = os.path.join(BASE_DIR, 'data', 'dinner_bento1_paragraphs_i18n.json')
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
            print(f"Error loading qf values: {e}")'''

code = code.replace(old_b1_load, new_b1_load)

# 3. Add buy-card localization inside Bento 1
old_b1_p = '''                                p_elem.clear()
                                p_frag = BeautifulSoup(p_text, 'html.parser')
                                p_elem.append(p_frag)'''

new_b1_p = '''                                p_elem.clear()
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
                            dep_text_loc = re.sub(r'\\bDock\\b', dock_term, dep_text, flags=re.IGNORECASE)
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
                        btn.string = ui['btn_check']'''

code = code.replace(old_b1_p, new_b1_p, 1)

# 4. Add qf1-wrap full localization
old_qf = '''        # 4. Quick facts table
        qf_wrap = body.find(class_='qf1-wrap')
        if qf_wrap:
            qf_title = qf_wrap.find(class_='qf1-title')
            if qf_title:
                qf_title.string = ui.get('quick_facts', 'Quick Facts — Verified Field Specs')'''

new_qf = '''        # 4. Quick facts table
        qf_wrap = body.find(class_='qf1-wrap')
        if qf_wrap:
            qf_title = qf_wrap.find(class_='qf1-title')
            if qf_title:
                qf_title.string = ui.get('quick_facts', 'Quick Facts — Verified Field Specs')
                
            qf_badge = qf_wrap.find(class_='qf1-badge')
            if qf_badge:
                dock_term = DOCK_TERMS.get(lang, 'Dock')
                qf_badge.string = re.sub(r'\\bDock\\b', dock_term, qf_badge.get_text(strip=True), flags=re.IGNORECASE)
                
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
                        val.string = re.sub(r'\\bDock\\b', dock_term, vtxt, flags=re.IGNORECASE)'''

code = code.replace(old_qf, new_qf, 1)

with open('/Users/adamdimitrov/Development/budapest-adventures/scripts/master_dinner_multilingual_compiler.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("master_dinner_multilingual_compiler.py patched with QF & Buy Card successfully!")
