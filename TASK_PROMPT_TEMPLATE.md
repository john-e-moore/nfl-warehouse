Use this prompt for roadmap milestone/task work. Small one-off requests outside
the roadmap follow the lightweight `main` workflow in AGENTS.md instead.

Read AGENTS.md and the project-control files it references. Work only on the
next milestone task from BOARD.md.

If no task is active because a new milestone has become current, first
decompose only that milestone into small, ordered tasks with acceptance checks
in BOARD.md. Do not implement milestone work until one decomposed task is in
**Today**.

Before editing, run git status and confirm you are on the dedicated task branch,
not main. Record the branch/worktree and a small commit plan in PLANS.md.

Implement the task in independently useful slices. After each slice passes its
relevant checks, review and commit it before starting the next slice. Do not
accumulate the whole task into one commit. Do not merge.

If a milestone has been completed, update README.md.

At completion, run the full relevant checks, update BOARD.md and PLANS.md, commit
the handoff, and report all commit SHAs and the final working-tree status. 

Push the completed branch to the remote repository and create a draft PR. Then stop so that I (human) can review the PR.

Only complete a single milestone/task; do not start the next one.
