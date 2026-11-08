#!/usr/bin/env python3
"""
MASTER BUDAPEST CARD COMPILER ACROSS ALL 22 LANGUAGES — BUDAPEST ADVENTURES
Compiles modern Luxury Editorial System architecture for Budapest Card pages:
- Hungarian: /hu/budapest-card-megéri-e, /hu/budapest-card-megeri-e, /hu/budapest-card-is-it-worth-it
- All 20 international languages: /{lang}/budapest-card-is-it-worth-it/index.html

Replaces legacy Webflow iframe harvest dump with native vanilla JS calculator,
standardized Plus Jakarta Sans navbar/footer, 100% affiliate tracking link preservation
(Legenda partner=38585, GetYourGuide partner_id=YS414AJ), and 22-language hreflang parity.
"""

import os
import re
import json
from bs4 import BeautifulSoup

BASE_DIR = '/Users/adamdimitrov/Development/budapest-adventures'

# Load canonical EN card page as template base
with open(os.path.join(BASE_DIR, 'budapest-card-is-it-worth-it.html'), 'r', encoding='utf-8') as f:
    en_html = f.read()

# 22 canonical language paths for hreflang
LANG_HREFLANGS = [
    ("en-us", "https://www.budapestadventures.com/budapest-card-is-it-worth-it"),
    ("hu", "https://www.budapestadventures.com/hu/budapest-card-megéri-e"),
    ("de", "https://www.budapestadventures.com/de/budapest-card-is-it-worth-it"),
    ("fr", "https://www.budapestadventures.com/fr/budapest-card-is-it-worth-it"),
    ("es", "https://www.budapestadventures.com/es/budapest-card-is-it-worth-it"),
    ("it", "https://www.budapestadventures.com/it/budapest-card-is-it-worth-it"),
    ("nl", "https://www.budapestadventures.com/nl/budapest-card-is-it-worth-it"),
    ("pl", "https://www.budapestadventures.com/pl/budapest-card-is-it-worth-it"),
    ("pt", "https://www.budapestadventures.com/pt/budapest-card-is-it-worth-it"),
    ("ro", "https://www.budapestadventures.com/ro/budapest-card-is-it-worth-it"),
    ("ru", "https://www.budapestadventures.com/ru/budapest-card-is-it-worth-it"),
    ("sk", "https://www.budapestadventures.com/sk/budapest-card-is-it-worth-it"),
    ("cs", "https://www.budapestadventures.com/cs/budapest-card-is-it-worth-it"),
    ("bg", "https://www.budapestadventures.com/bg/budapest-card-is-it-worth-it"),
    ("hr", "https://www.budapestadventures.com/hr/budapest-card-is-it-worth-it"),
    ("sr", "https://www.budapestadventures.com/sr/budapest-card-is-it-worth-it"),
    ("uk", "https://www.budapestadventures.com/uk/budapest-card-is-it-worth-it"),
    ("el", "https://www.budapestadventures.com/el/budapest-card-is-it-worth-it"),
    ("tr", "https://www.budapestadventures.com/tr/budapest-card-is-it-worth-it"),
    ("ja", "https://www.budapestadventures.com/ja/budapest-card-is-it-worth-it"),
    ("ko", "https://www.budapestadventures.com/ko/budapest-card-is-it-worth-it"),
    ("he", "https://www.budapestadventures.com/he/budapest-card-is-it-worth-it"),
    ("x-default", "https://www.budapestadventures.com/budapest-card-is-it-worth-it")
]

