# -*- coding: utf-8 -*-
"""Rebuild the best-hostels page for one language from scripts/hostels_data_<lang>.py.

    python3 scripts/upgrade_hostels.py en best-hostels-budapest.html
    python3 scripts/upgrade_hostels.py hu hu/legjobb-hostelek-budapesten/index.html

Runs on a page still built on the pre-2026-11 template (10th hostel = Carpe Noctem).
Selectors are structural (classes and ids), so every language uses the same code;
all copy comes from the data module (HOSTELS + UI).
"""
import importlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
lang, rel = sys.argv[1], sys.argv[2]
D = importlib.import_module('hostels_data_%s' % lang)
HOSTELS, U = D.HOSTELS, D.UI
CHECKED, CHECKED_ISO = D.CHECKED, D.CHECKED_ISO
from hostels_data_en import HIVE_LINK_CARD, HIVE_LINK_REVIEW

PAGE = os.path.join(HERE, '..', rel)
SZIMPLA = 'assets/cdn/60e43c7d6d05b671dff0dc1a/63c134628ac294035bf75327_1_Szimpla%20Ruin%20Bar-p-500.webp'
BOOKING_ICON = 'IHZpZXdCb3g9IjAgMCAzMiAzMiIg'  # Booking.com 32x32 svg icon (base64 fragment)

s = open(PAGE, encoding='utf-8').read()
assert 'section-10-carpe-noctem-hostel' in s, 'page already upgraded?'


def match_close(s, start, tag):
    pat = re.compile(r'<%s\b|</%s>' % (tag, tag))
    depth = 0
    for m in pat.finditer(s, start):
        depth += 1 if m.group(0)[1] != '/' else -1
        if depth == 0:
            return m.end()
    raise ValueError('unclosed ' + tag)


def inner(s, open_pat, new, count=1):
    """Replace the inner HTML of the first element whose opening tag matches open_pat."""
    m = re.search(open_pat, s)
    assert m, open_pat
    tag = re.match(r'<(\w+)', m.group(0)).group(1)
    end = match_close(s, m.start(), tag)
    return s[:m.end()] + new + '</%s>' % tag + s[end:]


