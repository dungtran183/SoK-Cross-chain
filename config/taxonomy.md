# Taxonomy — Controlled Vocabulary — Cross-Chain Bridge Attacks

Controlled vocabulary (source of truth for valid topic tags) for this knowledge
base. **Every tag in a paper card's `domains:` field and in
`compact*.jsonl .topics[]` MUST appear here.**

The vocabulary mirrors the paper's two analytical axes:
- the **attack surface** (where a bridge breaks), and
- the **defensive lifecycle stage** (when the attack is countered): design → pre-deployment → runtime → response.

## Category Hierarchy

### A. Surveys and Systematizations
Prior reviews, SoKs and multivocal studies of interoperability and bridge security.

| Code | Tag | Description |
|------|-----|-------------|
| `A.1` | `sok-bridge-security` | SoKs / surveys focused on bridge or cross-chain attacks and defenses |
| `A.2` | `survey-interoperability` | General blockchain interoperability / cross-chain technology surveys |
| `A.3` | `survey-defi-smart-contract` | Adjacent SoKs on DeFi / smart-contract attacks reused for definitions |

### B. Attack Surface and Empirical Attack Studies
Characterisations of how bridges and cross-chain protocols are attacked.

| Code | Tag | Description |
|------|-----|-------------|
| `B.1` | `atk-key-validator-compromise` | Private-key, validator-set, multisig/MPC committee or oracle compromise |
| `B.2` | `atk-verification-flaw` | Message/proof/signature/state verification bugs on the destination side |
| `B.3` | `atk-contract-logic` | Bridge contract logic, access control, upgrade/initialisation and accounting flaws |
| `B.4` | `atk-offchain-relay` | Relayer/oracle/off-chain component manipulation, censorship, liveness |
| `B.5` | `atk-protocol-level` | Replay, finality/reorg, front-running, HTLC griefing, DoS, consistency attacks |
| `B.6` | `atk-economic-user` | Economic, liquidity, phishing, front-end, and laundering via bridges |
| `B.7` | `incident-measurement` | Incident datasets, loss measurement, post-mortem and transaction-level studies |

### C. Design-Time Defenses
Architectural and cryptographic choices that remove trust or shrink the surface.

| Code | Tag | Description |
|------|-----|-------------|
| `C.1` | `def-lightclient-zk` | Light-client, SPV, zk-SNARK/STARK verified bridges |
| `C.2` | `def-threshold-committee` | TSS/MPC/threshold or committee-based verification, economic security |
| `C.3` | `def-formal-protocol` | Formal models, protocol verification, atomic swaps / HTLC design |
| `C.4` | `def-privacy-auth` | Privacy-preserving cross-chain authentication, identity, access control |

### D. Pre-Deployment Analysis
Detection of vulnerabilities in bridge code before deployment.

| Code | Tag | Description |
|------|-----|-------------|
| `D.1` | `pre-static-symbolic` | Static analysis, symbolic execution, taint analysis for cross-chain code |
| `D.2` | `pre-fuzzing-testing` | Fuzzing and dynamic testing of cross-chain contracts/protocols |
| `D.3` | `pre-ml-llm-audit` | ML / GNN / LLM-based vulnerability detection and auditing |

### E. Runtime Detection and Monitoring
Online detection of attacks or anomalies on deployed bridges.

| Code | Tag | Description |
|------|-----|-------------|
| `E.1` | `rt-rule-invariant` | Rule/invariant/accounting-based runtime monitors |
| `E.2` | `rt-graph-ml` | Transaction-graph mining and ML-based attack detection |
| `E.3` | `rt-trust-reputation` | Trust, reputation and behavioural scoring of relayers/validators |

### F. Response, Data and Benchmarks

| Code | Tag | Description |
|------|-----|-------------|
| `F.1` | `resp-mitigation` | Circuit breakers, rate limits, pausing, recovery, fund tracing |
| `F.2` | `data-benchmark` | Datasets and benchmarks for cross-chain security |

## Paper Types

| Type | Description |
|------|-------------|
| `survey` | Review / survey of a sub-field |
| `system` | An end-to-end built system / platform |
| `method` | A new algorithm / technique |
| `application` | Application of known methods to a domain |
| `benchmark` | A dataset / benchmark / evaluation suite |
| `theory` | Theoretical / analytical contribution |
| `empirical` | Measurement / empirical attack study |

## Novelty Classifications

| Classification | Description |
|----------------|-------------|
| `sota` | State of the art on a tracked benchmark / capability |
| `incremental` | Minor extension of a SoTA method |
| `complementary` | Different sub-problem or methodology, same domain |
| `derivative` | Known methods applied unmodified to a new domain |
| `survey` | Survey / review paper |
| `foundational` | Paradigm-defining ancestor that SoTA work depends on |
