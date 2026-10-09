# Primary-source register

Checked 9 October 2026. This is a targeted scoping review, not a completed systematic review. Reading depth is explicit; an abstract screening never counts as a replicated result. Standards editions are reference points, not claims of current certification. No external dataset has been downloaded or accepted into training in this work.

## S01 — Linux Kernel — SocketCAN

[Linux Kernel — SocketCAN](https://docs.kernel.org/networking/can.html)

- Type / reading depth: official documentation; Relevant documentation inspected.
- Finding: Linux exposes CAN interfaces through its networking API, including virtual interfaces.
- Implication / boundary: CAN adapter design; virtual CAN cannot validate electrical or arbitration behavior.

## S02 — 3GPP TS 23.287 v16.6.0 / ETSI TS 123 287

[3GPP TS 23.287 v16.6.0 / ETSI TS 123 287](https://www.etsi.org/deliver/etsi_ts/123200_123299/123287/16.06.00_60/ts_123287v160600p.pdf)

- Type / reading depth: standard, Release 16; Relevant architecture and coverage clauses inspected.
- Finding: Distinguishes PC5 direct communications from network-based V2X and specifies provisioning constraints.
- Implication / boundary: Use for link/failure taxonomy; historical edition, not a claim of current regional compliance.

## S03 — ETSI EN 302 637-2 v1.4.1 — Cooperative Awareness

[ETSI EN 302 637-2 v1.4.1 — Cooperative Awareness](https://www.etsi.org/deliver/etsi_en/302600_302699/30263702/01.04.01_60/en_30263702v010401p.pdf)

- Type / reading depth: standard, 2019; Relevant message/heading clauses inspected.
- Finding: Defines CAM fields and message behavior; heading uses true north.
- Implication / boundary: A decoder must preserve units, unavailable codes and coordinate conventions; freeze the required profile.

## S04 — ETSI TS 103 097 v2.1.1 — Security header and certificates

[ETSI TS 103 097 v2.1.1 — Security header and certificates](https://www.etsi.org/deliver/etsi_ts/103000_103099/103097/02.01.01_60/ts_103097v020101p.pdf)

- Type / reading depth: standard, 2021; Search screening only; full review pending.
- Finding: Security headers and certificate formats are a separate layer from detecting misleading telemetry.
- Implication / boundary: A newer 2026 edition appeared in the ETSI publication listing; verify the target edition before implementation.

## S05 — AUTOSAR R24-11 — Requirements on Secure Onboard Communication

[AUTOSAR R24-11 — Requirements on Secure Onboard Communication](https://www.autosar.org/fileadmin/standards/R24-11/CP/AUTOSAR_CP_RS_SecureOnboardCommunication.pdf)

- Type / reading depth: official standard requirements; Search screening only; full text fetch unavailable.
- Finding: SecOC is relevant to authenticated, fresh in-vehicle messages.
- Implication / boundary: Candidate reference for the separate CAN track; not evidence of implementation or conformance.

## S06 — van der Heijden et al. — VeReMi (2018)

[van der Heijden et al. — VeReMi (2018)](https://arxiv.org/abs/1804.06701)

- Type / reading depth: research paper; Abstract and official family overview screened.
- Finding: Introduces reproducible simulated misbehavior data for comparable evaluation.
- Implication / boundary: Historical benchmark and backward citation starting point; full paper extraction pending.

## S07 — VeReMi Extension (2020) — official dataset overview

[VeReMi Extension (2020) — official dataset overview](https://veremi-dataset.github.io/veremi-extension)

- Type / reading depth: dataset owner documentation; Documentation inspected.
- Finding: Adds simulated sensor errors and more misbehavior variants to the original benchmark.
- Implication / boundary: Candidate external benchmark; do not describe it as field-recorded attack traffic.

## S08 — VeReMi NextGen (2026) — official overview

[VeReMi NextGen (2026) — official overview](https://veremi-dataset.github.io/veremi-nextgen)

- Type / reading depth: dataset owner documentation; Documentation inspected.
- Finding: Provides simulated CAM logs, official splits, pseudonyms and a newer scenario setup. Attacks are applied after baseline simulation.
- Implication / boundary: Candidate main benchmark; offline injected DoS does not by itself demonstrate live channel disruption.

## S09 — VeReMi NextGen — message format

[VeReMi NextGen — message format](https://github.com/VeReMi-dataset/VeReMi-NextGen/blob/main/Documentation/README.md)

- Type / reading depth: dataset owner schema; Relevant schema inspected.
- Finding: Documents rcvTime/sendTime in nanoseconds, sender_alias, sender_id and sender/receiver measurements.
- Implication / boundary: Use receiver-visible pseudonyms; block hidden identity, labels, driver profiles and oracle metadata from model inputs.

## S10 — nuScenes — CAN bus expansion

[nuScenes — CAN bus expansion](https://github.com/nutonomy/nuscenes-devkit/blob/master/python-sdk/nuscenes/can_bus/README.md)

- Type / reading depth: dataset owner documentation; Relevant fields/units inspected.
- Finding: Real scene telemetry includes timestamped pose, IMU, steering and vehicle-monitor measurements; documentation calls this expansion experimental.
- Implication / boundary: Use for benign motion realism, not as a ready-made labelled V2X cyberattack benchmark.

## S11 — Fraunhofer HHI — BerlinV2X

[Fraunhofer HHI — BerlinV2X](https://github.com/fraunhoferhhi/BerlinV2X)

- Type / reading depth: dataset owner documentation; Measurement table inspected.
- Finding: Real cellular/sidelink radio measurements and GPS tracks are available.
- Implication / boundary: Use for benign communication impairment characterization; exact timing semantics and attack-label availability require a sample audit.

## S12 — ORNL — A comprehensive guide to CAN IDS data and ROAD

[ORNL — A comprehensive guide to CAN IDS data and ROAD](https://www.ornl.gov/publications/a-comprehensive-guide-to-can-ids-data-and-introduction-of-the-road-dataset/)

- Type / reading depth: primary research publication page; Abstract inspected.
- Finding: ROAD combines real vehicle CAN captures and attacks with simulated masquerade cases, from one vehicle.
- Implication / boundary: Evaluate CAN separately; real data and real attacks are different labels.

## S13 — ROAD dataset release

[ROAD dataset release](https://zenodo.org/records/10462796)

- Type / reading depth: author dataset release; Release description screened.
- Finding: Release includes ambient and attack captures and points to the associated paper.
- Implication / boundary: Pin files, license, checksums and attack provenance before use.

## S14 — AIR-THU — DAIR-V2X / V2X-Seq

[AIR-THU — DAIR-V2X / V2X-Seq](https://github.com/AIR-THU/DAIR-V2X)

- Type / reading depth: dataset owner documentation; Overview inspected.
- Finding: Real cooperative perception and trajectory resources are provided.
- Implication / boundary: Optional perception track; image/point-cloud labels are not message-attack labels.

## S15 — Veins — framework and founding paper link

[Veins — framework and founding paper link](https://veins.car2x.org/)

- Type / reading depth: official project documentation; Architecture description inspected.
- Finding: Couples OMNeT++ communication models with SUMO mobility.
- Implication / boundary: Candidate network-first simulator; validate the selected radio model rather than assuming PC5 support.

## S16 — CARLA — SUMO co-simulation

[CARLA — SUMO co-simulation](https://carla.readthedocs.io/en/latest/adv_sumo/)

- Type / reading depth: official documentation; Co-simulation workflow inspected.
- Finding: Provides a documented CARLA/SUMO synchronization workflow.
- Implication / boundary: Useful for sensor/driving scenarios; extra radio integration still needs engineering.

## S17 — CARLA — packaged quick start

[CARLA — packaged quick start](https://carla.readthedocs.io/en/latest/start_quickstart/)

- Type / reading depth: official documentation; Platform requirements inspected.
- Finding: The inspected package guide lists Windows/Ubuntu and recommends a dedicated GPU.
- Implication / boundary: Do not assume the user’s Apple Silicon Mac can run the chosen package natively; verify a lab host and exact release first.

## S18 — Eclipse MOSAIC

[Eclipse MOSAIC](https://eclipse.dev/mosaic/)

- Type / reading depth: official project documentation; Coupling overview inspected.
- Finding: A framework for coupling mobility, application and communication simulators.
- Implication / boundary: Candidate when reproducing NextGen; coupling support does not mean every version combination works.

## S19 — CTTC — 5G-LENA

[CTTC — 5G-LENA](https://5g-lena.cttc.es/)

- Type / reading depth: official project documentation; Overview inspected.
- Finding: An ns-3-based 5G NR simulation project with related NR-V2X work.
- Implication / boundary: A PC5 study must verify a compatible sidelink branch/module and its model assumptions; generic NR support is insufficient.

## S20 — Hyperledger Fabric — Ordering service

[Hyperledger Fabric — Ordering service](https://hyperledger-fabric.readthedocs.io/en/latest/orderer/ordering_service.html)

- Type / reading depth: official documentation; Consensus/commit sections inspected.
- Finding: Documents crash-tolerant Raft and BFT ordering introduced in Fabric v3.0, and the need to check peer commit validity.
- Implication / boundary: Select according to the adversary model; receipt acknowledgement is not committed evidence.

## S21 — Hyperledger Fabric — Private data

[Hyperledger Fabric — Private data](https://hyperledger-fabric.readthedocs.io/en/latest/private-data/private-data.html)

- Type / reading depth: official documentation; Private collection overview inspected.
- Finding: Collections restrict which organizations hold private application data.
- Implication / boundary: Candidate privacy mechanism, not automatic protection for all metadata or traffic.

## S22 — Besu — QBFT

[Besu — QBFT](https://docs.besu-eth.org/private-networks/how-to/configure/consensus/qbft)

- Type / reading depth: official documentation; Validator/quorum sections inspected.
- Finding: Permissioned validators finalize blocks using QBFT; insufficient participating validators stall progress.
- Implication / boundary: Candidate EVM network; test loss of quorum, governance and separate administrative control.

## S23 — Arp et al. — Dos and Don’ts of ML in Computer Security (USENIX Security 2022)

[Arp et al. — Dos and Don’ts of ML in Computer Security (USENIX Security 2022)](https://www.usenix.org/conference/usenixsecurity22/presentation/arp)

- Type / reading depth: research paper; Abstract and relevant full-text evaluation pitfalls inspected.
- Finding: Highlights biased collection, leakage, weak metrics and unrealistic threat models in security ML.
- Implication / boundary: Guides grouped splits, fair tuning, base-rate analysis and deployment-oriented validation.

## S24 — Lundberg & Lee — A Unified Approach to Interpreting Model Predictions (2017)

[Lundberg & Lee — A Unified Approach to Interpreting Model Predictions (2017)](https://proceedings.neurips.cc/paper/2017/hash/8a20a8621978632d76c43dfd28b67767-Abstract.html)

- Type / reading depth: research paper; Abstract screened.
- Finding: Introduces SHAP as additive attribution of model outputs.
- Implication / boundary: Explain the model’s reasoning; do not interpret attribution as causal proof of an attack.

## S25 — Chen & Guestrin — XGBoost (2016)

[Chen & Guestrin — XGBoost (2016)](https://arxiv.org/abs/1603.02754)

- Type / reading depth: research paper; Abstract screened.
- Finding: Describes a scalable tree-boosting system.
- Implication / boundary: Motivates a candidate; it does not establish superiority on RoadTrust’s data.

## S26 — Guo et al. — On Calibration of Modern Neural Networks (2017)

[Guo et al. — On Calibration of Modern Neural Networks (2017)](https://arxiv.org/abs/1706.04599)

- Type / reading depth: research paper; Abstract screened.
- Finding: Studies confidence calibration and post-processing for neural models.
- Implication / boundary: Calibration background; reported neural results are not direct evidence for calibrating this forest.

## S27 — scikit-learn — Probability calibration

[scikit-learn — Probability calibration](https://scikit-learn.org/stable/modules/calibration.html)

- Type / reading depth: official documentation; Reference page opened; detailed method review pending.
- Finding: Reference for probability-calibration workflows.
- Implication / boundary: Fit calibration without touching the final test set; verify methods against the pinned version.

## S28 — scikit-learn — Cross-validation

[scikit-learn — Cross-validation](https://scikit-learn.org/stable/modules/cross_validation.html)

- Type / reading depth: official documentation; Reference page opened; detailed splitter review pending.
- Finding: Reference for grouped and temporal model evaluation.
- Implication / boundary: Implement grouping from the actual recording lineage, not merely a random row split.

## S29 — scikit-learn — RandomForestClassifier.predict_proba

[scikit-learn — RandomForestClassifier.predict_proba](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)

- Type / reading depth: official documentation; Exact predict_proba definition inspected.
- Finding: A forest score averages tree class probabilities; it need not equal the fraction of hard tree votes.
- Implication / boundary: Correct existing score descriptions; retain the uncalibrated-score warning.

## S30 — FastAPI — Features

[FastAPI — Features](https://fastapi.tiangolo.com/features/)

- Type / reading depth: official documentation; Schema/API sections inspected.
- Finding: Supports API schemas and validation around Python services.
- Implication / boundary: Proposed backend wrapper around the existing pipeline; authentication policy still needs implementation.

## S31 — MLflow — Experiment tracking

[MLflow — Experiment tracking](https://mlflow.org/docs/latest/ml/tracking/)

- Type / reading depth: official documentation; Run tracking sections inspected.
- Finding: Records parameters, versions, metrics and artifacts.
- Implication / boundary: Proposed run catalog; data lineage and split integrity still require project code.
