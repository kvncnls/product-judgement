# Flywheel

> **Earn the next valuable step.**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)

Flywheel is a Skill for finding where a product loses value and deciding which relationship stage to fix first. Establish the intended cadence and success outcome before judging return, frequency, conversion, or engagement. Recurring products may need return and advocacy; finite or infrequent services may succeed through completion, safe handoff, and exit. Flywheel does not buy attention or prescribe a growth channel.

Where [Focal](https://github.com/kvncnls/product-judgement/tree/main/focal) owns decisions inside a screen and [Compass](https://github.com/kvncnls/product-judgement/tree/main/compass) owns movement through a journey, Flywheel owns whether those experiences build momentum across the relationship.

## The method

A funnel ends. A recurring product relationship can feed useful return and recommendation back into itself; a finite service can end successfully after completion, handoff, and safe exit. Flywheel checks four ordered plays:

| Play | Relationship question | Typical loss |
|---|---|---|
| **Trust** | Is this relevant, credible, and worth continuing? | People leave before meaningful engagement. |
| **Friction** | Can I reach value without avoidable effort, confusion, or exposure? | People engage but do not reach first value. |
| **Wins** | Did value happen, can I recognize it, and is the intended next step earned? | People reach value but do not recognize it, complete, continue, or convert when that outcome is intended. |
| **Emotion** | Does the intended next use preserve or compound something I value? | A recurring relationship drifts, or a finite service ends without confidence or control. |

The order matters because upstream loss reduces the population that can experience anything downstream. A full diagnosis scans all four plays, identifies the earliest consequential leak, and recommends one stage to fix first when a leak is supported; otherwise it reports the validation needed. “Earliest” governs non-critical investment, not emergency response: a P0 at any stage must be stopped or repaired first.

A **relationship leak** is the first point where momentum materially drops against the intended outcome: before engagement, before first value, after value but before recognition or completion, or after repeat use when repeat use is intended. A finite or infrequent service is not defective merely because users do not return. The audit can identify evidence and association, but it does not prove causality without research or experiment data.

## Flywheel Emotion versus Soul

Flywheel’s Emotion play is about substantive relationship behavior: continuity without reconstruction, accumulated value, meaningful preference, and the product’s intended return or completion outcome. [Soul](https://github.com/kvncnls/product-judgement/tree/main/soul) owns authored treatment and memory: which working moments deserve expressive craft and how much. A product can have a strong reason to return with quiet treatment, or a finite service can end with a clear, controlled handoff.

## What “build a stage” means

A stage is one relationship transition, not a screen and not the whole lifecycle. Building a stage means designing the product behavior that helps a defined audience move through one play—for example:

- from first encounter to willing engagement through **Trust**;
- from engagement to first value through **Friction**;
- from first value to recognized value and an earned next step through **Wins**;
- from repeat use to continuity, preference, or advocacy through **Emotion**, when recurring use is intended; otherwise, through a confident completion and exit.

The Stage Spec may touch several screens or states. Focal and Compass still own their local structure and path.

## When to use Flywheel

Reach for Flywheel when people arrive but do not trust, activate, recognize value, complete, return, convert after value, or develop a durable reason to stay, as those outcomes apply. Use a full diagnosis when the leaking stage is unknown; use a targeted stage review when the stage is already established and you need depth. If the intended outcome is met and no supported loss appears, report `No leak observed` and give a validation check instead of inventing a fix.

Flywheel does not own:

- screen composition—that is [Focal](https://github.com/kvncnls/product-judgement/tree/main/focal);
- route clarity, step count, or state across one journey—that is [Compass](https://github.com/kvncnls/product-judgement/tree/main/compass);
- expressive treatment or memorable authorship—that is [Soul](https://github.com/kvncnls/product-judgement/tree/main/soul);
- paid acquisition, SEO, campaign planning, analytics instrumentation, experiment statistics, or manufacturing product-market fit.

Use [Product Judgement](https://github.com/kvncnls/product-judgement/tree/main/product-judgement) when the question crosses several scales.

## Install and update

See the collection’s [installation and update guide](https://github.com/kvncnls/product-judgement#install) for the Skills CLI, Claude Code, Codex, Cursor, manual folders, and generated single-file bundles.

## Use

The slash-command examples below use Claude Code folder installs. Invoke `/flywheel` explicitly, or ask an agent with the Skill installed. With the Claude Code plugin, use `/product-judgement:flywheel`; the umbrella Skill is `/product-judgement:product-judgement`. Other agents use their own picker or invocation, or the Skill name.

### Diagnose the relationship

```text
/flywheel diagnose why activated users do not come back
```

A full diagnosis returns:

- **Verdict**—the earliest evidenced relationship leak, `No leak observed`, or the evidence gap that prevents ordering, plus one stage to fix first when needed.
- **Coverage and Basis**—the exact Screen · Flow · State · Lifecycle reviewed, evidence gaps, and a confirming behavior or metric.
- **Scorecard**—Trust, Friction, Wins, and Emotion scored `0–4` when supported, for a native total of `/16` only when all four are evaluable.
- **Issues**—P0–P3 findings ordered by priority first, then by Trust → Friction → Wins → Emotion within each priority, with exact locators and concrete fixes.
- **Fix this first**—one stage, or `None—no leak observed; validate <check>`, with no invented intervention.
- **Handoffs**—local screen, journey, or authored-treatment work owned by Focal, Compass, or Soul.

A targeted stage review scores only the selected play `/4`. The other three rows are `N/E—outside targeted scope`; Flywheel does not turn a one-stage review into a synthetic `/16` total or common band. A full diagnosis evaluates all four plays, but any play whose rubric is unsupported is `N/E—insufficient evidence`; any `N/E` prevents a `/16` total, average, band, or weakest-play ceiling and makes ordering provisional where the missing evidence matters.

Every evaluated score must explain **evidence → consequence → rubric anchor → smallest next-point change**. A `3/4` is the normal target for strong professional work and may say `None justified by the evidence` when no supported change is warranted. A `4/4` means above-and-beyond, unusually effective execution and is intentionally uncommon.

See the [locked diagnosis output](./reference/review.md#output-formatuse-this-exact-structure) and the collection’s [shared audit contract](https://github.com/kvncnls/product-judgement#shared-audit-contract).

### Build a relationship stage

```text
/flywheel build the first-value stage for a budgeting app
```

Flywheel returns the fixed **Stage Spec** in [reference/build.md](reference/build.md), loaded for a `build` request or when turning a reviewed relationship stage into a proposal. It includes:

- **Stage**—one play, audience, first value, intended cadence, success outcome, stakes, and relationship transition; finite services may define success through completion, handoff, and safe exit.
- **Evidence / assumptions**—supplied facts separated from proposal assumptions.
- **The leak**—what is being lost, the diagnostic hypothesis, and the fastest confirming metric or behavior.
- **The design**—the proposed intervention at that relationship stage.
- **State / applicability inventory**—only relevant completion, partial completion/failure, permission, recovery/retry, cancellation/abandonment, decline, and no-ask states, with N/A reasons for inapplicable states or gates and unknown behavior labeled.
- **Friction kept**—productive or protective effort retained deliberately.
- **The ask**—what value precedes a commercial or social request; declining preserves already-earned value, and any foregone benefit is explicit and noncoercive.
- **Gates**—binary, unscored checks marked pass, fail with a reason, or N/A with a reason.

See the [locked Stage Spec](./reference/build.md#output-format-use-this-exact-structure).

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
│   ├── build.md
│   └── examples.md
├── README.md
├── LICENSE
└── agents/
    └── openai.yaml
```

## Quick reference

```text
DIAGNOSE  leave before engagement → Trust · engage, no first value → Friction
          value occurs, no intended completion/recognition → Wins
          recurring use then drifts → Emotion · finite service ends well → completion, handoff, or safe exit may be success
EARLIEST  among non-critical work, fix the earliest evidenced leak first
P0        stop or repair immediately at any stage; then resume earliest-stage order
FRICTION  remove accidental and cognitive drag · keep protective and productive effort
ASKS      follow relevant value · preserve earned value when declined · disclose tradeoffs
NEVER     hide cost, permission, risk, or reversibility to increase action
```

## License

[MIT](./LICENSE) © 2026 Kevin Canlas.
