#!/usr/bin/env python3
"""
Apply full QC & structural parity to Budapest Adventures flagship guides:
- /Users/adamdimitrov/Development/budapest-adventures/river.html
- /Users/adamdimitrov/Development/budapest-adventures/river-ecom.html (synced 1:1 with river.html)
- /Users/adamdimitrov/Development/budapest-adventures/dinner.html

Parity benchmark:
- /Users/adamdimitrov/Development/luxurytraveltester/best-desert-safaris-dubai/index.html
- /Users/adamdimitrov/Development/luxurytraveltester/apply_full_qc_parity.py
"""

import shutil
import subprocess
import sys
from pathlib import Path
from bs4 import BeautifulSoup

sys.path.insert(0, "/Users/adamdimitrov/Development/budapest-adventures")
from apply_luxury_editorial_design import (
    build_river_deck_and_sticky,
    build_dinner_deck_and_sticky,
    upgrade_river_file,
    upgrade_dinner_file,
)

RIVER_PATH = "/Users/adamdimitrov/Development/budapest-adventures/river.html"
RIVER_ECOM_PATH = "/Users/adamdimitrov/Development/budapest-adventures/river-ecom.html"
DINNER_PATH = "/Users/adamdimitrov/Development/budapest-adventures/dinner.html"


def normalize_ids_and_deduplicate(raw: str) -> str:
    id_replacements = {
        'id="0-itinerary-and-landmarks"': 'id="cruise-0-itinerary-and-landmarks"',
        'href="#0-itinerary-and-landmarks"': 'href="#cruise-0-itinerary-and-landmarks"',
        'id="1-legenda"': 'id="cruise-1-legenda"',
        'href="#1-legenda"': 'href="#cruise-1-legenda"',
        'id="2-rubingroup"': 'id="cruise-2-rubingroup"',
        'href="#2-rubingroup"': 'href="#cruise-2-rubingroup"',
        'id="4-kisfaludy-historic-cruise"': 'id="cruise-4-kisfaludy-historic-cruise"',
        'href="#4-kisfaludy-historic-cruise"': 'href="#cruise-4-kisfaludy-historic-cruise"',
        'id="3-portum"': 'id="cruise-3-portum"',
        'href="#3-portum"': 'href="#cruise-3-portum"',
        'id="5-silverline-no-frills"': 'id="cruise-5-silverline-no-frills"',
        'href="#5-silverline-no-frills"': 'href="#cruise-5-silverline-no-frills"',
        'id="6-sunset-cocktail-cruise"': 'id="cruise-6-sunset-cocktail-cruise"',
        'href="#6-sunset-cocktail-cruise"': 'href="#cruise-6-sunset-cocktail-cruise"',
        'id="9-pizza-and-beer-cruise"': 'id="cruise-9-pizza-and-beer-cruise"',
        'href="#9-pizza-and-beer-cruise"': 'href="#cruise-9-pizza-and-beer-cruise"',
        'id="7-hk-dinner-cruise"': 'id="cruise-7-hk-dinner-cruise"',
        'href="#7-hk-dinner-cruise"': 'href="#cruise-7-hk-dinner-cruise"',
        'id="8-hk-drinks-cruise"': 'id="cruise-8-hk-drinks-cruise"',
        'href="#8-hk-drinks-cruise"': 'href="#cruise-8-hk-drinks-cruise"',
        'id="10-mahart"': 'id="cruise-10-mahart"',
        'href="#10-mahart"': 'href="#cruise-10-mahart"',
        'id="1-Legenda"': 'id="cruise-1-legenda"',
        'href="#1-Legenda"': 'href="#cruise-1-legenda"',
        'id="2-Silverline-no-show"': 'id="cruise-2-silverline-no-show"',
        'href="#2-Silverline-no-show"': 'href="#cruise-2-silverline-no-show"',
        'id="3-Silverline-folklore"': 'id="cruise-3-silverline-folklore"',
        'href="#3-Silverline-folklore"': 'href="#cruise-3-silverline-folklore"',
        'id="4-silverline-piano"': 'id="cruise-4-silverline-piano"',
        'href="#4-silverline-piano"': 'href="#cruise-4-silverline-piano"',
        'id="5-Hungaria-Koncert"': 'id="cruise-5-hungaria-koncert"',
        'href="#5-Hungaria-Koncert"': 'href="#cruise-5-hungaria-koncert"',
        'id="6-Eurama"': 'id="cruise-6-eurama"',
        'href="#6-Eurama"': 'href="#cruise-6-eurama"',
        'Item #2 on this list': 'Silverline Standard Dinner Cruise',
        'click here to be taken to Item #2': 'see the full Silverline dinner cruise breakdown above',
        'Item #3': 'Silverline Folklore Dinner Cruise',
        'item #4': 'Silverline Piano Dinner Cruise',
    }
    for k, v in id_replacements.items():
        raw = raw.replace(k, v)
    return raw


def fix_empty_hash_links(soup: BeautifulSoup, default_anchor: str):
    for a in soup.find_all("a", href=True):
        if a["href"].strip() == "#":
            txt = a.get_text(" ", strip=True).lower()
            if "3 cocktails" in txt:
                a["href"] = "#cruise-6-sunset-cocktail-cruise"
            elif "pizza" in txt:
                a["href"] = "#cruise-9-pizza-and-beer-cruise"
            elif "prosecco" in txt:
                a["href"] = "#cruise-2-rubingroup"
            elif "folk operetta" in txt:
                a["href"] = "#cruise-3-silverline-folklore"
            elif "folk show" in txt or "wine-tasting" in txt or "craft beers" in txt:
                a["href"] = "#cruise-8-hk-drinks-cruise"
            else:
                a["href"] = default_anchor


def deduplicate_soup_ids(soup: BeautifulSoup):
    seen = {}
    for el in soup.find_all(id=True):
        cid = el["id"]
        if cid not in seen:
            seen[cid] = 1
        else:
            seen[cid] += 1
            if cid == "faq" and el.name == "h2":
                el["id"] = "faq-section-2"
            else:
                el["id"] = f"{cid}-dup{seen[cid]}"

