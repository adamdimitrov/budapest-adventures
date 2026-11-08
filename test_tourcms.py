import os
from tourcms.tourcms import TourCMS

# TourCMS credentials
channel_id = 16485
marketplace_id = 0
api_key = "51405b89d978"

conn = TourCMS(0, api_key, "simple")

# Search bookings
res = conn.search_bookings(channel_id=channel_id)
print(res)
