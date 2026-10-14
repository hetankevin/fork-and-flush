# Model-usage budgets

## Paper protocol

Section 2 of [the paper](https://arxiv.org/html/2610.07447v1) defines B in
compute credits, a fixed function of model input/output tokens. The reported
conversion is approximately 100 credits per US dollar in that experiment.
This is not a universal Claude/Codex price or a published per-token rate table.
Appendix B distinguishes model credits from solver/training runtime, and
Appendix I says workers receive no total or remaining compute budget.

Keep the model, reasoning-effort setting, tools, and task prompt fixed. The
coordinator meters all search workers, including discarded branches and retries.
Four workers each spending b consume 4b globally, even when they run in parallel.
The three nominal exploration triggers are 0, 0.33B, and 0.66B. Each worker
receives approximately 0.06B per round. No overhead reserve is subtracted from B.

Episodes end when an agent self-halts or reaches a host-enforced token limit.
Resume unfinished allocations in the same session with a neutral continuation
message. Select, fork, or flush only at episode boundaries. Use measured usage
to locate triggers rather than elapsed time or the number of submissions.
Keep episodes bounded so that overshoot is limited, reserve allocations for
in-flight workers, and report actual spend and trigger offsets. The planner
provides nominal targets, not a token meter or an exact hard-cap guarantee.

## Supported units

| `--unit` | Integer budget means | Required accounting |
| --- | --- | --- |
| `credits` (default) | Metered compute credits | Fixed documented mapping from provider input/output usage to credits |
| `cost-microusd` | Millionths of one US dollar, e.g. 100000000 = $100 | Provider token-derived charges or usage multiplied by fixed recorded rates |
| `tokens` | Aggregate input plus output model tokens | Authoritative usage counters with token-category semantics recorded |

Raw tokens preserve a model-usage budget but weight input/output equally, unlike
a provider's cost schedule. Explicitly record that normalization. Do not claim
exact numerical reproduction of the paper's credits without its conversion.
For cost mode, define whether cache reads/writes and reasoning tokens are billed
separately or already included. Avoid counting a subset twice. Record rates and
currency resolution before running. Accumulate exact charges before rounding
rather than rounding every request down. Subscription price and rate-limit
percentages are not per-run model-usage meters.

The planner accepts whole units only. Express fractional dollar budgets in
microdollars, not floating-point dollars. For credits finer than one unit, fix
and document a scale before planning and use it consistently in the ledger.
The script does not supply conversion rates or fetch pricing.

## Coordinator contract

Before launching, record B, its unit, the authoritative usage source, fixed
conversion/rates, model and reasoning effort, episode control, concurrency, and
any separate overall spending cap. Keep this information outside inherited
worker workspaces. Do not pass the full user invocation or this contract to a
worker when it contains budgets. Send the budget-free task brief in SKILL.md.

For each request/episode, retain worker/session identifiers, usage deltas,
input/output categories, converted spend, and the raw usage receipt. Deduplicate
request IDs and turn cumulative counters into deltas. Count resumed prompts,
failed requests with reported usage, and all discarded branches. Missing usage
is not zero: reconcile it before launching further allocations or claiming a
budget was respected. Do not infer token counts from text length or ask workers
to estimate them.

B covers the search agents. Record any model-based orchestration and post-run
integration separately and include them in overall cost reporting. If the user
has an all-inclusive cap, establish the search B and separately authorized
allowances before running. Do not silently reduce the specified B or spend
beyond the overall cap. Deterministic evaluator execution and training duration
are separate machine resources, not model credits. Re-evaluate the chosen
artifact without further adaptive search after B.

## Missing capabilities

If the runtime cannot expose usage and control episodes without telling workers
their budgets, explain that the paper's budget protocol cannot be executed on
that runtime yet. Prepare the plan and identify the needed metering adapter, but
do not launch an unmetered run or silently substitute time/evaluation counts.
An explicitly requested alternative must be labeled as a departure from the
paper. Optional user-specified wall-time cancellation is an operational guard,
not a search budget or a scheduled fork trigger.
