# Task: translate the hostels guide into 12 languages (translation only)

Branch: `content/hostels-legacy-12` (already pushed). Work only on this branch. Do not commit to `main`, do not merge, do not force-push.
Read `GEMINI.md` (HARD RULES) first.

## What you do

The English page `best-hostels-budapest.html` is the source. The page structure is built by a script. **Your only job is translation.**

Languages: `it nl pt pl ro sk sr ru uk tr ja ko`

For each language `<lang>`:

1. Read `data/i18n/todo/best-hostels-budapest/<lang>.json`. It is `{ "<id>": "<english html>" }`, with 721 segments. The 12 files are identical.
2. Write `data/i18n/port/best-hostels-budapest/<lang>.json` as `{ "<id>": "<translated html>" }`:
   - Use **every id** from the todo file.
   - Change no ids and add no extra ones.
   - Write valid JSON in UTF-8.
3. Translation rules:
   - **Keep the HTML exactly.** Every tag, attribute, `href`, `class`, `id` and `data-*` stays identical, in the same order and number. Translate only the visible text, plus the values of `alt`, `title`, `aria-label` and `placeholder`.
   - **Do not touch** numbers, prices (€, Ft), ratings (9.2/10), review counts, times (15:00), dates as digits, URLs, `#anchors`, or emojis. You may change the number format to local conventions (decimal comma, thousands separator) only where it is plain text.
   - **Never translate brand, hostel, place or street names.** These stay exactly as written:
     - Maverick Central Market, Maverick Hostels, Onefam Budapest, Onefam, Avenue Hostel, Flow Spaces, a&amp;o Budapest City, a&amp;o Hostels, Wombat's City Hostel, Wombat's, Central Market Hall Zen Hostel, Zen Hostel, Adagio Hostel 2.0 Basilica, Adagio 2.0, Das Nest Budapest, Das Nest, The Hive Party Hostel, The Hive
     - Hostelworld, Booking.com, Budapest Adventures, Adam Dimitrov
     - Szimpla Kert, Gozsdu udvar, Sziget Festival
     - every Hungarian street and square name (Lónyay utca, Deák Ferenc tér, Oktogon, Király utca, Andrássy út, Fővám tér, Kálvin tér, Vámház körút ...)
     - metro and bus names (M1–M4, 100E)
     - Russian, Ukrainian and Serbian may transliterate city names (Будапешт, Будимпешта) but not hostel names.
   - **Serbian uses Cyrillic script**, like the existing page.
   - **Register:** informal "you" (tu / você / sen) is fine for IT, PT and TR. Use the polite or plural "you" for PL, RO, SK, SR, RU, UK and NL ("u"). Use polite です/ます for JA and 합니다/해요 polite style for KO. When in doubt, follow the register of the language's existing pages on the site.
   - **No em dash (—)** anywhere. Use a comma, colon or full stop.
   - **Never invent facts.** Translate only what is there:
     - Do not add "tested" claims.
     - The Hive must stay "not stayed in / no tested badge".
     - Keep the first-person voice ("I stayed in 9").
   - The title pattern must keep the meaning "10 Best Hostels in Budapest in 2026 (I Stayed in 9)".

## Then build and check (all must pass)

```bash
python3 scripts/port_page_i18n.py best-hostels-budapest.html --langs it,nl,pt,pl,ro,sk,sr,ru,uk,tr,ja,ko --cache-only
```

Each language must print `0 tag mismatches`. If one does not, fix those segments in your JSON and rerun.

```bash
python3 scripts/sync_layout.py
python3 scripts/sync_layout.py --check          # must exit 0
python3 scripts/fix_affiliate_rel.py --check    # must exit 0
grep -l "Carpe" */*/index.html                   # must print nothing for the 12 pages
git diff -U0 | grep '^+' | grep -c '—'           # must be 0
```

## Homepage cards (title change propagates)

In each `<lang>/index.html`, the hostel guide is linked 3 times (menu, mobile menu, guide card). The menu items come from sync_layout, so leave them alone.

Update **only** these two things to the new translated title "10 Best Hostels in Budapest (I Stayed in 9)" (no year, same as the EN homepage):

- the guide card's title text (`<h3>` inside the `hp-guide` / `ltt-guide-card` link to the hostels page);
- the matching `"name"` of the hostels entry in the homepage JSON-LD ItemList.

Card kicker or price text: if it says "tested" in a way that is now wrong, or shows a starting price, set it to the facts on the page (dorm beds from €8). Change nothing else on the homepage.

## Finish

1. Delete the folder `data/i18n/todo/` and this `handoff/` folder.
2. Commit with message `content(hostels): port hostel guide to IT, NL, PT, PL, RO, SK, SR, RU, UK, TR, JA, KO`.
3. Push, then open a PR to `main`. **Do not merge.**
4. In the PR body, list per language: segment count, tag mismatches (must be 0) and the final page title.
