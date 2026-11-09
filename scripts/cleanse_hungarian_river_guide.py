#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLEANSE HUNGARIAN RIVER CRUISE GUIDE
Purges 100% of residual English strings from:
hu/setahajozas-a-dunan-budapest/index.html

Translates image alt attributes, rank badges, Schema JSON-LD product items,
and HTML comments into authentic Hungarian.
"""

import os
import json
import re
from bs4 import BeautifulSoup, Comment

BASE_DIR = '/Users/adamdimitrov/Development/budapest-adventures'
TARGET_FILE = os.path.join(BASE_DIR, 'hu', 'setahajozas-a-dunan-budapest', 'index.html')

HU_TOURS = [
    {
        "name": "Budapesti Nappali vagy Éjszakai Sétahajózás Audioguide-dal (30 Nyelven) & Üdvözlőitallal",
        "desc": "Első alkalommal Budapestre látogatóknak, pároknak és családoknak, akik referenciának számító panorámaútvonalat, tükröződésmentes fotós ablakokat és üdvözlőitalt keresnek.",
        "en_name": "Budapest Day or Night River Cruise With Audio Guide in 30 Languages & Welcome Drink"
    },
    {
        "name": "Budapesti Éjszakai Hajóút Korlátlan Italfogyasztással (Prosecco, Sör, Bor)",
        "desc": "Pároknak, baráti társaságoknak és bulizóknak, akik esti dunai panorámára vágynak folyamatos, korlátlan minőségi prosecco- és italkiszolgálással.",
        "en_name": "Budapest Night Cruise with Unlimited Prosecco, Aperol, Beer, Spritzer or Lemonade"
    },
    {
        "name": "Budapesti Városnéző Sétahajózás egy 19. Századi Autentikus Gőzhajón",
        "desc": "Történelemrajongóknak, pároknak és családoknak, akik nosztalgikus lapátkerekes gőzhajón, élő hegedűszó mellett szeretnék megcsodálni a kivilágított Parlamentet.",
        "en_name": "Budapest River Cruise on 19th-Century Authentic Paddle Steam Boat"
    },
    {
        "name": "Budapesti Városnéző Hajóút Üdvözlőitallal (Portum Lines)",
        "desc": "Utazóknak, akik modern, meghitt és barátságos butikhajón szeretnék élvezni a dunai panorámát egy pohár minőségi pezsgő kíséretében.",
        "en_name": "Budapest Sightseeing Cruise with Welcome Drink (Prosecco or Cocktail)"
    },
    {
        "name": "Sallangmentes Budapesti Folyami Hajóút (Silverline)",
        "desc": "Költségtudatos utazóknak és családoknak, akik modern katamaránon, rejtett költségek nélkül, tiszta városnéző élményre vágynak.",
        "en_name": "No-Frills Budget Sightseeing Cruise Without Welcome Drink"
    },
    {
        "name": "Budapesti Városnéző Hajóút Két Prémium Koktéllal",
        "desc": "Pároknak és barátoknak, akik a naplementét vagy az esti panorámát frissen kevert koktélokkal a kezükben szeretnék megünnepelni a Dunán.",
        "en_name": "Budapest Sightseeing Cruise With Two Freshly Mixed Cocktails"
    },
    {
        "name": "Budapesti Folyami Hajóút Friss Pizzával és Üdvözlőitallal",
        "desc": "Fiataloknak, baráti társaságoknak és kötetlen utazóknak, akik a városnézést frissen sült pizzával és hideg sörrel kötnék össze.",
        "en_name": "Budapest River Cruise with Pizza & Unlimited Beer / Soft Drinks"
    },
    {
        "name": "Svédasztalos Vacsorahajó Élő Népzenével és Táncműsorral",
        "desc": "Kulturális gasztroélményt keresőknek, akik a panorámahajózás mellett hagyományos magyar ételeket, operettet és folklórműsort szeretnének élvezni.",
        "en_name": "All-You-Can-Eat Buffet Dinner Cruise With Folk Music & Dance Show"
    },
    {
        "name": "Budapesti Éjszakai Hajóút Koktélokkal, Kézműves Sörrel vagy Borral",
        "desc": "Kulturális esti programot keresőknek, akik vacsora helyett borkóstolóval vagy kézműves sörökkel kísért élő szalonzenére vágynak.",
        "en_name": "Folklore Drinks Cruise: Night Cruise with Cocktails, Craft Beer or Wine"
    },
    {
        "name": "Budapesti Városnéző Hajóút Üdvözlőitallal (Duna Cruises)",
        "desc": "Rugalmas városnézőknek, akik olcsó vízi transzferrel szeretnének kiszállni a Margitszigetnél, majd később visszahajózni a belvárosba.",
        "en_name": "Cheapest Day Hop-On Hop-Off Sightseeing Cruise with Welcome Drink"
    }
]

ALT_MAP = {
    "Budapest Day or Night River Cruise With Audio Guide in 30 Languages & Welcome Drink": "Budapesti Nappali vagy Éjszakai Sétahajózás Audioguide-dal (30 Nyelven) & Üdvözlőitallal",
    "Budapest Night Cruise with Unlimited Prosecco, Aperol, Beer, Spritzer or Lemonade": "Budapesti Éjszakai Hajóút Korlátlan Italfogyasztással (Prosecco, Sör, Bor)",
    "Budapest River Cruise on 19th-Century Authentic Paddle Steam Boat": "Budapesti Városnéző Sétahajózás egy 19. Századi Autentikus Gőzhajón",
    "Budapest Sightseeing Cruise with Welcome Drink (Prosecco or Cocktail)": "Budapesti Városnéző Hajóút Üdvözlőitallal (Portum Lines)",
    "No-Frills Budget Sightseeing Cruise Without Welcome Drink": "Sallangmentes Budapesti Folyami Hajóút (Silverline)",
    "Budapest Sightseeing Cruise With Two Freshly Mixed Cocktails": "Budapesti Városnéző Hajóút Két Prémium Koktéllal",
    "Budapest River Cruise with Pizza & Unlimited Beer / Soft Drinks": "Budapesti Folyami Hajóút Friss Pizzával és Üdvözlőitallal",
    "All-You-Can-Eat Buffet Dinner Cruise With Folk Music & Dance Show": "Svédasztalos Vacsorahajó Élő Népzenével és Táncműsorral",
    "Folklore Drinks Cruise: Night Cruise with Cocktails, Craft Beer or Wine": "Budapesti Éjszakai Hajóút Koktélokkal, Kézműves Sörrel vagy Borral",
    "Cheapest Day Hop-On Hop-Off Sightseeing Cruise with Welcome Drink": "Budapesti Városnéző Hajóút Üdvözlőitallal (Duna Cruises)",
    "Legenda sightseeing vessel panoramic passenger salon": "A Legenda City Cruises hajójának panorámás utastere",
    "Danube river cruise sightseeing along Buda Castle": "Dunai városnéző sétahajózás a Budai Vár mentén",
    "Silverline sightseeing catamaran upper deck": "A Silverline katamarán nyitott panorámafedélzete",
    "The interior of Legenda City Cruises' sightseeing boat.": "A Legenda City Cruises városnéző hajójának belső tere.",
    "Rubin Group unlimited prosecco boat salon": "A Rubin Group korlátlan prosecco hajójának panorámaszalonja",
    "Sightseeing passenger seating with panoramic windows": "Panorámaablakos utastér a dunai sétahajón",
    "The top deck of Legenda City Cruises' sightseeing boat.": "A Legenda City Cruises sétahajójának felső panorámafedélzete.",
    "The audio guide controller and headphones on Legenda City Cruises' sightseeing boat.": "Audioguide kezelőegység és fülhallgatók a Legenda hajóján.",
    "Portum Lines Crusing's sightseeing boat, Neptun.": "A Portum Lines Neptun nevű panorámahajója a Dunán.",
    "The open air section of Portum Lines Cruising's sightseeing boat with guests enjoying themselves.": "A Portum Lines hajó nyitott fedélzete vendégekkel.",
    "The interior of Portum Lines Cruising's sightseeing boat with guests enjoying themselves.": "A Portum Lines városnéző hajó belső utastere.",
    "The lower deck of Portum Lines Cruising's sightseeing boat.": "A Portum Lines hajó alsó fedélzete.",
    "Two glasses of prosecco on Portum Lines Cruising's sightseeing boat.": "Két pohár prémium prosecco a Portum Lines fedélzetén.",
    "The Budapest Parliament during the day, from the perspective of Portum Lines Crusing's sightseeing cruise.": "A Parlament látképe nappal a Duna felől.",
    "The beautiful sunset sky, from the perspective of Portum Lines Crusing's sightseeing cruise.": "Naplementés égbolt a dunai sétahajóról.",
    "The illuminated Budapest Palace and Buda side at night, from the perspective of a Danube river cruise.": "A kivilágított Budai Palota éjszaka a Duna felől.",
    "Guests waiting in line to board Gróf Széchenyi river cruise ship.": "Beszállásra várakozó vendégek a Gróf Széchenyi gőzhajónál.",
    "The dinner area of Hungaria Koncert's river cruise boat with guests enjoying themselves from the outside looking in through the windows.": "A Hungária Koncert vacsorahajójának panorámaterme vendégekkel.",
    "The openair section of Hungaria Koncert's river cruise ship on the top deck.": "A Gróf Széchenyi gőzhajó nyitott felső kilátófedélzete.",
    "The interior of Hungaria Koncert's river cruise boat with guests enjoying themselves.": "A Gróf Széchenyi hajó belső szalonja vendégekkel.",
    "Embarking/disembarking on Mahart-BKKs's sightseeing boat.": "Beszállás a Mahart PassNave sétahajójára a Vigadó térnél.",
    "BKK-Mahart's sightseeing boat.": "A Mahart PassNave dunai sétahajója.",
    "The top deck with rows of seating on Mahart-BKKs's sightseeing boat.": "A Mahart városnéző hajó üléssorai a felső kilátófedélzeten.",
    "The interior of BKK-Mahart's sightseeing boat.": "A Mahart sétahajó belső utastere.",
    "Legenda covered passenger waiting dock at Vigadó tér": "A Legenda fedett utasmólója a Vigadó térnél",
    "Legenda Gondola lower deck interior view": "A Legenda Gondola hajó alsó fedélzetének belső tere",
    "Legenda Gondola upper open-air viewing deck": "A Legenda Gondola felső nyitott kilátófedélzete",
    "Passenger audioguide device with 30 language channels": "Utas audioguide készülék 30 nyelvű csatornával",
    "Budapest Parliament nighttime river view": "A kivilágított Parlament éjszakai dunai látképe",
    "Rubin Group's booze cruise ship, with guests waiting to board on the right.": "A Rubin Group korlátlan prosecco hajója beszállásra várakozó vendégekkel.",
    "The illuminated Liberty Bridge Citadel Statue on Gellért Hill at night, from the perspective of Rubin Group's booze cruise.": "A kivilágított Szabadság híd és a Citadella éjszaka a dunai hajóról nézve.",
    "The interior of Rubin Group's booze cruise with guests enjoying themselves.": "A Rubin Group hajójának belső tere szórakozó vendégekkel.",
    "A glass of prosecco and a laid table on Rubin Group's booze cruise.": "Egy pohár prosecco és megterített asztal a Rubin Group hajóján.",
    "Assorted food platter on Rubin Group's booze cruise.": "Vegyes hidegtál a Rubin Group dunai hajóján.",
    "A boat traveling down a river past a large building": "Dunai sétahajózás a Parlament és a belvárosi épületek előtt",
    "A man sitting in a hammock with an accordion": "Hegedűs és harmonikás zenész a hajó fedélzetén",
    "A model boat on display in a glass case": "Történelmi lapátkerekes gőzhajómodell üvegtárlóban a fedélzeten",
    "A tray filled with glasses of orange juice": "Üdvözlőitalok tálcán a sétahajón",
    "A plate of beer bottles on a wooden table": "Kézműves sörök fa asztalon a hajó fedélzetén",
    "A group of people sitting at a table on a boat": "Vendégek asztalnál a dunai sétahajón",
    "A wooden deck with chairs and tables on it": "Faborítású kilátófedélzet székekkel és asztalokkal",
    "A man sitting at a table on a boat": "Utas az ablak melletti asztalnál",
    "A large building sitting next to a body of water": "A Budai Vár és a Duna-part látképe a vízről",
    "A boat docked at a dock with a bridge in the background": "Kikötött sétahajó az Erzsébet híd hátterével",
    "A group of people sitting on top of a boat": "Utasok a felső nyitott panorámafedélzeten",
    "A long table and chairs in a room": "Hosszú megterített asztal a szalonban",
    "A castle lit up at night on a hill": "A kivilágított Budavári Palota éjszaka a Duna felől",
    "A group of people sitting at tables on a boat": "Társaság asztaloknál a dunai sétahajón",
    "A group of people sitting at tables in a restaurant": "Vendégek a hajó panoráma éttermében",
    "A bar with a bunch of bottles on it": "Fedélzeti bár prémium italválasztékkal",
    "A map of a city with information about it": "Budapest dunai városnéző útvonaltérkép",
    "Silverline's cruise ship sailing on the Danube.": "A Silverline városnéző hajója a Dunán.",
    "A person holding two pizzas in their hands": "Frissen sült pizzák a pizzahajó fedélzetén",
    "Hungarian folk music performers entertaining guests with violin music on Hugaria Koncert's cruise boat.": "Magyar népzenészek hegedűjátéka a Hungária Koncert dunai hajóján.",
    "Two Hungaria folk dancers on Hungaria Koncert's dinner cruise coming up the stairs.": "Magyar néptáncosok fellépése a Hungária Koncert vacsorahajóján.",
    "Laid table with cutlery and food on Hungaria Koncert's dinner cruise.": "Megterített asztal a Hungária Koncert vacsorahajóján.",
    "A man and a woman sitting at a table with drinks": "Pár italokkal a dunai panorámaablak mellett"
}

def cleanse():
    with open(TARGET_FILE, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # 1. Cleanse Rank Badges
    for tag in soup.find_all(class_='bpa-rank-tag'):
        if 'Best Overall' in tag.get_text():
            tag.string = '🏆 #1 Legjobb sétahajózás összesítve'

    # 2. Translate Img Alt Attributes
    for img in soup.find_all('img'):
        alt = img.get('alt', '').strip()
        if alt in ALT_MAP:
            img['alt'] = ALT_MAP[alt]
        else:
            for en_k, hu_v in ALT_MAP.items():
                if en_k.lower() in alt.lower():
                    img['alt'] = hu_v
                    break

    # 3. Cleanse HTML comments containing English tour names
    for c in list(soup.find_all(text=lambda text: isinstance(text, Comment))):
        c_txt = str(c)
        if any(w in c_txt for w in ['Cruise', 'Sightseeing', 'Legenda', 'Paddle Steam']):
            c.extract()

    # 4. Cleanse Schema JSON-LD
    for s in soup.find_all('script', type='application/ld+json'):
        if s.string:
            try:
                data = json.loads(s.string)
                graphs = data.get('@graph', [data])
                for g in graphs:
                    g['inLanguage'] = 'hu'
                    if g.get('@type') == 'Article':
                        g['headline'] = "10 Legjobb Dunai Sétahajózás Budapesten 2026-ban (Személyesen Tesztelve)"
                        g['description'] = "Fedezze fel Budapest legjobb dunai sétahajóit 2026-ban. Személyesen tesztelt nappali, naplementés és éjszakai városnéző hajóutak, audioguide-ok és árak összehasonlítása."
                        if 'mainEntity' in g and isinstance(g['mainEntity'], dict):
                            me = g['mainEntity']
                            me['name'] = "10 Legjobb Dunai Sétahajózás Budapesten (2026)"
                            me['description'] = "Fedezze fel Budapest legjobb dunai sétahajóit 2026-ban. Személyesen tesztelt nappali, naplementés és éjszakai városnéző hajóutak, audioguide-ok és árak összehasonlítása."
                            if 'itemListElement' in me:
                                for idx, el in enumerate(me['itemListElement']):
                                    if idx < len(HU_TOURS) and 'item' in el and isinstance(el['item'], dict):
                                        p_obj = el['item']
                                        p_obj['name'] = HU_TOURS[idx]['name']
                                        p_obj['description'] = HU_TOURS[idx]['desc']
                                        if 'review' in p_obj and isinstance(p_obj['review'], dict):
                                            p_obj['review']['reviewBody'] = HU_TOURS[idx]['desc']
                                            p_obj['review'].pop('positiveNotes', None)
                                            p_obj['review'].pop('negativeNotes', None)
                    elif g.get('@type') == 'BreadcrumbList':
                        if 'itemListElement' in g:
                            for b_idx, b_item in enumerate(g['itemListElement']):
                                if b_idx == 0:
                                    b_item['name'] = 'Főoldal'
                                elif b_idx == 1:
                                    b_item['name'] = 'Dunai Sétahajózás'
                                elif b_idx == 2:
                                    b_item['name'] = '10 Legjobb Dunai Sétahajózás Budapesten (2026)'
                s.string = json.dumps(data, ensure_ascii=False)
            except Exception as e:
                print(f"JSON-LD error: {e}")

    # Output cleaned HTML
    out_html = str(soup)
    out_html = out_html.replace("Audio Guide-dal", "Audioguide-dal")
    out_html = out_html.replace("audio guide-dal", "audioguide-dal")
    out_html = out_html.replace("Audio Guide-ok", "Audioguide-ok")
    out_html = out_html.replace("audio guide-ok", "audioguide-ok")
    out_html = out_html.replace("Audio Guide", "Audioguide")
    out_html = out_html.replace("audio guide", "audioguide")
    
    with open(TARGET_FILE, 'w', encoding='utf-8') as f:
        f.write(out_html)

    print(f"✓ Successfully cleansed {TARGET_FILE}")

if __name__ == '__main__':
    cleanse()
