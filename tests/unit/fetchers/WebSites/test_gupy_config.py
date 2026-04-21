"""
tests/unit/fetchers/test_gupy_config.py
"""

import pytest
from unittest.mock import MagicMock
from Fetchers.WebSites.Gupy_Config import Gupy_Portal_Config


GUPY_JSON = {
    "data": [
        {
            "id": 2001,
            "name": "Engenheiro de Software",
            "city": "São Paulo",
            "state": "SP",
            "jobUrl": "https://portal.gupy.io/job/2001",
            "description": "<p>Vaga para engenheiro</p>",
        },
        {
            "id": 2002,
            "name": "Desenvolvedor Python",
            "city": "Campinas",
            "state": "SP",
            "jobUrl": "https://portal.gupy.io/job/2002",
            "description": "<p>Vaga para dev Python</p>",
        },
        {
            "id": 2003,
            "name": "QA Engineer",
            "city": None,
            "state": None,
            "jobUrl": "https://portal.gupy.io/job/2003",
            "description": "",
        },
    ]
}


@pytest.fixture
def config():
    return Gupy_Portal_Config()


@pytest.fixture
def config_with_term():
    return Gupy_Portal_Config(term="python")


@pytest.fixture
def mock_response():
    response = MagicMock()
    response.json.return_value = GUPY_JSON
    return response


# ---------------------------------------------------------------------------
# Propriedades
# ---------------------------------------------------------------------------

class TestGupyPortalConfigProperties:

    def test_default_term_is_software(self, config):
        assert "software" in config.url.lower()

    def test_custom_term_in_url(self, config_with_term):
        assert "python" in config_with_term.url.lower()

    def test_url_contains_gupy_endpoint(self, config):
        assert "employability-portal.gupy.io" in config.url

    def test_url_contains_sao_paulo_state(self, config):
        assert "S%C3%A3o%20Paulo" in config.url or "São Paulo" in config.url

    def test_url_contains_limit(self, config):
        assert "limit=50" in config.url

    def test_job_content_selector_is_none(self, config):
        assert config.job_content_selector is None

    def test_exclude_keywords_not_empty(self, config):
        assert len(config.exclude_keywords) > 0

    def test_include_keywords_not_empty(self, config):
        assert len(config.include_keywords) > 0

    def test_base_job_url(self, config):
        assert config.base_job_url == "https://portal.gupy.io/job-search"


# ---------------------------------------------------------------------------
# parse_listings
# ---------------------------------------------------------------------------

class TestGupyPortalConfigParseListings:

    def test_parses_correct_number(self, config, mock_response):
        listings = config.parse_listings(mock_response)
        assert len(listings) == 3

    def test_parses_id_as_string(self, config, mock_response):
        listings = config.parse_listings(mock_response)
        assert listings[0].id == "2001"

    def test_parses_title(self, config, mock_response):
        listings = config.parse_listings(mock_response)
        assert listings[0].title == "Engenheiro de Software"

    def test_parses_location_with_city_and_state(self, config, mock_response):
        listings = config.parse_listings(mock_response)
        assert "São Paulo" in listings[0].location
        assert "SP" in listings[0].location

    def test_parses_location_as_remoto_when_none(self, config, mock_response):
        listings = config.parse_listings(mock_response)
        assert listings[2].location == "Remoto"

    def test_parses_url(self, config, mock_response):
        listings = config.parse_listings(mock_response)
        assert listings[0].url == "https://portal.gupy.io/job/2001"

    def test_parses_html_from_description(self, config, mock_response):
        listings = config.parse_listings(mock_response)
        assert listings[0].html == "<p>Vaga para engenheiro</p>"

    def test_empty_description_stored_as_empty_string(self, config, mock_response):
        listings = config.parse_listings(mock_response)
        assert listings[2].html == ""

    def test_empty_data_returns_empty_list(self, config):
        response = MagicMock()
        response.json.return_value = {"data": []}
        assert config.parse_listings(response) == []

    def test_missing_data_key_returns_empty_list(self, config):
        response = MagicMock()
        response.json.return_value = {}
        assert config.parse_listings(response) == []

    def test_term_spaces_encoded_in_url(self):
        config = Gupy_Portal_Config(term="engenheiro software")
        assert " " not in config.url
