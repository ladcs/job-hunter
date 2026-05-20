from dataclasses import dataclass


@dataclass
class Project_Llm_Firestore:
    title: str
    period: str

    skills: list[str]

    summary: str

    highlights: list[str]