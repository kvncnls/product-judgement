#!/usr/bin/env python3
"""Verify the repository's source contracts and generated artifacts.

This check is deliberately text and structure based.  The opt-in evaluation
harness spends model tokens and is only syntax checked here; it is never run by
the verifier or by CI.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

try:  # Running as ``python scripts/verify.py`` has no package context.
    from yaml_utils import safe_load
except ImportError:  # pragma: no cover - supports ``python -m scripts.verify``.
    from scripts.yaml_utils import safe_load


ROOT = Path(__file__).resolve().parent.parent
SKILLS = ["focal", "compass", "flywheel", "soul", "product-judgement"]
errors: list[str] = []


def quoted(value: Any) -> str:
    """Render a value close to Ruby's ``#inspect`` for stable diagnostics."""

    return json.dumps(value, ensure_ascii=False)


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read(path: str | Path) -> str:
    # Decode the bytes directly so CRLF and other source formatting remain
    # visible to exact text checks, matching Ruby's File.read behavior.
    return (ROOT / path).read_bytes().decode("utf-8")


def require_text(path: str, text: str, label: str) -> None:
    try:
        present = text in read(path)
    except FileNotFoundError:
        present = False
    if not present:
        errors.append(f"{path}: missing {quoted(label)}")


def reject_text(paths: list[str], text: str, label: str) -> None:
    for path in paths:
        try:
            present = text in read(path)
        except FileNotFoundError:
            continue
        if present:
            errors.append(f"{path}: contains stale {quoted(label)}")


def first_error_line(error: BaseException) -> str:
    return str(error).splitlines()[0].strip()


