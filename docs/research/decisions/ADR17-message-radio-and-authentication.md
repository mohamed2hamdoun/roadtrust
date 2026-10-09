# ADR17: ETSI C-ITS messages first, 802.11p/ITS-G5 radio first, authentication checked separately from ML

Status: accepted · 9 October 2026 · Decided by: Mohamed Hamdoun · Plan step 1.2

## Decision

**Messages.** The first message profile is ETSI C-ITS: the Cooperative Awareness Message
(CAM, ETSI EN 302 637-2; v1.4.1 is the reviewed reference, source S03). DENM and CPM are
later additions. The detection core stays format-neutral: each format enters through its
own adapter into the receiver-observation format (P3). A SAE J2735 BSM adapter is planned
after the ETSI path works end to end. The exact CAM release to implement is fixed during
literature topic T3, after checking ETSI's current publications.

**Radio.** Simulation and the lab bench model IEEE 802.11p / ETSI ITS-G5 first. The
detector does not depend on the radio: radio measurements (RSSI, channel load) are
optional fields with explicit "not available" values. LTE-V2X PC5 and NR-V2X sidelink are
added later through a dedicated simulator spike (ns-3 / 5G-LENA, source S19).

**Authentication.** RoadTrust verifies message security where the data carries it, using
the ETSI TS 103 097 format (source S04; edition fixed during topic T4). Each observation
gets an authentication result, recorded **next to** the ML score and never merged into it:

`valid` · `invalid_signature` · `unknown_issuer` · `expired` · `revoked` · `unsigned` ·
`not_available`

A `valid` result means a credentialed sender signed the message. It does not mean the
content is true: a credentialed insider can still send false data, which is what the ML
and plausibility checks are for. Revocation freshness (how old the revocation list is) is
recorded with the result, so offline operation is visible.

## Why

- **ETSI first** lines up the three things the plan depends on: the candidate main
  benchmark (VeReMi NextGen provides CAM logs, source S08), the most complete open ETSI
  simulation stack (Artery with Vanetza, on Veins/OMNeT++), and the reviewed standards
  (S03, S04).
- **802.11p first** because the open simulators model it most completely; cellular V2X
  tooling is thinner and research-branch based.
- **Separate authentication** because "who signed it" and "is it plausible" are different
  questions (dossier chapter 02). Keeping them apart is what lets RoadTrust tell an
  outsider attack (fails authentication) from an insider attack (passes authentication,
  fails plausibility).

## Pros

- Datasets, simulator and standards agree on one message format from the start.
- The radio-neutral core can take cellular V2X later without redesign.
- Incident records show both authentication and behaviour evidence, so operators can see
  which attacker type they face.
- Explicit `not_available` keeps unsigned datasets usable without pretending they were
  verified.

## Cons

- **Public datasets carry no signatures.** VeReMi-style logs will all be
  `not_available`; the authentication path can only be exercised with simulated signed
  traffic (Artery/Vanetza) or standard test vectors.
- US-style deployments (BSM, IEEE 1609.2) wait for a second adapter and checker.
- Cellular V2X behaviour (scheduling, sidelink resource allocation) is not modelled until
  the later spike, so congestion/DoS results apply to 802.11p only.
- Implementing TS 103 097 verification correctly is non-trivial; the Python library or
  service to use is not yet chosen (decided in P3/P8, with its own record).
- The newest ETSI editions (CAM release, TS 103 097 2026 edition) still need checking.

## Alternatives considered

| Alternative | Why not chosen | When it would be better |
|---|---|---|
| SAE/IEEE (BSM, 1609.2) first | Weaker fit with the main candidate benchmark and full-stack simulator | Target deployment in North America |
| Both families from the start | Doubles adapters and security checks in every phase | Once the ETSI path is complete |
| LTE-V2X PC5 first | Thinner, older open simulator support | If a partner's lab hardware is C-V2X |
| NR-V2X sidelink first | Least mature tooling, little real data | Research focused on 5G sidelink specifically |
| Plausibility only, no authentication | Cannot separate outsider from insider attacks | If no signed data can ever be obtained |
| Fold authentication into an ML feature | Hides whether an alert came from cryptography or behaviour | Never; it would blur evidence |

## How to retest

Scope decision; later artifacts must show it:

- P3: schema has the seven authentication values plus revocation freshness, and radio
  fields that can be "not available"; tests cover both.
- P4A: VeReMi adapters emit `not_available` for authentication, never `valid`.
- P4C: Artery traces include signed messages with at least one invalid-signature case.
- P6: results are reported for outsider and insider attack groups separately.

## How to change or revert

Switching to BSM-first means writing the BSM adapter before the CAM adapter and updating
topic T3/T4 priorities; the core is unaffected. Undo with `git revert` on the commit that
added this file.

## Revisit trigger

A deployment partner in a BSM/1609.2 region; lab hardware that is C-V2X only; or no way to
obtain signed traffic for testing.
