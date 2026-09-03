# Flywheel Diagnose—the four-play audit

Find where a product loses the people it already earned and name the one stage to fix first. A full relationship diagnosis evaluates all four plays and reports `/16` only when all are supportable; a request explicitly limited to one stage scores that play only and reports no cross-play total. Use when the user asks to diagnose, audit, or review growth, retention, activation, conversion, churn, or a symptom like "nobody comes back."

## Input modes

- **A symptom** ("they sign up and never return")—map it to a stage with the diagnosis tree in [SKILL.md](../SKILL.md), scan all four to catch an earlier leak, then audit the selected stage deepest.
- **A targeted stage** ("audit the upgrade moment")—run that play deeply. Mark the other rows `N/E—outside targeted scope`, and do not print a native total or common band. `N/E` means not evaluated, not zero.
- **Funnel data**—the leak is where the drop-off is. Use cohorts with a shared start point, and read distributions rather than averages.
- **An artifact** (a screenshot, a page, a flow, a product)—diagnose heuristically from the play's own checks. This is the common case and it is legitimate; label it as diagnosed rather than measured. If the artifact and supplied context expose no evidence for a play, use `N/E—insufficient evidence` rather than inventing lifecycle behavior.

## Step 0—Frame, then find the leak

Before scoring, establish in one or two sentences each:

- **What is this product, and who is it for?** A growth judgment with no audience is a guess.
- **What is first value?** Name the event that changes the user's situation. If the team has not defined it, infer the strictest definition supported by the product evidence and label it as the audit's working definition—the tree below cannot be walked without one. Missing internal terminology does not cap a UX score by itself. If no value-changing outcome can be defended from the product or context at all, say so and score the resulting uncertainty where the local rubric supports it.
- **What are the stakes?** Low, medium, or high. In finance, health, children's products, employment, housing, education, identity, and safety, protective friction is a foundation and its removal is a defect, not an optimization.
- **Where is the leak?** Walk the diagnosis tree in **[SKILL.md](../SKILL.md)**—take the first match, and don't re-derive the categories here. If two stages leak, take the earliest; loss compounds downstream.
- **Which relationship and app states are covered?** Inventory the evidence across arrival, consideration, activation before value, first value, return, lapse, re-engagement, and advocacy—and the exact UI states exposed at those moments. Mark consequential stages or states `not shown` rather than filling them in from assumption.
- **Measured or diagnosed?** State which. Findings from data and findings from reading an artifact carry different weight, and blending them silently is how a heuristic becomes a false certainty.

## Locate every finding

Before scoring or suggesting a change, build a four-part implementation locator. Every issue, Fix this first recommendation, Next item, and handoff must carry the same locator:

1. **Screen**—the exact touchpoint, screen, message, or control.
2. **Flow**—the named journey or transition that carries the user to that touchpoint.
3. **State**—the rendered or system condition: first encounter, empty, loading, error, success, ask, retry, and so on.
4. **Lifecycle**—the relationship stage: arrival, consideration, activation before value, first value, return, lapse, re-engagement, or advocacy.

Use the narrowest defensible locator. `Report screen → result · report generation flow · success after processing · first value for a new signup` is actionable; `activation` is not. If any locator field is not evidenced, write `not shown` and name the metric or behavior that would confirm it in **Coverage** or **Basis**—do not invent behavior.

## The four gates

In a full diagnosis, evaluate all four plays even when only one appears to leak—a stage can be strong and still sit behind a broken one, and the reader needs to see that the fix is upstream. Score every play supported by evidence. If a play is entirely unexposed after inspecting the available artifact and context, mark it `N/E—insufficient evidence`; never turn an absent lifecycle stage into either credit or failure. In a targeted stage review, score only the selected play and mark the other three `N/E—outside targeted scope`.

### Gate 1—Trust *(the first push)*

- Can a stranger name who this is for and what changes for them, from the first screen alone?
- Can the user identify the next relationship commitment and its consequence? Local CTA competition is evidence only when it disrupts trust at this stage; Focal owns the screen-level hierarchy and action model.
- For each claim, is the evidence within one scroll of it?
- Do the entry points that carry real traffic preserve the promise that brought the user?
- Is consequence—cost, permission, reversibility—visible before the action that triggers it?

