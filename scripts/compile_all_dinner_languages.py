#!/usr/bin/env python3
"""
MASTER MULTILINGUAL DINNER COMPILER — BUDAPEST ADVENTURES
Compiles the perfected Paris luxury editorial bento architecture,
contextual food and ship photo filmstrips, and clean captions
across all 21 localized dinner cruise hub pages.
"""

import os
import sys
import json
from bs4 import BeautifulSoup

BASE_DIR = '/Users/adamdimitrov/Development/budapest-adventures'
sys.path.insert(0, BASE_DIR)

from scripts.compile_all_languages_luxury import compile_dinner_guide, SLUG_MAP, LANGS
from scripts.build_hungarian_pages import build_hungarian_dinner
from scripts.inject_language_switcher import inject_language_switcher_into_file

def compile_all_dinner():
    print(f"=== Compiling Multilingual Dinner Guides across all 21 Languages ===")
    
    # 1. Compile Hungarian Dinner Guide
    print("\n--- 1. Hungarian (HU) ---")
    build_hungarian_dinner()
    hu_path = os.path.join(BASE_DIR, 'hu', 'setahajozas-a-dunan-vacsoraval', 'index.html')
    inject_language_switcher_into_file(hu_path)
    print("✓ HU Dinner Guide compiled and language switcher injected.")

    # 2. Load Master English Template (dinner.html)
    en_dinner_path = os.path.join(BASE_DIR, 'dinner.html')
    with open(en_dinner_path, 'r', encoding='utf-8') as f:
        en_dinner = f.read()

    # 3. Compile the other 20 languages
    print(f"\n--- 2. Other 20 Foreign Languages ---")
    for lang in LANGS:
        if lang == 'hu':
            continue
        slugs = SLUG_MAP[lang]
        dinner_slug = slugs['dinner']
        out_dir = os.path.join(BASE_DIR, lang, dinner_slug)
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, 'index.html')

        html = compile_dinner_guide(lang, en_dinner)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html)

        try:
            inject_language_switcher_into_file(out_path)
        except Exception as e:
            print(f"Warning: could not inject switcher for {lang}: {e}")

        print(f"✓ [{lang.upper()}] Compiled {out_path}")

    # 4. Verification Check
    print("\n--- 3. Verification Audit across all 21 Languages ---")
    all_langs = ['hu'] + [l for l in LANGS if l != 'hu']
    success = 0
    for lang in all_langs:
        slug = SLUG_MAP[lang]['dinner']
        p = os.path.join(BASE_DIR, lang, slug, 'index.html')
        if not os.path.exists(p):
            print(f"❌ Missing file for {lang}: {p}")
            continue
        with open(p, 'r', encoding='utf-8') as f:
            c = f.read()
        fstrips = c.count('class="ltt-filmstrip-wrap"')
        bentos = c.count('class="ltt-bento-group"')
        partner = 'legenda.hu/en?partner=38585' in c
        if fstrips >= 8 and bentos >= 20 and partner:
            success += 1
            print(f"  [PASS] {lang.upper()} ({slug}): {fstrips} filmstrips, {bentos} bentos, partner=38585 OK")
        else:
            print(f"  [FAIL] {lang.upper()} ({slug}): {fstrips} filmstrips, {bentos} bentos, partner={partner}")

    print(f"\n=== Compilation Complete: {success} / {len(all_langs)} verified perfectly! ===")

if __name__ == '__main__':
    compile_all_dinner()
