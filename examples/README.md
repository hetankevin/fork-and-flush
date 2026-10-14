# Examples

From the repository root:

```sh
# 10,000 compute credits using the run contract's fixed token-to-credit mapping.
python3 skills/fork-and-flush/scripts/control.py plan --budget 10000 --unit credits
# $100 of token-derived model cost, represented as integer microdollars.
python3 skills/fork-and-flush/scripts/control.py plan --budget 100000000 --unit cost-microusd
# An explicitly chosen normalization: one million input-plus-output tokens.
python3 skills/fork-and-flush/scripts/control.py plan --budget 1000000 --unit tokens
python3 skills/fork-and-flush/scripts/control.py select examples/round.json
```

For B = 10,000 credits, each exploration worker receives 600 credits. Four
workers cost 2,400 credits per round, including discarded workers. Exploration
starts at aggregate spends of 0, 3,300, and 6,600 credits. The intervening serial
allocations are 900, 900, and 1,000 credits. Total nominal allocation is 10,000.

No overhead deduction changes B. The host meters actual token usage and applies
interventions at episode boundaries. The planner does not meter, enforce limits,
or convert provider tokens into credits. Cost rates, cache/reasoning accounting,
episode controls, and any separate coordinator costs belong in the run contract.
See [budget accounting](../skills/fork-and-flush/references/budgets.md).

`round.json` is synthetic, not an experiment. Its artifact/evidence strings are
illustrative and do not refer to real files. Selection returns `a-best` with 14.0,
not worker A's regressed last state (11.0), and rejects worker B's invalid 99.0.
The tests also cover minimization, inherited ties, failed rounds, and malformed
records.

## Example requests

These are coordinator requests. Do not forward their budget information to
workers. Use the budget-free worker brief in SKILL.md instead.

Codex, token budget:

```text
$fork-and-flush Improve this solver's benchmark score using the existing evaluator
and correctness checks unchanged. Set B to 1,000,000 aggregate input-plus-output
model tokens across all search workers, including discarded branches and retries.
Keep the current model and reasoning effort fixed. Use K=4 with exploration at
0%, 33%, and 66% of B and 6% of B per branch. Meter usage in the host and apply
interventions at episode boundaries. Do not disclose budgets to workers. Report
the best verified checkpoint, actual token usage, and any overshoot. Confirm the
metering capability before launch. Report any coordinator model usage separately.
```

Claude Code, token-derived cost budget:

```text
/fork-and-flush Minimize this kernel's simulated cycle count while passing all
correctness tests. Set B to $100 of metered token-derived search-model cost across
all workers, including discarded branches and retries. Record the fixed token
rates and cache/reasoning accounting before starting. Keep the current model and
reasoning effort fixed. Use K=4 with exploration at 0%, 33%, and 66% of B and 6%
of B per branch. Enforce allocations in the host at episode boundaries without
telling workers their budgets. Preserve the fastest valid checkpoint. Report
actual search cost and any coordinator model costs separately. If usage cannot
be metered, prepare the plan and explain the missing capability before launching.
```

For a host with a documented compute-credit meter, replace the budget sentence
with “Set B to 10,000 metered compute credits using the recorded input/output-token
conversion.” Do not assume the paper's approximate credit/dollar conversion is
your provider's price. Raw-token mode changes the weighting from cost-based
credits and should be identified as that normalization in the final report.
