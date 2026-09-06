# Entity coverage

Relia scores articles against a **curated profile** that we maintain for each supported
entity. You don't write or supply profiles — that's the point: consistent, expert-tuned
relevance criteria without any work on your side.

## Checking coverage

```bash
curl https://<your-deployment>/v1/entities
```

Returns every entity symbol Relia can score. A `POST /v1/score` for an entity outside
this list returns `404`.

## Why we curate profiles

A profile encodes what news is *materially* about an entity — its business, segments,
key customers/competitors, and what counts as an incidental mention. Getting this right
is what makes relevance scores trustworthy, so the profiles are a maintained asset rather
than free-text input. They are proprietary and are not distributed.

## Requesting new coverage

Need an entity we don't cover yet? Contact us — adding an entity is a matter of authoring
and validating its profile.
