# Handoff

## State

Portable skill implementation of arXiv:2610.07447v1, revised to follow its
model-usage budget protocol. The repository has
agent instructions, runtime adapters, a fixed-schedule planner, a best-checkpoint
selector, installation tooling, examples, attribution, MIT license, and CI.

## Design decisions

- Skill-operated orchestration with small deterministic helpers, no daemon or
  model-specific launcher. The host owns sessions, metering, and validation.
- Default K=4 and three rounds at 0/33/66% of aggregate search allowance.
- Full model-usage budget B with explicit credits/tokens/cost-microusd units.
  No overhead deduction or time/evaluation-count fallback.
- Host-metered episodes, budget-free worker prompts, fixed model/reasoning effort.
- Integer rounding, best-ever checkpoint retention, invalid-record rejection,
  deterministic incumbent-preserving ties.
- Planner schema v2 removes --overhead. Score-record schema remains v1.
- Fresh contexts only for exploration, same-session continuation for exploitation.
- Runtime adaptations and unverified performance claims are clearly separated.

## Verification

- 14 standard-library unit tests pass locally, including explicit token/cost
  units, rejection of non-model units, and budget conservation
  across rounding, maximization/minimization, regressions, failed branches,
  malformed evidence, incumbent ties, and install/update preservation.
- Bundled skill validator passes. Planner and synthetic selection CLI examples pass.
- Previous release passed GitHub Actions on macOS/Linux with Python 3.9/3.13.
  The revised budget implementation awaits its post-push CI run.
- Previous release was installed on both hosts. All four installations need
  the revised budget implementation after this push.
- Codex app-server discovery confirms the skill is enabled at user scope on
  both hosts. Claude Code installation is verified by file contents, not a live
  model invocation.
- Public repository: https://github.com/hetankevin/fork-and-flush
- No live autoresearch benchmark or paid multi-agent run has been executed.

## Next steps

Push the budget revision, update and compare all four installations, check CI,
and publish the updated skill archive. Preserve the distinction between unit
validation and an end-to-end autoresearch performance evaluation.
