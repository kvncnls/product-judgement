# Compass Review—the three-discipline flow audit

Evaluate a flow (or a set of screens) against the three disciplines and the overarching methodology, then return a scorecard with prioritized, concrete fixes. Use when the user asks to review, critique, audit, or "what's wrong with" any multi-screen flow, journey, or navigation in a functional product, app, or tool.

## Input modes

- **A described flow**—the user narrates the steps ("they sign up, pick a plan, then…"). Map it as a sequence, name the finite outcome or open-ended intent and home anchor, and audit the journey you reconstruct. If the narration is ambiguous, restate the sequence and ask before scoring—that is a clarifying exchange, not part of the emitted review.
- **A set of screens or screenshots**—read them in order, infer the transitions between them, and critique the joins. You're judging the *seams*, not each screen—a beautiful screen in the wrong order, or one that drops state on the way in, still fails. Per individual screen layout, defer to [Focal](../../focal).
- **A clickable prototype / live URL**—if browser automation is available, walk the flow: click through, hit Back, refresh mid-flow, follow a deep link cold. Otherwise audit the described or captured steps. Always test the transitions, not just the destinations—the failures live between screens.

## Step 0—Notice the journey, name the outcome or anchor, classify the flow

Before judging, *walk it*. Most people glance at one screen; a reviewer traces the whole path. Count the steps. Read the progress indicators and Back affordances verbatim. Note what each transition carries and what it drops. Try to get lost. The specificity of your observation is the ceiling on the quality of your critique.

Then frame, in one or two sentences each:
- **What is this journey?** Product type, what the journey is for, and its entry plus outcome or home anchor.
- **Name the outcome or anchor.** For a finite flow, settle *"This flow gets the user from ___ to ___."* If two outcomes can succeed independently, split them. For an open-ended journey, settle *"This space lets the user ___, and ___ is home."* Do not invent an end for browsing.
- **What's the user's state?** Anxious, rushed, first-time, returning, interrupted, one-handed? A checkout under time pressure tolerates fewer steps than a leisurely setup. A flow resumed after a phone call must survive the interruption. Name it; the critique must respect it.
- **Which journey states and lifecycle paths are covered?** Inventory the exact conditions walked: first run, returning, Back, refresh, validation error, retry, interruption/resume, deep link, branch change, or recovery. Mark important paths `not shown` when the artifact does not expose them.
- **What's the bar?** Every flow category has an invisible standard set by its best-in-class journey. A checkout is judged against the cleanest checkouts; an onboarding against the clearest onboardings; a multi-step setup against the cleanest wizard in the category. Ask: *what would the best-in-class flow do at this seam?*
- **The flow type.** Classify it by walking the decision tree in **Registers** in [SKILL.md](../SKILL.md)—take the first match, and don't re-derive the categories here. This sets how the gates should be read; see *Adjust for flow type* below. If the tree lands on linear but an unmanaged fork is bolted on, score it linear and flag the rogue fork under Gate 1.

## Locate every finding

Before scoring or suggesting a change, build a four-part implementation locator. Every issue, Top move, Next item, and handoff must carry the same locator:

1. **Screen**—the exact source screen, destination screen, entry point, or transition seam.
2. **Flow**—the named journey and transition being evaluated.
3. **State**—the interaction or system condition: waiting, validation error, retry, Back, refresh, deep-linked, resumed, and so on.
4. **Lifecycle**—the journey moment: first-run activation, returning completion, interruption/resume, recovery, or another specific path.

Use the narrowest defensible locator. `Email verification screen → workspace · account setup flow · code-expired error · first-run activation before entry` is actionable; `onboarding` is not. If any locator field is not evidenced, write `not shown` and name the fastest validating walk in **Coverage** or **Basis**—do not invent behavior.

## Adjust for flow type

Read the gates through the flow type you classified in Step 0. The disciplines still apply; their targets move. Scoring a hub-and-spoke or an open-ended space by linear rules produces false failures.

