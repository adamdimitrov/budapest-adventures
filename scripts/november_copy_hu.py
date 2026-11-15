# -*- coding: utf-8 -*-
"""HU copy for /hu/budapest-programok-november. Facts: scripts/november_data.py. No em dashes."""

LANG = "hu"
SLUG = "budapest-programok-november"
SLUG_CSS = "hu-budapest-programok-november"
PATH = "/hu/budapest-programok-november"
OG_LOCALE = "hu_HU"
TITLE_TAG = "Budapest novemberben 2026: a 8 legjobb program"
H1 = "Budapest novemberben: a 8 legjobb program 2026-ban"
H1_MUTED = "(esti hajók, forró medencék, vásárnyitás)"
CRUMB = "Budapest novemberben"
META = ("Mit csinálj Budapesten 2026 novemberében: esti hajóút 16:20-tól, forró kültéri medencék, "
        "vámpíros éjszakai séta, gasztrotúra és a karácsonyi vásárok nyitása. 12 eurótól.")
KICKER = "2026 novemberi programtervező"
AUTHOR_ROLE = "8 program • 7 saját tapasztalat • Dátumok és napfény"
UPDATED = "Frissítve"
UPDATED_DATE = "2026. nov. 15."

UI = dict(
    check="Időpontok és jegyek →", book_site="Időpontok és jegyek →", read="Részletek ↓",
    free_cxl="Ingyenes lemondás", instant="Azonnali QR", cxl24="Ingyenes lemondás 24 óráig",
    direct_trust="Foglalás közvetlenül az üzemeltetőnél",
    reviews_one="{n} értékelés · 1 oldal", reviews_many="{n} értékelés · {k} oldal",
    rating_on="Értékelés 1 foglalási oldalon", rating_many="Értékelések {k} foglalási oldalon, mind erre a termékre",
    no_rating="Új ajánlat", tested="✓ Kipróbáltam",
    pick="✓ Válaszd", skip="✕ Hagyd ki", pros="Előnyök:", cons="Hátrányok:", summary="Összefoglaló és értékelés", overview="Áttekintés",
    live="Hivatalos jegyek, élő elérhetőség", book_dates="Időpontok és foglalás",
    best_price="Legjobb ár • Azonnali visszaigazolás", qf="Gyors tények",
    perk_qr="Azonnali QR-kód a telefonodra", perk_refund="Teljes visszatérítés 24 óráig",
    perk_direct="Foglalás közvetlenül az üzemeltetőnél",
    breakdown_h="Részletesen: 8 novemberi program Budapesten",
    breakdown_sub="Rangsorolva • Minden leírás nyitva • Kattints az összecsukáshoz",
    expand="Mind kinyit", collapse="Mind összecsuk",
    contents="Tartalom (8)", all_items="Mind a 8 novemberi program", jump="Ugrás egy programhoz",
    toc_deck="A 8 legjobb novemberi program", toc_breakdown="Részletesen (8 program)",
    filter_all="Mind", filter_label="Szűrés:",
    filters=[("river", "A Dunán"), ("bath", "Termálfürdők"), ("dark", "Sötétedés után"),
             ("food", "Gasztro és vacsora"), ("u40", "40 € alatt")],
    per_person="fő", home="Főoldal", by="Írta:", founder="alapító, budapesti",
    faq_h="Gyakori kérdések", from_price="{p} €-tól",
)

