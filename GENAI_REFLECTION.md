# GenAI Critical Evaluation

## Tools Used

Generative AI was used for planning, debugging, code-review style critique, README drafting, and test-case brainstorming.

## Where GenAI Helped

- Suggested that an inverted index should store more than URLs.
- Helped compare REST-like command flows and interactive shell design.
- Suggested edge cases such as empty queries and missing words.
- Helped structure the 5-minute video demonstration.

## Where GenAI Hindered

- Initial suggestions were too generic and did not always include word positions.
- Some test ideas would have waited for the real six-second politeness window, which would make tests slow.
- AI suggestions needed manual simplification to keep the command-line tool explainable.

## Human Corrections

- I changed the index format to store `frequency` and `positions`.
- I injected the sleep function into the crawler so tests can mock it.
- I selected explainable TF-IDF ranking instead of a more complex recommendation model.
- I added explicit CLI messages for empty inputs and unknown commands.

## Learning Reflection

GenAI accelerated design exploration, but it did not replace understanding. The most useful learning came from checking AI suggestions against the assignment brief, writing tests, and explaining each trade-off in the video.
