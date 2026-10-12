"""Behavioral checks for data preservation and installation portability."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


init = module("init_brain", ROOT / "skills/my-exobrain/scripts/init_brain.py")
installer = module("installer", ROOT / "scripts/install.py")


class ScriptTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name).resolve()

    def tearDown(self):
        self.temp.cleanup()

    def test_four_modes_are_blank_and_select_only_requested_modules(self):
        for mode in init.MODES:
            with self.subTest(mode=mode):
                root, paths = init.initialize(self.base / mode, mode)
                state = json.loads((root / "brain.json").read_text())
                self.assertEqual(state["memory_permission"], "not_set")
                self.assertEqual(state["personalization"], "empty")
                self.assertEqual((root / "10_生活").exists(), mode in ("life", "both"))
                self.assertEqual((root / "20_工作").exists(), mode in ("work", "both"))
                self.assertFalse((root / ".git").exists())
                self.assertEqual(len(paths), len(list(p for p in root.rglob("*") if p.is_file())))

    def test_existing_records_are_never_overwritten(self):
        target = self.base / "existing"
        target.mkdir()
        record = target / "my-record.md"
        record.write_text("original record", encoding="utf-8")
        with self.assertRaises(ValueError):
            init.initialize(target, "both")
        self.assertEqual(record.read_text(), "original record")
        self.assertEqual(list(target.iterdir()), [record])

    def test_second_init_refuses_without_changing_files(self):
        target, _ = init.initialize(self.base / "brain", "life")
        before = installer.inventory(target)
        with self.assertRaises(ValueError):
            init.initialize(target, "work")
        self.assertEqual(installer.inventory(target), before)

    def test_preview_creates_nothing(self):
        target = self.base / "preview"
        _, paths = init.initialize(target, "work", True)
        self.assertTrue(paths)
        self.assertFalse(target.exists())
        installer.install(self.base / "skill-preview", True)
        self.assertFalse((self.base / "skill-preview").exists())

    def test_git_directory_and_worktree_file_are_blocked(self):
        for kind in ("directory", "file"):
            repo = self.base / kind
            repo.mkdir()
            if kind == "directory":
                (repo / ".git").mkdir()
            else:
                (repo / ".git").write_text("gitdir: elsewhere")
            with self.assertRaises(ValueError):
                init.initialize(repo / "brain", "auto")
            self.assertFalse((repo / "brain").exists())

    def test_symlink_parent_is_refused(self):
        real = self.base / "real"
        real.mkdir()
        alias = self.base / "alias"
        try:
            alias.symlink_to(real, target_is_directory=True)
        except OSError:
            self.skipTest("Symlinks unavailable")
        with self.assertRaises(ValueError):
            init.initialize(alias / "brain")
        self.assertFalse((real / "brain").exists())

    def test_self_contained_install_can_initialize(self):
        target = self.base / "installed/my-exobrain"
        self.assertEqual(installer.install(target)[0], "installed")
        self.assertEqual(installer.inventory(target), installer.inventory(installer.SOURCE))
        result = subprocess.run([sys.executable, str(target / "scripts/init_brain.py"),
                                 str(self.base / "my new 外脑"), "--mode", "both"],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.base / "my new 外脑/AGENTS.md").exists())
        self.assertEqual(installer.install(target)[0], "already-installed")

    def test_install_does_not_replace_an_existing_skill(self):
        target = self.base / "installed"
        target.mkdir()
        (target / "custom.md").write_text("keep me")
        with self.assertRaises(ValueError):
            installer.install(target)
        self.assertEqual((target / "custom.md").read_text(), "keep me")

    def test_runtime_gitignore_keeps_personal_records_out_of_default_add(self):
        root, _ = init.initialize(self.base / "private", "both")
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        subprocess.run(["git", "-C", str(root), "add", "--all"], check=True)
        tracked = subprocess.check_output(["git", "-C", str(root), "ls-files"], text=True).splitlines()
        self.assertEqual(tracked, [".gitignore"])


if __name__ == "__main__":
    unittest.main()
