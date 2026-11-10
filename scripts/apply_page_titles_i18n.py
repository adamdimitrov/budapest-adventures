"""Apply scripts/page_titles_i18n.py to localized pages.

Only fields that are still English (or half-English word swaps) are replaced, so
already-good native titles are left alone. Touches: <title>, <h1>, og:title,
twitter:title, meta/og/twitter description, JSON-LD headline.

usage: python3 scripts/apply_page_titles_i18n.py [--dry-run]
"""
import glob
import html
import json
import os
import re
import sys
from urllib.parse import unquote

sys.path.insert(0, os.path.dirname(__file__))
from page_titles_i18n import PAGE_TITLES  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRY = '--dry-run' in sys.argv
EN_WORDS = set('the and of to in for with is are this that you your on at by from or as be it an was we our have has '
               'will can best cruise cruises river night dinner boat boats personally tested paid hostels baths what '
               'which how walking thermal private unlimited evening tours tour guide local\'s get airport city centre '
               'booking form group experience explore top-rated'.split())


def english(text):
    words = re.findall(r'\w+', text or '')
    if not words:
        return False
    hits = sum(1 for w in re.findall(r"[A-Za-z']+", text) if w.lower() in EN_WORDS)
    return hits / len(words) >= 0.2


# Localized-slug copies of the same page (no hreflang to tell us their English twin).
ALIASES = {
    'mejores-recorridos-a-pie-budapest': 'best-walking-tours-budapest',
    'бест-валкинг-тоурс-будапест': 'best-walking-tours-budapest',
    'legjobb-privat-hajokirandulasok-budapest': 'best-private-boat-tours-budapest',
    'legjobb-privát-hajókirándulások-budapest': 'best-private-boat-tours-budapest',
}


def page_type(f, s):
    slug = f.split('/')[1]
    if slug in PAGE_TITLES or slug in ALIASES:
        return ALIASES.get(slug, slug)
    m = (re.search(r'<link[^>]*hreflang="en"[^>]*href="([^"]+)"', s)
         or re.search(r'<link[^>]*href="([^"]+)"[^>]*hreflang="en"', s))
    if not m:
        return None
    return unquote(m.group(1)).rstrip('/').rsplit('/', 1)[-1]


def set_meta(s, key, value, changes):
    pat = re.compile(r'<meta\b[^>]*\b(?:name|property)="%s"[^>]*>' % re.escape(key))

    def repl(m):
        tag = m.group(0)
        cur = re.search(r'\bcontent="([^"]*)"', tag)
        if cur and not english(html.unescape(cur.group(1))):
            return tag
        changes.append(key)
        new = 'content="%s"' % html.escape(value, quote=True)
        return re.sub(r'\bcontent="[^"]*"', lambda _: new, tag) if cur else tag.replace('<meta', '<meta ' + new, 1)

    return pat.sub(repl, s)


def main():
    os.chdir(ROOT)
    total = 0
    for f in sorted(glob.glob('*/*/index.html')):
        lang = f.split('/')[0]
        s = open(f, encoding='utf-8').read()
        ptype = page_type(f, s)
        data = PAGE_TITLES.get(ptype, {}).get(lang)
        if not data:
            continue
        title, desc = data
        changes = []

        def title_repl(m):
            if not english(html.unescape(m.group(2))):
                return m.group(0)
            changes.append('title')
            return m.group(1) + html.escape(title, quote=False) + m.group(3)

        s2 = re.sub(r'(<title>)([^<]*)(</title>)', title_repl, s, count=1)

        def h1_repl(m):
            text = re.sub(r'<[^>]+>', ' ', m.group(2))
            if not english(html.unescape(text)):
                return m.group(0)
            changes.append('h1')
            return m.group(1) + html.escape(title, quote=False) + m.group(3)

        s2 = re.sub(r'(<h1\b[^>]*>)(.*?)(</h1>)', h1_repl, s2, count=1, flags=re.S)
        def crumb_repl(m):
            if not english(html.unescape(m.group(2))):
                return m.group(0)
            changes.append('breadcrumb')
            return m.group(1) + html.escape(title, quote=False) + m.group(3)

        s2 = re.sub(r'(<div class="component-breadcrumb-rich-text[^"]*"><p><a [^>]*>[^<]*</a>\s*»\s*)([^<]+)(</p>)',
                    crumb_repl, s2, count=1)
        for key in ('og:title', 'twitter:title'):
            s2 = set_meta(s2, key, title, changes)
        for key in ('description', 'og:description', 'twitter:description'):
            s2 = set_meta(s2, key, desc, changes)

        def ld_repl(m):
            if not english(json.loads(m.group(2))):
                return m.group(0)
            changes.append('ld:headline')
            return m.group(1) + json.dumps(title, ensure_ascii=False)

        s2 = re.sub(r'("headline"\s*:\s*)("(?:[^"\\]|\\.)*")', ld_repl, s2)

        if s2 != s:
            total += 1
            print(f'{f}: {", ".join(changes)}')
            if not DRY:
                open(f, 'w', encoding='utf-8').write(s2)
    print(total, 'files', '(dry run)' if DRY else 'updated')


if __name__ == '__main__':
    main()
