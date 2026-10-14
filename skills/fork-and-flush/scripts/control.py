#!/usr/bin/env python3
"""Deterministic scheduling and verified-record selection. Python 3.9+, stdlib only."""
import argparse
import json
import math
from pathlib import Path
import sys


def integer(value, name, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value


def plan(budget, branches=4, unit="credits"):
    integer(budget, "budget", 1)
    integer(branches, "branches", 1)
    if unit not in ("credits", "tokens", "cost-microusd"):
        raise ValueError("unit must be credits, tokens, or cost-microusd")
    search = budget
    per_branch = search * 6 // 100
    if per_branch < 1:
        raise ValueError("budget is too small for a 6% branch allocation")
    bounds = [0, search * 33 // 100, search * 66 // 100, search]
    phases = []
    for round_id, (start, end) in enumerate(zip(bounds, bounds[1:])):
        explore_end = start + branches * per_branch
        if explore_end >= end:
            raise ValueError("branch allocations leave no exploitation before the next trigger")
        phases.append(dict(kind="explore", round=round_id, start=start,
                           end=explore_end, workers=branches,
                           per_worker=per_branch, allocation=branches * per_branch,
                           fresh_context=True))
        phases.append(dict(kind="exploit", round=round_id, start=explore_end,
                           end=end, workers=1, per_worker=end - explore_end,
                           allocation=end - explore_end, fresh_context=False))
    return dict(schema_version=2, total_budget=budget, budget_unit=unit,
                search_budget=search, branches=branches,
                note="Offsets are aggregate model-usage targets across all search workers. "
                     "The coordinator manages measured or estimated usage at episode boundaries.",
                phases=phases)


def nonempty(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a nonempty string")
    return value


def select(data, direction="max"):
    if direction not in ("min", "max"):
        raise ValueError("direction must be min or max")
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ValueError("expected a schema_version 1 record object")
    records = data.get("records")
    if not isinstance(records, list):
        raise ValueError("records must be a list")
    incumbent = data.get("incumbent")
    if incumbent is not None:
        nonempty(incumbent, "incumbent")
    seen, valid = set(), []
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("each record must be an object")
        checkpoint = nonempty(record.get("checkpoint"), "checkpoint")
        nonempty(record.get("lineage"), "lineage")
        if checkpoint in seen:
            raise ValueError(f"duplicate checkpoint: {checkpoint}")
        seen.add(checkpoint)
        if type(record.get("valid")) is not bool:
            raise ValueError(f"{checkpoint}: valid must be a boolean")
        score = record.get("score")
        if score is not None and (type(score) not in (int, float) or not math.isfinite(score)):
            raise ValueError(f"{checkpoint}: score must be finite numeric or null")
        if record["valid"]:
            if score is None:
                raise ValueError(f"{checkpoint}: valid checkpoint requires a score")
            nonempty(record.get("artifact"), "artifact")
            nonempty(record.get("evidence"), "evidence")
            valid.append(record)
    if incumbent is not None and not any(r["checkpoint"] == incumbent for r in valid):
        raise ValueError("incumbent must refer to a valid record in this file")
    if not valid:
        raise ValueError("no valid checkpoint to select")
    # Deterministic under input reordering, preserving an equally good incumbent.
    winner = min(valid, key=lambda r: (
        -r["score"] if direction == "max" else r["score"],
        r["checkpoint"] != incumbent, r["lineage"], r["checkpoint"]))
    return dict(schema_version=1, direction=direction, winner=winner,
                valid_count=len(valid), rejected_count=len(records) - len(valid))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    planning = commands.add_parser("plan", help="plan aggregate search allocations")
    planning.add_argument("--budget", type=int, required=True,
                          help="total model-usage budget B, in integer units")
    planning.add_argument("--unit", choices=("credits", "tokens", "cost-microusd"),
                          default="credits", help="metered budget unit (default: credits)")
    planning.add_argument("--branches", type=int, default=4)
    selection = commands.add_parser("select", help="rank independently verified checkpoint records")
    selection.add_argument("records", type=Path)
    selection.add_argument("--direction", choices=("max", "min"), default="max")
    args = parser.parse_args(argv)
    try:
        if args.command == "plan":
            result = plan(args.budget, args.branches, args.unit)
        else:
            result = select(json.loads(args.records.read_text()), args.direction)
    except (ValueError, OSError) as exc:
        parser.exit(2, f"error: {exc}\n")
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
