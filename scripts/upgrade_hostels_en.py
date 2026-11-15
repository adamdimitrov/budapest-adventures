# -*- coding: utf-8 -*-
"""Rebuild /best-hostels-budapest (EN) from scripts/hostels_data_en.py.

Run once on the pre-upgrade page: python3 scripts/upgrade_hostels_en.py
"""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from hostels_data_en import HOSTELS, CHECKED, CHECKED_ISO, HIVE_LINK_CARD, HIVE_LINK_REVIEW

PAGE = os.path.join(os.path.dirname(__file__), '..', 'best-hostels-budapest.html')
URL = 'https://www.budapestadventures.com/best-hostels-budapest'
TITLE = '10 Best Hostels in Budapest in 2026 (I Stayed in 9)'
H1_MAIN, H1_MUTED = '10 Best Hostels in Budapest in 2026', '(I Stayed in 9)'
META = ("I stayed in 9 of Budapest's top hostels, including 30 nights at Maverick. "
        "Dorms from €8: the best party, quiet, budget and nomad picks, by area.")
SZIMPLA = 'assets/cdn/60e43c7d6d05b671dff0dc1a/63c134628ac294035bf75327_1_Szimpla%20Ruin%20Bar-p-500.webp'

s = open(PAGE, encoding='utf-8').read()
assert 'Carpe Noctem' in s, 'page already upgraded?'


def match_close(s, start, tag):
    """Index just after the element opened at `start` closes."""
    pat = re.compile(r'<%s\b|</%s>' % (tag, tag))
    depth = 0
    for m in pat.finditer(s, start):
        depth += 1 if m.group(0)[1] != '/' else -1
        if depth == 0:
            return m.end()
    raise ValueError('unclosed ' + tag)


