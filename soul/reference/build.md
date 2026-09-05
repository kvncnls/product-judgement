# Soul Build—the moment spec

Use this reference when the request is to build, design, or treat one beat on a working path. It is a proposal, not a score. The caller may ship the Expected floor, the Elevated rung, or the Net-New rung named by **Target**. A build must make the floor shippable, explain its budget decision, and preserve the user's ability to understand and control the task.

Do not use this reference to repair a broken path. If the user cannot reach the beat, hand the issue to the relevant sibling Skill first: a screen problem to Focal, a path or state problem to Compass, or a value and return problem to Flywheel. A treatment can be drafted as a future candidate, but it is not the first fix.

## The five moves

1. **Frame it.** Name the product, user, beat, touchpoint, state, lifecycle occurrence, frequency, stakes, and one feeling. Use a concrete feeling such as confidence, relief, curiosity, control, or pride; `delight`, `soul`, and `personality` are not feelings. If the artifact does not expose a field, write `not shown` and name the fastest check. Stakes describe what can be lost at this beat—money, work, standing, safety, access, or nothing material. High stakes put reassurance, records, and control before expression.

2. **Inventory applicable states.** Review the state inventory below before choosing a treatment. Applicability depends on the beat and product: completion is relevant when the beat has an outcome, partial failure when work can divide into successes and failures, permission when an OS, device, data, or people permission is requested, recovery when interruption or retry is possible, cancel when work can be abandoned, repeated use when the beat recurs, and reduced motion or low-motion when motion or sensory feedback is present or the user preference can change it. For every row, mark `Applicable`, `N/A—<specific reason>`, or `Not shown—<fastest evidence check>`. Do not assume all listed states belong to every moment.

3. **Place it.** Run the beat through the sort tree in [SKILL.md](../SKILL.md). Set **Target** to Expected, Elevated, or Net-New. A Net-New target must clear the selection bar in [moments.md](moments.md) using the available reach, utility, stakes, frequency, cost, and recall evidence. An Elevated target adds craft without a new noun. An Expected target records why convention, frequency, stakes, an already-sufficient treatment, or missing evidence makes restraint correct. If the beat is off the default path, relocate the budget.

4. **Ladder it.** Write a real Expected floor first. Add Elevated only when the same moment can be executed with more care without introducing a feature, surface, or mechanic. Add Net-New only when the target and state inventory justify an entirely new experience in place of the old one. Rungs above the target must say `unavailable at this beat's ceiling` and give the reason. A proposed capability must state how it stays useful, perceivable, comprehensible, and controllable at the stated frequency; an assertion that it will be memorable or durable is a hypothesis to test.

5. **Guard it and run the gates.** No rung may delay the primary action, hide failure, remove control, or make feedback too fast, subtle, or complex to perceive. High-stakes moments state the material consequence before any feeling. Every-run treatments need evidence from repeated use or an explicit validating check; a quick first-run reaction is not enough. Use the gate notation below. These gates are unscored: mark `[x]` only when the proposal satisfies one, `[ ]—<reason>` when it does not, `[N/A—<specific reason>]` when it genuinely does not apply, and `[Not shown—<check>]` when the available evidence cannot judge it.

## Applicable state inventory

Use this inventory for the specific beat. It is a coverage tool, not a requirement to invent states. The reason column is required for `N/A` and `Not shown`.

| State or occurrence | Status | Applicability reason, evidence, or next check |
|---|---|---|
| Completion | `<Applicable; N/A—reason; Not shown—check>` | <what successful completion means here, or why this beat has no completion>
| Partial failure | `<Applicable; N/A—reason; Not shown—check>` | <how a mixed outcome can occur, or why the operation is atomic>
| Permission | `<Applicable; N/A—reason; Not shown—check>` | <permission boundary and user consequence, or why none exists>
| Recovery / retry | `<Applicable; N/A—reason; Not shown—check>` | <how interruption or failure can recover, or why no recovery exists>
| Cancel / exit | `<Applicable; N/A—reason; Not shown—check>` | <what leaving preserves or discards, or why cancellation is impossible>
| Repeated use | `<Applicable; N/A—reason; Not shown—check>` | <frequency and repeated-use behavior, or why the beat occurs only once>
| Reduced motion / low-motion | `<Applicable; N/A—reason; Not shown—check>` | <motion or sensory alternative, or why no motion treatment is proposed>

