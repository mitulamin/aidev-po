"""The lists written out in skills, agents and templates match the schemas they describe."""
import json
import unittest

from helpers import ROOT


def schema(name):
    return json.loads((ROOT / "schemas" / name).read_text(encoding="utf-8"))


def text(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


class Sync(unittest.TestCase):
    def test_trace_records_lists_every_item_type(self):
        skill = text("skills/trace-records/SKILL.md")
        for name, prefix in schema("trace.schema.json")["x-item-types"].items():
            self.assertIn(f"{name}: {prefix}", skill)

    def test_nine_categories_everywhere(self):
        cats = schema("feedback.schema.json")["x-categories"]
        self.assertEqual(len(cats), 9)
        for rel in ("skills/feedback-intake/SKILL.md", "templates/learning/feedback-comment.md"):
            body = text(rel)
            for c in cats:
                self.assertIn(f"`{c}`", body, rel)

    def test_tracer_lists_every_cause(self):
        body = text("agents/tracer.md")
        for c in schema("attribution.schema.json")["x-causes"]:
            self.assertIn(f"`{c}`", body)

    def test_scorecard_criteria_match_script(self):
        import scorecard
        props = schema("scorecard.schema.json")["properties"]["skills"]["items"]["properties"]["runs"]["items"]["properties"]
        self.assertEqual(tuple(props["scores"]["required"]), scorecard.CRITERIA)


if __name__ == "__main__":
    unittest.main()
