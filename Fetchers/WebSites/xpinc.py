from Fetchers.WebSites.Greenhouse.Greenhouse_config import Greenhouse_Config


class XP_Config(Greenhouse_Config):
    @property
    def url(self) -> str:
        return "https://boards-api.greenhouse.io/v1/boards/xpinc/jobs?content=true"

    @property
    def base_job_url(self) -> str:
        return "https://job-boards.greenhouse.io/xpinc/jobs"

    @property
    def job_content_selector(self) -> list[str]:
        return ["div#content", "div.job-post"]

    @property
    def exclude_keywords(self) -> list[str]:
        return ["senior", "sênior", "lead", "staff", "principal", "coordenador", "sr.", "diretor"]

    @property
    def include_keywords(self) -> list[str]:
        return ["software", "engenheiro", "engenheira", "developer", "desenvolvedor", "desenvolvdora", "automação", "QA"]