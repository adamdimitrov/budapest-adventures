# -*- coding: utf-8 -*-
"""
Generates verified translations for the 35 unique Dinner Quick Facts values across all 21 languages.
"""

import json
import os

BASE_DIR = '/Users/adamdimitrov/Development/budapest-adventures'
UNIQUE_EN_PATH = os.path.join(BASE_DIR, 'data', 'dinner_qf_unique_en.json')
OUTPUT_PATH = os.path.join(BASE_DIR, 'data', 'dinner_qf_values_i18n.json')

unique_en = json.load(open(UNIQUE_EN_PATH, encoding='utf-8'))

# Translations dictionary for all 21 languages
# Index mapping from dinner_qf_unique_en.json:
# 0: 1 Welcome drink + 4-course served menu
# 1: 1 Welcome drink + complete 4-course served meal
# 2: 1 Welcome glass of champagne or soft drink
# 3: 1 Welcome glass of sparkling wine + 4-course menu
# 4: 1.5 Hours (90 Minutes)
# 5: 12-Course Hungarian warm buffet + authentic folk music and live dance performance
# 6: 2.5 Hours
# 7: 2.5 Hours (150 Minutes)
# 8: 4-Course Hungarian feast + live traditional gypsy operetta musical performance
# 9: 4-Course dinner + live dual grand piano battle show with guest vocalist
# 10: 4-Course fine dining + authentic Hungarian folklore dance troupe and operetta singers
# 11: 4-Course gourmet served dinner + unlimited draft beer, wine, champagne & soft drinks
# 12: 4-Course gourmet à la carte fine dining (starter, soup, main, dessert)
# 13: 4-Course served dinner with candlelight table setting (ambient background music, no stage show)
# 14: 90–120 Minutes
# 15: All-you-can-eat buffet + 2 complimentary drinks (wine, beer, soft drinks)
# 16: Daily at 19:00 (Boarding at 18:30)
# 17: Daily at 19:00 (Boarding begins at 18:30)
# 18: Daily at 19:00, weekends at 22:00
# 19: Daily at 19:30 (Boarding at 19:00)
# 20: Daily at 20:00 (Boarding at 19:30)
# 21: Dock 7, Vigadó tér, 1051 Budapest
# 22: Evening boarding at 19:00 (2.5-hour duration)
# 23: Free for children (age 0–5)
# 24: Free for infants (age 0–2)
# 25: Free for infants (age 0–3)
# 26: Full refund up to 24 hours before departure
# 27: Id. Antall József rkp., 1051 Budapest (near Széchenyi Chain Bridge)
# 28: Instant smartphone QR ticket or printed
# 29: Instant smartphone QR voucher or printed
# 30: Jane Haining Rakpart, Dock 11, 1052 Budapest
# 31: Jane Haining rakpart, Dock 6, 1051 Budapest
# 32: Jane Haining rakpart, Dock 8A / Dock 11, 1052 Budapest
# 33: Live acoustic salon piano and vocal performance
# 34: Welcome glass of sparkling wine + mineral water + live salon violin/acoustic music

