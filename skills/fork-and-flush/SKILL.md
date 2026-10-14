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
score for a subjective task. Resolve a missing meaningful evaluator with the
user. Reuse any supplied budget. Otherwise choose a proportionate soft token
budget for the task, state it briefly, and proceed within the authorized scope.
Do not impose a universal token allowance or ask for a budget solely because
none was specified.

Record these in a coordinator-only run contract outside worker workspaces.
Use a fixed total model-usage budget B, summed across all search workers. The
paper uses compute credits that are a fixed function of input/output tokens.
Use credits with a documented conversion, token-derived cost, or an explicitly
chosen input-plus-output token budget. Prefer usage counters when available;
otherwise the coordinator estimates usage and manages a soft budget itself.
Missing per-worker counters or enforceable token limits are not launch blockers
and do not require a waiver or separate approval to use estimates. Keep the model,
reasoning-effort setting, tools, and task prompt fixed across workers. Reasoning
effort is a model setting, not the resource budget. Never silently substitute
elapsed time or evaluator-call counts for model usage.

Record the usage source or estimation method, token categories, conversion/rates,
evaluator version, seeds or repeat policy, and concurrency. Read
[budget accounting](references/budgets.md) for estimating usage and controlling
work without runtime token limits. Keep measured and estimated usage distinct.
Allocations and balances belong to the coordinator, not worker prompts. The
coordinator can bound task episodes, track estimates, and stop resuming workers
without an API that enforces token limits. A soft budget is not a guaranteed
billing ceiling. Respect any explicit user requirement for an enforced cap.

Read [the runtime adapters](references/runtimes.md) before launching agents.
Read [the record format](references/records.md) before creating score records.
Resolve helper paths relative to this SKILL.md, not the task's working directory.

## Run the fixed schedule

1. Snapshot the starting workspace without losing uncommitted user work. Put
   each worker in a separate checkout or copied workspace. Preserve required
   ignored assets explicitly. Keep the evaluator outside worker write scope when
   the runtime permits. Save the baseline's verified artifact and evidence.
2. Generate the schedule with `python3 scripts/control.py plan --budget B
   --unit credits` (or `tokens` / `cost-microusd` with the recorded accounting method).
   Use four branches, exploration rounds at 0%, 33%, and 66% of aggregate B,
   and approximately 6% of B per branch per round. Apply the schedule to the
   full search budget B without an overhead deduction. Integer rounding goes
   to exploitation. Small budgets that cannot support the schedule fail.
3. Start the opening K workers from identical base files and fresh contexts.
   For an existing project, those base files include its existing implementation.
   Each worker gets the same task facts, but no total, allocated, consumed, or
   remaining budget. Manage its allocation in the coordinator, using host
   controls when available and soft accounting otherwise. Do not pass the
   coordinator's contract, parent's conversation, reasoning summary, favorite
   hypothesis, or other workers' messages. A fresh context still receives required system,
   user, and repository instructions. Use the brief below.
4. At an episode boundary when allocations are exhausted, account for every
   worker, including failures, before closing the round.
   Independently evaluate its candidate checkpoints with the frozen evaluator.
   Record every valid improvement, its cumulative aggregate usage at first
   verified grading, and its exact immutable artifact. Mark usage as measured
   or estimated, with uncertainty where appropriate.
   Use `select` over this round's records plus the inherited incumbent. Select
   by best verified score attained in a lineage, not its last edited file or
   its prose report. Invalid artifacts cannot win. Ties retain the incumbent,
   then use stable lineage/checkpoint identifiers. This tie rule is an adaptation.
5. Continue the winning worker in its existing conversation and isolated
   workspace for the exploitation allocation. If needed, materialize the
   lineage-best scored submission at its canonical artifact paths and tell the
   worker what was restored. Retain the rest of its accumulated workspace,
   including experimental files and notes. Do not reset the whole checkout to
   an older commit merely because that commit holds the best submission. A new conversation here would add an
   extra flush, so label that fallback if session resumption is unavailable.
   If the inherited incumbent remains best, materialize its submission files
   in a surviving fresh worker chosen by stable worker ID and continue that
   worker, retaining that worker's other accumulated files. Do not resume
   the pre-flush parent, which would undo the intended context reset. If no
   worker can continue, stop with the incumbent or disclose a fresh restart.
6. At the next scheduled fork, snapshot the leader's accumulated workspace and
   start K new fresh-context workers from that same snapshot. Keep the verified
   incumbent available to all. Repeat selection and exploitation within the
   budget. Do not wait for a plateau to trigger the scheduled intervention.
7. Select the best verified artifact reached by aggregate budget B across all
   lineages, including pruned ones. Before final `select`, filter records by
   their first verified grading's cumulative usage. The helper ranks the supplied
   records; it does not enforce this cutoff. With estimates, use the recorded
   planning estimate and label the budget boundary approximate. Flag candidates
   whose uncertainty crosses B instead of claiming a strict equal-compute result.
   If an in-flight episode discovers a better artifact after B, retain it but
   report it separately as an overshoot result with its additional usage. If no
   valid result was reached by B, report that explicitly. Re-evaluate the chosen
   artifact with the fixed evaluator, integrate its change into the user's
   working tree, and run relevant checks. Make clear which artifact is delivered.
   Do not start extra search after B. Report post-run integration usage separately.
   Preserve unrelated work and report any unresolved conflict. Keep evidence
   before retiring workers or cleaning up workspaces.

The coordinator maintains the global ledger and best-ever artifact separately
from the active leader. Account for usage once for every search worker, retry,
and model-based audit that informs selection. Use measured usage when available
and documented estimates otherwise. Never treat K concurrent workers as one
worker's usage.
Account for concurrent in-flight allocations before launching more work. At
episode boundaries, compare aggregate measured/estimated usage with the
scheduled triggers. With no token-limit API, assign bounded task episodes and
decide whether to resume, select, fork, or stop from the ledger. Resume
self-halted episodes in the same session with a neutral continuation prompt
until their allocation is spent. If a bounded episode overshoots, cancel queued
work and reduce later allocations, then report usage estimates or measurements
and trigger offsets. Allocate required model-based audits within the phase
allowances so their cost does not create an uncounted expansion of B.
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
measured usage and/or estimated budget use with uncertainty, the selected
lineage, validation, and material deviations (estimated accounting, different
token weighting, fewer branches, sequential waves, extra flushes,
noisy scoring, or episode overshoot).
Distinguish completed experiments from planned ones. Do not claim the paper's
performance gains for this skill. See [method and attribution](references/method.md)
for the paper-to-implementation mapping and limitations.
