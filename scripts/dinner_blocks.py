"""Helpers to cut balanced card / details blocks out of the cruise listicle pages (shared by the dinner rebuild)."""
import re


def balanced(html, start, tag):
    """Return the end index of the element of type `tag` that opens at `start`."""
    pat = re.compile(r"<(/?)%s\b[^>]*>" % tag)
    depth = 0
    for m in pat.finditer(html, start):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return m.end()
    raise ValueError("unbalanced %s at %d" % (tag, start))


def deck_card(html, card_id):
    m = re.search(r'<div class="bpa-card"[^>]*id="%s"[^>]*>' % re.escape(card_id), html)
    return html[m.start():balanced(html, m.start(), "div")]


def details_card(html, det_id):
    m = re.search(r'<details class="bpa-details-card"[^>]*id="%s"[^>]*>' % re.escape(det_id), html)
    return html[m.start():balanced(html, m.start(), "details")]


def all_spans(html, kind):
    """(start, end) of every deck card ('card') or details card ('details') in order."""
    if kind == "card":
        pat, tag = r'<div class="bpa-card"[^>]*id="card-\d+"[^>]*>', "div"
    else:
        pat, tag = r'<details class="bpa-details-card"[^>]*>', "details"
    return [(m.start(), balanced(html, m.start(), tag)) for m in re.finditer(pat, html)]
