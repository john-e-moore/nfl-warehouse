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
3. Create a new branch/worktree from the resulting clean `main` commit.
4. Start Codex in the worktree and ask it to summarize the active instructions.
5. Ask it to complete only `M1-T1` in `BOARD.md`, verify the acceptance checks,
   and leave an end-of-session handoff.
6. Review the diff and evidence before committing the implementation.

Suggested first prompt:

```text
Read AGENTS.md and the project-control files it references. Work only on M1-T1
from BOARD.md. Before editing, restate the outcome, acceptance checks, and
non-goals. Implement the smallest coherent solution, run the relevant checks,
and update BOARD.md and PLANS.md with verification evidence and the next smallest
step. Do not start M1-T2.
```

`PLANS.md` is a project convention, not a filename Codex automatically discovers.
It becomes part of the workflow because root `AGENTS.md` explicitly requires it.

