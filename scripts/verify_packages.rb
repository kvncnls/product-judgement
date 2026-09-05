#!/usr/bin/env ruby
# frozen_string_literal: true

# Verify the archives users actually download, including all supporting files.
# Ruby 2.6 standard library plus system unzip; no runtime dependencies for skills.
require "open3"
require "optparse"
require "yaml"

ROOT = File.expand_path("..", __dir__)
SKILLS = %w[focal compass flywheel soul product-judgement].freeze
SPEC_KEYS = %w[name description license compatibility metadata allowed-tools].freeze
options = { dir: File.join(ROOT, "dist"), skills: [] }
OptionParser.new do |parser|
  parser.banner = "Usage: ruby scripts/verify_packages.rb [--dir DIR] [--skill NAME]"
  parser.on("--dir DIR", "Archive directory (default: dist/)") { |value| options[:dir] = File.expand_path(value) }
  parser.on("--skill NAME", "Verify one archive; repeatable, skips combined archive") { |value| options[:skills] << value }
  parser.on("-h", "--help") { puts parser; exit 0 }
end.parse!
abort "Unexpected arguments: #{ARGV.join(' ')}" unless ARGV.empty?
selected = options[:skills].empty? ? SKILLS : options[:skills].uniq
abort "Unknown Skill" unless (selected - SKILLS).empty?

def unzip(*args)
  stdout, stderr, status = Open3.capture3("unzip", *args)
  raise "unzip failed: #{stderr.strip}" unless status.success?
  stdout
rescue Errno::ENOENT
  raise "unzip is required to verify upload packages"
end

def document(text, path)
  text = text.dup.force_encoding("UTF-8")
  raise "#{path}: invalid UTF-8" unless text.valid_encoding?
  match = text.match(/\A---\n(.*?)\n---\n/m)
  raise "#{path}: missing frontmatter" unless match
  metadata = YAML.safe_load(match[1], permitted_classes: [], aliases: false)
  raise "#{path}: frontmatter is not a mapping" unless metadata.is_a?(Hash)
  [metadata, text[match.end(0)..-1]]
end

def expected_files(skills)
  skills.flat_map do |skill|
    Dir.glob(File.join(ROOT, skill, "**", "*"), File::FNM_DOTMATCH).select do |path|
      File.file?(path) && File.basename(path) != ".DS_Store"
    end.map { |path| path.delete_prefix(ROOT + "/") }
  end.sort
end

def verify_archive(archive, skills)
  raise "Missing archive: #{archive}" unless File.file?(archive)
  entries = unzip("-Z1", archive).lines.map(&:chomp)
  unsafe = entries.select do |entry|
    entry.empty? || entry.start_with?("/", "\\") || entry.include?("\\") ||
      entry.split("/").include?("..") || !skills.include?(entry.split("/").first)
  end
  raise "#{archive}: unexpected or unsafe paths #{unsafe.inspect}" unless unsafe.empty?
  raise "#{archive}: duplicate entries" unless entries.uniq == entries
  files = entries.reject { |entry| entry.end_with?("/") }.sort
  expected = expected_files(skills)
  unless files == expected
    raise "#{archive}: missing #{(expected - files).inspect}; extra #{(files - expected).inspect}"
  end

  files.each do |entry|
    packed = unzip("-p", archive, entry)
    source = File.binread(File.join(ROOT, entry))
    unless entry.end_with?("/SKILL.md")
      raise "#{archive}: #{entry} differs from source" unless packed.b == source.b
      next
    end
    metadata, body = document(packed, entry)
    canonical, canonical_body = document(source, "source #{entry}")
    unknown = metadata.keys - SPEC_KEYS
    raise "#{archive}: #{entry} contains unsupported keys #{unknown.inspect}" unless unknown.empty?
    expected_metadata = canonical.select { |key, _value| SPEC_KEYS.include?(key) }
    raise "#{archive}: #{entry} changed supported metadata" unless metadata == expected_metadata
    raise "#{archive}: #{entry} changed instructions" unless body == canonical_body
    raise "#{archive}: #{entry} name does not match folder" unless metadata["name"] == entry.split("/").first
    description = metadata["description"]
    unless description.is_a?(String) && !description.strip.empty? && description.length <= 1024
      raise "#{archive}: #{entry} invalid description"
    end
  end
  puts "Verified #{File.basename(archive)}: #{skills.length} Skill(s), #{files.length} source files, spec-compatible metadata."
end

begin
  selected.each { |skill| verify_archive(File.join(options[:dir], "#{skill}.zip"), [skill]) }
  if options[:skills].empty?
    verify_archive(File.join(options[:dir], "product-judgement-all-skills.zip"), SKILLS)
  end
rescue StandardError => error
  warn "Package verification failed: #{error.message}"
  exit 1
end
