# -*- coding: utf-8 -*-
"""Magyar adatok és szöveg: /hu/legjobb-hostelek-budapesten. Tények: lásd hostels_data_en.py (2026. 11. 14.)."""
from hostels_data_en import CHECKED_ISO

CHECKED = "2026. november 14."
HU = "https://www.budapestadventures.com/hu/legjobb-hostelek-budapesten"

HOSTELS = [
  {
    "n": 1, "id": "section-1-maverick-urban-lodge", "name": "Maverick Central Market", "brand": "Maverick Hostels",
    "tag": "🏆 #1 legjobb hostel összességében", "short": "Összességében a legjobb",
    "area": "IX. kerület, Központi Vásárcsarnok", "area_q": "Lonyay+utca+31+Budapest", "district": "IX",
    "address": "1093 Budapest, Lónyay utca 31.", "street": "Lónyay utca 31.", "zip": "1093",
    "hw": (9.2, 3037), "bk": (8.9, 5031), "dorm": 10, "private": 28,
    "checkin": "Bejelentkezés 15:00-tól, kijelentkezés 11:00-ig", "rules": "Nincs takarodó",
    "cats": "tested quiet nomad kitchen budget",
    "specs": ["Ágyfüggöny", "Tetőterasz", "Csendes mellékutca", "Hosszú távra is jó ár"],
    "best_for": "Egyedül utazóknak, digitális nomádoknak és hosszabb ideig maradó hátizsákosoknak, akik társasági hostelt szeretnének bulizaj nélkül.",
    "skip_if": "bulihostelt keres a romkocsmák mellett.",
    "trust": "Privát szoba 28 €-tól",
    "transit": "Kálvin tér (M3, M4) és Fővám tér (M4, 2-es, 47-es, 49-es villamos), mindkettő pár perc séta",
    "watch": "Csúcsidőben zsúfolt konyha; zárja el az értékeit", "noise": "Csendes",
    "pros": [
      ("Megfizethető", "Szezonon kívül már 9 €-tól kaptam ágyat éjszakánként. Márciusban 30 éjszakáért 280 €-t fizettem."),
      ("Hosszabb tartózkodásra is remek", "Olyan, mintha a saját kollégiumi szobájában lakna, egy hónapra is kényelmes."),
      ("Kiváló elhelyezkedés", "A csendesebb IX. kerületben van, mégis elég központi az éjszakai élethez és a tömegközlekedéshez."),
      ("Remek szobák", "Modern kollégiumi elrendezés nagy szekrényekkel és ágyfüggönnyel."),
      ("Remek fürdőszobák", "A közös (vagy privát) fürdőszobák jól karbantartottak, tiszták és igényesek."),
      ("Alacsony zajszint", "Az utcazaj minimális, mert a hostel egy kisebb utcában van."),
    ],
    "cons": [
      ("Konyha", "Csúcsidőben szűkös, és a konyhai eszközök cserére szorulnak. Gyorsan koszos lesz, bár naponta takarítják. A hűtő állandóan tele volt és rendezetlen."),
      ("Lopás", "Elloptak tőlem egy pulóvert és egy doboz orrtapaszt. Ez bármelyik hostelben megtörténhet, nem csak a Maverickben. <strong>Az értékeit mindig zárja el</strong>."),
    ],
    "summary": [
      "<strong>A Maverick Central Market a kényelmet keresőknek való, rövid és hosszabb tartózkodásra egyaránt.</strong> Olyan, mintha a saját kollégiumi szobájában lakna, egy hónapra is kényelmes.",
      "Nem <a href=\"#section-2-hostel-one\">bulihostel</a>, de <strong>bőven van alkalom társaságra</strong> és ismerkedésre.",
      "<strong>Kiemelkedő ár-érték arány</strong>: <strong>márciusban 30 éjszakát töltöttem itt 280 €-ért</strong> (kb. 9,33 € éjszakánként). 2026. november 14-i ellenőrzésemkor a közeli dátumokra <strong>kb. 10 €-tól</strong> volt ágy, és főszezonban is korrekt az ár ehhez a minőséghez.",
    ],
    "video": ("https://youtu.be/hJB53XdmJSY", "videós értékelésemet a Maverick Central Marketről"),
    "groups": [
      ("Szobák, ágyak és alvásminőség", "szobák és ágyak", [
        ("Függönyös kollégiumi ágyak", "<p>A kollégiumi szobák <strong>modern elrendezésűek, ágyfüggönnyel és nagy szekrényekkel</strong>, így egy teli szoba is nyugodt.</p>"),
        ("Csendes éjszakák", "<p>Egy <strong>kisebb mellékutcában van a IX. kerületben</strong>, távol a VII. kerület bulis utcáitól. A 30 éjszakám alatt az utcazaj minimális volt.</p>"),
        ("Valódi hosszú távú ár", "<p><strong>Márciusban 30 éjszaka 280 €-ba került.</strong> Digitális nomád bázisnak vagy lassú utazáshoz nem találtam jobb árat a belvárosban.</p>"),
      ]),
      ("Hangulat és társasági élet", "közösségi terek", [
        ("Társasági, de nem bulihostel", "<p>Olyan, mint egy barátságos egyetemi kollégium. <strong>Könnyű ismerkedni</strong> a közösségi terekben, hajnali négykor kiabálás nélkül.</p>"),
        ("Kikkel találkozik", "<p>Egyedül utazókkal, hosszabb ideig maradókkal és távmunkásokkal. Tökéletes, ha este társaságra, utána pedig jó alvásra vágyik.</p>"),
      ]),
      ("Felszereltség, konyha és fürdőszobák", "felszereltség", [
        ("Fürdőszobák", "<p>A közös és privát fürdőszobák <strong>tiszták és igényesek</strong> voltak, a tartózkodásom egyik legjobb része.</p>"),
        ("A konyha valósága", "<p>A vendégkonyha <strong>csúcsidőben szűkös</strong>, az eszközök elhasználtak, a hűtő mindig tele van. Címkézze fel az ételeit.</p>"),
        ("Zárja el a holmiját", "<p>Elloptak tőlem egy pulóvert és egy doboz orrtapaszt. <strong>Használja a szekrényeket</strong> mindenhez, ami hiányozna.</p>"),
      ]),
    ],
    "chips": [("yes", "Ágyfüggöny"), ("yes", "Tetőterasz"), ("yes", "Vendégkonyha"), ("yes", "24 órás recepció"), ("yes", "Ingyenes csomagmegőrzés")],
    "tested": True,
  },
  {
    "n": 2, "id": "section-2-hostel-one", "name": "Onefam Budapest", "brand": "Onefam",
    "tag": "#2 legjobb társasági hostel egyedül utazóknak", "short": "Egyedül utazóknak a legjobb",
    "area": "VII. kerület, zsidónegyed", "area_q": "Rumbach+Sebestyen+utca+6+Budapest", "district": "VII",
    "address": "1075 Budapest, Rumbach Sebestyén utca 6.", "street": "Rumbach Sebestyén utca 6.", "zip": "1075",
    "hw": (9.7, 6588), "bk": (9.4, 1048), "dorm": 14, "private": None,
    "checkin": "Bejelentkezés 15:00 és 23:00 között, kijelentkezés 11:00-ig", "rules": "Csak 18 és 39 év között, nincs takarodó",
    "cats": "tested party",
    "specs": ["Ingyenes napi programok", "Kocsmatúrák", "18 és 39 év között", "Deák tér"],
    "best_for": "18 és 39 év közötti egyedül utazóknak, akik azonnali társaságot, napi programokat és esti bulikat szeretnének.",
    "skip_if": "elmúlt 39, párként privát szférára vágyik, vagy korán szeretne lefeküdni.",
    "trust": "18 és 39 év között",
    "transit": "Deák Ferenc tér (M1, M2, M3 és a 100E reptéri busz), kb. 4 perc séta",
    "watch": "Drágább a legtöbbnél; csak 18 és 39 év között", "noise": "Éjfélig pörgős",
    "pros": [
      ("Legjobb bulihostel", "Remekül fog szórakozni az ivós játékokkal a bárban, utána a romkocsmákban, napközben pedig városnézéssel."),
      ("Szervezett programok", "Az Onefam nappali és esti programokat is szervez (kocsmatúrák, ivós játékok)."),
      ("Tökéletes elhelyezkedés", "A zsidónegyed közepén, közel a 100E reptéri busz megállójához, a látnivalókhoz és az éjszakai élethez."),
      ("Remek szobák", "Tágas szobák biztonságos tárolóval és szekrényekkel. Az ágyak privát szférát és kényelmet adnak."),
      ("Alacsony zajszint", "A zajszint elfogadható, a buli általában 23 óra és éjfél körül csendesedik el."),
    ],
    "cons": [
      ("Nincs tárolóhely az ágy mellett", "Az emeletes ágyakon nincs hely fülhallgatónak, pénztárcának és telefonnak."),
      ("Zuhanyproblémák", "A víz hőmérséklete ingadozhat, és egy rosszul elhelyezett mozgásérzékelő miatt kialszik a lámpa a zuhanyzóban."),
      ("Ár", "Drágább a többi budapesti hostelnél. A társasági élet és a bulizás miatt megéri a felárat."),
    ],
    "summary": [
      "<strong>Az Onefam Budapest a legjobb választás, ha szeret társaságban lenni, barátkozni és bulizni.</strong>",
      "Drágább a legtöbb budapesti hostelnél, de megéri az árát, ha nyitott, társasági tartózkodásra vágyik. Figyeljen a <strong>18 és 39 év közötti korhatárra</strong>.",
    ],
    "video": ("https://youtu.be/e8HHIXO8d_8", "videós értékelésemet az Onefam Budapestről"),
    "groups": [
      ("Szobák, ágyak és alvásminőség", "szobák és ágyak", [
        ("Tágas szobák, biztonságos tároló", "<p>A szobák <strong>tágasak, biztonságos tárolóval és szekrényekkel</strong>, az ágyak pedig privát szférát és kényelmet adnak.</p>"),
        ("Nincs polc az ágy mellett", "<p>Az ágyon <strong>nincs hova tenni a telefont, a fülhallgatót vagy a pénztárcát</strong>. Hozzon egy kis tasakot.</p>"),
        ("Mikor lesz csend", "<p>A buli általában <strong>23 óra és éjfél körül csendesedik el</strong>, utána a társaság átvonul a romkocsmákba.</p>"),
      ]),
      ("Hangulat és társasági élet", "közösségi terek", [
        ("Azonnali társaság", "<p>Ha egyedül érkezik, és gyorsan akar barátokat, <strong>ez a hely</strong>. A személyzet mindenkit bevon.</p>"),
        ("Nappali és esti programok", "<p>Ingyenes nappali programok, este pedig ivós játékok és <strong>kocsmatúrák</strong> a zsidónegyedben.</p>"),
      ]),
      ("Felszereltség, fürdőszobák és elhelyezkedés", "felszereltség", [
        ("Zuhany furcsaságai", "<p>A víz hőmérséklete ingadozhat, és <strong>egy mozgásérzékelő zuhanyzás közben lekapcsolja a villanyt</strong>.</p>"),
        ("Bázis a zsidónegyedben", "<p>Pár percre a <strong>Deák Ferenc tértől és a 100E reptéri busztól</strong>, a bárokból gyalog hazaér.</p>"),
      ]),
    ],
    "chips": [("yes", "Ingyenes napi programok"), ("yes", "Hostelbár"), ("yes", "Éjjel-nappal használható konyha"), ("yes", "Ingyenes széf szekrények"), ("no", "Csak 18 és 39 év között")],
    "tested": True,
  },
  {
    "n": 3, "id": "section-3-avenue-hostel", "name": "Avenue Hostel", "brand": "Avenue Hostel",
    "tag": "#3 legjobb olcsó hostel", "short": "A legolcsóbb ágy",
    "area": "VI. kerület, Oktogon", "area_q": "Oktogon+ter+4+Budapest", "district": "VI",
    "address": "1061 Budapest, Oktogon tér 4.", "street": "Oktogon tér 4.", "zip": "1061",
    "hw": (8.9, 9485), "bk": (8.6, 15668), "dorm": 8, "private": None,
    "checkin": "Bejelentkezés 14:00 és éjfél között, kijelentkezés 11:00-ig", "rules": "6 és 49 év között, nincs takarodó",
    "cats": "tested budget",
    "specs": ["Ingyenes reggeli", "Ágyfüggöny", "Éjjel-nappal villamos", "Oktogon"],
    "best_for": "Takarékos utazóknak, akik a legolcsóbb belvárosi ágyat, ingyenes reggelit és olcsó vacsorát keresnek.",
    "skip_if": "éber alvó, vagy társasági, személyes hangulatra vágyik.",
    "trust": "Ingyenes reggeli",
    "transit": "Oktogon (M1 és a 24 órás 4-es, 6-os villamos) a ház előtt",
    "watch": "Zajos villamoscsomópont; hozzon füldugót", "noise": "Zajos (villamoscsomópont)",
    "pros": [
      ("Legjobb ár-érték", "Szezonon kívül már 8 €-tól volt ágy éjszakánként, ingyenes reggelivel és kedvezményes vacsorával."),
      ("Pénzt spórol", "Magyarországon drága az étel, így az ingyenes és kedvezményes étkezésekkel sokat spórol."),
      ("Személyzet", "Segítőkész, gyors, és éjjel-nappal elérhető."),
    ],
    "cons": [
      ("Életminőség", "A 10 ágyas szoba, ahol aludtam, kényelemben, privát szférában és tisztaságban is közepes volt."),
      ("Nincs ingyen lakat", "A szekrényekhez nem jár lakat, de kb. 3 €-ért vehet egyet."),
      ("Személytelen", "Nincs társasági hangulat, személyes törődés vagy program, kivéve az étkezőben."),
      ("Zajos", "Egy nagy kereszteződés mellett van, ahol villamosok járnak. Hozzon füldugót."),
    ],
    "summary": [
      "<strong>Az Avenue Hostel a takarékos utazók első választása, ha a szálláson és az étkezésen is spórolna Budapesten.</strong>",
      "Az ágyak <strong>kb. 8 €-tól</strong> indulnak, <strong>ingyenes reggelivel</strong> és kedvezményes vacsorával (ottjártamkor kis minimális bárfogyasztással). A magas magyar élelmiszerárak mellett ez sokat számít.",
      "Nem luxus, de praktikus és olcsó, jó választás a pénztárcájára figyelő utazóknak.",
      "📝 <strong>Szerkesztői megjegyzés:</strong> a 10 ágyas \"függönyös\" szoba, ahol aludtam, és a hozzá tartozó közös fürdők nem voltak jók. A hostel többi, 4, 8 és 12 ágyas szobája szebb, csak drágább, így a hostel jobb értékelést érdemel, mint amit a szobám alapján adnék.",
    ],
    "video": ("https://youtu.be/JXyzhhnOo9I", "videós értékelésemet az Avenue Hostelről"),
    "groups": [
      ("Szobák, ágyak és alvásminőség", "szobák és ágyak", [
        ("Válasszon jobb szobát", "<p>A 10 ágyas szobám volt a gyenge pont. <strong>A 4, 8 és 12 ágyas szobák szebbek</strong>, és megérik azt a pár eurót.</p>"),
        ("A füldugó kötelező", "<p>Az <strong>Oktogon csomópontján van, egész éjjel járó villamosokkal</strong>. Éber alvóknak inkább a Maverick vagy a Zen.</p>"),
        ("Lakat a szekrényhez", "<p>Lakat nem jár. <strong>Hozzon egyet</strong>, vagy vegyen a recepción kb. 3 €-ért.</p>"),
      ]),
      ("Hangulat és társasági élet", "közösségi terek", [
        ("Praktikus, nem személyes", "<p>Ne várjon programokat vagy névre szóló vendéglátást. <strong>Az étkezőben ismerkednek az emberek.</strong></p>"),
        ("Kinek való", "<p>Diákoknak és hosszú úton lévő hátizsákosoknak, akik minden eurót megnéznek, és a hostelt főleg alvásra és evésre használják.</p>"),
      ]),
      ("Étkezés, felszereltség és elhelyezkedés", "felszereltség", [
        ("Ingyen reggeli, olcsó vacsora", "<p>Az <strong>ingyenes reggeli</strong> és a kedvezményes vacsora a fő vonzerő. Naponta többet spórol vele, mint amennyibe az ágy kerül.</p>"),
        ("Éjjel-nappal személyzet és közlekedés", "<p>A recepció éjjel-nappal nyitva, az <strong>M1 és a 24 órás 4-es, 6-os villamos</strong> a kapuban áll meg.</p>"),
      ]),
    ],
    "chips": [("yes", "Ingyenes reggeli"), ("yes", "Ágyfüggöny"), ("yes", "24 órás recepció"), ("yes", "Vendégkonyha"), ("no", "Lakatot hozzon")],
    "tested": True,
  },
  {
    "n": 4, "id": "section-4-flow-spaces", "name": "Flow Spaces", "brand": "Flow Spaces",
    "tag": "#4 legjobb digitális nomádoknak", "short": "Digitális nomádoknak a legjobb",
    "area": "IX. kerület, Központi Vásárcsarnok", "area_q": "Gonczy+Pal+utca+2+Budapest", "district": "IX",
    "address": "1093 Budapest, Gönczy Pál utca 2.", "street": "Gönczy Pál utca 2.", "zip": "1093",
    "hw": (8.9, 4563), "bk": (8.3, 6820), "dorm": 10, "private": None,
    "checkin": "Bejelentkezés 15:00 és éjfél között, kijelentkezés 11:00-ig", "rules": "Nincs takarodó",
    "cats": "tested budget nomad kitchen",
    "specs": ["Coworking tér", "Ingyen lakat", "Kapszulaágyak", "Vásárcsarnok"],
    "best_for": "Digitális nomádoknak és utazóknak, akik laptopbarát társalgót, kapszulaágyat és társasági, mégis nyugodt hangulatot keresnek.",
    "skip_if": "nehéz a csomagja (3. emelet, nincs lift), vagy saját fürdőszobát szeretne.",
    "trust": "Coworking tér",
    "transit": "Fővám tér (M4, 2-es, 47-es, 49-es villamos) és Kálvin tér (M3, M4)",
    "watch": "Koedukált közös fürdők; 3. emelet, nincs lift", "noise": "Nyugodt",
    "pros": [
      ("Személyzet", "A recepció éjjel-nappal elérhető, a személyzet barátságos és segítőkész."),
      ("Barátságos", "Társasági hangulat, könnyű más utazókkal megismerkedni."),
      ("Remek ágyak", "Függöny, konnektor, lámpa, kis polc és tárolódoboz az ágynál."),
      ("Biztonságos tároló", "Ingyen lakat jár hozzá."),
      ("Munkasarok", "Társalgó laptopbarát munkasarokkal."),
    ],
    "cons": [
      ("Fürdőszobák", "A fürdők koedukáltak és közösek, kevés privát szférával."),
      ("Nincs lift", "A hostel a 3. emeleten van."),
      ("Higiénia", "A lepedőmön hajszálak voltak, pedig ki volt mosva. Összességében higiénikus a hostel."),
      ("Tele hűtők", "Elveszett némi étel, amit vettem."),
      ("Szűk szobák", "Alig volt hely mozogni."),
    ],
    "summary": [
      "<strong>A Flow Spaces a hostel társasági életét ötvözi egy hotel nyugalmával</strong>, ideális, ha az arany középutat keresi.",
      "A hangulat egy kollégiumra emlékeztet, jó választás kiegyensúlyozott élményre vágyó, takarékos utazóknak. Az ágyak <strong>kb. 10 €-tól</strong> indulnak.",
      "Barátságos hangulatával, <strong>csendes munkaterével</strong> és jól felszerelt konyhájával érdemes megfontolni.",
    ],
    "groups": [
      ("Szobák, ágyak és alvásminőség", "szobák és ágyak", [
        ("Jól felszerelt kapszulák", "<p>Minden ágynál van <strong>függöny, konnektor, lámpa, kis polc és tárolódoboz</strong>, ingyen lakattal.</p>"),
        ("Szűk szobák", "<p>A szobák <strong>szűkek</strong>, alig lehet mozogni, amikor mindenki pakol.</p>"),
      ]),
      ("Hangulat és munkatér", "közösségi terek", [
        ("Laptopbarát társalgó", "<p>A társalgóban <strong>rendes munkasarok</strong> van, a hostel coworking teret is kínál, itt a legjobb a távmunka.</p>"),
        ("Társasági, de kiegyensúlyozott", "<p>Könnyű ismerkedni, bulihostel-éjszakák nélkül. Inkább kollégium, mint kocsmatúra-központ.</p>"),
      ]),
      ("Felszereltség, fürdőszobák és elhelyezkedés", "felszereltség", [
        ("Fürdők és lépcső", "<p>A fürdők <strong>koedukáltak és közösek</strong>, a hostel pedig a <strong>3. emeleten van, lift nélkül</strong>.</p>"),
        ("Konyha és hűtők", "<p>A konyha jól felszerelt, de a hűtők megtelnek, és <strong>elveszett némi ételem</strong>. Címkézzen fel mindent.</p>"),
        ("A Vásárcsarnok mellett", "<p>A <strong>Központi Vásárcsarnok egy háznyira van</strong>, a Duna pedig pár perc séta.</p>"),
      ]),
    ],
    "chips": [("yes", "Coworking tér"), ("yes", "Ingyen lakat"), ("yes", "Ágyfüggöny"), ("yes", "24 órás recepció"), ("no", "Nincs lift (3. emelet)")],
    "tested": True,
  },
  {
    "n": 5, "id": "section-5-a-o-budapest-city-hostel", "name": "a&amp;o Budapest City", "brand": "a&amp;o Hostels",
    "tag": "#5 legjobb hotelszerű hostel", "short": "Hotelszerű szállásnak a legjobb",
    "area": "VII. kerület, az Oktogon közelében", "area_q": "Csengery+utca+11+Budapest", "district": "VII",
    "address": "1074 Budapest, Csengery utca 11.", "street": "Csengery utca 11.", "zip": "1074",
    "hw": (8.6, 504), "bk": (7.7, 5373), "dorm": 12, "private": None,
    "checkin": "Be- és kijelentkezés a 24 órás recepción", "rules": "Családokat és csoportokat is fogad",
    "cats": "tested quiet private nomad",
    "specs": ["Csendes szobák", "Remek zuhany", "Munkasarok", "Privát szobák"],
    "best_for": "Pároknak, családoknak és mindenkinek, aki a társasági élet helyett csendes, egyszerű, tiszta szobát szeretne.",
    "skip_if": "társasági hostelt keres, vagy nem szeret külön fizetni az ágyneműért.",
    "trust": "Privát szobák",
    "transit": "Oktogon (M1, 4-es, 6-os villamos) és Vörösmarty utca (M1), pár perc séta",
    "watch": "Ágynemű kb. 3 € extra; hozzon lakatot", "noise": "Csendes",
    "pros": [
      ("Kiváló szobák", "Egyszerű, csendes és tiszta szoba, fantasztikus zuhannyal."),
      ("Biztonságos tároló", "A recepción készségesen elzárták a laptopomat."),
      ("Munkasarok", "A társalgóban kiváló laptopbarát munkasarok van."),
    ],
    "cons": [
      ("Ágynemű és törölköző", "Nem ingyenes, 1150 Ft (kb. 3 €) felárat kérnek érte."),
      ("Tároló \"ketrec\"", "A szobai tárolóhoz NEM jár lakat."),
      ("Koszos párna", "A párnámat lecserélhették volna, de összességében higiénikus a hostel."),
      ("Unalmas reggeli", "Átlagos szállodai reggeli kb. 8 €-ért (opcionális)."),
    ],
    "summary": [
      "<strong>Az a&amp;o Budapest City azoknak a takarékos utazóknak való, akiknek a kényelem és a csend fontosabb a pörgő társasági életnél.</strong>",
      "Az ágyak <strong>kb. 12 €-tól</strong> indulnak, de számoljon az ágynemű felárával (kb. 3 €).",
      "Az apróbb hibák, mint a párna és az ágyneműdíj ellenére az ára és a kényelme miatt jó választás, ha nyugodt helyet és munkateret keres.",
    ],
    "groups": [
      ("Szobák, ágyak és alvásminőség", "szobák és ágyak", [
        ("Csendes, tiszta, egyszerű", "<p><strong>Egyszerű, csendes és tiszta szoba</strong>, kiváló zuhannyal. Közelebb áll egy olcsó szállodához, mint egy hostelhez.</p>"),
        ("Számoljon az extrákkal", "<p>Az <strong>ágynemű kb. 3 €</strong>, a tárolóhoz pedig saját lakat kell. Ezt is számolja bele az árba.</p>"),
      ]),
      ("Hangulat és munkatér", "közösségi terek", [
        ("Nyugodt bázis, nem buli", "<p>Kevés hostelprogram. <strong>Privát szférára és alvásra</strong> vágyóknak, pároknak és családoknak való.</p>"),
        ("Laptopos társalgó", "<p>A társalgóban <strong>kiváló laptopbarát munkasarok</strong> van.</p>"),
      ]),
      ("Felszereltség és elhelyezkedés", "felszereltség", [
        ("Biztonságos tároló", "<p>A recepció <strong>biztonságban elzárta a laptopomat</strong>, amíg nem voltam ott.</p>"),
        ("Reggeli", "<p><strong>Opcionális, szállodai reggeli kb. 8 €-ért</strong>. Rendben van, semmi különös.</p>"),
        ("Elhelyezkedés", "<p>A Csengery utcában, pár perc sétára az <strong>Oktogontól és az Andrássy úttól</strong>.</p>"),
      ]),
    ],
    "chips": [("yes", "Csendes szobák"), ("yes", "Privát szobák"), ("yes", "Munkasarok"), ("no", "Ágynemű külön (kb. 3 €)"), ("no", "Lakatot hozzon")],
    "tested": True,
  },
  {
    "n": 6, "id": "section-6-wombat-s-city-hostel", "name": "Wombat's City Hostel", "brand": "Wombat's",
    "tag": "#6 legjobb visszafogott bulihostel", "short": "Visszafogott bulihostelnek a legjobb",
    "area": "VI. kerület, Király utca", "area_q": "Kiraly+utca+20+Budapest", "district": "VI",
    "address": "1061 Budapest, Király utca 20.", "street": "Király utca 20.", "zip": "1061",
    "hw": (9.0, 14947), "bk": (8.4, 2575), "dorm": 11, "private": None,
    "checkin": "Bejelentkezés 14:00 és 23:00 között, kijelentkezés 10:00-ig", "rules": "Nincs takarodó",
    "cats": "tested party private",
    "specs": ["Saját fürdős dormok", "Ágyfüggöny", "Hostelbár", "Király utca"],
    "best_for": "Hátizsákosoknak, akik társasági bárt és éjszakai életet szeretnének a küszöbön, de jól is akarnak aludni.",
    "skip_if": "a legolcsóbb ágyat vagy egy igazán egyedi hangulatú hostelt keres.",
    "trust": "Saját fürdős dormok",
    "transit": "Deák Ferenc tér (M1, M2, M3 és a 100E reptéri busz), 3 perc séta",
    "watch": "Drága ahhoz képest, amit ad", "noise": "Bent csendes",
    "pros": [
      ("Barátságos", "Laza társasági hangulat, könnyű ismerkedni."),
      ("Nem zajos", "Bulihostelhez képest csendes. Jól ki tudja pihenni magát."),
      ("Személyzet", "Éjjel-nappal elérhető recepció és biztonságos csomagmegőrző."),
    ],
    "cons": [
      ("Ár", "Lehetnének kedvezőbbek az árak. Nem éreztem, hogy a hostel bármi különlegeset adna, ami indokolná őket."),
    ],
    "summary": [
      "<strong>A Wombat's City Hostel a budapesti éjszakai életre vágyó fiatal utazók központja</strong>, fiatalos energiával és laza hangulattal, ideális visszafogott bulihostel.",
      "Drágább a legtöbb budapesti hostelnél. Az elhelyezkedése nagy előny, de egyes részei átlagosak: a fürdők például tiszták, de semmi több.",
      "A legjobb a vendégkör volt: a világ minden tájáról érkező érdekes utazókkal ismerkedni és bulizni bőven kárpótolt az apróságokért.",
    ],
    "groups": [
      ("Szobák, ágyak és alvásminőség", "szobák és ágyak", [
        ("Saját fürdős szobák", "<p>A hostel szerint minden szobához <strong>saját fürdő és légkondi</strong> tartozik, a dormágyakon pedig függöny van.</p>"),
        ("Jobban lehet aludni, mint bulizni", "<p>Bulihostelhez képest <strong>éjjel csendes</strong>. Jól aludtam.</p>"),
      ]),
      ("Hangulat és társasági élet", "közösségi terek", [
        ("Visszafogott bulis közönség", "<p>Könnyű ismerkedni a <strong>hostelbárban</strong>, a Gozsdu udvar bárjai pedig pár lépésre vannak.</p>"),
        ("A vendégek teszik", "<p>A nemzetközi társaság volt <strong>a tartózkodásom legjobb része</strong>.</p>"),
      ]),
      ("Felszereltség és elhelyezkedés", "felszereltség", [
        ("Átlagos, de tiszta", "<p>A felszereltség <strong>tiszta, de átlagos</strong>; ne a dizájn miatt foglalja.</p>"),
        ("Központi a Király utcában", "<p>Pár percre a <strong>Deák Ferenc tértől</strong>, a 100E reptéri busztól és a zsidónegyed éjszakai életétől.</p>"),
      ]),
    ],
    "chips": [("yes", "Saját fürdős dormok"), ("yes", "Légkondi"), ("yes", "Hostelbár"), ("yes", "24 órás recepció"), ("yes", "Ingyenes széf szekrények")],
    "tested": True,
  },
  {
    "n": 7, "id": "section-7-zen-hostel", "name": "Central Market Hall Zen Hostel", "brand": "Zen Hostel",
    "tag": "#7 legjobb csendes, otthonos hostel", "short": "Csendes, otthonos szállásnak a legjobb",
    "area": "IX. kerület, Központi Vásárcsarnok", "area_q": "Vamhaz+korut+5+Budapest", "district": "IX",
    "address": "1093 Budapest, Vámház körút 5.", "street": "Vámház körút 5.", "zip": "1093",
    "hw": (8.5, 510), "bk": (8.4, 1970), "dorm": 11, "private": 15,
    "checkin": "Bejelentkezés 14:00 és 21:00 között, kijelentkezés 11:00-ig", "rules": "Korlátozott recepciós nyitvatartás",
    "cats": "tested quiet private",
    "specs": ["Otthonos hangulat", "Kis hostel", "Ingyen tea és kávé", "Vásárcsarnok"],
    "best_for": "Introvertáltaknak és lassan utazóknak, akik kicsi, hangulatos, otthonos helyet keresnek a Duna mellett.",
    "skip_if": "késő este érkezik, szekrényre van szüksége, vagy konnektoros asztalt keres.",
    "trust": "Bejelentkezés 21:00-ig",
    "transit": "Fővám tér (M4, 2-es, 47-es, 49-es villamos), a Központi Vásárcsarnok mellett",
    "watch": "Nincs késői bejelentkezés; nincs zárható tároló", "noise": "Csendes",
    "pros": [
      ("Személyzet", "Ottjártamkor egyetlen házigazda vitte az egész hostelt: barátságos, segítőkész és vidám volt. Neki köszönhető a 9/10-es értékelés."),
      ("Barátságos", "Bárhol bele lehetett kezdeni egy beszélgetésbe. A nappali kanapéja remek hely volt a csevegésre."),
      ("Olyan, mint otthon", "Ha szereti a hangulatos, otthonos érzést, ez a mennyország."),
    ],
    "cons": [
      ("Nincs éjjel-nappali bejelentkezés", "A házigazda este 9-kor ment el, és a bejelentkezés is sokáig tartott."),
      ("Kevés a személyzet", "Egy ember túl sok feladattal zsonglőrködött; legalább még egy kolléga kellett volna."),
      ("Nem biztonságos", "Nem volt zárható tároló."),
      ("Nem nomádbarát", "Nincs konnektoros munkasarok."),
    ],
    "summary": [
      "<strong>A Central Market Hall Zen Hostel kedves menedék, ha kicsi, hangulatos helyet keres, amely inkább otthon, mint hostel.</strong>",
      "Az árak kicsit átlag felettiek ahhoz képest, amit kap, a dormágyak <strong>kb. 11 €-tól</strong> indulnak. Nem a legjobb ár-érték, de ha az otthonos hangulat és a Vásárcsarnok melletti fekvés fontos, megéri.",
    ],
    "groups": [
      ("Szobák és alvásminőség", "szobák és ágyak", [
        ("Kicsi és nyugodt", "<p>Egy <strong>kis hostel nyugodt, otthonos hangulattal</strong>, bulizó közönség nélkül.</p>"),
        ("Nincs zárható tároló", "<p>Ottjártamkor <strong>nem volt zárható tároló</strong>. Tartsa magánál az értékeit, vagy válasszon másik hostelt, ha ez fontos.</p>"),
      ]),
      ("Hangulat és nappali", "közösségi terek", [
        ("Beszélgetések a nappaliban", "<p>Mindenki a <strong>nappali kanapéján</strong> köt ki beszélgetni. Társasjátékok, tea és kávé egész nap.</p>"),
        ("Nem távmunkára való", "<p>Nincs konnektoros asztal. <strong>Digitális nomádoknak a Flow Spaces vagy a Maverick a jobb.</strong></p>"),
      ]),
      ("Bejelentkezés és elhelyezkedés", "felszereltség", [
        ("Érkezzen 21:00 előtt", "<p>A bejelentkezés <strong>14:00 és 21:00 között</strong> van, a recepció nyitvatartása korlátozott. Késői járattal érkezik? Foglaljon máshol.</p>"),
        ("A Vásárcsarnok mellett", "<p>A Vámház körúton, a <strong>Központi Vásárcsarnok és a Szabadság híd mellett</strong>, a Fővám téren M4 és 2-es villamos.</p>"),
      ]),
    ],
    "chips": [("yes", "Otthonos hangulat"), ("yes", "Ingyen tea és kávé"), ("yes", "A Vásárcsarnok mellett"), ("no", "Bejelentkezés 21:00-ig"), ("no", "Nincs zárható tároló")],
    "tested": True,
  },
  {
    "n": 8, "id": "section-8-adagio-hostel-2-0-basilica", "name": "Adagio Hostel 2.0 Basilica", "brand": "Adagio Hostels",
    "tag": "#8 legjobb fekvés városnézéshez", "short": "Városnézéshez a legjobb",
    "area": "VI. kerület, Andrássy út", "area_q": "Andrassy+ut+2+Budapest", "district": "VI",
    "address": "1061 Budapest, Andrássy út 2. (1. emelet)", "street": "Andrássy út 2.", "zip": "1061",
    "hw": (8.9, 2143), "bk": (8.5, 4410), "dorm": 11, "private": 22,
    "checkin": "Bejelentkezés 15:00 és éjfél között, kijelentkezés 10:00-ig", "rules": "Nincs takarodó",
    "cats": "tested budget quiet private",
    "specs": ["Kilátás a Bazilikára", "Saját fürdőszobák", "Ingyen tea és kávé", "Andrássy út"],
    "best_for": "Városnézőknek, akik nyugodt, tiszta ágyat szeretnének az Andrássy út elején, pár lépésre a Szent István-bazilikától.",
    "skip_if": "társasági hostelt keres, vagy érzékeny a forgalom zajára.",
    "trust": "Pár lépés a Bazilikától",
    "transit": "Bajcsy-Zsilinszky út (M1) a ház előtt, Deák Ferenc tér (M1, M2, M3) rövid séta",
    "watch": "Forgalmi zaj; nincs lift (1. emelet)", "noise": "Forgalmi zaj",
    "pros": [
      ("Remek fürdőszoba", "Kiváló, tiszta saját fürdőszoba."),
      ("Kiváló elhelyezkedés", "Kilátással a Szent István-bazilikára."),
      ("Nyugodt", "Nem olyan forgalmas, mint néhány másik hostel, így több a privát szféra."),
    ],
    "cons": [
      ("Zajos", "A szobámban a forgalom miatt nagy volt a zaj."),
      ("Nincs lift", "A hostel az első emeleten van."),
      ("Személytelen", "Nincs társasági hangulat vagy személyes törődés."),
    ],
    "summary": [
      "<strong>Az Adagio 2.0 az Ön helye, ha a jó éjszakai alvás tiszta, kényelmes szobában a legfontosabb.</strong>",
      "Nincs benne semmi különleges, de az alapokat jól csinálja: jó választás olcsó, minimalista szállásnak fantasztikus helyen.",
      "A pénztárcáját sem viszi el: a közeli dátumokra a dormágyak <strong>kb. 11 €-tól</strong>, a privát szobák <strong>kb. 22 €-tól</strong> indulnak.",
    ],
    "groups": [
      ("Szobák és alvásminőség", "szobák és ágyak", [
        ("Tiszta szobák, remek fürdő", "<p>A szobámhoz <strong>kiváló, tiszta saját fürdő</strong> tartozott. Vannak dormok és saját fürdős kétágyas szobák is.</p>"),
        ("Forgalmi zaj", "<p>Az Andrássy út főútvonal, és <strong>a szobám zajos volt a forgalom miatt</strong>. Hozzon füldugót, vagy kérjen udvari szobát.</p>"),
      ]),
      ("Hangulat", "közösségi terek", [
        ("Nyugodt, nem társasági", "<p><strong>Nincs társasági élet vagy személyes törődés.</strong> Csendes bázis városnézéshez, nem ismerkedéshez.</p>"),
      ]),
      ("Felszereltség és elhelyezkedés", "felszereltség", [
        ("Konyha, tea és kávé", "<p>A hostel szerint a vendégek használhatják a <strong>teljesen felszerelt konyhákat</strong>, ingyenes tea, kávé és ágynemű jár.</p>"),
        ("Első emelet, nincs lift", "<p>Egy <strong>palota első emeletén van, lift nélkül</strong>, egy lépcsősor.</p>"),
        ("Verhetetlen a látnivalókhoz", "<p>Az <strong>Andrássy út elején</strong>, pár perc sétára a Szent István-bazilikától, az Operától és a Deák Ferenc tértől.</p>"),
      ]),
    ],
    "chips": [("yes", "Kilátás a Bazilikára"), ("yes", "Vendégkonyha"), ("yes", "24 órás recepció"), ("yes", "Ingyen tea és kávé"), ("no", "Nincs lift (1. emelet)")],
    "tested": True,
  },
  {
    "n": 9, "id": "section-9-das-nest-budapest", "name": "Das Nest Budapest", "brand": "Das Nest",
    "tag": "#9 legjobb kis, otthonos hostel", "short": "Kis, otthonos hostelnek a legjobb",
    "area": "VII. kerület, zsidónegyed", "area_q": "Akacfa+utca+10+Budapest", "district": "VII",
    "address": "1072 Budapest, Akácfa utca 10.", "street": "Akácfa utca 10.", "zip": "1072",
    "hw": (8.7, 1507), "bk": (8.4, 1474), "dorm": 15, "private": 17,
    "checkin": "Bejelentkezés 12:00 és 23:00 között, kijelentkezés 11:00-ig", "rules": "Nincs takarodó",
    "cats": "tested private kitchen",
    "specs": ["Otthonos loft", "Helyi tippek", "Vendégkonyha", "Zsidónegyed"],
    "best_for": "Egyedül utazó hátizsákosoknak és kis csoportoknak, akik hangulatos, lakásszerű hostelt keresnek barátságos házigazdákkal a bulinegyedben.",
    "skip_if": "kártyával fizetne, akadálymentes bejutás kell, vagy hétvégén is csendre vágyik.",
    "trust": "Privát szoba 17 €-tól",
    "transit": "Wesselényi utca (4-es, 6-os villamos) és Blaha Lujza tér (M2), pár perc séta",
    "watch": "Ottjártamkor csak készpénz; hétvégi utcazaj", "noise": "Hétvégi utcazaj",
    "pros": [
      ("Központi elhelyezkedés", "Budapest szívében, közel a fő látnivalókhoz és az éjszakai élethez."),
      ("Barátságos személyzet", "Kedves, segítőkész, remek helyi ajánlásokkal."),
      ("Otthonos hangulat", "Hangulatos, bensőséges hely, kiváló ismerkedésre."),
      ("Jól felszerelt konyha", "Teljesen felszerelt konyha a vendégeknek."),
      ("Helyi kapcsolatok", "Tippek bárokhoz, éttermekhez és fesztiválokhoz, amelyeket egyedül nem találna meg."),
    ],
    "cons": [
      ("Csak készpénz", "Ottjártamkor nem fogadtak kártyát, csak készpénzt."),
      ("Lehetséges zaj", "A pörgő éjszakai élet miatt éjjel zajos lehet."),
      ("Korlátozott akadálymentesség", "Nem minden fogyatékossággal élő számára akadálymentes."),
    ],
    "summary": [
      "<strong>A Das Nest ideális, ha központi budapesti szállást keres hangulatos, társasági légkörrel.</strong> A barátságos kiszolgálásról, a laza hangulatról és a remek helyi tippekről szól.",
      "Ottjártamkor hiányoztak az olyan kényelmi szolgáltatások, mint a kártyás fizetés, de ezt személyes törődéssel és remek fekvéssel pótolja. Azoknak való, akiknek a megfizethető kényelem és az ismerkedés fontosabb a luxusnál.",
      "Szobák: 4 vagy 6 ágyas vegyes vagy csak női dormok és egy kétágyas privát szoba. Dormágy <strong>kb. 15 €-tól</strong>.",
    ],
    "groups": [
      ("Szobák és alvásminőség", "szobák és ágyak", [
        ("Kis dormok", "<p><strong>4 és 6 ágyas vegyes vagy csak női dormok</strong> és egy kétágyas privát szoba. Elég kicsi ahhoz, hogy személyes legyen.</p>"),
        ("Hétvégi zaj", "<p>A bulinegyedben van, így <strong>éber alvóknak érdemes füldugót hozni</strong> péntekre és szombatra.</p>"),
      ]),
      ("Hangulat és társasági élet", "közösségi terek", [
        ("Mint egy barát lakása", "<p>A hostel <strong>felújított tetőtéri loftlakásként</strong> írja le magát, és pontosan ilyen: bensőséges és társasági.</p>"),
        ("Házigazdák helyi tippekkel", "<p>A személyzettől olyan <strong>bár-, étterem- és fesztiváltippeket</strong> kaptam, amelyek egyik útikönyvben sem szerepeltek.</p>"),
      ]),
      ("Felszereltség és fizetés", "felszereltség", [
        ("Konyha", "<p><strong>Teljesen felszerelt vendégkonyha</strong>, jó a spóroláshoz.</p>"),
        ("Hozzon készpénzt", "<p>Ottjártamkor <strong>csak készpénzt</strong> fogadtak. Nézze meg a foglalási feltételeket, és biztos, ami biztos, hozzon forintot.</p>"),
      ]),
    ],
    "chips": [("yes", "Otthonos hangulat"), ("yes", "Vendégkonyha"), ("yes", "Ingyenes széf szekrények"), ("yes", "Csak női dormok"), ("no", "Csak készpénz (ottjártamkor)")],
    "tested": True,
  },
  {
    "n": 10, "id": "section-10-the-hive-party-hostel", "name": "The Hive Party Hostel", "brand": "The Hive",
    "tag": "#10 legjobb nagy bulihostel", "short": "A legnagyobb bulihostel",
    "area": "VII. kerület, zsidónegyed", "area_q": "Dob+utca+19+Budapest", "district": "VII",
    "address": "1074 Budapest, Dob utca 19.", "street": "Dob utca 19.", "zip": "1074",
    "hw": (9.0, 7023), "bk": None, "dorm": 13, "private": 20,
    "checkin": "Bejelentkezés 15:00 és éjfél között, kijelentkezés 11:00-ig", "rules": "Szigorúan 18 év felett, nincs takarodó",
    "cats": "party private",
    "specs": ["Tetőbár", "Napi kocsmatúrák", "Csak 18+", "Zsidónegyed"],
    "best_for": "18 év feletti csoportoknak és egyedül bulizóknak, akik nagy, hangos bulihostelt szeretnének tetőbárral a romkocsmanegyedben.",
    "skip_if": "éber alvó, korán kel, vagy ágyfüggönyt szeretne.",
    "trust": "Szigorúan 18+",
    "transit": "Astoria (M2) és Deák Ferenc tér (M1, M2, M3), pár perc séta",
    "watch": "Zaj a lenti klubból; nincs ágyfüggöny", "noise": "Hangos (bulihostel)",
    "why": [
      ("Nagy bulihostel", "A hostel szerint 300+ ágy 2015 óta, napi kocsmatúrákkal, bingós kocsmatúrákkal, SPArtykkal és bulihajókkal."),
      ("Tetőbár", "Saját tetőbár a vendégeknek, napi happy hourral 16 és 19 óra között."),
      ("Elhelyezkedés", "A romkocsmanegyedben, rövid sétára a Gozsdu udvartól és a Szimpla Kerttől."),
      ("Praktikus", "24 órás recepció, széf szekrények, fizetés készpénzzel vagy kártyával."),
    ],
    "skip": [
      ("Zaj", "Maga a hostel figyelmezteti az éber alvókat és a korán kelőket; a vendégek a lenti klub zaját említik."),
      ("Nincs ágyfüggöny", "Gyakori vendégkérés, hogy legyen függöny az ágyakon."),
      ("Wi-Fi", "A gyenge wifi visszatérő panasz a vendégektől."),
      ("Korhatár", "Szigorúan 18 év felett."),
    ],
    "summary": [
      "<strong>A The Hive Budapest nagy, hangos bulihostele.</strong> 300+ ággyal, tetőbárral és napi kocsmatúrákkal az éjszakákra épül, nem a korai reggelekre.",
      "Az Onefam bulis alternatívájaként vettem fel: az itteni tények a hostel saját információiból és a vendégek visszajelzéseiből származnak, 2026. november 14-én ellenőrizve. A dormágyak <strong>kb. 13 €-tól</strong> indulnak.",
    ],
    "groups": [],
    "chips": [("yes", "Tetőbár"), ("yes", "Napi kocsmatúrák"), ("yes", "24 órás recepció"), ("yes", "Ingyenes széf szekrények"), ("no", "Szigorúan 18+")],
    "tested": False,
  },
]


