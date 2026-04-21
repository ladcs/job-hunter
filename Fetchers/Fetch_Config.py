from abc import ABC, abstractmethod
from bs4 import BeautifulSoup                        # faltava
from Models.Job_Listing import Job_Listing

class Fetch_Config(ABC):

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
    def parse_listings(self, soup: BeautifulSoup) -> list[Job_Listing]:
        """
        Recebe o BeautifulSoup da página e devolve a lista de vagas cruas.
        Cada subclasse sabe como o HTML do seu próprio site é estruturado.
        """
        ...