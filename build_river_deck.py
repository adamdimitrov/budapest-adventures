import os

cruises = [
    {
        "rank": 1,
        "badge": "🏆 #1 Best Overall",
        "badge_cls": "bpa-gold",
        "kicker": "Legenda City Cruises • 📍 Dock 7 (Vigadó tér)",
        "title": "Budapest Day or Night River Cruise With Audio Guide in 30 Languages & Welcome Drink",
        "url": "https://legenda.hu/en?partner=38585",
        "score": "4.4 / 5.0",
        "stars": "★★★★☆",
        "reviews": "(12,810+ Reviews)",
        "channels": [
            ("gyg", "4.5", "(7,540+)"),
            ("viator", "4.3", "(3,340+)"),
            ("ta", "4.3", "(1,930+)")
        ],
        "specs": [
            "🥂 1 Welcome Drink",
            "🎧 30-Language Audio Guide",
            "⏱️ 60–70 Mins",
            "🏛️ Full Danube Circuit"
        ],
        "best_for": "First-time visitors wanting the gold-standard sightseeing route, interior anti-glare lighting for night photos, and a complimentary champagne, wine, or beer.",
        "price": "€20–25",
        "price_sub": "including welcome drink",
        "anchor": "#1-legenda",
        "hero_img": "68f3738fe72bf6e25526e991_best-budapest-river-cruises-legenda-sightseeing-cruise-00025.avif",
        "more_imgs": [
            "68f3728df887e78f3ca120db_best-budapest-river-cruises-legenda-sightseeing-cruise-00006.avif",
            "68f3738e03a6297dac92826a_best-budapest-river-cruises-legenda-sightseeing-cruise-00012.avif",
            "68f3738fb705f76f17608252_best-budapest-river-cruises-legenda-sightseeing-cruise-00017.avif",
            "68f3738f900b7b793aca6056_best-budapest-river-cruises-legenda-sightseeing-cruise-00024.avif",
            "68f3738ff7f68a9d80c0c037_best-budapest-river-cruises-legenda-sightseeing-cruise-00016.avif",
            "68f3738f025fb2e82c581a73_best-budapest-river-cruises-legenda-sightseeing-cruise-00013.avif",
            "68f3738f8abeb45efd6208e7_best-budapest-river-cruises-legenda-sightseeing-cruise-00022.avif",
            "68f3738f03a6297dac928295_best-budapest-river-cruises-legenda-sightseeing-cruise-00014.avif",
            "68f3738fbe24ee2467baeb41_best-budapest-river-cruises-legenda-sightseeing-cruise-00020.avif",
            "68f3738f6f2fe00689714d66_best-budapest-river-cruises-legenda-sightseeing-cruise-00018.avif",
            "68f3738fb13a0d71ea3326d2_best-budapest-river-cruises-legenda-sightseeing-cruise-00001.avif",
            "68f3738fb3ceaa52d1d63c11_best-budapest-river-cruises-legenda-sightseeing-cruise-00009.avif"
        ]
    },
    {
        "rank": 2,
        "badge": "🥂 #2 Best Unlimited Drinks",
        "badge_cls": "bpa-emerald",
        "kicker": "Rubin Group • 📍 Margaret Bridge Dock",
        "title": "Budapest Night Cruise with Unlimited Prosecco, Aperol, Beer, Spritzer or Lemonade",
        "url": "https://www.getyourguide.com/budapest-l29/budapest-unlimited-prosecco-beer-and-aperol-spritz-cruise-t416276/?partner_id=YS414AJ&utm_medium=online_publisher&cmp=budapest-river-cruises-comparison-list-unlimited-drinks-rubin-group&mkt_cmp=true",
        "score": "4.8 / 5.0",
        "stars": "★★★★★",
        "reviews": "(36,890+ Reviews)",
        "channels": [
            ("gyg", "4.8", "(31,980+)"),
            ("viator", "4.6", "(3,080+)"),
            ("ta", "4.6", "(1,830+)")
        ],
        "specs": [
            "🍾 Unlimited Prosecco & Drinks",
            "⏱️ 75–85 Mins",
            "🎵 Upbeat Cocktail Vibe",
            "🌇 Open-Air Top Deck"
        ],
        "best_for": "Couples, friends, and social travelers looking for an upbeat evening cruise with bottomless prosecco, spritzers, and illuminated Parliament views.",
        "price": "€25",
        "price_sub": "unlimited drinks included",
        "anchor": "#2-rubingroup",
        "hero_img": "650beeaa6847525facb1a507_best-unlimited-prosecco-cruises-hero.webp",
        "more_imgs": [
            "63b858ea56f82257ea9e0c70_Budapest-river-cruises-portum-16.webp",
            "63b858e8f731d90165d271cc_Budapest-river-cruises-portum-11.webp",
            "63b858e9803ea5e532e13df1_Budapest-river-cruises-portum-15.webp",
            "63b858e8a4e49cb177974356_Budapest-river-cruises-portum-14.webp",
            "63b858eda4b537601bf3ceab_Budapest-river-cruises-portum-21.webp",
            "64946bd848dfb642de48fcfb_16-rubin-group.webp",
            "63b858e92be2896fd573cf19_Budapest-river-cruises-portum-10.webp",
            "63b858eb6b6209525005c772_Budapest-river-cruises-portum-17.webp"
        ]
    },
    {
        "rank": 3,
        "badge": "⚓ #3 Best Historic Steamer",
        "badge_cls": "bpa-blue",
        "kicker": "Dunai Sétahajózási (Kisfaludy) • 📍 Dock 10 (Erzsébet Bridge)",
        "title": "Budapest River Cruise on 19th-Century Authentic Paddle Steam Boat",
        "url": "https://www.getyourguide.com/budapest-l29/budapest-city-lights-evening-cruise-with-audio-guide-t437737/?partner_id=YS414AJ&utm_medium=online_publisher&cmp=article-river-cruises-comparison-list-duna-cruises-steamer&mkt_cmp=true",
        "score": "4.6 / 5.0",
        "stars": "★★★★★",
        "reviews": "(10,950+ Reviews)",
        "channels": [
            ("gyg", "4.7", "(5,380+)"),
            ("viator", "4.6", "(290+)"),
            ("ta", "4.6", "(190+)")
        ],
        "specs": [
            "🛳️ 1847 Paddle Steamer Replica",
            "🥂 Optional Welcome Drink",
            "🎧 English Audio Guide",
            "🏛️ Onboard Museum"
        ],
        "best_for": "History buffs and photographers wanting to sail aboard a faithful 19th-century paddle steamer replica with 360° open bow views.",
        "price": "€10–32",
        "price_sub": "by selected ticket tier",
        "anchor": "#4-kisfaludy-historic-cruise",
        "hero_img": "64eb8e0e233b7bcba36b79ca_Kisdalufy%20historic%20paddle%20steam%20cruise%20(15).webp",
        "more_imgs": [
            "64eb8e07a2dc265f519b2a83_Kisdalufy%20historic%20paddle%20steam%20cruise%20(7).webp",
            "64eb8e09dbce9b580c818930_Kisdalufy%20historic%20paddle%20steam%20cruise%20(10).webp",
            "64eda40ea110f471e61d0537_Kisdalufy%20historic%20paddle%20steam%20cruise%20(18).avif",
            "64eb8e07233b7bcba36b7081_Kisdalufy%20historic%20paddle%20steam%20cruise%20(6).webp",
            "64eb8e08627363a3b67f4967_Kisdalufy%20historic%20paddle%20steam%20cruise%20(8).webp",
            "64eb8e0db7f9f26521c0cca8_Kisdalufy%20historic%20paddle%20steam%20cruise%20(13).webp",
            "64eda0f72a95bec78d110945_Kisdalufy%20historic%20paddle%20steam%20cruise%20(16).webp",
            "64eb8e060f9044a1a9e4900c_Kisdalufy%20historic%20paddle%20steam%20cruise%20(5).webp"
        ]
    },
    {
        "rank": 4,
        "badge": "💰 #4 Best Budget Value",
        "badge_cls": "bpa-emerald",
        "kicker": "Portum Lines Cruising • 📍 Dock 42 (Szent István Park)",
        "title": "Budapest Sightseeing Cruise with Welcome Drink (Prosecco or Cocktail)",
        "url": "https://www.getyourguide.com/budapest-l29/budapest-boat-cruise-cocktail-t73250/?partner_id=YS414AJ&utm_medium=online_publisher&cmp=article-river-cruises-comparison-list-portum&mkt_cmp=true",
        "score": "4.6 / 5.0",
        "stars": "★★★★★",
        "reviews": "(44,000+ Reviews)",
        "channels": [
            ("gyg", "4.6", "(40,400+)"),
            ("viator", "4.1", "(2,340+)"),
            ("ta", "4.1", "(1,260+)")
        ],
        "specs": [
            "🥂 1 Welcome Drink",
            "⏱️ 60 Mins",
            "🛳️ Modern Double-Decker",
            "💸 40% Less Than Legenda"
        ],
        "best_for": "Budget-conscious travelers wanting a modern, spacious double-decker boat and a welcome prosecco or seasonal cocktail for just €14.",
        "price": "€14",
        "price_sub": "including welcome drink",
        "anchor": "#3-portum",
        "hero_img": "63b858aaa4b5372841f3c9cb_Budapest-river-cruises-portum-1.webp",
        "more_imgs": [
            "63b858aa3433d05a938b3b9d_Budapest-river-cruises-portum-2.webp",
            "63b858ae01c3ee44f6c4f18c_Budapest-river-cruises-portum-10.webp",
            "63b858ab9b08757a269f08fd_Budapest-river-cruises-portum-8.webp",
            "63b858abea5f48ece83016e1_Budapest-river-cruises-portum-4.webp",
            "63b858abdd97c16e66cdfc88_Budapest-river-cruises-portum-5.webp",
            "63b858b0a4b5373981f3cb55_Budapest-river-cruises-portum-11.webp",
            "63b858ac482e83d1749e4d72_Budapest-river-cruises-portum-6.webp"
        ]
    },
    {
        "rank": 5,
        "badge": "⚡ #5 Central No-Frills Pick",
        "badge_cls": "bpa-slate",
        "kicker": "Silverline Cruises • 📍 Dock 11 (Elizabeth Bridge)",
        "title": "No-Frills Budget Sightseeing Cruise Without Welcome Drink",
        "url": "https://budapestrivercruise.eu/product/budapest-sightseeing-cruises/?code=bpadventures",
        "score": "4.2 / 5.0",
        "stars": "★★★★☆",
        "reviews": "(19,360+ Reviews)",
        "channels": [
            ("gyg", "4.2", "(19,040+)"),
            ("viator", "3.6", "(210+)"),
            ("ta", "3.6", "(110+)")
        ],
        "specs": [
            "📍 Central Dock 11",
            "⏱️ 60 Mins",
            "🍸 Full Bar Onboard",
            "🏛️ Full Danube Loop"
        ],
        "best_for": "Travelers staying in central Pest who want a cheap, straightforward 60-minute sightseeing loop departing right next to Elizabeth Bridge.",
        "price": "€12–14",
        "price_sub": "ticket only • bar onboard",
        "anchor": "#5-silverline-no-frills",
        "hero_img": "64ef34962db384577b89c4d5_Silverline%20Sightseeing%20Cruise%20%20(8).webp",
        "more_imgs": [
            "64c8d89ab333794837100497_Dinner-cruise-silverline-folklore-operetta%20(7).webp",
            "64ef3285d01ceeb33c48c392_Silverline%20sightseeing%20cruise%20(5).webp",
            "64ef321d5eb0ffac9e51c081_Silverline%20sightseeing%20cruise%20(3).webp",
            "64ef32638163f97d5da3ac80_Silverline%20sightseeing%20cruise%20(7).webp",
            "64946b4210f06faa6bdaf364_13-silverline-cruises.webp",
            "64ef32364cb5fd729f72343a_Silverline%20sightseeing%20cruise%20(11).webp"
        ]
    },
    {
        "rank": 6,
        "badge": "🍹 #6 Best Cocktail Cruise",
        "badge_cls": "bpa-blue",
        "kicker": "Silverline Cruises • 📍 Dock 11 (Elizabeth Bridge)",
        "title": "Budapest Sightseeing Cruise With Two Freshly Mixed Cocktails",
        "url": "https://budapestrivercruise.eu/product/sunset-cocktail-cruise/?code=bpadventures",
        "score": "4.3 / 5.0",
        "stars": "★★★★☆",
        "reviews": "(1,370+ Reviews)",
        "channels": [
            ("gyg", "4.4", "(1,000+)"),
            ("viator", "4.1", "(230+)"),
            ("ta", "4.1", "(140+)")
        ],
        "specs": [
            "🍹 2 Large Cocktails",
            "⏱️ 60–75 Mins",
            "📱 Free App Audio Guide",
            "🌇 Open-Air Top Deck"
        ],
        "best_for": "Evening sightseers who prefer two freshly mixed cocktails (Mojito, Cuba Libre, Piña Colada) over standard sparkling wine while cruising at sunset.",
        "price": "€32–37",
        "price_sub": "including 2 cocktails",
        "anchor": "#6-sunset-cocktail-cruise",
        "hero_img": "6638d3ec69d8d69f0271d0da_best-river-cruises-silverline-cocktail-pizza-drinks-cruise-10.webp",
        "more_imgs": [
            "6638d3ed86f3c86d86c9466b_best-river-cruises-silverline-cocktail-pizza-drinks-cruise-11.webp",
            "6638d3edd5cd846bb24b9410_best-river-cruises-silverline-cocktail-pizza-drinks-cruise-6.webp",
            "6638d3eb6ef3a0601bcec896_best-river-cruises-silverline-cocktail-pizza-drinks-cruise-3.webp",
            "6638d3e84e92f3c6c95eaece_best-river-cruises-silverline-cocktail-pizza-drinks-cruise-7.webp",
            "6638d3eb07cc7381da3f44f3_best-river-cruises-silverline-cocktail-pizza-drinks-cruise-2.webp",
            "6638d3ea5240bf0d972917c8_best-river-cruises-silverline-cocktail-pizza-drinks-cruise-8.webp"
        ]
    },
    {
        "rank": 7,
        "badge": "🍕 #7 Best Pizza & Beer Cruise",
        "badge_cls": "bpa-slate",
        "kicker": "Silverline Cruises • 📍 Dock 11 (Elizabeth Bridge)",
        "title": "Budapest River Cruise with Pizza & Unlimited Beer / Soft Drinks",
        "url": "https://budapestrivercruise.eu/product/pizza-cruise-budapest/?code=bpadventures",
        "score": "4.2 / 5.0",
        "stars": "★★★★☆",
        "reviews": "(1,190+ Reviews)",
        "channels": [
            ("gyg", "4.2", "(980+)"),
            ("viator", "4.2", "(130+)"),
            ("ta", "4.2", "(80+)")
        ],
        "specs": [
            "🍕 1 Whole Hot Pizza",
            "🍺 Unlimited Beer & Soft Drinks",
            "⏱️ 60–75 Mins",
            "📍 Central Dock 11"
        ],
        "best_for": "Casual travelers, friends, and families with teens wanting hot pizza and bottomless draft beer or soft drinks without a formal sit-down dinner.",
        "price": "€35–39",
        "price_sub": "pizza + unlimited drinks",
        "anchor": "#9-pizza-and-beer-cruise",
        "hero_img": "6638d3eb7ec40d20901aa81e_best-river-cruises-silverline-cocktail-pizza-drinks-cruise-9.webp",
        "more_imgs": [
            "64957c0835b706f1aa44c299_1-pizza-beer-cruise.webp",
            "64958a8b3e2fa8199f43a2a1_3-pizza-beer-cruise.webp",
            "6638d3ecb963489a0ad4d4a7_best-river-cruises-silverline-cocktail-pizza-drinks-cruise-5.webp",
            "6638d3ea5240bf0d972917c8_best-river-cruises-silverline-cocktail-pizza-drinks-cruise-8.webp",
            "64958b013eea741396853973_4-pizza-beer-cruise.webp"
        ]
    },
    {
        "rank": 8,
        "badge": "🎻 #8 Best Buffet & Folk Show",
        "badge_cls": "bpa-blue",
        "kicker": "Hungária Koncert (Gróf Széchenyi) • 📍 Dock 3 (Akadémia)",
        "title": "All-You-Can-Eat Buffet Dinner Cruise With Folk Music & Dance Show",
        "url": "https://budapestxplore.com/en/served-dinner-and-cruise-with-live-music-and-folklore-show-xpZWMYjcMjIw?affi=6876",
        "score": "4.6 / 5.0",
        "stars": "★★★★★",
        "reviews": "(15,460+ Reviews)",
        "channels": [
            ("gyg", "4.3", "(2,020+)"),
            ("viator", "4.7", "(7,360+)"),
            ("ta", "4.7", "(6,080+)")
        ],
        "specs": [
            "🍲 12-Course Hungarian Buffet",
            "🥂 2 Welcome Drinks",
            "🎻 Live Folk & Gypsy Show",
            "⏱️ 90–120 Mins"
        ],
        "best_for": "Travelers wanting to combine evening sightseeing with a generous all-you-can-eat Hungarian buffet and an energetic folklore show aboard a grand paddle steamer.",
        "price": "€89",
        "price_sub": "buffet + show + 2 drinks",
        "anchor": "#7-hk-dinner-cruise",
        "hero_img": "63b858cdb4ae8b9d0e597bf4_Budapest-river-cruises-hungaria-koncert-11.webp",
        "more_imgs": [
            "63b858cdb4ae8b56a4597bf5_Budapest-river-cruises-hungaria-koncert-10.webp",
            "63b858c9ab14b20add2d136a_Budapest-river-cruises-hungaria-koncert-8.webp",
            "63b858c97991129dcb5fa59a_Budapest-river-cruises-hungaria-koncert-3.webp",
            "63b858c9482e8373089e515f_Budapest-river-cruises-hungaria-koncert-4.webp",
            "63b858c9a4e49ca09097411c_Budapest-river-cruises-hungaria-koncert-6.webp",
            "63b858cee7351cbee9beb832_Budapest-river-cruises-hungaria-koncert-13.webp",
            "63b858cff69a68768c2aa8c0_Budapest-river-cruises-hungaria-koncert-16.webp"
        ]
    },
    {
        "rank": 9,
        "badge": "🍷 #9 Best Wine & Violin Cruise",
        "badge_cls": "bpa-slate",
        "kicker": "Hungária Koncert (Gróf Széchenyi) • 📍 Dock 3 (Akadémia)",
        "title": "Folklore Drinks Cruise: Night Cruise with Cocktails, Craft Beer or Wine",
        "url": "https://www.getyourguide.com/budapest-l29/budapest-evening-cruise-including-drink-options-t1745/?partner_id=YS414AJ&utm_medium=online_publisher&cmp=article-river-cruises-comparison-list-hk-drinks-cruise",
        "score": "4.2 / 5.0",
        "stars": "★★★★☆",
        "reviews": "(8,520+ Reviews)",
        "channels": [
            ("gyg", "4.1", "(6,470+)"),
            ("viator", "4.3", "(1,220+)"),
            ("ta", "4.3", "(830+)")
        ],
        "specs": [
            "🎻 Live Folk Violin Trio",
            "🍷 Wine, Craft Beer or Cocktails",
            "⏱️ 90–120 Mins",
            "🛳️ Historic Wood Salon"
        ],
        "best_for": "Travelers wanting the 90-minute historic paddle-steamer cruise and live Hungarian violin trio with a drink or wine tasting package instead of full dinner.",
        "price": "€21–65",
        "price_sub": "by selected drink package",
        "anchor": "#8-hk-drinks-cruise",
        "hero_img": "63b858cebbd3ae1fbe2a2462_Budapest-river-cruises-hungaria-koncert-15.webp",
        "more_imgs": [
            "63b858c9a4e49c05eb97411f_Budapest-river-cruises-hungaria-koncert-2.webp",
            "63b858cff69a68768c2aa8c0_Budapest-river-cruises-hungaria-koncert-16.webp",
            "63b858c9a4e49ca09097411c_Budapest-river-cruises-hungaria-koncert-6.webp",
            "6496b701c4e9164660d5a9d4_1-cabaret-cruise.webp"
        ]
    },
    {
        "rank": 10,
        "badge": "⛴️ #10 Cheapest Day Ferry",
        "badge_cls": "bpa-slate",
        "kicker": "Mahart PassNave • 📍 Vigadó tér Dock 5",
        "title": "Cheapest Day Hop-On Hop-Off Sightseeing Cruise with Welcome Drink",
        "url": "https://www.getyourguide.com/budapest-l29/budapest-winter-cruise-from-downtown-budapest-t69093/?partner_id=YS414AJ&utm_medium=online_publisher&cmp=article-river-cruises-comparison-list-mahart-cruise&mkt_cmp=true",
        "score": "4.3 / 5.0",
        "stars": "★★★★☆",
        "reviews": "(10,000+ Reviews)",
        "channels": [
            ("gyg", "4.3", "(10,000+)")
        ],
        "specs": [
            "🎟️ Unlimited Same-Day Rides",
            "🏝️ Stops at Margaret Island",
            "🥂 1 Drink Included",
            "💸 Bare-Bones Commuter Boat"
        ],
        "best_for": "Ultra-budget daytime travelers who want a cheap hop-on hop-off commuter boat to get off on Margaret Island and re-board later.",
        "price": "€12–18",
        "price_sub": "unlimited day pass",
        "anchor": "#10-mahart",
        "hero_img": "63b85923f731d953e7d2772f_Budapest-river-cruise-mahart-19.webp",
        "more_imgs": [
            "63b8591b6b62093c6505cb16_Budapest-river-cruise-mahart-8.webp",
            "63b8591bdd97c145adce0126_Budapest-river-cruise-mahart-7.webp",
            "63b8591b4f56a26af5651186_Budapest-river-cruise-mahart-4.webp",
            "63b8591b803ea5762ce141d5_Budapest-river-cruise-mahart-2.webp",
            "63b8591b56f82278919e0f51_Budapest-river-cruise-mahart-3.webp",
            "68ed771b2e1747ca22b7c863_best-river-cruises-budapest-boat-mahart00001.avif",
            "63b85920f69a68d3eb2aad0c_Budapest-river-cruise-mahart-12.webp"
        ]
    }
]

