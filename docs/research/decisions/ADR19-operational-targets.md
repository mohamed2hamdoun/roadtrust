# ADR19: Operational targets — provisional false-alarm and detection targets, fixed latency targets

Status: accepted · 9 October 2026 · Decided by: Mohamed Hamdoun (targets TG01–TG05,
approach); TG06–TG07 proposed by Claude · Plan step 1.4

## Decision

Targets live in `registries/targets.json`. The P6 benchmark reads them; a model that
misses an `accepted` target is ineligible, and `provisional` targets are confirmed or
changed by the owner in P6 while looking at the measured trade-off curves.

| ID | Target | Profiles | Status |
|---|---|---|---|
| TG01 | ≤ 0.125 false incidents per receiver-hour (≤ 1 per 8-hour shift) | rsu, obu reports | provisional |
| TG02 | ≤ 0.001 false driver warnings per driving-hour (≤ 1 per 1,000 h) | obu | provisional |
| TG03 | ≥ 90 % of attack events detected, per attack family | rsu, obu | provisional |
| TG04 | Per-message detection latency p99 ≤ 100 ms | rsu, obu | accepted |
| TG05 | Attack start to first alert, p95 over detected events ≤ 1 s | rsu, obu | accepted |
| TG06 | ≥ 2,000 messages/s sustained, no drops | rsu | provisional (Claude) |
| TG07 | ≥ 1,000 messages/s sustained, no drops; memory/CPU budget set with OBU hardware | obu | provisional (Claude) |

**Definitions**

- *False incident:* an alert about benign traffic, after grouping repeated flags about the
  same sender and time window into one incident (grouping rule fixed in the P6 protocol).
- *Attack event:* one continuous attack episode. Detected if at least one alert falls
  inside it. Counted per family so one family cannot hide behind an average.
- *Latency* excludes explanation and evidence/blockchain work, which are asynchronous.

**Proving a false-alarm target.** Zero false alarms in *n* benign hours bounds the rate
below about 3/*n* per hour at 95 % confidence ("rule of three"). TG01 therefore needs
about 24 benign hours per receiver; TG02 needs about 3,000 benign driving hours, which in
practice means simulated traffic plus whatever real driving data exists.

## Why

Per-message percentages hide the operational cost. The hackathon's 0.99 % false-positive
rate per normal message would mean about 17,800 false flags an hour at an RSU hearing
50 vehicles at 10 messages per second. Targets stated per receiver-hour and per attack
event describe what an operator or driver actually experiences.

The owner chose provisional values for false alarms and detection rate because the right
trade-off can only be judged against measured curves (consistent with the original plan
to choose the algorithm after testing). Latency targets were fixed directly: CAMs arrive
at up to 10 Hz per vehicle, so a p99 of 100 ms keeps pace, and a 1-second alert is about
one beacon interval to a few.

## Pros

- Eligibility in P6 is decided by declared numbers, not by whichever model looks best.
- Targets are phrased in units people experience (per shift, per driving year).
- The driver target is far stricter than the operator target, reflecting the
  distraction risk recorded in ADR16.
- Provisional status keeps the final choice evidence-based.

## Cons

- TG02 requires thousands of benign hours; real data will not reach that, so the claim
  will rest mostly on simulation, whose realism must itself be shown (E10).
- Event and incident grouping rules strongly affect the numbers and are not fixed yet.
- TG06/TG07 throughput values are estimates (about 200 vehicles at 10 Hz for an RSU),
  not derived from a real site or device.
- Provisional targets can drift toward whatever the best model achieves; P6 must record
  any change with its reason.

## Alternatives considered

| Alternative | Why not chosen | When it would be better |
|---|---|---|
| Per-message false-positive rate | Hides operational load (17,800/h example) | Only as a secondary diagnostic |
| Fix all targets as final now | Owner preferred to decide with trade-off curves | Once P6 curves exist |
| Looser operator target (1 per hour) | Alert fatigue with many receivers | Research-only use |
| Stricter driver target (1 per 10,000 h) | ~30,000 benign hours to prove | Product certification |
| Recall 95 % or 80 % | 90 % pushes past the old Sybil result without dominating the false-alarm trade-off | Re-evaluate in P6 |
| Latency p99 50 ms or 500 ms | 100 ms matches the 10 Hz message rate | Tighter if OBU hardware is fast; looser if operator-only |

## How to retest

```bash
uv run python tools/research/validate_registry.py   # "targets": 7, status PASS
```

The validator checks operators, numeric values, profiles and status. In P6 every report
must show each target as met, missed or not measurable, with confidence bounds.

## How to change or revert

Edit the value or status in `registries/targets.json` and record the reason (a CR, or a
new ADR if the approach changes). Undo with `git revert` on the commit that added this
file.

## Revisit trigger

P6 trade-off curves are available (confirm provisional targets); OBU or RSU hardware is
chosen (set TG06/TG07 and memory/CPU); a real deployment site gives traffic volumes; or
operator usability tests (E13) show a different tolerable alert rate.
