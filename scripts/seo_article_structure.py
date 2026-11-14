#!/usr/bin/env python3
"""Fix the heading outline of a comparison article and expose its comparison deck to crawlers.

Language-independent part (safe on every translation):
  * cruise titles (h3.bpa-details-title) become H2
  * review sub-points (h4 inside .ltt-sp-card) become H3, Quick Facts titles become H3
  * UI labels that are not content (buy-card title, drawer and modal titles) stop being headings
  * em dashes in the changed headings become colons
  * a crawlable <table> summary of the comparison deck is added inside <details>, under an H2

Usage: python3 scripts/seo_article_structure.py FILE [FILE ...] --lang en
"""
import argparse
import html
import re
import sys
from html.parser import HTMLParser

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}

LABELS = {
    'en': {
        'h2': 'Budapest {topic} Compared: Price, Duration and Departure Dock',
        'summary': 'Compare all {n} at a glance (table)',
        'caption': '{n} best {topic_lc} in Budapest compared ({month})',
        'cols': ['#', 'Cruise', 'Operator', 'Duration', 'Departs from', 'Price from'],
        'review': 'review',
    },
}


class Scan(HTMLParser):
    """Records every element's start/end offset with its ancestor classes."""

    def __init__(self, src):
        super().__init__(convert_charrefs=False)
        self.src = src
        self.stack = []
        self.elems = []
        self.line_starts = [0] + [m.end() for m in re.finditer('\n', src)]

    def _off(self):
        line, col = self.getpos()
        return self.line_starts[line - 1] + col

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        start = self._off()
        end_of_start = self.src.index('>', start) + 1
        el = {'tag': tag, 'cls': a.get('class') or '', 'id': a.get('id') or '', 'start': start,
              'sopen': end_of_start, 'anc': [x['cls'] for x in self.stack], 'end': None}
        self.elems.append(el)
        if tag not in VOID:
            self.stack.append(el)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID and self.stack and self.stack[-1]['tag'] == tag:
            self.stack.pop()

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]['tag'] == tag:
                off = self._off()
                self.stack[i]['end'] = self.src.index('>', off) + 1
                del self.stack[i:]
                return


def scan(src):
    p = Scan(src)
    p.feed(src)
    return p.elems


def in_cls(el, name):
    return any(name in c.split() for c in el['anc'])


def retag(src, el, new_tag, add_cls=None, text_fix=None):
    """Return (start, end, replacement) for one element."""
    seg = src[el['start']:el['end']]
    old = el['tag']
    open_tag = src[el['start']:el['sopen']]
    inner = seg[len(open_tag):-len('</%s>' % old)]
    new_open = '<' + new_tag + open_tag[1 + len(old):]
    if add_cls:
        if 'class="' in new_open:
            new_open = new_open.replace('class="', 'class="%s ' % add_cls, 1)
        else:
            new_open = new_open[:-1] + ' class="%s">' % add_cls
    if text_fix:
        inner = text_fix(inner)
    return el['start'], el['end'], new_open + inner + '</%s>' % new_tag


def dash_to_colon(s):
    return s.replace(' — ', ': ').replace(' &mdash; ', ': ')


def heading_edits(src):
    edits = []
    for el in scan(src):
        t, cls = el['tag'], el['cls'].split()
        if el['end'] is None:
            continue
        if t == 'h3' and 'bpa-details-title' in cls:
            edits.append(retag(src, el, 'h2', text_fix=dash_to_colon))
        elif t == 'h4' and not cls and in_cls(el, 'ltt-sp-card'):
            edits.append(retag(src, el, 'h3', add_cls='ltt-sp-title'))
        elif t == 'h4' and 'qf1-title' in cls:
            edits.append(retag(src, el, 'h3', text_fix=dash_to_colon))
        elif t == 'h4' and 'ltt-buy-card-title' in cls:
            edits.append(retag(src, el, 'div'))
        elif t == 'h2' and 'bpa-breakdown-heading' in cls:
            edits.append(retag(src, el, 'h2', text_fix=dash_to_colon))
    return edits


def apply(src, edits):
    for start, end, rep in sorted(edits, key=lambda e: e[0], reverse=True):
        src = src[:start] + rep + src[end:]
    return src


def text(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s)).strip()


def deck_rows(src):
    rows = []
    for m in re.finditer(r'<div class="bpa-card"[^>]*>', src):
        nxt = src.find('<div class="bpa-card"', m.end())
        card = src[m.start(): nxt if nxt > 0 else m.start() + 80000]
        g = lambda p: (re.search(p, card, re.S) or [None, ''])[1]
        kicker = [k.strip() for k in text(g(r'class="bpa-kicker">(.*?)</div>')).split('•')]
        kicker = [re.sub(r'^[^\w€]+', '', k).strip() for k in kicker]
        rows.append({
            'title': dash_to_colon(text(g(r'class="bpa-title"[^>]*>(.*?)</a>'))),
            'operator': kicker[0] if kicker else '',
            'duration': kicker[1] if len(kicker) > 1 else '',
            'dock': kicker[2] if len(kicker) > 2 else '',
            'price': re.sub(r'^From\s+', '', text(g(r'class="bpa-price">(.*?)</div>'))),
            'anchor': g(r'href="(#cruise-[^"]*)"'),
        })
    return rows