LTT_NAV_STYLES_AND_PARITY_CSS = """<style id="ltt-nav-styles">
  :root {
    --ltt-navy: #0c192c;
    --ltt-gold: #c89d54;
    --ltt-gold-hover: #b2873e;
    --ltt-text: #111827;
    --ltt-muted: #6b7280;
    --ltt-border: #e5e7eb;
    --ltt-bg: #ffffff;
    --ltt-surface: #f8fafc;
  }

  .ltt-navbar {
    position: sticky;
    top: 0;
    z-index: 9999;
    background: rgba(255, 255, 255, 0.97);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--ltt-border);
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    transition: box-shadow 0.2s ease;
  }
  .ltt-navbar.is-scrolled {
    box-shadow: 0 4px 20px rgba(12, 25, 44, 0.07);
  }
  .ltt-nav-inner {
    max-width: 1280px;
    margin: 0 auto;
    height: 72px;
    padding: 0 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
  }

  /* Brand Logo */
  .ltt-brand {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    text-decoration: none;
    color: var(--ltt-navy);
    font-weight: 800;
    font-size: 16px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    flex-shrink: 0;
  }
  .ltt-brand-mark {
    width: 34px;
    height: 34px;
    border-radius: 8px;
    background: var(--ltt-navy);
    color: var(--ltt-gold);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    box-shadow: 0 2px 6px rgba(12, 25, 44, 0.15);
  }
  .ltt-brand-sub {
    display: block;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.12em;
    color: var(--ltt-gold);
    margin-top: -2px;
  }

  /* Desktop Links */
  .ltt-nav-links {
    display: flex;
    align-items: center;
    gap: 6px;
    list-style: none;
    margin: 0;
    padding: 0;
  }
  .ltt-nav-item {
    position: relative;
  }
  .ltt-nav-link,
  .ltt-nav-trigger {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 10px 14px;
    border-radius: 8px;
    font-size: 14.5px;
    font-weight: 600;
    color: var(--ltt-text);
    text-decoration: none;
    background: transparent;
    border: none;
    cursor: pointer;
    font-family: inherit;
    transition: background 0.15s ease, color 0.15s ease;
  }
  .ltt-nav-link:hover,
  .ltt-nav-trigger:hover,
  .ltt-nav-item.is-open .ltt-nav-trigger {
    background: var(--ltt-surface);
    color: var(--ltt-navy);
  }
  .ltt-chevron {
    width: 14px;
    height: 14px;
    transition: transform 0.2s ease;
    opacity: 0.7;
  }
  .ltt-nav-item.is-open .ltt-chevron {
    transform: rotate(180deg);
  }

  /* Mega Dropdown */
  .ltt-mega-menu {
    position: absolute;
    top: calc(100% + 8px);
    left: -80px;
    width: 640px;
    background: var(--ltt-bg);
    border: 1px solid var(--ltt-border);
    border-radius: 16px;
    box-shadow: 0 20px 45px rgba(12, 25, 44, 0.14);
    padding: 20px;
    opacity: 0;
    visibility: hidden;
    transform: translateY(8px);
    transition: opacity 0.18s ease, transform 0.18s ease, visibility 0.18s;
    pointer-events: none;
  }
  .ltt-nav-item.is-open .ltt-mega-menu {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
    pointer-events: auto;
  }
  .ltt-mega-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 12px;
    margin-bottom: 12px;
    border-bottom: 1px solid var(--ltt-border);
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--ltt-muted);
  }
  .ltt-mega-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
  }
  .ltt-mega-card {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px;
    border-radius: 10px;
    text-decoration: none;
    color: var(--ltt-text);
    transition: background 0.15s ease, transform 0.15s ease;
  }
  .ltt-mega-card:hover {
    background: var(--ltt-surface);
    transform: translateX(2px);
  }
  .ltt-mega-icon {
    width: 38px;
    height: 38px;
    border-radius: 8px;
    background: #f1f5f9;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
  }
  .ltt-mega-title {
    font-size: 14px;
    font-weight: 700;
    color: var(--ltt-navy);
    margin: 0 0 2px 0;
    line-height: 1.3;
  }
  .ltt-mega-desc {
    font-size: 12px;
    color: var(--ltt-muted);
    margin: 0;
    line-height: 1.4;
  }

  /* Right Actions */
  .ltt-nav-actions {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .ltt-nav-cta {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 10px 16px;
    border-radius: 999px;
    background: var(--ltt-navy);
    color: #ffffff !important;
    font-size: 13.5px;
    font-weight: 700;
    text-decoration: none;
    transition: background 0.15s ease, transform 0.15s ease;
    white-space: nowrap;
  }
  .ltt-nav-cta:hover {
    background: var(--ltt-gold);
    color: var(--ltt-navy) !important;
    transform: translateY(-1px);
  }

  /* Mobile Hamburger */
  .ltt-burger {
    display: none;
    width: 42px;
    height: 42px;
    border-radius: 10px;
    border: 1px solid var(--ltt-border);
    background: var(--ltt-bg);
    align-items: center;
    justify-content: center;
    cursor: pointer;
    color: var(--ltt-navy);
    padding: 0;
  }
  .ltt-drawer {
    display: none;
    background: var(--ltt-bg);
    border-bottom: 1px solid var(--ltt-border);
    padding: 16px 24px 24px;
    box-shadow: 0 16px 32px rgba(12, 25, 44, 0.1);
  }
  .ltt-navbar.is-mobile-open .ltt-drawer {
    display: block;
  }
  .ltt-drawer-section {
    margin-bottom: 16px;
  }
  .ltt-drawer-label {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--ltt-muted);
    margin: 12px 0 8px;
  }
  .ltt-drawer-links {
    display: grid;
    gap: 6px;
  }
  .ltt-drawer-link {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 11px 14px;
    border-radius: 10px;
    background: var(--ltt-surface);
    color: var(--ltt-navy);
    font-size: 14.5px;
    font-weight: 600;
    text-decoration: none;
  }

  @media (max-width: 991px) {
    .ltt-nav-links,
    .ltt-nav-cta {
      display: none;
    }
    .ltt-burger {
      display: inline-flex;
    }
    .ltt-nav-inner {
      height: 64px;
      padding: 0 16px;
    }
  }

  /* --- Filter Bar Styles --- */
  .bpa-filter-bar {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 16px;
    padding-top: 4px;
  }
  .bpa-filter-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 9px 18px;
    border-radius: 999px;
    font-size: 13.5px;
    font-weight: 700;
    cursor: pointer;
    border: 1px solid #cbd5e1;
    background: #ffffff;
    color: #1e293b;
    transition: all 0.16s ease;
    font-family: inherit;
  }
  .bpa-filter-btn:hover {
    border-color: #0f172a;
    background: #f8fafc;
  }
  .bpa-filter-btn.is-active {
    background: #0f172a;
    color: #ffffff;
    border-color: #0f172a;
    box-shadow: 0 3px 10px rgba(15, 23, 42, 0.16);
  }

  /* --- Detailed Breakdown Accordion Cards (.bpa-details-card) --- */
  .bpa-breakdown-top-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
    margin: 24px 0 18px;
    padding-bottom: 14px;
    border-bottom: 2px solid #e2e8f0;
  }
  .bpa-breakdown-top-bar h2 {
    margin: 0 !important;
    font-size: 26px;
    line-height: 1.25;
    color: #0f172a;
  }
  .bpa-breakdown-controls {
    display: inline-flex;
    gap: 8px;
  }
  .bpa-acc-ctrl-btn {
    padding: 7px 13px;
    border-radius: 8px;
    border: 1px solid #cbd5e1;
    background: #f8fafc;
    color: #334155;
    font-size: 12.5px;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.15s ease;
  }
  .bpa-acc-ctrl-btn:hover {
    background: #e2e8f0;
    color: #0f172a;
  }

  details.bpa-details-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    margin-bottom: 26px;
    box-shadow: 0 4px 18px rgba(15, 23, 42, 0.05);
    overflow: hidden;
    scroll-margin-top: 90px;
  }
  details.bpa-details-card > summary.bpa-details-summary {
    list-style: none;
    cursor: pointer;
    padding: 20px 24px;
    background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
    border-bottom: 1px solid transparent;
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 16px;
    transition: background 0.15s ease;
  }
  details.bpa-details-card[open] > summary.bpa-details-summary {
    border-bottom-color: #e2e8f0;
  }
  details.bpa-details-card > summary.bpa-details-summary::-webkit-details-marker {
    display: none;
  }
  details.bpa-details-card > summary.bpa-details-summary:hover {
    background: #f1f5f9;
  }
  .bpa-details-summary-content {
    flex: 1;
    min-width: 0;
  }
  .bpa-acc-meta {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
  }
  .bpa-acc-meta .bpa-rank-tag {
    position: static !important;
    display: inline-flex;
    align-items: center;
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 800;
    background: #0f172a;
    color: #fff;
  }
  .bpa-acc-meta .bpa-rank-tag.bpa-gold {
    background: linear-gradient(135deg, #f59e0b, #d97706);
    color: #fff;
  }
  .bpa-acc-pill {
    font-size: 13px;
    color: #475569;
    font-weight: 600;
  }
  .bpa-acc-pill strong {
    color: #0f172a;
    font-weight: 800;
  }
  h3.bpa-details-title {
    margin: 4px 0 10px 0 !important;
    font-size: 21px !important;
    line-height: 1.3 !important;
    font-weight: 800 !important;
    color: #0f172a !important;
  }
  .bpa-summary-reviews .div-block-53 {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;
  }
  a.bpa-rev-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 11px;
    border-radius: 999px;
    background: #ffffff;
    border: 1px solid #cbd5e1;
    font-size: 12.5px;
    color: #1e293b;
    text-decoration: none !important;
    font-weight: 600;
    transition: border-color 0.15s ease, transform 0.15s ease;
  }
  a.bpa-rev-badge:hover {
    border-color: #0f172a;
    transform: translateY(-1px);
  }
  img.bpa-rev-icon {
    width: 16px !important;
    height: 16px !important;
    max-width: 16px !important;
    border-radius: 50%;
    object-fit: contain;
    margin: 0 !important;
  }
  .bpa-rev-score {
    font-weight: 800;
    color: #0f172a;
  }
  .bpa-rev-stars {
    color: #f59e0b;
    font-size: 12px;
    letter-spacing: -0.5px;
  }
  .bpa-rev-count {
    color: #64748b;
    font-size: 12px;
  }
  .bpa-details-toggle {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    border-radius: 999px;
    background: #f1f5f9;
    color: #334155;
    font-size: 12px;
    font-weight: 700;
    flex-shrink: 0;
    margin-top: 4px;
  }
  details.bpa-details-card > summary .bpa-details-state-text::before {
    content: "Expand";
  }
  details.bpa-details-card[open] > summary .bpa-details-state-text::before {
    content: "Collapse";
  }
  .bpa-details-chevron {
    display: inline-block;
    transition: transform 0.2s ease;
  }
  details.bpa-details-card[open] > summary .bpa-details-chevron {
    transform: rotate(180deg);
  }
  .bpa-details-body {
    padding: 22px 24px 26px;
  }
  .bpa-details-body img {
    max-width: 100%;
    height: auto;
    border-radius: 10px;
    margin: 12px 0;
  }
  @media (max-width: 767px) {
    details.bpa-details-card > summary.bpa-details-summary {
      padding: 16px;
      flex-direction: column;
    }
    .bpa-details-body {
      padding: 16px;
    }
    h3.bpa-details-title {
      font-size: 18px !important;
    }
  }

  /* --- Clean FAQ Accordion (.bpa-faq-item) --- */
  #faq {
    scroll-margin-top: 90px;
  }
  details.bpa-faq-item {
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    background: #ffffff;
    margin-bottom: 12px;
    overflow: hidden;
  }
  summary.bpa-faq-summary {
    list-style: none;
    cursor: pointer;
    padding: 16px 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    background: #f8fafc;
    font-weight: 700;
    color: #0f172a;
  }
  summary.bpa-faq-summary::-webkit-details-marker {
    display: none;
  }
  h3.bpa-faq-question {
    margin: 0 !important;
    font-size: 17px !important;
    line-height: 1.35 !important;
    font-weight: 700 !important;
    color: #0f172a !important;
  }
  .bpa-faq-chevron {
    font-size: 16px;
    color: #475569;
    transition: transform 0.2s ease;
  }
  details.bpa-faq-item[open] > summary.bpa-faq-summary .bpa-faq-chevron {
    transform: rotate(180deg);
  }
  .bpa-faq-answer {
    padding: 16px 20px;
    border-top: 1px solid #e2e8f0;
    color: #334155;
    line-height: 1.65;
  }

  /* --- Sidebar TOC (.tocitem) --- */
  #toc {
    display: flex;
    flex-direction: column;
    gap: 4px;
    max-height: calc(100vh - 150px);
    overflow-y: auto;
    padding-right: 6px;
  }
  #toc a.tocitem {
    display: block;
    padding: 7px 10px;
    border-radius: 7px;
    font-size: 13px;
    line-height: 1.35;
    color: #475569;
    text-decoration: none;
    border-left: 2px solid transparent;
    transition: all 0.15s ease;
  }
  #toc a.tocitem:hover {
    background: #f1f5f9;
    color: #0f172a;
  }
  #toc a.tocitem.active {
    background: #f1f5f9;
    color: #0f172a;
    font-weight: 700;
    border-left-color: #c89d54;
  }
  .ltt-anchor-alias {
    display: block;
    position: relative;
    top: -90px;
    visibility: hidden;
    height: 0;
  }
</style>
"""


