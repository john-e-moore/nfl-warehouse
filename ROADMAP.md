# Data platform roadmap

This roadmap covers the first production-capable Kalshi pipeline. Only the
current milestone should be decomposed into daily tasks. Later milestones remain
outcome-level until they become current.

## Status

| Milestone | State | Demonstration |
| --- | --- | --- |
| 1. Local extraction package | Complete | Fixture and live Kalshi market extraction work through one CLI boundary |
| 2. Development S3 output | Current | A run writes immutable raw JSON and a manifest that can be read back |
| 3. Reliability and metadata | Not started | Simulated pagination, rate limits, retries, and malformed responses behave correctly |
| 4. Scheduled Fargate deployment | Not started | Manual and scheduled tasks run the same immutable container successfully |
| 5. Snowflake raw ingestion | Not started | New objects load idempotently and remain traceable to S3 and the extraction run |
| 6. dbt transformations | Not started | `dbt build` creates tested staging models and a minimal market snapshot mart |
| 7. Monitoring and alerts | Not started | Forced execution failure and stale-data conditions both notify the operator |
| 8. Production trial | Not started | Several NFL slates run reliably and a detected gap is successfully backfilled |

## Codex model guidance

These recommendations optimize for the lowest-cost model likely to complete each
task well. They are based on the [OpenAI model catalog](https://developers.openai.com/api/docs/models),
which positions GPT-5.6 Luna for cost-sensitive work, GPT-5.6 Terra as the
intelligence/cost balance, GPT-5.6 Sol for complex professional work, and GPT-6
Astra for the hardest end-to-end work. Recheck the catalog when a milestone
becomes current because model availability and pricing can change.

Use the recommended model for implementation and its required verification.
Increase reasoning one level after a weak or incomplete attempt. Escalate the
specific difficult subtask to the next model only if increased reasoning is
still insufficient; do not rerun the entire milestone on a more expensive
model. Reserve GPT-6 Astra for an unresolved cross-system design, security, or
debugging problem rather than routine execution.

| Work item | Recommended model | Reasoning | Rationale |
| --- | --- | --- | --- |
| M1-T1 — Package and fixture parser | GPT-5.6 Luna | Medium | Small, bounded Python slice with fixture-backed acceptance checks. |
| M1-T2 — Read-only live client | GPT-5.6 Terra | Medium | External API boundary, authentication hygiene, and error handling need stronger judgment. |
| M1-T3 — Pagination | GPT-5.6 Terra | High | Completeness, cursor termination, and edge cases are correctness-sensitive. |
| M1-T4 — Developer commands and quality checks | GPT-5.6 Luna | Medium | Mostly mechanical packaging, documentation, linting, typing, and verification. |
| M2-T1 — Raw output contract | GPT-5.6 Terra | High | The object-key grammar, immutable-write semantics, and manifest contract determine every later persistence step. |
| M2-T2 — Raw artifact construction | GPT-5.6 Terra | High | Byte-preserving compression, checksums, and manifest assembly need careful deterministic tests. |
| M2-T3 — Development S3 infrastructure | GPT-5.6 Terra | High | Terraform state boundaries, bucket protections, and least-privilege IAM require cloud and security judgment. |
| M2-T4 — S3 persistence and read-back demonstration | GPT-5.6 Terra | High | Safe immutable writes and end-to-end checksum verification cross the application and AWS boundaries. |
| Milestone 3 — Reliability and metadata | GPT-5.6 Terra | High | Retry classification, quarantine states, and failure-path tests require careful state reasoning. |
| Milestone 4 — Scheduled Fargate deployment | GPT-5.6 Sol | High | CI, OIDC, IAM, networking, Terraform, and runtime diagnosis form a complex cloud boundary. |
| Milestone 5 — Snowflake raw ingestion | GPT-5.6 Sol | High | Storage integration, roles, idempotent loading, and lineage cross two managed systems. |
| Milestone 6 — dbt transformations | GPT-5.6 Terra | High | SQL modeling and data tests are well-scoped but grain and timestamp semantics need scrutiny. |
| Milestone 7 — Monitoring and alerts | GPT-5.6 Sol | High | End-to-end failure detection crosses CloudWatch, S3, Snowflake, and dbt. |
| Milestone 8 — Production trial | GPT-5.6 Terra | High | The work is primarily evidence review, gap diagnosis, backfill verification, and documentation. |

When a future milestone becomes current, decompose it first and downgrade
routine subtasks such as documentation, formatting, fixture creation, and
straightforward test additions to GPT-5.6 Luna at medium reasoning. Keep the
milestone-level recommendation for architecture, permissions, data contracts,
failure semantics, and end-to-end diagnosis.

## Milestone 1 — Local extraction package

### Outcome

A developer can run a provider-neutral Python command locally to retrieve and
validate Kalshi NFL market data, with deterministic fixture-backed tests and an
optional live integration path.

### Definition of done

- [ ] The package installs from a clean checkout using documented commands.
- [ ] A CLI command parses the committed Kalshi markets fixture without network
      access.
- [ ] The same application boundary can call the live Kalshi API when explicitly
      requested and credentials/configuration are present.
- [ ] Pagination retrieves all pages and terminates correctly.
- [ ] Parsed records retain the fields required by the ingestion spec.
- [ ] Tests cover success, empty results, malformed data, and pagination.
- [ ] Formatting, linting, typing, and tests pass using documented commands.
- [ ] No AWS, S3, Snowflake, dbt, scheduler, or production infrastructure is
      required.

### Demonstration

From a clean checkout, run the fixture-backed command and tests. If live access
is configured, run one read-only live retrieval and report the record/page count
without printing secrets.

## Milestone 2 — Development S3 output

### Outcome

An extraction writes the exact source response and a run manifest to a dedicated
development S3 bucket using an immutable, partitioned key convention.

### Definition of done

- [ ] Development bucket and least-privilege writer role exist through Terraform.
- [ ] Raw payloads are stored as compressed JSON without normalization.
- [ ] Each run writes a manifest containing run metadata and object checksums.
- [ ] Object keys contain provider, entity, observation date/hour, and run ID.
- [ ] A saved payload and manifest can be retrieved and verified.
- [ ] Local fixture mode remains usable without AWS.

### Tasks

#### M2-T1 — Define the raw output contract

Specify the persistence boundary before adding AWS behavior so object layout,
immutability, and traceability have one testable contract.

- [ ] Document the partitioned key grammar for raw payloads and manifests,
      including provider, entity, UTC observation date/hour, and run ID.
- [ ] Define immutable-write behavior and the response-body byte boundary used
      for compression and checksums.
- [ ] Define the Milestone 2 manifest schema with run metadata, raw object keys,
      byte and record counts, and checksums required by the ingestion spec.
- [ ] Record explicitly which richer statuses and failure metadata remain for
      Milestone 3.

#### M2-T2 — Build raw payload and manifest artifacts

Construct persistence-ready artifacts independently of AWS, retaining fixture
mode as the default offline path.

- [ ] Capture each exact source response body before normalization and encode it
      as compressed JSON without changing its contents.
- [ ] Generate keys and manifests through the M2-T1 contract with deterministic
      behavior for a supplied run ID and observation timestamp.
- [ ] Compute and test checksums against the bytes that will be persisted.
- [ ] Add fixture-backed tests for payload round trips, manifest contents,
      partition fields, and collision-safe object naming.
- [ ] Confirm the existing local fixture command and offline test suite require
      no AWS configuration or network access.

#### M2-T3 — Provision development S3 infrastructure

Create only the development storage and identity resources needed to exercise
the persistence boundary.

- [ ] Define the development bucket and writer role through Terraform with
      encryption, public-access blocking, and appropriate ownership settings.
- [ ] Grant the writer only the object and bucket permissions required by the
      documented key layout and read-back demonstration.
- [ ] Configure protections that prevent routine overwrites or deletion of raw
      observations.
- [ ] Document initialization, plan, apply, and safe teardown commands without
      committing credentials, state, or environment-specific data.
- [ ] Validate formatting and configuration locally, and review the plan before
      applying it to the development account.

#### M2-T4 — Persist to S3 and verify read-back

Connect the artifact boundary to S3 and demonstrate a complete development
write without changing the offline default workflow.

- [ ] Add an explicitly selected S3 output path that writes payload objects
      before their manifest and refuses to replace an existing key.
- [ ] Keep AWS credentials outside application arguments, logs, manifests, and
      committed configuration.
- [ ] Test S3 behavior with a local fake or stub, including write ordering,
      collision handling, and failed-write behavior.
- [ ] Run one authorized development integration that retrieves the stored
      payload and manifest, decompresses the payload, and verifies every
      recorded checksum and object reference.
- [ ] Record the demonstration evidence and confirm the local fixture workflow
      still passes without AWS.

## Milestone 3 — Reliability and metadata

### Outcome

The collector fails visibly, retries safely, and distinguishes complete,
partial, empty, quarantined, and failed runs.

### Definition of done

- [ ] Bounded exponential backoff with jitter handles retryable failures.
- [ ] Rate limiting, timeouts, and server failures have explicit error categories.
- [ ] Pagination completeness is validated.
- [ ] Structurally invalid responses are preserved and quarantined.
- [ ] Structured run summaries include counts, bytes, duration, status, and code version.
- [ ] Automated tests simulate all important failure paths.

## Milestone 4 — Scheduled Fargate deployment

### Outcome

The same container used locally runs as an ECS Fargate task manually and on an
EventBridge schedule.

### Definition of done

- [ ] Terraform provisions ECR, ECS task definitions, IAM, logs, and schedules.
- [ ] CI builds an immutable image and authenticates to AWS with OIDC.
- [ ] A manual task produces expected development S3 objects.
- [ ] An EventBridge-triggered task produces expected objects.
- [ ] Task image digest, Git SHA, and run ID are traceable.
- [ ] No NAT Gateway is required by the initial architecture.

## Milestone 5 — Snowflake raw ingestion

### Outcome

New S3 objects load into Snowflake raw tables without duplicate ingestion and
retain complete lineage back to S3.

### Definition of done

- [ ] Development Snowflake database, schemas, roles, warehouse, stage, and
      storage integration are defined reproducibly.
- [ ] Raw JSON loads into a `VARIANT` payload with file and run metadata.
- [ ] Reprocessing an already loaded object creates no duplicate rows.
- [ ] Rejected files and load latency are inspectable.
- [ ] One raw row can be traced to its S3 object and extraction manifest.

## Milestone 6 — dbt transformations

### Outcome

dbt converts raw Kalshi responses into tested staging relations and a minimal
append-only market snapshot mart.

### Definition of done

- [ ] dbt sources declare freshness using ingestion and observation timestamps.
- [ ] Staging models normalize required market fields without discarding raw data.
- [ ] Snapshot grain and uniqueness are explicit and tested.
- [ ] Core not-null, unique, relationship, and accepted-value tests pass.
- [ ] `dbt build` succeeds from documented local and containerized commands.

## Milestone 7 — Monitoring and alerts

### Outcome

Failures, missing successful runs, ingestion lag, and stale modeled data become
visible without manually inspecting several systems.

### Definition of done

- [ ] CloudWatch exposes task failures, duration, and successful-run heartbeat.
- [ ] Absence of a successful extraction beyond the threshold triggers an alert.
- [ ] Load failures or excessive ingestion lag trigger an alert.
- [ ] dbt source freshness failures trigger an alert.
- [ ] A concise operator view links a run across logs, S3, Snowflake, and dbt.
- [ ] Forced failure and stale-data drills deliver notifications successfully.

## Milestone 8 — Production trial

### Outcome

The pipeline operates through several real NFL slates, and the operator can
detect, explain, and repair a missing-data interval.

### Definition of done

- [ ] Production and development identities, data, schedules, and secrets are separated.
- [ ] Several NFL slates complete with documented success and freshness evidence.
- [ ] At least one backfill is run safely without creating duplicates.
- [ ] A recovery drill is documented in an operator runbook.
- [ ] Known gaps, costs, and the decision about polling frequency are recorded.
- [ ] The milestone demonstration is reviewed before adding another provider.

## Explicitly later

- FanDuel and DraftKings collection
- WebSocket or sub-hourly market capture
- S3 Parquet/silver layer
- Prefect or Airflow orchestration
- Website, external API, projections, and trading functionality
- Multi-agent automation and autonomous merging
