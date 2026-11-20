#!/usr/bin/env python3
"""PageSpeed fixes that every page inherits from its template, applied site-wide.

    python3 scripts/pagespeed.py            # apply all three steps below, in order
    python3 scripts/pagespeed.py fonts|has|css
    python3 scripts/pagespeed.py --check    # CI (kit/checks/check_pagespeed.py): fail if a page needs a step

1. fonts  Old Webflow pages load Google Fonts through webfont.js (a render-blocking or async script
          that downloads EVERY weight it lists, 38 files on Budapest Adventures). The same Google Fonts
          stylesheet is linked instead, without blocking render: the browser then downloads only the
          faces the page really uses, so the look is unchanged. Nothing on the sites reads the wf-*
          classes webfont.js used to set (checked before this step was written).
2. has    `body:has(.x)` makes the browser re-check the whole page on every DOM change (sliders,
          filters, popovers). For the selectors listed in site.json pagespeed.static_has (elements
          that are in the page's HTML and never added or removed by JS) the rule is rewritten to a
          class on <body> (`body.ps-has-x`), and every page's <body> gets exactly the classes of the
          elements it contains. Dynamic conditions (an open drawer...) are never listed and stay.
3. css    A `<style id="X">` block that is byte-identical on many pages (site.json
          pagespeed.shared_css_min_pages, default 20) is served from /css/shared/ instead (cached for a
          year; the file name carries a content hash, so a changed block never meets an old cached copy).
          Neighbouring shared blocks are joined into one file (fewer render-blocking requests), in the
          same place and order, so the cascade is unchanged. Not joined: blocks scripts/sync_layout.py
          copies from the language masters (they keep `<link id="X">`, which the sync finds), and blocks
          that could leak into a neighbour (unclosed brace or comment, @import, @charset). Blocks with
          relative url(...) stay inline.

A site opts in with site.json "pagespeed": {"static_has": [...], "shared_css_min_pages": 20};
without it the check is skipped.

Editing a shared block: `python3 scripts/pagespeed.py unpack <page>...` (no page: every page) puts the
blocks back inline; edit them (on the language master for synced blocks, then scripts/sync_layout.py),
then run this script again: the copies move to a new file. A script that edits blocks in place runs
unpack first. Never edit a file in css/shared/ in place (year-long cache).
"""
import argparse
import collections
import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "checks"))
from sitecfg import ROOT, SITE, published_html  # noqa: E402

CFG = SITE.get("pagespeed", {})
MIN_PAGES = int(CFG.get("shared_css_min_pages", 20))
STATIC_HAS = list(CFG.get("static_has", []))
SHARED_DIR = "css/shared"

# ------------------------------------------------------------------ helpers
def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def write(rel, text):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def pages():
    return [p for p in published_html() if not p.startswith(SHARED_DIR)]


# ------------------------------------------------------------------ 1. fonts
WEBFONT_SRC = r'https://ajax\.googleapis\.com/ajax/libs/webfont/[0-9.]+/webfont\.js'
FAMILIES = r'\{\s*google:\s*\{\s*families:\s*(\[[^\]]*\])\s*\}\s*\}'
# the two shapes Webflow wrote: async loader + WebFontConfig, or blocking loader + WebFont.load
FONT_PATTERNS = [
    re.compile(r'<script(?: type="text/javascript")?>\s*WebFontConfig\s*=\s*' + FAMILIES + r'\s*;?\s*</script>\s*'
               r'<script async(?:="")? src="' + WEBFONT_SRC + r'"(?: type="text/javascript")?>\s*</script>'),
    re.compile(r'<script src="' + WEBFONT_SRC + r'" type="text/javascript"></script>\s*'
               r'<script type="text/javascript">\s*WebFont\.load\(\s*' + FAMILIES + r'\s*\);?\s*</script>'),
]
ANY_WEBFONT = re.compile(r'webfont/[0-9.]+/webfont\.js|WebFont\.load\(|WebFontConfig\s*=')


