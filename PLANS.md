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
- Include explicit non-goals.
- Record decisions and discoveries as they occur.
- Replace this current plan when the board advances; durable decisions belong in
  `docs/decisions/`.
- A checked box means evidence exists, not merely that code was written.

## Current execution plan — M1-T1

### Outcome

A deterministic local command parses a committed Kalshi markets fixture into
typed records without network access.

### Non-goals

- Live API calls or authentication
- Pagination
- Persistence outside the local process
- AWS, Snowflake, dbt, containers, or CI deployment
- A generalized framework for hypothetical providers

### Steps

- [x] Inspect the repository and select the smallest coherent Python packaging
      setup consistent with existing files.
- [x] Add one sanitized Kalshi markets response fixture representative of the
      response envelope and required fields in the ingestion spec.
- [x] Define the minimum typed model needed to represent those fields while
      preserving a path to the raw response.
- [x] Add a local command that loads the fixture, validates it, and prints a
      concise deterministic summary.
- [x] Test the valid fixture and one malformed response.
- [x] Run documented install and test commands from a clean environment.
- [x] Review the diff for secrets, generated data, and premature scope.
- [x] Update `BOARD.md` with evidence and the next smallest task.

### Decisions

- Use a standard `pyproject.toml` with a `src/` layout and setuptools, with no
  runtime dependencies.
- Expose the fixture command as `kalshi-markets --fixture PATH`; use
  `python -m unittest discover` for dependency-free local verification.
- Represent validated markets with a frozen dataclass and retain the complete
  source market mapping in `raw` so unknown fields are not discarded.

### Discoveries

- The repository was an otherwise clean project-control scaffold: no package,
  fixture, tests, or dependency lockfile existed.

### Verification evidence

- `/usr/bin/python3.12 -m venv <temporary-dir>` created a clean environment.
- `pip install --no-deps -e .` succeeded.
- `python -m unittest discover -s tests -v` passed both tests: valid fixture
  parsing/raw-field preservation and malformed-response rejection.
- Installed `kalshi-markets --fixture fixtures/kalshi_markets.json` printed
  `parsed 1 typed market records` without network access.
- `git diff --check` passed; no secrets, generated raw data, or later-milestone
  infrastructure were added.

### Handoff

- Status: complete
- Next action: M1-T2 is the next smallest board item; it was not started.

## Plan template

```md
## Current execution plan — <task ID>

### Outcome

<One observable capability>

### Non-goals

- <Explicitly deferred work>

### Steps

- [ ] <Small verifiable step>

### Decisions

- <Decision and rationale>

### Discoveries

- <Unexpected fact affecting the plan>

### Verification evidence

- <Command, test result, object, query, or screenshot>

### Handoff

- Status: <not started | in progress | blocked | complete>
- Next action: <smallest concrete action>
```
