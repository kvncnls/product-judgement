---
name: flywheel
description: Use when improving how a product converts attention into durable value—the growth and retention side of design. Flywheel finds where a product loses the people it already earned, then applies the play that fixes that relationship stage across four ordered plays—Trust, Friction, Wins, and Emotion. A full relationship diagnosis evaluates all four plays and reports /16 only when each is supportable; a targeted stage review scores one play without fabricating a cross-play total. Triggers on growth, retention, activation, onboarding, conversion, churn, drop-off, first impression, time to value, empty state, upgrade prompt, referral, advocacy, "why do users leave", "nobody comes back", or "they sign up but never return". Not for screen-local structure (use Focal), route mechanics or journey orientation (use Compass), expressive treatment (use Soul), paid channels, campaign copy, analytics instrumentation, or research protocols.
license: MIT
argument-hint: "[build | diagnose] <product, stage, or symptom>"
---

# Flywheel

**Earn the second visit.**

A product's journey is usually drawn as a funnel—attention narrowing to trust, to activation, to value, to payment. But look at the last stage. People who return and bring others feed the top again. The chain closes. It is not a funnel, it is a wheel.

That changes what design is for. A funnel asks how to lose fewer people on the way down. A wheel asks how much energy the system stores, and whether each turn is easier than the last.

Four properties of a real flywheel decide everything here:

- **It is hardest to start.** At rest, inertia is highest, and the first turn costs the most.
- **Every push adds to what is already stored.** Force accumulates rather than dissipating.
- **Its mass keeps it turning between pushes.** A heavy wheel coasts; a light one stops the moment you stop pushing.
- **Friction steals what is stored.** An unmaintained wheel slows even while you push.

**The four plays are the four parts of the wheel**, and they run in this order:

| Play | The part | The question |
|---|---|---|
| **1. Trust** | the first push | Is this relevant, credible, and worth continuing? |
| **2. Friction** | drag on the bearing | Can I reach value without getting lost or exposed? |
| **3. Wins** | the power stroke | Did this improve my situation, and what now? |
| **4. Emotion** | the mass | How did that feel, and do I prefer it? |

The order is not a preference. Emotional polish cannot rescue a product that feels untrustworthy, and a perfectly timed referral prompt cannot rescue a product nobody reached value in. **You cannot add mass to a wheel that never started turning.**

---

## When to use

Flywheel is for **what attention becomes**—turning arrival into trust, trust into activation, activation into value, value into return, and return into new arrivals. That last clause is not a flourish: the wheel closes, so the moments that earn word of mouth are in scope alongside the ones that earn a second visit. Onboarding, first-run, activation paths, empty states, success states, upgrade and referral moments, re-entry, win visibility.

It is **not** for:
- Single-screen structure, hierarchy, or clutter—that is [Focal](../focal).
- Getting the user through a multi-screen path without getting lost—that is [Compass](../compass).
- **Buying** attention—paid channels, budget allocation, bidding, SEO, campaign copy. Flywheel designs what attention meets when it arrives, and what makes people bring more of it. It does not buy it. Earned acquisition is in scope; paid acquisition is not.
- Analytics instrumentation, event schemas, research protocols, or experiment statistics. It tells you which measurement would settle a question; it does not build the measurement.

**Scope.** Flywheel is a *lens* for the transitions between stages of a relationship—where value is lost and how a stage earns the next one. It decides which stage is leaking, why, and what to change. The execution of color, typography, spacing, and motion is left to your own design system.

**Flywheel cannot manufacture product-market fit.** It prevents a valuable product from hiding its value behind uncertainty, effort, silence, or forgettability. If the product does not solve a real problem, every play below will make a well-designed thing nobody wants.

---

## Diagnose first—which play do you need?

A **full relationship diagnosis evaluates all four plays**, because the earliest leak can sit upstream of the symptom the user named. It scores every play supported by evidence and reports `/16` only when all four are evaluable. It still selects only one stage to fix first; scanning four is not permission to redesign four. A **targeted stage review or build runs one play deeply** and does not invent a `/16` total. Walk this tree top to bottom and take the first evidenced match.

