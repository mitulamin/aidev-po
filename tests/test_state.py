"""Product state: the depth field in the schema, the template and the worked example, and where po and the briefs use it."""
import json
import unittest

from helpers import ROOT

try:
    import jsonschema
except ImportError:
    jsonschema = None

SCHEMA = ROOT / "schemas" / "product-state.schema.json"
TEMPLATE = ROOT / "templates" / "product-state.example.json"
EXAMPLE = ROOT / "examples" / "tool-library-loans" / ".po" / "state.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


class Depth(unittest.TestCase):
    def test_depth_values(self):
        self.assertEqual(load(SCHEMA)["properties"]["depth"]["enum"], ["thin", "full"])
        self.assertIn("depth", load(SCHEMA)["required"])

    def test_template_and_example_have_depth(self):
        for path in (TEMPLATE, EXAMPLE):
            self.assertIn(load(path).get("depth"), ("thin", "full"), path)

    def test_po_writes_depth_and_puts_it_in_briefs(self):
        po = (ROOT / "agents" / "po.md").read_text(encoding="utf-8")
        self.assertIn("`depth` set to the agreed choice", po)
        self.assertIn("Depth from `.po/state.json`", po)
        for rel in ("agents/fsd-producer.md", "agents/fsd-reviewer.md"):
            self.assertIn("depth", (ROOT / rel).read_text(encoding="utf-8"), rel)

    def test_template_note_is_neutral(self):
        self.assertNotIn("PR 3", TEMPLATE.read_text(encoding="utf-8"))


@unittest.skipIf(jsonschema is None, "jsonschema not installed")
class StateSchema(unittest.TestCase):
    def setUp(self):
        self.v = jsonschema.Draft202012Validator(load(SCHEMA))

    def test_template_and_example_validate(self):
        for path in (TEMPLATE, EXAMPLE):
            self.assertEqual([e.message for e in self.v.iter_errors(load(path))], [], path)

    def test_rejects_missing_or_unknown_depth(self):
        state = load(TEMPLATE)
        self.assertFalse(self.v.is_valid({k: x for k, x in state.items() if k != "depth"}))
        self.assertFalse(self.v.is_valid(dict(state, depth="medium")))
        self.assertTrue(self.v.is_valid(dict(state, depth="thin")))


if __name__ == "__main__":
    unittest.main()
