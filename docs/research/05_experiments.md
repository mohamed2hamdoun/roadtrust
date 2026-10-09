# 05 — Algorithms, experiments and selection

**No expanded benchmark has run yet. No optimal algorithm has been selected.** Candidate strengths and risks below are hypotheses to test, not limitations already observed in RoadTrust experiments. Existing RF results remain an archived synthetic baseline.

## Compare methods in waves

| Candidate | Why include it | Failure hypothesis / measurement |
|---|---|---|
| Constant benign / frequency baseline | Exposes label imbalance and trivial benchmarks | Recall collapses; establish reference metric behavior |
| Explicit physical/rate rules | Interpretable low-cost baseline | Noise and changing density may cause many false alarms |
| Logistic regression | Simple statistical baseline | May miss interactions; measure calibration and nonlinear residual errors |
| Small decision tree | Inspectable nonlinear baseline | May be unstable or overfit thresholds; repeat grouped seeds |
| Current Random Forest | Existing implementation to beat | Domain shift, size and explanation latency may dominate |
| Extra Trees | Tests another randomized ensemble | More randomness may not improve held-out behavior |
| Histogram boosting / XGBoost | Tests boosted tabular models [S25] | Tuning cost and domain transfer may offset in-domain gains |
| Isolation Forest | Tests a mostly-benign anomaly-learning route | Normal rare behavior may dominate alerts |
| One-Class SVM | A second novelty baseline on bounded data | Scaling and sample size may make deployment impractical |
| Kalman-style innovation checks | Tests sequential motion consistency with explicit uncertainty | Wrong motion/noise model may mimic attacks |
| Autoencoder | Conditional candidate for richer normal patterns | May reconstruct attacks well; requires careful contamination handling |
| GRU / temporal convolution | Conditional candidate for time dependencies | Needs enough independent sequences; leakage, memory and lag risks |
| Graph model | Later only if receiver-visible relations justify it | Dynamic graphs, pseudonyms and cost may erase benefit |

Wave 1: rules, logistic regression, small tree, RF and one boosting implementation. Wave 2: novelty/temporal methods only after wave 1 reveals a gap. Wave 3: graph or fusion approaches only with a concrete unresolved hypothesis. Do not add algorithms solely to increase the comparison count.

## Freeze the evaluation protocol before tuning

1. Define the domain, detection unit, allowable observations and label semantics. CAN and V2X get different evaluations.
2. Group by original recording/base trajectory/scenario, drive, day and vehicle where feasible. Keep all receivers of the same transmitted event and all attack variants derived from a shared clean trajectory in one split. Hash duplicates and record the grouping manifest.
3. Respect official benchmark splits, then audit their dependence structure. If a separate stronger holdout is needed, name it clearly and report both protocols rather than quietly altering the benchmark.
4. Use training groups for fitting and grouped inner validation for model/feature selection. Reserve separate grouped calibration and threshold-selection data where possible, or use documented out-of-fold predictions. Keep the final test sealed.
5. Purge overlapping windows across boundaries; account for maximum state/history duration. Define cold-start versus permitted warm-up and prevent warm-up from using labels or future observations.
6. Give candidates the same declared compute/tuning budget and input visibility. For a first pass, propose up to 20 search configurations per tunable family and five training seeds; log early stopping, timeouts and algorithms that exceed the budget. Adjust these numbers before the run if compute requires it.
7. Freeze preprocessing, feature profile, hyperparameters, calibration, threshold and alert aggregation policy. Then evaluate final held-out groups once. Further tuning creates a new experiment and a new untouched confirmation set.
8. Save code commit, environment lock, data hashes, group manifest, feature schema, seeds, predictions, errors, timings and logs. MLflow [S31] can catalog these; it cannot enforce the protocol by itself.

Use separate manifests for known-attack tests, leave-one-family-out tests, cross-density/road tests, cross-dataset transfer and real benign-data robustness. An unseen family cannot be used to tune the supposedly unseen-attack detector.

## Measure the things the application pays for

| Dimension | Required metrics |
|---|---|
| Detection | Per-family precision/recall; average precision; confusion matrix; event recall; missed-event list |
| Operational noise | Raw FPR plus deduplicated false incidents per receiver-hour, with aggregation rules and exposure duration |
| Speed | Time-to-first-alert per event; missed events included separately; p50/p95/p99 stage and end-to-end latency |
| Resources | Sustained message throughput, queue depth, dropped observations, CPU, memory, model size and storage |
| Confidence | Reliability plot, Brier score and calibration error definition; results per domain/profile |
| Robustness | Missing fields, clock errors, noise, pseudonyms, congestion, subtle attacks, unknown families and drift |
| Explainability | Fidelity/additivity where applicable, stability under harmless perturbation, latency and operator task success |
| Uncertainty | Paired group-level bootstrap confidence intervals; state resampling unit and sample counts |

Do not bootstrap individual correlated messages as independent trials. For temporal recordings, use drive/session-level or appropriate block resampling. Report event and message metrics together; one long flooding burst must not silently dominate the research conclusion. Describe alert matching windows, cooldowns and duplicates before counting events.

A mathematical illustration: if sensitivity and false-positive rate were fixed, precision depends on prevalence as `TPR*p / (TPR*p + FPR*(1-p))`. Sweep plausible prevalences for sensitivity analysis; do not treat the synthetic 22.3% attack fraction as an operational estimate.

## Feature selection evidence

Run rules-only, motion-only, receiver-rate-only, identity/spatial-only, all observable features, and all-minus-one-group. Remove `latency_ms` and RSSI separately; challenge receiver identity/clock shortcuts; vary motion bounds and co-location radius; test aliases and stale neighbors. Use grouped validation permutation/ablation findings, not impurity importance alone. A correlated feature’s isolated importance is not its unique causal contribution.

For each retained feature record its change in event recall, false incidents/hour, resource cost and failures, with uncertainty. If performance does not justify availability or maintenance cost, remove it.

## Explanation protocol

Record which output is explained: raw ensemble score, calibrated probability or another decision function. Existing TreeSHAP additivity for the raw forest does not automatically explain a nonlinear calibration layer. Compare explanations across repeated runs and nearby benign perturbations. Use honest “explanation unavailable” states on timeout/failure. Any future LLM narrative should be constrained to recorded evidence and evaluated for unsupported statements; it is not a required core component.

## Selection rule — decided later from evidence

Before running final comparisons, agree a minimum event-recall target, maximum false incidents/hour, p99 latency, memory budget and operating conditions. **These budgets are currently unset.** First eliminate methods that fail the required gates. Compare the remaining methods on a Pareto frontier; prefer the simpler method when differences are small or uncertain. Publish every tested candidate’s observed failures, not only the winner’s score.

A decision record must state: chosen scope, eligible alternatives, run IDs, reasons, observed limitations, rejected alternatives and revisit conditions. “Optimal” means best among tested eligible candidates under this protocol, not universally optimal.

## Experiment register

`registries/experiments.json` defines E01–E13. Every record currently has `status: planned`, empty runs and no result. Use `templates/experiment.yaml` and `templates/experiment_report.md` for executions. Never convert expected risks into measured findings.
