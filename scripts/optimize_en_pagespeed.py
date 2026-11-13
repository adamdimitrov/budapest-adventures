#!/usr/bin/env python3
"""PageSpeed pass for the English pages (idempotent; safe to re-run).

1. Third-party tags (Clarity, GTM, gtag.js, Meta Pixel, GetYourGuide analytics)
   load on the first scroll/touch/mousemove/click/keydown, or 7 s after `load`.
   Their queue stubs (dataLayer, gtag(), fbq(), clarity()) stay inline, so no
   event is lost. Hotjar/Emerald fallbacks move to 7 s as well.
2. Webflow's render-blocking webfont.js becomes async (WebFontConfig).
3. The dead first-party Google tag path (404 on Vercel) is removed.
4. /tourcms-sync.js gets `defer` where it was parser-blocking.
5. The two shared Webflow stylesheets (~300 KB + ~215 KB raw) are replaced by
   per-page purged copies under /css/purged/ (content-hashed filenames, since
   /css/* is served `immutable`).
6. The header logo <img> uses a 96 px WebP instead of the 256 px PNG.

Usage: python3 scripts/optimize_en_pagespeed.py [--check]
"""
import hashlib
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

EN_PAGES = """index.html river.html dinner.html candlelit-dinner-cruise.html
best-night-cruises-budapest.html thermal-baths-budapest.html
best-private-boat-tours-budapest.html unlimited-prosecco-cruises-budapest.html
best-walking-tours-budapest.html best-hostels-budapest.html
budapest-card-is-it-worth-it.html budapest-travel-guide.html
budapest-airport-to-city-center.html budapest-parliament.html
budapest-river-cruise-group-booking.html budapest-tourism-statistics.html
about.html contact.html
best-budapest-river-cruises.html best-dinner-cruises-budapest.html
best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest/index.html""".split()
# NB: with cleanUrls, Vercel serves an existing <slug>.html before applying a
# rewrite, so /best-budapest-river-cruises is best-budapest-river-cruises.html
# (not river.html) and /best-dinner-cruises-budapest is
# best-dinner-cruises-budapest.html (not dinner.html). Both copies are covered.

DEFER_EVENTS = "['scroll','touchstart','mousemove','click','keydown']"
LOADER = (
    '<script id="bpa-defer">(function(w){var q=[],d=0;function run(){if(d)return;d=1;'
    'for(var i=0;i<q.length;i++){try{q[i]()}catch(e){}}q=[]}'
    'w.bpaDefer=function(f){d?f():q.push(f)};'
    + DEFER_EVENTS +
    ".forEach(function(e){w.addEventListener(e,run,{once:true,passive:true})});"
    "w.addEventListener('load',function(){setTimeout(run,7000)})})(window);</script>"
)


def inject_script(src, attrs=""):
    return ("<script>bpaDefer(function(){var s=document.createElement('script');s.async=1;"
            f"{attrs}s.src='{src}';document.head.appendChild(s)}});</script>")


def optimize_scripts(h):
    # deferred loader, right after <head> so it precedes Clarity
    if 'id="bpa-defer"' not in h:
        h = re.sub(r'(<head[^>]*>)', lambda m: m.group(1) + LOADER, h, count=1)

    # Clarity
    h = re.sub(
        r'(?<!bpaDefer\(function\(\)\{)t=l\.createElement\(r\);t\.async=1;t\.src="https://www\.clarity\.ms/tag/"\+i;\s*'
        r'y=l\.getElementsByTagName\(r\)\[0\];y\.parentNode\.insertBefore\(t,y\);',
        'bpaDefer(function(){t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;'
        'y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);});', h)

    # GTM container
    h = re.sub(r"('https://www\.googletagmanager\.com/gtm\.js\?id='\+i\+dl;)\s*f\.parentNode\.insertBefore\(j,f\);",
               r"\1bpaDefer(function(){f.parentNode.insertBefore(j,f);});", h)

    # gtag.js loader
    h = re.sub(r'<script async="" src="(https://www\.googletagmanager\.com/gtag/js\?id=[\w-]+)"></script>',
               lambda m: inject_script(m.group(1)), h)

    # Meta Pixel base code (Webflow flavour, minified)
    h = re.sub(r't=b\.createElement\(e\);t\.async=!0;t\.src=v;s=b\.getElementsByTagName\(e\)\[0\];'
               r's\.parentNode\.insertBefore\(t,s\)(?!\}\))',
               'bpaDefer(function(){t=b.createElement(e);t.async=!0;t.src=v;'
               's=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)})', h)

    # GetYourGuide partner analytics
    h = re.sub(r'<script async="" data-gyg-partner-id="(\w+)" defer="" '
               r'src="(https://widget\.getyourguide\.com/dist/pa\.umd\.production\.min\.js)"></script>',
               lambda m: inject_script(m.group(2), f"s.setAttribute('data-gyg-partner-id','{m.group(1)}');"), h)

    # dead Webflow first-party Google tag path (404 on Vercel)
    h = re.sub(r'<script async="" src="/nvhc9u4gxsagNjBlNDNjN2Q2ZDA1YjY3MWRmZjBkYzFh/[\w-]+"></script>', '', h)

    # Hotjar / Emerald fallback timers inside the Lighthouse window
    h = h.replace('setTimeout(loadHotjar, 4500)', 'setTimeout(loadHotjar, 7000)')
    h = h.replace('setTimeout(loadEmerald, 6000)', 'setTimeout(loadEmerald, 7000)')

    # webfont.js: parser-blocking -> async
    h = re.sub(
        r'<script src="(https://ajax\.googleapis\.com/ajax/libs/webfont/1\.6\.26/webfont\.js)" type="text/javascript"></script>'
        r'<script type="text/javascript">WebFont\.load\((\{.*?\})\);</script>',
        lambda m: f'<script>WebFontConfig={m.group(2)};</script><script async src="{m.group(1)}"></script>',
        h, flags=re.S)

    # Google Fonts stylesheet still render-blocking on some pages -> async swap
    h = re.sub(r'<link href="(https://fonts\.googleapis\.com/css2\?[^"]*)" rel="stylesheet"/>',
               r'''<link href="\1" media="print" onload="this.media='all'" rel="stylesheet"/>''', h)

    # tourcms-sync.js: parser-blocking -> defer (handles readyState itself)
    h = h.replace('<script src="/tourcms-sync.js?v=20261113"></script>', '<script defer src="/tourcms-sync.js?v=20261113"></script>')
    return h


