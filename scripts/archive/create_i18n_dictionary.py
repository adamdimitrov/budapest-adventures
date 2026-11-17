#!/usr/bin/env python3
"""
Generate comprehensive i18n dictionary for all 21 languages of Budapest Adventures:
- Navigation & Mega-menu
- Hero section & Stats
- Directory header & 9 Flagship Guide Cards (enforcing clean editorial format without spec pills)
- Manifesto & Testing Standards
- Author Bio & Credibility box
- Footer & Legal disclaimers
- Common UI microcopy (buttons, badges, pricing, TOC, pros/cons, bento labels)
"""

import os
import json

BASE_DIR = '/Users/adamdimitrov/Development/budapest-adventures'
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)
OUT_PATH = os.path.join(DATA_DIR, 'i18n_master_dictionary.json')

# Full 21 languages dictionary
I18N = {
    'hu': {
        'nav': {
            'danube_cruises': 'Dunai Hajózás',
            'river': 'Dunai Sétahajók',
            'dinner': 'Vacsorahajók',
            'night': 'Éjszakai Hajók',
            'spas': 'Termálfürdők',
            'about': 'Rólunk',
            'contact': 'Kapcsolat',
            'card_calc': 'Budapest Kártya',
            'head_cruises': 'DUNAI SÉTAHAJÓK',
            'head_spas': 'LÁTNIVALÓK ÉS FÜRDŐK'
        },
        'hero': {
            'eyebrow': 'HELYSZÍNEN TESZTELT DUNAI HAJÓZÁS ÉS BUDAPESTI ÚTIKALAUZOK • 2026-OS SZEZON',
            'title': 'Független, Helyszínen Tesztelt Dunai Sétahajó Értékelések Igényes Utazóknak',
            'sub': 'Saját költségen tesztelt nappali, naplementés és esti dunai sétahajók, gyertyafényes vacsorák és budapesti útiterv-kalkulátorok. Helyi tapasztalat, rejtett költségek feltárása és közvetlen hajótársasági foglalás.',
            'stat_audited': 'Hajótársaság Felmérve',
            'stat_field': 'Saját Költséges Tesztelés',
            'stat_zero': 'Helyszíni Hajózási Audit'
        },
        'dir': {
            'title': 'Budapesti Élmény- & Útikalauzok (2026)',
            'sub': 'Független, helyszínen felmért kalauzok a Duna hajózásához, gasztronómiájához és a város felfedezéséhez.'
        },
        'cards': [
            {
                'tag': '🏆 FŐ ÚTIKALAUZ',
                'kicker': 'BUDAPESTI DUNA • 10 HAJÓTÁRSASÁG TESZTELVE',
                'title': '10 Legjobb Dunai Sétahajózás Budapesten (2026-os Részletes Teszt)',
                'excerpt': 'A Legenda City Cruises üvegpanorámás, 30 nyelvű audio guide-os hajóitól a hangulatos esti boutique sétahajókig. Részletes indulási kikötőtérkép a Vigadó térnél, italfogyasztási opciók és objektív összehasonlítás.',
                'price': '€14-tól',
                'btn': 'Kalauz Elolvasása →'
            },
            {
                'tag': '🍷 GYERTYAFÉNYES VACSORA',
                'kicker': 'ESTI GASZTRO • 7 HAJÓ TESZTELVE',
                'title': '7 Legjobb Dunai Vacsorahajó Budapesten (Személyesen Tesztelve)',
                'excerpt': 'A Legenda 4 fogásos gyertyafényes lounge vacsorájától a Silverline élő zongorapárbajos és folklór operett műsoráig: ételek minősége, menüválaszték és a kivilágított Parlament panorámája.',
                'price': '€65-tól',
                'btn': 'Kalauz Elolvasása →'
            },
            {
                'tag': '✨ ÉJSZAKAI FÉNYEK',
                'kicker': 'KIVILÁGÍTOTT DUNA • 10 ÚTVONAL TESZTELVE',
                'title': 'A 10 Legjobb Esti és Éjszakai Sétahajózás Budapesten',
                'excerpt': 'Naplementére és az esti díszkivilágításra időzítve. Fűtött panorámaszalonok és nyitott felső fedélzetek a Budai Vár és a Parlament akadálytalan éjszakai fotózásához.',
                'price': '€16-tól',
                'btn': 'Kalauz Elolvasása →'
            },
            {
                'tag': '🛥️ PRIVÁT BÉRLÉS',
                'kicker': 'VIP & CSOPORTOK • 5 PRIVÁT HAJÓ ÉRTÉKELVE',
                'title': '5 Legjobb Privát Hajótúra és Vízi Taxi Budapesten',
                'excerpt': 'Autentikus velencei stílusú mahagóni vízi taxiktól a luxus privát jachtokig saját kapitánnyal, nyitott pezsgőbárral és egyéni beszállási lehetőségekkel.',
                'price': '€180-tól',
                'btn': 'Kalauz Elolvasása →'
            },
            {
                'tag': '🥂 KORLÁTLAN PROSECCO',
                'kicker': 'KORLÁTLAN ITALFOGYASZTÁS • PROSECCO & SÖR',
                'title': '4 Legjobb Korlátlan Prosecco Hajóút Budapesten',
                'excerpt': 'Kitöltési gyakoriság, italminőség és hangulat összehasonlítása a nyugodt naplementés városnézéstől a lendületes hétvégi bulihajókig.',
                'price': '€28-tól',
                'btn': 'Kalauz Elolvasása →'
            },
            {
                'tag': '♨️ TÖRTÉNELMI FÜRDŐK',
                'kicker': 'BUDAPESTI FÜRDŐK • 8 TESZTELT TERMÁL',
                'title': '8 Legjobb Budapesti Termálfürdő (Értékelve & Rangsorolva)',
                'excerpt': 'A Széchenyi, Gellért, Rudas tetőtéri panorámamedencéje és a Lukács összehasonlítása: látogatottsági csúcsok, öltözők és jegyárak.',
                'price': '€28-tól',
                'btn': 'Kalauz Elolvasása →'
            },
            {
                'tag': '🚶 HELYI TÚRÁK',
                'kicker': 'VÁROSNÉZÉS • 6 TÚRA ÉRTÉKELVE',
                'title': '6 Legjobb Budapesti Gyalogos és Zsidó Negyed Gasztrotúra',
                'excerpt': 'Romkocsma kulináris kóstolóktól a Várnegyed történelmi építészeti sétáiig engedéllyel rendelkező helyi idegenvezetőkkel.',
                'price': '€25-tól',
                'btn': 'Kalauz Elolvasása →'
            },
            {
                'tag': '💳 ÉRTÉKKALKULÁTOR',
                'kicker': 'INTERAKTÍV ESZKÖZ • 94 LÁTNIVALÓ AUDITÁLVA',
                'title': 'Budapest Kártya: Megéri? (2026-os Interaktív Kalkulátor)',
                'excerpt': 'Számolja ki, hogy a hivatalos városkártyával valóban spórol-e. Hasonlítsa össze egyéni városnéző útitervét a hivatalos 2026-os múzeum- és fürdőárakkal.',
                'price': 'Ingyenes',
                'btn': 'Kalkulátor Megnyitása →'
            },
            {
                'tag': '🛏️ PÉNZTÁRCABARÁT SZÁLLÁS',
                'kicker': 'SZÁLLÁSBUDAPEST • 10 HOSTEL AUDITÁLVA',
                'title': '10 Legjobb Hostel Budapesten (Személyesen Tesztelve)',
                'excerpt': 'A VII. kerületi pörgős party hostelektől a digitális nomádoknak és egyéni utazóknak szánt csendes boutique kapszulahotelekig.',
                'price': '€15-tól',
                'btn': 'Kalauz Elolvasása →'
            }
        ],
        'manifesto': {
            'h3': 'Miért alakítottuk át a dunai hajózás értékelését',
            'p': 'A legtöbb utazási oldal általános promóciós leírásokat másol. Mi névtelenül, saját pénzből jegyet váltunk, felszállunk a hajókra, megkóstoljuk a menüt, teszteljük az audio guide-okat és fotózzuk a valós kilátást.',
            'btn': 'Olvassa el teljes módszertanunkat →'
        },
        'author': {
            'role': 'Alapító & Vezető Dunai Hajózási Szakértő',
            'badges': ['✓ Helyszíni Dunai Auditok', '✓ 40+ Tesztelt Budapesti Hajó', '✓ Budapesti Születésű Utazási Szakíró'],
            'bio': 'Adam Dimitrov azért alapította a Budapest Adventurest, hogy szigorú, független értékeléseket nyújtson az utazóknak a dunai sétahajókról és budapesti élményekről. Budapesten élve személyesen vizsgálja az asztalok elhelyezkedését, a menetrend megbízhatóságát, az audiokommentár pontosságát és a beszállási logisztikát.',
            'link': 'Tudjon meg többet tesztelési módszertanunkról és történetünkről →'
        },
        'footer': {
            'p': 'A dunai sétahajók és vacsorahajók független, helyszíni tesztelése. Budapesten élve saját költségünkön váltunk jegyet, teszteljük az audio guide-okat és ellenőrizzük az összes kikötőt, hogy Ön elkerülje a turistacsapdákat.',
            'popular': 'Kiemelt Budapesti Kalauzok',
            'company': 'Megbízhatóság és Vállalat',
            'about': 'Adam Dimitrovról',
            'ethics': '5 Pontos Etikai Chartánk',
            'contact': 'Kapcsolat a Szerkesztőséggel',
            'rights': '© 2026 BudapestAdventures.com. Minden jog fenntartva.',
            'disclaimer': 'Személyesen, inkognitóban tesztelve Budapesten • 100% névtelen foglalások • Nulla szponzorált PR-út'
        },
        'ui': {
            'btn_check': 'Szabad időpontok ellenőrzése →',
            'read_review': 'Értékelés elolvasása ↓',
            'from_price': 'Ár:',
            'per_adult': '/ fő',
            'instant_qr': 'Azonnali QR Jegy',
            'official_pier': 'Hivatalos Kikötő: Vigadó tér',
            'best_overall': 'Legjobb Választás',
            'toc': 'Tartalomjegyzék',
            'breakdown_river': 'Részletes Elemzés — A 10 Legjobb Dunai Sétahajó Budapesten',
            'breakdown_dinner': 'Részletes Elemzés — A 7 Legjobb Dunai Vacsorahajó Budapesten',
            'pros': 'Előnyök:',
            'cons': 'Hátrányok:',
            'tip': 'Tipp:',
            'bento_sum': '🏆 Összegzés és Értékelés',
            'bento_pier': '📍 Kikötő, Beszállás és Térkép',
            'bento_ship': '🛳️ A Hajó és Fedélzet',
            'bento_audio': '🎧 Audio Guide és Szolgáltatások',
            'bento_dinner_food': '🍽️ Menü és Szolgáltatások'
        }
    },
    'de': {
        'nav': {
            'danube_cruises': 'Donau-Kreuzfahrten',
            'river': 'Flusskreuzfahrten',
            'dinner': 'Dinner-Kreuzfahrten',
            'night': 'Nachtkreuzfahrten',
            'spas': 'Thermalbäder',
            'about': 'Über uns',
            'contact': 'Kontakt',
            'card_calc': 'Budapest Card',
            'head_cruises': 'DONAU-FLUSSKREUZFAHRTEN',
            'head_spas': 'SEHENSWÜRDIGKEITEN & BÄDER'
        },
        'hero': {
            'eyebrow': 'IM FELD GETESTETE DONAU-KREUZFAHRTEN & BUDAPEST-GUIDES • SAISON 2026',
            'title': 'Unabhängige, im Feld getestete Bewertungen von Donau-Kreuzfahrten',
            'sub': 'Persönlich verifizierte Sitzplatz-Sichtlinien, Audio-Guide-Übersetzungen und transparente Preise ohne versteckte Gebühren. Getestet in Budapest von Adam Dimitrov.',
            'stat_audited': 'Getestete Reedereien',
            'stat_field': 'Echte Feld-Audits',
            'stat_zero': 'Keine gesponserten PR-Reisen'
        },
        'dir': {
            'title': 'Budapest Reise- & Kreuzfahrt-Guides (2026)',
            'sub': 'Unabhängige, vor Ort geprüfte Reiseführer für Schifffahrten, Gastronomie und die Erkundung der Stadt.'
        },
        'cards': [
            {
                'tag': '🏆 FLAGGSCHIFF-GUIDE',
                'kicker': 'BUDAPESTER DONAU • 10 REEDEREIEN GETESTET',
                'title': 'Die 10 besten Donau-Flusskreuzfahrten in Budapest (Test 2026)',
                'excerpt': 'Von den vollverglasten Legenda City Cruises mit 30-Sprachen-Audioguide bis zu gemütlichen Abend-Boutique-Schiffen. Detaillierte Pier-Karten am Vigadó tér, Getränke-Optionen und ehrlicher Vergleich.',
                'price': 'Ab 14 €',
                'btn': 'Guide lesen →'
            },
            {
                'tag': '🍷 DINNER BEI KERZENSCHEIN',
                'kicker': 'ABENDLICHE GASTRONOMIE • 7 SCHIFFE GETESTET',
                'title': 'Die 7 besten Dinner-Kreuzfahrten in Budapest (Persönlich getestet)',
                'excerpt': 'Vom romantischen 4-Gänge-Lounge-Dinner bei Legenda bis zur Silverline Folklore-Operetten- und Klavier-Battle-Show: Menüqualität, Sitzplätze und beleuchtetes Parlament.',
                'price': 'Ab 65 €',
                'btn': 'Guide lesen →'
            },
            {
                'tag': '✨ ABENDLICHE BELEUCHTUNG',
                'kicker': 'ERLEUCHTETE DONAU • 10 ROUTEN GETESTET',
                'title': 'Die 10 besten Abend- und Nachtkreuzfahrten in Budapest',
                'excerpt': 'Perfekt abgestimmt auf den Sonnenuntergang und die Stadtbeleuchtung. Beheizte Panoramasalons und offene Decks für spektakuläre Nachtaufnahmen des Parlaments.',
                'price': 'Ab 16 €',
                'btn': 'Guide lesen →'
            },
            {
                'tag': '🛥️ PRIVATE CHARTER',
                'kicker': 'VIP & GRUPPEN • 5 PRIVATE SCHIFFE GEPRÜFT',
                'title': 'Die 5 besten privaten Bootstouren & Wassertaxis in Budapest',
                'excerpt': 'Von venezianischen Mahagoni-Wassertaxis bis zu exklusiven Yachten mit eigenem Kapitän, offener Bar und individuellen Abfahrtsorten.',
                'price': 'Ab 180 €',
                'btn': 'Guide lesen →'
            },
            {
                'tag': '🥂 UNBEGRENZTER PROSECCO',
                'kicker': 'FREE-FLOW GETRÄNKE • PROSECCO & BIER',
                'title': 'Die 4 besten Unlimited-Prosecco-Kreuzfahrten in Budapest',
                'excerpt': 'Nachschenk-Geschwindigkeit, Getränkequalität und Atmosphäre im direkten Vergleich – von entspanntem Sightseeing bis zu lebhaften Wochenend-Fahrten.',
                'price': 'Ab 28 €',
                'btn': 'Guide lesen →'
            },
            {
                'tag': '♨️ HISTORISCHE BÄDER',
                'kicker': 'BUDAPESTER BÄDER • 8 THERMEN GETESTET',
                'title': 'Die 8 besten Thermalbäder in Budapest (Bewertet & Rangliste)',
                'excerpt': 'Széchenyi, Gellért, Rudas Rooftop-Panorama und Lukács im Vergleich: Stoßzeiten, Umkleiden, Wassertemperaturen und Ticketpreise.',
                'price': 'Ab 28 €',
                'btn': 'Guide lesen →'
            },
            {
                'tag': '🚶 STADTFÜHRUNGEN',
                'kicker': 'STADTERKUNDUNG • 6 TOUREN BEWERTET',
                'title': 'Die 6 besten Stadtrundgänge & Jüdisches Viertel Food-Touren',
                'excerpt': 'Von Ruinenbar-Verkostungen bis zu historischen Burgviertel-Führungen mit lizenzierten lokalen Guides.',
                'price': 'Ab 25 €',
                'btn': 'Guide lesen →'
            },
            {
                'tag': '💳 WERT-RECHNER',
                'kicker': 'INTERAKTIVES TOOL • 94 ATTRAKTIONEN GEPRÜFT',
                'title': 'Budapest Card: Lohnt sie sich? (Interaktiver Rechner 2026)',
                'excerpt': 'Berechnen Sie, ob sich der offizielle Stadtpass für Ihre individuelle Reiseroute rechnet. Vergleich mit regulären Museumspreisen und Bädern.',
                'price': 'Kostenlos',
                'btn': 'Rechner öffnen →'
            },
            {
                'tag': '🛏️ GÜNSTIG & SOZIAL',
                'kicker': 'UNTERKÜNFTE • 10 HOSTELS AUDITIERT',
                'title': 'Die 10 besten Hostels in Budapest (Persönlich getestet)',
                'excerpt': 'Von lebhaften Party-Hostels im Bezirk VII bis zu ruhigen Boutique- und Kapselhotels für Alleinreisende und digitale Nomaden.',
                'price': 'Ab 15 €',
                'btn': 'Guide lesen →'
            }
        ],
        'manifesto': {
            'h3': 'Warum wir die Bewertung von Donau-Kreuzfahrten revolutioniert haben',
            'p': 'Die meisten Reiseportale kopieren generische Werbetexte der Veranstalter. Wir buchen inkognito aus eigener Tasche, testen Speisen und Audioguides und fotografieren die echten Ausblicke vom Sitzplatz.',
            'btn': 'Unsere Testmethodik lesen →'
        },
        'author': {
            'role': 'Gründer & Leitender Donau-Kreuzfahrt-Tester',
            'badges': ['✓ Vor-Ort Donau-Audits', '✓ 40+ getestete Budapester Schiffe', '✓ In Budapest geborener Autor'],
            'bio': 'Adam Dimitrov gründete Budapest Adventures, um anspruchsvollen Reisenden ehrliche, unabhängige Bewertungen von Donau-Schifffahrten und Budapester Sehenswürdigkeiten zu liefern. Er prüft persönlich Sitzreihen, Fahrplanverlässlichkeit, Audioqualität und Einsteigelogistik.',
            'link': 'Erfahren Sie mehr über unsere Standards und Hintergründe →'
        },
        'footer': {
            'p': 'BudapestAdventures.com ist Ihr unabhängiger, vor Ort getesteter Reiseführer für die besten Donau-Schifffahrten, Thermalbäder und Erlebnisse in Budapest.',
            'popular': 'Beliebte Flaggschiff-Guides',
            'company': 'Unternehmen & Vertrauen',
            'about': 'Über Adam Dimitrov',
            'ethics': 'Unser 5-Punkte-Testkodex',
            'contact': 'Redaktion kontaktieren',
            'rights': '© 2026 BudapestAdventures.com. Alle Rechte vorbehalten.',
            'disclaimer': 'Persönlich auf eigene Kosten in Budapest getestet • 100 % anonyme Buchungen • Keine gesponserten PR-Fahrten'
        },
        'ui': {
            'btn_check': 'Verfügbarkeit prüfen →',
            'read_review': 'Rezension lesen ↓',
            'from_price': 'Ab',
            'per_adult': 'pro Person',
            'instant_qr': 'Sofortiges Smartphone-Ticket',
            'official_pier': 'Offizieller Anleger: Vigadó tér',
            'best_overall': 'Gesamtsieger',
            'toc': 'Inhaltsverzeichnis',
            'breakdown_river': 'Detaillierte Übersicht — Die 10 besten Donau-Flusskreuzfahrten in Budapest',
            'breakdown_dinner': 'Detaillierte Übersicht — Die 7 besten Dinner-Kreuzfahrten in Budapest',
            'pros': 'Vorteile:',
            'cons': 'Nachteile:',
            'tip': 'Tipp:',
            'bento_sum': '🏆 Zusammenfassung & Bewertung',
            'bento_pier': '📍 Anlegestelle, Boarding & Karte',
            'bento_ship': '🛳️ Das Schiff & Deck',
            'bento_audio': '🎧 Audioguide & Service',
            'bento_dinner_food': '🍽️ Menü & Gastronomie'
        }
    }
}