When a state is applicable, the build must say what the proposed treatment does in that state. Clear failure treatment states what happened, what was preserved, what remains uncertain, and the next action. It keeps tone plain and respectful; failure is a place for agency and recovery, not a celebration destination. A permission request states why access is needed, what it enables, and what happens when the user declines. Cancel and recovery preserve work where the product can, make loss explicit before it occurs, and leave a visible path back.

For a repeated beat, inspect both first and later occurrences where evidence exists. Compare utility, feedback latency, perceivability, comprehension, and control. If later behavior is not shown, keep the proposed repeat treatment conditional and name the check. For reduced motion or low-motion, provide a complete non-animated equivalent; meaning cannot depend on motion, color, sound, or a timing-sensitive effect.

## Rung guidance

**Expected** is the obvious, fully functional version: standard conventions, clear copy, complete feedback, and a recoverable outcome. It is the final answer when novelty would tax a load-bearing convention, high stakes call for calm, frequency leaves no supported expressive lever, or the artifact already has enough authored care.

**Elevated** is the same moment with visible care. It can sharpen hierarchy, use the user's words, name what changed, show work during a wait, anticipate a safe next step, or provide feedback with a perceivable settle. It does not add a new surface or mechanic. Any motion remains optional, brief enough not to delay the task, and paired with text or structure that carries the meaning.

**Net-New** replaces the old treatment with an entirely new experience: a capability, mechanic, surface, or artifact that makes the moment worth choosing for this product. It is allowed only when the beat clears the selection bar and remains proportionate to stakes and frequency. State the utility that survives repeat use, the cost of building and maintaining it, and the evidence still needed. Never add a Net-New rung to fill the zero-to-three budget.

## Output—the Moment Spec

Every standalone build returns this structure in this order. Fill the slots and keep fixed labels. The state inventory remains in the output even when several rows are `N/A`.

```markdown
**Moment:** <the beat>—for <who>, on <the first pass | every pass | the nth pass>.
**Feeling:** <one named emotion> · **Frequency:** <once | recurring | every-run> · **Stakes:** <low | medium | high> · **Target:** <Expected | Elevated | Net-New>

## Why this moment
- On the path: <where it sits, and who reaches it>
- Budget decision: <why this beat earns treatment—or why Expected restraint is correct>
- Today: <what the moment does now—observed, inferred, or `not shown` with the check>

## Applicable states
| State or occurrence | Status | Applicability reason, evidence, or next check |
|---|---|---|
| Completion | <Applicable; N/A—reason; Not shown—check> | <...>
| Partial failure | <Applicable; N/A—reason; Not shown—check> | <...>
| Permission | <Applicable; N/A—reason; Not shown—check> | <...>
| Recovery / retry | <Applicable; N/A—reason; Not shown—check> | <...>
| Cancel / exit | <Applicable; N/A—reason; Not shown—check> | <...>
| Repeated use | <Applicable; N/A—reason; Not shown—check> | <...>
| Reduced motion / low-motion | <Applicable; N/A—reason; Not shown—check> | <...>

## The rungs
- **Expected:** <the floor—the obvious version, fully functional, shippable as-is>
- **Elevated:** <the same moment with more craft, or `unavailable at this beat's ceiling` with the reason>
- **Net-New:** <an entirely new experience in place of the old one, or `unavailable at this beat's ceiling` with the reason>

## Held constant
- <what no rung may damage—speed, comprehension, control, the primary action, reversibility>
- <the convention kept, if this beat is muscle-memory>

## Constraints for the pick
- <brand, technical, accessibility, frequency, stakes, and context limits every rung already respects>

## Gates
- [ ] On the default path—reached without hunting
- [ ] One feeling, named—"soul" and "delight" appear nowhere as specs
- [ ] Survives its frequency—repetition-proof only when evidence supports it
- [ ] Proportionate to the moment's magnitude
- [ ] Speed, comprehension, control, and the primary action untouched
- [ ] Honest without motion and without sound
```

The pick between rungs belongs to the caller. The Target records the result of the sort; it does not force the caller to ship Net-New. A checked gate is not a score. If a gate is inapplicable, include its `N/A` reason in the output; if evidence is missing, include the check instead of claiming that the proposal passes or fails.
