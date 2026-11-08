# DISPATCH — Worker M2 (Core Money Hubs Pipeline)

## Target
Execute Milestone 2: Rebuild and deploy all 5 core revenue hubs locally for staging preview without touching live DNS.

## 5 Core Revenue Hubs Scope
1. **Danube River Cruises Main Hub (`/` and `/budapest-river-cruises`)**:
   - Retire the obsolete Prosecco mockup in root `index.html`.
   - Promote clean `river-ecom.html` to root `index.html`.
   - Ensure `/` and `/budapest-river-cruises` both resolve to this clean hub.
2. **Budapest Dinner Cruises Hub (`/budapest-dinner-cruises`)**:
   - Ensure `dinner.html` is verified and routed from `/budapest-dinner-cruises` and `/best-dinner-cruises-budapest`.
3. **Candlelit Dinner Cruise Tested Review (`/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest`)**:
   - Assemble a dedicated static HTML file `candlelit-dinner-cruise.html`.
   - Extract tested review content, salon photo, review scores, food/menu details, and booking CTA from `dinner.html`, `article_embed_preview.html`, and components.
   - Verify route `/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest` rewrites to `candlelit-dinner-cruise.html`.
4. **Legenda City Cruises Dedicated Terminal (`/legenda-city-cruises`)**:
   - Ensure `legenda-city-cruises.html` is clean and correctly routed.
5. **Danube Cruise Decision Hub & Filter Engines (`danube_cruise_decision_hub.html`)**:
   - Ensure `danube_cruise_decision_hub.html` is clean and routed to `/danube-cruise-decision-hub` (and `/danube-river-cruise-hub`).

## Write Ownership
- `index.html`
- `candlelit-dinner-cruise.html`
- `dinner.html`
- `legenda-city-cruises.html`
- `danube_cruise_decision_hub.html`
- `vercel.json` (rewrites if needed)

## Mandatory Integrity Warning
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A forensic auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Instructions
1. Read `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/ORIGINAL_REQUEST.md`.
2. Read `/Users/adamdimitrov/Development/budapest-adventures/PROJECT.md`.
3. Read Survey Explorer 1 report at `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/teamwork_preview_explorer_survey_1/survey_codebase.md`.
4. Implement the 5 core money hubs cleanly in the working directory on branch `staging/static-overhaul`.
5. Verify with:
   - `python3 preview_server.py --check`
   - `python3 tests/test_runner.py --verbose --feature 4,5,6,7,8`
6. Verify live HTTP server responses for all 5 hubs return HTTP 200 with genuine content.
7. Document all commands, verification outputs, and files created/updated in `handoff.md`.
8. Notify the orchestrator via `send_message`.


## 2026-11-06T03:10:45Z
You are Worker M2 (Core Money Hubs Pipeline) for Budapest Adventures Staging Architecture Overhaul.
Your working directory is: `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/teamwork_preview_worker_m2_1`
Project root: `/Users/adamdimitrov/Development/budapest-adventures`
Mandatory: Read `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/ORIGINAL_REQUEST.md` before starting work.
Also read `/Users/adamdimitrov/Development/budapest-adventures/PROJECT.md` and your assignment in `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/teamwork_preview_worker_m2_1/DISPATCH.md`.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A forensic auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Your write ownership is strictly:
- `index.html`
- `candlelit-dinner-cruise.html`
- `dinner.html`
- `legenda-city-cruises.html`
- `danube_cruise_decision_hub.html`
- `vercel.json` (rewrites for core hubs)

Mission:
Rebuild and deploy the 5 core money hubs on branch `staging/static-overhaul`:
1. Danube River Cruises Main Hub (`/` and `/budapest-river-cruises`): promote clean `river-ecom.html` to root `index.html` (retiring obsolete Prosecco mockup).
2. Budapest Dinner Cruises Hub (`/budapest-dinner-cruises`): ensure `dinner.html` is verified and routed.
3. Candlelit Dinner Cruise Tested Review (`/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest`): build dedicated static page `candlelit-dinner-cruise.html` with complete tested review content, salon photo, scores, and booking CTA.
4. Legenda Dedicated Terminal (`legenda-city-cruises.html`): verify clean markup and routing.
5. Danube Cruise Decision Hub (`danube_cruise_decision_hub.html`): verify clean comparison hub and routing.

Run verification:
- `python3 preview_server.py --check`
- `python3 tests/test_runner.py --verbose --feature 4,5,6,7,8`
Document all verification commands and outputs in `handoff.md` and notify orchestrator via `send_message`.
