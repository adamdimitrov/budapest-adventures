from scripts.compile_all_languages_luxury import extract_tour_content, LANGS
import json

harvested = {}
for l in LANGS:
    if l == "hu": continue
    path = f"data/harvested_html/{l}/dinner.html"
    tours = extract_tour_content(path, "dinner")
    harvested[l] = []
    for t in tours:
        harvested[l].append({
            "title": t["clean_title"],
            "pros": t["pros"],
            "cons": t["cons"]
        })

print(f"Harvested data collected for {len(harvested)} languages.")
print(f"Sample German Tour 1 Title: {harvested['de'][0]['title']}")
print(f"Sample German Tour 1 Pros count: {len(harvested['de'][0]['pros'])}")
print(f"Sample German Tour 1 Cons count: {len(harvested['de'][0]['cons'])}")
