from requests import Response

from bs4 import BeautifulSoup
from Fetchers.Fetch_Config import Fetch_Config
from Models.Job_Listing import Job_Listing


class Nubank_Config(Fetch_Config):

    @property
    def job_content_selector(self) -> list[str]:
        return ["div.job-description__content", "div.job-page__content"]

    @property
    def url(self) -> str:
        return "https://international.nubank.com.br/careers/brazil/"

    @property
    def base_job_url(self) -> str:
        return "https://international.nubank.com.br/job-opportunity"

    @property
    def exclude_keywords(self) -> list[str]:
        return ["lead", "III", "senior", "security", "exclusiva", "principal", "staff", "SOx"]

    @property
    def include_keywords(self) -> list[str]:
        return ["IT", "TI", "engineer", "engenheiro", "Engenheira"]
    

    def parse_listings(self, response: Response) -> list[Job_Listing]:
        soup = BeautifulSoup(response.text, "html.parser")
        seen_ids: set[str] = set()
        listings: list[Job_Listing] = []

        for card in soup.select("a.job-card"):
            href = card.get("href", "")
            job_id = href.split("id=")[-1].strip() if "id=" in href else None

            if not job_id or job_id in seen_ids:
                continue
            seen_ids.add(job_id)

            title_el = card.select_one(".job-card__text p")
            title = title_el.get_text(strip=True) if title_el else ""

            location_el = card.select_one(".chip__text")
            location = location_el.get_text(strip=True) if location_el else ""

            listings.append(Job_Listing(
                id=job_id,
                title=title,
                location=location,
                url=f"{self.base_job_url}?id={job_id}",
            ))

        return listings
