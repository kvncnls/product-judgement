# Product Judgement

Skills for making better product decisions across the screen, the journey, the relationship, and the memory. The four foundational Skills—Focal, Compass, Flywheel, and Soul—each own a scale; Product Judgement combines them for holistic audits. The Skills are Markdown folders with no runtime build step or dependencies. Each also ships as a generated single-file bundle, so they work in Claude Code, Codex, ChatGPT, Cursor, and anything else that reads Markdown.

The umbrella is **coherence**: focused within a screen, navigable across a journey, valuable across the relationship, memorable after the experience, and trustworthy throughout.

## Quick install

All five Skills, in one command, on the agent you already use:

```bash
claude plugin marketplace add kvncnls/product-judgement && claude plugin install product-judgement@product-judgement
```

```bash
cursor-agent plugin marketplace add https://github.com/kvncnls/product-judgement
```

```bash
codex plugin marketplace add kvncnls/product-judgement && codex plugin add product-judgement@product-judgement
```

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
| [**product-judgement**](./product-judgement) | Holistic audit. Runs all 4 Skills below against a shared evidence map, then reconciles their findings into one prioritized fix sequence. | The question spans the app, or several Skills identify related issues and you need to decide what to fix first. |
| [**focal**](./focal) | One screen, one clear intent. Declutters and structures app/dashboard screens through three disciplines—Information Architecture, Progressive Disclosure, and Visual Hierarchy. Its action model adapts to task, hub, and exploration screens. | A screen feels crowded, unclear, or unable to make its organizing intent and action model legible. Use it to decide what belongs, what waits, and what wins attention. |
| [**compass**](./compass) | Never lost. Guides multi-screen flows and navigation through three disciplines—Orientation, Path Economy, and Continuity. Build new flows or review existing ones. Pairs with Focal (single screens). | A task spans screens and users may be lost, facing too many steps, dead ends, retreat that resets or loses context, missing progress in a bounded flow, or lost state. |
| [**flywheel**](./flywheel) | Earn the second visit. Growth and retention: finds where a product loses the users it already earned, across four ordered plays—Trust, Friction, Wins, and Emotion. Diagnose where value is leaking, or design the experience that earns the next stage of the relationship. | People arrive but do not trust, reach value, recognize value, return, or bring others. Use it to find the earliest relationship leak or design the stage that earns the next step. |
| [**soul**](./soul) | Never boring. Delight, placed: sorts every beat of the happy path into three tiers—Expected stays functional, Elevated adds craft to the small things, and up to three Net-New moments may be rebuilt entirely. Zero Net-New moments is valid when restraint is the better decision. | The happy path works but feels generic, forgettable, or over-designed. Use it to decide which moments stay conventional, gain craft, or become memorable—including where motion earns its place. |

## What each Skill returns

The four foundational Skills have two output modes. **Build** proposes a new design as a fixed specification with an unscored gate checklist. **Audit-style modes**—review, diagnose, or search—evaluate an existing artifact with numeric scores, prioritized findings, and a local methodology verdict. Product Judgement is audit-only: it preserves the four native scorecards and adds cross-scale prioritization without inventing a fifth score.

| Skill | Build output | Audit-style output | Local conclusion |
|---|---|---|---|
| [**Product Judgement**](./product-judgement) | — | **Holistic audit**—four native scorecards with evidence-backed component rationales, shared coverage, deduplicated cross-scale findings, and a prioritized list of changes with Screen · Flow · State · Lifecycle locators | Are the four scales coherent, and what should be fixed first? |
| [**Focal**](./focal) | **Screen Spec**—organizing intent, action model, information, disclosure, hierarchy, states, and gates | **Screen review**—three-discipline `/12` scorecard with per-discipline rationales, issues, up to three top moves, and structural/executional next steps, all located by Screen · Flow · State · Lifecycle | Does the screen satisfy **One Screen, One Clear Intent**? |
| [**Compass**](./compass) | **Flow Spec**—finite outcome or open-ended anchor, steps, cuts, orientation, continuity, and gates | **Flow review**—three-discipline `/12` scorecard with per-discipline rationales, issues, up to three top moves, and structural/executional next steps, all located by Screen · Flow · State · Lifecycle | Is the user **Never Lost**? |
| [**Flywheel**](./flywheel) | **Stage Spec**—first value, relationship leak, design, friction kept, ask placement, and gates | **Diagnosis**—a full four-play scan with `/16` only when every play is evaluable, or one targeted `/4` stage review, with rationales, issues, the earliest evidenced relationship stage to fix, and what follows, all located by Screen · Flow · State · Lifecycle | Where does momentum drop first—before engagement, before first value, after value, or after repeat use? |
| [**Soul**](./soul) | **Moment Spec**—feeling, frequency, Expected/Elevated/Net-New target, treatment ladder through that target, constraints, and gates | **Happy-path sweep**—an unscored Readiness verdict plus a three-gate `/12` scorecard, path map, up to three ranked Net-New moments, small things, and restraint receipt, all located by Screen · Flow · State · Lifecycle | Is the working path ready for authorship, and is its treatment memorable without becoming misplaced or exhausting? |

