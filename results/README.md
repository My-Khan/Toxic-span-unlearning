# Results

One folder per model: `qwen2.5-0.5b`, `tinyllama-v1.1`, `olmo-2-0425-1b`. The files are the outputs of the notebooks, unchanged. Rates are fractions between 0 and 1.

## `operating_points.csv`

One row per unlearning run (method × seed) and forgetting level reached. Measurements are on the test split, taken when the development span NLL first crossed the target.

| Column | Meaning |
|---|---|
| `method` | `sample` (sample-wise), `token_gold`, `token_lex`, `token_det`, `token_rand` (token-wise with gold spans, lexicon, detector or random spans) |
| `seed` | unlearning seed (0, 1, 2 for Qwen2.5; 0, 1 for the other models) |
| `target` | span-NLL target τ_ρ; the four values per model are listed in `meta.json` (retrain level, 30, 60 and 90 percent) |
| `kind`, `tag` | run type and run label |
| `also_crossed` | other targets crossed at the same development check (the model is labelled with the highest) |
| `step` | unlearning step of that development check |
| `dev_span_nll` | development span NLL at that check |
| `span_nll` | test span NLL on the forget tokens of the 935 test comments with spans |
| `nonspan_nll` | test NLL on the remaining tokens of the same comments (other-token NLL) |
| `benign_ppl` | perplexity on the 95 benign test comments (divide by the original model's value in `baselines.csv` for the ratio) |
| `toxicity`, `toxic>0.5` | mean judge-1 score and share of the 500 continuations scored above 0.5 (Detoxify "original") |
| `toxicity2`, `toxic2>0.5` | the same for judge 2 (Detoxify "unbiased") |
| `lexical_leak` | share of continuations containing a gold span string (longer than two characters) of their prompt comment |
| `semantic_leak` | judge-1 toxic rate among continuations without lexical leakage |
| `fluency_nll` | mean NLL of the continuation under the frozen pretrained model of the same family |
| `repeat3` | share of repeated word 3-grams, averaged over continuations with at least three words |
| `empty_rate` | share of continuations with at most one character after stripping |
| `avg_words`, `distinct1` | mean continuation length in words and distinct-word ratio (not reported in the paper) |
| `benign_*` | the same measures on the 82 benign prompts |

## Other files

| File | Contents |
|---|---|
| `baselines.csv` | the measurements above for the original model and the retrain reference |
| `dynamics.csv` | `method`, `seed`, `step`, `dev_span_nll`, `dev_nonspan_nll`: development checks every 5 steps up to step 100, then every 20 |
| `signal_quality.csv` | character-level precision, recall and F1 of each signal against gold spans on the 200 development comments, and the share of characters flagged |
| `results_table.csv` | the notebook's summary table (column names are LaTeX-escaped) |
| `meta.json` | `model`, `vocab`, `lnV` (ln\|V\|), `ref_span` (retrain-level span NLL), `targets`, `fracs`, `orig_span` (original model span NLL) |
| `summary.txt` | the notebook's plain-text summary |
| `logs/progress.log` | the notebook log, including run times; it lists some lexicon words |

`cross_model_table.csv` collects benign perplexity ratio, toxic continuations (judge 1, percent), other-token NLL and empty outputs per model, level and method, with the number of seeds.

## Which code produced which results

| Results | Notebook version |
|---|---|
| Qwen2.5: original, reference, sample-wise, gold, lexicon, detector (3 seeds) | v3 |
| Qwen2.5: random control (3 seeds) | v3.1, resumed from the v3 output |
| TinyLlama v1.1 and OLMo-2-0425-1B: sample-wise, gold, detector (2 seeds) | v3.3 |
