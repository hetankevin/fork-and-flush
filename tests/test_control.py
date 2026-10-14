import importlib.util
import itertools
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("control", ROOT / "skills/fork-and-flush/scripts/control.py")
control = importlib.util.module_from_spec(spec)
spec.loader.exec_module(control)


def record(checkpoint, score, valid=True, lineage="worker"):
    return dict(checkpoint=checkpoint, lineage=lineage, score=score, valid=valid,
                artifact="archive/" + checkpoint, evidence="logs/" + checkpoint)


class ScheduleTests(unittest.TestCase):
    def test_paper_schedule(self):
        result = control.plan(1000)
        self.assertEqual([p["allocation"] for p in result["phases"]], [240, 90, 240, 90, 240, 100])
        self.assertEqual([p["start"] for p in result["phases"][::2]], [0, 330, 660])

    def test_budget_conservation_across_rounding(self):
        for budget in range(100, 300):
            result = control.plan(budget, overhead=17)
            phases = result["phases"]
            self.assertEqual(sum(p["allocation"] for p in phases) + 17, budget)
            for first, second in zip(phases, phases[1:]):
                self.assertEqual(first["end"], second["start"])
            for phase in phases:
                self.assertEqual(phase["workers"] * phase["per_worker"], phase["allocation"])
                self.assertGreater(phase["per_worker"], 0)

    def test_reject_impossible_budgets(self):
        for args in [(0,), (10,), (100, 100), (100, -1), (1000, 0, 6), (True,), (10.5,)]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                control.plan(*args)

    def test_flush_only_is_explicit(self):
        result = control.plan(1000, branches=1)
        self.assertEqual(result["branches"], 1)
        self.assertEqual(result["phases"][0]["allocation"], 60)


class SelectionTests(unittest.TestCase):
    def select(self, records, incumbent=None, direction="max"):
        return control.select(dict(schema_version=1, records=records, incumbent=incumbent), direction)["winner"]["checkpoint"]

    def test_best_ever_not_last_and_invalid_never_wins(self):
        records = [record("best", 12), record("last", 3), record("bad", 999, False)]
        for ordered in itertools.permutations(records):
            self.assertEqual(self.select(list(ordered)), "best")

    def test_minimization_and_negative_scores(self):
        self.assertEqual(self.select([record("a", -3), record("b", -5)], direction="min"), "b")

    def test_incumbent_survives_failed_round(self):
        self.assertEqual(self.select([record("base", 5), record("bad", None, False)], "base"), "base")

    def test_tie_preserves_incumbent_then_stable_identifier(self):
        records = [record("z", 10), record("a", 10)]
        for ordered in itertools.permutations(records):
            self.assertEqual(self.select(list(ordered), "z"), "z")
            self.assertEqual(self.select(list(ordered)), "a")

    def test_no_winner_without_valid_evidence(self):
        for records in [[], [record("bad", None, False)]]:
            with self.assertRaises(ValueError):
                self.select(records)

    def test_reject_broken_records(self):
        variants = [dict(score=float("nan")), dict(score=float("inf")), dict(score=True),
                    dict(valid="false"), dict(score=None), dict(artifact=""), dict(evidence="")]
        for update in variants:
            candidate = record("a", 1)
            candidate.update(update)
            with self.subTest(update=update), self.assertRaises(ValueError):
                self.select([candidate])
        with self.assertRaises(ValueError):
            self.select([record("a", 1), record("a", 2)])
        with self.assertRaises(ValueError):
            self.select([record("a", 1)], "missing")
        with self.assertRaises(ValueError):
            control.select({"schema_version": 2, "records": []})


if __name__ == "__main__":
    unittest.main()
