import re
import json

from typing import List

from Models.Job_Listing import SkillRequirement
from Models.cvs_to_llm import Cv_To_Llm

from Models.Job_Firestore import Job_Firestore
from Models.Project_Llm_Firestore import Project_Llm_Firestore
from db.firestore.Projects_llm import Projects_to_Llm
from db.firestore.firestore_client import Firestore_Client

from Jobs.Job_Saver import Job_Saver

from Ia_generative.api.Ai_model.OpenAI.Cv_Resume_Extractor import Cv_Resume_extractor
from Ia_generative.api.Ai_model.Request_LLM import Request_LLM

from Models.Personal_Project import Personal_Project

json_path_to_cv = "projects/projects.json"

from Models.Job_Listing import SkillRequirement

class Used_Skill:
    def get_text(self, skills: List[SkillRequirement]) -> list[str]:
        with open(json_path_to_cv, 'r') as f:
            skills_used = json.load(f)
        
        to_cv = list()

        for skill in skills:
            category_name = ""
            skill_name = skill.skill.lower().strip()
            if skill.category:
                category_name = skill.category.lower().strip()

            if skill_name in skills_used:
                to_cv.extend(
                    skills_used[skill_name]
                )

            elif category_name and category_name in skills_used:
                to_cv.extend(
                    skills_used[category_name]
                )
        
        return list(set(to_cv))
    
    def get_project_to_llm(self, text: str, db: Projects_to_Llm) -> Project_Llm_Firestore:
        match = re.search(r'\\textbf\{([^}]*)\}', text)
        if match:
            content = match.group(1)
        else:
            return
        return db.get_by_title(content)
    

    def get_project(self, jobs: list[Job_Firestore]) -> list[Cv_To_Llm]:
        project_cv = []
        client = Firestore_Client()
        db = Projects_to_Llm(client)
        for job in jobs:
            requires = [SkillRequirement(**req) for req in job.requirements]
            latex = self.get_text(requires)
            to_llm = list()
            
            for l in latex:
                to_llm.append(self.get_project_to_llm(l, db))
            project_cv.append(Cv_To_Llm(project_latex=latex, content=job.content, url=job.url, title=job.title, project_to_llm=to_llm, job_id=job.id, source=job.source))
        return project_cv
    
    def personal_project_resume_url(self, project_cv: list[Cv_To_Llm], job_saver: Job_Saver) -> list[Personal_Project]:
        out_project_cv = []
        for job in project_cv:
            if job.project_to_llm is []:
                if job.source != "nubank":
                    job_saver.mark_analized(job.job_id, job.source)
                    continue
            resume = Cv_Resume_extractor(job.content, job.title, job.project_to_llm)
            resume = Request_LLM(resume).model_request()
            get_url_resume_project = {"resume": resume, "latex": job.project_latex, "url": job.url, "job_id": f"{job.source}-{job.job_id}"}
            job_saver.mark_analized(job.job_id, job.source)
            out_project_cv.append(Personal_Project(**get_url_resume_project))
        
        return out_project_cv