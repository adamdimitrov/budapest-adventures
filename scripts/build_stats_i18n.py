#!/usr/bin/env python3
"""Build the tourism statistics page in every language from the EN master.

The EN page (budapest-tourism-statistics.html) is the source of truth. HU is
written by hand (hu/budapest-turizmus-statisztika/index.html). The other 20
languages are generated from EN plus a translation file per language:

    python3 scripts/build_stats_i18n.py extract   # EN master -> data/i18n/stats/en.json
    python3 scripts/build_stats_i18n.py check     # which ids each language is missing
    python3 scripts/build_stats_i18n.py build     # write the 20 localized pages
    python3 scripts/build_stats_i18n.py masters   # full 22-language switcher on EN and HU
    python3 scripts/build_stats_embeds.py         # then rebuild the chart embeds

After changing the EN page: run extract, translate the new or changed ids in
data/i18n/stats/<lang>.json (check lists them), then build and embeds.

What build does per language:
  * replaces every text run (text plus inline tags) and translatable attribute
    of the EN page with the translation of the same segment id
  * points internal links at that language's version of each page (from the
    hreflang alternates of the EN pages), home at /<lang>
  * sets <html lang>, dir="rtl" for Hebrew, canonical, og:url, og:locale,
    JSON-LD inLanguage / mainEntityOfPage
  * puts the full 22-language switcher in the menu with this language current
"""
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.budapestadventures.com"
EN_FILE = "budapest-tourism-statistics.html"
DATA = os.path.join(ROOT, "data", "i18n", "stats")

LANGS = ["de", "fr", "it", "es", "ro", "pl", "nl", "cs", "sk", "pt", "ru",
         "hr", "sr", "bg", "el", "tr", "uk", "he", "ja", "ko"]
OG_LOCALE = {"en": "en_US", "hu": "hu_HU", "de": "de_DE", "fr": "fr_FR", "it": "it_IT", "es": "es_ES",
             "ro": "ro_RO", "pl": "pl_PL", "nl": "nl_NL", "cs": "cs_CZ", "sk": "sk_SK", "pt": "pt_PT",
             "ru": "ru_RU", "hr": "hr_HR", "sr": "sr_RS", "bg": "bg_BG", "el": "el_GR", "tr": "tr_TR",
             "uk": "uk_UA", "he": "he_IL", "ja": "ja_JP", "ko": "ko_KR"}

# tags that do not break a text run (unless they carry a bpa- chart class)
INLINE = {"a", "strong", "b", "em", "i", "span", "br", "sup", "sub", "code", "small", "abbr", "u", "mark"}
SKIP_CONTENT = {"script", "style", "textarea", "svg", "noscript"}
ATTRS = ("title", "alt", "aria-label", "placeholder")
META_NAMES = ("description", "og:title", "og:description", "twitter:title", "twitter:description")

TOKEN = re.compile(r"<!--.*?-->|<[^>]+>|[^<]+", re.S)
LETTER = re.compile(r"[^\W\d_]", re.U)


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def write(rel, text):
    full = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(text)


def strip_embeds(s):
    s = re.sub(r"<!--bpa-embed-->.*?<!--/bpa-embed-->", "", s, flags=re.S)
    s = re.sub(r'<style id="bpa-embed-css">.*?</style>', "", s, flags=re.S)
    s = re.sub(r'<script id="bpa-embed-js">.*?</script>', "", s, flags=re.S)
    return s


def tag_name(tok):
    m = re.match(r"</?\s*([a-zA-Z0-9]+)", tok)
    return m.group(1).lower() if m else None


def is_inline(tok):
    """Inline formatting that stays inside a sentence: <strong>, <br/>, prose <a href>, plain <span>.
    Any tag with a class or style (menu links, chart parts, badges) splits the text into separate runs."""
    name = tag_name(tok)
    if name not in INLINE:
        return False
    if tok.startswith("</"):
        return True
    if re.search(r'\s(class|style|id)=', tok):
        return False
    return True


def text_runs(s):
    """Yield (start, end) of each translatable run in the body."""
    body = s.find("<body")
    pos, skip, run = body, None, None
    for m in TOKEN.finditer(s, body):
        tok = m.group(0)
        if skip:
            if tok.lower().startswith("</" + skip):
                skip = None
            continue
        if tok.startswith("<!--"):
            continue
        if tok.startswith("<"):
            name = tag_name(tok)
            if name in SKIP_CONTENT and not tok.startswith("</") and not tok.endswith("/>"):
                if run:
                    yield run
                run, skip = None, name
                continue
            if is_inline(tok):
                if run:
                    run = (run[0], m.end())
                else:
                    run = (m.start(), m.end())
                continue
            if run:
                yield run
            run = None
        else:
            if run:
                run = (run[0], m.end())
            elif tok.strip():
                run = (m.start(), m.end())
    if run:
        yield run


