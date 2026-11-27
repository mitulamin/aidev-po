"""The worked example in examples/ passes every check, and every line validates against its schema."""
import json
import unittest

from helpers import ROOT, read_jsonl, run

try:
    import jsonschema
except ImportError:
    jsonschema = None

EXAMPLES = ROOT / "examples"
PRODUCTS = sorted(p for p in EXAMPLES.iterdir() if p.is_dir() and not p.name.startswith("."))
FILES = {
    "traces.jsonl": "trace.schema.json",
    "feedback.jsonl": "feedback.schema.json",
    "attributions.jsonl": "attribution.schema.json",
    "reruns.jsonl": "rerun.schema.json",
    "register.jsonl": "register.schema.json",
}


def validator(name):
    schema = json.loads((ROOT / "schemas" / name).read_text(encoding="utf-8"))
    return jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())


class Checks(unittest.TestCase):
    def test_has_a_product(self):
        self.assertTrue(PRODUCTS, "examples/ has no product folder")

    def test_traces(self):
        code, out, err = run("traces.py", "check", "--all", "--repo", EXAMPLES)
        self.assertEqual(code, 0, out + err)
        self.assertNotIn("warning", out + err)

    def test_registers(self):
        for product in PRODUCTS:
            code, out, err = run("register.py", "check", "--register", product / ".po" / "register.jsonl")
            self.assertEqual(code, 0, f"{product.name}: {out}{err}")

    def test_scorecard(self):
        code, out, err = run("scorecard.py", "check", "--repo", EXAMPLES)
        self.assertEqual(code, 0, out + err)

    def test_learning_loop_is_complete(self):
        for product in PRODUCTS:
            po = product / ".po"
            fb = read_jsonl(po / "feedback.jsonl")
            ats = read_jsonl(po / "attributions.jsonl")
            rrs = read_jsonl(po / "reruns.jsonl")
            self.assertTrue(fb and ats and rrs, product.name)
            self.assertTrue(any(a.get("alternatives") for a in ats), "an attribution with alternatives")
            self.assertTrue(any(a.get("user_verdict") for a in ats), "an attribution the user ruled on")
            self.assertIn("committed", {r["status"] for r in rrs})
            for at in {a["id"] for a in ats}:
                self.assertTrue(any((po / "tracer").glob(f"*-{at}.md")), f"tracer report for {at}")


    def test_fb002_is_open_feedback_for_the_next_retro(self):
        code, out, err = run("traces.py", "open-feedback", "--all", "--json", "--repo", EXAMPLES)
        self.assertEqual(code, 0, out + err)
        self.assertEqual([(f["product"], f["id"]) for f in json.loads(out)], [("tool-library-loans", "FB-002")])


@unittest.skipIf(jsonschema is None, "jsonschema not installed")
class Lines(unittest.TestCase):
    def test_product_files(self):
        for product in PRODUCTS:
            for fname, schema in FILES.items():
                path = product / ".po" / fname
                if not path.exists():
                    continue
                v = validator(schema)
                for n, obj in enumerate(read_jsonl(path), 1):
                    errs = [e.message for e in v.iter_errors(obj)]
                    self.assertEqual(errs, [], f"{product.name}/{fname}:{n}")

    def test_ledger(self):
        v = validator("ledger.schema.json")
        for n, obj in enumerate(read_jsonl(EXAMPLES / ".po" / "ledger.jsonl"), 1):
            self.assertEqual([e.message for e in v.iter_errors(obj)], [], f"ledger:{n}")

    def test_scorecard(self):
        doc = json.loads((EXAMPLES / ".po" / "scorecard.json").read_text(encoding="utf-8"))
        self.assertEqual([e.message for e in validator("scorecard.schema.json").iter_errors(doc)], [])


if __name__ == "__main__":
    unittest.main()
