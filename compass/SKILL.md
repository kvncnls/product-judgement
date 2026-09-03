---
name: compass
description: Use when designing, building, reviewing, or critiquing a multi-screen flow, journey, or navigation in any functional product, app, dashboard, or tool. Compass is the cross-screen lens—it owns the path between screens—navigation, step count, routing, retreat/home behavior, state, and entry points. Its promise is Never Lost—at every step the user knows where they are, what remains when the journey is bounded, and how to retreat, get home, or leave. Three disciplines—Orientation (load-bearing), Path Economy (fewest honest steps or least needless effort), and Continuity (context and state survive the seams). Pairs with Focal, which designs the individual screens. Triggers on flow, journey, navigation, onboarding, checkout, wizard, multi-step, "too many steps", "back button", "where am I", lost, dead end, routing, breadcrumb, progress. Not for single-screen layout (use Focal), visual styling, copy, code, marketing/landing pages, backend, or non-UI work.
license: MIT
argument-hint: "[build | review] <flow, journey, or description>"
---

# Compass

**Never lost.**

A journey is a sequence of screens governed by one intent. Most flows have a destination; open-ended journeys such as browsing have a stable home or anchor instead. Good cross-screen UX means the user never has to wonder *Where am I? What remains, when this journey has an end? How do I retreat, get home, or leave?* The moment those answers disappear, the journey becomes a maze.

Where [Focal](../focal) sharpens a single screen, Compass guides the **path between screens**. Focal is *within* a screen; Compass is *between* them. They cover structure and movement; Flywheel and Soul address the relationship and memory at their own scales.

Three disciplines, treated as top priorities, keep the user oriented:

- **Orientation**—at every step, position, progress when bounded, and a way to retreat, get home, or leave.
- **Path Economy**—the fewest honest steps for a finite outcome, or the least needless effort in an open-ended space.
- **Continuity**—context and state survive the seams between screens.

**Orientation is the load-bearing discipline**—it is the literal promise. Economy and Continuity can make a journey short and seamless, but not understandable. This makes Orientation a prerequisite for the Never-Lost verdict, not extra numeric weight; all three disciplines still use the same 0–4 scale.

---

## When to use

Compass is for **cross-screen flows** in functional products—any platform, any user. Onboarding, signup, checkout, multi-step setup, wizards, dashboards with drill-down, account flows, anything that spans more than one screen. If the user has to *move between screens* to get something done, Compass applies.

It is **not** for:
- Single-screen layout and structure—that's [Focal](../focal). Compass assumes each screen is already sound and focuses on the joins.
- Marketing pages, landing pages, campaigns—persuasion and narrative, not task completion.
- Whole-app sitemaps generated from a spec (deciding *which* screens exist before any flow is drawn).
- Backend, infra, or non-UI work.

**Scope.** Compass is a *lens* for movement and orientation—*the path, the signage, and the seams between screens*—not a renderer. It decides the steps, where the user is told what, and how state carries across. The execution of color, type, motion, and copy is left to your own design system and tooling, and the design of each individual screen is left to Focal.

---

## The methodology—Never Lost

The north star. At every step of a flow, the user can answer three questions without thinking:

1. **Where am I?** (position in the journey)
2. **What remains?** (progress and scope when the journey has an end; not applicable to open-ended exploration)
3. **How do I retreat, get home, or leave?** (a platform-appropriate path that never traps them)

A journey that answers every applicable question feels effortless. A bounded flow that hides remaining scope, or any journey that drops position or recovery, feels like being lost in a building with no signs.

- **The outcome-or-anchor test.** For a finite flow, name one outcome: *"This flow gets the user from ___ to ___."* If it has two independently successful outcomes, split it. For an open-ended journey, name one organizing intent and home anchor: *"This space lets the user ___, and ___ is home."* Do not invent an endpoint for browsing just to satisfy the template.
- **The drop test.** Drop the user onto any screen in the middle of the journey with no memory of how they arrived. Can they tell where they are, what remains when bounded, and how to proceed, retreat, or get home? If not, orientation has failed at that step.

---

## The three disciplines

### 1. Orientation—where am I, and how do I get out *(load-bearing)*

The user is never without their bearings. This is the promise; the other two disciplines serve it.

