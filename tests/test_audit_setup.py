import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/autonomy-audit/scripts/audit_setup.py"
FIXTURE = ROOT / "tests/fixtures/bloated-project"
HARDENED = ROOT / "examples/hardened-project"

spec = importlib.util.spec_from_file_location("audit_setup", SCRIPT)
audit_setup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit_setup)


def ids(findings):
    return {f["id"] for f in findings}


class BloatedProject(unittest.TestCase):
    def setUp(self):
        self.findings = audit_setup.audit(FIXTURE)

    def test_flags_shouted_emphasis(self):
        self.assertIn("CLAUDE_MD_EMPHASIS", ids(self.findings))

    def test_flags_bypass_permissions_as_high(self):
        match = [f for f in self.findings if f["id"] == "BYPASS_PERMISSIONS"]
        self.assertEqual(len(match), 1)
        self.assertEqual(match[0]["severity"], "high")

    def test_flags_missing_deny_rules(self):
        self.assertIn("NO_DENY_RULES", ids(self.findings))

    def test_flags_hook_that_exits_1_only(self):
        self.assertIn("HOOK_EXIT_1", ids(self.findings))

    def test_flags_no_ci(self):
        self.assertIn("NO_CI", ids(self.findings))

    def test_has_stop_hook_so_no_verification_gap(self):
        self.assertNotIn("NO_VERIFICATION_HOOK", ids(self.findings))

    def test_high_findings_sorted_first(self):
        self.assertEqual(self.findings[0]["severity"], "high")


class HardenedExample(unittest.TestCase):
    def test_no_high_or_medium_findings(self):
        findings = audit_setup.audit(HARDENED)
        bad = [f for f in findings if f["severity"] in ("high", "medium")]
        self.assertEqual(bad, [], bad)

    def test_hook_scripts_are_not_flagged(self):
        self.assertNotIn("HOOK_EXIT_1", ids(audit_setup.audit(HARDENED)))


class EdgeCases(unittest.TestCase):
    def test_empty_directory_reports_missing_settings_and_ci(self):
        with tempfile.TemporaryDirectory() as tmp:
            found = ids(audit_setup.audit(Path(tmp)))
        self.assertIn("NO_PROJECT_SETTINGS", found)
        self.assertIn("NO_CI", found)

    def test_invalid_json_is_high(self):
        with tempfile.TemporaryDirectory() as tmp:
            settings = Path(tmp) / ".claude"
            settings.mkdir()
            (settings / "settings.json").write_text("{not json")
            findings = audit_setup.audit(Path(tmp))
        match = [f for f in findings if f["id"] == "SETTINGS_INVALID_JSON"]
        self.assertEqual(len(match), 1)
        self.assertEqual(match[0]["severity"], "high")

    def test_env_without_gitignore_entry_is_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / ".env").write_text("EXAMPLE=value\n")
            self.assertIn("ENV_NOT_IGNORED", ids(audit_setup.audit(Path(tmp))))

    def test_env_with_gitignore_entry_is_not_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / ".env").write_text("EXAMPLE=value\n")
            (Path(tmp) / ".gitignore").write_text(".env\n")
            self.assertNotIn("ENV_NOT_IGNORED", ids(audit_setup.audit(Path(tmp))))

    def test_audit_never_modifies_the_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "CLAUDE.md").write_text("NEVER do that!\n")
            before = sorted((p.name, p.stat().st_mtime_ns) for p in root.rglob("*"))
            audit_setup.audit(root)
            after = sorted((p.name, p.stat().st_mtime_ns) for p in root.rglob("*"))
        self.assertEqual(before, after)


class CommandLine(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)

    def test_json_output_parses(self):
        result = self.run_cli(str(FIXTURE), "--json")
        self.assertEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        self.assertTrue(data["findings"])

    def test_fail_on_high_exits_1_for_bloated(self):
        self.assertEqual(self.run_cli(str(FIXTURE), "--fail-on", "high").returncode, 1)

    def test_fail_on_high_exits_0_for_hardened(self):
        self.assertEqual(self.run_cli(str(HARDENED), "--fail-on", "medium").returncode, 0)

    def test_missing_directory_exits_2(self):
        self.assertEqual(self.run_cli("/no/such/dir").returncode, 2)


if __name__ == "__main__":
    unittest.main()
