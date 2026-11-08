#!/usr/bin/env python3
"""Port Luxury Editorial & CRO Design System upgrades to Budapest Adventures core guides.

Upgrades:
1. Google Fonts Playfair Display preconnect & stylesheet in <head>.
2. Hero H1 centering override & Hero Credibility Stat badge ("Zero Freebies — No Sponsored PR Sailings").
3. Upgraded .bpa-card, .bpa-kicker, .bpa-title / .bpa-headline (Playfair Display serif),
   .bpa-proof, .bpa-stars, .bpa-score-text, .bpa-vchip, .bpa-channels, .bpa-ci,
   .bpa-specs-row (2-column grid with odd-last-child span 2), .bpa-best-for.
4. Fixed .hybrid-toc-btn vertical centering (viewBox="0 0 20 14") + .hybrid-sticky-bar + #hybridSheet TOC.
5. Complete 50/50 Luxury Editorial Pros & Cons Architecture (.pro-con-box-wrapper, .pro-con-box-pro-cell,
   .pro-con-box-con-cell) with normalized <ul><li> items.
"""

import re
from pathlib import Path

ROOT = Path("/Users/adamdimitrov/Development/budapest-adventures")

GOOGLE_FONTS_SNIPPET = """  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,600&display=swap" rel="stylesheet">"""