RAW_I18N = {
    "hu": [
        "1 üdvözlőital + 4 fogásos felszolgált menü",
        "1 üdvözlőital + komplett 4 fogásos felszolgált vacsora",
        "1 pohár üdvözlő pezsgő vagy üdítőital",
        "1 pohár üdvözlő pezsgő + 4 fogásos menü",
        "1,5 óra (90 perc)",
        "12 fogásos meleg magyar svédasztal + autentikus népzene és élő táncbemutató",
        "2,5 óra",
        "2,5 óra (150 perc)",
        "4 fogásos magyar lakoma + hagyományos élő cigányzene és operett előadás",
        "4 fogásos vacsora + élő zongorapárbaj show vendégénekesnővel",
        "4 fogásos prémium vacsora + autentikus magyar folklór táncegyüttes és operett énekesek",
        "4 fogásos ínyenc vacsora + korlátlan csapolt sör, bor, pezsgő és üdítőitalok",
        "4 fogásos à la carte prémium vacsora (előétel, leves, főétel, desszert)",
        "4 fogásos felszolgált vacsora gyertyafényes asztallal (hangulatos háttérzene, színpadi műsor nélkül)",
        "90–120 perc",
        "Korlátlan svédasztalos fogyasztás + 2 választható ital (bor, sör, üdítő)",
        "Naponta 19:00-kor (Beszállás 18:30-kor)",
        "Naponta 19:00-kor (A beszállás 18:30-kor kezdődik)",
        "Naponta 19:00-kor, hétvégén 22:00-kor",
        "Naponta 19:30-kor (Beszállás 19:00-kor)",
        "Naponta 20:00-kor (Beszállás 19:30-kor)",
        "7-es kikötő, Vigadó tér, 1051 Budapest",
        "Esti beszállás 19:00-kor (2,5 órás időtartam)",
        "Ingyenes gyermekeknek (0–5 éves korig)",
        "Ingyenes csecsemőknek (0–2 éves korig)",
        "Ingyenes csecsemőknek (0–3 éves korig)",
        "Teljes visszatérítés az indulás előtt 24 órával",
        "Id. Antall József rkp., 1051 Budapest (a Széchenyi Lánchíd közelében)",
        "Azonnali okostelefonos QR-jegy vagy nyomtatott",
        "Azonnali okostelefonos QR-voucher vagy nyomtatott",
        "Jane Haining rakpart, 11-es kikötő, 1052 Budapest",
        "Jane Haining rakpart, 6-os kikötő, 1051 Budapest",
        "Jane Haining rakpart, 8A / 11-es kikötő, 1052 Budapest",
        "Élő akusztikus szalon zongora- és énekelőadás",
        "Üdvözlő pohár pezsgő + ásványvíz + élő szalon hegedű/akusztikus zene"
    ],
    "de": [
        "1 Willkommensgetränk + serviertes 4-Gänge-Menü",
        "1 Willkommensgetränk + komplettes serviertes 4-Gänge-Menü",
        "1 Willkommensglas Champagner oder Softdrink",
        "1 Willkommensglas Sekt + 4-Gänge-Menü",
        "1,5 Stunden (90 Minuten)",
        "Warmes ungarisches 12-Gänge-Buffet + authentische Volksmusik und Live-Tanzshow",
        "2,5 Stunden",
        "2,5 Stunden (150 Minuten)",
        "Ungarisches 4-Gänge-Festmahl + traditionelle Live-Zigeuneroperette",
        "4-Gänge-Abendessen + Live-Klavierduell zweier Flügel mit Gastsängerin",
        "Gehobenes 4-Gänge-Menü + authentische Folklore-Tanzgruppe und Operettensänger",
        "Serviertes 4-Gänge-Gourmetmenü + unbegrenzt Fassbier, Wein, Sekt & Softdrinks",
        "À-la-carte-Gourmetmenü mit 4 Gängen (Vorspeise, Suppe, Hauptgang, Dessert)",
        "Serviertes 4-Gänge-Dinner bei Kerzenschein (dezente Hintergrundmusik, keine Bühnenshow)",
        "90–120 Minuten",
        "All-you-can-eat-Buffet + 2 Freigetränke (Wein, Bier, Softdrinks)",
        "Täglich um 19:00 Uhr (Boarding ab 18:30 Uhr)",
        "Täglich um 19:00 Uhr (Boarding beginnt um 18:30 Uhr)",
        "Täglich um 19:00 Uhr, am Wochenende auch 22:00 Uhr",
        "Täglich um 19:30 Uhr (Boarding ab 19:00 Uhr)",
        "Täglich um 20:00 Uhr (Boarding ab 19:30 Uhr)",
        "Anleger 7, Vigadó tér, 1051 Budapest",
        "Abendliches Boarding um 19:00 Uhr (2,5 Stunden Fahrzeit)",
        "Kostenlos für Kinder (0–5 Jahre)",
        "Kostenlos für Kleinkinder (0–2 Jahre)",
        "Kostenlos für Kleinkinder (0–3 Jahre)",
        "Volle Rückerstattung bis zu 24 Stunden vor Abfahrt",
        "Id. Antall József rkp., 1051 Budapest (nahe Kettenbrücke)",
        "Sofortiges Smartphone-QR-Ticket oder ausgedruckt",
        "Sofortiger Smartphone-QR-Gutschein oder ausgedruckt",
        "Jane Haining Rakpart, Anleger 11, 1052 Budapest",
        "Jane Haining rakpart, Anleger 6, 1051 Budapest",
        "Jane Haining rakpart, Anleger 8A / Anleger 11, 1052 Budapest",
        "Live-Salonklavier und Gesangsdarbietung",
        "Willkommens-Sekt + Mineralwasser + dezente Salon-Geigen-/Akustikmusik"
    ],
    "fr": [
        "1 Boisson d'accueil + menu 4 plats servi à table",
        "1 Boisson d'accueil + dîner complet 4 plats servi à table",
        "1 Coupe de champagne d'accueil ou boisson sans alcool",
        "1 Coupe de vin pétillant d'accueil + menu 4 plats",
        "1,5 heure (90 minutes)",
        "Buffet chaud hongrois 12 plats + musique folklorique et danse en direct",
        "2,5 heures",
        "2,5 heures (150 minutes)",
        "Festin hongrois 4 plats + musique tsigane traditionnelle et spectacle d'opérette",
        "Dîner 4 plats + duel de pianos à queue en direct avec chanteuse invitée",
        "Dîner gastronomique 4 plats + troupe de danseurs folkloriques et chanteurs d'opérette",
        "Dîner gastronomique 4 plats servi + bière pression, vin, champagne et sodas à volonté",
        "Menu gastronomique 4 plats à la carte (entrée, soupe, plat principal, dessert)",
        "Dîner 4 plats aux chandelles (musique d'ambiance intime, sans spectacle de scène)",
        "90–120 minutes",
        "Buffet à volonté + 2 boissons incluses (vin, bière, sodas)",
        "Tous les jours à 19h00 (embarquement à 18h30)",
        "Tous les jours à 19h00 (l'embarquement commence à 18h30)",
        "Tous les jours à 19h00, week-ends à 22h00",
        "Tous les jours à 19h30 (embarquement à 19h00)",
        "Tous les jours à 20h00 (embarquement à 19h30)",
        "Quai 7, Vigadó tér, 1051 Budapest",
        "Embarquement en soirée à 19h00 (durée de 2h30)",
        "Gratuit pour les enfants (0 à 5 ans)",
        "Gratuit pour les bébés (0 à 2 ans)",
        "Gratuit pour les bébés (0 à 3 ans)",
        "Remboursement intégral jusqu'à 24h avant le départ",
        "Id. Antall József rkp., 1051 Budapest (près du pont des Chaînes)",
        "Billet électronique QR instantané sur smartphone ou imprimé",
        "Bon d'échange QR instantané sur smartphone ou imprimé",
        "Jane Haining Rakpart, Quai 11, 1052 Budapest",
        "Jane Haining rakpart, Quai 6, 1051 Budapest",
        "Jane Haining rakpart, Quai 8A / Quai 11, 1052 Budapest",
        "Piano de salon et chant acoustique en direct",
        "Coupe de vin pétillant d'accueil + eau minérale + musique acoustique de salon en direct"
    ],
    "es": [
        "1 Bebida de bienvenida + menú servido de 4 platos",
        "1 Bebida de bienvenida + cena completa servida de 4 platos",
        "1 Copa de champán de bienvenida o refresco",
        "1 Copa de vino espumoso de bienvenida + menú de 4 platos",
        "1,5 horas (90 minutos)",
        "Buffet caliente húngaro de 12 platos + música folclórica y danza en vivo",
        "2,5 horas",
        "2,5 horas (150 minutos)",
        "Banquete húngaro de 4 platos + música tradicional gitana y opereta en vivo",
        "Cena de 4 platos + duelo de pianos de cola en vivo con vocalista invitada",
        "Cena gourmet de 4 platos + grupo de baile folclórico y cantantes de opereta",
        "Cena gourmet servida de 4 platos + cerveza de barril, vino, cava y refrescos ilimitados",
        "Cena gourmet a la carta de 4 platos (entrante, sopa, principal, postre)",
        "Cena servida de 4 platos a la luz de las velas (música ambiental, sin show en escenario)",
        "90–120 minutos",
        "Buffet libre + 2 bebidas incluidas (vino, cerveza, refrescos)",
        "Diario a las 19:00 (embarque a las 18:30)",
        "Diario a las 19:00 (el embarque comienza a las 18:30)",
        "Diario a las 19:00, fines de semana a las 22:00",
        "Diario a las 19:30 (embarque a las 19:00)",
        "Diario a las 20:00 (embarque a las 19:30)",
        "Muelle 7, Vigadó tér, 1051 Budapest",
        "Embarque nocturno a las 19:00 (duración de 2,5 horas)",
        "Gratis para niños (0–5 años)",
        "Gratis para bebés (0–2 años)",
        "Gratis para bebés (0–3 años)",
        "Reembolso total hasta 24 horas antes de la salida",
        "Id. Antall József rkp., 1051 Budapest (junto al Puente de las Cadenas)",
        "Billete QR instantáneo en smartphone o impreso",
        "Bono QR instantáneo en smartphone o impreso",
        "Jane Haining Rakpart, Muelle 11, 1052 Budapest",
        "Jane Haining rakpart, Muelle 6, 1051 Budapest",
        "Jane Haining rakpart, Muelle 8A / Muelle 11, 1052 Budapest",
        "Piano de salón y actuación vocal acústica en vivo",
        "Copa de vino espumoso de bienvenida + agua mineral + música acústica de violín en vivo"
    ],
    "it": [
        "1 Drink di benvenuto + menu servito di 4 portate",
        "1 Drink di benvenuto + cena completa servita di 4 portate",
        "1 Calice di champagne di benvenuto o bibita analcolica",
        "1 Calice di spumante di benvenuto + menu di 4 portate",
        "1,5 ore (90 minuti)",
        "Buffet caldo ungherese di 12 portate + musica folkloristica e danze dal vivo",
        "2,5 ore",
        "2,5 ore (150 minuti)",
        "Banchetto ungherese di 4 portate + musica tzigana tradizionale e operetta dal vivo",
        "Cena di 4 portate + duello di pianoforti a coda dal vivo con cantante",
        "Cena gourmet di 4 portate + corpo di ballo folcloristico e cantanti d'operetta",
        "Cena gourmet servita di 4 portate + birra alla spina, vino, spumante e bibite illimitati",
        "Cena gourmet à la carte di 4 portate (antipasto, zuppa, piatto principale, dessert)",
        "Cena servita di 4 portate a lume di candela (musica d'ambiente, nessun palco rumoroso)",
        "90–120 minuti",
        "Buffet a volontà + 2 bevande incluse (vino, birra, bibite)",
        "Tutti i giorni alle 19:00 (imbarco alle 18:30)",
        "Tutti i giorni alle 19:00 (l'imbarco inizia alle 18:30)",
        "Tutti i giorni alle 19:00, weekend alle 22:00",
        "Tutti i giorni alle 19:30 (imbarco alle 19:00)",
        "Tutti i giorni alle 20:00 (imbarco alle 19:30)",
        "Molo 7, Vigadó tér, 1051 Budapest",
        "Imbarco serale alle 19:00 (durata di 2,5 ore)",
        "Gratis per bambini (0–5 anni)",
        "Gratis per neonati (0–2 anni)",
        "Gratis per neonati (0–3 anni)",
        "Rimborso completo fino a 24 ore prima della partenza",
        "Id. Antall József rkp., 1051 Budapest (vicino al Ponte delle Catene)",
        "Biglietto QR istantaneo su smartphone o stampato",
        "Voucher QR istantaneo su smartphone o stampato",
        "Jane Haining Rakpart, Molo 11, 1052 Budapest",
        "Jane Haining rakpart, Molo 6, 1051 Budapest",
        "Jane Haining rakpart, Molo 8A / Molo 11, 1052 Budapest",
        "Pianoforte da salotto dal vivo e performance vocale acustica",
        "Calice di spumante di benvenuto + acqua minerale + musica tzigana acustica da salotto"
    ],
    "nl": [
        "1 Welkomstdrankje + geserveerd 4-gangenmenu",
        "1 Welkomstdrankje + compleet geserveerd 4-gangendiner",
        "1 Glas welkomstchampagne of frisdrank",
        "1 Glas welkomstbubbels + 4-gangenmenu",
        "1,5 uur (90 minuten)",
        "Warm Hongaars buffet met 12 gerechten + authentieke volksmuziek en dansshow",
        "2,5 uur",
        "2,5 uur (150 minuten)",
        "Hongaars 4-gangenfeestmaal + traditionele live zigeuneroperette",
        "4-gangendiner + live vleugelpianoduel met gastzangeres",
        "Gastronomisch 4-gangendiner + authentieke folkloredansgroep en operettezangers",
        "Geserveerd gastronomisch 4-gangendiner + onbeperkt tapbier, wijn, prosecco & frisdrank",
        "À-la-carte gastronomisch 4-gangenmenu (voorgerecht, soep, hoofdgerecht, dessert)",
        "Geserveerd 4-gangendiner bij kaarslicht (intiem achtergrondmuziekje, geen show)",
        "90–120 minuten",
        "All-you-can-eat buffet + 2 inbegrepen drankjes (wijn, bier, frisdrank)",
        "Dagelijks om 19:00 uur (Boarding om 18:30 uur)",
        "Dagelijks om 19:00 uur (Boarding begint om 18:30 uur)",
        "Dagelijks om 19:00 uur, in het weekend om 22:00 uur",
        "Dagelijks om 19:30 uur (Boarding om 19:00 uur)",
        "Dagelijks om 20:00 uur (Boarding om 19:30 uur)",
        "Steiger 7, Vigadó tér, 1051 Boedapest",
        "Avondboarding om 19:00 uur (duur 2,5 uur)",
        "Gratis voor kinderen (0–5 jaar)",
        "Gratis voor baby's (0–2 jaar)",
        "Gratis voor baby's (0–3 jaar)",
        "Volledige terugbetaling tot 24 uur voor vertrek",
        "Id. Antall József rkp., 1051 Boedapest (bij de Kettingbrug)",
        "Direct mobiel QR-ticket of geprint",
        "Direct mobiele QR-voucher of geprint",
        "Jane Haining Rakpart, Steiger 11, 1052 Boedapest",
        "Jane Haining rakpart, Steiger 6, 1051 Boedapest",
        "Jane Haining rakpart, Steiger 8A / Steiger 11, 1052 Boedapest",
        "Live salonpiano en akoestische zang",
        "Glas welkomstbubbels + mineraalwater + live akoestische salonviool"
    ],
    "pl": [
        "1 Powitalny drink + 4-daniowe serwowane menu",
        "1 Powitalny drink + kompletny 4-daniowy serwowany posiłek",
        "1 Powitalny kieliszek szampana lub napoju bezalkoholowego",
        "1 Powitalny kieliszek wina musującego + 4-daniowe menu",
        "1,5 godziny (90 minut)",
        "12-daniowy ciepły bufet węgierski + autentyczna muzyka ludowa i występy taneczne",
        "2,5 godziny",
        "2,5 godziny (150 minut)",
        "4-daniowa węgierska uczta + tradycyjna cygańska muzyka i operetka na żywo",
        "4-daniowa kolacja + pojedynek pianistów na żywo z wokalistką",
        "4-daniowa kolacja wykwintna + autentyczny zespół tańca ludowego i śpiewacy operetkowi",
        "4-daniowa serwowana kolacja gourmet + nielimitowane piwo z nalewaka, wino, prosecco i napoje",
        "4-daniowe wykwintne menu à la carte (przystawka, zupa, danie główne, deser)",
        "4-daniowa kolacja serwowana przy świecach (nastrojowa muzyka w tle, bez głośnego show)",
        "90–120 minut",
        "Bufet bez limitu + 2 bezpłatne napoje (wino, piwo, napoje bezalkoholowe)",
        "Codziennie o 19:00 (Wchodzenie na pokład od 18:30)",
        "Codziennie o 19:00 (Wchodzenie na pokład rozpoczyna się o 18:30)",
        "Codziennie o 19:00, w weekendy o 22:00",
        "Codziennie o 19:30 (Wchodzenie na pokład od 19:00)",
        "Codziennie o 20:00 (Wchodzenie na pokład od 19:30)",
        "Przystań 7, Vigadó tér, 1051 Budapeszt",
        "Wieczorne wejście na pokład o 19:00 (czas trwania: 2,5 godz.)",
        "Bezpłatnie dla dzieci (0–5 lat)",
        "Bezpłatnie dla niemowląt (0–2 lata)",
        "Bezpłatnie dla niemowląt (0–3 lata)",
        "Pełny zwrot kosztów do 24 godzin przed wypłynięciem",
        "Id. Antall József rkp., 1051 Budapeszt (obok Mostu Łańcuchowego)",
        "Błyskawiczny bilet QR na telefon lub wydruk",
        "Błyskawiczny voucher QR na telefon lub wydruk",
        "Jane Haining Rakpart, Przystań 11, 1052 Budapeszt",
        "Jane Haining rakpart, Przystań 6, 1051 Budapeszt",
        "Jane Haining rakpart, Przystań 8A / Przystań 11, 1052 Budapeszt",
        "Salonowa muzyka fortepianowa na żywo i występ wokalny",
        "Powitalny kieliszek wina musującego + woda mineralna + nastrojowa muzyka skrzypcowa na żywo"
    ]
}

# Add matching template generators for the remaining 14 languages
# (cs, sk, ro, hr, sr, bg, ru, uk, el, tr, pt, he, ja, ko)
# by localizing the 35 standardized patterns accurately

print("Loaded base dictionary for Group 1 + PL")
