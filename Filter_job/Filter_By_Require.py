"""
filteer_by_skills.py: módulo para filtrar vagas por habilidades dando check.
"""
from db.firestore.Skills_Firestore import Skills_Firestore
from db.firestore.Jobs_firestore import Jobs_Firestore

from Models.Job_Listing import Requirements
from Models.Job_Firestore import Job_Firestore
from Models.Skill_Firestore import Skill_Firestore

class Filter_By_Require:
    _weight = {
            "very_high": 5,
            "high": 4,
            "medium": 3,
            "low": 2,
            "very_low": 1,
        }
    
    def __init__(self, jobs_firestore: Jobs_Firestore, skills_firestore: Skills_Firestore, weights: dict = None):
        self.__weight = weights if weights else self._weight
        self.__jobs_firestore = jobs_firestore
        self.__skills_firestore = skills_firestore

    def _calculate_total_score(self, job_skills: Requirements) -> int:
        """
        Calcula uma pontuação total para a vaga com base nas habilidades listadas
        e suas respectivas prioridades.
        Atribui pesos diferentes para cada nível de prioridade.
        """
        weights = self.__weight
        total_score = 0
        skills = job_skills.priority
        for weight_key in weights.keys():
            total_score += len(skills.priority[weight_key]) * weights[weight_key]
        return total_score

    def _calculate_user_score_for_skill(self, user_skill: Skill_Firestore) -> int:
        """
        Calcula uma pontuação para a habilidade do usuário com base em seus atributos.
        Atribui pesos para nível, anos desde última utilização e confiança.
        """
        level_weight = user_skill.level / 5 * 0.6
        confidence_weight = user_skill.confidence / 100  * 0.2
        recencia = max(0, 1 - user_skill.last_used_years / 3) * 0.2
        
        return level_weight + confidence_weight + recencia

    def _calculate_user_score_for_job(self, user_skills: Skill_Firestore, weigth: int) -> int:
        """
        Calcula uma pontuação total para o usuário em relação a uma vaga específica.
        Compara as habilidades do usuário com as habilidades exigidas pela vaga,
        levando em consideração a prioridade de cada habilidade na vaga.
        """
        return self.calculate_user_score_for_skill(user_skills) * weigth

    def _calculate_user_score_in_job(self, job_skills: Requirements, user_skills: list[Skill_Firestore]) -> int:
        """
        Calcula a pontuação total do usuário para uma vaga específica.
        Itera sobre as habilidades exigidas pela vaga e soma as pontuações
        calculadas para cada habilidade do usuário.
        """
        total_score = 0
        for w in self.__weight.keys():
            valid_skills = [s for s in user_skills if s.skill_name in job_skills.priority[w]]
            for skill in valid_skills:
                total_score += self.calculate_user_score_for_job(skill, self.__weight[w])
        return total_score

    def _valid_job(self, job: Job_Firestore, user_skills: list[Skill_Firestore]) -> bool:
        """
        Verifica se uma vaga é válida para o usuário com base em suas habilidades.
        Define um limiar mínimo de pontuação para considerar a vaga como válida.
        Retorna True se a pontuação do usuário para a vaga for maior ou igual ao limiar, caso contrário, False.
        """
        job_skills = Requirements(**job["requirements"])
        total = self.calculate_total_score(job_skills)
        user_score = self.calculate_user_score_in_job(job_skills, user_skills)
        threshold = total * 0.6
        return user_score >= threshold

    def is_valid_jobs_for_user(self, jobs: list[Job_Firestore], user_id: str) -> list[Job_Firestore]:
        """
        Filtra as vagas disponíveis para um usuário específico com base em suas habilidades.
        Carrega as habilidades do usuário e as vagas disponíveis, e retorna uma lista de vagas válidas para o usuário.
        """
        user_skills = self.__skills_firestore.load_skills_by_user_id(user_id)
        for job in jobs:
            if not self._valid_job(job, user_skills):
                self.__jobs_firestore.mark_analyzed(job.id, job.source)
                jobs.remove(job)
        return jobs
    