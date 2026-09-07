#!/usr/bin/env python3
"""Offline regressions for source validation and generated-file maintenance."""

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parent.parent


class ToolingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix="product-judgement-tooling-")
        cls.checkout = Path(cls.temporary.name) / "checkout"
        shutil.copytree(
            ROOT,
            cls.checkout,
            ignore=shutil.ignore_patterns(".git", ".venv", "__pycache__", "dist", "results"),
        )

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def run_tool(self, name, *arguments):
        return subprocess.run(
            [sys.executable, str(self.checkout / "scripts" / name), *arguments],
            cwd=self.checkout,
            capture_output=True,
            text=True,
            timeout=30,
        )

    def check_rejected_edit(self, path, transform, expected):
        target = self.checkout / path
        original = target.read_bytes()
        try:
            target.write_text(transform(original.decode("utf-8")), encoding="utf-8")
            result = self.run_tool("verify.py")
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn(expected, result.stderr)
        finally:
            target.write_bytes(original)

    def test_clean_checkout(self):
        result = self.run_tool("verify.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_frontmatter_description_limit(self):
        # A Unicode character counts as one character, not its UTF-8 byte length.
        self.check_rejected_edit(
            "focal/SKILL.md",
            lambda text: text.replace("description:", "description: " + "é" * 1025 + "\nold-description:", 1),
            "1024",
        )

    def test_frontmatter_aliases_are_rejected(self):
        self.check_rejected_edit(
            "focal/SKILL.md",
            lambda text: text.replace("license: MIT", "license: &license MIT\nmetadata: *license", 1),
            "alias",
        )

    def test_yaml_objects_are_rejected(self):
        self.check_rejected_edit(
            "focal/SKILL.md",
            lambda text: text.replace("license: MIT", "license: !!python/object:builtins.object {}", 1),
            "YAML",
        )

    def test_ci_cannot_invoke_paid_harness(self):
        self.check_rejected_edit(
            ".github/workflows/verify.yml",
            lambda text: text + '\n      - run: uv run "scripts/eval.py" --ablation\n',
            "must not run scripts/eval.py",
        )

    def test_stale_bundle_is_rejected_and_rebuild_repairs_it(self):
        target = self.checkout / "bundles/focal.md"
        original = target.read_bytes()
        try:
            target.write_bytes(original + b"Stale generated text.\n")
            result = self.run_tool("build_bundles.py", "--check")
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(target.read_bytes(), original + b"Stale generated text.\n")
            result = self.run_tool("build_bundles.py")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(target.read_bytes(), original)
        finally:
            target.write_bytes(original)

    def test_contract_check_is_read_only_and_sync_repairs_it(self):
        target = self.checkout / "focal/reference/review.md"
        original = target.read_bytes()
        stale = original.replace(b"<!-- BEGIN SHARED: evidence -->\n", b"<!-- BEGIN SHARED: evidence -->\nStale fragment.\n", 1)
        self.assertNotEqual(stale, original)
        try:
            target.write_bytes(stale)
            result = self.run_tool("sync_contracts.py", "--check")
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(target.read_bytes(), stale)
            result = self.run_tool("sync_contracts.py")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(target.read_bytes(), original)
        finally:
            target.write_bytes(original)

    def test_duplicate_contract_marker_prevents_partial_writes(self):
        target = self.checkout / "focal/reference/review.md"
        original = target.read_bytes()
        duplicate = original + b"\n<!-- BEGIN SHARED: evidence -->\nDuplicate.\n<!-- END SHARED: evidence -->\n"
        try:
            target.write_bytes(duplicate)
            result = self.run_tool("sync_contracts.py")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("expected exactly one evidence fragment", result.stderr)
            self.assertEqual(target.read_bytes(), duplicate)
        finally:
            target.write_bytes(original)

    def test_release_version_mismatch(self):
        result = self.run_tool("check_version.py", "0.0.0-invalid")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        for path in (".claude-plugin/plugin.json", ".claude-plugin/marketplace.json", ".cursor-plugin/plugin.json", ".codex-plugin/plugin.json"):
            self.assertIn(path, result.stderr)

    def test_missing_release_version(self):
        result = self.run_tool("check_version.py")
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
