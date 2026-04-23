from Fetchers.WebSites.Greenhouse.Greenhouse_config import Greenhouse_Config


class BTGPactual_Config(Greenhouse_Config):    
    @property
    def url(self) -> str:
        return "https://boards-api.greenhouse.io/v1/boards/btgpactual/jobs?content=true"

    @property
    def base_job_url(self) -> str:
        return "https://carreiras.btgpactual.com/vagas"

    @property
    def exclude_keywords(self) -> list[str]:
        return ["coordenador", "afirmativa","mobile", "flutter", "senior", "security", "staff", "principal", "sênior", "angular", "lead"]

    @property
    def include_keywords(self) -> list[str]:
        return ["software"]
