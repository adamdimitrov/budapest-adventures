import hmac
import hashlib
import base64
import time
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

MARKETPLACE_ID = "57509"
API_KEY = "51405b89d978"
CHANNEL_ID = "16485"  # Legenda City Cruises


def tourcms_request(path: str, channel_id: str = CHANNEL_ID, verb: str = "GET", xml_body: str = None) -> ET.Element:
    """Execute a signed TourCMS REST API request and return parsed XML root."""
    outbound_time = int(time.time())
    http_date = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime(outbound_time))
    string_to_sign = f"{channel_id}/{MARKETPLACE_ID}/{verb}/{outbound_time}{path}"

    dig = hmac.new(
        API_KEY.encode("utf-8"),
        string_to_sign.encode("utf-8"),
        hashlib.sha256
    ).digest()
    signature = urllib.parse.quote(base64.b64encode(dig).decode("utf-8"), safe="")

    headers = {
        "x-tourcms-date": http_date,
        "Date": http_date,
        "Authorization": f"TourCMS {channel_id}:{MARKETPLACE_ID}:{signature}",
        "Content-type": 'text/xml;charset="utf-8"',
        "User-Agent": f"BudapestAdventures-Sync ({MARKETPLACE_ID}_{channel_id})"
    }

    url = f"https://api.tourcms.com{path}"
    data_bytes = xml_body.encode("utf-8") if xml_body else None
    req = urllib.request.Request(url, data=data_bytes, headers=headers, method=verb)

    with urllib.request.urlopen(req, timeout=15) as response:
        raw_xml = response.read().decode("utf-8")
        return ET.fromstring(raw_xml)


if __name__ == "__main__":
    print("1. Checking API Rate Limit Status...")
    rate_root = tourcms_request("/api/rate_limit_status.xml", channel_id="0")
    print(f"   Status: {rate_root.findtext('error')} | Remaining GET: {rate_root.findtext('remaining_hits')}/{rate_root.findtext('hourly_limit')}")

    print("\n2. Listing Tours on Legenda City Cruises (Channel 16485)...")
    tours_root = tourcms_request("/c/tours/list.xml", channel_id=CHANNEL_ID)
    for tour in tours_root.findall("tour"):
        t_id = tour.findtext("tour_id")
        t_name = tour.findtext("tour_name")
        t_code = tour.findtext("tour_code")
        has_sale = tour.findtext("has_sale")
        print(f"   - Tour #{t_id} [{t_code}]: {t_name} (Active: {has_sale})")

    print("\n3. Searching Bookings on Legenda City Cruises (Channel 16485)...")
    bookings_root = tourcms_request("/c/bookings/search.xml", channel_id=CHANNEL_ID)
    for b in bookings_root.findall("booking"):
        b_id = b.findtext("booking_id")
        b_name = b.findtext("booking_name")
        status_text = b.findtext("status_text")
        customer = b.findtext("lead_customer_name")
        revenue = float(b.findtext("sales_revenue") or 0.0)
        balance = float(b.findtext("balance") or 0.0)
        commission = float(b.findtext("commission") or 0.0)
        net_profit = commission if commission > 0 else round(revenue - balance, 2)
        currency = b.findtext("sale_currency") or "EUR"
        print(f"   - Booking #{b_id} ({status_text}): {b_name} | Customer: {customer} | Gross: €{revenue:.2f} | Net Profit: €{net_profit:.2f} {currency}")
