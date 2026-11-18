import os
import time
import requests
import json

from dotenv import load_dotenv
# We can use the tiqets-ads-sync .env since it has the same META_ACCESS_TOKEN and META_PIXEL_ID
load_dotenv(dotenv_path="/Users/adamdimitrov/Development/tiqets-ads-sync/.env")
META_ACCESS_TOKEN = os.environ.get("META_ACCESS_TOKEN")
META_PIXEL_ID = os.environ.get("META_PIXEL_ID")

test_code = "TEST25452"
order_id = "LEGENDA-TEST-999"
fbclid = "AdamLegendaTest"

timestamp = int(time.time())
fbc = f"fb.1.{timestamp}.{fbclid}"

payload = {
    "data": [
        {
            "event_name": "Purchase",
            "event_time": timestamp,
            "action_source": "website",
            "user_data": {
                "fbc": fbc
            },
            "custom_data": {
                "value": 15.50, # Fake commission for Legenda
                "currency": "EUR",
                "content_name": "Legenda River Cruise"
            },
            "event_id": order_id
        }
    ],
    "test_event_code": test_code
}

url = f"https://graph.facebook.com/v20.0/{META_PIXEL_ID}/events?access_token={META_ACCESS_TOKEN}"
try:
    res = requests.post(url, json=payload)
    print("STATUS:", res.status_code)
    print("RESPONSE:", res.text)
except Exception as e:
    print("ERROR:", e)
