# 5-Minute Video Demonstration Script

## 0:00-0:20 Project Overview

This project is a command-line search engine for `quotes.toscrape.com`. It crawls pages politely, creates an inverted index, saves and loads the index, and lets users search for single or multiple terms.

## 0:20-2:20 Live Demonstration

Run:

```text
build
load
print nonsense
find indifference
find good friends
find
find notarealword
rank
```

Explain:

- `build` crawls the website and saves `data/index.json`.
- `load` restores the compiled index from disk.
- `print` shows frequency and positions for a word.
- `find` returns pages containing all query terms, ranked by TF-IDF.
- empty and unknown queries are handled gracefully.

## 2:20-3:50 Code Walkthrough

Show:

- `src/crawler.py`: pagination, 6-second politeness window, error handling.
- `src/indexer.py`: tokenizer, case-insensitive terms, frequency and positions.
- `src/search.py`: multi-word intersection, TF-IDF ranking, suggestions.
- `src/main.py`: shell command dispatch.

Design decision:

The inverted index uses `term -> url -> statistics`, which makes lookup direct and multi-word searching efficient through set intersection.

## 3:50-4:20 Testing Demonstration

Run:

```bash
pytest --cov=src
```

Explain:

Tests mock crawler pages and sleep behavior, so they verify politeness logic without waiting six seconds. Tests cover crawler, indexer, search, CLI, and edge cases.

## 4:20-4:40 Version Control

Run:

```bash
git log --oneline --decorate -n 8
```

Explain:

The commit history shows incremental development: scaffold, crawler, indexer, CLI, ranking, tests, documentation, and final index generation.

## 4:40-5:00 GenAI Critical Evaluation

GenAI helped me compare indexing structures and think about edge cases. However, some suggestions were too broad and missed coursework-specific needs such as storing word positions and testing politeness without delay. I treated AI output as a proposal, manually revised it, and validated the final implementation through tests.
