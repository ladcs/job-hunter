from Ia_generative.api.Ai_model.Request_LLM import Ai_Config
from openai import OpenAI
from core.config import OPENAI_API_KEY

class Job_Requirement_Extractor_Config(Ai_Config):
    def __init__(self, content: str, title: str):
        super().__init__(prompt = f"""
You are a job requirements extraction assistant.

Your task is to extract technical skills from a job posting and assign an importance weight to each skill.

Return ONLY valid JSON in the following format:

{{
  "needs": [
    {{
      "skill": "string",
      "weight": 1-5
    }}
  ]
}}

Rules:
- Return ONLY valid JSON
- Do NOT explain anything
- Do NOT return any text outside the JSON
- All skill names must be lowercase
- Do NOT duplicate skills
- Extract only concrete technical skills
- Extract only the most relevant technical skills
- Ignore soft skills
- Ignore generic terms unless technically relevant
- Do not infer technologies that are not clearly mentioned
- Do not use external knowledge
- Return a raw JSON object.
- Do NOT wrap the JSON in quotes.
- Do NOT escape quotes.

Examples of valid skills:
- python
- java
- c#
- fastapi
- django
- spring
- react
- aws
- gcp
- postgresql

Weight meaning:
1 = optional or nice-to-have skill
2 = skill mentioned as a qualification or secondary requirement
3 = skill mentioned in responsibilities or daily activities
4 = important mandatory requirement
5 = primary/core technology directly defining the role identity, usually present in the title

Important constraints:
- Do NOT infer technologies that are not explicitly mentioned
- "API development" does NOT mean "fastapi"
- Avoid over-interpreting
- Only include technologies explicitly stated or strongly implied

Job title:
'''
{title}
''''

Job content:
'''
{content}
'''
""".strip())

    @property
    def model(self) -> str:
        return "gpt-4.1-mini"
    
    @property
    def reasoning(self) -> str:
        return None
    
    @property
    def temperature(self) -> float:
        return 0.4
    
    @property
    def max_tokens(self) -> int:
        return 1000
    
    @property
    def args(self) -> dict:
        return {
            "input": self.prompt,
            "model": self.model,
            "max_output_tokens": self.max_tokens,
            "temperature": self.temperature,
        }
    
    def client(self):
        return OpenAI(api_key=OPENAI_API_KEY)