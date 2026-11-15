# -*- coding: utf-8 -*-
"""Textos en español: /es/mejores-hostales-budapest. Datos: hostels_data_en.py (14/11/2026)."""
from hostels_data_en import CHECKED_ISO
from hostels_i18n import build

CHECKED = "14 de noviembre de 2026"
URL = "https://www.budapestadventures.com/es/mejores-hostales-budapest"

_T = [
  {  # 1 Maverick
    "tag": "🏆 #1 Mejor hostel en general", "short": "El mejor en general",
    "area": "Distrito IX, Gran Mercado Central",
    "checkin": "Check-in desde las 15:00, check-out hasta las 11:00", "rules": "Sin toque de queda",
    "specs": ["Cortinas en la cama", "Terraza en la azotea", "Calle tranquila", "Ideal para estancias largas"],
    "best_for": "Viajeros solos, nómadas digitales y mochileros de larga estancia que quieren un hostel sociable sin ruido de fiesta.",
    "skip_if": "buscas un hostel de fiesta junto a los bares en ruinas.",
    "trust": "Privadas desde 28 €",
    "transit": "Kálvin tér (M3, M4) y Fővám tér (M4, tranvías 2, 47, 49), ambos a pocos minutos a pie",
    "watch": "Cocina llena en horas punta; guarda tus objetos de valor bajo llave", "noise": "Tranquilo",
    "pros": [
      ("Económico", "En temporada baja conseguí cama desde 9 € la noche. En marzo pagué 280 € por 30 noches."),
      ("Genial para estancias largas", "Se siente como tu propia habitación de residencia, cómodo incluso para un mes."),
      ("Gran ubicación", "En el distrito IX, más tranquilo, pero lo bastante céntrico para la vida nocturna y el transporte."),
      ("Habitaciones geniales", "Dormitorios modernos con taquillas grandes y cortinas en la cama."),
      ("Baños geniales", "Los baños compartidos (o privados) están bien cuidados, limpios y son de calidad."),
      ("Poco ruido", "El ruido de la calle es mínimo porque el hostel está en una calle pequeña."),
    ],
    "cons": [
      ("Cocina", "Se queda pequeña en horas punta y los utensilios necesitan renovarse. Se ensucia rápido aunque la limpian a diario. La nevera estaba siempre llena y desordenada."),
      ("Robo", "Me robaron una sudadera y una caja de tiras nasales. Puede pasar en cualquier hostel, no solo en el Maverick. <strong>Guarda siempre tus objetos de valor bajo llave</strong>."),
    ],
    "summary": [
      "<strong>El Maverick Central Market es para quien busca comodidad, en estancias cortas y largas.</strong> Se siente como tu propia habitación de residencia, cómodo incluso para un mes.",
      "No es un <a href=\"#section-2-hostel-one\">hostel de fiesta</a>, pero hay <strong>muchas ocasiones para conocer gente</strong>.",
      "<strong>Relación calidad-precio excepcional</strong>: <strong>en marzo pasé aquí 30 noches por 280 €</strong> (unos 9,33 € la noche). En mi comprobación del 14 de noviembre de 2026, las camas para fechas cercanas salían <strong>desde unos 10 €</strong>, y en temporada alta el precio sigue siendo justo para esta calidad.",
    ],
    "video": "videorreseña del Maverick Central Market",
    "groups": [
      ("Habitaciones, camas y descanso", "habitaciones y camas", [
        ("Camas de dormitorio con cortina", "<p>Los dormitorios son <strong>modernos, con cortinas en la cama y taquillas grandes</strong>, así que incluso una habitación llena es tranquila.</p>"),
        ("Noches tranquilas", "<p>Está en una <strong>calle pequeña del distrito IX</strong>, lejos de las calles de fiesta del VII. En mis 30 noches el ruido de la calle fue mínimo.</p>"),
        ("Precio real para largas estancias", "<p><strong>30 noches en marzo me costaron 280 €.</strong> Como base de nómada digital o para viajar despacio, no encontré mejor precio en el centro.</p>"),
      ]),
      ("Ambiente y vida social", "zonas comunes", [
        ("Sociable, pero no de fiesta", "<p>Como una residencia de estudiantes simpática. <strong>Es fácil conocer gente</strong> en las zonas comunes, sin gritos a las cuatro de la mañana.</p>"),
        ("A quién conocerás", "<p>Viajeros solos, huéspedes de larga estancia y teletrabajadores. Perfecto si quieres compañía por la noche y buen descanso después.</p>"),
      ]),
      ("Instalaciones, cocina y baños", "instalaciones", [
        ("Baños", "<p>Los baños compartidos y privados estaban <strong>limpios y cuidados</strong>, de lo mejor de mi estancia.</p>"),
        ("La cocina en la práctica", "<p>La cocina es <strong>pequeña en horas punta</strong>, los utensilios están gastados y la nevera siempre llena. Etiqueta tu comida.</p>"),
        ("Guarda tus cosas bajo llave", "<p>Me robaron una sudadera y una caja de tiras nasales. <strong>Usa las taquillas</strong> para todo lo que echarías de menos.</p>"),
      ]),
    ],
    "chips": [("yes", "Cortinas en la cama"), ("yes", "Terraza en la azotea"), ("yes", "Cocina compartida"), ("yes", "Recepción 24 h"), ("yes", "Consigna gratuita")],
  },
  {  # 2 Onefam
    "tag": "#2 Mejor hostel social para viajeros solos", "short": "El mejor para viajeros solos",
    "area": "Distrito VII, barrio judío",
    "checkin": "Check-in de 15:00 a 23:00, check-out hasta las 11:00", "rules": "Solo de 18 a 39 años, sin toque de queda",
    "specs": ["Actividades diarias gratis", "Rutas de bares", "18 a 39 años", "Deák tér"],
    "best_for": "Viajeros solos de 18 a 39 años que quieren hacer amigos al instante, actividades diarias y noches de fiesta.",
    "skip_if": "tienes más de 39, viajas en pareja y quieres intimidad, o te acuestas temprano.",
    "trust": "18 a 39 años",
    "transit": "Deák Ferenc tér (M1, M2, M3 y bus al aeropuerto 100E), unos 4 minutos a pie",
    "watch": "Más caro que la mayoría; solo de 18 a 39 años", "noise": "Animado hasta medianoche",
    "pros": [
      ("Mejor hostel de fiesta", "Juegos de beber en el bar, luego los bares en ruinas y turismo de día: te lo vas a pasar genial."),
      ("Actividades organizadas", "Onefam organiza actividades de día y de noche (rutas de bares, juegos de beber)."),
      ("Ubicación perfecta", "En pleno barrio judío, cerca de la parada del bus 100E al aeropuerto, de los monumentos y la vida nocturna."),
      ("Habitaciones geniales", "Habitaciones amplias con almacenamiento seguro y taquillas. Las camas dan intimidad y comodidad."),
      ("Poco ruido", "El nivel de ruido es aceptable, la fiesta suele calmarse entre las 23:00 y medianoche."),
    ],
    "cons": [
      ("Sin espacio junto a la cama", "En las literas no hay sitio para auriculares, cartera y móvil."),
      ("Problemas en la ducha", "La temperatura del agua varía y un sensor de movimiento mal colocado apaga la luz en la ducha."),
      ("Precio", "Más caro que otros hostels de Budapest. Por la vida social y la fiesta merece la pena pagar más."),
    ],
    "summary": [
      "<strong>El Onefam Budapest es la mejor opción si te gusta estar rodeado de gente, hacer amigos y salir de fiesta.</strong>",
      "Más caro que la mayoría de hostels de Budapest, pero vale lo que cuesta si buscas una estancia abierta y sociable. Ojo con el <strong>límite de edad de 18 a 39 años</strong>.",
    ],
    "video": "videorreseña del Onefam Budapest",
    "groups": [
      ("Habitaciones, camas y descanso", "habitaciones y camas", [
        ("Habitaciones amplias, almacenamiento seguro", "<p>Las habitaciones son <strong>amplias, con almacenamiento seguro y taquillas</strong>, y las camas dan intimidad y comodidad.</p>"),
        ("Sin estante junto a la cama", "<p>En la cama <strong>no hay dónde dejar el móvil, los auriculares o la cartera</strong>. Lleva una bolsita.</p>"),
        ("Cuándo llega la calma", "<p>La fiesta suele calmarse <strong>entre las 23:00 y medianoche</strong>, y luego el grupo se va a los bares en ruinas.</p>"),
      ]),
      ("Ambiente y vida social", "zonas comunes", [
        ("Amigos al instante", "<p>Si llegas solo y quieres hacer amigos rápido, <strong>este es el sitio</strong>. El personal incluye a todo el mundo.</p>"),
        ("Actividades de día y de noche", "<p>Actividades gratis de día, y por la noche juegos de beber y <strong>rutas de bares</strong> por el barrio judío.</p>"),
      ]),
      ("Instalaciones, baños y ubicación", "instalaciones", [
        ("Manías de la ducha", "<p>La temperatura del agua varía y <strong>un sensor de movimiento apaga la luz mientras te duchas</strong>.</p>"),
        ("Base en el barrio judío", "<p>A pocos minutos de <strong>Deák Ferenc tér y del bus 100E al aeropuerto</strong>, vuelves de los bares a pie.</p>"),
      ]),
    ],
    "chips": [("yes", "Actividades diarias gratis"), ("yes", "Bar del hostel"), ("yes", "Cocina 24 h"), ("yes", "Taquillas gratis"), ("no", "Solo de 18 a 39 años")],
  },
  {  # 3 Avenue
    "tag": "#3 Mejor hostel barato", "short": "La cama más barata",
    "area": "Distrito VI, Oktogon",
    "checkin": "Check-in de 14:00 a medianoche, check-out hasta las 11:00", "rules": "De 6 a 49 años, sin toque de queda",
    "specs": ["Desayuno gratis", "Cortinas en la cama", "Tranvía 24 h", "Oktogon"],
    "best_for": "Viajeros con poco presupuesto que buscan la cama más barata del centro, con desayuno gratis y cena barata.",
    "skip_if": "tienes el sueño ligero o buscas un ambiente sociable y cercano.",
    "trust": "Desayuno gratis",
    "transit": "Oktogon (M1 y los tranvías 4, 6 que circulan 24 h) en la puerta",
    "watch": "Cruce de tranvías ruidoso; lleva tapones", "noise": "Ruidoso (cruce de tranvías)",
    "pros": [
      ("Mejor relación calidad-precio", "En temporada baja había camas desde 8 € la noche, con desayuno gratis y cena con descuento."),
      ("Ahorras dinero", "La comida es cara en Hungría, con las comidas gratis y con descuento ahorras mucho."),
      ("Personal", "Atento, rápido y disponible las 24 horas."),
    ],
    "cons": [
      ("Calidad de vida", "El dormitorio de 10 camas donde dormí era regular en comodidad, intimidad y limpieza."),
      ("Sin candado gratis", "Las taquillas no incluyen candado, pero puedes comprar uno por unos 3 €."),
      ("Impersonal", "No hay ambiente social, trato personal ni actividades, salvo en el comedor."),
      ("Ruidoso", "Está junto a un gran cruce con tranvías. Lleva tapones."),
    ],
    "summary": [
      "<strong>El Avenue Hostel es la primera opción para viajeros con poco presupuesto que quieren ahorrar en alojamiento y comida en Budapest.</strong>",
      "Las camas empiezan <strong>en unos 8 €</strong>, con <strong>desayuno gratis</strong> y cena con descuento (en mi estancia, con un pequeño consumo mínimo en el bar). Con los precios altos de la comida en Hungría, esto marca la diferencia.",
      "No es lujo, pero es práctico y barato, una buena opción si vigilas tu presupuesto.",
      "📝 <strong>Nota de la redacción:</strong> el dormitorio \"con cortinas\" de 10 camas donde dormí y sus baños compartidos no eran buenos. Las otras habitaciones de 4, 8 y 12 camas son más bonitas, solo que más caras, así que el hostel merece mejor nota de la que le daría por mi habitación.",
    ],
    "video": "videorreseña del Avenue Hostel",
    "groups": [
      ("Habitaciones, camas y descanso", "habitaciones y camas", [
        ("Elige una habitación mejor", "<p>Mi habitación de 10 camas fue el punto débil. <strong>Las de 4, 8 y 12 camas son más bonitas</strong> y valen esos pocos euros extra.</p>"),
        ("Los tapones son obligatorios", "<p>Está en el <strong>cruce de Oktogon, con tranvías toda la noche</strong>. Si tienes el sueño ligero, mejor el Maverick o el Zen.</p>"),
        ("Candado para la taquilla", "<p>No incluye candado. <strong>Lleva uno</strong> o cómpralo en recepción por unos 3 €.</p>"),
      ]),
      ("Ambiente y vida social", "zonas comunes", [
        ("Práctico, no personal", "<p>No esperes actividades ni trato personalizado. <strong>La gente se conoce en el comedor.</strong></p>"),
        ("Para quién es", "<p>Estudiantes y mochileros de largo recorrido que miran cada euro y usan el hostel sobre todo para dormir y comer.</p>"),
      ]),
      ("Comida, instalaciones y ubicación", "instalaciones", [
        ("Desayuno gratis, cena barata", "<p>El <strong>desayuno gratis</strong> y la cena con descuento son el gran atractivo. Ahorras cada día más de lo que cuesta la cama.</p>"),
        ("Personal y transporte 24 h", "<p>La recepción abre 24 horas, y el <strong>M1 y los tranvías 4, 6 de 24 horas</strong> paran en la puerta.</p>"),
      ]),
    ],
    "chips": [("yes", "Desayuno gratis"), ("yes", "Cortinas en la cama"), ("yes", "Recepción 24 h"), ("yes", "Cocina compartida"), ("no", "Lleva candado")],
  },
  {  # 4 Flow
    "tag": "#4 Mejor para nómadas digitales", "short": "El mejor para nómadas digitales",
    "area": "Distrito IX, Gran Mercado Central",
    "checkin": "Check-in de 15:00 a medianoche, check-out hasta las 11:00", "rules": "Sin toque de queda",
    "specs": ["Espacio coworking", "Candado gratis", "Camas cápsula", "Gran Mercado"],
    "best_for": "Nómadas digitales y viajeros que quieren una sala apta para trabajar con portátil, camas cápsula y un ambiente sociable pero tranquilo.",
    "skip_if": "llevas equipaje pesado (3.ª planta, sin ascensor) o quieres baño propio.",
    "trust": "Espacio coworking",
    "transit": "Fővám tér (M4, tranvías 2, 47, 49) y Kálvin tér (M3, M4)",
    "watch": "Baños compartidos mixtos; 3.ª planta, sin ascensor", "noise": "Tranquilo",
    "pros": [
      ("Personal", "La recepción está disponible 24 horas, el personal es amable y atento."),
      ("Sociable", "Ambiente social, es fácil conocer a otros viajeros."),
      ("Camas geniales", "Cortina, enchufe, lámpara, estante pequeño y caja de almacenaje en la cama."),
      ("Almacenamiento seguro", "Incluye candado gratis."),
      ("Rincón de trabajo", "Sala común con rincón de trabajo apto para portátil."),
    ],
    "cons": [
      ("Baños", "Los baños son mixtos y compartidos, con poca intimidad."),
      ("Sin ascensor", "El hostel está en la 3.ª planta."),
      ("Higiene", "Había pelos en mi sábana, aunque estaba lavada. En general el hostel es higiénico."),
      ("Neveras llenas", "Desapareció parte de la comida que compré."),
      ("Habitaciones estrechas", "Apenas había espacio para moverse."),
    ],
    "summary": [
      "<strong>Flow Spaces combina la vida social de un hostel con la calma de un hotel</strong>, ideal si buscas el término medio.",
      "El ambiente recuerda a una residencia, una buena opción para viajeros con poco presupuesto que quieren una experiencia equilibrada. Las camas empiezan <strong>en unos 10 €</strong>.",
      "Con su ambiente amable, su <strong>zona de trabajo tranquila</strong> y su cocina bien equipada, merece la pena tenerlo en cuenta.",
    ],
    "groups": [
      ("Habitaciones, camas y descanso", "habitaciones y camas", [
        ("Cápsulas bien equipadas", "<p>Cada cama tiene <strong>cortina, enchufe, lámpara, estante pequeño y caja de almacenaje</strong>, con candado gratis.</p>"),
        ("Habitaciones estrechas", "<p>Las habitaciones son <strong>estrechas</strong>, apenas hay sitio cuando todos hacen la maleta.</p>"),
      ]),
      ("Ambiente y zona de trabajo", "zonas comunes", [
        ("Sala apta para portátil", "<p>La sala común tiene un <strong>rincón de trabajo de verdad</strong> y el hostel ofrece espacio coworking: aquí es donde mejor se teletrabaja.</p>"),
        ("Sociable pero equilibrado", "<p>Es fácil conocer gente sin noches de hostel de fiesta. Más residencia que cuartel general de rutas de bares.</p>"),
      ]),
      ("Instalaciones, baños y ubicación", "instalaciones", [
        ("Baños y escaleras", "<p>Los baños son <strong>mixtos y compartidos</strong>, y el hostel está en la <strong>3.ª planta sin ascensor</strong>.</p>"),
        ("Cocina y neveras", "<p>La cocina está bien equipada, pero las neveras se llenan y <strong>desapareció parte de mi comida</strong>. Etiqueta todo.</p>"),
        ("Junto al Gran Mercado", "<p>El <strong>Gran Mercado Central está a una manzana</strong> y el Danubio a pocos minutos a pie.</p>"),
      ]),
    ],
    "chips": [("yes", "Espacio coworking"), ("yes", "Candado gratis"), ("yes", "Cortinas en la cama"), ("yes", "Recepción 24 h"), ("no", "Sin ascensor (3.ª planta)")],
  },
  {  # 5 a&o
    "tag": "#5 Mejor hostel tipo hotel", "short": "El mejor para comodidad de hotel",
    "area": "Distrito VII, cerca de Oktogon",
    "checkin": "Check-in y check-out en la recepción 24 h", "rules": "Acepta familias y grupos",
    "specs": ["Habitaciones tranquilas", "Ducha genial", "Rincón de trabajo", "Habitaciones privadas"],
    "best_for": "Parejas, familias y cualquiera que prefiera una habitación tranquila, sencilla y limpia a la vida social.",
    "skip_if": "buscas un hostel sociable o no quieres pagar aparte la ropa de cama.",
    "trust": "Habitaciones privadas",
    "transit": "Oktogon (M1, tranvías 4, 6) y Vörösmarty utca (M1), a pocos minutos a pie",
    "watch": "Ropa de cama unos 3 € extra; lleva candado", "noise": "Tranquilo",
    "pros": [
      ("Habitaciones excelentes", "Habitación sencilla, tranquila y limpia, con una ducha fantástica."),
      ("Almacenamiento seguro", "En recepción me guardaron el portátil bajo llave sin problema."),
      ("Rincón de trabajo", "La sala común tiene un rincón de trabajo excelente apto para portátil."),
    ],
    "cons": [
      ("Ropa de cama y toalla", "No están incluidas, cuestan 1150 Ft (unos 3 €) extra."),
      ("\"Jaula\" de almacenaje", "El almacenaje de la habitación NO incluye candado."),
      ("Almohada sucia", "Podrían haber cambiado mi almohada, pero en general el hostel es higiénico."),
      ("Desayuno aburrido", "Desayuno de hotel normal por unos 8 € (opcional)."),
    ],
    "summary": [
      "<strong>El a&amp;o Budapest City es para viajeros con poco presupuesto que valoran más la comodidad y la calma que una vida social intensa.</strong>",
      "Las camas empiezan <strong>en unos 12 €</strong>, pero cuenta con el suplemento de la ropa de cama (unos 3 €).",
      "Pese a pequeños fallos como la almohada y el cargo por la ropa de cama, su precio y su comodidad lo hacen una buena opción si buscas un sitio tranquilo con zona de trabajo.",
    ],
    "groups": [
      ("Habitaciones, camas y descanso", "habitaciones y camas", [
        ("Tranquilo, limpio, sencillo", "<p><strong>Habitación sencilla, tranquila y limpia</strong>, con una ducha excelente. Más cerca de un hotel barato que de un hostel.</p>"),
        ("Cuenta los extras", "<p>La <strong>ropa de cama cuesta unos 3 €</strong> y necesitas tu propio candado para el almacenaje. Súmalo al precio.</p>"),
      ]),
      ("Ambiente y zona de trabajo", "zonas comunes", [
        ("Base tranquila, sin fiesta", "<p>Pocas actividades de hostel. Para quien quiere <strong>intimidad y descanso</strong>, parejas y familias.</p>"),
        ("Sala para el portátil", "<p>La sala común tiene un <strong>rincón de trabajo excelente apto para portátil</strong>.</p>"),
      ]),
      ("Instalaciones y ubicación", "instalaciones", [
        ("Almacenamiento seguro", "<p>La recepción <strong>guardó mi portátil bajo llave</strong> mientras estaba fuera.</p>"),
        ("Desayuno", "<p><strong>Desayuno de hotel opcional por unos 8 €</strong>. Correcto, nada especial.</p>"),
        ("Ubicación", "<p>En la calle Csengery, a pocos minutos a pie de <strong>Oktogon y la avenida Andrássy</strong>.</p>"),
      ]),
    ],
    "chips": [("yes", "Habitaciones tranquilas"), ("yes", "Habitaciones privadas"), ("yes", "Rincón de trabajo"), ("no", "Ropa de cama aparte (unos 3 €)"), ("no", "Lleva candado")],
  },
  {  # 6 Wombat's
    "tag": "#6 Mejor hostel de fiesta relajado", "short": "El mejor para una fiesta relajada",
    "area": "Distrito VI, calle Király",
    "checkin": "Check-in de 14:00 a 23:00, check-out hasta las 10:00", "rules": "Sin toque de queda",
    "specs": ["Dormitorios con baño", "Cortinas en la cama", "Bar del hostel", "Calle Király"],
    "best_for": "Mochileros que quieren un bar sociable y la vida nocturna en la puerta, pero también dormir bien.",
    "skip_if": "buscas la cama más barata o un hostel con carácter de verdad.",
    "trust": "Dormitorios con baño",
    "transit": "Deák Ferenc tér (M1, M2, M3 y bus al aeropuerto 100E), a 3 minutos a pie",
    "watch": "Caro para lo que ofrece", "noise": "Tranquilo dentro",
    "pros": [
      ("Sociable", "Ambiente social relajado, es fácil conocer gente."),
      ("No es ruidoso", "Tranquilo para ser un hostel de fiesta. Puedes descansar bien."),
      ("Personal", "Recepción 24 horas y consigna segura."),
    ],
    "cons": [
      ("Precio", "Los precios podrían ser más bajos. No sentí que el hostel ofreciera nada especial que los justificara."),
    ],
    "summary": [
      "<strong>El Wombat's City Hostel es el punto de encuentro de los viajeros jóvenes que vienen por la vida nocturna de Budapest</strong>, con energía juvenil y ambiente relajado, ideal como hostel de fiesta tranquilo.",
      "Más caro que la mayoría de hostels de Budapest. La ubicación es una gran ventaja, pero algunas cosas son normales: los baños, por ejemplo, están limpios, pero nada más.",
      "Lo mejor fue la gente: conocer viajeros interesantes de todo el mundo y salir de fiesta con ellos compensó con creces los detalles.",
    ],
    "groups": [
      ("Habitaciones, camas y descanso", "habitaciones y camas", [
        ("Habitaciones con baño", "<p>Según el hostel, todas las habitaciones tienen <strong>baño propio y aire acondicionado</strong>, y las camas de dormitorio tienen cortinas.</p>"),
        ("Mejor para dormir que para la fiesta", "<p>Para ser un hostel de fiesta, es <strong>tranquilo por la noche</strong>. Dormí bien.</p>"),
      ]),
      ("Ambiente y vida social", "zonas comunes", [
        ("Público de fiesta relajado", "<p>Es fácil conocer gente en el <strong>bar del hostel</strong>, y los bares del Gozsdu udvar están a unos pasos.</p>"),
        ("La gente lo es todo", "<p>El grupo internacional fue <strong>lo mejor de mi estancia</strong>.</p>"),
      ]),
      ("Instalaciones y ubicación", "instalaciones", [
        ("Normal pero limpio", "<p>Las instalaciones están <strong>limpias pero son normales</strong>; no lo reserves por el diseño.</p>"),
        ("Céntrico en la calle Király", "<p>A pocos minutos de <strong>Deák Ferenc tér</strong>, del bus 100E al aeropuerto y de la vida nocturna del barrio judío.</p>"),
      ]),
    ],
    "chips": [("yes", "Dormitorios con baño"), ("yes", "Aire acondicionado"), ("yes", "Bar del hostel"), ("yes", "Recepción 24 h"), ("yes", "Taquillas gratis")],
  },
  {  # 7 Zen
    "tag": "#7 Mejor hostel tranquilo y acogedor", "short": "El mejor para calma y ambiente hogareño",
    "area": "Distrito IX, Gran Mercado Central",
    "checkin": "Check-in de 14:00 a 21:00, check-out hasta las 11:00", "rules": "Horario de recepción limitado",
    "specs": ["Ambiente hogareño", "Hostel pequeño", "Té y café gratis", "Gran Mercado"],
    "best_for": "Introvertidos y viajeros lentos que buscan un sitio pequeño, acogedor y hogareño junto al Danubio.",
    "skip_if": "llegas tarde, necesitas taquilla o buscas un escritorio con enchufe.",
    "trust": "Check-in hasta las 21:00",
    "transit": "Fővám tér (M4, tranvías 2, 47, 49), junto al Gran Mercado Central",
    "watch": "Sin check-in tardío; sin almacenaje con llave", "noise": "Tranquilo",
    "pros": [
      ("Personal", "En mi estancia, un solo anfitrión llevaba todo el hostel: amable, atento y alegre. Gracias a él le doy un 9/10."),
      ("Sociable", "Podías empezar una conversación en cualquier sitio. El sofá del salón era ideal para charlar."),
      ("Como en casa", "Si te gusta el ambiente acogedor y hogareño, esto es el paraíso."),
    ],
    "cons": [
      ("Sin check-in 24 h", "El anfitrión se iba a las 21:00, y el check-in tardó mucho."),
      ("Falta de personal", "Una sola persona hacía malabares con demasiadas tareas; hacía falta al menos otro compañero."),
      ("No es seguro", "No había almacenaje con llave."),
      ("No apto para nómadas", "No hay rincón de trabajo con enchufes."),
    ],
    "summary": [
      "<strong>El Central Market Hall Zen Hostel es un refugio agradable si buscas un sitio pequeño y acogedor que se siente más casa que hostel.</strong>",
      "Los precios están algo por encima de la media para lo que ofrece, con camas en dormitorio <strong>desde unos 11 €</strong>. No es la mejor relación calidad-precio, pero si te importan el ambiente hogareño y estar junto al Gran Mercado, merece la pena.",
    ],
    "groups": [
      ("Habitaciones y descanso", "habitaciones y camas", [
        ("Pequeño y tranquilo", "<p>Un <strong>hostel pequeño con ambiente tranquilo y hogareño</strong>, sin público de fiesta.</p>"),
        ("Sin almacenaje con llave", "<p>En mi estancia <strong>no había almacenaje con llave</strong>. Lleva tus objetos de valor encima o elige otro hostel si esto te importa.</p>"),
      ]),
      ("Ambiente y salón", "zonas comunes", [
        ("Charlas en el salón", "<p>Todo el mundo acaba charlando en el <strong>sofá del salón</strong>. Juegos de mesa, té y café todo el día.</p>"),
        ("No es para teletrabajar", "<p>No hay escritorio con enchufe. <strong>Para nómadas digitales son mejores Flow Spaces o el Maverick.</strong></p>"),
      ]),
      ("Check-in y ubicación", "instalaciones", [
        ("Llega antes de las 21:00", "<p>El check-in es <strong>de 14:00 a 21:00</strong> y el horario de recepción es limitado. ¿Llegas en un vuelo tarde? Reserva en otro sitio.</p>"),
        ("Junto al Gran Mercado", "<p>En el Vámház körút, <strong>junto al Gran Mercado Central y el puente de la Libertad</strong>, con M4 y tranvía 2 en Fővám tér.</p>"),
      ]),
    ],
    "chips": [("yes", "Ambiente hogareño"), ("yes", "Té y café gratis"), ("yes", "Junto al Gran Mercado"), ("no", "Check-in hasta las 21:00"), ("no", "Sin almacenaje con llave")],
  },
  {  # 8 Adagio
    "tag": "#8 Mejor ubicación para hacer turismo", "short": "El mejor para hacer turismo",
    "area": "Distrito VI, avenida Andrássy",
    "checkin": "Check-in de 15:00 a medianoche, check-out hasta las 10:00", "rules": "Sin toque de queda",
    "specs": ["Vistas a la basílica", "Baños privados", "Té y café gratis", "Avenida Andrássy"],
    "best_for": "Turistas que quieren una cama tranquila y limpia al inicio de la avenida Andrássy, a unos pasos de la basílica de San Esteban.",
    "skip_if": "buscas un hostel sociable o eres sensible al ruido del tráfico.",
    "trust": "A unos pasos de la basílica",
    "transit": "Bajcsy-Zsilinszky út (M1) en la puerta, Deák Ferenc tér (M1, M2, M3) a un paseo corto",
    "watch": "Ruido de tráfico; sin ascensor (1.ª planta)", "noise": "Ruido de tráfico",
    "pros": [
      ("Baño genial", "Baño privado excelente y limpio."),
      ("Ubicación excelente", "Con vistas a la basílica de San Esteban."),
      ("Tranquilo", "No tan concurrido como otros hostels, así que hay más intimidad."),
    ],
    "cons": [
      ("Ruidoso", "En mi habitación había mucho ruido por el tráfico."),
      ("Sin ascensor", "El hostel está en la primera planta."),
      ("Impersonal", "No hay ambiente social ni trato personal."),
    ],
    "summary": [
      "<strong>El Adagio 2.0 es tu sitio si lo más importante es dormir bien en una habitación limpia y cómoda.</strong>",
      "No tiene nada especial, pero hace bien lo básico: una buena opción para un alojamiento barato y minimalista en una ubicación fantástica.",
      "Tampoco castiga tu bolsillo: para fechas cercanas, las camas en dormitorio empiezan <strong>en unos 11 €</strong> y las habitaciones privadas <strong>en unos 22 €</strong>.",
    ],
    "groups": [
      ("Habitaciones y descanso", "habitaciones y camas", [
        ("Habitaciones limpias, baño genial", "<p>Mi habitación tenía un <strong>baño privado excelente y limpio</strong>. Hay dormitorios y habitaciones dobles con baño.</p>"),
        ("Ruido de tráfico", "<p>La avenida Andrássy es una vía principal y <strong>mi habitación era ruidosa por el tráfico</strong>. Lleva tapones o pide una habitación interior.</p>"),
      ]),
      ("Ambiente", "zonas comunes", [
        ("Tranquilo, no sociable", "<p><strong>No hay vida social ni trato personal.</strong> Una base tranquila para hacer turismo, no para conocer gente.</p>"),
      ]),
      ("Instalaciones y ubicación", "instalaciones", [
        ("Cocina, té y café", "<p>Según el hostel, los huéspedes pueden usar <strong>cocinas totalmente equipadas</strong>, con té, café y ropa de cama gratis.</p>"),
        ("Primera planta, sin ascensor", "<p>En la <strong>primera planta de un palacio, sin ascensor</strong>, un tramo de escaleras.</p>"),
        ("Imbatible para los monumentos", "<p>Al <strong>inicio de la avenida Andrássy</strong>, a pocos minutos a pie de la basílica de San Esteban, la Ópera y Deák Ferenc tér.</p>"),
      ]),
    ],
    "chips": [("yes", "Vistas a la basílica"), ("yes", "Cocina compartida"), ("yes", "Recepción 24 h"), ("yes", "Té y café gratis"), ("no", "Sin ascensor (1.ª planta)")],
  },
  {  # 9 Das Nest
    "tag": "#9 Mejor hostel pequeño y acogedor", "short": "El mejor pequeño y acogedor",
    "area": "Distrito VII, barrio judío",
    "checkin": "Check-in de 12:00 a 23:00, check-out hasta las 11:00", "rules": "Sin toque de queda",
    "specs": ["Loft acogedor", "Consejos locales", "Cocina compartida", "Barrio judío"],
    "best_for": "Mochileros solos y grupos pequeños que buscan un hostel acogedor, tipo apartamento, con anfitriones amables en el barrio de fiesta.",
    "skip_if": "quieres pagar con tarjeta, necesitas acceso adaptado o quieres silencio también el fin de semana.",
    "trust": "Privadas desde 17 €",
    "transit": "Wesselényi utca (tranvías 4, 6) y Blaha Lujza tér (M2), a pocos minutos a pie",
    "watch": "Solo efectivo en mi estancia; ruido de calle el fin de semana", "noise": "Ruido de calle el fin de semana",
    "pros": [
      ("Ubicación céntrica", "En el corazón de Budapest, cerca de los principales monumentos y la vida nocturna."),
      ("Personal amable", "Simpático, atento y con recomendaciones locales geniales."),
      ("Ambiente acogedor", "Un lugar acogedor e íntimo, ideal para conocer gente."),
      ("Cocina bien equipada", "Cocina totalmente equipada para los huéspedes."),
      ("Contactos locales", "Consejos de bares, restaurantes y festivales que no encontrarías por tu cuenta."),
    ],
    "cons": [
      ("Solo efectivo", "En mi estancia no aceptaban tarjeta, solo efectivo."),
      ("Posible ruido", "Por la animada vida nocturna puede haber ruido por la noche."),
      ("Accesibilidad limitada", "No es accesible para todas las personas con discapacidad."),
    ],
    "summary": [
      "<strong>Das Nest es ideal si buscas alojamiento céntrico en Budapest con un ambiente acogedor y sociable.</strong> Todo gira en torno al trato amable, el ambiente relajado y los buenos consejos locales.",
      "En mi estancia faltaban comodidades como el pago con tarjeta, pero lo compensa con trato personal y una gran ubicación. Para quien valora más la comodidad asequible y conocer gente que el lujo.",
      "Habitaciones: dormitorios mixtos o solo para mujeres de 4 o 6 camas y una habitación doble privada. Cama en dormitorio <strong>desde unos 15 €</strong>.",
    ],
    "groups": [
      ("Habitaciones y descanso", "habitaciones y camas", [
        ("Dormitorios pequeños", "<p><strong>Dormitorios mixtos o solo para mujeres de 4 y 6 camas</strong> y una habitación doble privada. Lo bastante pequeño para ser personal.</p>"),
        ("Ruido el fin de semana", "<p>Está en el barrio de fiesta, así que <strong>si tienes el sueño ligero, lleva tapones</strong> para el viernes y el sábado.</p>"),
      ]),
      ("Ambiente y vida social", "zonas comunes", [
        ("Como el piso de un amigo", "<p>El hostel se describe como un <strong>loft renovado en el ático</strong>, y es exactamente eso: íntimo y sociable.</p>"),
        ("Anfitriones con consejos locales", "<p>El personal me dio <strong>consejos de bares, restaurantes y festivales</strong> que no aparecían en ninguna guía.</p>"),
      ]),
      ("Instalaciones y pago", "instalaciones", [
        ("Cocina", "<p><strong>Cocina compartida totalmente equipada</strong>, buena para ahorrar.</p>"),
        ("Lleva efectivo", "<p>En mi estancia <strong>solo aceptaban efectivo</strong>. Revisa las condiciones de la reserva y, por si acaso, lleva florines.</p>"),
      ]),
    ],
    "chips": [("yes", "Ambiente acogedor"), ("yes", "Cocina compartida"), ("yes", "Taquillas gratis"), ("yes", "Dormitorios solo para mujeres"), ("no", "Solo efectivo (en mi estancia)")],
  },
  {  # 10 The Hive
    "tag": "#10 Mejor gran hostel de fiesta", "short": "El hostel de fiesta más grande",
    "area": "Distrito VII, barrio judío",
    "checkin": "Check-in de 15:00 a medianoche, check-out hasta las 11:00", "rules": "Solo mayores de 18, sin toque de queda",
    "specs": ["Bar en la azotea", "Rutas de bares diarias", "Solo +18", "Barrio judío"],
    "best_for": "Grupos mayores de 18 y fiesteros solos que quieren un hostel de fiesta grande y ruidoso con bar en la azotea en el barrio de los bares en ruinas.",
    "skip_if": "tienes el sueño ligero, madrugas o quieres cortinas en la cama.",
    "trust": "Solo +18",
    "transit": "Astoria (M2) y Deák Ferenc tér (M1, M2, M3), a pocos minutos a pie",
    "watch": "Ruido del club de abajo; sin cortinas en la cama", "noise": "Ruidoso (hostel de fiesta)",
    "why": [
      ("Gran hostel de fiesta", "Según el hostel, más de 300 camas desde 2015, con rutas de bares diarias, rutas con bingo, SPArties y barcos de fiesta."),
      ("Bar en la azotea", "Bar en la azotea propio para huéspedes, con happy hour diario de 16:00 a 19:00."),
      ("Ubicación", "En el barrio de los bares en ruinas, a un paseo corto del Gozsdu udvar y del Szimpla Kert."),
      ("Práctico", "Recepción 24 h, taquillas, pago en efectivo o con tarjeta."),
    ],
    "skip": [
      ("Ruido", "El propio hostel advierte a quienes tienen el sueño ligero y a los madrugadores; los huéspedes mencionan el ruido del club de abajo."),
      ("Sin cortinas en la cama", "Las cortinas en las camas son una petición frecuente de los huéspedes."),
      ("Wi-Fi", "El wifi débil es una queja recurrente de los huéspedes."),
      ("Límite de edad", "Solo mayores de 18."),
    ],
    "summary": [
      "<strong>The Hive es el gran hostel de fiesta ruidoso de Budapest.</strong> Con más de 300 camas, bar en la azotea y rutas de bares diarias, está pensado para las noches, no para madrugar.",
      "Lo incluí como alternativa de fiesta al Onefam: los datos aquí vienen de la información del propio hostel y de las opiniones de huéspedes, comprobados el 14 de noviembre de 2026. Las camas en dormitorio empiezan <strong>en unos 13 €</strong>.",
    ],
    "chips": [("yes", "Bar en la azotea"), ("yes", "Rutas de bares diarias"), ("yes", "Recepción 24 h"), ("yes", "Taquillas gratis"), ("no", "Solo +18")],
  },
]

