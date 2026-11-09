# -*- coding: utf-8 -*-
"""
Helper and validation script for Group 1 translations (HU, DE, FR, ES, IT, NL, PT)
for Budapest Dinner Cruises.
"""
import json
import os

PAYLOAD_PATH = "/Users/adamdimitrov/Development/budapest-adventures/data/dinner_source_payload_en.json"
OUTPUT_PATH = "/Users/adamdimitrov/Development/budapest-adventures/data/dinner_i18n_group1.json"

with open(PAYLOAD_PATH, "r", encoding="utf-8") as f:
    PAYLOAD_EN = json.load(f)

def validate_lang_dict(lang, data):
    assert "h4_headings" in data, f"{lang} missing h4_headings"
    assert isinstance(data["h4_headings"], dict), f"{lang} h4_headings is not dict"
    assert len(data["h4_headings"]) == len(PAYLOAD_EN["h4_headings"]), f"{lang} h4_headings len mismatch: {len(data['h4_headings'])} vs {len(PAYLOAD_EN['h4_headings'])}"
    for k in PAYLOAD_EN["h4_headings"]:
        assert k in data["h4_headings"], f"{lang} missing h4 key: {k}"

    assert "captions" in data, f"{lang} missing captions"
    assert isinstance(data["captions"], list), f"{lang} captions is not list"
    assert len(data["captions"]) == len(PAYLOAD_EN["captions"]), f"{lang} captions len mismatch: {len(data['captions'])} vs {len(PAYLOAD_EN['captions'])}"

    assert "leaf_lis" in data, f"{lang} missing leaf_lis"
    assert isinstance(data["leaf_lis"], list), f"{lang} leaf_lis is not list"
    assert len(data["leaf_lis"]) == len(PAYLOAD_EN["leaf_lis"]), f"{lang} leaf_lis len mismatch: {len(data['leaf_lis'])} vs {len(PAYLOAD_EN['leaf_lis'])}"

    assert "bios" in data, f"{lang} missing bios"
    assert isinstance(data["bios"], dict), f"{lang} bios is not dict"
    for k in PAYLOAD_EN["bios"]:
        assert k in data["bios"], f"{lang} missing bio key: {k}"

    assert "undercover_notes" in data, f"{lang} missing undercover_notes"
    assert isinstance(data["undercover_notes"], dict), f"{lang} undercover_notes is not dict"
    for k in PAYLOAD_EN["undercover_notes"]:
        assert k in data["undercover_notes"], f"{lang} missing undercover key: {k}"

    assert "transit_lines" in data, f"{lang} missing transit_lines"
    assert isinstance(data["transit_lines"], dict), f"{lang} transit_lines is not dict"
    for k in PAYLOAD_EN["transit_lines"]:
        assert k in data["transit_lines"], f"{lang} missing transit key: {k}"

    assert "bento_titles" in data, f"{lang} missing bento_titles"
    assert isinstance(data["bento_titles"], dict), f"{lang} bento_titles is not dict"
    for k in PAYLOAD_EN["bento_titles"]:
        assert k in data["bento_titles"], f"{lang} missing bento key: {k}"

    print(f"Validation PASSED for {lang}!")
