# -*- coding: utf-8 -*-
"""One-off: EN went from '2 sites' to '3 sites' (separate Tripadvisor badge) and
'Viator + Tripadvisor' to 'Viator'. Derive each language's translation of the new
strings from its translation of the old string, changing only the site-count digit
outside tags. Usage: patch_sites.py <old_en.html> <lang>..."""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "scripts")); sys.path.insert(0, HERE)
import port_page_i18n as P, tm
from bs4 import BeautifulSoup

def strings_of(html):
    soup = BeautifulSoup(html, "html.parser"); out = []
    for kind, ref, src in P.collect(soup):
        if kind == "jsonld": P.jsonld_strings(src, out)
        elif kind == "pagecfg": P.cfg_strings(src, out)
        else: out.append(src)
    return list(dict.fromkeys(out))

def bump(t):
    parts = re.split(r"(<[^>]+>)", t); n = 0
    for i, p in enumerate(parts):
        if p.startswith("<"): continue
        p2, k = re.subn(r"(?<![\d.,])2(?![\d.,])", "3", p); n += k; parts[i] = p2
    assert n == 1, (n, t)
    return "".join(parts)

old = set(strings_of(open(sys.argv[1], encoding="utf-8").read()))
new = tm.strings()
for lang in sys.argv[2:]:
    cp = os.path.join(tm.CACHE, f"{lang}.json"); cache = json.load(open(cp, encoding="utf-8"))
    added = 0
    for s in new:
        if P.key(s) in cache: continue
        if re.fullmatch(r"\s*(Viator|Tripadvisor)\s*", s):
            cache[P.key(s)] = s; added += 1; continue
        o = s.replace("3 sites", "2 sites").replace("Average of 3 booking", "Average of 2 booking")
        assert o != s and o in old and P.key(o) in cache, ("no source for", lang, s[:120])
        cache[P.key(s)] = bump(cache[P.key(o)]); added += 1
    json.dump(cache, open(cp, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(lang, "added", added)
