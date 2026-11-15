#!/usr/bin/env python3
"""After port_page_i18n.py: give each translated thermal-baths page its own affiliate tags
(GYG cmp=<lang>-thermal-baths-<placement>-<bath>, Viator campaign=<lang>-thermal-baths-...),
since the port copies the EN links verbatim."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = {"hu": "hu/legjobb-termalfurdok-budapest/index.html", "de": "de/thermalbaeder-budapest/index.html",
         "fr": "fr/bains-thermaux-budapest/index.html", "nl": "nl/thermaalbaden-boedapest/index.html",
         "it": "it/terme-budapest/index.html", "es": "es/banos-termales-budapest/index.html"}
for lang, rel in FILES.items():
    p = os.path.join(ROOT, rel)
    html = open(p, encoding="utf-8").read()
    n = html.count("=en-thermal-baths-")
    open(p, "w", encoding="utf-8").write(html.replace("=en-thermal-baths-", "=%s-thermal-baths-" % lang))
    print(lang, n)
