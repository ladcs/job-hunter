
import json
import logging
import re
from pprint import pprint

from Models.Job_Listing import SkillRequirement

logger = logging.getLogger(__name__)

class ParseResponseLLM:
    def _parse_requirements(self, raw: str) -> SkillRequirement | None:
        try:
            clean = self._sanitize_json(raw)
            data = json.loads(clean)

            if not isinstance(data.get("needs"), list):
                raise ValueError("needs inválido")

            requeriments = [SkillRequirement(**skill) for skill in data["needs"]]

            return requeriments

        except Exception as e:
            logger.error("Erro ao parsear/validar LLM: %s | raw=%s", str(e), raw)
            return None
        
    def _sanitize_json(self, raw: str) -> str:
        # remove ```json
        raw = re.sub(r"```json", "", raw, flags=re.IGNORECASE)

        # remove ```
        raw = re.sub(r"```", "", raw)

        # remove trailing commas
        raw = re.sub(r",\s*}", "}", raw)
        raw = re.sub(r",\s*]", "]", raw)

        return raw.strip()