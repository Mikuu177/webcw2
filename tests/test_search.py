from src.crawler import Page
from src.indexer import InvertedIndex
from src.search import SearchEngine


def make_index():
    index = InvertedIndex()
    index.build(
        [
            Page("https://example.test/1", "One", "Good friends are good"),
            Page("https://example.test/2", "Two", "Good ideas matter"),
            Page("https://example.test/3", "Three", "Indifference is costly"),
        ]
    )
    return index


def test_print_existing_word_shows_frequency_and_positions():
    output = SearchEngine(make_index()).print_term("GOOD")

    assert "Inverted index for 'good'" in output
    assert "frequency=2" in output
    assert "positions=[0, 3]" in output


def test_find_multi_word_query_returns_intersection_sorted_by_score():
    results = SearchEngine(make_index()).find("good friends")

    assert [result.url for result in results] == ["https://example.test/1"]
    assert results[0].score > 0


def test_tfidf_ranking_prefers_higher_term_frequency():
    results = SearchEngine(make_index()).find("good")

    assert [result.url for result in results][:2] == [
        "https://example.test/1",
        "https://example.test/2",
    ]


def test_find_formats_empty_and_unknown_query_gracefully():
    engine = SearchEngine(make_index())

    assert "Please provide" in engine.format_find("")
    assert "No pages found" in engine.format_find("frendz")
    assert "Did you mean 'friends'" in engine.format_find("frendz")


def test_ranking_explanation_mentions_tfidf():
    assert "TF-IDF" in SearchEngine(make_index()).explain_ranking()
