# -*- coding: utf-8 -*-
"""České texty: /cs/nejlepsi-hostely-budapest. Fakta: hostels_data_en.py (14. 11. 2026)."""
from hostels_data_en import CHECKED_ISO
from hostels_i18n import build

CHECKED = "14. listopadu 2026"
URL = "https://www.budapestadventures.com/cs/nejlepsi-hostely-budapest"

_T = [
  {  # 1 Maverick
    "tag": "🏆 #1 Nejlepší hostel celkově", "short": "Celkově nejlepší",
    "area": "IX. obvod, Velká tržnice",
    "checkin": "Check-in od 15:00, check-out do 11:00", "rules": "Bez zavírací hodiny",
    "specs": ["Závěsy u postelí", "Střešní terasa", "Klidná boční ulice", "Výhodné na delší pobyt"],
    "best_for": "Sólo cestovatelům, digitálním nomádům a batůžkářům na delší pobyt, kteří chtějí společenský hostel bez hluku z večírků.",
    "skip_if": "hledáte party hostel hned vedle ruin barů.",
    "trust": "Soukromé pokoje od 28 €",
    "transit": "Kálvin tér (M3, M4) a Fővám tér (M4, tramvaje 2, 47, 49), obojí pár minut pěšky",
    "watch": "Plná kuchyň ve špičce; cennosti zamykejte", "noise": "Klidný",
    "pros": [
      ("Cenově dostupný", "Mimo sezónu jsem měl postel už od 9 € za noc. V březnu jsem za 30 nocí zaplatil 280 €."),
      ("Skvělý na delší pobyt", "Je to jako mít vlastní pokoj na koleji, pohodlné i na měsíc."),
      ("Skvělá poloha", "V klidnějším IX. obvodu, a přesto dost v centru kvůli nočnímu životu a dopravě."),
      ("Skvělé pokoje", "Moderní dormy s velkými skříňkami a závěsy u postelí."),
      ("Skvělé koupelny", "Společné (nebo soukromé) koupelny jsou udržované, čisté a kvalitní."),
      ("Málo hluku", "Hluk z ulice je minimální, protože hostel stojí v menší ulici."),
    ],
    "cons": [
      ("Kuchyň", "Ve špičce je těsná a nádobí by chtělo vyměnit. Rychle se zašpiní, i když se uklízí denně. Lednice byla stále plná a neuspořádaná."),
      ("Krádež", "Ukradli mi mikinu a krabičku nosních náplastí. To se může stát v jakémkoli hostelu, nejen v Mavericku. <strong>Cennosti vždy zamykejte</strong>."),
    ],
    "summary": [
      "<strong>Maverick Central Market je pro ty, kdo chtějí pohodlí, na krátký i delší pobyt.</strong> Je to jako mít vlastní pokoj na koleji, pohodlné i na měsíc.",
      "Není to <a href=\"#section-2-hostel-one\">party hostel</a>, ale <strong>příležitostí k seznámení je tu spousta</strong>.",
      "<strong>Výjimečný poměr cena a výkon</strong>: <strong>v březnu jsem tu strávil 30 nocí za 280 €</strong> (asi 9,33 € za noc). Při mé kontrole 14. listopadu 2026 byly postele na nejbližší termíny <strong>zhruba od 10 €</strong> a i v hlavní sezóně je cena za tuto kvalitu férová.",
    ],
    "video": "videorecenzi Maverick Central Market",
    "groups": [
      ("Pokoje, postele a kvalita spánku", "pokoje a postele", [
        ("Postele v dormech se závěsy", "<p>Dormy jsou <strong>moderní, se závěsy u postelí a velkými skříňkami</strong>, takže i plný pokoj zůstává klidný.</p>"),
        ("Klidné noci", "<p>Stojí v <strong>menší boční ulici IX. obvodu</strong>, daleko od párty ulic VII. obvodu. Během mých 30 nocí byl hluk z ulice minimální.</p>"),
        ("Opravdová cena na dlouhý pobyt", "<p><strong>30 nocí v březnu stálo 280 €.</strong> Jako základnu pro digitálního nomáda nebo pomalé cestování jsem v centru lepší cenu nenašel.</p>"),
      ]),
      ("Atmosféra a společenský život", "společné prostory", [
        ("Společenský, ale ne party hostel", "<p>Jako přátelská vysokoškolská kolej. <strong>Snadno se seznámíte</strong> ve společných prostorách, bez křiku ve čtyři ráno.</p>"),
        ("Koho potkáte", "<p>Sólo cestovatele, hosty na delší pobyt a lidi pracující na dálku. Ideální, pokud chcete večer společnost a pak dobrý spánek.</p>"),
      ]),
      ("Vybavení, kuchyň a koupelny", "vybavení", [
        ("Koupelny", "<p>Společné i soukromé koupelny byly <strong>čisté a kvalitní</strong>, jedna z nejlepších věcí na mém pobytu.</p>"),
        ("Kuchyň ve skutečnosti", "<p>Kuchyň pro hosty je <strong>ve špičce těsná</strong>, nádobí opotřebované a lednice stále plná. Jídlo si označte.</p>"),
        ("Zamykejte si věci", "<p>Ukradli mi mikinu a krabičku nosních náplastí. <strong>Používejte skříňky</strong> na všechno, co by vám chybělo.</p>"),
      ]),
    ],
    "chips": [("yes", "Závěsy u postelí"), ("yes", "Střešní terasa"), ("yes", "Kuchyň pro hosty"), ("yes", "Recepce 24 h"), ("yes", "Úschovna zavazadel zdarma")],
  },
  {  # 2 Onefam
    "tag": "#2 Nejlepší společenský hostel pro sólo cestovatele", "short": "Nejlepší pro sólo cestovatele",
    "area": "VII. obvod, židovská čtvrť",
    "checkin": "Check-in 15:00 až 23:00, check-out do 11:00", "rules": "Jen 18 až 39 let, bez zavírací hodiny",
    "specs": ["Denní aktivity zdarma", "Bar crawly", "18 až 39 let", "Deák tér"],
    "best_for": "Sólo cestovatelům ve věku 18 až 39 let, kteří chtějí okamžitou partu, denní program a večírky.",
    "skip_if": "je vám přes 39, jako pár chcete soukromí nebo chodíte brzy spát.",
    "trust": "18 až 39 let",
    "transit": "Deák Ferenc tér (M1, M2, M3 a letištní autobus 100E), asi 4 minuty pěšky",
    "watch": "Dražší než většina; jen 18 až 39 let", "noise": "Živo do půlnoci",
    "pros": [
      ("Nejlepší party hostel", "Pitné hry na baru, pak ruin bary a přes den památky: budete se skvěle bavit."),
      ("Organizované aktivity", "Onefam pořádá denní i večerní program (bar crawly, pitné hry)."),
      ("Perfektní poloha", "Uprostřed židovské čtvrti, blízko zastávky letištního autobusu 100E, památek i nočního života."),
      ("Skvělé pokoje", "Prostorné pokoje s bezpečným úložným prostorem a skříňkami. Postele nabízejí soukromí a pohodlí."),
      ("Málo hluku", "Hluk je přijatelný, večírek obvykle utichá mezi 23:00 a půlnocí."),
    ],
    "cons": [
      ("U postele není odkládací místo", "Na palandách není kam dát sluchátka, peněženku a telefon."),
      ("Problémy se sprchou", "Teplota vody kolísá a špatně umístěný pohybový senzor zhasíná ve sprše světlo."),
      ("Cena", "Dražší než jiné hostely v Budapešti. Kvůli společnosti a večírkům se příplatek vyplatí."),
    ],
    "summary": [
      "<strong>Onefam Budapest je nejlepší volba, pokud rádi trávíte čas mezi lidmi, hledáte přátele a chcete pařit.</strong>",
      "Dražší než většina budapešťských hostelů, ale stojí za to, pokud chcete otevřený, společenský pobyt. Pozor na <strong>věkový limit 18 až 39 let</strong>.",
    ],
    "video": "videorecenzi Onefam Budapest",
    "groups": [
      ("Pokoje, postele a kvalita spánku", "pokoje a postele", [
        ("Prostorné pokoje, bezpečné úložiště", "<p>Pokoje jsou <strong>prostorné, s bezpečným úložným prostorem a skříňkami</strong>, postele nabízejí soukromí a pohodlí.</p>"),
        ("U postele není polička", "<p>U postele <strong>není kam dát telefon, sluchátka ani peněženku</strong>. Vezměte si malé pouzdro.</p>"),
        ("Kdy je klid", "<p>Večírek obvykle utichá <strong>mezi 23:00 a půlnocí</strong>, pak se parta přesune do ruin barů.</p>"),
      ]),
      ("Atmosféra a společenský život", "společné prostory", [
        ("Parta hned po příjezdu", "<p>Pokud přijedete sami a chcete rychle přátele, <strong>tohle je to místo</strong>. Personál zapojí každého.</p>"),
        ("Denní a večerní program", "<p>Denní aktivity zdarma, večer pitné hry a <strong>bar crawly</strong> po židovské čtvrti.</p>"),
      ]),
      ("Vybavení, koupelny a poloha", "vybavení", [
        ("Rozmary sprchy", "<p>Teplota vody kolísá a <strong>pohybový senzor při sprchování zhasíná světlo</strong>.</p>"),
        ("Základna v židovské čtvrti", "<p>Pár minut od <strong>Deák Ferenc tér a letištního autobusu 100E</strong>, z barů dojdete pěšky.</p>"),
      ]),
    ],
    "chips": [("yes", "Denní aktivity zdarma"), ("yes", "Hostelový bar"), ("yes", "Kuchyň nonstop"), ("yes", "Skříňky zdarma"), ("no", "Jen 18 až 39 let")],
  },
  {  # 3 Avenue
    "tag": "#3 Nejlepší levný hostel", "short": "Nejlevnější postel",
    "area": "VI. obvod, Oktogon",
    "checkin": "Check-in 14:00 až půlnoc, check-out do 11:00", "rules": "6 až 49 let, bez zavírací hodiny",
    "specs": ["Snídaně zdarma", "Závěsy u postelí", "Tramvaj nonstop", "Oktogon"],
    "best_for": "Šetřivým cestovatelům, kteří hledají nejlevnější postel v centru se snídaní zdarma a levnou večeří.",
    "skip_if": "máte lehké spaní nebo chcete společenskou, osobní atmosféru.",
    "trust": "Snídaně zdarma",
    "transit": "Oktogon (M1 a nonstop tramvaje 4, 6) přímo před domem",
    "watch": "Hlučný tramvajový uzel; vezměte si špunty do uší", "noise": "Hlučný (tramvajový uzel)",
    "pros": [
      ("Nejlepší poměr cena a výkon", "Mimo sezónu byly postele už od 8 € za noc, se snídaní zdarma a zlevněnou večeří."),
      ("Ušetříte peníze", "Jídlo je v Maďarsku drahé, s jídly zdarma a se slevou hodně ušetříte."),
      ("Personál", "Ochotný, rychlý a k dispozici nonstop."),
    ],
    "cons": [
      ("Kvalita bydlení", "Desetilůžkový dorm, kde jsem spal, byl co do pohodlí, soukromí a čistoty průměrný."),
      ("Zámek není zdarma", "Ke skříňkám zámek nedostanete, ale můžete si ho koupit asi za 3 €."),
      ("Neosobní", "Žádná společenská atmosféra, osobní péče ani program, kromě jídelny."),
      ("Hlučný", "Stojí u velké křižovatky s tramvajemi. Vezměte si špunty do uší."),
    ],
    "summary": [
      "<strong>Avenue Hostel je první volba šetřivých cestovatelů, kteří chtějí v Budapešti ušetřit na ubytování i jídle.</strong>",
      "Postele začínají <strong>zhruba na 8 €</strong>, se <strong>snídaní zdarma</strong> a zlevněnou večeří (při mém pobytu s malou minimální útratou na baru). Při vysokých cenách potravin v Maďarsku je to velký rozdíl.",
      "Žádný luxus, ale praktické a levné, dobrá volba pro ty, kdo hlídají rozpočet.",
      "📝 <strong>Poznámka redakce:</strong> desetilůžkový dorm \"se závěsy\", kde jsem spal, a jeho společné koupelny nebyly dobré. Ostatní 4, 8 a 12lůžkové pokoje hostelu jsou hezčí, jen dražší, takže si hostel zaslouží lepší hodnocení, než bych mu dal podle svého pokoje.",
    ],
    "video": "videorecenzi Avenue Hostel",
    "groups": [
      ("Pokoje, postele a kvalita spánku", "pokoje a postele", [
        ("Vyberte si lepší pokoj", "<p>Můj desetilůžkový pokoj byl slabé místo. <strong>Pokoje se 4, 8 a 12 lůžky jsou hezčí</strong> a stojí za těch pár eur navíc.</p>"),
        ("Špunty do uší jsou nutnost", "<p>Stojí na <strong>uzlu Oktogon s tramvajemi, které jezdí celou noc</strong>. Pro lehké spáče je lepší Maverick nebo Zen.</p>"),
        ("Zámek na skříňku", "<p>Zámek nedostanete. <strong>Vezměte si vlastní</strong> nebo si ho kupte na recepci asi za 3 €.</p>"),
      ]),
      ("Atmosféra a společenský život", "společné prostory", [
        ("Praktický, ne osobní", "<p>Nečekejte program ani osobní pohostinnost. <strong>Lidé se seznamují v jídelně.</strong></p>"),
        ("Pro koho je", "<p>Pro studenty a batůžkáře na dlouhé cestě, kteří otáčejí každé euro a hostel používají hlavně na spaní a jídlo.</p>"),
      ]),
      ("Jídlo, vybavení a poloha", "vybavení", [
        ("Snídaně zdarma, levná večeře", "<p><strong>Snídaně zdarma</strong> a zlevněná večeře jsou hlavní lákadlo. Denně ušetříte víc, než stojí postel.</p>"),
        ("Personál a doprava nonstop", "<p>Recepce je otevřená nonstop, <strong>M1 a nonstop tramvaje 4, 6</strong> zastavují před vchodem.</p>"),
      ]),
    ],
    "chips": [("yes", "Snídaně zdarma"), ("yes", "Závěsy u postelí"), ("yes", "Recepce 24 h"), ("yes", "Kuchyň pro hosty"), ("no", "Vezměte si zámek")],
  },
  {  # 4 Flow
    "tag": "#4 Nejlepší pro digitální nomády", "short": "Nejlepší pro digitální nomády",
    "area": "IX. obvod, Velká tržnice",
    "checkin": "Check-in 15:00 až půlnoc, check-out do 11:00", "rules": "Bez zavírací hodiny",
    "specs": ["Coworkingový prostor", "Zámek zdarma", "Kapslové postele", "Velká tržnice"],
    "best_for": "Digitálním nomádům a cestovatelům, kteří chtějí salonek vhodný pro práci na notebooku, kapslové postele a společenskou, ale klidnou atmosféru.",
    "skip_if": "máte těžká zavazadla (3. patro, bez výtahu) nebo chcete vlastní koupelnu.",
    "trust": "Coworkingový prostor",
    "transit": "Fővám tér (M4, tramvaje 2, 47, 49) a Kálvin tér (M3, M4)",
    "watch": "Smíšené společné koupelny; 3. patro, bez výtahu", "noise": "Klidný",
    "pros": [
      ("Personál", "Recepce je k dispozici nonstop, personál je přátelský a ochotný."),
      ("Přátelský", "Společenská atmosféra, snadno se seznámíte s dalšími cestovateli."),
      ("Skvělé postele", "Závěs, zásuvka, lampička, malá polička a úložný box u postele."),
      ("Bezpečné úložiště", "Zámek dostanete zdarma."),
      ("Pracovní kout", "Salonek s pracovním koutem vhodným pro notebook."),
    ],
    "cons": [
      ("Koupelny", "Koupelny jsou smíšené a společné, s malým soukromím."),
      ("Bez výtahu", "Hostel je ve 3. patře."),
      ("Hygiena", "Na prostěradle jsem měl vlasy, i když bylo vyprané. Celkově je hostel hygienický."),
      ("Plné lednice", "Část jídla, které jsem koupil, zmizela."),
      ("Stísněné pokoje", "Sotva bylo místo se pohnout."),
    ],
    "summary": [
      "<strong>Flow Spaces spojuje společenský život hostelu s klidem hotelu</strong>, ideální, pokud hledáte zlatou střední cestu.",
      "Atmosféra připomíná kolej, dobrá volba pro šetřivé cestovatele, kteří chtějí vyvážený zážitek. Postele začínají <strong>zhruba na 10 €</strong>.",
      "Díky přátelské atmosféře, <strong>klidnému pracovnímu prostoru</strong> a dobře vybavené kuchyni stojí za zvážení.",
    ],
    "groups": [
      ("Pokoje, postele a kvalita spánku", "pokoje a postele", [
        ("Dobře vybavené kapsle", "<p>Každá postel má <strong>závěs, zásuvku, lampičku, malou poličku a úložný box</strong>, se zámkem zdarma.</p>"),
        ("Stísněné pokoje", "<p>Pokoje jsou <strong>stísněné</strong>, když všichni balí, není se kam hnout.</p>"),
      ]),
      ("Atmosféra a pracovní prostor", "společné prostory", [
        ("Salonek pro notebook", "<p>V salonku je <strong>skutečný pracovní kout</strong> a hostel nabízí i coworkingový prostor: tady se na dálku pracuje nejlépe.</p>"),
        ("Společenský, ale vyvážený", "<p>Snadno se seznámíte, bez nocí jako v party hostelu. Spíš kolej než centrála bar crawlů.</p>"),
      ]),
      ("Vybavení, koupelny a poloha", "vybavení", [
        ("Koupelny a schody", "<p>Koupelny jsou <strong>smíšené a společné</strong> a hostel je ve <strong>3. patře bez výtahu</strong>.</p>"),
        ("Kuchyň a lednice", "<p>Kuchyň je dobře vybavená, ale lednice se zaplní a <strong>část mého jídla zmizela</strong>. Všechno si označte.</p>"),
        ("Vedle Velké tržnice", "<p><strong>Velká tržnice je o blok dál</strong> a Dunaj pár minut pěšky.</p>"),
      ]),
    ],
    "chips": [("yes", "Coworkingový prostor"), ("yes", "Zámek zdarma"), ("yes", "Závěsy u postelí"), ("yes", "Recepce 24 h"), ("no", "Bez výtahu (3. patro)")],
  },
  {  # 5 a&o
    "tag": "#5 Nejlepší hostel hotelového typu", "short": "Nejlepší pro hotelové pohodlí",
    "area": "VII. obvod, blízko Oktogonu",
    "checkin": "Check-in i check-out na recepci 24 h", "rules": "Vítá i rodiny a skupiny",
    "specs": ["Tiché pokoje", "Skvělá sprcha", "Pracovní kout", "Soukromé pokoje"],
    "best_for": "Párům, rodinám a všem, kdo místo společenského života chtějí tichý, jednoduchý a čistý pokoj.",
    "skip_if": "hledáte společenský hostel nebo nechcete platit zvlášť za povlečení.",
    "trust": "Soukromé pokoje",
    "transit": "Oktogon (M1, tramvaje 4, 6) a Vörösmarty utca (M1), pár minut pěšky",
    "watch": "Povlečení asi 3 € navíc; vezměte si zámek", "noise": "Klidný",
    "pros": [
      ("Výborné pokoje", "Jednoduchý, tichý a čistý pokoj s fantastickou sprchou."),
      ("Bezpečné úložiště", "Na recepci mi ochotně zamkli notebook."),
      ("Pracovní kout", "V salonku je výborný pracovní kout vhodný pro notebook."),
    ],
    "cons": [
      ("Povlečení a ručník", "Nejsou v ceně, stojí 1150 Ft (asi 3 €) navíc."),
      ("Úložná \"klec\"", "K úložnému prostoru v pokoji zámek NEDOSTANETE."),
      ("Špinavý polštář", "Polštář mi mohli vyměnit, ale celkově je hostel hygienický."),
      ("Nudná snídaně", "Průměrná hotelová snídaně asi za 8 € (volitelná)."),
    ],
    "summary": [
      "<strong>a&amp;o Budapest City je pro šetřivé cestovatele, kterým jsou pohodlí a klid důležitější než rušný společenský život.</strong>",
      "Postele začínají <strong>zhruba na 12 €</strong>, ale počítejte s příplatkem za povlečení (asi 3 €).",
      "I přes drobné nedostatky jako polštář a poplatek za povlečení je díky ceně a pohodlí dobrou volbou, pokud hledáte klidné místo s pracovním prostorem.",
    ],
    "groups": [
      ("Pokoje, postele a kvalita spánku", "pokoje a postele", [
        ("Tichý, čistý, jednoduchý", "<p><strong>Jednoduchý, tichý a čistý pokoj</strong> s výbornou sprchou. Blíž levnému hotelu než hostelu.</p>"),
        ("Započítejte si příplatky", "<p><strong>Povlečení stojí asi 3 €</strong> a na úložný prostor potřebujete vlastní zámek. Připočtěte si to k ceně.</p>"),
      ]),
      ("Atmosféra a pracovní prostor", "společné prostory", [
        ("Klidná základna, žádná párty", "<p>Málo hostelového programu. Pro ty, kdo chtějí <strong>soukromí a spánek</strong>, pro páry a rodiny.</p>"),
        ("Salonek pro notebook", "<p>V salonku je <strong>výborný pracovní kout vhodný pro notebook</strong>.</p>"),
      ]),
      ("Vybavení a poloha", "vybavení", [
        ("Bezpečné úložiště", "<p>Recepce mi <strong>bezpečně zamkla notebook</strong>, když jsem byl pryč.</p>"),
        ("Snídaně", "<p><strong>Volitelná hotelová snídaně asi za 8 €</strong>. V pořádku, nic zvláštního.</p>"),
        ("Poloha", "<p>V ulici Csengery, pár minut pěšky od <strong>Oktogonu a třídy Andrássy</strong>.</p>"),
      ]),
    ],
    "chips": [("yes", "Tiché pokoje"), ("yes", "Soukromé pokoje"), ("yes", "Pracovní kout"), ("no", "Povlečení zvlášť (asi 3 €)"), ("no", "Vezměte si zámek")],
  },
  {  # 6 Wombat's
    "tag": "#6 Nejlepší pohodový party hostel", "short": "Nejlepší pro pohodovou párty",
    "area": "VI. obvod, ulice Király",
    "checkin": "Check-in 14:00 až 23:00, check-out do 10:00", "rules": "Bez zavírací hodiny",
    "specs": ["Dormy s koupelnou", "Závěsy u postelí", "Hostelový bar", "Ulice Király"],
    "best_for": "Batůžkářům, kteří chtějí společenský bar a noční život za dveřmi, ale zároveň se dobře vyspat.",
    "skip_if": "hledáte nejlevnější postel nebo hostel s opravdovým charakterem.",
    "trust": "Dormy s koupelnou",
    "transit": "Deák Ferenc tér (M1, M2, M3 a letištní autobus 100E), 3 minuty pěšky",
    "watch": "Drahý na to, co nabízí", "noise": "Uvnitř klid",
    "pros": [
      ("Přátelský", "Uvolněná společenská atmosféra, snadno se seznámíte."),
      ("Není hlučný", "Na party hostel je tichý. Dobře se vyspíte."),
      ("Personál", "Recepce nonstop a bezpečná úschovna zavazadel."),
    ],
    "cons": [
      ("Cena", "Ceny by mohly být nižší. Neměl jsem pocit, že by hostel nabízel něco výjimečného, co by je ospravedlnilo."),
    ],
    "summary": [
      "<strong>Wombat's City Hostel je centrum mladých cestovatelů, kteří přijeli za budapešťským nočním životem</strong>, s mladistvou energií a uvolněnou atmosférou, ideální pohodový party hostel.",
      "Dražší než většina hostelů v Budapešti. Poloha je velká výhoda, ale některé věci jsou průměrné: koupelny jsou například čisté, ale nic víc.",
      "Nejlepší byli hosté: seznamovat se a pařit se zajímavými cestovateli z celého světa bohatě vyvážilo drobnosti.",
    ],
    "groups": [
      ("Pokoje, postele a kvalita spánku", "pokoje a postele", [
        ("Pokoje s koupelnou", "<p>Podle hostelu má každý pokoj <strong>vlastní koupelnu a klimatizaci</strong> a postele v dormech mají závěsy.</p>"),
        ("Lepší na spaní než na párty", "<p>Na party hostel je <strong>v noci klid</strong>. Spal jsem dobře.</p>"),
      ]),
      ("Atmosféra a společenský život", "společné prostory", [
        ("Pohodová party společnost", "<p>Snadno se seznámíte v <strong>hostelovém baru</strong> a bary v Gozsdu udvar jsou pár kroků odsud.</p>"),
        ("Dělají to hosté", "<p>Mezinárodní parta byla <strong>to nejlepší z mého pobytu</strong>.</p>"),
      ]),
      ("Vybavení a poloha", "vybavení", [
        ("Průměrné, ale čisté", "<p>Vybavení je <strong>čisté, ale průměrné</strong>; nerezervujte ho kvůli designu.</p>"),
        ("V centru v ulici Király", "<p>Pár minut od <strong>Deák Ferenc tér</strong>, letištního autobusu 100E a nočního života židovské čtvrti.</p>"),
      ]),
    ],
    "chips": [("yes", "Dormy s koupelnou"), ("yes", "Klimatizace"), ("yes", "Hostelový bar"), ("yes", "Recepce 24 h"), ("yes", "Skříňky zdarma")],
  },
  {  # 7 Zen
    "tag": "#7 Nejlepší klidný, útulný hostel", "short": "Nejlepší pro klid a útulnost",
    "area": "IX. obvod, Velká tržnice",
    "checkin": "Check-in 14:00 až 21:00, check-out do 11:00", "rules": "Omezená otevírací doba recepce",
    "specs": ["Domácká atmosféra", "Malý hostel", "Čaj a káva zdarma", "Velká tržnice"],
    "best_for": "Introvertům a pomalým cestovatelům, kteří hledají malé, útulné, domácké místo u Dunaje.",
    "skip_if": "přijíždíte pozdě, potřebujete skříňku nebo hledáte stůl se zásuvkou.",
    "trust": "Check-in do 21:00",
    "transit": "Fővám tér (M4, tramvaje 2, 47, 49), vedle Velké tržnice",
    "watch": "Žádný pozdní check-in; žádné uzamykatelné úložiště", "noise": "Klidný",
    "pros": [
      ("Personál", "Při mém pobytu vedl celý hostel jediný hostitel: přátelský, ochotný a veselý. Díky němu dávám 9/10."),
      ("Přátelský", "Konverzaci šlo začít kdekoli. Gauč v obýváku byl skvělé místo na povídání."),
      ("Jako doma", "Pokud máte rádi útulnou, domáckou atmosféru, je to ráj."),
    ],
    "cons": [
      ("Žádný nonstop check-in", "Hostitel odcházel ve 21:00 a check-in trval dlouho."),
      ("Málo personálu", "Jeden člověk žongloval s příliš mnoha úkoly; potřeboval by aspoň jednoho kolegu."),
      ("Není bezpečný", "Nebylo tu žádné uzamykatelné úložiště."),
      ("Není pro nomády", "Žádný pracovní kout se zásuvkami."),
    ],
    "summary": [
      "<strong>Central Market Hall Zen Hostel je milé útočiště, pokud hledáte malé, útulné místo, které působí spíš jako domov než hostel.</strong>",
      "Ceny jsou na to, co dostanete, trochu nadprůměrné, postele v dormu začínají <strong>zhruba na 11 €</strong>. Není to nejlepší poměr cena a výkon, ale pokud je pro vás důležitá domácká atmosféra a poloha u Velké tržnice, vyplatí se.",
    ],
    "groups": [
      ("Pokoje a kvalita spánku", "pokoje a postele", [
        ("Malý a klidný", "<p><strong>Malý hostel s klidnou, domáckou atmosférou</strong>, bez párty společnosti.</p>"),
        ("Žádné uzamykatelné úložiště", "<p>Při mém pobytu tu <strong>nebylo uzamykatelné úložiště</strong>. Cennosti noste u sebe, nebo si vyberte jiný hostel, pokud je to pro vás důležité.</p>"),
      ]),
      ("Atmosféra a obývák", "společné prostory", [
        ("Povídání v obýváku", "<p>Všichni skončí na <strong>gauči v obýváku</strong> a povídají si. Deskové hry, čaj a káva celý den.</p>"),
        ("Ne pro práci na dálku", "<p>Žádný stůl se zásuvkou. <strong>Pro digitální nomády je lepší Flow Spaces nebo Maverick.</strong></p>"),
      ]),
      ("Check-in a poloha", "vybavení", [
        ("Přijeďte před 21:00", "<p>Check-in je <strong>od 14:00 do 21:00</strong> a recepce má omezenou otevírací dobu. Letíte pozdním letem? Rezervujte jinde.</p>"),
        ("Vedle Velké tržnice", "<p>Na Vámház körút, <strong>vedle Velké tržnice a Mostu Svobody</strong>, na Fővám tér je M4 a tramvaj 2.</p>"),
      ]),
    ],
    "chips": [("yes", "Domácká atmosféra"), ("yes", "Čaj a káva zdarma"), ("yes", "Vedle Velké tržnice"), ("no", "Check-in do 21:00"), ("no", "Bez uzamykatelného úložiště")],
  },
  {  # 8 Adagio
    "tag": "#8 Nejlepší poloha na prohlídky města", "short": "Nejlepší na prohlídky města",
    "area": "VI. obvod, třída Andrássy",
    "checkin": "Check-in 15:00 až půlnoc, check-out do 10:00", "rules": "Bez zavírací hodiny",
    "specs": ["Výhled na baziliku", "Vlastní koupelny", "Čaj a káva zdarma", "Třída Andrássy"],
    "best_for": "Milovníkům prohlídek, kteří chtějí klidnou, čistou postel na začátku třídy Andrássy, pár kroků od baziliky svatého Štěpána.",
    "skip_if": "hledáte společenský hostel nebo vám vadí hluk z dopravy.",
    "trust": "Pár kroků od baziliky",
    "transit": "Bajcsy-Zsilinszky út (M1) před domem, Deák Ferenc tér (M1, M2, M3) kousek pěšky",
    "watch": "Hluk z dopravy; bez výtahu (1. patro)", "noise": "Hluk z dopravy",
    "pros": [
      ("Skvělá koupelna", "Výborná, čistá vlastní koupelna."),
      ("Výborná poloha", "S výhledem na baziliku svatého Štěpána."),
      ("Klidný", "Není tak rušný jako některé jiné hostely, takže je víc soukromí."),
    ],
    "cons": [
      ("Hlučný", "V mém pokoji byl kvůli dopravě velký hluk."),
      ("Bez výtahu", "Hostel je v prvním patře."),
      ("Neosobní", "Žádná společenská atmosféra ani osobní péče."),
    ],
    "summary": [
      "<strong>Adagio 2.0 je vaše místo, pokud je nejdůležitější dobře se vyspat v čistém, pohodlném pokoji.</strong>",
      "Nic výjimečného, ale základy dělá dobře: dobrá volba pro levné, minimalistické ubytování ve fantastické poloze.",
      "Ani peněženku nezruinuje: na nejbližší termíny začínají postele v dormu <strong>zhruba na 11 €</strong> a soukromé pokoje <strong>zhruba na 22 €</strong>.",
    ],
    "groups": [
      ("Pokoje a kvalita spánku", "pokoje a postele", [
        ("Čisté pokoje, skvělá koupelna", "<p>K mému pokoji patřila <strong>výborná, čistá vlastní koupelna</strong>. Jsou tu dormy i dvoulůžkové pokoje s koupelnou.</p>"),
        ("Hluk z dopravy", "<p>Třída Andrássy je hlavní tah a <strong>můj pokoj byl kvůli dopravě hlučný</strong>. Vezměte si špunty nebo požádejte o pokoj do dvora.</p>"),
      ]),
      ("Atmosféra", "společné prostory", [
        ("Klidný, ne společenský", "<p><strong>Žádný společenský život ani osobní péče.</strong> Klidná základna na prohlídky, ne na seznamování.</p>"),
      ]),
      ("Vybavení a poloha", "vybavení", [
        ("Kuchyň, čaj a káva", "<p>Podle hostelu mohou hosté používat <strong>plně vybavené kuchyně</strong>, čaj, káva a povlečení jsou zdarma.</p>"),
        ("První patro, bez výtahu", "<p>V <strong>prvním patře paláce, bez výtahu</strong>, jedno rameno schodů.</p>"),
        ("Nepřekonatelné na památky", "<p>Na <strong>začátku třídy Andrássy</strong>, pár minut pěšky od baziliky svatého Štěpána, Opery a Deák Ferenc tér.</p>"),
      ]),
    ],
    "chips": [("yes", "Výhled na baziliku"), ("yes", "Kuchyň pro hosty"), ("yes", "Recepce 24 h"), ("yes", "Čaj a káva zdarma"), ("no", "Bez výtahu (1. patro)")],
  },
  {  # 9 Das Nest
    "tag": "#9 Nejlepší malý, útulný hostel", "short": "Nejlepší malý a útulný",
    "area": "VII. obvod, židovská čtvrť",
    "checkin": "Check-in 12:00 až 23:00, check-out do 11:00", "rules": "Bez zavírací hodiny",
    "specs": ["Útulný loft", "Místní tipy", "Kuchyň pro hosty", "Židovská čtvrť"],
    "best_for": "Sólo batůžkářům a malým skupinám, kteří hledají útulný hostel jako byt s přátelskými hostiteli v párty čtvrti.",
    "skip_if": "chcete platit kartou, potřebujete bezbariérový přístup nebo chcete klid i o víkendu.",
    "trust": "Soukromé pokoje od 17 €",
    "transit": "Wesselényi utca (tramvaje 4, 6) a Blaha Lujza tér (M2), pár minut pěšky",
    "watch": "Při mém pobytu jen hotovost; víkendový hluk z ulice", "noise": "Víkendový hluk z ulice",
    "pros": [
      ("Centrální poloha", "V srdci Budapešti, blízko hlavních památek i nočního života."),
      ("Přátelský personál", "Milý, ochotný, se skvělými místními doporučeními."),
      ("Útulná atmosféra", "Útulné, komorní místo, ideální na seznamování."),
      ("Dobře vybavená kuchyň", "Plně vybavená kuchyň pro hosty."),
      ("Místní kontakty", "Tipy na bary, restaurace a festivaly, které byste sami nenašli."),
    ],
    "cons": [
      ("Jen hotovost", "Při mém pobytu nepřijímali karty, jen hotovost."),
      ("Možný hluk", "Kvůli rušnému nočnímu životu může být v noci hluk."),
      ("Omezená bezbariérovost", "Není přístupný všem lidem s postižením."),
    ],
    "summary": [
      "<strong>Das Nest je ideální, pokud hledáte ubytování v centru Budapešti s útulnou, společenskou atmosférou.</strong> Jde o přátelský přístup, uvolněnou náladu a skvělé místní tipy.",
      "Při mém pobytu chyběly vymoženosti jako platba kartou, ale vynahrazuje to osobní péčí a skvělou polohou. Pro ty, kdo dávají přednost dostupnému pohodlí a seznamování před luxusem.",
      "Pokoje: smíšené nebo jen dámské dormy se 4 nebo 6 lůžky a jeden dvoulůžkový soukromý pokoj. Postel v dormu <strong>zhruba od 15 €</strong>.",
    ],
    "groups": [
      ("Pokoje a kvalita spánku", "pokoje a postele", [
        ("Malé dormy", "<p><strong>Smíšené nebo jen dámské dormy se 4 a 6 lůžky</strong> a jeden dvoulůžkový soukromý pokoj. Dost malé na to, aby to bylo osobní.</p>"),
        ("Víkendový hluk", "<p>Leží v párty čtvrti, takže <strong>lehcí spáči by si na pátek a sobotu měli vzít špunty</strong>.</p>"),
      ]),
      ("Atmosféra a společenský život", "společné prostory", [
        ("Jako byt kamaráda", "<p>Hostel se popisuje jako <strong>zrekonstruovaný podkrovní loft</strong> a přesně takový je: komorní a společenský.</p>"),
        ("Hostitelé s místními tipy", "<p>Od personálu jsem dostal <strong>tipy na bary, restaurace a festivaly</strong>, které nebyly v žádném průvodci.</p>"),
      ]),
      ("Vybavení a placení", "vybavení", [
        ("Kuchyň", "<p><strong>Plně vybavená kuchyň pro hosty</strong>, dobrá na šetření.</p>"),
        ("Mějte hotovost", "<p>Při mém pobytu přijímali <strong>jen hotovost</strong>. Zkontrolujte podmínky rezervace a pro jistotu si vezměte forinty.</p>"),
      ]),
    ],
    "chips": [("yes", "Útulná atmosféra"), ("yes", "Kuchyň pro hosty"), ("yes", "Skříňky zdarma"), ("yes", "Dámské dormy"), ("no", "Jen hotovost (při mém pobytu)")],
  },
  {  # 10 The Hive
    "tag": "#10 Nejlepší velký party hostel", "short": "Největší party hostel",
    "area": "VII. obvod, židovská čtvrť",
    "checkin": "Check-in 15:00 až půlnoc, check-out do 11:00", "rules": "Výhradně 18+, bez zavírací hodiny",
    "specs": ["Střešní bar", "Denní bar crawly", "Jen 18+", "Židovská čtvrť"],
    "best_for": "Skupinám starším 18 let a sólo pařmenům, kteří chtějí velký, hlučný party hostel se střešním barem ve čtvrti ruin barů.",
    "skip_if": "máte lehké spaní, vstáváte brzy nebo chcete závěsy u postelí.",
    "trust": "Výhradně 18+",
    "transit": "Astoria (M2) a Deák Ferenc tér (M1, M2, M3), pár minut pěšky",
    "watch": "Hluk z klubu pod hostelem; bez závěsů u postelí", "noise": "Hlučný (party hostel)",
    "why": [
      ("Velký party hostel", "Podle hostelu přes 300 lůžek od roku 2015, s denními bar crawly, bingo bar crawly, SPArty a párty loděmi."),
      ("Střešní bar", "Vlastní střešní bar pro hosty, s denní happy hour od 16 do 19 hodin."),
      ("Poloha", "Ve čtvrti ruin barů, kousek pěšky od Gozsdu udvar a Szimpla Kert."),
      ("Praktický", "Recepce 24 h, skříňky, platba hotově nebo kartou."),
    ],
    "skip": [
      ("Hluk", "Sám hostel varuje lehké spáče a ranní ptáčata; hosté zmiňují hluk z klubu dole."),
      ("Bez závěsů u postelí", "Hosté často žádají závěsy u postelí."),
      ("Wi-Fi", "Slabá wifi je opakovaná stížnost hostů."),
      ("Věkový limit", "Výhradně od 18 let."),
    ],
    "summary": [
      "<strong>The Hive je velký, hlučný party hostel Budapešti.</strong> S více než 300 lůžky, střešním barem a denními bar crawly je stavěný na noci, ne na brzká rána.",
      "Zařadil jsem ho jako párty alternativu k Onefamu: fakta tady pocházejí z vlastních informací hostelu a z recenzí hostů, ověřeno 14. listopadu 2026. Postele v dormu začínají <strong>zhruba na 13 €</strong>.",
    ],
    "chips": [("yes", "Střešní bar"), ("yes", "Denní bar crawly"), ("yes", "Recepce 24 h"), ("yes", "Skříňky zdarma"), ("no", "Výhradně 18+")],
  },
]

