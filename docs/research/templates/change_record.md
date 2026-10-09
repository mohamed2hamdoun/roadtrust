# CR-nnn: <change in one line>

Status: applied · <date> · Plan step <n.n> · Implements: ADRnn (if any)

<!-- File: docs/research/changes/CR-nnn-<slug>.md. Add a row to changes/README.md.
The validator fails if any heading below is missing. -->

## Finding and evidence

What was wrong or missing, how it was measured, the numbers.

## What exactly changed

File and line list, with before and after.

## Why this option

## Pros

## Cons

Include what this change does not fix.

## Alternatives considered

| Alternative | Why not chosen | When it would be better |
|---|---|---|

## How to retest

Exact commands and the expected output.

## How to change or revert

The commit that added this file is
`git log --diff-filter=A --format=%h -- <this file>`; `git revert` that commit to undo the
change. Say what to edit to switch to an alternative instead.
