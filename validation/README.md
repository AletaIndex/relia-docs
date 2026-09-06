# Validation

How well does `relia-1` reproduce expert relevance judgments? These are the public,
trust-building numbers — the model weights and profiles stay private.

## Setup

- **Test set:** 200 articles drawn from a held-out split (seed-fixed), spanning the
  covered entities.
- **Raters:** each article was independently scored by three frontier LLMs — **Gemini**,
  **ChatGPT**, and **DeepSeek** — on the same 4-bin relevance scale
  (`0` irrelevant · `1` low · `2` medium · `3` high).
- **Ground truth = consensus:** the per-article **median** of the three LLM levels.
- **Metrics:**
  - `exact` — predicted bin equals consensus bin
  - `within-1` — predicted bin within one of consensus
  - `binary` — agree on relevant (`level ≥ 1`) vs not
  - `MAE(score)` — mean absolute error of the `[0,1]` expected score

## Baseline ceiling — how much the raters agree

Because relevance is partly subjective, the raters don't perfectly agree even with the
consensus they define. This is the noise floor any model is measured against.

| Rater | exact | within-1 | binary | MAE(level) |
|---|---|---|---|---|
| Gemini vs consensus | 90.5% | 100.0% | 94.0% | 0.095 |
| ChatGPT vs consensus | 90.0% | 99.5% | 92.5% | 0.105 |
| DeepSeek vs consensus | 88.0% | 99.5% | 90.0% | 0.125 |
| **Gemini vs ChatGPT** | **80.5%** | 99.5% | 86.5% | 0.200 |
| **Gemini vs DeepSeek** | **80.5%** | 98.0% | 84.0% | 0.220 |
| **ChatGPT vs DeepSeek** | **78.0%** | 99.0% | 82.5% | 0.230 |

The raters agree with the consensus ~88–90%, but with **each other only 78–80.5%**.

## Trained models vs consensus

Three bi-encoder candidates were trained on the same data; `qwen3` (shipped as
`relia-1`) won.

| Model | exact | within-1 | binary | MAE(level) | MAE(score) |
|---|---|---|---|---|---|
| all-MiniLM-L6-v2 | 79.0% | 98.0% | 85.5% | 0.230 | 0.065 |
| e5-large-v2 | 85.0% | 99.0% | 90.0% | 0.160 | 0.054 |
| **relia-1 (qwen3)** | **86.5%** | **100.0%** | **92.0%** | **0.135** | **0.045** |

**`relia-1` agrees with the consensus (86.5%) more than any two LLMs agree with each
other (≤80.5%)** — i.e. it lands inside the raters' own disagreement band, at 100%
within-1-bin.

## relia-1 vs each rater individually

| vs | exact | within-1 | binary | MAE(score) |
|---|---|---|---|---|
| Gemini | 81.0% | 100.0% | 88.0% | 0.052 |
| ChatGPT | 85.0% | 100.0% | 91.5% | 0.049 |
| DeepSeek | 80.5% | 99.5% | 85.0% | 0.060 |

## Confusion matrix (relia-1 predicted × consensus)

|            | cons 0 | cons 1 | cons 2 | cons 3 |
|------------|:------:|:------:|:------:|:------:|
| **pred 0** |  103   |   6    |   0    |   0    |
| **pred 1** |   10   |  38    |   6    |   0    |
| **pred 2** |    0   |   3    |   6    |   1    |
| **pred 3** |    0   |   0    |   1    |  26    |

Errors are almost entirely off-by-one into an adjacent bin; there is **no** cross-over
between "irrelevant" and "highly relevant".

## Speed

Warm end-to-end latency measured against the hosted `relia-1` endpoint (Cloud Run + L4):

- Single article: ~0.4 s (network-dominated round-trip)
- Batch of 32 articles: 0.585 s total → **~18 ms/article**

## Reproducing the charts

```bash
python validation/make_charts.py   # writes docs/assets/*.png
```

The script uses only the aggregate numbers above (no proprietary profiles or article
text), so it and its outputs are safe to publish.
