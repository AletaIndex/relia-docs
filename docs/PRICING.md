# Pricing & Rate Limits

Relia is billed per request — simple and predictable.

## Pricing

| | |
|---|---|
| **Price** | **$1 / 1,000 requests** |
| **What's a request?** | 1 request = 1 entity + up to **100 articles**. No token chunking — long articles count as one. |
| **Free tier** | **2,000 requests free** — no time limit, no monthly reset. |
| **After the free tier** | Top up anytime, prepaid. You only pay for what you use. |

## Rate limits

Applied per API key on a rolling 60-second window. Exceeding the limit returns HTTP `429`
with a `Retry-After` header indicating the seconds until the window resets.

| Limit | Value |
|---|---|
| Requests / minute | 120 |
| Articles / request | 100 |

- Batch multiple articles in a single `POST /v1/score` (up to 100) — it's both faster and
  counts as one request against the per-minute limit.
- Need higher limits or volume pricing? [Contact the team](mailto:info@aletaindex.com).

## How Relia's pricing differs from LLM APIs

LLM relevance raters bill **per token** — every article you score costs input tokens
(≈1.8K/article) on every call, and matching Relia's accuracy means running a *panel* of
models, multiplying that cost.

Relia is a single purpose-built model behind one API call, billed per request — no
per-token metering. See [`../validation/README.md`](../validation/README.md) for the
measured cost and speed comparison.

## Contact

Volume pricing or higher limits: **info@aletaindex.com**
