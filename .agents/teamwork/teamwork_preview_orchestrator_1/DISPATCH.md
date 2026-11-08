# Dispatch Log

## 2026-11-06T02:21:05Z
You are the Project Orchestrator for the Budapest Adventures Staging Architecture Overhaul.

Your Working Directory: `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/teamwork_preview_orchestrator_1`
Project Root: `/Users/adamdimitrov/Development/budapest-adventures`
Original Request File: `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/ORIGINAL_REQUEST.md`

Your Mission:
Coordinate the full multi-agent static architecture overhaul for Budapest Adventures (`budapestadventures.com`) on a dedicated branch (`staging/static-overhaul`).

Key Requirements to Decompose and Execute:
1. R1. Staging Isolation & Core Money Hubs Pipeline:
   - Dedicated branch `staging/static-overhaul`
   - Rebuild core revenue hubs locally for instant Vercel preview without modifying live production DNS (35.187.176.9 / Linguana / Webflow):
     - Danube River Cruises Main Hub (/ and /budapest-river-cruises)
     - Budapest Dinner Cruises Hub (/budapest-dinner-cruises)
     - Candlelit Dinner Cruise Tested Review (/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest)
     - Legenda City Cruises Dedicated Terminal (/legenda-city-cruises)
     - Danube Cruise Decision Hub & Filter Engines (danube_cruise_decision_hub.html)
2. R2. HCU & Webflow Anchor Pollution Elimination:
   - Strip all legacy Webflow table-of-contents hash fragments (#...), unicode artifacts, and duplicated CMS anchor IDs.
   - Clean semantic HTML5 IDs and self-referencing canonical tags pointing strictly to clean root URLs.
3. R3. Internationalization Pruning & 301 Redirect Architecture:
   - Audit Linguana multilingual routes: retain high-volume converting languages (en, de, it, fr, es) while pruning zero-click automated machine-translated zombie paths.
   - Comprehensive 301/308 redirect mapping in `vercel.json` pointing all pruned paths back to canonical targets.
4. R4. Legenda (€130k VIP Channel) & TourCMS Tracking Safeguards:
   - 100% verification that all outbound Legenda booking links, TourCMS API webhooks, and Tiqets partner IDs (budapestadventures) retain complete tracking query strings (gclid, fbclid, UTMs).
   - Verify Meta Pixel InitiateCheckout tracking triggers on all interactive decision cards and reservation buttons.

Operating Directives:
- Write coordination files (plan.md, progress.md, BRIEFING.md) ONLY in your working directory (`/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/teamwork_preview_orchestrator_1`).
- Keep `progress.md` updated continuously so sentinel liveness and progress monitors detect active work.
- When all acceptance criteria are met, report victory/completion to the Sentinel. Victory audit is mandatory before final signoff.
