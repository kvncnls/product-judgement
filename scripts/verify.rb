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
