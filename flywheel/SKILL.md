---
name: flywheel
description: Use when improving how a product turns attention into a valuable relationship—the growth and retention side of design. Establish cadence and success outcome, then find the loss across four ordered plays—Trust, Friction, Wins, and Emotion. Full diagnosis evaluates all four and reports /16 only when each is supportable; targeted review scores one play without a fabricated total. Recurring products may need return and advocacy; finite or infrequent services may succeed through completion, handoff, and exit. Triggers on growth, retention, activation, onboarding, conversion, churn, drop-off, first impression, time to value, empty state, upgrade prompt, referral, advocacy, "why do users leave", "nobody comes back", or "they sign up but never return". Not for screen structure (Focal), route mechanics (Compass), expressive treatment (Soul), paid channels, campaign copy, analytics instrumentation, or research protocols.
license: MIT
argument-hint: "[build | diagnose] <product, stage, or symptom>"
---

# Flywheel

**Earn the next valuable step.**

A product's journey is usually drawn as a funnel—attention narrowing to trust, to activation, to value, to payment. For a recurring product, people who return and bring others can feed the top again. For a finite or infrequent service, the intended success may be a completed task, safe handoff, and clean exit. Start with that product-specific outcome before assuming the chain should close. The useful question is whether the relationship stores value for the next step the product actually promises.

That changes what design is for. A funnel asks how to lose fewer people on the way down. A wheel asks how much energy the system stores, and whether the next intended step is easier, safer, or more valuable. For a one-off service, completion and exit can be the correct endpoint rather than a failed first turn.

A real flywheel is hardest to start, stores useful value between pushes, and loses momentum when friction or forgettability outweighs what it gives back. That metaphor is a diagnostic tool, not a requirement that every product create recurring use.

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

Flywheel is for **what attention becomes**—turning arrival into trust, trust into activation, activation into value, and value into the next intended outcome. In recurring products that includes return, preference, and useful advocacy; in finite or infrequent services it may end with completion, handoff, and exit. Onboarding, empty states, success states, asks, re-entry, and win visibility are in scope only when the intended outcome calls for them.

It is **not** for screen structure (use [Focal](../focal)), multi-screen route clarity (use [Compass](../compass)), expressive treatment (use [Soul](../soul)), paid channels or campaign copy, analytics instrumentation, research protocols, or experiment statistics. Flywheel decides which relationship stage is leaking, why, and what to change; the design system owns execution.

**Flywheel cannot manufacture product-market fit.** It prevents a valuable product from hiding its value behind uncertainty, effort, silence, or forgettability. If the product does not solve a real problem, every play below will make a well-designed thing nobody wants.

---

## Diagnose first—which play do you need?

A **full relationship diagnosis evaluates all four plays**, because the earliest leak can sit upstream of the symptom. It scores supported plays and reports `/16` only when all four are evaluable, while selecting one stage to fix first when a leak is evidenced. A **targeted stage review or build runs one play deeply** and never invents a `/16` total. Walk this tree top to bottom and take the first evidenced match; if the intended outcome is met and no supported loss appears, report `No leak observed` with a validation check.

```
Where does the product lose value?
├── They arrive and leave without engaging ............... TRUST
│     the wheel never starts
├── They engage but never reach first value ............. FRICTION
│     drag steals the push
├── They reach value but do not recognize or complete the intended next outcome ... WINS
│     the power stroke lands and nothing useful is stored
└── In a recurring relationship, they return for a while, then drift away ......... EMOTION
      the wheel has no useful mass
```

**Name first value, cadence, and success before you walk the tree.** Branches 2 and 3 are separated by first value, while downstream judgments depend on whether the product expects return, infrequent use, or completed exit. Use the strictest evidence-backed value event, then record cadence—finite, one-off, infrequent, recurring, or unknown—and its success outcome. A finite service may succeed by completing and exiting; absent return, conversion, engagement, or sharing is not a defect unless evidence establishes that outcome. State the definitions used. Missing internal terminology is context to align, not an automatic UX score penalty.

