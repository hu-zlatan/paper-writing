"""TouchBED experiment entry point. Every result written by this script comes from the real algorithms in touchbed/.

Sub-commands
  train    train a learned policy (spce_total | spce_myopic | no_nc_obj | no_nc_input | rl_success); writes
           <out>.json (config, status, learning curve) and <out>.npz (weights)
  eval     evaluate a method on a slice of a fixed episode split; writes one JSON line per episode to <out>.jsonl
  pilot    single-condition pilot that prints TIME_ESTIMATE lines (mandatory before every sweep)

Examples
  python main.py pilot --set S
  python main.py train --set S --method spce_total --seed 0 --L 4095 --max-episodes 100000 --out ../results/v1/train/S_spce_total_s0
  python main.py eval --set S --T 5 --method greedy --split test --start 0 --count 100 --n-eval 8000 --out ../results/v1/eval/x
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from touchbed.evaluate import make_states, run_episode  # noqa: E402
from touchbed.likelihood import ObsModel  # noqa: E402
from touchbed.policies import CoveragePolicy, GreedyEIGPolicy, RandomPolicy  # noqa: E402
from touchbed.train import TrainConfig, Trainer  # noqa: E402

LEARNED = ("spce_total", "spce_myopic", "no_nc_obj", "no_nc_input", "rl_success")


def env_info():
    return {"python": sys.version.split()[0], "numpy": np.__version__, "platform": platform.platform(),
            "cpu_count": os.cpu_count(), "time_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}


def save_trainer(tr: Trainer, out: str):
    sd = tr.state_dict()
    arrs = {f"pi_{i}": p for i, p in enumerate(sd["pi"])}
    arrs.update({f"vf_{i}": p for i, p in enumerate(sd["vf"])})
    arrs["log_std"] = sd["log_std"]
    np.savez_compressed(out + ".npz", **arrs)


def load_trainer(weights: str) -> Trainer:
    meta = json.load(open(weights.replace(".npz", ".json")))
    cfg = TrainConfig(**{k: (tuple(v) if k == "T_choices" else v) for k, v in meta["config"].items()})
    tr = Trainer(cfg)
    z = np.load(weights)
    for i, p in enumerate(tr.pi.params()):
        p[...] = z[f"pi_{i}"]
    tr.log_std[...] = z["log_std"]
    return tr


class LearnedAdapter:
    def __init__(self, tr: Trainer, T: int):
        self.tr, self.T = tr, T

    def act(self, pf):
        return self.tr.act_deterministic(pf.hist, self.T)


def cmd_train(a):
    cfg = TrainConfig(setname=a.set, method=a.method, L=a.L, batch=a.batch, seed=a.seed, max_episodes=a.max_episodes,
                      val_every=a.val_every, val_episodes=a.val_episodes, budget_minutes=a.budget_minutes,
                      encoder=a.encoder, budget_input=not a.no_budget_input, lr=a.lr, ent_coef=a.ent_coef,
                      critic_lr=a.critic_lr, extra={"train_pf_n": a.train_pf_n, "train_pf_mh": a.train_pf_mh})
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    tr = Trainer(cfg)
    t0 = time.time()
    status = tr.train(log_path=a.out + ".json")
    save_trainer(tr, a.out)
    meta = json.load(open(a.out + ".json"))
    meta["env"] = env_info()
    meta["wall_s"] = time.time() - t0
    json.dump(meta, open(a.out + ".json", "w"))
    print(f"TRAIN_DONE status={status} episodes={tr.episodes} wall_s={time.time() - t0:.0f}")


def policy_factory(a, T):
    if a.method == "random":
        return RandomPolicy, False
    if a.method == "coverage":
        return (lambda rng: CoveragePolicy(rng, C=a.C)), True
    if a.method == "greedy":
        return (lambda rng: GreedyEIGPolicy(rng, C=a.C, M=a.M)), True
    tr = load_trainer(a.weights)
    return (lambda rng: LearnedAdapter(tr, T)), False


def cmd_eval(a):
    om = ObsModel()
    lib, prior, states = make_states(a.set, a.split, a.start + a.count)
    fac, needs = policy_factory(a, a.T)
    obs_fn = None
    if a.mujoco_radius > 0:
        from touchbed.mujoco_eval import MujocoProbe
        obs_fn = MujocoProbe(lib.shapes, r_finger=a.mujoco_radius).sample_obs
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    t0 = time.time()
    with open(a.out + ".jsonl", "w") as f:
        for i in range(a.start, a.start + a.count):
            if time.time() - t0 > 0.8 * a.budget_minutes * 60:
                f.write(json.dumps({"EARLY_STOP_AT_80_PCT_BUDGET": True, "next_index": i}) + "\n")
                print("EARLY_STOP_AT_80_PCT_BUDGET", flush=True)
                break
            r, lat = run_episode(fac, lib, prior, om, states[i], a.T, (a.set, a.split, a.T, i), n_eval=a.n_eval,
                                 n_dec=a.n_dec, needs_belief=needs, obs_fn=obs_fn,
                                 pf_kwargs={"mh_steps": a.mh_steps})
            r.update({"episode": i, "set": a.set, "T": a.T, "method": a.method, "weights": a.weights, "n_eval": a.n_eval, "mujoco_radius": a.mujoco_radius, "mh_steps": a.mh_steps,
                      "latencies_s": lat})
            f.write(json.dumps(r) + "\n")
            f.flush()
    print(f"EVAL_DONE n={a.count} wall_s={time.time() - t0:.0f}")


def cmd_pilot(a):
    """One condition end-to-end per component; prints TIME_ESTIMATE lines used to size every sweep."""
    om = ObsModel()
    lib, prior, states = make_states(a.set, "pilot", 4)
    for name, fac, needs in (("random", RandomPolicy, False), ("greedy", lambda r: GreedyEIGPolicy(r, 64, 64), True)):
        t = time.time()
        for i, s0 in enumerate(states):
            run_episode(fac, lib, prior, om, s0, 5, (a.set, "pilot", 5, i), n_eval=a.n_eval, needs_belief=needs)
        per = (time.time() - t) / len(states)
        n_ep = 2 * 2000 * 4
        print(f"TIME_ESTIMATE: eval[{name}] {per:.2f}s per episode (T=5) x {n_ep} episodes (2 sets x 2000 x 4 budgets)"
              f" ~ {per * n_ep * 6.5 / 5 / 3600:.1f} CPU-h (scaled to mean T 6.5)", flush=True)
    cfg = TrainConfig(setname=a.set, L=a.L, batch=128, val_every=10 ** 9, max_episodes=128 * 3)
    tr = Trainer(cfg)
    t = time.time()
    tr.train(verbose=False)
    per = (time.time() - t) / tr.episodes
    print(f"TIME_ESTIMATE: train {per * 1000:.1f} ms per episode (L={a.L}) x 1e5 episodes x 1 run ~"
          f" {per * 1e5 / 3600:.2f} CPU-h per run (+ validation)", flush=True)


# ---------------------------------------------------------------------------------------------------------------- v2
def save_v2(tr, out):
    arrs = {f"pi_{i}": p for i, p in enumerate(tr.pi.params())}
    arrs.update({f"vf_{i}": p for i, p in enumerate(tr.vf.params())})
    np.savez_compressed(out + ".npz", **arrs)


def load_v2(weights):
    from touchbed.train_v2 import TrainConfigV2, TrainerV2
    meta = json.load(open(weights.replace(".npz", ".json")))
    tr = TrainerV2(TrainConfigV2(**meta["config"]))
    z = np.load(weights)
    for i, p in enumerate(tr.pi.params()):
        p[...] = z[f"pi_{i}"]
    return tr


def cmd_train2(a):
    from touchbed.train_v2 import TrainConfigV2, TrainerV2
    cfg = TrainConfigV2(setname=a.set, method=a.method, kappa=a.kappa, tau=a.tau, L=a.L, J=a.J, batch=a.batch,
                        lr=a.lr, critic_lr=a.critic_lr, ent_coef=a.ent_coef, seed=a.seed, max_episodes=a.max_episodes,
                        val_every=a.val_every, val_episodes=a.val_episodes, budget_minutes=a.budget_minutes)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    tr = TrainerV2(cfg)
    t0 = time.time()
    status = tr.train(log_path=a.out + ".json")
    save_v2(tr, a.out)
    meta = json.load(open(a.out + ".json"))
    meta.update({"env": env_info(), "wall_s": time.time() - t0})
    json.dump(meta, open(a.out + ".json", "w"))
    print(f"TRAIN_DONE status={status} episodes={tr.episodes} wall_s={time.time() - t0:.0f}")


def cmd_eval2(a):
    from touchbed.evaluate_v2 import make_states_v2, run_episode_v2
    from touchbed.policies_v2 import CoverageV2, GStar, RandomV2
    from touchbed.travel import rung_subset
    om = ObsModel()
    lib, prior, eps = make_states_v2(a.set, a.split, a.start + a.count)
    if a.method == "random":
        fac, needs = RandomV2, False
    elif a.method == "coverage":
        fac, needs = CoverageV2, True
    elif a.method in ("gstar", "full_state_greedy"):
        sub = None if a.rung_phi == 32 and a.rung_psi == 8 else rung_subset(a.rung_phi, a.rung_psi)
        tgt = "ball" if a.method == "gstar" else "state"
        fac, needs = (lambda rng: GStar(rng, M=a.M, subset=sub, target=tgt)), True
    else:
        tr = load_v2(a.weights)
        fac, needs = (lambda rng: tr), False
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    t0 = time.time()
    with open(a.out + ".jsonl", "w") as f:
        for i in range(a.start, a.start + a.count):
            if time.time() - t0 > 0.8 * a.budget_minutes * 60:
                f.write(json.dumps({"EARLY_STOP_AT_80_PCT_BUDGET": True, "next_index": i}) + "\n")
                print("EARLY_STOP_AT_80_PCT_BUDGET", flush=True)
                break
            s0, phi0 = eps[i]
            r = run_episode_v2(fac, lib, prior, om, s0, phi0, a.kappa, a.tau, (a.set, a.split, a.kappa, a.tau, i),
                               n_eval=a.n_eval, n_dec=a.n_dec, needs_belief=needs, pf_kwargs={"mh_steps": a.mh_steps})
            r.update({"episode": i, "set": a.set, "kappa": a.kappa, "tau": a.tau, "method": a.method,
                      "weights": a.weights, "n_eval": a.n_eval, "n_dec": a.n_dec, "M": a.M,
                      "rung": [a.rung_phi, a.rung_psi], "mh_steps": a.mh_steps})
            f.write(json.dumps(r) + "\n")
            f.flush()
    print(f"EVAL2_DONE n={a.count} wall_s={time.time() - t0:.0f}")


def cmd_calib(a):
    """G5 tau calibration (docs/07_hypotheses_v2.md §1.2): run G* WITHOUT a budget for n* probes on pilot episodes and
    record the travel time it spends; tau_kappa = n* + mean travel time (rounded to 0.1), then verified with the budget."""
    from touchbed.evaluate import stream
    from touchbed.evaluate_v2 import make_states_v2
    from touchbed.pf import ParticleFilter
    from touchbed.likelihood import sample_obs
    from touchbed.policies_v2 import GStar
    from touchbed.travel import PHI, PSI, TravelState
    om = ObsModel()
    lib, prior, eps = make_states_v2(a.set, "pilot", a.start + a.count)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out + ".jsonl", "w") as f:
        for i in range(a.start, a.start + a.count):
            (k0, x0, y0, t0), phi0 = eps[i]
            key = (a.set, "calib", a.kappa, i)
            pol = GStar(stream("policy", *key), M=a.M)
            pf = ParticleFilter(lib, om, prior, a.n_dec, stream("pf_dec", *key))
            ts = TravelState(phi0, a.kappa, 1e9)
            orng = stream("obs", *key)
            travel_time = 0.0
            for _ in range(a.n_star):
                c0 = ts.costs()
                act = pol.act(pf, ts)
                travel_time += float(c0[act]) - 1.0
                ts.step(act)
                obs = tuple(v[0] for v in sample_obs(om, lib, orng, np.array([k0]), x0, y0, t0, float(PHI[act]), float(PSI[act])))
                pf.update(float(PHI[act]), float(PSI[act]), obs)
            f.write(json.dumps({"episode": i, "set": a.set, "kappa": a.kappa, "n_star": a.n_star,
                                "travel_time": travel_time, "travel_rad": ts.travel}) + "\n")
            f.flush()
    print("CALIB_DONE")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("train")
    t.add_argument("--set", default="S"); t.add_argument("--method", default="spce_total", choices=LEARNED)
    t.add_argument("--seed", type=int, default=0); t.add_argument("--L", type=int, default=4095)
    t.add_argument("--batch", type=int, default=128); t.add_argument("--max-episodes", type=int, default=100_000)
    t.add_argument("--val-every", type=int, default=10_240); t.add_argument("--val-episodes", type=int, default=200)
    t.add_argument("--budget-minutes", type=float, default=330.0); t.add_argument("--encoder", default="deepsets")
    t.add_argument("--no-budget-input", action="store_true"); t.add_argument("--lr", type=float, default=3e-4)
    t.add_argument("--ent-coef", type=float, default=1e-3); t.add_argument("--critic-lr", type=float, default=1e-3); t.add_argument("--train-pf-n", type=int, default=500); t.add_argument("--train-pf-mh", type=int, default=2); t.add_argument("--out", required=True)
    e = sub.add_parser("eval")
    e.add_argument("--set", default="S"); e.add_argument("--T", type=int, default=5)
    e.add_argument("--method", default="random"); e.add_argument("--weights", default=None)
    e.add_argument("--split", default="test"); e.add_argument("--start", type=int, default=0)
    e.add_argument("--count", type=int, default=100); e.add_argument("--n-eval", type=int, default=8000)
    e.add_argument("--n-dec", type=int, default=2000); e.add_argument("--C", type=int, default=64)
    e.add_argument("--M", type=int, default=64); e.add_argument("--mujoco-radius", type=float, default=0.0); e.add_argument("--mh-steps", type=int, default=3); e.add_argument("--budget-minutes", type=float, default=330.0)
    e.add_argument("--out", required=True)
    p = sub.add_parser("pilot")
    p.add_argument("--set", default="S"); p.add_argument("--L", type=int, default=4095)
    p.add_argument("--n-eval", type=int, default=8000)
    t2 = sub.add_parser("train2")
    t2.add_argument("--set", default="S"); t2.add_argument("--method", default="spce_total")
    t2.add_argument("--kappa", type=float, default=6.0); t2.add_argument("--tau", type=float, default=10.0)
    t2.add_argument("--L", type=int, default=4095); t2.add_argument("--J", type=int, default=16)
    t2.add_argument("--batch", type=int, default=128); t2.add_argument("--lr", type=float, default=3e-4)
    t2.add_argument("--critic-lr", type=float, default=1e-3); t2.add_argument("--ent-coef", type=float, default=1e-3)
    t2.add_argument("--seed", type=int, default=0); t2.add_argument("--max-episodes", type=int, default=100_000)
    t2.add_argument("--val-every", type=int, default=10_240); t2.add_argument("--val-episodes", type=int, default=500)
    t2.add_argument("--budget-minutes", type=float, default=330.0); t2.add_argument("--out", required=True)
    e2 = sub.add_parser("eval2")
    e2.add_argument("--set", default="S"); e2.add_argument("--method", default="random")
    e2.add_argument("--kappa", type=float, default=0.0); e2.add_argument("--tau", type=float, default=4.0)
    e2.add_argument("--weights", default=None); e2.add_argument("--split", default="test")
    e2.add_argument("--start", type=int, default=0); e2.add_argument("--count", type=int, default=100)
    e2.add_argument("--n-eval", type=int, default=32000); e2.add_argument("--n-dec", type=int, default=2000)
    e2.add_argument("--M", type=int, default=64); e2.add_argument("--rung-phi", type=int, default=32)
    e2.add_argument("--rung-psi", type=int, default=8); e2.add_argument("--mh-steps", type=int, default=3)
    e2.add_argument("--budget-minutes", type=float, default=330.0); e2.add_argument("--out", required=True)
    cb = sub.add_parser("calib")
    cb.add_argument("--set", default="S"); cb.add_argument("--kappa", type=float, default=6.0)
    cb.add_argument("--n-star", type=int, default=4); cb.add_argument("--start", type=int, default=0)
    cb.add_argument("--count", type=int, default=50); cb.add_argument("--n-dec", type=int, default=2000)
    cb.add_argument("--M", type=int, default=64); cb.add_argument("--out", required=True)
    a = ap.parse_args()
    {"calib": cmd_calib, "train": cmd_train, "eval": cmd_eval, "pilot": cmd_pilot, "train2": cmd_train2, "eval2": cmd_eval2}[a.cmd](a)


if __name__ == "__main__":
    main()
