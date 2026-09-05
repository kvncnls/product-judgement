# Compass Patterns: techniques and anti patterns

Use this catalog when building a journey or prescribing a fix that the evidence supports. It follows the three disciplines: Orientation, Path Economy, and Continuity.

## Evidence anchors (not compliance certification)

- [GOV.UK task list](https://design-system.service.gov.uk/components/task-list/) describes a finite service where users can complete tasks in whatever order works for them, see task statuses, return to the task list, and move on only when the required tasks are complete. It also says to consider Save and return when a service spans multiple sessions. Use this as a pattern reference, not as a universal product requirement.
- [W3C WCAG 2.2 Redundant Entry](https://www.w3.org/WAI/WCAG22/Understanding/redundant-entry.html) covers information repeated within the same process and allows essential, security, and invalid-data exceptions. It explicitly does not add a requirement to store information between sessions. Use it to avoid memory bridges, not to certify a product or prescribe cross session persistence.

## Orientation patterns

The goal is a user who can answer *Where am I? What remains when bounded? How do I get back, home, or out?*

- **Outcome based progress, not a widget quota.** For a bounded journey, make the outcome and remaining work legible through the cue that fits the actual work: named stages, task statuses, a checklist, a stable count, or a concise summary. A counter is optional. A named three stage stepper such as `Account → Details → Submit` is valid without a numeric count. For open ended work, show position in the space and a known home instead of fake completion progress.
- **Task list as a finite hub.** When users need to complete several tasks in a user chosen order, show every task, its actionable status, and the finite completion condition. Let each task return to the hub. Add Save and return only when the service has a safe, permitted retention and re entry path; final review and submit close the finite journey.
- **Branch and hub cues.** Name a branch when a choice changes the route. In a hub-and-spoke journey, show the active hub location and a labeled route back to the center. Do not require a progress bar where the journey has no endpoint.
- **Platform appropriate retreat.** Use product Back when the product owns the stack, browser Back when history is expected and state safe, a breadcrumb or hub link in nested spaces, and Cancel, Close, or Save and return when the service supports it. Do not duplicate controls without adding clarity.
- **Escape and no dead ends.** Back retreats one step; an escape hatch leaves the bounded flow. Every shown screen, error, success state, and modal has a clear next step or a way out.
- **Drop test.** Remove the content and leave only title, position cue, applicable progress or task status, retreat/home path, and exit. A stranger should still identify the journey and leave or return home.

## Path Economy techniques

Every screen is effort. Remove waste while keeping protection and informed choice.

| Technique | Use when | Example |
|---|---|---|
| **Merge round trips** | Two screens bounce the user back and forth | Pick an item and confirm in place, then return to the list |
| **Safe visible default** | One value is right for most users and easy to change | Preselect locale, show why, and offer Edit before continuing |
| **Visible, correctable inference** | The system can derive a value | Show “Suggested workspace: Acme” with Change, rather than silently committing it |
| **Consequential confirmation** | A value changes money, identity, permission, destination, quantity, legal status, or an irreversible action | Show the interpreted value and effect before Submit |
| **First value before setup** | Configuration is blocking the first useful result | Open a usable workspace, then ask for optional setup in context |
| **Task list** | Several tasks are finite, independently completable, and users need order freedom | Task hub with Incomplete/Completed statuses, task detail, return, and final review |
| **Prune dead branches** | A choice has no real continuation | Remove it or give it a complete route |
| **Collapse adjacent steps** | Two thin screens fit without overloading one screen | Merge name and email; ask Focal to judge the resulting screen density |

Count the honest work for the journey type. User chosen task order is not waste. A step that protects the user or earns informed consent is not waste. Hiding cost, risk, permission, consequence, or a needed confirmation to make a path look shorter is a dark pattern, not economy.

## Continuity patterns

Moving between screens should not cost users context or safe work they already provided.

- **No memory bridge.** Show a code, amount, choice, or destination where it is needed. Within one process, make repeated information visible or available to select, while allowing essential, security, and invalid-data exceptions.
- **Back is a retreat.** Preserve entered state across Back when retaining it is safe. If a sensitive value cannot remain, say so before the user leaves and provide the safe recovery the service supports.
- **Conditional Save and return.** Decide retention from the data and journey, not from a blanket promise. Save only where the service may safely store the data, the user has the required permission, the retention and expiry are clear, re entry has the authentication and authorization the data requires, stale or consequential data is revalidated, and revoked access or conflicts can recover. Show what was saved and what will expire. If the conditions are absent, explain the limit and offer a recoverable re entry or safe alternative.
- **Deep links land in context.** A notification, shared URL, or email opens the relevant task or object with its route, permissions, and current state clear. If access has expired, explain it and route to a recoverable place.
- **Stable mental model.** Keep layout anchors, focused object, and transition direction coherent across a seam. A visual jump that loses context is a continuity issue even when the data remains.

At each seam, ask what the user knew and had on the source screen that the destination needs. If it must be re entered, re found, or re remembered, close the leak or explain why re entry is essential, security required, or invalidated.

## Flow type playbooks

- **Linear:** one path to one outcome. Use outcome based milestones, a task appropriate cue, and safe Back with an escape from the whole flow.
- **Branching:** a user choice creates a distinct sequence. Name the branch, make switching possible, default the common safe route, and remove dead branches.
- **Task-list:** a finite task hub leads to independently completable task details in user chosen order, back to the hub, then to final review and submit. Status tells users what is complete and actionable. Save and return, expiry, permission, revalidation, and recovery are part of the design only when the service needs or exposes them.
- **Hub-and-spoke:** center → detail → center. Keep the center as home and preserve the hub state on return. No progress counter is needed without a finite endpoint.
- **Open-ended:** browse, search, or explore with no fixed completion. Show location, active refinements, and home. Do not force a funnel or invent progress.

## Flow state care

- **Loading, validation, error, and retry:** keep the user on the relevant route, identify the issue, preserve safe work, and keep Back and exit live. Do this only for states the service has or the build explicitly requires.
- **Permission and expiry:** explain what cannot be done, what data or access is affected, and the route to recover. Recheck permission and freshness before a consequential action.
- **Interruption and re entry:** if Save and return is supported, show the saved point, retention/expiry, required authentication, and any revalidation. If it is not safe or permitted, state the boundary and provide the supported re entry path.
- **Final review and success:** make the final consequence and submitted values clear, confirm consequential changes, and give the user a next move or route home after success.

## Anti pattern library

- **The mandatory widget:** a flow is judged against a prescribed counter, progress bar, or breadcrumb even though its outcome is better expressed by named stages, task status, or location. *(Orientation)* Use the clearest outcome based cue; a named three stage stepper may omit a counter.
- **The hidden progress bar:** a bounded journey gives no clue about its outcome or remaining work. *(Orientation)* Add a meaningful named milestone, task status, checklist, or count when stable.
- **The task-list funnel:** independently completable tasks are forced into an arbitrary order or the hub hides the final completion condition. *(Orientation + Path Economy)* Preserve user chosen order, status, return to hub, and final review/submit.
- **The phantom Back:** Back resets entered data. *(Orientation + Continuity)* Preserve safe state or disclose the retention boundary before retreat.
- **The over persistent draft:** sensitive or stale data is retained indefinitely or reopens without permission, expiry, or revalidation. *(Continuity)* Limit retention, authenticate and authorize re entry, surface expiry, and revalidate before commit.
- **The opaque inference:** a consequential value is silently guessed. *(Path Economy)* Show the value and meaning, let the user correct it, and provide a manual fallback.
- **The unconfirmed consequence:** Submit silently applies a material amount, identity, permission, destination, quantity, or irreversible change. *(Path Economy)* Show the effect and require confirmation before commit.
- **The deep link to nowhere:** a notification or shared URL lands at an unrelated start screen. *(Continuity)* Land in context or explain the expired/unauthorized route and provide recovery.
- **The unseen-state fix:** a missing loading, error, permission, or resume state is treated as a defect. *(Evidence discipline)* Mark it `not shown`, name the fastest check, and do not propose implementation until evidence exists.

## Quick reference

```text
FRAME      finite: entry → outcome · task-list: tasks → hub → final submit · open-ended: intent + home
ORIENT     outcome based position/progress or location · retreat/home · exit · no widget quota
ECONOMY    fewest honest steps · safe visible defaults · correctable inference · confirmed consequence
CARRY      context across seams · safe/permissioned state · expiry and revalidation · recoverable re entry
NEVER      dead ends, traps, silent resets, opaque consequence, or invented behavior
```

See [SKILL.md](../SKILL.md) for the methodology and routing, [build.md](build.md) for the conditional Flow Spec, and [review.md](review.md) for the native scorecard.
