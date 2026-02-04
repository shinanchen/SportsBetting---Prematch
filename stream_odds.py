from dotenv import load_dotenv
load_dotenv()

import json
import os
import time
import requests
import sseclient



BASE_URL = "https://api.opticodds.com/api/v3"


def stream_odds(
    sport: str,
    params: dict,
    api_key_env: str = "OPTICODDS_API_KEY",
):
    api_key = os.environ.get(api_key_env)
    if not api_key:
        raise RuntimeError(f"Missing {api_key_env} environment variable")

    url = f"{BASE_URL}/stream/odds/{sport}"

    headers = {
        "X-Api-Key": api_key,
        "Accept": "text/event-stream",
    }

    last_entry_id = None

    while True:
        try:
            # if OpticOdds supports resuming via last_entry_id, include it
            connect_params = dict(params)
            if last_entry_id:
                connect_params["last_entry_id"] = last_entry_id

            r = requests.get(
                url,
                headers=headers,
                params=connect_params,
                stream=True,
                timeout=60,  # connection timeout; stream stays open
            )

            if r.status_code != 200:
                raise RuntimeError(f"HTTP {r.status_code}: {r.text}")

            client = sseclient.SSEClient(r)

            for event in client.events():
                # event.event might be: "odds", "locked-odds", "ping", etc.
                if not event.data:
                    continue

                if event.event in ("odds", "locked-odds"):
                    payload = json.loads(event.data)
                    last_entry_id = payload.get("entry_id", last_entry_id)

                    # payload["data"] is usually a list of odds objects
                    print(event.event, "entry_id=", last_entry_id, "n=", len(payload.get("data", [])))

                    # print first item as an example
                    if payload.get("data"):
                        print(json.dumps(payload["data"][0], indent=2)[:1500])
                else:
                    # other events like heartbeat/ping
                    print(event.event, event.data[:200])

        except (requests.exceptions.ChunkedEncodingError, requests.exceptions.ConnectionError):
            print("Disconnected. Reconnecting in 2s...")
            time.sleep(2)
        except requests.exceptions.ReadTimeout:
            print("Read timeout. Reconnecting in 2s...")
            time.sleep(2)
        except Exception as e:
            print("Fatal error:", repr(e))
            time.sleep(5)


if __name__ == "__main__":
    # Example filters: adjust to your use case
    params = {
        # use arrays for filters where supported
        "sportsbook": ["DraftKings", "FanDuel"],
        "market": ["moneyline"],          # moneyline only
        "league": ["nba"],                # or "ncaab", etc.
        # "fixture_id": ["202601231A7A576D"],  # optional, if you want only one game
        # "is_main": True,                 # optional, if supported
    }

    stream_odds("basketball", params)
