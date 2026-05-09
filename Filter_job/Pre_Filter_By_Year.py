from __future__ import annotations

import re
import logging

logger = logging.getLogger(__name__)

class Pre_Filter_By_Year:
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

    def __init__(self, max_years: int = MAX_YEARS):
        self._max_years = max_years

    
    def passes_experience_filter(self, html: str, title: str) -> bool:
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