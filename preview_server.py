#!/usr/bin/env python3
"""Budapest Adventures — Staging Local Preview Server.

Zero-dependency HTTP preview server emulating Vercel's modern routing engine:
- cleanUrls (extensionless HTML URLs with 308 redirects for .html)
- trailingSlash: false (strips trailing slashes with 308 redirects)
- Custom redirects (301/308 with full query string and parameter preservation)
- Rewrites (mapping clean money hubs to physical HTML files)
- Security headers (X-Content-Type-Options, X-Frame-Options, etc.)
- Programmatic self-diagnostic test mode (--check / --test)
"""

import argparse
import http.server
import json
import mimetypes
import os
import re
import socketserver
import sys
import urllib.parse
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

MIME_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".mjs": "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".xml": "application/xml; charset=utf-8",
    ".txt": "text/plain; charset=utf-8",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".avif": "image/avif",
    ".gif": "image/gif",
    ".ico": "image/x-icon",
    ".woff": "font/woff",
    ".woff2": "font/woff2",
    ".ttf": "font/ttf",
}


def pattern_to_regex(pattern: str) -> re.Pattern:
    """Compile a Vercel/path-to-regexp route source pattern into a Python regex."""
    p = pattern
    # 1. Parameter with custom regex: :name(regex) -> (?P<name>regex)
    p = re.sub(r":([a-zA-Z0-9_]+)\(([^)]+)\)", r"(?P<\1>\2)", p)
    # 2. Parameter with zero-or-more segments: /:name* -> (?:/(?P<name>.*))?
    p = re.sub(r"/:([a-zA-Z0-9_]+)\*", r"(?:/(?P<\1>.*))?", p)
    # 3. Parameter with zero-or-more suffix without slash: :name* -> (?P<name>.*)
    p = re.sub(r":([a-zA-Z0-9_]+)\*", r"(?P<\1>.*)", p)
    # 4. Parameter with one-or-more segments: /:name+ -> /(?P<name>.+)
    p = re.sub(r"/:([a-zA-Z0-9_]+)\+", r"/(?P<\1>.+)", p)
    # 5. Single segment parameter: /:name -> /(?P<name>[^/]+)
    p = re.sub(r":([a-zA-Z0-9_]+)", r"(?P<\1>[^/]+)", p)
    
    # Ensure full-string match
    if not p.startswith("^"):
        p = "^" + p
    if not p.endswith("$"):
        p = p + "$"
    return re.compile(p)


def substitute_destination(destination: str, match: re.Match) -> str:
    """Substitute captured parameters or backreferences into destination URL."""
    res = destination
    # Substitute named groups e.g. :path* or :path using literal replacement
    for name, val in match.groupdict().items():
        val_str = "" if val is None else str(val)
        res = res.replace(f":{name}*", val_str).replace(f":{name}", val_str)
    # Substitute numbered backreferences e.g. $1, $2
    for i, val in enumerate(match.groups(), 1):
        val_str = "" if val is None else str(val)
        res = res.replace(f"${i}", val_str)
    # Clean up excess consecutive slashes while preserving leading slash or protocol
    if "://" not in res:
        res = re.sub(r"/+", "/", res)
        if not res.startswith("/"):
            res = "/" + res
    return res


