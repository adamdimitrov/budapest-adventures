#!/usr/bin/env python3
"""Build the redesigned group booking page from the live one.

Keeps the live page's head scripts, menu and footer, swaps the SEO meta and
replaces the body content with scripts/group_booking/content.html.

    python3 scripts/build_group_booking_test.py          # -> budapest-river-cruise-group-booking-test.html (noindex)
    python3 scripts/build_group_booking_test.py --live   # overwrite the live page
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "budapest-river-cruise-group-booking.html"
CONTENT = ROOT / "scripts/group_booking/content.html"
URL = "https://www.budapestadventures.com/budapest-river-cruise-group-booking"

TITLE = "Budapest River Cruise Group Booking | Free Same-Day Quote"
DESC = ("Planning a Danube cruise for 20 to 250+ people? Send your date and headcount "
        "and get a free same-day quote for dinner, sightseeing or private boats.")
OG_IMG = ("https://www.budapestadventures.com/assets/cdn/60e43c7d6d05b671dff0dc1a/"
          "6482365138e2c970cdc10bc0_1-Best-River-Cruises-Budapest.webp")


def faq_schema(content: str) -> str:
    items = re.findall(r"<details[^>]*><summary>(.*?)</summary><p>(.*?)</p></details>", content, re.S)
    strip = lambda s: re.sub(r"<[^>]+>", "", s).replace("&amp;", "&").strip()
    data = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": strip(q),
                 "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in items]},
            {"@type": "Service", "name": "Budapest river cruise group booking",
             "serviceType": "Group cruise booking", "url": URL,
             "areaServed": {"@type": "City", "name": "Budapest"},
             "provider": {"@type": "Organization", "name": "Budapest Adventures",
                          "url": "https://www.budapestadventures.com/"},
             "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR",
                        "description": "Free group quote, no booking fee"}},
        ],
    }
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>"


def build(live: bool) -> Path:
    h = SRC.read_text()
    content = CONTENT.read_text()
    assert "—" not in content, "em dash in content"

    h = re.sub(r"<title>[^<]*</title>", f"<title>{TITLE}</title>", h, count=1)
    head_meta = (
        f'<meta content="{DESC}" name="description"/>'
        f'<meta content="{DESC}" property="og:description"/>'
        f'<meta content="{OG_IMG}" property="og:image"/>'
        f'<meta content="{DESC}" name="twitter:description"/>'
        f'<meta content="summary_large_image" name="twitter:card"/>'
    )
    if not live:
        head_meta = '<meta name="robots" content="noindex, nofollow"/>' + head_meta
    # drop any old copies, then insert after <title>
    h = re.sub(r'<meta content="[^"]*" (name="description"|property="og:description"|property="og:image"|'
               r'name="twitter:description"|name="twitter:card")/>', "", h)
    h = h.replace(f"<title>{TITLE}</title>", f"<title>{TITLE}</title>{head_meta}", 1)
    h = re.sub(r'<meta content="[^"]*" (property="og:title"|name="twitter:title")/>',
               lambda m: f'<meta content="{TITLE}" {m.group(1)}/>', h)
    if 'rel="canonical"' not in h:
        h = h.replace("</title>", f'</title><link href="{URL}" rel="canonical"/>', 1)
    h = re.sub(r'<script type="application/ld\+json" id="gb-schema">.*?</script>', "", h, flags=re.S)
    h = h.replace("</head>", faq_schema(content).replace("<script ", '<script id="gb-schema" ', 1) + "</head>", 1)

    # old Webflow content, or our own block when rebuilding an already-converted page
    marker = '<div class="hero-image-wrapper">' if '<div class="hero-image-wrapper">' in h else "<style>\n.gb{"
    start = h.index(marker)
    end = h.index('<footer class="footer-dark ltt-footer"')
    h = h[:start] + content + h[end:]

    out = SRC if live else ROOT / "budapest-river-cruise-group-booking-test.html"
    out.write_text(h)
    return out


if __name__ == "__main__":
    print("wrote", build("--live" in sys.argv).relative_to(ROOT))
