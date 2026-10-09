# ADR15: Data on the internal disk under a 60 GB cap, outside the repository; CARLA on the lab GPU

Status: accepted · 9 October 2026 · Decided by: Mohamed Hamdoun · Plan step 0.6

## Decision

- **Location.** All large project data (datasets, simulator output, chain data) lives in
  one folder outside the repository: `~/roadtrust-data` by default, changed with the
  environment variable `ROADTRUST_DATA_DIR`. Code gets the path from
  `roadtrust.paths.data_dir()`, which refuses any path inside the repository.
- **Budget.** Internal disk, with a 60 GB cap on project data. If the project needs more,
  move the folder to an external SSD and set `ROADTRUST_DATA_DIR`; no code changes.
- **Size check before download.** Every dataset's size is recorded on its data card and
  checked against the remaining budget before full download (plan step 4A).
- **Compute.** The Mac (Apple M4, 16 GB RAM) runs development, tests, SUMO/Veins/Artery/
  MOSAIC in Docker, blockchain nodes and the GUI. CARLA (optional perception track, P4C.5)
  runs on the owner's university lab machine with an NVIDIA GPU.

Measured on 9 October 2026: 100 GB free on the internal disk (460 GB volume, 77 % used).
Docker Desktop uses 7.2 GB on disk, of which 3.8 GB are unused volumes left for the owner
to review.

## Why

With 100 GB free, the estimated project need (about 25–80 GB, see below) fits if it is
watched. A cap leaves about 40 GB for macOS updates and swap. Keeping data outside the
repository means a dataset cannot be committed by accident, and moving to an SSD later is
one setting.

Rough needs used for the cap (to be confirmed per data card): tools 2–3 GB; simulator
images 5–10 GB; Besu/Fabric images 3–5 GB; datasets 10–60 GB.

## Pros

- No new hardware or cost now.
- Datasets can never enter git through `data_dir()`: the guard raises instead.
- One environment variable moves everything.
- CARLA's Windows/Linux + NVIDIA requirement is met without buying hardware.

## Cons

- The 60 GB cap is checked by hand (`du -sh ~/roadtrust-data`, `docker system df`) until
  the download tooling in P4 automates it.
- Docker images are stored in Docker Desktop's own disk image, not in
  `~/roadtrust-data`; they count toward the budget but are moved separately (Docker
  Desktop → Settings → Resources).
- The size estimates are unverified; a large dataset may force the SSD move early.
- 16 GB RAM may limit running a 4-node chain and a simulator at the same time; measured
  when P4C/P7 start.
- Work that needs CARLA depends on lab access and scheduling.

## Alternatives considered

| Alternative | Why not chosen | When it would be better |
|---|---|---|
| External SSD from the start | Not needed at 100 GB free; adds a drive that must be plugged in | When project data passes 60 GB |
| University or cloud machine for all heavy work | Setup and access overhead before it is needed | If datasets exceed SSD size or simulations need more RAM/CPU |
| `data/` inside the repo, ignored by git | One `.gitignore` mistake commits a dataset; deleting the repo deletes the data | For tiny example fixtures only (those go in `core/tests`) |
| CARLA on this Mac | Not supported for Apple Silicon in the reviewed documentation (source S17) | If an official Apple Silicon build appears |

## How to retest

```bash
uv run pytest core/tests/test_paths.py     # 3 passed: default, override, inside-repo rejected
df -h /System/Volumes/Data                 # free space
du -sh ~/roadtrust-data; docker system df  # project usage vs the 60 GB cap
```

## How to change or revert

- Move data: `export ROADTRUST_DATA_DIR=/Volumes/<ssd>/roadtrust-data` (add it to your shell
  profile), then move the folder.
- Change the cap: edit this record and the data-card checks in P4.
- Undo: `git revert` the commit that added this file (removes `roadtrust/paths.py`).

## Revisit trigger

Project data passes 60 GB, free space drops below 40 GB, RAM limits concurrent
simulator and chain runs, or lab GPU access changes.
