"""Replace the old Webflow nav on localized pages with the new translated mega header.

The header is taken from the same language's homepage (L/index.html, already translated),
its language-switcher links are rewritten to the page's own hreflang alternates, and the
header styles are copied from an English article.

usage: python3 scripts/swap_localized_header.py <file> [<file> ...]
"""
import re
import sys
from urllib.parse import unquote, urlparse

BASE = 'https://www.budapestadventures.com'
NAV_STYLES = re.search(r'<style id="ltt-nav-styles">.*?</style>',
                       open('best-hostels-budapest.html', encoding='utf-8').read(), re.S).group(0)
NAV_SCRIPT_SRC = 'best-hostels-budapest.html'
_donors = {}


def block(s, ident, tag):
    m = re.search(r'<%s\b[^>]*id="%s"[^>]*>.*?</%s>' % (tag, ident, tag), s, re.S)
    return m.group(0) if m else None


def donor_header(lang):
    if lang not in _donors:
        s = open(f'{lang}/index.html', encoding='utf-8').read()
        i = s.index('<header class="ltt-navbar"')
        _donors[lang] = (s[i:s.index('</header>', i) + 9], block(s, 'ltt-nav-script', 'script'))
    return _donors[lang]


def balanced_div_end(s, i):
    depth = 0
    for m in re.compile(r'<(/?)div\b[^>]*>').finditer(s, i):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return m.end()
    raise ValueError('unbalanced')


def swap(f):
    lang = f.split('/')[0]
    s = open(f, encoding='utf-8').read()
    i = s.find('<div class="t-navigation w-nav"')
    if i < 0 or '<header class="ltt-navbar"' in s:
        return 'skip'
    head = s[:s.index('</head>')]
    alts = {l: unquote(urlparse(h).path) or '/' for h, l in
            re.findall(r'<link href="([^"]+)" hreflang="([^"]+)" rel="alternate"/>', head)}
    header, nav_script = donor_header(lang)

    def fix_item(m):
        code = m.group(2)
        href = alts.get(code, m.group(3))
        cls = ' current' if code == lang else ''
        return f'<a class="ltt-lang-item{cls}" data-lang="{code}" href="{href}"'
    header = re.sub(r'<a class="ltt-lang-item( current)?" data-lang="([\w-]+)" href="([^"]*)"', fix_item, header)
    e = balanced_div_end(s, i)
    s = s[:i] + header + s[e:]
    # styles: page may carry an older copy; use the canonical one
    old = block(s, 'ltt-nav-styles', 'style')
    s = s.replace(old, NAV_STYLES) if old else s.replace('</head>', NAV_STYLES + '</head>', 1)
    # nav controller must exist (all these pages already carry it; add if missing)
    if not block(s, 'ltt-nav-script', 'script') and nav_script:
        s = s.replace('</body>', nav_script + '</body>', 1)
    open(f, 'w', encoding='utf-8').write(s)
    return 'ok'


if __name__ == '__main__':
    import collections
    c = collections.Counter(swap(f) for f in sys.argv[1:])
    print(dict(c))
