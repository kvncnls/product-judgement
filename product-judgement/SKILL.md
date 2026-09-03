---
name: product-judgement
description: "Use when auditing an existing product, app, feature, or consequential flow across multiple Product Judgement scales: screen structure (Focal), multi-screen journeys (Compass), relationship value and retention (Flywheel), and memorable moments (Soul). Run for a holistic app audit, cross-scale critique, or prioritized UX review using a codebase, live product, prototype, Figma/Paper frames, screenshots, or a description. Prefer a codebase because it exposes behavior, state, and lifecycle context. Do not use when the request is clearly confined to one scale; invoke that local Skill instead. Requires the four foundational Skills installed alongside it; it audits the scales it can load and marks any it cannot `N/E`. Not for implementation, design-system analysis, visual styling, animation implementation, research, or analytics."
license: MIT
argument-hint: "[audit] <product, codebase, prototype, or frames>"
---

# Product Judgement

**Audit the product as a connected system.**

Product Judgement is the orchestration Skill for the four foundational Skills:

- **Focal**—what belongs on a screen, what waits, and what wins attention.
- **Compass**—how a person moves between screens without getting lost.
- **Flywheel**—where momentum drops across the relationship and what earns the next stage.
- **Soul**—which working moments deserve craft and memory.

It is not a fifth design lens and it does not replace the four local methodologies. It runs them against a shared evidence map, keeps their boundaries intact, reconciles their findings, and returns one prioritized audit. Do not invent a fifth score or average the native totals together.

## Use it when

Use Product Judgement when the question is larger than one screen, one flow, one relationship stage, or one expressive moment:

- audit the whole app or a meaningful product area;
- find why a working product feels incoherent, hard to navigate, low-value, or forgettable;
- decide which UX problem to fix first when several Skills identify related issues;
- reconcile screen, journey, relationship, and memory findings into one implementation sequence.

For a question clearly confined to one scale, invoke the local Skill directly. A single dashboard belongs to Focal; a route-orientation problem belongs to Compass; a first-value or retention problem belongs to Flywheel; a happy-path authorship problem belongs to Soul. A single onboarding flow can still warrant Product Judgement when the question spans screen decisions, path integrity, first value, and memory—scope follows the decisions involved, not the number of screens.

## Evidence and context

Accept a codebase, live product, clickable prototype, Figma or Paper frames, screenshots, or a product description. Also accept the surrounding product context: the PRD (Product Requirements Document), product brief, strategy or goal documents, user research, personas, journey maps, analytics or funnel data, support themes, experiment history, and technical, accessibility, legal, or safety constraints. The artifact tells you what exists; these materials explain why it exists, for whom, and what success means. The more relevant context available, the more specific and defensible the audit. Prefer the codebase when it is available because it can expose routes, components, state transitions, validation, persistence, re-entry behavior, copy, and implementation constraints that frames cannot.

Before auditing, collect or infer the following and label assumptions:

- business goal, product requirements, success criteria, and the outcome that matters;
- primary audience, expertise, situation, and stakes;
- the user's intended first-value event;
- the primary entry points and journeys;
- known constraints, evidence, metrics, or unresolved questions.

Do not stall when context is missing. State the missing context in **Coverage** or **Basis**, use `not shown` for consequential states or lifecycle moments that the evidence does not expose, and name the fastest validating check.

### Figma and Paper

Frames are valid evidence for visible structure, hierarchy, copy, and the transitions they actually show. They are not proof of behavior. When auditing from frames:

1. Point the agent at one frame or component for Focal.
2. Select the ordered set of frames, including branches and meaningful variants, for Compass. Say which frames are in sequence; do not make the agent guess the path order.
3. Include first-run, success, error, empty, loading, permission, interruption, and re-entry frames when they exist.
4. Mark persistence, validation, timing, and unseen lifecycle behavior as `not shown` unless the frames or prototype demonstrate them.

Useful prompts include `/focal audit this dashboard` and `/compass audit this flow`. A holistic pass is `/product-judgement audit this app` with the relevant frames selected.

## Keep the four boundaries clear

Use the failure's location and consequence to assign a primary owner. Several Skills may mention the same symptom, but the holistic audit prints one issue with one owner and any dependencies.

