#!/usr/bin/env python3
"""Every affiliate / OTA link carries rel="nofollow sponsored noopener".

    python3 scripts/fix_affiliate_rel.py            # fix in place (idempotent)
    python3 scripts/fix_affiliate_rel.py --check    # report only, exit 1 if anything is missing
    python3 scripts/fix_affiliate_rel.py --report   # per-file counts: affiliate links / missing rel

What it walks: every published .html / .js file (anything .vercelignore does
not exclude), every Python generator (root *.py and scripts/**), and the i18n
port data (data/i18n/**/*.json), so regenerated pages keep the rel.

For each <a> tag whose href points at an affiliate or OTA host (see
AFFILIATE_HOSTS, plus any external host carrying a partner/ref/aid/... query
parameter), the tokens nofollow, sponsored and noopener are merged into the
existing rel. Other rel tokens are kept, nothing is duplicated, and the href,
its tracking parameters, target and the link text are never touched. A tag
that already has all three tokens is left byte-for-byte as it is.

The official thermal-bath ticket sites (BATH_BOOKING_HOSTS) are not
affiliates: they get rel="nofollow noopener" only (a stray "sponsored" is removed).

Generator templates whose href is a placeholder ({url}, %s, ' + x + ') are
covered when the tag is clearly an affiliate slot: it already says
"sponsored", or it is a rating badge (bpa-rev-badge).

Runtime: bpa-tracking.js applies the same rule (AFFILIATE_REL) to links it
decorates and to links clicked later, so links injected by JS are covered too.
"""

import argparse
import os
import re
import subprocess
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sync_layout import vercel_ignored  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SELF = "scripts/fix_affiliate_rel.py"

AFFILIATE_REL = ("nofollow", "sponsored", "noopener")
BATH_REL = ("nofollow", "noopener")

# Host suffixes: the host itself or any subdomain of it.
AFFILIATE_HOSTS = (
    # OTAs / marketplaces
    "getyourguide.com", "gyg.me", "viator.com", "tiqets.com", "fareharbor.com",
    "booking.com", "hostelworld.com", "klook.com", "civitatis.com", "musement.com",
    "expedia.com", "agoda.com", "hotels.com", "airbnb.com",
    # Travelpayouts redirect / short-link domains
    "tp.st", "tp.media", "tpm.lv", "tpk.lv", "travelpayouts.com",
    # Direct operator partners (partner/code/affi/ref links)
    "legenda.hu", "budapestrivercruise.eu", "budapestrivercruise.com", "silver-line.hu",
    "budapestxplore.com", "guruwalk.com",
)
TRIPADVISOR = re.compile(r"(^|\.)tripadvisor\.[a-z.]+$")

BATH_BOOKING_HOSTS = (
    "tickets.szechenyibath.hu", "tickets.gellertbath.hu", "tickets.rudasfurdo.hu",
    "tickets.lukacsfurdo.hu", "tickets.palatinusstrand.hu", "tickets.dandarfurdo.hu",
    "tickets.kiralyfurdo.hu", "budapestgyogyfurdoi.hu",
)

# Own sites and plain reference hosts: never affiliate, even with a ?ref=-style param.
NEVER = (
    "budapestadventures.com", "thecruisedetective.com", "luxurytraveltester.com",
    "cruisedetective.store", "google.com", "goo.gl", "youtube.com", "youtu.be",
    "instagram.com", "tiktok.com", "facebook.com", "apple.com", "wa.me",
    "googleapis.com", "gstatic.com", "cloudflare.com", "jsdelivr.net",
)
PARTNER_PARAMS = {"partner", "partner_id", "partnerid", "aid", "affi", "affid", "affiliate",
                  "affiliate_id", "ref", "pid", "marker", "code", "mcid", "awinaffid"}

TAG = re.compile(r"<a\b(?:[^>\"']|\"[^\"]*\"|'[^']*')*>", re.I)
HREF = re.compile(r"""\bhref\s*=\s*(\\?["'])(.*?)\1""", re.I | re.S)
REL = re.compile(r"""\brel\s*=\s*(\\?["'])(.*?)\1""", re.I | re.S)
CLASS = re.compile(r"""\bclass\s*=\s*(\\?["'])(.*?)\1""", re.I | re.S)
TARGET = re.compile(r"""\s+target\s*=""", re.I)
TEMPLATED = re.compile(r"\{|%s|%\(|'\s*\+|\"\s*\+|\$\{")


def host_match(host, suffixes):
    return any(host == s or host.endswith("." + s) for s in suffixes)


