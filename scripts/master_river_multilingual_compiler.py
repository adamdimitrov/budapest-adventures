#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MASTER RIVER MULTILINGUAL COMPILER — BUDAPEST ADVENTURES
Compiles 100% authentic, fully translated river cruise pages across all 20 foreign languages:
DE, FR, ES, IT, NL, PL, RO, CS, SK, HR, SR, BG, RU, UK, EL, TR, PT, HE, JA, KO.
Also updates canonical English and Hungarian pages with the Dutch hreflang tag.
"""

import os
import sys
import re
import json
from bs4 import BeautifulSoup

BASE_DIR = '/Users/adamdimitrov/Development/budapest-adventures'
sys.path.insert(0, os.path.join(BASE_DIR, 'scripts'))

from river_i18n_master_data import (
    PAGE_META,
    AUTHOR_DATA,
    INTRO_DATA,
    FILTER_TABS_DATA,
    UI_COMMON,
    BEST_FOR_DATA,
    BREAKDOWN_HEADERS,
    RANK_BADGES
)
from subpoint_headings_i18n import SUBPOINT_HEADINGS
from i18n_translation_data import BUY_CARD_I18N
from compile_all_languages_luxury import extract_tour_content, SLUG_MAP


from spec_chips_i18n import SPEC_CHIPS_I18N

MASTER_DICT_PATH = os.path.join(BASE_DIR, 'data', 'i18n_master_dictionary.json')
MASTER_DICT = json.load(open(MASTER_DICT_PATH, encoding='utf-8')) if os.path.exists(MASTER_DICT_PATH) else {}

TIPS_TRANSLATIONS = {
    'de': {
        'cancellation': "Alle Schifffahrten bieten eine kulante Stornierungsregelung mit voller Rückerstattung bis zu 24 Stunden vor Abfahrt.",
        'deck_view': "Für beste Sicht und Fotomotive begeben Sie sich direkt nach dem Einsteigen auf das offene Oberdeck.",
        'headphones': "Kopfhörer für den Audioguide werden an Bord ausgegeben; Sie können auch eigene 3,5-mm-Klinkenkopfhörer verwenden.",
        'arrival': "Kommen Sie 15–20 Minuten vor Abfahrt am Steg an, um sich die besten Plätze am Fenster oder auf dem Oberdeck zu sichern."
    },
    'fr': {
        'cancellation': "Toutes les croisières bénéficient d'une annulation gratuite avec remboursement intégral jusqu'à 24 heures avant le départ.",
        'deck_view': "Pour profiter des meilleures vues et photos, montez directement sur le pont supérieur découvert dès l'embarquement.",
        'headphones': "Des écouteurs pour l'audioguide sont fournis à bord, mais vous pouvez également brancher vos propres écouteurs filaires jack 3,5 mm.",
        'arrival': "Présentez-vous à l'embarcadère 15 à 20 minutes avant le départ pour choisir les meilleures places près des fenêtres ou sur le pont."
    },
    'es': {
        'cancellation': "Todos los paseos cuentan con política de cancelación flexible con reembolso íntegro hasta 24 horas antes de la salida.",
        'deck_view': "Para obtener las mejores fotos y vistas panorámicas, suba directamente a la cubierta superior abierta al embarcar.",
        'headphones': "A bordo se proporcionan auriculares para el audioguía, aunque también puede usar sus propios auriculares con cable jack de 3,5 mm.",
        'arrival': "Llegue al muelle 15 o 20 minutos antes de la salida para asegurarse los mejores asientos junto a las ventanas o en cubierta."
    },
    'it': {
        'cancellation': "Tutte le crociere prevedono la cancellazione gratuita con rimborso completo fino a 24 ore prima della partenza.",
        'deck_view': "Per le migliori viste e opportunità fotografiche, sali direttamente sul ponte superiore all'aperto al momento dell'imbarco.",
        'headphones': "Le cuffie per l'audioguida sono fornite a bordo, ma puoi utilizzare anche i tuoi auricolari con jack da 3,5 mm.",
        'arrival': "Arriva al molo 15-20 minuti prima della partenza per assicurarti i posti migliori vicino ai finestrini o sul ponte."
    },
    'nl': {
        'cancellation': "Alle afvaarten hebben een soepel annuleringsbeleid met volledige terugbetaling tot 24 uur voor vertrek.",
        'deck_view': "Ga direct na het instappen naar het open bovendek voor het beste uitzicht en de mooiste fotomomenten.",
        'headphones': "Koptelefoons voor de audiogids worden aan boord verstrekt, maar u kunt ook uw eigen 3,5 mm oordopjes aansluiten.",
        'arrival': "Zorg dat u 15 tot 20 minuten voor vertrek op de steiger bent om de beste stoelen aan het raam of op het dek te kiezen."
    },
    'pl': {
        'cancellation': "Wszystkie rejsy oferują bezpłatne anulowanie z pełnym zwrotem kosztów do 24 godzin przed wypłynięciem.",
        'deck_view': "Najlepsze widoki i kadry do zdjęć uzyskasz, wchodząc zaraz po wejściu na pokład na otwarty górny pokład.",
        'headphones': "Słuchawki do audioprzewodnika są rozdawane na pokładzie, ale możesz też podłączyć własne słuchawki z wtykiem minijack 3,5 mm.",
        'arrival': "Przybądź na przystań 15–20 minut przed rejsem, aby zająć najlepsze miejsca przy oknie lub na górnym pokładzie."
    },
    'ro': {
        'cancellation': "Toate croazierele oferă anulare gratuită cu rambursare integrală cu până la 24 de ore înainte de plecare.",
        'deck_view': "Pentru cele mai spectaculoase fotografii, urcați direct pe puntea superioară deschisă imediat după îmbarcare.",
        'headphones': "Căștile pentru ghidul audio sunt puse la dispoziție la bord, dar puteți folosi și căștile personale cu mufă jack de 3,5 mm.",
        'arrival': "Sosiți la ponton cu 15-20 de minute înainte de plecare pentru a prinde cele mai bune locuri la geam sau pe punte."
    },
    'cs': {
        'cancellation': "Všechny plavby nabízejí bezplatné zrušení s plnou refundací až 24 hodin před vyplutím.",
        'deck_view': "Pro nejlepší výhledy a fotografie zamiřte ihned po nalodění na otevřenou horní palubu.",
        'headphones': "Sluchátka k audiosprůvodci obdržíte na palubě, můžete však použít i vlastní drátová sluchátka s 3,5mm jackem.",
        'arrival': "Doražte k molu 15–20 minut předem, abyste si zajistili nejlepší místa u oken nebo na palubě."
    },
    'sk': {
        'cancellation': "Všetky plavby ponúkajú bezplatné storno s plným vrátením peňazí až 24 hodín pred odchodom.",
        'deck_view': "Pre najkrajšie výhľady a fotografie choďte hneď po nastúpení na otvorenú hornú palubu.",
        'headphones': "Slúchadlá k audiosprievodcovi dostanete na palube, môžete však použiť aj vlastné s 3,5 mm jackom.",
        'arrival': "Príďte k mólu 15 až 20 minút pred odchodom, aby ste si obsadili najlepšie miesta pri okne alebo na palube."
    },
    'hr': {
        'cancellation': "Sva krstarenja nude besplatno otkazivanje uz puni povrat novca do 24 sata prije polaska.",
        'deck_view': "Za najbolje vidike i fotografiranje uputite se odmah po ukrcaju na otvorenu gornju palubu.",
        'headphones': "Slušalice za audio vodič dobivate na brodu, a možete koristiti i vlastite slušalice s priključkom od 3,5 mm.",
        'arrival': "Dođite na dok 15-20 minuta prije polaska kako biste osigurali najbolja mjesta uz prozore ili na palubi."
    },
    'sr': {
        'cancellation': "Сва крстарења нуде бесплатно отказивање уз пун повраћај новца до 24 сата пре поласка.",
        'deck_view': "За најбоље погледе и фотографисање попните се одмах након укрцавања на отворену горњу палубу.",
        'headphones': "Слушалице за аудио водич добијате на броду, а можете користити и сопствене слушалице од 3,5 мм.",
        'arrival': "Дођите на док 15–20 минута раније како бисте заузели најбоља места поред прозора или на палуби."
    },
    'bg': {
        'cancellation': "Всички круизи предлагат безплатно анулиране с пълно възстановяване на сумата до 24 часа преди часа на отплаване.",
        'deck_view': "За най-красиви панорами и снимки се качете на откритата горна палуба веднага след качването на борда.",
        'headphones': "Слушалките за аудиогида се предоставят на борда, но можете да използвате и свои собствени с 3,5 мм жак.",
        'arrival': "Елате на кея 15–20 минути преди тръгване, за да заемете най-хубавите места до прозорците или на палубата."
    },
    'ru': {
        'cancellation': "На всех круизах действует бесплатная отмена с полным возвратом стоимости за 24 часа до отправления.",
        'deck_view': "Для лучших видов и фотографий сразу после посадки поднимайтесь на открытую верхнюю палубу.",
        'headphones': "Наушники для аудиогида выдаются на борту, но вы также можете подключить свои наушники со стандартным разъемом 3,5 мм.",
        'arrival': "Приходите на причал за 15–20 минут до отправления, чтобы занять лучшие места у окон или на палубе."
    },
    'uk': {
        'cancellation': "Усі круїзи пропонують безкоштовне скасування з повним поверненням коштів за 24 години до відправлення.",
        'deck_view': "Для найкращого огляду та фотозйомки піднімайтеся на відкриту верхню палубу одразу після посадки.",
        'headphones': "Навушники для аудіогіда видаються на борту, але ви також можете підключити власні навушники з роз'ємом 3,5 мм.",
        'arrival': "Приходьте на причал за 15–20 хвилин до відправлення, щоб зайняти найкращі місця біля вікон або на палубі."
    },
    'el': {
        'cancellation': "Όλες οι κρουαζιέρες προσφέρουν δωρεάν ακύρωση με πλήρη επιστροφή χρημάτων έως και 24 ώρες πριν την αναχώρηση.",
        'deck_view': "Για την καλύτερη θέα και φωτογράφιση, ανεβείτε απευθείας στο ανοιχτό επάνω κατάστρωμα κατά την επιβίβαση.",
        'headphones': "Ακουστικά για τον ηχητικό οδηγό παρέχονται στο σκάφος, αλλά μπορείτε να χρησιμοποιήσετε και τα δικά σας με βύσμα 3,5 mm.",
        'arrival': "Φτάστε στην αποβάθρα 15-20 λεπτά πριν από την αναχώρηση για να εξασφαλίσετε τις καλύτερες θέσεις."
    },
    'tr': {
        'cancellation': "Tüm tekne turlarında kalkış saatinden 24 saat öncesine kadar ücretsiz iptal ve tam ücret iadesi geçerlidir.",
        'deck_view': "En güzel manzara ve fotoğraf açıları için biner binmez doğrudan üst açık güverteye çıkın.",
        'headphones': "Sesli rehber kulaklıkları teknede dağıtılır; dilerseniz kendi 3,5 mm kablolu kulaklığınızı da kullanabilirsiniz.",
        'arrival': "Pencere kenarı veya açık güvertedeki en güzel koltukları kapmak için kalkıştan 15-20 dakika önce iskelede olun."
    },
    'pt': {
        'cancellation': "Todos os passeios oferecem cancelamento gratuito com reembolso total até 24 horas antes do embarque.",
        'deck_view': "Para as melhores fotos e vistas panorâmicas, dirija-se logo ao convés superior aberto assim que embarcar.",
        'headphones': "São fornecidos auriculares a bordo para o audioguia, mas também pode utilizar os seus próprios auscultadores de 3,5 mm.",
        'arrival': "Chegue ao cais 15 a 20 minutos antes da partida para garantir os melhores lugares junto às janelas ou no convés."
    },
    'he': {
        'cancellation': "כל השייט כולל מדיניות ביטול גמישה עם החזר כספי מלא עד 24 שעות לפני מועד היציאה.",
        'deck_view': "לתצפית ולצילומים הטובים ביותר, עלו ישירות לסיפון העליון הפתוח מיד עם העלייה לספינה.",
        'headphones': "אוזניות למדריך הקולי מסופקות על הסיפון, אך ניתן להשתמש גם באוזניות חוטיות אישיות עם חיבור 3.5 מ\"מ.",
        'arrival': "הגיעו לרציף 15-20 דקות לפני שעת היציאה כדי לתפוס את המקומות הטובים ביותר ליד החלונות או בסיפון."
    },
    'ja': {
        'cancellation': "すべてのクルーズで出発24時間前までキャンセル料無料・全額返金に対応しています。",
        'deck_view': "最高の景色と写真撮影を楽しむには、乗船後すぐに最上階のオープンデッキへお進みください。",
        'headphones': "音声ガイド用のイヤホンは船内で配布されますが、ご自身の3.5mm有線イヤホンもご利用いただけます。",
        'arrival': "窓際やデッキの見晴らしの良い席を確保するため、出航の15〜20分前には乗り場に到着することをおすすめします。"
    },
    'ko': {
        'cancellation': "모든 크루즈는 출발 24시간 전까지 무료 취소 및 전액 환불이 보장됩니다.",
        'deck_view': "가장 멋진 전망과 인생 사진을 남기시려면 탑승 직후 상층 오픈 덱으로 먼저 이동하세요.",
        'headphones': "오디오 가이드 이어폰이 선내에서 제공되지만, 개인 3.5mm 유선 이어폰을 사용하셔도 됩니다.",
        'arrival': "창가나 오픈 덱 명당자리를 선점하시려면 출발 15~20분 전까지 선착장에 여유 있게 도착하세요."
    }
}

NL_HREFLANG_TAG = '<link href="https://www.budapestadventures.com/nl/beste-boedapest-riviercruises" hreflang="nl" rel="alternate"/>'

def ensure_nl_hreflang(soup):
    """Ensures hreflang='nl' is present in head alternate links."""
    existing_nl = soup.find('link', rel='alternate', hreflang='nl')
    if not existing_nl:
        nl_link = soup.new_tag('link', rel='alternate', hreflang='nl', href='https://www.budapestadventures.com/nl/beste-boedapest-riviercruises')
        # Insert before hu or at end of alternates
        hu_alt = soup.find('link', rel='alternate', hreflang='hu')
        if hu_alt:
            hu_alt.insert_before(nl_link)
        else:
            first_alt = soup.find('link', rel='alternate')
            if first_alt:
                first_alt.insert_before(nl_link)
            elif soup.head:
                soup.head.append(nl_link)

def parse_harvested_subpoints(lang):
    """Extracts subpoint texts between h4/h5 tags from harvested HTML."""
    h_path = os.path.join(BASE_DIR, 'data', 'harvested_html', lang, 'river.html')
    if not os.path.exists(h_path):
        return []
    soup = BeautifulSoup(open(h_path, encoding='utf-8'), 'html.parser')
    h4_list = soup.find_all(['h4', 'h5'])
    subpoints_extracted = []
    
    for i in range(len(h4_list)):
        curr = h4_list[i]
        nxt = h4_list[i+1] if i + 1 < len(h4_list) else None
        
        lis = []
        node = curr.next_element
        while node and node != nxt:
            if hasattr(node, 'name') and node.name == 'li' and len(node.get_text(strip=True)) > 15:
                t = node.get_text(' ', strip=True)
                if t not in lis:
                    lis.append(t)
            node = node.next_element
            
        subpoints_extracted.append({
            'raw_h4': curr.get_text(strip=True),
            'lis': lis
        })
    return subpoints_extracted


def cleanse_json_ld(soup, lang, pm, intro, canonical_url):
    """Cleanse all English leftovers from JSON-LD Schema objects."""
    for s in soup.find_all('script', type='application/ld+json'):
        if s.string:
            try:
                data = json.loads(s.string)
                graphs = data.get('@graph', [data])
                for item in graphs:
                    item['inLanguage'] = lang
                    if '@id' in item:
                        item['@id'] = item['@id'].replace('https://www.budapestadventures.com/best-budapest-river-cruises', canonical_url)
                    if 'mainEntityOfPage' in item:
                        if isinstance(item['mainEntityOfPage'], dict):
                            item['mainEntityOfPage']['@id'] = canonical_url
                        else:
                            item['mainEntityOfPage'] = canonical_url
                    if 'headline' in item and pm.get('title'):
                        item['headline'] = pm['title']
                    if 'name' in item and pm.get('title'):
                        item['name'] = pm['title']
                    if 'description' in item and pm.get('desc'):
                        item['description'] = pm['desc']
                    if 'articleBody' in item and intro.get('p1'):
                        item['articleBody'] = f"{intro['p1']} {intro['p2']} {intro['p3']}"
                    if 'mainEntity' in item and isinstance(item['mainEntity'], dict):
                        if pm.get('title'): item['mainEntity']['name'] = pm['title']
                        if pm.get('desc'): item['mainEntity']['description'] = pm['desc']
                        
                s_out = json.dumps(data, ensure_ascii=False)
                # Double safety replace on residual string
                s_out = re.sub(r'Are you feeling overwhelmed[^"]+', pm.get('desc', ''), s_out)
                s.string = s_out
            except Exception:
                stxt = s.string
                stxt = stxt.replace('"inLanguage": "en"', f'"inLanguage": "{lang}"')
                stxt = stxt.replace('https://www.budapestadventures.com/best-budapest-river-cruises', canonical_url)
                if pm.get('title'):
                    stxt = stxt.replace("10 Best River Cruises in Budapest in 2026 (Personally Tested)", pm['title'])
                s.string.replace_with(stxt)

def localize_sticky_bar(soup, lang, tours, buy_card_data, ui, rank_badges):
    """Localizes the mobile bottom sticky navigation bar."""
    sticky_btn = soup.find(id='sticky-cta-btn')
    if sticky_btn and ui.get('btn_check'):
        sticky_btn.string = ui['btn_check']
        
    toc_btn = soup.find(id='hybridTocBtn')
    if toc_btn:
        sp = toc_btn.find('span')
        if sp:
            sp.string = f"{ui.get('overview', '10 Cruises')}"
            
    top_btn = soup.find(class_='hybrid-top-btn')
    if top_btn:
        sp = top_btn.find('span')
        if sp:
            sp.string = ui.get('top_label', 'Top')
            
    rank_el = soup.find(id='sticky-rank')
    if rank_el and len(rank_badges) > 0:
        rank_el.string = rank_badges[0]
        
    name_el = soup.find(id='sticky-name')
    if name_el and len(tours) > 0:
        name_el.string = tours[0]['clean_title']
        
    trust_el = soup.find(class_='hybrid-active-trust')
    if trust_el and buy_card_data.get('refund'):
        trust_el.string = buy_card_data['refund']

def localize_specs_row(soup, lang, ui):
    """Localizes spec pills in bpa-specs-row across all cards."""
    chips_dict = SPEC_CHIPS_I18N.get(lang, {})
    for row in soup.find_all(class_='bpa-specs-row'):
        for sp in row.find_all('span'):
            txt = sp.get_text(strip=True)
            if txt in chips_dict:
                sp.string = chips_dict[txt]
            elif 'Tested' in txt and ui.get('tested'):
                sp.string = ui['tested']

def localize_navbar_and_menu(soup, lang, river_slug, dinner_slug):
    """Localizes header navigation, mega-menu, direct links, and mobile drawer."""
    nav_data = MASTER_DICT.get(lang, {}).get('nav', {})
    if not nav_data:
        return
        
    # 1. Dropdown main button
    dropdown_btn = soup.find('button', class_='ltt-dropdown-btn')
    if dropdown_btn and nav_data.get('danube_cruises'):
        span = dropdown_btn.find('span')
        if span:
            span.string = nav_data['danube_cruises']
            
    # 2. Mega menu headers
    mega_heads = soup.find_all(class_='ltt-mega-head')
    if len(mega_heads) >= 1 and nav_data.get('head_cruises'):
        mega_heads[0].string = nav_data['head_cruises']
    if len(mega_heads) >= 2 and nav_data.get('head_spas'):
        mega_heads[1].string = nav_data['head_spas']
        
    # 3. Direct links in navbar
    for a in soup.find_all('a', class_='ltt-nav-link'):
        txt = a.get_text(strip=True)
        if 'River' in txt and nav_data.get('river'):
            a.string = nav_data['river']
            a['href'] = f"/{lang}/{river_slug}"
        elif 'Dinner' in txt and nav_data.get('dinner'):
            a.string = nav_data['dinner']
            a['href'] = f"/{lang}/{dinner_slug}"
        elif 'Card' in txt and nav_data.get('card_calc'):
            a.string = nav_data['card_calc']
        elif 'About' in txt and nav_data.get('about'):
            a.string = nav_data['about']
        elif 'Contact' in txt and nav_data.get('contact'):
            a.string = nav_data['contact']

def localize_footer_section(soup, lang, river_slug, dinner_slug):
    """Localizes footer brand description, column titles, and links."""
    f_data = MASTER_DICT.get(lang, {}).get('footer', {})
    if not f_data:
        return
    footer = soup.find('footer') or soup.find(class_='footer-dark')
    if not footer:
        return
        
    brand_desc = footer.find(class_='footer-paragraph') or footer.find(class_='footer-brand-desc')
    if brand_desc and f_data.get('p'):
        brand_desc.string = f_data['p']
        
    col_titles = footer.find_all(class_=lambda c: c and ('footer-col-title' in c or 'footer-link-title' in c or 'heading-36' in c))
    if len(col_titles) >= 1 and f_data.get('popular'):
        col_titles[0].string = f_data['popular']
    if len(col_titles) >= 2 and f_data.get('company'):
        col_titles[1].string = f_data['company']
        
    for a in footer.find_all('a', class_=lambda c: c and ('footer-link' in c or 'footer-link-3' in c)):
        href = a.get('href', '')
        if 'best-budapest-river-cruises' in href or 'setahajozas-a-dunan-budapest' in href or river_slug in href:
            a['href'] = f"/{lang}/{river_slug}"
        elif 'best-dinner-cruises-budapest' in href or 'setahajozas-a-dunan-vacsoraval' in href or dinner_slug in href:
            a['href'] = f"/{lang}/{dinner_slug}"
        elif 'about' in href and f_data.get('about'):
            a.string = f_data['about']
        elif 'ethics' in href and f_data.get('ethics'):
            a.string = f_data['ethics']
        elif 'contact' in href and f_data.get('contact'):
            a.string = f_data['contact']
            
    disclaimer = footer.find(class_='footer-disclaimer') or footer.find(class_='footer-trust-micro')
    if disclaimer and f_data.get('disclaimer'):
        disclaimer.string = f_data['disclaimer']

def compile_language_river(lang, en_html):
    """Compiles a 100% localized river cruise page for a given language."""
    print(f"Compiling [{lang.upper()}] River Cruise Guide...")
    soup = BeautifulSoup(en_html, 'html.parser')
    
    river_slug = SLUG_MAP[lang]['river']
    canonical_url = f"https://www.budapestadventures.com/{lang}/{river_slug}"
    
    # Brand logo link
    brand = soup.find('a', class_='ltt-brand')
    if brand:
        brand['href'] = f'/{lang}'

    # 1. HTML tag
    html_tag = soup.find('html')
    if html_tag:
        html_tag['lang'] = lang
        if lang == 'he':
            html_tag['dir'] = 'rtl'
            
    # 2. Canonical & Hreflang
    can = soup.find('link', rel='canonical')
    if can:
        can['href'] = canonical_url
    ensure_nl_hreflang(soup)
    
    # 3. Meta Tags
    pm = PAGE_META.get(lang, {})
    if soup.title and pm.get('title'):
        soup.title.string = pm['title']
    m_desc = soup.find('meta', {'name': 'description'})
    if m_desc and pm.get('desc'):
        m_desc['content'] = pm['desc']
    for tag_name, prop_name in [('meta', 'property'), ('meta', 'name')]:
        og_t = soup.find(tag_name, {prop_name: 'og:title'})
        if og_t and pm.get('title'): og_t['content'] = pm['title']
        tw_t = soup.find(tag_name, {prop_name: 'twitter:title'})
        if tw_t and pm.get('title'): tw_t['content'] = pm['title']
        og_d = soup.find(tag_name, {prop_name: 'og:description'})
        if og_d and pm.get('desc'): og_d['content'] = pm['desc']
        tw_d = soup.find(tag_name, {prop_name: 'twitter:description'})
        if tw_d and pm.get('desc'): tw_d['content'] = pm['desc']

    # 4. JSON-LD Localization
    intro = INTRO_DATA.get(lang, {})
    cleanse_json_ld(soup, lang, pm, intro, canonical_url)

    # 5. Breadcrumbs
    for bc in soup.find_all(class_='ltt-breadcrumbs'):
        bc.clear()
        home_a = soup.new_tag('a', href=f'/{lang}')
        home_a.string = pm.get('bc_home', 'Home')
        sep = soup.new_tag('span', **{'class': 'ltt-bc-sep'})
        sep.string = '›'
        curr = soup.new_tag('span', **{'class': 'ltt-bc-current'})
        curr.string = pm.get('bc_curr', 'River Cruises')
        bc.append(home_a)
        bc.append(' ')
        bc.append(sep)
        bc.append(' ')
        bc.append(curr)

    # 6. Hero Kicker & H1
    badge = soup.find(class_='ltt-hero-kicker-badge')
    if badge and pm.get('kicker'):
        badge.string = pm['kicker']
    h1 = soup.find(class_='ltt-editorial-h1') or soup.find('h1')
    if h1 and pm.get('h1'):
        h1.string = pm['h1']

    # 7. Author Byline & Metadata
    auth = AUTHOR_DATA.get(lang, {})
    auth_line = soup.find(class_='ltt-author-line')
    if auth_line and auth.get('prefix'):
        auth_line.clear()
        auth_line.append(auth['prefix'])
        a_tag = soup.new_tag('a', href="/about")
        a_tag.string = "Adam Dimitrov"
        auth_line.append(a_tag)
        auth_line.append(f" — {auth.get('role', 'Budapest River Cruise Specialist')}")
        
    auth_role = soup.find(class_='ltt-author-role')
    if auth_role and auth.get('badge'):
        auth_role.string = auth['badge']
        
    tp = soup.find(class_='ltt-trust-pill')
    if tp and auth.get('updated'):
        tp.string = auth['updated']
    upd = soup.find(class_='ltt-updated-date')
    if upd and auth.get('updated'):
        upd.string = auth['updated']

    # 8. Lead Copy (3 Editorial Intro Paragraphs)
    lead = soup.find(class_='ltt-lead-copy')
    if lead and intro.get('p1'):
        # Preserve figure (dinner callout) if present
        fig = lead.find('figure')
        lead.clear()
        for pkey in ['p1', 'p2', 'p3']:
            if intro.get(pkey):
                p = soup.new_tag('p')
                p.string = intro[pkey]
                lead.append(p)
        if fig:
            lead.append(fig)

    # 9. Dinner Guide Callout Box
    dinner_callout = soup.find(class_='ltt-dinner-callout') or soup.find(class_='ltt-dinner-crosslink') or soup.find(class_='ltt-dinner-banner')
    if dinner_callout and intro.get('dinner_title'):
        title_el = dinner_callout.find(class_='ltt-dinner-title') or dinner_callout.find('h3') or dinner_callout.find('strong')
        if title_el:
            title_el.string = intro['dinner_title']
        sub_el = dinner_callout.find(class_='ltt-dinner-sub') or dinner_callout.find('p')
        if sub_el and intro.get('dinner_desc'):
            sub_el.string = intro['dinner_desc']

    # 10. Filter Tabs
    ftabs = FILTER_TABS_DATA.get(lang, {})
    flabel = soup.find(class_='ltt-filter-label')
    if flabel and ftabs.get('label'):
        flabel.string = ftabs['label']
    tab_btns = soup.find_all(class_='ltt-tab-btn')
    tab_keys = ['all', 'tested', 'under20', 'drinks', 'dinner', 'historic']
    for idx, btn in enumerate(tab_btns[:6]):
        k = tab_keys[idx]
        if ftabs.get(k):
            btn.string = ftabs[k]

    # 11. Extract Harvested Tours & Subpoints
    harvested_river_path = os.path.join(BASE_DIR, 'data', 'harvested_html', lang, 'river.html')
    tours = extract_tour_content(harvested_river_path, 'river')
    subpoints_extracted = parse_harvested_subpoints(lang)
    
    ui = UI_COMMON.get(lang, {})
    best_fors = BEST_FOR_DATA.get(lang, [])
    rank_badges = RANK_BADGES.get(lang, [])

    # 12. Top Deck Summary Cards (10 Cards: div.bpa-card)
    deck_cards = soup.find_all(class_='bpa-card')
    for idx, dcard in enumerate(deck_cards):
        if idx >= len(tours): break
        tdata = tours[idx]
        
        # Rank badge
        rank_badge = dcard.find(class_='bpa-rank-tag')
        if rank_badge and idx < len(rank_badges):
            rank_badge.string = rank_badges[idx]
            
        # Clean title
        title_el = dcard.find(class_='bpa-title')
        if title_el:
            title_el.string = tdata['clean_title']
            
        # Best For
        bf_el = dcard.find(class_='bpa-best-for')
        if bf_el and idx < len(best_fors):
            bf_el.clear()
            st = soup.new_tag('strong')
            st.string = ui.get('best_for_label', 'Best For: ')
            bf_el.append(st)
            bf_el.append(best_fors[idx])
            
        # Price label
        psub = dcard.find(class_='bpa-card-price-sub')
        if psub and ui.get('per_adult'):
            psub.string = ui['per_adult']
            
        # CTA button
        btn = dcard.find(class_='bpa-btn')
        if btn and ui.get('btn_check'):
            btn.string = ui['btn_check']
            
        # Read review jump link
        jump = dcard.find(class_='bpa-sublink')
        if jump and ui.get('read_review'):
            jump.string = ui['read_review']
            
        # Trust micro
        for micro in dcard.find_all(class_='bpa-trust-micro'):
            spans = micro.find_all('span')
            if len(spans) >= 3:
                if ui.get('instant_qr'): spans[0].string = ui['instant_qr']
                if ui.get('official_pier'): spans[2].string = ui['official_pier']

    # 13. Detailed Breakdown Section Header & Expand/Collapse
    bd_headers = BREAKDOWN_HEADERS.get(lang, {})
    for bd_title in soup.find_all(class_='bpa-breakdown-heading'):
        if bd_headers.get('title'):
            bd_title.string = bd_headers['title']
    for bd_sub in soup.find_all(class_='bpa-breakdown-sub'):
        if bd_headers.get('sub'):
            bd_sub.string = bd_headers['sub']
        
    for ctrl_btn in soup.find_all(class_='bpa-acc-ctrl-btn'):
        btxt = ctrl_btn.get_text()
        if 'Expand All' in btxt and ui.get('expand_all'):
            ctrl_btn.string = ui['expand_all']
        elif 'Collapse All' in btxt and ui.get('collapse_all'):
            ctrl_btn.string = ui['collapse_all']

    # Table of Contents
    toc = soup.find(class_='ltt-toc-card')
    if toc:
        toc_title = toc.find(class_='ltt-toc-title')
        if toc_title: toc_title.string = ui.get('overview', 'Table of Contents')
        for idx, tlink in enumerate(toc.find_all('a')):
            if idx < len(tours):
                tlink.string = f"#{idx+1} {tours[idx]['clean_title']}"

    # 14. 10 Details Cards (Pros, Cons, Bento tabs, Subpoints, Buy box, Tips)
    details_cards = soup.find_all('details', class_='bpa-details-card')
    tips_data = TIPS_TRANSLATIONS.get(lang, {})
    buy_card_data = BUY_CARD_I18N.get(lang, {})
    
    sub_counter = 0

    for idx, dcard in enumerate(details_cards):
        if idx >= len(tours): break
        tdata = tours[idx]
        
        # Details title
        d_title = dcard.find(class_='bpa-details-title')
        if d_title:
            d_title.string = tdata['clean_title']
            
        # Pros & Cons replacement with native labels and content
        pros = tdata['pros'] if tdata['pros'] else ["Tested and vetted experience."]
        cons = tdata['cons'] if tdata['cons'] else ["Peak hours may sell out quickly."]
        
        pro_con_box = dcard.find(class_='pro-con-box-wrapper')
        if pro_con_box:
            new_box = soup.new_tag('div', **{'class': 'pro-con-box-wrapper'})
            grid = soup.new_tag('div', **{'class': 'w-layout-grid grid-15'})
            new_box.append(grid)
            
            pro_cell = soup.new_tag('div', **{'class': 'pro-con-box-pro-cell', 'data-wf-pbl': 'layout-grid-1x2-vertical'})
            pro_rich = soup.new_tag('div', **{'class': 'pro-con-box-pro-cell-rich-text-block w-richtext'})
            h3_pro = soup.new_tag('h3')
            st_pro = soup.new_tag('strong')
            st_pro.string = ui.get('pros', 'Pros:')
            h3_pro.append(st_pro)
            pro_rich.append(h3_pro)
            ul_pro = soup.new_tag('ul', **{'role': 'list'})
            for p_text in pros:
                li = soup.new_tag('li')
                li.string = p_text
                ul_pro.append(li)
            pro_rich.append(ul_pro)
            pro_cell.append(pro_rich)
            grid.append(pro_cell)
            
            con_cell = soup.new_tag('div', **{'class': 'pro-con-box-con-cell', 'data-wf-pbl': 'layout-grid-1x2-vertical'})
            con_rich = soup.new_tag('div', **{'class': 'pro-con-box-con-cell-rich-text-block w-richtext'})
            h3_con = soup.new_tag('h3')
            st_con = soup.new_tag('strong')
            st_con.string = ui.get('cons', 'Cons:')
            h3_con.append(st_con)
            con_rich.append(h3_con)
            ul_con = soup.new_tag('ul', **{'role': 'list'})
            for c_text in cons:
                li = soup.new_tag('li')
                li.string = c_text
                ul_con.append(li)
            con_rich.append(ul_con)
            con_cell.append(con_rich)
            grid.append(con_cell)
            
            pro_con_box.replace_with(new_box)

        # Bento Tabs Localization
        bento_groups = dcard.find_all('details', class_='ltt-bento-group')
        for bg in bento_groups:
            head = bg.find('summary')
            if not head: continue
            btitle = head.find(class_='ltt-bento-group-title')
            bmeta = head.find(class_='ltt-bento-group-meta')
            if btitle:
                btxt = btitle.text.strip()
                if any(w in btxt for w in ['Summary', 'Zusammenfassung', 'Résumé', 'Resumen', 'Sommario', 'Overzicht', 'Przegląd', 'Prezentare', 'Přehled', 'Prehľad', 'Pregled', 'Преглед', 'Обзор', 'Επισκόπηση', 'Özet', 'סקירה', '概要', '개요']):
                    btitle.string = f"🏆 {ui.get('overview', 'Summary & Review')}"
                    if bmeta and ui.get('overview'): bmeta.string = f"{ui['overview']} ▾"
                elif any(w in btxt for w in ['Pier', 'Boarding', 'Anlegestelle', 'Quai', 'Muelle', 'Molo', 'Steiger', 'Przystań', 'Ponton', 'Mólo', 'Dok', 'Док', 'Кей', 'Причал', 'Αποβάθρα', 'İskele', 'Cais', 'רציף', '乗り場', '선착장']):
                    btitle.string = f"📍 {ui.get('map_label', 'Pier, Boarding & Map')}"
                    if bmeta and ui.get('map_label'): bmeta.string = f"{ui['map_label']} ▾"
                elif any(w in btxt for w in ['Ship', 'Deck', 'Schiff', 'Bateau', 'Barco', 'Nave', 'Schip', 'Statek', 'Nava', 'Loď', 'Brod', 'Брод', 'Кораб', 'Теплоход', 'Πλοίο', 'Gemi', 'Navio', 'ספינה', '船', '선박']):
                    btitle.string = f"🛳️ {ui.get('walkthrough', 'The Ship & Deck')}"
                    if bmeta and ui.get('walkthrough'): bmeta.string = f"{ui['walkthrough']} ▾"
                elif any(w in btxt for w in ['Audio', 'Operator', 'Service', 'Guide', 'Reederei', 'Compagnie', 'Naviera', 'Armator', 'Operat']):
                    btitle.string = f"🎧 {ui.get('audio_op', 'Audio Guide & Services')}"
                    if bmeta and ui.get('audio_op'): bmeta.string = f"{ui['audio_op']} ▾"

        # Bento 0 Summary Body
        if len(bento_groups) >= 1 and tdata['summaries']:
            b0_body = bento_groups[0].find(class_='ltt-bento-group-body')
            if b0_body:
                rich = b0_body.find(class_='w-richtext')
                if not rich:
                    rich = soup.new_tag('div', **{'class': 'w-richtext'})
                    b0_body.clear()
                    b0_body.append(rich)
                else:
                    rich.clear()
                for p_text in tdata['summaries']:
                    p = soup.new_tag('p')
                    p.string = p_text
                    rich.append(p)

        # Subpoints Localization (Bento 1, 2, 3)
        sp_headings_dict = SUBPOINT_HEADINGS.get(lang, {})
        for sp in dcard.find_all(class_='ltt-sp-card'):
            h4 = sp.find('h4')
            if h4:
                en_h4_text = h4.get_text(strip=True)
                if en_h4_text in sp_headings_dict:
                    h4.string = sp_headings_dict[en_h4_text]
                    
            if sub_counter < len(subpoints_extracted):
                extracted = subpoints_extracted[sub_counter]
                if extracted['lis']:
                    sp_lis = sp.find_all('li')
                    for l_idx, li_text in enumerate(extracted['lis']):
                        if l_idx < len(sp_lis):
                            sp_lis[l_idx].string = li_text
            sub_counter += 1

        # Buy Box / Official Ticket Card Localization
        buy_card = dcard.find(class_='ltt-buy-card')
        if buy_card and buy_card_data:
            badge_span = buy_card.find(class_='ltt-buy-card-badge')
            if badge_span:
                text_span = [s for s in badge_span.find_all('span') if 'ltt-live-dot' not in s.get('class', [])]
                if text_span and buy_card_data.get('badge'):
                    text_span[0].string = buy_card_data['badge']
                    
            title_h4 = buy_card.find(class_='ltt-buy-card-title')
            if title_h4:
                title_h4.string = tdata['clean_title']
                
            psub_el = buy_card.find(class_='ltt-buy-price-sub')
            if psub_el and buy_card_data.get('per_adult'):
                psub_el.string = buy_card_data['per_adult']
                
            btn_el = buy_card.find(class_='ltt-buy-cta-btn')
            if btn_el and buy_card_data.get('btn'):
                btn_el.string = buy_card_data['btn']
                
            trust_div = buy_card.find(class_='ltt-buy-card-trust')
            if trust_div:
                sp_trust = trust_div.find('span')
                if sp_trust and buy_card_data.get('trust'):
                    sp_trust.string = buy_card_data['trust']
                    
            for perk in buy_card.find_all(class_='ltt-buy-perk'):
                p_txt = perk.get_text()
                if 'QR' in p_txt and buy_card_data.get('qr'):
                    perk.string = buy_card_data['qr']
                elif 'Refund' in p_txt and buy_card_data.get('refund'):
                    perk.string = buy_card_data['refund']
                elif 'Departure:' in p_txt and buy_card_data.get('departure'):
                    strong = perk.find('strong')
                    strong_txt = strong.get_text() if strong else ''
                    perk.clear()
                    perk.append(f"{buy_card_data['departure']} ")
                    st = soup.new_tag('strong')
                    st.string = strong_txt
                    perk.append(st)
                elif 'Duration:' in p_txt and buy_card_data.get('duration'):
                    strong = perk.find('strong')
                    strong_txt = strong.get_text() if strong else ''
                    perk.clear()
                    perk.append(f"{buy_card_data['duration']} ")
                    st = soup.new_tag('strong')
                    st.string = strong_txt
                    perk.append(st)

        # Tips Localization
        for tip in dcard.find_all(class_='ltt-tip-box'):
            tip_txt = tip.text
            if tips_data.get('cancellation') and 'cancellation' in tip_txt.lower():
                tip.string = f"{ui.get('tip_label', '💡 Tip: ')}{tips_data['cancellation']}"
            elif tips_data.get('deck_view') and any(w in tip_txt.lower() for w in ['sightseeing', 'photo opportunities', 'top deck']):
                tip.string = f"{ui.get('tip_label', '💡 Tip: ')}{tips_data['deck_view']}"
            elif tips_data.get('headphones') and 'headphones' in tip_txt.lower():
                tip.string = f"{ui.get('tip_label', '💡 Tip: ')}{tips_data['headphones']}"
            elif tips_data.get('arrival') and '15–20 minutes' in tip_txt:
                tip.string = f"{ui.get('tip_label', '💡 Tip: ')}{tips_data['arrival']}"


    dinner_slug = SLUG_MAP[lang]['dinner']
    localize_navbar_and_menu(soup, lang, river_slug, dinner_slug)
    localize_specs_row(soup, lang, ui)
    localize_sticky_bar(soup, lang, tours, buy_card_data, ui, rank_badges)
    localize_footer_section(soup, lang, river_slug, dinner_slug)

    # 15. Preserve Affiliate Links
    for a in soup.find_all('a', href=True):
        href = a['href']
        if 'legenda.hu' in href and 'partner=38585' not in href:
            sep = '&' if '?' in href else '?'
            a['href'] = f"{href}{sep}partner=38585"
        if 'budapestxplore.com' in href and 'affi=6876' not in href:
            sep = '&' if '?' in href else '?'
            a['href'] = f"{href}{sep}affi=6876"

    return str(soup)

def update_root_and_hu_hreflang():
    """Adds the Dutch hreflang tag into English master, river.html, and Hungarian river page."""
    paths = [
        os.path.join(BASE_DIR, 'best-budapest-river-cruises', 'index.html'),
        os.path.join(BASE_DIR, 'river.html'),
        os.path.join(BASE_DIR, 'hu', 'setahajozas-a-dunan-budapest', 'index.html')
    ]
    for p in paths:
        if os.path.exists(p):
            soup = BeautifulSoup(open(p, encoding='utf-8'), 'html.parser')
            ensure_nl_hreflang(soup)
            with open(p, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"✓ Added Dutch hreflang tag to: {os.path.relpath(p, BASE_DIR)}")

def compile_all_foreign_languages():
    """Compiles all 20 foreign languages."""
    langs = ['de', 'fr', 'es', 'it', 'nl', 'pl', 'ro', 'cs', 'sk', 'hr', 'sr', 'bg', 'ru', 'uk', 'el', 'tr', 'pt', 'he', 'ja', 'ko']
    
    en_path = os.path.join(BASE_DIR, 'best-budapest-river-cruises', 'index.html')
    en_html = open(en_path, encoding='utf-8').read()
    
    print(f"\n=======================================================")
    print(f"MASTER RIVER MULTILINGUAL COMPILATION: {len(langs)} LANGUAGES")
    print(f"=======================================================\n")
    
    success_count = 0
    for l in langs:
        river_slug = SLUG_MAP[l]['river']
        out_dir = os.path.join(BASE_DIR, l, river_slug)
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, 'index.html')
        
        compiled_html = compile_language_river(l, en_html)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(compiled_html)
        print(f"✓ [{l.upper()}] Written to {l}/{river_slug}/index.html ({len(compiled_html):,} bytes)")
        success_count += 1
        
    print(f"\n✓ Successfully compiled all {success_count} foreign language river cruise pages!")

if __name__ == '__main__':
    update_root_and_hu_hreflang()
    compile_all_foreign_languages()
