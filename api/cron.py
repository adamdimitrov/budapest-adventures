import os
import time
import hmac
import hashlib
import base64
import json
import urllib.request
import urllib.parse
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            self.process_cron()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "success"}')
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode())

    def process_cron(self):
        channel_id = os.environ.get("TOURCMS_CHANNEL_ID", "16485")
        api_key = os.environ.get("TOURCMS_API_KEY", "51405b89d978")
        meta_token = os.environ.get("META_ACCESS_TOKEN")
        meta_pixel = os.environ.get("META_PIXEL_ID")

        # Fetch bookings from TourCMS
        bookings = self.fetch_tourcms_bookings(channel_id, api_key)
        
        # Process and send to Meta
        for booking in bookings:
            # TourCMS stores affiliate tags usually in agent_ref or custom fields
            agent_ref = booking.get('agent_ref', '')
            
            fbclid = None
            if agent_ref and 'fbclid:' in agent_ref:
                # Extract fbclid:xxx|gclid:yyy
                parts = agent_ref.split('|')
                for part in parts:
                    if part.startswith('fbclid:'):
                        fbclid = part.split(':')[1]
            
            if fbclid:
                self.send_to_meta(booking, fbclid, meta_token, meta_pixel)

    def fetch_tourcms_bookings(self, channel_id, api_key):
        # We search the last few days of bookings
        verb = "GET"
        marketplace_id = "0"
        path = f"/c/{channel_id}/bookings/search.json"

        outbound_time = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
        string_to_sign = f"{channel_id}/{marketplace_id}/{verb}/{outbound_time}{path}"
        
        raw_key = api_key.encode('utf-8')
        message = string_to_sign.encode('utf-8')
        signature = urllib.parse.quote(base64.b64encode(hmac.new(raw_key, message, hashlib.sha256).digest()).decode('utf-8'))

        headers = {
            "x-tourcms-date": outbound_time,
            "Authorization": f"TourCMS {channel_id}:{marketplace_id}:{signature}",
            "Content-type": "application/json",
            "charset": "utf-8"
        }

        url = f"https://api.tourcms.com{path}"
        req = urllib.request.Request(url, headers=headers)
        
        try:
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                # TourCMS returns a 'booking' array inside 'tour' or 'channel' depending on the query
                # Assuming 'booking' root key based on TourCMS json format
                return data.get('booking', [])
        except Exception as e:
            print("TourCMS API Error:", e)
            return []

    def send_to_meta(self, booking, fbclid, token, pixel):
        if not token or not pixel:
            return

        # Assuming TourCMS booking gives booking_id and total_margin/commission
        event_id = str(booking.get('booking_id', ''))
        value = float(booking.get('total_margin', booking.get('total_price', 0)))
        currency = booking.get('sales_currency', 'EUR')

        timestamp = int(time.time())
        fbc = f"fb.1.{timestamp}.{fbclid}"

        payload = {
            "data": [
                {
                    "event_name": "Purchase",
                    "event_time": timestamp,
                    "action_source": "website",
                    "event_id": event_id,
                    "user_data": {
                        "fbc": fbc
                    },
                    "custom_data": {
                        "value": value,
                        "currency": currency
                    }
                }
            ]
        }

        url = f"https://graph.facebook.com/v19.0/{pixel}/events?access_token={token}"
        data_bytes = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data_bytes, headers={'Content-Type': 'application/json'})
        
        try:
            urllib.request.urlopen(req)
        except Exception as e:
            print("Meta API Error:", e)
