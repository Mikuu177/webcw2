"""Interactive command-line interface for the search engine."""

from __future__ import annotations

from pathlib import Path

from src.crawler import Crawler
from src.indexer import InvertedIndex
from src.search import SearchEngine

DEFAULT_INDEX_PATH = Path("data/index.json")


class SearchShell:
    def __init__(self, index_path: Path = DEFAULT_INDEX_PATH):
        self.index_path = index_path
        self.index: InvertedIndex | None = None

    def execute(self, raw_command: str) -> str:
        command = raw_command.strip()
        if not command:
            return "Please enter a command. Type 'help' for options."

        name, *rest = command.split(maxsplit=1)
        argument = rest[0] if rest else ""

        if name == "build":
            return self.build()
        if name == "load":
            return self.load()
        if name == "print":
            return self.print_word(argument)
        if name == "find":
            return self.find(argument)
        if name == "rank":
            return self.explain_ranking()
        if name == "help":
            return self.help()
        if name == "exit":
            return "Goodbye."
        return f"Unknown command '{name}'. Type 'help' for options."

    def build(self) -> str:
        crawler = Crawler()
        pages = crawler.crawl()
        index = InvertedIndex()
        index.build(pages)
        index.save(self.index_path)
        self.index = index
        return f"Built index for {index.document_count} page(s) and saved to {self.index_path}."

    def load(self) -> str:
        if not self.index_path.exists():
            return f"No saved index found at {self.index_path}. Run build first."
        self.index = InvertedIndex.load(self.index_path)
        return f"Loaded index with {self.index.document_count} page(s) from {self.index_path}."

    def print_word(self, argument: str) -> str:
        if not self._ensure_index():
            return "No index loaded. Run build or load first."
        return SearchEngine(self.index).print_term(argument)

    def find(self, argument: str) -> str:
        if not self._ensure_index():
            return "No index loaded. Run build or load first."
        return SearchEngine(self.index).format_find(argument)

    def explain_ranking(self) -> str:
        if not self._ensure_index():
            return "No index loaded. Run build or load first."
        return SearchEngine(self.index).explain_ranking()

    def help(self) -> str:
        return "\n".join(
            [
                "Commands:",
                "  build              Crawl website, build index, and save it.",
                "  load               Load saved index from data/index.json.",
                "  print <word>       Print inverted index for a word.",
                "  find <query>       Find pages containing all query terms.",
                "  rank               Explain the TF-IDF ranking method.",
                "  help               Show this help message.",
                "  exit               Exit the shell.",
            ]
        )

    def _ensure_index(self) -> bool:
        return self.index is not None


def main() -> None:
    shell = SearchShell()
    print("WebCW2 Search Tool. Type 'help' for commands.")
    while True:
        try:
            command = input("> ")
        except EOFError:
            print()
            break
        output = shell.execute(command)
        print(output)
        if command.strip() == "exit":
            break


if __name__ == "__main__":
    main()
