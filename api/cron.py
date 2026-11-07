import os
import re
import time
import hmac
import hashlib
import base64
import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler


def clean_env(val):
    if not val or not isinstance(val, str):
        return None
    val = val.strip()
    if val.startswith("dummy_") or not val:
        return None
    return val


def tourcms_request(path: str, channel_id: str, marketplace_id: str, api_key: str, verb: str = "GET", xml_body: str = None) -> ET.Element:
    """Execute a signed TourCMS REST API request and return parsed XML Element."""
    outbound_time = int(time.time())
    http_date = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime(outbound_time))
    string_to_sign = f"{channel_id}/{marketplace_id}/{verb}/{outbound_time}{path}"

    dig = hmac.new(
        api_key.encode("utf-8"),
        string_to_sign.encode("utf-8"),
        hashlib.sha256
    ).digest()
    signature = urllib.parse.quote(base64.b64encode(dig).decode("utf-8"), safe="")

    headers = {
        "x-tourcms-date": http_date,
        "Date": http_date,
        "Authorization": f"TourCMS {channel_id}:{marketplace_id}:{signature}",
        "Content-type": 'text/xml;charset="utf-8"',
        "User-Agent": f"BudapestAdventures-Sync ({marketplace_id}_{channel_id})"
    }

    url = f"https://api.tourcms.com{path}"
    data_bytes = xml_body.encode("utf-8") if xml_body else None
    req = urllib.request.Request(url, data=data_bytes, headers=headers, method=verb)

    with urllib.request.urlopen(req, timeout=15) as response:
        raw_xml = response.read().decode("utf-8")
        return ET.fromstring(raw_xml)


def extract_click_ids(*candidates):
    """Extract fbclid, fbp, and gclid/wbraid/gbraid from TourCMS agent_ref, customer_agent_ref, or notes."""
    fbclid = None
    fbp = None
    gclid = None
    gclid_type = "gclid"

    for raw in candidates:
        if not raw or not isinstance(raw, str):
            continue
        s = raw.strip()

        for part in s.split("|"):
            part = part.strip()
            if part.startswith("fbclid:") and not fbclid:
                fbclid = part.split(":", 1)[1].strip()
            elif part.startswith("fbp:") and not fbp:
                fbp = part.split(":", 1)[1].strip()
            elif not gclid and any(part.startswith(f"{k}:") for k in ("gclid", "wbraid", "gbraid")):
                k, v = part.split(":", 1)
                gclid_type = k.strip().lower()
                gclid = v.strip()

        if not fbclid:
            m_fb = re.search(r"(?:--|^)fbclid-([a-zA-Z0-9_.-]+)", s)
            if m_fb:
                fbclid = m_fb.group(1).split("--")[0].strip()

        if not fbp:
            m_fbp = re.search(r"(?:--|^)fbp-(fb\.[0-9]+\.[0-9]+\.[a-zA-Z0-9_.-]+)", s)
            if m_fbp:
                fbp = m_fbp.group(1).split("--")[0].strip()

        if not gclid:
            m_g = re.search(r"(?:--|^)(gclid|wbraid|gbraid)-([a-zA-Z0-9_.-]+)", s)
            if m_g:
                gclid_type = m_g.group(1).lower()
                gclid = m_g.group(2).split("--")[0].strip()

    return fbclid, fbp, gclid, gclid_type


