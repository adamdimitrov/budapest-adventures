# DISPATCH — Worker M1 (Iteration 2: Preview Server Remediation)

## Target
Remediate security and routing defects identified by Reviewers, Challengers, and Auditor in `preview_server.py` and `tests/test_runner.py`.

## Write Ownership
- `preview_server.py`
- `tests/test_runner.py` (CLI `--feature` argument parsing fix)

## Mandatory Integrity Warning
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A forensic auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Defect Remediation Instructions
Review the gate reports:
- Reviewer 1: `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/teamwork_preview_reviewer_m1_1/handoff.md`
- Reviewer 2: `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/teamwork_preview_reviewer_m1_2/handoff.md`
- Challenger 1: `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/teamwork_preview_challenger_m1_1/handoff.md`
- Challenger 2: `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/teamwork_preview_challenger_m1_2/handoff.md`
- Auditor: `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/teamwork_preview_auditor_m1_1/handoff.md`

Implement the following fixes:
1. **Path Traversal & Boundary Protection (`preview_server.py`)**:
   - Resolve absolute target file path: `resolved_target = (root_dir / rel_path).resolve()`
   - Strictly check: `if not resolved_target.is_relative_to(root_dir.resolve()): return 404`
   - Empirically test `curl --path-as-is http://127.0.0.1:3000/../../../../etc/passwd` returns HTTP 404 (not 200).
2. **Dotfile Protection**:
   - Reject any request where any path segment starts with `.` (e.g. `/.git/`, `/.env`), returning HTTP 404.
3. **Double-Slash URL Normalization**:
   - Normalize URI path before routing: collapse multiple leading slashes (e.g. `re.sub(r'^/+', '/', path)`).
4. **Routing Priority Order (Redirects BEFORE TrailingSlash)**:
   - In `resolve_request`: evaluate `config.redirect_rules` BEFORE `trailingSlash` logic.
   - Ensures `/ru/` directly returns HTTP 301 to `/` without an intermediate HTTP 308 hop to `/ru`.
5. **Safe Regex Replacement**:
   - Ensure `re.sub` in redirect rule destination does not crash on backslashes or corrupt octal escapes.
6. **Query String Preservation**:
   - When appending preserved query string to redirect destination: if destination already has `?`, append with `&` instead of dropping or corrupting.
7. **Test Runner CLI Argument Support (`tests/test_runner.py`)**:
   - Update `--feature` to accept comma-separated string of IDs (e.g. `--feature 1,2,3,21,22,23`) as well as single integers.

## Verification
- Run `python3 preview_server.py --check`
- Run `python3 tests/test_runner.py --feature 1,2,3,21,22,23`
- Run `python3 tests/test_adversarial_m1.py` (created by Challenger 1) and confirm 100% of adversarial checks pass!
- Document verification commands and output in `handoff.md` and notify orchestrator via `send_message`.


## 2026-11-06T02:53:57Z
You are Worker M1 (Iteration 2: Preview Server Remediation).
Your working directory is: `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/teamwork_preview_worker_m1_2`
Project root: `/Users/adamdimitrov/Development/budapest-adventures`
Mandatory: Read `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/ORIGINAL_REQUEST.md` before starting work.
Also read `/Users/adamdimitrov/Development/budapest-adventures/PROJECT.md` and your assignment in `/Users/adamdimitrov/Development/budapest-adventures/.agents/teamwork/teamwork_preview_worker_m1_2/DISPATCH.md`.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A forensic auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Your write ownership is strictly:
- `preview_server.py`
- `tests/test_runner.py` (CLI `--feature` argument parsing fix)

Mission:
Remediate the 7 defects identified in the gate reports:
1. Path traversal vulnerability (`is_relative_to` bounds checking) in `preview_server.py`.
2. Dotfile suppression (block `/.git/`, etc. returning 404).
3. Leading multi-slash normalization (`//`).
4. Reorder routing evaluation: evaluate `config.redirect_rules` BEFORE `trailingSlash` to prevent 2-hop 308->301 redirect chains.
5. Safe regex substitution (avoid crash on unescaped backslashes / octal escapes).
6. Query string preservation when redirect destination already has query parameters.
7. Support comma-separated feature lists in `tests/test_runner.py --feature`.

Run verification tests:
- `python3 preview_server.py --check`
- `python3 tests/test_runner.py --feature 1,2,3,21,22,23`
- `python3 tests/test_adversarial_m1.py`
Document commands and outputs in `handoff.md` and notify orchestrator via `send_message`.
