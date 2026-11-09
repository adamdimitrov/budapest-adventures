import re
import urllib.request
import urllib.parse

CDN = "/assets/cdn/60e43c7d6d05b671dff0dc1a/"

# 1. Exact verified working photo lists from dinner.html original table
dinner_photos = [
    # Card 1 Legenda (1 hero + 10 more = 11)
    [
        "66320defac2b58c3877cdbe5_best-dinner-cruises-budapest-legenda-city-cruises-2.webp",
        "663224a0b9517f8a892517a9_best-dinner-cruises-budapest-legenda-city-cruises-11.webp",
        "66320e4a4d501246b56e9d59_best-dinner-cruises-budapest-legenda-city-cruises-5.webp",
        "66320ed9bd523888f1d2aa1f_best-dinner-cruises-budapest-legenda-city-cruises-9.webp",
        "6632100d16cd1e9d193ff6d6_best-dinner-cruises-budapest-legenda-city-cruises-6.webp",
        "6632102a9455a44b8ba053fb_best-dinner-cruises-budapest-legenda-city-cruises-12.webp",
        "66322a2409d6d58a16b06276_best-dinner-cruises-budapest-legenda-city-cruises-16.webp",
        "66322994ce51b39cdb68bb77_best-dinner-cruises-budapest-legenda-city-cruises-8.webp",
        "66322a0f443d1321ca0ccc05_best-dinner-cruises-budapest-legenda-city-cruises-13.webp",
        "663229b884ffc8297ddcb52a_best-dinner-cruises-budapest-legenda-city-cruises-15.webp"
    ],
    # Card 2 Silverline No-Show (1 hero + 16 more = 17)
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
        "68e41f4c32ef581db78f327a_best-budapest-dinner-cruises-silverline-184.avif"
    ],
    # Card 3 Silverline Folklore (1 hero + 4 more = 5)
    [
        "64c8d8583e07bb712602367b_Dinner-cruise-silverline-folklore-operetta%20(10).webp",
        "64c8d7271075f67d40722de4_Silverline-dinner-cruise-piano-show%20(3).webp",
        "64c8d8323e1e4fe01cd6a77b_Dinner-cruise-silverline-folklore-operetta%20(4).webp",
        "64c8d903aae9a08e349f0f01_64c8d7262c32df84035842e1_Silverline-dinner-cruise-piano-show%20(4).webp"
    ],
    # Card 4 Silverline Piano (1 hero + 4 more = 5)
    [
        "64c8d727f93d12246ca21ddc_Silverline-dinner-cruise-piano-show%20(5).webp",
        "64c685e362db2b29aeae8f3e_Dinner-cruise-silverline-folklore-operetta%20(6).webp",
        "64c6862d339c9f8e98e8c419_Dinner-cruise-silverline-folklore-operetta%20(1).webp",
        "64c8d903aae9a08e349f0f01_64c8d7262c32df84035842e1_Silverline-dinner-cruise-piano-show%20(4).webp"
    ],
    # Card 5 Hungaria Koncert (1 hero + 8 more = 9)
    [
        "6a171485cb7f9db773f86225_hungaria-koncert-00003.avif",
        "6a17137547d8b03e7ab7dbfa_hungaria-koncert-00002.avif",
        "6a1717ab3b109f5aababa165_hungaria-koncert-00005.avif",
        "63b858c97991129dcb5fa59a_Budapest-river-cruises-hungaria-koncert-3.webp",
        "63b858c9482e8373089e515f_Budapest-river-cruises-hungaria-koncert-4.webp",
        "63b858cee7351cbee9beb832_Budapest-river-cruises-hungaria-koncert-13.webp",
        "6a1713758036c41f2768ca87_hungaria-koncert-00006.avif",
        "63b858c9a4e49ca09097411c_Budapest-river-cruises-hungaria-koncert-6.webp"
    ],
    # Card 6 Eurama (1 hero + 5 more = 6)
    [
        "64c900ca00a16648afedc0f2_Dinner-cruise-eurama-sightseeing%20(2).webp",
        "64c90214d23273a2e88e9615_Dinner-cruise-eurama-sightseeing%20(12).webp",
        "64c900cc6aab98bd3479f556_Dinner-cruise-eurama-sightseeing%20(8).webp",
        "64c900caed3c4d809550c8a7_Dinner-cruise-eurama-sightseeing%20(3).webp",
        "64c900cac89f6cf91209fc51_Dinner-cruise-eurama-sightseeing%20(4).webp"
    ],
    # Card 7 River Diva (1 hero + 5 more = 6)
    [
        "64946bd848dfb642de48fcfb_16-rubin-group.webp",
        "64ff0ad83b5217719ba1d701_Budapest-river-cruises-parliament.webp",
        "646f8757c76212af94a49dca_v5_Best%20River%20Cruises%20in%20Budapest.webp",
        "63b858ea56f82257ea9e0c70_Budapest-river-cruises-portum-16.webp",
        "64f9aa08f8ee33524047cdf3_Pest%20Walking%20Tour%20(10).webp"
    ]
]

