# Execution plans

This file is a lightweight working record, not a second roadmap. `ROADMAP.md`
owns milestone outcomes; `BOARD.md` owns the active task.

Explicitly requested small one-off changes outside the roadmap do not need an
execution-plan entry. They follow the lightweight `main` workflow in
`AGENTS.md`.

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

## Current execution plan — Task workflow controls

### Outcome

Agents must decompose a newly current milestone before implementation and push
a verified completed-task branch as a draft pull request for human review.
Explicitly requested small one-off changes outside the roadmap instead use a
local-only `main` workflow.

### Non-goals

- Decomposing or implementing Milestone 2
- Changing roadmap outcomes, infrastructure, or product behavior

### Steps

- [x] Align AGENTS.md, BOARD.md, and the task prompt template with the requested
      workflow; verify their instructions are consistent.
- [x] Commit the project-control update and verify the final working tree.

### Git workspace

- Branch: `chore/task-workflow-controls`
- Worktree: `/home/john/nfl-warehouse`

### Commit plan

- [x] `docs: clarify milestone task and PR workflow` — project-control
      instructions; verify with a focused content review and `git diff --check`.

### Decisions

- A completed, verified task is pushed and opened as a draft PR; merging remains
  an explicit human-authorized action.
- An explicitly requested small one-off change outside the roadmap is committed
  locally on `main`, with no push, pull request, board update, or plan update.
  Ambiguous work defaults to the roadmap/task workflow.
- The board and task template repeat the roadmap's milestone-decomposition gate
  so an agent cannot infer task-level work before it exists.

### Discoveries

- The task template already required a push and draft PR, but AGENTS.md
  contradicted it.

### Verification evidence

- `git diff --check` passed.
- A focused search confirmed that AGENTS.md authorizes the push/draft-PR
  handoff, while BOARD.md and the task template both require new-milestone
  decomposition before implementation.

### Handoff

- Status: complete
- Commit subjects: `docs: clarify milestone task and PR workflow`
- Working tree: clean after the handoff commit
- Next action: decompose Milestone 2 into board tasks before implementation.

## Previous execution plan — M1-T4

### Outcome

A clean checkout can install the package and run documented formatting, linting,
typing, and test commands for the local extraction package.

### Non-goals

- AWS, S3, Snowflake, dbt, containers, CI deployment, or scheduling
- New extraction behavior beyond what is needed for quality checks
- Live credentials or network access in the default verification suite

### Steps

- [x] Inspect the current package and choose minimal pinned developer tooling.
- [x] Add package metadata, developer commands, and source/test quality
      configuration; verify each command in the current checkout.
- [x] Add clean-checkout instructions and a small demonstration script or
      command sequence; verify from a fresh virtual environment.
- [x] Run the complete local checks, update board and handoff evidence, and
      commit the final project-control slice.

### Git workspace

- Branch: `milestone-1/developer-quality`
- Worktree: `/home/john/nfl-warehouse`

### Commit plan

- [x] `build: add pinned developer quality tooling` — package extras and
      formatter/linter/type-check configuration; verify the quality commands.
- [x] `docs: document clean-checkout verification` — developer workflow and
      clean-install demonstration; verify in a fresh Python 3.12 environment.
- [x] `docs: hand off developer quality task` — board/plan completion evidence;
      verify the full suite and clean working tree.

### Decisions

- Use Ruff for formatting and linting and mypy for static typing, exposed as a
  pinned `dev` extra so a clean checkout has one documented installation path.
- Keep unittest as the test runner because the repository already uses the
  standard library and the default suite must remain offline.

### Discoveries

- The repository has no README or developer-tool configuration yet; the package
  and tests already use Python 3.12-compatible annotations.

### Verification evidence

- `29f2d79` quality slice: pinned Ruff/mypy developer extra, project
  configuration, and formatting/import cleanup; Ruff, mypy, unittest, and
  `git diff --check` passed.
- `229d907` documentation slice: clean-checkout workflow and fixture/live CLI
  commands; current-checkout quality checks and tests passed.
- Detached clean-checkout demonstration from `229d907`: Python 3.12 editable
  install, Ruff format/check, mypy, 12 unittest cases, and fixture CLI all
  passed.

### Handoff

- Status: complete
- Commit subjects: `build: add pinned developer quality tooling`,
  `docs: document clean-checkout verification`, and the handoff commit below
- Working tree: clean after the handoff commit
- Next action: M2-T1 development S3 output boundary; do not begin it in this
  task.

## Previous execution plan — M1-T3

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
- [x] Run the full local suite and record completion evidence.
- [x] Update the board and plan handoff for M1-T4.

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
- [x] `docs: hand off pagination task` — board/plan completion evidence; verify
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

- In a fresh Python 3.12 virtual environment, `pip install --no-deps -e .`
  succeeded; `python -m unittest discover -s tests -v` passed all 12 tests.
- The installed `kalshi-markets --fixture fixtures/kalshi_markets.json` command
  printed `parsed 1 typed market records` without network access.
- Local-server tests prove two-page aggregation, correct cursor propagation,
  empty terminal results, malformed-cursor rejection, and repeated-cursor
  failure. `git diff --check` passed.

### Handoff

- Status: complete
- Commit subjects:
  - `feat: validate Kalshi markets pagination cursors`
  - `feat: paginate Kalshi markets retrieval`
  - `docs: hand off pagination task`
- Working tree: clean after the handoff commit
- Next action: M1-T4 developer commands, typing, linting, and clean-checkout
  demonstration. Do not begin it as part of this handoff.

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
