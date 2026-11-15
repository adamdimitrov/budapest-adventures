"""Copy rules for the thermal baths pages (hub + child pages).

No self-evident "checked on <date>" lines (user rule, 15 Nov 2026): the "Last updated" pill
already shows the date. A date stays only where it adds information (prices for a given day,
a closure date) and in the methodology section, which this pass never touches.
"""
import re

RULES = [
    # author line and sticky bar
    (r" • (?:Hours &amp; )?Prices (?:Updated|Checked) \d{1,2} Nov 2026", ""),
    (r'<span class="hybrid-active-trust">Prices checked \d{1,2} Nov 2026</span>', ""),
    # intros
    (r" Prices and opening hours are up to date as of \d{1,2} November 2026\.", ""),
    (r" Opening hours, desk prices and pool temperatures are <strong>up to date as of \d{1,2} November 2026</strong>\.", ""),
    # "tested" popovers
    (r" Every price, hour and (?:pool )?temperature (?:on this card )?was rechecked on [^<]*? on \d{1,2} November 2026\.", ""),
    # pill notes
    (r"Checked on the official site on \d{1,2} November 2026; hours change by season and holidays\.",
     "Hours change by season and on holidays."),
    (r"Checked on the booking calendar for ((?:Mon|Tues|Wednes|Thurs|Fri|Satur|Sun)day \d{1,2} November 2026)\.",
     r"Prices for \1."),
    (r"(From [^<,;]+?), (?:checked )?\d{1,2} November 2026([.;])", r"\1\2"),
    # Quick Facts
    (r" \(checked \d{1,2} Nov 2026\)", ""),
    (r'<p class="qf1-note"[^>]*>Checked on the official site and the live listings on \d{1,2} November 2026\. '
     r'Only what the source confirms is shown\.</p>', ""),
    # hub body
    (r"Every bath below was checked on its official site on \d{1,2} November 2026\. Each one suits",
     "Each bath below suits"),
    (r" Both were checked on their official sites on \d{1,2} November 2026, so they are not in this list\.",
     " Neither is in this list."),
    (r" \(official sites, \d{1,2} November 2026\)", ""),
    # meta / JSON-LD descriptions
    (r", updated \d{1,2} Nov 2026\.", "."),
]


def apply(page):
    for pat, rep in RULES:
        page = re.sub(pat, rep, page)
    return page
