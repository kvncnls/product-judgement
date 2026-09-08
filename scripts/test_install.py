#!/usr/bin/env python3
"""Regression coverage for :mod:`scripts/install.sh`.

Every installation uses temporary project roots.  The OpenCode user-scope
check only lists a path, so this suite never touches an agent configuration
directory owned by the user.
"""

from __future__ import annotations

import contextlib
import os
import shlex
import shutil
import subprocess
import tempfile
import textwrap
from pathlib import Path
from typing import Iterator


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
INSTALLER = REPOSITORY_ROOT / "scripts" / "install.sh"
SKILLS = ["focal", "compass", "flywheel", "soul", "product-judgement"]


class InstallerTest:
    """One fresh temporary source/project pair per regression method."""

    def assert_(self, condition: bool, message: str = "assertion failed") -> None:
        if not condition:
            raise AssertionError(message)

    def assert_equal(self, expected, actual, message: str | None = None) -> None:
        if expected == actual:
            return
        detail = message or f"expected {expected!r}, got {actual!r}"
        raise AssertionError(detail)

    def setup(self) -> None:
        self._temporary = tempfile.TemporaryDirectory(prefix="product-judgement-install-test-")
        self.temporary_root = Path(self._temporary.name)
        self.source_root = self.temporary_root / "source"
        self.project_root = self.temporary_root / "project"
        self.source_root.mkdir()
        self.project_root.mkdir()

        for skill in SKILLS:
            shutil.copytree(REPOSITORY_ROOT / skill, self.source_root / skill, symlinks=True)
        (self.source_root / "scripts").mkdir()
        self.installer = self.source_root / "scripts" / "install.sh"
        shutil.copy2(INSTALLER, self.installer)
        self.installer.chmod(0o755)

    def teardown(self) -> None:
        temporary = getattr(self, "_temporary", None)
        if temporary is not None:
            temporary.cleanup()

    def invoke(self, arguments: list[str], environment: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
        command_environment = os.environ.copy()
        command_environment["PATH"] = os.environ["PATH"]
        if environment:
            command_environment.update(environment)
        return subprocess.run(
            [str(self.installer), *arguments],
            cwd=self.source_root,
            env=command_environment,
            capture_output=True,
            text=True,
        )

    def project_arguments(self) -> list[str]:
        return ["--scope", "project", "--project", str(self.project_root), "--agent", "claude"]

    def target(self, skill: str) -> Path:
        return self.project_root / ".claude" / "skills" / skill

    def assert_success(self, result: subprocess.CompletedProcess[str], message: str = "installer should succeed"):
        self.assert_(result.returncode == 0, f"{message}\nstdout: {result.stdout}\nstderr: {result.stderr}")
        return result

    def assert_failure(self, result: subprocess.CompletedProcess[str], message: str = "installer should fail"):
        self.assert_(result.returncode != 0, f"{message}\nstdout: {result.stdout}\nstderr: {result.stderr}")
        return result

    @staticmethod
    def path_present(path: Path) -> bool:
        return path.exists() or path.is_symlink()

    def test_all_skills_link_install_reinstall_and_uninstall(self) -> None:
        self.assert_success(self.invoke(self.project_arguments()), "all five Skills should install as links")

        for skill in SKILLS:
            destination = self.target(skill)
            self.assert_(destination.is_symlink(), f"{skill} should be a symlink")
            self.assert_equal(os.path.realpath(self.source_root / skill), os.path.realpath(destination))

        reinstall = self.assert_success(
            self.invoke(self.project_arguments()),
            "reinstalling canonical links should be safe",
        )
        self.assert_("unchanged" in reinstall.stdout, "reinstall should report unchanged links")

        uninstall = self.assert_success(
            self.invoke(self.project_arguments() + ["--uninstall"]),
            "uninstall should remove only canonical links",
        )
        for skill in SKILLS:
            self.assert_(not self.path_present(self.target(skill)), f"{skill} link should be removed")
            self.assert_((self.source_root / skill / "SKILL.md").is_file(), f"{skill} source should remain")
        self.assert_("removed" in uninstall.stdout, "uninstall should report removed links")

    def test_copy_install_tracks_content_updates_and_refuses_customization(self) -> None:
        arguments = self.project_arguments() + ["--copy"]
        self.assert_success(self.invoke(arguments), "copy installation should succeed")

        destination = self.target("focal")
        marker = destination / ".product-judgement-install"
        self.assert_(destination.is_dir(), "copy should create a directory")
        self.assert_(not destination.is_symlink(), "copy should not create a symlink")
        self.assert_(marker.is_file(), "copy should carry provenance metadata")
        self.assert_equal((self.source_root / "focal" / "SKILL.md").read_bytes(), (destination / "SKILL.md").read_bytes())

        self.assert_success(self.invoke(arguments), "an intact copy should reinstall idempotently")

        source_skill = self.source_root / "focal" / "SKILL.md"
        with source_skill.open("ab") as file:
            file.write(b"\nfixture source update\n")
        self.assert_success(self.invoke(arguments), "an unmodified copy should accept a source update")
        self.assert_(b"fixture source update" in (destination / "SKILL.md").read_bytes())

        with (destination / "SKILL.md").open("ab") as file:
            file.write(b"\ncustom destination edit\n")
        failed = self.assert_failure(self.invoke(arguments), "a customized copy must be preserved")
        self.assert_("modified" in failed.stderr, "customization refusal should explain the reason")
        self.assert_(b"custom destination edit" in (destination / "SKILL.md").read_bytes())

        uninstall_failed = self.assert_failure(
            self.invoke(self.project_arguments() + ["--uninstall"]),
            "uninstall must refuse a customized copy",
        )
        self.assert_("modified" in uninstall_failed.stderr, "uninstall refusal should explain the reason")
        self.assert_(destination.is_dir(), "customized copy should remain after refused uninstall")

    def test_nested_reserved_name_is_part_of_copy_integrity(self) -> None:
        arguments = self.project_arguments() + ["--copy", "--skill", "focal"]
        self.assert_success(self.invoke(arguments))
        destination = self.target("focal")
        nested = destination / "reference" / ".product-judgement-install"
        nested.write_text("custom nested content\n", encoding="utf-8")

        failed = self.assert_failure(self.invoke(arguments), "a nested marker edit must count as customization")
        self.assert_("modified" in failed.stderr, "nested marker customization should be identified")
        self.assert_equal("custom nested content\n", nested.read_text(encoding="utf-8"))

    def test_unowned_directories_files_and_links_are_preserved(self) -> None:
        skills_root = self.project_root / ".claude" / "skills"
        skills_root.mkdir(parents=True)
        custom_directory = self.target("focal")
        custom_directory.mkdir()
        custom_file = custom_directory / "keep-me.txt"
        custom_file.write_text("user content\n", encoding="utf-8")

        external = self.temporary_root / "external-skill"
        external.mkdir()
        custom_link = self.target("flywheel")
        custom_link.symlink_to(external)
        unowned_file = self.target("compass")
        unowned_file.write_text("plain file\n", encoding="utf-8")

        failed = self.assert_failure(self.invoke(self.project_arguments()), "unowned entries must block replacement")
        self.assert_("refusing" in failed.stderr, "refusal should be visible")
        self.assert_equal("user content\n", custom_file.read_text(encoding="utf-8"))
        self.assert_(custom_link.is_symlink(), "unowned symlink should remain")
        self.assert_equal(os.path.realpath(external), os.path.realpath(custom_link))
        self.assert_equal("plain file\n", unowned_file.read_text(encoding="utf-8"))
        self.assert_(not self.path_present(self.target("soul")), "preflight should avoid partial installation")

    def test_invalid_skill_and_agent_values_are_rejected_before_mutation(self) -> None:
        sentinel = self.project_root / "sentinel.txt"
        sentinel.write_text("untouched\n", encoding="utf-8")

        invalid_skill = self.assert_failure(
            self.invoke(self.project_arguments() + ["--skill", "../focal"]),
            "traversal Skill names must be rejected",
        )
        self.assert_equal(2, invalid_skill.returncode)
        self.assert_("unknown Skill" in invalid_skill.stderr, "Skill error should be explicit")
        invalid_agent = self.assert_failure(
            self.invoke(self.project_arguments() + ["--agent", "../claude"]),
            "traversal agent names must be rejected",
        )
        self.assert_equal(2, invalid_agent.returncode)
        self.assert_("unknown agent" in invalid_agent.stderr, "agent error should be explicit")
        self.assert_equal("untouched\n", sentinel.read_text(encoding="utf-8"))
        self.assert_(not (self.project_root / ".claude").is_dir(), "invalid arguments should not create targets")

    def test_staging_copy_failure_leaves_existing_copy_untouched(self) -> None:
        arguments = self.project_arguments() + ["--copy", "--skill", "focal"]
        self.assert_success(self.invoke(arguments))
        destination = self.target("focal")
        original = (destination / "SKILL.md").read_bytes()

        with (self.source_root / "focal" / "SKILL.md").open("ab") as file:
            file.write(b"\nstaged source change\n")
        fake_bin = self.temporary_root / "fake-bin"
        fake_bin.mkdir()
        fake_cp = fake_bin / "cp"
        fake_cp.write_text("#!/bin/sh\nexit 77\n", encoding="utf-8")
        fake_cp.chmod(0o755)

        failed = self.assert_failure(
            self.invoke(arguments, {"PATH": f"{fake_bin}:{os.environ['PATH']}"}),
            "a staging copy failure should fail the run",
        )
        self.assert_("stage" in failed.stderr, "staging failure should be explained")
        self.assert_equal(original, (destination / "SKILL.md").read_bytes())
        self.assert_((destination / ".product-judgement-install").is_file())

    def test_opencode_user_scope_uses_config_path(self) -> None:
        actual_home = os.environ["HOME"]
        listing = self.assert_success(
            self.invoke(["--scope", "user", "--agent", "opencode", "--skill", "focal", "--list"]),
            "OpenCode list should succeed",
        )
        expected_target = os.path.join(actual_home, ".config", "opencode", "skills")
        self.assert_(expected_target in listing.stdout, "OpenCode should use ~/.config/opencode/skills")
        self.assert_(os.path.join(actual_home, ".opencode", "skills") not in listing.stdout, "legacy path must not be listed")

    @contextlib.contextmanager
    def with_command_shim(self, name: str, body: str) -> Iterator[dict[str, str]]:
        real_command = shutil.which(name, path=os.environ["PATH"])
        self.assert_(real_command is not None, f"{name} must be available")
        fake_bin = self.temporary_root / "shim-bin"
        fake_bin.mkdir(exist_ok=True)
        shim = fake_bin / name
        shim.write_text(
            "#!/bin/sh\nreal_command=" + shlex.quote(real_command) + "\n" + body,
            encoding="utf-8",
        )
        shim.chmod(0o755)
        yield {"PATH": f"{fake_bin}:{os.environ['PATH']}"}

    @staticmethod
    def mv_argument_parser() -> str:
        return textwrap.dedent(
            r'''\
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
            '''
        )

    def test_edit_during_staging_is_preserved(self) -> None:
        arguments = self.project_arguments() + ["--copy", "--skill", "focal"]
        self.assert_success(self.invoke(arguments))
        destination = self.target("focal")
        original = (destination / "SKILL.md").read_bytes()
        with (self.source_root / "focal" / "SKILL.md").open("ab") as file:
            file.write(b"\nupstream change\n")
        body = textwrap.dedent(
            r'''\
            "$real_command" "$@" || exit $?
            printf '\nconcurrent edit\n' >> "$PJ_TEST_DEST/SKILL.md"
            '''
        )
        with self.with_command_shim("cp", body) as environment:
            result = self.invoke(arguments, {**environment, "PJ_TEST_DEST": str(destination)})
            self.assert_failure(result, "concurrent customization must stop replacement")
            self.assert_("changed while" in result.stderr, "concurrent edit must be reported")
        self.assert_equal(original + b"\nconcurrent edit\n", (destination / "SKILL.md").read_bytes())

    def test_failed_final_move_restores_original(self) -> None:
        arguments = self.project_arguments() + ["--copy", "--skill", "focal"]
        self.assert_success(self.invoke(arguments))
        destination = self.target("focal")
        original = (destination / "SKILL.md").read_bytes()
        with (self.source_root / "focal" / "SKILL.md").open("ab") as file:
            file.write(b"\nupstream change\n")
        body = textwrap.dedent(
            """\
            {parser}
            case "$move_source" in */.product-judgement-stage.*/*) exit 78 ;; esac
            exec "$real_command" "$@"
            """
        ).format(parser=self.mv_argument_parser())
        with self.with_command_shim("mv", body) as environment:
            result = self.invoke(arguments, environment)
            self.assert_failure(result, "failed final move must fail the update")
            self.assert_("destination restored" in result.stderr, "rollback must be reported")
        self.assert_equal(original, (destination / "SKILL.md").read_bytes())

    def test_competing_destination_directory_is_rejected_before_backup_discard(self) -> None:
        self.assert_competing_directory_preserved()

    def test_competing_destination_directory_skipped_move_keeps_backup(self) -> None:
        self.assert_competing_directory_preserved(move_exit=0)

    def test_competing_destination_directory_rejected_move_keeps_backup(self) -> None:
        self.assert_competing_directory_preserved(move_exit=1)

    def assert_competing_directory_preserved(self, move_exit: int | None = None) -> None:
        arguments = self.project_arguments() + ["--copy", "--skill", "focal"]
        self.assert_success(self.invoke(arguments))
        destination = self.target("focal")
        original = (destination / "SKILL.md").read_bytes()
        with (self.source_root / "focal" / "SKILL.md").open("ab") as file:
            file.write(b"\nupstream change\n")
        body = textwrap.dedent(
            """\
            {parser}
            case "$move_source" in
              */.product-judgement-stage.*/*)
                mkdir -p "$move_destination"
                printf 'concurrent directory content\n' > "$move_destination/keep-me.txt"
                {move_outcome}
                ;;
            esac
            exec "$real_command" "$@"
            """
        ).format(
            parser=self.mv_argument_parser(),
            move_outcome="" if move_exit is None else f"exit {move_exit}",
        )
        with self.with_command_shim("mv", body) as environment:
            result = self.invoke(arguments, environment)
            self.assert_failure(result, "a competing destination directory must stop replacement")

        self.assert_equal("concurrent directory content\n", (destination / "keep-me.txt").read_text(encoding="utf-8"))
        self.assert_(not self.path_present(destination / "focal"), "staged entry must not remain nested")
        backup_entries = list((destination.parent).glob(".product-judgement-backup.*/entry/SKILL.md"))
        self.assert_equal(1, len(backup_entries), "original should remain in a rollback directory")
        self.assert_equal(original, backup_entries[0].read_bytes())

        # No-clobber mv implementations can skip with status 0 or reject with
        # a nonzero status. Both must fail the installation and retain the
        # original. A status-0 skip must also be caught by the identity check.
        self.assert_(
            "cannot install staged Skill at" in result.stderr and "original retained" in result.stderr,
            f"directory race and retained backup should be reported\nstderr: {result.stderr}",
        )
        if move_exit == 0:
            self.assert_("did not land" in result.stderr, "a skipped move must fail the destination identity check")

    def test_competing_destination_symlink_is_not_followed(self) -> None:
        arguments = self.project_arguments() + ["--copy", "--skill", "focal"]
        self.assert_success(self.invoke(arguments))
        destination = self.target("focal")
        original = (destination / "SKILL.md").read_bytes()
        external = self.temporary_root / "external-destination"
        external.mkdir()
        with (self.source_root / "focal" / "SKILL.md").open("ab") as file:
            file.write(b"\nupstream change\n")
        body = textwrap.dedent(
            """\
            {parser}
            case "$move_source" in
              */.product-judgement-stage.*/*) ln -s "$PJ_TEST_EXTERNAL" "$move_destination" ;;
            esac
            exec "$real_command" "$@"
            """
        ).format(parser=self.mv_argument_parser())
        with self.with_command_shim("mv", body) as environment:
            result = self.invoke(arguments, {**environment, "PJ_TEST_EXTERNAL": str(external)})
            self.assert_failure(result, "a competing destination symlink must stop replacement")

        self.assert_(destination.is_symlink(), "competing symlink should remain")
        self.assert_equal(os.path.realpath(external), os.path.realpath(destination))
        self.assert_equal([], list(external.iterdir()), "staged Skill must not be moved into the external directory")
        backup_entries = list(destination.parent.glob(".product-judgement-backup.*/entry/SKILL.md"))
        self.assert_equal(1, len(backup_entries), "original should remain in a rollback directory")
        self.assert_equal(original, backup_entries[0].read_bytes())

    def test_edit_after_backup_move_is_preserved(self) -> None:
        arguments = self.project_arguments() + ["--copy", "--skill", "focal"]
        self.assert_success(self.invoke(arguments))
        destination = self.target("focal")
        original = (destination / "SKILL.md").read_bytes()
        with (self.source_root / "focal" / "SKILL.md").open("ab") as file:
            file.write(b"\nupstream change\n")
        body = textwrap.dedent(
            """\
            "$real_command" "$@" || exit $?
            {parser}
            case "$move_source:$move_destination" in
              */.product-judgement-stage.*/*:*) ;;
              *:*/.product-judgement-backup.*/entry) printf '\nconcurrent backup edit\n' >> "$move_destination/SKILL.md" ;;
            esac
            """
        ).format(parser=self.mv_argument_parser())
        with self.with_command_shim("mv", body) as environment:
            result = self.invoke(arguments, environment)
            self.assert_failure(result, "an edit after backup must stop replacement")
            self.assert_("changed while it was being moved" in result.stderr, "backup edit should be reported")
        self.assert_equal(original + b"\nconcurrent backup edit\n", (destination / "SKILL.md").read_bytes())

    def test_uninstall_edit_after_backup_move_is_preserved(self) -> None:
        arguments = self.project_arguments() + ["--copy", "--skill", "focal"]
        self.assert_success(self.invoke(arguments))
        destination = self.target("focal")
        original = (destination / "SKILL.md").read_bytes()
        body = textwrap.dedent(
            """\
            "$real_command" "$@" || exit $?
            {parser}
            case "$move_source:$move_destination" in
              *:*/.product-judgement-backup.*/entry) printf '\nconcurrent uninstall edit\n' >> "$move_destination/SKILL.md" ;;
            esac
            """
        ).format(parser=self.mv_argument_parser())
        with self.with_command_shim("mv", body) as environment:
            result = self.invoke(self.project_arguments() + ["--uninstall"], environment)
            self.assert_failure(result, "an edit after backup must stop uninstall")
            self.assert_("changed while being moved for uninstall" in result.stderr, "backup edit should be reported")
        self.assert_equal(original + b"\nconcurrent uninstall edit\n", (destination / "SKILL.md").read_bytes())

    def test_interrupt_after_backup_preserves_original(self) -> None:
        arguments = self.project_arguments() + ["--copy", "--skill", "focal"]
        self.assert_success(self.invoke(arguments))
        destination = self.target("focal")
        original = (destination / "SKILL.md").read_bytes()
        with (self.source_root / "focal" / "SKILL.md").open("ab") as file:
            file.write(b"\nupstream change\n")
        body = textwrap.dedent(
            """\
            "$real_command" "$@" || exit $?
            {parser}
            case "$move_destination" in */.product-judgement-backup.*/entry) kill -TERM "$PPID" ;; esac
            """
        ).format(parser=self.mv_argument_parser())
        with self.with_command_shim("mv", body) as environment:
            self.assert_failure(self.invoke(arguments, environment), "interrupted update must exit")
        self.assert_equal(original, (destination / "SKILL.md").read_bytes())
        self.assert_((destination / ".product-judgement-install").is_file())

    def test_source_alias_is_refused_without_touching_source(self) -> None:
        skills_parent = self.project_root / ".claude"
        skills_parent.mkdir(parents=True)
        (skills_parent / "skills").symlink_to(self.source_root / "focal")

        failed = self.assert_failure(self.invoke(self.project_arguments()), "a target resolving into source must be refused")
        self.assert_("source Skill" in failed.stderr, "source alias refusal should be explicit")
        self.assert_((self.source_root / "focal" / "SKILL.md").is_file(), "source must survive refusal")
        self.assert_(not (self.source_root / "focal" / ".product-judgement-install").exists())

    def test_selected_source_skill_alias_is_refused_before_target_creation(self) -> None:
        focal = self.source_root / "focal"
        compass = self.source_root / "compass"
        shutil.rmtree(focal)
        focal.symlink_to(compass)

        failed = self.assert_failure(
            self.invoke(self.project_arguments() + ["--skill", "focal"]),
            "a selected source alias must be refused",
        )
        self.assert_("canonical directory" in failed.stderr, "source alias refusal should be explicit")
        self.assert_(not (self.project_root / ".claude").exists(), "source validation must precede target creation")

    def test_target_inside_unselected_source_is_refused(self) -> None:
        unsafe_project = self.source_root / "compass"
        arguments = [
            "--scope", "project", "--project", str(unsafe_project),
            "--agent", "claude", "--skill", "focal",
        ]

        failed = self.assert_failure(self.invoke(arguments), "an unselected source alias must still be refused")
        self.assert_("source Skill" in failed.stderr, "unselected source refusal should be explicit")
        self.assert_((unsafe_project / "SKILL.md").is_file(), "unselected source must remain intact")
        self.assert_(not (unsafe_project / ".claude").exists(), "refusal must not create a target inside source")

    def test_unsafe_nested_source_symlink_is_refused_before_target_creation(self) -> None:
        external = self.temporary_root / "external-source"
        external.mkdir()
        outside = external / "outside.md"
        outside.write_text("outside source\n", encoding="utf-8")
        link = self.source_root / "focal" / "reference" / "outside.md"
        link.symlink_to(outside)

        failed = self.assert_failure(
            self.invoke(self.project_arguments() + ["--copy", "--skill", "focal"]),
            "a nested source symlink escaping the Skill must be refused",
        )
        self.assert_("unsafe symlink" in failed.stderr, "source symlink refusal should be explicit")
        self.assert_(not (self.project_root / ".claude").exists(), "source validation must precede target creation")

    def test_unsafe_skill_md_symlink_is_refused_before_target_creation(self) -> None:
        external = self.temporary_root / "external-source"
        external.mkdir()
        outside = external / "outside.md"
        outside.write_text("outside source\n", encoding="utf-8")
        skill_md = self.source_root / "focal" / "SKILL.md"
        skill_md.unlink()
        skill_md.symlink_to(outside)

        failed = self.assert_failure(
            self.invoke(self.project_arguments() + ["--copy", "--skill", "focal"]),
            "SKILL.md symlinks escaping the Skill must be refused",
        )
        self.assert_("unsafe symlink" in failed.stderr, "source symlink refusal should be explicit")
        self.assert_(not (self.project_root / ".claude").exists(), "source validation must precede target creation")

    def test_absolute_internal_source_symlink_is_refused_during_copy_staging(self) -> None:
        focal = self.source_root / "focal"
        internal_target = focal / "reference"
        internal_link = internal_target / "source-reference"
        internal_link.symlink_to(internal_target)

        failed = self.assert_failure(
            self.invoke(self.project_arguments() + ["--copy", "--skill", "focal"]),
            "an absolute source symlink must not escape the staged copy",
        )
        self.assert_(
            "staged copy" in failed.stderr and "unsafe symlink" in failed.stderr,
            "staged source symlink refusal should be explicit",
        )
        self.assert_(not self.path_present(self.target("focal")), "unsafe staged source must not create a destination")


def main() -> int:
    test_names = sorted(name for name in dir(InstallerTest) if name.startswith("test_"))
    failures: list[tuple[str, Exception]] = []
    for name in test_names:
        test = InstallerTest()
        try:
            test.setup()
            getattr(test, name)()
            print(".", end="", flush=True)
        except Exception as error:  # Keep cleanup and all test failures visible.
            failures.append((name, error))
            print("F", end="", flush=True)
        finally:
            try:
                test.teardown()
            except Exception as error:
                failures.append((name, error))
    print()
    print(f"{len(test_names)} tests, {len(test_names) - len(failures)} passed, {len(failures)} failures")
    for name, error in failures:
        print(f"\nFAIL: {name}: {error}", file=os.sys.stderr)
        traceback = getattr(error, "__traceback__", None)
        if traceback is not None:
            import traceback as traceback_module

            lines = traceback_module.format_tb(traceback)
            print("".join(lines[-5:]).rstrip(), file=os.sys.stderr)
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
