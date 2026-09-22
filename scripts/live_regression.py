#!/usr/bin/env python3
"""Run optional live JEV regressions against local documents."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class CaseResult:
    name: str
    path: str
    probability_ai: float | None
    min_ai: float
    max_ai: float
    passed: bool
    note: str


def load_cases(path: Path) -> list[dict[str, Any]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"live cases file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid JSON in {path}: {exc}") from exc

    if not isinstance(data, list):
        raise SystemExit(f"{path} must contain a JSON list of cases")
    return data


def run_case(case: dict[str, Any], command: str) -> CaseResult:
    name = str(case.get("name") or case.get("path") or "unnamed")
    doc_path = str(case["path"])
    min_ai = float(case.get("min_ai", 0.0))
    max_ai = float(case.get("max_ai", 1.0))
    note = str(case.get("note", ""))

    result = subprocess.run(
        [command, doc_path, "--json"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or f"exit {result.returncode}"
        print(f"ERROR {name}: {message}", file=sys.stderr)
        return CaseResult(name, doc_path, None, min_ai, max_ai, False, note)

    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        print(f"ERROR {name}: non-JSON output: {exc}", file=sys.stderr)
        return CaseResult(name, doc_path, None, min_ai, max_ai, False, note)

    probability_ai = payload.get("probability_ai")
    if not isinstance(probability_ai, (int, float)):
        print(f"ERROR {name}: missing numeric probability_ai", file=sys.stderr)
        return CaseResult(name, doc_path, None, min_ai, max_ai, False, note)

    probability_ai = float(probability_ai)
    passed = min_ai <= probability_ai <= max_ai
    return CaseResult(name, doc_path, probability_ai, min_ai, max_ai, passed, note)


def print_results(results: list[CaseResult]) -> None:
    print("status  ai_prob  expected     name")
    print("------  -------  --------     ----")
    for result in results:
        status = "PASS" if result.passed else "FAIL"
        ai_prob = "n/a" if result.probability_ai is None else f"{result.probability_ai:.2%}"
        expected = f"{result.min_ai:.0%}-{result.max_ai:.0%}"
        print(f"{status:6}  {ai_prob:>7}  {expected:<11}  {result.name}")
        if result.note:
            print(f"        note: {result.note}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run optional live jevgram regressions.")
    parser.add_argument("cases", type=Path, help="JSON cases file")
    parser.add_argument("--command", default="jevgram", help="jevgram command to run")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    cases = load_cases(args.cases)
    results = [run_case(case, args.command) for case in cases]
    print_results(results)
    return 0 if all(result.passed for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
