"""Link css/shared/bpa-prose-editorial.*.css on every article page that has a content-right_blog body.

Brings the prose after the cards (guides, FAQ, editorial sections) onto the current design:
intro typography and brand-gold links instead of the old Webflow blue.
Re-run after adding pages; it replaces an older hash of the same file.
"""
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
css = sorted(glob.glob('css/shared/bpa-prose-editorial.*.css'))[-1]
TAG = '<link id="bpa-prose-editorial" rel="stylesheet" href="/%s"/>' % css
OLD = re.compile(r'<link id="bpa-prose-editorial"[^>]*>')

n = 0
for f in glob.glob('**/*.html', recursive=True):
    if f.startswith(('.claude', 'kit', 'drafts', 'tests', 'embed')):
        continue
    s = open(f, encoding='utf-8').read()
    if 'class="content-right_blog' not in s or '</head>' not in s:
        continue
    if OLD.search(s):
        new = OLD.sub(TAG, s, count=1)
    else:
        new = s.replace('</head>', TAG + '</head>', 1)
    if new != s:
        open(f, 'w', encoding='utf-8').write(new)
        n += 1
print('linked on', n, 'pages')
