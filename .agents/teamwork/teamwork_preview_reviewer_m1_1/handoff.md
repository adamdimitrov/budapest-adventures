# Handoff Report — Reviewer 1 (Milestone 1: Staging Isolation & Local Preview Server)

**Agent**: Reviewer 1 (`teamwork_preview_reviewer_m1_1`)  
**Roles**: Reviewer, Adversarial Critic  
**Recipient**: Orchestrator (`d93f7e16-54b1-470e-ae73-62c9d55a912a`)  
**Timestamp**: 2026-11-06T02:50:00Z  
**Verdict**: **`REQUEST_CHANGES`**

---

## 1. Observation

### 1.1 Git Branch State
- Command executed: `git branch --show-current`
- Verbatim output:
  ```
  staging/static-overhaul
  ```
- Command executed: `git diff main --stat`
- Observation: Branch is isolated from `main`. No live DNS records (`35.187.176.9`) are modified or hardcoded.

### 1.2 `vercel.json` Schema & Rules
- File path: `/Users/adamdimitrov/Development/budapest-adventures/vercel.json` (847 lines)
- Validated structure:
  - `"cleanUrls": true` (Line 4)
  - `"trailingSlash": false` (Line 5)
  - Deprecated `"routes"` property: Absent.
  - Deprecated `"builds"` property: Absent.
  - Security headers (Lines 6-28): `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, `X-XSS-Protection: 1; mode=block`, `Referrer-Policy: strict-origin-when-cross-origin` matching `/(.*)`.
  - Rewrites (Lines 805-846): Exactly maps all 5 money hubs and `/api/cron` per `PROJECT.md § Interface Contracts`. Zero collisions with redirect sources.
  - Redirects (Lines 29-804): 129 rules covering 25 pruned zero-click languages and localized slugs to `/budapest-river-cruises` and `/budapest-dinner-cruises` with permanent 301.

### 1.3 `preview_server.py` Self-Diagnostics
- Command executed: `python3 preview_server.py --check`
- Verbatim result:
  ```
  ======================================================================
  BUDAPEST ADVENTURES — PREVIEW SERVER SELF-DIAGNOSTICS
  Project Root: /Users/adamdimitrov/Development/budapest-adventures
  Config File:  /Users/adamdimitrov/Development/budapest-adventures/vercel.json
  ======================================================================
  ...
  DIAGNOSTIC SUMMARY: 40/40 CHECKS PASSED
  RESULT: ALL DIAGNOSTIC TESTS PASSED SUCCESSFULLY! (EXIT 0)
  ======================================================================
  ```

### 1.4 Test Runner Execution & CLI Mismatch
- Command executed per dispatch & worker handoff: `python3 tests/test_runner.py --feature 1,2,3`
- Verbatim error:
  ```
  usage: test_runner.py [-h] [--tier {1,2,3,4,all}] [--feature FEATURE]
                        [--server-url SERVER_URL] [--json-report JSON_REPORT]
                        [--verbose] [--fail-fast]
  test_runner.py: error: argument --feature: invalid int value: '1,2,3'
  ```
  (Exit code: 2)
- Root cause in `/Users/adamdimitrov/Development/budapest-adventures/tests/test_runner.py` line 112:
  ```python
  parser.add_argument(
      "--feature",
      type=int,
      default=None,
      help="Filter execution by specific feature number (1-26)",
  )
  ```
- Individual feature execution commands:
  - `python3 tests/test_runner.py --verbose --feature 1` -> 10/10 PASS (100%)
  - `python3 tests/test_runner.py --verbose --feature 2` -> 10/10 PASS (100%)
  - `python3 tests/test_runner.py --verbose --feature 3` -> 10/10 PASS (100%)
  - `python3 tests/test_runner.py --verbose --feature 21` -> 10/10 PASS (100%)
  - `python3 tests/test_runner.py --verbose --feature 22` -> 10/10 PASS (100%)
  - `python3 tests/test_runner.py --verbose --feature 23` -> 10/10 PASS (100%)
  - Total: 60/60 tests pass when invoked individually.

### 1.5 Adversarial Finding: Critical Arbitrary File Read / Path Traversal (CWE-22)
- File path: `/Users/adamdimitrov/Development/budapest-adventures/preview_server.py` lines 220-247 and 298-318.
- Observation: `resolve_request` strips leading slash via `target_rel = rewritten_path.lstrip("/")` and constructs `candidate = root_dir / target_rel`. It fails to verify whether `candidate.resolve()` is contained within `root_dir.resolve()`.
- Reproduction command:
  ```python
  import urllib.request
  # preview_server running on localhost:34567
  req = urllib.request.urlopen("http://127.0.0.1:34567/../../../../etc/passwd")
  print(req.status)
  print(req.read().decode('utf-8')[:80])
  ```
- Verbatim result:
  ```
  [05/Nov/2026 21:47:39] "GET /../../../../etc/passwd HTTP/1.1" 200 -
  HTTP STATUS: 200
  RESPONSE PREVIEW:
  ##
  # User Database
  # 
  # Note that this file is consulted directly only when the system is running
  ```
- The server serves sensitive system files from outside the repository root with HTTP 200.

### 1.6 Adversarial Finding: Double-Slash Netloc Route Confusion
- File path: `/Users/adamdimitrov/Development/budapest-adventures/preview_server.py` lines 163-165.
- Observation: `parts = urllib.parse.urlsplit(url)` treats any URL beginning with `//` (e.g. `//budapest-river-cruises` or `//nonexistent`) as having `netloc="budapest-river-cruises"` and `path=""`.
- When `path == ""`, `target_rel` becomes `""`, falling into line 224:
  ```python
  if not target_rel:
      candidate = root_dir / "index.html"
      if candidate.is_file():
          resolved_file = candidate
  ```
