# -*- coding: utf-8 -*-
"""Hrvatski tekstovi: /hr/najbolji-hosteli-budimpesta. Činjenice: hostels_data_en.py (14. 11. 2026.)."""
from hostels_data_en import CHECKED_ISO
from hostels_i18n import build

CHECKED = "14. studenoga 2026."
URL = "https://www.budapestadventures.com/hr/najbolji-hosteli-budimpesta"

_T = [
  {  # 1 Maverick
    "tag": "🏆 #1 Najbolji hostel ukupno", "short": "Najbolji ukupno",
    "area": "IX. okrug, Velika tržnica",
    "checkin": "Prijava od 15:00, odjava do 11:00", "rules": "Bez policijskog sata",
    "specs": ["Zavjese na krevetima", "Krovna terasa", "Mirna sporedna ulica", "Isplativ za duži boravak"],
    "best_for": "Solo putnicima, digitalnim nomadima i backpackerima na dužem boravku koji žele društven hostel bez buke od zabava.",
    "skip_if": "tražite party hostel odmah pokraj ruin barova.",
    "trust": "Privatne sobe od 28 €",
    "transit": "Kálvin tér (M3, M4) i Fővám tér (M4, tramvaji 2, 47, 49), oboje nekoliko minuta pješice",
    "watch": "Puna kuhinja u špici; zaključajte vrijedne stvari", "noise": "Mirno",
    "pros": [
      ("Povoljan", "Izvan sezone dobio sam krevet već od 9 € po noći. U ožujku sam za 30 noći platio 280 €."),
      ("Odličan za duži boravak", "Osjećate se kao u vlastitoj sobi u studentskom domu, udobno i na mjesec dana."),
      ("Odlična lokacija", "U mirnijem IX. okrugu, a opet dovoljno središnje za noćni život i javni prijevoz."),
      ("Odlične sobe", "Moderne spavaonice s velikim ormarićima i zavjesama na krevetima."),
      ("Odlične kupaonice", "Zajedničke (ili privatne) kupaonice su održavane, čiste i kvalitetne."),
      ("Malo buke", "Buka s ulice je minimalna jer je hostel u manjoj ulici."),
    ],
    "cons": [
      ("Kuhinja", "U špici je tijesna, a kuhinjsko posuđe treba zamijeniti. Brzo se zaprlja iako se čisti svaki dan. Hladnjak je stalno bio pun i neuredan."),
      ("Krađa", "Ukrali su mi majicu s kapuljačom i kutiju flastera za nos. To se može dogoditi u bilo kojem hostelu, ne samo u Mavericku. <strong>Vrijedne stvari uvijek zaključajte</strong>."),
    ],
    "summary": [
      "<strong>Maverick Central Market je za one koji žele udobnost, i na kratkom i na dužem boravku.</strong> Osjećate se kao u vlastitoj sobi u studentskom domu, udobno i na mjesec dana.",
      "Nije <a href=\"#section-2-hostel-one\">party hostel</a>, ali ima <strong>puno prilika za upoznavanje ljudi</strong>.",
      "<strong>Izvanredan omjer cijene i kvalitete</strong>: <strong>u ožujku sam ovdje proveo 30 noći za 280 €</strong> (oko 9,33 € po noći). Pri mojoj provjeri 14. studenoga 2026. kreveti za bliske datume bili su <strong>od oko 10 €</strong>, a i u glavnoj sezoni cijena je poštena za ovu kvalitetu.",
    ],
    "video": "video recenziju hostela Maverick Central Market",
    "groups": [
      ("Sobe, kreveti i kvaliteta sna", "sobe i kreveti", [
        ("Kreveti u spavaonici sa zavjesom", "<p>Spavaonice su <strong>moderne, sa zavjesama na krevetima i velikim ormarićima</strong>, pa je i puna soba mirna.</p>"),
        ("Mirne noći", "<p>Nalazi se u <strong>manjoj sporednoj ulici u IX. okrugu</strong>, daleko od party ulica VII. okruga. Tijekom mojih 30 noći buka s ulice bila je minimalna.</p>"),
        ("Prava cijena za duži boravak", "<p><strong>30 noći u ožujku stajalo je 280 €.</strong> Kao bazu za digitalnog nomada ili sporo putovanje nisam našao bolju cijenu u centru.</p>"),
      ]),
      ("Atmosfera i društveni život", "zajednički prostori", [
        ("Društven, ali ne party hostel", "<p>Kao prijateljski studentski dom. <strong>Lako je upoznati ljude</strong> u zajedničkim prostorima, bez vike u četiri ujutro.</p>"),
        ("Koga ćete upoznati", "<p>Solo putnike, goste na dužem boravku i ljude koji rade na daljinu. Savršeno ako navečer želite društvo, a poslije dobar san.</p>"),
      ]),
      ("Sadržaji, kuhinja i kupaonice", "sadržaji", [
        ("Kupaonice", "<p>Zajedničke i privatne kupaonice bile su <strong>čiste i kvalitetne</strong>, jedan od najboljih dijelova mog boravka.</p>"),
        ("Kuhinja u stvarnosti", "<p>Kuhinja za goste je <strong>tijesna u špici</strong>, posuđe istrošeno, a hladnjak uvijek pun. Označite svoju hranu.</p>"),
        ("Zaključajte svoje stvari", "<p>Ukrali su mi majicu s kapuljačom i kutiju flastera za nos. <strong>Koristite ormariće</strong> za sve što bi vam nedostajalo.</p>"),
      ]),
    ],
    "chips": [("yes", "Zavjese na krevetima"), ("yes", "Krovna terasa"), ("yes", "Kuhinja za goste"), ("yes", "Recepcija 24 h"), ("yes", "Besplatna garderoba za prtljagu")],
  },
  {  # 2 Onefam
    "tag": "#2 Najbolji društveni hostel za solo putnike", "short": "Najbolji za solo putnike",
    "area": "VII. okrug, židovska četvrt",
    "checkin": "Prijava od 15:00 do 23:00, odjava do 11:00", "rules": "Samo od 18 do 39 godina, bez policijskog sata",
    "specs": ["Besplatne dnevne aktivnosti", "Obilasci barova", "18 do 39 godina", "Deák tér"],
    "best_for": "Solo putnicima od 18 do 39 godina koji odmah žele društvo, dnevne aktivnosti i noćne zabave.",
    "skip_if": "imate više od 39 godina, kao par želite privatnost ili rano liježete.",
    "trust": "18 do 39 godina",
    "transit": "Deák Ferenc tér (M1, M2, M3 i autobus za zračnu luku 100E), oko 4 minute pješice",
    "watch": "Skuplji od većine; samo od 18 do 39 godina", "noise": "Živo do ponoći",
    "pros": [
      ("Najbolji party hostel", "Igre s pićem u baru, zatim ruin barovi, a danju razgledavanje: odlično ćete se zabaviti."),
      ("Organizirane aktivnosti", "Onefam organizira dnevne i večernje aktivnosti (obilasci barova, igre s pićem)."),
      ("Savršena lokacija", "Usred židovske četvrti, blizu stanice autobusa 100E za zračnu luku, znamenitosti i noćnog života."),
      ("Odlične sobe", "Prostrane sobe sa sigurnim spremištem i ormarićima. Kreveti pružaju privatnost i udobnost."),
      ("Malo buke", "Razina buke je prihvatljiva, zabava se obično stiša između 23 sata i ponoći."),
    ],
    "cons": [
      ("Nema mjesta uz krevet", "Na krevetima na kat nema mjesta za slušalice, novčanik i mobitel."),
      ("Problemi s tušem", "Temperatura vode varira, a loše postavljen senzor pokreta gasi svjetlo u tušu."),
      ("Cijena", "Skuplji od drugih hostela u Budimpešti. Zbog društva i zabava isplati se doplatiti."),
    ],
    "summary": [
      "<strong>Onefam Budapest je najbolji izbor ako volite biti među ljudima, sklapati prijateljstva i zabavljati se.</strong>",
      "Skuplji je od većine hostela u Budimpešti, ali vrijedi svoje cijene ako želite otvoren, društven boravak. Pazite na <strong>dobnu granicu od 18 do 39 godina</strong>.",
    ],
    "video": "video recenziju hostela Onefam Budapest",
    "groups": [
      ("Sobe, kreveti i kvaliteta sna", "sobe i kreveti", [
        ("Prostrane sobe, sigurno spremište", "<p>Sobe su <strong>prostrane, sa sigurnim spremištem i ormarićima</strong>, a kreveti pružaju privatnost i udobnost.</p>"),
        ("Nema police uz krevet", "<p>Na krevetu <strong>nemate gdje ostaviti mobitel, slušalice ili novčanik</strong>. Ponesite malu torbicu.</p>"),
        ("Kada nastupa mir", "<p>Zabava se obično stiša <strong>između 23 sata i ponoći</strong>, a onda društvo odlazi u ruin barove.</p>"),
      ]),
      ("Atmosfera i društveni život", "zajednički prostori", [
        ("Društvo odmah", "<p>Ako stižete sami i brzo želite prijatelje, <strong>ovo je pravo mjesto</strong>. Osoblje uključuje sve.</p>"),
        ("Dnevne i večernje aktivnosti", "<p>Besplatne dnevne aktivnosti, a navečer igre s pićem i <strong>obilasci barova</strong> po židovskoj četvrti.</p>"),
      ]),
      ("Sadržaji, kupaonice i lokacija", "sadržaji", [
        ("Hirovi tuša", "<p>Temperatura vode varira, a <strong>senzor pokreta gasi svjetlo dok se tuširate</strong>.</p>"),
        ("Baza u židovskoj četvrti", "<p>Nekoliko minuta od <strong>Deák Ferenc tér i autobusa 100E za zračnu luku</strong>, iz barova se vraćate pješice.</p>"),
      ]),
    ],
    "chips": [("yes", "Besplatne dnevne aktivnosti"), ("yes", "Bar u hostelu"), ("yes", "Kuhinja 0-24"), ("yes", "Besplatni ormarići"), ("no", "Samo od 18 do 39 godina")],
  },
  {  # 3 Avenue
    "tag": "#3 Najbolji jeftini hostel", "short": "Najjeftiniji krevet",
    "area": "VI. okrug, Oktogon",
    "checkin": "Prijava od 14:00 do ponoći, odjava do 11:00", "rules": "Od 6 do 49 godina, bez policijskog sata",
    "specs": ["Besplatan doručak", "Zavjese na krevetima", "Tramvaj 0-24", "Oktogon"],
    "best_for": "Putnicima s malim budžetom koji traže najjeftiniji krevet u centru s besplatnim doručkom i jeftinom večerom.",
    "skip_if": "imate lagan san ili želite društvenu, osobnu atmosferu.",
    "trust": "Besplatan doručak",
    "transit": "Oktogon (M1 i tramvaji 4, 6 koji voze 0-24) ispred vrata",
    "watch": "Bučno tramvajsko čvorište; ponesite čepiće za uši", "noise": "Bučno (tramvajsko čvorište)",
    "pros": [
      ("Najbolji omjer cijene i kvalitete", "Izvan sezone kreveti su bili već od 8 € po noći, s besplatnim doručkom i sniženom večerom."),
      ("Štedite novac", "Hrana je u Mađarskoj skupa, a s besplatnim i sniženim obrocima puno uštedite."),
      ("Osoblje", "Uslužno, brzo i dostupno 0-24."),
    ],
    "cons": [
      ("Kvaliteta boravka", "Spavaonica s 10 kreveta u kojoj sam spavao bila je osrednja po udobnosti, privatnosti i čistoći."),
      ("Nema besplatnog lokota", "Uz ormariće ne dobivate lokot, ali ga možete kupiti za oko 3 €."),
      ("Bezličan", "Nema društvene atmosfere, osobne pažnje ni aktivnosti, osim u blagovaonici."),
      ("Bučan", "Nalazi se uz veliko raskrižje s tramvajima. Ponesite čepiće za uši."),
    ],
    "summary": [
      "<strong>Avenue Hostel je prvi izbor za putnike s malim budžetom koji u Budimpešti žele uštedjeti na smještaju i hrani.</strong>",
      "Kreveti počinju <strong>od oko 8 €</strong>, uz <strong>besplatan doručak</strong> i sniženu večeru (tijekom mog boravka uz malu minimalnu potrošnju u baru). Uz visoke cijene hrane u Mađarskoj, to puno znači.",
      "Nije luksuz, ali je praktično i jeftino, dobar izbor za one koji paze na budžet.",
      "📝 <strong>Napomena urednika:</strong> spavaonica s 10 kreveta \"sa zavjesama\" u kojoj sam spavao i pripadajuće zajedničke kupaonice nisu bile dobre. Ostale sobe hostela s 4, 8 i 12 kreveta su ljepše, samo skuplje, pa hostel zaslužuje bolju ocjenu od one koju bih dao prema svojoj sobi.",
    ],
    "video": "video recenziju hostela Avenue Hostel",
    "groups": [
      ("Sobe, kreveti i kvaliteta sna", "sobe i kreveti", [
        ("Odaberite bolju sobu", "<p>Moja soba s 10 kreveta bila je slaba točka. <strong>Sobe s 4, 8 i 12 kreveta su ljepše</strong> i vrijede tih nekoliko eura više.</p>"),
        ("Čepići za uši su obavezni", "<p>Nalazi se na <strong>čvorištu Oktogon s tramvajima koji voze cijelu noć</strong>. Za one laganog sna bolji su Maverick ili Zen.</p>"),
        ("Lokot za ormarić", "<p>Lokot ne dobivate. <strong>Ponesite svoj</strong> ili ga kupite na recepciji za oko 3 €.</p>"),
      ]),
      ("Atmosfera i društveni život", "zajednički prostori", [
        ("Praktičan, ne osoban", "<p>Ne očekujte aktivnosti ni osobno gostoprimstvo. <strong>Ljudi se upoznaju u blagovaonici.</strong></p>"),
        ("Za koga je", "<p>Za studente i backpackere na dugom putovanju koji paze na svaki euro i hostel koriste uglavnom za spavanje i jelo.</p>"),
      ]),
      ("Hrana, sadržaji i lokacija", "sadržaji", [
        ("Besplatan doručak, jeftina večera", "<p><strong>Besplatan doručak</strong> i snižena večera glavni su mamac. Svaki dan uštedite više nego što košta krevet.</p>"),
        ("Osoblje i prijevoz 0-24", "<p>Recepcija radi 0-24, a <strong>M1 i tramvaji 4, 6 koji voze 0-24</strong> staju ispred ulaza.</p>"),
      ]),
    ],
    "chips": [("yes", "Besplatan doručak"), ("yes", "Zavjese na krevetima"), ("yes", "Recepcija 24 h"), ("yes", "Kuhinja za goste"), ("no", "Ponesite lokot")],
  },
  {  # 4 Flow
    "tag": "#4 Najbolji za digitalne nomade", "short": "Najbolji za digitalne nomade",
    "area": "IX. okrug, Velika tržnica",
    "checkin": "Prijava od 15:00 do ponoći, odjava do 11:00", "rules": "Bez policijskog sata",
    "specs": ["Coworking prostor", "Besplatan lokot", "Kapsule", "Velika tržnica"],
    "best_for": "Digitalnim nomadima i putnicima koji žele salon pogodan za rad na laptopu, kapsule i društvenu, ali opuštenu atmosferu.",
    "skip_if": "imate tešku prtljagu (3. kat, bez dizala) ili želite vlastitu kupaonicu.",
    "trust": "Coworking prostor",
    "transit": "Fővám tér (M4, tramvaji 2, 47, 49) i Kálvin tér (M3, M4)",
    "watch": "Mješovite zajedničke kupaonice; 3. kat, bez dizala", "noise": "Opušteno",
    "pros": [
      ("Osoblje", "Recepcija je dostupna 0-24, osoblje je ljubazno i uslužno."),
      ("Prijateljski", "Društvena atmosfera, lako je upoznati druge putnike."),
      ("Odlični kreveti", "Zavjesa, utičnica, lampica, mala polica i kutija za spremanje uz krevet."),
      ("Sigurno spremište", "Lokot dobivate besplatno."),
      ("Kutak za rad", "Salon s kutkom za rad pogodnim za laptop."),
    ],
    "cons": [
      ("Kupaonice", "Kupaonice su mješovite i zajedničke, s malo privatnosti."),
      ("Nema dizala", "Hostel je na 3. katu."),
      ("Higijena", "Na plahti sam imao kose iako je bila oprana. Sveukupno je hostel higijenski."),
      ("Puni hladnjaci", "Dio hrane koju sam kupio nestao je."),
      ("Tijesne sobe", "Jedva je bilo mjesta za kretanje."),
    ],
    "summary": [
      "<strong>Flow Spaces spaja društveni život hostela s mirom hotela</strong>, idealno ako tražite zlatnu sredinu.",
      "Atmosfera podsjeća na studentski dom, dobar izbor za putnike s malim budžetom koji žele uravnoteženo iskustvo. Kreveti počinju <strong>od oko 10 €</strong>.",
      "Uz prijateljsku atmosferu, <strong>miran radni prostor</strong> i dobro opremljenu kuhinju, vrijedi ga razmotriti.",
    ],
    "groups": [
      ("Sobe, kreveti i kvaliteta sna", "sobe i kreveti", [
        ("Dobro opremljene kapsule", "<p>Svaki krevet ima <strong>zavjesu, utičnicu, lampicu, malu policu i kutiju za spremanje</strong>, uz besplatan lokot.</p>"),
        ("Tijesne sobe", "<p>Sobe su <strong>tijesne</strong>, jedva ima mjesta kad se svi pakiraju.</p>"),
      ]),
      ("Atmosfera i radni prostor", "zajednički prostori", [
        ("Salon za laptop", "<p>U salonu je <strong>pravi kutak za rad</strong>, a hostel nudi i coworking prostor: ovdje se najbolje radi na daljinu.</p>"),
        ("Društven, ali uravnotežen", "<p>Lako je upoznati ljude, bez noći kao u party hostelu. Više studentski dom nego središte obilazaka barova.</p>"),
      ]),
      ("Sadržaji, kupaonice i lokacija", "sadržaji", [
        ("Kupaonice i stepenice", "<p>Kupaonice su <strong>mješovite i zajedničke</strong>, a hostel je na <strong>3. katu bez dizala</strong>.</p>"),
        ("Kuhinja i hladnjaci", "<p>Kuhinja je dobro opremljena, ali se hladnjaci napune i <strong>dio moje hrane je nestao</strong>. Sve označite.</p>"),
        ("Pokraj Velike tržnice", "<p><strong>Velika tržnica je jedan blok dalje</strong>, a Dunav nekoliko minuta pješice.</p>"),
      ]),
    ],
    "chips": [("yes", "Coworking prostor"), ("yes", "Besplatan lokot"), ("yes", "Zavjese na krevetima"), ("yes", "Recepcija 24 h"), ("no", "Bez dizala (3. kat)")],
  },
  {  # 5 a&o
    "tag": "#5 Najbolji hostel hotelskog tipa", "short": "Najbolji za hotelsku udobnost",
    "area": "VII. okrug, blizu Oktogona",
    "checkin": "Prijava i odjava na recepciji 0-24", "rules": "Primaju i obitelji i grupe",
    "specs": ["Mirne sobe", "Odličan tuš", "Kutak za rad", "Privatne sobe"],
    "best_for": "Parovima, obiteljima i svima koji umjesto društvenog života žele mirnu, jednostavnu i čistu sobu.",
    "skip_if": "tražite društven hostel ili ne želite posebno plaćati posteljinu.",
    "trust": "Privatne sobe",
    "transit": "Oktogon (M1, tramvaji 4, 6) i Vörösmarty utca (M1), nekoliko minuta pješice",
    "watch": "Posteljina oko 3 € dodatno; ponesite lokot", "noise": "Mirno",
    "pros": [
      ("Izvrsne sobe", "Jednostavna, mirna i čista soba s fantastičnim tušem."),
      ("Sigurno spremište", "Na recepciji su mi rado zaključali laptop."),
      ("Kutak za rad", "U salonu je izvrstan kutak za rad pogodan za laptop."),
    ],
    "cons": [
      ("Posteljina i ručnik", "Nisu uključeni, naplaćuju se 1150 Ft (oko 3 €) dodatno."),
      ("\"Kavez\" za spremanje", "Uz spremište u sobi NE dobivate lokot."),
      ("Prljav jastuk", "Jastuk su mi mogli zamijeniti, ali sveukupno je hostel higijenski."),
      ("Dosadan doručak", "Prosječan hotelski doručak za oko 8 € (neobavezno)."),
    ],
    "summary": [
      "<strong>a&amp;o Budapest City je za putnike s malim budžetom kojima su udobnost i mir važniji od živog društvenog života.</strong>",
      "Kreveti počinju <strong>od oko 12 €</strong>, ali računajte na doplatu za posteljinu (oko 3 €).",
      "Unatoč sitnim manama poput jastuka i naknade za posteljinu, zbog cijene i udobnosti dobar je izbor ako tražite mirno mjesto s radnim prostorom.",
    ],
    "groups": [
      ("Sobe, kreveti i kvaliteta sna", "sobe i kreveti", [
        ("Mirno, čisto, jednostavno", "<p><strong>Jednostavna, mirna i čista soba</strong> s izvrsnim tušem. Bliže jeftinom hotelu nego hostelu.</p>"),
        ("Uračunajte dodatke", "<p><strong>Posteljina košta oko 3 €</strong>, a za spremište vam treba vlastiti lokot. Uračunajte to u cijenu.</p>"),
      ]),
      ("Atmosfera i radni prostor", "zajednički prostori", [
        ("Mirna baza, bez zabava", "<p>Malo hostelskih aktivnosti. Za one koji žele <strong>privatnost i san</strong>, za parove i obitelji.</p>"),
        ("Salon za laptop", "<p>U salonu je <strong>izvrstan kutak za rad pogodan za laptop</strong>.</p>"),
      ]),
      ("Sadržaji i lokacija", "sadržaji", [
        ("Sigurno spremište", "<p>Recepcija je <strong>sigurno zaključala moj laptop</strong> dok me nije bilo.</p>"),
        ("Doručak", "<p><strong>Neobavezan hotelski doručak za oko 8 €</strong>. U redu, ništa posebno.</p>"),
        ("Lokacija", "<p>U ulici Csengery, nekoliko minuta pješice od <strong>Oktogona i avenije Andrássy</strong>.</p>"),
      ]),
    ],
    "chips": [("yes", "Mirne sobe"), ("yes", "Privatne sobe"), ("yes", "Kutak za rad"), ("no", "Posteljina dodatno (oko 3 €)"), ("no", "Ponesite lokot")],
  },
  {  # 6 Wombat's
    "tag": "#6 Najbolji opušteni party hostel", "short": "Najbolji za opuštenu zabavu",
    "area": "VI. okrug, ulica Király",
    "checkin": "Prijava od 14:00 do 23:00, odjava do 10:00", "rules": "Bez policijskog sata",
    "specs": ["Spavaonice s kupaonicom", "Zavjese na krevetima", "Bar u hostelu", "Ulica Király"],
    "best_for": "Backpackerima koji žele društven bar i noćni život pred vratima, ali i dobro se naspavati.",
    "skip_if": "tražite najjeftiniji krevet ili hostel s pravim karakterom.",
    "trust": "Spavaonice s kupaonicom",
    "transit": "Deák Ferenc tér (M1, M2, M3 i autobus za zračnu luku 100E), 3 minute pješice",
    "watch": "Skup za ono što nudi", "noise": "Unutra mirno",
    "pros": [
      ("Prijateljski", "Opuštena društvena atmosfera, lako je upoznati ljude."),
      ("Nije bučan", "Za party hostel je miran. Možete se dobro odmoriti."),
      ("Osoblje", "Recepcija 0-24 i sigurna garderoba za prtljagu."),
    ],
    "cons": [
      ("Cijena", "Cijene bi mogle biti niže. Nisam imao osjećaj da hostel nudi nešto posebno što bi ih opravdalo."),
    ],
    "summary": [
      "<strong>Wombat's City Hostel je središte mladih putnika koji su došli zbog budimpeštanskog noćnog života</strong>, s mladenačkom energijom i opuštenom atmosferom, idealan opušteni party hostel.",
      "Skuplji od većine hostela u Budimpešti. Lokacija je velika prednost, ali neke stvari su prosječne: kupaonice su, na primjer, čiste, ali ništa više.",
      "Najbolji su bili gosti: upoznavanje i zabava sa zanimljivim putnicima iz cijelog svijeta više su nego nadoknadili sitnice.",
    ],
    "groups": [
      ("Sobe, kreveti i kvaliteta sna", "sobe i kreveti", [
        ("Sobe s kupaonicom", "<p>Prema hostelu, svaka soba ima <strong>vlastitu kupaonicu i klimu</strong>, a kreveti u spavaonicama imaju zavjese.</p>"),
        ("Bolje za spavanje nego za zabavu", "<p>Za party hostel je <strong>noću mirno</strong>. Dobro sam spavao.</p>"),
      ]),
      ("Atmosfera i društveni život", "zajednički prostori", [
        ("Opuštena party publika", "<p>Lako je upoznati ljude u <strong>baru hostela</strong>, a barovi u Gozsdu udvaru su nekoliko koraka dalje.</p>"),
        ("Gosti čine razliku", "<p>Međunarodno društvo bilo je <strong>najbolji dio mog boravka</strong>.</p>"),
      ]),
      ("Sadržaji i lokacija", "sadržaji", [
        ("Prosječno, ali čisto", "<p>Sadržaji su <strong>čisti, ali prosječni</strong>; ne rezervirajte zbog dizajna.</p>"),
        ("Središnje u ulici Király", "<p>Nekoliko minuta od <strong>Deák Ferenc tér</strong>, autobusa 100E za zračnu luku i noćnog života židovske četvrti.</p>"),
      ]),
    ],
    "chips": [("yes", "Spavaonice s kupaonicom"), ("yes", "Klima"), ("yes", "Bar u hostelu"), ("yes", "Recepcija 24 h"), ("yes", "Besplatni ormarići")],
  },
  {  # 7 Zen
    "tag": "#7 Najbolji miran, ugodan hostel", "short": "Najbolji za mir i ugođaj",
    "area": "IX. okrug, Velika tržnica",
    "checkin": "Prijava od 14:00 do 21:00, odjava do 11:00", "rules": "Ograničeno radno vrijeme recepcije",
    "specs": ["Domaća atmosfera", "Mali hostel", "Besplatan čaj i kava", "Velika tržnica"],
    "best_for": "Introvertima i sporim putnicima koji traže malo, ugodno, domaće mjesto uz Dunav.",
    "skip_if": "stižete kasno, trebate ormarić ili tražite stol s utičnicom.",
    "trust": "Prijava do 21:00",
    "transit": "Fővám tér (M4, tramvaji 2, 47, 49), pokraj Velike tržnice",
    "watch": "Nema kasne prijave; nema spremišta koje se zaključava", "noise": "Mirno",
    "pros": [
      ("Osoblje", "Tijekom mog boravka jedan je domaćin vodio cijeli hostel: ljubazan, uslužan i veseo. Njemu dugujem ocjenu 9/10."),
      ("Prijateljski", "Razgovor ste mogli započeti bilo gdje. Kauč u dnevnom boravku bio je odlično mjesto za čavrljanje."),
      ("Kao kod kuće", "Ako volite ugodan, domaći osjećaj, ovo je raj."),
    ],
    "cons": [
      ("Nema prijave 0-24", "Domaćin je odlazio u 21 sat, a prijava je dugo trajala."),
      ("Premalo osoblja", "Jedna osoba žonglirala je s previše zadataka; trebao je barem još jedan kolega."),
      ("Nije sigurno", "Nije bilo spremišta koje se zaključava."),
      ("Nije za nomade", "Nema kutka za rad s utičnicama."),
    ],
    "summary": [
      "<strong>Central Market Hall Zen Hostel je drago utočište ako tražite malo, ugodno mjesto koje je više dom nego hostel.</strong>",
      "Cijene su malo iznad prosjeka za ono što dobivate, kreveti u spavaonici počinju <strong>od oko 11 €</strong>. Nije najbolji omjer cijene i kvalitete, ali ako su vam važni domaći ugođaj i lokacija uz Veliku tržnicu, isplati se.",
    ],
    "groups": [
      ("Sobe i kvaliteta sna", "sobe i kreveti", [
        ("Mali i miran", "<p><strong>Mali hostel s mirnom, domaćom atmosferom</strong>, bez party publike.</p>"),
        ("Nema spremišta koje se zaključava", "<p>Tijekom mog boravka <strong>nije bilo spremišta koje se zaključava</strong>. Vrijedne stvari držite uz sebe ili odaberite drugi hostel ako vam je to važno.</p>"),
      ]),
      ("Atmosfera i dnevni boravak", "zajednički prostori", [
        ("Razgovori u dnevnom boravku", "<p>Svi završe na <strong>kauču u dnevnom boravku</strong> u razgovoru. Društvene igre, čaj i kava cijeli dan.</p>"),
        ("Nije za rad na daljinu", "<p>Nema stola s utičnicom. <strong>Za digitalne nomade bolji su Flow Spaces ili Maverick.</strong></p>"),
      ]),
      ("Prijava i lokacija", "sadržaji", [
        ("Stignite prije 21:00", "<p>Prijava je <strong>od 14:00 do 21:00</strong>, a recepcija ima ograničeno radno vrijeme. Stižete kasnim letom? Rezervirajte drugdje.</p>"),
        ("Pokraj Velike tržnice", "<p>Na Vámház körútu, <strong>pokraj Velike tržnice i Mosta slobode</strong>, s M4 i tramvajem 2 na Fővám téru.</p>"),
      ]),
    ],
    "chips": [("yes", "Domaća atmosfera"), ("yes", "Besplatan čaj i kava"), ("yes", "Pokraj Velike tržnice"), ("no", "Prijava do 21:00"), ("no", "Nema spremišta s ključem")],
  },
  {  # 8 Adagio
    "tag": "#8 Najbolja lokacija za razgledavanje", "short": "Najbolji za razgledavanje",
    "area": "VI. okrug, avenija Andrássy",
    "checkin": "Prijava od 15:00 do ponoći, odjava do 10:00", "rules": "Bez policijskog sata",
    "specs": ["Pogled na baziliku", "Vlastite kupaonice", "Besplatan čaj i kava", "Avenija Andrássy"],
    "best_for": "Ljubiteljima razgledavanja koji žele miran, čist krevet na početku avenije Andrássy, nekoliko koraka od bazilike svetog Stjepana.",
    "skip_if": "tražite društven hostel ili vam smeta buka prometa.",
    "trust": "Nekoliko koraka od bazilike",
    "transit": "Bajcsy-Zsilinszky út (M1) ispred vrata, Deák Ferenc tér (M1, M2, M3) kratka šetnja",
    "watch": "Buka prometa; bez dizala (1. kat)", "noise": "Buka prometa",
    "pros": [
      ("Odlična kupaonica", "Izvrsna, čista vlastita kupaonica."),
      ("Izvrsna lokacija", "S pogledom na baziliku svetog Stjepana."),
      ("Mirno", "Nije tako užurbano kao neki drugi hosteli, pa ima više privatnosti."),
    ],
    "cons": [
      ("Bučno", "U mojoj sobi bilo je jako bučno zbog prometa."),
      ("Nema dizala", "Hostel je na prvom katu."),
      ("Bezličan", "Nema društvene atmosfere ni osobne pažnje."),
    ],
    "summary": [
      "<strong>Adagio 2.0 je vaše mjesto ako vam je najvažnije dobro se naspavati u čistoj, udobnoj sobi.</strong>",
      "Ništa posebno, ali osnove radi dobro: dobar izbor za jeftin, minimalistički smještaj na fantastičnoj lokaciji.",
      "Ni novčanik neće stradati: za bliske datume kreveti u spavaonici počinju <strong>od oko 11 €</strong>, a privatne sobe <strong>od oko 22 €</strong>.",
    ],
    "groups": [
      ("Sobe i kvaliteta sna", "sobe i kreveti", [
        ("Čiste sobe, odlična kupaonica", "<p>Uz moju sobu išla je <strong>izvrsna, čista vlastita kupaonica</strong>. Ima spavaonica i dvokrevetnih soba s kupaonicom.</p>"),
        ("Buka prometa", "<p>Avenija Andrássy je glavna prometnica i <strong>moja soba bila je bučna zbog prometa</strong>. Ponesite čepiće ili tražite sobu prema dvorištu.</p>"),
      ]),
      ("Atmosfera", "zajednički prostori", [
        ("Mirno, ne društveno", "<p><strong>Nema društvenog života ni osobne pažnje.</strong> Mirna baza za razgledavanje, ne za upoznavanje ljudi.</p>"),
      ]),
      ("Sadržaji i lokacija", "sadržaji", [
        ("Kuhinja, čaj i kava", "<p>Prema hostelu, gosti mogu koristiti <strong>potpuno opremljene kuhinje</strong>, a čaj, kava i posteljina su besplatni.</p>"),
        ("Prvi kat, bez dizala", "<p>Na <strong>prvom katu palače, bez dizala</strong>, jedan niz stepenica.</p>"),
        ("Nepobjedivo za znamenitosti", "<p>Na <strong>početku avenije Andrássy</strong>, nekoliko minuta pješice od bazilike svetog Stjepana, Opere i Deák Ferenc téra.</p>"),
      ]),
    ],
    "chips": [("yes", "Pogled na baziliku"), ("yes", "Kuhinja za goste"), ("yes", "Recepcija 24 h"), ("yes", "Besplatan čaj i kava"), ("no", "Bez dizala (1. kat)")],
  },
  {  # 9 Das Nest
    "tag": "#9 Najbolji mali, ugodan hostel", "short": "Najbolji mali i ugodan",
    "area": "VII. okrug, židovska četvrt",
    "checkin": "Prijava od 12:00 do 23:00, odjava do 11:00", "rules": "Bez policijskog sata",
    "specs": ["Ugodan potkrovni stan", "Lokalni savjeti", "Kuhinja za goste", "Židovska četvrt"],
    "best_for": "Solo backpackerima i malim grupama koji traže ugodan hostel nalik stanu, s ljubaznim domaćinima u party četvrti.",
    "skip_if": "želite plaćati karticom, trebate pristupačan ulaz ili želite mir i vikendom.",
    "trust": "Privatne sobe od 17 €",
    "transit": "Wesselényi utca (tramvaji 4, 6) i Blaha Lujza tér (M2), nekoliko minuta pješice",
    "watch": "Tijekom mog boravka samo gotovina; buka s ulice vikendom", "noise": "Buka s ulice vikendom",
    "pros": [
      ("Središnja lokacija", "U srcu Budimpešte, blizu glavnih znamenitosti i noćnog života."),
      ("Ljubazno osoblje", "Drago, uslužno, s odličnim lokalnim preporukama."),
      ("Ugodna atmosfera", "Ugodno, intimno mjesto, idealno za upoznavanje ljudi."),
      ("Dobro opremljena kuhinja", "Potpuno opremljena kuhinja za goste."),
      ("Lokalne veze", "Savjeti za barove, restorane i festivale koje sami ne biste pronašli."),
    ],
    "cons": [
      ("Samo gotovina", "Tijekom mog boravka nisu primali kartice, samo gotovinu."),
      ("Moguća buka", "Zbog živog noćnog života noću može biti bučno."),
      ("Ograničena pristupačnost", "Nije pristupačan svim osobama s invaliditetom."),
    ],
    "summary": [
      "<strong>Das Nest je idealan ako tražite središnji smještaj u Budimpešti s ugodnom, društvenom atmosferom.</strong> Sve se vrti oko ljubazne usluge, opuštene atmosfere i odličnih lokalnih savjeta.",
      "Tijekom mog boravka nedostajale su pogodnosti poput plaćanja karticom, ali to nadoknađuje osobnom pažnjom i odličnom lokacijom. Za one kojima su pristupačna udobnost i upoznavanje ljudi važniji od luksuza.",
      "Sobe: mješovite ili samo ženske spavaonice s 4 ili 6 kreveta i jedna dvokrevetna privatna soba. Krevet u spavaonici <strong>od oko 15 €</strong>.",
    ],
    "groups": [
      ("Sobe i kvaliteta sna", "sobe i kreveti", [
        ("Male spavaonice", "<p><strong>Mješovite ili samo ženske spavaonice s 4 i 6 kreveta</strong> i jedna dvokrevetna privatna soba. Dovoljno malo da bude osobno.</p>"),
        ("Buka vikendom", "<p>Nalazi se u party četvrti, pa bi <strong>oni laganog sna za petak i subotu trebali ponijeti čepiće</strong>.</p>"),
      ]),
      ("Atmosfera i društveni život", "zajednički prostori", [
        ("Kao stan prijatelja", "<p>Hostel sebe opisuje kao <strong>obnovljeni potkrovni stan</strong>, i upravo je takav: intiman i društven.</p>"),
        ("Domaćini s lokalnim savjetima", "<p>Od osoblja sam dobio <strong>savjete za barove, restorane i festivale</strong> kojih nije bilo ni u jednom vodiču.</p>"),
      ]),
      ("Sadržaji i plaćanje", "sadržaji", [
        ("Kuhinja", "<p><strong>Potpuno opremljena kuhinja za goste</strong>, dobra za uštedu.</p>"),
        ("Ponesite gotovinu", "<p>Tijekom mog boravka primali su <strong>samo gotovinu</strong>. Provjerite uvjete rezervacije i za svaki slučaj ponesite forinte.</p>"),
      ]),
    ],
    "chips": [("yes", "Ugodna atmosfera"), ("yes", "Kuhinja za goste"), ("yes", "Besplatni ormarići"), ("yes", "Ženske spavaonice"), ("no", "Samo gotovina (tijekom mog boravka)")],
  },
  {  # 10 The Hive
    "tag": "#10 Najbolji veliki party hostel", "short": "Najveći party hostel",
    "area": "VII. okrug, židovska četvrt",
    "checkin": "Prijava od 15:00 do ponoći, odjava do 11:00", "rules": "Strogo 18+, bez policijskog sata",
    "specs": ["Krovni bar", "Dnevni obilasci barova", "Samo 18+", "Židovska četvrt"],
    "best_for": "Grupama starijima od 18 i solo partijanerima koji žele velik, bučan party hostel s krovnim barom u četvrti ruin barova.",
    "skip_if": "imate lagan san, rano ustajete ili želite zavjese na krevetima.",
    "trust": "Strogo 18+",
    "transit": "Astoria (M2) i Deák Ferenc tér (M1, M2, M3), nekoliko minuta pješice",
    "watch": "Buka iz kluba ispod; nema zavjesa na krevetima", "noise": "Bučno (party hostel)",
    "why": [
      ("Velik party hostel", "Prema hostelu, više od 300 kreveta od 2015., s dnevnim obilascima barova, bingo obilascima, SPArtyjima i party brodovima."),
      ("Krovni bar", "Vlastiti krovni bar za goste, s dnevnim happy hourom od 16 do 19 sati."),
      ("Lokacija", "U četvrti ruin barova, kratka šetnja do Gozsdu udvara i Szimpla Kerta."),
      ("Praktično", "Recepcija 0-24, ormarići, plaćanje gotovinom ili karticom."),
    ],
    "skip": [
      ("Buka", "Sam hostel upozorava one laganog sna i rane ustajače; gosti spominju buku iz kluba ispod."),
      ("Nema zavjesa na krevetima", "Česta želja gostiju su zavjese na krevetima."),
      ("Wi-Fi", "Slab wifi je česta pritužba gostiju."),
      ("Dobna granica", "Strogo od 18 godina."),
    ],
    "summary": [
      "<strong>The Hive je veliki, bučni party hostel Budimpešte.</strong> S više od 300 kreveta, krovnim barom i dnevnim obilascima barova, stvoren je za noći, ne za rana jutra.",
      "Uvrstio sam ga kao party alternativu Onefamu: ovdje navedene činjenice potječu iz informacija samog hostela i recenzija gostiju, provjereno 14. studenoga 2026. Kreveti u spavaonici počinju <strong>od oko 13 €</strong>.",
    ],
    "chips": [("yes", "Krovni bar"), ("yes", "Dnevni obilasci barova"), ("yes", "Recepcija 24 h"), ("yes", "Besplatni ormarići"), ("no", "Strogo 18+")],
  },
]

