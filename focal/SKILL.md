---
name: focal
description: Use when designing, reviewing, or decluttering a functional product, app, dashboard, or tool screen on any platform. Focal is the screen-local structure-and-attention lens—it decides what belongs, what waits, and what wins attention through Information Architecture, Progressive Disclosure, and Visual Hierarchy. Its methodology is One Screen, One Clear Intent—not one action per screen. It classifies task, hub, and exploration registers, chooses the matching action model, supports inherent binary-choice or dual-mode sets, and adjusts density for expertise. Triggers on clutter, "too much on screen", "simplify this screen", "what's the primary action", "too many choices", choice overload, manual selection, input parsing, contextual information, "show the consequence", one screen one purpose, one clear intent, IA, dashboard, admin, or onboarding/settings. Not for multi-screen flows or navigation (use Compass), visual styling, motion, research, code, marketing/landing pages, backend, or non-UI work.
license: MIT
argument-hint: "[build | review] <screen, file, or description>"
---

# Focal

**One screen, one clear intent.**

Good UX guides attention. People don't read a screen, they orient on it—scanning for where they are, what matters, and what to do next. Every screen, the moment it appears, has to answer three questions: *Where am I? What matters here? What do I do?* The faster and more certainly it answers, the better it works—whether it's a phone app glanced at one-handed or a dashboard an expert lives in all day. Only the pace and the density change.

Focal's answer is a single methodology: **every screen needs one clear organizing intent.** That does not mean one action, one content block, or one possible user goal. A task screen usually has one primary action; a hub can offer many destinations; an exploration surface can foreground many items. What stays singular is the screen's center of gravity—the reason its content and actions belong together.

Simple, clean UX is not a style. It is the visible result of a screen making that organizing intent legible instead of forcing the user to sort competing intents by eye.

Three disciplines, treated as top priorities, are how you earn that outcome:

- **Information Architecture**—what belongs on the screen, and how it's organized.
- **Visual Hierarchy**—what wins attention once it's there.
- **Progressive Disclosure**—what's shown now, and what waits.

```
                 ┌────────────────────────────────────────────┐
   the outcome   │        ONE SCREEN, ONE CLEAR INTENT        │
                 └────────────────────────────────────────────┘
                        ▲              ▲               ▲
   the means     Information      Progressive       Visual
                 Architecture     Disclosure        Hierarchy
                 what belongs     what shows now    what wins
```

Get all three right and the screen settles around one clear intent on its own. Miss any one and that intent blurs. **Progressive Disclosure is the anti-overload discipline**—it runs before hierarchy because a screen cannot rank its way out of carrying too much. That is a sequencing dependency, not extra numeric weight: all three disciplines still score on the same 0–4 scale.

Together, the disciplines make the screen a better **decision surface**. Keep these four rules in view:

- **Minimize choices.** Minimize decisions, not information: present the choices that change the next action; keep technical detail discoverable when it supports trust, verification, or an expert path.
- **Pattern recognition—infer before asking.** Recognize structured input when the system can, show the interpretation, and let the user correct it instead of forcing manual classification.
- **Contextual UI—keep context at the decision surface.** Put the history, status, price, or consequence needed for an informed choice beside the action; defer deep detail, not decision-critical context.
- **Show the consequence.** Make relationships, tradeoffs, and process state legible through a clear summary, comparison, preview, or visualization when raw values alone make the user do the reasoning.

---

## When to use

Focal is for **functional interfaces**—the screens of an app, product, or tool, on any platform (mobile, web, desktop, tablet), for any user (first-timer or expert). Onboarding, feeds, home screens, settings, dashboards, admin panels, checkout, editors, consoles. If a person is on the screen trying to *do* something, Focal applies.

It is **not** for:
- Marketing pages, landing pages, campaigns—design there is persuasion and narrative, not task completion, so the clear-intent test and working-memory limit bend too far to guide you.
- Backend, infra, or non-UI work.

