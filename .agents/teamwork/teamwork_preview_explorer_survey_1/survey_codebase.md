# Codebase Structure & Staging Pipeline Survey Report

**Date**: 2026-11-06  
**Auditor**: Explorer Survey 1 (Codebase Structure & Staging Pipeline)  
**Project Root**: `/Users/adamdimitrov/Development/budapest-adventures`  
**Working Directory**: `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/teamwork_preview_explorer_survey_1`

---

## Executive Summary

Budapest Adventures (`budapestadventures.com`) is in transition from a bloated Webflow/Linguana reverse-proxy architecture (`35.187.176.9`) to a clean, high-performance static staging architecture hosted on Vercel.

The repository currently resides on git branch `main` with 5 tracked uncommitted files and over 40 untracked mockups, sync scripts, and partner datasets. Branch `staging/static-overhaul` **does not yet exist** and must be created. 

The primary revenue driver—Legenda City Cruises (€130,000+ volume in 2025)—relies on a finely-tuned TourCMS tracking pipeline (`tourcms-sync.js` client-side cookie persistence and link decoration, and `api/cron.py` serverless offline conversion attribution). This survey maps the source assets for all 5 core money hubs, audits the Vercel routing configuration, details the TourCMS tracking pipeline, and defines a zero-dependency local preview execution path.

---

## 1. Git Repository & Branch State

### 1.1 Branch Architecture
- **Active Branch**: `main` (`git rev-parse --abbrev-ref HEAD` -> `main`)
- **Remote Tracking**: `origin/main` (`4f592fb feat(media): integrate user-provided Legenda candlelit dinner salon photo`)
- **Branch `staging/static-overhaul` Status**: **DOES NOT EXIST**.
  - Must be created from `main`: `git checkout -b staging/static-overhaul`.

### 1.2 Working Tree Modifications (Tracked Files)
The following 5 files have uncommitted modifications on `main`:
1. `api/cron.py` (+459 / -131 lines): Complete TourCMS XML REST API integration, availability fetcher, and CAPI / Google Ads offline conversion sync.
2. `tourcms-sync.js` (+34 / -28 lines): Dynamic attribution capture (`fbclid`, `_fbp`, `gclid`/`wbraid`/`gbraid`), link decoration with `subid` and `agent_ref`, and Meta Pixel `InitiateCheckout` dispatch based on net commission values.
3. `river.html` (+37 / -7 lines): Injected `tourcms-sync.js`, updated rating scripts, and anchor adjustments.
4. `river-ecom.html` (+34 / -8 lines): E-commerce variant of `river.html`.
5. `dinner.html` (+12 / -2 lines): Updated canonical and tracking references.

### 1.3 Untracked Files Inventory
Over 40 files in the root directory are untracked (`??`), categorized as:
- **Core Hub Mockups & Implementations**: `danube_cruise_decision_hub.html`, `interactive_cruise_filter_engine_mockup.html`, `interactive_dinner_cruise_filter_engine_mockup.html`, `legenda_native_card_mockup.html`, `legenda_embed_only.html`, `programmatic_decision_hub_mockup.html`, `river_cruises_decision_hub_mockup.html`.
- **Card & Embed Components**: `webflow_part1_cruises_1_to_2.html`, `webflow_part2_cruises_3_to_4.html`, `webflow_part3_cruises_5_to_7.html`, `webflow_shadow_legenda_card_embed.html`, `live_dinner_embed.html`, `all_7_cruises_complete.html`, `comparison_deck_7_cruises.html`, `comparison_deck_10_river_cruises.html`.
- **Automation & Sync Scripts**: `update_ratings.py`, `sync_ratings.sh`, `sync_all_table_photos.py`, `test_tourcms.py`, `test_tourcms2.py`, `tourcms_test.py`, `send_legenda_test.py`, `add_smooth_anchor_fix.py`, `inject_all_photos.py`, `scripts/create_legenda_brand_campaign.py`.
- **B2B Directory & Data Intelligence**: `data/LEGENDA_PARTNER_DIRECTORY.md`, `data/legenda_partners_aug20_directory.json`, `data/legenda_partners_aug20_raw.json` (Leaked 200+ offline B2B accounts: Four Seasons, Ritz-Carlton, Kempinski, Abercrombie & Kent, Amex GBT).

---

## 2. Source Mapping for the 5 Core Money Hubs