C = {}
C["legenda-evening"] = dict(
    rank="🏆 #1 A legjobb novemberi este", title="Danube Legend esti hajóút üdvözlőitallal",
    dur="1 óra", place="7-es kikötő, Vigadó tér", map="Legenda City Cruises Dock 7 Budapest",
    psub="felnőtt • 16:20-tól 20 percenként",
    tested_pop="<strong>Ezt a hajóutat én is kipróbáltam.</strong> A fotók többsége saját, a Legenda hajóin készült.",
    pills=[("🕒", "20 percenként · 16:20-21:00",
            "<strong>November 22-ig:</strong> 16:20 és 21:00 között 20 percenként. <strong>November 23-tól:</strong> plusz egy 15:40-es indulás, utána 16:20-tól 21:00-ig 20 percenként. Kb. 1 óra. A Legenda 2026-os menetrendje szerint."),
           ("🌆", "Már az első hajó is sötétben megy", "November 15-én 16:07-kor, 30-án 15:55-kor megy le a nap, így már a 16:20-as hajó is a kivilágított Parlament és Vár előtt halad el."),
           ("🥂", "1 ital az árban", "Egy pohár pezsgő, bor, sör, üdítő vagy ásványvíz. Ingyenes wifi a fedélzeten."),
           ("🎧", "30 nyelvű audioguide", "Film és audioguide saját fejhallgatón 30 nyelven, köztük magyarul, angolul és németül."),
           ("🎟️", "25 € · 10 év alatt ingyenes", "Felnőtt 25 €, diák 22,50 €, gyerek 10-14 év 17,50 €, 10 év alatt ingyenes.")],
    pick="ha egy óra alatt akarod látni a kivilágított Dunát, november bármelyik estéjén, a folyó legjobb audioguide-jával.",
    skip="ha szűk a keret: 25 € több, mint amennyit a legtöbb városnéző hajó kér.",
    pros=["16:20-tól 20 percenként indul, bármilyen esti programba belefér",
          "Novemberben az egész út sötétben megy: minden látnivaló ki van világítva",
          "Fedett úszó kikötő mosdóval, hideg, esős estén sokat számít"],
    cons=["Drágább a fapados hajóknál", "Nem választhatod ki, melyik Legenda-hajót kapod"],
    body="""<p>Novemberben a dunai hajóút nem rosszabb, hanem jobb. <strong>November közepén 16:07-kor megy le a nap</strong>, így a Legenda első esti hajója <strong>16:20-kor</strong> már a kivilágított Parlament és a budai Vár előtt halad el, és 17:30 előtt vissza is érsz a rakpartra, előtted az egész este.</p>
<p>Ezt a hajóutat én is kipróbáltam. Egyórás kör üdvözlőitallal és a folyó legjobb audioguide-jával: film és kommentár saját fejhallgatón, 30 nyelven. <strong>November 23-tól</strong> a Legenda egy <strong>15:40-es</strong> indulást is beiktat, ez még elkapja az utolsó fényeket.</p>
<h3>Kinek ajánlom</h3>
<p><strong>Válaszd</strong> az első estédre Budapesten: egy óra alatt megmutatja a kivilágított várost, és szabadon hagyja az estét a vacsorára.</p>
<p><strong>Hagyd ki</strong>, ha a hajón akarsz vacsorázni: akkor <a href="#item-3-legenda-candlelit-dinner">a Legenda gyertyafényes vacsoráját</a> foglald, ugyanarról a kikötőről. Az összes esti hajó egymás mellett: <a href="/hu/legjobb-éjszakai-hajóutak-budapest">a legjobb éjszakai hajóutak Budapesten</a>.</p>
<h3>Találkozási pont</h3>
<p>🗺️ <strong>Találkozási pont: </strong>Legenda, Jane Haining rakpart 7, 7-es kikötő (Vigadó tér), pesti oldal.<br/>🚋 <strong>Tömegközlekedés:</strong> 2-es villamos a Vigadó térig, vagy M1 a Vörösmarty térig.</p>""",
    qf_badge="A Duna éjjel", qf=[("Indulások", "Nov. 22-ig: 16:20-21:00, 20 percenként · nov. 23-tól: 15:40 is"), ("Időtartam", "Kb. 1 óra"),
        ("Ár", "Felnőtt 25 € · diák 22,50 € · gyerek 10-14 év 17,50 € · 10 év alatt ingyenes"), ("Az árban", "1 ital, 30 nyelvű audioguide, wifi"),
        ("Kikötő", "7-es kikötő, Vigadó tér")],
    chips=[("yes", "✓ Már az első hajó is sötétben"), ("yes", "✓ Ital az árban"), ("yes", "✓ 30 nyelv"), ("no", "✕ Nem a legolcsóbb")],
    perks=["Kikötő: <strong>7-es</strong>", "Első esti hajó: <strong>16:20</strong>"],
    desc="Egyórás esti dunai hajóút üdvözlőitallal és 30 nyelvű audioguide-dal, 16:20-tól 20 percenként.",
)
C["szechenyi"] = dict(
    rank="#2 A legjobb fürdő a hidegben", title="Széchenyi fürdő", dur="Fél nap", place="Városliget",
    map="Széchenyi Thermal Bath Budapest", psub="felnőtt • hétfő-csütörtök reggeli jegy",
    tested_pop="<strong>A Széchenyiben én is jártam.</strong> A kártya fotóinak többsége saját.",
    pills=[("🕒", "Pénteken 22:00-ig", "<strong>Hétfő-csütörtök</strong> 7:00-20:00, <strong>péntek</strong> 7:00-22:00, <strong>szombat-vasárnap</strong> 8:00-20:00."),
           ("♨️", "Kültéri medencék 36-38 °C", "Kültéri termálmedence 36-38 °C, élménymedence 32-34 °C, úszómedence 26-28 °C, novemberben mind nyitva."),
           ("🎟️", "Reggeli jegy 39 €", "Reggeli jegy szekrénnyel, belépés 7:00 és 9:00 között, hétfő-csütörtök: 39 €. Hétköznapi jegy 46 €, saját kabinnal 50 €. "
            "A pénztárban: hétfő-csütörtök 13 200 Ft, péntek-vasárnap 14 800 Ft."),
           ("🎉", "Szombatonként Sparty", "A szombat esti medencés buli 21:30-kor kezdődik. Csak 18 év felett, és a jegy nem visszatéríthető.")],
    pick="Budapest novemberi képéért: forró kültéri medencék, gőz a hideg levegőben.",
    skip="ha nem bírod a tömeget: hétvégi délutánokon zsúfolt, hétköznap nyitáskor gyere.",
    pros=["Három kültéri medence novemberben is, a legmelegebb 36-38 °C",
          "Pénteken 22:00-ig nyitva, 16 órától sötétben fürdesz", "Metrómegálló a bejáratnál"],
    cons=["A város legzsúfoltabb fürdője", "Az online jegy drágább, mint a pénztárban"],
    body="""<p>A Széchenyit a hideg teszi igazán jóvá. Novemberben <strong>nappal 9, éjjel 3 fok körül</strong> van, a kültéri termálmedence viszont <strong>36-38 °C</strong>, így a sárga neobarokk homlokzat alatt gőzölög a víz. Ha 15:30 körül érkezel, nappali fényben kezdesz és szürkületben fejezed be.</p>
<p>A Széchenyiben én is jártam. <strong>Pénteken 22:00-ig nyitva van</strong>, ez a hét legjobb estéje egy sötétedés utáni fürdőzésre.</p>
<h3>Kinek ajánlom</h3>
<p><strong>Válaszd</strong> az első budapesti fürdődnek. A <strong>39 eurós reggeli jegy</strong> (hétfő-csütörtök, belépés 9:00-ig) a legjobb ár-érték.</p>
<p><strong>Hagyd ki</strong>, ha valami nyugodtabbat és régebbit keresel: akkor <a href="#item-4-rudas-thermal-bath">a Rudast</a> foglald. Mind a hat fürdő összehasonlítva: <a href="/hu/legjobb-termalfurdok-budapest">a legjobb budapesti termálfürdők</a>.</p>
<h3>Így jutsz oda</h3>
<p>🚇 <strong>Metró:</strong> M1 a Széchenyi fürdő megállóig, a bejáratnál van.<br/>🎒 <strong>Hozd magaddal:</strong> fürdőruha, papucs, törölköző. A beltéri csarnokokból gyorsan menj ki a kültéri medencékhez.</p>""",
    qf_badge="Városliget", qf=[("Nyitvatartás", "Hétfő-csütörtök 7:00-20:00 · péntek 22:00-ig · szombat-vasárnap 8:00-20:00"),
        ("Jegy", "Reggeli jegy 39 € · hétköznapi jegy 46 € · kabinnal 50 €"),
        ("Kültéri medencék", "36-38 °C termál · 32-34 °C élmény · 26-28 °C úszó"), ("Metró", "M1 Széchenyi fürdő")],
    chips=[("yes", "✓ Kültéri medencék novemberben"), ("yes", "✓ Pénteken 22:00-ig"), ("yes", "✓ Ingyenes lemondás"), ("no", "✕ Zsúfolt hétvégén")],
    perks=["Helyszín: <strong>Városliget</strong>", "Medencék: <strong>3 kültéri</strong>"],
    desc="Belépő a Széchenyi fürdőbe, 36-38 °C-os kültéri termálmedencével, ősszel és télen is nyitva.",
)
C["legenda-dinner"] = dict(
    rank="#3 A legjobb vacsorás hajó", title="Gyertyafényes 4 fogásos vacsorás hajóút élő zenével",
    dur="2,5 óra", place="7-es kikötő, Vigadó tér", map="Legenda City Cruises Dock 7 Budapest",
    psub="felnőtt • naponta 19:00",
    tested_pop="<strong>Ezt a hajóutat én is kipróbáltam.</strong> A részletes értékelés fotói és videója saját.",
    pills=[("🕒", "Naponta 19:00", "Novemberben <strong>minden este 19:00-kor</strong> indul. Kb. 2,5 óra a Legenda üvegtetős panorámahajóján."),
           ("🍽️", "4 fogás à la carte", "Minden fogást az asztalnál választasz az étlapról. 3 és 12 év között 3 fogásos gyerekmenü jár 84 euróért."),
           ("🎶", "Élő zene", "Élő zene egész este, üdvözlőital és gyertyafényes asztalok."),
           ("🍷", "Italok külön", "Az üdvözlőitalon kívül az italokat a fedélzeten fizeted.")],
    pick="romantikus, felszolgált vacsoráért, az asztalodtól látható kivilágított Parlamenttel.",
    skip="ha az italokat is benne akarod látni az árban: azokat a fedélzeten fizeted.",
    pros=["Az asztalnál rendelt 4 fogásos vacsora, nem büfé",
          "Üvegtetős hajó: bent meleg van, minden helyről látsz",
          "Minden este 19:00-kor indul"],
    cons=["Felnőttenként 110 €", "Az italok külön fizetendők"],
    body="""<p>A novemberi este hosszú: fél ötre besötétedik, és 19 óra után semmi nem csábít ki a szabadba. Ilyenkor jön ki a legjobban egy <strong>2,5 órás vacsora a Dunán</strong>, és a Legenda gyertyafényes hajója az, amit én foglalnék. <strong>Felszolgált, 4 fogásos à la carte vacsora</strong> élő zenével, üvegtetős hajón, így végig melegben ülsz, és közben látod a kivilágított Parlamentet, a Várat és a hidakat.</p>
<p>Ezt a hajóutat én is kipróbáltam. A büfés hajóktól a tempó különbözteti meg: minden fogást az asztalnál rendelsz, és senki nem siettet.</p>
<h3>Kinek ajánlom</h3>
<p><strong>Válaszd</strong> randira vagy évfordulóra. A 3-12 éves gyerekek 3 fogásos menüt kapnak 84 euróért.</p>
<p><strong>Hagyd ki</strong>, ha a 110 euró sok: <a href="#item-6-silverline-dinner-cruise">a Silverline 4 fogásos vacsorája</a> 77 eurótól indul. Mind a hat összehasonlítva: <a href="/hu/setahajozas-a-dunan-vacsoraval">a legjobb vacsorás hajóutak Budapesten</a>.</p>
<h3>Találkozási pont</h3>
<p>🗺️ <strong>Találkozási pont: </strong>Legenda, 7-es kikötő, Vigadó tér (pesti oldal).<br/>🚋 <strong>Tömegközlekedés:</strong> 2-es villamos a Vigadó térig, vagy M1 a Vörösmarty térig.</p>""",
    qf_badge="Vacsora a Dunán", qf=[("Indulás", "Naponta 19:00"), ("Időtartam", "Kb. 2,5 óra"),
        ("Ár", "Felnőtt 110 € · gyerek 3-12 év 84 €"), ("Étel", "4 fogásos à la carte vacsora (gyerekeknek 3 fogás)"),
        ("Az árban", "Hajóút, üdvözlőital, élő zene, vacsora"), ("Nincs benne", "További italok"), ("Kikötő", "7-es kikötő, Vigadó tér")],
    chips=[("yes", "✓ Asztalhoz felszolgálva"), ("yes", "✓ Élő zene"), ("yes", "✓ Fűtött üvegtető"), ("no", "✕ Italok külön")],
    perks=["Kikötő: <strong>7-es</strong>", "Indulás: <strong>19:00</strong>"],
    desc="Gyertyafényes, 4 fogásos à la carte vacsorás hajóút élő zenével a Dunán, naponta 19:00-kor.",
)
C["rudas"] = dict(
    rank="#4 A legjobb esti fürdő", title="Rudas fürdő 3 fogásos étkezéssel", dur="3-4 óra", place="Erzsébet híd",
    map="Rudas Thermal Bath Budapest", psub="felnőtt • fürdő + 3 fogásos étkezés",
    tested_pop="<strong>A Rudasban én is jártam.</strong> A tetőmedencében és a török fürdőben is ültem, amiről itt írok.",
    pills=[("🌙", "Éjszakai fürdő péntek, szombat", "<strong>Éjszakai fürdőzés</strong> pénteken és szombaton 22:00 és 3:00 között (csak online jegy, külön kell venni). "
            "Wellness: hétfő 6:00-22:00, kedd-vasárnap 6:00-20:00."),
           ("🏊", "Tetőmedence 36 °C", "36 °C-os panorámamedence a tetőn dunai kilátással, lent pedig hat török medence 16 és 42 °C között egy 16. századi kupola alatt."),
           ("🍽️", "3 fogásos étkezés az árban", "Ez a jegy egy napijegyet és egy 3 fogásos étkezést tartalmaz a Rudas Bistróban: wellness + kávé 74,99 €, wellness + bor 76,99 €, török fürdő + wellness 84,99 €."),
           ("🚻", "Nézd meg a napot", "A török fürdőben vannak férfi- és női napok: férfiaknak hétfőn, csütörtökön és pénteken 6:00-10:45 és szerdán egész nap; nőknek kedden. Hétvégén koedukált."),
           ("🔞", "14 év felett", "14 év alatti gyerekeket nem engednek be, és jelenleg nincs akadálymentes bejutás.")],
    pick="ha egy sötét novemberi délutánon forró tetőmedencében akarsz ülni a Duna felett, alatta az oszmán kupolával.",
    skip="14 év alatti gyerekkel, vagy ha étkezés nélküli sima belépőt szeretnél.",
    pros=["Forró tetőmedence dunai kilátással, sötétedés után a legjobb", "16. századi török fürdő kőkupola alatt", "Éjszakai fürdőzés pénteken és szombaton"],
    cons=["Férfi- és női napok a török részen", "14 év alatt nem lehet bemenni"],
    body="""<p>Egy szürke novemberi napra a Rudas a kedvencem. A <strong>tetőmedence 36 °C-os</strong>, és a Dunán át a Parlamentre és a hidakra néz, amelyek 16 óra után kigyulladnak. Lent a <strong>16. századi kupola alatti török fürdőben</strong> hat medence van 16 és 42 °C között. <strong>Pénteken és szombaton 22:00-tól 3:00-ig éjszakai fürdőzés</strong> is van.</p>
<p>A Rudasban én is jártam. Menj délután, nézd végig a tetőről, ahogy kigyulladnak a fények, aztán edd meg a jegyhez járó 3 fogásos ebédet vagy vacsorát.</p>
<h3>Kinek ajánlom</h3>
<p><strong>Válaszd</strong>, ha a Széchenyi már megvolt, vagy kisebb, régebbi fürdőt szeretnél a város legjobb kilátásával.</p>
<p><strong>Hagyd ki</strong>, ha vegyes párként épp egynemű napra esne a török rész (nézd meg fent a pillt), vagy ha gyerekkel jössz.</p>
<h3>Így jutsz oda</h3>
<p>🚋 <strong>Tömegközlekedés:</strong> 19-es vagy 41-es villamos, illetve 7-es busz a Rudas fürdő megállóig, az Erzsébet híd budai hídfőjénél.</p>""",
    qf_badge="Erzsébet híd", qf=[("Nyitvatartás", "Wellness hétfő 6:00-22:00, kedd-vasárnap 6:00-20:00"),
        ("Éjszakai fürdő", "Péntek és szombat 22:00-3:00 (külön online jegy)"), ("Jegy", "Napijegy + 3 fogásos étkezés 74,99 €-tól"),
        ("Tetőmedence", "36 °C"), ("Életkor", "14 év felett"), ("Közlekedés", "19-es, 41-es villamos · 7-es busz")],
    chips=[("yes", "✓ Forró tetőmedence"), ("yes", "✓ Étkezés az árban"), ("yes", "✓ Éjszakai fürdő hétvégén"), ("no", "✕ Egynemű napok")],
    perks=["Helyszín: <strong>Erzsébet híd</strong>", "Tetőmedence: <strong>36 °C</strong>"],
    desc="Rudas fürdő napijegy 3 fogásos étkezéssel, panorámás tetőmedencével és oszmán kori török fürdővel.",
)
C["vampire"] = dict(
    rank="#5 A legjobb esti séta", title="Vámpírok és legendák: éjszakai séta a budai Várban", dur="2 óra", place="Clark Ádám tér",
    map="Clark Adam ter Budapest", psub="fő • 20:00-kor indul",
    tested_pop="<strong>Ezt a sétát én is végigcsináltam</strong>, a 20:00-s angol nyelvű túrán.",
    pills=[("🕗", "20:00-kor indul", "November 21-én, szombaton az angol nyelvű séta <strong>20:00-kor</strong> indul. Kb. 2 óra."),
           ("🧛", "Mesék, nem évszámok", "Nagyjából tíz történet vámpírokról, kísértetekről és kelet-európai mítoszokról a Várnegyed udvarain, a Mátyás-templomnál és a Halászbástyánál."),
           ("🪜", "Lépcsővel indul", "5-10 perc lépcsőzés fel a Várhegyre a Clark Ádám térről. Plusz 10 euróért a Sikló is opció."),
           ("👥", "20-25 fős csoport", "Az én csoportom 20-25 fős volt. Angol, német és spanyol nyelvű séták vannak meghirdetve. 10 év felett.")],
    pick="olyan novemberi estére, ami sötétben jobb: a Várhegy lámpafénynél, egy mesélővel.",
    skip="ha történelmet és évszámokat szeretnél: ez folklór és színház.",
    pros=["Sötétre tervezve: éjjel üres és kivilágított a Várnegyed", "20 € két óráért egy mesélő idegenvezetővel", "Több mint 4600 vendég értékelte 4,6-ra"],
    cons=["Lépcső az elején", "A második fele kicsit ismétlődő"],
    body="""<p>A legtöbb gyalogtúra veszít novemberben: 16 órára sötét és hideg van. Ezt a sétát viszont pont erre találták ki. <strong>20:00-kor indul a Clark Ádám térről</strong>, felmegy a Várhegyre, és <strong>két órán át vámpír-, kísértet- és népmeséket</strong> mesél a Mátyás-templom és a Halászbástya körüli kihalt, lámpafényes udvarokon.</p>
<p>Ezt a sétát én is végigcsináltam. Az idegenvezetőnk improvizációs színészként dolgozott, az első fele lebilincselő volt. Hat-hét történet után kicsit ismétlődővé vált, de a helyszín elviszi.</p>
<h3>Kinek ajánlom</h3>
<p><strong>Válaszd</strong> a hajóút utáni estére, vagy kamaszokkal (10 év felett).</p>
<p><strong>Hagyd ki</strong>, ha tényeket és évszámokat keresel: a <a href="#item-8-buda-castle-walking-tour">délelőtti várséta</a> 12 euróért elmondja a történelmet. Több séta összehasonlítva: <a href="/hu/legjobb-gyalogtúrák-budapest">a legjobb budapesti gyalogtúrák</a>.</p>
<h3>Találkozási pont</h3>
<p>🗺️ <strong>Találkozási pont: </strong>Clark Ádám tér, a Nulla kilométerkő mellett, a Siklónál.<br/>🚌 <strong>Tömegközlekedés:</strong> 16-os, 105-ös vagy 178-as busz a Deák Ferenc térről vagy az Erzsébet térről, vagy gyalog át a Lánchídon.</p>""",
    qf_badge="Várnegyed", qf=[("Indulás", "20:00 (angolul, szombat, nov. 21.)"), ("Időtartam", "Kb. 2 óra"), ("Ár", "20 €-tól / fő"),
        ("Útvonal", "Várnegyedi udvarok, Mátyás-templom, Halászbástya"), ("Életkor", "10 év felett"),
        ("Találkozási pont", "Clark Ádám tér, a Nulla kilométerkőnél")],
    chips=[("yes", "✓ Sötétre tervezve"), ("yes", "✓ 40 € alatt"), ("yes", "✓ Ingyenes lemondás"), ("no", "✕ Lépcső az elején")],
    perks=["Indulás: <strong>Clark Ádám tér</strong>", "Időpont: <strong>20:00</strong>"],
    desc="Kétórás éjszakai séta a budai Várnegyedben vámpír- és népmesékkel, 20 eurótól.",
)
C["silverline"] = dict(
    rank="#6 A legjobb ár-érték vacsorahajó", title="Dinner &amp; Lights 4 fogásos vacsorás hajóút", dur="2 óra", place="11-es kikötő",
    map="Silverline Cruises Dock 11 Budapest", psub="felnőtt • 19:00",
    tested_pop="<strong>A Silverline vacsorás hajóútját én is kipróbáltam</strong>, a 11-es kikötőből.",
    pills=[("🕒", "19:00 · 2 óra", "<strong>19:00-kor</strong> indul, kb. 2 óra. A beszállás 45 perccel előtte kezdődik; legalább 30 perccel korábban érkezz."),
           ("🍽️", "4 fogás felszolgálva", "1 előétel, 2 leves, 4 főétel (diós tőkehal, sertésszűz, curry-s báránykaraj vagy vegetáriánus édesburgonya) és 3 desszert."),
           ("🎭", "Műsoros változat", "A Dinner &amp; Lights háttérzenével megy. Ugyanez a hajó és menü folklór- és operettműsorral 91 eurótól."),
           ("🪟", "Ablak melletti hely +15 €", "A garantált ablak melletti hely fejenként 15 euróval több. Egy üdvözlőital az árban; a többi italt a fedélzeten fizeted."),
           ("🌱", "Diétás kérések", "Vegetáriánus főétel az étlapon. Glutén- és laktózmentes, valamint vegán ételt előre kérhetsz.")],
    pick="felszolgált 4 fogásos dunai vacsoráért, 33 euróval olcsóbban, mint a Legenda.",
    skip="ha az alapárért garantált ablakhelyet akarsz: az 15 euró felár.",
    pros=["4 fogásos felszolgált vacsora 77 eurótól", "Vegetáriánus főétel, kérésre vegán", "Folklór- és operettműsorral is kérhető"],
    cons=["Az ablakhely felár", "Az üdvözlőitalon túl az italok külön"],
    body="""<p>Ha a vacsorás hajó a terv, de a 110 euró sok, ez a csere. A Silverline <strong>Dinner &amp; Lights</strong> ajánlata <strong>felszolgált, 4 fogásos vacsora</strong> (diós tőkehal, sertésszűz, báránykaraj vagy vegetáriánus főétel) egy <strong>2 órás, 19:00-kor induló</strong> hajóúton, <strong>77 eurótól</strong>.</p>
<p>A Silverline vacsorás hajóútját én is kipróbáltam. Fizesd ki a <strong>15 eurót az ablakhelyért</strong>: novemberben végig sötétben hajózol, és a kilátás a fele annak, amiért fizetsz.</p>
<h3>Kinek ajánlom</h3>
<p><strong>Válaszd</strong> közepes keretből, vagy ha vegetáriánus is van a társaságban.</p>
<p><strong>Hagyd ki</strong> különleges alkalomra: <a href="#item-3-legenda-candlelit-dinner">a Legenda gyertyafényes hajója</a> az elegánsabb este.</p>
<h3>Találkozási pont</h3>
<p>🗺️ <strong>Találkozási pont: </strong>Silverline, Jane Haining rakpart, 11-es kikötő, az Erzsébet hídnál (pesti oldal).<br/>🚋 <strong>Tömegközlekedés:</strong> 2-es villamos, vagy M1 a Vörösmarty térig.</p>""",
    qf_badge="Vacsora a Dunán", qf=[("Indulás", "19:00"), ("Időtartam", "Kb. 2 óra"), ("Ár", "77 €-tól · ablakhely +15 €"),
        ("Étel", "4 fogásos felszolgált menü"), ("Az árban", "Hajóút, vacsora, üdvözlőital"), ("Kikötő", "11-es kikötő, Jane Haining rakpart")],
    chips=[("yes", "✓ 4 fogás felszolgálva"), ("yes", "✓ Vegetáriánus főétel"), ("no", "✕ Ablakhely felár")],
    perks=["Kikötő: <strong>11-es</strong>", "Indulás: <strong>19:00</strong>"],
    desc="Kétórás, 4 fogásos vacsorás hajóút a Dunán 19:00-kor, 77 eurótól.",
)
C["foodapest"] = dict(
    rank="#7 A legjobb gasztrotúra", title="Foodapest gasztrotúra a vásárcsarnoktól a kocsmáig, borral", dur="3 óra", place="Központi Vásárcsarnok",
    map="Central Market Hall Budapest", psub="fő • 11:30-as csarnoktúra",
    pills=[("🏛️", "Csarnok + étterem", "A Központi Vásárcsarnokban indul, utána egy pékség és két helyi étterem. Az utolsó állomás a borkóstoló."),
           ("🍽️", "12+ kóstoló", "Felvágottak, savanyúság, gulyás, lángos, kürtőskalács és egy magyar desszert: egy ebédnek is elmegy."),
           ("🕒", "11:30 vagy 17:00", "A 11:30-as csarnoktúra 69 €. A 17:00-s esti túra (street food, bor, pálinka, kézműves sör, csarnok nélkül) 79 €."),
           ("🍷", "Bor és pálinka", "Borkóstoló az utolsó étteremben, közben egy házi pálinka. Alkoholmentes csere is kérhető.")],
    pick="egy hideg novemberi délre, amit nagyrészt fedett helyen töltesz, a csarnoktól egy kocsmáig evve.",
    skip="ha aznap este vacsorás hajó jön, és nem vagy nagyevő.",
    pros=["Közel 700 vendég értékelte 4,9-re", "Nagyrészt fedett helyen, ez novemberben számít", "Egy étkezést kivált"],
    cons=["3 óra talpon", "Az esti változat kihagyja a vásárcsarnokot"],
    body="""<p>November a vásárcsarnok-idő. Ez a túra <strong>11:30-kor</strong> indul a <strong>Központi Vásárcsarnokban</strong>, <strong>12+ kóstolón</strong> (gulyás, lángos, kürtőskalács, felvágottak) megy végig egy pékségben és két helyi étteremben, és <strong>magyar borkóstolóval</strong> zárul. A 3 óra nagy része fedett helyen telik, és kora délután végzel, maradt még fény egy fürdőhöz.</p>
<h3>Kinek ajánlom</h3>
<p><strong>Válaszd</strong> az első teljes napodon: utána tudni fogod, mit rendelj a többi napon. A 11:30-as túra 69 €.</p>
<p><strong>Hagyd ki</strong>, ha este vacsorás hajó jön, és keveset eszel. Kilenc gasztrotúra összehasonlítva: <a href="/best-food-tours-budapest">a legjobb budapesti gasztrotúrák</a> (angolul).</p>
<h3>Találkozási pont</h3>
<p>🗺️ <strong>Találkozási pont: </strong>Központi Vásárcsarnok, Fővám tér (a pontos helyet a voucher tartalmazza).<br/>🚇 <strong>Tömegközlekedés:</strong> M4 a Fővám térig, vagy 2-es, 47-es, 49-es villamos.</p>""",
    qf_badge="Étel + bor", qf=[("Indulások", "11:30 csarnoktúra · 17:00 esti túra (csarnok nélkül)"), ("Időtartam", "Kb. 3 óra"),
        ("Ár", "69 € (11:30) · 79 € (17:00)"), ("Étel", "12+ kóstoló"), ("Italok", "Borkóstoló, pálinka"), ("Indulás helye", "Központi Vásárcsarnok, Fővám tér")],
    chips=[("yes", "✓ Nagyrészt fedett helyen"), ("yes", "✓ Bor az árban"), ("yes", "✓ Ingyenes lemondás")],
    perks=["Indulás: <strong>Vásárcsarnok</strong>", "Kóstolók: <strong>12+</strong>"],
    desc="Háromórás budapesti gasztrotúra a Központi Vásárcsarnoktól egy helyi étteremig, 12+ kóstolóval és borral.",
)
C["castle"] = dict(
    rank="#8 A legjobb délelőtti séta", title="Gyalogtúra a budai Várnegyedben", dur="2 óra", place="Szentháromság tér",
    map="Szentháromság tér Budapest", psub="fő • 2 óra",
    tested_pop="<strong>Ezt a túrát én is végigcsináltam.</strong>",
    pills=[("🏰", "A Várhegy 2 órában", "Mátyás-templom, Halászbástya és a Várnegyed régi utcái idegenvezetővel."),
           ("☀️", "Menj 14:00 előtt", "16 óra körüli napnyugtával egy délelőtti időpont adja a dunai kilátást nappali fényben."),
           ("🎄", "Budavári Advent nov. 27-től", "November 27-től a Budavári Advent vásár tölti meg a Szentháromság teret, pont ott, ahol a túra indul."),
           ("💶", "12 eurótól", "A lista legolcsóbb vezetett programja.")],
    pick="olcsó, vezetett délelőttre a Várhegyen, amíg jó a fény.",
    skip="délutánra: fél négyre már megy a fény.",
    pros=["12 € egy 2 órás vezetett sétáért", "Több mint 2400 vendég értékelte 4,6-ra", "Nappal a legszebb a kilátás a folyóra"],
    cons=["2 óra a szabadban, hidegben", "A templombelsők külön fizetendők"],
    body="""<p>A Várhegy novemberben nappali program. Ez a <strong>2 órás, 12 eurós vezetett séta</strong> végigviszi a Mátyás-templomon, a Halászbástyán és a Várnegyed régi utcáin, és a Szentháromság téren indul.</p>
<p>Ezt a túrát én is végigcsináltam. Délelőttre foglald, aztán sötétedés után gyere vissza az ingyenesen bejárható, kivilágított Bástyához, vagy a <a href="#item-5-vampire-night-walk">vámpíros éjszakai sétára</a>.</p>
<h3>Kinek ajánlom</h3>
<p><strong>Válaszd</strong> egy száraz délelőttre, a történelemért és a legszebb dunai kilátásért.</p>
<p><strong>Hagyd ki</strong>, ha csak a kilátás kell: a Halászbástya alsó teraszai ingyenesek.</p>
<h3>Találkozási pont</h3>
<p>🗺️ <strong>Találkozási pont: </strong>Szentháromság tér, a Mátyás-templomnál.<br/>🚌 <strong>Tömegközlekedés:</strong> 16-os busz a Deák Ferenc térről, vagy a Budavári Sikló a Clark Ádám térről.</p>""",
    qf_badge="Várnegyed", qf=[("Időtartam", "2 óra"), ("Ár", "12 €-tól / fő"), ("Útvonal", "Mátyás-templom, Halászbástya, Várnegyed"),
        ("Legjobb időpont", "Délelőtt, 14:00 előtt"), ("Közlekedés", "16-os busz, Budavári Sikló")],
    chips=[("yes", "✓ A legolcsóbb"), ("yes", "✓ Ingyenes lemondás"), ("no", "✕ Szabadban, hidegben")],
    perks=["Indulás: <strong>Szentháromság tér</strong>", "Időtartam: <strong>2 óra</strong>"],
    desc="Kétórás vezetett gyalogtúra a budai Várnegyedben, 12 eurótól.",
)

