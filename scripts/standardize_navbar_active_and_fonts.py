#!/usr/bin/env python3
"""
Standardize navbar active states and fonts across all Budapest Adventures pages.
- Unifies font-family to 'Plus Jakarta Sans' across all navbar elements (eliminating Open Sans vs Plus Jakarta Sans discrepancies).
- Sets consistent font-weight: 600 for inactive items, 700 for active items.
- Statically marks active page in both desktop navbar and mobile drawer.
- Adds dynamic path-matching runtime inside ltt-nav-script for bulletproof live indication.
"""

import os
import glob
import re

BASE_DIR = "/Users/adamdimitrov/Development/budapest-adventures"

NAVBAR_CSS_PATCH = """
.ltt-navbar,
.ltt-navbar button,
.ltt-navbar a,
.ltt-navbar span,
.ltt-mobile-drawer,
.ltt-mobile-drawer * {
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
.ltt-nav-link {
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
  font-weight: 600 !important;
}
.ltt-nav-link.active,
.ltt-nav-link[aria-current="page"] {
  color: #0f172a !important;
  background: #f1f5f9 !important;
  font-weight: 700 !important;
  box-shadow: inset 0 -2px 0 #0f172a !important;
}
.ltt-mobile-link {
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
  font-weight: 600 !important;
}
.ltt-mobile-link.active,
.ltt-mobile-link[aria-current="page"] {
  color: #0f172a !important;
  background: #f1f5f9 !important;
  font-weight: 700 !important;
  border-left: 3px solid #0f172a !important;
}
"""

RUNTIME_JS = """
  // CANONICAL ACTIVE PAGE HIGHLIGHTER
  try {
    var rawPath = (window.location.pathname || '/').replace(/\\/$/, '') || '/';
    var normPath = rawPath.replace(/\\.html$/, '');
    
    var isRiver = (normPath.indexOf('river-cruise') !== -1 || normPath.indexOf('setahajozas-a-dunan-budapest') !== -1 || normPath.indexOf('bootsfahrten-dunau') !== -1 || normPath.indexOf('croisieres-danube') !== -1 || normPath.indexOf('riecne-plavby') !== -1 || normPath.indexOf('rejsy-dunaju') !== -1 || normPath.indexOf('rechnyye-kruizy') !== -1) && normPath.indexOf('dinner') === -1 && normPath.indexOf('vacsoraval') === -1 && normPath.indexOf('abendessen') === -1;
    var isDinner = normPath.indexOf('dinner-cruise') !== -1 || normPath.indexOf('vacsoraval') !== -1 || normPath.indexOf('candlelit') !== -1 || normPath.indexOf('abendessen') !== -1 || normPath.indexOf('diner-croisiere') !== -1 || normPath.indexOf('cena-danubio') !== -1 || normPath.indexOf('kolacja') !== -1 || normPath.indexOf('vecera-plavby') !== -1;
    var isCard = normPath.indexOf('budapest-card') !== -1;
    var isAbout = normPath.indexOf('/about') !== -1 || normPath.indexOf('/rolunk') !== -1 || normPath.indexOf('/körülbelül') !== -1;
    var isContact = normPath.indexOf('/contact') !== -1 || normPath.indexOf('/kapcsolat') !== -1 || normPath.indexOf('/érintkezés') !== -1;

    var navLinks = document.querySelectorAll('.ltt-nav-links .ltt-nav-link:not(.ltt-dropdown-btn), .ltt-mobile-drawer .ltt-mobile-link');
    navLinks.forEach(function(el) {
      var href = el.getAttribute('href');
      if (!href) return;
      var hClean = href.replace(/\\/$/, '').replace(/\\.html$/, '') || '/';
      
      var match = false;
      if (normPath === hClean) {
        match = true;
      } else if (isRiver && (hClean.indexOf('river-cruise') !== -1 || hClean.indexOf('setahajozas-a-dunan-budapest') !== -1 || hClean.indexOf('bootsfahrten-dunau') !== -1)) {
        match = true;
      } else if (isDinner && (hClean.indexOf('dinner-cruise') !== -1 || hClean.indexOf('setahajozas-a-dunan-vacsoraval') !== -1 || hClean.indexOf('bootsfahrten-mit-abendessen') !== -1)) {
        match = true;
      } else if (isCard && hClean.indexOf('budapest-card') !== -1) {
        match = true;
      } else if (isAbout && (hClean.indexOf('/about') !== -1 || hClean.indexOf('/rolunk') !== -1)) {
        match = true;
      } else if (isContact && (hClean.indexOf('/contact') !== -1 || hClean.indexOf('/kapcsolat') !== -1)) {
        match = true;
      }
      
      if (match) {
        el.classList.add('active');
        el.setAttribute('aria-current', 'page');
      } else if (hClean !== '/' && !hClean.match(/^\\/[a-z]{2}$/)) {
        el.classList.remove('active');
        el.removeAttribute('aria-current');
      }
    });
  } catch(e) {}
"""

