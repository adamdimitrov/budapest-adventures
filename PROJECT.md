# Project: Budapest Adventures Staging Architecture Overhaul

## Architecture
- **Staging Platform**: Dedicated branch `staging/static-overhaul`, configured for local Python-based preview and instant Vercel staging deployment. Live production DNS (`35.187.176.9` / Linguana / Webflow) remains 100% untouched.
- **Routing Engine**: Modern `vercel.json` using `cleanUrls: true`, `trailingSlash: false`, explicit `redirects` (HTTP 301 for pruned Linguana zombie routes, old slugs), `rewrites` (serving core HTML money hubs at clean semantic paths), and strict security headers.
- **Preview Engine**: Zero-dependency `preview_server.py` implementing exact `vercel.json` route resolution for instant local verification.
- **Tracking Pipeline**: `bpa-tracking.js` capturing UTMs, `gclid`, `fbclid`, and `_fbp` into dual cookies + localStorage, decorating outbound Legenda (`partner=38585` only, no subid), Silverline (`code=bpadventures` only) and Tiqets (`budapestadventures`) links, and firing Meta Pixel (`1355732169631751`) `InitiateCheckout` events with 25% net commission value.
- **SEO & Canonical Architecture**: Strict semantic HTML5 IDs, zero `#` fragments in canonical tags, self-referencing canonicals pointing to clean root URLs, and `sitemap.xml` strictly indexing canonical URLs across the 21 GSC active traffic languages (`en`, `hu`, `ro`, `ja`, `it`, `fr`, `pl`, `cs`, `hr`, `ru`, `el`, `bg`, `es`, `sr`, `he`, `pt`, `sk`, `tr`, `uk`, `de`, `ko`).

## Code Layout
- HTML Money Hubs:
  - `index.html` (Danube River Cruises Main Hub `/`)
  - `dinner.html` (Budapest Dinner Cruises Hub `/budapest-dinner-cruises`)
  - `candlelit-dinner-cruise.html` (Candlelit Dinner Cruise Review `/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest`)
  - `legenda-city-cruises.html` (Legenda Dedicated Terminal `/legenda-city-cruises`)
  - `danube_cruise_decision_hub.html` (Interactive Comparison & Filter Engine `/danube-cruise-decision-hub`)
  - `about.html` (About Us & Editorial Credentials `/about`)
- Routing & Config:
  - `vercel.json` (Modern redirects, rewrites, cleanUrls, headers)
  - `preview_server.py` (Local HTTP server matching vercel.json)
  - `sitemap.xml` (SEO canonical sitemap for the 21 GSC active languages)
- Tracking & Logic:
  - `bpa-tracking.js` (Unified tracking, UTM/click ID persistence, outbound link decoration, Meta Pixel dispatch)
