"""Shared "Budapest bath guides" navigation for the thermal baths hub and its child pages.

Used by the hub (/thermal-baths-budapest) and /szechenyi-baths-budapest; the Rudas and Sparty
pages may import it too. One place to change the list of bath guides.
A guide is linked only once its page exists in the checkout (live()), so re-run the hub and
Széchenyi builders after the Rudas or Sparty page is merged.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def live(href):
    """True when the page exists in this checkout. Guides from other open PRs stay unlinked until merged."""
    slug = href.strip("/")
    return not slug or os.path.exists(os.path.join(ROOT, slug + ".html")) or os.path.exists(os.path.join(ROOT, slug, "index.html"))


def guides():
    return [g for g in GUIDES if live(g[1])]

GUIDES = [
    ("hub", "/thermal-baths-budapest", "♨️", "All Budapest Thermal Baths",
     "6 open baths compared: prices, pools, crowds"),
    ("szechenyi", "/szechenyi-baths-budapest", "🏛️", "Széchenyi Baths Tickets",
     "Day ticket from €39, locker vs cabin, VIP and Beer Spa"),
    ("rudas", "/rudas-baths-budapest", "🕌", "Rudas Baths Tickets",
     "Turkish bath, rooftop pool, weekend night bathing"),
    ("sparty", "/sparty-budapest", "🎉", "Sparty Budapest",
     "Saturday night pool party at Széchenyi, from €73"),
]

CSS = ('<style id="bpa-hubnav-css">.bpa-hubnav{margin:8px 0 28px;padding:18px 18px 14px;border:1px solid #e2e8f0;'
       'border-radius:16px;background:#fafbfc}.bpa-hubnav-title{font-size:12px;font-weight:800;letter-spacing:1px;'
       'text-transform:uppercase;color:#855a00;margin:0 0 12px}.bpa-hubnav-grid{display:grid;'
       'grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px}.bpa-hubnav a.bpa-hubnav-item{display:flex;'
       'gap:10px;align-items:flex-start;padding:12px 14px;border:1px solid #e2e8f0;border-radius:12px;background:#fff;'
       'text-decoration:none!important;color:#0f172a!important;min-width:0}.bpa-hubnav a.bpa-hubnav-item:hover{'
       'border-color:#dfa732}.bpa-hubnav-item.is-current{border-color:#0f172a;box-shadow:inset 0 0 0 1px #0f172a}'
       '.bpa-hubnav-ico{font-size:20px;line-height:1.2}.bpa-hubnav-name{display:block;font-size:14.5px;font-weight:700;'
       'line-height:1.3}.bpa-hubnav-sub{display:block;font-size:12.5px;color:#64748b;line-height:1.35;margin-top:2px}'
       '</style>')

START = '<nav aria-label="Budapest bath guides" class="bpa-hubnav" id="bpa-hubnav">'


def block(current, title="Budapest Bath Guides"):
    items = []
    for key, href, ico, name, sub in guides():
        cur = key == current
        items.append('<a class="bpa-hubnav-item%s" href="%s"%s><span class="bpa-hubnav-ico" aria-hidden="true">%s</span>'
                     '<span><span class="bpa-hubnav-name">%s</span><span class="bpa-hubnav-sub">%s</span></span></a>'
                     % (" is-current" if cur else "", href, ' aria-current="page"' if cur else "", ico, name, sub))
    return '%s<p class="bpa-hubnav-title">%s</p><div class="bpa-hubnav-grid">%s</div></nav>\n' % (START, title, "".join(items))


def strip(page):
    return re.sub(re.escape(START) + r".*?</nav>\n?", "", page, flags=re.S)


def ensure_css(page):
    page = re.sub(r'<style id="bpa-hubnav-css">.*?</style>', "", page, flags=re.S)
    return page.replace("</head>", CSS + "\n</head>", 1)
