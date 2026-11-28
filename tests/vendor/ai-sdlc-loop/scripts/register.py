#!/usr/bin/env python3
"""Write to, read and validate the shared surface register (append-only JSON Lines).

Usage:
  scripts/register.py add --agent A --phase P --type assumption|question|blocker --text T
                          [--impact I] [--urgency U] [--recommendation R] [--via agent|coordinator] [--register PATH]
  scripts/register.py ingest FILE|- --agent A --phase P [--via agent|coordinator] [--register PATH]
  scripts/register.py update --ref ID --status S [--note N] [--answer A] [--by coordinator|human]
                             [--impact I] [--urgency U] [--agent A] [--phase P] [--register PATH]
  scripts/register.py list [--open] [--register PATH]
  scripts/register.py check [--register PATH]
  scripts/register.py selftest

Standard library only. The format, the allowed values, the register-request block and the
default path come from data/agent-contract.json. Lines are only ever appended, in one write
each, so agents running at the same time do not overwrite each other.

`ingest` reads every register-request block in a file (or stdin, with -) and appends one
declare line per [TYPE: statement] line (TYPE is any type in the contract: ASSUMPTION,
QUESTION, BLOCKER), with the statement copied verbatim. It fails on a block it cannot parse, and on a file with no block at all, so
nothing is dropped silently. `selftest` checks that the parser and the block writer
round-trip all three tags. `list` shows each entry with its current status; the register
file itself stays readable without this script.

`check` also accepts the optional types, statuses and fields of each tool listed in
register.extensions (aidev-po), so a register handed over by that tool, and handed back,
passes here and there. Extensions never add register-request block types.
"""
import argparse
import contextlib
import io
import json
import os
import re
import secrets
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTRACT_DOC = json.loads((ROOT / "data" / "agent-contract.json").read_text(encoding="utf-8"))
CONTRACT = CONTRACT_DOC["register"]


REQUESTS = CONTRACT_DOC["output_field"]["request_block"]
HEADER, FOOTER = REQUESTS["header"], REQUESTS["footer"]
NONE_TEXT = CONTRACT_DOC["output_field"]["none_text"]
TYPE_TO_TAG = {t: t.upper() for t in CONTRACT["types"]}
TAG_TO_TYPE = {tag: t for t, tag in TYPE_TO_TAG.items()}
LINE_RE = re.compile(r"\[(" + "|".join(re.escape(t) for t in TAG_TO_TYPE) + r"): (\S.*)\]")

# Extensions (register.extensions) widen what a line may hold, never the register-request block.
EXTENSIONS = CONTRACT.get("extensions", {})
ALL_TYPES = list(CONTRACT["types"]) + [t for e in EXTENSIONS.values() for t in e.get("types", {})]
ALL_STATUSES = list(CONTRACT["statuses"]["values"]) + [s for e in EXTENSIONS.values() for s in e.get("statuses", {})]
EXT_FIELDS = {ev: {k: f for e in EXTENSIONS.values() for k, f in e.get("fields", {}).items() if f["event"] == ev}
              for ev in CONTRACT["events"]}


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def new_id():
    return "r-" + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S") + "-" + secrets.token_hex(2)


def format_block(items):
    """Write (type, text) pairs as a register-request block: the format agents emit."""
    body = [f"[{TYPE_TO_TAG[t]}: {text}]" for t, text in items] or [NONE_TEXT]
    return "\n".join([HEADER, *body, FOOTER]) + "\n"