```
Where does the product lose people?
├── They arrive and leave without engaging ............... TRUST
│     the wheel never starts
├── They engage but never reach first value ............. FRICTION
│     drag steals the push
├── They reach value but do not return or convert ....... WINS
│     the power stroke lands and nothing is stored
└── They return for a while, then drift away ............ EMOTION
      the wheel has no mass
```

**Name first value before you walk the tree.** Branches 2 and 3 are separated by exactly that line, and nothing else—so an undefined first value makes the tree unwalkable, and undefined is the common case. If the team has not named it, use the strictest outcome the available product evidence can defend: the moment the user's situation changes, not the moment setup ends. Say which definition you used, because a looser one moves the whole diagnosis from Friction to Wins and changes every fix that follows. Missing internal terminology is context to align, not an automatic UX score penalty; score the experience the user actually receives.

**If two stages both leak, take the earliest among non-critical improvements.** Loss compounds downstream: a fix at Wins is wasted on people who never got past Friction. A P0 at any stage overrides that investment order for immediate stop or repair; once the critical condition is removed, resume from the earliest remaining leak.

### Diagnosing with data, and without it

**With funnel data**, the leak is where the drop-off is. Compare stage-to-stage conversion, and prefer cohorts with a shared start point over aggregate averages. Read distributions, not means—a median time-to-value can hide a long tail of people who are stuck.

**Without data**, which is the common case, diagnose from the artifact using the play's own audit checks, and say plainly which measurement would confirm it. Never stall for want of numbers, and never present a heuristic finding as a measured one—say the finding was diagnosed from the artifact, and name the metric that would confirm it. Both output templates have a slot for exactly that.

**Pick the confirming metric by what would change the verdict.** Each play's *What to measure* section is a menu; this rule picks from it, and it picks **one**. State it as a comparison, not only a level: the completion rate of the exact step you blamed, and the return or conversion rate of people who clear it versus those who do not. That comparison can support or weaken the diagnosis, but observational cohorts show association, not causation; use an experiment or additional evidence before claiming the step caused the outcome.

### Two modifiers

**Stakes.** In finance, health, children's products, employment, housing, education, identity, and safety, raise the standard. Protective friction is a growth foundation in these contexts, not a conversion problem—durable trust matters more than immediate completion, and a removed safeguard costs more than it earns.

**Motivation.** Effort must stay proportional to how much the user currently wants the outcome. The same form is reasonable at high motivation and fatal at low. Ask where in the journey the user is before judging whether a step is too much.

---

## The four plays

Each play has its own reference file. The review contract contains the light scan for all four. Read the selected play's reference for the deep diagnosis or build; read another only when evidence identifies a second independent issue. This keeps the work stage-focused without hiding upstream context.

### 1. Trust—the first push
*Read [reference/trust.md](reference/trust.md).*

The user is deciding whether this is relevant, credible, and worth another minute. Five layers, in order: **relevance** (I recognize the problem), **comprehension** (I understand the mechanism and the next step), **credibility** (the promise is supported), **craft** (this is coherent and maintained), **safety** (I know what will happen and keep control).

Craft is not a substitute for truth. Its job is to make the product's real quality legible.

### 2. Friction—drag on the bearing
*Read [reference/friction.md](reference/friction.md).*

The goal is not zero friction. It is **useful momentum**. Six kinds of friction, and only two of them are waste: accidental and cognitive friction should go, procedural friction should be automated or explained, commitment friction should move after value, and **protective and productive friction should stay**. Removing a safeguard is not a speed improvement; it is the bearing coming out of the wheel.

Define first value before redesigning onboarding. Activation is experiencing value, not completing setup.

### 3. Wins—the power stroke
*Read [reference/wins.md](reference/wins.md).*

Products deliver value silently and then wonder why nobody noticed. A win is a moment the user's situation measurably improves. Find them, make them visible, size the feedback to the magnitude, and place every ask *after* the value it relates to.

An ask before value converts stored momentum into resistance. That is braking your own wheel.

### 4. Emotion—the mass
*Read [reference/emotion.md](reference/emotion.md).*

What makes the wheel keep turning between visits. Name the relationship state the job calls for—confidence, control, momentum, mastery—and test whether it changes future behavior. Restore context on re-entry, show accumulated value, and give the user a real reason to continue rather than a novelty prompt.