LUXURY_EDITORIAL_CSS = """<style id="bpa-luxury-editorial-system">
/* ==========================================================================
   1. HERO H1 CENTERING & CREDIBILITY STAT STRIP
   ========================================================================== */
h1.component-heading-1,
.article-hero-container h1 {
  max-width: none !important;
  margin-left: auto !important;
  margin-right: auto !important;
  text-align: center !important;
  font-family: 'Playfair Display', Georgia, 'Times New Roman', serif !important;
  font-weight: 700 !important;
  letter-spacing: -0.02em !important;
  line-height: 1.16 !important;
  color: #0f172a !important;
}

.article-hero-container .component-breadcrumb-rich-text,
.article-hero-container .paragraph-26 {
  text-align: center !important;
}

.article-hero-container .div-block-37 {
  justify-content: center !important;
}

.bpa-hero-credibility-bar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 10px 18px;
  max-width: 880px;
  margin: 18px auto 10px auto;
  padding: 12px 20px;
  background: linear-gradient(to right, #faf8f5, #ffffff, #faf8f5);
  border: 1px solid #e6e1da;
  border-top: 2px solid #c5a059;
  border-radius: 12px;
  box-shadow: 0 6px 20px -8px rgba(15, 23, 42, 0.06);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.bpa-cred-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12.5px;
  font-weight: 600;
  color: #334155;
  line-height: 1.3;
}

.bpa-cred-pill strong {
  color: #0f172a;
  font-weight: 800;
}

.bpa-cred-dot {
  color: #c5a059;
  font-weight: 900;
}

.bpa-cred-link {
  font-size: 12px;
  font-weight: 700;
  color: #9a7b38 !important;
  text-decoration: underline !important;
  text-underline-offset: 3px;
  white-space: nowrap;
}

.bpa-cred-link:hover {
  color: #0f172a !important;
}

/* ==========================================================================
   2. LUXURY EDITORIAL COMPARISON CARDS (.bpa-deck-wrap & .bpa-card)
   ========================================================================== */
.bpa-deck-wrap {
  width: 100%;
  max-width: 1240px !important;
  margin: 36px auto !important;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  color: #1e293b;
  -webkit-font-smoothing: antialiased;
  display: flex;
  flex-direction: column;
  gap: 24px !important;
}

.bpa-section-header {
  text-align: center;
  margin-bottom: 8px;
}

.bpa-section-title {
  font-family: 'Playfair Display', Georgia, 'Times New Roman', serif !important;
  font-size: clamp(26px, 3.2vw, 36px) !important;
  font-weight: 700 !important;
  color: #0f172a !important;
  margin: 0 0 8px 0 !important;
  letter-spacing: -0.015em !important;
}

.bpa-section-sub {
  font-size: 14.5px !important;
  color: #64748b !important;
  margin: 0 !important;
}

.bpa-card {
  background: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
  border-radius: 16px !important;
  box-shadow: 0 12px 32px -8px rgba(15, 23, 42, 0.06), 0 2px 6px rgba(15, 23, 42, 0.03) !important;
  overflow: hidden;
  transition: box-shadow 0.25s ease, border-color 0.25s ease, transform 0.2s ease !important;
}

.bpa-card:hover {
  border-color: #cbd5e1 !important;
  box-shadow: 0 20px 44px -12px rgba(15, 23, 42, 0.11), 0 4px 12px rgba(15, 23, 42, 0.04) !important;
}

.bpa-main {
  display: grid;
  grid-template-columns: 350px 1fr 210px;
  gap: 28px;
  padding: 24px 26px;
  align-items: center;
}

.bpa-media {
  position: relative;
  width: 100%;
  height: 235px;
  border-radius: 12px;
  overflow: hidden;
  background: #0f172a;
}

.bpa-slider {
  display: flex;
  width: 100%;
  height: 100%;
  overflow-x: auto;
  overflow-y: hidden;
  scroll-snap-type: x mandatory;
  -webkit-overflow-scrolling: touch;
  overscroll-behavior-x: contain;
  touch-action: pan-y pinch-zoom;
  scrollbar-width: none;
  user-select: none;
  cursor: grab;
}

.bpa-slider:active {
  cursor: grabbing;
}

.bpa-slider::-webkit-scrollbar {
  display: none;
}

.bpa-slider img {
  flex: 0 0 100%;
  width: 100%;
  height: 100%;
  object-fit: cover;
  scroll-snap-align: start;
  scroll-snap-stop: always;
  user-select: none;
  -webkit-user-drag: none;
  pointer-events: none;
}

.bpa-nav-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 32px;
  height: 32px;
  background: rgba(255, 255, 255, 0.92);
  border: none;
  border-radius: 50%;
  font-size: 16px;
  font-weight: 700;
  color: #0f172a;
  cursor: pointer;
  z-index: 3;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
  transition: background 0.15s, transform 0.15s;
}

.bpa-nav-arrow:hover {
  background: #ffffff;
  transform: translateY(-50%) scale(1.08);
}

.bpa-nav-arrow.prev { left: 8px; }
.bpa-nav-arrow.next { right: 8px; }

.bpa-counter-pill {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: rgba(15, 23, 42, 0.78);
  color: #ffffff;
  font-size: 11px;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 12px;
  backdrop-filter: blur(4px);
  z-index: 3;
}

.bpa-rank-tag {
  position: absolute;
  top: 10px;
  left: 10px;
  background: #0f172a;
  color: #ffffff;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.6px;
  text-transform: uppercase;
  padding: 5px 11px;
  border-radius: 6px;
  z-index: 3;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
}

.bpa-info {
  display: flex;
  flex-direction: column;
  gap: 8px !important;
  min-width: 0;
}

.bpa-kicker {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 11.5px !important;
  font-weight: 800 !important;
  color: #9a7b38 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.12em !important;
  margin-bottom: 2px !important;
}

.bpa-title,
.bpa-headline {
  font-family: 'Playfair Display', Georgia, 'Times New Roman', serif !important;
  font-size: 20px !important;
  font-weight: 700 !important;
  color: #0f172a !important;
  line-height: 1.32 !important;
  letter-spacing: -0.01em !important;
  text-decoration: none !important;
  transition: color 0.15s ease !important;
  margin-bottom: 2px !important;
  display: block;
}

.bpa-title:hover,
.bpa-headline:hover {
  color: #9a7b38 !important;
  text-decoration: none !important;
}

/* Unified Rating & Multi-Platform Proof Box */
.bpa-proof,
.bpa-proof-bar {
  display: inline-flex !important;
  align-items: center !important;
  gap: 8px !important;
  flex-wrap: wrap !important;
  font-size: 13px !important;
  background: #f8fafc !important;
  border: 1px solid #e2e8f0 !important;
  border-bottom: none !important;
  border-radius: 10px 10px 0 0 !important;
  padding: 8px 12px 6px 12px !important;
  margin: 2px 0 0 0 !important;
  width: fit-content !important;
  max-width: 100% !important;
}

.bpa-stars,
.bpa-gold-stars {
  color: #d97706 !important;
  letter-spacing: 1px !important;
  font-size: 13.5px !important;
}

.bpa-score-text {
  font-weight: 800 !important;
  color: #0f172a !important;
  font-size: 13.5px !important;
}

.bpa-count-muted {
  font-size: 12px !important;
  color: #64748b !important;
}

.bpa-vchip,
.bpa-verified-chip {
  background: #ecfdf5 !important;
  color: #047857 !important;
  border: 1px solid #a7f3d0 !important;
  font-size: 11px !important;
  font-weight: 700 !important;
  padding: 2px 8px !important;
  border-radius: 999px !important;
  letter-spacing: 0.02em !important;
}

.bpa-channels {
  display: flex !important;
  align-items: center !important;
  gap: 14px !important;
  flex-wrap: wrap !important;
  background: #f8fafc !important;
  border: 1px solid #e2e8f0 !important;
  border-radius: 0 10px 10px 10px !important;
  padding: 6px 12px 8px 12px !important;
  margin-top: -9px !important;
  width: fit-content !important;
  max-width: 100% !important;
}

.bpa-ci,
.bpa-channel-item {
  display: inline-flex !important;
  align-items: center !important;
  gap: 5px !important;
  font-size: 12px !important;
  font-weight: 600 !important;
  color: #334155 !important;
}

.bpa-ci img,
.bpa-channel-item img {
  width: 15px !important;
  height: 15px !important;
  border-radius: 3px !important;
  object-fit: contain !important;
}

.bpa-ci i,
.bpa-channel-item i {
  display: inline-block;
  width: 15px;
  height: 15px;
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  border-radius: 3px;
  vertical-align: middle;
}

.bpa-ic-gyg { background-image: url("https://cdn.prod.website-files.com/60e43c7d6d05b671dff0dc1a/65350288cf6e222fd93f3745_getyourguide-icon.png"); }
.bpa-ic-ta { background-image: url("https://cdn.prod.website-files.com/652d0405192ba076b04f74a3/68f64414502d0348145b678e_tripadvisor-icon.avif"); }
.bpa-ic-viator { background-image: url("https://cdn.prod.website-files.com/60e43c7d6d05b671dff0dc1a/65350288cf6e222fd93f3747_viator-icon.png"); }

.bpa-ci strong,
.bpa-channel-item strong {
  color: #0f172a !important;
  font-weight: 800 !important;
}

.bpa-ci span,
.bpa-channel-item span {
  color: #64748b !important;
  font-weight: 500 !important;
}

/* Structured 2-Column Spec Grid */
.bpa-specs-row {
  display: grid !important;
  grid-template-columns: 1fr 1fr !important;
  gap: 7px 10px !important;
  margin-top: 6px !important;
  width: 100% !important;
}

.bpa-sp,
.bpa-spec-pill {
  background: #ffffff !important;
  color: #334155 !important;
  border: 1px solid #e2e8f0 !important;
  padding: 6px 10px !important;
  border-radius: 8px !important;
  font-size: 12px !important;
  font-weight: 600 !important;
  display: flex !important;
  align-items: center !important;
  gap: 6px !important;
  line-height: 1.3 !important;
  box-shadow: 0 1px 2px rgba(15, 23, 42, 0.02) !important;
}

/* If odd number of specs, let the last item span full width cleanly */
.bpa-specs-row .bpa-sp:last-child:nth-child(odd),
.bpa-specs-row .bpa-spec-pill:last-child:nth-child(odd) {
  grid-column: span 2 !important;
}

/* Warm Editorial "Best For" Callout */
.bpa-best-for {
  font-size: 12.5px !important;
  line-height: 1.5 !important;
  color: #334155 !important;
  background: linear-gradient(to right, #faf8f5, #ffffff) !important;
  border: 1px solid #ede8df !important;
  border-left: 3px solid #c5a059 !important;
  padding: 8px 12px !important;
  border-radius: 0 8px 8px 0 !important;
  margin-top: 6px !important;
}

.bpa-best-for strong {
  color: #0f172a !important;
  font-weight: 700 !important;
}

.bpa-cta-cell {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding-left: 22px;
  border-left: 1px solid #f1f5f9;
  height: 100%;
  text-align: center;
}

.bpa-price-num,
.bpa-price {
  font-size: 29px !important;
  font-weight: 900 !important;
  color: #0f172a !important;
  line-height: 1 !important;
}

.bpa-price-sub {
  font-size: 11.5px !important;
  color: #64748b !important;
  margin-top: 3px !important;
}

.bpa-book-button,
.bpa-btn {
  width: 100%;
  background: #0284c7 !important;
  color: #ffffff !important;
  padding: 12px 16px !important;
  border-radius: 9px !important;
  font-size: 13.5px !important;
  font-weight: 800 !important;
  text-decoration: none !important;
  text-align: center;
  box-shadow: 0 3px 10px rgba(2, 132, 199, 0.28) !important;
  transition: all 0.15s ease !important;
  display: inline-block;
}

.bpa-book-button:hover,
.bpa-btn:hover {
  background: #0369a1 !important;
  box-shadow: 0 6px 16px rgba(2, 132, 199, 0.38) !important;
  transform: translateY(-1px) !important;
  color: #ffffff !important;
}

.bpa-sublink {
  font-size: 12px !important;
  font-weight: 600 !important;
  color: #64748b !important;
  text-decoration: underline !important;
  transition: color 0.15s ease !important;
  cursor: pointer;
}

.bpa-sublink:hover {
  color: #0284c7 !important;
}

@media (max-width: 960px) {
  .bpa-main {
    grid-template-columns: 1fr !important;
    gap: 16px !important;
    padding: 18px !important;
  }
  .bpa-media {
    height: 230px !important;
  }
  .bpa-cta-cell {
    flex-direction: row !important;
    justify-content: space-between !important;
    border-left: none !important;
    border-top: 1px solid #f1f5f9 !important;
    padding-left: 0 !important;
    padding-top: 14px !important;
    width: 100% !important;
  }
  .bpa-book-button,
  .bpa-btn {
    width: auto !important;
    padding: 10px 20px !important;
  }
}

@media (max-width: 560px) {
  .bpa-title,
  .bpa-headline {
    font-size: 18px !important;
  }
  .bpa-specs-row {
    grid-template-columns: 1fr !important;
  }
  .bpa-specs-row .bpa-sp:last-child:nth-child(odd),
  .bpa-specs-row .bpa-spec-pill:last-child:nth-child(odd) {
    grid-column: span 1 !important;
  }
}

/* ==========================================================================
   3. 50/50 LUXURY EDITORIAL PROS & CONS ARCHITECTURE
   ========================================================================== */
.pro-con-box-wrapper {
  width: 100% !important;
  max-width: 100% !important;
  margin: 28px 0 36px 0 !important;
  padding: 0 !important;
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
}

.pro-con-box-wrapper > .w-layout-grid,
.pro-con-box-wrapper > .grid-15 {
  display: grid !important;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr) !important;
  gap: 22px !important;
  align-items: stretch !important;
  width: 100% !important;
}

@media (max-width: 767px) {
  .pro-con-box-wrapper > .w-layout-grid,
  .pro-con-box-wrapper > .grid-15 {
    grid-template-columns: 1fr !important;
    gap: 16px !important;
  }
}

.pro-con-box-pro-cell,
.pro-con-box-con-cell {
  background: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
  border-radius: 14px !important;
  padding: 24px 26px !important;
  box-shadow: 0 10px 28px -10px rgba(15, 23, 42, 0.06), 0 2px 6px rgba(15, 23, 42, 0.02) !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: flex-start !important;
  position: relative !important;
  overflow: hidden !important;
  height: 100% !important;
  box-sizing: border-box !important;
}

.pro-con-box-pro-cell {
  border-top: 4px solid #10b981 !important;
  background: linear-gradient(180deg, rgba(236, 253, 245, 0.45) 0%, #ffffff 65px) !important;
}

.pro-con-box-con-cell {
  border-top: 4px solid #f43f5e !important;
  background: linear-gradient(180deg, rgba(255, 241, 242, 0.45) 0%, #ffffff 65px) !important;
}

.pro-con-box-pro-cell .w-richtext,
.pro-con-box-con-cell .w-richtext {
  width: 100% !important;
  margin: 0 !important;
  padding: 0 !important;
}

.pro-con-box-pro-cell .w-richtext::before,
.pro-con-box-pro-cell .w-richtext::after,
.pro-con-box-con-cell .w-richtext::before,
.pro-con-box-con-cell .w-richtext::after {
  display: none !important;
}

/* Header Styling inside Pros & Cons */
.pro-con-box-pro-cell h3,
.pro-con-box-con-cell h3 {
  display: flex !important;
  align-items: center !important;
  gap: 10px !important;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
  font-size: 13px !important;
  font-weight: 800 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.1em !important;
  margin: 0 0 18px 0 !important;
  padding: 0 0 14px 0 !important;
  border-bottom: 1px solid #f1f5f9 !important;
  line-height: 1.2 !important;
}

.pro-con-box-pro-cell h3,
.pro-con-box-pro-cell h3 strong {
  color: #065f46 !important;
  font-weight: 800 !important;
}

.pro-con-box-con-cell h3,
.pro-con-box-con-cell h3 strong {
  color: #9f1239 !important;
  font-weight: 800 !important;
}

.pro-con-box-pro-cell h3::before {
  content: "✓" !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  width: 22px !important;
  height: 22px !important;
  border-radius: 50% !important;
  background: #22c55e !important;
  color: #ffffff !important;
  font-size: 12px !important;
  font-weight: 900 !important;
  flex-shrink: 0 !important;
  box-shadow: 0 2px 6px rgba(34, 197, 94, 0.3) !important;
}

.pro-con-box-con-cell h3::before {
  content: "✕" !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  width: 22px !important;
  height: 22px !important;
  border-radius: 50% !important;
  background: #f43f5e !important;
  color: #ffffff !important;
  font-size: 11px !important;
  font-weight: 900 !important;
  flex-shrink: 0 !important;
  box-shadow: 0 2px 6px rgba(244, 63, 94, 0.3) !important;
}

/* List Reset & Item Styling */
.pro-con-box-pro-cell ul,
.pro-con-box-con-cell ul {
  list-style: none !important;
  margin: 0 !important;
  padding: 0 !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 12px !important;
}

.pro-con-box-pro-cell li,
.pro-con-box-con-cell li {
  position: relative !important;
  padding-left: 28px !important;
  margin: 0 !important;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
  font-size: 14.5px !important;
  line-height: 1.55 !important;
  color: #334155 !important;
  list-style-type: none !important;
}

.pro-con-box-pro-cell li strong,
.pro-con-box-con-cell li strong {
  color: #0f172a !important;
  font-weight: 700 !important;
}

.pro-con-box-pro-cell li::before {
  content: "✓" !important;
  position: absolute !important;
  left: 0 !important;
  top: 2px !important;
  width: 18px !important;
  height: 18px !important;
  border-radius: 50% !important;
  background: #dcfce7 !important;
  color: #15803d !important;
  font-size: 11px !important;
  font-weight: 900 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  line-height: 1 !important;
}

.pro-con-box-con-cell li::before {
  content: "✕" !important;
  position: absolute !important;
  left: 0 !important;
  top: 2px !important;
  width: 18px !important;
  height: 18px !important;
  border-radius: 50% !important;
  background: #ffe4e6 !important;
  color: #be123c !important;
  font-size: 10px !important;
  font-weight: 900 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  line-height: 1 !important;
}

/* ==========================================================================
   4. HYBRID STICKY BAR & TOC BUTTON VERTICAL CENTERING
   ========================================================================== */
.hybrid-sticky-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 99990;
  background: rgba(15, 23, 42, 0.96);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border-top: 1px solid rgba(255, 255, 255, 0.12);
  padding: 10px 18px;
  transform: translateY(115%);
  opacity: 0;
  pointer-events: none;
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.25s ease;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.hybrid-sticky-bar.is-visible {
  transform: translateY(0);
  opacity: 1;
  pointer-events: auto;
}

.hybrid-bar-inner {
  max-width: 1120px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
}

.hybrid-toc-btn {
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 8px !important;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.18);
  color: #f8fafc;
  padding: 9px 14px;
  border-radius: 10px;
  font-size: 12.5px;
  font-weight: 700;
  line-height: 1 !important;
  cursor: pointer;
  white-space: nowrap;
  transition: background 0.15s ease;
}

.hybrid-toc-btn:hover {
  background: rgba(255, 255, 255, 0.18);
}

.hybrid-toc-btn svg {
  display: block !important;
  flex-shrink: 0 !important;
  margin: 0 !important;
}

.hybrid-toc-btn span {
  display: inline-block !important;
  line-height: 1 !important;
}

.hybrid-active-info {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
  flex: 1;
  color: #ffffff;
}

.hybrid-active-badge {
  background: #c5a059;
  color: #0f172a;
  font-size: 10.5px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 3px 7px;
  border-radius: 5px;
  white-space: nowrap;
}

.hybrid-active-title {
  font-size: 13.5px;
  font-weight: 700;
  color: #ffffff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.hybrid-active-price {
  font-size: 13px;
  font-weight: 800;
  color: #38bdf8;
  white-space: nowrap;
}

.hybrid-cta-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #0284c7;
  color: #ffffff !important;
  font-size: 13px;
  font-weight: 800;
  padding: 10px 18px;
  border-radius: 9px;
  text-decoration: none !important;
  white-space: nowrap;
  transition: background 0.15s ease, transform 0.15s ease;
  box-shadow: 0 3px 10px rgba(2, 132, 199, 0.35);
}

.hybrid-cta-btn:hover {
  background: #0369a1;
  transform: translateY(-1px);
}

/* Hybrid TOC Bottom Sheet Modal */
.hybrid-sheet-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(4px);
  z-index: 99995;
  display: none;
  align-items: flex-end;
  justify-content: center;
}

.hybrid-sheet-backdrop.is-open {
  display: flex;
}

.hybrid-sheet {
  background: #ffffff;
  width: 100%;
  max-width: 640px;
  max-height: 80vh;
  border-radius: 20px 20px 0 0;
  padding: 22px 24px 30px;
  overflow-y: auto;
  box-shadow: 0 -12px 40px rgba(15, 23, 42, 0.25);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.hybrid-sheet-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 14px;
  border-bottom: 1px solid #e2e8f0;
  margin-bottom: 14px;
}

.hybrid-sheet-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 20px;
  font-weight: 700;
  color: #0f172a;
  margin: 0;
}

.hybrid-sheet-close {
  background: #f1f5f9;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  font-size: 16px;
  font-weight: 700;
  color: #334155;
  cursor: pointer;
}

.hybrid-toc-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.hybrid-toc-link {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 11px 14px;
  border-radius: 10px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  color: #0f172a !important;
  text-decoration: none !important;
  font-size: 13.5px;
  font-weight: 600;
  transition: all 0.15s ease;
}

.hybrid-toc-link:hover {
  border-color: #c5a059;
  background: #faf8f5;
}

.hybrid-toc-link span.toc-price {
  font-size: 12px;
  font-weight: 800;
  color: #0284c7;
  white-space: nowrap;
}

@media (max-width: 640px) {
  .hybrid-active-badge { display: none; }
  .hybrid-toc-btn span { display: none; }
  .hybrid-toc-btn { padding: 9px 11px; }
}
/* Zero Yellow Banner Artefacts */
.h2-wrapper, .h2-wrapper-2, .h2-wrapper-3, .h2-wrapper-4 {
  background-color: transparent !important;
  box-shadow: none !important;
  padding: 0 !important;
  color: #0f172a !important;
}
.h2-wrapper h2, .h2-wrapper-2 h2, .h2-wrapper-3 h2, .h2-wrapper-4 h2,
.h2-wrapper *, .h2-wrapper-2 *, .h2-wrapper-3 *, .h2-wrapper-4 * {
  color: #0f172a !important;
}
</style>"""