def font_link(families_json):
    import json
    fams = json.loads(families_json)
    q = "|".join(f.replace(" ", "+") for f in fams)
    href = "https://fonts.googleapis.com/css?family=" + q + "&amp;display=swap"
    # same as webfont.js: without JS the page keeps the system fonts
    return f'<link href="{href}" media="print" onload="this.media=\'all\'" rel="stylesheet"/>'


def fix_fonts(s):
    for pat in FONT_PATTERNS:
        s = pat.sub(lambda m: font_link(m.group(1)), s)
    return s


# ------------------------------------------------------------------ 2. has
def has_class(sel):
    return "ps-has-" + re.sub(r"[^a-z0-9]+", "-", sel.lower()).strip("-")


def _sel_re(sel):
    m = re.fullmatch(r"([a-z][a-z0-9]*)?\.([A-Za-z0-9_-]+)", sel)
    if not m:
        raise SystemExit(f"site.json pagespeed.static_has: only tag.class or .class selectors, not {sel!r}")
    tag, cls = m.groups()
    return re.compile(r"<%s\b[^>]*\bclass=\"(?:[^\"]*\s)?%s(?:\s[^\"]*)?\"" % (tag or r"[a-z][a-z0-9]*", re.escape(cls)))


INERT = re.compile(r"<(script|style|template|noscript)\b.*?</\1>|<!--.*?-->", re.S | re.I)


def present(s, sels):
    dom = INERT.sub("", s)
    return {sel for sel in sels if _sel_re(sel).search(dom)}


def rewrite_has_css(css):
    """body:has(S) and body:is(:has(S),...) -> body classes, only for selectors in static_has."""
    def one(m):
        sel = m.group(1)
        return "body." + has_class(sel) if sel in STATIC_HAS else m.group(0)

    def many(m):
        inner = re.findall(r":has\(([^()]+)\)", m.group(1))
        if not inner or any(x not in STATIC_HAS for x in inner):
            return m.group(0)
        return "body:is(" + ",".join("." + has_class(x) for x in inner) + ")"
    css = re.sub(r"body:is\(((?::has\([^()]+\)\s*,?\s*)+)\)", many, css)
    return re.sub(r"body:has\(([^()]+)\)", one, css)


STYLE_RE = re.compile(r"(<style\b[^>]*>)(.*?)(</style>)", re.S)
BODY_RE = re.compile(r"<body\b[^>]*>")


def set_body_classes(s, want):
    m = BODY_RE.search(s)
    if not m:
        return s
    tag = m.group(0)
    cm = re.search(r'\bclass="([^"]*)"', tag)
    old = cm.group(1).split() if cm else []
    keep = [c for c in old if not c.startswith("ps-has-")]
    new = keep + sorted(has_class(x) for x in want)
    if new == old:
        return s
    if cm:
        tag2 = tag[:cm.start()] + 'class="%s"' % " ".join(new) + tag[cm.end():] if new else tag[:cm.start()].rstrip() + tag[cm.end():]
    else:
        tag2 = tag[:-1].rstrip("/") + ' class="%s">' % " ".join(new)
    return s[:m.start()] + tag2 + s[m.end():]


def fix_has(s):
    if not STATIC_HAS:
        return s
    s = STYLE_RE.sub(lambda m: m.group(1) + rewrite_has_css(m.group(2)) + m.group(3), s)
    return set_body_classes(s, present(s, STATIC_HAS))


# ------------------------------------------------------------------ 3. css
BLOCK_RE = re.compile(r'<style id="([A-Za-z0-9_-]+)">(.*?)</style>', re.S)
SHARED_LINK_RE = re.compile(r'<link [^>]*href="/%s/([^"]+)"[^>]*>' % SHARED_DIR)
RELATIVE_URL = re.compile(r"url\((?!\s*['\"]?\s*(?:data:|https?:|/|#))", re.I)


def shared_name(bid, css):
    return f"{bid}.{hashlib.sha256(css.encode('utf-8')).hexdigest()[:10]}.css"


