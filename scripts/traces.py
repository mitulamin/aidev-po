#!/usr/bin/env python3
"""Stable item IDs, trace records and the learning-loop files of a product folder.

Usage:
  scripts/traces.py new-run
  scripts/traces.py versions [--skills a,b] [--templates path,path]
  scripts/traces.py next-id TYPE              WHERE   TYPE is an item type (actor), a prefix (ACT), or FB, AT, RR, LE
  scripts/traces.py add KIND [--json TEXT]    WHERE   KIND is trace, feedback, attribution, rerun or ledger
  scripts/traces.py chain ITEM_ID [--feedback FB-n | --rev N] [--json]   WHERE
  scripts/traces.py downstream ITEM_ID... [--register-ref r-...] [--json]   WHERE
  scripts/traces.py locate FILE (--line N | --quote TEXT)   WHERE
  scripts/traces.py check                     WHERE | --all [--repo PATH]

  WHERE is --product SLUG (a folder in the products repo), or --dir PATH (a product folder
  anywhere). The products repo is --repo PATH if given, else what scripts/products-dir.py
  reports (AIDEV_PO_PRODUCTS_DIR or products_dir in aidev-po.local.json). Never a folder
  inside the aidev-po checkout by assumption.

Standard library only; if the jsonschema package is installed, every line is also checked
against its schema in schemas/. Files (all JSON Lines, append-only, one object per line):

  <product>/.po/traces.jsonl         trace.schema.json        write, review and remove lines
  <product>/.po/feedback.jsonl       feedback.schema.json     latest line per id wins
  <product>/.po/attributions.jsonl   attribution.schema.json  latest line per id wins
  <product>/.po/reruns.jsonl         rerun.schema.json        latest line per id wins
  <product>/.po/register.jsonl       register.schema.json     read for register_refs links
  <products repo>/.po/ledger.jsonl   ledger.schema.json       latest line per id wins

`add` reads one JSON object, a JSON array, or JSON Lines from --json or stdin. It fills in ts,
and for trace lines rev and (if missing) item_id; for the other kinds id. It appends only if the
new lines bring no new check errors, so a bad line never reaches the file.

`check` exits 1 on any error. Warnings do not change the exit code.
"""
import argparse
import json
import re
import secrets
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = ROOT / "schemas"
PO = ".po"
FILES = {
    "trace": "traces.jsonl",
    "feedback": "feedback.jsonl",
    "attribution": "attributions.jsonl",
    "rerun": "reruns.jsonl",
    "register": "register.jsonl",
}
LEDGER = "ledger.jsonl"
SCHEMA_FILES = {
    "trace": "trace.schema.json",
    "feedback": "feedback.schema.json",
    "attribution": "attribution.schema.json",
    "rerun": "rerun.schema.json",
    "register": "register.schema.json",
    "ledger": "ledger.schema.json",
}
RECORD_PREFIX = {"feedback": "FB", "attribution": "AT", "rerun": "RR", "ledger": "LE"}
ITEM_TYPES = json.loads((SCHEMAS / "trace.schema.json").read_text(encoding="utf-8"))["x-item-types"]
PREFIXES = {prefix: name for name, prefix in ITEM_TYPES.items()}
ITEM_ID = re.compile(r"^([A-Z]{2,4})-([0-9]{3,})$")
ID_IN_TEXT = re.compile(r"(?<![A-Za-z0-9-])([A-Z]{2,4}-[0-9]{3,})(?![A-Za-z0-9-])")
RECORD_ID = re.compile(r"^(FB|AT|RR|LE)-([0-9]{3,})$")
STAGES = ["idea", "audience", "actors", "systems", "scope", "workshops", "presentations", "fsd"]
LOW_CONFIDENCE = 0.5


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def new_run_id():
    return "run-" + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S") + "-" + secrets.token_hex(2)


# ---------------------------------------------------------------- locating folders

def products_repo(arg=None):
    """The products repo: --repo if given, else what scripts/products-dir.py reports."""
    if arg:
        return Path(arg).expanduser().resolve()
    out = subprocess.run([sys.executable, str(ROOT / "scripts" / "products-dir.py"), "--json"],
                         capture_output=True, text=True)
    if out.returncode != 0:
        raise SystemExit(f"scripts/products-dir.py failed: {out.stderr.strip()}")
    info = json.loads(out.stdout)
    path = info.get("path")
    if not path:
        raise SystemExit("No products repo is set. Set AIDEV_PO_PRODUCTS_DIR or products_dir in "
                         "aidev-po.local.json (po offers this on /po-start), or pass --repo.")
    path = Path(path)
    if not path.is_dir():
        raise SystemExit(f"The products repo {path} does not exist (state {info.get('state')}). Run /po-start.")
    return path.resolve()


def product_dir(args):
    if getattr(args, "dir", None):
        folder = Path(args.dir).expanduser().resolve()
    elif getattr(args, "product", None):
        folder = products_repo(getattr(args, "repo", None)) / args.product
    else:
        raise SystemExit("Say which product: --product SLUG or --dir PATH.")
    if not folder.is_dir():
        raise SystemExit(f"{folder}: no such product folder")
    return folder


