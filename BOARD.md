# Work board

Keep exactly one primary item in **Today**. New ideas go to **Parking lot** and
are not decomposed unless they become part of the current milestone.
Before beginning a newly current milestone, decompose only that milestone into
small, ordered tasks with acceptance checks, then move one task into **Today**.

## Today

None — M1-T4 is complete; Milestone 1 is ready for review.

## Next

- M2-T1 — Define the development S3 output boundary and immutable object
  convention.

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

**Result:** M1-T4 complete; Milestone 1 complete

**Evidence:** In a detached clean checkout and fresh Python 3.12 virtual
environment, `pip install -e '.[dev]'` succeeded. Ruff formatting/linting,
mypy, and `python -m unittest discover -s tests -v` all passed; the suite ran
12 tests. The installed fixture command returned `parsed 1 typed market
records`. No credentials or live access are needed for the default suite.
`git diff --check` passed.

**Next smallest step:** M2-T1 — define the development S3 output boundary and
immutable object convention. Do not begin it as part of this handoff.

**Unexpected discoveries:** None yet
