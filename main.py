import json
from pprint import pprint

from Fetchers.WebSites.Nubank_Config import Nubank_Config
from Fetchers.WebSites.Btg_Config import BTGPactual_Config
from Fetchers.WebSites.B3_Config import B3_Config
from Fetchers.WebSites.Gupy_Config import Gupy_Portal_Config
from Fetchers.WebSites.xpinc import XP_Config

from Fetchers.Job_Fetch import Job_Fetcher
from Fetchers.Job_Details_Fetch import Job_Details_Fetcher

config=B3_Config()
# config=Gupy_Portal_Config('python')


fetcher = Job_Fetcher(config=config)
jobs = fetcher.fetch()

detail_fetcher = Job_Details_Fetcher(config=config)
jobs = detail_fetcher.enrich(jobs)

with open("job_b3.json", "w", encoding="utf-8") as f:
    json.dump(
        [job.__dict__ for job in jobs],
        f,
        ensure_ascii=False,
        indent=2,
        default=lambda o: o.__dict__  # 👈 resolve seu problema
    )