def classify(href, tag):
    """'aff', 'bath' or None for the <a> tag's href."""
    raw = href.replace("&amp;", "&").replace("\\/", "/").strip()
    if TEMPLATED.search(raw) and not re.match(r"(https?:)?//[\w.-]+\.[a-z]{2,}[/?]", raw):
        cls = CLASS.search(tag)
        rel = REL.search(tag)
        if rel and "sponsored" in rel.group(2).split():
            return "aff"
        if cls and "bpa-rev-badge" in cls.group(2).split():
            return "aff"
        return None
    if raw.startswith("//"):
        raw = "https:" + raw
    if not re.match(r"https?://", raw, re.I):
        return None
    try:
        u = urllib.parse.urlsplit(raw)
    except ValueError:
        return None
    host = (u.hostname or "").lower()
    if not host or host_match(host, NEVER):
        return None
    if host_match(host, BATH_BOOKING_HOSTS):
        return "bath"
    if host_match(host, AFFILIATE_HOSTS) or TRIPADVISOR.search(host):
        return "aff"
    keys = {k.lower() for k, _ in urllib.parse.parse_qsl(u.query, keep_blank_values=True)}
    if keys & PARTNER_PARAMS:
        return "aff"
    return None


def merged_rel(existing, required):
    toks = existing.split()
    seen, out = set(), []
    for t in list(required) + toks:
        k = t.lower()
        if k not in seen:
            seen.add(k)
            out.append(t if k not in required else k)
    return " ".join(out)


def fix_tag(tag):
    """(new_tag, kind, was_missing)."""
    hm = HREF.search(tag)
    if not hm:
        return tag, None, False
    kind = classify(hm.group(2), tag)
    if not kind:
        return tag, None, False
    required = AFFILIATE_REL if kind == "aff" else BATH_REL
    forbidden = () if kind == "aff" else ("sponsored",)
    rm = REL.search(tag)
    if rm:
        have = {t.lower() for t in rm.group(2).split()}
        if all(r in have for r in required) and not have & set(forbidden):
            return tag, kind, False
        q = rm.group(1)
        kept = " ".join(t for t in rm.group(2).split() if t.lower() not in forbidden)
        new = tag[:rm.start()] + f"rel={q}{merged_rel(kept, required)}{q}" + tag[rm.end():]
        return new, kind, True
    q = hm.group(1)
    attr = f"rel={q}{' '.join(required)}{q}"
    tm = TARGET.search(tag)
    if tm:
        new = tag[:tm.start()] + " " + attr + tag[tm.start():]
    else:
        end = len(tag) - (2 if tag.endswith("/>") else 1)
        sep = "" if tag[end - 1].isspace() else " "
        new = tag[:end] + sep + attr + tag[end:]
    return new, kind, True


def process(text, code=False):
    """code=True for .py/.js/.json sources: only single-line tags, so a match
    never spans program code between two string literals."""
    stats = {"aff": 0, "bath": 0, "missing": 0}

    def sub(m):
        if code and "\n" in m.group(0):
            return m.group(0)
        new, kind, missing = fix_tag(m.group(0))
        if kind:
            stats[kind] += 1
            stats["missing"] += missing
        return new

    return TAG.sub(sub, text), stats


def files():
    out = subprocess.run(
        ["git", "-c", "core.quotepath=off", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT, capture_output=True, text=True, check=True).stdout.split("\0")
    ignored = vercel_ignored()
    for f in sorted(set(out)):
        if not f or f == SELF or not os.path.isfile(os.path.join(ROOT, f)):
            continue
        if f.startswith((".claude/", ".github/", "node_modules/", "data/harvested_html/")):
            continue
        if f.endswith(".py") and not f.startswith("tests/"):
            yield f
        elif f.startswith("data/i18n/") and f.endswith(".json"):
            yield f
        elif f.endswith((".html", ".htm", ".js")) and not f.endswith(".min.js") and not ignored(f):
            yield f


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="write nothing, exit 1 if any affiliate link lacks the rel")
    ap.add_argument("--report", action="store_true", help="write nothing, print per-file counts as TSV")
    args = ap.parse_args()

    bad, changed, tot = [], 0, {"aff": 0, "bath": 0, "missing": 0}
    if args.report:
        print("file\taffiliate_links\tbath_booking_links\tmissing_rel")
    for f in files():
        path = os.path.join(ROOT, f)
        try:
            with open(path, encoding="utf-8") as fh:
                s = fh.read()
        except UnicodeDecodeError:
            continue
        if "<a" not in s and "<A" not in s:
            continue
        new, st = process(s, code=not f.endswith((".html", ".htm")))
        for k in tot:
            tot[k] += st[k]
        if args.report and (st["aff"] or st["bath"]):
            print(f"{f}\t{st['aff']}\t{st['bath']}\t{st['missing']}")
        if st["missing"]:
            bad.append((f, st["missing"]))
            if not (args.check or args.report):
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(new)
                changed += 1

    summary = (f"{tot['aff']} affiliate + {tot['bath']} bath-booking links, "
               f"{tot['missing']} missing rel in {len(bad)} files")
    if args.report:
        print(f"# {summary}", file=sys.stderr)
        return 0
    if args.check:
        if bad:
            for f, n in bad:
                print(f"  {f}: {n} affiliate link(s) without rel=\"nofollow sponsored noopener\"")
            print(f"FAIL: {summary}. Fix with: python3 scripts/fix_affiliate_rel.py")
            return 1
        print(f"OK: {summary}")
        return 0
    print(f"Fixed {summary}; {changed} files written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