def repo_for(args, folder=None):
    if getattr(args, "repo", None):
        return Path(args.repo).expanduser().resolve()
    if folder is not None:
        return folder.parent
    return products_repo()


# ---------------------------------------------------------------- reading

def read_jsonl(path, errors, label):
    """Return [(line number, object)]. Bad lines become errors, never silently dropped."""
    rows = []
    if not path.exists():
        return rows
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as e:
            errors.append(Issue(f"{label}:{n}", f"not valid JSON ({e.msg})"))
            continue
        if not isinstance(obj, dict):
            errors.append(Issue(f"{label}:{n}", "each line must be a JSON object"))
            continue
        rows.append((n, obj))
    return rows


def latest_by_id(rows):
    """For latest-line-wins files: {id: (line number, object)} keeping the last line per id."""
    out = {}
    for n, obj in rows:
        if isinstance(obj.get("id"), str):
            out[obj["id"]] = (n, obj)
    return out


class Issue:
    def __init__(self, where, msg, item=None, level="error"):
        self.where, self.msg, self.item, self.level = where, msg, item, level

    def __str__(self):
        return f"{self.where}: {self.msg}"

    def key(self):
        return (self.level, self.msg, self.item)


class Product:
    """Everything in one product's .po folder, loaded once."""

    def __init__(self, folder, extra=None):
        self.dir = folder
        self.slug = folder.name
        self.load_issues = []
        self.rows = {}
        for kind, name in FILES.items():
            label = f"{self.slug}/{PO}/{name}"
            self.rows[kind] = read_jsonl(folder / PO / name, self.load_issues, label)
        for kind, objs in (extra or {}).items():
            start = (self.rows[kind][-1][0] if self.rows[kind] else 0) + 1
            self.rows[kind] = self.rows[kind] + [(start + i, o) for i, o in enumerate(objs)]
        self.index()

    def label(self, kind, n):
        return f"{self.slug}/{PO}/{FILES[kind]}:{n}"

    def index(self):
        self.history = {}
        self.reviews = []
        for n, obj in self.rows["trace"]:
            ev = obj.get("event")
            if ev in ("write", "remove") and isinstance(obj.get("item_id"), str):
                self.history.setdefault(obj["item_id"], []).append((n, obj))
            elif ev == "review":
                self.reviews.append((n, obj))
        self.register = {}
        self.register_status = {}
        for n, obj in self.rows["register"]:
            if obj.get("event") == "declare":
                self.register[obj.get("id")] = obj
                self.register_status[obj.get("id")] = obj
            elif obj.get("event") == "update" and obj.get("ref") in self.register:
                self.register_status[obj["ref"]] = obj
        self.feedback = latest_by_id(self.rows["feedback"])
        self.attributions = latest_by_id(self.rows["attribution"])
        self.reruns = latest_by_id(self.rows["rerun"])

    def current(self, item_id):
        """The item's latest write or remove line, or None."""
        hist = self.history.get(item_id)
        return hist[-1][1] if hist else None

    def live(self):
        return {i: h[-1][1] for i, h in self.history.items() if h[-1][1].get("event") == "write"}

    def write_at(self, item_id, rev):
        for _, obj in self.history.get(item_id, []):
            if obj.get("event") == "write" and obj.get("rev") == rev:
                return obj
        return None

    def write_before(self, item_id, ts):
        """The item's write line in force at time ts (the latest write at or before ts)."""
        found = None
        for _, obj in self.history.get(item_id, []):
            if obj.get("event") == "write" and str(obj.get("ts", "")) <= ts:
                found = obj
        return found

    def attribution_for(self, fb_id):
        """The current attribution for a feedback id: the latest line of any AT naming it."""
        best = None
        for n, obj in self.rows["attribution"]:
            if obj.get("feedback") == fb_id:
                best = self.attributions.get(obj.get("id"), (n, obj))[1]
        return best

    def feedback_status(self, fb_id):
        fb = self.feedback.get(fb_id, (0, {}))[1]
        if fb.get("withdrawn"):
            return "withdrawn"
        status = "open"
        if self.attribution_for(fb_id):
            status = "traced"
        for _, rr in self.reruns.values():
            if fb_id in rr.get("feedback", []) and rr.get("status") in ("done", "committed"):
                status = "fixed"
        return status


# ---------------------------------------------------------------- schema validation

_VALIDATORS = {}


def validator(kind):
    try:
        import jsonschema
    except ImportError:
        return None
    if kind not in _VALIDATORS:
        doc = json.loads((SCHEMAS / SCHEMA_FILES[kind]).read_text(encoding="utf-8"))
        _VALIDATORS[kind] = jsonschema.Draft202012Validator(doc, format_checker=jsonschema.FormatChecker())
    return _VALIDATORS[kind]


def schema_issues(kind, rows, label_fn):
    v = validator(kind)
    if v is None:
        return []
    out = []
    for n, obj in rows:
        for err in sorted(v.iter_errors(obj), key=lambda e: list(e.path)):
            path = "/".join(str(p) for p in err.path)
            msg = err.message if len(err.message) < 200 else err.message[:200] + "..."
            out.append(Issue(label_fn(n), f"schema: {path + ': ' if path else ''}{msg}", obj.get("item_id")))
    return out