def run_checked(command: list[str], *, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    """Run a free, deterministic maintenance check and capture its output."""

    return subprocess.run(command, cwd=cwd, capture_output=True, text=True)


def runtime_output(path: Path) -> bool:
    try:
        parts = path.relative_to(ROOT).parts
    except ValueError:
        return False
    return bool(parts) and (
        parts[0] == "dist" or (len(parts) > 1 and parts[0] == "tests" and parts[1] == "results")
    )


def is_within(path: Path, directory: Path) -> bool:
    try:
        path.relative_to(directory)
        return True
    except ValueError:
        return False


# Skill frontmatter must stay portable and discoverable.
for skill in SKILLS:
    path = f"{skill}/SKILL.md"
    try:
        content = read(path)
    except FileNotFoundError:
        errors.append(f"{path}: missing")
        continue
    match = re.match(r"\A---\n(.*?)\n---\n", content, re.DOTALL)

    if not match:
        errors.append(f"{path}: missing YAML frontmatter")
        continue

    try:
        metadata = safe_load(match.group(1))
    except yaml.YAMLError as error:
        errors.append(f"{path}: invalid YAML frontmatter ({first_error_line(error)})")
        continue

    if not isinstance(metadata, dict) or metadata.get("name") != skill:
        errors.append(f"{path}: frontmatter name must be {quoted(skill)}")
    description = metadata.get("description") if isinstance(metadata, dict) else None
    if not isinstance(description, str) or len(description) < 80:
        errors.append(f"{path}: frontmatter description must be a substantive string")
    # The Agent Skills spec caps description at 1024 characters. Over it, the
    # claude.ai and Skills API upload paths reject the Skill; Claude Code does
    # not validate, so nothing else in this repo would notice.
    if isinstance(description, str) and len(description) > 1024:
        errors.append(
            f"{path}: frontmatter description is {len(description)} characters; the spec cap is 1024"
        )
    if isinstance(metadata, dict) and len(str(metadata.get("name", ""))) > 64:
        errors.append(f"{path}: frontmatter name must be 64 characters or fewer")
    if not isinstance(metadata, dict) or metadata.get("license") != "MIT":
        errors.append(f"{path}: frontmatter must declare license: MIT")
    # argument-hint is a Claude Code extension, kept deliberately and stripped
    # from upload packages by scripts/package_skills.py.
    if not isinstance(metadata, dict) or not isinstance(metadata.get("argument-hint"), str):
        errors.append(f"{path}: frontmatter must carry an argument-hint")
    if isinstance(metadata, dict):
        allowed = {
            "name",
            "description",
            "license",
            "compatibility",
            "metadata",
            "allowed-tools",
            "argument-hint",
        }
        unknown_keys = [key for key in metadata if key not in allowed]
        if unknown_keys:
            errors.append(
                f"{path}: frontmatter keys {quoted(unknown_keys)} are neither spec fields nor known Claude Code extensions; teach scripts/package_skills.py about them first"
            )


# Every Skill folder is installed, zipped, and symlinked whole, so they must
# carry the same files. This is the check that would have caught ABOUT.md
# living in two of five folders and product-judgement shipping no LICENSE.
for skill in SKILLS:
    for required in ["SKILL.md", "README.md", "LICENSE", "agents/openai.yaml"]:
        if not (ROOT / skill / required).is_file():
            errors.append(f"{skill}/{required}: missing")
    extra = sorted(
        path.name
        for path in (ROOT / skill).glob("*.md")
        if path.name not in {"SKILL.md", "README.md"}
    )
    if extra:
        errors.append(
            f"{skill}: unexpected top-level Markdown {quoted(extra)}; reference material belongs in reference/"
        )
# product-judgement legitimately has no reference/ — it is audit-only and its
# contract is always needed, so it lives in the spine.
for skill in [name for name in SKILLS if name != "product-judgement"]:
    if not list((ROOT / skill / "reference").glob("*.md")):
        errors.append(f"{skill}/reference: must contain at least one Markdown file")


# agents/openai.yaml is Codex's per-skill interface file. It went unchecked and
# so existed on one Skill of five.
OPENAI_INTERFACE_KEYS = {
    "display_name",
    "short_description",
    "icon_small",
    "icon_large",
    "brand_color",
    "default_prompt",
}
for skill in SKILLS:
    rel = f"{skill}/agents/openai.yaml"
    path = ROOT / rel
    if not path.is_file():
        continue

    try:
        doc = safe_load(read(rel))
    except yaml.YAMLError as error:
        errors.append(f"{rel}: invalid YAML ({first_error_line(error)})")
        continue
    interface = doc.get("interface") if isinstance(doc, dict) else None
    if not isinstance(interface, dict):
        errors.append(f"{rel}: must declare an interface mapping")
        continue
    stray = [key for key in interface if key not in OPENAI_INTERFACE_KEYS]
    if stray:
        errors.append(f"{rel}: unknown interface key(s) {quoted(stray)}")
    display = interface.get("display_name")
    if not isinstance(display, str) or not display or len(display) > 64:
        errors.append(f"{rel}: interface.display_name is required and capped at 64 characters")
    short = interface.get("short_description")
    # OpenAI's own generator rejects anything outside 25-64, which is stricter
    # than the 1024 the Codex runtime allows. Match the generator.
    if not isinstance(short, str) or not 25 <= len(short) <= 64:
        short_kind = len(short) if isinstance(short, str) else type(short).__name__
        errors.append(
            f"{rel}: interface.short_description must be 25-64 characters (was {short_kind})"
        )


# Plugin manifests are the install path for Claude Code, Cursor, and Codex, so
# every one of them must stay valid, agree on a version, and expose all five
# Skills. A manifest that silently drops a Skill installs a broken collection.
PLUGIN_MANIFESTS = [
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    ".cursor-plugin/plugin.json",
    ".codex-plugin/plugin.json",
    ".agents/plugins/marketplace.json",
]

manifests: dict[str, Any] = {}
for path in PLUGIN_MANIFESTS:
    try:
        manifests[path] = json.loads(read(path))
    except FileNotFoundError:
        errors.append(f"{path}: missing")
    except json.JSONDecodeError as error:
        errors.append(f"{path}: invalid JSON ({first_error_line(error)})")

expected_skill_paths = sorted(f"./{skill}" for skill in SKILLS)
for path in [".claude-plugin/plugin.json", ".cursor-plugin/plugin.json", ".codex-plugin/plugin.json"]:
    manifest = manifests.get(path)
    if manifest is None:
        continue

    if not isinstance(manifest, dict) or manifest.get("name") != "product-judgement":
        errors.append(f'{path}: name must be "product-judgement"')
    declared = manifest.get("skills") if isinstance(manifest, dict) else None
    if not isinstance(declared, list) or sorted(declared) != expected_skill_paths:
        errors.append(f"{path}: skills must list every Skill as {quoted(expected_skill_paths)}")


# Each marketplace points at the repository root, so the plugin manifests above
# are what actually resolve the Skills.
marketplace = manifests.get(".claude-plugin/marketplace.json")
if isinstance(marketplace, dict):
    entries = marketplace.get("plugins")
    if isinstance(entries, list) and len(entries) == 1 and isinstance(entries[0], dict):
        if entries[0].get("source") != "./":
            errors.append('.claude-plugin/marketplace.json: plugin source must be "./"')
        if entries[0].get("name") != "product-judgement":
            errors.append('.claude-plugin/marketplace.json: plugin name must be "product-judgement"')
    else:
        errors.append(".claude-plugin/marketplace.json: expected exactly one plugin entry")
    owner = marketplace.get("owner")
    if not isinstance(owner, dict) or not isinstance(owner.get("name"), str):
        errors.append(".claude-plugin/marketplace.json: owner.name is required")
elif marketplace is not None:
    errors.append(".claude-plugin/marketplace.json: expected a mapping")

marketplace = manifests.get(".agents/plugins/marketplace.json")
if isinstance(marketplace, dict):
    entries = marketplace.get("plugins")
    if isinstance(entries, list) and len(entries) == 1 and isinstance(entries[0], dict):
        source = entries[0].get("source")
        if not isinstance(source, dict) or source.get("source") != "local" or source.get("path") != "./":
            errors.append('.agents/plugins/marketplace.json: plugin source must be a local path of "./"')
    else:
        errors.append(".agents/plugins/marketplace.json: expected exactly one plugin entry")
elif marketplace is not None:
    errors.append(".agents/plugins/marketplace.json: expected a mapping")


# One version across every manifest keeps a tagged release honest.
versions: list[tuple[str, Any]] = []
for path, manifest in manifests.items():
    if not isinstance(manifest, dict):
        continue
    if path.endswith("marketplace.json"):
        plugins = manifest.get("plugins")
        first_plugin = plugins[0] if isinstance(plugins, list) and plugins else {}
        version = first_plugin.get("version") if isinstance(first_plugin, dict) else None
    else:
        version = manifest.get("version")
    if version:
        versions.append((path, version))
if len({json.dumps(version, sort_keys=True) for _, version in versions}) > 1:
    detail = ", ".join(f"{path}={version}" for path, version in versions)
    errors.append(f"plugin manifests disagree on version: {detail}")


# The universal installer must stay runnable and cover every Skill and agent.
install_script = ROOT / "scripts" / "install.sh"
if install_script.is_file():
    if not os.access(install_script, os.X_OK):
        errors.append("scripts/install.sh: must be executable")
    install_source = read(install_script)
    if f'SKILLS="{" ".join(SKILLS)}"' not in install_source:
        errors.append("scripts/install.sh: SKILLS list must match the Skill folders")
    for agent in ["claude", "codex", "cursor"]:
        if not re.search(rf"^\s+{re.escape(agent)}\)", install_source, re.MULTILINE):
            errors.append(f"scripts/install.sh: missing a target directory for {agent}")
    completed = run_checked(["sh", "-n", str(install_script)])
    if completed.returncode != 0:
        errors.append(f"scripts/install.sh: shell syntax error ({completed.stderr.strip()})")
else:
    errors.append("scripts/install.sh: missing")


# Relative Markdown links in source documentation must resolve. Generated bundles
# rewrite them to internal source anchors, checked by the bundle generator.
markdown_files = sorted(
    path
    for path in ROOT.rglob("*.md")
    if not is_within(path, ROOT / ".git")
    and not runtime_output(path)
    and not is_within(path, ROOT / "bundles")
    and not is_within(path, ROOT / ".venv")
)
for path in markdown_files:
    for raw_target in re.findall(
        r"\[[^\]]*\]\(([^)]+)\)", path.read_bytes().decode("utf-8")
    ):
        target = raw_target.strip()
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1]
        target = re.split(r"\s+[\"']", target, maxsplit=1)[0]
        if not target or target.startswith("#"):
            continue
        if re.match(r"\A(?:https?|mailto|app)://", target, re.IGNORECASE):
            continue

        file_target = target.split("#", 1)[0]
        if not file_target:
            continue
        if not (path.parent / file_target).exists():
            errors.append(f"{relative(path)}: broken relative link {quoted(target)}")


