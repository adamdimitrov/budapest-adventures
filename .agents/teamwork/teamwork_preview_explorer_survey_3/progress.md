# Progress — Explorer Survey 3 (Tracking Safeguards & Internationalization Pruning)

- Last visited: 2026-11-06T02:29:00Z
- Status: Investigation and synthesis complete. Compiling survey report.
- Steps:
  - [x] Read ORIGINAL_REQUEST.md, GEMINI.md, DISPATCH.md
  - [x] Initialized BRIEFING.md and progress.md
  - [x] Investigate project directory structure and files
  - [x] Inspect outbound booking links (Legenda 38585 vs 38885 typo, TourCMS 16485/57509, Tiqets, Silverline, BudapestXplore)
  - [x] Inspect query string preservation scripts & logic (tourcms-sync.js, missing UTM capture, missing cookie fallbacks, interactive DOM bypass)
  - [x] Inspect Meta Pixel tracking & InitiateCheckout triggers (Pixel ID 1355732169631751 vs 889886707052830, value net vs gross discrepancy)
  - [x] Audit Linguana multilingual routes (30 total languages: 5 approved en/de/it/fr/es, 25 pruned zombie languages)
  - [x] Check vercel.json routes conflict and formulate complete 301/308 redirect mapping
  - [ ] Compile comprehensive `survey_tracking_i18n.md`
  - [ ] Update `BRIEFING.md`
  - [ ] Write `handoff.md` and send report to orchestrator
