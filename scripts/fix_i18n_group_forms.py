#!/usr/bin/env python3
"""Make the translated group booking forms actually send, and drop promises
that can't be guaranteed.

The old Webflow form has no handler since webflow.js stopped loading, so a
submit just reloads the page. This rewires it to formsubmit (same endpoint as
/contact and the EN group page) and removes the "same-day quote" and
"no markup" items from the how-it-works list. Idempotent.

    python3 scripts/fix_i18n_group_forms.py [--check]
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORMSUBMIT = "https://formsubmit.co/el/vojuru"
PAGES = [
    "bg/grupovi-rezervatsii-kruiz-budapeshta", "cs/skupinova-rezervace-plavby-budapest",
    "de/gruppenbuchung-bootsfahrt-budapest", "el/omadikes-kratiseis-krouaziera-voudapesti",
    "es/reserva-grupos-cruceros-budapest", "fr/reservation-groupe-croisiere-budapest",
    "he/hazmana-kvutsatit-shayit-budapest", "hr/grupne-rezervacije-krstarenja-budimpesta",
    "hu/budapest-nagy-csoportos-hajokirandulas", "it/prenotazione-gruppi-crociera-budapest",
    "ja/budapesuto-kuruzu-dantai-yoyaku", "ko/budapeseuteu-keulujeu-danche-yeyak",
    "nl/groepsboeking-cruise-boedapest", "pl/rezerwacja-grupowa-rejsy-budapeszt",
    "pt/reserva-grupo-cruzeiros-budapeste", "ro/rezervari-grup-croaziere-budapesta",
    "ru/gruppovoe-bronirovanie-kruizov-budapesht", "sk/skupinova-rezervacia-plavby-budapest",
    "sr/grupne-rezervacije-krstarenja-budimpesta", "tr/grup-tekne-turu-rezervasyonu-budapeste",
    "uk/hrupove-bronyuvannya-kruiziv-budapesht",
]

TRACK = ("<script>(function(){var f=document.getElementById('email-form');if(!f)return;"
         "f.addEventListener('submit',function(){"
         "try{if(window.fbq)fbq('track','Lead',{content_name:'group_booking'});}catch(e){}"
         "try{if(window.gtag)gtag('event','generate_lead',{form:'group_booking'});}catch(e){}"
         "});})();</script>")


def fix(h: str, lang: str) -> str:
    # 1. how-it-works list: keep items 1 and 4, drop same-day quote (2) and no markup (3)
    m = re.search(r"<p>(?:(?!</p>).)*✅(?:(?!</p>).)*</p>", h, re.S)
    if m and m.group(0).count("✅") == 4:
        parts = m.group(0).split("<br/>✅")
        assert len(parts) == 5, lang
        h = h.replace(m.group(0), "<br/>✅".join([parts[0], parts[1], parts[4]]), 1)

    # 2. form: Webflow GET form -> formsubmit POST
    old_open = re.search(r'<form data-name="Email Form"[^>]*>', h)
    if old_open:
        subject = f"[Budapest Adventures] Group cruise request ({lang.upper()})"
        hidden = (
            '<input autocomplete="off" name="_gotcha" style="position:absolute;left:-9999px;opacity:0;'
            'width:1px;height:1px" tabindex="-1" type="text"/>'
            f'<input name="_subject" type="hidden" value="{subject}"/>'
            '<input name="_template" type="hidden" value="table"/>'
            '<input name="_captcha" type="hidden" value="false"/>'
            f'<input name="language" type="hidden" value="{lang}"/>'
        )
        h = h.replace(old_open.group(0),
                      f'<form action="{FORMSUBMIT}" id="email-form" method="POST" name="email-form">' + hidden, 1)
        for old, new, req in [("Name-Touch", "name", True), ("Email-Touch", "email", True),
                              ("Message-Touch", "message", True)]:
            h = h.replace(f'name="{old}"', f'name="{new}"' + (' required=""' if req else ""), 1)
        h = h.replace('<div class="w-form-formrecaptcha g-recaptcha g-recaptcha-error '
                      'g-recaptcha-disabled g-recaptcha-invalid-key"></div>', "", 1)

    # 3. lead tracking
    if "content_name:'group_booking'" not in h:
        h = h.replace("</body>", TRACK + "</body>", 1)
    return h


def main() -> None:
    check = "--check" in sys.argv
    bad = 0
    for slug in PAGES:
        p = ROOT / slug / "index.html"
        h = p.read_text()
        new = fix(h, slug.split("/")[0])
        problems = []
        if "data-wf-page-id" in new.split("<form", 1)[-1].split("</form>", 1)[0]:
            problems.append("webflow form left")
        if FORMSUBMIT not in new:
            problems.append("no formsubmit")
        if new.count("✅") != 2:
            problems.append(f"{new.count('✅')} ticks")
        if problems:
            bad += 1
        print(f"{slug[:2]} {'changed' if new != h else 'ok'} {' '.join(problems)}")
        if not check and new != h:
            p.write_text(new)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
