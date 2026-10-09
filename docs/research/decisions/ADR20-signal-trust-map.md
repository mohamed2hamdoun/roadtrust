# ADR20: Every observable field carries a trust label; simulator truth and outputs can never be inputs

Status: accepted · 9 October 2026 · Decided by: Mohamed Hamdoun (paths, depth, CAM
release); labelling rules proposed by Claude · Plan step 1.5

## Decision

- Four signal paths are mapped field by field in `registries/signal_fields.json`:
  sender CAM, receiver, OBU ego sensors and evidence, plus every column of VeReMi NextGen
  (dataset D03). Explanation: [chapter 13](../13_signal_trust_map.md).
- **CAM coverage:** every Release 1 field (EN 302 637-2 v1.4.1 with TS 102 894-2 v1.3.1),
  with Release 2 additions (TS 103 900 v2.3.1 with TS 102 894-2 v2.4.1) flagged `R2`.
- **Labels:** trust ∈ {claimed, measured, measured_local, derived, verified, oracle,
  metadata, output}; use ∈ {allowed, caution, key_only, forbidden}.
- **Enforced rule:** a field labelled `oracle` or `output` must be `forbidden`. The
  validator fails otherwise (shown by marking `sender_id` allowed: build fails).
- **Timing rule:** time features use only what a real CAM carries (`generationDeltaTime`,
  65.536 s wraparound) plus the receiver's own clock, even when a dataset offers more.
- Feature code in P5 must take its inputs from fields labelled `allowed`, `caution` or
  `key_only`, and record which ones it uses on its feature card.

## Why

The hackathon audit found detector inputs that a real receiver could not trust or would
not have: arrival time inferred from the sender's timestamp (A03), mandatory RSSI (A04),
and sender-controlled residuals treated as facts (A07). Labelling every field once, at the
source, prevents each of these by construction. The field review also found two new traps
in the candidate main dataset: full-precision send times and `*_noise` fields that hold
the true injected error.

## Pros

- Leakage of simulator truth into features becomes a build failure, not a review comment.
- Datasets, simulators and real CAMs map onto one vocabulary.
- Release 2 support is planned without blocking Release 1 hardware.
- The map doubles as the source for the GUI Feature Inspector (P9).

## Cons

- Labels are judgments; `caution` covers 34 fields whose usefulness depends on context
  and must be argued per feature.
- The map covers CAM only; DENM, CPM and BSM need their own entries when added.
- Two dataset facts (heading convention, meaning of `*_noise`) are still unverified on
  real data samples.
- The validator checks label consistency, not that P5 code actually respects the labels;
  that check arrives with the feature code.

## Alternatives considered

| Alternative | Why not chosen | When it would be better |
|---|---|---|
| Main fields only now, rest in P3 | Owner chose full depth; traps were found in "minor" fields | If time is short |
| Diagram only | No field-level enforcement possible | Presentations |
| Release 2 only | Lab hardware may speak only Release 1 | Once all target hardware supports Release 2 |
| Release 1 only | Misses six Release 2 extension containers | Strictly Release 1 deployments |
| Trust labels without an enforced rule | Leakage would rely on reviewers noticing | Never |

## How to retest

```bash
uv run python tools/research/validate_registry.py   # "signal_fields": 86, status PASS
```

Negative check: set any `oracle` row's `feature_use` to `allowed` in a copy of the
registry; the validator fails with `signal_fields/<id>: oracle usable`.

## How to change or revert

Relabel a field in `registries/signal_fields.json` with a reason in its `note`. Change the
vocabularies or the rule in the `TRUST`/`USE` block of the validator together with this
record. Undo with `git revert` on the commit that added this file.

## Revisit trigger

A new message type (DENM, CPM, BSM) or dataset is added; a data sample contradicts a
label; lab hardware reveals a different CAM release.
