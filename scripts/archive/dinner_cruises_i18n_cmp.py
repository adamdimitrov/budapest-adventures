#!/usr/bin/env python3
"""After port_page_i18n.py: give each translated dinner-cruises page its own affiliate tags
(GYG cmp=<lang>-dinner-cruises-<placement>-<product>), since the port copies the EN links verbatim."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = {"hu": "hu/setahajozas-a-dunan-vacsoraval/index.html",
         "de": "de/bootsfahrten-mit-abendessen-dunau-budapest/index.html",
         "nl": "nl/beste-diner-cruises-boedapest/index.html",
         "fr": "fr/diner-croisieres-danube-budapest/index.html",
         "it": "it/crociere-cena-danubio-budapest/index.html",
         "es": "es/cruceros-con-cena-danubio-budapest/index.html"}
for lang, rel in FILES.items():
    p = os.path.join(ROOT, rel)
    html = open(p, encoding="utf-8").read()
    n = html.count("=en-dinner-cruises-")
    open(p, "w", encoding="utf-8").write(html.replace("=en-dinner-cruises-", "=%s-dinner-cruises-" % lang))
    print(lang, n)
