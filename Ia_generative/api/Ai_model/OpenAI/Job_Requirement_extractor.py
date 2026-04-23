from Ia_generative.api.Ai_model.Request_LLM import Ai_Config
from openai import OpenAI
from core.config import OPENAI_API_KEY

class Job_Requirement_Extractor_Config(Ai_Config):
    def __init__(self, content: str):
        super().__init__(prompt= f"""You are a job requirements extraction assistant. Given a job posting text, extract the requirements and return only a JSON object with exactly these fields:{"""{"needs": ["list of mandatory requirements — skills, tools, languages, certifications"],"seniority": "one of: junior, pleno, senior, or null if not determinable"}"""}
Rules:
- Extract concrete and specific items only (e.g. "Python", "REST API", "Git", "advanced English")
- Seniority: infer from context (years of experience, role level, responsibilities) even if not explicit
- Return ONLY the JSON object, no markdown, no explanation
- probably the requirements are after "Requeriments", "nice to have", "Requisitos", any words like that, but be prepared for variations and different formats.
job_posting = ```
{content}
```
""".strip())

    @property
    def model(self) -> str:
        return "gpt-4.1-nano"
    
    @property
    def reasoning(self) -> str:
        return None
    
    @property
    def temperature(self) -> float:
        return 0.3
    
    @property
    def max_tokens(self) -> int:
        return 700
    
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