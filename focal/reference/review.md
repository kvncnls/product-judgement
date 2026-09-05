# Focal Review—the three-discipline audit

Evaluate a screen against the three disciplines and the overarching methodology, then return a scorecard with prioritized, concrete fixes. Use when the user asks to review, critique, audit, or "what's wrong with" any functional product, app, or tool screen.

## Input modes

- **Screenshot / image**—read it, critique what you see. The common mode for design review.
- **File path (JSX/TSX/HTML/Vue/Svelte)**—read it, mentally render the layout, critique structure and prescribed styles. You can't see pixels, so qualify visual claims.
- **Live URL**—if browser automation is available, open the page; otherwise fetch markup. If the request names several screens, return one complete scorecard per screen, and say plainly that the path between them is Compass's.
- **A description**—walk the stated screen and its states, label findings as walked from a description, and name the fastest interaction or artifact check that would confirm the consequential claims.

## Step 0—Notice, frame, and name the intent

Before judging, *notice*. Most people glance; a reviewer sees. Count the elements. Name the colors. Identify the type sizes. Read the labels verbatim. The specificity of your observation is the ceiling on the quality of your critique.

Then frame, in one or two sentences each:
- **What is this?** App type, screen purpose, target user.
- **What's the user's state?** Anxious, rushed, casual, distracted, one-handed? A checkout under time pressure demands different care than a Sunday-morning feed scroll. Name it; the critique must respect it.
- **Which app state and lifecycle moment is this?** Name the rendered state—default/full, loading, empty, partial data or failure, error, success, expanded, permission-denied, interruption, or recovery—and when it occurs—first run, setup, recurring use, re-entry, or post-action. If the artifact shows several variants, inventory them. If it does not, mark material states `not shown` rather than assuming them.
- **What's the bar?** Every product category has an invisible standard set by its best-in-class tool. A notes screen is judged against Apple Notes and Bear; a dashboard against Linear, Stripe, and Vercel; a checkout against Stripe and Shop Pay. Ask: *what would the best-in-class product in this category do here?*
- **The register.** Classify it by walking the decision tree in **Scope and register** in [SKILL.md](../SKILL.md)—take the first match, and don't re-derive the categories here. This sets how the gates should be read; see *Adjust for register* below.
- **The methodology lens.** State the screen's apparent **organizing intent** in one sentence, then name its apparent **action model**: one primary action, an inherent co-equal set, ranked routes, or content-led exploration. On a task screen, an "and" fails only when it joins independently completable outcomes; multiple primary-weight actions fail only when they compete rather than form an inherent binary or dual-mode set. For a hub, the intent is *routing*; for exploration, *browsing one coherent content space*.

## Locate every finding

Before scoring or suggesting a change, build a four-part implementation locator. Every issue, Top move, Next item, and handoff must carry the same locator:

1. **Screen**—the exact screen, region, or control.
2. **Flow**—the named journey or transition that reaches it, or `screen-local` when no cross-screen path is involved.
3. **State**—the rendered UI or system condition, not the user's emotion.
4. **Lifecycle**—the moment in use or relationship: first run, setup, recurring use, re-entry, post-action, or another specific moment.

Use the narrowest defensible locator. `Contact detail · screen-local · empty state · first visit after contact creation` is actionable; `CRM screen` is not. If any locator field is not evidenced, write `not shown` and name the fastest validating check in **Coverage** or **Basis**—do not invent behavior.

## Adjust for register

Read the gates through the register you classified in Step 0. The disciplines still apply; their targets move. Scoring a hub or feed by task-screen rules produces false failures.

- **Task**: score exactly as the gates describe.
- **Hub**: the organizing intent is *routing*. Do **not** penalize many destinations under Gate 1 or Gate 2. Apply the chunk diagnostic *per group and per row*, not to the total destination count. Score IA on whether destinations form a coherent, grouped space, and VH on whether the likely next route or leading group is easy to find. A hub flattened to one action scores *worse*, not better.
- **Exploration**: abundance is the point. Do **not** penalize many items under Gate 1 or Gate 2. Apply the chunk diagnostic *per item*—to the facts or decisions inside a row or card, not to item count. Score VH on whether one coherent content field dominates and chrome recedes; a single primary action is not expected.
- **Task-overloaded**: score by task rules and flag the overload as the leading Gate 1 issue.
- **Audience:** weigh expertise. The working-memory budget is ~4 *chunks*, and experts read dense displays as a few learned groups. Don't score a pro tool's dense panel as overload if its users chunk it; do score a novice or first-run screen strictly. Density is a function of who's reading it.

