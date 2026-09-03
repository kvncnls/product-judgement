---
name: soul
description: Use when a product works but feels generic, forgettable, or indistinguishable from its competitors. Soul maps the happy path and sorts every beat into three tiers—Expected (stays functional), Elevated (the same moment with more craft), and Net-New (an entirely new experience, reserved for up to three justified moments; zero is valid). Places by reach and memory, splits treatments by frequency so repetition never turns expression into noise, and refuses the traditional dumping grounds (404 pages, easter eggs, error mascots) where delight goes to be unseen. Triggers on boring, bland, generic, soulless, forgettable, delight, personality, charm, whimsy, juice, microinteractions, wow moment, celebration, empty state, success state, first impression, "make it memorable", "feels generic". Not for screen structure (use Focal), flows and navigation (use Compass), retention and activation leaks (use Flywheel), brand identity systems, or marketing pages.
license: MIT
argument-hint: "[build | search] <product, flow, or moment>"
---

# Soul

**Never boring.**

Most products work and feel like nothing. Every screen functional, every flow passable, nothing anyone would describe to a friend. The word people reach for is *soulless*, and the word is a diagnosis: nothing here was authored. The product is the average of its competitors.

**Soul is not a spec—it is what accumulates when specific moments are placed well.** So this skill does not sprinkle. It maps the default path and sorts every beat into one of three tiers—what stays functional, what gets more craft, and which zero-to-three moments, if any, earn a full rebuild.

Three facts decide every placement:

- **People remember the peak and the ending, not the average.** A product with two entirely new moments and quiet craft on everything else is remembered. A product with twelve novelties is exhausting, and nothing in it reads as significant.
- **Reach beats risk.** Delight traditionally goes where failing is cheap—the 404 page, the easter egg—which is exactly where nobody walks. Placement here is chosen by reach × memory: the default path, because that is where everyone is.
- **Repetition kills novelty.** The 50th confetti is noise. A treatment that plays every session must survive its 50th viewing; a treatment that plays once may spend everything.

**The three tiers.** Every beat on the path gets exactly one:

| Tier | What it is | Where it goes | The test |
|---|---|---|---|
| **Expected** | the obvious version, fully functional | beats that must simply work | nothing missing, nothing added |
| **Elevated** | the same moment, executed with more craft | the small things, spread wide—this is how a product stops being boring | nothing new is introduced |
| **Net-New** | an entirely new experience in place of the old one | up to three justified moments; zero is valid | it could not be mistaken for a competitor, or for the moment it replaced |

---

## When to use

Soul is for a product that already works but reads as anonymous: a functional-but-flat happy path, a success state that stops instead of lands, an ending nobody designed, a personality budget with nowhere to go. Give it a product, a flow, screens, code, or a description.

It is **not** for:
- Single-screen structure, hierarchy, or clutter—that is [Focal](../focal).
- Multi-screen paths and navigation—that is [Compass](../compass).
- Losing users before they reach value—that is [Flywheel](../flywheel). Soul makes a working path memorable; it cannot make a broken path work, and treatments on a broken path read as cosmetic.
- Brand identity systems, logo, illustration style, or marketing pages. Soul places moments inside the product's default path; it does not define the visual language they are executed in.

---

## Map the path first

Every job starts with the happy path: the default flow the primary user actually walks, entry to outcome. Build it from the artifact; where the artifact is silent, ask—the skeleton below is the interview, seven blanks to fill.

```
1. Enters from [source]
2. Sees [first surface or message]
3. Understands [core value or next step]
4. Takes [primary action]
5. System responds with [result]
6. Reaches [successful outcome]
7. Feels [intended emotional state]
```

- **Keep the default path compact.** Expand the seven-part skeleton only when a distinct beat changes the user's understanding, action, system response, or feeling. Five to twelve beats covers many products, but it is a diagnostic range, not a quota or hard ceiling. Exclude edge branches; do not merge consequential beats merely to hit a number.
- **Tag every beat** with its touchpoint (screen, email, notification, external) and its frequency: `once` (first-run only), `recurring` (weekly-to-monthly rhythm), `every-run` (every session).
- **Beat 7 is a design input, not decoration.** If nobody can say what the user is meant to feel at the end, that absence is the first finding.
- First-run empty states and waits are beats on this path—they are in scope. Error branches are excluded from Net-New selection because they are not the happy path, but include them in the restraint check: personality must remain clear and respectful during failure without turning failure into a delight destination.

