# -*- coding: utf-8 -*-
"""
Canonical Hungarian Subpoints Data for Budapest Adventures Boat Articles.
Translates all onboard walkthrough, audio guide, dining, and operator cards
for River (10 cards) and Dinner (7 cards).
"""

RIVER_SUBPOINTS = {
    0: {  # Card 1: Legenda City Cruises
        'Sightseeing & Views': {
            'h4': 'Városnézés és Kilátás',
            'lis': [
                ("Mint minden budapesti sétahajózáson, a városkép lenyűgöző az út során.", "A legjobb kilátásért és fotózási pozícióért a felső nyitott fedélzetre érdemes ülni."),
                ("A hajó útvonala", "Budapest összes fontos folyóparti nevezetességét érinti, egészen a Művészetek Palotájáig és a Nemzeti Színházig.")
            ]
        },
        'Rooftop Waiting Area': {
            'h4': 'Tetőtéri Váróterasz',
            'lis': [
                ("A lépcsőn felmenve a tetőtéri, nyitott váróteraszra érkezünk,", "ahol friss levegőn, a budapesti panorámában gyönyörködve várhatjuk a beszállást.")
            ]
        },
        'Welcome Drink': {
            'h4': 'Üdvözlőital',
            'lis': [
                ("A beszállás után a vendégeket azonnal üdvözlőitallal köszöntik:", "választható minőségi pezsgő, bor, sör, üdítő vagy ásványvíz, a nyári főszezonban pedig egy extra frissítő limonádé is jár.")
            ]
        },
        'The Ship(s)': {
            'h4': 'A Hajó és Fedélzet',
            'ps': ['Gondola hajó', 'Legenda / Danube Legend hajó', 'Duna Bella hajó'],
            'lis': [
                ("A Legenda City Cruises három modern városnéző hajót üzemeltet,", "amelyek hasonló prémium élményt nyújtanak, de méretükben különböznek."),
                ("Gondola:", "A legkorszerűbb és legkényelmesebb hajó a teljes budapesti dunai flottában (tesztelve: 2023 őszén)."),
                ("Legenda:", "A Gondola valamivel kisebb és karcsúbb testvérhajója (tesztelve: 2025 októberében)."),
                ("Duna Bella:", "Elsősorban a nappali járatokon használt hajó, keskenyebb felső kilátófedélzettel."),
                ("Méretbeli különbségek:", "A fő eltérés a hajók méretében és a felső terasz kialakításában rejlik; még a kisebb hajókon is bőséges a hely és kitűnő a kilátás."),
                ("Hajótípus-kiosztás:", "A forgalomtól és karbantartástól függően a Legenda nem garantál előre konkrét hajótípust."),
                ("A Gondola felszereltsége:", "Modern, letisztult szalon, nyáron elhúzható panorámaablakok, fedélzeti bár, fülhallgatós audio guide és klíma/fűtés."),
                ("Menetrendi indítás:", "A Gondola általában 16:30 után indul a népszerű naplementés és esti járatokra."),
                ("A Legenda testvérhajó:", "A Gondola kisebb változata, azonos prémium technikai felszereltséggel."),
                ("Új generációs audiorendszer:", "A Legenda hajón még kényelmesebb az audio guide fülhallgatója, és a felső fedélzeten menetiránynak háttal elhelyezett fotós ülések is találhatók."),
                ("Duna Bella kialakítás:", "Nappali városnézésre kiváló, zárt panorámaszalonja megbízható védelmet nyújt bármilyen időjárás esetén.")
            ]
        },
        'The Weather-Proof Waiting Area': {
            'h4': 'Időjárásálló Váróterem',
            'lis': [
                ("A Legenda az egyetlen társaság Budapesten,", "amely teljesen zárt, fűtött és légkondicionált úszómólós váróteremmel rendelkezik a Vigadó téren, megvédve a vendégeket az esőtől és a hidegtől."),
                ("Prémium kikötői infrastruktúra:", "Tiszta mosdók, mozgássérült-mosdó és babapelenkázó áll rendelkezésre a beszállás előtt.")
            ]
        },
        'Lower Deck': {
            'h4': 'Alsó Zárt Fedélzet',
            'ps': ['Hajó: Gondola', 'Hajó: Legenda'],
            'lis': [
                ("Hangulatos fedélzeti bár:", "Az alsó fedélzet végében egy jól felszerelt bár található. A kényelmes üléssorok és a hatalmas panorámaablakok fantasztikus kilátást garantálnak."),
                ("Kényelmes ülésrend:", "A Legenda alsó fedélzetén 2x3-as elrendezésű, kárpitozott ülések találhatók, mindegyiknél beépített audio guide csatlakozóval."),
                ("Panoráma üvegtető az orrban:", "A hajó orrában elhelyezkedő szekció átlátszó üvegplafonnal van felszerelve, így közvetlenül rálátni a felül elsuhanó hidakra és a Várhegyre.")
            ]
        },
        'The Upper Deck': {
            'h4': 'Felső Kilátófedélzet',
            'ps': ['Hajó: Gondola', 'Hajó: Legenda'],
            'lis': [
                ("360°-os akadálytalan panoráma:", "Tágas nyitott fedélzet minden szögből tökéletes rálátással, ideális fotózáshoz. Hűvös estéken ingyenes meleg takarók kérhetők."),
                ("Tükröződésmentes fotózás:", "A belső világítást az esti hajóutak alatt lekapcsolják, hogy az üvegfelületek ne tükröződjenek a fotókon."),
                ("Páros ülések és elhúzható ablakok:", "A felső fedélzeten kétszemélyes ülések találhatók. Az ablakok szükség esetén elcsúsztathatók a friss levegő és a tiszta fotók érdekében."),
                ("Fedett felső szekció:", "A Gondolával ellentétben a Legenda felső fedélzetének egy része fedett és időjárásvédett."),
                ("Nyitott hátsó terasz:", "A felső szint leghátsó része teljesen nyitott, ahol menetiránynak háttal ülve zavartalanul élvezhető az elvonuló város látképe.")
            ]
        },
        'The Audio Guide': {
            'h4': 'Audio Guide és Fejhallgatók',
            'ps': ['Hajó: Gondola', 'Hajó: Legenda'],
            'lis': [
                ("Egyéni fejhallgatós rendszer:", "Ez az egyetlen dunai sétahajó, ahol a narráció egyéni fülhallgatón szól, így a motorzaj és a többi utas beszélgetése nem zavarja az érthetőséget."),
                ("30 elérhető nyelv:", "Kiváló digitális hangminőség és professzionális színészi szinkron 30 különböző világnyelven."),
                ("Tartalmas narráció:", "A látnivalók ismertetése mellett érdekes legendák és budapesti várostörténeti anekdoták kísérik az utat."),
                ("Segítőkész személyzet:", "Ha a fülhallgató kábele sérült vagy rövid, a személyzet kérésre azonnal és készségesen kicseréli."),
                ("Ergonomikus kialakítás:", "A Legenda hajón még újabb fejhallgatók találhatók, állítható egyéni hangerőszabályzóval az üléseknél."),
                ("GPS-vezérelt szinkronizáció:", "A közvetítés automatikusan a hajó dunai haladásához és a nevezetességekhez igazodik."),
                ("Ingyenesen biztosított:", "A fejhallgató használata díjtalan, a jegyár teljes mértékben tartalmazza.")
            ]
        }
    },
    1: {  # Card 2: Rubin Group Prosecco Cruise
        'The Ship': {
            'h4': 'A Hajó és Fedélzet',
            'lis': [
                ("Háromszintes, tágas kialakítás:", "A hajó kifejezetten tágas, elegáns koktélparti hangulattal és kényelmes, kétszemélyes asztalokkal várja a vendégeket a zárt és nyitott fedélzeteken.")
            ]
        },
        'The Top Deck': {
            'h4': 'A Felső Nyitott Fedélzet',
            'lis': [
                ("360°-os zavartalan körpanoráma:", "A legfelső nyitott kilátóterasz akadálytalan kilátást nyújt a kivilágított budapesti látképre, ami a tavaszi és nyári estéken a legkiválóbb fotós pozíció.")
            ]
        },
        'The Mid and Bottom Deck': {
            'h4': 'Középső és Alsó Zárt Fedélzet',
            'lis': [
                ("Két kényelmes belső fedélzet:", "Két tágas, fűtött és klimatizált belső szalon áll rendelkezésre kényelmes ülőhelyekkel, ahol a hangulat kellemes, védett és hívogató."),
                ("Érdemes korán érkezni:", "A legfelső fedélzet legnépszerűbb helyei hamar megtelnek, ezért célszerű 15–20 perccel a kapunyitás előtt a kikötőbe érkezni.")
            ]
        },
        'The Drinks Refills': {
            'h4': 'Italfelszolgálás és Újratöltés',
            'lis': [
                ("Figyelmes és gyors kiszolgálás:", "A személyzet rendkívül aktív: amint kiürül a pohár, azonnal érkeznek és újratöltik a minőségi proseccót vagy bort."),
                ("Önkiszolgáló limonádépult:", "Friss limonádé is korlátlanul elérhető klasszikus citrusos és uborkás-mentás ízesítésben.")
            ]
        },
        'The Assorted Food Platter': {
            'h4': 'Az Opcionális Hidegtál',
            'lis': [
                ("Középszerű hidegtál 10 euróért:", "A feláras hidegtál egyszerű sajtokat, felvágottakat és péksüteményt tartalmaz, nem számít prémium gourmet fogásnak."),
                ("Kisebb adag a vártnál:", "Az adag mérete kifejezetten szerény a fotókhoz képest, így nem javasoljuk az extra kiadást."),
                ("Spóroljon az ételen:", "Érdemesebb a hajózás előtt vagy után vacsorázni a városban, a fedélzeten pedig a korlátlan italokra és a panorámára fókuszálni.")
            ]
        },
        'The Audio Guide': {
            'h4': 'Audio Guide és Hangosítás',
            'lis': [
                ("Hangszórós közvetítés:", "A fedélzeti hangszórós audiokalauz a beszélgető vendégek és a zene zaja miatt nehezen hallható a nyitott fedélzeten."),
                ("Alapszintű ismertető:", "A személyzet kérésre emeli a hangerőt, de a narráció inkább az alapvető nevezetességekre szorítkozik.")
            ]
        },
        'About Rubin Group': {
            'h4': 'A Rubin Group Hajótársaságról',
            'ps': [
                "A Rubin Group egy megbízható hazai hajózási társaság, amely 2015 óta üzemeltet járatokat a Dunán. A klasszikus városnéző túrák helyett elsősorban a hangulatos, korlátlan italfogyasztásos és gasztronómiai élményhajózásra specializálódtak."
            ]
        }
    },
    2: {  # Card 3: Kisfaludy Paddle Steamer
        'The Ship': {
            'h4': 'A Hajó és Történeti Kialakítás',
            'lis': [
                ("Autentikus 19. századi gőzhajó-élmény:", "A hajótúra a híres Kisfaludy lapátkerekes gőzös korhű másolatán zajlik, sárgaréz korlátokkal, szegecselt acéllemezekkel és nemesfa burkolattal.")
            ]
        },
        '19th Century Maritime Museum': {
            'h4': '19. Századi Hajózási Múzeum',
            'lis': [
                ("Fedélzeti tengerészeti kiállítás:", "Az alsó fedélzeten egy izgalmas hajózástörténeti mikromúzeum kapott helyet, amely bemutatja a dunai gőzhajózás aranykorát és Széchenyi reformkori törekvéseit.")
            ]
        },
        'The Drinks': {
            'h4': 'Üdvözlőital',
            'lis': [
                ("Ingyenes üdvözlőital:", "A jegyár egy pohár választott italt tartalmaz (minőségi pezsgő, bor, sör vagy üdítőital).")
            ]
        },
        'The Top Deck': {
            'h4': 'A Felső Kilátófedélzet',
            'lis': [
                ("Kompakt felső terasz:", "A kis méretű felső fedélzeten négy asztal található, ám a gőzkémény és a kormányállás kissé korlátozza a kilátást."),
                ("Meleg takarók hűvös időben:", "Esténként puha plédeket biztosítanak a nyitott fedélzeten ülőknek.")
            ]
        },
        'The Main Deck': {
            'h4': 'Főfedélzet és Orr-rész',
            'lis': [
                ("360°-os panoráma az orrban:", "A főfedélzet elülső részén nyitott terület található, amely tiszta, akadálytalan kilátást nyújt a folyóra."),
                ("Fedett hátsó sétafedélzet:", "A hátsó rész fedett, de nyitott oldalú, így megvéd a szemerkélő esőtől."),
                ("Nosztalgikus fűtött kabin:", "A belső szalon kényelmes fa padokkal és békebeli hangulattal fogadja az utasokat.")
            ]
        },
        'Sightseeing & Views': {
            'h4': 'Városnézés és Kilátás',
            'lis': [
                ("Csodálatos folyóparti látkép:", "A hajó a Parlamenttől a Budai Várig a Duna legszebb belvárosi szakaszán halad végig.")
            ]
        },
        'The Audio Guide': {
            'h4': 'Az Audio Guide és Zene',
            'lis': [
                ("Kétnyelvű hangszórós kommentár:", "A hajóút során magyar és angol nyelvű ismertető hallható a hangszórókból."),
                ("Kellemes hangerő:", "A közvetítés jól érthető a csendesebb folyami szakaszokon."),
                ("Történelmi nevezetességek:", "A kommentár a legfontosabb hidakra, palotákra és a gőzhajózás történelmére összpontosít."),
                ("Klasszikus zongorazene:", "A szöveges részek között kellemes klasszikus zongoradallamok szólnak.")
            ]
        },
        'About Dunai Sétahajózási Ltd.': {
            'h4': 'A Dunai Sétahajózási Kft.-ről',
            'ps': [
                "A Dunai Sétahajózási Kft.-t 2021-ben alapították azzal a céllal, hogy a 19. századi magyar gőzhajózás aranykorát elevenítsék fel a mai utazók számára modern biztonsági háttérrel."
            ]
        }
    },
    3: {  # Card 4: Portum Lines
        'The Ship': {
            'h4': 'A Hajó és Kialakítás',
            'lis': [
                ("Modern, gondozott kétszintes hajó:", "A hajó tágas és kiválóan karbantartott, letisztult bútorzattal és modern hajótesttel rendelkezik.")
            ]
        },
        'The Top Deck': {
            'h4': 'Felső Nyitott Fedélzet',
            'lis': [
                ("Három részre osztott felső terasz:", "A felső fedélzet orr-, középső és tatrészre tagolódik, kényelmes ülőhelyekkel felszerelve."),
                ("Ideális fotós pozíciók:", "Az orr- és a tatrész teljesen nyitott, így akadálytalan 360 fokos panorámát nyújt a kivilágított hidakra."),
                ("Középső fedett lounge:", "A középső fedélzeti szakaszon asztalok és székek találhatók kellemes árnyékolással."),
                ("Kiváló rálátás a Parlamentre:", "A hajó mindkét oldaláról remek szögből fényképezhető a Gellért-hegy és az Országház.")
            ]
        },
        'The Lower Deck': {
            'h4': 'Alsó Zárt Szalon',
            'lis': [
                ("Kényelmes, fűtött és klimatizált belső tér:", "Az alsó szint tágas és modern bútorzatú, hideg vagy esős időben is kényelmes utazást biztosít."),
                ("Széles panorámaablakok:", "A nagy üvegfelületek rossz idő esetén is élvezhető kilátást garantálnak."),
                ("Hangulatos fedélzeti bár:", "A bárpultnál kedvező áron rendelhetők további minőségi italok és kávék.")
            ]
        },
        'The Drinks': {
            'h4': 'Üdvözlőital',
            'lis': [
                ("Ajándék üdvözlőital a jegyárban:", "Beszálláskor pezsgő, minőségi magyar bor, sör vagy üdítőital választható díjtalanul.")
            ]
        },
        'Sightseeing & Views': {
            'h4': 'Városnézés és Kilátás',
            'lis': [
                ("Központi dunai útvonal:", "A hajó a Szent Gellért térről indul, végighalad a belvároson a Margitszigetig, érintve az összes kivilágított hidat."),
                ("Tökéletes esti látvány:", "A folyó közepéről a Budai Vár és a Parlament kivilágítása rendkívül látványos képet nyújt.")
            ]
        },
        'About Portum Lines': {
            'h4': 'A Portum Lines Hajótársaságról',
            'ps': [
                "A Portum Lines több mint egy évtizede megbízható szereplője a budapesti dunai személyszállításnak. Kiváló ár-érték arányú, modern hajóparkjukkal és barátságos kiszolgálásukkal vívták ki az utazók elismerését."
            ]
        }
    },
    4: {  # Card 5: Silverline Budget
        'The Ship': {
            'h4': 'A Hajó és Általános Állapot',
            'lis': [
                ("Funkcionális és célszerű hajó:", "Nem a legújabb vagy legluxusabb hajó a Dunán, de egyszerű városnézésre tökéletesen megfelel."),
                ("Kétszintes elrendezés:", "Tágas zárt alsó fedélzet büfébárral és nyitott felső kilátóterasz áll rendelkezésre.")
            ]
        },
        'The Top Deck': {
            'h4': 'Felső Nyitott Fedélzet',
            'lis': [
                ("Jó kilátás a városra:", "A felső teraszról remek a rálátás a nevezetességekre, bár a tetőszerkezet oszlopai bizonyos szögekből belógnak a fotókba."),
                ("Egyszerű műanyag ülések:", "A bútorzat egyszerű és funkcionális, nem a legkényelmesebb, de a 75 perces útra megfelelő."),
                ("Csúcsidőben zsúfolt:", "A főszezoni esti órákban a felső fedélzet gyorsan megtelik, ezért érdemes időben beszállni.")
            ]
        },
        'The Main Deck': {
            'h4': 'Főfedélzet és Belső Tér',
            'lis': [
                ("Tágas és fűtött belső szalon:", "A zárt tér hideg időben jó menedéket nyújt, fűtéssel és alapvető büfészolgáltatással.")
            ]
        },
        'The Staff': {
            'h4': 'A Személyzet',
            'lis': [
                ("Barátságos fogadtatás:", "A beszállásnál a személyzet udvariasan és gyorsan kezeli a mobiljegyeket.")
            ]
        },
        'Unneccesary Stop': {
            'h4': 'Közbenső Megálló',
            'lis': [
                ("Rövid kikötés a Batthyány téren:", "Bizonyos járatokon a hajó rövid megállót iktat be a budai oldalon új utasok felvételére, ami kissé megtöri a folyamatos városnézést.")
            ]
        },
        'Sightseeing & Views': {
            'h4': 'Városnézés és Panoráma',
            'lis': [
                ("Klasszikus budapesti panoráma:", "A Duna közepéről megcsodálható a Lánchíd, az Erzsébet híd és a Parlament esti díszkivilágítása.")
            ]
        },
        'About Silverline Cruises Ltd.': {
            'h4': 'A Silverline Cruises-ról',
            'ps': [
                "A Silverline Cruises 2011 óta jelen van a budapesti piacon, fapados jellegű városnéző járatokat, koktélos hajókat és vacsorás programokat üzemeltetve a Petőfi téri 11-es kikötőből."
            ]
        }
    },
    5: {  # Card 6: Silverline Cocktails
        'The Ship': {
            'h4': 'A Hajó és Hangulat',
            'lis': [
                ("Praktikus rendezvényhajó:", "Funkcionális folyami hajó tágas belső szalonnal és panorámás felső kilátóterasszal.")
            ]
        },
        'Staff & Service': {
            'h4': 'Személyzet és Kiszolgálás',
            'lis': [
                ("Gyors és udvarias koktélkiszolgálás:", "A bártenderek készségesek, és a választott koktélokat (pl. Mojito, Piña Colada, Tequila Sunrise) frissen készítik el a bárpultnál.")
            ]
        },
        'Sightseeing & Views': {
            'h4': 'Városnézés és Panoráma',
            'lis': [
                ("Hosszabb déli útvonal:", "A hajó lecsorog egészen a Nemzeti Színházig és a Müpáig, így a Rákóczi híd modern fényei is megcsodálhatók."),
                ("Kiváló naplementés fotók:", "A kora esti indulások idején a Budai Vár felett lebukó nap fénye különösen szép látványt nyújt a felső fedélzetről.")
            ]
        },
        'About Silverline Cruises Ltd.': {
            'h4': 'A Silverline Cruises-ról',
            'ps': [
                "A Silverline Cruises a városnéző járatok mellett fiatalos, kötetlen koktélos és zenei esteket is szervez a Duna belvárosi szakaszán."
            ]
        }
    },
    6: {  # Card 7: Silverline Pizza
        'The Ship': {
            'h4': 'A Hajó és Étkezőhelyek',
            'lis': [
                ("Funkcionális kétszintes hajó:", "A megszokott Silverline hajó fűtött belső étkezőasztalokkal és nyitott felső terasszal.")
            ]
        },
        'The Food and Drinks': {
            'h4': 'Ételek és Italok',
            'lis': [
                ("Frissen sütött személyes pizza:", "Több klasszikus íz közül lehet választani (pl. Sonkás-kukoricás, Szalámis, Négysajtos, Hawaii vagy Magyaros)."),
                ("Korlátlan csapolt sör és üdítő:", "A hajóút teljes ideje alatt korlátlanul fogyasztható csapolt sör és szénsavas üdítő.")
            ]
        },
        'Sightseeing & Views': {
            'h4': 'Városnézés és Kilátás',
            'lis': [
                ("Látványos budapesti háttér:", "A kivilágított folyópart remek díszletet biztosít egy laza, baráti pizzázáshoz a Dunán."),
                ("Felső kilátófedélzet:", "Étkezés után a felső nyitott szintre sétálva kényelmesen lehet fényképezni az elhaladó nevezetességeket."),
                ("Praktikus elrendezés:", "Az alsó fedélzeten kényelmesen lehet enni az asztaloknál, a panorámát pedig a nagy ablakokon keresztül vagy a teraszon lehet élvezni.")
            ]
        },
        'About Silverline Cruises Ltd.': {
            'h4': 'A Silverline Cruises-ról',
            'ps': [
                "A Silverline Cruises laza, megfizethető gasztrohajózásokat kínál Budapest szívében baráti társaságok és fiatal utazók számára."
            ]
        }
    },
    7: {  # Card 8: Hungária Koncert 12-Course Buffet
        'The Ship': {
            'h4': 'A Hajó és Belső Tér',
            'lis': [
                ("Klasszikus, elegáns hajóbelső:", "A hajó belső tere nosztalgikus eleganciát áraszt: díszes csillárok, faburkolat, egyedi szőnyegek és intarziás díszítés jellemzi."),
                ("Két fedélzeti szint:", "A felső szinten zárt panorámaszalon és összesen négy szabadtéri kilátóterasz található."),
                ("Nyitott oldalsó sétányok:", "Az oldalsó nyitott fedélzetekről a városnéző vendégek zavartalanul gyönyörködhetnek a budapesti fényekben."),
                ("Panoráma a hajóvégeken:", "Az orr- és tatrészről tágas kilátás nyílik a folyóra és a partvonalra."),
                ("Tágas alsó étkezőszalon:", "Az alsó fedélzeten található a svédasztalos büfé, a bár és a népzenei együttes fellépőhelye.")
            ]
        },
        'Cruise Duration': {
            'h4': 'A Hajóút Időtartama',
            'lis': [
                ("1,5 vagy 2 órás program:", "Az indulási időponttól függően a program bőséges időt hagy a gazdag vacsora és a folklórműsor kényelmes élvezetére.")
            ]
        },
        'Dance and Music Performance': {
            'h4': 'Élő Folklórműsor és Tánc',
            'lis': [
                ("Hagyományos magyar élőzene:", "A vacsora alatt népi zenekar játszik autentikus dallamokat, majd dinamikus néptáncbemutató emeli az est hangulatát."),
                ("Századfordulós mulatóhangulat:", "A produkció a békebeli budapesti kávéházak és kabarék vidám atmoszféráját hozza el a Dunára.")
            ]
        },
        'About Hungaria Koncert': {
            'h4': 'A Hungária Koncertről',
            'ps': [
                "A Hungária Koncert 1995 óta Budapest egyik legjelentősebb kulturális és idegenforgalmi szervezője, magas színvonalú koncertekkel és dunai rendezvényhajókkal."
            ]
        },
        "What's Included": {
            'h4': 'A Jegy Tartalma és Menü',
            'lis': [
                ("Díjnyertes előadóművészek:", "Elismert népzenészek és táncosok gondoskodnak a színvonalas kulturális élményről."),
                ("12 fogásos gazdag svédasztal:", "Klasszikus magyar ételek korlátlan választéka: tradicionális gulyásleves, töltött káposzta, marhapörkölt, házi rétesek és somlói galuska."),
                ("Kiadós házias ízek:", "Kiváló lehetőség a magyar konyha legfontosabb fogásainak megkóstolására egyetlen este alatt.")
            ]
        }
    },
    8: {  # Card 9: Hungária Koncert Drinks & Violin
        'The Ship': {
            'h4': 'A Hajó és Kialakítás',
            'lis': [
                ("Békebeli elegancia:", "A hajó klasszikus stílusú, nemesfa burkolattal, csillárokkal és hangulatos belső terekkel felszerelt.")
            ]
        },
        'Indoor Area': {
            'h4': 'Belső Szalon',
            'lis': [
                ("Kávéházi hangulat:", "Az alsó fedélzet a századfordulós budapesti mulatók és kávéházak meghitt eleganciáját idézi.")
            ]
        },
        'Outdoor Area': {
            'h4': 'Szabadtéri Fedélzet',
            'lis': [
                ("Nyitott sétálófedélzet:", "Az oldalsó kilátóteraszok szabadon látogathatók a városnéző vendégek számára."),
                ("180 fokos látvány mindkét oldalon:", "A hajó mindkét oldaláról kényelmesen szemlélhető Buda és Pest kivilágított partja.")
            ]
        },
        'The Drinks': {
            'h4': 'Italok és Választék',
            'lis': [
                ("Üdvözlőital a jegyárban:", "Az alapticket egy szabadon választható üdvözlőitalt tartalmaz (bor, kézműves sör vagy üdítő)."),
                ("Prémium italkóstoló opciók:", "Lehetőség van magyar kézműves sörkóstolóra, borkóstolóra vagy koktélcsomagra váltani."),
                ("Kényelmes felső szalon:", "A magasabb kategóriájú jegyet váltók a felső kényelmesebb szalonban foglalhatnak helyet.")
            ]
        },
        'About Hungaria Koncert': {
            'h4': 'A Hungária Koncertről',
            'ps': [
                "A Hungária Koncert évtizedes tapasztalattal szervez komolyzenei, folklór és dunai kulturális programokat Budapest szívében."
            ]
        }
    },
    9: {  # Card 10: Mahart PassNave Ferry
        '5 Stops During the Cruise': {
            'h4': '5 Kikötői Megálló',
            'lis': [
                ("Több megállós menetrend:", "A hajó 5 kikötőt érint az útvonal mentén, többek között a Margitszigetet is, így közlekedési eszközként is használható.")
            ]
        },
        'The Ship': {
            'h4': 'A Hajó és Állapot',
            'lis': [
                ("Idősebb hajóflotta:", "A járatok klasszikus, idősebb vízibuszokkal üzemelnek, amelyek alapvető tömegközlekedési színvonalat biztosítanak.")
            ]
        },
        'The Top Deck': {
            'h4': 'Felső Fedélzet',
            'lis': [
                ("Nyitott terasz tetővel:", "A felső fedélzet nyitott, de a tető és az oldalsó oszlopok miatt a kilátás bizonyos szögekből korlátozott.")
            ]
        },
        'The Bottom Deck': {
            'h4': 'Alsó Utastér',
            'lis': [
                ("Egyszerű üléssorok:", "Az alsó fedélzeten egyszerű ülések találhatók, a motorzaj kissé érezhetőbb, mint a prémium sétahajókon.")
            ]
        }
    }
}


