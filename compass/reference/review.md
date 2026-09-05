# Compass Review: the three discipline flow audit

Use this reference for a `review` or `audit` of an existing flow, journey, finite task-list service, or navigation. Judge the route and its seams with evidence. Compass can report a supported finding without claiming that an unseen state exists.

## Input contract and modes

Provide the journey's entry points, intended finite outcome or open ended intent and home, audience, stakes, and the screens or routes in order. Include branches and the transitions that matter. When available, include loading, validation and error, retry, permission, Back, refresh, interruption, save and return, re entry, deep link, review, and final submit states. Mark a state or seam as `not shown` when the artifact does not expose it.

Use the mode that matches the evidence:

- **A described flow:** reconstruct only the narrated sequence, name its outcome or anchor, and keep uncertain transitions `not shown`. If the description cannot establish the journey shape, ask before scoring.
- **Screens or screenshots:** read the selected screens in order and judge the transitions they actually show. Screens prove visible structure and selected seams; they do not prove persistence, validation, timing, permission, or lifecycle behavior that is absent.
- **Clickable prototype or live URL:** walk the route, branches, Back, refresh, a relevant deep link, and any save, re entry, error, or submit states that the product exposes. Record what was actually tested.
- **Codebase:** inspect routes, state transitions, validation, persistence, permissions, expiry, revalidation, and re entry before making a claim. Treat code as evidence of behavior only where the path and state are reachable or otherwise verified.
- **Finite task-list service:** model a finite outcome composed of independently completable tasks. Capture the task hub, task names and statuses, user chosen order, task detail → hub returns, Save and return behavior, final review and submit, and any task dependencies or permission gates. Do not force this journey into a linear screen count.

## Step 0: frame and inventory the journey

Walk the actual path before judging it. Count screens only when a count is meaningful; for a task list, count the task level work and hops rather than pretending each user chosen task order is one fixed sequence. Read position cues and retreat labels verbatim. Record what each transition carries, drops, or makes the user re-enter.

Name, in one or two sentences each:

- **The journey:** product, purpose, entry, and finite outcome or open ended home anchor.
- **The user:** first time, returning, interrupted, rushed, one handed, expert, or another evidenced situation; include stakes.
- **The covered states and lifecycle paths:** only conditions walked or shown, such as default, loading, validation, retry, permission, Back, refresh, branch change, task order, save and return, interruption, re entry, deep link, review, or final submit.
- **The bar:** the best in category journey used as a comparator, when one is known.

Build a compact state and transition inventory before scoring. Use one row per evidenced surface or seam and keep the last column as a check when the behavior is not shown:

| Screen or transition | State and lifecycle | What is evidenced | Next evidence check |
|---|---|---|---|
| <source → destination> | <state · lifecycle> | <visible or tested behavior> | <fastest check, or `none`> |

Include only states appropriate to the actual flow. A task list usually needs task status, task detail → hub, order freedom, save and return, and final review → submit; a linear checkout may need payment retry and confirmation instead. Do not turn an exhaustive state checklist into a requirement.

### Evidence and N/E policy

<!-- BEGIN SHARED: evidence -->
Use `N/E—insufficient evidence` when the available artifact cannot support a dimension's rubric. A missing variant does not automatically make the whole dimension unevaluable. Report supported findings and the next evidence check; do not convert unknown behavior into a defect, an implementation recommendation, or a score. If any required dimension is N/E, omit the native total, average, band, and weakest-dimension ceiling.

Before assigning `0`, `1`, or `2`, identify the observed condition that meets the negative rubric anchor. “Not shown,” “untested,” and “unknown” cannot supply that condition. If an essential part of the dimension is unsupported, use N/E rather than a lower score as a substitute for uncertainty. Supported strengths can still be described without a number.
<!-- END SHARED: evidence -->

If a dimension has enough evidence to judge its rubric, score the supported behavior and put the unshown variants in **Coverage** or **Basis**. If the evidence cannot support its rubric, mark only that row N/E and name the behavior needed to evaluate it. Never create an issue, fix, or score from a missing state. For an unseen behavior, the next action is an evidence check, not an implementation recommendation.

Check the evidence needed by each discipline before choosing its integer. A position cue supports an Orientation strength, but not a whole-discipline score when retreat or home is essential and unknown. Named stages establish the advertised journey shape; Path Economy needs the actual actions, hops, and consequential commitments, supplied through a sufficiently concrete description, code, or a walked path. Continuity needs evidence of what crosses a relevant seam. Describe supported strengths without a number when these essentials are absent; do not treat an unshown problem as proof that the path is lean or safe.

