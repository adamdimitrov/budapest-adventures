#!/usr/bin/env python3
"""Standardize static pages (index.html, about.html, contact.html, budapest-card-is-it-worth-it.html)
with the canonical TCD-standard Luxury Editorial Navbar, Footer, and Assets."""

import re
from bs4 import BeautifulSoup

NAVBAR_HTML = """  <!-- NAVIGATION HEADER -->
  <header class="ltt-navbar" role="banner">
    <div class="ltt-nav-inner">
      <a aria-label="BUDAPEST ADVENTURES Homepage" class="ltt-brand" href="/">
        <img alt="BUDAPEST ADVENTURES Logo" class="ltt-brand-logo" height="36" src="/assets/budapest-adventures-logo.png" width="36"/>
        <span class="ltt-brand-text">BUDAPEST ADVENTURES</span>
      </a>

      <nav aria-label="Primary Navigation" class="ltt-nav-links">
        <div class="ltt-nav-dropdown" id="lttExploreDropdown">
          <button aria-expanded="false" aria-haspopup="true" class="ltt-nav-link ltt-dropdown-btn" type="button">
            <span>Danube Cruises</span>
            <svg class="ltt-chevron" fill="none" height="12" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" viewBox="0 0 24 24" width="12">
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </button>
          <div class="ltt-mega-menu" role="menu">
            <div class="ltt-mega-col">
              <div class="ltt-mega-head">DANUBE RIVER CRUISES</div>
              <a class="ltt-mega-item" href="/best-budapest-river-cruises">
                <span class="ltt-mega-icon">🚢</span>
                <div>
                  <strong>Top 10 River Cruises</strong>
                  <p>Personally tested day &amp; night boats</p>
                </div>
              </a>
              <a class="ltt-mega-item" href="/best-dinner-cruises-budapest">
                <span class="ltt-mega-icon">🍷</span>
                <div>
                  <strong>Top 7 Dinner Cruises</strong>
                  <p>4-course dining, folklore &amp; live piano</p>
                </div>
              </a>
              <a class="ltt-mega-item" href="/unlimited-prosecco-cruises-budapest">
                <span class="ltt-mega-icon">🥂</span>
                <div>
                  <strong>Unlimited Prosecco Cruises</strong>
                  <p>Bottomless sparkling wine &amp; music</p>
                </div>
              </a>
              <a class="ltt-mega-item" href="/best-night-cruises-budapest">
                <span class="ltt-mega-icon">✨</span>
                <div>
                  <strong>Best Night Cruises</strong>
                  <p>Illuminated Parliament evening trips</p>
                </div>
              </a>
              <a class="ltt-mega-item" href="/best-private-boat-tours-budapest">
                <span class="ltt-mega-icon">🛥️</span>
                <div>
                  <strong>Private Boat Tours</strong>
                  <p>Exclusive Danube charters &amp; speedboats</p>
                </div>
              </a>
              <a class="ltt-mega-item" href="/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest">
                <span class="ltt-mega-icon">🕯️</span>
                <div>
                  <strong>Legenda Candlelit Review</strong>
                  <p>In-depth test of Budapest's #1 dinner boat</p>
                </div>
              </a>
            </div>
            <div class="ltt-mega-col">
              <div class="ltt-mega-head">CITY ATTRACTIONS &amp; SPAS</div>
              <a class="ltt-mega-item" href="/budapest-card-is-it-worth-it">
                <span class="ltt-mega-icon">💳</span>
                <div>
                  <strong>Budapest Card Calculator</strong>
                  <p>Interactive value audit across 94 sights</p>
                </div>
              </a>
              <a class="ltt-mega-item" href="/thermal-baths-budapest">
                <span class="ltt-mega-icon">♨️</span>
                <div>
                  <strong>8 Best Thermal Baths</strong>
                  <p>Széchenyi, Gellért, Rudas &amp; Lukács tested</p>
                </div>
              </a>
              <a class="ltt-mega-item" href="/best-walking-tours-budapest">
                <span class="ltt-mega-icon">🚶</span>
                <div>
                  <strong>Best Walking Tours</strong>
                  <p>Castle District &amp; Jewish Quarter food walks</p>
                </div>
              </a>
              <a class="ltt-mega-item" href="/best-hostels-budapest">
                <span class="ltt-mega-icon">🛏️</span>
                <div>
                  <strong>Best Hostels in Budapest</strong>
                  <p>Social, boutique &amp; budget stays audited</p>
                </div>
              </a>
            </div>
          </div>
        </div>
        <a class="ltt-nav-link" href="/best-budapest-river-cruises">River Cruises</a>
        <a class="ltt-nav-link" href="/best-dinner-cruises-budapest">Dinner Cruises</a>
        <a class="ltt-nav-link" href="/budapest-card-is-it-worth-it">Budapest Card</a>
        <a class="ltt-nav-link" href="/about">About</a>
        <a class="ltt-nav-link" href="/contact">Contact</a>
      </nav>

      <div class="ltt-nav-right">
        <button aria-controls="lttMobileDrawer" aria-expanded="false" aria-label="Toggle Menu" class="ltt-hamburger" id="lttNavToggle" type="button">
          <span class="ltt-hamburger-bar"></span>
          <span class="ltt-hamburger-bar"></span>
          <span class="ltt-hamburger-bar"></span>
        </button>
      </div>
    </div>

    <!-- Mobile Drawer -->
    <div aria-hidden="true" class="ltt-mobile-drawer" id="lttMobileDrawer">
      <div class="ltt-drawer-content">
        <div class="ltt-mobile-section">
          <div class="ltt-mobile-label">Danube Cruises &amp; Guides</div>
          <a class="ltt-mobile-link" href="/best-budapest-river-cruises">
            <span>🚢 Top 10 River Cruises</span>
            <span style="font-size:10px; font-weight:800; background:#dfa732; color:#fff; padding:2px 7px; border-radius:9999px;">TOP PICK</span>
          </a>
          <a class="ltt-mobile-link" href="/best-dinner-cruises-budapest">
            <span>🍷 Top 7 Dinner Cruises</span>
          </a>
          <a class="ltt-mobile-link" href="/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest">
            <span>🕯️ Legenda Candlelit Review</span>
          </a>
          <a class="ltt-mobile-link" href="/unlimited-prosecco-cruises-budapest">
            <span>🥂 Unlimited Prosecco Cruises</span>
          </a>
          <a class="ltt-mobile-link" href="/best-night-cruises-budapest">
            <span>✨ Best Night Cruises</span>
          </a>
          <a class="ltt-mobile-link" href="/best-private-boat-tours-budapest">
            <span>🛥️ Private Boat Tours</span>
          </a>
        </div>
        <div class="ltt-mobile-section">
          <div class="ltt-mobile-label">City Attractions &amp; Spas</div>
          <a class="ltt-mobile-link" href="/budapest-card-is-it-worth-it">
            <span>💳 Budapest Card Calculator</span>
            <span style="font-size:10px; font-weight:800; background:#0284c7; color:#fff; padding:2px 7px; border-radius:9999px;">INTERACTIVE</span>
          </a>
          <a class="ltt-mobile-link" href="/thermal-baths-budapest">
            <span>♨️ 8 Best Thermal Baths</span>
          </a>
          <a class="ltt-mobile-link" href="/best-walking-tours-budapest">
            <span>🚶 Best Walking Tours</span>
          </a>
          <a class="ltt-mobile-link" href="/best-hostels-budapest">
            <span>🛏️ Best Hostels in Budapest</span>
          </a>
        </div>
        <div class="ltt-mobile-section">
          <div class="ltt-mobile-label">Editorial</div>
          <a class="ltt-mobile-link" href="/about">
            <span>📖 About &amp; Ethics</span>
          </a>
          <a class="ltt-mobile-link" href="/contact">
            <span>✉️ Contact</span>
          </a>
        </div>
      </div>
    </div>
  </header>"""

