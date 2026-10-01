# Pricing & Rate Limits

Relia is billed per call — simple and predictable.

## Pricing

| | |
|---|---|
| **Price** | **$0.0025 / call** |
| **What's a call?** | 1 call = 1 entity + up to **50 articles**. No token chunking — long articles count as one. |
| **Free tier** | **500 calls free** — no time limit, no monthly reset. |
| **After the free tier** | Top up anytime, prepaid. You only pay for what you use. |

## Rate limits

Applied per API key on a rolling 60-second window. Exceeding the limit returns HTTP `429`
with a `Retry-After` header indicating the seconds until the window resets.

| Limit | Value |
|---|---|
| Calls / minute | 120 |
| Articles / call | 50 |

- Batch multiple articles in a single `POST /v1/score` (up to 50) — it's both faster and
  counts as one call against the per-minute limit.
- Need higher limits or volume pricing? [Contact the team](mailto:info@aletaindex.com).

## How Relia's pricing differs from LLM APIs

LLM relevance raters bill **per token** — every article you score costs input tokens
(≈1.8K/article) on every call, and matching Relia's accuracy means running a *panel* of
models, multiplying that cost.

Relia is a single purpose-built model behind one API call, billed per call — no
per-token metering. To compare costs on the same basis: 1M input tokens covers about 556
articles at that rate — see [`../validation/README.md`](../validation/README.md) for the
measured cost and speed comparison against what that same volume costs on Relia.

## Contact

Volume pricing or higher limits: **info@aletaindex.com**
