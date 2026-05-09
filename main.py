import logging
from datetime import datetime, timezone

from Jobs.WebSites.Nubank_Config import Nubank_Config
from Jobs.WebSites.Btg_Config import BTGPactual_Config
from Jobs.WebSites.B3_Config import B3_Config
from Jobs.WebSites.Gupy_Config import Gupy_Portal_Config
from Jobs.WebSites.Xpinc_Config import XP_Config

from Filter_job.Filter_by_location import Filter_by_location
from Filter_job.Pre_Filter_By_Title import Pre_Filter_By_Title

from Jobs.Job_Fetch import Job_Fetcher
from Filter_job.Pre_Filter_By_Year import Pre_Filter_By_Year
from Job_listing.Job_Listing_Enrich import Job_Listing_Enrich
from Jobs.Job_Saver import Job_Saver
from db.firestore.Jobs_firestore import Jobs_Firestore
from db.firestore.firestore_client import Firestore_Client

from Filter_job.Filter_by_cotent_word import Filter_By_Content_Word


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
db = Jobs_Firestore(client)
job_db = Job_Saver(db)

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

        jobs = job_db.filter_new(jobs, source_name)
        logger.info(f"{source_name}: Novas vagas: {len(jobs)}")
        if not jobs:
            continue


        jobs = Filter_by_location().filter(jobs)
        filtered_count = len(jobs)
        logger.info(f"{source_name}: {filtered_count} após filtro por local.")
        if not jobs:
            continue

        enrich = Job_Listing_Enrich(config=config)
        try:
            jobs = [job for job in jobs if Pre_Filter_By_Year().passes_experience_filter(job.html, job.title)]
        except Exception as e:
            logger.error(f"Erro ao {str(job.url)} filtrar por anos de experiência: {str(e)}")
        if not jobs:
            continue
        filtered_count = len(jobs)
        logger.info(f"{source_name}: {filtered_count} após filtro por anos de experiência.")
        if not jobs:
            continue
        for job in jobs:
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
            
            job.source = source_name

        logger.info(f"{source_name}: vagas pos filtragem: {len(jobs)}")    

        to_save.extend(jobs)
    job_db.save(to_save)

if __name__ == "__main__":
    print("----start------")
    begin = datetime.now(timezone.utc)
    run()
    end = datetime.now(timezone.utc)
    duration = (end - begin).total_seconds()

    print(f"----end------ \nDuration: {duration:.2f} seconds")

    user_id = "00a713500d1646d88506e234595bdb24"
    