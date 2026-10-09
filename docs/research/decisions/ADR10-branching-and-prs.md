# ADR10: One short branch and one pull request per plan step

Status: accepted · 9 October 2026 · Decided by: Mohamed Hamdoun · Plan step 0.3

## Decision

- Every plan step gets its own branch from `main`, named `p<phase>/<step>-<slug>`
  (example: `p0/0.3-repo-layout`).
- Each branch opens a draft pull request into `main`. The owner reviews and merges.
- Inside a branch, one change = one commit = one change record (CR) or decision record
  (ADR), so any single change can be reverted.
- PRs are merged with a **merge commit** (not squash, not rebase). GitHub's squash and
  rebase options both create new commit hashes; a merge commit keeps every recorded
  commit on `main` with the exact hash its change record cites.
- The only commit made directly on `main` is the initial import (`994d044`).

## Why

Small PRs are easy to read and easy to undo. Keeping each recorded commit intact on
`main` keeps the promise that every change record points at exactly one revertible commit.

## Pros

- Each step can be reviewed, tested and reverted on its own.
- `main` always shows completed steps only.
- Change records link to real commits on `main`.

## Cons

- More PRs to open and merge.
- Steps that depend on an unmerged step need either a wait or a stacked branch.
- `main` gets one extra merge commit per PR. Use `git log --first-parent main` to see
  one line per step, plain `git log` to see every change.

## Alternatives considered

| Alternative | Why not chosen | When it would be better |
|---|---|---|
| One long rebuild branch | One huge, risky merge at the end; `main` shows nothing for months | Never for a multi-month rebuild |
| One PR per phase | Phases like P2 or P4 are large; PRs would be too big to review | If PR overhead becomes the bottleneck for a solo developer |
| Squash merging | Collapses several recorded commits into one, breaking the record-to-commit link | If each step only ever has one commit |
| Rebase merging | Linear history, but GitHub creates new hashes, so every record must be updated after merge | If a linear `main` matters more than stable hashes |

## How to retest

```bash
git log --first-parent --oneline main   # one merge per plan step
git log --oneline main                  # every recorded change, hashes match the records
gh pr list --state all          # one PR per plan step
```

## How to change or revert

Switch merge style in the GitHub repo settings (Settings → General → Pull Requests) and
update this record. Moving to phase-level PRs only changes how branches are named and
cut; no history is rewritten.

## Revisit trigger

PR overhead slows the work noticeably, or a second developer joins and needs a different
review flow.
