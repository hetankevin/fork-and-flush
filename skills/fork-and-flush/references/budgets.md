# Model-usage budgets

## Paper protocol and runtime accounting

Section 2 of [the paper](https://arxiv.org/html/2610.07447v1) defines B in
compute credits, a fixed function of model input/output tokens. The reported
conversion is approximately 100 credits per US dollar in that experiment.
This is not a universal Claude/Codex price or a published per-token rate table.
Appendix B distinguishes model credits from solver/training runtime, and
Appendix I says workers receive no total or remaining compute budget.

Keep the model, reasoning-effort setting, tools, and task prompt fixed. Account
for all search workers, including discarded branches and retries. Four workers
each spending b consume 4b globally, even when they run in parallel. The three
nominal exploration triggers are 0, 0.33B, and 0.66B. Each worker receives
approximately 0.06B per round. No overhead reserve is subtracted from B.

The paper's harness measures usage and bounds episodes. Prefer those facilities
when available. If the runtime provides neither per-worker counters nor token
limits, the coordinator can still manage a soft token/cost budget. Estimate
usage, disclose that accounting choice briefly, and proceed. Do not pause to
request a waiver or replace the method with a one-round comparison merely
because exact metering is unavailable. Estimated accounting is an implementation
approximation; do not claim it reproduces the paper's measured compute budget.

Use the user's budget if given. Otherwise choose and state a proportionate soft
budget based on task scope and available context. There is no universal default
of 100,000 tokens. Reuse existing authorization rather than requesting approval
for the accounting method itself. If the user explicitly requires exact audited
spending or a guaranteed hard cap, explain any inability to provide that
particular guarantee. An estimate alone cannot satisfy such a requirement.

## Units

| `--unit` | Integer budget means | Accounting |
| --- | --- | --- |
| `credits` (default) | Compute credits | Documented mapping from measured or estimated input/output usage |
| `cost-microusd` | Millionths of one US dollar, e.g. 100000000 = $100 | Provider token-derived charges or measured/estimated usage multiplied by recorded rates |
| `tokens` | Aggregate input plus output model tokens | Usage counters where available, otherwise coordinator estimates |

Raw tokens weight input/output equally, unlike a provider's cost schedule.
Record that normalization. Do not claim exact numerical reproduction of the
paper's credits without its conversion. For cost mode, record rates and how
cache reads/writes and reasoning tokens are billed. Avoid counting subsets
twice. Accumulate charges before rounding rather than rounding every request
down. Subscription price and rate-limit percentages are not per-run meters.

The planner accepts whole units only. Express dollars in integer microdollars.
For credits finer than one unit, document a scale and use it consistently. The
script plans nominal allocations; it does not fetch prices, meter usage, or
estimate tokens for you.

## Estimate from available evidence

The coordinator owns the estimate. Use the strongest evidence available without
turning the search for perfect accounting into a prerequisite for doing the task:

1. Use provider/session counters or usage receipts wherever exposed. Turn
   cumulative counters into deltas and deduplicate request identifiers.
2. For visible requests, tokenize the actual prompts, replayed context, tool
   results, and responses with a suitable tokenizer if available. This measures
   visible text only. Add estimates for unavailable system/tool framing, hidden
   reasoning, cache treatment, and internal requests when relevant.
3. If a tokenizer is unavailable, use a documented approximate text-to-token
   conversion suited to the content. Mark it as an estimate. A short final
   answer is not the worker's total usage: account for its repeated model calls
   and context processing, including tools and reasoning.
4. If worker traces are unavailable, make an ex-ante per-episode estimate from
   the known brief/context, expected work and output, and observed comparable
   episodes if any. State the assumptions and a plausible range. Use a
   conservative planning value and revise it from progress reports or any later
   counters. A coarse low-confidence estimate is allowed; do not invent a
   provider receipt or call the range a guaranteed upper bound.

For each worker or audit, record measured components, estimated components,
source/assumptions, a planning estimate and uncertainty, and whether the episode
is running or finished. Sum usage across all branches and selection audits,
including failed and discarded work. Distinguish incurred estimates from
reservations for running work so a reservation is replaced, not added again,
when an episode completes. Missing usage is not zero; estimate it and continue.
Where costs are requested, convert token categories using recorded rates rather
than silently equating all token types.

## Manage episodes without token-limit APIs

Allocate the planner's nominal shares in the coordinator ledger. Reserve the
estimated cost of in-flight episodes and any necessary audits before dispatching
more work. Give workers bounded task episodes, such as developing and evaluating
one candidate or checking a specified proof claim, and have them return artifacts
and a concise report. Do not tell workers total or remaining token budgets.
These task boundaries provide opportunities to reassess usage, not guaranteed
token caps. Retain the selected worker's session for continued work.

At each episode return, update estimated/measured usage. Resume unfinished
allocations in the same session with a neutral continuation message. At nominal
phase boundaries, select or fork as scheduled. If an episode overshoots, reduce
later allocations and report the estimated or measured offset. Stop dispatching
follow-ups when the soft budget is spent. Use cancellation where available if
needed, but do not imply it recovers consumed tokens or guarantees a bound on
in-flight work. When only a few episodes fit, report the coarse cadence.

Do not silently turn B into minutes, evaluation calls, or a count of approaches.
Those can inform estimates or bound tasks but remain different resources. The
usual K=4, repeated fresh-context forks, winner continuation, and final best-ever
selection still apply. Run workers in waves if necessary, from the same snapshot,
and reserve the same per-worker shares. A worker-slot limit does not reduce K.

## Scope and reporting

B includes search workers, retries, and model-based audits that affect viability
or selection. Such audits consume the corresponding phase allocation; reserve
for them before assigning the remaining work to workers. This audit overhead is
a task-specific adaptation, not extra free compute. Record model-based
orchestration and post-run integration separately and include them in overall
cost reporting. Respect any user cap on overall spending and make its relationship
to search B explicit. Keep budget records outside worker inputs.

Approximate resource accounting does not weaken the task's scientific criteria.
Keep correctness checks, statistical guarantees, implementation requirements,
and experimental measurement limits unchanged. Solver/evaluator runtime is a
separate machine resource. Re-evaluate the selected artifact without additional
adaptive search after B. Optional user-specified timeouts are operational guards.

Report which usage was measured or estimated, the estimation method and
uncertainty, aggregate spend including discarded work, and any schedule drift.
Describe soft control as soft control, not an enforced token or billing ceiling.

Record cumulative aggregate usage when each exact checkpoint is first verified.
For the result at B, filter the final selector's input to checkpoints reached
within B. Preserve the best artifact across every lineage in that filtered set.
If an episode overruns, report any better post-B artifact separately and give
its extra measured/estimated spend. Do not fold that improvement into the
budgeted score. Under estimated accounting, classify using the recorded planning
estimate and flag uncertainty spanning B. This is an approximate boundary, not
evidence of exact matched compute. If there is no valid within-B checkpoint,
say so even if an overrun produced a valid artifact.
