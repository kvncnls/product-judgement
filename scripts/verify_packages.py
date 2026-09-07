#!/usr/bin/env python3
"""Verify the upload archives users actually download.

The verifier checks every supporting file, frontmatter compatibility, source
instruction integrity, and archive paths. ZIP handling uses Python's standard
library so verification does not depend on a platform ``unzip`` command.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
import zipfile
from pathlib import Path
from typing import Any

try:  # Direct script execution puts scripts/ on sys.path.
    from yaml_utils import safe_load
except ImportError:  # pragma: no cover - supports package-style execution.
    from scripts.yaml_utils import safe_load


ROOT = Path(__file__).resolve().parent.parent
SKILLS = ["focal", "compass", "flywheel", "soul", "product-judgement"]
SPEC_KEYS = ["name", "description", "license", "compatibility", "metadata", "allowed-tools"]

_FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


class PackageVerificationError(Exception):
    """An expected archive verification failure."""


def ruby_inspect(value: Any) -> str:
    """Render the arrays and values used in errors like Ruby's ``inspect``."""

    return json.dumps(value, ensure_ascii=False)


def parser() -> argparse.ArgumentParser:
    command = "uv run scripts/verify_packages.py"
    result = argparse.ArgumentParser(
        prog=command,
        usage=f"{command} [--dir DIR] [--skill NAME]",
        description="Verify upload package archives.",
    )
    result.add_argument("--dir", default=str(ROOT / "dist"), metavar="DIR", help="Archive directory (default: dist/)")
    result.add_argument("--skill", action="append", dest="skills", default=[], metavar="NAME", help="Verify one archive; repeatable, skips combined archive")
    return result


def document(data: bytes, path: str) -> tuple[dict[Any, Any], str]:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise PackageVerificationError(f"{path}: invalid UTF-8") from error

    match = _FRONTMATTER.match(text)
    if match is None:
        raise PackageVerificationError(f"{path}: missing frontmatter")
    try:
        metadata = safe_load(match.group(1))
    except Exception as error:
        raise PackageVerificationError(f"{path}: invalid frontmatter ({str(error).splitlines()[0].strip()})") from error
    if not isinstance(metadata, dict):
        raise PackageVerificationError(f"{path}: frontmatter is not a mapping")
    return metadata, text[match.end() :]


def expected_files(skills: list[str]) -> list[str]:
    result: list[str] = []
    for skill in skills:
        skill_root = ROOT / skill
        for path in skill_root.rglob("*"):
            if path.name == ".DS_Store":
                continue
            if path.is_symlink():
                relative = path.relative_to(ROOT).as_posix()
                raise PackageVerificationError(f"{relative}: source symbolic links are not supported")
            if path.is_file():
                result.append(path.relative_to(ROOT).as_posix())
    return sorted(result)


def _is_symlink(info: zipfile.ZipInfo) -> bool:
    mode = (info.external_attr >> 16) & 0o177777
    return stat.S_ISLNK(mode)


def _entries(archive: Path) -> list[zipfile.ZipInfo]:
    try:
        with zipfile.ZipFile(archive) as package:
            return package.infolist()
    except (OSError, zipfile.BadZipFile) as error:
        raise PackageVerificationError(f"unzip failed: {str(error).strip()}") from error


def _read_entry(archive: Path, entry: str) -> bytes:
    try:
        with zipfile.ZipFile(archive) as package:
            return package.read(entry)
    except (OSError, RuntimeError, KeyError, zipfile.BadZipFile) as error:
        raise PackageVerificationError(f"unzip failed: {str(error).strip()}") from error


def verify_archive(archive: Path, skills: list[str]) -> None:
    if archive.is_symlink():
        raise PackageVerificationError(f"{archive}: symbolic links are not allowed")
    if not archive.is_file():
        raise PackageVerificationError(f"Missing archive: {archive}")

    infos = _entries(archive)
    entries = [info.filename for info in infos]
    unsafe = [
        entry
        for entry in entries
        if (
            not entry
            or entry.startswith(("/", "\\"))
            or "\\" in entry
            or "\x00" in entry
            or ".." in entry.split("/")
            or not entry.split("/")[0] in skills
        )
    ]
    if unsafe:
        raise PackageVerificationError(f"{archive}: unexpected or unsafe paths {ruby_inspect(unsafe)}")

    symlinks = [info.filename for info in infos if _is_symlink(info)]
    if symlinks:
        raise PackageVerificationError(f"{archive}: symbolic links are not allowed {ruby_inspect(symlinks)}")

    if len(set(entries)) != len(entries):
        raise PackageVerificationError(f"{archive}: duplicate entries")

    files = sorted(entry for entry in entries if not entry.endswith("/"))
    expected = expected_files(skills)
    if files != expected:
        missing = [entry for entry in expected if entry not in files]
        extra = [entry for entry in files if entry not in expected]
        raise PackageVerificationError(
            f"{archive}: missing {ruby_inspect(missing)}; extra {ruby_inspect(extra)}"
        )

    for entry in files:
        packed = _read_entry(archive, entry)
        try:
            source = (ROOT / entry).read_bytes()
        except OSError as error:
            raise PackageVerificationError(f"{archive}: {entry} cannot be read from source") from error

        if not entry.endswith("/SKILL.md"):
            if packed != source:
                raise PackageVerificationError(f"{archive}: {entry} differs from source")
            continue

        metadata, body = document(packed, entry)
        canonical, canonical_body = document(source, f"source {entry}")
        unknown = [key for key in metadata if key not in SPEC_KEYS]
        if unknown:
            raise PackageVerificationError(
                f"{archive}: {entry} contains unsupported keys {ruby_inspect(unknown)}"
            )
        expected_metadata = {key: value for key, value in canonical.items() if key in SPEC_KEYS}
        if metadata != expected_metadata:
            raise PackageVerificationError(f"{archive}: {entry} changed supported metadata")
        if body != canonical_body:
            raise PackageVerificationError(f"{archive}: {entry} changed instructions")
        if metadata.get("name") != entry.split("/")[0]:
            raise PackageVerificationError(f"{archive}: {entry} name does not match folder")
        description = metadata.get("description")
        if not isinstance(description, str) or not description.strip() or len(description) > 1024:
            raise PackageVerificationError(f"{archive}: {entry} invalid description")

    print(
        f"Verified {archive.name}: {len(skills)} Skill(s), {len(files)} source files, "
        "spec-compatible metadata."
    )


def main(argv: list[str]) -> int:
    try:
        args, unexpected = parser().parse_known_args(argv)
    except SystemExit as error:
        return 0 if error.code == 0 else 1
    if unexpected:
        print(f"Unexpected arguments: {' '.join(unexpected)}", file=sys.stderr)
        return 1

    archive_dir = Path(os.path.abspath(os.path.expanduser(args.dir)))
    selected = SKILLS if not args.skills else list(dict.fromkeys(args.skills))
    if any(skill not in SKILLS for skill in selected):
        print("Unknown Skill", file=sys.stderr)
        return 1

    try:
        for skill in selected:
            verify_archive(archive_dir / f"{skill}.zip", [skill])
        if not args.skills:
            verify_archive(archive_dir / "product-judgement-all-skills.zip", SKILLS)
    except PackageVerificationError as error:
        print(f"Package verification failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
