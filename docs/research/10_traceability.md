# 10 — Traceability and decision control

## One evidence chain for every major choice

Requirement → source/review question → dataset/adapter → observable feature → experiment/run → observed limitation → decision record → implementation/test → release claim.

Example, not a completed result: R01/R04 → Q04 and S09/S23 → D03 alias/timing audit → F014 `sender_age_s` → E02/E07 pseudonym ablations → measured false incidents pending → retain/revise/remove decision pending. No link in this chain should imply that an unrun test has passed.

## Documents that change with the project

| Record | Required contents | Location |
|---|---|---|
| Literature note | Question, exact source/version, reading depth, method, limits, implication | `templates/literature_note.md` |
| Data card | Rights, provenance, fields, label semantics, time/space units, leakage, checksums | `templates/data_card.md` |
| Feature card | Formula, dependencies, trust, availability, rationale, ablation and decision | `registries/features.json` plus `templates/feature_card.md` |
| Experiment | Preregistered protocol, execution manifest, metrics, errors, observed limitations | `registries/experiments.json`, experiment templates |
| Technology decision | Requirement, alternatives, evidence, choice, consequences, reversal trigger | `registries/decisions.json`, `templates/decision_record.md` |
| Failure case | Conditions, observations, expected response, acceptance evidence | `registries/failure_cases.json` |
| Release claim | Exact claim, scope, code/data/run evidence, limitation and owner | `templates/release_claim.md` |

The validator checks unique IDs, reference integrity, existing feature coverage and the absence of fabricated results in planned experiments. It does not certify the research or application.

## Open decisions

| Decision | State | Evidence needed |
|---|---|---|
| First deployment target | Proposed: receiver-side lab/edge monitor | Operator and hardware confirmation |
| Primary external dataset | Pending D02/D03 sample audit | Rights, schema/alias observability and lineage |
| Model family and final feature set | Pending E02–E08 | Comparable runs under agreed budgets |
| Radio protocol and simulator | Pending E07/E10 | Target stack and compatible model |
| Blockchain implementation | Pending E09 | Participant governance and measured comparison |
| API/UI stack | Provisional Python API and separate web client | Contract spike, operator tasks and deployment budget |
| CAN and perception expansion | Optional later tracks | Capacity and a specific extra hypothesis |

## Decision standards

“Used because it was already in the hackathon” is an acceptable description of history, not a final justification. “Used because it won the benchmark” is incomplete without the benchmark scope and constraints. An honest decision may be “keep the simpler method because the measured improvement is too small for the additional cost.”

Record positive and negative results. Keep failed runs with a reason. Revisit a decision when the observation profile, workload, hardware, threat model, data domain, license or measured failure distribution changes. A new feature definition requires a schema version and retraining/revalidation; it must not silently reuse an incompatible model.

## Review limits and remaining work

This delivery is a substantial planning and evidence foundation. It does not complete full literature reviews of every automotive subsystem, acquire external datasets, compare algorithms on those datasets, implement a distributed ledger, integrate production simulators or rebuild the GUI. Those are explicit milestones with acceptance evidence. The next concrete engineering deliverable is the baseline correction plus one audited external-data adapter.