HERO_CREDIBILITY_HTML = """<div class="bpa-hero-credibility-bar" role="region" aria-label="Editorial Testing Standards">
  <span class="bpa-cred-pill">🛡️ <strong>Zero Freebies:</strong> No Sponsored PR Sailings</span>
  <span class="bpa-cred-dot">•</span>
  <span class="bpa-cred-pill">🚢 <strong>40+ Danube Sailings:</strong> Field-Tested Firsthand</span>
  <span class="bpa-cred-dot">•</span>
  <span class="bpa-cred-pill">💳 <strong>100% Anonymous:</strong> Paid Out-of-Pocket</span>
  <span class="bpa-cred-dot">•</span>
  <a href="/about" class="bpa-cred-link">Our Testing Ethics →</a>
</div>"""


def normalize_pro_con_cells(html: str) -> str:
    """Convert <p>✔️ ...</p> and <br/> items inside .pro-con-box-pro-cell and .pro-con-box-con-cell into clean <ul><li> lists."""
    pattern = re.compile(
        r'(<div class="pro-con-box-(?:pro|con)-cell-rich-text-block w-richtext">\s*<h3>\s*<strong>(?:Pros|Cons):?</strong>)(?:\s*<br\s*/?>)*(\s*</h3>)(.*?)(</div>\s*</div>)',
        re.DOTALL
    )

    def repl(match):
        prefix = match.group(1) + match.group(2)
        body = match.group(3).strip()
        suffix = match.group(4)

        # If already converted to <ul><li> without leading checkmarks, clean up any leading emojis inside <li>
        raw_items = []
        if "<li" in body:
            for li_m in re.finditer(r"<li[^>]*>(.*?)</li>", body, re.DOTALL):
                raw_items.append(li_m.group(1))
        else:
            # Split by <p>...</p> and <br/>
            for p_m in re.finditer(r"<p[^>]*>(.*?)</p>", body, re.DOTALL):
                p_inner = p_m.group(1)
                parts = re.split(r"<br\s*/?>", p_inner, flags=re.IGNORECASE)
                raw_items.extend(parts)

        clean_lis = []
        for item in raw_items:
            txt = item.strip()
            if not txt:
                continue
            # Remove leading ✔️, ❌, ✔, ✖, ✗, • inside or outside <strong>
            txt = re.sub(r"^(\s*(?:<strong[^>]*>\s*)?)[✔️❌✔✖✗•\ufe0f]+\s*", r"\1", txt)
            txt = re.sub(r"^(&nbsp;|\xa0|\s)+", "", txt)
            if txt:
                clean_lis.append(f"<li>{txt}</li>")

        if not clean_lis:
            return match.group(0)

        return f"{prefix}<ul>{''.join(clean_lis)}</ul>{suffix}"

    return pattern.sub(repl, html)