def get_google_access_token(client_id, client_secret, refresh_token):
    if not (client_id and client_secret and refresh_token):
        return None
    token_url = "https://oauth2.googleapis.com/token"
    payload = urllib.parse.urlencode({
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }).encode("utf-8")
    req = urllib.request.Request(token_url, data=payload, headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8")).get("access_token")
    except Exception as e:
        print(f"Error fetching Google Access Token: {e}")
        return None


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            parsed = urllib.parse.urlparse(self.path)
            qs = urllib.parse.parse_qs(parsed.query)
            action = qs.get("action", ["sync"])[0]

            if action == "availability":
                tour_id = qs.get("tour_id", ["2"])[0]
                date_str = qs.get("date", [None])[0]
                rates = qs.get("rates", ["r1=2"])[0]
                result = self.fetch_availability(tour_id, date_str, rates)
            else:
                dry_run = qs.get("dry_run", ["0"])[0] == "1"
                test_event_code = qs.get("test_event_code", [None])[0]
                result = self.process_cron(dry_run=dry_run, test_event_code=test_event_code)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(result, indent=2).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode("utf-8"))

    def fetch_availability(self, tour_id: str, date_str: str = None, rates: str = "r1=2"):
        channel_id = os.environ.get("TOURCMS_CHANNEL_ID", "16485")
        marketplace_id = os.environ.get("TOURCMS_MARKETPLACE_ID", "57509")
        api_key = os.environ.get("TOURCMS_API_KEY", "51405b89d978")

        if date_str:
            path = f"/c/tour/datesprices/checkavail.xml?id={tour_id}&date={date_str}&{rates}"
            root = tourcms_request(path, channel_id, marketplace_id, api_key)
            slots = []
            for comp in root.findall(".//component"):
                total_price = float(comp.findtext("total_price") or 0.0)
                net_price = float(comp.findtext("net_price") or 0.0)
                slots.append({
                    "date": comp.findtext("start_date"),
                    "start_time": comp.findtext("start_time"),
                    "end_time": comp.findtext("end_time"),
                    "spaces_remaining": int(comp.findtext("spaces_remaining") or 0),
                    "total_price": total_price,
                    "net_price": net_price,
                    "commission_margin": round(total_price - net_price, 2),
                    "currency": comp.findtext("sale_currency") or "EUR",
                    "component_key": comp.findtext("component_key"),
                    "date_id": comp.findtext("date_id")
                })
            return {"status": "ok", "tour_id": tour_id, "date": date_str, "available_slots": slots}
        else:
            path = f"/c/tour/datesprices/dep/show.xml?id={tour_id}"
            root = tourcms_request(path, channel_id, marketplace_id, api_key)
            departures = []
            for dep in root.findall(".//departure")[:30]:
                rate_price = float(dep.findtext("main_price/rate_price") or 0.0)
                net_price = float(dep.findtext("main_price/net_price") or 0.0)
                departures.append({
                    "departure_id": dep.findtext("departure_id"),
                    "date": dep.findtext("start_date"),
                    "start_time": dep.findtext("start_time"),
                    "end_time": dep.findtext("end_time"),
                    "spaces_remaining": int(dep.findtext("spaces_remaining") or 0),
                    "status": dep.findtext("status"),
                    "adult_price": rate_price,
                    "adult_net_price": net_price,
                    "adult_margin": round(rate_price - net_price, 2),
                    "book_url": dep.findtext("book_url")
                })
            return {"status": "ok", "tour_id": tour_id, "departures": departures}

    def process_cron(self, dry_run: bool = False, test_event_code: str = None):
        channel_id = os.environ.get("TOURCMS_CHANNEL_ID", "16485")
        marketplace_id = os.environ.get("TOURCMS_MARKETPLACE_ID", "57509")
        api_key = os.environ.get("TOURCMS_API_KEY", "51405b89d978")
        meta_token = clean_env(os.environ.get("META_ACCESS_TOKEN"))
        meta_pixel = clean_env(os.environ.get("META_PIXEL_ID")) or "1355732169631751"

        google_client_id = clean_env(os.environ.get("GOOGLE_CLIENT_ID")) or clean_env(os.environ.get("GOOGLE_ADS_CLIENT_ID"))
        google_client_secret = clean_env(os.environ.get("GOOGLE_CLIENT_SECRET")) or clean_env(os.environ.get("GOOGLE_ADS_CLIENT_SECRET"))
        google_refresh_token = clean_env(os.environ.get("GOOGLE_REFRESH_TOKEN")) or clean_env(os.environ.get("GOOGLE_ADS_REFRESH_TOKEN"))
        google_customer_id = (clean_env(os.environ.get("GOOGLE_CUSTOMER_ID")) or clean_env(os.environ.get("GOOGLE_ADS_CUSTOMER_ID")) or "4899321613").replace("-", "")
        google_conversion_action_id = clean_env(os.environ.get("GOOGLE_CONVERSION_ACTION_ID")) or clean_env(os.environ.get("GOOGLE_ADS_CONVERSION_ACTION_ID")) or "7715980036"

        bookings = self.fetch_tourcms_bookings(channel_id, marketplace_id, api_key)
        now_ts = int(time.time())
        cached_google_token = None

        synced = []
        skipped = []

        for booking in bookings:
            booking_id = booking["booking_id"]
            event_ts = booking["event_ts"] or now_ts

            # Meta CAPI rejects events older than 7 days (604,800s) unless running a test_event_code
            if not test_event_code and (now_ts - event_ts) > 580000:
                skipped.append({"booking_id": booking_id, "reason": "older_than_7_days", "made_date_time": booking["made_date_time"]})
                continue

            if booking["cancel_reason"] != "0":
                skipped.append({"booking_id": booking_id, "reason": "cancelled"})
                continue

            fbclid, fbp, gclid, gclid_type = extract_click_ids(
                booking.get("agent_ref"),
                booking.get("agent_ref_components"),
                booking.get("lead_customer_agent_ref"),
                booking.get("customer_special_request")
            )

            meta_res = None
            google_res = None

            if not dry_run and meta_token and meta_pixel:
                meta_res = self.send_to_meta(booking, fbclid, fbp, meta_token, meta_pixel, event_ts, test_event_code)

            if not dry_run and gclid and google_client_id and google_customer_id and google_conversion_action_id:
                if not cached_google_token:
                    cached_google_token = get_google_access_token(google_client_id, google_client_secret, google_refresh_token)
                if cached_google_token:
                    google_res = self.send_to_google(booking, gclid, gclid_type, cached_google_token, google_customer_id, google_conversion_action_id)

            synced.append({
                "booking_id": booking_id,
                "booking_name": booking["booking_name"],
                "made_date_time": booking["made_date_time"],
                "sales_revenue": booking["sales_revenue"],
                "net_balance": booking["balance"],
                "commission_value": booking["commission_value"],
                "currency": booking["currency"],
                "fbclid": fbclid,
                "gclid": gclid,
                "meta_result": meta_res,
                "google_result": google_res
            })

        return {
            "status": "success",
            "marketplace_id": marketplace_id,
            "channel_id": channel_id,
            "total_bookings_found": len(bookings),
            "synced_count": len(synced),
            "skipped_count": len(skipped),
            "synced": synced,
            "skipped": skipped
        }

    def fetch_tourcms_bookings(self, channel_id: str, marketplace_id: str, api_key: str):
        root = tourcms_request("/c/bookings/search.xml?per_page=50", channel_id, marketplace_id, api_key)
        bookings = []

        for b in root.findall("booking"):
            b_id = b.findtext("booking_id") or ""
            # Fetch full booking details via /c/booking/show.xml to get customer email, phone, country, and component net prices
            detail_root = tourcms_request(f"/c/booking/show.xml?booking_id={b_id}", channel_id, marketplace_id, api_key)
            db = detail_root.find("booking") or b

            sales_revenue = float(db.findtext("sales_revenue") or 0.0)
            balance = float(db.findtext("balance") or 0.0)
            commission = float(db.findtext("commission") or 0.0)

            # TourCMS Net Rate contract (booking_has_net_price=1): profit is sales_revenue - balance (25% margin on Legenda)
            if commission > 0:
                commission_value = round(commission, 2)
            elif sales_revenue > 0 and balance > 0 and sales_revenue > balance:
                commission_value = round(sales_revenue - balance, 2)
            else:
                commission_value = round(sales_revenue * 0.25, 2)

            made_utc = db.findtext("made_date_time_at_utc_seconds")
            event_ts = int(made_utc) if (made_utc and made_utc.isdigit()) else int(time.time())

            bookings.append({
                "booking_id": b_id,
                "booking_name": db.findtext("booking_name") or "",
                "made_date_time": db.findtext("made_date_time") or "",
                "event_ts": event_ts,
                "status": db.findtext("status") or "",
                "status_text": db.findtext("status_text") or "",
                "cancel_reason": db.findtext("cancel_reason") or "0",
                "sales_revenue": sales_revenue,
                "balance": balance,
                "commission_value": commission_value,
                "currency": db.findtext("sale_currency") or "EUR",
                "agent_ref": db.findtext("agent_ref") or "",
                "agent_ref_components": db.findtext("agent_ref_components") or "",
                "tracking_miscid": db.findtext("tracking_miscid") or "0",
                "lead_customer_name": db.findtext("lead_customer_name") or "",
                "lead_customer_firstname": db.findtext("lead_customer_firstname") or "",
                "lead_customer_surname": db.findtext("lead_customer_surname") or "",
                "lead_customer_email": db.findtext("lead_customer_email") or "",
                "lead_customer_tel_mobile": db.findtext("lead_customer_tel_mobile") or "",
                "lead_customer_country": db.findtext("lead_customer_country") or db.findtext("nationality") or "",
                "lead_customer_agent_ref": db.findtext("lead_customer_agent_ref") or "",
                "customer_special_request": db.findtext("customer_special_request") or "",
                "product_id": db.findtext("components/component/product_id") or ""
            })

        return bookings

    def send_to_meta(self, booking: dict, fbclid: str, fbp: str, token: str, pixel: str, event_ts: int, test_event_code: str = None):
        booking_id = str(booking["booking_id"])
        event_id = f"tourcms_{booking_id}"
        use_ts = int(time.time()) if test_event_code else event_ts

        user_data = {
            "external_id": [hashlib.sha256(booking_id.encode("utf-8")).hexdigest()]
        }
        if fbclid:
            user_data["fbc"] = f"fb.1.{use_ts}.{fbclid}"
        if fbp:
            user_data["fbp"] = fbp

        email = (booking.get("lead_customer_email") or "").strip().lower()
        if email:
            user_data["em"] = [hashlib.sha256(email.encode("utf-8")).hexdigest()]

        phone = re.sub(r"[^0-9]", "", booking.get("lead_customer_tel_mobile") or "")
        if phone:
            user_data["ph"] = [hashlib.sha256(phone.encode("utf-8")).hexdigest()]

        fn = (booking.get("lead_customer_firstname") or "").strip().lower()
        if fn:
            user_data["fn"] = [hashlib.sha256(fn.encode("utf-8")).hexdigest()]

        ln = (booking.get("lead_customer_surname") or "").strip().lower()
        if ln:
            user_data["ln"] = [hashlib.sha256(ln.encode("utf-8")).hexdigest()]

        country = (booking.get("lead_customer_country") or "").strip().lower()
        if country:
            user_data["country"] = [hashlib.sha256(country.encode("utf-8")).hexdigest()]

        custom_data = {
            "value": booking["commission_value"],
            "currency": booking["currency"],
            "content_name": booking["booking_name"],
            "content_type": "product",
            "order_id": booking_id
        }
        if booking.get("product_id"):
            custom_data["content_ids"] = [f"legenda_{booking['product_id']}"]

        payload = {
            "data": [
                {
                    "event_name": "Purchase",
                    "event_time": use_ts,
                    "action_source": "website",
                    "event_id": event_id,
                    "user_data": user_data,
                    "custom_data": custom_data
                }
            ]
        }
        if test_event_code:
            payload["test_event_code"] = test_event_code

        url = f"https://graph.facebook.com/v20.0/{pixel}/events?access_token={token}"
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data_bytes, headers={"Content-Type": "application/json"})

        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            return {"error": str(e)}

    def send_to_google(self, booking: dict, gclid: str, gclid_type: str, access_token: str, customer_id: str, conversion_action_id: str):
        conversion_time_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        dm_url = "https://datamanager.googleapis.com/v1/events:ingest"
        dm_headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        dm_payload = {
            "destinations": [
                {
                    "operatingAccount": {
                        "accountType": "GOOGLE_ADS",
                        "accountId": str(customer_id)
                    },
                    "productDestinationId": str(conversion_action_id)
                }
            ],
            "events": [
                {
                    "eventSource": "WEB",
                    "eventTimestamp": conversion_time_iso,
                    "transactionId": f"TC-{booking['booking_id']}",
                    "conversionValue": booking["commission_value"],
                    "currency": booking["currency"],
                    "adIdentifiers": {
                        gclid_type: gclid
                    }
                }
            ]
        }
        data_bytes = json.dumps(dm_payload).encode("utf-8")
        req = urllib.request.Request(dm_url, data=data_bytes, headers=dm_headers)
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            return {"error": str(e)}
