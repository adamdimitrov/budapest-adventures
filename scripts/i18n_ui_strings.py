"""Second i18n pass: short English UI labels (badges, buttons, nav items, buy-box text)
and the Budapest Card calculator's JS strings.

  extract: python3 scripts/i18n_ui_strings.py extract <outdir>
           -> <outdir>/<lang>.ui.json  {"English text": ""}
  apply:   python3 scripts/i18n_ui_strings.py apply <outdir>   (reads <lang>.ui.out.json)

Only text nodes that are the ENTIRE content of their element are touched
(`<span class="x">Free 24h Cancellation</span>`), never sentence fragments, so a
dictionary replacement is safe. Applied to every page of that language.
"""
import glob
import html
import json
import os
import re
import sys

LANGS = 'bg cs de el es fr he hr it ja ko nl pl pt ro ru sk sr tr uk'.split()
CARD = 'budapest-card-is-it-worth-it'
EN = set('the and of to in for with is are this that you your on at by from or as be it an was we our have has will '
         'can best check availability book now read more price prices cruise cruises tickets ticket view details see '
         'show hide top pick tested personally free cancellation instant confirmation duration departure dock reviews '
         'review rating rated table contents overview summary pros cons verdict included includes not drinks food '
         'music live why choose how what where when who itinerary location map tips faq frequently asked questions '
         'guaranteed official dates dinner night river boat boats private tours tour hostels walking baths thermal '
         'airport city guide tested ideal perfect great complete extended public transport walking trip stay stays '
         'quick weekend'.split())
# element whose whole content is one text node
WHOLE_RE = re.compile(r'(<(a|span|button|div|p|li|strong|b|em|label|summary|th|td|h[1-6]|option)\b[^>]*>)([^<>]{2,90})(</\2>)')
KEEP = {'IT', 'EN', 'HU', 'DE', 'FR', 'ES'}


def english(t):
    w = re.findall(r"[A-Za-z']+", t)
    allw = re.findall(r'\w+', t)
    if not w or t in KEEP or not allw:
        return False
    return sum(1 for x in w if x.lower() in EN) >= max(1, len(allw) * 0.5)


def strip_code(s):
    return re.sub(r'<(script|style)\b.*?</\1>', lambda m: ' ' * len(m.group(0)), s, flags=re.S)


def card_js_strings(s):
    out = []
    for m in re.finditer(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', s, re.S):
        body = m.group(1)
        if 'miniBUD' not in body:
            continue
        for q in re.finditer(r"""(['"])((?:(?!\1)[^\\\n]){6,90})\1""", body):
            t = q.group(2)
            if re.search(r'[a-z]{3,} [a-z]{2,}', t) and not re.search(r'[{}<>=;]|https?:|\.(js|css|webp|png)|^[\w-]+$', t):
                out.append(t)
    return out


def pages(lang):
    return sorted(glob.glob(f'{lang}/*/index.html') + glob.glob(f'{lang}/*/*/index.html') + [f'{lang}/index.html'])


def extract(outdir):
    os.makedirs(outdir, exist_ok=True)
    for lang in LANGS:
        found = {}
        for f in pages(lang):
            if not os.path.exists(f):
                continue
            s = open(f, encoding='utf-8').read()
            for m in WHOLE_RE.finditer(strip_code(s)):
                t = html.unescape(m.group(3)).strip()
                if english(t):
                    found[t] = found.get(t, 0) + 1
            if CARD in f:
                for t in card_js_strings(s):
                    found['JS::' + t] = 1
        items = dict(sorted(found.items(), key=lambda kv: -kv[1]))
        json.dump({k: '' for k in items}, open(f'{outdir}/{lang}.ui.json', 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
        print(lang, len(items), 'strings')


def apply(outdir):
    for lang in LANGS:
        p = f'{outdir}/{lang}.ui.out.json'
        if not os.path.exists(p):
            print('missing', p)
            continue
        tr = {k: v for k, v in json.load(open(p, encoding='utf-8')).items() if v and v != k}
        html_map = {k: v for k, v in tr.items() if not k.startswith('JS::')}
        js_map = {k[4:]: v for k, v in tr.items() if k.startswith('JS::')}
        changed = 0
        for f in pages(lang):
            if not os.path.exists(f):
                continue
            s = open(f, encoding='utf-8').read()
            clean = strip_code(s)
            parts, last = [], 0
            for m in WHOLE_RE.finditer(clean):
                t = html.unescape(m.group(3)).strip()
                if t in html_map:
                    raw = m.group(3)
                    lead, trail = raw[:len(raw) - len(raw.lstrip())], raw[len(raw.rstrip()):]
                    parts.append(s[last:m.start(3)] + lead + html.escape(html_map[t], quote=False) + trail)
                    last = m.end(3)
            s2 = ''.join(parts) + s[last:]
            if CARD in f and js_map:
                def js_sub(m):
                    body = m.group(2)
                    for en_s, loc in js_map.items():
                        for q in ("'", '"'):
                            esc = loc.replace('\\', '\\\\').replace(q, '\\' + q)
                            body = body.replace(q + en_s + q, q + esc + q)
                    return m.group(1) + body + m.group(3)
                s2 = re.sub(r'(<script(?![^>]*\bsrc=)[^>]*>)(.*?)(</script>)',
                            lambda m: js_sub(m) if 'miniBUD' in m.group(2) else m.group(0), s2, flags=re.S)
            if s2 != s:
                open(f, 'w', encoding='utf-8').write(s2)
                changed += 1
        print(lang, len(tr), 'strings ->', changed, 'files')


if __name__ == '__main__':
    {'extract': extract, 'apply': apply}[sys.argv[1]](sys.argv[2])
