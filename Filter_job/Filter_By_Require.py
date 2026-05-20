"""
filteer_by_skills.py: módulo para filtrar vagas por habilidades dando check.
"""
from db.firestore.Skills_Firestore import Skills_Firestore
from db.firestore.Jobs_firestore import Jobs_Firestore

from Models.Job_Firestore import Job_Firestore, SkillRequirement
from Models.Skill_Firestore import Skill_Firestore

class Filter_By_Require:    
    def __init__(self, jobs_firestore: Jobs_Firestore, skills_firestore: Skills_Firestore):
        self.__jobs_firestore = jobs_firestore
        self.__skills_firestore = skills_firestore

    def _calculate_total_score(self, job_skills: list[SkillRequirement]) -> int:
        """
        Calcula uma pontuação total para a vaga com base nas habilidades listadas
        e suas respectivas prioridades.
        Atribui pesos diferentes para cada nível de prioridade.
        """
        total_score = 0
        for skill in job_skills:
            total_score += skill.weight / 5
        return total_score

    def _calculate_user_score_for_skill(self, user_skill: Skill_Firestore) -> int:
        """
        Calcula uma pontuação para a habilidade do usuário com base em seus atributos.
        Atribui pesos para nível, anos desde última utilização e confiança.
        """
        level_weight = user_skill.level / 5 * 0.8
        confidence_weight = user_skill.confidence / 100  * 0.2
        recencia = max(0, 1 - user_skill.last_used_years / 3) * 0.2
        
        return level_weight + recencia + confidence_weight

    def _calculate_user_score_for_job(self, user_skills: Skill_Firestore, weigth: int) -> int:
        """
        Calcula uma pontuação total para o usuário em relação a uma vaga específica.
        Compara as habilidades do usuário com as habilidades exigidas pela vaga,
        levando em consideração a prioridade de cada habilidade na vaga.
        """
        return self._calculate_user_score_for_skill(user_skills) * weigth

    def _calculate_user_score_in_job(
        self,
        job_skills: list[SkillRequirement],
        user_skills: list[Skill_Firestore],
    ) -> float:
        total_score = 0.0

        # index por nome normalizado
        user_skill_by_name = {
            skill.name_normalize: skill
            for skill in user_skills
        }

        # categorias do usuário
        user_categories = {
            skill.category
            for skill in user_skills
            if getattr(skill, "category", None)
        }

        for job_skill in job_skills:

            # match exato
            user_skill = user_skill_by_name.get(job_skill.skill)

            if user_skill:
                total_score += self._calculate_user_score_for_job(
                    user_skill,
                    job_skill.weight
                )
                continue

            # match por categoria
            if (
                job_skill.category
                and job_skill.category in user_categories
            ):
                total_score += job_skill.weight * 0.7

        return total_score

    def _valid_job(self, job: Job_Firestore, user_skills: list[Skill_Firestore]) -> bool:
        """
        Verifica se uma vaga é válida para o usuário com base em suas habilidades.
        Define um limiar mínimo de pontuação para considerar a vaga como válida.
        Retorna True se a pontuação do usuário para a vaga for maior ou igual ao limiar, caso contrário, False.
        """
        job_skills = [
            SkillRequirement(**skill)
            for skill in job.requirements
        ]
        total = self._calculate_total_score(job_skills)
        user_score = self._calculate_user_score_in_job(job_skills, user_skills)
        threshold = total * 0.6
        return user_score >= threshold

    def is_valid_jobs_for_user(self, user_id: str) -> list[Job_Firestore]:
        """
        Filtra as vagas disponíveis para um usuário específico com base em suas habilidades.
        Carrega as habilidades do usuário e as vagas disponíveis, e retorna uma lista de vagas válidas para o usuário.
        """
        jobs = self.__jobs_firestore.get_pending_analysis()
        jobs = [Job_Firestore(**job) for job in jobs]
        user_skills = self.__skills_firestore.load_skills_by_user_id(user_id)

        for job in jobs:
            if not self._valid_job(job, user_skills):
                self.__jobs_firestore.mark_analyzed(job.id, job.source)
                job.is_analyzed = True
        return [job for job in jobs if not job.is_analyzed]
    