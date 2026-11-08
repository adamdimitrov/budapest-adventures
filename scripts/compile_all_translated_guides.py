#!/usr/bin/env python3
"""
MASTER TRANSLATED DESTINATION GUIDE COMPILER — BUDAPEST ADVENTURES
Compiles static multi-language directory architecture across all 21 foreign languages (+ English = 22):
- Homepage: /{lang}/index.html
- River Cruises: /{lang}/{river_slug}/index.html
- Dinner Cruises: /{lang}/{dinner_slug}/index.html

Enforces 100% design parity with English Luxury Editorial System:
- Canonical card architecture without spec pills
- 4-Bento review cards, quick facts, photo sliders, mobile drawer
- 100% affiliate tracking link preservation (partner=38585 / TourCMS / Tiqets)
- Fast, pure static HTML on Vercel (Zero Webflow, Zero Linguana)
- 100% native localization: ltt-buy-card, CSS review pseudo-elements, breakdown headings, proof chips, author box, and footer.
"""

import os
import re
import sys
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import scripts.build_hungarian_pages as bhp
from scripts.i18n_translation_data import (
    BUY_CARD_I18N,
    REVIEW_TOGGLE_I18N,
    BREAKDOWN_I18N,
    AUTHOR_I18N,
    FOOTER_I18N,
    FILTER_TABS_I18N
)
from bs4 import BeautifulSoup

BASE_DIR = '/Users/adamdimitrov/Development/budapest-adventures'
CACHE_DIR = os.path.join(BASE_DIR, 'data', 'harvested_html')

LANGS = ['hu', 'ro', 'ja', 'it', 'fr', 'pl', 'cs', 'hr', 'ru', 'el', 'bg', 'es', 'sr', 'he', 'pt', 'sk', 'tr', 'uk', 'de', 'ko', 'nl']

SLUG_MAP = {
    'hu': {'home': '', 'river': 'setahajozas-a-dunan-budapest', 'dinner': 'setahajozas-a-dunan-vacsoraval'},
    'ro': {'home': '', 'river': 'croaziera-dunare-budapesta', 'dinner': 'croaziera-dunare-cu-cina-budapesta'},
    'ja': {'home': '', 'river': 'budapesuto-ribakuruzu', 'dinner': 'budapesuto-dinakuruzu'},
    'it': {'home': '', 'river': 'crociere-danubio-budapest', 'dinner': 'crociere-cena-danubio-budapest'},
    'fr': {'home': '', 'river': 'croisieres-danube-budapest', 'dinner': 'diner-croisieres-danube-budapest'},
    'pl': {'home': '', 'river': 'rejsy-dunaju-budapeszt', 'dinner': 'rejsy-dunaju-budapeszt-kolacja'},
    'cs': {'home': '', 'river': 'nejlepší-budapest-řeka-plavby', 'dinner': 'nejlepší-večeře-plavby-budapešť'},
    'hr': {'home': '', 'river': 'najbolja-krstarenja-rijekom-budimpešta', 'dinner': 'najbolja-krstarenja-svečerom-budimpešta'},
    'ru': {'home': '', 'river': 'rechnyye-kruizy-budapesht-dunay', 'dinner': 'uzhin-kruizy-budapesht-dunay'},
    'el': {'home': '', 'river': 'Βουδαπέστη-ποτάμι-κρουαζιέρες', 'dinner': 'καλύτερο-δείπνο-κρουαζιέρες-Βουδαπέστη'},
    'bg': {'home': '', 'river': 'най-добрите-будапеща-речни-круизи', 'dinner': 'най-добрата-вечеря-круизи-будапеща'},
    'es': {'home': '', 'river': 'cruceros-danubio-budapest', 'dinner': 'cruceros-con-cena-danubio-budapest'},
    'sr': {'home': '', 'river': 'најбоље-будапест-река-крстарења', 'dinner': 'најбоља-вечера-крстарења-будимпешта'},
    'he': {'home': '', 'river': 'הפלגות-דנובה-בודפשט', 'dinner': 'ארוחתערב-שייט-דנובה-בודפשט'},
    'pt': {'home': '', 'river': 'budapeste-cruzeiros-danubio', 'dinner': 'budapeste-jantar-cruzeiros-danubio'},
    'sk': {'home': '', 'river': 'riecne-plavby-budapest-dunaj', 'dinner': 'vecera-plavby-budapest-dunaj'},
    'tr': {'home': '', 'river': 'nehir-yolculuklari-budapeste-tuna', 'dinner': 'aksam-yemegi-yolculuklari-budapeste-tuna'},
    'uk': {'home': '', 'river': 'найкращі-річкові-круїзи-будапешті', 'dinner': 'найкраща-вечеря-круїзи-будапешт'},
    'de': {'home': '', 'river': 'bootsfahrten-dunau-budapest', 'dinner': 'bootsfahrten-mit-abendessen-dunau-budapest'},
    'ko': {'home': '', 'river': 'gang-keulujeu-budapeseuteu-danyubeu', 'dinner': 'dineo-keulujeu-budapeseuteu-danyubeu'},
    'nl': {'home': '', 'river': 'beste-boedapest-riviercruises', 'dinner': 'beste-diner-cruises-boedapest'}
}

