# TEST_READY — Budapest Adventures Staging Architecture E2E Test Suite

## 1. Executive Summary

The E2E Test Suite for the **Budapest Adventures Staging Architecture Overhaul** is fully implemented, verified, and operational. 

Built using a pure, zero-dependency Python 3 opaque-box architecture, the test harness validates all requirements from `ORIGINAL_REQUEST.md` and all 26 inventoried features in `PROJECT.md`. It executes across local static files, DOM structures, schemas, configuration files, and can optionally run dynamic HTTP tests against `preview_server.py`.

- **Total Test Cases**: **280**
- **Test Framework**: Standard Python 3 standard library (`unittest`, `urllib`, `re`, `xml.etree.ElementTree`, `json`, `html.parser`)
- **Execution Time**: **~0.49 seconds** for all 280 tests
- **Baseline Results**:
  - **Passed**: 225 (80.4%)
  - **Failed**: 55 (19.6%)
  - *Analysis*: The 55 failing tests represent the exact planned deliverables for Milestones M1–M5 (`preview_server.py`, `vercel.json` 301 redirects, `candlelit-dinner-cruise.html`, `#` anchor cleanup, `bpa-tracking.js`, and Legenda VIP partner ID correction).

---

## 2. Test Architecture & Tier Breakdown

```
==============================================================================
 Tier                                  Test Cases   Status
==============================================================================
 Tier 1: Feature Coverage (Isolation)         130   Features 1-26 (5 per feat)
 Tier 2: Boundary & Corner Cases (BVA)        130   Features 1-26 (5 per feat)
 Tier 3: Cross-Feature Interactions            15   Pairwise Combinations
 Tier 4: Real-World Scenarios                   5   End-to-End User Journeys
------------------------------------------------------------------------------
 TOTAL                                        280   Full Opaque-Box Suite
==============================================================================
```

### Tier 1: Feature Coverage (Category-Partition Isolation) — 130 Tests
Atomic verification of the primary functional requirements and acceptance criteria for all 26 features:
- **Features 1–3 (Staging Environment & Routing)**: Git branch isolation, `preview_server.py` implementation, modern `vercel.json` syntax (`cleanUrls`, `redirects`, `rewrites`, `headers`).
- **Features 4–8 (Core Money Hubs Pipeline)**: `/` (`index.html`), `/budapest-dinner-cruises` (`dinner.html`), `/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest` (`candlelit-dinner-cruise.html`), `/legenda-city-cruises` (`legenda-city-cruises.html`), and `/danube-cruise-decision-hub` (`danube_cruise_decision_hub.html`).
- **Features 9–14 (SEO, HCU, Anchor & Sitemap Architecture)**: Stripping Webflow `#` TOC fragments, fixing digits-first IDs (`1-legenda` -> semantic slugs), removing zero-width joiners (`\u200d`) and Relume boilerplate, deduplicating IDs (`id="faq"`), ensuring clean canonical tags with 0 `#` fragments, and generating clean sitemaps for approved languages (`en`, `de`, `it`, `fr`, `es`).
- **Features 15–20 (Tracking Safeguards & VIP Attribution)**: Correcting Legenda affiliate typo (`partner=38885` -> VIP `partner=38585`), plugging tracking bleed on Decision Hub, capturing full UTM suite + click IDs (`gclid`, `fbclid`, `_fbp`), dual cookie + localStorage persistence, standardizing Meta Pixel `1355732169631751` with 25% net commission value, and preserving Tiqets partner code (`budapestadventures`).
- **Features 21–24 (Internationalization Pruning & 301 Redirects)**: Pruning 25 machine-translated zero-click languages, explicit 1-to-1 301 redirects for localized slugs, wildcard catch-all redirects (`/:lang/:path* -> /:path*`), and zero broken links / redirect loops.
- **Features 25–26 (Harness & Adversarial Hardening)**: Full test runner discovery and resilience against malicious query parameters, XSS strings, and oversized payloads.

### Tier 2: Boundary & Corner Cases (Boundary Value Analysis) — 130 Tests
Rigorous stress-testing of edge conditions across all 26 features:
- Malformed URLs (multiple slashes, trailing slashes, uppercase characters, URL-encoded entities).
- Empty, missing, and duplicate query strings (`?partner=38885&partner=38585`, `?utm_source=&gclid=`).
- Extreme query string payloads (>2KB length, SQL injection strings, XSS payload tags).
- Private browsing mode simulation (localStorage throwing `QuotaExceededError` or `SecurityError`, cookies blocked).
- Price calculations at extremes (€0.00, €9.00 child ticket, €135.00 luxury dinner, €10,000 corporate bookings).
- Deeply nested language paths (`/cs/a/b/c/d`) and localized foreign characters in slugs (`/de/d%C3%BCsseldorf`).

### Tier 3: Cross-Feature Interactions (Pairwise Combinations) — 15 Tests
Evaluates multi-feature interactions where defects commonly surface:
- Paid Traffic (Google `gclid` / Meta `fbclid`) x Decision Hub Filters x Outbound Legenda Decoration.
- Localized Zombie Slugs x Campaign UTMs x 301 Permanent Redirects x Query String Retention.
- Dual Cookie / LocalStorage Sync x Single Storage Failure (Cookie cleared vs LocalStorage blocked).
- Unit Economics Pricing x Meta Pixel `InitiateCheckout` (Child €9.00 -> €2.25 net commission; Adult €18.00 -> €4.50; Family €54.00 -> €13.50).
- ItemList Schema x DOM Card IDs x Clean Canonical Rewrites.

