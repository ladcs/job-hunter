"""
tests/unit/models/test_job_listing.py
"""

import pytest
from Models.Job_Listing import Job_Listing, Requirements


class TestRequirements:

    def test_default_values(self):
        req = Requirements()
        assert req.needs == []
        assert req.good_to_have == []
        assert req.seniority is None

    def test_with_values(self):
        req = Requirements(
            needs=["Python", "Git"],
            good_to_have=["Docker"],
            seniority="junior"
        )
        assert "Python" in req.needs
        assert "Docker" in req.good_to_have
        assert req.seniority == "junior"

    def test_needs_and_good_to_have_are_independent(self):
        req = Requirements(needs=["Python"])
        assert req.good_to_have == []


class TestJobListing:

    def test_required_fields(self):
        job = Job_Listing(
            id="123",
            title="Engenheiro de Software",
            location="São Paulo",
            url="https://example.com/job/123",
        )
        assert job.id == "123"
        assert job.title == "Engenheiro de Software"
        assert job.location == "São Paulo"
        assert job.url == "https://example.com/job/123"

    def test_optional_fields_default_to_none(self):
        job = Job_Listing(id="1", title="Dev", location="SP", url="http://x.com")
        assert job.html is None
        assert job.content is None
        assert job.requirements is None

    def test_html_can_be_set(self):
        job = Job_Listing(id="1", title="Dev", location="SP", url="http://x.com")
        job.html = "<div>Conteúdo</div>"
        assert job.html == "<div>Conteúdo</div>"

    def test_content_can_be_set(self):
        job = Job_Listing(id="1", title="Dev", location="SP", url="http://x.com")
        job.content = "Texto limpo da vaga"
        assert job.content == "Texto limpo da vaga"

    def test_requirements_can_be_set(self):
        req = Requirements(needs=["Python"], seniority="junior")
        job = Job_Listing(
            id="1", title="Dev", location="SP", url="http://x.com",
            requirements=req
        )
        assert job.requirements.seniority == "junior"
        assert "Python" in job.requirements.needs

    def test_two_jobs_with_same_id_are_equal(self):
        job1 = Job_Listing(id="1", title="Dev", location="SP", url="http://x.com")
        job2 = Job_Listing(id="1", title="Dev", location="SP", url="http://x.com")
        assert job1 == job2

    def test_two_jobs_with_different_ids_are_not_equal(self):
        job1 = Job_Listing(id="1", title="Dev", location="SP", url="http://x.com")
        job2 = Job_Listing(id="2", title="Dev", location="SP", url="http://x.com")
        assert job1 != job2
