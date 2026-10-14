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
score. The final output retains the best result across the whole run.

The default planner uses four workers and starts rounds at 0%, 33%, and 66% of
aggregate search spend, allocating 6% to each worker per round. Between rounds,
one winner continues. Integer rounding is downward and remaining units go to
exploitation. A 1,000-unit search allowance therefore has exploration costs of
240 units each and exploitation allocations of 90, 90, and 100 units. This is
a concrete discretization of the paper's approximate schedule, not a claim that
those integers reproduce its harness.

| Aspect | This implementation |
| --- | --- |
| Existing code | May begin from a user's project rather than an empty research workspace |
| Metering | Explicit overhead reserve and host metering, or disclosed proxy budgets |
| Worker brief | Includes resource limits for practical enforcement |
| Selection | Independently verified records, explicit tie rule, inherited incumbent |
| Scheduling | Integer planning helper, agent-operated dispatch and cancellation |
| Runtime | Claude/Codex sessions instead of the paper's Copilot CLI harness |
| Capacity | May run K workers in waves, reported as a scheduling adaptation |

The paper's experimental workers were not told their remaining compute budget.
This skill's brief supplies limits, so it is a practical adaptation. The paper
also examined optional branch directives, which are not required here. We do
not implement the triplet embeddings used to analyze idea basins: those are an
analysis procedure rather than a prerequisite for the search loop.

There is no claim of reproducing the paper's task results, of guaranteed
improvement, or of a statistical advantage from this package. Fresh contexts
can still rediscover the same approach. Workspace notes can also carry prior
ideas. Noisy evaluations and proxy budgets require explicit experimental design.
