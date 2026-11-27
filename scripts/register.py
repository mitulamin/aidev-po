#!/usr/bin/env python3
"""Write to, read and validate a product's shared register (append-only JSON Lines).

Usage:
  scripts/register.py add --agent A --phase STAGE --type assumption|question|blocker|decision --text T
                          [--impact I] [--urgency U] [--recommendation R]
                          [--item-id ID ...] [--via agent|coordinator] [--register PATH]
  scripts/register.py add --agent po --phase STAGE --type feedback|attribution --record FB-n|AT-n --text T
                          [--item-id ID ...] [--register PATH]
  scripts/register.py ingest FILE|- --agent A --phase STAGE [--via agent|coordinator] [--register PATH]
  scripts/register.py update --ref ID --status S [--phase P] [--note N] [--answer A]
                             [--by coordinator|human] [--impact I] [--urgency U]
                             [--agent A] [--register PATH]
  scripts/register.py list [--open] [--phase P] [--register PATH]
  scripts/register.py check [--register PATH]
  scripts/register.py merge --from PATH [--register PATH]
  scripts/register.py migrate [--write] [--register PATH]
  scripts/register.py selftest

Standard library only. Strictly conforms to schemas/register.schema.json, which is
ai-sdlc-loop's shared surface register plus the optional aidev-po extension (DEC-002):
the same file passes this check and ai-sdlc-loop's. aidev-po writes its stage in the
shared phase field. Lines are only ever appended, in one atomic write, so concurrent
agents do not overwrite each other.

`merge` brings a register back from ai-sdlc-loop (the copy in a gate bundle): it appends,
in order, every valid line whose id the product register does not have yet, and writes
nothing if any line fails. `migrate` rewrites a register written before DEC-002
(stage -> phase, by user -> human); it is the one change that is not an append.
"""
import argparse
import contextlib
import io
import json
import os
import re
import secrets
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

STAGES = ("idea", "audience", "actors", "systems", "scope", "workshops", "presentations", "fsd")
BASE_TYPES = ("assumption", "question", "blocker")
EXT_TYPES = ("decision", "feedback", "attribution")
BLOCK_TYPES = BASE_TYPES + ("decision",)
RECORD_TYPES = ("feedback", "attribution")
TYPES = BASE_TYPES + EXT_TYPES
BASE_STATUSES = ("open", "surfaced", "answered", "dismissed", "duplicate")
STATUSES = BASE_STATUSES + ("decided", "superseded")
LEVELS = ("low", "medium", "high")
VIA_VALUES = ("agent", "coordinator")
BY_VALUES = ("coordinator", "human")
LEGACY = {"stage": "phase"}
LEGACY_BY = {"user": "human"}

ID_RE = re.compile(r"^r-[0-9]{14}-[0-9a-f]{4}$")
RECORD_RE = re.compile(r"^(FB|AT)-[0-9]{3,}$")
TS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

HEADER = "=== REGISTER REQUESTS ==="
FOOTER = "=== END REGISTER REQUESTS ==="
NONE_TEXT = "None."
PLACEHOLDER = "<one-line statement>"

TYPE_TO_TAG = {t: t.upper() for t in BLOCK_TYPES}
TAG_TO_TYPE = {tag: t for t, tag in TYPE_TO_TAG.items()}
LINE_RE = re.compile(r"\[(" + "|".join(re.escape(t) for t in TAG_TO_TYPE) + r"): (\S.*)\]")

DECLARE_REQUIRED = ("id", "event", "ts", "agent", "phase", "type", "text", "status")
DECLARE_OPTIONAL = ("impact", "urgency", "recommendation", "item_ids", "via", "record")
UPDATE_REQUIRED = ("id", "event", "ts", "agent", "phase", "ref", "status")
UPDATE_OPTIONAL = ("note", "answer", "by", "impact", "urgency")


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def new_id():
    return "r-" + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S") + "-" + secrets.token_hex(2)


def format_block(items):
    """Format (type, text) pairs as a register-request block."""
    body = [f"[{TYPE_TO_TAG[t]}: {text}]" for t, text in items] or [NONE_TEXT]
    return "\n".join([HEADER, *body, FOOTER]) + "\n"


