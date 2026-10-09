# Change records

One change = one commit = one record here. A record lets anyone retest or undo a single
change without reading the rest of the history.

File name: `CR-NNN-<short-slug>.md`. Technology choices go in an ADR
([template](../templates/decision_record.md)); the CR that implements an ADR links to it.

## Record format

1. **Finding and evidence** — what was wrong or missing, how it was measured, the numbers.
2. **What exactly changed** — file:line list, before and after.
3. **Why this option** — one paragraph.
4. **Pros**
5. **Cons** — including what this change does not fix.
6. **Alternatives considered** — each with why it was not chosen and what would make it
   the better choice later.
7. **How to retest** — exact commands and expected output.
8. **How to change or revert** — `git revert <sha>`, plus what to edit to switch to an
   alternative.

## Index

| CR | Title | Commit | Status |
|---|---|---|---|
| — | No changes recorded yet | — | — |
