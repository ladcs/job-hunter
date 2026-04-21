from dataclasses import dataclass, field

@dataclass
class Requirements:
    needs: list[str] = field(default_factory=list)
    good_to_have: list[str] = field(default_factory=list)
    seniority: str | None = None

@dataclass
class Job_Listing:
    id: str
    title: str
    location: str
    url: str
    html: str | None = None
    content: str | None = None
    requirements: Requirements | None = None
