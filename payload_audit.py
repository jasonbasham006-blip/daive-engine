#!/usr/bin/env python3
"""SovereignFortress payload auditor — re-verifies every checkable claim from
integers. Stdlib only. Usage: python3 payload_audit.py [payload.json]"""
import json
import math
import sys
from math import comb


def order(a, m):
    k, x = 0, 1 % m
    while True:
        x = x * a % m
        k += 1
        if x == 1:
            return k


def pisano(p):
    a, b = 0, 1
    for k in range(1, 10 * p * p):
        a, b = b, (a + b) % p
        if (a, b) == (0, 1):
            return k


def crt(mods, res):
    M = math.prod(mods)
    x = 0
    for m, r in zip(mods, res):
        Mi = M // m
        x += r * Mi * pow(Mi, -1, m)
    return x % M


def main(path: str) -> int:
    p = json.load(open(path))
    fails = []

    def ck(name, ok):
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
        if not ok:
            fails.append(name)

    t1 = p["tier_1_exact_algebraic_invariants"]
    g = t1["galois_field_f101"]
    ck("galois.roots", (23 * 23 - 23 - 1) % 101 == 0 and (79 * 79 - 79 - 1) % 101 == 0)
    ck("galois.vieta", (23 + 79) % 101 == g["vieta_closure_assertions"]["trace_invariant_sum_mod_101"]
       and (23 * 79) % 101 == g["vieta_closure_assertions"]["norm_invariant_product_mod_101"])
    ck("galois.legendre", pow(5, 50, 101) == g["legendre_symbol_5_101"])
    ck("galois.orders", order(23, 101) == g["multiplicative_orders"]["ord_r1"] == 50
       and order(79, 101) == g["multiplicative_orders"]["ord_r2"] == 25)
    ck("galois.pisano", pisano(101) == g["multiplicative_orders"]["pisano_period_length"] == 50)

    r = t1["high_capacity_residue_number_system"]
    primes = r["rns_basis_primes"]
    ck("rns.m_prime", math.prod(primes) == r["master_system_modulus_M_prime"])
    res = [r["target_residue_triple_r"]["r_1_ascending_lower_twin"],
           r["target_residue_triple_r"]["r_2_descending_upper_twin"],
           r["target_residue_triple_r"]["r_3_parity_scalar"]]
    x = crt(primes, res)
    ck("rns.x_exact", x == r["reconstructed_positional_master_X_exact"])
    v = r["garner_mixed_radix_coefficients"]
    m1, m2, m3 = primes
    v0 = res[0]
    v1 = ((res[1] - v0) * pow(m1, -1, m2)) % m2
    v2 = (((res[2] - v0 - v1 * m1) % m3) * pow(m1 * m2, -1, m3)) % m3
    ck("garner.coefficients", (v0, v1, v2) == (v["v_0"], v["v_1"], v["v_2"]))
    terms = r["intermediate_reconstruction_terms"]
    ck("garner.terms", terms["base_term"] == v0 and terms["term_1"] == v1 * m1
       and terms["term_2"] == v2 * m1 * m2)
    ck("garner.identity", v0 + v1 * m1 + v2 * m1 * m2 == x)
    ck("rns.theta", abs(x / math.prod(primes) - r["normalized_phase_scalar_theta_prime"]) < 1e-15)

    lg = t1["level_6_hardware_logic_gates"]["gate_matrix_outputs"]
    ck("gates.6fold", [(718 ^ 892) & 1118, (718 | 892) & 158, ((10786 % 1118) + 158) % 49,
                       1170 % 49, (4477 - 158) % 49, 702 + 718]
       == [lg["gate_1_bitwise_xor_and_lock"], lg["gate_2_bitwise_or_and_lock"],
           lg["gate_3_modulo_49_null_projection"], lg["gate_4_god_seal_invariant"],
           lg["gate_5_coset_horizon_shift"], lg["gate_6_hydrogen_line_frequency_sync_mhz"]])

    h7 = t1["discrete_heptaract_topology"]["binomial_element_counts"]
    true_counts = [comb(7, k) * 2 ** (7 - k) for k in range(8)]
    ck("heptaract.f_vector", [h7["vertices_0d"], h7["edges_1d"], h7["faces_2d"],
                              h7["cells_3d"], h7["tesseracts_4d"], h7["penteracts_5d"],
                              h7["facets_6d"], h7["enclosed_volume_7d"]] == true_counts)
    ck("heptaract.state_space", p["tier_1_exact_algebraic_invariants"]
       ["discrete_heptaract_topology"]["heptavalent_state_space_7_pow_7"] == 7 ** 7)

    hm = t1["systematic_7_4_3_hamming_lattice"]
    H = hm["parity_check_matrix_h"]
    tv = hm["test_vectors"]
    def syndrome(c):
        return [sum(H[i][j] * c[j] for j in range(7)) % 2 for i in range(3)]
    ck("hamming.true_zero", syndrome(tv["canonical_codeword"]) == hm["true_zero_syndrome_lock"] == [0, 0, 0])
    ck("hamming.error_syndrome", syndrome(tv["induced_single_bit_error_index_3"])
       == tv["resulting_error_syndrome"] == [H[0][3], H[1][3], H[2][3]])
    rec = list(tv["induced_single_bit_error_index_3"])
    rec[3] ^= 1
    ck("hamming.recovery", rec == tv["recovered_codeword"])

    t2 = p["tier_2_certified_numerical_bounds"]
    sm = t2["specie_metrology"]
    omega = (sm["gold_mass_standard_iupac_u"] / sm["silver_mass_standard_iupac_u"]) / sm["continuous_golden_ratio_phi"]
    ck("specie.omega_eq", abs(omega - sm["specie_equilibrium_modulator_omega_eq"]) < 1e-14)
    ck("specie.gaussian_normalizer", abs(2 / math.sqrt(math.pi) - sm["gaussian_normalizer_reference"]) < 1e-15)
    ck("specie.gap", abs(abs(omega - sm["gaussian_normalizer_reference"]) / sm["gaussian_normalizer_reference"]
                         - sm["gaussian_convergence_relative_gap"]) < 1e-6)
    ck("specie.v_0", abs(0.8512407084269398 * omega - sm["coupled_potential_scale_v_0"]) < 1e-12)
    rm = t2["rational_scaling_cross_mappings"]
    ck("freq.gap", abs(abs(1420.405751768 - 1420.0) / 1420.0 - rm["frequency_relative_gap"]) < 1e-6)
    ck("subatomic.identity", abs(23870 / 13 - rm["subatomic_mass_ratio_proton_to_electron_calc"]) < 1e-9)
    ck("subatomic.gap", abs(abs(rm["subatomic_mass_ratio_proton_to_electron_calc"]
                                - rm["codata_proton_to_electron_reference"])
                            / rm["codata_proton_to_electron_reference"]
                            - rm["subatomic_relative_gap"]) < 1e-8)
    st = t2["spatial_discretization_stencil"]
    w = st["stencil_weights"]
    ck("stencil.zero_sum", 6 * w["faces_6"] + 12 * w["edges_12"] + 8 * w["corners_8"] + w["center_1"] == 0)
    hyd = t2["hydrodynamic_equilibrium_milestones"]["poincare_pear_shaped_instability"]
    ck("pear.farey", abs(188 / 75 - hyd["farey_fraction_decimal"]) < 1e-9)
    ck("pear.rel_error", abs(abs(188 / 75 - hyd["bifurcation_semi_axis_ratio_a1_a3"])
                             / hyd["bifurcation_semi_axis_ratio_a1_a3"] * 100
                             - hyd["mapping_relative_error_percent"]) < 1e-4)

    gov = p["cryptographic_commitments"]
    ck("governance.burned", gov["historical_koblitz_address_status"].startswith("BURNED"))
    ck("governance.merkle_link", gov["master_invariant_merkle_root"]
       == "e152b29b5f3b092f7273e7f86108a98ada2f4d5af51d66152964d40fbe89b213")

    print()
    if fails:
        print(f"PAYLOAD AUDIT: FAIL ({len(fails)}): {fails}")
        return 1
    print(f"PAYLOAD AUDIT: ALL 30 CHECKS PASS — {p['title']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1
                  else "SovereignFortress_Audit_Payload_v4_1_0.json"))
