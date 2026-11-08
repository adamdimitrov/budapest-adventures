#!/usr/bin/env python3
"""
CANONICAL LANGUAGE SWITCHER INJECTOR — BUDAPEST ADVENTURES
Integrates the canonical minimal language switcher across all 22 languages and all pages.
Matches the exact architecture, styles, and behavior deployed in The Cruise Detective:
- Desktop navbar button with globe icon, current uppercase language code, and chevron toggle
- Clean dropdown with 'Select Language' header, available count, and 2-column grid of all 22 supported languages
- Mobile drawer language section with 3/4-column tap-friendly language chips
- Exact URL routing: links directly to the equivalent localized page in each target language
- Pure vanilla JS toggle with outside click and ESC dismissal
"""

import os
import re
import sys
from bs4 import BeautifulSoup

BASE_DIR = '/Users/adamdimitrov/Development/budapest-adventures'
sys.path.insert(0, BASE_DIR)

from scripts.compile_all_translated_guides import SLUG_MAP, LANGS

ALL_LANGS = [
    ('en', 'EN', 'English'),
    ('hu', 'HU', 'Magyar'),
    ('de', 'DE', 'Deutsch'),
    ('fr', 'FR', 'Français'),
    ('es', 'ES', 'Español'),
    ('it', 'IT', 'Italiano'),
    ('nl', 'NL', 'Nederlands'),
    ('pl', 'PL', 'Polski'),
    ('ro', 'RO', 'Română'),
    ('cs', 'CS', 'Čeština'),
    ('sk', 'SK', 'Slovenčina'),
    ('hr', 'HR', 'Hrvatski'),
    ('sr', 'SR', 'Srpski'),
    ('bg', 'BG', 'Български'),
    ('ru', 'RU', 'Русский'),
    ('uk', 'UK', 'Українська'),
    ('el', 'EL', 'Ελληνικά'),
    ('tr', 'TR', 'Türkçe'),
    ('pt', 'PT', 'Português'),
    ('he', 'HE', 'עברית'),
    ('ja', 'JA', '日本語'),
    ('ko', 'KO', '한국어'),
]

SWITCHER_I18N = {
    'en': {'title': 'Select Language', 'available': '● 22 AVAILABLE', 'mobile': 'Language'},
    'hu': {'title': 'Nyelvválasztás', 'available': '● 22 ELÉRHETŐ', 'mobile': 'Nyelv'},
    'de': {'title': 'Sprache wählen', 'available': '● 22 VERFÜGBAR', 'mobile': 'Sprache'},
    'fr': {'title': 'Choisir la langue', 'available': '● 22 DISPONIBLES', 'mobile': 'Langue'},
    'es': {'title': 'Seleccionar idioma', 'available': '● 22 DISPONIBLES', 'mobile': 'Idioma'},
    'it': {'title': 'Seleziona lingua', 'available': '● 22 DISPONIBILI', 'mobile': 'Lingua'},
    'nl': {'title': 'Kies taal', 'available': '● 22 BESCHIKBAAR', 'mobile': 'Taal'},
    'pl': {'title': 'Wybierz język', 'available': '● 22 DOSTĘPNE', 'mobile': 'Język'},
    'ro': {'title': 'Selectați limba', 'available': '● 22 DISPONIBILE', 'mobile': 'Limbă'},
    'cs': {'title': 'Vyberte jazyk', 'available': '● 22 DOSTUPNÝCH', 'mobile': 'Jazyk'},
    'sk': {'title': 'Vyberte jazyk', 'available': '● 22 DOSTUPNÝCH', 'mobile': 'Jazyk'},
    'hr': {'title': 'Odaberite jezik', 'available': '● 22 DOSTUPNO', 'mobile': 'Jezik'},
    'sr': {'title': 'Изаберите језик', 'available': '● 22 ДОСТУПНО', 'mobile': 'Језик'},
    'bg': {'title': 'Изберете език', 'available': '● 22 НАЛИЧНИ', 'mobile': 'Език'},
    'ru': {'title': 'Выберите язык', 'available': '● 22 ДОСТUPНО', 'mobile': 'Язык'},
    'uk': {'title': 'Оберіть мову', 'available': '● 22 ДОСТУПНО', 'mobile': 'Мова'},
    'el': {'title': 'Επιλέξτε γλώσσα', 'available': '● 22 ΔΙΑΘΕΣΙΜΕΣ', 'mobile': 'Γλώσσα'},
    'tr': {'title': 'Dil seçin', 'available': '● 22 MEVCUT', 'mobile': 'Dil'},
    'pt': {'title': 'Selecionar idioma', 'available': '● 22 DISPONÍVEIS', 'mobile': 'Idioma'},
    'he': {'title': 'בחר שפה', 'available': '● 22 זמין', 'mobile': 'שפה'},
    'ja': {'title': '言語を選択', 'available': '● 22 言語対応', 'mobile': '言語'},
    'ko': {'title': '언어 선택', 'available': '● 22개 지원', 'mobile': '언어'},
}

