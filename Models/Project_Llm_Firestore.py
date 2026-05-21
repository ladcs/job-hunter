from dataclasses import dataclass


@dataclass
class Project_Llm_Firestore:
    id: str
    title: str
    period: str

    skills: list[str]

    latex: str

    summary: str

    highlights: list[str]