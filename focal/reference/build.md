# Focal Build—the Screen Spec

Use this reference when the request is to build, design, or restructure one
functional screen. The output is a proposal, not a score. Read
[SKILL.md](../SKILL.md) first for the intent test, register tree, action
models, and decision procedures. Read [patterns.md](patterns.md) only when a
technique or anti-pattern is relevant. Before a direct build, calibrate from
[examples.md](examples.md); an orchestrated Product Judgement pass skips that
calibration read.

## The five moves

Write the answers in the Screen Spec below, in order.

1. **Name the intent and action model.** Finish *“This screen exists so the
   user can ___.”* Reject an “and” only when it joins independently
   completable outcomes. Classify the register, then name one primary action,
   an inherent co-equal set, ranked routes, or the content field that leads.
2. **Architect the information.** Keep elements that support the intent,
   group related items, label them in the user’s words, infer recognizable
   input before asking for classification, and keep decision-critical context
   beside the action. Move an independent outcome to its own focused screen or
   make the current screen an explicit hub.
3. **Triage disclosure.** Minimize decisions without withholding evidence.
   Judge the local decision load in context of audience, familiarity, stakes,
   device, frequency, and grouping. Sort every relevant element into Now,
   On-demand, or Never. Give each deferred item a cue visible in the default
   state; never defer a price, required field, material consequence, permission
   or risk, required control, or evidence needed for informed choice.
4. **Rank what stays.** Name the visual entry point and the intended attention
   order. Use space and weight before size and color. Exact spacing, type-size
   ratios, and mobile placement are contextual starting points: follow the
   product’s design system and verify against content, viewport, input method,
   reachability, and task frequency. When the dominant element is an action,
   name its control signifier. Make relationships and consequences legible
   with a summary, comparison, or preview when useful.
5. **Map applicable states and run the gates.** Enumerate the states this
   screen can actually enter. Include success/completion, partial data or
   failure, permission denial, and interruption/recovery when the screen has
   those modes. For each applicable state, specify visible status, action
   availability, retained work or context, and recovery. Mark an impossible
   mode `N/A—<reason>` only when that reason matters. Do not add irrelevant
   variants to satisfy a universal checklist.

## Screen Spec

Every direct build returns this structure, in this order. Repeat labeled
bullets when the screen needs more than one item. Leave a labeled bullet as
`None.` when it has no entries.

```text
**Screen:** <name>—organized around <one clear intent; no unrelated second outcome>. **Action model:** <one primary | inherent co-equal set | ranked routes | content-led>: <name the action, set, routes, or content field>.
**Register:** <task | hub | exploration | task-overloaded>   ·   **Audience:** <novice | mixed | expert>

## Information
- <element or group>—<why it belongs / how it is grouped>
- Moved off: <element> → <where it goes instead>

## Disclosure
- Now: <shown this visit>
- On-demand: <deferred> → behind <perceptible cue>
- Cut: <removed, or unsafe affordance replaced with what>

## Hierarchy
- Primary: <the visual entry point—the task action, read-first content, leading hub route/group, or exploration content field; when it is an action, say what makes it read as actionable>
- Secondary: <ranked supporting elements or regions; `None` is valid>
- Ambient: <the muted rest>

## States
- <applicable state or mode>: <visible status, available action, retained work/context, and recovery>
- Scope note: <why the listed variants apply; name any material impossible mode as `N/A—<reason>`>

## Gates
- [ ] One-sentence organizing intent; no unrelated second outcome
- [ ] Action model matches the register; any co-equal actions are inherent to the same intent
- [ ] Grouped + labeled; no orphans; no memory bridge
- [ ] Decision load fits the audience and stakes; nothing essential deferred
- [ ] One element or region is materially heaviest and expresses the action model; any primary action reads as actionable
- [ ] Every applicable state is specified, including success, partial, permission, and recovery modes when relevant; irrelevant modes have a reason
```

The gates are unscored checks of the proposal. Mark `[x]` only when the spec
actually satisfies a gate; leave `[ ]` with a short reason otherwise. Use
`N/A—<reason>` when a gate does not apply; that is not a failed check. Gate 5
describes intended hierarchy; the squint test itself requires a render and
belongs in a later review. A state that is unknown at build time gets a
constraint or evidence check, not an invented implementation detail.