def parse_blocks(text):
    """Return the (type, statement) pairs of every register-request block in text, in order.

    A line is [TYPE: statement], with TYPE any type in the contract, upper-cased. Raises ValueError on
    an unterminated block, a line inside a block that is not such a line or None., a None. mixed
    with entries, or a block that still holds the template placeholder."""
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
                    raise ValueError(f"line {n2}: not a [{'|'.join(TAG_TO_TYPE)}: statement] line or {NONE_TEXT}: {l.strip()!r}")
                if m[2] == REQUESTS["placeholder"]:
                    raise ValueError(f"line {n2}: still the template placeholder {REQUESTS['placeholder']}")
                items.append((TAG_TO_TYPE[m[1]], m[2]))
            if not real:
                raise ValueError(f"line {start}: empty block; write {NONE_TEXT} if there are no entries")
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
    """Return the problems with one register line."""
    errs = []
    event = rec.get("event")
    spec = CONTRACT["events"].get(event)
    if spec is None:
        return [f"event must be one of {sorted(CONTRACT['events'])}"]
    for k in spec["required"]:
        if not isinstance(rec.get(k), str) or not rec[k].strip():
            errs.append(f"{k} is required and must be a non-empty string")
    for k in spec.get("optional", []):
        if k in rec and not isinstance(rec[k], str):
            errs.append(f"{k} must be a string")
    ext = EXT_FIELDS[event]
    for k, f in ext.items():
        if k not in rec:
            continue
        v = rec[k]
        if f["kind"] == "string-array":
            if not isinstance(v, list) or not all(isinstance(x, str) and x.strip() for x in v):
                errs.append(f"{k} must be an array of non-empty strings")
        elif not isinstance(v, str) or not v.strip():
            errs.append(f"{k} must be a non-empty string")
        elif f.get("pattern") and not re.fullmatch(f["pattern"], v):
            errs.append(f"{k} {v!r} does not match {f['pattern']}")
    allowed = set(spec["required"]) | set(spec.get("optional", [])) | set(ext)
    for k in rec:
        if k not in allowed:
            errs.append(f"unexpected field {k}")
    if errs:
        return errs
    if not re.fullmatch(CONTRACT["id_pattern"], rec["id"]):
        errs.append(f"id {rec['id']!r} does not match {CONTRACT['id_pattern']}")
    if not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", rec["ts"]):
        errs.append(f"ts {rec['ts']!r} is not UTC RFC 3339 (YYYY-MM-DDTHH:MM:SSZ)")
    if rec["status"] not in ALL_STATUSES:
        errs.append(f"status must be one of {ALL_STATUSES}")
    if event == "declare":
        if rec["type"] not in ALL_TYPES:
            errs.append(f"type must be one of {ALL_TYPES}")
        for k, f in ext.items():
            if rec["type"] in f.get("required_for_types", []) and k not in rec:
                errs.append(f"type {rec['type']} needs {k}")
        if rec["status"] != "open":
            errs.append("a declared entry starts as open")
        if "via" in rec and rec["via"] not in CONTRACT["via"]["values"]:
            errs.append(f"via must be one of {CONTRACT['via']['values']}")
    else:
        if "by" in rec and rec["by"] not in CONTRACT["by"]:
            errs.append(f"by must be one of {CONTRACT['by']}")
    for k in ("impact", "urgency"):
        if k in rec and rec[k] not in CONTRACT[k]["values"]:
            errs.append(f"{k} must be one of {CONTRACT[k]['values']}")
    if event == "update":
        if known_ids is not None and rec["ref"] not in known_ids:
            errs.append(f"ref {rec['ref']} is not an earlier declared entry")
    return errs


def read(path):
    """Yield (line number, record or None, parse error) for each non-blank line."""
    for n, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
            yield n, rec if isinstance(rec, dict) else None, None if isinstance(rec, dict) else "not a JSON object"
        except json.JSONDecodeError as e:
            yield n, None, f"invalid JSON ({e.msg})"


def declare_record(a, used=()):
    rid = new_id()
    while rid in used:
        rid = new_id()
    rec = {"id": rid, "event": "declare", "ts": now(), "agent": a["agent"], "phase": a["phase"],
           "type": a["type"], "text": a["text"], "status": "open"}
    for k in ("impact", "urgency", "recommendation", "via"):
        if a.get(k):
            rec[k] = a[k]
    return rec


def cmd_add(args):
    rec = declare_record(vars(args))
    errs = validate(rec)
    if errs:
        sys.exit("; ".join(errs))
    append(args.register, [rec])
    print(rec["id"])
    return 0


