#!/usr/bin/env python3
"""Keep every page's "last updated" date honest, automatically.

A page carries its date in up to three places:
  * "<strong>Last updated</strong>: Nov 14, 2026"   (the pill in the hero)
  * "Updated 14 Nov 2026"                            (the author line)
  * "dateModified": "2026-11-14"                     (JSON-LD)

    python3 scripts/stamp_updated.py           # stamp pages whose content changed
    python3 scripts/stamp_updated.py --check   # fail if a changed page kept an old date (CI)
    python3 scripts/stamp_updated.py --page best-budapest-river-cruises.html   # force one page to today

A page counts as changed when its visible content differs from main (or from the last commit, for
uncommitted edits): text, links and images. Scripts, styles (inline or <link rel="stylesheet">), the synced menu and footer, and the dates
themselves are ignored, so a menu sync or a JS fix never makes a page look freshly updated.
Changed pages get today's date (Budapest time) in all three places. A page whose content matches main
but whose date went backwards (a builder re-run from an older base) gets main's date back.
Prose such as "prices checked 14 Nov 2026" is left alone: that is when facts were verified, not a page date.
"""
import argparse
import datetime as dt
import glob
import json
import os
import re
import subprocess
import sys
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
M = "|".join(MON)
PILL = re.compile(r"(<strong>Last updated</strong>: )(%s)[a-z]* (\d{1,2}), (\d{4})" % M)
AUTHOR = re.compile(r"(\bUpdated )(\d{1,2}) (%s)[a-z]* (\d{4})(?=\s*<)" % M)
LD = re.compile(r'("dateModified":\s*")(\d{4})-(\d{2})-(\d{2})')
STRIP = [re.compile(p, re.S | re.I) for p in (r"<script\b.*?</script>", r"<style\b.*?</style>",
                                              r"<link\b[^>]*\brel=\"stylesheet\"[^>]*>",
                                              r'<header class="ltt-navbar".*?</header>', r"<footer\b.*?</footer>",
                                              r"<!--.*?-->")]


def git(*args):
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def today():
    return dt.datetime.now(ZoneInfo("Europe/Budapest")).date()


def page_date(s):
    """The page's date: JSON-LD dateModified first, else the visible pill or author line."""
    m = LD.search(s)
    if m:
        return dt.date(int(m.group(2)), int(m.group(3)), int(m.group(4)))
    m = PILL.search(s)
    if m:
        return dt.date(int(m.group(4)), MON.index(m.group(2)) + 1, int(m.group(3)))
    m = AUTHOR.search(s)
    if m:
        return dt.date(int(m.group(4)), MON.index(m.group(3)) + 1, int(m.group(2)))
    return None


def all_dates(s):
    out = {dt.date(int(a), int(b), int(c)) for _, a, b, c in LD.findall(s)}
    out |= {dt.date(int(y), MON.index(mo) + 1, int(d)) for _, mo, d, y in PILL.findall(s)}
    out |= {dt.date(int(y), MON.index(mo) + 1, int(d)) for _, d, mo, y in AUTHOR.findall(s)}
    return out


def stamp(s, d):
    s = PILL.sub(lambda m: f"{m.group(1)}{MON[d.month - 1]} {d.day}, {d.year}", s)
    s = AUTHOR.sub(lambda m: f"{m.group(1)}{d.day} {MON[d.month - 1]} {d.year}", s)
    return LD.sub(lambda m: f"{m.group(1)}{d.isoformat()}", s)


def content(s):
    for p in STRIP:
        s = p.sub(" ", s)
    s = PILL.sub(" ", s)
    s = AUTHOR.sub(" ", s)
    return re.sub(r"\s+", " ", s).strip()


def base_ref(check):
    """main to compare with: origin/main locally (merge base), the PR's base branch in CI."""
    if os.environ.get("GITHUB_ACTIONS"):
        if os.environ.get("GITHUB_EVENT_NAME") != "pull_request":
            return None, "push to main: nothing to compare with"
        b = os.environ.get("GITHUB_BASE_REF") or "main"
        if git("fetch", "--quiet", "--depth=1", "origin", b) is None:
            return None, f"could not fetch origin/{b}"
        return git("rev-parse", "FETCH_HEAD").strip(), f"origin/{b}"
    git("fetch", "--quiet", "origin", "main")
    mb = git("merge-base", "HEAD", "origin/main")
    return (mb.strip(), "origin/main (merge base)") if mb else (None, "no origin/main")


def show(ref, path):
    return git("show", f"{ref}:{path}") if ref else None


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="report only; exit 1 when a changed page has an old date")
    ap.add_argument("--page", action="append", default=[], help="also stamp this page with today's date (e.g. one changed before this script existed)")
    a = ap.parse_args()
    ref, why = base_ref(a.check)
    if not ref:
        print(f"stamp_updated: skipped ({why})")
        return 0
    now = today()
    pages = sorted(p for p in glob.glob(os.path.join(ROOT, "*.html")) + glob.glob(os.path.join(ROOT, "[a-z][a-z]", "*.html")))
    stamped, restored, problems = [], [], []
    for path in pages:
        rel = os.path.relpath(path, ROOT)
        with open(path, encoding="utf-8") as f:
            cur = f.read()
        d = page_date(cur)
        if d is None:
            continue
        base = show(ref, rel)
        head = None if os.environ.get("GITHUB_ACTIONS") else show("HEAD", rel)
        if base is None:  # new page: date it when it is first written
            changed, bd = (head is None or content(head) != content(cur)), None
        else:
            bd = page_date(base)
            changed = content(base) != content(cur) or (head is not None and content(head) != content(cur))
        new = None
        if rel in a.page and d != now:
            new = now
        elif changed and (bd is None or d <= bd) and d != now:
            new = now
        elif not changed and bd and d < bd:
            new = bd
        if len(all_dates(cur)) > 1 and new is None:
            new = max(all_dates(cur))  # the pill, the author line and JSON-LD disagree: use the newest
        if new is None:
            continue
        if a.check:
            why_ = ("content changed" if changed and new == now else
                    "date went backwards from main's" if bd and d < bd and not changed else "pill, author line and JSON-LD disagree")
            problems.append(f"{rel}: {why_}: shows {', '.join(sorted(x.isoformat() for x in all_dates(cur)))}, should be {new.isoformat()}")
            continue
        with open(path, "w", encoding="utf-8") as f:
            f.write(stamp(cur, new))
        (stamped if new == now else restored).append(f"{rel} -> {new.isoformat()}")
    if a.check:
        for p in problems:
            print("stale date:", p)
        print(f"stamp_updated --check vs {why}: {len(problems)} page(s) need a new date"
              + ("; run python3 scripts/stamp_updated.py" if problems else ""))
        return 1 if problems else 0
    for x in stamped + restored:
        print("stamped:", x)
    print(f"stamp_updated vs {why}: {len(stamped)} stamped today, {len(restored)} restored")
    return 0


if __name__ == "__main__":
    sys.exit(main())
