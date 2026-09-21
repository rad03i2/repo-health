import tempfile
import unittest
from pathlib import Path

from repo_health.core import audit


class AuditTests(unittest.TestCase):
    def test_healthy_basics_score_cleanly(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# Project\n", encoding="utf-8")
            (root / "LICENSE").write_text("MIT\n", encoding="utf-8")
            (root / ".gitignore").write_text(".env\n", encoding="utf-8")
            (root / "SECURITY.md").write_text("# Security\n", encoding="utf-8")
            (root / "CONTRIBUTING.md").write_text("# Contributing\n", encoding="utf-8")
            (root / ".github/workflows").mkdir(parents=True)
            (root / ".github/workflows/ci.yml").write_text("name: CI\n", encoding="utf-8")
            report = audit(root)
            self.assertEqual(report.score, 100)
            self.assertEqual(report.errors, 0)
            self.assertEqual(report.warnings, 0)

    def test_missing_files_and_markers_are_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "app.py").write_text("# TODO: finish this\n", encoding="utf-8")
            report = audit(root)
            codes = {f.code for f in report.findings}
            self.assertIn("missing-readme", codes)
            self.assertIn("missing-license", codes)
            self.assertIn("unfinished-marker", codes)
            self.assertLess(report.score, 100)

    def test_secret_signal_never_exposes_value(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            token = "ghp_" + "A" * 30
            (root / "README.md").write_text("# X", encoding="utf-8")
            (root / "LICENSE").write_text("MIT", encoding="utf-8")
            (root / ".gitignore").write_text(".env", encoding="utf-8")
            (root / "bad.txt").write_text(token, encoding="utf-8")
            report = audit(root)
            finding = next(f for f in report.findings if f.code == "secret-signal")
            self.assertNotIn(token, finding.message)

    def test_invalid_path_is_rejected(self):
        with self.assertRaises(ValueError):
            audit("definitely-not-a-real-repo-health-path")


if __name__ == "__main__":
    unittest.main()