# ---------------------------------------------------------------- checks

def check_product(p):
    """Return a list of Issues for one product. Item-level issues carry the item ID."""
    issues = list(p.load_issues)
    for kind in FILES:
        issues += schema_issues(kind, p.rows[kind], lambda n, k=kind: p.label(k, n))
    issues += check_trace(p)
    issues += check_markdown(p)
    issues += check_feedback(p)
    issues += check_attributions(p)
    issues += check_reruns(p)
    return issues


def check_trace(p):
    out = []
    register_exists = (p.dir / PO / FILES["register"]).exists() or p.rows["register"]
    for item_id, hist in p.history.items():
        m = ITEM_ID.match(item_id)
        expected_rev = 1
        removed = False
        for n, obj in hist:
            where = p.label("trace", n)
            if not m:
                out.append(Issue(where, f"{item_id}: not a valid item ID (two to four capital letters, a hyphen, three or more digits)", item_id))
                break
            if obj.get("event") == "write":
                want = ITEM_TYPES.get(obj.get("item_type"))
                if want and want != m.group(1):
                    out.append(Issue(where, f"{item_id}: prefix {m.group(1)} does not match item_type {obj.get('item_type')} ({want})", item_id))
            if removed:
                out.append(Issue(where, f"{item_id}: written after it was removed; IDs are never reused, give the new item a new ID", item_id))
            if obj.get("rev") != expected_rev:
                out.append(Issue(where, f"{item_id}: rev {obj.get('rev')} out of order, expected {expected_rev}", item_id))
            expected_rev = (obj.get("rev") if isinstance(obj.get("rev"), int) else expected_rev) + 1
            removed = obj.get("event") == "remove"
            if obj.get("event") != "write":
                continue
            upstream, relied = obj.get("upstream_ids") or [], obj.get("register_refs") or []
            if not upstream and not relied:
                out.append(Issue(where, f"{item_id}: no upstream_ids and no register_refs; an item with no source is a question, not a fact", item_id))
            for up in upstream:
                if up == item_id:
                    out.append(Issue(where, f"{item_id}: lists itself as upstream", item_id))
                elif up not in p.history:
                    out.append(Issue(where, f"{item_id}: upstream {up} has no trace", item_id))
                elif not any(o.get("event") == "write" and k < n for k, o in p.history[up]):
                    out.append(Issue(where, f"{item_id}: upstream {up} is written later in the trace than this line", item_id))
            for ref in relied:
                if not register_exists:
                    out.append(Issue(where, f"{item_id}: relies on {ref} but the product has no {PO}/register.jsonl", item_id))
                elif ref not in p.register:
                    out.append(Issue(where, f"{item_id}: relies on {ref}, which is not declared in the register", item_id))
            tag, sources = obj.get("evidence_tag"), obj.get("sources")
            if tag == "Validated" and not sources:
                out.append(Issue(where, f"{item_id}: tagged Validated with no sources", item_id))
            if tag == "Stated" and not sources and not relied:
                out.append(Issue(where, f"{item_id}: tagged Stated but names no source and relies on no register entry", item_id))
            if tag == "Assumed" and not any(p.register.get(r, {}).get("type") == "assumption" for r in relied):
                out.append(Issue(where, f"{item_id}: tagged Assumed but relies on no register assumption", item_id, "warning"))
    for item_id, obj in p.live().items():
        current = [n for n, o in p.history[item_id]][-1]
        for up in obj.get("upstream_ids") or []:
            cur = p.current(up)
            if cur and cur.get("event") == "remove":
                out.append(Issue(p.label("trace", current), f"{item_id}: upstream {up} has been removed; rebuild or relink", item_id, "warning"))
    out += find_cycles(p)
    for n, obj in p.reviews:
        where = p.label("trace", n)
        ids = obj.get("item_ids") or []
        for i in ids:
            if i not in p.history:
                out.append(Issue(where, f"review names {i}, which has no trace"))
        for f in obj.get("findings") or []:
            if f.get("item_id") not in ids:
                out.append(Issue(where, f"finding on {f.get('item_id')}, which is not in the review's item_ids"))
    return out


def find_cycles(p):
    live = p.live()
    graph = {i: [u for u in (o.get("upstream_ids") or []) if u in live] for i, o in live.items()}
    state, out = {}, []

    def visit(node, stack):
        state[node] = 1
        for nxt in graph.get(node, []):
            if state.get(nxt) == 1:
                cycle = stack[stack.index(nxt):] + [nxt] if nxt in stack else [node, nxt]
                out.append(Issue(f"{p.slug}/{PO}/{FILES['trace']}", "upstream cycle: " + " -> ".join(cycle), node))
            elif not state.get(nxt):
                visit(nxt, stack + [nxt])
        state[node] = 2

    for node in sorted(graph):
        if not state.get(node):
            visit(node, [node])
    return out


