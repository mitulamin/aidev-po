"""Tests for scripts/traces.py: IDs, trace checks, appends, chain, downstream and locate."""
import json
import shutil
import unittest

from helpers import FIXTURE, ROOT, append_jsonl, copy_fixture, read_jsonl, run

import traces

RUN = "run-20261230090000-abcd"


def write_line(**over):
    line = {"event": "write", "item_type": "actor", "run": RUN, "stage": "actors", "agent": "actors-producer",
            "role": "producer", "step": "2-actor-sweep", "file": "03-actors.md", "summary": "Auditor: reads bookings.",
            "upstream_ids": ["IDEA-001"], "register_refs": [], "evidence_tag": "Inferred", "skill_versions": {"trace-records": "b11bf9d"},
            "template_versions": {}, "aidev_po": "b11bf9d"}
    line.update(over)
    return line


class FixtureIsValid(unittest.TestCase):
    def test_fixture_checks_clean(self):
        code, out, err = run("traces.py", "check", "--all", "--repo", FIXTURE)
        self.assertEqual(code, 0, err)
        self.assertNotIn("error", err)

    def test_item_types_match_schema_enum(self):
        schema = json.loads((traces.SCHEMAS / "trace.schema.json").read_text())
        self.assertEqual(sorted(schema["$defs"]["item_type"]["enum"]), sorted(schema["x-item-types"]))
        prefixes = list(schema["x-item-types"].values())
        self.assertEqual(len(prefixes), len(set(prefixes)), "prefixes must be unique")
        for p in prefixes:
            self.assertRegex(p, r"^[A-Z]{2,4}$")