| Score | Criteria |
|-------|----------|
| 0 | Actively repels—misleading claims, hidden cost, or a first encounter that damages trust |
| 1 | Missing—no recognizable audience, outcome, or reason to continue |
| 2 | Functional—the category is clear but the outcome, evidence, or next step is not |
| 3 | Strong—relevant, comprehensible, supported, coherent, and safe |
| 4 | Exemplary—the first encounter establishes relevance, proof, and safe agency with unusual clarity for this context |

### Gate 2—Friction *(drag on the bearing)*

- Is first value identifiable as an outcome rather than setup? If the team has not named it, use the audit's evidence-backed working definition. Cap this gate at `2` only when no value-changing outcome can be defended, not merely because internal documentation is missing.
- Walk the effort before first value and name its friction type. Use Compass to establish route mechanics; Flywheel scores whether that effort and uncertainty prevent the relationship from reaching value. Accidental and cognitive friction are waste; protective and productive friction are not.
- Is any commitment asked before value has been delivered?
- Do empty states create a path to value, and do errors preserve the user's work?

| Score | Criteria |
|-------|----------|
| 0 | Protective friction removed, or a required step the user cannot satisfy |
| 1 | A setup wall—value is gated behind configuration the user has no context to complete |
| 2 | Reachable, but padded with accidental or cognitive friction, or first value is undefined |
| 3 | Lean path, purposeful steps, progress preserved, recovery designed |
| 4 | Exemplary—the fewest honest steps; safe inference and defaults do the work; protection intact and explained |

### Gate 3—Wins *(the power stroke)*

- Name the largest win the product delivers. Does the user recognize it happened?
- Does feedback intensity match the magnitude of the win?
- Does every important workflow have a designed ending, or does it stop?
- Does each ask land after the value it extends? Does declining preserve value already earned, with any foregone benefit explicit and noncoercive?

| Score | Criteria |
|-------|----------|
| 0 | Claimed value is fabricated, or an ask uses hidden material consequence or coercion to extract action |
| 1 | Value is delivered silently, or an interruptive ask materially blocks inspection of the value just earned |
| 2 | Wins are acknowledged generically; endings stop rather than close |
| 3 | The main win is visible and proportionate; asks follow related value and preserve already-earned value when declined |
| 4 | Exemplary—value is made legible and accumulates; endings open the next action; asks read as continuation |

### Gate 4—Emotion *(the mass)*

- Is the intended relationship state named—confidence, control, momentum, mastery, belonging—and is there evidence it supports return or preference?
- Does re-entry restore context, show what changed, and preserve accumulated value?
- Does repeated use become easier or more valuable, giving the user a substantive reason to continue?
- Does anything here rely on shame, urgency, streak pressure, or guilt?

| Score | Criteria |
|-------|----------|
| 0 | Emotion is weaponized—shame, false urgency, punitive streaks, guilt-based retention |
| 1 | No relationship mass—each visit resets context or value, and return depends on prompting rather than a reason |
| 2 | Return is possible, but restored context, accumulated value, or preference is materially weak or inconsistent |
| 3 | Re-entry restores momentum, repeated use preserves or compounds value, and the reason to return is clear |
| 4 | Exemplary—each return is meaningfully easier or more valuable, preference is reinforced without pressure, and evidence supports durable return or advocacy |

## Scoring rules

Every evaluated play uses the same integer anchors:

| Score | Canonical label | Shared meaning |
|---:|---|---|
| **0** | **Broken or harmful** | The dimension fails outright, blocks its core outcome, actively inverts the intended behavior, or creates material harm. |
| **1** | **Major failure** | The outcome may remain technically possible, but the dimension is seriously compromised, unreliable, or largely absent. Substantial correction is required. |
| **2** | **Partial or inconsistent** | The basic function exists, with a material weakness, missing decision, or inconsistency that prevents dependable quality. |
| **3** | **Strong** | Deliberate, dependable, context-appropriate professional work with only minor gaps. This is the normal target for good execution. |
| **4** | **Exemplary—above and beyond** | Fully realized and unusually effective for the relevant context, including realistic states and constraints. This is intentionally uncommon, not the normal target. |

Score each evaluated play holistically against its local rubric. Read all checks and evidence, choose the anchor that best describes the play overall, apply explicit local caps or prerequisites, and let one severe material failure determine the score when the rubric warrants it. Do not use hidden sub-scores, checklist subtraction, averaging, or half-points. A 4 is exemplary for the play being scored; expressive distinctiveness is Soul's concern, not a Flywheel prerequisite.

### Score rationale—required

