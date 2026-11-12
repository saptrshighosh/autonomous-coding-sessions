import importlib.util
import os
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALL = ROOT / "install.sh"
SKILLS = ["autonomous-coding-sessions", "autonomy-audit", "reversibility-check", "verification-plan"]


def load_package_module():
    spec = importlib.util.spec_from_file_location("package_skill", ROOT / "scripts/package_skill.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_install(*args, **env):
    merged = {**os.environ, **env}
    return subprocess.run(["bash", str(INSTALL), *args], capture_output=True, text=True, env=merged)


class Installer(unittest.TestCase):
    def test_installs_all_skills_to_dest(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run_install("--dest", tmp)
            self.assertEqual(result.returncode, 0, result.stderr)
            for skill in SKILLS:
                self.assertTrue((Path(tmp) / skill / "SKILL.md").is_file(), skill)

    def test_list_changes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run_install("--dest", tmp, "--list")
            self.assertEqual(result.returncode, 0)
            self.assertEqual(list(Path(tmp).iterdir()), [])
            self.assertIn("would copy", result.stdout)

    def test_uninstall_removes_only_its_own_skills(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_install("--dest", tmp)
            other = Path(tmp) / "someone-elses-skill"
            other.mkdir()
            (other / "SKILL.md").write_text("keep me")
            run_install("--dest", tmp, "--uninstall")
            self.assertTrue(other.is_dir())
            for skill in SKILLS:
                self.assertFalse((Path(tmp) / skill).exists(), skill)

    def test_reinstall_replaces_stale_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_install("--dest", tmp)
            stale = Path(tmp) / "autonomy-audit" / "stale.txt"
            stale.write_text("old")
            run_install("--dest", tmp)
            self.assertFalse(stale.exists())

    def test_unknown_option_exits_2(self):
        self.assertEqual(run_install("--bogus").returncode, 2)

    def test_installer_never_touches_settings(self):
        with tempfile.TemporaryDirectory() as home:
            settings = Path(home) / "settings.json"
            settings.write_text("{}")
            run_install(CLAUDE_CONFIG_DIR=home)
            self.assertEqual(settings.read_text(), "{}")
            self.assertTrue((Path(home) / "skills" / "autonomy-audit" / "SKILL.md").is_file())


class Package(unittest.TestCase):
    def test_build_is_reproducible(self):
        module = load_package_module()
        skill_dir = ROOT / "skills" / "autonomous-coding-sessions"
        self.assertEqual(module.build_bytes(skill_dir), module.build_bytes(skill_dir))

    def test_archive_layout(self):
        module = load_package_module()
        data = module.build_bytes(ROOT / "skills" / "autonomous-coding-sessions")
        with tempfile.NamedTemporaryFile(suffix=".skill") as handle:
            handle.write(data)
            handle.flush()
            with zipfile.ZipFile(handle.name) as archive:
                names = archive.namelist()
        self.assertIn("autonomous-coding-sessions/SKILL.md", names)
        self.assertTrue(all(n.startswith("autonomous-coding-sessions/") for n in names))
        self.assertEqual(names, sorted(names))

    def test_committed_archive_matches_a_fresh_build(self):
        module = load_package_module()
        committed = ROOT / "dist" / "autonomous-coding-sessions.skill"
        self.assertTrue(committed.is_file(), "run: make package")
        self.assertEqual(committed.read_bytes(), module.build_bytes(ROOT / "skills" / "autonomous-coding-sessions"))


if __name__ == "__main__":
    unittest.main()