**A region can carry its own register.** A data table or log inside a task screen is an exploration *region*: score the screen by its own register, and apply a local contextual-density diagnostic within that region rather than counting its rows against the screen's decision point. Say which region you scored separately. A row or card with many unfamiliar facts may still be clear when facts are grouped, ranked, familiar, or needed together; it may overload when those conditions do not hold. There is no fixed row/card count that fails Gate 2. Judge the local density from expertise, stakes, device, content length, hierarchy, and whether each fact changes the current decision.

## The three gates

Run each gate in turn, in the order the disciplines apply. Each produces a 0–4 score when its rubric is supported, with the specific findings behind it; use `N/E—insufficient evidence` when the artifact cannot support that dimension.

### Gate 1—Information Architecture

*What belongs on this screen, and how is it organized?*

- Apply the **one-sentence test** to the actual content: write *"This screen exists so the user can ___."* If "and" joins independently completable outcomes, IA has put competing intents on one screen. A phrase such as *review and approve this invoice* can remain one coherent intent when the first action is necessary to the second.
- Identify the **action model** and test it against the register. On a task screen, multiple primary-weight actions usually signal competing intents unless they form an inherent binary or dual-mode set. On a hub, ranked routes are expected; in exploration, the content field leads.
- Check **grouping and labeling**: are related things together? Are labels in the user's words or in system jargon?
- Check whether the screen **infers recognizable input before asking for classification**. Does it show the interpretation, allow correction, and retain a fallback when ambiguity remains?
- Check whether **decision-critical context stays at the decision surface**: history, status, price, and consequence should not require a context jump or memory bridge.
- Check for the **memory bridge**: does any decision require a fact only shown on an earlier screen?
- Check for **orphan content** and **data-model-shaped structure** (organized for the database, not the user's intent).

| Score | Criteria |
|-------|----------|
| 0 | No discernible organizing intent—a dumping ground of unrelated content |
| 1 | Multiple competing intents; structure mirrors the data model; jargon labels |
| 2 | One intent is identifiable but an independent outcome muddies it; weak grouping or a memory bridge |
| 3 | Clear organizing intent, suitable action model, sensible grouping and labels; only minor structural noise, if any, remains |
| 4 | Exemplary organization makes a demonstrably difficult set of related decisions unusually easy to navigate; explain the specific structural choice and its benefit beyond ordinary clear intent, grouping, and labels |

### Gate 2—Progressive Disclosure *(anti-overload)*

*Of what belongs, is the right amount shown now?*

- At the busiest decision point, **count independent chunks in working memory** as a diagnostic starting point. About four unfamiliar chunks can be a useful task-screen probe, but it is not a universal pass/fail line, and no row or card count is one either. Judge familiarity, stakes, grouping, device, content length, and whether each item changes the decision before calling the screen overloaded.
- Check whether the screen **minimizes decisions without withholding evidence**. Technical detail can remain available for trust, verification, or expert use without making every user interpret it before proceeding.
- Check the **disclosure triage**: is anything shown that should be deferred (rare options, advanced settings)? Is anything deferred that should be shown *now* (price, required fields, consequences, the task's primary action, or a control required by the register's action model)?
- Check that deferral signals **what's hidden** (a count, a clear "More") rather than reading as absence. Name the cue for each deferred thing; if you cannot find one, the content is hidden rather than deferred. A function reachable only by an uncued gesture is the worst case.

| Score | Criteria |
|-------|----------|
| 0 | Fundamentally broken—severe overload blocks the core task, or essential information is concealed in a way that removes informed choice or creates material harm |
| 1 | Major failure—a wall of options or a dark-pattern reveal hides price, a required field, or a consequence, but the core task remains technically possible |
| 2 | Some layering, but a key decision point creates material cognitive overload for its audience; or content is deferred behind no perceptible cue |
| 3 | Appropriate layering for the audience and stakes; decision-critical facts stay available and deferred content has a clear cue; only minor gaps, if any, remain |
| 4 | An unusually effective disclosure strategy resolves a demonstrated complexity or competing information need without withholding essential evidence; explain what exceeds ordinary appropriate layering |

A **buried essential** is a blocker only when it prevents the core outcome, removes informed choice, or hides material cost, consequence, permission, or risk. Otherwise assign severity from consequence, reach, and recoverability. Do not infer blocker status from the Progressive Disclosure score alone or force the dimension to `0` unless its rubric supports `0`.

### Gate 3—Visual Hierarchy

*Does weight match importance?*

Before scoring this gate, establish rendered layout or concrete style/order evidence that supports the weight ranking and control signifiers. A description that merely names a “primary action” and a details affordance establishes their intended roles, not their visual prominence. Without evidence of presentation, use `N/E—insufficient evidence` for Visual Hierarchy, describe the supported action model under IA, and omit the aggregate total. A sufficiently concrete description of layout and styles can support a score; a screenshot is not the only valid evidence source.

- Run the **squint test** on the screenshot (or describe the weight order from the code). Name #1, #2, and the groupings.
- Run the **quick-orientation probe**: on a task screen, can a first-timer identify the read-first region or next action within the first few seconds? Three seconds can be a useful test prompt, but it is not a stopwatch threshold or an automatic scoring failure. For hubs and exploration surfaces, look for a leading group or content field rather than one CTA.
- Check **weight vs. importance**: does anything decorative outweigh the action model's dominant element or region? Is there a clear visual entry point (the focusing mechanism)? Count distinct type sizes/weights—deliberate scale, or noise?
- Check whether the **consequence is visible** when a decision depends on a relationship, tradeoff, or process state. A summary, comparison, preview, or visualization should clarify raw values without replacing the supporting evidence.
- Check **rank vs. actionability** separately. Ranking first is not the same as reading as actionable: when the dominant element is an action, name what says it can be acted on. Then count **false signifiers** (patterns.md, The false signifier).

| Score | Criteria |
|-------|----------|
| 0 | Flat—everything equal weight, no ranking survives a squint |
| 1 | Weak or inverted hierarchy; decoration beats function; no entry point; false signifiers competing with real controls |
| 2 | Hierarchy present but muddy; some elements miscalibrated; or a dominant action ranks first but carries nothing that reads as actionable |
| 3 | Clear hierarchy, weight mostly matches importance |
| 4 | Effortless ranking; the dominant element or region is the right one for the action model |

## Scoring rules

Every discipline uses the same integer anchors:

<!-- BEGIN SHARED: anchors -->
| Score | Canonical label | Shared meaning |
|---:|---|---|
| **0** | **Broken or harmful** | The dimension fails outright, blocks its core outcome, actively inverts the intended behavior, or creates material harm. |
| **1** | **Major failure** | The outcome may remain technically possible, but the dimension is seriously compromised, unreliable, or largely absent. Substantial correction is required. |
| **2** | **Partial or inconsistent** | The basic function exists, with a material weakness, missing decision, or inconsistency that prevents dependable quality. |
| **3** | **Strong** | Deliberate, dependable, context-appropriate professional work with only minor gaps. This is the normal target for good execution. |
| **4** | **Exemplary—above and beyond** | Fully realized and unusually effective for the relevant context, including realistic states and constraints. This is intentionally uncommon, not the normal target. |

Meeting the ordinary requirements of the task supports `3`, not automatically `4`. A `4` rationale must identify a specific unusually effective quality visible in the evidence, beyond listing correct ingredients or repeating the rubric. It need not be novel or backed by analytics, but “no defect was shown” is not enough.
<!-- END SHARED: anchors -->

Score each discipline holistically against its local rubric. Read all checks and evidence, choose the anchor that best describes the dimension overall, apply explicit local caps or prerequisites, and let one severe material failure determine the score when the rubric warrants it. Do not use hidden sub-scores, checklist subtraction, averaging, or half-points. A 4 is exemplary for the dimension being scored; it does not universally require novelty. If the available artifact cannot support a dimension's rubric, mark that dimension `N/E—insufficient evidence` rather than treating the gap as zero.

### Score rationale—required

A score without an explanation is invalid. Fill every scored row with the same chain: **evidence → consequence → rubric anchor → next-point change**. State what was observed, inferred, tested, walked, or measured; what it costs the user; why that evidence earns the integer under the local rubric and stops there; and the smallest concrete change that would raise it one point. A `2` must say what works and name the material weakness; a `3` names a supported remaining gap or says `None justified by the evidence` rather than inventing a change to earn `4`; a `4` must explain why the discipline is exemplary and say `None—already exemplary` in the next-point field. A dimension with no evidence for its rubric is `N/E—insufficient evidence`; replace the next-point change with the fastest evidence check. A missing variant alone does not make the whole dimension N/E: score the supported behavior and record the gap in Coverage/Basis.

When all three dimensions are scored, keep the native total: `total = Information Architecture + Progressive Disclosure + Visual Hierarchy`. Calculate `average = total / 3`, display it rounded to one decimal place, and apply this shared algorithm:

| Band | Average rule | Native total |
|---|---:|---:|
| **Broken** | `average <= 1.5` | `0–4 / 12` |
| **Significant rework** | `1.5 < average < 2.5` | `5–7 / 12` |
| **Solid** | `2.5 <= average < 3.5` | `8–10 / 12` |
| **Excellent** | `average >= 3.5` | `11–12 / 12` |

Then cap the band by the weakest discipline: a minimum of `0` allows only **Broken**, `1` allows at most **Significant rework**, `2` allows at most **Solid**, and `3–4` adds no ceiling. Use the lower-quality result of the average band and this ceiling. The total must equal the exact sum of the three scores. If any required dimension is N/E, omit the native total, average, band, and weakest-dimension ceiling; report the supported rows and the evidence gap instead.

- If more than one independent failure sits in a discipline, score the *worst* one, then list the others as separate issues.

<!-- BEGIN SHARED: evidence -->
Use `N/E—insufficient evidence` when the available artifact cannot support a dimension's rubric. A missing variant does not automatically make the whole dimension unevaluable. Report supported findings and the next evidence check; do not convert unknown behavior into a defect, an implementation recommendation, or a score. If any required dimension is N/E, omit the native total, average, band, and weakest-dimension ceiling.

Before assigning `0`, `1`, or `2`, identify the observed condition that meets the negative rubric anchor. “Not shown,” “untested,” and “unknown” cannot supply that condition. If an essential part of the dimension is unsupported, use N/E rather than a lower score as a substitute for uncertainty. Supported strengths can still be described without a number.
<!-- END SHARED: evidence -->

Dimension score, overall quality band, issue severity, critical blocker, and the **One Screen, One Clear Intent** verdict are separate. The verdict is Yes or No when the organizing intent is evidenced; use `N/E—insufficient evidence` when the artifact cannot support that verdict, with the fastest intent check. A screen can be Solid and still receive No if its organizing intent or action model is structurally unresolved. Every P0 is a blocker, but a blocker does not automatically rewrite a score to 0; a score of 0 does not automatically imply P0. Non-critical methodology failures belong in the local verdict, score, sequencing, or handoff—not in **Blocker**.

## Issue severity

<!-- BEGIN SHARED: severity -->
| Priority | Meaning |
|----------|---------|
| **P0 — Critical** | Blocks the core outcome; traps the user; destroys work or state; causes or risks material harm; hides material cost, consequence, permission, or risk; removes informed choice; or uses coercive manipulation. Fix before release. |
| **P1 — Major** | Materially damages comprehension, completion, orientation, trust, value realization, or return for a meaningful share of users. Fix before release. |
| **P2 — Moderate** | Creates real friction, confusion, dilution, or missed value with a viable recovery, workaround, or limited scope. Fix in the next planned pass. |
| **P3 — Minor** | Low-impact craft, consistency, or polish. Fix when time permits. |

Assign severity from consequence, reach, and recoverability. A methodology rule violation is not automatically P0.
<!-- END SHARED: severity -->

**Ordering (one rule):** sort by priority, P0 first. Within the same priority, break ties by type of harm—**structural** (IA: wrong job or mental model) outranks **behavioral** (PD: disclosure, overload) outranks **visual** (VH: weight, spacing, type). Never reorder across priorities; a P0 Hierarchy issue outranks a P1 IA issue.

## Output format—use this exact structure

Every review uses this structure, in this order. For a complete scorecard, return the template verbatim. For an incomplete scorecard, keep the same sections and dimension rows, apply the conditional N/E rule above, and omit only the invalid total row and total segment. Fill the `<…>` slots; keep every fixed label. This block is the single source of truth for the emitted shape—the issue line, the table columns, and the section list exist only here.

For an incomplete scorecard, keep the three dimension rows, write `N/E—insufficient evidence` in the unsupported row, and omit the **Total** row and the total segment in **Verdict**. The native total, average, band, and weakest-dimension ceiling are valid only when all required dimensions are scored.

```
**Verdict:** <clear intent—yes | no | N/E—insufficient evidence> · <the one biggest problem, one phrase> · **<total>/12**

**Screen:** <what it is> · register: <task | hub | exploration | task-overloaded> · audience: <novice | mixed | expert>
**Flow:** <named journey or `screen-local`; if not evidenced, `not shown`>
**State:** <exact rendered or system state(s) reviewed>
**Lifecycle:** <exact user/product moment(s) reviewed>
**Context:** <the user's state in a few words> · bar: <the best-in-class comparator you judged against>
**Coverage:** <app states and lifecycle moments actually reviewed> · gaps: <material states not shown or tested, or "none">
**Basis:** <observed from a screenshot or artifact | inferred from code | tested in a prototype or live product | walked from a description | measured from product data> · confirm with: <the fastest validating check>
**Blocker:** <None. | concise blocker reason>

## Scorecard
| Discipline | Score | Why this score | What raises it one point |
|---|---:|---|---|
| Information Architecture | _/4 or N/E—insufficient evidence | <evidence → consequence → rubric anchor, or evidence gap> | <smallest next-point change, or fastest evidence check> |
| Progressive Disclosure | _/4 or N/E—insufficient evidence | <evidence → consequence → rubric anchor, or evidence gap> | <smallest next-point change, or fastest evidence check> |
| Visual Hierarchy | _/4 or N/E—insufficient evidence | <evidence → consequence → rubric anchor, or evidence gap> | <smallest next-point change, or fastest evidence check> |
| **Total** | **_/12 · _._/4** | **<band; exact sum of justified component scores>** | <weakest-discipline ceiling applied> |

## Issues (most severe first)
- **[P0 · IA]** **At:** screen: <exact screen/region> · flow: <named flow or `screen-local`> · state: <exact state> · lifecycle: <exact moment>. <Name>—<observation>. <impact>. **Fix:** <fix>.
- **[P1 · Disclosure]** **At:** screen: <exact screen/region> · flow: <named flow or `screen-local`> · state: <exact state> · lifecycle: <exact moment>. <Name>—<observation>. <impact>. **Fix:** <fix>.

## Top moves (up to 3)
1. **At:** screen: <exact screen/region> · flow: <named flow or `screen-local`> · state: <exact state> · lifecycle: <exact moment> · <highest-leverage change>
2. **At:** screen: <exact screen/region> · flow: <named flow or `screen-local`> · state: <exact state> · lifecycle: <exact moment> · <next>
3. **At:** screen: <exact screen/region> · flow: <named flow or `screen-local`> · state: <exact state> · lifecycle: <exact moment> · <next>

## Next
- **Structural** (do first): **At:** screen: <exact screen/region> · flow: <named flow or `screen-local`> · state: <exact state> · lifecycle: <exact moment> · <what changes what the screen *is*—split or merge, regroup, relabel, re-triage>
- **Executional** (after): **At:** screen: <exact screen/region> · flow: <named flow or `screen-local`> · state: <exact state> · lifecycle: <exact moment> · <what changes how it *looks*—weight, color, type, spacing, motion>
- **Hand off**: **At:** screen: <exact screen/region or `not shown`> · flow: <named flow or `not shown`> · state: <exact state or `not shown`> · lifecycle: <exact moment or `not shown`> · <anything that is not this screen's problem—cross-screen path issues go to Compass; activation, value-recognition, or return leaks go to Flywheel; "None" if all of it is Focal's>
```

Filling it:
- **Coverage**—name only states and lifecycle moments the evidence actually exposes. Use `gaps` for consequential variants such as loading, error, first-run, re-entry, worst-case data, success, partial failure, permission, or recovery that were not shown or tested. If a dimension has no support for its rubric, mark that row `N/E—insufficient evidence`; a missing variant by itself does not make the dimension N/E.
- **Issues and suggestions**—repeat the issue line once per issue, and give every issue, Top move, Next item, and handoff a complete **Screen · Flow · State · Lifecycle** locator. Emit one to three Top moves, only when each names a real change; never invent filler to reach three. If no move is warranted, write `None.` Keep each locator specific enough that a designer or engineer can reproduce the state without rereading the diagnosis. `<observation>` may run two or three sentences when specificity requires it. If behavior is unknown, the next step is an evidence check; do not prescribe an implementation for the unknown condition. If nothing ranks above P3, write "None above P3." under the Issues header and keep the header.
- **Next**—structural before executional, always: polishing a screen with an unresolved organizing intent only organizes the clutter. Resolve structural items with the five-move build workflow in [build.md](build.md). Single-screen work is Focal's; if the real problem is the path between screens, hand off to Compass; if it is a lifecycle leak in activation, value recognition, or return, hand off to Flywheel.
- Re-run the audit after fixes to watch the score climb.
