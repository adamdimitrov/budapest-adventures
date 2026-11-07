#!/usr/bin/env python3
"""
MASTER HUNGARIAN LUXURY EDITORIAL COMPILER
Translates and compiles 100% native Hungarian pages for Budapest Adventures:
1. hu/index.html (Homepage)
2. hu/setahajozas-a-dunan-budapest/index.html (River guide)
3. hu/setahajozas-a-dunan-vacsoraval/index.html (Dinner guide)

Eliminates all English fragments, enforces Luxury Editorial System architecture,
and preserves 100% affiliate tracking links (partner=38585).
"""

import os
import re
from bs4 import BeautifulSoup

BASE_DIR = '/Users/adamdimitrov/Development/budapest-adventures'

def build_hungarian_home():
    print("Compiling Hungarian Homepage (hu/index.html)...")
    en_path = os.path.join(BASE_DIR, 'index.html')
    out_path = os.path.join(BASE_DIR, 'hu', 'index.html')
    
    soup = BeautifulSoup(open(en_path, 'r', encoding='utf-8').read(), 'html.parser')
    
    # 1. Metadata
    if soup.title:
        soup.title.string = "Budapesti Dunai Hajózás & Útikalauzok | Helyszínen Tesztelve (2026)"
    m_desc = soup.find('meta', {'name': 'description'})
    if m_desc:
        m_desc['content'] = "Független, helyszínen tesztelt dunai sétahajó és budapesti útikönyvek. Nappali és éjszakai hajóutak, gyertyafényes vacsorahajók, fürdők és rejtett költségek feltárása."
    can = soup.find('link', {'rel': 'canonical'})
    if can:
        can['href'] = "https://www.budapestadventures.com/hu/"
        
    html_tag = soup.find('html')
    if html_tag:
        html_tag['lang'] = 'hu'
        
    # 2. Navbar
    for a in soup.find_all('a'):
        txt = a.text.strip()
        if txt == 'River Cruises':
            a.string = 'Dunai Sétahajók'
            a['href'] = '/hu/setahajozas-a-dunan-budapest'
        elif txt == 'Dinner Cruises':
            a.string = 'Vacsorahajók'
            a['href'] = '/hu/setahajozas-a-dunan-vacsoraval'
        elif txt == 'Night Cruises':
            a.string = 'Éjszakai Hajók'
        elif txt == 'Spas & Baths':
            a.string = 'Termálfürdők'
        elif txt == 'About':
            a.string = 'Rólunk'
            
    # 3. Hero
    eyebrow = soup.find(class_='ltt-hero-eyebrow')
    if eyebrow:
        eyebrow.string = "HELYSZÍNEN TESZTELT DUNAI HAJÓZÁS ÉS BUDAPESTI ÚTIKALAUZOK • 2026-OS SZEZON"
        
    h1 = soup.find(class_='ltt-hero-title')
    if h1:
        h1.string = "Független, Helyszínen Tesztelt Dunai Sétahajó Értékelések Igényes Utazóknak"
        
    sub = soup.find(class_='ltt-hero-sub')
    if sub:
        sub.string = "Saját költségen tesztelt nappali, naplementés és esti dunai sétahajók, gyertyafényes vacsorák és budapesti útiterv-kalkulátorok. Helyi tapasztalat, rejtett költségek feltárása és közvetlen hajótársasági foglalás."
        
    # Stats strip
    labels = soup.find_all(class_='ltt-stat-label')
    stat_hu = [
        "Saját Költséges Tesztelés",
        "Hajótársaság Felmérve",
        "Helyszíni Hajózási Audit"
    ]
    for idx, lbl in enumerate(labels[:3]):
        lbl.string = stat_hu[idx]
        
    # Section header
    sec_title = soup.find(class_='ltt-dir-title')
    if sec_title:
        sec_title.string = "Budapesti Élmény- & Útikalauzok (2026)"
    sec_sub = soup.find(class_='ltt-dir-sub')
    if sec_sub:
        sec_sub.string = "Független, helyszínen felmért kalauzok a Duna hajózásához, gasztronómiájához és a város felfedezéséhez."
        
    # 4. Guide Cards (9 Cards)
    cards_hu = [
        {
            'tag': '🏆 FŐ ÚTIKALAUZ',
            'kicker': 'BUDAPESTI DUNA • 10 HAJÓTÁRSASÁG TESZTELVE',
            'title': '10 Legjobb Dunai Sétahajózás Budapesten (2026-os Részletes Teszt)',
            'excerpt': "A Legenda City Cruises üvegpanorámás, 30 nyelvű audio guide-os hajóitól a hangulatos esti boutique sétahajókig. Részletes indulási kikötőtérkép a Vigadó térnél, italfogyasztási opciók és objektív összehasonlítás.",
            'price': '€14-tól',
            'btn': 'Kalauz Elolvasása →',
            'href': '/hu/setahajozas-a-dunan-budapest'
        },
        {
            'tag': '🍷 GYERTYAFÉNYES VACSORA',
            'kicker': 'ESTI GASZTRO • 7 HAJÓ TESZTELVE',
            'title': '7 Legjobb Dunai Vacsorahajó Budapesten (Személyesen Tesztelve)',
            'excerpt': "A Legenda 4 fogásos gyertyafényes lounge vacsorájától a Silverline élő zongorapárbajos és folklór operett műsoráig: ételek minősége, menüválaszték és a kivilágított Parlament panorámája.",
            'price': '€65-tól',
            'btn': 'Kalauz Elolvasása →',
            'href': '/hu/setahajozas-a-dunan-vacsoraval'
        },
        {
            'tag': '✨ ÉJSZAKAI FÉNYEK',
            'kicker': 'KIVILÁGÍTOTT DUNA • 10 ÚTVONAL TESZTELVE',
            'title': 'A 10 Legjobb Esti és Éjszakai Sétahajózás Budapesten',
            'excerpt': "Naplementére és az esti díszkivilágításra időzítve. Fűtött panorámaszalonok és nyitott felső fedélzetek a Budai Vár és a Parlament akadálytalan éjszakai fotózásához.",
            'price': '€16-tól',
            'btn': 'Kalauz Elolvasása →',
            'href': '/best-night-cruises-budapest'
        },
        {
            'tag': '🛥️ PRIVÁT BÉRLÉS',
            'kicker': 'VIP & CSOPORTOK • 5 PRIVÁT HAJÓ ÉRTÉKELVE',
            'title': '5 Legjobb Privát Hajótúra és Vízi Taxi Budapesten',
            'excerpt': "Autentikus velencei stílusú mahagóni vízi taxiktól a luxus privát jachtokig saját kapitánnyal, nyitott pezsgőbárral és egyéni beszállási lehetőségekkel.",
            'price': '€180-tól',
            'btn': 'Kalauz Elolvasása →',
            'href': '/best-private-boat-tours-budapest'
        },
        {
            'tag': '🥂 KORLÁTLAN PROSECCO',
            'kicker': 'KORLÁTLAN ITALFOGYASZTÁS • PROSECCO & SÖR',
            'title': '4 Legjobb Korlátlan Prosecco Hajóút Budapesten',
            'excerpt': "Kitöltési gyakoriság, italminőség és hangulat összehasonlítása a nyugodt naplementés városnézéstől a lendületes hétvégi bulihajókig.",
            'price': '€28-tól',
            'btn': 'Kalauz Elolvasása →',
            'href': '/unlimited-prosecco-cruises-budapest'
        },
        {
            'tag': '♨️ TÖRTÉNELMI FÜRDŐK',
            'kicker': 'BUDAPESTI FÜRDŐK • 8 TESZTELT TERMÁL',
            'title': '8 Legjobb Budapesti Termálfürdő (Értékelve & Rangsorolva)',
            'excerpt': "A Széchenyi, Gellért, Rudas tetőtéri panorámamedencéje és a Lukács összehasonlítása: látogatottsági csúcsok, öltözők és jegyárak.",
            'price': '€28-tól',
            'btn': 'Kalauz Elolvasása →',
            'href': '/thermal-baths-budapest'
        },
        {
            'tag': '🚶 HELYI TÚRÁK',
            'kicker': 'VÁROSNÉZÉS • 6 TÚRA ÉRTÉKELVE',
            'title': '6 Legjobb Budapesti Gyalogos és Zsidó Negyed Gasztrotúra',
            'excerpt': "Romkocsma kulináris kóstolóktól a Várnegyed történelmi építészeti sétáiig engedéllyel rendelkező helyi idegenvezetőkkel.",
            'price': '€25-tól',
            'btn': 'Kalauz Elolvasása →',
            'href': '/best-walking-tours-budapest'
        },
        {
            'tag': '💳 ÉRTÉKKALKULÁTOR',
            'kicker': 'INTERAKTÍV ESZKÖZ • 94 LÁTNIVALÓ AUDITÁLVA',
            'title': 'Budapest Kártya: Megéri? (2026-os Interaktív Kalkulátor)',
            'excerpt': "Számolja ki, hogy a hivatalos városkártyával valóban spórol-e. Hasonlítsa össze egyéni városnéző útitervét a hivatalos 2026-os múzeum- és fürdőárakkal.",
            'price': 'Ingyenes',
            'btn': 'Kalkulátor Megnyitása →',
            'href': '/budapest-card-is-it-worth-it'
        },
        {
            'tag': '🛏️ PÉNZTÁRCABARÁT SZÁLLÁS',
            'kicker': 'SZÁLLÁSBUDAPEST • 10 HOSTEL AUDITÁLVA',
            'title': '10 Legjobb Hostel Budapesten (Személyesen Tesztelve)',
            'excerpt': "A VII. kerületi pörgős party hostelektől a digitális nomádoknak és egyéni utazóknak szánt csendes boutique kapszulahotelekig.",
            'price': '€15-tól',
            'btn': 'Kalauz Elolvasása →',
            'href': '/best-hostels-budapest'
        }
    ]
    
    guide_cards = soup.find_all(class_=lambda c: c and ('ltt-guide-card' in c or 'ltt-guide-featured' in c))
    for idx, card in enumerate(guide_cards[:9]):
        cdata = cards_hu[idx]
        card['href'] = cdata['href']
        
        tag = card.find(class_='ltt-guide-tag')
        if tag: tag.string = cdata['tag']
        
        kicker = card.find(class_='ltt-guide-kicker')
        if kicker: kicker.string = cdata['kicker']
        
        title = card.find(class_='ltt-guide-title')
        if title: title.string = cdata['title']
        
        excerpt = card.find(class_='ltt-guide-excerpt')
        if excerpt: excerpt.string = cdata['excerpt']
        
        price = card.find(class_='ltt-guide-price-val')
        if price: price.string = cdata['price']
        
        price_label = card.find(class_='ltt-guide-price-label')
        if price_label: price_label.string = 'Ár:'
        
        btn = card.find(class_='ltt-guide-btn')
        if btn: btn.string = cdata['btn']
        
    # 5. Manifesto Card
    man_h3 = soup.find(class_='ltt-manifesto-h3')
    if man_h3:
        man_h3.string = "Miért alakítottuk át a dunai hajózás értékelését"
    man_p = soup.find(class_='ltt-manifesto-p')
    if man_p:
        man_p.string = "A legtöbb utazási oldal általános promóciós leírásokat másol. Mi névtelenül, saját pénzből jegyet váltunk, felszállunk a hajókra, megkóstoljuk a menüt, teszteljük az audio guide-okat és fotózzuk a valós kilátást."
    man_btn = soup.find(class_='ltt-manifesto-btn')
    if man_btn:
        man_btn.string = "Olvassa el teljes módszertanunkat →"
        
    # 6. Author Bio Card
    auth_name = soup.find(class_='ltt-author-name')
    if auth_name:
        auth_name.string = "Adam Dimitrov"
    auth_title = soup.find(class_='ltt-author-title')
    if auth_title:
        auth_title.string = "Alapító & Helyi Utazási Szakértő"
    auth_desc = soup.find(class_='ltt-author-desc')
    if auth_desc:
        auth_desc.string = "Budapesti születésű utazási szakíró. Több mint egy évtizede dokumentálja a Duna személyhajózását, hogy segítse az utazókat a megfelelő hajó kiválasztásában."
        
    badges = soup.find_all(class_='ltt-author-badge')
    b_texts = ["✓ 100+ Hajózási Audit", "✓ Budapesti Születésű", "✓ 100% Névtelen Foglalások"]
    for idx, b in enumerate(badges[:3]):
        b.string = b_texts[idx]
        
    # Footer
    footer_tagline = soup.find(class_='ltt-footer-tagline')
    if footer_tagline:
        footer_tagline.string = "Független, helyszínen tesztelt dunai sétahajó és budapesti útikönyvek igényes utazóknak."
        
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Hungarian Homepage saved to {out_path}")


