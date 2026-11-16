# -*- coding: utf-8 -*-
"""HU pill dropdown copy for /hu/legjobb-hostelek-budapesten (order = hostels_pills_en.py)."""
T = [
  # 1 Maverick Central Market
  ("Függöny minden ágyon.", "Modern dormok függönnyel és nagy szekrényekkel, így egy teli szoba is nyugodt.", "Zárja el az értékeit: nálam elloptak egy pulóvert."),
  ("Tetőterasz a vendégeknek.", "Társasági, de nem bulihostel: este könnyű ismerkedni, utána aludni.", "Közönség: egyedül utazók, hosszabb távra érkezők és távmunkások."),
  ("Lónyay utca, IX. kerület.", "Kisebb mellékutca, távol a VII. kerület bulis utcáitól. 30 éjszaka alatt alig volt utcazaj.", "A Kálvin tér (M3, M4) és a Fővám tér (M4, 2-es, 47-es, 49-es villamos) pár perc séta."),
  ("30 éjszaka 280 €-ért.", "Ez márciusban kb. 9,33 € éjszakánként, a legjobb hosszú távú ár, amit a belvárosban találtam.", "Dormágy kb. 10 €-tól közeli dátumokra, privát szoba 28 €-tól."),
  # 2 Onefam Budapest
  ("Minden nap van program.", "Ingyenes nappali programok, este ivós játékok a bárban. A személyzet mindenkit bevon.", "Itt a legkönnyebb egyedül érkezni és társasággal távozni."),
  ("Kocsmatúrák a romkocsmákba.", "A hostelbuli 23 és éjfél között ér véget, utána a csapat indul a zsidónegyedbe.", "Nincs takarodó; bejelentkezés 15:00 és 23:00 között."),
  ("Csak 18 és 39 év között.", "Csak 18 és 39 év közötti vendégek szállhatnak meg, ettől fiatal és közösségi a társaság.", "Elmúlt 39? A Maverick korhatár nélkül ad hasonló közösséget."),
  ("4 perc a Deák Ferenc térig.", "M1, M2, M3 és a 100E reptéri busz, a Rumbach Sebestyén utca 6-tól.", "A bárokból gyalog hazaér."),
  # 3 Avenue Hostel
  ("Reggeli az árban.", "Plusz kedvezményes vacsora. A magyar élelmiszerárak mellett a kaja többet spórol naponta, mint amennyibe az ágy kerül.", "Ottjártamkor a vacsorakedvezményhez kis minimális bárfogyasztás kellett."),
  ("Függönyös emeletes ágyak.", "A 10 ágyas szobám függönyös volt, de ez volt a gyenge pont. A 4, 8 és 12 ágyas szobák jobbak, pár euróval drágábbak.", "Lakatot nem adnak: hozzon magával, vagy vegyen egyet kb. 3 €-ért."),
  ("Éjszakai villamos az ajtóban.", "Az M1 és a 4-es, 6-os éjjel-nappali villamos a ház előtt áll meg, hajnali 3-kor is könnyű hazajutni.", "Az ára: egész éjjel jár a villamos. Hozzon füldugót."),
  ("Oktogon tér 4, VI. kerület.", "Az Andrássy út és a Nagykörút találkozásánál, gyalog a belváros.", "A recepció 0-24 nyitva, bejelentkezés 14:00-tól éjfélig."),
  # 4 Flow Spaces
  ("Valódi munkasarok.", "A társalgóban laptopbarát munkaterület van, itt a legjobb a távmunkára.", "Közösségi, de nyugodt: inkább kollégium, mint kocsmatúra-központ."),
  ("Lakat jár hozzá.", "A tárolódobozhoz ingyen lakat jár, nem kell 3 €-t fizetni, mint máshol.", "A recepció 0-24 nyitva."),
  ("Kapszulaágy mindennel.", "Minden ágyhoz függöny, konnektor, lámpa, tálca és tárolódoboz tartozik.", "Szűkösek a szobák: kevés a hely, amikor mindenki pakol."),
  ("Gönczy Pál utca 2.", "Egy épületnyire a Nagyvásárcsarnoktól, pár perc séta a Dunáig.", "3. emelet, lift nincs. A Fővám tér (M4, 2-es, 47-es, 49-es villamos) közel van."),
  # 5 a&o Budapest City
  ("Olcsó hotel nyugalma.", "Egyszerű, csendes, tiszta szobák, kevés hostelhangulattal, alvásra tervezve.", "Pároknak, családoknak és mindenkinek, aki magánszférát akar."),
  ("Elképesztő zuhany.", "Egyszerű, csendes és tiszta szobában a zuhany volt a kiemelkedő.", "Ágynemű és törölköző külön díjas: 1150 Ft (kb. 3 €)."),
  ("Laptopbarát társalgó.", "Kiváló munkasarok a társalgóban, és a recepció biztonságosan megőrizte a laptopomat, amíg nem voltam ott.", "Opcionális szállodai reggeli kb. 8 €-ért."),
  ("Privát szobák 2 főtől.", "Privát szobák a dormok mellett, 0-24 recepcióval, bármikor bejelentkezhet.", "Csengery utca 11, pár percre az Oktogontól (M1, 4-es és 6-os villamos)."),
  # 6 Wombat's City Hostel
  ("Fürdő minden szobában.", "Minden szoba saját fürdős és légkondis, nincs sorbanállás a folyosón.", "Tiszta, de átlagos: ne a dizájn miatt foglalja."),
  ("Saját ágyfüggöny.", "Bulihostelhez képest csendes éjszaka. Jól aludtam.", "Ingyenes biztonsági szekrények."),
  ("Közösségi hostelbár.", "A hostelbárban könnyű ismerkedni, a Gozsdu udvar bárjai pár lépésre vannak.", "A nemzetközi társaság volt a legjobb rész."),
  ("Király utca 20.", "3 perc séta a Deák Ferenc térig (M1, M2, M3 és a 100E reptéri busz).", "Bejelentkezés 14:00 és 23:00 között, kijelentkezés 10:00-ig."),
  # 7 Central Market Hall Zen Hostel
  ("Igazi nappali.", "A kanapén köt ki mindenki beszélgetni, napközben társasjátékokkal.", "Ha szereti az otthonos, meghitt hangulatot, ez maga a mennyország."),
  ("Kicsi és személyes.", "Ottjártamkor egyetlen kedves vendéglátó vitte az egész hostelt. Miatta kapja a 9/10-es értékeléseket.", "Nincs zárható tároló és konnektoros asztal sem."),
  ("Egész nap ingyen.", "Önkiszolgáló tea és kávé egész nap, a nappaliban.", "Bejelentkezés csak 14:00 és 21:00 között: késői érkezéshez válasszon mást."),
  ("Vámház körút 5.", "A Nagyvásárcsarnok és a Szabadság híd mellett, pár percre a Dunától.", "A Fővám tér (M4, 2-es, 47-es, 49-es villamos) az ajtó előtt."),
  # 8 Adagio Hostel 2.0 Basilica
  ("Kilátás a Szent István-bazilikára.", "Az Andrássy út elején, pár perc séta a Bazilikától, az Operától és a Deák Ferenc tértől.", "A lista legjobb bázisa a gyalogos városnézéshez."),
  ("Saját fürdőszoba.", "Dormok és kétágyas szobák saját fürdővel; az enyém kiváló és tiszta volt.", "Privát szoba kb. 22 €-tól."),
  ("Ingyen tea, kávé és ágynemű.", "Önkiszolgáló tea és kávé, teljesen felszerelt vendégkonyhák, a hostel szerint.", "Nyugodt, nem közösségi: nincsenek programok, nincs személyes törődés."),
  ("Andrássy út 2, 1. emelet.", "A Bajcsy-Zsilinszky út (M1) az ajtóban, a Deák Ferenc tér (M1, M2, M3) rövid séta.", "Főútvonal: kérjen udvari szobát. Egy lépcsősor, lift nincs."),
  # 9 Das Nest Budapest
  ("Tetőtéri loftlakás.", "Felújított és meghitt, olyan, mintha egy barátjánál lakna.", "4 és 6 ágyas vegyes vagy női dormok, plusz egy privát franciaágyas szoba."),
  ("Tippek, amik nincsenek a neten.", "A vendéglátóktól olyan bár-, étterem- és fesztiváltippeket kaptam, amik egyik útikönyvben sem szerepeltek.", "Barátságos, kedves személyzet."),
  ("Teljesen felszerelt konyha.", "Főzzön magának, és spóroljon a budapesti éttermi árakon.", "Ottjártamkor csak készpénz volt: vigyen forintot a biztonság kedvéért."),
  ("Akácfa utca 10, VII. kerület.", "A bulinegyedben, közel a fő látnivalókhoz és a romkocsmákhoz.", "4-es és 6-os villamos a Wesselényi utcánál. Hétvégére vigyen füldugót."),
  # 10 The Hive Party Hostel
  ("Csak vendégeknek szóló tetőbár.", "Happy hour minden nap 16 és 19 óra között.", "300+ ágy, 2015 óta nyitva, a hostel szerint."),
  ("Minden este buli.", "Napi kocsmatúrák, plusz bingós túrák, SPArtyk és bulihajók a hostel szervezésében.", "A vendégek említik a lenti klub zaját."),
  ("Szigorúan 18 év felett.", "Az esti bulikra épül, nem a korai kelésre.", "Bejelentkezés 15:00-tól éjfélig; készpénz vagy kártya."),
  ("Dob utca 19, VII. kerület.", "Rövid séta a Gozsdu udvarig és a Szimpla Kertig.", "Az Astoria (M2) és a Deák Ferenc tér (M1, M2, M3) pár percre."),
]