def get_navbar_html(cta_href: str, cta_label: str) -> str:
    return f"""<header class="ltt-navbar" id="lttNavbar">
  <div class="ltt-nav-inner">
    <a href="/" class="ltt-brand" aria-label="Budapest Adventures Home">
      <span class="ltt-brand-mark">⚓</span>
      <span>
        BUDAPEST ADVENTURES
        <span class="ltt-brand-sub">Field-Tested Danube Guides</span>
      </span>
    </a>

    <ul class="ltt-nav-links">
      <li class="ltt-nav-item" id="lttMegaItem">
        <button type="button" class="ltt-nav-trigger" id="lttMegaTrigger" aria-expanded="false">
          Popular Guides
          <svg class="ltt-chevron" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
            <path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z" clip-rule="evenodd"/>
          </svg>
        </button>
        <div class="ltt-mega-menu" id="lttMegaMenu" role="menu">
          <div class="ltt-mega-header">
            <span>Budapest Flagship Rankings (2026)</span>
            <span>Personally Tested</span>
          </div>
          <div class="ltt-mega-grid">
            <a href="/best-budapest-river-cruises" class="ltt-mega-card">
              <span class="ltt-mega-icon">🚢</span>
              <div>
                <div class="ltt-mega-title">10 Best Danube River Cruises</div>
                <p class="ltt-mega-desc">Sightseeing, audio guide &amp; prosecco boats compared side-by-side</p>
              </div>
            </a>
            <a href="/best-dinner-cruises-budapest" class="ltt-mega-card">
              <span class="ltt-mega-icon">🍷</span>
              <div>
                <div class="ltt-mega-title">7 Best Budapest Dinner Cruises</div>
                <p class="ltt-mega-desc">4-course candlelit, folklore &amp; piano battle cruises ranked</p>
              </div>
            </a>
            <a href="/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest" class="ltt-mega-card">
              <span class="ltt-mega-icon">🕯️</span>
              <div>
                <div class="ltt-mega-title">Legenda Candlelit Dinner Review</div>
                <p class="ltt-mega-desc">In-depth review of Budapest's #1 romantic evening cruise</p>
              </div>
            </a>
            <a href="/unlimited-prosecco-cruises-budapest" class="ltt-mega-card">
              <span class="ltt-mega-icon">🥂</span>
              <div>
                <div class="ltt-mega-title">Unlimited Prosecco Cruises</div>
                <p class="ltt-mega-desc">Bottomless sparkling wine &amp; evening party boats on the Danube</p>
              </div>
            </a>
            <a href="/best-night-cruises-budapest" class="ltt-mega-card">
              <span class="ltt-mega-icon">🌃</span>
              <div>
                <div class="ltt-mega-title">Best Evening &amp; Night Cruises</div>
                <p class="ltt-mega-desc">Illuminated Parliament &amp; golden-hour departures</p>
              </div>
            </a>
            <a href="/thermal-baths-budapest" class="ltt-mega-card">
              <span class="ltt-mega-icon">♨️</span>
              <div>
                <div class="ltt-mega-title">8 Best Thermal Baths in Budapest</div>
                <p class="ltt-mega-desc">Széchenyi, Gellért &amp; Rudas compared from first-hand visits</p>
              </div>
            </a>
          </div>
        </div>
      </li>
      <li class="ltt-nav-item">
        <a href="/best-budapest-river-cruises" class="ltt-nav-link">River Cruises</a>
      </li>
      <li class="ltt-nav-item">
        <a href="/best-dinner-cruises-budapest" class="ltt-nav-link">Dinner Cruises</a>
      </li>
      <li class="ltt-nav-item">
        <a href="/about" class="ltt-nav-link">Our Testing Ethics</a>
      </li>
    </ul>

    <div class="ltt-nav-actions">
      <a href="{cta_href}" class="ltt-nav-cta">{cta_label}</a>
      <button type="button" class="ltt-burger" id="lttBurger" aria-label="Toggle Menu" aria-expanded="false">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round">
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <line x1="3" y1="12" x2="21" y2="12"></line>
          <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
      </button>
    </div>
  </div>

  <div class="ltt-drawer" id="lttDrawer">
    <div class="ltt-drawer-section">
      <div class="ltt-drawer-label">Budapest Flagship Guides</div>
      <div class="ltt-drawer-links">
        <a href="/best-budapest-river-cruises" class="ltt-drawer-link"><span>🚢 10 Best Danube River Cruises</span><span>→</span></a>
        <a href="/best-dinner-cruises-budapest" class="ltt-drawer-link"><span>🍷 7 Best Budapest Dinner Cruises</span><span>→</span></a>
        <a href="/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest" class="ltt-drawer-link"><span>🕯️ Legenda Candlelit Dinner Review</span><span>→</span></a>
        <a href="/unlimited-prosecco-cruises-budapest" class="ltt-drawer-link"><span>🥂 Unlimited Prosecco Cruises</span><span>→</span></a>
        <a href="/best-night-cruises-budapest" class="ltt-drawer-link"><span>🌃 Best Evening &amp; Night Cruises</span><span>→</span></a>
        <a href="/thermal-baths-budapest" class="ltt-drawer-link"><span>♨️ 8 Best Thermal Baths in Budapest</span><span>→</span></a>
      </div>
    </div>
    <div class="ltt-drawer-section">
      <div class="ltt-drawer-label">Independent Reviews</div>
      <div class="ltt-drawer-links">
        <a href="/danube-cruise-decision-hub" class="ltt-drawer-link"><span>🧭 Danube Cruise Decision Hub</span><span>→</span></a>
        <a href="/about" class="ltt-drawer-link"><span>✓ About &amp; Testing Ethics</span><span>→</span></a>
      </div>
    </div>
  </div>
</header>
"""