A score without an explanation is invalid. Fill every scorecard row with the same chain: **evidence → consequence → rubric anchor → next-point change**. State what was observed, inferred, tested, walked, or measured; what it costs the relationship; why that evidence earns the integer under the local rubric and stops there; and the smallest concrete change that would raise it one point. A `2` must say what works and name the material weakness; a `3` must name the remaining gap; a `4` must explain why the play is exemplary and say `None—already exemplary` in the next-point field. If the evidence does not expose a state or lifecycle stage, say `not shown` in Coverage/Basis and name the validating metric or behavior—do not award credit or invent failure.

For a **full diagnosis with all four plays evaluated**, keep the native total: `total = Trust + Friction + Wins + Emotion`. Calculate `average = total / 4`, display it rounded to one decimal place, and apply this shared algorithm. If any play is `N/E—insufficient evidence`, report no `/16` total, average, common band, or weakest-play ceiling. For a **targeted stage review**, report the selected play `/4`, mark the others `N/E—outside targeted scope`, and report `Total: N/E—targeted stage review`; do not calculate an average, common band, or weakest-play ceiling from one play.

| Band | Average rule | Native total |
|---|---:|---:|
| **Broken** | `average <= 1.5` | `0–6 / 16` |
| **Significant rework** | `1.5 < average < 2.5` | `7–9 / 16` |
| **Solid** | `2.5 <= average < 3.5` | `10–13 / 16` |
| **Excellent** | `average >= 3.5` | `14–16 / 16` |

Then cap the band by the weakest play: a minimum of `0` allows only **Broken**, `1` allows at most **Significant rework**, `2` allows at most **Solid**, and `3–4` adds no ceiling. Use the lower-quality result of the average band and this ceiling. The total must equal the exact sum of the four scores.

- If more than one independent failure sits in a play, score the *worst* one, then list the others as separate issues.

- **A dark pattern is a critical blocker regardless of total.** Hiding cost, permission, risk, or reversibility to increase action; weaponizing emotion; or removing informed choice must be tagged P0 and named in **Blocker**. Do not mechanically force an unrelated play to 0; score the play using its rubric.
- **The earliest evidenced leaking stage governs non-critical investment.** A 1 at Trust and a 1 at Emotion is a Trust problem; fixing Emotion first spends effort on people who never arrive. If an earlier play is `N/E`, call the ordering provisional and put its validating check before downstream investment. A P0 at any stage overrides that order for immediate stop or repair and becomes **Fix this first**. After the critical condition is removed, resume from the earliest remaining evidenced leak.
- **Do not average away a safety or accessibility failure.** Give it its own issue line and blocker state when warranted rather than hiding it inside the total.

Dimension score, overall quality band, issue severity, critical blocker, and the earliest leaking stage are separate. Every P0 is a blocker, but a blocker does not automatically rewrite a score to 0; a score of 0 does not automatically imply P0. Non-critical methodology failures belong in the local verdict, score, sequencing, or handoff—not in **Blocker**. P0 stop-or-repair work governs **Fix this first**; otherwise the earliest leaking stage does.

## Issue severity

| Priority | Meaning |
|----------|---------|
| **P0 — Critical** | Blocks the core outcome; traps the user; destroys work or state; causes or risks material harm; hides material cost, consequence, permission, or risk; removes informed choice; or uses coercive manipulation. Fix before release. |
| **P1 — Major** | Materially damages comprehension, completion, orientation, trust, value realization, or return for a meaningful share of users. Fix before release. |
| **P2 — Moderate** | Creates real friction, confusion, dilution, or missed value with a viable recovery, workaround, or limited scope. Fix in the next planned pass. |
| **P3 — Minor** | Low-impact craft, consistency, or polish. Fix when time permits. |

Assign severity from consequence, reach, and recoverability. A methodology rule violation is not automatically P0.

**Ordering (one rule):** sort by priority, P0 first. Within the same priority, break ties by stage order—Trust, then Friction, then Wins, then Emotion—because upstream fixes change the population that reaches everything downstream. Never reorder across priorities; a P0 Emotion issue outranks a P1 Trust issue.

## Output format—use this exact structure

Every diagnosis returns this template verbatim, in this order. Don't add, remove, reorder, or rename sections. Fill the `<…>` slots; keep every fixed label. This block is the single source of truth for the emitted shape—the issue line, the table columns, and the section list exist only here.

