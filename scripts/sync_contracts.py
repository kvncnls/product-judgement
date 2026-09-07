#!/usr/bin/env python3
"""Synchronize canonical shared contract fragments into installed Skills."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
LOCAL_SKILLS = ["focal", "compass", "flywheel", "soul"]
FRAGMENTS = ["anchors", "severity", "evidence"]


def main(argv: list[str]) -> int:
    if any(argument != "--check" for argument in argv):
        print("Usage: uv run scripts/sync_contracts.py [--check]", file=sys.stderr)
        return 1
    check = "--check" in argv

    changes: dict[str, str] = {}
    errors: list[str] = []

    targets: list[tuple[str, list[str]]] = [
        (f"{skill}/reference/review.md", FRAGMENTS) for skill in LOCAL_SKILLS
    ]
    targets.append(("product-judgement/SKILL.md", ["evidence"]))

    for relative_path, fragments in targets:
        path = ROOT / relative_path
        content = path.read_bytes().decode("utf-8")
        original = content
        for name in fragments:
            start = f"<!-- BEGIN SHARED: {name} -->"
            finish = f"<!-- END SHARED: {name} -->"
            pattern = re.compile(re.escape(start) + r"\n.*?\n" + re.escape(finish), re.DOTALL)
            matches = pattern.findall(content)
            if len(matches) != 1:
                errors.append(f"{relative_path}: expected exactly one {name} fragment, found {len(matches)}")
                continue
            canonical = (ROOT / "contracts" / f"{name}.md").read_bytes().decode("utf-8").strip()
            content = pattern.sub(
                lambda _match: f"{start}\n{canonical}\n{finish}",
                content,
                count=1,
            )
        if content != original:
            changes[relative_path] = content

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    if check:
        if changes:
            changed = ", ".join(changes)
            print(
                f"Shared contracts are stale: {changed}. Run uv run scripts/sync_contracts.py",
                file=sys.stderr,
            )
            return 1
        print("Shared evidence, score anchors, and severity contracts are current.")
        return 0

    for relative_path, content in changes.items():
        (ROOT / relative_path).write_bytes(content.encode("utf-8"))
    print(f"Synchronized {len(changes)} Skill file(s) from contracts/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
