# 09 — Delivery gates and first work sessions

Use milestones with evidence, not a promise to finish every research branch at once. Owners and dates can be assigned once capacity and hardware are known. A student-led effort of this breadth should be planned as sustained work across months, not a single GUI sprint; the actual duration remains unestimated.

| Milestone | Work and dependencies | Concrete output | Gate |
|---|---|---|---|
| M0. Baseline integrity | Code snapshot, A01/A02/metric semantics, reproducible environment | Corrected baseline report and regression fixtures | Clean run; complete pairwise split guard; accurate claims |
| M1. Real system understanding | Q01–Q03, trust map, sample dataset audits | Signal/device map, data cards and adapter contract | Every required field has observable provenance or declared absence |
| M2. External replay | M1; build one adapter/profile | Receiver logs through the shared feature path | Units, causality, alias handling and leakage checks pass |
| M3. Algorithm evidence | M0/M2; E02/E04/E05/E06/E08 | Reproducible comparison with failure analysis | Frozen evaluation and eligibility constraints; decision remains provisional until gate |
| M4. Network simulation | M1/M2; simulator compatibility spike and E07/E10 | Coupled receiver traces and robustness report | Loss/clock/network effects modeled and validated |
| M5. Real audit network | Durable store/outbox; E09 | Multi-node chain prototype and comparator report | Independent verification; quorum failure; restart/retry recovery |
| M6. Service and UI | Stable data, model and incident contracts | API, Feature Inspector, investigation UI and staging package | E11/E13; access control, recovery and meaningful health checks |
| M7. Controlled pilot | Successful earlier gates; target hardware/data agreements | Shadow deployment and operations/limitations report | Measured workload, rollback, monitoring and explicit operating boundary |

M3, M4 and M5 may overlap after their prerequisites, but each requires its own evidence. A prettier interface does not resolve missing training data, and a new chain does not improve detector validity.

## First ten focused sessions

1. Capture the actual judging feedback and confirm the initial operator/deployment target. Read the audit and keep unresolved decisions visible.
2. Reproduce the current baseline in a clean pinned environment; save exact commands and results. Correct score/metric wording and split guards.
3. Draw and verify one end-to-end signal path; identify trusted receiver measurements versus sender claims.
4. Audit one small D03 sample and one D02 sample: licenses, fields, clocks, aliases, labels and base-trajectory lineage.
5. Decide the first dataset/profile based on the audit. Freeze raw files and checksums; document why the other candidate is deferred.
6. Implement one adapter and conversion fixtures. Keep missing RSSI explicit. Prove receiver/session isolation and causal replay.
7. Review all 17 existing features using the registry. Choose candidate subsets and record exclusions before looking at final test results.
8. Freeze grouped evaluation, operational budgets and the first five model families. Add a minimal rules baseline.
9. Run the first controlled comparisons; investigate false incidents and missed events. Record failures and resource costs.
10. Write the first experiment report and decide the next measured gap: stronger simulation, novelty detection, edge cost or data quality.

These are ordered work units, not claims that each fits one hour or one day. Do not lock a blockchain implementation or full UI framework before the relevant spike has produced evidence.

## High-priority backlog

| ID | Task | Depends on | Done when |
|---|---|---|---|
| B01 | Correct RF score and average-precision language | None | Code comments, UI and incident metadata agree with actual output |
| B02 | Complete split/lineage guards | None | All pairwise overlap and duplicate-lineage fixtures are rejected |
| B03 | Clean reproduction and environment record | B01/B02 | Archived baseline is reproduced or discrepancy is explained |
| B04 | Dataset samples and rights audit | None | Two completed data cards with exact versions/checksums |
| B05 | Receiver observation schema | B04 | Every field has units, clock/trust and missingness semantics |
| B06 | First external replay adapter | B05 | Hand-audited fixture and causal replay checks pass |
| B07 | Feature profiles and evidence registry integration | B06 | Unsupported inputs are excluded/masked with retrained models |
| B08 | Experiment runner and result bundles | B03/B07 | Same manifest runs rules and candidate models reproducibly |
| B09 | Event metrics and grouped uncertainty | B08 | Matching/cooldown policy and confidence intervals documented |
| B10 | Classic-model benchmark and ablations | B09 | Failures and comparisons recorded; no arbitrary winner |
| B11 | Pseudonym, GNSS and clock campaign | B06 | Benign degradation and attacker behavior evaluated separately |
| B12 | Simulator compatibility spike | B05 | Pinned minimal scenario emits correctly timed receiver traces |
| B13 | Transactional incident store and outbox | B05 | Crash/retry/deduplication behavior verified |
| B14 | Signed-checkpoint audit baseline | B13 | Independent verifier detects rewritten history |
| B15 | Fabric/Besu comparison spike | B13/B14 | Real commits and partition behavior measured |
| B16 | API and headless pipeline | B07/B13 | UI-independent replay and investigation API |
| B17 | GUI prototype and Feature Inspector | B16 | Operator investigation task passes |
| B18 | Staging, load, backup and rollback | B15/B17 | Declared workload and recovery objectives demonstrated |
| B19 | Optional separate CAN track | B04 plus capacity | CAN-specific adapter/model/report; no mixed-domain claims |
| B20 | Optional perception consistency | B04 plus capacity | Independent sensor benefit beats added cost on a defined task |

## Research outputs worth aiming for

A reproducible benchmark, a feature availability/ablation study, a benign-impairment versus attack analysis, and an evidence-system fault comparison can each produce useful results even if a complex model or blockchain candidate loses. Decide a publication question after the first external benchmark exposes a real gap. Novelty and publishability are not established by combining more technologies.
