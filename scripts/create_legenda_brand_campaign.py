import urllib.request
import urllib.parse
import json
import sys
import os

env_path = "/Users/adamdimitrov/Development/budapest-adventures/.env"
env_vars = {}
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env_vars[k.strip()] = v.strip()

# 1. Fetch OAuth Token
data = urllib.parse.urlencode({
    "client_id": env_vars["GOOGLE_ADS_CLIENT_ID"],
    "client_secret": env_vars["GOOGLE_ADS_CLIENT_SECRET"],
    "refresh_token": env_vars["GOOGLE_ADS_REFRESH_TOKEN"],
    "grant_type": "refresh_token"
}).encode("utf-8")

req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data, method="POST")
with urllib.request.urlopen(req) as resp:
    token = json.loads(resp.read().decode())["access_token"]

customer_id = env_vars["GOOGLE_ADS_CUSTOMER_ID"].replace("-", "")
dev_token = env_vars.get("GOOGLE_ADS_DEVELOPER_TOKEN")

headers = {
    "Authorization": f"Bearer {token}",
    "developer-token": dev_token,
    "Content-Type": "application/json"
}

def api_call(endpoint, payload):
    url = f"https://googleads.googleapis.com/v26/customers/{customer_id}/{endpoint}"
    r = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(r) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode()
        print(f"Error on {endpoint}: {e.code}\n{err_msg}", file=sys.stderr)
        raise

