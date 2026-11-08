# Forensic Audit Report — Milestone 1 Iteration 2

**Work Product**: `preview_server.py` and `tests/test_runner.py` (M1 Iteration 2 Remediations)  
**Profile**: General Project  
**Integrity Mode**: Development (per `ORIGINAL_REQUEST.md`)  
**Auditor**: `teamwork_preview_auditor_m1_iter2_1`  
**Date**: 2026-11-06T03:08:00Z  
**Verdict**: **CLEAN**

---

## 1. Observation

### 1.1 Source Code Inspection & Prohibited Patterns Check

1. **Absence of Hardcoded Cheats and Bypasses**:
   - Inspected `preview_server.py` (620 lines).
   - `substitute_destination` (`preview_server.py:69-86`): Uses generic literal substitution (`str.replace`) iterating over `match.groupdict().items()` and `match.groups()`. No special-casing for specific URLs or test payloads like `test\x` or `test\123`.
   - `resolve_request` (`preview_server.py:160-264`): Fully dynamic evaluation pipeline. Multi-slash collapse uses `re.sub(r"^/+", "/", url)` (`line 163`). Redirect checks iterate through `config.redirect_rules` (`line 169`). Static file resolution validates path boundaries using `candidate.is_relative_to(root_resolved)` and filters dot segments generically via `any(seg.startswith(".") for seg in path_segments)` (`lines 228-252`).
   - Zero hardcoded PASS/FAIL flags, mock bypasses, or test result tables detected in project source.

2. **Authenticity of Bounds Checking**:
   - Location: `preview_server.py:226-252`
   - Code snippet:
     ```python
     root_resolved = root_dir.resolve()
     unquoted_rewritten = urllib.parse.unquote(rewritten_path)
     path_segments = [p for p in unquoted_rewritten.split("/") if p]
     if any(seg.startswith(".") for seg in path_segments):
         resolved_file = None
     elif not target_rel:
         candidate = (root_dir / "index.html").resolve()
         if candidate.is_file() and candidate.is_relative_to(root_resolved):
             resolved_file = candidate
     else:
         candidate = (root_dir / target_rel).resolve()
         if candidate.is_relative_to(root_resolved):
             rel_parts = candidate.relative_to(root_resolved).parts
             if any(part.startswith(".") for part in rel_parts):
                 resolved_file = None
             elif candidate.is_file():
                 resolved_file = candidate
     ```
   - Analysis: Candidate files are fully resolved (`.resolve()`) and checked against `root_dir.resolve()` via `is_relative_to`. Symlinks escaping the repository root resolve to paths outside `root_resolved`, failing `candidate.is_relative_to(root_resolved)`. Unquoted path segments and relative components starting with `.` are strictly rejected.

3. **Absence of Fabricated Artifacts**:
   - Pre-populated artifact check command: `find . -name '*.log' -o -name '*result*' -o -name '*output*'`
   - Results: Only legacy rating logs from July 19 (`sync_ratings.log`, `sync_ratings_err.log`) predating this project exist. No pre-populated test runner output or verification cache exists.

4. **Test Runner Feature Argument Parsing**:
   - Location: `tests/test_runner.py:111-116, 158-168`
   - Accepts comma-separated strings (`args.feature.split(",")`), strips whitespace, and parses integer tokens into a set: `{int(f.strip()) for f in args.feature.split(",") if f.strip()}`.
   - Rejects non-integer values with exit code 2 and explicit usage guidance. Tests are filtered strictly by `feature_filter` without altering test execution semantics.

---

### 1.2 Empirical Runtime Verification

1. **Self-Diagnostics (`python3 preview_server.py --check`)**:
   - Command: `python3 preview_server.py --check`
   - Result:
     ```
     ======================================================================
     BUDAPEST ADVENTURES — PREVIEW SERVER SELF-DIAGNOSTICS
     Project Root: /Users/adamdimitrov/Development/budapest-adventures
     Config File:  /Users/adamdimitrov/Development/budapest-adventures/vercel.json
     ======================================================================
     DIAGNOSTIC SUMMARY: 48/48 CHECKS PASSED
     RESULT: ALL DIAGNOSTIC TESTS PASSED SUCCESSFULLY! (EXIT 0)
     ======================================================================
     ```

2. **E2E Test Runner Composite Command (`python3 tests/test_runner.py --verbose --feature 1,2,3,21,22,23`)**:
   - Command: `python3 tests/test_runner.py --verbose --feature 1,2,3,21,22,23`
   - Verbatim Output:
     ```
     ==============================================================================
      BUDAPEST ADVENTURES — STAGING ARCHITECTURE E2E TEST RUNNER
      Timestamp: 2026-11-06T03:04:51.784869+00:00
      Project Root: /Users/adamdimitrov/Development/budapest-adventures
      Execution Mode: Static Filesystem Inspection
      Selected Tiers: [1, 2, 3, 4] | Feature Filter: 1,2,3,21,22,23
      Total Tests Discovered: 60
     ==============================================================================
      Total Tests:  60
      Passed:       60 (100.0%)
      Failed:       0
      Duration:     0.04 seconds
     ==============================================================================
     ```

3. **Adversarial Security Test Suite (`python3 tests/test_adversarial_m1.py`)**:
   - Executed against live socket server on port 3888.
   - Verbatim Output:
     ```
     TOTAL ADVERSARIAL CHECKS: 19
     PASSED: 19
     FAILED: 0 (Critical: 0, High: 0)
     ```