Flywheel owns whether the relationship earns return, preference, and advocacy. Soul owns the expressive treatment of memorable moments. A product can have strong relationship mass through useful continuity and compounding value without being visually distinctive.

---

## Routing

**Orchestrated pass—this overrides every other instruction in this Skill and its reference files.** When [Product Judgement](../product-judgement/SKILL.md) loads this Skill for a cross-scale audit, take this paragraph and skip the rest of this section. Treat the pass as `diagnose` over the evidence Product Judgement supplies: never ask a framing question and never stall—write `not shown` and name the fastest validating check instead. Never hand a cross-scale request back to Product Judgement, and send a sibling-owned finding to its **Handoffs** section rather than invoking that Skill. Run the whole contract in [reference/review.md](reference/review.md)—every gate, score, rationale, band, ceiling, severity, and locator—but do not print the locked template, do not read [reference/examples.md](reference/examples.md), and do not apply this Skill's **Voice**, opening-line, or re-run instructions: Product Judgement owns the emitted response, and prints this template only when the user asks for the detailed passes. When its wrapper has no slot for something this contract produces, hand that to Product Judgement in working notes—never append a line after its output. Run the full four-play diagnosis; read an individual play's reference file only when a next-point change cannot be grounded without it.

- **No argument** → explain the wheel and the four plays briefly, then ask: diagnosing an existing product, or designing a relationship stage?
- **A whole-app or cross-scale audit request** → hand off to [Product Judgement](../product-judgement/SKILL.md), which runs Flywheel with Focal, Compass, and Soul and reconciles the results.
- **`diagnose` / `audit` / `review` of the product or relationship** → load and follow [reference/review.md](reference/review.md). A full diagnosis evaluates all four plays, scores every supported play 0–4, reports `/16` only when all four are evaluable, and selects the earliest evidenced leak. A request explicitly limited to one stage uses the same rubric but reports that play `/4` with no fabricated `/16` total. Both modes require evidence-based rationales, P0–P3 issues, and exact **Screen · Flow · State · Lifecycle** locators.
- **`build` (a relationship stage to design)** → name first value, walk the diagnosis tree to confirm which stage, read that play's reference, then follow **Design** below. That order is fixed: the tree cannot be walked before first value is named.
- **A question about one play** → read that play's reference file.

Before emitting either output, read [reference/examples.md](reference/examples.md). It is the calibration for length, tone, and how the locked templates look when filled well.

---

## Design a relationship stage: the five moves

Designing a relationship stage needs one input Focal and Compass do not: you cannot design trust or activation in the abstract. Establish the frame first.

1. **Frame it.** What is the product, who is this stage for, and **what is the first-value event?** Name it as something that changes the user's situation, not as setup completed. "Created an account" is not first value; "imported data and got an actionable insight" is. Name it even when the stage sits after value—the Stage Spec has a slot for it either way, and a stage designed without knowing what value it follows is a stage designed blind.
2. **Name the stage and its leak.** Which of the four is this, and what is being lost there today (or what would be, if this ships wrong).
3. **Run the play.** Read that reference and apply it. One play, not four.
4. **Place the ask.** If this stage contains a commercial or social ask—upgrade, invite, share, rate, connect—state what value lands before it and why accepting extends that value. If no value lands first, move the ask or cut it.
5. **Run the gates.** Self-check against the **`## Gates`** block of the Stage Spec template below. That block is the single canonical list—read them there, and emit them there. Never restate them in your own words.

**Output—the Stage Spec (use this exact structure).** Every build returns this template verbatim, in this order. Fill the `<…>` slots; keep every fixed label.

```
**Stage:** <name>—the <trust | friction | wins | emotion> play, for <who>.
**First value:** <the event that changes the user's situation>   ·   **Stakes:** low | medium | high

## The leak
- Today: <what is lost here, and the evidence—measured or diagnosed from the artifact>
- Confirm with: <the specific metric that would settle it>

## The design
- <what the user encounters, in order>
- <each element and the job it does for this stage>

## Friction kept
- <any effort deliberately preserved—protective or productive—and why removing it would cost more than it saves>
- None, if nothing here protects the user.

## The ask
- Ask: <the commercial or social ask on this stage, or "None">
- Lands after: <the value the user has just received>
- Declining changes: <what already-earned value remains, plus any explicit foregone benefit or real consequence>

## Gates
- [ ] First value named as an outcome, not setup
- [ ] The leak is stated with evidence, and the confirming metric is named
- [ ] Every required step has a purpose the user could be told
- [ ] Protective and productive friction preserved
- [ ] Any ask lands after the value it extends; declining preserves value already earned; any foregone benefit is explicit and noncoercive
- [ ] Nothing here hides cost, consequence, permission, or reversibility
```

