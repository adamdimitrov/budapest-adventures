#!/usr/bin/env python3
"""Fill light listicle cards up to the river cruise card: 6-8 pills in two rows.

Adds pills only from facts on the card's own GetYourGuide listing (scripts/data/gyg_facts.json,
read in the browser: duration, guide languages, wheelchair flag, "not suitable for", "not allowed",
group limit, private option, skip-the-line, pickup, and the included / not included tick and cross
marks). Existing pills stay word for word; a topic the card already covers is not added twice.
Order follows the river cruise card: time, languages, access & kids, the card's own pills, then
what's included, group size, queue, pickup.

    python3 scripts/fact_pills.py [--dry-run] <page.json> ...
    python3 scripts/listicle.py build <page>.html
"""
import html
import importlib.util
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACTS = os.path.join(ROOT, "scripts", "data", "gyg_facts.json")
MAX, MIN = 8, 6
YES, NO, ASK = '<span class="cd-yes">✓</span>', '<span class="cd-no">✕</span>', '<span class="cd-ask">ⓘ</span>'
LANG = {"English": "en", "German": "de", "French": "fr", "Spanish": "es", "Italian": "it", "Hungarian": "hu",
        "Portuguese": "pt", "Dutch": "nl", "Polish": "pl", "Russian": "ru", "Chinese": "zh", "Japanese": "ja",
        "Korean": "ko", "Hebrew": "he", "Czech": "cs", "Slovak": "sk", "Romanian": "ro", "Croatian": "hr",
        "Serbian": "sr", "Bulgarian": "bg", "Greek": "el", "Turkish": "tr", "Ukrainian": "uk", "Arabic": "ar",
        "Swedish": "sv", "Danish": "da", "Norwegian": "no", "Finnish": "fi", "Slovenian": "sl", "Vietnamese": "vi"}
E = lambda s: html.escape(s, quote=False)