# Verify structure here; scenario fixtures and opt-in evaluations test judgment.
# Phrase matching cannot establish whether an instruction improves a real audit.
for skill in [name for name in SKILLS if name != "product-judgement"]:
    spine = f"{skill}/SKILL.md"
    for mode in ["review", "build"]:
        reference = f"reference/{mode}.md"
        if not (ROOT / skill / reference).is_file():
            errors.append(f"{spine}: missing {mode} reference")
        require_text(spine, f"]({reference})", f"{mode} reference link")
for skill in SKILLS:
    spine = ROOT / skill / "SKILL.md"
    if spine.is_file() and len(spine.read_bytes().decode("utf-8").splitlines()) > 500:
        errors.append(f"{skill}/SKILL.md: exceeds the 500-line progressive-disclosure budget")


# Public documentation must expose every Skill, the score contract, and the current
# install/update path without claiming the repository has no maintainer build step.
try:
    pnpm_policy = safe_load(read("pnpm-workspace.yaml"))
    minimum_age = pnpm_policy.get("minimumReleaseAge") if isinstance(pnpm_policy, dict) else None
    if not isinstance(minimum_age, int) or isinstance(minimum_age, bool) or minimum_age < 1440:
        errors.append("pnpm-workspace.yaml: minimumReleaseAge must be at least 1440 minutes")
