#!/usr/bin/env python3
"""Verifier v1 — DAIVE v5.0 acceptance harness. See verifier/v1/ACCEPTANCE.md."""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE = os.path.join(ROOT, "daive_engine.py")

failures = []


def check(name: str, ok: bool, detail: str = "") -> None:
    print(f"[{'PASS' if ok else 'FAIL'}] {name}{(' — ' + detail) if detail else ''}")
    if not ok:
        failures.append(name)


# 1-2. Runs clean, exit 0, writes certificate + lock
r1 = subprocess.run([sys.executable, ENGINE], capture_output=True, text=True)
cert = os.path.join(ROOT, "daive_state_certificate.json")
lock = os.path.join(ROOT, "DAIVE_LOCK.txt")
check("exit_code_zero", r1.returncode == 0, f"rc={r1.returncode}")
check("certificate_written", os.path.exists(cert))
check("lock_written", os.path.exists(lock))

payload = json.load(open(cert))

# 3. Seal format + determinism across two runs
seal1 = payload["cryptographic_seal_sha256"]
check("seal_is_64_hex", bool(re.fullmatch(r"[0-9a-f]{64}", seal1)))
r2 = subprocess.run([sys.executable, ENGINE], capture_output=True, text=True)
seal2 = json.load(open(cert))["cryptographic_seal_sha256"]
check("seal_deterministic_across_runs", seal1 == seal2, f"{seal1[:12]} == {seal2[:12]}")

# 4. Gate families
fam = payload["families"]
for k, v in fam.items():
    check(f"family:{k}", v is True)
check("corpus_gates_all_passed",
      payload["gate_counts"]["corpus_lattice_passed"]
      == payload["gate_counts"]["corpus_lattice"],
      f"{payload['gate_counts']['corpus_lattice_passed']}"
      f"/{payload['gate_counts']['corpus_lattice']}")

core = payload["legacy_core"]
check("subgroup_order_7", core["subgroup_43_order"] == 7)
check("hamming_recovery_bit3", core["hamming"]["recovery_bit"] == 3)
check("rns_x_crt", core["rns_crt"]["x_crt"] == 3398738)

cav = payload["cavity"]
check("cavity_baseline_477_5", cav["baseline_rounded_mhz"] == 477.5
      and abs(cav["baseline_frequency_mhz"] - 477.496251) < 1e-4,
      f"{cav['baseline_frequency_mhz']}")
check("cavity_tuned_radius", abs(cav["tuned_radius_m"] - 0.0433658) < 5e-5,
      f"{cav['tuned_radius_m']}")

# Quarantine register contains the false mod-13 claim
q = json.dumps(payload["quarantine_register"])
check("quarantine_mod13_claim", "mod 13" in q and "= 5" in q)

# Governance: burned address preserved
check("governance_burned",
      payload["governance"]["outbound_status"].startswith("BURNED"))

# 5. Self-healing on a corrupted fixture
fixture = json.loads(subprocess.run(
    [sys.executable, "-c",
     "import sys; sys.path.insert(0, %r); import daive_engine as d; "
     "import json; print(json.dumps(d.build_canonical_manifest()))" % ROOT],
    capture_output=True, text=True).stdout)
fixture["tier_1b_algebraic_invariants"]["subgroup_43_order_mod49"] = 6      # drift
fixture["tier_3_crt"]["x_crt"] = 462034366                                  # drift
fixture["tier_2_derived"]["rns_master_modulus_m_prime"] = 281401947524847   # drift
fixture["unknown_injected_section"] = {"injected": True}                    # anomaly
fix_path = os.path.join(ROOT, "verifier", "v1", "corrupted_fixture.json")
json.dump(fixture, open(fix_path, "w"))

heal_code = ("import sys; sys.path.insert(0, %r); import daive_engine as d; "
             "import json; h = d.HealingEngine(); "
             "m = json.load(open(%r)); merged, notes = h.heal(m); "
             "ok = (merged['tier_1b_algebraic_invariants']"
             "['subgroup_43_order_mod49'] == 7 and "
             "merged['tier_3_crt']['x_crt'] == 3398738 and "
             "merged['tier_2_derived']['rns_master_modulus_m_prime'] "
             "== 281401947524849 and h.repair_log.verify_chain() and "
             "any('unknown' in n for n in notes)); "
             "print(json.dumps({'ok': ok, 'notes': len(notes)}))" % (ROOT, fix_path))
hr = json.loads(subprocess.run([sys.executable, "-c", heal_code],
                               capture_output=True, text=True).stdout)
check("heal_restores_derivable_fields", hr["ok"], f"notes={hr['notes']}")

# 6. Evolution registry: chain integrity + reject failing proposal
evo_code = ("import sys; sys.path.insert(0, %r); import daive_engine as d; "
            "e = d.EvolutionRegistry('test'); "
            "e.propose_invariant('good', 7, lambda v: v == 7); "
            "e.propose_invariant('bad', 6, lambda v: v == 7); "
            "print(e.chain[-1]['promoted'], e.chain[-2]['promoted'], "
            "e.verify_chain())" % ROOT)
er = subprocess.run([sys.executable, "-c", evo_code],
                    capture_output=True, text=True).stdout.split()
check("evolution_verify_before_promote", er[:2] == ["False", "True"],
      f"bad={er[0]} good={er[1]}")
check("evolution_chain_valid", er[2] == "True")

print()
if failures:
    print(f"VERIFIER v1: FAIL — {len(failures)} failing checks: {failures}")
    sys.exit(1)
print("VERIFIER v1: ALL ACCEPTANCE CRITERIA PASS")