ICON_URLS = {
    "gyg": "https://cdn.prod.website-files.com/60e43c7d6d05b671dff0dc1a/65350288cf6e222fd93f3745_getyourguide-icon.png",
    "ta": "https://cdn.prod.website-files.com/652d0405192ba076b04f74a3/68f64414502d0348145b678e_tripadvisor-icon.avif",
    "viator": "https://cdn.prod.website-files.com/60e43c7d6d05b671dff0dc1a/65350288cf6e222fd93f3747_viator-icon.png"
}
ICON_ALTS = {"gyg": "GetYourGuide", "ta": "Tripadvisor", "viator": "Viator"}

CDN = "https://cdn.prod.website-files.com/60e43c7d6d05b671dff0dc1a/"

cards_html = []
for c in cruises:
    tot_imgs = 1 + len(c["more_imgs"])
    more_str = ",".join(c["more_imgs"])
    
    ch_items = []
    for ch_key, val, cnt in c["channels"]:
        ch_items.append(f'<div class="bpa-channel-item"><img src="{ICON_URLS[ch_key]}" alt="{ICON_ALTS[ch_key]}"><strong>{val}</strong> <span>{cnt}</span></div>')
    ch_html = "\n          ".join(ch_items)
    
    sp_items = [f'<span class="bpa-spec-pill">{s}</span>' for s in c["specs"]]
    sp_html = "\n          ".join(sp_items)
    
    card = f"""  <!-- CRUISE #{c["rank"]} -->
  <div class="bpa-card">
    <div class="bpa-main">
      <div class="bpa-media">
        <span class="bpa-rank-tag {c["badge_cls"]}">{c["badge"]}</span>
        <button type="button" class="bpa-nav-arrow prev" onclick="bpaSlide(this, -1)">‹</button>
        <button type="button" class="bpa-nav-arrow next" onclick="bpaSlide(this, 1)">›</button>
        <span class="bpa-counter-pill">1 / {tot_imgs}</span>
        <div class="bpa-slider" data-more="{more_str}" onscroll="bpaCount(this)">
          <img src="{CDN}{c["hero_img"]}" alt="{c["title"]}">
        </div>
      </div>
      <div class="bpa-info">
        <div class="bpa-kicker">{c["kicker"]}</div>
        <a href="{c["url"]}" target="_blank" rel="sponsored noopener" class="bpa-headline">
          {c["title"]}
        </a>
        <div class="bpa-proof-bar">
          <span class="bpa-gold-stars">{c["stars"]}</span>
          <span class="bpa-score-text">{c["score"]}</span>
          <span class="bpa-count-muted">{c["reviews"]}</span>
          <span class="bpa-verified-chip">✓ Personally Tested</span>
        </div>
        <div class="bpa-channels">
          {ch_html}
        </div>
        <div class="bpa-specs-row">
          {sp_html}
        </div>
        <div class="bpa-best-for">🎯 <strong>Best For:</strong> {c["best_for"]}</div>
      </div>
      <div class="bpa-cta-cell">
        <div><div class="bpa-price-num">{c["price"]}</div><div class="bpa-price-sub">{c["price_sub"]}</div></div>
        <a href="{c["url"]}" target="_blank" rel="sponsored noopener" class="bpa-book-button">Book Now →</a>
        <a href="{c["anchor"]}" class="bpa-sublink">Read Full Review ↓</a>
      </div>
    </div>
  </div>"""
    cards_html.append(card)

