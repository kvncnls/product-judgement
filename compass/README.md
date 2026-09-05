# Compass

> **Never lost.**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)

Compass is a Skill for designing and reviewing journeys across screens: how people move, know where they are, preserve safe context, and recover or leave. It covers onboarding, checkout, setup, finite task-list services, hub-and-spoke work, drill downs, search, and discovery.

Where [Focal](https://github.com/kvncnls/product-judgement/tree/main/focal) owns structure inside one screen, Compass owns the path and seams between screens. [Flywheel](https://github.com/kvncnls/product-judgement/tree/main/flywheel) owns relationship momentum, and [Soul](https://github.com/kvncnls/product-judgement/tree/main/soul) owns expressive treatment and memory.

## The method

Compass asks three questions at every applicable point:

- **Where am I?** Position in the journey or space.
- **What remains?** Meaningful remaining work when the journey has a finite outcome.
- **How do I retreat, get home, or leave?** A platform-appropriate route that does not trap the user.

Its three native disciplines are equal in numeric weight:

- **Orientation**—position, outcome based progress or location, and retreat/home/exit.
- **Path Economy**—fewest honest steps, with safe visible defaults, correctable inference, and protection for consequential choices.
- **Continuity**—context across seams and state handling that is safe, permitted, time bounded, revalidated, and recoverable.

A named three stage stepper can show “Tasks → Review → Submit” without a numeric counter. A finite task list can show task statuses and a final completion condition while letting users choose task order. Open ended exploration needs location and home, not a progress bar.

## Journey types

Compass classifies the user's actual journey as one of these:

| Type | Shape | Orientation cue |
|---|---|---|
| Linear | One path to one outcome | Outcome and meaningful milestones |
| Branching | A choice creates a distinct route | Branch identity and a way to change it |
| Task-list | Finite task hub → tasks in user chosen order → final review/submit | Task statuses, hub return, finite completion condition |
| Hub-and-spoke | Center → detail → center loop | Active location and route back to the hub |
| Open-ended | Explore with no fixed completion | Location, refinements, and home |

The shape determines the cue; no progress widget is mandatory by type. A task list is finite even though users can complete tasks in different orders.

## Install and invoke

Use the collection’s [installation and update guide](https://github.com/kvncnls/product-judgement#install) for native plugins, protected folder installs, verified uploads, and the Skills CLI with the project’s release-age policy.

The examples below use `/compass build <journey>` or `/compass review <journey>` for a Claude Code folder install. With the Claude Code plugin, use `/product-judgement:compass`. In other agents, use their own Skill picker or invocation syntax, or ask for Compass by name. When the decisions span multiple scales, use [Product Judgement](https://github.com/kvncnls/product-judgement/tree/main/product-judgement).

## Build a journey

```text
/compass build the license renewal service
```

For a build, provide the intended outcome or home anchor, audience and stakes, entry points, journey type, screens or task list, and applicable states and transitions. For a task list, include user chosen order, task statuses, final review/submit, and applicable Save and return, permission, expiry, revalidation, and recovery behavior. Save and return is conditional: retain only data the service may safely and permissibly store, with expiry, appropriate re-entry authorization, revalidation, and recovery; otherwise explain what is lost and provide a safe re-entry or restart. The build reference returns a Flow Spec with an explicit state/transition inventory.

Read the conditional [Flow Spec](./reference/build.md) and [build patterns](./reference/patterns.md).

## Audit a journey

```text
/compass review the license renewal flow
```

Provide ordered screens or routes and the states actually available: default, loading, validation/error, retry, permission, Back, refresh, branch changes, task order, interruption, Save and return, re entry, deep link, review, and submit as applicable. Screens do not prove behavior they do not show.

The audit returns a **Never Lost** verdict, exact Screen · Flow · State · Lifecycle coverage, a `0–4` score for each evaluable discipline, evidence based issues, and ranked next moves. A missing variant does not automatically make a dimension unevaluable. Use `N/E—insufficient evidence` when the artifact cannot support that rubric; report the next evidence check and do not invent an issue or implementation. If any dimension is N/E, the native total, average, band, and weakest dimension ceiling are omitted.

Read the [locked review output](./reference/review.md#output-format-use-this-exact-structure) and [review examples](./reference/examples.md). The review uses the shared score anchors and severity definitions in its own contract.

## Evidence anchors

[GOV.UK's task list guidance](https://design-system.service.gov.uk/components/task-list/) supports user chosen task order, multiple sessions, task statuses, and a final completion condition. [W3C's Redundant Entry guidance](https://www.w3.org/WAI/WCAG22/Understanding/redundant-entry.html) addresses repeated information within one process and says it does not require cross session storage. These are evidence anchors, not universal compliance certification or automatic product requirements.

## Files

```text
compass/
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
FRAME      finite: entry → outcome · task-list: tasks → hub → final submit · open-ended: intent + home
ORIENT     outcome based cue or location · retreat/home · exit · no widget quota
ECONOMY    fewest honest steps · safe visible defaults · correctable inference · confirmed consequence
CARRY      context across seams · conditional state · expiry and revalidation · recoverable re entry
NEVER      dead ends, traps, silent resets, hidden consequence, or invented behavior
```

## License

[MIT](./LICENSE) © 2026 Kevin Canlas.