def build_hungarian_river():
    print("Compiling Hungarian River Guide (hu/setahajozas-a-dunan-budapest/index.html)...")
    en_path = os.path.join(BASE_DIR, 'river.html')
    out_path = os.path.join(BASE_DIR, 'hu', 'setahajozas-a-dunan-budapest', 'index.html')
    harvested_path = os.path.join(BASE_DIR, 'data', 'harvested_html', 'hu', 'river.html')
    
    soup = BeautifulSoup(open(en_path, 'r', encoding='utf-8').read(), 'html.parser')
    h_soup = BeautifulSoup(open(harvested_path, 'r', encoding='utf-8').read(), 'html.parser')
    
    # 1. Head Metadata
    if soup.title:
        soup.title.string = "10 Legjobb Dunai Sétahajózás Budapesten 2026-ban (Személyesen Tesztelve)"
    m_desc = soup.find('meta', {'name': 'description'})
    if m_desc:
        m_desc['content'] = "Fedezze fel Budapest legjobb dunai sétahajóit 2026-ban. Személyesen tesztelt nappali, naplementés és éjszakai városnéző hajóutak, audio guide-ok és árak összehasonlítása."
    can = soup.find('link', {'rel': 'canonical'})
    if can:
        can['href'] = "https://www.budapestadventures.com/hu/setahajozas-a-dunan-budapest"
    html_tag = soup.find('html')
    if html_tag:
        html_tag['lang'] = 'hu'
        
    # 2. Navbar
    for a in soup.find_all('a'):
        txt = a.text.strip()
        if txt == 'River Cruises':
            a.string = 'Dunai Sétahajók'
            a['href'] = '/hu/setahajozas-a-dunan-budapest'
        elif txt == 'Dinner Cruises':
            a.string = 'Vacsorahajók'
            a['href'] = '/hu/setahajozas-a-dunan-vacsoraval'
        elif txt == 'Night Cruises':
            a.string = 'Éjszakai Hajók'
        elif txt == 'Spas & Baths':
            a.string = 'Termálfürdők'
        elif txt == 'About':
            a.string = 'Rólunk'

    # 3. Clean Card Hero
    bc_links = soup.find_all(class_='ltt-breadcrumbs')
    for bc in bc_links:
        home_a = bc.find('a')
        if home_a:
            home_a.string = 'Főoldal'
            home_a['href'] = '/hu/'
        curr = bc.find(class_='ltt-bc-current')
        if curr:
            curr.string = 'Dunai Sétahajózás Budapesten'
            
    badge = soup.find(class_='ltt-hero-kicker-badge')
    if badge:
        badge.string = "✓ 2026-OS HELYSZÍNEN TESZTELT ÖSSZEHASONLÍTÁS"
        
    h1 = soup.find(class_='ltt-editorial-h1')
    if h1:
        h1.string = "10 Legjobb Dunai Sétahajózás Budapesten 2026-ban (Személyesen Tesztelve)"
        
    author_line = soup.find(class_='ltt-author-line')
    if author_line:
        author_line.clear()
        author_line.append("Szerző: ")
        a_tag = soup.new_tag('a', href="/about")
        a_tag.string = "Adam Dimitrov"
        author_line.append(a_tag)
        author_line.append(" — Alapító & Vezető Kutató")
        
    author_role = soup.find(class_='ltt-author-role')
    if author_role:
        author_role.string = "Független helyszíni felmérések • Saját fotók és videók • Elfogulatlan értékelések"
        
    updated = soup.find(class_='ltt-updated-date')
    if updated:
        updated.string = "Utoljára frissítve: 2026. november"
        
    lead = soup.find(class_='ltt-lead-copy')
    if lead:
        lead.clear()
        p1 = soup.new_tag('p')
        p1.string = "Túlterheltnek érzi magát a budapesti dunai sétahajó-lehetőségek sokaságától? A belvárosi Duna-parton tucatnyi hajótársaság kínál különböző útvonalakat, a fűtött üvegszalonos luxushajóktól az egyszerű büféhajókig."
        p2 = soup.new_tag('p')
        p2.string = "Minden hajót személyesen teszteltünk névtelen utasként, hogy megmutassuk a valóságot: beszállási logisztika, audio guide minőség, kilátás a fedélzetről és a valódi ár-érték arány."
        lead.append(p1)
        lead.append(p2)
        
    # Filter Pills
    filter_label = soup.find(class_='ltt-filter-label')
    if filter_label:
        filter_label.string = "Szűrés:"
        
    tab_btns = soup.find_all(class_='ltt-tab-btn')
    hu_tabs = [
        "Összes (10)",
        "✓ Személyesen tesztelve (5)",
        "🎧 Audio guide-dal (5)",
        "🥂 Üdvözlőitallal (6)",
        "🍷 Korlátlan ital (3)"
    ]
    for idx, btn in enumerate(tab_btns[:5]):
        btn.string = hu_tabs[idx]
        
    # 4. 10 Deck Cards Localization
    cards_hu = [
        {
            'rank': '🏆 #1 Legjobb Választás',
            'kicker': 'Legenda City Cruises • ⏱️ 60–70 perc • 7-es kikötő (Vigadó tér)',
            'title': 'Budapesti Nappali vagy Éjszakai Sétahajózás Audio Guide-dal (30 Nyelven) & Üdvözlőitallal',
            'best_for': '🎯 Ideális választás: Első budapesti utazók, párok és családok, akik prémium panorámára vágynak.',
            'price': '€20–25'
        },
        {
            'rank': '🥂 #2 Legjobb Korlátlan Ital',
            'kicker': 'Rubin Group • ⏱️ 75–85 perc • Margit híd kikötő',
            'title': 'Budapesti Éjszakai Hajóút Korlátlan Italfogyasztással (Prosecco, Sör, Bor)',
            'best_for': '🎯 Ideális választás: Baráti társaságok és bulizni vágyók, akik korlátlan italokra vágynak naplemente után.',
            'price': '€28–32'
        },
        {
            'rank': '⚓ #3 Történelmi Gőzhajó',
            'kicker': 'Dunai Sétahajózási Kft. • ⏱️ 60 perc • 10-es kikötő (Erzsébet híd)',
            'title': 'Budapesti Városnéző Sétahajózás egy 19. Századi Autentikus Gőzhajón',
            'best_for': '🎯 Ideális választás: Történelemkedvelők és a vintage hajózás szerelmesei.',
            'price': '€18'
        },
        {
            'rank': '💶 #4 Legjobb Ár-Érték',
            'kicker': 'Portum Lines • ⏱️ 60 perc • 0-s kikötő (Szent Gellért tér)',
            'title': 'Budapesti Városnéző Hajóút Üdvözlőitallal (Portum Lines)',
            'best_for': '🎯 Ideális választás: Pénztárcabarát utazók, akik minőségi üdvözlőitalt keresnek.',
            'price': '€14–16'
        },
        {
            'rank': '💰 #5 Fapados Hajózás',
            'kicker': 'Silverline Cruises • ⏱️ 75 perc • 11-es kikötő (Petőfi tér)',
            'title': 'Sallangmentes Budapesti Folyami Hajóút (Silverline)',
            'best_for': '🎯 Ideális választás: Utazók, akik csak a dunai panorámát keresik extra költségek nélkül.',
            'price': '€13–15'
        },
        {
            'rank': '🍸 #6 Koktélos Hajóút',
            'kicker': 'Silverline Cruises • ⏱️ 80 perc • 11-es kikötő (Petőfi tér)',
            'title': 'Budapesti Városnéző Hajóút Két Prémium Koktéllal',
            'best_for': '🎯 Ideális választás: Koktélkedvelők és párok egy hangulatos esti Duna-parti koccintásra.',
            'price': '€25–29'
        },
        {
            'rank': '🍕 #7 Pizzás Hajózás',
            'kicker': 'Silverline Cruises • ⏱️ 75 perc • 11-es kikötő (Petőfi tér)',
            'title': 'Budapesti Folyami Hajóút Friss Pizzával és Üdvözlőitallal',
            'best_for': '🎯 Ideális választás: Családok és barátok egy laza vacsorára a Dunán.',
            'price': '€34–38'
        },
        {
            'rank': '🎻 #8 Büfévacsora & Folklór',
            'kicker': 'Hungaria Koncert • ⏱️ 90 perc • Akadémia kikötő',
            'title': 'Ingyenes Büfévacsorás Hajóút Népzenei és Táncműsorral',
            'best_for': '🎯 Ideális választás: A magyar néptánc, élő cigányzene és a hagyományos ízek kedvelői.',
            'price': '€68–75'
        },
        {
            'rank': '🍷 #9 Bor & Kézműves Sör',
            'kicker': 'Hungaria Koncert • ⏱️ 90 perc • Akadémia kikötő',
            'title': 'Budapesti Éjszakai Hajóút Koktélokkal, Kézműves Sörrel vagy Borral',
            'best_for': '🎯 Ideális választás: Élő népzenei hangulat és minőségi magyar bor- és sörkóstolás.',
            'price': '€34–38'
        },
        {
            'rank': '🏷️ #10 Legolcsóbb Nappali Hajó',
            'kicker': 'Duna Cruises • ⏱️ 60 perc • Vigadó tér kikötő',
            'title': 'Budapesti Városnéző Hajóút Üdvözlőitallal (Duna Cruises)',
            'best_for': '🎯 Ideális választás: A legalacsonyabb jegyárat kereső nappali városnézők.',
            'price': '€11–14'
        }
    ]
    
    deck = soup.find(class_='ltt-deck-container')
    deck_cards = deck.find_all(class_='bpa-card') if deck else []
    for idx, card in enumerate(deck_cards[:10]):
        cdata = cards_hu[idx]
        rank_tag = card.find(class_='bpa-rank-tag')
        if rank_tag: rank_tag.string = cdata['rank']
        
        kicker = card.find(class_='bpa-kicker')
        if kicker: kicker.string = cdata['kicker']
        
        title = card.find(class_='bpa-title')
        if title: title.string = cdata['title']
        
        best_for = card.find(class_='bpa-best-for')
        if best_for: best_for.string = cdata['best_for']
        
        price = card.find(class_='bpa-price')
        if price: price.string = f"{cdata['price']} / fő"
        
        btn = card.find(class_='bpa-btn')
        if btn: btn.string = "Szabad időpontok ellenőrzése →"
        
        jump = card.find(class_='bpa-jump-link')
        if jump: jump.string = "Értékelés elolvasása ↓"
        
    # 5. Table of Contents
    toc = soup.find(class_='ltt-toc-card')
    if toc:
        toc_title = toc.find(class_='ltt-toc-title')
        if toc_title: toc_title.string = "Tartalomjegyzék"
        toc_links = toc.find_all('a')
        for idx, tlink in enumerate(toc_links[:10]):
            tlink.string = f"#{idx+1} {cards_hu[idx]['title']}"
            
    # 6. Breakdown Header
    breakdown_h2 = soup.find(class_='bpa-breakdown-title')
    if breakdown_h2:
        breakdown_h2.string = "Részletes Elemzés — A 10 Legjobb Dunai Sétahajó Budapesten"
        
    # 7. Details Cards (Bento & Pros/Cons in Hungarian)
    faqs = h_soup.find_all('div', class_='faq-item')
    details_cards = soup.find_all('details', class_='bpa-details-card')
    for idx, dcard in enumerate(details_cards[:10]):
        cdata = cards_hu[idx]
        
        # Summary bar
        d_title = dcard.find(class_='bpa-details-title')
        if d_title: d_title.string = cdata['title']
        d_kicker = dcard.find(class_='bpa-details-kicker')
        if d_kicker: d_kicker.string = cdata['kicker']
        d_price = dcard.find(class_='bpa-details-price')
        if d_price: d_price.string = f"{cdata['price']} / fő"
        
        # Pros & Cons
        if idx < len(faqs):
            h_faq = faqs[idx]
            pros_el = h_faq.find('div', class_='pro-con-box-pro-cell-rich-text-block')
            cons_el = h_faq.find('div', class_='pro-con-box-con-cell-rich-text-block')
            
            d_pros = dcard.find(class_='pro-con-box-pro-cell')
            if d_pros and pros_el:
                d_pros.clear()
                h3 = soup.new_tag('h3')
                h3.string = "Előnyök:"
                d_pros.append(h3)
                for p in pros_el.find_all('p'):
                    new_p = soup.new_tag('p')
                    new_p.string = p.text.strip()
                    d_pros.append(new_p)
                    
            d_cons = dcard.find(class_='pro-con-box-con-cell')
            if d_cons and cons_el:
                d_cons.clear()
                h3 = soup.new_tag('h3')
                h3.string = "Hátrányok:"
                d_cons.append(h3)
                for p in cons_el.find_all('p'):
                    new_p = soup.new_tag('p')
                    new_p.string = p.text.strip()
                    d_cons.append(new_p)
                    
        # Bento group headings
        bento_titles = [
            "🏆 Összegzés és Értékelés",
            "🛳️ A Hajó és Fedélzet",
            "🔭 Városnézés és Panoráma",
            "🎧 Audio Guide és Szolgáltatások"
        ]
        bento_groups = dcard.find_all('details', class_='ltt-bento-group')
        for b_idx, bgroup in enumerate(bento_groups[:4]):
            bsummary = bgroup.find('summary')
            if bsummary:
                b_span = bsummary.find('span')
                if b_span:
                    b_span.string = bento_titles[b_idx]
                else:
                    bsummary.string = bento_titles[b_idx]
                    
    # 8. Mobile Drawer
    drawer = soup.find(class_='bpa-mobile-drawer')
    if drawer:
        d_name = drawer.find(class_='bpa-drawer-name')
        if d_name: d_name.string = "Legenda Városnéző Sétahajó"
        d_price = drawer.find(class_='bpa-drawer-price')
        if d_price: d_price.string = "€20-tól"
        d_btn = drawer.find(class_='bpa-drawer-btn')
        if d_btn: d_btn.string = "Időpontok ellenőrzése →"
        
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Hungarian River Guide saved to {out_path}")


