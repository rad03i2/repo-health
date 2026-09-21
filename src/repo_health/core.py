from __future__ import annotations

import json
import os
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

TEXT_LIMIT = 1_000_000
SKIP_DIRS = {".git", ".hg", ".svn", ".venv", "venv", "node_modules", "dist", "build", "__pycache__", ".tox", ".mypy_cache", ".pytest_cache"}
SECRET_PATTERNS = (
    ("private-key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b")),
    ("aws-access-key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
)

@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    message: str
    path: str | None = None

@dataclass(frozen=True)
class Report:
    root: str
    score: int
    files_scanned: int
    findings: tuple[Finding, ...]

    @property
    def errors(self) -> int:
        return sum(f.severity == "error" for f in self.findings)

    @property
    def warnings(self) -> int:
        return sum(f.severity == "warning" for f in self.findings)

    def to_dict(self) -> dict:
        data = asdict(self)
        data["errors"] = self.errors
        data["warnings"] = self.warnings
        return data


def _files(root: Path) -> Iterable[Path]:
    for current, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith(".repo-health"))
        for name in sorted(files):
            path = Path(current) / name
            try:
                if path.is_symlink() or path.stat().st_size > TEXT_LIMIT:
                    continue
            except OSError:
                continue
            yield path


def _text(path: Path) -> str | None:
    try:
        raw = path.read_bytes()
    except OSError:
        return None
    if b"\x00" in raw[:4096]:
        return None
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return None


def audit(root: str | Path) -> Report:
    root = Path(root).expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"Not a directory: {root}")
    findings: list[Finding] = []
    names = {p.name.lower(): p for p in root.iterdir() if p.is_file()}
    required = {
        "readme.md": ("error", "missing-readme", "README.md is missing."),
        "license": ("warning", "missing-license", "A LICENSE file is missing."),
        ".gitignore": ("warning", "missing-gitignore", ".gitignore is missing."),
    }
    for name, (severity, code, message) in required.items():
        if name not in names:
            findings.append(Finding(severity, code, message))

    has_ci = (root / ".github" / "workflows").is_dir()
    if not has_ci:
        findings.append(Finding("info", "no-ci", "No GitHub Actions workflow directory found."))
    if not (root / "SECURITY.md").is_file():
        findings.append(Finding("info", "no-security-policy", "SECURITY.md is not present."))
    if not (root / "CONTRIBUTING.md").is_file():
        findings.append(Finding("info", "no-contributing-guide", "CONTRIBUTING.md is not present."))

    count = 0
    for path in _files(root):
        count += 1
        rel = path.relative_to(root).as_posix()
        lower = path.name.lower()
        if lower == ".env" or lower.endswith((".pem", ".key", ".p12", ".pfx")):
            findings.append(Finding("warning", "sensitive-file", "Potentially sensitive file is present; verify it is safe to commit.", rel))
        text = _text(path)
        if text is None:
            continue
        for label, pattern in SECRET_PATTERNS:
            if pattern.search(text):
                findings.append(Finding("error", "secret-signal", f"Possible {label} detected. Rotate it if real and remove it from history.", rel))
        if path.suffix.lower() in {".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".go", ".rs"}:
            markers = len(re.findall(r"\b(?:TODO|FIXME|HACK)\b", text, flags=re.IGNORECASE))
            if markers:
                findings.append(Finding("warning", "unfinished-marker", f"Found {markers} TODO/FIXME/HACK marker(s).", rel))

    penalty = sum({"error": 20, "warning": 7, "info": 2}[f.severity] for f in findings)
    return Report(str(root), max(0, 100 - penalty), count, tuple(findings))


def render_text(report: Report) -> str:
    lines = [f"Repository health: {report.score}/100", f"Files scanned: {report.files_scanned}", f"Errors: {report.errors} | Warnings: {report.warnings}"]
    if not report.findings:
        lines.append("No findings.")
    for f in report.findings:
        location = f" ({f.path})" if f.path else ""
        lines.append(f"[{f.severity.upper()}] {f.code}{location}: {f.message}")
    return "\n".join(lines)


def render_json(report: Report) -> str:
    return json.dumps(report.to_dict(), indent=2, ensure_ascii=False)
