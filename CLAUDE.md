# aurmr-setup workflow

This repo drives the `aurmr` CLI, which manages per-task workspaces (one conda
env + one catkin workspace each) on inter and emmons. Full rationale and a
worked example: https://claude.ai/code/artifact/e4d804ad-89ea-4996-a1e4-1fbefa86b431
("The Overlay Protocol").

## The rule

**Packages are the unit of record. Workspaces are disposable.** The actual
code (`aurmr_tahoma`, `cartesian_controllers`, etc.) is ordinary git under
`au-rmr/` on GitHub. The workspace directory around it (conda env + catkin
`build`/`devel`) is scaffolding — it should be safe to delete and regenerate
from git at any time. If work only exists as an uncommitted diff in a
workspace, it does not count as done or as safe.

## Steady state

1. **One locked trunk workspace per shared package**, tracking `main`,
   nobody edits it directly (`aurmr lock`).
2. **Start new work with `aurmr clone` from trunk**, not by copying someone
   else's workspace — `clone` does `conda create --clone` + `rsync` of the
   whole tree *including `.git`*, so cloning a dirty workspace propagates
   its branch and uncommitted state. Clone from clean.
3. **Branch immediately** inside the package (`yourname/thing`) and
   **push at every stopping point**, even mid-feature.
4. **Merge small, within about a week**, via PR reviewed by one of the
   other two.
5. **`aurmr archive` the workspace once its branch merges.** A workspace
   should never outlive the branch it was created for.
6. **Hardware/end-effector variants live in trunk as sibling packages**
   selected at bringup (xacro/launch args), not as separate long-lived
   workspaces — see `aurmr_vacuum_gripper` / `robotiq/*` coexisting in
   `aurmr_tahoma`, and `tahoma_bringup/launch/gripper_seperate.launch` as
   the composition point. A workspace like `capacitive_cup` should
   ultimately just be "the capacitive gripper package, selected as an
   argument," not a permanent fork.

## New workspace vs. branch in place

A new workspace (via `aurmr clone`) isn't free — it's another conda env and
another `build`/`devel` to eventually clean up. Default to branching inside
a workspace you already have; only clone a new one when at least one is true:

- **You need it to run concurrently** with something you already have
  active/built — e.g. a demo running on one branch while you calibrate
  against another, or nodes on inter and emmons operating at the same time.
- **The task needs a different dependency flavor** than what's currently
  checked out (different CUDA/Python/ROS distro) — clone from the trunk
  built for *that* flavor, not your default one.
- **You want to sandbox risky/experimental installs** without touching a
  workspace you're relying on for something else.

None of those true? Branch in place, rebuild, keep going — don't spin up a
new workspace per small task. That habit is most of why `~/workspaces` has
30+ entries per machine today.

A brand-new dependency-flavor *trunk* (as opposed to a personal workspace)
is rarer still and should be a deliberate, discussed decision, not something
one person does mid-task: only when two packages have a proven, unavoidable
conflict that can't coexist in one conda env, and the split is durable
enough to maintain long-term. At runtime, nodes from different trunks still
form one ROS graph — each is launched from a terminal that has sourced the
workspace built for its flavor (`activate trunk_x`, then `rosrun`/`roslaunch`
just the nodes belonging to that flavor), all pointed at the same
`ROS_MASTER_URI`. Packages that don't belong in a given flavor's build can
carry a `CATKIN_IGNORE` file so `catkin build` skips them there.

## Known gaps in the tool itself

- `aurmr lock` (`core/workspace.py`) chmod's the env and `src/` read-only,
  but there is no `aurmr unlock` — refreshing trunk currently needs a
  manual `chmod -R +w` before `aurmr update` and re-locking after.
- `aurmr update` runs `git pull -r` across every repo in `src/` with no
  dirty check — only safe to run when the workspace is actually clean.