# 2. Exact verified working photo lists from river.html original table
river_original_photos = [
    # Card 1 Legenda (1 hero + 11 more = 12)
    [
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
        "68f3738fb13a0d71ea3326d2_best-budapest-river-cruises-legenda-sightseeing-cruise-00001.avif"
    ],
    # Card 2 Rubin Group Unlimited Prosecco (1 hero + 5 more = 6)
    [
        "63b858ea56f82257ea9e0c70_Budapest-river-cruises-portum-16.webp",
        "63b858e8f731d90165d271cc_Budapest-river-cruises-portum-11.webp",
        "63b858e9803ea5e532e13df1_Budapest-river-cruises-portum-15.webp",
        "63b858e8a4e49cb177974356_Budapest-river-cruises-portum-14.webp",
        "63b858eda4b537601bf3ceab_Budapest-river-cruises-portum-21.webp"
    ],
    # Card 3 Kisfaludy Steamer (1 hero + 5 more = 6)
    [
        "64eb8e07a2dc265f519b2a83_Kisdalufy%20historic%20paddle%20steam%20cruise%20(7).webp",
        "64eb8e09dbce9b580c818930_Kisdalufy%20historic%20paddle%20steam%20cruise%20(10).webp",
        "64eda40ea110f471e61d0537_Kisdalufy%20historic%20paddle%20steam%20cruise%20(18).avif",
        "64eb8e07233b7bcba36b7081_Kisdalufy%20historic%20paddle%20steam%20cruise%20(6).webp",
        "64eb8e08627363a3b67f4967_Kisdalufy%20historic%20paddle%20steam%20cruise%20(8).webp"
    ],
    # Card 4 Portum Sightseeing (1 hero + 5 more = 6)
    [
        "63b858aa3433d05a938b3b9d_Budapest-river-cruises-portum-2.webp",
        "63b858ae01c3ee44f6c4f18c_Budapest-river-cruises-portum-10.webp",
        "63b858ab9b08757a269f08fd_Budapest-river-cruises-portum-8.webp",
        "63b858abea5f48ece83016e1_Budapest-river-cruises-portum-4.webp",
        "63b858abdd97c16e66cdfc88_Budapest-river-cruises-portum-5.webp"
    ],
    # Card 5 Silverline No Frills (1 hero + 4 more = 5)
    [
        "64c8d89ab333794837100497_Dinner-cruise-silverline-folklore-operetta%20(7).webp",
        "64ef3285d01ceeb33c48c392_Silverline%20sightseeing%20cruise%20(5).webp",
        "64ef321d5eb0ffac9e51c081_Silverline%20sightseeing%20cruise%20(3).webp",
        "64ef32638163f97d5da3ac80_Silverline%20sightseeing%20cruise%20(7).webp"
    ],
    # Card 6 Silverline Cocktail (1 hero + 5 more = 6)
    [
        "6638d3ed86f3c86d86c9466b_best-river-cruises-silverline-cocktail-pizza-drinks-cruise-11.webp",
        "6638d3edd5cd846bb24b9410_best-river-cruises-silverline-cocktail-pizza-drinks-cruise-6.webp",
        "6638d3eb6ef3a0601bcec896_best-river-cruises-silverline-cocktail-pizza-drinks-cruise-3.webp",
        "6638d3e84e92f3c6c95eaece_best-river-cruises-silverline-cocktail-pizza-drinks-cruise-7.webp",
        "6638d3eb07cc7381da3f44f3_best-river-cruises-silverline-cocktail-pizza-drinks-cruise-2.webp"
    ],
    # Card 7 Silverline Pizza & Beer (1 hero + 4 more = 5)
    [
        "64957c0835b706f1aa44c299_1-pizza-beer-cruise.webp",
        "64958a8b3e2fa8199f43a2a1_3-pizza-beer-cruise.webp",
        "6638d3ecb963489a0ad4d4a7_best-river-cruises-silverline-cocktail-pizza-drinks-cruise-5.webp",
        "6638d3ea5240bf0d972917c8_best-river-cruises-silverline-cocktail-pizza-drinks-cruise-8.webp"
    ],
    # Card 8 Hungaria Koncert Buffet (1 hero + 5 more = 6)
    [
        "63b858cdb4ae8b56a4597bf5_Budapest-river-cruises-hungaria-koncert-10.webp",
        "63b858c9ab14b20add2d136a_Budapest-river-cruises-hungaria-koncert-8.webp",
        "63b858c97991129dcb5fa59a_Budapest-river-cruises-hungaria-koncert-3.webp",
        "63b858c9482e8373089e515f_Budapest-river-cruises-hungaria-koncert-4.webp",
        "63b858c9a4e49ca09097411c_Budapest-river-cruises-hungaria-koncert-6.webp"
    ],
    # Card 9 Hungaria Koncert Folklore Drinks (1 hero + 4 more = 5)
    [
        "63b858c9a4e49c05eb97411f_Budapest-river-cruises-hungaria-koncert-2.webp",
        "63b858cff69a68768c2aa8c0_Budapest-river-cruises-hungaria-koncert-16.webp",
        "63b858c9a4e49ca09097411c_Budapest-river-cruises-hungaria-koncert-6.webp",
        "6496b701c4e9164660d5a9d4_1-cabaret-cruise.webp"
    ],
    # Card 10 Mahart Day Cruise (1 hero + 5 more = 6)
    [
        "63b8591b6b62093c6505cb16_Budapest-river-cruise-mahart-8.webp",
        "63b8591bdd97c145adce0126_Budapest-river-cruise-mahart-7.webp",
        "63b8591b4f56a26af5651186_Budapest-river-cruise-mahart-4.webp",
        "63b8591b803ea5762ce141d5_Budapest-river-cruise-mahart-2.webp",
        "63b8591b56f82278919e0f51_Budapest-river-cruise-mahart-3.webp"
    ]
]