HOSTELS = build(_T, floor_label="1. patro")


def _areas(H, a):
    return (
        '<h3>VII. obvod (židovská čtvrť): kvůli nočnímu životu</h3>\n'
        '<p>Jsou tu ruin bary, Gozsdu udvar a Szimpla Kert, a také %s, %s a %s. Skvělé na párty, <strong>pro lehké spáče o víkendu nejhorší</strong>.</p>\n'
        '<h3>VI. obvod (ulice Király, třída Andrássy, Oktogon): v centru a dobře dostupný</h3>\n'
        '<p>%s, %s a %s leží na hlavních tazích, u M1 a nonstop tramvají 4, 6. Všude dojdete pěšky, ale <strong>doprava na hlavních ulicích</strong> může být hlučná.</p>\n'
        '<h3>IX. obvod (Velká tržnice): klidnější, u řeky</h3>\n'
        '<p>%s, %s a %s leží u Velké tržnice, pár minut od Dunaje. Tohle bych vybral, pokud chcete <strong>klidnější noci</strong> a přesto dojít do centra pěšky.</p>\n'
        '<p>Přilétáte? Tady se dočtete, <a href="/cs/letiste-budapest-do-centra">jak se dostat z letiště do centra</a>: autobus 100E staví na Deák Ferenc tér, kousek pěšky od hostelů v VI. a VII. obvodu.</p>'
    ) % (a(H[2]), a(H[9]), a(H[10]), a(H[6]), a(H[8]), a(H[3]), a(H[1]), a(H[4]), a(H[7]))