# UI Microcopy
COMMON_UI = {
    'hu': {
        'btn_book': 'Foglalás most →',
        'read_review': 'Értékelés elolvasása ↓',
        'per_adult': '/ felnőtt',
        'trust_qr': 'Azonnali mobiljegy',
        'trust_cancel': '24 órás ingyenes lemondás',
        'all_river': 'Mind a 10 dunai sétahajó',
        'all_dinner': 'Mind a 7 dunai vacsorahajó',
        'top': 'Fel',
        'pick': 'VÁLASZTÁS',
        'sheet_river': 'Ugrás a tesztelt budapesti sétahajókhoz',
        'sheet_dinner': 'Ugrás a tesztelt budapesti vacsorahajókhoz',
        'verified': 'Személyesen tesztelve',
        'home': 'Főoldal',
        'updated': 'Frissítve: 2026. november'
    },
    'de': {
        'btn_book': 'Jetzt buchen →',
        'read_review': 'Rezension lesen ↓',
        'per_adult': 'pro Erwachsener',
        'trust_qr': 'Sofortiges Smartphone-Ticket',
        'trust_cancel': 'Kostenlose Stornierung bis 24 Std.',
        'all_river': 'Alle 10 Donau-Schifffahrten',
        'all_dinner': 'Alle 7 Abendessen-Schifffahrten',
        'top': 'Nach oben',
        'pick': 'TIPP',
        'sheet_river': 'Zu den getesteten Donau-Schifffahrten',
        'sheet_dinner': 'Zu den getesteten Abendessen-Schifffahrten',
        'verified': 'Vor Ort getestet',
        'home': 'Startseite',
        'updated': 'Aktualisiert: November 2026'
    },
    'fr': {
        'btn_book': 'Réserver maintenant →',
        'read_review': "Lire l'avis ↓",
        'per_adult': 'par adulte',
        'trust_qr': 'Billet mobile instantané',
        'trust_cancel': 'Annulation gratuite 24h',
        'all_river': 'Les 10 croisières sur le Danube',
        'all_dinner': 'Les 7 dîners croisières',
        'top': 'Haut',
        'pick': 'CHOIX',
        'sheet_river': 'Accéder aux croisières testées',
        'sheet_dinner': 'Accéder aux dîners croisières testés',
        'verified': 'Testé personnellement',
        'home': 'Accueil',
        'updated': 'Mis à jour : Novembre 2026'
    },
    'es': {
        'btn_book': 'Reservar ahora →',
        'read_review': 'Leer reseña ↓',
        'per_adult': 'por adulto',
        'trust_qr': 'Ticket móvil instantáneo',
        'trust_cancel': 'Cancelación gratuita 24h',
        'all_river': 'Los 10 cruceros por el Danubio',
        'all_dinner': 'Los 7 cruceros con cena',
        'top': 'Arriba',
        'pick': 'ELECCIÓN',
        'sheet_river': 'Ir a los cruceros evaluados',
        'sheet_dinner': 'Ir a los cruceros con cena evaluados',
        'verified': 'Probado personalmente',
        'home': 'Inicio',
        'updated': 'Actualizado: Noviembre 2026'
    },
    'it': {
        'btn_book': 'Prenota ora →',
        'read_review': 'Leggi recensione ↓',
        'per_adult': 'per adulto',
        'trust_qr': 'Biglietto su smartphone',
        'trust_cancel': 'Cancellazione gratuita 24h',
        'all_river': 'Tutte le 10 crociere sul Danubio',
        'all_dinner': 'Tutte le 7 crociere con cena',
        'top': 'In alto',
        'pick': 'SCELTA',
        'sheet_river': 'Vai alle crociere testate',
        'sheet_dinner': 'Vai alle crociere con cena testate',
        'verified': 'Testato di persona',
        'home': 'Home',
        'updated': 'Aggiornato: Novembre 2026'
    },
    'ro': {
        'btn_book': 'Rezervă acum →',
        'read_review': 'Citește recenzia ↓',
        'per_adult': 'pe adult',
        'trust_qr': 'Bilet electronic instant',
        'trust_cancel': 'Anulare gratuită 24h',
        'all_river': 'Toate cele 10 croaziere pe Dunăre',
        'all_dinner': 'Toate cele 7 croaziere cu cină',
        'top': 'Sus',
        'pick': 'ALEGERE',
        'sheet_river': 'Sari la croazierele testate',
        'sheet_dinner': 'Sari la croazierele cu cină testate',
        'verified': 'Testat personal',
        'home': 'Acasă',
        'updated': 'Actualizat: Noiembrie 2026'
    },
    'pl': {
        'btn_book': 'Zarezerwuj teraz →',
        'read_review': 'Przeczytaj recenzję ↓',
        'per_adult': 'za osobę dorosłą',
        'trust_qr': 'Bilet na telefon',
        'trust_cancel': 'Bezpłatne anulowanie 24h',
        'all_river': 'Wszystkie 10 rejsów po Dunaju',
        'all_dinner': 'Wszystkie 7 rejsów z kolacją',
        'top': 'Góra',
        'pick': 'WYBÓR',
        'sheet_river': 'Przejdź do przetestowanych rejsów',
        'sheet_dinner': 'Przejdź do rejsów z kolacją',
        'verified': 'Sprawdzone osobiście',
        'home': 'Strona główna',
        'updated': 'Zaktualizowano: Listopad 2026'
    },
    'cs': {
        'btn_book': 'Rezervovat nyní →',
        'read_review': 'Přečíst recenzi ↓',
        'per_adult': 'za dospělého',
        'trust_qr': 'Okamžitá mobilní vstupenka',
        'trust_cancel': 'Zrušení zdarma do 24 hod.',
        'all_river': 'Všech 10 plaveb po Dunaji',
        'all_dinner': 'Všech 7 plaveb s večeří',
        'top': 'Nahoru',
        'pick': 'VOLBA',
        'sheet_river': 'Přejít na testované plavby',
        'sheet_dinner': 'Přejít na plavby s večeří',
        'verified': 'Osobně otestováno',
        'home': 'Domů',
        'updated': 'Aktualizováno: Listopad 2026'
    },
    'sk': {
        'btn_book': 'Rezervovať teraz →',
        'read_review': 'Prečítať recenziu ↓',
        'per_adult': 'za dospelého',
        'trust_qr': 'Okamžitý lístok v mobile',
        'trust_cancel': 'Bezplatné zrušenie do 24h',
        'all_river': 'Všetkých 10 plavieb po Dunaji',
        'all_dinner': 'Všetkých 7 plavieb s večerou',
        'top': 'Hore',
        'pick': 'VOĽBA',
        'sheet_river': 'Prejsť na testované plavby',
        'sheet_dinner': 'Prejsť na plavby s večerou',
        'verified': 'Osobne otestované',
        'home': 'Domov',
        'updated': 'Aktualizované: November 2026'
    },
    'nl': {
        'btn_book': 'Nu boeken →',
        'read_review': 'Lees recensie ↓',
        'per_adult': 'per volwassene',
        'trust_qr': 'Direct digitaal ticket',
        'trust_cancel': 'Gratis annuleren tot 24u',
        'all_river': 'Alle 10 Donau-rondvaarten',
        'all_dinner': 'Alle 7 diner-rondvaarten',
        'top': 'Omhoog',
        'pick': 'KEUZE',
        'sheet_river': 'Naar geteste rondvaarten',
        'sheet_dinner': 'Naar geteste dinervaarten',
        'verified': 'Zelf getest',
        'home': 'Home',
        'updated': 'Bijgewerkt: November 2026'
    },
    'pt': {
        'btn_book': 'Reservar agora →',
        'read_review': 'Ler avaliação ↓',
        'per_adult': 'por adulto',
        'trust_qr': 'Bilhete digital no telemóvel',
        'trust_cancel': 'Cancelamento gratuito até 24h',
        'all_river': 'Todos os 10 cruzeiros no Danúbio',
        'all_dinner': 'Todos os 7 cruzeiros com jantar',
        'top': 'Topo',
        'pick': 'ESCOLHA',
        'sheet_river': 'Ir para os cruzeiros testados',
        'sheet_dinner': 'Ir para cruzeiros com jantar',
        'verified': 'Testado pessoalmente',
        'home': 'Início',
        'updated': 'Atualizado: Novembro 2026'
    },
    'hr': {
        'btn_book': 'Rezervirajte sada →',
        'read_review': 'Pročitajte recenziju ↓',
        'per_adult': 'po odrasloj osobi',
        'trust_qr': 'Instant karta na mobitelu',
        'trust_cancel': 'Besplatno otkazivanje do 24h',
        'all_river': 'Svih 10 krstarenja Dunavom',
        'all_dinner': 'Svih 7 krstarenja s večerom',
        'top': 'Vrh',
        'pick': 'IZBOR',
        'sheet_river': 'Idi na testirana krstarenja',
        'sheet_dinner': 'Idi na krstarenja s večerom',
        'verified': 'Osobno provjereno',
        'home': 'Početna',
        'updated': 'Ažurirano: Studeni 2026'
    },
    'sr': {
        'btn_book': 'Резервиши сада →',
        'read_review': 'Прочитајте рецензију ↓',
        'per_adult': 'по одраслој особи',
        'trust_qr': 'Инстант карта на телефону',
        'trust_cancel': 'Бесплатно отказивање до 24ч',
        'all_river': 'Свих 10 крстарења Дунавом',
        'all_dinner': 'Свих 7 крстарења са вечером',
        'top': 'Врх',
        'pick': 'ИЗБОР',
        'sheet_river': 'Пређи на тестирана крстарења',
        'sheet_dinner': 'Пређи на крстарења са вечером',
        'verified': 'Лично проверено',
        'home': 'Почетна',
        'updated': 'Ажурирано: Новембар 2026'
    },
    'bg': {
        'btn_book': 'Резервирайте сега →',
        'read_review': 'Прочетете отзива ↓',
        'per_adult': 'за възрастен',
        'trust_qr': 'Мобилен билет на момента',
        'trust_cancel': 'Безплатно анулиране до 24ч',
        'all_river': 'Всички 10 круиза по Дунав',
        'all_dinner': 'Всички 7 круиза с вечеря',
        'top': 'Нагоре',
        'pick': 'ИЗБОР',
        'sheet_river': 'Към тестваните круизи',
        'sheet_dinner': 'Към тестваните круизи с вечеря',
        'verified': 'Лично тествано',
        'home': 'Начало',
        'updated': 'Обновено: Ноември 2026'
    },
    'ru': {
        'btn_book': 'Забронировать сейчас →',
        'read_review': 'Читать обзор ↓',
        'per_adult': 'за взрослого',
        'trust_qr': 'Электронный билет на телефон',
        'trust_cancel': 'Бесплатная отмена за 24 ч.',
        'all_river': 'Все 10 прогулок по Дунаю',
        'all_dinner': 'Все 7 круизов с ужином',
        'top': 'Наверх',
        'pick': 'ВЫБОР',
        'sheet_river': 'К проверенным круизам',
        'sheet_dinner': 'К проверенным круизам с ужином',
        'verified': 'Проверено лично',
        'home': 'Главная',
        'updated': 'Обновлено: Ноябрь 2026'
    },
    'uk': {
        'btn_book': 'Забронювати зараз →',
        'read_review': 'Читати відгук ↓',
        'per_adult': 'за дорослого',
        'trust_qr': 'Квиток на смартфон',
        'trust_cancel': 'Безкоштовне скасування за 24 год.',
        'all_river': 'Усі 10 круїзів по Дунаю',
        'all_dinner': 'Усі 7 круїзів з вечерею',
        'top': 'Вгору',
        'pick': 'ВИБІР',
        'sheet_river': 'До перевірених круїзів',
        'sheet_dinner': 'До перевірених круїзів з вечерею',
        'verified': 'Перевірено особисто',
        'home': 'Головна',
        'updated': 'Оновлено: Листопад 2026'
    },
    'el': {
        'btn_book': 'Κράτηση τώρα →',
        'read_review': 'Διαβάστε την αξιολόγηση ↓',
        'per_adult': 'ανά ενήλικα',
        'trust_qr': 'Άμεσο ψηφιακό εισιτήριο',
        'trust_cancel': 'Δωρεάν ακύρωση έως 24 ώρες',
        'all_river': 'Και οι 10 κρουαζιέρες στον Δούναβη',
        'all_dinner': 'Και οι 7 κρουαζιέρες με δείπνο',
        'top': 'Κορυφή',
        'pick': 'ΕΠΙΛΟΓΗ',
        'sheet_river': 'Μετάβαση στις κρουαζιέρες',
        'sheet_dinner': 'Μετάβαση στις κρουαζιέρες με δείπνο',
        'verified': 'Δοκιμασμένο προσωπικά',
        'home': 'Αρχική',
        'updated': 'Ενημερώθηκε: Νοέμβριος 2026'
    },
    'tr': {
        'btn_book': 'Şimdi Rezervasyon Yapın →',
        'read_review': 'İncelemeyi Oku ↓',
        'per_adult': 'yetişkin başına',
        'trust_qr': 'Anında mobil bilet',
        'trust_cancel': '24 saate kadar ücretsiz iptal',
        'all_river': 'Tüm 10 Tuna Gezisi',
        'all_dinner': 'Tüm 7 Yemekli Tuna Turu',
        'top': 'Yukarı',
        'pick': 'SEÇİM',
        'sheet_river': 'Test edilen turlara git',
        'sheet_dinner': 'Test edilen akşam yemekli turlara git',
        'verified': 'Bizzat test edildi',
        'home': 'Ana Sayfa',
        'updated': 'Güncellendi: Kasım 2026'
    },
    'he': {
        'btn_book': 'הזמן עכשיו ←',
        'read_review': 'קרא ביקורת מלאה ↓',
        'per_adult': 'למבוגר',
        'trust_qr': 'כרטיס דיגיטלי מיידי',
        'trust_cancel': 'ביטול חינם עד 24 שעות',
        'all_river': 'כל 10 ההפלגות בדנובה',
        'all_dinner': 'כל 7 הפלגות הערב עם ארוחה',
        'top': 'למעלה',
        'pick': 'בחירה',
        'sheet_river': 'עבור להפלגות שנבדקו',
        'sheet_dinner': 'עבור להפלגות ערב שנבדקו',
        'verified': 'נבדק אישית',
        'home': 'דף הבית',
        'updated': 'עודכן: נובמבר 2026'
    },
    'ja': {
        'btn_book': '今すぐ予約する →',
        'read_review': '詳細レビューを読む ↓',
        'per_adult': '大人1名',
        'trust_qr': '即時スマホQRバウチャー',
        'trust_cancel': '24時間前までキャンセル無料',
        'all_river': '全10のドナウ川クルーズ',
        'all_dinner': '全7のディナークルーズ',
        'top': 'トップへ',
        'pick': 'おすすめ',
        'sheet_river': '実走テスト済みクルーズ一覧',
        'sheet_dinner': '実走テスト済みディナークルーズ一覧',
        'verified': '現地で実走テスト済み',
        'home': 'ホーム',
        'updated': '更新日: 2026年11月'
    },
    'ko': {
        'btn_book': '지금 예약하기 →',
        'read_review': '상세 리뷰 보기 ↓',
        'per_adult': '성인 1인',
        'trust_qr': '스마트폰 즉시 QR 바우처',
        'trust_cancel': '24시간 전까지 무료 취소',
        'all_river': '다뉴브 유람선 10개 전체보기',
        'all_dinner': '디너 크루즈 7개 전체보기',
        'top': '맨 위로',
        'pick': '추천',
        'sheet_river': '검증된 다뉴브 크루즈 바로가기',
        'sheet_dinner': '검증된 디너 크루즈 바로가기',
        'verified': '직접 현장 검증',
        'home': '홈',
        'updated': '업데이트: 2026년 11월'
    }
}