ANCHORS = {"legenda-evening": "item-1-legenda-evening-cruise", "szechenyi": "item-2-szechenyi-thermal-bath",
           "legenda-dinner": "item-3-legenda-candlelit-dinner", "rudas": "item-4-rudas-thermal-bath",
           "vampire": "item-5-vampire-night-walk", "silverline": "item-6-silverline-dinner-cruise",
           "foodapest": "item-7-foodapest-food-tour", "castle": "item-8-buda-castle-walking-tour"}


def A(k):
    return "#" + ANCHORS[k]


LEAD = f"""<p>November közepén <strong>16:07-kor megy le a nap</strong>, november 30-án már 15:55-kor. A legtöbb útmutató ezt a hónap hátrányaként kezeli. Én inkább köré tervezném a napot: Budapest legszebb látnivalói a kivilágítottak, és novemberben már akkor égnek a fények, amikor még a délutáni kávédat iszod.</p>
<p>Lent a 8 program, amit novemberre foglalnék, ebből 7-et magam is kipróbáltam, plusz a <a href="#november-dates">dátumok, amik átírják a tervet</a> (a karácsonyi vásárok november 13-án és 27-én nyitnak) és az <a href="#free-things">ingyenes esték</a>. Csak egy estéd van? Foglald le <a href="{A('legenda-evening')}"><strong>a Legenda esti hajóútját</strong></a> (25 €, 16:20-tól 20 percenként).</p>"""