| Hub # | Money Hub Name | Live Target URL | Webflow Page ID | Local Source Files | Status & Action Needed |
|---|---|---|---|---|---|
| **1** | **Danube River Cruises Main Hub** | `/` and `/budapest-river-cruises` | `64abbb0ee146f7684dd945ef` (`/`) & `64abbb0ee146f7684dd9469f` (`/best-budapest-river-cruises`) | `river.html` (1,123 lines, 350KB)<br>`river-ecom.html` (1,146 lines, 355KB)<br>`river_desktop_wide_preview.html` (2,423 lines, 175KB) | **Discrepancy at root**: Root `index.html` currently contains an unrelated Prosecco cruise mockup. Needs replacement with Danube River Cruises Main Hub. `/budapest-river-cruises` returns 404 on live DNS; must be mapped in `vercel.json`. |
| **2** | **Budapest Dinner Cruises Hub** | `/budapest-dinner-cruises` | `690fc96a2a1078147a33d019` (`/budapest-dinner-cruises`) & `64abbb0ee146f7684dd946bc` (`/best-dinner-cruises-budapest`) | `dinner.html` (744 lines, 224KB)<br>`dinner_desktop_wide_preview.html` (2,229 lines, 142KB) | `dinner.html` in repo represents `/best-dinner-cruises-budapest`. Both `/budapest-dinner-cruises` and `/best-dinner-cruises-budapest` are live HTTP 200 on production. Must route `/budapest-dinner-cruises` to `dinner.html` in `vercel.json`. |
| **3** | **Candlelit Dinner Cruise Tested Review** | `/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest` | `69032f89be8ec49c419233a6` (parentId: `69032fd605ee18d114e33b79`) | Embedded sections in:<br>`dinner.html`<br>`all_7_cruises_complete.html`<br>`webflow_part1_cruises_1_to_2.html`<br>`article_embed_preview.html` | Live HTTP 200 on production (89,482 bytes). No standalone HTML file exists in root. Needs dedicated static file `candlelit-dinner-cruise-budapest.html` deployed and routed in `vercel.json`. |
| **4** | **Legenda City Cruises Dedicated Terminal** | `/legenda-city-cruises` | N/A (Custom bespoke LP for `cruises.budapestadventures.com`) | `legenda-city-cruises.html` (646 lines, 33KB)<br>`legenda.html` (756 lines, 42KB) | Fully implemented with Tailwind CSS, instant photo switching, live TourCMS timetable links, and Meta Pixel `InitiateCheckout`. Already routed in `vercel.json` (`/legenda-city-cruises` -> `legenda-city-cruises.html`). |
| **5** | **Danube Cruise Decision Hub & Filter Engines** | `danube_cruise_decision_hub.html` | N/A (Bespoke programmatic hub) | `danube_cruise_decision_hub.html` (707 lines, 39KB)<br>`interactive_cruise_filter_engine_mockup.html`<br>`programmatic_decision_hub_mockup.html` | Fully functional standalone comparison hub with ItemList + FAQPage JSON-LD schema, live category filters (Day, Sunset, Dinner, Unlimited Drinks), Pier Dock guide (Dock 7, 11, 8A), and clean UI. |

---

## 3. Configuration & Sync Pipeline Audit

### 3.1 Vercel Configuration (`vercel.json`)
```json
{
    "version": 2,
    "cleanUrls": true,
    "builds": [
        {
            "src": "api/**/*.py",
            "use": "@vercel/python"
        },
        {
            "src": "**/*.{html,jpg,jpeg,png,webp,svg,avif,css,js}",
            "use": "@vercel/static"
        }
    ],
    "routes": [
        {
            "src": "/api/cron",
            "dest": "/api/cron.py"
        },
        {
            "src": "/legenda-city-cruises",
            "dest": "/legenda-city-cruises.html"
        },
        {
            "src": "/(.*)",
            "dest": "/$1"
        }
    ]
}
```

#### Deficiencies in Current `vercel.json`:
1. **Root collision**: Navigating to `/` serves `index.html` (Prosecco cruise page) instead of the Danube River Cruises Main Hub.
2. **Missing core routes**: No explicit rewrites or routes exist for:
   - `/budapest-river-cruises` -> `river-ecom.html`
   - `/best-budapest-river-cruises` -> `river-ecom.html`
   - `/budapest-dinner-cruises` -> `dinner.html`
   - `/best-dinner-cruises-budapest` -> `dinner.html`
   - `/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest` -> `candlelit-dinner-cruise-budapest.html`
   - `/danube-river-cruise-hub` -> `danube_cruise_decision_hub.html`
3. **Missing 301 Redirect Architecture**:
   - Zero-click Linguana machine-translated paths (`/cs/*`, `/bg/*`, `/zh/*`, etc.) are not redirected back to their canonical targets.
   - Legacy hash fragment URLs and uppercase/trailing slash variants are unhandled.

---

### 3.2 TourCMS Tracking & Revenue Protection (`tourcms-sync.js`)
File: `/Users/adamdimitrov/Development/budapest-adventures/tourcms-sync.js` (170 lines)

#### Key Operational Mechanics:
1. **Attribution Ingestion**:
   - Captures `fbclid` from URL -> stores in cookie `tc_fbclid` (30-day lifetime).
   - Captures `gclid`, `wbraid`, or `gbraid` -> stores in `tc_gclid` and `tc_gclid_type`.
   - Reads existing first-party `_fbp` cookie.
   - Formats compound parameter: `fbclid:xxx|fbp:fb.1.xxx|gclid:yyy`.
2. **Partner Domain Whitelist**:
   - `legenda.hu`
   - `tourcms.com`
   - `budapestrivercruise.eu`
   - `tiqets.com`
