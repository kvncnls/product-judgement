#!/usr/bin/env ruby
# frozen_string_literal: true

require "json"
require "open3"
require "rbconfig"
require "yaml"

ROOT = File.expand_path("..", __dir__)
SKILLS = %w[focal compass flywheel soul product-judgement].freeze
errors = []

def relative(path)
  path.delete_prefix("#{ROOT}/")
end

def read(path)
  File.read(File.join(ROOT, path), encoding: "UTF-8")
end

def require_text(errors, path, text, label)
  return if read(path).include?(text)

  errors << "#{path}: missing #{label.inspect}"
end

def reject_text(errors, paths, text, label)
  paths.each do |path|
    errors << "#{path}: contains stale #{label.inspect}" if read(path).include?(text)
  end
end

# Skill frontmatter must stay portable and discoverable.
SKILLS.each do |skill|
  path = "#{skill}/SKILL.md"
  content = read(path)
  match = content.match(/\A---\n(.*?)\n---\n/m)

  unless match
    errors << "#{path}: missing YAML frontmatter"
    next
  end

  begin
    metadata = YAML.safe_load(match[1], permitted_classes: [], aliases: false)
  rescue Psych::SyntaxError => error
    errors << "#{path}: invalid YAML frontmatter (#{error.message.lines.first.strip})"
    next
  end

  errors << "#{path}: frontmatter name must be #{skill.inspect}" unless metadata.is_a?(Hash) && metadata["name"] == skill
  description = metadata.is_a?(Hash) ? metadata["description"] : nil
  errors << "#{path}: frontmatter description must be a substantive string" unless description.is_a?(String) && description.length >= 80
  # The Agent Skills spec caps description at 1024 characters. Over it, the
  # claude.ai and Skills API upload paths reject the Skill; Claude Code does
  # not validate, so nothing else in this repo would notice.
  if description.is_a?(String) && description.length > 1024
    errors << "#{path}: frontmatter description is #{description.length} characters; the spec cap is 1024"
  end
  errors << "#{path}: frontmatter name must be 64 characters or fewer" if metadata.is_a?(Hash) && metadata["name"].to_s.length > 64
  errors << "#{path}: frontmatter must declare license: MIT" unless metadata.is_a?(Hash) && metadata["license"] == "MIT"
  # argument-hint is a Claude Code extension, kept deliberately and stripped
  # from the upload packages by scripts/package_skills.rb.
  errors << "#{path}: frontmatter must carry an argument-hint" unless metadata.is_a?(Hash) && metadata["argument-hint"].is_a?(String)
  unknown_keys = metadata.is_a?(Hash) ? metadata.keys - %w[name description license compatibility metadata allowed-tools argument-hint] : []
  unless unknown_keys.empty?
    errors << "#{path}: frontmatter keys #{unknown_keys.inspect} are neither spec fields nor known Claude Code extensions; teach scripts/package_skills.rb about them first"
  end
end

# Every Skill folder is installed, zipped, and symlinked whole, so they must
# carry the same files. This is the check that would have caught ABOUT.md
# living in two of five folders and product-judgement shipping no LICENSE.
SKILLS.each do |skill|
  %w[SKILL.md README.md LICENSE agents/openai.yaml].each do |required|
    errors << "#{skill}/#{required}: missing" unless File.file?(File.join(ROOT, skill, required))
  end
  extra = Dir.glob(File.join(ROOT, skill, "*.md")).map { |p| File.basename(p) } - %w[SKILL.md README.md]
  errors << "#{skill}: unexpected top-level Markdown #{extra.inspect}; reference material belongs in reference/" unless extra.empty?
end
# product-judgement legitimately has no reference/ — it is audit-only and its
# contract is always needed, so it lives in the spine.
(SKILLS - %w[product-judgement]).each do |skill|
  errors << "#{skill}/reference: must contain at least one Markdown file" if Dir.glob(File.join(ROOT, skill, "reference", "*.md")).empty?
end

