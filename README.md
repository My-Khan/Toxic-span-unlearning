# Forgetting the Words, Keeping the Sentence

Code, derived data and results for the paper **"Forgetting the Words, Keeping the Sentence: Token-Level Unlearning of Toxic Spans in Large Language Models"**.

> **Content warning.** This repository works with abusive online comments. The lexicon, the run logs and the source data contain offensive words. Model generations are not included (see [What is not included](#what-is-not-included)).

The paper compares token-level and sample-level unlearning of toxic spans from the ToxicSpans dataset in three LoRA-fine-tuned models (Qwen2.5-0.5B, TinyLlama v1.1 and OLMo-2-0425-1B), at matched forgetting levels. This repository holds what is needed to check and reuse those results: the exact data split, the majority-vote spans, the forget signals, and the per-run measurements behind every table and figure.

## Repository layout

```
data/
  raw/                         ToxicSpans source files (downloaded, not committed)
  derived/
    comments_index.csv         split, majority-vote spans, dev-check set, benign sets
    lexicon.txt                the 120-word lexicon (offensive words)
    detector_word_drops_train.jsonl   occlusion-detector scores for training comments
scripts/
  download_toxicspans.py       fetches the source files at a pinned commit, checks SHA-256
  build_derived_data.py        rebuilds data/derived from the source files
  verify_derived_data.py       prints the statistics of Table 1 and compares a rebuild
notebooks/                     the Kaggle notebooks that produced the results
results/
  cross_model_table.csv        summary across the three models
  <model>/                     per-run measurements, baselines, training curves, logs
figures/                       method schematic, cross-model and per-model figures
```

## Quick start

```bash
pip install -r requirements.txt
python scripts/download_toxicspans.py     # about 6.5 MB, checked against fixed checksums
python scripts/verify_derived_data.py     # prints Table 1 of the paper
```

To rebuild the derived data from scratch and compare it with the shipped files:

```bash
python scripts/build_derived_data.py      # writes data/rebuilt/
python scripts/verify_derived_data.py
```

Add `--detoxify` to the build to recompute the benign sets as well. This needs the `detoxify` package and downloads its "original" checkpoint.

## Data

The source data is the ToxicSpans release of [Pavlopoulos et al. (2022)](https://aclanthology.org/2022.acl-long.259/), available from [github.com/ipavlopoulos/toxic_spans](https://github.com/ipavlopoulos/toxic_spans) under CC0 1.0. It is not copied here; the download script fetches the three files from a pinned commit. The derived data is described in [`data/README.md`](data/README.md).

| | Train | Dev | Test |
|---|---:|---:|---:|
| Comments | 12,879 | 1,609 | 1,611 |
| With at least one span | 7,754 | 971 | 935 |
| Median length (words) | 25 | 25 | 24 |
| Toxic share of characters (comments with spans) | 11.5% | 10.7% | 12.6% |
| Benign comments after filtering | 703 | – | 95 |

## Results

Each folder under `results/` corresponds to one model and holds the files written by the notebooks:

| File | Contents |
|---|---|
| `operating_points.csv` | one row per run and forgetting level: test-split measurements at the crossing |
| `baselines.csv` | the original model and the retrain reference |
| `dynamics.csv` | development-set span NLL and other-token NLL during unlearning |
| `signal_quality.csv` | agreement of the lexicon, detector and random signals with gold spans |
| `results_table.csv` | the summary table produced by the notebook |
| `meta.json` | model identifier, vocabulary size, ln\|V\|, retrain-level span NLL, targets |
| `summary.txt`, `logs/progress.log` | run summary and notebook log |

Column definitions are in [`results/README.md`](results/README.md). All rates in these files are fractions between 0 and 1; the paper reports them as percentages.

## What is not included

- **Model adapters.** The original adapters were fine-tuned on toxic comments and reproduce toxic language, so they are not released.
- **Raw generations.** The 500 toxic-prompt and 82 benign-prompt continuations of every run contain unmasked abusive text and are kept private. Aggregate measurements computed from them are in `results/`.
- **Qualitative example tables.** The example figures in the paper are not repeated here.

The reasons are set out in [`ETHICS.md`](ETHICS.md).

## Citation

If you use this repository, please cite the paper (details will be added on publication) and the ToxicSpans dataset:

```bibtex
@inproceedings{pavlopoulos-etal-2022-detection,
  title     = {From the Detection of Toxic Spans in Online Discussions to the Analysis of Toxic-to-Civil Transfer},
  author    = {Pavlopoulos, John and Laugier, L{\'e}o and Xenos, Alexandros and Sorensen, Jeffrey and Androutsopoulos, Ion},
  booktitle = {Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)},
  year      = {2022},
  doi       = {10.18653/v1/2022.acl-long.259}
}
```

Software citation metadata is in [`CITATION.cff`](CITATION.cff).

## Licence

Code is released under the MIT licence ([`LICENSE`](LICENSE)). Derived data, results and figures are released under CC BY 4.0 ([`DATA_LICENSE.md`](DATA_LICENSE.md)). The ToxicSpans source data remains under its own CC0 1.0 licence.
