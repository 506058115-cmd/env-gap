#!/usr/bin/env python3
"""Compare dotenv variable names without displaying their values."""

import argparse
import re
import sys
from pathlib import Path


KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*=")


def read_keys(path):
    keys = set()
    problems = []
    with path.open(encoding="utf-8-sig") as source:
        for number, line in enumerate(source, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if stripped.startswith("export "):
                stripped = stripped[7:].lstrip()
            match = KEY_RE.match(stripped)
            if not match:
                problems.append(f"{path}:{number}: expected NAME=value assignment")
                continue
            name = match.group(1)
            if name in keys:
                problems.append(f"{path}:{number}: duplicate key {name}")
            keys.add(name)
    return keys, problems


def main():
    parser = argparse.ArgumentParser(
        description="Compare .env variable names; values are never printed."
    )
    parser.add_argument("reference", type=Path, help="example/template dotenv file")
    parser.add_argument("actual", type=Path, help="local dotenv file")
    args = parser.parse_args()

    try:
        expected, problems = read_keys(args.reference)
        actual, actual_problems = read_keys(args.actual)
        problems.extend(actual_problems)
    except (OSError, UnicodeError) as error:
        print(f"env-gap: {error}", file=sys.stderr)
        return 2

    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    shared = expected & actual
    print(f"Shared keys: {len(shared)}")
    print("Missing from actual: " + (", ".join(missing) or "none"))
    print("Only in actual: " + (", ".join(extra) or "none"))
    for problem in problems:
        print(problem, file=sys.stderr)
    if problems:
        return 2
    return 1 if missing or extra else 0


if __name__ == "__main__":
    raise SystemExit(main())