PICKS_H = "Gyors választás novemberre"
PICKS = [("Az első estédre", "legenda-evening", "25 €, egy óra, 16:20-tól 20 percenként"),
         ("Forró medence hideg levegőben", "szechenyi", "39 €-tól, pénteken 22:00-ig nyitva"),
         ("Romantikus vacsora a folyón", "legenda-dinner", "110 €, naponta 19:00, 4 fogás felszolgálva"),
         ("Fürdő kilátással, sötétedés után", "rudas", "36 °C-os tetőmedence, éjszakai fürdő pénteken és szombaton"),
         ("Program este 8-ra", "vampire", "20 €, két óra népmese a Várhegyen"),
         ("Vacsorás hajó olcsóbban", "silverline", "77 €-tól, 4 fogás 19:00-kor"),
         ("Esős délre", "foodapest", "69 €, nagyrészt fedett helyen, 12+ kóstoló"),
         ("Kis keretből", "castle", "12 eurós vezetett séta a Várhegyen")]

DATES_H = "Novemberi dátumok, amik átírják a tervet"
DATES_INTRO = "November második felében két dolog történik: elindul a karácsonyi szezon, és változnak az esti menetrendek. Mi mikor kezdődik:"
DATES_COLS = ["Dátum", "Mi", "Miért számít"]
DATES_ROWS = [
    ("Nov. 13.", "Megnyílt az Advent Bazilika és a Vörösmarty téri karácsonyi vásár", "A két nagy belvárosi vásár mostantól nyitva, ingyenes belépéssel. <a href=\"#christmas-markets-november\">Nyitvatartás lent</a>."),
    ("Nov. 20.", "A Városligeti Műjégpálya tervezett nyitása", "A Vajdahunyad vára előtti jégpálya a tervek szerint november 20-án nyit; jegyek a saját oldalán, a mujegpalya.hu-n."),
    ("Nov. 23.", "A Legenda 15:40-es esti hajót is indít", f"November 22-ig az első esti hajó 16:20-kor indul. November 23-tól 15:40-kor is van indulás. <a href=\"{A('legenda-evening')}\">A hajóút</a>."),
    ("Nov. 27.", "Nyit a Budavári Advent és az Advent Óbudán", "Megnyílik a várhegyi és az óbudai vásár, és ugyanezen a napon indul az ingyenes óbudai Fő téri jégpálya."),
    ("Nov. 27-29.", "Art Weekend Budapest", "Galériák, műtermek és projektterek nyitják meg kapuikat a városban. Ingyenes; a vezetett sétákra regisztrálni kell."),
    ("Egész hónap", "Bonjour Monsieur Gauguin", "A Szépművészeti Múzeum Gauguin-kiállítása 2026. október 30. és 2027. február 28. között látogatható. Kedd-vasárnap 10:00-18:00, hétfőn zárva."),
    ("Egész hónap", "Lumina Park", "Bejárható fénypark a margitszigeti Palatinuson, 16:30 és 21:00 között, hétfőn zárva. Jegyek 5000 Ft-tól."),
]
DATES_NOTE = "A dátumok a szervezők saját oldaláról származnak. A jégpálya nyitása tervezett időpont, az időjárás miatt változhat."