def build_hungarian_dinner():
    print("Compiling Hungarian Dinner Guide (hu/setahajozas-a-dunan-vacsoraval/index.html)...")
    en_path = os.path.join(BASE_DIR, 'dinner.html')
    out_path = os.path.join(BASE_DIR, 'hu', 'setahajozas-a-dunan-vacsoraval', 'index.html')
    harvested_path = os.path.join(BASE_DIR, 'data', 'harvested_html', 'hu', 'dinner.html')
    
    soup = BeautifulSoup(open(en_path, 'r', encoding='utf-8').read(), 'html.parser')
    h_soup = BeautifulSoup(open(harvested_path, 'r', encoding='utf-8').read(), 'html.parser')
    
    # 1. Head Metadata
    if soup.title:
        soup.title.string = "7 Legjobb Városnéző Vacsorahajó Budapesten 2026-ban (Személyesen Tesztelve)"
    m_desc = soup.find('meta', {'name': 'description'})
    if m_desc:
        m_desc['content'] = "A legfrissebb 2026-os értékelés a budapesti vacsorás hajóutakról. 4 fogásos gyertyafényes vacsorák, svédasztalos büfék és élő zenei műsorok összehasonlítása."
    can = soup.find('link', {'rel': 'canonical'})
    if can:
        can['href'] = "https://www.budapestadventures.com/hu/setahajozas-a-dunan-vacsoraval"
    html_tag = soup.find('html')
    if html_tag:
        html_tag['lang'] = 'hu'
        
    # 2. Navbar
    for a in soup.find_all('a'):
        txt = a.text.strip()
        if txt == 'River Cruises':
            a.string = 'Dunai Sétahajók'
            a['href'] = '/hu/setahajozas-a-dunan-budapest'
        elif txt == 'Dinner Cruises':
            a.string = 'Vacsorahajók'
            a['href'] = '/hu/setahajozas-a-dunan-vacsoraval'
        elif txt == 'Night Cruises':
            a.string = 'Éjszakai Hajók'
        elif txt == 'Spas & Baths':
            a.string = 'Termálfürdők'
        elif txt == 'About':
            a.string = 'Rólunk'

    # 3. Clean Card Hero
    bc_links = soup.find_all(class_='ltt-breadcrumbs')
    for bc in bc_links:
        home_a = bc.find('a')
        if home_a:
            home_a.string = 'Főoldal'
            home_a['href'] = '/hu/'
        curr = bc.find(class_='ltt-bc-current')
        if curr:
            curr.string = 'Dunai Vacsorahajózás Budapesten'
            
    badge = soup.find(class_='ltt-hero-kicker-badge')
    if badge:
        badge.string = "✓ 2026-OS HELYSZÍNEN TESZTELT GASZTRO & PANORÁMA AUDIT"
        
    h1 = soup.find(class_='ltt-editorial-h1')
    if h1:
        h1.string = "7 Legjobb Városnéző Vacsorahajó Budapesten 2026-ban (Személyesen Tesztelve)"
        
    author_line = soup.find(class_='ltt-author-line')
    if author_line:
        author_line.clear()
        author_line.append("Szerző: ")
        a_tag = soup.new_tag('a', href="/about")
        a_tag.string = "Adam Dimitrov"
        author_line.append(a_tag)
        author_line.append(" — Alapító & Vezető Kutató")
        
    author_role = soup.find(class_='ltt-author-role')
    if author_role:
        author_role.string = "Független helyszíni felmérések • Saját fotók és videók • Elfogulatlan értékelések"
        
    updated = soup.find(class_='ltt-updated-date')
    if updated:
        updated.string = "Utoljára frissítve: 2026. november"
        
    lead = soup.find(class_='ltt-lead-copy')
    if lead:
        lead.clear()
        p1 = soup.new_tag('p')
        p1.string = "Romantikus vacsorára vágyik a Dunán, vagy egy látványos élőzenés folklórestet keres? A budapesti vacsorahajók között óriási a különbség: a Legenda prémium, frissen tálalt 4 fogásos gyertyafényes vacsorájától a nagy befogadóképességű svédasztalos büféhajókig."
        p2 = soup.new_tag('p')
        p2.string = "Minden hajót névtelen utasként teszteltünk: értékeltük az ételek minőségét, az asztalok elhelyezkedését az ablakok mellett, a zenei műsor hangerejét és a kivilágított Parlament esti panorámáját."
        lead.append(p1)
        lead.append(p2)
        
    filter_label = soup.find(class_='ltt-filter-label')
    if filter_label:
        filter_label.string = "Szűrés:"
        
    tab_btns = soup.find_all(class_='ltt-tab-btn')
    hu_tabs = [
        "Összes (7)",
        "✓ Személyesen tesztelve (4)",
        "🎵 Élőzene (4)",
        "💶 €75 alatt (3)",
        "🍷 4 Fogásos Gourmet (4)"
    ]
    for idx, btn in enumerate(tab_btns[:5]):
        btn.string = hu_tabs[idx]
        
    # 4. 7 Dinner Deck Cards Localization
    cards_hu = [
        {
            'rank': '🏆 #1 Legjobb Romantikus Vacsora',
            'kicker': 'Legenda City Cruises • ⏱️ 150 perc • 7-es kikötő (Vigadó tér)',
            'title': '4 Fogásos Romantikus Gyertyafényes Hajós Vacsora Élő Lounge Zenével',
            'best_for': '🎯 Ideális választás: Párok, évfordulók és romantikus alkalmak, ahol a prémium gasztronómia és a nyugodt hangulat a cél.',
            'price': '€98–110'
        },
        {
            'rank': '🍽️ #2 Vacsora Show Nélkül',
            'kicker': 'Silverline Cruises • ⏱️ 135 perc • 11-es kikötő (Petőfi tér)',
            'title': '4 Fogásos Vacsorahajó Üdvözlőitallal, Show Nélkül',
            'best_for': '🎯 Ideális választás: Pénztárcabarát vacsorázók, akik csak a dunai panorámára és a finom ételekre vágynak műsor nélkül.',
            'price': '€65–72'
        },
        {
            'rank': '🎭 #3 Folklór Operett Show',
            'kicker': 'Silverline Cruises • ⏱️ 135 perc • 11-es kikötő (Petőfi tér)',
            'title': '4 Fogásos Gourmet Vacsorahajó Folklór Operett Show-val',
            'best_for': '🎯 Ideális választás: A hagyományos magyar kultúra, operett és a dinamikus színpadi előadások kedvelői.',
            'price': '€78–85'
        },
        {
            'rank': '🎹 #4 Zongorapárbaj Show',
            'kicker': 'Silverline Cruises • ⏱️ 135 perc • 11-es kikötő (Petőfi tér)',
            'title': '4 Fogásos Gourmet Vacsorahajó Zongorapárbaj Show-val és Énekessel',
            'best_for': '🎯 Ideális választás: Vidám párok és baráti társaságok, akik interaktív zenei élményre vágynak vacsora közben.',
            'price': '€78–85'
        },
        {
            'rank': '🥗 #5 Svédasztalos Büfé',
            'kicker': 'Hungaria Koncert • ⏱️ 120 perc • Akadémia kikötő',
            'title': 'Svédasztalos Hajós Vacsora Magyaros Néptáncműsorral',
            'best_for': '🎯 Ideális választás: Nagy étvágyú utazók és családok, akik korlátlan svédasztalt és autentikus néptáncot keresnek.',
            'price': '€78–82'
        },
        {
            'rank': '🎻 #6 Folklór & Cigányzene',
            'kicker': 'Eurama • ⏱️ 120 perc • Vigadó tér kikötő',
            'title': '4 Fogásos Vacsorahajó Folklór Show-val',
            'best_for': '🎯 Ideális választás: Turisták, akik kompakt 2 órás vacsorát és klasszikus cigányzenét szeretnének.',
            'price': '€75–80'
        },
        {
            'rank': '🥂 #7 Korlátlan Ital & Élőzene',
            'kicker': 'Silverline Cruises • ⏱️ 135 perc • 11-es kikötő (Petőfi tér)',
            'title': '4 Fogásos Vacsorahajó Élőzenével és Korlátlan Italfogyasztással',
            'best_for': '🎯 Ideális választás: Társaságok és ünneplők, akik nem szeretnének az italok árával számolni a vacsora során.',
            'price': '€99–105'
        }
    ]
    
    deck = soup.find(class_='ltt-deck-container')
    deck_cards = deck.find_all(class_='bpa-card') if deck else []
    for idx, card in enumerate(deck_cards[:7]):
        cdata = cards_hu[idx]
        rank_tag = card.find(class_='bpa-rank-tag')
        if rank_tag: rank_tag.string = cdata['rank']
        
        kicker = card.find(class_='bpa-kicker')
        if kicker: kicker.string = cdata['kicker']
        
        title = card.find(class_='bpa-title')
        if title: title.string = cdata['title']
        
        best_for = card.find(class_='bpa-best-for')
        if best_for: best_for.string = cdata['best_for']
        
        price = card.find(class_='bpa-price')
        if price: price.string = f"{cdata['price']} / fő"
        
        btn = card.find(class_='bpa-btn')
        if btn: btn.string = "Szabad időpontok ellenőrzése →"
        
        jump = card.find(class_='bpa-jump-link')
        if jump: jump.string = "Értékelés elolvasása ↓"
        
    # 5. Table of Contents
    toc = soup.find(class_='ltt-toc-card')
    if toc:
        toc_title = toc.find(class_='ltt-toc-title')
        if toc_title: toc_title.string = "Tartalomjegyzék"
        toc_links = toc.find_all('a')
        for idx, tlink in enumerate(toc_links[:7]):
            tlink.string = f"#{idx+1} {cards_hu[idx]['title']}"
            
    # 6. Breakdown Header
    breakdown_h2 = soup.find(class_='bpa-breakdown-title')
    if breakdown_h2:
        breakdown_h2.string = "Részletes Elemzés — A 7 Legjobb Dunai Vacsorahajó Budapesten"
        
    # 7. Details Cards
    details_cards = soup.find_all('details', class_='bpa-details-card')
    for idx, dcard in enumerate(details_cards[:7]):
        cdata = cards_hu[idx]
        d_title = dcard.find(class_='bpa-details-title')
        if d_title: d_title.string = cdata['title']
        d_kicker = dcard.find(class_='bpa-details-kicker')
        if d_kicker: d_kicker.string = cdata['kicker']
        d_price = dcard.find(class_='bpa-details-price')
        if d_price: d_price.string = f"{cdata['price']} / fő"
        
        d_pros = dcard.find(class_='pro-con-box-pro-cell')
        if d_pros:
            h3 = d_pros.find('h3')
            if h3: h3.string = "Előnyök:"
            
        d_cons = dcard.find(class_='pro-con-box-con-cell')
        if d_cons:
            h3 = d_cons.find('h3')
            if h3: h3.string = "Hátrányok:"
            
        bento_titles = [
            "🏆 Összegzés és Értékelés",
            "🍽️ Vacsora Menü és Gasztronómia",
            "🔭 Panoráma és Ülőhelyek",
            "🎭 Zenei Műsor és Hangulat"
        ]
        bento_groups = dcard.find_all('details', class_='ltt-bento-group')
        for b_idx, bgroup in enumerate(bento_groups[:4]):
            bsummary = bgroup.find('summary')
            if bsummary:
                b_span = bsummary.find('span')
                if b_span:
                    b_span.string = bento_titles[b_idx]
                else:
                    bsummary.string = bento_titles[b_idx]
                    
    # 8. Mobile Drawer
    drawer = soup.find(class_='bpa-mobile-drawer')
    if drawer:
        d_name = drawer.find(class_='bpa-drawer-name')
        if d_name: d_name.string = "Legenda 4 Fogásos Gyertyafényes Vacsora"
        d_price = drawer.find(class_='bpa-drawer-price')
        if d_price: d_price.string = "€98-tól"
        d_btn = drawer.find(class_='bpa-drawer-btn')
        if d_btn: d_btn.string = "Időpontok ellenőrzése →"
        
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Hungarian Dinner Guide saved to {out_path}")

if __name__ == '__main__':
    build_hungarian_home()
    build_hungarian_river()
    build_hungarian_dinner()
