# Ethics and release decisions

**Toxic content.** The source data contains abusive language, some of it aimed at groups and individuals. The lexicon (`data/derived/lexicon.txt`) and the run logs list offensive words. They are included because the lexicon is one of the forget signals compared in the paper.

**What is withheld, and why.**

- *Original model adapters.* They were fine-tuned on toxic comments to give each model a controlled source of toxic behaviour, and they reproduce toxic language. Releasing them would add risk without helping anyone check the results.
- *Raw generations.* Continuations of toxic prompts contain unmasked abuse. Only aggregate measurements are released.
- *Qualitative example tables.* Masking in the example figures covers only words from the lexicon, so other abusive words and personal names can remain visible.

**Limits of the evidence.** All toxicity and fluency results rest on automatic measures: two Detoxify judges, a frozen-model fluency score and repetition counts. No human ratings were collected. The results describe reduced toxic generation on the tested prompts under these judges; they are not a guarantee of safety, and they do not show that toxic knowledge has been erased.

**Possible misuse.** The method is not specific to toxicity. The same objective could be used to suppress other kinds of speech, and forgetting words correlated with identity or politics may reduce a model's ability to discuss them.

**Licensing.** The ToxicSpans authors release their data under CC0 1.0. The three models (Qwen2.5-0.5B, TinyLlama v1.1, OLMo-2-0425-1B) are distributed by their developers under their own licences; check the model cards before reusing them.
