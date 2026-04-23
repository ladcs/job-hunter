from __future__ import annotations

import time
import requests
import re

from Fetchers.Fetch_Config import Fetch_Config
from Models.Job_Listing import Job_Listing    
import unicodedata

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
        config: Fetch_Config,
        request_delay: float = 1.5,
        headers: dict | None = None,
    ):
        self._config = config
        self._request_delay = request_delay
        self._headers = headers or self._DEFAULT_HEADERS
        self._raw_listings: list[Job_Listing] = []
        self._filtered_listings: list[Job_Listing] = []

    def _normalize(self, text: str) -> str:
        return unicodedata.normalize("NFKD", text)\
            .encode("ascii", "ignore")\
            .decode("ascii")\
            .lower()

    def fetch(self) -> list[Job_Listing]:
        self._raw_listings = self._scrape()
        self._filtered_listings = self._filter(self._raw_listings)
        return self._filtered_listings

    @property
    def raw_count(self) -> int:
        return len(self._raw_listings)

    @property
    def filtered_count(self) -> int:
        return len(self._filtered_listings)

    def _scrape(self) -> list[Job_Listing]:
        time.sleep(self._request_delay)

        response = requests.get(
            self._config.url,
            headers=self._headers,
            timeout=15,
        )
        response.raise_for_status()

        return self._config.parse_listings(response)

    def _filter(self, listings: list[Job_Listing]) -> list[Job_Listing]:
        return [
            job for job in listings
            if not self._is_excluded(job.title)
            and self._is_included(job.title)
        ]

    def _is_excluded(self, title: str) -> bool:
        if not self._config.exclude_keywords:
            return False
        
        title_norm = self._normalize(title)

        return any(
            re.search(rf"(?<!\w){re.escape(self._normalize(kw))}(?!\w)", title_norm)
            for kw in self._config.exclude_keywords
        )

    def _is_included(self, title: str) -> bool:
        if not self._config.include_keywords:
            return True
        
        title_norm = self._normalize(title)

        return any(
            re.search(rf"(?<!\w){re.escape(self._normalize(kw))}(?!\w)", title_norm)
            for kw in self._config.include_keywords
        )