class Checks(unittest.TestCase):
    def setUp(self):
        self.repo = copy_fixture()
        self.product = self.repo / "clinic-booking"
        self.trace = self.product / ".po" / "traces.jsonl"

    def tearDown(self):
        shutil.rmtree(self.repo.parent)

    def errors(self):
        code, _, err = run("traces.py", "check", "--dir", self.product)
        return code, [l for l in err.splitlines() if l.startswith("error:")]

    def test_untraced_id_in_markdown(self):
        with (self.product / "03-actors.md").open("a") as fh:
            fh.write("| ACT-009 | Auditor | Check bookings | Read only | Assumed |\n")
        code, errs = self.errors()
        self.assertEqual(code, 1)
        self.assertTrue(any("ACT-009 has no trace record" in e for e in errs), errs)

    def test_traced_item_missing_from_file(self):
        append_jsonl(self.trace, write_line(item_id="ACT-004", rev=1, ts="2026-12-30T09:00:00Z"))
        _, errs = self.errors()
        self.assertTrue(any("ACT-004: ID does not appear in 03-actors.md" in e for e in errs), errs)

    def test_prefix_must_match_type(self):
        append_jsonl(self.trace, write_line(item_id="REQ-009", rev=1, ts="2026-12-30T09:00:00Z"))
        _, errs = self.errors()
        self.assertTrue(any("prefix REQ does not match item_type actor" in e for e in errs), errs)

    def test_no_source_is_an_error(self):
        with (self.product / "03-actors.md").open("a") as fh:
            fh.write("| ACT-004 | Auditor | Check | Read | Inferred |\n")
        append_jsonl(self.trace, write_line(item_id="ACT-004", rev=1, ts="2026-12-30T09:00:00Z", upstream_ids=[]))
        _, errs = self.errors()
        self.assertTrue(any("no upstream_ids and no register_refs" in e for e in errs), errs)

    def test_rev_order_and_reuse(self):
        append_jsonl(self.trace, write_line(item_id="ACT-001", rev=3, ts="2026-12-30T09:00:00Z"))
        _, errs = self.errors()
        self.assertTrue(any("ACT-001: rev 3 out of order, expected 2" in e for e in errs), errs)

    def test_written_after_remove(self):
        append_jsonl(self.trace, {"event": "remove", "item_id": "ACT-002", "rev": 2, "ts": "2026-12-30T09:00:00Z", "run": RUN,
                                  "stage": "actors", "agent": "actors-producer", "role": "producer", "reason": "merged"})
        append_jsonl(self.trace, write_line(item_id="ACT-002", rev=3, ts="2026-12-30T09:01:00Z"))
        _, errs = self.errors()
        self.assertTrue(any("written after it was removed" in e for e in errs), errs)

    def test_unknown_register_ref(self):
        with (self.product / "03-actors.md").open("a") as fh:
            fh.write("| ACT-004 | Auditor | Check | Read | Stated |\n")
        append_jsonl(self.trace, write_line(item_id="ACT-004", rev=1, ts="2026-12-30T09:00:00Z",
                                            register_refs=["r-20261230000000-ffff"], evidence_tag="Stated"))
        _, errs = self.errors()
        self.assertTrue(any("not declared in the register" in e for e in errs), errs)

    def test_validated_needs_sources(self):
        with (self.product / "03-actors.md").open("a") as fh:
            fh.write("| ACT-004 | Auditor | Check | Read | Validated |\n")
        append_jsonl(self.trace, write_line(item_id="ACT-004", rev=1, ts="2026-12-30T09:00:00Z", evidence_tag="Validated"))
        _, errs = self.errors()
        self.assertTrue(any("tagged Validated with no sources" in e for e in errs), errs)

    def test_cycle(self):
        for item, up in (("ACT-004", "ACT-005"), ("ACT-005", "ACT-004")):
            with (self.product / "03-actors.md").open("a") as fh:
                fh.write(f"| {item} | x | x | x | Inferred |\n")
        append_jsonl(self.trace, write_line(item_id="ACT-004", rev=1, ts="2026-12-30T09:00:00Z"))
        append_jsonl(self.trace, write_line(item_id="ACT-005", rev=1, ts="2026-12-30T09:01:00Z", upstream_ids=["ACT-004"]))
        append_jsonl(self.trace, write_line(item_id="ACT-004", rev=2, ts="2026-12-30T09:02:00Z", upstream_ids=["ACT-005"]))
        _, errs = self.errors()
        self.assertTrue(any("upstream cycle" in e for e in errs), errs)

    def test_low_confidence_needs_question(self):
        path = self.product / ".po" / "attributions.jsonl"
        at = read_jsonl(path)[-1]
        at.update(confidence=0.3, user_verdict=None)
        append_jsonl(path, at)
        _, errs = self.errors()
        self.assertTrue(any("needs question_for_user" in e for e in errs), errs)

    def test_attribution_step_must_match_trace(self):
        path = self.product / ".po" / "attributions.jsonl"
        at = read_jsonl(path)[-1]
        at["origin"] = dict(at["origin"], agent="scope-producer")
        append_jsonl(path, at)
        _, errs = self.errors()
        self.assertTrue(any("agent 'scope-producer' does not match the trace of ACT-003 rev 1" in e for e in errs), errs)

    def test_rerun_needs_user_ok(self):
        path = self.product / ".po" / "reruns.jsonl"
        rr = read_jsonl(path)[0]
        rr.update(status="approved")
        append_jsonl(path, rr)
        _, errs = self.errors()
        self.assertTrue(any("without user_ok" in e for e in errs), errs)

    def test_duplicate_pr_comment(self):
        path = self.product / ".po" / "feedback.jsonl"
        fb = read_jsonl(path)[1]
        fb["id"] = "FB-003"
        append_jsonl(path, fb)
        _, errs = self.errors()
        self.assertTrue(any("PR comment 1001 was already taken in as FB-002" in e for e in errs), errs)

    def test_accepted_ledger_edit_with_regression(self):
        path = self.repo / ".po" / "ledger.jsonl"
        le = read_jsonl(path)[1]
        le.update(decision="accepted", id="LE-003")
        append_jsonl(path, le)
        code, _, err = run("traces.py", "check", "--all", "--repo", self.repo)
        self.assertEqual(code, 1)
        self.assertIn("LE-003: accepted, but learn-reviewer did not PASS it", err)
        self.assertIn("LE-003: accepted with held-out regressions", err)


