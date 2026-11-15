#!/usr/bin/env python3
"""SEO + copy pass on /best-walking-tours-budapest (EN), 2026-11-14.

GSC (Aug 13 to Nov 12 2026): avg position 36, 5.4K impressions, 0.2% CTR.
Largest query clusters: "free walking tour budapest" (~1,000 impr. across
variants) and "walking tour budapest" (~770). Changes:
- shorter title, real meta description (old one was 330 chars of filler)
- G&C intro, removes the false "street eats" claim (no food tour on the page)
- two new H2 sections: quick picks + how free walking tours work
- specific "Best For" line per card instead of the template sentence
- fact fixes: vampire quick-facts price (card says from EUR 18),
  inner city meeting point (Kossuth Lajos ter per the review, not Vorosmarty ter)
- FAQ: 3 -> 6 questions, FAQPage + ItemList JSON-LD
"""
import json
import re
from pathlib import Path

PAGE = Path(__file__).resolve().parent.parent / "best-walking-tours-budapest.html"
URL = "https://www.budapestadventures.com/best-walking-tours-budapest"

OLD_TITLE = "The 6 Best Free and Paid Walking Tours in Budapest in 2026 (Personally Tested)"
NEW_TITLE = "6 Best Walking Tours in Budapest (Free & Paid, Tested 2026)"
OLD_H1 = "The 6 Best Free and Paid Walking Tours in Budapest in 2026"
NEW_H1 = "The 6 Best Walking Tours in Budapest in 2026: Free and Paid"
OLD_DESC = ("Explore the best 6 walking tours in Budapest, personally tested by a local. Whether you're "
            "intrigued by history, passionate about culture, or simply seeking a compelling introduction "
            "to the city, we've curated the ultimate list of walking tour experiences to immerse you in "
            "Budapest's unique charm and rich character.")
NEW_DESC = ("I took 6 Budapest walking tours myself: 2 free tip-based walks, the castle caves, "
            "a night vampire walk and more. Paid tours from €12, and who each one suits.")

INTRO_OLD = re.compile(r'<div class="ltt-lead-copy">.*?</div>', re.S)
INTRO_NEW = """<div class="ltt-lead-copy">
<p>One long city tour sounds efficient, but Budapest's best walks are short and specific: <strong>the Castle District after dark, the caves underneath it, and the Jewish Quarter's wartime history</strong>. I took six of the city's most popular walking tours myself, two of them free (you tip the guide at the end).</p>
<p>Below they are side by side on what decides the booking: <strong>price (free to €35)</strong>, length (1.5 to 3 hours), where you meet and who each one suits. Only have one slot? Do the <strong>free Inner City walk on your first morning</strong> and the <strong>Night Vampire tour for an evening</strong>.</p>
<p>Prices and departure times checked on 13 November 2026.</p>
</div>"""

BEST_FOR = {
    "Night Vampire Walking Tour in Buda Castle District":
        ("2-hour", "An evening with a story: Castle District legends by lantern light, starting 19:45 or 20:00. Ages 10+."),
    "Buda Castle Cave Labyrinth Walking Tour":
        ("1.5-hour", "Rainy days and families (ages 3+): 1.5 hours in the natural caves under Castle Hill."),
    "Best Jewish Quarter Walking Tour":
        ("2.5-hour", "History lovers who want the full WWII story, free and on flat streets. Heavy for young kids."),
    "Best Budapest Inner City Walking Tour":
        ("2.25-hour", "Your first morning in Budapest: Parliament to the Danube in 2.25 hours, free, all ages."),
    "Best Buda Castle District Walking Tour":
        ("2-hour", "Castle Hill by day on a budget: Matthias Church and Fisherman's Bastion for €12."),
    "Grand City Tour of Budapest":
        ("3-hour", "One morning, the whole city: coach plus short walks from Heroes' Square to Castle Hill."),
}

ANCHORS = ["#item-1-vampire-walking-tour", "#item-2-buda-cave-tour", "#item-3-ww2-jewish-quarter-tour",
           "#item-4-pest-walking-tour", "#item-5-buda-castle-walking-tour", "#item-6-budapest-grand-city-tour"]

