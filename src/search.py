"""Search and display helpers for the inverted index."""

from __future__ import annotations

from dataclasses import dataclass

from src.indexer import InvertedIndex, Posting, tokenize


@dataclass(frozen=True)
class SearchResult:
    url: str
    title: str
    score: float
    matched_terms: list[str]


class SearchEngine:
    def __init__(self, index: InvertedIndex):
        self.index = index

    def print_term(self, word: str) -> str:
        tokens = tokenize(word)
        if not tokens:
            return "Please provide a word to print."

        term = tokens[0]
        postings = self.index.terms.get(term)
        if not postings:
            return f"No index entry found for '{term}'."

        lines = [f"Inverted index for '{term}':"]
        for url, posting in sorted(postings.items()):
            lines.append(f"- {url}: frequency={posting.frequency}, positions={posting.positions}")
        return "\n".join(lines)

    def find(self, query: str) -> list[SearchResult]:
        terms = tokenize(query)
        if not terms:
            return []

        page_sets = [set(self.index.terms.get(term, {}).keys()) for term in terms]
        if not page_sets or any(not pages for pages in page_sets):
            return []

        matching_urls = set.intersection(*page_sets)
        results: list[SearchResult] = []
        for url in matching_urls:
            score = sum(self._tf_idf(term, self.index.terms[term][url]) for term in terms)
            page = self.index.pages.get(url, {})
            results.append(
                SearchResult(
                    url=url,
                    title=str(page.get("title", url)),
                    score=round(score, 4),
                    matched_terms=terms,
                )
            )
        return sorted(results, key=lambda result: (-result.score, result.url))

    def explain_ranking(self) -> str:
        return (
            "Ranking uses TF-IDF: term frequency rewards repeated matches on a page, "
            "while inverse document frequency rewards terms that appear on fewer pages."
        )

    def format_find(self, query: str) -> str:
        terms = tokenize(query)
        if not terms:
            return "Please provide at least one search term."

        results = self.find(query)
        if not results:
            suggestion = self.suggest(terms[0])
            suffix = f" Did you mean '{suggestion}'?" if suggestion else ""
            return f"No pages found for '{query}'.{suffix}"

        lines = [f"Found {len(results)} page(s) for '{query}':"]
        for result in results:
            lines.append(f"- score={result.score:.4f} | {result.title} | {result.url}")
        return "\n".join(lines)

    def suggest(self, word: str) -> str | None:
        vocabulary = self.index.terms.keys()
        best: tuple[int, str] | None = None
        for candidate in vocabulary:
            distance = levenshtein(word, candidate)
            if best is None or distance < best[0] or (distance == best[0] and candidate < best[1]):
                best = (distance, candidate)
        if best and best[0] <= 2:
            return best[1]
        return None

    def _tf_idf(self, term: str, posting: Posting) -> float:
        return posting.frequency * self.index.inverse_document_frequency(term)


def levenshtein(left: str, right: str) -> int:
    if left == right:
        return 0
    if not left:
        return len(right)
    if not right:
        return len(left)

    previous = list(range(len(right) + 1))
    for i, left_char in enumerate(left, start=1):
        current = [i]
        for j, right_char in enumerate(right, start=1):
            insertion = current[j - 1] + 1
            deletion = previous[j] + 1
            substitution = previous[j - 1] + (left_char != right_char)
            current.append(min(insertion, deletion, substitution))
        previous = current
    return previous[-1]