Dense, expert tools (dashboards, IDEs, trading terminals) **are** in scope—high density is right when the audience can read it. The methodology bends for them, never breaks, through two modifiers covered below: the screen's **register** and the user's **expertise** (experts read dense displays as a few familiar chunks; first-timers can't).

**Scope.** Focal is a *lens* for structure and attention—*what belongs on a screen and how it's ranked*—not a full visual-design system. It tells you the screen's organizing intent, the action model appropriate to its register, its information structure, and its hierarchy. The execution of color, typography, spacing, and motion is left to your own design system and tooling. Get the methodology right first: visual polish lands far better on a screen whose center of gravity is already clear.

---

## The methodology—One Screen, One Clear Intent

The north star. Every screen earns its place by making one organizing intent legible. An **organizing intent** is the reason this screen exists in the product—not a demand that only one action, destination, or item can appear.

- **The one-sentence test.** Finish this sentence: *"This screen exists so the user can ______."* If "and" joins two outcomes that can succeed independently, the screen has competing intents. Split them, or demote one to a secondary path. Do not fail a coherent task merely because its natural name contains "and"—*review and approve this invoice* is one intent when review is necessary to approval.
- **The register-aware action model.** Do not force one CTA onto every screen. A task screen usually gives one action primary weight. A hub ranks several destinations. An exploration surface lets a coherent field of content lead. Binary-choice screens (Accept / Decline) and genuine dual-mode screens (a map's browse + search) may carry an inherent co-equal set. Multiple primary-weight actions are a failure only when they compete for different outcomes or leave the screen without a clear center of gravity.
- **Why this is the whole game.** People need to understand what kind of place they are in before they can use it. A screen with one legible organizing intent feels coherent; a screen hedging across three independent outcomes feels like work. The three disciplines below are the three ways that intent becomes clear—or gets lost.

---

## The three disciplines

These describe the **task screen**—the default screen type, where the user is completing a single job. Hub and exploration screens bend them; see **Registers**, below.

### 1. Information Architecture—what belongs, and how it's organized

A screen is a unit of intent. IA decides which content and actions belong on it, how they're grouped and labeled, and where the screen sits in the larger flow. Get this wrong and no amount of hierarchy or polish can rescue the screen—it is organizing the wrong things.

- **One organizing intent per screen.** Supporting actions can coexist when they advance the same intent. If an action or content region serves an independently completable outcome, move it, defer it, or make the screen's routing role explicit. Split by *intent*, not by content type or by your data model.
- **Group by relatedness.** Things used together live together. Proximity is the cheapest, strongest signal that two elements belong to the same idea.
- **Label in the user's words.** Navigation, sections, and actions named in plain language the user already owns—never system or domain jargon. Recognition beats recall.
- **Pattern recognition—infer before asking.** When input has recognizable structure—an address, identifier, date, or transaction type—parse it and propose the likely interpretation. Show what was inferred, let the user correct it, and keep a manual fallback for ambiguity; do not make the user classify input the system can already recognize.
- **Contextual UI—keep context at the decision surface.** Co-locate everything needed to make a choice where the choice is made. If history, status, price, or consequence informs the decision, bring the relevant slice into the same screen or region. Defer deep detail, never the context required to decide or trust the action, and never force the user to remember a fact from a previous screen (the "memory bridge").
- **Merge needless round-trips; split overloaded screens.** Two screens that each do half of one intent should be one. One screen carrying three independent intents should be split or reframed as an explicit hub. Focal decides whether the resulting screen is coherent; Compass decides how the route between screens works.

> **Fails:** the kitchen-sink screen (three jobs at once); structure that mirrors the database instead of the user's intent; orphan content with no clear home; jargon labels; the memory bridge across screens.

### 2. Progressive Disclosure—show now, defer the rest *(anti-overload)*

Reveal complexity only when the user needs it. Working memory is the hard constraint, not screen real estate. This is the discipline that *keeps* a screen's organizing intent legible over time.

- **Use four chunks as a task-screen diagnostic, not a universal limit.** At one unfamiliar decision point, about four independent options, fields, or facts is a useful default; a higher count is a prompt to test grouping, familiarity, and decision cost, not an automatic failure. A high-stakes choice may need fewer. A learned expert control set may support more.
- **Count chunks, not raw elements.** A group the audience recognizes as one unit—a familiar toolbar, a labeled section—counts as one. Expertise grows chunk size: a pro tool can show dense data because its users read it as a few learned groups, where a first-run screen cannot. Score the actual cognitive decision, not the DOM count.
- **The disclosure triage.** For every element, decide **Now / On-demand / Never.**
  - *Now*—needed to complete the primary action this visit. It stays.
  - *On-demand*—needed by some users sometimes. Defer it behind a reveal (see [reference/patterns.md](reference/patterns.md)).
  - *Never*—nobody needed it; you assumed they would. Cut it.
- **Minimize decisions, not information.** Present the few choices that change the next action. Keep technical detail available when it supports trust, verification, or an expert path, but do not force everyone to interpret it before they can proceed. Smart defaults plus an "Advanced" reveal beats a wall of equal options. Ten settings shown at once is a wall; three with "More options" is a path.
- **No disclosure without a signifier.** Every deferred thing needs a perceptible cue that it exists—a chevron, a labeled "More options," a tab, a count. Deferral hides *complexity*; it must never hide *existence*. Name the cue when you defer, not just the fact of deferring: "advanced filters, behind an 'Advanced' toggle," not "advanced filters, deferred." Content behind a cue nobody perceives is content you cut—and you cut it without deciding to, which is the one form of cutting this skill does not allow. **A cue qualifies only if it is present in the screen's default state, without hover or gesture.** A function reachable only by swipe or long-press is the named worst case: if the only way to discover it is to be told about it, it is hidden, not deferred.
- **The disclosure trap (read this).** Progressive disclosure is *deferral, not burial*. Hiding the primary action, the price, a required field, or a consequence behind a tap is a dark pattern, not disclosure. Never defer what the user needs *now* to act or to trust the screen. Disclosure reduces *choice overload*, never *honesty*.

> **Fails:** the wall of options; an onboarding form that asks everything up front; settings exposed before they're relevant; the primary action or price buried behind a reveal; a reveal with no cue that anything is behind it.

### 3. Visual Hierarchy—what wins attention

Once the right things are on the screen and the rest deferred, rank what remains. Importance is communicated by visual weight: the heaviest element or region is the most important one—always, with no exceptions you did not choose deliberately for the register.

- **The squint test.** Blur your eyes (or the screenshot). Can you still tell what's #1, what's #2, and how things group? If everything has the same weight, you have a list, not a hierarchy.
- **The quick-orientation test.** On a task screen, a first-time user should identify the read-first region or next action within a few seconds. Treat three seconds as a probe during testing, not a stopwatch-based scoring rule; hubs and exploration surfaces orient through a leading group or content field instead of one CTA.
- **Weight must match importance.** The most common hierarchy bug: decoration (a hero image, an illustration, a giant logo) outweighs the action model's dominant element or region. Visual weight is a budget—spend it on what the user came to do.
- **The focusing mechanism.** One element or region must be the visual entry point that says *start here*. On a task screen that is usually the primary action or the content needed before it; on a hub it can be the leading destination or group; in exploration it is the content field itself. If the eye bounces between unrelated, equally weighted regions, the organizing intent is not being expressed.
- **Show the consequence.** When a decision depends on a relationship, tradeoff, or process state, show that meaning at the decision surface—a simple summary, comparison, preview, or visualization may do more than a list of raw numbers. Keep exact values and supporting detail available as evidence; the visual should clarify, not decorate or conceal.
- **Weight ranks; it does not permit.** Hierarchy answers *what should I do*; it does not answer *what can I do*. A heading can be the heaviest thing on screen and still be inert. So where the primary is an action, it has to carry a signifier that reads as actionable during the first scan: a traced boundary (fill, border, or elevation), a platform-native control convention (an iOS bar button), or an icon plus label inside a tap target. Bare text at any weight, with no convention behind it, ranks without permitting—say which of these the primary is using. A screen can pass the squint test and still leave the user unsure they are allowed to touch anything.
- **No false signifiers.** A shadowed card that doesn't open, underlined text that isn't a link, a chevron that leads nowhere—these spend attention the screen budgeted for real actions, because the eye reads them exactly like real controls. They also cost trust the first time someone taps one and nothing happens. Count them as clutter, not decoration.
- **The hierarchy ladder.** Use the *fewest* dimensions that achieve clear ranking, in this order: **space → weight → size → color.** Reach for color last; it is the loudest and easiest to overuse.
- **The shape of a good screen:** one dominant element or region, two to three secondary tiers, everything else ambient. The dominant thing must match the register's action model. When every element is loud, none is.

> **Fails:** hierarchy carried by color alone; the "visual noise floor" where everything has equal weight; decoration outweighing function; six type sizes that read as one; a dominant action that ranks first but doesn't read as actionable; inert elements dressed as controls.

---

## Registers—when the rules shift

The disciplines above assume the **task screen**: the default, and the most common. Two other screen types are legitimate, and applying task rules to them is a mistake—it flattens screens that are *supposed* to hold many things. Identify the register first; it changes how the clear intent is expressed, which action model fits, and where the disciplines bind.

**Classify with this tree.** Walk it top to bottom and take the first match. Answer about what the user came to *do*, not about how the screen currently looks—a cluttered screen is not automatically a hub.

```
Did the user come here to complete one specific job?
├── Yes → TASK
└── No
    ├── Is this screen's own job to send them somewhere else?
    │   └── Yes → HUB
    └── Did they come to browse content, with no particular endpoint?
        ├── Yes → EXPLORATION
        └── Neither is clearly true
            └── TASK, overloaded into a hub. Score it as a task screen
                and flag the overload under Information Architecture.
```

Two ties worth naming, because they recur:
- **A record or detail screen** (a contact, an issue, an order) is a **hub** when its job is to show state and route you onward, and a **task** screen when it exists to be edited. If it tries to be both at once, that is the overloaded case—the tree's last branch.
- **Search results** are **exploration** when the user is scanning to discover, and a **task** screen when they are finding one known item to act on.

- **Task**—the user is completing a specific job. *Default; everything above applies as written.* One completion intent, usually one primary action, with decision load matched to audience and stakes. An inherent binary choice or inseparable dual mode can be co-equal without creating a second intent. (Checkout, compose, a signup step, a settings detail, any form.)
- **Hub**—the user is choosing where to go. The organizing intent *is routing*; many destinations is correct, not clutter. (Home screen, profile, settings index, account screen, app root.)
- **Exploration**—the user is browsing for its own sake. Abundance is the point; the goal is dwell and discovery, not a fast exit. (Feeds, discover/browse tabs, search results, a photo or product grid.)

The methodology still holds—*one screen, one clear intent*—but its expression changes by register, and the working-memory limit **relocates** rather than disappears:

| | Task | Hub | Exploration |
|---|---|---|---|
| **Organizing intent** | complete one coherent job | route among related destinations | browse one coherent content space |
| **Action model** | one primary action usually wins; name any inherent co-equal set | rank destinations; let the likely next route lead | content leads; controls support continued discovery |
| **Where the chunk diagnostic applies** | the unfamiliar decision point | per group / per row, not the total destination count | per item, not the item count |
| **Hierarchy** | one dominant action or read-first region | one destination or group leads; routes remain comparable | one content type dominates; chrome recedes |

The diagnostic relocates rather than vanishes. A settings index with 9 rows can be fine; a settings row asking a novice to compare 9 unfamiliar facts probably is not. A feed with 200 posts can be fine; a card with several competing decisions still needs scrutiny. Context and familiarity decide the score, not a raw count alone.

The trap runs both ways: flattening a hub or feed down to a single action (now it does its job badly), **or** letting a task screen sprawl into an accidental hub because you skipped the one-sentence test. When you can't tell which register you're in, you're usually looking at a task screen wearing too many hats—split it or deliberately reframe it as routing.

---

## How they combine—order of operations

Apply them in this order. Skipping ahead produces a pretty screen that does the wrong thing.

1. **Define the intent and action model** (methodology). One sentence; then choose the model that fits the register.
2. **Architect the information** (IA). Decide what belongs, how inputs are interpreted, and what decision-relevant context stays with the action.
3. **Disclose progressively** (PD). Minimize decisions, not information; sort what belongs into Now / On-demand / Never.
4. **Establish hierarchy** (VH). Rank what survived and make the consequence legible without letting supporting visualization outrank the action model.

You cannot rank elements before you know which show (3 before 4), cannot decide what shows before you know what belongs (2 before 3), and cannot decide what belongs before you know the screen's organizing intent (1 before 2). Hierarchy applied to a kitchen-sink screen just makes the clutter well-organized.

This order holds for every register; only the *targets* shift—in a hub, step 4 ranks destinations; in exploration, it ranks content types over chrome.

---

## Flows—hand off to Compass or Flywheel

Focal is screen-local on purpose. A flow is a *sequence* of screens with clear organizing intents, so apply Focal to each screen in one—but the path *between* them belongs to **Compass**, the sibling skill for cross-screen flows. Focal is *within* a screen; Compass is *between* them.

Route it:
- **Focal's**—a screen that does too much, buries what matters, uses the wrong action model, or ranks the wrong thing loudest.
- **Compass's**—too many steps, a dead end, a trapped modal, a Back that wipes work, a deep link that dumps the user at step one, or a user who can't tell where they are in the journey.
- **Flywheel's**—a journey step that stalls activation before first value, hides a delivered win, or causes users to drift instead of return. Compass maps and connects the step; Flywheel diagnoses the lifecycle leak.

An end-to-end journey must include necessary but unglamorous work—setup, verification, signing, recovery, and confirmation—not just the core utility. Compass owns how those steps are sequenced, connected, and resumable. Flywheel owns whether they create friction before value or another lifecycle leak. Focal owns the local decision surface of each screen and should not turn one step into a catch-all.

These skills are not a whole-app IA or sitemap tool. If the question is "how should the entire product be organized," that is a larger exercise—return to Focal screen by screen, and Compass flow by flow, once that map exists.

---

## Routing

**Orchestrated pass—this overrides every other instruction in this Skill and its reference files.** When [Product Judgement](../product-judgement/SKILL.md) loads this Skill for a cross-scale audit, take this paragraph and skip the rest of this section. Treat the pass as `review` over the evidence Product Judgement supplies: never ask a framing question and never stall—write `not shown` and name the fastest validating check instead. Never hand a cross-scale request back to Product Judgement, and send a sibling-owned finding to its **Handoffs** section rather than invoking that Skill. Run the whole contract in [reference/review.md](reference/review.md)—every gate, score, rationale, band, ceiling, severity, and locator—but do not print the locked template, do not read [reference/examples.md](reference/examples.md), and do not apply this Skill's **Voice**, opening-line, or re-run instructions: Product Judgement owns the emitted response, and prints this template only when the user asks for the detailed passes. When its wrapper has no slot for something this contract produces, hand that to Product Judgement in working notes—never append a line after its output. When Product Judgement names several screens, score the *worst* one, name that screen in the rationale, and raise the others as separate findings—never average screens into one score.

- **No argument** → explain the methodology and three disciplines briefly, then ask: building a new screen, or reviewing an existing one?
- **A whole-app or cross-scale audit request** → hand off to [Product Judgement](../product-judgement/SKILL.md), which runs Focal with Compass, Flywheel, and Soul and reconciles the results.
- **`build` (or a description of a screen to design)** → follow **The five moves** below. Pull techniques from [reference/patterns.md](reference/patterns.md).
- **A multi-screen flow, journey, or navigation question** → that is Compass's, not Focal's. Say so and hand off (see **Flows**, above). If the question is where the journey loses activation, value recognition, or return, also hand off to Flywheel.
- **`review` / `critique` / `audit` (or a file, screenshot, or URL to evaluate)** → load and follow [reference/review.md](reference/review.md). It scores each discipline 0–4 against a written rubric, requires an evidence-based rationale and next-point change for every score, totals to /12, displays a normalized /4 average and common quality band with a weakest-dimension ceiling, tags issues P0–P3, and anchors every issue and suggested move to the exact **Screen · Flow · State · Lifecycle** locator before closing on a Clear-Intent verdict. That file defines the rubrics, scoring contract, bands, severities, and audit locator—all of them, and nowhere else.
- **A question about a specific technique or anti-pattern** → consult [reference/patterns.md](reference/patterns.md).

Before emitting either output, read [reference/examples.md](reference/examples.md). It is the calibration for length, tone, and how the locked templates look when filled well—the templates define the shape, the examples set the bar.

---

## Build: the five moves

For each screen, in order. Write the answers down—they are the spec.

1. **Name the intent and action model.** One sentence: *"This screen exists so the user can ___."* Reject an "and" only when it joins independently completable outcomes. Classify the register, then name one primary action, an inherent co-equal set, ranked routes, or the content field that leads.
2. **Architect the information.** List what belongs on the screen. Group related items; label them in the user's words; infer recognizable inputs before asking the user to classify them; and keep decision-relevant context beside each action. Anything serving a different intent moves to another screen.
3. **Triage disclosure.** Minimize decisions, not information. Sort every element into Now / On-demand / Never. Cut the Nevers. Defer the On-demands behind a reveal. Keep the Nows.
4. **Rank what stays.** Assign each surviving element or region a tier: one dominant entry point, only the secondary ranks the screen actually needs, and the ambient rest. A small screen may need one secondary rank; a dense expert surface may need several. Make the dominant tier express the register's action model, and make the consequence legible without letting supporting visualization outrank the action.
5. **Run the gates.** Self-check against the six gates in the **`## Gates`** block of the Screen Spec template below. That block is the single canonical list—read them there, and emit them there. Never restate them in your own words.

A screen that passes all six is structurally sound by Focal's standard. Apply visual styling and motion on top of that foundation—it lands far better on a screen that already earns its hierarchy.

**Output—the Screen Spec (use this exact structure).** Every build returns this template verbatim, in this order. Fill the `<…>` slots; keep every fixed label and every gate, even when the answer is one line.

```
**Screen:** <name>—organized around <one clear intent; no unrelated second outcome>. **Action model:** <one primary | inherent co-equal set | ranked routes | content-led>: <name the action, set, routes, or content field>.
**Register:** task | hub | exploration | task-overloaded   ·   **Audience:** novice | mixed | expert

## Information
- <element or group>—<why it belongs / how it's grouped>
- Moved off: <element> → <where it goes instead>

## Disclosure
- Now: <shown this visit>
- On-demand: <deferred> → behind <reveal>
- Cut: <removed; nobody needed it>

## Hierarchy
- Primary: <the one element or region that is the visual entry point—the task action, read-first content, leading hub route/group, or exploration content field; when it is an action, name what makes it read as actionable>
- Secondary: <the ranked supporting elements or regions; `None` is valid>
- Ambient: <the muted rest>

## States
- Empty: <what the screen says and offers with no data, or `N/A—<reason>`>
- Loading: <skeleton or optimistic; never a blank, or `N/A—<reason>`>
- Error: <plain-language message, at the source, work preserved, or `N/A—<reason>`>
- Full (worst case): <how it holds at max realistic data—longest label, most rows, or `N/A—<reason>`>

## Gates
- [ ] One-sentence organizing intent; no unrelated second outcome
- [ ] Action model matches the register; any co-equal actions are inherent to the same intent
- [ ] Grouped + labeled; no orphans; no memory bridge
- [ ] Decision load fits the audience and stakes; nothing essential deferred
- [ ] One element or region is materially heaviest and expresses the action model; any primary action reads as actionable
- [ ] Every applicable state above designed; each `N/A` is justified
```

Filling it:
- **Repeat any labeled bullet as many times as the screen needs**—`Moved off`, `On-demand`, and `Cut` usually take several lines each. Repeating a label is not adding a section.
- **`<reveal>` means the perceptible cue, not the mechanism.** "Behind an 'Advanced' toggle" and "behind a chevron on the row" are answers; "behind a modal" and "deferred" are not, because neither tells the reader what the user would see that says anything is there.
- **Gates ship unchecked.** Mark `[x]` only for gates the spec actually satisfies; leave `[ ]` with a short reason (one clause) for any it doesn't. Never check a gate the spec does not satisfy—but a spec that genuinely satisfies all six should show all six checked.
- **`Cut` covers removed and replaced.** If a control was needed but has to become a different, safer control, put it under `Cut` and name the replacement—"uncapped refund field → hard-capped to the order total." Cutting an unsafe affordance is not the same as deciding nobody needed it.
- If a labeled bullet has nothing, keep the label and write "None."

Gate 5 is deliberately worded for spec time: it asks whether the spec *assigns* one element or region decisive weight, matches that weight to the action model, and names what makes any primary action read as actionable—all of which a spec can answer. The squint test itself needs a render—run it once the screen exists, and treat a failure there as a review finding, not a build gate.

---

## Voice (when giving feedback)

When you review or justify a Focal decision, write like a senior designer reviewing work they want to be great:

- **Emit the exact output template.** Build and review each have a locked structure—the build template is in the build section above, the review template is in [reference/review.md](reference/review.md). Use it verbatim every time: same sections, same order, same headers, same table columns, same issue-line format. Don't add, remove, reorder, or rename sections; if a section has nothing, keep its header and write "None." Repeatable and scannable is the whole point.
- **Template precedence.** The template is the complete contract for what gets emitted. If any instruction in this skill asks you to produce something the template has no slot for, put it in the nearest slot that fits, or leave it out—never invent a section. A gap like that is a bug in this skill, not a judgment call: name it in one line after the output so it can be fixed. Analysis the template has no room for is still worth doing; it informs the scores even when it isn't printed.
- **Be specific and quantitative.** "There are three primary-weight buttons" beats "too many buttons." Count elements, name the tiers, quote the labels.
- **Be decisive.** "This screen carries two independent intents"—not "this might feel unfocused."
- **Factual first, then judgment, then the fix.** State what you see, why it hurts the user, what it should be instead.
- **No hedging, no praise padding.** Don't sandwich criticism in empty compliments. If something works, say exactly why.
- **Tie every issue to a discipline.** Each problem names which of the three it breaks, and how that obscures the screen's organizing intent. That is the whole point of the lens.
- **Locate every issue.** Name the exact screen or region, rendered app state, and user lifecycle moment where the change belongs. Never make the implementer infer when the finding applies.

---

## Absolute don'ts

Match-and-refuse. If you're about to do one of these, you've broken a discipline—rework it.

- **The kitchen-sink screen.** (IA) A screen carrying three independent intents is three screens, or an explicit hub with focused task paths.
- **Structure that mirrors the data model.** (IA) Organize by user intent, not by your tables.
- **Jargon labels and the memory bridge.** (IA) Name things in the user's words; carry context forward instead of making them remember it.
- **Opaque inference.** (IA) Never silently infer a consequential value. Show the interpretation, let the user correct it, and provide a manual fallback when confidence is low.
- **The wall of options.** (PD) Defaults plus a reveal, never N equal choices at once.
- **Information withheld as simplification.** (PD) Minimize decisions, not the evidence a user needs to trust, verify, or understand the action.
- **Burying what the user needs now.** (PD) Price, required fields, consequences, and controls required by the action model are never hidden behind disclosure.
- **Competing primary actions on a task screen.** (Methodology / VH) Demote one when they pursue independent outcomes. Preserve an inherent binary-choice or dual-mode set, and never apply this task rule to a hub or exploration surface (see Registers).
- **A reveal with no cue.** (PD) If nothing on screen says something is there, it isn't deferred—it's cut by accident. Gesture-only functions are the worst case.
- **False signifiers.** (VH) Inert things dressed as controls. A shadowed card that doesn't open, underlined text that isn't a link. They spend the attention budget and cost trust on the first tap.
- **Hierarchy by color alone.** (VH) Climb the ladder: space and weight first.
- **Raw values without meaning.** (VH) Do not make users derive a relationship, tradeoff, or process consequence from numbers alone; add a clear summary, comparison, preview, or visualization while preserving exact values as supporting evidence.
- **Decoration outweighing the action model.** (VH) The hero image must not beat the task action, leading hub route, or exploration content field.
- **Modal as first thought.** (VH) A modal interrupts the screen's organizing intent. Exhaust inline and progressive alternatives first.

---

## References

- [reference/review.md](reference/review.md)—the three-discipline audit, the Focal scorecard (0–4 per discipline), severity, and output format.
- [reference/patterns.md](reference/patterns.md)—IA techniques, the progressive-disclosure technique catalog, focus mechanisms and the hierarchy ladder in practice, state care (empty / loading / error / full / first-run / peak-end), and the anti-pattern library with fixes.
- [reference/examples.md](reference/examples.md)—worked examples: a cluttered dashboard reviewed, and a screen built, both in the locked output templates.
