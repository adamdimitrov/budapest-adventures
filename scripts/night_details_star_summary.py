"""Replace the old icon-badge rating row in night-cruise detail headers with the
deck card's star summary (stars + score + 'N reviews · X sites' + per-site popover).
Each language copies its own (already translated) deck block, so no new strings."""
import re, sys

FILES = [
    "best-night-cruises-budapest.html",
    "hu/legjobb-éjszakai-hajóutak-budapest/index.html",
    "de/nacht-bootsfahrten-budapest/index.html",
    "nl/avondcruises-boedapest/index.html",
    "fr/croisieres-nocturnes-budapest/index.html",
    "it/crociere-notturne-budapest/index.html",
    "es/cruceros-nocturnos-budapest/index.html",
]


def block_end(s, start, tag="div"):
    """Index just past the element that opens at `start` (balanced tags)."""
    depth, i = 0, start
    pat = re.compile(r"<(/?)%s\b[^>]*>" % tag)
    for m in pat.finditer(s, start):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return m.end()
    raise ValueError("unbalanced")


def run(path):
    s = open(path, encoding="utf-8").read()
    deck = {}
    for n in range(1, 11):
        c = s.find('id="card-%d"' % n)
        r = s.find('<div class="bpa-summary-reviews bpa-rate">', c)
        deck[n] = s[r:block_end(s, r)]
    ids = re.findall(r'<details class="bpa-details-card"[^>]*id="(item-(\d+)-[^"]+)"', s)
    assert len(ids) == 10, (path, len(ids))
    done = 0
    for anchor, n in ids:
        d = s.find('id="%s"' % anchor)
        stop = s.find("</summary>", d)
        r = s.find('<div class="bpa-summary-reviews">', d)
        if r == -1 or r > stop:
            continue
        e = block_end(s, r)
        new = deck[int(n)]
        s = s[:r] + new + s[e:]
        done += 1
    open(path, "w", encoding="utf-8").write(s)
    print(path, done)


for f in sys.argv[1:] or FILES:
    run(f)
