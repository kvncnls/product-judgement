# Behavioral contracts

[`behavioral-contracts.yml`](./behavioral-contracts.yml) contains representative prompts and evidence conditions that guard the collection’s decision boundaries. Each fixture states behavior an agent should produce and behavior it must reject.

Two harnesses cover this repository, and the boundary between them matters. [`scripts/verify.rb`](../scripts/verify.rb) guards **text**: frontmatter, links, the cross-file identity of the shared audit contract, the plugin manifests, and exact bundle synchronization. It is free, runs on every push, and catches deletion and drift. [`scripts/eval.rb`](../scripts/eval.rb) guards **behavior**: it runs each fixture against a model and grades the result. It costs real tokens, so it is opt-in and never runs in CI. Do not move an assertion a string match can hold into the expensive harness.

## Running the fixtures

```bash
ruby scripts/eval.rb --dry-run
```

`--dry-run` renders every prompt, resolves every argv, self-checks the excerpt verifier, and spends nothing. Run it first, every time. A real pass adds the baseline arm:

```bash
ruby scripts/eval.rb --ablation --repeat 3
```

`--ablation` is the option that decides whether the suite means anything. It runs each fixture a second time with the Skills unloaded; a fixture that passes in both arms is reported **NO SIGNAL**, because it is measuring the base model rather than these 30,000 words. Run it.

`scripts/eval.rb --help` lists the rest. The unit of measurement is `(fixture, assertion)` and the number is always `k/N` — the runner is non-deterministic, with no temperature or seed available, so a per-fixture boolean is a number the harness cannot honestly produce.

Exit codes separate what was learned from what was not: `0` green, `1` a behavioral regression, `2` a harness or runner error (auth, timeout, budget — meaning nothing was learned), `3` no fixture matched the filters, `4` a fixture-quality failure only, such as NO SIGNAL or a judge-control leak.

## What these fixtures do not cover

Read this before treating a green run as coverage.

- **Roughly a dozen decision boundaries out of hundreds.** Untested: every rubric anchor at 0, 1, and 2; all four build modes; `patterns.md`, `moments.md`, `treatments.md`, and the four Flywheel play references; the routing tables. Green means "the boundaries we thought of still hold".
- **The default mode skips the most common real failure.** `--invoke slash` hands the model the Skill. In production a Skill fires, or fails to, off its `description`. `--invoke auto` tests that, at higher variance and cost.
- **`--repeat 3` is underpowered.** A regression that fails 20% of the time reads as PASS about half the time at N=3. It catches gross regressions and is blind to drift.
- **The judge is a model, and its agreement with a human is unmeasured.** Excerpt verification catches fabricated quotes, not misreading. `--calibrate` grades hand-labeled transcripts in `tests/judge-calibration/` when that directory exists.
- **One CLI, one model.** The collection also ships as `bundles/all.md` for ChatGPT Projects and custom GPTs — the artifact where progressive disclosure collapses into one flat file, and the one this harness never exercises.
- **It scores compliance, not craft.** Every assertion is a boundary. A transcript can satisfy all of them and still be a vague, generic, useless audit. Nothing in this repository guards whether the output is worth reading.
- **Being opt-in means it will rarely run, and its existence is not coverage.** Record the last real run below and let it visibly go stale.

## Last full run

Never run. `--ablation` has not been executed against this fixture set, so no fixture here is yet known to depend on the Skills rather than on the base model.

## What the fixtures concentrate on

- contextual Focal density instead of a hard item quota;
- finite and open-ended Compass journeys, and an indicator bound to flow type;
- platform-appropriate retreat behavior;
- targeted versus full Flywheel scoring;
- Soul restraint, Readiness, and zero-Net-New outcomes;
- the orchestrated pass: each local Skill suppressing its own locked template while preserving its scores;
- Product Judgement cross-scale deduplication, a missing sibling Skill, and skipping the local calibration reads;
- the intentionally uncommon `4/4` threshold.
