from Models.cvs_to_llm import Cv_To_Llm

from Jobs.Job_Saver import Job_Saver

from Ia_generative.api.Ai_model.Ai_config import Ai_Config
from Ia_generative.api.Ai_model.Request_LLM import Request_LLM

from Models.Personal_Project import Personal_Project

class User_Resume:
    def __init__(self, get_resume: Ai_Config, job_saver: Job_Saver):
        self.__get_resume = get_resume
        self.__job_saver = job_saver

    def personal_project_resume_url(self, project_cv: Cv_To_Llm) -> list[Personal_Project]:
            resume = Request_LLM(self.__get_resume).model_request()
            get_url_resume_project = {"resume": resume, "latex": project_cv.project_latex, "url": project_cv.url, "job_id": f"{project_cv.source}-{project_cv.job_id}", "source": project_cv.source}
            self.__job_saver.mark_analized(project_cv.job_id, project_cv.source)
            return Personal_Project(**get_url_resume_project)