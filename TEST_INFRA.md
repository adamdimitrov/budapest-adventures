# TEST_INFRA — Budapest Adventures Staging Architecture Test Specification

## 1. Overview & Philosophy

This document defines the comprehensive opaque-box test infrastructure for the **Budapest Adventures Staging Architecture Overhaul**. 

The test harness guarantees the highest degree of reliability across:
1. **SEO & Routing Integrity**: Elimination of Webflow/Linguana DOM bloat, removal of `#` anchor pollution, validation of canonical tags, clean sitemap generation, and zero-defect 301 redirect architecture.
2. **Commercial Attribution & Tracking Safeguards**: 100% preservation of partner affiliate parameters (Legenda VIP account `38585`, Tiqets `budapestadventures`, TourCMS `agent_ref=38585`), click IDs (`gclid`, `fbclid`, `_fbp`), UTM attribution persistence, and Meta Pixel (`1355732169631751`) conversion dispatch.
3. **Staging Isolation & Zero-Downtime Verification**: Ensuring all staging verification executes locally or on staging branches without modifying live production DNS (`35.187.176.9`).

### Core Architectural Principles
- **Opaque-Box Requirement-Driven**: Tests are designed strictly against the interface contracts and requirements defined in `ORIGINAL_REQUEST.md` and `PROJECT.md`. Tests observe only external interfaces (HTTP requests/responses, HTML DOM structure, JSON-LD schemas, script behavior, and configuration files).
- **Zero-Dependency Python 3**: The test runner and all test suites rely exclusively on the Python 3 standard library (`urllib`, `http.client`, `html.parser`, `xml.etree.ElementTree`, `json`, `re`, `pathlib`, `unittest`). No pip dependencies or external frameworks (`pytest`, `requests`, `selenium`, `beautifulsoup4`) are required.
- **Dual Execution Modes**:
  1. *Static Mode*: Inspects filesystem artifacts directly (`vercel.json`, `sitemap.xml`, HTML files, `bpa-tracking.js`, `preview_server.py`). Fast, deterministic, runnable in CI/pre-commit.
  2. *Live Server Mode*: Evaluates live HTTP transactions against `preview_server.py` or any staging URL (`http://localhost:3000`), verifying actual HTTP status codes, 301 redirect headers, content-types, cleanUrls resolution, and security headers.

---

## 2. The 4-Tier Test Architecture

The test suite is structured into four distinct, complementary tiers:

```
+-------------------------------------------------------------------------+
| Tier 4: Real-World Scenarios (Workload / End-to-End User Journeys)      |
|  - Google Ad Click -> River Hub -> Decision Filter -> Legenda Checkout   |
|  - Meta Ad -> Candlelit Review -> Tiqets Checkout                       |
|  - Zombie Language -> 301 Redirect -> Canonical Hub -> Tracking Retained |
+-------------------------------------------------------------------------+
                                    ^
+-------------------------------------------------------------------------+
| Tier 3: Cross-Feature Combinations (Pairwise Interaction Coverage)      |
|  - Mobile Viewport x UTM Preservation x Outbound Decoration             |
|  - Pruned Slug Redirect x Query String Preservation x Canonical Tag     |
|  - Decision Hub Filter State x Meta Pixel Trigger x Net Commission Val  |
+-------------------------------------------------------------------------+
                                    ^
+-------------------------------------------------------------------------+
| Tier 2: Boundary & Corner Cases (Boundary Value Analysis - BVA)         |
|  - Malformed query strings, missing UTMs, extreme lengths, SQLi/XSS     |
|  - Trailing slashes, uppercase paths, legacy `#` fragments              |
|  - Unsupported languages, missing cookies, localStorage disabled       |
+-------------------------------------------------------------------------+
                                    ^
