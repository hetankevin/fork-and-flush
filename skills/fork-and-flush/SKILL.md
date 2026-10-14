---
name: fork-and-flush
description: Optimize difficult, measurable research or engineering tasks through budgeted fresh-context branches, scored selection, and continued work on the winning lineage. Use for fork-and-flush, autoresearch, or repeated optimization that is stuck in one approach. Avoid routine edits, unscored brainstorming, and tasks with no reproducible evaluator.
---

# Fork and Flush

Preserve useful files while restarting the reasoning trajectory. This skill adapts
[Fork-and-Flush](https://arxiv.org/html/2610.07447v1) to Claude Code and Codex.
It is an agent-operated protocol with deterministic planning and selection helpers,
not a background scheduler. User instructions and execution permissions still apply.

## Establish the experiment

Read the task and repository instructions. Establish the objective, editable scope,
immutable evaluator, score direction, validity checks, starting workspace, total
budget, and budget unit. Prefer an existing benchmark. Do not invent a numerical
score for a subjective task. If the task lacks a meaningful evaluator or a bounded
resource allowance, resolve that with the user before launching the search.

Record these in a run contract outside worker workspaces. Include model/settings,
evaluator version, seeds or repeat policy for noisy measurements, concurrency,
timeouts, and an allowance for setup, coordination, and final verification. Keep
models and tools identical across branches unless the user requests a comparison.
Token/cost metering is preferable. Evaluation counts or summed worker-seconds are
explicit proxies, not equivalent to the paper's credit budget. A wall deadline
alone does not account for concurrent spend. Enforce limits in the host where
possible, and disclose when only cooperative limits are available.

Read [the runtime adapters](references/runtimes.md) before launching agents.
Read [the record format](references/records.md) before creating score records.
Resolve helper paths relative to this SKILL.md, not the task's working directory.

## Run the fixed schedule

1. Snapshot the starting workspace without losing uncommitted user work. Put
   each worker in a separate checkout or copied workspace. Preserve required
   ignored assets explicitly. Keep the evaluator outside worker write scope when
   the runtime permits. Save the baseline's verified artifact and evidence.
2. Generate the schedule with `python3 scripts/control.py plan --budget B
   --overhead H`. The defaults use four branches, three exploration rounds at
   0%, 33%, and 66% of the search allowance, and 6% per branch per round.
   `H` is reserved from the total `B` before planning. Do not spend this reserve
   on additional search. Small budgets that cannot support the schedule fail.
3. Start the opening K workers from identical base files and fresh contexts.
   For an existing project, those base files include its existing implementation.
   Each worker gets the same task contract and its assigned allowance. Do not
   pass the parent's conversation, reasoning summary, favorite hypothesis, or
   other workers' messages. A fresh context still receives required system,
   user, and repository instructions. Use the brief below.
4. At the round boundary, stop and account for every worker, including failures.
   Independently evaluate its candidate checkpoints with the frozen evaluator.
   Record every valid improvement and retain its exact immutable artifact.
   Use `select` over this round's records plus the inherited incumbent. Select
   by best verified score attained in a lineage, not its last edited file or
   its prose report. Invalid artifacts cannot win. Ties retain the incumbent,
   then use stable lineage/checkpoint identifiers. This tie rule is an adaptation.
5. Continue the winning worker in its existing conversation and isolated
   workspace for the exploitation allocation. Restore its best verified
   checkpoint if necessary and tell that worker what was restored. Preserve
   required surrounding workspace files. A new conversation here would add an
   extra flush, so label that fallback if session resumption is unavailable.
   If the inherited incumbent remains best, restore it in a surviving fresh
   worker chosen by stable worker ID and continue that worker. Do not resume
   the pre-flush parent, which would undo the intended context reset. If no
   worker can continue, stop with the incumbent or disclose a fresh restart.
6. At the next scheduled fork, snapshot the leader's accumulated workspace and
   start K new fresh-context workers from that same snapshot. Keep the verified
   incumbent available to all. Repeat selection and exploitation within the
   budget. Do not wait for a plateau to trigger the scheduled intervention.
7. Return the best verified artifact discovered anywhere in the run, including
   pruned lineages. Re-evaluate it using the reserved allowance, integrate only
   the winning change into the user's working tree, and run relevant checks.
   Preserve unrelated work and report any unresolved conflict. Keep evidence
   before retiring workers or cleaning up workspaces.

The coordinator maintains the global ledger and best-ever artifact separately
from the active leader. Charge actual costs once for every worker, retries, and
coordination. Never treat K concurrent workers as one worker's cost. Do not
launch an allocation that exceeds the remaining allowance. If an episode
overshoots, cancel queued work and reduce later allocations, then report the
actual spend and schedule deviation. Stop at the budget, user cancellation,
a verified target, or an evaluator/infrastructure failure that prevents reliable
selection. If all new candidates fail, retain the verified incumbent. If none
exists, report failure rather than manufacturing a winner.

## Worker brief

Populate only task facts and resource limits, using the same brief for each branch:

> Work independently on [objective] in [isolated workspace]. Follow the user and
> repository instructions. Improve [metric, direction] subject to [constraints].
> Evaluate with [fixed command/version/seeds]. Your allocation is [amount/unit]
> with [deadline/host limit]. The inherited verified checkpoint is [identifier,
> score, evidence] or there is no verified incumbent. Preserve it. Explore and
> test approaches within this allocation. Save exact candidate checkpoints and
> evaluator outputs, and report actual resource use. Do not change the evaluator
> or read sibling workspaces. Stop when the allocation is exhausted. Return
> checkpoint paths, measurements, validity evidence, and remaining artifacts.

Workspace notes may survive a flush, as in the paper. Do not erase project
instructions to simulate a blank context. Keep orchestration transcripts and
speculative reasoning summaries outside the inherited workspace so the
coordinator does not deliberately reintroduce the flushed conversation.

## Helpers and reporting

```sh
python3 scripts/control.py plan --budget 1000 --overhead 100
python3 scripts/control.py select /absolute/path/round.json --direction max
```

Helpers only plan and rank records. They do not spawn agents, meter tokens,
verify grader honesty, or move files. The coordinator performs those actions.
For noisy objectives, evaluate with a fixed repeat policy and record the same
aggregate for every candidate. Keep held-out tests out of adaptive selection.

Report baseline and final scores, metric/direction, exact artifact and evidence,
actual budget use, the selected lineage, validation, and material deviations
(fewer branches, sequential waves, proxy budgets, extra flushes, noisy scoring).
Distinguish completed experiments from planned ones. Do not claim the paper's
performance gains for this skill. See [method and attribution](references/method.md)
for the paper-to-implementation mapping and limitations.