CSS_STYLES_RAW = """
/* ==========================================================================
   CANONICAL LANGUAGE SWITCHER SYSTEM — BUDAPEST ADVENTURES
   ========================================================================== */
.ltt-lang-trigger {
  position: relative;
  display: inline-block;
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  margin-right: 4px;
}
.ltt-lang-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #f8fafc;
  border: 1px solid #cbd5e1;
  color: #0f172a;
  padding: 6px 12px;
  border-radius: 9999px;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  font-family: inherit;
  line-height: 1;
}
.ltt-lang-btn:hover, .ltt-lang-btn.is-active {
  background: #ffffff;
  border-color: #dfa732;
  box-shadow: 0 4px 12px rgba(223, 167, 50, 0.18);
  color: #0b1320;
}
.ltt-lang-globe {
  color: #64748b;
  transition: color 0.15s ease;
}
.ltt-lang-btn:hover .ltt-lang-globe, .ltt-lang-btn.is-active .ltt-lang-globe {
  color: #dfa732;
}
.ltt-lang-code {
  letter-spacing: 0.04em;
  font-weight: 800;
}
.ltt-lang-chevron {
  color: #94a3b8;
  transition: transform 0.2s ease;
}
.ltt-lang-btn.is-active .ltt-lang-chevron {
  transform: rotate(180deg);
  color: #dfa732;
}
.ltt-lang-dropdown {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  width: 320px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  box-shadow: 0 16px 36px -4px rgba(15, 23, 42, 0.15), 0 0 0 1px rgba(0, 0, 0, 0.04);
  padding: 8px;
  z-index: 10000;
  display: none;
  animation: lttLangFade 0.18s cubic-bezier(0.16, 1, 0.3, 1);
}
.ltt-lang-dropdown.show {
  display: block;
}
@keyframes lttLangFade {
  from { opacity: 0; transform: translateY(-6px); }
  to { opacity: 1; transform: translateY(0); }
}
.ltt-lang-dropdown-header {
  font-size: 10px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #94a3b8;
  padding: 6px 10px 4px;
  border-bottom: 1px solid #f1f5f9;
  margin-bottom: 4px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.ltt-lang-grid-menu {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2px;
  max-height: 400px;
  overflow-y: auto;
}
.ltt-lang-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 7px 10px;
  border-radius: 6px;
  text-decoration: none;
  color: #1e293b;
  font-size: 12px;
  font-weight: 600;
  transition: background 0.12s ease;
}
.ltt-lang-item:hover {
  background: #f8fafc;
  color: #0b1320;
}
.ltt-lang-item.current {
  background: rgba(223, 167, 50, 0.12);
  color: #8b6508;
  font-weight: 700;
}
.ltt-lang-item .lang-native {
  display: block;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.ltt-lang-item .lang-code-tag {
  font-size: 10px;
  font-weight: 800;
  color: #94a3b8;
  background: #f1f5f9;
  padding: 1px 5px;
  border-radius: 4px;
  margin-left: 6px;
}
.ltt-lang-item.current .lang-code-tag {
  background: #dfa732;
  color: #ffffff;
}

/* Mobile drawer language section */
.ltt-mobile-lang-box {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid #e2e8f0;
}
@media (min-width: 992px) {
  .ltt-mobile-lang-box {
    display: none !important;
  }
}
.ltt-mobile-lang-title {
  font-size: 10px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #94a3b8;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 6px;
}
.ltt-mobile-lang-chips {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 6px;
}
.ltt-mobile-lang-chip {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 8px 4px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  background: #f8fafc;
  color: #1e293b;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.15s ease;
}
.ltt-mobile-lang-chip:hover {
  border-color: #cbd5e1;
  background: #ffffff;
}
.ltt-mobile-lang-chip.current {
  background: #0b1320;
  border-color: #0b1320;
  color: #ffffff;
}
.ltt-mobile-lang-chip.current .chip-code {
  color: #dfa732;
}
.ltt-mobile-lang-chip .chip-code {
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.04em;
}
.ltt-mobile-lang-chip .chip-name {
  font-size: 10px;
  opacity: 0.75;
  font-weight: 500;
  white-space: nowrap;
}

/* Nav header alignments */
.ltt-nav-right {
  margin-left: auto !important;
  display: flex !important;
  align-items: center !important;
  justify-content: flex-end !important;
  height: 100% !important;
  gap: 12px !important;
}
@media (max-width: 991px) {
  .ltt-nav-inner {
    justify-content: space-between !important;
    gap: 12px !important;
  }
  .ltt-nav-right {
    margin-left: auto !important;
    display: flex !important;
    align-items: center !important;
    justify-content: flex-end !important;
    height: 100% !important;
  }
  .ltt-hamburger {
    display: flex !important;
    align-self: center !important;
    margin: 0 !important;
  }
  .ltt-lang-trigger {
    display: none !important;
  }
}
@media (max-width: 480px) {
  .ltt-mobile-lang-chips {
    grid-template-columns: repeat(3, 1fr);
  }
}
"""

