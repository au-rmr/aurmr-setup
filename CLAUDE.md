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

## Known gaps in the tool itself

- `aurmr lock` (`core/workspace.py`) chmod's the env and `src/` read-only,
  but there is no `aurmr unlock` — refreshing trunk currently needs a
  manual `chmod -R +w` before `aurmr update` and re-locking after.
- `aurmr update` runs `git pull -r` across every repo in `src/` with no
  dirty check — only safe to run when the workspace is actually clean.
