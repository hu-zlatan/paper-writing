"""Amendment 10 A7 (remaining part): integrated force over a hold of T s and the break-even T, by arithmetic on
results/v3/a_analysis.json A7_force (no new run). Integrated(arm, T) = shared phases (preload + squeeze + ramp-down,
N*s) + hold_F_N_mean(arm) * T, T in {1, 5, 30} s. Break-even vs CSF-1: the hold T at which CSF-1's extra hold force
(hold_F_N_mean(CSF-1) - hold_F_N_mean(arm)) * T equals the probe's extra force-time. Two readings, both reported:
(a) probe-specific phases = squeeze + ramp-down (a no-probe grasp still preloads); (b) all shared phases (upper bound).
Point values only (A7 has no interval). Writes results/v3/a7_integrated.json.  usage: python analysis_v3_d.py"""
import json
import os

from certgrip.io import ROOT

a = json.load(open(os.path.join(ROOT, "v3", "a_analysis.json")))["A7_force"]
ph = a["shared_phase_force_time_Ns"]
shared = ph["preload_mean"] + ph["squeeze_mean"] + ph["rampdown_mean"]
probe = ph["squeeze_mean"] + ph["rampdown_mean"]
F1 = a["arms"]["CSF-1"]["hold_F_N_mean"]
out = {"purpose": "p2 amendment 10 A7 integrated force / break-even (descriptive, point values, 08c CRC test split)",
       "shared_phases_Ns": shared, "probe_phases_Ns": probe, "arms": {}}
for arm, v in a["arms"].items():
    F = v["hold_F_N_mean"]; save = F1 - F
    out["arms"][arm] = {"integrated_Ns": {str(T): shared + F * T for T in (1, 5, 30)},
                        "hold_saving_vs_CSF1_N": save,
                        "break_even_T_s_probe_phases": (probe / save) if save > 0 else None,
                        "break_even_T_s_all_phases": (shared / save) if save > 0 else None}
json.dump(out, open(os.path.join(ROOT, "v3", "a7_integrated.json"), "w"), indent=1)
r = out["arms"]["full_rd@0.2#0"]
print(round(shared, 4), round(probe, 4), r)
