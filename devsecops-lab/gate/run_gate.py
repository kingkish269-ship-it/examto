"""Aggregate tool reports and apply the gate. Returns a pipeline exit code.

Usage:
    python -m gate.run_gate --semgrep samples/semgrep_sample.json \
        --trivy samples/trivy_sample.json --gitleaks samples/gitleaks_sample.json \
        --fail-on HIGH
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .gate import (evaluate, normalize_gitleaks, normalize_semgrep,
                   normalize_trivy, render)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="DevSecOps policy gate")
    p.add_argument("--semgrep", type=Path)
    p.add_argument("--trivy", type=Path)
    p.add_argument("--gitleaks", type=Path)
    p.add_argument("--fail-on", default="HIGH", choices=["CRITICAL", "HIGH", "MEDIUM", "LOW"])
    p.add_argument("--max-allowed", type=int, default=0)
    p.add_argument("--allow", action="append", default=[], help="finding id to ignore")
    return p


def _load(path: Path | None):
    return json.loads(path.read_text(encoding="utf-8")) if path else None


def run(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    findings: list[dict] = []
    if args.semgrep:
        findings += normalize_semgrep(_load(args.semgrep))
    if args.trivy:
        findings += normalize_trivy(_load(args.trivy))
    if args.gitleaks:
        findings += normalize_gitleaks(_load(args.gitleaks))

    decision = evaluate(findings, fail_on=args.fail_on,
                        max_allowed=args.max_allowed, allowlist=set(args.allow))
    print(render(decision))
    return decision["exit_code"]


if __name__ == "__main__":
    raise SystemExit(run())
