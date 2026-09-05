---
name: compass
description: "Use when designing, building, reviewing, or critiquing a multi-screen flow, journey, finite task-list service, or navigation in a functional product, app, dashboard, or tool. Compass owns the path between screens, states, entry points, progress, retreat, and recovery. Its promise is Never Lost: the user knows where they are, what remains when the journey is bounded, and how to retreat, get home, or leave. Pairs with Focal for single-screen structure. Not for visual styling, copy, code, marketing pages, backend work, or a speculative whole-app sitemap."
license: MIT
argument-hint: "[build | review] <flow, journey, or description>"
---

# Compass

**Never lost.**

Compass is the cross-screen lens. A journey is a sequence of screens and transitions governed by one intent. At every applicable point, the user can answer: *Where am I? What remains when this journey has an end? How do I retreat, get home, or leave?* Focal owns structure inside a screen; Compass owns the path, its seams, and its recovery.

Compass uses three equally weighted disciplines. **Orientation** makes position, meaningful progress or location, and retreat or home legible. **Path Economy** removes needless effort while retaining protection and informed choice. **Continuity** carries context and handles state across transitions, interruption, and re entry when that retention is safe and permitted.

Orientation is the load bearing promise for the Never Lost verdict, but it does not receive extra numeric weight. The native Compass score remains one `0–4` score for each discipline and a `/12` total only when all three are evaluable.

## When to use

Use Compass for onboarding, signup, checkout, setup, wizards, finite task-list services, hub-and-spoke work, drill downs, search and discovery, and any experience where people move between screens to complete or pursue something.

