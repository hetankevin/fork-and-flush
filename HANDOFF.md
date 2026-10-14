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

## README wording

Removed the opening slogan and rewrote the introduction as a direct description
of the algorithm. Removed decorative bold from the prose. This change affects
only repository documentation, so the installed skill files remain current.

## Verification

- 14 standard-library unit tests pass locally, including explicit token/cost
  units, rejection of non-model units, and budget conservation
  across rounding, maximization/minimization, regressions, failed branches,
  malformed evidence, incumbent ties, and install/update preservation.
- Bundled skill validator passes. Planner and synthetic selection CLI examples pass.
- Budget revision fea76ce passed all four GitHub Actions jobs on macOS/Linux
  with Python 3.9/3.13 (run 38639752952).
- All four Codex/Claude Code installations have been updated and their contents
  verified against the budget revision. Previous installs were backed up.
- The 14 tests also pass on the Linux installation host.
- Codex app-server discovery confirms the skill is enabled at user scope on
  both hosts. Claude Code installation is verified by file contents, not a live
  model invocation.
- Public repository: https://github.com/hetankevin/fork-and-flush
- No live autoresearch benchmark or paid multi-agent run has been executed.

## Next steps

The budget revision, push, and all four installation updates are complete. The
v0.2.0 archive packages the verified skill. No required implementation work
remains. Preserve the distinction between unit validation and an end-to-end
autoresearch performance evaluation.
