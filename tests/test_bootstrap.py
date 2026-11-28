"""scripts/bootstrap.sh, scripts/new-project.sh and scripts/install-harness.py.

Covers: create from nothing, an empty folder, an add-on to a project that already has ai-sdlc-loop
(legacy format as ai-sdlc-loop main writes it today, and the drop-in manifest format), a second run
that changes nothing, and either order. Every test works in a temp folder.

The tests marked "real ai-sdlc-loop" run ai-sdlc-loop's own bootstrap and need AI_SDLC_LOOP_DIR set to a
checkout of it; CI sets it. Without it they are skipped.
"""
import hashlib
import json
import os
import pty
import select
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

from helpers import ROOT

FIXTURE = ROOT / "tests" / "fixtures" / "ai-sdlc-loop-main-1d47323"
INSTALL = ROOT / "scripts" / "install-harness.py"
NEW_PROJECT = ROOT / "scripts" / "new-project.sh"
BOOTSTRAP = ROOT / "scripts" / "bootstrap.sh"
SDLC_DIR = os.environ.get("AI_SDLC_LOOP_DIR")


def snapshot(folder):
    """{relative path: sha256} of every file under folder, .git excluded."""
    out = {}
    for path in sorted(Path(folder).rglob("*")):
        rel = path.relative_to(folder)
        if ".git" in rel.parts or not path.is_file():
            continue
        out[rel.as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return out


def mtimes(folder):
    return {p.relative_to(folder).as_posix(): p.stat().st_mtime_ns
            for p in Path(folder).rglob("*") if p.is_file() and ".git" not in p.relative_to(folder).parts}


class BootstrapCase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="aidev-po-bootstrap-")).resolve()
        self.addCleanup(shutil.rmtree, self.tmp)
        self.home = self.tmp / "home"
        self.home.mkdir()

    def env(self, **extra):
        env = {k: v for k, v in os.environ.items()
               if not k.startswith(("GIT_", "AIDEV_PO_")) and k != "AI_SDLC_LOOP_DIR"}
        env.update(HOME=str(self.home), GIT_CONFIG_NOSYSTEM="1")
        env.update(extra)
        return env

    def run_cmd(self, *cmd, stdin="", **extra_env):
        out = subprocess.run([str(c) for c in cmd], input=stdin, capture_output=True, text=True,
                             cwd=self.tmp, env=self.env(**extra_env))
        return out.returncode, out.stdout, out.stderr

    def new_project(self, target, *args):
        return self.run_cmd(NEW_PROJECT, *args, target)

    def run_tty(self, *cmd, stdin="", **extra_env):
        """Run a command with a terminal, so bootstrap.sh treats the wizard as interactive."""
        master, slave = pty.openpty()
        proc = subprocess.Popen([str(c) for c in cmd], stdin=slave, stdout=slave, stderr=slave,
                                cwd=self.tmp, env=self.env(**extra_env), close_fds=True)
        os.close(slave)
        if stdin:
            os.write(master, stdin.encode())
        chunks = []
        deadline = time.time() + 30

        def drain(wait):
            ready, _, _ = select.select([master], [], [], wait)
            if not ready:
                return False
            try:
                data = os.read(master, 65536)
            except OSError:
                return False
            if data:
                chunks.append(data)
            return bool(data)

        while time.time() < deadline:
            if drain(0.5):
                continue
            if proc.poll() is not None:
                while drain(0.2):
                    pass
                break
        if proc.poll() is None:
            proc.kill()
        code = proc.wait()
        os.close(master)
        text = b"".join(chunks).decode("utf-8", "replace")
        return code, text, text

    def copy_fixture(self, name="project"):
        target = self.tmp / name
        shutil.copytree(FIXTURE, target)
        subprocess.run(["git", "init", "-q"], cwd=target, check=True, env=self.env())
        return target

    def assert_registered(self, project):
        project = Path(project)
        manifest = json.loads((project / ".aidev-po" / "install.json").read_text())
        self.assertEqual(manifest["tool"], "aidev-po")
        self.assertTrue((project / ".cursor" / "rules" / "aidev-po-bootstrap.mdc").is_file())
        self.assertTrue((project / ".cursor" / "agents" / "po.md").is_file())
        self.assertTrue((project / ".cursor" / "skills" / "po-start" / "SKILL.md").is_file())
        self.assertTrue((project / ".aidev-po" / "scripts" / "products-dir.py").is_file())
        for rel, digest in manifest["files"].items():
            self.assertEqual(hashlib.sha256((project / rel).read_bytes()).hexdigest(), digest, rel)
        return manifest

    def assert_untouched(self, before, project):
        after = snapshot(project)
        for rel, digest in before.items():
            self.assertEqual(after.get(rel), digest, f"{rel} changed or went missing")


