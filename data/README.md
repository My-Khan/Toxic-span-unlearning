# Data

## Source

ToxicSpans (Pavlopoulos et al., 2022): English comments from the Civil Comments corpus, in which raters marked the character spans that make a comment toxic. The release has three files:

| File | Rows | Contents |
|---|---:|---|
| `comments.csv` | 16,100 | `comment_id`, `comment_text` |
| `annotations.csv` | 59,215 | one row per rater and comment: `annotation`, `comment_id`, `worker`, `country`, `all toxic`, `not toxic` |
| `spans.csv` | 46,784 | one row per marked span: `annotation`, `type`, `start`, `end` (end exclusive) |

`scripts/download_toxicspans.py` fetches them from commit `beaf170` of [ipavlopoulos/toxic_spans](https://github.com/ipavlopoulos/toxic_spans) (`data/` folder) and checks their SHA-256 sums. The files are licensed CC0 1.0 by their authors.

## Derived files

### `derived/comments_index.csv`

One row per comment kept after preprocessing (16,099 rows), in split order.

| Column | Meaning |
|---|---|
| `comment_id` | identifier in the ToxicSpans release |
| `split` | `train`, `dev` or `test` |
| `n_raters` | number of annotation rows for the comment |
| `has_span` | the comment has at least one majority-vote span |
| `majority_spans` | JSON list of `[start, end)` character ranges marked by more than half of the raters |
| `dev_eval_200` | one of the 200 development comments with spans on which signal agreement was measured (Table C2) |
| `detoxify_original_toxicity` | Detoxify "original" score, for comments without a span only |
| `benign_anchor` | benign training comment (anchor and reference-model data, 703 comments) |
| `benign_test` | benign test comment (benign perplexity, 95 comments) |

How it was built:

1. **Majority vote.** For a comment with *n* raters, character *i* is toxic if more than *n*/2 raters marked it (the union of each rater's spans, whatever their type). Span ends beyond the text are clipped. The one comment with 357 annotation rows is removed. Two misspelled type labels exist in the source but types are not used.
2. **Split.** `numpy.random.RandomState(0).permutation` over the 16,099 comments in file order; the first `int(0.8 N)` are train, the next `int(0.1 N)` dev, the rest test. The split differs from the SemEval-2021 split.
3. **Development checks.** The first 200 development comments with at least one span, in split order. Agreement of the lexicon with gold spans on this set reproduces Table C2 (recall 0.832, F1 0.794).
4. **Benign sets.** Comments without a majority span that the Detoxify "original" checkpoint scores below 0.05. The 703 benign training comments are also part of the 12,879 training comments used to fine-tune the original models.

### `derived/lexicon.txt`

The 120-word lexicon used as a forget signal. **It contains offensive words.** A word (a lower-cased alphabetic string) counts as inside a span when at least half of its characters are covered. Words that occur inside spans in the training comments at least five times, with precision (inside occurrences / all occurrences) of at least 0.5, are kept. The list includes at least one proper name.

### `derived/detector_word_drops_train.jsonl`

Scores of the occlusion detector for the 7,754 training comments with spans, one JSON object per line:

```json
{"comment_id": 5929972, "words": [[0, 3, -0.06], [4, 8, 0.024], ...]}
```

Each entry is `[start, end, drop]`: a word's character range and the fall in the Detoxify "original" toxicity score when that word is deleted. At most 60 words and 500 characters per comment were scored. A word is flagged when the drop exceeds τ = 0.1, the threshold chosen on the 200 development comments. These are the scores used in the experiments; they are the same for all three models.

## Checks

`scripts/verify_derived_data.py` reproduces the statistics of Table 1 in the paper from these files. A rebuild from the source files with `scripts/build_derived_data.py` gives identical spans, split, development set and lexicon.