UI = {
    "url": URL, "home": "Domů", "home_url": "https://www.budapestadventures.com/cs", "about_url": "https://www.budapestadventures.com/cs/about",
    "title": "10 nejlepších hostelů v Budapešti v roce 2026 (spal jsem v 9)",
    "h1_main": "10 nejlepších hostelů v Budapešti v roce 2026", "h1_muted": "(spal jsem v 9)",
    "meta": "Spal jsem v 9 nejlepších hostelech v Budapešti, 30 nocí v Mavericku. Postele od 8 €: nejlepší party, klidné, levné a nomádské hostely podle čtvrti.",
    "breadcrumb": "Nejlepší hostely v Budapešti", "kicker_badge": "Srovnání hostelů 2026",
    "author_line": 'Autor: <a href="/cs/about" target="_blank">Adam Dimitrov</a>, zakladatel a tester v Budapešti',
    "author_role": "Spal jsem v 9 z 10 • Vlastní fotky a videorecenze",
    "last_updated": "<strong>Aktualizováno</strong>: 14. listopadu 2026",
    "job_title": "Zakladatel a tester v Budapešti",
    "intro": (
        '<p>Špatný hostel v Budapešti vás nestojí peníze, ale spánek. Postele v dormech v centru stojí <strong>8 až 15 €</strong> za noc, '
        'ale party hostel v židovské čtvrti a klidný kapslový hostel u Velké tržnice jsou dvě úplně jiné cesty.</p>\n'
        '<p>V <strong>9 z 10 hostelů níže jsem sám spal</strong>, v Mavericku například <strong>30 nocí za 280 €</strong>, a porovnal jsem je vedle sebe v tom, '
        'co při rezervaci rozhoduje: hluk v noci, soukromí v posteli, koupelny, kuchyň, věkový limit, klientela a skutečná cena za noc. '
        'The Hive je jediná párty volba, kde jsem nespal, proto u něj uvádím jen ověřená fakta, bez odznaku \"otestováno\".</p>\n'
        '<p>Ceny a hodnocení ověřeny <strong>%s</strong>. Filtry vás rovnou přenesou k party, klidným, levným, nomádským hostelům nebo hostelům se soukromými pokoji.</p>\n' % CHECKED),
    "filters": [("party", "🎉 Společenské a párty"), ("quiet", "😴 Klidný spánek"), ("budget", "💶 Pod 11 €"),
                ("private", "🛏️ Soukromé pokoje"), ("nomad", "💻 Digitální nomádi"), ("kitchen", "🍳 Kuchyň pro hosty")],
    "district_fmt": "%s. obvod", "decimal": ",", "thousands": " ", "k": "k",
    "tested_chip": "✓ Osobně otestováno",
    "best_for_card": "Pro koho:", "best_for_summary": "Pro koho:", "skip_if": "Vynechte, pokud",
    "from_eur": "od %d €", "eur": "%d €", "card_psub": "Postel/noc • 14. 11. 2026",
    "card_btn": "Ceny a termíny →", "read_review": "Recenze ↓",
    "pros": "Výhody:", "cons": "Nevýhody:", "why": "Proč ho vybrat:", "why_skip": "Proč ne:",
    "video": "Video:", "watch_my": "Podívejte se na moji",
    "summary_title": "Verdikt a hodnocení", "summary_pill": "Přehled",
    "swipe_photos": "%d fotek, posuňte →", "one_photo": "1 fotka", "no_photo": "Vlastní zkušenost",
    "photo_alt": "%s: %s, vlastní fotka", "prev_photo": "Předchozí fotka", "next_photo": "Další fotka",
    "buy_badge": "Aktuální ceny a volná místa", "buy_sub": "Postel v dormu za noc • Ověřeno: " + CHECKED,
    "address_perk": "Adresa: <strong>%s</strong>", "privates_perk": "Soukromý pokoj <strong>od %d €</strong>",
    "buy_cta": "Termíny a ceny", "buy_trust": "Cena se mění podle data; konečnou cenu uvidíte před platbou",
    "qf": {"title": "Rychlá fakta: %s", "address": "Adresa", "dorm": "Postel v dormu", "transit": "Doprava", "checkin": "Check-in",
           "rules": "Pravidla", "ratings": "Hodnocení", "watch": "Na co si dát pozor",
           "dorm_fmt": "od %d € za noc (ověřeno: " + CHECKED + ")", "priv_fmt": ", soukromý pokoj od %d €",
           "hw_fmt": "Hostelworld %s/10 (%s hodnocení)", "bk_fmt": ", Booking.com %s/10 (%s hodnocení)"},
    "breakdown_h2": "Podrobné recenze: 10 nejlepších hostelů v Budapešti",
    "breakdown_sub": "Spal jsem v 9, 1 párty volba podle ověřených faktů • Kliknutím otevřete nebo zavřete",
    "picks": [
        ("Celkově", 1, "Společenský bez hluku z večírků, postele se závěsem, skvělé koupelny a 280 € za mých 30 nocí."),
        ("Sólo cestovatelé (18 až 39 let)", 2, "S denními aktivitami zdarma a bar crawly najdete přátele hravě. Je vám přes 39? Vyberte Maverick nebo Wombat's."),
        ("Párty", 10, lambda H: 'Velká, hlučná volba se střešním barem ve čtvrti ruin barů. Raději v pohodě? <a href="#%s">%s</a>.' % (H[6]['id'], H[6]['name'])),
        ("Nejlevnější postel", 3, "Postel zhruba od 8 € se snídaní zdarma. Vezměte si špunty: stojí u tramvajového uzlu."),
        ("Klidný spánek", 1, lambda H: 'Klidná boční ulice v IX. obvodu. Také klidné: <a href="#%s">%s</a> a <a href="#%s">%s</a>.' % (H[7]['id'], H[7]['name'], H[5]['id'], H[5]['name'])),
        ("Digitální nomádi", 4, "Salonek pro práci na notebooku a coworkingový prostor. Na delší pobyt je alternativou Maverick."),
        ("Páry a rodiny", 5, "Jednoduché, tiché, čisté pokoje se soukromou variantou. Počítejte asi se 3 € za povlečení."),
        ("Prohlídky města", 8, "Na začátku třídy Andrássy, pár minut od baziliky svatého Štěpána a Deák tér."),
        ("Malý a útulný", 9, "Jako loft kamaráda v židovské čtvrti, s hostiteli plnými místních tipů."),
    ],
    "sections": {
        "picks_badge": "Rychlý výběr", "picks_h2": "Nejlepší hostel v Budapešti podle typu cestovatele",
        "picks_sub": "Krátká odpověď pro každý typ cesty, podle mých vlastních pobytů",
        "table_badge": "Vedle sebe", "table_h2": "Hostely v Budapešti ve srovnání: cena, hluk a háčky",
        "table_sub": "Ceny dormů a skóre Hostelworld ověřeny " + CHECKED + ". Hluk a háčky z mých vlastních pobytů (The Hive: recenze hostů).",
        "table_cols": ["Hostel", "Nejlepší pro", "Čtvrť", "Postel v dormu", "Hostelworld", "Hluk v noci", "Na co si dát pozor"],
        "areas_badge": "Čtvrti", "areas_h2": "Kde v Budapešti bydlet v hostelu",
        "areas_sub": "Všech 10 leží v centru Pešti. Obvod rozhoduje o tom, jak hlučné budou vaše noci.",
        "areas_body": _areas,
        "map_h2": "Mapa: nejlepší hostely v Budapešti",
        "map_sub": 'Hostely ze seznamu v centrálních obvodech (<a href="/cs/pesi-prohlidky-budapest">VII. obvod, židovská čtvrť</a>, V. obvod, VI. obvod Terézváros a IX. obvod Ferencváros)',
        "types_h2": "Typy hostelů v Budapešti",
    },
    "faq": [
        ("Který hostel v Budapešti je nejlepší?",
         "<p>Celkově je mým favoritem <strong>Maverick Central Market</strong>: společenský bez hluku z večírků, postele se závěsem, skvělé koupelny a opravdová cena na dlouhý pobyt (v březnu jsem za 30 nocí zaplatil 280 €). "
         "Na společenský pobyt je správnou volbou <strong>Onefam Budapest</strong>, na nejlevnější postel <strong>Avenue Hostel</strong>.</p>"),
        ("Které hostely v Budapešti jsou nejlepší pro sólo cestovatele?",
         "<p>V <strong>Onefam Budapest</strong> najdete přátele nejsnáz díky denním aktivitám zdarma a bar crawlům, přijímá ale jen hosty <strong>ve věku 18 až 39 let</strong>. "
         "Je vám přes 39 nebo chcete víc spát? <strong>Maverick Central Market</strong> a <strong>Wombat's City Hostel</strong> jsou společenské bez povinné párty.</p>"),
        ("Které party hostely v Budapešti jsou nejlepší?",
         "<p><strong>Onefam Budapest</strong> (společenský, denní bar crawly), <strong>The Hive Party Hostel</strong> (velký, hlučný, se střešním barem, výhradně 18+) a "
         "<strong>Wombat's City Hostel</strong> (pohodová párty, dá se i spát). Všechny tři jsou kousek pěšky od ruin barů židovské čtvrti.</p>"),
        ("Ve kterém hostelu v Budapešti se nejlépe vyspíte?",
         "<p>V <strong>Maverick Central Market</strong> (klidná boční ulice), v <strong>Central Market Hall Zen Hostel</strong> (malý a domácký) a v <strong>a&amp;o Budapest City</strong> (pokoje jako v hotelu). "
         "Pokud máte lehké spaní, vyhněte se Avenue Hostel: stojí u tramvajového uzlu Oktogon.</p>"),
        ("Kolik stojí hostel v Budapešti?",
         "<p>14. listopadu 2026 začínaly postele v dormech v těchto 10 hostelech <strong>zhruba na 8 až 15 €</strong> za noc (Avenue od 8 €, Das Nest od 15 €), soukromé pokoje zhruba na 17 až 28 €. "
         "Dráž je <strong>o víkendech, v létě (od května do září), během srpnového Sziget Festivalu, vánočních trhů a na Silvestra</strong>.</p>"),
        ("Ve které čtvrti si v Budapešti rezervovat hostel?",
         "<p>Ve <strong>VII. obvodu (židovská čtvrť)</strong> kvůli nočnímu životu, v <strong>VI. obvodu</strong> (ulice Király, třída Andrássy) kvůli centrální, dobře dostupné základně "
         "a v <strong>IX. obvodu</strong> u Velké tržnice kvůli klidnějším nocím blízko Dunaje.</p>"),
        ("Mají hostely v Budapešti věkové limity?",
         "<p>Některé ano. Podle svých pravidel <strong>Onefam Budapest přijímá hosty ve věku 18 až 39 let</strong>, <strong>The Hive je výhradně 18+</strong> a <strong>Avenue Hostel přijímá hosty od 6 do 49 let</strong>. Před rezervací si pravidla zkontrolujte.</p>"),
        ("Jsou hostely v Budapešti bezpečné?",
         "<p>Obecně ano, ale drobné krádeže se stávají: v jednom hostelu mi ukradli mikinu a krabičku nosních náplastí. <strong>Cennosti zamykejte do skříňky</strong> a vezměte si zámek, protože některé hostely "
         "(Avenue, a&amp;o) ho nedávají. Flow Spaces vám ho dá zdarma.</p>"),
        ("Podle čeho jste vybral nejlepší hostely v Budapešti?",
         "<p>V 9 z 10 hostelů jsem spal a hodnotil jsem je podle: <strong>polohy, hluku v noci, čistoty, pohodlí a soukromí postele, vybavení, klientely a ceny</strong>. "
         "The Hive je zařazen jako párty volba podle ověřených faktů a recenzí hostů, bez odznaku otestováno.</p>"),
        ("Co si vzít s sebou do hostelu?",
         "<p><strong>Nutnost:</strong> špunty do uší a maska na spaní. <strong>Základ:</strong> žabky, pyžamo, nabíječka na telefon, vlhčené ubrousky, deodorant, kartáček a zubní pasta. "
         "<strong>Volitelně</strong> (zjistěte, co hostel poskytuje): ručník, zámek, šampon a sprchový gel.</p>"),
    ],
    "sticky_trust": "Postel/noc", "sticky_cta": "Ceny →", "sheet_label": "Přejít na hostel v Budapešti",
    "toc_breakdown": "Podrobné recenze (10 hostelů)",
    "szimpla_alt": "Ruin bar Szimpla Kert, kousek pěšky od The Hive v ulici Dob",
    "szimpla_pill": "Szimpla Kert, 3 min pěšky",
    "collapse_label": "Zavřít", "expand_label": "Otevřít recenzi",
    "price_range": "Postel od %d €",
}
