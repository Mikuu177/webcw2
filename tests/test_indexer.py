from src.crawler import Page
from src.indexer import InvertedIndex, tokenize


def test_tokenize_is_case_insensitive_and_ignores_punctuation():
    assert tokenize("Good, good! Friends.") == ["good", "good", "friends"]


def test_inverted_index_records_frequency_positions_and_pages(tmp_path):
    index = InvertedIndex()
    page = Page(url="https://example.test/1", title="Example", text="Good friends are good")

    index.add_page(page)

    posting = index.terms["good"][page.url]
    assert posting.frequency == 2
    assert posting.positions == [0, 3]
    assert index.pages[page.url]["token_count"] == 4


def test_index_save_and_load_round_trip(tmp_path):
    path = tmp_path / "index.json"
    index = InvertedIndex()
    index.build(
        [
            Page(url="https://example.test/1", title="One", text="Good friends"),
            Page(url="https://example.test/2", title="Two", text="Good ideas"),
        ]
    )

    index.save(path)
    loaded = InvertedIndex.load(path)

    assert loaded.document_count == 2
    assert loaded.terms["good"]["https://example.test/1"].frequency == 1
    assert loaded.terms["friends"]["https://example.test/1"].positions == [1]
