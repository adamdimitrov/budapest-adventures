#!/usr/bin/env python3
"""Things to do: add the Viator rating where the same operator sells the same product there
(matched by Viator's supplier name, read 2026-11-20), and recompute the weighted average like
the Legenda card. Card 7 takes the Viator + Tripadvisor rows of the same cruise from the night
cruise page. Cards without a same-operator Viator product keep their single rating.

    python3 scripts/ttd_viator_ratings.py && python3 scripts/listicle.py build best-things-to-do-budapest.html
"""
import importlib.util, json, os, re, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "listicles", "best-things-to-do-budapest.json")
NIGHT = os.path.join(ROOT, "data", "listicles", "best-night-cruises-budapest.json")
SUB = "best_things_to_do_budapest"
VIATOR = {  # card: (viator path, exact score, review count, supplier)
    "card-2": ("/tours/Budapest/Private-Entrance-to-Szechenyi-Spa-in-Budapest-with-Optional-Massage/d499-5808SZECHENYI", 3.8, 2395),
    "card-6": ("/tours/Budapest/Budapest-St-Stephens-Basilica-Skip-The-Line-Tickets/d499-5808P211", 4.6, 226),
    "card-9": ("/tours/Budapest/Budapest-City-Park-True-Crime-of-Hungary-Night-Walking-Tour/d499-425820P9", 4.9, 15),
    "card-11": ("/tours/Budapest/Budapest-Jewish-Heritage-Walking-Tour/d499-5808JEWISH", 4.8, 642),
    "card-12": ("/tours/Budapest/Foodapest-Originals-24-Food-Tour-Off-The-Beaten-Path/d499-387012P5", 4.9, 838),
    "card-14": ("/tours/Budapest/Small-Group-Electric-Scooter-Tour-of-Budapest/d499-43748P1", 5.0, 1898),
    "card-21": ("/tours/Budapest/Budapest-St-Stephens-Basilica-Organ-Concert-with-Optional-Danube-River-Dinner-Cruise/d499-5808ORGAN", 4.2, 198),
    "card-22": ("/tours/Budapest/Budapest-Palatinus-Bath-Full-Day-Admission/d499-5808P202", 3.5, 27),
}


def count_of(s):
    s = s.strip("()+ ").replace(",", "")
    return float(s[:-1]) * 1000 if s.lower().endswith("k") else float(s)


def fmt(n):
    return f"({n / 1000:.1f}k+)".replace(".0k", "k") if n >= 1000 else f"({int(n):,})"


def tp(campaign, p, url, slug):
    return (f"https://tp.media/r?campaign_id={campaign}&marker=404154&p={p}&sub_id={SUB}_{slug}&trs=204442&u="
            + urllib.parse.quote(url, safe=""))


def recompute(r):
    sites = r["sites"]
    tot = sum(count_of(s["count"]) for s in sites)
    avg = sum(float(s["score"]) * count_of(s["count"]) for s in sites) / tot
    r["stars"] = f"{avg:.2f}"
    r["score"] = f"{avg:.1f}"
    r["meta"] = f"{fmt(tot)[1:-1]} reviews · {len(sites)} sites"
    r["heading"] = f"Average of {len(sites)} booking sites, weighted by number of reviews"


def main():
    d = json.load(open(DATA))
    night = json.load(open(NIGHT))
    cruise = next(c for c in night["cards"] if "t416276" in c["cta"]["btn"]["url"])
    for c in d["cards"]:
        r = c["reviews"]["ratings"]
        if any(s["site"] == "Viator" for s in r["sites"]):
            continue
        slug = re.sub(r"[^a-z0-9]+", "_", re.sub(r"<[^>]+>|&[a-z#0-9]+;", "", c["title"]["text"].lower())).strip("_")
        if c["id"] in VIATOR:
            path, score, n = VIATOR[c["id"]]
            r["sites"].append({"kind": "link", "site": "Viator", "score": f"{score:.1f}", "count": fmt(n),
                               "url": tp(47, 1922, "https://www.viator.com" + path, slug),
                               "rel": "noopener nofollow sponsored", "target": "_blank"})
        elif c["id"] == "card-7":
            for s in cruise["reviews"]["ratings"]["sites"]:
                if s["site"] in ("Viator", "Tripadvisor"):
                    s = dict(s)
                    s["url"] = re.sub(r"sub_id=[^&]+", f"sub_id={SUB}_{slug}", s["url"])
                    r["sites"].append(s)
        else:
            continue
        recompute(r)
        print(c["id"], r["score"], r["meta"])
    spec = importlib.util.spec_from_file_location("k", os.path.join(ROOT, "kit", "scripts", "listicle.py"))
    k = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(k)
    open(DATA, "w").write(k.dumps(d) + "\n")


if __name__ == "__main__":
    main()
