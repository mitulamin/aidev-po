"""Shared helpers for the tests: run the scripts against a copy of the fixture products repo."""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "tests" / "fixtures" / "products-repo"
sys.path.insert(0, str(ROOT / "scripts"))


def copy_fixture():
    """A fresh copy of the fixture products repo in a temp folder. The caller removes it."""
    tmp = Path(tempfile.mkdtemp(prefix="aidev-po-test-"))
    shutil.copytree(FIXTURE, tmp / "products")
    return tmp / "products"


def run(script, *args, stdin=None):
    """Run scripts/<script> with args; return (exit code, stdout, stderr)."""
    out = subprocess.run([sys.executable, str(ROOT / "scripts" / script), *map(str, args)],
                         input=stdin, capture_output=True, text=True, cwd=ROOT)
    return out.returncode, out.stdout, out.stderr


def read_jsonl(path):
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]


def append_jsonl(path, obj):
    with Path(path).open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(obj) + "\n")