| Question | Primary owner | Keep it out of this Skill |
|---|---|---|
| What belongs here, what waits, and what should draw attention? | **Focal**—the screen-local decision surface | Do not turn it into a navigation, retention, or expressive-treatment fix. |
| Can the user reach the destination, know where they are, and keep their state? | **Compass**—the path and its seams | Do not score local hierarchy or call every extra step a retention problem. |
| Does the relationship earn trust, first value, recognition, return, or advocacy? | **Flywheel**—the stage transition and lifecycle | Do not use it to replace a missing Back affordance, lost route, or screen-level action model. |
| Once the floor holds, what deserves to be remembered? | **Soul**—the authored moment and its frequency | Do not decorate a maze, hide a trust failure, or treat novelty as a retention strategy. |

### The two common overlaps

**Compass vs Flywheel.** Compass asks whether the route is understandable, economical, reversible, and stateful: *Where do I go? What is next? How do I get back?* Flywheel asks whether the effort and uncertainty on that route earn the next relationship stage: *Why should I continue? Is this too much work or exposure before value?* A hidden step, dead end, or lost state is Compass. A coherent but over-demanding setup, premature ask, or effort that delays first value is Flywheel. Use both when both conditions are present; make the path defect the primary owner when it blocks access to the stage.

**Flywheel vs Soul.** Flywheel owns whether value lands, is recognized, compounds, and creates a substantive reason to return. Soul owns where and how a working moment is authored and made memorable. Flywheel Emotion does not require novelty, motion, or recognizability without the logo; it asks whether re-entry restores momentum and repeated use becomes more valuable. If value lands and return is earned but the experience remains anonymous, use Soul. Soul may identify expressive treatment that strengthens a Flywheel win, but it waits behind trust, comprehension, accessibility, and path integrity.

Focal has the same boundary rule: a confusing action surface is Focal; a misleading product promise or missing evidence across the relationship is Flywheel; a broken transition is Compass. Do not let a local symptom acquire the wrong owner just because it appears on a screen.

## The audit workflow

Run the four local methodologies in this order. This is the evidence order, not an automatic fix order.

### When a sibling Skill is not installed

Every pass below loads a sibling spine by relative path. Those paths resolve when the four foundational Skills sit beside this one—the plugin, marketplace, and `install.sh` layouts all produce that—but not for a single-Skill upload, a lone `bundles/product-judgement.md`, or a partial `skills add`. Check before auditing, and never simulate a methodology you could not read: an invented Focal score is worse than a missing one, because the reader cannot tell the two apart.

A single-file bundle is the exception that looks like this case but is not. `bundles/all.md` concatenates all five spines and their review contracts into one file, so the content is already in context even though `../focal/SKILL.md` resolves to nothing. Use the in-context sections and run the full audit. Report a scale unavailable only when its methodology is neither readable at its path nor present in context.

When a spine or review contract is genuinely unavailable:

1. Name the unavailable scale and the reason in **Coverage**.
2. Run the passes whose Skills are present, in the same order.
3. Score the missing scale `N/E—Skill not installed` in the scorecard and leave its cross-scale finding empty. Keep the row: the gap is part of the result.
4. Say what closes it—`claude plugin install product-judgement@product-judgement`, or `./scripts/install.sh`, installs all five.
5. Keep the reconciliation and the priority sequence, and mark the ordering provisional. An unread scale can hide the real upstream owner.

With fewer than two scales available, stop and say so. Reconciliation is this Skill's whole function, and there is nothing to reconcile.

### 1. Frame the audit and map coverage

Establish the product, audience, stakes, first value, business goal, and evidence basis. Build a compact map with four views:

- **Screens**—entry, first decision, first value, repeat use, re-entry, high-stakes actions, and failure or recovery states.
- **Journeys**—the primary entry-to-outcome flows, branches, deep links, Back behavior, interruption, and resume behavior.
- **Relationship**—arrival, trust, activation before value, first value, return, lapse, re-engagement, and advocacy.
- **Memory**—the default happy path, its beats, frequency, ending, and any moments already carrying expressive treatment.

Use the same four-part implementation locator throughout: **Screen · Flow · State · Lifecycle**. Keep rendered state separate from occurrence. For example, `Import screen · CSV upload flow · validation error · first-run activation` is precise; `onboarding` is not. If one field is not evidenced, write `not shown` and name the check that would expose it.

