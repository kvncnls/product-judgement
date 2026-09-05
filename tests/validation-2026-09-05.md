# Remediation validation, 2026-09-05 UTC

This note records the installation and UX-instruction repairs made on `main`, based on `a79cce0`, before publication. Six implementation subagents covered the installer, Focal, Compass, Flywheel, Soul, and evaluation harness. Separate subagents performed installation safety review and fresh behavioral samples; integration, shared contracts, packaging, and the conclusions below were handled in the main task.

The repository changes and generated packages are local. Version `1.1.0` is prepared in the four versioned manifests. No commit, tag, release, or global Skill installation was made. The published `v1.0.0` archives remain old; the README now directs upload users to build and verify current source packages until a corrected release is published.

## Changes covered

| Audit finding | Remediation and evidence boundary |
|---|---|
| I1: installer deletes unrelated or customized content | Strict Skill/agent allowlists, canonical-link recognition, provenance and content checks for copies, staged replacement, rollback, source checks, and regression tests. Exact source links are recognized even when manually created; unknown or modified directories are preserved. |
| I2: incompatible published archives | Version prepared, actual ZIP validator and negative tests added, and release workflow validates its archives. Local packages are checked against current source. Publication remains outstanding. |
| I3–I4: installation instructions and discovery path | Cursor registration is followed by plugin selection, Install, scope, and five-Skill verification. OpenCode's user path is corrected to `~/.config/opencode/skills`. No authenticated Cursor or live OpenCode discovery test was performed during these repairs. |
| U1: unsupported scores | Every dimension can be N/E. Incomplete scorecards omit aggregate totals and bands. Negative anchors need observed evidence; positive anchors also need the dimension's essential evidence. Missing variants remain coverage gaps when enough evidence otherwise exists. |
| U2–U3: universal density and memory rules | Focal judges density by task, expertise, grouping, and decision relevance. Soul treats peak/end and later-beat preferences as contextual hypotheses; fast responses still need understandable feedback. |
| U4–U6: routing, task lists, persistence | The umbrella routes by requested decisions, including cross-scale work in one flow. Compass supports finite task-list journeys and conditional safe retention, expiry, revalidation, and recovery. |
| U7–U8: state coverage and prescribed widgets | Mode-specific build templates carry applicable completion, partial failure, permission, and recovery states. Compass judges understandable progress and position rather than requiring numeric counters. |
| Flywheel refinements | Intended cadence and successful completion/exit precede retention judgments. Voluntary value, portability, declining an ask, and protective friction remain explicit. |
| Q1: behavior assurance | Expanded to 28 scenarios, including four build scenarios, producing 31 Skill-specific rows. Prompt-isolation, namespaced invocation, baseline parity, and utility assertions were added. Small fresh-agent comparisons were run; a complete CLI comparison and human calibration are still outstanding. |
| Q2: mandatory instruction volume | Build templates moved to conditional references; shared evidence, score anchors, and severity fragments have one maintained source with generated standalone copies. Bundles deduplicate shared fragments and rewrite internal links. |

## Deterministic checks

Local checks use macOS system Ruby `2.6.10`. CI is configured to run source, installer, and archive tests on Linux Ruby `3.3` and macOS system Ruby; a remote CI run has not been started by this task.

- Package tests accept all complete archives and reject unsupported upload metadata, changed Skill instructions, and a missing license.
- Actual package validation checks all five individual ZIPs and the combined ZIP for the complete source file set, source-equivalent instructions, and spec-compatible frontmatter.
- All four versioned manifests agree on `1.1.0`.
- Evaluation dry-run passes the excerpt-verifier and candidate-prompt-isolation checks for all 31 rows. It makes no model calls and produces no behavioral grades.
- `ruby scripts/verify.rb` passes for five Skills, 36 Markdown source files, synchronized shared contracts, generated bundles, manifests, fixture structure, and score arithmetic.
- Claude Code validates both the plugin and marketplace manifests.
- Installer regression suite: **20 tests, 20 passed, 0 failures**. It covers all-five-Skill link lifecycle, copy updates, unowned/customized preservation, traversal and alias rejection, failed staging and final moves, concurrent destination directories/symlinks, edits during staging and backup, interruption, unsafe source symlinks, and the OpenCode user path. All writes use temporary project roots.
- Source verification excludes generated downloads and ignored evaluation outputs so its source checks remain reproducible after local evaluation runs.

## CLI behavioral attempt

The following bounded with/without-Skill comparison was attempted:

```bash
ruby scripts/eval.rb --ablation --repeat 1 \
  --id compass-static-three-stage-checkout \
  --id focal-dense-expert-row \
  --id focal-build-applicable-states \
  --max-cost-usd 5 \
  --out tests/results/remediation-2026-09-05
```

