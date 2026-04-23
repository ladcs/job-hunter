"""
tests/unit/fetchers/test_job_details_fetch.py
"""

import pytest
import requests as req
from unittest.mock import MagicMock, patch
from Fetchers.Job_Details_Fetch import Job_Details_Fetcher
from Fetchers.util.clean_html import HTMLCleaner
from Models.Job_Listing import Job_Listing


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_job(id="1", title="IT Engineer", html=None):
    return Job_Listing(
        id=id, title=title, location="SP",
        url=f"https://example.com/job/{id}",
        html=html,
    )


def make_config(selector=None):
    config = MagicMock()
    config.job_content_selector = selector
    return config


def make_response(text="<div><p>Conteúdo</p></div>"):
    r = MagicMock()
    r.raise_for_status.return_value = None
    r.text = text
    return r


# ---------------------------------------------------------------------------
# _passes_experience_filter
# ---------------------------------------------------------------------------

class TestPassesExperienceFilter:

    @pytest.fixture
    def fetcher(self):
        return Job_Details_Fetcher(config=make_config(), max_years=2)

    def test_passes_when_no_years_mentioned(self, fetcher):
        html = "<p>Buscamos desenvolvedor python com experiência em APIs</p>"
        assert fetcher._passes_experience_filter(html, "Dev") is True

    def test_passes_when_years_within_limit(self, fetcher):
        html = "<p>At least 2 years of experience required</p>"
        assert fetcher._passes_experience_filter(html, "Dev") is True

    def test_passes_when_exactly_at_limit(self, fetcher):
        html = "<p>Mínimo 2 anos de experiência</p>"
        assert fetcher._passes_experience_filter(html, "Dev") is True

    def test_fails_when_years_exceed_limit(self, fetcher):
        html = "<p>At least 4 years of experience in software development</p>"
        assert fetcher._passes_experience_filter(html, "Dev") is False

    def test_fails_when_any_mention_exceeds_limit(self, fetcher):
        # tem 1 ano e 3 anos — o 3 descarta
        html = "<p>1 year preferred. Minimum 3 years required.</p>"
        assert fetcher._passes_experience_filter(html, "Dev") is False

    def test_passes_with_range_starting_within_limit(self, fetcher):
        # "3-5 anos" — pega o 3, descarta
        html = "<p>Desejável 3-5 anos de experiência</p>"
        assert fetcher._passes_experience_filter(html, "Dev") is False

    def test_passes_with_plus_within_limit(self, fetcher):
        html = "<p>2+ years of experience</p>"
        assert fetcher._passes_experience_filter(html, "Dev") is True

    def test_fails_with_plus_exceeding_limit(self, fetcher):
        html = "<p>3+ years of experience managing SaaS</p>"
        assert fetcher._passes_experience_filter(html, "Dev") is False

    def test_portuguese_minimum_pattern(self, fetcher):
        html = "<p>No mínimo 3 anos de experiência em desenvolvimento</p>"
        assert fetcher._passes_experience_filter(html, "Dev") is False

    def test_portuguese_comprovada_pattern(self, fetcher):
        html = "<p>Experiência comprovada de 10+ anos em projetos de TI</p>"
        assert fetcher._passes_experience_filter(html, "Dev") is False

    def test_custom_max_years(self):
        fetcher = Job_Details_Fetcher(config=make_config(), max_years=4)
        html = "<p>At least 4 years of experience</p>"
        assert fetcher._passes_experience_filter(html, "Dev") is True

    # --- intervalos pt-br ---

    def test_range_1_3_anos_passes(self, fetcher):
        html = "<p>1-3 anos de experiência em desenvolvimento</p>"
        assert fetcher._passes_experience_filter(html, "Dev") is True

    def test_range_2_5_anos_passes(self, fetcher):
        html = "<p>2-5 anos de experiência em suporte</p>"
        assert fetcher._passes_experience_filter(html, "Dev") is True

    def test_range_3_6_anos_fails(self, fetcher):
        html = "<p>3-6 anos de experiência em projetos</p>"
        assert fetcher._passes_experience_filter(html, "Dev") is False

    # --- intervalos inglês ---

    def test_range_1_3_years_passes(self, fetcher):
        html = "<p>1-3 years of experience required</p>"
        assert fetcher._passes_experience_filter(html, "Dev") is True

    def test_range_2_5_years_passes(self, fetcher):
        html = "<p>2-5 years of experience in SaaS</p>"
        assert fetcher._passes_experience_filter(html, "Dev") is True

    def test_range_3_6_years_fails(self, fetcher):
        html = "<p>3-6 years of experience managing teams</p>"
        assert fetcher._passes_experience_filter(html, "Dev") is False

    # --- intervalos com prefixo ---

    def test_between_2_5_years_passes(self, fetcher):
        html = "<p>between 2-5 years of experience preferred</p>"
        assert fetcher._passes_experience_filter(html, "Dev") is True

    def test_between_3_6_years_fails(self, fetcher):
        html = "<p>between 3-6 years of experience required</p>"
        assert fetcher._passes_experience_filter(html, "Dev") is False


# ---------------------------------------------------------------------------
# enrich — filtro integrado
# ---------------------------------------------------------------------------

