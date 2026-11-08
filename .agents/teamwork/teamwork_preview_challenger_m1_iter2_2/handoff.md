# Handoff Report — Challenger 2 (Milestone 1 Iteration 2 Priority & Language Redirects Test)

**Agent**: Challenger 2 (`teamwork_preview_challenger_m1_iter2_2`)  
**Roles**: critic, specialist  
**Recipient**: Orchestrator (`d93f7e16-54b1-470e-ae73-62c9d55a912a`)  
**Date**: 2026-11-06T03:09:00Z  
**Verdict**: **APPROVE**

---

## 1. Observation

### 1.1 Direct Empirical Verification of Dispatch Mission

The orchestrator tasked Challenger 2 with:
1. Empirically verifying priority order and 25 pruned language redirects following Worker M1 Iteration 2 fixes.
2. Verifying that `/ru/`, `/zh/`, `/cs/` return direct HTTP 301 to `/` without 2-hop 308 redirect.
3. Verifying tests with `python3 tests/test_runner.py --feature 1,2,3,21,22,23`.

#### Direct Probes on Mandatory Target Languages (`/ru/`, `/zh/`, `/cs/`):
Live socket requests against `http://127.0.0.1:3888` (PID 77320) returned:
- `GET /ru/ HTTP/1.1` -> Status: **HTTP 301 Moved Permanently**, `Location: /` (Direct 1-Hop, 0 trailing-slash 308 intermediates).
- `GET /zh/ HTTP/1.1` -> Status: **HTTP 301 Moved Permanently**, `Location: /` (Direct 1-Hop).
- `GET /cs/ HTTP/1.1` -> Status: **HTTP 301 Moved Permanently**, `Location: /` (Direct 1-Hop).

#### Verification of All 25 Pruned Languages:
All 25 pruned language roots (`cs`, `bg`, `zh`, `vi`, `uk`, `ar`, `sv`, `sr`, `el`, `fi`, `da`, `th`, `hr`, `nl`, `no`, `sk`, `tr`, `ko`, `ru`, `pt`, `ja`, `ro`, `he`, `pl`, `hu`):
- Both trailing slash (`/{lang}/`) and bare root (`/{lang}`) return HTTP 301 with `Location: /` (50/50 PASS).
- Inbound query parameters (`?utm_source=meta...`, `?gclid=123...`) are fully preserved in `Location: /?...` (12/12 PASS).
- Subpath catch-all routes (`/{lang}/:path*`) redirect with HTTP 301 to `/:path*` (40/40 PASS).

#### Core Money Hubs Rewrites & 308 Trailing Slash Handling:
- `GET /` -> HTTP 200 `text/html; charset=utf-8` (serves `index.html`, 1,027 bytes).
- `GET /budapest-river-cruises` -> HTTP 200 `text/html; charset=utf-8` (serves `index.html`).
- `GET /budapest-dinner-cruises` -> HTTP 200 `text/html; charset=utf-8` (serves `dinner.html`, 8,822 bytes).
- `GET /legenda-city-cruises` -> HTTP 200 `text/html; charset=utf-8` (serves `legenda-city-cruises.html`, 14,082 bytes).
- `GET /danube-cruise-decision-hub` -> HTTP 200 `text/html; charset=utf-8` (serves `danube_cruise_decision_hub.html`, 18,740 bytes).
- Trailing slashes on non-pruned money hubs (`/legenda-city-cruises/`, `/budapest-dinner-cruises/`, etc.) return HTTP 308 stripping the trailing slash (4/4 PASS).
- Clean URL extension stripping (`GET /dinner.html`) returns HTTP 308 with `Location: /dinner` (PASS).

#### Security & Boundary Defenses:
- `GET /../../../../etc/passwd` -> HTTP 404 (Path traversal blocked, 0 bytes of sensitive files).
- `GET /.git/config` -> HTTP 404 (Dotfile suppressed).
- `GET //legenda-city-cruises` -> HTTP 200 (Multi-slash normalized, serves Legenda terminal).
- `GET /cs/test\x` -> Handled safely without `re.error` 500 crash.

---

### 1.2 Test Suite Execution Logs

#### 1. Preview Server Self-Diagnostics:
Command: `python3 preview_server.py --check`
```
======================================================================
BUDAPEST ADVENTURES — PREVIEW SERVER SELF-DIAGNOSTICS
Project Root: /Users/adamdimitrov/Development/budapest-adventures
Config File:  /Users/adamdimitrov/Development/budapest-adventures/vercel.json
======================================================================
[Phase 1: vercel.json Schema Validation]          7/7 checks passed
[Phase 2: Core Money Hubs Rewrites Resolution]    10/10 checks passed
[Phase 3: Redirects, CleanUrls & Query String]    15/15 checks passed
[Phase 4: Security Headers Verification]          3/3 checks passed
[Phase 5: Static File On-Disk Verification]       4/4 checks passed (1 pending M2)
[Phase 6: Adversarial & Boundary Safety]          8/8 checks passed
======================================================================
DIAGNOSTIC SUMMARY: 48/48 CHECKS PASSED (EXIT 0)
======================================================================
```

