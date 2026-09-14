# Execution plans

This file is a lightweight working record, not a second roadmap. `ROADMAP.md`
owns milestone outcomes; `BOARD.md` owns the active task.

## When to write a plan

Write or update the current plan when a task:

- changes several files or boundaries;
- requires an architectural choice;
- touches cloud infrastructure, permissions, data contracts, or migrations;
- is likely to take more than one focused session.

For a small, obvious edit, the acceptance checks in `BOARD.md` are enough.

## Planning rules

- Plan only the active board item in executable detail.
- Keep steps independently verifiable.
- Name the task branch and, when used, the worktree path before editing.
- Group steps into small commit slices. Each slice should leave the branch in a
  working state and state the check that must pass before committing.
- Include explicit non-goals.
- Record decisions and discoveries as they occur.
- Replace this current plan when the board advances; durable decisions belong in
  `docs/decisions/`.
- A checked box means evidence exists, not merely that code was written.

## Current execution plan — M1-T2

### Outcome

An explicitly selected CLI mode retrieves a read-only Kalshi markets response
and validates it through the same parser used by fixture mode.

### Non-goals

- Pagination or multi-page aggregation
- Retry/backoff policy and structured logging
- Persistence outside the local process
- AWS, Snowflake, dbt, containers, or CI deployment
- A generalized framework for hypothetical providers

### Steps

- [x] Inspect the existing parser/CLI, live-configuration placeholders, and
      the M1 source-boundary requirements.
- [x] Add a read-only HTTP client that reads only non-secret configuration from
      the environment and passes successful JSON through `parse_markets_response`.
- [x] Extend the CLI with explicit, mutually exclusive fixture and live modes.
- [x] Add local-server tests for request shape, successful validation, and safe
      failure handling without requiring live credentials or network access.
- [x] Run the full local suite and one optional live command, then record
      completion evidence.
- [x] Update the board and plan handoff for M1-T3.

### Git workspace

- Branch: `milestone-1/live-kalshi-client`
- Worktree: `/home/john/nfl-warehouse`

### Commit plan

- [x] `feat: add read-only Kalshi markets client` — client, CLI live mode, and
      fixture-backed/local-server tests; verify with `python -m unittest discover -s tests -v`.
- [x] `docs: hand off live client task` — board and plan evidence; verify with
      `git diff --check` and the full local test suite.

### Decisions

- Keep the live transport in a dedicated standard-library module so the parser
  remains deterministic and independently testable.
- Require an explicit `--live` selector; fixture mode remains network-free and
  usable without credentials.

### Discoveries

- `.env.example` reserves `KALSHI_API_BASE_URL`, `KALSHI_API_KEY_ID`, and
  `KALSHI_PRIVATE_KEY_PATH`, but no runtime configuration or HTTP client exists.

### Verification evidence

- In a fresh Python 3.12 virtual environment, `pip install --no-deps -e .`
  succeeded; `python -m unittest discover -s tests -v` passed 6 tests.
- The installed `kalshi-markets --fixture fixtures/kalshi_markets.json` command
  printed `parsed 1 typed market records` without network access.
- The installed public read-only command `kalshi-markets --live --series-ticker
  KXNFLGAME --limit 1` printed `parsed 1 typed market records`.
- `git diff --check` passed before the implementation commit and before this
  handoff commit.

### Handoff

- Status: complete
- Commit subjects: `feat: add read-only Kalshi markets client`; `docs: hand off live client task`
- Working tree: clean after the handoff commit
- Next action: M1-T3 pagination, empty responses, and terminal cursors.

## Plan template

```md
## Current execution plan — <task ID>

### Outcome

<One observable capability>

### Non-goals

- <Explicitly deferred work>

### Steps

- [ ] <Small verifiable step>

### Git workspace

- Branch: `milestone-<n>/<short-task-name>`
- Worktree: <path, or "not used">

### Commit plan

- [ ] `<type>: <cohesive slice>` — includes <files/behavior>; verify with
      `<smallest relevant command>`

### Decisions

- <Decision and rationale>

### Discoveries

- <Unexpected fact affecting the plan>

### Verification evidence

- <Command, test result, object, query, or screenshot>

### Handoff

- Status: <not started | in progress | blocked | complete>
- Commit subjects: <subject for each completed slice>
- Working tree: <clean, or list and explain intentional uncommitted changes>
- Next action: <smallest concrete action>
```