class TestEnrichWithExperienceFilter:

    def test_discards_job_exceeding_years(self):
        job = make_job(html="<p>At least 4 years of experience required</p>")
        fetcher = Job_Details_Fetcher(config=make_config(), max_years=2)

        with patch("Fetchers.Job_Details_Fetch.time.sleep"):
            result = fetcher.enrich([job])

        assert result == []

    def test_keeps_job_within_years(self):
        job = make_job(html="<p>2 years of experience. Python and Git.</p>")
        fetcher = Job_Details_Fetcher(config=make_config(), max_years=2)

        with patch("Fetchers.Job_Details_Fetch.time.sleep"):
            result = fetcher.enrich([job])

        assert len(result) == 1
        assert result[0].content is not None

    def test_keeps_job_with_no_years_mentioned(self):
        job = make_job(html="<p>Buscamos desenvolvedor com experiência em Python</p>")
        fetcher = Job_Details_Fetcher(config=make_config(), max_years=2)

        with patch("Fetchers.Job_Details_Fetch.time.sleep"):
            result = fetcher.enrich([job])

        assert len(result) == 1

    def test_mixed_list_keeps_only_qualifying(self):
        jobs = [
            make_job("1", html="<p>Junior dev, sem requisito de anos</p>"),
            make_job("2", html="<p>At least 4 years of experience required</p>"),
            make_job("3", html="<p>Mínimo 2 anos de experiência</p>"),
            make_job("4", html="<p>Minimum 5 years required</p>"),
        ]
        fetcher = Job_Details_Fetcher(config=make_config(), max_years=2)

        with patch("Fetchers.Job_Details_Fetch.time.sleep"):
            result = fetcher.enrich(jobs)

        assert len(result) == 2
        ids = [j.id for j in result]
        assert "1" in ids
        assert "3" in ids
        assert "2" not in ids
        assert "4" not in ids

    def test_skips_fetch_when_html_populated_and_applies_filter(self):
        job = make_job(html="<p>At least 5 years required</p>")
        fetcher = Job_Details_Fetcher(config=make_config(), max_years=2)

        with patch("Fetchers.Job_Details_Fetch.requests.get") as mock_get:
            with patch("Fetchers.Job_Details_Fetch.time.sleep"):
                result = fetcher.enrich([job])

        mock_get.assert_not_called()
        assert result == []


# ---------------------------------------------------------------------------
# retry
# ---------------------------------------------------------------------------

class TestRetry:

    def test_retries_on_failure_and_succeeds(self):
        job = make_job(html=None)
        fetcher = Job_Details_Fetcher(config=make_config(), request_delay=0, max_years=2)

        fail = MagicMock()
        fail.raise_for_status.side_effect = req.RequestException("timeout")
        success = make_response("<p>2 years of experience</p>")

        with patch("Fetchers.Job_Details_Fetch.requests.get",
                   side_effect=[fail, fail, success]):
            with patch("Fetchers.Job_Details_Fetch.time.sleep"):
                result = fetcher.enrich([job])

        assert len(result) == 1

    def test_gives_up_after_max_retries(self):
        job = make_job(html=None)
        fetcher = Job_Details_Fetcher(config=make_config(), request_delay=0, max_years=2)

        fail = MagicMock()
        fail.raise_for_status.side_effect = req.RequestException("erro")

        with patch("Fetchers.Job_Details_Fetch.requests.get", return_value=fail):
            with patch("Fetchers.Job_Details_Fetch.time.sleep"):
                result = fetcher.enrich([job])

        assert result == []

    def test_max_retries_count(self):
        job = make_job(html=None)
        fetcher = Job_Details_Fetcher(config=make_config(), request_delay=0, max_years=2)

        fail = MagicMock()
        fail.raise_for_status.side_effect = req.RequestException("erro")

        with patch("Fetchers.Job_Details_Fetch.requests.get", return_value=fail) as mock_get:
            with patch("Fetchers.Job_Details_Fetch.time.sleep"):
                fetcher.enrich([job])

        assert mock_get.call_count == 5

    def test_continues_to_next_after_failure(self):
        job_fail = make_job("1", html=None)
        job_ok = make_job("2", html="<p>Junior dev sem requisito</p>")
        fetcher = Job_Details_Fetcher(config=make_config(), request_delay=0, max_years=2)

        fail = MagicMock()
        fail.raise_for_status.side_effect = req.RequestException("erro")

        with patch("Fetchers.Job_Details_Fetch.requests.get", return_value=fail):
            with patch("Fetchers.Job_Details_Fetch.time.sleep"):
                result = fetcher.enrich([job_fail, job_ok])

        assert len(result) == 1
        assert result[0].id == "2"


# ---------------------------------------------------------------------------
# injeção de dependência
# ---------------------------------------------------------------------------

class TestDependencyInjection:

    def test_uses_injected_cleaner(self):
        job = make_job(html="<div><p>Python e Git, 1 year experience</p></div>")
        mock_cleaner = MagicMock(spec=HTMLCleaner)
        mock_cleaner.extract_job_content.return_value = "conteúdo limpo"

        fetcher = Job_Details_Fetcher(
            config=make_config(), cleaner=mock_cleaner, max_years=2
        )

        with patch("Fetchers.Job_Details_Fetch.time.sleep"):
            result = fetcher.enrich([job])

        mock_cleaner.extract_job_content.assert_called_once_with(job.html)
        assert result[0].content == "conteúdo limpo"

    def test_creates_cleaner_from_config_when_not_injected(self):
        config = make_config(selector=["div.job-content"])
        fetcher = Job_Details_Fetcher(config=config)
        assert fetcher._cleaner.selectors == ["div.job-content"]