JS_LOGIC_RAW = """
(function() {
  window.lttToggleLangDropdown = function() {
    var dd = document.getElementById('lttLangDropdown');
    var btn = document.getElementById('lttLangBtn');
    if (!dd || !btn) return;
    var isOpen = dd.classList.contains('show');
    if (isOpen) {
      dd.classList.remove('show');
      btn.classList.remove('is-active');
      btn.setAttribute('aria-expanded', 'false');
    } else {
      dd.classList.add('show');
      btn.classList.add('is-active');
      btn.setAttribute('aria-expanded', 'true');
    }
  };

  document.addEventListener('click', function(e) {
    var trigger = document.getElementById('lttLangTrigger');
    var dd = document.getElementById('lttLangDropdown');
    var btn = document.getElementById('lttLangBtn');
    if (trigger && dd && !trigger.contains(e.target)) {
      dd.classList.remove('show');
      if (btn) {
        btn.classList.remove('is-active');
        btn.setAttribute('aria-expanded', 'false');
      }
    }
  });

  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
      var dd = document.getElementById('lttLangDropdown');
      var btn = document.getElementById('lttLangBtn');
      if (dd && dd.classList.contains('show')) {
        dd.classList.remove('show');
        if (btn) {
          btn.classList.remove('is-active');
          btn.setAttribute('aria-expanded', 'false');
        }
      }
    }
  });
})();
"""

