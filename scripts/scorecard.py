#!/usr/bin/env python3
"""Work out the learning-loop measures for a products repo and keep its scorecard.

Usage:
  scripts/scorecard.py measures [--repo PATH] [--product SLUG] [--json]
  scripts/scorecard.py update   [--repo PATH]
  scripts/scorecard.py check    [--repo PATH | --file PATH]
  scripts/scorecard.py add-run  --skill NAME --stage STAGE --run RUN --scores triggered=2,followed=1,reviewer_caught=2,outcome=2,cost=2
                                [--product SLUG] [--date YYYY-MM-DD] [--harm] [--evidence LINK] [--note TEXT] [--repo PATH]

The products repo is --repo if given, else what scripts/products-dir.py reports. The scorecard
is <products repo>/.po/scorecard.json (schemas/scorecard.schema.json).

`measures` prints the per-run measures, worked out from every product's .po files and the
ledger. `update` writes them into the scorecard, keeping the per-skill rows. `check` validates
the scorecard and prints the verdict each skill's runs point to under ai-sdlc-loop's rules (the
user's verdict and note always win). `add-run` appends one run entry to a skill's row.

Definitions (also in the schema):
  feedback per 100 items   feedback on items as written in the run / items written in the run * 100
  reviewer catch share     reviewer findings / (reviewer findings + user feedback), as a percentage
  cause key                the attribution's cause and its origin agent, e.g. unsupported-inference / actors-producer
  repeat cause             an attribution whose cause key began in an earlier run too
  recurrence after edit    an attribution whose cause key matches an accepted ledger edit applied before its run
Attributions the user rejected are left out, and so are causes input-changed and unknown, which
are not failures of the loop.

Standard library only. jsonschema, if installed, is used by `check`.
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import traces as tr  # noqa: E402

SCORECARD = "scorecard.json"
SCHEMA_VERSION = "1.0.0"
CRITERIA = ("triggered", "followed", "reviewer_caught", "outcome", "cost")
MAX_TOTAL = 2 * len(CRITERIA)
SEVERITIES = ("P0", "P1", "P2", "P3")
NOT_FAILURES = {"input-changed", "unknown"}


def pct(num, den):
    return None if not den else round(100.0 * num / den, 1)


def per100(num, den):
    return None if not den else round(100.0 * num / den, 1)


def by_severity(fbs):
    out = {"total": len(fbs)}
    for s in SEVERITIES:
        out[s] = sum(1 for f in fbs if f.get("severity") == s)
    return out


def runs_of(p):
    """{run: {"stages": [...], "start": ts, "items": set, "findings": n}} from the trace."""
    runs = {}
    for _, obj in p.rows["trace"]:
        run = obj.get("run")
        if not run:
            continue
        r = runs.setdefault(run, {"stages": [], "start": obj.get("ts", ""), "items": set(), "findings": 0})
        r["start"] = min(r["start"], obj.get("ts", ""))
        if obj.get("stage") and obj["stage"] not in r["stages"]:
            r["stages"].append(obj["stage"])
        if obj.get("event") == "write":
            r["items"].add(obj["item_id"])
        if obj.get("event") == "review":
            r["findings"] += len(obj.get("findings") or [])
    return runs


def feedback_runs(p, fb):
    """The runs a feedback line is about: the runs that wrote the revs it names, or the run it names."""
    target = fb.get("target") or {}
    runs = set()
    if target.get("run"):
        runs.add(target["run"])
    revs = target.get("item_revs") or {}
    for item_id in target.get("item_ids") or []:
        w = p.write_at(item_id, revs[item_id]) if item_id in revs else p.write_before(item_id, fb.get("ts", ""))
        if w:
            runs.add(w.get("run"))
    if not runs and target.get("file"):
        latest = None
        for _, obj in p.rows["trace"]:
            if obj.get("event") == "write" and obj.get("file") == target["file"] and obj.get("ts", "") <= fb.get("ts", ""):
                latest = obj
        if latest:
            runs.add(latest.get("run"))
    return runs


def counted_attributions(p):
    """Current attribution per feedback, leaving out rejected ones and non-failure causes."""
    out = []
    for fb_id, (_, fb) in p.feedback.items():
        if fb.get("withdrawn"):
            continue
        at = p.attribution_for(fb_id)
        if at and at.get("user_verdict") != "rejected" and at.get("cause") not in NOT_FAILURES:
            out.append(at)
    return out


def applied_edits(repo, products):
    """[(applied ts, {cause keys})] for accepted, applied ledger edits."""
    edits = []
    for _, (_, obj) in tr.latest_by_id(tr.ledger_rows(repo)).items():
        if obj.get("decision") != "accepted" or not obj.get("applied"):
            continue
        keys = set()
        for ref in (obj.get("evidence") or {}).get("attributions") or []:
            slug, _, at_id = ref.partition("/")
            p = products.get(slug)
            at = p.attributions.get(at_id, (0, None))[1] if p else None
            if at:
                keys.add((at.get("cause"), (at.get("origin") or {}).get("agent")))
        edits.append((obj["applied"].get("ts") or obj.get("ts", ""), keys))
    return edits


def compute(repo, only=None):
    products = tr.all_products(repo)
    edits = applied_edits(repo, products)
    held_out_regressions = sum(1 for _, (_, o) in tr.latest_by_id(tr.ledger_rows(repo)).items()
                               if o.get("decision") == "accepted" and (o.get("held_out") or {}).get("regressions"))
    rows = []
    for slug, p in products.items():
        runs = runs_of(p)
        issues = tr.check_product(p)
        bad_items = {i.item for i in issues if i.level == "error" and i.item}
        fb_by_run = {}
        for fb_id, (_, fb) in p.feedback.items():
            if fb.get("withdrawn"):
                continue
            for run in feedback_runs(p, fb):
                fb_by_run.setdefault(run, []).append(fb)
        ats = counted_attributions(p)
        for run, r in runs.items():
            fbs = fb_by_run.get(run, [])
            fb_ids = {f["id"] for f in fbs}
            run_ats = [a for a in ats if a.get("feedback") in fb_ids]
            origins = [a for a in ats if (a.get("origin") or {}).get("run") == run]
            items = len(r["items"])
            sev = by_severity(fbs)
            rows.append({
                "product": slug, "run": run, "stage": ",".join(r["stages"]), "date": r["start"][:10],
                "start": r["start"], "items_written": items,
                "trace_complete_pct": pct(len(r["items"] - bad_items), items),
                "feedback": sev,
                "feedback_per_100_items": {k: per100(sev[k], items) for k in ("total",) + SEVERITIES},
                "p0_p1": sev["P0"] + sev["P1"],
                "reviewer_findings": r["findings"],
                "reviewer_catch_share": pct(r["findings"], r["findings"] + sev["total"]),
                "attributions": len(run_ats),
                "origins_in_run": len(origins),
                "confirmed": sum(1 for a in run_ats if a.get("user_verdict") == "confirmed"),
                "confirmed_share": pct(sum(1 for a in run_ats if a.get("user_verdict") == "confirmed"), len(run_ats)),
                "_origins": [((a.get("cause"), a["origin"].get("agent")), a) for a in origins],
            })
    rows.sort(key=lambda m: (m["start"], m["product"], m["run"]))
    seen = {}
    causes = {}
    for m in rows:
        repeats = recur = 0
        for key, at in m["_origins"]:
            if key in seen and seen[key] != m["run"]:
                repeats += 1
            seen.setdefault(key, m["run"])
            later = [ts for ts, keys in edits if key in keys and ts <= m["start"]]
            if later:
                recur += 1
            c = causes.setdefault(key, {"cause": key[0], "agent": key[1], "count": 0, "runs": set(), "products": set(),
                                        "first_seen": m["date"], "last_seen": m["date"], "after_edit": 0})
            c["count"] += 1
            c["runs"].add(m["run"])
            c["products"].add(m["product"])
            c["last_seen"] = m["date"]
            c["after_edit"] += 1 if later else 0
        m["repeat_causes"] = repeats
        m["repeat_cause_rate"] = pct(repeats, m["origins_in_run"])
        m["recurrence_after_edit"] = recur
    stages = []
    for slug, p in products.items():
        runs = runs_of(p)
        for stage in tr.STAGES:
            gates = sum(1 for r in runs.values() if stage in r["stages"])
            questions = sum(1 for o in p.register.values() if o.get("type") == "question" and o.get("phase") == stage)
            if gates or questions:
                stages.append({"product": slug, "stage": stage, "gates": gates, "questions": questions,
                               "questions_per_gate": None if not gates else round(questions / gates, 1)})
    if only:
        rows = [m for m in rows if m["product"] == only]
        stages = [s for s in stages if s["product"] == only]
    measures = [{k: v for k, v in m.items() if not k.startswith("_") and k != "start"} for m in rows]
    total_items = sum(m["items_written"] for m in measures)
    all_fb = [fb for slug, p in products.items() if not only or slug == only
              for _, (_, fb) in p.feedback.items() if not fb.get("withdrawn")]
    all_ats = [a for slug, p in products.items() if not only or slug == only for a in counted_attributions(p)]
    findings = sum(m["reviewer_findings"] for m in measures)
    origins = sum(1 for m in rows for _ in m["_origins"])
    traced_ok = sum(m["items_written"] * (m["trace_complete_pct"] or 0) / 100 for m in measures)
    summary = {
        "runs": len(measures), "items_written": total_items, "feedback": by_severity(all_fb),
        "feedback_per_100_items": per100(len(all_fb), total_items),
        "trace_complete_pct": pct(round(traced_ok), total_items),
        "reviewer_catch_share": pct(findings, findings + len(all_fb)),
        "confirmed_share": pct(sum(1 for a in all_ats if a.get("user_verdict") == "confirmed"), len(all_ats)),
        "repeat_cause_rate": pct(sum(m["repeat_causes"] for m in measures), origins),
        "recurrence_after_edit": sum(m["recurrence_after_edit"] for m in measures),
        "held_out_regressions": held_out_regressions,
    }
    cause_list = [dict(c, runs=len(c["runs"]), products=sorted(c["products"]))
                  for c in sorted(causes.values(), key=lambda c: (-c["count"], c["cause"], c["agent"] or ""))
                  if not only or only in c["products"]]
    return {"measures": measures, "stages": stages, "causes": cause_list, "summary": summary}


def scorecard_path(repo):
    return repo / tr.PO / SCORECARD


def load_scorecard(path):
    if not path.exists():
        return {"schema_version": SCHEMA_VERSION,
                "note": "skills: one row per skill, a run entry added by po after each run, each criterion 0 to 2. "
                        "measures, stages, causes and summary: written by scripts/scorecard.py update.",
                "skills": []}
    return json.loads(path.read_text(encoding="utf-8"))


def save(path, doc):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def fmt(v):
    return "-" if v is None else str(v)


def cmd_measures(args):
    repo = tr.repo_for(args)
    out = compute(repo, args.product)
    if args.json:
        print(json.dumps(out, indent=2))
        return 0
    print("product\trun\tstage\titems\tfeedback\tper 100\tP0+P1\ttraced %\treviewer catch %\torigins\trepeat %\tafter edit")
    for m in out["measures"]:
        print("\t".join(fmt(v) for v in (m["product"], m["run"], m["stage"], m["items_written"], m["feedback"]["total"],
                                          m["feedback_per_100_items"]["total"], m["p0_p1"], m["trace_complete_pct"],
                                          m["reviewer_catch_share"], m["origins_in_run"], m["repeat_cause_rate"],
                                          m["recurrence_after_edit"])))
    s = out["summary"]
    print(f"\n{s['runs']} run(s), {s['items_written']} item(s), {s['feedback']['total']} feedback "
          f"({fmt(s['feedback_per_100_items'])} per 100 items), repeat-cause rate "
          f"{'-' if s['repeat_cause_rate'] is None else str(s['repeat_cause_rate']) + '%'}, "
          f"recurrence after edit {s['recurrence_after_edit']}, held-out regressions {s['held_out_regressions']}")
    for c in out["causes"]:
        print(f"cause {c['cause']} / {c['agent']}: {c['count']} time(s) in {c['runs']} run(s), {c['after_edit']} after an edit")
    return 0


def cmd_update(args):
    repo = tr.repo_for(args)
    path = scorecard_path(repo)
    doc = load_scorecard(path)
    doc.update(compute(repo))
    doc["generated"] = tr.now()
    save(path, doc)
    print(f"wrote {path}")
    return 0


def suggest(row):
    """The verdict a skill's runs point to under ai-sdlc-loop's rules; the user's verdict wins."""
    runs = row.get("runs") or []
    if not runs:
        return None, "no runs yet"
    shares = [r.get("total", 0) / MAX_TOTAL for r in runs]
    if all((r.get("scores") or {}).get("triggered", 0) == 0 for r in runs):
        return "drop", "never triggered"
    if any(r.get("harm_flag") for r in runs):
        return None, "harm flagged in a run: the user decides"
    if sum(1 for s in shares if s >= 0.7) >= 2:
        return "keep", "70% or more of the maximum in at least two runs, no harm"
    if all(s <= 0.4 for s in shares):
        return "drop", "40% or less of the maximum in every run"
    return None, "not enough evidence yet"