def trim_run(s, a, b):
    """Shrink a run to its translatable core: no outer whitespace, no stray closing tags at either end."""
    while True:
        seg = s[a:b]
        lead = len(seg) - len(seg.lstrip())
        trail = len(seg) - len(seg.rstrip())
        a, b = a + lead, b - trail
        seg = s[a:b]
        m = re.match(r"</[a-zA-Z0-9]+>", seg)
        if m:
            a += m.end()
            continue
        m = re.search(r"</([a-zA-Z0-9]+)>$", seg)
        if m and len(re.findall(r"<%s\b" % m.group(1), seg)) < len(re.findall(r"</%s>" % m.group(1), seg)):
            b -= len(m.group(0))
            continue
        return a, b


SWITCHER_PATS = (
    re.compile(r'<div[^>]*id="lttLangDropdown"[^>]*>.*?</div>\s*</div>', re.S),
    re.compile(r'<div class="ltt-mobile-lang-box">.*?</div>\s*</div>', re.S),
    re.compile(r'<span class="ltt-lang-code" id="lttActiveLangLabel">[^<]*</span>'),
)
NUMERIC = re.compile(r"^[+\-\u2212]?\d[\d,]*(?:\.\d+)?%?$")
MILLIONS = re.compile(r"^(\d+(?:\.\d+)?)M$")


def excluded(s):
    spans = []
    for pat in SWITCHER_PATS:
        for m in pat.finditer(s):
            spans.append((m.start(), m.end()))
    return spans


def segments(s):
    """Return list of (start, end, kind, text) for body runs, attributes and head fields."""
    out = []
    skip = excluded(s)
    inside = lambda a: any(x <= a < y for x, y in skip)
    for a, b in text_runs(s):
        a, b = trim_run(s, a, b)
        if inside(a):
            continue
        txt = s[a:b]
        plain = html.unescape(re.sub(r"<[^>]+>", "", txt)).strip()
        w = re.match(r"^<(strong|span|b|em)>([^<]*)</\1>$", txt)
        if w:  # a bare wrapper: translate only the text inside it
            a += len(w.group(1)) + 2
            b -= len(w.group(1)) + 3
            txt = s[a:b]
        if NUMERIC.match(plain) or MILLIONS.match(plain):
            out.append((a, b, "num", txt))
            continue
        if not LETTER.search(plain):
            continue
        # an unbalanced run (e.g. starts with </a>) is cut to its text part
        out.append((a, b, "run", txt))
    body = s.find("<body")
    for m in re.finditer(r"<[a-zA-Z][^>]*>", s[body:]):
        tag = m.group(0)
        for attr in ATTRS:
            for am in re.finditer(r'\s%s="([^"]*)"' % re.escape(attr), tag):
                val = am.group(1)
                if LETTER.search(html.unescape(val)) and not inside(body + m.start()):
                    st = body + m.start() + am.start(1)
                    out.append((st, st + len(val), "attr", val))
    head = s[:body]
    t = re.search(r"<title>(.*?)</title>", head, re.S)
    out.append((t.start(1), t.end(1), "title", t.group(1)))
    for nm in META_NAMES:
        mm = re.search(r'<meta content="([^"]*)" (?:name|property)="%s"/>' % re.escape(nm), head)
        if mm:
            out.append((mm.start(1), mm.end(1), "meta", mm.group(1)))
    out.sort()
    return out


def load_en():
    return strip_embeds(read(EN_FILE))


def extract():
    s = load_en()
    segs = segments(s)
    ids, data = {}, {}
    for a, b, kind, txt in segs:
        if kind == "num" or txt in KEEP or pattern_match(txt)[0]:
            continue
        if txt not in ids:
            sid = "s%03d" % (len(ids) + 1)
            ids[txt] = sid
            data[sid] = txt
    # JSON-LD
    ld = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S).group(1))
    data.update({k: "" for k in TEMPLATE_KEYS})
    data["ld_headline"] = ld["headline"]
    data["ld_description"] = ld["description"]
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, "en.json"), "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
    print(len(segs), "segments,", len(data), "unique ->", os.path.relpath(os.path.join(DATA, "en.json"), ROOT))