4. **Direct Independent Forensic Probes (Raw Curl & Socket Probing)**:
   - Path Traversal probe:
     `curl -s -i --path-as-is http://127.0.0.1:3888/../../../../etc/passwd`
     Returned `HTTP/1.0 404 Not Found` (zero bytes of system files disclosed).
   - Encoded Traversal probe:
     `curl -s -i --path-as-is http://127.0.0.1:3888/%2e%2e/%2e%2e/etc/passwd`
     Returned `HTTP/1.0 404 Not Found`.
   - Dotfile probe:
     `curl -s -i --path-as-is http://127.0.0.1:3888/.git/config`
     Returned `HTTP/1.0 404 Not Found`.
     `curl -s -i --path-as-is http://127.0.0.1:3888/.env`
     Returned `HTTP/1.0 404 Not Found`.
   - Multi-slash probe:
     `curl -s -i --path-as-is http://127.0.0.1:3888//legenda-city-cruises`
     Returned `HTTP/1.0 200 OK` (served authentic Legenda Terminal HTML with title `Legenda City Cruises Budapest — Official Live Timetable & Direct Booking`).
   - Trailing Slash Pruned Language probe:
     `curl -s -i http://127.0.0.1:3888/ru/`
     Returned `HTTP/1.0 301 Moved Permanently` with `Location: /` (direct 1-hop redirect).
   - Query String Preservation probe:
     `curl -s -i "http://127.0.0.1:3888/ru/?utm_source=test"`
     Returned `HTTP/1.0 301 Moved Permanently` with `Location: /?utm_source=test`.

5. **Live Production DNS Isolation Check**:
   - `git branch --show-current`: `staging/static-overhaul`.
   - `dig +short budapestadventures.com`: `35.187.176.9`.
   - Grep for `35.187.176.9` in repository: Only occurs in documentation and defensive test assertions verifying that the IP is not configured as a deploy target.
   - No `CNAME` file pointing apex domain exists in repository.
   - Live production DNS is 100% untouched.

---

## 2. Logic Chain

1. **Authenticity of Bounds Check**:
   - Observations 1.1.2 and 1.2.4 confirm that `preview_server.py` enforces canonical path containment via `candidate.resolve().is_relative_to(root_dir.resolve())` and unquoted segment validation.
   - Any path escaping root (`/../../../../etc/passwd`, `/%2e%2e/`, dotfiles) evaluates to `resolved_file = None` and yields HTTP 404.
   - Independent verification confirms that arbitrary file disclosure is completely remediated.

2. **Evaluation Order & Clean Redirects**:
   - Observation 1.1.1 and 1.2.4 demonstrate that `config.redirect_rules` precedes `trailingSlash` and `cleanUrls`.
   - This ensures requests like `/ru/` are matched immediately by the configured redirect rules, returning a clean 301 redirect in 1 hop without intermediate 308 hops.

3. **URL Normalization and Escaping**:
   - Observation 1.1.1 demonstrates that `re.sub(r"^/+", "/", url)` eliminates `netloc` ambiguity in `urlsplit`.
   - Literal replacement in `substitute_destination` eliminates backslash regex syntax crashes (`\x`) and octal interpretation (`\123`).

4. **Absence of Integrity Cheats**:
   - Observations 1.1.1, 1.1.3, and 1.2.2 confirm that `test_runner.py` and `preview_server.py` implement genuine computational logic without hardcoded test values, facade stubs, or pre-populated artifacts.
   - The test runner executes all 60 tests dynamically in memory.

5. **Staging Isolation Adherence**:
   - Observation 1.2.5 confirms that live production DNS (`35.187.176.9`) is untouched and active development remains isolated on `staging/static-overhaul`.

---

## 3. Caveats

- Milestone 2 target HTML file (`candlelit-dinner-cruise.html`) is planned for M2 and not yet created; self-diagnostics correctly classify it as `PENDING M2 PIPELINE` while verifying rewrite logic.
- No other caveats.

---

## 4. Conclusion

The Milestone 1 Iteration 2 work product satisfies all integrity and functional requirements:
- Remediations in `preview_server.py` and `tests/test_runner.py` are authentic and free of hardcoded cheats, facades, or test-bypass logic.
- Path traversal and dotfile protections (`is_relative_to`) are genuinely implemented and empirically verified.
- Staging isolation is strictly preserved; live production DNS (`35.187.176.9`) is 100% untouched.

**Final Forensic Verdict**: **`CLEAN`**

---

## 5. Verification Method

To reproduce this verification:

1. **Run Self-Diagnostics**:
   ```bash
   python3 preview_server.py --check
   ```
   *Expected*: `DIAGNOSTIC SUMMARY: 48/48 CHECKS PASSED`, Exit 0.

2. **Run E2E Test Runner for M1 Features**:
   ```bash
   python3 tests/test_runner.py --verbose --feature 1,2,3,21,22,23
   ```
   *Expected*: `Total Tests: 60, Passed: 60 (100.0%), Failed: 0`, Exit 0.

3. **Run Adversarial Suite Against Preview Server**:
   ```bash
   python3 preview_server.py --port 3888 &
   python3 tests/test_adversarial_m1.py
   ```
   *Expected*: `TOTAL ADVERSARIAL CHECKS: 19, PASSED: 19, FAILED: 0`, Exit 0.

4. **Verify Live Production DNS**:
   ```bash
   dig +short budapestadventures.com
   ```
   *Expected*: `35.187.176.9`.