For Flywheel, a **leak** is not just churn. It is the first point where momentum drops out of the relationship: people leave without engaging, engage without reaching first value, reach value without returning or converting, or return for a while and then drift away.

## Shared audit contract

Build outputs are proposals, so their gates remain binary and unscored. Audit-style outputs evaluate something that already exists, so every evaluated local dimension receives an integer score from `0–4`:

| Score | Meaning |
|---:|---|
| **0 — Broken or harmful** | Fails outright, blocks the dimension's core outcome, inverts the intended behavior, or creates material harm. |
| **1 — Major failure** | Technically possible, but seriously compromised, unreliable, or largely absent. |
| **2 — Partial or inconsistent** | The basic function exists, but a material weakness prevents dependable quality. |
| **3 — Strong** | Deliberate, dependable professional work with only minor gaps—the normal target for good execution. |
| **4 — Exemplary, above and beyond** | Goes beyond strong professional execution: fully realized and unusually effective for its context, realistic states, and constraints. It is intentionally uncommon and not the norm. |

These are ordinal quality levels, not percentages or school grades. A `3/4` is the intended bar for strong product work; it does **not** mean 75%. A Focal, Compass, or Soul result of `9/12`, or a full Flywheel result of `12/16`, means every evaluated dimension is Strong. A `4/4` is deliberately harder: it recognizes above-and-beyond execution in a selectively exemplary dimension. It is not the norm, the expected baseline, or the minimum acceptable result.

Do not optimize every audit toward a perfect total. Eliminate `0`s and `1`s, improve consequential `2`s, establish `3` as the dependable baseline, then pursue selected `4`s only where deeper investment supports the product's goals or creates meaningful differentiation. Scores describe the quality profile; they do not decide release readiness by themselves. A P0 or explicit blocker still requires action regardless of the total.

The scorecard keeps each foundational Skill's native total—`/12` for Focal, Compass, and Soul, and `/16` for a complete Flywheel diagnosis—and also displays `total ÷ evaluated dimensions` as a normalized `/4` average rounded to one decimal place. A targeted Flywheel stage review reports one `/4` score and marks the other plays `N/E—outside targeted scope`; a full diagnosis marks an entirely unexposed play `N/E—insufficient evidence`. Neither case invents a `/16` total. Product Judgement preserves native totals and does not average them into a misleading collection-wide score.

| Common band | Average | `/12` total | `/16` total |
|---|---:|---:|---:|
| **Broken** | `≤ 1.5` | `0–4` | `0–6` |
| **Significant rework** | `> 1.5` and `< 2.5` | `5–7` | `7–9` |
| **Solid** | `≥ 2.5` and `< 3.5` | `8–10` | `10–13` |
| **Excellent** | `≥ 3.5` | `11–12` | `14–16` |

The weakest dimension then caps the final displayed band: a lowest score of `0` caps it at **Broken**, `1` at **Significant rework**, `2` at **Solid**, and `3–4` adds no ceiling. This prevents a high total from hiding one failed dimension.

`N/E` means **not evaluated**, not zero. Use it only where the local contract permits it: a Flywheel play outside targeted scope or entirely unsupported by evidence, or a Soul gate made genuinely unevaluable by Deferred Readiness. When a native scorecard is incomplete, report the evaluated rows and the evidence gap, but do not calculate its native total or common band.

### Scores must explain themselves

A score without an explanation is invalid. Every scorecard row must show the chain **evidence → consequence → rubric anchor → next-point change**:

- **Evidence**—what was observed, inferred, tested, walked, or measured, anchored to the relevant surface or transition, app state, and lifecycle moment.
- **Consequence**—what that condition costs the user or product in the Skill's terms.
- **Rubric anchor**—why the evidence earns this integer and what keeps it from the next higher integer. A `2` says what works and names the material weakness; a `3` names the remaining gap; a `4` explains why the dimension is exemplary.
- **Next-point change**—the smallest concrete change that would raise the score by one point; a `4` says `None—already exemplary.`

Do not award credit for behavior the artifact does not expose, and do not turn an unseen state into a failure without a rubric basis. Mark it `not shown` in Coverage/Basis and name the validating check. The total is the exact sum of the justified component scores; never derive component scores from the total.