except (FileNotFoundError, yaml.YAMLError) as error:
    errors.append(f"pnpm-workspace.yaml: {first_error_line(error)}")

required_docs = ["README.md"] + [f"{skill}/README.md" for skill in SKILLS]
for path in required_docs:
    if not (ROOT / path).is_file():
        errors.append(f"{path}: missing")
require_text("README.md", "pnpm dlx skills update -g product-judgement focal compass flywheel soul", "global update command")
require_text("README.md", "`/12` for Focal, Compass, and Soul", "native totals")
require_text("README.md", "`N/E` means **not evaluated**, not zero", "N/E explanation")
require_text("README.md", "no runtime build step", "runtime/build distinction")
reject_text(required_docs, "Claude Code skill", "platform-specific Skill description")
reject_text(["README.md"], "no build step, no dependencies", "obsolete no-build claim")


# Behavioral fixtures are machine-readable and must carry both positive and negative
# assertions so they can drive a later model-evaluation harness.
fixture_path = ROOT / "tests" / "behavioral-contracts.yml"
try:
    fixtures = safe_load(fixture_path.read_bytes().decode("utf-8"))
    if not isinstance(fixtures, list) or len(fixtures) < 8:
        errors.append("tests/behavioral-contracts.yml: expected at least eight fixtures")
    else:
        ids = [fixture.get("id") for fixture in fixtures if isinstance(fixture, dict) and fixture.get("id") is not None]
        if len(ids) != len(set(ids)):
            errors.append("tests/behavioral-contracts.yml: fixture IDs must be unique")

        for index, fixture in enumerate(fixtures, start=1):
            if not isinstance(fixture, dict):
                errors.append(f"tests/behavioral-contracts.yml: fixture {index} must be a mapping")
                continue

            for key in ["id", "skill", "scenario"]:
                value = fixture.get(key)
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"tests/behavioral-contracts.yml: fixture {index} needs {key}")

            if fixture.get("skill") not in [*SKILLS, "shared"]:
                errors.append(f"tests/behavioral-contracts.yml: fixture {index} names an unknown Skill")
            if fixture.get("mode", "audit") not in ["audit", "build"]:
                errors.append(f"tests/behavioral-contracts.yml: fixture {index} has an unsupported mode")
            if fixture.get("skill") == "product-judgement" and fixture.get("mode") == "build":
                errors.append("tests/behavioral-contracts.yml: Product Judgement is audit-only")

            for key in ["evidence", "expected", "reject"]:
                value = fixture.get(key)
                valid = isinstance(value, list) and bool(value) and all(
                    isinstance(item, str) and item.strip() for item in value
                )
                if not valid:
                    errors.append(
                        f"tests/behavioral-contracts.yml: fixture {index} needs a non-empty {key} list"
                    )
