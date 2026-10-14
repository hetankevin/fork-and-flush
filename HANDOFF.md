# Handoff

## State

Initial portable skill implementation of arXiv:2610.07447v1. The repository has
agent instructions, runtime adapters, a fixed-schedule planner, a best-checkpoint
selector, installation tooling, examples, attribution, MIT license, and CI.

## Design decisions

- Skill-operated orchestration with small deterministic helpers, no daemon or
  model-specific launcher. The host owns sessions, metering, and validation.
- Default K=4 and three rounds at 0/33/66% of aggregate search allowance.
- Explicit overhead reserve, integer rounding, best-ever checkpoint retention,
  invalid-record rejection, deterministic incumbent-preserving ties.
- Fresh contexts only for exploration, same-session continuation for exploitation.
- Runtime adaptations and unverified performance claims are clearly separated.

## Verification

- 12 standard-library unit tests pass locally, including budget conservation
  across rounding, maximization/minimization, regressions, failed branches,
  malformed evidence, incumbent ties, and install/update preservation.
- Skill frontmatter validation and remote installation checks are pending.
- No live autoresearch benchmark or paid multi-agent run has been executed.

## Next steps

Finish validation, publish the repository, install on both requested hosts, and
verify installed content. Record completed results here. Future improvements
should be driven by real host behavior or measured benchmark runs.
