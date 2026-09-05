# Focal Examples

Three worked examples, shown in the locked output templates: a **review**, a **build**, and a review with an unevaluable dimension. The first two share a narrative: the review finds a CRM contact screen carrying four jobs, and the build designs one of the task screens it recommends splitting out. The third shows how to preserve supported findings without inventing a score or implementation when evidence is incomplete. These set the bar for length, specificity, and tone; the templates set the shape.

---

## Example 1—Review: a CRM contact detail screen

**Input:** A CRM contact record for reps who primarily check recent activity and the open deal during calls. The description shows name/photo/title; six editable fields; 40 activity entries expanded with no grouping or filter; open “Log a call” and “Send email” composers; Deals, Notes, and Files panels; eight similar contacts in a right rail; and Save, Convert to Deal, and Delete styled as identical filled buttons. Every panel header has equal weight. The supplied workflow says prospecting happens in the search view. No empty state, autosave, confirmation, or responsive behavior is supplied.

**Focal's output:**

```text
**Verdict:** No · the record’s read-first purpose competes with two open composers · **4/12**

**Screen:** CRM Contact detail · register: task-overloaded · audience: mixed
**Flow:** screen-local
**State:** full/default only
**Lifecycle:** recurring record review during calls
**Context:** rep checking recent activity and the open deal · bar: the supplied workflow
**Coverage:** described full/default composition and action styling · gaps: empty, save, destructive-action, responsive, and permission behavior not shown
**Basis:** walked from a description · confirm with: observe a rep locating the last interaction and open deal, then inspect save and Delete behavior
**Blocker:** None observed. Delete’s consequence and reversibility are not shown.

## Scorecard
| Discipline | Score | Why this score | What raises it one point |
|---|---:|---|---|
| Information Architecture | 1/4 | The supplied read-first job competes with two open composers and a prospecting rail. Those independent tasks are a major structural distraction from the stated record-review intent. | Make the record a coherent hub; reveal a composer only when selected and move prospecting to its supplied search context. |
| Progressive Disclosure | 2/4 | The necessary activity and deal context is present, but both composers and 40 ungrouped entries appear before selection, creating a material mismatch with the quick-scan workflow. The count alone is not the failure. | Group recent activity and make composers on-demand, while preserving access to the full history and open deal. |
| Visual Hierarchy | 1/4 | Equal panel headers and three equally filled actions give no dependable read-first region or action ranking. | Give recent activity and the open deal clear precedence; differentiate actions after confirming their role and consequence. |
| **Total** | **4/12 · 1.3/4** | **Broken; exact sum of justified scores** | Weakest-discipline ceiling applied |

## Issues (most severe first)
- **[P1 · IA]** **At:** screen: Contact detail body · flow: screen-local · state: full/default · lifecycle: recurring record review. Open composers and prospecting content compete with the supplied activity-and-deal task. **Fix:** use a record hub with explicitly selected call/email composers and move prospecting to search. Keep editing available; verify save semantics before changing persistence or retiring Save.
- **[P1 · Hierarchy]** **At:** screen: Contact detail body and action bar · flow: screen-local · state: full/default · lifecycle: recurring record review. Equal headers and identical filled buttons obscure the intended read-first region and action roles. **Fix:** rank activity and the open deal; visually distinguish routine and potentially destructive actions. Check Delete’s consequence before prescribing confirmation or undo.
- **[P2 · Disclosure]** **At:** screen: Activity timeline and composers · flow: screen-local · state: full/default · lifecycle: recurring record review. The needed context exists, but ungrouped history and unselected composers compete with scanning. **Fix:** group activity by meaningful time or event, provide a visible history/filter control, and reveal composers on selection. Choose any initial history window from realistic usage, not a fixed item quota.

## Top moves (up to 3)
1. **At:** screen: Contact detail body · flow: screen-local · state: full/default · lifecycle: recurring record review · Make the record a hub with activity and the open deal leading; launch composers on selection.
2. **At:** screen: Contact detail action bar · flow: screen-local · state: full/default · lifecycle: recurring record review · Rank action roles and verify save/Delete semantics before changing behavior.

## Next
- **Structural** (do first): **At:** screen: Contact detail body · flow: screen-local · state: full/default · lifecycle: recurring record review · Prototype the hub and check whether reps find the last interaction and open deal without losing useful context.
- **Executional** (after): **At:** screen: Contact detail body and controls · flow: screen-local · state: full/default · lifecycle: recurring record review · Apply the product’s hierarchy and control conventions, then inspect realistic content and viewport sizes.
- **Hand off**: **At:** screen: selected composer → record · flow: call/email completion · state: not shown · lifecycle: after composing · Compass can verify the return and state transition once a route is available.
```

