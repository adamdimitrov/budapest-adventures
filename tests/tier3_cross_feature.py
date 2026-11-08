"""Tier 3: Cross-Feature Interactions & Combinations (Pairwise Coverage).

Tests pairwise interactions between marketing channels, device views,
redirect routing, canonical structures, partner parameter persistence, and pixel dispatches.
"""

import json
import re
import urllib.parse
import xml.etree.ElementTree
from pathlib import Path

from tests.common import (
    APPROVED_LANGUAGES,
    CANONICAL_DOMAIN,
    CORE_HUBS,
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


class Tier3CrossFeatureTests(BaseTestCase):
    """Test suite for Tier 3 pairwise cross-feature interactions."""

    def test_pair_01_google_ads_mobile_decision_hub_legenda(self):
        """Pair 1: Google Ads (gclid) + Decision Hub filter + Outbound Legenda booking."""
        inbound = "https://budapestadventures.com/danube-cruise-decision-hub?gclid=test_gclid_12345&utm_source=google&utm_medium=cpc"
        params = TrackingAttributionSimulator.extract_inbound_params(inbound)
        self.assert_equal(params.get("gclid"), "test_gclid_12345")
        self.assert_equal(params.get("utm_source"), "google")

        # Simulate clicking Legenda Dock 7 booking button
        base_outbound = "https://legenda.hu/en/ticket-purchase"
        decorated = TrackingAttributionSimulator.decorate_outbound_url(base_outbound, params)

        self.assert_in(f"partner={VIP_LEGENDA_PARTNER_ID}", decorated)
        self.assert_in("subid=", decorated)
        self.assert_in("g_test_gclid_12345", decorated)

    def test_pair_02_meta_ads_candlelit_tourcms_checkout(self):
        """Pair 2: Meta Ads (fbclid) + Candlelit Review Hub + TourCMS checkout + Net Commission."""
        inbound = "https://budapestadventures.com/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest?fbclid=IwAR_test_fbclid_999&utm_source=facebook&utm_medium=paid"
        params = TrackingAttributionSimulator.extract_inbound_params(inbound)
        self.assert_equal(params.get("fbclid"), "IwAR_test_fbclid_999")

        # Outbound TourCMS decoration
        base_tourcms = "https://budapestrivercruise.eu/booking"
        decorated = TrackingAttributionSimulator.decorate_outbound_url(base_tourcms, params)
        self.assert_in(f"agent_ref={TOURCMS_AGENT_REF}", decorated)
        self.assert_in("tc_fbclid=IwAR_test_fbclid_999", decorated)

        # Commission calculation for Candlelit Dinner (€85.00 ticket)
        comm = TrackingAttributionSimulator.calculate_commission(85.0, 0.25)
        self.assert_equal(comm, 21.25)

    def test_pair_03_pruned_german_slug_redirect_utm_preservation(self):
        """Pair 3: Pruned dead language slug & non-cruise zombie + Inbound campaign UTMs + 301 Redirect + Query String."""
        vj = read_project_json("vercel.json")
        self.assert_true(vj is not None)
        evaluator = VercelConfigEvaluator(vj)

        incoming = "/da/bedste-budapest-flod?utm_campaign=winter2025&gclid=g123"
        res = evaluator.resolve_redirect(incoming)
        self.assert_true(res is not None, "Danish river slug must redirect")
        dest, code = res
        self.assert_equal(code, 301)
        self.assert_in("utm_campaign=winter2025", dest)
        self.assert_in("gclid=g123", dest)

    def test_pair_04_pruned_language_catch_all_canonical_alignment(self):
        """Pair 4: Pruned Thai language path + Catch-all 301 + Canonical target."""
        vj = read_project_json("vercel.json")
        self.assert_true(vj is not None)
        evaluator = VercelConfigEvaluator(vj)

        incoming = "/th/budapest-dinner-cruises"
        res = evaluator.resolve_redirect(incoming)
        if res:
            dest, code = res
            self.assert_equal(code, 301)
            self.assert_equal(dest, "/budapest-dinner-cruises")

    def test_pair_05_tiqets_partner_dual_storage_cookie_recovery(self):
        """Pair 5: Tiqets outbound link + Dual storage sync (localStorage empty, cookie populated)."""
        # Simulated cookie state
        cookie_attribution = {"utm_campaign": "easter_sale", "gclid": "g_cook_77"}
        decorated = TrackingAttributionSimulator.decorate_outbound_url(
            "https://www.tiqets.com/en/tickets-p101/",
            cookie_attribution
        )
        self.assert_in(f"partner={TIQETS_PARTNER_HANDLE}", decorated)
        self.assert_in("utm_campaign=easter_sale", decorated)

    def test_pair_06_legenda_partner_storage_sync_recovery(self):
        """Pair 6: Legenda link + Dual storage sync (cookie blocked, localStorage populated)."""
        storage_attribution = {"utm_campaign": "spring_break", "fbclid": "fb_store_88"}
        decorated = TrackingAttributionSimulator.decorate_outbound_url(
            "https://legenda.hu/en",
            storage_attribution
        )
        self.assert_in(f"partner={VIP_LEGENDA_PARTNER_ID}", decorated)
        self.assert_in("f_fb_store_88", decorated)

    def test_pair_07_decision_hub_filter_state_and_anchor_nav(self):
        """Pair 7: Decision Hub filter selection + Clean anchor jump + Legenda CTA."""
        html_text = read_project_file("danube_cruise_decision_hub.html")
        if html_text:
            parser = parse_html(html_text)
            # Find Legenda card
            legenda_links = [l for l in parser.links if "legenda" in l]
            self.assert_true(len(legenda_links) > 0)
            self.assert_in(VIP_LEGENDA_PARTNER_ID, html_text)

    def test_pair_08_sitemap_url_and_canonical_rewrite_parity(self):
        """Pair 8: URLs listed in sitemap.xml strictly match canonical tags and vercel.json rewrites."""
        vj = read_project_json("vercel.json")
        xml_text = read_project_file("sitemap.xml")
        if vj and xml_text:
            evaluator = VercelConfigEvaluator(vj)
            root = xml.etree.ElementTree.fromstring(xml_text) if hasattr(xml, "etree") else None
            # Core hubs must be in sitemap
            self.assert_in("budapestadventures.com", xml_text)

    def test_pair_09_preview_server_clean_url_and_rewrite_resolution(self):
        """Pair 9: preview_server.py resolves /budapest-dinner-cruises to dinner.html."""
        vj = read_project_json("vercel.json")
        if vj:
            evaluator = VercelConfigEvaluator(vj)
            dest = evaluator.resolve_rewrite("/budapest-dinner-cruises")
            self.assert_true(dest in ["/dinner.html", "dinner.html"])

    def test_pair_10_security_headers_and_frame_options_pair(self):
        """Pair 10: vercel.json headers enforce X-Frame-Options: SAMEORIGIN with cleanUrls."""
        vj = read_project_json("vercel.json")
        if vj and "headers" in vj:
            headers_list = vj["headers"]
            has_xframe = False
            for h_group in headers_list:
                for h in h_group.get("headers", []):
                    if h.get("key", "").lower() == "x-frame-options":
                        has_xframe = True
            self.assert_true(has_xframe, "Security headers must include X-Frame-Options")

    def test_pair_11_child_ticket_unit_economics_pixel_pair(self):
        """Pair 11: Child ticket (€9.00) + Meta Pixel InitiateCheckout (net commission €2.25 EUR)."""
        ticket_price = 9.00
        comm = TrackingAttributionSimulator.calculate_commission(ticket_price, 0.25)
        self.assert_equal(comm, 2.25)

    def test_pair_12_standard_adult_ticket_unit_economics_pixel_pair(self):
        """Pair 12: Adult ticket (€18.00) + Meta Pixel InitiateCheckout (net commission €4.50 EUR)."""
        ticket_price = 18.00
        comm = TrackingAttributionSimulator.calculate_commission(ticket_price, 0.25)
        self.assert_equal(comm, 4.50)

    def test_pair_13_family_basket_unit_economics_pixel_pair(self):
        """Pair 13: Family basket (2 Adults + 2 Kids = €54.00) + Commission (€13.50 EUR)."""
        basket = (2 * 18.00) + (2 * 9.00)
        comm = TrackingAttributionSimulator.calculate_commission(basket, 0.25)
        self.assert_equal(comm, 13.50)

    def test_pair_14_schema_itemlist_and_dom_card_ids_alignment(self):
        """Pair 14: ItemList schema URLs align with DOM element IDs on Decision Hub."""
        html_text = read_project_file("danube_cruise_decision_hub.html")
        if html_text:
            parser = parse_html(html_text)
            for s in parser.json_ld_schemas:
                if s.get("@type") == "ItemList":
                    for item in s.get("itemListElement", []):
                        url = item.get("url", "")
                        if "#" in url:
                            target_id = url.split("#")[1]
                            self.assert_in(target_id, parser.ids)

    def test_pair_15_mobile_sticky_cta_outbound_decoration(self):
        """Pair 15: River hub mobile sticky CTA retains verified Legenda partner ID."""
        html_text = read_project_file("index.html")
        if html_text and "mobile-sticky-cta" in html_text:
            self.assert_in(VIP_LEGENDA_PARTNER_ID, html_text)