Do not use it for screen-local hierarchy or composition ([Focal](https://github.com/kvncnls/product-judgement/blob/main/focal/SKILL.md)), relationship momentum ([Flywheel](https://github.com/kvncnls/product-judgement/blob/main/flywheel/SKILL.md)), expressive treatment ([Soul](https://github.com/kvncnls/product-judgement/blob/main/soul/SKILL.md)), visual styling, backend behavior, or a speculative whole-app sitemap. Use [Product Judgement](https://github.com/kvncnls/product-judgement/blob/main/product-judgement/SKILL.md) when the decision crosses several scales.

## Methodology: Never Lost

The outcome-or-anchor test. For a finite journey, name one outcome: *“This flow gets the user from ___ to ___.”* If two outcomes can succeed independently, split the flow. For an open ended journey, name one organizing intent and a stable home: *“This space lets the user ___, and ___ is home.”* Do not invent an endpoint for browsing.

The **drop test.** Place the user on each evidenced screen or transition with no memory of arrival. Can they identify their position, what remains when the journey is bounded, and how to proceed, retreat, get home, or leave? Apply only the questions that fit the journey shape.

### Orientation

- Signpost the actual outcome and remaining work. A bounded journey may use named stages, task statuses, a checklist, a stable count, or another clear cue. A counter is optional: a named three stage stepper is valid without one. Open ended work needs position in the space and a route home, not completion progress.
- Show the branch when a choice changes the route; show the hub relationship when a detail screen returns to a center; show task status, available tasks, and the final completion condition in a finite task list.
- Give every owned flow a platform appropriate retreat and escape: in product Back, browser Back when history is meaningful and state safe, a breadcrumb or hub link, Cancel, Close, or Save and return as the service supports. Every screen has a next step or a way out.

### Path Economy

- Count the honest work for the journey shape. Merge redundant screens and round trips, default the common route, and defer setup until users have context. A task list may let users choose task order; do not call that freedom waste or force it into a linear count.
- Infer only safe, useful values. Show the inferred value and its source or meaning, let the user correct it, and provide a manual route when confidence is low. Confirm financial, identity, permission, legal, security, destination, quantity, destructive, or otherwise consequential values before commit.
- Never shorten a path by hiding cost, risk, permission, consequence, or protective confirmation. That is a dark pattern, not economy.

### Continuity

- Show required context at the point of use; do not make the user remember a code, choice, amount, or destination across screens. Within one process, avoid redundant entry while honoring essential, security, and invalid-data exceptions.
- Preserve state across Back when it is safe. Cross session save and return is conditional, not a universal requirement: retain only data the service may safely and permissibly store, with clear expiry, the authentication and authorization appropriate to the data and service at re entry, stale-data revalidation, and a recoverable route when access or retention changes. Explain what will be lost when it cannot be retained.
- Land deep links, notifications, and search results in context. Keep the mental model and focused object stable across the seam. Do not claim persistence, validation, permission, or re entry behavior that the artifact or requirements do not expose.

## Registers: journey types

Classify the journey users are actually on. Take the first match:

```
Is roaming or discovery itself the intent, with no completion event?
├── Yes → OPEN-ENDED
└── No—name one finite outcome
    ├── Are several tasks independently completable in user-chosen order before one final outcome?
    │   └── Yes → TASK-LIST
    ├── Does the user leave a center and return to it repeatedly, with no endpoint beyond the loop?
    │   └── Yes → HUB-AND-SPOKE
    └── Does the path fork on a choice the user makes?
        ├── Yes → BRANCHING
        └── No → LINEAR
```

| Type | Shape | Compass emphasis |
|---|---|---|
| Linear | One path from entry to outcome | Make the outcome and remaining milestones legible; Back retreats with safe state. |
| Branching | A choice sends the user down a distinct route | Name the branch, show how to change it, and prune dead branches. |
| Task-list | Finite task hub → independently completable task details → hub → final review and submit | Let users choose order; show task status and the finite outcome; represent Save and return, expiry, permission, revalidation, and final submit when applicable. |
| Hub-and-spoke | Center → detail → center loop | Keep the hub as home and make the return route explicit; no progress counter is required. |
| Open-ended | Explore a space with no fixed completion | Show location, active refinements, and home; do not invent progress. |

A wizard with optional steps remains linear when it rejoins the same path. A drill down remains part of the surrounding journey unless returning to the center is itself the complete loop. A task list is distinct because it has a finite outcome while allowing independently completed tasks in user chosen order.

## Routing

**Orchestrated pass—this overrides every other instruction in this Skill and its reference files.** When [Product Judgement](https://github.com/kvncnls/product-judgement/blob/main/product-judgement/SKILL.md) orchestrates a cross scale audit, treat Compass as a `review` over the evidence supplied. Do not ask a framing question, invent a state, or emit Compass's standalone template; return Compass findings through Product Judgement's wrapper and its Handoffs section. Never hand a cross-scale request back to Product Judgement; do not read [reference/examples.md](reference/examples.md) during this pass. Use [reference/review.md](reference/review.md) for the native contract and score only what the evidence supports.

- **No argument:** explain Never Lost and ask whether the user is building or reviewing a journey.
- **`build` or a flow description:** read [reference/build.md](reference/build.md), then return its Flow Spec. Use [reference/patterns.md](reference/patterns.md) for techniques.
- **`review` or `audit`:** read [reference/review.md](reference/review.md). It defines the native scorecard, N/E handling, severity, locators, and output.
- **A technique or anti pattern question:** read [reference/patterns.md](reference/patterns.md).

Before a standalone build, read [reference/build.md](reference/build.md) and the relevant patterns. Before a standalone review, read [reference/review.md](reference/review.md) and [reference/examples.md](reference/examples.md) for calibration. The orchestrated Product Judgement pass follows its own evidence and output rules.

## References

- [reference/build.md](reference/build.md): conditional build workflow, state and transition inventory, and Flow Spec.
- [reference/review.md](reference/review.md): native three discipline audit, scoring, evidence gaps, severity, and output format.
- [reference/patterns.md](reference/patterns.md): orientation, task list, path, continuity, and anti pattern techniques.
- [reference/examples.md](reference/examples.md): one evidence bounded review and one finite task list build.
