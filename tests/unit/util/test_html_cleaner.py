"""
tests/test_html_cleaner.py

Testes unitários para HTMLCleaner.
Nenhuma requisição de rede — tudo com HTML/texto fixo.
"""

import pytest
from Fetchers.util.clean_html import HTMLCleaner


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def cleaner():
    """HTMLCleaner sem seletores — usa o HTML inteiro."""
    return HTMLCleaner()


@pytest.fixture
def cleaner_with_selector():
    """HTMLCleaner com seletor específico."""
    return HTMLCleaner(selectors=["div.job-content"])


# ---------------------------------------------------------------------------
# remove_emojis
# ---------------------------------------------------------------------------

class TestRemoveEmojis:

    def test_remove_common_emojis(self, cleaner):
        result = cleaner.remove_emojis("Vaga para engenheiro 🚀🎯")
        assert result == "Vaga para engenheiro "

    def test_text_without_emojis_unchanged(self, cleaner):
        text = "Vaga para engenheiro de software"
        assert cleaner.remove_emojis(text) == text

    def test_only_emojis_returns_empty(self, cleaner):
        result = cleaner.remove_emojis("🚀🎯🔗")
        assert result.strip() == ""

    def test_emoji_between_words(self, cleaner):
        result = cleaner.remove_emojis("Python 🐍 developer")
        assert "Python" in result
        assert "developer" in result


# ---------------------------------------------------------------------------
# clean_html
# ---------------------------------------------------------------------------

class TestCleanHtml:

    def test_removes_script_tags(self, cleaner):
        from bs4 import BeautifulSoup
        html = "<div>Conteúdo<script>alert('xss')</script></div>"
        soup = BeautifulSoup(html, "html.parser")
        result = cleaner.clean_html(soup)
        assert "alert" not in result
        assert "Conteúdo" in result

    def test_removes_style_tags(self, cleaner):
        from bs4 import BeautifulSoup
        html = "<div>Texto<style>.btn { color: red }</style></div>"
        soup = BeautifulSoup(html, "html.parser")
        result = cleaner.clean_html(soup)
        assert "color" not in result
        assert "Texto" in result

    def test_removes_svg_tags(self, cleaner):
        from bs4 import BeautifulSoup
        html = "<div>Título<svg><path d='M0 0'/></svg></div>"
        soup = BeautifulSoup(html, "html.parser")
        result = cleaner.clean_html(soup)
        assert "<svg>" not in result
        assert "Título" in result

    def test_removes_anchor_tags(self, cleaner):
        from bs4 import BeautifulSoup
        html = "<div>Veja <a href='http://example.com'>aqui</a></div>"
        soup = BeautifulSoup(html, "html.parser")
        result = cleaner.clean_html(soup)
        assert "href" not in result

    def test_collapses_multiple_newlines(self, cleaner):
        from bs4 import BeautifulSoup
        html = "<div><p>Linha 1</p><p>Linha 2</p><p>Linha 3</p></div>"
        soup = BeautifulSoup(html, "html.parser")
        result = cleaner.clean_html(soup)
        assert "\n\n" not in result

    def test_collapses_extra_spaces(self, cleaner):
        from bs4 import BeautifulSoup
        html = "<div>Texto   com    espaços   extras</div>"
        soup = BeautifulSoup(html, "html.parser")
        result = cleaner.clean_html(soup)
        assert "  " not in result

    def test_plain_text_preserved(self, cleaner):
        from bs4 import BeautifulSoup
        html = "<div><h3>Requisitos</h3><p>Python, Git, REST API</p></div>"
        soup = BeautifulSoup(html, "html.parser")
        result = cleaner.clean_html(soup)
        assert "Requisitos" in result
        assert "Python" in result
        assert "Git" in result


# ---------------------------------------------------------------------------
# extract_job_content
# ---------------------------------------------------------------------------

class TestExtractJobContent:

    def test_extracts_with_selector(self, cleaner_with_selector):
        html = """
        <html>
            <header>Header irrelevante</header>
            <div class="job-content">
                <h3>Sobre a vaga</h3>
                <p>Buscamos engenheiro de software</p>
            </div>
            <footer>Footer irrelevante</footer>
        </html>
        """
        result = cleaner_with_selector.extract_job_content(html)
        assert "Sobre a vaga" in result
        assert "engenheiro de software" in result
        assert "Header irrelevante" not in result
        assert "Footer irrelevante" not in result

    def test_falls_back_to_full_html_when_selector_not_found(self, cleaner_with_selector):
        html = "<div class='other'><p>Conteúdo</p></div>"
        result = cleaner_with_selector.extract_job_content(html)
        assert "Conteúdo" in result

    def test_unescapes_html_entities(self, cleaner):
        html = "&lt;p&gt;Engenheiro de Software&lt;/p&gt;"
        result = cleaner.extract_job_content(html)
        assert "Engenheiro de Software" in result
        assert "&lt;" not in result

    def test_no_selector_uses_full_html(self, cleaner):
        html = "<div><p>Requisitos</p><p>Python</p></div>"
        result = cleaner.extract_job_content(html)
        assert "Requisitos" in result
        assert "Python" in result

    def test_removes_emojis_in_pipeline(self, cleaner):
        html = "<div><p>Vaga para dev 🚀</p></div>"
        result = cleaner.extract_job_content(html)
        assert "🚀" not in result
        assert "Vaga para dev" in result

    def test_handles_empty_html(self, cleaner):
        result = cleaner.extract_job_content("")
        assert result == ""

    def test_nbsp_treated_as_space(self, cleaner):
        html = "<p>Experiência&nbsp;com&nbsp;Python</p>"
        result = cleaner.extract_job_content(html)
        assert "Experiência" in result
        assert "Python" in result
