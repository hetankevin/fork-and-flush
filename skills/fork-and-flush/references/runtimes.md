# Runtime adapters

A flush requires a new worker context. A request to forget, a compaction summary,
or a branch of the existing conversation is insufficient. The coordinator may
retain its history, but passes only the worker brief and necessary task facts.

## Codex

Use available agent tools that can start workers without inherited conversation.
For a runtime exposing `collaboration.spawn_agent`, use `fork_turns="none"`, a
unique task name, and an explicit absolute workspace in the prompt. Such workers
can share a filesystem: spawning alone does not isolate edits. First create
separate worktrees or copies, and direct each worker to its own directory. Resume
that same worker for exploitation using the runtime's follow-up mechanism.

For a CLI-only host, check `codex exec --help` and `codex exec resume --help` for
that installed version. A new exec session can provide a fresh context, while
resuming its session can preserve the winning conversation. Do not use resume
for exploration branches. Preserve the session identifier and run logs outside
inherited workspaces. Use the user's configured model and permission settings.

Do not create user-visible desktop chats merely to implement worker branches.
Use subagents or isolated CLI sessions where supported and authorized. If the
runtime forbids delegation, explain that limitation and offer the single-worker
or externally orchestrated adaptation rather than claiming to have forked.

## Claude Code

Use Claude's subagent facility with a new context, a self-contained brief, and an
isolated worktree when available. Confirm the tool's current semantics: a
conversation fork that inherits the transcript does not satisfy a flush. Retain
the returned agent/session identifier to resume the selected worker during
exploitation. Do not resume the parent for new exploration branches.

On a CLI host, inspect `claude --help` for fresh noninteractive sessions, worktree
support, and session resumption. Run each branch in its assigned directory and
save its session ID. Starting a new process without a resume/continue option
provides the desired session boundary when the installed CLI supports it. Do
not add permission-bypass flags. If resumption is unavailable, disclose that
exploitation also restarts the conversation.

## Isolation and capacity

All K branches in a round receive the same snapshot. Git worktrees include
committed files only: preserve uncommitted task inputs in an isolated snapshot
before branching, without staging unrelated files. Copy needed ignored assets
explicitly. For non-Git projects, make independent copies from an explicit
allowlist. Avoid copying credentials or unrelated personal files. Required
project instructions remain present. Do not delete existing HANDOFF.md or
CLAUDE.md files to force a flush.

Keep controller logs outside worker workspaces. Stop workers before selection
and integration. Do not merge competing solutions together as the selection
step. Retain each best-scoring artifact separately from the mutable checkout. When
materializing the winner, restore the canonical submission paths while keeping
its accumulated experimental files and notes. Avoid a whole-workspace rollback.

If fewer than K worker slots are available, run identical-snapshot workers in
waves with no sibling communication. This preserves K candidates and total
allocations but changes parallel wall time. Report the deviation. Reduce K only
with an explicit run configuration and replan the budget. K=1 is flush-only.

Inspect available usage counters and host limits, then use what the runtime
actually exposes. Neither per-worker token accounting nor an enforceable token
limit is required to start. If counters are absent, estimate usage in the
coordinator and manage a soft budget using [budget accounting](budgets.md).
State this choice once and proceed without requesting a waiver. Do not describe
a documented estimate as measured usage or an enforced billing ceiling.

Without a token-limit API, give each worker a bounded task episode, such as
implementing and evaluating one candidate or auditing one specified argument.
Have it return artifacts and a concise report, then decide whether to resume
that same worker. Reserve estimated usage for running episodes and required
audits before launching more work. Use cancellation if available and necessary;
otherwise stop dispatching follow-ups. Do not assume cancellation can recover
already consumed tokens or guarantee a maximum for an in-flight episode.

Wall-time cancellation is an optional operational guard. Elapsed time and
submission counts do not become token units. Keep the model-usage budget and
scientific measurement budget separate, and preserve all requested validity
requirements when using estimated accounting.
