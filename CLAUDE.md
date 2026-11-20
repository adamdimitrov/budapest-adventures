# Budapest Adventures

1. Read `kit/RULES.md` first: the shared rules for every site (nothing goes live
   without the owner's OK, QC, copy, affiliate links, photos, layout).
2. Then this site's own notes:
   - `GEMINI.md` (hard rules, partners such as Legenda / Silverline) and `PROJECT.md` (architecture, menu, photos, filters)
   They add site-specific rules and win only where they are stricter.
3. Before every PR: `python3 scripts/stamp_updated.py` (sets the "Last updated" date on every page whose
   content changed), then `python3 kit/checks/check_all.py` must exit 0 (CI runs the same, and fails on a
   changed page that kept an old date).
4. Anthropic API key: for now (until the owner says otherwise) it is used ONLY by the site's AI search
   bars (`api/`). Do not call the API from scripts: no `listicle.py translate`, no `port_page_i18n.py`
   without `--cache-only`. Translations are written by hand in the session and fed in through the
   cache (`port_page_i18n.py --dump-todo` / `--cache-only`, the language JSON files).
5. Never edit `kit/` here: change github.com/adamdimitrov/site-kit and run
   `python3 kit/update.py`. Site settings live in `site.json`.
