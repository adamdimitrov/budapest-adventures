#!/usr/bin/env python3
"""PageSpeed basics every page inherits from its template (see kit/scripts/pagespeed.py):
no webfont.js, no `body:has()` for elements listed in site.json pagespeed.static_has, no inline
copy of a CSS block that is shared by many pages. Fix: python3 scripts/pagespeed.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import pagespeed  # noqa: E402

if __name__ == "__main__":
    sys.exit(pagespeed.run(["fonts", "has", "css"], check=True))