HOSTELS = build(_T, floor_label="1. kat")


def _areas(H, a):
    return (
        '<h3>VII. okrug (židovska četvrt): zbog noćnog života</h3>\n'
        '<p>Ovdje su ruin barovi, Gozsdu udvar i Szimpla Kert, a ovdje su i %s, %s i %s. Odlično za zabavu, <strong>za one laganog sna vikendom najgore</strong>.</p>\n'
        '<h3>VI. okrug (ulica Király, avenija Andrássy, Oktogon): središnje i dobro povezano</h3>\n'
        '<p>%s, %s i %s su na glavnim pravcima, uz M1 i tramvaje 4, 6 koji voze 0-24. Svugdje stižete pješice, ali <strong>promet na glavnim ulicama</strong> može biti bučan.</p>\n'
        '<h3>IX. okrug (Velika tržnica): mirnije, uz rijeku</h3>\n'
        '<p>%s, %s i %s su pokraj Velike tržnice, nekoliko minuta od Dunava. Ovo bih odabrao ako želite <strong>mirnije noći</strong>, a da i dalje pješice stignete do centra.</p>\n'
        '<p>Stižete avionom? Ovdje pročitajte <a href="/hr/zracna-luka-budimpesta-centar">kako doći od zračne luke do centra</a>: autobus 100E staje na Deák Ferenc téru, kratka šetnja do hostela u VI. i VII. okrugu.</p>'
    ) % (a(H[2]), a(H[9]), a(H[10]), a(H[6]), a(H[8]), a(H[3]), a(H[1]), a(H[4]), a(H[7]))


