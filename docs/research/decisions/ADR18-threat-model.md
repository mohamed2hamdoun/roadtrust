# ADR18: Threat model — four attacker types, four attack families, physical threats and benign look-alikes

Status: accepted · 9 October 2026 · Decided by: Mohamed Hamdoun · Plan step 1.3

## Decision

The threat catalog is the machine-checked registry `registries/threats.json`: 18 threats
(`TH01`–`TH18`) and 8 benign look-alikes (`BN01`–`BN08`). Each entry records attacker
type, the layer expected to catch it, affected profiles (`rsu`/`obu`), data sources and a
coverage status.

**Attacker types in scope**

| Code | Attacker | Caught mainly by |
|---|---|---|
| `OUT` | Outsider without valid credentials | Authentication check (ADR17) |
| `INS` | Insider with valid credentials (malicious or compromised vehicle) | Plausibility checks and ML |
| `RSU` | Compromised roadside unit (false reports, altered or suppressed logs) | Multi-receiver cross-checks, evidence integrity (P7) |
| `SENS` | Attack on the receiver's own sensors (GNSS spoofing, tampering) | Ego-data consistency checks (OBU, ADR16) |
| `ENV` | No attacker: benign situations that resemble attacks | Must not alert |

**Attack families:** data falsification (position, speed, acceleration, heading,
eventual stop), replay and delay, flooding/denial of service, Sybil and pseudonym abuse.
**Physical threats:** radio jamming (reported as degraded reception, never attributed to
a sender) and GNSS spoofing/loss (of senders or of the receiver).
**Benign look-alikes:** hard braking, GNSS outage/multipath, congestion, pseudonym
rotation, GNSS noise, stopped vehicles, late joiners, close following.

**Attacker knowledge:** benchmark on standard, non-adaptive attacks first; then test
adaptive attackers who craft physically consistent false trajectories (`TH06`) in the
P6 robustness stage.

**Coverage at decision time:**

| Coverage | Count | Meaning |
|---|---|---|
| `dataset` | 18 | A candidate dataset contains it (attack names to confirm on data cards) |
| `simulate` | 7 | Must be generated in simulation (P4C) |
| `gap` | 1 | `TH18` receiver sensor tampering: no source yet; candidate for P4B bench recording |

## Why

Detection can only be claimed for threats that were defined and tested. Naming the
attacker separates what cryptography handles (outsiders) from what behaviour analysis
handles (insiders), which ADR17 made possible. Listing benign look-alikes as first-class
entries forces false-alarm measurement on the situations most likely to cause them. The
coverage column turns "we don't have data for that" into a visible, tracked gap instead of
a silent omission.

## Pros

- Every later benchmark result can be read per threat, per attacker type and per profile.
- Gaps are visible before any model is trained.
- Benign look-alikes guard against a detector that flags every hard brake or tunnel.
- The adaptive attacker test prevents overstating protection.

## Cons

- Large scope: seven threats need simulation work before they can be evaluated.
- VeReMi attack names are taken from its documentation and must be confirmed against the
  actual data (4A.1); VeReMi NextGen's attack list is not yet checked.
- Jamming and GNSS spoofing need simulator models whose realism must itself be validated
  (E10).
- The compromised-RSU threat depends on the evidence system (P7) and multi-receiver
  scenarios, so it is tested late.
- An adaptive attacker can always be made stronger; the robustness test bounds one
  attacker strategy, not all.

## Alternatives considered

| Alternative | Why not chosen | When it would be better |
|---|---|---|
| Keep the hackathon's three families | Misses replay, delay, physical and infrastructure threats | Quick demo only |
| Only threats present in datasets | Hides gaps; omits outsider and RSU attacks entirely | If simulation work must be cut |
| Insider only | Ignores what authentication can catch and the RSU/evidence threat | Pure ML research question |
| Non-adaptive attackers only | Overstates real protection | Never for a deployment claim |
| Adaptive from the start | Much harder data generation before any baseline exists | After the non-adaptive benchmark is complete |
| Use an external taxonomy as-is (e.g. a standard's misbehaviour list) | Not yet reviewed (topic T4); may not cover receiver-sensor threats | After T4, map entries to it as an extra field |

## How to retest

```bash
uv run python tools/research/validate_registry.py   # "threats": 26, status PASS
```

The validator checks unique IDs, allowed attacker/profile/coverage values, and that every
`dataset` entry names an existing dataset. Later, each P6 report must include one row per
threat in scope.

## How to change or revert

Add, remove or reclassify entries in `registries/threats.json` and record why. Change the
allowed vocabularies in `THREAT_VOCAB` in the validator together with this record. Undo
with `git revert` on the commit that added this file.

## Revisit trigger

Data cards contradict the assumed attack names; literature topics T4/T6 reveal a missing
threat class; a gap entry gets a data source; or a new deployment profile is added.
