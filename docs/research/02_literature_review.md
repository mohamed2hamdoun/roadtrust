# 02 — Literature review method and first synthesis

## Review questions

| ID | Question | Evidence to extract | Initial sources |
|---|---|---|---|
| Q01 | How does a physical measurement reach a receiver? | Device, bus/radio, message schema, units, timestamps and trust boundary | S01–S05 |
| Q02 | What survives WAN loss, radio impairment or a compromised sender? | Preconditions, local dependencies and failure behavior | S02, S11, S15, S19 |
| Q03 | Which data match each security question? | Real/simulated provenance, labels, available fields, split and rights | S06–S14 |
| Q04 | Which features remain observable and useful outside the generator? | Extraction, leakage, missingness, ablations and confounders | S03, S09–S11, S23 |
| Q05 | Which detectors meet the same operational target? | Tuning budget, event recall, false alarms, compute and external validity | S23, S25, S27–S29 |
| Q06 | What does an explanation establish? | Attribution target, fidelity, stability, human usefulness | S24 |
| Q07 | What additional trust does consensus provide? | Adversary, governance, finality, privacy and failure modes | S20–S22 |
| Q08 | Which simulator validates which phenomenon? | Mobility, radio, sensors, synchronization and model calibration | S15–S19 |

## A repeatable search protocol

1. Begin with standards bodies, dataset owners, original papers, official documentation and linked code. Secondary reviews can locate papers but should not be the sole evidence for a technical choice.
2. Use queries such as `(V2X OR VANET) misbehavior detection dataset pseudonym`, `vehicular intrusion detection cross dataset evaluation`, `CAN IDS real attacks dataset`, `PC5 out of coverage security`, and `permissioned blockchain offline evidence consensus`.
3. Search by subquestion; retain the exact query, search date, source, version and inclusion decision. This initial search used targeted web queries and official-page retrieval; it is not exhaustive database searching.
4. Include sources with an identifiable task, mechanism or dataset and usable experimental details. Record paywalls/unavailable full text. Exclude duplicate versions, unsupported marketing comparisons and results whose task does not match the proposed claim.
5. Deduplicate by DOI/title/version. Follow references backward and citations forward from relevant original papers. Check newer standard editions separately from historical experimental versions.
6. Read methods and limitations before copying a headline metric. Capture threat assumptions, attacker knowledge, grouping unit, class prevalence, observation access, tuning budget, hardware and code/data availability.
7. Mark each source as screened, relevant sections read, fully reviewed or reproduced. A second reviewer is useful when available; no second review has occurred here.
8. Finish each subreview with a decision implication and an unresolved experiment, not a list of paper summaries.

Use `templates/literature_note.md`. Store short paraphrases and exact page/section references. Do not copy whole papers into the project documentation. The source registry lists 31 references, including standards and software documentation; it is **not 31 completed paper reviews**.

## Synthesis that changes the engineering plan

**Communication domain comes first.** A CAN frame, a cooperative-awareness report and a cloud request are different observations. Therefore, adapters and claims must remain domain-specific. A binary detector trained on current synthetic V2X features cannot simply accept arbitrary CAN bytes.

**Authenticity and plausibility answer different questions.** Authentication may establish that a credential signed a message. A valid credential can still report false telemetry. Conversely, an unusual trajectory can be honest. Keep cryptographic checks, data-quality checks and statistical alerts separate in the incident record.

**A public benchmark improves reproducibility, not automatically realism.** The VeReMi family is relevant simulated V2X data. Real driving telemetry and real radio measurements provide complementary realism but may not supply attack truth for the same task. Test performance on each supported task separately and label any attack overlays.

**Deployment evidence must measure the operational cost of errors.** Security-ML evaluation pitfalls motivate grouped holdouts, realistic negative traffic, careful feature access and explicit base rates [S23]. Comparing accuracy on differently sampled papers is not model selection.

**Explanation is an audit aid.** SHAP attributes a model output [S24]. A convincing narrative cannot repair wrong inputs, a mismatched domain or a weak detector. Record explanation method, output scale and failures.

**Consensus has a trust model.** Fabric and Besu offer different implementation choices [S20–S22]. RoadTrust must first name the independent organizations, acceptable faults and evidence access rules. A blockchain cannot make a fabricated sensor report true.

**Simulation fidelity is task-specific.** Mobility/network co-simulation and sensor-rich driving simulation cover different questions [S15–S19]. More visual realism alone does not validate V2X timing or attack detection.

## What the deeper reviews must add

Full-paper extraction and reproduction remain pending for detection approaches, Sybil detection under privacy rotation, RF/radio uncertainty, offline credential revocation, robust time handling and blockchain audit semantics. Establish exact claims with evidence before selecting any of these as production mechanisms. Do not backfill a literature justification after choosing a fashionable tool.

## Completion criterion for a technology decision

A decision is ready when its requirement is explicit, alternatives have been compared, evidence matches the actual task, local experiments cover its main failure modes, and residual limitations are recorded. If the evidence is weak, write “provisional” and define a test or revisit trigger.
