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

    def test_no_pull_request_leftovers(self):
        markers = ("PR 3", "arrive in later pull requests", "Lock Sheet", "run_summary_for_pr3")
        for folder in ("agents", "commands", "skills", "templates", "docs"):
            for path in (ROOT / folder).rglob("*.md"):
                body = path.read_text(encoding="utf-8")
                for m in markers:
                    self.assertNotIn(m, body, f"{path.relative_to(ROOT)}: {m}")
        for rel in ("AGENTS.md", "README.md", "templates/product-state.example.json"):
            for m in markers:
                self.assertNotIn(m, text(rel), f"{rel}: {m}")

    def test_fsd_template_cites_29148_without_clauses(self):
        body = text("templates/08-fsd.md")
        self.assertNotIn("29148 §", body)
        self.assertIn("### 5.3 Data & Information Requirements", body)
        self.assertIn("## 10. Definitions / Glossary", body)

    def test_scorecard_criteria_match_script(self):
        import scorecard
        props = schema("scorecard.schema.json")["properties"]["skills"]["items"]["properties"]["runs"]["items"]["properties"]
        self.assertEqual(tuple(props["scores"]["required"]), scorecard.CRITERIA)


if __name__ == "__main__":
    unittest.main()
