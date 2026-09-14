# Kalshi NFL market ingestion specification

## Status

Initial specification for Milestones 1-8. Amend deliberately when observed API
behavior proves an assumption wrong.

## Objective

Collect reproducible, append-only observations of Kalshi NFL markets so that
later analytical models can reconstruct what the collector observed at a given
time and trace every normalized record to its original response.

## Initial scope

- Provider: Kalshi
- Domain: NFL game and player-related markets available through the supported API
- Initial entity: markets
- Initial cadence: hourly once scheduling is implemented
- Initial interface: deterministic fixture mode plus an explicitly selected,
  read-only live mode
- Repository responsibility: extraction, storage, loading, transformation,
  validation, and operational observability

## Non-goals through Milestone 8

- Trading, order placement, or account-position management
- Website or public API
- Fantasy projections or recommendations
- Guaranteed tick-level or order-book reconstruction
- FanDuel, DraftKings, or other providers
- Browser automation or anti-bot workarounds
- Fully autonomous agent operation or merging

## Functional requirements

### Extraction

1. The collector must retrieve all pages for the requested entity and filters.
2. Every run must have a unique run ID and UTC observation timestamp.
3. Fixture mode must use committed, sanitized source-shaped responses and require
   no network access.
4. Live mode must be opt-in and read-only.
5. Empty results may be valid but must be distinguishable from incomplete or
   failed retrieval.
6. Retryable failures must use bounded exponential backoff with jitter.
7. The collector must not silently treat partial pagination as success.

### Raw preservation

1. Once S3 is in scope, preserve the exact response body before normalization.
2. Compression may change the physical representation but not its contents.
3. Raw objects are immutable. Corrections produce new observations or explicit
   reprocessing outputs.
4. Invalid or unexpected responses must be preserved in a quarantine path when
   safe to do so.

### Traceability

Every persisted run must eventually retain:

- run ID;
- provider and entity;
- request start/completion and observation timestamps;
- endpoint and non-secret request parameters;
- page/cursor sequence;
- record, byte, and object counts;
- response checksum;
- completion status and error category;
- collector/schema version and Git SHA;
- raw object key(s).

### Security

- Credentials and private keys come from environment-specific secret storage.
- Secrets, authorization headers, and private-key contents must never appear in
  logs, exceptions, fixtures, manifests, or committed files.
- The collector is read-only through Milestone 8.
- Cloud roles use least privilege and development cannot write to production data.

## Minimum market representation

The normalized application model should retain, when supplied by the source:

- provider market identifier/ticker;
- event or series identifier;
- title and subtitle/description;
- market status;
- open, close, and expiration timestamps;
- yes/no bid, ask, last, or equivalent price fields;
- volume and open interest;
- source-created and source-updated timestamps;
- rules or settlement metadata needed to interpret the contract;
- raw or unknown fields through the preserved source payload.

Exact field names and optionality should be derived from the current API response
and committed fixture rather than guessed. Changes in the source schema should
fail visibly when required fields disappear while allowing unknown fields to be
preserved.

## Snapshot semantics

- `observed_at` means when this collector observed the response.
- Source timestamps retain their source meaning and must not replace `observed_at`.
- Repeated unchanged market states are valid observations unless a later ADR
  explicitly introduces content-addressed deduplication.
- The snapshot grain must eventually be explicit and enforced in dbt.

## Initial acceptance scenarios

1. Valid single-page fixture returns typed records.
2. Valid empty fixture returns a successful zero-record outcome.
3. Malformed response produces a validation failure without leaking payload secrets.
4. Multi-page fixture retrieves every page exactly once and stops at the terminal cursor.
5. Rate-limit response retries within policy and either succeeds or fails visibly.
6. Replaying a previously ingested raw object does not duplicate Snowflake records.
7. Missing successful runs beyond the freshness threshold generate an alert.
8. A selected historical interval can be safely backfilled.

## Open questions to resolve from evidence

- Which Kalshi identifiers most reliably connect series, events, and markets?
- Which NFL and player-market filters are stable enough for production retrieval?
- Which fields and endpoints require authentication for read-only access?
- How frequently do source schemas or market taxonomies change?
- Is hourly capture sufficient for the intended first analytical use case?
- What file size and load cadence minimize Snowflake cost without sacrificing freshness?

