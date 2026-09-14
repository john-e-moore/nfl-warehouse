# Work board

Keep exactly one primary item in **Today**. New ideas go to **Parking lot** and
are not decomposed unless they become part of the current milestone.

## Today

### M1-T1 — Bootstrap the package and parse one fixture

**Finish line:** A deterministic local command parses a committed Kalshi markets
fixture into typed records without network access.

**Acceptance checks:**

- [ ] The Python package installs from a clean checkout.
- [ ] The fixture-backed command returns typed market records and a concise count.
- [ ] Tests cover a valid response and a malformed response.

**Not today:**

- Live authentication or pagination
- S3, Docker, AWS, Snowflake, or dbt
- Every Kalshi entity
- Generalization for unimplemented providers

## Next

- M1-T2 — Add the read-only live Kalshi client behind the same application boundary.
- M1-T3 — Implement and test pagination, including empty and terminal cursors.
- M1-T4 — Finish Milestone 1 developer commands, typing, linting, and clean-checkout demonstration.

## Blocked

None.

## Done

- Project roadmap, architecture, specification, decision record, and working conventions created.

## Parking lot

- Decide the higher-frequency collection strategy after observing hourly data.
- Evaluate sportsbook collection rights and technical constraints after Milestone 8.
- Revisit orchestration only when cross-provider dependencies justify it.

## End-of-session handoff

**Result:** Not started

**Evidence:** None yet

**Next smallest step:** Ask the agent to complete only `M1-T1` and verify each acceptance check.

**Unexpected discoveries:** None yet

