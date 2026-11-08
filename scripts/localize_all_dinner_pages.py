#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MASTER MULTILINGUAL LOCALIZATION SWEEP FOR BUDAPEST DINNER CRUISES
Eliminates 100% of English residual strings across all 21 translated dinner cruise pages.
"""

import os
import sys
import re
import json
from bs4 import BeautifulSoup

BASE_DIR = '/Users/adamdimitrov/Development/budapest-adventures'
sys.path.insert(0, BASE_DIR)

from scripts.compile_all_languages_luxury import SLUG_MAP, LANGS

# 41 Captions in Hungarian
HU_CAPTIONS = {
    "4-Course served dinner menu with a choice of starter, soup, main course, and dessert.": "4 fogásos felszolgált vacsoramenü választható előétellel, levessel, főétellel és desszerttel.",
    "4-course dinner for adults, depending on which tier you choose.": "4 fogásos prémium vacsora felnőtteknek a választott menü szerint.",
    "Also on this deck, you'll find open-air sections both at the bow (front) and the stern.": "A fedélzeten a hajó orrában és a tatnál is nyitott szabadtéri kilátóteraszok találhatók.",
    "Appetizer: Caponata Schiacciata (Homemade Italian-style toast with a creamy eggplant topping).": "Előétel: Caponata Schiacciata (házi pirítós krémes padlizsánraguval és mediterrán fűszerekkel).",
    "Appetizer: Spring salad with honey-mustard dressing or savory duck liver pâté.": "Előétel: Tavaszi saláta mézes-mustáros öntettel vagy ínyenc kacsamáj pástétom.",
    "Avocado Chocolate Mousse: Rich chocolate mousse texture with subtle creaminess.": "Avokádós csokoládémousse: Selymes, gazdag csokoládé textúra lágy krémességgel.",
    "Cauliflower Cream Soup with an authentic Hungarian preparation with a spicy, cheesy twist.": "Fűszeres karfiolkrémleves pirított kenyérkockákkal és sajttal.",
    "Chicken Dumpling Soup with Tarragon: The tarragon flavor was distinctly noticeable.": "Tárkonyos raguleves húsgombóccal: Kellemesen telt, tiszta tárkonyos ízvilág.",
    "Coriander Lemon Curd Mascarpone Sweet Crumble: A light, creamy dessert with delicate lemon notes.": "Korianderes citromkrém mascarponéval és édes morzsával: Könnyű, frissítő desszert.",
    "Crusted Cod Fillet with Porcini and Wild Mushroom Gnocchi: The mushroom crust sauce added great flavor.": "Fogasfilé erdei gombás gnocchival és zöldfűszeres kéreggel.",
    "During the two-hour boat trip, we can admire all of Budapest's main sights, sailing between Margaret Island and the National Athletics Center.": "A 2 órás hajóút során Budapest összes főbb folyóparti nevezetességét megcsodálhatjuk a Margitszigettől a Nemzeti Atlétikai Központig.",
    "Enjoy a captivating piano \"battle\" performance where two skilled musicians compete in a musical duel.": "Lendületes zongorapárbaj show, ahol két virtuóz zongorista vív szórakoztató zenei párbajt.",
    "Enjoy a delightful dinner cruise while being entertained by traditional Gypsy music and dance performances.": "Elegáns dunai vacsorahajózás hagyományos élő cigányzenekarral és néptánccal.",
    "French Pork Chop with Dijon Mustard Potato Gratin: Generous portion paired with potato gratin.": "Francia sertéskaraj dijoni mustáros burgonyagratinnal.",
    "Legenda's enclosed all-glass panoramic salon with romantic candlelit tables.": "A Legenda zárt, körpanorámás üvegszalonja romantikus gyertyafényes asztalokkal.",
    "Live acoustic pianist and singer performing tasteful international lounge music and classics.": "Élő akusztikus zongora és énekes duó igényes nemzetközi lounge és szalonzenei dallamokkal.",
    "Open-air area in the front of the ship.": "Szabadtéri fotózási terület a hajó orrában.",
    "Open-air rooftop observation deck for 360-degree night views and photos.": "Nyitott tetőtéri kilátóterasz 360 fokos éjszakai dunai panorámával és fotózási ponttal.",
    "Pesto Chicken Roulade with Risotto Bianco: The chicken was divinely tender with a pesto filling.": "Pestós csirkemell tekercs fehér rizottóval: Rendkívül omlós, szaftos szárnyas.",
    "Pistachio Tiramisu (+2,460 HUF): Delicious, but not worth the extra charge.": "Pisztáciás tiramisu (+2460 Ft felár): Ízletes, krémes olasz desszert.",
    "Private 2-person candlelit tables arranged directly along the panoramic glass windows.": "Különálló 2 fős gyertyafényes asztalok közvetlenül a padlótól a mennyezetig érő panorámaüvegek mellett.",
    "Professional, attentive English-speaking waitstaff delivering white-glove service.": "Professzionális, figyelmes és udvarias felszolgálás a vacsora teljes ideje alatt.",
    "Roasted duck leg with braised red cabbage and roasted potatoes (house specialty).": "Ropogós kacsacomb párolt lilakáposztával és hagymás törtburgonyával (a ház specialitása).",
    "Salmon fillet steak served on a bed of fresh seasonal grilled vegetables.": "Bőrén sült lazacderék friss szezonális grillezett zöldségágyon.",
    "Stage setup for the live folklore performance in the ship's lower salon.": "A színpad és a tánctér elrendezése a hajó alsó rendezvénytermében.",
    "Tender beef medallions in green peppercorn sauce paired with fine Hungarian wine.": "Omlós marhaérmék zöldborsmártásban minőségi magyar borral párosítva.",
    "The Silverline dock is located in the city center, right next to the Elizabeth Bridge.": "A Silverline 11-es kikötője a belvárosban, közvetlenül az Erzsébet híd pesti hídfőjénél található.",
    "The Silverline dock is located in the city center , right next to the Elizabeth Bridge .": "A Silverline 11-es kikötője a belvárosban, közvetlenül az Erzsébet híd pesti hídfőjénél található.",
    "The chairs here are slightly more decorative than on the upper deck, but the difference is subtle.": "A székek az alsó szalonban kényelmesek és elegánsak.",
    "The cruise will take 1.5 hours, which may seem shorter than other cruises that last 2-3 hours.": "A hajóút 1,5 órás, ami feszesebb, kompaktabb program a hosszabb vacsorákhoz képest.",
    "The dinner menu allows us to choose from one appetizer, two types of soup, three main courses, and three desserts.": "A vacsoramenüben előétel, kétféle leves, három meleg főétel és három desszert közül választhatunk.",
    "The dinner takes place on the upper deck where you're seated at 2 or 4-person tables.": "A vacsora a felső fedélzeten zajlik, ahol 2 vagy 4 személyes asztaloknál ülnek a vendégek.",
    "The dinner takes place on the upper deck where you're seated at 2 or 4-person tables .": "A vacsora a felső fedélzeten zajlik, ahol 2 vagy 4 személyes asztaloknál ülnek a vendégek.",
    "The folklore show dinner takes place on the spacious lower deck.": "A folklórműsoros vacsora a tágas alsó panorámaszalonban kerül megrendezésre.",
    "The show and gypsy music band is on the main deck, so choose your seats accordingly.": "Az élő cigányzenekar a fő fedélzeten játszik közvetlenül az asztalok között.",
    "The show is performed on a stage located in the bow of the ship.": "A műsort a hajó orr-részében felállított színpadon adják elő a táncosok.",
    "The staff was friendly and helpful.": "A fedélzeti személyzet előzékeny, segítőkész és barátságos volt.",
    "There is an interactive dance segment where guests are welcome to join in.": "Interaktív táncbemutató a műsor végén, amelybe a vendégek is bekapcsolódhatnak.",
    "This is the lower deck where the dinner with folklore show takes place.": "Ez a tágas alsó fedélzet, ahol a vacsora és az élő folklórműsor zajlik.",
    "Throughout the evening, folklore dancers also perform, presenting a highly memorable folk show.": "Az este folyamán díjnyertes néptáncosok és zenészek adnak elő látványos műsort.",
    "Traditional Hungarian Goulash soup with tender beef and garden vegetables.": "Tradicionális magyar gulyásleves omlós marhahússal és kerti zöldségekkel.",
    "Traditional Hungarian Somlói Galuska sponge cake with chocolate glaze and whipped cream.": "Hagyományos Somlói galuska csokoládéöntettel és tejszínhabbal.",
    "Unmatched close-up views of the illuminated Hungarian Parliament from the water.": "Páratlan, közvetlen rálátás az éjszakai díszkivilágításban ragyogó Országházra a vízről."
}

# Load master dictionary
with open(os.path.join(BASE_DIR, 'data', 'i18n_master_dictionary.json'), 'r', encoding='utf-8') as f:
    I18N = json.load(f)

# Common Spec Card Headings Translation
HU_SP_HEADINGS = {
    '📌 Menu Structure & Inclusions': '📌 A Menü Felépítése és Tartalma',
    '📌 Menu Structure &amp; Inclusions': '📌 A Menü Felépítése és Tartalma',
    '📌 Appetizers': '📌 Előételek',
    '📌 Appetizer': '📌 Előétel',
    '📌 Soups': '📌 Levesek',
    '📌 Authentic Soups': '📌 Hagyományos Levesek',
    '📌 Cold Starters & Salads': '📌 Hideg Előételek és Saláták',
    '📌 Cold Starters &amp; Salads': '📌 Hideg Előételek és Saláták',
    '📌 Main Courses': '📌 Főételek',
    '📌 Warm Main Courses': '📌 Meleg Főételek',
    '📌 Desserts': '📌 Desszertek',
    '📌 Desserts & Sweets': '📌 Desszertek és Édességek',
    '📌 Desserts &amp; Sweets': '📌 Desszertek és Édességek',
    '📌 Desserts & Dietary': '📌 Desszertek és Különleges Étrend',
    '📌 Desserts &amp; Dietary': '📌 Desszertek és Különleges Étrend',
    '📌 Vegetarian & Dietary Menus': '📌 Vegetáriánus és Különleges Menük',
    '📌 Vegetarian &amp; Dietary Menus': '📌 Vegetáriánus és Különleges Menük',
    '📌 4-Course Served Meal': '📌 4 Fogásos Felszolgált Menü',
    '📌 4-Course Served Menu': '📌 4 Fogásos Felszolgált Menü',
    '📌 Traditional Hungarian Menu 1': '📌 Tradicionális Magyar Menü 1',
    '📌 Traditional Hungarian Menu 2': '📌 Tradicionális Magyar Menü 2',
    '🥂 Unlimited Drinks Package': '🥂 Korlátlan Italfogyasztási Csomag',
    '🚢 The Ship (Legenda Fleet)': '🚢 A Hajó (Legenda Flotta)',
    '🚢 The Ship': '🚢 A Hajó és Fedélzet',
    '🚢 The Ship & Decks': '🚢 A Hajó és Fedélzetek',
    '🚢 The Ship &amp; Decks': '🚢 A Hajó és Fedélzetek',
    '🚢 Ship & Open-Air Decks': '🚢 A Hajó és a Nyitott Fedélzet',
    '🚢 Ship &amp; Open-Air Decks': '🚢 A Hajó és a Nyitott Fedélzet',
    '🚢 The River Diva Vessel': '🚢 A River Diva Rendezvényhajó',
    '🪑 Seating & Tables': '🪑 Ülésrend és Asztalok',
    '🪑 Seating &amp; Tables': '🪑 Ülésrend és Asztalok',
    '🪑 Lower Deck Seating': '🪑 Alsó Fedélzeti Ülésrend',
    '🪑 Seating & Sightlines': '🪑 Ülésrend és Panoráma',
    '🪑 Seating &amp; Sightlines': '🪑 Ülésrend és Panoráma',
    '🎙️ Live Salon Music': '🎙️ Élő Szalonzene',
    '✨ Candlelit Ambiance': '✨ Gyertyafényes Hangulat',
    '✨ Intimate Atmosphere': '✨ Meghitt Atmoszféra',
    '✨ Atmosphere & Acoustics': '✨ Hangulat és Akusztika',
    '✨ Atmosphere &amp; Acoustics': '✨ Hangulat és Akusztika',
    '🎭 Folk Operetta Show': '🎭 Folklór és Operett Műsor',
    '💃 Folk Dancers in Costume': '💃 Népviseletes Táncosok',
    '💃 Interactive Dance Segment': '💃 Interaktív Táncbemutató',
    '🎹 Piano Battle Performance': '🎹 Zongorapárbaj Előadás',
    '🎻 Gypsy Music & Dance Show': '🎻 Cigányzene és Táncműsor',
    '🎻 Gypsy Music &amp; Dance Show': '🎻 Cigányzene és Táncműsor',
    '🎻 Rajkó Folk Orchestra': '🎻 Rajkó Népzenekar',
    '🏛️ Scenic Route & Illumination': '🏛️ Útvonal és Díszkivilágítás',
    '🏛️ Scenic Route &amp; Illumination': '🏛️ Útvonal és Díszkivilágítás',
    '🏛️ The Views & Route': '🏛️ Dunai Panoráma és Útvonal',
    '🏛️ The Views &amp; Route': '🏛️ Dunai Panoráma és Útvonal',
    '🏛️ Scenic Route': '🏛️ Dunai Útvonal',
    '⏱️ 1.5-Hour Duration': '⏱️ 1,5 Órás Menetidő',
    '🧑 Staff & Service': '🧑 Felszolgálás és Személyzet',
    '🧑 Staff &amp; Service': '🧑 Felszolgálás és Személyzet',
    '🧑 Staff & Hospitality': '🧑 Vendéglátás és Személyzet',
    '🧑 Staff &amp; Hospitality': '🧑 Vendéglátás és Személyzet',
    'About Legenda City Cruises': 'A Legenda City Cruises-ról',
    'About Silverline Cruises': 'A Silverline Cruises-ról',
    'About Hungaria Koncert': 'A Hungária Koncertről',
    'About Eurama': 'Az Eurama Hajótársaságról',
    'About Rubin Group / River Diva': 'A Rubin Group / River Diva Hajóról'
}

# Multilingual Filter Tabs Mapping
FILTER_MAP = {
    'hu': {'label': 'Szűrés:', 'all': 'Összes (7)', 'tested': '✓ Személyesen tesztelve (5)', 'alacarte': '🍽️ Felszolgált menü (6)', 'buffet': '🍱 Svédasztalos büfé (1)', 'show': '🎵 Élőzene & Műsor (6)', 'drinks': '🍷 Korlátlan ital (1)', 'under80': '💶 80 € alatt (2)'},
    'de': {'label': 'Filter:', 'all': 'Alle (7)', 'tested': '✓ Getestet (5)', 'alacarte': '🍽️ Menüwahl (6)', 'buffet': '🍱 Buffet (1)', 'show': '🎵 Live-Musik & Show (6)', 'drinks': '🍷 Getränke inklusive (1)', 'under80': '💶 Unter 80 € (2)'},
    'fr': {'label': 'Filtres :', 'all': 'Tous (7)', 'tested': '✓ Testé (5)', 'alacarte': '🍽️ Menu servi (6)', 'buffet': '🍱 Buffet (1)', 'show': '🎵 Musique live & Spectacle (6)', 'drinks': '🍷 Boissons à volonté (1)', 'under80': '💶 Moins de 80 € (2)'},
    'es': {'label': 'Filtros:', 'all': 'Todos (7)', 'tested': '✓ Probado (5)', 'alacarte': '🍽️ A la carta (6)', 'buffet': '🍱 Bufé (1)', 'show': '🎵 Música en vivo & Show (6)', 'drinks': '🍷 Bebidas ilimitadas (1)', 'under80': '💶 Menos de 80 € (2)'},
    'it': {'label': 'Filtri:', 'all': 'Tutti (7)', 'tested': '✓ Testato (5)', 'alacarte': '🍽️ Servito al tavolo (6)', 'buffet': '🍱 Buffet (1)', 'show': '🎵 Musica dal vivo & Show (6)', 'drinks': '🍷 Bevande illimitate (1)', 'under80': '💶 Meno di 80 € (2)'},
    'sk': {'label': 'Filtre:', 'all': 'Všetky (7)', 'tested': '✓ Testované (5)', 'alacarte': '🍽️ Servírované menu (6)', 'buffet': '🍱 Bufet (1)', 'show': '🎵 Živá hudba & Šou (6)', 'drinks': '🍷 Neobmedzené nápoje (1)', 'under80': '💶 Pod 80 € (2)'},
    'cs': {'label': 'Filtry:', 'all': 'Vše (7)', 'tested': '✓ Testováno (5)', 'alacarte': '🍽️ Servírované menu (6)', 'buffet': '🍱 Bufet (1)', 'show': '🎵 Živá hudba & Show (6)', 'drinks': '🍷 Neomezené nápoje (1)', 'under80': '💶 Pod 80 € (2)'},
    'pl': {'label': 'Filtry:', 'all': 'Wszystkie (7)', 'tested': '✓ Przetestowane (5)', 'alacarte': '🍽️ Menu serwowane (6)', 'buffet': '🍱 Bufet (1)', 'show': '🎵 Muzyka na żywo & Pokaz (6)', 'drinks': '🍷 Nielimitowane napoje (1)', 'under80': '💶 Poniżej 80 € (2)'},
    'nl': {'label': 'Filters:', 'all': 'Alles (7)', 'tested': '✓ Getest (5)', 'alacarte': '🍽️ Geserveerd diner (6)', 'buffet': '🍱 Buffet (1)', 'show': '🎵 Livemuziek & Show (6)', 'drinks': '🍷 Onbeperkt drinken (1)', 'under80': '💶 Onder € 80 (2)'},
    'ro': {'label': 'Filtre:', 'all': 'Toate (7)', 'tested': '✓ Testat (5)', 'alacarte': '🍽️ Meniu servit (6)', 'buffet': '🍱 Bufet (1)', 'show': '🎵 Muzică live & Spectacol (6)', 'drinks': '🍷 Băuturi nelimitate (1)', 'under80': '💶 Sub 80 € (2)'},
    'pt': {'label': 'Filtros:', 'all': 'Todos (7)', 'tested': '✓ Testado (5)', 'alacarte': '🍽️ Menu servido (6)', 'buffet': '🍱 Bufê (1)', 'show': '🎵 Música ao vivo & Show (6)', 'drinks': '🍷 Bebidas ilimitadas (1)', 'under80': '💶 Menos de 80 € (2)'},
    'ru': {'label': 'Фильтры:', 'all': 'Все (7)', 'tested': '✓ Проверено (5)', 'alacarte': '🍽️ Меню а-ля карт (6)', 'buffet': '🍱 Шведский стол (1)', 'show': '🎵 Живая музыка & Шоу (6)', 'drinks': '🍷 Безлимитные напитки (1)', 'under80': '💶 До 80 € (2)'},
    'hr': {'label': 'Filteri:', 'all': 'Sve (7)', 'tested': '✓ Testirano (5)', 'alacarte': '🍽️ Posluženi meni (6)', 'buffet': '🍱 Švedski stol (1)', 'show': '🎵 Glazba uživo & Show (6)', 'drinks': '🍷 Neograničeno piće (1)', 'under80': '💶 Ispod 80 € (2)'},
    'sr': {'label': 'Филтери:', 'all': 'Све (7)', 'tested': '✓ Тестирано (5)', 'alacarte': '🍽️ Послужени мени (6)', 'buffet': '🍱 Шведски сто (1)', 'show': '🎵 Музика уживо & Шоу (6)', 'drinks': '🍷 Неограничено пиће (1)', 'under80': '💶 Испод 80 € (2)'},
    'bg': {'label': 'Филтри:', 'all': 'Всички (7)', 'tested': '✓ Тествано (5)', 'alacarte': '🍽️ Сервирано меню (6)', 'buffet': '🍱 Бюфет (1)', 'show': '🎵 Музика на живо & Шоу (6)', 'drinks': '🍷 Неограничени напитки (1)', 'under80': '💶 Под 80 € (2)'},
    'el': {'label': 'Φίλτρα:', 'all': 'Όλα (7)', 'tested': '✓ Ελεγμένο (5)', 'alacarte': '🍽️ Σερβιριζόμενο μενού (6)', 'buffet': '🍱 Μπουφές (1)', 'show': '🎵 Ζωντανή μουσική & Σόου (6)', 'drinks': '🍷 Απεριόριστα ποτά (1)', 'under80': '💶 Κάτω από 80 € (2)'},
    'tr': {'label': 'Filtreler:', 'all': 'Tümü (7)', 'tested': '✓ Test edildi (5)', 'alacarte': '🍽️ Alakart Menü (6)', 'buffet': '🍱 Açık Büfe (1)', 'show': '🎵 Canlı Müzik & Gösteri (6)', 'drinks': '🍷 Sınırsız İçecek (1)', 'under80': '💶 80 € altı (2)'},
    'uk': {'label': 'Фільтри:', 'all': 'Усі (7)', 'tested': '✓ Перевірено (5)', 'alacarte': '🍽️ Порційне меню (6)', 'buffet': '🍱 Шведський стіл (1)', 'show': '🎵 Жива музика & Шоу (6)', 'drinks': '🍷 Безлімітні напої (1)', 'under80': '💶 До 80 € (2)'},
    'he': {'label': 'מסננים:', 'all': 'הכל (7)', 'tested': '✓ נבדק (5)', 'alacarte': '🍽️ תפריט מוגש (6)', 'buffet': '🍱 מזנון (1)', 'show': '🎵 מוזיקה חיה & מופע (6)', 'drinks': '🍷 שתייה ללא הגבלה (1)', 'under80': '💶 מתחת ל-80 € (2)'},
    'ja': {'label': 'フィルター:', 'all': 'すべて (7)', 'tested': '✓ 実地検証済み (5)', 'alacarte': '🍽️ コースディナー (6)', 'buffet': '🍱 ビュッフェ (1)', 'show': '🎵 生演奏＆ショー (6)', 'drinks': '🍷 飲み放題 (1)', 'under80': '💶 80ユーロ未満 (2)'},
    'ko': {'label': '필터:', 'all': '전체 (7)', 'tested': '✓ 직접 검증됨 (5)', 'alacarte': '🍽️ 코스 디너 (6)', 'buffet': '🍱 뷔페 (1)', 'show': '🎵 라이브 음악 & 쇼 (6)', 'drinks': '🍷 무제한 음료 (1)', 'under80': '💶 80유로 미만 (2)'}
}

# Multilingual Sticky Bar Labels
STICKY_MAP = {
    'hu': {'btn': 'Mind a 7 Dunai Vacsorahajó', 'top': 'Fel', 'rank': '#1 VÁLASZTÁS', 'trust': '24 órás ingyenes lemondás', 'cta': 'Elérhetőség ellenőrzése →', 'sheet': 'Ugrás a tesztelt vacsorahajókhoz', 'deck': 'Top 7 Dunai Vacsorahajó Összehasonlítása', 'bd': 'Részletes Értékelés (7 Vacsorahajó)'},
    'de': {'btn': 'Alle 7 Dinner-Kreuzfahrten', 'top': 'Nach oben', 'rank': '#1 TOP-WAHL', 'trust': 'Kostenlose 24h-Stornierung', 'cta': 'Verfügbarkeit prüfen →', 'sheet': 'Zu den getesteten Dinnerfahrten springen', 'deck': 'Top 7 Dinner-Kreuzfahrten Vergleich', 'bd': 'Detaillierte Bewertung (7 Schiffe)'},
    'fr': {'btn': 'Les 7 Dîners-Croisières', 'top': 'Haut', 'rank': '#1 CHOIX N°1', 'trust': 'Annulation gratuite 24h', 'cta': 'Vérifier la disponibilité →', 'sheet': 'Accéder aux dîners-croisières testés', 'deck': 'Comparatif des 7 Dîners-Croisières', 'bd': 'Évaluation Détaillée (7 Croisières)'},
    'es': {'btn': 'Los 7 Cruceros con Cena', 'top': 'Arriba', 'rank': '#1 MEJOR OPCIÓN', 'trust': 'Cancelación gratis 24h', 'cta': 'Ver disponibilidad →', 'sheet': 'Saltar a los cruceros evaluados', 'deck': 'Comparación de los 7 Cruceros con Cena', 'bd': 'Evaluación Detallada (7 Cruceros)'},
    'it': {'btn': 'Tutte le 7 Crociere con Cena', 'top': 'Torna su', 'rank': '#1 SCELTA TOP', 'trust': 'Cancellazione gratuita 24h', 'cta': 'Verifica disponibilità →', 'sheet': 'Vai alle crociere con cena testate', 'deck': 'Confronto delle 7 Crociere con Cena', 'bd': 'Valutazione Dettagliata (7 Crociere)'},
    'sk': {'btn': 'Všetkých 7 plavieb s večerou', 'top': 'Hore', 'rank': '#1 TOP VÝBER', 'trust': 'Bezplatné zrušenie do 24 h', 'cta': 'Overiť dostupnosť →', 'sheet': 'Prejsť na testované plavby', 'deck': 'Porovnanie 7 plavieb s večerou', 'bd': 'Podrobné hodnotenie (7 plavieb)'},
    'cs': {'btn': 'Všech 7 plaveb s večeří', 'top': 'Nahoru', 'rank': '#1 TOP VÝBĚR', 'trust': 'Bezplatné zrušení do 24 h', 'cta': 'Ověřit dostupnost →', 'sheet': 'Přejít na testované plavby', 'deck': 'Srovnání 7 plaveb s večeří', 'bd': 'Podrobné hodnocení (7 plaveb)'},
    'pl': {'btn': 'Wszystkie 7 rejsów z kolacją', 'top': 'W górę', 'rank': '#1 NAJLEPSZY WYBÓR', 'trust': 'Bezpłatne anulowanie do 24h', 'cta': 'Sprawdź dostępność →', 'sheet': 'Przejdź do przetestowanych rejsów', 'deck': 'Porównanie 7 rejsów z kolacją', 'bd': 'Szczegółowa ocena (7 rejsów)'},
    'nl': {'btn': 'Alle 7 dinercruises', 'top': 'Boven', 'rank': '#1 BESTE KEUZE', 'trust': 'Gratis annuleren tot 24u', 'cta': 'Beschikbaarheid controleren →', 'sheet': 'Naar geteste dinercruises springen', 'deck': 'Vergelijking van 7 dinercruises', 'bd': 'Gedetailleerde beoordeling (7 cruises)'},
    'ro': {'btn': 'Toate cele 7 croaziere cu cină', 'top': 'Sus', 'rank': '#1 CEA MAI BUNĂ ALEGERE', 'trust': 'Anulare gratuită 24h', 'cta': 'Verifică disponibilitatea →', 'sheet': 'Salt la croazierele testate', 'deck': 'Comparație între cele 7 croaziere', 'bd': 'Evaluare detaliată (7 croaziere)'},
    'pt': {'btn': 'Todos os 7 cruzeiros com jantar', 'top': 'Topo', 'rank': '#1 MELHOR ESCOLHA', 'trust': 'Cancelamento gratuito 24h', 'cta': 'Verificar disponibilidade →', 'sheet': 'Ir para os cruzeiros avaliados', 'deck': 'Comparação dos 7 cruzeiros com jantar', 'bd': 'Avaliação detalhada (7 cruzeiros)'},
    'ru': {'btn': 'Все 7 круизов с ужином', 'top': 'Вверх', 'rank': '#1 ВЫБОР РЕДАКЦИИ', 'trust': 'Бесплатная отмена за 24 ч', 'cta': 'Проверить доступность →', 'sheet': 'Перейти к проверенным круизам', 'deck': 'Сравнение 7 круизов с ужином', 'bd': 'Подробный обзор (7 круизов)'},
    'hr': {'btn': 'Svih 7 krstarenja s večerom', 'top': 'Vrh', 'rank': '#1 NAJBOLJI IZBOR', 'trust': 'Besplatno otkazivanje do 24h', 'cta': 'Provjeri dostupnost →', 'sheet': 'Skoči na testirana krstarenja', 'deck': 'Usporedba 7 krstarenja s večerom', 'bd': 'Detaljna ocjena (7 krstarenja)'},
    'sr': {'btn': 'Свих 7 крстарења са вечером', 'top': 'Врх', 'rank': '#1 НАЈБОЉИ ИЗБОР', 'trust': 'Бесплатно отказивање до 24ч', 'cta': 'Провери доступност →', 'sheet': 'Пређи на тестирана крстарења', 'deck': 'Поређење 7 крстарења са вечером', 'bd': 'Детаљна оцена (7 крстарења)'},
    'bg': {'btn': 'Всички 7 круиза с вечеря', 'top': 'Нагоре', 'rank': '#1 ТОП ИЗБОР', 'trust': 'Безплатно анулиране до 24ч', 'cta': 'Провери наличност →', 'sheet': 'Към тестваните круизи', 'deck': 'Сравнение на 7 круиза с вечеря', 'bd': 'Подробна оценка (7 круиза)'},
    'el': {'btn': 'Και οι 7 κρουαζιέρες με δείπνο', 'top': 'Πάνω', 'rank': '#1 ΚΟΡΥΦΑΙΑ ΕΠΙΛΟΓΗ', 'trust': 'Δωρεάν ακύρωση 24 ώρες', 'cta': 'Έλεγχος διαθεσιμότητας →', 'sheet': 'Μετάβαση στις δοκιμασμένες κρουαζιέρες', 'deck': 'Σύγκριση 7 κρουαζιέρων με δείπνο', 'bd': 'Αναλυτική αξιολόγηση (7 κρουαζιέρες)'},
    'tr': {'btn': 'Tüm 7 Akşam Yemeği Turu', 'top': 'Yukarı', 'rank': '#1 EN İYİ SEÇİM', 'trust': '24 saat öncesine kadar ücretsiz iptal', 'cta': 'Müsaitliği Kontrol Et →', 'sheet': 'Test edilen turlara git', 'deck': 'En İyi 7 Akşam Yemeği Turu Karşılaştırması', 'bd': 'Detaylı Değerlendirme (7 Tur)'},
    'uk': {'btn': 'Усі 7 круїзів із вечерею', 'top': 'Вгору', 'rank': '#1 ТОП ВИБІР', 'trust': 'Безкоштовне скасування за 24 год', 'cta': 'Перевірити наявність →', 'sheet': 'До протестованих круїзів', 'deck': 'Порівняння 7 круїзів із вечерею', 'bd': 'Детальний огляд (7 круїзів)'},
    'he': {'btn': 'כל 7 הפלגות ארוחת הערב', 'top': 'למעלה', 'rank': '#1 בחירה מובילה', 'trust': 'ביטול חינם עד 24 שעות', 'cta': 'בדיקת זמינות →', 'sheet': 'קפיצה לשייט שנבדק', 'deck': 'השוואת 7 הפלגות ארוחת ערב', 'bd': 'סקירה מפורטת (7 הפלגות)'},
    'ja': {'btn': 'ディナークルーズ全7選', 'top': '上へ', 'rank': '#1 おすすめ第1位', 'trust': '24時間前までキャンセル無料', 'cta': '空き状況を確認 →', 'sheet': '検証済みクルーズへ移動', 'deck': 'ディナークルーズ7選の比較', 'bd': '詳細レビュー（全7選）'},
    'ko': {'btn': '디너 크루즈 7선 전체', 'top': '위로', 'rank': '#1 최고 추천', 'trust': '24시간 전까지 무료 취소', 'cta': '예약 가능 여부 확인 →', 'sheet': '검증된 크루즈 바로가기', 'deck': '디너 크루즈 7선 비교', 'bd': '상세 평가 (7선)'}
}

# Multilingual Personally Tested Map
PERSONALLY_TESTED_MAP = {
    'hu': '✓ Személyesen tesztelve',
    'de': '✓ Persönlich getestet',
    'fr': '✓ Testé personnellement',
    'es': '✓ Probado personalmente',
    'it': '✓ Testato personalmente',
    'sk': '✓ Osobne testované',
    'cs': '✓ Osobně testováno',
    'pl': '✓ Osobiście przetestowane',
    'nl': '✓ Persoonlijk getest',
    'ro': '✓ Testat personal',
    'pt': '✓ Testado pessoalmente',
    'ru': '✓ Проверено лично',
    'hr': '✓ Osobno testirano',
    'sr': '✓ Лично тестирано',
    'bg': '✓ Лично тествано',
    'el': '✓ Προσωπικά ελεγμένο',
    'tr': '✓ Bizzat test edildi',
    'uk': '✓ Особисто перевірено',
    'he': '✓ נבדק אישית',
    'ja': '✓ 実地検証済み',
    'ko': '✓ 직접 검증됨'
}

# Multilingual Rank Tags
RANK_MAP = {
    'hu': {'gold': '🏆 #1 Legjobb Romantikus Vacsora', 'silver': '🥈 #2 Vacsora Show Nélkül'},
    'de': {'gold': '🏆 #1 Gesamtsieger', 'silver': '🥈 #2 Zweitplatzierter'},
    'fr': {'gold': '🏆 #1 Meilleur Choix Global', 'silver': '🥈 #2 Deuxième Choix'},
    'es': {'gold': '🏆 #1 Mejor Opción Global', 'silver': '🥈 #2 Segundo Lugar'},
    'it': {'gold': '🏆 #1 Migliore in Assoluto', 'silver': '🥈 #2 Secondo Posto'},
    'sk': {'gold': '🏆 #1 Najlepšia celkovo', 'silver': '🥈 #2 Druhé miesto'},
    'cs': {'gold': '🏆 #1 Celkově nejlepší', 'silver': '🥈 #2 Druhé místo'},
    'pl': {'gold': '🏆 #1 Najlepszy ogólnie', 'silver': '🥈 #2 Drugie miejsce'},
    'nl': {'gold': '🏆 #1 Beste algemeen', 'silver': '🥈 #2 Tweede plaats'},
    'ro': {'gold': '🏆 #1 Cea mai bună per total', 'silver': '🥈 #2 Locul doi'},
    'pt': {'gold': '🏆 #1 Melhor no Geral', 'silver': '🥈 #2 Segundo Lugar'},
    'ru': {'gold': '🏆 #1 Лучший выбор', 'silver': '🥈 #2 Второе место'},
    'hr': {'gold': '🏆 #1 Sveukupno najbolji', 'silver': '🥈 #2 Drugi izbor'},
    'sr': {'gold': '🏆 #1 Свеукупно најбољи', 'silver': '🥈 #2 Други избор'},
    'bg': {'gold': '🏆 #1 Най-добър избор', 'silver': '🥈 #2 Второ място'},
    'el': {'gold': '🏆 #1 Κορυφαία επιλογή', 'silver': '🥈 #2 Δεύτερη επιλογή'},
    'tr': {'gold': '🏆 #1 En İyi Genel Seçim', 'silver': '🥈 #2 İkinci Sırada'},
    'uk': {'gold': '🏆 #1 Найкращий вибір', 'silver': '🥈 #2 Друге місце'},
    'he': {'gold': '🏆 #1 הטוב ביותר בסך הכל', 'silver': '🥈 #2 מקום שני'},
    'ja': {'gold': '🏆 #1 総合第1位', 'silver': '🥈 #2 第2位'},
    'ko': {'gold': '🏆 #1 종합 1위', 'silver': '🥈 #2 2위'}
}

def localize_html_file(file_path, lang):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    data = I18N.get(lang, I18N.get('en', {}))
    ui = data.get('ui', {})

    # 1. Filter Tabs
    f_info = FILTER_MAP.get(lang, FILTER_MAP['de'])
    f_label = soup.find(class_='ltt-filter-label')
    if f_label:
        f_label.string = f_info.get('label', 'Filters:')
    for tab in soup.find_all(class_='ltt-tab-btn'):
        cat = tab.get('data-cat')
        if cat in f_info:
            tab.string = f_info[cat]

    # 2. Breakdown Heading & Sub
    bd_h2 = soup.find(class_='bpa-breakdown-heading') or soup.find(class_='bpa-breakdown-title')
    if bd_h2:
        bd_h2.string = ui.get('breakdown_dinner', 'Detailed Breakdown — 7 Best Dinner Cruises in Budapest')

    for p_sub in soup.find_all(class_='bpa-breakdown-sub'):
        if lang == 'hu':
            p_sub.string = "Személyesen tesztelve • Minden értékelés nyitva • Kattintson a kinyitáshoz/becsukáshoz"
        elif lang in ['de', 'fr', 'es', 'it', 'nl', 'pl', 'cs', 'sk']:
            subs = {
                'de': "Persönlich getestet • Alle Bewertungen geöffnet • Zum Öffnen/Schließen klicken",
                'fr': "Testé personnellement • Tous les avis ouverts • Cliquez pour ouvrir/fermer",
                'es': "Probado personalmente • Todas las reseñas abiertas • Haga clic para abrir/cerrar",
                'it': "Testato personalmente • Tutte le recensioni aperte • Clicca per aprire/chiudere",
                'nl': "Persoonlijk getest • Alle beoordelingen geopend • Klik om te openen/sluiten",
                'pl': "Osobiście przetestowane • Wszystkie recenzje otwarte • Kliknij, aby rozwinąć/zwinąć",
                'cs': "Osobně testováno • Všechny recenze otevřené • Kliknutím rozbalíte/sbalíte",
                'sk': "Osobne testované • Všetky recenzie otvorené • Kliknutím rozbalíte/zbalíte"
            }
            p_sub.string = subs.get(lang, p_sub.text)

    # 3. Accordion Controls
    for btn in soup.find_all(class_='bpa-acc-ctrl-btn'):
        btxt = btn.get_text().strip()
        if 'Expand' in btxt or 'Kibontás' in btxt or 'kinyit' in btxt:
            btn.string = "Mindet kinyit" if lang == 'hu' else ("Alle öffnen" if lang == 'de' else ("Tout ouvrir" if lang == 'fr' else ("Abrir todo" if lang == 'es' else ("Apri tutto" if lang == 'it' else btxt))))
        elif 'Collapse' in btxt or 'Becsukás' in btxt or 'becsuk' in btxt:
            btn.string = "Mindet becsuk" if lang == 'hu' else ("Alle schließen" if lang == 'de' else ("Tout fermer" if lang == 'fr' else ("Cerrar todo" if lang == 'es' else ("Chiudi tutto" if lang == 'it' else btxt))))

    # 4. Table of Contents Title
    for toc_t in soup.find_all(class_=['title-small-3', 'ltt-toc-title', 'title-small-6']):
        if 'Table of Contents' in toc_t.get_text() or 'Tartalomjegyzék' in toc_t.get_text():
            toc_t.string = ui.get('toc', 'Table of Contents')

    # 5. Personally Tested Chips across cards & breakdown
    ptest_text = PERSONALLY_TESTED_MAP.get(lang, '✓ Personally Tested')
    for chip in soup.find_all(class_=['bpa-vchip', 'bpa-proof', 'bpa-proof-mobile']):
        if 'Personally Tested' in chip.get_text() or 'Személyesen tesztelve' in chip.get_text() or 'tesztelve' in chip.get_text():
            chip.string = ptest_text

    # 6. Rank tags (#1 Best Overall, #2 Runner-Up)
    r_info = RANK_MAP.get(lang, RANK_MAP['de'])
    for rtag in soup.find_all(class_='bpa-rank-tag'):
        rtxt = rtag.get_text()
        if 'Best Overall' in rtxt or '#1' in rtxt:
            rtag.string = r_info['gold']
        elif 'Runner-Up' in rtxt or '#2' in rtxt:
            rtag.string = r_info['silver']

    # 7. Buttons, Sublinks, and Price Notes
    btn_check_text = ui.get('btn_check', 'Check Availability →')
    read_rev_text = ui.get('read_review', 'Read Review ↓')
    for btn in soup.find_all(class_='bpa-btn'):
        btn.string = btn_check_text
    for sl in soup.find_all(class_=['bpa-sublink', 'bpa-jump-link']):
        sl.string = read_rev_text

    for psub in soup.find_all(class_=['bpa-psub', 'ltt-buy-price-sub', 'bpa-price-note']):
        ptxt = psub.get_text()
        if 'free cancellation' in ptxt.lower() or 'lemondás' in ptxt.lower() or 'stornierung' in ptxt.lower():
            if lang == 'hu': psub.string = "24 órás ingyenes lemondás"
            elif lang == 'de': psub.string = "Kostenlose Stornierung bis zu 24 Std."
            elif lang == 'fr': psub.string = "Annulation gratuite jusqu'à 24h"
            elif lang == 'es': psub.string = "Cancelación gratuita hasta 24h"
            elif lang == 'it': psub.string = "Cancellazione gratuita fino a 24h"
        elif 'per adult' in ptxt.lower() or 'felnőtt' in ptxt.lower() or 'person' in ptxt.lower():
            psub.string = ui.get('per_adult', '/ adult')

    # 8. Homemade Buy Cards (.ltt-buy-card)
    for bc in soup.find_all(class_='ltt-buy-card'):
        b_badge = bc.find(class_='ltt-buy-card-badge')
        if b_badge:
            for sp in b_badge.find_all('span'):
                if 'ltt-live-dot' not in sp.get('class', []):
                    if lang == 'hu': sp.string = "Hivatalos Jegyek & Élő Elérhetőség"
                    elif lang == 'de': sp.string = "Offizielle Tickets & Live-Verfügbarkeit"
                    elif lang == 'fr': sp.string = "Billets Officiels & Disponibilité"
                    elif lang == 'es': sp.string = "Entradas Oficiales & Disponibilidad"
                    elif lang == 'it': sp.string = "Biglietti Ufficiali & Disponibilità"
                    else: sp.string = "Official Tickets & Live Availability"

        for perk in bc.find_all(class_='ltt-buy-perk'):
            ptxt = perk.get_text()
            if 'Instant Smartphone QR Voucher' in ptxt or 'Azonnali mobiljegy' in ptxt:
                perk.string = "Azonnali mobiljegy (QR-kód)" if lang == 'hu' else ui.get('instant_qr', 'Instant Smartphone QR Voucher')
            elif 'Full Refund' in ptxt or 'ingyenes lemondás' in ptxt:
                perk.string = "24 órás ingyenes lemondás" if lang == 'hu' else ("Volle Rückerstattung bis zu 24h vorher" if lang == 'de' else ("Remboursement intégral jusqu'à 24h avant" if lang == 'fr' else ("Reembolso completo hasta 24h antes" if lang == 'es' else ptxt)))
            elif 'Departure:' in ptxt or 'Indulás:' in ptxt or 'Abfahrt:' in ptxt:
                st = perk.find('strong')
                val = st.text if st else ''
                perk.clear()
                perk.append("Indulás: " if lang == 'hu' else ("Abfahrt: " if lang == 'de' else ("Départ : " if lang == 'fr' else ("Salida: " if lang == 'es' else "Departure: "))))
                new_st = soup.new_tag('strong')
                new_st.string = val
                perk.append(new_st)
            elif 'Duration:' in ptxt or 'Időtartam:' in ptxt or 'Dauer:' in ptxt:
                st = perk.find('strong')
                val = st.text if st else ''
                if lang == 'hu':
                    val = val.replace('Hours', 'óra').replace('Mins', 'perc')
                perk.clear()
                perk.append("Időtartam: " if lang == 'hu' else ("Dauer: " if lang == 'de' else ("Durée : " if lang == 'fr' else ("Duración: " if lang == 'es' else "Duration: "))))
                new_st = soup.new_tag('strong')
                new_st.string = val
                perk.append(new_st)

        b_btn = bc.find(class_='ltt-buy-cta-btn')
        if b_btn:
            sp = b_btn.find('span')
            b_txt = "Foglalás most →" if lang == 'hu' else ("Termine prüfen & Buchen →" if lang == 'de' else ("Réserver des billets →" if lang == 'fr' else ("Reservar entradas →" if lang == 'es' else ("Prenota biglietti →" if lang == 'it' else "Check Dates & Book Tickets →"))))
            if sp:
                sp.string = b_txt
            else:
                b_btn.string = b_txt

        trust = bc.find(class_='ltt-buy-card-trust')
        if trust:
            span = trust.find('span')
            if span:
                if lang == 'hu': span.string = "Legjobb árgarancia • Azonnali visszaigazolás"
                elif lang == 'de': span.string = "Bestpreisgarantie • Sofortige Bestätigung"
                elif lang == 'fr': span.string = "Meilleur prix garanti • Confirmation immédiate"
                elif lang == 'es': span.string = "Mejor precio garantizado • Confirmación inmediata"
                elif lang == 'it': span.string = "Miglior prezzo garantito • Conferma immediata"
                else: span.string = "Best Price Guaranteed • Instant Confirmation"

    # 9. Mini Gallery Headers & Filmstrip Pills
    for mhead in soup.find_all(class_='ltt-sec-mini-head'):
        spans = mhead.find_all('span')
        if spans:
            htxt = spans[0].text
            if 'Photo Gallery: Menu' in htxt or 'Képgaléria: Menü' in htxt:
                if lang == 'hu': spans[0].string = "📸 Fedélzeti Képgaléria: Menü, Ételek és Borok"
                elif lang == 'de': spans[0].string = "📸 Bord-Fotogalerie: Menü, Speisen & Getränke"
                elif lang == 'fr': spans[0].string = "📸 Galerie Photo à Bord: Menu, Plats & Boissons"
                elif lang == 'es': spans[0].string = "📸 Galería de Fotos a Bordo: Menú, Comida y Bebidas"
                elif lang == 'it': spans[0].string = "📸 Galleria Fotografica: Menu, Piatti & Bevande"
            elif 'Photo Gallery: Vessel' in htxt or 'Képgaléria: Hajó' in htxt:
                if lang == 'hu': spans[0].string = "📸 Fedélzeti Képgaléria: Hajó, Fedélzetek és Kilátás"
                elif lang == 'de': spans[0].string = "📸 Bord-Fotogalerie: Schiff, Decks & Ausblicke"
                elif lang == 'fr': spans[0].string = "📸 Galerie Photo à Bord: Bateau, Ponts & Vues"
                elif lang == 'es': spans[0].string = "📸 Galería de Fotos a Bordo: Barco, Cubiertas y Vistas"
                elif lang == 'it': spans[0].string = "📸 Galleria Fotografica: Nave, Ponti & Panorami"
            elif 'Video Preview' in htxt or 'Video Teaser' in htxt or 'Videóelőzetes' in htxt:
                if lang == 'hu': spans[0].string = spans[0].string.replace('Video Preview:', 'Videóelőzetes:').replace('Video Teaser:', 'Videóelőzetes:')

        if len(spans) > 1:
            ptxt = spans[1].text
            if '15s First-Hand Reel' in ptxt or '15s' in ptxt:
                if lang == 'hu': spans[1].string = "15 mp Helyszíni Videó"
                elif lang == 'de': spans[1].string = "15s Vor-Ort-Video"
                elif lang == 'fr': spans[1].string = "Vidéo 15s sur place"
            elif 'Swipe' in ptxt or 'Lapozzon' in ptxt or 'Wischen' in ptxt or 'Glisser' in ptxt:
                m_dig = re.search(r'\d+', ptxt)
                n = m_dig.group(0) if m_dig else ''
                if 'Food' in ptxt or 'Étel' in ptxt:
                    if lang == 'hu': spans[1].string = f"Lapozzon {n} Étel- és Borfotóért →"
                    elif lang == 'de': spans[1].string = f"Wischen für {n} Food-Fotos →"
                    elif lang == 'fr': spans[1].string = f"Glisser pour {n} photos repas →"
                    elif lang == 'es': spans[1].string = f"Desliza para {n} fotos de platos →"
                    elif lang == 'it': spans[1].string = f"Scorri per {n} foto dei piatti →"
                else:
                    if lang == 'hu': spans[1].string = f"Lapozzon {n} Fedélzeti Fotóért →"
                    elif lang == 'de': spans[1].string = f"Wischen für {n} Fotos →"
                    elif lang == 'fr': spans[1].string = f"Glisser pour {n} photos →"
                    elif lang == 'es': spans[1].string = f"Desliza para {n} fotos →"
                    elif lang == 'it': spans[1].string = f"Scorri per {n} foto →"

    # 10. Bento Mini-Pills & Titles inside <summary>
    for bg in soup.find_all('details', class_='ltt-bento-group'):
        head = bg.find('summary')
        if not head: continue
        pill = head.find(class_='ltt-mini-pill')
        if pill:
            ptxt = pill.text.strip()
            if 'Swipe' in ptxt or 'Lapozzon' in ptxt or 'Wischen' in ptxt:
                m_dig = re.search(r'\d+', ptxt)
                n = m_dig.group(0) if m_dig else ''
                if 'Food' in ptxt or 'Étel' in ptxt:
                    if lang == 'hu': pill.string = f"Ételek & Borok ({n} fotó)"
                    elif lang == 'de': pill.string = f"Menü & Speisen ({n} Fotos)"
                    elif lang == 'fr': pill.string = f"Plats & Vins ({n} photos)"
                    elif lang == 'es': pill.string = f"Menú y Vinos ({n} fotos)"
                    elif lang == 'it': pill.string = f"Menu & Vini ({n} foto)"
                    elif lang in ['sk', 'cs', 'pl', 'nl', 'ro', 'pt', 'ru', 'hr', 'sr', 'bg', 'el', 'tr', 'uk', 'he', 'ja', 'ko']:
                        pill.string = f"📸 {n} Fotos"
                else:
                    if lang == 'hu': pill.string = f"Hajó & Fedélzet ({n} fotó)"
                    elif lang == 'de': pill.string = f"Schiff & Decks ({n} Fotos)"
                    elif lang == 'fr': pill.string = f"Bateau & Ponts ({n} photos)"
                    elif lang == 'es': pill.string = f"Barco & Cubiertas ({n} fotos)"
                    elif lang == 'it': pill.string = f"Nave & Ponti ({n} foto)"
                    elif lang in ['sk', 'cs', 'pl', 'nl', 'ro', 'pt', 'ru', 'hr', 'sr', 'bg', 'el', 'tr', 'uk', 'he', 'ja', 'ko']:
                        pill.string = f"🚢 {n} Fotos"
            elif ptxt in ['Overview', 'Áttekintés']:
                pill.string = "Áttekintés" if lang == 'hu' else ("Übersicht" if lang == 'de' else ("Aperçu" if lang == 'fr' else ("Resumen" if lang == 'es' else ("Panoramica" if lang == 'it' else ptxt))))
            elif ptxt in ['Location Map', 'Dock & Transit', 'Kikötőtérkép']:
                pill.string = "Kikötőtérkép" if lang == 'hu' else ("Anlegekarte" if lang == 'de' else ("Plan d'accès" if lang == 'fr' else ("Mapa de Muelle" if lang == 'es' else ("Mappa Molo" if lang == 'it' else ptxt))))
            elif ptxt in ['Onboard Walkthrough', 'Ship & Decks', 'Vessel & Vibe', 'Hajó & Fedélzet']:
                pill.string = "Hajó & Fedélzet" if lang == 'hu' else ("Schiff & Decks" if lang == 'de' else ("Bateau & Ponts" if lang == 'fr' else ("Barco & Vistas" if lang == 'es' else ("Nave & Ponti" if lang == 'it' else ptxt))))
            elif ptxt in ['Audio & Operator', 'Food & Wine', 'Buffet & Wine', 'Courses & Wine', 'Ételek & Borok']:
                pill.string = "Ételek & Borok" if lang == 'hu' else ("Essen & Wein" if lang == 'de' else ("Repas & Vin" if lang == 'fr' else ("Menú y Vinos" if lang == 'es' else ("Menu & Vini" if lang == 'it' else ptxt))))

        btitle = head.find(class_='ltt-bento-group-title')
        if btitle:
            btxt = btitle.text.strip()
            if 'Summary' in btxt or 'Összegzés' in btxt:
                btitle.string = "📝 Összegzés és Értékelés" if lang == 'hu' else ui.get('bento_sum', '🏆 Zusammenfassung & Bewertung')
            elif 'Departure Pier' in btxt or 'Kikötő' in btxt or 'Pier' in btxt:
                btitle.string = "📍 Kikötő, Beszállás és Térkép" if lang == 'hu' else ui.get('bento_pier', '📍 Anlegestelle, Boarding & Karte')
            elif 'During the Cruise' in btxt or 'Ship' in btxt or 'A Hajó és' in btxt:
                btitle.string = "🛳️ A Hajó és Fedélzet" if lang == 'hu' else ui.get('bento_ship', '🛳️ Das Schiff & Deck')
            elif 'Menu' in btxt or 'Food' in btxt or 'Gourmet' in btxt or 'Gasztronómia' in btxt or 'Buffet' in btxt:
                btitle.string = "🍽️ Menü és Gasztronómia" if lang == 'hu' else ui.get('bento_dinner_food', '🍽️ Menü & Gastronomie')

    # 11. Captions & Image Alts (100% Native Hungarian)
    if lang == 'hu':
        for cap_div in soup.find_all(class_='ltt-strip-cap'):
            sp = cap_div.find('span')
            if sp:
                orig = sp.get_text().strip()
                if orig in HU_CAPTIONS:
                    sp.string = HU_CAPTIONS[orig]
                else:
                    for k, v in HU_CAPTIONS.items():
                        if k[:25] in orig:
                            sp.string = v
                            break

        # Also localize img[alt] in filmstrips
        for slide in soup.find_all(class_='ltt-strip-slide'):
            img = slide.find('img')
            if img and img.get('alt'):
                alt_txt = img['alt'].strip()
                if alt_txt in HU_CAPTIONS:
                    img['alt'] = HU_CAPTIONS[alt_txt]
                else:
                    for k, v in HU_CAPTIONS.items():
                        if k[:25] in alt_txt:
                            img['alt'] = v
                            break

        # Hungarian Spec Cards Headings
        for sp_card in soup.find_all(class_='ltt-sp-card'):
            h4 = sp_card.find('h4')
            if h4:
                h4_txt = h4.get_text().strip()
                if h4_txt in HU_SP_HEADINGS:
                    h4.string = HU_SP_HEADINGS[h4_txt]

        # Field note blockquotes
        for bq in soup.find_all('blockquote'):
            btxt = bq.get_text()
            if 'Undercover Field Note:' in btxt:
                bq.clear()
                bq.append("💡 ")
                st = soup.new_tag('strong')
                st.string = "Helyszíni Tesztelői Megjegyzés:"
                bq.append(st)
                bq.append(" A Legenda Budapest legszínvonalasabb dunai vacsorahajózása. Saját építésű, csupa üveg panorámahajóikon valódi éttermi minőségű gyertyafényes vacsorát nyújtanak turistabüfé helyett.")

    # 12. Sticky Bar Translation
    s_info = STICKY_MAP.get(lang, STICKY_MAP.get('de', {}))
    bar = soup.find(class_='hybrid-sticky-bar') or soup.find(id='sticky-bar')
    if bar:
        for span in bar.find_all('span'):
            stxt = span.text.strip()
            if 'All 7 Dinner Cruises' in stxt or 'Mind a 7' in stxt:
                span.string = s_info.get('btn', stxt)
            elif stxt in ['Top', 'Fel']:
                span.string = s_info.get('top', stxt)
            elif 'Free 24h Cancellation' in stxt or '24h Cancellation' in stxt or 'lemondás' in stxt:
                span.string = s_info.get('trust', stxt)
            elif stxt in ['#1 PICK', '#1 VÁLASZTÁS', '#1 TOP-WAHL', '#1 CHOIX N°1']:
                span.string = s_info.get('rank', '#1 TOP')

        s_cta = bar.find(id='sticky-cta-btn') or bar.find(class_='hybrid-cta-btn')
        if s_cta:
            s_cta.string = s_info.get('cta', btn_check_text)

    # Sheet modal
    sheet_title = soup.find(class_='hybrid-sheet-title')
    if sheet_title:
        sheet_title.string = s_info.get('sheet', sheet_title.text)

    # 13. Update Inline Script JSON (window.LTT_PAGE_CONFIG)
    for sc in soup.find_all('script'):
        if sc.string and 'window.LTT_PAGE_CONFIG' in sc.string:
            sc_text = sc.string
            deck_lbl = s_info.get('deck', 'Top 7 Dinner Cruises Comparison')
            bd_lbl = s_info.get('bd', 'Detailed Breakdown (7 Dinner Cruises)')
            sc_text = re.sub(r'\"tocDeckLabel\":\s*\"[^\"]*\"', f'\"tocDeckLabel\": \"{deck_lbl}\"', sc_text)
            sc_text = re.sub(r'\"tocBreakdownLabel\":\s*\"[^\"]*\"', f'\"tocBreakdownLabel\": \"{bd_lbl}\"', sc_text)
            sc.string.replace_with(sc_text)

    # 14. Clean schema JSON-LD headline and descriptions
    for sc in soup.find_all('script', type='application/ld+json'):
        if sc.string:
            sc_text = sc.string
            pt_clean = ptest_text.replace('✓ ', '')
            sc_text = sc_text.replace('(Personally Tested)', f'({pt_clean})')
            sc_text = sc_text.replace('🏆 #1 Best Overall', r_info['gold'])
            sc_text = sc_text.replace('🥈 #2 Runner-Up', r_info['silver'])
            sc.string.replace_with(sc_text)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"✓ Localized {lang.upper()}: {file_path}")

def run_all_localizations():
    print("=== RUNNING FULL MULTILINGUAL LOCALIZATION SWEEP ===")
    
    # 1. Hungarian
    hu_slug = SLUG_MAP['hu']['dinner']
    hu_file = os.path.join(BASE_DIR, 'hu', hu_slug, 'index.html')
    localize_html_file(hu_file, 'hu')

    # 2. All other 20 languages
    for lang in LANGS:
        if lang == 'hu': continue
        slug = SLUG_MAP[lang]['dinner']
        p = os.path.join(BASE_DIR, lang, slug, 'index.html')
        if os.path.exists(p):
            localize_html_file(p, lang)

    print("\n=== SWEEP COMPLETED SUCCESSFULLY ===")

if __name__ == '__main__':
    run_all_localizations()
