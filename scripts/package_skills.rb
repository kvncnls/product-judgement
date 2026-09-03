#!/usr/bin/env ruby
# frozen_string_literal: true

# Builds the upload packages for environments that take a .zip instead of a
# plugin: Claude.ai and Claude Desktop, and the Skills API.
#
# Why this exists rather than a plain `zip -r focal.zip focal`: the Agent Skills
# spec allows exactly six frontmatter keys, and an upload carrying anything else
# fails with a hard error instead of ignoring it —
#   Unexpected key(s) in SKILL.md frontmatter: argument-hint.
# `argument-hint` is a Claude Code extension we want to keep in the source,
# because Claude Code is the primary install target and honors it. So the source
# keeps it and the packages drop it.
#
# Targets Ruby 2.6 — the interpreter macOS ships — like the rest of scripts/.

require "fileutils"
require "open3"
require "optparse"
require "tmpdir"

ROOT = File.expand_path("..", __dir__)
SKILLS = %w[focal compass flywheel soul product-judgement].freeze

# https://agentskills.io/specification — the complete allowed set.
SPEC_KEYS = %w[name description license compatibility metadata allowed-tools].freeze

options = { out: File.join(ROOT, "dist"), skills: [], combined: true }
OptionParser.new do |parser|
  parser.banner = "Usage: ruby scripts/package_skills.rb [options]"
  parser.on("--out DIR", "Output directory (default: dist/)") { |v| options[:out] = File.expand_path(v) }
  parser.on("--skill NAME", "Package only this Skill; repeatable") { |v| options[:skills] << v }
  parser.on("--no-combined", "Skip the all-five package") { options[:combined] = false }
  parser.on("--check", "Report what would be stripped; write nothing") { options[:check] = true }
  parser.on("-h", "--help") { puts parser; exit 0 }
end.parse!

selected = options[:skills].empty? ? SKILLS : options[:skills]
unknown = selected - SKILLS
abort "unknown Skill(s): #{unknown.join(", ")}" unless unknown.empty?

# Drops non-spec keys from a SKILL.md frontmatter block without re-serializing
# the YAML, so the retained keys keep their exact original formatting.
def strip_non_spec_frontmatter(text, path)
  match = text.match(/\A---\n(.*?\n)---\n/m)
  raise "#{path}: missing YAML frontmatter" unless match

  stripped = []
  kept_lines = []
  dropping = false

  match[1].each_line do |line|
    if (key = line[/\A([A-Za-z0-9_-]+):/, 1])
      dropping = !SPEC_KEYS.include?(key)
      stripped << key if dropping
    elsif line.strip.empty?
      dropping = false
    end
    # A continuation line (indented, or a block scalar body) belongs to the key
    # above it, so it follows that key's fate.
    kept_lines << line unless dropping
  end

  raise "#{path}: every frontmatter key was stripped" if kept_lines.empty?

  [text.sub(match[0], "---\n#{kept_lines.join}---\n"), stripped]
end

def zip(out_zip, staging, entries)
  FileUtils.rm_f(out_zip)
  _, stderr, status = Open3.capture3(
    "zip", "-q", "-r", "-X", out_zip, *entries, "-x", "*.DS_Store", chdir: staging
  )
  raise "zip failed for #{out_zip}: #{stderr.strip}" unless status.success?
end

all_stripped = {}

Dir.mktmpdir("pj-package") do |staging|
  selected.each do |skill|
    FileUtils.cp_r(File.join(ROOT, skill), staging)
    skill_md = File.join(staging, skill, "SKILL.md")
    text = File.read(skill_md, encoding: "UTF-8")
    rewritten, stripped = strip_non_spec_frontmatter(text, "#{skill}/SKILL.md")
    all_stripped[skill] = stripped
    File.write(skill_md, rewritten)
  end

  if options[:check]
    selected.each do |skill|
      dropped = all_stripped[skill]
      puts "#{skill}: #{dropped.empty? ? "nothing to strip" : "would strip #{dropped.join(", ")}"}"
    end
    exit 0
  end

  FileUtils.mkdir_p(options[:out])
  selected.each do |skill|
    zip(File.join(options[:out], "#{skill}.zip"), staging, [skill])
  end
  if options[:combined] && selected.sort == SKILLS.sort
    zip(File.join(options[:out], "product-judgement-all-skills.zip"), staging, SKILLS)
  end
end

selected.each do |skill|
  dropped = all_stripped[skill]
  puts format("%-20s %s", "#{skill}.zip", dropped.empty? ? "spec-clean" : "stripped #{dropped.join(", ")}")
end
puts "Packages written to #{options[:out].sub("#{ROOT}/", "")}"
