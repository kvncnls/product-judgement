# Contributing

Each Skill owns one scale: Focal the screen, Compass the path, Flywheel the relationship, Soul authored memory, and Product Judgement the reconciliation between them. Changes should sharpen those boundaries.

## Setup

Maintainer tooling uses **Python 3.11 or newer** and [uv](https://docs.astral.sh/uv/getting-started/installation/) **0.12.10 or newer**. From this checkout, run:

```bash
uv sync --locked
```

uv creates a local environment and installs the pinned PyYAML dependency from `uv.lock`. The remaining tooling uses Python's standard library, including ZIP creation and validation. The project enforces a 24-hour minimum package release age; preserve any stricter policy in your environment. Installing or using the Skills does not require this maintainer setup.

CI checks Python 3.11 and 3.14 on Linux and macOS. The shell installer continues to run without Python; its regression tests use Python.

## Updating sources and bundles

Shared evidence rules, score anchors, and severity definitions live in `contracts/` and are copied into each standalone Skill. Edit the canonical fragment, then regenerate its inline copies and the bundles:

```bash
uv run scripts/sync_contracts.py
uv run scripts/build_bundles.py
```

Build instructions live in mode-specific references so an audit does not need to load a build template. Bundles are generated artifacts; regenerate them in the same commit as any source edit.

## Verification

Run the repository checks before committing:

```bash
uv run scripts/verify.py
uv run scripts/test_install.py
uv run scripts/test_packages.py
uv run scripts/test_tooling.py
uv run scripts/test_eval.py
uv run scripts/test_eval_cli.py
```

The verifier checks frontmatter, relative links, shared contracts, score arithmetic, fixture structure, plugin manifests, and exact bundle synchronization. Separate offline regression tests exercise installer preservation, archive integrity, source validation, and evaluation harness controls. These checks run in CI without model calls.

The [behavioral fixtures](./tests/README.md) have an opt-in evaluation harness. Its dry run validates prompts and runner arguments without spending model tokens:

```bash
uv run scripts/eval.py --dry-run
```

Real evaluations spend model tokens and never run in CI. Read the fixture guide before running them.

## Building upload packages

For Claude Desktop and Claude.ai, build and verify ZIPs from this checkout after completing setup:

```bash
uv run scripts/package_skills.py --out dist
uv run scripts/verify_packages.py --dir dist
```

Use the packaging script instead of a bare ZIP command. The source Skills carry `argument-hint` for Claude Code, but the Agent Skills specification does not allow that frontmatter key in uploads. The script strips non-spec keys from packages while preserving the source and the formatting of retained fields. Pass `--skill focal` for one Skill, or `--check` to preview stripped fields without writing archives.

The `description` field is capped at 1024 characters; `scripts/verify.py` enforces that ceiling. Keep Claude Code extensions in source, and teach `scripts/package_skills.py` about any new non-spec key before adding it. The archive verifier checks the resulting files, metadata, links, and licenses.

## Cutting a release

The plugin version appears in four manifests: `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.cursor-plugin/plugin.json`, and `.codex-plugin/plugin.json`. Bump all four plugin manifests, rebuild and inspect packages, and review the intended commit before publishing a new tag. Never move an existing release tag. For the prepared 1.1.0 release:

```bash
uv run scripts/build_bundles.py
uv run scripts/verify.py
uv run scripts/package_skills.py --out dist
uv run scripts/verify_packages.py --dir dist
uv run scripts/check_version.py 1.1.0
```

After reviewed changes are committed and pushed, publishing a new `v*` tag runs the checks, confirms that all four plugin versions match the tag, builds and validates the upload packages and combined bundle, and publishes the release. Verify published asset contents before restoring a download recommendation in [the README](./README.md#claude-desktop-and-claudeai).
