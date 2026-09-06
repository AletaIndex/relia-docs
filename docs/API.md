# Relia API Reference

Base URL: `https://<your-deployment>`

## `POST /v1/score`

Score a batch of articles against a supported entity. Relia uses its own **curated
profile** for that entity — you do not supply one.

### Request

```json
{
  "model": "relia-1",
  "entity": "NVDA",
  "articles": [
    { "id": "a1", "title": "Headline", "body": "Article text..." }
  ]
}
```

| Field | Type | Required | Notes |
|---|---|---|---|
| `entity` | string | yes | A supported entity symbol. See `GET /v1/entities`. |
| `articles` | array | yes | Each item: `id`, `title`, `body`. |
| `articles[].id` | string \| int | yes | Echoed back so you can match results. |
| `articles[].title` | string | no | Headline. |
| `articles[].body` | string | no | Body. At least one of title/body must be non-empty. |
| `model` | string | no | Defaults to `relia-1`. |

### Response

```json
{
  "model": "relia-1",
  "entity": "NVDA",
  "scores": [
    { "id": "a1", "score": 0.87, "level": 3, "probs": [0.01, 0.04, 0.28, 0.67] }
  ]
}
```

| Field | Meaning |
|---|---|
| `score` | Expected relevance in `[0, 1]`. |
| `level` | Argmax bin: `0` irrelevant → `3` highly relevant. |
| `probs` | Distribution over the relevance bins. |

Articles with no usable text are omitted from `scores`.

### Errors

| Status | When |
|---|---|
| `404` | `entity` is not covered. Call `GET /v1/entities` for the supported list. |
| `400` | Unknown `model`. |

## `GET /v1/entities`

List every entity Relia can score.

```json
{ "entities": ["AAPL", "AMD", "AMZN", "GOOGL", "META", "MSFT", "NVDA", "TSLA"] }
```

## `GET /health`

```json
{ "status": "ok", "model": "relia-1" }
```

## Notes

- Articles are scored independently; batching many in one request is more efficient.
- Score bins: `0.125 / 0.375 / 0.625 / 0.875` — `score` is their probability-weighted mean.
- A common production filter is `score >= 0.50` (i.e. relevance level ≥ 1).