def kit():
    spec = importlib.util.spec_from_file_location("kit_listicle", os.path.join(ROOT, "kit", "scripts", "listicle.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def text_of(p):
    s = p.get("label") or p.get("summary_html") or ""
    return html.unescape(re.sub(r"<[^>]+>", " ", s)) + " " + p.get("emoji", "")


def covers(pills):
    t = " ".join(text_of(p) for p in pills)
    cls = " ".join(p.get("cls", "") for p in pills)
    return {
        "time": "bpa-time" in cls or bool(re.search(r"🕒|⏱|\b\d+(\.\d+)?\s*(h|hr|hrs|hours?|min|mins|minutes)\b", t, re.I)),
        "lang": bool(re.search(r"🗣|🎧|English|languages?\b|guide in", t, re.I)),
        "access": "cd-access" in cls or bool(re.search(r"♿|🔞|\b1[0-9]\+|\b[5-9]\+|kids|children|wheelchair", t, re.I)),
        "group": bool(re.search(r"👥|\bmax\b|small group|private|people\b|guests\b", t, re.I)),
        "incl": bool(re.search(r"✅|included|includes", t, re.I)),
        "queue": bool(re.search(r"skip|fast.?track|queue", t, re.I)),
        "pickup": bool(re.search(r"pick.?up|transfer|🚐", t, re.I)),
    }


def pill(emoji, label, pop, kind="", langs=None):
    p = {"cls": "bpa-lang" + {"time": " bpa-time", "access": " cd-access", "": ""}[kind], "emoji": emoji,
         "label": E(label), "pop_html": pop}
    if langs:
        p["data"] = {"langs": langs}
    return p


def andlist(xs):
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def time_pill(f):
    d = f.get("dur", "")
    if d.startswith("Duration "):
        v = d[len("Duration "):].replace(" - ", "–")
        return pill("🕒", v, f"<strong>Duration:</strong> {E(v)}.", "time")
    if d.startswith("Valid "):
        return pill("🕒", d, f"<strong>{E(d)}.</strong> Pick your date and start time when you book.", "time")


def lang_pill(f):
    langs = [x.strip() for x in (f.get("lang") or "").split(",") if x.strip()]
    if not langs:
        return None
    g = f.get("g", "")
    codes = " ".join(LANG[x] for x in langs if x in LANG)
    if g.startswith("Audio guide"):
        lab = "Audio guide" if len(langs) == 1 else f"Audio guide, {len(langs)} languages"
        return pill("🎧", lab, f"<strong>Audio guide in</strong> {E(andlist(langs))}.", langs=codes)
    who = {"Instructor": "instructor", "Host or greeter": "host", "Driver": "driver"}.get(g, "guide")
    lab = f"{langs[0]} {who}" if len(langs) == 1 else f"{len(langs)} languages"
    lead = {"instructor": "Instructor speaks", "host": "Host speaks", "driver": "Driver speaks"}.get(who, "Live guide in")
    return pill("🗣️", lab, f"<strong>{lead}</strong> {E(andlist(langs))}.", langs=codes)


def access_pill(f):
    ns, na = f.get("ns") or [], f.get("na") or []
    notes, label = [], None
    kid = next((re.search(r"Children under (\d+)", x) for x in ns if re.search(r"Children under (\d+)", x)), None)
    if f.get("w"):
        notes.append(f"♿ <b>Wheelchair:</b> {YES} listed as wheelchair-accessible")
        label = "Wheelchair-friendly"
    elif any("Wheelchair users" in x for x in ns):
        notes.append(f"♿ <b>Wheelchair:</b> {NO} not suitable for wheelchair users")
        label = "Not step-free"
    elif any("mobility" in x.lower() for x in ns):
        notes.append(f"♿ <b>Wheelchair:</b> {NO} not suitable for people with mobility impairments")
        label = "Not step-free"
    if any("stroller" in x.lower() or "baby carriage" in x.lower() for x in na):
        notes.append(f"👶 <b>Stroller:</b> {NO} strollers not allowed")
    if kid:
        notes.append(f"🎟️ <b>Kids:</b> {NO} not suitable for children under {kid.group(1)}")
        label = f"{kid.group(1)}+ only"
    other = [x for x in ns if not re.search(r"Wheelchair users|Children under|mobility", x, re.I)]
    if other and notes:
        notes.append(f"⚠️ <b>Not suitable for:</b> {E(andlist([x[0].lower() + x[1:] for x in other[:4]]))}")
    if not notes:
        return None
    return {"cls": "bpa-lang cd-access", "emoji": "♿", "label": E(label or "Access & kids"),
            "pop_html": "".join(f'<span class="bpa-lang-note">{n}</span>' for n in notes)}


def incl_pill(f):
    y = [x for x in (f.get("y") or []) if len(x) <= 110]
    n = [x for x in (f.get("n") or []) if len(x) <= 110]
    if not y:
        return None
    pop = "<strong>Included:</strong> " + E("; ".join(y[:5])) + "."
    if n:
        pop += f'<span class="bpa-lang-note"><b>Not included:</b> {E("; ".join(n[:4]))}.</span>'
    return pill("✅", "What's included", pop)


def group_pill(f):
    if f.get("lim"):
        return pill("👥", f"Max {f['lim']} people", f"<strong>Small group,</strong> limited to {f['lim']} participants.")
    pv = f.get("priv") or ""
    if pv:
        return pill("🔒", "Private option" if "available" in pv.lower() else "Private tour", f"<strong>{E(pv.split(';')[0])}.</strong>")


def queue_pill(f):
    if f.get("skip"):
        return pill("🎟️", "Skip the ticket queue", "<strong>Skip the ticket queue:</strong> your entry is booked in advance.")


def pickup_pill(f):
    pk = (f.get("pick") or "").split(";")[0].strip()
    if pk:
        return pill("🚐", "Pickup available", "<strong>Pickup available</strong> on this listing: choose it when you book.")


def upgrade(card, f):
    old = card["pills"]
    has = covers(old)
    front = []
    for key, fn in (("time", time_pill), ("lang", lang_pill), ("access", access_pill)):
        if not has[key]:
            p = fn(f)
            if p:
                front.append(p)
    back = []
    for key, fn in (("incl", incl_pill), ("group", group_pill), ("queue", queue_pill), ("pickup", pickup_pill)):
        if not has[key]:
            p = fn(f)
            if p:
                back.append(p)
    # still short of two rows: split "what's included" into included / not included
    if len(old) + len(front) + len(back) < MIN and not has["incl"]:
        y = [x for x in (f.get("y") or []) if len(x) <= 110]
        n = [x for x in (f.get("n") or []) if len(x) <= 110]
        if y and n:
            back = [p for p in back if p.get("emoji") != "✅"]
            back.insert(0, pill("✅", "What's included", "<strong>Included:</strong> " + E("; ".join(y[:5])) + "."))
            back.insert(1, pill("➖", "Not included", "<strong>Not included:</strong> " + E("; ".join(n[:4])) + "."))
    room = MAX - len(old)
    if room <= 0:
        return old
    # front pills first (river order), then the back ones, within the 8 cap
    add_front = front[:room]
    add_back = back[:max(0, room - len(add_front))]
    return add_front + old + add_back


def gyg_path(card):
    m = re.match(r"https://www\.getyourguide\.com/([^?]+?)/?(\?|$)", card["cta"]["btn"]["url"])
    return m.group(1) if m else None


def main(argv):
    dry = "--dry-run" in argv
    pages = [a for a in argv if not a.startswith("--")]
    keys = ("dur", "g", "lang", "w", "lim", "priv", "skip", "pick", "ns", "stroller", "y", "n")
    facts = {}
    for k, v in json.load(open(FACTS)).items():
        if k.startswith("_"):
            continue
        f = dict(zip(keys, v))
        f["na"] = ["Baby strollers"] if f.pop("stroller") else []
        facts[k.replace("~", "budapest-l29/", 1)] = f
    K = kit()
    short = []
    for page in pages:
        d = json.load(open(page))
        for c in d["cards"]:
            path = gyg_path(c)
            f = facts.get(path) if path else None
            if not f or f.get("err"):
                if len(c["pills"]) < MIN:
                    short.append(f"{os.path.basename(page)} {c['id']}: {len(c['pills'])} pills, no listing facts")
                continue
            c["pills"] = upgrade(c, f)
            if len(c["pills"]) < MIN:
                short.append(f"{os.path.basename(page)} {c['id']}: {len(c['pills'])} pills after facts")
        if not dry:
            open(page, "w").write(K.dumps(d) + "\n")
        print(os.path.basename(page), [len(c["pills"]) for c in d["cards"]])
    if short:
        print("\nstill under 6:\n  " + "\n  ".join(short))


if __name__ == "__main__":
    main(sys.argv[1:])
