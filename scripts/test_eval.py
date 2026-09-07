#!/usr/bin/env python3
"""Offline unit coverage for the Python behavioral evaluation harness."""

from __future__ import annotations

import hashlib
import importlib.util
import contextlib
import io
import json
import os
from pathlib import Path
import signal
import sys
import tempfile
import time
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("product_judgement_eval", ROOT / "scripts" / "eval.py")
assert SPEC and SPEC.loader
EVAL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EVAL)


class EvaluationHelperTests(unittest.TestCase):
    def test_fixture_fingerprint_preserves_legacy_serialization(self):
        # Fixed input keeps the serialization contract test independent of
        # legitimate additions and edits to the behavioral fixture collection.
        fixture = {
            "skill": "focal",
            "id": "fingerprint-fixture",
            "mode": "audit",
            "scenario": "Audit an expert dashboard with café metrics.",
            "evidence": ["The organizing intent is routing."],
            "expected": ["Classify the screen as a hub before scoring."],
            "reject": ["Require four or fewer total routes."],
        }
        actual = hashlib.sha256(EVAL.canonical_fixture_yaml(fixture).encode()).hexdigest()
        self.assertEqual(actual, "40320e8ddcab6741c29b0f83db052cde5a7289a461aa4be26e8a3c393b330004")

    def test_prompt_and_excerpt_self_checks_pass(self):
        self.assertTrue(all(ok for _label, ok in EVAL.excerpt_selftest()))
        rows = EVAL.expand_rows(
            EVAL.load_fixtures(EVAL.FIXTURE_PATH),
            EVAL.default_options(),
            "product-judgement",
        )
        checks = EVAL.all_prompt_selftests(rows, "product-judgement")
        self.assertTrue(rows)
        self.assertTrue(all(ok for _label, ok in checks))

    def test_excerpt_adjudication_downgrades_unverifiable_verdicts(self):
        verdicts = [
            {
                "n": 1,
                "kind": "expected",
                "verdict": "pass",
                "excerpt": "present span",
                "reason": "ok",
            },
            {
                "n": 2,
                "kind": "expected",
                "verdict": "pass",
                "excerpt": "",
                "reason": "missing quote",
            },
            {
                "n": 3,
                "kind": "reject",
                "verdict": "fail",
                "excerpt": "invented span",
                "reason": "bad",
            },
        ]
        fabricated, empty = EVAL.adjudicate_verdicts(
            verdicts, "The present span is in this transcript."
        )
        self.assertEqual((fabricated, empty), (1, 1))
        self.assertEqual(verdicts[0]["verdict"], "pass")
        self.assertEqual(verdicts[1]["verdict"], "fail")
        self.assertEqual(verdicts[2]["verdict"], "unclear")

    def test_envelope_and_judge_payload_guards(self):
        with self.assertRaises(EVAL.RunnerError):
            EVAL.parse_envelope("", "authentication failed")
        with self.assertRaises(EVAL.RunnerError):
            EVAL.parse_envelope("[]", "")
        with self.assertRaises(EVAL.RunnerError):
            EVAL.parse_envelope(
                '{"is_error":"authentication failed","result":"expired"}', ""
            )
        payload = EVAL.judge_payload(
            {"structuredOutput": '{"verdicts": [{"n": 1}]}'}
        )
        self.assertEqual(payload["verdicts"][0]["n"], 1)
        self.assertEqual(
            EVAL.judge_payload({"result": [{"n": 1}]}),
            {"verdicts": [{"n": 1}]},
        )
        assertions = [{"n": 1, "kind": "expected", "text": "x"}]
        self.assertIsNone(
            EVAL.shape_error(
                [{"n": 1, "kind": "expected", "verdict": "pass"}],
                assertions,
            )
        )
        self.assertIn(
            "expected 1 verdicts",
            EVAL.shape_error([], assertions),
        )

    def test_ruby_truthiness_and_half_up_rounding(self):
        self.assertTrue(EVAL._ruby_truthy(""))
        self.assertTrue(EVAL._ruby_truthy(0))
        self.assertFalse(EVAL._ruby_truthy(None))
        self.assertEqual(EVAL._ruby_round(1 / 16), 0.063)

    def test_nonstandard_json_numbers_are_rejected(self):
        for constant in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(constant=constant):
                with self.assertRaises(EVAL.RunnerError):
                    EVAL.parse_envelope('{"result":"review","total_cost_usd":' + constant + '}', "")
                with self.assertRaises(json.JSONDecodeError):
                    EVAL.extract_json('{"verdicts":' + constant + '}')
        with self.assertRaises(ValueError):
            EVAL._json_generate({"cost": float("nan")})

    def test_nonfinite_numeric_options_are_rejected(self):
        for option in ("--max-cost-usd", "--per-run-budget-usd", "--fail-under"):
            for value in ("NaN", "Infinity", "-Infinity"):
                with self.subTest(option=option, value=value):
                    with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as raised:
                        EVAL.parse_options([f"{option}={value}"])
                    self.assertEqual(raised.exception.code, 2)

    def test_fixture_yaml_uses_restricted_loader(self):
        with tempfile.TemporaryDirectory(prefix="product-judgement-eval-yaml-") as directory:
            source = Path(directory) / "fixture.yml"
            source.write_text("first: &value safe\nsecond: *value\n", encoding="utf-8")
            with self.assertRaises(EVAL.yaml.YAMLError):
                EVAL.load_yaml(str(source))

    def test_provenance_hashes_preserve_line_endings(self):
        canonical = (Path(EVAL.ROOT) / "focal/SKILL.md").read_bytes()
        with tempfile.TemporaryDirectory(prefix="product-judgement-eval-provenance-") as directory:
            checkout = Path(directory) / "checkout"
            (checkout / "focal").mkdir(parents=True)
            (checkout / "focal/SKILL.md").write_bytes(canonical)
            installed = Path(directory) / "installed.md"
            installed_bytes = canonical.replace(b"\n", b"\r\n")
            installed.write_bytes(installed_bytes)
            with patch.object(EVAL, "ROOT", str(checkout)), patch.object(EVAL, "installed_skill_paths", return_value=[str(installed)]):
                plan = EVAL.build_provenance_plan("focal")
            self.assertEqual(plan["working_tree_sha256"], hashlib.sha256(canonical).hexdigest())
            self.assertEqual(plan["installed_copies"][0]["sha256"], hashlib.sha256(installed_bytes).hexdigest())
            self.assertFalse(plan["installed_copies"][0]["identical_to_working_tree"])
            self.assertEqual(plan["status"], "undecidable")

    def test_timeout_remains_bounded_when_detached_child_holds_pipes(self):
        with tempfile.TemporaryDirectory(prefix="product-judgement-eval-detached-") as directory:
            pid_path = Path(directory) / "child.pid"
            child = (
                "from pathlib import Path; import os, time; "
                f"Path({str(pid_path)!r}).write_text(str(os.getpid())); "
                "print('ready', flush=True); time.sleep(6)"
            )
            parent = (
                "import subprocess, sys, time; "
                "subprocess.Popen([sys.executable, '-c', sys.argv[1]], start_new_session=True); "
                "time.sleep(6)"
            )
            try:
                started = time.monotonic()
                stdout, _, _, state = EVAL.spawn_capture([sys.executable, "-c", parent, child], "", 0.25, directory)
                self.assertEqual(state, "timeout")
                self.assertLess(time.monotonic() - started, 4.8)
                self.assertIn("ready", stdout)
            finally:
                if pid_path.exists():
                    try:
                        os.killpg(int(pid_path.read_text()), signal.SIGKILL)
                    except ProcessLookupError:
                        pass

    def test_process_group_timeout_returns_without_waiting_for_child(self):
        with tempfile.TemporaryDirectory(prefix="product-judgement-eval-timeout-") as directory:
            directory_path = Path(directory)
            pid_path = directory_path / "child.pid"
            done_path = directory_path / "child.done"
            child = (
                "from pathlib import Path; import os, time; "
                f"Path({str(pid_path)!r}).write_text(str(os.getpid())); "
                "time.sleep(30); "
                f"Path({str(done_path)!r}).write_text('done')"
            )
            parent = (
                "import subprocess, sys, time; "
                "subprocess.Popen([sys.executable, '-c', sys.argv[1]]); "
                "time.sleep(30)"
            )
            started = time.monotonic()
            _stdout, _stderr, _status, state = EVAL.spawn_capture(
                [sys.executable, "-c", parent, child],
                "",
                0.25,
                str(directory_path),
            )
            elapsed = time.monotonic() - started
            self.assertEqual(state, "timeout")
            self.assertLess(elapsed, 3.0)
            time.sleep(0.1)
            self.assertFalse(done_path.exists())
            if pid_path.exists():
                child_pid = int(pid_path.read_text())
                try:
                    os.kill(child_pid, 0)
                except (ProcessLookupError, PermissionError):
                    pass
                else:
                    self.fail("timed-out child process survived its process-group kill")

    def test_argv_keeps_loader_and_tool_guards(self):
        opts = EVAL.default_options()
        candidate = EVAL.candidate_argv(opts)
        ablation = EVAL.ablation_argv(opts)
        judge = EVAL.judge_argv(opts, "/tmp/judge-system-prompt.txt")
        self.assertIn("--plugin-dir", candidate)
        self.assertIn("--add-dir", candidate)
        self.assertNotIn("--plugin-dir", ablation)
        self.assertEqual(judge[judge.index("--tools") + 1], "")
        self.assertEqual(judge[judge.index("--setting-sources") + 1], "")
        self.assertEqual(
            EVAL._sha256_text(EVAL._json_generate(EVAL.JUDGE_SCHEMA))[:8],
            "bd7f93fb",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
