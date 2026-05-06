from Ia_generative.api.Ai_model.Request_LLM import Ai_Config
from openai import OpenAI
from core.config import OPENAI_API_KEY

class Job_Requirement_Extractor_Config(Ai_Config):
    def __init__(self, content: str, title: str):
        super().__init__(prompt = f"""
You are a job requirements extraction assistant.
Extract technical skills from the job posting and return structured data.
Return ONLY valid JSON in this exact format:
{{
  "needs": [
    {{
      "skill": "string",
      "type": "language | framework | tool | concept | platform",
      "mentions": integer,
      "in_requirements_section": true or false,
      "appears_in_responsibilities": true or false,
      "appears_in_title": true or false,
      "explicitly_optional": true or false
    }}
  ],
}}
Rules:
- Extract skills from both title and content
- Process title and content separately:
  - If a skill appears in the title:
    - set appears_in_title = true
    - add exactly +1 to mentions
  - If the title text is repeated inside the content:
    - do NOT count duplicated occurrences from the title again
- Mentions must reflect unique occurrences across title and content combined
- Extract only concrete technical skills, and technical profile like graduation:
  - programming languages (Python, Java, C#)
  - frameworks (FastAPI, Spring, React)
  - tools (Git, Jira, Postman)
  - platforms (AWS, Azure, GCP)
  - technical concepts (rest api, microservices, ci/cd, oop, solid, dry, clean code, tdd, bdd)
  - methodologies (agile, scrum, kanban, devops)
- Do NOT include soft skills (communication, teamwork, etc.)
- Do NOT include generic phrases (e.g., "experiência prévia", "boa comunicação")
- Normalize skill names:
  - lowercase
  - singular form when possible
  - examples:
    - "REST APIs" → "rest api"
    - "PostgreSQL" → "postgresql"
    - "APIs" → "rest api" (only if clearly referring to REST APIs)
    - "SOLID principles" → "solid"
    - "Orientação a Objetos" → "oop"
    - "Metodologias Ágeis" → "agile"
- Do NOT duplicate skills
- Each skill must appear only once
Field definitions:
- "mentions": approximate number of times the skill appears (estimate is fine)
- "in_requirements_section": true if appears under sections like "Requirements", "Requisitos", "O que esperamos" or text indicates obligation (e.g., "required", "must", "necessário", "conhecimento em")
- "appears_in_responsibilities": true if appears in responsibilities, daily tasks, or job description sections
- "appears_in_title": true if the skill is explicitly mentioned in the job title
- "explicitly_optional": true if mentioned as optional (e.g., "nice to have", "diferencial")
Type classification:
- language: programming languages (python, java, c#)
- framework: frameworks and libraries (fastapi, spring, react)
- tool: tools (git, jira, postman)
- platform: cloud/platforms (aws, azure, gcp, kubernetes)
- concept: technical concepts and principles (rest api, microservices, solid, clean code, tdd)
- methodology: development processes and practices (agile, scrum, kanban, devops)
Important constraints:
- Do NOT infer specific technologies from generic mentions
  - Example: "API development" ≠ "fastapi"
- Only include a technology if it is explicitly mentioned or strongly implied
- Avoid over-interpreting
Ignore:
- Benefits
- Company description
- Marketing text
- UI boilerplate text
Output must be valid JSON only:
- No markdown
- No explanations
- No trailing commas
title: {title}
job_posting:
\"\"\"
{content}
\"\"\"
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