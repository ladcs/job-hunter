from dataclasses import asdict
from glob import glob
import json
import logging
import pprint
from datetime import datetime, timezone

from Fetchers.WebSites.Nubank_Config import Nubank_Config
from Fetchers.WebSites.Btg_Config import BTGPactual_Config
from Fetchers.WebSites.B3_Config import B3_Config
from Fetchers.WebSites.Gupy_Config import Gupy_Portal_Config
from Fetchers.WebSites.Xpinc_Config import XP_Config

from Fetchers.Job_Fetch import Job_Fetcher
from Fetchers.Job_Details_Fetch import Job_Details_Fetcher
from Fetchers.job_saver import Job_Saver
from Models.Job_Listing import Job_Listing, Requirements, SkillRequirement
from Models.Job_Firestore import Job_Firestore
from db.firestore.Jobs_firestore import Jobs_Firestore
from db.firestore.firestore_client import Firestore_Client
from Ia_generative.api.Ai_model.Request_LLM import Request_LLM
from Ia_generative.api.Ai_model.OpenAI.Job_Requirement_extractor import Job_Requirement_Extractor_Config
from Models.Skill_Firestore import Skill_Firestore
from db.firestore.Skills_Firestore import Skills_Firestore


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

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
db = Jobs_Firestore(client)
saver = Job_Saver(db)


def run():
    for source_name, config in SOURCES:

        # 1. busca e filtra por keywords no título
        jobs = Job_Fetcher(config=config).fetch()

        if not jobs:
            continue

        # 2. elimina vagas já processadas anteriormente
        jobs = saver.filter_new(jobs, source=source_name)
        if not jobs:
            continue

        # 3. busca detalhes, filtra por anos de exp e extrai requisitos via LLM
        jobs = Job_Details_Fetcher(config=config).enrich(jobs)

        if not jobs:
            continue
        
        # 4. salva no Firestore
        saver.save(jobs, source=source_name)

if __name__ == "__main__":
    print("----start------")
    begin = datetime.now(timezone.utc)
    # run()

    # files = list(glob("data/jobs/2026-04-22_job_b3.json"))

    # for file in files:
    #     jobs0 = []
    #     jobs1 = []
    #     with open(file, "r") as f:
    #         data = json.load(f)
    #         source = "b3"
    #         id = data[0].get("id", "unknown") if data else "unknown"
    #         for d in data:
    #             req = d.pop("requirements", None)
    #             d.pop("source", None)
    #             is_analyzed = d.pop("is_analyzed", None)
    #             job = Job_Listing(**d)
    #             jobs0.append(job)

    #     job_details = Job_Details_Fetcher(config=None)
    #     jobs = job_details.enrich(jobs0)
    #     saver = Job_Saver(db)
    #     print(source)
    #     saver.save(jobs, source=source)
    #     break

    # skills = Skill_Firestore(skill_name="Mensageria", level=3, last_used_years=0, confidence=85)
    # user_skills = Skills_Firestore(client)
    # user_id = user_skills.save_new_user("Luciano Augusto de Castro Silva")
    # user_id = user_skills.load_user_id_by_name("Luciano Augusto de Castro Silva")
    # user_skills.save_new_skill_batch(user_id, skills)

    # user_id = '8df773c725cf427e9c074fa72605e943'
    # user_skills.save_new_skill(user_id, skill)
    # loaded_skills = [asdict(s) for s in user_skills.load_skills_by_user_id(user_id)]
    # # user_skills.delete_skill(user_id, skill.skill_name)

    end = datetime.now(timezone.utc)
    duration = (end - begin).total_seconds()

    print(f"----end------ \nDuration: {duration:.2f} seconds")

    pass
    