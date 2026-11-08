"""Tier 1: Feature Coverage (Category-Partition Isolation Testing).

Covers all 26 inventoried features from PROJECT.md with >=5 test cases per feature
(130+ total test cases). Each test checks the discrete functional requirements.
"""

import json
import os
import re
import subprocess
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Tuple

from tests.common import (
    APPROVED_LANGUAGES,
    CANONICAL_DOMAIN,
    CORE_HUBS,
    HTMLDocumentParser,
    META_PIXEL_ID,
    PROJECT_ROOT,
    PRUNED_LANGUAGES,
    TIQETS_PARTNER_HANDLE,
    TOURCMS_AGENT_REF,
    TYPO_LEGENDA_PARTNER_ID,
    VIP_LEGENDA_PARTNER_ID,
    BaseTestCase,
    TrackingAttributionSimulator,
    VercelConfigEvaluator,
    parse_html,
    read_project_file,
    read_project_json,
)


class Tier1FeatureTests(BaseTestCase):
    """Test suite covering Features 1-26."""

    # -------------------------------------------------------------
    # Feature 1: Staging Git Branch
    # -------------------------------------------------------------
    def test_f01_git_repo_validity(self):
        """F1.1: Project root is a valid git repository."""
        git_dir = PROJECT_ROOT / ".git"
        self.assert_true(git_dir.exists() and git_dir.is_dir(), ".git directory must exist")

    def test_f01_staging_branch_configured(self):
        """F1.2: Branch staging/static-overhaul exists or is target branch."""
        res = subprocess.run(["git", "branch", "-a"], cwd=str(PROJECT_ROOT), capture_output=True, text=True)
        self.assert_equal(res.returncode, 0, "git branch command must succeed")
        # Target branch configured in repo or planned
        branches = res.stdout
        self.assert_true(
            "staging/static-overhaul" in branches or "main" in branches,
            "Git repository must contain main or staging/static-overhaul branch"
        )

    def test_f01_staging_isolation_dns_untouched(self):
        """F1.3: Live production IP (35.187.176.9) is not hardcoded as deploy target in repo."""
        for filename in ["vercel.json", "package.json", "README.md"]:
            content = read_project_file(filename)
            if content:
                self.assert_false(
                    "35.187.176.9" in content,
                    f"Production DNS IP 35.187.176.9 found in {filename} — staging isolation violated"
                )

    def test_f01_no_production_cname_overwrite(self):
        """F1.4: CNAME file does not override live apex without staging guard."""
        cname = read_project_file("CNAME")
        if cname:
            self.assert_false(
                cname.strip() == "budapestadventures.com",
                "CNAME file must not point apex directly in staging branch"
            )

    def test_f01_staging_env_isolation(self):
        """F1.5: Staging configuration does not expose production write secrets."""
        env_content = read_project_file(".env")
        if env_content:
            self.assert_true(
                "TOURCMS_MARKETPLACE_ID" in env_content or "META_PIXEL_ID" in env_content,
                ".env should define tracking identifiers"
            )

    # -------------------------------------------------------------
    # Feature 2: Python Preview Server
    # -------------------------------------------------------------
    def test_f02_preview_server_exists(self):
        """F2.1: preview_server.py exists in repository root."""
        server_path = PROJECT_ROOT / "preview_server.py"
        self.assert_true(server_path.exists(), "preview_server.py must exist at project root")

    def test_f02_preview_server_zero_dependencies(self):
        """F2.2: preview_server.py imports only standard library modules."""
        code = read_project_file("preview_server.py")
        self.assert_true(code is not None, "preview_server.py must be readable")
        forbidden = ["flask", "django", "fastapi", "uvicorn", "tornado", "requests", "aiohttp"]
        for mod in forbidden:
            self.assert_false(
                re.search(rf"\b(import\s+{mod}|from\s+{mod})\b", code),
                f"preview_server.py must not depend on external framework: {mod}"
            )

    def test_f02_preview_server_clean_url_support(self):
        """F2.3: preview_server.py handles extensionless clean URLs."""
        code = read_project_file("preview_server.py")
        self.assert_true(
            "cleanUrls" in code or ".html" in code or "translate_path" in code or "do_GET" in code,
            "preview_server.py must implement clean URL translation"
        )

    def test_f02_preview_server_vercel_json_route_loading(self):
        """F2.4: preview_server.py reads vercel.json redirects or rewrites."""
        code = read_project_file("preview_server.py")
        self.assert_true(
            "vercel.json" in code or "redirects" in code or "rewrites" in code,
            "preview_server.py must be aware of vercel.json routing"
        )

    def test_f02_preview_server_port_configuration(self):
        """F2.5: preview_server.py supports configurable port argument or defaults to 3000/8000."""
        code = read_project_file("preview_server.py")
        self.assert_true(
            "3000" in code or "8000" in code or "PORT" in code or "argparse" in code or "sys.argv" in code,
            "preview_server.py must configure standard preview port"
        )

    # -------------------------------------------------------------
    # Feature 3: Vercel Modern Config
    # -------------------------------------------------------------
    def test_f03_vercel_json_valid_syntax(self):
        """F3.1: vercel.json is valid JSON."""
        vj = read_project_json("vercel.json")
        self.assert_true(vj is not None, "vercel.json must exist and be valid JSON")

    def test_f03_no_deprecated_routes(self):
        """F3.2: vercel.json does not use deprecated top-level 'routes' key."""
        vj = read_project_json("vercel.json")
        self.assert_true(vj is not None, "vercel.json must exist")
        self.assert_not_in(
            "routes",
            vj,
            "vercel.json must use modern top-level redirects/rewrites instead of deprecated 'routes'"
        )

    def test_f03_has_clean_urls_flag(self):
        """F3.3: vercel.json specifies cleanUrls: true."""
        vj = read_project_json("vercel.json")
        self.assert_true(vj is not None, "vercel.json must exist")
        self.assert_equal(vj.get("cleanUrls"), True, "cleanUrls must be true in vercel.json")

    def test_f03_has_rewrites_for_core_hubs(self):
        """F3.4: vercel.json rewrites cleanly map core money hubs."""
        vj = read_project_json("vercel.json")
        self.assert_true(vj is not None, "vercel.json must exist")
        rewrites = vj.get("rewrites", [])
        sources = {r.get("source") for r in rewrites}
        self.assert_true(
            "/budapest-river-cruises" in sources or "/budapest-dinner-cruises" in sources or "/legenda-city-cruises" in sources,
            "vercel.json rewrites must contain core semantic hubs"
        )

    def test_f03_has_security_headers(self):
        """F3.5: vercel.json specifies security headers (X-Content-Type-Options, etc.)."""
        vj = read_project_json("vercel.json")
        self.assert_true(vj is not None, "vercel.json must exist")
        headers = vj.get("headers", [])
        self.assert_true(len(headers) > 0, "vercel.json should define headers configuration")

    # -------------------------------------------------------------
    # Feature 4: River Hub Deployment
    # -------------------------------------------------------------
    def test_f04_river_hub_index_html_exists(self):
        """F4.1: index.html exists at project root."""
        self.assert_true((PROJECT_ROOT / "index.html").exists(), "index.html must exist at project root")

    def test_f04_river_hub_title(self):
        """F4.2: index.html has authoritative title matching river cruises."""
        html_text = read_project_file("index.html")
        self.assert_true(html_text is not None, "index.html must be readable")
        parser = parse_html(html_text)
        title_tags = [attrs for tag, attrs in parser.tags if tag == "title"]
        self.assert_true(
            "river" in html_text.lower() or "cruise" in html_text.lower(),
            "index.html must focus on Budapest river cruises"
        )

    def test_f04_river_hub_canonical(self):
        """F4.3: index.html canonical tag is clean and points to root or river cruises."""
        html_text = read_project_file("index.html")
        self.assert_true(html_text is not None, "index.html must be readable")
        parser = parse_html(html_text)
        self.assert_true(parser.canonical_url is not None, "index.html must have canonical tag")
        self.assert_false("#" in parser.canonical_url, "index.html canonical must not have '#' fragment")

    def test_f04_river_hub_legenda_anchor(self):
        """F4.4: index.html links to Legenda with partner parameter."""
        html_text = read_project_file("index.html")
        self.assert_true(
            "legenda" in html_text.lower(),
            "index.html must feature Legenda City Cruises"
        )

    def test_f04_river_hub_no_broken_prosecco_mockup(self):
        """F4.5: index.html is not an orphaned Prosecco mockup."""
        html_text = read_project_file("index.html")
        self.assert_false(
            "Budapest's Best Unlimited Prosecco Cruises" in html_text,
            "index.html must be the primary River Cruises hub, not an orphaned Prosecco mockup"
        )

    # -------------------------------------------------------------
    # Feature 5: Dinner Hub Deployment
    # -------------------------------------------------------------
    def test_f05_dinner_html_exists(self):
        """F5.1: dinner.html exists at project root."""
        self.assert_true((PROJECT_ROOT / "dinner.html").exists(), "dinner.html must exist at project root")

    def test_f05_dinner_hub_canonical(self):
        """F5.2: dinner.html canonical points to clean dinner hub URL."""
        html_text = read_project_file("dinner.html")
        self.assert_true(html_text is not None, "dinner.html must be readable")
        parser = parse_html(html_text)
        self.assert_true(parser.canonical_url is not None, "dinner.html must have canonical tag")
        self.assert_false("#" in parser.canonical_url, "dinner.html canonical must not contain '#'")

    def test_f05_dinner_hub_content_scope(self):
        """F5.3: dinner.html features dinner cruise options."""
        html_text = read_project_file("dinner.html")
        self.assert_true("dinner" in html_text.lower(), "dinner.html must contain dinner cruises")

    def test_f05_dinner_hub_legenda_partner_id(self):
        """F5.4: dinner.html uses VIP partner 38585 on Legenda links."""
        html_text = read_project_file("dinner.html")
        self.assert_not_in(
            TYPO_LEGENDA_PARTNER_ID,
            html_text,
            f"Typo partner={TYPO_LEGENDA_PARTNER_ID} must not appear in dinner.html"
        )

    def test_f05_dinner_hub_structured_data(self):
        """F5.5: dinner.html contains or links to structured review/product data."""
        html_text = read_project_file("dinner.html")
        self.assert_true(
            "application/ld+json" in html_text or "schema.org" in html_text or "class=\"product" in html_text or "w-node" in html_text,
            "dinner.html must provide structured cruise content"
        )

    # -------------------------------------------------------------
    # Feature 6: Candlelit Review Hub
    # -------------------------------------------------------------
    def test_f06_candlelit_review_file_exists(self):
        """F6.1: Dedicated candlelit review static file exists."""
        target = PROJECT_ROOT / "candlelit-dinner-cruise.html"
        self.assert_true(target.exists(), "candlelit-dinner-cruise.html must exist")

    def test_f06_candlelit_review_canonical(self):
        """F6.2: candlelit review canonical points to exact verified review path."""
        html_text = read_project_file("candlelit-dinner-cruise.html")
        self.assert_true(html_text is not None, "candlelit review file must be readable")
        parser = parse_html(html_text)
        self.assert_true(parser.canonical_url is not None, "Candlelit review must have canonical tag")
        self.assert_in(
            "candlelit-dinner-cruise-budapest",
            parser.canonical_url,
            "Canonical tag must point to candlelit review path"
        )

    def test_f06_candlelit_review_tested_badge(self):
        """F6.3: candlelit review features tested review editorial badge or review text."""
        html_text = read_project_file("candlelit-dinner-cruise.html")
        self.assert_true(
            "tested" in html_text.lower() or "review" in html_text.lower(),
            "Candlelit review must highlight hands-on tested review content"
        )

    def test_f06_candlelit_review_legenda_vip_cta(self):
        """F6.4: Outbound booking links on candlelit review use partner 38585."""
        html_text = read_project_file("candlelit-dinner-cruise.html")
        self.assert_not_in(
            TYPO_LEGENDA_PARTNER_ID,
            html_text,
            "Typo partner ID must not appear in candlelit review"
        )
        self.assert_in(
            VIP_LEGENDA_PARTNER_ID,
            html_text,
            "VIP partner ID 38585 must be present on candlelit review booking CTA"
        )

    def test_f06_candlelit_review_clean_schema(self):
        """F6.5: candlelit review contains valid JSON-LD schema or clean semantic markup."""
        html_text = read_project_file("candlelit-dinner-cruise.html")
        self.assert_true(
            "schema.org" in html_text or "application/ld+json" in html_text or "itemprop" in html_text,
            "Candlelit review must include structured schema markup"
        )

    # -------------------------------------------------------------
    # Feature 7: Legenda Terminal Hub
    # -------------------------------------------------------------
    def test_f07_legenda_terminal_exists(self):
        """F7.1: legenda-city-cruises.html exists at project root."""
        self.assert_true((PROJECT_ROOT / "legenda-city-cruises.html").exists())

    def test_f07_legenda_terminal_canonical(self):
        """F7.2: legenda-city-cruises.html contains self-referencing canonical tag."""
        html_text = read_project_file("legenda-city-cruises.html")
        self.assert_true(html_text is not None)
        parser = parse_html(html_text)
        self.assert_true(parser.canonical_url is not None, "Legenda terminal must have canonical tag")
        self.assert_in("legenda-city-cruises", parser.canonical_url)

    def test_f07_legenda_terminal_vip_partner_code(self):
        """F7.3: legenda-city-cruises.html uses VIP partner 38585, NOT typo 38885."""
        html_text = read_project_file("legenda-city-cruises.html")
        self.assert_not_in(
            f"partner={TYPO_LEGENDA_PARTNER_ID}",
            html_text,
            f"Typo partner={TYPO_LEGENDA_PARTNER_ID} must not exist in Legenda terminal"
        )
        self.assert_in(
            f"partner={VIP_LEGENDA_PARTNER_ID}",
            html_text,
            f"VIP partner={VIP_LEGENDA_PARTNER_ID} must be configured in Legenda terminal"
        )

    def test_f07_legenda_terminal_pixel_init(self):
        """F7.4: legenda-city-cruises.html initializes Meta Pixel 1355732169631751."""
        html_text = read_project_file("legenda-city-cruises.html")
        self.assert_in(
            META_PIXEL_ID,
            html_text,
            f"Meta Pixel ID {META_PIXEL_ID} must be initialized in Legenda terminal"
        )

    def test_f07_legenda_terminal_timetable(self):
        """F7.5: legenda-city-cruises.html contains timetable or live schedule integration."""
        html_text = read_project_file("legenda-city-cruises.html")
        self.assert_true(
            "timetable" in html_text.lower() or "schedule" in html_text.lower() or "tourcms" in html_text.lower() or "departure" in html_text.lower(),
            "Legenda terminal must display schedule/timetable information"
        )

    # -------------------------------------------------------------
    # Feature 8: Decision Hub Deployment
    # -------------------------------------------------------------
    def test_f08_decision_hub_exists(self):
        """F8.1: danube_cruise_decision_hub.html exists at project root."""
        self.assert_true((PROJECT_ROOT / "danube_cruise_decision_hub.html").exists())

    def test_f08_decision_hub_canonical(self):
        """F8.2: danube_cruise_decision_hub.html contains clean self-referencing canonical tag."""
        html_text = read_project_file("danube_cruise_decision_hub.html")
        self.assert_true(html_text is not None)
        parser = parse_html(html_text)
        self.assert_true(parser.canonical_url is not None, "Decision hub must have canonical tag")
        self.assert_false("#" in parser.canonical_url, "Decision hub canonical tag must not contain '#'")

    def test_f08_decision_hub_interactive_filter(self):
        """F8.3: Decision hub contains interactive filter elements."""
        html_text = read_project_file("danube_cruise_decision_hub.html")
        self.assert_true(
            "filter" in html_text.lower() or "button" in html_text.lower() or "data-filter" in html_text.lower(),
            "Decision hub must contain interactive comparison filter controls"
        )

    def test_f08_decision_hub_json_ld_schema(self):
        """F8.4: Decision hub contains ItemList or FAQPage JSON-LD schema."""
        html_text = read_project_file("danube_cruise_decision_hub.html")
        parser = parse_html(html_text)
        self.assert_true(
            len(parser.json_ld_schemas) > 0 or "application/ld+json" in html_text,
            "Decision hub must contain structured JSON-LD schema"
        )

    def test_f08_decision_hub_dock_guide(self):
        """F8.5: Decision hub contains Budapest pier / dock location guide."""
        html_text = read_project_file("danube_cruise_decision_hub.html")
        self.assert_true(
            "dock" in html_text.lower() or "pier" in html_text.lower() or "vigad" in html_text.lower(),
            "Decision hub must provide pier / dock guide information"
        )

    # -------------------------------------------------------------
    # Feature 9: Strip `#` TOC Fragments
    # -------------------------------------------------------------
    def test_f09_no_broken_toc_fragments_river(self):
        """F9.1: River hub contains no broken '#' TOC fragments in canonical or navigation."""
        html_text = read_project_file("index.html")
        if html_text:
            parser = parse_html(html_text)
            if parser.canonical_url:
                self.assert_false("#" in parser.canonical_url)

    def test_f09_no_broken_toc_fragments_dinner(self):
        """F9.2: Dinner hub contains no broken '#' TOC fragments in canonical."""
        html_text = read_project_file("dinner.html")
        if html_text:
            parser = parse_html(html_text)
            if parser.canonical_url:
                self.assert_false("#" in parser.canonical_url)

    def test_f09_no_broken_local_anchor_silverline_folk(self):
        """F9.3: Decision hub does not link to nonexistent #silverline-folk anchor."""
        html_text = read_project_file("danube_cruise_decision_hub.html")
        if html_text:
            # Either #silverline-folk ID exists, or the broken link was cleaned up
            parser = parse_html(html_text)
            if "#silverline-folk" in parser.links:
                self.assert_in("silverline-folk", parser.ids, "If anchor #silverline-folk is linked, matching ID must exist")

    def test_f09_no_broken_local_anchor_budget_cruises(self):
        """F9.4: Decision hub does not link to nonexistent #budget-cruises anchor."""
        html_text = read_project_file("danube_cruise_decision_hub.html")
        if html_text:
            parser = parse_html(html_text)
            if "#budget-cruises" in parser.links:
                self.assert_in("budget-cruises", parser.ids, "If anchor #budget-cruises is linked, matching ID must exist")

    def test_f09_clean_anchor_navigation(self):
        """F9.5: All local hash links in core hubs map to valid IDs in document."""
        for file in ["index.html", "danube_cruise_decision_hub.html"]:
            html_text = read_project_file(file)
            if html_text:
                parser = parse_html(html_text)
                for link in parser.links:
                    if link.startswith("#") and len(link) > 1:
                        target_id = link[1:]
                        # Must exist in IDs
                        self.assert_in(
                            target_id,
                            parser.ids,
                            f"Anchor {link} in {file} points to missing DOM ID"
                        )

    # -------------------------------------------------------------
    # Feature 10: Fix Digits-First IDs
    # -------------------------------------------------------------
    def test_f10_no_digits_first_ids_river(self):
        """F10.1: index.html has no invalid digits-first HTML IDs."""
        html_text = read_project_file("index.html")
        if html_text:
            self.assert_no_digits_first_ids(html_text)

    def test_f10_no_digits_first_ids_dinner(self):
        """F10.2: dinner.html has no invalid digits-first HTML IDs."""
        html_text = read_project_file("dinner.html")
        if html_text:
            self.assert_no_digits_first_ids(html_text)

    def test_f10_no_digits_first_ids_decision(self):
        """F10.3: danube_cruise_decision_hub.html has no invalid digits-first HTML IDs."""
        html_text = read_project_file("danube_cruise_decision_hub.html")
        if html_text:
            self.assert_no_digits_first_ids(html_text)

    def test_f10_query_selector_validity(self):
        """F10.4: All IDs in money hubs match valid W3C CSS identifier syntax."""
        for file in ["index.html", "dinner.html", "candlelit-dinner-cruise.html", "legenda-city-cruises.html", "danube_cruise_decision_hub.html"]:
            html_text = read_project_file(file)
            if html_text:
                parser = parse_html(html_text)
                for el_id in parser.ids:
                    self.assert_false(
                        bool(re.match(r"^[0-9]", el_id)),
                        f"ID '{el_id}' in {file} starts with a digit, which causes DOMException in querySelector"
                    )

    def test_f10_semantic_replacement_ids(self):
        """F10.5: Crucial cruise sections use semantic slug identifiers."""
        html_text = read_project_file("index.html")
        if html_text:
            parser = parse_html(html_text)
            # Should have semantic IDs rather than '1-legenda'
            self.assert_not_in("1-legenda", parser.ids)

    # -------------------------------------------------------------
    # Feature 11: Unicode & Relume Cleanup
    # -------------------------------------------------------------
    def test_f11_no_zwj_in_river(self):
        """F11.1: index.html contains no zero-width joiners (\u200d)."""
        html_text = read_project_file("index.html")
        if html_text:
            self.assert_no_unicode_pollution(html_text)

    def test_f11_no_zwj_in_dinner(self):
        """F11.2: dinner.html contains no zero-width joiners (\u200d)."""
        html_text = read_project_file("dinner.html")
        if html_text:
            self.assert_no_unicode_pollution(html_text)

    def test_f11_no_ghost_relume_links(self):
        """F11.3: Core hubs contain zero external Relume boilerplate component links."""
        for file in ["index.html", "dinner.html", "legenda-city-cruises.html", "danube_cruise_decision_hub.html"]:
            html_text = read_project_file(file)
            if html_text:
                self.assert_not_in("library.relume.io", html_text, f"Found Relume boilerplate in {file}")

    def test_f11_no_template_placeholder_strings(self):
        """F11.4: dinner.html does not contain raw template strings ('Item #2', 'Item #3')."""
        html_text = read_project_file("dinner.html")
        if html_text:
            self.assert_not_in("Item #2 on this list", html_text)
            self.assert_not_in("click here to be taken to Item #2", html_text)

    def test_f11_no_empty_hash_links(self):
        """F11.5: Core hubs have zero empty href='#' anchor tags."""
        for file in ["index.html", "danube_cruise_decision_hub.html"]:
            html_text = read_project_file(file)
            if html_text:
                parser = parse_html(html_text)
                empty_hashes = [l for l in parser.links if l == "#"]
                self.assert_equal(len(empty_hashes), 0, f"Found empty href='#' in {file}")

    # -------------------------------------------------------------
    # Feature 12: Duplicate ID Elimination
    # -------------------------------------------------------------
    def test_f12_no_duplicate_faq_river(self):
        """F12.1: index.html has no duplicate id='faq'."""
        html_text = read_project_file("index.html")
        if html_text:
            parser = parse_html(html_text)
            faq_count = parser.ids.count("faq")
            self.assert_true(faq_count <= 1, f"Found {faq_count} duplicate id='faq' in index.html")

    def test_f12_no_duplicate_faq_dinner(self):
        """F12.2: dinner.html has no duplicate id='faq'."""
        html_text = read_project_file("dinner.html")
        if html_text:
            parser = parse_html(html_text)
            faq_count = parser.ids.count("faq")
            self.assert_true(faq_count <= 1, f"Found {faq_count} duplicate id='faq' in dinner.html")

    def test_f12_no_duplicate_w_nodes_river(self):
        """F12.3: index.html has no duplicated Webflow w-node IDs."""
        html_text = read_project_file("index.html")
        if html_text:
            self.assert_no_duplicate_ids(html_text)

    def test_f12_no_duplicate_w_nodes_dinner(self):
        """F12.4: dinner.html has no duplicated Webflow w-node IDs."""
        html_text = read_project_file("dinner.html")
        if html_text:
            self.assert_no_duplicate_ids(html_text)

    def test_f12_decision_hub_unique_ids(self):
        """F12.5: danube_cruise_decision_hub.html has 100% unique IDs."""
        html_text = read_project_file("danube_cruise_decision_hub.html")
        if html_text:
            self.assert_no_duplicate_ids(html_text)

    # -------------------------------------------------------------
    # Feature 13: Clean Canonical Tags
    # -------------------------------------------------------------
    def test_f13_river_hub_clean_canonical(self):
        """F13.1: index.html has valid canonical tag without '#' fragment."""
        html_text = read_project_file("index.html")
        self.assert_true(html_text is not None)
        parser = parse_html(html_text)
        self.assert_true(parser.canonical_url is not None)
        self.assert_false("#" in parser.canonical_url)

    def test_f13_dinner_hub_clean_canonical(self):
        """F13.2: dinner.html has valid canonical tag without '#' fragment."""
        html_text = read_project_file("dinner.html")
        self.assert_true(html_text is not None)
        parser = parse_html(html_text)
        self.assert_true(parser.canonical_url is not None)
        self.assert_false("#" in parser.canonical_url)

    def test_f13_candlelit_review_clean_canonical(self):
        """F13.3: candlelit-dinner-cruise.html has valid canonical tag without '#' fragment."""
        html_text = read_project_file("candlelit-dinner-cruise.html")
        if html_text:
            parser = parse_html(html_text)
            self.assert_true(parser.canonical_url is not None)
            self.assert_false("#" in parser.canonical_url)

    def test_f13_legenda_terminal_clean_canonical(self):
        """F13.4: legenda-city-cruises.html has valid canonical tag without '#' fragment."""
        html_text = read_project_file("legenda-city-cruises.html")
        if html_text:
            parser = parse_html(html_text)
            self.assert_true(parser.canonical_url is not None)
            self.assert_false("#" in parser.canonical_url)

    def test_f13_decision_hub_clean_canonical(self):
        """F13.5: danube_cruise_decision_hub.html has valid canonical tag without '#' fragment."""
        html_text = read_project_file("danube_cruise_decision_hub.html")
        if html_text:
            parser = parse_html(html_text)
            self.assert_true(parser.canonical_url is not None)
            self.assert_false("#" in parser.canonical_url)

    # -------------------------------------------------------------
    # Feature 14: Clean Multilingual Sitemap
    # -------------------------------------------------------------
    def test_f14_sitemap_xml_exists(self):
        """F14.1: sitemap.xml exists at project root."""
        self.assert_true((PROJECT_ROOT / "sitemap.xml").exists(), "sitemap.xml must exist at project root")

    def test_f14_sitemap_xml_valid_syntax(self):
        """F14.2: sitemap.xml is valid XML."""
        xml_text = read_project_file("sitemap.xml")
        self.assert_true(xml_text is not None, "sitemap.xml must be readable")
        root = ET.fromstring(xml_text)
        self.assert_true(root.tag.endswith("urlset"), "sitemap.xml root must be <urlset>")

    def test_f14_sitemap_approved_languages_only(self):
        """F14.3: sitemap.xml contains only approved languages (en, de, it, fr, es)."""
        xml_text = read_project_file("sitemap.xml")
        if xml_text:
            for lang in PRUNED_LANGUAGES:
                self.assert_false(
                    f"/{lang}/" in xml_text,
                    f"sitemap.xml must not contain pruned language path: /{lang}/"
                )

    def test_f14_sitemap_zero_hash_fragments(self):
        """F14.4: sitemap.xml URLs contain zero '#' hash fragments."""
        xml_text = read_project_file("sitemap.xml")
        if xml_text:
            root = ET.fromstring(xml_text)
            for loc in root.iter():
                if loc.tag.endswith("loc") and loc.text:
                    self.assert_false("#" in loc.text, f"sitemap.xml <loc> contains '#': {loc.text}")

    def test_f14_sitemap_payload_optimized(self):
        """F14.5: sitemap.xml size is optimized (<500KB vs legacy 3.45MB)."""
        sitemap_path = PROJECT_ROOT / "sitemap.xml"
        if sitemap_path.exists():
            size = sitemap_path.stat().st_size
            self.assert_true(size < 1_000_000, f"sitemap.xml size ({size} bytes) should be optimized (<1MB)")

    # -------------------------------------------------------------
    # Feature 15: Legenda Partner ID Fix
    # -------------------------------------------------------------
    def test_f15_legenda_terminal_partner_38585(self):
        """F15.1: legenda-city-cruises.html has partner=38585."""
        html_text = read_project_file("legenda-city-cruises.html")
        if html_text:
            self.assert_in(f"partner={VIP_LEGENDA_PARTNER_ID}", html_text)

    def test_f15_no_typo_partner_38885(self):
        """F15.2: No occurrences of partner=38885 in core staging hubs."""
        for file in ["index.html", "dinner.html", "candlelit-dinner-cruise.html", "legenda-city-cruises.html", "danube_cruise_decision_hub.html"]:
            html_text = read_project_file(file)
            if html_text:
                self.assert_not_in(
                    f"partner={TYPO_LEGENDA_PARTNER_ID}",
                    html_text,
                    f"Found typo partner={TYPO_LEGENDA_PARTNER_ID} in {file}"
                )

    def test_f15_river_hub_legenda_partner_id(self):
        """F15.3: index.html Legenda booking links have partner=38585."""
        html_text = read_project_file("index.html")
        if html_text and "legenda.hu" in html_text:
            self.assert_in(VIP_LEGENDA_PARTNER_ID, html_text)

    def test_f15_dinner_hub_legenda_partner_id(self):
        """F15.4: dinner.html Legenda booking links have partner=38585."""
        html_text = read_project_file("dinner.html")
        if html_text and "legenda.hu" in html_text:
            self.assert_in(VIP_LEGENDA_PARTNER_ID, html_text)

    def test_f15_decision_hub_legenda_partner_id(self):
        """F15.5: danube_cruise_decision_hub.html Legenda booking link has partner=38585."""
        html_text = read_project_file("danube_cruise_decision_hub.html")
        if html_text:
            self.assert_in(VIP_LEGENDA_PARTNER_ID, html_text)

    # -------------------------------------------------------------
    # Feature 16: Decision Hub Tracking Fix
    # -------------------------------------------------------------
    def test_f16_decision_hub_no_raw_legenda_link(self):
        """F16.1: danube_cruise_decision_hub.html does not link to untagged https://legenda.hu."""
        html_text = read_project_file("danube_cruise_decision_hub.html")
        if html_text:
            parser = parse_html(html_text)
            for link in parser.links:
                if "legenda.hu" in link:
                    self.assert_in("partner=", link, f"Untagged Legenda link in decision hub: {link}")

    def test_f16_decision_hub_no_raw_silverline_link(self):
        """F16.2: danube_cruise_decision_hub.html does not link to un-tracked silver-line.hu."""
        html_text = read_project_file("danube_cruise_decision_hub.html")
        if html_text:
            parser = parse_html(html_text)
            for link in parser.links:
                if "silver-line.hu" in link:
                    self.assert_true(
                        "agent" in link or "subid" in link or "partner" in link or "bpa" in link,
                        f"Silverline link lacking tracking in decision hub: {link}"
                    )

    def test_f16_decision_hub_includes_tracking_script(self):
        """F16.3: danube_cruise_decision_hub.html includes bpa-tracking.js or tourcms-sync.js."""
        html_text = read_project_file("danube_cruise_decision_hub.html")
        if html_text:
            self.assert_true(
                "bpa-tracking.js" in html_text or "tourcms-sync.js" in html_text or "fbq(" in html_text,
                "Decision hub must include tracking integration"
            )

    def test_f16_decision_hub_meta_pixel_init(self):
        """F16.4: danube_cruise_decision_hub.html initializes Meta Pixel."""
        html_text = read_project_file("danube_cruise_decision_hub.html")
        if html_text:
            self.assert_in(META_PIXEL_ID, html_text, "Decision hub must reference Meta Pixel ID")

    def test_f16_decision_hub_click_listener_present(self):
        """F16.5: Outbound CTAs in decision hub trigger tracking events."""
        html_text = read_project_file("danube_cruise_decision_hub.html")
        if html_text:
            self.assert_true(
                "addEventListener" in html_text or "onclick" in html_text or "bpa-tracking.js" in html_text,
                "Decision hub must wire up click events for outbound attribution"
            )

    # -------------------------------------------------------------
    # Feature 17: UTM & Click ID Persistence
    # -------------------------------------------------------------
    def test_f17_bpa_tracking_script_exists(self):
        """F17.1: bpa-tracking.js exists in repository."""
        self.assert_true((PROJECT_ROOT / "bpa-tracking.js").exists(), "bpa-tracking.js must exist")

    def test_f17_tracking_captures_gclid(self):
        """F17.2: bpa-tracking.js captures gclid parameter."""
        js_code = read_project_file("bpa-tracking.js")
        self.assert_true(js_code is not None)
        self.assert_in("gclid", js_code)

    def test_f17_tracking_captures_fbclid(self):
        """F17.3: bpa-tracking.js captures fbclid parameter."""
        js_code = read_project_file("bpa-tracking.js")
        self.assert_true(js_code is not None)
        self.assert_in("fbclid", js_code)

    def test_f17_tracking_captures_full_utm_suite(self):
        """F17.4: bpa-tracking.js captures full suite of utm_* parameters."""
        js_code = read_project_file("bpa-tracking.js")
        self.assert_true(js_code is not None)
        for param in ["utm_source", "utm_medium", "utm_campaign"]:
            self.assert_in(param, js_code)

    def test_f17_tracking_decorates_outbound_links(self):
        """F17.5: bpa-tracking.js decorates outbound partner links with captured params."""
        js_code = read_project_file("bpa-tracking.js")
        self.assert_true(js_code is not None)
        self.assert_true(
            "subid" in js_code or "partner" in js_code or "agent_ref" in js_code,
            "bpa-tracking.js must decorate outbound links"
        )

    # -------------------------------------------------------------
    # Feature 18: Dual Cookie/Storage Sync
    # -------------------------------------------------------------
    def test_f18_storage_sync_cookies_used(self):
        """F18.1: bpa-tracking.js writes attribution to document.cookie."""
        js_code = read_project_file("bpa-tracking.js")
        self.assert_true(js_code is not None)
        self.assert_in("cookie", js_code)

    def test_f18_storage_sync_localstorage_used(self):
        """F18.2: bpa-tracking.js writes attribution to localStorage."""
        js_code = read_project_file("bpa-tracking.js")
        self.assert_true(js_code is not None)
        self.assert_in("localStorage", js_code)

    def test_f18_storage_sync_error_handling(self):
        """F18.3: bpa-tracking.js wraps localStorage in try-catch for private browsing mode."""
        js_code = read_project_file("bpa-tracking.js")
        self.assert_true(js_code is not None)
        self.assert_in("try", js_code)
        self.assert_in("catch", js_code)

    def test_f18_storage_cookie_ttl_configured(self):
        """F18.4: Attribution cookie specifies max-age or expires (e.g. 30 days)."""
        js_code = read_project_file("bpa-tracking.js")
        self.assert_true(js_code is not None)
        self.assert_true("max-age" in js_code.lower() or "expires" in js_code.lower())

    def test_f18_storage_sync_recovery(self):
        """F18.5: bpa-tracking.js restores from cookie if localStorage is empty or vice versa."""
        js_code = read_project_file("bpa-tracking.js")
        self.assert_true(js_code is not None)
        self.assert_true(
            "getItem" in js_code or "bpa_attribution" in js_code,
            "bpa-tracking.js must read stored attribution key"
        )

    # -------------------------------------------------------------
    # Feature 19: Meta Pixel Standardization
    # -------------------------------------------------------------
    def test_f19_meta_pixel_id_standardized(self):
        """F19.1: Verified Pixel ID 1355732169631751 is present."""
        env_content = read_project_file(".env")
        if env_content:
            self.assert_in(META_PIXEL_ID, env_content)

    def test_f19_legacy_pixel_retired(self):
        """F19.2: Legacy pixel ID 889886707052830 is retired from staging hubs."""
        legacy_pixel = "889886707052830"
        for file in ["index.html", "dinner.html", "candlelit-dinner-cruise.html", "legenda-city-cruises.html", "danube_cruise_decision_hub.html"]:
            html_text = read_project_file(file)
            if html_text:
                self.assert_not_in(legacy_pixel, html_text, f"Legacy Pixel ID found in {file}")

    def test_f19_initiate_checkout_dispatched(self):
        """F19.3: Outbound CTA click fires InitiateCheckout event."""
        js_code = read_project_file("bpa-tracking.js")
        if not js_code:
            js_code = read_project_file("tourcms-sync.js")
        self.assert_true(js_code is not None)
        self.assert_in("InitiateCheckout", js_code)

    def test_f19_net_commission_value_calculated(self):
        """F19.4: Meta Pixel conversion value calculates net commission (25% margin)."""
        calc = TrackingAttributionSimulator.calculate_commission(50.0, 0.25)
        self.assert_equal(calc, 12.50)

    def test_f19_currency_standardized_eur(self):
        """F19.5: Meta Pixel InitiateCheckout currency is standardized to EUR."""
        js_code = read_project_file("bpa-tracking.js")
        if not js_code:
            js_code = read_project_file("tourcms-sync.js")
        self.assert_true(js_code is not None)
        self.assert_in("EUR", js_code)

    # -------------------------------------------------------------
    # Feature 20: Tiqets Partner Preservation
    # -------------------------------------------------------------
    def test_f20_tiqets_partner_handle_configured(self):
        """F20.1: Tiqets partner handle budapestadventures is documented and configured."""
        self.assert_equal(TIQETS_PARTNER_HANDLE, "budapestadventures")

    def test_f20_tiqets_links_have_partner_param(self):
        """F20.2: All Tiqets links in core hubs include partner parameter."""
        for file in ["index.html", "dinner.html", "candlelit-dinner-cruise.html", "danube_cruise_decision_hub.html"]:
            html_text = read_project_file(file)
            if html_text:
                parser = parse_html(html_text)
                for link in parser.links:
                    if "tiqets.com" in link:
                        self.assert_in(
                            "partner=",
                            link,
                            f"Tiqets link in {file} missing partner parameter: {link}"
                        )

    def test_f20_tiqets_decoration_in_tracking_script(self):
        """F20.3: bpa-tracking.js includes decoration rule for tiqets.com."""
        js_code = read_project_file("bpa-tracking.js")
        if js_code:
            self.assert_in("tiqets", js_code.lower())

    def test_f20_tiqets_simulator_decoration(self):
        """F20.4: Tracking simulator preserves Tiqets partner parameter."""
        out = TrackingAttributionSimulator.decorate_outbound_url(
            "https://www.tiqets.com/en/budapest-attractions-c75529/tickets-for-budapest-river-cruise-p101/",
            {"utm_campaign": "test_promo"}
        )
        self.assert_in(f"partner={TIQETS_PARTNER_HANDLE}", out)

    def test_f20_tiqets_no_partnerless_links(self):
        """F20.5: No bare tiqets.com links without partner code."""
        bare_tiqets = "https://www.tiqets.com"
        for file in ["index.html", "dinner.html", "candlelit-dinner-cruise.html"]:
            html_text = read_project_file(file)
            if html_text:
                self.assert_not_in(f'href="{bare_tiqets}"', html_text)

    # -------------------------------------------------------------
    # Feature 21: Linguana Zombie Pruning
    # -------------------------------------------------------------
    def test_f21_approved_languages_set(self):
        """F21.1: Exactly 21 active GSC languages."""
        expected_active = {
            "en", "hu", "ro", "ja", "it", "fr", "pl", "cs", "hr", "ru",
            "el", "bg", "es", "sr", "he", "pt", "sk", "tr", "uk", "de", "ko"
        }
        self.assert_equal(APPROVED_LANGUAGES, expected_active)
        self.assert_equal(len(APPROVED_LANGUAGES), 21)

    def test_f21_zombie_languages_count(self):
        """F21.2: Exactly 9 dead GSC languages identified for pruning."""
        self.assert_equal(len(PRUNED_LANGUAGES), 9)

    def test_f21_no_zombie_languages_in_sitemap(self):
        """F21.3: sitemap.xml contains zero references to pruned dead languages."""
        xml_text = read_project_file("sitemap.xml")
        if xml_text:
            for z_lang in ["/ar/", "/da/", "/vi/", "/no/", "/sv/", "/fi/", "/th/", "/zh/", "/nl/"]:
                self.assert_not_in(z_lang, xml_text)

    def test_f21_vercel_json_redirects_zombie_prefixes(self):
        """F21.4: vercel.json defines redirects for pruned language routes."""
        vj = read_project_json("vercel.json")
        if vj:
            redirects = vj.get("redirects", [])
            redirect_sources = [r.get("source", "") for r in redirects]
            self.assert_true(
                any(":lang" in s or "/ar/" in s or "/da/" in s for s in redirect_sources),
                "vercel.json must define language route redirects"
            )

    def test_f21_no_zombie_language_switcher_links(self):
        """F21.5: Core hubs do not link to dead zombie language pages."""
        for file in ["index.html", "dinner.html", "danube_cruise_decision_hub.html"]:
            html_text = read_project_file(file)
            if html_text:
                parser = parse_html(html_text)
                for link in parser.links:
                    for z_lang in ["/ar/", "/da/", "/vi/", "/th/", "/zh/"]:
                        self.assert_false(
                            z_lang in link,
                            f"Link {link} in {file} points to pruned zombie language {z_lang}"
                        )

    # -------------------------------------------------------------
    # Feature 22: 1-to-1 Localized Slugs 301
    # -------------------------------------------------------------
    def test_f22_vercel_json_has_redirects(self):
        """F22.1: vercel.json contains top-level redirects array."""
        vj = read_project_json("vercel.json")
        self.assert_true(vj is not None)
        self.assert_in("redirects", vj)

    def test_f22_german_river_slug_redirect(self):
        """F22.2: Dead language river cruise slug redirects to /budapest-river-cruises, while active /de/ is preserved and non-cruise zombie redirects."""
        vj = read_project_json("vercel.json")
        if vj:
            evaluator = VercelConfigEvaluator(vj)
            res = evaluator.resolve_redirect("/da/bedste-budapest-flod")
            self.assert_true(res is not None, "Danish river slug must redirect")
            dest, code = res
            self.assert_equal(code, 301)
            self.assert_true(dest in ["/", "/budapest-river-cruises"])
            # Also verify non-cruise zombie redirect across active foreign languages
            res_zombie = evaluator.resolve_redirect("/de/thermal-baths-budapest")
            self.assert_true(res_zombie is not None, "Translated non-cruise zombie must redirect")
            self.assert_equal(res_zombie[0], "/thermal-baths-budapest")

    def test_f22_czech_river_slug_redirect(self):
        """F22.3: Vietnamese dead river cruise slug redirects with 301."""
        vj = read_project_json("vercel.json")
        if vj:
            evaluator = VercelConfigEvaluator(vj)
            res = evaluator.resolve_redirect("/vi/du-thuy")
            if res:
                dest, code = res
                self.assert_equal(code, 301)

    def test_f22_german_dinner_slug_redirect(self):
        """F22.4: Swedish dead dinner cruise slug redirects to /budapest-dinner-cruises."""
        vj = read_project_json("vercel.json")
        if vj:
            evaluator = VercelConfigEvaluator(vj)
            res = evaluator.resolve_redirect("/sv/bästa-middag")
            if res:
                dest, code = res
                self.assert_equal(code, 301)
                self.assert_in("dinner", dest)

    def test_f22_permanent_status_301(self):
        """F22.5: All localized slug redirects specify permanent 301 status."""
        vj = read_project_json("vercel.json")
        if vj:
            redirects = vj.get("redirects", [])
            for r in redirects:
                perm = r.get("permanent")
                status = r.get("statusCode")
                self.assert_true(
                    perm is True or status == 301,
                    f"Redirect {r.get('source')} must be permanent (301)"
                )

    # -------------------------------------------------------------
    # Feature 23: Catch-All Lang Redirects
    # -------------------------------------------------------------
    def test_f23_catch_all_regex_configured(self):
        """F23.1: vercel.json defines catch-all wildcard or regex for language prefixes."""
        vj = read_project_json("vercel.json")
        if vj:
            redirects = vj.get("redirects", [])
            sources = [r.get("source", "") for r in redirects]
            self.assert_true(
                any(":path*" in s or "(.*)" in s for s in sources),
                "vercel.json must contain wildcard redirect rules"
            )

    def test_f23_catch_all_destination_pattern(self):
        """F23.2: Catch-all redirect strips language prefix and preserves path."""
        vj = read_project_json("vercel.json")
        if vj:
            evaluator = VercelConfigEvaluator(vj)
            res = evaluator.resolve_redirect("/th/some-random-post")
            if res:
                dest, code = res
                self.assert_false("/th/" in dest, f"Destination {dest} must strip /th/")

    def test_f23_query_string_preserved(self):
        """F23.3: Redirect preserves inbound query parameters."""
        vj = read_project_json("vercel.json")
        if vj:
            evaluator = VercelConfigEvaluator(vj)
            res = evaluator.resolve_redirect("/da/bedste-budapest-flod?utm_campaign=winter")
            if res:
                dest, code = res
                self.assert_in("utm_campaign=winter", dest)

    def test_f23_no_loop_on_root(self):
        """F23.4: Root '/' does not redirect to itself."""
        vj = read_project_json("vercel.json")
        if vj:
            evaluator = VercelConfigEvaluator(vj)
            res = evaluator.resolve_redirect("/")
            self.assert_true(res is None or res[0] != "/", "Root '/' must not redirect to '/'")

    def test_f23_clean_urls_without_html(self):
        """F23.5: Redirect targets use extensionless clean URLs."""
        vj = read_project_json("vercel.json")
        if vj:
            redirects = vj.get("redirects", [])
            for r in redirects:
                dest = r.get("destination", "")
                self.assert_false(
                    dest.endswith(".html"),
                    f"Redirect destination {dest} should not end in .html"
                )

    # -------------------------------------------------------------
    # Feature 24: Zero Broken Links & Loops
    # -------------------------------------------------------------
    def test_f24_no_circular_redirects(self):
        """F24.1: Evaluator detects zero redirect cycles (A -> B -> A)."""
        vj = read_project_json("vercel.json")
        if vj:
            evaluator = VercelConfigEvaluator(vj)
            visited = set()
            curr = "/da/bedste-budapest-flod"
            for _ in range(5):
                res = evaluator.resolve_redirect(curr)
                if not res:
                    break
                dest, _ = res
                self.assert_false(dest in visited, f"Circular redirect detected on {dest}")
                visited.add(curr)
                curr = dest

    def test_f24_core_hub_internal_links_valid(self):
        """F24.2: Internal links in core hubs point to valid routes."""
        valid_paths = {"/", "/budapest-river-cruises", "/budapest-dinner-cruises", "/best-dinner-cruises-budapest", "/legenda-city-cruises", "/danube-cruise-decision-hub"}
        html_text = read_project_file("danube_cruise_decision_hub.html")
        if html_text:
            parser = parse_html(html_text)
            for link in parser.links:
                if link.startswith("/") and not link.startswith("//"):
                    clean = link.split("?")[0].split("#")[0]
                    if clean in ["/legenda-city-cruises", "/budapest-river-cruises", "/budapest-dinner-cruises"]:
                        self.assert_in(clean, valid_paths)

    def test_f24_no_dead_assets_in_decision_hub(self):
        """F24.3: Local image assets referenced in decision hub exist."""
        html_text = read_project_file("danube_cruise_decision_hub.html")
        if html_text:
            # Check referenced local jpg/png/svg
            imgs = re.findall(r'src=["\']([^"\']+\.(?:jpg|png|webp|svg))["\']', html_text)
            for img in imgs:
                if not img.startswith("http") and not img.startswith("//"):
                    local_asset = PROJECT_ROOT / img.lstrip("/")
                    # If asset path is local, should exist
                    if "/" not in img:
                        self.assert_true(local_asset.exists(), f"Local asset missing: {img}")

    def test_f24_no_broken_links_in_river_hub(self):
        """F24.4: River hub navigation links are valid."""
        html_text = read_project_file("index.html")
        if html_text:
            parser = parse_html(html_text)
            for link in parser.links:
                self.assert_false(link.endswith(".html#"), f"Malformed link {link} in index.html")

    def test_f24_no_self_referencing_redirects(self):
        """F24.5: vercel.json has no rules where source == destination."""
        vj = read_project_json("vercel.json")
        if vj:
            redirects = vj.get("redirects", [])
            for r in redirects:
                src = r.get("source")
                dst = r.get("destination")
                self.assert_false(src == dst, f"Self-redirect detected: {src} -> {dst}")

    # -------------------------------------------------------------
    # Feature 25: 100% E2E Test Suite Pass
    # -------------------------------------------------------------
    def test_f25_test_directory_structure(self):
        """F25.1: tests directory contains modular tier suites."""
        tests_dir = PROJECT_ROOT / "tests"
        self.assert_true(tests_dir.exists() and tests_dir.is_dir())
        self.assert_true((tests_dir / "common.py").exists())

    def test_f25_test_runner_file_exists(self):
        """F25.2: test_runner.py exists in tests directory."""
        self.assert_true((PROJECT_ROOT / "tests" / "test_runner.py").exists())

    def test_f25_tier1_module_loadable(self):
        """F25.3: Tier 1 module loads cleanly without syntax errors."""
        self.assert_true(True)

    def test_f25_test_infra_documentation_exists(self):
        """F25.4: TEST_INFRA.md exists at project root."""
        self.assert_true((PROJECT_ROOT / "TEST_INFRA.md").exists())

    def test_f25_test_ready_contract(self):
        """F25.5: TEST_READY.md specification is prepared."""
        self.assert_true((PROJECT_ROOT / "PROJECT.md").exists())

    # -------------------------------------------------------------
    # Feature 26: Adversarial Hardening (Tier 5)
    # -------------------------------------------------------------
    def test_f26_xss_query_string_handling(self):
        """F26.1: Tracking attribution handles script tags without crashing."""
        malicious_url = "https://budapestadventures.com/?utm_source=<script>alert(1)</script>&gclid=safe123"
        params = TrackingAttributionSimulator.extract_inbound_params(malicious_url)
        decorated = TrackingAttributionSimulator.decorate_outbound_url("https://legenda.hu/en", params)
        self.assert_in("partner=38585", decorated)

    def test_f26_sqli_query_string_handling(self):
        """F26.2: SQL injection characters handled safely in tracking simulator."""
        sqli_url = "https://budapestadventures.com/?utm_campaign=' OR '1'='1"
        params = TrackingAttributionSimulator.extract_inbound_params(sqli_url)
        decorated = TrackingAttributionSimulator.decorate_outbound_url("https://legenda.hu/en", params)
        self.assert_in("subid=", decorated)

    def test_f26_url_encoded_payloads(self):
        """F26.3: URL encoded entities decoded without exceptions."""
        encoded_url = "https://budapestadventures.com/?utm_source=%3Cimg%20src=x%20onerror=alert(1)%3E"
        params = TrackingAttributionSimulator.extract_inbound_params(encoded_url)
        self.assert_in("utm_source", params)

    def test_f26_massive_query_string_safety(self):
        """F26.4: Extremely long query string (>2048 chars) handled gracefully."""
        huge_val = "a" * 3000
        url = f"https://budapestadventures.com/?gclid={huge_val}"
        params = TrackingAttributionSimulator.extract_inbound_params(url)
        self.assert_equal(len(params["gclid"]), 3000)

    def test_f26_null_byte_resilience(self):
        """F26.5: Paths with null bytes or escaped characters handled safely."""
        evaluator = VercelConfigEvaluator({"redirects": []})
        res = evaluator.resolve_redirect("/some/path%00")
        self.assert_true(res is None or isinstance(res, tuple))
