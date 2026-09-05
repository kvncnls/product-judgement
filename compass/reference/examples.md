# Compass Examples

These examples calibrate the native review and build shapes. The review demonstrates partial evidence and per dimension `N/E`; the build demonstrates a finite task list with user chosen order, Save and return, and final submit. They are examples, not universal requirements.

## Example 1 — Review: a task list with an unseen re entry seam

**Input:** A municipal license renewal service shows a start page, a task hub, and one task detail screen. The hub lists “Applicant details,” “Supporting evidence,” and “Review and submit”; the first task is marked Completed and the other tasks Incomplete. The description says users may choose their task order and return to the hub after each task. No frame or test shows Back, refresh, Save and return, expiry, permission changes, re entry, validation, or final submission.

**Compass's output:**

```text
**Verdict:** N/E · the final outcome and re entry seam are not shown

**Flow:** Municipal license renewal · type: task-list · audience: mixed
**Outcome / anchor:** submitted renewal application
**Screen:** start page → task hub → Applicant details task
**State:** task hub default, one completed task, one incomplete task, and task detail default; Save and return and final submit not shown
**Lifecycle:** first-run application setup before submission
**Context:** applicant completing work across tasks · bar: a clear government service with task statuses and a visible final review
**Coverage:** start page, task hub, task order statement, task detail, and hub return · gaps: Back, refresh, validation, permission, expiry, Save and return, re entry, final review, and submit not shown
**Basis:** walked from a description and selected frames · confirm with: complete two tasks in different orders, leave and re-enter, then review and submit
**Blocker:** None observed. The final submission and re-entry behavior are not shown.

## Scorecard
| Discipline | Score | Why this score | What raises it one point |
|---|---:|---|---|
| Orientation | 3/4 | The task hub names the finite application, shows Completed and Incomplete statuses, and the shown task returns to the hub; this is Strong for the evidenced route, while the final submit and error escape are not shown. | Walk final review and submit plus error and permission states; change only what that evidence warrants. |
| Path Economy | 3/4 | The service lets users choose task order and return to the hub, so it avoids an arbitrary linear funnel; the unseen task dependencies and final route prevent an exemplary judgment. | Confirm task dependencies and final review hops before proposing a cut. |
| Continuity | N/E—insufficient evidence | The selected frames expose no Back, Save and return, refresh, expiry, permission, or re-entry seam, so this rubric cannot be judged without turning unknown behavior into a defect. | N/E—walk Save and return, expiry, permission, revalidation, and re-entry before proposing a change. |

## Issues (most severe first)
None above P3.

## Top moves (up to 3)
1. **At:** screen: task hub → task detail → task hub · flow: municipal license renewal · state: task order and return · lifecycle: first-run application setup · Walk the final review and submit path and the Save and return/re-entry seam before prescribing a change.

## Next
- **Structural** (do first): **At:** screen: final review and submit · flow: municipal license renewal · state: not shown · lifecycle: first-run application setup before submission · Confirm the finite completion event and required task dependencies.
- **Executional** (after): **At:** screen: task hub · flow: municipal license renewal · state: default task statuses · lifecycle: first-run application setup · None—no executional issue is evidenced.
- **Hand off**: **At:** screen: task hub rows · flow: municipal license renewal · state: default status labels · lifecycle: first-run application setup · None—single-screen hierarchy is not being judged here.
```

The missing variants do not erase the supported Orientation and Path Economy findings. Continuity is N/E because the available artifact contains no continuity seam to evaluate; the output names the next evidence check instead of inventing a persistence defect or implementation.

## Example 2 — Build: a finite task-list service

**Input:** “Design a license renewal service for mixed-expertise applicants. They must complete three tasks in whatever order works, may save a safe draft and return, and must review and submit the renewal.”

**Compass's output:**

```text
**Flow:** License renewal—gets the user from the service start page to a submitted renewal.
**Type:** task-list   ·   **Audience:** mixed
**Outcome / anchor:** renewal submitted after all required tasks are complete

## Steps
1. Task list hub—shows the three finite tasks, their Completed or Incomplete status, the task the user can choose next, and the final Review and submit condition. Users choose order and return here after each task.
2. Task detail—completes Applicant details, Supporting evidence, or Renewal dates, then offers Save and return when safe and permitted; Back returns to the hub with safe values intact. [repeat: one task at a time in user-chosen order]
3. Review and submit—shows the completed task summary, fee, effective date, and renewal consequence; the user corrects errors, confirms the consequential values, and submits.

## State / transition inventory
- States: hub default with mixed statuses; task detail default, loading, validation error, permission denied, saved draft, expired draft, and success; review with unresolved validation; submit confirmation and submitted success.
- Transitions: start → hub; hub → any incomplete task; task → hub; Back; Save and return; authenticated re-entry; expired or unauthorized draft recovery; hub → review when required tasks are complete; review → correction or submit; submit → success/home.

## Cut
- Merged: task completion and return → one task detail → hub loop, so each task can be completed without a confirmation round trip.
- Removed: a forced task order and a setup tour—neither protects the renewal and both delay the service outcome.
- Kept as protection: the final review and submit step, fee and effective-date disclosure, validation, permission checks, and confirmation of consequential values.

## Orientation
- Position/progress: the hub states “Renewal application” and the finite outcome. Task statuses show what is complete and actionable. A named three-stage cue—“Tasks → Review → Submit”—shows the journey without requiring a numeric counter.
- Retreat/home + exit: each task has Back to task list and Save and return where supported; the start page has Exit service; review has Back to task list and Cancel; success returns to the application home.

## Continuity
- Carries forward: the task name, entered values, evidence status, fee, and effective date appear where needed. Any inferred date or applicant detail is labeled with its source and can be corrected before review.
- Survives: Back keeps safe task values in the current activity. Save and return stores only permitted draft fields after the user chooses it, shows what was saved and the expiry date, requires authenticated and authorized re-entry, and revalidates permissions, dates, fee, and stale evidence before review or submit. An expired or revoked draft explains the limit and offers a recoverable new start; it does not promise that everything resumes tomorrow.
- Entry points: a signed resume link opens the authorized task hub or named task with status and expiry visible; an unauthorized or expired link explains the result and routes to the service start.
- Consequence checks: before submit, show the final task summary, fee, effective date, and permission to submit; ask for explicit confirmation and keep correction routes available.

## Gates
- [x] Finite: one outcome with no independent second outcome · open-ended: one organizing intent and a stable home anchor
- [x] Every step earns its place; nothing protective cut
- [x] Where-am-I + journey-appropriate progress or location + retreat/home + exit throughout
- [x] No memory bridge; safe state handling; deep links land in context
- [x] Inferred defaults are visible and correctable; consequential values are confirmed
- [x] Drop test passes on every applicable screen and transition
```

The task list remains finite without pretending that users follow one sequence. Its Save and return behavior is specified with safety, permission, expiry, revalidation, and recovery conditions; the W3C redundant-entry guidance is not used as a claim that every service must persist across sessions.
