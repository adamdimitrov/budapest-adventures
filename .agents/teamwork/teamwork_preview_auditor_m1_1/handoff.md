# Forensic Audit & Adversarial Challenge Report — Milestone 1

**Audit Target**: Milestone 1 Deliverables (`staging/static-overhaul` git branch, `preview_server.py`, `vercel.json`, and live DNS isolation)  
**Profile**: General Project (Development Mode per `ORIGINAL_REQUEST.md`)  
**Verdict**: **CLEAN** (Integrity Check) | **HIGH RISK / REMEDIATION REQUIRED** (Adversarial Security Challenge)

---

## 1. Observation

### Observation 1: Git Branch State & Live DNS Isolation
- Command: `git status && git branch -a`
  - Active branch: `* staging/static-overhaul`
  - Base commit: `4f592fb feat(media): integrate user-provided Legenda candlelit dinner salon photo` matching `remotes/origin/main`.
- Command: `dig +short budapestadventures.com`
  - Output: `35.187.176.9`
  - Grep search for `35.187.176.9` across codebase: zero configuration of live IP as deploy target in `vercel.json`, `package.json`, or scripts. Live production DNS and server remain 100% untouched.

### Observation 2: `vercel.json` Schema & Route Structure
- Inspection of `/Users/adamdimitrov/Development/budapest-adventures/vercel.json`:
  - Total lines: 847.
  - JSON parse test: Valid JSON. Top-level keys: `['$schema', 'version', 'cleanUrls', 'trailingSlash', 'headers', 'redirects', 'rewrites']`.
  - Deprecated properties check: `"routes"` and `"builds"` are 100% absent, eliminating Vercel build conflicts.
  - Rewrites: 10 rules mapping core money hubs (`/`, `/budapest-river-cruises`, `/budapest-dinner-cruises`, `/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest`, `/legenda-city-cruises`, `/danube-cruise-decision-hub`, `/api/cron`).
  - Redirects: 129 rules (1-to-1 localized river and dinner cruise slugs, German legacy URLs, and 25 pruned language catch-alls).

### Observation 3: `preview_server.py` Authenticity & Route Resolution
- Inspection of `/Users/adamdimitrov/Development/budapest-adventures/preview_server.py`:
  - 571 lines of standard-library Python 3 (`http.server`, `urllib.parse`, `json`, `pathlib`, `re`, `socketserver`, `argparse`).
  - Zero third-party dependencies (`flask`, `fastapi`, `requests` absent).
  - Genuine regex compilation engine: `pattern_to_regex()` dynamically converts path patterns like `/:name(regex)` and `/:lang/:path*`.
  - Hardcoded test cheating search: grep search for `test` revealed zero canned responses or test-harness bypass logic in `resolve_request()` or `handle_request()`.
  - Novel route verification: Tested 12 arbitrary unseen routes (e.g. `/cs/non-existent-tour`, `/bg/random-slug-12345`, `/ro/some/deep/subpath`, `/fr/some-page`, `/unknown-path-xyz.html`, `/unknown-path-xyz/`). All 12/12 evaluated dynamically according to specification.

### Observation 4: Test Suite & Diagnostics Execution
- Command: `python3 preview_server.py --check`
  - Output: `DIAGNOSTIC SUMMARY: 40/40 CHECKS PASSED`, exit code 0.
- Command: `python3 tests/test_runner.py --verbose --feature <N>`
  - Feature 1 (Staging Git Branch): 10/10 PASS (100%)
  - Feature 2 (Python Preview Server): 10/10 PASS (100%)
  - Feature 3 (Vercel Modern Config): 10/10 PASS (100%)
  - Feature 21 (Linguana Zombie Pruning): 10/10 PASS (100%)
  - Feature 22 (1-to-1 Localized Slugs 301): 10/10 PASS (100%)
  - Feature 23 (Catch-All Lang Redirects): 10/10 PASS (100%)
  - Total: 60/60 tests PASSED across Tiers 1 and 2.
- Live HTTP server execution (`tests/test_runner.py --feature 2 --server-url http://127.0.0.1:3046`): 10/10 PASS (100%).
- Pre-populated test artifacts check: `find . -name '*.log' -o -name '*result*' -o -name '*output*'` revealed only historical logs (`sync_ratings.log` from Jul 19 2026). No falsified test outputs.

### Observation 5: Adversarial Vulnerabilities Discovered
1. **Critical Path Traversal in `preview_server.py`**:
   - Lines 220-238 in `preview_server.py`:
     ```python
     # 5. Static File Resolution
     resolved_file: Optional[Path] = None
     target_rel = rewritten_path.lstrip("/")

     if not target_rel:
         candidate = root_dir / "index.html"
         if candidate.is_file():
             resolved_file = candidate
     else:
         candidate = root_dir / target_rel
         if candidate.is_file():
             resolved_file = candidate
     ```
   - Empirical proof:
     Executing HTTP GET against live `preview_server.py`:
     ```python
     conn.request('GET', '/../../../../../../etc/passwd')
     resp = conn.getresponse()
     ```
     Result: HTTP 200 OK. Body snippet: `b'##\n# User Database\n# ...'`.
     The server leaked the contents of `/etc/passwd` because `target_rel = rewritten_path.lstrip("/")` (`../../../../../../etc/passwd`) joined with `root_dir` resolves outside `root_dir` and `candidate.is_file()` returns True.
2. **Percent-Encoded Non-ASCII URL Matching Gap**:
   - `vercel.json` defines Cyrillic / Arabic / Chinese rules using raw UTF-8 strings (e.g. `"/bg/най-добрите:slug(.*)"`).
   - A real-world browser request sends percent-encoded octets (`/bg/%D0%BD%D0%B0%D0%B9-%D0%B4%D0%BE%D0%B1%D1%80%D0%B8%D1%82%D0%B5`).
   - `urllib.parse.urlsplit(url).path` retains the percent-encoding.
   - Result: The specific 1-to-1 rule fails to match, and the request falls through to the generic catch-all redirect `/:lang/:path* -> /:path*` instead of redirecting directly to `/budapest-river-cruises`.