FOOTER_HTML = """  <!-- 6. CANONICAL DARK LUXURY FOOTER -->
  <footer class="footer-dark ltt-footer" role="contentinfo">
    <div class="footer-wrapper">
      <div class="footer-content">
        <div>
          <div class="footer-brand-title">
            <a href="/" style="color: #fff; text-decoration: none; display: inline-flex; align-items: center; gap: 10px;">
              <img src="/assets/budapest-adventures-logo.png" alt="Budapest Adventures Logo" width="28" height="28" style="border-radius: 50%; display: inline-block; flex-shrink: 0;"/>
              <span>BUDAPEST ADVENTURES</span>
            </a>
          </div>
          <p class="footer-brand-desc">
            Independent, undercover field testing of the Danube's premier sightseeing and dinner cruises. Based locally in Budapest, we pay our own fares, test audio guides, and inspect every pier dock so you avoid tourist traps.
          </p>
        </div>

        <div>
          <div class="footer-col-title">Flagship Budapest Guides</div>
          <div class="footer-links-list">
            <a href="/best-budapest-river-cruises" class="footer-link-item">10 Best Danube River Cruises</a>
            <a href="/best-dinner-cruises-budapest" class="footer-link-item">7 Best Dinner Cruises in Budapest</a>
            <a href="/budapest-card-is-it-worth-it" class="footer-link-item">Budapest Card Value Calculator (2026)</a>
            <a href="/thermal-baths-budapest" class="footer-link-item">8 Best Budapest Thermal Baths</a>
            <a href="/best-night-cruises-budapest" class="footer-link-item">Best Night Cruises in Budapest</a>
            <a href="/unlimited-prosecco-cruises-budapest" class="footer-link-item">Unlimited Prosecco Cruises</a>
            <a href="/best-private-boat-tours-budapest" class="footer-link-item">Best Private Boat Tours</a>
            <a href="/best-walking-tours-budapest" class="footer-link-item">Best Walking Tours in Budapest</a>
            <a href="/best-hostels-budapest" class="footer-link-item">Best Hostels in Budapest</a>
          </div>
        </div>

        <div>
          <div class="footer-col-title">Trust &amp; Company</div>
          <div class="footer-links-list">
            <a href="/about" class="footer-link-item">About Adam Dimitrov</a>
            <a href="/about#ethics" class="footer-link-item">Our 5-Point Testing Ethics Charter</a>
            <a href="/about#manifesto" class="footer-link-item">The Anti-Influencer Manifesto</a>
            <a href="/contact" class="footer-link-item">Contact Editorial Desk</a>
          </div>
        </div>
      </div>

      <div class="grey-divider"></div>

      <div class="legal-wrapper">
        <div>© 2026 BudapestAdventures.com. All rights reserved.</div>
        <div style="color: rgba(255,255,255,0.45); font-size: 13px;">
          Personally tested undercover in Budapest • 100% anonymous bookings • Zero sponsored PR sailings
        </div>
      </div>
    </div>
  </footer>"""

