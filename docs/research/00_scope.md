# 00 — Scope and target product

## A precise product definition

**Proposed:** RoadTrust observes received vehicle communications, checks authenticity and data quality where the transport supports it, detects suspicious behavior, explains the detector output, and preserves evidence for an operator. The initial user is an RSU/fleet security operator or researcher. The initial deployment is an edge receiver plus a private analysis service.

The first milestone is a deployable monitoring platform. Integrating software into a vehicle’s safety-critical control path is a separate project with additional engineering, testing and assurance obligations. The first platform produces observations and alerts, not braking or steering commands.

Keep three domains explicit:

| Track | Inputs | Primary question | Relationship to current code |
|---|---|---|---|
| A. V2X receiver security | Claimed position/speed, observed arrival timing, available radio/authentication metadata | Is a received message misleading, abusive or untrustworthy? | Direct continuation; first priority |
| B. In-vehicle network security | CAN/CAN FD frames, gateway observations, decoded signals where available | Is communication inside the car anomalous? | Separate schema, model and evaluation |
| C. Cooperative perception consistency | Camera/LiDAR tracks, ego motion and cooperative reports | Does independent perception support a report? | Later research extension |

A connected car is not necessarily autonomous. Autonomous sensing, in-vehicle control messages, V2X broadcasts and cloud telemetry are different sources. A dataset containing real cars does not automatically validate a detector for all of them.

## Initial requirements

| ID | Requirement | Acceptance evidence |
|---|---|---|
| R01 | Every input has documented units, provenance, trust and availability | Adapter contract plus sample audit |
| R02 | The feature path is causal and identical offline/online | Prefix-invariance and replay-parity checks |
| R03 | No source lineage, label or hidden identity leaks into evaluation | Pairwise split/lineage audit |
| R04 | Selection compares detection and false alarms with resource cost | Frozen protocol and reproducible run bundle |
| R05 | WAN or blockchain failure does not halt local detection | Failure-injection trace and bounded queue behavior |
| R06 | Explanations distinguish attribution from verified incident truth | Fidelity checks and operator tasks |
| R07 | Evidence is durable and independently verifiable | Crash recovery, tamper and receipt tests |
| R08 | A real chain demonstrates independently validated transactions | Multi-node consensus and quorum-loss evidence |
| R09 | Simulators expose the phenomena claimed in the evaluation | Pinned configuration and receiver traces |
| R10 | The GUI is a client of the service, with clear stale/offline states | API, authorization and usability checks |
| R11 | A deployment can be installed, monitored, backed up and rolled back | Rehearsed staging runbook |
| R12 | Conclusions name the data and operational conditions supporting them | Limitations and claim-to-evidence register |

## Meaning of “ready”

A research release is ready when another person can reproduce the dataset manifest, feature extraction, split, selected threshold and report. A staging application is ready when authentication, data durability, observability, load behavior and recovery have been demonstrated. A field pilot is ready only after the hardware, operating conditions, data rights, stakeholders and acceptable risks are specified. These are different completion states.

## Working assumptions to validate

1. Retain Python for the research core because the existing implementation and tests are in Python. A different runtime can be justified later by a measured edge constraint.
2. Prefer an RSU/edge-computer observer for the first integration; final hardware is unselected.
3. Treat disconnected operation as a normal state. Cloud services enrich operations; they are not a prerequisite for the local detector.
4. Keep the existing demo available as a regression fixture and historical baseline.
5. Use available compute before committing to a new purchase. A known Apple Silicon development machine does not establish simulator compatibility.
6. Confirm team availability, intended user and budget before assigning dates. This dossier provides ordered milestones rather than an unsupported calendar promise.

## Information still needed

- Which deployment is the first target: lab replay, roadside unit, fleet back office or on-vehicle monitor?
- Which V2X protocol/profile, radio and geographic deployment requirements apply?
- Who would operate independent blockchain validators and why should they distrust each other?
- What real data access, GPU/lab access and weekly engineering capacity are available?
- What did judges identify as the most important weaknesses? Preserve their actual wording when available.

None of these prevents the first external-data adapter and benchmark work from starting.
