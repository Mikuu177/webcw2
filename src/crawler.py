"""Polite crawler for quotes.toscrape.com."""

from __future__ import annotations

from dataclasses import dataclass
from time import sleep
from typing import Callable
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


DEFAULT_START_URL = "https://quotes.toscrape.com/"
USER_AGENT = "XJCO3011-WebCW2-SearchTool/1.0"


@dataclass(frozen=True)
class Page:
    """A crawled page with text content ready for indexing."""

    url: str
    title: str
    text: str


class Crawler:
    """Crawl quote pages while respecting the required politeness window."""

    def __init__(
        self,
        start_url: str = DEFAULT_START_URL,
        politeness_window: float = 6.0,
        timeout: float = 10.0,
        sleeper: Callable[[float], None] = sleep,
        session: requests.Session | None = None,
    ) -> None:
        self.start_url = start_url
        self.politeness_window = politeness_window
        self.timeout = timeout
        self.sleeper = sleeper
        self.session = session or requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})

    def crawl(self, max_pages: int | None = None) -> list[Page]:
        """Crawl pages by following the site's `next` pagination link."""

        pages: list[Page] = []
        visited: set[str] = set()
        next_url: str | None = self.start_url

        while next_url and next_url not in visited:
            if max_pages is not None and len(pages) >= max_pages:
                break

            if pages:
                self.sleeper(self.politeness_window)

            visited.add(next_url)
            response = self._get(next_url)
            if response is None:
                break

            page, next_url = self._parse_page(next_url, response.text)
            pages.append(page)

        return pages

    def _get(self, url: str) -> requests.Response | None:
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response
        except (requests.RequestException, Exception):
            return None

    def _parse_page(self, url: str, html: str) -> tuple[Page, str | None]:
        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.get_text(strip=True) if soup.title else url
        quote_text = " ".join(q.get_text(" ", strip=True) for q in soup.select(".quote"))
        if not quote_text:
            quote_text = soup.get_text(" ", strip=True)

        next_anchor = soup.select_one("li.next a")
        next_url = urljoin(url, next_anchor["href"]) if next_anchor and next_anchor.get("href") else None
        return Page(url=url, title=title, text=quote_text), next_url