3. **Outbound Link Decoration**:
   - For `tiqets.com`: appends `subid` and `click_id`.
   - For `legenda.hu` / `tourcms.com` / `budapestrivercruise.eu`: appends `subid` and `agent_ref`.
4. **Just-In-Time Event Interception**:
   - Listens to document click events in capture phase (`addEventListener('click', ..., true)`).
   - Dynamically decorates links at click time to guarantee no query string loss.
   - Calculates **estimated net commission value** (not gross ticket value):
     - Legenda Sightseeing (€25 retail -> €6.25 net commission @ 25% margin).
     - Legenda Candlelit Dinner (€110 retail -> €27.50 net commission @ 25% margin).
     - Legenda Daytime Duna Bella (€20 retail -> €5.00 net commission @ 25% margin).
   - Dispatches Meta Pixel `InitiateCheckout`:
     ```javascript
     window.fbq('track', 'InitiateCheckout', {
         content_name: contentName,
         content_category: 'River Cruise',
         value: estimatedValue,
         currency: 'EUR'
     });
     ```
   - Pushes `initiate_checkout_partner` to `dataLayer` for GTM / GA4.

---

### 3.3 TourCMS Backend Sync & Offline Conversion Engine (`api/cron.py`)
File: `/Users/adamdimitrov/Development/budapest-adventures/api/cron.py` (425 lines)

#### Operational Capabilities:
1. **Credentials & Endpoints**:
   - TourCMS Channel ID: `16485` (Legenda City Cruises)
   - TourCMS Marketplace ID: `57509`
   - API Key: `51405b89d978`
   - Meta Pixel: `1355732169631751`
   - Google Ads Customer ID: `4899321613`
2. **Authentication Engine**:
   - Native Python HMAC-SHA256 signature generator (`tourcms_request()`), zero external dependencies.
3. **Actions Supported via Query Params**:
   - `GET /api/cron?action=availability&tour_id=2&date=YYYY-MM-DD`: Returns live available slots, spaces remaining, retail price, net price, and commission margin.
   - `GET /api/cron?action=sync&dry_run=0`: Searches TourCMS bookings, extracts `fbclid`, `fbp`, `gclid`, and pushes offline conversion data to Meta CAPI and Google Ads API.

---

### 3.4 Ratings & Scraper Sync (`sync_ratings.sh` & `update_ratings.py`)
- `update_ratings.py` (369 lines): Scrapes ratings and review counts from GetYourGuide, Viator, and TripAdvisor. Uses native `urllib.request` with an automated AppleScript fallback to macOS Safari (`osascript`) for JavaScript-heavy targets.
- Output: `ratings.json` (918 lines, 40KB).
- Frontend consumer: `webflow-ratings.js` dynamically updates DOM star ratings and prices on page load without manual rebuilds.

---

## 4. Local Preview & Runtime Architecture

### 4.1 System Runtime State
- **Node.js / npm / Vercel CLI**: Not found in system PATH (`/usr/local/bin` does not exist; node is not installed).
- **Python**: `Python 3.9.6` installed at `/usr/bin/python3`.
- **Operating System**: macOS (Darwin 24.3.0).

### 4.2 Recommended Staging Preview Server
Because `@vercel/cli` is unavailable in PATH, static preview cannot rely on `vercel dev`. However, Python 3.9.6 is fully capable of running a zero-dependency staging preview server that emulates Vercel's `cleanUrls`, routing rules, and redirect headers.

#### Staging Server Specification (`scripts/preview_server.py`):
- Port: `3000` (or `8080`)
- Built using `http.server.SimpleHTTPRequestHandler`
- Features:
  - Parses `vercel.json` routes and redirects.
  - Automatically resolves extensionless URLs (e.g. `/legenda-city-cruises` -> `legenda-city-cruises.html`).
  - Implements 301 redirects for pruned routes.
  - Serves correct MIME types for modern assets (`.avif`, `.webp`, `.svg`, `.json`).

---

## 5. Architectural Recommendations for Next Milestones

1. **Create Branch Immediately**:
   ```bash
   git checkout -b staging/static-overhaul
   ```
2. **Reorganize Core Hub Files for Vercel Staging**:
   - Copy or rename `river-ecom.html` to `index.html` (or configure explicit route `^/$` -> `river-ecom.html`) so the Danube River Cruises Main Hub sits at root.
   - Deploy `candlelit-dinner-cruise-budapest.html` by extracting and modernizing the dedicated tested review page.
   - Ensure `danube_cruise_decision_hub.html` is accessible at `/danube-river-cruise-hub`.
3. **Upgrade `vercel.json`**:
   - Add explicit routing rules for all 5 core money hubs.
   - Add 301 redirect map for pruned Linguana languages (`/cs/(.*)`, `/bg/(.*)`, `/zh/(.*)`, `/ro/(.*)`, etc.) back to English canonical targets.
4. **Deploy Local Python Preview Runner**:
   - Add `scripts/preview_server.py` and document `python3 scripts/preview_server.py` for instant verification.
5. **Preserve Tracking Query Strings**:
   - Include `tourcms-sync.js` on every staging page to safeguard the €130,000 Legenda partner pipeline.
