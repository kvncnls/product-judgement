#!/usr/bin/env python3
"""Verify the repository's source contracts.

Checks Skill frontmatter, plugin manifests, the installer, relative links,
scoring and boundary invariants, behavioral contract fixtures, documentation,
text hygiene, and exact bundle synchronization. CI runs this file.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ["focal", "compass", "flywheel", "soul", "product-judgement"]

errors: list[str] = []


def quoted(value) -> str:
    """Render a value the way Ruby's #inspect did, so CI messages stay stable."""
    return json.dumps(value)


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require_text(path: str, text: str, label: str) -> None:
    if text not in read(path):
        errors.append(f"{path}: missing {quoted(label)}")


def reject_text(paths: list[str], text: str, label: str) -> None:
    for path in paths:
        if text in read(path):
            errors.append(f"{path}: contains stale {quoted(label)}")


# Skill frontmatter must stay portable and discoverable.
for skill in SKILLS:
    path = f"{skill}/SKILL.md"
    match = re.match(r"\A---\n(.*?)\n---\n", read(path), re.DOTALL)

    if not match:
        errors.append(f"{path}: missing YAML frontmatter")
        continue

    try:
        metadata = yaml.safe_load(match.group(1))
    except yaml.YAMLError as error:
        first_line = str(error).splitlines()[0].strip()
        errors.append(f"{path}: invalid YAML frontmatter ({first_line})")
        continue

    if not isinstance(metadata, dict) or metadata.get("name") != skill:
        errors.append(f"{path}: frontmatter name must be {quoted(skill)}")
    description = metadata.get("description") if isinstance(metadata, dict) else None
    if not isinstance(description, str) or len(description) < 80:
        errors.append(f"{path}: frontmatter description must be a substantive string")

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

manifests: dict[str, dict] = {}
for path in PLUGIN_MANIFESTS:
    try:
        manifests[path] = json.loads(read(path))
    except FileNotFoundError:
        errors.append(f"{path}: missing")
    except json.JSONDecodeError as error:
        errors.append(f"{path}: invalid JSON ({str(error).splitlines()[0].strip()})")

expected_skill_paths = sorted(f"./{skill}" for skill in SKILLS)

for path in [".claude-plugin/plugin.json", ".cursor-plugin/plugin.json", ".codex-plugin/plugin.json"]:
    manifest = manifests.get(path)
    if manifest is None:
        continue

    if manifest.get("name") != "product-judgement":
        errors.append(f'{path}: name must be "product-judgement"')
    declared = manifest.get("skills")
    if not isinstance(declared, list) or sorted(declared) != expected_skill_paths:
        errors.append(f"{path}: skills must list every Skill as {quoted(expected_skill_paths)}")

# Each marketplace points at the repository root, so the plugin manifests above
# are what actually resolve the Skills.
marketplace = manifests.get(".claude-plugin/marketplace.json")
if marketplace is not None:
    entries = marketplace.get("plugins")
    if isinstance(entries, list) and len(entries) == 1:
        if entries[0].get("source") != "./":
            errors.append('.claude-plugin/marketplace.json: plugin source must be "./"')
        if entries[0].get("name") != "product-judgement":
            errors.append('.claude-plugin/marketplace.json: plugin name must be "product-judgement"')
    else:
        errors.append(".claude-plugin/marketplace.json: expected exactly one plugin entry")
    if not isinstance(marketplace.get("owner", {}).get("name"), str):
        errors.append(".claude-plugin/marketplace.json: owner.name is required")

marketplace = manifests.get(".agents/plugins/marketplace.json")
if marketplace is not None:
    entries = marketplace.get("plugins")
    if isinstance(entries, list) and len(entries) == 1:
        source = entries[0].get("source")
        if not isinstance(source, dict) or source.get("source") != "local" or source.get("path") != "./":
            errors.append('.agents/plugins/marketplace.json: plugin source must be a local path of "./"')
    else:
        errors.append(".agents/plugins/marketplace.json: expected exactly one plugin entry")