def build_river_deck_and_sticky() -> str:
    """Build the 10-card River Cruises comparison deck + Hybrid Sticky Bar with valid semantic IDs."""
    from build_river_deck import cruises, ICON_URLS, ICON_ALTS, CDN

    anchor_map = {
        "#1-legenda": "#cruise-1-legenda",
        "#2-rubingroup": "#cruise-2-rubingroup",
        "#4-kisfaludy-historic-cruise": "#cruise-4-kisfaludy-historic-cruise",
        "#3-portum": "#cruise-3-portum",
        "#5-silverline-no-frills": "#cruise-5-silverline-no-frills",
        "#6-sunset-cocktail-cruise": "#cruise-6-sunset-cocktail-cruise",
        "#9-pizza-and-beer-cruise": "#cruise-9-pizza-and-beer-cruise",
        "#7-hk-dinner-cruise": "#cruise-7-hk-dinner-cruise",
        "#8-hk-drinks-cruise": "#cruise-8-hk-drinks-cruise",
        "#10-mahart": "#cruise-10-mahart",
    }

    cards_html = []
    toc_links_html = []
    js_cruises = []

    for c in cruises:
        sem_anchor = anchor_map.get(c["anchor"], c["anchor"])
        tot_imgs = 1 + len(c["more_imgs"])
        more_str = ",".join(c["more_imgs"])

        ch_items = []
        for ch_key, val, cnt in c["channels"]:
            ch_items.append(
                f'<div class="bpa-channel-item bpa-ci"><i class="bpa-ic-{ch_key}" title="{ICON_ALTS[ch_key]}"></i><strong>{val}</strong> <span>{cnt}</span></div>'
            )
        ch_html = "\n          ".join(ch_items)

        sp_items = [f'<span class="bpa-spec-pill bpa-sp">{s}</span>' for s in c["specs"]]
        sp_html = "\n          ".join(sp_items)

        card = f"""  <div class="bpa-card">
    <div class="bpa-main">
      <div class="bpa-media">
        <span class="bpa-rank-tag {c["badge_cls"]}">{c["badge"]}</span>
        <button type="button" class="bpa-nav-arrow prev" onclick="bpaSlide(this, -1)">‹</button>
        <button type="button" class="bpa-nav-arrow next" onclick="bpaSlide(this, 1)">›</button>
        <span class="bpa-counter-pill">1 / {tot_imgs}</span>
        <div class="bpa-slider" data-more="{more_str}" onscroll="bpaCount(this)">
          <img src="{CDN}{c["hero_img"]}" alt="{c["title"]}">
        </div>
      </div>
      <div class="bpa-info">
        <div class="bpa-kicker">{c["kicker"]}</div>
        <a href="{c["url"]}" target="_blank" rel="sponsored noopener" class="bpa-headline bpa-title">
          {c["title"]}
        </a>
        <div class="bpa-proof-bar bpa-proof">
          <span class="bpa-gold-stars bpa-stars">{c["stars"]}</span>
          <span class="bpa-score-text">{c["score"]}</span>
          <span class="bpa-count-muted">{c["reviews"]}</span>
          <span class="bpa-verified-chip bpa-vchip">✓ Personally Tested</span>
        </div>
        <div class="bpa-channels">
          {ch_html}
        </div>
        <div class="bpa-specs-row">
          {sp_html}
        </div>
        <div class="bpa-best-for">🎯 <strong>Best For:</strong> {c["best_for"]}</div>
      </div>
      <div class="bpa-cta-cell">
        <div><div class="bpa-price-num bpa-price">{c["price"]}</div><div class="bpa-price-sub">{c["price_sub"]}</div></div>
        <a href="{c["url"]}" target="_blank" rel="sponsored noopener" class="bpa-book-button bpa-btn">Book Now →</a>
        <a href="{sem_anchor}" class="bpa-sublink">Read Full Review ↓</a>
      </div>
    </div>
  </div>"""
        cards_html.append(card)

        toc_links_html.append(
            f'<a href="{sem_anchor}" class="hybrid-toc-link" onclick="closeHybridSheet()"><span><strong>#{c["rank"]}</strong> · {c["kicker"].split("•")[0].strip()} — {c["badge"].split(" ", 1)[-1]}</span><span class="toc-price">{c["price"]}</span></a>'
        )
        js_cruises.append(
            f'{{id:"{sem_anchor.lstrip("#")}",badge:"#{c["rank"]} PICK",title:{c["kicker"].split("•")[0].strip()!r},price:{c["price"]!r},url:{c["url"]!r}}}'
        )

    unwrap_river_css = """<style id="bpa-river-unwrap-css">
.div-block-27, .table-row-grey-3, .table-row-grey-3-copy {
  scroll-margin-top: 90px !important;
}
.w-tabs .tabs-menu,
.w-tabs .grid-cell-2,
.w-tabs .div-block-21,
.w-tabs .grid-cell-5,
.w-tabs .price-2,
.w-tabs .buy-button-read-full-review,
.w-tabs .div-block-47,
.w-tabs .faq-item-toggle,
.load-more {
  display: none !important;
}
.w-tabs .table-wrapper-2,
.w-tabs .table-2 {
  min-width: 0 !important;
  width: 100% !important;
  max-width: 1080px !important;
  margin: 0 auto !important;
  overflow: visible !important;
}
.w-tabs .table-row-grey-3,
.w-tabs .table-row-grey-3-copy {
  display: block !important;
  padding: 32px 28px !important;
  margin-bottom: 36px !important;
  background: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
  border-radius: 16px !important;
  box-shadow: 0 4px 20px rgba(15, 23, 42, 0.05) !important;
}
.w-tabs .grid-cell-3 {
  display: block !important;
  width: 100% !important;
  padding: 0 !important;
}
.w-tabs .faq-section,
.w-tabs .faq-container-2,
.w-tabs .faq-wrapper,
.w-tabs .faq-item,
.w-tabs nav.faq-content-wrap,
.w-tabs .faq-content-wrap.w-dropdown-list,
.w-tabs .w-dropdown-list,
.load-more-div {
  display: block !important;
  position: static !important;
  width: 100% !important;
  max-width: 100% !important;
  opacity: 1 !important;
  visibility: visible !important;
  overflow: visible !important;
  background: transparent !important;
  padding: 0 !important;
}
</style>"""

    sticky_and_js = f"""
<aside class="hybrid-sticky-bar" id="hybridStickyBar" aria-label="Quick Cruise Navigation & Booking">
  <div class="hybrid-bar-inner">
    <button type="button" class="hybrid-toc-btn" onclick="openHybridSheet()" aria-label="Jump to Cruise Review">
      <svg width="16" height="12" viewBox="0 0 20 14" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round">
        <line x1="2" y1="2" x2="18" y2="2"></line>
        <line x1="2" y1="7" x2="18" y2="7"></line>
        <line x1="2" y1="12" x2="18" y2="12"></line>
      </svg>
      <span>All 10 Cruises</span>
    </button>
    <div class="hybrid-active-info">
      <span class="hybrid-active-badge" id="hybridActiveBadge">#1 PICK</span>
      <span class="hybrid-active-title" id="hybridActiveTitle">Legenda City Cruises</span>
      <span class="hybrid-active-price" id="hybridActivePrice">€20–25</span>
    </div>
    <a href="https://legenda.hu/en?partner=38585" target="_blank" rel="sponsored noopener" class="hybrid-cta-btn" id="hybridActiveCta">
      Check Availability →
    </a>
  </div>
</aside>

<div class="hybrid-sheet-backdrop" id="hybridSheet" onclick="if(event.target===this)closeHybridSheet()">
  <div class="hybrid-sheet" role="dialog" aria-modal="true" aria-label="Jump to Any Danube River Cruise">
    <div class="hybrid-sheet-head">
      <h3 class="hybrid-sheet-title">Jump to Tested River Cruise</h3>
      <button type="button" class="hybrid-sheet-close" onclick="closeHybridSheet()" aria-label="Close">✕</button>
    </div>
    <div class="hybrid-toc-list">
      {"".join(toc_links_html)}
    </div>
  </div>
</div>

<script>
(function() {{
  const BPA_CDN = "https://cdn.prod.website-files.com/60e43c7d6d05b671dff0dc1a/";
  document.querySelectorAll(".bpa-slider[data-more]").forEach(c => {{
    const m = c.getAttribute("data-more").split(",");
    m.forEach(f => {{
      if (!f) return;
      const img = document.createElement("img");
      img.src = f.startsWith("http") ? f : BPA_CDN + f;
      img.loading = "lazy";
      img.alt = "Budapest Danube River Cruise";
      c.appendChild(img);
    }});
    c.removeAttribute("data-more");
    const tot = c.children.length;
    const cnt = c.parentElement.querySelector(".bpa-counter-pill");
    if (cnt) cnt.textContent = "1 / " + tot;
  }});

  window.bpaSlide = function(btn, dir) {{
    const c = btn.parentElement.querySelector(".bpa-slider");
    if (c) c.scrollBy({{ left: dir * c.offsetWidth, behavior: "smooth" }});
  }};

  window.bpaCount = function(c) {{
    if (c._ticking) return;
    c._ticking = true;
    requestAnimationFrame(() => {{
      const w = c.offsetWidth || 1;
      const tot = c.children.length;
      const idx = Math.min(tot, Math.max(1, Math.round(c.scrollLeft / w) + 1));
      const cnt = c.parentElement.querySelector(".bpa-counter-pill");
      if (cnt) cnt.textContent = idx + " / " + tot;
      c._ticking = false;
    }});
  }};

  window.openHybridSheet = function() {{
    const s = document.getElementById("hybridSheet");
    if (s) s.classList.add("is-open");
  }};
  window.closeHybridSheet = function() {{
    const s = document.getElementById("hybridSheet");
    if (s) s.classList.remove("is-open");
  }};

  const items = [{",".join(js_cruises)}];
  function onScroll() {{
    const bar = document.getElementById("hybridStickyBar");
    if (!bar) return;
    if (window.scrollY > 450) {{
      bar.classList.add("is-visible");
    }} else {{
      bar.classList.remove("is-visible");
      return;
    }}
    const vCenter = window.innerHeight * 0.45;
    let active = items[0];
    for (const item of items) {{
      const el = document.getElementById(item.id);
      if (el) {{
        const rect = el.getBoundingClientRect();
        if (rect.top <= vCenter) active = item;
      }}
    }}
    if (active) {{
      const b = document.getElementById("hybridActiveBadge");
      const t = document.getElementById("hybridActiveTitle");
      const p = document.getElementById("hybridActivePrice");
      const c = document.getElementById("hybridActiveCta");
      if (b) b.textContent = active.badge;
      if (t) t.textContent = active.title;
      if (p) p.textContent = active.price;
      if (c) c.href = active.url;
    }}
  }}
  window.addEventListener("scroll", onScroll, {{ passive: true }});
}})();
</script>"""

    return f"""{unwrap_river_css}
<div class="bpa-deck-wrap">
  <div class="bpa-section-header">
    <h2 class="bpa-section-title">Comparison — 10 Best Boat Tours &amp; River Cruises in Budapest (2026)</h2>
    <p class="bpa-section-sub">Personally field-tested on the Danube • Verified prices, dock locations &amp; unretouched photos</p>
  </div>
{chr(10).join(cards_html)}
</div>
{sticky_and_js}"""