DINNER_SUBPOINTS = {
    0: {  # Card 1: Legenda Candlelit Dinner
        'About Legenda City Cruises': {
            'h4': 'A Legenda City Cruises-ról',
            'ps': [
                "A Legenda City Cruises Budapest legrégebbi és legelismertebb hajózási vállalkozása. Több mint három évtizede garantálják a prémium dunai színvonalat, saját exkluzív úszómólóval a Vigadó téren és kimagasló gasztronómiával."
            ]
        }
    },
    1: {  # Card 2: Silverline No Show Dinner
        'About Silverline Cruises': {
            'h4': 'A Silverline Cruises-ról',
            'ps': [
                "A Silverline Cruises több mint egy évtizede üzemeltet megbízható dunai járatokat. Fő profiljuk a jó ár-érték arányú, modern katamaránokon felszolgált vacsorás hajózás a Petőfi téri 11-es kikötőből."
            ]
        }
    },
    2: {  # Card 3: Silverline Folklore Dinner
        'About Silverline Cruises': {
            'h4': 'A Silverline Cruises-ról',
            'ps': [
                "A Silverline Cruises folklóros vacsorahajója a magyar operett és néptánc hagyományait ötvözi a modern dunai gasztronómiával, színvonalas kulturális élményt nyújtva a kivilágított Parlament előtt."
            ]
        }
    },
    3: {  # Card 4: Silverline Piano Battle
        'About Silverline Cruises': {
            'h4': 'A Silverline Zongorapárbaj Show-ról',
            'ps': [
                "A Silverline zongorapárbajos estje az egyik legnépszerűbb élőzenés vacsoraprogram a Dunán, ahol két virtuóz zongorista és egy énekesnő interaktív show-val szórakoztatja a vendégeket."
            ],
            'lis': [
                ("A Silverline három hasonló 4 fogásos vacsorahajót kínál:", "különböző fedélzeti programokkal."),
                ("Műsor nélküli vacsorahajó:", "(lásd a #2-es kártyát fenti összefoglalónkban)."),
                ("Folklór operett vacsorahajó:", "(lásd a #3-as kártyát)."),
                ("Zongorapárbajos vacsorahajó:", "(a jelenlegi kártyán bemutatott élmény)."),
                ("A lényeges megkülönböztető elemek:", "az ismétlések elkerülése végett az alábbi pontok a zongorás show-ra fókuszálnak."),
                ("Fedélzeti szórakoztatás:", "két tehetséges zongorista szellemes párbaja és népszerű világslágerek énekes kísérettel."),
                ("Panorámás étkezőfedélzet:", "az asztalok a felső szinten találhatók, nagy ablakokkal a budapesti éjszakára."),
                ("Közös szolgáltatások:", "a kikötő (Petőfi tér 11-es móló), a hajótest és az ételminőség megegyezik a Silverline flotta standardjával.")
            ]
        }
    },
    4: {  # Card 5: Hungária Koncert 12-Course Buffet Dinner
        'The Ship': {
            'h4': 'A Hajó és Kialakítás',
            'lis': [
                ("Klasszikus, nosztalgikus hajóbelső:", "A hajó csillárokkal, faburkolattal, intarziás díszítéssel és elegáns szőnyegekkel fogadja a vacsoravendégeket."),
                ("Két szimmetrikus zárt szalon:", "A felső fedélzeten tágas étkezőterek találhatók, összesen négy szabadtéri kilátóterasszal kiegészítve."),
                ("Nyitott kilátófedélzetek:", "A szabadtéri teraszok szabadon látogathatók a vacsora alatt a folyóparti fotózáshoz."),
                ("360 fokos látvány:", "A hajóvégekről akadálytalan kilátás nyílik a kivilágított hidakra és a Budai Várra."),
                ("Alsó rendezvényterem:", "Az alsó szint meleg, hívogató büféteremként működik a svédasztalos étkezéshez.")
            ]
        },
        'Welcome Drink': {
            'h4': 'Üdvözlőital és Büfévacsora',
            'lis': [
                ("Ajándék üdvözlőital:", "Beszálláskor minőségi pezsgő vagy gyümölcslé köszönti a vendégeket."),
                ("Élő népzenei műsor:", "A vacsora alatt prímás és népzenekar játszik hagyományos magyar dallamokat."),
                ("Korlátlan svédasztal:", "Gazdag büfékínálat tradicionális magyar ételekből: gulyásleves, töltött káposzta, marhapörkölt, somlói galuska és rétesvariációk."),
                ("Házias és bőséges ízek:", "Kiadós adagok és autentikus ízek, ideális a magyar gasztronómia felfedezéséhez.")
            ]
        },
        'Dance and Music Performance': {
            'h4': 'Élő Folklórelőadás és Tánc',
            'lis': [
                ("Autentikus magyar néptánc:", "A vacsoravendégek számára rendezett élő táncbemutató lendületes és magával ragadó élményt nyújt."),
                ("Békebeli hangulat:", "A zenei összeállítás a 20. század eleji budapesti kávéházi estek világát idézi meg.")
            ]
        },
        'About Hungaria Koncert': {
            'h4': 'A Hungária Koncertről',
            'ps': [
                "A Hungária Koncert 1995 óta Budapest vezető kulturális és turisztikai szolgáltatója, amely évtizedes tapasztalattal garantálja a magas színvonalú vendéglátást és a felejthetetlen élményeket."
            ]
        }
    },
    5: {  # Card 6: Eurama Folk Dinner
        'About Eurama': {
            'h4': 'Az Euramáról',
            'ps': [
                "Az Eurama több mint 20 éve megbízható idegenforgalmi iroda Budapesten, magas minőségű dunai sétahajózásokat és városnézéseket szervezve a Vigadó téri mólóról."
            ]
        },
        "What's Included": {
            'h4': 'A Menü és Szolgáltatások',
            'lis': [
                ("Frissen tálalt 4 fogásos gourmet vacsora:", "Ízletes, asztalhoz felszolgált vacsora autentikus magyar és nemzetközi fogásokkal, élő cigányzenei kíséret mellett a teljes 2 órás út során.")
            ]
        }
    },
    6: {  # Card 7: Silverline Unlimited Drinks Dinner
        "What's Included & Menu Highlights": {
            'h4': 'Mit Tartalmaz a Menü és Szolgáltatás',
            'lis': [
                ("🥂 Üdvözlő pezsgő & korlátlan italfogyasztás:", "Korlátlan minőségi magyar fehér-, rosé- és vörösborok, pezsgő, csapolt sör és üdítők a teljes 2,5 órás út alatt."),
                ("🍽️ 4 fogásos prémium vacsora:", "Friss előételek, hagyományos levesek, választható ínyenc főételek (lassan sült húsok, halak, vegetáriánus opciók) és desszertkülönlegességek."),
                ("🎶 Élő akusztikus zene:", "Hangulatos élőzenei előadás a panorámás szalonban, romantikus aláfestést nyújtva a kivilágított Duna-parti látványhoz.")
            ]
        }
    }
}


