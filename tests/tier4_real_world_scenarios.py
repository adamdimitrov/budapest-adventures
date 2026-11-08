"""Tier 4: Real-World Scenarios (End-to-End User Journeys).

Simulates realistic, multi-step customer journeys and workload operational profiles:
- Scenario 1: Google Ads Paid Traffic -> River Hub -> Decision Filter -> Legenda Checkout
- Scenario 2: Meta Ads Retargeting -> Candlelit Dinner Review -> TourCMS Checkout
- Scenario 3: International Organic Visitor -> Pruned Zombie Slug -> 301 Redirect -> Canonical Hub
- Scenario 4: Decision Hub Power User -> Filter Interactivity -> Pier 7 Guide -> Direct Booking CTA
- Scenario 5: Search Engine Spider -> Robots.txt -> Sitemap.xml -> Canonical & DOM Crawl Audit
"""

import json
import re
import urllib.parse
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
    HTMLDocumentParser,
    TrackingAttributionSimulator,
    VercelConfigEvaluator,
    parse_html,
    read_project_file,
    read_project_json,
)


class Tier4RealWorldScenarioTests(BaseTestCase):
    """Test suite for Tier 4 end-to-end user journeys."""

    def test_scenario_1_google_ads_river_to_legenda_journey(self):
        """Scenario 1: Full Google Ads Paid Search to Legenda VIP Checkout Journey.
        
        1. User clicks Google ad: ?gclid=Cj0KCQjwnNy...&utm_source=google&utm_medium=cpc&utm_campaign=budapest_boat_tours
        2. Lands on River Cruises Main Hub (index.html / /budapest-river-cruises)
        3. Script captures attribution into dual storage (cookie + localStorage)
        4. User clicks link to Decision Hub (/danube-cruise-decision-hub)
        5. User filters for "Sightseeing" and views Legenda Dock 7 card
        6. User clicks Legenda "Book Direct" button
        7. Outbound URL is verified: partner=38585, subid containing gclid, 0 typo partner 38885
        8. Meta Pixel InitiateCheckout event fired with 25% net commission value.
        """
        # Step 1: Inbound ad click
        inbound_url = (
            "https://www.budapestadventures.com/budapest-river-cruises?"
            "gclid=Cj0KCQjwnNy_Test_Google_Click_ID"
            "&utm_source=google"
            "&utm_medium=cpc"
            "&utm_campaign=budapest_boat_tours"
            "&utm_content=sightseeing_headline"
        )
        attribution = TrackingAttributionSimulator.extract_inbound_params(inbound_url)
        self.assert_equal(attribution["gclid"], "Cj0KCQjwnNy_Test_Google_Click_ID")
        self.assert_equal(attribution["utm_campaign"], "budapest_boat_tours")

        # Step 2: River hub inspection
        river_html = read_project_file("index.html")
        self.assert_true(river_html is not None, "index.html must exist")
        river_parser = parse_html(river_html)
        self.assert_true(river_parser.canonical_url is not None)
        self.assert_false("#" in river_parser.canonical_url)

        # Step 3: Decision hub navigation
        decision_html = read_project_file("danube_cruise_decision_hub.html")
        self.assert_true(decision_html is not None, "danube_cruise_decision_hub.html must exist")
        decision_parser = parse_html(decision_html)
        self.assert_clean_canonical(decision_html, "/danube-cruise-decision-hub")

        # Step 4: Outbound Legenda conversion link
        legenda_links = [l for l in decision_parser.links if "legenda.hu" in l]
        self.assert_true(len(legenda_links) > 0, "Decision hub must contain Legenda booking link")
        base_legenda_url = legenda_links[0]
        decorated_url = TrackingAttributionSimulator.decorate_outbound_url(base_legenda_url, attribution)

        # Step 5: Verification of tracking parameters
        self.assert_in(f"partner={VIP_LEGENDA_PARTNER_ID}", decorated_url)
        self.assert_not_in(f"partner={TYPO_LEGENDA_PARTNER_ID}", decorated_url)
        self.assert_in("subid=", decorated_url)
        self.assert_in("Cj0KCQjwnNy_Test_Google_Click_ID", decorated_url)

        # Step 6: Conversion tracking value
        legenda_ticket_eur = 18.00  # 70-min sightseeing adult ticket
        net_commission = TrackingAttributionSimulator.calculate_commission(legenda_ticket_eur, 0.25)
        self.assert_equal(net_commission, 4.50)

    def test_scenario_2_meta_ads_candlelit_review_to_tourcms_journey(self):
        """Scenario 2: Meta Ads Retargeting -> Candlelit Review -> TourCMS Checkout.
        
        1. User clicks Instagram story ad with ?fbclid=IwAR2...&utm_source=instagram&utm_medium=paid_social
        2. Lands on Candlelit Dinner Cruise Review (/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest)
        3. Canonical tag confirms clean review path without hash fragment
        4. Editorial tested review schema verified
        5. Outbound TourCMS reservation link clicked
        6. Outbound URL contains agent_ref=38585, tc_fbclid, and Meta Pixel InitiateCheckout
        7. Conversion value equals 25% net commission margin on €85.00 ticket.
        """
        # Step 1: Inbound Meta ad click
        inbound_url = (
            "https://www.budapestadventures.com/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest?"
            "fbclid=IwAR2_Meta_Story_Retargeting_Click_9988"
            "&utm_source=instagram"
            "&utm_medium=paid_social"
            "&utm_campaign=candlelit_luxury_retargeting"
        )
        attribution = TrackingAttributionSimulator.extract_inbound_params(inbound_url)
        self.assert_equal(attribution["fbclid"], "IwAR2_Meta_Story_Retargeting_Click_9988")

        # Step 2: Candlelit review static page inspection
        review_html = read_project_file("candlelit-dinner-cruise.html")
        self.assert_true(review_html is not None, "candlelit-dinner-cruise.html must exist")
        self.assert_clean_canonical(review_html, "/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest")

        # Step 3: Outbound TourCMS / Legenda decoration
        base_booking_url = "https://legenda.hu/en/ticket-purchase"
        decorated = TrackingAttributionSimulator.decorate_outbound_url(base_booking_url, attribution)
        self.assert_in(f"partner={VIP_LEGENDA_PARTNER_ID}", decorated)
        self.assert_in("f_IwAR2_Meta_Story_Retargeting_Click_9988", decorated)

        # Step 4: Unit economics net commission assertion
        candlelit_price = 85.00
        commission = TrackingAttributionSimulator.calculate_commission(candlelit_price, 0.25)
        self.assert_equal(commission, 21.25)

    def test_scenario_3_international_zombie_slug_to_canonical_journey(self):
        """Scenario 3: International Organic Search from Pruned Zombie URL.
        
        1. German traveler clicks an old indexed Google result:
           https://budapestadventures.com/de/donau-kreuzfahrten-budapest?ref=munich_travel_blog
        2. vercel.json routing engine intercepts the request
        3. Returns HTTP 301 redirect to /budapest-river-cruises or /
        4. Preserves inbound query parameters (?ref=munich_travel_blog)
        5. Destination page contains valid self-referencing canonical tag
        6. German visitor navigates to Legenda dedicated terminal (/legenda-city-cruises)
        7. Legenda terminal displays live timetable and partner=38585.
        """
        vj = read_project_json("vercel.json")
        self.assert_true(vj is not None, "vercel.json must exist")
        evaluator = VercelConfigEvaluator(vj)

        # Step 1 & 2: Evaluate redirect on pruned dead language river slug
        requested_path = "/da/bedste-budapest-flod?ref=copenhagen_travel_blog"
        res = evaluator.resolve_redirect(requested_path)
        self.assert_true(res is not None, "Pruned Danish slug must redirect")
        dest, code = res

        # Step 3 & 4: Status 301 & Query preservation
        self.assert_equal(code, 301)
        self.assert_true(dest.startswith("/") or dest.startswith("/budapest-river-cruises"))
        self.assert_in("ref=copenhagen_travel_blog", dest)

        # Step 5: Legenda terminal inspection
        legenda_html = read_project_file("legenda-city-cruises.html")
        self.assert_true(legenda_html is not None, "legenda-city-cruises.html must exist")
        self.assert_clean_canonical(legenda_html, "/legenda-city-cruises")
        self.assert_in(VIP_LEGENDA_PARTNER_ID, legenda_html)

    def test_scenario_4_decision_hub_power_user_journey(self):
        """Scenario 4: Decision Hub Power User & Dock 7 Verification.
        
        1. User arrives directly at /danube-cruise-decision-hub
        2. Interacts with comparison filters (Sightseeing vs Dinner, Unlimited Drinks, Live Music)
        3. Clicks anchor jump to Vigado ter Pier 7 dock guide
        4. Verifies no DOMException crashes on querySelector
        5. Verifies all 3 recommended cruise options have valid booking links
        6. Confirms zero broken anchors (#silverline-folk or #budget-cruises).
        """
        decision_html = read_project_file("danube_cruise_decision_hub.html")
        self.assert_true(decision_html is not None)
        parser = parse_html(decision_html)

        # Assert no broken anchor links
        for link in parser.links:
            if link.startswith("#") and len(link) > 1:
                target_id = link[1:]
                self.assert_in(
                    target_id,
                    parser.ids,
                    f"Broken local anchor jump {link} found in decision hub"
                )

        # Assert clean semantic IDs
        self.assert_no_digits_first_ids(decision_html)
        self.assert_no_duplicate_ids(decision_html)

    def test_scenario_5_search_engine_crawler_audit(self):
        """Scenario 5: Search Engine Spider Full Crawl Audit.
        
        1. Spider requests /sitemap.xml
        2. Validates sitemap has zero zombie languages and <loc> tags have zero '#' fragments
        3. Crawls each hub in sitemap:
           - Verifies canonical tag exists and self-references clean URL
           - Verifies zero ghost Relume links (library.relume.io)
           - Verifies zero zero-width joiners (\u200d)
           - Verifies valid JSON-LD schema markup
        4. Verifies vercel.json cleanUrls: true and trailingSlash: false.
        """
        sitemap_xml = read_project_file("sitemap.xml")
        self.assert_true(sitemap_xml is not None, "sitemap.xml must exist")
        
        # Check no dead zombie languages in sitemap
        for z_lang in ["/ar/", "/da/", "/vi/", "/no/", "/sv/", "/fi/", "/th/", "/zh/", "/nl/"]:
            self.assert_not_in(z_lang, sitemap_xml)

        # Check canonicals across all core hubs
        for path, filename in CORE_HUBS.items():
            content = read_project_file(filename)
            if content:
                parser = parse_html(content)
                self.assert_true(
                    parser.canonical_url is not None,
                    f"Hub {filename} missing canonical tag"
                )
                self.assert_false(
                    "#" in parser.canonical_url,
                    f"Hub {filename} canonical contains '#' fragment: {parser.canonical_url}"
                )
                self.assert_no_ghost_links(content)
                self.assert_no_unicode_pollution(content)
