#!/usr/bin/env python3
"""Resubmit every sitemap of this site in Google Search Console.

Runs in CI (.github/workflows/gsc-sitemaps.yml) with a service account key in the
GSC_SERVICE_ACCOUNT_JSON env var. The service account's e-mail must be added as an
Owner of the property in Search Console (Settings > Users and permissions).

What it does:
  1. finds the Search Console property for the domain in site.json
     (domain property "sc-domain:..." or URL-prefix property, whichever the account sees);
  2. collects sitemaps: the ones already registered in GSC + the ones in robots.txt;
  3. PUTs each one again (= "Submit" in the UI) and prints its status.

Usage:  python3 scripts/gsc_submit_sitemaps.py [--dry-run]
"""
import json
import os
import re
import sys
from urllib.parse import quote, urlparse

from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://www.googleapis.com/webmasters/v3"
SCOPES = ["https://www.googleapis.com/auth/webmasters"]


def main():
    dry = "--dry-run" in sys.argv
    raw = os.environ.get("GSC_SERVICE_ACCOUNT_JSON", "").strip()
    if not raw:
        sys.exit("GSC_SERVICE_ACCOUNT_JSON is not set (add it as a GitHub repo secret).")
    creds = service_account.Credentials.from_service_account_info(json.loads(raw), scopes=SCOPES)
    s = AuthorizedSession(creds)

    domain = json.load(open(os.path.join(ROOT, "site.json")))["domain"].rstrip("/")
    host = urlparse(domain).hostname
    bare = host[4:] if host.startswith("www.") else host

    r = s.get(f"{API}/sites")
    r.raise_for_status()
    sites = [e["siteUrl"] for e in r.json().get("siteEntry", [])
             if e.get("permissionLevel") in ("siteOwner", "siteFullUser")]
    candidates = [f"sc-domain:{bare}", domain + "/", f"https://{bare}/"]
    prop = next((c for c in candidates if c in sites), None)
    if not prop:
        sys.exit(f"No Search Console property for {host} with owner/full access. "
                 f"Visible: {sites or 'none'}. Add {creds.service_account_email} as Owner in GSC.")
    print(f"Property: {prop}")

    feeds = set()
    r = s.get(f"{API}/sites/{quote(prop, safe='')}/sitemaps")
    r.raise_for_status()
    feeds.update(sm["path"] for sm in r.json().get("sitemap", []))
    robots = open(os.path.join(ROOT, "robots.txt")).read()
    feeds.update(re.findall(r"(?im)^\s*sitemap:\s*(\S+)", robots))
    if not feeds:
        feeds.add(domain + "/sitemap.xml")

    failed = 0
    for feed in sorted(feeds):
        url = f"{API}/sites/{quote(prop, safe='')}/sitemaps/{quote(feed, safe='')}"
        if dry:
            print(f"[dry-run] would submit {feed}")
            continue
        r = s.put(url)
        if r.status_code >= 300:
            failed += 1
            print(f"FAIL {feed}: {r.status_code} {r.text[:300]}")
            continue
        info = s.get(url).json()
        print(f"OK   {feed}  submitted={info.get('lastSubmitted')} "
              f"errors={info.get('errors')} warnings={info.get('warnings')}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
