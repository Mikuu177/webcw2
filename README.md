# WebCW2 - Search Engine Tool

Coursework 2 for COMP/XJCO3011 Web Services and Web Data.

This project implements a command-line search engine for `https://quotes.toscrape.com/`.

## Features

- Polite crawler with at least 6 seconds between live HTTP requests.
- Inverted index with word frequency and positions per page.
- Persistent index saved to `data/index.json`.
- Interactive commands: `build`, `load`, `print`, `find`, `help`, `exit`.
- Ranked multi-word search and query suggestions.
- Automated tests for crawler, indexer, search, and CLI behavior.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python -m src.main
```

Example commands inside the shell:

```text
build
load
print nonsense
find indifference
find good friends
find notarealword
exit
```

## Testing

```bash
pytest --cov=src
```

## Submission Notes

The compiled index file is generated at `data/index.json` after running `build`.

GenAI was used as a planning and debugging aid. The video demonstration explains where AI suggestions helped, where they required correction, and how manual testing shaped the final implementation.
