# Flywheel Examples

Two worked examples in the locked output templates—one incomplete full diagnosis, one relationship-stage design. Each input states the supplied facts; proposed changes and assumptions are labeled so the output does not invent analytics or unshown states.

---

## Example 1—Diagnose: a team analytics product with a retention complaint

**Input:** *"People sign up and never come back. We think we need better re-engagement emails."* The product turns support tickets into themed insight reports for support and product teams. The complete landing-page copy contains the headline "Turn support tickets into prioritized themes" and a "Get started" CTA, with no report example or indication that a CSV export is required. Signup is email plus a 6-field workspace setup, then a required CSV upload with no sample data, then an empty dashboard reading "No reports yet." A first report takes about 4 minutes to generate and completes with a toast reading "Done." The working first-value event is a user reading a prioritized report. The intended cadence is recurring weekly. No analytics beyond signup counts are supplied. The re-engagement email is a proposed intervention, not an observed state; no returning-user, lapse, or advocacy state is supplied.

**Flywheel's output:**

```
**Verdict:** Friction · setup precedes any chance to inspect a report · **N/E**

**Product:** support-ticket analytics for support and product teams · first value: a user reads a prioritized report · cadence: recurring weekly · success outcome: repeated weekly analysis that informs a support or product decision · stakes: low
**Scope:** full relationship diagnosis
**Screen:** landing promise, workspace setup, report result, and empty dashboard
**Flow:** signup-to-first-report
**State:** first encounter, required setup, empty dashboard, report loading, and report success
**Lifecycle:** arrival, activation before first value, and first value
**Coverage:** landing promise, signup, pre-value setup, CSV upload, empty dashboard, report loading/success · gaps: measured activation cohorts, returning-user state, lapse timing, re-engagement, and advocacy not shown
**Basis:** walked from a description · confirm with: share of signups that generate a first report, then weekly return among those who do
**Blocker:** None.

## Scorecard
| Play | Score | Why this score | What raises it one point |
|---|---:|---|---|
| Trust | 2/4 | The landing headline names the audience problem and output, but the supplied page omits a report example and the required CSV commitment; the category is functional while credibility and the next commitment remain partial. | Show a real or clearly labeled sample report beside the promise and expose the next commitment and its consequence. |
| Friction | 1/4 | Six setup fields and a required CSV upload block any first report; the outcome remains technically reachable, but commitment effort is seriously misplaced before value. | Generate a real report from sample data in one click and defer fields that are unnecessary for safe processing until after first value. |
| Wins | 1/4 | The supplied 4-minute generation ends in a generic "Done" toast, so the user is not shown what changed or why the result matters; value arrives but is largely invisible. | Replace the toast with the report result, what was analyzed, and one next action that extends the win. |
| Emotion | N/E—insufficient evidence | The supplied description contains no returning-user, lapse, re-entry, accumulated-value, or advocacy state; no recurring relationship judgment is supportable from this artifact. | N/E—confirm the intended weekly return state and inspect successful re-entry after a first report. |

## Issues (most severe first)
- **[P1 · Friction]** **At:** screen: Workspace setup → CSV upload · flow: signup-to-first-report · state: required configuration with no sample · lifecycle: activation before first value. The setup wall—6 workspace fields and a CSV upload sit before any output. The upload requires an export before someone can inspect the output; the purpose and processing dependency of the six fields need verification. This is commitment friction placed before value. **Fix:** ship a sample dataset that generates a real report in one click; verify which fields are unnecessary for safe processing and defer those until after the first report exists.
- **[P1 · Wins]** **At:** screen: Report generation → result · flow: signup-to-first-report · state: success after a 4-minute loading wait · lifecycle: first value. The silent power stroke—the product's whole value arrives after a 4-minute wait and is announced by a toast reading "Done." The supplied artifact does not show what was found, how many tickets were read, or what changed. **Fix:** replace the toast with the result—themes found, tickets analyzed, the top theme stated in one line—and a next action that extends it.
- **[P2 · Trust]** **At:** screen: Landing promise · flow: signup-to-first-report · state: first encounter with no report example or CSV requirement in the supplied page · lifecycle: arrival before signup. The headline is specific, but the complete supplied landing-page copy omits a report example and the CSV requirement. **Fix:** put an actual or clearly labeled sample output beside the promise and verify the first commitment's consequence.

## Fix this first
**At:** screen: Workspace setup and Reports dashboard · flow: signup-to-first-report · state: required setup and empty dashboard · lifecycle: activation before first value
Friction. Repair the effort before the first report first; the downstream retention hypothesis remains unverified. The Emotion play is N/E because no recurring return state was supplied, so validate it after first value rather than inventing a re-engagement intervention.

## Next
- **Now**: **At:** screen: Workspace setup and Reports dashboard · flow: signup-to-first-report · state: required setup and empty dashboard · lifecycle: activation before first value · cut the path to first report to one click on sample data; defer fields confirmed unnecessary for safe processing; turn the empty state into the entry point.
- **After it moves**: **At:** screen: Report result · flow: signup-to-first-report · state: success after processing · lifecycle: first value · replace the "Done" toast with the result and a next action; test a related upgrade or weekly return prompt only if that outcome is part of the supplied product goal.
- **Hand off**: **At:** screen: Workspace setup form · flow: signup-to-first-report · state: required pre-value setup · lifecycle: activation before first value · the 6-field setup form is a single-screen structure problem once it is repositioned—Focal.
```

