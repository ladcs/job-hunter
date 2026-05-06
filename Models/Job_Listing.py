from dataclasses import dataclass, field
from typing import TypedDict

class Priority(TypedDict):
    very_high: list[str]
    high: list[str]
    medium: list[str]
    low: list[str]
    very_low: list[str]

@dataclass
class SkillRequirement:
    skill: str
    type: str
    score: int | None = None
    rank: str | None = None
    mentions: int = 0
    in_requirements_section: bool = False
    appears_in_responsibilities: bool = False
    appears_in_title: bool = False
    explicitly_optional: bool = False

@dataclass
class Requirements:
    needs: list[SkillRequirement] = field(default_factory=list)
    priority: Priority = field(default_factory=lambda: {
        "very_high": [],
        "high": [],
        "medium": [],
        "low": [],
        "very_low": [],
    })

@dataclass
class Job_Listing:
    id: str
    title: str
    location: str
    url: str
    html: str | None = None
    content: str | None = None
    requirements: Requirements | None = None
