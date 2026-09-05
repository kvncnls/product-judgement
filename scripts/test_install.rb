#!/usr/bin/env ruby
# frozen_string_literal: true

# Regression coverage for scripts/install.sh. All installs use temporary project
# roots; the OpenCode user-path check is read-only, and the test suite never
# touches a real agent configuration directory.

require "fileutils"
require "open3"
require "shellwords"
require "tmpdir"

REPOSITORY_ROOT = File.expand_path("..", __dir__)
INSTALLER = File.join(REPOSITORY_ROOT, "scripts", "install.sh")
SKILLS = %w[focal compass flywheel soul product-judgement].freeze

class InstallerTest
  def assert(condition, message = "assertion failed")
    raise message unless condition
  end

  def assert_equal(expected, actual, message = nil)
    return if expected == actual

    detail = message || "expected #{expected.inspect}, got #{actual.inspect}"
    raise detail
  end

  def setup
    @temporary_root = Dir.mktmpdir("product-judgement-install-test")
    @source_root = File.join(@temporary_root, "source")
    @project_root = File.join(@temporary_root, "project")
    FileUtils.mkdir_p(@source_root)
    FileUtils.mkdir_p(@project_root)

    SKILLS.each do |skill|
      FileUtils.cp_r(File.join(REPOSITORY_ROOT, skill), @source_root)
    end
    FileUtils.mkdir_p(File.join(@source_root, "scripts"))
    @installer = File.join(@source_root, "scripts", "install.sh")
    FileUtils.cp(INSTALLER, @installer)
    FileUtils.chmod(0o755, @installer)
  end

  def teardown
    FileUtils.remove_entry_secure(@temporary_root) if @temporary_root && File.exist?(@temporary_root)
  end

  def invoke(arguments, environment = {})
    command_environment = { "PATH" => ENV["PATH"] }.merge(environment)
    Open3.capture3(command_environment, @installer, *arguments, chdir: @source_root)
  end

  def project_arguments
    ["--scope", "project", "--project", @project_root, "--agent", "claude"]
  end

  def target(skill)
    File.join(@project_root, ".claude", "skills", skill)
  end

  def assert_success(result, message = "installer should succeed")
    stdout, stderr, status = result
    assert(status.success?, "#{message}\nstdout: #{stdout}\nstderr: #{stderr}")
    result
  end

  def assert_failure(result, message = "installer should fail")
    stdout, stderr, status = result
    assert(!status.success?, "#{message}\nstdout: #{stdout}\nstderr: #{stderr}")
    result
  end

  def path_present(path)
    File.exist?(path) || File.symlink?(path)
  end

  def test_all_skills_link_install_reinstall_and_uninstall
    assert_success(invoke(project_arguments), "all five Skills should install as links")

    SKILLS.each do |skill|
      destination = target(skill)
      assert(File.symlink?(destination), "#{skill} should be a symlink")
      assert_equal(File.realpath(File.join(@source_root, skill)), File.realpath(destination))
    end

    reinstall = assert_success(invoke(project_arguments), "reinstalling canonical links should be safe")
    assert(reinstall[0].include?("unchanged"), "reinstall should report unchanged links")

    uninstall = assert_success(
      invoke(project_arguments + ["--uninstall"]),
      "uninstall should remove only canonical links"
    )
    SKILLS.each do |skill|
      assert(!path_present(target(skill)), "#{skill} link should be removed")
      assert(File.file?(File.join(@source_root, skill, "SKILL.md")), "#{skill} source should remain")
    end
    assert(uninstall[0].include?("removed"), "uninstall should report removed links")
  end

  def test_copy_install_tracks_content_updates_and_refuses_customization
    arguments = project_arguments + ["--copy"]
    assert_success(invoke(arguments), "copy installation should succeed")

    destination = target("focal")
    marker = File.join(destination, ".product-judgement-install")
    assert(File.directory?(destination), "copy should create a directory")
    assert(!File.symlink?(destination), "copy should not create a symlink")
    assert(File.file?(marker), "copy should carry provenance metadata")
    assert_equal(
      File.binread(File.join(@source_root, "focal", "SKILL.md")),
      File.binread(File.join(destination, "SKILL.md"))
    )

    assert_success(invoke(arguments), "an intact copy should reinstall idempotently")

    source_skill = File.join(@source_root, "focal", "SKILL.md")
    File.open(source_skill, "ab") { |file| file.write("\nfixture source update\n") }
    assert_success(invoke(arguments), "an unmodified copy should accept a source update")
    assert(File.binread(File.join(destination, "SKILL.md")).include?("fixture source update"))

    File.open(File.join(destination, "SKILL.md"), "ab") { |file| file.write("\ncustom destination edit\n") }
    failed = assert_failure(invoke(arguments), "a customized copy must be preserved")
    assert(failed[1].include?("modified"), "customization refusal should explain the reason")
    assert(File.binread(File.join(destination, "SKILL.md")).include?("custom destination edit"))

    uninstall_failed = assert_failure(
      invoke(project_arguments + ["--uninstall"]),
      "uninstall must refuse a customized copy"
    )
    assert(uninstall_failed[1].include?("modified"), "uninstall refusal should explain the reason")
    assert(File.directory?(destination), "customized copy should remain after refused uninstall")
  end

  def test_nested_reserved_name_is_part_of_copy_integrity
    arguments = project_arguments + ["--copy", "--skill", "focal"]
    assert_success(invoke(arguments))
    destination = target("focal")
    nested = File.join(destination, "reference", ".product-judgement-install")
    File.open(nested, "wb") { |file| file.write("custom nested content\n") }

    failed = assert_failure(invoke(arguments), "a nested marker edit must count as customization")
    assert(failed[1].include?("modified"), "nested marker customization should be identified")
    assert_equal("custom nested content\n", File.binread(nested))
  end

  def test_unowned_directories_files_and_links_are_preserved
    skills_root = File.join(@project_root, ".claude", "skills")
    FileUtils.mkdir_p(skills_root)
    custom_directory = target("focal")
    FileUtils.mkdir_p(custom_directory)
    custom_file = File.join(custom_directory, "keep-me.txt")
    File.open(custom_file, "wb") { |file| file.write("user content\n") }

    external = File.join(@temporary_root, "external-skill")
    FileUtils.mkdir_p(external)
    custom_link = target("flywheel")
    File.symlink(external, custom_link)
    unowned_file = target("compass")
    File.open(unowned_file, "wb") { |file| file.write("plain file\n") }

    failed = assert_failure(invoke(project_arguments), "unowned entries must block replacement")
    assert(failed[1].include?("refusing"), "refusal should be visible")
    assert_equal("user content\n", File.binread(custom_file))
    assert(File.symlink?(custom_link), "unowned symlink should remain")
    assert_equal(File.realpath(external), File.realpath(custom_link))
    assert_equal("plain file\n", File.binread(unowned_file))
    assert(!path_present(target("soul")), "preflight should avoid partial installation")
  end

  def test_invalid_skill_and_agent_values_are_rejected_before_mutation
    sentinel = File.join(@project_root, "sentinel.txt")
    File.open(sentinel, "wb") { |file| file.write("untouched\n") }

    invalid_skill = assert_failure(
      invoke(project_arguments + ["--skill", "../focal"]),
      "traversal Skill names must be rejected"
    )
    assert_equal(2, invalid_skill[2].exitstatus)
    assert(invalid_skill[1].include?("unknown Skill"), "Skill error should be explicit")
    invalid_agent = assert_failure(
      invoke(project_arguments + ["--agent", "../claude"]),
      "traversal agent names must be rejected"
    )
    assert_equal(2, invalid_agent[2].exitstatus)
    assert(invalid_agent[1].include?("unknown agent"), "agent error should be explicit")
    assert_equal("untouched\n", File.binread(sentinel))
    assert(!File.directory?(File.join(@project_root, ".claude")), "invalid arguments should not create targets")
  end

  def test_staging_copy_failure_leaves_existing_copy_untouched
    arguments = project_arguments + ["--copy", "--skill", "focal"]
    assert_success(invoke(arguments))
    destination = target("focal")
    original = File.binread(File.join(destination, "SKILL.md"))

    File.open(File.join(@source_root, "focal", "SKILL.md"), "ab") { |file| file.write("\nstaged source change\n") }
    fake_bin = File.join(@temporary_root, "fake-bin")
    FileUtils.mkdir_p(fake_bin)
    fake_cp = File.join(fake_bin, "cp")
    File.open(fake_cp, "wb") do |file|
      file.write("#!/bin/sh\nexit 77\n")
    end
    FileUtils.chmod(0o755, fake_cp)

    failed = assert_failure(
      invoke(arguments, "PATH" => "#{fake_bin}:#{ENV["PATH"]}"),
      "a staging copy failure should fail the run"
    )
    assert(failed[1].include?("stage"), "staging failure should be explained")
    assert_equal(original, File.binread(File.join(destination, "SKILL.md")))
    assert(File.file?(File.join(destination, ".product-judgement-install")))
  end

  def test_opencode_user_scope_uses_config_path
    actual_home = ENV.fetch("HOME")
    list = assert_success(
      invoke(
        ["--scope", "user", "--agent", "opencode", "--skill", "focal", "--list"],
      ),
      "OpenCode list should succeed"
    )
    expected_target = File.join(actual_home, ".config", "opencode", "skills")
    assert(list[0].include?(expected_target), "OpenCode should use ~/.config/opencode/skills")
    assert(!list[0].include?(File.join(actual_home, ".opencode", "skills")), "legacy path must not be listed")
  end

  def with_command_shim(name, body)
    real_command = ENV.fetch("PATH").split(File::PATH_SEPARATOR).map { |dir| File.join(dir, name) }.find { |path| File.executable?(path) && File.file?(path) }
    assert(real_command, "#{name} must be available")
    fake_bin = File.join(@temporary_root, "shim-bin")
    FileUtils.mkdir_p(fake_bin)
    shim = File.join(fake_bin, name)
    File.write(shim, "#!/bin/sh\nreal_command=#{Shellwords.escape(real_command)}\n" + body)
    FileUtils.chmod(0o755, shim)
    yield("PATH" => "#{fake_bin}:#{ENV.fetch("PATH")}")
  end

  def mv_argument_parser
    <<~SH
      case "$1" in
        -T|-h)
          if [ "$2" = "-n" ]; then
            move_source="$3"
            move_destination="$4"
          else
            move_source="$2"
            move_destination="$3"
          fi
          ;;
        -n)
          case "$2" in
            -T|-h) move_source="$3"; move_destination="$4" ;;
            *) move_source="$2"; move_destination="$3" ;;
          esac
          ;;
        *) move_source="$1"; move_destination="$2" ;;
      esac
    SH
  end

  def test_edit_during_staging_is_preserved
    arguments = project_arguments + ["--copy", "--skill", "focal"]
    assert_success(invoke(arguments))
    destination = target("focal")
    original = File.binread(File.join(destination, "SKILL.md"))
    File.open(File.join(@source_root, "focal", "SKILL.md"), "ab") { |file| file.write("\nupstream change\n") }
    body = <<~SH
      "$real_command" "$@" || exit $?
      printf '\\nconcurrent edit\\n' >> "$PJ_TEST_DEST/SKILL.md"
    SH
    with_command_shim("cp", body) do |environment|
      result = invoke(arguments, environment.merge("PJ_TEST_DEST" => destination))
      assert_failure(result, "concurrent customization must stop replacement")
      assert(result[1].include?("changed while"), "concurrent edit must be reported")
    end
    assert_equal(original + "\nconcurrent edit\n", File.binread(File.join(destination, "SKILL.md")))
  end

  def test_failed_final_move_restores_original
    arguments = project_arguments + ["--copy", "--skill", "focal"]
    assert_success(invoke(arguments))
    destination = target("focal")
    original = File.binread(File.join(destination, "SKILL.md"))
    File.open(File.join(@source_root, "focal", "SKILL.md"), "ab") { |file| file.write("\nupstream change\n") }
    body = <<~SH
      #{mv_argument_parser}
      case "$move_source" in */.product-judgement-stage.*/*) exit 78 ;; esac
      exec "$real_command" "$@"
    SH
    with_command_shim("mv", body) do |environment|
      result = invoke(arguments, environment)
      assert_failure(result, "failed final move must fail the update")
      assert(result[1].include?("destination restored"), "rollback must be reported")
    end
    assert_equal(original, File.binread(File.join(destination, "SKILL.md")))
  end

  def test_competing_destination_directory_is_rejected_before_backup_discard
    arguments = project_arguments + ["--copy", "--skill", "focal"]
    assert_success(invoke(arguments))
    destination = target("focal")
    original = File.binread(File.join(destination, "SKILL.md"))
    File.open(File.join(@source_root, "focal", "SKILL.md"), "ab") { |file| file.write("\nupstream change\n") }
    body = <<~SH
      #{mv_argument_parser}
      case "$move_source" in
        */.product-judgement-stage.*/*)
          mkdir -p "$move_destination"
          printf 'concurrent directory content\n' > "$move_destination/keep-me.txt"
          ;;
      esac
      exec "$real_command" "$@"
    SH
    with_command_shim("mv", body) do |environment|
      result = invoke(arguments, environment)
      assert_failure(result, "a competing destination directory must stop replacement")
      assert(result[1].include?("did not land"), "directory race should be reported")
    end

    assert_equal(
      "concurrent directory content\n",
      File.binread(File.join(destination, "keep-me.txt"))
    )
    assert(!path_present(File.join(destination, "focal")), "staged entry must not remain nested")
    backup_entries = Dir.glob(File.join(File.dirname(destination), ".product-judgement-backup.*", "entry", "SKILL.md"))
    assert_equal(1, backup_entries.length, "original should remain in a rollback directory")
    assert_equal(original, File.binread(backup_entries.first))
  end

  def test_competing_destination_symlink_is_not_followed
    arguments = project_arguments + ["--copy", "--skill", "focal"]
    assert_success(invoke(arguments))
    destination = target("focal")
    original = File.binread(File.join(destination, "SKILL.md"))
    external = File.join(@temporary_root, "external-destination")
    FileUtils.mkdir_p(external)
    File.open(File.join(@source_root, "focal", "SKILL.md"), "ab") { |file| file.write("\nupstream change\n") }
    body = <<~SH
      #{mv_argument_parser}
      case "$move_source" in
        */.product-judgement-stage.*/*) ln -s "$PJ_TEST_EXTERNAL" "$move_destination" ;;
      esac
      exec "$real_command" "$@"
    SH
    with_command_shim("mv", body) do |environment|
      result = invoke(arguments, environment.merge("PJ_TEST_EXTERNAL" => external))
      assert_failure(result, "a competing destination symlink must stop replacement")
    end

    assert(File.symlink?(destination), "competing symlink should remain")
    assert_equal(File.realpath(external), File.realpath(destination))
    assert_equal([], Dir.children(external), "staged Skill must not be moved into the external directory")
    backup_entries = Dir.glob(File.join(File.dirname(destination), ".product-judgement-backup.*", "entry", "SKILL.md"))
    assert_equal(1, backup_entries.length, "original should remain in a rollback directory")
    assert_equal(original, File.binread(backup_entries.first))
  end

  def test_edit_after_backup_move_is_preserved
    arguments = project_arguments + ["--copy", "--skill", "focal"]
    assert_success(invoke(arguments))
    destination = target("focal")
    original = File.binread(File.join(destination, "SKILL.md"))
    File.open(File.join(@source_root, "focal", "SKILL.md"), "ab") { |file| file.write("\nupstream change\n") }
    body = <<~SH
      "$real_command" "$@" || exit $?
      #{mv_argument_parser}
      case "$move_source:$move_destination" in
        */.product-judgement-stage.*/*:*) ;;
        *:*/.product-judgement-backup.*/entry) printf '\\nconcurrent backup edit\\n' >> "$move_destination/SKILL.md" ;;
      esac
    SH
    with_command_shim("mv", body) do |environment|
      result = invoke(arguments, environment)
      assert_failure(result, "an edit after backup must stop replacement")
      assert(result[1].include?("changed while it was being moved"), "backup edit should be reported")
    end
    assert_equal(
      original + "\nconcurrent backup edit\n",
      File.binread(File.join(destination, "SKILL.md"))
    )
  end

  def test_uninstall_edit_after_backup_move_is_preserved
    arguments = project_arguments + ["--copy", "--skill", "focal"]
    assert_success(invoke(arguments))
    destination = target("focal")
    original = File.binread(File.join(destination, "SKILL.md"))
    body = <<~SH
      "$real_command" "$@" || exit $?
      #{mv_argument_parser}
      case "$move_source:$move_destination" in
        *:*/.product-judgement-backup.*/entry) printf '\\nconcurrent uninstall edit\\n' >> "$move_destination/SKILL.md" ;;
      esac
    SH
    with_command_shim("mv", body) do |environment|
      result = invoke(project_arguments + ["--uninstall"], environment)
      assert_failure(result, "an edit after backup must stop uninstall")
      assert(result[1].include?("changed while being moved for uninstall"), "backup edit should be reported")
    end
    assert_equal(
      original + "\nconcurrent uninstall edit\n",
      File.binread(File.join(destination, "SKILL.md"))
    )
  end

  def test_interrupt_after_backup_preserves_original
    arguments = project_arguments + ["--copy", "--skill", "focal"]
    assert_success(invoke(arguments))
    destination = target("focal")
    original = File.binread(File.join(destination, "SKILL.md"))
    File.open(File.join(@source_root, "focal", "SKILL.md"), "ab") { |file| file.write("\nupstream change\n") }
    body = <<~SH
      "$real_command" "$@" || exit $?
      #{mv_argument_parser}
      case "$move_destination" in */.product-judgement-backup.*/entry) kill -TERM "$PPID" ;; esac
    SH
    with_command_shim("mv", body) do |environment|
      assert_failure(invoke(arguments, environment), "interrupted update must exit")
    end
    assert_equal(original, File.binread(File.join(destination, "SKILL.md")))
    assert(File.file?(File.join(destination, ".product-judgement-install")))
  end

  def test_source_alias_is_refused_without_touching_source
    skills_parent = File.join(@project_root, ".claude")
    FileUtils.mkdir_p(skills_parent)
    File.symlink(File.join(@source_root, "focal"), File.join(skills_parent, "skills"))

    failed = assert_failure(invoke(project_arguments), "a target resolving into source must be refused")
    assert(failed[1].include?("source Skill"), "source alias refusal should be explicit")
    assert(File.file?(File.join(@source_root, "focal", "SKILL.md")), "source must survive refusal")
    assert(!File.exist?(File.join(@source_root, "focal", ".product-judgement-install")))
  end

  def test_selected_source_skill_alias_is_refused_before_target_creation
    focal = File.join(@source_root, "focal")
    compass = File.join(@source_root, "compass")
    FileUtils.rm_rf(focal)
    File.symlink(compass, focal)

    failed = assert_failure(
      invoke(project_arguments + ["--skill", "focal"]),
      "a selected source alias must be refused"
    )
    assert(failed[1].include?("canonical directory"), "source alias refusal should be explicit")
    assert(!File.exist?(File.join(@project_root, ".claude")), "source validation must precede target creation")
  end

  def test_target_inside_unselected_source_is_refused
    unsafe_project = File.join(@source_root, "compass")
    arguments = [
      "--scope", "project", "--project", unsafe_project,
      "--agent", "claude", "--skill", "focal"
    ]

    failed = assert_failure(invoke(arguments), "an unselected source alias must still be refused")
    assert(failed[1].include?("source Skill"), "unselected source refusal should be explicit")
    assert(File.file?(File.join(unsafe_project, "SKILL.md")), "unselected source must remain intact")
    assert(!File.exist?(File.join(unsafe_project, ".claude")), "refusal must not create a target inside source")
  end

  def test_unsafe_nested_source_symlink_is_refused_before_target_creation
    external = File.join(@temporary_root, "external-source")
    FileUtils.mkdir_p(external)
    outside = File.join(external, "outside.md")
    File.write(outside, "outside source\n")
    link = File.join(@source_root, "focal", "reference", "outside.md")
    File.symlink(outside, link)

    failed = assert_failure(
      invoke(project_arguments + ["--copy", "--skill", "focal"]),
      "a nested source symlink escaping the Skill must be refused"
    )
    assert(failed[1].include?("unsafe symlink"), "source symlink refusal should be explicit")
    assert(!File.exist?(File.join(@project_root, ".claude")), "source validation must precede target creation")
  end

  def test_unsafe_skill_md_symlink_is_refused_before_target_creation
    external = File.join(@temporary_root, "external-source")
    FileUtils.mkdir_p(external)
    outside = File.join(external, "outside.md")
    File.write(outside, "outside source\n")
    skill_md = File.join(@source_root, "focal", "SKILL.md")
    FileUtils.rm_f(skill_md)
    File.symlink(outside, skill_md)

    failed = assert_failure(
      invoke(project_arguments + ["--copy", "--skill", "focal"]),
      "SKILL.md symlinks escaping the Skill must be refused"
    )
    assert(failed[1].include?("unsafe symlink"), "SKILL.md symlink refusal should be explicit")
    assert(!File.exist?(File.join(@project_root, ".claude")), "source validation must precede target creation")
  end

  def test_absolute_internal_source_symlink_is_refused_during_copy_staging
    focal = File.join(@source_root, "focal")
    internal_target = File.join(focal, "reference")
    internal_link = File.join(internal_target, "source-reference")
    File.symlink(internal_target, internal_link)

    failed = assert_failure(
      invoke(project_arguments + ["--copy", "--skill", "focal"]),
      "an absolute source symlink must not escape the staged copy"
    )
    assert(failed[1].include?("staged copy") && failed[1].include?("unsafe symlink"), "staged source symlink refusal should be explicit")
    assert(!path_present(target("focal")), "unsafe staged source must not create a destination")
  end
end

if $PROGRAM_NAME == __FILE__
  test_names = InstallerTest.instance_methods(false).map(&:to_s).grep(/\Atest_/).sort
  failures = []
  test_names.each do |name|
    test = InstallerTest.new
    begin
      test.setup
      test.public_send(name)
      print "."
    rescue StandardError => error
      failures << [name, error]
      print "F"
    ensure
      begin
        test.teardown
      rescue StandardError => error
        failures << [name, error]
      end
    end
  end
  puts
  puts "#{test_names.length} tests, #{test_names.length - failures.length} passed, #{failures.length} failures"
  failures.each do |name, error|
    warn "\nFAIL: #{name}: #{error.message}"
    warn error.backtrace.first(5).join("\n") if error.backtrace
  end
  exit(failures.empty? ? 0 : 1)
end
