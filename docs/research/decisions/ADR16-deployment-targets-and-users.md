# ADR16: Two deployment profiles (RSU and on-vehicle) on one core, for operators and researchers, monitoring only

Status: accepted · 9 October 2026 · Decided by: Mohamed Hamdoun · Plan step 1.1 ·
Supersedes: ADR01 (proposed RSU-only boundary)

## Decision

**Deployment profiles.** RoadTrust targets two receivers from the start, built on one
shared detection core:

| | `rsu` profile | `obu` profile |
|---|---|---|
| Runs on | Roadside unit / edge computer | On-board unit or computer in one vehicle |
| Observes | V2X messages received at a fixed site | V2X messages received by one moving vehicle |
| Extra trusted input | Its own surveyed position | Optional ego-sensor channel: own GNSS, speed, heading, IMU |
| Constraints | Few | Power, CPU, memory, intermittent connectivity |
| Evidence | Uploads continuously | Stores locally, uploads when connected |
| Alert goes to | Operator GUI | Misbehavior report to the authority **and** a driver warning display |

- The receiver-observation format (P3) records the receiver type and carries the optional
  ego channel from version 1.
- Every evaluation (P5–P6) reports results per profile; a detector may differ per profile.
- The `obu` detector must work without ego data and may use it when present.
- Lab bench order (after replay): RSU first, then OBU.

**Users.** One application with role-based screens:

- Road-authority operator: live monitoring, incident investigation, evidence verification.
- Researcher: everything above plus datasets, experiments and the simulation lab. Ground
  truth is visible only in research/replay mode.

**Realism.** Replay of datasets and simulator traces through the real pipeline first,
then a live lab bench. A field pilot is out of scope until separately decided.

**Boundary.** Monitor and alert only. RoadTrust never brakes, steers or blocks messages.

**Driver warning display.** Built as a prototype in the lab and simulator only. It gets
its own, stricter false-alarm budget (step 1.4). Any on-road use requires a separate
driver-distraction and in-vehicle HMI safety review, recorded as its own decision.

## Why

Both targets see the same kind of V2X message, so one core avoids duplicate work while the
profiles capture what genuinely differs: field of view, trusted local data and resources.
Defining both in the data format from day one stops the core from quietly assuming an RSU
view. The on-vehicle profile's main advantage is its own sensors, which give an
independent check on what other vehicles claim. Researchers and operators share most
screens, and a single app keeps the evaluation and the operational view of an alert
identical.

## Pros

- Covers both places where V2X misbehavior is detected in practice.
- One codebase, one data format, one benchmark harness.
- Ego-sensor cross-checks give the OBU evidence that sender claims alone can't.
- Monitoring-only keeps the project out of safety-critical vehicle-control certification.
- Researchers see exactly what operators see, plus evaluation tools.

## Cons

- Every phase does more work: two profiles to define, evaluate and test on hardware.
- OBU evaluation needs receiver-side ego data; public datasets may not provide it, which
  raises the value of recording real vehicle data (P4B) or simulating it.
- **A driver display turns false alarms into driver distraction.** A detector acceptable
  for an operator queue may be unacceptable in a car. This needs its own budget and, for
  road use, an HMI safety review.
- The OBU's limited CPU and memory may rule out models that are fine on an RSU.
- Role-based screens need real server-side authorization (P8).

## Alternatives considered

| Alternative | Why not chosen | When it would be better |
|---|---|---|
| RSU only (ADR01 proposal) | Owner wants on-vehicle monitoring too | If time runs short; OBU can drop to a later phase |
| RSU end to end first, OBU after P8 | Core would likely assume the RSU view and need rework | If the first deadline needs a single complete demo |
| Two separate systems | Duplicate code and evaluation | If the profiles turn out to need incompatible detectors and data |
| Back-office / cloud analysis as the target | Not real time; depends on connectivity | As a later addition receiving OBU/RSU reports |
| In-vehicle CAN monitor | Different data and attacks | Stays a separate optional track (plan B19) |
| OBU without ego data | Gives up the OBU's main advantage | If ego data proves unavailable or untrustworthy |
| No driver display (report only) | Owner chose to include it | If false-alarm rates cannot meet the driver budget |
| Message filtering | A false positive could hide a real safety warning | Never within this project's boundary |
| Separate research toolkit | Less consistent with what operators see | If GUI effort must be cut |

## How to retest

This is a scope decision; later artifacts must show it:

- P3: the observation schema has a receiver-type field (`rsu`/`obu`) and an optional ego
  channel; schema tests cover both.
- P6: every benchmark report has separate per-profile tables.
- P8/P9: the API enforces operator vs researcher roles server-side; ground truth is absent
  from operator responses.
- P9: the driver warning exists only in lab/simulator builds.

## How to change or revert

Drop a profile by removing it from the schema's allowed receiver types and the benchmark
matrix; record the change. Removing the driver display deletes one GUI component and its
budget. Undo the whole decision with `git revert` on the commit that added this file and
restore ADR01's status to `proposed`.

## Revisit trigger

OBU ego data unavailable in every dataset and recording option; the driver-warning
false-alarm budget proves unreachable; a partner offers a field pilot; or the team cannot
sustain two profiles.