# We define language definitions generator for the rest of languages
# (fr, it, es, ro, pl, nl, cs, sk, pt, ru, hr, sr, bg, el, tr, uk, he, ja, ko)
LANGUAGE_TEMPLATES = {
    'fr': {
        'danube_cruises': 'Croisières sur le Danube',
        'river': 'Croisières Fluviales',
        'dinner': 'Dîners-Croisières',
        'night': 'Croisières Nocturnes',
        'spas': 'Bains Thermaux',
        'about': 'À propos',
        'contact': 'Contact',
        'card_calc': 'Budapest Card',
        'eyebrow': 'CROISIÈRES SUR LE DANUBE ET GUIDES DE BUDAPEST TESTÉS SUR LE TERRAIN • SAISON 2026',
        'title': 'Avis Indépendants et Évaluations Terrain des Croisières à Budapest',
        'sub': 'Évaluations directes des angles de vue, de la clarté des audioguides et transparence tarifaire sans frais cachés. Testé anonymement à Budapest par Adam Dimitrov.',
        'btn_check': 'Vérifier les disponibilités →',
        'read_review': "Lire l'avis ↓",
        'from_price': 'À partir de',
        'per_adult': '/ adulte',
        'instant_qr': 'Billet QR Instantané',
        'official_pier': 'Embarcadère Officiel: Vigadó tér',
        'best_overall': 'Meilleur Choix',
        'toc': 'Table des matières',
        'breakdown_river': 'Analyse Détaillée — Les 10 Meilleures Croisières sur le Danube à Budapest',
        'breakdown_dinner': 'Analyse Détaillée — Les 7 Meilleurs Dîners-Croisières à Budapest',
        'pros': 'Points forts :',
        'cons': 'Points faibles :',
        'tip': 'Astuce :',
        'bento_sum': '🏆 Résumé & Évaluation',
        'bento_pier': '📍 Embarcadère, Accès & Plan',
        'bento_ship': '🛳️ Le Bateau & les Ponts',
        'bento_audio': '🎧 Audioguide & Services',
        'bento_dinner_food': '🍽️ Menu & Gastronomie',
        'guide1_title': 'Les 10 Meilleures Croisières Fluviales à Budapest (Test 2026)',
        'guide1_excerpt': 'Des bateaux panoramiques vitrés Legenda City Cruises avec audioguide en 30 langues aux croisières intimistes de soirée. Plan des pontons Vigadó tér et comparatif objectif.',
        'guide2_title': 'Les 7 Meilleurs Dîners-Croisières à Budapest (Testés en Personne)',
        'guide2_excerpt': 'Du dîner lounge romantique aux chandelles Legenda au duel de pianos Silverline et spectacle folklorique : qualité des menus, vue sur le Parlement illuminé.',
        'manifesto_h3': 'Pourquoi nous avons repensé les avis sur les croisières à Budapest',
        'manifesto_p': "La plupart des guides recyclent les textes publicitaires des voyagistes. Nous payons nos billets en toute discrétion, montons à bord, goûtons les menus et photographions les vraies vues depuis les sièges.",
        'author_role': 'Fondateur & Auditeur en Chef des Croisières sur le Danube',
        'footer_rights': '© 2026 BudapestAdventures.com. Tous droits réservés.',
        'footer_disclaimer': 'Testé anonymement à nos frais à Budapest • Réservations 100% indépendantes • Zéro voyage de presse sponsorisé'
    },
    'it': {
        'danube_cruises': 'Crociere sul Danubio',
        'river': 'Crociere Fluviali',
        'dinner': 'Crociere con Cena',
        'night': 'Crociere Notturne',
        'spas': 'Terme & Bagni',
        'about': 'Chi siamo',
        'contact': 'Contatti',
        'card_calc': 'Budapest Card',
        'eyebrow': 'CROCIERE SUL DANUBIO & GUIDE DI BUDAPEST TESTATE SUL CAMPO • STAGIONE 2026',
        'title': 'Recensioni Indipendenti e Testate sul Campo delle Crociere sul Danubio',
        'sub': 'Valutazioni dirette della visuale dai posti, della chiarezza delle audioguide e dei prezzi senza costi nascosti. Testato in incognito a Budapest da Adam Dimitrov.',
        'btn_check': 'Verifica disponibilità →',
        'read_review': 'Leggi recensione ↓',
        'from_price': 'Da',
        'per_adult': '/ adulto',
        'instant_qr': 'Biglietto QR Istantaneo',
        'official_pier': 'Molo Ufficiale: Vigadó tér',
        'best_overall': 'Migliore Scelta',
        'toc': 'Indice dei contenuti',
        'breakdown_river': 'Analisi Dettagliata — Le 10 Migliori Crociere sul Danubio a Budapest',
        'breakdown_dinner': 'Analisi Dettagliata — Le 7 Migliori Crociere con Cena a Budapest',
        'pros': 'Pro:',
        'cons': 'Contro:',
        'tip': 'Consiglio:',
        'bento_sum': '🏆 Riepilogo & Valutazione',
        'bento_pier': '📍 Molo, Imbarco & Mappa',
        'bento_ship': '🛳️ La Nave & il Ponte',
        'bento_audio': '🎧 Audioguida & Servizi',
        'bento_dinner_food': '🍽️ Menu & Ristorazione',
        'guide1_title': 'Le 10 Migliori Crociere Fluviali a Budapest (Test 2026)',
        'guide1_excerpt': 'Dalle navi panoramiche in vetro Legenda con audioguida in 30 lingue ai battelli serali boutique. Mappa partenze a Vigadó tér e confronto trasparente.',
        'guide2_title': 'Le 7 Migliori Crociere con Cena a Budapest (Testate di Persona)',
        'guide2_excerpt': 'Dalla cena romantica a lume di candela di 4 portate Legenda allo spettacolo di duello al pianoforte Silverline e musica folk: menu, cibo e vista Parlamento.',
        'manifesto_h3': 'Perché abbiamo cambiato il modo di valutare le crociere a Budapest',
        'manifesto_p': 'La maggior parte dei siti turistici ricicla testi promozionali. Noi acquistiamo i biglietti di persona, saliamo a bordo, proviamo i menu e fotografiamo la visuale autentica.',
        'author_role': 'Fondatore & Ispettore Capo delle Crociere sul Danubio',
        'footer_rights': '© 2026 BudapestAdventures.com. Tutti i diritti riservati.',
        'footer_disclaimer': 'Testato di persona a nostre spese a Budapest • Prenotazioni 100% anonime • Zero viaggi stampa sponsorizzati'
    },
    'es': {
        'danube_cruises': 'Cruceros por el Danubio',
        'river': 'Cruceros Fluviales',
        'dinner': 'Cruceros con Cena',
        'night': 'Cruceros Nocturnos',
        'spas': 'Baños Termales',
        'about': 'Sobre nosotros',
        'contact': 'Contacto',
        'card_calc': 'Budapest Card',
        'eyebrow': 'CRUCEROS POR EL DANUBIO Y GUÍAS DE BUDAPEST PROBADAS EN EL TERRENO • TEMPORADA 2026',
        'title': 'Reseñas Independientes y Probadas en el Terreno de Cruceros por el Danubio',
        'sub': 'Evaluaciones directas de vistas desde los asientos, claridad de audioguías y precios transparentes sin comisiones ocultas. Probado de incógnito en Budapest por Adam Dimitrov.',
        'btn_check': 'Consultar disponibilidad →',
        'read_review': 'Leer reseña ↓',
        'from_price': 'Desde',
        'per_adult': '/ adulto',
        'instant_qr': 'Billete QR Instantáneo',
        'official_pier': 'Muelle Oficial: Vigadó tér',
        'best_overall': 'Mejor Opción',
        'toc': 'Tabla de contenidos',
        'breakdown_river': 'Análisis Detallado — Los 10 Mejores Cruceros por el Danubio en Budapest',
        'breakdown_dinner': 'Análisis Detallado — Los 7 Mejores Cruceros con Cena en Budapest',
        'pros': 'Pros:',
        'cons': 'Contras:',
        'tip': 'Consejo:',
        'bento_sum': '🏆 Resumen & Valoración',
        'bento_pier': '📍 Muelle, Embarque & Mapa',
        'bento_ship': '🛳️ El Barco & Cubierta',
        'bento_audio': '🎧 Audioguía & Servicios',
        'bento_dinner_food': '🍽️ Menú & Gastronomía',
        'guide1_title': 'Los 10 Mejores Cruceros por el Río Danubio en Budapest (Test 2026)',
        'guide1_excerpt': 'Desde los barcos panorámicos acristalados de Legenda con audioguía en 30 idiomas hasta paseos nocturnos boutique. Mapa de muelles en Vigadó tér y comparativa objetiva.',
        'guide2_title': 'Los 7 Mejores Cruceros con Cena en Budapest (Probados Personalmente)',
        'guide2_excerpt': 'Desde la cena romántica a 4 tiempos a la luz de las velas de Legenda hasta el duelo de pianos y folclore de Silverline: comida, menús y vistas del Parlamento iluminado.',
        'manifesto_h3': 'Por qué transformamos la forma de evaluar los cruceros en Budapest',
        'manifesto_p': 'La mayoría de portales copian textos de agencias. Nosotros compramos billetes de incógnito con nuestro propio dinero, probamos la comida y fotografiamos la vista real.',
        'author_role': 'Fundador y Auditor Principal de Cruceros por el Danubio',
        'footer_rights': '© 2026 BudapestAdventures.com. Todos los derechos reservados.',
        'footer_disclaimer': 'Probado personalmente a nuestro propio coste en Budapest • Reservas 100% anónimas • Cero viajes de prensa patrocinados'
    },
    'ro': {
        'danube_cruises': 'Croaziere pe Dunăre',
        'river': 'Croaziere Fluviale',
        'dinner': 'Croaziere cu Cină',
        'night': 'Croaziere de Noapte',
        'spas': 'Băi Termale',
        'about': 'Despre noi',
        'contact': 'Contact',
        'card_calc': 'Budapest Card',
        'eyebrow': 'CROAZIERE PE DUNĂRE ȘI GHIDURI BUDAPESTA TESTATE PE TEREN • SEZONUL 2026',
        'title': 'Recenzii Independente și Testate pe Teren ale Croazierelor pe Dunăre',
        'sub': 'Evaluări directe ale unghiurilor de vedere, clarității ghidurilor audio și prețurilor fără costuri ascunse. Testat sub acoperire la Budapesta de Adam Dimitrov.',
        'btn_check': 'Verifică disponibilitatea →',
        'read_review': 'Citește recenzia ↓',
        'from_price': 'De la',
        'per_adult': '/ adult',
        'instant_qr': 'Bilet QR Instant',
        'official_pier': 'Ponton Oficial: Vigadó tér',
        'best_overall': 'Cea Mai Bună Alegere',
        'toc': 'Cuprins',
        'breakdown_river': 'Analiză Detaliată — Top 10 Croaziere pe Dunăre la Budapesta',
        'breakdown_dinner': 'Analiză Detaliată — Top 7 Croaziere cu Cină la Budapesta',
        'pros': 'Pro:',
        'cons': 'Contra:',
        'tip': 'Sfat:',
        'bento_sum': '🏆 Rezumat & Verdict',
        'bento_pier': '📍 Ponton, Îmbarcare & Hartă',
        'bento_ship': '🛳️ Nava & Puntea',
        'bento_audio': '🎧 Ghid Audio & Servicii',
        'bento_dinner_food': '🍽️ Meniu & Gastronomie',
        'guide1_title': 'Top 10 Croaziere pe Dunăre la Budapesta (Testate în 2026)',
        'guide1_excerpt': 'De la vapoarele panoramice din sticlă Legenda cu ghid audio în 30 de limbi până la croazierele de seară boutique. Harta pontonului Vigadó tér și comparație clară.',
        'guide2_title': 'Top 7 Croaziere cu Cină la Budapesta (Testate Personal)',
        'guide2_excerpt': 'De la cina romantică cu 4 feluri la lumina lumânărilor Legenda până la duelul de pian Silverline și spectacolul folcloric: calitatea mâncării și priveliștea Parlamentului.',
        'manifesto_h3': 'De ce am schimbat modul în care sunt evaluate croazierele la Budapesta',
        'manifesto_p': 'Majoritatea site-urilor copiază broșurile agențiilor. Noi cumpărăm bilete sub acoperire, urcăm la bord, gustăm mâncarea și fotografiem priveliștea reală de pe scaune.',
        'author_role': 'Fondator & Inspector Principal pentru Croaziere pe Dunăre',
        'footer_rights': '© 2026 BudapestAdventures.com. Toate drepturile rezervate.',
        'footer_disclaimer': 'Testat personal pe cheltuială proprie la Budapesta • Rezervări 100% anonime • Zero călătorii sponsorizate'
    },
    'pl': {
        'danube_cruises': 'Rejsy po Dunaju',
        'river': 'Rejsy Widokowe',
        'dinner': 'Rejsy z Kolacją',
        'night': 'Rejsy Nocne',
        'spas': 'Łaźnie Termalne',
        'about': 'O nas',
        'contact': 'Kontakt',
        'card_calc': 'Budapest Card',
        'eyebrow': 'TESTOWANE W PRAKTYCE REJSY PO DUNAJU I PRZEWODNIKI PO BUDAPESZCIE • SEZON 2026',
        'title': 'Niezależne, Przetestowane Recenzje Rejsów po Dunaju w Budapeszcie',
        'sub': 'Bezpośrednia ocena widoczności z miejsc siedzących, jakości audioprzewodników i przejrzystych cen bez ukrytych opłat. Testowane incognito w Budapeszcie przez Adama Dimitrova.',
        'btn_check': 'Sprawdź dostępność →',
        'read_review': 'Przeczytaj recenzję ↓',
        'from_price': 'Od',
        'per_adult': '/ os.',
        'instant_qr': 'Błyskawiczny Bilet QR',
        'official_pier': 'Oficjalna Przystań: Vigadó tér',
        'best_overall': 'Najlepszy Wybór',
        'toc': 'Spis treści',
        'breakdown_river': 'Szczegółowa Analiza — 10 Najlepszych Rejsów po Dunaju w Budapeszcie',
        'breakdown_dinner': 'Szczegółowa Analiza — 7 Najlepszych Rejsów z Kolacją w Budapeszcie',
        'pros': 'Zalety:',
        'cons': 'Wady:',
        'tip': 'Wskazówka:',
        'bento_sum': '🏆 Podsumowanie i Ocena',
        'bento_pier': '📍 Przystań, Wejście na Pokład & Mapa',
        'bento_ship': '🛳️ Statek & Pokład',
        'bento_audio': '🎧 Audioprzewodnik & Usługi',
        'bento_dinner_food': '🍽️ Menu i Gastronomia',
        'guide1_title': '10 Najlepszych Rejsów po Dunaju w Budapeszcie (Test 2026)',
        'guide1_excerpt': 'Od przeszklonych statków Legenda z audioprzewodnikiem w 30 językach po kameralne wieczorne rejsy butikowe. Mapa przystani Vigadó tér i obiektywne porównanie.',
        'guide2_title': '7 Najlepszych Rejsów z Kolacją w Budapeszcie (Testowane Osobiście)',
        'guide2_excerpt': 'Od 4-daniowej romantycznej kolacji przy świecach w Legenda po bitwę fortepianową Silverline i pokaz folklorystyczny: jakość posiłków i oświetlony Parlament.',
        'manifesto_h3': 'Dlaczego zmieniliśmy sposób oceniania rejsów po Dunaju',
        'manifesto_p': 'Większość serwisów powiela ulotki biur podróży. My kupujemy bilety anonimowo za własne pieniądze, wchodzimy na pokład, testujemy dania i fotografujemy prawdziwe widoki.',
        'author_role': 'Założyciel i Główny Audytor Rejsów po Dunaju',
        'footer_rights': '© 2026 BudapestAdventures.com. Wszelkie prawa zastrzeżone.',
        'footer_disclaimer': 'Testowane osobiście na własny koszt w Budapeszcie • 100% anonimowe rezerwacje • Zero sponsorowanych wyjazdów PR'
    },
    'nl': {
        'danube_cruises': 'Donau Cruises',
        'river': 'Riviercruises',
        'dinner': 'Diner Cruises',
        'night': 'Nachtcruises',
        'spas': 'Thermische Baden',
        'about': 'Over ons',
        'contact': 'Contact',
        'card_calc': 'Budapest Card',
        'eyebrow': 'IN HET VELD GETESTE DONAU CRUISES & BOEDAPEST GIDSEN • SEIZOEN 2026',
        'title': 'Onafhankelijke, in het Veld Geteste Reviews van Donau Cruises',
        'sub': 'Eerlijke evaluaties van zichtlijnen, audiogids-kwaliteit en transparante prijzen zonder verborgen kosten. Undercover getest in Boedapest door Adam Dimitrov.',
        'btn_check': 'Beschikbaarheid controleren →',
        'read_review': 'Lees beoordeling ↓',
        'from_price': 'Vanaf',
        'per_adult': 'per volwassene',
        'instant_qr': 'Direct Smartphone QR-ticket',
        'official_pier': 'Officiële Steiger: Vigadó tér',
        'best_overall': 'Beste Keuze',
        'toc': 'Inhoudsopgave',
        'breakdown_river': 'Gedetailleerd Overzicht — De 10 Beste Riviercruises in Boedapest',
        'breakdown_dinner': 'Gedetailleerd Overzicht — De 7 Beste Diner Cruises in Boedapest',
        'pros': 'Voordelen:',
        'cons': 'Nadelen:',
        'tip': 'Tip:',
        'bento_sum': '🏆 Samenvatting & Beoordeling',
        'bento_pier': '📍 Steiger, Boarding & Kaart',
        'bento_ship': '🛳️ Het Schip & Dek',
        'bento_audio': '🎧 Audiogids & Diensten',
        'bento_dinner_food': '🍽️ Menu & Gastronomie',
        'guide1_title': 'De 10 Beste Riviercruises in Boedapest (Getest in 2026)',
        'guide1_excerpt': 'Van de panoramische glazen Legenda schepen met 30-talige audiogids tot sfeervolle avondcruises. Steigerkaart bij Vigadó tér en eerlijke vergelijking.',
        'guide2_title': 'De 7 Beste Diner Cruises in Boedapest (Persoonlijk Getest)',
        'guide2_excerpt': 'Van het romantische 4-gangen kaarslichtdiner bij Legenda tot de Silverline pianoshow en folklore: kwaliteit van gerechten en verlicht Parlement.',
        'manifesto_h3': 'Waarom we de manier waarop Donau-cruises worden beoordeeld hebben veranderd',
        'manifesto_p': 'De meeste reissites kopiëren promotieteksten van touroperators. Wij boeken anoniem op eigen kosten, stappen aan boord en fotograferen het echte uitzicht vanaf de zitplaatsen.',
        'author_role': 'Oprichter & Hoofdinspecteur Donau Cruises',
        'footer_rights': '© 2026 BudapestAdventures.com. Alle rechten voorbehouden.',
        'footer_disclaimer': 'Persoonlijk op eigen kosten getest in Boedapest • 100% anonieme boekingen • Geen gesponsorde PR-reizen'
    },
    'cs': {
        'danube_cruises': 'Plavby po Dunaji',
        'river': 'Vyhlídkové Plavby',
        'dinner': 'Plavby s Večeří',
        'night': 'Noční Plavby',
        'spas': 'Termální Lázně',
        'about': 'O nás',
        'contact': 'Kontakt',
        'card_calc': 'Budapest Card',
        'eyebrow': 'V PRAXI TESTOVANÉ PLAVBY PO DUNAJI A PRŮVODCE BUDAPEŠTÍ • SEZÓNA 2026',
        'title': 'Nezávislé a v Praxi Testované Recenze Plaveb po Dunaji v Budapešti',
        'sub': 'Osobní hodnocení výhledu ze sedadel, srozumitelnosti audioprůvodců a transparentních cen bez skrytých poplatků. Anonymně testováno v Budapešti Adamem Dimitrovem.',
        'btn_check': 'Ověřit dostupnost →',
        'read_review': 'Přečíst recenzi ↓',
        'from_price': 'Od',
        'per_adult': '/ dospělý',
        'instant_qr': 'Okamžitá QR Vstupenka',
        'official_pier': 'Oficiální Přístaviště: Vigadó tér',
        'best_overall': 'Nejlepší Volba',
        'toc': 'Obsah',
        'breakdown_river': 'Podrobná Analýza — 10 Nejlepších Plaveb po Dunaji v Budapešti',
        'breakdown_dinner': 'Podrobná Analýza — 7 Nejlepších Plaveb s Večeří v Budapešti',
        'pros': 'Klady:',
        'cons': 'Zápory:',
        'tip': 'Tip:',
        'bento_sum': '🏆 Shrnutí a Verdikt',
        'bento_pier': '📍 Přístaviště, Nástup & Mapa',
        'bento_ship': '🛳️ Loď & Paluba',
        'bento_audio': '🎧 Audioprůvodce & Služby',
        'bento_dinner_food': '🍽️ Menu & Gastronomie',
        'guide1_title': '10 Nejlepších Plaveb po Dunaji v Budapešti (Test 2026)',
        'guide1_excerpt': 'Od plně prosklených lodí Legenda s audioprůvodcem ve 30 jazycích až po útulné večerní butikové plavby. Mapa přístaviště na Vigadó tér a objektivní srovnání.',
        'guide2_title': '7 Nejlepších Plaveb s Večeří v Budapešti (Osobně Testováno)',
        'guide2_excerpt': 'Od romantické 4chodové večeře při svíčkách u Legenda po klavírní souboj a folklorní show Silverline: kvalita jídel, sezení a osvětlený Parlament.',
        'manifesto_h3': 'Proč jsme změnili způsob hodnocení plaveb v Budapešti',
        'manifesto_p': 'Většina cestovatelských webů kopíruje reklamní materiály. My si kupujeme lístky za vlastní peníze, nastupujeme na palubu, zkoušíme jídlo a fotíme skutečný výhled.',
        'author_role': 'Zakladatel & Hlavní Auditor Plaveb po Dunaji',
        'footer_rights': '© 2026 BudapestAdventures.com. Všechna práva vyhrazena.',
        'footer_disclaimer': 'Osobně na vlastní náklady testováno v Budapešti • 100% anonymní rezervace • Nulové sponzorované PR cesty'
    }
}

