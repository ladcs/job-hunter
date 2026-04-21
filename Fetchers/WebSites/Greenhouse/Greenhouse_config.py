from Fetchers.Fetch_Config import Fetch_Config 
from Fetchers.WebSites.Greenhouse.Get_greenhouse import Get_Greenhouse
from Models.Job_Listing import Job_Listing
from requests import Response


class Greenhouse_Config(Fetch_Config):
    """Base para todos os sites que usam Greenhouse."""

    @property
    def job_content_selector(self) -> list[str] | None:
        return None

    def parse_listings(self, response: Response) -> list[Job_Listing]:
        return Get_Greenhouse().parse_listings(response)