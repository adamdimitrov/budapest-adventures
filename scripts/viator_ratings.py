#!/usr/bin/env python3
"""Add a Viator rating row to cards rated only on GetYourGuide, where the same operator sells the
same product on Viator (scripts/data/viator_matches.json, matched on title and supplier, read
2026-11-20), and recompute the weighted average like the Legenda card. Idempotent.

    python3 scripts/viator_ratings.py && python3 scripts/listicle.py build <page>.html ...
"""
import importlib.util, json, os, re, sys, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MATCHES = os.path.join(ROOT, "scripts", "data", "viator_matches.json")


def count_of(s):
    s = s.strip("()+ ").replace(",", "")
    return float(s[:-1]) * 1000 if s.lower().endswith("k") else float(s)


def fmt(n):
    return f"({n / 1000:.1f}k+)".replace(".0k", "k") if n >= 1000 else f"({int(n):,})"


def main():
    spec = importlib.util.spec_from_file_location("k", os.path.join(ROOT, "kit", "scripts", "listicle.py"))
    kit = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(kit)
    m = {k: v for k, v in json.load(open(MATCHES)).items() if not k.startswith("_")}
    pages = sorted({k.split("#")[0] for k in m})
    for pg in pages:
        path = os.path.join(ROOT, "data", "listicles", pg + ".json")
        d = json.load(open(path))
        done = 0
        for c in d["cards"]:
            v = m.get(f"{pg}#{c['id']}")
            r = (c.get("reviews") or {}).get("ratings")
            if not v or not r or any(s["site"] == "Viator" for s in r["sites"]):
                continue
            vpath, score, n = v
            if not n:
                continue
            slug = re.sub(r"[^a-z0-9]+", "_", re.sub(r"<[^>]+>|&[a-z#0-9]+;", "", c["title"]["text"].lower())).strip("_")[:40]
            url = ("https://tp.media/r?campaign_id=47&marker=404154&p=1922&sub_id=" + pg.replace("-", "_") + "_" + slug
                   + "&trs=204442&u=" + urllib.parse.quote("https://www.viator.com" + vpath, safe=""))
            r["sites"].append({"kind": "link", "site": "Viator", "score": f"{score:.1f}", "count": fmt(n), "url": url,
                               "rel": "noopener nofollow sponsored", "target": "_blank"})
            tot = sum(count_of(s["count"]) for s in r["sites"])
            avg = sum(float(s["score"]) * count_of(s["count"]) for s in r["sites"]) / tot
            r["stars"], r["score"] = f"{avg:.2f}", f"{avg:.1f}"
            r["meta"] = f"{fmt(tot)[1:-1]} reviews · {len(r['sites'])} sites"
            r["heading"] = f"Average of {len(r['sites'])} booking sites, weighted by number of reviews"
            done += 1
        open(path, "w").write(kit.dumps(d) + "\n")
        print(pg, done)


if __name__ == "__main__":
    main()