---

## Example 2—Build: the "Log a call" screen

**Input:** "Build the Log a call screen launched from the contact record."

**Proposal assumptions:** a dialer can supply call context; authorized users may access an existing recording; follow-up scheduling and deal association are optional. Confirm these capabilities before implementation. The state handling below specifies intended behavior rather than claiming it already exists.

**Focal's output:**

```
**Screen:** Log a call—organized around recording what happened on a call the user just made. **Action model:** one primary: Log call.
**Register:** task   ·   **Audience:** mixed

## Information
- Call context strip (contact name, photo, number dialed, timestamp, prefilled)—co-locates the decision with its inputs so the rep never has to remember who they called or when; read-only, no fields to re-enter.
- Outcome selector: Connected / Voicemail / No answer / Wrong number—the one fact every logged call must carry. The four supplied outcomes form one recognizable decision; verify labels and selection behavior with reps.
- Duration—prefilled from the dialer, editable. Sits beside Outcome because the two are read together as one "what happened" chunk.
- Notes—the reason the rep is on this screen thirty seconds after hanging up. Given the most vertical space of anything on the screen.
- "Schedule follow-up" toggle—a proposed optional next step after a connected call, kept local when the workflow supports it; validate its frequency with reps.
- "Add to deal (3)"—one quiet control, with the count, because a call that moves a deal must be attributable to it.
- Last call line ("Last call: Jul 2, voicemail")—one ambient line, so the rep knows whether this is a first attempt or a fifth without leaving for the timeline.
- Moved off: the six editable contact fields → Contact detail hub, edited using the record’s verified save model.
- Moved off: the full 40+ activity timeline → Contact detail hub, grouped and filterable; only the relevant last-call summary stays here.
- Moved off: Send email composer → its own compose screen, launched from the Contact detail header.
- Moved off: Deals, Notes, and Files panels → Contact detail hub; this screen reaches Deals only through "Add to deal (3)".
- Moved off: the 8 similar contacts → search and list views, where comparing people is the actual job.

## Disclosure
- Now: call context strip, Outcome (4 options), Duration, Notes, last-call line, "Log call". Busiest decision point holds 4 chunks—context, outcome, duration, notes.
- On-demand: follow-up date and task title → behind the "Schedule follow-up" toggle (contextual reveal—the fields only matter after the rep says yes).
- On-demand: deal association picker → behind "Add to deal (3)", with the count shown so the deferral reads as depth, not absence.
- On-demand: call recording and transcript → behind a "Recording" link in the context strip, present for the rare dispute, absent from the fast path.
- Cut: lifecycle stage and lead source editors—a call log is not where a rep re-classifies a contact, and offering it invites a wrong edit under time pressure.
- Cut: the similar-contacts rail. Nobody logging a call needs eight other people.
- Exit: Discard names that unsaved notes will be lost; offer the safe draft option when supported. No extra confirmation is needed when there is no unsaved work.

## Hierarchy
- Primary: "Log call"—the only filled button on the screen, at the form’s completion point, with placement tested against the viewport, keyboard, and product conventions.
- Secondary: the Outcome selector (four clearly labeled targets; focus follows the supported input method), the Notes field (largest area, quiet-bordered), Duration.
- Ambient: the call context strip and last-call line (muted, read-only), "Schedule follow-up", "Add to deal (3)", "Recording", and "Discard" as a plain text link. Space and weight carry the whole ranking; the single accent color is spent only on "Log call".

## States
- Empty: a first-ever call shows "First call with Ana" in place of the last-call line.
- Loading: context strip skeletons while the dialer record resolves; the form is interactive immediately.
- Partial: if the dialer returns the contact but not duration or timestamp, show the available context, mark missing values as unavailable, and let the rep edit them before logging.
- Permission denied: if access to an existing recording is denied, explain that it is unavailable while keeping call logging available. Do not request microphone access merely to play a stored recording.
- Error: a save failure states the verified result and retains the current input while the screen is open. Say “Saved locally” only if that storage succeeded and the service permits it.
- Recovery: retry preserves the entered notes and avoids duplicate call logs. Specify draft storage, expiry, appropriate access control, and revalidation only if the service safely supports return; otherwise explain the loss before exit.
- Success: after "Log call," confirm the call was saved, show the new last-call line, and offer the local next action, "Schedule follow-up."
- Full (worst case): 900-character notes scroll inside the field without pushing "Log call" off-screen; a 40-character company name truncates in the strip rather than wrapping to three lines.

Scope note: all listed variants apply because dialer data, recording access, save completion, and interruption are part of this task’s possible states.

## Gates
- [x] One-sentence organizing intent; no unrelated second outcome
- [x] Action model matches the register; any co-equal actions are inherent to the same intent
- [x] Grouped + labeled; no orphans; no memory bridge
- [x] Decision load fits the audience and stakes; nothing essential deferred
- [x] One element or region is materially heaviest and expresses the action model; any primary action reads as actionable
- [x] Every applicable state is specified, including success, partial, permission, and recovery modes when relevant; irrelevant modes have a reason
```

