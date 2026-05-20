import logging

from Ia_generative.api.Ai_model.Ai_config import Ai_Config

logger = logging.getLogger(__name__)


class Request_LLM:
    def __init__(self, Ai_config: Ai_Config):
        self._Ai_config = Ai_config
    
    def model_request(self) -> str:
        client = self._Ai_config.client()
        args = self._Ai_config.args
        response = client.responses.create(**args)
        logger.info(
            "Tokens usados | input=%s output=%s total=%s",
            response.usage.input_tokens,
            response.usage.output_tokens,
            response.usage.total_tokens
        )
        output = response.output_text.strip()

        logger.debug(output)
        return output
        