HOSTELS = build(_T, floor_label="1.ª planta")


def _areas(H, a):
    return (
        '<h3>Distrito VII (barrio judío): para la vida nocturna</h3>\n'
        '<p>Aquí están los bares en ruinas, el Gozsdu udvar y el Szimpla Kert, y aquí están también %s, %s y %s. Genial para salir, <strong>lo peor el fin de semana si tienes el sueño ligero</strong>.</p>\n'
        '<h3>Distrito VI (calle Király, avenida Andrássy, Oktogon): céntrico y bien conectado</h3>\n'
        '<p>%s, %s y %s están en los ejes principales, junto al M1 y los tranvías 4, 6 de 24 horas. Vas a pie a todas partes, pero el <strong>tráfico de las avenidas</strong> puede ser ruidoso.</p>\n'
        '<h3>Distrito IX (Gran Mercado Central): más tranquilo, junto al río</h3>\n'
        '<p>%s, %s y %s están junto al Gran Mercado Central, a pocos minutos del Danubio. Es lo que yo elegiría si quieres <strong>noches más tranquilas</strong> y llegar al centro a pie.</p>\n'
        '<p>¿Llegas en avión? Aquí tienes <a href="/es/aeropuerto-budapest-al-centro">cómo ir del aeropuerto al centro</a>: el bus 100E para en Deák Ferenc tér, a un paseo corto de los hostels de los distritos VI y VII.</p>'
    ) % (a(H[2]), a(H[9]), a(H[10]), a(H[6]), a(H[8]), a(H[3]), a(H[1]), a(H[4]), a(H[7]))