#### 2. E2E Test Runner Composite Command:
Command: `python3 tests/test_runner.py --verbose --feature 1,2,3,21,22,23`
```
==============================================================================
 BUDAPEST ADVENTURES — STAGING ARCHITECTURE E2E TEST RUNNER
 Selected Tiers: [1, 2, 3, 4] | Feature Filter: 1,2,3,21,22,23
 Total Tests Discovered: 60
==============================================================================
--- Tier 1: Feature Coverage (Category-Partition) --- 30/30 PASS
--- Tier 2: Boundary & Corner Cases (BVA) ---         30/30 PASS
==============================================================================
 TEST EXECUTION SUMMARY: 60/60 PASSED (100.0%), 0 FAILED (0.04s, EXIT 0)
==============================================================================
```

#### 3. Adversarial Security Suite:
Command: `python3 tests/test_adversarial_m1.py`
```
======================================================================
TOTAL ADVERSARIAL CHECKS: 19
PASSED: 19 | FAILED: 0 (Critical: 0, High: 0) (EXIT 0)
======================================================================
```

#### 4. Challenger 2 Dedicated Stress Test Suite:
Command: `python3 tests/test_challenger_m1_iter2.py`
```
================================================================================
VERIFICATION SUMMARY: 180/180 CHECKS PASSED (0 FAILED)
ALL EMPIRICAL CHECKS PASSED CLEANLY (EXIT 0)
================================================================================
```

---

### 1.3 Adversarial Findings (Milestone 5 Scope)

Through white-box rule inspection and socket fuzzing, Challenger 2 discovered two latent defects in `vercel.json` and `preview_server.py`. These do not block Milestone 1 (which only scopes the routing engine base and staging isolation; full localized slug pruning is scheduled for Milestone 5), but require documented remediation in Milestone 5:

#### Finding 1: Dinner Cruise Slug Shadowing in `vercel.json`
- **Location**: `vercel.json:43, 169, 181, 193, 319, 331`
- **Observation**:
  - Czech: Line 43 defines `"source": "/cs/nejlep:slug(.*)"` -> `/budapest-river-cruises`. Line 193 defines `"source": "/cs/nejlepší-večeře:slug(.*)"` -> `/budapest-dinner-cruises`. Because `nejlepší-večeře` begins with `nejlep`, line 43 matches first! Czech users visiting the dinner cruise slug are erroneously redirected to the river cruises hub.
  - Romanian: Line 169 defines `"source": "/ro/croaziera-dunare:slug(.*)"` -> `/budapest-river-cruises`. Line 319 defines `"source": "/ro/croaziera-dunare-cu-cina:slug(.*)"` -> `/budapest-dinner-cruises`. Because `croaziera-dunare-cu-cina` begins with `croaziera-dunare`, line 169 matches first! Line 319 is unreachable dead code.
  - Polish: Line 181 defines `"source": "/pl/rejsy-dunaju-budapeszt:slug(.*)"` -> `/budapest-river-cruises`. Line 331 defines `"source": "/pl/rejsy-dunaju-budapeszt-kolacja:slug(.*)"` -> `/budapest-dinner-cruises`. Line 181 matches first, shadowing line 331.
- **Severity**: MEDIUM (scheduled for Milestone 5).
- **Mitigation for M5**: Re-order the rules in `vercel.json` so that the more specific dinner cruise slugs precede the general river cruise slugs, or tighten river slug patterns to exact segment boundaries (e.g. `^/ro/croaziera-dunare(?:/|$)`).

#### Finding 2: URL Decoding Prior to Regex Evaluation in `preview_server.py`
- **Location**: `preview_server.py:165, 170`
- **Observation**: `preview_server.resolve_request` matches `raw_path` without unquoting. Standard HTTP clients send percent-encoded non-ASCII characters (`/bg/%D0%BD...`). Vercel's production routing engine unquotes pathnames before matching `redirects` patterns.
- **Severity**: LOW (scheduled for Milestone 5).
- **Mitigation for M5**: In `resolve_request`, evaluate redirect patterns against both `raw_path` and `urllib.parse.unquote(raw_path)`.

---

## 2. Logic Chain

1. **Elimination of the 2-Hop 308->301 Redirect Defect**:
   - In pre-remediation state, `trailingSlash: false` check ran at line 170 before `redirect_rules`, turning `GET /ru/` into `308 /ru`, followed by `301 /`.
   - In post-remediation `preview_server.py:168-184`, `config.redirect_rules` is evaluated as Step 1.
   - Socket requests to `/ru/`, `/zh/`, `/cs/`, and all 25 pruned languages directly match their configured rules and return HTTP 301 with `Location: /` in exactly 1 hop.
   - Direct verification: 50/50 language root checks passed.