# One version across every manifest keeps a tagged release honest.
versions = []
for path, manifest in manifests.items():
    if manifest is None:
        continue
    if path.endswith("marketplace.json"):
        plugins = manifest.get("plugins") or [{}]
        version = plugins[0].get("version")
    else:
        version = manifest.get("version")
    if version:
        versions.append((path, version))
if len({version for _, version in versions}) > 1:
    detail = ", ".join(f"{path}={version}" for path, version in versions)
    errors.append(f"plugin manifests disagree on version: {detail}")

# The universal installer must stay runnable and cover every Skill and agent.
install_script = ROOT / "scripts" / "install.sh"
if install_script.is_file():
    import os

    if not os.access(install_script, os.X_OK):
        errors.append("scripts/install.sh: must be executable")
    install_source = read("scripts/install.sh")
    if f'SKILLS="{" ".join(SKILLS)}"' not in install_source:
        errors.append("scripts/install.sh: SKILLS list must match the Skill folders")
    for agent in ["claude", "codex", "cursor"]:
        if not re.search(rf"^\s+{agent}\)", install_source, re.MULTILINE):
            errors.append(f"scripts/install.sh: missing a target directory for {agent}")
    completed = subprocess.run(["sh", "-n", str(install_script)], capture_output=True, text=True)
    if completed.returncode != 0:
        errors.append(f"scripts/install.sh: shell syntax error ({completed.stderr.strip()})")
else:
    errors.append("scripts/install.sh: missing")

# Relative Markdown links in source documentation must resolve. Generated bundles
# intentionally preserve source-relative links verbatim, so they are checked by the
# bundle synchronization test rather than by this path resolver.
markdown_files = [
    path
    for path in ROOT.rglob("*.md")
    if "/.git/" not in f"/{path.relative_to(ROOT)}" and not str(path).startswith(str(ROOT / "bundles") + "/")
]

for path in markdown_files:
    for raw_target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
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

# Guard the behavioral decisions most likely to regress into rigid heuristics or
# overlapping ownership.
require_text("focal/SKILL.md", "Use four chunks as a task-screen diagnostic, not a universal limit.", "contextual chunk diagnostic")
require_text("focal/SKILL.md", "not extra numeric weight", "equal discipline weighting")
require_text("focal/reference/review.md", "not a stopwatch threshold or an automatic scoring failure", "quick-orientation probe")
require_text("focal/reference/review.md", "Top moves (up to 3)", "non-quota top moves")
require_text("focal/SKILL.md", "Every applicable state above designed", "contextual state gate")

require_text("compass/SKILL.md", "The outcome-or-anchor test.", "finite/open-ended framing")
require_text("compass/SKILL.md", "what remains when the journey is bounded", "bounded progress rule")
require_text("compass/reference/review.md", "Browser Back can be sufficient", "platform-appropriate retreat rule")
require_text("compass/reference/review.md", "A failed drop test is not automatically release-critical", "consequence-based drop-test severity")

require_text("flywheel/SKILL.md", "full relationship diagnosis evaluates all four plays", "full diagnosis contract")
require_text("flywheel/SKILL.md", "targeted stage review or build runs one play deeply", "targeted stage contract")
require_text("flywheel/reference/review.md", "N/E—outside targeted scope", "targeted N/E output")
require_text("flywheel/reference/review.md", "N/E—insufficient evidence", "evidence-gap N/E output")
require_text("flywheel/reference/review.md", "A P0 at any stage overrides that order", "critical-severity precedence")
require_text("flywheel/reference/review.md", "Missing internal terminology does not cap a UX score by itself", "evidence-based first-value scoring")
require_text("flywheel/reference/emotion.md", "Boundary with Soul", "Flywheel/Soul boundary")

