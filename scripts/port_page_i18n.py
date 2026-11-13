#!/usr/bin/env python3
"""Port an English page to its translated URLs using the EN page as the template.

The English page is the single source of truth for structure and content. For each
language that already has a translated URL (hreflang alternate on the EN page), this
script translates the EN page's text with Claude and writes the result to that
translated file, so translations get the same layout as English.

    python3 scripts/port_page_i18n.py best-night-cruises-budapest.html --langs de,hu
    python3 scripts/port_page_i18n.py best-night-cruises-budapest.html            # all 21
    python3 scripts/port_page_i18n.py best-night-cruises-budapest.html --dry-run  # no API, keeps EN text

Needs ANTHROPIC_API_KEY (environment or the repo .env) and `pip install anthropic bs4`.
Translations are cached in data/i18n/port/<page>/<lang>.json, so re-runs only send
new or changed segments. After porting, run scripts/sync_layout.py for the menu/footer.

Rules sent to the model: keep brand, company, boat, place and street names as written
(Legenda, Silverline, Vigadó tér, ...), keep every HTML tag and attribute, numbers,
prices, times and URLs unchanged, no em dashes, and no "independent / unsponsored /
undercover / paid our own tickets" style claims.
"""
import argparse
import copy
import hashlib
import json
import os
import re
import sys
import urllib.parse

from bs4 import BeautifulSoup, NavigableString, Comment

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.budapestadventures.com"
MODEL = "claude-opus-5-5"
LANG_NAMES = {
    "hu": "Hungarian", "de": "German", "fr": "French", "it": "Italian", "es": "Spanish",
    "ro": "Romanian", "pl": "Polish", "nl": "Dutch", "cs": "Czech", "sk": "Slovak",
    "pt": "Portuguese", "ru": "Russian", "hr": "Croatian", "sr": "Serbian (Cyrillic script)",
    "bg": "Bulgarian", "el": "Greek", "tr": "Turkish", "uk": "Ukrainian", "he": "Hebrew",
    "ja": "Japanese", "ko": "Korean",
}
INLINE = {"a", "strong", "b", "em", "i", "span", "br", "small", "sup", "sub", "u", "mark", "abbr", "code", "s"}
SKIP = {"script", "style", "svg", "noscript", "template", "iframe", "code"}
ATTRS = ("alt", "title", "aria-label", "placeholder", "data-tooltip", "data-label")
JSONLD_KEYS = {"name", "description", "headline", "text", "alternateName", "caption", "about"}

SYSTEM = """You translate pages of Budapest Adventures, a travel guide to Budapest Danube cruises, from English into {lang}.

Rules:
- Translate naturally for travelers reading {lang}; keep the meaning, tone and length close to the English.
- Each item is an HTML fragment. Keep every tag, attribute and attribute value exactly as given; translate only the human-readable text between tags. Keep leading/trailing spaces.
- Never translate brand, company, boat, venue, product, place or street names (for example Legenda, Silverline, Duna-Weser, Portum, Rubin, GetYourGuide, Viator, Tripadvisor, Budapest Adventures, Vigadó tér, Jane Haining rakpart, Akadémia, Széchenyi). Keep the site name "Budapest Adventures" in English.
- Keep numbers, prices, currencies, dates, times, ratings, dock numbers and URLs exactly.
- Do not use em dashes (—); use a comma, colon or en dash with spaces instead.
- Do not add claims about being independent, unbiased, unsponsored, undercover, anonymous or paying for our own tickets, even if the wording would make them sound natural.
- Return every id you were given, once, with its translation."""

