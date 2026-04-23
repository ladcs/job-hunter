"""
tests/integration/fetchers/test_b3_integration.py
"""

import pytest
from unittest.mock import MagicMock, patch
from Fetchers.WebSites.B3_Config import B3_Config
from Fetchers.Job_Fetch import Job_Fetcher


B3_VOLUME_HTML = """
<html><body>
    <ul>
        <li><a href="/job/SP-Analista-Automacao-Junior/1001/">Analista de Automação Júnior</a></li>
        <li><a href="/job/SP-Software-Engineer/1002/">Software Engineer</a></li>
        <li><a href="/job/SP-Senior-Software-Engineer/1003/">Senior Software Engineer</a></li>
        <li><a href="/job/SP-Lead-Developer/1004/">Lead Developer</a></li>
        <li><a href="/job/SP-Analista-Dados-Pleno/1005/">Analista de Dados Pleno</a></li>
        <li><a href="/job/SP-Diretor-Tecnologia/1006/">Diretor de Tecnologia</a></li>
        <li><a href="/job/SP-QA-Engineer/1007/">QA Engineer</a></li>
        <li><a href="/job/SP-Manager-Engenharia/1008/">Manager de Engenharia</a></li>
        <li><a href="/job/SP-Analista-Tecnologia/1009/">Analista de Tecnologia</a></li>
        <li><a href="/job/SP-Principal-Engineer/1010/">Principal Engineer</a></li>
    </ul>
</body></html>
"""


@pytest.mark.integration
class TestB3Smoke:

    def test_request_succeeds_and_returns_listings(self):
        config = B3_Config()
        fetcher = Job_Fetcher(config=config, request_delay=0)
        jobs = fetcher.fetch()

        assert isinstance(jobs, list)
        assert fetcher.raw_count > 0

    def test_all_listings_have_required_fields(self):
        config = B3_Config()
        fetcher = Job_Fetcher(config=config, request_delay=0)
        jobs = fetcher.fetch()

        for job in jobs:
            assert job.id
            assert job.title
            assert job.url
            assert "b3.com.br" in job.url


@pytest.mark.integration
class TestB3Volume:

    @pytest.fixture
    def mock_response(self):
        response = MagicMock()
        response.raise_for_status.return_value = None
        response.text = B3_VOLUME_HTML
        return response

    def test_raw_count(self, mock_response):
        with patch("Fetchers.Job_Fetch.requests.get", return_value=mock_response):
            with patch("Fetchers.Job_Fetch.time.sleep"):
                fetcher = Job_Fetcher(config=B3_Config())
                fetcher.fetch()
        assert fetcher.raw_count == 10

    def test_excluded_senior_lead_diretor_manager_principal(self, mock_response):
        with patch("Fetchers.Job_Fetch.requests.get", return_value=mock_response):
            with patch("Fetchers.Job_Fetch.time.sleep"):
                fetcher = Job_Fetcher(config=B3_Config())
                jobs = fetcher.fetch()

        titles = [j.title for j in jobs]
        assert "Senior Software Engineer" not in titles
        assert "Lead Developer" not in titles
        assert "Diretor de Tecnologia" not in titles
        assert "Manager de Engenharia" not in titles
        assert "Principal Engineer" not in titles

    def test_included_software_dados_qa_tecnologia(self, mock_response):
        with patch("Fetchers.Job_Fetch.requests.get", return_value=mock_response):
            with patch("Fetchers.Job_Fetch.time.sleep"):
                fetcher = Job_Fetcher(config=B3_Config())
                jobs = fetcher.fetch()

        titles = [j.title for j in jobs]
        assert "Software Engineer" in titles
        assert "Analista de Dados Pleno" in titles
        assert "QA Engineer" not in titles
        assert "Analista de Tecnologia" in titles

    def test_filtered_count_is_correct(self, mock_response):
        with patch("Fetchers.Job_Fetch.requests.get", return_value=mock_response):
            with patch("Fetchers.Job_Fetch.time.sleep"):
                fetcher = Job_Fetcher(config=B3_Config())
                fetcher.fetch()
        # passa: Automação Jr, Software Engineer, Dados Pleno, QA Engineer, Tecnologia
        assert fetcher.filtered_count == 4

    def test_url_prepends_base_url_for_relative_paths(self, mock_response):
        with patch("Fetchers.Job_Fetch.requests.get", return_value=mock_response):
            with patch("Fetchers.Job_Fetch.time.sleep"):
                fetcher = Job_Fetcher(config=B3_Config())
                jobs = fetcher.fetch()

        for job in jobs:
            assert job.url.startswith("https://vagas.b3.com.br")