require_text("soul/reference/review.md", "Readiness is deliberately **unscored**", "unscored Readiness")
require_text("soul/reference/review.md", "## The three scored gates", "three-gate Soul scorecard")
require_text("soul/reference/review.md", "zero Net-New moments as valid", "zero-Net-New outcome")
require_text("soul/SKILL.md", "**Target:** <Expected | Elevated | Net-New>", "all three build targets")
require_text("soul/reference/treatments.md", "Elevated is the default ceiling", "contextual frequency/stakes default")
require_text("soul/reference/treatments.md", "Net-New is an exception, not an entitlement", "durable Net-New exception")

require_text("product-judgement/SKILL.md", "scope follows the decisions involved, not the number of screens", "cross-scale scope rule")
require_text("product-judgement/SKILL.md", "One condition may legitimately affect several local scores", "deduplication contract")
require_text("product-judgement/SKILL.md", "Priority changes (up to 4)", "non-quota priorities")

source_contract_files = sorted(
    relative(path)
    for skill in SKILLS
    for path in (ROOT / skill).rglob("*.md")
)
reject_text(source_contract_files, "Never run all four plays by default", "Flywheel full-audit contradiction")
reject_text(source_contract_files, "A real Back on every screen", "universal Back requirement")
reject_text(source_contract_files, "declining is free", "absolute decline-cost claim")
reject_text(source_contract_files, "2–3 biggest moments", "Soul Net-New quota")
reject_text(source_contract_files, "Baseline, Placement, Proportion, and Signature", "obsolete four-gate Soul scorecard")

# Public documentation must expose every Skill, the score contract, and the current
# install/update path without claiming the repository has no maintainer build step.
required_docs = ["README.md"] + [f"{skill}/README.md" for skill in SKILLS]
for path in required_docs:
    if not (ROOT / path).is_file():
        errors.append(f"{path}: missing")
require_text("README.md", "npx skills update -g product-judgement focal compass flywheel soul", "global update command")
require_text("README.md", "`/12` for Focal, Compass, and Soul", "native totals")
require_text("README.md", "`N/E` means **not evaluated**, not zero", "N/E explanation")
require_text("README.md", "no runtime build step", "runtime/build distinction")
reject_text(required_docs, "Claude Code skill", "platform-specific Skill description")
reject_text(["README.md"], "no build step, no dependencies", "obsolete no-build claim")

# Behavioral fixtures are machine-readable and must carry both positive and negative
# assertions so they can drive a later model-evaluation harness.
fixture_path = ROOT / "tests" / "behavioral-contracts.yml"
try:
    fixtures = yaml.safe_load(fixture_path.read_text(encoding="utf-8"))
    if not isinstance(fixtures, list) or len(fixtures) < 8:
        errors.append("tests/behavioral-contracts.yml: expected at least eight fixtures")
    else:
        ids = [fixture["id"] for fixture in fixtures if isinstance(fixture, dict) and "id" in fixture]
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

            for key in ["evidence", "expected", "reject"]:
                value = fixture.get(key)
                valid = (
                    isinstance(value, list)
                    and len(value) > 0
                    and all(isinstance(item, str) and item.strip() for item in value)
                )
                if not valid:
                    errors.append(f"tests/behavioral-contracts.yml: fixture {index} needs a non-empty {key} list")
except FileNotFoundError:
    errors.append("tests/behavioral-contracts.yml: No such file or directory")
except yaml.YAMLError as error:
    errors.append(f"tests/behavioral-contracts.yml: {str(error).splitlines()[0].strip()}")

# Generated bundles must be exact products of the canonical source files.
completed = subprocess.run(
    [sys.executable, str(ROOT / "scripts" / "build_bundles.py"), "--check"],
    capture_output=True,
    text=True,
    cwd=ROOT,
)
if completed.returncode != 0:
    errors.append(f"bundles: {(completed.stderr + completed.stdout).strip()}")

# Lightweight text hygiene catches drift that Markdown renderers often hide.
text_files = sorted(
    {
        path
        for pattern in ["*.md", "*.py", "*.yml", "*.yaml"]
        for path in ROOT.rglob(pattern)
        if "/.git/" not in f"/{path.relative_to(ROOT)}"
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
