from dataclasses import dataclass


@dataclass
class Skill_Firestore:
    skill_name: str
    level: int
    last_used_years: int
    confidence: int