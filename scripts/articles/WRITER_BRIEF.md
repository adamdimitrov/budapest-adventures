# Writer brief: one budapestadventures.com "best X in Budapest" article

Repo (worktree): `/Users/adamdimitrov/Development/bpa-experiences`. Work ONLY on your own files:
`scripts/articles/<slug>.json`, `assets/<slug>/`, `<slug>.html`. Do not edit menus, homepage, sitemap, other pages, the builder or the shell. Do not commit, push or use git. No browser needed.

## Inputs
- Harvested live GetYourGuide data (read today, 2026-11-16): `scripts/articles/harvest/<topic>.json`, a list of products: `id`, `p` (GYG path), `name`, `rating`, `reviews` (either may be missing = new listing), `price` (EUR from-price), `desc`, `gallery` (image ids), `text` (listing text: cancellation, duration, languages, highlights, description, includes, meeting point, sometimes review snippets).
- Spec format: `scripts/articles/README.md`. `rating`/`reviews` may be `null` for listings without reviews; the builder then shows "New listing".
- Look of a finished page: `best-day-trips-from-budapest.html` (the builder uses its shell) and `best-walking-tours-budapest.html`.
- Copy style: read `~/.claude/skills/growandconvert-content/SKILL.md` and follow it.

## Steps
1. Read your harvest file. Drop products that duplicate another (same thing sold twice) unless the difference matters; keep 5-9 genuinely different options. Rank them honestly (best overall first, then distinct "best for" picks).
2. Write `scripts/articles/<slug>.json`. Use only facts present in the harvest data. If a fact (meeting point, what's included, languages) is not in the data, leave it out. Never invent.
3. Build: `python3 scripts/build_article.py --photos scripts/articles/<slug>.json`
4. QC: `python3 ~/.claude/skills/qc-article/qc_article.py --site-dir . --page <slug>.html`. Fix every FAIL except the `[wiring]` ones (sitemap/menu/homepage/inbound links are done later by the orchestrator). A photo-count warning is fine when the listing itself has fewer than 9 photos. Rebuild and re-run until only wiring fails remain. Aim for 2+ internal links OUT of the guide copy (see "Links").
5. Re-read your built page's text once as a strict editor (rules below) and fix anything off.
6. Final message: slug, number of cards, a table (rank, product id, title, price, rating/reviews), anything you dropped and why, and any rule you could not satisfy.

## Content rules (hard)
- Title tag ≤ 60 chars, like "9 Best Wine Tastings in Budapest (2026): Prices Compared". Meta 110-160 chars. No em dashes (—) anywhere: use commas, colons, periods. En dash only in ranges (12–25 minutes, €45–60).
- Never say tested / personally tested / I tried / we tried / field-tested / undercover. The user has not done these activities. The value is the side-by-side comparison. author_role example: "9 wine tastings compared on wines poured, food, price per glass and group size".
- No OTA names (GetYourGuide, Viator, Tripadvisor, Tiqets) and no review totals in title, meta, h1, lead. No "GetYourGuide showed…", no "only N spots left", no "checked on the booking calendar", no "prices checked on <date>", no "to keep this honest", no "based on listings", no apologies or self-undermining disclaimers. Card buttons/badges already name the booking site; that's fine.
- Brand, venue, operator and ship names stay in their original form (Dohány Street Synagogue, Matthias Church, Memento Park, MonsteRoller).
- Lead (2-4 short paragraphs): answer the buying question immediately (which one to book for whom, with a concrete number, and a link to that card's anchor `#item-1-<kebab of short_title>`), then what decides it. No "Budapest is a city of…" openers. No AI tells: delve, whether you're, in the heart of, unforgettable, nestled, look no further, embark, tapestry, elevate, hidden gem, must-see.
- Every card: specific `pick` ("for … because …") and `skip` ("if …"); 6-8 pills (two full rows, like the Legenda card on best-budapest-river-cruises), in this order: 🕒 start times/duration (`"kind": "time"`), 🗣️ languages, ♿ access & kids (`"kind": "access"`: wheelchair, stroller, minimum age, child price), 2-4 pills on what you actually get (inclusions, highlights, group size, food/drinks, transport), then the vibe (`"kind": "vibe"`: calm, lively, hands-on, who you share it with). Each pill is a dropdown and its `body` must add facts not in its label (label "8 wines" → body: which regions/grapes, pour size, what food comes with it). `pros`/`cons` 3-5 each, concrete.
- `review`: 2-4 paragraphs of original analysis per product: what you actually get for the money, how it differs from the neighbours, who it suits, catches (extras, timing, meeting point). Facts only from the data. Never base a claim on a single guest review.
- "Includes" and "Not included" often run together in `text`: never claim something is included unless it clearly sits on the included side.
- `guide` (mandatory, this is the page's value): at least
  1. a side-by-side comparison table (`<div class="ltt-guide-tablewrap"><table>…</table></div>`) on the real decision axes for this topic, with computed numbers (price per hour, price per wine/gun/shot, group size, private vs shared, what's included);
  2. "Which one should you book?" decision section;
  3. a practical section (best time, what to bring, how to get there, what costs extra) using only data you have.
- `faqs`: 5-7 real buyer questions with direct answers.
- `methodology`: short, positive: what was compared (number of options, the axes, live listing prices for a normal date). No apologies.
- `filters`: 3-5 buyer-intent filters with emoji labels, `cat` values used on items.
- rank_class: #1 bpa-gold, #2 bpa-silver, #3 bpa-bronze, rest bpa-accent. rank_tag like "🏆 #1 Best Overall", "🥈 #2 Best Value", "🥉 #3 Best Small Group".
- `photo_slug`: short kebab of the product. `short_title` ≤ 45 chars. `cmp`: the slug without "best-" using underscores is fine (e.g. "wine_tasting_budapest").
- `price_unit`: "per person" unless the listing is per group (then e.g. "per group up to 3").
- `trust`: only what the listing states ("Free cancellation up to 24 hours before", "Reserve now, pay later", "Hotel pickup").
- `map_q`: the meeting point or venue + "Budapest".

## Links (internal, in guide/faq copy as `<a href="/slug">anchor</a>`)
Live pages: `/best-walking-tours-budapest`, `/best-food-tours-budapest`, `/best-pub-crawls-budapest`, `/best-day-trips-from-budapest`, `/best-budapest-river-cruises`, `/best-dinner-cruises-budapest`, `/best-night-cruises-budapest`, `/best-private-boat-tours-budapest`, `/unlimited-prosecco-cruises-budapest`, `/thermal-baths-budapest`, `/sparty-budapest`, `/best-hop-on-hop-off-bus-budapest`, `/budapest-card-is-it-worth-it`, `/budapest-parliament-tickets`, `/best-things-to-do-budapest`, `/budapest-travel-guide`, `/best-hostels-budapest`.
Also live (batch 1): `/best-wine-tasting-budapest`, `/best-bike-tours-budapest`, `/best-shooting-ranges-budapest`, `/best-cave-tours-budapest`, `/best-concerts-budapest`, `/best-jewish-quarter-tours-budapest`, `/best-buda-castle-tours`, `/best-cooking-classes-budapest`, `/best-communist-tours-budapest`, `/best-helicopter-tours-budapest`.
Sibling pages publishing in this batch: `/best-things-to-do-budapest-with-kids`, `/best-vienna-day-trips-from-budapest`.

## Tiqets items
A harvest item with `"platform": "tiqets"` is booked on Tiqets: in the spec set `"platform": "tiqets"`, `"link"` = its full `p` URL (the builder adds the partner parameter), and `"gallery"` = its full image URLs (the builder downloads them). Its badge and button then name Tiqets automatically.
