# Focal Patterns—techniques and anti-patterns

The working catalog behind the three disciplines and the decision-support rules. Pull from here when building or when prescribing a fix in a review. Ordered the way the disciplines apply: Information Architecture → Progressive Disclosure → Visual Hierarchy.

---

## Information Architecture (Discipline 1)

How to decide what belongs on a screen and organize it around one clear intent.

- **The screen inventory.** List every element a screen wants to hold. For each, ask: *does this support the organizing intent?* If it serves an independently completable outcome, move it, defer it, or make the screen an explicit hub. This is the fastest way to find an accidental kitchen-sink screen.
- **Split by intent, not content type.** "Account" is not one screen because the data lives in one table—it's profile, security, billing, and notifications, each a separate intent. Split where the user's goal changes, not where your schema does.
- **Group by relatedness.** Things used together live together. Proximity is the strongest, cheapest grouping signal—closer than a border, closer than a shared background. Reach for dividers and containers only when space alone isn't enough.
- **Label in the user's words.** Sections, nav, and actions named in language the user already owns. "Trips" not "Itinerary records." Test a label by asking whether a first-timer would pick it blind.
- **Pattern recognition—infer before asking.** When input has recognizable structure—an address, identifier, date, or transaction type—parse it and show the likely interpretation. Let the user correct it, and retain a manual fallback when ambiguity remains. Never make the user classify input the system can already recognize.
- **Contextual UI—keep context at the decision surface.** Everything needed to make a choice is present where the choice is made. If a decision needs history, status, price, or consequence, show the relevant slice beside the action; if step 3 needs a number from step 1, show it on step 3. Never make the user hold it in their head or leave the work surface for decision-critical context.
- **Merge round-trips; split overload.** Two screens that each do half a job and bounce the user back and forth should be one. One screen juggling three jobs should be three.
- **Keep local groups legible.** On a hub, group related destinations and rank the likely routes instead of flattening every destination into one list. Whole-product navigation depth, breadcrumbs, and Back behavior belong to Compass.

**Test:** read only the screen's labels and groupings, ignoring the visuals. Can a stranger tell what the screen is for and what they'd do here? If not, the architecture is unclear before any pixel is styled.

---

## Progressive-disclosure technique catalog (Discipline 2—load-bearing)

Match the technique to *why* the content is deferred.

*About four unfamiliar chunks is a task-screen diagnostic starting point, not a universal limit. On hub and exploration screens, inspect decision load per row or card rather than counting destinations or items. Judge each row or card from familiarity, grouping, stakes, device, content length, and the decision at hand. See **Registers** in [SKILL.md](../SKILL.md).*

| Technique | Use when | Example |
|-----------|----------|---------|
| **Smart defaults + Advanced** | Most users want the common choice; a few need control | "Send now" with a collapsed "Schedule / options" |
| **Accordion / expander** | Several independent sections, user needs one at a time | FAQ, settings groups, order details |
| **Stepper / wizard** | A task has natural sequential stages | Checkout, multi-part signup, setup |
| **Drill-down (master → detail)** | A list where each item has depth | Inbox → message, feed → post |
| **Contextual reveal** | A field/control only matters after a prior choice | "Other" → free-text box; "Ship to address" → address form |
| **Overflow / "more" menu** | A dominant action or small inherent set, plus a tail of rare actions | "⋯" menu, kebab on a card |
| **Peek + expand** | Content is scannable truncated, occasionally read in full | "Show more" on long text, truncated comments |
| **Tooltip / inline hint** | Help is needed rarely and contextually | "?" next to an unfamiliar term |

**Choosing well:**
- **Minimize decisions, not information.** Present the few choices that change the next action. Keep evidence and technical detail discoverable when it supports trust, verification, or an expert path; do not force every user to interpret it before proceeding.
- Defer the *rare*, surface the *common*. The split is by frequency of need, never by your convenience.
- **Every deferral needs a signifier**—the perceptible cue that says something is there, present in the screen's default state without hover or gesture. The table above pairs each technique with its cue: an accordion has its chevron, an overflow menu its "⋯", a peek its "Show more", a stepper its position marker. Choosing a technique means committing to its cue; a technique whose cue you cannot name is not deferral, it is disappearance. When the deferred thing is a countable set, make the cue a count ("12 more") rather than a bare "More", so deferral reads as depth and not absence. Gestures (swipe, long-press) carry no inherent cue, so they need a visible partner control on the screen itself—never use one as the only path to a function.
- One layer of disclosure is a path; three nested layers is a maze. If users must expand to expand to expand, the screen has the wrong architecture (Discipline 1).
- A stepper must show **where the user is and how far is left**—but frame it as achievable milestones ("Step 1 of 3"), not a demoralizing tally ("3 of 47 done").