def _areas(H, a):
    return (
        '<h3>VII. kerület (zsidónegyed): az éjszakai életért</h3>\n'
        '<p>Itt vannak a romkocsmák, a Gozsdu udvar és a Szimpla Kert, és itt van az %s, a %s és a %s is. Bulizáshoz remek, <strong>éber alvóknak hétvégén a legrosszabb</strong>.</p>\n'
        '<h3>VI. kerület (Király utca, Andrássy út, Oktogon): központi és jól megközelíthető</h3>\n'
        '<p>A %s, az %s és az %s a főútvonalakon van, az M1 és a 24 órás 4-es, 6-os villamos mellett. Mindenhova el lehet sétálni, de a <strong>főúti forgalom</strong> zajos lehet.</p>\n'
        '<h3>IX. kerület (Központi Vásárcsarnok): nyugodtabb, a folyó mellett</h3>\n'
        '<p>A %s, a %s és a %s a Központi Vásárcsarnok mellett van, pár percre a Dunától. Ezt választanám, ha <strong>csendesebb éjszakákat</strong> szeretne, de gyalog is elérné a belvárost.</p>\n'
        '<p>Repülővel érkezik? Itt olvashatja, <a href="/hu/budapest-reptér-városközpont">hogyan juthat el a reptérről a belvárosba</a>: a 100E busz a Deák Ferenc téren áll meg, rövid sétára a VI. és VII. kerületi hostelektől.</p>'
    ) % (a(H[2]), a(H[9]), a(H[10]), a(H[6]), a(H[8]), a(H[3]), a(H[1]), a(H[4]), a(H[7]))