+-------------------------------------------------------------------------+
| Tier 1: Feature Coverage (Category-Partition Isolation Testing)         |
|  - >=5 atomic test cases per feature across all 26 inventoried features  |
|  - Verification of happy-path functional behavior and schema validation |
+-------------------------------------------------------------------------+
```

### Tier 1: Feature Coverage (Category-Partition Isolation)
- **Methodology**: Category-Partition Method. The specification for each feature is broken into input domains, environmental states, and expected outputs.
- **Goal**: Full isolation coverage for all 26 inventoried features. Every feature has at least 5 atomic test cases asserting its discrete requirements.
- **Scope**:
  - F1–F3: Git branch isolation, preview server functionality, modern `vercel.json` config.
  - F4–F8: 5 Core money hubs (`/`, `/budapest-dinner-cruises`, `/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest`, `/legenda-city-cruises`, `danube_cruise_decision_hub.html`).
  - F9–F14: `#` TOC fragment removal, semantic HTML5 IDs, unicode cleanup, duplicate ID elimination, clean canonicals, approved multilingual sitemap.
  - F15–F20: Legenda VIP partner ID `38585`, Decision Hub tracking, UTM persistence, dual cookie/localStorage sync, Meta Pixel `1355732169631751` net commission value, Tiqets partner preservation.
  - F21–F24: Linguana 25 zombie language pruning, 1-to-1 localized 301 redirects, catch-all redirects, zero broken links/loops.
  - F25–F26: E2E suite pass and adversarial hardening.

### Tier 2: Boundary & Corner Cases (Boundary Value Analysis - BVA)
- **Methodology**: Boundary Value Analysis and Equivalence Partitioning at extreme boundary conditions.
- **Goal**: Ensure the staging architecture gracefully handles malformed inputs, malicious injections, unexpected user actions, and legacy edge cases.
- **Edge Conditions Tested**:
  - URL edge cases: paths with multiple consecutive slashes (`//budapest-dinner-cruises`), uppercase letters, trailing slashes, URL-encoded special characters (`%20`, `%23`, `%2F`), non-ASCII unicode paths.
  - Query string edge cases: empty values (`?utm_source=&gclid=`), unrecognized params, massive parameter strings (>2KB), duplicate keys (`?partner=38885&partner=38585`), SQL/XSS payloads (`?gclid=<script>`).
  - Hash fragment resilience: requests containing legacy `#1-legenda`, `#faq`, `#toc` preserved in client navigation without triggering DOMException.
  - Internationalization edge cases: unknown language codes (`/xx/`, `/zz/`), mixed-case codes (`/DE/`), double prefix paths (`/en/de/`).
  - Storage & tracking fallbacks: simulated private browsing mode (cookies disabled, localStorage throwing SecurityError), missing `_fbp`, null click IDs.

### Tier 3: Cross-Feature Interactions (Pairwise Combinations)
- **Methodology**: Pairwise / Orthogonal Array Testing. Real-world failures commonly emerge from unexpected interactions between two or more independently working features.
- **Combinations Tested**:
  1. *Paid Campaign x Outbound Booking*: Inbound `gclid` + `utm_source=google` on `/` -> Navigating to `/danube-cruise-decision-hub` -> Outbound click to `legenda.hu` -> Both `partner=38585` and `subid` containing original `gclid` present.
  2. *Zombie Slug Redirect x Tracking Persistence*: Inbound request `https://budapestadventures.com/de/donau-kreuzfahrten-budapest?utm_campaign=winter2025` -> HTTP 301 redirect to `/` or `/budapest-river-cruises` -> Location header preserves `utm_campaign=winter2025`.
  3. *Review Page x Decision Hub x Canonical Tag*: Viewing `candlelit-dinner-cruise.html` -> clicking link to decision hub -> canonical tag on both pages correctly references respective canonical root without hash fragments.
  4. *Device Filter x Pixel Trigger*: User filters for "Dinner Cruises" on Decision Hub -> Clicks "Book Legenda Dock 7" -> Verifies Meta Pixel `InitiateCheckout` fires with `value` equal to 25% net commission and currency `EUR`.
  5. *Dual Storage Sync x Cross-Subdomain*: User sets cookie `bpa_attribution` -> clears localStorage -> Script recovers attribution from cookie -> Decorates Tiqets partner link.