def en_data():
    with open(os.path.join(DATA, "en.json"), encoding="utf-8") as fh:
        return json.load(fh)


def lang_data(lg):
    p = os.path.join(DATA, lg + ".json")
    if not os.path.exists(p):
        return {}
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def check():
    en = en_data()
    bad = 0
    for lg in LANGS:
        tr = lang_data(lg)
        miss = [k for k in en if k not in tr]
        extra = [k for k in tr if k not in en]
        tags = [k for k in en if k in tr and sorted(re.findall(r"<(/?[a-z]+)", en[k])) != sorted(re.findall(r"<(/?[a-z]+)", tr[k]))]
        dash = [k for k, v in tr.items() if "—" in v]
        if miss or extra or tags or dash:
            bad += 1
        print(f"{lg}: {len(tr)}/{len(en)}  missing={len(miss)} extra={len(extra)} tag-mismatch={tags[:8]} emdash={dash[:8]}")
    return bad


# ---------- numbers and untranslated strings ----------

# EN strings that stay as they are in every language (brand names, hidden template text)
KEEP = {
    "BUDAPEST ADVENTURES", "This is also a heading<br/>", "This is a heading<br/>",
    "BUDAPEST ADVENTURES Homepage", "BUDAPEST ADVENTURES Logo", "Budapest Adventures Logo", "Adam Dimitrov",
    '<span class="ltt-brand-text">BUDAPEST ADVENTURES</span>\n</a>', "<span>BUDAPEST ADVENTURES</span>\n</a>",
    '<a class="tocitem" href="#top">This is also a heading<br/></a><a class="tocitem active" href="#top">This is a heading<br/></a>',
}

NBSP, NNBSP = "\u00a0", "\u202f"
# language: (thousands separator, decimal separator, millions template)
NUM = {
    "de": (".", ",", "{} Mio."), "fr": (NNBSP, ",", "{}" + NBSP + "M"), "it": (".", ",", "{} Mln"),
    "es": (".", ",", "{}" + NBSP + "M"), "ro": (".", ",", "{} mil."), "pl": (NBSP, ",", "{} mln"),
    "nl": (".", ",", "{} mln"), "cs": (NBSP, ",", "{} mil."), "sk": (NBSP, ",", "{} mil."),
    "pt": (".", ",", "{}" + NBSP + "M"), "ru": (NBSP, ",", "{} млн"), "hr": (".", ",", "{} mil."),
    "sr": (".", ",", "{} мил."), "bg": (NBSP, ",", "{} млн"), "el": (".", ",", "{} εκ."),
    "tr": (".", ",", "{} Mn"), "uk": (NBSP, ",", "{} млн"), "he": (",", ".", "{}M"),
    "ja": (",", ".", None), "ko": (",", ".", None),
}


def fmt_number(plain, lg):
    th, dec, mil = NUM[lg]
    m = MILLIONS.match(plain)
    if m:
        x = m.group(1)
        if mil is None:  # ja / ko count in units of 10,000
            v = round(float(x) * 100)
            return f"{v:,}" + ("万" if lg == "ja" else "만")
        return mil.format(x.replace(".", dec))
    out = plain.replace(",", "\x00").replace(".", dec).replace("\x00", th)
    return out


def localize_num(txt, lg):
    plain_raw = re.sub(r"<[^>]+>", "", txt)
    plain = html.unescape(plain_raw).strip()
    return txt.replace(plain_raw.strip(), fmt_number(plain, lg), 1)


# Chart tooltips follow a few fixed patterns. Each language file gives one template per
# pattern ({y} year, {x} number, {name} month or country, translated via its own segment).
PATTERNS = [
    (re.compile(r"^(?P<y>\d{4}) international: (?P<x>[\d.]+) million$"), "t_intl_m"),
    (re.compile(r"^(?P<y>\d{4}) domestic: (?P<x>[\d.]+) million$"), "t_dom_m"),
    (re.compile(r"^(?P<y>\d{4}) international: (?P<x>[\d.]+) nights$"), "t_intl_n"),
    (re.compile(r"^(?P<y>\d{4}) domestic: (?P<x>[\d.]+) nights$"), "t_dom_n"),
    (re.compile(r"^(?P<y>\d{4}) spending: (?P<x>[\d,]+) billion forints$"), "t_spend"),
    (re.compile(r"^(?P<name>[A-Z][A-Za-z ]+) nights: (?P<x>[\d.]+) million$"), "t_named_m"),
]
TEMPLATE_KEYS = [k for _, k in PATTERNS]