LTT_UNIFIED_FOOTER_SCRIPT = """<script id="ltt-nav-script">
(function() {
  var nav = document.getElementById('lttNavbar');
  var megaItem = document.getElementById('lttMegaItem');
  var megaTrigger = document.getElementById('lttMegaTrigger');
  var burger = document.getElementById('lttBurger');

  if (megaTrigger && megaItem) {
    megaTrigger.addEventListener('click', function(e) {
      e.stopPropagation();
      var open = megaItem.classList.toggle('is-open');
      megaTrigger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('click', function(e) {
      if (!megaItem.contains(e.target)) {
        megaItem.classList.remove('is-open');
        megaTrigger.setAttribute('aria-expanded', 'false');
      }
    });
  }

  if (burger && nav) {
    burger.addEventListener('click', function() {
      var open = nav.classList.toggle('is-mobile-open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  window.addEventListener('scroll', function() {
    if (!nav) return;
    if (window.scrollY > 12) {
      nav.classList.add('is-scrolled');
    } else {
      nav.classList.remove('is-scrolled');
    }
  }, { passive: true });

  /* Category Filter Logic */
  window.bpaFilterCruises = function(btn, cat) {
    var bar = btn.closest('.bpa-filter-bar');
    if (bar) {
      bar.querySelectorAll('.bpa-filter-btn').forEach(function(b) {
        b.classList.remove('is-active');
      });
    }
    btn.classList.add('is-active');
    var deck = btn.closest('.bpa-deck-wrap') || document;
    deck.querySelectorAll('.bpa-card').forEach(function(card) {
      if (cat === 'all') {
        card.style.display = '';
      } else {
        var cats = (card.getAttribute('data-cat') || '').split(/\\s+/);
        card.style.display = cats.indexOf(cat) !== -1 ? '' : 'none';
      }
    });
  };

  /* Expand / Collapse All Detailed Reviews */
  window.bpaToggleAllDetails = function(openState) {
    document.querySelectorAll('details.bpa-details-card').forEach(function(d) {
      d.open = !!openState;
    });
  };

  /* Smooth Scroll with Sticky Header Offset & Auto-Open Details */
  function smoothScrollToElement(targetEl) {
    if (!targetEl) return;
    var parentDetails = targetEl.closest('details');
    if (parentDetails) parentDetails.open = true;
    if (targetEl.tagName && targetEl.tagName.toLowerCase() === 'details') {
      targetEl.open = true;
    }
    var offset = 85;
    var rect = targetEl.getBoundingClientRect();
    var top = rect.top + window.pageYOffset - offset;
    window.scrollTo({ top: Math.max(0, top), behavior: 'smooth' });
  }

  function setupSmoothAnchorJumps() {
    document.addEventListener('click', function(e) {
      var link = e.target.closest('a[href^="#"]');
      if (!link) return;
      var href = link.getAttribute('href');
      if (!href || href === '#') return;
      var targetId = href.slice(1);
      var targetEl = document.getElementById(targetId);
      if (targetEl) {
        e.preventDefault();
        if (nav && nav.classList.contains('is-mobile-open')) {
          nav.classList.remove('is-mobile-open');
        }
        smoothScrollToElement(targetEl);
        if (history.pushState) {
          history.pushState(null, null, '#' + targetId);
        }
      }
    });
  }

  function syncSidebarTOC() {
    var tocContainer = document.getElementById('toc');
    if (!tocContainer) return;
    var links = Array.from(tocContainer.querySelectorAll('a.tocitem'));
    if (!links.length) return;
    var targets = links.map(function(a) {
      var id = (a.getAttribute('href') || '').replace(/^#/, '');
      return { link: a, el: document.getElementById(id) };
    }).filter(function(item) { return !!item.el; });

    function updateActiveTOC() {
      var threshold = window.innerHeight * 0.28;
      var activeItem = targets[0];
      for (var i = 0; i < targets.length; i++) {
        var r = targets[i].el.getBoundingClientRect();
        if (r.top <= threshold) {
          activeItem = targets[i];
        }
      }
      links.forEach(function(a) { a.classList.remove('active'); });
      if (activeItem && activeItem.link) {
        activeItem.link.classList.add('active');
      }
    }
    window.addEventListener('scroll', updateActiveTOC, { passive: true });
    updateActiveTOC();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      setupSmoothAnchorJumps();
      syncSidebarTOC();
    });
  } else {
    setupSmoothAnchorJumps();
    syncSidebarTOC();
  }
})();
</script>
"""


def build_rev_badges_html(rev_nodes) -> str:
    badges = []
    for r in rev_nodes:
        a_tag = r.find("a", href=True)
        href = a_tag["href"] if a_tag else "#river-cruises-quick-summary"
        img_tag = r.find("img")
        img_src = img_tag["src"] if img_tag and img_tag.get("src") else "https://cdn.prod.website-files.com/60e43c7d6d05b671dff0dc1a/65350288cf6e222fd93f3745_getyourguide-icon.png"
        score_el = r.select_one(".price-2-copy")
        score = score_el.get_text(strip=True) if score_el else "4.5"
        cnt_el = r.select_one(".price-5 span, .price-6 span")
        cnt_text = cnt_el.get_text(" ", strip=True) if cnt_el else "+500 reviews"
        badges.append(
            f'<a class="bpa-rev-badge" href="{href}" onclick="event.stopPropagation()" rel="noopener nofollow sponsored" target="_blank">'
            f'<img alt="" class="bpa-rev-icon" loading="lazy" src="{img_src}"/>'
            f'<span class="bpa-rev-score">{score}</span>'
            f'<span class="bpa-rev-stars">★★★★★</span>'
            f'<span class="bpa-rev-count">{cnt_text}</span>'
            f'</a>'
        )
    return "\n".join(badges)


def upgrade_footer_and_faq(soup: BeautifulSoup, current_path: str):
    # 1. Convert .cf-faq-plus-card inside #faq into <details open class="bpa-faq-item">
    faq = soup.find(id="faq")
    if faq:
        for card in faq.select(".cf-faq-plus-card"):
            q_el = card.select_one("h3")
            q_text = q_el.get_text(" ", strip=True) if q_el else "Question"
            ans_el = card.select_one(".cf-faq-content-2, .cf-faq-answer-wrap-2")
            ans_inner = ans_el.decode_contents() if ans_el else ""
            details_html = f"""<details open class="bpa-faq-item">
  <summary class="bpa-faq-summary">
    <h3 class="bpa-faq-question">{q_text}</h3>
    <span class="bpa-faq-chevron">▾</span>
  </summary>
  <div class="bpa-faq-answer w-richtext">{ans_inner}</div>
</details>"""
            new_det = BeautifulSoup(details_html, "html.parser")
            card.replace_with(new_det)

    # 2. Remove .hide---but-don-t-delete from .stick-wrapper
    for dummy in soup.select(".hide---but-don-t-delete"):
        dummy.decompose()

    # 3. Clean legacy TOC scripts in .add-to-footer and upgrade .footer-dark links
    footer = soup.select_one("section.footer-dark")
    if footer:
        cols = footer.select(".footer-link-column")
        if len(cols) >= 2:
            r_curr = ' aria-current="page" class="footer-link-3 w--current"' if current_path == "river" else ' class="footer-link-3"'
            d_curr = ' aria-current="page" class="footer-link-3 w--current"' if current_path == "dinner" else ' class="footer-link-3"'
            cols[0].clear()
            cols[0].append(BeautifulSoup(f"""
              <div class="footer-link-title">Budapest Cruise Guides</div>
              <a{r_curr} href="/best-budapest-river-cruises">10 Best Danube River Cruises</a>
              <a{d_curr} href="/best-dinner-cruises-budapest">7 Best Budapest Dinner Cruises</a>
              <a class="footer-link-3" href="/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest">Legenda Candlelit Dinner Review</a>
              <a class="footer-link-3" href="/unlimited-prosecco-cruises-budapest">Unlimited Prosecco Cruises</a>
              <a class="footer-link-3" href="/best-night-cruises-budapest">Best Evening &amp; Night Cruises</a>
              <a class="footer-link-3" href="/thermal-baths-budapest">8 Best Thermal Baths</a>
            """, "html.parser"))
            cols[1].clear()
            cols[1].append(BeautifulSoup("""
              <div class="footer-link-title">Editorial &amp; Network</div>
              <a class="footer-link-3" href="/danube-cruise-decision-hub">Danube Cruise Decision Hub</a>
              <a class="footer-link-3" href="/legenda-city-cruises">Legenda City Cruises Guide</a>
              <a class="footer-link-3" href="/about">About &amp; Testing Ethics</a>
              <a class="footer-link-3" href="https://www.thecruisedetective.com" target="_blank" rel="noopener">TheCruiseDetective.com</a>
              <a class="footer-link-3" href="https://luxurytraveltester.com/" target="_blank" rel="noopener">LuxuryTravelTester.com</a>
            """, "html.parser"))
        legal = footer.select_one(".legal-text")
        if legal:
            legal.string = "© 2026 BudapestAdventures.com. All rights reserved."
        add_footer = footer.select_one(".add-to-footer")
        if add_footer:
            for sc in add_footer.find_all("script"):
                txt = sc.get_text() or ""
                if "IntersectionObserver" in txt or "querySelectorAll(\"h2\")" in txt:
                    sc.decompose()


