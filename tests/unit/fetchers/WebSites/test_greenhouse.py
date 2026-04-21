"""
tests/unit/fetchers/test_greenhouse.py

Testes unitários para Get_Greenhouse e Greenhouse_Config.
Usa JSON fixo para simular a resposta da API.
"""

import pytest
from unittest.mock import MagicMock
from Fetchers.WebSites.Greenhouse.Get_greenhouse import Get_Greenhouse
from Fetchers.WebSites.Greenhouse.Greenhouse_config import Greenhouse_Config
from Fetchers.WebSites.Btg_Config import BTGPactual_Config


# ---------------------------------------------------------------------------
# JSON simulado — baseado na estrutura real da API Greenhouse
# ---------------------------------------------------------------------------

GREENHOUSE_JSON = {
    "jobs": [
        {
            "id": 1001,
            "title": "Software Engineer",
            "location": {"name": "São Paulo, Brazil"},
            "absolute_url": "https://boards.greenhouse.io/company/jobs/1001",
            "content": "<p>Descrição da vaga</p>",
        },
        {
            "id": 1002,
            "title": "Senior Software Engineer",
            "location": {"name": "São Paulo, Brazil"},
            "absolute_url": "https://boards.greenhouse.io/company/jobs/1002",
            "content": "<p>Vaga sênior</p>",
        },
        {
            "id": 1003,
            "title": "Data Analyst",
            "location": {"name": "Remote"},
            "absolute_url": "https://boards.greenhouse.io/company/jobs/1003",
            "content": "",
        },
    ]
}


@pytest.fixture
def mock_response():
    response = MagicMock()
    response.json.return_value = GREENHOUSE_JSON
    return response


# ---------------------------------------------------------------------------
# Get_Greenhouse
# ---------------------------------------------------------------------------

class TestGetGreenhouse:

    def test_parses_all_jobs(self, mock_response):
        parser = Get_Greenhouse()
        listings = parser.parse_listings(mock_response)
        assert len(listings) == 3

    def test_parses_id_as_string(self, mock_response):
        parser = Get_Greenhouse()
        listings = parser.parse_listings(mock_response)
        assert listings[0].id == "1001"

    def test_parses_title(self, mock_response):
        parser = Get_Greenhouse()
        listings = parser.parse_listings(mock_response)
        assert listings[0].title == "Software Engineer"

    def test_parses_location(self, mock_response):
        parser = Get_Greenhouse()
        listings = parser.parse_listings(mock_response)
        assert listings[0].location == "São Paulo, Brazil"

    def test_parses_absolute_url(self, mock_response):
        parser = Get_Greenhouse()
        listings = parser.parse_listings(mock_response)
        assert listings[0].url == "https://boards.greenhouse.io/company/jobs/1001"

    def test_parses_html_content(self, mock_response):
        parser = Get_Greenhouse()
        listings = parser.parse_listings(mock_response)
        assert listings[0].html == "<p>Descrição da vaga</p>"

    def test_empty_content_stored_as_empty_string(self, mock_response):
        parser = Get_Greenhouse()
        listings = parser.parse_listings(mock_response)
        assert listings[2].html == ""

    def test_empty_jobs_returns_empty_list(self):
        response = MagicMock()
        response.json.return_value = {"jobs": []}
        parser = Get_Greenhouse()
        assert parser.parse_listings(response) == []

    def test_missing_jobs_key_returns_empty_list(self):
        response = MagicMock()
        response.json.return_value = {}
        parser = Get_Greenhouse()
        assert parser.parse_listings(response) == []


# ---------------------------------------------------------------------------
# Greenhouse_Config (via BTGPactual_Config)
# ---------------------------------------------------------------------------

class TestGreenhouseConfig:

    def test_job_content_selector_is_none(self):
        config = BTGPactual_Config()
        assert config.job_content_selector is None

    def test_parse_listings_delegates_to_get_greenhouse(self, mock_response):
        config = BTGPactual_Config()
        listings = config.parse_listings(mock_response)
        assert len(listings) == 3
        assert listings[0].title == "Software Engineer"

    def test_btg_url_points_to_greenhouse(self):
        config = BTGPactual_Config()
        assert "greenhouse.io" in config.url
        assert "btgpactual" in config.url

    def test_btg_exclude_keywords_not_empty(self):
        config = BTGPactual_Config()
        assert len(config.exclude_keywords) > 0

    def test_btg_include_keywords_not_empty(self):
        config = BTGPactual_Config()
        assert len(config.include_keywords) > 0
