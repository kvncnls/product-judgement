# Friction—drag on the bearing

The push landed and the wheel is turning, but effort is stealing it. This play is where most activation is won or lost.

**The job is not zero friction. It is useful momentum.** A bearing with no friction is a bearing that has come out of the wheel—some effort is what keeps the thing safe, understood, and worth having done.

## The six kinds of friction

The whole play turns on telling these apart. Two are waste; four are not.

| Kind | What it is | Default action |
|---|---|---|
| **Accidental** | Effort from poor execution—duplicate fields, unclear labels, broken validation, lost progress, repeated auth, needless context switching | **Remove it.** It serves nobody. |
| **Cognitive** | Effort to understand options, terminology, state, or consequence—dense screens, jargon, ambiguous choices, too many simultaneous decisions | **Reduce, sequence, or explain it.** |
| **Procedural** | Steps a process genuinely requires—account setup, verification, data import, configuration | **Remove what is inherited, automate what is safe, explain what remains.** |
| **Commitment** | Effort that asks the user to invest or decide—choosing a plan, inviting a team, entering payment, publishing | **Move it after value and confidence.** |
| **Protective** | Effort that prevents harm—transaction preview, destructive-action confirmation, permission explanation, risk acknowledgment | **Preserve it.** Make it clear and proportionate, never smaller. |
| **Productive** | Effort that increases ownership, quality, or future value—naming a project, choosing a goal, reviewing an AI output | **Keep it when future value exceeds present cost.** |

**Removing protective friction is not a speed improvement.** It raises completion and transfers the cost to the user, where it returns as support load, refunds, and lost trust. In finance, health, identity, and anything irreversible, protective friction *is* the growth foundation.

## The friction decision test

For every step, field, screen, and decision, answer all seven. If you cannot name the purpose, remove or redesign it.

1. What user or business purpose does this serve?
2. What would fail if it were gone?
3. Can the product infer it or defer it?
4. Does the user understand why it is required?
5. Is this the right moment to ask?
6. Does it increase safety, confidence, or future value?
7. Is the effort proportional to the user's motivation *right now*?

Question 7 is the one teams skip. The same form is reasonable from someone who arrived ready to buy and fatal from someone still deciding whether the product is real.

## Define activation before redesigning onboarding

Onboarding is not a set of introductory screens. It is the path from expectation to first credible value.

**Name the first-value event as a change in the user's situation, not a completed setup step.**

| Weak activation | Strong activation |
|---|---|
| Created an account | Generated and used a meaningful output |
| Completed the tutorial | Completed the first successful transaction |
| Reached the dashboard | Imported data and received an actionable insight |
| Enabled notifications | Invited a collaborator who participated |

**Validate it.** If people who complete the proposed activation event do not reach the product's intended success outcome more often than comparable people who do not, the event is weak evidence of value and the definition should be revisited. For recurring products, that outcome may be return; for finite or infrequent services, it may be completion, handoff, or safe exit. The cohort comparison shows association, not causation; control for acquisition, intent, and survivorship, and use experiments or research before claiming the event caused retention or completion.

## Design backward from first value

1. **Name the first-value event.** What changes for the user?
2. **List true prerequisites.** What must exist before it can happen?
3. **Cut inherited steps.** Which requirements exist only because the process was built that way?
4. **Infer what is safe.** What can defaults, imports, or context supply?
5. **Defer secondary setup.** What can wait until after value?
6. **Explain what remains.** Why is each surviving step needed?
7. **Preserve progress.** Can they leave and resume?
8. **Make completion visible.** Do they recognize that value occurred?

Step 8 is the handoff to the Wins play. Value the user does not notice did not land.

## Progressive disclosure across the stage

Sequence setup so only prerequisites for the next value-bearing step are required now; reveal secondary configuration when it becomes useful. Flywheel owns whether the timing delays first value. Focal owns the disclosure and hierarchy inside any one screen, and Compass owns the route between screens.

**Never defer anything that materially affects consent, cost, risk, or expected outcome.** That is not disclosure, it is concealment, and it is a P0 under this skill's don'ts.

## Defaults, empty states, errors

**A good default** is safe, commonly useful, easy to understand, easy to change, and transparent when consequential. Defaults that benefit the business at the user's expense are a dark pattern wearing a convenience costume.

**An empty state is an activation surface**, not a notice that nothing exists. It should say what will appear here, why it will be useful, offer one primary path to create or import it, and reassure about effort or reversibility.

**Errors decide whether effort is lost.** An effective error says what happened, what was and was not completed, whether data or money is safe, what to do next, whose fault it is, and how to get help. Never blame the user for a system they could not reasonably understand.

## What to measure

Onboarding completion, step-level abandonment, time to first value, error rate, backtracking, repeated attempts, support contact during activation, and activation rate by acquisition source. For recurring products add meaningful return; for finite or infrequent services add completion, handoff, or safe exit.

**Use distributions, not averages.** A median hides the tail of people who are stuck, and the tail is the leak.

Compare the intended success outcome for comparable activated and non-activated cohorts as one validation signal: retention or meaningful return when recurring, completion, handoff, or safe exit when finite or infrequent. Report the result as association unless an experiment or stronger causal design isolates the activation event.

## Anti-patterns

- Optimizing the number of screens instead of the amount of understanding
- Removing information required for informed consent
- Treating every pause as a conversion problem
- Forcing setup before demonstrating value
- Long educational carousels disconnected from action
- Collecting information "for later" with no stated use
- Requiring notification permission before establishing relevance
- Showing expert complexity to beginners by default
- Hiding important detail in the name of simplicity
