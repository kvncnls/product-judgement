#!/usr/bin/env ruby
# frozen_string_literal: true

# Canonical shared fragments are copied into each installed Skill so no runtime
# dependency on the repository root is introduced. Edit contracts/, then sync.
ROOT = File.expand_path("..", __dir__)
LOCAL_SKILLS = %w[focal compass flywheel soul].freeze
FRAGMENTS = %w[anchors severity evidence].freeze
abort "Usage: ruby scripts/sync_contracts.rb [--check]" unless (ARGV - ["--check"]).empty?
check = ARGV.include?("--check")
changes = {}
errors = []

targets = LOCAL_SKILLS.map { |skill| ["#{skill}/reference/review.md", FRAGMENTS] }
targets << ["product-judgement/SKILL.md", ["evidence"]]
targets.each do |path, fragments|
  content = File.read(File.join(ROOT, path), encoding: "UTF-8")
  original = content.dup
  fragments.each do |name|
    start = "<!-- BEGIN SHARED: #{name} -->"
    finish = "<!-- END SHARED: #{name} -->"
    pattern = /#{Regexp.escape(start)}\n.*?\n#{Regexp.escape(finish)}/m
    matches = content.scan(pattern)
    if matches.length != 1
      errors << "#{path}: expected exactly one #{name} fragment, found #{matches.length}"
      next
    end
    canonical = File.read(File.join(ROOT, "contracts", "#{name}.md"), encoding: "UTF-8").strip
    content = content.sub(pattern) { "#{start}\n#{canonical}\n#{finish}" }
  end
  changes[path] = content if content != original
end
abort errors.join("\n") unless errors.empty?
if check
  abort "Shared contracts are stale: #{changes.keys.join(', ')}. Run ruby scripts/sync_contracts.rb" unless changes.empty?
  puts "Shared evidence, score anchors, and severity contracts are current."
else
  changes.each { |path, content| File.write(File.join(ROOT, path), content) }
  puts "Synchronized #{changes.length} Skill file(s) from contracts/."
end
