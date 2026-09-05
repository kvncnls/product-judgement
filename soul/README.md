# Soul

> **Never boring.**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)

Soul is a Skill for deciding where a working product should remain conventional, where it deserves more craft, and where a genuinely new treatment could make the experience memorable. It places authorship; it does not add decoration everywhere.

Where [Focal](https://github.com/kvncnls/product-judgement/tree/main/focal) owns screen structure, [Compass](https://github.com/kvncnls/product-judgement/tree/main/compass) owns the path, and [Flywheel](https://github.com/kvncnls/product-judgement/tree/main/flywheel) owns relationship momentum, Soul owns treatment and the contextual memory question on a sound path.

## The method

Soul maps the default path and assigns each beat one target tier:

| Tier | Meaning | Appropriate use |
|---|---|---|
| **Expected** | The conventional version, fully functional and restrained. | The moment should simply work, especially when stakes or repetition punish novelty. |
| **Elevated** | The same moment executed with more care. | Small, repeated craft in timing, feedback, transitions, language, or sensory detail. |
| **Net-New** | A materially different experience replaces the obvious treatment. | A selectively authored moment whose reach, memory value, and constraints justify the investment. |

Net-New is a budget, not a quota. A sweep may recommend zero, one, two, or three Net-New moments. Zero is a valid conclusion when the path is high-stakes, highly repetitive, not yet ready, already distinctive through quiet craft, or simply does not contain a moment that earns reinvention.

Soul uses three placement principles:

- **Memory is contextual**—peak and ending cues are hypotheses to compare with reach, utility, stakes, frequency, cost, and actual recall or user-description evidence. A later beat is not automatically stronger.
- **Reach and consequence matter**—default-path moments usually deserve attention before rare error pages, easter eggs, or other dumping grounds, unless user evidence or utility supports another choice.
- **Frequency constrains treatment**—repeated beats need feedback that remains perceivable, comprehensible, and controllable; one-time moments can spend more, but repeat value must be tested before calling it durable. Elevated is the every-run default, while Net-New remains exceptional.

Error, recovery, and interruption states are still reviewed for restraint and appropriateness, but they are not promoted into Net-New candidates merely because expressive treatment is safer there.

## Soul versus Flywheel Emotion

[Flywheel](https://github.com/kvncnls/product-judgement/tree/main/flywheel) asks whether returning preserves or compounds substantive value and whether the relationship earns preference, return, or advocacy. Soul asks how a working moment is authored and remembered. A quiet continuity feature can strengthen Flywheel without becoming a Soul moment; a memorable completion can be strong Soul work without creating a durable reason to return.

## When to use Soul

Reach for Soul when a working path feels anonymous, generic, emotionally flat, over-decorated, or inconsistent about where expressive treatment belongs. It can also identify where motion earns its place, but it does not implement animation.

Soul does not own:

- screen structure or clutter—that is [Focal](https://github.com/kvncnls/product-judgement/tree/main/focal);
- navigation, route economy, or state continuity across a journey—that is [Compass](https://github.com/kvncnls/product-judgement/tree/main/compass);
- activation, value recognition, or durable relationship momentum—that is [Flywheel](https://github.com/kvncnls/product-judgement/tree/main/flywheel);
- brand identity, illustration systems, typography systems, marketing pages, or production animation code.

Use [Product Judgement](https://github.com/kvncnls/product-judgement/tree/main/product-judgement) when the question crosses several scales.

## Install and update

Use the collection’s [installation and update guide](https://github.com/kvncnls/product-judgement#install) for Claude Code, Codex, Cursor, manual folders, and generated single-file bundles.

## Use

The slash-command examples below use Claude Code folder installs. Invoke `/soul` explicitly, or ask an agent with the Skill installed. With the Claude Code plugin, use `/product-judgement:soul`; the umbrella Skill is `/product-judgement:product-judgement`. Other agents use their own picker or invocation, or the Skill name.

### Audit the default path

```text
/soul audit the checkout completion path
```

Soul returns a fixed **happy-path sweep**:

- **Readiness**—an unscored `Ready`, `Deferred`, or `N/E—insufficient evidence` verdict stating whether the path is sound enough for expressive investment and which upstream condition matters.
- **Coverage and Basis**—the exact Screen · Flow · State · Lifecycle reviewed, evidence gaps, and a confirming check.
- **Path map**—the beats, touchpoints, frequency, stakes, and Expected/Elevated/Net-New assignments.
- **Scorecard**—Placement, Proportion, and Signature scored `0–4` when each gate is supported, for a native total of `/12` only when all three are evaluable. Unsupported gates are `N/E—insufficient evidence`; supported findings remain reported.
- **Moments**—up to three ranked Net-New opportunities, which may be `None`, plus Elevated small things.
- **Issues and restraint receipt**—P0–P3 findings, what remains Expected on purpose, and any Focal, Compass, or Flywheel handoff.

Readiness is not a fourth scored gate. Any unsupported Soul-local gate may be `N/E—insufficient evidence`, whether readiness is Ready or Deferred. Keep supported rows, report the next evidence check, and omit the native total, average, band, and weakest-gate ceiling whenever a required gate is N/E. `N/E` is not zero.

Every evaluated score must explain **evidence → consequence → rubric anchor → smallest next-point change**. A `3/4` is the normal target for strong professional work and may say `None justified by the evidence` when no supported change is warranted. A `4/4` means above-and-beyond, unusually effective execution and is intentionally uncommon. Signature does not require a Net-New moment: a distinctive, repeatable Elevated pattern can earn it.

See the [locked sweep output](./reference/review.md#output-formatuse-this-exact-structure) and the collection’s [shared audit contract](https://github.com/kvncnls/product-judgement#shared-audit-contract).

### Build one moment

```text
/soul build the payment-landed moment
```

Soul returns a fixed **Moment Spec**:

- **Moment**—the beat, audience, named feeling, frequency, stakes, and target tier.
- **Why this moment**—its role on the path and the budget decision, including why restraint may be right.
- **Applicable states**—completion, partial failure, permission, recovery/retry, cancel/exit, repeated use, and reduced motion/low-motion marked Applicable, N/A with a reason, or Not shown with a fastest check as each beat warrants.
- **Treatment ladder**—a real Expected floor, the selected target, and higher rungs marked unavailable with their ceiling reason.
- **Held constant**—speed, comprehension, control, convention, safety, and other invariants.
- **Constraints**—brand, technical, accessibility, frequency, and contextual limits.
- **Gates**—binary, unscored checks marked pass, fail with a reason, N/A with a reason, or Not shown with a check.

Expected, Elevated, and Net-New are all valid build targets. See the build route in [SKILL.md](./SKILL.md#routing).

## Give it context

Provide the default path, intended audience, product promise, frequency, stakes, brand constraints, accessibility needs, existing patterns, business goal, and known relationship behavior. A PRD, research, prototype, codebase, analytics, and design references help Soul distinguish a meaningful moment from decoration. Each applicable-state row is marked `Applicable`, `N/A—<reason>`, or `Not shown—<check>`; missing states are marked `not shown` rather than invented, and a missing variant does not automatically make a gate unevaluable.

## What is inside

```text
soul/
├── SKILL.md
├── reference/
│   ├── review.md
│   ├── build.md
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
READINESS  Ready, Deferred, or N/E when unsupported; do not disguise an upstream defect as a Soul score
TIERS      Expected · Elevated · Net-New
BUDGET     zero to three Net-New moments; zero is valid; never fill a quota
RANK       contextual reach × likely memory, utility, stakes, frequency, cost, and evidence
CONSTRAIN  every-run → tested feedback, control, perceivability, and comprehension · high stakes → reassurance first
NEVER      wit at failure · celebration before safety · novelty on every run
```

## License

[MIT](./LICENSE) © 2026 Kevin Canlas.
