#!/usr/bin/env python3
"""Make the tourism statistics charts embeddable.

For every <div class="bpa-chart" id="..."> on the statistics page in every language:
  * writes a standalone embed page to embed/<page path>/<chart id>.html
    (served at /embed/<page path>/<chart id>, frameable from any site, noindex)
  * adds an "Embed this chart" button under the chart on the page itself, which
    reveals a copy-paste snippet: the iframe plus a plain-text source link back
    to the statistics page (the backlink we want).

Re-run after editing the charts (it replaces what it added before):

    python3 scripts/build_stats_embeds.py
"""
import html
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.budapestadventures.com"

PAGES = [
    {
        "file": "budapest-tourism-statistics.html",
        "path": "/budapest-tourism-statistics",
        "lang": "en",
        "page_name": "Budapest tourism statistics",
        "source_tpl": 'Source: <a href="{url}">{name}</a> by Budapest Adventures, based on KSH data',
        "credit": "Chart by Budapest Adventures",
        "btn": "Embed this chart",
        "copy": "Copy code",
        "copied": "Copied!",
        "note": "Free to use on your site, article or report. Please keep the source link.",
    },
    {
        "file": "hu/budapest-turizmus-statisztika/index.html",
        "path": "/hu/budapest-turizmus-statisztika",
        "lang": "hu",
        "page_name": "Budapest turizmus statisztika",
        "source_tpl": 'Forrás: <a href="{url}">{name}</a>, Budapest Adventures, KSH adatok alapján',
        "credit": "Grafikon: Budapest Adventures",
        "btn": "Grafikon beágyazása",
        "copy": "Kód másolása",
        "copied": "Kimásolva!",
        "note": "Szabadon felhasználható weboldalon, cikkben vagy riportban. Kérjük, a forráslinket hagyd meg.",
    },
]

