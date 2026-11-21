"""Affiliate link leak audit over deployed HTML (git-tracked, minus .vercelignore patterns).

Usage: python3 scripts/audit_affiliate_links.py /tmp/audit.json   (summary to stdout, details to the JSON)
"""
import re, subprocess, fnmatch, json, html, sys
from collections import defaultdict, Counter
from urllib.parse import urlparse, parse_qs

files = subprocess.run(['git', 'ls-files', '*.html'], capture_output=True, text=True).stdout.split()
ign = [l.strip() for l in open('.vercelignore') if l.strip() and not l.startswith('#')]
def ignored(f):
    for p in ign:
        if p.endswith('/') and f.startswith(p): return True
        if p.startswith('/') and fnmatch.fnmatch(f, p[1:]) and '/' not in f: return True
        if fnmatch.fnmatch(f, p) or fnmatch.fnmatch(f.split('/')[-1], p): return True
    return False
files = [f for f in files if not ignored(f)]

A = re.compile(r'<a\b([^>]*)>', re.I)
HREF = re.compile(r'href="([^"]+)"')
CLS = re.compile(r'class="([^"]*)"')
issues = defaultdict(lambda: defaultdict(list))   # rule -> url -> [files]
domains = Counter()
MAIN_BTN = {'bpa-btn', 'ltt-buy-cta-btn', 'hybrid-cta-btn', 'bpa-book-button', 'bpa-big-btn', 'btn-sticky-cta', 'ltt-mobile-cta'}

def add(rule, url, f): issues[rule][url].append(f)

for f in files:
    t = open(f, errors='ignore').read()
    for m in A.finditer(t):
        attrs = m.group(1)
        h = HREF.search(attrs)
        if not h: continue
        url = html.unescape(h.group(1))
        cls = set((CLS.search(attrs).group(1) if CLS.search(attrs) else '').split())
        u = urlparse(url)
        host = (u.netloc or '').lower()
        q = parse_qs(u.query)
        if host: domains[host] += 1
        if cls & MAIN_BTN:
            if not host or 'budapestadventures.com' in host:
                add('main button not affiliate', url, f)
        if host.endswith('getyourguide.com') and host != 'widget.getyourguide.com':
            if q.get('partner_id') != ['YS414AJ']: add('GYG missing/wrong partner_id', url, f)
            elif q.get('mkt_cmp') != ['true']: add('GYG missing mkt_cmp=true', url, f)
            if '/s/' in u.path or u.path.rstrip('/') in ('', '/s'): add('GYG search/home link (not a product)', url, f)
        elif host == 'budapestrivercruise.eu':
            if u.query != 'code=bpadventures': add('Silverline query not exactly code=bpadventures', url, f)
        elif host.endswith('legenda.hu'):
            if q.get('partner') != ['38585']: add('Legenda missing partner=38585', url, f)
        elif host.endswith('budapestxplore.com'):
            if q.get('affi') != ['6876']: add('BudapestXplore missing affi=6876', url, f)
        elif host.endswith('viator.com'):
            if q.get('pid') != ['P00072830'] or q.get('mcid') != ['42383']: add('Viator missing pid/mcid', url, f)
        elif host.endswith('guruwalk.com'):
            if 'ref' not in q: add('Guruwalk missing ref', url, f)
        elif host in ('www.booking.com', 'booking.com', 'www.hostelworld.com', 'www.tripadvisor.com', 'www.tiqets.com', 'tiqets.com', 'www.klook.com'):
            if not any(k in q for k in ('aid', 'partner', 'affiliate', 'marker')): add(f'Raw OTA link, no affiliate ({host})', url, f)
        elif host in ('jegymester.hu', 'dunacruises.com'):
            add(f'Bookable operator, no affiliate param ({host})', url, f)
        elif url.startswith('http://'):
            add('Insecure http link', url, f)

out = {r: {u: sorted(set(fs)) for u, fs in d.items()} for r, d in issues.items()}
json.dump(out, open(sys.argv[1], 'w'), indent=1)
print(len(files), 'deployed html files')
for r, d in sorted(out.items(), key=lambda x: -sum(len(v) for v in x[1].values())):
    n = sum(len(v) for v in d.values())
    print(f'\n## {r}: {len(d)} distinct urls on {len(set(sum(d.values(), [])))} files ({n} url-file pairs)')
    for u, fs in sorted(d.items(), key=lambda x: -len(x[1]))[:6]:
        print(f'  {len(fs):4}x {u[:150]}   e.g. {fs[0]}')