def kfmt(n):
    if n < 1000:
        return '%d+' % (n // 10 * 10)
    v = n // 100 / 10
    return ('%d' % v if v == int(v) else U['decimal'].join(('%.1f' % v).split('.'))) + U['k'] + '+'


def num(x):  # 9.2 -> "9.2" / "9,2"
    return U['decimal'].join(('%.1f' % x).split('.'))


def thousands(n):
    return format(n, ',').replace(',', U['thousands'])


def strip(x):
    return re.sub(r'<[^>]+>', '', x).replace('&amp;', '&')


def a(h):
    return '<a href="#%s">%s</a>' % (h['id'], h['name'])


H = {h['n']: h for h in HOSTELS}

# ---------------------------------------------------------------- head / meta
s = re.sub(r'<title>[^<]*</title>', '<title>%s</title>' % U['title'], s, count=1)
for prop in ('og:title', 'twitter:title'):
    s = re.sub(r'<meta content="[^"]*" (property|name)="%s"/>' % prop,
               lambda m: '<meta content="%s" %s="%s"/>' % (U['title'], m.group(1), prop), s)
for prop in ('description', 'og:description', 'twitter:description'):
    s = re.sub(r'<meta content="[^"]*" (property|name)="%s"/>' % prop,
               lambda m: '<meta content="%s" %s="%s"/>' % (U['meta'].replace('"', '&quot;'), m.group(1), prop), s)

# ---------------------------------------------------------------- hero
s = inner(s, r'<span class="ltt-bc-current">', U['breadcrumb'])
s = inner(s, r'<span class="ltt-hero-kicker-badge">', U['kicker_badge'])
s = inner(s, r'<h1 class="ltt-editorial-h1">', '\n      %s <span class="ltt-h1-muted">%s</span>\n' % (U['h1_main'], U['h1_muted']))
s = inner(s, r'<div class="ltt-author-line">', '\n            %s\n          ' % U['author_line'])
s = inner(s, r'<div class="ltt-author-role">', U['author_role'])
s = inner(s, r'<span class="ltt-trust-pill paragraph-26">', U['last_updated'])
lc = s.index('<div class="ltt-lead-copy">') + len('<div class="ltt-lead-copy">')
fig = s.index('<figure', lc)
s = s[:lc] + '\n' + U['intro'] + s[fig:]


def count(cat):
    return sum(1 for h in HOSTELS if cat in h['cats'].split())
for cat, label in U['filters']:
    s = re.sub(r'(data-cat="%s" onclick="lttFilterItems\(\'%s\', this\)" type="button">)[^<]*(</button>)' % (cat, cat),
               lambda m: m.group(1) + '%s (%d)' % (label, count(cat)) + m.group(2), s)

# ---------------------------------------------------------------- deck cards
def rev_badges(html, h, link_override=None):
    def fix(m):
        b = m.group(0)
        href = re.search(r'href="([^"]+)"', b).group(1)
        if 'booking' in href or BOOKING_ICON in b:
            if not h['bk']:
                return ''
            sc, n = h['bk']
        else:
            sc, n = h['hw']
            if link_override:
                b = b.replace(href, link_override)
        b = re.sub(r'<span class="bpa-rev-score">[^<]*</span>', '<span class="bpa-rev-score">%s</span>' % num(sc), b)
        b = re.sub(r'<span class="bpa-rev-count">[^<]*</span>', '<span class="bpa-rev-count">(%s)</span>' % kfmt(n), b)
        return b
    return re.sub(r'<a class="bpa-rev-badge".*?</a>', fix, html, flags=re.S)


def kicker(h):
    return ('<div class="bpa-kicker">%s • %s • <a class="bpa-kicker-map-link" '
            'href="https://www.google.com/maps/search/?api=1&amp;query=%s" onclick="event.stopPropagation()" '
            'rel="noopener noreferrer" target="_blank">%s</a></div>') % (
        h['brand'], U['district_fmt'] % h['district'], h['area_q'], h['area'].split(', ', 1)[1])


CARPE_LINK = re.compile(r'https://tp\.media/r\?marker=404154\.article-best-hostels-budapest-carpe-noctem-([a-z-]+)&amp;[^"]+')
best_for = lambda h, label: '<strong>%s</strong> %s <strong>%s</strong> %s' % (label, h['best_for'], U['skip_if'], h['skip_if'])

for h in HOSTELS:
    n = h['n']
    st = s.rindex('<div class="bpa-card"', 0, s.index('id="card-%d"' % n))
    en = match_close(s, st, 'div')
    c = s[st:en]
    c = re.sub(r'data-cat="[^"]*"', 'data-cat="%s"' % h['cats'], c, count=1)
    c = re.sub(r'(<span class="bpa-rank-tag [^"]*">)[^<]*(</span>)', r'\g<1>%s\g<2>' % h['tag'], c, count=1)
    c = re.sub(r'<div class="bpa-kicker">.*?</div>', kicker(h), c, count=1, flags=re.S)
    if n == 10:
        c = CARPE_LINK.sub(HIVE_LINK_CARD, c)
        c = re.sub(r'<div class="bpa-slider"[^>]*>.*?</div>',
                   '<div class="bpa-slider" onscroll="bpaCount(this)"><img alt="%s" loading="lazy" src="%s"/></div>' % (U['szimpla_alt'], SZIMPLA),
                   c, count=1, flags=re.S)
        c = re.sub(r'<button aria-label="[^"]*" class="bpa-arrow[^"]*"[^>]*>.</button>\s*', '', c)
        c = re.sub(r'<span class="bpa-pill">[^<]*</span>\s*', '', c)
        c = c.replace('<div class="bpa-slider"', '<span class="bpa-pill">%s</span>\n<div class="bpa-slider"' % U['szimpla_pill'], 1)
    else:
        c = re.sub(r'(<img alt=")[^"]+(")', lambda m: m.group(1) + h['name'] + m.group(2), c)
    c = re.sub(r'(<a class="bpa-title"[^>]*>)[^<]*(</a>)', r'\g<1>%s\g<2>' % h['name'], c, count=1)
    c = rev_badges(c, h, HIVE_LINK_CARD if n == 10 else None)
    c = re.sub(r'<div class="bpa-proof">.*?</div>',
               '<div class="bpa-proof"><span class="bpa-vchip">%s</span></div>' % U['tested_chip'] if h['tested'] else '<div class="bpa-proof"></div>',
               c, count=1, flags=re.S)
    specs = '\n'.join('<span class="bpa-sp">%s</span>' % x for x in h['specs'])
    mob = '<span class="bpa-vchip bpa-proof-mobile">%s</span>\n' % U['tested_chip'] if h['tested'] else ''
    c = re.sub(r'<div class="bpa-specs-row">.*?</div>', '<div class="bpa-specs-row">\n%s%s\n</div>' % (mob, specs), c, count=1, flags=re.S)
    c = re.sub(r'<div class="bpa-best-for">.*?</div>', '<div class="bpa-best-for">\n%s\n</div>' % best_for(h, U['best_for_card']), c, count=1, flags=re.S)
    c = re.sub(r'<div class="bpa-price">[^<]*</div>', '<div class="bpa-price">%s</div>' % (U['from_eur'] % h['dorm']), c, count=1)
    c = re.sub(r'<div class="bpa-psub">[^<]*</div>', '<div class="bpa-psub">%s</div>' % U['card_psub'], c, count=1)
    c = re.sub(r'<div class="bpa-trust-micro">.*?</div>', '<div class="bpa-trust-micro">\n<span>%s</span>\n</div>' % h['trust'], c, count=1, flags=re.S)
    c = re.sub(r'(<a class="bpa-btn"[^>]*>)[^<]*(</a>)', r'\g<1>%s\g<2>' % U['card_btn'], c, count=1)
    c = re.sub(r'<a class="bpa-sublink" href="[^"]*">[^<]*</a>', '<a class="bpa-sublink" href="#%s">%s</a>' % (h['id'], U['read_review']), c, count=1)
    s = s[:st] + c + s[en:]
    s = re.sub(r'<!-- #%d: [^>]*-->' % n, '<!-- #%d: %s -->' % (n, strip(h['name'])), s, count=1)

# ---------------------------------------------------------------- detailed reviews
def ul(items):
    return '<ul role="list">' + ''.join('<li><strong>%s</strong>: %s</li>' % it for it in items) + '</ul>'


def pros_cons(h):
    if h['tested']:
        x, y, lx, ly = h['pros'], h['cons'], U['pros'], U['cons']
    else:
        x, y, lx, ly = h['why'], h['skip'], U['why'], U['why_skip']
    return ('<div class="pro-con-box-wrapper"><div class="w-layout-grid grid-15"><div class="pro-con-box-pro-cell" data-wf-pbl="layout-grid-1x2-vertical">'
            '<div class="pro-con-box-pro-cell-rich-text-block w-richtext"><h3><strong>%s</strong></h3>%s</div></div>'
            '<div class="pro-con-box-con-cell" data-wf-pbl="layout-grid-1x2-vertical"><div class="pro-con-box-con-cell-rich-text-block w-richtext">'
            '<h3><strong>%s</strong></h3>%s</div></div></div></div>') % (lx, ul(x), ly, ul(y))


def bento(title, pill, body):
    return ('<details class="ltt-bento-group" open="">\n<summary class="ltt-bento-group-head">\n'
            '<span class="ltt-bento-group-title">%s</span>\n<span class="ltt-bento-right">\n<span class="ltt-mini-pill">%s</span>\n'
            '<span class="ltt-bento-chev">▾</span>\n</span>\n</summary>\n<div class="ltt-bento-group-body">\n%s\n</div>\n</details>\n') % (title, pill, body)


def filmstrip(name, what, imgs):
    if not imgs:
        return ''
    k = len(imgs)
    slides = ''.join(
        '<div class="ltt-strip-slide"><img alt="%s" loading="lazy" src="%s"/>'
        '<div class="ltt-strip-cap"><span class="ltt-strip-num">%d / %d</span> <span>%s: %s</span></div></div>' % (
            U['photo_alt'] % (name, what), src, i + 1, k, name, what) for i, src in enumerate(imgs))
    return ('<div class="ltt-filmstrip-wrap"><button aria-label="%s" class="ltt-film-btn ltt-film-prev is-disabled" '
            'onclick="window.lttFilmSlide(this, -1)" type="button">‹</button><button aria-label="%s" class="ltt-film-btn ltt-film-next" '
            'onclick="window.lttFilmSlide(this, 1)" type="button">›</button><div class="ltt-filmstrip" onscroll="window.lttFilmSync(this)">'
            '%s</div></div>\n') % (U['prev_photo'], U['next_photo'], slides)


def buy_card(h, link):
    perks = [U['address_perk'] % h['address'], h['checkin'], h['rules']]
    if h['private']:
        perks.insert(1, U['privates_perk'] % h['private'])
    return ('<div class="ltt-buy-card">\n<div class="ltt-buy-card-head">\n<div class="ltt-buy-card-badge">\n<span class="ltt-live-dot"></span>\n'
            '<span>%s</span>\n</div>\n<div class="ltt-buy-card-price">\n<span class="ltt-buy-price-val">%s</span>\n'
            '<span class="ltt-buy-price-sub">%s</span>\n</div>\n</div>\n<div class="ltt-buy-card-body">\n'
            '<div class="ltt-buy-card-info">\n<h4 class="ltt-buy-card-title">%s</h4>\n<div class="ltt-buy-card-perks">\n%s\n</div>\n</div>\n'
            '<div class="ltt-buy-card-action">\n<a class="ltt-buy-cta-btn" href="%s" rel="noopener nofollow sponsored" target="_blank">\n'
            '<span>%s</span>\n<span class="ltt-cta-arrow">→</span>\n</a>\n<div class="ltt-buy-card-trust">\n'
            '<span>%s</span>\n</div>\n</div>\n</div>\n</div>\n') % (
        U['buy_badge'], U['from_eur'] % h['dorm'], U['buy_sub'], h['name'],
        '\n'.join('<span class="ltt-buy-perk">%s</span>' % p for p in perks), link, U['buy_cta'], U['buy_trust'])


def quick_facts(h):
    q = U['qf']
    dorm = q['dorm_fmt'] % h['dorm'] + (q['priv_fmt'] % h['private'] if h['private'] else '')
    rating = q['hw_fmt'] % (num(h['hw'][0]), thousands(h['hw'][1])) + (q['bk_fmt'] % (num(h['bk'][0]), thousands(h['bk'][1])) if h['bk'] else '')
    rows = [(q['address'], h['address']), (q['dorm'], dorm), (q['transit'], h['transit']), (q['checkin'], h['checkin']),
            (q['rules'], h['rules']), (q['ratings'], rating), (q['watch'], h['watch'])]
    chips = '\n'.join('<span class="qf1-chip %s">%s %s</span>' % (k, '✓' if k == 'yes' else '✕', t) for k, t in h['chips'])
    return ('<div class="qf1-wrap">\n<div class="qf1-title-row">\n<h4 class="qf1-title">%s</h4>\n<span class="qf1-badge">%s</span>\n</div>\n'
            '<div class="qf1-table">\n%s\n</div>\n<div class="qf1-Validation-pills">\n%s\n</div>\n</div>\n') % (
        q['title'] % h['name'], h['area'], '\n'.join('<div class="qf1-row"><div class="qf1-label">%s</div><div class="qf1-val">%s</div></div>' % r for r in rows), chips)


for h in HOSTELS:
    n = h['n']
    old_id = 'section-10-carpe-noctem-hostel' if n == 10 else h['id']
    st = s.rindex('<details class="bpa-details-card"', 0, s.index('id="%s"' % old_id))
    en = match_close(s, st, 'details')
    old = s[st:en]
    head = old[:old.index('</summary>') + len('</summary>')]
    head = re.sub(r'data-cat="[^"]*"', 'data-cat="%s"' % h['cats'], head, count=1)
    head = head.replace('id="%s"' % old_id, 'id="%s"' % h['id'])
    head = re.sub(r'(<span class="bpa-rank-tag [^"]*">)[^<]*(</span>)', r'\g<1>%s\g<2>' % h['tag'], head, count=1)
    head = re.sub(r'<div class="bpa-kicker">.*?</div>', kicker(h), head, count=1, flags=re.S)
    head = re.sub(r'(<h3 class="bpa-details-title">)[^<]*(</h3>)', r'\g<1>%s\g<2>' % h['name'], head, count=1)
    head = rev_badges(head, h, HIVE_LINK_REVIEW if n == 10 else None)
    head = re.sub(r'<div class="bpa-proof">.*?</div>',
                  '<div class="bpa-proof"><span class="bpa-vchip">%s</span></div>' % U['tested_chip'] if h['tested'] else '<div class="bpa-proof"></div>',
                  head, count=1, flags=re.S)
    head = re.sub(r'<span class="bpa-details-price">[^<]*</span>', '<span class="bpa-details-price">%s</span>' % (U['from_eur'] % h['dorm']), head, count=1)
    groups_imgs = [re.findall(r'<div class="ltt-strip-slide"><img [^>]*src="([^"]+)"', g.group(0))
                   for g in re.finditer(r'<details class="ltt-bento-group".*?</details>', old, flags=re.S)]
    link = HIVE_LINK_REVIEW if n == 10 else re.search(r'<a class="ltt-buy-cta-btn" href="([^"]+)"', old).group(1)
    body = pros_cons(h) + '\n'
    summ = ''
    if h.get('video'):
        summ += '<blockquote><strong>🎥 %s </strong>%s <a href="%s" target="_blank"><strong>%s</strong></a>.</blockquote>' % (
            U['video'], U['watch_my'], h['video'][0], h['video'][1])
    summ += ''.join('<p>%s</p>' % p for p in h['summary'])
    summ += '<p>%s</p>' % best_for(h, U['best_for_summary'])
    body += bento(U['summary_title'], U['summary_pill'], '<div class="w-richtext">%s</div>\n%s' % (summ, buy_card(h, link)))
    for gi, (title, what, cards) in enumerate(h['groups']):
        imgs = groups_imgs[gi + 1] if gi + 1 < len(groups_imgs) else []
        k = len(imgs)
        pill = (U['swipe_photos'] % k) if k > 1 else (U['one_photo'] if k == 1 else U['no_photo'])
        sp = '<div class="ltt-sub-points">%s</div>' % ''.join('<div class="ltt-sp-card"><h4>%s</h4>%s</div>' % cc for cc in cards)
        body += bento(title, pill, filmstrip(h['name'], what, imgs) + sp)
    body += quick_facts(h)
    s = s[:st] + head + '\n<div class="bpa-details-body">\n' + body + '</div>\n</details>' + s[en:]

s = inner(s, r'<h2 class="bpa-breakdown-heading"[^>]*>', U['breakdown_h2'])
s = inner(s, r'<p class="bpa-breakdown-sub">', U['breakdown_sub'])

# ---------------------------------------------------------------- new editorial sections
picks_html = ''.join('<li><strong>%s:</strong> %s. %s</li>' % (lab, a(H[n]), why(H) if callable(why) else why) for lab, n, why in U['picks'])
rows = ''.join(
    '<tr><td><a class="ltt-tbl-title" href="#%s">%d. %s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
        h['id'], h['n'], h['name'], h['short'], h['area'], U['eur'] % h['dorm'], num(h['hw'][0]), h['noise'], h['watch']) for h in HOSTELS)
