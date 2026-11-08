# DISPATCH — Forensic Auditor (Milestone 2 Integrity Verification)

## Mission
Forensically audit Milestone 2 deliverables across the 5 core money hubs (`index.html`, `dinner.html`, `candlelit-dinner-cruise.html`, `legenda-city-cruises.html`, `danube_cruise_decision_hub.html`).

## Instructions
1. Read `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/ORIGINAL_REQUEST.md`.
2. Read `/Users/adamdimitrov/Development/budapest-adventures/PROJECT.md`.
3. Read Worker M2 handoff at `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/teamwork_preview_worker_m2_1/handoff.md`.
4. Forensic integrity checks:
   - Verify that all 5 hubs contain genuine, full, authentic HTML markup and real editorial copy (not dummy text, empty shells, or facade pages).
   - Check `candlelit-dinner-cruise.html`: verify authentic review content, real menu details, valid schema, real photo references.
   - Check partner links: verify genuine URLs without tampering.
   - Confirm live production DNS (`35.187.176.9` / Linguana / Webflow) is 100% untouched.
5. Issue an unambiguous binary forensic verdict:
   - `CLEAN` (authentic implementation, zero violations)
   - `INTEGRITY VIOLATION` (cheating, facade, dummy placeholders detected)
6. Write `handoff.md` and notify orchestrator via `send_message`.