# agents/openai.yaml is Codex's per-skill interface file. It went unchecked and
# so existed on one Skill of five.
OPENAI_INTERFACE_KEYS = %w[display_name short_description icon_small icon_large brand_color default_prompt].freeze
SKILLS.each do |skill|
  rel = "#{skill}/agents/openai.yaml"
  next unless File.file?(File.join(ROOT, rel))

  begin
    doc = YAML.safe_load(read(rel), permitted_classes: [], aliases: false)
  rescue Psych::SyntaxError => error
    errors << "#{rel}: invalid YAML (#{error.message.lines.first.strip})"
    next
  end
  interface = doc.is_a?(Hash) ? doc["interface"] : nil
  unless interface.is_a?(Hash)
    errors << "#{rel}: must declare an interface mapping"
    next
  end
  stray = interface.keys - OPENAI_INTERFACE_KEYS
  errors << "#{rel}: unknown interface key(s) #{stray.inspect}" unless stray.empty?
  display = interface["display_name"]
  errors << "#{rel}: interface.display_name is required and capped at 64 characters" unless display.is_a?(String) && !display.empty? && display.length <= 64
  short = interface["short_description"]
  # OpenAI's own generator rejects anything outside 25-64, which is stricter
  # than the 1024 the Codex runtime allows. Match the generator.
  unless short.is_a?(String) && (25..64).cover?(short.length)
    errors << "#{rel}: interface.short_description must be 25-64 characters (was #{short.is_a?(String) ? short.length : short.class})"
  end
end

# Plugin manifests are the install path for Claude Code, Cursor, and Codex, so
# every one of them must stay valid, agree on a version, and expose all five
# Skills. A manifest that silently drops a Skill installs a broken collection.
PLUGIN_MANIFESTS = %w[
  .claude-plugin/plugin.json
  .claude-plugin/marketplace.json
  .cursor-plugin/plugin.json
  .codex-plugin/plugin.json
  .agents/plugins/marketplace.json
].freeze

manifests = {}
PLUGIN_MANIFESTS.each do |path|
  manifests[path] = JSON.parse(read(path))
rescue Errno::ENOENT
  errors << "#{path}: missing"
rescue JSON::ParserError => error
  errors << "#{path}: invalid JSON (#{error.message.lines.first.strip})"
end

expected_skill_paths = SKILLS.map { |skill| "./#{skill}" }.sort

%w[.claude-plugin/plugin.json .cursor-plugin/plugin.json .codex-plugin/plugin.json].each do |path|
  next unless (manifest = manifests[path])

  errors << "#{path}: name must be \"product-judgement\"" unless manifest["name"] == "product-judgement"
  declared = manifest["skills"]
  unless declared.is_a?(Array) && declared.sort == expected_skill_paths
    errors << "#{path}: skills must list every Skill as #{expected_skill_paths.inspect}"
  end
end

# Each marketplace points at the repository root, so the plugin manifests above
# are what actually resolve the Skills.
if (marketplace = manifests[".claude-plugin/marketplace.json"])
  entries = marketplace["plugins"]
  if entries.is_a?(Array) && entries.length == 1
    errors << ".claude-plugin/marketplace.json: plugin source must be \"./\"" unless entries.first["source"] == "./"
    errors << ".claude-plugin/marketplace.json: plugin name must be \"product-judgement\"" unless entries.first["name"] == "product-judgement"
  else
    errors << ".claude-plugin/marketplace.json: expected exactly one plugin entry"
  end
  errors << ".claude-plugin/marketplace.json: owner.name is required" unless marketplace.dig("owner", "name").is_a?(String)
end

if (marketplace = manifests[".agents/plugins/marketplace.json"])
  entries = marketplace["plugins"]
  if entries.is_a?(Array) && entries.length == 1
    source = entries.first["source"]
    unless source.is_a?(Hash) && source["source"] == "local" && source["path"] == "./"
      errors << ".agents/plugins/marketplace.json: plugin source must be a local path of \"./\""
    end
  else
    errors << ".agents/plugins/marketplace.json: expected exactly one plugin entry"
  end
end

# One version across every manifest keeps a tagged release honest.
versions = manifests.map do |path, manifest|
  next unless manifest
  version = path.end_with?("marketplace.json") ? manifest.dig("plugins", 0, "version") : manifest["version"]
  [path, version] if version
end.compact
if versions.map(&:last).uniq.length > 1
  errors << "plugin manifests disagree on version: #{versions.map { |path, version| "#{path}=#{version}" }.join(", ")}"
