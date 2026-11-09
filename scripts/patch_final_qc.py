import re

with open('/Users/adamdimitrov/Development/budapest-adventures/scripts/master_dinner_multilingual_compiler.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update localize_css_pseudo
old_pseudo = '''def localize_css_pseudo(soup, lang, ui):
    """Localizes CSS pseudo-elements like content:'Read Review' inside style tags."""
    read_text = ui.get('read_review', 'Read Review ↓').replace('"', '\\"')
    close_text = ui.get('close_review', 'Close Review ↑').replace('"', '\\"')
    for st in soup.find_all('style'):
        if st.string and 'content:"Read Review"' in st.string:
            st.string = st.string.replace('content:"Read Review"', f'content:"{read_text}"')
            st.string = st.string.replace('content:"Close Review"', f'content:"{close_text}"')'''

new_pseudo = '''def localize_css_pseudo(soup, lang, ui):
    """Localizes CSS pseudo-elements like content:'Read Review' inside style tags."""
    read_text = ui.get('read_review', 'Read Review ↓').replace('"', '\\"')
    close_text = ui.get('close_review', 'Close Review ↑').replace('"', '\\"')
    for st in soup.find_all('style'):
        if st.string:
            st.string = re.sub(r'content:\s*"Read Review[^"]*"', f'content:"{read_text}"', st.string)
            st.string = re.sub(r'content:\s*"Close Review[^"]*"', f'content:"{close_text}"', st.string)
            st.string = re.sub(r'content:\s*"Collapse Review[^"]*"', f'content:"{close_text}"', st.string)'''

code = code.replace(old_pseudo, new_pseudo)

# 2. In Bento 4 bios: clean Dock 11
old_bio = '''                    p = sp.find('p')
                    if p:
                        bio_keys = ['legenda', 'silverline_budget', 'silverline_folk', 'silverline_piano', 'hungaria', 'eurama', 'rubin']
                        if c_idx < len(bio_keys) and bio_keys[c_idx] in bios_dict:
                            p.string = bios_dict[bio_keys[c_idx]]'''

new_bio = '''                    p = sp.find('p')
                    if p:
                        bio_keys = ['legenda', 'silverline_budget', 'silverline_folk', 'silverline_piano', 'hungaria', 'eurama', 'rubin']
                        if c_idx < len(bio_keys) and bio_keys[c_idx] in bios_dict:
                            bio_txt = bios_dict[bio_keys[c_idx]]
                            dock_term = DOCK_TERMS.get(lang, 'Dock')
                            bio_txt = re.sub(r'\\bDock\\s*(\\d+)', f'{dock_term} \\1', bio_txt, flags=re.IGNORECASE)
                            bio_txt = re.sub(r'\\bDock\\b', dock_term, bio_txt, flags=re.IGNORECASE)
                            if lang in ['ja', 'ko']:
                                bio_txt = re.sub(r'[（\\(]Dock\\s*\\d+[）\\)]', '', bio_txt, flags=re.IGNORECASE)
                            p.string = bio_txt'''

code = code.replace(old_bio, new_bio)

# 3. In leaf lis: clean welcome drink for cs & sk
old_lis = '''                    leaf_lis = [li for li in sp.find_all('li') if not li.find('li')]
                    for lli in leaf_lis:
                        if leaf_li_idx < len(leaf_lis_list):
                            t_li = leaf_lis_list[leaf_li_idx]
                            set_li_strong(lli, t_li, soup, lang)
                            leaf_li_idx += 1'''

new_lis = '''                    leaf_lis = [li for li in sp.find_all('li') if not li.find('li')]
                    for lli in leaf_lis:
                        if leaf_li_idx < len(leaf_lis_list):
                            t_li = leaf_lis_list[leaf_li_idx]
                            if lang == 'cs':
                                t_li = re.sub(r'\\bwelcome drink\\b', 'nápoj na uvítanou', t_li, flags=re.IGNORECASE)
                            elif lang == 'sk':
                                t_li = re.sub(r'\\bwelcome drink\\b', 'prípitok na privítanie', t_li, flags=re.IGNORECASE)
                            set_li_strong(lli, t_li, soup, lang)
                            leaf_li_idx += 1'''

code = code.replace(old_lis, new_lis)

# 4. In Hungarian footer description: audio guide-okat -> audioguide-okat
old_footer = '''    # Determine output path'''
new_footer = '''    if lang == 'hu':
        for el in soup.find_all(text=lambda t: t and 'audio guide-okat' in t):
            el.replace_with(el.replace('audio guide-okat', 'audioguide-okat'))

    # Determine output path'''

code = code.replace(old_footer, new_footer)

with open('/Users/adamdimitrov/Development/budapest-adventures/scripts/master_dinner_multilingual_compiler.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("master_dinner_multilingual_compiler.py successfully patched with final QC fixes!")
