# -*- coding: utf-8 -*-
"""Translation-memory helper for the prosecco page port.

export: write the EN page's port segments (tags -> ⟦n⟧ placeholders) to
        scripts/prosecco_i18n/source.json  {id: text}
apply <lang>: read scripts/prosecco_i18n/<lang>.json {id: translated text},
        restore tags, check placeholders, and merge into the port cache
        data/i18n/port/unlimited-prosecco-cruises-budapest/<lang>.json
Then run: python3 scripts/port_page_i18n.py unlimited-prosecco-cruises-budapest.html --langs <lang> --dry-run
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import port_page_i18n as P  # noqa
from bs4 import BeautifulSoup

PAGE = "unlimited-prosecco-cruises-budapest.html"
CACHE = os.path.join(ROOT, "data", "i18n", "port", "unlimited-prosecco-cruises-budapest")
TAG = re.compile(r"<[^>]+>")


def strings():
    soup = BeautifulSoup(P.read(PAGE), "html.parser")
    out = []
    for kind, ref, src in P.collect(soup):
        if kind == "jsonld":
            P.jsonld_strings(src, out)
        elif kind == "pagecfg":
            P.cfg_strings(src, out)
        else:
            out.append(src)
    return list(dict.fromkeys(out))


def split(s):
    tags = []
    def r(m):
        tags.append(m.group(0)); return "⟦%d⟧" % (len(tags) - 1)
    return TAG.sub(r, s), tags


def export():
    src = {}
    for s in strings():
        src[P.key(s)] = split(s)[0]
    json.dump(src, open(os.path.join(HERE, "source.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    with open(os.path.join(HERE, "source.txt"), "w", encoding="utf-8") as fh:
        for i, v in enumerate(src.values(), 1):
            fh.write(f"{i}|{v.replace(chr(10), '⏎')}\n")
    print(len(src), "strings")


def load_lang(lang):
    """<lang>.txt lines 'N|text' (N = line in source.txt, '=' keeps the source, ⏎ = newline)."""
    src = list(json.load(open(os.path.join(HERE, "source.json"), encoding="utf-8")).items())
    out = {}
    for line in open(os.path.join(HERE, f"{lang}.txt"), encoding="utf-8"):
        line = line.rstrip("\n")
        if not line.strip():
            continue
        n, _, t = line.partition("|")
        k, v = src[int(n) - 1]
        out[k] = (v if t == "=" else t).replace("⏎", "\n")
    return out


def apply(lang):
    tr = load_lang(lang)
    os.makedirs(CACHE, exist_ok=True)
    cp = os.path.join(CACHE, f"{lang}.json")
    cache = json.load(open(cp, encoding="utf-8")) if os.path.exists(cp) else {}
    # reuse translation memory from other pages for identical source strings
    tm = {}
    for d in os.listdir(os.path.join(ROOT, "data", "i18n", "port")):
        f = os.path.join(ROOT, "data", "i18n", "port", d, f"{lang}.json")
        if os.path.exists(f):
            tm.update(json.load(open(f, encoding="utf-8")))
    errs, missing = [], []
    for s in strings():
        k = P.key(s)
        if k in tr:
            text, tags = split(s)
            t = tr[k]
            used = [int(x) for x in re.findall(r"⟦(\d+)⟧", t)]
            if sorted(used) != list(range(len(tags))):
                errs.append((k, text[:80], t[:80])); continue
            if "—" in t:
                errs.append((k, "EM DASH", t[:80])); continue
            cache[k] = re.sub(r"⟦(\d+)⟧", lambda m: tags[int(m.group(1))], t)
        elif k in tm:
            cache[k] = tm[k]
        elif k not in cache:
            missing.append(k)
    json.dump(cache, open(cp, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(lang, "cached", len(cache), "errors", len(errs), "missing", len(missing))
    for e in errs[:20]:
        print("  ERR", e)
    for m in missing[:20]:
        print("  MISSING", m)
    return not errs and not missing


if __name__ == "__main__":
    if sys.argv[1] == "export":
        export()
    else:
        ok = all(apply(l) for l in sys.argv[2:])
        sys.exit(0 if ok else 1)
