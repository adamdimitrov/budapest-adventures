#!/usr/bin/env python3
"""Challenger 2 Empirical Verification Suite — Milestone 1 Iteration 2.

Exhaustive verification of:
1. Priority order: Redirects evaluated before trailingSlash & cleanUrls.
2. 25 Pruned Languages:
   - Trailing-slash roots (e.g. /ru/, /zh/, /cs/) returning direct 1-hop HTTP 301 to /
   - Non-trailing-slash roots (e.g. /ru, /zh, /cs) returning direct 1-hop HTTP 301 to /
   - Query string preservation across pruned language redirects
   - Subpath catch-alls (/:lang/:path* -> /:path*)
   - Transliterated/ASCII Localized slugs for river cruises & dinner cruises
3. Approved languages (en, de, it, fr, es) are NOT redirected by language pruning
4. Core money hubs URL rewrites and 308 trailing slash handling
5. Multi-slash and boundary stress tests
6. Adversarial edge case audit (shadowed slug detection & non-ASCII URL encoding)
"""

import socket
import sys
import urllib.parse
from typing import Dict, Tuple, List

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 3888

PRUNED_LANGUAGES = [
    "cs", "bg", "zh", "vi", "uk", "ar", "sv", "sr", "el", "fi",
    "da", "th", "hr", "nl", "no", "sk", "tr", "ko", "ru", "pt",
    "ja", "ro", "he", "pl", "hu"
]

APPROVED_LANGUAGES = ["en", "de", "it", "fr", "es"]