- Tests:
  - `tests/` (E2E Test Runner, test cases across Tiers 1-5)

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Staging Git Branch | Dedicated `staging/static-overhaul` git branch cleanly initialized | M1 | Survey E1 |
| 2 | Python Preview Server | Zero-dependency local staging server emulating `vercel.json` routes/redirects | M1 | Survey E1 |
| 3 | Vercel Modern Config | Modern `vercel.json` structure (cleanUrls, redirects, rewrites, headers) | M1 | Survey E1/E3 |
| 4 | River Hub Deployment | Clean Danube River Cruises Hub at `/` and `/budapest-river-cruises` | M2 | Survey E1 |
| 5 | Dinner Hub Deployment | Clean Budapest Dinner Cruises Hub at `/budapest-dinner-cruises` | M2 | Survey E1 |
| 6 | Candlelit Review Hub | Dedicated Candlelit Dinner Cruise Tested Review static page | M2 | Survey E1 |
| 7 | Legenda Terminal Hub | Dedicated Legenda Terminal at `/legenda-city-cruises` | M2 | Survey E1 |
| 8 | Decision Hub Deployment | Danube Cruise Decision Hub at `/danube-cruise-decision-hub` | M2 | Survey E1 |
| 9 | Strip `#` TOC Fragments | Remove legacy Webflow `#` table-of-contents fragments and dead anchors | M3 | Survey E2 |
| 10 | Fix Digits-First IDs | Replace invalid IDs (`1-legenda`, etc.) with semantic HTML5 IDs | M3 | Survey E2 |
| 11 | Unicode & Relume Cleanup | Remove `\u200d`, `\u00a0`, ghost `library.relume.io...#` links & empty buttons | M3 | Survey E2 |
| 12 | Duplicate ID Elimination | Eliminate duplicate IDs (`id="faq"`, duplicated `w-node` blocks) | M3 | Survey E2 |
| 13 | Clean Canonical Tags | Ensure all hubs have self-referencing canonical tags with 0 `#` fragments | M3 | Survey E2 |
| 14 | Clean Multilingual Sitemap | Generate `sitemap.xml` for 21 GSC active languages (`en`, `hu`, `ro`, `ja`, `it`, `fr`, `pl`, `cs`, `hr`, `ru`, `el`, `bg`, `es`, `sr`, `he`, `pt`, `sk`, `tr`, `uk`, `de`, `ko`) | M3 | Survey E2 |
| 15 | Legenda Partner ID Fix | Correct typo `partner=38885` to verified VIP `partner=38585` | M4 | Survey E3 |
| 16 | Decision Hub Tracking Fix | Eliminate tracking bleed on Decision Hub; add Legenda & TourCMS tracking | M4 | Survey E3 |
| 17 | UTM & Click ID Persistence | Preserve `gclid`, `fbclid`, and full `utm_*` suite across session | M4 | Survey E3 |
| 18 | Dual Cookie/Storage Sync | Persist tracking in cookies + localStorage with fallback | M4 | Survey E3 |
| 19 | Meta Pixel Standardization | Pixel `1355732169631751` & `InitiateCheckout` with 25% net commission value | M4 | Survey E3 |
| 20 | Tiqets Partner Preservation | Ensure `budapestadventures` partner parameter preserved on all Tiqets links | M4 | Survey E3 |
| 21 | Linguana Zombie Pruning | Prune 9 dead GSC languages (`ar`, `da`, `vi`, `no`, `sv`, `fi`, `th`, `zh`, `nl`) and 224 non-cruise translated zombie URLs | M5 | Survey E3 |
| 22 | 1-to-1 Localized Slugs 301 | 301 redirects for dead localized river/dinner cruise slugs & non-cruise zombies | M5 | Survey E3 |
| 23 | Catch-All Lang Redirects | Regex 301 redirects for dead language prefixes (`/:lang/:path* -> /:path*`) | M5 | Survey E3 |
| 24 | Zero Broken Links & Loops | Complete validation of all internal links and redirect chains | M5 | Survey E3 |
| 25 | 100% E2E Test Suite Pass | Pass all Tier 1-4 tests generated by E2E Testing Track | M6 | E2E Track |
| 26 | Adversarial Hardening (Tier 5) | White-box edge case testing, challenger audit, and zero-defect pass | M6 | Challenger |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Staging Isolation & Local Preview Server | Branch `staging/static-overhaul`, modern `vercel.json` base, `preview_server.py` | none | DONE |
| M2 | Core Money Hubs Pipeline | Rebuild 5 core hubs (`/`, `/budapest-dinner-cruises`, `/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest`, `/legenda-city-cruises`, `danube_cruise_decision_hub.html`) | M1 | DONE |
| M3 | HCU, Anchor Pollution & Canonicals | Strip `#` TOC fragments, clean semantic HTML5 IDs, fix ghost links, canonical tags with 0 `#`, clean `sitemap.xml` | M2 | DONE |
| M4 | Tracking Safeguards & VIP Attribution | Fix Legenda partner ID (`38585`), plug Decision Hub bleed, `bpa-tracking.js` (UTM/click ID persistence), Meta Pixel `1355732169631751` | M2 | DONE |
| M5 | i18n Pruning & 301 Redirect Architecture | Prune 25 zombie languages, complete 1-to-1 301 redirects in `vercel.json`, catch-all redirects, zero 404 traps | M1, M2, M3 | DONE |
| M6 | Final Milestone: E2E Test Pass & Hardening | Pass 100% E2E tests (Tiers 1-4), Adversarial Hardening (Tier 5), Forensic Audit signoff | M3, M4, M5, E2E Test Suite | DONE |

## Parallel Track: E2E Testing Track
- **Scope**: Requirement-driven opaque-box testing harness and comprehensive test cases (Tiers 1-4).
- **Deliverables**: `TEST_INFRA.md`, `tests/` test runner & test cases, `TEST_READY.md`.

## Interface Contracts
### Routing Engine ↔ Static Pages
- `vercel.json` rewrites route:
  - `/` -> `/index.html`
  - `/budapest-river-cruises` -> `/index.html`
  - `/budapest-dinner-cruises` -> `/dinner.html`
  - `/best-dinner-cruises-budapest` -> `/dinner.html`
  - `/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest` -> `/candlelit-dinner-cruise.html`
  - `/legenda-city-cruises` -> `/legenda-city-cruises.html`
  - `/danube-cruise-decision-hub` -> `/danube_cruise_decision_hub.html`
  - `/about` -> `/about.html`
- Canonical tags inside each page MUST match the rewritten URL without trailing slash or hash fragment.

### Tracking Engine (`bpa-tracking.js`) ↔ Outbound Booking Links
- Captures on page load: `utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, `utm_content`, `gclid`, `fbclid`, `_fbp`.
- Stores in: Cookie `bpa_attribution` (30 days) and `localStorage['bpa_attribution']`.
- Outbound link decoration:
  - Legenda links: `https://legenda.hu/...?partner=38585&subid=<serialized_tracking>`
  - TourCMS links: `https://...tourcms.com/...?agent_ref=38585&subid=<serialized_tracking>`
  - Tiqets links: `https://www.tiqets.com/...?partner=budapestadventures&...`
- Meta Pixel:
  - Standardized Pixel ID: `1355732169631751`
  - Event: `fbq('track', 'InitiateCheckout', { content_name: '...', value: <25% net commission EUR>, currency: 'EUR' })`

## Menu and footer (must stay identical site-wide)
- The master menu (header + mobile drawer + nav styles/script) and footer live on the tourism statistics pages:
  `budapest-tourism-statistics.html` (EN) and `hu/budapest-turizmus-statisztika/index.html` (HU).
- Change them only on the master page, then run `python3 scripts/sync_layout.py --langs en,hu` to copy them to every EN/HU page in `sitemap.xml`.
  `--check` reports pages that drifted (exit code 1) without writing.
- Language switcher rule: On the tourism statistics pages (`budapest-tourism-statistics.html` and `hu/budapest-turizmus-statisztika`), the language switcher shows EN and HU only. On ALL other pages, the language switcher retains the full 22 languages — never overwrite or truncate standard pages to EN/HU.
- The footer lists only the five cruise money pages plus About and Contact. Do not add other guides to it.