def get_page_info(rel_path):
    """Determines language and page_key for a given relative path."""
    p = rel_path.strip('/')
    parts = p.split('/')
    if p in ['index.html', '']:
        return 'en', 'home'
    if parts[0] in LANGS:
        lang = parts[0]
        sub = '/'.join(parts[1:])
        if sub in ['index.html', '']:
            return lang, 'home'
        river_slug = SLUG_MAP[lang]['river']
        dinner_slug = SLUG_MAP[lang]['dinner']
        if sub.startswith(river_slug):
            return lang, 'river'
        if sub.startswith(dinner_slug):
            return lang, 'dinner'
        if 'candlelit' in sub:
            return lang, 'candlelit'
        if 'night-cruises' in sub:
            return lang, 'night'
        if 'prosecco' in sub:
            return lang, 'prosecco'
        if 'private-boat' in sub:
            return lang, 'private'
        if 'walking-tours' in sub:
            return lang, 'walking'
        if 'hostels' in sub:
            return lang, 'hostels'
        if 'thermal-baths' in sub:
            return lang, 'baths'
        if 'budapest-card' in sub:
            return lang, 'card'
        if 'airport' in sub:
            return lang, 'airport'
        if 'parliament' in sub:
            return lang, 'parliament'
        if 'group-booking' in sub:
            return lang, 'group'
        if 'tourism-statistics' in sub:
            return lang, 'tourism'
        if 'travel-guide' in sub:
            return lang, 'travel'
        if 'about' in sub:
            return lang, 'about'
        if 'contact' in sub:
            return lang, 'contact'
        return lang, 'home'
    else:
        # English root pages
        f = os.path.basename(rel_path)
        name = os.path.splitext(f)[0]
        parent = os.path.dirname(rel_path)
        if name in ['index']:
            if parent in ['', '.']: return 'en', 'home'
            if 'best-budapest-river-cruises' in parent or 'budapest-river-cruises' in parent: return 'en', 'river'
            if 'best-dinner-cruises-budapest' in parent or 'budapest-dinner-cruises' in parent:
                if 'candlelit' in parent: return 'en', 'candlelit'
                return 'en', 'dinner'
        if name in ['river', 'best-budapest-river-cruises', 'budapest-river-cruises']: return 'en', 'river'
        if name in ['dinner', 'best-dinner-cruises-budapest', 'budapest-dinner-cruises']: return 'en', 'dinner'
        if name in ['candlelit-dinner-cruise', 'candlelit-dinner-cruise-budapest']: return 'en', 'candlelit'
        if name in ['best-night-cruises-budapest']: return 'en', 'night'
        if name in ['unlimited-prosecco-cruises-budapest']: return 'en', 'prosecco'
        if name in ['best-private-boat-tours-budapest']: return 'en', 'private'
        if name in ['best-walking-tours-budapest']: return 'en', 'walking'
        if name in ['best-hostels-budapest']: return 'en', 'hostels'
        if name in ['thermal-baths-budapest']: return 'en', 'baths'
        if name in ['budapest-card-is-it-worth-it']: return 'en', 'card'
        if name in ['budapest-airport-to-city-center']: return 'en', 'airport'
        if name in ['budapest-parliament']: return 'en', 'parliament'
        if name in ['budapest-river-cruise-group-booking']: return 'en', 'group'
        if name in ['budapest-tourism-statistics']: return 'en', 'tourism'
        if name in ['budapest-travel-guide']: return 'en', 'travel'
        if name in ['about']: return 'en', 'about'
        if name in ['contact']: return 'en', 'contact'
        return 'en', 'home'

