import logging
from dataclasses import asdict
from datetime import datetime, timezone

import pprint

from Jobs.WebSites.Nubank_Config import Nubank_Config
from Jobs.WebSites.Btg_Config import BTGPactual_Config
from Jobs.WebSites.B3_Config import B3_Config
from Jobs.WebSites.Gupy_Config import Gupy_Portal_Config
from Jobs.WebSites.Xpinc_Config import XP_Config

from Filter_job.Filter_by_location import Filter_by_location
from Filter_job.Pre_Filter_By_Title import Pre_Filter_By_Title

from Filter_job.Filter_By_Require import Filter_By_Require
from Jobs.Job_Fetch import Job_Fetcher
from Filter_job.Pre_Filter_By_Year import Pre_Filter_By_Year
from Job_listing.Job_Listing_Enrich import Job_Listing_Enrich
from Jobs.Job_Saver import Job_Saver
from db.firestore.Projects_Firestore import Projects_Firestore
from db.firestore.Jobs_firestore import Jobs_Firestore
from db.firestore.Skills_Firestore import Skills_Firestore
from db.firestore.firestore_client import Firestore_Client
from Models.Job_Firestore import Job_Firestore
from Models.Personal_Project import Personal_Project

from Filter_job.Filter_by_cotent_word import Filter_By_Content_Word

from cv.Get_Project import Get_Project
from cv.generate_resume import User_Resume
from cv.create_cv import Make_Cv

from Ia_generative.api.Ai_model.OpenAI.Cv_Resume_Extractor import Cv_Resume_extractor
from Ia_generative.api.Ai_model.OpenAI.History_Gupy_Extractor import History_Gupy_Extractor


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

SOURCES = [
    ("nubank", Nubank_Config()),
    ("btg", BTGPactual_Config()),
    ("b3", B3_Config()),
    ("xp", XP_Config()),
    ("gupy", Gupy_Portal_Config("python")),
    ("gupy", Gupy_Portal_Config("backend")),
    ("gupy", Gupy_Portal_Config("back-end")),
    ("gupy", Gupy_Portal_Config("c#")),
]


client = Firestore_Client()
job_db = Jobs_Firestore(client)
job_saver = Job_Saver(job_db)
skill_db = Skills_Firestore(client)
project_db = Projects_Firestore(client)

fetch = Job_Fetcher()

def run():
    to_save = []
    for source_name, config in SOURCES:
        try:
            res = fetch.fetch(config.url)
        except:
            continue
        jobs = config.parse_listings(res)
        row_count = len(jobs)
        jobs = Pre_Filter_By_Title(config).filter(jobs)
        filtered_count = len(jobs)

        logger.info(f"{source_name}: {row_count} vagas encontradas.")
        if not jobs:
            continue

        jobs, not_valid = job_saver.filter_new(jobs, source_name)
        job_saver.delete_jobs(not_valid, source_name)
        logger.info(f"{source_name}: Novas vagas: {len(jobs)}")
        if not jobs:
            continue


        jobs = Filter_by_location().filter(jobs)

        filtered_count = len(jobs)

        logger.info(f"{source_name}: {filtered_count} após filtro por local.")
        if not jobs:
            continue

        enrich = Job_Listing_Enrich(config=config)
        aux = []
        for job in jobs:
            try:
                if not job.html:
                    if Pre_Filter_By_Year().passes_experience_filter(job.content, job.title):
                        aux.append(job)  
                elif Pre_Filter_By_Year().passes_experience_filter(job.html, job.title):
                    aux.append(job)
            except Exception as e:
                logger.error(f"Erro no {source_name}_{job.id} ao filtrar por anos de experiência: {str(e)}")
        if not jobs:
            continue
        filtered_count = len(jobs)
        logger.info(f"{source_name}: {filtered_count} após filtro por anos de experiência.")
        if not jobs:
            continue

        for job in jobs:
            job.source = source_name
            if not job.html:
                
                try:
                    res = fetch.fetch(job.url)
                except:
                    continue

                enrich.html_enrich(job, html=res.text)
            
            if not job.html:
                continue
            
            if source_name.lower() != "nubank":
                valid = Filter_By_Content_Word(config).filter(job)
                if not valid:
                    continue
            
            if not job.content:
                enrich.content_enrich(job)
            
            enrich.content_to_llm_enrich(job)
            
            enrich.requirements_enrich(job)

        logger.info(f"{source_name}: vagas pos filtragem: {len(jobs)}")    

        to_save.extend(jobs)
    job_saver.save(to_save)


def get_valid_jobs(user_id: str) -> list[Job_Firestore]:
    filter = Filter_By_Require(skills_firestore=skill_db, jobs_firestore=job_db)
    jobs = filter.is_valid_jobs_for_user(user_id)
    return jobs

if __name__ == "__main__":
    logger.info("----start------")
    begin = datetime.now(timezone.utc)
    run() # busca novas vagas
    user_id = "00a713500d1646d88506e234595bdb24"
    jobs = get_valid_jobs(user_id) # filtra vagas por requisito

    user_project = Get_Project(job_saver, project_db)
    projects_cv = [p for p in user_project.get_project(jobs)]
    personal_project = []
    for project_cv in projects_cv:
        if project_cv.source != "gupy":
            to_llm = Cv_Resume_extractor(project_cv.content, project_cv.title, project_cv.project_to_llm)
        elif project_cv.source == "gupy":
            to_llm = History_Gupy_Extractor(project_cv.content, project_cv.title, project_cv.project_to_llm)
        user_resume = User_Resume(to_llm, job_saver)
        personal_project.append(user_resume.personal_project_resume_url(project_cv))
    
    to_json = [asdict(pproject) for pproject in personal_project]
    
    # import json
    # with open("test.json", "w") as f:
    #     json.dump(project_cv, f, indent=4)

    
    import json
    with open("test_create_resume.json", "w", encoding="utf-8") as f:
        json.dump(
            to_json,
            f,
            indent=4,
            ensure_ascii=False
        )

    # gupy_11283139

    # test = job_db.get("11283139", "gupy")
    # print(test)

    # get = "test_create_resume.json"

    # with open(get, 'r', encoding='utf-8') as f:
    #     personal_project = json.load(f)

    cv = Make_Cv()
    for pp in personal_project:
        actual_personal_project = Personal_Project(**pp)
        latex_code = cv.generate_latex(actual_personal_project)
        cv.create_zip(latex_code, actual_personal_project.job_id)
    

    end = datetime.now(timezone.utc)
    duration = (end - begin).total_seconds()
    logger.info(f"----end------ \nDuration: {duration:.2f} seconds")

