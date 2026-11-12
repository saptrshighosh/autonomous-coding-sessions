import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOKS = ROOT / "skills/verification-plan/scripts/hooks"


def run_hook(name, stdin="{}", **env):
    merged = {k: v for k, v in os.environ.items() if not k.startswith("ACS_")}
    merged.update(env)
    return subprocess.run(
        ["bash", str(HOOKS / name)], input=stdin, capture_output=True, text=True, env=merged, timeout=30
    )


class LintOnEdit(unittest.TestCase):
    def payload(self, path="src/app.py"):
        return json.dumps({"tool_name": "Edit", "tool_input": {"file_path": path}})

    def test_unset_command_does_nothing(self):
        self.assertEqual(run_hook("lint-on-edit.sh", self.payload()).returncode, 0)

    def test_passing_linter_exits_0(self):
        self.assertEqual(run_hook("lint-on-edit.sh", self.payload(), ACS_LINT_CMD="true").returncode, 0)

    def test_failing_linter_exits_2_not_1(self):
        result = run_hook("lint-on-edit.sh", self.payload(), ACS_LINT_CMD="false")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Lint failed", result.stderr)

    def test_file_path_is_passed_to_the_linter(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "seen.txt"
            cmd = f'sh -c \'echo "$0" > {out}\''
            run_hook("lint-on-edit.sh", self.payload("some/file.py"), ACS_LINT_CMD=cmd)
            self.assertEqual(out.read_text().strip(), "some/file.py")

    def test_missing_file_path_does_nothing(self):
        result = run_hook("lint-on-edit.sh", "{}", ACS_LINT_CMD="false")
        self.assertEqual(result.returncode, 0)

    def test_garbage_stdin_does_not_crash(self):
        self.assertEqual(run_hook("lint-on-edit.sh", "not json", ACS_LINT_CMD="false").returncode, 0)


class TestsOnTaskComplete(unittest.TestCase):
    def test_unset_command_does_nothing(self):
        self.assertEqual(run_hook("tests-on-task-complete.sh").returncode, 0)

    def test_pass(self):
        self.assertEqual(run_hook("tests-on-task-complete.sh", ACS_TASK_TEST_CMD="true").returncode, 0)

    def test_fail_exits_2_with_output(self):
        result = run_hook(
            "tests-on-task-complete.sh", ACS_TASK_TEST_CMD="echo boom; exit 1"
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("boom", result.stderr)


class FullSuiteOnStop(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def stop(self, command, session="s1", **extra):
        return run_hook(
            "full-suite-on-stop.sh",
            json.dumps({"session_id": session}),
            ACS_TEST_CMD=command,
            TMPDIR=self.tmp.name,
            **extra,
        )

    def test_unset_command_does_nothing(self):
        self.assertEqual(run_hook("full-suite-on-stop.sh", TMPDIR=self.tmp.name).returncode, 0)

    def test_pass_exits_0(self):
        self.assertEqual(self.stop("true").returncode, 0)

    def test_fail_blocks_with_exit_2(self):
        result = self.stop("echo broken; exit 1")
        self.assertEqual(result.returncode, 2)
        self.assertIn("attempt 1 of 5", result.stderr)

    def test_gives_up_after_max_blocks(self):
        codes = [self.stop("false", ACS_MAX_BLOCKS="2").returncode for _ in range(4)]
        self.assertEqual(codes, [2, 2, 0, 2])  # third call exceeds the cap and lets the session end

    def test_success_resets_counter(self):
        self.stop("false")
        self.stop("true")
        self.assertIn("attempt 1 of 5", self.stop("false").stderr)

    def test_sessions_are_counted_separately(self):
        self.stop("false", session="a", ACS_MAX_BLOCKS="1")
        self.assertEqual(self.stop("false", session="b", ACS_MAX_BLOCKS="1").returncode, 2)

    def test_hostile_session_id_stays_inside_tmpdir(self):
        self.stop("false", session="../../escape")
        self.assertEqual([p for p in Path(self.tmp.name).iterdir() if p.name.startswith("acs-stop-")][0].parent,
                         Path(self.tmp.name))
        self.assertFalse((Path(self.tmp.name).parent / "escape.count").exists())


class ExampleScriptsMatch(unittest.TestCase):
    def test_example_project_copies_are_identical(self):
        example = ROOT / "examples/hardened-project/.claude/hooks"
        for source in HOOKS.glob("*.sh"):
            self.assertEqual((example / source.name).read_bytes(), source.read_bytes(), source.name)


if __name__ == "__main__":
    unittest.main()