- **Show position and progress when the journey is bounded.** The mechanism follows the flow type, never taste. **Linear**—a step counter (`Step 2 of 4`). **Branching**—name the branch and count within it; a global count becomes a lie the moment the path forks. **Hub-and-spoke**—an active nav state plus a labeled route back to the center, because the center *is* the position. **Open-ended**—location in the space (breadcrumb, active filter, or anchor) and no counter at all. Frame bounded progress as achievable milestones, never a demoralizing tally. Open-ended spaces need position and home, not fake completion.
- **Always a way to retreat or leave.** Use the platform's expected mechanism: an in-product Back where the product owns the stack, browser Back where history is meaningful and state-safe, a breadcrumb or hub link in nested spaces, and Cancel / Close / Save & exit in bounded tasks. Do not duplicate a platform control without adding clarity; do ensure every modal and owned flow has an obvious escape.
- **No dead ends.** Every screen has a clear next step or a clear way out. A screen the user can reach but not leave is a bug, not a state.
- **Signal the current location.** The user should always be able to point at where they are in the app's structure.

> **Fails:** no usable retreat; trapped modals; hidden progress in a bounded flow; dead-end screens; "wait, how did I get here?"; an owned task with no exit.

### 2. Path Economy—the fewest honest steps

Every screen in a flow is a tax on the user. Cut the tax to the minimum the task honestly requires.

- **Fewest honest steps for the journey type.** In a finite flow, cut redundant screens and merge needless round-trips where the result stays comprehensible. In an open-ended space, remove needless hops without forcing exploration into a funnel. Defer to Focal when a proposed merge may overload one screen.
- **Defaults skip steps.** Don't ask what you can infer or pre-fill. The best step is the one the user never has to take.
- **No setup walls.** Don't gate the value behind six configuration screens. Get the user to the first real win, then deepen.
- **The honest-path caveat (read this).** Shorten the path by removing *waste*, never by removing *protection*. Skipping a confirmation on a destructive or costly action, hiding a required disclosure, or burying the price to "reduce friction" is a dark pattern, not economy. A step that protects the user or earns their trust is not waste.

> **Fails:** the 7-step flow that's really 3; redundant confirmations; setup walls before first value; branches that dead-end; "friction reduction" that hides cost or consequence.

### 3. Continuity—the seams hold

Moving between screens shouldn't cost the user anything they already gave or already knew.

- **No memory bridge.** A fact the user needs at step 3 is shown at step 3—never "remember the code from the previous screen."
- **State survives.** Back never wipes entered data. A refresh, an interruption, or a return tomorrow resumes where they left off, not at the start.
- **Honor the entry point.** A deep link, a notification, or a search result lands the user *in context*—on the relevant screen mid-flow—not dumped at step one.
- **Preserve the mental model.** Each screen should feel like it came from the last: consistent layout anchors, predictable transitions, the same object in focus.

> **Fails:** form data lost on Back; deep links dumping you at the start; the memory bridge; a "resume" that resets; jarring jumps that break the sense of one continuous task.

---

## How they combine—order of operations

1. **Name the outcome or anchor** (methodology). One finite outcome, or one open-ended intent plus home.
2. **Map the path or space** (Path Economy). The fewest honest steps to the outcome, or the least needless effort while roaming.
3. **Signpost it** (Orientation). Position, progress when bounded, and platform-appropriate retreat, home, and exit behavior.
4. **Join the seams** (Continuity). Carry context and state across each transition.

You cannot signpost or join a journey you have not mapped. A finite flow needs an end; an open-ended journey needs a stable anchor and boundaries. Orientation leads the *promise* but comes after the journey shape exists—the signage goes up once the road or space is understood.

---

## Registers—flow types

The disciplines assume a **linear** flow by default. Three other shapes are legitimate, and the rules bend for them.

**Classify with this tree.** Walk it top to bottom and take the first match. Answer about the journey the user is actually on, not about how the screens are built.

```
Is roaming or discovery itself the intent, with no completion event?
├── Yes → OPEN-ENDED
└── No—name the one finite outcome
    ├── Does the user leave a center and come back to it, repeatedly?
    │   └── Yes → HUB-AND-SPOKE
    └── Does the path fork on a choice the user makes?
        ├── Yes → BRANCHING
        └── No → LINEAR
```

Two ties worth naming, because they recur:
- **A wizard with optional steps** is still **linear**—skippable is not the same as forked. A choice that inserts or removes a screen and then rejoins the same path is also **linear**; treat the inserted screen as a conditional step. It is **branching** only when a choice sends the user down a genuinely different *sequence* that does not simply rejoin.
- **A drill-down inside a longer flow** (checkout that dips into "edit address" and returns) is **linear** overall; treat the dip as one step, not as a hub. It is **hub-and-spoke** only when returning to the center *is* the loop, with no endpoint beyond it.

