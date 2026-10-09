# ADR09: One repository, folders added only when their phase starts

Status: accepted · 9 October 2026 · Decided by: Mohamed Hamdoun · Plan step 0.3

## Decision

All parts of RoadTrust live in this one repository. Top-level folders:

| Folder | Holds | Created in |
|---|---|---|
| `docs/` | Research dossier, decisions, change records, guides | Exists |
| `tools/` | Repository maintenance scripts (validators, generators) | Exists |
| `core/` | Python package `roadtrust`: schema, adapters, features, detectors, service | P0.4 / P3 |
| `sim/` | Simulator configs, Dockerfiles and trace exporters | P4C |
| `chain/` | Smart contracts / chaincode, node configs, verifier | P7 |
| `web/` | Operator GUI | P9 |
| `deploy/` | Compose files, runbooks, monitoring config | P10 |

A folder is created by the first change that needs it, never as empty scaffolding.

## Why

The parts share contracts: the observation schema (P3) is used by datasets, simulators,
the detector, the chain worker and the GUI. One repository lets a single PR change a
contract and every consumer together, and lets CI check them together. Creating folders
only when needed keeps the tree honest about what exists.

## Pros

- One PR can update a shared schema and all its users at once.
- One CI pipeline, one issue tracker, one place to look.
- Each folder keeps its own toolchain (Python in `core/`, Node in `web/`, Docker images
  in `sim/` and `chain/`), so dependencies don't collide.
- No empty folders pretending work exists.

## Cons

- The repository grows large over time (simulator configs, contracts, frontend).
  Datasets and large binaries must stay out of git (manifests and checksums only).
- CI must be split by path so a GUI change doesn't rerun simulator builds.
- Someone cloning for one part gets all parts.

## Alternatives considered

| Alternative | Why not chosen | When it would be better |
|---|---|---|
| All folders created now | Empty folders imply progress that doesn't exist | If a team needs to see the whole structure to divide work |
| Separate repos per part | Shared-schema changes need coordinated PRs across repos and version pinning | When parts have different owners or release on different schedules |
| Python-only flat package | Simulators, contracts and the web client aren't Python | Never, given the plan |

## How to retest

```bash
ls   # only folders whose phase has started should exist
```

## How to change or revert

Moving a folder to its own repo later is straightforward (`git subtree split --prefix=<folder>`
keeps its history). Reverting this ADR means choosing a different layout before P3
creates `core/`; after that, it becomes a migration.

## Revisit trigger

A part gets a separate owner or release cycle, or CI time for unrelated parts becomes a
real cost.
