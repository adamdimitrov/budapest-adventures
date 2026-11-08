# BRIEFING — 2026-11-06T02:30:00Z

## Mission
Investigate git status, repo layout, 5 core money hubs, Vercel config, TourCMS/sync scripts, and local preview staging architecture for Budapest Adventures static overhaul.

## 🔒 My Identity
- Archetype: explorer
- Roles: Codebase Structure & Staging Pipeline Survey
- Working directory: /Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/teamwork_preview_explorer_survey_1
- Original parent: d93f7e16-54b1-470e-ae73-62c9d55a912a
- Milestone: Milestone 1 - Architectural Survey & Staging Plan

## 🔒 Key Constraints
- Read-only investigation — do NOT modify project source code
- Only write within working directory (.agents/teamwork/teamwork_preview_explorer_survey_1)
- Objective, candid, direct demeanor with zero fluff or sycophancy

## Current Parent
- Conversation ID: d93f7e16-54b1-470e-ae73-62c9d55a912a
- Updated: 2026-11-06T02:30:00Z

## Investigation State
- **Explored paths**:
  - `git status`, `git branch -a`, `git log`
  - 38 HTML files in repo root (`index.html`, `river.html`, `river-ecom.html`, `dinner.html`, `legenda-city-cruises.html`, `danube_cruise_decision_hub.html`, etc.)
  - `vercel.json`, `pages.json`, `ratings.json`
  - `tourcms-sync.js`, `api/cron.py`, `sync_ratings.sh`, `update_ratings.py`, `test_tourcms.py`
  - Production DNS / HTTP response checks (`35.187.176.9`)
- **Key findings**:
  - Branch `staging/static-overhaul` does NOT exist; must be created from `main`.
  - 5 tracked uncommitted files on `main`, 40+ untracked files.
  - 5 Core Money Hubs mapped:
    1. Danube River Cruises Main Hub: `river.html` / `river-ecom.html`. (Vercel `index.html` has prosecco mockup collision; `/budapest-river-cruises` is 404 on live).
    2. Budapest Dinner Cruises Hub: `dinner.html` (`/best-dinner-cruises-budapest`).
    3. Candlelit Dinner Review: embedded in `dinner.html` and components; needs dedicated standalone HTML file.
    4. Legenda City Cruises Terminal: `legenda-city-cruises.html` (fully implemented with TourCMS & Meta Pixel).
    5. Danube Cruise Decision Hub: `danube_cruise_decision_hub.html` (fully implemented with Tailwind & schema).
  - TourCMS attribution pipeline: client-side cookie persistence in `tourcms-sync.js` (subid, agent_ref, InitiateCheckout) + backend serverless sync in `api/cron.py`.
  - Preview runtime: Node/npm not in PATH; Python 3.9.6 available for zero-dependency staging preview server.
- **Unexplored areas**: None for codebase survey; complete.

## Key Decisions Made
- Fully documented codebase structure and staging plan in `survey_codebase.md`.
- Recommended Python-based preview server runner due to lack of Node in system PATH.
- Preserved read-only discipline on source files.

## Artifact Index
- survey_codebase.md — Comprehensive codebase survey report (13KB)
- handoff.md — 5-component handoff report
- progress.md — Liveness heartbeat