def replace_navbars(soup: BeautifulSoup, cta_href: str, cta_label: str):
    # Remove old Webflow navbars
    for sel in [".t-navigation", ".navigation-mob", ".navigation-4", "#lttNavbar", "#ltt-nav-styles", "#ltt-nav-script"]:
        for el in soup.select(sel):
            el.decompose()
    head = soup.find("head")
    if head:
        head.append(BeautifulSoup(LTT_NAV_STYLES_AND_PARITY_CSS, "html.parser"))
    body = soup.find("body")
    if body:
        body.insert(0, BeautifulSoup(get_navbar_html(cta_href, cta_label), "html.parser"))
        body.append(BeautifulSoup(LTT_UNIFIED_FOOTER_SCRIPT, "html.parser"))


def process_river():
    subprocess.run(["git", "checkout", "--", "river.html"], cwd="/Users/adamdimitrov/Development/budapest-adventures", check=True)
    upgrade_river_file("river.html", build_river_deck_and_sticky())
    raw = open(RIVER_PATH, "r", encoding="utf-8").read().replace("\u200d", "")
    raw = normalize_ids_and_deduplicate(raw)
    soup = BeautifulSoup(raw, "html.parser")
    fix_empty_hash_links(soup, "#river-cruises-quick-summary")

    # 1. Replace navbars
    replace_navbars(soup, "#river-cruises-quick-summary", "Compare Top 10 ↓")

    # 2. Clean intro container & remove 2022 H1 / Jump to list / mobile-sticky-cta
    for div25 in soup.select(".div-block-25"):
        div25.decompose()
    for mcta in soup.select(".mobile-sticky-cta"):
        mcta.decompose()
    for a in soup.find_all("a"):
        if "jump to list" in a.get_text(" ", strip=True).lower():
            p = a.find_parent("p")
            if p:
                p.decompose()
            else:
                a.decompose()

    # 3. Assign data-cat to the 10 .bpa-card elements and add filter bar inside .bpa-section-header
    river_cats = [
        "sightseeing",           # 1 Legenda
        "drinks",                # 2 Rubin Group Unlimited Prosecco
        "sightseeing",           # 3 Kisfaludy Steamer
        "sightseeing budget",    # 4 Portum €14
        "sightseeing budget",    # 5 Silverline No-Frills €12-14
        "drinks",                # 6 Silverline Sunset Cocktails
        "food drinks",           # 7 Silverline Pizza & Beer
        "food",                  # 8 Hungaria Koncert Buffet & Folk
        "drinks",                # 9 Hungaria Koncert Wine & Violin
        "sightseeing budget",    # 10 Mahart Hop-On Hop-Off €12-18
    ]
    cards = soup.select(".bpa-deck-wrap .bpa-card")
    for idx, card in enumerate(cards):
        if idx < len(river_cats):
            card["data-cat"] = river_cats[idx]

    deck_wrap = soup.select_one(".bpa-deck-wrap")
    if deck_wrap:
        deck_wrap["id"] = "river-cruises-quick-summary"
        sec_header = deck_wrap.select_one(".bpa-section-header")
        if sec_header and not sec_header.select_one(".bpa-filter-bar"):
            filter_bar_html = """<div class="bpa-filter-bar" role="tablist" aria-label="Filter Budapest River Cruises">
  <button type="button" class="bpa-filter-btn is-active" onclick="bpaFilterCruises(this, 'all')">All 10 Cruises</button>
  <button type="button" class="bpa-filter-btn" onclick="bpaFilterCruises(this, 'sightseeing')">🏛️ Sightseeing &amp; Audio Guide</button>
  <button type="button" class="bpa-filter-btn" onclick="bpaFilterCruises(this, 'drinks')">🥂 Prosecco &amp; Cocktail Cruises</button>
  <button type="button" class="bpa-filter-btn" onclick="bpaFilterCruises(this, 'food')">🍕 Dinner &amp; Pizza Cruises</button>
  <button type="button" class="bpa-filter-btn" onclick="bpaFilterCruises(this, 'budget')">💰 Budget Under €18</button>
</div>"""
            sec_header.append(BeautifulSoup(filter_bar_html, "html.parser"))

    # 4. Extract all 10 reviews from div.w-tabs nav.faq-content-wrap and build <details open class="bpa-details-card">
    navs = soup.select("div.w-tabs nav.faq-content-wrap")
    details_elements = []
    toc_entries = [
        ("river-cruises-quick-summary", "Comparison — Top 10 River Cruises"),
        ("river-cruises-detailed-breakdown", "Detailed Cruise Reviews (1–10)"),
    ]

    for idx, nav in enumerate(navs):
        card = cards[idx] if idx < len(cards) else None
        db27 = nav.select_one(".div-block-27[id]") or nav.select_one("[id^='cruise-']")
        cid = db27["id"] if db27 and db27.get("id") else f"cruise-{idx+1}"

        rank_el = card.select_one(".bpa-rank-tag") if card else None
        rank_text = rank_el.get_text(" ", strip=True) if rank_el else f"#{idx+1} Pick"
        rank_cls = " ".join(rank_el.get("class", ["bpa-rank-tag"])) if rank_el else "bpa-rank-tag"

        kicker_el = card.select_one(".bpa-kicker") if card else None
        kicker_text = kicker_el.get_text(" ", strip=True) if kicker_el else "Danube Cruise"

        price_el = card.select_one(".bpa-price-num") if card else None
        price_text = price_el.get_text(" ", strip=True) if price_el else "€20"

        title_el = card.select_one(".bpa-title") if card else nav.find("h2")
        title_text = title_el.get_text(" ", strip=True) if title_el else f"Cruise {idx+1}"
        numbered_title = f"{idx+1}. {title_text}"

        rev_nodes = nav.select(".reviews-3, .reviews-4")
        rev_badges_html = build_rev_badges_html(rev_nodes)

        # Clean inner duplicate IDs and redundant headers inside nav
        for el_with_id in nav.select(f"[id='{cid}']"):
            del el_with_id["id"]
        for h2 in nav.select("h2.heading-33"):
            h2.decompose()
        for db26 in nav.select(".div-block-26"):
            db26.decompose()
        for tb27 in nav.select(".text-block-27"):
            tb27.decompose()
        for db34 in nav.select(".div-block-34, .div-block-34-obsolete"):
            db34.decompose()
        for rev_leftover in nav.select(".reviews-3, .reviews-4"):
            rev_leftover.decompose()

        body_html = nav.decode_contents()
        details_html = f"""<details open class="bpa-details-card" id="{cid}">
  <summary class="bpa-details-summary">
    <div class="bpa-details-summary-content">
      <div class="bpa-acc-meta">
        <span class="{rank_cls}">{rank_text}</span>
        <span class="bpa-acc-pill">{kicker_text} • <strong>{price_text}</strong></span>
      </div>
      <h3 class="bpa-details-title">{numbered_title}</h3>
      <div class="bpa-summary-reviews">
        <div class="div-block-53">
          {rev_badges_html}
        </div>
      </div>
    </div>
    <div class="bpa-details-toggle">
      <span class="bpa-details-state-text"></span>
      <span class="bpa-details-chevron">▾</span>
    </div>
  </summary>
  <div class="bpa-details-body">
    {body_html}
  </div>
</details>"""
        details_elements.append(BeautifulSoup(details_html, "html.parser"))
        short_kicker = kicker_text.split("•")[0].strip()
        toc_entries.append((cid, f"{idx+1}. {short_kicker} ({price_text})"))

    # Remove old div.h2-wrapper#river-cruises-quick-summary and div.w-tabs from .comparison-table
    comp_section = soup.select_one(".comparison-table")
    if comp_section:
        for old_h2_wrap in comp_section.select("div.h2-wrapper, h2#river-cruises-quick-summary"):
            old_h2_wrap.decompose()
        for wtabs in comp_section.select("div.w-tabs"):
            wtabs.decompose()

    # Insert .bpa-breakdown-top-bar and all 10 <details> at the top of .content-right_blog
    content_right = soup.select_one(".blog-section .content-right_blog")
    if content_right:
        top_bar_html = """<div class="bpa-breakdown-top-bar">
  <h2 class="heading-30" id="river-cruises-detailed-breakdown">Detailed Breakdown — 10 Best River Cruises in Budapest</h2>
  <div class="bpa-breakdown-controls">
    <button type="button" class="bpa-acc-ctrl-btn" onclick="bpaToggleAllDetails(true)">Expand All</button>
    <button type="button" class="bpa-acc-ctrl-btn" onclick="bpaToggleAllDetails(false)">Collapse All</button>
  </div>
</div>"""
        anchor_ref = content_right.find(id="cruise-0-itinerary-and-landmarks")
        if anchor_ref:
            anchor_ref.insert_before(BeautifulSoup(top_bar_html, "html.parser"))
            for det in details_elements:
                anchor_ref.insert_before(det)

        # Unwrap .load-more-div inside #cruise-0-itinerary-and-landmarks
        for lmd in content_right.select(".load-more-div"):
            lmd.unwrap()

        # Ensure clean IDs on remaining H2s in .content-right_blog
        for h2 in content_right.find_all("h2"):
            txt = h2.get_text(" ", strip=True)
            if "Types of River Cruises" in txt:
                h2["id"] = "types-of-river-cruises-in-budapest"
            elif txt == "Video":
                h2["id"] = "river-cruise-video-overview"

    toc_entries.extend([
        ("why-go-on-a-river-cruise", "Itinerary & Port Map"),
        ("types-of-river-cruises-in-budapest", "Types of River Cruises"),
        ("river-cruise-video-overview", "Video Overview"),
        ("faq", "Frequently Asked Questions"),
    ])

    # Populate #toc
    toc_box = soup.find(id="toc")
    if toc_box:
        toc_box.clear()
        for tid, tlabel in toc_entries:
            a_tag = soup.new_tag("a", href=f"#{tid}", **{"class": "tocitem"})
            a_tag.string = tlabel
            toc_box.append(a_tag)

    # Upgrade FAQ and Footer
    upgrade_footer_and_faq(soup, "river")
    deduplicate_soup_ids(soup)

    # Fix JSON-LD ItemList anchor URLs at bottom of river.html
    for sc in soup.find_all("script", type="application/ld+json"):
        if sc.string and "#3-duna-cruises" in sc.string:
            s = sc.string
            s = s.replace("#3-duna-cruises", "#cruise-4-kisfaludy-historic-cruise")
            s = s.replace("#4-portum", "#cruise-3-portum")
            s = s.replace("#5-silverline-sightseeing", "#cruise-5-silverline-no-frills")
            s = s.replace("#6-silverline-cocktails", "#cruise-6-sunset-cocktail-cruise")
            s = s.replace('"#7"', '"#cruise-9-pizza-and-beer-cruise"')
            s = s.replace("#8-hungaria-koncert", "#cruise-7-hk-dinner-cruise")
            s = s.replace("#9-hungaria-koncert", "#cruise-8-hk-drinks-cruise")
            s = s.replace("#10-mahart", "#cruise-10-mahart")
            sc.string = s

    out_html = str(soup).replace("\u200d", "")
    open(RIVER_PATH, "w", encoding="utf-8").write(out_html)
    shutil.copyfile(RIVER_PATH, RIVER_ECOM_PATH)
    print("Successfully updated river.html and synced to river-ecom.html")


