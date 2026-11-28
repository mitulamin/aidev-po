"""aidev-po and ai-sdlc-loop share one register taxonomy (DEC-002), so a register passes both checkers.

ai-sdlc-loop's checker and contract are vendored in tests/vendor/ai-sdlc-loop (pin in its README).
"""
import importlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from helpers import FIXTURE, ROOT, read_jsonl, run

try:
    import jsonschema
except ImportError:
    jsonschema = None

VENDOR = ROOT / "tests" / "vendor" / "ai-sdlc-loop"
BACK = ROOT / "tests" / "fixtures" / "ai-sdlc-loop" / "register-back.jsonl"
REGISTERS = sorted(ROOT.glob("examples/*/.po/register.jsonl")) + sorted(FIXTURE.glob("*/.po/register.jsonl"))
CONTRACT = json.loads((VENDOR / "data" / "agent-contract.json").read_text(encoding="utf-8"))
REG = CONTRACT["register"]
EXT = REG.get("extensions", {}).get("aidev-po", {})

register = importlib.import_module("register")


def sdlc_check(path, vendor=VENDOR):
    out = subprocess.run([sys.executable, str(vendor / "scripts" / "register.py"), "check", "--register", str(path)],
                         capture_output=True, text=True)
    return out.returncode, out.stdout + out.stderr


class AidevPoRegisterPassesAiSdlcLoop(unittest.TestCase):
    def test_registers_found(self):
        self.assertGreaterEqual(len(REGISTERS), 3)

    def test_every_aidev_po_register_passes_ai_sdlc_loop_check(self):
        for path in REGISTERS:
            code, out = sdlc_check(path)
            self.assertEqual(code, 0, f"{path.relative_to(ROOT)}: {out}")

    def test_baseline_lines_pass_without_the_extension(self):
        """Without register.extensions, ai-sdlc-loop's checker passes the baseline lines and rejects the rest."""
        tmp = Path(tempfile.mkdtemp(prefix="aidev-po-sdlc-"))
        try:
            vendor = tmp / "ai-sdlc-loop"
            shutil.copytree(VENDOR, vendor)
            contract = dict(CONTRACT, register={k: v for k, v in REG.items() if k != "extensions"})
            (vendor / "data" / "agent-contract.json").write_text(json.dumps(contract), encoding="utf-8")
            for path in REGISTERS:
                kept, lines = set(), []
                for rec in read_jsonl(path):
                    if rec["event"] == "declare" and rec["type"] in register.BASE_TYPES:
                        kept.add(rec["id"])
                        lines.append({k: v for k, v in rec.items() if k not in EXT.get("fields", {})})
                    elif rec["event"] == "update" and rec["ref"] in kept and rec["status"] in register.BASE_STATUSES:
                        lines.append(rec)
                base = tmp / f"{path.parent.parent.name}.jsonl"
                base.write_text("".join(json.dumps(r) + "\n" for r in lines), encoding="utf-8")
                code, out = sdlc_check(base, vendor)
                self.assertEqual(code, 0, f"{path.relative_to(ROOT)} baseline lines: {out}")
            code, _ = sdlc_check(ROOT / "examples" / "tool-library-loans" / ".po" / "register.jsonl", vendor)
            self.assertNotEqual(code, 0, "decision lines should need the extension")
        finally:
            shutil.rmtree(tmp)


class AiSdlcLoopRegisterPassesAidevPo(unittest.TestCase):
    def test_lines_written_by_ai_sdlc_loop_pass_both_checks(self):
        code, _, err = run("register.py", "check", "--register", BACK)
        self.assertEqual(code, 0, err)
        code, out = sdlc_check(BACK)
        self.assertEqual(code, 0, out)

    @unittest.skipIf(jsonschema is None, "jsonschema not installed")
    def test_lines_written_by_ai_sdlc_loop_match_the_schema(self):
        schema = json.loads((ROOT / "schemas" / "register.schema.json").read_text(encoding="utf-8"))
        v = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
        for n, rec in enumerate(read_jsonl(BACK), 1):
            self.assertEqual([e.message for e in v.iter_errors(rec)], [], f"line {n}")

    def test_round_trip_through_a_gate_bundle(self):
        """Copy the product register into a bundle, let ai-sdlc-loop append to it, merge it back."""
        tmp = Path(tempfile.mkdtemp(prefix="aidev-po-bundle-"))
        try:
            product = tmp / "register.jsonl"
            shutil.copy(FIXTURE / "clinic-booking" / ".po" / "register.jsonl", product)
            bundle = tmp / "bundle.jsonl"
            bundle.write_text(product.read_text(encoding="utf-8") + BACK.read_text(encoding="utf-8"), encoding="utf-8")
            self.assertEqual(sdlc_check(bundle)[0], 0)
            code, out, err = run("register.py", "merge", "--from", bundle, "--register", product)
            self.assertEqual(code, 0, err)
            self.assertIn("merged 5 new line(s)", out)
            code, out, err = run("register.py", "merge", "--from", bundle, "--register", product)
            self.assertIn("merged 0 new line(s)", out)
            self.assertEqual(product.read_text(encoding="utf-8"), bundle.read_text(encoding="utf-8"))
            self.assertEqual(run("register.py", "check", "--register", product)[0], 0)
            code, out, _ = run("register.py", "list", "--open", "--register", product)
            self.assertTrue(out.splitlines()[0].split()[2] == "blocker", out)
        finally:
            shutil.rmtree(tmp)

    def test_merge_writes_nothing_when_a_line_is_bad(self):
        tmp = Path(tempfile.mkdtemp(prefix="aidev-po-bundle-"))
        try:
            product = tmp / "register.jsonl"
            shutil.copy(FIXTURE / "team-rota" / ".po" / "register.jsonl", product)
            before = product.read_text(encoding="utf-8")
            bad = dict(read_jsonl(BACK)[0], id="r-20261215093000-a006", type="guess")
            bundle = tmp / "bundle.jsonl"
            bundle.write_text(BACK.read_text(encoding="utf-8") + json.dumps(bad) + "\n", encoding="utf-8")
            code, _, err = run("register.py", "merge", "--from", bundle, "--register", product)
            self.assertNotEqual(code, 0)
            self.assertIn("nothing merged", err)
            self.assertEqual(product.read_text(encoding="utf-8"), before)
        finally:
            shutil.rmtree(tmp)