def build_dinner_deck_and_sticky() -> str:
    """Build the 7-card Dinner Cruises comparison deck + Hybrid Sticky Bar with valid semantic IDs."""
    deck7_raw = (ROOT / "comparison_deck_7_cruises.html").read_text(encoding="utf-8")
    start = deck7_raw.find('<div class="bpa-deck-wrap">')
    end = deck7_raw.find("<script>", start)
    deck_html = deck7_raw[start:end].strip()

    # Upgrade classes inside deck_html so both .bpa-headline/.bpa-title, .bpa-proof-bar/.bpa-proof, etc. are present
    deck_html = deck_html.replace('class="bpa-headline"', 'class="bpa-headline bpa-title"')
    deck_html = deck_html.replace('class="bpa-proof-bar"', 'class="bpa-proof-bar bpa-proof"')
    deck_html = deck_html.replace('class="bpa-gold-stars"', 'class="bpa-gold-stars bpa-stars"')
    deck_html = deck_html.replace('class="bpa-verified-chip"', 'class="bpa-verified-chip bpa-vchip"')
    deck_html = deck_html.replace('class="bpa-channel-item"', 'class="bpa-channel-item bpa-ci"')
    deck_html = deck_html.replace('class="bpa-spec-pill"', 'class="bpa-spec-pill bpa-sp"')
    deck_html = deck_html.replace('class="bpa-price-num"', 'class="bpa-price-num bpa-price"')
    deck_html = deck_html.replace('class="bpa-book-button"', 'class="bpa-book-button bpa-btn"')

    # Map old digits-first anchors to dinner.html's clean semantic IDs
    replacements = {
        'href="#1-Legenda"': 'href="#cruise-1-legenda"',
        'href="#2-Silverline-no-show"': 'href="#cruise-2-silverline-no-show"',
        'href="#3-Silverline-folklore"': 'href="#cruise-3-silverline-folklore"',
        'href="#4-silverline-piano"': 'href="#cruise-4-silverline-piano"',
        'href="#5-Hungaria-Koncert"': 'href="#cruise-5-hungaria-koncert"',
        'href="#6-Eurama"': 'href="#cruise-6-eurama"',
    }
    for old_a, new_a in replacements.items():
        deck_html = deck_html.replace(old_a, new_a)

    dinner_extra_css = """<style id="bpa-dinner-deck-css">
.comparison-table .w-tabs {
  display: none !important;
}
.div-block-27 {
  scroll-margin-top: 90px !important;
}
</style>"""

    dinner_sticky_and_js = """
<aside class="hybrid-sticky-bar" id="hybridStickyBar" aria-label="Quick Dinner Cruise Navigation & Booking">
  <div class="hybrid-bar-inner">
    <button type="button" class="hybrid-toc-btn" onclick="openHybridSheet()" aria-label="Jump to Dinner Cruise Review">
      <svg width="16" height="12" viewBox="0 0 20 14" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round">
        <line x1="2" y1="2" x2="18" y2="2"></line>
        <line x1="2" y1="7" x2="18" y2="7"></line>
        <line x1="2" y1="12" x2="18" y2="12"></line>
      </svg>
      <span>All 7 Dinner Cruises</span>
    </button>
    <div class="hybrid-active-info">
      <span class="hybrid-active-badge" id="hybridActiveBadge">#1 PICK</span>
      <span class="hybrid-active-title" id="hybridActiveTitle">Legenda Candlelit Dinner Cruise</span>
      <span class="hybrid-active-price" id="hybridActivePrice">€110</span>
    </div>
    <a href="https://legenda.hu/en?partner=38585" target="_blank" rel="sponsored noopener" class="hybrid-cta-btn" id="hybridActiveCta">
      Reserve Table →
    </a>
  </div>
</aside>

<div class="hybrid-sheet-backdrop" id="hybridSheet" onclick="if(event.target===this)closeHybridSheet()">
  <div class="hybrid-sheet" role="dialog" aria-modal="true" aria-label="Jump to Any Budapest Dinner Cruise">
    <div class="hybrid-sheet-head">
      <h3 class="hybrid-sheet-title">Jump to Tested Dinner Cruise</h3>
      <button type="button" class="hybrid-sheet-close" onclick="closeHybridSheet()" aria-label="Close">✕</button>
    </div>
    <div class="hybrid-toc-list">
      <a href="#cruise-1-legenda" class="hybrid-toc-link" onclick="closeHybridSheet()"><span><strong>#1</strong> · Legenda Candlelit 4-Course Dinner (Best Overall)</span><span class="toc-price">€110</span></a>
      <a href="#cruise-2-silverline-no-show" class="hybrid-toc-link" onclick="closeHybridSheet()"><span><strong>#2</strong> · Silverline 4-Course Dinner Without Show (Best Value)</span><span class="toc-price">€74</span></a>
      <a href="#cruise-3-silverline-folklore" class="hybrid-toc-link" onclick="closeHybridSheet()"><span><strong>#3</strong> · Silverline 4-Course Dinner + Folk Operetta</span><span class="toc-price">€91</span></a>
      <a href="#cruise-4-silverline-piano" class="hybrid-toc-link" onclick="closeHybridSheet()"><span><strong>#4</strong> · Silverline 4-Course Dinner + Piano Battle</span><span class="toc-price">€91</span></a>
      <a href="#cruise-5-hungaria-koncert" class="hybrid-toc-link" onclick="closeHybridSheet()"><span><strong>#5</strong> · Hungária Koncert 12-Course Buffet + Folk Show</span><span class="toc-price">€79</span></a>
      <a href="#cruise-6-eurama" class="hybrid-toc-link" onclick="closeHybridSheet()"><span><strong>#6</strong> · Eurama 4-Course Dinner + Gypsy Music</span><span class="toc-price">€90</span></a>
    </div>
  </div>
</div>

<script>
(function() {
  const BPA_CDN = "https://cdn.prod.website-files.com/60e43c7d6d05b671dff0dc1a/";
  document.querySelectorAll(".bpa-slider[data-more]").forEach(c => {
    const m = c.getAttribute("data-more").split(",");
    m.forEach(f => {
      if (!f) return;
      const img = document.createElement("img");
      img.src = f.startsWith("http") ? f : BPA_CDN + f;
      img.loading = "lazy";
      img.alt = "Budapest Dinner Cruise";
      c.appendChild(img);
    });
    c.removeAttribute("data-more");
    const tot = c.children.length;
    const cnt = c.parentElement.querySelector(".bpa-counter-pill");
    if (cnt) cnt.textContent = "1 / " + tot;
  });

  window.bpaSlide = function(btn, dir) {
    const c = btn.parentElement.querySelector(".bpa-slider");
    if (c) c.scrollBy({ left: dir * c.offsetWidth, behavior: "smooth" });
  };

  window.bpaCount = function(c) {
    if (c._ticking) return;
    c._ticking = true;
    requestAnimationFrame(() => {
      const w = c.offsetWidth || 1;
      const tot = c.children.length;
      const idx = Math.min(tot, Math.max(1, Math.round(c.scrollLeft / w) + 1));
      const cnt = c.parentElement.querySelector(".bpa-counter-pill");
      if (cnt) cnt.textContent = idx + " / " + tot;
      c._ticking = false;
    });
  };

  window.openHybridSheet = function() {
    const s = document.getElementById("hybridSheet");
    if (s) s.classList.add("is-open");
  };
  window.closeHybridSheet = function() {
    const s = document.getElementById("hybridSheet");
    if (s) s.classList.remove("is-open");
  };

  const items = [
    {id:"cruise-1-legenda",badge:"#1 PICK",title:"Legenda Candlelit 4-Course Dinner",price:"€110",url:"https://legenda.hu/en?partner=38585"},
    {id:"cruise-2-silverline-no-show",badge:"#2 VALUE",title:"Silverline 4-Course (No Show)",price:"€74",url:"https://budapestrivercruise.eu/product/dinner-lights/?code=bpadventures"},
    {id:"cruise-3-silverline-folklore",badge:"#3 FOLK SHOW",title:"Silverline Folklore & Operetta",price:"€91",url:"https://budapestrivercruise.eu/product/budapest-danube-dinner-cruise/?code=bpadventures"},
    {id:"cruise-4-silverline-piano",badge:"#4 PIANO DUEL",title:"Silverline Piano Battle Dinner",price:"€91",url:"https://budapestrivercruise.eu/product/dinner-cruise-piano-battle-show/?code=bpadventures"},
    {id:"cruise-5-hungaria-koncert",badge:"#5 BUFFET",title:"Hungária Koncert 12-Course Buffet",price:"€79",url:"https://budapestxplore.com/en/budapest-dinner-and-cruise-with-live-music-xpZDZlZTExMN?affi=6876"},
    {id:"cruise-6-eurama",badge:"#6 CENTRAL",title:"Eurama 4-Course Dinner & Folk",price:"€90",url:"https://www.getyourguide.com/budapest-l29/budapest-evening-cruise-and-dinner-with-champagne-t408084/?partner_id=YS414AJ&utm_medium=online_publisher&cmp=eng-dinner-cruises-budapest-eurama-reviews&mkt_cmp=true"}
  ];

  function onScroll() {
    const bar = document.getElementById("hybridStickyBar");
    if (!bar) return;
    if (window.scrollY > 450) {
      bar.classList.add("is-visible");
    } else {
      bar.classList.remove("is-visible");
      return;
    }
    const vCenter = window.innerHeight * 0.45;
    let active = items[0];
    for (const item of items) {
      const el = document.getElementById(item.id);
      if (el) {
        const rect = el.getBoundingClientRect();
        if (rect.top <= vCenter) active = item;
      }
    }
    if (active) {
      const b = document.getElementById("hybridActiveBadge");
      const t = document.getElementById("hybridActiveTitle");
      const p = document.getElementById("hybridActivePrice");
      const c = document.getElementById("hybridActiveCta");
      if (b) b.textContent = active.badge;
      if (t) t.textContent = active.title;
      if (p) p.textContent = active.price;
      if (c) c.href = active.url;
    }
  }
  window.addEventListener("scroll", onScroll, { passive: true });
})();
</script>"""

    return f"{dinner_extra_css}\n{deck_html}\n{dinner_sticky_and_js}"


