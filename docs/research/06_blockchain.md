# 06 — From local hash chain to a real blockchain

## What changes

The current ledger provides local tamper evidence for a particular stored history. An attacker able to replace the file and recompute every hash can produce another locally valid history. A real blockchain adds a protocol under which multiple nodes validate and agree on the committed record. Its benefit depends on the independence, governance and compromise assumptions of those nodes.

The user’s requested real-blockchain track remains in scope. A signed, externally anchored log is also a required comparator so the study can show exactly what consensus adds.

## Candidate comparison

| Option | Why evaluate it | Main unresolved limitation | Experiment |
|---|---|---|---|
| Existing local chain | Historical baseline, simplest implementation | No independent witness; single writer/file scaling | Rewrite and concurrent-writer cases |
| Signed append-only store + independent checkpoints | Lower-complexity audit alternative | Key compromise, witness availability, weaker multi-party governance | Remote witness verification and rollback attack |
| Fabric with Raft | Candidate for organizations with known identities and crash-fault assumptions | Raft is not Byzantine tolerance | Leader/node loss, recovery and endorsement policies |
| Fabric with BFT ordering | Candidate when malicious orderers are in scope | More operational and governance complexity | Malicious/failed-node and quorum behavior |
| Besu QBFT | Candidate permissioned EVM implementation | Key/admin concentration and quorum dependence | Four-validator partition and contract tests |
| Public-chain anchoring | Optional externally visible checkpoint comparison | Privacy, variable fees, timing and jurisdictional constraints | Later scoped study; no deployment selected |

Fabric documentation distinguishes Raft and BFT ordering [S20]; Besu documents QBFT validator participation requirements [S22]. Fabric private collections are a possible access-control mechanism [S21]. These facts do not choose a winner. Freeze exact software/consensus versions in the experiment manifest.

## Proposed evidence path

Local detection → transactional incident store and outbox → asynchronous evidence worker → signed canonical commitment → blockchain submission → independently checked valid commit receipt.

The detector never waits for consensus. Preserve at least these states: `captured`, `queued`, `submitted`, `committed`, `failed`, `verification_failed`. Submission is not finality. During a partition, do not fabricate a committed status to keep the dashboard green.

An incident may be stored encrypted off-chain. Proposed commitment fields are schema/hash-algorithm version, opaque event reference, digest of canonical evidence or batch root, model/schema digests, reporter signature/key reference and creation/commit metadata. Keep detailed trajectories, identities, payloads and SHAP vectors off-chain by default. Hashing low-entropy personal information is not anonymization; use carefully designed randomized commitments when needed and keep verification material under access control.

Specify canonical serialization, numeric handling, byte encoding, signing domain and schema migration. An independent verifier must reconstruct the exact committed digest. With batching, store the membership proof for each incident. Document how old records remain verifiable after key rotation or application upgrades.

## Governance before infrastructure

Name proposed participants, who can submit evidence, who validates, who can change membership/contracts, who retains raw evidence and how disputes are resolved. A four-container network on one laptop is a real protocol demonstration, but it is not four independent trust domains.

For a Byzantine-tolerant study, a four-validator setup is a useful minimum experiment for one-fault scenarios; verify the chosen protocol’s exact quorum and fault assumptions. Losing two of four is a deliberate quorum-loss case, not an excuse to lower safety conditions. For Raft, test majority availability and clearly label the weaker fault model.

## E09 experiment matrix

Replay the same incident stream through every candidate. Record enqueue latency, submission/commit p50/p95/p99, valid committed throughput, backlog age, CPU/memory/storage, recovery duration and operations required. Separate hardware/cost assumptions from measurements.

Test: duplicate retries; conflicting duplicate IDs; process crash before/after acknowledgement; one validator/orderer down; quorum loss; network partition/rejoin; corrupt off-chain evidence; altered contract parameters; revoked reporter; key rotation; snapshot restore; full local-history rewrite; unavailable evidence object; and a dishonest but correctly signed sensor report.

For each case state which property is protected: integrity, authorization, ordering, availability or provenance. “Correctly committed” does not mean “factually true.” Consensus cannot repair malicious data submitted by a trusted reporter, compromised endpoint software or all relevant administrators colluding.

## Completion gate

A second node verifies an incident against the canonical evidence; only valid committed transactions appear as committed; a lost-quorum run queues without halting detection; recovery is idempotent; key/membership procedures are documented; and measured limitations are compared with the signed-log baseline. Final platform selection remains pending.