def pattern_match(txt):
    for pat, key in PATTERNS:
        m = pat.match(txt)
        if m:
            return m, key
    return None, None


def from_template(txt, lg, tr, en_ids):
    m, key = pattern_match(txt)
    g = m.groupdict()
    out = tr[key]
    if "y" in g:
        out = out.replace("{y}", g["y"])
    if "name" in g:
        out = out.replace("{name}", html.unescape(tr[en_ids[g["name"]]]))
    th, dec, _ = NUM[lg]
    return out.replace("{x}", g["x"].replace(",", "\x00").replace(".", dec).replace("\x00", th))


# ---------- links ----------

def page_alternates():
    """EN path -> {lang: localized path}, from hreflang on every EN page in the sitemap."""
    sm = read("sitemap.xml")
    rw = {r["source"]: r["destination"] for r in json.loads(read("vercel.json")).get("rewrites", []) if ":" not in r["source"]}
    paths = re.findall(r"<loc>https://www\.budapestadventures\.com([^<]*)</loc>", sm)
    alt = {}
    for p in paths:
        p0 = p.rstrip("/") or "/"
        for cand in (p0, rw.get(p0)):
            if not cand:
                continue
            for f in (["index.html"] if cand == "/" else [cand.lstrip("/") + ".html", cand.lstrip("/") + "/index.html"]):
                fp = os.path.join(ROOT, f)
                if os.path.exists(fp):
                    with open(fp, encoding="utf-8") as fh:
                        s = fh.read()
                    hl = {m.group(2): (m.group(1).replace(SITE, "") or "/")
                          for m in re.finditer(r'<link href="(https://www\.budapestadventures\.com[^"]*)" hreflang="([a-z-]+)" rel="alternate"/>', s)}
                    if hl.get("en"):
                        alt.setdefault(hl["en"], hl)
                    break
            else:
                continue
            break
    return alt


def localize_href(href, lg, alt):
    if not href.startswith("/") or href.startswith("//"):
        return href
    path, frag = (href.split("#", 1) + [""])[:2]
    path = path.rstrip("/") or "/"
    if path == "/":
        new = "/" + lg
    elif path in alt and lg in alt[path]:
        new = alt[path][lg]
    else:
        return href
    return new + ("#" + frag if frag else "")


# ---------- language switcher ----------

def full_switcher(lg, page_alt):
    """Return (desktop dropdown, mobile box) with all 22 languages, localized, from the language's stats page."""
    tpl = read(stats_file(page_alt[lg]))
    drop = re.search(r'<div[^>]*id="lttLangDropdown"[^>]*>.*?</div>\s*</div>', tpl, re.S).group(0)
    box = re.search(r'<div class="ltt-mobile-lang-box">.*?</div>\s*</div>', tpl, re.S).group(0)
    return drop, box


