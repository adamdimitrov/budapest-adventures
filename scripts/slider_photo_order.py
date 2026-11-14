"""Order card slider photos so each sequence sells the card's promise.

First photo = the single strongest shot for the card's promise, then the story
(venue/boat, food/drinks, views, details). Off-topic shots (menus, payment
graphics, text boards, near-duplicates) are dropped. Orders were picked by
looking at contact sheets of every card, not by filename.

PHOTO_ORDER keys are page -> card number (1-based slider index on the page),
values are 1-based indexes into the card's current photo list. Indexes not
listed are dropped. The same order is applied to every language version that
uses the bpa-slider deck (image files are shared, only alt text differs).

Usage: python3 scripts/slider_photo_order.py [--check]
"""
import html
import json
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import quote, unquote

ROOT = Path(__file__).resolve().parent.parent

PHOTO_ORDER = {
    "best-walking-tours-budapest": {
        1: [  # guide in top hat with group at the lit castle gate
            "64f4a48b4133b5962d6ab7d2",
            "64f4a489ecf32dc7dd179a76",
            "64f4a7845f940d47fb880b33",
            "64f4a48be5685905ad1bc079",
            "64f4a48ba5f2e8bea5e2ae46",
            "64f4a48b4133b5962d6ab825",
        ],
        2: [  # lamp-lit tunnel walk
            "64f9a91e10ac16f2e2443a9e",
            "64f9a89e012119ea6136de78",
            "64f9a90a23415b24210a6b43",
            "64f9a93534cd09847ca17935",
            "64f9a8c5e5a13d680b19f3ee",
            "64f9a945012119ea61379ac4",
            "64f9a8e02324ecc4fb69ef07",
        ],
        3: [  # guide with group at the ghetto wall
            "64f9a974c8931dba57b758e6",
            "64f9a962741588aefc3ca6e7",
            "64f9a9c70c385a4c5457d028",
            "64f9a9a6dd44c9b55d0396c8",
            "64f9a9b5b54fef43d38c55f8",
            "64f9a97e0c385a4c54577c42",
        ],
        4: [  # Basilica street view
            "64f9a9e69165aa480e2191dd",
            "64f9aa08f8ee33524047cdf3",
            "64f9a9fcab96feb3ee4822df",
            "64f9aa2b7eeef24bb914cd46",
            "64f9aa420cfff4a85997ea49",
            "64f9aa18b2ff17a3658353d0",
        ],
        5: [  # Royal Palace courtyard
            "64f9aa665536d44a917a4be1",
            "64f9ab1ba5e26b34774d7e87",
            "64f9aaf8060885d81f1a5826",
            "64f9aae8db5d54ad86f5d18f",
            "64f9aab76a90d3270b8a5f22",
            "64f9ab0d3fe3f203a88ae5ae",
        ],
        6: [  # Fisherman's Bastion; drop 7 (map sign)
            "64f9ab4e4c6fedcabe27aa05",
            "64f9ab3947c2731b07da4884",
            "64f9ab9212c70e72edf275b2",
            "64f9ab7e9cecaecc5731db1e",
            "64f9ab5efd1746ad2656f8a0",
            "64f9ab6e97747bcde67d8abf",
        ],
    },
    "best-hostels-budapest": {
        1: [  # rooftop terrace
            "64a94406fe5dca443dcfeee5",
            "63b460511ecae0707a91a9fc",
            "63aef926eb85a17e98e01193",
            "63aef92513fcc88a48350ee7",
            "63aef922493ff733d6613db2",
            "63aef921d9415442ca96647b",
            "63aef9266c21e68d16e4b16a",
            "63aef926910c7054c7cefa1f",
            "63aef9203ba6d19eab0b717a",
        ],
        2: [  # guests at the bar
            "63aef9157013f819d68e2e1c",
            "63aef9185808d3607b270498",
            "63aef918a6bbf6adff3a3e94",
            "64a7dab4164c44de40679311",
            "63aef9166c21e60003e4b009",
            "63aef9150e332a523f9f300e",
            "63aef912493ff722e7613c9e",
            "63aef9153ca6980829000f48",
        ],
        3: [  # busy common room; drop 8 (chalkboard text)
            "63aef9910e332a1f839f36d1",
            "63aef9915b5d512baed7e33d",
            "63aef991a6bbf62b7e3a516e",
            "63aef991917c0c464343e0c1",
            "63aef99467bbedd0c4716ced",
            "63aef9965808d3a2d5270bdc",
            "63aef9963ca698878f001df5",
            "63aef9905808d3c5ad270b9b",
        ],
        4: [  # big lounge
            "63aef9bf3ca6989a610020e7",
            "63aef9be32bfdbdc4e3f5dea",
            "64a956ee944d79396c9730c2",
            "63aef9c2cee58c44bb1960ee",
            "63aef9be32bfdbd0533f5de9",
            "63aef9be892ff658fb9ca33f",
            "63aef9be32bfdb7d663f5de8",
            "63aef9bf92392d479560aae3",
        ],
        5: [  # bright lounge
            "63b45ede9dfe51ce60f63c17",
            "63b45d25d5b3809762c22aed",
            "63aef937493ff750c5613e6a",
            "6442664309951f1a6d28e8b2",
            "63b45d28eb88351b48fc92ff",
            "64a955153bb29577389129e8",
            "63b45f5e52440eb825de072a",
            "64a955ce7dba1d1588c93325",
            "63b45edb52787cbf17c70440",
        ],
        6: [  # social hall; drop 6 (whiteboard text)
            "63aef953eb85a192f0e0139d",
            "63aef954917c0c23e143dfc6",
            "63aef950917c0c24b843dfba",
            "63aef950917c0ccbc643dfb9",
            "63aef94f0e332a1b5d9f3327",
        ],
        7: [  # homely living room; drop 5 (annotated duplicate of 4)
            "63aef969d94154f616966c40",
            "63aef969a6bbf6d4603a4b50",
            "63aef969cee58c73f519585b",
            "63b4631ae4929f71abdcc0e0",
            "63aef9679c2695daf8aca622",
            "63aef96892392d38d560a51d",
            "63aef96692392d624960a4cc",
        ],
        8: [  # Basilica from the hostel
            "63aef94632bfdb4b043f5539",
            "63aef9422c152d3712e95a3d",
            "63b460a5eb8835761bfce593",
            "63aef94192392de8b160a1af",
            "64a950e4a4d8d06ce556b46a",
            "63aef946da54a218662cf8a8",
            "63aef9405808d36a7a27074c",
            "63aef9412c152dd671e95a27",
            "63aef941f706a176e0ea4e4c",
            "63aef94692392d481960a1bf",
        ],
    },
    "christmas-cruises-budapest": {
        1: [  # couple toasting with lit Parliament; drop 7, 8 (menus)
            "budapest-christmas-cruise-silverline-01.avif",
            "budapest-christmas-cruise-silverline-02.avif",
            "budapest-christmas-cruise-silverline-03.avif",
            "budapest-christmas-cruise-silverline-04.avif",
            "budapest-christmas-cruise-silverline-06.avif",
            "budapest-christmas-cruise-silverline-05.avif",
            "budapest-christmas-cruise-silverline-10.avif",
            "budapest-christmas-cruise-silverline-09.avif",
            "budapest-christmas-cruise-silverline-11.avif",
        ],
        2: [  # couple dining by the tree
            "budapest-christmas-cruise-folk-dinner-01.avif",
            "budapest-christmas-cruise-folk-dinner-05.avif",
            "budapest-christmas-cruise-folk-dinner-02.avif",
            "budapest-christmas-cruise-folk-dinner-03.avif",
            "budapest-christmas-cruise-folk-dinner-04.avif",
        ],
        3: [  # festive deck crowd with Parliament; drop 5 (blurred duplicate of 4)
            "budapest-christmas-cruise-christmas-market-01.avif",
            "budapest-christmas-cruise-christmas-market-03.avif",
            "budapest-christmas-cruise-christmas-market-02.avif",
            "budapest-christmas-cruise-christmas-market-04.avif",
        ],
        4: [  # prosecco pour with lit Parliament
            "budapest-christmas-cruise-mahart-mulled-prosecco-02.avif",
            "budapest-christmas-cruise-mahart-mulled-prosecco-05.avif",
            "budapest-christmas-cruise-mahart-mulled-prosecco-04.avif",
            "budapest-christmas-cruise-mahart-mulled-prosecco-03.avif",
            "budapest-christmas-cruise-mahart-mulled-prosecco-01.avif",
        ],
        5: [  # mulled wine toast at Parliament; drop 7 (menu), 12 (duplicate of 6)
            "budapest-christmas-cruise-mulled-wine-03.avif",
            "budapest-christmas-cruise-mulled-wine-11.avif",
            "budapest-christmas-cruise-mulled-wine-10.avif",
            "budapest-christmas-cruise-mulled-wine-01.avif",
            "budapest-christmas-cruise-mulled-wine-02.avif",
            "budapest-christmas-cruise-mulled-wine-09.avif",
            "budapest-christmas-cruise-mulled-wine-05.avif",
            "budapest-christmas-cruise-mulled-wine-04.avif",
            "budapest-christmas-cruise-mulled-wine-06.avif",
            "budapest-christmas-cruise-mulled-wine-08.avif",
            "budapest-christmas-cruise-mulled-wine-13.avif",
        ],
        6: [  # couple at dinner with folk dancers
            "budapest-christmas-cruise-grof-szechenyi-05.avif",
            "budapest-christmas-cruise-grof-szechenyi-01.avif",
            "budapest-christmas-cruise-grof-szechenyi-02.avif",
            "budapest-christmas-cruise-grof-szechenyi-03.avif",
            "budapest-christmas-cruise-grof-szechenyi-06.avif",
            "budapest-christmas-cruise-grof-szechenyi-07.avif",
            "budapest-christmas-cruise-grof-szechenyi-08.avif",
            "budapest-christmas-cruise-grof-szechenyi-10.avif",
            "budapest-christmas-cruise-grof-szechenyi-11.avif",
            "budapest-christmas-cruise-grof-szechenyi-13.avif",
            "budapest-christmas-cruise-grof-szechenyi-12.avif",
            "budapest-christmas-cruise-grof-szechenyi-14.avif",
            "budapest-christmas-cruise-grof-szechenyi-09.avif",
            "budapest-christmas-cruise-grof-szechenyi-04.avif",
        ],
        7: [  # guests on deck under lit castle; drop 5, 10 (menus)
            "budapest-christmas-cruise-river-diva-03.avif",
            "budapest-christmas-cruise-river-diva-04.avif",
            "budapest-christmas-cruise-river-diva-01.avif",
            "budapest-christmas-cruise-river-diva-02.avif",
            "budapest-christmas-cruise-river-diva-09.avif",
            "budapest-christmas-cruise-river-diva-13.avif",
            "budapest-christmas-cruise-river-diva-17.avif",
            "budapest-christmas-cruise-river-diva-06.avif",
            "budapest-christmas-cruise-river-diva-07.avif",
            "budapest-christmas-cruise-river-diva-11.avif",
            "budapest-christmas-cruise-river-diva-12.avif",
            "budapest-christmas-cruise-river-diva-08.avif",
            "budapest-christmas-cruise-river-diva-15.avif",
            "budapest-christmas-cruise-river-diva-16.avif",
            "budapest-christmas-cruise-river-diva-14.avif",
        ],
        8: [  # diners under the lit castle; drop 1 (duplicate of 4), 14 (payment logos)
            "663224a0b9517f8a892517a9",
            "64c683ce54d6bc13eb860a03",
            "66320ed9bd523888f1d2aa1f",
            "66320e4a4d501246b56e9d59",
            "6632100d16cd1e9d193ff6d6",
            "66322994ce51b39cdb68bb77",
            "6632102a9455a44b8ba053fb",
            "66322a0f443d1321ca0ccc05",
            "66322a2409d6d58a16b06276",
            "663229b884ffc8297ddcb52a",
            "66320defac2b58c3877cdbe5",
            "66320e04d3230ba7d3c2276e",
        ],
        9: [  # chimney cake with Parliament
            "budapest-christmas-cruise-cozy-chimney-cake-01.avif",
            "budapest-christmas-cruise-cozy-chimney-cake-04.avif",
            "budapest-christmas-cruise-cozy-chimney-cake-02.avif",
            "budapest-christmas-cruise-cozy-chimney-cake-03.avif",
            "budapest-christmas-cruise-cozy-chimney-cake-05.avif",
        ],
    },
    "new-years-eve-cruises-budapest": {
        1: [  # party hats and sparklers; drop 10, 18 (menus)
            "budapest-new-years-eve-cruise-silverline-07.avif",
            "budapest-new-years-eve-cruise-silverline-09.avif",
            "budapest-new-years-eve-cruise-silverline-01.avif",
            "budapest-new-years-eve-cruise-silverline-11.avif",
            "budapest-new-years-eve-cruise-silverline-12.avif",
            "budapest-new-years-eve-cruise-silverline-03.avif",
            "budapest-new-years-eve-cruise-silverline-14.avif",
            "budapest-new-years-eve-cruise-silverline-15.avif",
            "budapest-new-years-eve-cruise-silverline-16.avif",
            "budapest-new-years-eve-cruise-silverline-17.avif",
            "budapest-new-years-eve-cruise-silverline-13.avif",
            "budapest-new-years-eve-cruise-silverline-19.avif",
            "budapest-new-years-eve-cruise-silverline-02.avif",
            "budapest-new-years-eve-cruise-silverline-05.avif",
            "budapest-new-years-eve-cruise-silverline-08.avif",
            "budapest-new-years-eve-cruise-silverline-06.avif",
            "budapest-new-years-eve-cruise-silverline-04.avif",
        ],
        2: [  # folk dancer with guests
            "budapest-new-years-eve-cruise-hungaria-koncert-01.avif",
            "budapest-new-years-eve-cruise-hungaria-koncert-08.avif",
            "budapest-new-years-eve-cruise-hungaria-koncert-03.avif",
            "budapest-new-years-eve-cruise-hungaria-koncert-02.avif",
            "budapest-new-years-eve-cruise-hungaria-koncert-09.avif",
            "budapest-new-years-eve-cruise-hungaria-koncert-06.avif",
            "budapest-new-years-eve-cruise-hungaria-koncert-04.avif",
            "budapest-new-years-eve-cruise-hungaria-koncert-05.avif",
            "budapest-new-years-eve-cruise-hungaria-koncert-07.avif",
            "budapest-new-years-eve-cruise-hungaria-koncert-10.avif",
        ],
        3: [  # midnight fireworks
            "budapest-new-years-eve-cruise-portum-01.avif",
            "budapest-new-years-eve-cruise-portum-02.avif",
            "budapest-new-years-eve-cruise-portum-05.avif",
            "budapest-new-years-eve-cruise-portum-03.avif",
            "budapest-new-years-eve-cruise-portum-07.avif",
            "budapest-new-years-eve-cruise-portum-06.avif",
            "budapest-new-years-eve-cruise-portum-04.avif",
        ],
        4: [  # the boat lit at night
            "budapest-new-years-eve-cruise-todo-millennium-03.avif",
            "budapest-new-years-eve-cruise-todo-millennium-04.avif",
            "budapest-new-years-eve-cruise-todo-millennium-02.avif",
            "budapest-new-years-eve-cruise-todo-millennium-01.avif",
            "budapest-new-years-eve-cruise-todo-millennium-05.avif",
            "budapest-new-years-eve-cruise-todo-millennium-06.avif",
        ],
        5: [  # fireworks and party crowd
            "budapest-new-years-eve-cruise-budapest-boat-party-01.avif",
            "budapest-new-years-eve-cruise-budapest-boat-party-07.avif",
            "budapest-new-years-eve-cruise-budapest-boat-party-02.avif",
            "budapest-new-years-eve-cruise-budapest-boat-party-08.avif",
            "budapest-new-years-eve-cruise-budapest-boat-party-05.avif",
            "budapest-new-years-eve-cruise-budapest-boat-party-06.avif",
            "budapest-new-years-eve-cruise-budapest-boat-party-03.avif",
            "budapest-new-years-eve-cruise-budapest-boat-party-04.avif",
            "budapest-new-years-eve-cruise-budapest-boat-party-10.avif",
            "budapest-new-years-eve-cruise-budapest-boat-party-09.avif",
        ],
        6: [  # group with drinks and city lights
            "budapest-new-years-eve-cruise-dinner-cruise-budapest-02.avif",
            "budapest-new-years-eve-cruise-dinner-cruise-budapest-01.avif",
            "budapest-new-years-eve-cruise-dinner-cruise-budapest-03.avif",
            "budapest-new-years-eve-cruise-dinner-cruise-budapest-04.avif",
            "budapest-new-years-eve-cruise-dinner-cruise-budapest-05.avif",
        ],
        7: [  # candlelit gala dinner
            "budapest-new-years-eve-cruise-fattori-03.avif",
            "budapest-new-years-eve-cruise-fattori-01.avif",
            "budapest-new-years-eve-cruise-fattori-04.avif",
            "budapest-new-years-eve-cruise-fattori-02.avif",
        ],
    },
    "unlimited-prosecco-cruises-budapest": {
        1: [  # GYG product shots (t416276) lead: toast at the lit Parliament; own photos follow; drop rainy dock shot
            "/assets/cdn/60e43c7d6d05b671dff0dc1a/prosecco-cruise-duna-weser-01.avif",
            "/assets/cdn/60e43c7d6d05b671dff0dc1a/prosecco-cruise-duna-weser-02.avif",
            "/assets/cdn/60e43c7d6d05b671dff0dc1a/prosecco-cruise-duna-weser-03.avif",
            "/assets/cdn/60e43c7d6d05b671dff0dc1a/prosecco-cruise-duna-weser-04.avif",
            "63b858e8a4e49cb177974356",
            "63b858ea56f82257ea9e0c70",
            "/assets/cdn/60e43c7d6d05b671dff0dc1a/prosecco-cruise-duna-weser-05.avif",
            "63b858e9803ea5e532e13df1",
            "650beeaa6847525facb1a507",
            "63b858e8f731d90165d271cc",
            "63b858eb6b6209525005c772",
            "63b858eda4b537601bf3ceab",
        ],
        4: [  # drop the duplicate summer boat shot
            "prosecco-cruise-silverline-02.avif",
            "prosecco-cruise-silverline-04.avif",
            "prosecco-cruise-silverline-03.avif",
            "prosecco-cruise-silverline-01.avif",
            "prosecco-cruise-silverline-05.avif",
            "prosecco-cruise-silverline-07.avif",
            "prosecco-cruise-silverline-10.avif",
            "prosecco-cruise-silverline-06.avif",
            "prosecco-cruise-silverline-09.avif",
        ],
    },
}

