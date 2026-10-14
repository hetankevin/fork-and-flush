# Run contract and checkpoint records

Keep the coordinator's contract, ledger, worker IDs, selection outputs, and
verification logs outside inherited worker directories. A practical run folder:

```text
run/
  contract.json
  ledger.jsonl
  schedule.json
  rounds/0.json
  checkpoints/...
  evidence/...
  sessions/...
```

The contract should identify the task, baseline, evaluator version and command,
score direction, validity checks, fixed seeds/repeat aggregation, editable scope,
model/settings, total budget/unit, overhead reserve, limits, and snapshot policy.
The append-only ledger records each completed allocation's worker ID, phase,
actual spend, measurement source, checkpoint IDs, failures, and timestamps.
Record partial/cancelled allocations too. Do not count inherited work again.

The selection helper reads this format:

```json
{
  "schema_version": 1,
  "incumbent": "base-001",
  "records": [
    {
      "lineage": "base",
      "checkpoint": "base-001",
      "score": 12.5,
      "valid": true,
      "artifact": "/run/checkpoints/base-001.tar",
      "evidence": "/run/evidence/base-001.json"
    },
    {
      "lineage": "round-0-worker-1",
      "checkpoint": "candidate-001",
      "score": null,
      "valid": false
    }
  ]
}
```

Every checkpoint identifier is unique within the selection input. Include the
inherited incumbent in each round. Include every verified improvement in that
round, not just final workspace states. For final selection, combine records
from every round, including pruned lineages. For a first run with no valid
baseline, omit `incumbent` or set it to null.

A valid score is finite and numeric. `valid` must be a JSON boolean. Artifact
and evidence are nonempty identifiers or paths. The helper validates structure,
not their existence or truth: the coordinator must verify them. Evidence should
include command, evaluator version, inputs/seeds, environment, exit status,
validity checks, raw measurements, aggregation, and the artifact's content hash
or Git commit. Git artifacts must include required untracked/ignored files via
an accompanying manifest/archive. Retain the best artifact before more edits.

Use `--direction min` for cost/loss objectives. Ties retain the incumbent and
then sort by lineage/checkpoint ID. Invalid candidates remain in the records
for accounting but cannot win. Malformed records fail the whole command rather
than silently hiding broken evidence. No valid records means an error, not a
fabricated score. The helper makes no statistical significance claim.
