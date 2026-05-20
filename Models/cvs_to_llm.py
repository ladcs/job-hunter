
from dataclasses import dataclass

@dataclass
class Cv_To_Llm:
    content: str
    project_latex: list[str]
    title: str
    project_to_llm: list[str]
    url: str
    source: str
    job_id: str