except FileNotFoundError as error:
    errors.append(f"tests/behavioral-contracts.yml: {first_error_line(error)}")
except yaml.YAMLError as error:
    errors.append(f"tests/behavioral-contracts.yml: {first_error_line(error)}")


# Shared fragments have a single maintained source and are copied inline so a
# standalone install retains its complete evidence and scoring contract.
sync_script = ROOT / "scripts" / "sync_contracts.py"
if sync_script.is_file():
    completed = run_checked([sys.executable, str(sync_script), "--check"])
    if completed.returncode != 0:
        errors.append(f"shared contracts: {(completed.stderr + completed.stdout).strip()}")
else:
    errors.append("shared contracts: scripts/sync_contracts.py: missing")


# The /12 band table is shared by the three three-dimension Skills; Flywheel's
# /16 rows are correct local arithmetic for four plays, not drift.
BAND_ROWS_12 = [
    "| **Broken** | `average <= 1.5` | `0–4 / 12` |",
    "| **Significant rework** | `1.5 < average < 2.5` | `5–7 / 12` |",
    "| **Solid** | `2.5 <= average < 3.5` | `8–10 / 12` |",
    "| **Excellent** | `average >= 3.5` | `11–12 / 12` |",
]
BAND_ROWS_16 = [
    "| **Broken** | `average <= 1.5` | `0–6 / 16` |",
    "| **Significant rework** | `1.5 < average < 2.5` | `7–9 / 16` |",
    "| **Solid** | `2.5 <= average < 3.5` | `10–13 / 16` |",
    "| **Excellent** | `average >= 3.5` | `14–16 / 16` |",
]
for skill in ["focal", "compass", "soul"]:
    rel = f"{skill}/reference/review.md"
    for row in BAND_ROWS_12:
        if row not in read(rel):
            errors.append(f"{rel}: missing shared /12 band row {quoted(row)}")
for row in BAND_ROWS_16:
    if row not in read("flywheel/reference/review.md"):
        errors.append(f"flywheel/reference/review.md: missing /16 band row {quoted(row)}")


# The orchestration override is what stops a local Skill printing its own locked
# template, asking a framing question, or routing back to the orchestrator from
# inside an orchestrated pass. Losing it silently breaks every holistic audit.
for skill in [name for name in SKILLS if name != "product-judgement"]:
    rel = f"{skill}/SKILL.md"
    content = read(rel)
    if "**Orchestrated pass—this overrides every other instruction in this Skill and its reference files.**" not in content:
        errors.append(f"{rel}: missing the orchestrated-pass override")
    if "do not read [reference/examples.md](reference/examples.md)" not in content.lower():
        errors.append(f"{rel}: orchestrated pass must suppress the examples calibration read")
    if "Never hand a cross-scale request back to Product Judgement" not in content:
        errors.append(f"{rel}: orchestrated pass must forbid handing a cross-scale request back")

require_text("product-judgement/SKILL.md", "N/E—Skill not installed", "uninstalled-scale verdict")
require_text("product-judgement/SKILL.md", "This wrapper supersedes local output instructions", "local-output supersession")
require_text("README.md", "a scale whose Skill is not installed alongside Product Judgement", "third permitted N/E use")


