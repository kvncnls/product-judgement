# Moments—where the budget goes

A moment is a beat on the happy path that earns the Net-New tier—an entirely new experience, not a better version of the old one. This file is how you decide whether zero to three beats clear that bar, rank those that do, and sort everything else into Elevated or Expected.

## The frequency classes

Frequency is destiny for a treatment—it decides what a moment may carry before anything else does.

| Class | What it is | What it may take | Why |
|---|---|---|---|
| `once` | first-run beats: first impression, first success, setup completion | one-shot expressive treatment—storytelling, sequence, ceremony | it plays once, so it may spend everything |
| `recurring` | weekly-to-monthly rhythm: a report ships, an invoice is paid, a milestone lands | mid intensity, with variation—the 30th arrival must still read as alive | familiar enough to expect, rare enough to feel |
| `every-run` | every session: open, navigate, compose, save, send | treatment whose utility, feedback, perceivability, comprehension, and control survive observed repetition | novelty may decay with repetition; durability is a hypothesis to test |

**The 50th-viewing test:** before treating any beat, say its frequency out loud and imagine the treatment on its 50th appearance. Ask what could fail: delay, hidden status, lost control, low perceivability, or comprehension. Confetti may fail early; a faster save may hold value, but only if the response is truthful, perceivable, and recoverable under real conditions.

## The archetypes

Eight places soul is usually won or lost. Skeleton positions refer to the 7-beat map in [SKILL.md](../SKILL.md).

| Archetype | Skeleton position | Frequency | Candidate feelings | What usually goes wrong |
|---|---|---|---|---|
| **The first impression** | beats 1–2 | once | curiosity, recognition, relief | generic welcome copy; a form where an experience should be |
| **The first success** | beats 5–6, first pass | once | capability, pride | the product's biggest moment announced by a toast |
| **The wait** | beat 5, when work takes >1s | varies | anticipation, confidence | a spinner where evidence of work should be |
| **The effort peak** | beat 4 at its hardest | varies | momentum, control | the hardest step is also the most sterile |
| **The ending** | beat 6 | varies | completion, relief, pride | it stops instead of landing—a surface teams often under-design |
| **The milestone** | recurring passes | recurring | progress, accumulation | either silent, or identical the 40th time |
| **The handoff** | the artifact that leaves the product | recurring | pride to the sender, sense to the receiver | an export nobody would show anyone |
| **The return** | re-entry after absence | recurring | continuity, being known | a cold start where a "welcome back" state should be |

Three boundary notes. *The first success* is the beat where first value lands—Flywheel's term for the event that changes the user's situation; if the product loses people before this beat, that is a leak, and leaks go to [Flywheel](../../flywheel) before treatments. *The return* is expressive treatment on re-entry: [Compass](../../compass) owns whether state survives the specific transition, Flywheel owns whether returning restores momentum or accumulated value, and Soul makes that working return felt. *The ending* can be a strong candidate when users reach it, the outcome matters, and evidence suggests it shapes recall; an every-run ending still takes only treatment that remains useful and comprehensible, while ceremony may fit rare endings.

## Selection—the bar a moment must clear

Rank candidates with **reach × likely memory** as a working hypothesis, not a fixed law. Compare how many users reach the beat, the utility and meaning of the outcome, stakes, frequency, implementation and maintenance cost, and actual recall or user-description evidence. Peak and ending cues may help when the moment is salient and reachable, but a later beat is not automatically better; if recall evidence is absent, label the comparison as a hypothesis and name the fastest delayed-recall, interview, replay, or sharing check.

One bounded reference points in both directions: a study of a rich, heterogeneous VR experience found average valence and arousal better predicted one-week remembered experience, while peak valence helped immediate recall. That limited context does not establish a product rule or disprove peak/end effects universally; Soul's placement remains a heuristic, not proof of human recall. See [From Experience to Memory](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2019.01705/full).

Then interrogate the shortlist:

1. Where would a generic execution actively hurt—cost trust, utility, or the story users tell?
2. Which beat is public-facing—screenshotted, demoed, shared, or judged by people who are not users yet?
3. Where does effort or uncertainty matter most, and what are the stakes if treatment gets it wrong?
4. Which beat carries the product's distinctive claim, and how often does it recur?
5. What will it cost to build and maintain, and what user evidence supports recall or repeat value?
6. What would marketing show? If nothing on the path is showable, that is the finding—not a reason to invent a novelty.

**Take up to three as Net-New, only when they clear the bar.** Zero, one, two, or three can be correct. If more than three appear necessary, the path is probably scoped too broadly or significance is being diffused; narrow the path or review distinct journeys separately rather than filling one sweep with peaks. Everything below the line takes **Elevated** where its ceiling allows craft that pays, and **Expected** otherwise—recorded either way, because the receipt separates restraint from neglect.

**Reasons a beat stays Expected** (any one suffices):
- **Load-bearing convention**—checkout, save, undo, back. Muscle memory is the feature; novelty there costs comprehension and pays nothing.
- **Every-run frequency with no supported repetition-proof lever available**—if speed, feel, feedback, and control are already at an acceptable ceiling, standard is correct; verify latency and failure behavior before claiming the ceiling.
- **High stakes, calm already present**—money movement, health data, and irreversible actions want reassurance and records before anything else. Where the calm, clear version already exists, standard is the treatment; where it does not, calm *is* the treatment (see proportionality in [treatments.md](treatments.md)). Trustworthy restraint is an emotional choice, not the absence of one.
- **Below the line**—a fine Net-New candidate that lost to a better one; it takes Elevated craft instead, and loses nothing but the rebuild. The cap is a budget, not a quota.

## The dumping grounds

The canonical list. These are where delight traditionally goes—chosen because failing there is cheap, which is exactly the problem: cheap failure means no reach, and no reach means the work is unseen or seen by a frustrated user at the worst possible moment.

- **404 and error pages**—reached by accident, read in annoyance. Audit them for respectful restraint and recovery, but do not select failure itself as a Net-New delight moment.
- **Error mascots and cheerful failure copy**—wit at the moment the user is most tense reads as mockery.
- **Easter eggs and hidden games**—found by almost nobody, by definition off every path.
- **Release notes bits**—read by a rounding error of the user base.
- **Splash-screen and loading-copy jokes on every-run loads**—novelty can decay into noise; if the wait is real, show the work and test the repeat experience instead.

**The two moves when the sweep finds delight in a dumping ground:**
1. **Relocate the effort.** The craft is real; the placement is wrong. Name the on-path beat that deserves it.
2. **Fix the frequency, not the feeling.** An error state frequent enough to be worth delighting is a bug to fix, not a moment to elevate—route it to [Flywheel](../../flywheel) (a leak) or [Focal](../../focal) (a screen).

One honest edge: a 404 that carries real traffic—dead links shared socially, a renamed content library—is not a dumping ground. It is an entry beat for those users. Treat it as recovery: state what happened, one clear path to the likely destination, zero jokes. The rule was never "404s don't matter"; it was "placement follows reach."