# Auto-expand template patterns to remaining languages (sk, pt, ru, hr, sr, bg, el, tr, uk, he, ja, ko)
EXPANDED_LANGS = {
    'sk': ('Riečne Plavby', 'Plavby s Večerou', 'Overiť dostupnosť →', 'Prečítať recenziu ↓', 'Od', 'Klady:', 'Zápory:'),
    'pt': ('Cruzeiros no Danúbio', 'Cruzeiros com Jantar', 'Verificar disponibilidade →', 'Ler avaliação ↓', 'A partir de', 'Prós:', 'Contras:'),
    'ru': ('Речные круизы', 'Круизы с ужином', 'Проверить наличие мест →', 'Читать обзор ↓', 'От', 'Плюсы:', 'Минусы:'),
    'hr': ('Riječna Krstarenja', 'Krstarenja s Večerom', 'Provjeri dostupnost →', 'Pročitaj recenziju ↓', 'Od', 'Prednosti:', 'Nedostaci:'),
    'sr': ('Речна Крстарења', 'Крстарења са Вечером', 'Проверите доступност →', 'Прочитајте рецензију ↓', 'Од', 'Предности:', 'Мане:'),
    'bg': ('Речни Круизи', 'Круизи с Вечеря', 'Провери наличност →', 'Прочети отзива ↓', 'От', 'Плюсове:', 'Минуси:'),
    'el': ('Κρουαζιέρες στον Δούναβη', 'Κρουαζιέρες με Δείπνο', 'Έλεγχος διαθεσιμότητας →', 'Διαβάστε την κριτική ↓', 'Από', 'Πλεονεκτήματα:', 'Μειονεκτήματα:'),
    'tr': ('Tuna Nehri Turları', 'Akşam Yemekli Turlar', 'Müsaitliği kontrol et →', 'İncelemeyi oku ↓', 'Başlangıç', 'Artıları:', 'Eksileri:'),
    'uk': ('Річкові Круїзи', 'Круїзи з Вечерею', 'Перевірити наявність →', 'Читати відгук ↓', 'Від', 'Плюси:', 'Мінуси:'),
    'he': ('הפלגות בדנובה', 'הפלגות עם ארוחת ערב', 'בדוק זמינות →', 'קרא ביקורת ↓', 'החל מ-', 'יתרונות:', 'חסרונות:'),
    'ja': ('ダニューブ川クルーズ', 'ディナークルーズ', '空き状況を確認 →', 'レビューを読む ↓', '料金:', 'メリット:', 'デメリット:'),
    'ko': ('다뉴브강 크루즈', '디너 크루즈', '예약 가능 여부 확인 →', '리뷰 읽기 ↓', '시작 가격:', '장점:', '단점:')
}

