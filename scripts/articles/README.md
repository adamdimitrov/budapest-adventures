# Article specs (`scripts/articles/<slug>.json`)

`python3 scripts/build_article.py --photos scripts/articles/<slug>.json` downloads the gallery photos
(AVIF, `assets/<slug>/`) and writes `<slug>.html` inside the shell of
`best-day-trips-from-budapest.html` (all CSS, menu, footer, runtime JS come from there).

```jsonc
{
  "slug": "best-water-parks-dubai",
  "cmp": "water_parks_dubai",                 // GYG cmp tag
  "title_tag": "7 Best Water Parks in Dubai (2026): Prices Compared",   // ≤ 60 chars, no em dash, no OTA names
  "meta_description": "…",                   // 110-160 chars, buying intent, no review totals, no OTA names
  "h1": "7 Best Water Parks in Dubai (2026)",  // used in JSON-LD
  "h1_main": "7 Best Water Parks in Dubai in 2026",
  "h1_muted": "(Compared Side by Side)",
  "breadcrumb": "Best Water Parks in Dubai",
  "kicker_badge": "✓ 2026 Side-by-Side Comparison",
  "author_role": "7 water parks compared on price, rides, transfers and fast-track",  // no "tested" unless true
  "lead": ["<strong>…</strong> html paragraph", "…"],     // G&C intro: answer the buying question first
  "filter_all_label": "All Parks",
  "filters": [{"cat": "family", "label": "👨‍👩‍👧 Families"}],   // counts are computed
  "breakdown_title": "Detailed Breakdown: 7 Best Water Parks in Dubai",
  "things": "Water Parks",                    // sticky bar: "All 7 Water Parks"
  "sheet_label": "a Dubai Water Park",
  "items": [{
    "rank_tag": "🏆 #1 Best Overall", "rank_class": "bpa-gold",   // bpa-gold | bpa-silver | bpa-bronze | bpa-accent
    "cat": "family thrill",                   // space-separated filter cats
    "operator": "Atlantis Aquaventure", "duration": "Full day", "place": "Atlantis, The Palm", "map_q": "Aquaventure Waterpark Dubai",
    "title": "…", "short_title": "…",         // short_title ≤ 45 chars (sticky bar, buy card)
    "link": "/dubai-l173/…-t570397/",        // GYG path; partner/cmp/mkt_cmp are added by the builder
    "rating": 4.52, "reviews": 14152, "price": 76.54, "price_was": null, "price_unit": "per person",
    "gallery": ["<64-hex>.jpg", …],           // GYG activityImage ids, 9-10; builder fills "photos"
    "photo_slug": "aquaventure",
    "pills": [                                // 6-8 pills = two full rows, same order as the river cruise cards:
      {"kind": "time", "emoji": "🕒", "label": "4 starts · 10:00–18:00", "lead": "Start times:", "body": "…"},
      {"emoji": "🗣️", "label": "English guide", "lead": "Languages:", "body": "…"},
      {"kind": "access", "emoji": "♿", "label": "Access & kids", "lead": "Access:", "body": "♿ Wheelchair: … 👶 Stroller: … 🎟️ Kids: …"},
      {"emoji": "🎢", "label": "105 slides", "lead": "What's inside:", "body": "…", "note": "optional source note"},
      {"kind": "vibe", "emoji": "🙂", "label": "Calm, small group", "lead": "What it feels like:", "body": "…"},
      {"emoji": "👥", "label": "Max 12 people", "lead": "Group size:", "body": "…"}
    ],                                        // each pill is a dropdown whose body adds facts not in its label; the builder stops on <6 or >8
    "pick": "for … (specific)", "skip": "if … (specific)",
    "pros": ["…"], "cons": ["…"],
    "review": ["html paragraph", "…"],        // original analysis, no invented experience
    "facts": [["Meeting point", "…"], ["Included", "…"], ["Not included", "…"], ["Languages", "…"], ["Cancellation", "…"]],
    "trust": ["Free cancellation up to 24 hours before", "Mobile ticket"],
    "cancel": "Free cancellation up to 24 hours before"
  }],
  "guide": [{"id": "compare", "h2": "…", "html": "<p>…</p><div class=\"ltt-guide-tablewrap\"><table>…</table></div>"}],
  "faqs": [{"q": "…", "a": "html"}],
  "methodology": "<p>…</p>"
}
```