`Focal 7/12` is therefore incomplete. A valid result must show something like: `Information Architecture 2/4`—the screen groups the core content but leaves two independent jobs resident, so the user still sorts competing outcomes; split or demote one job to reach 3. `Progressive Disclosure 2/4`—the primary facts are visible but secondary history loads at full depth; cap the default and defer the rest to reach 3. `Visual Hierarchy 3/4`—the primary action wins, with one secondary region still too loud; quiet that region to reach 4. Then, and only then, report **7/12 · 2.3/4 · Significant rework**.

Five concepts remain separate in every audit:

- **Dimension score**—quality within one Skill-specific discipline, play, or gate.
- **Final quality band**—the lower of the average-derived band and weakest-dimension ceiling.
- **Issue severity**—P0 Critical, P1 Major, P2 Moderate, or P3 Minor, assigned from consequence, reach, and recoverability.
- **Blocker**—an explicit release-critical condition; every P0 is a blocker, but a blocker does not automatically force a score to `0`.
- **Local verdict**—the Skill's own north-star conclusion, evaluated independently from the common band.

Every audit declares **Coverage** with a four-part implementation locator: **Screen** (the exact UI surface), **Flow** (the named journey or transition, or `screen-local`), **State** (the exact rendered or system condition), and **Lifecycle** (the exact user/product moment). Every issue, top move, Next item, handoff, and Product Judgement priority change carries the same four fields, so the reader can open the right place and reproduce how and when the condition occurs. Here, lifecycle means the user's journey or relationship with the product (first run, pre-value activation, recurring use, interruption/resume, re-entry, lapse), not a software release phase. Never use only `the dashboard` or `onboarding`; if a field is not evidenced, write `not shown` and name the validating check instead of inventing behavior.

Every audit also states its evidence **Basis** and the fastest test, behavior, or metric that would confirm its most consequential uncertain claim.

## How to use

Designers and developers can use these Skills from a codebase, Figma, Paper, a clickable prototype, screenshots, or a product description. Point the LLM at the artifact and name the scale you want it to inspect.

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

When the question spans the app, use the holistic Skill:

```text
/product-judgement audit the app
```

Product Judgement runs all four foundational Skills, keeps their ownership distinct, and returns the native scorecards plus a deduplicated issue ledger, a prioritized list of changes with dependencies, and a validation plan. It does not add another lens: Focal owns the screen, Compass the path, Flywheel the relationship, and Soul the memory.

Give the Skills the surrounding product context as well. Attach or point the LLM at the PRD (Product Requirements Document), product brief, strategy or goal documents, user research, personas, journey maps, analytics or funnel data, support themes, experiment history, and technical, accessibility, legal, or safety constraints. The more relevant context you provide, the better the Skills can judge whether a design serves a real user, goal, and constraint instead of only reacting to what is visible. When context is missing, the Skills state their assumptions instead of presenting them as facts.

## Install

Each Skill is a folder with a `SKILL.md` at its root, which is the shape Claude Code, Cursor, Codex, and Gemini CLI all read. Pick the row that matches where you work.

| Environment | How it installs | Invocation |
|---|---|---|
| Claude Code, Cursor, Codex | Plugin, from this repository | `/product-judgement:focal`, `/product-judgement:compass`, … |
| Claude Desktop, Claude.ai | Upload a Skill `.zip` | `/focal`, `/compass`, … |
| ChatGPT, custom GPTs | Upload the combined Markdown bundle | Ask for the Skill by name |
| Anything else, or a project-scoped setup | `scripts/install.sh` | `/focal`, `/compass`, … |

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

Claude Code and Cursor also accept the same commands from inside a session as `/plugin marketplace add kvncnls/product-judgement` followed by `/plugin install`. Pin a release by appending a tag to the source, as in `kvncnls/product-judgement@v1.0.0`.

