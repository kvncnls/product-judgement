# Soul Search—the readiness check and three-gate happy-path sweep

Map the working happy path, decide where expressive treatment belongs, and return a restrained set of opportunities. Use when the user asks to search, sweep, audit, review, or find the soul in a product that feels generic, forgettable, over-decorated, or inconsistently authored.

## Input modes

- **A product or flow description**—reconstruct the default path and label every assumed beat. Walked evidence is valid when it is named as such; borrowed confidence is not.
- **Screens, Figma/Paper frames, or a prototype**—read the visible beats and their order. Include first-use, repeat-use, success, failure, interruption, and re-entry states when available. A frame does not prove timing, persistence, or repetition.
- **A live product or codebase**—walk the default path, trigger the real success state, repeat frequent beats, inspect reduced-motion behavior, and test failure for restraint. The codebase can expose lifecycle and frequency behavior that static frames cannot.

## Step 0—Map the path and check readiness

Build the happy path with the seven-part skeleton in [SKILL.md](../SKILL.md), then expand only where a beat changes understanding, action, system response, or feeling. Tag each beat with its touchpoint, frequency, and stakes; if one is not evidenced, write `not shown` and name the check. State the intended ending feeling; `unnamed` is a finding, not permission to invent brand personality.

Then run Readiness before choosing treatment:

- **Ready**—the primary user can reach the outcome with enough clarity, stability, trust, and control that expressive work will not cover a defect.
- **Deferred**—a screen, path, or relationship failure materially prevents the outcome or makes treatment cosmetic. Name the owner: Focal for the screen, Compass for the path, Flywheel for the relationship stage.
- **N/E—insufficient evidence**—the available artifact cannot establish whether that working floor holds. Name the next check; this is neither an observed failure nor a blocker. Continue recording supported treatment findings, with investment conditional on that check.

Readiness is deliberately **unscored**. The other Skills already score structural and lifecycle quality; scoring it again would double-penalize the same failure. A Deferred result still records observed treatment problems and future candidates, but **Next** starts with the handoff. Any gate that the available evidence cannot support is `N/E—insufficient evidence`, whether or not readiness is Deferred; supported gates remain scored. Do not calculate a `/12` total when a required gate is N/E.

Error branches are not Net-New candidates, but they are evidence for restraint. Check whether failure copy, motion, and personality preserve clarity and dignity; do not turn the error itself into a delight opportunity.

## Locate every finding

Before scoring or suggesting a change, build a four-part implementation locator. Every issue, Moment, small thing, Next item, and handoff must carry the same locator:

1. **Screen**—the exact beat, touchpoint, message, or control.
2. **Flow**—the named happy path or transition.
3. **State**—the rendered or system condition: first-use, empty, loading, success, failure, re-entry, and so on.
4. **Lifecycle**—the occurrence: first run, every run, recurring milestone, first value, return, lapse, or recovery.

Use the narrowest defensible locator. `Payment notification · invoice-to-payment · successful settlement · recurring value realization` is actionable; `the ending` is not. If any locator field is not evidenced, write `not shown` and name the fastest validating check in **Coverage** or **Basis**—do not invent behavior.

## The three scored gates

### Gate 1—Placement *(where does expressiveness belong?)*

- List every deliberate expressive touch and every meaningful beat kept Expected.
- Check whether treatment follows the contextual reach × likely memory comparison rather than low implementation risk.
- Check the selection bar, frequency and stakes constraints, and load-bearing conventions before promoting any beat. Treat Elevated as the default ceiling for every-run or high-stakes beats, with Net-New allowed only when evidence-backed utility, reassurance, records, or control justify the exception.
- Treat zero Net-New moments as valid when the restraint receipt explains why no beat earns a rebuild.