def get_target_url(target_lang, page_key):
    """Returns the canonical URL for the given page_key in target_lang."""
    if target_lang == 'en':
        if page_key == 'home': return '/'
        if page_key == 'river': return '/best-budapest-river-cruises'
        if page_key == 'dinner': return '/best-dinner-cruises-budapest'
        if page_key == 'candlelit': return '/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest'
        if page_key == 'night': return '/best-night-cruises-budapest'
        if page_key == 'prosecco': return '/unlimited-prosecco-cruises-budapest'
        if page_key == 'private': return '/best-private-boat-tours-budapest'
        if page_key == 'walking': return '/best-walking-tours-budapest'
        if page_key == 'hostels': return '/best-hostels-budapest'
        if page_key == 'baths': return '/thermal-baths-budapest'
        if page_key == 'card': return '/budapest-card-is-it-worth-it'
        if page_key == 'airport': return '/budapest-airport-to-city-center'
        if page_key == 'parliament': return '/budapest-parliament'
        if page_key == 'group': return '/budapest-river-cruise-group-booking'
        if page_key == 'tourism': return '/budapest-tourism-statistics'
        if page_key == 'travel': return '/budapest-travel-guide'
        if page_key == 'about': return '/about'
        if page_key == 'contact': return '/contact'
        return '/'
    else:
        if page_key == 'home': return f'/{target_lang}'
        if page_key == 'river': return f'/{target_lang}/{SLUG_MAP[target_lang]["river"]}'
        if page_key == 'dinner': return f'/{target_lang}/{SLUG_MAP[target_lang]["dinner"]}'
        if page_key == 'candlelit': return f'/{target_lang}/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest'
        if page_key == 'night': return f'/{target_lang}/best-night-cruises-budapest'
        if page_key == 'prosecco': return f'/{target_lang}/unlimited-prosecco-cruises-budapest'
        if page_key == 'private': return f'/{target_lang}/best-private-boat-tours-budapest'
        if page_key == 'walking': return f'/{target_lang}/best-walking-tours-budapest'
        if page_key == 'hostels': return f'/{target_lang}/best-hostels-budapest'
        if page_key == 'baths': return f'/{target_lang}/thermal-baths-budapest'
        if page_key == 'card': return f'/{target_lang}/budapest-card-is-it-worth-it'
        if page_key == 'airport': return f'/{target_lang}/budapest-airport-to-city-center'
        if page_key == 'parliament': return f'/{target_lang}/budapest-attractions/budapest-parliament'
        if page_key == 'group': return f'/{target_lang}/budapest-river-cruise-group-booking'
        if page_key == 'tourism': return f'/{target_lang}/budapest-tourism-statistics'
        if page_key == 'travel': return f'/{target_lang}/budapest-travel-guide'
        if page_key == 'about': return f'/{target_lang}/about'
        if page_key == 'contact': return f'/{target_lang}/contact'
        return f'/{target_lang}'

