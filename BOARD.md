# Work board

Keep exactly one primary item in **Today**. New ideas go to **Parking lot** and
are not decomposed unless they become part of the current milestone.
Before beginning a newly current milestone, decompose only that milestone into
small, ordered tasks with acceptance checks, then move one task into **Today**.
Explicitly requested small one-off changes outside the roadmap do not become
board items and follow the lightweight `main` workflow defined in `AGENTS.md`.

## Today

None — M2-T3 is complete; M2-T4 is ready for a separately reviewed task.

## Next

- M2-T4 — Persist to S3 and verify read-back.
  - Acceptance: an explicitly selected S3 path writes immutable payloads then
    a manifest, rejects collisions, is fake-tested, and has one authorized
    development read-back demonstration.

## Blocked

None.

## Done

- Project roadmap, architecture, specification, decision record, and working conventions created.
- M1-T1 — Bootstrap the package and parse one fixture. A fresh Python 3.12
  environment installed the package, the offline CLI parsed the committed
  fixture into one typed market record, and the valid/malformed parser tests
  passed.
- M1-T2 — Add the read-only live Kalshi client behind the same application
  boundary. The explicit `--live` CLI mode retrieved and validated a single
  public Kalshi markets page without reading or emitting credentials.
- M1-T3 — Implement and test pagination, including empty and terminal cursors.
  The live client aggregates every validated page, passes each cursor once,
  terminates at an empty cursor, and rejects malformed or repeated cursors.
- M1-T4 — Finish developer commands, typing, linting, and clean-checkout
  demonstration. A detached clean checkout installed the pinned `dev` extra
  under Python 3.12, passed Ruff formatting/linting, mypy, all 12 offline tests,
  and the fixture CLI demonstration.
- M2-T1 — Define the raw output contract for immutable Kalshi response
  artifacts and run manifests. The versioned contract defines the partitioned
  key grammar, source-byte and persisted-byte checksum boundaries, create-only
  publication semantics, successful-run manifest schema, and M3 deferrals.
- M2-T2 — Build raw payload and manifest artifacts. The client captures exact
  response bytes before decoding, and offline construction deterministically
  produces lossless gzip payloads, contract keys, checksums, and verifiable
  manifests from supplied run metadata without AWS configuration.
- M2-T3 — Provision development S3 infrastructure. Terraform defines an
  isolated development bucket with public-access blocks, enforced ownership and
  encryption, versioning and Object Lock protections, and a create-only,
  prefix-scoped writer role; review-first operational instructions keep state,
  credentials, and environment-specific values out of the repository.

## Parking lot

- Decide the higher-frequency collection strategy after observing hourly data.
- Evaluate sportsbook collection rights and technical constraints after Milestone 8.
- Revisit orchestration only when cross-provider dependencies justify it.

## End-of-session handoff

**Result:** M2-T3 complete; Milestone 2 remains in progress

**Evidence:** Terraform 1.8.5 passed `fmt -check` and `validate` with locked
AWS provider 5.100.0. The Terraform configuration creates one development-only
bucket, protection resources, bucket policy, and constrained writer role/policy;
it does not apply anything. Ruff format/check, mypy, all 18 offline unit tests,
the fixture CLI (`parsed 1 typed market records`), and `git diff --check`
passed. An authorized AWS identity exists locally, but no remote Terraform-state
backend or approved environment-specific input was supplied, so no actual
development-account plan or apply was run.

**Next smallest step:** M2-T4 — implement only the explicitly selected S3
persistence/read-back path against the writer role. First initialize the
approved remote Terraform state backend, review the real development plan, and
apply it through the documented review-first procedure. Do not begin M2-T4 as
part of this handoff.

**Unexpected discoveries:** A Terraform root with an intentionally unconfigured
S3 backend cannot produce a plan after `init -backend=false`; a real plan needs
the approved remote backend configuration and local `development.tfvars`.
