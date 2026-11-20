#!/usr/bin/env python3
"""Every desktop mega menu fits on the screen, on every language's menu.

    python3 kit/checks/check_menu_fit.py              # the master page of each language
    python3 kit/checks/check_menu_fit.py page.html    # given pages
    python3 kit/checks/check_menu_fit.py --strict     # fail (not skip) without a browser

The menu is the same on every page of a language (sync_layout copies it from that language's
master page, scripts/layout_config.json "masters"), so checking the masters checks the whole
site. On each page, at several desktop widths, every .ltt-nav-dropdown is opened and its
.ltt-mega-menu must lie inside the screen (1 px margin of error), must not cut its columns off,
must keep its columns on one row while the screen has room, and the page must not get wider
than the screen. A menu that grows (more pages, a longer label, a new column) fails here before
it reaches an article, whatever article it is.

The fix is in the menu code, not in the menu data: nav.js (fitMenus) moves a menu that would
stick out back inside the screen, and only a menu wider than the screen gets the full screen
width with wrapped columns. A failure here means a page runs an older copy of nav.js / nav.css
(bring the master pages' #ltt-nav-script and #ltt-nav-styles up to templates/site/chrome/, then
run sync_layout.py) or page CSS that overrides it.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sitecfg import ROOT  # noqa: E402
import check_listicle_layout as L  # noqa: E402

WIDTHS = [992, 1100, 1280, 1440, 1920]

NODE = r"""
const { chromium } = require('playwright');
const [base, pagesJson, widthsJson] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch(); const out = {};
  for (const page of JSON.parse(pagesJson)) {
    out[page] = [];
    for (const w of JSON.parse(widthsJson)) {
      const ctx = await b.newContext({ viewport: { width: w, height: 900 } }); const p = await ctx.newPage();
      await p.route('**/*', r => r.request().url().startsWith(base) ? r.continue() : r.abort());
      try { await p.goto(base + '/' + page, { waitUntil: 'load', timeout: 60000 }); }
      catch (e) { out[page].push(w + 'px: page did not load (' + e.message.split('\n')[0] + ')'); await ctx.close(); continue; }
      await p.waitForTimeout(300);
      const n = await p.evaluate(() => document.querySelectorAll('.ltt-nav-dropdown').length);
      for (let i = 0; i < n; i++) {
        const d = p.locator('.ltt-nav-dropdown').nth(i);
        if (!(await d.isVisible())) continue;
        await d.hover();
        await p.waitForTimeout(250);
        const r = await p.evaluate(i => {
          const d = document.querySelectorAll('.ltt-nav-dropdown')[i], m = d.querySelector('.ltt-mega-menu');
          if (!m) return null;
          const x = m.getBoundingClientRect(), vw = document.documentElement.clientWidth;
          const btn = d.querySelector('.ltt-dropdown-btn');
          const tops = new Set(Array.from(m.querySelectorAll(':scope > .ltt-mega-col')).map(c => Math.round(c.getBoundingClientRect().top)));
          return { left: Math.round(x.left), right: Math.round(x.right), vw: vw, rows: tops.size, w: Math.round(x.width), cut: m.scrollWidth > m.clientWidth + 1,
                   label: (btn ? btn.innerText : d.innerText).replace(/\s+/g, ' ').trim().slice(0, 40) };
        }, i);
        if (r && (r.left < -1 || r.right > r.vw + 1))
          out[page].push(w + 'px: menu "' + r.label + '" runs ' + r.left + '..' + r.right + 'px on a ' + r.vw + 'px screen');
        if (r && r.cut)
          out[page].push(w + 'px: menu "' + r.label + '" cuts its columns off (content wider than the menu box)');
        if (r && r.rows > 1 && r.w < r.vw - 40)
          out[page].push(w + 'px: menu "' + r.label + '" wraps its columns into ' + r.rows + ' rows although the screen has room');
      }
      await p.mouse.move(1, 899);
      await p.waitForTimeout(250);
      const sw = await p.evaluate(() => [document.documentElement.scrollWidth, document.documentElement.clientWidth]);
      if (sw[0] > sw[1] + 1) out[page].push(w + 'px: page is ' + sw[0] + 'px wide on a ' + sw[1] + 'px screen (sideways overflow)');
      await ctx.close();
    }
  }
  await b.close(); console.log(JSON.stringify(out));
})().catch(e => { console.error(e.message); process.exit(3); });
"""


def masters():
    path = os.path.join(ROOT, "scripts", "layout_config.json")
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as fh:
        m = json.load(fh).get("masters", {})
    return [p for p in dict.fromkeys(m.values()) if os.path.exists(os.path.join(ROOT, p))]


def measure(pages, widths=WIDTHS):
    """{page: [problem, ...]}; None when no browser is available."""
    old_node, old_vp = L.NODE, L.VIEWPORTS
    try:
        L.NODE, L.VIEWPORTS = NODE, widths   # the layout check's server and runner, this script
        return L.measure(pages)
    finally:
        L.NODE, L.VIEWPORTS = old_node, old_vp


def main(argv):
    strict = "--strict" in argv
    pages = [a for a in argv if not a.startswith("--")] or masters()
    if not pages:
        print("menu fit: no master pages (scripts/layout_config.json) to check")
        return 0
    res = measure(pages)
    if res is None:
        print("menu fit: skipped, no browser (Node + Playwright); run it where one is installed")
        return 1 if strict else 0
    bad = 0
    for page in pages:
        probs = res.get(page, [])
        if probs:
            bad += 1
            print(f"{page}: {len(probs)} menu problem(s)")
            print("\n".join("  " + x for x in probs))
    print(f"menu fit: {len(pages)} page(s) at {', '.join(map(str, WIDTHS))} px, {bad} with problems")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
