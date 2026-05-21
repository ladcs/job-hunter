import re
import json

from typing import List

from Models.Job_Listing import SkillRequirement
from Models.cvs_to_llm import Cv_To_Llm

from Models.Job_Firestore import Job_Firestore
from Models.Project_Llm_Firestore import Project_Llm_Firestore
from db.firestore.Projects_Firestore import Projects_Firestore

from Jobs.Job_Saver import Job_Saver

json_path_to_cv = "projects/projects.json"

from Models.Job_Listing import SkillRequirement

class Get_Project:
    def __init__(self, job_saver: Job_Saver, projects_firestore: Projects_Firestore):
        self.__job_saver = job_saver
        self.__projects_to_llm = projects_firestore

    def get_text(self, skills: List[SkillRequirement]) -> list[str]:
        projects = self.__projects_to_llm.get_all()
        skills_used = {}
        for project in projects:
            for skill in project["skills"]:
                skill_name = skill.lower().strip()
                if skill_name not in skills_used:
                    skills_used[skill_name] = []
                skills_used[skill_name].append(project["latex"])
        
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
    
    def get_project_to_llm(self, text: str) -> Project_Llm_Firestore:
        match = re.search(r'\\textbf\{([^}]*)\}', text)
        if match:
            content = match.group(1)
        else:
            return
        return self.__projects_to_llm.get_by_title(content)
    

    def get_project(self, jobs: list[Job_Firestore]) -> list[Cv_To_Llm]:
        project_cv = []
        for job in jobs:
            requires = [SkillRequirement(**req) for req in job.requirements]
            latex = self.get_text(requires)
            to_llm = list()

            for l in latex:
                to_llm.append(self.get_project_to_llm(l))
            if len(to_llm) == 0:
                self.__job_saver.mark_analized(job.id, job.source)
                continue
            
            project_cv.append(Cv_To_Llm(project_latex=latex, content=job.content, url=job.url, title=job.title, project_to_llm=to_llm, job_id=job.id, source=job.source))
        
        return project_cv