class VercelConfig:
    """Loads and compiles routing rules from vercel.json."""

    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.clean_urls: bool = False
        self.trailing_slash: bool = False
        self.headers_rules: List[Tuple[re.Pattern, List[Dict[str, str]]]] = []
        self.redirect_rules: List[Tuple[re.Pattern, str, int]] = []
        self.rewrite_rules: List[Tuple[re.Pattern, str]] = []
        self.raw_config: Dict[str, Any] = {}
        self.load()

    def load(self):
        if not self.config_path.exists():
            raise FileNotFoundError(f"vercel.json not found at {self.config_path}")
        with open(self.config_path, "r", encoding="utf-8") as f:
            self.raw_config = json.load(f)

        self.clean_urls = bool(self.raw_config.get("cleanUrls", False))
        self.trailing_slash = bool(self.raw_config.get("trailingSlash", False))

        # Headers
        for h_def in self.raw_config.get("headers", []):
            src = h_def.get("source")
            headers = h_def.get("headers", [])
            if src and headers:
                self.headers_rules.append((pattern_to_regex(src), headers))

        # Redirects
        for r_def in self.raw_config.get("redirects", []):
            src = r_def.get("source")
            dest = r_def.get("destination")
            if src and dest:
                if "statusCode" in r_def:
                    status = int(r_def["statusCode"])
                elif r_def.get("permanent", True):
                    status = 308
                else:
                    status = 307
                self.redirect_rules.append((pattern_to_regex(src), dest, status))

        # Rewrites
        for rw_def in self.raw_config.get("rewrites", []):
            src = rw_def.get("source")
            dest = rw_def.get("destination")
            if src and dest:
                self.rewrite_rules.append((pattern_to_regex(src), dest))


