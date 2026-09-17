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

## Current execution plan — M1-T3

### Outcome

The read-only Kalshi client retrieves every markets page for a requested series,
validates each envelope, and stops only at a valid terminal cursor.

### Non-goals

- Retry/backoff policy, structured logging, or partial-run metadata
- Persistence outside the local process
- AWS, Snowflake, dbt, containers, or CI deployment
- A generalized framework for hypothetical providers

### Steps

- [x] Inspect the existing client/parser boundary and the M1 pagination
      requirements.
- [x] Add cursor-envelope validation and multi-page retrieval through the
      existing public client boundary.
- [x] Add local-server tests for cursor propagation, terminal cursors, empty
      results, and invalid cursor envelopes.
- [ ] Run the full local suite and record completion evidence.
- [ ] Update the board and plan handoff for M1-T4.

### Git workspace

- Branch: `milestone-1/paginate-markets`
- Worktree: `/home/john/nfl-warehouse`

### Commit plan

- [x] `feat: validate Kalshi markets pagination cursors` — page-envelope
      validation and parser tests; verify with
      `PYTHONPATH=src /usr/bin/python3.12 -m unittest discover -s tests -p 'test_markets.py' -v`.
- [x] `feat: paginate Kalshi markets retrieval` — multi-page client retrieval
      and local-server coverage; verify with
      `PYTHONPATH=src /usr/bin/python3.12 -m unittest discover -s tests -p 'test_client.py' -v`.
- [ ] `docs: hand off pagination task` — board/plan completion evidence; verify
      with `git diff --check` and the full local test suite.

### Decisions

- Preserve the existing `fetch_markets` list-returning application boundary;
  make it aggregate validated page records rather than exposing transport
  envelopes to the CLI.
- Treat only an empty cursor string as terminal. Missing or wrongly typed cursor
  fields are validation failures, so an incomplete retrieval can never look
  successful.

### Discoveries

- The committed fixture already represents a terminal cursor as an empty
  string, matching the required terminal-cursor test coverage.

### Verification evidence

- Pending implementation.

### Handoff

- Status: in progress
- Commit subjects: pending
- Working tree: expected to be clean after each commit
- Next action: implement validated cursor-envelope parsing and aggregation.

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
