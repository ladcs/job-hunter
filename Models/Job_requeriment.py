from dataclasses import dataclass

@dataclass
class Job_Listing:
    id: str
    title: str
    location: str
    url: str
    content: str
    requeriments: list[str]