def check_doc(doc, label):
    errors = []
    v = None
    try:
        import jsonschema
        schema = json.loads((tr.SCHEMAS / "scorecard.schema.json").read_text(encoding="utf-8"))
        v = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
    except ImportError:
        pass
    if v:
        for err in v.iter_errors(doc):
            errors.append(f"{label}: schema: {'/'.join(str(x) for x in err.path)}: {err.message}")
    names = set()
    for row in doc.get("skills") or []:
        name = row.get("skill_name")
        if name in names:
            errors.append(f"{label}: skill {name} has two rows")
        names.add(name)
        for r in row.get("runs") or []:
            scores = r.get("scores") or {}
            if all(isinstance(scores.get(c), int) for c in CRITERIA) and r.get("total") != sum(scores[c] for c in CRITERIA):
                errors.append(f"{label}: {name} run {r.get('run_id')}: total {r.get('total')} is not the sum of the scores "
                              f"({sum(scores[c] for c in CRITERIA)})")
    return errors


def cmd_check(args):
    path = Path(args.file) if args.file else scorecard_path(tr.repo_for(args))
    if not path.exists():
        raise SystemExit(f"{path}: not found")
    doc = json.loads(path.read_text(encoding="utf-8"))
    errors = check_doc(doc, path.name)
    try:
        import jsonschema  # noqa: F401
    except ImportError:
        print(tr.NO_JSONSCHEMA.replace("no line was", "the scorecard was not"), file=sys.stderr)
    for e in errors:
        print(f"error: {e}", file=sys.stderr)
    for row in doc.get("skills") or []:
        verdict, why = suggest(row)
        current = row.get("verdict")
        note = "" if verdict in (None, current) or current is None else f" (the user chose {current})"
        print(f"{row.get('skill_name')}: runs point to {verdict or 'no verdict'}: {why}{note}")
    return 1 if errors else 0


