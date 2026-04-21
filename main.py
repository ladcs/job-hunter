from Fetchers.WebSites.Nubank_Config import Nubank_Config
from Fetchers.Job_Fetch import Job_Fetcher

fetcher = Job_Fetcher(config=Nubank_Config())
jobs = fetcher.fetch()

print(f"Total na listagem : {fetcher.raw_count}")
print(f"Após filtro       : {fetcher.filtered_count}\n")

for job in jobs:
    print(f"[{job.id}] {job.title}")
    print(f"         {job.location}")
    print(f"         {job.url}\n")