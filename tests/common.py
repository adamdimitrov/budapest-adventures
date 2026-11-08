"""Common test utilities, parsers, and assertions for Budapest Adventures E2E Test Suite.

Zero-dependency Python 3 module supporting both static filesystem inspection
and live HTTP preview server validation.
"""

import html.parser
import json
import os
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Approved active languages for internationalization (21 GSC traffic languages)
APPROVED_LANGUAGES = {
    "en", "hu", "ro", "ja", "it", "fr", "pl", "cs", "hr", "ru",
    "el", "bg", "es", "sr", "he", "pt", "sk", "tr", "uk", "de", "ko"
}

# Known pruned 9 dead GSC zombie languages (<90 clicks in 16 months)
PRUNED_LANGUAGES = {
    "ar", "da", "vi", "no", "sv", "fi", "th", "zh", "nl"
}

# Core money hubs mapping
CORE_HUBS = {
    "/": "index.html",
    "/best-budapest-river-cruises": "river.html",
    "/budapest-river-cruises": "river.html",
    "/budapest-dinner-cruises": "dinner.html",
    "/best-dinner-cruises-budapest": "dinner.html",
    "/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest": "candlelit-dinner-cruise.html",
    "/about": "about.html",
}

# Canonical domain
CANONICAL_DOMAIN = "https://www.budapestadventures.com"
VIP_LEGENDA_PARTNER_ID = "38585"
TYPO_LEGENDA_PARTNER_ID = "38885"
TOURCMS_AGENT_REF = "38585"
TIQETS_PARTNER_HANDLE = "budapestadventures"
META_PIXEL_ID = "1355732169631751"


class HTMLDocumentParser(html.parser.HTMLParser):
    """Zero-dependency HTML parser extracting elements, IDs, links, canonicals, and schemas."""

    def __init__(self):
        super().__init__()
        self.tags: List[Tuple[str, Dict[str, str]]] = []
        self.ids: List[str] = []
        self.duplicate_ids: List[str] = []
        self._seen_ids: Set[str] = set()
        self.links: List[str] = []
        self.canonical_url: Optional[str] = None
        self.scripts: List[Dict[str, str]] = []
        self.json_ld_schemas: List[Dict[str, Any]] = []
        self._in_script = False
        self._script_type = None
        self._script_content = []
        self.raw_text: List[str] = []

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]):
        attr_dict = {k.lower(): (v or "") for k, v in attrs}
        self.tags.append((tag.lower(), attr_dict))

        # ID extraction & duplicate tracking
        if "id" in attr_dict and attr_dict["id"]:
            element_id = attr_dict["id"]
            if element_id in self._seen_ids:
                self.duplicate_ids.append(element_id)
            self._seen_ids.add(element_id)
            self.ids.append(element_id)

        # Link extraction
        if tag.lower() == "a" and "href" in attr_dict:
            self.links.append(attr_dict["href"])

        # Canonical tag
        if tag.lower() == "link" and attr_dict.get("rel") == "canonical":
            self.canonical_url = attr_dict.get("href")

        # Script tracking
        if tag.lower() == "script":
            self._in_script = True
            self._script_type = attr_dict.get("type", "")
            self._script_content = []
            self.scripts.append(attr_dict)

    def handle_endtag(self, tag: str):
        if tag.lower() == "script" and self._in_script:
            self._in_script = False
            full_content = "".join(self._script_content).strip()
            if self._script_type == "application/ld+json" and full_content:
                try:
                    schema_obj = json.loads(full_content)
                    self.json_ld_schemas.append(schema_obj)
                except Exception:
                    pass

    def handle_data(self, data: str):
        if self._in_script:
            self._script_content.append(data)
        else:
            self.raw_text.append(data)


def parse_html(html_str: str) -> HTMLDocumentParser:
    """Parse HTML string and return populated parser."""
    parser = HTMLDocumentParser()
    parser.feed(html_str)
    return parser


def read_project_file(rel_path: str) -> Optional[str]:
    """Read a text file relative to PROJECT_ROOT."""
    target = PROJECT_ROOT / rel_path
    if not target.exists() or not target.is_file():
        return None
    try:
        return target.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None


def read_project_json(rel_path: str) -> Optional[Dict[str, Any]]:
    """Read and parse a JSON file relative to PROJECT_ROOT."""
    content = read_project_file(rel_path)
    if not content:
        return None
    try:
        return json.loads(content)
    except Exception:
        return None


