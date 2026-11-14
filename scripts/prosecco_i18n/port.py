# -*- coding: utf-8 -*-
"""Full port for one or more languages:
tm.py apply -> port_page_i18n.py --dry-run (uses the cache) -> localize affiliate cmp/campaign -> check.
Usage: python3 scripts/prosecco_i18n/port.py de hu ...
"""
import os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import port_page_i18n as P
EN = "unlimited-prosecco-cruises-budapest.html"

def target(lang):
    return P.url_to_file(P.alternates(P.read(EN))[lang])

for lang in sys.argv[1:]:
    subprocess.run([sys.executable, "scripts/prosecco_i18n/tm.py", "apply", lang], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "scripts/port_page_i18n.py", EN, "--langs", lang, "--dry-run"], cwd=ROOT, check=True)
    t = target(lang)
    p = os.path.join(ROOT, t)
    s = open(p, encoding="utf-8").read()
    s = s.replace("cmp=en-prosecco-cruises-", f"cmp={lang}-prosecco-cruises-").replace("campaign=en-prosecco-cruises-", f"campaign={lang}-prosecco-cruises-")
    open(p, "w", encoding="utf-8").write(s)
    subprocess.run([sys.executable, "scripts/prosecco_i18n/check.py", f"{lang}={t}"], cwd=ROOT)
