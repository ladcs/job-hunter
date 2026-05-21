from dataclasses import dataclass

@dataclass
class SkillRequirement:
    skill: str
    category: str | None = None
    weight: int = 1

@dataclass
class Job_Listing:
    id: str
    title: str
    location: str
    url: str
    updated_at: str | None = None
    source: str | None = None
    html: str | None = None
    content: str | None = None
    content_to_llm: str | None = None
    requirements: list[SkillRequirement] | None = None