SLIDER_RE = re.compile(r'<div[^>]*class="bpa-slider"')
IMG_RE = re.compile(r"<img [^>]*>")
LD_LOG = []
PILL_RE = re.compile(r'(<span class="bpa-pill">1 / )(\d+)(</span>)')


def balanced_end(h, start):
    depth = 0
    for m in re.finditer(r"<(/?)div\b[^>]*>", h[start:]):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return start + m.end()
    raise ValueError("unbalanced div")


def img_url(im):
    m = re.search(r'data-src="([^"]+)"', im) or re.search(r' src="([^"]+)"', im)
    return m.group(1)


def attr(im, name):
    m = re.search(r'\s%s="[^"]*"' % name, im)
    return m.group(0) if m else None


def fill_slot(template, im):
    """Put photo `im` into the slot `template` (keeps the slot's loading attrs)."""
    out = template
    out = re.sub(r'\salt="[^"]*"', lambda _: attr(im, "alt") or ' alt=""', out, count=1)
    u = img_url(im)
    if 'data-src="' in out:
        out = re.sub(r'data-src="[^"]*"', lambda _: 'data-src="%s"' % u, out, count=1)
    else:
        out = re.sub(r' src="[^"]*"', lambda _: ' src="%s"' % u, out, count=1)
    oe_t, oe_i = attr(out, "onerror"), attr(im, "onerror")
    if oe_t and oe_i:
        out = out.replace(oe_t, oe_i, 1)
    return out


