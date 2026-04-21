from requests import Response
from Models.Job_Listing import Job_Listing

from Fetchers.Fetch_Config import Fetch_Config
from Fetchers.WebSites.Greenhouse.Get_greenhouse import Get_Greenhouse


class BTGPactual_Config(Fetch_Config):
    def __init__(self, parser=None):
        self.fetcher = parser or Get_Greenhouse()

    @property
    def url(self) -> str:
        return "https://boards-api.greenhouse.io/v1/boards/btgpactual/jobs?content=true"

    @property
    def base_job_url(self) -> str:
        return "https://carreiras.btgpactual.com/vagas"

    @property
    def exclude_keywords(self) -> list[str]:
        return ["coordenador", "afirmativa","mobile", "flutter", "senior", "security", "staff", "principal", "sênior", "angular"]

    @property
    def include_keywords(self) -> list[str]:
        return ["software"]
    
    def parse_listings(self, response: Response) -> list[Job_Listing]:
        return self.fetcher.parse_listings(response)