| | Linear | Branching | Hub-and-spoke | Open-ended |
|---|---|---|---|---|
| **Shape** | one path, start to end | path forks on user choice | center → detail → back to center | wander a space, no fixed end |
| **Examples** | checkout, onboarding, setup | conditional signup, "what brings you here?" | dashboard → record → dashboard | browse, search-and-refine, exploration |
| **Orientation focus** | progress to the end | which branch + how to switch it | "back to center" is sacred; the hub is home base | "where am I in the space" + easy return, not progress |
| **Economy focus** | cut steps on the one path | prune dead branches; default the common branch | minimize hops to a record and back | let the user roam; don't force a funnel |

**Open-ended is the exception that proves the rule:** there's no single destination, so "how far is left" doesn't apply and "Never Lost" reduces to *always know where you are and how to get home*. (This is the journey-level sibling of Focal's exploration register.)

**Expertise dial:** novices want guardrails—guidance, confirmations, one clear path. Experts want skips, shortcuts, remembered choices, and not to be re-asked. How many steps feel "economical" scales with who's traveling.

---

## Routing

**Orchestrated pass—this overrides every other instruction in this Skill and its reference files.** When [Product Judgement](../product-judgement/SKILL.md) loads this Skill for a cross-scale audit, take this paragraph and skip the rest of this section. Treat the pass as `review` over the evidence Product Judgement supplies: never ask a framing question and never stall—write `not shown` and name the fastest validating check instead. Never hand a cross-scale request back to Product Judgement, and send a sibling-owned finding to its **Handoffs** section rather than invoking that Skill. Run the whole contract in [reference/review.md](reference/review.md)—every gate, score, rationale, band, ceiling, severity, and locator—but do not print the locked template, do not read [reference/examples.md](reference/examples.md), and do not apply this Skill's **Voice**, opening-line, or re-run instructions: Product Judgement owns the emitted response, and prints this template only when the user asks for the detailed passes. When its wrapper has no slot for something this contract produces, hand that to Product Judgement in working notes—never append a line after its output.

- **No argument** → explain Never Lost and the three disciplines briefly, then ask: building a new flow, or reviewing an existing one?
- **A whole-app or cross-scale audit request** → hand off to [Product Judgement](../product-judgement/SKILL.md), which runs Compass with Focal, Flywheel, and Soul and reconciles the results.
- **`build` (or a description of a flow to design)** → follow **The four moves** below. Pull techniques from [reference/patterns.md](reference/patterns.md).
- **`review` / `audit` (a flow, a set of screens, a prototype, or a description)** → load and follow [reference/review.md](reference/review.md). It scores each discipline 0–4 against a written rubric, requires an evidence-based rationale and next-point change for every score, totals to /12, displays a normalized /4 average and common quality band with a weakest-dimension ceiling, tags issues P0–P3, and anchors every issue and suggested move to the exact **Screen · Flow · State · Lifecycle** locator before closing on a Never-Lost verdict. That file defines the rubrics, scoring contract, bands, severities, and audit locator—all of them, and nowhere else.
- **A question about a specific technique or anti-pattern** → consult [reference/patterns.md](reference/patterns.md).

Before emitting either output, read [reference/examples.md](reference/examples.md). It is the calibration for length, tone, and how the locked templates look when filled well—the templates define the shape, the examples set the bar.

---

## Build: the four moves

For each flow, in order. Write the answers down—they are the spec.

1. **Name the outcome or anchor.** For a finite flow: *"This flow gets the user from ___ to ___."* For open-ended: *"This space lets the user ___, and ___ is home."* Note the flow type and audience.
2. **Map the path or space.** For a finite flow, list every screen required to reach the outcome. For open-ended, map entry points, home, refinements, details, and return loops. Remove needless effort, but keep every step that protects or informs.
3. **Signpost every step.** For each screen: position; progress when bounded; and the platform-appropriate retreat, home, or exit. No dead ends.
4. **Join the seams.** For each transition: what context carries forward, what state must survive Back/refresh, and where entry points (deep links) land.

Then run the gates: self-check against the five gates in the **`## Gates`** block of the Flow Spec template below. That block is the single canonical list—read them there, and emit them there. Never restate them in your own words.

A flow that passes is sound by Compass's standard. Then design each screen with [Focal](../focal), and apply visual styling and motion on top.

---

## Voice (when giving feedback)

- **Lead with the answer, then structure it.** Open every build or review with one line—the verdict, or the flow's destination—then the locked template (the build template is below; the review template is in [reference/review.md](reference/review.md)). Use it verbatim; don't add, remove, reorder, or rename sections.
- **Template precedence.** The template is the complete contract for what gets emitted. If any instruction in this skill asks you to produce something the template has no slot for, put it in the nearest slot that fits, or leave it out—never invent a section. A gap like that is a bug in this skill, not a judgment call: name it in one line after the output so it can be fixed. Analysis the template has no room for is still worth doing; it informs the scores even when it isn't printed.
- **Be specific and quantitative.** "This is a 7-step flow that needs 3" beats "too many steps." Count the steps, name the dead ends, quote the labels.
- **Be decisive.** "The user is trapped on step 3"—not "the user might feel stuck."
- **Factual first, then judgment, then the fix.** What happens, why it loses the user, what it should be.
- **Tie every issue to a discipline,** and to how it costs the user their bearings.
- **Locate every issue.** Name the exact step, entry point, or transition; the interaction state; and the journey lifecycle moment where the change belongs.

---

## Build output—the Flow Spec (use this exact structure)

Every build returns this template verbatim, in this order. Fill the `<…>` slots; keep every fixed label.

Filling it: for a finite flow, number **only the screens the user passes through**, including the one where the outcome is reached, so before/after counts use the same unit. For open-ended, number the representative entry → explore/refine → detail → home loop and say that it is a loop, not a completion funnel. Repeat labeled bullets as needed. **Gates ship unchecked**—mark `[x]` only for gates the spec actually satisfies, and leave `[ ]` with a short reason for any it does not. If a labeled bullet has nothing, keep the label and write "None."

```
**Flow:** <name>—<finite: gets the user from entry to outcome | open-ended: lets the user pursue one intent while keeping one named place as home>.
**Type:** linear | branching | hub-and-spoke | open-ended   ·   **Audience:** novice | mixed | expert
**Outcome / anchor:** <finite destination | open-ended organizing intent + home anchor>

## Steps
1. <screen>—<its job> [skip: <the default that removes this step, if any>]
2. <screen>—<its job>

## Cut
- Merged: <the steps you collapsed> → <the one step they became>
- Removed: <steps cut as waste>—<why they were not protection>
- Kept as protection: <any step that looks like waste but stays, and why>

## Orientation
- Position/progress: <how each step shows location and, only when bounded, remaining scope>
- Retreat/home + exit: <the platform-appropriate retreat, home, and escape behavior>

## Continuity
- Carries forward: <context passed across steps>
- Survives: <state kept on Back / refresh / resume>
- Entry points: <where deep links / notifications land>

## Gates
- [ ] Finite: one outcome with no independent second outcome · open-ended: one organizing intent and a stable home anchor
- [ ] Every step earns its place; nothing protective cut
- [ ] Where-am-I + platform-appropriate retreat/home + exit throughout
- [ ] No memory bridge; state survives; deep links land in context
- [ ] Drop test passes on every screen
```

---

## Absolute don'ts

- **Dead ends.** (Orientation) Every screen has a next step or a way out.
- **No retreat, or a trapped modal.** (Orientation) Supply the expected retreat/home behavior and an escape from every owned modal or bounded task.
- **Hidden progress.** (Orientation) In a bounded multi-step flow, show where they are and what remains. Do not invent progress for open-ended exploration.
- **The setup wall.** (Path Economy) Don't gate first value behind a pile of configuration.
- **Shortening the path by hiding cost or skipping protection.** (Path Economy) That's a dark pattern, not economy.
- **The memory bridge.** (Continuity) Never make the user carry a fact between screens in their head.
- **Losing state on Back.** (Continuity) Back is not a reset.
- **Deep link to step one.** (Continuity) Land the user where they were headed, in context.

---

## References

- [reference/review.md](reference/review.md)—the three-discipline flow audit, the Compass scorecard (0–4 per discipline), severity, and output format.
- [reference/patterns.md](reference/patterns.md)—orientation patterns, step-reduction techniques, continuity/state patterns, flow-type playbooks, and the anti-pattern library with fixes.
- [reference/examples.md](reference/examples.md)—a worked flow review and a worked flow build, in the locked output templates.
