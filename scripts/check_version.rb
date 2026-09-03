#!/usr/bin/env ruby
# frozen_string_literal: true

# Confirms a release tag matches the version every plugin manifest advertises,
# so a tagged install can never resolve to a differently numbered plugin.

require "json"

ROOT = File.expand_path("..", __dir__)

MANIFESTS = {
  ".claude-plugin/plugin.json" => ->(data) { data["version"] },
  ".claude-plugin/marketplace.json" => ->(data) { data.fetch("plugins").first["version"] },
  ".cursor-plugin/plugin.json" => ->(data) { data["version"] },
  ".codex-plugin/plugin.json" => ->(data) { data["version"] }
}.freeze

expected = ARGV[0]
if expected.nil? || expected.strip.empty?
  warn "Usage: ruby scripts/check_version.rb <version>"
  exit 2
end
expected = expected.strip

errors = []
MANIFESTS.each do |path, reader|
  found = reader.call(JSON.parse(File.read(File.join(ROOT, path), encoding: "UTF-8")))
  errors << "#{path}: version #{found.inspect}, expected #{expected.inspect}" unless found == expected
end

if errors.any?
  warn "Version mismatch:"
  errors.each { |error| warn "- #{error}" }
  exit 1
end

puts "All plugin manifests report version #{expected}."