def parse_blocks(text):
    """Return (type, statement) pairs from every register-request block in text."""
    items, inside, body, start = [], False, [], 0
    for n, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if not inside:
            if s == HEADER:
                inside, body, start = True, [], n
            continue
        if s == FOOTER:
            inside = False
            real = [(n2, l) for n2, l in body if l.strip()]
            if [l.strip() for _, l in real] == [NONE_TEXT]:
                continue
            for n2, l in real:
                m = LINE_RE.fullmatch(l.rstrip())
                if not m:
                    tags = "|".join(TAG_TO_TYPE)
                    raise ValueError(f"line {n2}: expected [{tags}: statement] or {NONE_TEXT}, got {l.strip()!r}")
                if m[2] == PLACEHOLDER:
                    raise ValueError(f"line {n2}: still contains template placeholder {PLACEHOLDER}")
                items.append((TAG_TO_TYPE[m[1]], m[2]))
            if not real:
                raise ValueError(f"line {start}: empty block; write {NONE_TEXT} when there are no entries")
        else:
            body.append((n, line))
    if inside:
        raise ValueError(f"line {start}: block has no {FOOTER}")
    return items


def append(path, records):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records).encode("utf-8")
    fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
    try:
        os.write(fd, data)
    finally:
        os.close(fd)


def validate(rec, known_ids=None):
    """Validate one register record against schemas/register.schema.json rules."""
    errs = []
    event = rec.get("event")
    if event not in ("declare", "update"):
        return ["event must be 'declare' or 'update'"]

    required = DECLARE_REQUIRED if event == "declare" else UPDATE_REQUIRED
    optional = DECLARE_OPTIONAL if event == "declare" else UPDATE_OPTIONAL

    for k in required:
        if not isinstance(rec.get(k), str) or not rec[k].strip():
            errs.append(f"{k} is required and must be a non-empty string")
    for k in optional:
        if k not in rec:
            continue
        if k == "item_ids":
            if not isinstance(rec[k], list) or not all(isinstance(x, str) and x.strip() for x in rec[k]):
                errs.append("item_ids must be an array of non-empty strings")
        elif not isinstance(rec[k], str):
            errs.append(f"{k} must be a string")

    allowed = set(required) | set(optional)
    for k in rec:
        if k not in allowed:
            hint = f" (written before DEC-002: run scripts/register.py migrate)" if k in LEGACY else ""
            errs.append(f"unexpected field {k}{hint}")
    if errs:
        return errs

    if not ID_RE.fullmatch(rec["id"]):
        errs.append(f"id {rec['id']!r} must match {ID_RE.pattern}")
    if not TS_RE.fullmatch(rec["ts"]):
        errs.append(f"ts {rec['ts']!r} must be UTC RFC 3339 (YYYY-MM-DDTHH:MM:SSZ)")
    if rec["status"] not in STATUSES:
        errs.append(f"status must be one of {STATUSES}")

    if event == "declare":
        if rec["type"] not in TYPES:
            errs.append(f"type must be one of {TYPES}")
        if rec["status"] != "open":
            errs.append("a declared entry must start with status 'open'")
        if "via" in rec and rec["via"] not in VIA_VALUES:
            errs.append(f"via must be one of {VIA_VALUES}")
        if rec["type"] in RECORD_TYPES and "record" not in rec:
            errs.append(f"type {rec['type']} needs record, the FB- or AT- id of the full record")
        if "record" in rec and not RECORD_RE.fullmatch(rec["record"]):
            errs.append(f"record {rec['record']!r} must match {RECORD_RE.pattern}")
    else:
        if not ID_RE.fullmatch(rec["ref"]):
            errs.append(f"ref {rec['ref']!r} must match {ID_RE.pattern}")
        if "by" in rec and rec["by"] not in BY_VALUES:
            hint = " (written before DEC-002: run scripts/register.py migrate)" if rec["by"] in LEGACY_BY else ""
            errs.append(f"by must be one of {BY_VALUES}{hint}")
        if known_ids is not None and rec["ref"] not in known_ids:
            errs.append(f"ref {rec['ref']} is not an earlier declared entry")

    for k in ("impact", "urgency"):
        if k in rec and rec[k] not in LEVELS:
            errs.append(f"{k} must be one of {LEVELS}")
    return errs


