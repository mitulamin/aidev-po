"""Tests for scripts/scorecard.py: per-run measures, the cause summary, update, check and add-run."""
import json
import shutil
import unittest

from helpers import FIXTURE, append_jsonl, copy_fixture, read_jsonl, run

import scorecard


def by_run(out):
    return {m["run"]: m for m in out["measures"]}


class Measures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = scorecard.compute(FIXTURE)
        cls.runs = by_run(cls.out)

    def test_feedback_per_100_items(self):
        actors = self.runs["run-20261202090000-b2b2"]
        self.assertEqual(actors["items_written"], 3)
        self.assertEqual(actors["feedback"], {"total": 1, "P0": 0, "P1": 0, "P2": 0, "P3": 1})
        self.assertEqual(actors["feedback_per_100_items"]["total"], 33.3)
        fsd = self.runs["run-20261204090000-d4d4"]
        self.assertEqual((fsd["feedback_per_100_items"]["P1"], fsd["p0_p1"]), (100.0, 1))

    def test_feedback_goes_to_the_rev_it_names(self):
        rerun = self.runs["run-20261210090000-e5e5"]
        self.assertEqual(rerun["items_written"], 3)
        self.assertEqual(rerun["feedback"]["total"], 0)

    def test_reviewer_catch_share(self):
        self.assertEqual(self.runs["run-20261202090000-b2b2"]["reviewer_catch_share"], 50.0)
        self.assertEqual(self.runs["run-20261204090000-d4d4"]["reviewer_catch_share"], 0.0)
        self.assertIsNone(self.runs["run-20261201090000-a1a1"]["reviewer_catch_share"])

    def test_origin_counted_where_it_began(self):
        self.assertEqual(self.runs["run-20261202090000-b2b2"]["origins_in_run"], 1)
        self.assertEqual(self.runs["run-20261204090000-d4d4"]["origins_in_run"], 0)
        self.assertEqual(self.runs["run-20261204090000-d4d4"]["attributions"], 1)
        self.assertEqual(self.runs["run-20261204090000-d4d4"]["confirmed_share"], 100.0)

    def test_repeat_cause_and_recurrence_after_edit(self):
        first = self.runs["run-20261202090000-b2b2"]
        again = self.runs["run-20261221090000-a7a7"]
        self.assertEqual((first["repeat_causes"], first["recurrence_after_edit"]), (0, 0))
        self.assertEqual((again["repeat_causes"], again["repeat_cause_rate"], again["recurrence_after_edit"]), (1, 100.0, 1))
        cause = self.out["causes"][0]
        self.assertEqual((cause["cause"], cause["agent"], cause["count"], cause["runs"], cause["after_edit"]),
                         ("unsupported-inference", "actors-producer", 2, 2, 1))
        self.assertEqual(cause["products"], ["clinic-booking", "team-rota"])

    def test_summary(self):
        s = self.out["summary"]
        self.assertEqual((s["runs"], s["items_written"], s["feedback"]["total"]), (7, 11, 3))
        self.assertEqual(s["feedback_per_100_items"], 27.3)
        self.assertEqual(s["repeat_cause_rate"], 50.0)
        self.assertEqual(s["trace_complete_pct"], 100.0)
        self.assertEqual((s["recurrence_after_edit"], s["held_out_regressions"]), (1, 0))

    def test_questions_per_gate(self):
        actors = [x for x in self.out["stages"] if x["product"] == "clinic-booking" and x["stage"] == "actors"][0]
        self.assertEqual((actors["gates"], actors["questions"], actors["questions_per_gate"]), (2, 1, 0.5))

    def test_one_product(self):
        out = scorecard.compute(FIXTURE, "team-rota")
        self.assertEqual({m["product"] for m in out["measures"]}, {"team-rota"})
        self.assertEqual(out["summary"]["items_written"], 2)