end

# The universal installer must stay runnable and cover every Skill and agent.
install_script = File.join(ROOT, "scripts", "install.sh")
if File.file?(install_script)
  errors << "scripts/install.sh: must be executable" unless File.executable?(install_script)
  install_source = read("scripts/install.sh")
  errors << "scripts/install.sh: SKILLS list must match the Skill folders" unless install_source.include?("SKILLS=\"#{SKILLS.join(" ")}\"")
  %w[claude codex cursor].each do |agent|
    errors << "scripts/install.sh: missing a target directory for #{agent}" unless install_source.match?(/^\s+#{agent}\)/)
  end
  _, shellcheck_stderr, shellcheck_status = Open3.capture3("sh", "-n", install_script)
  errors << "scripts/install.sh: shell syntax error (#{shellcheck_stderr.strip})" unless shellcheck_status.success?
else
  errors << "scripts/install.sh: missing"
end

# Relative Markdown links in source documentation must resolve. Generated bundles
# intentionally preserve source-relative links verbatim, so they are checked by the
# bundle synchronization test rather than by this path resolver.
markdown_files = Dir.glob(File.join(ROOT, "**", "*.md")).reject do |path|
  path.include?("/.git/") || path.start_with?(File.join(ROOT, "bundles") + "/")
end

markdown_files.each do |path|
  File.read(path, encoding: "UTF-8").scan(/\[[^\]]*\]\(([^)]+)\)/).flatten.each do |raw_target|
    target = raw_target.strip
    target = target[1...-1] if target.start_with?("<") && target.end_with?(">")
    target = target.split(/\s+["']/, 2).first
    next if target.empty? || target.start_with?("#")
    next if target.match?(%r{\A(?:https?|mailto|app)://}i)

    file_target = target.split("#", 2).first
    next if file_target.empty?

    resolved = File.expand_path(file_target, File.dirname(path))
    errors << "#{relative(path)}: broken relative link #{target.inspect}" unless File.exist?(resolved)
  end
end

# Guard the behavioral decisions most likely to regress into rigid heuristics or
# overlapping ownership.
require_text(errors, "focal/SKILL.md", "Use four chunks as a task-screen diagnostic, not a universal limit.", "contextual chunk diagnostic")
require_text(errors, "focal/SKILL.md", "not extra numeric weight", "equal discipline weighting")
require_text(errors, "focal/reference/review.md", "not a stopwatch threshold or an automatic scoring failure", "quick-orientation probe")
require_text(errors, "focal/reference/review.md", "Top moves (up to 3)", "non-quota top moves")
require_text(errors, "focal/SKILL.md", "Every applicable state above designed", "contextual state gate")

require_text(errors, "compass/SKILL.md", "The outcome-or-anchor test.", "finite/open-ended framing")
require_text(errors, "compass/SKILL.md", "what remains when the journey is bounded", "bounded progress rule")
require_text(errors, "compass/reference/review.md", "Browser Back can be sufficient", "platform-appropriate retreat rule")
require_text(errors, "compass/reference/review.md", "A failed drop test is not automatically release-critical", "consequence-based drop-test severity")

require_text(errors, "flywheel/SKILL.md", "full relationship diagnosis evaluates all four plays", "full diagnosis contract")
require_text(errors, "flywheel/SKILL.md", "targeted stage review or build runs one play deeply", "targeted stage contract")
require_text(errors, "flywheel/reference/review.md", "N/E—outside targeted scope", "targeted N/E output")
require_text(errors, "flywheel/reference/review.md", "N/E—insufficient evidence", "evidence-gap N/E output")
require_text(errors, "flywheel/reference/review.md", "A P0 at any stage overrides that order", "critical-severity precedence")
require_text(errors, "flywheel/reference/review.md", "Missing internal terminology does not cap a UX score by itself", "evidence-based first-value scoring")
require_text(errors, "flywheel/reference/emotion.md", "Boundary with Soul", "Flywheel/Soul boundary")

require_text(errors, "soul/reference/review.md", "Readiness is deliberately **unscored**", "unscored Readiness")
require_text(errors, "soul/reference/review.md", "## The three scored gates", "three-gate Soul scorecard")
require_text(errors, "soul/reference/review.md", "zero Net-New moments as valid", "zero-Net-New outcome")
require_text(errors, "soul/SKILL.md", "**Target:** <Expected | Elevated | Net-New>", "all three build targets")
require_text(errors, "soul/reference/treatments.md", "Elevated is the default ceiling", "contextual frequency/stakes default")
require_text(errors, "soul/reference/treatments.md", "Net-New is an exception, not an entitlement", "durable Net-New exception")

require_text(errors, "product-judgement/SKILL.md", "scope follows the decisions involved, not the number of screens", "cross-scale scope rule")
require_text(errors, "product-judgement/SKILL.md", "One condition may legitimately affect several local scores", "deduplication contract")
require_text(errors, "product-judgement/SKILL.md", "Priority changes (up to 4)", "non-quota priorities")

source_contract_files = Dir.glob(File.join(ROOT, "{focal,compass,flywheel,soul,product-judgement}", "**", "*.md")).map { |path| relative(path) }
reject_text(errors, source_contract_files, "Never run all four plays by default", "Flywheel full-audit contradiction")
reject_text(errors, source_contract_files, "A real Back on every screen", "universal Back requirement")
reject_text(errors, source_contract_files, "declining is free", "absolute decline-cost claim")
reject_text(errors, source_contract_files, "2–3 biggest moments", "Soul Net-New quota")
reject_text(errors, source_contract_files, "Baseline, Placement, Proportion, and Signature", "obsolete four-gate Soul scorecard")

# Public documentation must expose every Skill, the score contract, and the current
# install/update path without claiming the repository has no maintainer build step.
required_docs = ["README.md"] + SKILLS.map { |skill| "#{skill}/README.md" }
required_docs.each { |path| errors << "#{path}: missing" unless File.file?(File.join(ROOT, path)) }
require_text(errors, "README.md", "npx skills update -g product-judgement focal compass flywheel soul", "global update command")
require_text(errors, "README.md", "`/12` for Focal, Compass, and Soul", "native totals")
require_text(errors, "README.md", "`N/E` means **not evaluated**, not zero", "N/E explanation")
require_text(errors, "README.md", "no runtime build step", "runtime/build distinction")
reject_text(errors, required_docs, "Claude Code skill", "platform-specific Skill description")
reject_text(errors, ["README.md"], "no build step, no dependencies", "obsolete no-build claim")

# Behavioral fixtures are machine-readable and must carry both positive and negative
# assertions so they can drive a later model-evaluation harness.
fixture_path = File.join(ROOT, "tests", "behavioral-contracts.yml")
begin
  fixtures = YAML.safe_load(File.read(fixture_path, encoding: "UTF-8"), permitted_classes: [], aliases: false)
  unless fixtures.is_a?(Array) && fixtures.length >= 8
    errors << "tests/behavioral-contracts.yml: expected at least eight fixtures"
  else
    ids = fixtures.map { |fixture| fixture.is_a?(Hash) ? fixture["id"] : nil }.compact
    errors << "tests/behavioral-contracts.yml: fixture IDs must be unique" unless ids.length == ids.uniq.length

    fixtures.each_with_index do |fixture, index|
      unless fixture.is_a?(Hash)
        errors << "tests/behavioral-contracts.yml: fixture #{index + 1} must be a mapping"
        next
      end

      %w[id skill scenario].each do |key|
        value = fixture[key]
        errors << "tests/behavioral-contracts.yml: fixture #{index + 1} needs #{key}" unless value.is_a?(String) && !value.strip.empty?
      end

      %w[evidence expected reject].each do |key|
        value = fixture[key]
        valid = value.is_a?(Array) && !value.empty? && value.all? { |item| item.is_a?(String) && !item.strip.empty? }
        errors << "tests/behavioral-contracts.yml: fixture #{index + 1} needs a non-empty #{key} list" unless valid
      end
    end
  end
rescue Errno::ENOENT, Psych::SyntaxError => error
  errors << "tests/behavioral-contracts.yml: #{error.message.lines.first.strip}"
end

# The four review contracts each restate one shared audit contract, because every
# Skill must be installable standalone. Nothing compared the copies, so Soul had
# silently paraphrased the score anchors and dropped whole rules. These passages
# are contract, not prose: they must be byte-identical in all four.
REVIEW_CONTRACTS = SKILLS.reject { |skill| skill == "product-judgement" }.map { |skill| "#{skill}/reference/review.md" }.freeze

SHARED_CONTRACT_TEXT = [
  ["score anchor 0", "| **0** | **Broken or harmful** | The dimension fails outright, blocks its core outcome, actively inverts the intended behavior, or creates material harm. |"],
  ["score anchor 1", "| **1** | **Major failure** | The outcome may remain technically possible, but the dimension is seriously compromised, unreliable, or largely absent. Substantial correction is required. |"],
  ["score anchor 2", "| **2** | **Partial or inconsistent** | The basic function exists, with a material weakness, missing decision, or inconsistency that prevents dependable quality. |"],
  ["score anchor 3", "| **3** | **Strong** | Deliberate, dependable, context-appropriate professional work with only minor gaps. This is the normal target for good execution. |"],
  ["score anchor 4", "| **4** | **Exemplary—above and beyond** | Fully realized and unusually effective for the relevant context, including realistic states and constraints. This is intentionally uncommon, not the normal target. |"],
  ["P0 severity definition", "| **P0 — Critical** | Blocks the core outcome; traps the user; destroys work or state; causes or risks material harm; hides material cost, consequence, permission, or risk; removes informed choice; or uses coercive manipulation. Fix before release. |"],
  ["P3 severity definition", "| **P3 — Minor** | Low-impact craft, consistency, or polish. Fix when time permits. |"],
  ["severity assignment rule", "Assign severity from consequence, reach, and recoverability. A methodology rule violation is not automatically P0."],
  ["ordering rule", "**Ordering (one rule):** sort by priority, P0 first. Within the same priority, break ties by"],
  ["band ceiling rule", "Use the lower-quality result of the average band and this ceiling."],
  ["blocker independence rule", "a blocker does not automatically rewrite a score to 0; a score of 0 does not automatically imply P0"],
  ["non-critical failures rule", "Non-critical methodology failures belong in the local verdict, score, sequencing, or handoff—not in **Blocker**."],
  ["score rationale chain", "**evidence → consequence → rubric anchor → next-point change**"],
  ["worst-failure rule", "score the *worst* one, then list the others as separate issues."],
  ["holistic scoring rule", "let one severe material failure determine the score when the rubric warrants it"],
  ["no-invented-behavior rule", "do not invent behavior."],
  ["narrowest locator rule", "Use the narrowest defensible locator."],
].freeze

SHARED_CONTRACT_TEXT.each do |label, text|
  missing = REVIEW_CONTRACTS.reject { |rel| read(rel).include?(text) }
  next if missing.empty?

  errors << "shared audit contract drifted: #{label.inspect} is missing from #{missing.join(", ")}"
end

# The /12 band table is shared by the three three-dimension Skills; Flywheel's
# /16 rows are correct local arithmetic for four plays, not drift.
BAND_ROWS_12 = [
  "| **Broken** | `average <= 1.5` | `0–4 / 12` |",
  "| **Significant rework** | `1.5 < average < 2.5` | `5–7 / 12` |",
  "| **Solid** | `2.5 <= average < 3.5` | `8–10 / 12` |",
  "| **Excellent** | `average >= 3.5` | `11–12 / 12` |",
].freeze
BAND_ROWS_16 = [
  "| **Broken** | `average <= 1.5` | `0–6 / 16` |",
  "| **Significant rework** | `1.5 < average < 2.5` | `7–9 / 16` |",
  "| **Solid** | `2.5 <= average < 3.5` | `10–13 / 16` |",
  "| **Excellent** | `average >= 3.5` | `14–16 / 16` |",
].freeze
%w[focal compass soul].each do |skill|
  rel = "#{skill}/reference/review.md"
  BAND_ROWS_12.each { |row| errors << "#{rel}: missing shared /12 band row #{row.inspect}" unless read(rel).include?(row) }
end
BAND_ROWS_16.each { |row| errors << "flywheel/reference/review.md: missing /16 band row #{row.inspect}" unless read("flywheel/reference/review.md").include?(row) }

# The orchestration override is what stops a local Skill printing its own locked
# template, asking a framing question, or routing back to the orchestrator from
# inside an orchestrated pass. Losing it silently breaks every holistic audit.
(SKILLS - %w[product-judgement]).each do |skill|
  rel = "#{skill}/SKILL.md"
  content = read(rel)
  errors << "#{rel}: missing the orchestrated-pass override" unless content.include?("**Orchestrated pass—this overrides every other instruction in this Skill and its reference files.**")
  errors << "#{rel}: orchestrated pass must suppress the examples calibration read" unless content.include?("do not read [reference/examples.md](reference/examples.md)")
  errors << "#{rel}: orchestrated pass must forbid handing a cross-scale request back" unless content.include?("Never hand a cross-scale request back to Product Judgement")
end

require_text(errors, "product-judgement/SKILL.md", "### When a sibling Skill is not installed", "missing-sibling fallback")
require_text(errors, "product-judgement/SKILL.md", "N/E—Skill not installed", "uninstalled-scale verdict")
require_text(errors, "product-judgement/SKILL.md", "This wrapper supersedes local output instructions", "local-output supersession")
require_text(errors, "README.md", "a scale whose Skill is not installed alongside Product Judgement", "third permitted N/E use")

# The behavioral fixtures now have a runner. It spends real model tokens, so it
# must stay opt-in and must never be wired into the verifier or CI.
eval_script = File.join(ROOT, "scripts", "eval.rb")
if File.file?(eval_script)
  errors << "scripts/eval.rb: must be executable" unless File.executable?(eval_script)
  _, eval_stderr, eval_status = Open3.capture3(RbConfig.ruby, "-c", eval_script)
  errors << "scripts/eval.rb: syntax error (#{eval_stderr.strip})" unless eval_status.success?
  errors << ".github/workflows/verify.yml: must not run scripts/eval.rb; it costs model tokens" if read(".github/workflows/verify.yml").include?("eval.rb")
  errors << ".github/workflows/release.yml: must not run scripts/eval.rb; it costs model tokens" if read(".github/workflows/release.yml").include?("eval.rb")
else
  errors << "scripts/eval.rb: missing"
end

# The upload packages must be built by the script that strips non-spec
# frontmatter, not by a bare zip that would ship a rejected argument-hint.
package_script = File.join(ROOT, "scripts", "package_skills.rb")
if File.file?(package_script)
  errors << "scripts/package_skills.rb: must be executable" unless File.executable?(package_script)
  _, pkg_stderr, pkg_status = Open3.capture3(RbConfig.ruby, "-c", package_script)
  errors << "scripts/package_skills.rb: syntax error (#{pkg_stderr.strip})" unless pkg_status.success?
  require_text(errors, ".github/workflows/release.yml", "scripts/package_skills.rb", "packaging step")
else
  errors << "scripts/package_skills.rb: missing"
end

# Generated bundles must be exact products of the canonical source files.
stdout, stderr, status = Open3.capture3(RbConfig.ruby, File.join(ROOT, "scripts", "build_bundles.rb"), "--check", chdir: ROOT)
errors << "bundles: #{(stderr + stdout).strip}" unless status.success?

# Lightweight text hygiene catches drift that Markdown renderers often hide.
text_files = Dir.glob(File.join(ROOT, "{README.md,*.md,**/*.md,**/*.rb,**/*.yml,**/*.yaml}"), File::FNM_EXTGLOB).uniq
text_files.reject! { |path| path.include?("/.git/") }
text_files.each do |path|
  content = File.binread(path)
  errors << "#{relative(path)}: must end with a newline" unless content.empty? || content.end_with?("\n")
  content.each_line.with_index(1) do |line, line_number|
    errors << "#{relative(path)}:#{line_number}: trailing whitespace" if line.match?(/[ \t]+(?:\r?\n)?\z/) && !line.strip.empty?
  end
end

if errors.any?
  warn "Verification failed with #{errors.length} issue#{errors.length == 1 ? "" : "s"}:"
  errors.each { |error| warn "- #{error}" }
  exit 1
end

puts "Verified #{SKILLS.length} Skills, #{markdown_files.length} Markdown source files, generated bundles, and behavioral contracts."