## Sort every beat

The tiers have owners:

- **Expected** owns the beats that must simply work—load-bearing convention, high stakes, anywhere addition would tax the task. **Expected is a verdict, not a failure**, and the receipt of Expected beats is half the deliverable.
- **Elevated** owns the small things, and it spreads as wide as the ceilings allow. This is the anti-boring tier: the same moments with more craft—copy in the user's words, feedback that names what changed, response that feels instant. Craft survives repetition; novelty does not, which is why Elevated can be distributed and Net-New cannot.
- **Net-New** owns **up to three** exceptional moments, and zero is a valid result. It is not the old moment done better but an entirely new experience in its place. Concentration protects significance, while the eligibility tree protects restraint: use Net-New only when a beat clears reach × memory, frequency, stakes, and convention. Two or three is common when the path genuinely earns them; it is a budget, never a quota.

Walk this for every beat, top to bottom, first match wins:

```
Which tier may this beat take?
├── Off the default path ................. none—dumping ground; relocate the budget
├── The floor fails here ................. none yet—hand off first (leak → Flywheel,
│                                          screen → Focal, maze → Compass)
├── Load-bearing convention .............. Expected—muscle memory is the feature
├── High stakes .......................... Expected or calm Elevated by default; Net-New
│                                          only when it strengthens reassurance or control
├── Every-run ............................ Elevated by default; Net-New only when durable
│                                          utility—not surprise—still pays on the 50th run
└── Otherwise ............................ Elevated; promote to Net-New only if it clears
                                           the selection bar and ranks within the top three
```

**The frequency split sets each beat's ceiling:**

- `every-run` beats take only repetition-proof treatment—speed, feel, anticipation, useful variation, or an exceptional Net-New capability whose utility survives the 50th run. Jokes, celebration, and novelty decay with repetition; usefulness does not.
- `once` beats may take one-shot expressive treatment—this is where storytelling spends well.
- `recurring` beats sit between: intensity below first-run, variation so the 30th arrival still reads as alive.

**The dumping grounds are refused.** 404 pages, error mascots, easter eggs, release-note bits—the traditional homes of product delight, chosen because failing there is cheap. Cheap failure means no reach: the work is unseen, or seen by a frustrated user at the worst moment. When the sweep finds existing delight in a dumping ground, it relocates the effort to a chosen beat. And an error state frequent enough to be worth delighting is a bug to fix, not a moment to elevate—route it to [Flywheel](../flywheel) or [Focal](../focal). One honest edge: a 404 that carries real traffic is not a dumping ground, it is an entry beat—treat it as recovery, one clear path back, no jokes.

Selection heuristics, archetypes, and the full dumping-grounds list live in [reference/moments.md](reference/moments.md).

---

## Routing

**Orchestrated pass—this overrides every other instruction in this Skill and its reference files.** When [Product Judgement](../product-judgement/SKILL.md) loads this Skill for a cross-scale audit, take this paragraph and skip the rest of this section. Treat the pass as `search` over the evidence Product Judgement supplies: never ask a framing question and never stall—write `not shown` and name the fastest validating check instead. Never hand a cross-scale request back to Product Judgement, and send a sibling-owned finding to its **Handoffs** section rather than invoking that Skill. Run the whole contract in [reference/review.md](reference/review.md)—every gate, score, rationale, band, ceiling, severity, and locator—but do not print the locked template, do not read [reference/examples.md](reference/examples.md), and do not apply this Skill's **Voice**, opening-line, or re-run instructions: Product Judgement owns the emitted response, and prints this template only when the user asks for the detailed passes. When its wrapper has no slot for something this contract produces, hand that to Product Judgement in working notes—never append a line after its output. Record the findings even when an earlier pass found a broken floor: Product Judgement sequences the repair ahead of the treatment, and an empty Soul contribution leaves a required row unfillable.

