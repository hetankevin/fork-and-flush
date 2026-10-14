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

Record these in a coordinator-only run contract outside worker workspaces.
Use a fixed total model-usage budget B, summed across all search workers. The
paper uses compute credits that are a fixed function of input/output tokens.
Use metered credits with a documented conversion, metered token-derived cost,
or an explicitly chosen input-plus-output token budget. Keep the model,
reasoning-effort setting, tools, and task prompt fixed across workers. Reasoning
effort is a model setting, not the resource budget. Never silently substitute
elapsed time or evaluator-call counts for model usage.

Record the meter, token categories, conversion/rates, evaluator version, seeds
or repeat policy, and concurrency. Read [budget accounting](references/budgets.md)
for units, episode boundaries, and missing-meter handling. Budget allocations and
remaining balances belong to the coordinator, not worker prompts. The host must
meter and control episodes without relying on workers to self-estimate tokens.

Read [the runtime adapters](references/runtimes.md) before launching agents.
Read [the record format](references/records.md) before creating score records.
Resolve helper paths relative to this SKILL.md, not the task's working directory.

## Run the fixed schedule

1. Snapshot the starting workspace without losing uncommitted user work. Put
   each worker in a separate checkout or copied workspace. Preserve required
   ignored assets explicitly. Keep the evaluator outside worker write scope when
   the runtime permits. Save the baseline's verified artifact and evidence.
2. Generate the schedule with `python3 scripts/control.py plan --budget B
   --unit credits` (or `tokens` / `cost-microusd` with the recorded meter).
   Use four branches, exploration rounds at 0%, 33%, and 66% of aggregate B,
   and approximately 6% of B per branch per round. Apply the schedule to the
   full search budget B without an overhead deduction. Integer rounding goes
   to exploitation. Small budgets that cannot support the schedule fail.
3. Start the opening K workers from identical base files and fresh contexts.
   For an existing project, those base files include its existing implementation.
   Each worker gets the same task facts, but no total, allocated, consumed, or
   remaining budget. Enforce its allocation in the host. Do not pass the
   coordinator's contract, parent's conversation, reasoning summary, favorite
   hypothesis, or other workers' messages. A fresh context still receives required system,
   user, and repository instructions. Use the brief below.
4. At an episode boundary when allocations are exhausted, account for every
   worker, including failures, before closing the round.
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
   pruned lineages. Re-evaluate the saved artifact with the fixed evaluator,
   integrate only the winning change into the user's working tree, and run
   relevant checks. Do not use extra search after B to improve the final score.
   Report any model usage for post-run integration separately.
   Preserve unrelated work and report any unresolved conflict. Keep evidence
   before retiring workers or cleaning up workspaces.

The coordinator maintains the global ledger and best-ever artifact separately
from the active leader. Charge actual metered usage once for every search
worker and retry. Never treat K concurrent workers as one worker's usage.
Account for concurrent in-flight allocations before launching more work. At
episode boundaries, compare aggregate usage with the scheduled triggers. Resume
self-halted episodes in the same session with a neutral continuation prompt
until their allocation is spent. If a bounded episode overshoots, cancel queued
work and reduce later allocations, then report actual usage and trigger offsets.
Keep orchestration and post-run costs visible separately from search B and
respect any user cap on total cost. Stop at B, user cancellation, an explicit
user stopping target, or a failure that prevents reliable selection. If all new
candidates fail, retain the verified incumbent. If none exists, report failure
rather than manufacturing a winner.

## Worker brief

Populate only task facts, using the same brief for each branch. Following
Appendix I, do not reveal compute budgets or remaining usage in any worker or
continuation message. Keep coordinator logs and budget files out of their inputs:

> Work independently on [objective] in [isolated workspace]. Follow the user and
> repository instructions. Improve [metric, direction] subject to [constraints].
> Evaluate with [fixed command/version/seeds]. The inherited verified checkpoint
> is [identifier, score, evidence] or there is no verified incumbent. Preserve it.
> Explore and test approaches. Save exact candidate checkpoints and evaluator
> outputs. Do not change the evaluator or read sibling workspaces. Return
> checkpoint paths, measurements, validity evidence, and remaining artifacts.

Workspace notes may survive a flush, as in the paper. Do not erase project
instructions to simulate a blank context. Keep orchestration transcripts and
speculative reasoning summaries outside the inherited workspace so the
coordinator does not deliberately reintroduce the flushed conversation.

## Helpers and reporting

```sh
python3 scripts/control.py plan --budget 10000 --unit credits
python3 scripts/control.py select /absolute/path/round.json --direction max
```

Helpers only plan and rank records. They do not spawn agents, meter tokens,
verify grader honesty, or move files. The coordinator performs those actions.
For noisy objectives, evaluate with a fixed repeat policy and record the same
aggregate for every candidate. Keep held-out tests out of adaptive selection.

Report baseline and final scores, metric/direction, exact artifact and evidence,
actual budget use, the selected lineage, validation, and material deviations
(different token weighting, fewer branches, sequential waves, extra flushes,
noisy scoring, or episode overshoot).
Distinguish completed experiments from planned ones. Do not claim the paper's
performance gains for this skill. See [method and attribution](references/method.md)
for the paper-to-implementation mapping and limitations.
