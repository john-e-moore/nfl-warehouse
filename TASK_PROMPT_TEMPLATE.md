Read AGENTS.md and the project-control files it references. Work only on {milestone}-{task}
from BOARD.md.

Before editing, run git status and confirm you are on the dedicated task branch,
not main. Record the branch/worktree and a small commit plan in PLANS.md.

Implement the task in independently useful slices. After each slice passes its
relevant checks, review and commit it before starting the next slice. Do not
accumulate the whole task into one commit. Do not push or merge.

At completion, run the full relevant checks, update BOARD.md and PLANS.md, commit
the handoff, and report all commit SHAs and the final working-tree status. Do not
start {milestone}-{next_task}.