GUIDE_ANCHOR = '<div class="content-right_blog" id="content"><div class="container-33 w-container">'
GUIDE = """
<div class="w-richtext bpa-wt-guide">
<h2 id="which-walking-tour">Which Budapest Walking Tour Should You Book?</h2>
<ul>
<li><strong>First day, want the big picture:</strong> <a href="#item-4-pest-walking-tour">Inner City walk</a> (free, 2.25 hours, Parliament to the Danube).</li>
<li><strong>History, especially WWII:</strong> <a href="#item-3-ww2-jewish-quarter-tour">Jewish Quarter walk</a> (free, 2.5 hours, ends at the Dohány Street Synagogue).</li>
<li><strong>Something to do in the evening:</strong> <a href="#item-1-vampire-walking-tour">Night Vampire tour</a> (from €18, 2 hours, starts 19:45 or 20:00).</li>
<li><strong>Rain, or kids aged 3+:</strong> <a href="#item-2-buda-cave-tour">Cave Labyrinth tour</a> (from €17, 1.5 hours underground).</li>
<li><strong>Castle Hill by day for little money:</strong> <a href="#item-5-buda-castle-walking-tour">Buda Castle District tour</a> (€12, 2 hours).</li>
<li><strong>Only one morning and tired legs:</strong> <a href="#item-6-budapest-grand-city-tour">Grand City Tour</a> (€35, 3 hours, coach plus walks).</li>
</ul>
<h2 id="free-walking-tours-budapest">Free Walking Tours in Budapest: How They Work</h2>
<p>Two of the six are <strong>free, tip-based walks</strong>: the Inner City tour (English daily at 10:00, meeting at Kossuth Lajos tér by the Parliament) and the Jewish Quarter tour (English at 11:00 and 15:00, meeting at Madách Imre tér). You reserve a free spot online, walk with the group and <strong>pay the guide what you think the tour was worth at the end</strong>. Most people give <strong>€10 to €20 per person</strong>, in cash.</p>
<p>Free does not mean worse. Both free walks were among the best guiding I had in Budapest. The trade-off is group size (20 to 30 people on my Jewish Quarter walk) and that everything happens outdoors. Paid tours take you where a free walk can't: <strong>into the cave labyrinth under Castle Hill</strong>, or up to the castle at night with a story-led guide.</p>
</div>
"""

FAQ_OLD = re.compile(r'<h2 id="faq-dup2">Frequently Asked Questions</h2>.*?(?=<div class="ltt-filmstrip-wrap">)', re.S)
FAQS = [
    ("What is the best walking tour in Budapest?",
     "For a first visit, the <strong>free Inner City walk</strong> gives the best overview: Parliament, Liberty Square, "
     "St. Stephen's Basilica and the Danube promenade in 2.25 hours. For an evening, the <strong>Night Vampire tour</strong> "
     "in the Castle District was my favourite of the six."),
    ("Are free walking tours in Budapest really free?",
     "Booking is free and nobody checks a ticket. At the end you <strong>tip the guide what the tour was worth to you</strong>. "
     "The guides earn their living from these tips, so plan to pay something."),
    ("How much do you tip a free walking tour guide in Budapest?",
     "A common tip is <strong>€10 to €20 per person</strong>, usually in cash. Some people give more for an exceptionally "
     "informative and entertaining guide."),
    ("How much is a walking tour in Budapest?",
     "Free walks cost only your tip. The paid group walks on this list run from <strong>€12 (Buda Castle District)</strong> "
     "to <strong>€35 (Grand City Tour with coach)</strong>, with the Cave Labyrinth from €17 and the Night Vampire tour from €18. "
     "Private tours cost more."),
    ("Can you do a walking tour in Budapest at night?",
     "Yes. The <strong>Night Vampire tour</strong> starts at 19:45 or 20:00 in English and spends 2 hours in the lit-up "
     "Castle District, past Matthias Church and Fisherman's Bastion."),
    ("Can you walk around Buda Castle for free?",
     "Yes, you can walk around the <strong>exterior grounds of Buda Castle for free</strong>. This includes several courtyards "
     "and terraces that offer stunning views of Budapest. However, to access the interior of the castle, including the "
     "Budapest History Museum and the Hungarian National Gallery, <strong>there is an admission fee</strong>."),
]