### 2. Run Focal on the decision surfaces

Load [Focal](../focal/SKILL.md) and its [review contract](../focal/reference/review.md). Review the screens that carry the primary decisions or expose the largest relationship stages. Include representative variants rather than pretending one screenshot proves every state. Preserve Focal's native `/12` score and **One Screen, One Clear Intent** verdict.

Record which screen issue is local and which one is actually a path, lifecycle, or memory issue for the later reconciliation.

### 3. Run Compass on the primary journeys

Load [Compass](../compass/SKILL.md) and its [review contract](../compass/reference/review.md). Review the primary journeys as ordered paths, including the seams where state, context, or entry points can fail. Preserve Compass's native `/12` score and **Never Lost** verdict.

Do not use Compass to rescore every screen. Use Focal for local structure and Compass for the route between those surfaces.

### 4. Run Flywheel across the relationship

Load [Flywheel](../flywheel/SKILL.md) and its [review contract](../flywheel/reference/review.md). Name first value before diagnosing. Evaluate all four plays—Trust, Friction, Wins, and Emotion—then identify the earliest evidenced leaking stage, not merely the largest downstream symptom. Preserve Flywheel's native `/16` only when all four plays are supportable; if a relationship stage is entirely unexposed, preserve `N/E—insufficient evidence`, omit the total, and make the ordering provisional.

Use the Compass map as evidence for the route, but keep the question separate: Compass explains whether the user can traverse the path; Flywheel explains whether the path earns the next relationship stage.

### 5. Run Soul after checking the floor

Load [Soul](../soul/SKILL.md) and its [review contract](../soul/reference/review.md). Run its unscored Readiness check, sweep the default happy path, assign frequency and state to each beat, and preserve the authored-state verdict. Preserve Soul's native `/12` only when all three gates are evaluable. Deferred Readiness is not by itself `N/E`: score the treatment the artifact actually shows, and use `N/E` only for a gate the structural failure genuinely prevents evaluating. Omit the total whenever any gate is `N/E`; never invent one.

If Focal, Compass, or Flywheel finds a broken floor, still record the Soul findings, but sequence expressive treatment after the structural or lifecycle repair. Do not use delight to cover confusion, a maze, a trust break, or invisible value.

### 6. Reconcile without flattening the Skills

Create one issue ledger from the four native reports:

1. Deduplicate findings that describe the same condition.
2. Assign one primary owner using the boundary rules above.
3. Keep the exact **Screen · Flow · State · Lifecycle** locator on every finding, recommendation, handoff, and priority change.
4. Record dependencies, such as `Soul after Compass` or `Flywheel after Focal`.
5. Preserve every local score, verdict, and component score rationale; do not average unlike totals into a false Product Judgement score.
6. Separate observed, inferred, walked, tested, and measured claims.

Order the ledger by severity, P0 first. Within one severity, order by owner in the run order above—Focal, then Compass, then Flywheel, then Soul—and then by that Skill's own tie-break. One condition may legitimately affect several local scores, but it still prints once in the cross-scale ledger. Secondary score rationales cite the shared condition and its primary owner instead of creating duplicate issues or duplicate fixes. For example, state loss can lower Compass Continuity and Flywheel Emotion when it damages return; Compass owns the defect, Flywheel records the relationship consequence, and the priority list contains one state-preservation change.

Set the priority changes by dependency and consequence. Rank concrete implementation changes, not just findings or Skill owners:

1. Stop material harm, coercion, hidden cost, permission, or safety failures.
2. Repair the earliest blocker on the route to first value—often trust or path integrity.
3. Fix screen-local decision surfaces that keep the user from acting or understanding.
4. Make delivered value visible and earn the next relationship stage.
5. Spend Soul's expressive budget only after the path, value, and trust floor holds.

This order can change when evidence shows a different upstream dependency. Do not force every product through the same backlog.

## Holistic output

Run all four local audits first, then return this wrapper. Keep the local reports available in working notes; print their full locked templates only when the user asks for the detailed passes.