all_cards_str = "\n\n".join(cards_html)

# Read the CSS block from comparison_deck_7_cruises.html to keep identical styling
with open("/Users/adamdimitrov/Development/budapest-adventures/comparison_deck_7_cruises.html") as f:
    dinner_deck = f.read()

style_end = dinner_deck.find("</style>")
base_css = dinner_deck[:style_end]

# Add CSS rules that automatically unwrap the 10 hidden reviews inside .comparison-table on the River Cruises page!
river_unwrap_css = """
/* === AUTO-UNWRAP 10 HIDDEN RIVER CRUISE REVIEWS FOR 10/10 SEO === */
.div-block-27, .table-row-grey-3, .table-row-grey-3-copy,
[id^="1-"], [id^="2-"], [id^="3-"], [id^="4-"], [id^="5-"],
[id^="6-"], [id^="7-"], [id^="8-"], [id^="9-"], [id^="10-"] {
  scroll-margin-top: 90px !important;
}
.comparison-table .view-all-button,
.comparison-table .tabs-menu,
.comparison-table .grid-cell-2,
.comparison-table .div-block-21,
.comparison-table .grid-cell-5,
.comparison-table .price-2,
.comparison-table .buy-button-read-full-review,
.comparison-table .div-block-47,
.comparison-table .faq-item-toggle,
.load-more {
  display: none !important;
}
.comparison-table .table-wrapper-2,
.comparison-table .table-2 {
  min-width: 0 !important;
  width: 100% !important;
  overflow: visible !important;
}
.comparison-table .table-row-grey-3,
.comparison-table .table-row-grey-3-copy {
  display: block !important;
  padding: 28px 24px !important;
  margin-bottom: 32px !important;
  background: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
  border-radius: 16px !important;
  box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04) !important;
}
.comparison-table .grid-cell-3 {
  display: block !important;
  width: 100% !important;
  padding: 0 !important;
}
.comparison-table .coin-name-wrapper {
  white-space: normal !important;
  margin-bottom: 18px !important;
  padding-bottom: 14px !important;
  border-bottom: 2px solid #f1f5f9 !important;
}
.comparison-table .coin-name-2 {
  font-size: 24px !important;
  line-height: 1.3 !important;
  font-weight: 800 !important;
  margin: 0 0 6px 0 !important;
}
.comparison-table .faq-content-wrap.w-dropdown-list,
.bpa-open-review-body,
.load-more-div {
  display: block !important;
  position: static !important;
  background: transparent !important;
  padding: 0 !important;
  overflow: visible !important;
  width: 100% !important;
}
</style>"""

