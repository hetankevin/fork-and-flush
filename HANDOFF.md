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
- Bundled skill validator passes. Planner and synthetic selection CLI examples pass.
- GitHub Actions passes on macOS and Linux with Python 3.9 and 3.13.
- Both requested hosts have matching Codex and Claude Code skill contents.
- Codex app-server discovery confirms the skill is enabled at user scope on
  both hosts. Claude Code installation is verified by file contents, not a live
  model invocation.
- Public repository: https://github.com/hetankevin/fork-and-flush
- No live autoresearch benchmark or paid multi-agent run has been executed.

## Next steps

Requested implementation, publication, and installations are complete. No
required work remains. Future improvements should be driven by real host
behavior or measured benchmark runs. Preserve the distinction between unit
validation and an end-to-end autoresearch performance evaluation.