# Hungarian translation map for 94 sights
HU_ATTRACTION_NAMES = {
    "BKK public transport": "BKK korlátlan tömegközlekedés (metró, villamos, busz)",
    "Airport transfer with miniBUD": "miniBUD közvetlen repülőtéri transzfer",
    "Universal airporthub": "Universal Airport Hub csomagmegőrző",
    "Historic Vehicles (Vintage Tram Rides Day Ticket)": "BKV Nosztalgiajáratok (Nosztalgia villamos napijegy)",
    "Zugliget chairlift": "Zugligeti Libegő (oda-vissza)",
    "Official Budapest castle bus": "Hivatalos Budavári elektromos kisbusz",
    "Walking tour Buda": "Vezetett gyalogtúra a Várnegyedben (Buda)",
    "Walking tour Pest": "Vezetett történelmi gyalogtúra (Pest)",
    "Bike & relax Budapest bicycle tours": "Bike & Relax kerékpáros városnéző túra",
    "Budapest bike rental – Amigo shop": "Kerékpárbérlés – Amigo Shop",
    "Bike carriage (Bringóhintó)": "Bringóhintó kölcsönzés (Margitsziget)",
    "Eurama sightseeing tours": "Eurama panoráma városnéző túrák",
    "Sisi tour & Gödöllő palace": "Sisi túra & Gödöllői Királyi Kastély",
    "Avalon rent a car(e)": "Avalon Rent a Car autóbérlés",
    "Jewish heritage tours": "Zsidó örökség és gettó túrák",
    "Hop-on hop-off bus tour": "Hop-On Hop-Off városnéző busz",
    "Legenda City Cruises": "Legenda Városnéző Hajózás (Vigadó tér 7-es móló)",
    "Day sightseeing cruise (Legenda)": "Duna Bella nappali sétahajózás fülhallgatóval (Legenda)",
    "Evening cruise (Legenda)": "Danube Legend esti kivilágított sétahajózás (Legenda)",
    "River boat service (BKV)": "BKV dunai átkelőhajó járatok",
    "Evening river cruise (BP Sightseeing)": "Esti dunai panoráma sétahajózás",
    "St. Lukács thermal bath and swimming pool": "Szent Lukács Gyógyfürdő és Uszoda",
    "Széchenyi thermal bath and swimming pool": "Széchenyi Gyógyfürdő és Uszoda",
    "Rudas thermal bath and swimming pool": "Rudas Gyógyfürdő és Uszoda",
    "Palatinus thermal bath, public and wave pool": "Palatinus Gyógy-, Strand- és Hullámfürdő",
    "Római bath": "Római Strandfürdő",
    "Aquaworld resort Budapest": "Aquaworld Resort Budapest Élményfürdő",
    "Lupa beach": "Lupa Beach tengerparti strand",
    "Hungarian national museum": "Magyar Nemzeti Múzeum",
    "Hungarian national gallery": "Magyar Nemzeti Galéria (Budavári Palota)",
    "Budapest history museum - Castle museum": "Budapesti Történeti Múzeum – Vármúzeum",
    "Saint Stephen's hall": "Szent István-terem (Budavári Palota)",
    "Museum of fine arts": "Szépművészeti Múzeum (Hősök tere)",
    "Kunsthalle Budapest (Műcsarnok)": "Műcsarnok (Hősök tere)",
    "Budapest history museum - Aquincum museum": "Aquincumi Múzeum és Régészeti Park",
    "Budapest history museum - Kiscell museum": "Kiscelli Múzeum – Fővárosi Képtár",
    "Budapest history museum - Budapest gallery": "Budapest Galéria",
    "Budapest history museum - Medieval Jewish prayer house": "Középkori Zsidó Imaház (Buda)",
    "Ludwig museum – Museum of contemporary art": "Ludwig Múzeum – Kortárs Művészeti Múzeum",
    "Robert Capa contemporary photography center": "Robert Capa Kortárs Fotográfiai Központ",
    "Hungarian house of photography - Mai Manó house": "Magyar Fotográfusok Háza – Mai Manó Ház",
    "Vasarely museum Budapest": "Vasarely Múzeum Budapest",
    "Memento park - The statue park": "Memento Park – Szoborpark",
    "Hungarian museum of trade and tourism": "Magyar Kereskedelmi és Vendéglátóipari Múzeum",
    "Ferenc Hopp museum of Asiatic arts": "Hopp Ferenc Ázsiai Művészeti Múzeum",
    "Underground railway museum": "Földalatti Vasúti Múzeum (Deák tér)",
    "Museum of Óbuda": "Óbudai Múzeum",
    "Goldberger textile industry collection": "Goldberger Textilipari Gyűjtemény",
    "Budatower - The Mary Magdalene tower": "BudaTower – Mária Magdolna-torony",
    "Margaret island water tower and panoramic lookout tower": "Margitszigeti Víztorony és Panoráma Kilátó",
    "Guided tours at the Pesti Vigadó": "Vezetett épületséta a Pesti Vigadóban",
    "Museum Fradi": "Fradi Múzeum (Groupama Aréna)",
    "Museum of ethnography": "Néprajzi Múzeum (Városliget)",
    "Hospital in the rock – Nuclear bunker museum": "Sziklakórház Atombunker Múzeum",
    "Szamos chocolate museum": "Szamos Csokoládé Múzeum (Kossuth tér)",
    "St. Stephen's basilica": "Szent István-bazilika & Kilátó",
    "The main parish church of the assumption in downtown": "Belvárosi Nagyboldogasszony Főplébániatemplom",
    "Gödöllő royal palace": "Gödöllői Királyi Kastély",
    "Museum of illusion": "Illúziók Múzeuma Budapest",
    "Light art museum": "Light Art Museum (LAM)",
    "Cinema mystica": "Cinema Mystica fényművészeti kiállítás",
    "House of Hungarian music": "Magyar Zene Háza (Városliget)",
    "Synagogue in Kazinczy street": "Kazinczy utcai Ortodox Zsinagóga",
    "Dohány street synagogue": "Dohány utcai Zsinagóga",
    "Hungarian Jewish museum and archives": "Magyar Zsidó Múzeum és Levéltár",
    "Pálvölgyi cave": "Pál-völgyi-barlang túra",
    "Organ concert in St. Stephen's basilica": "Orgonakoncert a Szent István-bazilikában",
    "Budapest zoo & botanical garden": "Fővárosi Állat- és Növénykert",
    "House of Unicum": "Zwack Unicum Ház és Múzeum",
    "Exhibitions at the Pesti Vigadó": "Pesti Vigadó időszaki kiállítások",
    "Madame Tussauds Budapest": "Madame Tussauds Budapest panoptikum",
    "Timetrap exit game": "Időcsapda Szabadulószoba",
    "Ferris wheel of Budapest with champagne": "Budapest Eye Óriáskerék pezsgővel",
    "Tropicarium - The shark zoo": "Tropicarium – A cápás állatkert",
    "City park boating lake": "Városligeti Csónakázótó",
    "Premier outlet Budapest": "Premier Outlet Budapest (Biatorbágy)",
    "Gastrocellar": "Gastrocellar borkóstoló pince",
    "Champion wines vinarium & gastro boutique": "Champion Wines Borászat és Gasztro Butik",
    "Molnár's kürtőskalács": "Molnár's Kürtőskalács Kávézó",
    "Parisi passage restaurant experience": "Párisi Passage Café & Étterem",
    "Halászbástya restaurant": "Halászbástya Étterem (Panoráma terasz)",
    "Zsolnay café": "Zsolnay Kávéház (Radisson Blu Béke)",
    "Lángos in the heart of the city": "Lángos a Belváros Szívében",
    "Bonnie restro comics": "Bonnie Restro Comics & Bar",
    "Yellow bistro & bar": "Yellow Bistro & Bar",
    "Café Astoria restaurant": "Café Astoria Restaurant",
    "Láng bistro & grill restaurant": "Láng Bistro & Grill (Hilton Budapest)",
    "Csíki beer bar & restaurant": "Csíki Söröző és Étterem",
    "Bamba marha burger bar": "Bamba Marha Burger Bár",
    "Beerselection craft beer store & bar": "Beerselection Kézműves Sörszaküzlet és Bár",
    "Tati farm to table restaurant": "Tati Farm to Table Étterem",
    "Hard rock cafe": "Hard Rock Cafe Budapest",
    "Solid restaurant": "Solid Rooftop Borétterem",
    "Hősök bistro": "Hősök Bisztró (Városliget)"
}

def extract_meta_tags(lang):
    path = os.path.join(BASE_DIR, f"{lang}/budapest-card-is-it-worth-it/index.html")
    if lang == 'hu':
        path = os.path.join(BASE_DIR, "hu/budapest-card-megéri-e/index.html")
    title = ""
    desc = ""
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        if soup.title and soup.title.string:
            title = soup.title.string.strip()
        desc_el = soup.find('meta', attrs={'name': 'description'})
        if desc_el and desc_el.get('content'):
            desc = desc_el['content'].strip()
    title = title.replace('2025', '2026')
    desc = desc.replace('2025', '2026')
    return title, desc