if __name__ == "__main__":
    print(f"Creating Legenda Brand Search Campaign on customer {customer_id}...")

    # 1. Create Campaign Budget (€10/day)
    budget_payload = {
        "operations": [
            {
                "create": {
                    "name": "[BUDGET] Budapest - Legenda Brand (€10/day)",
                    "amountMicros": "10000000",
                    "deliveryMethod": "STANDARD"
                }
            }
        ]
    }
    budget_res = api_call("campaignBudgets:mutate", budget_payload)
    budget_resource = budget_res["results"][0]["resourceName"]
    print(f"✓ Budget Created: {budget_resource}")

    # 2. Create Campaign (Target Spend / Maximize Clicks with €0.20 CPC bid ceiling)
    campaign_payload = {
        "operations": [
            {
                "create": {
                    "name": "[SEARCH] Budapest - Legenda Brand (Max Clicks €0.20, €10/day)",
                    "status": "PAUSED",
                    "advertisingChannelType": "SEARCH",
                    "campaignBudget": budget_resource,
                    "containsEuPoliticalAdvertising": "DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING",
                    "targetSpend": {
                        "cpcBidCeilingMicros": "200000"
                    },
                    "networkSettings": {
                        "targetGoogleSearch": True,
                        "targetSearchNetwork": False,
                        "targetContentNetwork": False
                    },
                    "geoTargetTypeSetting": {
                        "positiveGeoTargetType": "PRESENCE"
                    }
                }
            }
        ]
    }
    camp_res = api_call("campaigns:mutate", campaign_payload)
    campaign_resource = camp_res["results"][0]["resourceName"]
    print(f"✓ Campaign Created: {campaign_resource}")

    # 3. Add Language (English) + Geo Targets + Negative Keywords
    geo_locations = [
        "geoTargetConstants/1007677", # Budapest, Hungary
        "geoTargetConstants/2840",    # United States
        "geoTargetConstants/2826",    # United Kingdom
        "geoTargetConstants/2276",    # Germany
        "geoTargetConstants/2124",    # Canada
        "geoTargetConstants/2036"     # Australia
    ]

    negatives = [
        "free", "jobs", "career", "careers", "address", "phone", "telephone",
        "cancel", "cancellation", "refund", "login", "map", "directions", "parking", "recruitment"
    ]

    criteria_operations = [
        {
            "create": {
                "campaign": campaign_resource,
                "language": {
                    "languageConstant": "languageConstants/1000"
                }
            }
        }
    ]

    for geo in geo_locations:
        criteria_operations.append({
            "create": {
                "campaign": campaign_resource,
                "location": {
                    "geoTargetConstant": geo
                }
            }
        })

    for neg in negatives:
        criteria_operations.append({
            "create": {
                "campaign": campaign_resource,
                "negative": True,
                "keyword": {
                    "text": neg,
                    "matchType": "BROAD"
                }
            }
        })

    crit_res = api_call("campaignCriteria:mutate", {"operations": criteria_operations})
    print(f"✓ Added {len(crit_res['results'])} Campaign Criteria (English + 6 Geo Targets + {len(negatives)} Negatives)")

    # 4. Create Ad Group
    ad_group_payload = {
        "operations": [
            {
                "create": {
                    "name": "Legenda City Cruises - Exact & Phrase (€0.20)",
                    "campaign": campaign_resource,
                    "status": "ENABLED",
                    "type": "SEARCH_STANDARD"
                }
            }
        ]
    }
    ag_res = api_call("adGroups:mutate", ad_group_payload)
    ad_group_resource = ag_res["results"][0]["resourceName"]
    print(f"✓ Ad Group Created: {ad_group_resource}")

    # 5. Add Brand Keywords
    keywords = [
        {"text": "legenda city cruises", "matchType": "EXACT"},
        {"text": "legenda city cruises", "matchType": "PHRASE"},
        {"text": "legenda budapest", "matchType": "EXACT"},
        {"text": "legenda cruise budapest", "matchType": "PHRASE"},
        {"text": "legenda dinner cruise", "matchType": "EXACT"},
        {"text": "legenda candlelit dinner", "matchType": "PHRASE"},
        {"text": "legenda boat tour budapest", "matchType": "EXACT"},
        {"text": "legenda duna bella", "matchType": "PHRASE"}
    ]

    kw_operations = []
    for kw in keywords:
        kw_operations.append({
            "create": {
                "adGroup": ad_group_resource,
                "status": "ENABLED",
                "keyword": {
                    "text": kw["text"],
                    "matchType": kw["matchType"]
                }
            }
        })

    kw_res = api_call("adGroupCriteria:mutate", {"operations": kw_operations})
    print(f"✓ Added {len(kw_res['results'])} Keywords")

    # 6. Create Responsive Search Ad (RSA)
    final_url = "https://www.budapestadventures.com/best-budapest-river-cruises"
    rsa_payload = {
        "operations": [
            {
                "create": {
                    "adGroup": ad_group_resource,
                    "status": "ENABLED",
                    "ad": {
                        "finalUrls": [final_url],
                        "responsiveSearchAd": {
                            "headlines": [
                                {"text": "Legenda Cruises Budapest", "pinnedField": "HEADLINE_1"},
                                {"text": "Official Partner Booking"},
                                {"text": "Dock 7 Departure Schedule"},
                                {"text": "Candlelit Dinner & Drinks"},
                                {"text": "Danube Legend Sightseeing"},
                                {"text": "Live Real-Time Seats"},
                                {"text": "Free 24h Cancellation"},
                                {"text": "Verified Budapest Reviews"},
                                {"text": "Instant Mobile QR Tickets"},
                                {"text": "Compare & Book Direct"}
                            ],
                            "descriptions": [
                                {"text": "Legenda Danube cruises with welcome drink & audio guide. Dock 7 departures."},
                                {"text": "Comparison of Legenda sightseeing & candlelit dinner cruises. 2026 timetable."},
                                {"text": "Official authorized ticket partner for Legenda Budapest. Instant QR boarding pass."},
                                {"text": "Save on Danube Legend & Duna Bella cruises. 100% full refund up to 24h before."}
                            ],
                            "path1": "budapest",
                            "path2": "legenda"
                        }
                    }
                }
            }
        ]
    }
    ad_res = api_call("adGroupAds:mutate", rsa_payload)
    ad_resource = ad_res["results"][0]["resourceName"]
    print(f"✓ Responsive Search Ad Created: {ad_resource}")
    print("\n🎉 ALL DONE! Campaign is created and safely PAUSED for your review.")
