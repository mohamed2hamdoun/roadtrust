# ADR14: Every change carries a checked record

Status: accepted · 9 October 2026 · Decided by: Mohamed Hamdoun (format and all three
enforcement levels) · Plan step 0.5

## Decision

**Format.** Decision records use the structure of ADR08–ADR13: Decision, Why, Pros, Cons,
Alternatives considered (why not / when better), How to retest, How to change or revert,
Revisit trigger. The old dossier template is replaced. Change records (CR) use the eight
sections listed in `changes/README.md`. Templates: `templates/decision_record.md`,
`templates/change_record.md`.

**Enforcement, three levels:**

| Level | Tool | Fails when |
|---|---|---|
| Record files | `tools/research/validate_registry.py` (CI, pre-commit) | An accepted ADR or any CR lacks a required section; a CR file and the CR index disagree; an ADR file is not in `decisions.json`; a commit listed in a decision's `commits` field is not in git |
| Commit messages | `tools/check_commit_refs.py` (CI on PRs, `commit-msg` hook) | A non-merge commit message contains no `ADRnn` or `CR-nnn` |
| Pull requests | `.github/pull_request_template.md` | Not enforced; prompts for plan step, records, retest, revert, limits |

**Commit lookup.** A record never types its own commit hash (impossible: the record is
inside that commit). The commit that added a record is found with
`git log --diff-filter=A --format=%h -- <record file>`. Hashes may be cited afterwards in
the `commits` field of `decisions.json`; ADR08–ADR13 have been backfilled and are verified.

CI now checks out full history (`fetch-depth: 0`) so these lookups work.

## Why

The owner wants to retest or reverse any decision later without asking anyone why it was
made. That only works if records exist for every change and are complete. Templates alone
drift; checks that fail the build don't.

## Pros

- No commit can reach a PR without naming its reason.
- Incomplete records (for example, missing alternatives or revert steps) fail CI.
- Record-to-commit links can't go stale: they are derived from git, or verified when cited.
- Both the validator and the commit checker were shown to fail on broken input (missing
  section, unindexed CR, unregistered ADR, invented commit, message without reference).

## Cons

- **Small fixes need a record too.** A typo fix must cite an existing record (for example
  the CR it corrects) or get a short new CR. This is deliberate, but it adds friction.
- Checks verify structure, not quality: a record with empty sections under the right
  headings still passes. Review is still needed.
- Full-history checkout makes CI slightly slower as the repository grows.
- Commit messages naming the wrong record are not detected.
- The `commit-msg` hook needs `uv run pre-commit install` once per clone; CI catches it
  otherwise.

## Alternatives considered

| Alternative | Why not chosen | When it would be better |
|---|---|---|
| Old dossier template | No explicit pros/cons or retest/revert steps, which the owner asked for | For pure research decisions, its source/experiment fields could be merged back in |
| Templates without checks | Records drift or get skipped | Never, given the owner's goal |
| Exempt commit types (`chore:`, typo) from the message check | Owner chose the strict rule | If friction on trivial commits becomes a real cost |
| Typing commit hashes into the CR index | A record can't contain its own commit's hash; would need a follow-up commit every time | — |
| A GitHub App/bot for PR checks | Extra service; a script in CI does the same | If several repos need the same rules |

## How to retest

```bash
uv run python tools/research/validate_registry.py     # status PASS, 6 cited commits verified
uv run pytest                                         # 3 passed, incl. commit-message tests
echo "fix typo" > /tmp/m && uv run python tools/check_commit_refs.py --message-file /tmp/m
#   → exit 1, "Commit message has no ADR/CR reference"
uv run python tools/check_commit_refs.py main..HEAD   # exit 0 on this branch
```

To see a record check fail, delete a `## Cons` heading from any ADR and rerun the validator.

## How to change or revert

- Relax the message rule: add exemptions to `has_record` in `tools/check_commit_refs.py`,
  or delete the `commit-record` hook and the last CI step.
- Change required sections: edit `ADR_HEADINGS` / `CR_HEADINGS` in
  `tools/research/validate_registry.py` and the two templates together.
- Undo everything: `git revert` the commit that added this file.

## Revisit trigger

Record friction slows routine work, a second contributor joins, or records start passing
the checks while being empty.
