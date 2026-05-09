from abc import ABC, abstractmethod
from typing import List
from Models.Job_Listing import Job_Listing
from requests import Response

class Fetch_Config(ABC):

    @property
    def job_content_selector(self) -> List[str] | None: ...

    @property
    @abstractmethod
    def url(self) -> str: ...

    @property
    @abstractmethod
    def base_job_url(self) -> str: ...

    @property
    @abstractmethod
    def exclude_keywords(self) -> list[str]: ...

    @property
    @abstractmethod
    def include_keywords(self) -> list[str]: ...

    @abstractmethod
    def parse_listings(self, response: Response) -> list[Job_Listing]:
        """
        Recebe a resposta da requisição e devolve a lista de vagas cruas.
        Cada subclasse sabe como o HTML do seu próprio site é estruturado.
        """
        ...

    @abstractmethod
    def _clean_content(self, html: str) -> str:
        """
        Recebe o conteúdo bruto da vaga e devolve o conteúdo limpo.
        Cada subclasse pode ter regras específicas de limpeza, ou usar um HTMLCleaner genérico.
        """
        ...