The local contracts produce more than this wrapper prints, so five rules settle the surplus. **Several screens, one Focal row**—score the worst screen, name it in the Score rationale, and raise the others as separate cross-scale findings; never average screens. **Bands live in the rationale**—put each local quality band and its weakest-dimension ceiling at the end of that Skill's **Score rationale** bullet, since the scorecard has no band column. **One Blocker**—take the highest-consequence local blocker, name its owner, and record the rest as findings at their own severity. **Four slots, not six**—the local contracts mandate up to three Top moves each plus Flywheel's Fix this first and Soul's ranked moments; select for this wrapper by dependency and consequence, and say in **Handoffs** which owner's moves did not make the cut. **This wrapper supersedes local output instructions**—the local Voice sections, calibration reads of `reference/examples.md`, re-run advice, build-workflow trailers, and sibling handoffs do not apply to an orchestrated pass; their analysis still informs the scores. The **Score rationale** section is required: never report a native total such as `Focal 7/12` without its component rationales. Each component must use the local chain **evidence → consequence → rubric anchor → next-point change**, citing the same four-part locator. The **Priority changes** section is also required: each item must name the owner, **Screen, Flow, State, and Lifecycle**, concrete change, reason for its rank, and dependency.

```markdown
**Verdict:** <coherent | needs structural work | needs lifecycle work | needs authorship> · <one biggest cross-scale issue>

**Product:** <what it is, for whom> · goal: <business or user outcome> · first value: <event, or "undefined"> · stakes: <low | medium | high>
**Screen:** <exact screens, regions, or touchpoints reviewed>
**Flow:** <named journeys and transitions reviewed>
**State:** <exact rendered or system states reviewed>
**Lifecycle:** <exact user/product relationship moments reviewed>
**Coverage:** <screens, journeys, relationship stages, states, and lifecycle moments reviewed> · gaps: <material gaps, or "none">
**Basis:** <observed from a screenshot or artifact | inferred from code | tested in a prototype or live product | walked from a description | measured from product data> · confirm with: <fastest validating check>
**Blocker:** <None. | concise blocker reason>

## Four-scale scorecard
| Skill | Native verdict | Score | Cross-scale finding |
|---|---|---:|---|
| Focal | <Clear Intent verdict | N/E—Skill not installed> | <_/12 · _._/4 | N/E> | <one line> |
| Compass | <Never Lost verdict | N/E—Skill not installed> | <_/12 · _._/4 | N/E> | <one line> |
| Flywheel | <earliest evidenced leak | undetermined pending evidence | N/E—Skill not installed> | <_/16 · _._/4 | N/E> | <one line> |
| Soul | <Readiness + authored-state verdict | N/E—Skill not installed> | <_/12 · _._/4 | N/E> | <one line> |

## Score rationale
- **Focal <_/12>:** Information Architecture _/4 — <evidence → consequence → rubric anchor → next-point change>; Progressive Disclosure _/4 — <evidence → consequence → rubric anchor → next-point change>; Visual Hierarchy _/4 — <evidence → consequence → rubric anchor → next-point change>.
- **Compass <_/12>:** Orientation _/4 — <evidence → consequence → rubric anchor → next-point change>; Path Economy _/4 — <evidence → consequence → rubric anchor → next-point change>; Continuity _/4 — <evidence → consequence → rubric anchor → next-point change>.
- **Flywheel <_/16 or N/E>:** Trust <_/4 or N/E> — <evidence → consequence → rubric anchor → next-point change, or N/E reason>; Friction <_/4 or N/E> — <evidence → consequence → rubric anchor → next-point change, or N/E reason>; Wins <_/4 or N/E> — <evidence → consequence → rubric anchor → next-point change, or N/E reason>; Emotion <_/4 or N/E> — <evidence → consequence → rubric anchor → next-point change, or N/E reason>.
- **Soul <_/12 or N/E> · Readiness <Ready | Deferred>:** Placement <_/4 or N/E> — <evidence → consequence → rubric anchor → next-point change>; Proportion <_/4 or N/E> — <evidence → consequence → rubric anchor → next-point change>; Signature <_/4 or N/E> — <evidence → consequence → rubric anchor → next-point change>.

## Cross-scale findings
- **[P0–P3 · <Focal | Compass | Flywheel | Soul> · <discipline, play, or beat>]** **At:** screen: <exact screen/region/touchpoint> · flow: <named flow or transition> · state: <exact app state> · lifecycle: <exact lifecycle moment>. <Name>—<observation and cost>. **Fix:** <specific change>. **Depends on:** <owner or "none">.

## Priority changes (up to 4)
1. **Priority 1 · <P0–P3> · Now — <primary owner and stage>** · **At:** screen: <exact screen/region/touchpoint> · flow: <named flow or transition> · state: <exact app state> · lifecycle: <exact lifecycle moment>. **Change:** <the concrete implementation change>. **Why now:** <the consequence and upstream reason>. **Depends on:** <owner or "none">.
2. **Priority 2 · <P0–P3> · Next — <primary owner>** · **At:** screen: <exact screen/region/touchpoint> · flow: <named flow or transition> · state: <exact app state> · lifecycle: <exact lifecycle moment>. **Change:** <the change unlocked by Now>. **Why now:** <the consequence and dependency>. **Depends on:** <owner or "none">.
3. **Priority 3 · <P0–P3> · Then — <primary owner>** · **At:** screen: <exact screen/region/touchpoint> · flow: <named flow or transition> · state: <exact app state> · lifecycle: <exact lifecycle moment>. **Change:** <the change that makes value, return, or comprehension stronger>. **Why now:** <the consequence and dependency>. **Depends on:** <owner or "none">.
4. **Priority 4 · <P0–P3> · Later — <primary owner>** · **At:** screen: <exact screen/region/touchpoint> · flow: <named flow or transition> · state: <exact app state> · lifecycle: <exact lifecycle moment>. **Change:** <a fourth warranted change>. **Why now:** <why it belongs after the earlier work>. **Depends on:** <owner or "none">.

## Handoffs and validation
- **Focal:** **At:** screen: <exact screen/region or `not shown`> · flow: <named flow or `not shown`> · state: <exact state or `not shown`> · lifecycle: <exact moment or `not shown`> · <screen(s) to review or rebuild>.
- **Compass:** **At:** screen: <source/destination screen or seam or `not shown`> · flow: <named journey or transition or `not shown`> · state: <exact state or `not shown`> · lifecycle: <exact moment or `not shown`> · <journey or seam to review or rebuild>.
- **Flywheel:** **At:** screen: <exact touchpoint or `not shown`> · flow: <named journey or transition or `not shown`> · state: <exact state or `not shown`> · lifecycle: <exact moment or `not shown`> · <stage and first-value or return check to validate>.
- **Soul:** **At:** screen: <exact beat/touchpoint or `not shown`> · flow: <named happy path or transition or `not shown`> · state: <exact state or `not shown`> · lifecycle: <exact moment or `not shown`> · <moment to author only after its dependency holds>.
- **Validation:** <fastest behavior, user test, or metric for the highest-consequence claim>.
```