UI = {
    "url": URL, "home": "Početna", "home_url": "https://www.budapestadventures.com/hr", "about_url": "https://www.budapestadventures.com/hr/about",
    "title": "10 najboljih hostela u Budimpešti u 2026. (spavao sam u 9)",
    "h1_main": "10 najboljih hostela u Budimpešti u 2026.", "h1_muted": "(spavao sam u 9)",
    "meta": "Spavao sam u 9 najboljih hostela u Budimpešti, 30 noći u Mavericku. Kreveti od 8 €: najbolji party, mirni, jeftini i nomadski hosteli po četvrtima.",
    "breadcrumb": "Najbolji hosteli u Budimpešti", "kicker_badge": "Usporedba hostela 2026.",
    "author_line": 'Autor: <a href="/hr/about" target="_blank">Adam Dimitrov</a>, osnivač i tester u Budimpešti',
    "author_role": "Spavao sam u 9 od 10 • Vlastite fotografije i video recenzije",
    "last_updated": "<strong>Ažurirano</strong>: 14. studenoga 2026.",
    "job_title": "Osnivač i tester u Budimpešti",
    "intro": (
        '<p>Loš hostel u Budimpešti ne košta vas novca, nego sna. Kreveti u spavaonicama u centru koštaju <strong>od 8 do 15 €</strong> po noći, '
        'ali party hostel u židovskoj četvrti i miran hostel s kapsulama uz Veliku tržnicu dva su potpuno različita putovanja.</p>\n'
        '<p>U <strong>9 od 10 hostela ispod sam osobno spavao</strong>, u Mavericku na primjer <strong>30 noći za 280 €</strong>, i usporedio sam ih jedan uz drugi po onome '
        'što je važno pri rezervaciji: buka noću, privatnost u krevetu, kupaonice, kuhinja, dobna granica, publika i stvarna cijena po noći. '
        'The Hive je jedina party opcija u kojoj nisam spavao, zato za nju navodim samo provjerene činjenice, bez oznake \"testirano\".</p>\n'
        '<p>Cijene i ocjene provjerene <strong>%s</strong> Filtri vas odmah vode do party, mirnih, jeftinih, nomadskih hostela ili onih s privatnim sobama.</p>\n' % CHECKED),
    "filters": [("party", "🎉 Društveno i zabava"), ("quiet", "😴 Miran san"), ("budget", "💶 Ispod 11 €"),
                ("private", "🛏️ Privatne sobe"), ("nomad", "💻 Digitalni nomadi"), ("kitchen", "🍳 Kuhinja za goste")],
    "district_fmt": "%s. okrug", "decimal": ",", "thousands": ".", "k": "k",
    "tested_chip": "✓ Osobno testirano",
    "best_for_card": "Najbolje za:", "best_for_summary": "Najbolje za:", "skip_if": "Preskočite ako",
    "from_eur": "od %d €", "eur": "%d €", "card_psub": "Krevet/noć • 14. 11. 2026.",
    "card_btn": "Cijene i datumi →", "read_review": "Recenzija ↓",
    "pros": "Prednosti:", "cons": "Nedostaci:", "why": "Zašto ga odabrati:", "why_skip": "Zašto ne:",
    "video": "Video:", "watch_my": "Pogledajte moju",
    "summary_title": "Zaključak i ocjena", "summary_pill": "Pregled",
    "swipe_photos": "%d fotografija, povucite →", "one_photo": "1 fotografija", "no_photo": "Osobno iskustvo",
    "photo_alt": "%s: %s, vlastita fotografija", "prev_photo": "Prethodna fotografija", "next_photo": "Sljedeća fotografija",
    "buy_badge": "Cijene i dostupnost uživo", "buy_sub": "Krevet u spavaonici po noći • Provjereno: " + CHECKED,
    "address_perk": "Adresa: <strong>%s</strong>", "privates_perk": "Privatna soba <strong>od %d €</strong>",
    "buy_cta": "Datumi i cijene", "buy_trust": "Cijena ovisi o datumu; konačnu cijenu vidite prije plaćanja",
    "qf": {"title": "Brze činjenice: %s", "address": "Adresa", "dorm": "Krevet u spavaonici", "transit": "Prijevoz", "checkin": "Prijava",
           "rules": "Kućni red", "ratings": "Ocjene", "watch": "Na što paziti",
           "dorm_fmt": "od %d € po noći (provjereno: " + CHECKED + ")", "priv_fmt": ", privatna soba od %d €",
           "hw_fmt": "Hostelworld %s/10 (%s recenzija)", "bk_fmt": ", Booking.com %s/10 (%s recenzija)"},
    "breakdown_h2": "Detaljne recenzije: 10 najboljih hostela u Budimpešti",
    "breakdown_sub": "Spavao sam u 9, 1 party opcija prema provjerenim činjenicama • Kliknite za otvaranje ili zatvaranje",
    "picks": [
        ("Ukupno", 1, "Društven bez buke od zabava, kreveti sa zavjesom, odlične kupaonice i 280 € za mojih 30 noći."),
        ("Solo putnici (18 do 39 godina)", 2, "Uz besplatne dnevne aktivnosti i obilaske barova prijatelje ćete naći za tren. Imate više od 39? Odaberite Maverick ili Wombat's."),
        ("Zabava", 10, lambda H: 'Veliki, bučni izbor s krovnim barom u četvrti ruin barova. Radije opuštenije? <a href="#%s">%s</a>.' % (H[6]['id'], H[6]['name'])),
        ("Najjeftiniji krevet", 3, "Krevet od oko 8 € s besplatnim doručkom. Ponesite čepiće: nalazi se uz tramvajsko čvorište."),
        ("Miran san", 1, lambda H: 'Mirna sporedna ulica u IX. okrugu. Također mirni: <a href="#%s">%s</a> i <a href="#%s">%s</a>.' % (H[7]['id'], H[7]['name'], H[5]['id'], H[5]['name'])),
        ("Digitalni nomadi", 4, "Salon za rad na laptopu i coworking prostor. Za duži boravak alternativa je Maverick."),
        ("Parovi i obitelji", 5, "Jednostavne, mirne, čiste sobe s privatnom opcijom. Računajte oko 3 € za posteljinu."),
        ("Razgledavanje", 8, "Na početku avenije Andrássy, nekoliko minuta od bazilike svetog Stjepana i Deák téra."),
        ("Malo i ugodno", 9, "Kao potkrovni stan prijatelja u židovskoj četvrti, s domaćinima punim lokalnih savjeta."),
    ],
    "sections": {
        "picks_badge": "Brzi izbor", "picks_h2": "Najbolji hostel u Budimpešti prema vrsti putnika",
        "picks_sub": "Kratak odgovor za svaku vrstu putovanja, prema mojim boravcima",
        "table_badge": "Jedan uz drugi", "table_h2": "Hosteli u Budimpešti u usporedbi: cijena, buka i zamke",
        "table_sub": "Cijene spavaonica i Hostelworld ocjene provjerene " + CHECKED + " Buka i zamke iz mojih boravaka (The Hive: recenzije gostiju).",
        "table_cols": ["Hostel", "Najbolji za", "Četvrt", "Krevet u spavaonici", "Hostelworld", "Buka noću", "Na što paziti"],
        "areas_badge": "Četvrti", "areas_h2": "Gdje odsjesti u hostelu u Budimpešti",
        "areas_sub": "Svih 10 je u središtu Pešte. Okrug odlučuje koliko će vaše noći biti bučne.",
        "areas_body": _areas,
        "map_h2": "Karta: najbolji hosteli u Budimpešti",
        "map_sub": 'Hosteli s popisa u središnjim okruzima (<a href="/hr/pjesacke-ture-budimpesta">VII. okrug, židovska četvrt</a>, V. okrug, VI. okrug Terézváros i IX. okrug Ferencváros)',
        "types_h2": "Vrste hostela u Budimpešti",
    },
    "faq": [
        ("Koji je najbolji hostel u Budimpešti?",
         "<p>Ukupno mi je favorit <strong>Maverick Central Market</strong>: društven bez buke od zabava, kreveti sa zavjesom, odlične kupaonice i prava cijena za duži boravak (u ožujku sam za 30 noći platio 280 €). "
         "Za društven boravak pravi izbor je <strong>Onefam Budapest</strong>, a za najjeftiniji krevet <strong>Avenue Hostel</strong>.</p>"),
        ("Koji su najbolji hosteli u Budimpešti za solo putnike?",
         "<p>U <strong>Onefam Budapest</strong> najlakše ćete steći prijatelje zahvaljujući besplatnim dnevnim aktivnostima i obilascima barova, ali prima samo goste <strong>od 18 do 39 godina</strong>. "
         "Imate više od 39 ili želite više spavati? <strong>Maverick Central Market</strong> i <strong>Wombat's City Hostel</strong> su društveni bez obavezne zabave.</p>"),
        ("Koji su najbolji party hosteli u Budimpešti?",
         "<p><strong>Onefam Budapest</strong> (društven, dnevni obilasci barova), <strong>The Hive Party Hostel</strong> (veliki, bučni, s krovnim barom, strogo 18+) i "
         "<strong>Wombat's City Hostel</strong> (opuštena zabava, može se i spavati). Sva tri su kratka šetnja od ruin barova židovske četvrti.</p>"),
        ("U kojem se hostelu u Budimpešti najmirnije spava?",
         "<p>U <strong>Maverick Central Market</strong> (mirna sporedna ulica), <strong>Central Market Hall Zen Hostel</strong> (mali i domaći) i <strong>a&amp;o Budapest City</strong> (sobe hotelskog tipa). "
         "Ako imate lagan san, izbjegavajte Avenue Hostel: nalazi se uz tramvajsko čvorište Oktogon.</p>"),
        ("Koliko košta hostel u Budimpešti?",
         "<p>14. studenoga 2026. kreveti u spavaonicama ovih 10 hostela počinjali su <strong>od oko 8 do 15 €</strong> po noći (Avenue od 8 €, Das Nest od 15 €), a privatne sobe od oko 17 do 28 €. "
         "Skuplje je <strong>vikendom, ljeti (od svibnja do rujna), tijekom Sziget Festivala u kolovozu, božićnih sajmova i za Novu godinu</strong>.</p>"),
        ("U kojoj četvrti rezervirati hostel u Budimpešti?",
         "<p>U <strong>VII. okrugu (židovska četvrt)</strong> zbog noćnog života, u <strong>VI. okrugu</strong> (ulica Király, avenija Andrássy) za središnju, dobro povezanu bazu "
         "i u <strong>IX. okrugu</strong> uz Veliku tržnicu za mirnije noći blizu Dunava.</p>"),
        ("Imaju li hosteli u Budimpešti dobne granice?",
         "<p>Neki imaju. Prema kućnom redu, <strong>Onefam Budapest prima goste od 18 do 39 godina</strong>, <strong>The Hive je strogo 18+</strong>, a <strong>Avenue Hostel prima goste od 6 do 49 godina</strong>. Prije rezervacije provjerite pravila.</p>"),
        ("Jesu li hosteli u Budimpešti sigurni?",
         "<p>Općenito jesu, ali sitne krađe se događaju: u jednom hostelu ukrali su mi majicu s kapuljačom i kutiju flastera za nos. <strong>Vrijedne stvari zaključajte u ormarić</strong> i ponesite lokot, jer ga neki hosteli "
         "(Avenue, a&amp;o) ne daju. Flow Spaces vam ga daje besplatno.</p>"),
        ("Prema kojim ste kriterijima odabrali najbolje hostele u Budimpešti?",
         "<p>Spavao sam u 9 od 10 hostela i ocijenio ih prema: <strong>lokaciji, buci noću, čistoći, udobnosti i privatnosti kreveta, sadržajima, publici i cijeni</strong>. "
         "The Hive je uvršten kao party opcija prema provjerenim činjenicama i recenzijama gostiju, bez oznake testirano.</p>"),
        ("Što ponijeti u hostel?",
         "<p><strong>Obavezno:</strong> čepići za uši i maska za spavanje. <strong>Osnove:</strong> japanke, pidžama, punjač za mobitel, vlažne maramice, dezodorans, četkica i pasta za zube. "
         "<strong>Po želji</strong> (provjerite što hostel daje): ručnik, lokot, šampon i gel za tuširanje.</p>"),
    ],
    "sticky_trust": "Krevet/noć", "sticky_cta": "Cijene →", "sheet_label": "Idi na hostel u Budimpešti",
    "toc_breakdown": "Detaljne recenzije (10 hostela)",
    "szimpla_alt": "Ruin bar Szimpla Kert, kratka šetnja od The Hivea u ulici Dob",
    "szimpla_pill": "Szimpla Kert, 3 min pješice",
    "collapse_label": "Zatvori", "expand_label": "Otvori recenziju",
    "price_range": "Krevet od %d €",
}
