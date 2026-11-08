#!/usr/bin/env python3
"""
RATE-LIMIT-SAFE HARVESTER FOR ALL SECONDARY PAGES ACROSS 21 LANGUAGES
Scrapes all remaining editorial, attraction, and utility pages from live Linguana
with polite rate limiting, retry backoff, and caching.
"""

import os
import time
import random
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = '/Users/adamdimitrov/Development/budapest-adventures'
CACHE_DIR = os.path.join(BASE_DIR, 'data', 'harvested_html')

LANGS = ['hu', 'de', 'fr', 'it', 'es', 'ro', 'pl', 'nl', 'cs', 'sk', 'pt', 'ru', 'hr', 'sr', 'bg', 'el', 'tr', 'uk', 'he', 'ja', 'ko']

PAGES = {
    'about': 'about',
    'contact': 'contact',
    'thermal_baths': 'thermal-baths-budapest',
    'night_cruises': 'best-night-cruises-budapest',
    'private_boats': 'best-private-boat-tours-budapest',
    'unlimited_prosecco': 'unlimited-prosecco-cruises-budapest',
    'walking_tours': 'best-walking-tours-budapest',
    'hostels': 'best-hostels-budapest',
    'budapest_card': 'budapest-card-is-it-worth-it',
    'travel_guide': 'budapest-travel-guide',
    'airport_transfer': 'budapest-airport-to-city-center',
    'parliament': 'budapest-attractions/budapest-parliament',
    'group_booking': 'budapest-river-cruise-group-booking',
    'tourism_statistics': 'budapest-tourism-statistics',
    'candlelit_dinner': 'best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest'
}

def fetch_page(lang, key, slug):
    lang_dir = os.path.join(CACHE_DIR, lang)
    os.makedirs(lang_dir, exist_ok=True)
    out_file = os.path.join(lang_dir, f"{key}.html")
    
    # If already cached and valid size (> 5KB)
    if os.path.exists(out_file) and os.path.getsize(out_file) > 5000:
        return (lang, key, "CACHED", os.path.getsize(out_file))

    url = f"https://www.budapestadventures.com/{lang}/{slug}"
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
    )
    
    for attempt in range(5):
        try:
            # Polite random pause to prevent rate limiting
            time.sleep(random.uniform(0.3, 0.6))
            with urllib.request.urlopen(req, timeout=15) as resp:
                if resp.status == 200:
                    html = resp.read().decode('utf-8', errors='ignore')
                    with open(out_file, 'w', encoding='utf-8') as f:
                        f.write(html)
                    return (lang, key, "SUCCESS", len(html))
                else:
                    return (lang, key, f"HTTP_{resp.status}", 0)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait_time = (attempt + 1) * 3 + random.uniform(1.0, 3.0)
                time.sleep(wait_time)
                continue
            return (lang, key, f"HTTP_{e.code}", 0)
        except Exception as e:
            time.sleep(2)
            continue
            
    return (lang, key, "FAILED_AFTER_RETRIES", 0)

def main():
    tasks = []
    for lang in LANGS:
        for key, slug in PAGES.items():
            tasks.append((lang, key, slug))

    print(f"Starting harvest of {len(tasks)} tasks across {len(LANGS)} languages with 3 polite workers...")
    
    success = 0
    cached = 0
    failed = 0

    with ThreadPoolExecutor(max_workers=3) as executor:
        future_map = {executor.submit(fetch_page, lang, key, slug): (lang, key) for lang, key, slug in tasks}
        for future in as_completed(future_map):
            lang, key, status, size = future.result()
            if status == "SUCCESS":
                success += 1
                if (success + cached) % 15 == 0 or (success + cached) == len(tasks):
                    print(f"[{success + cached}/{len(tasks)}] Downloaded {lang}/{key} ({size:,} bytes)")
            elif status == "CACHED":
                cached += 1
            else:
                failed += 1
                print(f"[FAIL] {lang}/{key} -> {status}")

    print("\n=======================================================")
    print(f"HARVEST FINISHED:")
    print(f"  Successfully downloaded: {success}")
    print(f"  Already cached:          {cached}")
    print(f"  Failed:                  {failed}")
    print(f"  Total target pages:      {len(tasks)}")
    print("=======================================================")

if __name__ == '__main__':
    main()
