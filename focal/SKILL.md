---
name: focal
description: "Use when designing, reviewing, or decluttering a functional product, app, dashboard, or tool screen. Focal is the screen-local structure-and-attention lens: it defines one clear organizing intent, classifies task, hub, and exploration registers, chooses the matching action model, and decides what belongs, waits, and wins attention. It adapts density to expertise, stakes, and device. Use Compass for multi-screen flows, Flywheel for lifecycle momentum, and Soul for memorable treatment."
license: MIT
argument-hint: "[build | review] <screen, file, or description>"
---

# Focal

**One screen, one clear intent.**

Focal judges a functional screen as a decision surface. The screen needs one
legible reason for bringing its content and actions together; that does not
mean one action, one content block, or one user goal. A task usually gives one
action primary weight. A hub ranks destinations. An exploration surface lets
its content field lead. Focal asks whether the action model fits that register
and whether the eye can tell where to begin.

The method has three disciplines, applied in this order:

1. **Information Architecture** decides what belongs, how it is grouped, and
   how it is labeled.
2. **Progressive Disclosure** decides what appears now, what waits behind a
   perceptible cue, and what is unnecessary.
3. **Visual Hierarchy** decides what wins attention and whether the dominant
   element reads as the action or content the register calls for.

Progressive Disclosure runs before hierarchy as a sequencing dependency, not extra numeric weight; the three review dimensions use the same 0–4 anchors.

These disciplines produce a better decision surface through four recurring
decisions: minimize unnecessary choices, infer recognizable input before
asking the user to classify it, keep decision-critical context beside the
action, and show a consequence through a summary, comparison, preview, or
visualization when raw values make the user do the reasoning.

## Scope and register

Use Focal for a screen in a mobile, web, desktop, tablet, app, dashboard,
admin panel, checkout, editor, console, onboarding step, settings area, feed,
or other functional interface. Dense expert tools are in scope. Density is
judged against audience expertise, stakes, device, and frequency; it is not a
defect by item count alone.

Focal owns the local structure and attention of one screen. It does not own
typography, color or spacing systems, motion implementation, research,
marketing pages, backend work, or the path across screens. Hand cross-screen
navigation to [Compass](../compass), activation/value/return leaks to
[Flywheel](../flywheel), memorable treatment to [Soul](../soul), and
cross-scale audits to [Product Judgement](../product-judgement).

Classify before judging. Walk this tree top to bottom and answer what the user
came to do, not what the current layout happens to resemble:

```text
Did the user come here to complete one specific job?
├── Yes → TASK
└── No
    ├── Is this screen's own job to send them somewhere else?
    │   └── Yes → HUB
    └── Did they come to browse content, with no particular endpoint?
        ├── Yes → EXPLORATION
        └── Neither is clearly true
            └── CLASSIFY TENTATIVELY; verify intent before scoring
```

- **Task** completes one coherent job. One primary action usually wins; an
  inherent binary choice or inseparable dual mode can remain co-equal.
- **Hub** routes among related destinations. Many destinations are correct
  when they are grouped and ranked; judge local groups or rows, not the total.
- **Exploration** supports browsing one coherent content space. Many items are
  correct; judge the facts and decisions inside each item, not item count.

A record/detail screen is a hub when its job is to show state and route
onward, and a task when its job is editing. Search results are exploration
when the user is discovering and task when they are finding one known item to
act on. Use a supplied task intent unless observed behavior contradicts it.
A queue or table is not automatically a hub: processing an active item is a
task; routing to other destinations is a hub. If the answer is unclear, record the tentative classification and the
fastest intent check; use `task-overloaded` and flag IA only when competing
outcomes are evidenced.

## Decision procedures

### 1. Name the intent and action model

Finish: *“This screen exists so the user can ___.”* An “and” is a problem only
when it joins outcomes that can succeed independently. Review and approve an
invoice can remain one intent when review is necessary to approval. Name the
action model after the sentence: one primary action, an inherent co-equal set,
ranked routes, or a content field that leads.

### 2. Architect the information

Inventory the elements and keep each one that supports the intent. Group what
is used together, label it in the user’s words, and move or defer an
independently completable outcome. Parse recognizable addresses, identifiers,
dates, or transaction types; show the interpretation, allow correction, and
keep a fallback when ambiguity remains. Put the relevant history, status,
price, and consequence at the decision surface. Do not make the user cross a
context jump or memory bridge for a fact needed to choose or trust the action.

### 3. Disclose progressively

