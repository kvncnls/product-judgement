# Flywheel Build—the Stage Spec

Read this reference only for a `build` request or when turning a reviewed relationship stage into a proposal. It owns the build workflow, the Stage Spec, state applicability, and unscored gates. A build is a proposal: supplied facts are evidence, while unspecified behavior is a proposal assumption or an evidence check. A finite or infrequent service may be designed to complete, hand off, and exit; do not add a recurring habit, upgrade, share, or retention objective without an intended product outcome.

## The workflow

1. **Frame the relationship.** Name the product, audience, stakes, first-value event, intended cadence, and success outcome. First value changes the user's situation; it is not setup completed. Cadence is `finite`, `one-off`, `infrequent`, `recurring`, or `unknown`; success must fit it. A finite service can succeed by safe completion and exit.
2. **Name one stage and its leak.** Choose Trust, Friction, Wins, or Emotion. State what is lost there today, or what would be lost if the stage shipped poorly. Give a diagnostic hypothesis when evidence supports one, and label assumptions.
3. **Run one play.** Read that play's reference and apply its checks deeply. A stage build is focused; it does not redesign the other three plays.
4. **Design the stage.** Describe what the user encounters in order, what each element does, and which protective or productive effort remains. Keep the proposal within Flywheel's relationship scope; hand screen structure to Focal, route mechanics to Compass, and expressive treatment to Soul.
5. **Place or refuse the ask.** If the stage contains an upgrade, invite, share, rating, subscription, or other commercial or social ask, put it after the related value. State what declining preserves and any real foregone benefit. If the product has no justified ask, write `None—no ask on this stage`; do not invent one.
6. **Inventory applicable states and exits.** Select only the states this stage can enter from completion, partial completion or failure, permission, recovery or retry, cancellation or abandonment, decline, and no ask. For each selected state specify what is visible, what remains available, what context is retained, and how the user exits or recovers. Give `N/A—<reason>` for a named state or gate that cannot apply. Do not turn an unknown behavior into an implementation claim.

## Output format: use this exact structure

Return this template in order. Mark `[x]` only when the proposal actually satisfies a gate; keep `[ ]` with a short reason otherwise. Gates are unscored. Use `N/A—<reason>` for an inapplicable state or gate; a justified N/A is not a failed gate. Repeat design and state bullets when needed, but do not add a universal state checklist to a stage that does not need it.

```text
**Stage:** <name>—the <trust | friction | wins | emotion> play, for <who>.
**First value:** <the event that changes the user's situation>   ·   **Success outcome:** <the outcome that defines success for this product>   ·   **Cadence:** finite | one-off | infrequent | recurring | unknown
**Stakes:** low | medium | high

## Evidence / assumptions
- Evidence: <supplied facts, artifact observations, or `None.`>
- Proposal assumptions: <assumptions required to make the design concrete, or `None.`>

## The leak
- Today: <what is lost here, and the evidence—measured, diagnosed from an artifact, or `not shown`>
- Hypothesis: <the mechanism that may explain the loss, or `None—insufficient evidence`>
- Confirm with: <the specific metric or behavior that would settle it>

## The design
- <what the user encounters, in order>
- <each element and the job it does for this stage>

## State / applicability inventory
- Applicable states: <only the relevant states selected from completion, partial completion/failure, permission, recovery/retry, cancellation/abandonment, decline, and no ask>
- <state>: <visible status, available action, retained work/context, and recovery or exit>
- N/A states or gates: <candidate states or gates that do not apply, each with a reason, or `None.`>
- Unknown behavior: <the next evidence check or explicit proposal assumption, never an invented implementation>

## Friction kept
- <any effort deliberately preserved—protective or productive—and why removing it would cost more than it saves>
- None, if nothing here protects the user.

## The ask
- Ask: <the commercial or social ask on this stage, or `None—no ask on this stage`>
- Lands after: <the value the user has just received, or `N/A—no ask`>
- Declining changes: <what already-earned value remains, plus any explicit foregone benefit or real consequence, or `N/A—no ask`>

## Gates
- [ ] First value, intended cadence, and success outcome are named; a finite or infrequent stage is not given a fabricated recurring target
- [ ] The leak and diagnostic hypothesis are grounded in evidence or labeled as assumptions, and the confirming metric or behavior is named
- [ ] Every required step has a purpose the user could be told
- [ ] Applicable states and exits are inventoried only where relevant; N/A reasons and unknown behavior are explicit
- [ ] Protective and productive friction preserved
- [ ] Any ask lands after the value it extends; declining preserves value already earned and any foregone benefit is explicit and noncoercive; a no-ask path is stated when relevant
- [ ] Nothing here hides cost, consequence, permission, reversibility, cancellation, or recovery
```