class Add(unittest.TestCase):
    def setUp(self):
        self.repo = copy_fixture()
        self.product = self.repo / "clinic-booking"

    def tearDown(self):
        shutil.rmtree(self.repo.parent)

    def test_next_ids(self):
        self.assertEqual(run("traces.py", "next-id", "actor", "--dir", self.product)[1].strip(), "ACT-004")
        self.assertEqual(run("traces.py", "next-id", "REQ", "--dir", self.product)[1].strip(), "REQ-002")
        self.assertEqual(run("traces.py", "next-id", "presentation-item", "--dir", self.product)[1].strip(), "PRS-001")
        self.assertEqual(run("traces.py", "next-id", "FB", "--dir", self.product)[1].strip(), "FB-003")
        self.assertEqual(run("traces.py", "next-id", "LE", "--repo", self.repo)[1].strip(), "LE-003")

    def test_add_fills_id_rev_ts(self):
        with (self.product / "03-actors.md").open("a") as fh:
            fh.write("| ACT-004 | Auditor | Check bookings | Read only | Inferred |\n")
        line = write_line()
        code, out, err = run("traces.py", "add", "trace", "--dir", self.product, "--json", json.dumps(line))
        self.assertEqual(code, 0, err)
        self.assertEqual(out.strip(), "ACT-004 rev 1")
        last = read_jsonl(self.product / ".po" / "traces.jsonl")[-1]
        self.assertEqual((last["item_id"], last["rev"]), ("ACT-004", 1))
        self.assertIn("ts", last)

    def test_add_rewrite_gets_next_rev(self):
        line = write_line(item_id="ACT-002", summary="Receptionist: rebooks a missed slot in under a minute.")
        code, out, err = run("traces.py", "add", "trace", "--dir", self.product, "--json", json.dumps(line))
        self.assertEqual(code, 0, err)
        self.assertEqual(out.strip(), "ACT-002 rev 2")

    def test_add_refuses_bad_line_and_appends_nothing(self):
        before = (self.product / ".po" / "traces.jsonl").read_text()
        line = write_line(upstream_ids=["ACT-099"])
        code, _, err = run("traces.py", "add", "trace", "--dir", self.product, "--json", json.dumps(line))
        self.assertEqual(code, 1)
        self.assertIn("nothing appended", err)
        self.assertEqual((self.product / ".po" / "traces.jsonl").read_text(), before)

    def test_add_several_lines_from_stdin(self):
        with (self.product / "03-actors.md").open("a") as fh:
            fh.write("| ACT-004 | Auditor | x | x | Inferred |\n| ACT-005 | Insurer | x | x | Inferred |\n")
        lines = "\n".join(json.dumps(write_line(summary=s)) for s in ("Auditor", "Insurer"))
        code, out, err = run("traces.py", "add", "trace", "--dir", self.product, stdin=lines)
        self.assertEqual(code, 0, err)
        self.assertEqual(out.split("\n")[:2], ["ACT-004 rev 1", "ACT-005 rev 1"])

    def test_add_feedback(self):
        fb = {"source": "command", "target": {"level": "item", "item_ids": ["ACT-001"], "item_revs": {"ACT-001": 1}},
              "severity": "P2", "category": "missing", "text": "Where is the practice owner?"}
        code, out, err = run("traces.py", "add", "feedback", "--dir", self.product, "--json", json.dumps(fb))
        self.assertEqual(code, 0, err)
        self.assertEqual(out.strip(), "FB-003")
        self.assertIn("no register line of type feedback", err)

    def test_add_feedback_bad_category(self):
        fb = {"source": "command", "target": {"level": "item", "item_ids": ["ACT-001"]},
              "severity": "P2", "category": "typo", "text": "x"}
        code, _, err = run("traces.py", "add", "feedback", "--dir", self.product, "--json", json.dumps(fb))
        if traces.validator("feedback") is None:
            self.skipTest("jsonschema not installed")
        self.assertEqual(code, 1, err)

    def test_add_ledger_rejects_unproven_acceptance(self):
        le = read_jsonl(self.repo / ".po" / "ledger.jsonl")[0]
        del le["id"]
        le["held_in"] = {"cases": ["clinic-booking/FB-001"], "before": 1, "after": 1}
        code, _, err = run("traces.py", "add", "ledger", "--repo", self.repo, "--json", json.dumps(le))
        self.assertEqual(code, 1)
        self.assertIn("held-in cases did not improve", err)


