#!/usr/bin/env python3
"""Fix the legacy floating CTA bar (global-sticky-cta) on all pages.

1. Bar text: drop the emoji prefix; on non-English pages use the card's own
   translated booking label instead of the hardcoded English "Check Availability".
2. Brand names: restore the original company/brand names in card names
   (.coin-shortname), which the bar shows. Descriptive names such as
   "100E airport bus" or "Bolt (Uber alternative)" stay translated.

Idempotent. Run: python3 scripts/fix_floating_bars.py
"""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

OLD_NAME = "const currentName = '👉 ' + nameEl.innerText;"
NEW_NAME = "const currentName = nameEl.innerText;"
OLD_LABEL = re.compile(r"(text\.innerText = currentName;\s*btn\.href = btnEl\.href;)(?!\s*var pl)")
NEW_LABEL = (" var pl = (document.documentElement.lang || 'en').slice(0, 2).toLowerCase(); "
             r"if (pl !== 'en') { var bl = (btnEl.innerText || '').split(/[\u2192\u2190\n]/)[0].trim(); "
             r"if (bl) btn.innerText = bl; }")

BRANDS = {
    "Silverline Cruises": ["Crociere Silverline", "Croisières Silverline", "Cruceros Silverline", "Cruzeiros Silverline",
                           "Rejsy Silverline", "Silverline Kreuzfahrten", "Silverline krstarenja", "Silverline plavby",
                           "Silverline-cruises", "Κρουαζιέρες Silverline", "Круизы Silverline", "Круїзи Silverline",
                           "סיילברליין קרוז", "シルバーラインクルーズ", "실버라인 크루즈"],
    "Legenda City Cruises": ["Crociere della città di Legenda", "Croisières Legenda City", "Cruceros por la ciudad de Legenda",
                             "Cruzeiros da Cidade Legenda", "Legenda Stadscruises", "Legenda Şehir Turları",
                             "Rejsy po mieście Legenda", "Міські круїзи Legenda", "レジェンダ シティ クルーズ", "레전다 시티 크루즈"],
    "Portum Lines Cruising": ["Croazieră Portum Lines", "Crociera Portum Lines", "Croisière Portum Lines", "Cruzeiro Portum Lines",
                              "Líneas de crucero Portum", "Portum Lines Cruise", "Portum Lines Cruisen", "Portum Lines Kreuzfahrten",
                              "Portum Lines Seyir", "Portum Lines krstarenje", "Portum Lines körutazás", "Rejs liniami Portum",
                              "Круизы Portum Lines", "Круїз Portum Lines", "שייט פורטום קווים", "ポルタムラインクルージング", "포텀 라인 크루징"],
    "Hungaria Koncert": ["Hungria Koncert", "ハンガリーコンサート", "헝가리 콘서트"],
    "Rubin Group": ["루빈 그룹"],
    "Budapest Boat Party": ["ブダペスト ボートパーティー", "부다페스트 보트 파티"],
    "Mysterium Tours": ["Mysterium túrák", "Recorridos por el misterio", "Мистериум Тоурс"],
    "BudapestTours": ["Budapesti túrák", "Excursiones por Budapest", "БудапестТоурс"],
    "GoZeppelin Tours": ["GoZeppelin túrák", "Excursiones GoZeppelin", "ГоЗеппелин Тоурс"],
    "Cityrama Budapest": ["El Cityrama de Budapest", "Цитирама Будапест"],
    "Tourist Angel Smc": ["Ángel Turístico Smc", "Туристички анђео Смц"],
    "Duna-Weser Kft.": ["Дуна-Везер Кфт.", "Дуна-Весер Кфт.", 'דונה-וסר בע"מ', "두나-베저 주식회사"],
    "Dunai Sétahajózási Ltd.": ["Dunai Setahajózási Ltd.", "Dunai Sétahajózási Ltda.", "Дунаи Сетахајозаси Лтд.",
                                "ООО «Дунай Сетахаджозаси»", "두나이 세타하호자시 유한회사"],
    "Avenue Hostel": ["Avenue szálló"],
    "Zen Hostel": ["Zen Szálló"],
    "Adagio 2.0 Basilica": ["Adagio 2.0 Bazilika"],
}
TO_ORIGINAL = {v: k for k, vs in BRANDS.items() for v in vs}
SHORTNAME = re.compile(r'(<(\w+)[^>]*class="[^"]*coin-shortname[^"]*"[^>]*>)(.*?)(</\2>)', re.S)


def fix_names(s):
    def sub(m):
        inner = re.sub(r"\s+", " ", m.group(3)).strip()
        key = inner.replace("&quot;", '"')
        if key in TO_ORIGINAL:
            return m.group(1) + TO_ORIGINAL[key].replace("&", "&amp;") + m.group(4)
        return m.group(0)
    return SHORTNAME.sub(sub, s)


def main():
    files = subprocess.run(["git", "-c", "core.quotepath=off", "ls-files", "*.html"], cwd=ROOT,
                           capture_output=True, text=True).stdout.split("\n")
    changed = 0
    for f in filter(None, files):
        p = ROOT / f
        s = p.read_text(encoding="utf-8")
        t = s.replace(OLD_NAME, NEW_NAME)
        t = OLD_LABEL.sub(lambda m: m.group(1) + NEW_LABEL, t)
        if "coin-shortname" in t:
            t = fix_names(t)
        if t != s:
            p.write_text(t, encoding="utf-8")
            changed += 1
    print("changed", changed)


if __name__ == "__main__":
    main()
