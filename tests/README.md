# Behavioral contracts

[`behavioral-contracts.yml`](./behavioral-contracts.yml) contains representative prompts and evidence conditions that guard the collection’s decision boundaries. Each fixture states behavior an agent should produce and behavior it must reject.

Two harnesses cover this repository, and the boundary between them matters. [`scripts/verify.py`](../scripts/verify.py) guards **text**: frontmatter, links, the cross-file identity of the shared audit contract, the plugin manifests, and exact bundle synchronization. It is free, runs on every push, and catches deletion and drift. [`scripts/eval.py`](../scripts/eval.py) guards **behavior**: it runs each fixture against a model and grades the result. It costs real tokens, so it is opt-in and never runs in CI. Do not move an assertion a string match can hold into the expensive harness.

## Running the fixtures

Complete the [maintainer setup](../CONTRIBUTING.md#setup) first.

```bash
uv run scripts/eval.py --dry-run
```

`--dry-run` renders every audit and build prompt, resolves every argv, checks the excerpt verifier, verifies the namespaced invocation and ablation body, and checks that expected/reject text is withheld. It spends nothing. Run it first, every time. A real pass adds the baseline arm:

```bash
uv run scripts/eval.py --ablation --repeat 3
```

`--ablation` is the option that decides whether the suite means anything. It runs each fixture a second time with the Skills unloaded; a fixture that passes in both arms is reported **NO SIGNAL**, because it is measuring the base model rather than these instructions. Use `--id` for a bounded representative run before attempting a larger sample.

`scripts/eval.py --help` lists the rest. The unit of measurement is `(fixture, assertion)` and the number is always `k/N` — the runner is non-deterministic, with no temperature or seed available, so a per-fixture boolean is a number the harness cannot honestly produce.

Exit codes separate what was learned from what was not: `0` green, `1` a behavioral regression, `2` a harness or runner error (auth, timeout, budget — meaning nothing was learned), `3` no fixture matched the filters, `4` a fixture-quality failure only, such as NO SIGNAL or a judge-control leak.

## What these fixtures do not cover

Read this before treating a green run as coverage.

- **Twenty-eight fixture scenarios out of hundreds of possible boundaries.** The set now includes static evidence gaps, named finite progress without numeric counters, finite user-chosen task lists, safe sensitive resume, contextual expert density, Soul moment selection, one-flow cross-scale routing, infrequent-service exits, and one representative build for each local Skill. It still does not cover every rubric anchor, reference, routing branch, or content shape. Green means "the boundaries we thought of still hold".
- **The default mode skips the most common real failure.** `--invoke slash` hands the model the Skill. In production a Skill fires, or fails to, off its `description`. `--invoke auto` tests that, at higher variance and cost.
- **`--repeat 3` is underpowered.** A regression that fails 20% of the time reads as PASS about half the time at N=3. It catches gross regressions and is blind to drift.
- **The judge is a model, and its agreement with a human is unmeasured.** Excerpt verification catches fabricated quotes, not misreading. `--calibrate` grades hand-labeled transcripts in `tests/judge-calibration/` when that directory exists.
- **One CLI, one model.** The collection also ships as `bundles/all.md` for ChatGPT Projects and custom GPTs — the artifact where progressive disclosure collapses into one flat file, and the one this harness never exercises.
- **Usefulness is only a model-judged proxy.** Several assertions now require a situated locator, concrete evidence-to-consequence fix, preserved context or protection, and a named tradeoff. Those checks reject generic slogans, but they do not establish human usefulness, craft quality, or that a real team would act on the recommendation.
- **Being opt-in means it will rarely run, and its existence is not coverage.** Record the last real run below and let it visibly go stale.

## Last full run

No complete CLI ablation has finished. A bounded attempt on 2026-09-05 UTC stopped during provenance preflight because the local Claude OAuth session had expired. It produced no behavioral grades. A separate fresh-agent comparison and its limits are recorded in [the remediation validation note](validation-2026-09-05.md); it is not a completed CLI suite or human calibration.

## What the fixtures concentrate on

- contextual Focal density instead of a hard item quota, including an expert row with more than eight needed facts;
- finite and open-ended Compass journeys, named stages without a numeric counter, user-chosen task order, final submit, and conditional sensitive resume;
- platform-appropriate retreat behavior and evidence-bounded missing states;
- targeted versus full Flywheel scoring;
- Soul restraint, Readiness, contextual early-versus-late moment selection, and zero-Net-New outcomes;
- success and clean exit for an infrequent finite service without manufactured retention;
- applicable completion, partial-failure, permission, and interruption/recovery states in representative builds for Focal, Compass, Flywheel, and Soul;
- candidate prompt isolation: the mode and evidence reach the candidate, while grading assertions stay with the judge;
- the orchestrated pass: each local Skill suppressing its own locked template while preserving its scores;
- Product Judgement cross-scale routing and deduplication, a missing sibling Skill, and skipping the local calibration reads;
- the intentionally uncommon `4/4` threshold.
