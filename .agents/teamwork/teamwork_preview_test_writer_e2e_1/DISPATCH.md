# DISPATCH — E2E Testing Track Test Writer

## Target
Design test infrastructure and write the comprehensive opaque-box E2E test suite across Tiers 1-4 for Budapest Adventures Staging Architecture.

## Instructions
1. Read `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/ORIGINAL_REQUEST.md` (authoritative source).
2. Read `/Users/adamdimitrov/Development/budapest-adventures/PROJECT.md` (feature inventory, architecture, interface contracts).
3. Create `TEST_INFRA.md` at `/Users/adamdimitrov/Development/budapest-adventures/TEST_INFRA.md` following the project test specification:
   - Methodology: Category-Partition + BVA + Pairwise + Workload Testing.
   - Opaque-box, requirement-driven.
   - Coverage goals across all 26 inventoried features.
4. Implement a clean, zero-dependency Python 3 test runner in `/Users/adamdimitrov/Development/budapest-adventures/tests/test_runner.py` and test modules under `/Users/adamdimitrov/Development/budapest-adventures/tests/`:
   - **Tier 1 - Feature Coverage**: >=5 tests per feature for isolation/happy-path.
   - **Tier 2 - Boundary & Corner**: >=5 tests per feature (empty query strings, malicious params, missing UTMs, weird character encodings, edge case URLs, legacy `#` handling).
   - **Tier 3 - Cross-Feature Combinations**: Pairwise testing (e.g. mobile user + UTMs + Legenda click + currency conversion; zombie language request + redirect + UTM preservation).
   - **Tier 4 - Real-World Scenarios**: Realistic user workflows (User arrives from Google Ad with gclid -> lands on river hub -> compares cruises in decision hub -> clicks Legenda checkout -> verifies partner 38585 and click_id preserved and Meta Pixel fired).
5. Ensure the test suite can execute against local files or against `preview_server.py` HTTP endpoints.
6. Verify test execution by running `python3 tests/test_runner.py` and document results.
7. Once test suite is complete and functional, publish `TEST_READY.md` at `/Users/adamdimitrov/Development/budapest-adventures/TEST_READY.md`.
8. Write `handoff.md` in your working directory and notify the Project Orchestrator via `send_message`.


## 2026-11-06T02:33:06Z
You are the E2E Test Writer for Budapest Adventures Staging Architecture Overhaul.
Your working directory is: `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/teamwork_preview_test_writer_e2e_1`
Project root: `/Users/adamdimitrov/Development/budapest-adventures`
Mandatory: Read `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/ORIGINAL_REQUEST.md` before starting work.
Also read `/Users/adamdimitrov/Development/budapest-adventures/PROJECT.md` and your assignment in `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/teamwork_preview_test_writer_e2e_1/DISPATCH.md`.

Your mission:
1. Create `TEST_INFRA.md` at project root (`/Users/adamdimitrov/Development/budapest-adventures/TEST_INFRA.md`) detailing the 4-tier test architecture, opaque-box methodology, and feature inventory mapping.
2. Build an opaque-box, zero-dependency Python 3 test harness in `tests/test_runner.py` and test modules under `tests/` covering:
   - Tier 1: Feature Coverage (>=5 test cases per feature)
   - Tier 2: Boundary & Corner Cases (>=5 test cases per feature)
   - Tier 3: Cross-Feature Interactions & Combinations (pairwise coverage)
   - Tier 4: Real-World Scenarios (realistic end-to-end user journeys)
3. Ensure the test runner can test static files, route mappings, HTML IDs, canonical tags, sitemaps, UTM/gclid link decoration, and Meta Pixel triggers.
4. Execute `python3 tests/test_runner.py` to verify the runner executes properly.
5. Create `TEST_READY.md` at `/Users/adamdimitrov/Development/budapest-adventures/TEST_READY.md` summarizing the test suite.
6. Write `handoff.md` in your working directory and notify the orchestrator via `send_message`.
