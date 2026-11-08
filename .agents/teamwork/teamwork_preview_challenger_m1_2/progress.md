# Progress — Challenger M1 (2)

Last visited: 2026-11-06T02:51:00Z

- [x] Initialized BRIEFING.md and DISPATCH.md
- [x] Inspected git branch status and vercel.json structure: confirmed branch `staging/static-overhaul` and modern schema
- [x] Ran test runner: `python3 tests/test_runner.py --tier 1` (89 passed, 41 failed due to M2-M4 scope)
- [x] Ran M1 feature tests: F1, F2, F3, F21, F22, F23 pass 60/60 (100%)
- [x] Ran preview_server self-diagnostics: 40/40 checks passed
- [x] Adversarial stress-test: 25 pruned languages
  - Found routing order bug: `preview_server.py` evaluates trailingSlash before configured redirects, causing `/{lang}/` (`/ru/`, `/zh/`, `/pl/`, etc.) to return HTTP 308 to `/{lang}` instead of HTTP 301 to `/` (2-hop redirect chain).
- [x] Adversarial stress-test: 5 core money hubs rewrite resolution verified (all 5 resolve to target HTML files)
- [x] Adversarial stress-test: Security headers validation (present on 200, 301, 308, 404 responses over live HTTP sockets)
- [x] Adversarial stress-test: Inbound query preservation verified (`utm_*`, `gclid`, `fbclid` retained across redirects)
- [x] Final verdict formulated: REQUEST_CHANGES (with drop-in fix for `preview_server.py`)
