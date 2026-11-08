# Handoff Report — Explorer Survey 1 (Codebase Structure & Staging Pipeline)

## 1. Observation
- **Git Branch & Status**:
  - Command: `git branch -a` returned `* main` and `remotes/origin/main`. Branch `staging/static-overhaul` does not exist.
  - Command: `git status -s` revealed 5 tracked uncommitted modified files:
    - `M api/cron.py`
    - `M dinner.html`
    - `M river-ecom.html`
    - `M river.html`
    - `M tourcms-sync.js`
    - 40+ untracked files (`??`) in root including `danube_cruise_decision_hub.html`, `interactive_cruise_filter_engine_mockup.html`, `test_tourcms.py`, `sync_ratings.sh`, `ratings.json`, `data/`, etc.
- **5 Core Money Hubs Mapping**:
  - **Hub 1: Danube River Cruises Main Hub** (`/` and `/budapest-river-cruises`):
    - `pages.json` line 1: `id="64abbb0ee146f7684dd945ef"`, `publishedPath="/"`, title `"Budapest River Cruises | Day, Night & Dinner Tours from €14"`.
    - `pages.json` line 1: `id="64abbb0ee146f7684dd9469f"`, `publishedPath="/best-budapest-river-cruises"`, title `"The 10 Best River Cruises and Boat Tours in Budapest (Personally Tested)"`.
    - Local source files: `river.html` (1,123 lines, 350KB), `river-ecom.html` (1,146 lines, 355KB), `river_desktop_wide_preview.html` (2,423 lines, 175KB).
    - Discrepancy observed: Live `https://www.budapestadventures.com/budapest-river-cruises` returned `HTTP/2 404`. Root `index.html` on Vercel currently contains an unrelated Prosecco cruise mockup (`<title>Budapest's Best Unlimited Prosecco Cruises...</title>`).
  - **Hub 2: Budapest Dinner Cruises Hub** (`/budapest-dinner-cruises`):
    - `pages.json` line 1: `id="690fc96a2a1078147a33d019"`, `publishedPath="/budapest-dinner-cruises"`, title `"Budapest Dinner Cruises"`.
    - `pages.json` line 1: `id="64abbb0ee146f7684dd946bc"`, `publishedPath="/best-dinner-cruises-budapest"`, title `"7 Best Dinner Cruises in Budapest in 2025 (Personally Tested)"`.
    - Local source files: `dinner.html` (744 lines, 224KB), `dinner_desktop_wide_preview.html` (2,229 lines, 142KB). Both URLs return `HTTP/2 200` on production.
  - **Hub 3: Candlelit Dinner Cruise Tested Review** (`/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest`):
    - `pages.json` line 1: `id="69032f89be8ec49c419233a6"`, `publishedPath="/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest"`, title `"Candlelit Dinner Cruise Budapest Review (Personally Tested)"`.
    - Live URL returns `HTTP/2 200` (89,482 bytes) with canonical pointing to `https://www.budapestadventures.com/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest`.
    - Local source files: Content exists embedded inside `dinner.html`, `all_7_cruises_complete.html`, and `webflow_part1_cruises_1_to_2.html`. No standalone file exists at root.
  - **Hub 4: Legenda City Cruises Dedicated Terminal** (`/legenda-city-cruises`):
    - Local source file: `legenda-city-cruises.html` (646 lines, 33KB). Clean Tailwind CSS, live TourCMS timetable, Meta Pixel `1355732169631751`, Google Tag `AW-16782417237`.
    - `vercel.json` line 20: `{ "src": "/legenda-city-cruises", "dest": "/legenda-city-cruises.html" }`.
  - **Hub 5: Danube Cruise Decision Hub & Filter Engines** (`danube_cruise_decision_hub.html`):
    - Local source file: `danube_cruise_decision_hub.html` (707 lines, 39KB). Standalone comparison hub with ItemList + FAQPage JSON-LD schema, interactive filters, dock pier guide.