SCHEMA = {
    "type": "object",
    "properties": {
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"id": {"type": "string"}, "html": {"type": "string"}},
                "required": ["id", "html"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["items"],
    "additionalProperties": False,
}


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def load_env_key():
    if os.environ.get("ANTHROPIC_API_KEY"):
        return
    import subprocess
    candidates = [os.path.join(ROOT, ".env")]
    try:  # in a git worktree, .env lives in the main checkout
        common = subprocess.run(["git", "rev-parse", "--git-common-dir"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        if common:
            candidates.append(os.path.join(os.path.dirname(os.path.abspath(os.path.join(ROOT, common))), ".env"))
    except OSError:
        pass
    for env in candidates:
        if not os.path.exists(env):
            continue
        for line in open(env, encoding="utf-8"):
            if line.startswith("ANTHROPIC_API_KEY="):
                os.environ["ANTHROPIC_API_KEY"] = line.split("=", 1)[1].strip().strip('"').strip("'")
                return


def url_to_file(url):
    p = urllib.parse.unquote(url.split(SITE, 1)[-1]).strip("/")
    for c in ([p + ".html", p + "/index.html"] if p else ["index.html"]):
        if os.path.isfile(os.path.join(ROOT, c)):
            return c
    rw = {r["source"]: r["destination"] for r in json.loads(read("vercel.json")).get("rewrites", []) if ":" not in r["source"]}
    d = rw.get("/" + p)
    if d:
        for c in [d.strip("/") + ".html", d.strip("/") + "/index.html"]:
            if os.path.isfile(os.path.join(ROOT, c)):
                return c
    return None


def alternates(html):
    return {lg: href for href, lg in re.findall(r'<link href="([^"]+)" hreflang="([a-zA-Z-]+)" rel="alternate"', html)}


def link_map():
    """EN internal path -> {lang: localized path}, from the hreflang tags of every EN page."""
    out = {}
    locs = re.findall(r"<loc>([^<]*)</loc>", read("sitemap.xml"))
    for u in locs:
        path = "/" + u.split(SITE, 1)[-1].strip("/")
        if re.match(r"^/[a-z]{2}(/|$)", path) and path.split("/")[1] in LANG_NAMES:
            continue
        f = url_to_file(u)
        if not f:
            continue
        alts = alternates(read(f))
        out[path.rstrip("/") or "/"] = {lg: "/" + h.split(SITE, 1)[-1].strip("/") for lg, h in alts.items()}
    return out


# ---------------------------------------------------------------- segments
def is_leaf_block(el):
    if el.name in INLINE or el.name in SKIP:
        return False
    has_text = False
    for c in el.children:
        if isinstance(c, Comment):
            continue
        if isinstance(c, NavigableString):
            if c.strip():
                has_text = True
        elif c.name in INLINE:
            if c.get_text(strip=True):
                has_text = True
            if any(d.name and d.name not in INLINE for d in c.find_all(True)):
                return False
        else:
            if c.name not in SKIP and c.get_text(strip=True):
                return False
    return has_text


def translatable(text):
    t = re.sub(r"<[^>]+>", "", text)
    return bool(re.search(r"[A-Za-z]{2}", t))


def collect(soup):
    """Return list of (kind, ref, source_html). kind: 'inner' | 'text' | 'attr' | 'meta' | 'title' | 'jsonld'."""
    segs = []
    body = soup.body
    hdr = body.find("header", class_="ltt-navbar")
    ftr = body.find(lambda t: t.name in ("footer", "section") and "footer-dark" in (t.get("class") or []))

    def in_chrome(el):
        return (hdr and (el is hdr or hdr in el.parents)) or (ftr and (el is ftr or ftr in el.parents))

    done = set()
    for el in body.find_all(True):
        if in_chrome(el) or el.name in SKIP or any(p.name in SKIP for p in el.parents):
            continue
        if any(id(p) in done for p in el.parents):
            continue
        if is_leaf_block(el):
            inner = el.decode_contents()
            if translatable(inner):
                segs.append(("inner", el, inner))
            done.add(id(el))
    # loose text nodes in mixed containers
    for s in body.find_all(string=True):
        if isinstance(s, Comment) or not s.strip() or not translatable(s):
            continue
        el = s.parent
        if in_chrome(el) or el.name in SKIP or any(p.name in SKIP for p in el.parents):
            continue
        if id(el) in done or any(id(p) in done for p in el.parents):
            continue
        segs.append(("text", s, str(s)))
    for el in body.find_all(True):
        if in_chrome(el):
            continue
        for a in ATTRS:
            v = el.get(a)
            if isinstance(v, str) and translatable(v):
                segs.append(("attr", (el, a), v))
    if soup.title and soup.title.string and translatable(soup.title.string):
        segs.append(("title", soup.title, soup.title.string))
    for m in soup.find_all("meta"):
        key = m.get("name") or m.get("property") or ""
        if key in ("description", "og:title", "og:description", "twitter:title", "twitter:description", "og:image:alt") and translatable(m.get("content", "")):
            segs.append(("meta", m, m["content"]))
    for sc in soup.find_all("script"):
        m = re.search(r"window\.LTT_PAGE_CONFIG\s*=\s*(\{.*?\});", sc.string or "", re.S)
        if m:
            try:
                cfg = json.loads(m.group(1))
                cfg.setdefault("pickLabel", "PICK")  # floating bar badge text; JS falls back to English
                segs.append(("pagecfg", sc, cfg))
            except ValueError:
                pass
    for sc in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(sc.string or "")
        except ValueError:
            continue
        segs.append(("jsonld", sc, data))
    return segs


def jsonld_strings(node, acc):
    if isinstance(node, dict):
        for k, v in node.items():
            if k in JSONLD_KEYS and isinstance(v, str) and translatable(v) and not v.startswith("http"):
                acc.append(v)
            else:
                jsonld_strings(v, acc)
    elif isinstance(node, list):
        for v in node:
            jsonld_strings(v, acc)


def jsonld_apply(node, tr):
    if isinstance(node, dict):
        return {k: (tr.get(v, v) if k in JSONLD_KEYS and isinstance(v, str) else jsonld_apply(v, tr)) for k, v in node.items()}
    if isinstance(node, list):
        return [jsonld_apply(v, tr) for v in node]
    return node


def cfg_strings(node, acc):
    if isinstance(node, dict):
        for k, v in node.items():
            if k.lower().endswith("id") or k.lower() in ("href", "url", "anchor"):
                continue
            cfg_strings(v, acc)
    elif isinstance(node, list):
        for v in node:
            cfg_strings(v, acc)
    elif isinstance(node, str) and translatable(node) and not node.startswith(("http", "#", "/")):
        acc.append(node)


def cfg_apply(node, tr, k=""):
    if isinstance(node, dict):
        return {kk: (v if kk.lower().endswith("id") or kk.lower() in ("href", "url", "anchor") else cfg_apply(v, tr, kk)) for kk, v in node.items()}
    if isinstance(node, list):
        return [cfg_apply(v, tr, k) for v in node]
    if isinstance(node, str):
        return tr.get(node, node)
    return node


def key(s):
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:12]


# ---------------------------------------------------------------- translation
def translate(strings, lang, cache_path, dry_run):
    cache = json.load(open(cache_path, encoding="utf-8")) if os.path.exists(cache_path) else {}
    todo = [s for s in dict.fromkeys(strings) if key(s) not in cache]
    if dry_run:
        return {s: cache.get(key(s), s) for s in strings}
    if todo:
        import anthropic
        client = anthropic.Anthropic()
        batch, size = [], 0
        batches = []
        for s in todo:
            if batch and size + len(s) > 12000:
                batches.append(batch); batch, size = [], 0
            batch.append(s); size += len(s)
        if batch:
            batches.append(batch)
        for i, b in enumerate(batches, 1):
            payload = [{"id": key(s), "html": s} for s in b]
            with client.messages.stream(
                model=MODEL,
                max_tokens=64000,
                system=SYSTEM.format(lang=LANG_NAMES[lang]),
                output_config={"effort": "low", "format": {"type": "json_schema", "schema": SCHEMA}},
                messages=[{"role": "user", "content": json.dumps({"items": payload}, ensure_ascii=False)}],
            ) as stream:
                msg = stream.get_final_message()
            if msg.stop_reason not in ("end_turn",):
                raise RuntimeError(f"{lang} batch {i}: stop_reason={msg.stop_reason}")
            text = next(bl.text for bl in msg.content if bl.type == "text")
            got = {it["id"]: it["html"] for it in json.loads(text)["items"]}
            missing = [p["id"] for p in payload if p["id"] not in got]
            if missing:
                raise RuntimeError(f"{lang} batch {i}: {len(missing)} ids missing in response")
            cache.update(got)
            os.makedirs(os.path.dirname(cache_path), exist_ok=True)
            json.dump(cache, open(cache_path, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
            print(f"  {lang}: batch {i}/{len(batches)} ({len(b)} segments)", flush=True)
    return {s: cache[key(s)] for s in strings}


def tags_of(h):
    """Tags with translatable attribute values blanked, so translated tooltips/alt text still match."""
    norm = lambda t: re.sub(r'\b(%s)="[^"]*"' % "|".join(ATTRS), r'\1=""', t)
    return sorted(norm(t) for t in re.findall(r"<[^>]+>", h))


# ---------------------------------------------------------------- build
def port(en_file, lang, target_file, links, dry_run):
    en_html = read(en_file)
    soup = BeautifulSoup(en_html, "html.parser")
    segs = collect(soup)
    strings = []
    for kind, ref, src in segs:
        if kind == "jsonld":
            jsonld_strings(src, strings)
        elif kind == "pagecfg":
            cfg_strings(src, strings)
        else:
            strings.append(src)
    page = os.path.splitext(en_file.replace("/", "__"))[0]
    tr = translate(strings, lang, os.path.join(ROOT, "data", "i18n", "port", page, f"{lang}.json"), dry_run)

    bad = 0
    for kind, ref, src in segs:
        if kind == "inner":
            new = tr[src]
            if tags_of(new) != tags_of(src):
                bad += 1
                new = src if dry_run else new
            ref.clear()
            for node in BeautifulSoup(new, "html.parser").contents:
                ref.append(copy.copy(node))
        elif kind == "text":
            ref.replace_with(tr[src])
        elif kind == "attr":
            el, a = ref
            el[a] = tr[src]
        elif kind == "title":
            ref.string = tr[src]
        elif kind == "meta":
            ref["content"] = tr[src]
        elif kind == "jsonld":
            ref.string = json.dumps(jsonld_apply(src, tr), ensure_ascii=False)
        elif kind == "pagecfg":
            new = json.dumps(cfg_apply(src, tr), ensure_ascii=False)
            ref.string = re.sub(r"(window\.LTT_PAGE_CONFIG\s*=\s*)\{.*?\};", lambda m: m.group(1) + new + ";", ref.string, count=1, flags=re.S)

    target_url = SITE + "/" + target_file.replace("/index.html", "").replace(".html", "")
    html_tag = soup.find("html")
    html_tag["lang"] = lang
    if lang == "he":
        html_tag["dir"] = "rtl"
    elif html_tag.has_attr("dir"):
        del html_tag["dir"]
    can = soup.find("link", rel="canonical")
    if can:
        can["href"] = target_url
    for m in soup.find_all("meta", property="og:url"):
        m["content"] = target_url
    # internal links -> localized equivalents
    for a in soup.find_all("a", href=True):
        h = a["href"]
        if not h.startswith("/") or h.startswith("//"):
            continue
        path, _, frag = h.partition("#")
        path = path.rstrip("/") or "/"
        loc = links.get(path, {}).get(lang)
        if loc:
            a["href"] = loc + (("#" + frag) if frag else "")
    out = str(soup)
    with open(os.path.join(ROOT, target_file), "w", encoding="utf-8") as fh:
        fh.write(out)
    return len(strings), bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("en_file")
    ap.add_argument("--langs", default=",".join(LANG_NAMES))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    load_env_key()
    if not args.dry_run and not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set (environment or .env)")
    alts = alternates(read(args.en_file))
    links = link_map()
    for lang in args.langs.split(","):
        href = alts.get(lang)
        target = url_to_file(href) if href else None
        if not target:
            print(f"{lang}: no translated URL for {args.en_file}, skipped")
            continue
        n, bad = port(args.en_file, lang, target, links, args.dry_run)
        print(f"{lang}: {target} ({n} strings, {bad} tag mismatches)")


if __name__ == "__main__":
    main()