def process_file(fpath: str):
    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()
    
    if "ltt-navbar" not in html:
        return False

    orig_html = html
    rel_path = os.path.relpath(fpath, BASE_DIR).replace("\\", "/")
    
    # 1. Determine category
    is_river = ("river-cruise" in rel_path or "setahajozas-a-dunan-budapest" in rel_path or "bootsfahrten-dunau" in rel_path or "croisieres-danube" in rel_path or "riecne-plavby" in rel_path or "rejsy-dunaju" in rel_path or "river.html" in rel_path) and "dinner" not in rel_path and "vacsoraval" not in rel_path and "abendessen" not in rel_path
    is_dinner = "dinner-cruise" in rel_path or "setahajozas-a-dunan-vacsoraval" in rel_path or "candlelit" in rel_path or "abendessen" in rel_path or "diner-croisiere" in rel_path or "cena-danubio" in rel_path or "dinner.html" in rel_path
    is_card = "budapest-card" in rel_path
    is_about = "about" in rel_path or "rolunk" in rel_path or "körülbelül" in rel_path
    is_contact = "contact" in rel_path or "kapcsolat" in rel_path or "érintkezés" in rel_path
    
    # 2. Inject CSS patch if not already present
    if "CANONICAL_NAVBAR_UNIFIED_FONTS" not in html:
        style_inject = f"<style id=\"CANONICAL_NAVBAR_UNIFIED_FONTS\">{NAVBAR_CSS_PATCH}</style>"
        if "</head>" in html:
            html = html.replace("</head>", f"{style_inject}\n</head>", 1)
        elif "<body" in html:
            html = html.replace("<body", f"{style_inject}\n<body", 1)

    # 3. Update static active states on desktop nav links
    # Reset existing active on ltt-nav-links first (except if needed)
    def clean_nav_link(match):
        attrs = match.group(1)
        # remove active from class
        attrs = re.sub(r'class="([^"]*)\bactive\b([^"]*)"', r'class="\1\2"', attrs)
        attrs = re.sub(r'\s+class="\s*"', '', attrs)
        attrs = re.sub(r'class="\s+([^"]+)"', r'class="\1"', attrs)
        attrs = re.sub(r'class="([^"]+)\s+"', r'class="\1"', attrs)
        # remove aria-current="page"
        attrs = re.sub(r'\s+aria-current="page"', '', attrs)
        return f'<a {attrs.strip()}>'

    # 4. Target specific link to make active
    if is_river:
        # Match river nav link and make active
        # Matches any <a ...href="...river-cruise..."...> or setahajozas-a-dunan-budapest
        def make_river_active(match):
            tag = match.group(0)
            if 'active' not in tag:
                tag = re.sub(r'class="([^"]*)"', r'class="\1 active"', tag)
                tag = tag.replace('<a ', '<a aria-current="page" ')
            return tag
        html = re.sub(r'<a\s+class="ltt-nav-link"[^>]*href="[^"]*(?:river-cruise|setahajozas-a-dunan-budapest|bootsfahrten-dunau|croisieres-danube|riecne-plavby|rejsy-dunaju)[^"]*"[^>]*>', make_river_active, html)
        html = re.sub(r'<a\s+aria-current="page"\s+class="ltt-nav-link"[^>]*href="[^"]*(?:river-cruise|setahajozas-a-dunan-budapest|bootsfahrten-dunau|croisieres-danube|riecne-plavby|rejsy-dunaju)[^"]*"[^>]*>', make_river_active, html)

    elif is_dinner:
        def make_dinner_active(match):
            tag = match.group(0)
            if 'active' not in tag:
                tag = re.sub(r'class="([^"]*)"', r'class="\1 active"', tag)
                tag = tag.replace('<a ', '<a aria-current="page" ')
            return tag
        html = re.sub(r'<a\s+class="ltt-nav-link"[^>]*href="[^"]*(?:dinner-cruise|setahajozas-a-dunan-vacsoraval|bootsfahrten-mit-abendessen|diner-croisiere|vecera-plavby)[^"]*"[^>]*>', make_dinner_active, html)
        html = re.sub(r'<a\s+aria-current="page"\s+class="ltt-nav-link"[^>]*href="[^"]*(?:dinner-cruise|setahajozas-a-dunan-vacsoraval|bootsfahrten-mit-abendessen|diner-croisiere|vecera-plavby)[^"]*"[^>]*>', make_dinner_active, html)

    elif is_card:
        def make_card_active(match):
            tag = match.group(0)
            if 'active' not in tag:
                tag = re.sub(r'class="([^"]*)"', r'class="\1 active"', tag)
                tag = tag.replace('<a ', '<a aria-current="page" ')
            return tag
        html = re.sub(r'<a\s+class="ltt-nav-link"[^>]*href="[^"]*budapest-card[^"]*"[^>]*>', make_card_active, html)

    elif is_about:
        def make_about_active(match):
            tag = match.group(0)
            if 'active' not in tag:
                tag = re.sub(r'class="([^"]*)"', r'class="\1 active"', tag)
                tag = tag.replace('<a ', '<a aria-current="page" ')
            return tag
        html = re.sub(r'<a\s+class="ltt-nav-link"[^>]*href="[^"]*(?:about|rolunk)[^"]*"[^>]*>', make_about_active, html)

    elif is_contact:
        def make_contact_active(match):
            tag = match.group(0)
            if 'active' not in tag:
                tag = re.sub(r'class="([^"]*)"', r'class="\1 active"', tag)
                tag = tag.replace('<a ', '<a aria-current="page" ')
            return tag
        html = re.sub(r'<a\s+class="ltt-nav-link"[^>]*href="[^"]*(?:contact|kapcsolat)[^"]*"[^>]*>', make_contact_active, html)

    # 5. Inject runtime active highlighter in ltt-nav-script
    if "CANONICAL ACTIVE PAGE HIGHLIGHTER" not in html and 'id="ltt-nav-script"' in html:
        # inject right before the end of the script: })();</script>
        html = re.sub(r'(\}\)\(\);\s*<\/script>)', f'{RUNTIME_JS}\\n\\1', html)

    if html != orig_html:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(html)
        return True
    return False

def main():
    files = glob.glob(os.path.join(BASE_DIR, "**/*.html"), recursive=True)
    files = [f for f in files if "harvested_html" not in f and "mockup" not in f and "preview" not in f]
    
    modified = 0
    for f in files:
        if process_file(f):
            modified += 1
            
    print(f"✓ Successfully processed {len(files)} files. Modified: {modified}")

if __name__ == "__main__":
    main()
