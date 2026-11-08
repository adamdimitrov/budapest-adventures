# DISPATCH — Challenger 2 (Milestone 2 Stress & Linking Verification)

## Mission
Stress-test linking, route resolution, and JSON-LD schema across the 5 core money hubs.

## Instructions
1. Read `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/ORIGINAL_REQUEST.md`.
2. Read `/Users/adamdimitrov/Development/budapest-adventures/PROJECT.md`.
3. Read Worker M2 handoff at `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/teamwork_preview_worker_m2_1/handoff.md`.
4. Empirical stress testing:
   - Check internal cross-links between the 5 hubs (e.g. from decision hub to dinner cruise review, from river hub to legenda terminal).
   - Test JSON-LD schema syntax across all 5 hubs using `python3 -c "import json..."` to ensure no malformed JSON.
   - Verify that all image assets referenced in the 5 hubs actually exist on disk in the repo.
   - Verify tests with `python3 tests/test_runner.py --tier 1`.
5. Write `handoff.md` with explicit verdict `APPROVE` or `REQUEST_CHANGES` and notify orchestrator via `send_message`.
