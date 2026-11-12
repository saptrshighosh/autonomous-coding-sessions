import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class VerifyRepo(unittest.TestCase):
    def test_repo_passes_its_own_verification(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "tests/verify_repo.py")], capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