# Generated languages (scripts/build_stats_i18n.py). Labels: button, copy, copied, note, "Source", "by", credit.
EMBED_I18N = {
    "de": ("Grafik einbetten", "Code kopieren", "Kopiert!", "Frei nutzbar auf Ihrer Website, in Artikeln oder Berichten. Bitte den Quellenlink beibehalten.", "Quelle", "von Budapest Adventures, auf Basis von KSH-Daten", "Grafik: Budapest Adventures"),
    "fr": ("Intégrer ce graphique", "Copier le code", "Copié !", "Libre d'utilisation sur votre site, article ou rapport. Merci de garder le lien source.", "Source", "par Budapest Adventures, d'après les données du KSH", "Graphique : Budapest Adventures"),
    "it": ("Incorpora il grafico", "Copia il codice", "Copiato!", "Libero da usare su sito, articolo o report. Mantieni il link alla fonte.", "Fonte", "di Budapest Adventures, su dati KSH", "Grafico: Budapest Adventures"),
    "es": ("Insertar este gráfico", "Copiar código", "¡Copiado!", "Uso libre en tu web, artículo o informe. Mantén el enlace a la fuente.", "Fuente", "de Budapest Adventures, con datos de la KSH", "Gráfico: Budapest Adventures"),
    "ro": ("Încorporează graficul", "Copiază codul", "Copiat!", "Liber de folosit pe site, în articole sau rapoarte. Păstrează linkul către sursă.", "Sursa", "de la Budapest Adventures, pe baza datelor KSH", "Grafic: Budapest Adventures"),
    "pl": ("Osadź wykres", "Kopiuj kod", "Skopiowano!", "Możesz go używać na stronie, w artykule lub raporcie. Zachowaj link do źródła.", "Źródło", "Budapest Adventures, na podstawie danych KSH", "Wykres: Budapest Adventures"),
    "nl": ("Grafiek insluiten", "Code kopiëren", "Gekopieerd!", "Vrij te gebruiken op je site, in artikelen of rapporten. Laat de bronlink staan.", "Bron", "door Budapest Adventures, op basis van KSH-cijfers", "Grafiek: Budapest Adventures"),
    "cs": ("Vložit graf", "Kopírovat kód", "Zkopírováno!", "Volně k použití na webu, v článku nebo zprávě. Ponechte prosím odkaz na zdroj.", "Zdroj", "Budapest Adventures, podle dat KSH", "Graf: Budapest Adventures"),
    "sk": ("Vložiť graf", "Kopírovať kód", "Skopírované!", "Voľne na použitie na webe, v článku alebo správe. Ponechajte prosím odkaz na zdroj.", "Zdroj", "Budapest Adventures, podľa údajov KSH", "Graf: Budapest Adventures"),
    "pt": ("Incorporar gráfico", "Copiar código", "Copiado!", "Uso livre no seu site, artigo ou relatório. Mantenha a ligação à fonte.", "Fonte", "de Budapest Adventures, com dados do KSH", "Gráfico: Budapest Adventures"),
    "ru": ("Встроить график", "Скопировать код", "Скопировано!", "Можно свободно использовать на сайте, в статье или отчёте. Сохраните ссылку на источник.", "Источник", "Budapest Adventures, по данным KSH", "График: Budapest Adventures"),
    "hr": ("Ugradi grafikon", "Kopiraj kod", "Kopirano!", "Slobodno za upotrebu na webu, u članku ili izvješću. Zadržite poveznicu na izvor.", "Izvor", "Budapest Adventures, prema podacima KSH-a", "Grafikon: Budapest Adventures"),
    "sr": ("Угради графикон", "Копирај код", "Копирано!", "Слободно за употребу на сајту, у чланку или извештају. Задржите линк ка извору.", "Извор", "Budapest Adventures, према подацима KSH", "Графикон: Budapest Adventures"),
    "bg": ("Вграждане на графиката", "Копирай кода", "Копирано!", "Свободна употреба на сайт, в статия или доклад. Моля, запазете връзката към източника.", "Източник", "Budapest Adventures, по данни на KSH", "Графика: Budapest Adventures"),
    "el": ("Ενσωμάτωση γραφήματος", "Αντιγραφή κώδικα", "Αντιγράφηκε!", "Ελεύθερη χρήση σε ιστότοπο, άρθρο ή αναφορά. Διατηρήστε τον σύνδεσμο της πηγής.", "Πηγή", "από Budapest Adventures, με στοιχεία KSH", "Γράφημα: Budapest Adventures"),
    "tr": ("Grafiği yerleştir", "Kodu kopyala", "Kopyalandı!", "Sitenizde, makalenizde veya raporunuzda serbestçe kullanabilirsiniz. Lütfen kaynak bağlantısını koruyun.", "Kaynak", "Budapest Adventures, KSH verilerine dayanır", "Grafik: Budapest Adventures"),
    "uk": ("Вбудувати графік", "Скопіювати код", "Скопійовано!", "Можна вільно використовувати на сайті, у статті чи звіті. Збережіть посилання на джерело.", "Джерело", "Budapest Adventures, за даними KSH", "Графік: Budapest Adventures"),
    "he": ("הטמעת התרשים", "העתקת הקוד", "הועתק!", "מותר לשימוש חופשי באתר, בכתבה או בדוח. נא לשמור על הקישור למקור.", "מקור", "מאת Budapest Adventures, על בסיס נתוני KSH", "תרשים: Budapest Adventures"),
    "ja": ("グラフを埋め込む", "コードをコピー", "コピーしました", "サイト、記事、レポートで自由に使えます。出典リンクは残してください。", "出典", "Budapest Adventures（KSHデータに基づく）", "グラフ：Budapest Adventures"),
    "ko": ("차트 삽입", "코드 복사", "복사됨!", "웹사이트, 기사, 보고서에서 자유롭게 사용할 수 있습니다. 출처 링크는 유지해 주세요.", "출처", "Budapest Adventures, KSH 데이터 기반", "차트: Budapest Adventures"),
}


