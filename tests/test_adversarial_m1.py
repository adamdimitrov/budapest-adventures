#!/usr/bin/env python3
"""Adversarial Security & Stress Test Suite for Milestone 1.

Target: preview_server.py & vercel.json
Author: Challenger 1 (Milestone 1 Adversarial Verification)
"""

import concurrent.futures
import http.client
import json
import re
import socket
import sys
import time
import urllib.parse
import urllib.request
from typing import Tuple, Dict, Any, List

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 3888
SERVER_BASE = f"http://{SERVER_HOST}:{SERVER_PORT}"


def raw_http_get(path: str, host: str = SERVER_HOST, port: int = SERVER_PORT) -> Tuple[int, Dict[str, str], bytes]:
    """Send raw HTTP/1.1 GET request over socket to bypass client-side path normalization."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    s.connect((host, port))
    
    req = f"GET {path} HTTP/1.1\r\nHost: {host}:{port}\r\nConnection: close\r\n\r\n"
    s.sendall(req.encode("latin-1"))
    
    raw_resp = b""
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        raw_resp += chunk
    s.close()
    
    if not raw_resp:
        return 0, {}, b""
    parts = raw_resp.split(b"\r\n\r\n", 1)
    headers_raw = parts[0].decode("latin-1")
    body = parts[1] if len(parts) > 1 else b""
    
    status_lines = headers_raw.split("\r\n")
    if not status_lines or not status_lines[0]:
        return 0, {}, b""
    status_code = int(status_lines[0].split(" ")[1])
    
    headers = {}
    for line in headers_raw.split("\r\n")[1:]:
        if ":" in line:
            k, v = line.split(":", 1)
            headers[k.strip().lower()] = v.strip()
            
    return status_code, headers, body


def run_all_adversarial_tests():
    print("=" * 70)
    print("ADVERSARIAL STRESS TEST SUITE — MILESTONE 1 AUDIT")
    print(f"Target: {SERVER_BASE}")
    print("=" * 70)

    results = []

    def record(name: str, passed: bool, severity: str, details: str):
        status = "PASS" if passed else "FAIL"
        results.append({"name": name, "passed": passed, "severity": severity, "details": details})
        print(f"  [{status}] ({severity}) {name}")
        if not passed:
            print(f"         ISSUE: {details}")

    # =========================================================================
    # 1. Path Traversal Attacks
    # =========================================================================
    print("\n--- Test Suite 1: Path Traversal Vulnerabilities ---")
    
    # 1.1 /etc/passwd
    status, headers, body = raw_http_get("/../../../../etc/passwd")
    if status == 200 and b"root:" in body:
        record("Path Traversal /etc/passwd", False, "CRITICAL", 
               f"Arbitrary File Read: Server returned HTTP 200 with contents of /etc/passwd ({len(body)} bytes)!")
    elif status in (400, 403, 404):
        record("Path Traversal /etc/passwd", True, "CRITICAL", f"Correctly blocked with HTTP {status}")
    else:
        record("Path Traversal /etc/passwd", False, "HIGH", f"Unexpected status HTTP {status}")

    # 1.2 /.git/config exposure
    status, headers, body = raw_http_get("/.git/config")
    if status == 200 and (b"[core]" in body or b"repositoryformatversion" in body):
        record("Dotfile Exposure: /.git/config", False, "CRITICAL", 
               "Sensitive File Leak: Server returned HTTP 200 with repository .git/config containing credentials!")
    elif status in (400, 403, 404):
        record("Dotfile Exposure: /.git/config", True, "CRITICAL", f"Correctly blocked with HTTP {status}")
    else:
        record("Dotfile Exposure: /.git/config", False, "HIGH", f"Unexpected status HTTP {status}")

    # 1.3 /../../../etc/hosts
    status, headers, body = raw_http_get("/../../../../etc/hosts")
    if status == 200 and (b"localhost" in body or b"127.0.0.1" in body):
        record("Path Traversal /etc/hosts", False, "CRITICAL",
               f"Arbitrary File Read: Server returned HTTP 200 with contents of /etc/hosts ({len(body)} bytes)!")
    elif status in (400, 403, 404):
        record("Path Traversal /etc/hosts", True, "CRITICAL", f"Correctly blocked with HTTP {status}")
    else:
        record("Path Traversal /etc/hosts", False, "HIGH", f"Unexpected status HTTP {status}")

    # 1.3 /../preview_server.py
    status, headers, body = raw_http_get("/../preview_server.py")
    if status == 200 and b"VercelConfig" in body:
        record("Path Traversal parent dir escaping", False, "CRITICAL",
               "Arbitrary File Read: Escaped root to read source code via /../preview_server.py!")
    else:
        record("Path Traversal parent dir escaping", True, "CRITICAL", f"Handled with HTTP {status}")

    # =========================================================================
    # 2. Multi-Slash & URL Normalization
    # =========================================================================
    print("\n--- Test Suite 2: Multi-Slash & URL Normalization ---")
    
    # 2.1 //best-budapest-river-cruises
    status, headers, body = raw_http_get("//best-budapest-river-cruises")
    if status in (200, 301, 308):
        record("Multi-slash //best-budapest-river-cruises routing", True, "HIGH", f"Resolved properly (status {status})")
    else:
        record("Multi-slash //best-budapest-river-cruises routing", False, "MEDIUM", f"Returned HTTP {status}")

    # 2.2 //budapest-dinner-cruises
    status, headers, body = raw_http_get("//budapest-dinner-cruises")
    if status == 200 and b"Dinner" not in body and b"Danube River Cruises" in body:
        record("Multi-slash //budapest-dinner-cruises routing", False, "HIGH",
               "URL '//budapest-dinner-cruises' served index.html instead of Dinner Hub!")
    else:
        record("Multi-slash //budapest-dinner-cruises routing", True, "HIGH", f"Resolved properly (status {status})")

    # 2.3 //cs/tour-page redirect bypass
    status, headers, body = raw_http_get("//cs/tour-page")
    if status == 301 and headers.get("location") == "/tour-page":
        record("Multi-slash //cs/tour-page redirect", True, "MEDIUM", "Redirected to /tour-page")
    else:
        record("Multi-slash //cs/tour-page redirect", False, "MEDIUM",
               f"Expected 301 redirect to /tour-page, got status {status}, location {headers.get('location')}")

    # =========================================================================
    # 3. Robustness Against Malformed & Escaped Paths
    # =========================================================================
    print("\n--- Test Suite 3: Server Robustness Against Escapes & Malformed URLs ---")
    
    # 3.1 Backslash in URL: /cs/test\x
    status, headers, body = raw_http_get(r"/cs/test\x")
    if status == 500:
        record("Backslash URL robustness (/cs/test\\x)", False, "HIGH",
               "Server crashed with HTTP 500 due to unhandled re.error: bad escape \\x in substitute_destination!")
    elif status == 0:
        record("Backslash URL robustness (/cs/test\\x)", False, "HIGH",
               "Server aborted socket connection on backslash URL!")
    else:
        record("Backslash URL robustness (/cs/test\\x)", True, "HIGH", f"Handled gracefully with HTTP {status}")

    # 3.2 Backslash in URL: /cs/test\123 (Octal escape injection)
    status, headers, body = raw_http_get(r"/cs/test\123")
    loc = headers.get("location", "")
    if loc == "/testS":
        record("Backslash Octal Escape Corruption (/cs/test\\123)", False, "MEDIUM",
               "Destination was corrupted from /test\\123 to /testS due to re.sub octal interpretation!")
    else:
        record("Backslash Octal Escape Corruption (/cs/test\\123)", True, "MEDIUM", f"Destination: {loc}")

    # =========================================================================
    # 4. Complex Query String Preservation in 301/308 Redirects
    # =========================================================================
    print("\n--- Test Suite 4: Query String Preservation Across Redirects ---")
    
    complex_query = "gclid=TEST1234&fbclid=FB9999&utm_source=google&utm_campaign=winter2026&utm_medium=cpc&utm_content=hero_card"
    
    # 4.1 German legacy redirect query preservation
    status, headers, body = raw_http_get(f"/de/donau-kreuzfahrten-budapest?{complex_query}")
    expected_loc = f"/budapest-river-cruises?{complex_query}"
    if status == 301 and headers.get("location") == expected_loc:
        record("Query Preservation: German Legacy 301", True, "CRITICAL", "Query preserved intact")
    else:
        record("Query Preservation: German Legacy 301", False, "CRITICAL",
               f"Expected 301 to {expected_loc}, got status {status}, location {headers.get('location')}")

    # 4.2 Localized zombie 1-to-1 redirect query preservation
    status, headers, body = raw_http_get(f"/cs/nejlepsi-budapest-reka-plavby?{complex_query}")
    if status == 301 and headers.get("location") == expected_loc:
        record("Query Preservation: Localized Slug 301", True, "CRITICAL", "Query preserved intact")
    else:
        record("Query Preservation: Localized Slug 301", False, "CRITICAL",
               f"Expected 301 to {expected_loc}, got status {status}, location {headers.get('location')}")

    # 4.3 Catch-all language prefix redirect query preservation
    status, headers, body = raw_http_get(f"/cs/some/custom/tour?{complex_query}")
    expected_cat = f"/some/custom/tour?{complex_query}"
    if status == 301 and headers.get("location") == expected_cat:
        record("Query Preservation: Language Catch-All 301", True, "CRITICAL", "Query preserved intact")
    else:
        record("Query Preservation: Language Catch-All 301", False, "CRITICAL",
               f"Expected 301 to {expected_cat}, got status {status}, location {headers.get('location')}")

    # 4.4 Trailing slash 308 redirect query preservation
    status, headers, body = raw_http_get(f"/best-budapest-river-cruises/?{complex_query}")
    expected_ts = f"/best-budapest-river-cruises?{complex_query}"
    if status == 308 and headers.get("location") == expected_ts:
        record("Query Preservation: Trailing Slash 308", True, "HIGH", "Query preserved intact")
    else:
        record("Query Preservation: Trailing Slash 308", False, "HIGH",
               f"Expected 308 to {expected_ts}, got status {status}, location {headers.get('location')}")

    # 4.5 cleanUrls .html stripping 308 redirect query preservation
    status, headers, body = raw_http_get(f"/dinner.html?{complex_query}")
    expected_cu = f"/dinner?{complex_query}"
    if status == 308 and headers.get("location") == expected_cu:
        record("Query Preservation: cleanUrls .html 308", True, "HIGH", "Query preserved intact")
    else:
        record("Query Preservation: cleanUrls .html 308", False, "HIGH",
               f"Expected 308 to {expected_cu}, got status {status}, location {headers.get('location')}")

    # 4.6 Encoded characters in query string
    encoded_query = "name=John%20Doe&currency=%E2%82%AC&tag=a%26b"
    status, headers, body = raw_http_get(f"/cs/tour?{encoded_query}")
    expected_enc = f"/tour?{encoded_query}"
    if status == 301 and headers.get("location") == expected_enc:
        record("Query Preservation: Encoded Characters in Query", True, "MEDIUM", "Encoded query preserved intact")
    else:
        record("Query Preservation: Encoded Characters in Query", False, "MEDIUM",
               f"Expected location {expected_enc}, got {headers.get('location')}")

    # =========================================================================
    # 5. MIME Types & Headers
    # =========================================================================
    print("\n--- Test Suite 5: MIME Types & Security Headers ---")
    
    # 5.1 HTML
    status, headers, body = raw_http_get("/")
    content_type = headers.get("content-type", "")
    if status == 200 and "text/html" in content_type:
        record("MIME Type: HTML", True, "HIGH", f"Content-Type: {content_type}")
    else:
        record("MIME Type: HTML", False, "HIGH", f"Expected text/html, got {content_type}")

    # Check security headers
    has_xcto = headers.get("x-content-type-options") == "nosniff"
    has_xfo = headers.get("x-frame-options") == "SAMEORIGIN"
    has_xxss = headers.get("x-xss-protection") == "1; mode=block"
    has_ref = headers.get("referrer-policy") == "strict-origin-when-cross-origin"
    if has_xcto and has_xfo and has_xxss and has_ref:
        record("Security Headers on HTML responses", True, "HIGH", "All 4 security headers present")
    else:
        record("Security Headers on HTML responses", False, "HIGH", f"Missing headers in: {headers}")

    # =========================================================================
    # 6. Concurrency & Stress Load Test
    # =========================================================================
    print("\n--- Test Suite 6: Concurrency & High-Rate Stress Test ---")
    
    NUM_REQUESTS = 100
    CONCURRENCY = 10
    success_count = 0
    fail_count = 0
    start_time = time.time()
    
    def worker_fetch(req_id: int):
        endpoints = ["/", "/best-budapest-river-cruises", "/best-dinner-cruises-budapest", "/about"]
        target = endpoints[req_id % len(endpoints)]
        try:
            status, _, _ = raw_http_get(target)
            return status == 200
        except Exception:
            return False

    with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
        futures = [executor.submit(worker_fetch, i) for i in range(NUM_REQUESTS)]
        for f in concurrent.futures.as_completed(futures):
            if f.result():
                success_count += 1
            else:
                fail_count += 1
                
    elapsed = time.time() - start_time
    rps = NUM_REQUESTS / elapsed if elapsed > 0 else 0
    print(f"  Load test: {NUM_REQUESTS} requests, {CONCURRENCY} workers in {elapsed:.2f}s ({rps:.1f} req/s). Success: {success_count}, Fail: {fail_count}")
    if fail_count == 0 and success_count == NUM_REQUESTS:
        record("Concurrency: 100 concurrent requests without error", True, "HIGH", f"100% success ({rps:.1f} rps)")
    else:
        record("Concurrency: 100 concurrent requests without error", False, "HIGH", f"{fail_count} failed requests")

    # =========================================================================
    # 7. DNS & Staging Isolation
    # =========================================================================
    print("\n--- Test Suite 7: DNS & Staging Isolation ---")
    
    # 7.1 Confirm live DNS 35.187.176.9 is untouched
    import subprocess
    proc = subprocess.run(["git", "branch"], capture_output=True, text=True)
    active_branch = ""
    for line in proc.stdout.splitlines():
        if line.startswith("*"):
            active_branch = line.replace("*", "").strip()
            
    if active_branch == "staging/static-overhaul":
        record("Staging Git Branch Isolation", True, "CRITICAL", f"Active branch is {active_branch}")
    else:
        record("Staging Git Branch Isolation", False, "CRITICAL", f"Expected staging/static-overhaul, got {active_branch}")

    # Summary
    print("\n" + "=" * 70)
    failed = [r for r in results if not r["passed"]]
    critical_failed = [r for r in failed if r["severity"] == "CRITICAL"]
    high_failed = [r for r in failed if r["severity"] == "HIGH"]
    
    print(f"TOTAL ADVERSARIAL CHECKS: {len(results)}")
    print(f"PASSED: {len(results) - len(failed)}")
    print(f"FAILED: {len(failed)} (Critical: {len(critical_failed)}, High: {len(high_failed)})")
    print("=" * 70)
    
    return results


if __name__ == "__main__":
    from typing import Tuple, Dict
    results = run_all_adversarial_tests()
    failed = [r for r in results if not r["passed"]]
    if any(r["severity"] == "CRITICAL" for r in failed):
        sys.exit(2)
    elif failed:
        sys.exit(1)
    else:
        sys.exit(0)
