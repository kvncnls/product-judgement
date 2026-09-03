# Flywheel

> **Earn the second visit.**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)

Flywheel is a Skill for finding where a product loses people who already showed up and deciding which relationship stage to fix first. It does not buy attention or prescribe a growth channel. It examines what happens from first encounter through first value, recognized value, return, and durable preference.

Where [Focal](../focal) owns decisions inside a screen and [Compass](../compass) owns movement through a journey, Flywheel owns whether those experiences build momentum across the relationship.

## The method

A funnel ends. A healthy product relationship feeds future engagement, return, and recommendation back into itself. Flywheel checks four ordered plays:

| Play | Relationship question | Typical loss |
|---|---|---|
| **Trust** | Is this relevant, credible, and worth continuing? | People leave before meaningful engagement. |
| **Friction** | Can I reach value without avoidable effort, confusion, or exposure? | People engage but do not reach first value. |
| **Wins** | Did value happen, can I recognize it, and is the next step earned? | People reach value but do not return, convert, or continue. |
| **Emotion** | Does returning preserve or compound something I value? | Repeat users drift because the relationship does not deepen. |

The order matters because upstream loss reduces the population that can experience anything downstream. A full diagnosis scans all four plays, identifies the earliest consequential leak, and recommends one stage to fix first. “Earliest” governs non-critical investment, not emergency response: a P0 at any stage must be stopped or repaired first.

A **relationship leak** is the first point where momentum materially drops: before engagement, before first value, after value but before recognition or return, or after repeat use. The audit can identify evidence and association, but it does not prove causality without research or experiment data.

## Flywheel Emotion versus Soul

Flywheel’s Emotion play is about substantive relationship behavior: continuity without reconstruction, accumulated value, meaningful preference, return, and advocacy. [Soul](../soul) owns authored treatment and memory: which working moments deserve expressive craft and how much. A product can have a strong reason to return with quiet treatment, or a memorable moment that does not create durable relationship value.

## What “build a stage” means

A stage is one relationship transition, not a screen and not the whole lifecycle. Building a stage means designing the product behavior that helps a defined audience move through one play—for example:

- from first encounter to willing engagement through **Trust**;
- from engagement to first value through **Friction**;
- from first value to recognized value and an earned next step through **Wins**;
- from repeat use to continuity, preference, or advocacy through **Emotion**.

The Stage Spec may touch several screens or states. Focal and Compass still own their local structure and path.

## When to use Flywheel

Reach for Flywheel when people arrive but do not trust, activate, recognize value, return, convert after value, or develop a durable reason to stay. Use a full diagnosis when the leaking stage is unknown; use a targeted stage review when the stage is already established and you need depth.

Flywheel does not own:

- screen composition—that is [Focal](../focal);
- route clarity, step count, or state across one journey—that is [Compass](../compass);
- expressive treatment or memorable authorship—that is [Soul](../soul);
- paid acquisition, SEO, campaign planning, analytics instrumentation, experiment statistics, or manufacturing product-market fit.

Use [Product Judgement](../product-judgement) when the question crosses several scales.

## Install and update

Install Flywheel globally with the [Skills CLI](https://skills.sh/docs/cli):

```bash
npx skills add kvncnls/product-judgement --skill flywheel -g
```

Update an installation tracked by the CLI:

```bash
npx skills update -g flywheel
```

See the collection’s [installation and update guide](../README.md#install) for Claude Code, Codex, Cursor, manual folders, and generated single-file bundles.

## Use

Invoke `/flywheel` explicitly or ask an agent with the Skill installed.

### Diagnose the relationship

```text
/flywheel diagnose why activated users do not come back
```

A full diagnosis returns:

- **Verdict**—the earliest evidenced relationship leak, or the evidence gap that prevents ordering, plus the one stage to fix first.
- **Coverage and Basis**—the exact Screen · Flow · State · Lifecycle reviewed, evidence gaps, and a confirming behavior or metric.
- **Scorecard**—Trust, Friction, Wins, and Emotion scored `0–4` when supported, for a native total of `/16` only when all four are evaluable.
- **Issues**—P0–P3 findings ordered from earlier to later relationship stages, with exact locators and concrete fixes.
- **Fix this first**—one stage, the reason it precedes downstream work, and what becomes worthwhile afterward.
- **Handoffs**—local screen, journey, or authored-treatment work owned by Focal, Compass, or Soul.

A targeted stage review scores only the selected play `/4`. The other three rows are `N/E—outside targeted scope`; Flywheel does not turn a one-stage review into a synthetic `/16` total or common band. A full diagnosis evaluates all four plays, but an entirely unexposed play is `N/E—insufficient evidence`; any `N/E` prevents a `/16` total and makes the earliest-stage ordering provisional.

Every evaluated score must explain **evidence → consequence → rubric anchor → smallest next-point change**. A `3/4` is the normal target for strong professional work. A `4/4` means above-and-beyond, unusually effective execution and is intentionally uncommon.

See the [locked diagnosis output](./reference/review.md#output-formatuse-this-exact-structure) and the collection’s [shared audit contract](../README.md#shared-audit-contract).

### Build a relationship stage

```text
/flywheel build the first-value stage for a budgeting app
```

Flywheel returns a fixed **Stage Spec**:

- **Stage**—one play, audience, first value, stakes, and relationship transition.
- **The leak**—what is being lost and the fastest confirming metric or behavior.
- **The design**—the proposed intervention at that relationship stage.
- **Friction kept**—productive or protective effort retained deliberately.
- **The ask**—what value precedes a commercial or social request; declining preserves already-earned value, and any foregone benefit is explicit and noncoercive.
- **Gates**—a binary, unscored check of the proposal.

See the [locked Stage Spec](./SKILL.md#design-a-relationship-stage-the-five-moves).

## Give it context

Provide the audience, product promise, first value, business model, stakes, funnel or cohort evidence, lifecycle behavior, and known constraints. A PRD, analytics, research, support themes, experiment history, and codebase help separate a visible symptom from a plausible cause. Flywheel labels uncertain claims and names a confirming test instead of presenting correlation as proof.

## What is inside

```text
flywheel/
├── SKILL.md
├── reference/
│   ├── trust.md
│   ├── friction.md
│   ├── wins.md
│   ├── emotion.md
│   ├── review.md
│   └── examples.md
├── README.md
├── LICENSE
└── agents/
    └── openai.yaml
```

## Quick reference

```text
DIAGNOSE  leave before engagement → Trust · engage, no first value → Friction
          value occurs, no recognition/return → Wins · repeat use, then drift → Emotion
EARLIEST  among non-critical work, fix the earliest evidenced leak first
P0        stop or repair immediately at any stage; then resume earliest-stage order
FRICTION  remove accidental and cognitive drag · keep protective and productive effort
ASKS      follow relevant value · preserve earned value when declined · disclose tradeoffs
NEVER     hide cost, permission, risk, or reversibility to increase action
```

## License

[MIT](./LICENSE) © 2026 Kevin Canlas.
