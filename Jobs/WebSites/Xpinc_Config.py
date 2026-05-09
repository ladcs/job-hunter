from bs4 import BeautifulSoup
import re

from Jobs.WebSites.Greenhouse.Greenhouse_config import Greenhouse_Config

from pprint import pprint


class XP_Config(Greenhouse_Config):
    @property
    def url(self) -> str:
        return "https://boards-api.greenhouse.io/v1/boards/xpinc/jobs?content=true"

    @property
    def base_job_url(self) -> str:
        return "https://job-boards.greenhouse.io/xpinc/jobs"

    @property
    def exclude_keywords(self) -> list[str]:
        return ["senior", "sênior", "lead", "staff", "principal", "coordenador", "sr", "diretor", "exclusiva"]

    @property
    def include_keywords(self) -> list[str]:
        return ["software", "engenheiro", "engenheira", "developer", "desenvolvedor", "desenvolvdora", "automação"]
    
    def _clean_content(self, html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")

        content = soup.get_text(
            separator="\n",
            strip=True
        ).lower()

        content = re.sub(
            r"^.*?imposs[ií]vel\.?",
            "",
            content,
            flags=re.IGNORECASE | re.DOTALL
        )

        content = re.sub(
            r"benef[ií]cios.*$",
            "",
            content,
            flags=re.IGNORECASE | re.DOTALL
        )

        return content.strip()
