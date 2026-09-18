# Raw output contract v1

## Purpose and scope

This contract defines the artifacts that a successful Milestone 2 Kalshi
extraction will persist. It is deliberately independent of an S3 SDK and
Terraform implementation. Its root-relative keys are placed beneath the
environment-specific raw bucket in Milestone 2 task M2-T4.

The contract covers successful, fully retrieved `markets` runs only. It does
not make a partial or failed run look complete.

## Object key grammar

Each run has this root-relative prefix:

```text
provider=<provider>/entity=<entity>/observed_date=<YYYY-MM-DD>/observed_hour=<HH>/run_id=<run-id>/
```

It contains one gzip-compressed source response for every retrieved page and a
single manifest:

```text
response-<page-sequence>.json.gz
manifest.json
```

The complete grammar is therefore:

```text
provider=<provider>/entity=<entity>/observed_date=<UTC-date>/observed_hour=<UTC-hour>/run_id=<run-id>/response-<page-sequence>.json.gz
provider=<provider>/entity=<entity>/observed_date=<UTC-date>/observed_hour=<UTC-hour>/run_id=<run-id>/manifest.json
```

`provider` and `entity` use lower-case ASCII identifiers matching
`[a-z0-9][a-z0-9_-]{0,63}`. For the initial collector they are `kalshi` and
`markets`. `observed_date` and `observed_hour` are respectively the UTC date
and zero-padded 24-hour (`00` through `23`) partition derived from the one
run-level `observed_at` timestamp. `run-id` is a lower-case, canonical textual
UUID. It is supplied by the run boundary; it is not generated from a response
or key.

`page-sequence` is the one-based request order, zero-padded to at least four
digits (for example, `0001`; more digits are allowed after `9999`). It includes
an empty-but-valid response page. No source-controlled value may become a path
segment.

The key includes both logical provider/entity dimensions and the UTC observation
partition. It is not a request-time, source-created-time, or ingestion-time
partition.

## Byte, compression, and checksum boundary

For each page, `response_bytes` is the exact byte sequence returned by the HTTP
client's response-body byte interface at the source-client boundary, captured
before character decoding, JSON parsing, validation, pretty-printing, or
re-serialization. HTTP transport framing, headers, credentials, and request
authorization are not part of this artifact.

The corresponding `response-<page-sequence>.json.gz` object is a gzip encoding
of exactly `response_bytes`; decompressing it must recover byte-for-byte the
captured response. Compression must use a fixed zero timestamp and no filename
metadata so an implementation can create repeatable stored bytes from the same
input. Compression is a physical representation only, never a JSON
normalization step.

Every raw-object entry records two SHA-256 digests, written as 64 lower-case
hexadecimal characters without a prefix:

- `response_sha256` is calculated from `response_bytes`.
- `compressed_sha256` is calculated from the exact gzip bytes written to the
  object key.

`response_bytes` and `compressed_bytes` are the corresponding byte lengths.
The latter digest and length verify what was persisted; the former verifies that
decompression restored the source body.

## Immutability and publication

Object names are deterministic when the provider, entity, observation time,
run ID, and page sequence are supplied. A new observation must use a new run
ID, even if its source response is unchanged.

The writer must use create-only semantics for every payload and manifest key.
An existing key is a collision: it must be reported to the caller and must not
be overwritten, deleted, or silently reused. A normal raw-data writer has no
delete or replace path.

Publish every payload object in ascending page sequence before publishing
`manifest.json`. Manifest publication is the successful-run completion signal;
there must be no manifest if a required payload could not be published. This
contract does not define rollback or failure records.

## Manifest schema

`manifest.json` is UTF-8 JSON with this logical shape. Keys in this document
are required unless explicitly marked optional.

```json
{
  "schema_version": "raw-output/v1",
  "run": {
    "run_id": "<uuid>",
    "provider": "kalshi",
    "entity": "markets",
    "observed_at": "<RFC-3339 UTC timestamp>",
    "request_started_at": "<RFC-3339 UTC timestamp>",
    "request_completed_at": "<RFC-3339 UTC timestamp>",
    "collector_version": "<non-empty version string>",
    "git_sha": "<non-empty revision string>",
    "request": {
      "endpoint": "<non-secret endpoint path or URL>",
      "parameters": { "<non-secret parameter>": "<value>" }
    }
  },
  "raw_objects": [
    {
      "key": "provider=kalshi/entity=markets/observed_date=2026-09-17/observed_hour=14/run_id=<uuid>/response-0001.json.gz",
      "page_sequence": 1,
      "request_cursor": null,
      "next_cursor": "<cursor or empty terminal string>",
      "record_count": 0,
      "response_bytes": 0,
      "compressed_bytes": 0,
      "response_sha256": "<64 lower-case hex characters>",
      "compressed_sha256": "<64 lower-case hex characters>"
    }
  ],
  "totals": {
    "raw_object_count": 1,
    "record_count": 0,
    "response_bytes": 0,
    "compressed_bytes": 0
  }
}
```

All timestamps are RFC 3339 UTC strings ending in `Z`; `observed_at` is the
collector observation time and does not replace any source timestamp inside a
payload. `request.parameters` contains only non-secret, request-shaping values;
authorization headers, credentials, and secret values are prohibited. The
first page has `request_cursor: null`; a cursor used on a later request is a
non-empty string. A valid terminal `next_cursor` is the empty string.

Every count is a non-negative integer. `raw_objects` is ordered by
`page_sequence`, has no duplicate key or page sequence, and contains at least
one entry for a successful run. `totals` is the sum of the corresponding raw
object fields. `raw_object_count` counts payload objects only; it excludes the
manifest. Each `key` is root-relative, follows this document's grammar, and
identifies the exact object whose compressed checksum it carries.

The manifest does not carry a checksum for itself: adding one inside the same
document would be circular. Its known key and the checksums of all raw objects
are sufficient for the Milestone 2 read-back demonstration.

## Deferred to Milestone 3

M2 persists only complete successful runs and does not define a run-status
field. M3 will add the durable semantics and metadata for `complete`, `empty`,
`partial`, `quarantined`, and `failed` outcomes; error categories; retry and
rate-limit attempts; failure timestamps and diagnostics; preservation/quarantine
of malformed responses; and any failure or partial-run artifacts. M3 may extend
this schema with a new version but must not reinterpret a v1 manifest.