---

## Example 2—Stage design: the first-report stage

**Input:** *"Design the first-report experience the diagnosis called for."* Supplied facts: the product turns support tickets into themed reports; signup has email plus 6 workspace fields; a required CSV upload precedes an empty dashboard; the first report takes about 4 minutes and ends with a "Done" toast. The product is intended for recurring weekly use by support leads. The sample dataset, generated report, deferred fields, and state behavior below are proposal assumptions; no implementation is supplied.

**Flywheel's output:**

```
**Stage:** First report—the friction play, for a support lead evaluating the product in their first session.
**First value:** a themed report generated from real tickets, read and understood   ·   **Success outcome:** a weekly analysis that informs a support or product decision   ·   **Cadence:** recurring
**Stakes:** low

## Evidence / assumptions
- Evidence: email signup, 6 workspace fields, required CSV upload, empty dashboard, 4-minute report generation, and a "Done" toast.
- Proposal assumptions: a safe sample dataset can be shown, a generated report can render before real upload, and deferred workspace fields can be saved after first value.

## The leak
- Today: 6 workspace fields and a required CSV upload stand between signup and any output, and the empty state offers no path. Nobody can see a report without exporting data first.
- Hypothesis: commitment friction is asked before the user has evidence that the report is useful.
- Confirm with: share of signups generating a first report within 24 hours, then weekly return among those who read it.

## The design
- Signup asks for email only. Proposal assumption: infer the workspace name from the domain, show it as editable text, and defer nonessential fields.
- Show a generated sample report after signup so the user reads an actual output before doing work. Label the data as sample and explain what will change when real tickets replace it.
- One primary action: "Run this on your tickets." It opens the upload after value has been demonstrated.
- Show the 4-minute generation state with tickets read and themes forming instead of an indeterminate spinner. This is a proposed progress treatment, not a claim about current behavior.
- Completion states the result: themes found, tickets analyzed, the top theme in one sentence, and the report itself. Replace the current "Done" toast with the result.

## State / applicability inventory
- Applicable states: completion, partial upload or generation failure, recovery/retry, cancellation/abandonment, and no ask.
- Completion: proposed report summary and saved result; the user can inspect the report or run it on real tickets.
- Partial/failure: preserve uploaded work where safe, identify what failed, and offer retry or a clear recovery path.
- Recovery/retry: return to the failed step with context intact; proposal assumption pending implementation evidence.
- Cancellation/abandonment: explain what is retained or discarded and how to return safely; do not promise persistence until verified.
- N/A states or gates: permission—N/A—no permission request is supplied; decline—N/A—there is no ask on this stage.
- Unknown behavior: report persistence, upload recovery, and generation failure behavior require an implementation check; they are not observed facts.

## Friction kept
- The upload step itself. It is procedural—the product cannot analyze tickets it does not have—and it now sits after the user has seen what the analysis produces.
- Naming the report before saving it. Productive friction: a named report is easier to find for the intended weekly return, and the cost is a few seconds against a durable gain.

## The ask
- Ask: None—no ask on this stage
- Lands after: N/A—no ask
- Declining changes: N/A—no ask

## Gates
- [x] First value, intended cadence, and success outcome are named; a finite or infrequent stage is not given a fabricated recurring target
- [x] The leak and diagnostic hypothesis are grounded in supplied evidence, and the confirming metric is named
- [x] Every required step has a purpose the user could be told
- [x] Applicable states and exits are inventoried only where relevant; N/A reasons and unknown behavior are explicit
- [x] Protective and productive friction preserved
- [x] Any ask lands after the value it extends; declining preserves value already earned and any foregone benefit is explicit and noncoercive; a no-ask path is stated when relevant
- [x] Nothing here hides cost, consequence, permission, reversibility, cancellation, or recovery
```

The first diagnosis does not turn the proposed email into a lapsed-user state or score a missing recurring behavior as a defect. It identifies the supported Friction and Wins evidence, leaves Emotion N/E, and puts the fastest validation before a re-engagement intervention. The stage design then makes its sample report and state handling explicit proposal assumptions, while preserving the upload as procedural friction.