sec = U['sections']
NEW = ('<section id="best-hostel-by-traveler" style="margin-bottom: 50px;">\n<div class="ltt-sec-header">\n<span class="ltt-sec-badge">%s</span>\n'
       '<h2 class="ltt-sec-title">%s</h2>\n<p class="ltt-sec-subtitle">%s</p>\n</div>\n'
       '<div class="w-richtext" style="margin-top: 16px;"><ul role="list">%s</ul></div>\n</section>\n') % (
    sec['picks_badge'], sec['picks_h2'], sec['picks_sub'], picks_html)
NEW += ('<section id="hostels-side-by-side" style="margin-bottom: 50px;">\n<div class="ltt-sec-header">\n<span class="ltt-sec-badge">%s</span>\n'
        '<h2 class="ltt-sec-title">%s</h2>\n<p class="ltt-sec-subtitle">%s</p>\n</div>\n'
        '<div class="ltt-summary-table-wrap" style="margin-top: 16px;"><div class="ltt-table-scroll"><table class="ltt-summary-table">\n'
        '<thead><tr>%s</tr></thead>\n<tbody>%s</tbody></table></div></div>\n</section>\n') % (
    sec['table_badge'], sec['table_h2'], sec['table_sub'], ''.join('<th>%s</th>' % t for t in sec['table_cols']), rows)
