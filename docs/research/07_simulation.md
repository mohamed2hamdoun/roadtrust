# 07 — Simulation and hardware path

## Select fidelity to answer a question

| Tool | Best initial role | What it does not establish alone |
|---|---|---|
| Existing Python simulator | Fast regression and feature fixtures | Radio delivery, sensor realism or vehicle integration |
| SUMO-based mobility | Road layouts, vehicle interaction and traffic scenarios | Packet transmission or RF propagation |
| Veins + OMNeT++ + SUMO [S15] | Coupled mobility and network experiments | Every modern radio profile, including PC5, without the right model |
| Eclipse MOSAIC [S18] | Coordinating domains and reproducing a compatible scenario stack | Correctness of every coupled simulator/version |
| ns-3 / appropriate NR-V2X module [S19] | Detailed cellular/sidelink research when required | That a generic 5G package contains the needed sidelink configuration |
| CARLA, optionally coupled to SUMO [S16] | Sensors, driving scenes and later perception experiments | A validated V2X network stack |
| SocketCAN / virtual CAN [S01] | CAN ingestion/replay contract and parser tests | Bus wiring, transceiver faults or real arbitration timing |
| Bench hardware / authorized field capture | Device timestamps, throughput, drivers and real noise | Broad road generalization from one setup |

**Proposed first spike:** compare a NextGen-compatible MOSAIC path with a minimal Veins/SUMO path. Reproducing an external benchmark may favor MOSAIC; a narrower network experiment may favor Veins. Decide using installability, protocol fit, reproducibility and trace quality. CARLA follows only when sensor/driving research needs it.

## Integration contract

Each adapter emits the same receiver-observation envelope. Preserve simulator truth in a separate stream. For network experiments, use the receiver delivery event, not a globally visible list of every transmitted message. Lost frames must remain absent from the observed stream. Track transmitted, delivered, rejected and processed counts independently.

Use one declared simulation clock, deterministic stepping policy, pinned seeds and versioned maps. Define vehicle-ID mapping, coordinate conversion, traffic-light ownership and time synchronization for coupled simulators. Report wall-clock latency separately from simulated time. Freeze the external detector interface and buffer policy before benchmarking.

## E10 acceptance tests

1. Replay an identical seeded scenario twice and compare normalized observations; explain any nondeterminism.
2. Verify a stopped vehicle, constant-speed motion, a turn and a hard brake against known trajectories.
3. Confirm receiver-specific visibility and packet loss under a selected network model.
4. Verify timestamp/position/heading conversions and no oracle fields entering features.
5. Compare the current extractor on a hand-audited fixture before and after adapter integration.
6. Measure density, offered load, delivery ratio, end-to-end delay and queue behavior independently of IDS accuracy.
7. Run paired benign impairments and attacks so the detector cannot equate every bad link with malicious behavior.
8. Export a manifest containing simulator versions, commit hashes, map/configuration, seed, run command and observation schema.

DoS attacks post-processed into an offline log cannot measure feedback into radio scheduling or traffic behavior. To claim those effects, run attacks in a coupled closed-loop simulation and inspect network/application outcomes. This matters for interpreting D03 [S08].

## Hardware feasibility

The inspected CARLA package guide targets Windows/Ubuntu and a dedicated GPU [S17]. Confirm the exact release and supported architecture before scheduling work on an Apple Silicon Mac. Prefer existing university/lab hardware for a compatibility spike; do not commit to purchases or cloud costs from a generic specification.

Keep independent environments for research, simulator client/server and blockchain nodes. Their Python/runtime versions may differ. A protocol adapter is a cleaner boundary than forcing all dependencies into one environment.

## Reproducibility deliverables

A small deterministic scenario, a receiver trace, a separate ground-truth file, the adapter, a manifest, conversion fixtures and a report of what the simulator models and omits. Screenshots and a convincing animation are supplementary artifacts, not simulation validation.
