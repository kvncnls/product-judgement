#!/usr/bin/env ruby
# frozen_string_literal: true

# Behavioral evaluation harness for the Skill collection.
#
# verify.rb guards spelling: it proves a sentence is still in a file. This script
# guards behavior: it runs each fixture in tests/behavioral-contracts.yml against a
# model with the working tree's Skills loaded, has a second model grade the
# transcript against the fixture's assertions, and reports a per-assertion k/N pass
# rate. It costs money and model tokens, it is not deterministic, and it must never
# run in CI by default. Nothing in verify.rb or in .github/workflows may invoke it.
#
# Read tests/README.md and section 5 of the design notes before trusting a green
# run. The short version: with --repeat 3 this catches gross regressions and is
# blind to drift; without --ablation it may be measuring the base model rather than
# the instructions; and it scores boundary compliance, never craft.
#
# Ruby 2.6 only (the macOS system interpreter), standard library only. No gems, no
# bundler. Nothing newer than 2.6 syntax: no filter_map, tally, Hash#except, then,
# endless defs, case/in, _1, or beginless ranges.

require "digest"
require "fileutils"
require "json"
require "optparse"
require "set"
require "shellwords"
require "timeout"
require "tmpdir"
require "yaml"

ROOT = File.expand_path("..", __dir__)

# "shared" in a fixture names no runnable Skill. It expands to the four local
# Skills and the fixture passes only if all four arms pass; each arm is its own row.
LOCAL_SKILLS = %w[focal compass flywheel soul].freeze
ALL_SKILLS = (LOCAL_SKILLS + %w[product-judgement]).freeze

FIXTURE_PATH = File.join(ROOT, "tests", "behavioral-contracts.yml")
CALIBRATION_DIR = File.join(ROOT, "tests", "judge-calibration")
ARTIFACT_SCHEMA = "product-judgement.eval/1"

# Pinned full dated ids, never the moving aliases "sonnet"/"opus"/"fable". An alias
# silently changes model under you and turns last month's green into an
# unexplainable red.
#
# UNVERIFIED: these two ids were not resolved against this account, because doing so
# costs model tokens. If either is wrong the run fails as a harness error (is_error
# true, exit 2), which is the correct failure mode: it reports "we learned nothing",
# not "the Skill regressed". Override with --model / --judge-model.
DEFAULT_MODEL = "claude-sonnet-4-5-20250929"
DEFAULT_JUDGE_MODEL = "claude-haiku-4-5-20251001"

# The candidate keeps Read/Glob/Grep because every Skill instructs a read of its own
# reference/*.md. Disabling all tools would test a crippled Skill. Deny the rest.
CANDIDATE_DENY_TOOLS = "Bash,Edit,Write,NotebookEdit,WebFetch,WebSearch,Task"
JUDGE_BUDGET_USD = "0.20"

EXIT_OK = 0
EXIT_REGRESSION = 1
EXIT_HARNESS = 2
EXIT_NO_MATCH = 3
EXIT_FIXTURE_QUALITY = 4

class RunnerError < StandardError; end
class JudgeError < StandardError; end

# ---------------------------------------------------------------------------
# Judge contract
# ---------------------------------------------------------------------------

JUDGE_SYSTEM_PROMPT = <<~PROMPT
  You are a strict contract grader for a design-methodology skill collection. You are
  given (1) a numbered list of assertions and (2) a candidate transcript. For each
  assertion you return a verdict and a verbatim excerpt from the transcript that
  justifies it.

  Rules you must follow exactly.

  1. Judge only the candidate transcript. You have no other evidence. Do not use what
     you believe a good design review should say. Do not reward effort, length,
     formatting, or confident tone.
  2. Every excerpt must be copied character-for-character from the transcript. Never
     paraphrase, summarize, translate, correct, or complete an excerpt. If you cannot
     copy a span that justifies your verdict, the verdict is not "pass".
  3. Assertions are of two kinds.
     - kind "expected": pass only if the transcript actually does the thing. An
       assertion the transcript merely gestures at, or does adjacently, is "fail".
       Absence of evidence is "fail", not "pass".
     - kind "reject": this describes a behavior the transcript must NOT exhibit. pass
       means the transcript does not do it; fail means it does. For a "reject" that
       passes, set excerpt to "" and state in one clause what you looked for and did
       not find.
  4. Use "unclear" only when the transcript addresses the assertion's subject but the
     wording genuinely permits both readings. "unclear" is not a way to avoid
     deciding, and it does not mean "partially". Never use it because the assertion
     is hard.
  5. If the transcript is an error, a refusal, an empty string, or a clarifying
     question rather than an audit, mark every "expected" assertion "fail" with
     excerpt "" and reason "no audit produced".
  6. Judge each assertion independently. Do not let a strong overall impression carry
     a specific assertion, and do not let one failure drag down the others.
  7. Output only the JSON object. No preamble, no code fence, no commentary.
PROMPT

JUDGE_SCHEMA = {
  "type" => "object",
  "additionalProperties" => false,
  "required" => %w[verdicts],
  "properties" => {
    "verdicts" => {
      "type" => "array",
      "minItems" => 1,
      "items" => {
        "type" => "object",
        "additionalProperties" => false,
        "required" => %w[n kind verdict excerpt reason],
        "properties" => {
          "n" => { "type" => "integer", "minimum" => 1 },
          "kind" => { "type" => "string", "enum" => %w[expected reject] },
          "verdict" => { "type" => "string", "enum" => %w[pass fail unclear] },
          "excerpt" => { "type" => "string", "maxLength" => 400 },
          "reason" => { "type" => "string", "maxLength" => 300 }
        }
      }
    }
  }
}.freeze

# ---------------------------------------------------------------------------
# Prompt rendering
# ---------------------------------------------------------------------------

# THE CARDINAL RULE. This is the only function in the file that builds a candidate
# prompt, and it takes exactly three values: the Skill name, the scenario, and the
# evidence list. It has no parameter through which a fixture's `expected` or `reject`
# list could reach the model, and no caller passes it a whole fixture. That is
# deliberate and structural: handing the grading contract to the thing being graded
# would turn the entire suite into a leak, and a reader should be able to see in one
# screen that it cannot happen.
#
# The "do not ask clarifying questions" line is necessary rather than leading: every
# Skill's routing section says to ask for the product when given no argument, and a
# clarifying question back is a null result, not a failure. "Use your contract's own
# convention" deliberately avoids naming "not shown" or "N/E", both of which are the
# answer to several fixtures.
def render_candidate_prompt(skill_name, scenario, evidence, invoke)
  prefix = invoke == "slash" ? "/#{skill_name} " : ""
  lines = []
  lines << "#{prefix}Audit this. Produce your normal output from the evidence below."
  lines << "Do not ask clarifying questions; if a field is unevidenced, use your contract's"
  lines << "own convention for that."
  lines << ""
  lines << "Scenario: #{scenario}"
  lines << ""
  lines << "Evidence:"
  evidence.each { |item| lines << "- #{item}" }
  lines.join("\n") + "\n"
end

# Deliberately withheld from the judge: the fixture id, the Skill name, and the
# scenario. Handing over the scenario invites the judge to reason about the correct
# answer instead of reading the transcript.
def render_judge_user_message(assertions, candidate_text)
  lines = []
  lines << "## Assertions"
  lines << ""
  assertions.each { |a| lines << "#{a["n"]}. [#{a["kind"]}] #{a["text"]}" }
  lines << ""
  lines << "## Candidate transcript"
  lines << ""
  lines << "<<<BEGIN TRANSCRIPT"
  lines << candidate_text.to_s
  lines << "END TRANSCRIPT"
  lines.join("\n") + "\n"
end

# ---------------------------------------------------------------------------
# Text normalization and excerpt verification
# ---------------------------------------------------------------------------

# Model output routinely re-types straight punctuation as curly, collapses a hard
# wrap into a space, or substitutes an em dash for a hyphen. None of those are
# fabrication, so normalize them away before deciding whether an excerpt is real.
PUNCTUATION_MAP = {
  "‘" => "'", "’" => "'", "‚" => "'", "‛" => "'",
  "“" => '"', "”" => '"', "„" => '"', "‟" => '"',
  "′" => "'", "″" => '"', "«" => '"', "»" => '"',
  "‐" => "-", "‑" => "-", "‒" => "-", "–" => "-",
  "—" => "-", "―" => "-", "−" => "-",
  " " => " ", " " => " ", " " => " ", " " => " ",
  "…" => "..."
}.freeze

# Two more that are only readable as escapes: an ideographic space and a BOM look
# like nothing at all in a source listing.
INVISIBLE_MAP = { "　" => " ", "﻿" => "" }.freeze

def normalize_for_match(text)
  out = text.to_s.dup
  PUNCTUATION_MAP.each { |from, to| out.gsub!(from, to) }
  INVISIBLE_MAP.each { |from, to| out.gsub!(from, to) }
  out.gsub!(/\s+/, " ")
  out.strip
end