def build_hungarian_pages():
    print("--- COMPILING HUNGARIAN BUDAPEST CARD PAGES ---")
    soup = BeautifulSoup(en_html, 'html.parser')
    soup.html['lang'] = 'hu'
    
    # 1. Meta tags
    soup.title.string = "Budapest Kártya: Valóban Megéri 2026-ban? Interaktív Értékkalkulátor (Mind a 94 Látnivaló)"
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc:
        meta_desc['content'] = "Számolja ki pontosan, megéri-e Önnek a Budapest Kártya! Interaktív kalkulátorunk összehasonlítja mind a 94 hivatalos budapesti látnivalót, fürdőt, múzeumot és dunai hajót a 2026-os árakkal."
    canonical = soup.find('link', rel='canonical')
    if canonical:
        canonical['href'] = "https://www.budapestadventures.com/hu/budapest-card-megéri-e"
        
    for h in soup.find_all('link', rel='alternate'):
        h.decompose()
    for hlang, hhref in LANG_HREFLANGS:
        soup.head.append(soup.new_tag('link', rel='alternate', hreflang=hlang, href=hhref))
        
    # 2. Extract Canonical Hungarian Header, Drawer, Footer
    with open(os.path.join(BASE_DIR, 'hu/index.html'), 'r', encoding='utf-8') as f:
        hu_home_soup = BeautifulSoup(f.read(), 'html.parser')
        
    hu_navbar = hu_home_soup.find('header', class_='ltt-navbar')
    hu_drawer = hu_home_soup.find('div', class_='ltt-mobile-drawer')
    hu_footer = hu_home_soup.find('footer', class_='footer-dark')
    
    for a in hu_navbar.find_all('a', class_='ltt-nav-link'):
        href = a.get('href', '')
        if 'budapest-card' in href or 'megéri' in href or 'megeri' in href:
            a['class'] = ['ltt-nav-link', 'active']
            a['aria-current'] = 'page'
        else:
            a['class'] = ['ltt-nav-link']
            if 'aria-current' in a.attrs: del a['aria-current']

    if hu_drawer:
        for a in hu_drawer.find_all('a', class_='ltt-mobile-link'):
            href = a.get('href', '')
            if 'budapest-card' in href or 'megéri' in href or 'megeri' in href:
                a['class'] = ['ltt-mobile-link', 'active']
                a['aria-current'] = 'page'
            else:
                a['class'] = ['ltt-mobile-link']
                if 'aria-current' in a.attrs: del a['aria-current']
                
    old_nav = soup.find('header', class_='ltt-navbar')
    if old_nav and hu_navbar: old_nav.replace_with(hu_navbar)
    old_drawer = soup.find('div', class_='ltt-mobile-drawer')
    if old_drawer and hu_drawer: old_drawer.replace_with(hu_drawer)
    old_footer = soup.find('footer', class_='footer-dark')
    if old_footer and hu_footer: old_footer.replace_with(hu_footer)
    
    # 3. Breadcrumbs
    bc = soup.find('nav', class_='breadcrumbs')
    if bc:
        bc.clear()
        bc.append(BeautifulSoup('<a href="/hu/">Kezdőlap</a> › <a href="/hu/">Utazási Útmutatók</a> › <span>Budapest Kártya Elemzés & Értékkalkulátor</span>', 'html.parser'))
        
    # 4. Hero
    hero = soup.find('section', class_='article-hero')
    if hero:
        h1 = hero.find('h1')
        if h1:
            h1.clear()
            h1.append(BeautifulSoup('Budapest Kártya: <span>Valóban Megéri 2026-ban?</span> (Részletes Értékkalkulátor & Őszinte Elemzés)', 'html.parser'))
        meta_bar = hero.find('div', class_='meta-bar')
        if meta_bar:
            meta_bar.clear()
            meta_bar.append(BeautifulSoup('''
              <span class="badge-pill">Szerkesztőségi Elemzés</span>
              <span>Szerző: <strong>Adam Dimitrov</strong> (Budapest Adventures)</span>
              <span>•</span>
              <span>Frissítve: <strong>2026. november 6.</strong></span>
              <span>•</span>
              <span>⚡ Mind a 94 Hivatalos Látnivaló Tesztelve</span>
            ''', 'html.parser'))
            
    # 5. Verdict
    verdict = soup.find('section', class_='verdict-callout')
    if verdict:
        kicker = verdict.find('div', class_='verdict-kicker')
        if kicker: kicker.string = "⚖️ Az Őszinte Ítélet"
        v_title = verdict.find('h2', class_='verdict-title')
        if v_title: v_title.string = "Teljesen a látogatási tempótól függ. Óriási megtakarítás múzeumkedvelőknek, de gyenge értékajánlat, ha csak a főbb nevezetességek érdeklik."
        v_body = verdict.find('p', class_='verdict-body')
        if v_body:
            v_body.clear()
            v_body.append(BeautifulSoup('''A hivatalos Budapest Kártya korlátlan BKK tömegközlekedést és ingyenes belépést biztosít több mint 30 fővárosi múzeumba, galériába, valamint a Szent Lukács Gyógyfürdőbe. Ugyanakkor a legnépszerűbb élmények – mint a <strong>Magyar Országház</strong>, a <strong>Széchenyi Fürdő</strong>, vagy a <strong>kivilágított esti dunai sétahajózások</strong> – vagy teljesen kimaradnak a csomagból, vagy mindössze 20% kedvezmény jár rájuk.''', 'html.parser'))
            
        for box in verdict.find_all('div', recursive=True):
            t = box.get_text()
            if "When The Card IS Worth It" in t or "Mikor ÉRI MEG" in t:
                box.clear()
                box.append(BeautifulSoup('''
                  <div style="font-size: 13px; font-weight: 800; color: #15803d; text-transform: uppercase; margin-bottom: 6px;">✓ Mikor ÉRI MEG a Budapest Kártya</div>
                  <ul style="font-size: 13px; color: #166534; line-height: 1.5; padding-left: 18px;">
                    <li>3+ nagy múzeum meglátogatása (Nemzeti Galéria, Szépművészeti, Nemzeti Múzeum)</li>
                    <li>Metró, történelmi 2-es villamos és buszok napi aktív használata</li>
                    <li>Feltöltődés a Szent Lukács Gyógyfürdőben (100% ingyenes belépő)</li>
                    <li>Egyetlen kényelmes digitális bérlet a telefonon fizikai jegyvásárlás helyett</li>
                  </ul>
                ''', 'html.parser'))
            elif "When To Skip The Card" in t or "Mikor ÉRDEMES KIHAGYNI" in t:
                box.clear()
                box.append(BeautifulSoup('''
                  <div style="font-size: 13px; font-weight: 800; color: #be123c; text-transform: uppercase; margin-bottom: 6px;">✕ Mikor ÉRDEMES KIHAGYNI a Kártyát</div>
                  <ul style="font-size: 13px; color: #9f1239; line-height: 1.5; padding-left: 18px;">
                    <li>A fő cél a Magyar Országház (0% kedvezmény, külön kell jegyet váltani)</li>
                    <li>A Széchenyi Fürdő a terv (csak 20% kedvezmény a magas alapárból)</li>
                    <li>Esti kivilágított sétahajózásra vágyik (a kártya csak nappali átkelőhajót fedez)</li>
                    <li>Gyalogosan szeret felfedezni, vagy napi 1-2 villamosozást tervez csupán</li>
                  </ul>
                ''', 'html.parser'))

    # 6. Calculator Header & Summary Aside
    calc_sec = soup.find('section', id='calculator')
    if calc_sec:
        tag = calc_sec.find('div', class_='calc-tag')
        if tag: tag.string = "Interaktív Értékszimulátor"
        title = calc_sec.find('h2', class_='calc-title')
        if title: title.string = "Tesztelje Saját Útitervét (Mind a 94 Hivatalos Látnivaló)"
        desc = calc_sec.find('p', class_='calc-desc')
        if desc: desc.string = "Válassza ki a tervezett időtartamot, és jelölje be azokat a látnivalókat, amelyeket valóban fel szeretne keresni. A kalkulátor a hivatalos felnőtt jegyárak alapján kiszámolja, hogy a kártyával valóban spórol-e, vagy felesleges pénzkidobás."
        
        dur_label = calc_sec.find('div', class_='duration-label')
        if dur_label:
            span_text = dur_label.find('span')
            if span_text: span_text.string = "1. Válassza ki a Budapest Kártya érvényességét:"
            gyg_link = dur_label.find('a')
            if gyg_link: gyg_link.string = "Budapest Kártya hivatalos elérhetőség a GYG-n →"
            
        search_input = calc_sec.find('input', id='searchInput')
        if search_input:
            search_input['placeholder'] = "Keresés 94 látnivaló között (pl. Széchenyi, Legenda, Vár, Parlament)..."
            
        preset_std = calc_sec.find('button', id='presetStandard')
        if preset_std: preset_std.string = "★ Első Látogatás (3 Nap)"
        preset_mus = calc_sec.find('button', id='presetMuseum')
        if preset_mus: preset_mus.string = "🏛️ Múzeum Maraton"
        preset_clr = calc_sec.find('button', id='presetClear')
        if preset_clr: preset_clr.string = "✕ Törlés"
        
        # Set HUF active in currency toggle
        curr_eur = calc_sec.find('button', id='currEur')
        curr_huf = calc_sec.find('button', id='currHuf')
        if curr_eur and curr_huf:
            curr_eur['class'] = ['curr-btn']
            curr_huf['class'] = ['curr-btn', 'active']
            
        # Summary widget strings
        sum_widget = calc_sec.find('aside', class_='summary-widget')
        if sum_widget:
            sum_title = sum_widget.find('div', class_='summary-title')
            if sum_title:
                tspan = sum_title.find('span')
                if tspan: tspan.string = "Az Ön Tervezett Útitervje"
            
            rows = sum_widget.find_all('div', class_='summary-row')
            for r in rows:
                span_lbl = r.find('span')
                if span_lbl:
                    lbl = span_lbl.get_text().strip()
                    if "Card Price:" in lbl: span_lbl.string = "Kártya ára:"
                    elif "Attractions Value:" in lbl: span_lbl.string = "Egyedi jegyek összértéke:"
                    elif "Card Savings Value:" in lbl: span_lbl.string = "Kártyás megtakarítás:"
                    elif "Net Financial Balance:" in lbl: span_lbl.string = "Nettó Pénzügyi Egyenleg:"

    # 7. Booking Options
    bundle = soup.find('section', id='booking-options')
    if bundle:
        kicker = bundle.find('div', class_='bundle-kicker')
        if kicker: kicker.string = "Utazástervezési Kalauz"
        b_title = bundle.find('h2', class_='bundle-title')
        if b_title: b_title.string = "Hivatalos Városkártya vs. Egyéni Foglalás: Melyik illik Önhöz?"
        b_desc = bundle.find('p', class_='bundle-desc')
        if b_desc: b_desc.string = "A Budapestre utazók két jól elkülönülő útvonal közül választhatnak a prioritásaik alapján. Íme a két opció a gyakorlatban:"
        
        bundle_cards_container = bundle.find('div', style=lambda s: s and 'grid-template-columns' in s)
        if bundle_cards_container:
            bundle_cards_container.clear()
            bundle_cards_container.append(BeautifulSoup('''
              <div style="background: #f8fafc; border: 1.5px solid #cbd5e1; border-radius: 12px; padding: 24px; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                  <div style="font-size: 11px; font-weight: 800; color: #15803d; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px;">A Opció • A Hivatalos All-Inclusive Bérlet</div>
                  <h3 style="font-family: var(--font-heading); font-size: 20px; color: #0f172a; margin-bottom: 10px;">Hivatalos Budapest Kártya</h3>
                  <p style="font-size: 13.5px; color: #475569; line-height: 1.55; margin-bottom: 16px;">
                    Ideális, ha szereti a történelmet és múzeumokat, és egyetlen kényelmes digitális bérletre vágyik. Korlátlan BKK tömegközlekedést (metrók, villamosok, buszok), ingyenes belépést több mint 30 fővárosi múzeumba (Nemzeti Galéria, Szépművészeti, Nemzeti Múzeum), Lukács Fürdő belépőt és vezetett sétákat tartalmaz.
                  </p>
                  <ul style="font-size: 13px; color: #334155; line-height: 1.6; margin-bottom: 20px; padding-left: 18px;">
                    <li><strong>Tartalmazza:</strong> Korlátlan 24h, 48h vagy 72h BKK tömegközlekedés</li>
                    <li><strong>Tartalmazza:</strong> 30+ fővárosi múzeum és galéria díjmentesen</li>
                    <li><strong>Tartalmazza:</strong> Szent Lukács Gyógyfürdő és Budavári kisbusz</li>
                    <li><strong>Nem tartalmazza:</strong> Országház és Széchenyi (csak 20% kedvezmény)</li>
                  </ul>
                </div>
                <div>
                  <div style="font-size: 16px; font-weight: 700; color: #0f172a; margin-bottom: 12px;">39 € (24h) és 69 € (72h) között</div>
                  <a href="https://www.getyourguide.com/budapest-card-t187335/?partner_id=YS414AJ&utm_medium=online_publisher&cmp=budapest-card-review&mkt_cmp=true" target="_blank" rel="noopener sponsored" class="b-btn" style="background: #0f172a; display: block; text-align: center; color: #fff; padding: 12px 18px; border-radius: 8px; font-weight: 700; text-decoration: none;">Budapest Kártya Foglalása a GYG-n →</a>
                </div>
              </div>

              <div style="background: #ffffff; border: 2px solid #0f172a; border-radius: 12px; padding: 24px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 4px 16px rgba(0,0,0,0.06);">
                <div>
                  <div style="font-size: 11px; font-weight: 800; color: #d97706; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px;">B Opció • A Szabad Útiterv (Szerkesztői Ajánlás)</div>
                  <h3 style="font-family: var(--font-heading); font-size: 20px; color: #0f172a; margin-bottom: 10px;">BKK Bérlet + Egyedi Prémium Jegyek</h3>
                  <p style="font-size: 13.5px; color: #475569; line-height: 1.55; margin-bottom: 16px;">
                    A legtöbb látogató számára pénzügyileg jóval kedvezőbb megoldás. Vásároljon egy hivatalos 72 órás BKK Budapest-bérletet a BudapestGO appban mindössze 5 500 Ft-ért (~14 €), és foglalja le a prémium élményeket közvetlenül a hivatalos partnereknél:
                  </p>
                  <div style="display: flex; flex-direction: column; gap: 10px; margin-bottom: 20px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; background: #f8fafc; padding: 10px 14px; border-radius: 6px; border: 1px solid #e2e8f0;">
                      <div>
                        <div style="font-size: 13px; font-weight: 700; color: #0f172a;">Legenda Esti Kivilágított Hajózás</div>
                        <div style="font-size: 11px; color: #64748b;">#1 prémium panorámahajó, üdvözlőitallal</div>
                      </div>
                      <a href="https://legenda.hu/en?partner=38585" target="_blank" rel="noopener sponsored" style="font-size: 12px; font-weight: 700; background: #0f172a; color: #fff; padding: 6px 12px; border-radius: 4px; text-decoration: none;">24 € Foglalás →</a>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; background: #f8fafc; padding: 10px 14px; border-radius: 6px; border: 1px solid #e2e8f0;">
                      <div>
                        <div style="font-size: 13px; font-weight: 700; color: #0f172a;">Széchenyi Gyógyfürdő Soron Kívüli Belépő</div>
                        <div style="font-size: 11px; color: #64748b;">Egész napos kabinos / szekrényes jegy</div>
                      </div>
                      <a href="https://www.getyourguide.com/budapest-szechenyi-spa-full-day-entrance-pass-t4139/?partner_id=YS414AJ&utm_medium=online_publisher&cmp=budapest-card-review&mkt_cmp=true" target="_blank" rel="noopener sponsored" style="font-size: 12px; font-weight: 700; background: #0f172a; color: #fff; padding: 6px 12px; border-radius: 4px; text-decoration: none;">35 € Foglalás →</a>
                    </div>
                  </div>
                </div>
                <div>
                  <div style="font-size: 13px; color: #64748b; margin-bottom: 8px;">Total BKK 72h + Legenda + Széchenyi = <strong>kb. 73 €</strong> (Teljes szabadság, felesleges múzeumi kényszer nélkül)</div>
                </div>
              </div>
            ''', 'html.parser'))

    # 8. Comparison Tables
    tbl_sec = soup.find('section', class_='table-section')
    if tbl_sec:
        h2 = tbl_sec.find('h2')
        if h2: h2.string = "Egymás Melletti Összehasonlítás: Két Tipikus 3 Napos Útiterv"
        p = tbl_sec.find('p')
        if p: p.string = "Hogy lássa, hogyan alakulnak a számok a valóságban, hasonlítsunk össze két tipikus 72 órás utazási stílust:"
        tbl_container = tbl_sec.find('div', style=lambda s: s and 'grid-template-columns' in s)
        if tbl_container:
            tbl_container.clear()
            tbl_container.append(BeautifulSoup('''
              <div>
                <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px 8px 0 0; padding: 12px 16px; display: flex; justify-content: space-between; align-items: center;">
                  <span style="font-size: 14px; font-weight: 700; color: #166534;">A forgatókönyv: Kultúra & Múzeumfókusz</span>
                  <span style="font-size: 11px; font-weight: 800; background: #22c55e; color: #fff; padding: 2px 8px; border-radius: 4px;">KÁRTYA NYER</span>
                </div>
                <table class="data-table" style="border-radius: 0 0 8px 8px; border-top: none; width: 100%; border-collapse: collapse;">
                  <thead>
                    <tr style="background: #f8fafc; text-align: left; font-size: 12px; border-bottom: 1px solid #e2e8f0;">
                      <th style="padding: 10px 12px;">Élmény / Látnivaló</th>
                      <th style="padding: 10px 12px;">Külön Jegyek</th>
                      <th style="padding: 10px 12px;">72h Kártyával (69 €)</th>
                    </tr>
                  </thead>
                  <tbody style="font-size: 13px;">
                    <tr style="border-bottom: 1px solid #e2e8f0;"><td style="padding: 8px 12px;">Korlátlan BKK bérlet (72 óra)</td><td style="padding: 8px 12px;">14,00 € (5 500 Ft)</td><td style="padding: 8px 12px; color: #15803d; font-weight: 600;">Benne van (0 €)</td></tr>
                    <tr style="border-bottom: 1px solid #e2e8f0;"><td style="padding: 8px 12px;">Magyar Nemzeti Múzeum</td><td style="padding: 8px 12px;">9,00 € (3 500 Ft)</td><td style="padding: 8px 12px; color: #15803d; font-weight: 600;">Benne van (0 €)</td></tr>
                    <tr style="border-bottom: 1px solid #e2e8f0;"><td style="padding: 8px 12px;">Magyar Nemzeti Galéria (Vár)</td><td style="padding: 8px 12px;">8,00 € (3 200 Ft)</td><td style="padding: 8px 12px; color: #15803d; font-weight: 600;">Benne van (0 €)</td></tr>
                    <tr style="border-bottom: 1px solid #e2e8f0;"><td style="padding: 8px 12px;">Szépművészeti Múzeum</td><td style="padding: 8px 12px;">16,00 € (6 200 Ft)</td><td style="padding: 8px 12px; color: #15803d; font-weight: 600;">Benne van (0 €)</td></tr>
                    <tr style="border-bottom: 1px solid #e2e8f0;"><td style="padding: 8px 12px;">Szent Lukács Gyógyfürdő</td><td style="padding: 8px 12px;">13,50 € (5 400 Ft)</td><td style="padding: 8px 12px; color: #15803d; font-weight: 600;">Benne van (0 €)</td></tr>
                    <tr style="border-bottom: 1px solid #e2e8f0;"><td style="padding: 8px 12px;">Hivatalos Budavári kisbusz</td><td style="padding: 8px 12px;">18,00 € (7 400 Ft)</td><td style="padding: 8px 12px; color: #15803d; font-weight: 600;">Benne van (0 €)</td></tr>
                    <tr style="background:#f1f5f9; font-weight:700;"><td style="padding: 10px 12px;">Teljes Utazói Költség</td><td style="padding: 10px 12px;">78,50 €</td><td style="padding: 10px 12px;">69,00 €</td></tr>
                    <tr style="background:#dcfce7; font-weight:700; color:#15803d;"><td colspan="2" style="padding: 10px 12px;">Pénzügyi Végeredmény:</td><td style="padding: 10px 12px;">+9,50 € (~3 900 Ft) MEGTAKARÍTÁS</td></tr>
                  </tbody>
                </table>
              </div>

              <div>
                <div style="background: #fff1f2; border: 1px solid #fecdd3; border-radius: 8px 8px 0 0; padding: 12px 16px; display: flex; justify-content: space-between; align-items: center;">
                  <span style="font-size: 14px; font-weight: 700; color: #9f1239;">B forgatókönyv: Ikonikus Látnivalók</span>
                  <span style="font-size: 11px; font-weight: 800; background: #e11d48; color: #fff; padding: 2px 8px; border-radius: 4px;">EGYÉNI FOGLALÁS NYER</span>
                </div>
                <table class="data-table" style="border-radius: 0 0 8px 8px; border-top: none; width: 100%; border-collapse: collapse;">
                  <thead>
                    <tr style="background: #f8fafc; text-align: left; font-size: 12px; border-bottom: 1px solid #e2e8f0;">
                      <th style="padding: 10px 12px;">Élmény / Látnivaló</th>
                      <th style="padding: 10px 12px;">Külön Jegyek</th>
                      <th style="padding: 10px 12px;">72h Kártyával (69 €)</th>
                    </tr>
                  </thead>
                  <tbody style="font-size: 13px;">
                    <tr style="border-bottom: 1px solid #e2e8f0;"><td style="padding: 8px 12px;">Korlátlan BKK bérlet (72 óra)</td><td style="padding: 8px 12px;">14,00 € (5 500 Ft)</td><td style="padding: 8px 12px; color: #15803d; font-weight: 600;">Benne van (0 €)</td></tr>
                    <tr style="border-bottom: 1px solid #e2e8f0;"><td style="padding: 8px 12px;">Magyar Országház Látogatás</td><td style="padding: 8px 12px;">16,00 € (6 500 Ft)</td><td style="padding: 8px 12px; color: #b91c1c;">16,00 € (0% kedvezmény)</td></tr>
                    <tr style="border-bottom: 1px solid #e2e8f0;"><td style="padding: 8px 12px;">Széchenyi Fürdő napijegy</td><td style="padding: 8px 12px;">34,00 € (13 900 Ft)</td><td style="padding: 8px 12px; color: #475569;">27,20 € (20% kedvezmény)</td></tr>
                    <tr style="border-bottom: 1px solid #e2e8f0;"><td style="padding: 8px 12px;">Szent István-bazilika Kilátó</td><td style="padding: 8px 12px;">8,00 € (3 300 Ft)</td><td style="padding: 8px 12px; color: #b91c1c;">8,00 € (0% kedvezmény)</td></tr>
                    <tr style="border-bottom: 1px solid #e2e8f0;"><td style="padding: 8px 12px;">Legenda Esti Kivilágított Hajózás</td><td style="padding: 8px 12px;">24,00 € (9 800 Ft)</td><td style="padding: 8px 12px; color: #b91c1c;">24,00 € (0% kedvezmény)</td></tr>
                    <tr style="background:#f1f5f9; font-weight:700;"><td style="padding: 10px 12px;">Teljes Utazói Költség</td><td style="padding: 10px 12px;">96,00 €</td><td style="padding: 10px 12px;">144,20 €</td></tr>
                    <tr style="background:#fee2e2; font-weight:700; color:#b91c1c;"><td colspan="2" style="padding: 10px 12px;">Pénzügyi Végeredmény:</td><td style="padding: 10px 12px;">-48,20 € (~19 800 Ft) VESZTESÉG a Kártyával!</td></tr>
                  </tbody>
                </table>
              </div>
            ''', 'html.parser'))

    # 9. FAQ
    faq = soup.find('section', class_='faq-section')
    if faq:
        faq.clear()
        faq.append(BeautifulSoup('''
          <h2>Gyakran Ismételt Kérdések a Budapest Kártyáról</h2>
          <div class="faq-item">
            <div class="faq-q">Tartalmazza a Budapest Kártya a Széchenyi Gyógyfürdőt?<span>+</span></div>
            <div class="faq-a">Nem. A standard Budapest Kártyák (24, 48, 72, 96, 120 órás) csupán 20% kedvezményt nyújtanak a standard belépőjegy árából. Kizárólag a Szent Lukács Gyógyfürdőbe biztosít 100%-ban ingyenes belépést a normál kártya. A jóval drágább 72 órás Plus Kártya (99 €) tartalmaz egy belépőt a Széchenyibe, de 99 eurós árával jóval drágább, mintha a BKK bérletet és a fürdőjegyet külön vásárolná meg.</div>
          </div>
          <div class="faq-item">
            <div class="faq-q">Érvényes a Budapest Kártya a Magyar Országházba (Parlament)?<span>+</span></div>
            <div class="faq-a">Nem. A Magyar Országház látogatását az Országgyűlés Hivatala felügyeli, és semmilyen formában nem vesz részt a Budapest Kártya programban. A belépőjegyeket kizárólag a hivatalos Jegymester portálon vagy szervezett idegenvezetés keretében lehet megváltani. A kártya 0% kedvezményt ad.</div>
          </div>
          <div class="faq-item">
            <div class="faq-q">Ingyenes a tömegközlekedés a Budapest Kártyával?<span>+</span></div>
            <div class="faq-a">Igen. A kártya korlátlan utazást biztosít a BKK teljes fővárosi hálózatán (metrók, villamosok, trolibuszok és nappali/éjszakai buszok). Ugyanakkor egy önálló 72 órás BKK Budapest-bérlet mindössze 5 500 Ft (~14 €) a BudapestGO applikációban, így pusztán a közlekedés miatt megvenni a 69 eurós Budapest Kártyát mintegy 55 eurós veszteséget jelent.</div>
          </div>
          <div class="faq-item">
            <div class="faq-q">Érvényes a kártya a 100E repülőtéri közvetlen expresszbuszra?<span>+</span></div>
            <div class="faq-a">Nem. A 100E repülőtéri expresszjárat egyedi díjszabású járat (2 200 Ft / ~5,50 €), amelyre sem a standard Budapest Kártya, sem az általános BKK bérletek nem érvényesek (kivéve a 72h Plus kártyát, amely miniBUD transzfert tartalmaz). A Liszt Ferenc repülőtérről a 200E busszal a Kőbánya-Kispest metróállomásig viszont normál BKK jeggyel és a Budapest Kártyával is korlátlanul lehet utazni.</div>
          </div>
          <div class="faq-item">
            <div class="faq-q">Mikor éri meg igazán megvásárolni a Budapest Kártyát?<span>+</span></div>
            <div class="faq-a">A kártya kizárólag akkor éri meg pénzügyileg, ha a napi tömegközlekedés mellett legalább 3-4 olyan fővárosi múzeumot is meglátogat 48-72 órán belül, amely szerepel az ingyenes listán (pl. Magyar Nemzeti Galéria, Szépművészeti Múzeum, Aquincumi Múzeum, Történeti Múzeum, Kiscelli Múzeum), valamint igénybe veszi a Lukács Fürdőt. Ha a fókuszban a termálfürdők, építészeti ikonok, gasztronómia és esti dunai hajózások állnak, ne vegye meg a kártyát.</div>
          </div>
        ''', 'html.parser'))

    # 10. Calculator JS (Full Hungarian Localization)
    for s in soup.body.find_all('script', recursive=False):
        if s.string and 'CALCULATOR_DATA' in s.string:
            js_code = s.string
            m = re.search(r'const CALCULATOR_DATA = (\{[\s\S]*?\});', js_code)
            if m:
                calc_json_str = m.group(1)
                calc_data = json.loads(calc_json_str)
                calc_data["cards"] = [
                    {"id": "24h", "name": "24 Órás Kártya", "duration": "24h", "price": 39, "description": "Tökéletes egy gyors városi sétához"},
                    {"id": "48h", "name": "48 Órás Kártya", "duration": "48h", "price": 53, "description": "Ideális hétvégi kiruccanáshoz"},
                    {"id": "72h", "name": "72 Órás Kártya", "duration": "72h", "price": 69, "description": "Legnépszerűbb: 3 napos teljes városnézés"},
                    {"id": "72h+", "name": "72 Órás Plus Kártya", "duration": "72h+", "price": 99, "description": "Tartalmazza a miniBUD-ot és a Széchenyit"},
                    {"id": "96h", "name": "96 Órás Kártya", "duration": "96h", "price": 87, "description": "Részletes 4 napos felfedezés"},
                    {"id": "120h", "name": "120 Órás Kártya", "duration": "120h", "price": 96, "description": "Teljes 5 napos budapesti élmény"}
                ]
                calc_data["categories"] = [
                    {"id": "transport", "name": "Közlekedés", "icon": "🚌"},
                    {"id": "cruises", "name": "Dunai Hajózás", "icon": "🚢"},
                    {"id": "baths", "name": "Termálfürdők", "icon": "♨️"},
                    {"id": "museums", "name": "Múzeumok & Kultúra", "icon": "🏛️"},
                    {"id": "tours", "name": "Vezetett Túrák", "icon": "🚶"},
                    {"id": "entertainment", "name": "Szórakozás", "icon": "🎟️"},
                    {"id": "food", "name": "Gasztronómia", "icon": "🍽️"}
                ]
                for attr in calc_data["attractions"]:
                    orig_name = attr["name"]
                    if orig_name in HU_ATTRACTION_NAMES:
                        attr["name"] = HU_ATTRACTION_NAMES[orig_name]
                        
                new_js = js_code.replace(m.group(0), f"const CALCULATOR_DATA = {json.dumps(calc_data, ensure_ascii=False)};")
                
                # Switch currency default to HUF
                new_js = new_js.replace("let currentCurrency = 'EUR';", "let currentCurrency = 'HUF';")
                
                # Update presets to target Hungarian attraction names
                new_js = new_js.replace(
                    """const toSelect = [
        'BKK public transport',
        'Széchenyi thermal bath and swimming pool',
        'Evening cruise (Legenda)',
        'Hungarian National Museum',
        'Hungarian National Gallery'
      ];""",
                    """const toSelect = [
        'BKK korlátlan tömegközlekedés (metró, villamos, busz)',
        'Széchenyi Gyógyfürdő és Uszoda',
        'Danube Legend esti kivilágított sétahajózás (Legenda)',
        'Magyar Nemzeti Múzeum',
        'Magyar Nemzeti Galéria (Budavári Palota)'
      ];"""
                )
                
                new_js = new_js.replace(
                    """const toSelect = [
        'BKK public transport',
        'Hungarian National Museum',
        'Hungarian National Gallery',
        'Budapest History Museum',
        'Museum of Fine Arts',
        'Aquincum Museum and Archaeological Park'
      ];""",
                    """const toSelect = [
        'BKK korlátlan tömegközlekedés (metró, villamos, busz)',
        'Magyar Nemzeti Múzeum',
        'Magyar Nemzeti Galéria (Budavári Palota)',
        'Budapesti Történeti Múzeum – Vármúzeum',
        'Szépművészeti Múzeum (Hősök tere)',
        'Aquincumi Múzeum és Régészeti Park'
      ];"""
                )
                
                # Localize dynamically generated text in JS
                new_js = new_js.replace("verdictTitle.textContent = 'Select Sights on the Left';", "verdictTitle.textContent = 'Válasszon Látnivalókat Balra';")
                new_js = new_js.replace("verdictText.textContent = 'Check the attractions you plan to visit to see if the card saves you money.';", "verdictText.textContent = 'Jelölje be a meglátogatni kívánt helyeket a pontos megtakarítás vagy ráfizetés kalkulálásához.';")
                new_js = new_js.replace("verdictCta.textContent = 'Select Attractions ←';", "verdictCta.textContent = 'Látnivalók Kiválasztása ←';")
                new_js = new_js.replace("verdictTitle.textContent = '💡 Individual Tickets Cheaper';", "verdictTitle.textContent = '💡 Az Egyedi Jegyek Olcsóbbak';")
                new_js = new_js.replace("For this specific itinerary, booking tickets separately saves", "Ehhez az útitervhez a jegyek külön megvétele kedvezőbb, megtakarítás:")
                new_js = new_js.replace("verdictCta.textContent = 'Compare Booking Options ↓';", "verdictCta.textContent = 'Foglalási Opciók Összehasonlítása ↓';")
                new_js = new_js.replace("verdictTitle.textContent = '🎉 Great Value! Card Recommended';", "verdictTitle.textContent = '🎉 Kiváló Értékajánlat! A Kártya Megéri';")
                new_js = new_js.replace("The Budapest Card pays off! You save", "A Budapest Kártya megtérül! Ön megtakarít:")
                new_js = new_js.replace("compared to standalone tickets.", "a külön megvásárolt jegyekhez képest.")
                new_js = new_js.replace("verdictCta.textContent = 'Check Official Budapest Card →';", "verdictCta.textContent = 'Budapest Kártya Foglalása a GYG-n →';")
                new_js = new_js.replace("No attractions selected yet. Check boxes on the left to simulate.", "Még nem választott látnivalót. Jelölje be a helyeket a bal oldalon.")
                new_js = new_js.replace("${selCount} selected", "${selCount} kiválasztva")
                new_js = new_js.replace("Free on 72h+ Card", "Ingyenes 72h+ Kártyával")
                new_js = new_js.replace("100% Free with Card", "100% Ingyenes Kártyával")
                new_js = new_js.replace("${attr.discountPercent}% OFF", "-${attr.discountPercent}% Kedvezmény")
                new_js = new_js.replace("No Discount", "Nincs Kedvezmény")
                
                s.string = new_js
                break

    output_html = str(soup)
    targets = [
        os.path.join(BASE_DIR, 'hu/budapest-card-megéri-e/index.html'),
        os.path.join(BASE_DIR, 'hu/budapest-card-megeri-e/index.html'),
        os.path.join(BASE_DIR, 'hu/budapest-card-is-it-worth-it/index.html')
    ]
    for target in targets:
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, 'w', encoding='utf-8') as f:
            f.write(output_html)
        print(f"  ✓ HU: {target} ({os.path.getsize(target):,} bytes)")

