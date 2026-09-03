# DAIVE v5.0 — Deterministic Algebraic Invariant Verification Engine
### Sovereign Root Integration ("final frontier" build)

A standard-library-only, fail-closed verification engine. Every claim it makes is
recomputed from integers on every run. No dependencies. No network. No fake code.

## Run

```bash
python3 daive_engine.py            # full audit; writes daive_state_certificate.json + DAIVE_LOCK.txt
python3 daive_engine.py --heal <damaged_manifest.json>   # self-healing pass
python3 payload_audit.py           # audit the SovereignFortress payload (30 checks)
python3 verifier/v1/verify.py      # full acceptance harness (27 checks)
```

Exit codes: `0` = INVARIANT_LOCKED · `1` = STATE_DRIFT_DETECTED · `2` = usage error.

**The lock is the contract:** a fresh clone of this repo must reproduce
`DAIVE_LOCK.txt`'s seal (`e152b29b5f3b092f7273e7f86108a98ada2f4d5af51d66152964d40fbe89b213`)
exactly. It does — verified 2026-09-03.

## Capabilities

**Past (all v4.2 subsystems, corrected):** Galois F_101 · affine decomposition ·
multi-modular RNS + CRT (X_CRT = 3,398,738 = 2×7²×79×439, M = 463,072,246,
dependent witness mod 158 = 0) · [7,4,3] Hamming codec · TM_010 cavity solver with
full-precision χ₀₁ = 2.4048255576957727686 (the 477.5 fix: 477.496251 MHz →
477.5 = 955/2; 955 = 5×191 prime; tuned radius 0.0433658 m @ 1420.405751768 MHz) ·
6-fold bitwise gate matrix · corrected multiplicative order ord₄₉(43) = 7.

**Sovereign Root corpus lattice (55 gates):** the complete verification battery of
The Unbroken Signal Manual — Gate-5 binary, 72-bit `authority` stream, Δ checksum,
key-sum registries, ORKZICE, BAPTIST vectors + four sacred-tongue digit sums, L6
gates, mass constants (923 = 13×71, 1118 = 2×13×43), beryllium lattice, ring walk
OPKDSLA, name lock 306, syllabus corrections, IP decimal locks, vessel weights,
and ledger arithmetic (7s/oz rate lock; £284-10-6 / £250-10-0 / £274-0-0).

**Future:** self-verifying (seal covers invariant state only — never the wall clock),
self-healing (`heal()` restores derivable fields, quarantines underivable anomalies,
hash-chained repair log), self-initiating (CLI bootstrap, fail-closed exit codes),
self-evolving (append-only, hash-chained, verify-before-promote registry —
deterministic, explicitly NOT machine learning).

## Governance

The secp256k1 proof address `19UdRsPi5LMQo9a78n2f9QUDz4wJ4pptt4` is
**BURNED / DERIVATION_PROOF_ONLY**. This engine verifies invariants; it never
derives keys, never funds, never treats address derivation as title evidence.