Never emit a vague location such as `the onboarding` or `the dashboard` when **Screen, Flow, State, and Lifecycle** can be named. If the evidence cannot support that precision, say `not shown` for the missing field and name what would expose it.

Emit one to four Priority changes, only when each is a concrete warranted change. Do not reserve a slot for Soul or invent filler to reach four. If Soul Readiness is Deferred, record the dependency in Handoffs rather than manufacturing an expressive priority.

## Routing

- **No argument** → explain that this is the whole-app audit and ask for the product, codebase, prototype, or selected frames plus the primary goal.
- **`audit` / `review` / `critique`** → run the full workflow above. Treat `audit` as the default command.
- **A single-screen request** → hand off to `/focal` and do not run the other three unless the user asks for a holistic pass.
- **A single-flow request** → hand off to `/compass`; add `/flywheel` only when the question includes activation, value, return, or a relationship leak.
- **A single moment or expressive-treatment request** → hand off to `/soul`, after checking whether the floor is sound.
- **A build request** → use the relevant local build Skill; Product Judgement is an audit and reconciliation layer, not a replacement for the Screen, Flow, Stage, or Moment Specs.

## Source files

Read the sibling Skill spines and their review contracts when running the local passes:

- [Focal](../focal/SKILL.md) · [review](../focal/reference/review.md)
- [Compass](../compass/SKILL.md) · [review](../compass/reference/review.md)
- [Flywheel](../flywheel/SKILL.md) · [review](../flywheel/reference/review.md)
- [Soul](../soul/SKILL.md) · [review](../soul/reference/review.md)
