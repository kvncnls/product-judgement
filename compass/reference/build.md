# Compass Build: the Flow Spec

Read this reference only for a `build` request or when turning a reviewed journey into a new flow. Compass builds a route whose outcome or home is explicit, whose steps are honest, and whose state and exits are specified for the states the actual journey needs.

## Four moves

1. **Frame the journey.** Name the finite outcome or the open ended intent and home anchor. Record the audience, stakes, entry points, and journey type. A finite task list is a `task-list` journey when users complete several tasks in a user chosen order before one final outcome.
2. **Map the route or space.** List the screens, repeat loops, branches, task hub and task details, and the final review or submit path that the user actually needs. A task list is a finite hub/detail loop, not a linear screen count: users may choose task order, return to the hub, and submit only when the service's required tasks are complete.
3. **Inventory applicable states and transitions.** Record only the states and seams the journey needs: default, loading, validation or error, partial completion or failure, retry, permission, Back, branch change, save and return, interruption, re entry, review, final submit, and completion as applicable. For each, state what is visible, what carries forward, what can be safely retained, what expires or must be revalidated, and how the user recovers. Do not add a generic state checklist to a flow that does not need it.
4. **Signpost and join the seams.** Give each screen a cue for its actual position and remaining work. Use a stable count only when it is meaningful; a named three stage stepper can omit a counter. Give every owned flow a platform appropriate retreat, home path, and exit. Make defaults visible and correctable, confirm consequential values, and specify context and state across each transition.

For persistence, choose the smallest safe scope. Retain data only when the service has a safe and permitted place to keep it, a stated retention and expiry policy, a re entry path with the authentication and authorization the data requires, and a way to revalidate stale or consequential data. If those conditions do not hold, explain the loss at exit and provide a recoverable re entry or safe alternative appropriate to the service. “Return tomorrow resumes everything” is not a default requirement.

## Output format: use this exact structure

Return the following template in this order. Number screens the user passes through for a linear flow. For a `task-list`, use the representative hub → task → hub loop, then review and submit; state that task order is user chosen and that the loop is finite. For an open ended journey, number a representative entry → explore or refine → detail → home loop and call it a loop, not a completion funnel. Mark a gate `[x]` only when the spec actually satisfies it; keep `[ ]` with a reason otherwise. Use `N/A—<reason>` for a gate or state that does not apply; a justified N/A is not a failed gate. Keep a labeled field and write `None.` when it has no content.

```text
**Flow:** <name>—<finite: gets the user from entry to outcome | open-ended: lets the user pursue one intent while keeping one named place as home>.
**Type:** linear | branching | hub-and-spoke | task-list | open-ended   ·   **Audience:** novice | mixed | expert
**Outcome / anchor:** <finite destination | open-ended organizing intent + home anchor>

## Steps
1. <screen>—<its job> [skip: <the safe, visible, correctable default that removes this step, if any>]
2. <screen>—<its job>

## State / transition inventory
- States: <only the applicable default, loading, validation/error, partial completion/failure, retry, permission, saved, expired, review, success, or other states>
- Transitions: <forward/back, branch change, task order, save/return, interruption/re entry, deep link, final review/submit, and recovery as applicable>

## Cut
- Merged: <the steps you collapsed> → <the one step they became>
- Removed: <steps cut as waste>—<why they were not protection>
- Kept as protection: <any step that looks like waste but stays, and why>

## Orientation
- Position/progress: <the outcome and the cue suited to this journey—named stages, task statuses, a stable count, or location/home; do not force a widget or counter>
- Retreat/home + exit: <the platform-appropriate retreat, home, and escape behavior>

## Continuity
- Carries forward: <context passed across steps; inferred values shown and correctable>
- Survives: <state kept on Back / refresh / interruption / re entry only when safe, permitted, unexpired, and revalidated as needed; otherwise the stated recovery>
- Entry points: <where deep links / notifications land>
- Consequence checks: <what is confirmed before a consequential commit, and what permission or revalidation is required>

## Gates
- [ ] Finite: one outcome with no independent second outcome · open-ended: one organizing intent and a stable home anchor
- [ ] Every step earns its place; nothing protective cut
- [ ] Where-am-I + journey-appropriate progress or location + retreat/home + exit throughout
- [ ] No memory bridge; safe state handling; deep links land in context
- [ ] Inferred defaults are visible and correctable; consequential values are confirmed
- [ ] Drop test passes on every applicable screen and transition
```

Build output is a proposal. Do not claim that a state, persistence rule, permission, validation path, or implementation exists unless it is supplied as a requirement or deliberately specified in the proposal. Design each individual screen with [Focal](https://github.com/kvncnls/product-judgement/blob/main/focal/SKILL.md).
