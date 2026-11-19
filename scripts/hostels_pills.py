# -*- coding: utf-8 -*-
"""Turn the 4 spec pills on each best-hostels card into dropdowns (BPA details.bpa-lang pattern).

    python3 scripts/hostels_pills.py en best-hostels-budapest.html

Copy comes from scripts/hostels_pills_<lang>.py (PILLS[n] = 4 x (emoji, lead, text, note)).
The pill labels already on the page are kept as they are, so translated pages keep their labels.
CSS and JS are copied from de/private-bootsfahrten-budapest/index.html, which still carries the inline pattern
(the English pages now load the shared kit listicle files). Not for best-hostels-budapest.html: its cards are
built from data/listicles/best-hostels-budapest.json.
Idempotent: a page whose pills are already dropdowns is rebuilt from scratch.
"""
import html, importlib, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
sys.path.insert(0, HERE)
lang, rel = sys.argv[1], sys.argv[2]
_M = importlib.import_module('hostels_pills_%s' % lang)
if hasattr(_M, 'T'):  # translation: 40 x (lead, text, note) in card order, emojis from EN
    from hostels_pills_en import PILLS as _EN
    assert len(_M.T) == 40, 'need 40 pills, got %d' % len(_M.T)
    PILLS = {n: [(_EN[n][k][0],) + tuple(_M.T[(n - 1) * 4 + k]) for k in range(4)] for n in range(1, 11)}
else:
    PILLS = _M.PILLS
PAGE = os.path.join(ROOT, rel)

ref = open(os.path.join(ROOT, 'de', 'private-bootsfahrten-budapest', 'index.html'), encoding='utf-8').read()
CSS = re.search(r'<style id="bpa-lang-css">.*?</style>', ref, re.S).group(0)
JS = re.search(r'<script id="bpa-lang-js">.*?</script>', ref, re.S).group(0)

s = open(PAGE, encoding='utf-8').read()

# undo a previous run: dropdown back to a plain pill
s = re.sub(r'<details class="bpa-lang"><summary class="bpa-sp">[^<]*<span class="bpa-lang-label">(.*?)</span>'
           r'<span class="bpa-lang-chev"[^>]*>▾</span></summary><div class="bpa-lang-pop">.*?</div></details>',
           r'<span class="bpa-sp">\1</span>', s, flags=re.S)

rows = list(re.finditer(r'<div class="bpa-specs-row">(.*?)</div>', s, re.S))
assert len(rows) == 10, 'expected 10 card spec rows, found %d' % len(rows)


def pill(label, p):
    emoji, lead, text, note = p
    return ('<details class="bpa-lang"><summary class="bpa-sp">%s <span class="bpa-lang-label">%s</span>'
            '<span class="bpa-lang-chev" aria-hidden="true">▾</span></summary>'
            '<div class="bpa-lang-pop"><strong>%s</strong> %s<span class="bpa-lang-note">%s</span></div></details>'
            ) % (emoji, label, lead, text, note)


out, last = [], 0
for n, m in enumerate(rows, 1):
    labels = re.findall(r'<span class="bpa-sp">(.*?)</span>', m.group(1))
    assert len(labels) == 4, 'card %d has %d pills' % (n, len(labels))
    body = m.group(1)
    for label, p in zip(labels, PILLS[n]):
        body = body.replace('<span class="bpa-sp">%s</span>' % label, pill(label, p), 1)
    out.append(s[last:m.start(1)] + body)
    last = m.end(1)
s = ''.join(out) + s[last:]

s = re.sub(r'<style id="bpa-lang-css">.*?</style>', '', s, flags=re.S)
s = re.sub(r'<script id="bpa-lang-js">.*?</script>', '', s, flags=re.S)
s = s.replace('</head>', CSS + '</head>', 1)
s = s.replace('</body>', JS + '</body>', 1)
open(PAGE, 'w', encoding='utf-8').write(s)
print('%s: %d pills -> dropdowns' % (rel, sum(len(v) for v in PILLS.values())))