def product_markdown(p):
    for path in sorted(p.dir.rglob("*.md")):
        rel = path.relative_to(p.dir)
        if rel.parts and rel.parts[0] == PO:
            continue
        yield rel.as_posix(), path.read_text(encoding="utf-8")


def check_markdown(p):
    """Every live item appears in its file; every item ID in the product's Markdown has a trace."""
    out = []
    texts = dict(product_markdown(p))
    for item_id, obj in p.live().items():
        n = p.history[item_id][-1][0]
        f = obj.get("file")
        if f not in texts:
            out.append(Issue(p.label("trace", n), f"{item_id}: file {f} not found in the product folder", item_id))
        elif item_id not in set(ID_IN_TEXT.findall(texts[f])):
            out.append(Issue(p.label("trace", n), f"{item_id}: ID does not appear in {f}", item_id))
    for rel, text in texts.items():
        for lineno, line in enumerate(text.splitlines(), 1):
            for found in ID_IN_TEXT.findall(line):
                if found.split("-")[0] not in PREFIXES:
                    continue
                if found not in p.history:
                    out.append(Issue(f"{p.slug}/{rel}:{lineno}", f"{found} has no trace record; declare it with scripts/traces.py add trace", found))
    return out


def check_feedback(p):
    out = []
    comment_ids = {}
    for fb_id, (n, obj) in p.feedback.items():
        where = p.label("feedback", n)
        target = obj.get("target") or {}
        for item_id in target.get("item_ids") or []:
            if item_id not in p.history:
                out.append(Issue(where, f"{fb_id}: names {item_id}, which has no trace"))
        for item_id, rev in (target.get("item_revs") or {}).items():
            if not p.write_at(item_id, rev):
                out.append(Issue(where, f"{fb_id}: {item_id} has no rev {rev}"))
        if target.get("level") in ("item", "quote") and not target.get("item_ids"):
            out.append(Issue(where, f"{fb_id}: level {target.get('level')} needs item_ids"))
        if target.get("level") in ("artefact", "section") and not target.get("file"):
            out.append(Issue(where, f"{fb_id}: level {target.get('level')} needs file"))
        if obj.get("source") == "pr-comment":
            cid = (obj.get("pr") or {}).get("comment_id")
            if cid is None:
                out.append(Issue(where, f"{fb_id}: a pr-comment needs pr.url and pr.comment_id"))
            elif cid in comment_ids and comment_ids[cid] != fb_id:
                out.append(Issue(where, f"{fb_id}: PR comment {cid} was already taken in as {comment_ids[cid]}"))
            else:
                comment_ids[cid] = fb_id
        if not any(r.get("type") == "feedback" and r.get("record") == fb_id for r in p.register.values()):
            out.append(Issue(where, f"{fb_id}: no register line of type feedback with record {fb_id}", level="warning"))
    return out


def check_step(p, step, where, label):
    out = []
    if not isinstance(step, dict):
        return out
    item_id = step.get("item_id")
    if item_id:
        hist = p.history.get(item_id)
        if not hist:
            out.append(Issue(where, f"{label} names {item_id}, which has no trace"))
        elif step.get("rev") is not None:
            w = p.write_at(item_id, step["rev"])
            if not w:
                out.append(Issue(where, f"{label}: {item_id} has no rev {step['rev']}"))
            else:
                for key in ("run", "stage", "agent", "step"):
                    if step.get(key) != w.get(key):
                        out.append(Issue(where, f"{label}: {key} {step.get(key)!r} does not match the trace of {item_id} rev {step['rev']} ({w.get(key)!r})"))
    return out


def check_attributions(p):
    out = []
    for at_id, (n, obj) in p.attributions.items():
        where = p.label("attribution", n)
        fb_id = obj.get("feedback")
        if fb_id not in p.feedback:
            out.append(Issue(where, f"{at_id}: feedback {fb_id} not found"))
            fb = {}
        else:
            fb = p.feedback[fb_id][1]
        out += check_step(p, obj.get("origin"), where, f"{at_id} origin")
        for i, c in enumerate(obj.get("carriers") or []):
            out += check_step(p, c, where, f"{at_id} carrier {i + 1}")
            if c == obj.get("origin"):
                out.append(Issue(where, f"{at_id}: carrier {i + 1} is the origin; a step is either where it began or where it was passed on"))
        for i, alt in enumerate(obj.get("alternatives") or []):
            out += check_step(p, alt.get("origin"), where, f"{at_id} alternative {i + 1}")
        conf = obj.get("confidence")
        if isinstance(conf, (int, float)) and (conf < LOW_CONFIDENCE or fb.get("category") == "not-sure"):
            if not obj.get("question_for_user") and obj.get("user_verdict") is None:
                out.append(Issue(where, f"{at_id}: confidence under {LOW_CONFIDENCE} or category not-sure needs question_for_user"))
        if isinstance(conf, (int, float)) and conf >= 0.8 and (obj.get("replay") or {}).get("result") != "confirmed":
            out.append(Issue(where, f"{at_id}: confidence 0.8 or more needs a replay that confirmed it", level="warning"))
        if not obj.get("alternatives") and isinstance(conf, (int, float)) and conf < 0.8:
            out.append(Issue(where, f"{at_id}: below high confidence but no alternatives given", level="warning"))
    return out