def cmd_update(args):
    path = Path(args.register)
    ids = {r["id"] for _, r, e in read(path) if r and r.get("event") == "declare"} if path.exists() else set()
    rec = {"id": new_id(), "event": "update", "ts": now(), "agent": args.agent or args.by or "coordinator",
           "phase": args.phase or "all", "ref": args.ref, "status": args.status}
    for k in ("note", "answer", "by", "impact", "urgency"):
        if getattr(args, k):
            rec[k] = getattr(args, k)
    errs = validate(rec, ids)
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
        sys.exit(f"{args.file}: no {HEADER} block found; if the agent has no entries it must still emit a block that says {NONE_TEXT}")
    recs, used = [], set()
    for t, statement in items:
        rec = declare_record({"agent": args.agent, "phase": args.phase, "type": t, "text": statement, "via": args.via}, used)
        used.add(rec["id"])
        errs = validate(rec)
        if errs:
            sys.exit(f"{args.file}: {statement!r}: " + "; ".join(errs))
        recs.append(rec)
    if recs:
        append(args.register, recs)
    print(f"appended {len(recs)} entries")
    return 0


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


def cmd_list(args):
    if not Path(args.register).exists():
        print("no register yet")
        return 0
    entries, latest = current(args.register)
    scale = {"high": 0, "medium": 1, "low": 2}
    rows = []
    for i, e in entries.items():
        status = latest[i]["status"] if i in latest else e["status"]
        if args.open and status not in ("open", "surfaced"):
            continue
        rating = {k: next((r[k] for r in (latest.get(i), e) if r and k in r), None) for k in ("impact", "urgency")}
        rows.append((e["type"] != "blocker", scale.get(rating["impact"], 0), scale.get(rating["urgency"], 0), e["ts"], i, status, e, rating))
    for *_, i, status, e, rating in sorted(rows, key=lambda r: r[:5]):
        print(f"{i}  {status:9}  {e['type']:10}  impact={rating['impact'] or 'unrated':7} urgency={rating['urgency'] or 'unrated':7} {e['agent']} ({e['phase']}): {e['text']}")
    return 0


def cmd_check(args):
    if not Path(args.register).exists():
        print("no register yet")
        return 0
    errors, ids = [], set()
    for n, rec, err in read(args.register):
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


def selftest_extensions():
    """Each extension's types, statuses and fields validate on a line, and stay out of the block."""
    problems = []
    base = {"id": new_id(), "event": "declare", "ts": now(), "agent": "po", "phase": "fsd", "text": "x", "status": "open"}
    upd = {"id": new_id(), "event": "update", "ts": now(), "agent": "po", "phase": "fsd", "ref": base["id"], "status": "open"}
    plain = CONTRACT["types"][0]
    for name, e in EXTENSIONS.items():
        fields = {k: f for k, f in e.get("fields", {}).items() if f["event"] == "declare"}
        for t in e.get("types", {}):
            rec = dict(base, type=t)
            needs = [k for k, f in fields.items() if t in f.get("required_for_types", [])]
            for k in needs:
                rec[k] = "FB-001"
            if validate(rec):
                problems.append(f"extension {name}: type {t} does not validate: {validate(rec)}")
            if t.upper() in TAG_TO_TYPE:
                problems.append(f"extension {name}: type {t} must not be a register-request block type")
            for k in needs:
                if not validate({x: y for x, y in rec.items() if x != k}):
                    problems.append(f"extension {name}: type {t} without {k} was accepted")
        for s in e.get("statuses", {}):
            if validate(dict(upd, status=s), {base["id"]}):
                problems.append(f"extension {name}: status {s} does not validate")
        for k, f in fields.items():
            if f["kind"] == "string-array":
                if validate(dict(base, type=plain, **{k: ["REQ-001"]})):
                    problems.append(f"extension {name}: field {k} does not validate")
                if not validate(dict(base, type=plain, **{k: "REQ-001"})):
                    problems.append(f"extension {name}: field {k} accepted a string for an array")
            elif f.get("pattern") and not validate(dict(base, type=plain, **{k: "not an id"})):
                problems.append(f"extension {name}: field {k} accepted a value that does not match {f['pattern']}")
    if not validate(dict(base, type="guess")):
        problems.append("an unknown type was accepted")
    return problems


