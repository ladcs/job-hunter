
import json
import logging
import re

from Models.Job_Listing import Requirements

logger = logging.getLogger(__name__)

class ParseResponseLLM:
    def _parse_requirements(self, raw: str) -> Requirements | None:
        try:
            clean = self._sanitize_json(raw)
            data = json.loads(clean)

            if not isinstance(data.get("needs"), list):
                raise ValueError("needs inválido")

            return Requirements(
                needs=data["needs"],
                seniority=data.get("seniority"),
            )

        except Exception as e:
            logger.error("Erro ao parsear/validar LLM: %s | raw=%s", str(e), raw)
            return None
        
    def _sanitize_json(self, raw: str) -> str:
        raw = re.sub(r"```.*?```", "", raw, flags=re.DOTALL)

        # remove trailing commas
        raw = re.sub(r",\s*}", "}", raw)
        raw = re.sub(r",\s*]", "]", raw)

        return raw.strip()