def check_reruns(p):
    out = []
    for rr_id, (n, obj) in p.reruns.items():
        where = p.label("rerun", n)
        for fb in obj.get("feedback") or []:
            if fb not in p.feedback:
                out.append(Issue(where, f"{rr_id}: feedback {fb} not found"))
        if obj.get("attribution") and obj["attribution"] not in p.attributions:
            out.append(Issue(where, f"{rr_id}: attribution {obj['attribution']} not found"))
        for key in ("invalidated", "kept", "rebuilt", "removed"):
            for i in obj.get(key) or []:
                if i not in p.history:
                    out.append(Issue(where, f"{rr_id}: {key} names {i}, which has no trace"))
        status = obj.get("status")
        if status in ("approved", "done", "committed") and not obj.get("user_ok"):
            out.append(Issue(where, f"{rr_id}: status {status} without user_ok; a rerun needs the user's OK first"))
        if status == "committed" and not obj.get("commit"):
            out.append(Issue(where, f"{rr_id}: status committed needs the commit"))
        if obj.get("commit") and status != "committed":
            out.append(Issue(where, f"{rr_id}: has a commit but status is {status}"))
        ref = (obj.get("correction") or {}).get("register_ref")
        if ref and ref not in p.register:
            out.append(Issue(where, f"{rr_id}: correction register_ref {ref} is not in the register"))
    return out


def ledger_rows(repo, issues=None):
    return read_jsonl(repo / PO / LEDGER, issues if issues is not None else [], f"{PO}/{LEDGER}")


def check_ledger(repo, products, rows=None):
    """Checks for <products repo>/.po/ledger.jsonl, or for the given rows. products: {slug: Product}."""
    issues = []
    label = f"{PO}/{LEDGER}"
    if rows is None:
        rows = ledger_rows(repo, issues)
    issues += schema_issues("ledger", rows, lambda n: f"{label}:{n}")
    for le_id, (n, obj) in latest_by_id(rows).items():
        where = f"{label}:{n}"
        ev = obj.get("evidence") or {}
        for ref in (ev.get("feedback") or []) + (ev.get("attributions") or []):
            slug, _, rid = str(ref).partition("/")
            p = products.get(slug)
            if not p:
                issues.append(Issue(where, f"{le_id}: {ref} names product {slug!r}, not found"))
            elif rid not in p.feedback and rid not in p.attributions:
                issues.append(Issue(where, f"{le_id}: {ref} not found"))
        if obj.get("decision") == "accepted":
            if (obj.get("review") or {}).get("verdict") != "PASS":
                issues.append(Issue(where, f"{le_id}: accepted, but learn-reviewer did not PASS it"))
            held_in, held_out = obj.get("held_in") or {}, obj.get("held_out") or {}
            if held_out.get("regressions"):
                issues.append(Issue(where, f"{le_id}: accepted with held-out regressions {held_out['regressions']}"))
            if isinstance(held_out.get("after"), int) and isinstance(held_out.get("before"), int) and held_out["after"] < held_out["before"]:
                issues.append(Issue(where, f"{le_id}: accepted though held-out passes fell from {held_out['before']} to {held_out['after']}"))
            if isinstance(held_in.get("after"), int) and isinstance(held_in.get("before"), int) and held_in["after"] <= held_in["before"]:
                issues.append(Issue(where, f"{le_id}: accepted though the held-in cases did not improve"))
            if not held_out.get("cases"):
                issues.append(Issue(where, f"{le_id}: accepted with no held-out cases"))
        if obj.get("applied") and obj.get("decision") != "accepted":
            issues.append(Issue(where, f"{le_id}: applied but the decision is {obj.get('decision')}"))
    return issues


def report(issues):
    errors = [i for i in issues if i.level == "error"]
    warnings = [i for i in issues if i.level == "warning"]
    for i in errors:
        print(f"error: {i}", file=sys.stderr)
    for i in warnings:
        print(f"warning: {i}", file=sys.stderr)
    return errors


# ---------------------------------------------------------------- commands

def cmd_new_run(args):
    print(new_run_id())
    return 0


def git(*args):
    out = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)
    return out.stdout.strip() if out.returncode == 0 else None


def version_of(rel):
    sha = git("log", "-1", "--format=%h", "--", rel) or "uncommitted"
    if git("status", "--porcelain", "--", rel):
        sha += "+dirty"
    return sha


def cmd_versions(args):
    skills_dir, templates_dir = ROOT / "skills", ROOT / "templates"
    names = [s for s in (args.skills or "").split(",") if s] or sorted(
        p.name for p in skills_dir.iterdir() if (p / "SKILL.md").exists())
    skills = {}
    for name in names:
        if name.startswith("po-") and (ROOT / "commands" / f"{name[3:]}.md").exists():
            skills[name] = version_of(f"commands/{name[3:]}.md")
        elif (skills_dir / name / "SKILL.md").exists():
            skills[name] = version_of(f"skills/{name}")
        else:
            raise SystemExit(f"no skill or command named {name!r}")
    templates = {}
    for rel in [t for t in (args.templates or "").split(",") if t]:
        if not (templates_dir / rel).exists():
            raise SystemExit(f"no template templates/{rel}")
        templates[rel] = version_of(f"templates/{rel}")
    head = git("rev-parse", "--short", "HEAD") or "unknown"
    if git("status", "--porcelain", "--untracked-files=no"):
        head += "+dirty"
    print(json.dumps({"aidev_po": head, "skill_versions": skills, "template_versions": templates}, indent=2))
    return 0


