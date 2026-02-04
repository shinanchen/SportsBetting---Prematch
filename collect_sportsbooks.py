import os
import json
import time
import requests
import sseclient  # pip install sseclient-py

API_KEY = os.environ.get("OPTICODDS_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing OPTICODDS_API_KEY")

URL = "https://api.opticodds.com/api/v3/stream/odds/football"

params = {
    "key": API_KEY,
    "league": ["NFL"],
    "market": ["Moneyline"],
    # keep it simple, no fixture_id needed for discovery
}

r = requests.get(URL, params=params, stream=True)
client = sseclient.SSEClient(r)

seen = {}
start = time.time()
duration = 30  # seconds

for event in client.events():
    if time.time() - start > duration:
        break
    if event.event not in ("odds", "locked-odds"):
        continue

    data = json.loads(event.data)
    for o in data.get("data", []):
        sbid = o.get("sportsbook_id")
        sbname = o.get("sportsbook")
        if sbid:
            seen[sbid] = sbname or sbid

print("sportsbooks found:", len(seen))
for k in sorted(seen):
    print(k, "=>", seen[k])

