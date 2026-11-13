# Statistics Articles: Playbook for AI Agents

Read this file in full before you write, translate or edit any statistics article on budapestadventures.com
(for example "Budapest tourism statistics", "Budapest hotel statistics", "Danube cruise statistics").

The reference implementation is `budapest-tourism-statistics.html` (EN) and `hu/budapest-turizmus-statisztika/index.html` (HU).
Copy that file as the starting point for every new statistics page. Do not invent a new layout.

## 1. Hard rules (a page that breaks any of these is not done)

1. **No em dashes (`—`) anywhere**: body copy, headings, `<title>`, meta description, JSON-LD, alt text, chart labels.
   Use a comma, a colon, a full stop or parentheses instead. An en dash is only allowed in number ranges (`2021–2025`).
   The owner considers em dashes an AI giveaway. Check with: `grep -n '—' <file>` (must return nothing).
2. **Every number needs a source you actually opened.** Never write a figure from memory or "general knowledge".
   For each figure, record the source URL and table ID (for example `ksh.hu/stadat_files/tur/en/tur0081.html`, table 27.1.1.20).
   If you cannot open the source, leave the figure out and say so to the user. Do not estimate or "round to look nice".
3. **Prefer primary sources** in this order: KSH (Hungarian Central Statistical Office), MNB, Eurostat,
   Budapest Airport, BFTK / Budapest Festival and Tourism Centre, operator-published figures.
   Secondary sources (Statista, news articles, blogs) are only allowed when no primary source exists, and must be labelled as such.
4. **Say what the data does not cover.** If KSH only publishes a series for Hungary and not Budapest, write that plainly
   (the reference page does this for spending and source countries). Never present a national figure as a Budapest figure.
5. **Math must check out.** Recompute every percentage change, share and average from the raw numbers before publishing.
   Example: if arrivals went from 4.10M to 4.68M, the change is +14.1%, not "about 15%".
6. **Never translate brand names**: Budapest Adventures, Legenda, Viator, GetYourGuide, Tripadvisor, ship names, venue names.
7. **Do not touch** `GEMINI.md` business sections, `ratings.json`, affiliate links or partner IDs while working on a stats page.
8. **Tone**: neutral, factual, data-journalism style. No hype ("amazing", "breathtaking", "unforgettable"),
   no filler intros ("In today's fast-paced world..."). The first sentence under each H2 answers the question in the H2 with a number.

## 2. Page structure (match the reference page)

1. Header (menu) and footer: identical to the reference page. Copy them verbatim. Do not restyle, add CTAs or change links.
   Standards: dropdown labelled "Explore" (HU: "Felfedezés"), full 22-language switcher,
   no "Top 10 Cruises" button, footer = five cruise pages (river, dinner, night, prosecco, private boat tours) + About + Contact.
   If `scripts/sync_layout.py` exists on your branch, run `python3 scripts/sync_layout.py --langs en,hu` before finishing;
   `--check` must report no drift.
2. H1 with the year, for example "Budapest Hotel Statistics 2026: ...". Kicker line like "KSH Data · 2021 to 2025".
3. Author block (`ltt-author-*` classes), same author as the reference page, with "Updated" date = today.
4. "Key ... statistics (YEAR)" summary box: 5 to 8 bullet points, each one number + one short sentence.
5. Table of contents (`.toc` / `.tocitem`) linking every H2.
6. H2s phrased as the questions people search for ("How many ...", "When do ...", "Where do ...", "How much ...").
   Under each: a 1 to 2 sentence direct answer, then a chart, then 1 to 3 short paragraphs of context.
7. Charts: inline SVG inside a `.bpa-chart` block (`.bpa-chart-head`, `.bpa-chart-title`, `.bpa-chart-sub`),
   each followed by a `<details>` element containing an HTML `<table>` with the exact numbers behind the chart
   and a source line. No external chart libraries, no images of charts. Charts must be readable at 375px width.
8. "Sources and methodology" section at the end: every source with link, table ID, date accessed,
   and notes on definitions (for example "commercial accommodation only, excludes Airbnb").
9. Where it fits naturally, one or two internal links to the cruise money pages. No ad-style blocks inside the data sections.

## 3. SEO and technical checklist

- `<title>` under 60 characters, meta description 140 to 160 characters, both without em dashes.
- `<link rel="canonical">` pointing to the production URL of this page.
- hreflang `alternate` links for EN and HU (and `x-default` to EN) on both language versions.
- JSON-LD: `Article` (headline, datePublished, dateModified = today, author `Person`, publisher `Organization`),
  copied from the reference page and updated. Add `Dataset` only if you publish a full data table.
- Every `<img>` has a descriptive `alt`. New images: `.webp`, under 150 KB, in `assets/`.
- Add the new URL to `sitemap.xml` (both languages).
- No console errors, no horizontal scroll on mobile (375px), all TOC links jump to the right section.

## 4. Other languages

The EN page is the source for the other 20 languages. After changing it, run
`python3 scripts/build_stats_i18n.py extract`, translate the new or changed ids in
`data/i18n/stats/<lang>.json` (`check` lists them), then `build` and `python3 scripts/build_stats_embeds.py`.

## 5. Hungarian version

- Write the HU page as a native Hungarian text, not a word-for-word translation. Numbers use Hungarian format
  (`4,68 millió`, `14,2%`, space as thousands separator: `1 234 567`).
- HU URL lives under `hu/<hungarian-slug>/index.html`. Keep the same charts and tables, translate labels and the source notes.
- Brand names stay in their original form (see rule 6).

## 6. Workflow

1. Work on a new branch in a git worktree, never directly on `main` and never in a checkout another session is using.
2. Collect the data first: build a small table (figure, value, unit, period, source URL, table ID) and show it to the user
   before writing the article. The user approves the data, then you write.
3. Write EN, then HU.
4. Self-check before handing over:
   - `grep -n '—' <files>` returns nothing
   - every number in the text appears in a chart table or the sources section
   - all percentages recomputed
   - mobile layout checked at 375px
5. Commit, push the branch, open a PR to `main`. Give the user the Vercel preview URL of the new page(s).
   Do not merge without the user's approval.
6. After the user merges: the user resubmits the sitemap and requests indexing in Google Search Console.
