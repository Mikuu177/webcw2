from src.crawler import Crawler


class FakeResponse:
    def __init__(self, text: str):
        self.text = text

    def raise_for_status(self):
        return None


class FakeSession:
    def __init__(self, pages):
        self.pages = pages
        self.headers = {}
        self.requested = []

    def get(self, url, timeout):
        self.requested.append((url, timeout))
        return FakeResponse(self.pages[url])


def test_crawler_follows_next_link_and_extracts_quote_text():
    pages = {
        "https://quotes.toscrape.com/": """
            <html><head><title>Quotes</title></head><body>
            <div class="quote"><span class="text">Good friends matter.</span></div>
            <li class="next"><a href="/page/2/">Next</a></li>
            </body></html>
        """,
        "https://quotes.toscrape.com/page/2/": """
            <html><head><title>Quotes 2</title></head><body>
            <div class="quote"><span class="text">Indifference is expensive.</span></div>
            </body></html>
        """,
    }
    sleeps = []
    crawler = Crawler(session=FakeSession(pages), sleeper=sleeps.append)

    result = crawler.crawl()

    assert len(result) == 2
    assert result[0].url == "https://quotes.toscrape.com/"
    assert "Good friends" in result[0].text
    assert result[1].url == "https://quotes.toscrape.com/page/2/"
    assert sleeps == [6.0]


def test_crawler_handles_request_errors_gracefully():
    class BrokenSession:
        headers = {}

        def get(self, url, timeout):
            raise RuntimeError("network unavailable")

    crawler = Crawler(session=BrokenSession())

    assert crawler.crawl() == []
