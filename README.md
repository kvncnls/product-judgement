# Product Judgement

Skills for making better product decisions across the screen, the journey, the relationship, and the memory. The four foundational Skills—Focal, Compass, Flywheel, and Soul—each own a scale; Product Judgement combines them for holistic audits. The Skills are Markdown folders with no runtime build step or dependencies. Each also ships as a generated single-file bundle, so they work in Claude Code, Codex, ChatGPT, Cursor, and anything else that reads Markdown.

The umbrella is **coherence**: focused within a screen, navigable across a journey, valuable across the relationship, memorable after the experience, and trustworthy throughout.

## Quick install

Install all five Skills through your agent’s plugin system:

```bash
claude plugin marketplace add kvncnls/product-judgement && claude plugin install product-judgement@product-judgement
```

```bash
cursor-agent plugin marketplace add https://github.com/kvncnls/product-judgement
```

```bash
codex plugin marketplace add kvncnls/product-judgement && codex plugin add product-judgement@product-judgement
```

For Cursor, marketplace registration is the first step: open **Customize → Plugins**, select **Product Judgement**, choose **Install**, and select user or project scope.

Then ask for an audit: `audit this dashboard with Focal`, or `audit this app with Product Judgement`.

Using Claude Desktop, Claude.ai, ChatGPT, or another agent? See [Install](#install) for uploads, single-file bundles, project-scoped setups, and the script that covers everything else.

## Why this collection exists

Vibe coding made implementation fast and easy and made product judgement even easier to skip. Features accumulate, screens grow crowded, flows become mazes, value gets buried, and working products become generic and forgettable. The 'Ship fast, iterate later' mantra has produced AI product slop en masse.

These Skills put product judgement back in the loop. They encode principles, decision trees, failure modes, audit rubrics, exceptions, and fixed outputs for recurring UX problems—helping an AI reason about the experience as a connected system instead of generating one plausible screen at a time.

They complement design systems: design systems standardize how decisions are rendered; these Skills help decide which decisions should be made.

The four foundational Skills each own one scale: Focal sharpens the screen, Compass connects the journey, Flywheel strengthens the relationship, and Soul authors what gets remembered. They stay narrow so they can be combined when a problem crosses scales. **Product Judgement** is the holistic audit that runs all four, keeps their boundaries clear, and turns their findings into one prioritized sequence; it is not a fifth scale or an all-purpose product design system.

## What this repo is not

This is not a design-system analyzer, component library, token validator, visual-regression suite, renderer, prototyping tool, animation library, or implementation framework. It produces product-design judgement, audits, and fixed specifications—not production UI or animation code. Soul can identify where motion or expressive treatment earns its place; other tools implement it.

It is not context-free product wisdom. Because these Skills make product-design decisions, they work best with the context behind the decision: business goals, user intent, audience, constraints, stakes, the existing journey, and the evidence available. The more relevant context you provide, the more specific and useful the output; without it, the result is a hypothesis to validate, not a substitute for product knowledge.

It is not user research, analytics, experimentation, marketing, or product strategy. It can form hypotheses, locate leaks, and name a confirming test or metric, but it does not collect evidence, prove causality, buy attention, set roadmaps, or manufacture product-market fit. It is not a whole-app sitemap or all-purpose UX system, and it does not replace design-system, accessibility, security, legal, or safety reviews.

## Skills

| Skill | What it does | Reach for it when |
|-------|--------------|------------------|
| [**product-judgement**](./product-judgement) | Holistic audit. Runs all 4 Skills below against a shared evidence map, then reconciles their findings into one prioritized fix sequence. | The decisions span two or more scales, even within one flow, or related findings need a shared fix order. |
| [**focal**](./focal) | One screen, one clear intent. Declutters and structures app/dashboard screens through three disciplines—Information Architecture, Progressive Disclosure, and Visual Hierarchy. Its action model adapts to task, hub, and exploration screens. | A screen feels crowded, unclear, or unable to make its organizing intent and action model legible. Use it to decide what belongs, what waits, and what wins attention. |
| [**compass**](./compass) | Never lost. Guides multi-screen flows and navigation through three disciplines—Orientation, Path Economy, and Continuity. Build new flows or review existing ones. Pairs with Focal (single screens). | A task spans screens and users may be lost, facing too many steps, dead ends, retreat that resets or loses context, missing progress in a bounded flow, or lost state. |
| [**flywheel**](./flywheel) | Earn the next valuable step. Establishes the product's intended cadence and success outcome, then examines Trust, Friction, Wins, and Emotion. Diagnose where value is leaking, or design the stage that supports the relationship. | People struggle to trust, reach value, recognize value, or take the intended next step. Success can mean return or advocacy, or safe completion, handoff, and exit for a finite service. |
| [**soul**](./soul) | Never boring. Delight, placed: sorts every beat of the happy path into three tiers—Expected stays functional, Elevated adds craft to the small things, and up to three Net-New moments may be rebuilt entirely. Zero Net-New moments is valid when restraint is the better decision. | The happy path works but feels generic, forgettable, or over-designed. Use it to decide which moments stay conventional, gain craft, or become memorable—including where motion earns its place. |

## What each Skill returns

The four foundational Skills have two output modes. **Build** proposes a new design as a fixed specification with an unscored gate checklist. **Audit-style modes**—review, diagnose, or search—evaluate an existing artifact with scores for supported dimensions, prioritized findings, and a local methodology verdict. Unsupported dimensions are marked `N/E`. Product Judgement is audit-only: it preserves the four native scorecards and adds cross-scale prioritization without inventing a fifth score.

| Skill | Build output | Audit-style output | Local conclusion |
|---|---|---|---|
| [**Product Judgement**](./product-judgement) | — | **Holistic audit**—four native scorecards with evidence-backed component rationales, shared coverage, deduplicated cross-scale findings, and a prioritized list of changes with Screen · Flow · State · Lifecycle locators | Are the four scales coherent, and what should be fixed first? |
| [**Focal**](./focal) | **Screen Spec**—organizing intent, action model, information, disclosure, hierarchy, states, and gates | **Screen review**—three-discipline `/12` scorecard with per-discipline rationales, issues, up to three top moves, and structural/executional next steps, all located by Screen · Flow · State · Lifecycle | Does the screen satisfy **One Screen, One Clear Intent**? |
| [**Compass**](./compass) | **Flow Spec**—finite outcome or open-ended anchor, steps, cuts, orientation, continuity, and gates | **Flow review**—three-discipline `/12` scorecard with per-discipline rationales, issues, up to three top moves, and structural/executional next steps, all located by Screen · Flow · State · Lifecycle | Is the user **Never Lost**? |
| [**Flywheel**](./flywheel) | **Stage Spec**—first value, cadence, success outcome, relationship leak, design, applicable states and exits, friction kept, ask placement or refusal, and gates | **Diagnosis**—a full four-play scan with `/16` only when every play is evaluable, or one targeted `/4` stage review, with rationales, issues, the earliest evidenced relationship stage to fix, and what follows, all located by Screen · Flow · State · Lifecycle | Where does progress toward the intended outcome break down, if an evidenced leak exists? |
| [**Soul**](./soul) | **Moment Spec**—feeling, frequency, Expected/Elevated/Net-New target, applicable states, treatment ladder through that target, constraints, and gates | **Happy-path sweep**—an unscored Readiness verdict plus a three-gate `/12` scorecard, path map, up to three ranked Net-New moments, small things, and restraint receipt, all located by Screen · Flow · State · Lifecycle | Is the working path ready for authorship, and is its treatment memorable without becoming misplaced or exhausting? |

For Flywheel, a **leak** is an evidenced loss of progress toward the intended outcome: people may leave before reaching value, fail to recognize value, or stop returning when recurring use serves their goal. Judge this against the product's cadence. A finite or infrequent service can succeed through safe completion, handoff, and exit; lack of return alone is not a leak.

## Shared audit contract

Build outputs are proposals, so their gates remain unscored. Mark a gate pass, fail, or N/A with a reason; identify the states that apply to the proposed interaction. Audit-style outputs evaluate something that already exists, so every evaluated local dimension receives an integer score from `0–4`:

| Score | Canonical label | Shared meaning |
|---:|---|---|
| **0** | **Broken or harmful** | The dimension fails outright, blocks its core outcome, actively inverts the intended behavior, or creates material harm. |
| **1** | **Major failure** | The outcome may remain technically possible, but the dimension is seriously compromised, unreliable, or largely absent. Substantial correction is required. |
| **2** | **Partial or inconsistent** | The basic function exists, with a material weakness, missing decision, or inconsistency that prevents dependable quality. |
| **3** | **Strong** | Deliberate, dependable, context-appropriate professional work with only minor gaps. This is the normal target for good execution. |
| **4** | **Exemplary—above and beyond** | Fully realized and unusually effective for the relevant context, including realistic states and constraints. This is intentionally uncommon, not the normal target. |

These are ordinal quality levels, not percentages or school grades. A `3/4` is the intended bar for strong product work; it does **not** mean 75%. Scoring every dimension Strong produces `9/12` for Focal, Compass, or Soul, or `12/16` for a full Flywheel diagnosis. Those totals alone do not establish that profile: `4 + 4 + 1` also produces `9/12`, while exposing a major failure. Read the component scores and apply the weakest-dimension ceiling below. A `4/4` recognizes a specific, unusually effective quality supported by the evidence; meeting ordinary requirements does not automatically earn it.

Do not optimize every audit toward a perfect total. Eliminate `0`s and `1`s, improve consequential `2`s, establish `3` as the dependable baseline, then pursue selected `4`s only where deeper investment supports the product's goals or creates meaningful differentiation. Scores describe the quality profile; they do not decide release readiness by themselves. A P0 or explicit blocker still requires action regardless of the total.

When all required dimensions are evaluable, the scorecard keeps each foundational Skill's native total—`/12` for Focal, Compass, and Soul, and `/16` for a complete Flywheel diagnosis—and displays `total ÷ required dimensions` as a normalized `/4` average rounded to one decimal place. A targeted Flywheel stage review reports one `/4` score and marks the other plays `N/E—outside targeted scope`; a full diagnosis marks a play whose rubric is unsupported `N/E—insufficient evidence`. Neither case invents a `/16` total. Product Judgement preserves native totals and does not average them into a misleading collection-wide score.

| Common band | Average | `/12` total | `/16` total |
|---|---:|---:|---:|
| **Broken** | `≤ 1.5` | `0–4` | `0–6` |
| **Significant rework** | `> 1.5` and `< 2.5` | `5–7` | `7–9` |
| **Solid** | `≥ 2.5` and `< 3.5` | `8–10` | `10–13` |
| **Excellent** | `≥ 3.5` | `11–12` | `14–16` |

For complete scorecards, the weakest dimension then caps the overall quality band: a lowest score of `0` caps it at **Broken**, `1` at **Significant rework**, `2` at **Solid**, and `3–4` adds no ceiling. This prevents a high total from hiding one failed dimension.

`N/E` means **not evaluated**, not zero. Any dimension whose rubric cannot be supported by the available evidence uses `N/E—insufficient evidence`. A missing variant does not automatically invalidate an otherwise supported dimension. Targeted reviews may mark other plays `N/E—outside targeted scope`; a scale whose Skill is not installed alongside Product Judgement uses `N/E—Skill not installed`. When any required dimension is unevaluable, report supported findings and the evidence check, but no native total, average, common band, or weakest-dimension ceiling. Do not turn unknown behavior into a defect or an implementation recommendation.

### Scores must explain themselves

A score without an explanation is invalid. Every scorecard row must show the chain **evidence → consequence → rubric anchor → next-point change**:

- **Evidence**—what was observed, inferred, tested, walked, or measured, anchored to the relevant surface or transition, app state, and lifecycle moment.
- **Consequence**—what that condition costs the user or product in the Skill's terms.
- **Rubric anchor**—why the evidence earns this integer. A `2` says what works and names the material weakness; a `3` names a supported remaining gap or says `None justified by the evidence`; a `4` identifies what makes the dimension unusually effective.
- **Next-point change**—the smallest supported improvement or evidence check needed to establish the next score. A strong `3` may say `None justified by the evidence`; do not invent a flaw or extra work to pursue `4`. A `4` says `None—already exemplary.`

Do not award credit for behavior the artifact does not expose, and do not turn an unseen state into a failure without a rubric basis. Mark it `not shown` in Coverage/Basis and name the validating check. The total is the exact sum of the justified component scores; never derive component scores from the total.

`Focal 7/12` is therefore incomplete. A valid result must show something like: `Information Architecture 2/4`—the screen groups the core content but leaves two independent jobs resident, so the user still sorts competing outcomes; split or demote one job to reach 3. `Progressive Disclosure 2/4`—the primary facts are visible but secondary history loads at full depth; cap the default and defer the rest to reach 3. `Visual Hierarchy 3/4`—the rendered screen gives the primary action clear emphasis and keeps supporting content legible, so the next action is easy to identify; this is dependable hierarchy, with no unusually effective quality evidenced to justify 4; next-point change: `None justified by the evidence`. Then report **7/12 · 2.3/4 · Significant rework**.

Five concepts remain separate in every audit:

- **Dimension score**—quality within one Skill-specific discipline, play, or gate.
- **Overall quality band**—the lower of the average-derived band and weakest-dimension ceiling.
- **Issue severity**—P0 Critical, P1 Major, P2 Moderate, or P3 Minor, assigned from consequence, reach, and recoverability.
- **Blocker**—an explicit release-critical condition; every P0 is a blocker, but a blocker does not automatically rewrite a score to `0`, and a score of `0` does not automatically imply P0.
- **Local verdict**—the Skill's own north-star conclusion, evaluated independently from the common band.

### Issue severity

| Priority | Meaning |
|----------|---------|
| **P0 — Critical** | Blocks the core outcome; traps the user; destroys work or state; causes or risks material harm; hides material cost, consequence, permission, or risk; removes informed choice; or uses coercive manipulation. Fix before release. |
| **P1 — Major** | Materially damages comprehension, completion, orientation, trust, value realization, or return for a meaningful share of users. Fix before release. |
| **P2 — Moderate** | Creates real friction, confusion, dilution, or missed value with a viable recovery, workaround, or limited scope. Fix in the next planned pass. |
| **P3 — Minor** | Low-impact craft, consistency, or polish. Fix when time permits. |

Assign severity from consequence, reach, and recoverability. A methodology rule violation is not automatically P0.

Every audit declares **Coverage** with a four-part implementation locator: **Screen** (the exact UI surface), **Flow** (the named journey or transition, or `screen-local`), **State** (the exact rendered or system condition), and **Lifecycle** (the exact user/product moment). Every issue, top move, Next item, handoff, and Product Judgement priority change carries the same four fields, so the reader can open the right place and reproduce how and when the condition occurs. Here, lifecycle means the user's journey or relationship with the product (first run, pre-value activation, recurring use, interruption/resume, re-entry, lapse), not a software release phase. Never use only `the dashboard` or `onboarding`; if a field is not evidenced, write `not shown` and name the validating check instead of inventing behavior.

Every audit also states its evidence **Basis** and the fastest test, behavior, or metric that would confirm its most consequential uncertain claim.

## How to use

Designers and developers can use these Skills from a codebase, Figma, Paper, a clickable prototype, screenshots, or a product description. Point the LLM at the artifact and name the scale you want it to inspect.

The slash-command examples below use **Claude Code folder installs**. With the Claude Code plugin, prefix the Skill name with `product-judgement:`, for example `/product-judgement:focal` or `/product-judgement:product-judgement`. In other agents, ask for the Skill by name or use the agent's own picker or invocation syntax.

### From Figma or Paper

Point at one frame when using Focal:

```text
/focal audit this dashboard
```

For Compass, select the screens in order—including branches and important variants—and say which frames form the flow:

```text
/compass audit this flow
```

You can also ask Flywheel to inspect the relationship represented by the frames, or Soul to sweep the happy path:

```text
/flywheel audit this onboarding flow
/soul audit the happy path
```

Frames show visible structure and selected transitions well, but they do not prove persistence, validation, timing, or lifecycle behavior. Include loading, empty, error, success, permission, interruption, and re-entry states when they exist; otherwise the audit will mark them `not shown`.

### From the codebase (recommended)

The codebase usually contains more context than Figma or Paper: routes, state transitions, persistence, validation, copy, error handling, and the actual lifecycle of the product. Run the Skills from the project so the LLM can inspect that context:

```text
/focal audit the dashboard
/compass audit the onboarding flow
/flywheel audit the onboarding flow
/soul audit the happy path
```

When the decisions span two or more scales, even within one flow, use the holistic Skill:

```text
/product-judgement audit the app
```

A full Product Judgement audit runs all four foundational Skills, keeps their ownership distinct, and returns the native scorecards plus a deduplicated issue ledger, a prioritized list of changes with dependencies, and a validation plan. A partial audit can proceed with at least two available scales, marking missing Skill rows `N/E—Skill not installed` and reconciliation provisional. With fewer than two, it offers the available local review. Focal owns the screen, Compass the path, Flywheel the relationship, and Soul the memory.

Give the Skills the surrounding product context as well. Attach or point the LLM at the PRD (Product Requirements Document), product brief, strategy or goal documents, user research, personas, journey maps, analytics or funnel data, support themes, experiment history, and technical, accessibility, legal, or safety constraints. The more relevant context you provide, the better the Skills can judge whether a design serves a real user, goal, and constraint instead of only reacting to what is visible. When context is missing, the Skills state their assumptions instead of presenting them as facts.

## Install

Each Skill is a folder with a `SKILL.md` at its root, which is the shape Claude Code, Cursor, Codex, and Gemini CLI all read. Pick the row that matches where you work.

| Environment | How it installs | Invocation |
|---|---|---|
| Claude Code, Cursor, Codex | Plugin, from this repository | Ask for the Skill by name; Claude Code also supports `/product-judgement:focal`, etc. |
| Claude Desktop, Claude.ai | Upload a Skill `.zip` | Ask for the Skill by name |
| ChatGPT, custom GPTs | Upload the combined Markdown bundle | Ask for the Skill by name |
| Anything else, or a project-scoped setup | `scripts/install.sh` | Ask for the Skill by name or use the agent’s Skill picker |

### Claude Code, Cursor, and Codex

These three read a plugin manifest from this repository, so installation is one marketplace and one plugin. Claude Code and Cursor share `.claude-plugin/`; Codex reads `.agents/plugins/` and `.codex-plugin/`.

Claude Code:

```bash
claude plugin marketplace add kvncnls/product-judgement
claude plugin install product-judgement@product-judgement
```

Cursor:

```bash
cursor-agent plugin marketplace add https://github.com/kvncnls/product-judgement
```

Codex:

```bash
codex plugin marketplace add kvncnls/product-judgement
codex plugin add product-judgement@product-judgement
```

In Claude Code, the equivalent session commands are `/plugin marketplace add kvncnls/product-judgement` and `/plugin install`. In Cursor, open **Customize → Plugins**, select **Product Judgement**, choose **Install**, then choose user or project scope after registering the marketplace. Confirm that the plugin lists all five Skills. See [Cursor’s plugin instructions](https://prod.cursor.com/docs/plugins) for the current UI.

In Claude Code, plugin Skills use namespaced commands such as `/product-judgement:focal`. Folder installs use bare Skill names such as `/focal`. Other agents expose their own picker or invocation syntax; asking for Focal by name also makes the intended lens clear. Use [the install script](#any-other-agent-or-a-project-scoped-install) for folder installs.

Update or remove an installed plugin with its own tooling:

```bash
claude plugin update product-judgement
codex plugin marketplace upgrade product-judgement
cursor-agent plugin marketplace update product-judgement
```

### Claude Desktop and Claude.ai

Claude.ai takes a Skill as a `.zip` whose root is the Skill folder. Follow the [upload package instructions](./CONTRIBUTING.md#building-upload-packages) to build verified ZIPs from this checkout.

The published `v1.0.0` ZIPs predate the frontmatter compatibility fix. Do not use those archives for uploads. A newer release must pass the archive checks before replacing this source-build recommendation.

Enable **Code execution and file creation** in Settings → Capabilities, then upload the `.zip` under Settings → Capabilities → Skills. Repeat for each Skill you want. A holistic `/product-judgement` audit needs all five, because the orchestration Skill calls the four local methodologies.

### ChatGPT, custom GPTs, and other single-file environments

Some tools accept only one Markdown file. [`bundles/all.md`](./bundles/all.md) is the whole collection—all five Skills, generated from the same sources—in one file, which is what a holistic audit needs:

```bash
cp bundles/all.md ~/Desktop/product-judgement.md
```

Upload it as a ChatGPT Project or custom GPT knowledge file, or attach it to a Claude Project. For a single Skill, upload its own bundle, such as `bundles/focal.md`, and ask for that Skill when needed. Prefer native Skill installation when supported so references load only for the selected mode. Avoid appending a full bundle to `AGENTS.md` or another always-loaded rules file: doing so loads the methodology on unrelated requests and removes progressive disclosure.

### Any other agent, or a project-scoped install

`scripts/install.sh` symlinks the Skill folders into whichever agents it finds, with no Node and no build step. Because the links point back at your clone, `git pull` updates every agent at once.

```bash
git clone https://github.com/kvncnls/product-judgement.git
cd product-judgement
./scripts/install.sh
```

It targets Claude Code, Cursor, Codex, Gemini CLI, and opencode, and installs the bare Skill folders. Useful variations:

```bash
./scripts/install.sh --agent claude --agent cursor   # only these agents
./scripts/install.sh --skill focal --skill compass   # only these Skills
./scripts/install.sh --scope project                 # into ./.claude/skills and friends
./scripts/install.sh --copy                          # independent copies, not symlinks
./scripts/install.sh --list                          # print target directories, change nothing
./scripts/install.sh --uninstall                     # remove recognized installations
```

The installer recognizes any symlink resolving exactly to a Skill in this checkout as an installation, including a link you created manually. It replaces or removes those links and unchanged copies carrying its provenance marker. It stages replacements and checks copy integrity before switching. Unknown entries, older unmarked copies, and customized copies are preserved with an explanation. If one conflicts, move it to a backup location you choose, review any customizations, and rerun; the installer does not delete it for you. A failed or interrupted replacement restores the original when possible or reports the retained rollback path.

OpenCode user installs go to `~/.config/opencode/skills`; project installs use `.opencode/skills` inside the project root.

Run `./scripts/install.sh --help` for the full set. Restart your agent afterwards so it reloads Skill metadata.

To wire up an agent by hand, link each Skill folder into that agent's Skill directory. The common global locations are `~/.claude/skills/` for Claude Code, `~/.cursor/skills/` for Cursor, and `~/.agents/skills/` for Codex, which also reads a repository's `.agents/skills/`:

```bash
ln -s "$(pwd)/focal" ~/.claude/skills/focal
```

Consult the agent's current documentation, because discovery paths change.

### Skills CLI

The [Skills CLI](https://skills.sh/docs/cli) is an alternative that keeps one canonical copy and links supported agents to it. It requires Node and pnpm **11 or newer** for the `dlx` examples below: this is the first pnpm version whose [dlx execution respects project release-age policy](https://pnpm.io/cli/dlx#security-and-trust-policies). Run these commands from this checkout, whose `pnpm-workspace.yaml` requires `minimumReleaseAge: 1440` (24 hours). Preserve any stricter policy in your own environment.

```bash
pnpm dlx skills add kvncnls/product-judgement --skill '*' -g -a claude-code -a codex -a cursor -y
```

Run `pnpm dlx skills add kvncnls/product-judgement` to be asked which Skills, agents, and scope you want, or name one Skill directly:

```bash
pnpm dlx skills add kvncnls/product-judgement --skill focal -g
```

Check for upstream changes with `pnpm dlx skills check`, then update this collection's five globally installed Skills:

```bash
pnpm dlx skills update -g product-judgement focal compass flywheel soul
```

Rerun the full `skills add` command when an update reports a failure, when a new Skill is added to the repository, when an agent link is missing, or when an installation predates the CLI lock record. Use `pnpm dlx skills list -g` to inspect what is installed.

## Contributing

Issues and pull requests are welcome. A change should sharpen one Skill's ownership of its own scale rather than broaden it: Focal owns the screen, Compass the path, Flywheel the relationship, Soul authored memory, and Product Judgement only the reconciliation between them.

The installed Skills stay pure Markdown and have no runtime build step. See [the contributor guide](./CONTRIBUTING.md) for maintainer setup, verification, bundle generation, and releases.

## License

[MIT](./LICENSE) © 2026 Kevin Canlas.
