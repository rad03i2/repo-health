from __future__ import annotations

import argparse
import sys

from .core import audit, render_json, render_text


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="repo-health", description="Audit a local repository for practical health and hygiene signals.")
    p.add_argument("path", nargs="?", default=".", help="Repository directory (default: current directory)")
    p.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    p.add_argument("--fail-on", choices=("never", "warning", "error"), default="error", help="Exit non-zero at this severity (default: error)")
    p.add_argument("--min-score", type=int, metavar="N", help="Exit non-zero when score is below 0..100")
    p.add_argument("--version", action="version", version="repo-health 1.0.0 — Radwan Abdulhadi Ahmed / @rad03i2")
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.min_score is not None and not 0 <= args.min_score <= 100:
        parser().error("--min-score must be between 0 and 100")
    try:
        report = audit(args.path)
    except (ValueError, OSError) as exc:
        print(f"repo-health: {exc}", file=sys.stderr)
        return 2
    print(render_json(report) if args.json else render_text(report))
    failed = args.min_score is not None and report.score < args.min_score
    if args.fail_on == "error" and report.errors:
        failed = True
    elif args.fail_on == "warning" and (report.errors or report.warnings):
        failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