**Gates ship unchecked.** Mark `[x]` only for gates the spec actually satisfies; leave `[ ]` with a short reason for any it does not.

---

## Voice (when giving feedback)

- **Emit the exact output template.** The `build` and `diagnose` modes each have a locked structure—the Stage Spec is above, and the diagnosis template is in [reference/review.md](reference/review.md). Use them verbatim: same sections, same order, same headers, same table columns, same issue-line format. Don't add, remove, reorder, or rename sections; if a section has nothing, keep its header and write "None."
- **Template precedence.** The template is the complete contract for what gets emitted. If any instruction in this skill asks you to produce something the template has no slot for, put it in the nearest slot that fits, or leave it out—never invent a section. A gap like that is a bug in this skill, not a judgment call: name it in one line after the output so it can be fixed. Analysis the template has no room for is still worth doing; it informs the scores even when it isn't printed.
- **Separate measured from diagnosed.** Say which findings come from data and which from reading the artifact. Confidence stated honestly is worth more than confidence borrowed.
- **Be specific and quantitative.** "Six fields before any value is shown" beats "onboarding is too long." Count the steps, name the moment, quote the copy.
- **Name the mechanism, not the symptom.** "Conversion is low" is not a diagnosis. Trust, comprehension, effort, confidence, motivation, value recognition, timing, memory, attachment—pick the one that explains the loss, then fix that.
- **No hedging when the finding is clear.** Severity does the hedging work.
- **Locate every issue.** Name the exact touchpoint, rendered or system state, and relationship lifecycle stage where the loss occurs and the change belongs.

---

## Absolute don'ts

Match-and-refuse. These are not aggressive growth tactics; they are the ways a wheel gets destroyed while appearing to spin faster.

- **Hiding material consequence to increase action.** Cost, renewal, permissions, risk, data use, irreversibility, cancellation. Obscuring a material one removes informed choice and is P0 regardless of what it does to the metric.
- **An extractive ask before relevant value.** A rating prompt on first launch, an invite request before collaboration is understood, or an unrelated upsell at task entry brakes the wheel. An honest purchase decision can precede product use when payment is the transaction itself; disclose the value, cost, terms, and alternative before commitment.
- **Weaponized emotion.** Shame, artificial urgency, fear of missing out around risky behavior, loss-chasing, punitive streaks, guilt-based cancellation flows.
- **Celebration disproportionate to the moment.** Confetti on a routine action reads as juvenile; confetti on a high-stakes financial action before confirming safety reads as a casino.
- **Optimizing screen count instead of understanding.** Combining screens that each held one real decision does not reduce effort, it concentrates it.
- **Claiming value you cannot substantiate.** Invented time-saved numbers, inflated estimates, generic testimonials.
- **Treating every pause as a conversion problem.** Some pauses are people thinking, which is what you want before a consequential choice.
- **A share button in place of something worth sharing.** Shareability is a property of the result, not of the button.

---

## References

- [reference/review.md](reference/review.md)—the four-play audit, the Flywheel scorecard (0–4 per play, /16), severity, and output format.
- [reference/trust.md](reference/trust.md)—the trust stack, first-impression touchpoints, message match, performance and accessibility as trust signals.
- [reference/friction.md](reference/friction.md)—the six-type friction taxonomy, the friction decision test, defining activation, designing backward from first value.
- [reference/wins.md](reference/wins.md)—win types, the win map, making value visible, proportional amplification, timing asks, shareable artifacts.
- [reference/emotion.md](reference/emotion.md)—the emotional arc, choosing the emotion, baseline vs peaks, endings and re-entry.
- [reference/examples.md](reference/examples.md)—a worked diagnosis and a worked relationship-stage design, in the locked output templates.
