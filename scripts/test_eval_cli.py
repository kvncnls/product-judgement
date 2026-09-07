#!/usr/bin/env python3
"""Exercise the evaluation CLI with a local fake runner; never call a model."""

from pathlib import Path
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parent.parent
TRANSCRIPT = "The review found evidence."
FAKE_RUNNER = r'''
import json, os, re, sys
from pathlib import Path

args = sys.argv[1:]
if args == ["--version"]:
    print("offline-eval-test-runner")
    raise SystemExit(0)
prompt = sys.stdin.read()
mode = os.environ["PJ_FAKE_MODE"]
judge = "--json-schema" in args
provenance = "PROVENANCE CHECK" in prompt
record = {"role": "judge" if judge else "provenance" if provenance else "candidate", "args": args, "prompt": prompt}
with open(os.environ["PJ_FAKE_LOG"], "a", encoding="utf-8") as log:
    log.write(json.dumps(record) + "\n")
envelope = {"is_error": False, "subtype": "success", "total_cost_usd": 0.02, "session_id": "offline", "num_turns": 1, "duration_ms": 1}
if mode == "auth-error" and not judge:
    envelope.update(is_error=True, result="Test authentication failure")
elif provenance:
    skill = prompt.split()[0].rsplit(":", 1)[1]
    checkout = Path(args[args.index("--plugin-dir") + 1])
    envelope["result"] = (checkout / skill / "SKILL.md").read_text(encoding="utf-8")
elif judge:
    if mode == "malformed-judge":
        envelope["result"] = "No usable JSON here."
    else:
        assertions = re.findall(r"^(\d+)\. \[(expected|reject)\]", prompt, re.MULTILINE)
        verdicts = []
        for number, kind in assertions:
            verdicts.append({"n": int(number), "kind": kind, "verdict": "fail" if mode == "regression" and kind == "expected" else "pass", "excerpt": "The review found evidence.", "reason": "Offline test verdict"})
        envelope["structured_output"] = {"verdicts": verdicts}
        envelope["result"] = ""
else:
    envelope["result"] = "The review found evidence."
print(json.dumps(envelope))
'''


class EvaluationCLITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix="product-judgement-eval-cli-")
        cls.directory = Path(cls.temporary.name)
        cls.checkout = cls.directory / "checkout"
        shutil.copytree(ROOT, cls.checkout, ignore=shutil.ignore_patterns(".git", ".venv", "__pycache__", "dist", "results"))
        cls.fake_bin = cls.directory / "bin"
        cls.fake_bin.mkdir()
        runner = cls.fake_bin / "claude"
        runner.write_text(f"#!{sys.executable}\n" + FAKE_RUNNER, encoding="utf-8")
        runner.chmod(0o755)

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def run_evaluation(self, mode="pass", arguments=(), *, allow_ci=True):
        run_directory = Path(tempfile.mkdtemp(prefix="run-", dir=self.directory))
        log = run_directory / "calls.jsonl"
        # PATH contains only our fake runner, so a test can never fall through
        # to a signed-in model CLI. The shebang uses this test's absolute Python.
        environment = dict(os.environ, PATH=str(self.fake_bin), PJ_FAKE_MODE=mode, PJ_FAKE_LOG=str(log), CI="true")
        command = [sys.executable, str(self.checkout / "scripts/eval.py"), "--id", "focal-expert-hub", "--repeat", "1", "--jobs", "1", "--out", str(run_directory / "output")]
        if allow_ci:
            command.append("--allow-ci")
        command.extend(arguments)
        result = subprocess.run(command, cwd=self.checkout, env=environment, capture_output=True, text=True, timeout=30)
        artifact_path = run_directory / "output/eval.json"
        artifact = json.loads(artifact_path.read_text()) if artifact_path.exists() else None
        calls = [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []
        return result, artifact, calls

    def test_success_artifact_and_runner_isolation(self):
        result, artifact, calls = self.run_evaluation()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(artifact["schema"], "product-judgement.eval/1")
        self.assertEqual(artifact["harness"]["script"], "scripts/eval.py")
        self.assertEqual(artifact["totals"]["rows"], 1)
        self.assertEqual(artifact["totals"]["pass"], 1)
        self.assertEqual(artifact["results"][0]["status_label"], "PASS")
        for assertion in artifact["results"][0]["assertions"]:
            self.assertEqual((assertion["pass"], assertion["denominator"], assertion["rate"]), (1, 1, 1.0))
        candidate = next(call for call in calls if call["role"] == "candidate")
        judge = next(call for call in calls if call["role"] == "judge")
        self.assertIn("--plugin-dir", candidate["args"])
        self.assertNotIn("Classify the screen as a hub before scoring.", candidate["prompt"])
        self.assertEqual(judge["args"][judge["args"].index("--tools") + 1], "")
        self.assertIn("Classify the screen as a hub before scoring.", judge["prompt"])

    def test_behavioral_failure_uses_regression_exit(self):
        result, artifact, _ = self.run_evaluation("regression")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(artifact["totals"]["fail"], 1)
        self.assertEqual(artifact["totals"]["harness_errors"], 0)

    def test_authentication_failure_is_not_a_regression(self):
        result, artifact, calls = self.run_evaluation("auth-error")
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertFalse(any(call["role"] == "judge" for call in calls))
        if artifact:
            self.assertGreater(artifact["totals"]["harness_errors"], 0)

    def test_bad_judge_retries_once_then_reports_harness_error(self):
        result, artifact, calls = self.run_evaluation("malformed-judge")
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertEqual(sum(call["role"] == "judge" for call in calls), 2)
        self.assertEqual(artifact["totals"]["error"], 1)

    def test_ablation_no_signal_is_fixture_quality_exit(self):
        result, artifact, calls = self.run_evaluation(arguments=("--ablation", "--control", "0"))
        self.assertEqual(result.returncode, 4, result.stdout + result.stderr)
        self.assertEqual(artifact["totals"]["no_signal"], 1)
        baseline = next(call for call in calls if call["role"] == "candidate" and "--safe-mode" in call["args"])
        self.assertNotIn("--plugin-dir", baseline["args"])
        self.assertNotIn("/product-judgement:focal", baseline["prompt"])

    def test_cost_ceiling_stops_remaining_work(self):
        result, artifact, calls = self.run_evaluation(arguments=("--repeat", "3", "--max-cost-usd", "0.01"))
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("cost", result.stderr.lower())
        self.assertLessEqual(sum(call["role"] == "candidate" for call in calls), 1)
        self.assertGreaterEqual(artifact["totals"]["cost_usd"], 0.01)

    def test_ci_guard_rejects_execution_without_opt_in(self):
        result, artifact, calls = self.run_evaluation(allow_ci=False)
        self.assertEqual(result.returncode, 2)
        self.assertIn("--allow-ci", result.stderr)
        self.assertIsNone(artifact)
        self.assertEqual(calls, [])

    def test_no_matching_fixture_uses_no_match_exit(self):
        result, artifact, calls = self.run_evaluation(arguments=("--skill", "no-such-skill"))
        self.assertEqual(result.returncode, 3, result.stdout + result.stderr)
        self.assertIsNone(artifact)
        self.assertEqual(calls, [])

    def test_decoy_control_records_a_judge_leak(self):
        result, artifact, _ = self.run_evaluation(arguments=("--id", "focal-static-evidence", "--control", "1"))
        self.assertEqual(result.returncode, 4, result.stdout + result.stderr)
        self.assertEqual(len(artifact["judge_control"]), 1)
        self.assertTrue(artifact["judge_control"][0]["leak"])
        self.assertEqual(artifact["totals"]["judge_control_leak"], 1)

    def test_calibration_only_grades_the_supplied_transcript(self):
        directory = self.checkout / "tests/judge-calibration"
        directory.mkdir(exist_ok=True)
        case = directory / "offline-cli-test.yml"
        case.write_text(json.dumps({
            "id": "offline-cli-test",
            "transcript": TRANSCRIPT,
            "assertions": [
                {"kind": "expected", "text": "Describe observed evidence.", "verdict": "pass"},
                {"kind": "reject", "text": "Invent absent observations.", "verdict": "pass"},
            ],
        }), encoding="utf-8")
        try:
            result, artifact, calls = self.run_evaluation(arguments=("--calibrate",))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue(all(call["role"] == "judge" for call in calls))
            self.assertEqual(artifact["totals"]["rows"], 0)
            calibration = next(item for item in artifact["calibration"] if item["id"] == "offline-cli-test")
            self.assertEqual(calibration["agreements"], 2)
            self.assertEqual(calibration["rate"], 1.0)
        finally:
            case.unlink()


if __name__ == "__main__":
    unittest.main(verbosity=2)
