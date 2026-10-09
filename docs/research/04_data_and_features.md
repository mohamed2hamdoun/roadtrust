# 04 — Data acquisition and feature evidence

## Dataset roles

| ID | Source | What to take | What to avoid claiming |
|---|---|---|---|
| D01 | Existing generator | Regression fixtures, known label/edge-case behavior | External generalization |
| D02 | VeReMi Extension [S07] | Receiver-observable kinematics and timing after a version-specific audit | Real field-recorded attacks |
| D03 | VeReMi NextGen [S08–S09] | Candidate CAM benchmark; preserve official splits and audit lineage | Network disruption demonstrated by offline attack overlays |
| D04 | nuScenes CAN expansion [S10] | Timestamped benign ego motion/IMU/steering; unit-aware consistency tests | Remote V2X attack truth or a joint multi-car radio log |
| D05 | BerlinV2X [S11] | Real radio/GPS conditions for benign impairment analysis | A complete labelled intrusion dataset without verification |
| D06 | ROAD [S12–S13] | Real CAN traces with per-attack provenance | Direct comparability with V2X spatial features |
| D07 | DAIR-V2X / V2X-Seq [S14] | Later perception/trajectory consistency studies | Camera annotations as malicious-message labels |

All external sources are **not acquired** in this work. Links identify candidate sources, not downloaded assets. Access terms, license, permitted redistribution and storage cost must pass the dataset gate before ingestion. A repository code license does not establish the dataset license.

Do not concatenate unrelated rows from these sources. Their clocks, identities, semantics and labels are not aligned. A synthetic V2X message generated from a real trajectory is a **real trajectory with a synthetic communication/attack overlay**. Keep that lineage visible.

## Verified example field mappings

These are schema-level candidates, not a tested parser:

| Dataset field | Proposed use | Important check |
|---|---|---|
| D03 `rcvTime`, `sendTime` | Receive/source time; convert nanoseconds relative to epoch | Keep trusted observation time separate from claims |
| D03 `sender_alias` | Observable identity key | Test rotation, reuse and receiver scope |
| D03 `sender_id` | Offline grouping/lineage only | Do not use hidden persistent identity to make tracking easier |
| D03 `sender.pos`, `.spd`, `.acl`, `.hed` | Claimed kinematics | Verify axis/heading conventions and units on a sample |
| D03 `attacker` | Evaluation label only | Never model input |
| D03 noise fields, `driversProfile`, road-edge metadata | Audit observability first | Do not assume simulator metadata appears on the wire |
| D04 `pose.utime`, `pos`, `vel`, `accel` | Motion consistency track | Coordinate transforms and sample frequency |
| D04 `vehicle_monitor.vehicle_speed` | Alternate speed observation | km/h to m/s; align causally with other signals |
| D04 `imu.linear_accel`, steering feedback | Later independent motion checks | Sensor frame and measurement semantics |
| D05 GPS/radio tables | Link conditions and benign robustness | Match recording/device clocks, measure gaps; exact adapter schema pending |
| D06 CAN capture fields | CAN ID, payload, size and timing candidates | Confirm release format and signal-decoding rights before mapping |

RSSI is absent from the inspected D03 message schema. Its absence must be represented. A reduced-input model is a separate versioned model; adding a constant RSSI to an old model is not validation.

## The feature component the project needs

The proposed **Feature Evidence Registry** is both a research record and the source of a future GUI Feature Inspector. Every feature card records:

1. Name, unit, coordinate/clock convention and exact causal formula.
2. Raw dependencies; observable versus claimed versus oracle classification.
3. Source website, file/version/hash, decoder and receiver hardware requirements.
4. Threat hypothesis and benign situations with the same symptom.
5. Missing/first-message/stale behavior, state size and computation cost.
6. Primary references and their actual reading depth.
7. Feature-group and single-feature ablations, robustness checks and external validation.
8. Keep/revise/remove decision, measured benefit, observed limitations and revisit trigger.

`registries/features.json` contains all **17 current features**, extracted from the repository’s own `FeatureSpec` records and supplemented with deployment caveats. It does not assert that any of them has passed external validation.

## Review of every current input

| Group | Features | Main question before retention |
|---|---|---|
| Claimed kinematics | `speed_mps`, `acceleration_mps2` | Are values meaningful for this vehicle, field and unit? Can the attacker falsify them consistently? |
| Observation quality | `latency_ms`, `signal_strength_dbm` | Can the receiver actually measure them with useful accuracy? |
| Motion history | `position_jump_m`, `jump_excess_m`, `speed_change_mps`, `speed_change_excess_mps`, `heading_change_abs_rad` | Do noise, time gaps and aliases explain the residual? |
| Receiver traffic | `sender_msgs_in_window`, `network_msgs_in_window`, `sender_share_in_window`, `duplicate_payloads_in_window` | Do honest congestion, adaptive rate and stationary vehicles create the same signature? |
| Identity history | `sender_age_s`, `active_senders_in_window` | Does privacy rotation or changing visibility dominate the feature? |
| Spatial comparison | `cospatial_senders`, `nearest_sender_distance_m` | Does closeness distinguish abuse after uncertainty and traffic context are considered? |

Candidate new inputs include explicit uncertainty, missingness masks, interarrival variation, authentication/freshness status, physically normalized residuals and independent sensor agreement. Their inclusion is conditional on observability and measured incremental value. A persistent physical identifier, attacker flag, file name or attack-specific metadata is not an acceptable shortcut.

## Unit/component verification

The extractor must pass causal prefix invariance; receiver/session isolation; deterministic arrival ordering; unit/coordinate conversion fixtures; equal and out-of-order timestamps; heading wrap; pseudonym rotation; absent first history; stale neighbor expiry; unknown/unavailable values; noise near thresholds; bounded memory under many aliases; and replay parity with the offline builder.

Distinguish a zero-valued measurement from an unavailable one. Never interpolate using future samples in a streaming test. Fit scaling, imputation, dimensionality reduction and feature selection on training data only.

## Acquisition gate

For each source, obtain the smallest useful sample; record access date, version, checksum, license and sizes; inspect schema and labels; calculate missingness and durations; establish drive/scenario/receiver lineage; inspect which fields are attacker-controlled; and produce a data card. Then approve a manifest for full download. Preserve source bytes immutably and produce normalized data with a versioned adapter.

Start D03 versus D02 with a small compatibility audit. Prefer the source whose fields and lineage can be explained and reproduced. The final benchmark choice remains provisional until that audit succeeds.
