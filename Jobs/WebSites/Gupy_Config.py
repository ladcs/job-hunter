import re

from bs4 import BeautifulSoup
from requests import Response
from Jobs.Fetch_Config import Fetch_Config
from Models.Job_Listing import Job_Listing

class Gupy_Portal_Config(Fetch_Config):

    def __init__(self, term: str = "software"):
        self.term = term

    @property
    def job_content_selector(self) -> list[str]:
        return None

    @property
    def url(self) -> str:
        term = self.term.replace(" ", "%20")
        return (
            f"https://employability-portal.gupy.io/api/v1/jobs"
            f"?jobName={term}"
            f"&limit=50&offset=0"
        )

    @property
    def base_job_url(self) -> str:
        return "https://portal.gupy.io/job-search"

    @property
    def exclude_keywords(self) -> list[str]:
        return ["senior", "sênior", "lead", "staff", "principal", "coordenador", "sr", "afirmativa", "Exclusivo para"]

    @property
    def include_keywords(self) -> list[str]:
        return ["software", "automação", "automacao", "engenheiro", "developer", "desenvolvedor", "desenvolvedora", "engenheira"]

    def parse_listings(self, response: Response) -> list[Job_Listing]:
        data = response.json()
        listings: list[Job_Listing] = []

        for job in data.get("data", []):
            city = job.get("city", "") or ""
            state = job.get("state", "") or ""
            location = f"{city} - {state}".strip(" -") if city or state else "Remoto"


            listings.append(Job_Listing(
                id=str(job.get("id", "")),
                title=job.get("name", ""),
                location=location,
                url=job.get("jobUrl", ""),
                content_to_llm=None,
                content=job.get("description", ""),
                html=None
            ))
        return listings
    
    def _clean_content(self, html: str) -> str | None:

        soup = BeautifulSoup(html, "html.parser")

        sections_text = []
        get = ["Responsabilidades e atribuições", "Requisitos e qualificações"]

        for section_name in get:
            header = soup.find("h2", attrs={
                "data-testid": f"section-{section_name}-title"
            })
            if not header:
                return
            div = header.find_parent("div")
            texto_secao = div.get_text(separator="\n", strip=True)
            sections_text.append(texto_secao)

        content = "\n\n".join(sections_text)

        return content