def _generated_pages():
    import json as _json
    import sys as _sys
    _sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import build_stats_i18n as b
    alt = b.page_alternates()["/budapest-tourism-statistics"]
    out = []
    for lg, (btn, copy, copied, note, src, by, credit) in EMBED_I18N.items():
        with open(os.path.join(ROOT, "data", "i18n", "stats", lg + ".json"), encoding="utf-8") as fh:
            name = _json.load(fh)["s042"]
        out.append({"file": b.stats_file(alt[lg]), "path": alt[lg], "lang": lg, "page_name": name,
                    "source_tpl": src + ': <a href="{url}">{name}</a>, ' + by, "credit": credit,
                    "btn": btn, "copy": copy, "copied": copied, "note": note})
    return out


PAGES += _generated_pages()

MARK_START = "<!--bpa-embed-->"
MARK_END = "<!--/bpa-embed-->"

EMBED_CSS = """<style id="bpa-embed-css">
.bpa-embed{margin:-8px 0 20px}
.bpa-embed-btn{display:inline-flex;align-items:center;gap:6px;background:#fff;border:1px solid #cbd5e1;border-radius:9999px;padding:6px 14px;font:700 12.5px/1.2 inherit;color:#1e3a5f;cursor:pointer}
.bpa-embed-btn:hover{background:#f1f5f9}
.bpa-embed-panel{margin-top:10px;padding:14px;border:1px solid #e2e8f0;border-radius:12px;background:#f8fafc}
.bpa-embed-panel[hidden]{display:none}
.bpa-embed-code{width:100%;box-sizing:border-box;min-height:118px;font:12px/1.45 ui-monospace,SFMono-Regular,Menlo,monospace;color:#0f172a;border:1px solid #cbd5e1;border-radius:8px;padding:10px;background:#fff;resize:vertical}
.bpa-embed-row{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin-top:8px}
.bpa-embed-copy{background:#1e3a5f;color:#fff;border:0;border-radius:8px;padding:8px 14px;font:700 13px/1 inherit;cursor:pointer}
.bpa-embed-note{font-size:12.5px;color:#475569;line-height:1.4;flex:1;min-width:200px}
</style>"""

EMBED_JS = """<script id="bpa-embed-js">(function(){
document.addEventListener('click',function(e){
  var b=e.target.closest('.bpa-embed-btn');
  if(b){var p=document.getElementById(b.getAttribute('aria-controls'));if(!p)return;var open=p.hasAttribute('hidden');
    if(open){p.removeAttribute('hidden');}else{p.setAttribute('hidden','');}
    b.setAttribute('aria-expanded',open?'true':'false');
    if(open&&window.gtag){gtag('event','embed_open',{chart_id:b.getAttribute('data-chart')});}
    return;}
  var c=e.target.closest('.bpa-embed-copy');
  if(c){var t=c.closest('.bpa-embed-panel').querySelector('textarea');t.select();
    var done=function(){var l=c.textContent;c.textContent=c.getAttribute('data-done');setTimeout(function(){c.textContent=l;},1800);};
    if(navigator.clipboard){navigator.clipboard.writeText(t.value).then(done,function(){document.execCommand('copy');done();});}
    else{document.execCommand('copy');done();}
    if(window.gtag){gtag('event','embed_copy',{chart_id:c.getAttribute('data-chart')});}}
});})();</script>"""

