# Treatments—the three tiers

The path sort assigns every beat a **tier**—its verdict. A build designs the **rungs**—the full range for one beat, floor to target—so the caller can land anywhere on it without re-briefing. Same three names, two uses: the tier is where a beat ends up; the rungs are the steps a build lays out getting there.

## Expected—the obvious version

The fully functional execution a competent team ships without thinking hard. Standard pattern, standard copy, standard feedback.

**Expected is real work, not a strawman.** It must be shippable, because the beats that must simply work—load-bearing convention, high stakes, anywhere addition taxes the task—end here as the final answer, on purpose. Getting Expected right is also the precondition for the other tiers: an Elevated treatment of a broken interaction is polish on a defect.

**The test:** nothing missing, nothing added. A user relies on it without noticing it.

Examples of the register: a standard signup form, a clear confirmation toast, a conventional dashboard layout, a plain progress bar, a system-default notification.

## Elevated—the same moment, executed with visible care

Nothing new is introduced. The existing thing, done at a grade users can feel even when they cannot say why: hierarchy sharpened, copy in the user's words, motion that explains, feedback that names what changed, an empty state that starts the work, a wait that shows the work.

**Elevated is the anti-boring tier.** It spreads to beats whose ceiling allows it when the craft remains useful, perceivable, and comprehensible under their frequency. Concentration is for Net-New; distribution is for craft that earns repeat use.

**The test:** describe the treatment in one sentence—if the sentence needs a new noun (a new feature, a new surface, a new mechanic), it is not Elevated, it is Net-New wearing modest clothes.

Examples of the register: the confirmation that states the amount and the running total instead of "Done"; the upload that shows filenames processing instead of a spinner; the form whose labels anticipate the next question; the settle animation that gives a completed payment weight.

**On `every-run` and high-stakes beats, Elevated is the default ceiling**—it can raise quality without spending novelty, if feedback stays perceivable and the user retains control. Net-New is an exception, not an entitlement: on an every-run beat it must add utility shown or explicitly tested to remain valuable on later runs; on a high-stakes beat it must strengthen reassurance, records, or control while preserving load-bearing convention. If the case depends on surprise, spectacle, or unfamiliarity, keep the target at Elevated or Expected.

## Net-New—an entirely new experience

An entirely new experience in place of the old one—not the same moment executed better. Elevated asks how well the moment can be executed; Net-New asks what the moment could be instead. A new mechanic, surface, or artifact that makes the moment itself a reason to talk about the product.

**The test:** it could not be mistaken for a competitor—or for the moment it replaced.

Examples of the register: a live visualization where a table was assumed; a personalized artifact worth keeping (a year-in-review, a printable record, a shareable result card); an interactive demo where static onboarding was assumed; a progress mechanic that accumulates something users check voluntarily.

**Net-New ships on no more than three chosen moments, and zero is valid.** It spends surprise, so concentration matters—spread thinly, none may clear the threshold of memorable. A build designs the Net-New rung only when the beat's ceiling and target allow it; otherwise the rung states why it is unavailable. Two rules keep the tier honest:
- **It must survive its frequency.** A Net-New mechanic on an every-run beat must show useful, perceivable, comprehensible behavior on later runs, not only a clever first response. If repeat value is untested, move it to a `once` or `recurring` beat or label the proposal conditional.
- **It must be worth keeping, not just worth noticing.** The strongest Net-New treatments produce an artifact or capability the user returns to; the weakest produce a reaction and then a chore.

## The levers

What treatments are actually made of. Every lever carries its own failure mode—both columns matter.

| Lever | Used well | The failure mode |
|---|---|---|
| **Speed** | a response that feels attentive while remaining truthful and perceivable | feedback that is too fast to notice, hides failure, removes control, or creates a false sense of completion |
| **Feel** | weight, physics, and settle that make interaction tactile | motion that delays the action it decorates |
| **Language** | copy in the user's words, at the moment's temperature; the highest-leverage lever per hour spent | charm before clarity; a voice that jokes at tense moments |
| **Anticipation** | the field pre-filled, the next step staged, the default that shows the product was paying attention | guessing wrong confidently; anticipation that removes control |
| **Continuity** | picking up exactly where the user left off, visibly | claiming to know the user better than the relationship supports |
| **Ceremony** | sequence and pacing that give a rare moment weight—reserved for `once` and milestones | ceremony on routine actions; the 12-second animated unboxing of a weekly report |
| **Accumulation** | progress that visibly builds into something owned—streak-free, pressure-free | streaks and guilt; accumulation that punishes absence |

**Sound is opt-in and off by default.** Meaning never depends on it.

## Repetition-proof design

Potentially repeatable levers, to verify against the actual beat and audience:

1. **Speed**—can reduce repeated effort when the result remains truthful, visible, and recoverable.
2. **Feel**—may signal quality when motion is brief, legible, and optional; test whether it delays or distracts.
3. **Anticipation**—can stay useful when its inference is accurate and reversible.
4. **Useful variation**—content that reflects real state (this week's number, this run's result) may remain relevant; confirm comprehension and control.
5. **Cosmetic variation**—a rotating copy pool can feel alive briefly, but its value and readability need repeat testing. Use small doses.

Jokes, confetti, celebration sounds, surprise, mascot appearances, and sequences longer than the action may lose value with repetition; test them before assigning a recurring ceiling, and move surprise-dependent treatments to `once` or `recurring` when repeat value is absent.

## Proportionality

Feedback intensity matches the size of the moment, and high stakes reorder the sequence:

- **Routine completion**—confirm clearly, offer the next step. No more.
- **Meaningful progress**—name what changed, show the accumulation, restrained motion.
- **Major milestone**—ceremony earned: a designed pause, a summary, an artifact.
- **High-stakes success**—reassurance, records, and control **before** any feeling. The user should be able to confirm what happened and what they can do next before expressive treatment. Calm often fits better where loss is possible, but check user expectations, context, and actual comprehension.

Over-celebrating the routine reads as juvenile and burns trust in every future celebration; under-playing the milestone reads as indifference. Both are Proportion failures in the scorecard, and they are the same failure: intensity decided by habit instead of by the moment.

## The accessibility floor

No rung ships below it: treatments honor `prefers-reduced-motion` with a complete non-animated equivalent, never depend on color, motion, or sound alone, preserve focus and keyboard paths, and keep copy legible at the user's reading pace across languages and assistive technology. A transient toast should carry only what can be perceived in its available time; important status must remain available for retrieval. If motion or speed changes comprehension, revise the treatment.
