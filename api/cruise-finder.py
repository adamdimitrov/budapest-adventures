"""AI cruise finder for the river cruises comparison page.

GET /api/cruise-finder?page=best-budapest-river-cruises&q=romantic+under+30

Reads the cards and the author's reviews from the page's own HTML (bundled with the function)
plus guest-review themes from api/_knowledge/<page>.json. Answers questions in 2-3 sentences
("kind": "question") or matches a wish ("preference"), and returns card ids plus a one-line reason. Prices and booking links always come from the page itself.
Identical questions are cached at the Vercel CDN for a day, so repeats are free.
Needs ANTHROPIC_API_KEY in the Vercel project's environment variables.
"""
import html
import json
import os
import re
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

import anthropic

MODEL = os.environ.get("CRUISE_FINDER_MODEL", "claude-haiku-5-5")
MAX_Q = 300
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Only these pages can be queried; value = HTML file bundled via vercel.json includeFiles.
PAGES = {
    "best-budapest-river-cruises": "best-budapest-river-cruises.html",
}

_cards_cache = {}
_client = None

SCHEMA = {
    "type": "object",
    "properties": {
        "kind": {"type": "string", "enum": ["question", "preference"]},
        "answer": {"type": "string"},
        "lead": {"type": "string"},
        "picks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"id": {"type": "string"}, "why": {"type": "string"}},
                "required": ["id", "why"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["kind", "answer", "lead", "picks"],
    "additionalProperties": False,
}
KNOWLEDGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_knowledge")


def _text(fragment):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


def load_cards(page):
    if page in _cards_cache:
        return _cards_cache[page]
    with open(os.path.join(ROOT, PAGES[page]), encoding="utf-8") as f:
        src = f.read()
    try:
        with open(os.path.join(KNOWLEDGE_DIR, page + ".json"), encoding="utf-8") as f:
            know = json.load(f)
    except (OSError, ValueError):
        know = {"general": [], "cruises": {}}
    # the author's own detailed review of each cruise (Detailed Breakdown section)
    reviews = {}
    for m in re.finditer(r'<details class="bpa-details-card"[^>]*id="([^"]+)"', src):
        start = src.index(">", m.end()) + 1
        body = src[start: start + 60000]
        nxt = body.find('<details class="bpa-details-card"')
        reviews[m.group(1)] = _text(body[: nxt if nxt > 0 else 60000])[:1800]
    cards = []
    for chunk in re.split(r'<div class="bpa-card" ', src)[1:]:
        m = re.search(r'id="(card-\d+)"', chunk)
        if not m:
            continue
        anchor = re.search(r'class="bpa-sublink" href="#([^"]+)"', chunk)
        anchor = anchor.group(1) if anchor else ""
        # Stop at the card's "Read Review" link so the long review sections don't leak in.
        end = chunk.find("Read Review")
        part = chunk[: end if end > 0 else 20000]
        facts = []
        for det in re.findall(r"<details[^>]*>(.*?)</details>", part, re.S):
            t = _text(det).replace("▾", "")
            if "Personally Tested" in t or "booking sites" in t:
                continue
            facts.append(t[:280])
        cards.append({"id": m.group(1), "card": _text(part)[:1400], "details": facts[:6],
                      "my_review": reviews.get(anchor, ""),
                      "guests_say": know.get("cruises", {}).get(anchor, {}).get("guests_say", [])})
    _cards_cache[page] = (cards, know.get("general", []))
    return _cards_cache[page]


def build_prompt(q, cards, ctx=None, general=None):
    static = (
        "You are the cruise finder on a Budapest river cruise comparison page. "
        "The author rode most of the cruises below and wrote each card and review. A visitor typed something into the search box.\n\n"
        "First decide the kind:\n"
        "- question: they ask something (is it cold, can kids come, is the guide audible, is it worth it, what is included, which is better).\n"
        "- preference: they describe the cruise or experience they want.\n\n"
        "For a question, write answer: 2 or 3 short sentences that answer it directly from the data below (card facts, the author's "
        "review in my_review, what guests say in guests_say, and the general tips). When you use guests_say, say it plainly, for "
        "example 'Guests say...' or '14 of 64 recent guests mention...'. If the data does not cover it, say you don't know rather "
        "than guess. Then still pick the 1 to 3 cruises that best fit the question.\n"
        "For a preference, answer is an empty string; pick the 1 to 3 cruises that fit best, best first.\n\n"
        "Rules:\n"
        "- Use only the data below. Never invent prices, times, menus, features or guest opinions.\n"
        "- Never name or quote review websites or Facebook; say 'guests' or 'travellers'. No em dashes.\n"
        "- In answer, lead and why, call cruises by their name (for example 'the Duna-Weser prosecco cruise'), never by card id. "
        "You speak for the author in the first person: write 'I found' or 'when I tested it', never 'the author' or 'the data'.\n"
        "- If a card says it is not bookable now, pick it only if nothing else fits, and say so.\n"
        "- If nothing fits well, return the closest 1 or 2 and say plainly what does not match.\n"
        "- why: one sentence of at most 22 words, to the visitor, citing the concrete facts that match "
        "(price, drinks, length, pier, audio guide).\n"
        "- lead: one short sentence summarising the recommendation.\n"
        "- Answer in the visitor's language.\n"
        "- If the request has nothing to do with Budapest cruises, kind is preference, answer is empty, and return the #1 card with a short lead.\n"
        "- If the visitor mentions sunset, night, the lights, dark or a time of day, use the lighting info for their date "
        "and name the exact sailing time to book in the why (for example 'book the 16:30 sailing for sunset into lights'). "
        "A cruise whose sailings all end before dark does not fit a night or lights request.\n\n"
        f"General tips:\n{json.dumps(general or [], ensure_ascii=False)}\n\n"
        f"Cards:\n{json.dumps(cards, ensure_ascii=False)}"
    )
    dynamic = ((f"Visitor's context: {json.dumps(ctx, ensure_ascii=False)}\n\n" if ctx else "")
               + f"Visitor typed: {json.dumps(q, ensure_ascii=False)}")
    return static, dynamic


def visitor_context(params, cards):
    """Date, lighting and active filters sent by the page, trimmed to safe sizes."""
    one = lambda k, n: re.sub(r"\s+", " ", (params.get(k) or [""])[0]).strip()[:n]
    ctx = {}
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", one("date", 10)):
        ctx["cruise_date"] = one("date", 10)
    if one("light", 160):
        ctx["light_on_that_date"] = one("light", 160)
    if one("filters", 200):
        ctx["active_filters"] = one("filters", 200)
    try:
        slots = json.loads((params.get("slots") or ["{}"])[0])
        valid = {c["id"] for c in cards}
        slots = {str(k): re.sub(r"\s+", " ", str(v))[:180] for k, v in slots.items() if str(k) in valid}
        if slots:
            ctx["sailing_lights_per_card"] = slots
    except (ValueError, AttributeError):
        pass
    return ctx


def ask_claude(q, cards, ctx=None, general=None):
    global _client
    if _client is None:
        _client = anthropic.Anthropic(max_retries=1, timeout=25.0)
    static, dynamic = build_prompt(q, cards, ctx, general)
    response = _client.messages.create(
        model=MODEL,
        max_tokens=2000,
        output_config={"effort": "low", "format": {"type": "json_schema", "schema": SCHEMA}},
        messages=[{"role": "user", "content": [
            {"type": "text", "text": static, "cache_control": {"type": "ephemeral"}},
            {"type": "text", "text": dynamic},
        ]}],
    )
    if response.stop_reason == "refusal":
        raise ValueError("refused")
    text = next(b.text for b in response.content if b.type == "text")
    data = json.loads(text)
    valid = {c["id"] for c in cards}
    picks = []
    for p in data.get("picks", []):
        pid = str(p.get("id", ""))
        if pid in valid and pid not in {x["id"] for x in picks}:
            picks.append({"id": pid, "why": str(p.get("why", ""))[:220].replace("\u2014", ",")})
    if not picks:
        raise ValueError("no valid picks")
    kind = "question" if data.get("kind") == "question" else "preference"
    answer = str(data.get("answer", ""))[:600].replace("\u2014", ",") if kind == "question" else ""
    print(json.dumps({"finder_log": {"q": q, "kind": kind, "picks": [p["id"] for p in picks]}}, ensure_ascii=False))
    return {"kind": kind, "answer": answer, "lead": str(data.get("lead", ""))[:220].replace("\u2014", ","), "picks": picks[:3]}


class handler(BaseHTTPRequestHandler):
    def _send(self, status, payload, cache=False):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "public, max-age=0, s-maxage=86400" if cache else "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)
        page = (params.get("page") or [""])[0]
        q = re.sub(r"\s+", " ", (params.get("q") or [""])[0]).strip().lower()[:MAX_Q]
        if page not in PAGES:
            return self._send(400, {"error": "unknown_page"})
        if len(q) < 2:
            return self._send(400, {"error": "empty_question"})
        try:
            cards, general = load_cards(page)
            # only the cards the visitor's filters leave on screen (all of them if none sent)
            ids = [i for i in (params.get("ids") or [""])[0].split(",") if i]
            pool = [c for c in cards if c["id"] in ids] or cards
            return self._send(200, ask_claude(q, pool, visitor_context(params, pool), general), cache=True)
        except anthropic.RateLimitError:
            return self._send(429, {"error": "busy"})
        except anthropic.APIConnectionError:
            return self._send(503, {"error": "unavailable"})
        except anthropic.APIStatusError as e:
            print(f"cruise-finder API error {e.status_code}: {e.message}")
            return self._send(502, {"error": "unavailable"})
        except Exception as e:  # bad JSON, refusal, no valid picks
            print(f"cruise-finder failed: {e!r}")
            return self._send(502, {"error": "no_answer"})
