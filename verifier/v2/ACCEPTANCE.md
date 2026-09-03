# Acceptance Criteria v2 — SovereignFortress Audit Payload v4.1.0 + mesh

Adds payload-level and mesh-level verification on top of v1.

The upgraded payload MUST:
1. Parse as valid JSON.
2. Pass `payload_audit.py` — every checkable claim re-verified from integers:
   Galois orders/Pisano/Legendre, RNS M' + X_exact + residue ordering, Garner
   coefficients and reconstruction identity, 6 gates, heptaract f-vector,
   Hamming matrix + true-zero + recovery, Tier-2 bounds (omega_eq, gaussian
   normalizer 2/sqrt(pi), gaps, v_0, frequency gap, subatomic ratio), stencil
   zero-sum, Farey approximant + recomputed relative error, governance (burned
   address, DAIVE seal linkage).
3. Contain no v4.0.0 defect: no empty arrays, no swapped residue ordering,
   no stale Garner terms, no corrupted Hamming row, no 823543 in the 7d slot,
   no 0.0095% Farey error, no O(h^4)/Q-08 contradiction.

The mesh MUST (verifier/v2/mesh_test.py):
1. Start two nodes from genesis.json and reach height >= 3.
2. Converge to identical chains (block hashes equal on both nodes).
3. Propagate an injected transaction to both chains.
4. Anchor every block to the DAIVE audit seal e152b29b...89b213.
5. Keep the genesis block linked to the all-zero prev hash.

Differs from v1: v1 checks the engine; v2 checks the payload document and the live mesh.
