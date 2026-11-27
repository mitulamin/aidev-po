"""scripts/products-dir.py: argparse, paths inside the checkout, absolute paths, and --init's identity check and first commit."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from helpers import ROOT


class ProductsDir(unittest.TestCase):
    """Each test runs a copy of the script in a fake checkout, so the real aidev-po.local.json is never touched."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="aidev-po-test-")).resolve()
        self.addCleanup(shutil.rmtree, self.tmp)
        self.checkout = self.tmp / "aidev-po"
        (self.checkout / "scripts").mkdir(parents=True)
        shutil.copy(ROOT / "scripts" / "products-dir.py", self.checkout / "scripts" / "products-dir.py")
        self.home = self.tmp / "home"
        self.home.mkdir()
        self.config = self.checkout / "aidev-po.local.json"

    def env(self):
        env = {k: v for k, v in os.environ.items()
               if not k.startswith("GIT_") and k != "AIDEV_PO_PRODUCTS_DIR"}
        env.update(HOME=str(self.home), GIT_CONFIG_NOSYSTEM="1")
        return env

    def identity(self):
        (self.home / ".gitconfig").write_text("[user]\n\tname = Test User\n\temail = test@example.com\n")

    def run_script(self, *args):
        out = subprocess.run([sys.executable, str(self.checkout / "scripts" / "products-dir.py"), *map(str, args)],
                             capture_output=True, text=True, cwd=self.checkout, env=self.env())
        return out.returncode, out.stdout, out.stderr

    def git(self, path, *args):
        return subprocess.run(["git", "-C", str(path), *args], capture_output=True, text=True, env=self.env())

    def recorded(self):
        return json.loads(self.config.read_text())["products_dir"] if self.config.exists() else None

    def test_help(self):
        code, out, _ = self.run_script("--help")
        self.assertEqual(code, 0)
        self.assertIn("--set", out)
        self.assertIn("--init", out)

    def test_unknown_flag_errors(self):
        code, _, err = self.run_script("--frobnicate")
        self.assertEqual(code, 2)
        self.assertIn("unrecognized arguments", err)

    def test_init_needs_set(self):
        code, _, err = self.run_script("--init")
        self.assertEqual(code, 2)
        self.assertIn("--init goes with --set", err)

    def test_set_needs_a_path(self):
        code, _, _ = self.run_script("--set")
        self.assertEqual(code, 2)

    def test_rejects_checkout_and_any_path_inside_it(self):
        for path in (self.checkout, self.checkout / "products", "products/acme", "./scripts/.."):
            code, _, err = self.run_script("--set", path)
            self.assertNotEqual(code, 0, path)
            self.assertIn("inside the aidev-po checkout", err)
            self.assertIsNone(self.recorded(), path)

    def test_records_resolved_absolute_path(self):
        code, _, err = self.run_script("--set", "../aidev-products")
        self.assertEqual(code, 0, err)
        self.assertEqual(self.recorded(), str(self.tmp / "aidev-products"))
        code, _, err = self.run_script("--set", "~/products")
        self.assertEqual(code, 0, err)
        self.assertEqual(self.recorded(), str(self.home / "products"))

    def test_init_without_identity_records_nothing(self):
        target = self.tmp / "aidev-products"
        code, _, err = self.run_script("--set", target, "--init")
        self.assertNotEqual(code, 0)
        self.assertIn("user.name and user.email not set", err)
        self.assertIn("git config --global user.name", err)
        self.assertIsNone(self.recorded())
        self.assertFalse(target.exists())

    def test_init_with_only_name_set(self):
        (self.home / ".gitconfig").write_text("[user]\n\tname = Test User\n")
        code, _, err = self.run_script("--set", self.tmp / "aidev-products", "--init")
        self.assertNotEqual(code, 0)
        self.assertIn("user.email not set", err)
        self.assertIsNone(self.recorded())

    def test_init_commits_readme_and_gitignore(self):
        self.identity()
        target = self.tmp / "aidev-products"
        code, out, err = self.run_script("--set", target, "--init")
        self.assertEqual(code, 0, err)
        self.assertEqual(self.recorded(), str(target))
        files = self.git(target, "ls-files").stdout.split()
        self.assertEqual(sorted(files), [".gitignore", "README.md"])
        self.assertEqual(self.git(target, "remote").stdout.strip(), "")
        self.assertEqual(self.git(target, "status", "--porcelain").stdout.strip(), "")
        code, out, _ = self.run_script("--json")
        info = json.loads(out)
        self.assertEqual((info["state"], info["has_commits"]), ("git-local", True))

    def test_init_keeps_existing_readme(self):
        self.identity()
        target = self.tmp / "aidev-products"
        target.mkdir()
        (target / "README.md").write_text("mine\n")
        code, _, err = self.run_script("--set", target, "--init")
        self.assertEqual(code, 0, err)
        self.assertEqual((target / "README.md").read_text(), "mine\n")
        self.assertEqual(self.git(target, "ls-files").stdout.split(), [".gitignore"])

    def test_existing_repo_with_commits_needs_no_identity(self):
        target = self.tmp / "existing"
        target.mkdir()
        self.git(target, "init")
        self.git(target, "-c", "user.name=A", "-c", "user.email=a@example.com", "commit", "--allow-empty", "-m", "first")
        code, out, err = self.run_script("--set", target, "--init")
        self.assertEqual(code, 0, err)
        self.assertIn("already a git repo", out)
        self.assertEqual(self.git(target, "rev-list", "--count", "HEAD").stdout.strip(), "1")
        self.assertEqual(self.recorded(), str(target))


if __name__ == "__main__":
    unittest.main()