def next_number(ids, prefix):
    nums = [int(m.group(2)) for m in (re.match(rf"^({prefix})-([0-9]+)$", i) for i in ids) if m]
    return f"{prefix}-{(max(nums) if nums else 0) + 1:03d}"


def next_id_for(p, code):
    if code in RECORD_PREFIX.values():
        kind = {v: k for k, v in RECORD_PREFIX.items()}[code]
        return next_number([o.get("id", "") for _, o in p.rows[kind]], code)
    prefix = ITEM_TYPES.get(code, code if code in PREFIXES else None)
    if not prefix:
        raise SystemExit(f"unknown item type or prefix {code!r}; see x-item-types in schemas/trace.schema.json")
    return next_number(list(p.history), prefix)


def cmd_next_id(args):
    if args.type == "LE":
        print(next_number([o.get("id", "") for _, o in ledger_rows(repo_for(args))], "LE"))
        return 0
    print(next_id_for(Product(product_dir(args)), args.type))
    return 0


def parse_input(text):
    text = text.strip()
    if not text:
        raise SystemExit("nothing to add: pass --json or JSON on stdin")
    try:
        obj = json.loads(text)
        return obj if isinstance(obj, list) else [obj]
    except json.JSONDecodeError:
        return [json.loads(line) for line in text.splitlines() if line.strip()]


def fill_trace(folder, objs):
    """Fill ts, rev and item_id in new trace lines, in order, as if each earlier one were already appended."""
    for k, obj in enumerate(objs):
        staged = Product(folder, {"trace": objs[:k]})
        obj.setdefault("ts", now())
        if obj.get("event") == "write" and not obj.get("item_id"):
            obj["item_id"] = next_id_for(staged, obj.get("item_type", ""))
        if obj.get("event") in ("write", "remove") and "rev" not in obj:
            hist = staged.history.get(obj.get("item_id"), [])
            obj["rev"] = (hist[-1][1].get("rev", 0) if hist else 0) + 1
    return objs


def fill_records(rows, objs, prefix):
    ids = [o.get("id", "") for _, o in rows]
    for obj in objs:
        obj.setdefault("ts", now())
        if not obj.get("id"):
            obj["id"] = next_number(ids, prefix)
        ids.append(obj["id"])
    return objs


def cmd_add(args):
    """Append only if the new lines add no check errors (warnings are shown but allowed)."""
    objs = parse_input(args.json if args.json is not None else sys.stdin.read())
    if args.kind == "ledger":
        repo = repo_for(args)
        products = all_products(repo)
        rows = ledger_rows(repo)
        objs = fill_records(rows, objs, "LE")
        before = {i.key() for i in check_ledger(repo, products, rows)}
        last = rows[-1][0] if rows else 0
        after = check_ledger(repo, products, rows + [(last + 1 + k, o) for k, o in enumerate(objs)])
        path = repo / PO / LEDGER
    else:
        folder = product_dir(args)
        p = Product(folder)
        before = {i.key() for i in check_product(p)}
        objs = fill_trace(folder, objs) if args.kind == "trace" else fill_records(p.rows[args.kind], objs, RECORD_PREFIX[args.kind])
        after = check_product(Product(folder, {args.kind: objs}))
        path = folder / PO / FILES[args.kind]
    new = [i for i in after if i.key() not in before]
    if report(new):
        print("nothing appended", file=sys.stderr)
        return 1
    append(path, objs)
    for o in objs:
        print(f"{o['item_id']} rev {o['rev']}" if args.kind == "trace" and "item_id" in o else o.get("id", o.get("event")))
    return 0


def append(path, objs):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write("".join(json.dumps(o, ensure_ascii=False) + "\n" for o in objs))


def register_state(p, ref, ts=None):
    """The register entry's declare line and its latest update at or before ts (or now)."""
    decl = p.register.get(ref, {})
    state = decl
    for _, obj in p.rows["register"]:
        if obj.get("event") == "update" and obj.get("ref") == ref and (ts is None or str(obj.get("ts", "")) <= ts):
            state = obj
    return decl, state


