"""Fail when a commit message names no decision (ADRnn) or change record (CR-nnn).

Usage:
    check_commit_refs.py <revision-range>          # CI: every non-merge commit in the range
    check_commit_refs.py --message-file <path>     # commit-msg hook: the message being written
"""

import re
import subprocess
import sys
from pathlib import Path

RECORD = re.compile(r"\b(?:ADR\d{2,}|CR-\d{3,})\b")
HINT = "Name the record this commit implements, e.g. 'ADR14' or 'CR-001' (see docs/research)."


def has_record(message: str) -> bool:
    # Lines starting with '#' are git's editor comments, not part of the message.
    text = "\n".join(line for line in message.splitlines() if not line.startswith("#"))
    return RECORD.search(text) is not None


def commits_without_record(rev_range: str, cwd: Path | None = None) -> list[str]:
    log = subprocess.run(
        ["git", "log", "--no-merges", "--format=%h %s%x00%B%x01", rev_range],
        capture_output=True,
        text=True,
        check=True,
        cwd=cwd,
    ).stdout
    missing = []
    for entry in log.split("\x01"):
        header, _, body = entry.strip().partition("\x00")
        if header and not has_record(body):
            missing.append(header)
    return missing


def main(argv: list[str]) -> int:
    if argv[:1] == ["--message-file"] and len(argv) == 2:
        if has_record(Path(argv[1]).read_text()):
            return 0
        print(f"Commit message has no ADR/CR reference. {HINT}", file=sys.stderr)
        return 1
    if len(argv) != 1:
        print(__doc__, file=sys.stderr)
        return 2
    missing = commits_without_record(argv[0])
    for commit in missing:
        print(f"no ADR/CR reference: {commit}", file=sys.stderr)
    if missing:
        print(HINT, file=sys.stderr)
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