### Tier 4: Real-World Scenarios (End-to-End User Journeys) — 5 Tests
Complete operational profile simulations representing authentic customer sessions:
1. **Google Ads Paid Search to Legenda VIP Checkout**: Ad click with `gclid` -> lands on river hub -> compares in decision hub -> clicks Legenda checkout -> verifies partner `38585` and `subid` with encoded `gclid` -> verifies Meta Pixel `InitiateCheckout`.
2. **Meta Ads Retargeting to Candlelit Review**: Instagram story ad click -> lands on verified candlelit review -> checks canonical tag -> clicks TourCMS booking link -> verifies `agent_ref=38585` and net commission calculation.
3. **International Organic Visitor from Pruned Language**: Old indexed German slug request -> HTTP 301 redirect to canonical hub -> query string preserved -> navigation to Legenda terminal.
4. **Decision Hub Power User**: Interactive filters -> Vigadó tér Pier 7 dock guide -> verified anchor navigation -> zero DOMException errors.
5. **Search Engine Spider Crawl Audit**: Robots.txt -> Sitemap.xml -> validation of all canonical links -> zero `#` fragments -> zero ghost links.

---

## 3. How to Run the Tests

The test suite requires only Python 3 (built and verified with Python 3.9+).

```bash
# 1. Run all 280 test cases across Tiers 1-4
python3 tests/test_runner.py

# 2. Run a specific test tier
python3 tests/test_runner.py --tier 1    # Tier 1 Feature Coverage (130 tests)
python3 tests/test_runner.py --tier 2    # Tier 2 Boundary & Corner Cases (130 tests)
python3 tests/test_runner.py --tier 3    # Tier 3 Pairwise Combinations (15 tests)
python3 tests/test_runner.py --tier 4    # Tier 4 Real-World Journeys (5 tests)

# 3. Run tests for a specific feature (e.g. Feature 15: Legenda Partner ID Fix)
python3 tests/test_runner.py --feature 15

# 4. Run with detailed test-by-test verbose output
python3 tests/test_runner.py -v

# 5. Stop on first failure (fail-fast)
python3 tests/test_runner.py -x

# 6. Run live HTTP tests against a running preview server
python3 tests/test_runner.py --server-url http://localhost:3000

# 7. Export machine-readable JSON results
python3 tests/test_runner.py --json-report test_results.json
```

### Exit Codes
- `0`: All executed tests passed.
- `1`: One or more test assertions failed (implementation gaps identified).
- `2`: Configuration error or invalid arguments.

---

## 4. Discovered Implementation Defects & Milestone Roadmap

The initial test run establishes an exact, verifiable punchlist of 55 items for implementation workers:

### Milestone 1 Target Deficiencies
- `preview_server.py` does not yet exist.
- `vercel.json` uses deprecated `"routes"` schema instead of modern `"redirects"`, `"rewrites"`, and `"cleanUrls"`.
- Clean URL rewrites for `/budapest-river-cruises`, `/budapest-dinner-cruises`, and `/danube-cruise-decision-hub` are missing.

### Milestone 2 Target Deficiencies
- Dedicated `candlelit-dinner-cruise.html` static file does not yet exist at root.
- Root `index.html` currently contains an orphaned Prosecco cruise mockup rather than the comprehensive Danube River Cruises Hub (`river-ecom.html`).

### Milestone 3 Target Deficiencies
- Digits-first IDs exist in `dinner.html` (`1-Legenda`, `2-Silverline-no-show`) and `river.html` (`1-legenda`, `2-rubingroup`), crashing `document.querySelector()`.
- Local anchor `#silverline-folk` in `danube_cruise_decision_hub.html` points to a missing DOM element.
- `\u200d` zero-width joiners and unedited template strings ("Item #2 on this list") pollute `dinner.html`.
- Duplicate `id="faq"` exists in `dinner.html`.
- `sitemap.xml` contains 25 zero-click machine-translated languages (Thai, Arabic, Czech, Bulgarian, etc.).

### Milestone 4 Target Deficiencies
- Typo `partner=38885` exists in `legenda-city-cruises.html` (lines 365, 384, 403), misattributing sales away from Adam's VIP account `38585`.
- `danube_cruise_decision_hub.html` has un-tagged outbound links (`https://legenda.hu` and `https://silver-line.hu`) with no tracking parameters.
- Universal tracking script `bpa-tracking.js` is not yet deployed to capture UTMs, `gclid`, `fbclid`, and persist via dual cookie + localStorage.

### Milestone 5 Target Deficiencies
- 301 redirects for 25 pruned Linguana languages are missing from `vercel.json`.
- 1-to-1 mappings for known localized foreign slugs (e.g. `/de/donau-kreuzfahrten-budapest`) are not yet configured.

---

## 5. Artifact Index

- **`TEST_INFRA.md`**: Architectural specification, Category-Partition methodology, BVA domains, and feature inventory mapping.
- **`TEST_READY.md`**: Executive summary, command reference, baseline results, and defect catalog (this document).
- **`tests/test_runner.py`**: Zero-dependency CLI test runner supporting tier/feature filtering, JSON reporting, and live server testing.
- **`tests/common.py`**: Shared parsers (`HTMLDocumentParser`), `VercelConfigEvaluator`, `TrackingAttributionSimulator`, and assertion helpers (`BaseTestCase`).
- **`tests/tier1_feature_coverage.py`**: 130 atomic isolation tests covering Features 1-26.
- **`tests/tier2_boundary_corner.py`**: 130 BVA and edge case tests covering Features 1-26.
- **`tests/tier3_cross_feature.py`**: 15 pairwise interaction test cases.
- **`tests/tier4_real_world_scenarios.py`**: 5 end-to-end customer journey test cases.