class RouteResolution:
    """Represents the resolved destination for a request."""

    def __init__(
        self,
        original_url: str,
        is_redirect: bool = False,
        redirect_status: int = 0,
        redirect_location: str = "",
        rewritten_path: str = "",
        file_path: Optional[Path] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        self.original_url = original_url
        self.is_redirect = is_redirect
        self.redirect_status = redirect_status
        self.redirect_location = redirect_location
        self.rewritten_path = rewritten_path
        self.file_path = file_path
        self.headers = headers or {}


def resolve_request(url: str, root_dir: Path, config: VercelConfig) -> RouteResolution:
    """Evaluate Vercel routing logic against incoming URL path and query."""
    # Normalize leading multiple slashes to avoid netloc parsing confusion
    clean_url = re.sub(r"^/+", "/", url)
    parts = urllib.parse.urlsplit(clean_url)
    raw_path = parts.path or "/"
    query = parts.query

    # 1. Configured Redirects (evaluated first per Vercel spec)
    for pattern, dest_template, status in config.redirect_rules:
        match = pattern.match(raw_path)
        if match:
            dest = substitute_destination(dest_template, match)
            # Preserve incoming query string (append with & if dest already has ?, otherwise ?)
            if query:
                dest = f"{dest}&{query}" if "?" in dest else f"{dest}?{query}"
            headers = get_matching_headers(raw_path, config)
            return RouteResolution(
                original_url=url,
                is_redirect=True,
                redirect_status=status,
                redirect_location=dest,
                headers=headers,
            )

    # 2. Trailing slash check (trailingSlash: false)
    if not config.trailing_slash and raw_path != "/" and raw_path.endswith("/"):
        clean = raw_path.rstrip("/")
        dest = f"{clean}?{query}" if query else clean
        headers = get_matching_headers(raw_path, config)
        return RouteResolution(
            original_url=url,
            is_redirect=True,
            redirect_status=308,
            redirect_location=dest,
            headers=headers,
        )

    # 3. Clean URLs check (cleanUrls: true)
    if config.clean_urls and raw_path.endswith(".html"):
        clean = raw_path[:-5]
        if clean == "/index":
            clean = "/"
        dest = f"{clean}?{query}" if query else clean
        headers = get_matching_headers(raw_path, config)
        return RouteResolution(
            original_url=url,
            is_redirect=True,
            redirect_status=308,
            redirect_location=dest,
            headers=headers,
        )

    # 4. Configured Rewrites
    rewritten_path = raw_path
    for pattern, dest_template in config.rewrite_rules:
        match = pattern.match(raw_path)
        if match:
            rewritten_path = substitute_destination(dest_template, match)
            break

    # 5. Static File Resolution with Path Traversal & Dotfile Protection
    resolved_file: Optional[Path] = None
    target_rel = rewritten_path.lstrip("/")

    try:
        root_resolved = root_dir.resolve()
        # Reject traversal segments ('..') and hidden dotfiles/directories ('.*')
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
            # Enforce boundary: must be inside root_dir
            if candidate.is_relative_to(root_resolved):
                rel_parts = candidate.relative_to(root_resolved).parts
                if any(part.startswith(".") for part in rel_parts):
                    resolved_file = None
                elif candidate.is_file():
                    resolved_file = candidate
                elif candidate.is_dir() and (candidate / "index.html").is_file():
                    cand_index = (candidate / "index.html").resolve()
                    if cand_index.is_relative_to(root_resolved):
                        resolved_file = cand_index
                elif config.clean_urls:
                    cand_html = (root_dir / f"{target_rel}.html").resolve()
                    if cand_html.is_file() and cand_html.is_relative_to(root_resolved):
                        resolved_file = cand_html
    except (OSError, ValueError):
        resolved_file = None

    headers = get_matching_headers(raw_path, config)

    return RouteResolution(
        original_url=url,
        is_redirect=False,
        rewritten_path=rewritten_path,
        file_path=resolved_file,
        headers=headers,
    )


def get_matching_headers(path: str, config: VercelConfig) -> Dict[str, str]:
    """Retrieve all headers applicable to path."""
    headers: Dict[str, str] = {}
    for pattern, h_list in config.headers_rules:
        if pattern.match(path):
            for h in h_list:
                headers[h["key"]] = h["value"]
    return headers


class PreviewRequestHandler(http.server.BaseHTTPRequestHandler):
    """HTTP request handler implementing Vercel routing rules."""

    server_root: Path
    vercel_config: VercelConfig

    def do_HEAD(self):
        self.handle_request(send_body=False)

    def do_GET(self):
        self.handle_request(send_body=True)

    def handle_request(self, send_body: bool = True):
        resolution = resolve_request(self.path, self.server_root, self.vercel_config)

        # Handle Redirects (301, 307, 308)
        if resolution.is_redirect:
            self.send_response(resolution.redirect_status)
            self.send_header("Location", resolution.redirect_location)
            for k, v in resolution.headers.items():
                self.send_header(k, v)
            self.end_headers()
            if send_body:
                body = (
                    f"<!DOCTYPE html><html><head><meta http-equiv='refresh' "
                    f"content='0;url={resolution.redirect_location}'></head>"
                    f"<body>Redirecting to <a href='{resolution.redirect_location}'>"
                    f"{resolution.redirect_location}</a>...</body></html>"
                ).encode("utf-8")
                self.wfile.write(body)
            return

        # Handle API functions (e.g. /api/cron.py)
        if resolution.rewritten_path.startswith("/api/"):
            self.handle_api(resolution, send_body)
            return

        # Handle Static Files
        if resolution.file_path and resolution.file_path.is_file():
            try:
                with open(resolution.file_path, "rb") as f:
                    content = f.read()

                suffix = resolution.file_path.suffix.lower()
                mime = MIME_TYPES.get(suffix) or mimetypes.guess_type(str(resolution.file_path))[0] or "application/octet-stream"

                self.send_response(200)
                self.send_header("Content-Type", mime)
                self.send_header("Content-Length", str(len(content)))
                for k, v in resolution.headers.items():
                    self.send_header(k, v)
                self.end_headers()

                if send_body:
                    self.wfile.write(content)
                return
            except Exception as e:
                self.send_error(500, f"Error reading file: {e}")
                return

        # 404 Not Found
        self.send_response(404)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        for k, v in resolution.headers.items():
            self.send_header(k, v)
        self.end_headers()
        if send_body:
            body = (
                "<!DOCTYPE html><html><head><title>404 Not Found</title></head>"
                "<body style='font-family:sans-serif;padding:40px;text-align:center;'>"
                "<h1>404 — Page Not Found</h1>"
                f"<p>The requested URL <code>{self.path}</code> was not found on this preview server.</p>"
                f"<p><small>Rewritten to: <code>{resolution.rewritten_path}</code></small></p>"
                "</body></html>"
            ).encode("utf-8")
            self.wfile.write(body)

    def handle_api(self, resolution: RouteResolution, send_body: bool):
        """Minimal invocation or stub response for Vercel API functions."""
        # Clean API route confirmation
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        for k, v in resolution.headers.items():
            self.send_header(k, v)
        self.end_headers()
        if send_body:
            resp = json.dumps({
                "status": "preview_ok",
                "api_endpoint": resolution.rewritten_path,
                "message": "Budapest Adventures serverless API endpoint active in preview mode."
            }, indent=2).encode("utf-8")
            self.wfile.write(resp)

    def log_message(self, format, *args):
        # Clean logging format
        sys.stderr.write(f"[{self.log_date_time_string()}] {format % args}\n")


def run_diagnostics(root_dir: Path, config_path: Path) -> bool:
    """Programmatically verify vercel.json routing and server resolution."""
    print("=" * 70)
    print("BUDAPEST ADVENTURES — PREVIEW SERVER SELF-DIAGNOSTICS")
    print(f"Project Root: {root_dir}")
    print(f"Config File:  {config_path}")
    print("=" * 70)

    all_passed = True
    total_checks = 0
    passed_checks = 0

    def check(description: str, condition: bool, details: str = ""):
        nonlocal all_passed, total_checks, passed_checks
        total_checks += 1
        status = "PASS" if condition else "FAIL"
        if condition:
            passed_checks += 1
            print(f"  [✓] {description}")
        else:
            all_passed = False
            print(f"  [✗] {description} — FAILED")
            if details:
                print(f"      Details: {details}")

    # 1. Config Syntax and Schema Validation
    print("\n[Phase 1: vercel.json Schema Validation]")
    check("vercel.json exists", config_path.is_file())
    
    try:
        config = VercelConfig(config_path)
        check("Parse vercel.json successfully", True)
        check("cleanUrls is enabled (true)", config.clean_urls is True)
        check("trailingSlash is explicitly disabled (false)", config.trailing_slash is False)
        check("Legacy 'routes' property is absent (no schema conflict)", "routes" not in config.raw_config)
        check("Headers rules present", len(config.headers_rules) > 0)
        check("Redirect rules present", len(config.redirect_rules) > 0)
        check("Rewrite rules present", len(config.rewrite_rules) > 0)
    except Exception as e:
        check("Parse vercel.json successfully", False, str(e))
        return False

    # 2. Core Rewrites Resolution (Live BPA Routes)
    print("\n[Phase 2: Core Money Hubs Rewrites Resolution]")
    test_rewrites = [
        ("/", "/index.html"),
        ("/budapest-river-cruises", "/river.html"),
        ("/best-budapest-river-cruises", "/river.html"),
        ("/budapest-dinner-cruises", "/dinner.html"),
        ("/best-dinner-cruises-budapest", "/dinner.html"),
        (
            "/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest",
            "/candlelit-dinner-cruise.html",
        ),
        ("/about", "/about.html"),
        ("/api/cron", "/api/cron.py"),
    ]

    for incoming_path, expected_dest in test_rewrites:
        res = resolve_request(incoming_path, root_dir, config)
        is_ok = not res.is_redirect and res.rewritten_path == expected_dest
        check(
            f"Rewrite '{incoming_path}' -> '{expected_dest}'",
            is_ok,
            f"Got rewritten_path='{res.rewritten_path}', is_redirect={res.is_redirect}",
        )

    # 3. Redirects Resolution & Preservation
    print("\n[Phase 3: Redirects, CleanUrls & Query String Preservation]")
    test_redirects = [
        # Trailing slash
        ("/best-budapest-river-cruises/", "/best-budapest-river-cruises", 308),
        ("/budapest-dinner-cruises/?fbclid=xyz", "/budapest-dinner-cruises?fbclid=xyz", 308),
        # Clean URLs
        ("/dinner.html", "/dinner", 308),
        ("/index.html", "/", 308),
        ("/dinner.html?gclid=abc", "/dinner?gclid=abc", 308),
        # Localized dead language river cruise slugs (9 dead GSC languages)
        ("/da/bedste-budapest-flod", "/budapest-river-cruises", 301),
        ("/vi/du-thuy", "/budapest-river-cruises", 301),
        ("/nl/beste-boedapest-rivier", "/budapest-river-cruises", 301),
        # Active GSC traffic languages must NOT have river/dinner cruise hubs redirected
        ("/de/some-path", None, 0),
        ("/hu/setahajozas-a-dunan-budapest", None, 0),
        ("/cs/nejlepsi-budapest-reka-plavby", None, 0),
        # Zero-click translated non-cruise zombie paths across active foreign languages
        ("/hu/thermal-baths-budapest", "/thermal-baths-budapest", 301),
        ("/de/best-walking-tours-budapest", "/best-walking-tours-budapest", 301),
        ("/fr/best-hostels-budapest/party-hostels", "/best-hostels-budapest/party-hostels", 301),
        # Localized dead language dinner cruise slugs
        (
            "/ar/أفضل-رحلات-العشاء-البحرية-في-بودابست",
            "/budapest-dinner-cruises",
            301,
        ),
        ("/sv/bästa-middag", "/budapest-dinner-cruises", 301),
        # Dead language catch-all
        ("/da/tour-page", "/tour-page", 301),
        ("/da", "/", 301),
        # Query preservation through language redirect
        (
            "/da/bedste-budapest-flod?utm_source=meta&utm_campaign=spring&fbclid=123",
            "/budapest-river-cruises?utm_source=meta&utm_campaign=spring&fbclid=123",
            301,
        ),
    ]

    for item in test_redirects:
        incoming_path, expected_dest, expected_status = item
        res = resolve_request(incoming_path, root_dir, config)
        if expected_dest is None:
            # Should NOT redirect (e.g. approved language)
            check(
                f"Approved language '{incoming_path}' is NOT redirected",
                not res.is_redirect,
                f"Was unexpectedly redirected to '{res.redirect_location}'",
            )
        else:
            is_ok = res.is_redirect and res.redirect_location == expected_dest and res.redirect_status == expected_status
            check(
                f"Redirect '{incoming_path}' -> '{expected_dest}' (HTTP {expected_status})",
                is_ok,
                f"Got location='{res.redirect_location}', status={res.redirect_status}, is_redirect={res.is_redirect}",
            )

    # 4. Security Headers Test
    print("\n[Phase 4: Security Headers Verification]")
    sample_routes = ["/", "/best-budapest-river-cruises", "/best-dinner-cruises-budapest"]
    for path in sample_routes:
        res = resolve_request(path, root_dir, config)
        h = res.headers
        has_content_type_options = h.get("X-Content-Type-Options") == "nosniff"
        has_frame_options = h.get("X-Frame-Options") == "SAMEORIGIN"
        has_xss = h.get("X-XSS-Protection") == "1; mode=block"
        has_referrer = h.get("Referrer-Policy") == "strict-origin-when-cross-origin"
        all_h = has_content_type_options and has_frame_options and has_xss and has_referrer
        check(
            f"Security headers applied to '{path}'",
            all_h,
            f"Headers received: {h}",
        )

    # 5. File Resolution State Audit
    print("\n[Phase 5: Static File On-Disk Verification]")
    file_checks = [
        ("index.html", root_dir / "index.html"),
        ("river.html", root_dir / "river.html"),
        ("dinner.html", root_dir / "dinner.html"),
        ("candlelit-dinner-cruise.html", root_dir / "candlelit-dinner-cruise.html"),
        ("about.html", root_dir / "about.html"),
    ]
    for label, fpath in file_checks:
        exists = fpath.is_file()
        check(f"Static file '{label}' exists on disk", exists)

    # 6. Adversarial & Boundary Safety Verification
    print("\n[Phase 6: Adversarial & Boundary Safety Verification]")
    pt_res = resolve_request("/../../../../etc/passwd", root_dir, config)
    check("Path traversal (/../../../../etc/passwd) blocked", pt_res.file_path is None)

    git_res = resolve_request("/.git/config", root_dir, config)
    check("Dotfile exposure (/.git/config) blocked", git_res.file_path is None)

    env_res = resolve_request("/.env", root_dir, config)
    check("Dotfile exposure (/.env) blocked", env_res.file_path is None)

    ms_res = resolve_request("//best-budapest-river-cruises", root_dir, config)
    check("Multi-slash //best-budapest-river-cruises resolves to river.html", ms_res.rewritten_path == "/river.html")

    bs_res = resolve_request(r"/da/test\x", root_dir, config)
    check("Backslash URL (/da/test\\x) handled safely", bs_res.is_redirect and bs_res.redirect_location == r"/test\x")

    oct_res = resolve_request(r"/da/test\123", root_dir, config)
    check("Octal escape (/da/test\\123) preserved without corruption", oct_res.is_redirect and oct_res.redirect_location == r"/test\123")

    ar_res = resolve_request("/ar/", root_dir, config)
    check("Pruned language trailing slash (/ar/) returns 301 directly", ar_res.is_redirect and ar_res.redirect_status == 301 and ar_res.redirect_location == "/")

    nl_res = resolve_request("/nl/", root_dir, config)
    check("Pruned language trailing slash (/nl/) returns 301 directly", nl_res.is_redirect and nl_res.redirect_status == 301 and nl_res.redirect_location == "/")

    print("\n" + "=" * 70)
    print(f"DIAGNOSTIC SUMMARY: {passed_checks}/{total_checks} CHECKS PASSED")
    if all_passed:
        print("RESULT: ALL DIAGNOSTIC TESTS PASSED SUCCESSFULLY! (EXIT 0)")
    else:
        print("RESULT: SOME CHECKS FAILED! (EXIT 1)")
    print("=" * 70)

    return all_passed


def main():
    parser = argparse.ArgumentParser(description="Budapest Adventures Staging Preview Server")
    parser.add_argument("--port", type=int, default=3000, help="Port to listen on (default: 3000)")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host interface (default: 127.0.0.1)")
    parser.add_argument("--config", type=str, default="vercel.json", help="Path to vercel.json")
    parser.add_argument(
        "--test",
        "--check",
        dest="run_check",
        action="store_true",
        help="Run self-diagnostic route and config verification test suite and exit",
    )

    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent
    config_file = (project_root / args.config).resolve()

    if args.run_check:
        passed = run_diagnostics(project_root, config_file)
        sys.exit(0 if passed else 1)

    # Server mode
    config = VercelConfig(config_file)
    PreviewRequestHandler.server_root = project_root
    PreviewRequestHandler.vercel_config = config

    class ThreadedTCPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
        allow_reuse_address = True

    server_address = (args.host, args.port)
    try:
        with ThreadedTCPServer(server_address, PreviewRequestHandler) as httpd:
            print("=" * 60)
            print("BUDAPEST ADVENTURES — STAGING LOCAL PREVIEW SERVER")
            print(f"Serving at: http://{args.host}:{args.port}")
            print(f"Project Root: {project_root}")
            print(f"Vercel Config: {config_file}")
            print("Press Ctrl+C to terminate.")
            print("=" * 60)
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nShutting down server gracefully...")
                httpd.server_close()
    except OSError as e:
        if e.errno == 48 or "Address already in use" in str(e):
            print(f"Error: Port {args.port} is already in use. Please specify another port using --port <PORT>.", file=sys.stderr)
            sys.exit(1)
        raise


if __name__ == "__main__":
    main()