## Locate every finding

Every issue, Top move, Next item, and handoff carries the same four part locator:

1. **Screen**: exact source, destination, entry point, or transition seam.
2. **Flow**: named journey and transition.
3. **State**: exact interaction or system condition.
4. **Lifecycle**: exact journey moment, such as first run, returning completion, interruption and re entry, recovery, or final submit.

Use the narrowest defensible locator supported by the evidence. If one field is not evidenced, write `not shown` and name the fastest validating check in **Coverage** or **Basis**. Do not fill an unknown locator with a guessed behavior. The rule is simple: do not invent behavior.

## Adjust for journey type

Classify with the decision tree in [SKILL.md](../SKILL.md), taking its first match. The journey type changes what counts as progress and recovery:

- **Linear:** one path to one outcome. Make the outcome and remaining work legible with a cue that fits the journey; a counter is optional. Back and exit should preserve safe state.
- **Branching:** a choice sends the user down a distinct sequence. Name the branch, show how to change it, and prune dead branches. Do not require one global progress count when the path differs.
- **Task-list:** a finite service has a task hub, independently completable tasks in user chosen order, returns to the hub, and one final review or submit outcome. Task statuses and the completion condition can orient the user; a linear step counter is not required. Judge Save and return, expiry, permission, stale-data revalidation, and recoverable re entry only when the service needs or exposes them.
- **Hub-and-spoke:** a center → detail → center loop. The hub is home and the return route must be explicit; a progress counter is not required when there is no endpoint beyond the loop.
- **Open ended:** browse, search, or explore without a fixed completion event. Judge position and home; do not penalize the absence of a progress indicator or invent a finish line.

An optional step that rejoins the same path remains linear. A drill down inside a longer journey remains part of that journey. A task list is distinct from an unbounded hub because its task set and final outcome are finite.

## Gate 1: Orientation (load bearing)

*At every evidenced step, can the user answer where am I, what remains when bounded, and how do I retreat, get home, or leave?*

- Run the drop test on each evidenced screen and seam, applying only the questions that fit its journey type.
- Check that the outcome and remaining work are legible through an appropriate cue: named stages, task statuses, a checklist, a stable count when meaningful, or location and home. A named three stage stepper can be valid without a numeric counter.
- Check branch identity, the task hub and return route, or the home anchor as applicable. Browser Back can be sufficient when history is expected, discoverable, and state safe.
- Check a platform appropriate retreat and an escape from every owned bounded flow, modal, success, and error state that is shown. Do not demand duplicate controls that add no clarity.
- Hunt for dead ends. A screen the user can reach but not leave is a bug, not an assumed state.

| Score | Criteria |
|-------|----------|
| 0 | No recovery exists—a true dead end, or a flow the user cannot leave from any screen |
| 1 | A way out exists but is hidden or unlabeled; or progress is hidden and the drop test fails on a key screen. Browser Back alone is a failure only when the product owns a bounded flow, history is unsafe or surprising, or the retreat is absent from the screen's default state, reachable only by hover or gesture. A retreat that *wipes work* is Gate 3's, not this gate's |
| 2 | Orientable, but one applicable answer—where-am-I, what-remains-when-bounded, or how-to-retreat/get-home—is weak or absent at a step |
| 3 | Clear position, platform-appropriate retreat/home, and exit throughout; minor signposting gaps |
| 4 | At every step the user knows where they are, what remains when bounded, and how to proceed, retreat, get home, or escape—the journey-appropriate drop test passes everywhere |

A failed drop test is not automatically release-critical: assign severity from consequence, reach, and recoverability, and reserve blocker status for a key state where the user cannot orient, proceed, retreat, or recover.

## Gate 2: Path Economy

*For this journey type, is this the least needless effort without cutting protection?*

- Count the honest work. For a task list, include task completion and the hops through the hub, but respect user chosen order and do not invent one canonical route.
- Merge redundant screens and round trips where the result remains comprehensible. Defer screen density questions to Focal.
- Infer or default only safe, useful values. The inferred value and its source or meaning must be visible and correctable; provide a manual route when confidence is low.
- Confirm financial, identity, permission, legal, security, destination, quantity, destructive, or otherwise consequential values before commitment.
- Keep protective work. Hiding cost, risk, permission, consequence, or a required confirmation is a dark pattern, not economy.

