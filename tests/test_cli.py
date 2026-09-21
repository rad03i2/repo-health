import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from repo_health.cli import main


class CliTests(unittest.TestCase):
    def test_json_output_and_fail_policy(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# X", encoding="utf-8")
            out = StringIO()
            with redirect_stdout(out):
                code = main([tmp, "--json", "--fail-on", "warning"])
            payload = json.loads(out.getvalue())
            self.assertEqual(code, 1)
            self.assertIn("score", payload)
            self.assertGreaterEqual(payload["warnings"], 1)

    def test_min_score_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = StringIO()
            with redirect_stdout(out):
                code = main([tmp, "--min-score", "100", "--fail-on", "never"])
            self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
