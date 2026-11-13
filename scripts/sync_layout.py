#!/usr/bin/env python3
"""Keep the site menu (header) and footer identical on every page of a language.

The master copies live on the tourism statistics pages:
  EN: budapest-tourism-statistics.html
  HU: hu/budapest-turizmus-statisztika/index.html

To change the menu or footer site-wide, edit it on the master page for that
language, then run:

    python3 scripts/sync_layout.py --langs en,hu          # write changes
    python3 scripts/sync_layout.py --langs en,hu --check  # report only

What it syncs on each published page (sitemap.xml URLs) of the given languages:
  * <style id="ltt-nav-styles">, <header class="ltt-navbar"> (incl. the mobile
    drawer) and <script id="ltt-nav-script">
  * the footer (new <footer class="ltt-footer"> or the old Webflow
    <section class="footer-dark"><div class="footer-section">) plus the
    <style id="bpa-new-footer"> rules it needs
The language switcher on each page keeps the master's languages (EN/HU), but
its links point at that page's own EN/HU versions (from its hreflang tags),
falling back to the language homepage.
"""
import argparse
import json
import os
import re
import sys
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.budapestadventures.com"
MASTERS = {"en": "budapest-tourism-statistics.html", "hu": "hu/budapest-turizmus-statisztika/index.html"}
HOMES = {"en": "/", "hu": "/hu"}

PAT_STYLE = re.compile(r'<style id="ltt-nav-styles">.*?</style>', re.S)
PAT_HEADER = re.compile(r'<header[^>]*class="ltt-navbar".*?</header>', re.S)
PAT_SCRIPT = re.compile(r'<script id="ltt-nav-script">.*?</script>', re.S)
PAT_FOOTER_NEW = re.compile(r'<footer class="footer-dark ltt-footer".*?</footer>', re.S)
PAT_FOOTER_OLD = re.compile(r'<section class="footer-dark">\s*<div class="footer-section">.*?</section>', re.S)
PAT_FOOTER_CSS = re.compile(r'<style id="bpa-new-footer">.*?</style>', re.S)
LINGUANA_CSS = '<link href="https://static.linguana.io/public/linguana_switcher.min.css" rel="stylesheet" type="text/css"/>'


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def rewrites():
    cfg = json.loads(read("vercel.json"))
    return {r["source"]: r["destination"] for r in cfg.get("rewrites", []) if ":" not in r["source"]}


def url_to_file(path, rw):
    path = urllib.parse.unquote(path).rstrip("/") or "/"
    for p in (path, rw.get(path)):
        if not p:
            continue
        cands = ["index.html"] if p == "/" else [p.lstrip("/") + ".html", p.lstrip("/") + "/index.html"]
        for c in cands:
            if os.path.exists(os.path.join(ROOT, c)):
                return c
    return None


def page_lang(s):
    m = re.search(r'<html[^>]*\blang="([a-z-]+)"', s)
    return m.group(1) if m else None


def alternates(s):
    return {m.group(2): m.group(1).replace(SITE, "") or "/"
            for m in re.finditer(r'<link href="(https://www\.budapestadventures\.com[^"]*)" hreflang="([a-z-]+)" rel="alternate"/>', s)}


def point_switcher(header, alt):
    for code in HOMES:
        href = alt.get(code, HOMES[code])
        header = re.sub(rf'(<a [^>]*data-(?:m-)?lang="{code}"[^>]*href=")[^"]*(")', rf"\g<1>{href}\2", header)
        header = re.sub(rf'(<a [^>]*href=")[^"]*("[^>]*data-(?:m-)?lang="{code}")', rf"\g<1>{href}\2", header)
    return header


def replace_once(s, pat, new):
    m = pat.search(s)
    if not m:
        return s, False
    return s[:m.start()] + new + s[m.end():], True


def sync_page(s, master, alt):
    changed = []
    for name, pat in (("nav-styles", PAT_STYLE), ("nav-script", PAT_SCRIPT)):
        s2, ok = replace_once(s, pat, pat.search(master).group())
        if ok and s2 != s:
            changed.append(name)
        s = s2
    hdr = point_switcher(PAT_HEADER.search(master).group(), alt)
    s2, ok = replace_once(s, PAT_HEADER, hdr)
    if not ok:
        raise ValueError("no ltt-navbar header")
    if s2 != s:
        changed.append("header")
    s = s2

    foot = PAT_FOOTER_NEW.search(master).group()
    if PAT_FOOTER_NEW.search(s):
        s2, _ = replace_once(s, PAT_FOOTER_NEW, foot)
    elif PAT_FOOTER_OLD.search(s):
        old = PAT_FOOTER_OLD.search(s).group()
        s2, _ = replace_once(s, PAT_FOOTER_OLD, foot + (LINGUANA_CSS if LINGUANA_CSS in old else ""))
    else:
        raise ValueError("no footer found")
    if s2 != s:
        changed.append("footer")
    s = s2

    css = PAT_FOOTER_CSS.search(master).group()
    if PAT_FOOTER_CSS.search(s):
        s2, _ = replace_once(s, PAT_FOOTER_CSS, css)
    else:
        s2 = s.replace("</head>", css + "</head>", 1)
    if s2 != s:
        changed.append("footer-css")
    return s2, changed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--langs", default="en,hu")
    ap.add_argument("--check", action="store_true", help="report pages that differ, write nothing")
    args = ap.parse_args()
    langs = [x.strip() for x in args.langs.split(",") if x.strip()]
    for lg in langs:
        if lg not in MASTERS:
            sys.exit(f"no master page for language '{lg}'")
    masters = {lg: read(MASTERS[lg]) for lg in langs}
    rw = rewrites()
    sm = read("sitemap.xml")
    paths = re.findall(r"<loc>https://www\.budapestadventures\.com([^<]*)</loc>", sm)
    seen, todo, errors = set(), 0, []
    for p in paths:
        f = url_to_file(p, rw)
        if not f or f in seen:
            continue
        seen.add(f)
        s = read(f)
        lg = page_lang(s)
        if lg not in langs or f == MASTERS[lg]:
            continue
        try:
            new, changed = sync_page(s, masters[lg], alternates(s))
        except ValueError as e:
            errors.append(f"{f}: {e}")
            continue
        if changed:
            todo += 1
            print(f"{'would update' if args.check else 'updated'} {f}: {', '.join(changed)}")
            if not args.check:
                with open(os.path.join(ROOT, f), "w", encoding="utf-8") as fh:
                    fh.write(new)
    for e in errors:
        print("ERROR", e)
    print(f"{todo} page(s) {'out of sync' if args.check else 'updated'}, {len(errors)} error(s)")
    sys.exit(1 if (args.check and todo) or errors else 0)


if __name__ == "__main__":
    main()