EMBED_PAGE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{title} | Budapest Adventures</title>
<meta name="robots" content="noindex, follow"/>
<link rel="canonical" href="{page_url}"/>
<style>
html,body{{margin:0;padding:0;background:#fff}}
body{{font-family:'Plus Jakarta Sans',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:#0f172a}}
.bpa-chart{{margin:0 !important}}
.bpa-credit{{font-size:12px;color:#64748b;margin:8px 4px 0;text-align:right}}
.bpa-credit a{{color:#1e3a5f;font-weight:700;text-decoration:none}}
{chart_css}
</style>
</head>
<body>
{chart}
<div class="bpa-credit"><a href="{page_url}?utm_source=embed&amp;utm_medium=chart&amp;utm_campaign={chart_id}" target="_blank" rel="noopener">{credit}</a></div>
</body>
</html>
"""


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def write(rel, text):
    full = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(text)


def div_end(s, start):
    """Index just past the </div> that closes the <div> opening at `start`."""
    depth, pos = 0, start
    for m in re.compile(r"<div\b|</div>").finditer(s, start):
        depth += 1 if m.group(0) == "<div" else -1
        if depth == 0:
            return m.end()
    raise ValueError("unbalanced div at %d" % start)


# iframe heights measured in Chrome (tallest of 360px and 760px widths, EN/HU) + slack
HEIGHTS = {"chart-arrivals": 345, "chart-nights": 330, "chart-stay": 375,
           "chart-months": 460, "chart-countries": 425, "chart-spending": 420}


def estimate_height(chart_html, chart_id=None):
    if chart_id in HEIGHTS:
        return HEIGHTS[chart_id]
    rows = chart_html.count('class="bpa-row"')
    pair = 'class="bpa-pair"' in chart_html
    legend = 'class="bpa-legend"' in chart_html
    return 170 + (40 if legend else 0) + rows * (36 if pair else 32)


def main():
    for cfg in PAGES:
        s = read(cfg["file"])
        # drop anything a previous run added
        s = re.sub(re.escape(MARK_START) + r".*?" + re.escape(MARK_END), "", s, flags=re.S)
        s = re.sub(r'<style id="bpa-embed-css">.*?</style>', "", s, flags=re.S)
        s = re.sub(r'<script id="bpa-embed-js">.*?</script>', "", s, flags=re.S)

        chart_css = re.search(r'<style id="bpa-stats-charts">(.*?)</style>', s, re.S).group(1)
        page_url = SITE + cfg["path"]
        source_html = cfg["source_tpl"].format(url=page_url, name=cfg["page_name"])

        out, last = [], 0
        for m in re.finditer(r'<div class="bpa-chart" id="([^"]+)"', s):
            chart_id = m.group(1)
            end = div_end(s, m.start())
            chart = s[m.start():end]
            title = html.unescape(re.search(r'class="bpa-chart-title"[^>]*>([^<]*)<', chart).group(1))
            embed_path = "/embed" + cfg["path"] + "/" + chart_id

            write("embed" + cfg["path"] + "/" + chart_id + ".html", EMBED_PAGE.format(
                lang=cfg["lang"], title=html.escape(title), page_url=page_url, chart_css=chart_css,
                chart=chart, chart_id=chart_id, credit=cfg["credit"]))

            snippet = (
                f'<iframe src="{SITE}{embed_path}" title="{html.escape(title)}" width="100%" '
                f'height="{estimate_height(chart, chart_id)}" style="border:0;max-width:760px" loading="lazy"></iframe>\n'
                f'<p style="font-size:13px">{source_html}</p>'
            )
            panel_id = "bpa-embed-" + chart_id
            ui = (
                f'{MARK_START}<div class="bpa-embed">'
                f'<button type="button" class="bpa-embed-btn" aria-expanded="false" aria-controls="{panel_id}" data-chart="{chart_id}">'
                f'<span aria-hidden="true">&lt;/&gt;</span> {cfg["btn"]}</button>'
                f'<div class="bpa-embed-panel" id="{panel_id}" hidden>'
                f'<textarea class="bpa-embed-code" readonly aria-label="{cfg["btn"]}">{html.escape(snippet)}</textarea>'
                f'<div class="bpa-embed-row"><button type="button" class="bpa-embed-copy" data-chart="{chart_id}" data-done="{cfg["copied"]}">{cfg["copy"]}</button>'
                f'<span class="bpa-embed-note">{cfg["note"]}</span></div></div></div>{MARK_END}'
            )
            out.append(s[last:end] + ui)
            last = end
        out.append(s[last:])
        s = "".join(out)
        s = s.replace("</head>", EMBED_CSS + "</head>", 1).replace("</body>", EMBED_JS + "</body>", 1)
        write(cfg["file"], s)
        print("updated", cfg["file"], "with", len(out) - 1, "embeddable charts")


if __name__ == "__main__":
    main()
