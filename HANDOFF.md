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
- Coordinator-managed soft budgets when host counters/limits are unavailable.
  Prefer measured usage; otherwise document estimates and uncertainty, with no
  separate waiver. Budget-free worker prompts and fixed model/reasoning effort.
- Task-specific selection audits count inside B. Bounded task episodes enable
  budget decisions without runtime token-limit APIs.
- Restore canonical submission files without rolling back accumulated workspace.
  Report results at B separately from overshoot improvements.
- Integer rounding, best-ever checkpoint retention, invalid-record rejection,
  deterministic incumbent-preserving ties.
- Planner schema v2 removes --overhead. Score-record schema remains v1.
- Fresh contexts only for exploration, same-session continuation for exploitation.
- Runtime adaptations and unverified performance claims are clearly separated.

## Independent paper review

A subagent compared the current skill with Sections 2/4/5.1 and Appendices D/I,
including PDF prompt blocks omitted from the HTML. It found the core algorithm
consistent and confirmed that missing counters no longer block native subagents.
Both findings were addressed: preserve accumulated workspace when materializing
submission files, and separate results at B from overshoot discoveries. The
reviewer reread the fixes and found no remaining blocker or material fidelity
issue.
Estimated accounting remains an explicit approximation of the paper's measured
credits. No performance reproduction is claimed.

## README wording

Removed the opening slogan and rewrote the introduction as a direct description
of the algorithm. Removed decorative bold from the prose. This change affects
only repository documentation.

## Verification

- 14 standard-library unit tests pass locally, including explicit token/cost
  units, rejection of non-model units, and budget conservation
  across rounding, maximization/minimization, regressions, failed branches,
  malformed evidence, incumbent ties, and install/update preservation.
- Bundled skill validator passes. Planner and synthetic selection CLI examples pass.
- Reviewed revision 6413a71 passed all four GitHub Actions jobs on macOS/Linux
  with Python 3.9/3.13 (run 38648005492).
- All four Codex/Claude Code installations have been updated and their contents
  verified against the reviewed soft-budget revision. Previous installs were backed up.
- The 14 tests also pass on the Linux installation host.
- Codex app-server discovery confirms the skill is enabled at user scope on
  both hosts. Claude Code installation is verified by file contents, not a live
  model invocation.
- Public repository: https://github.com/hetankevin/fork-and-flush
- No live autoresearch benchmark or paid multi-agent run has been executed.

## Next steps

The reviewed soft-budget revision is pushed, verified, and installed in all
four requested locations. The v0.2.1 archive packages the same skill. Existing
agent sessions that already read the old instructions should reread SKILL.md
and references/budgets.md. No required implementation work remains.
