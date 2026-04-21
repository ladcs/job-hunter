from requests import Response
from Models.Job_Listing import Job_Listing

class Get_Greenhouse:
    def parse_listings(self, response: Response) -> list[Job_Listing]:
        data = response.json()
        listings: list[Job_Listing] = []

        for job in data.get("jobs", []):
            job_id = str(job.get("id", ""))
            title = job.get("title", "")
            location = job.get("location", {}).get("name", "")
            job_url = job.get("absolute_url", "")
            job_html = job.get("content", "")

            listings.append(Job_Listing(
                id=job_id,
                title=title,
                location=location,
                url=job_url,
                html=job_html,
            ))

        return listings