**Never defer:** the price, required fields, destructive consequences, error states, or controls needed to use the screen's action model now. Deferral is for reducing choice overload, never for hiding what the user needs to act or to trust the screen.

---

## Focus mechanisms (Discipline 3)

How to give a screen a clear visual entry point so the eye knows where to start—the visual expression of its organizing intent and action model.

- **Size and weight differential.** Make the primary element materially larger or heavier than its neighbors. A ratio or token step can be a useful starting point when the system gives no guidance, but choose the relationship in context of the typeface, content, viewport, and audience; defer exact values to the product’s design system.
- **Isolation by space.** Surround the primary element with more whitespace than anything else. The eye goes to what's alone.
- **Position.** Start with reading flow and reachability: place the dominant action where this device, input method, handedness, viewport, and task frequency make it easy to find and use. A thumb-reachable mobile region or a desktop resolution zone may be a hypothesis, not a fixed placement rule; follow the product’s layout system and verify the rendered context.
- **Disciplined color.** On a task screen, reserve the strongest accent for the primary action or inherent co-equal set. On hubs and exploration surfaces, repeated link or interaction color can support a family of comparable routes; keep one region or content type visually dominant through space and weight.
- **Show the consequence.** When a decision depends on a relationship, tradeoff, or process state, make that meaning legible at the decision surface with a summary, comparison, preview, or visualization when useful. Preserve exact values as supporting evidence; do not use the visual to decorate or hide the underlying facts.
- **Suppress the rest.** Often the fastest way to create a focal point is not to amplify the hero but to *quiet everything else*—mute secondary text, recede chrome, drop ambient elements to low contrast.

**Test:** squint at the screen and name where the eye starts. It should land on the task's dominant action or read-first content, the hub's leading route or group, or the exploration surface's content field. If unrelated regions tie for first, the focus mechanism has failed.

---

## The hierarchy ladder in practice (Discipline 3)

Climb only as far as you need. Each rung is louder than the last.

1. **Space.** Proximity groups; distance separates; generous margin elevates. Most hierarchy problems are solved here, for free. Use the product’s spacing tokens when available; otherwise make within-group gaps visibly tighter than between-group gaps and verify with the real content.
2. **Weight.** Font weight and contrast. A bold label against regular body, or full-contrast text against muted, ranks without changing size or hue.
3. **Size.** Type scale and element scale. A deliberate ratio between tiers can help when the system is silent, but the right relationship depends on typeface, language, viewport, and audience. Follow existing tokens and verify that the intended order survives the rendered content.
4. **Color.** The loudest, last rung. On task screens, reserve the strongest accent for the dominant action or inherent set. On hubs and exploration surfaces, use interaction color consistently across comparable controls while space and weight preserve a dominant region. Color as *the* hierarchy tool (rather than reinforcement) is fragile—it fails for colorblind users and in dark/light inversion.

**Rule:** if space and weight already rank the screen, don't add size and color on top. Redundant emphasis flattens hierarchy as surely as no emphasis.

---

## State care

Products live or die on the states most teams treat as afterthoughts. Each is a Focal surface in its own right—it has an organizing intent, an architecture, and a disclosure budget.

- **Full (worst-case) state.** The biggest clutter trap in data UIs: a screen designed against tidy demo rows becomes chaos at realistic volume—with the longest label, the most items, max-digit numbers, and deepest nesting. Design and review against the worst realistic data, not the mock. A layout that only holds together when nearly empty isn’t done.

- **Empty state.** Not a void—the first-run teacher. One sentence of what this becomes, one primary action to get there. Empty states are the highest-leverage onboarding you have.
- **Loading.** Always communicate system status. Skeletons over spinners for content; optimistic UI for actions the user just took. Never a blank screen with no signal.
- **Success and partial states.** When the screen can complete an action or render only part of its data, show what changed or what is available, identify what remains, and keep the next local action clear. Do not assume full success from a partial response.
- **Error.** Plain language, name the actual problem, offer the fix, preserve the user's work. "Email is missing an @" beats "Invalid input." Place it at the source, not in a banner far away.
- **Permission and recovery states.** If access, device permission, interruption, or resumption can change the screen, name the blocked capability, preserve recoverable context, and offer the appropriate retry or return path. These states are relevant only when the screen can enter them.
- **First-use state.** Make the screen's local action model legible without a wall of coach marks. Defer controls that are not needed on this visit. Whether the whole onboarding path reaches first value is Flywheel's question.
- **Completion state.** Confirm what changed, preserve control, and expose the next locally relevant action. Flywheel owns whether the win earns return; Soul owns whether the moment deserves expressive treatment.

