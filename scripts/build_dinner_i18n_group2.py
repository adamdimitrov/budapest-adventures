# -*- coding: utf-8 -*-
"""
Assembles and writes /Users/adamdimitrov/Development/budapest-adventures/data/dinner_i18n_group2.json
for languages: pl, cs, sk, ro, hr, sr, bg.
"""

import json
import os
import sys

sys.path.append('/Users/adamdimitrov/Development/budapest-adventures')

from scripts.i18n_group2_pl import DATA_PL
from scripts.i18n_group2_cs import DATA_CS
from scripts.i18n_group2_sk import DATA_SK
from scripts.i18n_group2_ro import DATA_RO
from scripts.i18n_group2_hr import DATA_HR
from scripts.i18n_group2_sr import DATA_SR
from scripts.i18n_group2_bg import DATA_BG

EN_PAYLOAD_PATH = '/Users/adamdimitrov/Development/budapest-adventures/data/dinner_source_payload_en.json'
OUTPUT_JSON_PATH = '/Users/adamdimitrov/Development/budapest-adventures/data/dinner_i18n_group2.json'

with open(EN_PAYLOAD_PATH, 'r', encoding='utf-8') as f:
    en_payload = json.load(f)

LANG_MAP = {
    'pl': DATA_PL,
    'cs': DATA_CS,
    'sk': DATA_SK,
    'ro': DATA_RO,
    'hr': DATA_HR,
    'sr': DATA_SR,
    'bg': DATA_BG
}

print(f"Validating {len(LANG_MAP)} languages against source payload...")

for lang, data in LANG_MAP.items():
    print(f"Checking {lang}...")
    assert len(data['captions']) == len(en_payload['captions']), f"[{lang}] captions len mismatch: {len(data['captions'])} vs {len(en_payload['captions'])}"
    assert len(data['leaf_lis']) == len(en_payload['leaf_lis']), f"[{lang}] leaf_lis len mismatch: {len(data['leaf_lis'])} vs {len(en_payload['leaf_lis'])}"
    assert set(data['h4_headings'].keys()) == set(en_payload['h4_headings']), f"[{lang}] h4_headings mismatch"
    assert set(data['bios'].keys()) == set(en_payload['bios'].keys()), f"[{lang}] bios mismatch"
    assert set(data['undercover_notes'].keys()) == set(en_payload['undercover_notes'].keys()), f"[{lang}] undercover_notes mismatch"
    assert set(data['transit_lines'].keys()) == set(en_payload['transit_lines'].keys()), f"[{lang}] transit_lines mismatch"
    assert set(data['bento_titles'].keys()) == set(en_payload['bento_titles'].keys()), f"[{lang}] bento_titles mismatch"

print("All validations PASSED! Writing output file...")

with open(OUTPUT_JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(LANG_MAP, f, ensure_ascii=False, indent=2)

file_size = os.path.getsize(OUTPUT_JSON_PATH)
print(f"File successfully written to {OUTPUT_JSON_PATH} ({file_size:,} bytes)")

# Re-read and verify validity
with open(OUTPUT_JSON_PATH, 'r', encoding='utf-8') as f:
    reloaded = json.load(f)

assert list(reloaded.keys()) == ['pl', 'cs', 'sk', 'ro', 'hr', 'sr', 'bg']
for lang in reloaded:
    assert len(reloaded[lang]['captions']) == 41
    assert len(reloaded[lang]['leaf_lis']) == 79
    assert len(reloaded[lang]['h4_headings']) == 46
    assert len(reloaded[lang]['bios']) == 7
    assert len(reloaded[lang]['undercover_notes']) == 2
    assert len(reloaded[lang]['transit_lines']) == 16
    assert len(reloaded[lang]['bento_titles']) == 31

print("Reload and integrity check 100% SUCCESSFUL!")
