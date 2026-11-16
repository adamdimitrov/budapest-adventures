"""Legenda booking links: every Legenda CTA goes straight to the ticket-purchase
(checkout) page in the page's language, with partner=38585 only (no subid).
Languages Legenda has no ticket page for fall back to English.

    from legenda_links import localize, ticket_url
    html = localize(html, lang)   # rewrites any Legenda home/product/ticket link
"""
import re

PARTNER = "38585"
TICKET_PATH = {
    "hu": "hu/jegyvasarlas",
    "en": "en/ticket-purchase",
    "fr": "fr/achat-de-tickets",
    "de": "de/ticketkauf",
    "it": "it/acquisto-dei-biglietti",
    "es": "es/venta-de-billetes",
    "ru": "ru/pokupka-biletov",
    "zh": "zh/gou-piao",
    "ja": "ja/tiketutogou-ru",
}

# Booking-type Legenda URLs: home page, product pages and ticket pages in any language,
# with any partner id and an optional subid. Info assets (menu PDFs, virtual tours) are left alone.
_SLUGS = "|".join(["candlelit-dinner-cruise", "danube-legend", "duna-bella"]
                  + [p.split("/", 1)[1] for p in TICKET_PATH.values()])
LEGENDA_BOOKING = re.compile(
    r"https?://(?:www\.)?legenda\.hu(?:/[a-z]{2}(?:/(?:%s))?)?/?\?partner=\d+(?:&(?:amp;)?subid=[\w-]+)?" % _SLUGS)


def ticket_url(lang):
    return "https://legenda.hu/%s?partner=%s" % (TICKET_PATH.get(lang, TICKET_PATH["en"]), PARTNER)


def localize(text, lang):
    url = ticket_url(lang)
    return LEGENDA_BOOKING.sub(lambda m: url, text)
