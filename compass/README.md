# Compass

> **Never lost.**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)

Compass is a Skill for designing and reviewing the product decisions across a journey: how people move, understand where they are, preserve context, and recover or leave. It covers onboarding, checkout, setup, wizards, hub-and-spoke work, drill-down, search, discovery, and other cross-screen behavior.

Where [Focal](../focal) owns the structure and attention inside a screen, Compass owns the path between screens and states.

## The method

A journey can be finite or open-ended:

- A **finite journey** has an entry and a meaningful outcome, such as completing checkout or connecting an account.
- An **open-ended journey** has a stable intent and home anchor rather than a fabricated finish line, such as browsing a feed, exploring a map, or searching a catalog.

Compass evaluates three disciplines:

```text
                         NEVER LOST
                         /    |    \
                Orientation  Path   Continuity
                             Economy
                where am I   honest  do the seams hold
                / how out    effort  and state survive
```

- **Orientation**—the user can understand position, available direction, and a platform-appropriate way to retreat, return home, or exit. Finite journeys also make meaningful progress or remaining work legible.
- **Path Economy**—the journey uses the fewest honest steps for its intent. It removes waste without hiding cost, risk, permission, or protective work.
- **Continuity**—context and state survive transitions, retreat, interruption, resumption, and alternate entry points.

Orientation is load-bearing for the Never Lost verdict, but all three disciplines keep equal numeric weight. Compass does not force progress bars onto exploration, fabricate destinations for roaming, or require a literal Back control on every screen.

## Journey types

Compass adapts to linear, branching, hub-and-spoke, interruptible, and open-ended journeys. The same behavior can be correct in one type and harmful in another: a skip may support an expert workflow, a confirmation may be necessary protection, and discovery itself may be the user’s intended outcome.

## When to use Compass

Reach for Compass when users may lose position, repeat work, hit a dead end, endure avoidable steps, arrive through a deep link without context, or fail to resume after interruption.

Compass does not own:

- structure or attention inside one screen—that is [Focal](../focal);
- whether a journey earns trust, first value, return, or advocacy across the relationship—that is [Flywheel](../flywheel);
- expressive or memorable treatment—that is [Soul](../soul);
- typography, color, animation implementation, marketing pages, backend behavior, or a speculative whole-app sitemap.

Use [Product Judgement](../product-judgement) when the question crosses several scales.

## Install and update

Install Compass globally with the [Skills CLI](https://skills.sh/docs/cli):

```bash
npx skills add kvncnls/product-judgement --skill compass -g
```

Update an installation tracked by the CLI:

```bash
npx skills update -g compass
```

See the collection’s [installation and update guide](../README.md#install) for Claude Code, Codex, Cursor, manual folders, and generated single-file bundles.

## Use

Invoke `/compass` explicitly or ask an agent with the Skill installed.

### Build a journey

```text
/compass build the onboarding journey for a budgeting app
```

Compass returns a fixed **Flow Spec**:

- **Flow**—entry, type, audience, and finite outcome or open-ended intent and home anchor.
- **Steps**—the ordered path, branches, optional work, and repeat behavior.
- **Cut**—what was removed or merged and which protection was retained deliberately.
- **Orientation**—position, progress when bounded, and retreat/home/exit behavior.
- **Continuity**—what carries forward and survives interruption, plus how alternate entries land.
- **Gates**—a binary, unscored check of the proposal.

See the [locked Flow Spec](./SKILL.md#build-outputthe-flow-spec-use-this-exact-structure).

### Audit a journey

```text
/compass audit the onboarding flow
```

Select or expose the full sequence when possible, including branches, errors, retreat, interruption, resumption, and re-entry. Compass returns:

- **Verdict**—Yes or No for Never Lost, plus the largest journey break.
- **Coverage and Basis**—the exact Screen · Flow · State · Lifecycle walked, missing evidence, and a confirming check.
- **Outcome / anchor**—the finite outcome or open-ended intent and stable home used to judge the path.
- **Scorecard**—Orientation, Path Economy, and Continuity scored `0–4`, for a native total of `/12`.
- **Issues**—P0–P3 findings with exact locators and concrete fixes.
- **Top moves**—up to three high-leverage changes; fewer when fewer are justified.
- **Next**—structural-before-executional sequencing and any Focal, Flywheel, or Soul handoff.

Every score must explain **evidence → consequence → rubric anchor → smallest next-point change**. A `3/4` is the normal target for strong professional work. A `4/4` means above-and-beyond, unusually effective execution and is intentionally uncommon. A total without those row-level explanations is invalid.

See the [locked review output](./reference/review.md#output-formatuse-this-exact-structure) and the collection’s [shared audit contract](../README.md#shared-audit-contract).

## Give it context

Provide the journey’s user intent, entry points, audience, stakes, business goal, branch rules, persistence behavior, and technical constraints. A PRD, route map, prototype, codebase, analytics, and support evidence make the audit more specific. Screens alone rarely prove state persistence or resumption; Compass marks unsupported behavior `not shown` instead of guessing.

## What is inside

```text
compass/
├── SKILL.md
├── reference/
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
FRAME      finite: entry → outcome · open-ended: intent + stable home anchor
STEPS      fewest honest steps · remove waste, not protection
ORIENT     position · meaningful direction · progress only when bounded
RETREAT    platform-appropriate back, home, close, cancel, or exit behavior
CARRY      context survives transitions, retreat, interruption, and re-entry
NEVER      dead ends, traps, silent resets, or shortcuts that hide consequence
```

## License

[MIT](./LICENSE) © 2026 Kevin Canlas.
