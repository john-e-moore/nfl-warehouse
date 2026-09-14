# Repository instructions

## Mission

Build a production-minded, maintainable data platform that captures append-only
market observations, beginning with Kalshi NFL markets. The repository owns data
engineering only. A website, public API, projections model, trading system, and
additional sportsbooks are outside the initial scope.

The current source of truth is, in order:

1. The task explicitly requested by the user.
2. `BOARD.md` for the one active task.
3. `docs/specs/kalshi-ingestion.md` for product and data requirements.
4. `ROADMAP.md` for milestone order and definitions of done.
5. `docs/decisions/` for accepted architectural decisions.
6. `docs/architecture.md` for the intended system shape.

If these conflict, stop and explain the conflict before changing code.

## Scope discipline

- Work on only the item under `BOARD.md` > `Today`, unless the user explicitly
  changes the task.
- Do not implement later milestones early merely because their future interfaces
  are visible.
- Capture attractive but unnecessary ideas under `BOARD.md` > `Parking lot`.
- Prefer the smallest vertical slice that satisfies the active acceptance checks.
- Do not introduce an abstraction until the current requirement needs it or a
  second concrete use case proves it.
- Do not add Airflow, Prefect, Kubernetes, streaming infrastructure, a web app,
  or sportsbook scrapers during Milestones 1-8 unless the roadmap is explicitly
  amended.

## Working protocol

Before editing:

1. Read `BOARD.md`, the relevant milestone in `ROADMAP.md`, and the applicable
   spec or decision record.
2. Inspect the repository and existing changes. Preserve unrelated user work.
3. Run `git status --short --branch` and verify the work is on a dedicated task
   branch, not `main`. If still on `main`, create or switch to a branch/worktree
   named for the active task before changing files. If existing changes make
   that unsafe, stop and ask the user how to preserve them.
4. State the active outcome, acceptance checks, and anything intentionally not
   included.
5. For a non-trivial task, create or update the current execution plan using
   `PLANS.md`. Include proposed commit boundaries, but do not plan future
   milestones in detail.

While editing:

- Make small, reviewable changes.
- Treat each independently useful, verified slice as a commit boundary. Commit
  it before beginning the next slice; do not accumulate an entire task or
  milestone into one final commit.
- Keep tests and documentation that establish one behavior in the same commit
  as that behavior. Separate unrelated refactors, formatting, and documentation.
- Before each commit, inspect the staged diff, run the smallest relevant check,
  and stage only files belonging to that slice. Do not create knowingly broken
  checkpoint commits.
- Keep source retrieval, validation, persistence, and orchestration separable.
- Preserve original source responses before normalization once persistence is in
  scope.
- Make reruns safe. Prefer deterministic identifiers and idempotent writes.
- Use UTC for stored timestamps; retain source timestamps separately.
- Never log credentials, private keys, authorization headers, or full secrets.
- Never commit `.env` files, credentials, generated raw market data, Terraform
  state, dbt targets, or local caches.
- Ask before adding a paid service, a production dependency with substantial
  operational impact, or a change that expands project scope.

Before declaring completion:

1. Run the smallest relevant checks, followed by the full available local test
   suite when practical.
2. Confirm every acceptance check with concrete evidence.
3. Review the diff for secrets, generated files, accidental scope expansion, and
   unrelated changes.
4. Update `BOARD.md` and `PLANS.md` to leave a precise handoff, including the
   task branch/worktree and completed commit subjects. Move an item to
   Done only when its checks actually pass.
5. Do not mark a roadmap milestone complete unless its milestone demonstration
   succeeds end to end.
6. Report any intentionally uncommitted changes. A completed task should
   normally have a clean worktree. In the final response, list every commit with
   its short SHA, including the final handoff commit.

## Engineering expectations

- Target Python 3.12 unless the repository establishes another supported version.
- Prefer a `src/` package layout, type annotations, explicit interfaces at
  external boundaries, and small modules.
- Use fixture-backed tests for external APIs. Unit tests must not require live
  network access.
- Keep one optional, explicitly selected live integration path; never make live
  credentials a prerequisite for the default test suite.
- Validate external response envelopes and required fields. Preserve unknown
  fields in raw data rather than silently dropping them.
- Bound retries, use exponential backoff with jitter for retryable failures, and
  distinguish retryable errors from permanent validation failures.
- Treat pagination completeness as part of correctness.
- Prefer structured logs containing `run_id`, provider, entity, timestamps,
  record counts, page counts, byte counts, status, and error category.
- Pin direct dependencies and commit the lockfile once package tooling exists.
- Favor boring, widely supported components and readable code over cleverness.

## Testing and review

Tests should cover, as applicable:

- successful fixture parsing;
- malformed or incomplete responses;
- empty-but-valid responses;
- pagination and cursor termination;
- timeouts, retryable status codes, and rate limiting;
- deterministic object names and idempotent reruns;
- secret redaction from logs and errors.

Do not weaken or delete a test simply to make a change pass. If a test encodes an
obsolete requirement, explain and update the requirement and test together.

## Git workflow

- Use one dedicated branch per narrowly scoped issue; use a separate worktree
  as well when concurrent or isolated work would benefit from it.
- Never edit or commit task work on `main` unless the user explicitly requests
  that exception. Merely starting the session on `main` is not permission.
- Local commits are part of implementation work unless the user explicitly asks
  for uncommitted changes. Commit after each coherent, passing slice rather than
  once at task or milestone completion.
- Keep commits cohesive and reviewable. Avoid mixing unrelated behavior,
  refactors, formatting, or project-control updates.
- Before starting, record the intended branch name and commit slices in
  `PLANS.md`; revise them when discoveries change the sequence.
- Do not push, merge, create a pull request, or alter remote infrastructure unless
  explicitly asked.
- Suggested branch format: `milestone-<n>/<short-task-name>`.

## Documentation

- Record durable architecture choices as short ADRs under `docs/decisions/`.
- Update the ingestion spec when externally observable behavior changes.
- Update the architecture diagram when component relationships change.
- Keep transient work notes in `PLANS.md`; do not turn `AGENTS.md` into a backlog.