class OpenFeedback(unittest.TestCase):
    """What /po-retro traces first: feedback with no attribution."""

    def test_fixture_gap(self):
        code, out, err = run("traces.py", "open-feedback", "--all", "--json", "--repo", FIXTURE)
        self.assertEqual(code, 0, err)
        self.assertEqual([(r["product"], r["id"], r["severity"]) for r in json.loads(out)], [("clinic-booking", "FB-002", "P3")])

    def test_traced_and_withdrawn_are_not_open(self):
        product = copy_fixture()
        self.addCleanup(shutil.rmtree, product.parent)
        fb = read_jsonl(product / "clinic-booking" / ".po" / "feedback.jsonl")[1]
        append_jsonl(product / "clinic-booking" / ".po" / "feedback.jsonl", dict(fb, ts="2026-12-30T09:00:00Z", withdrawn=True))
        code, out, _ = run("traces.py", "open-feedback", "--all", "--json", "--repo", product)
        self.assertEqual(json.loads(out), [])

    def test_one_product(self):
        code, out, _ = run("traces.py", "open-feedback", "--dir", FIXTURE / "team-rota")
        self.assertIn("0 feedback line(s)", out)

    def test_catch_up_fixture(self):
        code, out, err = run("traces.py", "open-feedback", "--catch-up", "--all", "--json", "--repo", FIXTURE)
        self.assertEqual(code, 0, err)
        doc = json.loads(out)
        self.assertEqual([(r["product"], r["id"]) for r in doc["open"]], [("clinic-booking", "FB-002")])
        self.assertEqual([(r["product"], r["id"]) for r in doc["traced_not_fixed"]], [("team-rota", "FB-001")])
        self.assertEqual((doc["waiting_attributions"], doc["unfinished_reruns"]), ([], []))

    def test_catch_up_lists_waiting_attribution_and_unfinished_rerun(self):
        repo = copy_fixture()
        self.addCleanup(shutil.rmtree, repo.parent)
        po = repo / "clinic-booking" / ".po"
        at = read_jsonl(po / "attributions.jsonl")[-1]
        append_jsonl(po / "attributions.jsonl", dict(at, id="AT-009", ts="2026-12-30T09:00:00Z", user_verdict=None))
        rr = read_jsonl(po / "reruns.jsonl")[-1]
        append_jsonl(po / "reruns.jsonl", dict(rr, id="RR-009", ts="2026-12-30T09:05:00Z", status="planned"))
        code, out, err = run("traces.py", "open-feedback", "--catch-up", "--json", "--dir", repo / "clinic-booking")
        self.assertEqual(code, 0, err)
        doc = json.loads(out)
        self.assertIn("AT-009", [r["id"] for r in doc["waiting_attributions"]])
        self.assertEqual([(r["id"], r["status"]) for r in doc["unfinished_reruns"]], [("RR-009", "planned")])
        code, out, _ = run("traces.py", "open-feedback", "--catch-up", "--dir", repo / "clinic-booking")
        self.assertIn("1 rerun(s) not done", out)

    def test_continue_uses_catch_up(self):
        for rel in ("commands/continue.md", "agents/po.md"):
            self.assertIn("traces.py open-feedback --catch-up", (ROOT / rel).read_text(), rel)

    def test_retro_traces_open_feedback_first(self):
        text = (ROOT / "commands" / "retro.md").read_text()
        self.assertIn("traces.py open-feedback", text)
        self.assertLess(text.index("open-feedback"), text.index("**Set up.**"))


class Walks(unittest.TestCase):
    def test_chain_as_of_feedback(self):
        code, out, err = run("traces.py", "chain", "REQ-001", "--feedback", "FB-001", "--json",
                             "--dir", FIXTURE / "clinic-booking")
        self.assertEqual(code, 0, err)
        doc = json.loads(out)
        self.assertEqual(doc["nodes"]["REQ-001"]["rev"], 1)
        self.assertEqual(doc["nodes"]["ACT-003"]["rev"], 1)
        self.assertIn("delete", doc["nodes"]["ACT-003"]["summary"])
        self.assertEqual(doc["nodes"]["ACT-003"]["register_refs"][0]["answer_then"], "They look after users and tidy up old bookings.")
        self.assertEqual(set(doc["nodes"]), {"REQ-001", "US-001", "ACT-003", "ACT-001", "IDEA-001"})

    def test_chain_current(self):
        code, out, _ = run("traces.py", "chain", "REQ-001", "--json", "--dir", FIXTURE / "clinic-booking")
        self.assertEqual(json.loads(out)["nodes"]["ACT-003"]["rev"], 2)

    def test_downstream(self):
        code, out, _ = run("traces.py", "downstream", "ACT-003", "--json", "--dir", FIXTURE / "clinic-booking")
        doc = json.loads(out)
        self.assertEqual(doc["invalidated"], ["ACT-003", "US-001", "REQ-001"])
        self.assertEqual(doc["reopened_stages"], ["actors", "scope", "fsd"])

    def test_downstream_of_register_ref(self):
        code, out, _ = run("traces.py", "downstream", "IDEA-001", "--register-ref", "r-20261210085500-0003", "--json",
                           "--dir", FIXTURE / "clinic-booking")
        doc = json.loads(out)
        self.assertEqual(set(doc["invalidated"]), {"IDEA-001", "ACT-001", "ACT-002", "ACT-003", "US-001", "REQ-001"})

    def test_locate_line_and_quote(self):
        code, out, _ = run("traces.py", "locate", "03-actors.md", "--line", "6", "--dir", FIXTURE / "clinic-booking")
        self.assertEqual(json.loads(out)["item_ids"], ["ACT-002"])
        code, out, _ = run("traces.py", "locate", "08-fsd.md", "--quote", "shall not let anyone delete",
                           "--dir", FIXTURE / "clinic-booking")
        self.assertEqual(json.loads(out)["item_ids"], ["REQ-001"])


class Resolver(unittest.TestCase):
    def test_uses_products_dir_resolver(self):
        import os
        import subprocess
        import sys
        env = dict(os.environ, AIDEV_PO_PRODUCTS_DIR=str(FIXTURE))
        out = subprocess.run([sys.executable, str(traces.ROOT / "scripts" / "traces.py"), "check", "--product", "team-rota"],
                             capture_output=True, text=True, env=env)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("team-rota: ok", out.stdout)


if __name__ == "__main__":
    unittest.main()