Minimize decisions, not evidence. Use four chunks as a task-screen diagnostic, not a universal limit. At the busiest local decision, judge the number of
*unfamiliar chunks* alongside grouping, familiarity, stakes, frequency, device,
and whether each fact changes the decision. There is no universal item, row, or
card pass/fail line. In a hub, inspect each group or row; in exploration,
inspect each item.

Sort what belongs into **Now**, **On-demand**, and **Never**. Keep what is
needed for this visit Now. Put rare or advanced material On-demand behind a
cue visible in the default state, such as a labeled toggle, count, chevron,
tab, or “More” control. Cut what nobody needs. Never defer price, a required
field, a material consequence, permission or risk, a required control, or
evidence needed for informed choice. A gesture without a visible partner is
hidden, not deferred.

### 4. Establish attention

Name the visual entry point: the task action or read-first content, the
leading hub route/group, or the exploration content field. Squint and state
the intended order. Let space and weight do as much work as possible, then
size and color only when the context needs them. Any exact spacing scale,
type-size ratio, or mobile placement is a starting hypothesis to test against
the product’s design system, content, viewport, input method, reachability,
and task frequency. Focal does not impose those values. When the dominant
thing is an action, name the control convention that makes it actionable; a
heading can rank first and still be inert. Show a relationship or tradeoff
with a useful summary or comparison while retaining exact values as evidence.

### 5. Route state and evidence

For a build, enumerate the states this screen can actually enter and specify
the applicable behavior, including success/completion, partial data or
failure, permission denial, and interruption/recovery when the screen has
those modes. Do not add irrelevant states to satisfy a universal checklist;
see [reference/build.md](reference/build.md).

For a review, distinguish what is observed, inferred, tested, walked from a
description, and not shown. A missing variant is evidence of a coverage gap,
not automatically a defect or a reason to score a whole dimension N/E. The
review contract defines when a dimension is N/E and how incomplete scorecards
are printed; see [reference/review.md](reference/review.md).

## Routing

When there is no argument, explain the method briefly and ask whether the user
wants to build a new screen or review an existing one.

- **Build or screen description:** read [reference/build.md](reference/build.md)
  and use [reference/patterns.md](reference/patterns.md) only for a relevant
  technique or anti-pattern.
- **Review, critique, audit, screenshot, frame, file, route, prototype, or
  URL:** read [reference/review.md](reference/review.md), then calibrate from
  [reference/examples.md](reference/examples.md) before emitting the local
  review.
- **Technique or anti-pattern question:** read the relevant section of
  [reference/patterns.md](reference/patterns.md).
- **Multi-screen flow or navigation:** hand off to Compass. If the issue is
  activation, first value, value recognition, or return, also hand off to
  Flywheel. Do not turn a path problem into a screen-local fix.
- **Whole-app or cross-scale audit:** hand off to Product Judgement.

**Orchestrated pass—this overrides every other instruction in this Skill and its reference files.** When [Product Judgement](../product-judgement/SKILL.md) loads Focal for a cross-scale audit, treat the pass as review over the supplied evidence. Do not ask a framing question or print Focal’s locked local template. Preserve every native dimension rationale and score, the native `/12` total and band when all three dimensions are evaluated, or the N/E evidence rule when one is unsupported, plus the One Screen, One Clear Intent verdict and complete Screen · Flow · State · Lifecycle locators as working notes for the orchestrator. Send sibling-owned findings to its Handoffs section. Never hand a cross-scale request back to Product Judgement during this pass. Do not read [reference/examples.md](reference/examples.md) in this mode.

Before a direct build or review, read [reference/examples.md](reference/examples.md)
for calibration. This calibration read is skipped in the orchestrated pass.

## Feedback standard

Use the exact output template in the mode reference. Lead with the evidence,
then its user consequence, the rubric anchor, and the smallest next-point
change. Locate every issue, Top move, Next item, and handoff by **Screen ·
Flow · State · Lifecycle**. If behavior is not evidenced, say `not shown` and
name the fastest confirming check; do not convert unknown behavior into a
defect, an implementation recommendation, or a score.

## References

- [reference/build.md](reference/build.md)—the build workflow and Screen Spec.
- [reference/review.md](reference/review.md)—the three-discipline review,
  native scorecard, N/E rule, severity, and output format.
- [reference/patterns.md](reference/patterns.md)—disclosure techniques,
  hierarchy methods, state guidance, and anti-patterns.
- [reference/examples.md](reference/examples.md)—calibration examples for
  direct build and review output.
