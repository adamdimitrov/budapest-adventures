# DISPATCH — Worker M1 (Staging Isolation & Local Preview Server)

## Target
Execute Milestone 1: Create dedicated git branch `staging/static-overhaul`, refactor `vercel.json` to modern format, and implement zero-dependency Python `preview_server.py`.

## Write Ownership
You exclusively own:
- `vercel.json`
- `preview_server.py`
- Git branch operations (`staging/static-overhaul`)
You MUST NOT edit other HTML or JS files in this milestone.

## Mandatory Integrity Warning
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A forensic auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Instructions
1. Read `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/ORIGINAL_REQUEST.md` (authoritative request).
2. Read `/Users/adamdimitrov/Development/budapest-adventures/PROJECT.md`.
3. Read Survey Explorer 1 report at `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/teamwork_preview_explorer_survey_1/survey_codebase.md`.
4. Git Branch Setup:
   - Ensure you are on dedicated branch `staging/static-overhaul`. Create it if it doesn't exist (`git checkout -b staging/static-overhaul`).
   - Do NOT affect live production DNS (`35.187.176.9` / Linguana / Webflow).
5. Refactor `vercel.json`:
   - Replace legacy `"routes": [...]` block with modern Vercel schema:
     - `"cleanUrls": true`
     - `"trailingSlash": false`
     - Modern `"redirects": [...]`
     - Modern `"rewrites": [...]`
     - Modern `"headers": [...]`
   - Configure initial core rewrites per `PROJECT.md § Interface Contracts`:
     - `/` -> `/index.html`
     - `/budapest-river-cruises` -> `/index.html`
     - `/budapest-dinner-cruises` -> `/dinner.html`
     - `/best-dinner-cruises-budapest` -> `/dinner.html`
     - `/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest` -> `/candlelit-dinner-cruise.html`
     - `/legenda-city-cruises` -> `/legenda-city-cruises.html`
     - `/danube-cruise-decision-hub` -> `/danube_cruise_decision_hub.html`
6. Create `preview_server.py`:
   - Zero external Python dependencies (uses standard library `http.server`, `urllib.parse`, `json`, `pathlib`).
   - Parses `vercel.json` to handle redirects (301/308) and rewrites natively.
   - Serves static files with correct MIME types and security headers.
   - Includes a `--test` or `--check` self-diagnostic mode that verifies route resolution programmatically.
7. Verify build and execution:
   - Run python diagnostic tests to confirm server starts, route resolution works, and `vercel.json` parses cleanly.
8. Document exact verification commands and outputs in your report.
9. Write `handoff.md` in your working directory and notify the Project Orchestrator via `send_message`.


## 2026-11-06T02:33:06Z
Received from orchestrator (d93f7e16-54b1-470e-ae73-62c9d55a912a):
You are Worker M1 for Budapest Adventures Staging Architecture Overhaul.
Your working directory is: `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/teamwork_preview_worker_m1_1`
Project root: `/Users/adamdimitrov/Development/budapest-adventures`
Mandatory: Read `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/ORIGINAL_REQUEST.md` before starting work.
Also read `/Users/adamdimitrov/Development/budapest-adventures/PROJECT.md` and your assignment in `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/teamwork_preview_worker_m1_1/DISPATCH.md`.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A forensic auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Your write ownership is strictly:
- `vercel.json`
- `preview_server.py`
- Git branch operations (`staging/static-overhaul`)

Your mission:
1. Switch to/create dedicated git branch `staging/static-overhaul`.
2. Refactor `vercel.json` into modern Vercel schema (cleanUrls, trailingSlash: false, redirects, rewrites, headers) per `PROJECT.md`.
3. Create zero-dependency Python 3 `preview_server.py` supporting `vercel.json` rewrites and redirects with self-diagnostic mode.
4. Test and verify server and routes using Python commands.
5. Document verification commands and output in `handoff.md` and notify orchestrator via `send_message`.