js_block = """<script>
(function() {
  const BPA_CDN = "https://cdn.prod.website-files.com/60e43c7d6d05b671dff0dc1a/";
  
  // 1. Hydrate lazy images & desktop drag
  document.querySelectorAll(".bpa-slider[data-more]").forEach(c => {
    const m = c.getAttribute("data-more").split(",");
    m.forEach(f => {
      if (!f) return;
      const img = document.createElement("img");
      img.src = f.startsWith("http") ? f : BPA_CDN + f;
      img.loading = "lazy";
      img.alt = "Budapest River Cruise";
      c.appendChild(img);
    });
    c.removeAttribute("data-more");
    
    const tot = c.children.length;
    const cnt = c.parentElement.querySelector(".bpa-counter-pill");
    if (cnt) cnt.textContent = "1 / " + tot;
    
    let isDown = false, startX, sLeft;
    c.addEventListener("mousedown", e => {
      isDown = true;
      c.style.scrollSnapType = "none";
      startX = e.pageX - c.offsetLeft;
      sLeft = c.scrollLeft;
    });
    const stopDrag = () => {
      if (!isDown) return;
      isDown = false;
      c.style.scrollSnapType = "x mandatory";
      const w = c.offsetWidth || 1;
      const target = Math.round(c.scrollLeft / w) * w;
      c.scrollTo({ left: target, behavior: "smooth" });
    };
    c.addEventListener("mouseleave", stopDrag);
    c.addEventListener("mouseup", stopDrag);
    c.addEventListener("mousemove", e => {
      if (!isDown) return;
      e.preventDefault();
      const x = e.pageX - c.offsetLeft;
      const walk = (x - startX) * 1.15;
      c.scrollLeft = sLeft - walk;
    });
  });

  window.bpaSlide = function(btn, dir) {
    const c = btn.parentElement.querySelector(".bpa-slider");
    if (c) c.scrollBy({ left: dir * c.offsetWidth, behavior: "smooth" });
  };

  window.bpaCount = function(c) {
    if (c._ticking) return;
    c._ticking = true;
    requestAnimationFrame(() => {
      const w = c.offsetWidth || 1;
      const tot = c.children.length;
      const idx = Math.min(tot, Math.max(1, Math.round(c.scrollLeft / w) + 1));
      const cnt = c.parentElement.querySelector(".bpa-counter-pill");
      if (cnt) cnt.textContent = idx + " / " + tot;
      c._ticking = false;
    });
  };

  // 2. Unwrap <nav class="w-dropdown-list"> into semantic <div> & hoist anchor IDs to row top
  const compHeading = document.getElementById("quick-summary-river-cruises-budapest");
  if (compHeading) {
    compHeading.textContent = "Detailed Breakdown — 10 Best River Cruises in Budapest";
  }
  document.querySelectorAll(".comparison-table .table-row-grey-3, .comparison-table .table-row-grey-3-copy").forEach(row => {
    const innerTarget = row.querySelector('[id^="1-"], [id^="2-"], [id^="3-"], [id^="4-"], [id^="5-"], [id^="6-"], [id^="7-"], [id^="8-"], [id^="9-"], [id^="10-"]');
    if (innerTarget && innerTarget.id) {
      const targetId = innerTarget.id;
      innerTarget.removeAttribute("id");
      row.id = targetId;
    }
    const navEl = row.querySelector("nav.faq-content-wrap");
    if (navEl) {
      const divEl = document.createElement("div");
      divEl.className = "bpa-open-review-body";
      while (navEl.firstChild) {
        divEl.appendChild(navEl.firstChild);
      }
      navEl.parentNode.replaceChild(divEl, navEl);
    }
  });

  // 3. Precision anchor scrolling with 85px top offset
  document.querySelectorAll('.bpa-sublink[href^="#"]').forEach(link => {
    link.addEventListener('click', function(e) {
      const hash = this.getAttribute('href');
      const target = document.getElementById(hash.substring(1)) || document.querySelector(hash);
      if (target) {
        e.preventDefault();
        const headerOffset = 85;
        const elementPosition = target.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
        window.scrollTo({
          top: Math.max(0, offsetPosition),
          behavior: 'smooth'
        });
        if (history.pushState) {
          history.pushState(null, null, hash);
        } else {
          location.hash = hash;
        }
      }
    });
  });
})();
</script>"""