def describe(p, item_id, w):
    """One node of a chain: the write line w, the reviews of that rev, and the register entries it relied on."""
    writes = [o for _, o in p.history[item_id] if o.get("event") == "write"]
    later = [o.get("ts", "") for _, o in p.history[item_id] if o.get("rev", 0) > w.get("rev", 0)]
    until = min(later) if later else None
    reviews = [{"agent": r.get("agent"), "verdict": r.get("verdict"), "run": r.get("run"),
                "findings": [f for f in r.get("findings") or [] if f.get("item_id") == item_id]}
               for _, r in p.reviews if item_id in (r.get("item_ids") or [])
               and str(r.get("ts", "")) >= w.get("ts", "") and (until is None or str(r.get("ts", "")) < until)]
    relied = []
    for ref in w.get("register_refs") or []:
        decl, then = register_state(p, ref, w.get("ts"))
        _, current = register_state(p, ref)
        relied.append({"id": ref, "type": decl.get("type"), "text": decl.get("text"),
                       "status_then": then.get("status"), "answer_then": then.get("answer"),
                       "status_now": current.get("status"), "answer_now": current.get("answer")})
    cur = p.current(item_id)
    return {"item_id": item_id, "rev": w.get("rev"), "latest_rev": cur.get("rev"), "removed": cur.get("event") == "remove",
            "item_type": w.get("item_type"), "summary": w.get("summary"), "file": w.get("file"), "ts": w.get("ts"),
            "run": w.get("run"), "stage": w.get("stage"), "agent": w.get("agent"), "step": w.get("step"),
            "evidence_tag": w.get("evidence_tag"), "sources": w.get("sources") or [],
            "skill_versions": w.get("skill_versions"), "template_versions": w.get("template_versions"),
            "rerun": w.get("rerun"), "register_refs": relied, "reviews": reviews, "upstream_ids": w.get("upstream_ids") or [],
            "revisions": len(writes)}


def cmd_chain(args):
    """Walk upstream from an item. With --feedback or --rev, each node is the rev in force at that time."""
    p = Product(product_dir(args))
    if args.item_id not in p.history:
        raise SystemExit(f"{args.item_id}: no trace")
    if args.feedback:
        if args.feedback not in p.feedback:
            raise SystemExit(f"{args.feedback}: not found")
        fb = p.feedback[args.feedback][1]
        rev = ((fb.get("target") or {}).get("item_revs") or {}).get(args.item_id)
        root = p.write_at(args.item_id, rev) if rev else p.write_before(args.item_id, fb.get("ts", ""))
    elif args.rev:
        root = p.write_at(args.item_id, args.rev)
    else:
        cur = p.current(args.item_id)
        root = cur if cur.get("event") == "write" else p.write_at(args.item_id, cur.get("rev", 2) - 1)
    if not root:
        raise SystemExit(f"{args.item_id}: no such rev")
    as_of = root.get("ts", "")
    nodes, order, seen = {}, [], set()

    def walk(item_id, w, depth):
        order.append((depth, item_id, item_id in seen))
        if item_id in seen:
            return
        seen.add(item_id)
        if not w:
            nodes[item_id] = {"item_id": item_id, "missing": True}
            return
        nodes[item_id] = describe(p, item_id, w)
        for up in nodes[item_id]["upstream_ids"]:
            walk(up, p.write_before(up, as_of), depth + 1)

    walk(args.item_id, root, 0)
    if args.json:
        print(json.dumps({"root": args.item_id, "as_of": as_of, "nodes": nodes,
                          "edges": [[i, u] for i, d in nodes.items() for u in d.get("upstream_ids", [])]}, indent=2))
        return 0
    print(f"as of {as_of}")
    for depth, item_id, repeat in order:
        pad = "  " * depth
        d = nodes[item_id]
        if repeat:
            print(f"{pad}{item_id} (see above)")
            continue
        if d.get("missing"):
            print(f"{pad}{item_id} (no trace at that time)")
            continue
        tag = d.get("evidence_tag")
        later = f", now rev {d['latest_rev']}" if d["latest_rev"] != d["rev"] else ""
        print(f"{pad}{item_id} rev {d['rev']}{later}{' REMOVED' if d['removed'] else ''} [{tag}] {d['summary']}")
        print(f"{pad}  wrote: {d['stage']} / {d['agent']} / step {d['step']} / {d['run']} in {d['file']}"
              f"{' / rerun ' + d['rerun'] if d.get('rerun') else ''}")
        print(f"{pad}  skills: {', '.join(f'{k}@{v}' for k, v in (d.get('skill_versions') or {}).items()) or 'none'}")
        for r in d["register_refs"]:
            then = f"{r['status_then']}: {r['answer_then']}" if r.get("answer_then") else r.get("status_then")
            now_ = f"{r['status_now']}: {r['answer_now']}" if r.get("answer_now") else r.get("status_now")
            changed = f" (now {now_})" if now_ != then else ""
            print(f"{pad}  relied on {r['id']} ({r['type']}): {r['text']} -> then {then}{changed}")
        if not d["register_refs"] and not d["upstream_ids"]:
            print(f"{pad}  relied on nothing")
        for r in d["reviews"]:
            notes = "; ".join(f"{f['severity']} {f['text']}" for f in r["findings"]) or "no finding on this item"
            print(f"{pad}  reviewed: {r['agent']} {r['verdict']} ({notes})")
        if not d["reviews"]:
            print(f"{pad}  reviewed: no review of this rev")
    return 0


