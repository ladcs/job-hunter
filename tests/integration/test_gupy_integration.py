"""
tests/integration/fetchers/test_gupy_integration.py
"""

import pytest
from unittest.mock import MagicMock, patch
from Fetchers.WebSites.Gupy_Config import Gupy_Portal_Config
from Fetchers.Job_Fetch import Job_Fetcher


GUPY_VOLUME_JSON = {
    "data": [
        {"id": 1, "name": "Engenheiro de Software Jr", "city": "São Paulo", "state": "SP", "jobUrl": "https://gupy.io/job/1", "description": "<p>Vaga 1</p>"},
        {"id": 2, "name": "Senior Engenheiro de Software", "city": "São Paulo", "state": "SP", "jobUrl": "https://gupy.io/job/2", "description": "<p>Vaga 2</p>"},
        {"id": 3, "name": "Desenvolvedor Python", "city": "Campinas", "state": "SP", "jobUrl": "https://gupy.io/job/3", "description": "<p>Vaga 3</p>"},
        {"id": 4, "name": "Lead Developer", "city": "São Paulo", "state": "SP", "jobUrl": "https://gupy.io/job/4", "description": "<p>Vaga 4</p>"},
        {"id": 5, "name": "QA Engineer", "city": None, "state": None, "jobUrl": "https://gupy.io/job/5", "description": "<p>Vaga 5</p>"},
        {"id": 6, "name": "Staff Engineer", "city": "São Paulo", "state": "SP", "jobUrl": "https://gupy.io/job/6", "description": "<p>Vaga 6</p>"},
        {"id": 7, "name": "Coordenador de TI", "city": "São Paulo", "state": "SP", "jobUrl": "https://gupy.io/job/7", "description": "<p>Vaga 7</p>"},
        {"id": 8, "name": "Desenvolvedora Frontend", "city": "São Paulo", "state": "SP", "jobUrl": "https://gupy.io/job/8", "description": "<p>Vaga 8</p>"},
        {"id": 9, "name": "Analista de Automação", "city": "São Paulo", "state": "SP", "jobUrl": "https://gupy.io/job/9", "description": "<p>Vaga 9</p>"},
        {"id": 10, "name": "Vaga Afirmativa Desenvolvedor", "city": "São Paulo", "state": "SP", "jobUrl": "https://gupy.io/job/10", "description": "<p>Vaga 10</p>"},
    ]
}


@pytest.mark.integration
class TestGupySmoke:

    def test_request_succeeds_and_returns_listings(self):
        config = Gupy_Portal_Config(term="engenheiro software")
        fetcher = Job_Fetcher(config=config, request_delay=0)
        jobs = fetcher.fetch()

        assert isinstance(jobs, list)
        assert fetcher.raw_count > 0

    def test_all_listings_have_required_fields(self):
        config = Gupy_Portal_Config(term="engenheiro software")
        fetcher = Job_Fetcher(config=config, request_delay=0)
        jobs = fetcher.fetch()

        for job in jobs:
            assert job.id
            assert job.title
            assert job.url


@pytest.mark.integration
class TestGupyVolume:

    @pytest.fixture
    def mock_response(self):
        response = MagicMock()
        response.raise_for_status.return_value = None
        response.json.return_value = GUPY_VOLUME_JSON
        return response

    def test_raw_count(self, mock_response):
        with patch("Fetchers.Job_Fetch.requests.get", return_value=mock_response):
            with patch("Fetchers.Job_Fetch.time.sleep"):
                fetcher = Job_Fetcher(config=Gupy_Portal_Config())
                fetcher.fetch()
        assert fetcher.raw_count == 10

    def test_excluded_senior_lead_staff_coordenador_afirmativa(self, mock_response):
        with patch("Fetchers.Job_Fetch.requests.get", return_value=mock_response):
            with patch("Fetchers.Job_Fetch.time.sleep"):
                fetcher = Job_Fetcher(config=Gupy_Portal_Config())
                jobs = fetcher.fetch()

        titles = [j.title for j in jobs]
        assert "Senior Engenheiro de Software" not in titles
        assert "Lead Developer" not in titles
        assert "Staff Engineer" not in titles
        assert "Coordenador de TI" not in titles
        assert "Vaga Afirmativa Desenvolvedor" not in titles

    def test_included_engenheiro_desenvolvedor_qa(self, mock_response):
        with patch("Fetchers.Job_Fetch.requests.get", return_value=mock_response):
            with patch("Fetchers.Job_Fetch.time.sleep"):
                fetcher = Job_Fetcher(config=Gupy_Portal_Config())
                jobs = fetcher.fetch()

        titles = [j.title for j in jobs]
        assert "Engenheiro de Software Jr" in titles
        assert "Desenvolvedor Python" in titles
        assert "QA Engineer" not in titles
        assert "Desenvolvedora Frontend" in titles

    def test_filtered_count_is_correct(self, mock_response):
        with patch("Fetchers.Job_Fetch.requests.get", return_value=mock_response):
            with patch("Fetchers.Job_Fetch.time.sleep"):
                fetcher = Job_Fetcher(config=Gupy_Portal_Config())
                fetcher.fetch()
        # passa: Engenheiro Jr, Desenvolvedor Python, QA Engineer, Desenvolvedora Frontend, Analista de Automação (não tem keyword)
        assert fetcher.filtered_count == 4

