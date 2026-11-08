# Adversarial Audit Handoff Report — Challenger 1 (Milestone 1)

**Verdict**: `REQUEST_CHANGES`

---

## 1. Observation

### Observation 1: Critical Arbitrary File Read via Path Traversal
- **File**: `preview_server.py`, lines 220–238:
  ```python
  222:     target_rel = rewritten_path.lstrip("/")
  ...
  229:     candidate = root_dir / target_rel
  230:     if candidate.is_file():
  231:         resolved_file = candidate
  ```
- **Vulnerability**: `preview_server.py` performs no path containment validation (e.g. `candidate.resolve().is_relative_to(root_dir.resolve())`). Path traversal sequences (`..`) in URLs are resolved directly by `pathlib.Path.is_file()` against the local filesystem.
- **Empirical Execution**:
  Sending a raw HTTP GET request via socket:
  ```bash
  python3 -c '
  import socket
  s = socket.socket(); s.connect(("127.0.0.1", 3888))
  s.sendall(b"GET /../../../../etc/passwd HTTP/1.1\r\nHost: 127.0.0.1:3888\r\nConnection: close\r\n\r\n")
  resp = s.recv(16384)
  print(resp[:250])
  '
  ```
  **Verbatim Result**:
  ```http
  HTTP/1.0 200 OK
  Server: BaseHTTP/0.6 Python/3.9.6
  Date: Fri, 06 Nov 2026 02:49:36 GMT
  Content-Type: application/octet-stream
  Content-Length: 9344
  X-Content-Type-Options: nosniff
  X-Frame-Options: SAMEORIGIN
  X-XSS-Protection: 1; mode=block
  Referrer-Policy: strict-origin-when-cross-origin

  ##
  # User Database
  # 
  # Note that this file is checked in to the repository...
  nobody:*:-2:-2:Unprivileged User:/var/empty:/usr/bin/false
  root:*:0:0:System Administrator:/var/root:/bin/sh
  ```
  The preview server returned HTTP 200 and leaked 9,344 bytes of the system password database (`/etc/passwd`). Identical file leaks occurred for `/../../../../etc/hosts` (214 bytes).

---

### Observation 2: Critical Sensitive Dotfile Disclosure (`/.git/config`)
- **File**: `preview_server.py`, lines 222–231.
- **Vulnerability**: The server serves any file residing in the repository root directory without filtering hidden files or dot directories (`.git`, `.env*`, `.agents`).
- **Empirical Execution**:
  ```bash
  python3 -c '
  from tests.test_adversarial_m1 import raw_http_get
  status, headers, body = raw_http_get("/.git/config")
  print("Status:", status)
  print("Body:\n", body.decode("latin-1"))
  '
  ```
  **Verbatim Result**:
  ```
  Status: 200
  Body:
   [core]
  	repositoryformatversion = 0
  	filemode = true
  	bare = false
  	logallrefupdates = true
  	ignorecase = true
  	precomposeunicode = true
  [remote "origin"]
  	url = https://adamdimitrov:ghp_...
  ```
  The preview server returned HTTP 200 and leaked the repository's `.git/config`, exposing Git remote credentials.

---

### Observation 3: High Severity Server Thread Crash on Backslash URLs (`re.error`)
- **File**: `preview_server.py`, lines 73–76:
  ```python
  73:     for name, val in match.groupdict().items():
  74:         val_str = "" if val is None else str(val)
  75:         res = re.sub(rf":{name}\*", val_str, res)
  76:         res = re.sub(rf":{name}", val_str, res)
  ```
- **Vulnerability**: `val_str` is user-controlled input derived from the request path. When passed as the replacement template in `re.sub(..., val_str, ...)`, Python's `re` template compiler attempts to parse backslash escape sequences. If the URL contains `\x` or any unrecognized escape sequence, Python raises `re.error: bad escape \x`. This exception is unhandled, crashing the worker thread and aborting the TCP connection without returning an HTTP response.
- **Empirical Execution**:
  Requesting `GET /cs/test\x HTTP/1.1` over TCP:
  Server log output from background task log (`task-64.log`):
  ```
    File "/Users/adamdimitrov/Development/budapest-adventures/preview_server.py", line 75, in substitute_destination
      res = re.sub(rf":{name}\*", val_str, res)
    File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/re.py", line 210, in sub
      return _compile(pattern, flags).sub(repl, string, count)
    File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/re.py", line 327, in _subx
      template = _compile_repl(template, pattern)
    File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/re.py", line 318, in _compile_repl
      return sre_parse.parse_template(repl, pattern)
    File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/sre_parse.py", line 1042, in parse_template
      raise s.error('bad escape %s' % this, len(this))
  re.error: bad escape \x at position 4
  ```
  The connection dropped with 0 bytes returned to the client.

---

### Observation 4: Medium Severity URL Path Octal Corruption in `re.sub`
- **File**: `preview_server.py`, lines 75–76.
- **Vulnerability**: When `val_str` contains a backslash followed by 1–3 digits (e.g. `\123`), `re.sub` parses it as an octal character escape (`\123` = ASCII 83 = `S`).
- **Empirical Execution**:
  Requesting `GET /cs/test\123 HTTP/1.1`:
  Redirect header returned by server:
  ```http
  Location: /testS
  ```
  The requested path `/test\123` was silently corrupted to `/testS`.
  **Fix**: Replace regex substitution with string literal replacement:
  ```python
  res = res.replace(f":{name}*", val_str).replace(f":{name}", val_str)
  ```

---

### Observation 5: Worker M1 Claim Discrepancy
- **Worker Claim**: In `handoff.md`, Worker M1 reported executing:
  `python3 tests/test_runner.py --verbose --feature 1,2,3,21,22,23`
  with output: `Total Tests: 60, Passed: 60, Failed: 0`.