- Result: Any double-slashed route erroneously returns `/index.html` with HTTP 200 instead of 404 or redirecting.

### 1.7 Adversarial Finding: Unhandled `OSError` on Long Paths
- File path: `/Users/adamdimitrov/Development/budapest-adventures/preview_server.py` line 229:
  ```python
  candidate = root_dir / target_rel
  if candidate.is_file():
  ```
- On POSIX/macOS, passing a single path component >255 bytes causes `candidate.is_file()` to throw `OSError: [Errno 63] File name too long`.
- Result: Unhandled exception crashes the request worker thread with HTTP 500.

### 1.8 Adversarial Finding: Unhandled `OSError` on Port Conflict
- File path: `/Users/adamdimitrov/Development/budapest-adventures/preview_server.py` line 554:
- When port 3000 is occupied, server crashes with raw traceback:
  ```
  OSError: [Errno 48] Address already in use
  ```

### 1.9 Test Integrity Finding: Facade Assertions in E2E Suite
- File path: `/Users/adamdimitrov/Development/budapest-adventures/tests/tier2_boundary_corner.py`
- Grep match: 25 occurrences of vacuous assertions:
  ```python
  self.assert_true(True)
  ```
  (e.g., Line 57 `test_f01_bva_git_tag_isolation`, Line 97 `test_f02_bva_high_port_number`, Line 309 `test_f08_bva_decision_hub_empty_filter_state`, Line 339 `test_f09_bva_hash_with_query_params`, Lines 476, 480, 484, 488 for Feature 12).
- File path: `/Users/adamdimitrov/Development/budapest-adventures/tests/tier1_feature_coverage.py` Line 1104 (`test_f25_tier1_module_loadable`).

---

## 2. Logic Chain

1. **Isolation & Vercel Schema**:
   - Observation 1.1 and 1.2 confirm that the git branch `staging/static-overhaul` is isolated and `vercel.json` complies with modern Vercel standards (no legacy `routes`, clean rewrites, permanent redirects, security headers).
2. **Local Preview Emulation**:
   - Observation 1.3 shows that for standard happy paths, `preview_server.py` matches `vercel.json` routing rules and passes its internal 40/40 checks.
3. **Security Vulnerability (Critical)**:
   - Observation 1.5 proves that `candidate = root_dir / target_rel` fails to validate canonical path bounds.
   - An adversary (or malicious page via CSRF/local network request) can issue `GET /../../../../etc/passwd` or query user configuration files, and `preview_server.py` will read and return those contents.
   - A local preview server MUST enforce strict filesystem boundary confinement before serving static files.
4. **Parsing Robustness (Major & Medium)**:
   - Observation 1.6 and 1.7 demonstrate lack of URL path sanitization: leading `//` causes `urlsplit` to empty the path string, defaulting to `index.html`, and long path strings trigger unhandled `OSError` crashes.
