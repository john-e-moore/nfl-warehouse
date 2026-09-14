# Drop-in project-control files

Copy the contents of this directory into the root of the Git repository while
preserving paths. Review before overwriting an existing `.gitignore`,
`.env.example`, or issue template.

## What each file does

| File | Purpose |
| --- | --- |
| `AGENTS.md` | Automatically discovered repository-wide instructions for Codex |
| `ROADMAP.md` | Eight durable outcomes and definitions of done |
| `BOARD.md` | One active daily task, short queue, and parking lot |
| `PLANS.md` | Current non-trivial execution plan and handoff template |
| `docs/architecture.md` | Target architecture, boundaries, and data layers |
| `docs/architecture.mmd` | Standalone Mermaid source |
| `docs/specs/kalshi-ingestion.md` | Functional, data, security, and acceptance requirements |
| `docs/decisions/0001-initial-platform.md` | Why the initial stack was chosen |
| `.github/ISSUE_TEMPLATE/task.md` | Repeatable small-task issue template |
| `.gitignore` | Initial secret, data, Python, dbt, and Terraform exclusions |
| `.env.example` | Empty configuration names; never place real secrets here |

## Initial workflow

1. Copy and review these files.
2. Commit them to `main` and push.
3. Create a dedicated task branch, preferably in a separate worktree, from the
   resulting clean `main` commit. For example:

   ```bash
   git worktree add ../nfl-warehouse-m1-t1 -b milestone-1/package-fixture-parser main
   cd ../nfl-warehouse-m1-t1
   ```

4. Start Codex from that worktree. Do not start implementation from the checkout
   of `main` and rely on the agent to notice later.
5. Ask it to complete only `M1-T1` in `BOARD.md`, verify the acceptance checks,
   commit each coherent passing slice as it finishes, and leave an end-of-session
   handoff.
6. Review the commit series, final diff against `main`, and verification evidence
   before pushing or merging.

Suggested first prompt:

```text
Read AGENTS.md and the project-control files it references. Work only on M1-T1
from BOARD.md. Before editing, run git status, confirm you are on the dedicated
task branch (not main), and record the branch/worktree plus a small commit plan
in PLANS.md. If you are on main, create or switch to the task branch before
changing files; if existing changes make that unsafe, stop and ask me. Restate
the outcome, acceptance checks, and non-goals. Implement the smallest coherent
solution. After each independently useful slice passes its relevant checks,
review and commit that slice before starting the next one; do not wait until the
whole task or milestone is finished. Do not push or merge. Run the full relevant
checks at the end, then update BOARD.md and PLANS.md with verification evidence,
completed commit subjects, working-tree status, and the next smallest step.
Commit that handoff, then report every resulting short SHA. Do not start M1-T2.
```

For later tasks, replace the task ID and branch name but retain the branch check,
commit-plan, incremental-commit, no-push/no-merge, and handoff language. A branch
is sufficient for sequential work; a separate worktree is preferable when you
want to keep `main` available or run more than one task concurrently.

`PLANS.md` is a project convention, not a filename Codex automatically discovers.
It becomes part of the workflow because root `AGENTS.md` explicitly requires it.
