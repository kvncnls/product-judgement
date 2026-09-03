# Soul

> **Never boring.**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)

Soul is a Skill for deciding where a working product should remain conventional, where it deserves more craft, and where a genuinely new treatment could make the experience memorable. It places authorship; it does not add decoration everywhere.

Where [Focal](../focal) owns screen structure, [Compass](../compass) owns the path, and [Flywheel](../flywheel) owns relationship momentum, Soul owns the treatment and memory of moments on a sound path.

## The method

Soul maps the default path and assigns each beat one target tier:

| Tier | Meaning | Appropriate use |
|---|---|---|
| **Expected** | The conventional version, fully functional and restrained. | The moment should simply work, especially when stakes or repetition punish novelty. |
| **Elevated** | The same moment executed with more care. | Small, repeated craft in timing, feedback, transitions, language, or sensory detail. |
| **Net-New** | A materially different experience replaces the obvious treatment. | A selectively authored moment whose reach, memory value, and constraints justify the investment. |

Net-New is a budget, not a quota. A sweep may recommend zero, one, two, or three Net-New moments. Zero is a valid conclusion when the path is high-stakes, highly repetitive, not yet ready, already distinctive through quiet craft, or simply does not contain a moment that earns reinvention.

Soul uses three placement principles:

- **Peak and ending matter**—larger treatments belong where they can shape memory, not at arbitrary decorative points.
- **Reach matters**—default-path moments usually deserve attention before rare error pages, easter eggs, or other dumping grounds.
- **Frequency constrains treatment**—what happens every run must survive repetition; one-time moments can spend more. Elevated is the every-run default, while Net-New must prove durable utility beyond surprise.

Error, recovery, and interruption states are still reviewed for restraint and appropriateness, but they are not promoted into Net-New candidates merely because expressive treatment is safer there.

## Soul versus Flywheel Emotion

[Flywheel](../flywheel) asks whether returning preserves or compounds substantive value and whether the relationship earns preference, return, or advocacy. Soul asks how a working moment is authored and remembered. A quiet continuity feature can strengthen Flywheel without becoming a Soul moment; a memorable completion can be strong Soul work without creating a durable reason to return.

## When to use Soul

Reach for Soul when a working path feels anonymous, generic, emotionally flat, over-decorated, or inconsistent about where expressive treatment belongs. It can also identify where motion earns its place, but it does not implement animation.

Soul does not own:

- screen structure or clutter—that is [Focal](../focal);
- navigation, route economy, or state continuity across a journey—that is [Compass](../compass);
- activation, value recognition, or durable relationship momentum—that is [Flywheel](../flywheel);
- brand identity, illustration systems, typography systems, marketing pages, or production animation code.

Use [Product Judgement](../product-judgement) when the question crosses several scales.

## Install and update

Install Soul globally with the [Skills CLI](https://skills.sh/docs/cli):

```bash
npx skills add kvncnls/product-judgement --skill soul -g
```

Update an installation tracked by the CLI:

```bash
npx skills update -g soul
```

See the collection’s [installation and update guide](../README.md#install) for Claude Code, Codex, Cursor, manual folders, and generated single-file bundles.

## Use

Invoke `/soul` explicitly or ask an agent with the Skill installed.

### Audit the default path

```text
/soul audit the checkout completion path
```

Soul returns a fixed **happy-path sweep**:

- **Readiness**—an unscored `Ready` or `Deferred` verdict stating whether the path is sound enough for expressive investment and which upstream condition matters.
- **Coverage and Basis**—the exact Screen · Flow · State · Lifecycle reviewed, evidence gaps, and a confirming check.
- **Path map**—the beats, touchpoints, frequency, stakes, and Expected/Elevated/Net-New assignments.
- **Scorecard**—Placement, Proportion, and Signature scored `0–4`, for a native total of `/12` when all three are evaluable.
- **Moments**—up to three ranked Net-New opportunities, which may be `None`, plus Elevated small things.
- **Issues and restraint receipt**—P0–P3 findings, what remains Expected on purpose, and any Focal, Compass, or Flywheel handoff.

Readiness is not a fourth scored gate. If a Deferred path makes a Soul-local gate genuinely unevaluable, that row is `N/E`; Soul reports no native total or common band until the evidence or upstream condition is resolved. `N/E` is not zero.

Every evaluated score must explain **evidence → consequence → rubric anchor → smallest next-point change**. A `3/4` is the normal target for strong professional work. A `4/4` means above-and-beyond, unusually effective execution and is intentionally uncommon. Signature does not require a Net-New moment: a distinctive, repeatable Elevated pattern can earn it.

See the [locked sweep output](./reference/review.md#output-formatuse-this-exact-structure) and the collection’s [shared audit contract](../README.md#shared-audit-contract).

### Build one moment

```text
/soul build the payment-landed moment
```

Soul returns a fixed **Moment Spec**:

- **Moment**—the beat, audience, named feeling, frequency, stakes, and target tier.
- **Why this moment**—its role on the path and the budget decision, including why restraint may be right.
- **Treatment ladder**—only the rungs from Expected through the selected target. If Expected is the target, no more expressive rung is prescribed.
- **Held constant**—speed, comprehension, convention, safety, and other invariants.
- **Constraints**—brand, technical, accessibility, frequency, and contextual limits.
- **Gates**—a binary, unscored check of the proposal.

Expected, Elevated, and Net-New are all valid build targets. See the [locked Moment Spec](./SKILL.md#build-the-five-moves).

## Give it context

Provide the default path, intended audience, product promise, frequency, stakes, brand constraints, accessibility needs, existing patterns, business goal, and known relationship behavior. A PRD, research, prototype, codebase, analytics, and design references help Soul distinguish a meaningful moment from decoration. Missing states are marked `not shown` rather than invented.

## What is inside

```text
soul/
├── SKILL.md
├── reference/
│   ├── review.md
│   ├── moments.md
│   ├── treatments.md
│   └── examples.md
├── README.md
├── LICENSE
└── agents/
    └── openai.yaml
```

## Quick reference

```text
MAP        default-path beats · touchpoint · frequency · stakes · lifecycle
READINESS  Ready or Deferred; do not disguise an upstream defect as a Soul score
TIERS      Expected · Elevated · Net-New
BUDGET     zero to three Net-New moments; zero is valid; never fill a quota
RANK       reach × memory, tempered by stakes, frequency, and feasibility
CONSTRAIN  every-run → durable utility, speed, and feel · high stakes → reassurance first
NEVER      wit at failure · celebration before safety · novelty on every run
```

## License

[MIT](./LICENSE) © 2026 Kevin Canlas.
