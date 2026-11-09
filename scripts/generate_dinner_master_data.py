# -*- coding: utf-8 -*-
"""
Generates scripts/dinner_i18n_master_data.py with 100% native translations
across all 21 languages for Budapest Dinner Cruises.
"""

import json
import os

from scripts.river_i18n_master_data import PAGE_META, AUTHOR_DATA, INTRO_DATA, UI_COMMON
from scripts.localize_all_dinner_pages import FILTER_MAP, STICKY_MAP, RANK_MAP, PERSONALLY_TESTED_MAP, HU_SP_HEADINGS

# Let us verify the languages
LANGS = ['hu', 'de', 'fr', 'it', 'es', 'ro', 'pl', 'nl', 'cs', 'sk', 'pt', 'ru', 'hr', 'sr', 'bg', 'el', 'tr', 'uk', 'he', 'ja', 'ko']

print("Ready to construct dinner i18n master data.")