The configured candidate was `claude-sonnet-4-5-20250929` and the judge was `claude-haiku-4-5-20251001`, using Claude Code `2.1.251`. The candidate calls stopped in working-tree provenance preflight because the local OAuth session had expired and could not be refreshed. The process exited `2`; no fixture was graded. This is a runner failure, not a failed Skill and not a passing evaluation. The harness now records failed preflight details and distinguishes runner errors from source-provenance ambiguity.

After restoring the CLI session, rerun the dry-run and bounded command with a fresh output directory before expanding the suite. Do not remove or overwrite global Skills merely to force a provenance probe to succeed.

## Fresh-agent comparison

Fresh Luna workers received the same three scenario/evidence prompts, without grading assertions: a static checkout with named stages, a daily expert row with ten decision-relevant facts, and an invoice-upload build with completion, partial acceptance, denied permission, and interruption recovery. The baseline worker was given no Skill files. The Skill worker loaded the requested Focal or Compass entrypoint and mode references. They were instructed not to read earlier outputs, audit notes, fixtures' expected/reject assertions, or memories.

The baseline and Skill outputs both accepted named progress without a numeric counter, preserved needed expert facts, and covered the supplied upload states. These shared successes do not establish an advantage from the Skills. The Skill output added the native structure, evidence scopes, and explicit unevaluable dimensions.

The first Skill sample also exposed a false negative: Compass used unshown retreat behavior to justify Orientation `2/4`. A procedural evidence rule was added, and a new worker reran the two audit cases. That sample stopped penalizing the unknown behavior and omitted incomplete totals, but still assigned positive Compass scores to incompletely evidenced dimensions. It also gave Focal `4/4` for ordinary correct structure. The local rubrics were then clarified: Compass identifies the essential evidence for each discipline; Focal's `3` covers ordinary appropriate organization and layering without requiring a flaw, while `4` must explain a specific benefit beyond that baseline. The post-guard worker confirmed from its tool history that it read repository files, including some additional build/pattern references; relevant truncated reads were reread separately.

One attempted final sample loaded the installed `1.0.0` plugin cache instead of the edited checkout. Its file-path provenance was confirmed after the mismatch was noticed in quoted rubric language. That output is excluded from evidence about these repairs. The replacement final sample receives exact absolute checkout paths and records source hashes before generating its answers. This is why a response that looks like a Skill audit is insufficient proof that it used the version under test.

The final checkout Compass sample marked all three unsupported journey dimensions N/E, retained the valid named stepper, and proposed evidence checks without an invented implementation defect or aggregate score. In that same run, Focal still treated an intended action role as visual evidence and reclassified the explicitly task-oriented queue as a hub. Those two boundaries were made explicit in the Focal entrypoint/review and fixture assertions. A final fresh Focal sample kept the task register, scored IA and Progressive Disclosure `3/4`, marked Visual Hierarchy N/E, and omitted the aggregate and invented fixes. The three Compass source hashes and three final Focal source hashes recorded by the workers match the respective current checkout files.

These are single outputs per arm, followed by deliberately targeted regression samples. They use description-based evidence and one model family. The main agent interpreted the results with knowledge of which arm used Skills. They are neither a blind human assessment nor the isolated CLI ablation. No pass rate, statistical reliability, improvement in real product outcomes, or universal score calibration is established. The upload build was not resampled after audit-only rubric changes. Flywheel, Soul, umbrella auto-routing, and uploaded single-file bundles were not exercised in this comparison.

Raw prompts and outputs are kept locally under `tests/results/independent-remediation-2026-09-05/`, which is intentionally ignored by Git. The input file `cases.json` has SHA-256 `c7661bbf279ed7829c2224c6fd9a1b7e6c4c5283748f2a100e4f2955d25b71a0`; candidate-facing evidence stayed unchanged across these samples. This checked-in note preserves the outcome and limitations without claiming the raw transcripts are shipped with the repository.

## Instruction volume

Counts use whitespace-delimited words, including frontmatter, tables, and templates, against the original `a79cce0` tree. They measure reading volume, not model tokens or quality. The five entrypoints fell from 18,533 to 8,773 words (52.7%). The mandatory holistic read (five entrypoints plus four review contracts) fell from 31,460 to 23,165 words (26.4%), and the combined bundle fell from 51,639 to 45,143 words (12.6%). Build references remain complete for build requests and are still included in single-file bundles, where conditional file loading is unavailable.

## Final integration results

All local source, shared-contract, bundle, plugin-manifest, package, installer, and dry-run checks passed after integration. The installer review additionally caught final-move races and nested source links; the implementation now requires no-clobber/no-follow move support, verifies the exact staged destination before discarding the original, rechecks backup integrity, and preserves a reported backup when concurrent data prevents restoration. A copy also validates links against its staged tree, keeping it independent of the original checkout.

Thirteen subagents participated: six initial implementation workers and seven validation workers, including the excluded stale-plugin sample. The final checkout-specific Compass and Focal samples demonstrate the repaired boundaries in those cases. They do not establish general effectiveness. The full CLI comparison, human calibration, authenticated upload/discovery checks, remote CI execution, release publication, and updating installed copies remain outstanding.
