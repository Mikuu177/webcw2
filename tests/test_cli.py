from pathlib import Path

from src.crawler import Page
from src.indexer import InvertedIndex
import src.main as main_module
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
    assert "TF-IDF" in shell.execute("rank")
    assert "Please provide" in shell.execute("find")
    assert "Unknown command" in shell.execute("dance")


def test_shell_requires_index_before_search(tmp_path):
    shell = SearchShell(index_path=tmp_path / "missing.json")

    assert "Run build or load first" in shell.execute("find good")
    assert "Run build or load first" in shell.execute("print good")
    assert "Run build first" in shell.execute("load")


def test_shell_build_help_exit_and_empty_command(tmp_path, monkeypatch):
    class FakeCrawler:
        def crawl(self):
            return [Page("https://example.test/1", "One", "Good friends")]

    monkeypatch.setattr(main_module, "Crawler", FakeCrawler)
    shell = SearchShell(index_path=tmp_path / "index.json")

    assert "Please enter a command" in shell.execute("")
    assert "Commands:" in shell.execute("help")
    assert "Built index for 1 page" in shell.execute("build")
    assert "Goodbye" in shell.execute("exit")
    assert (tmp_path / "index.json").exists()


def test_shell_print_rejects_empty_word(tmp_path):
    index_path = tmp_path / "index.json"
    index = InvertedIndex()
    index.build([Page("https://example.test/1", "One", "Good friends")])
    index.save(index_path)
    shell = SearchShell(index_path=index_path)

    shell.execute("load")

    assert "Please provide a word" in shell.execute("print")