pattern = re.compile(r'(<span class="bpa-counter-pill">)1 / \d+(</span>\s*<div class="bpa-slider" data-more=")[^"]*(" onscroll="bpaCount(?:Cruise2)?\(this\)">)')

def update_file(filepath, photos_list):
    with open(filepath, "r") as f:
        c = f.read()
    matches = list(pattern.finditer(c))
    print(f"{filepath}: found {len(matches)} matches, expected {len(photos_list)}")
    assert len(matches) == len(photos_list)
    for i in reversed(range(len(photos_list))):
        m = matches[i]
        more_imgs = ",".join(photos_list[i])
        tot = len(photos_list[i]) + 1
        rep = m.group(1) + f"1 / {tot}" + m.group(2) + more_imgs + m.group(3)
        c = c[:m.start()] + rep + c[m.end():]
    with open(filepath, "w") as f:
        f.write(c)
    print(f"Updated {filepath} successfully! (Length: {len(c)})")

# Update Dinner files
update_file("/Users/adamdimitrov/Development/budapest-adventures/comparison_deck_7_cruises.html", dinner_photos)
update_file("/Users/adamdimitrov/Development/budapest-adventures/all_7_cruises_complete.html", dinner_photos)

# Update Webflow split parts
def update_part(filename, indices):
    with open("/Users/adamdimitrov/Development/budapest-adventures/" + filename, "r") as f:
        c = f.read()
    matches = list(pattern.finditer(c))
    assert len(matches) == len(indices)
    for idx_in_part in reversed(range(len(indices))):
        m = matches[idx_in_part]
        global_idx = indices[idx_in_part]
        more_imgs = ",".join(dinner_photos[global_idx])
        tot = len(dinner_photos[global_idx]) + 1
        rep = m.group(1) + f"1 / {tot}" + m.group(2) + more_imgs + m.group(3)
        c = c[:m.start()] + rep + c[m.end():]
    with open("/Users/adamdimitrov/Development/budapest-adventures/" + filename, "w") as f:
        f.write(c)
    print(f"Updated {filename} successfully! (Length: {len(c)})")

update_part("webflow_part1_cruises_1_to_2.html", [0, 1])
update_part("webflow_part2_cruises_3_to_4.html", [2, 3])
update_part("webflow_part3_cruises_5_to_7.html", [4, 5, 6])

# Update River deck
update_file("/Users/adamdimitrov/Development/budapest-adventures/comparison_deck_10_river_cruises.html", river_original_photos)
