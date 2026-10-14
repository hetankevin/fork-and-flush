# Examples

From the repository root:

```sh
python3 skills/fork-and-flush/scripts/control.py plan --budget 1000
python3 skills/fork-and-flush/scripts/control.py select examples/round.json
```

The schedule charges all four workers: 240 units per exploration round, followed
by 90, 90, and 100 units of serial work. Total search allocation is exactly 1,000.
Use `--overhead 100` to reserve 100 of those units for coordination and validation,
leaving 900 search units. The planner does not enforce or meter these allocations.

`round.json` is synthetic, not an experiment. Its artifact/evidence strings are
illustrative and do not refer to real files. Selection returns `a-best` with 14.0,
not worker A's regressed last state (11.0), and rejects worker B's invalid 99.0.
The tests also cover minimization, inherited ties, failed rounds, and malformed
records.

## Example requests

Codex:

```text
$fork-and-flush Improve this solver's benchmark score. Use the existing evaluator
and correctness tests unchanged. Limit the search to 100 evaluator calls, reserve
10 for validation, and cap each worker at 10 minutes. Use four independent workers
from the current implementation. Report measured scores and actual calls used.
```

Claude Code:

```text
/fork-and-flush Minimize this kernel's simulated cycle count while passing all
correctness tests. Use four fresh-context branches per round. Limit the run to
100 evaluator calls with 10 reserved for validation and a 10-minute per-worker
cap. Preserve the fastest valid checkpoint even if later experiments regress.
```

These use evaluator calls as a disclosed proxy, not a model-token budget. Set
resource limits suitable for your environment before launching workers. The host
must support fresh contexts and session resumption for the full workflow.
