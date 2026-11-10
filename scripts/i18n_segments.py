"""Extract English text blocks from localized pages for translation, and apply them back.

  extract: python3 scripts/i18n_segments.py extract <outdir> <page> [<page>...]
           -> <outdir>/<lang>.json  [{"id": "<file>#<start>", "html": "<inner html>"}...]
  apply:   python3 scripts/i18n_segments.py apply <dir_with_<lang>.out.json>

Segments are the innermost block elements (p, li, h2-h6, blockquote, td, th, summary,
figcaption, label, button) whose text is still English. Inner HTML is kept verbatim so
links/bold survive; ids carry the byte offset so apply can verify nothing moved.
"""
import glob
import json
import os
import re
import sys

LANGS = 'bg cs de el es fr he hr it ja ko nl pl pt ro ru sk sr tr uk'.split()
TAGS = 'p|li|h2|h3|h4|h5|h6|blockquote|td|th|summary|figcaption|label|button'
BLOCK_RE = re.compile(r'<(%s)\b[^>]*>(.*?)</\1>' % TAGS, re.S)
EN = set('the and of to in for with is are this that you your on at by from or as be it an was we our have has '
         'will can if not but they their there more most all also one very just about into than when which what '
         'how get best'.split())


def text_of(h):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', h)).strip()


def is_english(t):
    words = re.findall(r'\w+', t)
    if len(words) < 3:
        return False
    hits = sum(1 for w in re.findall(r"[A-Za-z']+", t) if w.lower() in EN)
    return hits / len(words) >= 0.15


def strip_code(s):
    """Blank out script/style bodies (same length) so offsets stay valid."""
    return re.sub(r'<(script|style)\b.*?</\1>', lambda m: ' ' * len(m.group(0)), s, flags=re.S)


def segments(s):
    clean = strip_code(s)
    cands = [(m.start(2), m.end(2), m.group(2)) for m in BLOCK_RE.finditer(clean)]
    # BLOCK_RE is non-nesting per tag; also catch inner blocks of other tags inside a match
    inner = []
    for a, b, h in cands:
        for m in BLOCK_RE.finditer(h):
            inner.append((a + m.start(2), a + m.end(2), m.group(2)))
    allc = sorted(set(cands + inner))
    out = []
    for a, b, h in allc:
        if any(a <= a2 and b2 <= b and (a2, b2) != (a, b) for a2, b2, _ in allc):
            continue  # keep innermost only
        if is_english(text_of(h)):
            out.append((a, b, s[a:b]))
    return out


INLINE_OK = re.compile(r'</?(?:a|strong|b|em|i|span|br|small|sup|sub|img|u|mark|code)\b[^>]*>', re.I)
ANY_RE = re.compile(r'<(div|span|a|p|li|h[2-6]|td|th|summary|button|label|figcaption|blockquote|strong|em|b)\b[^>]*>', re.I)
# brand names that earlier machine translation rendered in local script / translated
MISBRAND = re.compile(r'Рубин|Рубін|רובין|ルービン|Легенда|Леґенда|Портум|Силверлине|Сілверлайн|Силверлайн|Хунгариа|'
                      r'Унгарски концерт|Венгрия Концерт|Угорський концерт|קונצרט הונגריה|Ουγγρική συναυλία|'
                      r'Тхе |Детаилед|Хоме|Gümüş Hat|Macaristan Konseri|Concierto de Hungría|Concert Hongrie|'
                      r'Concerto ungherese|Maďarský koncert|Mađarski koncert|Koncert Węgierski|Concertul din Ungaria|'
                      r'Hongarije Concert|Hungaria Konzert|Kooncert|(?:Grupo|Gruppo|Groupe|Grupa|Grupul|Skupina) Rubin|'
                      r'Rubin[- ](?:Gruppe|Groep|Grubu|csoport)|Rubina\b')


def segments2(s):
    """Innermost elements of ANY text tag whose content is inline-only, still English or mis-branded."""
    clean = strip_code(s)
    out = []
    for m in ANY_RE.finditer(clean):
        tag = m.group(1).lower()
        # find matching close for this tag accounting for nesting of the same tag
        depth, pos = 1, m.end()
        tre = re.compile(r'<(/?)%s\b[^>]*>' % tag, re.I)
        while depth:
            n = tre.search(clean, pos)
            if not n:
                break
            depth += -1 if n.group(1) else 1
            pos = n.end()
        if depth:
            continue
        a, b = m.end(), n.start()
        inner = clean[a:b]
        if re.sub(INLINE_OK, '', inner).count('<'):
            continue  # contains block-level children
        t = text_of(inner)
        if not t or len(t) < 2:
            continue
        if is_english(t) or MISBRAND.search(t) or (len(re.findall(r'\w+', t)) <= 3 and re.search(
                r'\b(Best|Cruise|Tested|Check|Book|Price|Free|Cancellation|Dock|Departure|Duration|Tickets?|Reviews?|'
                r'Overview|Summary|Included|Top|Pick|From|Live|Night|Party|Unlimited|Drinks?|Lemonade|Spritzer|'
                r'Instant|Official|Availability|Confirmation|Guaranteed|Private|Yacht|Water Taxi|Hour|Min)\b', t)):
            out.append((a, b, s[a:b]))
    # innermost only
    out.sort()
    keep = [x for x in out if not any(y is not x and x[0] <= y[0] and y[1] <= x[1] for y in out)]
    return keep