def upgrade_river_file(fname: str, river_deck_block: str):
    path = ROOT / fname
    html = path.read_text(encoding="utf-8")

    # Remove previous injection if re-running
    html = re.sub(r'<style id="bpa-luxury-editorial-system">.*?</style>\s*', '', html, flags=re.DOTALL)
    html = re.sub(r'<div class="bpa-hero-credibility-bar".*?</div>\s*', '', html, flags=re.DOTALL)
    html = re.sub(r'<style id="bpa-river-unwrap-css">.*?</script>\s*', '', html, flags=re.DOTALL)

    # 1. Inject Playfair Display Google Fonts & Luxury Editorial CSS before </head>
    if "Playfair+Display" not in html:
        html = html.replace("</head>", f"{GOOGLE_FONTS_SNIPPET}\n{LUXURY_EDITORIAL_CSS}\n</head>", 1)
    else:
        html = html.replace("</head>", f"{LUXURY_EDITORIAL_CSS}\n</head>", 1)

    # 2. Inject Hero Credibility Bar inside .article-hero-container right before <div class="divider"></div></address>
    target_hero_end = '<div class="divider"></div></address>'
    if target_hero_end in html:
        html = html.replace(target_hero_end, f'{HERO_CREDIBILITY_HTML}<div class="divider"></div></address>', 1)

    # 3. Inject 10-card River Comparison Deck before the summary table
    if '<div class="container w-container"><h2 class="heading-30"> Summary — Top 10 River Cruises in Budapest</h2>' in html:
        anchor = '<div class="container w-container"><h2 class="heading-30"> Summary — Top 10 River Cruises in Budapest</h2>'
        html = html.replace(anchor, f"{river_deck_block}\n{anchor}", 1)
    elif '<div id="river-cruises-quick-summary" class="h2-wrapper">' in html:
        anchor = '<div id="river-cruises-quick-summary" class="h2-wrapper">'
        html = html.replace(anchor, f"{river_deck_block}\n{anchor}", 1)

    # 4. Normalize all .pro-con-box-pro-cell and .pro-con-box-con-cell items into clean <ul><li>
    html = normalize_pro_con_cells(html)

    # 5. Strip any zero-width joiners just in case
    html = html.replace("\u200d", "")

    path.write_text(html, encoding="utf-8")
    print(f"Upgraded {fname} (size={len(html)})")


