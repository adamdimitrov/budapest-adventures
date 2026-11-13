#!/usr/bin/env python3
"""Refresh ratings, review counts and prices on /best-walking-tours-budapest.

Figures read on 2026-11-13:
- GetYourGuide: each product page's structured data (aggregateRating, offers)
- Viator / Tripadvisor: Mysterium Tours vampire tour (Viator d499-135788P1,
  supplier "Mysterium Tours (Budapest)"; Tripadvisor listing of the same tour)
- GuruWalk: each walk page's structured data

Card 6 (Cityrama, GYG t739): the Viator/Tripadvisor badges are removed, the
Cityrama listing there is a different product (with Parliament visit).

Idempotent per run on the original page only (old figures are anchors).
"""
import base64
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "best-walking-tours-budapest.html"
GURU_ICON = Path(sys.argv[1]) if len(sys.argv) > 1 else None  # 32px GuruWalk favicon PNG

# (old score, old count) -> (new score, new count)
BADGES = {
    ("4.7", "750"): ("4.6", "4630"),    # vampire, GetYourGuide 4.64 (4,639)
    ("5.0", "470"): ("4.5", "1500"),    # vampire, Viator 4.5 (1,505)
    ("5.0", "270"): ("4.7", "700"),     # vampire, Tripadvisor 4.7 (708)
    ("4.7", "1230"): ("4.6", "8020"),   # caves, GetYourGuide 4.63 (8,024)
    ("4.9", "3780"): ("4.9", "3050"),   # Jewish Quarter, GuruWalk 4.86 (3,059)
    ("4.9", "3830"): ("4.9", "10870"),  # inner city, GuruWalk 4.89 (10,875)
    ("4.5", "630"): ("4.6", "2410"),    # castle, GetYourGuide 4.58 (2,417)
    ("4.3", "910"): ("4.4", "1150"),    # city tour, GetYourGuide 4.4 (1,157)
}
REMOVE_COUNTS = ("120", "110")          # city tour Viator / Tripadvisor (unmatched product)
GURU_COUNTS = ("3050", "10870")         # badges that are GuruWalk, not Tripadvisor

# price text per product (old -> new), only in that product's own phrases
PRICES = [("€22", "€18"), ("€13", "€17"), ("€29", "€35")]
PRICE_10 = [("From €10", "From €12"), ("Verified Pricing €10 / person", "Verified Pricing €12 / person"),
            ('<div class="qf1-val">€10 / person</div>', '<div class="qf1-val">€12 / person</div>')]

# JSON-LD Product blocks: brand -> (ratingValue, reviewCount, price)
LD = {
    "Mysterium Tours": ("4.6", "4639", "18"),
    "Danube-Ipoly": ("4.6", "8024", "16.97"),
    "BudapestTours": ("4.9", "3059", "0"),
    "GoZeppelin Tours": ("4.9", "10875", "0"),
    "Tourist Angel": ("4.6", "2417", "12"),
    "Cityrama": ("4.4", "1157", "35"),
}

FULL = '<path d="M11.9999 18.26L4.94691 22.208L6.52191 14.28L0.586914 8.792L8.61391 7.84L11.9999 0.5L15.3859 7.84L23.4129 8.792L17.4779 14.28L19.0529 22.208L11.9999 18.26Z"'
HALF_START = '<path d="M11.9999 15.968L16.2469'


def badge_span(s, count):
    """Yield (start, end) of each badge element whose count is (+count reviews)."""
    for m in re.finditer(re.escape(f"(+{count} reviews)"), s):
        a = max(s.rfind('<a class="bpa-rev-badge"', 0, m.start()), s.rfind('<span class="bpa-rev-badge', 0, m.start()))
        tag = "a" if s.startswith("<a", a) else "span"
        e = s.find(f"</{tag}>", m.end()) + len(f"</{tag}>")
        yield a, e


def stars_for(score, html):
    """Last star: full when score >= 4.8, half otherwise (page convention)."""
    svgs = list(re.finditer(r"<svg.*?</svg>", html, re.S))
    if len(svgs) != 5:
        return html
    last = svgs[-1]
    body = last.group(0)
    want_full = float(score) >= 4.8
    if want_full and HALF_START in body:
        body = re.sub(r'<path d="[^"]+"', FULL, body, count=1)
    elif not want_full and HALF_START not in body:
        half = re.search(r'<path d="M11\.9999 15\.968L16\.2469[^"]+"', PAGE_TEXT).group(0)
        body = re.sub(r'<path d="[^"]+"', half, body, count=1)
    return html[:last.start()] + body + html[last.end():]


def main():
    global PAGE_TEXT
    s = PAGE.read_text()
    PAGE_TEXT = s
    assert "(+750 reviews)" in s, "already refreshed?"

    for (old_sc, old_n), (sc, n) in BADGES.items():
        spans = list(badge_span(s, old_n))
        assert spans, old_n
        for a, e in reversed(spans):
            b = s[a:e]
            b = b.replace(f'<span class="bpa-rev-score">{old_sc}</span>', f'<span class="bpa-rev-score">{sc}</span>', 1)
            b = b.replace(f"(+{old_n} reviews)", f"(+{n} reviews)")
            b = stars_for(sc, b)
            if GURU_ICON and n in GURU_COUNTS:
                data = "data:image/png;base64," + base64.b64encode(GURU_ICON.read_bytes()).decode()
                b = re.sub(r'(<img alt=")[^"]*(" class="bpa-rev-icon"[^>]*src=")[^"]+(")', r"\g<1>GuruWalk\g<2>" + data + r"\3", b, count=1)
            s = s[:a] + b + s[e:]

    for n in REMOVE_COUNTS:
        spans = list(badge_span(s, n))
        assert spans, n
        for a, e in reversed(spans):
            s = s[:a] + s[e:]

    for old, new in PRICES:
        s = s.replace(old, new)
    for old, new in PRICE_10:
        s = s.replace(old, new)

    for brand, (rv, rc, price) in LD.items():
        pat = re.compile(r'("brand":\{"@type":"Organization","name":"%s"\},"aggregateRating":\{"@type":"AggregateRating","ratingValue":")[^"]+(","bestRating":"5","worstRating":"1","reviewCount":")[^"]+("\},"offers":\{"@type":"Offer","price":")[^"]+(")' % re.escape(brand))
        s, k = pat.subn(lambda m: m.group(1) + rv + m.group(2) + rc + m.group(3) + price + m.group(4), s)
        assert k >= 1, brand

    PAGE.write_text(s)
    print("refreshed", PAGE.name)


if __name__ == "__main__":
    main()