| Score | Criteria |
|---|---|
| 0 | Backwards or harmful—expressiveness concentrates in dumping grounds, obstructs the path, or exploits failure while consequential beats are neglected |
| 1 | Unauthored—no deliberate treatment decisions and no evidence that Expected restraint was chosen |
| 2 | Partial—some on-path craft exists, but placement is scattered, inherited, or unsupported by a clear restraint receipt |
| 3 | Deliberate—every meaningful beat has a defensible tier; Elevated craft is distributed where useful; zero to three Net-New moments are chosen only when justified |
| 4 | Exemplary—treatment and restraint are ranked against the strongest available candidates, alternatives were explicitly refused, and each choice is unusually effective for its context |

### Gate 2—Proportion *(does intensity fit frequency, magnitude, and stakes?)*

- Does an every-run beat use repetition-proof craft rather than novelty that decays?
- Does intensity match the size of the moment?
- On high-stakes actions, do reassurance, records, and control precede feeling?
- Does the ending receive enough weight without turning routine completion into ceremony?

| Score | Criteria |
|---|---|
| 0 | Inverted or harmful—celebration precedes safety on a high-stakes action, or heavy novelty repeatedly obstructs a core task |
| 1 | Uniform—one intensity is applied everywhere, so routine and milestone beats carry the same emotional weight |
| 2 | Mostly fit with a material mismatch—one decayed repeat, misplaced ceremony, or underplayed consequential ending |
| 3 | Fit—frequent beats are repetition-proof, rare beats may carry greater expression, and intensity follows magnitude and stakes |
| 4 | Exemplary—variation, pacing, and restraint remain unusually effective across first use, repetition, reduced-motion behavior, and the ending |

### Gate 3—Signature *(is any authorship worth remembering?)*

- Name the product-specific moment, interaction quality, or quiet pattern a user could describe.
- Cover the logo: does the experience retain a coherent point of view without depending on novelty or decoration?
- Check whether authorship survives both success and failure through clarity, restraint, and consistent character.
- Do not require Net-New. A distinctive, repetition-proof Elevated pattern or exceptional quiet baseline can carry signature.

| Score | Criteria |
|---|---|
| 0 | Anti-signature—the memorable thing is an interruption, dark pattern, mockery at failure, or exhausting repeated treatment |
| 1 | Anonymous—no product-specific authorship is visible in the evaluated path |
| 2 | Coherent surface, weak memory—the experience has care or style but nothing yet forms a describable product-specific pattern |
| 3 | Authored—at least one product-specific moment or quiet pattern is useful, coherent, and describable without taxing the task |
| 4 | Exemplary—a coherent authored point of view survives success, failure, repetition, accessibility constraints, and multiple path beats without becoming noise |

## Scoring rules

Every evaluated gate uses the same integer anchors:

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

Score each evaluated gate holistically against its local rubric. Read all checks and evidence, choose the anchor that best describes the gate overall, apply explicit local caps or prerequisites, and let one severe material failure determine the score when the rubric warrants it. Do not use hidden sub-scores, checklist subtraction, averaging, half-points, or a Net-New count as a proxy for quality. A `4` is exemplary for the gate being scored; a restrained `3` can be better product judgment than an over-authored `4` attempt.

- If more than one independent failure sits in a gate, score the *worst* one, then list the others as separate issues.

### Score rationale—required

A score without an explanation is invalid. Fill every scorecard row with the same chain: **evidence → consequence → rubric anchor → next-point change**. State what was observed, inferred, tested, walked, or measured; what it costs the user; why that evidence earns the integer under the local rubric and stops there; and the smallest concrete change that would raise it one point. A `2` must say what works and name the material weakness; a `3` names a supported remaining gap or says `None justified by the evidence` rather than inventing a change to earn `4`; a `4` must explain why the gate is exemplary and say `None—already exemplary` in the next-point field. If the evidence does not expose a state or occurrence, say `not shown` in Coverage/Basis and name the validating check. Score the supported behavior; do not award credit or invent failure for an unknown condition.