**If two stages both leak, take the earliest among non-critical improvements.** Loss compounds downstream: a fix at Wins is wasted on people who never got past Friction. A P0 at any stage overrides that investment order for immediate stop or repair; once the critical condition is removed, resume from the earliest remaining leak.

### Diagnosing with data, and without it

**With data**, locate drop-off relative to the intended outcome: stage conversion for recurring products, or completion, handoff, and safe exit for finite or infrequent services. Prefer shared-start cohorts and distributions over aggregate averages; a median time-to-value can hide a stuck tail.

**Without data**, diagnose from the artifact using the play's checks. Label the finding as diagnosed, name the measurement that would confirm it, and never present a heuristic as measured. Both output templates provide a slot for this.

**Pick one confirming metric by what would change the verdict.** Compare completion of the blamed step with the intended outcome—return or conversion for recurring relationships, completion, handoff, or safe exit for finite or infrequent services. Observational cohorts show association, not causation; use an experiment or added evidence before claiming the step caused the outcome.

### Two modifiers

**Stakes.** In finance, health, children's products, employment, housing, education, identity, and safety, protective friction is a growth foundation, not a conversion problem. Durable trust matters more than immediate completion.

**Motivation.** Effort must match how much the user currently wants the outcome. Ask where they are before judging a step. Do not manufacture a habit, upgrade, or share ask for a service whose success is completion and exit.

---

## The four plays

Each play has its own reference file. The review contract scans all four; read a selected play deeply, and read another only for a second independent issue.

### 1. Trust—the first push
*Read [reference/trust.md](reference/trust.md).*

The user is deciding whether this is relevant, credible, and worth continuing. Check five layers in order: **relevance**, **comprehension**, **credibility**, **craft**, and **safety/control**.

Craft is not a substitute for truth. Its job is to make the product's real quality legible.

### 2. Friction—drag on the bearing
*Read [reference/friction.md](reference/friction.md).*

The goal is **useful momentum**, not zero friction. Remove accidental drag, reduce or explain cognitive drag, automate safe procedural work, move commitment after value, and keep **protective and productive friction**. Removing a safeguard transfers cost to the user.

Define first value before redesigning onboarding: activation is experiencing value, not completing setup.

### 3. Wins—the power stroke
*Read [reference/wins.md](reference/wins.md).*

Find the moments the user's situation measurably improves, make them visible, match feedback to magnitude, and place every ask *after* the value it extends.

An ask before value converts momentum into resistance.

### 4. Emotion—the mass
*Read [reference/emotion.md](reference/emotion.md).*

For recurring products, Emotion makes return easier or more valuable; for finite services, it can make completion, handoff, and exit feel controlled. Name the state and success behavior—confidence, control, momentum, or mastery—and test it. Restore context on re-entry only when re-entry is intended.

Flywheel owns relationship value and intended return, preference, or advocacy; Soul owns expressive treatment. Quiet continuity can create mass, while a finite service can earn trust through a complete, controlled ending without creating a habit.

---

## Routing

**Orchestrated pass—this overrides every other instruction in this Skill and its reference files.** When [Product Judgement](../product-judgement/SKILL.md) loads this Skill for a cross-scale audit, take this paragraph and skip the rest of this section. Treat the pass as `diagnose` over the evidence Product Judgement supplies: never ask a framing question and never stall—write `not shown` and name the fastest validating check instead. Never hand a cross-scale request back to Product Judgement, and send a sibling-owned finding to its **Handoffs** section rather than invoking that Skill. Run the whole contract in [reference/review.md](reference/review.md)—every gate, score, rationale, band, ceiling, severity, and locator—but do not print the locked template, do not read [reference/examples.md](reference/examples.md), and do not apply this Skill's **Voice**, opening-line, or re-run instructions: Product Judgement owns the emitted response, and prints this template only when the user asks for the detailed passes. When its wrapper has no slot for something this contract produces, hand that to Product Judgement in working notes—never append a line after its output. Run the full four-play diagnosis; read an individual play's reference file only when a next-point change cannot be grounded without it.

