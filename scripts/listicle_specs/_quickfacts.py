# -*- coding: utf-8 -*-
"""Upgrade specs derived from a page's own "Quick Facts" tables (qf1-row label/value pairs in each
card's review section). Used for pages whose builders keep no per-card data file.

- the 5 questions travellers ask: one per quick fact, in a fixed priority (where, when, what is
  included, what is not, age, drinks, payment, ...), the cancellation line only as a filler;
- the price dropdown: the card's headline price, with the ticket/desk price facts as its note.
Every answer is a fact the page already shows.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

QUESTIONS = [
    (("Meeting Point",), "Where does it start?"),
    (("Pier",), "Which pier does it leave from?"),
    (("Address",), "Where is it?"),
    (("December 2026", "When", "Dates &amp; Times", "Nights", "Night Bathing", "Opening", "Opening Hours"), "When is it on?"),
    (("Included", "Includes"), "What is included?"),
    (("Not Included",), "What is not included?"),
    (("Drinks", "Drink Coupons"), "Which drinks are included?"),
    (("Age Limit",), "Is there an age limit?"),
    (("Children",), "Can children come?"),
    (("Duration", "Session"), "How long is it?"),
    (("Bar Payment", "Payment at Bars"), "How do I pay at the bars?"),
    (("Turkish Bath Rules",), "What are the Turkish bath rules?"),
    (("What Is Open", "Closed at Night"), "What is open at night?"),
    (("Pool Temperature",), "How warm are the pools?"),
    (("Bring", "Towels", "Towel &amp; Robe"), "What should I bring?"),
    (("Group Size",), "How big is the group?"),
    (("Fast Track",), "Can I skip the queue?"),
    (("Night Transport", "After Midnight"), "How do I get home at night?"),
    (("Nearest Transport",), "How do I get there?"),
    (("Accessibility",), "Is it accessible?"),
    (("Valid",), "How long is the ticket valid?"),
    (("Extras", "Supplement", "Extra Guests", "Cabin", "Entry"), "What costs extra?"),
    (("Desk Price 2026", "Desk Prices 2026", "Desk Price", "Weekday Prices", "Weekend Price", "Weekend Early Bird"),
     "How much is it at the desk?"),
]
PRICE_KEYS = ("Price", "Ticket Options", "Official Ticket Tiers", "Ticket (this card)", "Ticket", "Online Price",
              "Desk Price 2026", "Desk Prices 2026", "Desk Price", "Weekday Prices", "Weekend Price")


def sentence(v):
    v = v.strip()
    plain = re.sub(r"<[^>]+>", "", v).strip()
    if not plain:
        return v
    if v[0].islower():
        v = v[0].upper() + v[1:]
    return v if plain[-1] in ".!?" else v + "."


def quick_facts(src, anchor):
    a = src.find(f'id="{anchor}"')
    if a < 0:
        return []
    b = src.find('<details class="bpa-details-card"', a + 10)
    sec = src[a:b if b > 0 else len(src)]
    return [(l.strip(), v.strip()) for l, v in
            re.findall(r'<div class="qf1-label">(.*?)</div><div class="qf1-val">(.*?)</div>', sec, re.S)]


def faq_for(facts):
    d = dict(facts)
    out, used = [], set()
    for keys, q in QUESTIONS:
        for k in keys:
            if k in d and k not in used:
                out.append((q, sentence(d[k])))
                used.add(k)
                break
        if len(out) == 5:
            return out
    if "Cancellation" in d:
        out.append(("Can I cancel?", sentence(d["Cancellation"])))
    for k in PRICE_KEYS:
        if len(out) >= 5:
            break
        if k in d and k not in used:
            out.append(("How much is it?" if "Desk" not in k else "How much is it at the desk?", sentence(d[k])))
            used.add(k)
    return out[:5]


def build(page_file, anchors, noun, filters):
    """anchors: {card id: breakdown anchor}; filters: [{"label", "chips": [(cat, label)]}]."""
    src = open(os.path.join(ROOT, page_file), encoding="utf-8").read()
    cards = {}
    for cid, anchor in anchors.items():
        facts = quick_facts(src, anchor)
        faq = faq_for(facts)
        d = dict(facts)
        notes = [f"<b>{k}:</b> {d[k]}" for k in PRICE_KEYS if k in d][:2]
        cards[cid] = {"faq": faq, "price": {"note": " ".join(notes) or "Prices change by date; the final price shows before you pay."},
                      "_facts": len(facts)}
    page = {"noun": noun, "filter_aria": "Filter " + noun, "filters": filters}
    return page, cards


def anchors(page_file):
    """{card id: its "Read review" anchor} from the page's own cards."""
    src = open(os.path.join(ROOT, page_file), encoding="utf-8").read()
    out = {}
    starts = [(m.start(), m.group(1)) for m in re.finditer(r'<div class="bpa-card"[^>]*\bid="(card-\d+)"', src)]
    for i, (pos, cid) in enumerate(starts):
        end = starts[i + 1][0] if i + 1 < len(starts) else len(src)
        m = re.search(r'class="bpa-sublink"[^>]*href="#([^"]+)"', src[pos:end])
        if m:
            out[cid] = m.group(1)
    return out