def get_ui(lang, key, default=''):
    return COMMON_UI.get(lang, {}).get(key, default)

def localize_guide_page_ui(soup, lang, cruise_type, total_count):
    btn_book_text = get_ui(lang, 'btn_book', 'Book Now →')
    read_review_text = get_ui(lang, 'read_review', 'Read Review ↓')
    per_adult_text = get_ui(lang, 'per_adult', '/ adult')
    trust_qr_text = get_ui(lang, 'trust_qr', 'Instant Smartphone Ticket')
    trust_cancel_text = get_ui(lang, 'trust_cancel', 'Free 24h Cancel')
    all_cruises_text = get_ui(lang, 'all_river' if cruise_type == 'river' else 'all_dinner', f'All {total_count} Cruises')
    top_text = get_ui(lang, 'top', 'Top')
    pick_word = get_ui(lang, 'pick', 'PICK')
    sheet_title_text = get_ui(lang, 'sheet_river' if cruise_type == 'river' else 'sheet_dinner', 'Tested Budapest Cruises')
    verified_text = get_ui(lang, 'verified', 'Personally Tested')

    buy_data = BUY_CARD_I18N.get(lang, BUY_CARD_I18N['de'])
    toggle_data = REVIEW_TOGGLE_I18N.get(lang, REVIEW_TOGGLE_I18N['de'])
    bd_data = BREAKDOWN_I18N.get(lang, BREAKDOWN_I18N['de'])

    # 0. Clean Breadcrumbs & Trust Pill
    home_text = get_ui(lang, 'home', 'Home')
    for bc in soup.find_all(class_='ltt-breadcrumbs'):
        curr = bc.find(class_='ltt-bc-current')
        curr_text = curr.get_text(strip=True) if curr else (bd_data['title_river'] if cruise_type == 'river' else bd_data['title_dinner'])
        bc.clear()
        home_a = soup.new_tag('a', href=f'/{lang}/' if lang != 'en' else '/')
        home_a.string = home_text
        sep = soup.new_tag('span', **{'class': 'ltt-bc-sep'})
        sep.string = '›'
        n_curr = soup.new_tag('span', **{'class': 'ltt-bc-current'})
        n_curr.string = curr_text
        bc.append(home_a)
        bc.append(' ')
        bc.append(sep)
        bc.append(' ')
        bc.append(n_curr)

    updated_str = get_ui(lang, 'updated', 'Updated: November 2026')
    tp = soup.find(class_='ltt-trust-pill')
    if tp:
        tp.clear()
        parts = updated_str.split(':')
        lbl = parts[0].strip()
        val = parts[1].strip() if len(parts) > 1 else 'November 2026'
        st = soup.new_tag('strong')
        st.string = lbl
        tp.append(st)
        tp.append(f': {val}')

    # 1. Deck Cards
    for idx, card in enumerate(soup.find_all(class_='bpa-card')):
        btn = card.find(class_='bpa-btn')
        if btn: btn.string = btn_book_text
        
        psub = card.find(class_='bpa-psub')
        if psub: psub.string = per_adult_text
        
        sublink = card.find(class_='bpa-sublink') or card.find(class_='bpa-jump-link')
        if sublink: sublink.string = read_review_text
        
        if cruise_type == 'dinner' and idx in [5, 6]:
            card['data-cat'] = card.get('data-cat', '').replace('tested', '').strip()
            for p in card.find_all(class_='bpa-proof') + card.find_all(class_='bpa-proof-mobile') + card.find_all(class_='bpa-vchip'):
                p.decompose()
        elif cruise_type == 'river' and idx >= 6:
            card['data-cat'] = card.get('data-cat', '').replace('tested', '').strip()
            for p in card.find_all(class_='bpa-proof') + card.find_all(class_='bpa-proof-mobile') + card.find_all(class_='bpa-vchip'):
                p.decompose()
        else:
            vchip = card.find(class_='bpa-vchip')
            if vchip: vchip.string = f"✓ {verified_text}"
        
        trust = card.find(class_='bpa-trust-micro')
        if trust:
            spans = trust.find_all('span')
            if len(spans) >= 3:
                spans[0].string = trust_qr_text
                spans[2].string = trust_cancel_text

    # Details Cards Proof Badges
    for idx, dc in enumerate(soup.find_all('details', class_='bpa-details-card')):
        if cruise_type == 'dinner' and idx in [5, 6]:
            dc['data-cat'] = dc.get('data-cat', '').replace('tested', '').strip()
            for p in dc.find_all(class_='bpa-proof') + dc.find_all(class_='bpa-vchip'):
                p.decompose()
        elif cruise_type == 'river' and idx >= 6:
            dc['data-cat'] = dc.get('data-cat', '').replace('tested', '').strip()
            for p in dc.find_all(class_='bpa-proof') + dc.find_all(class_='bpa-vchip'):
                p.decompose()

    # 1b. Filter Tabs (.ltt-tab-btn)
    tab_data = FILTER_TABS_I18N.get(lang, {})
    if tab_data:
        for tab in soup.find_all(class_='ltt-tab-btn'):
            cat = tab.get('data-cat')
            if cruise_type == 'dinner':
                if cat == 'all' and 'all' in tab_data:
                    tab.string = tab_data['all'].replace('(10)', '(7)')
                elif cat == 'tested' and 'tested_dinner' in tab_data:
                    tab.string = tab_data['tested_dinner']
                elif cat == 'drinks' and 'drinks_dinner' in tab_data:
                    tab.string = tab_data['drinks_dinner']
                elif cat == 'under80' and 'budget' in tab_data:
                    tab.string = tab_data['budget']
                elif cat in tab_data:
                    tab.string = tab_data[cat]
            else:
                if cat in tab_data:
                    tab.string = tab_data[cat]

    # 2. Details Card Buy Cards (.ltt-buy-card)
    for bc in soup.find_all(class_='ltt-buy-card'):
        # Badge
        badge = bc.find(class_='ltt-buy-card-badge')
        if badge:
            for s in badge.find_all('span'):
                if 'ltt-live-dot' not in s.get('class', []):
                    s.string = buy_data['badge']
                    break
                    
        # Price sub
        psub = bc.find(class_='ltt-buy-price-sub')
        if psub:
            psub.string = buy_data['per_adult']
            
        # Perks
        for perk in bc.find_all(class_='ltt-buy-perk'):
            st = perk.find('strong')
            if st:
                txt = perk.get_text()
                st_text = st.get_text(strip=True)
                if any(k in txt.lower() for k in ['departure', 'départ', 'salida', 'partenza', 'vertrek', 'wypłynięcie', 'plecare', 'odjezd', 'polazak', 'отправление', 'αναχώρηση', 'отплаване', 'полазак', 'יציאה', 'partida', 'odchod', 'kalkış', 'відправлення', '出航', '출발', 'indulás', 'abfahrt']):
                    perk.clear()
                    perk.append(f"{buy_data['departure']} ")
                    nst = soup.new_tag('strong')
                    nst.string = st_text
                    perk.append(nst)
                elif any(k in txt.lower() for k in ['duration', 'durée', 'duración', 'durata', 'duur', 'czas trwania', 'durată', 'doba trvání', 'trajanje', 'продолжительность', 'διάρκεια', 'продължителност', 'трајање', 'משך', 'duração', 'trvanie', 'süre', 'тривалість', '所要時間', '운항 시간', 'időtartam', 'dauer']):
                    perk.clear()
                    perk.append(f"{buy_data['duration']} ")
                    nst = soup.new_tag('strong')
                    nst.string = st_text
                    perk.append(nst)
            else:
                txt = perk.get_text().strip()
                if any(k in txt.lower() for k in ['qr', 'smartphone', 'mobile', 'telefon', 'handy', 'celular', 'mobitel', 'телефон', 'κινητό', 'סמארטפון', 'telemóvel', 'smartfón', '스마트폰', 'スマホ']):
                    perk.string = buy_data['qr']
                elif any(k in txt.lower() for k in ['refund', '24h', 'remboursement', 'reembolso', 'rimborso', 'terugbetaling', 'zwrot', 'rambursare', 'vrácení', 'povrat', 'возврат', 'επιστροφή', 'възстановяване', 'повраћај', 'החזר', 'vrátenie', 'iade', 'повернення', '返金', '환불', 'lemondás', 'stornierung']):
                    perk.string = buy_data['refund']
                    
        # CTA Button
        cta = bc.find(class_='ltt-buy-cta-btn')
        if cta:
            spans = cta.find_all('span')
            if spans:
                btn_clean = btn_book_text.replace(' →', '').replace(' ->', '').replace(' ←', '').strip()
                spans[0].string = btn_clean
                if len(spans) > 1 and 'ltt-cta-arrow' in spans[1].get('class', []):
                    spans[1].string = '←' if lang == 'he' else '→'
            else:
                cta.string = btn_book_text
                
        # Trust microcopy
        trust = bc.find(class_='ltt-buy-card-trust')
        if trust:
            t_span = trust.find('span')
            if t_span:
                t_span.string = buy_data['trust']

    # 3. Review Toggle CSS Pseudo-elements in <style>
    collapse_str = toggle_data['collapse'].replace('"', '\\"')
    read_str = toggle_data['read'].replace('"', '\\"')
    for style in soup.find_all('style'):
        if style.string and 'bpa-details-state-text::before' in style.string:
            s = style.string
            s = re.sub(
                r'(\.bpa-details-card\[open\]\s*\.bpa-details-state-text::before\s*\{\s*content:\s*")[^"]*(";?\s*\})',
                lambda m: m.group(1) + collapse_str + m.group(2),
                s
            )
            s = re.sub(
                r'(\.bpa-details-card:not\(\[open\]\)\s*\.bpa-details-state-text::before\s*\{\s*content:\s*")[^"]*(";?\s*\})',
                lambda m: m.group(1) + read_str + m.group(2),
                s
            )
            style.string = s

    # 4. Breakdown Section Heading & Controls
    heading_text = bd_data['river_title'] if cruise_type == 'river' else bd_data['dinner_title']
    h2 = soup.find(class_='bpa-breakdown-heading')
    if h2:
        h2.string = heading_text
        
    sub = soup.find(class_='bpa-breakdown-sub')
    if sub:
        sub.string = bd_data['sub']
        
    for btn in soup.find_all(class_='bpa-acc-ctrl-btn'):
        onclick = btn.get('onclick', '')
        if 'true' in onclick:
            btn.string = bd_data['expand']
        elif 'false' in onclick:
            btn.string = bd_data['collapse']

    # 5. Proof Chips across all elements (.bpa-proof, .bpa-proof-mobile, .bpa-vchip)
    for vchip in soup.find_all(class_='bpa-vchip'):
        vchip.string = f"✓ {verified_text}"
        
    for proof in soup.find_all(class_=lambda c: c and ('bpa-proof' in c or 'bpa-proof-mobile' in c)):
        if not proof.find(class_='bpa-vchip'):
            proof.string = f"✓ {verified_text}"

    # 6. Mobile Drawer
    drawer = soup.find(class_='bpa-mobile-drawer')
    if drawer:
        d_btn = drawer.find(class_='bpa-drawer-btn')
        if d_btn: d_btn.string = btn_book_text

    # 7. Floating Bar
    bar = soup.find(id='sticky-bar')
    if bar:
        toc_btn = bar.find(id='hybridTocBtn')
        if toc_btn:
            span = toc_btn.find('span')
            if span: span.string = all_cruises_text
            
        top_btn = bar.find(class_='hybrid-top-btn')
        if top_btn:
            span = top_btn.find('span')
            if span: span.string = top_text
            
        s_rank = bar.find(id='sticky-rank')
        if s_rank: s_rank.string = f"#1 {pick_word}"
        
        s_trust = bar.find(class_='hybrid-active-trust')
        if s_trust: s_trust.string = trust_cancel_text
        
        s_btn = bar.find(id='sticky-cta-btn')
        if s_btn: s_btn.string = btn_book_text

    sheet = soup.find(id='hybridSheet')
    if sheet:
        stitle = sheet.find(class_='hybrid-sheet-title')
        if stitle: stitle.string = sheet_title_text

    # 8. window.LTT_PAGE_CONFIG
    for s in soup.find_all('script'):
        if s.string and 'window.LTT_PAGE_CONFIG' in s.string:
            s_content = s.string
            match = re.search(r'window\.LTT_PAGE_CONFIG\s*=\s*(\{.*?\});', s_content)
            if match:
                try:
                    cfg_obj = json.loads(match.group(1))
                    cfg_obj['pickLabel'] = pick_word
                    cfg_obj['btnText'] = btn_book_text
                    cfg_obj['tocDeckLabel'] = bd_data['deck_river'] if cruise_type == 'river' else bd_data['deck_dinner']
                    cfg_obj['tocBreakdownLabel'] = bd_data['toc_river'] if cruise_type == 'river' else bd_data['toc_dinner']
                    s.string = f"window.LTT_PAGE_CONFIG = {json.dumps(cfg_obj, ensure_ascii=False)};"
                except Exception:
                    pass
            break