def get_cruise_7_dinner_details_html() -> str:
    gyg_url = "https://www.getyourguide.com/budapest-l29/budapestpremium-dinner-cruise-live-music-unlimited-drinks-t494832/?partner_id=YS414AJ&utm_medium=online_publisher&cmp=budapest-dinner-cruises-comparison-list-unlimited-drinks"
    return f"""<details open class="bpa-details-card" id="cruise-7-unlimited-drinks">
  <summary class="bpa-details-summary">
    <div class="bpa-details-summary-content">
      <div class="bpa-acc-meta">
        <span class="bpa-rank-tag">🍸 #7 Unlimited Drinks</span>
        <span class="bpa-acc-pill">River Diva / Rubin Group • 📍 Dock 8A • <strong>€99</strong></span>
      </div>
      <h3 class="bpa-details-title">7. 4-Course Dinner Cruise With Live Music &amp; Unlimited Drinks</h3>
      <div class="bpa-summary-reviews">
        <div class="div-block-53">
          <a class="bpa-rev-badge" href="{gyg_url}" onclick="event.stopPropagation()" rel="noopener nofollow sponsored" target="_blank">
            <img alt="" class="bpa-rev-icon" loading="lazy" src="https://cdn.prod.website-files.com/60e43c7d6d05b671dff0dc1a/65350288cf6e222fd93f3745_getyourguide-icon.png"/>
            <span class="bpa-rev-score">4.6</span>
            <span class="bpa-rev-stars">★★★★★</span>
            <span class="bpa-rev-count">+540 reviews</span>
          </a>
          <a class="bpa-rev-badge" href="{gyg_url}" onclick="event.stopPropagation()" rel="noopener nofollow sponsored" target="_blank">
            <img alt="" class="bpa-rev-icon" loading="lazy" src="https://cdn.prod.website-files.com/652d0405192ba076b04f74a3/68f64414502d0348145b678e_tripadvisor-icon.avif"/>
            <span class="bpa-rev-score">4.4</span>
            <span class="bpa-rev-stars">★★★★☆</span>
            <span class="bpa-rev-count">+230 reviews</span>
          </a>
          <a class="bpa-rev-badge" href="{gyg_url}" onclick="event.stopPropagation()" rel="noopener nofollow sponsored" target="_blank">
            <img alt="" class="bpa-rev-icon" loading="lazy" src="https://cdn.prod.website-files.com/60e43c7d6d05b671dff0dc1a/65350288cf6e222fd93f3747_viator-icon.png"/>
            <span class="bpa-rev-score">4.5</span>
            <span class="bpa-rev-stars">★★★★★</span>
            <span class="bpa-rev-count">+150 reviews</span>
          </a>
        </div>
      </div>
    </div>
    <div class="bpa-details-toggle">
      <span class="bpa-details-state-text"></span>
      <span class="bpa-details-chevron">▾</span>
    </div>
  </summary>
  <div class="bpa-details-body">
    <a id="cruise-7-grasham-palace" class="ltt-anchor-alias"></a>
    <img alt="4-Course Dinner Cruise With Live Music &amp; Unlimited Drinks on River Diva" loading="lazy" src="https://cdn.prod.website-files.com/60e43c7d6d05b671dff0dc1a/68e7f8b85dd0bfdd37755de4_best-budapest-dinner-cruises-unlimited-drinks.avif"/>
    <div class="pro-con-box-wrapper">
      <div class="w-layout-grid grid-15">
        <div class="pro-con-box-pro-cell" data-wf-pbl="layout-grid-1x2-vertical">
          <div class="pro-con-box-pro-cell-rich-text-block w-richtext">
            <h3><strong>Pros:</strong></h3>
            <ul>
              <li><strong>Unlimited Drinks Package Included</strong> — Bottomless Hungarian wines, sparkling wine, draft beer, soft drinks, and espresso/tea throughout the entire 2.5-hour sailing.</li>
              <li><strong>Modern Event Ship (River Diva)</strong> — Floor-to-ceiling panoramic dining room windows plus a spacious open-air upper viewing deck for unobstructed Parliament photos.</li>
              <li><strong>Fine-Dining 4-Course Plated Menu</strong> — Contemporary plated presentation with duck, beef cheeks, salmon, or vegetarian/vegan courses prepared fresh onboard.</li>
              <li><strong>Relaxed Live Acoustic Atmosphere</strong> — Live acoustic guitar and vocal duo sets an upscale evening mood without overpowering table conversation.</li>
            </ul>
          </div>
        </div>
        <div class="pro-con-box-con-cell" data-wf-pbl="layout-grid-1x2-vertical">
          <div class="pro-con-box-con-cell-rich-text-block w-richtext">
            <h3><strong>Cons:</strong></h3>
            <ul>
              <li><strong>No Traditional Folklore Dance Show</strong> — Focuses on modern live music and social dining rather than traditional Hungarian folk dancing.</li>
              <li><strong>Hard Spirits Cost Extra</strong> — The unlimited package covers wines, sparkling wine, beer, and soft drinks, while premium cocktails and shots are billed à la carte.</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    <div class="w-richtext">
      <h3><strong>Summary</strong></h3>
      <p>If you want a sit-down <strong>4-course plated dinner</strong> without worrying about an expensive bar tab at the end of the night, the <strong>River Diva Unlimited Drinks Dinner Cruise</strong> at Dock 8A is the standout choice in Budapest.</p>
      <p>Most Danube dinner cruises only include a single welcome glass of sparkling wine, charging €6–€10 for every extra glass of wine or beer. Here, <strong>unlimited Hungarian wines, sparkling wine, beer, and soft drinks</strong> are bundled directly into the €99 ticket across a generous <strong>2.5-hour route</strong>.</p>
      <h3><strong>What's Included &amp; Menu Highlights</strong></h3>
      <ul role="list">
        <li><strong>🥂 Welcome Sparkling Wine &amp; Bottomless Drinks:</strong> Unlimited white, rosé, and red Hungarian wines, sparkling wine, beer, mineral water, juices, and coffee/tea.</li>
        <li><strong>🍽️ 4-Course Plated Dinner:</strong> Choice of amuse-bouche and starter, traditional soup, main course (slow-cooked beef cheeks, crispy duck leg, grilled salmon, or vegetarian tofu steak), and artisan dessert.</li>
        <li><strong>🎶 Live Acoustic Music:</strong> Live acoustic performance in the panoramic lower salon followed by upper-deck sightseeing under the illuminated bridges.</li>
      </ul>
      <h3><strong>Quick Facts</strong></h3>
      <ul role="list">
        <li><strong>📅 Schedule:</strong> Evening boarding at 19:00 (2.5-hour duration)</li>
        <li><strong>🎟️ Ticket type:</strong> Instant smartphone QR ticket (free cancellation up to 24h in advance)</li>
        <li><strong>✔️ Open-air upper deck:</strong> Yes, 360-degree rooftop viewing deck</li>
        <li><strong>✔️ Air conditioning/heating:</strong> Yes, climate-controlled glass dining salon</li>
      </ul>
      <h3><strong>How to Get There</strong></h3>
      <ul role="list">
        <li>🗺️ <strong>Meeting point:</strong> Budapest, Jane Haining rakpart, <strong>Dock 8A</strong> (directly beneath the white Elizabeth Bridge on the Pest side).</li>
        <li>📘 Take <strong>Tram Line 2</strong> to <strong>Március 15. tér</strong> and walk 2 minutes down to the Danube promenade at Dock 8A.</li>
      </ul>
      <p><a href="{gyg_url}" target="_blank" rel="sponsored noopener" class="bpa-book-button bpa-btn" style="display:inline-block;margin-top:8px;text-decoration:none;">Check Availability &amp; Menu on GetYourGuide →</a></p>
    </div>
  </div>
</details>"""