---

## Example 3—Review with incomplete visual evidence

**Input:** A text-only inventory of an import preview: one labeled source picker, a preview table with the source’s three fields needed to verify records, an optional mapping control behind a visible “Edit mapping” label, and Import. The stated goal is to verify this source and import it. No screenshot, style definitions, visual ordering, or interaction tests are available.

**Focal’s output:**

```text
**Verdict:** Yes · the described local intent is clear; visual hierarchy is unevaluable

**Screen:** Import preview · register: task · audience: mixed
**Flow:** screen-local
**State:** described default contents only
**Lifecycle:** before import
**Context:** user verifying records before committing · bar: supplied task requirements
**Coverage:** content inventory, required context, and disclosure label · gaps: rendered hierarchy, interaction, long-file, partial-result, permission, and recovery states
**Basis:** walked from a text inventory · confirm with: render the screen with realistic records, inspect the mapping reveal, and exercise import outcomes
**Blocker:** None observed.

## Scorecard
| Discipline | Score | Why this score | What raises it one point |
|---|---:|---|---|
| Information Architecture | 3/4 | Source, verification data, and Import support the stated job; this is a coherent structure in the supplied inventory. Label comprehension has not been tested. | Check the source and column labels with intended users. |
| Progressive Disclosure | 3/4 | Verification fields remain visible and optional mapping has a named cue. The described default layering is strong; interaction and long-file behavior remain coverage gaps. | Inspect the reveal and representative data sizes before changing the design. |
| Visual Hierarchy | N/E—insufficient evidence | The inventory contains no rendered order, weight, spacing, or control styling, so it cannot support this rubric. | Obtain a rendered view or the relevant styles before scoring. |

## Issues (most severe first)
None observed in the supplied inventory.

## Top moves (up to 3)
None. The next step is to inspect the missing evidence.

## Next
- **Structural** (do first): **At:** screen: Import preview · flow: screen-local · state: default and mapping reveal · lifecycle: before import · Verify the described content and reveal against the rendered behavior.
- **Executional** (after): **At:** screen: Import preview · flow: screen-local · state: not shown · lifecycle: before import · Inspect visual order and control signifiers at supported viewports.
- **Hand off**: **At:** screen: import outcome · flow: import completion · state: not shown · lifecycle: after commit · Compass can assess recovery and continuity when the relevant transition evidence is available.
```

Missing visual evidence prevents a hierarchy score. Missing interaction variants
remain coverage gaps for otherwise supported dimensions. No native total,
average, band, or weakest-dimension ceiling is reported.