<!-- BEGIN SHARED: evidence -->
Use `N/E—insufficient evidence` when the available artifact cannot support a dimension's rubric. A missing variant does not automatically make the whole dimension unevaluable. Report supported findings and the next evidence check; do not convert unknown behavior into a defect, an implementation recommendation, or a score. If any required dimension is N/E, omit the native total, average, band, and weakest-dimension ceiling.

Before assigning `0`, `1`, or `2`, identify the observed condition that meets the negative rubric anchor. “Not shown,” “untested,” and “unknown” cannot supply that condition. If an essential part of the dimension is unsupported, use N/E rather than a lower score as a substitute for uncertainty. Supported strengths can still be described without a number.
<!-- END SHARED: evidence -->

When all three gates are evaluated, keep the native total: `total = Placement + Proportion + Signature`. Calculate `average = total / 3`, display it rounded to one decimal place, and apply this shared algorithm:

| Band | Average rule | Native total |
|---|---:|---:|
| **Broken** | `average <= 1.5` | `0–4 / 12` |
| **Significant rework** | `1.5 < average < 2.5` | `5–7 / 12` |
| **Solid** | `2.5 <= average < 3.5` | `8–10 / 12` |
| **Excellent** | `average >= 3.5` | `11–12 / 12` |

Then cap the band by the weakest evaluated gate: a minimum of `0` allows only **Broken**, `1` allows at most **Significant rework**, `2` allows at most **Solid**, and `3–4` adds no ceiling. Use the lower-quality result of the average band and this ceiling. The total must equal the exact sum of the three scores. If any required gate is `N/E`, omit the native total, average, common band, and weakest-gate ceiling; report the supported rows and evidence gap instead.

Readiness, dimension score, overall quality band, issue severity, critical blocker, and the authored-state verdict are separate. A Deferred readiness result is not itself P0. Every P0 is a blocker, but a blocker does not automatically rewrite a score to 0; a score of 0 does not automatically imply P0. Non-critical methodology failures belong in the local verdict, score, sequencing, or handoff—not in **Blocker**.

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

**Ordering (one rule):** sort by priority, P0 first. Within the same priority, break ties by gate order—**Placement** (the wrong beat, or a beat off the default path) outranks **Proportion** (treatment out of scale with the moment) outranks **Signature** (character that reads as anonymous or borrowed). Never reorder across priorities; a P0 Signature issue outranks a P1 Placement issue.

## Output format—use this exact structure

Every search returns this template in this order. Repeat Moment and small-thing lines only as warranted; fixed sections remain present even when their content is `None.` For a complete scorecard, include the native total, average, band, and weakest-gate ceiling. For an incomplete scorecard, keep all three gate rows, write `N/E—insufficient evidence` for each unsupported gate, use `N/E` in the Verdict without a total segment, and omit the **Total** row entirely.