def upgrade_dinner_file(dinner_deck_block: str):
    path = ROOT / "dinner.html"
    html = path.read_text(encoding="utf-8")

    # Remove previous injection if re-running
    html = re.sub(r'<style id="bpa-luxury-editorial-system">.*?</style>\s*', '', html, flags=re.DOTALL)
    html = re.sub(r'<div class="bpa-hero-credibility-bar".*?</div>\s*', '', html, flags=re.DOTALL)
    html = re.sub(r'<style id="bpa-dinner-deck-css">.*?</script>\s*', '', html, flags=re.DOTALL)

    # 1. Inject Playfair Display Google Fonts & Luxury Editorial CSS before </head>
    if "Playfair+Display" not in html:
        html = html.replace("</head>", f"{GOOGLE_FONTS_SNIPPET}\n{LUXURY_EDITORIAL_CSS}\n</head>", 1)
    else:
        html = html.replace("</head>", f"{LUXURY_EDITORIAL_CSS}\n</head>", 1)

    # 2. Inject Hero Credibility Bar inside .article-hero-container right before <div class="divider"></div></div>
    target_hero_end = '<div class="divider"></div></div><div class="container w-container">'
    if target_hero_end in html:
        html = html.replace(
            target_hero_end,
            f'{HERO_CREDIBILITY_HTML}<div class="divider"></div></div><div class="container w-container">',
            1
        )

    # 3. Inject 7-card Dinner Comparison Deck right after the #dinner-cruises-list h2-wrapper
    target_comp = '<div id="dinner-cruises-list" class="h2-wrapper"><h2 id="quick-summary-river-cruises-budapest" class="heading-30">Comparison — 7 Best Dinner Cruises in Budapest</h2><a href="#dinner-cruises-list" class="view-all-button w-inline-block"><div>View All</div></a></div>'
    if target_comp in html:
        html = html.replace(target_comp, f"{target_comp}\n{dinner_deck_block}", 1)

    # 4. Normalize all .pro-con-box-pro-cell and .pro-con-box-con-cell items into clean <ul><li>
    html = normalize_pro_con_cells(html)

    # 5. Strip any zero-width joiners
    html = html.replace("\u200d", "")

    path.write_text(html, encoding="utf-8")
    print(f"Upgraded dinner.html (size={len(html)})")


