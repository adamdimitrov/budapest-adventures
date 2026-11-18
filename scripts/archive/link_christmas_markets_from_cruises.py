#!/usr/bin/env python3
"""Add (or refresh) the link from every Christmas cruises page to the Christmas markets guide.
Idempotent: the sentence sits in <p class="xm-backlink"> at the end of the hero lead."""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import build_private_boats as bp  # noqa: E402

EN = "/budapest-christmas-markets"
LINKS = {
    "christmas-cruises-budapest.html": ("Visiting the Christmas markets too? My <a href=\"%s\">Budapest Christmas markets 2026 guide</a> has the dates, 24 to 31 December hours and prices." % EN),
    "de/weihnachts-bootsfahrten-budapest/index.html": "Auch auf den Weihnachtsmarkt? Mein <a href=\"/de/weihnachtsmarkt-budapest\">Ratgeber Weihnachtsmarkt Budapest 2026</a> hat Termine, Öffnungszeiten vom 24. bis 31. Dezember und Preise.",
    "es/cruceros-navidad-budapest/index.html": "¿También vas a los mercadillos? Mi <a href=\"/es/mercadillo-navideno-budapest\">guía de los mercadillos navideños de Budapest 2026</a> tiene fechas, horarios del 24 al 31 de diciembre y precios.",
    "cs/vanocni-plavby-budapest/index.html": "Chystáte se i na vánoční trhy? Můj <a href=\"%s\">průvodce vánočními trhy v Budapešti 2026</a> (v angličtině) uvádí termíny, otevírací doby a ceny." % EN,
    "hr/bozicna-krstarenja-budimpesta/index.html": "Idete i na božićne sajmove? Moj <a href=\"%s\">vodič kroz božićne sajmove u Budimpešti 2026</a> (na engleskom) donosi datume, radno vrijeme i cijene." % EN,
    "bg/koledni-kruizi-budapeshta/index.html": "Ще посетите и коледните базари? Моят <a href=\"%s\">пътеводител за коледните базари в Будапеща 2026</a> (на английски) има дати, работно време и цени." % EN,
    "el/christougenniatikes-krouazieres-voudapesti/index.html": "Θα πάτε και στις χριστουγεννιάτικες αγορές; Ο <a href=\"%s\">οδηγός μου για τις χριστουγεννιάτικες αγορές της Βουδαπέστης 2026</a> (στα αγγλικά) έχει ημερομηνίες, ωράρια και τιμές." % EN,
    "he/shayit-chag-hamolad-budapest/index.html": "מגיעים גם לשווקי חג המולד? <a href=\"%s\">המדריך שלי לשווקי חג המולד בבודפשט 2026</a> (באנגלית) כולל תאריכים, שעות פתיחה ומחירים." % EN,
}

for rel, text in LINKS.items():
    fn = os.path.join(ROOT, rel)
    s = open(fn, encoding="utf-8").read()
    s = re.sub(r'<p class="xm-backlink">.*?</p>', "", s, flags=re.S)
    i = s.index('<div class="ltt-lead-copy">')
    j = bp.balanced_end(s, i)
    k = s.rindex("</div>", i, j)
    s = s[:k] + '<p class="xm-backlink">%s</p>\n' % text + s[k:]
    open(fn, "w", encoding="utf-8").write(s)
    print("linked", rel)