def norm(u):
    """Compare slider URLs (&amp;, spaces) with JSON-LD URLs (%26, %20)."""
    return unquote(html.unescape(u)).lstrip("/")


def ld_url(u, like):
    return ("/" if like.startswith("/") else "") + quote(norm(u), safe="/:()")


def cluster_files(page):
    h = (ROOT / (page + ".html")).read_text()
    files = []
    for path, lang in re.findall(
            r'<link href="https://www.budapestadventures.com/([^"]*)" hreflang="([^"]+)" rel="alternate"', h):
        if lang == "x-default":
            continue
        path = unquote(path)
        for c in (path + ".html", path + "/index.html",
                  unicodedata.normalize("NFD", path) + ".html",
                  unicodedata.normalize("NFD", path) + "/index.html"):
            if (ROOT / c).exists():
                files.append((lang, ROOT / c))
                break
    return files


def photo_key(u):
    """Webflow asset hash when there is one, else the file name."""
    b = norm(u).split("/")[-1]
    m = re.match(r"([0-9a-f]{24})_", b)
    return m.group(1) if m else b


class MissingPhoto(Exception):
    pass


def reorder_page(h, orders):
    sliders = []
    for m in SLIDER_RE.finditer(h):
        sliders.append((m.start(), balanced_end(h, m.start())))
    urls = [[img_url(i) for i in IMG_RE.findall(h[a:b])] for a, b in sliders]
    first_swaps = []
    card_lists = {}
    for idx in sorted(orders, reverse=True):
        order = orders[idx]
        a, b = sliders[idx - 1]
        s = h[a:b]
        imgs = IMG_RE.findall(s)
        by_key = {photo_key(img_url(i)): i for i in imgs}
        new = []
        for k in order:
            if k in by_key:
                new.append(by_key[k])
            elif k.startswith("/assets/") and (ROOT / k.lstrip("/")).exists():
                # a photo added to the card: same alt as the card's other photos
                new.append('<img%s src="%s"/>' % (attr(imgs[0], "alt") or ' alt=""', k))
            else:
                raise MissingPhoto((idx, k))
        card_lists[idx] = ([img_url(i) for i in imgs], [img_url(i) for i in new])
        rest_t = imgs[1] if len(imgs) > 1 else imgs[0]
        tags = [fill_slot(imgs[0], new[0])] + [fill_slot(rest_t, im) for im in new[1:]]
        head = s[:s.find("<img ")]
        tail = s[s.rfind(">", 0, s.rfind("</div>")) + 1:]
        # keep the separator used between tags
        sep = "\n" if "\n<img " in s else ""
        new_s = head + sep.join(tags) + tail
        pre_start = h.rfind('<div class="bpa-media"', 0, a)
        pre = h[pre_start:a]
        pre_new, n = PILL_RE.subn(lambda m: m.group(1) + str(len(order)) + m.group(3), pre)
        assert n <= 1
        h = h[:pre_start] + pre_new + new_s + h[b:]
        if img_url(imgs[0]) != img_url(new[0]):
            first_swaps.append((idx, img_url(imgs[0]), img_url(new[0])))
    # JSON-LD: each card's ListItem image (and the Article lead image for card 1)
    # follows the card's first photo. Replace as text to keep the formatting, but
    # only when every occurrence of the old URL sits in one of those spots.
    def fix_ld(m):
        block = m.group(0)
        body = block[block.find(">") + 1:block.rfind("<")]
        try:
            data = json.loads(body)
        except ValueError:
            return block
        nodes = []
        def walk(o):
            if isinstance(o, dict):
                nodes.append(o)
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(data)
        def imgs_of(o):
            im = o.get("image")
            if isinstance(im, str):
                return [im]
            if isinstance(im, list):
                return [x for x in im if isinstance(x, str)]
            return []
        def count(lst, u):
            return sum(1 for x in lst if norm(x).endswith(norm(u)))
        for idx, old, new_u in first_swaps:
            allowed = 0
            for n in nodes:
                if n.get("@type") == "ListItem" and n.get("position") == idx and isinstance(n.get("item"), dict):
                    allowed += count(imgs_of(n["item"]), old)
                if idx == 1 and n.get("@type") in ("Article", "BlogPosting", "WebPage"):
                    allowed += count(imgs_of(n), old)
            total = sum(count(imgs_of(n), old) for n in nodes)
            spellings = {x for x in re.findall(r'"([^"]+)"', block)
                         if "/assets/" in x and norm(x).endswith(norm(old))}
            if allowed and allowed == total and sum(block.count('"%s"' % x) for x in spellings) == allowed:
                for x in spellings:
                    block = block.replace('"%s"' % x, '"%s%s"' % (x[:x.find("/assets/")], ld_url(new_u, "/")))
                LD_LOG.append((idx, "ok"))
            elif total:
                LD_LOG.append((idx, "skip: old url also used elsewhere (%d/%d)" % (allowed, total)))
        # Multi-photo image lists made from one card's slider (hostels): follow
        # the new slider order, drop removed photos, lead with the new first photo.
        def fix_list(lm):
            items = re.findall(r'"([^"]*)"', lm.group(2))
            if len(items) < 2:
                return lm.group(0)
            for idx, (old_list, new_list) in card_lists.items():
                old_n = [norm(u) for u in old_list]
                if not all(norm(u) in old_n for u in items):
                    continue
                new_n = [norm(u) for u in new_list]
                kept = sorted([u for u in items if norm(u) in new_n], key=lambda u: new_n.index(norm(u)))
                if not kept or norm(kept[0]) != new_n[0]:
                    kept = [ld_url(new_list[0], items[0])] + kept
                kept = kept[:len(items)]
                if kept == items:
                    return lm.group(0)
                inner = lm.group(2)
                lead = re.match(r'\s*', inner).group(0)
                trail = re.search(r'\s*$', inner).group(0)
                sep = re.search(r'",(\s*)"', inner)
                sep = "," + (sep.group(1) if sep else " ")
                LD_LOG.append((idx, "list reordered"))
                return lm.group(1) + lead + sep.join('"%s"' % u for u in kept) + trail + "]"
            return lm.group(0)
        block = re.sub(r'("image":\s*\[)([^\]]*)\]', fix_list, block)
        return block
    h = re.sub(r'<script[^>]*type="application/ld\+json"[^>]*>.*?</script>', fix_ld, h, flags=re.S)
    return h, urls, first_swaps


def main():
    check = "--check" in sys.argv
    report = {}
    for page, orders in PHOTO_ORDER.items():
        files = cluster_files(page)
        done, skipped = [], []
        for lang, f in files:
            h = f.read_text()
            if 'class="bpa-slider"' not in h:
                skipped.append(lang + " (old w-slider template)")
                continue
            try:
                new_h, urls, _ = reorder_page(h, orders)
            except MissingPhoto as e:
                skipped.append("%s (different photo set: %s)" % (lang, e))
                continue
            if new_h != h:
                if not check:
                    f.write_text(new_h)
                done.append(lang)
        report[page] = {"changed": done, "skipped": skipped}
    print(json.dumps(report, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
