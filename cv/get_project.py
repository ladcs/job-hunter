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

from Models.Personal_Project import Personal_Project

json_path_to_cv = "projects/projects.json"

from Models.Job_Listing import SkillRequirement

class Used_Skill:
    def __init__(self, job_saver: Job_Saver):
        self.__job_saver = job_saver
        pass
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
            if len(to_llm) == 0:
                self.__job_saver.mark_analized(job.id, job.source)
                continue
            
            project_cv.append(Cv_To_Llm(project_latex=latex, content=job.content, url=job.url, title=job.title, project_to_llm=to_llm, job_id=job.id, source=job.source))
        
        return project_cv