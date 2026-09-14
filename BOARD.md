# Work board

Keep exactly one primary item in **Today**. New ideas go to **Parking lot** and
are not decomposed unless they become part of the current milestone.

## Today

None — M1-T2 is complete; the next task remains queued below.

## Next

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
- M1-T2 — Add the read-only live Kalshi client behind the same application
  boundary. The explicit `--live` CLI mode retrieved and validated a single
  public Kalshi markets page without reading or emitting credentials.

## Parking lot

- Decide the higher-frequency collection strategy after observing hourly data.
- Evaluate sportsbook collection rights and technical constraints after Milestone 8.
- Revisit orchestration only when cross-provider dependencies justify it.

## End-of-session handoff

**Result:** M1-T2 complete

**Evidence:** In a fresh Python 3.12 virtual environment, `pip install --no-deps
-e .` succeeded and `python -m unittest discover -s tests -v` passed all 6
tests. The installed fixture command returned `parsed 1 typed market records`.
The explicitly selected, public read-only command
`kalshi-markets --live --series-ticker KXNFLGAME --limit 1` also returned
`parsed 1 typed market records`. Tests use a local HTTP server for request
shape, parser-boundary validation, and response-body redaction; no credentials
or live access are needed for the default suite. `git diff --check` passed.

**Next smallest step:** M1-T3 — implement and test cursor pagination, including
empty results and terminal cursors. Do not begin it as part of this handoff.

**Unexpected discoveries:** None yet