def cmd_add_run(args):
    repo = tr.repo_for(args)
    path = scorecard_path(repo)
    doc = load_scorecard(path)
    scores = {}
    for part in args.scores.split(","):
        key, _, val = part.partition("=")
        if key not in CRITERIA or not val.isdigit() or int(val) > 2:
            raise SystemExit(f"bad score {part!r}: use {', '.join(CRITERIA)} with 0, 1 or 2")
        scores[key] = int(val)
    missing = [c for c in CRITERIA if c not in scores]
    if missing:
        raise SystemExit(f"missing scores: {', '.join(missing)}")
    row = next((r for r in doc["skills"] if r["skill_name"] == args.skill), None)
    if row is None:
        row = {"skill_name": args.skill, "stage": args.stage, "runs": [], "verdict": None}
        doc["skills"].append(row)
    entry = {"run_id": args.run, "date": args.date or datetime.now(timezone.utc).strftime("%Y-%m-%d"),
             "scores": scores, "total": sum(scores.values()), "harm_flag": bool(args.harm)}
    if args.product:
        entry["product"] = args.product
    if args.evidence:
        entry["evidence_link"] = args.evidence
    if args.note:
        entry["human_note"] = args.note
    row["runs"].append(entry)
    errors = check_doc(doc, path.name)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    save(path, doc)
    print(f"{args.skill}: run {args.run} total {entry['total']} of {MAX_TOTAL}")
    return 0


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sp = sub.add_parser("measures")
    sp.add_argument("--repo")
    sp.add_argument("--product")
    sp.add_argument("--json", action="store_true")
    sp = sub.add_parser("update")
    sp.add_argument("--repo")
    sp = sub.add_parser("check")
    sp.add_argument("--repo")
    sp.add_argument("--file")
    sp = sub.add_parser("add-run")
    sp.add_argument("--repo")
    sp.add_argument("--skill", required=True)
    sp.add_argument("--stage", required=True, choices=tr.STAGES + ["learn", "all"])
    sp.add_argument("--run", required=True)
    sp.add_argument("--scores", required=True)
    sp.add_argument("--product")
    sp.add_argument("--date")
    sp.add_argument("--harm", action="store_true")
    sp.add_argument("--evidence")
    sp.add_argument("--note")
    args = ap.parse_args(argv)
    return {"measures": cmd_measures, "update": cmd_update, "check": cmd_check, "add-run": cmd_add_run}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