NEW += ('<section id="where-to-stay-hostels" style="margin-bottom: 50px;">\n<div class="ltt-sec-header">\n<span class="ltt-sec-badge">%s</span>\n'
        '<h2 class="ltt-sec-title">%s</h2>\n<p class="ltt-sec-subtitle">%s</p>\n</div>\n<div class="w-richtext" style="margin-top: 16px;">\n%s\n</div>\n</section>\n') % (
    sec['areas_badge'], sec['areas_h2'], sec['areas_sub'], sec['areas_body'](H, a))
anchor = '<div class="ltt-editorial-wrapper">\n<section id="budapest-hostels-map"'
assert anchor in s
s = s.replace(anchor, '<div class="ltt-editorial-wrapper">\n' + NEW + '<section id="budapest-hostels-map"', 1)

ms = s.index('<section id="budapest-hostels-map"')
s = s[:ms] + inner(s[ms:], r'<h2 class="ltt-sec-title">', sec['map_h2'])
ms = s.index('<section id="budapest-hostels-map"')
s = s[:ms] + inner(s[ms:], r'<p class="ltt-sec-subtitle">', sec['map_sub'])
ts = s.index('<section id="budapest-hostel-types"')
s = s[:ts] + inner(s[ts:], r'<h2 class="ltt-sec-title">', sec['types_h2'])