def selftest():
    """Round-trip every contract type through the block writer and the parser, and check the rejects."""
    problems = []
    statements = {t: f"{t} statement with [brackets], a: colon, \u00e9 and  double  spaces ({n})" for n, t in enumerate(TYPE_TO_TAG)}
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
        "the old bare-tag form": f"{HEADER}\n[{next(iter(TAG_TO_TYPE))}] x\n{FOOTER}\n",
        "no footer": f"{HEADER}\n[{next(iter(TAG_TO_TYPE))}: x]\n",
        "None. mixed with entries": f"{HEADER}\n{NONE_TEXT}\n[{next(iter(TAG_TO_TYPE))}: x]\n{FOOTER}\n",
        "the template placeholder": f"{HEADER}\n[{next(iter(TAG_TO_TYPE))}: {REQUESTS['placeholder']}]\n{FOOTER}\n",
        "an empty block": f"{HEADER}\n{FOOTER}\n",
    }
    for what, text in bad.items():
        try:
            parse_blocks(text)
            problems.append(f"{what} was accepted")
        except ValueError:
            pass
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        reg, src = Path(d) / "r.jsonl", Path(d) / "out.md"
        src.write_text("report\n" + block, encoding="utf-8")
        ns = argparse.Namespace(file=str(src), agent="selftest", phase="Test", via="coordinator", register=str(reg))
        with contextlib.redirect_stdout(io.StringIO()):
            cmd_ingest(ns)
        got = [(r["type"], r["text"]) for _, r, _ in read(reg)]
        if got != items:
            problems.append("ingest did not write every statement verbatim and in order")
        with contextlib.redirect_stdout(io.StringIO()):
            checked = cmd_check(argparse.Namespace(register=str(reg)))
        if checked != 0:
            problems.append("ingested entries do not validate")
    problems += selftest_extensions()
    if problems:
        print("\n".join(problems), file=sys.stderr)
        return 1
    print(f"register-request parser OK: {', '.join(TYPE_TO_TAG.values())} round-trip, verbatim ingest, rejects bad blocks")
    return 0


def main():
    default = CONTRACT["default_path"]
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)

    def common(sp):
        sp.add_argument("--register", default=default, help=f"register path (default {default})")
        return sp

    a = common(sub.add_parser("add"))
    a.add_argument("--agent", required=True)
    a.add_argument("--phase", required=True)
    a.add_argument("--type", required=True, choices=CONTRACT["types"])
    a.add_argument("--text", required=True)
    a.add_argument("--impact", choices=CONTRACT["impact"]["values"])
    a.add_argument("--urgency", choices=CONTRACT["urgency"]["values"])
    a.add_argument("--recommendation")
    a.add_argument("--via", choices=CONTRACT["via"]["values"])
    u = common(sub.add_parser("update"))
    u.add_argument("--ref", required=True)
    u.add_argument("--status", required=True, choices=CONTRACT["statuses"]["values"])
    u.add_argument("--note")
    u.add_argument("--answer")
    u.add_argument("--by", choices=CONTRACT["by"])
    u.add_argument("--impact", choices=CONTRACT["impact"]["values"])
    u.add_argument("--urgency", choices=CONTRACT["urgency"]["values"])
    u.add_argument("--agent")
    u.add_argument("--phase")
    i = common(sub.add_parser("ingest"))
    i.add_argument("file", help="a file, or - for stdin")
    i.add_argument("--agent", required=True, help="the agent that emitted the block")
    i.add_argument("--phase", required=True)
    i.add_argument("--via", choices=CONTRACT["via"]["values"])
    ls = common(sub.add_parser("list"))
    ls.add_argument("--open", action="store_true", help="only entries still open or surfaced")
    common(sub.add_parser("check"))
    sub.add_parser("selftest")
    args = p.parse_args()
    if args.cmd == "selftest":
        return selftest()
    return {"add": cmd_add, "update": cmd_update, "ingest": cmd_ingest, "list": cmd_list, "check": cmd_check}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
