"""
tests/integration/fetchers/test_nubank_integration.py
"""

import pytest
from unittest.mock import MagicMock, patch
from Fetchers.WebSites.Nubank_Config import Nubank_Config
from Fetchers.Job_Fetch import Job_Fetcher


NUBANK_VOLUME_HTML = """
<html><body>
    <a class="job-card" href="?id=1001">
        <div class="chip"><span class="chip__text">Brazil: Sao Paulo</span></div>
        <div class="job-card__text"><p>IT Engineer</p></div>
    </a>
    <a class="job-card" href="?id=1002">
        <div class="chip"><span class="chip__text">Brazil: Sao Paulo</span></div>
        <div class="job-card__text"><p>Senior IT Engineer</p></div>
    </a>
    <a class="job-card" href="?id=1003">
        <div class="chip"><span class="chip__text">Brazil: Sao Paulo</span></div>
        <div class="job-card__text"><p>Lead IT Engineer</p></div>
    </a>
    <a class="job-card" href="?id=1004">
        <div class="chip"><span class="chip__text">Brazil: Sao Paulo</span></div>
        <div class="job-card__text"><p>Staff Software Engineer</p></div>
    </a>
    <a class="job-card" href="?id=1005">
        <div class="chip"><span class="chip__text">Brazil: Sao Paulo</span></div>
        <div class="job-card__text"><p>Junior IT Engineer</p></div>
    </a>
    <a class="job-card" href="?id=1006">
        <div class="chip"><span class="chip__text">Brazil: Sao Paulo</span></div>
        <div class="job-card__text"><p>SOx IT Specialist</p></div>
    </a>
    <a class="job-card" href="?id=1007">
        <div class="chip"><span class="chip__text">Brazil: Sao Paulo</span></div>
        <div class="job-card__text"><p>Security Engineer</p></div>
    </a>
    <a class="job-card" href="?id=1008">
        <div class="chip"><span class="chip__text">Brazil: Sao Paulo</span></div>
        <div class="job-card__text"><p>Mobile Engineering Manager</p></div>
    </a>
    <a class="job-card" href="?id=1009">
        <div class="chip"><span class="chip__text">Brazil: Sao Paulo</span></div>
        <div class="job-card__text"><p>Senior Software Engineer</p></div>
    </a>
    <a class="job-card" href="?id=1010">
        <div class="chip"><span class="chip__text">Brazil: Sao Paulo</span></div>
        <div class="job-card__text"><p>engenheiro de software</p></div>
    </a>
</body></html>
"""


@pytest.mark.integration
class TestNubankSmoke:

    def test_request_succeeds_and_returns_listings(self):
        config = Nubank_Config()
        fetcher = Job_Fetcher(config=config, request_delay=0)
        jobs = fetcher.fetch()

        assert isinstance(jobs, list)
        assert fetcher.raw_count > 0

    def test_all_listings_have_required_fields(self):
        config = Nubank_Config()
        fetcher = Job_Fetcher(config=config, request_delay=0)
        jobs = fetcher.fetch()

        for job in jobs:
            assert job.id
            assert job.title
            assert job.url
            assert "nubank" in job.url.lower()


@pytest.mark.integration
class TestNubankVolume:

    @pytest.fixture
    def mock_response(self):
        response = MagicMock()
        response.raise_for_status.return_value = None
        response.text = NUBANK_VOLUME_HTML
        return response

    def test_raw_count(self, mock_response):
        with patch("Fetchers.Job_Fetch.requests.get", return_value=mock_response):
            with patch("Fetchers.Job_Fetch.time.sleep"):
                fetcher = Job_Fetcher(config=Nubank_Config())
                fetcher.fetch()
        assert fetcher.raw_count == 10

    def test_excluded_senior_lead_staff_sox_security(self, mock_response):
        with patch("Fetchers.Job_Fetch.requests.get", return_value=mock_response):
            with patch("Fetchers.Job_Fetch.time.sleep"):
                fetcher = Job_Fetcher(config=Nubank_Config())
                jobs = fetcher.fetch()

        titles = [j.title for j in jobs]
        assert "Senior IT Engineer" not in titles
        assert "Lead IT Engineer" not in titles
        assert "Staff Software Engineer" not in titles
        assert "SOx IT Specialist" not in titles
        assert "Security Engineer" not in titles

    def test_included_engineer_engenheiro(self, mock_response):
        with patch("Fetchers.Job_Fetch.requests.get", return_value=mock_response):
            with patch("Fetchers.Job_Fetch.time.sleep"):
                fetcher = Job_Fetcher(config=Nubank_Config())
                jobs = fetcher.fetch()

        titles = [j.title for j in jobs]
        assert "IT Engineer" in titles
        assert "Junior IT Engineer" in titles
        assert "engenheiro de software" in titles

    def test_filtered_count_is_correct(self, mock_response):
        with patch("Fetchers.Job_Fetch.requests.get", return_value=mock_response):
            with patch("Fetchers.Job_Fetch.time.sleep"):
                fetcher = Job_Fetcher(config=Nubank_Config())
                fetcher.fetch()
        # passa: IT Engineer, Junior IT Engineer, engenheiro de software
        assert fetcher.filtered_count == 3
