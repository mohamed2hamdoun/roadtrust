# ADR08: Build the new system in a separate repository

Status: accepted · 9 October 2026 · Decided by: Mohamed Hamdoun · Plan step 0.3

## Decision

Build the rebuilt RoadTrust in a new private repository, `mohamed2hamdoun/roadtrust`.
The hackathon code stays untouched in `mohamed2hamdoun/Cyberthorn-project` (tag
`v0.3.0-hackathon`, commit `b4c4a03`). The research documents were copied into the new
repository as its first commit (`994d044`), unchanged, with their origin recorded.

## Why

The rebuild shares no code with the hackathon system. A separate repository means
nothing old can be imported by accident, the new history starts clean, and the old demo
keeps working exactly as it did.

## Pros

- No risk of new code quietly depending on old modules.
- Clean history: every commit in the new repo belongs to the rebuild.
- The old demo, its docs and its PRs stay usable and unchanged.
- Private by default, so licenses and data terms can be checked before anything is public.

## Cons

- Git history of the research documents stays in the old repo; the new repo only has a
  copy. Use the old repo to trace who changed a research document before 9 October 2026.
- Two repos to keep in mind; old-repo PR #1 and branch `plan/roadtrust-rebuild` are now
  historical.
- Comparing new results with the old model needs the old repo checked out (the E01
  record gives the exact commands).

## Alternatives considered

| Alternative | Why not chosen | When it would be better |
|---|---|---|
| Same repo, new code beside the old | Old and new code mixed until P10; easy to import old modules by accident | If one continuous history matters more than a clean start, e.g. for a thesis that must show the evolution in one place |
| Same repo, delete old code now | Loses the runnable demo on the current branch | If nobody needs to run the old demo again |
| Carry research docs with git history (`git filter-repo`) | More steps for little gain; history remains in the old repo anyway | If authorship of every research edit must be visible in the new repo |

## How to retest

```bash
gh repo view mohamed2hamdoun/roadtrust --json visibility -q .visibility   # PRIVATE
python tools/research/validate_registry.py                                 # status PASS
```

Compare the copied files with the source:

```bash
diff -r <Cyberthorn-project>/docs/research docs/research   # only post-import edits differ
```

## How to change or revert

- Go back to one repository: copy the new repo's `docs/` and code into a folder of
  `Cyberthorn-project` and archive this repo. The research docs are already in both.
- Make it public: `gh repo edit mohamed2hamdoun/roadtrust --visibility public` (check
  that no dataset files, keys or personal recordings are in the history first).

## Revisit trigger

Publishing the project, adding outside collaborators, or a thesis/paper requirement for a
single continuous history.