# ---------------------------------------------------------------- logo
LOGO_PNG = 'assets/budapest-adventures-logo.png'
LOGO_WEBP = 'assets/budapest-adventures-logo-96.webp'


def ensure_logo():
    if not os.path.exists(LOGO_WEBP):
        from PIL import Image
        im = Image.open(LOGO_PNG).convert('RGBA').resize((96, 96), Image.LANCZOS)
        im.save(LOGO_WEBP, 'WEBP', quality=88, method=6)


def optimize_logo(h):
    return re.sub(r'(<img\b[^>]*?\s)src="/?assets/budapest-adventures-logo\.png"',
                  r'\1src="/assets/budapest-adventures-logo-96.webp"', h)


# ---------------------------------------------------------------- CSS purge
def _skip_string(css, i):
    q = css[i]
    i += 1
    while i < len(css) and css[i] != q:
        i += 2 if css[i] == '\\' else 1
    return i + 1


def parse_css(css):
    """Return list of (prelude, body) where body is a str (declarations) or
    a list (nested rules) or None (statement at-rule like @charset)."""
    nodes, i, n, start = [], 0, len(css), 0
    while i < n:
        c = css[i]
        if c in '"\'':
            i = _skip_string(css, i)
            continue
        if css.startswith('/*', i):
            j = css.find('*/', i + 2)
            i = n if j < 0 else j + 2
            start = i if not css[start:i].strip().replace('/*', '').strip() else start
            continue
        if c == ';' and css[start:i].strip().startswith('@'):
            nodes.append((css[start:i].strip(), None))
            i += 1
            start = i
            continue
        if c == '{':
            prelude = css[start:i].strip()
            depth, j = 1, i + 1
            while j < n and depth:
                if css[j] in '"\'':
                    j = _skip_string(css, j)
                    continue
                if css[j] == '{':
                    depth += 1
                elif css[j] == '}':
                    depth -= 1
                j += 1
            inner = css[i + 1:j - 1]
            low = prelude.lower()
            if low.startswith(('@media', '@supports', '@layer', '@container', '@document')):
                nodes.append((prelude, parse_css(inner)))
            else:
                nodes.append((prelude, inner))
            i = j
            start = i
            continue
        if c == '}':  # stray
            i += 1
            start = i
            continue
        i += 1
    return nodes


def split_selectors(sel):
    out, depth, cur = [], 0, ''
    for ch in sel:
        if ch in '([':
            depth += 1
        elif ch in ')]':
            depth -= 1
        if ch == ',' and depth == 0:
            out.append(cur)
            cur = ''
        else:
            cur += ch
    out.append(cur)
    return [s.strip() for s in out if s.strip()]


ALWAYS_PREFIX = ('w-mod-', 'wf-', 'w--')


def selector_used(sel, used, prefixes):
    s = re.sub(r'\[[^\]]*\]', '', sel)                       # attribute selectors
    s = re.sub(r':(?:not|has|where|is)\((?:[^()]|\([^()]*\))*\)', '', s)  # functional pseudos
    s = re.sub(r'::?[\w-]+(\([^)]*\))?', '', s)            # other pseudos
    for kind, name in re.findall(r'([.#])(-?[_a-zA-Z][\w-]*)', s):
        if name in used or name.startswith(ALWAYS_PREFIX):
            continue
        if any(name.startswith(p) for p in prefixes):
            continue
        return False
    return True


