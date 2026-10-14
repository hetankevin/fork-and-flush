# Contributing

Open an issue with the task, host/runtime version, expected behavior, and a small
reproduction. For bugs, include sanitized planner inputs or checkpoint records.
Do not include credentials, private prompts, or proprietary benchmark data.

Keep the skill portable between Claude Code and Codex. Put runtime-specific
instructions in the adapter reference and substantive methodological departures
in the method notes. Keep Python helpers dependency-free and compatible with
Python 3.9+. Add tests for observable failures or algorithmic invariants.

Run `python3 -m unittest discover -s tests -v` before submitting a change. Update
HANDOFF.md with meaningful state and verification. Any performance claim needs a
reproducible evaluator, baseline, matched budget, and actual measurements.