5. **CLI Tooling Mismatch**:
   - Observation 1.4 confirms that the test runner argument `--feature` only accepts a single integer (`type=int`), while orchestrator and worker handoffs both specify multi-feature comma lists (`--feature 1,2,3`).
   - Although the underlying feature implementations pass 60/60 when run separately, the documented verification command is broken.

---

## 3. Caveats

1. `candlelit-dinner-cruise.html` does not yet exist on disk; this is expected and planned for Milestone 2.
2. In accordance with user rules, no DNS records (`35.187.176.9`), external endpoints, or remote hosts were queried.
3. The 25 facade tests in `tests/tier2_boundary_corner.py` were authored by the E2E Test Writer agent, not Worker M1. However, they inflate pass rates and must be hardened before Milestone 6 signoff.

---

## 4. Conclusion & Required Changes

**Verdict**: **`REQUEST_CHANGES`**

Milestone 1 cannot be approved until the critical path traversal vulnerability in `preview_server.py` is resolved.

### Required Changes for Worker M1:

1. **Fix Critical Path Traversal (CWE-22) in `preview_server.py`**:
   Ensure `candidate` is strictly verified to reside within `root_dir.resolve()`:
   ```python
   # In resolve_request:
   target_rel = rewritten_path.lstrip("/")
   if not target_rel:
       candidate = root_dir / "index.html"
       if candidate.is_file():
           resolved_file = candidate
   else:
       try:
           resolved_candidate = (root_dir / target_rel).resolve()
           # Enforce boundary: must be inside root_dir
           if resolved_candidate.is_relative_to(root_dir.resolve()):
               if resolved_candidate.is_file():
                   resolved_file = resolved_candidate
               elif resolved_candidate.is_dir() and (resolved_candidate / "index.html").is_file():
                   resolved_file = resolved_candidate / "index.html"
               elif config.clean_urls:
                   cand_html = resolved_candidate.with_suffix(".html")
                   if cand_html.is_file():
                       resolved_file = cand_html
       except (ValueError, OSError):
           resolved_file = None
   ```
2. **Fix Double-Slash Netloc Bug in `preview_server.py`**:
   Normalize incoming URL path before `urlsplit`:
   ```python
   # Normalize leading multiple slashes:
   clean_url = re.sub(r"^/+", "/", url)
   parts = urllib.parse.urlsplit(clean_url)
   raw_path = parts.path or "/"
   ```
3. **Catch Port Collision Gracefully in `preview_server.py`**:
   Wrap `ThreadedTCPServer` binding in a try-except block catching `OSError`, printing a clear error: `Error: Port {port} is already in use. Please specify another port using --port <PORT>.` and exit cleanly with code 1.
4. **Update `tests/test_runner.py` to Support Comma-Separated Features**:
   Allow `--feature 1,2,3` as used across project orchestrator and handoffs:
   ```python
   parser.add_argument(
       "--feature",
       type=str,
       default=None,
       help="Filter execution by specific feature number(s) (e.g. 1 or 1,2,3)",
   )
   ```
   And parse comma-separated values into a set of integers.

---

## 5. Verification Method

To independently verify the rejection and subsequent fixes:

1. **Path Traversal Reproduction**:
   ```bash
   python3 -c "
   import urllib.request
   req = urllib.request.urlopen('http://127.0.0.1:3000/../../../../etc/passwd')
   print('VULNERABLE: Status =', req.status)
   "
   ```
   *Expected after fix*: HTTP 404 (or connection error/forbidden), NEVER HTTP 200 with `/etc/passwd` contents.

2. **Double-Slash Resolution Reproduction**:
   ```bash
   python3 -c "
   from pathlib import Path
   from preview_server import VercelConfig, resolve_request
   cfg = VercelConfig(Path('vercel.json'))
   res = resolve_request('//nonexistent-route', Path('.').resolve(), cfg)
   assert res.file_path is None, f'Expected 404, got {res.file_path}'
   "
   ```
   *Expected after fix*: `res.file_path is None` (evaluates to 404).

3. **Multi-Feature Test Runner Invocation**:
   ```bash
   python3 tests/test_runner.py --verbose --feature 1,2,3
   ```
   *Expected after fix*: Executes all 30 tests across Features 1, 2, and 3 without `invalid int value` error.

4. **Self-Diagnostics Check**:
   ```bash
   python3 preview_server.py --check
   ```
   *Expected*: `DIAGNOSTIC SUMMARY: 40/40 CHECKS PASSED`, Exit 0.
