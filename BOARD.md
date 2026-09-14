# Work board

Keep exactly one primary item in **Today**. New ideas go to **Parking lot** and
are not decomposed unless they become part of the current milestone.

## Today

None — M1-T1 is complete; the next task remains queued below.

## Next

- M1-T2 — Add the read-only live Kalshi client behind the same application boundary.
- M1-T3 — Implement and test pagination, including empty and terminal cursors.
- M1-T4 — Finish Milestone 1 developer commands, typing, linting, and clean-checkout demonstration.

## Blocked

None.

## Done

- Project roadmap, architecture, specification, decision record, and working conventions created.
- M1-T1 — Bootstrap the package and parse one fixture. A fresh Python 3.12
  environment installed the package, the offline CLI parsed the committed
  fixture into one typed market record, and the valid/malformed parser tests
  passed.

## Parking lot

- Decide the higher-frequency collection strategy after observing hourly data.
- Evaluate sportsbook collection rights and technical constraints after Milestone 8.
- Revisit orchestration only when cross-provider dependencies justify it.

## End-of-session handoff

**Result:** M1-T1 complete

**Evidence:** `python3.12 -m venv <temporary-dir>`, `pip install --no-deps -e .`,
`python -m unittest discover -s tests -v` (2 tests passed), and the installed
`kalshi-markets --fixture fixtures/kalshi_markets.json` command returned
`parsed 1 typed market records`. `git diff --check` passed.

**Next smallest step:** M1-T2 — add the explicitly selected, read-only live
Kalshi client behind the existing parser boundary. Do not begin it as part of
this handoff.

**Unexpected discoveries:** None yet
