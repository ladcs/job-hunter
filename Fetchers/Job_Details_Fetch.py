from __future__ import annotations

import re
import time
import logging
import requests

from Fetchers.Fetch_Config import Fetch_Config
from Fetchers.util.clean_html import HTMLCleaner
from Models.Job_Listing import Job_Listing
from Ia_generative.api.Ai_model.Request_LLM import Request_LLM
from Ia_generative.api.Ai_model.OpenAI.Job_Requirement_extractor import Job_Requirement_Extractor_Config
from Fetchers.util.parse_response_llm import ParseResponseLLM

logger = logging.getLogger(__name__)
parse_response_llm = ParseResponseLLM()


class Job_Details_Fetcher:

    MAX_RETRIES = 5
    BACKOFF_BASE = 2
    MAX_YEARS = 2

    BEFORE_PATTERN = re.compile(
        r"""
        (?:
            experi[êe]ncia[:\s]+(?:de\s+)?(?:m[ií]nima[:\s]+)?
            |
            at\s+least\s+|minim(?:um|o)\s+|more\s+than\s+|over\s+|above\s+
            |
            no\s+m[ií]nimo\s+|m[ií]nimo\s+|comprovada\s+de\s+|acima\s+de\s+
            |
            experi[êe]ncia\s+comprovada\s+de\s+
            |
            desej[aá]vel[:\s]+(?:no\s+m[ií]nimo\s+)?
        )
        (\d+)
        (?:\s*\+|\s*-\s*\d+|\s+a\s+\d+)?
        \s*anos?\b
        """,
        re.IGNORECASE | re.VERBOSE
    )

    AFTER_PATTERN = re.compile(
        r"""
        (?:de\s+|entre\s+)?
        (\d+)
        (?:\s*\+|\s*-\s*\d+|\s+a\s+\d+)?
        \s*
        (?:
            anos?\s+de\s+experi[êe]ncia
            |
            years?\s+of\s+experience
            |
            anos?\s+como
            |
            years?\s+(?:in|working|managing|of)
            |
            anos?\s+em\s+projetos
        )
        """,
        re.IGNORECASE | re.VERBOSE
    )

    _DEFAULT_HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
    }

    def __init__(
        self,
        config: Fetch_Config,
        cleaner: HTMLCleaner | None = None,
        request_delay: float = 1.5,
        headers: dict | None = None,
        max_years: int = MAX_YEARS,
    ):
        self._config = config
        self._cleaner = cleaner or HTMLCleaner(selectors=config.job_content_selector)
        self._request_delay = request_delay
        self._headers = headers or self._DEFAULT_HEADERS
        self._max_years = max_years

    def enrich(self, listings: list[Job_Listing]) -> list[Job_Listing]:
        """
        Para cada vaga:
        1. Busca o HTML de detalhe se ainda não estiver preenchido
        2. Verifica requisito de anos de experiência — descarta se > max_years
        3. Popula job.content via HTMLCleaner
        
        Retorna apenas as vagas que passaram pelo filtro de anos.
        """
        result = []

        for job in listings:
            if not self._enrich_job(job):
                continue
            job.requirements = self.enrich_request(job)
            result.append(job)
        return result
    
    def enrich_request(self, job: Job_Listing) -> Job_Listing | None:
        """
        enrich que usa LLM para extrair requisitos.
        Pode ser usada para pegar os requisitos da vaga.
        """
        if not job.content:
            logger.warning(
                    "Vaga sem conteúdo para extração."
                )
            return None

        prompt_config = Job_Requirement_Extractor_Config(job.content)
        llm = Request_LLM(Ai_config=prompt_config)
        try:
            requirements = llm.model_request()
            
            return parse_response_llm._parse_requirements(requirements)
        except Exception as e:
            logger.error(
                "Erro ao extrair requisitos para '%s': %s",
                job.title, str(e)
            )
            return None
        

    def _enrich_job(self, job: Job_Listing) -> bool:
        """
        Retorna True se a vaga passou o filtro de anos, False se deve ser descartada.
        """
        if not job.html:
            html = self._fetch_with_retry(job)
            if html is None:
                return False
            job.html = html

        print(job.url)
        if not self._passes_experience_filter(job.html, job.title):
            return False

        job.content = self._cleaner.extract_job_content(job.html)
        return True

    def _passes_experience_filter(self, html: str, title: str) -> bool:
        matches = self.BEFORE_PATTERN.findall(html) + self.AFTER_PATTERN.findall(html)

        if not matches:
            return True

        max_found = max(int(y) for y in matches)

        if max_found > self._max_years:
            logger.info(
                "Vaga descartada por experiência: '%s' exige %d anos (máximo permitido: %d).",
                title, max_found, self._max_years
            )
            return False

        return True

    def _fetch_with_retry(self, job: Job_Listing) -> str | None:
        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                time.sleep(self._request_delay)
                response = requests.get(
                    job.url,
                    headers=self._headers,
                    timeout=15,
                )
                response.raise_for_status()
                return response.text

            except requests.RequestException:
                wait = self.BACKOFF_BASE ** attempt
                logger.warning(
                    "Tentativa %d/%d falhou para '%s' [%s]. Aguardando %ds.",
                    attempt, self.MAX_RETRIES, job.title, job.url, wait
                )
                if attempt < self.MAX_RETRIES:
                    time.sleep(wait)
                else:
                    logger.error(
                        "Todas as %d tentativas falharam para '%s' [%s]. Pulando.",
                        self.MAX_RETRIES, job.title, job.url
                    )
                    return None
               