def localize_author_box(soup, lang):
    author_box = soup.find(class_='ltt-author-box')
    if not author_box:
        return
    data = AUTHOR_I18N.get(lang, AUTHOR_I18N['de'])
    
    role = author_box.find(class_='ltt-author-role')
    if role:
        role.string = data['role']
        
    vbadges = author_box.find_all(class_='ltt-vbadge')
    for idx, vb in enumerate(vbadges[:3]):
        if idx < len(data['badges']):
            vb.string = data['badges'][idx]
            
    bio = author_box.find(class_='ltt-author-bio')
    if bio:
        bio.string = data['bio']
        
    links_div = author_box.find(class_='ltt-author-links')
    if links_div:
        a = links_div.find('a')
        if a:
            a.string = data['link']
            a['href'] = '/about'

def extract_meta_and_headings(harvested_path):
    if not os.path.exists(harvested_path):
        return None
    soup = BeautifulSoup(open(harvested_path, 'r', encoding='utf-8').read(), 'html.parser')
    
    title = soup.title.string.strip() if soup.title and soup.title.string else ''
    meta_desc = ''
    m = soup.find('meta', {'name': 'description'})
    if m and m.get('content'):
        meta_desc = m['content'].strip()
    
    h1 = soup.find('h1')
    h1_text = h1.text.strip() if h1 else ''
    
    h2s = [h2.text.strip() for h2 in soup.find_all('h2') if h2.text.strip()]
    return {
        'title': title,
        'description': meta_desc,
        'h1': h1_text,
        'h2s': h2s
    }

