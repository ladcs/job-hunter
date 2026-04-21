from pprint import pprint

import requests

from Fetchers.WebSites.Nubank_Config import Nubank_Config
from Fetchers.WebSites.Btg_Config import BTGPactual_Config
from Fetchers.WebSites.B3_Config import B3_Config
from Fetchers.WebSites.Gupy_Config import Gupy_Portal_Config
from Fetchers.Job_Fetch import Job_Fetcher
from Fetchers.util.clean_html import HTMLCleaner

config=BTGPactual_Config()
# config=Gupy_Portal_Config('python')

fetcher = Job_Fetcher(config=config)
jobs = fetcher.fetch()
cleaner = HTMLCleaner(selectors = config.job_content_selector)
job = jobs[0]
if not job.html:
    res = requests.get(job.url)
    job.html = res.text
job.content = cleaner.extract_job_content(job.html)

# pprint(job)

print(job.content)
# print(job.url)