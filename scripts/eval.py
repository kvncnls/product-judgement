#!/usr/bin/env python3
"""Behavioral evaluation harness for the Product Judgement Skill collection.

This is the Python port of the repository's Ruby evaluator. Live runs are
intentionally opt-in: they spend model tokens, are non-deterministic, and must
never be invoked by CI or the free text verifier.
"""

from __future__ import annotations

import argparse
import datetime as _datetime
import fnmatch
import hashlib
import json
import math
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path
from queue import Empty, Queue
from typing import Any

import yaml

try:  # Running scripts/eval.py directly has no package context.
    from yaml_utils import safe_load
except ImportError:  # Supports importing as scripts.eval from the repository root.
    from scripts.yaml_utils import safe_load


ROOT = str(Path(__file__).resolve().parent.parent)
PLUGIN_MANIFEST_PATH = os.path.join(ROOT, ".claude-plugin", "plugin.json")
SUPPORTED_MODES = ("audit", "build")

# shared names no runnable Skill. It expands to the four local Skills and each
# arm is reported as its own row.
LOCAL_SKILLS = ("focal", "compass", "flywheel", "soul")
ALL_SKILLS = LOCAL_SKILLS + ("product-judgement",)

FIXTURE_PATH = os.path.join(ROOT, "tests", "behavioral-contracts.yml")
CALIBRATION_DIR = os.path.join(ROOT, "tests", "judge-calibration")
ARTIFACT_SCHEMA = "product-judgement.eval/1"

# Pinned full dated ids, never moving aliases such as sonnet, opus, or fable.
# UNVERIFIED: these ids were not resolved against this account because doing so
# costs model tokens. A failed resolution is a harness error (exit 2).
DEFAULT_MODEL = "claude-sonnet-4-5-20250929"
DEFAULT_JUDGE_MODEL = "claude-haiku-4-5-20251001"

# The candidate keeps Read/Glob/Grep because each Skill instructs a read of its
# own reference files. All other tools are denied.
CANDIDATE_DENY_TOOLS = "Bash,Edit,Write,NotebookEdit,WebFetch,WebSearch,Task"
JUDGE_BUDGET_USD = "0.20"

EXIT_OK = 0
EXIT_REGRESSION = 1
EXIT_HARNESS = 2
EXIT_NO_MATCH = 3
EXIT_FIXTURE_QUALITY = 4


class RunnerError(Exception):
    """The runner or its envelope did not produce usable evaluation evidence."""


class JudgeError(Exception):
    """The judge did not produce a usable verdict payload."""


def _ruby_truthy(value: Any) -> bool:
    # Ruby considers every value except nil and false truthy, including "" and 0.
    return value is not None and value is not False


def _ruby_string(value: Any) -> str:
    """The small subset of Ruby Object#to_s used by the original harness."""

    if value is None:
        return ""
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, str):
        return value
    return str(value)


def _ruby_float(value: Any) -> float:
    # Ruby nil.to_f and non-numeric String#to_f both produce zero.
    if value is None:
        return 0.0
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _ruby_int(value: Any) -> int:
    if value is None:
        return 0
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def _ruby_round(value: float, digits: int = 3) -> float:
    # Ruby Float#round is half-away-from-zero; Decimal avoids Python's
    # ties-to-even behavior at exact halfway values.
    from decimal import Decimal, ROUND_HALF_UP

    quantum = Decimal(1).scaleb(-digits)
    rounded = Decimal(str(value)).quantize(quantum, rounding=ROUND_HALF_UP)
    return float(rounded)


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _read_utf8_file(path: str) -> str:
    # Ruby File.read(..., encoding: "UTF-8") preserves CRLF bytes; open(...,
    # encoding="utf-8") would apply Python's universal-newline translation.
    with open(path, "rb") as handle:
        return handle.read().decode("utf-8")


class _JSONConstantError(json.JSONDecodeError):
    """JSONDecodeError raised specifically for NaN and Infinity constants."""


def _reject_json_constant(value: str) -> Any:
    raise _JSONConstantError(
        f"invalid JSON constant {value}", value, 0
    )


def _json_loads(text: str) -> Any:
    return json.loads(text, parse_constant=_reject_json_constant)


def _json_generate(value: Any) -> str:
    # Ruby JSON.generate emits compact UTF-8 JSON.
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        allow_nan=False,
    )


def _json_pretty(value: Any) -> str:
    # Ruby JSON.pretty_generate uses two-space indentation and retains UTF-8.
    return json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)


def load_plugin_name() -> str:
    try:
        raw = _json_loads(_read_utf8_file(PLUGIN_MANIFEST_PATH))
    except (OSError, json.JSONDecodeError) as error:
        raise RunnerError(
            f"cannot read plugin manifest {PLUGIN_MANIFEST_PATH}: {error}"
        ) from error

    name = raw.get("name") if isinstance(raw, dict) else None
    if (
        not isinstance(name, str)
        or not name.strip()
        or re.fullmatch(r"[a-z0-9][a-z0-9._-]*", name) is None
    ):
        raise RunnerError(
            f"{PLUGIN_MANIFEST_PATH}: name must be a non-empty CLI-safe string"
        )
    return name


# ---------------------------------------------------------------------------
# Judge contract
# ---------------------------------------------------------------------------

JUDGE_SYSTEM_PROMPT = """You are a strict contract grader for a design-methodology skill collection. You are
given (1) a numbered list of assertions and (2) a candidate transcript. For each
assertion you return a verdict and a verbatim excerpt from the transcript that
justifies it.

Rules you must follow exactly.

1. Judge only the candidate transcript. You have no other evidence. Do not use what
   you believe a good design review should say. Do not reward effort, length,
   formatting, or confident tone.
2. Every excerpt must be copied character-for-character from the transcript. Never
   paraphrase, summarize, translate, correct, or complete an excerpt. If you cannot
   copy a span that justifies your verdict, the verdict is not "pass".
3. Assertions are of two kinds.
   - kind "expected": pass only if the transcript actually does the thing. An
     assertion the transcript merely gestures at, or does adjacently, is "fail".
     Absence of evidence is "fail", not "pass".
   - kind "reject": this describes a behavior the transcript must NOT exhibit. pass
     means the transcript does not do it; fail means it does. For a "reject" that
     passes, set excerpt to "" and state in one clause what you looked for and did
     not find.
4. Use "unclear" only when the transcript addresses the assertion's subject but the
   wording genuinely permits both readings. "unclear" is not a way to avoid
   deciding, and it does not mean "partially". Never use it because the assertion
   is hard.
5. If the transcript is an error, a refusal, an empty string, or a clarifying
   question rather than an audit, mark every "expected" assertion "fail" with
   excerpt "" and reason "no audit produced".
6. Judge each assertion independently. Do not let a strong overall impression carry
   a specific assertion, and do not let one failure drag down the others.
7. Output only the JSON object. No preamble, no code fence, no commentary.
8. When an assertion asks for a useful or actionable audit, pass requires a
   concrete, situated change grounded in the transcript's evidence. A generic
   principle, a keyword, or an unlocated recommendation is not enough. If the
   assertion asks to preserve context, safety, permission, or informed choice,
   the excerpt must show that protection and its relevant boundary. If it asks for
   a tradeoff, the excerpt must name both sides of the decision.
"""

JUDGE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["verdicts"],
    "properties": {
        "verdicts": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["n", "kind", "verdict", "excerpt", "reason"],
                "properties": {
                    "n": {"type": "integer", "minimum": 1},
                    "kind": {"type": "string", "enum": ["expected", "reject"]},
                    "verdict": {
                        "type": "string",
                        "enum": ["pass", "fail", "unclear"],
                    },
                    "excerpt": {"type": "string", "maxLength": 400},
                    "reason": {"type": "string", "maxLength": 300},
                },
            },
        }
    },
}


# ---------------------------------------------------------------------------
# Prompt rendering
# ---------------------------------------------------------------------------

def render_candidate_prompt(
    skill_name: str,
    mode: str,
    scenario: str,
    evidence: list[str],
    invoke: str,
    plugin_name: str,
) -> str:
    """Render the only candidate prompt builder in the harness."""

    if mode not in SUPPORTED_MODES:
        raise ValueError(f"unsupported candidate mode {mode!r}")

    prefix = f"/{plugin_name}:{skill_name} " if invoke == "slash" else ""
    verb = "Build" if mode == "build" else "Audit"
    lines = [
        f"{prefix}{verb} this. Produce your normal output from the evidence below.",
        "Do not ask clarifying questions; if a field is unevidenced, use your contract's",
        "own convention for that.",
        "",
        f"Scenario: {scenario}",
        "",
        "Evidence:",
    ]
    lines.extend(f"- {item}" for item in evidence)
    return "\n".join(lines) + "\n"


def render_judge_user_message(
    assertions: list[dict[str, Any]], candidate_text: str
) -> str:
    lines = ["## Assertions", ""]
    lines.extend(
        f"{assertion['n']}. [{assertion['kind']}] {assertion['text']}"
        for assertion in assertions
    )
    lines.extend(
        [
            "",
            "## Candidate transcript",
            "",
            "<<<BEGIN TRANSCRIPT",
            _ruby_string(candidate_text),
            "END TRANSCRIPT",
        ]
    )
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Text normalization and excerpt verification
# ---------------------------------------------------------------------------

PUNCTUATION_MAP = {
    "‘": "'",
    "’": "'",
    "‚": "'",
    "‛": "'",
    "“": '"',
    "”": '"',
    "„": '"',
    "‟": '"',
    "′": "'",
    "″": '"',
    "«": '"',
    "»": '"',
    "‐": "-",
    "‑": "-",
    "‒": "-",
    "–": "-",
    "—": "-",
    "―": "-",
    "−": "-",
    "\u00a0": " ",
    "\u2007": " ",
    "\u202f": " ",
    "\u2009": " ",
    "…": "...",
}
INVISIBLE_MAP = {"　": " ", "\ufeff": ""}


def normalize_for_match(text: Any) -> str:
    out = _ruby_string(text)
    for source, target in PUNCTUATION_MAP.items():
        out = out.replace(source, target)
    for source, target in INVISIBLE_MAP.items():
        out = out.replace(source, target)
    return re.sub(r"\s+", " ", out).strip()


def normalize_loose(text: Any) -> str:
    return re.sub(r"[*_\x60]", "", normalize_for_match(text)).strip()


def excerpt_present(excerpt: Any, candidate_text: Any) -> bool:
    needle = normalize_for_match(excerpt)
    if not needle:
        return False
    haystack = normalize_for_match(candidate_text)
    if needle in haystack:
        return True
    trimmed = re.sub(r'^["\']+', "", needle)
    trimmed = re.sub(r'["\']+$', "", trimmed)
    return bool(trimmed) and trimmed in haystack


