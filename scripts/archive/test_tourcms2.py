import tourcms

# TourCMS credentials
channel_id = 16485
api_key = "51405b89d978"

conn = tourcms.Connection(0, api_key, "simple")
# Or maybe it's tourcms.TourCMS()
print(dir(tourcms))
