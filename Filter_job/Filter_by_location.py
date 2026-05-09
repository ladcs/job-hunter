from typing import List
import unicodedata

from Models.Job_Listing import Job_Listing


class Filter_by_location:
    LOCATIONS = [
        "São Paulo",
        "Paraná",
        "Remote"
    ]

    def __init__(self, locations: List[str] = LOCATIONS):
        self._locations = [
            self._normalize(location)
            for location in locations
        ]

    def _normalize(self, text: str) -> str:
        return (
            unicodedata.normalize("NFKD", text)
            .encode("ascii", "ignore")
            .decode("ascii")
            .lower()
            .strip()
        )

    def filter(self, listings: List[Job_Listing]) -> List[Job_Listing]:
        if not self._locations:
            return listings

        filtered = []

        for job in listings:
            if not job.location:
                continue

            job_location = self._normalize(job.location)

            if any(location in job_location for location in self._locations):
                filtered.append(job)

        return filtered