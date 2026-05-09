from __future__ import annotations

import logging

from skills.util.categories import SKILL_CATEGORIES
from skills.util.Normalize_skill import Normalize_skill

from Models.Job_Listing import SkillRequirement

logger = logging.getLogger(__name__)

class Enrich:
    def __init__(self, normalize: Normalize_skill):
        self._normalize = normalize

    def enrich_category(self, skill: SkillRequirement):
        try:
            skill.category = SKILL_CATEGORIES[skill.skill]
        except:
            logger.warning(f"não tem a categoria para {skill.skill}")

    def normalize_skill(self, skill: SkillRequirement):
        name = skill.skill
        skill.skill = self._normalize.normalize(name)