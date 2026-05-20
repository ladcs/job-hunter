from __future__ import annotations

import logging
import datetime

from Jobs.Fetch_Config import Fetch_Config
from Jobs.util.clean_html import HTMLCleaner
from Models.Job_Listing import Job_Listing
from Ia_generative.api.Ai_model.Request_LLM import Request_LLM
from Ia_generative.api.Ai_model.OpenAI.Job_Requirement_extractor import Job_Requirement_Extractor_Config
from Jobs.util.parse_response_llm import ParseResponseLLM

from skills.util.Normalize_skill import Normalize_skill
from skills.util.categories import SKILL_CATEGORIES

logger = logging.getLogger(__name__)
parse_response_llm = ParseResponseLLM()


class Job_Listing_Enrich:
    def __init__(
        self,
        config: Fetch_Config,
        cleaner: HTMLCleaner | None = None,
    ):
        self._cleaner = cleaner or HTMLCleaner(selectors=config.job_content_selector)
        self.config = config

    def html_enrich(self, job: Job_Listing, html: str) -> None:
        try:
            job.html = html
        except Exception as e:
            logger.error(
                "Erro ao enriquecer HTML para '%s': %s",
                job.title, str(e)
            )

    def content_enrich(self, job: Job_Listing) -> None:
        job.content = self._cleaner.extract_job_content(job.html)

    
    def content_to_llm_enrich(self, job: Job_Listing) -> None:
        job.content_to_llm = self.config._clean_content(job.html)

    def requirements_enrich(self, job: Job_Listing) -> None:
        if not job.content_to_llm:
            logger.warning(
                    "Vaga sem conteúdo para extração de requisitos."
                )
            return
        
        prompt_config = Job_Requirement_Extractor_Config(job.content_to_llm, job.title)
        llm = Request_LLM(Ai_config=prompt_config)
        try:
            requirements = llm.model_request()            
            job.requirements = parse_response_llm._parse_requirements(requirements)
        except Exception as e:
            logger.error(
                "Erro ao extrair requisitos para '%s': %s",
                job.title, str(e)
            )
        
        not_categories = []

        for skill in job.requirements:
                normalized_skill = Normalize_skill.normalize(skill.skill)
                skill.skill = normalized_skill
                category = SKILL_CATEGORIES.get(normalized_skill, None)
                if not category:
                    if any(word in skill.skill.lower() for word in ["oracle", "aws"]):
                        category = "cloud"
                    else:
                        not_categories.append(skill.skill)
                        continue
                skill.category = category
            
        if len(not_categories) > 0:
            with open(
                f"missing_categories_{datetime.date.today().strftime('%Y%m%d')}.txt",
                "a",
                encoding="utf-8"
            ) as f:
                f.write("\n".join(not_categories) + "\n")