QF_LABELS_HU = {
    'Ticket Format': 'Jegyformátum',
    'Inclusions & Drinks': 'Italok & Csomag Tartalma',
    'Inclusions & Dining': 'Gasztronómia & Csomag Tartalma',
    'Meeting Point & Pier': 'Indulási Kikötő & Cím',
    'Vessel Architecture': 'Hajótípus & Kialakítás',
    'Child & Family Discounts': 'Gyermek- & Családi Kedvezmények',
    'Schedule & Frequency': 'Menetrend & Gyakoriság',
    'Cancellation Policy': 'Lemondási Feltételek',
    'Audio Commentary': 'Audioguide & Nyelvek',
    'Special Feature': 'Különleges Jellemző',
    'Duration': 'Időtartam',
    'Entertainment': 'Élőzene & Szórakoztatás',
    'Dining Format': 'Étkezési Forma',
    'Dining & Show': 'Vacsora & Műsor',
    'Dining & Drinks': 'Vacsora & Italok',
}

QF_CHIPS_HU = {
    '✓ Onboard Restrooms': '✓ Fedélzeti Mosdók',
    '✓ Open-Air Top Deck': '✓ Nyitott Panorámafedélzet',
    '✓ Pets Allowed': '✓ Háziállat Hozható',
    '✕ Not Wheelchair Accessible': '✕ Kerekesszékkel Nem Megközelíthető',
    '✕ No Pets (Service Only)': '✕ Háziállat Nem Hozható (kivéve segítőkutya)',
    '✓ Stroller Accessible': '✓ Babakocsival Megközelíthető',
    '✓ Dedicated Smoking Area': '✓ Kijelölt Dohányzóhely',
    '✕ No AC/Heating (Authentic Steamer)': '✕ Nincs Klíma/Fűtés (Autentikus Gőzös)',
    '✓ Wheelchair Accessible': '✓ Kerekesszékkel Megközelíthető',
    '✕ No Onboard Wi-Fi': '✕ Nincs Fedélzeti Wi-Fi',
    '✓ Heated & AC Cabin': '✓ Fűtött & Klímás Szalon',
    '✕ No Strollers': '✕ Babakocsival Nem Megközelíthető',
    '✓ Free Onboard Wi-Fi': '✓ Ingyenes Fedélzeti Wi-Fi',
}

