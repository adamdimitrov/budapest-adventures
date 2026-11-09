# -*- coding: utf-8 -*-
"""
Master compiler for Group 1 translations (HU, DE, FR, ES, IT, NL, PT)
for Budapest Dinner Cruises.
"""
import json
import os
import sys

sys.path.insert(0, '/Users/adamdimitrov/Development/budapest-adventures')

from scripts.dinner_group1_hu import HU_DATA
from scripts.dinner_group1_de import DE_DATA
from scripts.dinner_group1_fr import FR_DATA
from scripts.dinner_group1_es import ES_DATA
from scripts.dinner_group1_it import IT_DATA
from scripts.dinner_group1_nl import NL_DATA
from scripts.dinner_group1_pt import PT_DATA
from scripts.validate_dinner_group1 import validate_lang_dict, OUTPUT_PATH

GROUP1_MASTER = {
    "hu": HU_DATA,
    "de": DE_DATA,
    "fr": FR_DATA,
    "es": ES_DATA,
    "it": IT_DATA,
    "nl": NL_DATA,
    "pt": PT_DATA
}

def main():
    print("Validating all 7 Group 1 languages...")
    for lang, data in GROUP1_MASTER.items():
        validate_lang_dict(lang, data)

    print(f"Writing master JSON to: {OUTPUT_PATH}")
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(GROUP1_MASTER, f, ensure_ascii=False, indent=2)

    # Re-read and verify validity
    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        verified = json.load(f)

    assert set(verified.keys()) == {"hu", "de", "fr", "es", "it", "nl", "pt"}
    size_kb = os.path.getsize(OUTPUT_PATH) / 1024
    print(f"Successfully generated and verified {OUTPUT_PATH} ({size_kb:.2f} KB)")

if __name__ == "__main__":
    main()
