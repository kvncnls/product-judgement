#!/usr/bin/env ruby
# frozen_string_literal: true

require "fileutils"
require "open3"
require "rbconfig"
require "tmpdir"

ROOT = File.expand_path("..", __dir__)
RUBY = RbConfig.ruby

def run(*argv, **options)
  stdout, stderr, status = Open3.capture3(*argv, **options)
  [stdout + stderr, status.success?]
end

def expect_success(*argv, **options)
  output, success = run(*argv, **options)
  raise "#{argv.inspect}: #{output}" unless success
end

Dir.mktmpdir("pj-package-tests-") do |directory|
  dist = File.join(directory, "dist")
  expect_success(RUBY, File.join(ROOT, "scripts/package_skills.rb"), "--out", dist)
  expect_success(RUBY, File.join(ROOT, "scripts/verify_packages.rb"), "--dir", dist)
  original = File.join(directory, "original.zip")
  focal = File.join(dist, "focal.zip")
  FileUtils.cp(focal, original)
  extracted = File.join(directory, "extracted")
  FileUtils.mkdir_p(extracted)
  expect_success("unzip", "-q", original, "-d", extracted)
  skill = File.join(extracted, "focal/SKILL.md")
  clean = File.read(skill)

  {
    "unsupported upload metadata" => clean.sub("---\n", "---\nargument-hint: rejected\n"),
    "changed skill instructions" => clean + "\nUnreviewed instruction.\n"
  }.each do |label, content|
    FileUtils.cp(original, focal)
    File.write(skill, content)
    expect_success("zip", "-q", focal, "focal/SKILL.md", chdir: extracted)
    _output, success = run(RUBY, File.join(ROOT, "scripts/verify_packages.rb"), "--dir", dist, "--skill", "focal")
    raise "Verifier accepted #{label}" if success
  end

  FileUtils.cp(original, focal)
  expect_success("zip", "-qd", focal, "focal/LICENSE")
  _output, success = run(RUBY, File.join(ROOT, "scripts/verify_packages.rb"), "--dir", dist, "--skill", "focal")
  raise "Verifier accepted an incomplete package" if success
end
puts "Package tests passed: complete archives accepted; unsupported metadata, changed instructions, and missing files rejected."