# ---------------------------------------------------------------- FAQ
def faq_card(i, q, ans):
    first = ' first' if i == 0 else ''
    return ('<div class="cf-faq-plus-card">\n<div class="cf-faq-question-container-3%s">\n<div class="cf-faq-question-wrap">\n'
            '<h3 class="cf-faq-questions-2">%s</h3>\n<div class="cf-faq-icon-contain">\n<div class="cf-faq-line">\n</div>\n'
            '<div class="cf-faq-line-vertical">\n</div>\n</div>\n</div>\n</div>\n<div class="cf-faq-answer-wrap-2">\n'
            '<div class="cf-faq-content-2 w-richtext">%s</div>\n</div>\n<div class="cf-bottom-line-2">\n</div>\n</div>\n') % (first, q, ans)


fs = s.index('<div class="cf-faqs-container">')
fe = match_close(s, fs, 'div')
s = s[:fs] + '<div class="cf-faqs-container">\n' + ''.join(faq_card(i, q, x) for i, (q, x) in enumerate(U['faq'])) + '</div>' + s[fe:]

# ---------------------------------------------------------------- sticky bar + page config
s = re.sub(r'(<span class="hybrid-active-title" id="sticky-name">)[^<]*(</span>)', r'\g<1>%s\g<2>' % HOSTELS[0]['name'], s, count=1)
s = re.sub(r'(<span class="hybrid-active-price" id="sticky-price">)[^<]*(</span>)', r'\g<1>%s\g<2>' % (U['from_eur'] % HOSTELS[0]['dorm']), s, count=1)
s = inner(s, r'<span class="hybrid-active-trust">', U['sticky_trust'])
s = inner(s, r'<a class="hybrid-cta-btn"[^>]*>', '\n      %s\n    ' % U['sticky_cta'])
s = re.sub(r'(<div aria-label=")[^"]*(" aria-modal="true" class="hybrid-sheet")', r'\g<1>%s\g<2>' % U['sheet_label'], s, count=1)
s = s.replace('Jump to Tested Budapest Hostel', U['sheet_label'])
s = re.sub(r'"shortTitles": \[[^\]]*\]', '"shortTitles": ' + json.dumps([strip(h['name']) for h in HOSTELS], ensure_ascii=False), s, count=1)
s = re.sub(r'"tocBreakdownLabel": "[^"]*"', '"tocBreakdownLabel": "%s"' % U['toc_breakdown'], s, count=1)