def read(path):
    """Yield (line_number, record_or_None, error_or_None) for each non-blank line."""
    for n, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
            if isinstance(rec, dict):
                yield n, rec, None
            else:
                yield n, None, "not a JSON object"
        except json.JSONDecodeError as e:
            yield n, None, f"invalid JSON ({e.msg})"


def declare_record(fields, used=()):
    rid = new_id()
    while rid in used:
        rid = new_id()
    rec = {
        "id": rid,
        "event": "declare",
        "ts": now(),
        "agent": fields["agent"],
        "phase": fields["phase"],
        "type": fields["type"],
        "text": fields["text"],
        "status": "open",
    }
    for k in ("impact", "urgency", "recommendation", "via", "record"):
        if fields.get(k):
            rec[k] = fields[k]
    if fields.get("item_ids"):
        rec["item_ids"] = list(fields["item_ids"])
    return rec


def current(path):
    entries, latest = {}, {}
    for _, rec, _ in read(path):
        if not rec:
            continue
        if rec.get("event") == "declare":
            entries[rec["id"]] = rec
        elif rec.get("event") == "update" and rec.get("ref") in entries:
            latest[rec["ref"]] = rec
    return entries, latest


def cmd_add(args):
    rec = declare_record({
        "agent": args.agent,
        "phase": args.phase,
        "type": args.type,
        "text": args.text,
        "impact": args.impact,
        "urgency": args.urgency,
        "recommendation": args.recommendation,
        "item_ids": args.item_id,
        "via": args.via,
        "record": args.record,
    })
    errs = validate(rec)
    if errs:
        sys.exit("; ".join(errs))
    append(args.register, [rec])
    print(rec["id"])
    return 0


def cmd_update(args):
    path = Path(args.register)
    entries = {}
    if path.exists():
        entries, _ = current(path)
    ids = set(entries)
    phase = args.phase or (entries[args.ref].get("phase") if args.ref in entries else None)
    if not phase:
        sys.exit(f"--phase is required when {args.ref} cannot be resolved from {path}")
    rec = {
        "id": new_id(),
        "event": "update",
        "ts": now(),
        "agent": args.agent or args.by or "po",
        "phase": phase,
        "ref": args.ref,
        "status": args.status,
    }
    for k in ("note", "answer", "by", "impact", "urgency"):
        val = getattr(args, k, None)
        if val:
            rec[k] = val
    errs = validate(rec, ids if path.exists() else set())
    if errs:
        sys.exit("; ".join(errs))
    append(path, [rec])
    print(rec["id"])
    return 0


def cmd_ingest(args):
    text = sys.stdin.read() if args.file == "-" else Path(args.file).read_text(encoding="utf-8")
    try:
        items = parse_blocks(text)
    except ValueError as e:
        sys.exit(f"{args.file}: {e}")
    if HEADER not in text:
        sys.exit(f"{args.file}: no {HEADER} block found; emit a block with {NONE_TEXT} if there are no entries")
    recs, used = [], set()
    for t, statement in items:
        rec = declare_record({
            "agent": args.agent,
            "phase": args.phase,
            "type": t,
            "text": statement,
            "via": args.via,
        }, used)
        used.add(rec["id"])
        errs = validate(rec)
        if errs:
            sys.exit(f"{args.file}: {statement!r}: " + "; ".join(errs))
        recs.append(rec)
    if recs:
        append(args.register, recs)
    print(f"appended {len(recs)} entries")
    return 0


