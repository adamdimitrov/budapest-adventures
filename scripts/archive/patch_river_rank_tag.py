with open('/Users/adamdimitrov/Development/budapest-adventures/scripts/master_river_multilingual_compiler.py', 'r', encoding='utf-8') as f:
    code = f.read()

target = '''        # Rank tag
        rank_tag = dcard.find(class_='bpa-rank-tag')
        if rank_tag and tdata.get('badge'):
            rank_tag.string = tdata['badge']'''

replacement = '''        # Rank tag
        rank_tag = dcard.find(class_='bpa-rank-tag')
        badges = RANK_BADGES.get(lang, [])
        if rank_tag and idx < len(badges):
            rank_tag.string = badges[idx]'''

assert target in code, "Target not found in river compiler!"
code = code.replace(target, replacement)

with open('/Users/adamdimitrov/Development/budapest-adventures/scripts/master_river_multilingual_compiler.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("River compiler rank tag patched successfully!")