def link_tag(bid, css):
    return f'<link id="{bid}" rel="stylesheet" href="/{SHARED_DIR}/{shared_name(bid, css)}"/>'


def existing_shared():
    d = os.path.join(ROOT, SHARED_DIR)
    return set(os.listdir(d)) if os.path.isdir(d) else set()


def standalone_ids():
    """Blocks scripts/sync_layout.py copies from the language masters keep their own file
    (it finds them by id), so they are never joined into a bundle."""
    import json
    try:
        cfg = json.load(open(os.path.join(ROOT, "scripts", "layout_config.json"), encoding="utf-8"))
    except (OSError, ValueError):
        return set()
    out = set()
    for b in cfg.get("sync_blocks", []):
        m = re.fullmatch(r'<style id="([^"]+)">', b.get("open", ""))
        if m:
            out.add(m.group(1))
    return out


STANDALONE = standalone_ids()


# a bundle marks where each block starts and the whitespace that stood before it in the page,
# so `unpack` gives back the page byte for byte
GAP = {"\n": "n", " ": "s", "\t": "t", "\r": "r"}
MARK_RE = re.compile(r"/\*ps-block:([A-Za-z0-9_-]+):([nstr]*)\*/\n")


def mark(bid, gap):
    return f"/*ps-block:{bid}:{''.join(GAP[c] for c in gap)}*/\n"


def unpack(s):
    """Shared links back to the inline <style id> blocks they came from (for scripts that edit a
    block in place; run this script again afterwards)."""
    def back(m):
        tag, name = m.group(0), m.group(1)
        css = read(f"{SHARED_DIR}/{name}")
        if name.startswith("bundle."):
            back_gap = {v: k for k, v in GAP.items()}
            parts = MARK_RE.split(css)[1:]
            return "".join("".join(back_gap[c] for c in parts[i + 1]) + f'<style id="{parts[i]}">{parts[i + 2]}</style>'
                           for i in range(0, len(parts), 3))
        bid = re.search(r'id="([^"]+)"', tag).group(1)
        return f'<style id="{bid}">{css}</style>'
    return SHARED_LINK_RE.sub(back, s)


def safe_to_join(css):
    """A block can be joined with its neighbours only if it cannot leak into them: braces and
    comments closed, no @import/@charset (those must start a stylesheet)."""
    if re.search(r"@(import|charset)\b", css, re.I):
        return False
    t = re.sub(r'"(?:[^"\\\n]|\\.)*"|\'(?:[^\'\\\n]|\\.)*\'', "", css)
    t, n = re.subn(r"/\*.*?\*/", "", t, flags=re.S)
    if "/*" in t or "*/" in t:
        return False
    depth = 0
    for ch in t:
        depth += (ch == "{") - (ch == "}")
        if depth < 0:
            return False
    return depth == 0


def shared_blocks(texts):
    """(id, css) pairs to serve as files: inline on >= MIN_PAGES pages, or already a file."""
    count = collections.Counter()
    for s in texts.values():
        for m in BLOCK_RE.finditer(s):
            count[(m.group(1), m.group(2))] += 1
    files = existing_shared()
    out = set()
    for (bid, css), n in count.items():
        if RELATIVE_URL.search(css) or "</" in css:
            continue
        if n >= MIN_PAGES or shared_name(bid, css) in files:
            out.add((bid, css))
    return out