# The behavioral fixtures have a runner. It spends real model tokens, so it must
# stay opt-in and must never be wired into the verifier or CI. Syntax checking
# invokes Python's compiler only; it never imports or runs the paid harness.
eval_script = ROOT / "scripts" / "eval.py"
if eval_script.is_file():
    if not os.access(eval_script, os.X_OK):
        errors.append("scripts/eval.py: must be executable")
    completed = run_checked([sys.executable, "-m", "py_compile", str(eval_script)])
    if completed.returncode != 0:
        errors.append(f"scripts/eval.py: syntax error ({completed.stderr.strip()})")
    for workflow in [".github/workflows/verify.yml", ".github/workflows/release.yml"]:
        workflow_path = ROOT / workflow
        # Match the paid harness path even when quoted or followed by shell
        # punctuation.  ``scripts/test_eval.py`` does not contain this path.
        if workflow_path.is_file() and re.search(r"(?<![\w/])(?:\./)?scripts/eval\.py(?![\w.])", read(workflow)):
            errors.append(f"{workflow}: must not run scripts/eval.py; it costs model tokens")
else:
    errors.append("scripts/eval.py: missing")


# Maintainer and regression tools must remain executable Python 3.11+ scripts.
# Keep test_eval.py/test_tooling.py in this list: they are offline regressions,
# while eval.py above is the only paid harness and is never executed here.
tool_names = [
    "build_bundles",
    "check_version",
    "package_skills",
    "verify_packages",
    "test_packages",
    "test_install",
    "test_eval",
    "test_eval_cli",
    "test_tooling",
    "sync_contracts",
]
for name in tool_names:
    path = ROOT / "scripts" / f"{name}.py"
    rel = f"scripts/{name}.py"
    if not path.is_file():
        errors.append(f"{rel}: missing")
        continue
    if not os.access(path, os.X_OK):
        errors.append(f"{rel}: must be executable")
    completed = run_checked([sys.executable, "-m", "py_compile", str(path)])
    if completed.returncode != 0:
        errors.append(f"{rel}: syntax error ({completed.stderr.strip()})")

for name in ["package_skills", "verify_packages"]:
    require_text(".github/workflows/release.yml", f"scripts/{name}.py", f"{name} release step")


# Generated bundles must be exact products of the canonical source files.
bundle_script = ROOT / "scripts" / "build_bundles.py"
if bundle_script.is_file():
    completed = run_checked([sys.executable, str(bundle_script), "--check"])
    if completed.returncode != 0:
        errors.append(f"bundles: {(completed.stderr + completed.stdout).strip()}")
else:
    errors.append("bundles: scripts/build_bundles.py: missing")


# Lightweight text hygiene catches drift that Markdown renderers often hide.
# Include Python and TOML because the maintainer tooling and uv project metadata
# are source; skip generated/runtime output and local environments.
text_files = sorted(
    {
        path
        for pattern in ["*.md", "*.py", "*.rb", "*.toml", "*.yml", "*.yaml"]
        for path in ROOT.rglob(pattern)
        if not is_within(path, ROOT / ".git")
        and not is_within(path, ROOT / ".venv")
        and not runtime_output(path)
    }
)
for path in text_files:
    content = path.read_bytes()
    if content and not content.endswith(b"\n"):
        errors.append(f"{relative(path)}: must end with a newline")
    for line_number, line in enumerate(content.splitlines(keepends=True), start=1):
        stripped = line.rstrip(b"\r\n")
        if stripped.strip() and re.search(rb"[ \t]+\Z", stripped):
            errors.append(f"{relative(path)}:{line_number}: trailing whitespace")


if errors:
    plural = "" if len(errors) == 1 else "s"
    print(f"Verification failed with {len(errors)} issue{plural}:", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    sys.exit(1)

print(
    f"Verified {len(SKILLS)} Skills, {len(markdown_files)} Markdown source files, "
    "generated bundles, and behavioral contracts."
)