```
**Verdict:** <the leaking stage | undetermined pending evidence> · <the one biggest loss or evidence gap, one phrase> · **<full: total/16 or N/E | targeted: play score/4>**

**Product:** <what it is, for whom> · first value: <the event, or "undefined"> · stakes: <low | medium | high>
**Scope:** <full relationship diagnosis | targeted stage: Trust | Friction | Wins | Emotion>
**Screen:** <exact touchpoint(s) or `not shown`>
**Flow:** <named journey or transition(s) or `not shown`>
**State:** <exact rendered or system state(s) reviewed>
**Lifecycle:** <exact relationship stage(s) reviewed>
**Coverage:** <relationship stages and app states actually reviewed> · gaps: <material stages or states not shown or measured, or "none">
**Basis:** <observed from a screenshot or artifact | inferred from code | tested in a prototype or live product | walked from a description | measured from product data> · confirm with: <the fastest validating check>
**Blocker:** <None. | concise blocker reason>

## Scorecard
| Play | Score | Why this score | What raises it one point |
|---|---:|---|---|
| Trust | <_/4 or N/E> | <evidence → consequence → rubric anchor, or N/E reason> | <smallest concrete change, `None—already exemplary`, or `N/E`> |
| Friction | <_/4 or N/E> | <evidence → consequence → rubric anchor, or N/E reason> | <smallest concrete change, `None—already exemplary`, or `N/E`> |
| Wins | <_/4 or N/E> | <evidence → consequence → rubric anchor, or N/E reason> | <smallest concrete change, `None—already exemplary`, or `N/E`> |
| Emotion | <_/4 or N/E> | <evidence → consequence → rubric anchor, or N/E reason> | <smallest concrete change, `None—already exemplary`, or `N/E`> |
| **Total** | **<full and complete: _/16 · _._/4 | otherwise: N/E>** | **<full and complete: band and exact sum | incomplete/targeted: why no cross-play total>** | <full and complete: weakest-play ceiling | otherwise: validating check or selected play only> |

## Issues (most severe first)
- **[P0 · Trust]** **At:** screen: <exact touchpoint> · flow: <named flow or transition> · state: <exact app state> · lifecycle: <exact relationship stage>. <Name>—<observation>. <what it costs>. **Fix:** <fix>.
- **[P1 · Friction]** **At:** screen: <exact touchpoint> · flow: <named flow or transition> · state: <exact app state> · lifecycle: <exact relationship stage>. <Name>—<observation>. <what it costs>. **Fix:** <fix>.

## Fix this first
**At:** screen: <exact touchpoint> · flow: <named flow or transition> · state: <exact app state> · lifecycle: <exact relationship stage>
<the single leaking stage, and why fixing anything downstream is premature>

## Next
- **Now**: **At:** screen: <exact touchpoint> · flow: <named flow or transition> · state: <exact app state> · lifecycle: <exact relationship stage> · <the change at the leaking stage>
- **After it moves**: **At:** screen: <exact touchpoint> · flow: <named flow or transition> · state: <exact app state> · lifecycle: <exact relationship stage> · <what becomes worth doing once that stage holds>
- **Hand off**: **At:** screen: <exact touchpoint or `not shown`> · flow: <named flow or transition or `not shown`> · state: <exact app state or `not shown`> · lifecycle: <exact relationship stage or `not shown`> · <single-screen structure → Focal; multi-screen path → Compass; expressive moment treatment → Soul; "None" if all of it is Flywheel's>
```

Filling it:
- **Coverage**—name only relationship stages and app states the evidence actually exposes. Use `gaps` for consequential stages such as first value, return, lapse, or re-engagement that were not shown or measured.
- **Scope and total**—use `/16` only when all four plays were evaluated. In a full diagnosis, an entirely unsupported play is `N/E—insufficient evidence`; in a targeted stage review, the three out-of-scope rows are `N/E—outside targeted scope`. Neither kind of `N/E` is `0`, and either prevents a total or common band.
- **Issues and suggestions**—repeat the issue line once per issue, and give every issue, Fix this first recommendation, Next item, and handoff a complete **Screen · Flow · State · Lifecycle** locator. Keep the `At` locator precise enough to identify the exact touchpoint and cohort moment that must change. `<observation>` may run two or three sentences when being specific and quantitative; the rest stay tight. If nothing ranks above P3, write "None above P3." under the Issues header and keep the header.
- **Fix this first**—one stage, never a list. The whole point of the diagnosis is to refuse to work on four things at once.
- **Basis**—never claim measurement you do not have. Use the controlled basis vocabulary in the template, and name the fastest confirming metric or behavior.
