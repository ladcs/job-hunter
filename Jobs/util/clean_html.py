from bs4 import BeautifulSoup
import html as html_lib
import re

import emoji

class HTMLCleaner:

    def __init__(self, selectors: list[str] = None):
        self.selectors = selectors

    def _looks_escaped(self, html: str) -> bool:
        return "&lt;" in html or "&gt;" in html or "&amp;" in html

    def remove_emojis(self, text: str) -> str:
        return emoji.replace_emoji(text, replace=" ")

    def clean_html(self, soup: BeautifulSoup) -> str:
        for tag in soup(["script", "style", "noscript", "header", "footer", "svg", "a"]):
            tag.decompose()

        for comment in soup.find_all(string=lambda text: isinstance(text, type(soup.comment))):
            comment.extract()
    
        text = soup.get_text(separator="\n", strip=True)

        text = self.remove_emojis(text)
        text = re.sub(r'\n{2,}', '\n', text)
        text = re.sub(r'[ \t]+', ' ', text)

        return text.strip()
    
    def extract_job_content(self, html:str) -> str:
        if self._looks_escaped(html):
            html = html_lib.unescape(html)
        soup = BeautifulSoup(html, "html.parser")
        selectors = self.selectors
        if selectors:
            for sel in selectors:
                main = soup.select_one(sel)
                if main:
                    return self.clean_html(main)
        return self.clean_html(soup)