def faq_html():
    out = ['<h2 id="faq-dup2">Frequently Asked Questions</h2>']
    for q, a in FAQS:
        out.append(f'<h3 class="cf-faq-questions-2">{q}</h3><div class="cf-faq-answer-wrap-2">'
                   f'<div class="cf-faq-content-2 w-richtext"><p>{a}</p></div></div>')
    return "".join(out)


def strip(t):
    return re.sub(r"<[^>]+>", "", t)


def sub1(s, old, new, count=1):
    n = s.count(old)
    assert n >= count, (old[:80], n)
    return s.replace(old, new)


def main():
    s = PAGE.read_text()
    assert OLD_TITLE in s, "already applied?"

    s = sub1(s, f"<title>{OLD_TITLE}</title>", f"<title>{NEW_TITLE}</title>")
    s = sub1(s, f'content="{OLD_TITLE}"', f'content="{NEW_TITLE}"', 2)  # og + twitter
    s = sub1(s, f'content="{OLD_DESC}"', f'content="{NEW_DESC}"', 3)    # description, og, twitter
    s = sub1(s, f"{OLD_H1} <span", f"{NEW_H1} <span")
    s = sub1(s, '<span class="ltt-h1-muted">(PERSONALLY TESTED)</span>', '<span class="ltt-h1-muted">(Personally Tested)</span>')
    s = sub1(s, f'<span class="ltt-bc-current">{OLD_H1}</span>', '<span class="ltt-bc-current">The 6 Best Walking Tours in Budapest in 2026</span>')

    s, n = INTRO_OLD.subn(INTRO_NEW, s, count=1)
    assert n == 1

    for name, (dur, line) in BEST_FOR.items():
        s = sub1(s, f"Best For:</strong> Travelers looking for a verified {dur} experience with {name}.",
                 f"Best For:</strong> {line}")

    s = sub1(s, "<strong>Last updated</strong>: Nov 13, 2026", "<strong>Last updated</strong>: Nov 14, 2026")

    # fact fixes
    s = sub1(s, '<div class="qf1-val">€21–22 / person</div>', '<div class="qf1-val">From €18 / person</div>')
    s = sub1(s, "Vörösmarty+tér", "Kossuth+Lajos+tér")
    s = sub1(s, "Vörösmarty tér", "Kossuth Lajos tér")

    s = sub1(s, GUIDE_ANCHOR, GUIDE_ANCHOR + GUIDE)
    s, n = FAQ_OLD.subn(faq_html(), s, count=1)
    assert n == 1

    # JSON-LD
    m = re.search(r'(<script id="ltt-schema-jsonld" type="application/ld\+json">)(.*?)(</script>)', s, re.S)
    data = json.loads(m.group(2))
    graph = [n for n in data["@graph"] if n["@type"] not in ("FAQPage", "ItemList")]
    for node in graph:
        if node["@type"] == "Article":
            node["headline"] = f"{NEW_H1} (Personally Tested)"
            node["description"] = NEW_DESC
            node["dateModified"] = "2026-11-14"
            lst = node["mainEntity"]  # existing ItemList of the 6 tours (ratings, offers)
            lst["name"] = f"{NEW_H1} (Personally Tested)"
            lst["description"] = strip(INTRO_NEW).replace("\n", " ").strip()
            for el in lst["itemListElement"]:
                prod = el["item"]
                prod["description"] = BEST_FOR[prod["name"]][1]
        if node["@type"] == "BreadcrumbList":
            node["itemListElement"][-1]["name"] = "The 6 Best Walking Tours in Budapest in 2026"
    graph.append({
        "@type": "FAQPage", "@id": f"{URL}#faq",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in FAQS],
    })
    data["@graph"] = graph
    s = s[:m.start(2)] + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + s[m.end(2):]

    assert "—" not in s
    PAGE.write_text(s)
    print("ok")


if __name__ == "__main__":
    main()

# Applied once after main() on 2026-11-14: each Product review.reviewBody in the
# JSON-LD ItemList was replaced with that card's own "Should You Go?" verdict
# (the old value was the "Travelers looking for a verified ..." template).