full_output = f"""{base_css}{river_unwrap_css}

<div class="bpa-deck-wrap">
  <div class="bpa-section-header">
    <h2 class="bpa-section-title">Comparison — 10 Best Boat Tours &amp; River Cruises in Budapest (2026)</h2>
    <p class="bpa-section-sub">Personally field-tested on the Danube • Verified prices, dock locations &amp; real photos</p>
  </div>

{all_cards_str}
</div>

{js_block}
"""

out_path = "/Users/adamdimitrov/Development/budapest-adventures/comparison_deck_10_river_cruises.html"
with open(out_path, "w") as f:
    f.write(full_output)

print("Generated:", out_path)
print("Total character count:", len(full_output))

# Optimize character count to ~39,000 chars (well below Webflow 50,000 char limit even with CRLF)
import re

with open(out_path, "r") as f:
    raw = f.read()

# 1. Replace repeated 14px channel icon URLs with compact CSS classes
icon_css = """.bpa-channel-item i { display:inline-block; width:15px; height:15px; background-size:contain; background-repeat:no-repeat; background-position:center; border-radius:3px; vertical-align:middle; }
.bpa-ic-gyg { background-image:url('https://cdn.prod.website-files.com/60e43c7d6d05b671dff0dc1a/65350288cf6e222fd93f3745_getyourguide-icon.png'); }
.bpa-ic-ta { background-image:url('https://cdn.prod.website-files.com/652d0405192ba076b04f74a3/68f64414502d0348145b678e_tripadvisor-icon.avif'); }
.bpa-ic-viator { background-image:url('https://cdn.prod.website-files.com/60e43c7d6d05b671dff0dc1a/65350288cf6e222fd93f3747_viator-icon.png'); }
"""

