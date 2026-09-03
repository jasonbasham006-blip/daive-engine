# Verifier — DAIVE Engine

Append-only index of acceptance-criteria versions and run records.

| Version | Created | Measures | Differs from prior |
|---|---|---|---|
| v1 | 2026-09-02 | Exit code, certificate presence, seal format + cross-run seal determinism, all-gates-passed flags, corpus-gate count, 477.5 cavity lock, subgroup order 7, RNS/CRT constants, Hamming recovery, heal-on-corruption recovery, evolution-chain integrity | initial |
| v2 | 2026-09-02 | Payload-level audit: JSON validity, all integer-checkable claims in SovereignFortress_Audit_Payload_v4_1_0 (Galois orders/Pisano, RNS ordering, Garner identity, gates, heptaract f-vector, Hamming, tier-2 bounds, stencil, Farey, governance) via payload_audit.py; live two-node mesh test via mesh_test.py | v1 checked the engine; v2 checks the payload document and the mesh |

Run records are appended under `verifier/runs/` (one file per run: command, exit code, values produced).