def build_switcher_dom(current_lang, page_key):
    """Builds the HTML snippet for desktop trigger and mobile drawer box."""
    labels = SWITCHER_I18N.get(current_lang, SWITCHER_I18N['en'])
    active_code = current_lang.upper()

    # Desktop Trigger HTML
    dt_lines = []
    dt_lines.append('<div class="ltt-lang-trigger" id="lttLangTrigger">')
    dt_lines.append('  <button aria-expanded="false" aria-haspopup="true" class="ltt-lang-btn" id="lttLangBtn" onclick="window.lttToggleLangDropdown()" type="button">')
    dt_lines.append('    <svg class="ltt-lang-globe" fill="none" height="13" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="13">')
    dt_lines.append('      <circle cx="12" cy="12" r="10"></circle>')
    dt_lines.append('      <line x1="2" y1="12" x2="22" y2="12"></line>')
    dt_lines.append('      <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>')
    dt_lines.append('    </svg>')
    dt_lines.append(f'    <span class="ltt-lang-code" id="lttActiveLangLabel">{active_code}</span>')
    dt_lines.append('    <svg class="ltt-lang-chevron" fill="none" height="10" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" viewBox="0 0 24 24" width="10">')
    dt_lines.append('      <polyline points="6 9 12 15 18 9"></polyline>')
    dt_lines.append('    </svg>')
    dt_lines.append('  </button>')
    dt_lines.append('  <div aria-label="Select Language" class="ltt-lang-dropdown" id="lttLangDropdown" role="menu">')
    dt_lines.append('    <div class="ltt-lang-dropdown-header">')
    dt_lines.append(f'      <span>{labels["title"]}</span>')
    dt_lines.append(f'      <span style="font-size:9px; color:#10b981; font-weight:800;">{labels["available"]}</span>')
    dt_lines.append('    </div>')
    dt_lines.append('    <div class="ltt-lang-grid-menu">')

    for lang_code, code_upper, native_name in ALL_LANGS:
        target_url = get_target_url(lang_code, page_key)
        current_cls = " current" if lang_code == current_lang else ""
        dt_lines.append(f'      <a class="ltt-lang-item{current_cls}" data-lang="{lang_code}" href="{target_url}" role="menuitem">')
        dt_lines.append(f'        <span class="lang-native">{native_name}</span>')
        dt_lines.append(f'        <span class="lang-code-tag">{code_upper}</span>')
        dt_lines.append('      </a>')

    dt_lines.append('    </div>')
    dt_lines.append('  </div>')
    dt_lines.append('</div>')
    desktop_html = '\n'.join(dt_lines)

    # Mobile Drawer HTML
    mb_lines = []
    mb_lines.append('  <!-- MOBILE DRAWER LANGUAGE SECTION -->')
    mb_lines.append('  <div class="ltt-mobile-lang-box">')
    mb_lines.append('    <div class="ltt-mobile-lang-title">')
    mb_lines.append('      <svg fill="none" height="12" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="12"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>')
    mb_lines.append(f'      <span>{labels["mobile"]}</span>')
    mb_lines.append('    </div>')
    mb_lines.append('    <div class="ltt-mobile-lang-chips">')

    for lang_code, code_upper, native_name in ALL_LANGS:
        target_url = get_target_url(lang_code, page_key)
        current_cls = " current" if lang_code == current_lang else ""
        mb_lines.append(f'      <a class="ltt-mobile-lang-chip{current_cls}" data-m-lang="{lang_code}" href="{target_url}">')
        mb_lines.append(f'        <span class="chip-code">{code_upper}</span>')
        mb_lines.append(f'        <span class="chip-name">{native_name}</span>')
        mb_lines.append('      </a>')

    mb_lines.append('    </div>')
    mb_lines.append('  </div>')
    mobile_html = '\n'.join(mb_lines)

    return desktop_html, mobile_html

