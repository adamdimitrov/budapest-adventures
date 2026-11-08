# BRIEFING — 2026-11-06T02:30:30Z

## Mission
Audit and document outbound booking links (Legenda, TourCMS, Tiqets), query parameter preservation, Meta Pixel InitiateCheckout tracking, and Linguana multilingual routing/redirect architecture for Budapest Adventures staging overhaul.

## 🔒 My Identity
- Archetype: explorer
- Roles: survey, tracking safeguards, internationalization audit
- Working directory: /Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/teamwork_preview_explorer_survey_3
- Original parent: d93f7e16-54b1-470e-ae73-62c9d55a912a
- Milestone: Survey & Audit Phase Complete

## 🔒 Key Constraints
- Read-only investigation — do NOT implement changes in source code
- Work only in own working directory (`.agents/teamwork/teamwork_preview_explorer_survey_3`)
- Never touch live production DNS (`35.187.176.9`)
- Strict objectivity, candor, direct analysis, no sycophancy

## Current Parent
- Conversation ID: d93f7e16-54b1-470e-ae73-62c9d55a912a
- Updated: 2026-11-06T02:30:30Z

## Investigation State
- **Explored paths**:
  - `river.html`, `river-ecom.html`, `river_desktop_wide_preview.html`
  - `dinner.html`, `dinner_desktop_wide_preview.html`, `live_dinner_embed.html`
  - `legenda-city-cruises.html`, `legenda.html`, `direct_checkout_mockup.html`
  - `danube_cruise_decision_hub.html`, `index.html`, `things-to-do.html`
  - `tourcms-sync.js`, `api/cron.py`, `tourcms_test.py`, `test_tourcms.py`
  - `ratings.json`, `webflow-ratings.js`, `pages.json`, `vercel.json`, `.env`
- **Key findings**:
  1. Critical Legenda partner ID typo in `legenda-city-cruises.html`: `partner=38885` instead of verified `38585`.
  2. `danube_cruise_decision_hub.html` has bare affiliate links (`legenda.hu`, `silver-line.hu`), no tracking script, and no Meta Pixel.
  3. `tourcms-sync.js` fails to capture or persist UTM parameters (`utm_source`, etc.).
  4. Vercel schema conflict: `routes` cannot coexist with `redirects`/`rewrites` in `vercel.json`.
  5. Linguana has 30 languages: 5 to retain (`en`, `de`, `it`, `fr`, `es`), 25 to prune via explicit 301 mappings.
  6. Value discrepancy: client-side `InitiateCheckout` (gross retail vs net commission) vs backend CAPI `Purchase` (net commission).
- **Unexplored areas**:
  - Live DNS propagation (strictly out of scope for staging phase).

## Key Decisions Made
- Formulated complete 1-to-1 301/308 redirect mapping for all 25 pruned languages to prevent 404 crawl errors.
- Designed enhanced `bpa-tracking.js` specification to unify UTM capture, cookie/localStorage persistence, and multi-partner link decoration.
- Standardized conversion values on net commission margin (25%) to harmonize client Pixel and backend CAPI bidding.

## Artifact Index
- `DISPATCH.md` — Incoming dispatch instructions & timestamp log
- `BRIEFING.md` — Persistent working memory
- `progress.md` — Liveness heartbeat
- `survey_tracking_i18n.md` — Comprehensive survey report (7 sections)
- `handoff.md` — 5-component handoff report for orchestrator
