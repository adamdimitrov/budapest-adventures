"""Move localized pages from English slugs to native ASCII slugs.

Reads data/localized_slugs.json ({english_slug: {lang: new_slug}}) and the current
localized URL of each page from sitemap.xml, then:
  1. git-mv's each page folder to its new slug,
  2. rewrites every reference to the old URL across the site (HTML, sitemap, txt, json),
  3. adds permanent redirects old -> new to vercel.json (and repoints existing
     redirects whose destination was an old URL, so there are no chains).

usage: python3 scripts/migrate_localized_slugs.py [--dry-run]
"""
import json
import os
import re
import subprocess
import sys
from urllib.parse import quote, unquote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
DRY = '--dry-run' in sys.argv
BASE = 'https://www.budapestadventures.com'
NEW = json.load(open('data/localized_slugs.json', encoding='utf-8'))


def current_urls():
    sm = open('sitemap.xml', encoding='utf-8').read()
    out = {}
    for u in re.findall(r'<url>(.*?)</url>', sm, re.S):
        loc = unquote(re.search(r'<loc>([^<]+)</loc>', u).group(1)).replace(BASE, '').strip('/')
        if loc in NEW:
            for lang, href in re.findall(r'hreflang="([^"]+)" href="([^"]+)"', u):
                if lang in NEW[loc]:
                    out[(loc, lang)] = unquote(href).replace(BASE, '')
    return out


def main():
    cur = current_urls()
    moves = {}  # old path -> new path
    for (eng, lang), old in cur.items():
        new = f'/{lang}/{NEW[eng][lang]}'
        moves[old] = new
        eng_path = f'/{lang}/{eng}'
        if eng_path != old and os.path.exists(eng_path.strip('/') + '/index.html'):
            moves[eng_path] = new  # stale English-slug duplicate: redirect it too
    print(len(moves), 'old paths')

    # 1. move folders
    for (eng, lang), old in cur.items():
        src, dst = old.strip('/'), f'{lang}/{NEW[eng][lang]}'
        assert os.path.exists(src + '/index.html'), src
        assert not os.path.exists(dst), dst
        if not DRY:
            subprocess.run(['git', 'mv', src, dst], check=True)

    # 2. rewrite references (longest paths first so prefixes don't clash)
    olds = sorted(moves, key=len, reverse=True)
    variants = []  # (needle, regex, replacement): needle is a cheap substring pre-check
    for old in olds:
        forms = {old, quote(old, safe='/')}
        for f in forms:
            needle = f
            # review sub-pages don't exist (they redirect to the parent): link the new parent directly
            variants.append((needle, re.compile(
                r'(?<=["\'(=\s>])((?:' + re.escape(BASE) + r')?)' + re.escape(f) + r'/[a-z0-9-]+-review(?=["\'#?)\s<,])'),
                moves[old]))
            variants.append((needle, re.compile(
                r'(?<=["\'(=\s>])((?:' + re.escape(BASE) + r')?)' + re.escape(f) + r'(?=["\'#?)\s<,]|/?["\'<])'),
                moves[old]))
    files = subprocess.run(['git', '-c', 'core.quotepath=off', 'ls-files', '*.html', '*.xml', '*.txt', '*.json', '*.md'],
                           capture_output=True, text=True, check=True).stdout.split('\n')
    files = [f for f in files if f and os.path.exists(f) and not f.startswith(('.agents/', 'node_modules/'))
             and f not in ('vercel.json', 'data/localized_slugs.json')]
    changed = 0
    for f in files:
        try:
            s = open(f, encoding='utf-8').read()
        except UnicodeDecodeError:
            continue
        s2 = s
        for needle, rx, new in variants:
            if needle in s2:
                s2 = rx.sub(lambda m, new=new: m.group(1) + new, s2)
        if s2 != s:
            changed += 1
            if not DRY:
                open(f, 'w', encoding='utf-8').write(s2)
    print(changed, 'files with rewritten references')

    # 3. redirects
    v = json.load(open('vercel.json', encoding='utf-8'))
    reds = v.setdefault('redirects', [])
    repointed = 0
    for r in reds:
        d = unquote(r.get('destination', ''))
        if d in moves:
            r['destination'] = moves[d]
            repointed += 1
    new_rules = [{'source': old, 'destination': new, 'permanent': True} for old, new in sorted(moves.items())]
    existing = {r['source'] for r in reds}
    new_rules = [r for r in new_rules if r['source'] not in existing]
    v['redirects'] = new_rules + reds  # first match wins: specific moves first
    print(len(new_rules), 'redirects added,', repointed, 'existing redirects repointed')
    if not DRY:
        open('vercel.json', 'w', encoding='utf-8').write(json.dumps(v, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