def cmd_list(args):
    path = Path(args.register)
    if not path.exists():
        print("no register yet")
        return 0
    entries, latest = current(path)
    scale = {"high": 0, "medium": 1, "low": 2}
    rows = []
    for eid, e in entries.items():
        if args.phase and e.get("phase") != args.phase:
            continue
        status = latest[eid]["status"] if eid in latest else e["status"]
        if args.open and status not in ("open", "surfaced"):
            continue
        rating = {
            k: next((r[k] for r in (latest.get(eid), e) if r and k in r), None)
            for k in ("impact", "urgency")
        }
        rows.append((
            e["type"] != "blocker",
            scale.get(rating["urgency"], 1),
            scale.get(rating["impact"], 1),
            e["ts"],
            eid,
            status,
            e,
            rating,
        ))
    for *_, eid, status, e, rating in sorted(rows, key=lambda r: r[:5]):
        imp = rating["impact"] or "unrated"
        urg = rating["urgency"] or "unrated"
        print(f"{eid}  {status:10}  {e['type']:11}  phase={e['phase']:13}  impact={imp:7}  urgency={urg:7}  {e['agent']}: {e['text']}")
    return 0


def cmd_check(args):
    path = Path(args.register)
    if not path.exists():
        print("no register yet")
        return 0
    errors, ids = [], set()
    for n, rec, err in read(path):
        if err:
            errors.append(f"line {n}: {err}")
            continue
        for p in validate(rec, ids):
            errors.append(f"line {n}: {p}")
        if rec.get("event") == "declare" and isinstance(rec.get("id"), str):
            if rec["id"] in ids:
                errors.append(f"line {n}: duplicate id {rec['id']}")
            ids.add(rec["id"])
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"{args.register}: {len(ids)} entries, valid")
    return 0


def cmd_merge(args):
    src, path = Path(args.source), Path(args.register)
    have, declared = set(), set()
    if path.exists():
        for n, rec, err in read(path):
            if err:
                sys.exit(f"{path}: line {n}: {err}; fix the register before merging into it")
            have.add(rec.get("id"))
            if rec.get("event") == "declare":
                declared.add(rec.get("id"))
    new, errors, skipped = [], [], 0
    for n, rec, err in read(src):
        if err:
            errors.append(f"{src}: line {n}: {err}")
            continue
        if rec.get("id") in have:
            skipped += 1
            continue
        for p in validate(rec, declared):
            errors.append(f"{src}: line {n}: {p}")
        have.add(rec.get("id"))
        if rec.get("event") == "declare":
            declared.add(rec.get("id"))
        new.append(rec)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        print("nothing merged", file=sys.stderr)
        return 1
    if new:
        append(path, new)
    print(f"merged {len(new)} new line(s) from {src}; {skipped} already in {path}")
    return 0


def migrate_record(rec):
    """A pre-DEC-002 line in the shared taxonomy: stage -> phase in place, by user -> human."""
    out = {LEGACY.get(k, k): v for k, v in rec.items()}
    if out.get("by") in LEGACY_BY:
        out["by"] = LEGACY_BY[out["by"]]
    return out


def cmd_migrate(args):
    path = Path(args.register)
    if not path.exists():
        print("no register yet")
        return 0
    lines, changed = [], 0
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError as e:
            sys.exit(f"{path}: line {n}: invalid JSON ({e.msg}); nothing migrated")
        new = migrate_record(rec) if isinstance(rec, dict) else rec
        changed += new != rec
        lines.append(json.dumps(new, ensure_ascii=False) if new != rec else line)
    if not args.write:
        print(f"{path}: {changed} line(s) would change; run again with --write to rewrite the file")
        return 0
    if changed:
        tmp = path.with_name(path.name + ".migrating")
        tmp.write_text("\n".join(lines) + "\n", encoding="utf-8")
        os.replace(tmp, path)
    print(f"{path}: {changed} line(s) migrated")
    return 0