raw = raw.replace("</style>", icon_css + "</style>")
raw = raw.replace(f'<img src="{ICON_URLS["gyg"]}" alt="GetYourGuide">', '<i class="bpa-ic-gyg" title="GetYourGuide"></i>')
raw = raw.replace(f'<img src="{ICON_URLS["ta"]}" alt="Tripadvisor">', '<i class="bpa-ic-ta" title="Tripadvisor"></i>')
raw = raw.replace(f'<img src="{ICON_URLS["viator"]}" alt="Viator">', '<i class="bpa-ic-viator" title="Viator"></i>')

# 2. Compact multi-line CSS rules slightly while keeping readability
style_m = re.search(r"<style>(.*?)</style>", raw, re.DOTALL)
if style_m:
    s_body = style_m.group(1)
    # remove CSS comments
    s_body = re.sub(r"/\*.*?\*/", "", s_body, flags=re.DOTALL)
    # collapse newlines inside { ... }
    s_body = re.sub(r"\{\s+", "{ ", s_body)
    s_body = re.sub(r";\s+", "; ", s_body)
    s_body = re.sub(r"\s+\}", " }", s_body)
    s_body = re.sub(r"\n{2,}", "\n", s_body).strip()
    raw = raw[:style_m.start(1)] + "\n" + s_body + "\n" + raw[style_m.end(1):]

# 3. Trim excessive leading spaces on HTML lines
lines = [re.sub(r"^\s{2,}", "  ", line) for line in raw.split("\n")]
raw = "\n".join(line for line in lines if line.strip())

with open(out_path, "w") as f:
    f.write(raw)

print("Optimized character count:", len(raw))
print("Optimized CRLF length:", len(raw) + raw.count("\n"))