def downstream_of(p, start, register_refs=()):
    """Live items whose current upstream reaches any start item, or that rely on a given register entry."""
    live = p.live()
    children = {}
    for i, o in live.items():
        for u in o.get("upstream_ids") or []:
            children.setdefault(u, set()).add(i)
    hit = set(start) & set(live)
    hit |= {i for i, o in live.items() if set(o.get("register_refs") or []) & set(register_refs)}
    todo = list(hit)
    while todo:
        for c in children.get(todo.pop(), ()):
            if c not in hit:
                hit.add(c)
                todo.append(c)
    return hit


def cmd_downstream(args):
    p = Product(product_dir(args))
    for i in args.item_ids:
        if i not in p.history:
            raise SystemExit(f"{i}: no trace")
    hit = downstream_of(p, args.item_ids, args.register_ref or [])
    live = p.live()
    rows = sorted(hit, key=lambda i: (STAGES.index(live[i].get("stage")) if live[i].get("stage") in STAGES else 99,
                                       live[i].get("file", ""), i))
    stages = sorted({live[i].get("stage") for i in hit}, key=lambda s: STAGES.index(s) if s in STAGES else 99)
    if args.json:
        print(json.dumps({"invalidated": rows, "reopened_stages": stages,
                          "files": sorted({live[i].get("file") for i in hit})}, indent=2))
        return 0
    for i in rows:
        print(f"{i}\t{live[i].get('stage')}\t{live[i].get('file')}\t{live[i].get('summary')}")
    print(f"{len(rows)} item(s); stages to reopen: {', '.join(stages) or 'none'}")
    return 0


def cmd_locate(args):
    p = Product(product_dir(args))
    path = p.dir / args.file
    if not path.exists():
        raise SystemExit(f"{args.file}: not found in {p.slug}")
    lines = path.read_text(encoding="utf-8").splitlines()
    if args.quote:
        hits = [n for n, l in enumerate(lines, 1) if args.quote in l]
        if not hits:
            raise SystemExit(f"quote not found in {args.file}")
        line = hits[0]
    else:
        line = args.line
    known = set(p.history)
    for n in range(min(line, len(lines)), 0, -1):
        ids = [i for i in ID_IN_TEXT.findall(lines[n - 1]) if i in known]
        if ids:
            print(json.dumps({"file": args.file, "line": line, "item_ids": ids[:1], "found_on_line": n,
                              "rev": {i: (p.current(i) or {}).get("rev") for i in ids[:1]}}))
            return 0
    print(json.dumps({"file": args.file, "line": line, "item_ids": [], "found_on_line": None}))
    return 0


def all_products(repo):
    return {d.name: Product(d) for d in sorted(repo.iterdir())
            if d.is_dir() and not d.name.startswith(".")} if repo.is_dir() else {}


def cmd_check(args):
    issues = []
    if args.all:
        repo = repo_for(args)
        products = all_products(repo)
        for p in products.values():
            issues += check_product(p)
        issues += check_ledger(repo, products)
        scope = f"{len(products)} product(s) and the ledger in {repo}"
    else:
        p = Product(product_dir(args))
        issues = check_product(p)
        scope = p.slug
    errors = report(issues)
    note = "" if validator("trace") else " (jsonschema not installed: schema checks skipped)"
    if errors:
        print(f"{len(errors)} error(s) in {scope}{note}", file=sys.stderr)
        return 1
    print(f"{scope}: ok{note}")
    return 0


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    def where(sp):
        sp.add_argument("--product", help="product folder name in the products repo")
        sp.add_argument("--dir", help="path to a product folder")
        sp.add_argument("--repo", help="products repo path (default: scripts/products-dir.py)")

    sub.add_parser("new-run")
    sp = sub.add_parser("versions")
    sp.add_argument("--skills")
    sp.add_argument("--templates")
    sp = sub.add_parser("next-id")
    sp.add_argument("type")
    where(sp)
    sp = sub.add_parser("add")
    sp.add_argument("kind", choices=["trace", "feedback", "attribution", "rerun", "ledger"])
    sp.add_argument("--json")
    where(sp)
    sp = sub.add_parser("chain")
    sp.add_argument("item_id")
    g = sp.add_mutually_exclusive_group()
    g.add_argument("--feedback", help="walk the revs in force when this feedback was given")
    g.add_argument("--rev", type=int, help="start from this rev of the item")
    sp.add_argument("--json", action="store_true")
    where(sp)
    sp = sub.add_parser("downstream")
    sp.add_argument("item_ids", nargs="+")
    sp.add_argument("--register-ref", action="append")
    sp.add_argument("--json", action="store_true")
    where(sp)
    sp = sub.add_parser("locate")
    sp.add_argument("file")
    g = sp.add_mutually_exclusive_group(required=True)
    g.add_argument("--line", type=int)
    g.add_argument("--quote")
    where(sp)
    sp = sub.add_parser("check")
    sp.add_argument("--all", action="store_true", help="every product in the products repo, and the ledger")
    where(sp)
    args = ap.parse_args(argv)
    return {"new-run": cmd_new_run, "versions": cmd_versions, "next-id": cmd_next_id, "add": cmd_add,
            "chain": cmd_chain, "downstream": cmd_downstream, "locate": cmd_locate, "check": cmd_check}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