2. **Priority Order Compliance**:
   - Vercel specification states `redirects` take precedence over filesystem cleanUrls and trailing slash normalization.
   - In `preview_server.py`, the evaluation sequence is now:
     1. Configured Redirects (`config.redirect_rules`)
     2. Trailing Slash Normalization (`trailingSlash: false` -> 308)
     3. Clean URLs (`cleanUrls: true` -> 308)
     4. Configured Rewrites (`config.rewrite_rules`)
     5. Static Filesystem Resolution
   - Direct verification: Trailing slash redirects on pruned languages trigger 301, while trailing slash on clean money hubs (`/legenda-city-cruises/`) triggers 308.

3. **E2E Test Runner Filter Compatibility**:
   - Worker M1 Iteration 2 updated `tests/test_runner.py`'s `--feature` argument to parse comma-separated integers (`1,2,3,21,22,23`).
   - Direct verification: `python3 tests/test_runner.py --verbose --feature 1,2,3,21,22,23` runs 60 tests across Tiers 1 and 2, passing 100% in 0.04s.

4. **Safety & Zero Regressions**:
   - Path traversal and dotfile checks continue to return HTTP 404.
   - Multi-slash leading normalization prevents `urlsplit` netloc hijacking.
   - Direct verification: 19/19 checks pass in `test_adversarial_m1.py`.

---

## 3. Caveats

- **Scope Boundary**: Findings regarding shadowed dinner cruise slugs (`nejlep`, `croaziera-dunare`, `rejsy-dunaju-budapeszt`) and non-ASCII URL decoding belong formally to **Milestone 5 (i18n Pruning & 301 Redirect Architecture)** as defined in `PROJECT.md:63`. They do not impede Milestone 1 approval.
- **Pending Milestone 2 Static Assets**: `candlelit-dinner-cruise.html` does not yet exist on disk, as it is scheduled for implementation in Milestone 2. Its routing rewrite is verified in `preview_server.py` and `vercel.json`.
- **DNS Isolation**: Verified that live production DNS (`35.187.176.9`) has not been modified. All testing was executed strictly on local socket `127.0.0.1:3888` on the `staging/static-overhaul` branch.

---

## 4. Conclusion

**Verdict**: **APPROVE**

Worker M1 Iteration 2 has completely resolved the 2-hop redirect defect and aligned `preview_server.py` priority evaluation with the Vercel routing engine specification:
- `/ru/`, `/zh/`, `/cs/` and all 25 pruned languages return direct 1-hop HTTP 301 to `/`.
- Priority order evaluates custom redirects before trailing-slash stripping and cleanUrls.
- Inbound query strings (`gclid`, `fbclid`, UTMs) are preserved without dropping existing parameters.
- `python3 preview_server.py --check` passes 48/48 checks.
- `python3 tests/test_runner.py --feature 1,2,3,21,22,23` passes 60/60 tests (100%).
- `python3 tests/test_adversarial_m1.py` passes 19/19 checks (100%).
- `python3 tests/test_challenger_m1_iter2.py` passes 180/180 checks (100%).

Milestone 1 is verified and approved to proceed to Milestone 2.

---

## 5. Verification Method

To independently reproduce Challenger 2's empirical findings:

1. **Run Preview Server Diagnostics**:
   ```bash
   python3 preview_server.py --check
   ```
   *Expected*: `DIAGNOSTIC SUMMARY: 48/48 CHECKS PASSED`, Exit 0.

2. **Run E2E Test Runner Composite Command**:
   ```bash
   python3 tests/test_runner.py --verbose --feature 1,2,3,21,22,23
   ```
   *Expected*: `60/60 PASSED (100.0%)`, Exit 0.

3. **Run Adversarial Security Suite**:
   ```bash
   python3 tests/test_adversarial_m1.py
   ```
   *Expected*: `19/19 checks passed`, Exit 0.

4. **Run Challenger 2 Dedicated Verification Harness**:
   ```bash
   python3 tests/test_challenger_m1_iter2.py
   ```
   *Expected*: `180/180 checks passed`, Exit 0.

5. **Direct Single-Hop Probe Verification**:
   ```bash
   curl -s -i http://127.0.0.1:3888/ru/ | grep -E "HTTP/|Location:"
   curl -s -i http://127.0.0.1:3888/zh/ | grep -E "HTTP/|Location:"
   curl -s -i http://127.0.0.1:3888/cs/ | grep -E "HTTP/|Location:"
   ```
   *Expected Output for each probe*:
   ```
   HTTP/1.0 301 Moved Permanently
   Location: /
   ```