SEASON_H = "Novemberi időjárás és napfény Budapesten"
SEASON_P = ("Számíts <strong>nappal 9, éjjel 3 fok körülire</strong>: a havi középhőmérséklet 5,9 °C, a csapadék nagyjából <strong>48 mm</strong> "
            "(HungaroMet, 1991-2020-as átlag). Többnyire szürke az ég, és a hónap végére hidegebb lesz. "
            "Hozz meleg, vízálló kabátot és jól tapadó cipőt a várhegyi macskakövekre.")
SUN_COLS = ["Dátum", "Napkelte", "Napnyugta", "Nappal hossza"]
SEASON_TIP = ("<strong>Hogyan használd ki a rövid napokat:</strong> szabadtéri látnivalók és vásárcsarnok 9 és 14 óra között, "
              "fürdő szürkületkor, fél öt után pedig hajóút, vacsora vagy éjszakai séta.")

XMAS_H = "Karácsonyi vásárok novemberben"
XMAS_P = ("Nem kell decemberig várni. A két nagy belvárosi vásár <strong>november 13-án megnyílt</strong>, a várhegyi és az óbudai pedig "
          "<strong>november 27-én</strong> nyit. Mind a négy ingyenes. A Bazilika homlokzatán 17:30-tól félóránként 3D-s fényfestés van.")