def process_dinner():
    subprocess.run(["git", "checkout", "--", "dinner.html"], cwd="/Users/adamdimitrov/Development/budapest-adventures", check=True)
    base_d = open(DINNER_PATH, "r", encoding="utf-8").read()
    base_d = base_d.replace(
        '<a href="#" class="view-all-button w-inline-block">',
        '<a href="#dinner-cruises-list" class="view-all-button w-inline-block">'
    )
    open(DINNER_PATH, "w", encoding="utf-8").write(base_d)
    upgrade_dinner_file(build_dinner_deck_and_sticky())
    raw = open(DINNER_PATH, "r", encoding="utf-8").read().replace("\u200d", "")
    raw = normalize_ids_and_deduplicate(raw)
    soup = BeautifulSoup(raw, "html.parser")
    fix_empty_hash_links(soup, "#dinner-cruises-list")

    # 1. Replace navbars
    replace_navbars(soup, "#dinner-cruises-list", "Compare Top 7 ↓")

    # 2. Clean .comparison-table: remove duplicate div#dinner-cruises-list.h2-wrapper and old div.container-20 (.w-tabs)
    comp_section = soup.select_one(".comparison-table")
    if comp_section:
        for old_h2_wrap in comp_section.select("div.h2-wrapper"):
            old_h2_wrap.decompose()
        for old_c20 in comp_section.select("div.container-20"):
            old_c20.decompose()

    # 3. Configure .bpa-deck-wrap with id="dinner-cruises-list", alias, .bpa-section-header, and filter tabs
    dinner_cats = [
        "plated",                  # 1 Legenda Candlelit
        "plated value",            # 2 Silverline No Show €74
        "plated show",             # 3 Silverline Folklore €91
        "plated show",             # 4 Silverline Piano Battle €91
        "buffet-drinks show value",# 5 Hungaria Koncert Buffet €79
        "plated show",             # 6 Eurama €90
        "plated buffet-drinks",    # 7 River Diva Unlimited Drinks €99
    ]
    cards = soup.select(".bpa-deck-wrap .bpa-card")
    for idx, card in enumerate(cards):
        if idx < len(dinner_cats):
            card["data-cat"] = dinner_cats[idx]
        # Fix Card 7 sublink to jump to #cruise-7-unlimited-drinks
        if idx == 6:
            sublink = card.select_one(".bpa-sublink")
            if sublink:
                sublink["href"] = "#cruise-7-unlimited-drinks"
                del sublink["target"]
                del sublink["rel"]
                sublink.string = "Read Full Review ↓"

    deck_wrap = soup.select_one(".bpa-deck-wrap")
    if deck_wrap:
        deck_wrap["id"] = "dinner-cruises-list"
        if not deck_wrap.select_one(".bpa-section-header"):
            header_html = """<div class="bpa-section-header">
  <a id="quick-summary-river-cruises-budapest" class="ltt-anchor-alias"></a>
  <h2 class="bpa-section-title">Comparison — 7 Best Dinner Cruises in Budapest (2026)</h2>
  <p class="bpa-section-sub">Personally field-tested on the Danube • Verified prices, dock locations &amp; unretouched photos</p>
  <div class="bpa-filter-bar" role="tablist" aria-label="Filter Budapest Dinner Cruises">
    <button type="button" class="bpa-filter-btn is-active" onclick="bpaFilterCruises(this, 'all')">All 7 Dinner Cruises</button>
    <button type="button" class="bpa-filter-btn" onclick="bpaFilterCruises(this, 'plated')">🍽️ 4-Course Plated</button>
    <button type="button" class="bpa-filter-btn" onclick="bpaFilterCruises(this, 'show')">🎻 Folklore &amp; Piano Shows</button>
    <button type="button" class="bpa-filter-btn" onclick="bpaFilterCruises(this, 'buffet-drinks')">🍷 Buffet &amp; Unlimited Drinks</button>
    <button type="button" class="bpa-filter-btn" onclick="bpaFilterCruises(this, 'value')">💰 Best Value Under €85</button>
  </div>
</div>"""
            deck_wrap.insert(0, BeautifulSoup(header_html, "html.parser"))

    # Update #hybridSheet and scroll spy script to include #7
    hybrid_sheet = soup.find(id="hybridSheet")
    if hybrid_sheet:
        toc_list = hybrid_sheet.select_one(".hybrid-toc-list")
        if toc_list and not toc_list.select_one("a[href='#cruise-7-unlimited-drinks']"):
            link7_html = """<a class="hybrid-toc-link" href="#cruise-7-unlimited-drinks" onclick="closeHybridSheet()">
  <span><strong>#7</strong> · River Diva 4-Course Dinner + Unlimited Drinks</span>
  <span class="toc-price">€99</span>
</a>"""
            toc_list.append(BeautifulSoup(link7_html, "html.parser"))
        sc = hybrid_sheet.find_next_sibling("script")
        if sc and sc.string and "cruise-6-eurama" in sc.string and "cruise-7-unlimited-drinks" not in sc.string:
            sc.string = sc.string.replace(
                '{id:"cruise-6-eurama",badge:"#6 CENTRAL",title:"Eurama 4-Course Dinner & Folk",price:"€90",url:"https://www.getyourguide.com/budapest-l29/budapest-evening-cruise-and-dinner-with-champagne-t408084/?partner_id=YS414AJ&utm_medium=online_publisher&cmp=eng-dinner-cruises-budapest-eurama-reviews&mkt_cmp=true"}',
                '{id:"cruise-6-eurama",badge:"#6 CENTRAL",title:"Eurama 4-Course Dinner & Folk",price:"€90",url:"https://www.getyourguide.com/budapest-l29/budapest-evening-cruise-and-dinner-with-champagne-t408084/?partner_id=YS414AJ&utm_medium=online_publisher&cmp=eng-dinner-cruises-budapest-eurama-reviews&mkt_cmp=true"},\n    {id:"cruise-7-unlimited-drinks",badge:"#7 DRINKS",title:"River Diva 4-Course + Unlimited Drinks",price:"€99",url:"https://www.getyourguide.com/budapest-l29/budapestpremium-dinner-cruise-live-music-unlimited-drinks-t494832/?partner_id=YS414AJ&utm_medium=online_publisher&cmp=budapest-dinner-cruises-comparison-list-unlimited-drinks"}'
            )

    # 4. Inside .content-right_blog: unwrap all .load-more-div, remove .div-block-39, wrap 6 reviews in <details open class="bpa-details-card"> and append 7th review
    content_right = soup.select_one(".blog-section .content-right_blog")
    toc_entries = [
        ("dinner-cruises-list", "Comparison — Top 7 Dinner Cruises"),
        ("budapest-dinner-cruise-itinerary", "Budapest Dinner Cruise Itinerary"),
        ("dinner-cruises-breakdown", "Detailed Cruise Reviews (1–7)"),
    ]

    if content_right:
        # Remove all "LOAD MORE" button containers and gradients, and unwrap .load-more-div
        for db39 in content_right.select(".div-block-39, .linear-gradient"):
            db39.decompose()
        for lmd in content_right.select(".load-more-div"):
            lmd.unwrap()
        for div_line in content_right.select(".divider"):
            div_line.decompose()

        # Fix H2 itinerary ID and convert inner "Detailed Breakdown" h2 inside cruise 3 to h3
        for h2 in content_right.find_all("h2"):
            txt = h2.get_text(" ", strip=True)
            if txt == "Budapest Dinner Cruise Itinerary":
                h2["id"] = "budapest-dinner-cruise-itinerary"
            elif txt == "Detailed Breakdown":
                h2.name = "h3"

        # Upgrade h2#dinner-cruises-breakdown wrapper into .bpa-breakdown-top-bar
        bd_h2 = content_right.find(id="dinner-cruises-breakdown")
        if bd_h2 and bd_h2.parent and "h2-wrapper" in (bd_h2.parent.get("class") or []):
            top_bar_html = """<div class="bpa-breakdown-top-bar">
  <h2 class="heading-30" id="dinner-cruises-breakdown">Detailed Breakdown — 7 Best Dinner Cruises in Budapest</h2>
  <div class="bpa-breakdown-controls">
    <button type="button" class="bpa-acc-ctrl-btn" onclick="bpaToggleAllDetails(true)">Expand All</button>
    <button type="button" class="bpa-acc-ctrl-btn" onclick="bpaToggleAllDetails(false)">Collapse All</button>
  </div>
</div>"""
            bd_h2.parent.replace_with(BeautifulSoup(top_bar_html, "html.parser"))

        # Transform each of the 6 existing review containers into <details open class="bpa-details-card">
        last_details = None
        for idx in range(1, 7):
            db = content_right.select_one(f"div[id^='cruise-{idx}-']")
            if not db:
                continue
            cid = db["id"]
            container = db.parent
            card = cards[idx - 1] if idx - 1 < len(cards) else None

            rank_el = card.select_one(".bpa-rank-tag") if card else None
            rank_raw = rank_el.get_text(" ", strip=True) if rank_el else f"#{idx} Pick"
            rank_text = f"🏆 #{idx} {rank_raw}" if idx == 1 else f"#{idx} {rank_raw}"
            rank_cls = "bpa-rank-tag bpa-gold" if idx == 1 else "bpa-rank-tag"

            kicker_el = card.select_one(".bpa-kicker") if card else None
            kicker_text = kicker_el.get_text(" ", strip=True) if kicker_el else "Budapest Dinner Cruise"

            price_el = card.select_one(".bpa-price-num") if card else None
            price_text = price_el.get_text(" ", strip=True) if price_el else "€90"

            title_el = card.select_one(".bpa-title") if card else db.find("h2")
            title_text = title_el.get_text(" ", strip=True) if title_el else f"Dinner Cruise {idx}"
            numbered_title = f"{idx}. {title_text}"

            rev_nodes = container.select(".reviews-3, .reviews-4")
            rev_badges_html = build_rev_badges_html(rev_nodes)

            # Remove duplicate ID and old header elements inside container
            del db["id"]
            for h2 in container.select("h2.heading-33"):
                h2.decompose()
            for db26 in container.select(".div-block-26"):
                db26.decompose()
            for db34 in container.select(".div-block-34, .div-block-34-obsolete"):
                db34.decompose()
            for rev_leftover in container.select(".reviews-3, .reviews-4"):
                rev_leftover.decompose()

            body_html = container.decode_contents()
            details_html = f"""<details open class="bpa-details-card" id="{cid}">
  <summary class="bpa-details-summary">
    <div class="bpa-details-summary-content">
      <div class="bpa-acc-meta">
        <span class="{rank_cls}">{rank_text}</span>
        <span class="bpa-acc-pill">{kicker_text} • <strong>{price_text}</strong></span>
      </div>
      <h3 class="bpa-details-title">{numbered_title}</h3>
      <div class="bpa-summary-reviews">
        <div class="div-block-53">
          {rev_badges_html}
        </div>
      </div>
    </div>
    <div class="bpa-details-toggle">
      <span class="bpa-details-state-text"></span>
      <span class="bpa-details-chevron">▾</span>
    </div>
  </summary>
  <div class="bpa-details-body">
    {body_html}
  </div>
</details>"""
            new_det = BeautifulSoup(details_html, "html.parser")
            container.replace_with(new_det)
            last_details = new_det
            short_kicker = kicker_text.split("•")[0].strip()
            toc_entries.append((cid, f"{idx}. {short_kicker} ({price_text})"))

        # Insert 7th review (#cruise-7-unlimited-drinks) right after #cruise-6-eurama
        det7 = BeautifulSoup(get_cruise_7_dinner_details_html(), "html.parser")
        c6_el = content_right.find(id="cruise-6-eurama")
        if c6_el:
            c6_el.insert_after(det7)
        elif last_details:
            last_details.insert_after(det7)
        toc_entries.append(("cruise-7-unlimited-drinks", "7. River Diva Unlimited Drinks (€99)"))

    toc_entries.append(("faq", "Frequently Asked Questions"))

    # Populate #toc
    toc_box = soup.find(id="toc")
    if toc_box:
        toc_box.clear()
        for tid, tlabel in toc_entries:
            a_tag = soup.new_tag("a", href=f"#{tid}", **{"class": "tocitem"})
            a_tag.string = tlabel
            toc_box.append(a_tag)

    # Upgrade FAQ and Footer
    upgrade_footer_and_faq(soup, "dinner")
    deduplicate_soup_ids(soup)

    out_html = str(soup).replace("\u200d", "")
    open(DINNER_PATH, "w", encoding="utf-8").write(out_html)
    print("Successfully updated dinner.html")


if __name__ == "__main__":
    process_river()
    process_dinner()
