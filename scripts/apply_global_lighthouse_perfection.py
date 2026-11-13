import os
import glob
import re
from bs4 import BeautifulSoup

def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    original_len = len(content)
    changed = False

    # 1. Fix tourcms-sync.js path
    if 'src="tourcms-sync.js"' in content or "src='tourcms-sync.js'" in content:
        content = re.sub(r'src=["\']tourcms-sync\.js["\']', 'src="/tourcms-sync.js?v=20261113"', content)
        changed = True

    # 2. Strip broken integrity attributes from local assets
    if 'integrity=' in content:
        content = re.sub(r'\s+integrity=["\']sha[^\"]+["\']', '', content)
        changed = True

    # 3. Replace heavy legenda-candlelit-dinner.jpg (384 KB) with avif (47 KB)
    if '/legenda-candlelit-dinner.jpg' in content:
        content = content.replace('/legenda-candlelit-dinner.jpg', '/assets/cdn/60e43c7d6d05b671dff0dc1a/690332b608818ef6e357242b_candlelit-dinner-cruise-00002-p-800.avif')
        changed = True

    # 4. Replace heavy prosecco hero jpg (461 KB) with webp (62 KB)
    if '650beeaa6847525facb1a507_best-unlimited-prosecco-cruises-hero.jpg' in content:
        content = content.replace('650beeaa6847525facb1a507_best-unlimited-prosecco-cruises-hero.jpg', '650beeaa6847525facb1a507_best-unlimited-prosecco-cruises-hero-p-800.webp')
        changed = True

    # 5. Fix WCAG AA Color Contrast issues
    # #0284c7 (4.09:1) -> #026aa2 (4.6:1)
    if '#0284c7' in content:
        content = content.replace('#0284c7', '#026aa2')
        changed = True

    # #9f6e0d (4.45:1) -> #855a00 (5.2:1)
    if '#9f6e0d' in content:
        content = content.replace('#9f6e0d', '#855a00')
        changed = True

    # qf1-chip.no contrast
    if 'color:#64748b !important;' in content:
        content = content.replace('.qf1-chip.no{background:#f1f5f9 !important;color:#64748b !important;', '.qf1-chip.no{background:#f1f5f9 !important;color:#334155 !important;')
        changed = True

    # ltt-buy-price-val contrast on dark card header
    if '.ltt-buy-price-val{font-size:16px !important;font-weight:800 !important;color:#dfa732 !important;' in content:
        content = content.replace('.ltt-buy-price-val{font-size:16px !important;font-weight:800 !important;color:#dfa732 !important;', '.ltt-buy-price-val{font-size:16px !important;font-weight:800 !important;color:#fbbf24 !important;')
        changed = True

    # Top pick pill contrast
    if 'background:#dfa732; color:#fff;' in content:
        content = content.replace('background:#dfa732; color:#fff;', 'background:#855a00; color:#fff;')
        changed = True
    if 'background:#dfa732;color:#fff;' in content:
        content = content.replace('background:#dfa732;color:#fff;', 'background:#855a00;color:#fff;')
        changed = True

    # Filmstrip number badge contrast
    if '.ltt-strip-num{background:rgba(255,255,255,0.2)' in content:
        content = content.replace('.ltt-strip-num{background:rgba(255,255,255,0.2)', '.ltt-strip-num{background:rgba(15,23,42,0.85) !important;color:#ffffff')
        changed = True

    # 6. Parse DOM for structural fixes: deduplicate styles, scrollable tabindex, main landmark
    needs_soup = (
        content.count(":root{--primary-color:#0a192f") > 1 or
        'class="bpa-slider"' in content or
        'class="ltt-filmstrip"' in content or
        ('<main' not in content and ('class="ltt-editorial-wrapper"' in content or 'id="rankedDecks"' in content))
    )

    if needs_soup:
        soup = BeautifulSoup(content, 'html.parser')

        # Deduplicate identical style blocks
        seen_styles = set()
        for s in soup.find_all('style'):
            st_text = (s.string or '').strip()
            if not st_text:
                continue
            key = (len(st_text), st_text[:100])
            if key in seen_styles:
                s.decompose()
                changed = True
            else:
                seen_styles.add(key)

        # Ensure scrollable sliders have tabindex and unique labels
        for idx, slider in enumerate(soup.find_all(class_='bpa-slider')):
            if not slider.get('tabindex'):
                slider['tabindex'] = '0'
                slider['aria-label'] = f"Photo gallery {idx+1}"
                changed = True

        for idx, film in enumerate(soup.find_all(class_='ltt-filmstrip')):
            if not film.get('tabindex'):
                film['tabindex'] = '0'
                film['aria-label'] = f"Filmstrip gallery {idx+1}"
                changed = True

        # Ensure main landmark
        if not soup.find('main'):
            wrapper = soup.find(class_='ltt-editorial-wrapper') or soup.find(id='rankedDecks') or soup.find('article')
            if wrapper:
                wrapper['role'] = 'main'
                changed = True

        # Preload type update for dinner cruise avif if rel=preload points to avif
        for pl in soup.find_all('link', rel='preload'):
            href = pl.get('href', '')
            if href.endswith('.avif') and pl.get('type') != 'image/avif':
                pl['type'] = 'image/avif'
                changed = True
            elif href.endswith('.webp') and pl.get('type') != 'image/webp':
                pl['type'] = 'image/webp'
                changed = True

        if changed:
            content = str(soup)

    if changed:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True, original_len, len(content)
    return False, original_len, original_len

def main():
    root_dir = "/Users/adamdimitrov/Development/budapest-adventures"
    html_files = glob.glob(f"{root_dir}/**/*.html", recursive=True)
    
    modified_count = 0
    total_saved_bytes = 0

    print(f"Scanning and optimizing {len(html_files)} HTML files...")
    for path in html_files:
        mod, orig, new_sz = process_file(path)
        if mod:
            modified_count += 1
            if orig > new_sz:
                total_saved_bytes += (orig - new_sz)

    print(f"\nOptimization Complete!")
    print(f"Total HTML files modified: {modified_count}")
    print(f"Total bytes saved across repository: {total_saved_bytes:,} bytes ({total_saved_bytes/1024/1024:.2f} MB)")

if __name__ == "__main__":
    main()
