#!/usr/bin/env python3
"""
Optimization Script for Budapest River Cruises Article:
1. Progressive Lazy Loading for Photo Carousels (.bpa-slider slides 2..N)
2. Deduplicate Google Fonts & Consolidate Preconnects
3. Defer Emerald (emrld.cc) tracking script to user interaction
4. Optimize sizes attribute on .ltt-sp-card images
5. Update bpaSlide and slider runtime in Script 12
"""

import re
from bs4 import BeautifulSoup

SVG_PLACEHOLDER = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 500'%3E%3C/svg%3E"

def optimize_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # 1. Deduplicate Google Fonts and clean up preconnects
    # Find all link tags
    # Remove redundant Playfair Display link: href containing Playfair+Display:ital,wght@0,600;0,700;1,600&display=swap
    for link in soup.find_all('link', rel='stylesheet'):
        href = link.get('href', '')
        if 'fonts.googleapis.com' in href and 'Plus+Jakarta+Sans' not in href:
            link.decompose()

    # Deduplicate preconnect tags for fonts.googleapis.com and fonts.gstatic.com
    seen_preconnects = set()
    for link in soup.find_all('link', rel='preconnect'):
        href = link.get('href', '')
        if href in seen_preconnects:
            link.decompose()
        else:
            seen_preconnects.add(href)

    # 2. Defer Emerald (emrld.cc) script to user interaction
    # Locate emerald script
    for script in soup.find_all('script'):
        text = script.string or script.text or ''
        if 'emrld.cc' in text:
            new_emerald_js = """
window.addEventListener('load', function() {
  function loadEmerald() {
    if (window._emLoaded) return;
    window._emLoaded = true;
    var script = document.createElement('script');
    script.async = 1;
    script.src = 'https://emrld.cc/MjA0NDQy.js?t=204442';
    document.head.appendChild(script);
  }
  ['scroll', 'touchstart', 'mousemove'].forEach(function(evt) {
    window.addEventListener(evt, loadEmerald, { once: true, passive: true });
  });
  setTimeout(loadEmerald, 6000);
});
"""
            script.string = new_emerald_js

    # 3. Optimize .bpa-slider: Slide 1 stays eager/visible; Slides 2..N use data-src
    sliders = soup.find_all(class_='bpa-slider')
    total_deferred = 0
    for slider in sliders:
        imgs = slider.find_all('img')
        for img in imgs[1:]:
            src = img.get('src', '')
            if src and not src.startswith('data:'):
                img['data-src'] = src
                img['src'] = SVG_PLACEHOLDER
                if img.get('srcset'):
                    img['data-srcset'] = img['srcset']
                    del img['srcset']
                img['loading'] = 'lazy'
                img['decoding'] = 'async'
                total_deferred += 1

    # 4. Optimize sizes attribute on .ltt-sp-card images
    sp_cards = soup.find_all(class_='ltt-sp-card')
    sp_updated = 0
    for card in sp_cards:
        img = card.find('img')
        if img and img.get('sizes') == '100vw':
            img['sizes'] = '(max-width: 640px) 100vw, 420px'
            sp_updated += 1

    result_html = str(soup)

    # 5. Update Script 12 slider runtime
    # Add loadSliderImages and call it in bpaSlide
    old_bpa_slide = """  // 1. Slider controls
  window.bpaSlide = function(btn, dir) {
    var media = btn.closest('.bpa-media');
    if (!media) return;
    var slider = media.querySelector('.bpa-slider');
    if (!slider) return;
    var w = slider.clientWidth;
    slider.scrollBy({ left: dir * w, behavior: 'smooth' });
  };"""

    new_bpa_slide = """  // 1. Slider controls with Progressive Lazy-Loading
  function loadSliderImages(slider) {
    if (!slider || slider._loaded) return;
    slider._loaded = true;
    var lazyImgs = slider.querySelectorAll('img[data-src]');
    for (var i = 0; i < lazyImgs.length; i++) {
      var img = lazyImgs[i];
      if (img.getAttribute('data-srcset')) {
        img.setAttribute('srcset', img.getAttribute('data-srcset'));
        img.removeAttribute('data-srcset');
      }
      img.src = img.getAttribute('data-src');
      img.removeAttribute('data-src');
    }
  }

  window.bpaSlide = function(btn, dir) {
    var media = btn.closest('.bpa-media');
    if (!media) return;
    var slider = media.querySelector('.bpa-slider');
    if (!slider) return;
    loadSliderImages(slider);
    var w = slider.clientWidth;
    slider.scrollBy({ left: dir * w, behavior: 'smooth' });
  };"""

    if old_bpa_slide in result_html:
        result_html = result_html.replace(old_bpa_slide, new_bpa_slide, 1)
    else:
        print("Warning: old_bpa_slide pattern not matched exactly, checking regex...")
        # fallback regex replace
        pattern = r'// 1\. Slider controls\s*\n\s*window\.bpaSlide\s*=\s*function\(btn,\s*dir\)\s*\{.*?slider\.scrollBy\(\{\s*left:\s*dir\s*\*\s*w,\s*behavior:\s*[\'\"]smooth[\'\"]\s*\}\);\s*\};'
        result_html = re.sub(pattern, new_bpa_slide, result_html, flags=re.DOTALL)

    # Add initLazySliders to initAll in Script 12
    old_init_all = """  function initAll() {
    initHybridSheet();
    syncSidebarTOC();
    initAllFilmstrips();
    updateFloatingCTA();
    updateActiveTOC();"""

    new_init_all = """  function initLazySliders() {
    document.querySelectorAll('.bpa-slider').forEach(function(slider) {
      if (slider._lazyBound) return;
      slider._lazyBound = true;
      var media = slider.closest('.bpa-media');
      if (media) {
        media.addEventListener('mouseenter', function() { loadSliderImages(slider); }, { once: true, passive: true });
        media.addEventListener('touchstart', function() { loadSliderImages(slider); }, { once: true, passive: true });
      }
      slider.addEventListener('scroll', function() { loadSliderImages(slider); }, { once: true, passive: true });
    });
  }

  function initAll() {
    initHybridSheet();
    syncSidebarTOC();
    initAllFilmstrips();
    initLazySliders();
    updateFloatingCTA();
    updateActiveTOC();"""

    if old_init_all in result_html:
        result_html = result_html.replace(old_init_all, new_init_all, 1)
    else:
        print("Warning: old_init_all pattern not matched exactly, checking regex...")
        pattern_init = r'function initAll\(\)\s*\{\s*initHybridSheet\(\);\s*syncSidebarTOC\(\);\s*initAllFilmstrips\(\);\s*updateFloatingCTA\(\);\s*updateActiveTOC\(\);\s*\}'
        result_html = re.sub(pattern_init, new_init_all, result_html, flags=re.DOTALL)

    print(f"Optimized: {total_deferred} slider images deferred, {sp_updated} spec card sizes updated.")
    return result_html

if __name__ == '__main__':
    target_files = [
        '/Users/adamdimitrov/Development/budapest-adventures/river.html',
        '/Users/adamdimitrov/Development/budapest-adventures/budapest-river-cruises.html',
        '/Users/adamdimitrov/Development/budapest-adventures/best-budapest-river-cruises.html',
        '/Users/adamdimitrov/Development/budapest-adventures/budapest-river-cruises/index.html',
        '/Users/adamdimitrov/Development/budapest-adventures/best-budapest-river-cruises/index.html'
    ]

    for path in target_files:
        print(f"Processing {path}...")
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        optimized = optimize_html(content)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(optimized)
        print(f"Finished {path} (new size: {len(optimized)} bytes)")
