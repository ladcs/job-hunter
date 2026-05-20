from dataclasses import dataclass


@dataclass
class Project_To_Llm:
    id: str
    title: str
    period: str

    skills: list[str]

    summary: str

    highlights: list[str]