UI = {
    "url": HU, "home": "Főoldal", "home_url": "https://www.budapestadventures.com/hu", "about_url": "https://www.budapestadventures.com/hu/rolunk",
    "title": "A 10 legjobb budapesti hostel 2026-ban (9-ben aludtam)",
    "h1_main": "A 10 legjobb budapesti hostel 2026-ban", "h1_muted": "(9-ben aludtam)",
    "meta": "Budapest 9 legjobb hostelében aludtam, a Mavericknél 30 éjszakát. Dormágy 8 €-tól: a legjobb bulis, csendes, olcsó és nomád hostelek, környékenként.",
    "breadcrumb": "A legjobb budapesti hostelek", "kicker_badge": "2026-os hostel-összehasonlítás",
    "author_line": 'Írta: <a href="/hu/rolunk" target="_blank">Adam Dimitrov</a>, alapító és budapesti tesztelő',
    "author_role": "A 10-ből 9-ben aludtam • Saját fotók és videós értékelések",
    "last_updated": "<strong>Frissítve</strong>: 2026. november 14.",
    "job_title": "Alapító és budapesti tesztelő",
    "intro": (
        '<p>A rossz budapesti hostel nem pénzbe, hanem alvásba kerül. A belvárosi dormágyak <strong>8 és 15 € között</strong> vannak éjszakánként, '
        'de egy bulihostel a zsidónegyedben és egy csendes kapszulás hostel a Központi Vásárcsarnok mellett két teljesen más utazás.</p>\n'
        '<p>Az alábbi <strong>10 hostelből 9-ben én magam aludtam</strong>, a Mavericknél például <strong>30 éjszakát 280 €-ért</strong>, és egymás mellé tettem őket abban, '
        'ami a foglalásnál számít: éjszakai zaj, privát szféra az ágyban, fürdők, konyha, korhatár, a közönség és a valódi éjszakai ár. '
        'A The Hive az egyetlen bulis választás, ahol nem aludtam, ezért csak ellenőrzött tények szerepelnek róla, "tesztelt" jelölés nélkül.</p>\n'
        '<p>Árak és értékelések ellenőrizve: <strong>%s</strong> A szűrőkkel egyből a bulis, csendes, olcsó, privát szobás vagy digitális nomád hostelekre ugorhat.</p>\n' % CHECKED),
    "filters": [("party", "🎉 Társasági és buli"), ("quiet", "😴 Csendes alvás"), ("budget", "💶 11 € alatt"),
                ("private", "🛏️ Privát szobák"), ("nomad", "💻 Digitális nomádok"), ("kitchen", "🍳 Vendégkonyha")],
    "district_fmt": "%s. kerület", "decimal": ",", "thousands": " ", "k": "k",
    "tested_chip": "✓ Személyesen tesztelve",
    "best_for_card": "Kinek ajánlom:", "best_for_summary": "Kinek ajánlom:", "skip_if": "Kerülje, ha",
    "from_eur": "%d €-tól", "eur": "%d €", "card_psub": "Dormágy/éj • 2026. 11. 14.",
    "card_btn": "Árak és időpontok →", "read_review": "Értékelés ↓",
    "pros": "Előnyök:", "cons": "Hátrányok:", "why": "Miért válassza:", "why_skip": "Miért ne:",
    "video": "Videó:", "watch_my": "Nézze meg a",
    "summary_title": "Összefoglaló és értékelés", "summary_pill": "Áttekintés",
    "swipe_photos": "%d fotó, lapozzon →", "one_photo": "1 fotó", "no_photo": "Saját tapasztalat",
    "photo_alt": "%s: %s, saját fotó", "prev_photo": "Előző fotó", "next_photo": "Következő fotó",
    "buy_badge": "Élő árak és szabad helyek", "buy_sub": "Dormágy éjszakánként • Ellenőrizve: " + CHECKED,
    "address_perk": "Cím: <strong>%s</strong>", "privates_perk": "Privát szoba <strong>%d €-tól</strong>",
    "buy_cta": "Időpontok és árak", "buy_trust": "Az ár dátumonként változik; a végső ár fizetés előtt látható",
    "qf": {"title": "Gyors tények: %s", "address": "Cím", "dorm": "Dormágy", "transit": "Megközelítés", "checkin": "Bejelentkezés",
           "rules": "Házirend", "ratings": "Értékelések", "watch": "Mire figyeljen",
           "dorm_fmt": "%d €-tól éjszakánként (ellenőrizve: " + CHECKED + ")", "priv_fmt": ", privát szoba %d €-tól",
           "hw_fmt": "Hostelworld %s/10 (%s értékelés)", "bk_fmt": ", Booking.com %s/10 (%s értékelés)"},
    "breakdown_h2": "Részletes értékelések: a 10 legjobb budapesti hostel",
    "breakdown_sub": "9-ben aludtam, 1 bulis választás ellenőrzött tények alapján • Kattintson a kinyitáshoz vagy bezáráshoz",
    "picks": [
        ("Összességében", 1, "Társasági, de nincs bulizaj, függönyös ágyak, remek fürdők, és 280 € a 30 éjszakámért."),
        ("Egyedül utazóknak (18 és 39 év között)", 2, "Az ingyenes napi programokkal és kocsmatúrákkal pofonegyszerű barátkozni. Elmúlt 39? Válassza a Mavericket vagy a Wombat'st."),
        ("Bulizáshoz", 10, lambda H: 'A nagy, hangos választás tetőbárral a romkocsmanegyedben. Visszafogottabban? <a href="#%s">%s</a>.' % (H[6]['id'], H[6]['name'])),
        ("A legolcsóbb ágy", 3, "Ágy kb. 8 €-tól ingyenes reggelivel. Hozzon füldugót: villamoscsomópontnál van."),
        ("Csendes alváshoz", 1, lambda H: 'Csendes mellékutca a IX. kerületben. Szintén nyugodt: <a href="#%s">%s</a> és <a href="#%s">%s</a>.' % (H[7]['id'], H[7]['name'], H[5]['id'], H[5]['name'])),
        ("Digitális nomádoknak", 4, "Laptopbarát társalgó és coworking tér. Hosszabb maradáshoz a Maverick az alternatíva."),
        ("Pároknak és családoknak", 5, "Egyszerű, csendes, tiszta szobák privát lehetőséggel. Számoljon kb. 3 €-val az ágyneműért."),
        ("Városnézéshez", 8, "Az Andrássy út elején, pár percre a Szent István-bazilikától és a Deák tértől."),
        ("Kicsi és otthonos", 9, "Olyan, mint egy barát loftja a zsidónegyedben, helyi tippekkel teli házigazdákkal."),
    ],
    "sections": {
        "picks_badge": "Gyors választás", "picks_h2": "A legjobb budapesti hostel utazótípusonként",
        "picks_sub": "Rövid válasz minden utazástípusra, a saját tartózkodásaim alapján",
        "table_badge": "Egymás mellett", "table_h2": "Budapesti hostelek összehasonlítva: ár, zaj és buktatók",
        "table_sub": "Dormárak és Hostelworld-pontszámok ellenőrizve: " + CHECKED + " A zaj és a buktatók a saját tartózkodásaimból (The Hive: vendégvisszajelzések).",
        "table_cols": ["Hostel", "Kinek a legjobb", "Környék", "Dormágy", "Hostelworld", "Éjszakai zaj", "Mire figyeljen"],
        "areas_badge": "Környékek", "areas_h2": "Hol szálljon meg Budapesten, ha hostelt keres",
        "areas_sub": "Mind a 10 a pesti belvárosban van. A kerület dönti el, mennyire hangosak az éjszakái.",
        "areas_body": _areas,
        "map_h2": "Térkép: a legjobb budapesti hostelek",
        "map_sub": 'A lista hostelei a belvárosi kerületekben (<a href="/hu/legjobb-gyalogtúrák-budapest">VII. kerület, zsidónegyed</a>, V. kerület, VI. kerület Terézváros és IX. kerület Ferencváros)',
        "types_h2": "Budapesti hosteltípusok",
    },
    "faq": [
        ("Melyik a legjobb hostel Budapesten?",
         "<p>Összességében a <strong>Maverick Central Market</strong> a kedvencem: társasági, de nincs bulizaj, függönyös ágyak, remek fürdők és valódi hosszú távú ár (márciusban 30 éjszakáért 280 €-t fizettem). "
         "Társasági utazáshoz az <strong>Onefam Budapest</strong>, a legolcsóbb ágyhoz az <strong>Avenue Hostel</strong> a jó választás.</p>"),
        ("Melyek a legjobb budapesti hostelek egyedül utazóknak?",
         "<p>Az <strong>Onefam Budapest</strong>ben a legkönnyebb barátokat szerezni az ingyenes napi programokkal és kocsmatúrákkal, de csak <strong>18 és 39 év közötti</strong> vendégeket fogad. "
         "Elmúlt 39, vagy többet aludna? A <strong>Maverick Central Market</strong> és a <strong>Wombat's City Hostel</strong> társasági, bulikényszer nélkül.</p>"),
        ("Melyek a legjobb bulihostelek Budapesten?",
         "<p>Az <strong>Onefam Budapest</strong> (társasági, napi kocsmatúrák), a <strong>The Hive Party Hostel</strong> (a nagy, hangos, tetőbáros, szigorúan 18+) és a "
         "<strong>Wombat's City Hostel</strong> (visszafogott buli, lehet mellette aludni). Mindhárom rövid sétára van a zsidónegyed romkocsmáitól.</p>"),
        ("Melyik budapesti hostelben lehet a legcsendesebben aludni?",
         "<p>A <strong>Maverick Central Market</strong>ben (csendes mellékutca), a <strong>Central Market Hall Zen Hostel</strong>ben (kicsi és otthonos) és az <strong>a&amp;o Budapest City</strong>ben (hotelszerű szobák). "
         "Éber alvóként kerülje az Avenue Hostelt: az Oktogon villamoscsomópontjánál van.</p>"),
        ("Mennyibe kerül egy hostel Budapesten?",
         "<p>2026. november 14-én ennél a 10 hostelnél a dormágyak <strong>kb. 8 és 15 € között</strong> indultak éjszakánként (Avenue 8 €-tól, Das Nest 15 €-tól), a privát szobák kb. 17 és 28 € között. "
         "Drágább <strong>hétvégén, nyáron (májustól szeptemberig), az augusztusi Sziget Fesztivál, a karácsonyi vásárok és szilveszter idején</strong>.</p>"),
        ("Melyik környéken érdemes hostelt foglalni Budapesten?",
         "<p>A <strong>VII. kerületben (zsidónegyed)</strong> az éjszakai élet miatt, a <strong>VI. kerületben</strong> (Király utca, Andrássy út) a központi, jól megközelíthető bázisért, "
         "a <strong>IX. kerületben</strong>, a Központi Vásárcsarnok mellett pedig a csendesebb éjszakákért a Duna közelében.</p>"),
        ("Van korhatár a budapesti hostelekben?",
         "<p>Van, ahol igen. A házirendjük szerint az <strong>Onefam Budapest 18 és 39 év közötti vendégeket fogad</strong>, a <strong>The Hive szigorúan 18 év feletti</strong>, az <strong>Avenue Hostel pedig 6 és 49 év között</strong>. Foglalás előtt nézze meg a szabályokat.</p>"),
        ("Biztonságosak a budapesti hostelek?",
         "<p>Általában igen, de apró lopások előfordulnak: egy hostelben elloptak tőlem egy pulóvert és egy doboz orrtapaszt. <strong>Zárja el az értékeit a szekrényébe</strong>, és hozzon lakatot, mert néhány hostel "
         "(Avenue, a&amp;o) nem ad. A Flow Spaces ingyen ad egyet.</p>"),
        ("Milyen szempontok alapján választotta ki a legjobb budapesti hosteleket?",
         "<p>A 10 hostelből 9-ben aludtam, és ezek alapján értékeltem őket: <strong>elhelyezkedés, éjszakai zaj, tisztaság, az ágy kényelme és privát szférája, felszereltség, a közönség és az ár</strong>. "
         "A The Hive ellenőrzött tények és vendégvisszajelzések alapján szerepel bulis választásként, tesztelt jelölés nélkül.</p>"),
        ("Mit vigyek magammal egy hostelbe?",
         "<p><strong>Kötelező:</strong> füldugó és alvómaszk. <strong>Alapok:</strong> papucs, pizsama, telefontöltő, nedves törlőkendő, dezodor, fogkefe és fogkrém. "
         "<strong>Opcionális</strong> (nézze meg, mit ad a hostel): törölköző, lakat, sampon és tusfürdő.</p>"),
    ],
    "sticky_trust": "Dormágy/éj", "sticky_cta": "Árak →", "sheet_label": "Ugrás egy budapesti hostelre",
    "toc_breakdown": "Részletes értékelések (10 hostel)",
    "szimpla_alt": "A Szimpla Kert romkocsma, rövid sétára a The Hive-tól a Dob utcában",
    "szimpla_pill": "Szimpla Kert, 3 perc séta",
    "collapse_label": "Bezárás", "expand_label": "Értékelés megnyitása",
    "price_range": "Dormágy %d €-tól",
}
