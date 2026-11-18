"""Polish the translated mega header on localized pages.

- language badge shows the page language (was hard-coded EN)
- long translated labels no longer wrap: nowrap + tighter gaps, and below 1440px the two
  direct cruise links (also inside the dropdown) are hidden
- de-duplicate the first direct link where it repeated the dropdown label (el, pt, ja)
usage: python3 scripts/fix_localized_header_fit.py   (all localized pages)
"""
import glob
import re

LANGS = 'bg cs de el es fr he hr hu it ja ko nl pl pt ro ru sk sr tr uk'.split()
CSS = ('<style id="ltt-nav-i18n-fit">.ltt-nav-link{white-space:nowrap}'
       '@media (min-width:992px){.ltt-nav-inner{gap:24px}.ltt-nav-links{gap:4px}}@media (min-width:1440px){.ltt-nav-inner{max-width:1340px}}'
       '@media (min-width:992px) and (max-width:1439px){.ltt-nav-links>a.ltt-nav-link:nth-of-type(-n+2){display:none}}'
       '</style>')
RELABEL = {'el': ('Κρουαζιέρες στον Δούναβη', 'Κρουαζιέρες Ποταμού'),
           'pt': ('Cruzeiros no Danúbio', 'Cruzeiros Fluviais'),
           'ja': ('ダニューブ川クルーズ', 'リバークルーズ')}
n = 0
for L in LANGS:
    for f in glob.glob(f'{L}/index.html') + glob.glob(f'{L}/**/index.html', recursive=True):
        s = open(f, encoding='utf-8').read()
        i = s.find('<header class="ltt-navbar"')
        if i < 0:
            continue
        j = s.index('</header>', i)
        h = s[i:j]
        h2 = h.replace('id="lttActiveLangLabel">EN<', f'id="lttActiveLangLabel">{L.upper()}<')
        if L in RELABEL:
            a, b = RELABEL[L]
            h2 = re.sub(r'(<a (?:aria-current="page" )?class="ltt-(?:nav|mobile)-link[^"]*" href="[^"]*">\s*)' + re.escape(a) + r'(?=\s*<)',
                        lambda m: m.group(1) + b, h2)
            if L == 'ja':
                h2 = h2.replace(a, b)
        s2 = s[:i] + h2 + s[j:]
        if 'id="ltt-nav-i18n-fit"' not in s2:
            s2 = s2.replace('</head>', CSS + '</head>', 1)
        if s2 != s:
            open(f, 'w', encoding='utf-8').write(s2)
            n += 1
print(n, 'files updated')
