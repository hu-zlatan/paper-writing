"""RL comparator sweep selection (amendment v3.1 D9): 4 configs, seed 519, E_train = 5e4, S12.
Rule: highest final validation ball-sPCE of the argmax policy; ties within 0.02 nats -> lower index.
Deviation (recorded in PROGRESS, run 6): the value is the trainer's own validation stream (stream "val_v2",
500 episodes, last validation at 40,960 episodes since val_every = 10,240), not val3.
Writes results/v3/12_rl_sweep_selection.json."""
import json
import os

base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "v3")
rows = []
for c in range(4):
    d = json.load(open(os.path.join(base, "rl", f"sweep_S_k12_cfg{c}_sd519.json")))
    vals = [h for h in d["history"] if "val_ball_spce" in h]
    cfg = d["config"]
    rows.append({"cfg": c, "lr": cfg["lr"], "ent_coef": cfg["ent_coef"], "batch": cfg["batch"],
                 "critic_lr": cfg["critic_lr"], "status": d["status"], "episodes": d["history"][-1]["episodes"],
                 "final_val_episodes": vals[-1]["episodes"], "final_val_ball_spce": vals[-1]["val_ball_spce"],
                 "final_val_ball_spce_sampled": vals[-1]["val_ball_spce_sampled"],
                 "train_g_T_last_batch": d["history"][-1]["g_T_mean"]})
best = max(r["final_val_ball_spce"] for r in rows)
sel = min(r["cfg"] for r in rows if r["final_val_ball_spce"] >= best - 0.02)
out = {"rule": "argmax final val ball-sPCE; ties within 0.02 nats -> lower index", "rows": rows, "selected_cfg": sel,
       "validation_stream": "trainer val_v2 (deviation: not val3)"}
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(base, "12_rl_sweep_selection.json"), "w"), indent=1)
