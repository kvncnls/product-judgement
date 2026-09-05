---
name: soul
description: Use when a product works but feels generic, forgettable, or indistinguishable from its competitors. Soul maps the happy path and sorts every beat into three tiers—Expected (stays functional), Elevated (the same moment with more craft), and Net-New (an entirely new experience, reserved for up to three justified moments; zero is valid). Places by contextual reach, utility, stakes, frequency, cost, and evidence about memory; tests repeated treatments for feedback, control, perceivability, and comprehension; and refuses traditional dumping grounds (404 pages, easter eggs, error mascots) where expression goes unseen. Triggers on boring, bland, generic, soulless, forgettable, delight, personality, charm, whimsy, juice, microinteractions, wow moment, celebration, empty state, success state, first impression, "make it memorable", "feels generic". Not for screen structure (use Focal), flows and navigation (use Compass), retention and activation leaks (use Flywheel), brand identity systems, or marketing pages.
license: MIT
argument-hint: "[build | search] <product, flow, or moment>"
---

# Soul

**Never boring.**

Most products work and feel like nothing. Every screen is functional, every flow passable, yet nothing feels authored. Soul treats that flatness as a placement problem.

**Soul is not a spec—it is what accumulates when specific moments are placed well.** It maps the default path and sorts every beat into one of three tiers: functional, crafted, or a zero-to-three full rebuild.

Three contextual hypotheses guide every placement:

- **Memory is a hypothesis, not a law.** Peaks and endings can shape recall when users reach them, the moment carries meaning, and recall or user evidence supports the effect. Compare reach, utility, stakes, frequency, implementation and maintenance cost, and any actual recall evidence; a later beat is not automatically stronger.
- **Reach and consequence matter more than cheap risk.** Delight traditionally goes where failing is cheap—the 404 page, the easter egg—which is exactly where nobody walks. Use `reach × likely memory` as a working comparison, then test it against the user's job, the cost of getting it wrong, and the cost to build and maintain it.
- **Repetition changes the bar.** A treatment that plays every session must remain perceivable, comprehensible, and under the user's control when repeated. A one-time treatment may spend more, but neither frequency nor novelty alone proves that it will endure.

**The three tiers.** Every beat on the path gets exactly one:

| Tier | What it is | Where it goes | The test |
|---|---|---|---|
| **Expected** | the obvious version, fully functional | beats that must simply work | nothing missing, nothing added |
| **Elevated** | the same moment, executed with more craft | the small things, spread wide—this is how a product stops being boring | nothing new is introduced |
| **Net-New** | an entirely new experience in place of the old one | up to three justified moments; zero is valid | it could not be mistaken for a competitor, or for the moment it replaced |

---

## When to use

Soul is for a working product that reads as anonymous: a flat happy path, a success state that stops instead of lands, or an ending nobody designed. Give it a product, flow, screens, code, or description.

It is **not** for:
- Single-screen structure, hierarchy, or clutter—that is [Focal](../focal).
- Multi-screen paths and navigation—that is [Compass](../compass).
- Losing users before value—that is [Flywheel](../flywheel). Soul makes a sound path memorable; it cannot repair a broken one.
- Brand identity systems, logo, illustration style, or marketing pages. Soul places moments inside the product's default path; it does not define the visual language they are executed in.

---

## Map the path first

Every job starts with the happy path: the default flow the primary user walks, entry to outcome. Build it from the artifact; where it is silent, ask.

```
1. Enters from [source]
2. Sees [first surface or message]
3. Understands [core value or next step]
4. Takes [primary action]
5. System responds with [result]
6. Reaches [successful outcome]
7. Feels [intended emotional state]
```

- **Keep the default path compact.** Expand the skeleton only when a beat changes understanding, action, system response, or feeling. Five to twelve beats is a diagnostic range, not a quota. Exclude edge branches and do not merge consequential beats to hit a number.
- **Tag every beat** with its touchpoint (screen, email, notification, external), frequency, and stakes: `once` (first-run only), `recurring` (weekly-to-monthly rhythm), `every-run` (every session); stakes are `low`, `medium`, or `high`. If frequency or stakes are not evidenced, write `not shown` and name the check.
- **Beat 7 is a design input.** If nobody can name the intended ending feeling, that absence is the first finding.
- First-run empty states and waits are in scope. Error branches are excluded from Net-New selection, but belong in the restraint check: failure must stay clear and respectful without becoming a delight destination.