Plugin Skills are namespaced by their plugin, so the audit commands appear as `/product-judgement:focal` rather than `/focal`. If you would rather type the bare names, use [the install script](#any-other-agent-or-a-project-scoped-install) instead.

Update or remove an installed plugin with its own tooling:

```bash
claude plugin update product-judgement
codex plugin marketplace upgrade product-judgement
cursor-agent plugin marketplace update product-judgement
```

### Claude Desktop and Claude.ai

Claude.ai takes a Skill as a `.zip` whose root is the Skill folder. Download the packages from the [latest release](https://github.com/kvncnls/product-judgement/releases/latest), or build them yourself:

```bash
zip -r focal.zip focal
```

Enable **Code execution and file creation** in Settings → Capabilities, then upload the `.zip` under Settings → Capabilities → Skills. Repeat for each Skill you want. A holistic `/product-judgement` audit needs all five, because the orchestration Skill calls the four local methodologies.

### ChatGPT, custom GPTs, and other single-file environments

Some tools accept only one Markdown file. [`bundles/all.md`](./bundles/all.md) is the whole collection—all five Skills, generated from the same sources—in one file, which is what a holistic audit needs:

```bash
cp bundles/all.md ~/Desktop/product-judgement.md
```

Upload it as a ChatGPT Project or custom GPT knowledge file, or attach it to a Claude Project. For a single Skill, use its own bundle instead:

```bash
cat bundles/focal.md >> AGENTS.md
cp bundles/focal.md .cursor/rules/focal.md
```

At roughly 320 KB, the combined bundle suits an uploaded knowledge file rather than an always-loaded instruction file. Append a single-Skill bundle to `AGENTS.md` instead when the whole file is read on every request.

### Any other agent, or a project-scoped install

`scripts/install.sh` symlinks the Skill folders into whichever agents it finds, with no Node and no build step. Because the links point back at your clone, `git pull` updates every agent at once.

```bash
git clone https://github.com/kvncnls/product-judgement.git
cd product-judgement
./scripts/install.sh
```

It targets Claude Code, Cursor, Codex, Gemini CLI, and opencode, and installs the bare `/focal`-style names rather than namespaced plugin ones. Useful variations:

```bash
./scripts/install.sh --agent claude --agent cursor   # only these agents
./scripts/install.sh --skill focal --skill compass   # only these Skills
./scripts/install.sh --scope project                 # into ./.claude/skills and friends
./scripts/install.sh --copy                          # independent copies, not symlinks
./scripts/install.sh --list                          # print target directories, change nothing
./scripts/install.sh --uninstall                     # remove what it installed
```

Run `./scripts/install.sh --help` for the full set. Restart your agent afterwards so it reloads Skill metadata.

To wire up an agent by hand, link each Skill folder into that agent's Skill directory. The common global locations are `~/.claude/skills/` for Claude Code, `~/.cursor/skills/` for Cursor, and `~/.agents/skills/` for Codex, which also reads a repository's `.agents/skills/`:

```bash
ln -s "$(pwd)/focal" ~/.claude/skills/focal
```

Consult the agent's current documentation, because discovery paths change.

### Skills CLI

The [Skills CLI](https://skills.sh/docs/cli) is an alternative that keeps one canonical copy and links supported agents to it. It requires Node:

```bash
npx skills add kvncnls/product-judgement --skill '*' -g -a claude-code -a codex -a cursor -y
```

Run `npx skills add kvncnls/product-judgement` to be asked which Skills, agents, and scope you want, or name one Skill directly:

```bash
npx skills add kvncnls/product-judgement --skill focal -g
```

Check for upstream changes with `npx skills check`, then update this collection's five globally installed Skills:

```bash
npx skills update -g product-judgement focal compass flywheel soul
```

Rerun the full `skills add` command when an update reports a failure, when a new Skill is added to the repository, when an agent link is missing, or when an installation predates the CLI lock record. Use `npx skills list -g` to inspect what is installed.

### For maintainers

The tooling under `scripts/` is Ruby, and it deliberately targets **Ruby 2.6** so it runs on the interpreter macOS ships, with nothing to install. CI pins 3.3, so a 2.7-only method such as `filter_map` passes CI and still fails on a stock Mac. Keep new code inside the 2.6 standard library; `/usr/bin/ruby scripts/verify.rb` is the check that matters. The Skills themselves stay pure Markdown, so this constraint never reaches anyone installing them.

Bundles are build artifacts, regenerated from the source folders rather than edited directly:

```bash
ruby scripts/build_bundles.rb
```

Run the repository verifier before committing. It validates Skill frontmatter, relative links, scoring and boundary invariants, behavioral contract fixtures, the plugin manifests and installer, and exact bundle synchronization; CI runs the same command:

```bash
ruby scripts/verify.rb
```

#### Cutting a release

The version appears in four manifests, and `scripts/check_version.rb` fails the release if any of them disagrees with the tag. Bump all four first, then tag:

```bash
ruby scripts/check_version.rb 1.1.0
git commit -am "Release 1.1.0" && git push
git tag v1.1.0 && git push origin v1.1.0
```

The four are `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.cursor-plugin/plugin.json`, and `.codex-plugin/plugin.json`. Pushing the `v*` tag runs the verifier, confirms the tag matches, builds the Skill `.zip` packages and combined bundle, and publishes the release that the [Claude Desktop and Claude.ai](#claude-desktop-and-claudeai) section links to.

## License

[MIT](./LICENSE) © 2026 Kevin Canlas.
