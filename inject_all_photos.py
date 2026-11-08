import re

with open("/Users/adamdimitrov/Development/budapest-adventures/comparison_deck_7_cruises.html", "r") as f:
    content = f.read()

# All expanded photo datasets
photos = [
    # Card 1 Legenda (1 static + 13 more = 14)
    [
        "66320defac2b58c3877cdbe5_best-dinner-cruises-budapest-legenda-city-cruises-2.webp",
        "66320e04d3230ba7d3c2276e_best-dinner-cruises-budapest-legenda-city-cruises-3.webp",
        "66320e4a4d501246b56e9d59_best-dinner-cruises-budapest-legenda-city-cruises-5.webp",
        "6632100d16cd1e9d193ff6d6_best-dinner-cruises-budapest-legenda-city-cruises-6.webp",
        "663224a034f71a9316d3bbd6_best-dinner-cruises-budapest-legenda-city-cruises-7.webp",
        "66322994ce51b39cdb68bb77_best-dinner-cruises-budapest-legenda-city-cruises-8.webp",
        "66320ed9bd523888f1d2aa1f_best-dinner-cruises-budapest-legenda-city-cruises-9.webp",
        "663224a0baaa33d6b63ca75d_best-dinner-cruises-budapest-legenda-city-cruises-10.webp",
        "663224a0b9517f8a892517a9_best-dinner-cruises-budapest-legenda-city-cruises-11.webp",
        "6632102a9455a44b8ba053fb_best-dinner-cruises-budapest-legenda-city-cruises-12.webp",
        "66322a0f443d1321ca0ccc05_best-dinner-cruises-budapest-legenda-city-cruises-13.webp",
        "663229b884ffc8297ddcb52a_best-dinner-cruises-budapest-legenda-city-cruises-15.webp",
        "66322a2409d6d58a16b06276_best-dinner-cruises-budapest-legenda-city-cruises-16.webp"
    ],
    # Card 2 Silverline No-Show (1 static + 17 more = 18)
    [
        "68e41f4ca4cf389c00f1d86d_best-budapest-dinner-cruises-silverline-7.avif",
        "68e41f4cc77b0bf60d90e732_best-budapest-dinner-cruises-silverline-31.avif",
        "68e41f4c76d60be8879c4c56_best-budapest-dinner-cruises-silverline-68.avif",
        "68e41f4cb924ed0b010c12d6_best-budapest-dinner-cruises-silverline-43.avif",
        "68e41f4c4eb37345f0ae26a5_best-budapest-dinner-cruises-silverline-81.avif",
        "68e41f4ce41432b98e5ea0d5_best-budapest-dinner-cruises-silverline-90.avif",
        "68e41f4cc07e68f39d183c3d_best-budapest-dinner-cruises-silverline-96.avif",
        "68e41f4c49f552630c60894a_best-budapest-dinner-cruises-silverline-102.avif",
        "68e41f4b17cb3aefbd5b6237_best-budapest-dinner-cruises-silverline-98.avif",
        "68e41f4c7d21d3f5803a13ec_best-budapest-dinner-cruises-silverline-161.avif",
        "68e41f4c853fe56d60faa043_best-budapest-dinner-cruises-silverline-79.avif",
        "68e41f4cf2a365e6e1cfb88f_best-budapest-dinner-cruises-silverline-165.avif",
        "68e41f4c5cc1ea04e90e1b5e_best-budapest-dinner-cruises-silverline-168.avif",
        "68e41f4c8e889bb32cb1bc1f_best-budapest-dinner-cruises-silverline-179.avif",
        "68e41f4cae3cd385bb537124_best-budapest-dinner-cruises-silverline-187.avif",
        "68e41f4c32ef581db78f327a_best-budapest-dinner-cruises-silverline-184.avif",
        "68e50b7fb228260007cb9efc_best-budapest-dinner-cruises-silverline-70.avif"
    ],
    # Card 3 Silverline Folklore (1 static + 9 more = 10)
    [
        "64c8d8583e07bb712602367b_Dinner-cruise-silverline-folklore-operetta%20(10).webp",
        "64c8d8323e1e4fe01cd6a77b_Dinner-cruise-silverline-folklore-operetta%20(4).webp",
        "64c8d89ab333794837100497_Dinner-cruise-silverline-folklore-operetta%20(7).webp",
        "64c685e362db2b29aeae8f3e_Dinner-cruise-silverline-folklore-operetta%20(6).webp",
        "64c6862d339c9f8e98e8c419_Dinner-cruise-silverline-folklore-operetta%20(1).webp",
        "68e5192df437885c6f3101bd_best-budapest-dinner-cruises-silverline-151.avif",
        "68e41f4c7d21d3f5803a13ec_best-budapest-dinner-cruises-silverline-161.avif",
        "68e41f4cf2a365e6e1cfb88f_best-budapest-dinner-cruises-silverline-165.avif",
        "68e50b1313afcdd3e12cbd8c_best-budapest-dinner-cruises-silverline-8.avif"
    ],
    # Card 4 Silverline Piano (1 static + 8 more = 9)
    [
        "64c8d7271075f67d40722de4_Silverline-dinner-cruise-piano-show%20(3).webp",
        "64c8d727f93d12246ca21ddc_Silverline-dinner-cruise-piano-show%20(5).webp",
        "64c8d903aae9a08e349f0f01_64c8d7262c32df84035842e1_Silverline-dinner-cruise-piano-show%20(4).webp",
        "68e51dce60ee5db481b8636d_best-budapest-dinner-cruises-silverline-105.avif",
        "68e41f4c49f552630c60894a_best-budapest-dinner-cruises-silverline-102.avif",
        "68e41f4c853fe56d60faa043_best-budapest-dinner-cruises-silverline-79.avif",
        "68e50ca9d6698af6925d4955_best-budapest-dinner-cruises-silverline-188.avif",
        "68e52baf60c0a1aa52cf634d_best-budapest-dinner-cruises-silverline-121.avif"
    ],
    # Card 5 Hungaria Koncert (1 static + 13 more = 14)
    [
        "6a171485cb7f9db773f86225_hungaria-koncert-00003.avif",
        "6a17137547d8b03e7ab7dbfa_hungaria-koncert-00002.avif",
        "6a1717ab3b109f5aababa165_hungaria-koncert-00005.avif",
        "6a1713758036c41f2768ca87_hungaria-koncert-00006.avif",
        "6a1718a5c527a0f3579e0080_hungaria-koncert-00007.avif",
        "6a17125c2e3e5a94222c3ddb_IMG_9424.avif",
        "63b858c97991129dcb5fa59a_Budapest-river-cruises-hungaria-koncert-3.webp",
        "63b858c9482e8373089e515f_Budapest-river-cruises-hungaria-koncert-4.webp",
        "63b858cee7351cbee9beb832_Budapest-river-cruises-hungaria-koncert-13.webp",
        "63b858c9a4e49ca09097411c_Budapest-river-cruises-hungaria-koncert-6.webp",
        "63b858cdb4ae8b56a4597bf5_Budapest-river-cruises-hungaria-koncert-10.webp",
        "63b858c9ab14b20add2d136a_Budapest-river-cruises-hungaria-koncert-8.webp",
        "63b858cff69a68768c2aa8c0_Budapest-river-cruises-hungaria-koncert-16.webp"
    ],
    # Card 6 Eurama (1 static + 7 more = 8)
    [
        "64c900ca00a16648afedc0f2_Dinner-cruise-eurama-sightseeing%20(2).webp",
        "64c90214d23273a2e88e9615_Dinner-cruise-eurama-sightseeing%20(12).webp",
        "64c900cc6aab98bd3479f556_Dinner-cruise-eurama-sightseeing%20(8).webp",
        "64c900caed3c4d809550c8a7_Dinner-cruise-eurama-sightseeing%20(3).webp",
        "64c900cac89f6cf91209fc51_Dinner-cruise-eurama-sightseeing%20(4).webp",
        "64c9008beb38ebbbf8eb6d91_Dinner-cruise-eurama-sightseeing%20(7).avif",
        "64c900c953b6154b953dd8e9_Dinner-cruise-eurama-sightseeing%20(1).webp"
    ],
    # Card 7 River Diva (1 static + 5 more = 6)
    [
        "64946bd848dfb642de48fcfb_16-rubin-group.webp",
        "64ff0ad83b5217719ba1d701_Budapest-river-cruises-parliament.webp",
        "646f8757c76212af94a49dca_v5_Best%20River%20Cruises%20in%20Budapest.webp",
        "63b858ea56f82257ea9e0c70_Budapest-river-cruises-portum-16.webp",
        "64f9aa08f8ee33524047cdf3_Pest%20Walking%20Tour%20(10).webp"
    ]
]

# Find all blocks of counter pill and slider
# Format:
# <span class="bpa-counter-pill">1 / \d+</span>\s*<div class="bpa-slider" data-more="[^"]*" onscroll="bpaCount\(this\)">

pattern = re.compile(r'(<span class="bpa-counter-pill">)1 / \d+(</span>\s*<div class="bpa-slider" data-more=")[^"]*(" onscroll="bpaCount\(this\)">)')

matches = list(pattern.finditer(content))
print(f"Found {len(matches)} matches")

if len(matches) == 7:
    # Rebuild string from back to front to preserve offsets
    for i in reversed(range(7)):
        m = matches[i]
        more_imgs = ",".join(photos[i])
        total_count = len(photos[i]) + 1
        replacement = f'{m.group(1)}1 / {total_count}{m.group(2)}{more_imgs}{m.group(3)}'
        content = content[:m.start()] + replacement + content[m.end():]

with open("/Users/adamdimitrov/Development/budapest-adventures/comparison_deck_7_cruises.html", "w") as f:
    f.write(content)

print("Updated deck written successfully!")
print("New length in characters:", len(content))