## Sort every beat

The tiers have owners:

- **Expected** owns load-bearing convention, high stakes, and any beat where addition taxes the task. It is a verdict, not a failure; record the restraint.
- **Elevated** owns the small things: the same moment with clearer language, feedback, anticipation, or feel. Distribute it where the ceiling allows.
- **Net-New** owns up to three exceptional moments, and zero is valid. It replaces the old experience and earns its place only after the contextual comparison below; it is a budget, never a quota.

Walk this for every beat, top to bottom, first match wins:

```
Which tier may this beat take?
├── Off the default path ................. none—dumping ground; relocate the budget
├── The floor fails here ................. none yet—hand off first (leak → Flywheel,
│                                          screen → Focal, maze → Compass)
├── Load-bearing convention .............. Expected—muscle memory is the feature
├── High stakes .......................... Expected or calm Elevated by default; Net-New
│                                          only when it strengthens reassurance or control
├── Every-run ............................ Elevated by default; Net-New only when later-use
│                                          utility is supported or explicitly tested
└── Otherwise ............................ Elevated; promote to Net-New only if it clears
                                           the selection bar and ranks within the top three
```

**Frequency sets each beat's ceiling:**

- `every-run` beats take treatment that evidence shows can remain useful, perceivable, comprehensible, and controllable under repetition—speed, feel, anticipation, useful variation, or an exceptional Net-New capability. Jokes, celebration, and surprise often decay; test the actual beat instead of assuming either decay or durability.
- `once` beats may take one-shot expressive treatment.
- `recurring` beats sit between: intensity below first-run, with variation tested against later arrivals.

**Refuse dumping grounds.** 404 pages, error mascots, easter eggs, and release-note bits are often low-reach places to spend expression. Relocate existing craft to an on-path beat; route frequent error exposure to [Flywheel](../flywheel) or [Focal](../focal). A high-traffic 404 is an entry beat: state what happened and provide one clear way back.

Selection heuristics, archetypes, and the full dumping-grounds list live in [reference/moments.md](reference/moments.md).

---

## Routing

**Orchestrated pass—this overrides every other instruction in this Skill and its reference files.** When [Product Judgement](../product-judgement/SKILL.md) loads Soul for a cross-scale audit, treat it as `search` over supplied evidence: never ask a framing question or stall; write `not shown` and name the fastest check. Never hand a cross-scale request back to Product Judgement; put sibling-owned findings in its **Handoffs** section. Run [reference/review.md](reference/review.md)'s full contract—gates, scores, rationales, bands, ceilings, severity, and locators—but do not print its locked template, do not read [reference/examples.md](reference/examples.md), or apply Soul's Voice/opening/re-run instructions. Product Judgement owns the emitted response and any working notes; keep findings even when an earlier pass found a broken floor so its repair sequence can account for Soul.

- **No argument** → explain the placement idea in three sentences, then ask: search an existing product, or build one moment?
- **A whole-app or cross-scale audit request** → hand off to [Product Judgement](../product-judgement/SKILL.md), which runs Soul after Focal, Compass, and Flywheel and reconciles the results.
- **`search` / `sweep` / `audit` / `review` / `find` (a product, a flow, screens, or "it feels generic")** → load and follow [reference/review.md](reference/review.md). It first runs an unscored Readiness check, then maps the path, assigns every beat a tier, and evaluates three Soul-local gates 0–4—Placement, Proportion, and Signature—with a `/12` total only when all three are evaluable. It requires evidence-based rationales, P0–P3 issues, and exact **Screen · Flow · State · Lifecycle** locators before returning up to three justified Net-New moments plus the small things worth elevating.
- **`build` / `design` / `treat` (one beat)** → run the beat through the sort tree above; its tier is the build's **Target**. Load [reference/build.md](reference/build.md) for the build workflow, applicable state inventory, Moment Spec, and gates. Read [reference/treatments.md](reference/treatments.md)—plus [reference/moments.md](reference/moments.md) when the target is Net-New, to confirm it clears the selection bar.
- **A question about a moment type or a treatment lever** → [reference/moments.md](reference/moments.md) or [reference/treatments.md](reference/treatments.md).

