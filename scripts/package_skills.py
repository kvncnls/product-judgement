#!/usr/bin/env python3
"""Build upload ZIP packages for the Product Judgement Skills.

The source frontmatter retains Claude Code extensions such as
``argument-hint``. Upload packages contain only the keys allowed by the Agent
Skills specification, while preserving the retained YAML lines byte-for-byte.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILLS = ["focal", "compass", "flywheel", "soul", "product-judgement"]

# https://agentskills.io/specification — the complete allowed set.
SPEC_KEYS = ["name", "description", "license", "compatibility", "metadata", "allowed-tools"]

_FRONTMATTER = re.compile(r"\A---\n(.*?\n)---\n", re.DOTALL)
_FRONTMATTER_KEY = re.compile(r"\A([A-Za-z0-9_-]+):")


class PackagingError(Exception):
    """An expected packaging failure with a user-facing message."""


def parser() -> argparse.ArgumentParser:
    command = "uv run scripts/package_skills.py"
    result = argparse.ArgumentParser(
        prog=command,
        usage=f"{command} [options]",
        description="Build upload packages for the Product Judgement Skills.",
    )
    result.add_argument("--out", default=str(ROOT / "dist"), metavar="DIR", help="Output directory (default: dist/)")
    result.add_argument("--skill", action="append", default=[], metavar="NAME", help="Package only this Skill; repeatable")
    result.add_argument("--no-combined", action="store_true", help="Skip the all-five package")
    result.add_argument("--check", action="store_true", help="Report what would be stripped; write nothing")
    return result


def strip_non_spec_frontmatter(text: str, path: str) -> tuple[str, list[str]]:
    """Drop unsupported frontmatter keys without serializing the YAML.

    A continuation line belongs to the key above it. A blank line resets the
    continuation state, matching the Ruby implementation's line-oriented rule.
    """

    match = _FRONTMATTER.match(text)
    if match is None:
        raise PackagingError(f"{path}: missing YAML frontmatter")

    stripped: list[str] = []
    kept_lines: list[str] = []
    dropping = False
    # Ruby's String#each_line splits only at LF. splitlines() would also split
    # a bare CR and could reinterpret a mixed-line-ending frontmatter block.
    frontmatter_lines = match.group(1).split("\n")
    for line in (part + "\n" for part in frontmatter_lines[:-1]):
        key_match = _FRONTMATTER_KEY.match(line)
        if key_match:
            key = key_match.group(1)
            dropping = key not in SPEC_KEYS
            if dropping:
                stripped.append(key)
        elif not line.strip():
            dropping = False

        if not dropping:
            kept_lines.append(line)

    if not kept_lines:
        raise PackagingError(f"{path}: every frontmatter key was stripped")

    replacement = "---\n" + "".join(kept_lines) + "---\n"
    rewritten = text[: match.start()] + replacement + text[match.end() :]
    return rewritten, stripped


def assert_no_symlinks(root: Path, display_root: str) -> None:
    """Reject source links so packaging can never read outside the checkout."""

    if root.is_symlink():
        raise PackagingError(f"{display_root}: symbolic links are not supported in upload packages")
    for directory, dirnames, filenames in os.walk(root, topdown=True, followlinks=False):
        for name in (*dirnames, *filenames):
            path = Path(directory) / name
            if path.is_symlink():
                relative = path.relative_to(ROOT).as_posix()
                raise PackagingError(f"{relative}: symbolic links are not supported in upload packages")


def tree_entries(staging: Path, root_name: str) -> list[tuple[Path, str]]:
    """Return directory and file entries in a stable, ZIP-friendly order."""

    root = staging / root_name
    entries: list[tuple[Path, str]] = []

    def visit(path: Path) -> None:
        if path.name == ".DS_Store":
            return
        if path.is_symlink():
            raise PackagingError(f"{root_name}: symbolic links are not supported in upload packages")

        archive_name = path.relative_to(staging).as_posix()
        if path.is_dir():
            entries.append((path, archive_name + "/"))
            # Path.iterdir follows the source directory's enumeration order,
            # just as Info-ZIP's recursive walk does. Archive consumers only
            # need the same set of entries, but preserving this order keeps
            # cross-language package comparisons maximally close.
            for child in path.iterdir():
                visit(child)
        elif path.is_file():
            entries.append((path, archive_name))
        else:
            raise PackagingError(f"{archive_name}: unsupported filesystem entry")

    visit(root)
    return entries


def write_zip(output: Path, staging: Path, roots: list[str]) -> None:
    """Write a package with explicit directory entries and deflated files."""

    if output.is_file() or output.is_symlink():
        output.unlink()

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for root_name in roots:
            for path, archive_name in tree_entries(staging, root_name):
                archive.write(path, archive_name)


def output_label(output: Path) -> str:
    output_string = str(output)
    prefix = str(ROOT) + os.sep
    return output_string[len(prefix) :] if output_string.startswith(prefix) else output_string


def main(argv: list[str]) -> int:
    try:
        args, unexpected = parser().parse_known_args(argv)
    except SystemExit as error:
        # Ruby's OptionParser reports malformed options with status 1 while
        # reserving status 0 for help. argparse uses status 2 for both errors.
        return 0 if error.code == 0 else 1
    unknown_options = [argument for argument in unexpected if argument.startswith("-")]
    if unknown_options:
        print(f"{parser().prog}: invalid option: {unknown_options[0]}", file=sys.stderr)
        return 1
    # File.expand_path expands a leading ``~`` as well as normalizing relative
    # components; shell quoting should not change that Ruby-compatible result.
    out = Path(os.path.abspath(os.path.expanduser(args.out)))
    selected = SKILLS if not args.skill else args.skill
    unknown = [skill for skill in selected if skill not in SKILLS]
    if unknown:
        print(f"unknown Skill(s): {', '.join(unknown)}", file=sys.stderr)
        return 1

    all_stripped: dict[str, list[str]] = {}
    with tempfile.TemporaryDirectory(prefix="pj-package-") as temporary:
        staging = Path(temporary)
        for skill in selected:
            source = ROOT / skill
            assert_no_symlinks(source, f"{skill}")
            destination = staging / skill
            shutil.copytree(source, destination, symlinks=True, dirs_exist_ok=True)
            skill_md = destination / "SKILL.md"
            if skill_md.is_symlink():
                raise PackagingError(f"{skill}/SKILL.md: symbolic links are not supported in upload packages")
            # Decode bytes explicitly so CRLF and other valid UTF-8 line
            # endings remain exactly as they were in the source file.
            text = skill_md.read_bytes().decode("utf-8")
            rewritten, stripped = strip_non_spec_frontmatter(text, f"{skill}/SKILL.md")
            all_stripped[skill] = stripped
            skill_md.write_bytes(rewritten.encode("utf-8"))

        if args.check:
            for skill in selected:
                dropped = all_stripped[skill]
                detail = "nothing to strip" if not dropped else f"would strip {', '.join(dropped)}"
                print(f"{skill}: {detail}")
            return 0

        out.mkdir(parents=True, exist_ok=True)
        for skill in selected:
            write_zip(out / f"{skill}.zip", staging, [skill])

        if not args.no_combined and sorted(selected) == sorted(SKILLS):
            write_zip(out / "product-judgement-all-skills.zip", staging, SKILLS)

    for skill in selected:
        dropped = all_stripped[skill]
        detail = "spec-clean" if not dropped else f"stripped {', '.join(dropped)}"
        print(f"{skill + '.zip':<20s} {detail}")
    print(f"Packages written to {output_label(out)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except PackagingError as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