```markdown
**Verdict:** <authored | anonymous | misplaced | exhausting | deferred | N/E> · <the biggest missed, misplaced, or unsupported decision> · **<total/12 only when all gates are scored; otherwise omit this segment>**

**Product:** <what it is, for whom> · **Path:** <N> beats, <entry> → <outcome> · **Ends feeling:** <named state or `unnamed`>
**Readiness:** <Ready | Deferred | N/E—insufficient evidence> · <why, plus owner when Deferred>
**Screen:** <exact touchpoint(s) or `not shown`>
**Flow:** <named happy path or transition(s) or `not shown`>
**State:** <exact rendered or system state(s) reviewed>
**Lifecycle:** <exact occurrence(s) reviewed>
**Coverage:** <app states and lifecycle occurrences actually reviewed> · gaps: <material states or occurrences not shown, or `none`>
**Basis:** <observed from a screenshot or artifact | inferred from code | tested in a prototype or live product | walked from a description | measured from product data> · confirm with: <fastest validating check>
**Blocker:** <None. | concise blocker reason>

## The path
| # | Beat | Touchpoint | Frequency | Stakes | Verdict |
|---|---|---|---|---|---|
| 1 | <enters from…> | <surface> | <once | recurring | every-run> | <low | medium | high | not shown> | <Expected | Elevated | Net-New (Moment 1)> |

## Scorecard
| Gate | Score | Why this score | What raises it one point |
|---|---:|---|---|
| Placement | <_/4 or N/E—insufficient evidence> | <evidence → consequence → rubric anchor, or evidence gap> | <change, `None—already exemplary`, or fastest evidence check> |
| Proportion | <_/4 or N/E—insufficient evidence> | <evidence → consequence → rubric anchor, or evidence gap> | <change, `None—already exemplary`, or fastest evidence check> |
| Signature | <_/4 or N/E—insufficient evidence> | <evidence → consequence → rubric anchor, or evidence gap> | <change, `None—already exemplary`, or fastest evidence check> |
| **Total** | **<_/12 · _._/4>** | **<band and exact sum>** | <weakest-gate ceiling> |

## The moments (Net-New, up to 3, ranked by contextual reach × likely memory)
### Moment 1—<beat>, <named feeling>
- **At:** screen: <exact beat/touchpoint> · flow: <named happy path or transition> · state: <exact app state> · lifecycle: <exact occurrence>
- Why here: <contextual reach × likely memory comparison, including utility, stakes, frequency, cost, and evidence>
- Expected: <one line> · Elevated: <one line> · Net-New: <one line>
- Constraints: <one line>

## The small things (Elevated)
- **At:** screen: <exact beat/touchpoint> · flow: <named happy path or transition> · state: <exact app state> · lifecycle: <exact occurrence> · Beat <n>—<craft touch>

## Issues (most severe first)
- **[P0–P3 · beat <n> | off-path restraint]** **At:** screen: <exact beat/touchpoint> · flow: <named path or transition> · state: <exact app state> · lifecycle: <exact occurrence>. <Name>—<observation and consequence>. **Fix:** <fix>.

## Kept Expected, on purpose
<beats kept standard and the strongest reason—convention, frequency, stakes, already-sufficient craft>

## Next
- **Now**: **At:** screen: <exact beat/touchpoint> · flow: <named path or transition> · state: <exact app state> · lifecycle: <exact occurrence> · <first treatment—or required readiness handoff>
- **After it lands**: **At:** screen: <exact beat/touchpoint or `not shown`> · flow: <named path or transition or `not shown`> · state: <exact app state or `not shown`> · lifecycle: <exact occurrence or `not shown`> · <next justified treatment, or `None`>
- **Hand off**: **At:** screen: <exact beat/touchpoint or `not shown`> · flow: <named path or transition or `not shown`> · state: <exact app state or `not shown`> · lifecycle: <exact occurrence or `not shown`> · <screen structure → Focal; path/navigation → Compass; relationship leak → Flywheel; `None` if ready>
```

Filling it:

- **The path**—one row per consequential default-path beat, including Expected beats. A beat whose first pass differs from steady state carries both frequency tags.
- **The moments**—emit zero to three. If none clears the bar, keep the header and write `None—no beat currently earns Net-New; see Kept Expected.` Never create filler to satisfy a count.
- **The small things**—emit only craft the beat's ceiling allows. Write `None.` when no Elevated treatment is warranted.
- **Readiness and N/E**—Deferred does not automatically erase Soul findings. Use `N/E—insufficient evidence` for any unsupported gate, including when readiness is Ready; score supported treatment and sequence it appropriately. A missing variant alone does not make a gate N/E.
- **Coverage and Basis**—name only states and occurrences actually observed or walked. Use `not shown` and the fastest validating check instead of awarding credit or inventing failure.
- **Issues and suggestions**—every issue, Moment, small thing, Next item, and handoff receives a complete **Screen · Flow · State · Lifecycle** locator. If behavior is unknown, report the next evidence check rather than a defect, implementation recommendation, or score. If nothing ranks above P3, write `None above P3.` under Issues.
