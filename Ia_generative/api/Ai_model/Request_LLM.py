import logging
from pprint import pprint

from Ia_generative.api.Ai_model.Ai_config import Ai_Config

logger = logging.getLogger(__name__)


class Request_LLM:
    def __init__(self, Ai_config: Ai_Config):
        self._Ai_config = Ai_config
    
    def model_request(self) -> str:
        client = self._Ai_config.client()
        args = self._Ai_config.args
        response = client.responses.create(**args)
        print("LLM response:", response.output_text)  # Log the raw response for debugging
        print("LLM tokens used:", response.usage)  # Log token usage for insight into model behavior

        return response.output_text.strip()
        