QF_BADGES_HU = {
    'Dock 7 (Vigadó tér)': '7-es kikötő (Vigadó tér)',
    'Margaret Bridge Dock': 'Margit híd kikötő',
    'Dock 10 (Erzsébet Bridge)': '10-es kikötő (Erzsébet híd)',
    'Dock 42 (Szent István Park)': '42-es kikötő (Szent István park)',
    'Dock 11 (Elizabeth Bridge)': '11-es kikötő (Petőfi tér / Erzsébet híd)',
    'Dock 3 (Akadémia)': '3-as kikötő (Akadémia)',
    'Vigadó tér Dock 5': '5-ös kikötő (Vigadó tér)',
    'Dock 7': '7-es kikötő (Vigadó tér)',
    'Dock 11': '11-es kikötő (Petőfi tér)',
    'Dock 3 (Gróf Széchényi)': '3-as kikötő (Gróf Széchenyi)',
    'Dock 6 (Jane Haining rkp.)': '6-os kikötő (Jane Haining rkp.)',
    'Dock 8A': '8A kikötő',
}

QF_VALS_HU = {
    'Daily from 10:00 AM to 10:00 PM (hourly departures)': 'Naponta 10:00 és 22:00 között (óránkénti indulások)',
    'Every day at 19:00 and 21:00 (sunset & night sailings)': 'Minden nap 19:00 és 21:00 órakor (naplementés és esti járatok)',
    'Tuesday–Saturday at 12:00, 14:00, 16:00, 18:00, and 20:00 (Closed Mondays)': 'Kedd–Szombat 12:00, 14:00, 16:00, 18:00 és 20:00 (Hétfőn zárva)',
    'Daily at 16:30, 17:30, 19:00, 20:30, and 22:00': 'Naponta 16:30, 17:30, 19:00, 20:30 és 22:00 órakor',
    'Daily continuous departures from 11:00 AM to 10:00 PM': 'Naponta folyamatos indulások 11:00 és 22:00 között',
    'Daily from 17:00 to 22:00 (hourly evening departures)': 'Naponta 17:00 és 22:00 között (óránkénti esti indulások)',
    'Daily sunset departures at 17:00, 19:00, and 21:00': 'Naponta naplementés járatok 17:00, 19:00 és 21:00 órakor',
    'Daily at 19:00, weekends at 22:00': 'Naponta 19:00 órakor, hétvégén 22:00 órakor is',
    'Daily at 19:00 (Boarding at 18:30)': 'Naponta 19:00 órakor (Beszállás: 18:30)',
    'Daily at 19:00 (Boarding begins at 18:30)': 'Naponta 19:00 órakor (Beszállás kezdete: 18:30)',
    'Daily at 19:30 (Boarding at 19:00)': 'Naponta 19:30 órakor (Beszállás: 19:00)',
    'Daily at 20:00 (Boarding at 19:30)': 'Naponta 20:00 órakor (Beszállás: 19:30)',
    'Evening boarding at 19:00 (2.5-hour duration)': 'Esti beszállás 19:00 órakor (2,5 órás időtartam)',
    '60 Minutes': '60 perc',
    '60–70 Minutes': '60–70 perc',
    '60–80 Minutes': '60–80 perc',
    '75 Minutes': '75 perc',
    '75–85 Minutes': '75–85 perc',
    '90 Minutes': '90 perc',
    '90–120 Minutes': '90–120 perc',
    '1.5 Hours (90 Minutes)': '1,5 óra (90 perc)',
    '2.5 Hours': '2,5 óra',
    '2.5 Hours (150 Minutes)': '2,5 óra (150 perc)',
    '1 Complimentary welcome drink (champagne, wine, beer, or soda) + summer lemonade': '1 ingyenes üdvözlőital (pezsgő, bor, sör vagy üdítő) + nyári limonádé',
    'Unlimited Prosecco, Aperol Spritz, draft beer, spritzer & homemade lemonade': 'Korlátlan Prosecco, Aperol Spritz, csapolt sör, fröccs és házi limonádé',
    '1 Complimentary welcome drink (sparkling wine, Hungarian wine, or soda)': '1 ingyenes üdvözlőital (pezsgő, magyar bor vagy üdítő)',
    '1 Complimentary beverage included (Hungarian wine, beer, or soft drink)': '1 ingyenes ital a jegyárban (magyar bor, sör vagy üdítő)',
    'No-frills ticket (full cash/card bar available onboard for drinks & snacks)': 'Sallangmentes alapticket (a fedélzeti bárban vásárolhatók italok és snackek)',
    '2 Large freshly mixed full-size cocktails included (Mojito, Piña Colada, Cuba Libre, etc.)': '2 nagy méretű, frissen kevert prémium koktél a jegyárban (Mojito, Piña Colada stb.)',
    'Individual hot personal pizza + 60 minutes unlimited draft beer & soft drinks': 'Frissen sült személyes meleg pizza + 60 perc korlátlan csapolt sör és üdítő',
    '12-Course Hungarian warm buffet + 2 drinks + live folklore operetta & dance performance': '12 fogásos meleg magyar svédasztal + 2 ital + élő operett és néptáncműsor',
    'Live Hungarian folk string trio + choice of wine tasting, craft beers, or cocktails': 'Élő magyar vonós trió + választható borkóstoló, kézműves sör vagy koktél',
    '1 Welcome drink included (Prosecco, cocktail, or soft drink)': '1 üdvözlőital a jegyárban (Prosecco, koktél vagy üdítő)',
    'Welcome glass of sparkling wine + mineral water + live salon violin/acoustic music': 'Egy pohár üdvözlő pezsgő + ásványvíz + élő szalonzene (hegedű/akusztikus gitár)',
    '1 Welcome drink + 4-course served menu': '1 üdvözlőital + 4 fogásos felszolgált gourmet menü',
    '1 Welcome drink + complete 4-course served meal': '1 üdvözlőital + teljes 4 fogásos asztalhoz felszolgált vacsora',
    '4-Course fine dining + authentic Hungarian folklore dance troupe and operetta singers': '4 fogásos ínyenc vacsora + autentikus magyar néptáncegyüttes és operetténekesek',
    '4-Course dinner + live dual grand piano battle show with guest vocalist': '4 fogásos vacsora + élő kétzongorás párbajshow és vendégénekesnő',
    '12-Course Hungarian warm buffet + authentic folk music and live dance performance': '12 fogásos meleg magyar svédasztalos vacsora + autentikus népzene és élő táncelőadás',
    '4-Course Hungarian feast + live traditional gypsy operetta musical performance': '4 fogásos magyaros díszvacsora + élő tradicionális cigányzene és operett',
    '4-Course gourmet served dinner + unlimited draft beer, wine, champagne & soft drinks': '4 fogásos ínyenc vacsora + korlátlan csapolt sör, bor, pezsgő és üdítőfogyasztás',
    '4-Course gourmet à la carte fine dining (starter, soup, main, dessert)': '4 fogásos prémium gourmet vacsora (előétel, leves, főétel, desszert)',
    '4-Course served dinner with candlelight table setting (ambient background music, no stage show)': '4 fogásos gyertyafényes vacsora hangulatos háttérzenével (színpadi műsor nélkül)',
    'All-you-can-eat buffet + 2 complimentary drinks (wine, beer, soft drinks)': 'Korlátlan svédasztalos büfé + 2 ajándék ital (bor, sör, üdítő)',
    '1 Welcome glass of champagne or soft drink': '1 pohár üdvözlő pezsgő vagy üdítőital',
    '1 Welcome glass of sparkling wine + 4-course menu': '1 pohár üdvözlő pezsgő + 4 fogásos felszolgált menü',
    '30 Languages with crystal-clear individual headsets': '30 világnyelv kristálytiszta egyéni fülhallgatóval',
    'Digital smartphone audio commentary + upbeat cocktail lounge music': 'Okostelefonos digitális audioguide + kellemes koktélbár zene',
    'Mobile app audio narration available in multiple languages': 'Többnyelvű mobilalkalmazásos audioguide',
    'Live acoustic salon piano and vocal performance': 'Élő akusztikus szalonzongora és énekes előadás',
    'Instant smartphone QR voucher or printed': 'Azonnali okostelefonos QR-utalvány vagy nyomtatott jegy',
    'Instant smartphone QR ticket or printed': 'Azonnali okostelefonos QR-jegy vagy nyomtatott jegy',
    'Full refund up to 24 hours before departure': 'Teljes visszatérítés az indulás előtt legkésőbb 24 órával történő lemondás esetén',
    'Free for children (age 0–9), ~50% discount for teens (age 10–14)': '0–9 éves korig ingyenes, 10–14 éves korig ~50% kedvezmény',
    'Free for infants (age 0–2)': '2 éves kor alatt ingyenes',
    'Free for infants (age 0–2) on Viator': '2 éves kor alatt ingyenes',
    'Free for infants (age 0–3)': '3 éves kor alatt ingyenes',
    'Free for children (age 0–3)': '3 éves kor alatt ingyenes',
    'Free for children (age 0–5)': '5 éves kor alatt ingyenes',
    'Free for children (age 0–6)': '6 éves kor alatt ingyenes',
    'Free for children (age 0–7)': '7 éves kor alatt ingyenes',
    'Authentic 1847 paddle steamer with lower-deck salon maritime museum': 'Autentikus 1847-es lapátkerekes gőzös alsó fedélzeti hajózástörténeti múzeummal',
    'Hop-on hop-off day pass with 5 circular river stops': 'Hop-on hop-off napijegy 5 belvárosi dunai kikötői megállóval',
    'Vintage turn-of-the-century Gróf Széchenyi paddle steamer with chandeliers & teak woodwork': 'Békebeli századfordulós Gróf Széchenyi gőzhajó csillárokkal és nemesfa burkolattal',
    'Dock 7 (Vigadó tér), 1051 Budapest': '7-es kikötő (Vigadó tér), 1051 Budapest',
    'Jane Haining rakpart 10, Dock 10, 1052 Budapest': 'Jane Haining rakpart 10, 10-es kikötő, 1052 Budapest',
    'Dock 42 port, Szent István park, 1138 Budapest': '42-es kikötő, Szent István park, 1138 Budapest',
    'Jane Haining rakpart, Dock 11, 1052 Budapest': 'Jane Haining rakpart, 11-es kikötő, 1052 Budapest',
    'Dock 11, Jane Haining rakpart / Szent István park 5, 1137 Budapest': '11-es kikötő (Jane Haining rkp.) / Szent István park 5, Budapest',
    'Id. Antall József rkp., 1051 Budapest (near Széchenyi Chain Bridge)': 'Id. Antall József rkp., 1051 Budapest (a Lánchíd közelében)',
    'Vigadó tér (Pest) or Batthyány tér (Buda), 1051 Budapest': 'Vigadó tér (Pest) vagy Batthyány tér (Buda)',
    'Dock 7, Vigadó tér, 1051 Budapest': '7-es kikötő, Vigadó tér, 1051 Budapest',
    'Jane Haining Rakpart, Dock 11, 1052 Budapest': 'Jane Haining rakpart, 11-es kikötő, 1052 Budapest',
    'Jane Haining rakpart, Dock 6, 1051 Budapest': 'Jane Haining rakpart, 6-os kikötő, 1051 Budapest',
    'Jane Haining rakpart, Dock 8A / Dock 11, 1052 Budapest': 'Jane Haining rakpart, 8A vagy 11-es kikötő, 1052 Budapest',
}
