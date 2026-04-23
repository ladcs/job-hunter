from requests import Response
from bs4 import BeautifulSoup

from Fetchers.Fetch_Config import Fetch_Config
from Models.Job_Listing import Job_Listing


class B3_Config(Fetch_Config):

    @property
    def url(self) -> str:
        return "https://vagas.b3.com.br/go/todas-vagas/4559419/"
    
    @property
    def job_content_selector(self) -> list[str]:
        return ["div.jobDisplay"]

    @property
    def base_job_url(self) -> str:
        return "https://vagas.b3.com.br"

    @property
    def exclude_keywords(self) -> list[str]:
        return ["senior", "lead", "principal", "manager", "diretor", "sênior", "líder", "gerente", "coordenador", "supervisor", "sr.", "sr", "staff", "sr"]

    @property
    def include_keywords(self) -> list[str]:
        return ["software", "tecnologia", "dados", "automação", "automacao"]

    def parse_listings(self, response: Response) -> list[Job_Listing]:
        soup = BeautifulSoup(response.text, "html.parser")

        listings: list[Job_Listing] = []
        seen_ids: set[str] = set()

        for link in soup.select("li a[href*='/job/']"):
            href = link.get("href", "").strip()
            title = link.get_text(strip=True)

            if not href or not title:
                continue

            job_id = href.rstrip("/").split("/")[-1]

            if job_id in seen_ids:
                continue
            seen_ids.add(job_id)

            full_url = href if href.startswith("http") else f"{self.base_job_url}{href}"

            listings.append(Job_Listing(
                id=job_id,
                title=title,
                location="São Paulo",
                url=full_url,
            ))

        return listings