INLINE_TAGS = {'a', 'strong', 'b', 'em', 'i', 'span', 'br', 'small', 'sup', 'sub', 'u', 'mark', 'code', 'img'}
TOKEN_RE = re.compile(r'<(/?)([a-zA-Z0-9]+)\b[^>]*?(/?)>|[^<]+', re.S)
LABEL_RE = re.compile(r'\b(Summary|Overall|Impression|Location|Map|map|Video|Check|Book|Tickets?|Departure|Duration|Virtual|'
                      r'tour|Tour|Area|from|reviews?|Watch|Perfect|Prices?|Best|Cruises?|Hostels?|Type|details|Your|Name|'
                      r'Email|Message|Cons|Pros|Free|Walking|Cloakroom|Read|here|The|Gondola)\b')


def segments3(s):
    """Maximal runs of inline content (text + balanced inline tags) between block-level tags."""
    clean = strip_code(s)
    body = clean.find('<body')
    runs, cur = [], None
    for m in TOKEN_RE.finditer(clean, max(body, 0)):
        tagname = (m.group(2) or '').lower()
        is_inline = not m.group(2) or tagname in INLINE_TAGS
        if is_inline:
            if cur is None:
                cur = [m.start(), m.end()]
            cur[1] = m.end()
        else:
            if cur:
                runs.append(tuple(cur))
            cur = None
    out = []
    for a, b in runs:
        raw = clean[a:b]
        # trim to balanced inline tags: require each open inline tag to be closed inside the run
        opens = [t.lower() for t in re.findall(r'<([a-zA-Z]+)\b(?![^>]*/>)', raw) if t.lower() not in ('br', 'img')]
        closes = [t.lower() for t in re.findall(r'</([a-zA-Z]+)>', raw)]
        if sorted(opens) != sorted(closes):
            continue
        t = text_of(raw)
        if len(t) < 2 or not re.search(r'[A-Za-z]{2}', t):
            continue
        words = re.findall(r'\w+', t)
        if is_english(t) or (len(words) <= 6 and LABEL_RE.search(t) and
                             sum(1 for w in re.findall(r"[A-Za-z]+", t) if w.lower() in EN or LABEL_RE.fullmatch(w))
                             >= max(1, len(words) * 0.5)):
            lead = len(raw) - len(raw.lstrip())
            trail = len(raw) - len(raw.rstrip())
            out.append((a + lead, b - trail, s[a + lead:b - trail]))
    return out


def extract(outdir, pages, finder=None):
    finder = finder or segments
    os.makedirs(outdir, exist_ok=True)
    for lang in LANGS:
        segs = []
        for page in pages:
            f = f'{lang}/{page}/index.html'
            if not os.path.exists(f):
                continue
            s = open(f, encoding='utf-8').read()
            for a, b, h in finder(s):
                lead = len(h) - len(h.lstrip())
                segs.append({'id': f'{f}#{a + lead}', 'html': h.strip()})
        json.dump(segs, open(f'{outdir}/{lang}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(lang, len(segs), 'segments', sum(len(x['html']) for x in segs), 'chars')


def apply(indir):
    byfile = {}
    for lang in LANGS:
        src_p, out_p = f'{indir}/{lang}.json', f'{indir}/{lang}.out.json'
        if not os.path.exists(out_p):
            print('missing', out_p)
            continue
        src = {x['id']: x['html'] for x in json.load(open(src_p, encoding='utf-8'))}
        out = {x['id']: x['html'] for x in json.load(open(out_p, encoding='utf-8'))}
        missing = set(src) - set(out)
        if missing:
            print(lang, 'untranslated ids:', len(missing))
        for i, h in out.items():
            if i not in src:
                continue
            f, a = i.rsplit('#', 1)
            byfile.setdefault(f, []).append((int(a), src[i], h))
    bad = 0
    for f, items in byfile.items():
        s = open(f, encoding='utf-8').read()
        for a, old, new in sorted(items, reverse=True):
            j = s.find(old, a)
            if j != a and s[a:a + len(old)] != old:
                j = s.find(old)  # fall back to unique match
                if j < 0 or s.count(old) != 1:
                    bad += 1
                    continue
            else:
                j = a
            s = s[:j] + new + s[j + len(old):]
        open(f, 'w', encoding='utf-8').write(s)
    print(len(byfile), 'files updated;', bad, 'segments skipped (moved/ambiguous)')


if __name__ == '__main__':
    if sys.argv[1] == 'extract':
        extract(sys.argv[2], sys.argv[3:])
    elif sys.argv[1] == 'extract2':
        extract(sys.argv[2], sys.argv[3:], finder=segments2)
    elif sys.argv[1] == 'extract3':
        extract(sys.argv[2], sys.argv[3:], finder=segments3)
    elif sys.argv[1] == 'apply':
        apply(sys.argv[2])