def adjudicate_verdicts(
    verdicts: list[dict[str, Any]], candidate_text: str
) -> tuple[int, int]:
    fabricated = 0
    empties = 0

    for verdict in verdicts:
        verdict["excerpt_verified"] = None
        verdict["adjusted_from"] = None
        verdict["adjust_reason"] = None

        kind = verdict.get("kind")
        call = verdict.get("verdict")
        excerpt = _ruby_string(verdict.get("excerpt"))

        if kind == "expected" and call == "pass":
            if not normalize_for_match(excerpt):
                empties += 1
                verdict["adjusted_from"] = "pass"
                verdict["verdict"] = "fail"
                verdict["excerpt_verified"] = False
                verdict["adjust_reason"] = "empty excerpt on an expected pass"
            elif excerpt_present(excerpt, candidate_text):
                verdict["excerpt_verified"] = True
            else:
                fabricated += 1
                verdict["adjusted_from"] = "pass"
                verdict["verdict"] = "fail"
                verdict["excerpt_verified"] = False
                verdict["adjust_reason"] = (
                    "excerpt not present in the candidate transcript"
                )
        elif kind == "reject" and call == "fail":
            if not normalize_for_match(excerpt) or not excerpt_present(
                excerpt, candidate_text
            ):
                fabricated += 1
                verdict["adjusted_from"] = "fail"
                verdict["verdict"] = "unclear"
                verdict["excerpt_verified"] = False
                verdict["adjust_reason"] = (
                    "excerpt not present in the candidate transcript"
                )
            else:
                verdict["excerpt_verified"] = True

    return fabricated, empties


def excerpt_selftest() -> list[tuple[str, bool]]:
    transcript = (
        "The journey is open‑ended: catalog search has no completion event.\n"
        "It preserves the user’s filtered\nresult set on return."
    )
    cases: list[tuple[str, bool]] = [
        [
            "curly apostrophe matches straight",
            excerpt_present("the user's filtered result set", transcript),
        ],
        ["hard wrap collapses to a space", excerpt_present("filtered result set", transcript)],
        ["non-breaking hyphen matches ASCII", excerpt_present("open-ended", transcript)],
        ["quoted excerpt still matches", excerpt_present('"no completion event"', transcript)],
        ["absent span is rejected", not excerpt_present("names a progress bar", transcript)],
        ["empty excerpt is rejected", not excerpt_present("   ", transcript)],
    ]
    verdicts: list[dict[str, Any]] = [
        {
            "n": 1,
            "kind": "expected",
            "verdict": "pass",
            "excerpt": "no completion event",
            "reason": "x",
        },
        {
            "n": 2,
            "kind": "expected",
            "verdict": "pass",
            "excerpt": "invented span",
            "reason": "x",
        },
        {
            "n": 3,
            "kind": "expected",
            "verdict": "pass",
            "excerpt": "",
            "reason": "x",
        },
        {
            "n": 4,
            "kind": "reject",
            "verdict": "fail",
            "excerpt": "invented span",
            "reason": "x",
        },
        {
            "n": 5,
            "kind": "reject",
            "verdict": "pass",
            "excerpt": "",
            "reason": "x",
        },
    ]
    fabricated, empties = adjudicate_verdicts(verdicts, transcript)
    cases.extend(
        [
            [
                "verified pass survives",
                verdicts[0]["verdict"] == "pass"
                and verdicts[0]["excerpt_verified"] is True,
            ],
            ["fabricated expected pass becomes fail", verdicts[1]["verdict"] == "fail"],
            ["empty expected pass becomes fail", verdicts[2]["verdict"] == "fail"],
            [
                "fabricated reject fail becomes unclear",
                verdicts[3]["verdict"] == "unclear",
            ],
            [
                "clean reject pass is untouched",
                verdicts[4]["verdict"] == "pass"
                and verdicts[4]["adjusted_from"] is None,
            ],
            [
                "counters split fabrication from emptiness",
                fabricated == 2 and empties == 1,
            ],
        ]
    )
    return [(str(label), bool(ok)) for label, ok in cases]


def candidate_prompt_selftest(plugin_name: str) -> list[tuple[str, bool]]:
    scenario = "A static review with one supported state."
    evidence = ["The default state is visible."]
    expected_text = "Award the score named by this hidden assertion."
    reject_text = "Do not reveal this hidden rejection."
    slash_audit = render_candidate_prompt(
        "compass", "audit", scenario, evidence, "slash", plugin_name
    )
    auto_audit = render_candidate_prompt(
        "compass", "audit", scenario, evidence, "auto", plugin_name
    )
    slash_build = render_candidate_prompt(
        "compass", "build", scenario, evidence, "slash", plugin_name
    )
    auto_build = render_candidate_prompt(
        "compass", "build", scenario, evidence, "auto", plugin_name
    )
    prefix = f"/{plugin_name}:compass "

    return [
        ["namespaced slash invocation", slash_audit.startswith(prefix)],
        [
            "slash and baseline audit bodies match",
            slash_audit.removeprefix(prefix) == auto_audit,
        ],
        [
            "slash and baseline build bodies match",
            slash_build.removeprefix(prefix) == auto_build,
        ],
        ["audit mode renders audit instruction", auto_audit.splitlines()[0].startswith("Audit this.")],
        ["build mode renders build instruction", auto_build.splitlines()[0].startswith("Build this.")],
        [
            "synthetic expected assertion is withheld",
            expected_text not in slash_audit and expected_text not in auto_audit,
        ],
        [
            "synthetic reject assertion is withheld",
            reject_text not in slash_audit and reject_text not in auto_audit,
        ],
    ]


def candidate_prompt_leak_selftest(rows: list[dict[str, Any]]) -> list[tuple[str, bool]]:
    results: list[tuple[str, bool]] = []
    for row in rows:
        prompts = [row.get("prompt"), row.get("ablation_prompt")]
        leaked = [
            assertion
            for assertion in row["assertions"]
            if any(
                _ruby_string(prompt).find(_ruby_string(assertion["text"])) >= 0
                for prompt in prompts
            )
        ]
        results.append(
            [
                f"{row['label']} has no expected/reject text in candidate prompt",
                not leaked,
            ]
        )
    return results


def all_prompt_selftests(
    rows: list[dict[str, Any]], plugin_name: str
) -> list[tuple[str, bool]]:
    return candidate_prompt_selftest(plugin_name) + candidate_prompt_leak_selftest(rows)


# ---------------------------------------------------------------------------
# Subprocess runner
# ---------------------------------------------------------------------------

def spawn_capture(
    cmd: list[str], stdin_data: str, timeout_s: int | float, chdir: str
) -> tuple[str, str, int | None, str]:
    """Run a command in its own process group and capture output with a timeout."""

    try:
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=chdir,
            start_new_session=True,
        )
    except FileNotFoundError as error:
        raise RunnerError(f"cannot execute {cmd[0]!r}: {error}") from error

    encoded_input = stdin_data.encode("utf-8")
    try:
        stdout, stderr = process.communicate(input=encoded_input, timeout=timeout_s)
        return (
            stdout.decode("utf-8", errors="replace"),
            stderr.decode("utf-8", errors="replace"),
            process.returncode,
            "ok",
        )
    except subprocess.TimeoutExpired as error:
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except (ProcessLookupError, PermissionError):
            pass
        time.sleep(0.5)
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass
        partial_stdout = error.output or b""
        partial_stderr = error.stderr or b""
        try:
            collected_stdout, collected_stderr = process.communicate(timeout=2)
            partial_stdout = collected_stdout or partial_stdout
            partial_stderr = collected_stderr or partial_stderr
        except subprocess.TimeoutExpired as reap_error:
            # A detached descendant can retain inherited pipes after the parent
            # dies. Do not wait forever for EOF from that descendant.
            partial_stdout = reap_error.output or partial_stdout
            partial_stderr = reap_error.stderr or partial_stderr
            for stream in (process.stdin, process.stdout, process.stderr):
                if stream is not None:
                    try:
                        stream.close()
                    except OSError:
                        pass
            try:
                process.kill()
            except ProcessLookupError:
                pass
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                pass
        except OSError:
            for stream in (process.stdin, process.stdout, process.stderr):
                if stream is not None:
                    try:
                        stream.close()
                    except OSError:
                        pass
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                pass
        return (
            (partial_stdout or b"").decode("utf-8", errors="replace"),
            (partial_stderr or b"").decode("utf-8", errors="replace"),
            None,
            "timeout",
        )


def parse_envelope(stdout: str, stderr: str) -> dict[str, Any]:
    if not _ruby_string(stdout).strip():
        raise RunnerError(
            f"runner produced no stdout (stderr: {_ruby_string(stderr).strip()[:300]})"
        )
    try:
        envelope = _json_loads(stdout)
    except json.JSONDecodeError as error:
        first_line = str(error).splitlines()[0].strip()
        raise RunnerError(
            f"unparseable --output-format json envelope: {first_line}"
        ) from error
    if not isinstance(envelope, dict):
        raise RunnerError("envelope is not a JSON object")
    if _ruby_truthy(envelope.get("is_error")):
        raise RunnerError(_ruby_string(envelope.get("result"))[:400])
    return envelope


def extract_json(text: Any) -> Any:
    stripped = _ruby_string(text).strip()
    stripped = re.sub(r"^\x60\x60\x60(?:json)?\s*", "", stripped, count=1)
    stripped = re.sub(r"\x60\x60\x60\s*$", "", stripped, count=1)
    try:
        return _json_loads(stripped)
    except _JSONConstantError:
        raise
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", stripped, flags=re.DOTALL)
        if match is None:
            raise JudgeError("no JSON in judge output")
        return _json_loads(match.group(0))


def judge_payload(envelope: dict[str, Any]) -> Any:
    for key in ("structured_output", "structuredOutput", "structured_result", "json"):
        value = envelope.get(key)
        if isinstance(value, dict):
            return value
        if isinstance(value, str) and value.strip():
            return extract_json(value)

    result = envelope.get("result")
    if isinstance(result, dict):
        return result
    if isinstance(result, list):
        return {"verdicts": result}
    return extract_json(result)


def verdicts_from(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, dict) and isinstance(payload.get("verdicts"), list):
        return payload["verdicts"]
    if isinstance(payload, list):
        return payload
    raise JudgeError("judge JSON has no verdicts array")


def _inspect(value: Any) -> str:
    # Messages are diagnostic only; this keeps the familiar Ruby-ish spelling.
    if value is None:
        return "nil"
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False, allow_nan=False)
    return str(value)


def shape_error(
    verdicts: Any, assertions: list[dict[str, Any]]
) -> str | None:
    if not isinstance(verdicts, list):
        return "verdicts is not an array"
    if len(verdicts) != len(assertions):
        return f"expected {len(assertions)} verdicts, got {len(verdicts)}"

    numbers = [
        verdict.get("n") if isinstance(verdict, dict) else None
        for verdict in verdicts
    ]
    if (
        any(not isinstance(number, int) or isinstance(number, bool) for number in numbers)
        or sorted(numbers) != list(range(1, len(assertions) + 1))
    ):
        return (
            f"verdict n values are {_inspect(numbers)}, expected exactly "
            f"1..{len(assertions)}"
        )

    for assertion in assertions:
        verdict = next(
            (
                candidate
                for candidate in verdicts
                if isinstance(candidate, dict)
                and candidate.get("n") == assertion["n"]
            ),
            None,
        )
        if not isinstance(verdict, dict):
            return f"verdict {assertion['n']} is not an object"
        if verdict.get("kind") != assertion["kind"]:
            return (
                f"verdict {assertion['n']} kind {_inspect(verdict.get('kind'))} "
                f"disagrees with assertion kind {_inspect(assertion['kind'])}"
            )
        if verdict.get("verdict") not in ("pass", "fail", "unclear"):
            return (
                f"verdict {assertion['n']} verdict {_inspect(verdict.get('verdict'))} "
                "is not pass/fail/unclear"
            )

    return None


