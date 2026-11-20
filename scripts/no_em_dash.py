#!/usr/bin/env python3
"""Replace em dashes in a page's text (house rule: no em dashes), leaving <style> blocks alone.

    python3 scripts/no_em_dash.py page.html [data/listicles/page.json ...]

"</strong> — x" -> "</strong>: x", "Quick Facts — x" -> "Quick Facts: x", "X — photo 3" -> "X, photo 3",
any other " — " -> ", ", a bare "—" between words -> ", ". JSON files get the same text rules.
"""
import re
import sys


def fix(t):
    t = t.replace("</strong> — ", "</strong>: ").replace("</b> — ", "</b>: ")
    t = re.sub(r"Quick Facts — ", "Quick Facts: ", t)
    t = re.sub(r" — (photo \d+)", r", \1", t)
    t = t.replace(" — ", ", ").replace(" —", ",").replace("— ", "").replace("—", ", ")
    return t


for path in sys.argv[1:]:
    s = open(path, encoding="utf-8").read()
    parts = re.split(r"(<style\b.*?</style>)", s, flags=re.S)
    out = "".join(p if p.startswith("<style") else fix(p) for p in parts)
    if out != s:
        open(path, "w", encoding="utf-8").write(out)
        print(f"{path}: {s.count('—') - out.count('—')} em dashes replaced")
