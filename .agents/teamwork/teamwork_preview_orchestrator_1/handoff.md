# Orchestrator Soft Handoff (Generation 1 → Generation 2)

**Timestamp**: 2026-11-06T03:09:30Z  
**From**: Project Orchestrator Gen 1 (`teamwork_preview_orchestrator_1`)  
**To**: Project Orchestrator Gen 2 (Successor)  
**Parent Conversation ID**: `40f3afb7-d012-4ac6-8e24-b01d81ea518b` (Sentinel)

---

## 1. Milestone State

| Milestone | Name | Status | Verified Deliverables |
|-----------|------|--------|------------------------|
| **Phase 0** | Survey & Scope Mapping | **DONE** | Full reports from 3 Explorers (`survey_codebase.md`, `survey_seo_anchors.md`, `survey_tracking_i18n.md`), `PROJECT.md` initialized with 26-feature inventory. |
| **Track B** | E2E Testing Track | **DONE** | `TEST_INFRA.md` published, `tests/test_runner.py` with 280 tests across Tiers 1-4, `TEST_READY.md` published. |
| **M1** | Staging Isolation & Local Preview Server | **DONE** (Gate: PASS) | Git branch `staging/static-overhaul`, modern `vercel.json` (cleanUrls, redirects, rewrites, headers), `preview_server.py` with bounds checking (`is_relative_to`), dotfile suppression, 1-hop redirect evaluation order. All 48 self-checks, 60 test_runner tests, and 19 adversarial tests pass 100%. Live DNS `35.187.176.9` untouched. |
| **M2** | Core Money Hubs Pipeline | **READY** | Source files mapped: `river-ecom.html` -> `/`, `dinner.html` -> `/budapest-dinner-cruises`, `candlelit-dinner-cruise.html` -> `/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest`, `legenda-city-cruises.html` -> `/legenda-city-cruises`, `danube_cruise_decision_hub.html`. |
| **M3** | HCU, Anchor Pollution & Canonicals | **PLANNED** | Ready to follow M2. Clean digits-first IDs, strip `#` fragments, sitemap generation. |
| **M4** | Tracking Safeguards & VIP Attribution | **PLANNED** | Fix Legenda typo `38885` -> `38585`, Decision Hub tracking injection, `bpa-tracking.js`, Meta Pixel `1355732169631751`. |
| **M5** | i18n Pruning & 301 Redirect Architecture | **PLANNED** | 25 zombie languages pruned, complete 1-to-1 redirects in `vercel.json`. |
| **M6** | Final Milestone: E2E Test Pass & Hardening | **PLANNED** | Pass 100% of 280 E2E tests + Tier 5 Adversarial Hardening. |

---

## 2. Active Subagents

All 16 subagents spawned by Gen 1 have delivered their handoffs and are permanently retired. There are currently **0** active subagents running.

---

## 3. Pending Decisions & Critical Context

1. **Legenda €130k VIP Channel ID**: The correct partner ID is **`38585`**. Do NOT use `38885` (which was a typo found in legacy `legenda-city-cruises.html:365,384,403`).
2. **Meta Pixel ID**: Standardized strictly on **`1355732169631751`** (the active production Pixel). Retire legacy `889886707052830`.
3. **Live DNS Isolation**: `35.187.176.9` (Linguana / Webflow) must remain untouched. All work lives on `staging/static-overhaul`.
4. **Vercel Modern Schema**: `vercel.json` already uses the modern top-level format (`cleanUrls: true`, `trailingSlash: false`, `headers`, `rewrites`, `redirects`). Do NOT reintroduce legacy `"routes"`.
5. **Preview Server**: Local Python preview server is `python3 preview_server.py [PORT]` with `--check` self-diagnostic.
6. **Test Runner**: Run tests using `python3 tests/test_runner.py` (accepts `--feature 1,2,3`, `--tier 1`, `--verbose`).

---

## 4. Remaining Work (Concrete Next Steps for Gen 2)

Your immediate focus is **Milestone 2 (Core Money Hubs Pipeline)**:
1. **Milestone 2 Dispatch**:
   - Spawn an Explorer or proceed to Worker dispatch for M2.
   - Rebuild/place the 5 core money hubs:
     - Replace obsolete Prosecco mockup in root `index.html` with clean Danube River Cruises Main Hub (`river-ecom.html`).
     - Map/deploy Budapest Dinner Cruises Hub (`dinner.html`) to `/budapest-dinner-cruises` and `/best-dinner-cruises-budapest`.
     - Assemble and deploy dedicated static Candlelit Dinner Cruise Tested Review page at `candlelit-dinner-cruise.html` (mapped to `/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest`).
     - Verify Legenda Terminal (`legenda-city-cruises.html`).
     - Verify Danube Cruise Decision Hub (`danube_cruise_decision_hub.html`).
   - Run Gate verification for M2: Worker -> Reviewers (2) -> Challengers (2) -> Forensic Auditor.
2. **Follow with Milestones 3, 4, 5**:
   - M3: HCU & Anchor Pollution Cleanup (strip `#` fragments, semantic IDs, canonicals, sitemap).
   - M4: Tracking Safeguards (correct Legenda ID `38585`, plug Decision Hub tracking bleed, UTM/click ID persistence, Meta Pixel `1355732169631751`).
   - M5: i18n Pruning & 301 Redirect Architecture (25 zombie languages 301 redirects in `vercel.json`).
3. **Final Milestone 6**:
   - Run full E2E test suite (`python3 tests/test_runner.py`) until 100% pass (0 failures).
   - Adversarial coverage hardening (Tier 5).
   - Final Forensic Audit signoff and victory report to Sentinel (`40f3afb7-d012-4ac6-8e24-b01d81ea518b`).

---

## 5. Key Artifacts

- `/Users/adamdimitrov/Development/budapest-adventures/PROJECT.md` — Global architecture, feature inventory, milestones, contracts
- `/Users/adamdimitrov/Development/budapest-adventures/TEST_INFRA.md` — E2E test architecture and methodology
- `/Users/adamdimitrov/Development/budapest-adventures/TEST_READY.md` — E2E test runner documentation and baseline status
- `/Users/adamdimitrov/Development/budapest-adventures/preview_server.py` — Local Vercel-compatible staging server
- `/Users/adamdimitrov/Development/budapest-adventures/vercel.json` — Modern Vercel routing and redirect configuration
- `/Users/adamdimitrov/Development/budapest-adventures/tests/test_runner.py` — Python E2E test runner
- `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/teamwork_preview_orchestrator_1/GATE_STATUS.md` — M1 Gate record (PASS)
- `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/ORIGINAL_REQUEST.md` — Authoritative user requirements

---

## 6. Logic Chain & Verification Method

- **Observation**: Milestone 1 complete. Git branch `staging/static-overhaul` established; `vercel.json` and `preview_server.py` verified across 48 internal checks, 60 feature tests, and 19 adversarial tests.
- **Verification Commands**:
  - `python3 preview_server.py --check` -> 48/48 PASS
  - `python3 tests/test_runner.py --verbose --feature 1,2,3,21,22,23` -> 60/60 PASS
  - `python3 tests/test_adversarial_m1.py` -> 19/19 PASS
- **Verdict**: Milestone 1 GATE PASS. Ready for Milestone 2 dispatch.
