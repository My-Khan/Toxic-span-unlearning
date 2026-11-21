# Notebooks

The experiments were run as Kaggle notebooks on one NVIDIA T4 GPU (16 GB), in fp32.

| Notebook | Used for |
|---|---|
| `toxic_span_unlearning_v3.ipynb` | Qwen2.5-0.5B: original and reference models, sample-wise, gold, lexicon and detector runs |
| `toxic_span_unlearning_v3.1.ipynb` | Qwen2.5-0.5B: random-span control, resumed from the v3 output |
| `toxic_span_unlearning_v3.3.ipynb` | TinyLlama v1.1 and OLMo-2-0425-1B |

v3.3 differs from v3 in four ways: the toxic and benign losses are backpropagated separately before one optimiser step (mathematically identical to one backward pass on their sum), the judge model is kept on the CPU, generation adds no extra start token, and a memory-allocator setting is used.

## Running them

Each notebook expects the three ToxicSpans files and writes a `results_<model>_full/` folder with the files found in `../results/`.

Package versions used on Kaggle:

| Package | Version |
|---|---|
| Python | 3.13 |
| torch | |
| transformers | |
| peft | |
| detoxify | |
