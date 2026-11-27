"""Every fixture line validates against its schema, and the schemas reject the obvious mistakes."""
import json
import unittest

from helpers import FIXTURE, ROOT, read_jsonl

try:
    import jsonschema
except ImportError:
    jsonschema = None

FILES = {
    "trace.jsonl": "trace.schema.json",
    "feedback.jsonl": "feedback.schema.json",
    "attributions.jsonl": "attribution.schema.json",
    "reruns.jsonl": "rerun.schema.json",
    "register.jsonl": "register.schema.json",
}


def validator(name):
    schema = json.loads((ROOT / "schemas" / name).read_text(encoding="utf-8"))
    return jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())


@unittest.skipIf(jsonschema is None, "jsonschema not installed")
class FixtureLines(unittest.TestCase):
    def test_product_files(self):
        for product in ("clinic-booking", "team-rota"):
            for fname, schema in FILES.items():
                path = FIXTURE / product / ".po" / fname
                if not path.exists():
                    continue
                v = validator(schema)
                for n, obj in enumerate(read_jsonl(path), 1):
                    errs = [e.message for e in v.iter_errors(obj)]
                    self.assertEqual(errs, [], f"{product}/{fname}:{n}")

    def test_ledger(self):
        v = validator("ledger.schema.json")
        for n, obj in enumerate(read_jsonl(FIXTURE / ".po" / "ledger.jsonl"), 1):
            self.assertEqual([e.message for e in v.iter_errors(obj)], [], f"ledger:{n}")


@unittest.skipIf(jsonschema is None, "jsonschema not installed")
class Rejects(unittest.TestCase):
    def first(self, fname, product="clinic-booking"):
        return read_jsonl(FIXTURE / product / ".po" / fname)[0]

    def test_feedback_category_and_severity(self):
        v = validator("feedback.schema.json")
        fb = self.first("feedback.jsonl")
        self.assertFalse(v.is_valid(dict(fb, category="typo")))
        self.assertFalse(v.is_valid(dict(fb, severity="P4")))
        schema = json.loads((ROOT / "schemas" / "feedback.schema.json").read_text())
        self.assertEqual(len(schema["properties"]["category"]["enum"]), 9)
        self.assertEqual(sorted(schema["properties"]["category"]["enum"]), sorted(schema["x-categories"]))

    def test_trace_needs_evidence_tag_and_good_id(self):
        v = validator("trace.schema.json")
        line = self.first("trace.jsonl")
        self.assertFalse(v.is_valid(dict(line, evidence={"tag": "Guessed"})))
        self.assertFalse(v.is_valid(dict(line, item_id="PRB-1")))
        self.assertFalse(v.is_valid({k: x for k, x in line.items() if k != "upstream"}))

    def test_attribution_causes(self):
        v = validator("attribution.schema.json")
        at = self.first("attributions.jsonl")
        self.assertFalse(v.is_valid(dict(at, cause="bad-luck")))
        self.assertFalse(v.is_valid(dict(at, confidence=1.5)))
        schema = json.loads((ROOT / "schemas" / "attribution.schema.json").read_text())
        self.assertEqual(sorted(schema["$defs"]["cause"]["enum"]), sorted(schema["x-causes"]))

    def test_register_feedback_needs_record(self):
        v = validator("register.schema.json")
        line = [l for l in read_jsonl(FIXTURE / "clinic-booking" / ".po" / "register.jsonl") if l.get("type") == "feedback"][0]
        self.assertTrue(v.is_valid(line))
        self.assertFalse(v.is_valid({k: x for k, x in line.items() if k != "record"}))


if __name__ == "__main__":
    unittest.main()