# A looser form for the provenance probe only, where a model may drop Markdown
# emphasis markers while still reproducing the words. Never used to credit a judge
# verdict.
def normalize_loose(text)
  normalize_for_match(text).gsub(/[*_`]/, "").gsub(/\s+/, " ").strip
end

def excerpt_present?(excerpt, candidate_text)
  needle = normalize_for_match(excerpt)
  return false if needle.empty?

  haystack = normalize_for_match(candidate_text)
  return true if haystack.include?(needle)

  # Judges sometimes wrap the span they copied in quotes of their own.
  trimmed = needle.sub(/\A["']+/, "").sub(/["']+\z/, "")
  !trimmed.empty? && haystack.include?(trimmed)
end

# The highest-value anti-rubber-stamping control, and it costs zero tokens.
#
# For every `expected` verdict of "pass", the excerpt must be literally present in
# the candidate text after normalization; if it is not, the pass is not evidence of
# anything and is downgraded to "fail".
#
# For every `reject` verdict of "fail" the same check applies, but the downgrade
# target is "unclear", not "fail". A reject/fail is an accusation that the transcript
# did the forbidden thing; if the quote backing it is not in the transcript we can
# neither credit the accusation nor clear the transcript, and silently converting it
# to "pass" would make fabrication read as good news. "unclear" keeps it out of both
# k and N-minus-k and surfaces it in the fabricated_excerpts count instead.
#
# An empty excerpt on an `expected` pass is a separate, mechanical rule (rule 2 of
# the judge prompt) rather than a fabrication, so it is counted separately.
def adjudicate_verdicts!(verdicts, candidate_text)
  fabricated = 0
  empties = 0

  verdicts.each do |verdict|
    verdict["excerpt_verified"] = nil
    verdict["adjusted_from"] = nil
    verdict["adjust_reason"] = nil

    kind = verdict["kind"]
    call = verdict["verdict"]
    excerpt = verdict["excerpt"].to_s

    if kind == "expected" && call == "pass"
      if normalize_for_match(excerpt).empty?
        empties += 1
        verdict["adjusted_from"] = "pass"
        verdict["verdict"] = "fail"
        verdict["excerpt_verified"] = false
        verdict["adjust_reason"] = "empty excerpt on an expected pass"
      elsif excerpt_present?(excerpt, candidate_text)
        verdict["excerpt_verified"] = true
      else
        fabricated += 1
        verdict["adjusted_from"] = "pass"
        verdict["verdict"] = "fail"
        verdict["excerpt_verified"] = false
        verdict["adjust_reason"] = "excerpt not present in the candidate transcript"
      end
    elsif kind == "reject" && call == "fail"
      if normalize_for_match(excerpt).empty? || !excerpt_present?(excerpt, candidate_text)
        fabricated += 1
        verdict["adjusted_from"] = "fail"
        verdict["verdict"] = "unclear"
        verdict["excerpt_verified"] = false
        verdict["adjust_reason"] = "excerpt not present in the candidate transcript"
      else
        verdict["excerpt_verified"] = true
      end
    end
  end

  [fabricated, empties]
end

# Exercised by --dry-run so the one control the whole suite leans on is not taken on
# faith. Returns a list of [label, ok] pairs.
def excerpt_selftest
  transcript = "The journey is open‑ended: catalog search has no completion event.\n" \
               "It preserves the user’s filtered\nresult set on return."
  cases = []
  cases << ["curly apostrophe matches straight", excerpt_present?("the user's filtered result set", transcript)]
  cases << ["hard wrap collapses to a space", excerpt_present?("filtered result set", transcript)]
  cases << ["non-breaking hyphen matches ASCII", excerpt_present?("open-ended", transcript)]
  cases << ["quoted excerpt still matches", excerpt_present?("\"no completion event\"", transcript)]
  cases << ["absent span is rejected", !excerpt_present?("names a progress bar", transcript)]
  cases << ["empty excerpt is rejected", !excerpt_present?("   ", transcript)]

  verdicts = [
    { "n" => 1, "kind" => "expected", "verdict" => "pass", "excerpt" => "no completion event", "reason" => "x" },
    { "n" => 2, "kind" => "expected", "verdict" => "pass", "excerpt" => "invented span", "reason" => "x" },
    { "n" => 3, "kind" => "expected", "verdict" => "pass", "excerpt" => "", "reason" => "x" },
    { "n" => 4, "kind" => "reject", "verdict" => "fail", "excerpt" => "invented span", "reason" => "x" },
    { "n" => 5, "kind" => "reject", "verdict" => "pass", "excerpt" => "", "reason" => "x" }
  ]
  fabricated, empties = adjudicate_verdicts!(verdicts, transcript)
  cases << ["verified pass survives", verdicts[0]["verdict"] == "pass" && verdicts[0]["excerpt_verified"] == true]
  cases << ["fabricated expected pass becomes fail", verdicts[1]["verdict"] == "fail"]
  cases << ["empty expected pass becomes fail", verdicts[2]["verdict"] == "fail"]
  cases << ["fabricated reject fail becomes unclear", verdicts[3]["verdict"] == "unclear"]
  cases << ["clean reject pass is untouched", verdicts[4]["verdict"] == "pass" && verdicts[4]["adjusted_from"].nil?]
  cases << ["counters split fabrication from emptiness", fabricated == 2 && empties == 1]
  cases
end

# ---------------------------------------------------------------------------
# Subprocess runner
# ---------------------------------------------------------------------------

# Open3.capture3 has no timeout on Ruby 2.6, and `claude` spawns children, so
# killing only the parent leaves orphans burning tokens. Spawn into its own process
# group and signal the negative pgid.
def spawn_capture(cmd, stdin_data, timeout_s, chdir)
  out_r, out_w = IO.pipe
  err_r, err_w = IO.pipe
  in_r, in_w = IO.pipe

  begin
    pid = Process.spawn(*cmd, in: in_r, out: out_w, err: err_w, pgroup: true, chdir: chdir)
  rescue Errno::ENOENT => error
    [in_r, in_w, out_r, out_w, err_r, err_w].each { |io| io.close rescue nil }
    raise RunnerError, "cannot execute #{cmd.first.inspect}: #{error.message}"
  end

  [in_r, out_w, err_w].each { |io| io.close rescue nil }
  begin
    in_w.write(stdin_data)
  rescue SystemCallError # rubocop:disable Lint/SuppressedException
  end
  in_w.close rescue nil

  out = +""
  err = +""
  reader_out = Thread.new { out << out_r.read.to_s }
  reader_err = Thread.new { err << err_r.read.to_s }

  begin
    Timeout.timeout(timeout_s) do
      _, status = Process.waitpid2(pid)
      return [out, err, status, :ok]
    end
  rescue Timeout::Error
    Process.kill("-TERM", Process.getpgid(pid)) rescue nil
    sleep 0.5
    Process.kill("-KILL", Process.getpgid(pid)) rescue nil
    Process.waitpid2(pid) rescue nil
    [out, err, nil, :timeout]
  ensure
    reader_out.join(2)
    reader_err.join(2)
    out_r.close rescue nil
    err_r.close rescue nil
  end
end

# VERIFIED GOTCHA: the envelope reports subtype "success" even on a hard
# authentication failure. Key off is_error, never subtype. A terminal_reason of
# "api_error" is a harness error (exit 2), not a Skill failure -- conflating the two
# is how an expired OAuth token gets read as a behavioral regression.
def parse_envelope(stdout, stderr)
  raise RunnerError, "runner produced no stdout (stderr: #{stderr.to_s.strip[0, 300]})" if stdout.to_s.strip.empty?

  begin
    envelope = JSON.parse(stdout)
  rescue JSON::ParserError => error
    raise RunnerError, "unparseable --output-format json envelope: #{error.message.lines.first.to_s.strip}"
  end
  raise RunnerError, "envelope is not a JSON object" unless envelope.is_a?(Hash)
  raise RunnerError, envelope["result"].to_s[0, 400] if envelope["is_error"]

  envelope
end

def extract_json(text)
  stripped = text.to_s.strip.sub(/\A```(?:json)?\s*/, "").sub(/```\s*\z/, "")
  begin
    JSON.parse(stripped)
  rescue JSON::ParserError
    match = stripped[/\{.*\}/m]
    raise JudgeError, "no JSON in judge output" unless match

    JSON.parse(match)
  end
end

# UNCERTAIN: how --json-schema shapes the envelope was not verified (the probe
# session could not reach the API). It may leave `result` as a JSON string, replace
# it with a parsed object, or add a sibling key. Handle all three rather than assume.
def judge_payload(envelope)
  %w[structured_output structuredOutput structured_result json].each do |key|
    value = envelope[key]
    return value if value.is_a?(Hash)
    return extract_json(value) if value.is_a?(String) && !value.strip.empty?
  end

  result = envelope["result"]
  return result if result.is_a?(Hash)
  return { "verdicts" => result } if result.is_a?(Array)

  extract_json(result.to_s)
end

def verdicts_from(payload)
  return payload["verdicts"] if payload.is_a?(Hash) && payload["verdicts"].is_a?(Array)
  return payload if payload.is_a?(Array)

  raise JudgeError, "judge JSON has no verdicts array"
end

def shape_error(verdicts, assertions)
  return "verdicts is not an array" unless verdicts.is_a?(Array)
  unless verdicts.length == assertions.length
    return "expected #{assertions.length} verdicts, got #{verdicts.length}"
  end

  numbers = verdicts.map { |v| v.is_a?(Hash) ? v["n"] : nil }
  unless numbers.sort == (1..assertions.length).to_a
    return "verdict n values are #{numbers.inspect}, expected exactly 1..#{assertions.length}"
  end

  assertions.each do |assertion|
    verdict = verdicts.find { |v| v.is_a?(Hash) && v["n"] == assertion["n"] }
    return "verdict #{assertion["n"]} is not an object" unless verdict.is_a?(Hash)
    unless verdict["kind"] == assertion["kind"]
      return "verdict #{assertion["n"]} kind #{verdict["kind"].inspect} disagrees with assertion kind #{assertion["kind"].inspect}"
    end
    unless %w[pass fail unclear].include?(verdict["verdict"])
      return "verdict #{assertion["n"]} verdict #{verdict["verdict"].inspect} is not pass/fail/unclear"
    end
  end

  nil
end

# ---------------------------------------------------------------------------
# argv construction
# ---------------------------------------------------------------------------

def candidate_argv(opts)
  [
    "claude", "-p",
    "--output-format", "json",
    "--model", opts[:model],
    "--plugin-dir", ROOT,
    "--add-dir", ROOT,
    "--restricted",
    "--strict-mcp-config",
    "--setting-sources", "",
    "--no-session-persistence",
    "--disallowed-tools", CANDIDATE_DENY_TOOLS,
    "--exclude-dynamic-system-prompt-sections",
    "--max-budget-usd", format("%.4f", opts[:per_run_budget])
  ]
end

# --safe-mode disables CLAUDE.md, skills, plugins and hooks, so this arm sees the
# base model on the same prompt. No --plugin-dir and no --add-dir: with the Skills
# off there is nothing in the working tree it should be reading.
def ablation_argv(opts)
  [
    "claude", "-p",
    "--output-format", "json",
    "--model", opts[:model],
    "--safe-mode",
    "--restricted",
    "--strict-mcp-config",
    "--setting-sources", "",
    "--no-session-persistence",
    "--disallowed-tools", CANDIDATE_DENY_TOOLS,
    "--exclude-dynamic-system-prompt-sections",
    "--max-budget-usd", format("%.4f", opts[:per_run_budget])
  ]
end

# --tools "" is load-bearing on the judge: it stops the judge going and reading the
# Skill source to decide what should have happened instead of what the transcript
# says.
def judge_argv(opts, system_prompt_path)
  [
    "claude", "-p",
    "--output-format", "json",
    "--json-schema", JSON.generate(JUDGE_SCHEMA),
    "--model", opts[:judge_model],
    "--system-prompt-file", system_prompt_path,
    "--tools", "",
    "--restricted",
    "--strict-mcp-config",
    "--setting-sources", "",
    "--no-session-persistence",
    "--max-budget-usd", JUDGE_BUDGET_USD
  ]
end

# Shell-quoted so a --dry-run line can be pasted into a terminal verbatim. The
# empty-string arguments (--tools "", --setting-sources "") are load-bearing and
# would vanish without quoting.
def display_argv(argv)
  argv.map do |raw|
    part = raw.to_s
    # The inline JSON schema is 500 characters of braces; shell-escaped it drowns the
    # rest of the line. Its sha is printed separately.
    if part.length > 120 && part.start_with?("{")
      "'<json-schema #{part.length} chars, sha #{Digest::SHA256.hexdigest(part)[0, 8]}>'"
    else
      Shellwords.escape(part)
    end
  end.join(" ")
end

# ---------------------------------------------------------------------------
# Provenance preflight: is the working tree what actually got loaded?
# ---------------------------------------------------------------------------
#
# This machine has focal, compass, flywheel, soul and product-judgement installed as
# global Skills. If --plugin-dir loses precedence to an installed copy, this harness
# grades the last release, reports green, and gives you confidence about code you
# just changed and never executed. It fails silently and looks identical to success,
# which makes it the single most expensive way this script can lie.
#
# The check works without touching any SKILL.md, because the working tree already
# carries something unique that can be computed at runtime: a line of its own prose.
# For each Skill under test we
#   1. locate every installed copy of that Skill's SKILL.md,
#   2. compare bytes with the working tree,
#   3. if they differ, pick a prose line that exists in the working-tree SKILL.md and
#      in none of the installed copies -- the discriminator,
#   4. slide a 14-word window along that line, past the first eight words, until the
#      window's text appears in no installed copy at all -- the needle. Checking the
#      needle rather than the whole line matters: a working-tree line is often an
#      installed line with a clause appended, so a span taken from its shared opening
#      would prove nothing,
#   5. ask the loaded Skill, in one cheap call, to reproduce the line, handing over
#      only its first eight words as the anchor, and assert the needle is in the
#      reply.
#
# WHAT A PASS PROVES: the text in the model's context for that Skill contained a span
# of prose that exists only in the working tree. The working tree's SKILL.md is
# therefore what reached the model.
#
# WHAT A PASS DOES NOT PROVE:
#   (a) that reference/*.md resolved from the working tree. Those are read by tool
#       call at runtime; a Read of ROOT/<skill>/reference/x.md returns working-tree
#       bytes no matter which SKILL.md was loaded, so no probe here can settle it.
#   (b) that an installed copy was not ALSO loaded alongside the working tree. Two
#       copies of the same Skill in context is a different failure and is invisible
#       to this check.
#   (c) anything at all when the working tree and every installed copy are
#       byte-identical. The check is then vacuous -- and harmless, because loading
#       either yields the same bytes. That case is recorded as "moot", not "proven".
#   (d) immunity to guessing. The probe hands over eight words, so a model could in
#       principle complete the rest. Mitigated by taking the needle strictly after
#       those eight words, requiring at least 14 further words and 40 characters, and
#       requiring an exact normalized match. Not eliminated.
#   (e) that the reply came from context rather than from pretraining. A widely
#       published sentence would be a bad needle; these are unreleased edits to an
#       unpublished working tree, which is the only reason this works at all.
#
# When differences exist but no discriminator can be built, the run aborts with
# exit 2. An unprovable provenance claim is worth less than no run at all.

INSTALL_ROOT_CANDIDATES = [
  "~/.claude/skills",
  "~/.config/claude/skills",
  "~/.agents/skills",
  "~/.cursor/skills",
  "~/.cursor/skills-cursor",
  "~/.codex/skills",
  "~/.claude/plugins/cache",
  "~/.claude/plugins/marketplaces",
  "/usr/local/share/claude/skills",
  "/opt/homebrew/share/claude/skills"
].freeze

def installed_skill_paths(skill_name)
  found = []
  INSTALL_ROOT_CANDIDATES.each do |raw_root|
    base = File.expand_path(raw_root)
    next unless File.directory?(base)

    # Bounded globs on purpose: an unbounded ** under the plugin cache can walk a
    # very large tree for no benefit.
    [
      File.join(base, skill_name, "SKILL.md"),
      File.join(base, "*", skill_name, "SKILL.md"),
      File.join(base, "*", "*", skill_name, "SKILL.md"),
      File.join(base, "*", "*", "*", skill_name, "SKILL.md")
    ].each { |pattern| found.concat(Dir.glob(pattern)) }
  end

  found.map { |path| File.realpath(path) rescue path }
       .uniq
       .reject { |path| path == File.join(ROOT, skill_name, "SKILL.md") }
       .select { |path| File.file?(path) }
end

def strip_frontmatter(text)
  match = text.match(/\A---\n.*?\n---\n/m)
  match ? text[match[0].length..-1].to_s : text
end

PROVENANCE_PREFIX_WORDS = 8
PROVENANCE_NEEDLE_WORDS = 14
PROVENANCE_NEEDLE_MIN_CHARS = 40

# Prose only. Headings, table rules, fenced code and the ASCII diagrams in the Skill
# bodies are all things a model will not reproduce byte-for-byte. No upper length
# bound: the longest lines in these files are single-paragraph rules, and they make
# the best discriminators precisely because they are the most heavily edited.
def quotable_line?(line)
  return false unless line.length >= 80
  return false if line.match?(/[─-╿]/)
  return false if line.include?("```") || line.include?("|")
  return false if line.match?(/\A\s*#/)
  return false if line.match?(/\A\s{4,}/)
  return false unless line.match?(/[a-z]{4}/)
  return false unless normalize_loose(line).split(" ").length >= PROVENANCE_PREFIX_WORDS + PROVENANCE_NEEDLE_WORDS

  true
end

# Slide a window along the line, starting past the words handed to the model, and
# return the first span that appears in no installed copy. A working-tree line is
# frequently an installed line with a clause appended, so a span taken from the
# shared opening would prove nothing at all.
def choose_needle(line, installed_blobs)
  words = normalize_loose(line).split(" ")
  start = PROVENANCE_PREFIX_WORDS
  while start + PROVENANCE_NEEDLE_WORDS <= words.length
    needle = words[start, PROVENANCE_NEEDLE_WORDS].join(" ")
    if needle.length >= PROVENANCE_NEEDLE_MIN_CHARS &&
       installed_blobs.none? { |blob| blob.include?(needle) }
      return needle
    end

    start += 1
  end
  nil
end

def build_provenance_plan(skill_name)
  working_path = File.join(ROOT, skill_name, "SKILL.md")
  plan = {
    "skill" => skill_name,
    "working_tree_path" => working_path,
    "working_tree_sha256" => nil,
    "installed_copies" => [],
    "status" => "moot",
    "discriminator" => nil,
    "prefix" => nil,
    "needle" => nil,
    "note" => nil
  }

  unless File.file?(working_path)
    plan["status"] = "undecidable"
    plan["note"] = "working tree has no #{skill_name}/SKILL.md"
    return plan
  end

  working_text = File.read(working_path, encoding: "UTF-8")
  plan["working_tree_sha256"] = Digest::SHA256.hexdigest(working_text)

  installed = installed_skill_paths(skill_name)
  divergent_texts = []
  installed.each do |path|
    text = begin
      File.read(path, encoding: "UTF-8")
    rescue SystemCallError
      nil
    end
    identical = !text.nil? && Digest::SHA256.hexdigest(text) == plan["working_tree_sha256"]
    plan["installed_copies"] << {
      "path" => path,
      "sha256" => text.nil? ? nil : Digest::SHA256.hexdigest(text),
      "identical_to_working_tree" => identical
    }
    divergent_texts << text.to_s unless identical
  end

  if divergent_texts.empty?
    plan["note"] = installed.empty? ? "no installed copy found" : "every installed copy is byte-identical to the working tree"
    return plan
  end

  # One normalized blob per divergent installed copy: a needle must be absent from
  # all of them, since any one of them could be the copy that wins precedence.
  installed_blobs = divergent_texts.map { |text| normalize_loose(text) }

  # The five Skills share boilerplate paragraphs, so the longest working-tree-only
  # line in focal/SKILL.md is often word-for-word the one in soul/SKILL.md. Such a
  # needle still separates working tree from installed copy, which is the question
  # being asked, but a needle unique to this Skill is strictly better, so try the
  # narrower corpus first and only widen if nothing qualifies.
  sibling_blobs = (ALL_SKILLS - [skill_name]).map do |sibling|
    path = File.join(ROOT, sibling, "SKILL.md")
    File.file?(path) ? normalize_loose(File.read(path, encoding: "UTF-8")) : nil
  end.compact

  candidates = strip_frontmatter(working_text).each_line.map { |line| line.chomp }
  candidates = candidates.select { |line| quotable_line?(line) }
  # Longest first: the more words past the anchor, the less a model could guess.
  candidates = candidates.sort_by { |line| -line.length }

  chosen = nil
  needle = nil
  unique_to_skill = false
  [installed_blobs + sibling_blobs, installed_blobs].each_with_index do |corpus, pass|
    candidates.each do |line|
      found = choose_needle(line, corpus)
      next if found.nil?

      chosen = line
      needle = found
      unique_to_skill = pass.zero?
      break
    end
    break unless chosen.nil?
  end

  if chosen.nil?
    plan["status"] = "undecidable"
    plan["note"] = "#{plan["installed_copies"].length} installed copy/copies diverge from the working tree, " \
                   "but no working-tree-only span of prose was found in SKILL.md to probe with"
    return plan
  end

  plan["status"] = "pending"
  plan["discriminator"] = chosen
  plan["prefix"] = normalize_loose(chosen).split(" ").first(PROVENANCE_PREFIX_WORDS).join(" ")
  plan["needle"] = needle
  plan["needle_unique_to_skill"] = unique_to_skill
  plan["note"] = "#{plan["installed_copies"].length} installed copy/copies diverge; " \
                 "probing with a #{PROVENANCE_NEEDLE_WORDS}-word span that exists only in the working tree" \
                 "#{unique_to_skill ? " and only in this Skill" : " (shared with a sibling Skill's working tree)"}"
  plan
end

def render_provenance_prompt(skill_name, prefix)
  lines = []
  lines << "/#{skill_name} PROVENANCE CHECK. Do not run an audit. Do not read any files."
  lines << "One line of your loaded instructions contains this phrase:"
  lines << "  #{prefix}"
  lines << "Reply with that entire line, copied verbatim from your instructions, on a single"
  lines << "line, and nothing else."
  lines << "If your instructions contain no such phrase, reply with exactly: ABSENT"
  lines.join("\n") + "\n"
end

def provenance_satisfied?(response, needle)
  answer = normalize_loose(response)
  return false if answer.empty? || answer == "ABSENT"

  answer.include?(needle)
end

# ---------------------------------------------------------------------------
# Fixtures and rows
# ---------------------------------------------------------------------------

def canonical_fixture_yaml(fixture)
  ordered = {}
  fixture.keys.sort.each { |key| ordered[key] = fixture[key] }
  ordered.to_yaml
end

def load_fixtures(path)
  fixtures = YAML.safe_load(File.read(path, encoding: "UTF-8"), permitted_classes: [], aliases: false)
  raise "#{path}: expected a top-level list of fixtures" unless fixtures.is_a?(Array)

  fixtures.each_with_index do |fixture, index|
    raise "#{path}: fixture #{index + 1} is not a mapping" unless fixture.is_a?(Hash)

    %w[id skill scenario].each do |key|
      raise "#{path}: fixture #{index + 1} needs a #{key}" unless fixture[key].is_a?(String) && !fixture[key].strip.empty?
    end
    %w[evidence expected reject].each do |key|
      value = fixture[key]
      valid = value.is_a?(Array) && !value.empty? && value.all? { |item| item.is_a?(String) && !item.strip.empty? }
      raise "#{path}: fixture #{fixture["id"]} needs a non-empty #{key} list" unless valid
    end
  end
  fixtures
end

def build_assertions(fixture)
  assertions = []
  fixture["expected"].each { |text| assertions << { "kind" => "expected", "text" => text } }
  fixture["reject"].each { |text| assertions << { "kind" => "reject", "text" => text } }
  assertions.each_with_index { |assertion, index| assertion["n"] = index + 1 }
  assertions
end

def assertion_label(assertions, assertion)
  kind_letter = assertion["kind"] == "expected" ? "E" : "R"
  ordinal = assertions.select { |other| other["kind"] == assertion["kind"] }.index(assertion) + 1
  "#{kind_letter}#{ordinal}"
end

def expand_rows(fixtures, opts)
  rows = []
  fixtures.each do |fixture|
    declared = fixture["skill"]
    skills = declared == "shared" ? LOCAL_SKILLS : [declared]

    skills.each do |skill_name|
      label = declared == "shared" ? "#{fixture["id"]} [shared -> #{skill_name}]" : fixture["id"]
      rows << {
        "id" => fixture["id"],
        "label" => label,
        "slug" => declared == "shared" ? "#{fixture["id"]}.#{skill_name}" : fixture["id"],
        "declared_skill" => declared,
        "skill" => skill_name,
        "scenario" => fixture["scenario"],
        "evidence" => fixture["evidence"],
        "assertions" => build_assertions(fixture),
        "fixture_sha256" => Digest::SHA256.hexdigest(canonical_fixture_yaml(fixture)),
        "prompt" => nil,
        "prompt_sha256" => nil
      }
    end
  end

  rows.each do |row|
    prompt = render_candidate_prompt(row["skill"], row["scenario"], row["evidence"], opts[:invoke])
    row["prompt"] = prompt
    row["prompt_sha256"] = Digest::SHA256.hexdigest(prompt)
    # The ablation arm carries the same body without the slash invocation: with
    # --safe-mode the Skills are off, so a leading /focal is inert text that can only
    # confuse the base model. Everything after that first token is byte-identical.
    ablation = render_candidate_prompt(row["skill"], row["scenario"], row["evidence"], "auto")
    row["ablation_prompt"] = ablation
    row["ablation_prompt_sha256"] = Digest::SHA256.hexdigest(ablation)
  end

  rows
end

def filter_rows(rows, opts)
  selected = rows
  if opts[:skills].any?
    wanted = Set.new
    opts[:skills].each do |name|
      if name == "shared"
        LOCAL_SKILLS.each { |local| wanted << local }
        wanted << "shared"
      else
        wanted << name
      end
    end
    selected = selected.select { |row| wanted.include?(row["skill"]) || wanted.include?(row["declared_skill"]) }
  end
  if opts[:ids].any?
    selected = selected.select do |row|
      opts[:ids].any? { |glob| File.fnmatch?(glob, row["id"], File::FNM_CASEFOLD) }
    end
  end
  selected
end

# ---------------------------------------------------------------------------
# Option parsing
# ---------------------------------------------------------------------------

opts = {
  skills: [],
  ids: [],
  repeat: 3,
  model: DEFAULT_MODEL,
  judge_model: DEFAULT_JUDGE_MODEL,
  allow_self_judge: false,
  invoke: "slash",
  ablation: false,
  control: nil,
  control_given: false,
  calibrate: false,
  json_path: nil,
  out_dir: nil,
  dry_run: false,
  jobs: 2,
  timeout: 300,
  max_cost: nil,
  per_run_budget: 0.50,
  fail_under: 1.0,
  runner: "claude",
  allow_ci: false,
  verbose: false
}

parser = OptionParser.new do |o|
  o.banner = "Usage: scripts/eval.rb [options]"
  o.separator ""
  o.separator "Opt-in behavioral evaluation. Costs model tokens. Never run from CI or verify.rb."
  o.separator ""
  o.on("--skill NAME", "Filter on the fixture skill field (repeatable); \"shared\" means the four locals") { |v| opts[:skills] << v }
  o.on("--id GLOB", "fnmatch against the fixture id (repeatable)") { |v| opts[:ids] << v }
  o.on("--repeat N", Integer, "Repeats per row (default 3)") { |v| opts[:repeat] = v }
  o.on("--model NAME", "Candidate model, pinned full dated id (default #{DEFAULT_MODEL})") { |v| opts[:model] = v }
  o.on("--judge-model NAME", "Judge model (default #{DEFAULT_JUDGE_MODEL})") { |v| opts[:judge_model] = v }
  o.on("--allow-self-judge", "Permit judge model == candidate model") { opts[:allow_self_judge] = true }
  o.on("--invoke MODE", %w[slash auto], "slash (default) tests the Skill body; auto tests description triggering") { |v| opts[:invoke] = v }
  o.on("--ablation", "Add the no-Skill baseline arm and report NO SIGNAL rows") { opts[:ablation] = true }
  o.on("--control [N]", "Decoy-transcript judge control (default 2 when --ablation is on)") do |v|
    opts[:control_given] = true
    opts[:control] = v.nil? ? 2 : Integer(v)
  end
  o.on("--calibrate", "Grade tests/judge-calibration/*.yml instead of the fixtures") { opts[:calibrate] = true }
  o.on("--json PATH", "Write the machine artifact here instead of <out>/eval.json") { |v| opts[:json_path] = v }
  o.on("--out DIR", "Output directory (default tests/results/<UTC timestamp>)") { |v| opts[:out_dir] = v }
  o.on("--dry-run", "Render every prompt and argv, run nothing, exit 0") { opts[:dry_run] = true }
  o.on("--jobs N", Integer, "Parallel model calls (default 2, capped at 8)") { |v| opts[:jobs] = v }
  o.on("--timeout SEC", Integer, "Per model call timeout (default 300)") { |v| opts[:timeout] = v }
  o.on("--max-cost-usd X", Float, "Abort once summed total_cost_usd crosses this") { |v| opts[:max_cost] = v }
  o.on("--per-run-budget-usd X", Float, "Per candidate call budget (default 0.50)") { |v| opts[:per_run_budget] = v }
  o.on("--fail-under RATE", Float, "Per-assertion pass rate below which a row fails (default 1.0)") { |v| opts[:fail_under] = v }
  o.on("--runner NAME", %w[claude codex cursor], "Runner CLI (default claude)") { |v| opts[:runner] = v }
  o.on("--allow-ci", "Required to run when ENV[\"CI\"] is set") { opts[:allow_ci] = true }
  o.on("-v", "--verbose", "Print full prompts and per-run detail") { opts[:verbose] = true }
  o.on("-h", "--help", "Show this help") do
    puts o
    exit EXIT_OK
  end
end

begin
  parser.parse!(ARGV)
rescue OptionParser::ParseError => error
  warn "scripts/eval.rb: #{error.message}"
  warn parser.to_s
  exit EXIT_HARNESS
end

# CI GUARD, side one. Side two lives in verify.rb, which asserts that
# .github/workflows/verify.yml never mentions eval.rb. "Do not call it from CI" is a
# convention, and conventions decay; both sides are needed.
if ENV["CI"] && !opts[:allow_ci]
  warn "scripts/eval.rb costs model tokens and is opt-in. Pass --allow-ci to run it in CI."
  # Exit 2, not 1: refusing to run is "we learned nothing", not "the Skill regressed".
  # A CI job that reads 1 as a behavioral failure would be reading the wrong thing.
  exit EXIT_HARNESS
end

opts[:jobs] = 1 if opts[:jobs] < 1
opts[:jobs] = 8 if opts[:jobs] > 8
opts[:repeat] = 1 if opts[:repeat] < 1
opts[:control] = opts[:ablation] ? 2 : 0 unless opts[:control_given]
opts[:control] = 0 if opts[:control].nil?

if opts[:judge_model] == opts[:model] && !opts[:allow_self_judge]
  warn "scripts/eval.rb: judge model equals candidate model (#{opts[:model]}). Same-model self-grading inflates."
  warn "Pass --allow-self-judge to override, or set --judge-model to a different model."
  exit EXIT_HARNESS
end

unless opts[:runner] == "claude"
  warn "scripts/eval.rb: --runner #{opts[:runner]} is not implemented."
  warn "Neither codex nor cursor-agent has a per-session plugin loader, so those arms would have to"
  warn "inline the generated text from bundles/ and would test a different artifact than --plugin-dir"
  warn "loads. Their envelope contracts were also never verified here. Use --runner claude."
  exit EXIT_HARNESS
end

# ---------------------------------------------------------------------------
# Environment facts
# ---------------------------------------------------------------------------

def detect_cli_version
  out, _err, status, state = spawn_capture(%w[claude --version], "", 30, Dir.tmpdir)
  return "unknown" unless state == :ok && status && status.success?

  out.strip.empty? ? "unknown" : out.strip
rescue RunnerError
  "unavailable"
end

def git_fact(args)
  out, _err, status, state = spawn_capture(["git"] + args, "", 30, ROOT)
  return nil unless state == :ok && status && status.success?

  out
rescue RunnerError
  nil
end

cli_version = detect_cli_version
started_at = Time.now.utc
stamp = started_at.strftime("%Y%m%dT%H%M%SZ")
out_dir = File.expand_path(opts[:out_dir] || File.join(ROOT, "tests", "results", stamp))
json_path = opts[:json_path] ? File.expand_path(opts[:json_path]) : File.join(out_dir, "eval.json")

git_sha = (git_fact(%w[rev-parse --short HEAD]) || "").strip
git_dirty = !(git_fact(%w[status --porcelain]) || "").strip.empty?

# ---------------------------------------------------------------------------
# Row selection
# ---------------------------------------------------------------------------

if opts[:calibrate]
  calibration_files = Dir.glob(File.join(CALIBRATION_DIR, "*.yml")).sort
  if calibration_files.empty?
    warn "scripts/eval.rb --calibrate: no cases in tests/judge-calibration/*.yml."
    warn ""
    warn "Until those exist, \"the judge said pass\" is an unaudited claim wearing a JSON schema."
    warn "Hand-label five transcripts -- two clear passes, two clear fails, one genuinely"
    warn "borderline -- as files of this shape:"
    warn ""
    warn "  id: compass-open-ended-clear-pass"
    warn "  transcript: |"
    warn "    <the full candidate transcript>"
    warn "  assertions:"
    warn "    - kind: expected"
    warn "      text: Classify the journey as open-ended."
    warn "      verdict: pass"
    warn "    - kind: reject"
    warn "      text: Penalize the absence of a progress bar."
    warn "      verdict: pass"
    warn ""
    exit EXIT_NO_MATCH
  end
end

begin
  fixtures = load_fixtures(FIXTURE_PATH)
rescue StandardError => error
  warn "scripts/eval.rb: #{error.message}"
  exit EXIT_HARNESS
end

fixtures_sha = Digest::SHA256.hexdigest(File.read(FIXTURE_PATH, encoding: "UTF-8"))
all_rows = expand_rows(fixtures, opts)
rows = filter_rows(all_rows, opts)

# --calibrate replaces the fixture run rather than adding to it: it grades the judge
# against hand labels, so there is nothing to run the candidate arm on.
rows = [] if opts[:calibrate]

if rows.empty? && !opts[:calibrate]
  warn "scripts/eval.rb: no fixture matched the filters " \
       "(--skill #{opts[:skills].inspect}, --id #{opts[:ids].inspect}) " \
       "across #{all_rows.length} rows from #{fixtures.length} fixtures."
  exit EXIT_NO_MATCH
end

calibration_cases = []
if opts[:calibrate]
  Dir.glob(File.join(CALIBRATION_DIR, "*.yml")).sort.each do |path|
    begin
      raw = YAML.safe_load(File.read(path, encoding: "UTF-8"), permitted_classes: [], aliases: false)
    rescue Psych::SyntaxError => error
      warn "scripts/eval.rb: #{path}: #{error.message.lines.first.to_s.strip}"
      exit EXIT_HARNESS
    end
    unless raw.is_a?(Hash) && raw["assertions"].is_a?(Array)
      warn "scripts/eval.rb: #{path}: needs an assertions list"
      exit EXIT_HARNESS
    end
    transcript = raw["transcript"]
    if transcript.nil? && raw["transcript_path"].is_a?(String)
      transcript = File.read(File.expand_path(raw["transcript_path"], CALIBRATION_DIR), encoding: "UTF-8")
    end
    unless transcript.is_a?(String) && !transcript.strip.empty?
      warn "scripts/eval.rb: #{path}: needs a transcript or transcript_path"
      exit EXIT_HARNESS
    end
    assertions = raw["assertions"].each_with_index.map do |item, index|
      { "n" => index + 1, "kind" => item["kind"], "text" => item["text"], "label" => item["verdict"] }
    end
    calibration_cases << {
      "id" => raw["id"] || File.basename(path, ".yml"),
      "path" => path,
      "transcript" => transcript,
      "assertions" => assertions
    }
  end
end

# ---------------------------------------------------------------------------
# Provenance plans (zero model calls; the probe itself is a model call)
# ---------------------------------------------------------------------------

probe_skills = rows.map { |row| row["skill"] }.uniq.sort
provenance_plans = probe_skills.map { |skill_name| build_provenance_plan(skill_name) }

# ---------------------------------------------------------------------------
# Decoy control pairing
# ---------------------------------------------------------------------------

# Judge fixture A's assertions against fixture B's transcript, where B is a different
# fixture for the same Skill. A judge that passes the decoy's expected assertions is
# rubber-stamping, and no amount of prompt wording proves otherwise.
def plan_control_pairs(rows, sample)
  return [] if sample.to_i <= 0

  by_skill = {}
  rows.each do |row|
    by_skill[row["skill"]] ||= []
    by_skill[row["skill"]] << row
  end

  pairs = []
  rows.sort_by { |row| row["label"] }.each do |row|
    break if pairs.length >= sample.to_i

    partner = by_skill[row["skill"]].find { |other| other["slug"] != row["slug"] }
    next unless partner

    pairs << { "id" => row["label"], "slug" => row["slug"], "decoy_id" => partner["label"], "decoy_slug" => partner["slug"] }
  end
  pairs
end

control_pairs = plan_control_pairs(rows, opts[:control])

# ---------------------------------------------------------------------------
# Dry run
# ---------------------------------------------------------------------------

def print_block(text, indent)
  text.to_s.each_line { |line| puts "#{indent}#{line.chomp}" }
end

if opts[:dry_run]
  puts "product-judgement eval --dry-run - no model calls, nothing written"
  puts "candidate #{opts[:model]} - judge #{opts[:judge_model]} - cli #{cli_version}"
  puts "#{opts[:repeat]} repeats - invoke=#{opts[:invoke]} - ablation=#{opts[:ablation] ? "on" : "off"} " \
       "- jobs=#{opts[:jobs]} - timeout=#{opts[:timeout]}s - fail-under=#{opts[:fail_under]}"
  puts "fixtures #{FIXTURE_PATH.sub(ROOT + "/", "")} sha #{fixtures_sha[0, 8]} - git #{git_sha}#{git_dirty ? " (dirty)" : ""}"
  puts

  puts "EXCERPT VERIFIER SELF-CHECK"
  selftest = excerpt_selftest
  selftest.each { |label, ok| puts "  #{ok ? "ok  " : "FAIL"} #{label}" }
  failed = selftest.reject { |_label, ok| ok }
  unless failed.empty?
    warn "scripts/eval.rb: the excerpt verifier is broken (#{failed.length} self-check failure(s)). Refusing to go further."
    exit EXIT_HARNESS
  end
  puts

  puts "CANDIDATE ARGV (prompt on stdin, cwd = a fresh empty scratch dir)"
  puts "  #{display_argv(candidate_argv(opts))}"
  puts
  if opts[:ablation]
    puts "ABLATION ARGV"
    puts "  #{display_argv(ablation_argv(opts))}"
    puts
  end
  puts "JUDGE ARGV (assertions + transcript on stdin)"
  puts "  #{display_argv(judge_argv(opts, File.join(out_dir, "judge-system-prompt.txt")))}"
  puts "  judge system prompt sha #{Digest::SHA256.hexdigest(JUDGE_SYSTEM_PROMPT)[0, 16]} " \
       "(#{JUDGE_SYSTEM_PROMPT.length} chars, --system-prompt-file, full replacement)"
  puts "  judge json schema sha #{Digest::SHA256.hexdigest(JSON.generate(JUDGE_SCHEMA))[0, 16]}"
  puts

  puts "PROVENANCE PREFLIGHT (#{provenance_plans.length} skill(s), 1 model call each on a real run)"
  provenance_plans.each do |plan|
    puts "  #{plan["skill"]}: #{plan["status"]} - #{plan["note"]}"
    puts "    working tree #{plan["working_tree_sha256"].to_s[0, 12]} #{plan["working_tree_path"].sub(ROOT + "/", "")}"
    plan["installed_copies"].each do |copy|
      marker = copy["identical_to_working_tree"] ? "same" : "DIFF"
      puts "    installed    #{copy["sha256"].to_s[0, 12]} [#{marker}] #{copy["path"]}"
    end
    if plan["discriminator"]
      puts "    discriminator line (#{plan["discriminator"].length} chars):"
      puts "      #{plan["discriminator"][0, 140]}#{plan["discriminator"].length > 140 ? "..." : ""}"
      puts "    needle asserted in the reply (working tree only):"
      puts "      #{plan["needle"]}"
      puts "    probe prompt:"
      print_block(render_provenance_prompt(plan["skill"], plan["prefix"]), "      ")
    end
  end
  undecidable = provenance_plans.select { |plan| plan["status"] == "undecidable" }
  unless undecidable.empty?
    puts "  WOULD ABORT (exit #{EXIT_HARNESS}): provenance undecidable for #{undecidable.map { |plan| plan["skill"] }.join(", ")}"
  end
  puts

  puts "ROWS (#{rows.length} of #{all_rows.length}, from #{fixtures.length} fixtures)"
  rows.each do |row|
    puts "  #{row["label"]}"
    puts "    skill=#{row["skill"]} declared=#{row["declared_skill"]} " \
         "assertions=#{row["assertions"].length} " \
         "(#{row["assertions"].count { |a| a["kind"] == "expected" }} expected / " \
         "#{row["assertions"].count { |a| a["kind"] == "reject" }} reject)"
    puts "    fixture sha #{row["fixture_sha256"][0, 12]} - prompt sha #{row["prompt_sha256"][0, 12]} (#{row["prompt"].length} chars)"
    if opts[:ablation]
      puts "    ablation prompt sha #{row["ablation_prompt_sha256"][0, 12]} (#{row["ablation_prompt"].length} chars)"
    end
    if opts[:verbose]
      puts "    candidate prompt:"
      print_block(row["prompt"], "      ")
      puts "    judge user message:"
      print_block(render_judge_user_message(row["assertions"], "<candidate transcript for #{row["label"]}>"), "      ")
    end
  end
  puts

  unless control_pairs.empty?
    puts "JUDGE CONTROL (decoy transcripts)"
    control_pairs.each { |pair| puts "  #{pair["id"]} graded against the transcript of #{pair["decoy_id"]}" }
    puts
  end

  if opts[:calibrate]
    puts "CALIBRATION CASES (#{calibration_cases.length})"
    calibration_cases.each do |kase|
      puts "  #{kase["id"]} - #{kase["assertions"].length} labelled assertions - " \
           "#{kase["transcript"].length} char transcript - #{kase["path"].sub(ROOT + "/", "")}"
    end
    puts
  end

  arms = 1 + (opts[:ablation] ? 1 : 0)
  candidate_calls = rows.length * opts[:repeat] * arms
  judge_calls = candidate_calls + control_pairs.length + calibration_cases.length
  puts "WOULD RUN"
  puts "  #{provenance_plans.count { |plan| plan["status"] == "pending" }} provenance probe(s)"
  puts "  #{candidate_calls} candidate call(s) (#{rows.length} rows x #{opts[:repeat]} repeats x #{arms} arm(s))"
  puts "  #{judge_calls} judge call(s)"
  puts "  ceiling: #{opts[:max_cost] ? format("$%.2f", opts[:max_cost]) : "none (--max-cost-usd unset)"}" \
       " - per candidate call #{format("$%.2f", opts[:per_run_budget])} - per judge call $#{JUDGE_BUDGET_USD}"
  puts "  artifact #{json_path}"
  puts "  transcripts #{File.join(out_dir, "runs")}/"
  unless File.exist?(File.join(ROOT, ".gitignore")) && File.read(File.join(ROOT, ".gitignore")).include?("tests/results")
    puts "  note: tests/results/ is not in .gitignore; add it before committing a real run"
  end
  puts
  puts "Nothing ran. Exit 0."
  exit EXIT_OK
end

# ---------------------------------------------------------------------------
# Live run
# ---------------------------------------------------------------------------

selftest = excerpt_selftest
selftest_failures = selftest.reject { |_label, ok| ok }
unless selftest_failures.empty?
  warn "scripts/eval.rb: the excerpt verifier failed its own self-check " \
       "(#{selftest_failures.map { |label, _ok| label }.join("; ")}). Refusing to grade anything."
  exit EXIT_HARNESS
end

FileUtils.mkdir_p(File.join(out_dir, "runs"))
FileUtils.mkdir_p(File.dirname(json_path))
judge_system_path = File.join(out_dir, "judge-system-prompt.txt")
File.write(judge_system_path, JUDGE_SYSTEM_PROMPT)
scratch_dir = Dir.mktmpdir("pj-eval-")

cost_lock = Mutex.new
io_lock = Mutex.new
total_cost = 0.0
harness_errors = []
budget_exhausted = false

record_cost = lambda do |amount|
  cost_lock.synchronize do
    total_cost += amount.to_f
    if opts[:max_cost] && total_cost >= opts[:max_cost]
      budget_exhausted = true
    end
  end
end

note_harness_error = lambda do |message|
  io_lock.synchronize do
    harness_errors << message
    warn "  ! #{message}" if opts[:verbose]
  end
end

write_side_file = lambda do |name, content|
  path = File.join(out_dir, "runs", name)
  io_lock.synchronize { File.write(path, content.to_s) }
  File.join("runs", name)
end

# One candidate call. Returns a hash; on failure the hash carries "error".
call_candidate = lambda do |argv, prompt, slug|
  stdout, stderr, status, state = spawn_capture(argv, prompt, opts[:timeout], scratch_dir)
  if state == :timeout
    return { "error" => "timed out after #{opts[:timeout]}s", "cost_usd" => 0.0 }
  end

  begin
    envelope = parse_envelope(stdout, stderr)
  rescue RunnerError => error
    return {
      "error" => error.message,
      "cost_usd" => 0.0,
      "exit_status" => status && status.exitstatus
    }
  end

  record_cost.call(envelope["total_cost_usd"])
  text = envelope["result"].to_s
  envelope_path = write_side_file.call("#{slug}.envelope.json", JSON.pretty_generate(envelope))
  text_path = write_side_file.call("#{slug}.candidate.md", text)

  {
    "session_id" => envelope["session_id"],
    "num_turns" => envelope["num_turns"],
    "duration_ms" => envelope["duration_ms"],
    "cost_usd" => envelope["total_cost_usd"].to_f,
    "is_error" => envelope["is_error"] ? true : false,
    "terminal_reason" => envelope["terminal_reason"],
    "envelope_path" => envelope_path,
    "text_path" => text_path,
    "text_sha256" => Digest::SHA256.hexdigest(text),
    "chars" => text.length,
    "text" => text
  }
end

# One judge call, with a single retry on a parse or shape failure. Two bad shapes in
# a row is a harness error, never a pass.
call_judge = lambda do |assertions, candidate_text, slug|
  argv = judge_argv(opts, judge_system_path)
  message = render_judge_user_message(assertions, candidate_text)
  last_error = nil
  raw_path = nil
  cost = 0.0

  2.times do |attempt|
    stdout, stderr, _status, state = spawn_capture(argv, message, opts[:timeout], scratch_dir)
    if state == :timeout
      last_error = "judge timed out after #{opts[:timeout]}s"
      next
    end

    begin
      envelope = parse_envelope(stdout, stderr)
    rescue RunnerError => error
      last_error = "judge runner error: #{error.message}"
      next
    end

    record_cost.call(envelope["total_cost_usd"])
    cost += envelope["total_cost_usd"].to_f
    raw_path = write_side_file.call("#{slug}.judge#{attempt.zero? ? "" : ".retry"}.json", JSON.pretty_generate(envelope))

    begin
      verdicts = verdicts_from(judge_payload(envelope))
    rescue JudgeError, JSON::ParserError => error
      last_error = "judge JSON unusable: #{error.message}"
      next
    end

    problem = shape_error(verdicts, assertions)
    if problem
      last_error = "judge shape error: #{problem}"
      next
    end

    fabricated, empties = adjudicate_verdicts!(verdicts, candidate_text)
    # `return` from inside the retry loop, not `next`: `next` here would only start
    # the second attempt and throw the good result away.
    return {
      "session_id" => envelope["session_id"],
      "cost_usd" => cost,
      "raw_path" => raw_path,
      "attempts" => attempt + 1,
      "verdicts" => verdicts.sort_by { |verdict| verdict["n"] },
      "fabricated_excerpts" => fabricated,
      "empty_excerpt_downgrades" => empties
    }
  end

  { "error" => last_error || "judge produced nothing usable", "cost_usd" => cost, "raw_path" => raw_path }
end

# --- provenance preflight -------------------------------------------------

provenance_undecidable = provenance_plans.select { |plan| plan["status"] == "undecidable" }
unless provenance_undecidable.empty?
  warn "scripts/eval.rb: cannot prove the working tree is what would be loaded."
  provenance_undecidable.each { |plan| warn "  #{plan["skill"]}: #{plan["note"]}" }
  warn ""
  warn "This machine has these Skills installed globally. If --plugin-dir loses to an installed"
  warn "copy, this harness grades the last release and reports green on code you just changed."
  warn "Remedies: uninstall or move the global copy (~/.agents/skills, ~/.claude/skills), or make"
  warn "any prose edit inside the affected SKILL.md so a working-tree-only line exists to probe."
  exit EXIT_HARNESS
end

provenance_plans.each do |plan|
  next unless plan["status"] == "pending"

  prompt = render_provenance_prompt(plan["skill"], plan["prefix"])
  result = call_candidate.call(candidate_argv(opts), prompt, "provenance.#{plan["skill"]}")
  if result["error"]
    plan["status"] = "unproven"
    plan["note"] = "provenance probe failed: #{result["error"]}"
    next
  end

  plan["response_path"] = result["text_path"]
  if provenance_satisfied?(result["text"], plan["needle"])
    plan["status"] = "proven"
    plan["note"] = "the loaded instructions contained a span of prose that exists only in the working tree"
  else
    plan["status"] = "unproven"
    plan["note"] = "the loaded Skill could not reproduce the working-tree-only span; " \
                   "an installed copy probably won precedence over --plugin-dir"
  end
end

unproven = provenance_plans.select { |plan| plan["status"] == "unproven" }
unless unproven.empty?
  warn "scripts/eval.rb: provenance preflight FAILED for #{unproven.map { |plan| plan["skill"] }.join(", ")}."
  unproven.each { |plan| warn "  #{plan["skill"]}: #{plan["note"]}" }
  warn ""
  warn "Refusing to grade. A green run against the installed release is worse than no run:"
  warn "it reports confidence about code that never executed. Either remove the installed copies"
  warn "(~/.agents/skills, ~/.claude/skills) or stop using --plugin-dir and inline from bundles/."
  warn "Artifact of the failed preflight: #{out_dir}"
  exit EXIT_HARNESS
end

# --- work units -----------------------------------------------------------

units = []
rows.each do |row|
  arms = [["with-skill", candidate_argv(opts), row["prompt"], row["prompt_sha256"]]]
  if opts[:ablation]
    arms << ["no-skill", ablation_argv(opts), row["ablation_prompt"], row["ablation_prompt_sha256"]]
  end
  arms.each do |arm_name, argv, prompt, prompt_sha|
    opts[:repeat].times do |index|
      units << {
        "row" => row, "arm" => arm_name, "argv" => argv, "prompt" => prompt,
        "prompt_sha256" => prompt_sha, "run" => index + 1
      }
    end
  end
end

results_lock = Mutex.new
unit_results = []
queue = units.dup
queue_lock = Mutex.new

worker = lambda do
  loop do
    unit = queue_lock.synchronize { queue.shift }
    break if unit.nil?

    if budget_exhausted
      results_lock.synchronize do
        unit_results << unit.merge("skipped" => "cost ceiling reached before this run started")
      end
      next
    end

    row = unit["row"]
    slug = "#{row["slug"]}.#{unit["arm"]}.#{unit["run"]}"
    candidate = call_candidate.call(unit["argv"], unit["prompt"], slug)

    if candidate["error"]
      note_harness_error.call("#{row["label"]} #{unit["arm"]} run #{unit["run"]}: #{candidate["error"]}")
      results_lock.synchronize { unit_results << unit.merge("candidate" => candidate, "judge" => nil) }
      next
    end

    judge = call_judge.call(row["assertions"], candidate["text"], slug)
    if judge["error"]
      note_harness_error.call("#{row["label"]} #{unit["arm"]} run #{unit["run"]}: #{judge["error"]}")
    end
    results_lock.synchronize { unit_results << unit.merge("candidate" => candidate, "judge" => judge) }
  end
end

threads = Array.new([opts[:jobs], units.length].min) { Thread.new { worker.call } }
threads.each(&:join)

# --- decoy control --------------------------------------------------------

transcript_by_slug = {}
unit_results.each do |unit|
  next unless unit["arm"] == "with-skill"

  candidate = unit["candidate"]
  next if candidate.nil? || candidate["error"]

  transcript_by_slug[unit["row"]["slug"]] ||= candidate["text"]
end

control_results = []
control_pairs.each do |pair|
  decoy_text = transcript_by_slug[pair["decoy_slug"]]
  row = rows.find { |candidate_row| candidate_row["slug"] == pair["slug"] }
  if decoy_text.nil? || row.nil?
    control_results << pair.merge("skipped" => "no usable decoy transcript")
    next
  end

  judge = call_judge.call(row["assertions"], decoy_text, "control.#{pair["slug"]}")
  if judge["error"]
    note_harness_error.call("judge control #{pair["id"]}: #{judge["error"]}")
    control_results << pair.merge("error" => judge["error"])
    next
  end

  expected_count = row["assertions"].count { |assertion| assertion["kind"] == "expected" }
  decoy_passes = judge["verdicts"].count do |verdict|
    verdict["kind"] == "expected" && verdict["verdict"] == "pass"
  end
  control_results << pair.merge(
    "expected_assertions" => expected_count,
    "decoy_passes" => decoy_passes,
    "leak" => decoy_passes > 0,
    "raw_path" => judge["raw_path"]
  )
end

# --- calibration ----------------------------------------------------------

calibration_results = []
calibration_cases.each do |kase|
  judge = call_judge.call(kase["assertions"], kase["transcript"], "calibration.#{kase["id"]}")
  if judge["error"]
    note_harness_error.call("calibration #{kase["id"]}: #{judge["error"]}")
    calibration_results << { "id" => kase["id"], "error" => judge["error"] }
    next
  end

  agree = 0
  detail = []
  kase["assertions"].each do |assertion|
    verdict = judge["verdicts"].find { |candidate| candidate["n"] == assertion["n"] }
    got = verdict && verdict["verdict"]
    matched = !assertion["label"].nil? && got == assertion["label"]
    agree += 1 if matched
    detail << { "n" => assertion["n"], "label" => assertion["label"], "judge" => got, "agrees" => matched }
  end
  calibration_results << {
    "id" => kase["id"], "assertions" => kase["assertions"].length,
    "agreements" => agree, "rate" => (agree.to_f / kase["assertions"].length).round(3),
    "verdicts" => detail, "raw_path" => judge["raw_path"]
  }
end

# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------

def tally_arm(units_for_arm, row)
  counts = {}
  row["assertions"].each do |assertion|
    counts[assertion["n"]] = { "pass" => 0, "fail" => 0, "unclear" => 0, "missing" => 0, "failures" => [] }
  end

  units_for_arm.each do |unit|
    judge = unit["judge"]
    if judge.nil? || judge["error"]
      counts.each_value { |bucket| bucket["missing"] += 1 }
      next
    end

    judge["verdicts"].each do |verdict|
      bucket = counts[verdict["n"]]
      next if bucket.nil?

      call = verdict["verdict"]
      bucket[call] = bucket[call].to_i + 1
      if call != "pass" && bucket["failures"].length < 3
        excerpt = verdict["excerpt"].to_s.strip
        excerpt = verdict["reason"].to_s.strip if excerpt.empty?
        bucket["failures"] << "run #{unit["run"]} #{call}: #{excerpt[0, 120]}"
      end
    end
  end
  counts
end

report_rows = []
rows.each do |row|
  own = unit_results.select { |unit| unit["row"]["slug"] == row["slug"] }
  with_units = own.select { |unit| unit["arm"] == "with-skill" && !unit.key?("skipped") }
  without_units = own.select { |unit| unit["arm"] == "no-skill" && !unit.key?("skipped") }

  with_counts = tally_arm(with_units, row)
  attempted = with_units.length
  judged = with_units.count { |unit| unit["judge"] && !unit["judge"]["error"] }

  assertion_rows = row["assertions"].map do |assertion|
    bucket = with_counts[assertion["n"]]
    denominator = judged
    rate = denominator.zero? ? 0.0 : (bucket["pass"].to_f / denominator)
    unclear_rate = denominator.zero? ? 0.0 : (bucket["unclear"].to_f / denominator)
    {
      "n" => assertion["n"], "kind" => assertion["kind"], "text" => assertion["text"],
      "label" => assertion_label(row["assertions"], assertion),
      "pass" => bucket["pass"], "fail" => bucket["fail"], "unclear" => bucket["unclear"],
      "missing" => bucket["missing"], "denominator" => denominator, "rate" => rate.round(3),
      "ambiguous_assertion" => unclear_rate > (1.0 / 3.0),
      "failures" => bucket["failures"]
    }
  end

  expected_rows = assertion_rows.select { |entry| entry["kind"] == "expected" }
  with_rate = expected_rows.empty? ? 0.0 : (expected_rows.map { |entry| entry["rate"] }.reduce(0.0, :+) / expected_rows.length)

  without_rate = nil
  if opts[:ablation]
    without_counts = tally_arm(without_units, row)
    judged_without = without_units.count { |unit| unit["judge"] && !unit["judge"]["error"] }
    expected_assertions = row["assertions"].select { |assertion| assertion["kind"] == "expected" }
    if judged_without.zero? || expected_assertions.empty?
      without_rate = nil
    else
      rates = expected_assertions.map { |assertion| without_counts[assertion["n"]]["pass"].to_f / judged_without }
      without_rate = (rates.reduce(0.0, :+) / rates.length).round(3)
    end
  end

  status =
    if attempted.zero? || judged.zero? || judged < attempted
      "ERROR"
    elsif assertion_rows.any? { |entry| entry["pass"].zero? }
      "FAIL"
    elsif !without_rate.nil? && without_rate >= opts[:fail_under]
      "NO SIGNAL"
    elsif assertion_rows.any? { |entry| entry["pass"] < entry["denominator"] }
      "FLAKY"
    else
      "PASS"
    end

  report_rows << {
    "id" => row["id"], "label" => row["label"], "skill" => row["skill"], "arm" => "with-skill",
    "fixture_sha256" => row["fixture_sha256"], "prompt_sha256" => row["prompt_sha256"],
    "status" => status.downcase.tr(" ", "_"), "status_label" => status,
    "attempted" => attempted, "judged" => judged,
    "with_rate" => with_rate.round(3), "without_rate" => without_rate,
    "assertions" => assertion_rows,
    "runs" => own.map do |unit|
      candidate = unit["candidate"]
      judge = unit["judge"]
      {
        "run" => unit["run"], "arm" => unit["arm"], "skipped" => unit["skipped"],
        "candidate" => candidate.nil? ? nil : candidate.reject { |key, _value| key == "text" },
        "judge" => judge
      }
    end
  }
end

# ---------------------------------------------------------------------------
# Human report
# ---------------------------------------------------------------------------

def truncate(text, width)
  return text if text.length <= width

  text[0, width - 3] + "..."
end

finished_at = Time.now.utc
duration_s = (finished_at - started_at).round

puts "product-judgement eval - candidate #{opts[:model]} - judge #{opts[:judge_model]}"
puts "#{opts[:repeat]} repeats - invoke=#{opts[:invoke]} - ablation=#{opts[:ablation] ? "on" : "off"} " \
     "- cli #{cli_version} - fixtures sha #{fixtures_sha[0, 8]} - #{started_at.strftime("%Y-%m-%dT%H:%M:%SZ")}"
puts

report_rows.each do |entry|
  # The row number is the worst assertion's k over the number of judged repeats.
  # A single number per fixture would be a boolean in disguise, which is exactly the
  # information a non-deterministic runner cannot support.
  worst = entry["assertions"].map { |assertion| assertion["pass"] }.min.to_i
  denominator = entry["assertions"].empty? ? entry["judged"] : entry["assertions"].first["denominator"]
  puts format("%-60s  %s  %s", truncate(entry["label"], 60), "#{worst}/#{denominator}", entry["status_label"])
  if entry["judged"] < entry["attempted"]
    puts "     #{entry["attempted"] - entry["judged"]} of #{entry["attempted"]} repeats produced nothing judgeable"
  end
  entry["assertions"].each do |assertion|
    marker = ""
    marker = "  <- flaky" if assertion["pass"] > 0 && assertion["pass"] < assertion["denominator"]
    marker = "  <- zero" if assertion["pass"].zero?
    marker += "  <- ambiguous_assertion" if assertion["ambiguous_assertion"]
    puts format("  %-2s %-64s %s%s", assertion["label"], truncate(assertion["text"], 64),
                "#{assertion["pass"]}/#{assertion["denominator"]}", marker)
    assertion["failures"].each { |line| puts "     #{truncate(line, 100)}" }
  end
  puts
end

status_counts = { "PASS" => 0, "FLAKY" => 0, "FAIL" => 0, "ERROR" => 0, "NO SIGNAL" => 0 }
report_rows.each { |entry| status_counts[entry["status_label"]] += 1 }

unless opts[:calibrate]
  puts "#{report_rows.length} rows - #{status_counts["PASS"]} pass - #{status_counts["FLAKY"]} flaky - " \
       "#{status_counts["FAIL"]} fail - #{status_counts["ERROR"]} error - #{status_counts["NO SIGNAL"]} no signal"
end

if opts[:calibrate]
  # nothing: --calibrate grades the judge, so there is no candidate arm to ablate
elsif opts[:ablation]
  no_signal = report_rows.select { |entry| entry["status_label"] == "NO SIGNAL" }
  gated = report_rows.length - no_signal.length
  detail = no_signal.empty? ? "" : " (#{no_signal.map { |entry| entry["label"] }.join(", ")})"
  puts "ablation:      #{gated} gated on the skill - #{no_signal.length} NO SIGNAL#{detail}"
else
  puts "ablation:      off - these rows may be measuring the base model, not the instructions"
end

fabricated_total = 0
empty_total = 0
report_rows.each do |entry|
  entry["runs"].each do |run|
    judge = run["judge"]
    next if judge.nil? || judge["error"]

    fabricated_total += judge["fabricated_excerpts"].to_i
    empty_total += judge["empty_excerpt_downgrades"].to_i
  end
end
leaks = control_results.count { |result| result["leak"] }
unless opts[:calibrate]
  puts "judge control: #{control_results.length} sampled - #{leaks} leak#{leaks == 1 ? "" : "s"} - " \
       "#{fabricated_total} fabricated excerpt#{fabricated_total == 1 ? "" : "s"} - " \
       "#{empty_total} empty-excerpt downgrade#{empty_total == 1 ? "" : "s"}"
end
control_results.each do |result|
  next unless result["leak"] || result["error"] || result["skipped"]

  puts "  #{result["id"]} vs decoy #{result["decoy_id"]}: " \
       "#{result["error"] || result["skipped"] || "#{result["decoy_passes"]}/#{result["expected_assertions"]} expected assertions passed on the wrong transcript"}"
end

unless calibration_results.empty?
  agreed = calibration_results.map { |result| result["agreements"].to_i }.reduce(0, :+)
  total_labels = calibration_results.map { |result| result["assertions"].to_i }.reduce(0, :+)
  puts "calibration:   #{calibration_results.length} cases - #{agreed}/#{total_labels} verdicts agreed with the hand labels"
  calibration_results.each do |result|
    next if result["error"].nil? && result["rate"].to_f >= 1.0

    puts "  #{result["id"]}: #{result["error"] || "#{result["agreements"]}/#{result["assertions"]}"}"
  end
end

ambiguous = report_rows.flat_map { |entry| entry["assertions"].select { |a| a["ambiguous_assertion"] } }
puts "ambiguity:     #{ambiguous.length} assertion(s) returned unclear in more than a third of repeats (fixture bug, not a judge tuning problem)" unless ambiguous.empty?

unless harness_errors.empty?
  puts "harness:       #{harness_errors.length} error(s) - nothing was learned from those runs"
  harness_errors.first(10).each { |message| puts "  #{message}" }
  puts "  ... #{harness_errors.length - 10} more" if harness_errors.length > 10
end

provenance_plans.each do |plan|
  puts "provenance:    #{plan["skill"]} #{plan["status"]} - #{plan["note"]}"
end

puts format("$%.4f - %dm%02ds - artifact %s", total_cost, duration_s / 60, duration_s % 60, json_path.sub(ROOT + "/", ""))

# ---------------------------------------------------------------------------
# Machine artifact
# ---------------------------------------------------------------------------

artifact = {
  "schema" => ARTIFACT_SCHEMA,
  "started_at" => started_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
  "finished_at" => finished_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
  "harness" => { "script" => "scripts/eval.rb", "git_sha" => git_sha, "dirty" => git_dirty },
  "runner" => {
    "kind" => opts[:runner],
    "cli_version" => cli_version,
    "candidate_model" => opts[:model],
    "judge_model" => opts[:judge_model],
    "invoke" => opts[:invoke],
    "argv_template" => candidate_argv(opts),
    "ablation_argv_template" => opts[:ablation] ? ablation_argv(opts) : nil,
    "judge_argv_template" => judge_argv(opts, judge_system_path),
    "judge_system_prompt_sha256" => Digest::SHA256.hexdigest(JUDGE_SYSTEM_PROMPT)
  },
  "config" => {
    "repeat" => opts[:repeat], "ablation" => opts[:ablation], "control_sample" => opts[:control],
    "fail_under" => opts[:fail_under], "timeout_s" => opts[:timeout], "jobs" => opts[:jobs],
    "per_run_budget_usd" => opts[:per_run_budget], "max_cost_usd" => opts[:max_cost],
    "skills" => opts[:skills], "ids" => opts[:ids]
  },
  "fixtures_file" => { "path" => "tests/behavioral-contracts.yml", "sha256" => fixtures_sha },
  "provenance" => provenance_plans,
  "totals" => {
    "rows" => report_rows.length,
    "pass" => status_counts["PASS"], "flaky" => status_counts["FLAKY"], "fail" => status_counts["FAIL"],
    "error" => status_counts["ERROR"], "no_signal" => status_counts["NO SIGNAL"],
    "fabricated_excerpts" => fabricated_total, "empty_excerpt_downgrades" => empty_total,
    "judge_control_leak" => leaks,
    "cost_usd" => total_cost.round(4), "duration_s" => duration_s,
    "harness_errors" => harness_errors.length
  },
  "results" => report_rows,
  "ablation" => report_rows.map do |entry|
    next nil if entry["without_rate"].nil?

    {
      "id" => entry["label"], "with" => entry["with_rate"], "without" => entry["without_rate"],
      "delta" => (entry["with_rate"] - entry["without_rate"]).round(3),
      "no_signal" => entry["status_label"] == "NO SIGNAL"
    }
  end.compact,
  "judge_control" => control_results,
  "calibration" => calibration_results,
  "harness_error_messages" => harness_errors
}

File.write(json_path, JSON.pretty_generate(artifact) + "\n")
FileUtils.remove_entry(scratch_dir) if File.directory?(scratch_dir)

# ---------------------------------------------------------------------------
# Exit codes
# ---------------------------------------------------------------------------
#
# Separating 1 from 2 is the whole point. Exit 2 means "we learned nothing" -- an
# expired token, a timeout, a malformed judge reply. Exit 1 means "we learned
# something bad". Conflating them is how auth failures get read as regressions.

if budget_exhausted
  warn "scripts/eval.rb: --max-cost-usd ceiling of #{format("$%.2f", opts[:max_cost])} reached; results are partial."
  exit EXIT_HARNESS
end
exit EXIT_HARNESS unless harness_errors.empty?
exit EXIT_HARNESS if status_counts["ERROR"] > 0

regression = report_rows.any? do |entry|
  entry["status_label"] == "FAIL" ||
    entry["assertions"].any? { |assertion| assertion["rate"] < opts[:fail_under] }
end
exit EXIT_REGRESSION if regression

# Judge disagreement with a hand label is a judge-quality signal, not a Skill
# regression, so it lands on 4 alongside NO SIGNAL and control leaks. Gate CI-style
# checks on 1 and triage 4 on your own schedule.
calibration_disagreements = calibration_results.map do |result|
  result["assertions"].to_i - result["agreements"].to_i
end.reduce(0, :+)

exit EXIT_FIXTURE_QUALITY if status_counts["NO SIGNAL"] > 0 || leaks > 0 || calibration_disagreements > 0
exit EXIT_OK
