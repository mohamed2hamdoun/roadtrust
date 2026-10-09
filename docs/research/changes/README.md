# Change records

One change = one commit = one record here. A record lets anyone retest or undo a single
change without reading the rest of the history.

File name: `CR-NNN-<short-slug>.md` ([template](../templates/change_record.md)). Technology
choices go in an ADR ([template](../templates/decision_record.md)) under
[decisions](../decisions/); the CR that implements an ADR links to it.

## Record format

1. **Finding and evidence** — what was wrong or missing, how it was measured, the numbers.
2. **What exactly changed** — file:line list, before and after.
3. **Why this option** — one paragraph.
4. **Pros**
5. **Cons** — including what this change does not fix.
6. **Alternatives considered** — each with why it was not chosen and what would make it
   the better choice later.
7. **How to retest** — exact commands and expected output.
8. **How to change or revert** — `git revert` the commit that added the record (find it
   with `git log --diff-filter=A --format=%h -- <record file>`), plus what to edit to
   switch to an alternative.

## Enforcement ([ADR14](../decisions/ADR14-record-system.md))

- `tools/research/validate_registry.py` fails if a record lacks a required section, a CR
  file is missing from the index below (or the reverse), an ADR file is not registered in
  `registries/decisions.json`, or a commit cited there does not exist.
- Every commit message must name its record (`ADRnn` or `CR-nnn`): checked by the
  `commit-msg` hook locally and by CI on every pull request.

## Index

| CR | Title | Plan step | Status |
|---|---|---|---|
| CR-001 | [Add VeReMi NextGen attack names to the threat catalog](CR-001-veremi-nextgen-attack-names.md) | 1.5 | applied |

A record's commit is found from git (see item 8), so the index does not repeat it.