---

## 2. Logic Chain

1. **Staging Isolation & Production Safety**:
   - Observation 1 confirmed the repo is on `staging/static-overhaul` branched from `main`.
   - `dig +short budapestadventures.com` returned `35.187.176.9`, confirming live production DNS is untouched.
   - No DNS, registrar, or deploy target configurations touch production.
2. **Integrity Verification (Development Mode)**:
   - Per `ORIGINAL_REQUEST.md`, integrity mode is `development`.
   - Prohibited patterns under Development mode: hardcoded test results, facade implementations, and fabricated verification outputs.
   - Observation 3 proved `preview_server.py` contains genuine parsing, compiling, and routing algorithms with zero hardcoded test response shortcuts. It correctly evaluated 12 arbitrary unseen routes.
   - Observation 4 confirmed zero fabricated test logs or cheat files.
   - Therefore, no integrity violations occurred. Verdict is **CLEAN**.
3. **Adversarial Security Assessment**:
   - Observation 5 demonstrated an empirical path traversal vulnerability in `preview_server.py` allowing unauthenticated local file extraction via `../` traversal.
   - Observation 5 also demonstrated that percent-encoded non-ASCII URLs bypass 1-to-1 redirect rules.
   - While these are engineering defects rather than deliberate integrity cheats, they represent significant functional and security risks that must be addressed before production/staging usage.

---

## 3. Caveats

1. **Scope of Audit**:
   - Audited Milestone 1 deliverables: `staging/static-overhaul` git branch, `preview_server.py`, `vercel.json`, and live DNS safety.
   - Did not audit Milestone 2 static HTML assets (`candlelit-dinner-cruise.html`), which are scheduled for M2.
2. **Test Runner Command Syntax in Worker Handoff**:
   - Worker handoff documented: `python3 tests/test_runner.py --verbose --feature 1,2,3,21,22,23`.
   - `test_runner.py`'s `argparse` defines `--feature` as `type=int`, which rejects commas. However, executing each feature individually (`--feature 1`, etc.) yielded 100% PASS (60/60 tests).
3. **Audit-Only Constraint**:
   - In accordance with auditor directives ("Audit-only — do NOT modify implementation code"), the auditor did NOT alter `preview_server.py` or `vercel.json`. Mitigations are provided below for the worker/orchestrator to apply.

---

## 4. Conclusion & Forensic Verdict

### Forensic Verdict: **CLEAN**
- **Git Branching**: Genuine `staging/static-overhaul` branch exists, is active, and isolates work from `main`.
- **Live DNS**: Untouched (35.187.176.9).
- **`vercel.json`**: Genuine modern schema conforming to Vercel standards; legacy conflicting `routes` and `builds` are removed; rewrites and redirects are authentic.
- **`preview_server.py`**: Genuine zero-dependency implementation; zero hardcoded test cheats; zero facade stubs.

### Adversarial Challenge Finding: **HIGH RISK**
- **Vulnerability**: Path traversal in `preview_server.py` (lines 220-238) permits reading arbitrary files outside project root (e.g. `/etc/passwd`).
- **Recommended Action for Milestone 2 / Worker**:
  Add path containment validation in `preview_server.py` before serving files:
  ```python
  # Guard against path traversal
  try:
      resolved_target = candidate.resolve()
      if not resolved_target.is_relative_to(root_dir.resolve()):
          # Reject path traversal attempt
          resolved_file = None
      elif resolved_target.is_file():
          resolved_file = resolved_target
  except (ValueError, RuntimeError):
      resolved_file = None
  ```
  And decode percent-encoded paths before rule matching:
  ```python
  decoded_path = urllib.parse.unquote(raw_path)
  # match against decoded_path for unicode slug rules
  ```

---

## 5. Verification Method

To independently verify the auditor's findings:

1. **Verify Git Branch & DNS Isolation**:
   ```bash
   git branch
   dig +short budapestadventures.com
   ```
   *Expected*: `* staging/static-overhaul` and `35.187.176.9`.

2. **Verify preview_server.py Diagnostics**:
   ```bash
   python3 preview_server.py --check
   ```
   *Expected*: `40/40 CHECKS PASSED`.

3. **Verify E2E Tests for M1 Features**:
   ```bash
   python3 tests/test_runner.py --verbose --feature 1
   python3 tests/test_runner.py --verbose --feature 2
   python3 tests/test_runner.py --verbose --feature 3
   ```
   *Expected*: 30/30 tests PASS (100%).

4. **Reproduce Path Traversal Finding**:
   ```bash
   python3 -c "
   import http.client, http.server, threading, time
   from preview_server import PreviewRequestHandler, VercelConfig
   from pathlib import Path
   root = Path('.').resolve()
   PreviewRequestHandler.server_root = root
   PreviewRequestHandler.vercel_config = VercelConfig(root / 'vercel.json')
   server = http.server.HTTPServer(('127.0.0.1', 3998), PreviewRequestHandler)
   threading.Thread(target=server.serve_forever, daemon=True).start()
   time.sleep(0.3)
   conn = http.client.HTTPConnection('127.0.0.1', 3998)
   conn.request('GET', '/../../../../../../etc/passwd')
   resp = conn.getresponse()
   print('Status:', resp.status, '| Leaked bytes:', len(resp.read()))
   server.shutdown()
   "
   ```
   *Expected*: Status: 200 (proves path traversal vulnerability).
