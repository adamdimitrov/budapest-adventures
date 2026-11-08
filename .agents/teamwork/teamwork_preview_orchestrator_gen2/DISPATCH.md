# DISPATCH — Project Orchestrator (Generation 2)

## Mission
Resume Project Orchestrator duties for Budapest Adventures Staging Architecture Overhaul.
Your Parent Conversation ID is `40f3afb7-d012-4ac6-8e24-b01d81ea518b` (Sentinel).

## Context & State
- Read `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/ORIGINAL_REQUEST.md` (authoritative request).
- Read `/Users/adamdimitrov/Development/budapest-adventures/PROJECT.md` (global architecture, feature inventory, milestones, contracts).
- Read `/Users/adamdimitrov/Development/budapest-adventures/TEST_INFRA.md` & `TEST_READY.md`.
- Read soft handoff from predecessor: `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/teamwork_preview_orchestrator_1/handoff.md`.
- Read predecessor briefing: `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/teamwork_preview_orchestrator_1/BRIEFING.md`.

## Immediate Assignment
- Milestone 1 is **DONE** and passed gate verification (staging branch `staging/static-overhaul`, modern `vercel.json`, and zero-dependency `preview_server.py`).
- Execute **Milestone 2 (Core Money Hubs Pipeline)**:
  1. Rebuild and deploy the 5 core money hubs:
     - Replace Prosecco mockup at `/` with clean Danube River Cruises Main Hub (`river-ecom.html`).
     - Deploy Budapest Dinner Cruises Hub (`dinner.html`) to `/budapest-dinner-cruises` and `/best-dinner-cruises-budapest`.
     - Assemble and deploy Candlelit Dinner Cruise Tested Review static page at `candlelit-dinner-cruise.html` (mapped to `/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest`).
     - Verify Legenda Dedicated Terminal (`legenda-city-cruises.html`).
     - Verify Danube Cruise Decision Hub (`danube_cruise_decision_hub.html`).
  2. Run the Iteration Loop for Milestone 2: Explorer -> Worker -> Reviewers (2) -> Challengers (2) -> Forensic Auditor. Strict AND gate.
  3. Proceed sequentially through Milestones 3, 4, 5, and Milestone 6 (100% E2E test pass + Tier 5 adversarial hardening) to final victory signoff.
