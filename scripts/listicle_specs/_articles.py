# -*- coding: utf-8 -*-
"""Upgrade specs for the experience pages built by scripts/build_article.py.

Their facts already live in scripts/articles/<slug>.json, so the spec is derived from that file:
- the 5 questions travellers ask come from each item's quick facts (meeting point, what is included,
  what is not, languages, who it is not for, ...), in a fixed priority, topped up from the cons;
- the price dropdown shows the item's price (and the struck-through regular price when there is one);
- filters reuse the page's own filter list (cats are the item's existing `cat` words).
Nothing on these pages is personally tested, so no tested stamp.
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# fact label -> question, in the order they are used
QUESTIONS = [
    (("Meeting point", "Venue", "Location", "Address", "Pickup", "Pick-up"), "Where does it start?"),
    (("Included",), "What is included?"),
    (("Not included",), "What is not included?"),
    (("Not suitable for", "Minimum age", "Children", "Not allowed", "Rules"), "Who is it not for?"),
    (("Languages",), "Which languages?"),
    (("Group size", "Group"), "How big is the group?"),
    (("Duration", "Visit length", "Session", "When"), "How long is it?"),
    (("Bring", "What to bring"), "What should I bring?"),
    (("Dress code",), "Is there a dress code?"),
    (("Finish", "Ends at"), "Where does it end?"),
    (("Getting there",), "How do I get there?"),
    (("Temperature",), "How warm or cold is it?"),
    (("Validity",), "How long is the ticket valid?"),
    (("Vehicle",), "What do we ride in?"),
    (("Seating", "Tables"), "How is the seating?"),
    (("Dietary",), "Can I eat vegetarian or gluten-free?"),
    (("Performers", "Show", "Programmes", "Format"), "What is on the programme?"),
    (("Cancellation",), "Can I cancel?"),
]


# hotel pages (spec "kind": "hotels"): questions a hotel guest asks, in this order
HOTEL_QUESTIONS = [
    (("Location", "Address"), "Where exactly is it?"),
    (("Breakfast",), "Is breakfast included?"),
    (("Pool & spa", "Spa", "Pool"), "Is there a pool or spa?"),
    (("Check-in",), "What are the check-in and check-out times?"),
    (("Walk to", "Nearby"), "What is within walking distance?"),
    (("Airport", "Getting there"), "How do I get there from the airport?"),
    (("Parking",), "Is there parking?"),
    (("Good to know", "Rules", "Children", "Pets"), "Anything to know before booking?"),
    (("Cancellation",), "Can I cancel?"),
]


def sentence(v):
    v = v.strip()
    if not v:
        return v
    v = v[0].upper() + v[1:]
    return v if v[-1] in ".!?" else v + "."


def esc(v):
    return html.escape(v, quote=False)


def money(v):
    """Same rounding as build_article.py, so the dropdown matches the card's headline price."""
    v = float(v)
    return f"€{v:.0f}" if v >= 10 or v == int(v) else f"€{v:.2f}"


def faq_for(it, questions=None):
    facts = dict((k, v) for k, v in it.get("facts", []))
    if questions is not None:
        out = []
        for keys, q in questions:
            for k in keys:
                if k in facts:
                    out.append((q, esc(sentence(facts[k]))))
                    break
            if len(out) == 5:
                break
        return out
    out = []
    # the trust box already says the cancellation terms, and "English." alone is a weak answer:
    # those two only fill in when nothing better is left
    weak = []
    if facts.get("Languages", "").strip().rstrip(".") == "English":
        weak.append(("Which languages?", "English only."))
        facts.pop("Languages")
    if "Cancellation" in facts:
        weak.append(("Can I cancel?", esc(sentence(facts.pop("Cancellation")))))
    for keys, q in QUESTIONS:
        for k in keys:
            if k in facts:
                a = facts[k]
                if keys[0] == "Meeting point" and k in ("Pickup", "Pick-up"):
                    q2 = "Is there hotel pickup?"
                else:
                    q2 = q
                out.append((q2, esc(sentence(a))))
                break
        if len(out) == 5:
            return out
    cons = [c for c in it.get("cons", []) if c]
    if len(out) < 5 and cons:
        out.append(("What are the downsides?", esc(" ".join(sentence(c) for c in cons[:3]))))
    pros = [p for p in it.get("pros", []) if p]
    if len(out) < 5 and pros:
        out.append(("Why pick it?", esc(" ".join(sentence(c) for c in pros[:3]))))
    out += weak
    return out[:5]


def build(slug):
    d = json.load(open(os.path.join(ROOT, "scripts", "articles", slug + ".json"), encoding="utf-8"))
    page = {
        "noun": d.get("noun", "experiences"),
        "filter_aria": "Filter " + d.get("noun", "experiences"),
        "filters": [{"label": d.get("filter_group", "Type"), "chips": [(f["cat"], f["label"]) for f in d["filters"]]}],
    }
    cards = {}
    for n, it in enumerate(d["items"], 1):
        rows = [{"label": "Adult" if "person" in it.get("price_unit", "") else it.get("price_unit", "Price").capitalize(),
                 "small": esc(it.get("duration", "")), "price": money(it["price"])}]
        if it.get("price_was"):
            rows.append({"label": "Regular price", "price": f"<s>{money(it['price_was'])}</s>"})
        faq = faq_for(it, HOTEL_QUESTIONS if d.get("kind") == "hotels" else None)
        if len(faq) != 5:
            raise SystemExit(f"{slug} card-{n}: only {len(faq)} questions from its facts")
        cards[f"card-{n}"] = {
            "_title": it["title"],
            "faq": faq,
            "price": {"rows": rows,
                      "note": esc(sentence(it.get("cancel", "Prices change by date"))) + " The final price shows before you pay."},
        }
    return page, cards
