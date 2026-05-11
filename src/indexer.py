"""Inverted index construction and persistence."""

from __future__ import annotations

import json
import math
import re
from dataclasses import asdict, dataclass
from pathlib import Path

from src.crawler import Page

TOKEN_RE = re.compile(r"[a-z0-9']+")


@dataclass
class Posting:
    """Word statistics for one page."""

    frequency: int
    positions: list[int]


def tokenize(text: str) -> list[str]:
    """Return lowercase tokens while ignoring punctuation."""

    return TOKEN_RE.findall(text.lower())


class InvertedIndex:
    """Store word -> page -> statistics mappings."""

    def __init__(self) -> None:
        self.terms: dict[str, dict[str, Posting]] = {}
        self.pages: dict[str, dict[str, str | int]] = {}
        self.document_count = 0

    def add_page(self, page: Page) -> None:
        tokens = tokenize(page.text)
        self.pages[page.url] = {
            "url": page.url,
            "title": page.title,
            "token_count": len(tokens),
            "preview": page.text[:220],
        }
        self.document_count = len(self.pages)

        for position, token in enumerate(tokens):
            page_postings = self.terms.setdefault(token, {})
            posting = page_postings.setdefault(page.url, Posting(frequency=0, positions=[]))
            posting.frequency += 1
            posting.positions.append(position)

    def build(self, pages: list[Page]) -> None:
        for page in pages:
            self.add_page(page)

    def to_dict(self) -> dict:
        return {
            "document_count": self.document_count,
            "pages": self.pages,
            "terms": {
                term: {url: asdict(posting) for url, posting in postings.items()}
                for term, postings in sorted(self.terms.items())
            },
        }

    @classmethod
    def from_dict(cls, payload: dict) -> "InvertedIndex":
        index = cls()
        index.document_count = int(payload.get("document_count", 0))
        index.pages = payload.get("pages", {})
        index.terms = {
            term: {
                url: Posting(frequency=int(stats["frequency"]), positions=list(stats["positions"]))
                for url, stats in postings.items()
            }
            for term, postings in payload.get("terms", {}).items()
        }
        return index

    def save(self, path: str | Path) -> None:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(self.to_dict(), indent=2, sort_keys=True), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "InvertedIndex":
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls.from_dict(payload)

    def inverse_document_frequency(self, term: str) -> float:
        postings = self.terms.get(term, {})
        if not postings or self.document_count == 0:
            return 0.0
        return math.log((1 + self.document_count) / (1 + len(postings))) + 1
