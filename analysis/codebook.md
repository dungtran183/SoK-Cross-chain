# Codebook for study-level re-coding (v1, 2026-10-02)

Coders and procedure: every included study (S001–S168) was re-coded one at a time from its title and abstract by the first author, assisted by an LLM (Claude Opus 5.5) that drafted a code and a one-line rationale for each study. The author reviews every row in `recoded_studies.csv` before submission. When no bibliographic index exposed an abstract (27 studies), coding used the title and the venue record only (`basis = title`).

The unit of coding is the study's **own contribution and threat model** as stated in the title and abstract, not its category.

## Stage (primary contribution)
- `D` design time: a protocol, architecture, cryptographic scheme or formal model of a protocol.
- `P` pre-deployment: analysis of bridge or contract **code** before deployment (static analysis, symbolic execution, fuzzing, learned auditors, exploit generation used for testing).
- `R` runtime: monitoring, detection, trust or reputation scoring of live participants, and datasets or tools built for detection (e.g. transaction pairing).
- `X` response: actions after detection (pausing, kill switches, fund tracing after theft).
- `-` no defensive stage: attack papers, measurement studies, incident analyses and surveys.

## Attack classes (multi-label; a class is coded only when the abstract names a threat, property or mechanism that maps to it)
- `T1` attestation-key or verifier-set compromise (P1 with valid-looking evidence): dishonest or compromised committees, notaries, validators, relayer quorums, key custody; designs that remove or reduce trust in attesters (light clients, ZK proofs of consensus, trust boosting); reputation of attesters.
- `T2` verification flaws (P1/P3 through faulty checking of evidence): forged proofs, fake deposits, forged events or logs, light-client or proof-verifier bugs, value-binding gaps.
- `T3` authorization and contract-logic flaws (P4, often P3). Two kinds are recorded in `t3_kind`:
  - `policy`: the study designs authentication or access control for cross-chain principals or resources;
  - `impl`: the study targets implementation flaws in bridge or contract logic (unauthorized unlocks, unvalidated input, business-logic errors).
- `T4` observation and relay attacks (P1/P5 off-chain): relayer or oracle manipulation, censorship or delay, integrity of data in transit, light-client jamming, RPC poisoning.
- `T5` protocol consistency, atomicity and liveness (P2/P5): atomic swaps, replay, double spending, finality and reorganization, timeouts, griefing, sore-loser behavior, stalled transfers.
- `T6` economic and user-level attacks (P6): bribery, MEV and front-running, liquidity exhaustion, contagion through bridged collateral, laundering through bridges.
- `T7` privacy and linkability (P7): anonymity, confidentiality and unlinkability of users, amounts and routes.

Surveys (`-` with no class) are not coded for classes. Studies whose abstract names no specific threat get an empty class set and are counted as "unspecific".