### Tier 4: Real-World Scenarios (Workload & User Journeys)
- **Methodology**: Operational Profile Testing simulating real visitor sessions from arrival to conversion.
- **End-to-End Scenarios**:
  - **Scenario 1 (The Google Ads Direct Booker)**:
    Visitor clicks Google Search ad for "budapest boat tour" with `?gclid=Cj0KCQ...&utm_source=google&utm_medium=cpc&utm_campaign=river_search_us`. Lands on Danube River Cruises Hub (`/`). Reads boat comparison table. Selects Legenda 70-minute sightseeing cruise. Clicks direct checkout button. Test asserts: outbound URL is `https://legenda.hu/...partner=38585...`, includes `subid` with encoded `gclid`, and Meta Pixel `InitiateCheckout` is triggered.
  - **Scenario 2 (The Meta Retargeting Luxury Diner)**:
    Visitor clicks Instagram Story ad with `?fbclid=IwAR2...&utm_source=instagram&utm_medium=paid_social`. Lands on Candlelit Dinner Cruise Review (`/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest`). Reads verified review and menu analysis. Clicks TourCMS booking link. Test asserts: outbound TourCMS link contains `agent_ref=38585`, `tc_fbclid` is retained, and Meta Pixel `InitiateCheckout` value corresponds to 25% of ticket price.
  - **Scenario 3 (The International Organic Visitor from Pruned Language)**:
    German traveler clicks an old indexed Google result for `/de/donau-schifffahrt-budapest` with `?ref=travelblog`. Server returns HTTP 301 redirecting to clean canonical `/budapest-river-cruises`. Page renders valid canonical `<link rel="canonical" href="https://www.budapestadventures.com/budapest-river-cruises">`. German traveler navigates to Legenda terminal (`/legenda-city-cruises`). All tracking and partner codes remain intact.
  - **Scenario 4 (The Decision Engine Power User)**:
    Visitor lands on `/danube-cruise-decision-hub`. Interacts with interactive filters (Day vs Night, Dinner vs Sightseeing). Clicks through to multiple cruise details (`#legenda-dock7`, `#prosecco-sunset`). Verifies no DOMException crashes on hash navigation, no broken anchors (`#silverline-folk`), and all partner outbound links contain verified IDs.
  - **Scenario 5 (The Search Engine Spider / SEO Audit)**:
    Crawler requests `/robots.txt` and `/sitemap.xml`. Verifies `sitemap.xml` contains ONLY valid approved language routes (`en`, `de`, `it`, `fr`, `es`) with zero machine-translated zombie paths. Crawls every URL in `sitemap.xml`, asserting HTTP 200, matching self-referencing canonical tag with 0 `#` fragments, valid JSON-LD schema, and zero empty/ghost links.

---

## 3. Feature Inventory to Test Mapping

Every one of the 26 inventoried features from `PROJECT.md` is covered across the test suites:

| # | Feature | Scope | Tier 1 Tests | Tier 2 Edge Cases | Tier 3 & 4 Journeys |
|---|---------|-------|--------------|-------------------|---------------------|
| 1 | Staging Git Branch | Branch `staging/static-overhaul` verification | `test_f01_*` (5 tests) | `test_f01_bva_*` | Scenario 5 |
| 2 | Python Preview Server | `preview_server.py` routing & headers | `test_f02_*` (5 tests) | `test_f02_bva_*` | Scenario 1, 3 |
| 3 | Vercel Modern Config | `vercel.json` redirects, rewrites, cleanUrls | `test_f03_*` (5 tests) | `test_f03_bva_*` | Scenario 3 |
| 4 | River Hub Deployment | `/` & `/budapest-river-cruises` -> `index.html` | `test_f04_*` (5 tests) | `test_f04_bva_*` | Scenario 1 |
| 5 | Dinner Hub Deployment | `/budapest-dinner-cruises` -> `dinner.html` | `test_f05_*` (5 tests) | `test_f05_bva_*` | Scenario 2 |
| 6 | Candlelit Review Hub | Dedicated review static hub | `test_f06_*` (5 tests) | `test_f06_bva_*` | Scenario 2 |
| 7 | Legenda Terminal Hub | `/legenda-city-cruises` dedicated hub | `test_f07_*` (5 tests) | `test_f07_bva_*` | Scenario 1, 4 |
| 8 | Decision Hub Deployment | `/danube-cruise-decision-hub` interactive hub | `test_f08_*` (5 tests) | `test_f08_bva_*` | Scenario 4 |
| 9 | Strip `#` TOC Fragments | Removal of legacy Webflow TOC hash fragments | `test_f09_*` (5 tests) | `test_f09_bva_*` | Scenario 4, 5 |
| 10 | Fix Digits-First IDs | Clean semantic IDs (replacing `1-legenda`, etc.) | `test_f10_*` (5 tests) | `test_f10_bva_*` | Scenario 4 |
| 11 | Unicode & Relume Cleanup | Strip `\u200d`, `\u00a0`, ghost relume links | `test_f11_*` (5 tests) | `test_f11_bva_*` | Scenario 5 |
| 12 | Duplicate ID Elimination | Deduplicate `faq`, `w-node` attributes | `test_f12_*` (5 tests) | `test_f12_bva_*` | Scenario 5 |
| 13 | Clean Canonical Tags | Self-referencing canonicals with 0 `#` | `test_f13_*` (5 tests) | `test_f13_bva_*` | Scenario 3, 5 |
| 14 | Clean Multilingual Sitemap | `sitemap.xml` for approved `en/de/it/fr/es` | `test_f14_*` (5 tests) | `test_f14_bva_*` | Scenario 5 |
| 15 | Legenda Partner ID Fix | Correction of `38885` to VIP `38585` | `test_f15_*` (5 tests) | `test_f15_bva_*` | Scenario 1, 4 |
| 16 | Decision Hub Tracking Fix | Elimination of untracked outbound links | `test_f16_*` (5 tests) | `test_f16_bva_*` | Scenario 4 |
| 17 | UTM & Click ID Persistence | Capture & retention of `gclid`, `fbclid`, UTMs | `test_f17_*` (5 tests) | `test_f17_bva_*` | Scenario 1, 2 |
| 18 | Dual Cookie/Storage Sync | Cookies + localStorage synchronization | `test_f18_*` (5 tests) | `test_f18_bva_*` | Scenario 1, 2 |
| 19 | Meta Pixel Standardization | Pixel `1355732169631751` & 25% net commission | `test_f19_*` (5 tests) | `test_f19_bva_*` | Scenario 1, 2 |
| 20 | Tiqets Partner Preservation | Retention of `partner=budapestadventures` | `test_f20_*` (5 tests) | `test_f20_bva_*` | Scenario 2 |
| 21 | Linguana Zombie Pruning | Pruning 25 zero-click machine-translated langs | `test_f21_*` (5 tests) | `test_f21_bva_*` | Scenario 3 |
| 22 | 1-to-1 Localized Slugs 301 | Explicit 301 redirects for translated slugs | `test_f22_*` (5 tests) | `test_f22_bva_*` | Scenario 3 |
| 23 | Catch-All Lang Redirects | Regex redirects for pruned language prefixes | `test_f23_*` (5 tests) | `test_f23_bva_*` | Scenario 3 |
| 24 | Zero Broken Links & Loops | Validation of internal anchors and redirects | `test_f24_*` (5 tests) | `test_f24_bva_*` | Scenario 4, 5 |
| 25 | 100% E2E Test Suite Pass | Complete harness execution & reporting | `test_f25_*` (5 tests) | `test_f25_bva_*` | Full Suite |
| 26 | Adversarial Hardening (Tier 5) | Fault injection, XSS/injection resistance | `test_f26_*` (5 tests) | `test_f26_bva_*` | Challenger |

---

## 4. Test Execution & Reporting

The test suite is executed using the unified test runner:

```bash
# Run all tests across Tiers 1-4 in static inspection mode
python3 tests/test_runner.py

# Run a specific tier
python3 tests/test_runner.py --tier 1
python3 tests/test_runner.py --tier 2
python3 tests/test_runner.py --tier 3
python3 tests/test_runner.py --tier 4

# Run tests for a specific feature (e.g. Feature 15: Legenda Partner ID)
python3 tests/test_runner.py --feature 15

# Run against a live preview server
python3 tests/test_runner.py --server-url http://localhost:3000

# Generate machine-readable JSON output
python3 tests/test_runner.py --json-report test_results.json
```

### Exit Codes
- `0`: All executed tests passed with 0 errors or failures.
- `1`: One or more tests failed (assertions failed).
- `2`: Test execution setup error or invalid arguments.