---

## Anti-pattern library

Each entry: the tell, the discipline it breaks, the fix. Severity is assigned in [review.md](review.md), not here—one authority, so a finding can't carry two priorities.

- **The kitchen-sink screen**—one screen carries several independent intents without declaring itself a hub. *(IA)* Split by intent, or explicitly organize it as routing with focused task paths.
- **The data-model screen**—structure mirrors the database, not the user's goal. *(IA)* Reorganize around intent; group what's used together.
- **The jargon label**—sections and actions named in system terms. *(IA)* Rename in the user's words; test labels blind.
- **The classification tax**—recognizable input requires the user to select its type, network, or mode before the product can proceed. *(IA)* Parse the input, show the interpretation, allow correction, and keep a manual fallback for ambiguous cases.
- **The context jump**—the user must leave the decision surface to inspect history, status, price, or consequence. *(IA)* Bring the decision-relevant slice into the same screen or region; defer deep detail, not the context needed to choose.
- **The memory bridge**—step 3 needs a fact only shown on step 1. *(IA, PD)* Carry the context forward, or co-locate the decision with its inputs.
- **The wall of options**—many equal, unfamiliar choices at one decision point. *(PD)* Defaults + reveal; recommend one; group the rest. Count alone is not the diagnosis: judge familiarity, stakes, grouping, and whether the choices change the next action.
- **The numeric fog**—raw values leave the user to derive the relationship, tradeoff, or process state that matters. *(VH)* Add a clear summary, comparison, preview, or visualization; keep exact values available as evidence.
- **The everything-up-front form**—onboarding asks for all data immediately. *(PD)* Ask only what's needed for the first success; defer the rest to when it's relevant.
- **The premature settings dump**—advanced options shown before anyone needs them. *(PD)* Collapse behind "Advanced"; smart-default the common case.
- **The buried essential**—price, required field, or consequence hidden behind a tap. *(PD)* Surface it. This is a dark pattern, not disclosure.
- **Competing primary CTAs**—two equally weighted task actions pursue independent outcomes. *(VH)* Demote or move one. Preserve a genuine binary choice or inseparable dual-mode set, and do not apply this task rule to ranked hub routes or content-led exploration.
- **The hero that eats the button**—a giant image/illustration outweighs the primary action. *(VH)* Cut the decoration's weight; the action wins.
- **The rainbow screen**—color used decoratively everywhere, so it can't signal hierarchy. *(VH)* Reserve the strongest accent for the dominant task action or use one consistent interaction color across comparable hub/exploration controls; mute the rest.
- **The flat list pretending to be a hierarchy**—every row identical weight. *(VH)* Differentiate the lead item, or add grouping by space.
- **The invisible reveal**—content deferred behind nothing the user can perceive. *(PD)* Name the cue, or bring the content back. A gesture-only function is this at its worst.
- **The false signifier**—an element that looks interactive and isn't: a shadowed card that doesn't open, underlined text that isn't a link, a chevron that leads nowhere. *(VH)* Give it a control's shape or take the shape away; the ambiguous middle costs a tap and some trust.
- **Nothing reads as actionable**—the primary action carries no control signifier at all, regardless of where it ranks, so the user can see what matters and still not know they may act on it. *(VH)* Give it a traced boundary, a platform-native control convention, or an icon-plus-label tap target.
- **The modal reflex**—interrupting the screen's organizing intent with a dialog for something that could be inline. *(VH)* Exhaust inline and progressive alternatives first.
- **The icon-only mystery nav**—unlabeled icons forcing recall. *(IA)* Add labels; recognition beats recall.

---

## Quick reference card

```
INTENT     "This screen exists so the user can ___."   (no unrelated second outcome)
ACTION     task: one primary usually · hub: ranked routes · exploration: content leads
IA         everything supports the organizing intent · group related · label plainly
DISCLOSE   every element → Now / On-demand / Never · ~4 unfamiliar chunks is a diagnostic
           name the signifier for each deferral
DECIDE     minimize choices · infer before asking · context at the decision · consequence visible
HIERARCHY  1 dominant entry point · only the secondary ranks needed · rest ambient
           space → weight → size → color
NEVER      hide price, required fields, consequences, or controls needed now
```

*A task can preserve an inherent binary choice or inseparable dual mode. On hubs and exploration surfaces, inspect per-row or per-item decision load instead of total item count.*