class VercelConfigEvaluator:
    """Evaluates vercel.json routing, rewrites, redirects, and cleanUrls."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.redirects = config.get("redirects", [])
        self.rewrites = config.get("rewrites", [])
        self.clean_urls = config.get("cleanUrls", False)
        self.trailing_slash = config.get("trailingSlash", False)
        self.headers = config.get("headers", [])

    def resolve_redirect(self, path: str) -> Optional[Tuple[str, int]]:
        """Evaluate path against redirects rules, returning (destination, status_code)."""
        # Strip query string for path matching
        parsed = urllib.parse.urlsplit(path)
        clean_path = parsed.path
        query = parsed.query

        for rule in self.redirects:
            source_regex = rule.get("source")
            destination = rule.get("destination")
            permanent = rule.get("permanent", True)
            status_code = rule.get("statusCode", 301 if permanent else 307)

            if not source_regex or not destination:
                continue

            # Convert simple route pattern or regex
            # e.g., /da/:path* -> ^/da(?:/(.*))?$
            pattern = source_regex
            pattern = re.sub(r":([a-zA-Z0-9_]+)\(([^)]+)\)", r"(?P<\1>\2)", pattern)
            pattern = re.sub(r"/:([a-zA-Z0-9_]+)\*", r"(?:/(?P<\1>.*))?", pattern)
            pattern = re.sub(r":([a-zA-Z0-9_]+)\*", r"(?P<\1>.*)", pattern)
            pattern = re.sub(r":([a-zA-Z0-9_]+)", r"(?P<\1>[^/]+)", pattern)
            if not pattern.startswith("^"):
                pattern = f"^{pattern}"
            if not pattern.endswith("$"):
                pattern = f"{pattern}$"

            try:
                match = re.match(pattern, clean_path)
                if match:
                    dest = destination
                    for k, v in match.groupdict().items():
                        val_str = v or ""
                        dest = dest.replace(f":{k}*", val_str).replace(f":{k}", val_str)
                    if "://" not in dest:
                        dest = re.sub(r"/+", "/", dest)
                    # Preserve query string if destination doesn't specify one
                    if query and "?" not in dest:
                        dest = f"{dest}?{query}"
                    elif query and "?" in dest:
                        dest = f"{dest}&{query}"
                    return (dest, status_code)
            except re.error:
                continue

        return None

    def resolve_rewrite(self, path: str) -> Optional[str]:
        """Evaluate path against rewrites rules, returning destination file."""
        parsed = urllib.parse.urlsplit(path)
        clean_path = parsed.path

        for rule in self.rewrites:
            source = rule.get("source")
            destination = rule.get("destination")
            if not source or not destination:
                continue

            pattern = source
            pattern = re.sub(r":([a-zA-Z0-9_]+)\*", r"(?P<\1>.*)", pattern)
            pattern = re.sub(r":([a-zA-Z0-9_]+)", r"(?P<\1>[^/]+)", pattern)
            if not pattern.startswith("^"):
                pattern = f"^{pattern}"
            if not pattern.endswith("$"):
                pattern = f"{pattern}$"

            try:
                if re.match(pattern, clean_path):
                    return destination
            except re.error:
                continue

        return None


class TrackingAttributionSimulator:
    """Simulates client-side bpa-tracking.js behavior for attribution and URL decoration."""

    @staticmethod
    def extract_inbound_params(url: str) -> Dict[str, str]:
        parsed = urllib.parse.urlparse(url)
        params = urllib.parse.parse_qs(parsed.query)
        result = {}
        for key in ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "gclid", "fbclid", "_fbp"]:
            if key in params and params[key]:
                result[key] = params[key][0]
        return result

    @staticmethod
    def decorate_outbound_url(base_url: str, attribution: Dict[str, str]) -> str:
        """Decorates outbound link with appropriate partner code and subid/click IDs."""
        parsed = urllib.parse.urlparse(base_url)
        query = urllib.parse.parse_qs(parsed.query)

        host = parsed.netloc.lower()

        # Legenda decoration
        if "legenda.hu" in host:
            query["partner"] = [VIP_LEGENDA_PARTNER_ID]
            subid_parts = []
            if "gclid" in attribution:
                subid_parts.append(f"g_{attribution['gclid']}")
            if "fbclid" in attribution:
                subid_parts.append(f"f_{attribution['fbclid']}")
            if "utm_campaign" in attribution:
                subid_parts.append(f"c_{attribution['utm_campaign']}")
            if subid_parts:
                query["subid"] = ["_".join(subid_parts)]

        # TourCMS decoration
        elif "tourcms.com" in host or "budapestrivercruise.eu" in host:
            query["agent_ref"] = [TOURCMS_AGENT_REF]
            if "fbclid" in attribution:
                query["tc_fbclid"] = [attribution["fbclid"]]
            if "gclid" in attribution:
                query["tc_gclid"] = [attribution["gclid"]]
                query["tc_gclid_type"] = ["gclid"]
            if "_fbp" in attribution:
                query["_fbp"] = [attribution["_fbp"]]

        # Tiqets decoration
        elif "tiqets.com" in host:
            query["partner"] = [TIQETS_PARTNER_HANDLE]
            if "utm_campaign" in attribution:
                query["utm_campaign"] = [attribution["utm_campaign"]]

        new_query = urllib.parse.urlencode(query, doseq=True)
        return urllib.parse.urlunparse(parsed._replace(query=new_query))

    @staticmethod
    def calculate_commission(retail_eur: float, commission_rate: float = 0.25) -> float:
        """Calculates net commission value for Meta Pixel InitiateCheckout."""
        return round(retail_eur * commission_rate, 2)


class BaseTestCase:
    """Lightweight test case class with comprehensive assertion helpers."""

    def __init__(self, name: str):
        self.name = name

    def assert_true(self, condition: bool, msg: str = "Expected condition to be True"):
        if not condition:
            raise AssertionError(f"[{self.name}] {msg}")

    def assert_false(self, condition: bool, msg: str = "Expected condition to be False"):
        if condition:
            raise AssertionError(f"[{self.name}] {msg}")

    def assert_equal(self, actual: Any, expected: Any, msg: str = ""):
        if actual != expected:
            detail = f" Expected {expected!r}, got {actual!r}."
            raise AssertionError(f"[{self.name}] {msg}{detail}")

    def assert_in(self, member: Any, container: Any, msg: str = ""):
        if member not in container:
            container_repr = repr(container)[:100] + "..." if len(repr(container)) > 100 else repr(container)
            raise AssertionError(f"[{self.name}] {msg} Expected {member!r} to be in {container_repr}")

    def assert_not_in(self, member: Any, container: Any, msg: str = ""):
        if member in container:
            container_repr = repr(container)[:100] + "..." if len(repr(container)) > 100 else repr(container)
            raise AssertionError(f"[{self.name}] {msg} Expected {member!r} NOT to be in {container_repr}")

    def assert_clean_canonical(self, html_content: str, expected_canonical_path: str):
        """Assert canonical tag exists, points to canonical domain + path, and has 0 '#' fragments."""
        parser = parse_html(html_content)
        self.assert_true(
            parser.canonical_url is not None,
            f"Missing <link rel='canonical'> tag."
        )
        canonical = parser.canonical_url
        self.assert_false(
            "#" in canonical,
            f"Canonical tag contains forbidden '#' fragment: {canonical}"
        )
        expected_full = f"{CANONICAL_DOMAIN}{expected_canonical_path}".rstrip("/")
        clean_actual = canonical.rstrip("/")
        self.assert_equal(
            clean_actual,
            expected_full,
            f"Canonical tag mismatch."
        )

    def assert_no_digits_first_ids(self, html_content: str):
        """Assert no DOM element IDs start with a digit (e.g. '1-legenda')."""
        parser = parse_html(html_content)
        digits_first = [i for i in parser.ids if re.match(r"^[0-9]", i)]
        self.assert_equal(
            len(digits_first),
            0,
            f"Found invalid digits-first HTML5 IDs: {digits_first[:10]}"
        )

    def assert_no_duplicate_ids(self, html_content: str):
        """Assert no duplicate HTML IDs exist in DOM."""
        parser = parse_html(html_content)
        self.assert_equal(
            len(parser.duplicate_ids),
            0,
            f"Found duplicate DOM element IDs: {parser.duplicate_ids[:10]}"
        )

    def assert_no_ghost_links(self, html_content: str):
        """Assert no Relume boilerplate or empty '#' links exist."""
        parser = parse_html(html_content)
        ghost_relume = [l for l in parser.links if "library.relume.io" in l]
        empty_hashes = [l for l in parser.links if l == "#"]
        self.assert_equal(
            len(ghost_relume),
            0,
            f"Found ghost Relume boilerplate links: {ghost_relume[:5]}"
        )
        self.assert_equal(
            len(empty_hashes),
            0,
            f"Found {len(empty_hashes)} empty href='#' anchor links."
        )

    def assert_no_unicode_pollution(self, html_content: str):
        """Assert no zero-width joiners (\u200d) pollute the content."""
        zwj_count = html_content.count("\u200d")
        self.assert_equal(
            zwj_count,
            0,
            f"Found {zwj_count} zero-width joiners (\\u200d) in HTML content."
        )