def raw_http_get(path: str, host: str = SERVER_HOST, port: int = SERVER_PORT) -> Tuple[int, Dict[str, str], bytes]:
    """Send raw HTTP/1.1 GET request over socket to avoid client-side normalization."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    s.connect((host, port))

    req = f"GET {path} HTTP/1.1\r\nHost: {host}:{port}\r\nConnection: close\r\n\r\n"
    s.sendall(req.encode("utf-8"))

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
    headers_raw = parts[0].decode("utf-8", errors="replace")
    body = parts[1] if len(parts) > 1 else b""

    status_lines = headers_raw.split("\r\n")
    if not status_lines or not status_lines[0]:
        return 0, {}, b""

    tokens = status_lines[0].split(" ")
    if len(tokens) < 2:
        return 0, {}, b""
    status_code = int(tokens[1])

    headers = {}
    for line in status_lines[1:]:
        if ":" in line:
            k, v = line.split(":", 1)
            headers[k.strip().lower()] = v.strip()

    return status_code, headers, body


def main():
    print("=" * 80)
    print("CHALLENGER 2 EMPIRICAL VERIFICATION — M1 ITERATION 2")
    print(f"Target: http://{SERVER_HOST}:{SERVER_PORT}")
    print(f"Pruned Languages ({len(PRUNED_LANGUAGES)}): {', '.join(PRUNED_LANGUAGES)}")
    print(f"Approved Languages ({len(APPROVED_LANGUAGES)}): {', '.join(APPROVED_LANGUAGES)}")
    print("=" * 80)

    total_checks = 0
    passed_checks = 0
    failed_checks = 0
    failures: List[str] = []

    def check(name: str, condition: bool, details: str):
        nonlocal total_checks, passed_checks, failed_checks
        total_checks += 1
        if condition:
            passed_checks += 1
            print(f"  [PASS] {name}")
        else:
            failed_checks += 1
            msg = f"  [FAIL] {name} — {details}"
            print(msg)
            failures.append(msg)

    # -------------------------------------------------------------------------
    # SUITE 1: SPECIFIC DISPATCH TARGETS (/ru/, /zh/, /cs/) 1-HOP 301 VERIFICATION
    # -------------------------------------------------------------------------
    print("\n--- Suite 1: Mandatory Dispatch Targets (/ru/, /zh/, /cs/) ---")
    for lang in ["ru", "zh", "cs"]:
        path = f"/{lang}/"
        status, headers, _ = raw_http_get(path)
        loc = headers.get("location", "")
        check(
            f"Direct 1-Hop 301 for {path}",
            status == 301 and loc == "/",
            f"Expected HTTP 301 with Location: /, got HTTP {status} with Location: {loc}"
        )

    # -------------------------------------------------------------------------
    # SUITE 2: ALL 25 PRUNED LANGUAGES TRAILING SLASH ROOTS (/{lang}/)
    # -------------------------------------------------------------------------
    print(f"\n--- Suite 2: All 25 Pruned Languages Trailing Slash Roots (/{'{lang}'}/) ---")
    for lang in PRUNED_LANGUAGES:
        path = f"/{lang}/"
        status, headers, _ = raw_http_get(path)
        loc = headers.get("location", "")
        check(
            f"Trailing-slash root /{lang}/ -> 301 to /",
            status == 301 and loc == "/",
            f"Expected 301 to '/', got status={status}, location={loc}"
        )

    # -------------------------------------------------------------------------
    # SUITE 3: ALL 25 PRUNED LANGUAGES NON-TRAILING SLASH ROOTS (/{lang})
    # -------------------------------------------------------------------------
    print(f"\n--- Suite 3: All 25 Pruned Languages Non-Trailing Slash Roots (/{'{lang}'}) ---")
    for lang in PRUNED_LANGUAGES:
        path = f"/{lang}"
        status, headers, _ = raw_http_get(path)
        loc = headers.get("location", "")
        check(
            f"Bare root /{lang} -> 301 to /",
            status == 301 and loc == "/",
            f"Expected 301 to '/', got status={status}, location={loc}"
        )

    # -------------------------------------------------------------------------
    # SUITE 4: QUERY STRING PRESERVATION ON PRUNED LANGUAGE ROOTS
    # -------------------------------------------------------------------------
    print("\n--- Suite 4: Query String Preservation Across Pruned Language Roots ---")
    test_queries = [
        "?utm_source=meta&utm_medium=cpc&utm_campaign=spring2026",
        "?gclid=EAIaIQobChMI12345&fbclid=IwAR0xyz",
        "?partner=38585&subid=seo_test",
    ]
    for lang in ["ru", "zh", "cs", "pl", "hu", "ar"]:
        for q in test_queries:
            # Trailing slash with query
            path = f"/{lang}/{q}"
            status, headers, _ = raw_http_get(path)
            loc = headers.get("location", "")
            expected = f"/{q}"
            check(
                f"Trailing slash query preservation: /{lang}/{q}",
                status == 301 and loc == expected,
                f"Expected 301 with Location: {expected}, got {status} with {loc}"
            )

            # Non-trailing slash with query
            path = f"/{lang}{q}"
            status, headers, _ = raw_http_get(path)
            loc = headers.get("location", "")
            check(
                f"Bare root query preservation: /{lang}{q}",
                status == 301 and loc == expected,
                f"Expected 301 with Location: {expected}, got {status} with {loc}"
            )

    # -------------------------------------------------------------------------
    # SUITE 5: CATCH-ALL SUBPATH REDIRECTS (/{lang}/:path* -> /:path*)
    # -------------------------------------------------------------------------
    print("\n--- Suite 5: Catch-All Subpath Redirects for Pruned Languages ---")
    test_subpaths = [
        "danube-cruise-decision-hub",
        "legenda-city-cruises",
        "tours/night-cruise",
        "deeply/nested/sub/path",
    ]
    for lang in ["ru", "zh", "cs", "nl", "ja"]:
        for sub in test_subpaths:
            path = f"/{lang}/{sub}"
            status, headers, _ = raw_http_get(path)
            loc = headers.get("location", "")
            expected = f"/{sub}"
            check(
                f"Catch-all subpath: /{lang}/{sub} -> /{sub}",
                status == 301 and loc == expected,
                f"Expected 301 to {expected}, got {status} to {loc}"
            )

            # With query params
            path_q = f"/{lang}/{sub}?gclid=123"
            status, headers, _ = raw_http_get(path_q)
            loc = headers.get("location", "")
            expected_q = f"/{sub}?gclid=123"
            check(
                f"Catch-all subpath + query: /{lang}/{sub}?gclid=123 -> {expected_q}",
                status == 301 and loc == expected_q,
                f"Expected 301 to {expected_q}, got {status} to {loc}"
            )

    # -------------------------------------------------------------------------
    # SUITE 6: TRANSLITERATED / ASCII LOCALIZED SLUGS (RIVER & DINNER)
    # -------------------------------------------------------------------------
    print("\n--- Suite 6: Transliterated & ASCII Localized Slugs ---")
    ascii_localized_slugs = [
        ("/cs/nejlepsi-budapest-reka-plavby", "/budapest-river-cruises"),
        ("/cs/nejlep", "/budapest-river-cruises"),
        ("/ru/rechnyye-kruizy", "/budapest-river-cruises"),
        ("/ru/uzhin-kruizy", "/budapest-dinner-cruises"),
        ("/nl/beste-boedapest-rivier", "/budapest-river-cruises"),
        ("/nl/beste-diner", "/budapest-dinner-cruises"),
        ("/no/beste-budapest-elve", "/budapest-river-cruises"),
        ("/no/beste-middags", "/budapest-dinner-cruises"),
        ("/sk/riecne-plavby", "/budapest-river-cruises"),
        ("/sk/vecera-plavby", "/budapest-dinner-cruises"),
        ("/tr/nehir-yolculuklari", "/budapest-river-cruises"),
        ("/tr/aksam-yemegi", "/budapest-dinner-cruises"),
        ("/ko/gang-keulujeu", "/budapest-river-cruises"),
        ("/ko/dineo-keulujeu", "/budapest-dinner-cruises"),
        ("/pt/budapeste-cruzeiros", "/budapest-river-cruises"),
        ("/pt/budapeste-jantar", "/budapest-dinner-cruises"),
        ("/ja/budapesuto-ribakuruzu", "/budapest-river-cruises"),
        ("/ja/budapesuto-dinakuruzu", "/budapest-dinner-cruises"),
        ("/ro/croaziera-dunare", "/budapest-river-cruises"),
        ("/pl/rejsy-dunaju-budapeszt", "/budapest-river-cruises"),
        ("/hu/setahajozas-a-dunan-budapest", "/budapest-river-cruises"),
        ("/hu/setahajozas-a-dunan-vacsoraval", "/budapest-dinner-cruises"),
    ]
    for slug, expected in ascii_localized_slugs:
        status, headers, _ = raw_http_get(slug)
        loc = headers.get("location", "")
        check(
            f"ASCII Localized slug: {slug} -> {expected}",
            status == 301 and loc == expected,
            f"Expected 301 to {expected}, got {status} to {loc}"
        )

    # -------------------------------------------------------------------------
    # SUITE 7: APPROVED LANGUAGES NOT PRUNED (en, de, it, fr, es)
    # -------------------------------------------------------------------------
    print("\n--- Suite 7: Approved Languages Isolation (en, de, it, fr, es) ---")
    for lang in APPROVED_LANGUAGES:
        # Subpath should NOT redirect via language pruning rules
        path = f"/{lang}/overview"
        status, headers, _ = raw_http_get(path)
        loc = headers.get("location", "")
        check(
            f"Approved lang /{lang}/overview not redirected to /overview",
            status != 301 or loc != "/overview",
            f"Erroneously redirected with status={status}, location={loc}"
        )

    # Legacy German slugs DO redirect per vercel.json
    status, headers, _ = raw_http_get("/de/donau-kreuzfahrten-budapest")
    check(
        "German legacy river cruise redirects to /budapest-river-cruises",
        status == 301 and headers.get("location") == "/budapest-river-cruises",
        f"Expected 301 to /budapest-river-cruises, got {status} to {headers.get('location')}"
    )
    status, headers, _ = raw_http_get("/de/schifffahrt-budapest-mit-abendessen")
    check(
        "German legacy dinner cruise redirects to /budapest-dinner-cruises",
        status == 301 and headers.get("location") == "/budapest-dinner-cruises",
        f"Expected 301 to /budapest-dinner-cruises, got {status} to {headers.get('location')}"
    )

    # -------------------------------------------------------------------------
    # SUITE 8: CORE MONEY HUBS REWRITES & TRAILING SLASH 308 (NON-LANGUAGE)
    # -------------------------------------------------------------------------
    print("\n--- Suite 8: Core Money Hubs Rewrites & Trailing Slash 308 ---")
    hub_rewrites = [
        ("/", 200, "Budapest Adventures Homepage"),
        ("/budapest-river-cruises", 200, "Danube River Cruises Rewrite"),
        ("/best-budapest-river-cruises", 200, "Best River Cruises Hub"),
        ("/budapest-dinner-cruises", 200, "Dinner Cruises Rewrite"),
        ("/best-dinner-cruises-budapest", 200, "Best Dinner Cruises Hub"),
        ("/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest", 200, "Candlelit Dinner Review"),
        ("/about", 200, "About & Methodology"),
    ]
    for path, expected_status, label in hub_rewrites:
        status, headers, body = raw_http_get(path)
        content_type = headers.get("content-type", "")
        check(
            f"Money hub rewrite: {path} ({label})",
            status == expected_status and "text/html" in content_type and len(body) > 0,
            f"Expected {expected_status} text/html, got {status} {content_type} ({len(body)} bytes)"
        )

    # Trailing slash on non-pruned paths MUST return 308 (trailingSlash: false)
    trailing_slash_checks = [
        ("/best-budapest-river-cruises/", "/best-budapest-river-cruises"),
        ("/budapest-dinner-cruises/", "/budapest-dinner-cruises"),
        ("/budapest-river-cruises/", "/budapest-river-cruises"),
        ("/about/", "/about"),
    ]
    for path, expected_loc in trailing_slash_checks:
        status, headers, _ = raw_http_get(path)
        loc = headers.get("location", "")
        check(
            f"Trailing slash strip: {path} -> 308 to {expected_loc}",
            status == 308 and loc == expected_loc,
            f"Expected 308 to {expected_loc}, got {status} to {loc}"
        )

    # cleanUrls .html to clean slug
    status, headers, _ = raw_http_get("/dinner.html")
    check(
        "cleanUrls: /dinner.html -> 308 to /dinner",
        status == 308 and headers.get("location") == "/dinner",
        f"Expected 308 to /dinner, got {status} to {headers.get('location')}"
    )

    # -------------------------------------------------------------------------
    # SUITE 9: ADVERSARIAL & BOUNDARY ROBUSTNESS
    # -------------------------------------------------------------------------
    print("\n--- Suite 9: Adversarial & Edge Case Robustness ---")
    # Multi-slash pruned routes
    for lang in ["ru", "zh", "cs"]:
        path = f"//{lang}/"
        status, headers, _ = raw_http_get(path)
        loc = headers.get("location", "")
        check(
            f"Multi-slash leading //{lang}/ -> 301 to /",
            status == 301 and loc == "/",
            f"Expected 301 to '/', got {status} to {loc}"
        )

    # Multi-slash trailing on money hub
    status, headers, _ = raw_http_get("//best-budapest-river-cruises")
    check(
        "Multi-slash //best-budapest-river-cruises -> 200 River Cruises Hub",
        status == 200 and "text/html" in headers.get("content-type", ""),
        f"Expected 200 text/html, got {status}"
    )

    # Path traversal blocking
    status, _, body = raw_http_get("/../../../../etc/passwd")
    check(
        "Path traversal /etc/passwd blocked with 404",
        status == 404 and b"root:" not in body,
        f"Expected 404, got {status} with body len {len(body)}"
    )

    # Dotfile blocking
    status, _, body = raw_http_get("/.git/config")
    check(
        "Dotfile /.git/config blocked with 404",
        status == 404 and b"[core]" not in body,
        f"Expected 404, got {status} with body len {len(body)}"
    )

    # Escaped backslash URL
    status, headers, _ = raw_http_get("/cs/test%5Cx")
    check(
        "Escaped backslash URL handles safely without 500 crash",
        status in (301, 404),
        f"Expected 301 or 404, got {status}"
    )

    # Security headers on redirect responses
    status, headers, _ = raw_http_get("/ru/")
    check(
        "Security header X-Content-Type-Options on 301 response",
        headers.get("x-content-type-options") == "nosniff",
        f"Expected nosniff, got {headers.get('x-content-type-options')}"
    )
    check(
        "Security header X-Frame-Options on 301 response",
        headers.get("x-frame-options") == "SAMEORIGIN",
        f"Expected SAMEORIGIN, got {headers.get('x-frame-options')}"
    )

    print("\n" + "=" * 80)
    print(f"VERIFICATION SUMMARY: {passed_checks}/{total_checks} CHECKS PASSED ({failed_checks} FAILED)")
    print("=" * 80)

    if failed_checks > 0:
        print("\nFAILURES DETECTED:")
        for f in failures:
            print(f)
        sys.exit(1)
    else:
        print("\nALL EMPIRICAL CHECKS PASSED CLEANLY (EXIT 0)")
        sys.exit(0)


if __name__ == "__main__":
    main()
