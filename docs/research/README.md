# RoadTrust: research and development dossier

**Version 1 · 9 October 2026 · Owner: Mohamed Hamdoun**

Repository reviewed: `mohamed2hamdoun/Cyberthorn-project` at commit `b4c4a03d1ff852a07c8ffa4c53167b59f5662567` (8 October 2026). Current application package: RoadTrust 0.3.0.

The objective is to turn the hackathon prototype into a reproducible, evidence-backed vehicle-communication security platform, then a deployable monitoring application. Every important choice should be traceable from a requirement to a source, dataset, feature, experiment, decision and test.

This first delivery contains a source-code audit, a targeted literature evidence map, seven dataset candidates, a registry of all 17 existing features, 13 experiment definitions, failure scenarios, technology decisions to evaluate, and staged delivery gates. **It does not claim that external-data benchmarks, blockchain deployment, simulator integration or the GUI overhaul have already been performed.** Algorithm winners and observed limitations stay empty until measured.

## Read in this order

1. [Scope and target product](00_scope.md)
2. [Verified baseline and gaps](01_repository_audit.md)
3. [Literature review method and synthesis](02_literature_review.md)
4. [Vehicle signal flow and failure cases](03_vehicle_and_failures.md)
5. [Datasets and feature evidence](04_data_and_features.md)
6. [Algorithm experiments and selection](05_experiments.md)
7. [Blockchain architecture and comparison](06_blockchain.md)
8. [Simulation and hardware path](07_simulation.md)
9. [Application architecture and GUI](08_application_and_gui.md)
10. [Delivery gates and first work sessions](09_delivery_plan.md)
11. [Traceability, templates and open decisions](10_traceability.md)
12. [Primary sources and reading depth](11_sources.md)
13. [Rebuild from scratch: step-by-step plan](12_rebuild_plan.md) — supersedes the order in 09

The machine-readable records are under [registries](registries/). Templates are under [templates](templates/). Run `python tools/research/validate_registry.py` from the repository root to check their relationships. This command validates documentation records, not application readiness.

## The first build target

A receiver-side **offline-capable V2X monitoring pipeline** that replays a pinned external benchmark, shows exactly which inputs are available, evaluates several baselines fairly, explains alerts, and queues verifiable evidence. Build a private web interface around this pipeline after its contracts stabilize. Explore CAN and perception through separate adapters and experiments.

## Status language

- **Verified in code:** observed in the pinned repository, with a path.
- **Archived measurement:** recorded by the repository; not automatically reproduced here.
- **Checked here:** explicitly executed during this review, with a bounded result.
- **Source-supported:** backed by a listed primary reference; reading depth is stated.
- **Proposed:** our design or test hypothesis; not an established result.
- **Pending:** requires data, experiment, stakeholder input or full-text review.

The actual judges’ detailed feedback was not available. It has not been reconstructed or invented.
