"""
tests/integration/fetchers/test_btg_integration.py
"""

import pytest
from unittest.mock import MagicMock, patch
from Fetchers.WebSites.Btg_Config import BTGPactual_Config
from Fetchers.Job_Fetch import Job_Fetcher


GREENHOUSE_VOLUME_JSON = {
    "jobs": [
        {"id": 1, "title": "Software Engineer", "location": {"name": "São Paulo"}, "absolute_url": "https://btg.com/job/1", "content": "<p>Vaga 1</p>"},
        {"id": 2, "title": "Senior Software Engineer", "location": {"name": "São Paulo"}, "absolute_url": "https://btg.com/job/2", "content": "<p>Vaga 2</p>"},
        {"id": 3, "title": "Lead Software Engineer", "location": {"name": "São Paulo"}, "absolute_url": "https://btg.com/job/3", "content": "<p>Vaga 3</p>"},
        {"id": 4, "title": "Mobile Developer", "location": {"name": "São Paulo"}, "absolute_url": "https://btg.com/job/4", "content": "<p>Vaga 4</p>"},
        {"id": 5, "title": "Flutter Engineer", "location": {"name": "São Paulo"}, "absolute_url": "https://btg.com/job/5", "content": "<p>Vaga 5</p>"},
        {"id": 6, "title": "Angular Developer", "location": {"name": "São Paulo"}, "absolute_url": "https://btg.com/job/6", "content": "<p>Vaga 6</p>"},
        {"id": 7, "title": "Staff Software Engineer", "location": {"name": "São Paulo"}, "absolute_url": "https://btg.com/job/7", "content": "<p>Vaga 7</p>"},
        {"id": 8, "title": "Junior Software Engineer", "location": {"name": "São Paulo"}, "absolute_url": "https://btg.com/job/8", "content": "<p>Vaga 8</p>"},
        {"id": 9, "title": "Coordenador de TI", "location": {"name": "São Paulo"}, "absolute_url": "https://btg.com/job/9", "content": "<p>Vaga 9</p>"},
        {"id": 10, "title": "Analista de Software Pleno", "location": {"name": "São Paulo"}, "absolute_url": "https://btg.com/job/10", "content": "<p>Vaga 10</p>"},
    ]
}


@pytest.mark.integration
class TestBTGSmoke:

    def test_request_succeeds_and_returns_listings(self):
        config = BTGPactual_Config()
        fetcher = Job_Fetcher(config=config, request_delay=0)
        jobs = fetcher.fetch()

        assert isinstance(jobs, list)
        assert fetcher.raw_count > 0

    def test_all_listings_have_required_fields(self):
        config = BTGPactual_Config()
        fetcher = Job_Fetcher(config=config, request_delay=0)
        jobs = fetcher.fetch()

        for job in jobs:
            assert job.id
            assert job.title
            assert job.url
            assert job.html is not None


@pytest.mark.integration
class TestBTGVolume:

    @pytest.fixture
    def mock_response(self):
        response = MagicMock()
        response.raise_for_status.return_value = None
        response.json.return_value = GREENHOUSE_VOLUME_JSON
        return response

    def test_raw_count(self, mock_response):
        with patch("Fetchers.Job_Fetch.requests.get", return_value=mock_response):
            with patch("Fetchers.Job_Fetch.time.sleep"):
                fetcher = Job_Fetcher(config=BTGPactual_Config())
                fetcher.fetch()
        assert fetcher.raw_count == 10

    def test_excluded_senior_lead_mobile_flutter_angular_staff_coordenador(self, mock_response):
        with patch("Fetchers.Job_Fetch.requests.get", return_value=mock_response):
            with patch("Fetchers.Job_Fetch.time.sleep"):
                fetcher = Job_Fetcher(config=BTGPactual_Config())
                jobs = fetcher.fetch()

        titles = [j.title for j in jobs]
        assert "Senior Software Engineer" not in titles
        assert "Lead Software Engineer" not in titles
        assert "Mobile Developer" not in titles
        assert "Flutter Engineer" not in titles
        assert "Angular Developer" not in titles
        assert "Staff Software Engineer" not in titles
        assert "Coordenador de TI" not in titles

    def test_included_software(self, mock_response):
        with patch("Fetchers.Job_Fetch.requests.get", return_value=mock_response):
            with patch("Fetchers.Job_Fetch.time.sleep"):
                fetcher = Job_Fetcher(config=BTGPactual_Config())
                jobs = fetcher.fetch()

        titles = [j.title for j in jobs]
        assert "Software Engineer" in titles
        assert "Junior Software Engineer" in titles

    def test_filtered_count_is_correct(self, mock_response):
        with patch("Fetchers.Job_Fetch.requests.get", return_value=mock_response):
            with patch("Fetchers.Job_Fetch.time.sleep"):
                fetcher = Job_Fetcher(config=BTGPactual_Config())
                fetcher.fetch()
        # passa: Software Engineer, Junior Software Engineer, Analista de Software Pleno
        assert fetcher.filtered_count == 3

    def test_html_populated_from_content(self, mock_response):
        with patch("Fetchers.Job_Fetch.requests.get", return_value=mock_response):
            with patch("Fetchers.Job_Fetch.time.sleep"):
                fetcher = Job_Fetcher(config=BTGPactual_Config())
                jobs = fetcher.fetch()

        for job in jobs:
            assert job.html is not None
