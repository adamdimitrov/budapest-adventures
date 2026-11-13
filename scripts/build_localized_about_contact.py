"""Rebuild localized About/Contact pages from the English templates (about.html, contact.html).

Header and footer come from the same language's homepage (already translated); the page body
and meta strings come from translated fragments in <indir>/<lang>/{about,contact}.html + meta.json.

usage: python3 scripts/build_localized_about_contact.py <indir> [lang ...]
"""
import html
import json
import os
import re
import sys
from urllib.parse import unquote, urlparse
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from fix_language_switcher_links import fix_switcher_html  # keeps switcher links = hreflang

BASE = 'https://www.budapestadventures.com'


def cut(s, start_pat, end_tag):
    i = s.index(start_pat)
    return i, s.index(end_tag, i) + len(end_tag)


def build(page, lang, indir):
    s = open(f'{page}.html', encoding='utf-8').read()
    home = open(f'{lang}/index.html', encoding='utf-8').read()
    head = s[:s.index('</head>')]
    alts = {l: h for h, l in re.findall(r'<link href="([^"]+)" hreflang="([^"]+)" rel="alternate"/>', head)}
    url = alts[lang]
    path = unquote(urlparse(url).path)
    frag = open(f'{indir}/{lang}/{page}.html', encoding='utf-8').read()
    meta = json.load(open(f'{indir}/{lang}/meta.json', encoding='utf-8'))[page]

    # header from the localized homepage, language links -> this page's alternates
    hi, he = cut(home, '<header class="ltt-navbar"', '</header>')
    header = home[hi:he]

    def fix_item(m):
        code = m.group(2)
        href = unquote(urlparse(alts.get(code, m.group(3))).path) or '/'
        return f'<a class="ltt-lang-item{" current" if code == lang else ""}" data-lang="{code}" href="{href}"'
    header = re.sub(r'<a class="ltt-lang-item( current)?" data-lang="([\w-]+)" href="([^"]*)"', fix_item, header)
    for cls in ('ltt-nav-link', 'ltt-mobile-link'):
        header = re.sub(r'<a class="%s( [^"]*)?" href="%s">' % (cls, re.escape(path)),
                        lambda m: f'<a aria-current="page" class="{cls} active{m.group(1) or ""}" href="{path}">', header)
    fi, fe = cut(home, '<footer class="footer-dark ltt-footer"', '</footer>')
    footer = home[fi:fe]

    a, b = cut(s, '<header class="ltt-navbar"', '</header>')
    c = s.index('<footer class="footer-dark ltt-footer"')
    d = s.index('</footer>', c) + 9
    s = s[:a] + header + frag + footer + s[d:]

    # head
    s = re.sub(r'<html[^>]*>', re.search(r'<html[^>]*>', home).group(0), s, count=1)
    s = re.sub(r'<title>.*?</title>', f'<title>{meta["title"]}</title>', s, count=1)
    for k, v in meta.items():
        if k == 'title':
            continue
        attr = 'property' if k.startswith('og:') else 'name'
        s = re.sub(r'<meta content="[^"]*" %s="%s"/>' % (attr, re.escape(k)),
                   lambda m: f'<meta content="{v}" {attr}="{k}"/>', s, count=1)
    s = re.sub(r'<link href="[^"]*" rel="canonical"/>', f'<link href="{url}" rel="canonical"/>', s, count=1)
    s = re.sub(r'<meta content="[^"]*" property="og:url"/>', f'<meta content="{url}" property="og:url"/>', s, count=1)
    loc = re.search(r'<meta content="([^"]*)" property="og:locale"/>', home)
    if loc:
        s = re.sub(r'<meta content="[^"]*" property="og:locale"/>', f'<meta content="{loc.group(1)}" property="og:locale"/>', s, count=1)
    out = path.strip('/') + '/index.html'
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(fix_switcher_html(s, out))
    return out


if __name__ == '__main__':
    indir = sys.argv[1]
    langs = sys.argv[2:] or sorted(os.listdir(indir))
    for lang in langs:
        for page in ('about', 'contact'):
            print(build(page, lang, indir))
