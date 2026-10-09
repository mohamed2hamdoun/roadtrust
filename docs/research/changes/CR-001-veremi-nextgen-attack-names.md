# CR-001: Add VeReMi NextGen attack names to the threat catalog

Status: applied · 9 October 2026 · Plan step 1.5 · Implements: ADR18 (correction)

## Finding and evidence

ADR18 recorded VeReMi NextGen's (D03) attack list as "to verify". While mapping fields for
step 1.5, the dataset's own documentation (`Documentation/README.md` in
`VeReMi-dataset/VeReMi-NextGen`, read from a sparse clone on 9 October 2026) listed 15
attack subsets: `constantPositionOffset`, `randomPositionOffset`, `positionMirroring`,
`constantSpeedOffset`, `randomSpeedOffset`, `zeroSpeedReport`, `suddenConstantSpeed`,
`reversedHeading`, `feignedBraking`, `accelerationMultiplication`, `timeDelayAttack`,
`dosAttack`, `trafficCongestionSybil`, `suddenStop`, `dataReplay`.

Five threats had no D03 coverage recorded although D03 contains a matching attack.

## What exactly changed

`docs/research/registries/threats.json` only:

| Threat | `dataset_ids` before → after | D03 attack names added to `note` |
|---|---|---|
| TH02 | D01, D02, D03 (unchanged) | constantPositionOffset, positionMirroring |
| TH03 | D02, D03 (unchanged) | randomPositionOffset |
| TH04 | D01, D02, D03 (unchanged) | constantSpeedOffset, randomSpeedOffset, zeroSpeedReport, suddenConstantSpeed, reversedHeading, feignedBraking, accelerationMultiplication |
| TH05 | D02 → D02, D03 | suddenStop |
| TH07 | D02 → D02, D03 | dataReplay |
| TH08 | D02 → D02, D03 | timeDelayAttack |
| TH10 | D01, D02 → D01, D02, D03 | dosAttack (message duplication) |
| TH11 | D01, D02 → D01, D02, D03 | trafficCongestionSybil |
| TH09, TH12 | unchanged | note: not in VeReMi NextGen |

No threat added or removed; coverage counts unchanged (18 dataset, 7 simulate, 1 gap).

## Why this option

The catalog is what P6 reports against; missing dataset links would hide that D03 can test
five more threats. Correcting the registry in place, with the source in each note, keeps
one catalog instead of a separate errata list.

## Pros

- Five threats gain a second, newer dataset for evaluation.
- Exact attack names make the P4 adapter mapping mechanical.
- `positionMirroring` and `reversedHeading` are now visible as distinct variants.

## Cons

- Names come from documentation, not from inspecting data files; a release could differ.
- Mapping `suddenStop` to TH05 "eventual stop" and `trafficCongestionSybil` to TH11 is a
  judgment of equivalence, not a confirmed identity of attack generators.
- ADR18's text still says the D03 list was unchecked; this record is the correction.

## Alternatives considered

| Alternative | Why not chosen | When it would be better |
|---|---|---|
| Wait for the data card in 4A.1 | Leaves known coverage unrecorded for weeks | If documentation and data were known to disagree |
| New threat entries per D03 attack | Duplicates threats that already describe the behaviour | If an attack has no matching threat |
| Rewrite ADR18 | Records should show what was known at decision time | Never; corrections go in CRs |

## How to retest

```bash
uv run python tools/research/validate_registry.py   # PASS; threats: 26
grep -c '"D03"' docs/research/registries/threats.json
```

In 4A.1, compare the attack folder names in the downloaded D03 release with the notes.

## How to change or revert

The commit that added this file is
`git log --diff-filter=A --format=%h -- docs/research/changes/CR-001-veremi-nextgen-attack-names.md`;
`git revert` it to restore the previous catalog. To change a mapping, edit the threat's
`dataset_ids` and `note` and record the reason in a new CR.
