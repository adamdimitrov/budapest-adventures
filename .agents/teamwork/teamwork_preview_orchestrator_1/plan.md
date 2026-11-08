# Orchestration Plan — Budapest Adventures Staging Architecture Overhaul

## Objective
Establish a clean staging-first static architecture for `budapestadventures.com` on branch `staging/static-overhaul`, stripping DOM and anchor bloat, establishing 301 redirects for pruned zombie language routes, protecting Legenda/TourCMS tracking, and rebuilding core revenue hubs with local preview and Vercel staging deployment.

## Phase 0: Survey & Scope Mapping
- Spawn 3 parallel Explorers:
  - Explorer 1 (Survey: Codebase & Git Architecture): Branch state (`staging/static-overhaul`), repo file tree, existing static/HTML files, Vercel config, build/sync scripts (`tourcms-sync.js`, `test_tourcms.py`, etc.).
  - Explorer 2 (Survey: Route & SEO Anchor Inventory): Money hubs (`/`, `/budapest-river-cruises`, `/budapest-dinner-cruises`, `/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest`, `/legenda-city-cruises`, `danube_cruise_decision_hub.html`), Webflow `#` anchor fragments, TOC links, canonical tags, sitemap structure.
  - Explorer 3 (Survey: Tracking & i18n Redirects): Outbound booking links (Legenda, TourCMS, Tiqets partner `budapestadventures`), query string preservation (`gclid`, `fbclid`, UTMs), Meta Pixel InitiateCheckout triggers, Linguana routes vs `vercel.json` 301 redirects.
- Synthesize findings into `PROJECT.md` (Feature Inventory, Architecture, Interface Contracts, Milestones).

## Phase 1: Dual Track Launch
- **Track A (Implementation Track)**:
  - Milestone 1: Git Branching & Staging Foundation Setup (`staging/static-overhaul`, base directory structure, local preview server / Vercel config).
  - Milestone 2: Core Revenue Hubs Extraction & Anchor Cleaning (Semantic HTML5 IDs, zero `#` fragments in canonicals/TOC, clean canonical tags).
  - Milestone 3: Decision Hub & Interactive Engines (danube_cruise_decision_hub.html, filter logic, Meta Pixel InitiateCheckout tracking).
  - Milestone 4: Tracking & E-Commerce Safeguards (Legenda direct links, TourCMS sync/webhooks, Tiqets IDs, UTM/gclid/fbclid preservation).
  - Milestone 5: Internationalization Pruning & 301 Redirects (`vercel.json` 301 rules for pruned routes, sitemap.xml with canonical approved languages).
  - Milestone 6: Final Milestone — Pass 100% E2E Test Suite (Tiers 1-4) & Adversarial Hardening (Tier 5).
- **Track B (E2E Testing Track)**:
  - Spawn E2E Testing Orchestrator to build opaque-box test runner and 4-tier test suite.
  - Generates `TEST_INFRA.md` and signals completion via `TEST_READY.md`.

## Phase 2: Execution, Forensic Audit & Gate Verification
- Each milestone executes Explorer -> Worker -> Reviewers (2) -> Challengers (2) -> Auditor.
- Binary veto on forensic integrity violations.
- Final victory signoff to Sentinel.