class FreshInstall(BootstrapCase):
    def test_missing_target_is_created_with_git_init_and_registered(self):
        target = self.tmp / "nested" / "does-not-exist-yet"
        self.assertFalse(target.exists())
        code, out, err = self.new_project(target)
        self.assertEqual(code, 0, err)
        self.assertTrue(target.is_dir())
        self.assertTrue((target / ".git").exists())
        head = subprocess.run(["git", "-C", target, "symbolic-ref", "HEAD"], capture_output=True, text=True).stdout.strip()
        self.assertEqual(head, "refs/heads/main")
        log = subprocess.run(["git", "-C", target, "log", "--oneline"], capture_output=True, text=True)
        self.assertNotEqual(log.returncode, 0, "no commits are made")
        remotes = subprocess.run(["git", "-C", target, "remote"], capture_output=True, text=True).stdout.strip()
        self.assertEqual(remotes, "")
        self.assert_registered(target)

    def test_installs_only_aidev_po(self):
        target = self.tmp / "p"
        self.assertEqual(self.new_project(target)[0], 0)
        top = {p.name for p in target.iterdir()}
        self.assertEqual(top, {".git", ".cursor", ".aidev-po"})
        self.assertFalse((target / "AGENTS.md").exists())
        self.assertFalse((target / ".ai-sdlc").exists())
        names = {p.name for p in (target / ".cursor" / "rules").iterdir()}
        self.assertEqual(names, {"aidev-po-bootstrap.mdc"})

    def test_empty_existing_folder_is_initialised_and_registered(self):
        target = self.tmp / "empty"
        target.mkdir()
        code, _, err = self.new_project(target)
        self.assertEqual(code, 0, err)
        self.assertTrue((target / ".git").exists())
        self.assert_registered(target)

    def test_empty_folder_that_is_already_a_repo_is_not_reinitialised(self):
        target = self.tmp / "repo"
        target.mkdir()
        subprocess.run(["git", "init", "-q", "-b", "trunk"], cwd=target, check=True, env=self.env())
        self.assertEqual(self.new_project(target, "--yes", "--git-init")[0], 0)
        head = subprocess.run(["git", "-C", target, "symbolic-ref", "HEAD"], capture_output=True, text=True).stdout.strip()
        self.assertEqual(head, "refs/heads/trunk")

    def test_never_writes_settings_mcp_or_hooks(self):
        target = self.tmp / "p"
        self.assertEqual(self.new_project(target)[0], 0)
        files = set(snapshot(target))
        for rel in files:
            name = Path(rel).name
            self.assertNotIn(name, {"mcp.json", "hooks.json", "settings.json", "settings.local.json", "mcp_config.json"}, rel)
            self.assertFalse(rel.startswith((".vscode/", ".claude/", ".cursor/mcp", ".cursor/hooks")), rel)
        self.assertEqual({p.name for p in (target / ".cursor").iterdir()}, {"agents", "skills", "rules"})

    def test_installed_agents_match_the_generated_ones_apart_from_rewrites(self):
        target = self.tmp / "p"
        self.assertEqual(self.new_project(target)[0], 0)
        source = {p.name for p in (ROOT / ".cursor" / "agents").glob("*.md")}
        installed = {p.name for p in (target / ".cursor" / "agents").glob("*.md")}
        self.assertEqual(installed, (source - {"learn-producer.md", "learn-reviewer.md"})
                         | {"po-learn-producer.md", "po-learn-reviewer.md"})
        text = (target / ".cursor" / "agents" / "po-learn-reviewer.md").read_text()
        self.assertIn("name: po-learn-reviewer", text)
        self.assertIn("Modelled on ai-sdlc-loop's learn-reviewer", text, "mentions of ai-sdlc-loop's own agent stay")
        po = (target / ".cursor" / "agents" / "po.md").read_text()
        self.assertIn(".aidev-po/scripts/products-dir.py", po)
        self.assertIn("po-learn-producer", po)

    def test_target_inside_the_checkout_is_refused(self):
        inside = ROOT / "tests" / "_should-not-exist"
        try:
            code, _, err = self.new_project(inside)
            self.assertNotEqual(code, 0)
            self.assertIn("inside the aidev-po checkout", err)
            self.assertFalse(inside.exists())
        finally:
            shutil.rmtree(inside, ignore_errors=True)

    def test_unknown_harness_and_help(self):
        code, _, err = self.run_cmd(NEW_PROJECT, "--harness", "nope", self.tmp / "p")
        self.assertNotEqual(code, 0)
        self.assertIn("Unknown harness", err)
        self.assertFalse((self.tmp / "p").exists())
        code, out, _ = self.run_cmd(NEW_PROJECT, "--help")
        self.assertEqual(code, 0)
        self.assertIn("--harness", out)
        self.assertIn("--yes", out)
        self.assertIn("--git-init", out)
        self.assertIn("--no-git-init", out)
        self.assertIn("cursor", out)

    def test_harness_data_lists_cursor(self):
        code, out, _ = self.run_cmd(sys.executable, INSTALL, "--list")
        self.assertEqual(code, 0)
        self.assertIn("cursor\tCursor", out)
        self.assertEqual(self.run_cmd(sys.executable, INSTALL, "--validate", "cursor")[0], 0)
        self.assertEqual(self.run_cmd(sys.executable, INSTALL, "--validate", "claude-code")[0], 1)