def build_international_pages():
    print("--- COMPILING 20 INTERNATIONAL BUDAPEST CARD PAGES ---")
    other_langs = ["de", "fr", "es", "it", "nl", "pl", "pt", "ro", "ru", "sk", "cs", "bg", "hr", "sr", "uk", "el", "tr", "ja", "ko", "he"]
    
    for lang in other_langs:
        lang_home_path = os.path.join(BASE_DIR, f"{lang}/index.html")
        if not os.path.exists(lang_home_path):
            continue
            
        with open(lang_home_path, 'r', encoding='utf-8') as f:
            lang_home_soup = BeautifulSoup(f.read(), 'html.parser')
            
        lang_navbar = lang_home_soup.find('header', class_='ltt-navbar')
        lang_drawer = lang_home_soup.find('div', class_='ltt-mobile-drawer')
        lang_footer = lang_home_soup.find('footer', class_='footer-dark')
        
        if lang_navbar:
            for a in lang_navbar.find_all('a', class_='ltt-nav-link'):
                href = a.get('href', '')
                if 'budapest-card' in href:
                    a['class'] = ['ltt-nav-link', 'active']
                    a['aria-current'] = 'page'
                else:
                    a['class'] = ['ltt-nav-link']
                    if 'aria-current' in a.attrs: del a['aria-current']

        if lang_drawer:
            for a in lang_drawer.find_all('a', class_='ltt-mobile-link'):
                href = a.get('href', '')
                if 'budapest-card' in href:
                    a['class'] = ['ltt-mobile-link', 'active']
                    a['aria-current'] = 'page'
                else:
                    a['class'] = ['ltt-mobile-link']
                    if 'aria-current' in a.attrs: del a['aria-current']

        soup = BeautifulSoup(en_html, 'html.parser')
        soup.html['lang'] = lang
        
        loc_title, loc_desc = extract_meta_tags(lang)
        if loc_title:
            soup.title.string = loc_title
        if loc_desc:
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc: meta_desc['content'] = loc_desc
            
        canonical = soup.find('link', rel='canonical')
        if canonical:
            canonical['href'] = f"https://www.budapestadventures.com/{lang}/budapest-card-is-it-worth-it"
            
        for h in soup.find_all('link', rel='alternate'):
            h.decompose()
        for hlang, hhref in LANG_HREFLANGS:
            soup.head.append(soup.new_tag('link', rel='alternate', hreflang=hlang, href=hhref))
            
        old_nav = soup.find('header', class_='ltt-navbar')
        if old_nav and lang_navbar: old_nav.replace_with(lang_navbar)
        old_drawer = soup.find('div', class_='ltt-mobile-drawer')
        if old_drawer and lang_drawer: old_drawer.replace_with(lang_drawer)
        old_footer = soup.find('footer', class_='footer-dark')
        if old_footer and lang_footer: old_footer.replace_with(lang_footer)
        
        bc = soup.find('nav', class_='breadcrumbs')
        if bc:
            a_home = bc.find('a')
            if a_home:
                a_home['href'] = f"/{lang}/"
                
        out_path = os.path.join(BASE_DIR, f"{lang}/budapest-card-is-it-worth-it/index.html")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"  ✓ {lang:5}: {out_path} ({os.path.getsize(out_path):,} bytes)")

if __name__ == '__main__':
    build_hungarian_pages()
    build_international_pages()