Before emitting standalone output, read [reference/examples.md](reference/examples.md) for calibrated length, tone, and template use. The orchestrated pass skips examples.

---

## Voice (when giving feedback)

- **Emit the exact output template.** Search has the locked structure in [reference/review.md](reference/review.md). One-beat build output follows the template loaded by the build route. Use each template verbatim: same sections, same order, same headers, same table columns. If a section has nothing, keep its header and write "None."
- **Template precedence.** The template is the complete contract for what gets emitted. If any instruction in this skill asks for something the template has no slot for, put it in the nearest slot that fits, or leave it out—never invent a section. A gap like that is a bug in this skill: name it in one line after the output so it can be fixed.
- **Name the feeling, every time.** "Delight," "personality," "magic," and "soul" never appear as specifications. The feeling, the beat, and the second it happens—or it is not a design decision yet.
- **Separate observed from assumed.** Findings read off the artifact and findings inferred from a description carry different weight; the Basis line says which is which.
- **Be specific and quantitative.** "The paid notification says 'Done' and nothing else" beats "the success state is underwhelming." Quote the copy, count the beats, name the second.
- **Locate every issue.** Name the exact beat or touchpoint, rendered app state, and lifecycle occurrence where the treatment—or restraint—belongs.
- **Your output is a spec, not a performance.** Zero wit is the default register; one placed line is the ceiling, and never at anyone's expense.

---

## Absolute don'ts

Match-and-refuse. Each of these is expressiveness spending trust it did not earn.

- **Wit at failure or loss.** The joke at the worst moment reads as mockery. Personality is tested at failure, and it passes the test by restraint.
- **Celebration before confirmation on high-stakes actions.** Confetti before "your money arrived safely" reads as a casino. Reassurance, records, and control come first; feeling comes after.
- **Motion or speed that taxes the task.** Any animation or response that delays the primary action, hides failure, removes control, or cannot be perceived or understood converts treatment into friction. Respect reduced-motion preferences without exception.
- **Every-run novelty.** A joke on a beat users hit daily may become noise by week two. If the beat is every-run, require evidence that speed, feel, anticipation, or useful variation stays perceivable, comprehensible, and controllable; nothing may depend on surprise alone.
- **The dumping grounds.** Delight placed by low risk instead of reach. If the path is sterile and the 404 has an easter egg, the budget is upside down.
- **Charm covering confusion.** A mascot in front of an unclear flow is a bandage on a structural problem—fix the structure first (Focal or Flywheel), then decide if the moment deserves treatment.
- **Breaking load-bearing convention.** Checkout, save, undo, back—muscle-memory beats rely on the Expected. Novelty there costs comprehension and pays back nothing.
- **"Make it delightful" as a requirement.** Refuse the adjective; extract the moment. Which beat, for whom, feeling what? Then work.
- **Manufactured intimacy.** Personalization the relationship has not earned—first-name warmth from a product used twice, references to sensitive data, false friendship.
- **Decorating a broken path.** If users cannot reliably reach the outcome, hand off before treating anything—a leak is Flywheel's, a screen is Focal's, a maze is Compass's.

---

## References

- [reference/review.md](reference/review.md)—the search mode: unscored Readiness plus the three-gate audit (Placement, Proportion, Signature), 0–4 rubrics, `/12` bands, severity, and the locked Moment Map template.
- [reference/moments.md](reference/moments.md)—moment archetypes, frequency classes, selection heuristics, the up-to-three budget, and the dumping grounds.
- [reference/treatments.md](reference/treatments.md)—the three tiers in depth, the rungs a build lays out, the craft levers, repetition-proof design, and proportionality.
- [reference/examples.md](reference/examples.md)—a worked search and a worked build, in the locked templates.
