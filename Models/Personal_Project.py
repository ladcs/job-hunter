from dataclasses import dataclass


@dataclass
class Personal_Project:
    url: str
    resume: str
    latex: list[str]
    job_id: str