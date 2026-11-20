"""The old (pre-listicle) best-day-trips-from-budapest.html, which several older builders use as their
page shell (head CSS, nav, footer, deck CSS, runtime JS): build_article, build_november, build_december,
build_itinerary, build_budapest_vienna, build_budapest_amsterdam.

The live page moved to the shared listicle design (cards from data/listicles/), so it no longer carries
the inline card CSS/JS those builders expect. They read this frozen copy from git history instead.
"""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMMIT = "a58feb609c4afb5e334f8ddb1ff7001d15438594"  # main just before the listicle move of the day trips page


def read():
    return subprocess.run(["git", "show", f"{COMMIT}:best-day-trips-from-budapest.html"], cwd=ROOT,
                          capture_output=True, text=True, check=True).stdout