| Score | Criteria |
|-------|----------|
| 0 | The path cannot be completed as designed—branches that dead-end, or a required step the user cannot satisfy |
| 1 | Completable but badly bloated (roughly double the honest step count), a setup wall before first value, or a "shortcut" that hides cost or skips protection |
| 2 | Some waste—one or two redundant steps, or a round-trip that should be one screen |
| 3 | Lean, purposeful path with protection intact; only minor opportunities, if any, remain |
| 4 | The fewest honest steps; every screen earns its place; nothing protective was cut |

## Gate 3: Continuity

*Do context and state survive the seams between screens?*

- Check for a memory bridge. Within the same process, previously entered information that is required again should be visible or available to select, subject to essential, security, and invalid-data exceptions. See [W3C's Redundant Entry guidance](https://www.w3.org/WAI/WCAG22/Understanding/redundant-entry.html); it does not require storage between sessions.
- Test state on Back and refresh where those transitions are exposed. Back is a retreat, not a reset, when retaining that state is safe.
- Treat cross session save and return as conditional. Evaluate whether the service safely and permissibly stores the data, tells the user what is retained and when it expires, applies the authentication and authorization appropriate to the data and service at re entry, revalidates stale or consequential data, handles revoked access or conflicts, and offers a recoverable re entry path. Do not make “return tomorrow resumes everything” a universal requirement.
- Test deep links, notifications, and search results where shown. They should land in context rather than at an unrelated start screen.
- Check whether consecutive screens keep the same object, anchors, and mental model.

| Score | Criteria |
|-------|----------|
| 0 | The seams break the task through avoidable context or state loss, broken entry points, or unrecoverable re-entry |
| 1 | A memory bridge on a key step, or a "resume" that resets |
| 2 | Mostly continuous, but one transition drops context or state |
| 3 | Context and permitted state carry dependably across the evidenced seams; only minor roughness, if any, remains |
| 4 | Context and permitted state carry dependably across relevant seams and entry points; expiry, security-driven reset, and recovery remain understandable and effective |

## Scoring rules

Every discipline uses these shared integer anchors:

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

Score each evaluable discipline holistically against its local rubric. Do not use hidden sub scores, checklist subtraction, averaging, or half points; let one severe material failure determine the score when the rubric warrants it. A score row must show **evidence → consequence → rubric anchor → next-point change**. A `2` says what works and names the material weakness; a `3` names a supported remaining gap or says `None justified by the evidence` rather than inventing a change to earn `4`; a `4` explains why the discipline is exemplary and says `None—already exemplary` in the next point field. When more than one independent failure sits in a discipline, score the *worst* one, then list the others as separate issues.

For an N/E row, explain why the available evidence cannot support that rubric and name the fastest evidence check. Do not award credit, invent failure, or propose implementation for unseen behavior. A missing variant can remain in **Coverage** while the supported dimension is scored.

When all three disciplines are integer scores, keep the native total: `total = Orientation + Path Economy + Continuity`; calculate `average = total / 3`, rounded to one decimal place; then apply this band and weakest dimension ceiling:

| Band | Average rule | Native total |
|---|---:|---:|
| **Broken** | `average <= 1.5` | `0–4 / 12` |
| **Significant rework** | `1.5 < average < 2.5` | `5–7 / 12` |
| **Solid** | `2.5 <= average < 3.5` | `8–10 / 12` |
| **Excellent** | `average >= 3.5` | `11–12 / 12` |

Then cap the band by the weakest discipline: a minimum of `0` allows only **Broken**, `1` allows at most **Significant rework**, `2` allows at most **Solid**, and `3–4` adds no ceiling. Use the lower-quality result of the average band and this ceiling. If any required dimension is N/E, report no native total, average, band, or weakest dimension ceiling.

The Never Lost verdict is separate from the total. Use **Yes** only when every applicable, evidenced step passes; use **No** for an observed break; use **N/E** when the outcome or the relevant drop test cannot be judged from the evidence. A true dead end on the core path is a blocker. The rule remains: a blocker does not automatically rewrite a score to 0; a score of 0 does not automatically imply P0. Non-critical methodology failures belong in the local verdict, score, sequencing, or handoff—not in **Blocker**.

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

**Ordering (one rule):** sort by priority, P0 first. Within the same priority, break ties by type of harm—**Orientation** (the user is lost or trapped) outranks **Path Economy** (the path is longer or less honest than it should be) outranks **Continuity** (a seam drops context or state). Never reorder across priorities.

## Output format: use this exact structure

Return this template in order. Keep every section. Emit issues and fixes only for evidenced behavior; for an evidence gap, use Coverage, Basis, or a scorecard N/E reason with the next evidence check. When any discipline is N/E, omit the native total segment from **Verdict** and omit the entire **Total** row from **Scorecard**; do not print an N/E pseudoaggregate. Emit the total, average, band, and weakest-dimension ceiling only when all three disciplines are scored.

```text
**Verdict:** <No | Yes | N/E> · <the single biggest break or evidence gap, one phrase> [append ` · **<total>/12**` only when all three disciplines are scored]

**Flow:** <name> · type: <linear | branching | hub-and-spoke | task-list | open-ended> · audience: <novice | mixed | expert>
**Outcome / anchor:** <finite destination | open-ended organizing intent + home anchor>
**Screen:** <source and destination screens or exact seam reviewed>
**State:** <states and transitions actually reviewed>
**Lifecycle:** <exact journey moment(s) reviewed>
**Context:** <the user's state in a few words> · bar: <relevant supplied convention or comparator, or not provided>
**Coverage:** <journey states and lifecycle paths actually reviewed> · gaps: <material paths not shown or tested, or "none">
**Basis:** <observed from a screenshot or artifact | inferred from code | tested in a prototype or live product | walked from a description | measured from product data> · confirm with: <the fastest validating check>
**Blocker:** <None. | concise blocker reason>

## Scorecard
| Discipline | Score | Why this score | What raises it one point |
|---|---:|---|---|
| Orientation | <_/4 or N/E—insufficient evidence> | <evidence → consequence → rubric anchor, or N/E reason> | <smallest concrete change, `None—already exemplary`, or next evidence check; no implementation for unseen behavior> |
| Path Economy | <_/4 or N/E—insufficient evidence> | <evidence → consequence → rubric anchor, or N/E reason> | <smallest concrete change, `None—already exemplary`, or next evidence check; no implementation for unseen behavior> |
| Continuity | <_/4 or N/E—insufficient evidence> | <evidence → consequence → rubric anchor, or N/E reason> | <smallest concrete change, `None—already exemplary`, or next evidence check; no implementation for unseen behavior> |
| **Total** | **<_/12 · _._/4>** | **<band; exact sum of justified component scores>** | <weakest-dimension ceiling> |

## Issues (most severe first)
- **[P0 · Orientation]** **At:** screen: <source/destination screen or seam> · flow: <named flow and transition> · state: <exact state> · lifecycle: <exact journey moment>. <Name>—<observation>. <impact>. **Fix:** <specific change supported by the evidence>.
- **[P1 · Path Economy]** **At:** screen: <source/destination screen or seam> · flow: <named flow and transition> · state: <exact state> · lifecycle: <exact journey moment>. <Name>—<observation>. <impact>. **Fix:** <specific change supported by the evidence>.

## Top moves (up to 3)
1. **At:** screen: <source/destination screen or seam> · flow: <named flow and transition> · state: <exact state> · lifecycle: <exact journey moment> · <highest-leverage evidenced change>
2. **At:** screen: <source/destination screen or seam> · flow: <named flow and transition> · state: <exact state> · lifecycle: <exact journey moment> · <next evidenced change>
3. **At:** screen: <source/destination screen or seam> · flow: <named flow and transition> · state: <exact state> · lifecycle: <exact journey moment> · <next evidenced change>

## Next
- **Structural** (do first): **At:** screen: <source/destination screen or seam or `not shown`> · flow: <named flow or `not shown`> · state: <exact state or `not shown`> · lifecycle: <exact journey moment or `not shown`> · <evidenced structural change, or the next evidence check when unseen>
- **Executional** (after): **At:** screen: <source/destination screen or seam or `not shown`> · flow: <named flow or `not shown`> · state: <exact state or `not shown`> · lifecycle: <exact journey moment or `not shown`> · <evidenced presentation change, or the next evidence check when unseen>
- **Hand off**: **At:** screen: <source/destination screen or seam or `not shown`> · flow: <named flow or `not shown`> · state: <exact state or `not shown`> · lifecycle: <exact journey moment or `not shown`> · <single-screen hierarchy → Focal; relationship leak → Flywheel; expressive treatment → Soul; `None` if all of it is Compass's>
```

Use `None.` under **Issues**, **Top moves**, or a **Next** item when no evidenced item is warranted; do not add filler. For a single-screen hierarchy problem, route it to [Focal](https://github.com/kvncnls/product-judgement/blob/main/focal/reference/review.md). Re-run after an evidenced fix when the user requests a follow-up audit.
