# ADR 0002: Immutable raw-output contract

- Status: Accepted
- Date: 2026-09-17

## Context

Milestone 2 introduces persistence, so later S3, Snowflake, and replay work
needs one stable answer for raw-object names, byte preservation, and run
lineage. Ad hoc names or a checksum of re-serialized JSON would make exact
source preservation and read-back verification ambiguous.

## Decision

- Use the versioned [raw output v1 contract](../contracts/raw-output-v1.md).
- Partition root-relative object keys by `provider`, `entity`, UTC observation
  date/hour, and a run UUID; store page-ordered gzip responses plus one
  successful-run manifest.
- Capture raw bytes at the source-client response-body boundary before parsing;
  retain both raw-body and persisted-gzip SHA-256 checksums in the manifest.
- Require create-only writes and publish the manifest only after every payload
  object succeeds.
- Leave statuses, retries, classified failures, and quarantine artifacts to
  Milestone 3 rather than inventing incomplete failure semantics in M2.

## Consequences

### Benefits

- An observation has a collision-resistant, traceable location independent of
  S3 client code.
- Read-back can prove both stored-object integrity and source-body recovery.
- Consumers can treat a manifest as the boundary of a complete successful run.

### Costs and tradeoffs

- Storing each page separately makes pagination traceable but can create many
  small objects for large runs.
- Repeated unchanged source bodies remain separate observations, by design.
- Incomplete writes can leave unreferenced payload objects until reliability
  policy is added; they cannot be mistaken for complete runs because no
  manifest is published.

## Revisit when

- a provider requires a different safe raw-body capture boundary;
- object counts or costs make page-level objects impractical; or
- Milestone 3 establishes failure/quarantine artifact conventions that require
  a new manifest version.
