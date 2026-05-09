from __future__ import annotations

from abc import ABC, abstractmethod
import re

from Jobs.Fetch_Config import Fetch_Config
from Models.Job_Listing import Job_Listing    
import unicodedata

class Filter_Word_Pre_Llm(ABC):
    def __init__(
        self,
        config: Fetch_Config,
    ):
        self._config = config
        self._raw_listings: list[Job_Listing] = []
        self._filtered_listings: list[Job_Listing] = []

    def _normalize(self, text: str) -> str:
        return unicodedata.normalize("NFKD", text)\
            .encode("ascii", "ignore")\
            .decode("ascii")\
            .lower()
    
    @abstractmethod
    def filter(self, listings: list[Job_Listing]) -> list[Job_Listing]:
        """"
        Configura o filtro para a lista de vagas, usando as palavras-chave de inclusão e exclusão.
        """
    
    def _is_excluded(self, content: str) -> bool:
        if not self._config.exclude_keywords:
            return False
        
        content_norm = self._normalize(content)

        return any(
            re.search(rf"(?<!\w){re.escape(self._normalize(kw))}(?!\w)", content_norm)
            for kw in self._config.exclude_keywords
        )

    def _is_included(self, content: str) -> bool:
        if not self._config.include_keywords:
            return True
        
        content_norm = self._normalize(content)

        return any(
            re.search(rf"(?<!\w){re.escape(self._normalize(kw))}(?!\w)", content_norm)
            for kw in self._config.include_keywords
        )