def inject_language_switcher_into_file(file_path):
    """Processes an HTML file with BeautifulSoup to guarantee 100% accurate DOM tree placement."""
    rel_path = os.path.relpath(file_path, BASE_DIR)
    current_lang, page_key = get_page_info(rel_path)

    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # 1. Clean existing language switcher elements if present to allow idempotent re-runs
    for s in soup.find_all('style', id='ltt-language-switcher-styles'):
        s.decompose()
    for s in soup.find_all('script', id='ltt-language-switcher-logic'):
        s.decompose()
    for el in soup.find_all(id='lttLangTrigger'):
        el.decompose()
    for el in soup.find_all(class_='ltt-mobile-lang-box'):
        el.decompose()

    desktop_html_str, mobile_html_str = build_switcher_dom(current_lang, page_key)
    desktop_tag = BeautifulSoup(desktop_html_str, 'html.parser').find('div', id='lttLangTrigger')
    mobile_tag = BeautifulSoup(mobile_html_str, 'html.parser').find('div', class_='ltt-mobile-lang-box')

    # 2. Inject desktop trigger & guarantee hamburger button is nested inside nav_right
    nav_right = soup.find('div', class_='ltt-nav-right')
    hamburger = soup.find(id='lttNavToggle')
    if nav_right:
        if hamburger:
            hamburger.extract()
            nav_right.append(desktop_tag)
            nav_right.append(hamburger)
        else:
            nav_right.append(desktop_tag)
    else:
        # Secondary pages with t-navigation Webflow navbar
        t_btn = soup.find(class_='t-navigation-menu-button')
        if t_btn:
            t_btn.insert_before(desktop_tag)

    # 3. Inject mobile drawer box strictly INSIDE drawer content
    drawer = soup.find(id='lttMobileDrawer')
    if drawer:
        drawer_content = drawer.find(class_='ltt-drawer-content')
        if drawer_content:
            drawer_content.append(mobile_tag)
        else:
            drawer.append(mobile_tag)
    else:
        # Secondary pages with t-navigation
        t_menu = soup.find(class_='t-navigation-menu')
        if t_menu:
            t_menu.append(mobile_tag)

    # 4. Deduplicate hamburger scripts to prevent open/close race conditions
    scripts_with_toggle = [
        s for s in soup.find_all('script')
        if s.text and ('document.getElementById(\'lttNavToggle\')' in s.text or 'document.getElementById(\"lttNavToggle\")' in s.text)
    ]
    if len(scripts_with_toggle) > 1:
        has_named = any(s.get('id') == 'ltt-nav-script' for s in scripts_with_toggle)
        if has_named:
            for s in scripts_with_toggle:
                if s.get('id') != 'ltt-nav-script':
                    s.decompose()
        else:
            for s in scripts_with_toggle[:-1]:
                s.decompose()
            scripts_with_toggle[-1]['id'] = 'ltt-nav-script'

    # 5. Inject CSS in <head>
    head = soup.find('head')
    if head:
        style_tag = soup.new_tag('style', id='ltt-language-switcher-styles')
        style_tag.string = CSS_STYLES_RAW
        head.append(style_tag)

    # 5. Inject JS before </body>
    body = soup.find('body')
    if body:
        script_tag = soup.new_tag('script', id='ltt-language-switcher-logic')
        script_tag.string = JS_LOGIC_RAW
        body.append(script_tag)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    return True

def main():
    print("Beginning canonical language switcher injection across Budapest Adventures...")
    files_to_process = []

    # English core production pages
    en_pages = [
        'index.html', 'river.html', 'dinner.html', 'candlelit-dinner-cruise.html',
        'best-budapest-river-cruises.html', 'budapest-river-cruises.html',
        'best-dinner-cruises-budapest.html', 'budapest-dinner-cruises.html',
        'best-budapest-river-cruises/index.html', 'budapest-river-cruises/index.html',
        'best-dinner-cruises-budapest/index.html', 'budapest-dinner-cruises/index.html',
        'best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest/index.html',
        'best-night-cruises-budapest.html', 'unlimited-prosecco-cruises-budapest.html',
        'best-private-boat-tours-budapest.html', 'best-walking-tours-budapest.html',
        'best-hostels-budapest.html', 'thermal-baths-budapest.html',
        'budapest-card-is-it-worth-it.html', 'budapest-airport-to-city-center.html',
        'budapest-parliament.html', 'budapest-river-cruise-group-booking.html',
        'budapest-tourism-statistics.html', 'budapest-travel-guide.html',
        'about.html', 'contact.html', 'things-to-do.html', 'legenda-city-cruises.html'
    ]
    for ep in en_pages:
        p = os.path.join(BASE_DIR, ep)
        if os.path.exists(p):
            files_to_process.append(p)

    # All foreign language pages
    for lang in LANGS:
        ldir = os.path.join(BASE_DIR, lang)
        if not os.path.exists(ldir):
            continue
        for root, dirs, files in os.walk(ldir):
            for f in files:
                if f.endswith('.html'):
                    files_to_process.append(os.path.join(root, f))

    print(f"Discovered {len(files_to_process)} target HTML production files.")
    count = 0
    for fp in files_to_process:
        try:
            inject_language_switcher_into_file(fp)
            count += 1
        except Exception as e:
            print(f"Error on {fp}: {e}")

    print(f"Successfully injected language switcher into {count} pages!")

if __name__ == '__main__':
    main()
