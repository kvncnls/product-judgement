#!/usr/bin/env python3
"""Confirm a release tag matches the version every plugin manifest advertises.

Without this, a tagged install can resolve to a differently numbered plugin.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MANIFESTS = {
    ".claude-plugin/plugin.json": lambda data: data.get("version"),
    ".claude-plugin/marketplace.json": lambda data: data["plugins"][0].get("version"),
    ".cursor-plugin/plugin.json": lambda data: data.get("version"),
    ".codex-plugin/plugin.json": lambda data: data.get("version"),
}


def main(argv: list[str]) -> int:
    if not argv or not argv[0].strip():
        print("Usage: python3 scripts/check_version.py <version>", file=sys.stderr)
        return 2

    expected = argv[0].strip()
    errors = []
    for path, reader in MANIFESTS.items():
        data = json.loads((ROOT / path).read_text(encoding="utf-8"))
        found = reader(data)
        if found != expected:
            errors.append(f"{path}: version {json.dumps(found)}, expected {json.dumps(expected)}")

    if errors:
        print("Version mismatch:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"All plugin manifests report version {expected}.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