XMAS_COLS = ["Vásár", "Dátum", "Nyitvatartás"]
XMAS_LINK = ("Standok, ételárak, sétaidők és egy egyestés útvonal: <a href=\"/hu/karacsonyi-vasar-budapest\">budapesti karácsonyi vásárok 2026</a>. "
             "Decemberben is maradsz? Nézd meg, <a href=\"/hu/budapest-programok-december\">mit csinálj Budapesten decemberben</a>.")

FREE_H = "Ingyenes novemberi programok"
FREE = [
    ("Sétálj a folyóparton sötétedés után", "A pesti rakparton a Lánchíd és a Parlament között ingyen kapod meg a kivilágított Várat, a hidakat és a Parlamentet, nagyjából 16:30-tól."),
    ("Járd végig a karácsonyi vásárokat", "Az Advent Bazilika és a Vörösmarty tér ingyenes, öt percre van egymástól, és naponta 11:00-tól nyitva. A Bazilika fényfestése 17:30-tól megy."),
    ("Menj fel a Várhegyre este", "A Várnegyed és a Halászbástya alsó teraszai ingyenesek, és sötétedés után szinte üresek."),
    ("Korcsolyázz Óbudán", "Az óbudai Fő téri jégpálya november 27-től ingyenes (vasárnap-csütörtök 8:00-21:00, péntek-szombat 22:00-ig)."),
    ("Art Weekend Budapest", "November 27. és 29. között galériák és műtermek nyitnak ki ingyen a városban."),
]

