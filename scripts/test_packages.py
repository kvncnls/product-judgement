#!/usr/bin/env python3
"""Regression tests for upload package creation and verification."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PYTHON = sys.executable

sys.path.insert(0, str(ROOT / "scripts"))
from package_skills import strip_non_spec_frontmatter  # noqa: E402


def run(*argv: str) -> tuple[str, bool]:
    result = subprocess.run(argv, capture_output=True, text=True)
    return result.stdout + result.stderr, result.returncode == 0


def expect_success(*argv: str) -> None:
    output, success = run(*argv)
    if not success:
        raise RuntimeError(f"{list(argv)!r}: {output}")


def replace_archive(source: Path, destination: Path, replacements: dict[str, bytes], removed: set[str] | None = None) -> None:
    removed = removed or set()
    with zipfile.ZipFile(source) as original, zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as rewritten:
        for info in original.infolist():
            if info.filename in removed:
                continue
            data = replacements.get(info.filename, original.read(info.filename))
            rewritten.writestr(info, data)


def main() -> int:
    package_script = ROOT / "scripts" / "package_skills.py"
    verifier_script = ROOT / "scripts" / "verify_packages.py"

    mixed_lines = "---\nname: focal\nargument-hint: reject\n---\nfirst\r\nsecond\n"
    rewritten, stripped = strip_non_spec_frontmatter(mixed_lines, "fixture/SKILL.md")
    if stripped != ["argument-hint"] or rewritten != "---\nname: focal\n---\nfirst\r\nsecond\n":
        raise RuntimeError("Frontmatter stripping changed mixed line endings")

    with tempfile.TemporaryDirectory(prefix="pj-package-tests-") as temporary:
        directory = Path(temporary)
        dist = directory / "dist"
        expect_success(PYTHON, str(package_script), "--out", str(dist))
        expect_success(PYTHON, str(verifier_script), "--dir", str(dist))

        original = directory / "original.zip"
        focal = dist / "focal.zip"
        shutil.copyfile(focal, original)

        extracted = directory / "extracted"
        extracted.mkdir()
        with zipfile.ZipFile(original) as archive:
            archive.extractall(extracted)
        skill = extracted / "focal" / "SKILL.md"
        clean = skill.read_text(encoding="utf-8")

        mutations = {
            "unsupported upload metadata": clean.replace("---\n", "---\nargument-hint: rejected\n", 1),
            "changed skill instructions": clean + "\nUnreviewed instruction.\n",
        }
        for label, content in mutations.items():
            shutil.copyfile(original, focal)
            replace_archive(original, focal, {"focal/SKILL.md": content.encode("utf-8")})
            _output, success = run(
                PYTHON,
                str(verifier_script),
                "--dir",
                str(dist),
                "--skill",
                "focal",
            )
            if success:
                raise RuntimeError(f"Verifier accepted {label}")

        shutil.copyfile(original, focal)
        replace_archive(original, focal, {}, {"focal/LICENSE"})
        _output, success = run(
            PYTHON,
            str(verifier_script),
            "--dir",
            str(dist),
            "--skill",
            "focal",
        )
        if success:
            raise RuntimeError("Verifier accepted an incomplete package")

        # A ZIP symlink has no safe source-file equivalent. Keep this check in
        # the regression suite so verifier changes cannot accidentally turn it
        # into an extract-and-follow operation.
        shutil.copyfile(original, focal)
        with zipfile.ZipFile(focal, "a") as archive:
            info = zipfile.ZipInfo("focal/external-link")
            info.create_system = 3
            info.external_attr = (0o120777 << 16) | 0xA000
            archive.writestr(info, b"../../outside")
        output, success = run(
            PYTHON,
            str(verifier_script),
            "--dir",
            str(dist),
            "--skill",
            "focal",
        )
        if success or "symbolic links" not in output:
            raise RuntimeError("Verifier did not reject a symbolic-link archive entry")

    print(
        "Package tests passed: complete archives accepted; unsupported metadata, changed instructions, "
        "and missing files rejected."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