def kfmt(n):
    if n < 1000:
        return '%d+' % (n // 10 * 10)
    v = n // 100 / 10
    return ('%d' % v if v == int(v) else '%.1f' % v) + 'k+'


def esc_q(x):
    return x


# ---------------------------------------------------------------- head / meta
s = re.sub(r'<title>[^<]*</title>', '<title>%s</title>' % TITLE, s, count=1)
for prop in ('og:title', 'twitter:title'):
    s = re.sub(r'<meta content="[^"]*" (property|name)="%s"/>' % prop,
               lambda m: '<meta content="%s" %s="%s"/>' % (TITLE, m.group(1), prop), s)
for prop in ('description', 'og:description', 'twitter:description'):
    s = re.sub(r'<meta content="[^"]*" (property|name)="%s"/>' % prop,
               lambda m: '<meta content="%s" %s="%s"/>' % (META.replace('"', '&quot;'), m.group(1), prop), s)

# ---------------------------------------------------------------- hero
s = s.replace('<span class="ltt-bc-current">10 Best Hostels in Budapest in 2026</span>',
              '<span class="ltt-bc-current">Best Hostels in Budapest</span>')
s = s.replace('<span class="ltt-hero-kicker-badge">2026 Field-Tested Comparison</span>',
              '<span class="ltt-hero-kicker-badge">2026 Hostel Comparison</span>')
s = re.sub(r'(<h1 class="ltt-editorial-h1">)\s*10 Best Hostels in Budapest in 2026 <span class="ltt-h1-muted">\(Personally Tested\)</span>',
           r'\1\n      %s <span class="ltt-h1-muted">%s</span>' % (H1_MAIN, H1_MUTED), s)
s = s.replace('By <a href="/about" target="_blank">Adam Dimitrov</a> — Founder &amp; Local Budapest Tester',
              'By <a href="/about" target="_blank">Adam Dimitrov</a>, Founder &amp; Local Budapest Tester')
s = s.replace('<div class="ltt-author-role">Personally Field-Tested • Original Photos &amp; Videos</div>',
              '<div class="ltt-author-role">Stayed in 9 of these 10 • Own photos &amp; video reviews</div>')
s = re.sub(r'<strong>Last updated</strong>: [A-Za-z]+ \d+, 2026', '<strong>Last updated</strong>: Nov 14, 2026', s)

INTRO = (
    '<p>Picking the wrong Budapest hostel costs you sleep, not money. Dorm beds in the center run <strong>€8 to €15 a night</strong>, '
    'but a party hostel in the Jewish Quarter and a quiet pod hostel by the Central Market Hall are two completely different trips.</p>\n'
    '<p>I <strong>stayed in 9 of the 10 hostels below</strong>, including <strong>30 nights at Maverick for €280</strong>, and compared them side by side '
    'on what decides the booking: noise at night, bed privacy, bathrooms, kitchen, age rules, the crowd and the real price per night. '
    'The Hive is the one party pick I haven\'t slept in, so it gets checked facts only and no "tested" badge.</p>\n'
    '<p>Prices and ratings checked on <strong>%s</strong>. Use the filters to jump straight to party, quiet, budget, private-room or digital-nomad picks.</p>\n' % CHECKED)
s = re.sub(r'<p>Budapest is renowned as one of Europe\'s top backpacking destinations.*?</p>\s*<p>I personally visited, stayed in.*?</p>\s*',
           INTRO, s, count=1, flags=re.S)

# filters (counts computed from data-cat)
def count(cat):
    return sum(1 for h in HOSTELS if cat in h['cats'].split())
FILTERS = [('party', '🎉 Social &amp; Party'), ('quiet', '😴 Quiet Sleep'), ('budget', '💶 Under €11'),
           ('private', '🛏️ Private Rooms'), ('nomad', '💻 Digital Nomads'), ('kitchen', '🍳 Guest Kitchen')]
for cat, label in FILTERS:
    s = re.sub(r'(data-cat="%s" onclick="lttFilterItems\(\'%s\', this\)" type="button">)[^<]*(</button>)' % (cat, cat),
               lambda m: m.group(1) + '%s (%d)' % (label, count(cat)) + m.group(2), s)

# ---------------------------------------------------------------- comparison deck cards
def rev_badges(html, h, link_override=None):
    """Update Booking/Hostelworld badge scores inside a reviews block."""
    def fix(m):
        a = m.group(0)
        href = re.search(r'href="([^"]+)"', a).group(1)
        if 'booking' in href:
            if not h['bk']:
                return ''
            sc, n = h['bk']
        else:
            sc, n = h['hw']
            if link_override:
                a = a.replace(href, link_override)
        a = re.sub(r'<span class="bpa-rev-score">[^<]*</span>', '<span class="bpa-rev-score">%.1f</span>' % sc, a)
        a = re.sub(r'<span class="bpa-rev-count">[^<]*</span>', '<span class="bpa-rev-count">(%s)</span>' % kfmt(n), a)
        return a
    return re.sub(r'<a class="bpa-rev-badge".*?</a>', fix, html, flags=re.S)


def kicker(h):
    return ('<div class="bpa-kicker">%s • %s District • <a class="bpa-kicker-map-link" '
            'href="https://www.google.com/maps/search/?api=1&amp;query=%s" onclick="event.stopPropagation()" '
            'rel="noopener noreferrer" target="_blank">%s</a></div>') % (
        h['brand'], h['district'], h['area_q'], h['area'].split(', ', 1)[1])


CARPE_LINK = re.compile(r'https://tp\.media/r\?marker=404154\.article-best-hostels-budapest-carpe-noctem-([a-z-]+)&amp;[^"]+')

for h in HOSTELS:
    n = h['n']
    st = s.index('<div class="bpa-card" data-cat=')
    st = s.index('id="card-%d"' % n)
    st = s.rindex('<div class="bpa-card"', 0, st)
    en = match_close(s, st, 'div')
    c = s[st:en]
    c = re.sub(r'data-cat="[^"]*"', 'data-cat="%s"' % h['cats'], c, count=1)
    c = re.sub(r'(<span class="bpa-rank-tag [^"]*">)[^<]*(</span>)', r'\g<1>%s\g<2>' % h['tag'], c, count=1)
    c = re.sub(r'<div class="bpa-kicker">.*?</div>', kicker(h), c, count=1, flags=re.S)
    if n == 10:
        c = CARPE_LINK.sub(HIVE_LINK_CARD, c)
        c = re.sub(r'<div class="bpa-slider"[^>]*>.*?</div>',
                   '<div class="bpa-slider" onscroll="bpaCount(this)"><img alt="Szimpla Kert ruin bar, a short walk from The Hive on Dob utca" '
                   'loading="lazy" src="%s"/></div>' % SZIMPLA, c, count=1, flags=re.S)
        c = re.sub(r'<button aria-label="(Previous|Next) photo"[^>]*>.</button>\s*', '', c)
        c = re.sub(r'<span class="bpa-pill">[^<]*</span>\s*', '', c)
    c = re.sub(r'(<img alt=")[^"]+(")', lambda m: m.group(1) + h['name'] + m.group(2), c)
    c = re.sub(r'(<a class="bpa-title"[^>]*>)[^<]*(</a>)', r'\g<1>%s\g<2>' % h['name'], c, count=1)
    c = rev_badges(c, h, HIVE_LINK_CARD if n == 10 else None)
    chip = '✓ Personally Tested' if h['tested'] else '★ 9.0 Hostelworld Party Pick'
    c = c.replace('<div class="bpa-proof"><span class="bpa-vchip">✓ Personally Tested</span></div>',
                  '<div class="bpa-proof"><span class="bpa-vchip">%s</span></div>' % chip if h['tested'] else '<div class="bpa-proof"></div>')
    specs = '\n'.join('<span class="bpa-sp">%s</span>' % x for x in h['specs'])
    mob = '<span class="bpa-vchip bpa-proof-mobile">✓ Personally Tested</span>\n' if h['tested'] else ''
    c = re.sub(r'<div class="bpa-specs-row">.*?</div>', '<div class="bpa-specs-row">\n%s%s\n</div>' % (mob, specs), c, count=1, flags=re.S)
    c = re.sub(r'<div class="bpa-best-for">.*?</div>',
               '<div class="bpa-best-for">\n<strong>Best For:</strong> %s <strong>Skip if</strong> %s\n</div>' % (h['best_for'], h['skip_if']),
               c, count=1, flags=re.S)
    c = re.sub(r'<div class="bpa-price">[^<]*</div>', '<div class="bpa-price">From €%d</div>' % h['dorm'], c, count=1)
    c = re.sub(r'<div class="bpa-psub">[^<]*</div>', '<div class="bpa-psub">Dorm bed per night • Checked %s</div>' % CHECKED, c, count=1)
    c = re.sub(r'<div class="bpa-trust-micro">.*?</div>',
               '<div class="bpa-trust-micro">\n<span>%s</span>\n</div>' % h['trust'], c, count=1, flags=re.S)
    c = re.sub(r'(<a class="bpa-btn"[^>]*>)[^<]*(</a>)', r'\g<1>Check Prices &amp; Dates →\g<2>', c, count=1)
    c = re.sub(r'<a class="bpa-sublink" href="[^"]*">', '<a class="bpa-sublink" href="#%s">' % h['id'], c, count=1)
    s = s[:st] + c + s[en:]
    s = s.replace('<!-- #%d: %s -->' % (n, h['old']), '<!-- #%d: %s -->' % (n, h['name']))

# ---------------------------------------------------------------- detailed reviews
def ul(items):
    return '<ul role="list">' + ''.join('<li><strong>%s</strong>: %s</li>' % it for it in items) + '</ul>'


def pros_cons(h):
    if h['tested']:
        a, b, la, lb = h['pros'], h['cons'], 'Pros:', 'Cons:'
    else:
        a, b, la, lb = h['why'], h['skip'], 'Why pick it:', 'Why skip it:'
    return ('<div class="pro-con-box-wrapper"><div class="w-layout-grid grid-15"><div class="pro-con-box-pro-cell" data-wf-pbl="layout-grid-1x2-vertical">'
            '<div class="pro-con-box-pro-cell-rich-text-block w-richtext"><h3><strong>%s</strong></h3>%s</div></div>'
            '<div class="pro-con-box-con-cell" data-wf-pbl="layout-grid-1x2-vertical"><div class="pro-con-box-con-cell-rich-text-block w-richtext">'
            '<h3><strong>%s</strong></h3>%s</div></div></div></div>') % (la, ul(a), lb, ul(b))


def bento(title, pill, body):
    return ('<details class="ltt-bento-group" open="">\n<summary class="ltt-bento-group-head">\n'
            '<span class="ltt-bento-group-title">%s</span>\n<span class="ltt-bento-right">\n<span class="ltt-mini-pill">%s</span>\n'
            '<span class="ltt-bento-chev">▾</span>\n</span>\n</summary>\n<div class="ltt-bento-group-body">\n%s\n</div>\n</details>\n') % (title, pill, body)


def filmstrip(name, what, imgs):
    if not imgs:
        return ''
    k = len(imgs)
    slides = ''.join(
        '<div class="ltt-strip-slide"><img alt="%s: %s, photo from my stay" loading="lazy" src="%s"/>'
        '<div class="ltt-strip-cap"><span class="ltt-strip-num">%d / %d</span> <span>%s: %s</span></div></div>' % (
            name, what, src, i + 1, k, name, what) for i, src in enumerate(imgs))
    return ('<div class="ltt-filmstrip-wrap"><button aria-label="Previous photo" class="ltt-film-btn ltt-film-prev is-disabled" '
            'onclick="window.lttFilmSlide(this, -1)" type="button">‹</button><button aria-label="Next photo" class="ltt-film-btn ltt-film-next" '
            'onclick="window.lttFilmSlide(this, 1)" type="button">›</button><div class="ltt-filmstrip" onscroll="window.lttFilmSync(this)">'
            '%s</div></div>\n') % slides


def buy_card(h, link):
    perks = ['Address: <strong>%s</strong>' % h['address'], h['checkin'], h['rules']]
    if h['private']:
        perks.insert(1, 'Private rooms from <strong>€%d</strong>' % h['private'])
    return ('<div class="ltt-buy-card">\n<div class="ltt-buy-card-head">\n<div class="ltt-buy-card-badge">\n<span class="ltt-live-dot"></span>\n'
            '<span>Live Prices &amp; Availability</span>\n</div>\n<div class="ltt-buy-card-price">\n<span class="ltt-buy-price-val">From €%d</span>\n'
            '<span class="ltt-buy-price-sub">Dorm bed per night • Checked %s</span>\n</div>\n</div>\n<div class="ltt-buy-card-body">\n'
            '<div class="ltt-buy-card-info">\n<h4 class="ltt-buy-card-title">%s</h4>\n<div class="ltt-buy-card-perks">\n%s\n</div>\n</div>\n'
            '<div class="ltt-buy-card-action">\n<a class="ltt-buy-cta-btn" href="%s" rel="noopener nofollow sponsored" target="_blank">\n'
            '<span>Check Dates &amp; Prices</span>\n<span class="ltt-cta-arrow">→</span>\n</a>\n<div class="ltt-buy-card-trust">\n'
            '<span>Prices change by date; the final price shows before you pay</span>\n</div>\n</div>\n</div>\n</div>\n') % (
        h['dorm'], CHECKED, h['name'], '\n'.join('<span class="ltt-buy-perk">%s</span>' % p for p in perks), link)


def quick_facts(h):
    rows = [('Address', h['address']),
            ('Dorm Beds', 'From €%d a night (checked %s)%s' % (h['dorm'], CHECKED, ', privates from €%d' % h['private'] if h['private'] else '')),
            ('Getting There', h['transit']),
            ('Check-In', h['checkin']),
            ('House Rules', h['rules']),
            ('Ratings', 'Hostelworld %.1f/10 (%s reviews)%s' % (h['hw'][0], format(h['hw'][1], ','),
                         ', Booking.com %.1f/10 (%s reviews)' % (h['bk'][0], format(h['bk'][1], ',')) if h['bk'] else '')),
            ('Watch Out For', h['watch'])]
    chips = '\n'.join('<span class="qf1-chip %s">%s %s</span>' % (k, '✓' if k == 'yes' else '✕', t) for k, t in h['chips'])
    return ('<div class="qf1-wrap">\n<div class="qf1-title-row">\n<h4 class="qf1-title">Quick Facts: %s</h4>\n<span class="qf1-badge">%s</span>\n</div>\n'
            '<div class="qf1-table">\n%s\n</div>\n<div class="qf1-Validation-pills">\n%s\n</div>\n</div>\n') % (
        h['name'], h['area'], '\n'.join('<div class="qf1-row"><div class="qf1-label">%s</div><div class="qf1-val">%s</div></div>' % r for r in rows), chips)


for h in HOSTELS:
    n = h['n']
    old_id = 'section-10-carpe-noctem-hostel' if n == 10 else h['id']
    st = s.index('id="%s"' % old_id)
    st = s.rindex('<details class="bpa-details-card"', 0, st)
    en = match_close(s, st, 'details')
    old = s[st:en]
    # head (summary) kept, then updated
    head_end = old.index('</summary>') + len('</summary>')
    head = old[:head_end]
    head = re.sub(r'data-cat="[^"]*"', 'data-cat="%s"' % h['cats'], head, count=1)
    head = head.replace('id="%s"' % old_id, 'id="%s"' % h['id'])
    head = re.sub(r'(<span class="bpa-rank-tag [^"]*">)[^<]*(</span>)', r'\g<1>%s\g<2>' % h['tag'], head, count=1)
    head = re.sub(r'<div class="bpa-kicker">.*?</div>', kicker(h), head, count=1, flags=re.S)
    head = re.sub(r'(<h3 class="bpa-details-title">)[^<]*(</h3>)', r'\g<1>%s\g<2>' % h['name'], head, count=1)
    head = rev_badges(head, h, HIVE_LINK_REVIEW if n == 10 else None)
    if not h['tested']:
        head = head.replace('<div class="bpa-proof"><span class="bpa-vchip">✓ Personally Tested</span></div>', '<div class="bpa-proof"></div>')
    head = re.sub(r'<span class="bpa-details-price">[^<]*</span>', '<span class="bpa-details-price">From €%d</span>' % h['dorm'], head, count=1)
    # images per old bento group, in order
    groups_imgs = []
    for g in re.finditer(r'<details class="ltt-bento-group".*?</details>', old, flags=re.S):
        groups_imgs.append(re.findall(r'<div class="ltt-strip-slide"><img [^>]*src="([^"]+)"', g.group(0)) +
                           re.findall(r'<div class="ltt-strip-slide">\s*<img [^>]*src="([^"]+)"', g.group(0)) * 0)
    link = re.search(r'<a class="ltt-buy-cta-btn" href="([^"]+)"', old).group(1)
    if n == 10:
        link = HIVE_LINK_REVIEW
    body = pros_cons(h) + '\n'
    summ = ''
    if h.get('video'):
        summ += '<blockquote><strong>🎥 Video: </strong>Watch my <a href="%s" target="_blank"><strong>%s</strong></a>.</blockquote>' % h['video']
    summ += ''.join('<p>%s</p>' % p for p in h['summary'])
    summ += '<p><strong>Best for:</strong> %s <strong>Skip it if</strong> %s</p>' % (h['best_for'], h['skip_if'])
    body += bento('Summary &amp; Review', 'Overview', '<div class="w-richtext">%s</div>\n%s' % (summ, buy_card(h, link)))
    for gi, (title, what, cards) in enumerate(h['groups']):
        imgs = groups_imgs[gi + 1] if gi + 1 < len(groups_imgs) else []
        k = len(imgs)
        pill = ('Swipe %d Photos →' % k) if k > 1 else ('1 Photo' if k == 1 else 'From my stay')
        sp = '<div class="ltt-sub-points">%s</div>' % ''.join('<div class="ltt-sp-card"><h4>%s</h4>%s</div>' % c for c in cards)
        body += bento(title, pill, filmstrip(h['name'], what, imgs) + sp)
    body += quick_facts(h)
    new = head + '\n<div class="bpa-details-body">\n' + body + '</div>\n</details>'
    s = s[:st] + new + s[en:]

s = s.replace('Detailed Breakdown — 10 Best Hostels in Budapest', 'Detailed Reviews: 10 Best Hostels in Budapest')
s = s.replace('<p class="bpa-breakdown-sub">Personally field-tested • All reviews open by default • Click to collapse/expand</p>',
              '<p class="bpa-breakdown-sub">9 stayed in, 1 party pick on checked facts • Click to collapse or expand</p>')

# ---------------------------------------------------------------- new editorial sections (traveler type + side-by-side + areas)
def a(h):
    return '<a href="#%s">%s</a>' % (h['id'], h['name'])
H = {h['n']: h for h in HOSTELS}
PICKS = [
    ('Best overall', H[1], 'Social without party noise, curtained beds, great bathrooms, and €280 for my 30-night stay.'),
    ('Solo travelers (18 to 39)', H[2], 'Free daily activities and pub crawls make friends on easy mode. Over 39? Pick Maverick or Wombat\'s.'),
    ('Party', H[10], 'The big, loud option with a rooftop bar in the ruin bar district. Want it more low-key? '
     + a(H[6]) + '.'),
    ('Cheapest bed', H[3], 'Beds from about €8 plus a free breakfast. Bring earplugs: it\'s on a tram junction.'),
    ('Quiet sleep', H[1], 'A quiet side street in District IX. Also calm: ' + a(H[7]) + ' and ' + a(H[5]) + '.'),
    ('Digital nomads', H[4], 'Laptop-friendly lounge and coworking space. Maverick is the long-stay alternative.'),
    ('Couples &amp; families', H[5], 'Simple, quiet, clean rooms with private options. Budget about €3 for linens.'),
    ('Sightseeing', H[8], 'At the start of Andrássy út, minutes from St. Stephen\'s Basilica and Deák tér.'),
    ('Small &amp; homely', H[9], 'Feels like a friend\'s loft in the Jewish Quarter, with hosts full of local tips.'),
]
picks_html = ''.join('<li><strong>%s:</strong> %s. %s</li>' % (lab, a(h), why) for lab, h, why in PICKS)

rows = ''.join(
    '<tr><td><a class="ltt-tbl-title" href="#%s">%d. %s</a></td><td>%s</td><td>%s</td><td>€%d</td><td>%.1f</td><td>%s</td><td>%s</td></tr>' % (
        h['id'], h['n'], h['name'], h['short'], h['area'], h['dorm'], h['hw'][0], h['noise'], h['watch']) for h in HOSTELS)

NEW_SECTIONS = '''<section id="best-hostel-by-traveler" style="margin-bottom: 50px;">
<div class="ltt-sec-header">
<span class="ltt-sec-badge">Quick Picks</span>
<h2 class="ltt-sec-title">Best Hostel in Budapest by Traveler Type</h2>
<p class="ltt-sec-subtitle">The short answer for each kind of trip, based on my stays</p>
</div>
<div class="w-richtext" style="margin-top: 16px;"><ul role="list">%s</ul></div>
</section>
<section id="hostels-side-by-side" style="margin-bottom: 50px;">
<div class="ltt-sec-header">
<span class="ltt-sec-badge">Side by Side</span>
<h2 class="ltt-sec-title">Budapest Hostels Compared: Price, Noise and Catches</h2>
<p class="ltt-sec-subtitle">Dorm prices and Hostelworld scores checked %s. Noise and catches from my own stays (The Hive: guest feedback).</p>
</div>
<div class="ltt-summary-table-wrap" style="margin-top: 16px;"><div class="ltt-table-scroll"><table class="ltt-summary-table">
<thead><tr><th>Hostel</th><th>Best for</th><th>Area</th><th>Dorms from</th><th>Hostelworld</th><th>Noise at night</th><th>Watch out for</th></tr></thead>
<tbody>%s</tbody></table></div></div>
</section>
<section id="where-to-stay-hostels" style="margin-bottom: 50px;">
<div class="ltt-sec-header">
<span class="ltt-sec-badge">Areas</span>
<h2 class="ltt-sec-title">Where to Stay in Budapest for Hostels</h2>
<p class="ltt-sec-subtitle">All 10 are in central Pest. The district decides how loud your nights are.</p>
</div>
<div class="w-richtext" style="margin-top: 16px;">
<h3>District VII (Jewish Quarter): for nightlife</h3>
<p>The ruin bars, Gozsdu Udvar and Szimpla Kert are here, and so are %s, %s and %s. Great for going out, <strong>worst for light sleepers</strong> on weekends.</p>
<h3>District VI (Király utca, Andrássy út, Oktogon): central and connected</h3>
<p>%s, %s and %s sit on the main boulevards with M1 and the 24 hour trams 4 and 6. Walkable to everything, but <strong>main-road traffic</strong> can be loud.</p>
<h3>District IX (Central Market Hall): calmer, by the river</h3>
<p>%s, %s and %s are next to the Central Market Hall, a few minutes from the Danube. My pick if you want <strong>quieter nights</strong> and still walk to the center.</p>
<p>Flying in? Here is <a href="/budapest-airport-to-city-center">how to get from the airport to the city center</a>: the 100E bus stops at Deák Ferenc tér, a short walk from the District VI and VII hostels.</p>
</div>
</section>
''' % (picks_html, CHECKED, rows, a(H[2]), a(H[9]), a(H[10]), a(H[6]), a(H[8]), a(H[3]), a(H[1]), a(H[4]), a(H[7]))

s = s.replace('<div class="ltt-editorial-wrapper">\n<section id="budapest-hostels-map"',
              '<div class="ltt-editorial-wrapper">\n' + NEW_SECTIONS + '<section id="budapest-hostels-map"', 1)
assert 'id="best-hostel-by-traveler"' in s

s = s.replace('<h2 class="ltt-sec-title">Map — Best Hostels in Budapest</h2>', '<h2 class="ltt-sec-title">Map: Best Hostels in Budapest</h2>')
s = s.replace("Explore all 10 verified hostels across Budapest's downtown districts",
              "The hostels on this list across Budapest's downtown districts")
s = s.replace('<h2 class="ltt-sec-title">Overview — Budapest Hostel Types</h2>', '<h2 class="ltt-sec-title">Budapest Hostel Types Explained</h2>')

# ---------------------------------------------------------------- FAQ
FAQ = [
    ('What is the best hostel in Budapest?',
     '<p><strong>Maverick Central Market</strong> is my best overall pick: social without party noise, curtained beds, great bathrooms and real long-stay value (I paid €280 for 30 nights in March). '
     'For a social trip pick <strong>Onefam Budapest</strong>; for the cheapest bed, <strong>Avenue Hostel</strong>.</p>'),
    ('What are the best hostels in Budapest for solo travelers?',
     '<p><strong>Onefam Budapest</strong> is the easiest place to make friends, with free daily activities and pub crawls, but it only takes guests aged <strong>18 to 39</strong>. '
     'Over 39, or want more sleep? <strong>Maverick Central Market</strong> and <strong>Wombat\'s City Hostel</strong> are social without the party pressure.</p>'),
    ('What are the best party hostels in Budapest?',
     '<p><strong>Onefam Budapest</strong> (social, daily bar crawls), <strong>The Hive Party Hostel</strong> (the big, loud one with a rooftop bar, strictly 18+) and '
     '<strong>Wombat\'s City Hostel</strong> (low-key party, quiet enough to sleep). All three are a short walk from the Jewish Quarter ruin bars.</p>'),
    ('Which Budapest hostels are best for a quiet night?',
     '<p><strong>Maverick Central Market</strong> (quiet side street), <strong>Central Market Hall Zen Hostel</strong> (small and homely) and <strong>a&amp;o Budapest City</strong> (hotel-style rooms). '
     'Avoid Avenue Hostel if you are a light sleeper: it\'s on the Oktogon tram junction.</p>'),
    ('How much does a hostel cost in Budapest?',
     '<p>On %s, dorm beds at these 10 hostels started at <strong>about €8 to €15 a night</strong> (Avenue from €8, Das Nest from €15), and private rooms from about €17 to €28. '
     'Prices rise on <strong>weekends, in summer (May to September), during Sziget Festival in August, the Christmas markets and New Year\'s Eve</strong>.</p>' % CHECKED),
    ('What is the best area to stay in Budapest for hostels?',
     '<p><strong>District VII (Jewish Quarter)</strong> for nightlife, <strong>District VI</strong> (Király utca, Andrássy út) for a central, well-connected base, and '
     '<strong>District IX</strong> by the Central Market Hall for quieter nights near the Danube.</p>'),
    ('Do Budapest hostels have age limits?',
     '<p>Some do. Per their house rules, <strong>Onefam Budapest takes guests aged 18 to 39</strong>, <strong>The Hive is strictly 18+</strong>, and <strong>Avenue Hostel accepts ages 6 to 49</strong>. Check the rules before you book.</p>'),
    ('Are hostels in Budapest safe?',
     '<p>Generally yes, but petty theft happens: I had a pullover and a box of nasal strips stolen at a hostel. <strong>Lock valuables in your locker</strong> and bring a padlock, since some hostels '
     '(Avenue, a&amp;o) don\'t include one. Flow Spaces gives you one for free.</p>'),
    ('What criteria did you use to choose the best hostels in Budapest?',
     '<p>I stayed in 9 of the 10 hostels and judged them on <strong>location, noise at night, cleanliness, bed comfort and privacy, facilities, the crowd and price</strong>. '
     'The Hive is included as a party pick based on checked facts and guest feedback, without a tested badge.</p>'),
    ('What should I bring with me to a hostel?',
     '<p><strong>Mandatory:</strong> earplugs and an eye mask. <strong>Basics:</strong> slippers, pajamas, phone charger, wet wipes, deodorant, toothbrush and toothpaste. '
     '<strong>Optional</strong> (check if your hostel includes them): towel, padlock, shampoo and shower gel.</p>'),
]


def faq_card(i, q, ans):
    first = ' first' if i == 0 else ''
    return ('<div class="cf-faq-plus-card">\n<div class="cf-faq-question-container-3%s">\n<div class="cf-faq-question-wrap">\n'
            '<h3 class="cf-faq-questions-2">%s</h3>\n<div class="cf-faq-icon-contain">\n<div class="cf-faq-line">\n</div>\n'
            '<div class="cf-faq-line-vertical">\n</div>\n</div>\n</div>\n</div>\n<div class="cf-faq-answer-wrap-2">\n'
            '<div class="cf-faq-content-2 w-richtext">%s</div>\n</div>\n<div class="cf-bottom-line-2">\n</div>\n</div>\n') % (first, q, ans)


fs = s.index('<div class="cf-faqs-container">')
fe = match_close(s, fs, 'div')
s = s[:fs] + '<div class="cf-faqs-container">\n' + ''.join(faq_card(i, q, a_) for i, (q, a_) in enumerate(FAQ)) + '</div>' + s[fe:]

# ---------------------------------------------------------------- sticky bar
s = re.sub(r'(<span class="hybrid-active-title" id="sticky-name">)[^<]*(</span>)', r'\g<1>%s\g<2>' % HOSTELS[0]['name'], s, count=1)
s = re.sub(r'(<span class="hybrid-active-price" id="sticky-price">)[^<]*(</span>)', r'\g<1>From €%d\g<2>' % HOSTELS[0]['dorm'], s, count=1)
s = s.replace('<span class="hybrid-active-trust">Free 24h Cancel</span>', '<span class="hybrid-active-trust">Dorm bed per night</span>')
s = re.sub(r'(id="sticky-cta-btn"[^>]*>)\s*Check Availability →', r'\1\n      Check Prices →', s, count=1)
s = s.replace('Jump to Tested Budapest Hostel', 'Jump to a Budapest Hostel')

# ---------------------------------------------------------------- JSON-LD
def strip(x):
    return re.sub(r'<[^>]+>', '', x).replace('&amp;', '&')

graph = [
    {"@type": "Article", "@id": URL + "#article",
     "mainEntityOfPage": {"@type": "WebPage", "@id": URL},
     "headline": TITLE, "description": META, "url": URL, "inLanguage": "en",
     "datePublished": "2022-12-28", "dateModified": CHECKED_ISO,
     "author": {"@type": "Person", "name": "Adam Dimitrov", "jobTitle": "Founder & Local Budapest Tester",
                "url": "https://www.budapestadventures.com/about"},
     "publisher": {"@type": "Organization", "name": "Budapest Adventures", "url": "https://www.budapestadventures.com",
                   "logo": {"@type": "ImageObject", "url": "https://www.budapestadventures.com/assets/budapest-adventures-logo.png"}},
     "image": ["https://www.budapestadventures.com/assets/cdn/60e43c7d6d05b671dff0dc1a/63aef937493ff750c5613e6a_Budapest-hostels-3.webp",
               "https://www.budapestadventures.com/assets/cdn/60e43c7d6d05b671dff0dc1a/64a94406fe5dca443dcfeee5_03-maverick-urban-lodge-roof-terrace-area.webp"],
     "mainEntity": {"@id": URL + "#list"}},
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.budapestadventures.com/"},
        {"@type": "ListItem", "position": 2, "name": "Best Hostels in Budapest", "item": URL}]},
    {"@type": "ItemList", "@id": URL + "#list", "name": TITLE, "itemListOrder": "https://schema.org/ItemListOrderAscending",
     "numberOfItems": len(HOSTELS),
     "itemListElement": [
         {"@type": "ListItem", "position": h['n'], "url": URL + '#' + h['id'],
          "item": {"@type": "Hostel", "name": strip(h['name']), "description": strip(h['best_for']),
                   "address": {"@type": "PostalAddress", "streetAddress": h['address'].split(', ')[0].replace(' (1st floor)', ''),
                               "postalCode": h['address'].split(', ')[-1].split(' ')[0], "addressLocality": "Budapest", "addressCountry": "HU"},
                   "priceRange": "From €%d per dorm bed" % h['dorm']}} for h in HOSTELS]},
    {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a_)}} for q, a_ in FAQ]},
]
ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)
js = s.index('<script id="ltt-schema-jsonld" type="application/ld+json">')
je = s.index('</script>', js)
s = s[:js] + '<script id="ltt-schema-jsonld" type="application/ld+json">\n' + ld + '\n' + s[je:]

s = re.sub(r'"shortTitles": \[[^\]]*\]',
           '"shortTitles": ' + json.dumps([strip(h['name']) for h in HOSTELS], ensure_ascii=False), s, count=1)
s = s.replace('"tocBreakdownLabel": "Detailed Breakdown (10 Hostels)"', '"tocBreakdownLabel": "Detailed Reviews (10 Hostels)"')

# ---------------------------------------------------------------- leftovers
assert 'Carpe' not in s.replace('carpe', ''), [m.start() for m in re.finditer('Carpe', s)][:5]
open(PAGE, 'w', encoding='utf-8').write(s)
print('ok', len(s))