SCRIPT_HTML = """  <script>
    (function() {
      'use strict';
      var toggle = document.getElementById('lttNavToggle');
      var drawer = document.getElementById('lttMobileDrawer');
      var dropdown = document.getElementById('lttExploreDropdown');
      var dropBtn = dropdown ? dropdown.querySelector('.ltt-dropdown-btn') : null;

      if (toggle && drawer) {
        toggle.addEventListener('click', function(e) {
          e.stopPropagation();
          var isOpen = drawer.classList.contains('is-open');
          if (isOpen) {
            drawer.classList.remove('is-open');
            toggle.classList.remove('is-active');
            toggle.setAttribute('aria-expanded', 'false');
            drawer.setAttribute('aria-hidden', 'true');
          } else {
            drawer.classList.add('is-open');
            toggle.classList.add('is-active');
            toggle.setAttribute('aria-expanded', 'true');
            drawer.setAttribute('aria-hidden', 'false');
          }
        });

        drawer.querySelectorAll('a').forEach(function(link) {
          link.addEventListener('click', function() {
            drawer.classList.remove('is-open');
            toggle.classList.remove('is-active');
            toggle.setAttribute('aria-expanded', 'false');
            drawer.setAttribute('aria-hidden', 'true');
          });
        });
      }

      if (dropdown && !dropdown._bound) {
        dropdown._bound = true;
        var closeTimeout = null;

        function openMenu() {
          if (closeTimeout) {
            clearTimeout(closeTimeout);
            closeTimeout = null;
          }
          dropdown.classList.add('is-open');
          if (dropBtn) dropBtn.setAttribute('aria-expanded', 'true');
        }

        function closeMenuWithGrace(delay) {
          if (closeTimeout) clearTimeout(closeTimeout);
          closeTimeout = setTimeout(function() {
            dropdown.classList.remove('is-open');
            if (dropBtn) dropBtn.setAttribute('aria-expanded', 'false');
          }, delay !== undefined ? delay : 350);
        }

        dropdown.addEventListener('mouseenter', openMenu);
        dropdown.addEventListener('mouseleave', function() {
          closeMenuWithGrace(350);
        });

        if (dropBtn) {
          dropBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            if (dropdown.classList.contains('is-open')) {
              closeMenuWithGrace(0);
            } else {
              openMenu();
            }
          });
        }
      }

      document.addEventListener('click', function(e) {
        if (drawer && drawer.classList.contains('is-open') && !drawer.contains(e.target) && (!toggle || !toggle.contains(e.target))) {
          drawer.classList.remove('is-open');
          if (toggle) {
            toggle.classList.remove('is-active');
            toggle.setAttribute('aria-expanded', 'false');
          }
          drawer.setAttribute('aria-hidden', 'true');
        }
        if (dropdown && dropdown.classList.contains('is-open') && !dropdown.contains(e.target)) {
          dropdown.classList.remove('is-open');
          if (dropBtn) dropBtn.setAttribute('aria-expanded', 'false');
        }
      });
    })();
  </script>"""