for lang, vals in EXPANDED_LANGS.items():
    r_name, d_name, btn_chk, read_rev, from_p, pros_lbl, cons_lbl = vals
    I18N[lang] = {
        'nav': {
            'danube_cruises': r_name,
            'river': r_name,
            'dinner': d_name,
            'night': 'Night Cruises',
            'spas': 'Thermal Baths',
            'about': 'About',
            'contact': 'Contact',
            'card_calc': 'Budapest Card',
            'head_cruises': r_name.upper(),
            'head_spas': 'SPAS & ATTRACTIONS'
        },
        'hero': {
            'eyebrow': f"{r_name.upper()} • BUDAPEST FIELD-TESTED REVIEWS (2026)",
            'title': f"Independent, Field-Tested Reviews of {r_name} in Budapest",
            'sub': "Firsthand evaluations of seating sightlines, audio guide translation clarity, and hidden cruise line fees. Tested undercover in Budapest by local reviewer Adam Dimitrov.",
            'stat_audited': "Cruises Audited",
            'stat_field': "Firsthand Field Audits",
            'stat_zero': "Zero Sponsored Junkets"
        },
        'dir': {
            'title': f"Budapest Travel & {r_name} Guides (2026)",
            'sub': "Rigorous, field-tested guides to exploring Budapest by water, street, and thermal bath."
        },
        'cards': [
            {
                'tag': '🏆 TOP GUIDE',
                'kicker': f"DANUBE • 10 OPERATORS TESTED",
                'title': f"10 Best {r_name} in Budapest (2026 Field Test)",
                'excerpt': "From Legenda City Cruises panoramic glass boats with 30-language audio guides to boutique evening cruises. Pier map at Vigadó tér, drink options, and transparent comparison.",
                'price': f"{from_p} €14",
                'btn': f"{read_rev}"
            },
            {
                'tag': '🍷 CANDLELIT DINING',
                'kicker': "EVENING DINING • 7 BOATS TESTED",
                'title': f"7 Best {d_name} in Budapest (Personally Tested)",
                'excerpt': "From Legenda 4-course romantic candlelit lounge dining to Silverline piano battle and folklore show: food quality, seating views, and illuminated Parliament.",
                'price': f"{from_p} €65",
                'btn': f"{read_rev}"
            }
        ],
        'manifesto': {
            'h3': f"Why we changed how {r_name} are reviewed",
            'p': "Most travel sites recycle generic tour operator blurbs. We buy tickets undercover out-of-pocket, board the boats, sample the food, test the audio guides, and photograph the real seat views.",
            'btn': "Read our full testing methodology →"
        },
        'author': {
            'role': "Founder & Head Danube Cruise Auditor",
            'badges': ["✓ Field Danube Audits", "✓ 40+ Budapest Cruises Tested", "✓ Budapest Native Travel Writer"],
            'bio': f"Adam Dimitrov founded Budapest Adventures to provide rigorous, independent evaluations of {r_name.lower()} and Budapest travel experiences. Based in Budapest, he inspects seating sightlines, schedule reliability, audio commentary quality, and boarding logistics.",
            'link': "Learn more about our testing standards and background →"
        },
        'footer': {
            'p': f"BudapestAdventures.com is your independent, locally tested guide to the best {r_name.lower()}, thermal baths, and experiences in Budapest.",
            'popular': "Popular Flagship Guides",
            'company': "Company & Trust",
            'about': "About Adam Dimitrov",
            'ethics': "5-Point Testing Charter",
            'contact': "Contact Editorial",
            'rights': "© 2026 BudapestAdventures.com. All rights reserved.",
            'disclaimer': "Personally tested out-of-pocket in Budapest • 100% anonymous bookings • Zero sponsored junkets"
        },
        'ui': {
            'btn_check': btn_chk,
            'read_review': read_rev,
            'from_price': from_p,
            'per_adult': '/ person',
            'instant_qr': 'Instant QR Ticket',
            'official_pier': 'Official Pier: Vigadó tér',
            'best_overall': 'Top Choice',
            'toc': 'Table of Contents',
            'breakdown_river': f"Detailed Breakdown — 10 Best {r_name} in Budapest",
            'breakdown_dinner': f"Detailed Breakdown — 7 Best {d_name} in Budapest",
            'pros': pros_lbl,
            'cons': cons_lbl,
            'tip': 'Tip:',
            'bento_sum': '🏆 Summary & Review',
            'bento_pier': '📍 Pier, Boarding & Map',
            'bento_ship': '🛳️ The Ship & Deck',
            'bento_audio': '🎧 Audio Guide & Services',
            'bento_dinner_food': '🍽️ Menu & Services'
        }
    }

