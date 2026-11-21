"""Move the nice-to-know guide blocks that sit between the comparison list and card #1
to the end of the article (right after the last card).

Rule: the hero comparison list is followed directly by the detailed breakdown (cards).
Useful but non-critical info ("Which X should you book", price tables, best time, free
alternatives, related links) goes after the cards.

Usage: python3 scripts/move_precard_guides.py [--check] [files...]
Without files it scans every listicle page.
"""
import glob
import re
import sys

GUIDE_RE = re.compile(r'(?:<!--[^>]*?-->\s*)?<div class="w-richtext bpa-wt-guide"[^>]*>')
CARD = '<details class="bpa-details-card'


def balanced_end(s, start, tag):
    """Index just past the element opened at `start` (a <tag ...>)."""
    pat = re.compile(r'<(/?)%s\b[^>]*>' % tag)
    depth = 0
    for m in pat.finditer(s, start):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return m.end()
    raise ValueError('unbalanced <%s> at %d' % (tag, start))


def process(s):
    m = re.search(r'<div class="content-right_blog"[^>]*>', s)
    if not m:
        return s, 0
    start = m.end()
    ends = [x for x in (s.find('class="bpa-breakdown-top-bar"', start), s.find(CARD, start)) if x > 0]
    if not ends:
        return s, 0
    stop = min(ends)
    blocks = []
    pos = start
    while True:
        g = GUIDE_RE.search(s, pos, stop)
        if not g:
            break
        div_at = s.index('<div', g.start())
        end = balanced_end(s, div_at, 'div')
        blocks.append((g.start(), end))
        pos = end
    if not blocks:
        return s, 0
    moved = ''.join(s[a:b] + '\n' for a, b in blocks)
    # cut blocks out (back to front so offsets stay valid)
    for a, b in reversed(blocks):
        tail = s[b:]
        s = s[:a] + (tail[1:] if tail.startswith('\n') else tail)
    last_card = s.rfind(CARD)
    insert_at = balanced_end(s, last_card, 'details')
    s = s[:insert_at] + '\n' + moved.rstrip('\n') + s[insert_at:]
    return s, len(blocks)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    check = '--check' in sys.argv
    files = args or [f for f in glob.glob('**/*.html', recursive=True)
                     if not f.startswith(('.claude', 'kit', 'drafts', 'tests', 'embed'))]
    bad = 0
    for f in sorted(files):
        s = open(f, encoding='utf-8').read()
        if CARD not in s:
            continue
        new, n = process(s)
        if n:
            bad += 1
            print(('WOULD MOVE' if check else 'moved'), n, 'block(s):', f)
            if not check:
                open(f, 'w', encoding='utf-8').write(new)
    if check and bad:
        sys.exit(1)


if __name__ == '__main__':
    main()