def update_index_page():
    path = '/Users/adamdimitrov/Development/budapest-adventures/index.html'
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Favicons
    html = re.sub(
        r'<link rel="icon"[^>]*>',
        '<link rel="icon" type="image/png" href="/assets/budapest-adventures-logo.png"/>',
        html
    )
    html = re.sub(
        r'<link rel="shortcut icon"[^>]*>',
        '<link rel="shortcut icon" type="image/png" href="/assets/budapest-adventures-logo.png"/>',
        html
    )
    html = re.sub(
        r'<link rel="apple-touch-icon"[^>]*>',
        '<link rel="apple-touch-icon" href="/assets/budapest-adventures-logo.png"/>',
        html
    )

    # Broken Walking Tours image
    html = html.replace(
        'https://cdn.prod.website-files.com/60e43c7d6d05b671dff0dc1a/60e557f1b50ff47e8fc4ca54_Webclip-8.png',
        'https://cdn.prod.website-files.com/60e43c7d6d05b671dff0dc1a/64f8c324f5839b9f2092fef3_walking-tours-featured-image.webp'
    )

    # Remove conflicting inline navbar CSS (between "/* Navbar */" and "/* Hero */")
    html = re.sub(
        r'/\*\s*Navbar\s*\*/.*?(?=/\*\s*Hero\s*\*/)',
        '',
        html,
        flags=re.DOTALL
    )

    # Replace header and mobile drawer
    html = re.sub(
        r'<header class="ltt-navbar".*?</div>\s*</div>\s*(?=<main>)',
        NAVBAR_HTML + '\n\n',
        html,
        flags=re.DOTALL
    )

    # Add quick jump pill for Budapest Card if not present
    if '/budapest-card-is-it-worth-it' not in html.split('<div class="ltt-quick-links">')[1].split('</div>')[0]:
        html = html.replace(
            '<a href="/thermal-baths-budapest" class="ltt-quick-btn">♨️ Thermal Baths</a>',
            '<a href="/thermal-baths-budapest" class="ltt-quick-btn">♨️ Thermal Baths</a>\n          <a href="/budapest-card-is-it-worth-it" class="ltt-quick-btn">💳 Budapest Card Calculator</a>'
        )

    # Add Budapest Card and Hostels cards to guides grid if not present
    if '<!-- Guide 8: Budapest Card Calculator -->' not in html:
        card_cards_html = """          <!-- Guide 8: Budapest Card Calculator -->
          <a href="/budapest-card-is-it-worth-it" class="ltt-guide-card">
            <div class="ltt-guide-img-wrap">
              <span class="ltt-guide-tag">💳 VALUE CALCULATOR</span>
              <img src="https://cdn.prod.website-files.com/60e43c7d6d05b671dff0dc1a/64823741c9e79f16c66f949c_2-budapest-card.webp" alt="Official Budapest Card Pass with Free Public Transport & Museums" class="ltt-guide-img" loading="lazy"/>
            </div>
            <div class="ltt-guide-content">
              <div>
                <div class="ltt-guide-kicker">Interactive Tool • 94 Sights Audited</div>
                <h3 class="ltt-guide-title">Budapest Card: Is It Worth It? (2026 Interactive Calculator)</h3>
                <p class="ltt-guide-excerpt">
                  Calculate whether the official city card actually saves you money. Check your custom sightseeing itinerary against official 2026 museum and bath prices.
                </p>
                <div class="ltt-guide-specs">
                  <span class="ltt-guide-sp">🧮 Live Value Calculator</span>
                  <span class="ltt-guide-sp">🚇 Free Public Transit</span>
                </div>
              </div>
              <div class="ltt-guide-footer">
                <span class="ltt-guide-price">From €33 (24h–120h)</span>
                <span class="ltt-guide-btn">Calculate Savings →</span>
              </div>
            </div>
          </a>

          <!-- Guide 9: Hostels -->
          <a href="/best-hostels-budapest" class="ltt-guide-card">
            <div class="ltt-guide-img-wrap">
              <span class="ltt-guide-tag">🛏️ BUDGET & SOCIAL</span>
              <img src="https://cdn.prod.website-files.com/60e43c7d6d05b671dff0dc1a/649187aa6fba10735a62132d_06-best-hostels-in-budapest.webp" alt="Best Hostels in Budapest for Solo Travelers and Groups" class="ltt-guide-img" loading="lazy"/>
            </div>
            <div class="ltt-guide-content">
              <div>
                <div class="ltt-guide-kicker">Where to Stay • 8 Hostels Audited</div>
                <h3 class="ltt-guide-title">8 Best Hostels in Budapest (Personally Tested)</h3>
                <p class="ltt-guide-excerpt">
                  From social party hostels in District VII to boutique quiet pods for remote workers and solo travelers.
                </p>
                <div class="ltt-guide-specs">
                  <span class="ltt-guide-sp">🔒 Safe Pods & Lockers</span>
                  <span class="ltt-guide-sp">📍 District VII & V Mapped</span>
                </div>
              </div>
              <div class="ltt-guide-footer">
                <span class="ltt-guide-price">From €15 / night</span>
                <span class="ltt-guide-btn">Read Guide →</span>
              </div>
            </div>
          </a>"""
        # Insert before closing </div> of ltt-guides-grid
        # Guide 7 ends with </a> \n </div> \n </div> \n </section>
        html = re.sub(
            r'(<!-- Guide 7: Walking Tours -->.*?</a>)\s*(?=</div>\s*</div>\s*</section>)',
            r'\1\n\n' + card_cards_html + '\n',
            html,
            flags=re.DOTALL
        )

    # Replace footer
    html = re.sub(
        r'<footer class="footer-dark.*?(?=<script>)',
        FOOTER_HTML + '\n\n  ',
        html,
        flags=re.DOTALL
    )

    # Replace runtime script
    html = re.sub(
        r'<script>\s*\(function\(\)\s*\{.*?\}\)\(\);\s*</script>',
        SCRIPT_HTML,
        html,
        flags=re.DOTALL
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("SUCCESS: index.html updated")

def update_about_contact(page_name):
    path = f'/Users/adamdimitrov/Development/budapest-adventures/{page_name}'
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Favicons
    html = re.sub(
        r'<link rel="icon"[^>]*>',
        '<link rel="icon" type="image/png" href="/assets/budapest-adventures-logo.png"/>',
        html
    )
    html = re.sub(
        r'<link rel="shortcut icon"[^>]*>',
        '<link rel="shortcut icon" type="image/png" href="/assets/budapest-adventures-logo.png"/>',
        html
    )
    html = re.sub(
        r'<link rel="apple-touch-icon"[^>]*>',
        '<link rel="apple-touch-icon" href="/assets/budapest-adventures-logo.png"/>',
        html
    )

    # Remove conflicting inline navbar CSS if present
    html = re.sub(
        r'/\*\s*Navbar\s*\*/.*?(?=/\*\s*Hero\s*\*/|/\*\s*About\s*\*/|/\*\s*Contact\s*\*/|\.ltt-about|\.ltt-contact|\.ltt-hero)',
        '',
        html,
        flags=re.DOTALL
    )

    # Replace header and mobile drawer
    html = re.sub(
        r'<header class="ltt-navbar".*?</div>\s*</div>\s*(?=<main>)',
        NAVBAR_HTML + '\n\n',
        html,
        flags=re.DOTALL
    )

    # Replace footer
    html = re.sub(
        r'<footer class="footer-dark.*?(?=<script>)',
        FOOTER_HTML + '\n\n  ',
        html,
        flags=re.DOTALL
    )

    # Replace runtime script
    html = re.sub(
        r'<script>\s*\(function\(\)\s*\{.*?\}\)\(\);\s*</script>',
        SCRIPT_HTML,
        html,
        flags=re.DOTALL
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"SUCCESS: {page_name} updated")

def update_budapest_card_page():
    path = '/Users/adamdimitrov/Development/budapest-adventures/budapest-card-is-it-worth-it.html'
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update Favicon & Stylesheet in head
    head_inject = """  <!-- Local Favicon Assets -->
  <link rel="icon" type="image/png" href="/assets/budapest-adventures-logo.png"/>
  <link rel="shortcut icon" type="image/png" href="/assets/budapest-adventures-logo.png"/>
  <link rel="apple-touch-icon" href="/assets/budapest-adventures-logo.png"/>

  <!-- Google Fonts & Luxury Editorial Stylesheet -->
  <link rel="stylesheet" href="/css/editorial-luxury.css"/>"""

    if '/css/editorial-luxury.css' not in html:
        html = html.replace('<link rel="canonical" href="https://www.budapestadventures.com/budapest-card-is-it-worth-it">', '<link rel="canonical" href="https://www.budapestadventures.com/budapest-card-is-it-worth-it">\n' + head_inject)

    # 2. Replace .top-header with canonical NAVBAR_HTML
    html = re.sub(
        r'<!-- Top Global Header -->\s*<header class="top-header">.*?</header>',
        NAVBAR_HTML,
        html,
        flags=re.DOTALL
    )

    # 3. Add canonical FOOTER_HTML before calculator script if no footer exists
    if '<footer class="footer-dark' not in html:
        html = html.replace(
            '  <script>\n    const CALCULATOR_DATA = {',
            FOOTER_HTML + '\n\n  ' + SCRIPT_HTML + '\n\n  <script>\n    const CALCULATOR_DATA = {'
        )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("SUCCESS: budapest-card-is-it-worth-it.html updated")

if __name__ == '__main__':
    update_index_page()
    update_about_contact('about.html')
    update_about_contact('contact.html')
    update_budapest_card_page()