TABLE_CSS = """<style id="bpa-compare-table-css">
.bpa-compare-h2{font-size:13px!important;font-weight:800!important;letter-spacing:.08em!important;text-transform:uppercase!important;color:#855a00!important;margin:0 0 10px!important;line-height:1.35!important;font-family:inherit!important;text-align:left!important}
.bpa-compare-more{display:block;width:100%;max-width:1240px;min-width:0;margin:4px auto 28px;padding:0 16px;box-sizing:border-box;overflow:hidden}
.bpa-compare-more>*{min-width:0;max-width:100%}
@media(max-width:600px){.bpa-compare-tbl th,.bpa-compare-tbl td{padding:9px 10px}.bpa-compare-tbl tbody th{min-width:180px}}
.bpa-compare-more>summary{cursor:pointer;font-weight:700;font-size:14px;color:#0f172a;padding:10px 0;list-style:revert}
.bpa-compare-scroll{width:100%;max-width:100%;overflow-x:auto;-webkit-overflow-scrolling:touch;border:1px solid #e2e8f0;border-radius:12px;background:#fff}
.bpa-compare-tbl{width:100%;border-collapse:collapse;font-size:13.5px;line-height:1.4;text-align:left}
.bpa-compare-tbl caption{caption-side:top;text-align:left;font-size:12px;color:#64748b;padding:10px 14px 0}
.bpa-compare-tbl th{background:#f8fafc;color:#475569;font-size:11.5px;font-weight:700;text-transform:uppercase;letter-spacing:.04em;padding:10px 14px;border-bottom:1px solid #e2e8f0;white-space:nowrap}
.bpa-compare-tbl tbody th{background:none;color:#1e293b;font-size:13.5px;font-weight:600;text-transform:none;letter-spacing:0;white-space:normal;border-bottom:1px solid #f1f5f9}
.bpa-compare-tbl tr:last-child th{border-bottom:0}
.bpa-compare-tbl td{padding:10px 14px;border-bottom:1px solid #f1f5f9;vertical-align:top;color:#1e293b}
.bpa-compare-tbl td:first-child,.bpa-compare-tbl td:nth-child(4),.bpa-compare-tbl td:last-child{white-space:nowrap}
.bpa-compare-tbl tr:last-child td{border-bottom:0}
.bpa-compare-tbl a{color:#0f172a;font-weight:600;text-decoration:underline;text-decoration-color:#dfa732;text-underline-offset:2px}
</style>"""


def table_block(rows, lab, topic, month):
    n = len(rows)
    head = ''.join('<th scope="col">%s</th>' % html.escape(c) for c in lab['cols'])
    body = []
    for i, r in enumerate(rows, 1):
        name = html.escape(r['title'])
        cell = '<a href="%s">%s</a>' % (r['anchor'], name) if r['anchor'] else name
        body.append('<tr><td>%d</td><th scope="row">%s</th><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
            i, cell, html.escape(r['operator']), html.escape(r['duration']), html.escape(r['dock']), html.escape(r['price'])))
    caption = lab['caption'].format(n=n, topic_lc=topic.lower(), month=month)
    return ('<details class="bpa-compare-more"><summary>%s</summary><div class="bpa-compare-scroll">'
            '<table class="bpa-compare-tbl"><caption>%s</caption><thead><tr>%s</tr></thead><tbody>%s</tbody></table>'
            '</div></details>') % (html.escape(lab['summary'].format(n=n)), html.escape(caption), head, ''.join(body))


def add_compare(src, lab, topic, month):
    if 'bpa-compare-tbl' in src:
        return src
    rows = deck_rows(src)
    if not rows:
        return src
    els = scan(src)
    deck = next(e for e in els if e['tag'] == 'div' and 'comparison-table' in e['cls'].split())
    filt = next((e for e in els if e['tag'] == 'div' and 'ltt-integrated-filter-bar' in e['cls'].split()), None)
    h2 = '<h2 class="bpa-compare-h2" id="comparison">%s</h2>' % html.escape(lab['h2'].format(topic=topic))
    out = src[:deck['end']] + table_block(rows, lab, topic, month) + src[deck['end']:]
    pos = filt['start'] if filt else deck['start']
    out = out[:pos] + h2 + out[pos:]
    return out.replace('</head>', TABLE_CSS + '</head>', 1)


def css_compat(src):
    """Rules written for the old h4 sub-points also style the new h3.ltt-sp-title."""
    def fix(m):
        return m.group(0).replace('.ltt-sp-card h4', '.ltt-sp-card :is(h4,h3.ltt-sp-title)')
    src = re.sub(r'<style[^>]*>.*?</style>', fix, src, flags=re.S)
    if 'id="bpa-heading-compat"' not in src:
        # cruise titles were h3; keep generic "h2" rules (e.g. .content-right_blog h2) from restyling them
        compat = ('<style id="bpa-heading-compat">.content-right_blog h2.bpa-details-title,h2.bpa-details-title'
                  '{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif!important}</style>')
        src = src.replace('</head>', compat + '</head>', 1)
    return src


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('files', nargs='+')
    ap.add_argument('--lang', default='en')
    ap.add_argument('--topic', required=True, help='e.g. "River Cruises" (in the page language)')
    ap.add_argument('--month', default='November 2026')
    a = ap.parse_args()
    lab = LABELS[a.lang]
    for f in a.files:
        src = open(f, encoding='utf-8').read()
        out = css_compat(apply(src, heading_edits(src)))
        out = add_compare(out, lab, a.topic, a.month)
        if out != src:
            open(f, 'w', encoding='utf-8').write(out)
            print('updated', f)
        else:
            print('unchanged', f)


if __name__ == '__main__':
    sys.exit(main())