- **Linear** (default—checkout, onboarding, setup, wizards): score exactly as the gates describe. Progress to the end is sacred. A skippable step is waste only when skipping it loses no protection, comprehension, preference, or branch-specific value; optional does not automatically mean unnecessary.
- **Branching** (conditional signup, "what brings you here?", plan-dependent paths): Orientation must also tell the user *which branch they're on* and *how to change it*—a fork the user can't see or undo fails Gate 1. Under Path Economy, judge whether dead or rarely-taken branches are pruned and whether the common branch is defaulted. Don't penalize the existence of branches; penalize unmanaged ones.
- **Hub-and-spoke** (dashboard → record → dashboard, settings index → detail → index): *"back to the hub" is sacred*—the center is home base, and losing the way back to it is a Gate 1 failure even mid-spoke. Don't score it as a broken linear flow for "having no progress bar"; a hub has no single end. Under Path Economy, count hops out to a spoke and back—minimize them, don't funnel.
- **Open-ended** (browse, search-and-refine, exploration, infinite spaces): the exception that proves the rule. There's no single destination, so *"how far is left" does not apply*—do **not** penalize the absence of a progress indicator under Gate 1. "Never Lost" reduces to *always know where you are in the space, and how to get home*. Under Path Economy, let the user roam; don't force a funnel onto a wander. (This is the journey-level sibling of Focal's exploration register.)
- **Audience / expertise:** weigh who's traveling. Novices want guardrails—guidance, confirmations, one visible path; re-asking a novice is safer than stranding them. Experts want skips, shortcuts, remembered choices, and not to be re-asked; making an expert re-confirm a known step is the economy failure. How many steps feel "economical," and how much signposting feels like hand-holding, both scale with the audience. Don't score a pro flow's terse, skip-heavy path as under-oriented if its users have the route memorized; do score a first-run flow strictly.

A flow you can't classify is usually a linear flow with an unmanaged branch or a hidden hub—score it as linear and flag the structural confusion under Gate 1.

## The three gates

Run each gate in turn. Orientation leads—it's the load-bearing promise. Each produces a 0–4 score and the specific findings behind it.

### Gate 1—Orientation *(load-bearing)*

*At every step, can the user answer where am I, what remains when bounded, and how do I retreat, get home, or leave?*

- Run the **drop test** on every screen: drop the user onto it with no memory of how they arrived. Can they tell where they are, what remains when bounded, and how to proceed, retreat, or get home? A screen that fails those applicable questions fails Orientation.
- Check **position and progress** against the mechanism the flow type requires, in **Orientation** in [SKILL.md](../SKILL.md): a counter for linear, a named branch counted within itself for branching, an active nav state plus a labeled route to the center for hub-and-spoke, location without a counter for open-ended. A mechanism borrowed from the wrong flow type is a finding even when something is displayed. Is bounded progress framed as achievable milestones, not a demoralizing tally ("12 of 47")?
- Check for a **platform-appropriate retreat or home path** and an **escape hatch** from every owned bounded flow—especially modals and wizards. Browser Back can be sufficient when history and state behave correctly; a product-owned stack needs its own visible retreat. Do not demand duplicate controls that add no clarity.
- Hunt for **dead ends**: a screen the user can reach but not leave is a bug, not a state.
- For branching/hub flows, check that the user can see **which branch they're on** or **how to get back to the hub**.

| Score | Criteria |
|-------|----------|
| 0 | No recovery exists—a true dead end, or a flow the user cannot leave from any screen |
| 1 | A way out exists but is hidden or unlabeled; or progress is hidden and the drop test fails on a key screen. Browser Back alone is a failure only when the product owns a bounded flow, history is unsafe or surprising, or the retreat is absent from the screen's default state, reachable only by hover or gesture. A retreat that *wipes work* is Gate 3's, not this gate's |
| 2 | Orientable, but one applicable answer—where-am-I, what-remains-when-bounded, or how-to-retreat/get-home—is weak or absent at a step |
| 3 | Clear position, platform-appropriate retreat/home, and exit throughout; minor signposting gaps |
| 4 | At every step the user knows where they are, what remains when bounded, and how to proceed, retreat, get home, or escape—the journey-appropriate drop test passes everywhere |

Because this discipline is load-bearing, a true dead end on the core path is a blocker. A failed drop test is not automatically release-critical: assign severity from consequence, reach, and recoverability, and reserve blocker status for a key state where the user cannot orient, proceed, retreat, or recover.

### Gate 2—Path Economy

*For this journey type, is this the least needless effort without cutting protection?*

- **Count the steps**, then count how many the task *honestly* requires. "This is a 7-step flow that needs 3" is the finding.
- Check for **redundant screens**, needless round-trips, and steps that could **merge** without overloading a single screen (defer to Focal for whether the merged screen is too dense).
- Check whether **defaults skip steps**: is the flow asking what it could infer or pre-fill?
- Check for a **setup wall**: is first value gated behind a pile of configuration?
- **Honesty guardrail:** a step that protects the user or earns trust is not waste. Skipping a confirmation on a destructive or costly action, hiding a required disclosure, or burying the price to "reduce friction" is a **dark pattern, not economy**—score that as a failure, not a saving.

| Score | Criteria |
|-------|----------|
| 0 | The path cannot be completed as designed—branches that dead-end, or a required step the user cannot satisfy |
| 1 | Completable but badly bloated (roughly double the honest step count), a setup wall before first value, or a "shortcut" that hides cost or skips protection |
| 2 | Some waste—one or two redundant steps, or a round-trip that should be one screen |
| 3 | Lean path; a default or two could still be inferred |
| 4 | The fewest honest steps; every screen earns its place; nothing protective was cut |

### Gate 3—Continuity

*Do context and state survive the seams between screens?*

- Check for the **memory bridge**: does any step ask the user to carry a fact (a code, a choice, a number) from an earlier screen in their head, rather than showing it where it's needed?
- Test **state on Back and refresh**: does Back wipe entered data? Does a refresh or interruption resume where they left off, or reset to step one?
- Test **entry points**: does a deep link, notification, or search result land the user *in context* on the relevant screen, or dump them at the start?
- Check the **mental model**: do consecutive screens feel like one continuous task—consistent anchors, predictable transitions, the same object in focus—or like jarring jumps?

| Score | Criteria |
|-------|----------|
| 0 | The seams break the task—state lost on Back, deep links dump to step one, the user re-enters everything |
| 1 | A memory bridge on a key step, or a "resume" that resets |
| 2 | Mostly continuous, but one transition drops context or state |
| 3 | Context and state carry well; one rough seam or jarring jump |
| 4 | Nothing the user gave or knew is lost across any seam; every entry point lands in context; the journey feels like one continuous task |

## Scoring rules

Every discipline uses the same integer anchors:

| Score | Canonical label | Shared meaning |
|---:|---|---|
| **0** | **Broken or harmful** | The dimension fails outright, blocks its core outcome, actively inverts the intended behavior, or creates material harm. |
| **1** | **Major failure** | The outcome may remain technically possible, but the dimension is seriously compromised, unreliable, or largely absent. Substantial correction is required. |
| **2** | **Partial or inconsistent** | The basic function exists, with a material weakness, missing decision, or inconsistency that prevents dependable quality. |
| **3** | **Strong** | Deliberate, dependable, context-appropriate professional work with only minor gaps. This is the normal target for good execution. |
| **4** | **Exemplary—above and beyond** | Fully realized and unusually effective for the relevant context, including realistic states and constraints. This is intentionally uncommon, not the normal target. |

Score each discipline holistically against its local rubric. Read all checks and evidence, choose the anchor that best describes the dimension overall, apply explicit local caps or prerequisites, and let one severe material failure determine the score when the rubric warrants it. Do not use hidden sub-scores, checklist subtraction, averaging, or half-points. A 4 is exemplary for the dimension being scored; it does not universally require novelty.

### Score rationale—required

A score without an explanation is invalid. Fill every scorecard row with the same chain: **evidence → consequence → rubric anchor → next-point change**. State what was observed, inferred, tested, walked, or measured; what it costs the user; why that evidence earns the integer under the local rubric and stops there; and the smallest concrete change that would raise it one point. A `2` must say what works and name the material weakness; a `3` must name the remaining gap; a `4` must explain why the discipline is exemplary and say `None—already exemplary` in the next-point field. If the evidence does not expose a state or transition, say `not shown` in Coverage/Basis and name the validating check—do not award credit or invent failure.

Keep the native total: `total = Orientation + Path Economy + Continuity`. Calculate `average = total / 3`, display it rounded to one decimal place, and apply this shared algorithm:

| Band | Average rule | Native total |
|---|---:|---:|
| **Broken** | `average <= 1.5` | `0–4 / 12` |
| **Significant rework** | `1.5 < average < 2.5` | `5–7 / 12` |
| **Solid** | `2.5 <= average < 3.5` | `8–10 / 12` |
| **Excellent** | `average >= 3.5` | `11–12 / 12` |

Then cap the band by the weakest discipline: a minimum of `0` allows only **Broken**, `1` allows at most **Significant rework**, `2` allows at most **Solid**, and `3–4` adds no ceiling. Use the lower-quality result of the average band and this ceiling. The total must equal the exact sum of the three scores.

- **Score 0 vs 1 (Orientation only).** Score **0** when the flow strands the user with no recovery at all—a true dead end, or a flow with no exit anywhere. Score **1** when a way out exists but is hidden, surprising, unsafe, or unlabeled. Browser Back is not inherently a failure; judge whether it is the expected, discoverable, state-safe retreat for this platform and flow. A retreat that *wipes work* is a Continuity failure, scored by Gate 3.
- If more than one independent failure sits in a discipline, score the *worst* one, then list the others as separate issues.
- **The verdict—Never Lost.** Yes or no: at every step, does the user know where they are, what remains when bounded, and how to retreat, get home, or leave? The total measures how close the journey gets; the verdict states whether it arrives. A true dead end on the core path is a blocker; other drop-test failures take severity from their actual consequence.
- **A doubled destination** (the flow needs an "and") is an Orientation failure; assign P0 only when its consequence meets the shared critical definition, and flag it as the split it implies.

Dimension score, overall quality band, issue severity, critical blocker, and the **Never Lost** verdict are separate. Every P0 is a blocker, but a blocker does not automatically rewrite a score to 0; a score of 0 does not automatically imply P0. Non-critical methodology failures belong in the local verdict, score, sequencing, or handoff—not in **Blocker**.

## Issue severity

| Priority | Meaning |
|----------|---------|
| **P0 — Critical** | Blocks the core outcome; traps the user; destroys work or state; causes or risks material harm; hides material cost, consequence, permission, or risk; removes informed choice; or uses coercive manipulation. Fix before release. |
| **P1 — Major** | Materially damages comprehension, completion, orientation, trust, value realization, or return for a meaningful share of users. Fix before release. |
| **P2 — Moderate** | Creates real friction, confusion, dilution, or missed value with a viable recovery, workaround, or limited scope. Fix in the next planned pass. |
| **P3 — Minor** | Low-impact craft, consistency, or polish. Fix when time permits. |

Assign severity from consequence, reach, and recoverability. A methodology rule violation is not automatically P0.

**Ordering (one rule):** sort by priority, P0 first. Within the same priority, break ties by type of harm—**Orientation** (the user is lost or trapped) outranks **Path Economy** (the path is longer or less honest than it should be) outranks **Continuity** (a seam drops context or state). Never reorder across priorities; a P0 Continuity issue outranks a P1 Orientation issue.

## Output format—use this exact structure

Every review returns this template verbatim, in this order. Don't add, remove, reorder, or rename sections. Fill the `<…>` slots; keep every fixed label. This block is the single source of truth for the emitted shape—the issue line, the table columns, and the section list exist only here.

```
**Verdict:** <No | Yes> · <the single biggest break, one phrase> · **<total>/12**

**Flow:** <name> · type: <linear | branching | hub-and-spoke | open-ended> · audience: <novice | mixed | expert>
**Outcome / anchor:** <finite destination | open-ended organizing intent + home anchor>
**Screen:** <source and destination screens or exact seam reviewed>
**State:** <exact interaction or system state(s) reviewed>
**Lifecycle:** <exact journey moment(s) reviewed>
**Context:** <the user's state in a few words> · bar: <the best-in-class comparator you judged against>
**Coverage:** <journey states and lifecycle paths actually reviewed> · gaps: <material paths not shown or tested, or "none">
**Basis:** <observed from a screenshot or artifact | inferred from code | tested in a prototype or live product | walked from a description | measured from product data> · confirm with: <the fastest validating check>
**Blocker:** <None. | concise blocker reason>

## Scorecard
| Discipline | Score | Why this score | What raises it one point |
|---|---:|---|---|
| Orientation | _/4 | <evidence → consequence → rubric anchor> | <smallest concrete change, or `None—already exemplary`> |
| Path Economy | _/4 | <evidence → consequence → rubric anchor> | <smallest concrete change, or `None—already exemplary`> |
| Continuity | _/4 | <evidence → consequence → rubric anchor> | <smallest concrete change, or `None—already exemplary`> |
| **Total** | **_/12 · _._/4** | **<band; exact sum of justified component scores>** | <weakest-discipline ceiling applied> |

## Issues (most severe first)
- **[P0 · Orientation]** **At:** screen: <source/destination screen or seam> · flow: <named flow and transition> · state: <exact state> · lifecycle: <exact journey moment>. <Name>—<observation>. <impact>. **Fix:** <fix>.
- **[P1 · Path Economy]** **At:** screen: <source/destination screen or seam> · flow: <named flow and transition> · state: <exact state> · lifecycle: <exact journey moment>. <Name>—<observation>. <impact>. **Fix:** <fix>.

## Top moves (up to 3)
1. **At:** screen: <source/destination screen or seam> · flow: <named flow and transition> · state: <exact state> · lifecycle: <exact journey moment> · <highest-leverage change>
2. **At:** screen: <source/destination screen or seam> · flow: <named flow and transition> · state: <exact state> · lifecycle: <exact journey moment> · <next>
3. **At:** screen: <source/destination screen or seam> · flow: <named flow and transition> · state: <exact state> · lifecycle: <exact journey moment> · <next>

## Next
- **Structural** (do first): **At:** screen: <source/destination screen or seam> · flow: <named flow and transition> · state: <exact state> · lifecycle: <exact journey moment> · <what changes what the journey *is*—steps to cut or merge, a branch to manage, a dead end to close, state to carry, an entry point to re-route>
- **Executional** (after): **At:** screen: <source/destination screen or seam> · flow: <named flow and transition> · state: <exact state> · lifecycle: <exact journey moment> · <what changes how a step *looks or reads*—indicator weight, Back label wording, transition motion>
- **Hand off**: **At:** screen: <source/destination screen or seam or `not shown`> · flow: <named flow or `not shown`> · state: <exact state or `not shown`> · lifecycle: <exact journey moment or `not shown`> · <anything that is not this flow's problem—single-screen layout or hierarchy goes to Focal; "None" if all of it is Compass's>
```

Filling it:
- **Coverage**—name only conditions actually walked or evidenced. Use `gaps` for consequential paths such as Back, refresh, retry, interruption/resume, deep link, or returning-user bypass that were not shown or tested.
- **Issues and suggestions**—repeat the issue line once per issue, and give every issue, Top move, Next item, and handoff a complete **Screen · Flow · State · Lifecycle** locator. Emit one to three Top moves only when each is warranted; never invent filler to reach three. If none is warranted, write `None.` Keep the `At` locator precise enough to replay the failing transition directly. `<observation>` may run two or three sentences when specificity requires it. If nothing ranks above P3, write "None above P3." under the Issues header and keep the header.
- **Next**—structural before executional, always: signposting a maze only labels the dead ends. Resolve structural items with the four-move build workflow in [SKILL.md](../SKILL.md) and the techniques in [patterns.md](patterns.md).
- **Single-screen problems are out of scope—route them to [Focal](../../focal).** If an individual screen is overloaded, mis-ranked, or has no clear primary action, that is a within-screen failure for Focal, not a seam for Compass; name it in **Next** and hand it off.
- Re-run the audit after fixes to watch the score climb.
