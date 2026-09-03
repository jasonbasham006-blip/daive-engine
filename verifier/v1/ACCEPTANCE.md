# Acceptance Criteria v1 — DAIVE v5.0 "Sovereign Root Integration"

The engine MUST:
1. Run with the Python 3 standard library only; exit 0 on a clean audit.
2. Write `daive_state_certificate.json` and `DAIVE_LOCK.txt` on every run.
3. Produce a 64-hex SHA-256 seal that is identical across two consecutive runs in the same directory (determinism).
4. Report `all_gates_passed == true` across every gate family:
   - v4.2 legacy: Galois F101 (roots 23/79, Vieta, inverses 22/78, sqrt5 {45,56}), affine decomposition closure, RNS/CRT (X=3398738, M=463072246, y2=173, dependent witness mod 158 = 0), Hamming true-zero + single-bit recovery, 6 bitwise gates, cavity solver.
   - The `<43>` multiplicative order mod 49 must compute as exactly 7 (fixes the v4.2 off-by-one audit bug).
   - Cavity: full-precision chi_01 = 2.4048255576957727686; baseline frequency rounds to 477.5 MHz = 955/2 (955 = 5 x 191, 191 prime); tuned radius ~0.0433658 m.
   - Sovereign Root corpus lattice: every gate ported from The Unbroken Signal Manual Appendix A (Gate-5 binary, authority stream, Delta checksum, key sums, ORKZICE, BAPTIST vectors + four tongue sums, L6 gates, mass constants 923/1118, beryllium lattice, ring walk OPKDSLA, name lock 306, syllabus corrections, IP decimals, vessel weights 230/238, ledger arithmetic incl. the 7s/oz rate lock and the £284-10-6 / £250-10-0 / £274-0-0 figures).
   - The false auxiliary claim "X_CRT ≡ 0 (mod 13)" must NOT be asserted (true value: 5); it must appear in the quarantine register.
5. Self-healing: given a deliberately corrupted manifest (three mutated derivable fields + one underivable anomaly), heal() must restore all derivable fields exactly, quarantine the underivable anomaly, and return a repair report whose hash-chain verifies.
6. Self-evolving: the evolution registry must expose an append-only hash chain; a proposed invariant that fails verification must be rejected (not promoted).
7. The burned secp256k1 proof address must remain marked BURNED / DERIVATION_PROOF_ONLY; the engine must never derive or suggest keys for funding.

Verification harness: `verifier/v1/verify.py` — runs the engine, exercises heal() with a corrupted fixture, walks the evolution chain, and checks every criterion above. Every execution is logged under `verifier/runs/`.
