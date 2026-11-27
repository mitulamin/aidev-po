#!/usr/bin/env python3
"""Check that every file in schemas/ is valid JSON with $schema, $id, title and x-status.

Usage: scripts/check-schemas.py

Standard library only. If the `jsonschema` package is installed, it also checks each schema is
itself a valid draft 2020-12 schema and that the register examples below validate.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = ("$schema", "$id", "title", "x-status")
STATUSES = {"draft", "stub", "stable"}

REGISTER_OK = [
    {"id": "r-20261127223000-ab12", "event": "declare", "ts": "2026-11-27T22:30:00Z", "agent": "audience-producer",
     "stage": "audience", "type": "question", "text": "Who pays? Recommend: the clinic manager.", "status": "open"},
    {"id": "r-20261127223100-cd34", "event": "update", "ts": "2026-11-27T22:31:00Z", "agent": "po",
     "stage": "audience", "ref": "r-20261127223000-ab12", "status": "answered", "answer": "Clinic manager.", "by": "user"},
]
REGISTER_BAD = [
    {"id": "r-1", "event": "declare"},
    {"id": "r-20261127223000-ab12", "event": "declare", "ts": "2026-11-27T22:30:00Z", "agent": "a",
     "stage": "build", "type": "question", "text": "x", "status": "open"},
    {"id": "r-20261127223000-ab12", "event": "declare", "ts": "2026-11-27T22:30:00Z", "agent": "a",
     "stage": "idea", "type": "blocker", "text": "x", "status": "open"},
]


def main():
    errors = []
    schemas = sorted((ROOT / "schemas").glob("*.schema.json"))
    if not schemas:
        errors.append("schemas/: no *.schema.json files")
    loaded = {}
    for path in schemas:
        rel = path.relative_to(ROOT)
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"{rel}: invalid JSON ({e})")
            continue
        loaded[path.name] = doc
        for key in REQUIRED:
            if key not in doc:
                errors.append(f"{rel}: missing {key}")
        if doc.get("x-status") not in STATUSES:
            errors.append(f"{rel}: x-status must be one of {sorted(STATUSES)}")
        if not str(doc.get("$id", "")).endswith(f"/schemas/{path.name}"):
            errors.append(f"{rel}: $id must end with /schemas/{path.name}")
    try:
        import jsonschema
    except ImportError:
        jsonschema = None
    if jsonschema and not errors:
        for name, doc in loaded.items():
            try:
                jsonschema.Draft202012Validator.check_schema(doc)
            except jsonschema.SchemaError as e:
                errors.append(f"schemas/{name}: not a valid schema ({e.message})")
        validator = jsonschema.Draft202012Validator(loaded["register.schema.json"])
        for entry in REGISTER_OK:
            for err in validator.iter_errors(entry):
                errors.append(f"register example should be valid but: {err.message}")
        for entry in REGISTER_BAD:
            if validator.is_valid(entry):
                errors.append(f"register example should be invalid but passed: {entry}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    note = "" if jsonschema else " (jsonschema not installed: structure checked only)"
    print(f"{len(schemas)} schema(s) ok{note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