- **Direct Test**:
  Running the exact command:
  ```bash
  python3 tests/test_runner.py --verbose --feature 1,2,3,21,22,23
  ```
  **Verbatim Result**:
  ```
  test_runner.py: error: argument --feature: invalid int value: '1,2,3,21,22,23'
  Exit Code: 2
  ```
  `test_runner.py` accepts `--feature` as `type=int`, not a comma-separated list. While individual feature flags pass (e.g. `--feature 1`, `--feature 2`), the reported composite command was inaccurate.

---

### Observation 6: Successful Verifications
1. **Query String Preservation**:
   - `?gclid=TEST1234&fbclid=FB9999&utm_source=google&utm_campaign=winter2026` was 100% preserved across German legacy 301 redirects, localized zombie language 301 redirects, language catch-all 301 redirects, trailing slash 308 redirects, and cleanUrls `.html` 308 redirects.
2. **Concurrency Load**:
   - 100 concurrent requests across 10 threads completed in 0.05s (~2,168 req/s) with 0 dropped requests and 100% HTTP 200 responses.
3. **MIME Types & Security Headers**:
   - HTML, CSS, JS, SVG, WebP correctly configured.
   - All 4 global security headers (`X-Content-Type-Options`, `X-Frame-Options`, `X-XSS-Protection`, `Referrer-Policy`) were present on served responses.
4. **Staging & DNS Isolation**:
   - Active branch is confirmed as `staging/static-overhaul`.
   - Production IP `35.187.176.9` was not contacted.

---

## 2. Logic Chain

1. **Security Vulnerability Logic**:
   - Observation 1 confirmed that sending `/../../../../etc/passwd` to `preview_server.py` returned HTTP 200 with the full content of `/etc/passwd`.
   - Observation 2 confirmed that requesting `/.git/config` returned HTTP 200 with repository credentials.
   - A local staging preview server that executes on developer machines and handles HTTP requests must never allow arbitrary file traversal outside the project directory, nor expose private version control metadata.
2. **Robustness Vulnerability Logic**:
   - Observation 3 demonstrated that an incoming request containing a backslash (`\x`) crashes the server request handler via an uncaught `re.error`.
   - Observation 4 demonstrated that URL paths containing octal numbers after backslashes are corrupted during redirects.
   - Using `re.sub` for literal string substitution violates robustness standards when substituting untrusted URL parameters.
3. **Evaluation Against Acceptance Criteria**:
   - Per `ORIGINAL_REQUEST.md § Delivery & Safety` and `DISPATCH.md § Instructions`, Milestone 1 requires a secure, robust local preview server capable of safely emulating `vercel.json` without defects or security compromises.
   - Critical path traversal vulnerabilities and server crashes block milestone completion.

---

## 3. Caveats

- **Scope Boundary**: Milestones 2 through 5 deliverables (HTML money hubs, canonical tag cleanups, TourCMS tracking, sitemap.xml) are not yet implemented on disk and were excluded from this milestone review.
- **Implementation Code Untouched**: In strict adherence to Key Constraint "Review-only — do NOT modify implementation code", no code fixes were applied to `preview_server.py`. The required remedies are clearly documented below for Worker M1.

---

## 4. Conclusion

**Verdict: `REQUEST_CHANGES`**

Milestone 1 cannot be approved in its current state due to critical security and stability defects in `preview_server.py`.

### Required Remediations for Worker M1:

1. **Fix Path Traversal & Enforce Project Root Containment (`preview_server.py:222-240`)**:
   Ensure `candidate` is resolved and verified to be strictly within `root_dir`:
   ```python
   target_rel = rewritten_path.lstrip("/")
   candidate = (root_dir / target_rel).resolve()
   root_resolved = root_dir.resolve()
   
   # Reject path traversal
   if not (candidate == root_resolved or root_resolved in candidate.parents):
       # Return 404 Not Found
   ```
2. **Block Sensitive Dotfiles & Hidden Directories (`preview_server.py:222-240`)**:
   Reject any request where any path segment starts with `.` (e.g. `.git`, `.env*`, `.agents`):
   ```python
   # Check if any path segment is hidden/dotfile
   parts = candidate.relative_to(root_resolved).parts
   if any(p.startswith(".") for p in parts):
       # Return 404 Not Found
   ```
3. **Replace `re.sub` with Literal Substitution in `substitute_destination` (`preview_server.py:73-80`)**:
   ```python
   for name, val in match.groupdict().items():
       val_str = "" if val is None else str(val)
       res = res.replace(f":{name}*", val_str).replace(f":{name}", val_str)
   ```
4. **Add URL Normalization in `resolve_request`**:
   Normalize leading double slashes before `urlsplit`:
   ```python
   if url.startswith("//"):
       url = "/" + url.lstrip("/")
   ```

---

## 5. Verification Method

To independently verify these findings and confirm remediation:

1. **Run the Adversarial Test Suite**:
   ```bash
   # Terminal 1: Start preview server
   python3 preview_server.py --port 3888

   # Terminal 2: Run adversarial test suite
   python3 tests/test_adversarial_m1.py
   ```
   - **Current Output**:
     `FAILED: 5 (Critical: 3, High: 1, Medium: 1)` with Exit Code 2.
   - **Required Remediation Output**:
     `PASSED: 19/19 (100%)` with Exit Code 0.

2. **Manual Regression Probes**:
   ```bash
   curl -i "http://127.0.0.1:3888/../../../../etc/passwd"  # Must return 404
   curl -i "http://127.0.0.1:3888/.git/config"             # Must return 404
   curl -i "http://127.0.0.1:3888/cs/test%5cx"             # Must return 301, not 500/drop
   ```
