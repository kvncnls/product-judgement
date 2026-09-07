#!/usr/bin/env python3
"""Confirm a release tag matches every plugin manifest's advertised version."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent.parent

MANIFESTS: dict[str, Callable[[dict[str, Any]], Any]] = {
    ".claude-plugin/plugin.json": lambda data: data["version"],
    ".claude-plugin/marketplace.json": lambda data: data["plugins"][0]["version"],
    ".cursor-plugin/plugin.json": lambda data: data["version"],
    ".codex-plugin/plugin.json": lambda data: data["version"],
}


def ruby_inspect(value: Any) -> str:
    """Render manifest values like Ruby's String#inspect for CLI diagnostics."""

    if value is None:
        return "nil"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    return repr(value)


def main(argv: list[str]) -> int:
    # The Ruby script uses only ARGV[0], so preserve its behavior with extra
    # positional arguments rather than rejecting them.
    if not argv or not argv[0].strip():
        print("Usage: uv run scripts/check_version.py <version>", file=sys.stderr)
        return 2
    expected = argv[0].strip()

    errors: list[str] = []
    for relative_path, reader in MANIFESTS.items():
        data = json.loads((ROOT / relative_path).read_bytes().decode("utf-8"))
        found = reader(data)
        if found != expected:
            errors.append(
                f"{relative_path}: version {ruby_inspect(found)}, expected {ruby_inspect(expected)}"
            )

    if errors:
        print("Version mismatch:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"All plugin manifests report version {expected}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