- **No argument** → explain the wheel and the four plays briefly, then ask: diagnosing an existing product, or designing a relationship stage?
- **A whole-app or cross-scale audit request** → hand off to [Product Judgement](../product-judgement/SKILL.md), which runs Flywheel with Focal, Compass, and Soul and reconciles the results.
- **`diagnose` / `audit` / `review` of the product or relationship** → load and follow [reference/review.md](reference/review.md). A full diagnosis evaluates all four plays, scores every supported play 0–4, reports `/16` only when all four are evaluable, and selects the earliest evidenced leak. A request explicitly limited to one stage uses the same rubric but reports that play `/4` with no fabricated `/16` total. Both modes require evidence-based rationales, P0–P3 issues, and exact **Screen · Flow · State · Lifecycle** locators.
- **`build` (a relationship stage to design)** → name first value, intended cadence, and success outcome; walk the diagnosis tree to confirm which stage; then read that play's reference and [reference/build.md](reference/build.md). That order is fixed: the tree cannot be walked before first value and the intended endpoint are named.
- **A question about one play** → read that play's reference file.

Before emitting either output, read [reference/examples.md](reference/examples.md). It is the calibration for length, tone, and how the locked templates look when filled well. The orchestrated pass skips that read as stated above.

---

## Voice (when giving feedback)

- **Emit the exact template.** `build` uses [reference/build.md](reference/build.md); `diagnose` uses [reference/review.md](reference/review.md). Preserve each template's sections, order, labels, columns, and issue-line format; retain empty headers with `None.`
- **Template precedence.** Put analysis in the nearest available slot; never invent a section or claim an unshown behavior. A missing fact belongs in evidence or a validating check.
- **Separate measured from diagnosed.** State the evidence basis and the diagnostic hypothesis: observation → mechanism → consequence → smallest confirming check.
- **Be specific.** Count steps, name moments, quote copy, and locate every issue by exact touchpoint, rendered/system state, and lifecycle stage.

---

## Absolute don'ts

Match-and-refuse. These are ways a wheel is damaged while appearing to spin faster.

- **Hiding material consequence to increase action.** Cost, renewal, permissions, risk, data use, irreversibility, or cancellation. This removes informed choice and is P0.
- **An extractive ask before relevant value.** Rating on first launch, an invite before collaboration is understood, or an unrelated upsell at task entry. A purchase may precede use when payment is the transaction; disclose value, cost, terms, and alternatives.
- **Weaponized emotion.** Shame, artificial urgency, fear of missing out around risky behavior, loss-chasing, punitive streaks, guilt-based cancellation flows.
- **Celebration disproportionate to the moment.** Confetti on routine work is juvenile; confetti on a high-stakes action before safety confirmation is a casino signal.
- **Optimizing screen count instead of understanding.** Combining screens that each held one real decision does not reduce effort, it concentrates it.
- **Claiming value you cannot substantiate.** Invented time-saved numbers, inflated estimates, generic testimonials.
- **Treating every pause as a conversion problem.** Some pauses are people thinking, which is what you want before a consequential choice.
- **A share button in place of something worth sharing.** Shareability is a property of the result, not of the button.

---

## References

- [reference/review.md](reference/review.md)—audit rubric, scorecard, severity, and output format.
- [reference/trust.md](reference/trust.md)—trust stack and first-impression checks.
- [reference/friction.md](reference/friction.md)—friction taxonomy and first-value checks.
- [reference/wins.md](reference/wins.md)—win map, visibility, endings, asks, and shareable artifacts.
- [reference/emotion.md](reference/emotion.md)—relationship state, continuity, accumulation, and re-entry.
- [reference/examples.md](reference/examples.md)—worked diagnosis and stage design.