MORE_H = "További novemberi ötletek"
MORE = [
    ("Minden esti hajó összehasonlítva", "Tíz esti és éjszakai hajóút egymás mellett, ebből 6-ot kipróbáltam: <a href=\"/hu/legjobb-éjszakai-hajóutak-budapest\">a legjobb éjszakai hajóutak Budapesten</a>."),
    ("Minden termálfürdő összehasonlítva", "Hat fürdő nyitvatartással és árakkal, ebből 4-et kipróbáltam: <a href=\"/hu/legjobb-termalfurdok-budapest\">a legjobb budapesti termálfürdők</a>."),
    ("A Parlament", "Vezetett túrák egész évben, este pedig ki van világítva az épület: <a href=\"/hu/budapest-attractions/budapest-parlament\">Parlament jegyek és tippek</a>."),
    ("Múzeumok esős napokra", "Megéri-e a Budapest Card egy múzeumos útra: <a href=\"/hu/budapest-card-megéri-e\">Budapest Card, megéri?</a>"),
    ("Egész éves kedvencek", "A klasszikusok bármelyik hónapra: <a href=\"/best-things-to-do-budapest\">Budapest 10 legjobb látnivalója</a> (angolul)."),
]
DEC_LINK = ("Később jössz? Nézd meg, <a href=\"/hu/budapest-programok-december\">mit csinálj Budapesten decemberben</a>.")