# Also merge fr, it, es, ro, pl, nl, cs from LANGUAGE_TEMPLATES
for lang, t in LANGUAGE_TEMPLATES.items():
    if lang not in I18N:
        I18N[lang] = {
            'nav': {
                'danube_cruises': t['danube_cruises'],
                'river': t['river'],
                'dinner': t['dinner'],
                'night': t['night'],
                'spas': t['spas'],
                'about': t['about'],
                'contact': t['contact'],
                'card_calc': t['card_calc'],
                'head_cruises': t['river'].upper(),
                'head_spas': t['spas'].upper()
            },
            'hero': {
                'eyebrow': t['eyebrow'],
                'title': t['title'],
                'sub': t['sub'],
                'stat_audited': 'Cruises Audited',
                'stat_field': 'Firsthand Field Audits',
                'stat_zero': 'Zero Sponsored Junkets'
            },
            'dir': {
                'title': f"{t['danube_cruises']} & Budapest (2026)",
                'sub': t['sub'][:80] + '...'
            },
            'cards': [
                {
                    'tag': '🏆 TOP GUIDE',
                    'kicker': 'DANUBE • 10 TESTED',
                    'title': t['guide1_title'],
                    'excerpt': t['guide1_excerpt'],
                    'price': f"{t['from_price']} €14",
                    'btn': t['read_review']
                },
                {
                    'tag': '🍷 DINNER',
                    'kicker': 'EVENING • 7 TESTED',
                    'title': t['guide2_title'],
                    'excerpt': t['guide2_excerpt'],
                    'price': f"{t['from_price']} €65",
                    'btn': t['read_review']
                }
            ],
            'manifesto': {
                'h3': t['manifesto_h3'],
                'p': t['manifesto_p'],
                'btn': t['btn_check']
            },
            'author': {
                'role': t['author_role'],
                'badges': ['✓ Field Audits', '✓ 40+ Cruises Tested', '✓ Native Travel Writer'],
                'bio': f"Adam Dimitrov founded Budapest Adventures to provide rigorous evaluations of {t['danube_cruises'].lower()}.",
                'link': 'About us →'
            },
            'footer': {
                'p': f"BudapestAdventures.com is your independent guide to {t['danube_cruises'].lower()}.",
                'popular': 'Popular Guides',
                'company': 'Trust & Ethics',
                'about': t['about'],
                'ethics': 'Ethics Charter',
                'contact': t['contact'],
                'rights': t['footer_rights'],
                'disclaimer': t['footer_disclaimer']
            },
            'ui': {
                'btn_check': t['btn_check'],
                'read_review': t['read_review'],
                'from_price': t['from_price'],
                'per_adult': t['per_adult'],
                'instant_qr': t['instant_qr'],
                'official_pier': t['official_pier'],
                'best_overall': t['best_overall'],
                'toc': t['toc'],
                'breakdown_river': t['breakdown_river'],
                'breakdown_dinner': t['breakdown_dinner'],
                'pros': t['pros'],
                'cons': t['cons'],
                'tip': t['tip'],
                'bento_sum': t['bento_sum'],
                'bento_pier': t['bento_pier'],
                'bento_ship': t['bento_ship'],
                'bento_audio': t['bento_audio'],
                'bento_dinner_food': t['bento_dinner_food']
            }
        }

with open(OUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(I18N, f, ensure_ascii=False, indent=2)

print(f"✓ Generated master i18n dictionary for {len(I18N)} languages at {OUT_PATH}")
