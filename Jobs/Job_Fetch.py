from __future__ import annotations

import time
import random
import requests

from Models.Job_Listing import Job_Listing    

class Job_Fetcher:

    _DEFAULT_HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
    }

    def __init__(
        self,
        headers: dict | None = None,
    ):
        self._headers = headers or self._DEFAULT_HEADERS


    def fetch(self, url: str) -> list[Job_Listing]:
        response = requests.get(
            url,
            headers=self._headers,
            timeout=15,
        )
        response.raise_for_status()
        return response