# ---------------------------------------------------------------------------
# argv construction
# ---------------------------------------------------------------------------

def candidate_argv(opts: dict[str, Any]) -> list[str]:
    return [
        "claude",
        "-p",
        "--output-format",
        "json",
        "--model",
        opts["model"],
        "--plugin-dir",
        ROOT,
        "--add-dir",
        ROOT,
        "--restricted",
        "--strict-mcp-config",
        "--setting-sources",
        "",
        "--no-session-persistence",
        "--disallowed-tools",
        CANDIDATE_DENY_TOOLS,
        "--exclude-dynamic-system-prompt-sections",
        "--max-budget-usd",
        f"{opts['per_run_budget']:.4f}",
    ]


def ablation_argv(opts: dict[str, Any]) -> list[str]:
    return [
        "claude",
        "-p",
        "--output-format",
        "json",
        "--model",
        opts["model"],
        "--safe-mode",
        "--restricted",
        "--strict-mcp-config",
        "--setting-sources",
        "",
        "--no-session-persistence",
        "--disallowed-tools",
        CANDIDATE_DENY_TOOLS,
        "--exclude-dynamic-system-prompt-sections",
        "--max-budget-usd",
        f"{opts['per_run_budget']:.4f}",
    ]


def judge_argv(opts: dict[str, Any], system_prompt_path: str) -> list[str]:
    return [
        "claude",
        "-p",
        "--output-format",
        "json",
        "--json-schema",
        _json_generate(JUDGE_SCHEMA),
        "--model",
        opts["judge_model"],
        "--system-prompt-file",
        system_prompt_path,
        "--tools",
        "",
        "--restricted",
        "--strict-mcp-config",
        "--setting-sources",
        "",
        "--no-session-persistence",
        "--max-budget-usd",
        JUDGE_BUDGET_USD,
    ]


def display_argv(argv: list[str]) -> str:
    rendered: list[str] = []
    for raw in argv:
        part = _ruby_string(raw)
        if len(part) > 120 and part.startswith("{"):
            rendered.append(
                "'<json-schema "
                f"{len(part)} chars, sha {_sha256_text(part)[:8]}>'"
            )
        else:
            rendered.append(shlex.quote(part))
    return " ".join(rendered)


# ---------------------------------------------------------------------------
# Provenance preflight
# ---------------------------------------------------------------------------

INSTALL_ROOT_CANDIDATES = [
    "~/.claude/skills",
    "~/.config/claude/skills",
    "~/.agents/skills",
    "~/.cursor/skills",
    "~/.cursor/skills-cursor",
    "~/.codex/skills",
    "~/.claude/plugins/cache",
    "~/.claude/plugins/marketplaces",
    "/usr/local/share/claude/skills",
    "/opt/homebrew/share/claude/skills",
]


def installed_skill_paths(skill_name: str) -> list[str]:
    found: list[str] = []
    for raw_root in INSTALL_ROOT_CANDIDATES:
        base = os.path.abspath(os.path.expanduser(raw_root))
        if not os.path.isdir(base):
            continue
        patterns = [
            os.path.join(base, skill_name, "SKILL.md"),
            os.path.join(base, "*", skill_name, "SKILL.md"),
            os.path.join(base, "*", "*", skill_name, "SKILL.md"),
            os.path.join(base, "*", "*", "*", skill_name, "SKILL.md"),
        ]
        for pattern in patterns:
            found.extend(str(path) for path in __import__("glob").glob(pattern))

    unique: list[str] = []
    for path in found:
        try:
            path = os.path.realpath(path)
        except OSError:
            pass
        if path not in unique:
            unique.append(path)
    working_path = os.path.join(ROOT, skill_name, "SKILL.md")
    return [
        path
        for path in unique
        if path != working_path and os.path.isfile(path)
    ]


def strip_frontmatter(text: str) -> str:
    match = re.match(r"\A---\n.*?\n---\n", text, flags=re.DOTALL)
    return text[match.end() :] if match else text


def _ruby_chomp_line(line: str) -> str:
    if line.endswith("\r\n"):
        return line[:-2]
    if line.endswith("\n") or line.endswith("\r"):
        return line[:-1]
    return line


PROVENANCE_PREFIX_WORDS = 8
PROVENANCE_NEEDLE_WORDS = 14
PROVENANCE_NEEDLE_MIN_CHARS = 40


def quotable_line(line: str) -> bool:
    if len(line) < 80:
        return False
    if re.search(r"[─-╿]", line):
        return False
    if "\x60\x60\x60" in line or "|" in line:
        return False
    if re.match(r"\s*#", line):
        return False
    if re.match(r"\s{4,}", line):
        return False
    if not re.search(r"[a-z]{4}", line):
        return False
    return len(normalize_loose(line).split()) >= (
        PROVENANCE_PREFIX_WORDS + PROVENANCE_NEEDLE_WORDS
    )


def choose_needle(line: str, installed_blobs: list[str]) -> str | None:
    words = normalize_loose(line).split()
    start = PROVENANCE_PREFIX_WORDS
    while start + PROVENANCE_NEEDLE_WORDS <= len(words):
        needle = " ".join(words[start : start + PROVENANCE_NEEDLE_WORDS])
        if len(needle) >= PROVENANCE_NEEDLE_MIN_CHARS and all(
            needle not in blob for blob in installed_blobs
        ):
            return needle
        start += 1
    return None


def build_provenance_plan(skill_name: str) -> dict[str, Any]:
    working_path = os.path.join(ROOT, skill_name, "SKILL.md")
    plan: dict[str, Any] = {
        "skill": skill_name,
        "working_tree_path": working_path,
        "working_tree_sha256": None,
        "installed_copies": [],
        "status": "moot",
        "discriminator": None,
        "prefix": None,
        "needle": None,
        "note": None,
    }
    if not os.path.isfile(working_path):
        plan["status"] = "undecidable"
        plan["note"] = f"working tree has no {skill_name}/SKILL.md"
        return plan

    working_text = _read_utf8_file(working_path)
    plan["working_tree_sha256"] = _sha256_text(working_text)

    installed = installed_skill_paths(skill_name)
    divergent_texts: list[str] = []
    for path in installed:
        try:
            text = _read_utf8_file(path)
        except OSError:
            text = None
        identical = text is not None and _sha256_text(text) == plan["working_tree_sha256"]
        plan["installed_copies"].append(
            {
                "path": path,
                "sha256": _sha256_text(text) if text is not None else None,
                "identical_to_working_tree": identical,
            }
        )
        if not identical:
            divergent_texts.append(_ruby_string(text))

    if not divergent_texts:
        plan["note"] = (
            "no installed copy found"
            if not installed
            else "every installed copy is byte-identical to the working tree"
        )
        return plan

    installed_blobs = [normalize_loose(text) for text in divergent_texts]
    sibling_blobs: list[str] = []
    for sibling in ALL_SKILLS:
        if sibling == skill_name:
            continue
        sibling_path = os.path.join(ROOT, sibling, "SKILL.md")
        if os.path.isfile(sibling_path):
            sibling_blobs.append(normalize_loose(_read_utf8_file(sibling_path)))

    candidates = [
        _ruby_chomp_line(line)
        for line in strip_frontmatter(working_text).splitlines(keepends=True)
        if quotable_line(_ruby_chomp_line(line))
    ]
    candidates.sort(key=len, reverse=True)

    chosen = None
    needle = None
    unique_to_skill = False
    for corpus, is_unique in (
        (installed_blobs + sibling_blobs, True),
        (installed_blobs, False),
    ):
        for line in candidates:
            found = choose_needle(line, corpus)
            if found is not None:
                chosen = line
                needle = found
                unique_to_skill = is_unique
                break
        if chosen is not None:
            break

    if chosen is None:
        plan["status"] = "undecidable"
        plan["note"] = (
            f"{len(plan['installed_copies'])} installed copy/copies diverge from the "
            "working tree, but no working-tree-only span of prose was found in "
            "SKILL.md to probe with"
        )
        return plan

    plan["status"] = "pending"
    plan["discriminator"] = chosen
    plan["prefix"] = " ".join(normalize_loose(chosen).split()[:PROVENANCE_PREFIX_WORDS])
    plan["needle"] = needle
    plan["needle_unique_to_skill"] = unique_to_skill
    shared_note = (
        " and only in this Skill"
        if unique_to_skill
        else " (shared with a sibling Skill's working tree)"
    )
    plan["note"] = (
        f"{len(plan['installed_copies'])} installed copy/copies diverge; probing with "
        f"a {PROVENANCE_NEEDLE_WORDS}-word span that exists only in the working tree"
        f"{shared_note}"
    )
    return plan


def render_provenance_prompt(
    skill_name: str, prefix: str, plugin_name: str
) -> str:
    lines = [
        f"/{plugin_name}:{skill_name} PROVENANCE CHECK. Do not run an audit. Do not read any files.",
        "One line of your loaded instructions contains this phrase:",
        f"  {prefix}",
        "Reply with that entire line, copied verbatim from your instructions, on a single",
        "line, and nothing else.",
        "If your instructions contain no such phrase, reply with exactly: ABSENT",
    ]
    return "\n".join(lines) + "\n"


def provenance_satisfied(response: str, needle: str) -> bool:
    answer = normalize_loose(response)
    return bool(answer and answer != "ABSENT" and needle in answer)


# ---------------------------------------------------------------------------
# Fixtures and rows
# ---------------------------------------------------------------------------

def canonical_fixture_yaml(fixture: dict[str, Any]) -> str:
    ordered = {key: fixture[key] for key in sorted(fixture)}
    # Psych's default emitter starts with a document marker and wraps at 80
    # columns. These options produce the same canonical bytes for fixture
    # mappings while still using PyYAML's safe emitter.
    return yaml.safe_dump(
        ordered,
        sort_keys=False,
        default_flow_style=False,
        allow_unicode=True,
        width=80,
        explicit_start=True,
    )


def load_yaml(path: str) -> Any:
    return safe_load(_read_utf8_file(path))


def load_fixtures(path: str) -> list[dict[str, Any]]:
    fixtures = load_yaml(path)
    if not isinstance(fixtures, list):
        raise ValueError(f"{path}: expected a top-level list of fixtures")

    for index, fixture in enumerate(fixtures):
        if not isinstance(fixture, dict):
            raise ValueError(f"{path}: fixture {index + 1} is not a mapping")
        for key in ("id", "skill", "mode", "scenario"):
            value = fixture.get(key)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{path}: fixture {index + 1} needs a {key}")
        if fixture["mode"] not in SUPPORTED_MODES:
            raise ValueError(
                f"{path}: fixture {fixture['id']} mode must be one of "
                f"{', '.join(SUPPORTED_MODES)}"
            )
        for key in ("evidence", "expected", "reject"):
            value = fixture.get(key)
            valid = (
                isinstance(value, list)
                and bool(value)
                and all(isinstance(item, str) and item.strip() for item in value)
            )
            if not valid:
                raise ValueError(
                    f"{path}: fixture {fixture['id']} needs a non-empty {key} list"
                )
    return fixtures


