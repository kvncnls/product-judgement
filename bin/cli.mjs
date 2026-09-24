#!/usr/bin/env node
// Interactive front end for scripts/install.sh. The shell script owns every
// filesystem decision; this only turns answers into flags.
import { spawnSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..')
const INSTALLER = join(ROOT, 'scripts', 'install.sh')

const AGENTS = [
  { value: 'claude', label: 'Claude Code' },
  { value: 'cursor', label: 'Cursor' },
  { value: 'codex', label: 'Codex' },
  { value: 'gemini', label: 'Gemini CLI' },
  { value: 'opencode', label: 'OpenCode' },
]

const SKILLS = [
  { value: 'focal', label: 'focal', hint: 'One screen, one clear intent' },
  { value: 'compass', label: 'compass', hint: 'Never lost across a journey' },
  { value: 'flywheel', label: 'flywheel', hint: 'Earn the next valuable step' },
  { value: 'soul', label: 'soul', hint: 'Never boring' },
  { value: 'product-judgement', label: 'product-judgement', hint: 'Holistic audit across all four' },
]

function run(args) {
  const result = spawnSync('sh', [INSTALLER, ...args], { stdio: 'inherit' })
  return result.status ?? 1
}

// Any argument means scripted use: hand it straight to the installer without
// loading the prompt library at all.
if (process.argv.length > 2) {
  process.exit(run(process.argv.slice(2)))
}

// No arguments and nowhere to prompt: show the installer's own usage rather
// than blocking forever on a terminal that will never answer.
if (!process.stdin.isTTY) {
  process.exit(run(['--help']))
}

const p = await import('@clack/prompts')

function keep(value) {
  if (p.isCancel(value)) {
    p.cancel('Nothing installed.')
    process.exit(0)
  }
  return value
}

p.intro('Product Judgement')

const scope = keep(
  await p.select({
    message: 'Where do you want to install these Skills?',
    options: [
      { value: 'user', label: 'Globally', hint: 'every project on this machine' },
      { value: 'project', label: 'This project only', hint: process.cwd() },
    ],
  }),
)

const agents = keep(
  await p.multiselect({
    message: 'Which tools do you want to set up?',
    options: AGENTS,
    required: true,
  }),
)

const skills = keep(
  await p.multiselect({
    message: 'Which Skills do you want to install?',
    options: SKILLS,
    initialValues: SKILLS.map((skill) => skill.value),
    required: true,
  }),
)

// Always --copy. This package lives in npm's cache, which npm is free to
// sweep, so a symlink back into it would dangle. Cloning the repository and
// running scripts/install.sh directly is what gives you tracking symlinks.
const args = ['--scope', scope, '--copy']
for (const agent of agents) args.push('--agent', agent)
for (const skill of skills) args.push('--skill', skill)

p.outro('Installing…')
process.exit(run(args))