s = s.replace('content: "Collapse Review";', 'content: "%s";' % U['collapse_label']).replace('content: "Read Review";', 'content: "%s";' % U['expand_label'])

# ---------------------------------------------------------------- JSON-LD
URL = U['url']
graph = [
    {"@type": "Article", "@id": URL + "#article", "mainEntityOfPage": {"@type": "WebPage", "@id": URL},
     "headline": U['title'], "description": U['meta'], "url": URL, "inLanguage": lang,
     "datePublished": "2022-12-28", "dateModified": CHECKED_ISO,
     "author": {"@type": "Person", "name": "Adam Dimitrov", "jobTitle": U['job_title'], "url": U['about_url']},
     "publisher": {"@type": "Organization", "name": "Budapest Adventures", "url": "https://www.budapestadventures.com",
                   "logo": {"@type": "ImageObject", "url": "https://www.budapestadventures.com/assets/budapest-adventures-logo.png"}},
     "image": ["https://www.budapestadventures.com/assets/cdn/60e43c7d6d05b671dff0dc1a/63aef937493ff750c5613e6a_Budapest-hostels-3.webp",
               "https://www.budapestadventures.com/assets/cdn/60e43c7d6d05b671dff0dc1a/64a94406fe5dca443dcfeee5_03-maverick-urban-lodge-roof-terrace-area.webp"],
     "mainEntity": {"@id": URL + "#list"}},
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": U['home'], "item": U['home_url']},
        {"@type": "ListItem", "position": 2, "name": strip(U['breadcrumb']), "item": URL}]},
    {"@type": "ItemList", "@id": URL + "#list", "name": U['title'], "itemListOrder": "https://schema.org/ItemListOrderAscending",
     "numberOfItems": len(HOSTELS),
     "itemListElement": [
         {"@type": "ListItem", "position": h['n'], "url": URL + '#' + h['id'],
          "item": {"@type": "Hostel", "name": strip(h['name']), "description": strip(h['best_for']),
                   "address": {"@type": "PostalAddress", "streetAddress": h['street'], "postalCode": h['zip'],
                               "addressLocality": "Budapest", "addressCountry": "HU"},
                   "priceRange": strip(U['price_range'] % h['dorm'])}} for h in HOSTELS]},
    {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(x)}} for q, x in U['faq']]},
]
ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)
js = s.index('<script id="ltt-schema-jsonld" type="application/ld+json">')
je = s.index('</script>', js)
s = s[:js] + '<script id="ltt-schema-jsonld" type="application/ld+json">\n' + ld + '\n' + s[je:]

# ---------------------------------------------------------------- checks
s = s.replace(' — ', ' - ')
assert '—' not in s, [m.start() for m in re.finditer('—', s)][:5]
left = [m.start() for m in re.finditer('Carpe Noctem', s)]
assert not left, [s[i - 120:i + 60] for i in left[:3]]
open(PAGE, 'w', encoding='utf-8').write(s)
print('ok', rel, len(s))
