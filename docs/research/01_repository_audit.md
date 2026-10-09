# 01 — Verified baseline and gaps

Review scope: the pinned tree and 50 text files were retrieved, including the core modules, tests and existing technical guides. No `AGENTS.md`, CI workflow, service deployment configuration or repository license file was present in that tree. Absence here is a finding about this snapshot, not a claim about infrastructure outside the repository.

## What is already useful

| Component | Evidence in repository | What to preserve |
|---|---|---|
| Streaming features | `av_xai_blockchain_demo/features/online.py`, `features/schema.py` | One feature implementation, explicit units/schema version, arrival sequence |
| Data generation | `simulator/generate_data.py`, `simulator/world.py` | Whole simulation sessions and declared benign edge cases |
| Detection | `ids/train_model.py`, `ids/predict.py` | Validation-selected threshold and separation of ground truth |
| Explanations | `xai/explain.py` | Additivity check and explicit explanation failure state |
| Evidence | `ledger/simple_blockchain.py`, `ledger/incident_logger.py` | Canonical hashing, atomic replacement and stable incident IDs |
| Interface | `dashboard/app.py`, root `app.py` | Observe → detect → explain → verify investigation flow |
| Tests/docs | Seven test modules; `docs/FINAL_SYSTEM_GUIDE.md`, `docs/ISSUE_REGISTER.md` | Existing edge cases, known limitations and historical issues |

## Baseline measurements: archived, not reproduced end to end

The committed `artifacts/evaluation.json` reports 32,297 test messages, 7,189 attacks, a threshold of 0.35, attack recall 0.9794, precision 0.9660, F1 0.9726 and normal-message FPR 0.009877. These are results from this synthetic generator, not road performance. The stored validation Sybil recall is about 0.8120 versus 0.9418 on test; this motivates uncertainty reporting and broader seeds.

The code stores `average_precision_score` under `pr_auc`. Average precision and trapezoidal area under a plotted precision–recall curve are different summaries. Use the exact metric name in future reports.

The README reports 120 tests. **The complete suite was not run during this review:** pytest, SHAP and Streamlit were unavailable in the review environment. No dependency installation, full training run or claimed metric reproduction was performed.

Bounded checks actually run here: generated an 80-message, two-second normal synthetic replay; confirmed all 17 feature values were finite; created/appended/verified a temporary ledger; and demonstrated on a tiny separate forest that `predict_proba=1/3` while its hard vote is zero. These checks establish only those narrow behaviors.

## Priority findings

| ID | Finding and evidence | Consequence / required work |
|---|---|---|
| A01 | `Detector.score_frame` uses `predict_proba`; comments and incident metadata call it a fraction of hard votes | Correct score semantics throughout. scikit-learn averages leaf class probabilities [S29]. It remains uncalibrated. |
| A02 | `train_model.main` checks train/test and train/validation session intersections, omitting validation/test | Add all three pairwise checks plus raw-lineage checks. This is a missing guard; it does not prove the supplied generated split leaks. |
| A03 | `ReceiverState.process` infers receive time from sent time plus latency if absent | Require an independently observed receiver timestamp in real adapters. Never derive trusted arrival order from attacker-controlled time. |
| A04 | `latency_ms` and `signal_strength_dbm` are mandatory current inputs | Real datasets may lack them. Build explicit feature profiles/masks and retrain; do not invent nominal values to satisfy the old model. |
| A05 | `world.py` uses a single receiver state and annotates an RSU ID | RSU assignment is not radio delivery. Model each receiver’s visibility and state separately before claiming wireless realism. |
| A06 | Co-location rationale treats nearby identities as evidence of Sybil behavior | Multiple honest vehicles, motorcycles and uncertain positions can be close. Nearby aliases are a hypothesis, not physical proof; test pseudonym rotation and dispersed attackers. |
| A07 | The current motion bounds compare sender-reported speed and position | Jointly forged plausible trajectories can evade these checks. They are consistency residuals, not facts an attacker cannot fake. |
| A08 | `simple_blockchain.py` is a local file; whole-chain rewrites are explicitly outside its protection | Retain as baseline; add signed off-box commitments and compare an actual multi-party network. |
| A09 | Ledger append rewrites the file and has no multi-process locking | Replace the application evidence store with transactional persistence before concurrent service use. Atomic replace is not writer coordination. |
| A10 | Streamlit directly drives the simulation/pipeline; no service boundary/auth layer in reviewed code | Extract a headless runner and API before a complete GUI rebuild. |
| A11 | `joblib.load` accepts the selected model bundle | Production artifact ingestion needs trusted provenance, integrity verification and controlled promotion; untrusted serialized models must not enter the loader. |
| A12 | Threshold code calls an F1 tolerance “statistically indistinguishable” | It is an operational heuristic, not a significance test. Report the tolerance honestly and add grouped uncertainty estimates. |
| A13 | Evaluation is primarily per-message, with deliberately visible simulated attacks | Add event-level outcomes, long benign recordings, subtle attacks, missingness and external domains. |

The archive already documents several limitations: single-receiver visibility, no message authentication, missed widely spaced Sybil ghosts, no unknown-attack path, co-location false positives and expensive synchronous explanations. Preserve those disclosures.

## First corrective change set after this dossier

Fix A01/A02 and exact metric naming with narrow regression checks; establish a clean reproducible baseline; introduce a receiver-observation schema and profiles for unavailable fields. Do not compare new algorithms until the data/feature contracts and split audit are reliable.