def serialize(nodes, used, prefixes):
    out = []
    for prelude, body in nodes:
        if body is None:
            out.append(prelude + ';')
        elif isinstance(body, list):
            inner = serialize(body, used, prefixes)
            if inner:
                out.append(prelude + '{' + inner + '}')
        elif prelude.startswith('@'):
            out.append(prelude + '{' + body + '}')
        else:
            keep = [s for s in split_selectors(prelude) if selector_used(s, used, prefixes)]
            if keep:
                out.append(','.join(keep) + '{' + body + '}')
    return ''.join(out)


_JS_TOKENS = None


def js_tokens():
    global _JS_TOKENS
    if _JS_TOKENS is None:
        toks = set()
        for d, _, files in os.walk('.'):
            if 'node_modules' in d or '/.git' in d:
                continue
            for f in files:
                if f.endswith('.js') and (d.startswith('./assets') or d in ('.', './js')):
                    try:
                        toks |= set(re.findall(r'[\w-]+', open(os.path.join(d, f), errors='ignore').read()))
                    except OSError:
                        pass
        _JS_TOKENS = toks
    return _JS_TOKENS


_PARSED = {}


def purge_for_page(h, css_path):
    if css_path not in _PARSED:
        _PARSED[css_path] = parse_css(open(css_path).read())
    used = set(re.findall(r'[\w-]+', h)) | js_tokens()
    prefixes = tuple(t for t in used if t.endswith('-') and len(t) > 2)
    return serialize(_PARSED[css_path], used, prefixes)


WF_CSS_RE = re.compile(r'href="/(assets/cdn/[0-9a-f]+/css/[\w.]+\.webflow\.shared\.[0-9a-f]+\.min\.css)"')


def optimize_css(h, page):
    def repl(m):
        src = m.group(1)
        purged = purge_for_page(h, src)
        digest = hashlib.sha1(purged.encode()).hexdigest()[:10]
        base = os.path.basename(src).replace('.min.css', '')
        out = f'css/purged/{page[:-5].replace("/", "--")}.{base}.{digest}.css'
        os.makedirs('css/purged', exist_ok=True)
        if not os.path.exists(out):
            open(out, 'w').write(purged)
        return f'href="/{out}"'
    return WF_CSS_RE.sub(repl, h)


# LCP images (per PSI mobile) that lack a priority hint
LCP_HINTS = {
    'best-hostels-budapest.html': 'best-unlimited-prosecco-cruises-hero-p-500.webp',
}


def responsive_preloads(h):
    """An image preload without imagesrcset fetches the full-size file even when
    the <img> it targets picks a smaller srcset candidate (double download on
    mobile). Mirror the img's srcset/sizes onto the preload."""
    def repl(m):
        tag = m.group(0)
        if 'imagesrcset' in tag:
            return tag
        href = re.search(r'href="([^"]+)"', tag).group(1)
        img = re.search(r'<img\b[^>]*\ssrc="' + re.escape(href) + r'"[^>]*>', h)
        if not img:
            return tag
        ss = re.search(r'\ssrcset="([^"]+)"', img.group(0))
        sz = re.search(r'\ssizes="([^"]+)"', img.group(0))
        if not (ss and sz):
            return tag
        return tag.replace(' rel="preload"', f' imagesizes="{sz.group(1)}" imagesrcset="{ss.group(1)}" rel="preload"')
    return re.sub(r'<link as="image"[^>]*rel="preload"[^>]*/?>', repl, h)


def optimize_lcp(h, page):
    h = responsive_preloads(h)
    needle = LCP_HINTS.get(page)
    if not needle:
        return h
    return re.sub(r'<img (?![^>]*fetchpriority)(?=[^>]*src="[^"]*' + re.escape(needle) + '")',
                  '<img fetchpriority="high" ', h, count=1)


def main():
    check = '--check' in sys.argv
    ensure_logo()
    # editorial stylesheet: drop the render-blocking @import chain (every page
    # using it already loads the same families via an async <link>)
    ed = 'css/editorial-luxury.css'
    s = open(ed).read()
    s2 = re.sub(r"@import url\('https://fonts\.googleapis\.com/css2\?[^']*'\);\s*", '', s)
    if s2 != s and not check:
        open(ed, 'w').write(s2)

    for page in EN_PAGES:
        h = open(page).read()
        new = optimize_scripts(h)
        new = optimize_logo(new)
        new = optimize_lcp(new, page)
        new = optimize_css(new, page)
        if new != h:
            print(('would update ' if check else 'updated ') + page)
            if not check:
                open(page, 'w').write(new)


if __name__ == '__main__':
    main()
