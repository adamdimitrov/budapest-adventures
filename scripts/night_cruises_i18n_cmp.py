#!/usr/bin/env python3
"""After port_page_i18n.py: give each translated night-cruises page its own GYG cmp tag
(cmp=<lang>-night-cruises-<placement>-<card>), since the port copies EN links verbatim."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = {"hu": "hu/legjobb-éjszakai-hajóutak-budapest/index.html", "de": "de/nacht-bootsfahrten-budapest/index.html",
         "nl": "nl/avondcruises-boedapest/index.html", "fr": "fr/croisieres-nocturnes-budapest/index.html",
         "it": "it/crociere-notturne-budapest/index.html", "es": "es/cruceros-nocturnos-budapest/index.html"}
for lang, rel in FILES.items():
    p = os.path.join(ROOT, rel)
    html = open(p, encoding="utf-8").read()
    n = html.count("cmp=en-night-cruises-")
    open(p, "w", encoding="utf-8").write(html.replace("cmp=en-night-cruises-", "cmp=%s-night-cruises-" % lang))
    print(lang, n)