NAV_I18N = {
    'hu': {'dropdown': 'Dunai Hajózás', 'head_cruises': 'DUNAI SÉTAHAJÓK', 'head_attractions': 'LÁTNIVALÓK ÉS FÜRDŐK', 'river': 'Dunai Sétahajók', 'dinner': 'Vacsorahajók', 'card': 'Budapest Kártya', 'about': 'Rólunk', 'contact': 'Kapcsolat', 'footer_flagship': 'Kiemelt Budapesti Kalauzok', 'footer_trust': 'Megbízhatóság és Vállalat', 'footer_copy': '© 2026 BudapestAdventures.com. Minden jog fenntartva.'},
    'de': {'dropdown': 'Donau-Schifffahrten', 'head_cruises': 'DONAU-SCHIFFFAHRTEN', 'head_attractions': 'SEHENSWÜRDIGKEITEN & BÄDER', 'river': 'Donau-Schifffahrten', 'dinner': 'Abendessen-Schifffahrten', 'card': 'Budapest Card', 'about': 'Über uns', 'contact': 'Kontakt', 'footer_flagship': 'Wichtige Budapest-Guides', 'footer_trust': 'Vertrauen & Unternehmen', 'footer_copy': '© 2026 BudapestAdventures.com. Alle Rechte vorbehalten.'},
    'fr': {'dropdown': 'Croisières Danube', 'head_cruises': 'CROISIÈRES SUR LE DANUBE', 'head_attractions': 'ATTRACTIONS & BAINS', 'river': 'Croisières Promenade', 'dinner': 'Dîners Croisières', 'card': 'Budapest Card', 'about': 'À propos', 'contact': 'Contact', 'footer_flagship': 'Guides Phares de Budapest', 'footer_trust': 'Confiance & Entreprise', 'footer_copy': '© 2026 BudapestAdventures.com. Tous droits réservés.'},
    'es': {'dropdown': 'Cruceros Danubio', 'head_cruises': 'CRUCEROS POR EL DANUBIO', 'head_attractions': 'ATRACCIONES Y BALNEARIOS', 'river': 'Cruceros Paseo', 'dinner': 'Cruceros con Cena', 'card': 'Budapest Card', 'about': 'Sobre nosotros', 'contact': 'Contacto', 'footer_flagship': 'Guías Principales de Budapest', 'footer_trust': 'Confianza y Empresa', 'footer_copy': '© 2026 BudapestAdventures.com. Todos los derechos reservados.'},
    'it': {'dropdown': 'Crociere Danubio', 'head_cruises': 'CROCIERE SUL DANUBIO', 'head_attractions': 'ATTRAZIONI E TERME', 'river': 'Crociere Panoramiche', 'dinner': 'Crociere con Cena', 'card': 'Budapest Card', 'about': 'Chi siamo', 'contact': 'Contatti', 'footer_flagship': 'Guide Principali di Budapest', 'footer_trust': 'Affidabilità & Azienda', 'footer_copy': '© 2026 BudapestAdventures.com. Tutti i diritti riservati.'},
    'ro': {'dropdown': 'Croaziere Dunăre', 'head_cruises': 'CROAZIERE PE DUNĂRE', 'head_attractions': 'ATRACȚII & BĂI TERMALE', 'river': 'Croaziere pe Dunăre', 'dinner': 'Croaziere cu Cină', 'card': 'Budapest Card', 'about': 'Despre noi', 'contact': 'Contact', 'footer_flagship': 'Ghiduri de Top în Budapesta', 'footer_trust': 'Încredere & Companie', 'footer_copy': '© 2026 BudapestAdventures.com. Toate drepturile rezervate.'},
    'pl': {'dropdown': 'Rejsy po Dunaju', 'head_cruises': 'REJSY PO DUNAJU', 'head_attractions': 'ATRAKCJE I TERMY', 'river': 'Rejsy Widokowe', 'dinner': 'Rejsy z Kolacją', 'card': 'Budapest Card', 'about': 'O nas', 'contact': 'Kontakt', 'footer_flagship': 'Główne Przewodniki po Budapeszcie', 'footer_trust': 'Zaufanie i Informacje', 'footer_copy': '© 2026 BudapestAdventures.com. Wszelkie prawa zastrzeżone.'},
    'cs': {'dropdown': 'Plavby po Dunaji', 'head_cruises': 'PLAVBY PO DUNAJI', 'head_attractions': 'PAMÁTKY A LÁZNĚ', 'river': 'Vyhlídkové Plavby', 'dinner': 'Plavby s Večeří', 'card': 'Budapest Card', 'about': 'O nás', 'contact': 'Kontakt', 'footer_flagship': 'Hlavní Průvodci Budapeští', 'footer_trust': 'Důvěryhodnost a Společnost', 'footer_copy': '© 2026 BudapestAdventures.com. Všechna práva vyhrazena.'},
    'sk': {'dropdown': 'Plavby po Dunaji', 'head_cruises': 'PLAVBY PO DUNAJI', 'head_attractions': 'PAMIATKY A KÚPELE', 'river': 'Vyhliadkové Plavby', 'dinner': 'Plavby s Večerou', 'card': 'Budapest Card', 'about': 'O nás', 'contact': 'Kontakt', 'footer_flagship': 'Hlavné Sprievodce Budapešťou', 'footer_trust': 'Dôveryhodnosť a Spoločnosť', 'footer_copy': '© 2026 BudapestAdventures.com. Všetky práva vyhradené.'},
    'nl': {'dropdown': 'Donau Cruises', 'head_cruises': 'DONAU RIVIERCRUISES', 'head_attractions': 'ATTRACTIES & BADEN', 'river': 'Riviercruises', 'dinner': 'Diner Cruises', 'card': 'Budapest Card', 'about': 'Over ons', 'contact': 'Contact', 'footer_flagship': 'Belangrijkste Boedapest Gidsen', 'footer_trust': 'Vertrouwen & Bedrijf', 'footer_copy': '© 2026 BudapestAdventures.com. Alle rechten voorbehouden.'},
    'pt': {'dropdown': 'Cruzeiros Danúbio', 'head_cruises': 'CRUZEIROS NO DANÚBIO', 'head_attractions': 'ATRAÇÕES E TERMAS', 'river': 'Cruzeiros no Danúbio', 'dinner': 'Cruzeiros com Jantar', 'card': 'Budapest Card', 'about': 'Sobre nós', 'contact': 'Contato', 'footer_flagship': 'Principais Guias de Budapeste', 'footer_trust': 'Confiança e Empresa', 'footer_copy': '© 2026 BudapestAdventures.com. Todos os direitos reservados.'},
    'ja': {'dropdown': 'ドナウ川クルーズ', 'head_cruises': 'ドナウ川クルーズ', 'head_attractions': '観光名所＆温泉', 'river': 'リバークルーズ', 'dinner': 'ディナークルーズ', 'card': 'ブダペストカード', 'about': '運営情報', 'contact': 'お問い合わせ', 'footer_flagship': 'ブダペスト主要ガイド', 'footer_trust': '信頼と運営方針', 'footer_copy': '© 2026 BudapestAdventures.com. All rights reserved.'},
    'hr': {'dropdown': 'Krstarenja Dunavom', 'head_cruises': 'KRSTARENJA DUNAVOM', 'head_attractions': 'ATRAKCIJE & TOPLICE', 'river': 'Panoramska Krstarenja', 'dinner': 'Krstarenja s Večerom', 'card': 'Budapest Card', 'about': 'O nama', 'contact': 'Kontakt', 'footer_flagship': 'Vodeći Vodiči kroz Budimpeštu', 'footer_trust': 'Povjerenje & Tvrtka', 'footer_copy': '© 2026 BudapestAdventures.com. Sva prava pridržana.'},
    'ru': {'dropdown': 'Круизы по Дунаю', 'head_cruises': 'КРУИЗЫ ПО ДУНАЮ', 'head_attractions': 'ДОСТОПРИМЕЧАТЕЛЬНОСТИ И КУПАЛЬНИ', 'river': 'Прогулочные Круизы', 'dinner': 'Круизы с Ужином', 'card': 'Budapest Card', 'about': 'О нас', 'contact': 'Контакты', 'footer_flagship': 'Главные Гиды по Будапешту', 'footer_trust': 'Доверие и Компания', 'footer_copy': '© 2026 BudapestAdventures.com. Все права защищены.'},
    'el': {'dropdown': 'Κρουαζιέρες Δούναβη', 'head_cruises': 'ΚΡΟΥΑΖΙΕΡΕΣ ΣΤΟΝ ΔΟΥΝΑΒΗ', 'head_attractions': 'ΑΞΙΟΘΕΑΤΑ & ΛΟΥΤΡΑ', 'river': 'Κρουαζιέρες Περιήγησης', 'dinner': 'Κρουαζιέρες με Δείπνο', 'card': 'Budapest Card', 'about': 'Σχετικά', 'contact': 'Επικοινωνία', 'footer_flagship': 'Κορυφαίοι Οδηγοί Βουδαπέστης', 'footer_trust': 'Εμπιστοσύνη & Εταιρεία', 'footer_copy': '© 2026 BudapestAdventures.com. Με επιφύλαξη παντός δικαιώματος.'},
    'bg': {'dropdown': 'Круизи по Дунав', 'head_cruises': 'КРУИЗИ ПО ДУНАВ', 'head_attractions': 'ЗАБЕЛЕЖИТЕЛНОСТИ И БАНИ', 'river': 'Панорамни Круизи', 'dinner': 'Круизи с Вечеря', 'card': 'Budapest Card', 'about': 'За нас', 'contact': 'Контакти', 'footer_flagship': 'Водещи Пътеводители за Будапеща', 'footer_trust': 'Доверие и Компания', 'footer_copy': '© 2026 BudapestAdventures.com. Всички права запазени.'},
    'sr': {'dropdown': 'Krstarenja Dunavom', 'head_cruises': 'KRSTARENJA DUNAVOM', 'head_attractions': 'ATRAKCIJE & BANJE', 'river': 'Panoramska Krstarenja', 'dinner': 'Krstarenja sa Večerom', 'card': 'Budapest Card', 'about': 'O nama', 'contact': 'Kontakt', 'footer_flagship': 'Glavni Vodiči kroz Budimpeštu', 'footer_trust': 'Poverenje & Kompanija', 'footer_copy': '© 2026 BudapestAdventures.com. Sva prava zadržana.'},
    'he': {'dropdown': 'שייט על הדנובה', 'head_cruises': 'שייט על הדנובה', 'head_attractions': 'אטרקציות ומרחצאות', 'river': 'שייט סיור', 'dinner': 'שייט עם ארוחת ערב', 'card': 'כרטיס בודפשט', 'about': 'אודות', 'contact': 'צור קשר', 'footer_flagship': 'מדריכי הדגל של בודפשט', 'footer_trust': 'אמינות והחברה', 'footer_copy': '© 2026 BudapestAdventures.com. כל הזכויות שמורות.'},
    'tr': {'dropdown': 'Tuna Nehri Turları', 'head_cruises': 'TUNA NEHRİ TURLARI', 'head_attractions': 'GEZİLECEK YERLER VE KAPLICALAR', 'river': 'Nehir Gezi Turları', 'dinner': 'Akşam Yemekli Turlar', 'card': 'Budapest Card', 'about': 'Hakkımızda', 'contact': 'İletişim', 'footer_flagship': 'Öne Çıkan Budapeşte Rehberleri', 'footer_trust': 'Güvenilirlik ve Şirket', 'footer_copy': '© 2026 BudapestAdventures.com. Tüm hakları saklıdır.'},
    'uk': {'dropdown': 'Круїзи по Дунаю', 'head_cruises': 'КРУЇЗИ ПО ДУНАЮ', 'head_attractions': 'ВИЗНАЧНІ МІСЦЯ ТА КУПАЛЬНІ', 'river': 'Оглядові Круїзи', 'dinner': 'Круїзи з Вечерею', 'card': 'Budapest Card', 'about': 'Про нас', 'contact': 'Контакти', 'footer_flagship': 'Головні Гіди по Будапешту', 'footer_trust': 'Довіра та Компанія', 'footer_copy': '© 2026 BudapestAdventures.com. Всі права захищені.'},
    'ko': {'dropdown': '다뉴브강 크루즈', 'head_cruises': '다뉴브강 유람선', 'head_attractions': '관광명소 & 온천', 'river': '유람선 투어', 'dinner': '디너 크루즈', 'card': '부다페스트 카드', 'about': '소개', 'contact': '문의하기', 'footer_flagship': '부다페스트 주요 여행 가이드', 'footer_trust': '신뢰 & 운영 정책', 'footer_copy': '© 2026 BudapestAdventures.com. All rights reserved.'}
}

