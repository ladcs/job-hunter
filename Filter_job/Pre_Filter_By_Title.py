from Filter_job.Filter_Word_Pre_Llm import Filter_Word_Pre_Llm
from Models.Job_Listing import Job_Listing

from Jobs.Fetch_Config import Fetch_Config

class Pre_Filter_By_Title(Filter_Word_Pre_Llm):
    def __init__(self, config: Fetch_Config):
        super().__init__(config)

    def filter(self, listings: list[Job_Listing]) -> list[Job_Listing]:
        return [
                job for job in listings
                if not self._is_excluded(job.title)
                and self._is_included(job.title)
            ]