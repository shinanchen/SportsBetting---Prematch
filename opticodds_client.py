"""
opticodds_client.py

Minimal OpticOdds API client:
- Uses header auth: X-Api-Key from env var OPTICODDS_API_KEY
- Does NOT inject any default query parameters
- Supports retries and basic rate-limit backoff
"""

from __future__ import annotations

import os
import time
from typing import Any, Dict, Optional

import requests


BASE_URL = "https://api.opticodds.com/api/v3"


class OpticOddsError(Exception):
    pass


def _get_api_key() -> str:
    api_key = os.environ.get("OPTICODDS_API_KEY")
    if not api_key:
        raise OpticOddsError(
            "Missing OPTICODDS_API_KEY environment variable.\n"
            "Set it with:\n"
            "export OPTICODDS_API_KEY='your_api_key_here'"
        )
    return api_key


def get(
    path: str,
    params: Optional[Dict[str, Any]] = None,
    timeout: int = 30,
    retries: int = 3,
    backoff: float = 0.8,
) -> Dict[str, Any]:
    """
    Perform a GET request to the OpticOdds API.

    Important:
    - Only sends params you explicitly pass in
    - Will not add fixture_id/sport/league automatically
    """
    if not path.startswith("/"):
        path = "/" + path

    if params is None:
        params = {}

    url = f"{BASE_URL}{path}"
    headers = {
        "X-Api-Key": _get_api_key(),
        "Accept": "application/json",
    }

    last_err: Optional[Exception] = None

    for attempt in range(retries):
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=timeout)

            # Rate limiting
            if resp.status_code == 429:
                time.sleep(backoff * (attempt + 1))
                continue

            if not resp.ok:
                raise OpticOddsError(f"HTTP {resp.status_code}: {resp.text}")

            return resp.json()

        except (requests.RequestException, OpticOddsError) as e:
            last_err = e
            if attempt == retries - 1:
                raise
            time.sleep(backoff * (attempt + 1))

    # Should never reach here
    raise last_err or OpticOddsError("Unknown error")