- **No argument** → explain the placement idea in three sentences, then ask: search an existing product, or build one moment?
- **A whole-app or cross-scale audit request** → hand off to [Product Judgement](../product-judgement/SKILL.md), which runs Soul after Focal, Compass, and Flywheel and reconciles the results.
- **`search` / `sweep` / `audit` / `review` / `find` (a product, a flow, screens, or "it feels generic")** → load and follow [reference/review.md](reference/review.md). It first runs an unscored Readiness check, then maps the path, assigns every beat a tier, and evaluates three Soul-local gates 0–4—Placement, Proportion, and Signature—with a `/12` total only when all three are evaluable. It requires evidence-based rationales, P0–P3 issues, and exact **Screen · Flow · State · Lifecycle** locators before returning up to three justified Net-New moments plus the small things worth elevating.
- **`build` / `design` / `treat` (one beat)** → run the beat through the sort tree above; its tier is the build's **Target**. Read [reference/treatments.md](reference/treatments.md)—plus [reference/moments.md](reference/moments.md) when the target is Net-New, to confirm it clears the selection bar—then follow **Build** below.
- **A question about a moment type or a treatment lever** → [reference/moments.md](reference/moments.md) or [reference/treatments.md](reference/treatments.md).

Before emitting either output, read [reference/examples.md](reference/examples.md). It calibrates length, tone, and what the locked templates look like filled well.

---

## Build: the five moves

1. **Frame it.** The product, the user, the beat, its frequency class, the stakes, and the one feeling this moment should produce—named, not "delight." If you cannot name the feeling, the screen, and the second it happens, you have a brand adjective, not a design target. Stakes are what the user can lose at this beat—money, work, standing, safety. Anything real to lose is high, and high puts reassurance before feeling.
2. **Place it.** Run the beat through the sort tree—Expected, Elevated, or Net-New is the spec's **Target**. A Net-New target must also clear the selection bar in [reference/moments.md](reference/moments.md); an Elevated target respects its ceiling; an Expected target records why convention, frequency, stakes, or an already-sufficient treatment makes restraint correct. If the request points at a dumping ground, say so and redirect the budget to the nearest on-path beat.
3. **Ladder it.** Design Expected as a real shippable floor. Add Elevated and Net-New only through the target; every rung above the target is `unavailable at this beat's ceiling` with the reason. This makes an Expected target a complete answer rather than a forced prelude to extra treatment.
4. **Guard it.** No rung may tax speed, comprehension, or the primary action. High-stakes moments get reassurance before feeling. Every-run moments get only what survives repetition.
5. **Run the gates.** Self-check against the **`## Gates`** block of the Moment Spec below—that block is the canonical list. Mark `[x]` only what the spec satisfies; leave `[ ]` with a one-line reason for any it does not.

**Output—the Moment Spec (use this exact structure).** Every build returns this template verbatim, in this order. Fill the `<…>` slots; keep every fixed label.

```
**Moment:** <the beat>—for <who>, on <the first pass | every pass | the nth pass>.
**Feeling:** <one named emotion> · **Frequency:** <once | recurring | every-run> · **Stakes:** <low | medium | high> · **Target:** <Expected | Elevated | Net-New>

## Why this moment
- On the path: <where it sits, and who reaches it>
- Budget decision: <why this beat earns treatment—or why Expected restraint is correct>
- Today: <what the moment does now—observed from the artifact, or assumed>

## The rungs
- **Expected:** <the floor—the obvious version, fully functional, shippable as-is>
- **Elevated:** <the same moment with more craft, or `unavailable at this beat's ceiling` with the reason>
- **Net-New:** <an entirely new experience in place of the old one, or `unavailable at this beat's ceiling` with the reason>

## Held constant
- <what no rung may damage—speed, comprehension, the primary action, reversibility>
- <the convention kept, if this beat is muscle-memory>

## Constraints for the pick
- <brand, technical, accessibility, and context limits every rung already respects>

## Gates
- [ ] On the default path—reached without hunting
- [ ] One feeling, named—"soul" and "delight" appear nowhere as specs
- [ ] Survives its frequency—repetition-proof if every-run
- [ ] Proportionate to the moment's magnitude
- [ ] Speed, comprehension, and the primary action untouched
- [ ] Honest without motion and without sound
```

**The pick between rungs is the caller's.** The target names the tier the sort assigned; rungs below it are interim ships, and landing on one is a product decision that belongs to the human. Recommend only when asked.

---

## Voice (when giving feedback)

- **Emit the exact output template.** Search and build each have a locked structure—the build template is above, the search template is in [reference/review.md](reference/review.md). Use it verbatim: same sections, same order, same headers, same table columns. If a section has nothing, keep its header and write "None."
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
- **Motion that taxes the task.** Any animation that delays the primary action or comprehension converts delight into friction. Respect reduced-motion preferences without exception.
- **Every-run novelty.** A joke on a beat users hit daily is noise by week two. If the beat is every-run, the treatment is speed, feel, or anticipation—nothing that depends on surprise.
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
