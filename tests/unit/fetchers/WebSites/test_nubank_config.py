"""
tests/unit/fetchers/test_nubank_config.py

Testes unitários para Nubank_Config.
Usa HTML fixo para simular a resposta da página de listagem.
"""

import pytest
from unittest.mock import MagicMock
from Fetchers.WebSites.Nubank_Config import Nubank_Config


# ---------------------------------------------------------------------------
# HTML de listagem simulado — baseado na estrutura real do Nubank
# ---------------------------------------------------------------------------

NUBANK_LISTING_HTML = """
<html>
<body>
    <a class="job-card" href="https://international.nubank.com.br/job-opportunity?id=111">
        <div class="job-card__location">
            <div class="chip">
                <span class="chip__text">Brazil: Sao Paulo</span>
            </div>
        </div>
        <div class="job-card__text"><p>IT Engineer</p></div>
    </a>
    <a class="job-card" href="https://international.nubank.com.br/job-opportunity?id=222">
        <div class="job-card__location">
            <div class="chip">
                <span class="chip__text">Brazil: Sao Paulo</span>
            </div>
        </div>
        <div class="job-card__text"><p>Senior Software Engineer</p></div>
    </a>
    <a class="job-card" href="https://international.nubank.com.br/job-opportunity?id=333">
        <div class="job-card__location">
            <div class="chip">
                <span class="chip__text">Brazil: Sao Paulo</span>
            </div>
        </div>
        <div class="job-card__text"><p>Lead IT Engineer</p></div>
    </a>
    <a class="job-card" href="https://international.nubank.com.br/job-opportunity?id=444">
        <div class="job-card__location">
            <div class="chip">
                <span class="chip__text">Brazil: Sao Paulo</span>
            </div>
        </div>
        <div class="job-card__text"><p>IT Engineer</p></div>
    </a>
</body>
</html>
"""


@pytest.fixture
def config():
    return Nubank_Config()


@pytest.fixture
def mock_response():
    response = MagicMock()
    response.text = NUBANK_LISTING_HTML
    return response


# ---------------------------------------------------------------------------
# Propriedades
# ---------------------------------------------------------------------------

class TestNubankConfigProperties:

    def test_url_is_correct(self, config):
        assert config.url == "https://international.nubank.com.br/careers/brazil/"

    def test_base_job_url_is_correct(self, config):
        assert config.base_job_url == "https://international.nubank.com.br/job-opportunity"

    def test_job_content_selector_returns_list(self, config):
        assert isinstance(config.job_content_selector, list)
        assert len(config.job_content_selector) > 0

    def test_exclude_keywords_not_empty(self, config):
        assert len(config.exclude_keywords) > 0

    def test_include_keywords_not_empty(self, config):
        assert len(config.include_keywords) > 0


# ---------------------------------------------------------------------------
# parse_listings
# ---------------------------------------------------------------------------

class TestNubankConfigParseListings:

    def test_parses_correct_number_of_listings(self, config, mock_response):
        # HTML tem 4 cards mas 2 com id duplicado (111 e 444 são diferentes, ok)
        # id=444 tem título repetido mas id diferente — deve aparecer
        listings = config.parse_listings(mock_response)
        assert len(listings) == 4

    def test_deduplicates_same_id(self, config):
        html = """
        <html><body>
            <a class="job-card" href="?id=999">
                <div class="chip"><span class="chip__text">Brazil: SP</span></div>
                <div class="job-card__text"><p>IT Engineer</p></div>
            </a>
            <a class="job-card" href="?id=999">
                <div class="chip"><span class="chip__text">Brazil: SP</span></div>
                <div class="job-card__text"><p>IT Engineer</p></div>
            </a>
        </body></html>
        """
        response = MagicMock()
        response.text = html
        listings = config.parse_listings(response)
        assert len(listings) == 1

    def test_listing_has_correct_id(self, config, mock_response):
        listings = config.parse_listings(mock_response)
        ids = [j.id for j in listings]
        assert "111" in ids
        assert "222" in ids

    def test_listing_has_correct_title(self, config, mock_response):
        listings = config.parse_listings(mock_response)
        titles = [j.title for j in listings]
        assert "IT Engineer" in titles
        assert "Senior Software Engineer" in titles

    def test_listing_url_contains_base_url(self, config, mock_response):
        listings = config.parse_listings(mock_response)
        for job in listings:
            assert config.base_job_url in job.url

    def test_listing_url_contains_job_id(self, config, mock_response):
        listings = config.parse_listings(mock_response)
        job = next(j for j in listings if j.id == "111")
        assert "111" in job.url

    def test_empty_html_returns_empty_list(self, config):
        response = MagicMock()
        response.text = "<html><body></body></html>"
        listings = config.parse_listings(response)
        assert listings == []