def upgrade_candlelit_file():
    path = ROOT / "candlelit-dinner-cruise.html"
    html = path.read_text(encoding="utf-8")

    # Remove previous injection if re-running
    html = re.sub(r'<style id="bpa-luxury-editorial-system">.*?</style>\s*', '', html, flags=re.DOTALL)

    # 1. Add Playfair Display font link & Luxury Editorial CSS in <head>
    if "Playfair+Display" not in html:
        html = html.replace(
            '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">',
            '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Playfair+Display:ital,wght@0,600;0,700;1,600&display=swap" rel="stylesheet">'
        )
    html = html.replace("</head>", f"{LUXURY_EDITORIAL_CSS}\n</head>", 1)

    # 2. Add /about link in top nav & footer nav if not present
    if 'href="/about"' not in html:
        html = html.replace(
            '<a href="https://www.budapestadventures.com/legenda-city-cruises" class="hover:text-slate-900 transition">Legenda Terminal</a>',
            '<a href="https://www.budapestadventures.com/legenda-city-cruises" class="hover:text-slate-900 transition">Legenda Terminal</a>\n        <a href="/about" class="hover:text-slate-900 transition">About &amp; Ethics</a>'
        )
        html = html.replace(
            '<a href="https://www.budapestadventures.com/legenda-city-cruises" class="hover:text-white transition">Legenda Terminal</a>',
            '<a href="https://www.budapestadventures.com/legenda-city-cruises" class="hover:text-white transition">Legenda Terminal</a>\n        <a href="/about" class="hover:text-white transition">About &amp; Ethics</a>'
        )

    # 3. Center H1 with Playfair Display class & add Hero Credibility Stat Bar
    html = html.replace(
        '<h1 class="text-3xl sm:text-4xl lg:text-5xl font-black text-slate-950 tracking-tight leading-tight mb-4">',
        '<h1 class="component-heading-1 text-3xl sm:text-4xl lg:text-5xl font-black text-slate-950 tracking-tight leading-tight mb-4">'
    )
    if 'aria-label="Editorial Testing Standards"' not in html:
        marker = "<!-- Verified Salon Hero Photo -->"
        html = html.replace(marker, f"{HERO_CREDIBILITY_HTML}\n\n    {marker}", 1)

    # 4. Upgrade Quick Verdict Card to include a Luxury Editorial .bpa-card summary block & 2-col .bpa-specs-row
    old_verdict_pattern = re.compile(
        r"<!-- Quick Verdict Card -->.*?<!-- Pros & Cons Grid -->",
        re.DOTALL
    )
    new_verdict_and_card = """<!-- Quick Verdict & Luxury Editorial Tested Card -->
    <div id="verdict-summary" class="bpa-card mb-10" style="padding: 26px 28px;">
      <div class="bpa-kicker">Legenda City Cruises • 📍 Vigadó tér Dock 7 • Flagship Evening Sailing</div>
      <a href="https://legenda.hu/en/ticket-purchase?partner=38585" target="_blank" rel="noopener" class="bpa-headline bpa-title">
        Legenda 4-Course Romantic Candlelit Dinner Cruise With Live Salon Music
      </a>
      <div class="bpa-proof-bar bpa-proof">
        <span class="bpa-gold-stars bpa-stars">★★★★★</span>
        <span class="bpa-score-text">4.8 / 5.0</span>
        <span class="bpa-count-muted">(3,200+ Verified Reviews)</span>
        <span class="bpa-verified-chip bpa-vchip">✓ Personally Tested Out-of-Pocket</span>
      </div>
      <div class="bpa-channels">
        <div class="bpa-channel-item bpa-ci"><i class="bpa-ic-gyg" title="GetYourGuide"></i><strong>4.8</strong> <span>(1,840+)</span></div>
        <div class="bpa-channel-item bpa-ci"><i class="bpa-ic-ta" title="Tripadvisor"></i><strong>4.7</strong> <span>(890+)</span></div>
        <div class="bpa-channel-item bpa-ci"><i class="bpa-ic-viator" title="Viator"></i><strong>4.8</strong> <span>(470+)</span></div>
      </div>
      <div class="bpa-specs-row">
        <span class="bpa-spec-pill bpa-sp">🍽️ 4-Course Plated Gourmet Menu</span>
        <span class="bpa-spec-pill bpa-sp">⏱️ 2.5 Hours (Full Extended Circuit)</span>
        <span class="bpa-spec-pill bpa-sp">🎷 Live Acoustic Violin &amp; Piano</span>
        <span class="bpa-spec-pill bpa-sp">🥂 Welcome Sparkling Wine Included</span>
        <span class="bpa-spec-pill bpa-sp">📸 Anti-Glare Dimmed Glass Salon at Dock 7</span>
      </div>
      <div class="bpa-best-for">🎯 <strong>The Quick Verdict:</strong> If you want high gastronomic standards, professional seated table service, and zero tourist-trap gimmicks, Legenda is unmatched. Crisp linens, warm dimmed cabin lighting for reflection-free night Parliament photos, and fresh plated courses cooked on board.</div>
      <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:16px; margin-top:18px; padding-top:16px; border-top:1px solid #f1f5f9;">
        <div>
          <span class="bpa-price-num bpa-price">€110</span>
          <span class="bpa-price-sub" style="margin-left:8px;">per adult · 4-course all-inclusive · free 24h cancellation</span>
        </div>
        <a href="https://legenda.hu/en/ticket-purchase?partner=38585" target="_blank" rel="noopener" class="bpa-book-button bpa-btn" style="width:auto; padding:12px 26px !important;">
          Book Legenda Direct →
        </a>
      </div>
    </div>

    <!-- Pros & Cons Grid -->"""
    html = old_verdict_pattern.sub(new_verdict_and_card, html, count=1)

    # 5. Upgrade Pros & Cons Grid to the 50/50 Luxury Editorial Pros & Cons Architecture
    old_pro_con_pattern = re.compile(
        r"<!-- Pros & Cons Grid -->.*?<!-- Editorial Tested Content Body -->",
        re.DOTALL
    )
    new_pro_con_block = """<!-- Pros & Cons Grid (50/50 Luxury Editorial Architecture) -->
    <div id="pros-and-cons" class="pro-con-box-wrapper">
      <div class="w-layout-grid grid-15">
        <div class="pro-con-box-pro-cell">
          <div class="pro-con-box-pro-cell-rich-text-block w-richtext">
            <h3><strong>Pros:</strong></h3>
            <ul>
              <li><strong>Gourmet Kitchen Quality:</strong> Plated à la carte dining freshly prepared on board rather than mass-heated chafing pans.</li>
              <li><strong>Anti-Glare Lighting:</strong> Interior salon lights dim to ambient candle warmth upon departure, allowing crystal-clear night photography through panoramic glass windows.</li>
              <li><strong>Acoustic Live Music:</strong> Live violin and piano salon duo provides elegant background melodies that never drown out private conversation.</li>
              <li><strong>Dedicated Private Tables:</strong> Every booking receives an assigned private table with white tablecloths and warm candle lighting.</li>
            </ul>
          </div>
        </div>
        <div class="pro-con-box-con-cell">
          <div class="pro-con-box-con-cell-rich-text-block w-richtext">
            <h3><strong>Cons:</strong></h3>
            <ul>
              <li><strong>Higher Price Point:</strong> At €110 per adult, it carries a premium over buffet booze boats, though the culinary quality justifies the cost.</li>
              <li><strong>Early Sell-Outs:</strong> High season (April–October) sunset departures frequently sell out 3–5 days in advance; advance reservation is critical.</li>
              <li><strong>Enclosed Salon During Meal:</strong> Dinner is served in a climate-controlled glass salon; guests step onto the open viewing deck between courses.</li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Editorial Tested Content Body -->"""
    html = old_pro_con_pattern.sub(new_pro_con_block, html, count=1)

    # 6. Add semantic IDs to the 4 section h2s in candlelit-dinner-cruise.html and add Hybrid Sticky TOC Bar
    for _ in range(3):
        html = re.sub(r'<span id="(?:boarding-dock-7|gourmet-menu|navigation-route|dock-7-directions)">(.*?)</span>', r'\1', html)
    html = html.replace('1. Boarding Experience at Dock 7', '<span id="boarding-dock-7">1. Boarding Experience at Dock 7</span>')
    html = html.replace('2. The 4-Course Gourmet Dinner Menu', '<span id="gourmet-menu">2. The 4-Course Gourmet Dinner Menu</span>')
    html = html.replace('3. Scenic 2.5-Hour Navigation Route', '<span id="navigation-route">3. Scenic 2.5-Hour Navigation Route</span>')
    html = html.replace('4. How to Reach Dock 7 (Directions)', '<span id="dock-7-directions">4. How to Reach Dock 7 (Directions)</span>')

    if "hybridStickyBar" not in html:
        candlelit_sticky = """
  <!-- Hybrid Sticky Bar & TOC Sheet -->
  <aside class="hybrid-sticky-bar is-visible" id="hybridStickyBar" aria-label="Quick Review Navigation & Booking">
    <div class="hybrid-bar-inner">
      <button type="button" class="hybrid-toc-btn" onclick="document.getElementById('hybridSheet').classList.add('is-open')" aria-label="Review Sections">
        <svg width="16" height="12" viewBox="0 0 20 14" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round">
          <line x1="2" y1="2" x2="18" y2="2"></line>
          <line x1="2" y1="7" x2="18" y2="7"></line>
          <line x1="2" y1="12" x2="18" y2="12"></line>
        </svg>
        <span>Review Sections</span>
      </button>
      <div class="hybrid-active-info">
        <span class="hybrid-active-badge">#1 PICK</span>
        <span class="hybrid-active-title">Legenda Candlelit Dinner Cruise (Dock 7)</span>
        <span class="hybrid-active-price">€110</span>
      </div>
      <a href="https://legenda.hu/en/ticket-purchase?partner=38585" target="_blank" rel="noopener" class="hybrid-cta-btn">
        Book Dock 7 Direct →
      </a>
    </div>
  </aside>

  <div class="hybrid-sheet-backdrop" id="hybridSheet" onclick="if(event.target===this)this.classList.remove('is-open')">
    <div class="hybrid-sheet" role="dialog" aria-modal="true" aria-label="Review Sections">
      <div class="hybrid-sheet-head">
        <h3 class="hybrid-sheet-title">Candlelit Dinner Review Sections</h3>
        <button type="button" class="hybrid-sheet-close" onclick="document.getElementById('hybridSheet').classList.remove('is-open')" aria-label="Close">✕</button>
      </div>
      <div class="hybrid-toc-list">
        <a href="#verdict-summary" class="hybrid-toc-link" onclick="document.getElementById('hybridSheet').classList.remove('is-open')"><span><strong>01</strong> · Quick Verdict &amp; Tested Ratings</span><span class="toc-price">4.8 ★</span></a>
        <a href="#pros-and-cons" class="hybrid-toc-link" onclick="document.getElementById('hybridSheet').classList.remove('is-open')"><span><strong>02</strong> · 50/50 Tested Pros &amp; Cons</span><span class="toc-price">Audit</span></a>
        <a href="#boarding-dock-7" class="hybrid-toc-link" onclick="document.getElementById('hybridSheet').classList.remove('is-open')"><span><strong>03</strong> · Boarding Experience at Dock 7</span><span class="toc-price">Pier 7</span></a>
        <a href="#gourmet-menu" class="hybrid-toc-link" onclick="document.getElementById('hybridSheet').classList.remove('is-open')"><span><strong>04</strong> · 4-Course Plated Gourmet Menu</span><span class="toc-price">Menu</span></a>
        <a href="#navigation-route" class="hybrid-toc-link" onclick="document.getElementById('hybridSheet').classList.remove('is-open')"><span><strong>05</strong> · Scenic 2.5-Hour Danube Route</span><span class="toc-price">2.5h</span></a>
        <a href="#dock-7-directions" class="hybrid-toc-link" onclick="document.getElementById('hybridSheet').classList.remove('is-open')"><span><strong>06</strong> · How to Reach Vigadó tér Dock 7</span><span class="toc-price">Map</span></a>
      </div>
    </div>
  </div>
"""
        html = html.replace("<!-- Unified Tracking Script -->", f"{candlelit_sticky}\n  <!-- Unified Tracking Script -->", 1)

    html = html.replace("\u200d", "")
    path.write_text(html, encoding="utf-8")
    print(f"Upgraded candlelit-dinner-cruise.html (size={len(html)})")


def main():
    river_deck_block = build_river_deck_and_sticky()
    dinner_deck_block = build_dinner_deck_and_sticky()

    for fname in ["index.html", "river.html", "river-ecom.html"]:
        upgrade_river_file(fname, river_deck_block)

    upgrade_dinner_file(dinner_deck_block)
    upgrade_candlelit_file()


if __name__ == "__main__":
    main()