class AddOnToSdlc(BootstrapCase):
    def test_legacy_ai_sdlc_loop_project_is_recognised_and_left_byte_identical(self):
        project = self.copy_fixture()
        before = snapshot(project)
        self.assertIn(".ai-sdlc/register.jsonl", before)
        code, out, err = self.new_project(project, "--yes")
        self.assertEqual(code, 0, err)
        self.assertIn("Found ai-sdlc-loop already registered here (legacy format", out)
        self.assertIn("Left untouched", out)
        self.assert_untouched(before, project)
        self.assert_registered(project)
        after = snapshot(project)
        self.assertTrue(all(r.startswith((".aidev-po/", ".cursor/")) for r in set(after) - set(before)))

    def test_non_empty_folder_without_yes_is_refused(self):
        project = self.tmp / "plain"
        shutil.copytree(FIXTURE, project)
        before = snapshot(project)
        code, _, err = self.new_project(project)
        self.assertNotEqual(code, 0)
        self.assertIn("There are files in", err)
        self.assertIn("Nothing was written", err)
        self.assertIn("--yes", err)
        self.assertEqual(snapshot(project), before)
        self.assertFalse((project / ".aidev-po").exists())

    def test_git_init_is_the_default_and_no_git_init_leaves_the_folder(self):
        project = self.tmp / "plain"
        shutil.copytree(FIXTURE, project)
        code, out, err = self.new_project(project, "--yes")
        self.assertEqual(code, 0, err)
        self.assertTrue((project / ".git").exists())
        self.assertIn("Ran git init", out)
        head = subprocess.run(["git", "-C", project, "symbolic-ref", "HEAD"], capture_output=True, text=True).stdout.strip()
        self.assertEqual(head, "refs/heads/main")
        left = self.tmp / "left"
        shutil.copytree(FIXTURE, left)
        code, out, err = self.new_project(left, "--yes", "--no-git-init")
        self.assertEqual(code, 0, err)
        self.assertFalse((left / ".git").exists())
        self.assertIn("without a Git repository", out)
        self.assert_registered(left)

    def test_both_tools_agents_coexist_with_distinct_names(self):
        project = self.copy_fixture()
        self.assertEqual(self.new_project(project, "--yes")[0], 0)
        agents = project / ".cursor" / "agents"
        self.assertIn("ai-sdlc-loop", (agents / "learn-reviewer.md").read_text())
        self.assertIn("aidev-po", (agents / "po-learn-reviewer.md").read_text() + "aidev-po")
        self.assertTrue((agents / "coordinator.md").is_file() and (agents / "po.md").is_file())
        sdlc_skills = {p.name for p in (FIXTURE / ".cursor" / "skills").iterdir()}
        po_skills = {p.name for p in (ROOT / ".cursor" / "skills").iterdir()}
        self.assertEqual(sdlc_skills & po_skills, set())

    def test_manifest_format_registration_is_recognised_and_left_alone(self):
        project = self.tmp / "other"
        (project / ".other-tool").mkdir(parents=True)
        (project / ".other-tool" / "install.json").write_text(json.dumps({"tool": "other-tool", "files": {}}) + "\n")
        (project / ".cursor" / "rules").mkdir(parents=True)
        (project / ".cursor" / "rules" / "other-tool-bootstrap.mdc").write_text("---\nalwaysApply: true\n---\nOther.\n")
        before = snapshot(project)
        code, out, err = self.new_project(project, "--yes")
        self.assertEqual(code, 0, err)
        self.assertIn("Found other-tool already registered here (manifest format", out)
        self.assert_untouched(before, project)
        self.assert_registered(project)

    def test_sdlc_manifest_with_the_name_ai_sdlc_loop_is_recognised(self):
        project = self.copy_fixture()
        (project / ".ai-sdlc" / "install.json").write_text(json.dumps({"tool": "ai-sdlc-loop", "files": {}}) + "\n")
        before = snapshot(project)
        code, out, _ = self.new_project(project, "--yes")
        self.assertEqual(code, 0)
        self.assertIn("ai-sdlc-loop", out)
        self.assert_untouched(before, project)

    def test_detect(self):
        project = self.copy_fixture()
        code, out, _ = self.run_cmd(sys.executable, INSTALL, "--detect", project)
        self.assertEqual(code, 0)
        found = json.loads(out)
        self.assertEqual([f["tool"] for f in found], ["ai-sdlc-loop"])
        self.assertEqual(found[0]["format"], "legacy")
        empty = self.tmp / "e"
        empty.mkdir()
        self.assertEqual(json.loads(self.run_cmd(sys.executable, INSTALL, "--detect", empty)[1]), [])

    def test_aidev_po_first_then_sdlc_files_added_then_aidev_po_again(self):
        project = self.tmp / "order"
        self.assertEqual(self.new_project(project)[0], 0)
        po_before = {k: v for k, v in snapshot(project).items()}
        for path in sorted(FIXTURE.rglob("*")):
            if path.is_file():
                rel = path.relative_to(FIXTURE)
                self.assertFalse((project / rel).exists(), f"{rel} clashes with an aidev-po file")
                (project / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(path, project / rel)
        sdlc = snapshot(FIXTURE)
        mid = snapshot(project)
        code, out, err = self.new_project(project, "--yes")
        self.assertEqual(code, 0, err)
        self.assertIn("Found ai-sdlc-loop", out)
        self.assertEqual(snapshot(project), mid, "the second aidev-po run changed something")
        self.assert_untouched(po_before, project)
        self.assert_untouched(sdlc, project)


class Idempotent(BootstrapCase):
    def test_second_run_on_a_created_project_changes_nothing(self):
        target = self.tmp / "p"
        self.assertEqual(self.new_project(target)[0], 0)
        before, times = snapshot(target), mtimes(target)
        code, out, err = self.new_project(target, "--yes")
        self.assertEqual(code, 0, err)
        self.assertIn("Nothing changed", out)
        self.assertEqual(snapshot(target), before)
        self.assertEqual(mtimes(target), times, "no file was rewritten")
        status = subprocess.run(["git", "-C", target, "status", "--porcelain"], capture_output=True, text=True).stdout
        self.assertEqual(status.strip().split("\n")[0:2], ["?? .aidev-po/", "?? .cursor/"])

    def test_second_run_on_an_sdlc_project_is_a_no_op(self):
        project = self.copy_fixture()
        self.assertEqual(self.new_project(project, "--yes")[0], 0)
        before, times = snapshot(project), mtimes(project)
        code, out, _ = self.new_project(project, "--yes")
        self.assertEqual(code, 0)
        self.assertIn("Nothing changed", out)
        self.assertEqual(snapshot(project), before)
        self.assertEqual(mtimes(project), times)

    def test_second_run_after_a_commit_leaves_the_working_tree_clean(self):
        project = self.copy_fixture()
        self.assertEqual(self.new_project(project, "--yes")[0], 0)
        git = ["git", "-c", "user.name=T", "-c", "user.email=t@example.com", "-C", str(project)]
        subprocess.run([*git, "add", "-A"], check=True, env=self.env())
        subprocess.run([*git, "commit", "-qm", "both tools"], check=True, env=self.env())
        self.assertEqual(self.new_project(project, "--yes")[0], 0)
        status = subprocess.run([*git, "status", "--porcelain"], capture_output=True, text=True, env=self.env()).stdout
        self.assertEqual(status, "")


class Safety(BootstrapCase):
    def test_a_clash_with_a_file_aidev_po_did_not_write_stops_everything(self):
        project = self.tmp / "clash"
        rule = project / ".cursor" / "rules" / "aidev-po-bootstrap.mdc"
        rule.parent.mkdir(parents=True)
        rule.write_text("someone else's file\n")
        code, _, err = self.new_project(project, "--yes")
        self.assertNotEqual(code, 0)
        self.assertIn("Refusing to overwrite", err)
        self.assertIn("aidev-po-bootstrap.mdc", err)
        self.assertEqual(rule.read_text(), "someone else's file\n")
        self.assertEqual(sorted(p.relative_to(project).as_posix() for p in project.rglob("*") if p.is_file()),
                         [".cursor/rules/aidev-po-bootstrap.mdc"])

    def test_a_clash_with_an_agent_in_the_project_stops_everything(self):
        project = self.tmp / "clash"
        agent = project / ".cursor" / "agents" / "po.md"
        agent.parent.mkdir(parents=True)
        agent.write_text("my own po\n")
        self.assertNotEqual(self.new_project(project, "--yes")[0], 0)
        self.assertEqual(agent.read_text(), "my own po\n")
        self.assertFalse((project / ".aidev-po").exists())

    def test_an_edited_aidev_po_file_is_not_overwritten_on_a_rerun(self):
        project = self.tmp / "p"
        self.assertEqual(self.new_project(project)[0], 0)
        rule = project / ".cursor" / "rules" / "aidev-po-bootstrap.mdc"
        rule.write_text(rule.read_text() + "\nMy own addition.\n")
        edited = rule.read_bytes()
        code, _, err = self.new_project(project, "--yes")
        self.assertNotEqual(code, 0)
        self.assertIn("detected local edits", err)
        self.assertIn("own files", err)
        self.assertIn("halted rather than overwrite", err)
        self.assertIn("nothing was written", err)
        self.assertIn(".cursor/rules/aidev-po-bootstrap.mdc", err)
        self.assertEqual(rule.read_bytes(), edited)

    def test_an_unedited_older_aidev_po_file_is_updated_and_a_retired_one_removed(self):
        project = self.tmp / "p"
        self.assertEqual(self.new_project(project)[0], 0)
        manifest_path = project / ".aidev-po" / "install.json"
        manifest = json.loads(manifest_path.read_text())
        old = project / ".aidev-po" / "templates" / "01-idea.md"
        old.write_text("older version\n")
        manifest["files"][".aidev-po/templates/01-idea.md"] = hashlib.sha256(old.read_bytes()).hexdigest()
        retired = project / ".aidev-po" / "templates" / "retired.md"
        retired.write_text("retired\n")
        manifest["files"][".aidev-po/templates/retired.md"] = hashlib.sha256(retired.read_bytes()).hexdigest()
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
        before = snapshot(project)
        code, out, err = self.new_project(project, "--yes")
        self.assertEqual(code, 0, err)
        self.assertEqual(old.read_bytes(), (ROOT / "templates" / "01-idea.md").read_bytes())
        self.assertFalse(retired.exists())
        self.assertIn("Removed 1 files", out)
        after = snapshot(project)
        self.assertEqual({k for k in before if before[k] != after.get(k)},
                         {".aidev-po/templates/01-idea.md", ".aidev-po/templates/retired.md", ".aidev-po/install.json"})

    def test_overlay_is_a_no_op_by_default_and_additive_when_given(self):
        overlay = self.tmp / "overlay"
        (overlay / "docs").mkdir(parents=True)
        (overlay / "docs" / "team-notes.md").write_text("extra\n")
        plain = self.tmp / "plain"
        self.assertEqual(self.new_project(plain)[0], 0)
        self.assertFalse((plain / "docs").exists())
        with_overlay = self.tmp / "with"
        self.assertEqual(self.new_project(with_overlay, "--overlay", overlay)[0], 0)
        self.assertEqual((with_overlay / "docs" / "team-notes.md").read_text(), "extra\n")
        manifest = self.assert_registered(with_overlay)
        self.assertIn("docs/team-notes.md", manifest["files"])
        self.assertEqual(self.new_project(with_overlay, "--yes", "--overlay", overlay)[0], 0)
        (with_overlay / "docs" / "team-notes.md").write_text("mine\n")
        code, _, err = self.new_project(with_overlay, "--yes", "--overlay", overlay)
        self.assertNotEqual(code, 0)
        self.assertEqual((with_overlay / "docs" / "team-notes.md").read_text(), "mine\n")

    def test_overlay_cannot_replace_an_aidev_po_file(self):
        overlay = self.tmp / "overlay"
        (overlay / ".cursor" / "agents").mkdir(parents=True)
        (overlay / ".cursor" / "agents" / "po.md").write_text("replacement\n")
        code, _, err = self.new_project(self.tmp / "p", "--overlay", overlay)
        self.assertNotEqual(code, 0)
        self.assertIn("would replace", err)

    def test_products_repo_stays_separate_from_the_project(self):
        project = self.tmp / "project"
        self.assertEqual(self.new_project(project)[0], 0)
        script = project / ".aidev-po" / "scripts" / "products-dir.py"
        for bad in (project, project / "products", "."):
            out = subprocess.run([sys.executable, script, "--set", str(bad)], capture_output=True, text=True,
                                 cwd=project, env=self.env())
            self.assertNotEqual(out.returncode, 0, bad)
            self.assertIn("inside the aidev-po checkout or project", out.stderr)
        self.assertFalse((project / ".aidev-po" / "aidev-po.local.json").exists())
        products = self.tmp / "aidev-products"
        out = subprocess.run([sys.executable, script, "--set", str(products)], capture_output=True, text=True,
                             cwd=project, env=self.env())
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(json.loads((project / ".aidev-po" / "aidev-po.local.json").read_text())["products_dir"], str(products))
        report = subprocess.run([sys.executable, script], capture_output=True, text=True, cwd=project, env=self.env()).stdout
        self.assertIn(f"{self.tmp}/aidev-products", report, "../aidev-products is next to the project")
        ignored = subprocess.run(["git", "-C", project, "check-ignore", ".aidev-po/aidev-po.local.json"],
                                 capture_output=True, text=True, env=self.env())
        self.assertEqual(ignored.returncode, 0 if (project / ".git").exists() else 1)

    def test_no_git_init_on_a_new_folder_and_both_flags_refused(self):
        target = self.tmp / "fresh"
        code, out, err = self.new_project(target, "--no-git-init")
        self.assertEqual(code, 0, err)
        self.assertFalse((target / ".git").exists())
        self.assert_registered(target)
        self.assertIn("without a Git repository", out)
        code, _, err = self.new_project(self.tmp / "both", "--git-init", "--no-git-init")
        self.assertNotEqual(code, 0)
        self.assertIn("only one", err)
        self.assertFalse((self.tmp / "both").exists())
        via_env = self.tmp / "via-env"
        code, out, err = self.run_cmd(NEW_PROJECT, via_env, AIDEV_PO_BOOTSTRAP_GIT_INIT="0")
        self.assertEqual(code, 0, err)
        self.assertFalse((via_env / ".git").exists())
        self.assertIn("without a Git repository", out)
        code, _, err = self.run_cmd(NEW_PROJECT, "--git-init", self.tmp / "clash-env", AIDEV_PO_BOOTSTRAP_GIT_INIT="0")
        self.assertNotEqual(code, 0)
        self.assertIn("conflicts with --git-init", err)
        self.assertFalse((self.tmp / "clash-env").exists())

    def test_bootstrap_names_each_local_edit_and_writes_nothing(self):
        target = self.tmp / "edited"
        self.assertEqual(self.new_project(target)[0], 0)
        rule = target / ".cursor" / "rules" / "aidev-po-bootstrap.mdc"
        agent = target / ".cursor" / "agents" / "po.md"
        rule.write_text(rule.read_text() + "\nLocal rule note.\n")
        agent.write_text(agent.read_text() + "\nLocal agent note.\n")
        after_edit = snapshot(target)
        code, _, err = self.run_cmd(BOOTSTRAP, "--yes", str(target))
        self.assertNotEqual(code, 0)
        self.assertIn("detected local edits", err)
        self.assertIn("own files", err)
        self.assertIn("halted rather than overwrite", err)
        self.assertIn("nothing was written", err)
        self.assertIn(".cursor/rules/aidev-po-bootstrap.mdc", err)
        self.assertIn(".cursor/agents/po.md", err)
        self.assertEqual(snapshot(target), after_edit)

    def test_installed_copy_contains_the_texts_and_their_licences(self):
        target = self.tmp / "standalone"
        self.assertEqual(self.new_project(target)[0], 0)
        for rel in (
            ".aidev-po/LICENSE",
            ".aidev-po/LICENSE-CONTENT",
            ".aidev-po/NOTICE.md",
            ".aidev-po/templates/LICENSE",
            ".aidev-po/examples/tool-library-loans/01-idea.md",
            ".aidev-po/docs/products-repo.md",
        ):
            path = target / rel
            self.assertTrue(path.is_file(), rel)
            self.assertFalse(path.is_symlink(), rel)
        self.assertEqual((target / ".aidev-po/examples/tool-library-loans/01-idea.md").read_bytes(),
                         (ROOT / "examples/tool-library-loans/01-idea.md").read_bytes())
        notice = (target / ".aidev-po/NOTICE.md").read_text()
        self.assertIn("GPL-3.0", notice)
        self.assertIn("CC BY-SA 4.0", notice)
        self.assertIn("MIT", notice)
        self.assertNotIn("github.com/mitulamin/aidev-po", (target / ".aidev-po/docs/products-repo.md").read_text())
        retro = (target / ".cursor/skills/po-retro/SKILL.md").read_text()
        self.assertIn(".aidev-po/examples/", retro)
        self.assertNotIn("worktree", retro)
        self.assertNotIn("aidev-po checkout", retro)
        tracer = (target / ".cursor/agents/tracer.md").read_text()
        self.assertNotIn("git show", tracer)
        self.assertIn(".cursor/skills/", tracer)
        po = (target / ".cursor/agents/po.md").read_text()
        self.assertIn(".cursor/skills/learning-loop/SKILL.md", po)
        self.assertNotIn("`aidev-po` checkout", po)
        loop = (target / ".cursor/skills/learning-loop/SKILL.md").read_text()
        self.assertIn(".cursor/skills/po-retro/SKILL.md", loop)
        # install.json records the source commit for version stamps. products-dir.py credits
        # aidev-po in the products-repo README it writes. Schema $id values are identifiers.
        # The worked example is copied as it stands, including one historical pull-request URL
        # in its ledger. None of these is fetched to read an agent, skill, rule, template or script.
        allowed = {".aidev-po/install.json", ".aidev-po/scripts/products-dir.py"}
        for path in target.rglob("*"):
            self.assertFalse(path.is_symlink(), path)
            if not path.is_file():
                continue
            rel = path.relative_to(target).as_posix()
            if rel in allowed or rel.startswith((".aidev-po/schemas/", ".aidev-po/examples/")):
                continue
            if rel.startswith((".cursor/", ".aidev-po/")):
                self.assertNotIn(b"github.com/mitulamin/aidev-po", path.read_bytes(), rel)

    def test_installed_scripts_run_from_the_project(self):
        project = self.tmp / "project"
        self.assertEqual(self.new_project(project)[0], 0)
        out = subprocess.run([sys.executable, project / ".aidev-po" / "scripts" / "traces.py", "versions",
                              "--skills", "po-idea", "--templates", "01-idea.md"],
                             capture_output=True, text=True, cwd=project, env=self.env())
        self.assertEqual(out.returncode, 0, out.stderr)
        versions = json.loads(out.stdout)
        self.assertEqual(versions["skill_versions"]["po-idea"], versions["aidev_po"])
        out = subprocess.run([sys.executable, project / ".aidev-po" / "scripts" / "register.py", "selftest"],
                             capture_output=True, text=True, cwd=project, env=self.env())
        self.assertEqual(out.returncode, 0, out.stderr)


class Wizard(BootstrapCase):
    def test_folder_argument_skips_the_questions(self):
        target = self.tmp / "via-arg"
        code, out, err = self.run_cmd(BOOTSTRAP, target)
        self.assertEqual(code, 0, err)
        self.assertIn("aidev-po is ready in", out)
        self.assertIn("/po-start", out)
        self.assert_registered(target)
        code, _, err = self.run_cmd(BOOTSTRAP, target, stdin="y\n")
        self.assertNotEqual(code, 0)
        self.assertIn("There are files in", err)
        self.assertIn("--yes", err)
        code, out, err = self.run_cmd(BOOTSTRAP, "--yes", target)
        self.assertEqual(code, 0, err)
        self.assertIn("Nothing changed", out)

    def test_environment_variables_skip_the_questions(self):
        place = self.tmp / "place"
        place.mkdir()
        code, out, err = self.run_cmd(BOOTSTRAP, AIDEV_PO_BOOTSTRAP_LOCATION=str(place), AIDEV_PO_BOOTSTRAP_NAME="made-here")
        self.assertEqual(code, 0, err)
        self.assert_registered(place / "made-here")
        self.assertTrue((place / "made-here" / ".git").exists())

    def test_environment_variables_add_on_to_an_existing_project(self):
        project = self.copy_fixture("existing")
        before = snapshot(project)
        code, _, err = self.run_cmd(BOOTSTRAP, AIDEV_PO_BOOTSTRAP_LOCATION=str(self.tmp), AIDEV_PO_BOOTSTRAP_NAME="existing", stdin="y\n")
        self.assertNotEqual(code, 0)
        self.assertIn("There are files in", err)
        self.assertEqual(snapshot(project), before)
        code, out, err = self.run_cmd(BOOTSTRAP, AIDEV_PO_BOOTSTRAP_LOCATION=str(self.tmp), AIDEV_PO_BOOTSTRAP_NAME="existing", AIDEV_PO_BOOTSTRAP_YES="1")
        self.assertEqual(code, 0, err)
        self.assertIn("Found ai-sdlc-loop", out)
        self.assert_untouched(before, project)
        self.assert_registered(project)

    def test_interactive_answers(self):
        code, out, err = self.run_cmd(BOOTSTRAP, stdin="1\nanswered\n", HOME=str(self.home))
        self.assertEqual(code, 0, err)
        self.assertIn("Where is the project, or where would you like it to be put?", out)
        self.assert_registered(self.home / "answered")
        self.assertTrue((self.home / "answered" / ".git").exists())

    def test_piped_add_on_does_not_ask_and_changes_nothing(self):
        project = self.copy_fixture("existing")
        before = snapshot(project)
        code, out, err = self.run_cmd(BOOTSTRAP, stdin="1\nexisting\ny\n", HOME=str(self.tmp))
        self.assertNotEqual(code, 0)
        self.assertNotIn("Are you sure you want me to work", out + err)
        self.assertIn("There are files in", err)
        self.assertIn("--yes", err)
        self.assertEqual(snapshot(project), before)

    def test_tty_add_on_asks_and_honours_the_answer(self):
        project = self.copy_fixture("existing")
        before = snapshot(project)
        code, out, _ = self.run_tty(BOOTSTRAP, stdin="1\nexisting\nn\n", HOME=str(self.tmp))
        self.assertEqual(code, 0, out)
        self.assertIn("There are files in", out)
        self.assertIn("Are you sure you want me to work in this folder? [y/N]", out)
        self.assertIn("Stopped without changing anything", out)
        self.assertEqual(snapshot(project), before)
        code, out, _ = self.run_tty(BOOTSTRAP, stdin="1\nexisting\ny\n", HOME=str(self.tmp))
        self.assertEqual(code, 0, out)
        self.assert_registered(project)

    def test_tty_can_decline_git_init(self):
        code, out, _ = self.run_tty(BOOTSTRAP, stdin="1\nnogit\nn\n", HOME=str(self.home))
        self.assertEqual(code, 0, out)
        self.assertIn("This folder isn't a Git repository. Initialise one? [Y/n]", out)
        project = self.home / "nogit"
        self.assert_registered(project)
        self.assertFalse((project / ".git").exists())
        self.assertIn("without a Git repository", out)

    def test_no_answers_stops_without_changing_anything(self):
        code, _, err = self.run_cmd(BOOTSTRAP, stdin="")
        self.assertNotEqual(code, 0)
        self.assertIn("did not get an answer", err)

    def test_location_inside_the_checkout_is_refused(self):
        code, _, err = self.run_cmd(BOOTSTRAP, AIDEV_PO_BOOTSTRAP_LOCATION=str(ROOT), AIDEV_PO_BOOTSTRAP_NAME="x")
        self.assertNotEqual(code, 0)
        self.assertIn("inside the aidev-po folder", err)
        self.assertFalse((ROOT / "x").exists())

    def test_help(self):
        code, out, _ = self.run_cmd(BOOTSTRAP, "--help")
        self.assertEqual(code, 0)
        self.assertIn("AIDEV_PO_BOOTSTRAP_LOCATION", out)
        self.assertIn("--yes", out)
        self.assertIn("--git-init", out)
        self.assertIn("--no-git-init", out)
        self.assertIn("ai-sdlc-loop", out)


@unittest.skipUnless(SDLC_DIR and (Path(SDLC_DIR) / "scripts" / "bootstrap.sh").is_file(),
                     "set AI_SDLC_LOOP_DIR to a checkout of ai-sdlc-loop to run the real ai-sdlc-loop tests")
class RealAiSdlcLoop(BootstrapCase):
    def sdlc_bootstrap(self, name):
        out = subprocess.run(["bash", str(Path(SDLC_DIR) / "scripts" / "bootstrap.sh")], capture_output=True, text=True,
                             stdin=subprocess.DEVNULL, cwd=SDLC_DIR,
                             env=self.env(AI_SDLC_BOOTSTRAP_LOCATION=str(self.tmp), AI_SDLC_BOOTSTRAP_NAME=name))
        self.assertEqual(out.returncode, 0, out.stderr)
        return self.tmp / name

    def test_real_ai_sdlc_loop_then_aidev_po_leaves_every_sdlc_file_identical(self):
        project = self.sdlc_bootstrap("sdlc-first")
        before = snapshot(project)
        self.assertIn(".cursor/rules/ai-sdlc-bootstrap.mdc", before)
        code, out, err = self.new_project(project, "--yes")
        self.assertEqual(code, 0, err)
        self.assertIn("Found ai-sdlc-loop already registered here", out)
        self.assert_untouched(before, project)
        self.assert_registered(project)
        mid, times = snapshot(project), mtimes(project)
        self.assertEqual(self.new_project(project, "--yes")[0], 0)
        self.assertEqual(snapshot(project), mid)
        self.assertEqual(mtimes(project), times)

    def test_real_ai_sdlc_loop_file_names_do_not_overlap_aidev_po(self):
        project = self.sdlc_bootstrap("sdlc-names")
        sdlc_files = set(snapshot(project))
        target = self.tmp / "po-only"
        self.assertEqual(self.new_project(target)[0], 0)
        po_files = set(snapshot(target))
        self.assertEqual(sdlc_files & po_files, set())


if __name__ == "__main__":
    unittest.main()
