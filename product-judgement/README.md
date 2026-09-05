# Product Judgement

> **Audit the product as a connected system.**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)

Product Judgement is the holistic audit for the four foundational Skills in this collection:

- [Focal](../focal) owns decisions inside the screen.
- [Compass](../compass) owns movement across the journey.
- [Flywheel](../flywheel) owns value and momentum across the relationship.
- [Soul](../soul) owns authorship and memory on a working path.

It runs all four against one evidence map, preserves their boundaries and native scorecards, deduplicates overlapping symptoms, and returns one prioritized sequence of changes. It is not a fifth design scale and does not create a collection-wide score.

## When to use it

Reach for Product Judgement when:

- you want to audit a whole app, product area, or consequential flow across several scales;
- the product feels incoherent but the source of the problem is unclear;
- several local Skills identify related symptoms and you need one implementation order;
- a screen, path, relationship stage, and memorable moment depend on one another.

Scope follows the decisions involved, not the number of screens. One onboarding flow may warrant Product Judgement if the question includes its screens, route, first value, return, and authorship. A clearly local question should use the corresponding foundational Skill directly.

## How the Skills work together

Product Judgement assigns every condition one primary owner while preserving legitimate downstream consequences:

| Question | Primary owner |
|---|---|
| What belongs here, what waits, and what wins attention? | **Focal** |
| Can the user move, orient, preserve state, and recover? | **Compass** |
| Does the relationship earn trust, first value, recognition, return, or advocacy? | **Flywheel** |
| Once the floor holds, what deserves authored or memorable treatment? | **Soul** |

The common overlaps are deliberate but bounded:

- **Compass and Flywheel:** Compass asks whether the route works; Flywheel asks whether that route earns the next relationship stage. Lost state is primarily Compass. A coherent but over-demanding setup before value is primarily Flywheel.
- **Flywheel and Soul:** Flywheel asks whether value compounds into a substantive reason to return; Soul asks how a working moment is treated and remembered. Novelty is not a retention strategy, and continuity does not need spectacle.

One condition may lower more than one local score, but it appears once in the cross-scale issue ledger with one owner, one fix, and named dependencies.

## What it returns

Product Judgement is audit-only. It returns:

- **Verdict**—the largest cross-scale issue and the kind of work the product needs.
- **Coverage and Basis**—the exact Screen · Flow · State · Lifecycle reviewed, material gaps, evidence type, and a confirming check.
- **Four native scorecards**—Focal `/12`, Compass `/12`, Flywheel `/16`, and Soul `/12` only when every required dimension is evaluable, each with component rationales.
- **Cross-scale issue ledger**—deduplicated P0–P3 findings with one primary owner and exact implementation locators.
- **Priority changes**—zero to four concrete, warranted changes ordered by consequence and dependency; no filler and no reserved slot for any Skill.
- **Handoffs and validation**—local work that belongs to a foundational Skill and the fastest check for the most consequential uncertain claim.

Every component score must explain **evidence → consequence → rubric anchor → smallest next-point change**. Native totals are never averaged together. Any dimension unsupported by the available evidence is `N/E—insufficient evidence`, not zero. A missing variant need not invalidate an otherwise supported dimension. Soul Readiness remains unscored. Any incomplete native scorecard receives no total, average, common band, or weakest-dimension ceiling. Unknown behavior becomes a validation check, not an implementation fix.

## Use

```text
/product-judgement audit the app
```

You can point the agent at a codebase, live product, prototype, Figma or Paper frames, screenshots, or a product description. A codebase is recommended because it can expose routes, state transitions, persistence, validation, copy, failure behavior, and re-entry that static frames cannot prove.

For Figma or Paper, select the relevant frames in sequence and include meaningful loading, empty, error, success, permission, interruption, and re-entry variants. Product Judgement marks unsupported behavior `not shown` rather than inventing it.

## Give it context

Provide the PRD, business goal, success criteria, primary audience, user intent, first-value event, constraints, stakes, research, analytics, support themes, experiment history, and technical or regulatory requirements when available. The more relevant context the audit receives, the more specific and defensible its decisions become.

Missing context does not stop the audit. It becomes an explicit assumption or evidence gap with a validating check.

## Install and update

Product Judgement needs all four foundational Skills. Use the complete plugin or installer in the root [installation and update guide](../README.md#install). That guide includes native plugins, protected folder installation, upload packages, and generated single-file bundles.

## Boundaries

Product Judgement does not implement the changes it recommends. It is not a design-system analyzer, component or token validator, visual-regression suite, animation library, user-research substitute, analytics platform, product strategy, or production renderer. Soul may identify where motion earns its place; another tool implements it.

For build work, route to the local output you need: Focal’s Screen Spec, Compass’s Flow Spec, Flywheel’s Stage Spec, or Soul’s Moment Spec.

## What is inside

```text
product-judgement/
├── SKILL.md
├── README.md
├── LICENSE
└── agents/
    └── openai.yaml
```

## License

[MIT](./LICENSE) © 2026 Kevin Canlas.
