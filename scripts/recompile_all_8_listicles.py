#!/usr/bin/env python3
"""
Recompile all 8 Budapest Adventures listicles with complete, authentic Quick Facts.
"""

import subprocess
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path('/Users/adamdimitrov/Development/budapest-adventures')
COMPILER = Path('/Users/adamdimitrov/.gemini/config/skills/luxury-editorial-system/scripts/compile_webflow_article.py')
CFG_DIR = Path('/Users/adamdimitrov/.gemini/config/skills/luxury-editorial-system/configs')

ARTICLES = [
    ("budapest_river_cruises.json", "river.html"),
    ("budapest_dinner_cruises.json", "dinner.html"),
    ("budapest_night_cruises.json", "best-night-cruises-budapest.html"),
    ("budapest_private_boats.json", "best-private-boat-tours-budapest.html"),
    ("budapest_unlimited_prosecco.json", "unlimited-prosecco-cruises-budapest.html"),
    ("budapest_thermal_baths.json", "thermal-baths-budapest.html"),
    ("budapest_walking_tours.json", "best-walking-tours-budapest.html"),
    ("budapest_hostels.json", "best-hostels-budapest.html")
]

def main():
    print("Compiling all 8 listicles...")
    for cfg_name, html_name in ARTICLES:
        src_path = ROOT / html_name
        cfg_path = CFG_DIR / cfg_name
        out_path = ROOT / html_name
        
        cmd = [
            "python3", str(COMPILER),
            "--source", str(src_path),
            "--config", str(cfg_path),
            "--output", str(out_path)
        ]
        
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"FAILED {html_name}: {res.stderr[:300]}")
        else:
            print(f"✓ COMPILED {html_name}")

    print("\n--- Verifying Quick Facts across all 8 files ---")
    for _, html_name in ARTICLES:
        path = ROOT / html_name
        soup = BeautifulSoup(open(path, encoding='utf-8'), 'html.parser')
        qfs = soup.select('.qf1-wrap')
        details = soup.select('details.bpa-details-card')
        
        total_rows = 0
        total_chips = 0
        for qf in qfs:
            total_rows += len(qf.select('.qf1-row'))
            total_chips += len(qf.select('.qf1-chip'))
            
        avg_rows = (total_rows / len(qfs)) if qfs else 0
        avg_chips = (total_chips / len(qfs)) if qfs else 0
        print(f"{html_name:40s}: {len(details)} details | {len(qfs)} QF cards | avg {avg_rows:.1f} rows/card | avg {avg_chips:.1f} chips/card")

if __name__ == "__main__":
    main()