UI = {
    "url": URL, "home": "Inicio", "home_url": "https://www.budapestadventures.com/es", "about_url": "https://www.budapestadventures.com/es/about",
    "title": "Los 10 mejores hostels de Budapest en 2026 (dormí en 9)",
    "h1_main": "Los 10 mejores hostels de Budapest en 2026", "h1_muted": "(dormí en 9)",
    "meta": "Dormí en 9 de los mejores hostels de Budapest, 30 noches en el Maverick. Camas desde 8 €: los mejores hostels de fiesta, tranquilos, baratos y para nómadas, por barrio.",
    "breadcrumb": "Mejores hostels de Budapest", "kicker_badge": "Comparativa de hostels 2026",
    "author_line": 'Por <a href="/es/about" target="_blank">Adam Dimitrov</a>, fundador y probador en Budapest',
    "author_role": "Dormí en 9 de 10 • Fotos y videorreseñas propias",
    "last_updated": "<strong>Actualizado</strong>: 14 de noviembre de 2026",
    "job_title": "Fundador y probador en Budapest",
    "intro": (
        '<p>Un mal hostel en Budapest no te cuesta dinero, te cuesta sueño. Las camas en dormitorio del centro cuestan <strong>de 8 a 15 €</strong> la noche, '
        'pero un hostel de fiesta en el barrio judío y un hostel cápsula tranquilo junto al Gran Mercado Central son dos viajes totalmente distintos.</p>\n'
        '<p>He <strong>dormido yo mismo en 9 de los 10 hostels de abajo</strong>, en el Maverick por ejemplo <strong>30 noches por 280 €</strong>, y los he comparado lado a lado en lo que importa al reservar: '
        'ruido de noche, intimidad en la cama, baños, cocina, límite de edad, el tipo de gente y el precio real por noche. '
        'The Hive es la única opción de fiesta donde no dormí, así que solo incluye datos comprobados, sin la insignia de \"probado\".</p>\n'
        '<p>Precios y valoraciones comprobados el <strong>%s</strong>. Usa los filtros para saltar directamente a los hostels de fiesta, tranquilos, baratos, con habitación privada o para nómadas digitales.</p>\n' % CHECKED),
    "filters": [("party", "🎉 Social y fiesta"), ("quiet", "😴 Dormir tranquilo"), ("budget", "💶 Menos de 11 €"),
                ("private", "🛏️ Habitaciones privadas"), ("nomad", "💻 Nómadas digitales"), ("kitchen", "🍳 Cocina compartida")],
    "district_fmt": "Distrito %s", "decimal": ",", "thousands": ".", "k": "k",
    "tested_chip": "✓ Probado en persona",
    "best_for_card": "Ideal para:", "best_for_summary": "Ideal para:", "skip_if": "Evítalo si",
    "from_eur": "desde %d €", "eur": "%d €", "card_psub": "Cama/noche • 14/11/2026",
    "card_btn": "Precios y fechas →", "read_review": "Reseña ↓",
    "pros": "Ventajas:", "cons": "Inconvenientes:", "why": "Por qué elegirlo:", "why_skip": "Por qué no:",
    "video": "Vídeo:", "watch_my": "Mira mi",
    "summary_title": "Veredicto y valoración", "summary_pill": "Resumen",
    "swipe_photos": "%d fotos, desliza →", "one_photo": "1 foto", "no_photo": "Experiencia propia",
    "photo_alt": "%s: %s, foto propia", "prev_photo": "Foto anterior", "next_photo": "Foto siguiente",
    "buy_badge": "Precios y disponibilidad en directo", "buy_sub": "Cama en dormitorio por noche • Comprobado: " + CHECKED,
    "address_perk": "Dirección: <strong>%s</strong>", "privates_perk": "Habitación privada <strong>desde %d €</strong>",
    "buy_cta": "Fechas y precios", "buy_trust": "El precio cambia según la fecha; el precio final se muestra antes de pagar",
    "qf": {"title": "Datos clave: %s", "address": "Dirección", "dorm": "Cama en dormitorio", "transit": "Cómo llegar", "checkin": "Check-in",
           "rules": "Normas", "ratings": "Valoraciones", "watch": "A tener en cuenta",
           "dorm_fmt": "desde %d € la noche (comprobado: " + CHECKED + ")", "priv_fmt": ", habitación privada desde %d €",
           "hw_fmt": "Hostelworld %s/10 (%s opiniones)", "bk_fmt": ", Booking.com %s/10 (%s opiniones)"},
    "breakdown_h2": "Reseñas detalladas: los 10 mejores hostels de Budapest",
    "breakdown_sub": "Dormí en 9, 1 opción de fiesta con datos comprobados • Haz clic para abrir o cerrar",
    "picks": [
        ("En general", 1, "Sociable sin ruido de fiesta, camas con cortina, baños geniales y 280 € por mis 30 noches."),
        ("Viajeros solos (18 a 39 años)", 2, "Con las actividades diarias gratis y las rutas de bares, hacer amigos está chupado. ¿Más de 39? Elige el Maverick o el Wombat's."),
        ("Fiesta", 10, lambda H: 'La opción grande y ruidosa con bar en la azotea en el barrio de los bares en ruinas. ¿Algo más tranquilo? <a href="#%s">%s</a>.' % (H[6]['id'], H[6]['name'])),
        ("La cama más barata", 3, "Cama desde unos 8 € con desayuno gratis. Lleva tapones: está en un cruce de tranvías."),
        ("Dormir tranquilo", 1, lambda H: 'Calle tranquila en el distrito IX. También tranquilos: <a href="#%s">%s</a> y <a href="#%s">%s</a>.' % (H[7]['id'], H[7]['name'], H[5]['id'], H[5]['name'])),
        ("Nómadas digitales", 4, "Sala apta para portátil y espacio coworking. Para estancias largas, la alternativa es el Maverick."),
        ("Parejas y familias", 5, "Habitaciones sencillas, tranquilas y limpias con opción privada. Cuenta unos 3 € por la ropa de cama."),
        ("Turismo", 8, "Al inicio de la avenida Andrássy, a pocos minutos de la basílica de San Esteban y de Deák tér."),
        ("Pequeño y acogedor", 9, "Como el loft de un amigo en el barrio judío, con anfitriones llenos de consejos locales."),
    ],
    "sections": {
        "picks_badge": "Elección rápida", "picks_h2": "El mejor hostel de Budapest según tu tipo de viaje",
        "picks_sub": "La respuesta corta para cada tipo de viaje, según mis propias estancias",
        "table_badge": "Lado a lado", "table_h2": "Hostels de Budapest comparados: precio, ruido y trampas",
        "table_sub": "Precios de dormitorio y notas de Hostelworld comprobados el " + CHECKED + ". Ruido y trampas según mis propias estancias (The Hive: opiniones de huéspedes).",
        "table_cols": ["Hostel", "Ideal para", "Barrio", "Cama en dormitorio", "Hostelworld", "Ruido de noche", "A tener en cuenta"],
        "areas_badge": "Barrios", "areas_h2": "Dónde alojarse en un hostel en Budapest",
        "areas_sub": "Los 10 están en el centro de Pest. El distrito decide lo ruidosas que serán tus noches.",
        "areas_body": _areas,
        "map_h2": "Mapa: los mejores hostels de Budapest",
        "map_sub": 'Los hostels de la lista en los distritos del centro (<a href="/es/tours-a-pie-budapest">distrito VII, barrio judío</a>, distrito V, distrito VI Terézváros y distrito IX Ferencváros)',
        "types_h2": "Tipos de hostel en Budapest",
    },
    "faq": [
        ("¿Cuál es el mejor hostel de Budapest?",
         "<p>En general, mi favorito es el <strong>Maverick Central Market</strong>: sociable sin ruido de fiesta, camas con cortina, baños geniales y un precio real para estancias largas (en marzo pagué 280 € por 30 noches). "
         "Para una estancia sociable, la opción es el <strong>Onefam Budapest</strong>, y para la cama más barata, el <strong>Avenue Hostel</strong>.</p>"),
        ("¿Cuáles son los mejores hostels de Budapest para viajeros solos?",
         "<p>En el <strong>Onefam Budapest</strong> es donde más fácil se hacen amigos gracias a las actividades gratis y las rutas de bares, pero solo admite a huéspedes <strong>de 18 a 39 años</strong>. "
         "¿Tienes más de 39 o quieres dormir más? El <strong>Maverick Central Market</strong> y el <strong>Wombat's City Hostel</strong> son sociables sin obligarte a salir de fiesta.</p>"),
        ("¿Cuáles son los mejores hostels de fiesta de Budapest?",
         "<p>El <strong>Onefam Budapest</strong> (sociable, rutas de bares diarias), <strong>The Hive Party Hostel</strong> (el grande y ruidoso, con bar en la azotea, solo mayores de 18) y el "
         "<strong>Wombat's City Hostel</strong> (fiesta relajada, se puede dormir). Los tres están a un paseo corto de los bares en ruinas del barrio judío.</p>"),
        ("¿En qué hostel de Budapest se duerme más tranquilo?",
         "<p>En el <strong>Maverick Central Market</strong> (calle tranquila), el <strong>Central Market Hall Zen Hostel</strong> (pequeño y hogareño) y el <strong>a&amp;o Budapest City</strong> (habitaciones tipo hotel). "
         "Si tienes el sueño ligero, evita el Avenue Hostel: está en el cruce de tranvías de Oktogon.</p>"),
        ("¿Cuánto cuesta un hostel en Budapest?",
         "<p>El 14 de noviembre de 2026, las camas en dormitorio de estos 10 hostels empezaban <strong>en unos 8 a 15 €</strong> la noche (Avenue desde 8 €, Das Nest desde 15 €), y las habitaciones privadas en unos 17 a 28 €. "
         "Es más caro <strong>los fines de semana, en verano (de mayo a septiembre), durante el Sziget Festival en agosto, los mercados de Navidad y Nochevieja</strong>.</p>"),
        ("¿En qué barrio conviene reservar un hostel en Budapest?",
         "<p>En el <strong>distrito VII (barrio judío)</strong> por la vida nocturna, en el <strong>distrito VI</strong> (calle Király, avenida Andrássy) para una base céntrica y bien conectada, "
         "y en el <strong>distrito IX</strong>, junto al Gran Mercado Central, para noches más tranquilas cerca del Danubio.</p>"),
        ("¿Tienen límite de edad los hostels de Budapest?",
         "<p>Algunos sí. Según sus normas, el <strong>Onefam Budapest admite a huéspedes de 18 a 39 años</strong>, <strong>The Hive es solo para mayores de 18</strong> y el <strong>Avenue Hostel admite de 6 a 49 años</strong>. Revisa las normas antes de reservar.</p>"),
        ("¿Son seguros los hostels de Budapest?",
         "<p>En general sí, pero hay pequeños robos: en un hostel me robaron una sudadera y una caja de tiras nasales. <strong>Guarda tus objetos de valor en la taquilla</strong> y lleva candado, porque algunos hostels "
         "(Avenue, a&amp;o) no lo dan. Flow Spaces te da uno gratis.</p>"),
        ("¿Con qué criterios elegiste los mejores hostels de Budapest?",
         "<p>Dormí en 9 de los 10 hostels y los valoré según: <strong>ubicación, ruido de noche, limpieza, comodidad e intimidad de la cama, instalaciones, el tipo de gente y el precio</strong>. "
         "The Hive aparece como opción de fiesta con datos comprobados y opiniones de huéspedes, sin insignia de probado.</p>"),
        ("¿Qué llevar a un hostel?",
         "<p><strong>Imprescindible:</strong> tapones y antifaz. <strong>Básicos:</strong> chanclas, pijama, cargador del móvil, toallitas, desodorante, cepillo y pasta de dientes. "
         "<strong>Opcional</strong> (mira qué ofrece el hostel): toalla, candado, champú y gel.</p>"),
    ],
    "sticky_trust": "Cama/noche", "sticky_cta": "Precios →", "sheet_label": "Ir a un hostel de Budapest",
    "toc_breakdown": "Reseñas detalladas (10 hostels)",
    "szimpla_alt": "El bar en ruinas Szimpla Kert, a un paseo corto del The Hive en la calle Dob",
    "szimpla_pill": "Szimpla Kert, a 3 min a pie",
    "collapse_label": "Cerrar", "expand_label": "Abrir reseña",
    "price_range": "Cama desde %d €",
}
