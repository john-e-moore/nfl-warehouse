# Work board

Keep exactly one primary item in **Today**. New ideas go to **Parking lot** and
are not decomposed unless they become part of the current milestone.
Before beginning a newly current milestone, decompose only that milestone into
small, ordered tasks with acceptance checks, then move one task into **Today**.
Explicitly requested small one-off changes outside the roadmap do not become
board items and follow the lightweight `main` workflow defined in `AGENTS.md`.

## Today

- M2-T1 — Define the raw output contract for immutable Kalshi response
  artifacts and run manifests.
  - Acceptance: a versioned, reviewable contract defines the partitioned
    payload/manifest key grammar, exact-response byte boundary, immutability,
    checksums, required manifest fields, and the reliability metadata deferred
    to Milestone 3.

## Next

- M2-T2 — Build raw payload and manifest artifacts.
  - Acceptance: offline, fixture-backed artifact construction deterministically
    produces lossless compressed payloads, collision-safe keys, and verifiable
    manifests without AWS configuration.
- M2-T3 — Provision development S3 infrastructure.
  - Acceptance: Terraform defines a protected development bucket and
    least-privilege writer identity, with reviewed local configuration and safe
    operating instructions.
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

## Parking lot

- Decide the higher-frequency collection strategy after observing hourly data.
- Evaluate sportsbook collection rights and technical constraints after Milestone 8.
- Revisit orchestration only when cross-provider dependencies justify it.

## End-of-session handoff

**Result:** Milestone 2 decomposed; M2-T1 is active

**Evidence:** M2-T1 through M2-T4 now have ordered scope and acceptance checks.
Only M2-T1 is in Today; its dedicated branch is
`milestone-2/raw-output-contract`.

**Next smallest step:** Define and review the M2 raw artifact contract. Do not
begin M2-T2 artifact construction or any AWS work.

**Unexpected discoveries:** None yet