def fix_css(s, share, files_out=None):
    """Each run of neighbouring shared blocks becomes ONE stylesheet (fewer render-blocking
    requests), in the same place and order, so the cascade is unchanged."""
    runs, cur, last_end = [], [], None
    for m in BLOCK_RE.finditer(s):
        key = (m.group(1), m.group(2))
        if key not in share:
            if cur:
                runs.append(cur)
            cur, last_end = [], None
            continue
        joinable = m.group(1) not in STANDALONE and safe_to_join(m.group(2))
        if cur and last_end is not None and not s[last_end:m.start()].strip() and cur[-1][1] and joinable:
            cur.append((m, joinable))
        else:
            if cur:
                runs.append(cur)
            cur = [(m, joinable)]
        last_end = m.end()
    if cur:
        runs.append(cur)
    out, pos = [], 0
    for run in runs:
        first, last = run[0][0], run[-1][0]
        if len(run) == 1:
            bid, css = first.group(1), first.group(2)
            name, tag = shared_name(bid, css), link_tag(bid, css)
        else:
            ids = [m.group(1) for m, _ in run]
            gaps = [""] + [s[a[0].end():b[0].start()] for a, b in zip(run, run[1:])]
            css = "".join(mark(m.group(1), g) + m.group(2) for (m, _), g in zip(run, gaps))
            name = shared_name("bundle", css)
            tag = (f'<link id="ps-{name[7:17]}" data-ps-blocks="{" ".join(ids)}" rel="stylesheet" '
                   f'href="/{SHARED_DIR}/{name}"/>')
        if files_out is not None:
            files_out[name] = css
        out.append(s[pos:first.start()])
        out.append(tag)
        pos = last.end()
    out.append(s[pos:])
    return "".join(out)


# ------------------------------------------------------------------ run
def run(steps, check):
    if "pagespeed" not in SITE:
        print('pagespeed: skipped (no "pagespeed" in site.json; see kit/scripts/pagespeed.py)')
        return 0
    rels = pages()
    texts = {r: read(r) for r in rels}
    out = dict(texts)
    if "fonts" in steps:
        out = {r: fix_fonts(s) for r, s in out.items()}
    if "has" in steps:
        out = {r: fix_has(s) for r, s in out.items()}
    share, css_files = set(), {}
    if "css" in steps:
        share = shared_blocks(out)
        out = {r: fix_css(s, share, css_files) for r, s in out.items()}
    changed = [r for r in rels if out[r] != texts[r]]
    files = existing_shared()
    new_files = sorted(set(css_files) - files)
    problems = []
    for r in rels:
        if ANY_WEBFONT.search(out[r]):
            problems.append(f"{r}: loads webfont.js in a shape this script does not know; link the Google Fonts CSS instead")
        for m in SHARED_LINK_RE.finditer(out[r]):
            if m.group(1) not in files and m.group(1) not in css_files:
                problems.append(f"{r}: links /{SHARED_DIR}/{m.group(1)}, which does not exist")
    if check:
        for r in changed:
            steps_needed = [st for st in steps if (st == "fonts" and fix_fonts(texts[r]) != texts[r])
                            or (st == "has" and fix_has(texts[r]) != texts[r])
                            or (st == "css" and fix_css(texts[r], share) != texts[r])]
            problems.append(f"{r}: needs `python3 scripts/pagespeed.py` ({', '.join(steps_needed) or 'fonts/has/css'})")
        for f in new_files:
            problems.append(f"/{SHARED_DIR}/{f} missing: run python3 scripts/pagespeed.py")
        for p in problems:
            print(p)
        print(f"pagespeed: {len(rels)} page(s) checked, {len(problems)} problem(s)")
        return 1 if problems else 0
    for name in new_files:
        write(f"{SHARED_DIR}/{name}", css_files[name])
    for r in changed:
        write(r, out[r])
    for p in problems:
        print(p)
    print(f"pagespeed: {len(changed)} page(s) updated, {len(new_files)} shared CSS file(s) written")
    return 1 if problems else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("steps", nargs="*", help="fonts, has, css (default: all three, in that order), "
                    "or: unpack PAGE... (shared CSS links back to inline blocks)")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if a.steps[:1] == ["unpack"]:
        for rel in a.steps[1:] or pages():
            s = read(rel)
            s2 = unpack(s)
            if s2 != s:
                write(rel, s2)
                print(f"unpacked {rel}")
        return
    bad = [x for x in a.steps if x not in ("fonts", "has", "css")]
    if bad:
        ap.error(f"unknown step(s): {', '.join(bad)}")
    steps = [x for x in ("fonts", "has", "css") if x in (a.steps or ["fonts", "has", "css"])]
    sys.exit(run(steps, a.check))


if __name__ == "__main__":
    main()