FAQ = [
    ("Megéri novemberben Budapestre menni?",
     "Igen, ha a sötétség köré tervezel. Rövidek a napok (16 óra körül megy le a nap), gyakran szürke és 9 fok körül van, de a városban korán kigyulladnak a fények, "
     "a fürdők kültéri medencéi a hidegben a legjobbak, és november 13-tól nyitva vannak a belvárosi karácsonyi vásárok."),
    ("Milyen az időjárás Budapesten novemberben?",
     "Hűvös és gyakran szürke: nappal kb. 9, éjjel 3 fok, a hónapban nagyjából 48 mm csapadékkal (1991-2020-as átlag). "
     "A hónap során a nap 6:27 és 7:09 között kel, és 16:26 és 15:55 között nyugszik."),
    ("Nyitva vannak a budapesti karácsonyi vásárok 2026 novemberében?",
     "Igen. Az Advent Bazilika (Szent István tér) és a Vörösmarty tér 2026. november 13-án nyitott. A várhegyi Budavári Advent és az Advent Óbudán november 27-én nyit. "
     "Mind ingyenes. Részletek: <a href=\"/hu/karacsonyi-vasar-budapest\">budapesti karácsonyi vásárok 2026</a>."),
    ("Nyitva vannak a termálfürdők novemberben?",
     "Igen, egész évben. A Széchenyi kültéri medencéi nyitva vannak (a termálmedence 36-38 °C); hétfőtől csütörtökig 7:00-20:00, pénteken 22:00-ig, hétvégén 8:00-20:00 között. "
     "A Rudasban pénteken és szombaton 22:00 és 3:00 között éjszakai fürdőzés van."),
    ("Járnak a dunai hajók novemberben?",
     f"Igen. <a href=\"{A('legenda-evening')}\">A Legenda esti hajója</a> 16:20 és 21:00 között 20 percenként indul, november 23-tól 15:40-kor is. "
     f"A vacsorás hajók 19:00-kor indulnak, például <a href=\"{A('legenda-dinner')}\">a Legenda gyertyafényes vacsorája</a> (110 €) és <a href=\"{A('silverline')}\">a Silverline Dinner &amp; Lights</a> (77 €-tól)."),
    ("Mit csináljak Budapesten egy esős novemberi napon?",
     f"Menj fürdőbe (a Rudas tetőmedencéje bármilyen időben meleg), vegyél részt a nagyrészt fedett helyen zajló <a href=\"{A('foodapest')}\">Foodapest csarnoktúrán</a>, "
     "vagy nézd meg a Gauguin-kiállítást a Szépművészeti Múzeumban (kedd-vasárnap 10:00-18:00)."),
    ("Mikor nyit a Városligeti Műjégpálya 2026-ban?",
     "A tervek szerint 2026. november 20-án. Az időpont az időjárás miatt változhat, indulás előtt nézd meg a mujegpalya.hu-t. Az óbudai Fő téri kisebb pálya november 27-től ingyenes."),
    ("Mit lehet csinálni Budapesten novemberben este?",
     f"Fél öttől sötét van, így hosszúak az esték: <a href=\"{A('legenda-evening')}\">egyórás esti hajóút</a>, fürdő sötétedés után (a Széchenyi pénteken 22:00-ig), "
     f"a 20:00-kor induló <a href=\"{A('vampire')}\">vámpíros éjszakai séta</a>, a karácsonyi vásárok 21:00-ig vagy tovább, vagy a margitszigeti Lumina Park."),
]

METHOD_H = "Így választottam ki a programokat"
METHOD = ("Minden kártya árát, indulási idejét, tartalmát és értékelését az adott termék élő oldalán néztem meg, a Legenda indulásait a 2026-os menetrendjében. "
          "A vásárok dátumai a szervezők oldaláról, a fürdők nyitvatartása a hivatalos fürdőoldalakról, a napkelte és napnyugta a timeanddate.com-ról, "
          "az éghajlati adatok a HungaroMet 1991-2020-as budapesti átlagaiból származnak. "
          "A \"Kipróbáltam\" jelölés csak azon a hét programon van, amit magam csináltam; a gasztrotúra az, amit nem.")

HOMECARD = ("Budapest novemberben", "")
MENU_SUB = "Esti hajók, forró medencék, vásárnyitás"
MENU_TITLE = "Budapest novemberben"

TEMPLATE_STRINGS = [
    (">Check Availability →</a>", ">Időpontok és jegyek →</a>"),
    ("      Check Availability →", "      Időpontok és jegyek →"),
    (">Table of Contents<", ">Tartalomjegyzék<"),
]

_HU_MONTH = {"Nov": "nov."}


def DAY(d):
    n, m = d.split()
    return f"{_HU_MONTH[m]} {n}."


def DUR(c):
    return c.replace(" h ", " óra ").replace(" min", " perc")


_MON = ["jan.", "febr.", "márc.", "ápr.", "máj.", "jún.", "júl.", "aug.", "szept.", "okt.", "nov.", "dec."]


def _d(iso, year=False):
    y, m, d = (int(x) for x in iso.split("-"))
    return (f"{y}. " if year else "") + f"{_MON[m - 1]} {d}."


def SPAN(a, b):
    return f"{_d(a)} - {_d(b, year=b[:4] != '2026')}"


def _h(v):
    return v


def HOURS(m):
    h = m["hours"]
    if "fri" in h:
        return f"Hétfő-csütörtök {h['mon_thu']} · péntek {h['fri']} · szombat {h['sat']} · vasárnap {h['sun']}"
    if h["mon_thu"] == h["fri_sat"] == h["sun"]:
        return f"Naponta {h['mon_thu']}"
    return f"Vasárnap-csütörtök {h['mon_thu']} · péntek-szombat {h['fri_sat']}"
