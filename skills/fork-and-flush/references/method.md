# Method, provenance, and adaptations

Source: Ziyang Cai, Christos Ziakas, Vasilis Kontonis, Tim Pearce, Siddhartha Sen,
Akshay Krishnamurthy, Shivam Garg, and Dimitris Papailiopoulos.
*Fork-and-Flush: Escaping Idea Basins in Autoresearch Agents*, arXiv:2610.07447v1,
2026. [Paper](https://arxiv.org/html/2610.07447v1), especially Sections 2, 4, 5.1
and Appendices D and I. The paper is CC BY 4.0. These instructions are an
independently written implementation and adaptation, not the authors' software
or an endorsed reproduction. No paper figures, code, or prompt text are bundled.

The preserved mechanism is workspace inheritance with fresh conversational
contexts at each exploration round, followed by scored branch selection and
continued execution of the winner. Each lineage is valued by its best attained
score. The budgeted result retains the best checkpoint across all lineages reached
within B. Improvements from an episode overrun are retained and reported
separately, with approximate boundary attribution when accounting is estimated.

The default planner uses four workers and starts rounds at 0%, 33%, and 66% of
aggregate model-usage budget B, allocating 6% to each worker per round. Between rounds,
one winner continues. Integer rounding is downward and remaining units go to
exploitation. A 10,000-credit search budget therefore has exploration costs of
2,400 credits each and exploitation allocations of 900, 900, and 1,000 credits. This is
a concrete discretization of the paper's approximate schedule, not a claim that
those integers reproduce its harness.

| Aspect | This implementation |
| --- | --- |
| Existing code | May begin from a user's project rather than an empty research workspace |
| Accounting | Token-derived credits/cost or raw tokens; coordinator estimates when counters are absent; full B is scheduled |
| Worker brief | No total, allocated, consumed, or remaining compute budgets, as in Appendix I |
| Selection | Independently verified records, explicit tie rule, inherited incumbent |
| Scheduling | Integer planning helper, agent-operated dispatch and cancellation |
| Runtime | Claude/Codex sessions instead of the paper's Copilot CLI harness |
| Capacity | May run K workers in waves, reported as a scheduling adaptation |

The coordinator manages allocations at episode boundaries and keeps budget
information out of worker prompts, following Sections 2 and 5.1 and Appendix I.
The paper used measured credits. When a host lacks usage counters, this skill
uses documented estimates and soft episode control. That is an accounting
approximation, not a reproduction of the paper's measured budget. It requires
no separate waiver in the ordinary skill workflow. The branching and selection
procedure stays the same. Scientific validity criteria are not relaxed.
Appendix I's protected-incumbent prompt materializes the best submission at its
canonical path. This skill likewise preserves the surrounding accumulated
workspace when restoring submission files. Those prompt blocks are visible in
the [PDF](https://arxiv.org/pdf/2610.07447v1) but omitted from the HTML rendering.
The paper reports credits as a fixed input/output-token function, approximately
100 credits per dollar in its experiment. We do not invent its unpublished
per-token conversion or apply that dollar ratio to other providers. See
[budget accounting](budgets.md) for the chosen meter and cost/token normalization.
Elapsed time and evaluator counts do not replace the budget. The paper also
examined optional branch directives, which are not required here. We do
not implement the triplet embeddings used to analyze idea basins: those are an
analysis procedure rather than a prerequisite for the search loop.

There is no claim of reproducing the paper's task results, of guaranteed
improvement, or of a statistical advantage from this package. Fresh contexts
can still rediscover the same approach. Workspace notes can also carry prior
ideas. Noisy evaluations and changes in token weighting require explicit
experimental design. This package has not reproduced the original harness.
