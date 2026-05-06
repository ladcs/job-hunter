from pprint import pprint

from Models.Job_Listing import SkillRequirement


class Skills:
    @staticmethod
    def score_skills(required_skills: SkillRequirement) -> int:
        score = 0
        score += min(int(required_skills.mentions), 3)
        score += 5 if required_skills.appears_in_title else 0
        score += 4 if required_skills.appears_in_responsibilities else 0
        score += 3 if required_skills.in_requirements_section else 0
        score -= 1 if required_skills.explicitly_optional else 0
        return score
    
    @staticmethod
    def rank_skills(score: int) -> str:
        if score == 0:
            return "very_low"
        if score < 3:
            return "low"
        if score < 5:
            return "medium"
        if score < 8:
            return "high"
        return "very_high"