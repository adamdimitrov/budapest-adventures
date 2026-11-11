#!/usr/bin/env python3
"""
Re-point every language-switcher link (desktop .ltt-lang-item and mobile
.ltt-mobile-lang-chip) at the URL declared in the page's own
<link rel="alternate" hreflang="..."> tags, and mark the page's own language
as `current`.

Why: several build scripts guess the target URL from folder names, which left
many translated pages with an "English" link pointing back to the translated
page (or to the language home), so visitors could not switch back to English.
The hreflang tags are the source of truth for page equivalents.

Only href/class attributes inside the switcher anchors are touched; the rest of
each file is left byte-for-byte unchanged. Safe to re-run; run it after any
script that regenerates the header/switcher.

Usage:  python3 scripts/fix_language_switcher_links.py [--dry-run]
"""
import glob
import os
import re
import sys
import urllib.parse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HREFLANG_RE = re.compile(r'<link\b[^>]*>', re.I)
ANCHOR_RE = re.compile(
    r'<a\b(?=[^>]*\bclass="(?:ltt-lang-item|ltt-mobile-lang-chip)\b)[^>]*>', re.I)
ATTR_RE = lambda name: re.compile(r'\b' + name + r'="([^"]*)"')


def lang_dirs():
    return {d for d in os.listdir(BASE_DIR)
            if os.path.isdir(os.path.join(BASE_DIR, d)) and re.fullmatch(r'[a-z]{2}', d) and d != 'js'}


def hreflang_map(html):
    out = {}
    for tag in HREFLANG_RE.findall(html):
        if 'alternate' not in tag:
            continue
        hl = ATTR_RE('hreflang').search(tag)
        href = ATTR_RE('href').search(tag)
        if not hl or not href or hl.group(1) == 'x-default':
            continue
        path = urllib.parse.urlsplit(href.group(1)).path or '/'
        out[hl.group(1)] = urllib.parse.unquote(path)
    return out


def page_lang(rel_path, langs):
    first = rel_path.split(os.sep)[0]
    return first if first in langs else 'en'


def fix_anchor(tag, hl, own_lang):
    m = re.search(r'\bdata-(?:m-)?lang="([^"]+)"', tag)
    if not m:
        return tag
    lang = m.group(1)
    target = hl.get(lang)
    new = tag
    if target:
        new = re.sub(r'\bhref="[^"]*"', 'href="%s"' % target, new, count=1)
    cls = ATTR_RE('class').search(new).group(1).split()
    want_current = lang == own_lang
    if want_current and 'current' not in cls:
        cls.append('current')
    elif not want_current and 'current' in cls:
        cls.remove('current')
    new = re.sub(r'\bclass="[^"]*"', 'class="%s"' % ' '.join(cls), new, count=1)
    return new


def fix_switcher_html(html, path):
    """Return `html` with every switcher link taken from its hreflang tags.

    Every script that writes a page must pass its output through this before
    writing, so a wrong guessed URL can never reach a published page.
    `path` is the output file (absolute, or relative to the repo root).
    Pages without an hreflang="en" tag (prototypes, mockups) are returned unchanged.
    """
    if 'ltt-lang-item' not in html and 'ltt-mobile-lang-chip' not in html:
        return html
    hl = hreflang_map(html)
    if 'en' not in hl:
        return html
    if not os.path.isabs(path):
        path = os.path.join(BASE_DIR, path)
    own = page_lang(os.path.relpath(os.path.abspath(path), BASE_DIR), lang_dirs())
    return ANCHOR_RE.sub(lambda m: fix_anchor(m.group(0), hl, own), html)


def main():
    dry = '--dry-run' in sys.argv
    langs = lang_dirs()
    files = set(glob.glob(os.path.join(BASE_DIR, '*.html')))
    files |= set(glob.glob(os.path.join(BASE_DIR, '**', 'index.html'), recursive=True))
    for lang in langs:
        files |= set(glob.glob(os.path.join(BASE_DIR, lang, '**', '*.html'), recursive=True))

    changed_files = changed_links = skipped = 0
    for path in sorted(files):
        if 'node_modules' in path:
            continue
        with open(path, encoding='utf-8') as f:
            html = f.read()
        if 'ltt-lang-item' not in html and 'ltt-mobile-lang-chip' not in html:
            continue
        hl = hreflang_map(html)
        if 'en' not in hl:
            skipped += 1  # prototypes/mockups without hreflang: leave alone
            continue
        own = page_lang(os.path.relpath(path, BASE_DIR), langs)
        n = 0

        def repl(m):
            nonlocal n
            new = fix_anchor(m.group(0), hl, own)
            if new != m.group(0):
                n += 1
            return new

        out = ANCHOR_RE.sub(repl, html)
        if out != html:
            changed_files += 1
            changed_links += n
            if not dry:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(out)

    print('%s %d links in %d files (%d pages without hreflang skipped)'
          % ('Would fix' if dry else 'Fixed', changed_links, changed_files, skipped))


if __name__ == '__main__':
    main()
