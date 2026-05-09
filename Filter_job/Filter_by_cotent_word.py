

import re
from typing import List

from Jobs import Fetch_Config
from Filter_job.Filter_Word_Pre_Llm import Filter_Word_Pre_Llm
from Models.Job_Listing import Job_Listing


INCLUDE_KEYWORDS = ["java", "python", "javascript", "typescript", "c#"]

class Filter_By_Content_Word(Filter_Word_Pre_Llm):
    def __init__(self, config: Fetch_Config, include: List[str] = INCLUDE_KEYWORDS):
        super().__init__(config)
        self._include_keywords = include

    def filter(self, job: Job_Listing) -> bool:
        return  self._is_included(job.html)
    
    def _is_included(self, content: str) -> bool:
        if not self._include_keywords:
            return True
        
        content_norm = self._normalize(content)

        return any(
            re.search(rf"(?<!\w){re.escape(self._normalize(kw))}(?!\w)", content_norm)
            for kw in self._include_keywords
        )