def build_assertions(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    assertions = [
        {"kind": "expected", "text": text} for text in fixture["expected"]
    ]
    assertions.extend({"kind": "reject", "text": text} for text in fixture["reject"])
    for index, assertion in enumerate(assertions):
        assertion["n"] = index + 1
    return assertions


def assertions_index(
    assertions: list[dict[str, Any]], assertion: dict[str, Any]
) -> int:
    return assertions.index(assertion)


def assertion_label(
    assertions: list[dict[str, Any]], assertion: dict[str, Any]
) -> str:
    kind_letter = "E" if assertion["kind"] == "expected" else "R"
    index = assertions_index(assertions, assertion)
    ordinal = sum(
        other["kind"] == assertion["kind"] for other in assertions[:index]
    ) + 1
    return f"{kind_letter}{ordinal}"


def expand_rows(
    fixtures: list[dict[str, Any]], opts: dict[str, Any], plugin_name: str
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for fixture in fixtures:
        declared = fixture["skill"]
        skills = LOCAL_SKILLS if declared == "shared" else (declared,)
        for skill_name in skills:
            label = (
                f"{fixture['id']} [shared -> {skill_name}]"
                if declared == "shared"
                else fixture["id"]
            )
            rows.append(
                {
                    "id": fixture["id"],
                    "label": label,
                    "slug": (
                        f"{fixture['id']}.{skill_name}"
                        if declared == "shared"
                        else fixture["id"]
                    ),
                    "declared_skill": declared,
                    "skill": skill_name,
                    "mode": fixture["mode"],
                    "scenario": fixture["scenario"],
                    "evidence": fixture["evidence"],
                    "assertions": build_assertions(fixture),
                    "fixture_sha256": _sha256_text(canonical_fixture_yaml(fixture)),
                    "prompt": None,
                    "prompt_sha256": None,
                }
            )

    for row in rows:
        prompt = render_candidate_prompt(
            row["skill"],
            row["mode"],
            row["scenario"],
            row["evidence"],
            opts["invoke"],
            plugin_name,
        )
        row["prompt"] = prompt
        row["prompt_sha256"] = _sha256_text(prompt)
        # The ablation arm carries the same body without the slash invocation.
        ablation = render_candidate_prompt(
            row["skill"],
            row["mode"],
            row["scenario"],
            row["evidence"],
            "auto",
            plugin_name,
        )
        row["ablation_prompt"] = ablation
        row["ablation_prompt_sha256"] = _sha256_text(ablation)
    return rows


def filter_rows(rows: list[dict[str, Any]], opts: dict[str, Any]) -> list[dict[str, Any]]:
    selected = rows
    if opts["skills"]:
        wanted: set[str] = set()
        for name in opts["skills"]:
            if name == "shared":
                wanted.update(LOCAL_SKILLS)
                wanted.add("shared")
            else:
                wanted.add(name)
        selected = [
            row
            for row in selected
            if row["skill"] in wanted or row["declared_skill"] in wanted
        ]
    if opts["ids"]:
        selected = [
            row
            for row in selected
            if any(fnmatch.fnmatchcase(row["id"].casefold(), pattern.casefold()) for pattern in opts["ids"])
        ]
    return selected


# ---------------------------------------------------------------------------
# Option parsing
# ---------------------------------------------------------------------------

def _finite_float(value: str) -> float:
    try:
        parsed = float(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            f"expected a floating-point number, got {value!r}"
        ) from error
    if not math.isfinite(parsed):
        raise argparse.ArgumentTypeError(
            f"expected a finite floating-point number, got {value!r}"
        )
    return parsed


def default_options() -> dict[str, Any]:
    return {
        "skills": [],
        "ids": [],
        "repeat": 3,
        "model": DEFAULT_MODEL,
        "judge_model": DEFAULT_JUDGE_MODEL,
        "allow_self_judge": False,
        "invoke": "slash",
        "ablation": False,
        "control": None,
        "control_given": False,
        "calibrate": False,
        "json_path": None,
        "out_dir": None,
        "dry_run": False,
        "jobs": 2,
        "timeout": 300,
        "max_cost": None,
        "per_run_budget": 0.50,
        "fail_under": 1.0,
        "runner": "claude",
        "allow_ci": False,
        "verbose": False,
    }


def option_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="scripts/eval.py",
        usage="Usage: scripts/eval.py [options]",
        description=(
            "Opt-in behavioral evaluation. Costs model tokens. "
            "Never run from CI or verify.py."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--skill",
        dest="skills",
        action="append",
        default=[],
        metavar="NAME",
        help='Filter on the fixture skill field (repeatable); "shared" means the four locals',
    )
    parser.add_argument(
        "--id",
        dest="ids",
        action="append",
        default=[],
        metavar="GLOB",
        help="fnmatch against the fixture id (repeatable)",
    )
    parser.add_argument("--repeat", type=int, default=3, metavar="N", help="Repeats per row (default 3)")
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        metavar="NAME",
        help=f"Candidate model, pinned full dated id (default {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--judge-model",
        dest="judge_model",
        default=DEFAULT_JUDGE_MODEL,
        metavar="NAME",
        help=f"Judge model (default {DEFAULT_JUDGE_MODEL})",
    )
    parser.add_argument(
        "--allow-self-judge",
        dest="allow_self_judge",
        action="store_true",
        help="Permit judge model == candidate model",
    )
    parser.add_argument(
        "--invoke",
        choices=("slash", "auto"),
        default="slash",
        metavar="MODE",
        help="slash (default) tests the Skill body; auto tests description triggering",
    )
    parser.add_argument(
        "--ablation",
        action="store_true",
        help="Add the no-Skill baseline arm and report NO SIGNAL rows",
    )
    parser.add_argument(
        "--control",
        nargs="?",
        const=2,
        type=int,
        default=None,
        metavar="N",
        help="Decoy-transcript judge control (default 2 when --ablation is on)",
    )
    parser.add_argument(
        "--calibrate",
        action="store_true",
        help="Grade tests/judge-calibration/*.yml instead of the fixtures",
    )
    parser.add_argument(
        "--json",
        dest="json_path",
        metavar="PATH",
        help="Write the machine artifact here instead of <out>/eval.json",
    )
    parser.add_argument(
        "--out",
        dest="out_dir",
        metavar="DIR",
        help="Output directory (default tests/results/<UTC timestamp>)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Render every prompt and argv, run nothing, exit 0",
    )
    parser.add_argument(
        "--jobs",
        type=int,
        default=2,
        metavar="N",
        help="Parallel model calls (default 2, capped at 8)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        metavar="SEC",
        help="Per model call timeout (default 300)",
    )
    parser.add_argument(
        "--max-cost-usd",
        dest="max_cost",
        type=_finite_float,
        metavar="X",
        help="Abort once summed total_cost_usd crosses this",
    )
    parser.add_argument(
        "--per-run-budget-usd",
        dest="per_run_budget",
        type=_finite_float,
        default=0.50,
        metavar="X",
        help="Per candidate call budget (default 0.50)",
    )
    parser.add_argument(
        "--fail-under",
        dest="fail_under",
        type=_finite_float,
        default=1.0,
        metavar="RATE",
        help="Per-assertion pass rate below which a row fails (default 1.0)",
    )
    parser.add_argument(
        "--runner",
        choices=("claude", "codex", "cursor"),
        default="claude",
        metavar="NAME",
        help="Runner CLI (default claude)",
    )
    parser.add_argument(
        "--allow-ci",
        dest="allow_ci",
        action="store_true",
        help='Required to run when ENV["CI"] is set',
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print full prompts and per-run detail",
    )
    return parser


def parse_options(argv: list[str] | None = None) -> dict[str, Any]:
    namespace = option_parser().parse_args(argv)
    opts = vars(namespace)
    opts["control_given"] = opts["control"] is not None
    opts["jobs"] = 1 if opts["jobs"] < 1 else 8 if opts["jobs"] > 8 else opts["jobs"]
    opts["repeat"] = 1 if opts["repeat"] < 1 else opts["repeat"]
    if not opts["control_given"]:
        opts["control"] = 2 if opts["ablation"] else 0
    if opts["control"] is None:
        opts["control"] = 0
    return opts


# ---------------------------------------------------------------------------
# Environment facts and calibration data
# ---------------------------------------------------------------------------

def detect_cli_version() -> str:
    try:
        out, _err, status, state = spawn_capture(
            ["claude", "--version"], "", 30, tempfile.gettempdir()
        )
    except RunnerError:
        return "unavailable"
    if state != "ok" or status != 0:
        return "unknown"
    return out.strip() if out.strip() else "unknown"


def git_fact(args: list[str]) -> str | None:
    try:
        out, _err, status, state = spawn_capture(
            ["git"] + args, "", 30, ROOT
        )
    except RunnerError:
        return None
    return out if state == "ok" and status == 0 else None


def _time_stamp(dt: _datetime.datetime) -> str:
    return dt.strftime("%Y%m%dT%H%M%SZ")


def _time_iso(dt: _datetime.datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def _time_ruby_string(dt: _datetime.datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S UTC")


def _expand_path(path: str) -> str:
    return os.path.abspath(os.path.expanduser(path))


def _root_relative(path: str) -> str:
    prefix = ROOT + os.sep
    return path[len(prefix) :] if path.startswith(prefix) else path


def load_calibration_cases() -> list[dict[str, Any]]:
    calibration_cases: list[dict[str, Any]] = []
    paths = sorted(
        str(path)
        for path in Path(CALIBRATION_DIR).glob("*.yml")
    )
    for path in paths:
        try:
            raw = load_yaml(path)
        except yaml.YAMLError as error:
            first_line = str(error).splitlines()[0].strip()
            raise ValueError(f"{path}: {first_line}") from error
        if not isinstance(raw, dict) or not isinstance(raw.get("assertions"), list):
            raise ValueError(f"{path}: needs an assertions list")
        transcript = raw.get("transcript")
        if transcript is None and isinstance(raw.get("transcript_path"), str):
            transcript_path = _expand_path(
                os.path.join(CALIBRATION_DIR, raw["transcript_path"])
            )
            transcript = _read_utf8_file(transcript_path)
        if not isinstance(transcript, str) or not transcript.strip():
            raise ValueError(f"{path}: needs a transcript or transcript_path")
        assertions = []
        for index, item in enumerate(raw["assertions"]):
            assertions.append(
                {
                    "n": index + 1,
                    "kind": item.get("kind"),
                    "text": item.get("text"),
                    "label": item.get("verdict"),
                }
            )
        fallback_id = Path(path).stem
        case_id = raw.get("id") if _ruby_truthy(raw.get("id")) else fallback_id
        calibration_cases.append(
            {
                "id": case_id,
                "path": path,
                "transcript": transcript,
                "assertions": assertions,
            }
        )
    return calibration_cases


def plan_control_pairs(
    rows: list[dict[str, Any]], sample: int | None
) -> list[dict[str, Any]]:
    if sample is None or sample <= 0:
        return []
    by_skill: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_skill.setdefault(row["skill"], []).append(row)

    pairs: list[dict[str, Any]] = []
    for row in sorted(rows, key=lambda candidate: candidate["label"]):
        if len(pairs) >= sample:
            break
        partner = next(
            (
                other
                for other in by_skill[row["skill"]]
                if other["slug"] != row["slug"]
            ),
            None,
        )
        if partner is None:
            continue
        pairs.append(
            {
                "id": row["label"],
                "slug": row["slug"],
                "decoy_id": partner["label"],
                "decoy_slug": partner["slug"],
            }
        )
    return pairs


def print_block(text: Any, indent: str) -> None:
    for line in _ruby_string(text).splitlines():
        print(f"{indent}{line}")


# ---------------------------------------------------------------------------
# Aggregation helpers
# ---------------------------------------------------------------------------

def tally_arm(
    units_for_arm: list[dict[str, Any]], row: dict[str, Any]
) -> dict[int, dict[str, Any]]:
    counts: dict[int, dict[str, Any]] = {
        assertion["n"]: {
            "pass": 0,
            "fail": 0,
            "unclear": 0,
            "missing": 0,
            "failures": [],
        }
        for assertion in row["assertions"]
    }

    for unit in units_for_arm:
        judge = unit.get("judge")
        if judge is None or judge.get("error"):
            for bucket in counts.values():
                bucket["missing"] += 1
            continue
        for verdict in judge["verdicts"]:
            bucket = counts.get(verdict.get("n"))
            if bucket is None:
                continue
            call = verdict.get("verdict")
            bucket[call] = bucket.get(call, 0) + 1
            if call != "pass" and len(bucket["failures"]) < 3:
                excerpt = _ruby_string(verdict.get("excerpt")).strip()
                if not excerpt:
                    excerpt = _ruby_string(verdict.get("reason")).strip()
                bucket["failures"].append(
                    f"run {unit['run']} {call}: {excerpt[:120]}"
                )
    return counts


def aggregate_report_rows(
    rows: list[dict[str, Any]],
    unit_results: list[dict[str, Any]],
    opts: dict[str, Any],
) -> list[dict[str, Any]]:
    report_rows: list[dict[str, Any]] = []
    for row in rows:
        own = [
            unit
            for unit in unit_results
            if unit["row"]["slug"] == row["slug"]
        ]
        with_units = [
            unit
            for unit in own
            if unit["arm"] == "with-skill" and "skipped" not in unit
        ]
        without_units = [
            unit
            for unit in own
            if unit["arm"] == "no-skill" and "skipped" not in unit
        ]

        with_counts = tally_arm(with_units, row)
        attempted = len(with_units)
        judged = sum(
            unit.get("judge") is not None and not unit["judge"].get("error")
            for unit in with_units
        )
        assertion_rows: list[dict[str, Any]] = []
        for assertion in row["assertions"]:
            bucket = with_counts[assertion["n"]]
            denominator = judged
            rate = 0.0 if denominator == 0 else bucket["pass"] / denominator
            unclear_rate = (
                0.0 if denominator == 0 else bucket["unclear"] / denominator
            )
            assertion_rows.append(
                {
                    "n": assertion["n"],
                    "kind": assertion["kind"],
                    "text": assertion["text"],
                    "label": assertion_label(row["assertions"], assertion),
                    "pass": bucket["pass"],
                    "fail": bucket["fail"],
                    "unclear": bucket["unclear"],
                    "missing": bucket["missing"],
                    "denominator": denominator,
                    "rate": _ruby_round(rate),
                    "ambiguous_assertion": unclear_rate > (1.0 / 3.0),
                    "failures": bucket["failures"],
                }
            )

        expected_rows = [
            entry for entry in assertion_rows if entry["kind"] == "expected"
        ]
        with_rate = (
            0.0
            if not expected_rows
            else sum(entry["rate"] for entry in expected_rows) / len(expected_rows)
        )

        without_rate: float | None = None
        if opts["ablation"]:
            without_counts = tally_arm(without_units, row)
            judged_without = sum(
                unit.get("judge") is not None
                and not unit["judge"].get("error")
                for unit in without_units
            )
            expected_assertions = [
                assertion
                for assertion in row["assertions"]
                if assertion["kind"] == "expected"
            ]
            if judged_without != 0 and expected_assertions:
                rates = [
                    without_counts[assertion["n"]]["pass"] / judged_without
                    for assertion in expected_assertions
                ]
                without_rate = _ruby_round(sum(rates) / len(rates))

        if attempted == 0 or judged == 0 or judged < attempted:
            status = "ERROR"
        elif any(entry["pass"] == 0 for entry in assertion_rows):
            status = "FAIL"
        elif without_rate is not None and without_rate >= opts["fail_under"]:
            status = "NO SIGNAL"
        elif any(entry["pass"] < entry["denominator"] for entry in assertion_rows):
            status = "FLAKY"
        else:
            status = "PASS"

        runs: list[dict[str, Any]] = []
        for unit in own:
            candidate = unit.get("candidate")
            if candidate is not None:
                candidate = {
                    key: value for key, value in candidate.items() if key != "text"
                }
            runs.append(
                {
                    "run": unit["run"],
                    "arm": unit["arm"],
                    "skipped": unit.get("skipped"),
                    "candidate": candidate,
                    "judge": unit.get("judge"),
                }
            )

        report_rows.append(
            {
                "id": row["id"],
                "label": row["label"],
                "skill": row["skill"],
                "mode": row["mode"],
                "arm": "with-skill",
                "fixture_sha256": row["fixture_sha256"],
                "prompt_sha256": row["prompt_sha256"],
                "status": status.lower().replace(" ", "_"),
                "status_label": status,
                "attempted": attempted,
                "judged": judged,
                "with_rate": _ruby_round(with_rate),
                "without_rate": without_rate,
                "assertions": assertion_rows,
                "runs": runs,
            }
        )
    return report_rows


def truncate(text: str, width: int) -> str:
    return text if len(text) <= width else text[: width - 3] + "..."


def run_dry_run(
    opts: dict[str, Any],
    plugin_name: str,
    cli_version: str,
    started_at: _datetime.datetime,
    out_dir: str,
    json_path: str,
    git_sha: str,
    git_dirty: bool,
    fixtures_sha: str,
    fixtures: list[dict[str, Any]],
    all_rows: list[dict[str, Any]],
    rows: list[dict[str, Any]],
    provenance_plans: list[dict[str, Any]],
    control_pairs: list[dict[str, Any]],
    calibration_cases: list[dict[str, Any]],
) -> int:
    print("product-judgement eval --dry-run - no model calls, nothing written")
    print(
        f"candidate {opts['model']} - judge {opts['judge_model']} - "
        f"cli {cli_version} - plugin {plugin_name}"
    )
    print(
        f"{opts['repeat']} repeats - invoke={opts['invoke']} - "
        f"ablation={'on' if opts['ablation'] else 'off'} - jobs={opts['jobs']} - "
        f"timeout={opts['timeout']}s - fail-under={opts['fail_under']}"
    )
    dirty_note = " (dirty)" if git_dirty else ""
    print(
        f"fixtures {_root_relative(FIXTURE_PATH)} sha {fixtures_sha[:8]} - "
        f"git {git_sha}{dirty_note}"
    )
    print()

    print("EXCERPT VERIFIER SELF-CHECK")
    selftest = excerpt_selftest()
    for label, ok in selftest:
        print(f"  {'ok  ' if ok else 'FAIL'} {label}")
    failed = [(label, ok) for label, ok in selftest if not ok]
    if failed:
        print(
            f"scripts/eval.py: the excerpt verifier is broken ({len(failed)} "
            "self-check failure(s)). Refusing to go further.",
            file=sys.stderr,
        )
        return EXIT_HARNESS
    print()

    print("CANDIDATE PROMPT LEAK SELF-CHECK")
    prompt_selftest = all_prompt_selftests(rows, plugin_name)
    for label, ok in prompt_selftest:
        print(f"  {'ok  ' if ok else 'FAIL'} {label}")
    failed = [(label, ok) for label, ok in prompt_selftest if not ok]
    if failed:
        print(
            f"scripts/eval.py: candidate prompt leak self-check failed "
            f"({len(failed)} failure(s)). Refusing to go further.",
            file=sys.stderr,
        )
        return EXIT_HARNESS
    print()

    judge_system_path = os.path.join(out_dir, "judge-system-prompt.txt")
    print("CANDIDATE ARGV (prompt on stdin, cwd = a fresh empty scratch dir)")
    print(f"  {display_argv(candidate_argv(opts))}")
    print()
    if opts["ablation"]:
        print("ABLATION ARGV")
        print(f"  {display_argv(ablation_argv(opts))}")
        print()
    print("JUDGE ARGV (assertions + transcript on stdin)")
    print(f"  {display_argv(judge_argv(opts, judge_system_path))}")
    print(
        f"  judge system prompt sha {_sha256_text(JUDGE_SYSTEM_PROMPT)[:16]} "
        f"({len(JUDGE_SYSTEM_PROMPT)} chars, --system-prompt-file, full replacement)"
    )
    print(f"  judge json schema sha {_sha256_text(_json_generate(JUDGE_SCHEMA))[:16]}")
    print()

    print(
        f"PROVENANCE PREFLIGHT ({len(provenance_plans)} skill(s), "
        "1 model call each on a real run)"
    )
    for plan in provenance_plans:
        print(f"  {plan['skill']}: {plan['status']} - {plan['note']}")
        sha = _ruby_string(plan["working_tree_sha256"])[:12]
        print(
            f"    working tree {sha} "
            f"{_root_relative(plan['working_tree_path'])}"
        )
        for copy in plan["installed_copies"]:
            marker = "same" if copy["identical_to_working_tree"] else "DIFF"
            print(
                f"    installed    {_ruby_string(copy['sha256'])[:12]} "
                f"[{marker}] {copy['path']}"
            )
        if plan["discriminator"]:
            discriminator = plan["discriminator"]
            suffix = "..." if len(discriminator) > 140 else ""
            print(f"    discriminator line ({len(discriminator)} chars):")
            print(f"      {discriminator[:140]}{suffix}")
            print("    needle asserted in the reply (working tree only):")
            print(f"      {plan['needle']}")
            print("    probe prompt:")
            print_block(
                render_provenance_prompt(
                    plan["skill"], plan["prefix"], plugin_name
                ),
                "      ",
            )
    undecidable = [
        plan for plan in provenance_plans if plan["status"] == "undecidable"
    ]
    if undecidable:
        names = ", ".join(plan["skill"] for plan in undecidable)
        print(
            f"  WOULD ABORT (exit {EXIT_HARNESS}): provenance undecidable for "
            f"{names}"
        )
    print()

    print(
        f"ROWS ({len(rows)} of {len(all_rows)}, from {len(fixtures)} fixtures)"
    )
    for row in rows:
        expected_count = sum(
            assertion["kind"] == "expected" for assertion in row["assertions"]
        )
        reject_count = sum(
            assertion["kind"] == "reject" for assertion in row["assertions"]
        )
        print(f"  {row['label']}")
        print(
            f"    skill={row['skill']} declared={row['declared_skill']} "
            f"mode={row['mode']} assertions={len(row['assertions'])} "
            f"({expected_count} expected / {reject_count} reject)"
        )
        print(
            f"    fixture sha {row['fixture_sha256'][:12]} - prompt sha "
            f"{row['prompt_sha256'][:12]} ({len(row['prompt'])} chars)"
        )
        if opts["ablation"]:
            print(
                f"    ablation prompt sha {row['ablation_prompt_sha256'][:12]} "
                f"({len(row['ablation_prompt'])} chars)"
            )
        if opts["verbose"]:
            print("    candidate prompt:")
            print_block(row["prompt"], "      ")
            print("    judge user message:")
            print_block(
                render_judge_user_message(
                    row["assertions"],
                    f"<candidate transcript for {row['label']}>",
                ),
                "      ",
            )
    print()

    if control_pairs:
        print("JUDGE CONTROL (decoy transcripts)")
        for pair in control_pairs:
            print(
                f"  {pair['id']} graded against the transcript of "
                f"{pair['decoy_id']}"
            )
        print()

    if opts["calibrate"]:
        print(f"CALIBRATION CASES ({len(calibration_cases)})")
        for case in calibration_cases:
            print(
                f"  {case['id']} - {len(case['assertions'])} labelled assertions "
                f"- {len(case['transcript'])} char transcript - "
                f"{_root_relative(case['path'])}"
            )
        print()

    arms = 1 + (1 if opts["ablation"] else 0)
    candidate_calls = len(rows) * opts["repeat"] * arms
    judge_calls = candidate_calls + len(control_pairs) + len(calibration_cases)
    pending_probes = sum(
        plan["status"] == "pending" for plan in provenance_plans
    )
    print("WOULD RUN")
    print(f"  {pending_probes} provenance probe(s)")
    print(
        f"  {candidate_calls} candidate call(s) ({len(rows)} rows x "
        f"{opts['repeat']} repeats x {arms} arm(s))"
    )
    print(f"  {judge_calls} judge call(s)")
    ceiling = (
        "$" + f"{opts['max_cost']:.2f}"
        if opts["max_cost"] is not None
        else "none (--max-cost-usd unset)"
    )
    print(
        f"  ceiling: {ceiling} - per candidate call "
        + "$"
        + f"{opts['per_run_budget']:.2f}"
        + " - per judge call $"
        + JUDGE_BUDGET_USD
    )
    print(f"  artifact {json_path}")
    print(f"  transcripts {os.path.join(out_dir, 'runs')}/")
    gitignore_path = os.path.join(ROOT, ".gitignore")
    gitignore = ""
    if os.path.isfile(gitignore_path):
        with open(gitignore_path, encoding="utf-8") as handle:
            gitignore = handle.read()
    if "tests/results" not in gitignore:
        print(
            "  note: tests/results/ is not in .gitignore; add it before "
            "committing a real run"
        )
    print()
    print("Nothing ran. Exit 0.")
    return EXIT_OK


def run_live(
    opts: dict[str, Any],
    plugin_name: str,
    cli_version: str,
    started_at: _datetime.datetime,
    out_dir: str,
    json_path: str,
    git_sha: str,
    git_dirty: bool,
    fixtures_sha: str,
    fixtures: list[dict[str, Any]],
    all_rows: list[dict[str, Any]],
    rows: list[dict[str, Any]],
    provenance_plans: list[dict[str, Any]],
    control_pairs: list[dict[str, Any]],
    calibration_cases: list[dict[str, Any]],
) -> int:
    selftest = excerpt_selftest()
    selftest_failures = [(label, ok) for label, ok in selftest if not ok]
    if selftest_failures:
        labels = "; ".join(label for label, _ok in selftest_failures)
        print(
            f"scripts/eval.py: the excerpt verifier failed its own self-check "
            f"({labels}). Refusing to grade anything.",
            file=sys.stderr,
        )
        return EXIT_HARNESS

    prompt_selftest = all_prompt_selftests(rows, plugin_name)
    prompt_selftest_failures = [
        (label, ok) for label, ok in prompt_selftest if not ok
    ]
    if prompt_selftest_failures:
        labels = "; ".join(label for label, _ok in prompt_selftest_failures)
        print(
            f"scripts/eval.py: candidate prompt leak self-check failed "
            f"({labels}). Refusing to grade anything.",
            file=sys.stderr,
        )
        return EXIT_HARNESS

    os.makedirs(os.path.join(out_dir, "runs"), exist_ok=True)
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    judge_system_path = os.path.join(out_dir, "judge-system-prompt.txt")
    with open(judge_system_path, "w", encoding="utf-8") as handle:
        handle.write(JUDGE_SYSTEM_PROMPT)
    scratch_dir = tempfile.mkdtemp(prefix="pj-eval-")

    cost_lock = threading.Lock()
    io_lock = threading.Lock()
    results_lock = threading.Lock()
    total_cost = 0.0
    budget_exhausted = False
    harness_errors: list[str] = []

    def record_cost(amount: Any) -> None:
        nonlocal total_cost, budget_exhausted
        with cost_lock:
            total_cost += _ruby_float(amount)
            if (
                opts["max_cost"] is not None
                and total_cost >= opts["max_cost"]
            ):
                budget_exhausted = True

    def note_harness_error(message: str) -> None:
        with io_lock:
            harness_errors.append(message)
            if opts["verbose"]:
                print(f"  ! {message}", file=sys.stderr)

    def write_side_file(name: str, content: Any) -> str:
        path = os.path.join(out_dir, "runs", name)
        with io_lock:
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(_ruby_string(content))
        return os.path.join("runs", name)

    def call_candidate(
        argv: list[str], prompt: str, slug: str
    ) -> dict[str, Any]:
        try:
            stdout, stderr, status, state = spawn_capture(
                argv, prompt, opts["timeout"], scratch_dir
            )
        except RunnerError as error:
            return {
                "error": str(error),
                "cost_usd": 0.0,
                "exit_status": None,
            }
        if state == "timeout":
            return {
                "error": f"timed out after {opts['timeout']}s",
                "cost_usd": 0.0,
            }

        try:
            envelope = parse_envelope(stdout, stderr)
        except RunnerError as error:
            return {
                "error": str(error),
                "cost_usd": 0.0,
                "exit_status": status,
            }

        record_cost(envelope.get("total_cost_usd"))
        text = _ruby_string(envelope.get("result"))
        envelope_path = write_side_file(
            f"{slug}.envelope.json", _json_pretty(envelope)
        )
        text_path = write_side_file(f"{slug}.candidate.md", text)
        return {
            "session_id": envelope.get("session_id"),
            "num_turns": envelope.get("num_turns"),
            "duration_ms": envelope.get("duration_ms"),
            "cost_usd": _ruby_float(envelope.get("total_cost_usd")),
            "is_error": _ruby_truthy(envelope.get("is_error")),
            "terminal_reason": envelope.get("terminal_reason"),
            "envelope_path": envelope_path,
            "text_path": text_path,
            "text_sha256": _sha256_text(text),
            "chars": len(text),
            "text": text,
        }

    def call_judge(
        assertions: list[dict[str, Any]], candidate_text: str, slug: str
    ) -> dict[str, Any]:
        argv = judge_argv(opts, judge_system_path)
        message = render_judge_user_message(assertions, candidate_text)
        last_error: str | None = None
        raw_path: str | None = None
        cost = 0.0

        for attempt in range(2):
            try:
                stdout, stderr, _status, state = spawn_capture(
                    argv, message, opts["timeout"], scratch_dir
                )
            except RunnerError as error:
                last_error = f"judge runner error: {error}"
                continue
            if state == "timeout":
                last_error = f"judge timed out after {opts['timeout']}s"
                continue

            try:
                envelope = parse_envelope(stdout, stderr)
            except RunnerError as error:
                last_error = f"judge runner error: {error}"
                continue

            record_cost(envelope.get("total_cost_usd"))
            amount = _ruby_float(envelope.get("total_cost_usd"))
            cost += amount
            suffix = "" if attempt == 0 else ".retry"
            raw_path = write_side_file(
                f"{slug}.judge{suffix}.json", _json_pretty(envelope)
            )

            try:
                verdicts = verdicts_from(judge_payload(envelope))
            except (JudgeError, json.JSONDecodeError) as error:
                last_error = f"judge JSON unusable: {error}"
                continue

            problem = shape_error(verdicts, assertions)
            if problem:
                last_error = f"judge shape error: {problem}"
                continue

            fabricated, empties = adjudicate_verdicts(verdicts, candidate_text)
            return {
                "session_id": envelope.get("session_id"),
                "cost_usd": cost,
                "raw_path": raw_path,
                "attempts": attempt + 1,
                "verdicts": sorted(verdicts, key=lambda verdict: verdict["n"]),
                "fabricated_excerpts": fabricated,
                "empty_excerpt_downgrades": empties,
            }

        return {
            "error": last_error or "judge produced nothing usable",
            "cost_usd": cost,
            "raw_path": raw_path,
        }

    # --- provenance preflight ---------------------------------------------
    provenance_undecidable = [
        plan for plan in provenance_plans if plan["status"] == "undecidable"
    ]
    if provenance_undecidable:
        print(
            "scripts/eval.py: cannot prove the working tree is what would be loaded.",
            file=sys.stderr,
        )
        for plan in provenance_undecidable:
            print(f"  {plan['skill']}: {plan['note']}", file=sys.stderr)
        print(file=sys.stderr)
        print(
            "This machine has these Skills installed globally. If --plugin-dir "
            "loses to an installed",
            file=sys.stderr,
        )
        print(
            "copy, this harness grades the last release and reports green on code "
            "you just changed.",
            file=sys.stderr,
        )
        print(
            "Use an isolated test installation whose source can be identified. "
            "Preserve existing",
            file=sys.stderr,
        )
        print(
            "installations; do not change Skill prose solely to make this probe pass.",
            file=sys.stderr,
        )
        return EXIT_HARNESS

    for plan in provenance_plans:
        if plan["status"] != "pending":
            continue
        prompt = render_provenance_prompt(
            plan["skill"], plan["prefix"], plugin_name
        )
        result = call_candidate(
            candidate_argv(opts), prompt, f"provenance.{plan['skill']}"
        )
        if result.get("error"):
            plan["status"] = "runner-error"
            plan["note"] = f"provenance probe failed: {result['error']}"
            continue

        plan["response_path"] = result["text_path"]
        if provenance_satisfied(result["text"], plan["needle"]):
            plan["status"] = "proven"
            plan["note"] = (
                "the loaded instructions contained a span of prose that exists "
                "only in the working tree"
            )
        else:
            plan["status"] = "unproven"
            plan["note"] = (
                "the loaded Skill could not reproduce the working-tree-only span; "
                "an installed copy probably won precedence over --plugin-dir"
            )

    unproven = [
        plan
        for plan in provenance_plans
        if plan["status"] in ("unproven", "runner-error")
    ]
    if unproven:
        print(
            "scripts/eval.py: provenance preflight FAILED for "
            + ", ".join(plan["skill"] for plan in unproven)
            + ".",
            file=sys.stderr,
        )
        for plan in unproven:
            print(f"  {plan['skill']}: {plan['note']}", file=sys.stderr)
        print(file=sys.stderr)
        if any(plan["status"] == "runner-error" for plan in unproven):
            print(
                "No behavioral output was graded. Resolve the reported runner or "
                "authentication error",
                file=sys.stderr,
            )
            print(
                "before retrying; a failed call is not evidence of an "
                "installation-precedence problem.",
                file=sys.stderr,
            )
        else:
            print(
                "No behavioral output was graded because working-tree provenance "
                "was not established.",
                file=sys.stderr,
            )
            print(
                "Inspect plugin resolution or use an isolated test installation; "
                "preserve existing copies.",
                file=sys.stderr,
            )
        preflight_path = os.path.join(out_dir, "preflight.json")
        preflight = {
            "status": "harness-error",
            "started_at": _time_ruby_string(started_at),
            "candidate_model": opts["model"],
            "provenance": provenance_plans,
        }
        with open(preflight_path, "w", encoding="utf-8") as handle:
            handle.write(_json_pretty(preflight) + "\n")
        print(f"Artifact of the failed preflight: {out_dir}", file=sys.stderr)
        return EXIT_HARNESS

    # --- work units --------------------------------------------------------
    units: list[dict[str, Any]] = []
    for row in rows:
        arms = [
            (
                "with-skill",
                candidate_argv(opts),
                row["prompt"],
                row["prompt_sha256"],
            )
        ]
        if opts["ablation"]:
            arms.append(
                (
                    "no-skill",
                    ablation_argv(opts),
                    row["ablation_prompt"],
                    row["ablation_prompt_sha256"],
                )
            )
        for arm_name, argv, prompt, prompt_sha in arms:
            for index in range(opts["repeat"]):
                units.append(
                    {
                        "row": row,
                        "arm": arm_name,
                        "argv": argv,
                        "prompt": prompt,
                        "prompt_sha256": prompt_sha,
                        "run": index + 1,
                    }
                )

    unit_results: list[dict[str, Any]] = []
    queue: Queue[dict[str, Any]] = Queue()
    for unit in units:
        queue.put(unit)

    def worker() -> None:
        nonlocal budget_exhausted
        while True:
            try:
                unit = queue.get_nowait()
            except Empty:
                return
            try:
                with cost_lock:
                    exhausted = budget_exhausted
                if exhausted:
                    result = {
                        **unit,
                        "skipped": "cost ceiling reached before this run started",
                    }
                    with results_lock:
                        unit_results.append(result)
                    continue

                row = unit["row"]
                slug = f"{row['slug']}.{unit['arm']}.{unit['run']}"
                candidate = call_candidate(
                    unit["argv"], unit["prompt"], slug
                )
                if candidate.get("error"):
                    note_harness_error(
                        f"{row['label']} {unit['arm']} run {unit['run']}: "
                        f"{candidate['error']}"
                    )
                    result = {**unit, "candidate": candidate, "judge": None}
                    with results_lock:
                        unit_results.append(result)
                    continue

                judge = call_judge(row["assertions"], candidate["text"], slug)
                if judge.get("error"):
                    note_harness_error(
                        f"{row['label']} {unit['arm']} run {unit['run']}: "
                        f"{judge['error']}"
                    )
                result = {
                    **unit,
                    "candidate": candidate,
                    "judge": judge,
                }
                with results_lock:
                    unit_results.append(result)
            finally:
                queue.task_done()

    thread_count = min(opts["jobs"], len(units))
    threads = [
        threading.Thread(target=worker, name=f"eval-worker-{index}")
        for index in range(thread_count)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    # --- decoy control -----------------------------------------------------
    transcript_by_slug: dict[str, str] = {}
    for unit in unit_results:
        if unit["arm"] != "with-skill":
            continue
        candidate = unit.get("candidate")
        if candidate is None or candidate.get("error"):
            continue
        transcript_by_slug.setdefault(unit["row"]["slug"], candidate["text"])

    control_results: list[dict[str, Any]] = []
    for pair in control_pairs:
        decoy_text = transcript_by_slug.get(pair["decoy_slug"])
        row = next(
            (candidate_row for candidate_row in rows if candidate_row["slug"] == pair["slug"]),
            None,
        )
        if decoy_text is None or row is None:
            control_results.append(
                {**pair, "skipped": "no usable decoy transcript"}
            )
            continue

        judge = call_judge(
            row["assertions"], decoy_text, f"control.{pair['slug']}"
        )
        if judge.get("error"):
            note_harness_error(
                f"judge control {pair['id']}: {judge['error']}"
            )
            control_results.append({**pair, "error": judge["error"]})
            continue

        expected_count = sum(
            assertion["kind"] == "expected" for assertion in row["assertions"]
        )
        decoy_passes = sum(
            verdict["kind"] == "expected" and verdict["verdict"] == "pass"
            for verdict in judge["verdicts"]
        )
        control_results.append(
            {
                **pair,
                "expected_assertions": expected_count,
                "decoy_passes": decoy_passes,
                "leak": decoy_passes > 0,
                "raw_path": judge["raw_path"],
            }
        )

    # --- calibration -------------------------------------------------------
    calibration_results: list[dict[str, Any]] = []
    for case in calibration_cases:
        judge = call_judge(
            case["assertions"],
            case["transcript"],
            f"calibration.{case['id']}",
        )
        if judge.get("error"):
            note_harness_error(
                f"calibration {case['id']}: {judge['error']}"
            )
            calibration_results.append(
                {"id": case["id"], "error": judge["error"]}
            )
            continue

        agree = 0
        detail: list[dict[str, Any]] = []
        for assertion in case["assertions"]:
            verdict = next(
                (
                    candidate
                    for candidate in judge["verdicts"]
                    if candidate["n"] == assertion["n"]
                ),
                None,
            )
            got = verdict.get("verdict") if verdict is not None else None
            matched = (
                assertion.get("label") is not None
                and got == assertion["label"]
            )
            if matched:
                agree += 1
            detail.append(
                {
                    "n": assertion["n"],
                    "label": assertion.get("label"),
                    "judge": got,
                    "agrees": matched,
                }
            )
        calibration_results.append(
            {
                "id": case["id"],
                "assertions": len(case["assertions"]),
                "agreements": agree,
                "rate": _ruby_round(
                    agree / len(case["assertions"])
                ),
                "verdicts": detail,
                "raw_path": judge["raw_path"],
            }
        )

    # --- aggregation -------------------------------------------------------
    report_rows = aggregate_report_rows(rows, unit_results, opts)

    # --- human report ------------------------------------------------------
    finished_at = _datetime.datetime.now(_datetime.timezone.utc)
    duration_s = int((finished_at - started_at).total_seconds() + 0.5)
    print(
        f"product-judgement eval - candidate {opts['model']} - "
        f"judge {opts['judge_model']} - plugin {plugin_name}"
    )
    print(
        f"{opts['repeat']} repeats - invoke={opts['invoke']} - "
        f"ablation={'on' if opts['ablation'] else 'off'} - cli {cli_version} - "
        f"fixtures sha {fixtures_sha[:8]} - {_time_iso(started_at)}"
    )
    print()

    for entry in report_rows:
        # The row number is the worst assertion's k over the judged repeats.
        worst = min(
            (assertion["pass"] for assertion in entry["assertions"]),
            default=0,
        )
        denominator = (
            entry["judged"]
            if not entry["assertions"]
            else entry["assertions"][0]["denominator"]
        )
        print(
            f"{truncate(entry['label'], 60):<60}  "
            f"{worst}/{denominator}  {entry['status_label']}"
        )
        if entry["judged"] < entry["attempted"]:
            print(
                f"     {entry['attempted'] - entry['judged']} of "
                f"{entry['attempted']} repeats produced nothing judgeable"
            )
        for assertion in entry["assertions"]:
            marker = ""
            if (
                assertion["pass"] > 0
                and assertion["pass"] < assertion["denominator"]
            ):
                marker = "  <- flaky"
            if assertion["pass"] == 0:
                marker = "  <- zero"
            if assertion["ambiguous_assertion"]:
                marker += "  <- ambiguous_assertion"
            print(
                f"  {assertion['label']:<2} "
                f"{truncate(assertion['text'], 64):<64} "
                f"{assertion['pass']}/{assertion['denominator']}{marker}"
            )
            for line in assertion["failures"]:
                print(f"     {truncate(line, 100)}")
        print()

    status_counts = {
        "PASS": 0,
        "FLAKY": 0,
        "FAIL": 0,
        "ERROR": 0,
        "NO SIGNAL": 0,
    }
    for entry in report_rows:
        status_counts[entry["status_label"]] += 1

    if not opts["calibrate"]:
        print(
            f"{len(report_rows)} rows - {status_counts['PASS']} pass - "
            f"{status_counts['FLAKY']} flaky - {status_counts['FAIL']} fail - "
            f"{status_counts['ERROR']} error - "
            f"{status_counts['NO SIGNAL']} no signal"
        )

    if opts["calibrate"]:
        pass
    elif opts["ablation"]:
        no_signal = [
            entry for entry in report_rows if entry["status_label"] == "NO SIGNAL"
        ]
        gated = len(report_rows) - len(no_signal)
        detail = (
            ""
            if not no_signal
            else " (" + ", ".join(entry["label"] for entry in no_signal) + ")"
        )
        print(
            f"ablation:      {gated} gated on the skill - "
            f"{len(no_signal)} NO SIGNAL{detail}"
        )
    else:
        print(
            "ablation:      off - these rows may be measuring the base model, "
            "not the instructions"
        )

    fabricated_total = 0
    empty_total = 0
    for entry in report_rows:
        for run in entry["runs"]:
            judge = run["judge"]
            if judge is None or judge.get("error"):
                continue
            fabricated_total += _ruby_int(judge.get("fabricated_excerpts"))
            empty_total += _ruby_int(judge.get("empty_excerpt_downgrades"))
    leaks = sum(bool(result.get("leak")) for result in control_results)
    if not opts["calibrate"]:
        fabricated_word = "excerpt" if fabricated_total == 1 else "excerpts"
        empty_word = "downgrade" if empty_total == 1 else "downgrades"
        leak_word = "leak" if leaks == 1 else "leaks"
        print(
            f"judge control: {len(control_results)} sampled - {leaks} {leak_word} - "
            f"{fabricated_total} fabricated {fabricated_word} - "
            f"{empty_total} empty-excerpt {empty_word}"
        )
    for result in control_results:
        if not (
            result.get("leak")
            or result.get("error")
            or result.get("skipped")
        ):
            continue
        reason = (
            result.get("error")
            or result.get("skipped")
            or (
                f"{result['decoy_passes']}/{result['expected_assertions']} "
                "expected assertions passed on the wrong transcript"
            )
        )
        print(
            f"  {result['id']} vs decoy {result['decoy_id']}: {reason}"
        )

    if calibration_results:
        agreed = sum(
            _ruby_int(result.get("agreements")) for result in calibration_results
        )
        total_labels = sum(
            _ruby_int(result.get("assertions")) for result in calibration_results
        )
        print(
            f"calibration:   {len(calibration_results)} cases - "
            f"{agreed}/{total_labels} verdicts agreed with the hand labels"
        )
        for result in calibration_results:
            if result.get("error") is None and _ruby_float(result.get("rate")) >= 1.0:
                continue
            detail = (
                result.get("error")
                if result.get("error") is not None
                else f"{result.get('agreements')}/{result.get('assertions')}"
            )
            print(f"  {result['id']}: {detail}")

    ambiguous = [
        assertion
        for entry in report_rows
        for assertion in entry["assertions"]
        if assertion["ambiguous_assertion"]
    ]
    if ambiguous:
        print(
            f"ambiguity:     {len(ambiguous)} assertion(s) returned unclear in "
            "more than a third of repeats (fixture bug, not a judge tuning problem)"
        )

    if harness_errors:
        print(
            f"harness:       {len(harness_errors)} error(s) - nothing was "
            "learned from those runs"
        )
        for message in harness_errors[:10]:
            print(f"  {message}")
        if len(harness_errors) > 10:
            print(f"  ... {len(harness_errors) - 10} more")

    for plan in provenance_plans:
        print(
            f"provenance:    {plan['skill']} {plan['status']} - "
            f"{plan['note']}"
        )

    print(
        "$"
        + f"{total_cost:.4f}"
        + f" - {duration_s // 60}m{duration_s % 60:02d}s - artifact "
        + _root_relative(json_path)
    )

    # --- machine artifact --------------------------------------------------
    artifact = {
        "schema": ARTIFACT_SCHEMA,
        "started_at": _time_iso(started_at),
        "finished_at": _time_iso(finished_at),
        "harness": {
            "script": "scripts/eval.py",
            "git_sha": git_sha,
            "dirty": git_dirty,
        },
        "runner": {
            "kind": opts["runner"],
            "cli_version": cli_version,
            "plugin_name": plugin_name,
            "candidate_model": opts["model"],
            "judge_model": opts["judge_model"],
            "invoke": opts["invoke"],
            "argv_template": candidate_argv(opts),
            "ablation_argv_template": (
                ablation_argv(opts) if opts["ablation"] else None
            ),
            "judge_argv_template": judge_argv(opts, judge_system_path),
            "judge_system_prompt_sha256": _sha256_text(JUDGE_SYSTEM_PROMPT),
        },
        "config": {
            "repeat": opts["repeat"],
            "ablation": opts["ablation"],
            "control_sample": opts["control"],
            "fail_under": opts["fail_under"],
            "timeout_s": opts["timeout"],
            "jobs": opts["jobs"],
            "per_run_budget_usd": opts["per_run_budget"],
            "max_cost_usd": opts["max_cost"],
            "skills": opts["skills"],
            "ids": opts["ids"],
        },
        "fixtures_file": {
            "path": "tests/behavioral-contracts.yml",
            "sha256": fixtures_sha,
        },
        "provenance": provenance_plans,
        "totals": {
            "rows": len(report_rows),
            "pass": status_counts["PASS"],
            "flaky": status_counts["FLAKY"],
            "fail": status_counts["FAIL"],
            "error": status_counts["ERROR"],
            "no_signal": status_counts["NO SIGNAL"],
            "fabricated_excerpts": fabricated_total,
            "empty_excerpt_downgrades": empty_total,
            "judge_control_leak": leaks,
            "cost_usd": _ruby_round(total_cost, 4),
            "duration_s": duration_s,
            "harness_errors": len(harness_errors),
        },
        "results": report_rows,
        "ablation": [
            {
                "id": entry["label"],
                "with": entry["with_rate"],
                "without": entry["without_rate"],
                "delta": _ruby_round(
                    entry["with_rate"] - entry["without_rate"]
                ),
                "no_signal": entry["status_label"] == "NO SIGNAL",
            }
            for entry in report_rows
            if entry["without_rate"] is not None
        ],
        "judge_control": control_results,
        "calibration": calibration_results,
        "harness_error_messages": harness_errors,
    }
    with open(json_path, "w", encoding="utf-8") as handle:
        handle.write(_json_pretty(artifact) + "\n")
    shutil.rmtree(scratch_dir, ignore_errors=True)

    # -----------------------------------------------------------------------
    # Exit codes
    # -----------------------------------------------------------------------
    if budget_exhausted:
        print(
            "scripts/eval.py: --max-cost-usd ceiling of "
            + "$"
            + f"{opts['max_cost']:.2f}"
            + " reached; results are partial.",
            file=sys.stderr,
        )
        return EXIT_HARNESS
    if harness_errors:
        return EXIT_HARNESS
    if status_counts["ERROR"] > 0:
        return EXIT_HARNESS

    regression = any(
        entry["status_label"] == "FAIL"
        or any(
            assertion["rate"] < opts["fail_under"]
            for assertion in entry["assertions"]
        )
        for entry in report_rows
    )
    if regression:
        return EXIT_REGRESSION

    calibration_disagreements = sum(
        _ruby_int(result.get("assertions"))
        - _ruby_int(result.get("agreements"))
        for result in calibration_results
    )
    if (
        status_counts["NO SIGNAL"] > 0
        or leaks > 0
        or calibration_disagreements > 0
    ):
        return EXIT_FIXTURE_QUALITY
    return EXIT_OK


def main(argv: list[str] | None = None) -> int:
    opts = parse_options(argv)

    # CI guard. The free verifier separately ensures no workflow calls this
    # paid harness; requiring an explicit flag here protects manual invocations.
    if _ruby_truthy(os.environ.get("CI")) and not opts["allow_ci"]:
        print(
            "scripts/eval.py costs model tokens and is opt-in. "
            "Pass --allow-ci to run it in CI.",
            file=sys.stderr,
        )
        return EXIT_HARNESS

    if opts["judge_model"] == opts["model"] and not opts["allow_self_judge"]:
        print(
            f"scripts/eval.py: judge model equals candidate model "
            f"({opts['model']}). Same-model self-grading inflates.",
            file=sys.stderr,
        )
        print(
            "Pass --allow-self-judge to override, or set --judge-model to a "
            "different model.",
            file=sys.stderr,
        )
        return EXIT_HARNESS

    if opts["runner"] != "claude":
        print(
            f"scripts/eval.py: --runner {opts['runner']} is not implemented.",
            file=sys.stderr,
        )
        print(
            "Neither codex nor cursor-agent has a per-session plugin loader, "
            "so those arms would have to",
            file=sys.stderr,
        )
        print(
            "inline the generated text from bundles/ and would test a different "
            "artifact than --plugin-dir",
            file=sys.stderr,
        )
        print(
            "loads. Their envelope contracts were also never verified here. "
            "Use --runner claude.",
            file=sys.stderr,
        )
        return EXIT_HARNESS

    try:
        plugin_name = load_plugin_name()
    except RunnerError as error:
        print(f"scripts/eval.py: {error}", file=sys.stderr)
        return EXIT_HARNESS

    # Capture environment facts before row selection, matching the original
    # harness's timestamp and output-directory ordering.
    cli_version = detect_cli_version()
    started_at = _datetime.datetime.now(_datetime.timezone.utc)
    stamp = _time_stamp(started_at)
    out_dir = _expand_path(
        opts["out_dir"]
        if opts["out_dir"] is not None
        else os.path.join(ROOT, "tests", "results", stamp)
    )
    json_path = (
        _expand_path(opts["json_path"])
        if opts["json_path"] is not None
        else os.path.join(out_dir, "eval.json")
    )
    git_sha = (git_fact(["rev-parse", "--short", "HEAD"]) or "").strip()
    git_dirty = bool(
        (git_fact(["status", "--porcelain"]) or "").strip()
    )

    # Calibration mode has an explicit no-cases result before fixture loading,
    # matching the Ruby harness's early quality gate.
    if opts["calibrate"]:
        calibration_files = sorted(
            str(path) for path in Path(CALIBRATION_DIR).glob("*.yml")
        )
        if not calibration_files:
            print(
                "scripts/eval.py --calibrate: no cases in "
                "tests/judge-calibration/*.yml.",
                file=sys.stderr,
            )
            print(file=sys.stderr)
            print(
                'Until those exist, "the judge said pass" is an unaudited claim '
                "wearing a JSON schema.",
                file=sys.stderr,
            )
            print(
                "Hand-label five transcripts -- two clear passes, two clear "
                "fails, one genuinely",
                file=sys.stderr,
            )
            print(
                "borderline -- as files of this shape:",
                file=sys.stderr,
            )
            print(file=sys.stderr)
            print("  id: compass-open-ended-clear-pass", file=sys.stderr)
            print("  transcript: |", file=sys.stderr)
            print("    <the full candidate transcript>", file=sys.stderr)
            print("  assertions:", file=sys.stderr)
            print("    - kind: expected", file=sys.stderr)
            print(
                "      text: Classify the journey as open-ended.",
                file=sys.stderr,
            )
            print("      verdict: pass", file=sys.stderr)
            print("    - kind: reject", file=sys.stderr)
            print(
                "      text: Penalize the absence of a progress bar.",
                file=sys.stderr,
            )
            print("      verdict: pass", file=sys.stderr)
            print(file=sys.stderr)
            return EXIT_NO_MATCH

    try:
        fixtures = load_fixtures(FIXTURE_PATH)
    except Exception as error:
        print(f"scripts/eval.py: {error}", file=sys.stderr)
        return EXIT_HARNESS

    fixtures_sha = _sha256_text(_read_utf8_file(FIXTURE_PATH))
    all_rows = expand_rows(fixtures, opts, plugin_name)
    rows = filter_rows(all_rows, opts)
    if opts["calibrate"]:
        rows = []
    if not rows and not opts["calibrate"]:
        print(
            "scripts/eval.py: no fixture matched the filters "
            f"(--skill {opts['skills']!r}, --id {opts['ids']!r}) "
            f"across {len(all_rows)} rows from {len(fixtures)} fixtures.",
            file=sys.stderr,
        )
        return EXIT_NO_MATCH

    calibration_cases: list[dict[str, Any]] = []
    if opts["calibrate"]:
        try:
            calibration_cases = load_calibration_cases()
        except Exception as error:
            print(f"scripts/eval.py: {error}", file=sys.stderr)
            return EXIT_HARNESS

    provenance_plans = [
        build_provenance_plan(skill_name)
        for skill_name in sorted({row["skill"] for row in rows})
    ]
    control_pairs = plan_control_pairs(rows, opts["control"])

    if opts["dry_run"]:
        return run_dry_run(
            opts,
            plugin_name,
            cli_version,
            started_at,
            out_dir,
            json_path,
            git_sha,
            git_dirty,
            fixtures_sha,
            fixtures,
            all_rows,
            rows,
            provenance_plans,
            control_pairs,
            calibration_cases,
        )
    return run_live(
        opts,
        plugin_name,
        cli_version,
        started_at,
        out_dir,
        json_path,
        git_sha,
        git_dirty,
        fixtures_sha,
        fixtures,
        all_rows,
        rows,
        provenance_plans,
        control_pairs,
        calibration_cases,
    )


if __name__ == "__main__":
    sys.exit(main())
