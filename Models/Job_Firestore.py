from dataclasses import dataclass, field
from datetime import datetime, timezone

from Models.Job_Listing import SkillRequirement

@dataclass
class Job_Firestore:
    id: str
    title: str
    location: str
    url: str
    source: str
    is_analyzed: bool = False
    content: str | None = None
    created_at: datetime | None = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = None
    requirements: SkillRequirement | None = None