def build():
    en = en_data()
    s = load_en()
    segs = segments(s)
    alt = page_alternates()
    stats_alt = alt["/budapest-tourism-statistics"]
    for lg in LANGS:
        tr = lang_data(lg)
        miss = [k for k in en if k not in tr]
        if miss:
            print(f"skip {lg}: {len(miss)} untranslated ids")
            continue
        rev = {v: k for k, v in en.items() if not k.startswith("ld_")}
        out, last = [], 0
        for a, b, kind, txt in segs:
            out.append(s[last:a])
            if kind == "num":
                new = localize_num(txt, lg)
            elif txt in KEEP:
                new = txt
            elif pattern_match(txt)[0]:
                new = from_template(txt, lg, tr, rev)
            else:
                new = tr[rev[txt]]
            if kind in ("attr", "meta"):
                new = new.replace('"', "&quot;")
            out.append(new)
            last = b
        out.append(s[last:])
        p = "".join(out)

        url = stats_alt[lg]
        # links
        p = re.sub(r'(<a\b[^>]*\shref=")([^"]*)(")', lambda m: m.group(1) + localize_href(m.group(2), lg, alt) + m.group(3), p)
        # head
        p = re.sub(r'<html([^>]*)\blang="en"', lambda m: f'<html{m.group(1)}lang="{lg}"' + (' dir="rtl"' if lg == "he" else ""), p, count=1)
        p = p.replace(f'<link href="{SITE}/budapest-tourism-statistics" rel="canonical"/>', f'<link href="{SITE}{url}" rel="canonical"/>')
        p = re.sub(r'(<meta content=")[^"]*(" property="og:url"/>)', lambda m: m.group(1) + SITE + url + m.group(2), p)
        p = re.sub(r'(<meta content=")[^"]*(" property="og:locale"/>)', lambda m: m.group(1) + OG_LOCALE[lg] + m.group(2), p)
        # JSON-LD
        def fix_ld(m):
            ld = json.loads(m.group(1))
            ld["headline"] = tr["ld_headline"]
            ld["description"] = tr["ld_description"]
            ld["inLanguage"] = lg
            ld["mainEntityOfPage"] = SITE + url
            return '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False, separators=(",", ":")) + "</script>"
        p = re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix_ld, p, count=1, flags=re.S)
        # switcher: full 22 languages, this one current
        drop, box = full_switcher(lg, stats_alt)
        p = re.sub(r'<div[^>]*id="lttLangDropdown"[^>]*>.*?</div>\s*</div>', lambda m: drop, p, count=1, flags=re.S)
        p = re.sub(r'<div class="ltt-mobile-lang-box">.*?</div>\s*</div>', lambda m: box, p, count=1, flags=re.S)
        p = set_current_lang(p, lg)
        p = re.sub(r'(<span class="ltt-lang-code" id="lttActiveLangLabel">)[^<]*(</span>)', lambda m: m.group(1) + lg.upper() + m.group(2), p)
        target = stats_file(url)
        write(target, p)
        print("built", target)


MASTER_FILES = {"en": EN_FILE, "hu": "hu/budapest-turizmus-statisztika/index.html"}
MASTER_SWITCHER_TEXT = {
    "en": ("Select Language", "● 22 AVAILABLE", "Language"),
    "hu": ("Nyelvválasztás", "● 22 ELÉRHETŐ", "Nyelv"),
}


def masters():
    """Give the hand-written EN and HU pages the full 22-language switcher (links to every stats page)."""
    alt = page_alternates()["/budapest-tourism-statistics"]
    drop, box = full_switcher("de", alt)
    for lg, f in MASTER_FILES.items():
        title, count, mobile = MASTER_SWITCHER_TEXT[lg]
        d = re.sub(r'(<div class="ltt-lang-dropdown-header">\s*<span>)[^<]*(</span>\s*<span[^>]*>)[^<]*(</span>)',
                   lambda m: m.group(1) + title + m.group(2) + count + m.group(3), drop, count=1)
        b = re.sub(r'(<div class="ltt-mobile-lang-title">.*?<span>)[^<]*(</span>)',
                   lambda m: m.group(1) + mobile + m.group(2), box, count=1, flags=re.S)
        p = read(f)
        p = re.sub(r'<div[^>]*id="lttLangDropdown"[^>]*>.*?</div>\s*</div>', lambda m: d, p, count=1, flags=re.S)
        p = re.sub(r'<div class="ltt-mobile-lang-box">.*?</div>\s*</div>', lambda m: b, p, count=1, flags=re.S)
        p = set_current_lang(p, lg)
        write(f, p)
        print("full switcher on", f)


def set_current_lang(p, lg):
    p = re.sub(r'(<a class="ltt-lang-item) current(")', r"\1\2", p)
    p = re.sub(r'(<a class="ltt-lang-item)(" data-lang="%s")' % lg, r"\1 current\2", p)
    p = re.sub(r'(<a class="ltt-mobile-lang-chip) current(")', r"\1\2", p)
    p = re.sub(r'(<a class="ltt-mobile-lang-chip)(" data-m-lang="%s")' % lg, r"\1 current\2", p)
    return p


def stats_file(url):
    rw = {r["source"]: r["destination"] for r in json.loads(read("vercel.json")).get("rewrites", []) if ":" not in r["source"]}
    for cand in (url, rw.get(url)):
        if cand:
            for f in (cand.lstrip("/") + "/index.html", cand.lstrip("/") + ".html"):
                if os.path.exists(os.path.join(ROOT, f)):
                    return f
    return url.lstrip("/") + "/index.html"


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd == "extract":
        extract()
    elif cmd == "check":
        sys.exit(1 if check() else 0)
    elif cmd == "build":
        build()
    elif cmd == "masters":
        masters()
    else:
        sys.exit(__doc__)
