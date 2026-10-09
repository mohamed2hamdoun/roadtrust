import subprocess
from pathlib import Path

from check_commit_refs import commits_without_record, has_record


def test_message_reference_detection() -> None:
    assert has_record("docs: ADR08 build in a separate repository")
    assert has_record("fix: wrap heading at +-pi\n\nImplements CR-001.")
    assert not has_record("fix typo")
    assert not has_record("bump the ADR template")  # 'ADR' without a number
    assert not has_record("CR-1 is too short")
    assert not has_record("fix typo\n# Please enter the commit message (ADR08)")


def test_range_reports_only_unreferenced_non_merge_commits(tmp_path: Path) -> None:
    def git(*args: str) -> None:
        subprocess.run(
            ["git", "-c", "user.name=t", "-c", "user.email=t@t", *args],
            cwd=tmp_path,
            check=True,
            capture_output=True,
        )

    git("init", "-q", "-b", "main")
    git("commit", "-q", "--allow-empty", "-m", "base")
    git("commit", "-q", "--allow-empty", "-m", "docs: ADR14 record system")
    git("commit", "-q", "--allow-empty", "-m", "fix typo")
    missing = commits_without_record("HEAD~2..HEAD", cwd=tmp_path)
    assert [m.split(" ", 1)[1] for m in missing] == ["fix typo"]