class OneTaxonomy(unittest.TestCase):
    """aidev-po's register.py and schema say what the vendored ai-sdlc-loop contract says."""

    def test_baseline_values(self):
        self.assertEqual(list(register.BASE_TYPES), REG["types"])
        self.assertEqual(list(register.BASE_STATUSES), REG["statuses"]["values"])
        self.assertEqual(list(register.BY_VALUES), REG["by"])
        self.assertEqual(list(register.VIA_VALUES), REG["via"]["values"])
        self.assertEqual(list(register.LEVELS), REG["impact"]["values"])
        self.assertEqual(list(register.LEVELS), REG["urgency"]["values"])
        self.assertEqual(register.ID_RE.pattern, REG["id_pattern"])

    def test_fields(self):
        ext_fields = set(EXT.get("fields", {}))
        for event, req, opt in (("declare", register.DECLARE_REQUIRED, register.DECLARE_OPTIONAL),
                                ("update", register.UPDATE_REQUIRED, register.UPDATE_OPTIONAL)):
            spec = REG["events"][event]
            self.assertEqual(set(req), set(spec["required"]), event)
            mine_ext = {k for k, f in EXT.get("fields", {}).items() if f["event"] == event}
            self.assertEqual(set(opt), set(spec.get("optional", [])) | mine_ext, event)
        self.assertEqual(ext_fields, {"item_ids", "record"})
        self.assertEqual(register.RECORD_RE.pattern.strip("^$"), EXT["fields"]["record"]["pattern"].strip("^$"))
        self.assertEqual(set(register.RECORD_TYPES), set(EXT["fields"]["record"]["required_for_types"]))

    def test_extension_values(self):
        self.assertEqual(list(register.EXT_TYPES), list(EXT["types"]))
        self.assertEqual([s for s in register.STATUSES if s not in register.BASE_STATUSES], list(EXT["statuses"]))
        for stage in register.STAGES:
            self.assertIn(stage, EXT["phase_values"])

    def test_block_format(self):
        block = CONTRACT["output_field"]["request_block"]
        self.assertEqual((register.HEADER, register.FOOTER, register.PLACEHOLDER, register.NONE_TEXT),
                         (block["header"], block["footer"], block["placeholder"], CONTRACT["output_field"]["none_text"]))
        self.assertTrue(set(REG["types"]) <= set(register.BLOCK_TYPES))

    def test_schema_matches(self):
        schema = json.loads((ROOT / "schemas" / "register.schema.json").read_text(encoding="utf-8"))
        d = schema["$defs"]
        self.assertEqual(d["declare"]["properties"]["type"]["enum"], REG["types"] + list(EXT["types"]))
        self.assertEqual(d["status"]["enum"], REG["statuses"]["values"] + list(EXT["statuses"]))
        self.assertEqual(d["update"]["properties"]["by"]["enum"], REG["by"])
        self.assertEqual(d["id"]["pattern"], REG["id_pattern"])
        self.assertEqual(schema["x-extension"]["types"], list(EXT["types"]))
        self.assertEqual(schema["x-extension"]["statuses"], list(EXT["statuses"]))
        self.assertEqual(sorted(schema["x-extension"]["declare_fields"]), sorted(EXT["fields"]))
        for event in ("declare", "update"):
            self.assertEqual(set(d[event]["required"]), set(REG["events"][event]["required"]), event)


if __name__ == "__main__":
    unittest.main()
