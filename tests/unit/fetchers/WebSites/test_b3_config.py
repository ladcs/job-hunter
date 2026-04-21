"""
tests/unit/fetchers/test_b3_config.py
"""

import pytest
from unittest.mock import MagicMock
from Fetchers.WebSites.B3_Config import B3_Config


B3_LISTING_HTML = """
<html>
<body>
    <ul>
        <li>
            <a href="/job/Sao-Paulo-Analista-de-Automacao-Junior/1111111/">
                Analista de Automação Júnior
            </a>
        </li>
        <li>
            <a href="/job/Sao-Paulo-Software-Engineer/2222222/">
                Software Engineer
            </a>
        </li>
        <li>
            <a href="/job/Sao-Paulo-Senior-Engineer/3333333/">
                Senior Engineer
            </a>
        </li>
        <li>
            <a href="https://external.com/job/outros/4444444/">
                Tecnologia Pleno
            </a>
        </li>
    </ul>
</body>
</html>
"""

B3_LISTING_HTML_DUPLICATES = """
<html>
<body>
    <ul>
        <li>
            <a href="/job/Sao-Paulo-Software-Engineer/9999999/">
                Software Engineer
            </a>
        </li>
        <li>
            <a href="/job/Sao-Paulo-Software-Engineer/9999999/">
                Software Engineer
            </a>
        </li>
    </ul>
</body>
</html>
"""


@pytest.fixture
def config():
    return B3_Config()


@pytest.fixture
def mock_response():
    response = MagicMock()
    response.text = B3_LISTING_HTML
    return response


# ---------------------------------------------------------------------------
# Propriedades
# ---------------------------------------------------------------------------

class TestB3ConfigProperties:

    def test_url_is_correct(self, config):
        assert config.url == "https://vagas.b3.com.br/go/todas-vagas/4559419/"

    def test_base_job_url(self, config):
        assert config.base_job_url == "https://vagas.b3.com.br"

    def test_job_content_selector_returns_list(self, config):
        assert isinstance(config.job_content_selector, list)
        assert "div.jobDisplay" in config.job_content_selector

    def test_exclude_keywords_not_empty(self, config):
        assert len(config.exclude_keywords) > 0

    def test_include_keywords_not_empty(self, config):
        assert len(config.include_keywords) > 0


# ---------------------------------------------------------------------------
# parse_listings
# ---------------------------------------------------------------------------

class TestB3ConfigParseListings:

    def test_parses_correct_number(self, config, mock_response):
        listings = config.parse_listings(mock_response)
        assert len(listings) == 4

    def test_extracts_id_from_url(self, config, mock_response):
        listings = config.parse_listings(mock_response)
        ids = [j.id for j in listings]
        assert "1111111" in ids
        assert "2222222" in ids

    def test_extracts_title(self, config, mock_response):
        listings = config.parse_listings(mock_response)
        titles = [j.title for j in listings]
        assert "Software Engineer" in titles

    def test_location_is_sao_paulo(self, config, mock_response):
        listings = config.parse_listings(mock_response)
        for job in listings:
            assert job.location == "São Paulo"

    def test_relative_url_gets_base_prepended(self, config, mock_response):
        listings = config.parse_listings(mock_response)
        job = next(j for j in listings if j.id == "1111111")
        assert job.url.startswith("https://vagas.b3.com.br")

    def test_absolute_url_kept_as_is(self, config, mock_response):
        listings = config.parse_listings(mock_response)
        job = next(j for j in listings if j.id == "4444444")
        assert job.url == "https://external.com/job/outros/4444444/"

    def test_deduplicates_same_id(self, config):
        response = MagicMock()
        response.text = B3_LISTING_HTML_DUPLICATES
        listings = config.parse_listings(response)
        assert len(listings) == 1

    def test_empty_html_returns_empty_list(self, config):
        response = MagicMock()
        response.text = "<html><body><ul></ul></body></html>"
        listings = config.parse_listings(response)
        assert listings == []

    def test_skips_links_without_href(self, config):
        response = MagicMock()
        response.text = """
        <html><body><ul>
            <li><a href="">Vaga sem href</a></li>
            <li><a href="/job/SP-Engineer/5555555/">Engineer</a></li>
        </ul></body></html>
        """
        listings = config.parse_listings(response)
        assert len(listings) == 1
        assert listings[0].id == "5555555"
