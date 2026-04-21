from requests import Response
from Fetchers.Fetch_Config import Fetch_Config
from Models.Job_Listing import Job_Listing
from pprint import pprint


class Gupy_Portal_Config(Fetch_Config):

    def __init__(self, term: str = "software"):
        self.term = term

    @property
    def url(self) -> str:
        term = self.term.replace(" ", "%20")
        return (
            f"https://employability-portal.gupy.io/api/v1/jobs"
            f"?jobName={term}"
            f"&state=S%C3%A3o%20Paulo"
            f"&limit=50&offset=0"
        )

    @property
    def base_job_url(self) -> str:
        return "https://portal.gupy.io/job-search"

    @property
    def exclude_keywords(self) -> list[str]:
        return ["senior", "sênior", "lead", "staff", "principal", "coordenador", "sr", "afirmativa"]

    @property
    def include_keywords(self) -> list[str]:
        return ["software", "automação", "automacao", "engenheiro", "developer", "desenvolvedor", "desenvolvedora", "engenheira", "QA", "quality assurance"]

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
            ))
        
        pprint(listings)

        return listings