- **Vercel & Sync Configuration**:
  - `vercel.json` (29 lines) only routes `/api/cron` and `/legenda-city-cruises`. Does not map clean routes for the other core money hubs or handle 301 redirects for pruned Linguana languages.
  - `tourcms-sync.js` (170 lines): Persists `tc_fbclid`, `tc_gclid`, `tc_gclid_type`, `_fbp`, decorates partner links with `subid` and `agent_ref`, and fires Meta Pixel `InitiateCheckout` on click with net commission margin.
  - `api/cron.py` (425 lines): Native HMAC-SHA256 TourCMS client (Channel `16485`, Marketplace `57509`, API Key `51405b89d978`), availability checker, and Meta CAPI / Google Ads offline conversion sync.
- **Runtime Environment**:
  - Command `which vercel npx node` returned exit code 1 (`not found`).
  - Command `python3 --version` returned `Python 3.9.6`.

## 2. Logic Chain
1. From Observation 1, because branch `staging/static-overhaul` does not exist, all staging work must be isolated by branching from `main` before modifications occur.
2. From Observation 2 (Hub 1), the live URL `/budapest-river-cruises` is a 404, while `/best-budapest-river-cruises` is the live canonical target. On Vercel, root `/` currently resolves to an obsolete Prosecco mockup (`index.html`). Therefore, `river-ecom.html` must be placed at root (or routed to `/`) and `/budapest-river-cruises` must be given a 301 rewrite/redirect in `vercel.json`.
3. From Observation 2 (Hub 2 & Hub 3), `dinner.html` serves `/best-dinner-cruises-budapest`. `/budapest-dinner-cruises` must be routed to `dinner.html` in `vercel.json`. The candlelit review page needs a dedicated static file extracted or built and routed at `/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest`.
4. From Observation 2 (Hub 4 & Hub 5), `legenda-city-cruises.html` and `danube_cruise_decision_hub.html` are modern Tailwind static pages that are already production-ready and independent of Webflow runtime bloat.
5. From Observation 3, `vercel.json` is currently incomplete: it lacks routes for the core hubs and lacks 301 redirect rules for pruned Linguana language prefixes (`/cs/*`, `/bg/*`, `/zh/*`).
6. From Observation 4, `tourcms-sync.js` and `api/cron.py` contain all required keys and logic to safeguard the €130,000 Legenda partnership. They must be preserved and included in all staging hubs.
7. From Observation 5, because Node.js and `@vercel/cli` are not in the environment PATH, local preview must be driven by a zero-dependency Python script (`preview_server.py`) that emulates `vercel.json` cleanUrls and routing.

## 3. Caveats
- No direct Webflow API token was present in `.env` to pull draft collections; however, `pages.json` provides an export of the Webflow page tree, and live production URLs were directly queried via HTTP.
- Did not modify repository branch state or source files, adhering to read-only explorer discipline.

## 4. Conclusion
The Budapest Adventures repository contains all core source components needed to build an isolated, high-performance static staging environment on Vercel without touching live production DNS (`35.187.176.9`).

### Key Actions Required for Staging Build:
1. Create dedicated branch: `git checkout -b staging/static-overhaul`.
2. Deploy Danube River Cruises Main Hub (`river-ecom.html`) as root `index.html`.
3. Route `/budapest-dinner-cruises` and `/best-dinner-cruises-budapest` to `dinner.html`.
4. Create dedicated `candlelit-dinner-cruise-budapest.html` review page.
5. Expand `vercel.json` with clean URL rewrites for all 5 hubs and 301 redirects for pruned Linguana language paths.
6. Provide `scripts/preview_server.py` for instant local testing on `http://localhost:3000`.

## 5. Verification Method
1. Verify branch state:
   ```bash
   git branch -a
   ```
2. Verify live production HTTP status of hubs:
   ```bash
   curl -sI https://www.budapestadventures.com/
   curl -sI https://www.budapestadventures.com/best-budapest-river-cruises
   curl -sI https://www.budapestadventures.com/budapest-dinner-cruises
   curl -sI https://www.budapestadventures.com/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest
   ```
3. Verify comprehensive survey report exists:
   ```bash
   test -f /Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/teamwork_preview_explorer_survey_1/survey_codebase.md && echo "Report OK"
   ```
4. Verify TourCMS tracking script integrity:
   ```bash
   grep -E 'subid|agent_ref|InitiateCheckout' /Users/adamdimitrov/Development/budapest-adventures/tourcms-sync.js
   ```
