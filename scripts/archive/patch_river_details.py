with open('/Users/adamdimitrov/Development/budapest-adventures/scripts/master_river_multilingual_compiler.py', 'r', encoding='utf-8') as f:
    code = f.read()

target = '''        # Details title
        d_title = dcard.find(class_='bpa-details-title')
        if d_title:
            d_title.string = tdata['clean_title']'''

replacement = '''        # Rank tag
        rank_tag = dcard.find(class_='bpa-rank-tag')
        if rank_tag and tdata.get('badge'):
            rank_tag.string = tdata['badge']

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
                        st.string = st.string.replace('Dock ', ku['dock'])'''

assert target in code, "Target not found in river compiler!"
code = code.replace(target, replacement)

with open('/Users/adamdimitrov/Development/budapest-adventures/scripts/master_river_multilingual_compiler.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("River compiler patched successfully!")