def selftest():
    """Round-trip every register type and validate bad-block rejection."""
    problems = []
    statements = {
        t: f"{t} statement with [brackets], a: colon, \u00e9 and  double  spaces ({n})"
        for n, t in enumerate(TYPE_TO_TAG)
    }
    items = [(t, statements[t]) for t in TYPE_TO_TAG] * 2
    block = format_block(items)
    if parse_blocks(block) != items:
        problems.append("a block with every type does not round-trip")
    for t in TYPE_TO_TAG:
        if parse_blocks(format_block([(t, statements[t])])) != [(t, statements[t])]:
            problems.append(f"type {t} does not round-trip on its own")
    wrapped = "Final answer.\n```text\n" + block + "```\nthanks\n" + format_block([])
    if parse_blocks(wrapped) != items:
        problems.append("a block inside a code fence and a None. block do not parse as written")
    if parse_blocks(format_block([])) != []:
        problems.append("a None. block must parse to no entries")

    bad = {
        "an unknown type": f"{HEADER}\n[GUESS: x]\n{FOOTER}\n",
        "a record-only type": f"{HEADER}\n[FEEDBACK: x]\n{FOOTER}\n",
        "the old bare-tag form": f"{HEADER}\n[QUESTION] x\n{FOOTER}\n",
        "no footer": f"{HEADER}\n[QUESTION: x]\n",
        "None. mixed with entries": f"{HEADER}\n{NONE_TEXT}\n[QUESTION: x]\n{FOOTER}\n",
        "the template placeholder": f"{HEADER}\n[QUESTION: {PLACEHOLDER}]\n{FOOTER}\n",
        "an empty block": f"{HEADER}\n{FOOTER}\n",
    }
    for what, text in bad.items():
        try:
            parse_blocks(text)
            problems.append(f"{what} was accepted")
        except ValueError:
            pass

    with tempfile.TemporaryDirectory() as d:
        reg, src = Path(d) / "r.jsonl", Path(d) / "out.md"
        src.write_text("report\n" + block, encoding="utf-8")
        ns = argparse.Namespace(file=str(src), agent="selftest", phase="idea", via="coordinator", register=str(reg))
        with contextlib.redirect_stdout(io.StringIO()):
            cmd_ingest(ns)
        got = [(r["type"], r["text"]) for _, r, _ in read(reg)]
        if got != items:
            problems.append("ingest did not write every statement verbatim and in order")
        first_id = next(r["id"] for _, r, _ in read(reg))
        with contextlib.redirect_stdout(io.StringIO()):
            cmd_update(argparse.Namespace(
                ref=first_id, status="decided", phase=None, note="locked", answer="yes",
                by="human", impact="high", urgency="medium", agent="po", register=str(reg),
            ))
        with contextlib.redirect_stdout(io.StringIO()):
            checked = cmd_check(argparse.Namespace(register=str(reg)))
        if checked != 0:
            problems.append("ingested/updated entries do not validate")

        with contextlib.redirect_stdout(io.StringIO()):
            for t, record in (("feedback", "FB-001"), ("attribution", "AT-001")):
                cmd_add(argparse.Namespace(
                    agent="po", phase="actors", type=t, text=f"{t} line", impact=None, urgency=None,
                    recommendation=None, item_id=["ACT-003"], via=None, record=record, register=str(reg),
                ))
            checked = cmd_check(argparse.Namespace(register=str(reg)))
        if checked != 0:
            problems.append("feedback and attribution entries do not validate")
        base = {"id": new_id(), "event": "declare", "ts": now(), "agent": "po", "phase": "actors", "text": "x", "status": "open"}
        if not validate(dict(base, type="feedback")):
            problems.append("a feedback entry with no record was accepted")
        if not validate(dict(base, type="attribution", record="FB-1")):
            problems.append("a malformed record was accepted")
        if not validate(dict(base, type="question", stage="actors")):
            problems.append("a pre-DEC-002 stage field was accepted")

        eng = Path(d) / "bundle.jsonl"
        eng.write_text(reg.read_text(encoding="utf-8"), encoding="utf-8")
        q = "r-20261127230000-0a0a"
        append(eng, [
            {"id": q, "event": "declare", "ts": "2026-11-27T23:00:00Z", "agent": "plan-reviewer", "phase": "Plan",
             "type": "blocker", "text": "AC-003 has no Then.", "status": "open", "via": "coordinator"},
            {"id": "r-20261127230500-0b0b", "event": "update", "ts": "2026-11-27T23:05:00Z", "agent": "coordinator",
             "phase": "all", "ref": q, "status": "surfaced", "by": "coordinator", "impact": "high", "urgency": "high"},
        ])
        with contextlib.redirect_stdout(io.StringIO()):
            merged = cmd_merge(argparse.Namespace(source=str(eng), register=str(reg)))
            again = cmd_merge(argparse.Namespace(source=str(eng), register=str(reg)))
            checked = cmd_check(argparse.Namespace(register=str(reg)))
        lines = [r for _, r, _ in read(reg)]
        if merged or again or checked or len(lines) != len({r["id"] for r in lines}) or lines[-1]["ref"] != q:
            problems.append("an ai-sdlc-loop register (phase Plan, blocker, update in phase all) does not merge back once and check")

        old = Path(d) / "old.jsonl"
        old.write_text(json.dumps({"id": q, "event": "declare", "ts": "2026-11-27T23:00:00Z", "agent": "po", "stage": "idea",
                                   "type": "question", "text": "x", "status": "open"}) + "\n" +
                       json.dumps({"id": "r-20261127230500-0b0b", "event": "update", "ts": "2026-11-27T23:05:00Z", "agent": "po",
                                   "stage": "idea", "ref": q, "status": "answered", "by": "user"}) + "\n", encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            before = cmd_check(argparse.Namespace(register=str(old)))
            cmd_migrate(argparse.Namespace(register=str(old), write=True))
            after = cmd_check(argparse.Namespace(register=str(old)))
        if before == 0 or after != 0 or [r.get("phase") for _, r, _ in read(old)] != ["idea", "idea"]:
            problems.append("migrate does not turn a pre-DEC-002 register into a valid one")

    if problems:
        print("\n".join(problems), file=sys.stderr)
        return 1
    print(f"register-request parser OK: {', '.join(TYPE_TO_TAG.values())} round-trip, verbatim ingest, rejects bad blocks; "
          f"{' and '.join(RECORD_TYPES)} entries need a record; ai-sdlc-loop lines merge back; migrate fixes pre-DEC-002 lines")
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)

    def common(sp):
        sp.add_argument("--register", default=".po/register.jsonl", help="register path (default .po/register.jsonl)")
        return sp

    a = common(sub.add_parser("add"))
    a.add_argument("--agent", required=True)
    a.add_argument("--phase", required=True, choices=STAGES, help="the stage, in the shared phase field")
    a.add_argument("--type", required=True, choices=TYPES)
    a.add_argument("--text", required=True)
    a.add_argument("--impact", choices=LEVELS)
    a.add_argument("--urgency", choices=LEVELS)
    a.add_argument("--recommendation")
    a.add_argument("--item-id", action="append", default=[], help="stable item ID (repeatable)")
    a.add_argument("--via", choices=VIA_VALUES)
    a.add_argument("--record", help="for types feedback and attribution: the FB- or AT- id in .po/feedback.jsonl or .po/attributions.jsonl")

    u = common(sub.add_parser("update"))
    u.add_argument("--ref", required=True)
    u.add_argument("--status", required=True, choices=STATUSES)
    u.add_argument("--phase", choices=STAGES + ("all",), help="default: the phase of the entry in --ref")
    u.add_argument("--note")
    u.add_argument("--answer")
    u.add_argument("--by", choices=BY_VALUES)
    u.add_argument("--impact", choices=LEVELS)
    u.add_argument("--urgency", choices=LEVELS)
    u.add_argument("--agent")

    i = common(sub.add_parser("ingest"))
    i.add_argument("file", help="a file, or - for stdin")
    i.add_argument("--agent", required=True)
    i.add_argument("--phase", required=True, choices=STAGES, help="the stage, in the shared phase field")
    i.add_argument("--via", choices=VIA_VALUES)

    ls = common(sub.add_parser("list"))
    ls.add_argument("--open", action="store_true", help="only entries still open or surfaced")
    ls.add_argument("--phase", help="only entries in this phase: a stage, or an ai-sdlc-loop phase such as Plan")

    common(sub.add_parser("check"))

    m = common(sub.add_parser("merge"))
    m.add_argument("--from", dest="source", required=True, help="the register to merge in, e.g. the copy in a gate bundle")

    mg = common(sub.add_parser("migrate"))
    mg.add_argument("--write", action="store_true", help="rewrite the file; without it, only report")

    sub.add_parser("selftest")

    args = p.parse_args()
    if args.cmd == "selftest":
        return selftest()
    return {"add": cmd_add, "update": cmd_update, "ingest": cmd_ingest, "list": cmd_list, "check": cmd_check,
            "merge": cmd_merge, "migrate": cmd_migrate}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
