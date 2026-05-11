from pathlib import Path

from src.crawler import Page
from src.indexer import InvertedIndex
from src.main import SearchShell


def test_shell_load_print_find_and_edge_cases(tmp_path):
    index_path = tmp_path / "index.json"
    index = InvertedIndex()
    index.build([Page("https://example.test/1", "One", "Good friends")])
    index.save(index_path)
    shell = SearchShell(index_path=Path(index_path))

    assert "Loaded index" in shell.execute("load")
    assert "frequency=1" in shell.execute("print good")
    assert "Found 1 page" in shell.execute("find good friends")
    assert "Please provide" in shell.execute("find")
    assert "Unknown command" in shell.execute("dance")


def test_shell_requires_index_before_search(tmp_path):
    shell = SearchShell(index_path=tmp_path / "missing.json")

    assert "Run build or load first" in shell.execute("find good")
    assert "Run build or load first" in shell.execute("print good")
    assert "Run build first" in shell.execute("load")