class Exclusions(unittest.TestCase):
    def setUp(self):
        self.repo = copy_fixture()

    def tearDown(self):
        shutil.rmtree(self.repo.parent)

    def test_rejected_attribution_not_counted(self):
        path = self.repo / "team-rota" / ".po" / "attributions.jsonl"
        at = read_jsonl(path)[-1]
        at["user_verdict"] = "rejected"
        append_jsonl(path, at)
        runs = by_run(scorecard.compute(self.repo))
        self.assertEqual(runs["run-20261221090000-a7a7"]["origins_in_run"], 0)
        self.assertEqual(runs["run-20261221090000-a7a7"]["recurrence_after_edit"], 0)

    def test_input_changed_is_not_a_repeat(self):
        path = self.repo / "team-rota" / ".po" / "attributions.jsonl"
        at = read_jsonl(path)[-1]
        at["cause"] = "input-changed"
        append_jsonl(path, at)
        runs = by_run(scorecard.compute(self.repo))
        self.assertEqual(runs["run-20261221090000-a7a7"]["repeat_causes"], 0)

    def test_withdrawn_feedback_not_counted(self):
        path = self.repo / "clinic-booking" / ".po" / "feedback.jsonl"
        fb = read_jsonl(path)[1]
        fb["withdrawn"] = True
        append_jsonl(path, fb)
        runs = by_run(scorecard.compute(self.repo))
        self.assertEqual(runs["run-20261202090000-b2b2"]["feedback"]["total"], 0)


class ScorecardFile(unittest.TestCase):
    def setUp(self):
        self.repo = copy_fixture()

    def tearDown(self):
        shutil.rmtree(self.repo.parent)

    def test_update_add_run_check(self):
        code, _, err = run("scorecard.py", "update", "--repo", self.repo)
        self.assertEqual(code, 0, err)
        for run_id, total in (("run-20261202090000-b2b2", "2,2,2,2,1"), ("run-20261221090000-a7a7", "2,2,1,2,1")):
            scores = ",".join(f"{c}={v}" for c, v in zip(scorecard.CRITERIA, total.split(",")))
            code, out, err = run("scorecard.py", "add-run", "--repo", self.repo, "--skill", "trace-records", "--stage", "all",
                                 "--run", run_id, "--scores", scores, "--date", "2026-12-21")
            self.assertEqual(code, 0, err)
        doc = json.loads((self.repo / ".po" / "scorecard.json").read_text())
        self.assertEqual(doc["summary"]["feedback_per_100_items"], 27.3)
        self.assertEqual([r["total"] for r in doc["skills"][0]["runs"]], [9, 8])
        code, out, err = run("scorecard.py", "check", "--repo", self.repo)
        self.assertEqual(code, 0, err)
        self.assertIn("trace-records: runs point to keep", out)
        code, _, _ = run("scorecard.py", "update", "--repo", self.repo)
        self.assertEqual(json.loads((self.repo / ".po" / "scorecard.json").read_text())["skills"], doc["skills"])

    def test_check_catches_wrong_total(self):
        path = self.repo / ".po" / "scorecard.json"
        path.write_text(json.dumps({"schema_version": "1.0.0", "skills": [
            {"skill_name": "feedback-intake", "stage": "all", "verdict": None, "runs": [
                {"run_id": "r1", "date": "2026-12-21", "scores": dict.fromkeys(scorecard.CRITERIA, 1), "total": 7, "harm_flag": False}]}]}))
        code, _, err = run("scorecard.py", "check", "--repo", self.repo)
        self.assertEqual(code, 1)
        self.assertIn("total 7 is not the sum of the scores (5)", err)

    def test_bad_scores_rejected(self):
        code, _, err = run("scorecard.py", "add-run", "--repo", self.repo, "--skill", "x", "--stage", "all", "--run", "r",
                           "--scores", "triggered=3,followed=1,reviewer_caught=1,outcome=1,cost=1")
        self.assertNotEqual(code, 0)


class Suggest(unittest.TestCase):
    def row(self, *totals, harm=False, triggered=2):
        return {"runs": [{"total": t, "harm_flag": harm, "scores": {"triggered": triggered}} for t in totals]}

    def test_rules(self):
        self.assertEqual(scorecard.suggest(self.row(8, 7))[0], "keep")
        self.assertEqual(scorecard.suggest(self.row(8))[0], None)
        self.assertEqual(scorecard.suggest(self.row(8, 9, harm=True))[0], None)
        self.assertEqual(scorecard.suggest(self.row(4, 3))[0], "drop")
        self.assertEqual(scorecard.suggest(self.row(8, 8, triggered=0))[0], "drop")


if __name__ == "__main__":
    unittest.main()