def localize_nav_and_footer_multilingual(soup, lang, slugs):
    river_slug = slugs.get('river', 'best-budapest-river-cruises')
    dinner_slug = slugs.get('dinner', 'best-dinner-cruises-budapest')
    
    # 0. Set HTML lang attribute
    html_tag = soup.find('html')
    if html_tag:
        html_tag['lang'] = lang
    
    # 1. Update internal hrefs to point to localized slugs
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href in ['/best-budapest-river-cruises', '/budapest-river-cruises']:
            a['href'] = f'/{lang}/{river_slug}'
        elif href in ['/best-dinner-cruises-budapest', '/budapest-dinner-cruises']:
            a['href'] = f'/{lang}/{dinner_slug}'
        elif href == '/':
            a['href'] = f'/{lang}/'

    # 2. Localize Navigation
    i18n = NAV_I18N.get(lang)
    if i18n:
        dropdown_btn = soup.find('button', class_='ltt-dropdown-btn')
        if dropdown_btn:
            span = dropdown_btn.find('span')
            if span and 'dropdown' in i18n:
                span.string = i18n['dropdown']
                
        mega_heads = soup.find_all(class_='ltt-mega-head')
        if len(mega_heads) >= 1 and 'head_cruises' in i18n:
            mega_heads[0].string = i18n['head_cruises']
        if len(mega_heads) >= 2 and 'head_attractions' in i18n:
            mega_heads[1].string = i18n['head_attractions']
            
        nav_links = soup.find_all(class_='ltt-nav-link')
        for nl in nav_links:
            if 'ltt-dropdown-btn' in nl.get('class', []):
                continue
            txt = nl.text.strip().lower()
            if 'river' in txt or 'sétahajó' in txt: nl.string = i18n.get('river', nl.text)
            elif 'dinner' in txt or 'vacsorahajó' in txt: nl.string = i18n.get('dinner', nl.text)
            elif 'card' in txt or 'kártya' in txt: nl.string = i18n.get('card', nl.text)
            elif 'about' in txt or 'rólunk' in txt: nl.string = i18n.get('about', nl.text)
            elif 'contact' in txt or 'kapcsolat' in txt: nl.string = i18n.get('contact', nl.text)

    # 3. Localize Footer
    footer = soup.find('footer') or soup.find(class_='footer-dark')
    if footer:
        f_data = FOOTER_I18N.get(lang, FOOTER_I18N['de'])
        
        # Brand Description
        brand_desc = footer.find(class_='footer-brand-desc') or footer.find(class_='footer-paragraph')
        if brand_desc:
            brand_desc.string = f_data['desc']
            
        # Column Titles
        col_titles = footer.find_all(class_=lambda c: c and ('footer-col-title' in c or 'footer-link-title' in c))
        if len(col_titles) >= 1:
            col_titles[0].string = f_data['flagship_title']
        if len(col_titles) >= 2:
            col_titles[1].string = f_data['trust_title']
            
        # Footer Links
        link_map = f_data['links']
        footer_links = footer.find_all('a', class_=lambda c: c and ('footer-link-item' in c or 'footer-link-3' in c))
        for fl in footer_links:
            href = fl.get('href', '')
            if href in ['/best-budapest-river-cruises', f'/{lang}/{river_slug}'] or 'river' in href:
                fl.string = link_map['river']
                fl['href'] = f'/{lang}/{river_slug}'
            elif href in ['/best-dinner-cruises-budapest', f'/{lang}/{dinner_slug}'] or 'dinner' in href:
                fl.string = link_map['dinner']
                fl['href'] = f'/{lang}/{dinner_slug}'
            elif 'card' in href:
                fl.string = link_map['card']
            elif 'thermal' in href or 'baths' in href:
                fl.string = link_map['baths']
            elif 'night' in href:
                fl.string = link_map['night']
            elif 'prosecco' in href:
                fl.string = link_map['prosecco']
            elif 'private' in href:
                fl.string = link_map['private']
            elif 'walking' in href:
                fl.string = link_map['walking']
            elif 'hostels' in href:
                fl.string = link_map['hostels']
            elif href == '/about':
                fl.string = link_map['about']
            elif 'ethics' in href or 'methodology' in href:
                fl.string = link_map['ethics']
            elif 'manifesto' in href:
                fl.string = link_map['manifesto']
            elif 'contact' in href:
                fl.string = link_map['contact']

        # Legal Copyright and Subtitle
        legal = footer.find(class_='legal-wrapper')
        if legal:
            divs = legal.find_all(class_='legal-text') or legal.find_all('div')
            if len(divs) >= 1:
                divs[0].string = f_data['copy']
            if len(divs) >= 2:
                divs[1].string = f_data['sub']

