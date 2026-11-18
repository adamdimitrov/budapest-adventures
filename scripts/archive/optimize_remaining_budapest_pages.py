#!/usr/bin/env python3
"""
Optimization Script for Remaining Budapest Adventures Pages (Homepages & Category Hubs):
1. Replaces @import url('https://fonts.googleapis.com...') with high-priority <link rel="preconnect"> and <link rel="stylesheet"> in <head>
2. Removes render-blocking @import from <style> blocks
3. Ensures all below-the-fold images have loading="lazy" decoding="async"
"""

import os
import glob
import re
from bs4 import BeautifulSoup

REPO_ROOT = '/Users/adamdimitrov/Development/budapest-adventures'

PRECONNECT_TAGS = """<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous"/>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,600;1,700&amp;family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet"/>"""

def optimize_homepage(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False

    # Check for @import font
    import_match = re.search(r"@import\s+url\(['\"]https://fonts\.googleapis\.com[^'\"]+['\"]\);", content)
    if import_match:
        # Remove the @import statement
        content = content[:import_match.start()] + content[import_match.end():]
        # Insert preconnect tags in <head> if not already there
        if 'https://fonts.gstatic.com' not in content:
            if '<head>' in content:
                content = content.replace('<head>', f'<head>\n{PRECONNECT_TAGS}', 1)
            elif '<head ' in content:
                content = re.sub(r'(<head[^>]*>)', r'\1\n' + PRECONNECT_TAGS, content, count=1)
        modified = True

    # Check images on homepages to ensure below-the-fold images are lazy loaded
    soup = BeautifulSoup(content, 'html.parser')
    imgs = soup.find_all('img')
    img_modified = False
    for idx, img in enumerate(imgs):
        # Keep first 2 images (logo / hero) eager or as-is
        if idx >= 2 and not img.get('loading'):
            img['loading'] = 'lazy'
            img['decoding'] = 'async'
            img_modified = True
            modified = True

    if modified:
        if img_modified:
            content = str(soup)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True

    return False

def main():
    all_html = sorted(glob.glob(os.path.join(REPO_ROOT, '**/*.html'), recursive=True))
    count = 0
    for h in all_html:
        if 'data/' in h:
            continue
        if optimize_homepage(h):
            count += 1
            print(f"Optimized {os.path.relpath(h, REPO_ROOT)}")

    print(f"\nDone! Optimized {count} additional pages.")

if __name__ == '__main__':
    main()
