#!/usr/bin/env python3
"""Add Google and Tripadvisor rating badges to the hotel cards (next to Booking.com).

Scores come from scripts/data/hotel_ratings.json (each hotel's own Google place and Tripadvisor
listing, matched by name and address). Booking.com stays the first badge and the booking link;
Google is shown as a plain badge (no link), Tripadvisor links through Travelpayouts like the
Tripadvisor badges on best-budapest-river-cruises. The star summary becomes the review-weighted
average on a 5-point scale (Booking.com /10 halved).

Idempotent: re-run after a page rebuild.

    python3 scripts/hotel_ratings.py && python3 scripts/listicle.py build <page> (done for each page here)
"""
import json
import os
import subprocess
import sys
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ["where-to-stay-in-budapest", "best-hotels-budapest", "best-luxury-hotels-budapest", "best-boutique-hotels-budapest",
         "best-spa-hotels-budapest", "best-cheap-hotels-budapest", "best-airport-hotels-budapest"]
GOOGLE_ICON = "/assets/cdn/67d02edca7795b0f57073b59/67ebc6e4688dbf65f4077122_google-logo.avif"


def fmt(n):
    if n >= 1000:
        return f"{n / 1000:.1f}".rstrip("0").rstrip(".") + "k+"
    if n >= 100:
        return f"{n // 10 * 10}+"
    return str(n)


def parse(c):
    c = c.strip("()").replace(",", "")
    if c.endswith("k+"):
        return int(float(c[:-2]) * 1000)
    return int(c.rstrip("+"))


def ta_link(url, sub):
    return (f"https://tp.media/r?campaign_id=149&marker=404154&p=4456&sub_id={sub}&trs=204442"
            f"&u={quote(url, safe='')}")


def main():
    data = json.load(open(os.path.join(ROOT, "scripts", "data", "hotel_ratings.json"), encoding="utf-8"))["hotels"]
    for page in PAGES:
        spec = json.load(open(os.path.join(ROOT, "scripts", "articles", page + ".json"), encoding="utf-8"))
        slugs = [it["_slug"] for it in spec["items"]]
        dpath = os.path.join(ROOT, "data", "listicles", page + ".json")
        d = json.load(open(dpath, encoding="utf-8"))
        for card, slug in zip(d["cards"], slugs):
            r = card["reviews"]["ratings"]
            booking = next(s for s in r["sites"] if s["site"] == "Booking.com")
            sites = [booking]
            h = data.get(slug, {})
            if "google" in h:
                g = h["google"]
                sites.append({"kind": "static", "site": "Google", "score": g["score"], "count": f"({fmt(g['count'])})",
                              "icon": GOOGLE_ICON})
            if "tripadvisor" in h:
                t = h["tripadvisor"]
                sites.append({"kind": "link", "site": "Tripadvisor", "score": t["score"], "count": f"({fmt(t['count'])})",
                              "url": ta_link(t["url"], page.replace("-", "_") + "_" + slug.replace("-", "_")),
                              "rel": "noopener nofollow sponsored", "target": "_blank"})
            # weighted average on a 5-point scale; counts from the badges
            tot = w = 0.0
            for s in sites:
                n = parse(s["count"])
                v = float(s["score"]) / (2 if s["site"] == "Booking.com" else 1)
                tot += n
                w += v * n
            avg = w / tot
            exact = int(sum(parse(s["count"]) for s in sites))
            r.update({"stars": f"{avg:.2f}", "score": f"{avg:.1f}", "sites": sites,
                      "meta": f"{fmt(exact)} reviews · {len(sites)} site{'s' if len(sites) > 1 else ''}",
                      "heading": ("Average of " + str(len(sites)) + " sites, weighted by number of reviews "
                                  "(out of 5; Booking.com scores out of 10 are halved)") if len(sites) > 1
                      else "Rating on Booking.com (out of 10)"})
        open(dpath, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
        subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "listicle.py"), "build", os.path.join(ROOT, page + ".html")],
                       check=True)


if __name__ == "__main__":
    main()