def compile_pages():
    print(f"Starting compilation for {len(LANGS)} languages...")
    
    en_river_html = open(os.path.join(BASE_DIR, 'river.html'), 'r', encoding='utf-8').read()
    en_dinner_html = open(os.path.join(BASE_DIR, 'dinner.html'), 'r', encoding='utf-8').read()
    en_home_html = open(os.path.join(BASE_DIR, 'index.html'), 'r', encoding='utf-8').read()
    
    compiled_count = 0
    
    for lang in LANGS:
        slugs = SLUG_MAP[lang]
        river_slug = slugs['river']
        dinner_slug = slugs['dinner']
        lang_dir = os.path.join(BASE_DIR, lang)
        os.makedirs(lang_dir, exist_ok=True)

        if lang == 'hu':
            bhp.build_hungarian_home()
            bhp.build_hungarian_river()
            bhp.build_hungarian_dinner()

            # Post-process HU river guide for full parity (ltt-buy-card, CSS pseudo-elements, breakdown heading, proof chips)
            hu_river_path = os.path.join(BASE_DIR, 'hu', 'setahajozas-a-dunan-budapest', 'index.html')
            if os.path.exists(hu_river_path):
                soup_hu_river = BeautifulSoup(open(hu_river_path, 'r', encoding='utf-8').read(), 'html.parser')
                localize_guide_page_ui(soup_hu_river, 'hu', 'river', 10)
                localize_nav_and_footer_multilingual(soup_hu_river, 'hu', slugs)
                with open(hu_river_path, 'w', encoding='utf-8') as f:
                    f.write(str(soup_hu_river))

            # Post-process HU dinner guide
            hu_dinner_path = os.path.join(BASE_DIR, 'hu', 'setahajozas-a-dunan-vacsoraval', 'index.html')
            if os.path.exists(hu_dinner_path):
                soup_hu_dinner = BeautifulSoup(open(hu_dinner_path, 'r', encoding='utf-8').read(), 'html.parser')
                localize_guide_page_ui(soup_hu_dinner, 'hu', 'dinner', 7)
                localize_nav_and_footer_multilingual(soup_hu_dinner, 'hu', slugs)
                with open(hu_dinner_path, 'w', encoding='utf-8') as f:
                    f.write(str(soup_hu_dinner))

            # Post-process HU home
            hu_home_path = os.path.join(BASE_DIR, 'hu', 'index.html')
            if os.path.exists(hu_home_path):
                soup_hu_home = BeautifulSoup(open(hu_home_path, 'r', encoding='utf-8').read(), 'html.parser')
                localize_author_box(soup_hu_home, 'hu')
                localize_nav_and_footer_multilingual(soup_hu_home, 'hu', slugs)
                with open(hu_home_path, 'w', encoding='utf-8') as f:
                    f.write(str(soup_hu_home))

            compiled_count += 3
            print(f"✓ [HU] Compiled Hungarian home, river ({river_slug}), and dinner ({dinner_slug}) with 100% native localization")
            continue
        
        # 1. COMPILE RIVER GUIDE
        river_dir = os.path.join(lang_dir, river_slug)
        os.makedirs(river_dir, exist_ok=True)
        river_out = os.path.join(river_dir, 'index.html')
        
        harvested_river = os.path.join(CACHE_DIR, lang, 'river.html')
        river_data = extract_meta_and_headings(harvested_river)
        
        soup_river = BeautifulSoup(en_river_html, 'html.parser')
        
        # Set HTML lang
        html_river = soup_river.find('html')
        if html_river: html_river['lang'] = lang

        # Update canonical
        can = soup_river.find('link', {'rel': 'canonical'})
        if can:
            can['href'] = f"https://www.budapestadventures.com/{lang}/{river_slug}"
            
        # Update meta & title
        if river_data and river_data['title']:
            if soup_river.title:
                soup_river.title.string = river_data['title']
        if river_data and river_data['description']:
            m = soup_river.find('meta', {'name': 'description'})
            if m:
                m['content'] = river_data['description']
        if river_data and river_data['h1']:
            h1 = soup_river.find('h1')
            if h1:
                h1.string = river_data['h1']
                
        # Localize CTAs, Buy Cards, Pseudo-elements, Breakdown, Proof Chips, and Floating Bar
        localize_guide_page_ui(soup_river, lang, 'river', 10)
                
        # Localize nav & footer
        localize_nav_and_footer_multilingual(soup_river, lang, slugs)
        with open(river_out, 'w', encoding='utf-8') as f:
            f.write(str(soup_river))
        compiled_count += 1
        
        # 2. COMPILE DINNER GUIDE
        dinner_dir = os.path.join(lang_dir, dinner_slug)
        os.makedirs(dinner_dir, exist_ok=True)
        dinner_out = os.path.join(dinner_dir, 'index.html')
        
        harvested_dinner = os.path.join(CACHE_DIR, lang, 'dinner.html')
        dinner_data = extract_meta_and_headings(harvested_dinner)
        
        soup_dinner = BeautifulSoup(en_dinner_html, 'html.parser')
        
        # Set HTML lang
        html_dinner = soup_dinner.find('html')
        if html_dinner: html_dinner['lang'] = lang

        can_dinner = soup_dinner.find('link', {'rel': 'canonical'})
        if can_dinner:
            can_dinner['href'] = f"https://www.budapestadventures.com/{lang}/{dinner_slug}"
            
        if dinner_data and dinner_data['title']:
            if soup_dinner.title:
                soup_dinner.title.string = dinner_data['title']
        if dinner_data and dinner_data['description']:
            m = soup_dinner.find('meta', {'name': 'description'})
            if m:
                m['content'] = dinner_data['description']
        if dinner_data and dinner_data['h1']:
            h1 = soup_dinner.find('h1')
            if h1:
                h1.string = dinner_data['h1']
                
        # Localize CTAs, Buy Cards, Pseudo-elements, Breakdown, Proof Chips, and Floating Bar
        localize_guide_page_ui(soup_dinner, lang, 'dinner', 7)
                
        # Localize nav & footer
        localize_nav_and_footer_multilingual(soup_dinner, lang, slugs)
        with open(dinner_out, 'w', encoding='utf-8') as f:
            f.write(str(soup_dinner))
        compiled_count += 1
        
        # 3. COMPILE LOCALIZED HOMEPAGE
        home_out = os.path.join(lang_dir, 'index.html')
        harvested_home = os.path.join(CACHE_DIR, lang, 'home.html')
        home_data = extract_meta_and_headings(harvested_home)
        
        soup_home = BeautifulSoup(en_home_html, 'html.parser')
        
        # Set HTML lang
        html_home = soup_home.find('html')
        if html_home: html_home['lang'] = lang

        can_home = soup_home.find('link', {'rel': 'canonical'})
        if can_home:
            can_home['href'] = f"https://www.budapestadventures.com/{lang}/"
            
        if home_data and home_data['title']:
            if soup_home.title:
                soup_home.title.string = home_data['title']
        if home_data and home_data['description']:
            m = soup_home.find('meta', {'name': 'description'})
            if m:
                m['content'] = home_data['description']
                
        # Update cards links to point to localized slugs
        for a in soup_home.find_all('a', href=True):
            if a['href'] in ['/best-budapest-river-cruises', '/budapest-river-cruises']:
                a['href'] = f"/{lang}/{river_slug}"
            elif a['href'] in ['/best-dinner-cruises-budapest', '/budapest-dinner-cruises']:
                a['href'] = f"/{lang}/{dinner_slug}"

        # Localize Author Box
        localize_author_box(soup_home, lang)
                
        # Localize nav & footer
        localize_nav_and_footer_multilingual(soup_home, lang, slugs)
        with open(home_out, 'w', encoding='utf-8') as f:
            f.write(str(soup_home))
        compiled_count += 1
        
        print(f"✓ [{lang.upper()}] Compiled home, river ({river_slug}), and dinner ({dinner_slug})")

    print(f"\nCompilation Complete: {compiled_count} static pages compiled across {len(LANGS)} languages.")
    try:
        from scripts.inject_language_switcher import main as inject_main
        print("\nInjecting canonical language switcher across all compiled pages...")
        inject_main()
    except Exception as e:
        print(f"Warning: could not inject language switcher: {e}")


if __name__ == '__main__':
    compile_pages()
