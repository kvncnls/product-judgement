# Focal

> **One screen, one clear intent.**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)

Focal is a Skill for designing and reviewing the product decisions inside a functional screen: what belongs, what waits, and what deserves attention. It works across mobile, web, desktop, apps, tools, dashboards, and expert interfaces.

“One clear intent” does not mean one action, one content block, or one possible user goal. A task screen usually has one primary action. A hub can offer many ranked destinations. An exploration surface can foreground many items. Focal asks whether the screen has one legible reason for bringing those elements together and an action model that fits the kind of screen it is.

## The method

Focal treats a screen as a decision surface, not a container. Three disciplines support one local conclusion:

```text
                 ONE SCREEN, ONE CLEAR INTENT
                         /      |      \
            Information   Progressive   Visual
            Architecture   Disclosure    Hierarchy
            what belongs   what waits    what wins
```

- **Information Architecture** decides what belongs on the screen and how related information is grouped.
- **Progressive Disclosure** sequences information and choices so the user can decide without unnecessary overload. It does not hide price, risk, requirements, or evidence needed now.
- **Visual Hierarchy** defines the intended attention order. The strongest element or region should match the screen’s action model.

Progressive Disclosure is the main anti-overload lever, but it is not a universal item-count rule. Roughly four decision chunks is a useful diagnostic starting point for an unfamiliar task screen. Experts, high-stakes comparisons, hubs, and exploration surfaces can support more when the information is meaningfully grouped and necessary to the decision.

Focal also asks whether the interface can reduce unnecessary choices by recognizing input, keep decision-critical context beside the action, and show consequences through a useful summary, comparison, preview, or visualization instead of raw data alone. It specifies what the product should make clear; it does not implement parsers, chart systems, or visual styling.

## Screen registers

Focal classifies the screen before judging it:

- **Task**—one coherent job, usually with one primary action. An inherent binary choice or inseparable dual mode can remain co-equal.
- **Hub**—a routing surface where many ranked destinations may be correct. Decision load is judged within meaningful groups, not by counting every route as clutter.
- **Exploration**—a feed, search, grid, or canvas where browsing is the intent and content leads. Decision load is judged at the item or local-choice level.

Audience, expertise, stakes, device, and frequency change what “clear” requires. Density is not automatically a defect.

## When to use Focal

Reach for Focal when a screen feels crowded, unclear, over-explained, under-contextualized, or unable to show what matters now. Use it for both new designs and existing screens.

Focal does not own:

- the route across multiple screens—that is [Compass](../compass);
- activation, value recognition, return, or relationship momentum—that is [Flywheel](../flywheel);
- the placement of memorable or expressive moments—that is [Soul](../soul);
- typography, color, spacing systems, animation implementation, marketing pages, or backend work.

Use [Product Judgement](../product-judgement) when the question crosses several of those scales.

## Install and update

Use the collection’s [installation and update guide](../README.md#install). It covers native plugins, protected folder installs, verified upload packages, and the Skills CLI with the project’s release-age policy.

## Use

Invoke `/focal` explicitly or ask an agent with the Skill installed.

### Build a screen

```text
/focal build a checkout screen for a food-delivery app
```

Focal returns a fixed **Screen Spec**:

- **Screen**—organizing intent, register, audience, and action model.
- **Information**—what stays, moves, merges, or leaves.
- **Disclosure**—what appears Now, On-demand, or Never.
- **Hierarchy**—the intended attention order and focusing mechanism.
- **States**—the variants this screen can actually enter, including success, partial, permission, and recovery behavior when relevant.
- **Gates**—an unscored check of the proposal, with a reason when a gate is not applicable.

See the [locked Screen Spec](./reference/build.md#screen-spec).

### Audit a screen

```text
/focal audit this dashboard
```

Point the agent at a frame, screenshot, component, route, prototype, or running product. Focal returns:

- **Verdict**—Yes or No for One Screen, One Clear Intent when intent is evidenced; `N/E—insufficient evidence` when it cannot be assessed, plus the largest supported local problem.
- **Coverage and Basis**—the exact Screen · Flow · State · Lifecycle reviewed, missing evidence, and a confirming check.
- **Scorecard**—Information Architecture, Progressive Disclosure, and Visual Hierarchy scored `0–4`, with the native `/12` total only when all three dimensions are evaluable.
- **Issues**—P0–P3 findings with exact locators and concrete fixes.
- **Top moves**—up to three high-leverage changes; fewer when fewer are justified.
- **Next**—structural-before-executional sequencing and any Compass, Flywheel, or Soul handoff.

Every score must explain **evidence → consequence → rubric anchor → smallest next-point change**. A `3/4` is the normal target for strong professional work. A `4/4` means above-and-beyond, unusually effective execution and is intentionally uncommon. A total without those row-level explanations is invalid.

See the [locked review output](./reference/review.md#output-formatuse-this-exact-structure) and the collection’s [shared audit contract](../README.md#shared-audit-contract).

## Give it context

The more Focal knows about the user, intent, business goal, constraints, stakes, device, frequency, and surrounding flow, the more useful its decisions become. Include a PRD, research, analytics, requirements, or codebase when available. If a state is not visible or verifiable, the audit marks it `not shown` rather than inventing behavior. A missing variant can be a coverage gap without making the entire dimension N/E; a dimension is `N/E—insufficient evidence` when the available evidence cannot support its rubric.

## What is inside

```text
focal/
├── SKILL.md
├── reference/
│   ├── build.md
│   ├── review.md
│   ├── patterns.md
│   └── examples.md
├── README.md
├── LICENSE
└── agents/
    └── openai.yaml
```

## Quick reference

```text
INTENT     “This screen exists so the user can ___.”
REGISTER   task: focused action · hub: ranked routes · exploration: content leads
IA         include what supports the intent · group meaningfully · label plainly
DISCLOSE   Now / On-demand / Never · fit decision load to audience and stakes
DECIDE     minimize unnecessary choices · infer before asking · keep context nearby
SHOW       make consequences legible; use a preview or visualization when it helps
STATE      specify only applicable variants, including success, partial, permission, and recovery
EVIDENCE   N/E only when a dimension's rubric lacks support; omit total, average, and band if any is N/E
HIERARCHY  one intended attention order · strongest treatment matches the action model
NEVER      hide price, requirements, consequences, or controls needed now
```

## License

[MIT](./LICENSE) © 2026 Kevin Canlas.
