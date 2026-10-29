"""v3 sub-commands of main.py (amendments v3.0 / v3.1; docs/08_experiment_plan_v3.yaml). Every output records the
action set (TOUCHBED_NPHI) and is written incrementally; long loops stop at 80 % of --budget-minutes and say so."""
from __future__ import annotations

import glob
import json
import os
import platform
import time

import numpy as np

from .evaluate import stream
from .likelihood import ObsModel
from .travel import A, N_PHI


def _env():
    return {"TOUCHBED_NPHI": os.environ.get("TOUCHBED_NPHI", "32"), "action_set": f"{N_PHI}x8", "A": A,
            "numpy": np.__version__, "python": platform.python_version(),
            "threads": {k: os.environ.get(k) for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")}}


def _open(out, suffix):
    os.makedirs(os.path.dirname(os.path.abspath(out)) or ".", exist_ok=True)
    return open(out + suffix, "w")


# ─── weights ─────────────────────────────────────────────────────────────────────────────────────────────────────────
def save_student(path, st, meta):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    ps = st.get_state()
    np.savez_compressed(path, kind=np.array(type(st).__name__), meta=np.array(json.dumps(meta)),
                        **{f"p{i}": p for i, p in enumerate(ps)})


def load_student(path):
    from .distill import BeliefStudent, Student
    d = np.load(path, allow_pickle=False)
    meta = json.loads(str(d["meta"]))
    cls = {"Student": Student, "BeliefStudent": BeliefStudent}[str(d["kind"])]
    st = cls(np.random.default_rng(0), hidden=meta["hidden"], tau=meta["tau"])
    n = len(st.get_state())
    st.set_state([d[f"p{i}"] for i in range(n)])
    return st, meta


# ─── policies ────────────────────────────────────────────────────────────────────────────────────────────────────────
class Pruned:
    """H1-fb: student top-k (or k random feasible actions) re-scored by G* (N = 2,000 decision PF, M = 64)."""
    needs_belief = True

    def __init__(self, rng, student, k=16, M=64, random_k=False):
        from .policies_v2 import GStar
        self.student, self.k, self.random_k, self.rng = student, k, random_k, rng
        self.g = GStar(rng, M=M)

    def act(self, pf, ts):
        feas = np.flatnonzero(ts.feasible())
        if self.random_k:
            top = self.rng.choice(feas, size=min(self.k, len(feas)), replace=False)
        else:
            from .latency3 import timed_student
            _, z, _ = timed_student(self.student, pf.hist, ts)
            top = feas[np.argsort(-z[feas], kind="stable")[:self.k]]
        self.g.subset = np.sort(top)
        return self.g.act(pf, ts)


def make_policy(method, rng, n_star=None, weights=None):
    """Returns (policy, needs_belief, n_dec)."""
    from .heuristics import HEURISTICS
    from .latency3 import parse, subset_for
    from .policies_v2 import GStar, RandomV2
    if method == "random":
        return RandomV2(rng), False, 2000
    if method == "gstar":
        return GStar(rng, M=64), True, 2000
    if method in HEURISTICS:
        cls = HEURISTICS[method]
        return cls(rng, n_star), cls.needs_belief, 2000
    if method.startswith("g") and method.count("_") == 2:          # greedy grid configuration gN_C_M
        N, C, M = parse(method)
        return GStar(rng, M=M, subset=subset_for(C)), True, N
    if method in ("student", "belief_student", "bc"):
        st, _ = load_student(weights)
        return st, st.needs_belief, 2000
    if method == "rl":                                              # RL-relative comparator (train2 --frame rel)
        from .train_v2 import TrainConfigV2, TrainerV2
        meta = json.load(open(weights.replace(".npz", ".json")))
        tr = TrainerV2(TrainConfigV2(**meta["config"]))
        z = np.load(weights)
        for i, p in enumerate(tr.pi.params()):
            p[...] = z[f"pi_{i}"]
        return tr, False, 2000
    if method in ("pruned16", "random16"):
        st, _ = load_student(weights)
        return Pruned(rng, st, 16, 64, random_k=method == "random16"), True, 2000
    raise ValueError(method)


# ─── commands ────────────────────────────────────────────────────────────────────────────────────────────────────────
def cmd_eval3(a):
    """Evaluate one method on episodes [start, start+count) of a v3 split in one cell; grid read-out (v3.0 C2)."""
    from .v3 import ep_key_v3, require_v3_actions, run_episode_v3, states_v3
    if not a.allow_32:
        require_v3_actions()
    om = ObsModel()
    idx = range(a.start, a.start + a.count)
    lib, prior, eps = states_v3(a.set, a.split, idx)
    t0 = time.time()
    with _open(a.out, ".jsonl") as f:
        f.write(json.dumps({"header": True, "args": vars(a), "env": _env()}) + "\n")
        for i, (s0, phi0) in zip(idx, eps):
            if time.time() - t0 > 0.8 * a.budget_minutes * 60:
                f.write(json.dumps({"EARLY_STOP_AT_80_PCT_BUDGET": True, "next_index": i}) + "\n")
                break
            key = ep_key_v3(a.set, a.split, a.kappa, a.tau, i)
            pol, needs, n_dec = make_policy(a.method, stream("policy", *key), a.n_star, a.weights)
            t1 = time.time()
            r = run_episode_v3(pol, lib, prior, om, s0, phi0, a.kappa, a.tau, key, needs_belief=needs, n_dec=n_dec,
                               evaluate=not a.no_grid, grid_sub=a.sub)
            r.pop("history")
            r.update({"episode": i, "set": a.set, "split": a.split, "kappa": a.kappa, "tau": a.tau, "method": a.method,
                      "action_set": f"{N_PHI}x8", "wall_s": time.time() - t1,
                      "latency_median_s": float(np.median(r["latencies_s"])) if r["latencies_s"] else 0.0})
            f.write(json.dumps(r) + "\n"); f.flush()
    print(f"EVAL3_DONE wall_s={time.time() - t0:.0f}")


def cmd_calib3(a):
    """Cal′ (v3.0 C4): G* without a budget for n* probes on cal3 episodes; records travel time (tau_kappa rule)."""
    from .likelihood import sample_obs
    from .pf import ParticleFilter
    from .policies_v2 import GStar
    from .travel import PHI, PSI, TravelState
    from .v3 import require_v3_actions, states_v3
    if not a.allow_32:
        require_v3_actions()
    om = ObsModel()
    idx = range(a.start, a.start + a.count)
    lib, prior, eps = states_v3(a.set, "cal3", idx)
    t0 = time.time()
    with _open(a.out, ".jsonl") as f:
        f.write(json.dumps({"header": True, "args": vars(a), "env": _env()}) + "\n")
        for i, ((k0, x0, y0, t0_), phi0) in zip(idx, eps):
            if time.time() - t0 > 0.8 * a.budget_minutes * 60:
                f.write(json.dumps({"EARLY_STOP_AT_80_PCT_BUDGET": True, "next_index": i}) + "\n")
                break
            key = (a.set, "cal3", float(a.kappa), int(i))
            pol = GStar(stream("policy", *key), M=64)
            pf = ParticleFilter(lib, om, prior, 2000, stream("pf_dec", *key))
            ts = TravelState(phi0, a.kappa, 1e9)
            orng = stream("obs", *key)
            travel_time = 0.0
            for _ in range(a.n_star):
                c0 = ts.costs()
                act = pol.act(pf, ts)
                travel_time += float(c0[act]) - 1.0
                ts.step(act)
                obs = tuple(v[0] for v in sample_obs(om, lib, orng, np.array([k0]), x0, y0, t0_, float(PHI[act]),
                                                     float(PSI[act])))
                pf.update(float(PHI[act]), float(PSI[act]), obs)
            f.write(json.dumps({"episode": i, "set": a.set, "kappa": a.kappa, "n_star": a.n_star,
                                "travel_time": travel_time, "travel_rad": ts.travel}) + "\n"); f.flush()
    print(f"CALIB3_DONE wall_s={time.time() - t0:.0f}")


def _label_loop(a, split, idx_list, policy_fn, beta, mix_key):
    from .distill import episode_arrays, save_shard
    from .policies_v2 import GStar
    from .v3 import ep_key_v3, require_v3_actions, run_episode_v3, states_v3
    if not a.allow_32:
        require_v3_actions()
    om = ObsModel()
    lib, prior, eps = states_v3(a.set, split, idx_list, kappa=a.kappa)
    T = int(np.floor(a.tau + 1e-9))
    packed, summ = [], []
    t0 = time.time()
    status = "complete"
    for i, (s0, phi0) in zip(idx_list, eps):
        if time.time() - t0 > 0.8 * a.budget_minutes * 60:
            status = "EARLY_STOP_AT_80_PCT_BUDGET"
            break
        key = ep_key_v3(a.set, split, a.kappa, a.tau, i)
        teacher = GStar(stream("teacher", *key), M=64)
        pol = policy_fn()
        r = run_episode_v3(pol, lib, prior, om, s0, phi0, a.kappa, a.tau, key, needs_belief=False, n_dec=2000,
                           teacher=teacher, beta=beta, mix_rng=stream("mix", *mix_key, i), evaluate=False)
        packed.append(episode_arrays(r["history"], r["labels"], T))
        summ.append({"episode": int(i), "n_probes": r["n_probes"], "executed_teacher": r["executed_teacher"],
                     "actions": r["actions"], "a_policy": [lab["a_policy"] for lab in r["labels"]]})
    meta = {"args": vars(a), "env": _env(), "split": split, "episodes": [s["episode"] for s in summ], "status": status,
            "wall_s": time.time() - t0}
    if packed:
        save_shard(a.out + ".npz", packed, meta)
    with _open(a.out, ".json") as f:
        json.dump({**meta, "summary": summ}, f)
    print(f"LABEL3_DONE status={status} episodes={len(packed)} wall_s={time.time() - t0:.0f}")


def cmd_label3(a):
    """Round-0 G* rollouts (label3 split, kappa-keyed): every decision labelled with G*'s score vector (v3.0 C7)."""
    _label_loop(a, "label3", list(range(a.start, a.start + a.count)), lambda: None, 0.0, ("r0",))


def cmd_dagger3(a):
    """DAgger round r (dagger3 split, indices of v3.1 D1): the student acts, G* labels every visited belief; with
    probability beta the teacher's action is executed."""
    from .v3 import dagger_index
    st, _ = load_student(a.weights)
    idx = [dagger_index(a.round, a.seed, j) for j in range(a.start, a.start + a.count)]
    _label_loop(a, "dagger3", idx, lambda: st, a.beta, ("dagger", a.set, a.kappa, a.seed, a.round))


def cmd_distill3(a):
    """One distillation round on the aggregated shards (v3.0 C7): returns weights + per-epoch log."""
    from .distill import HP_GRID, BeliefStudent, DistillConfig, Student, load_shards, mean_regret, train_round
    from .nn import Adam
    lr, beta_T, lam, batch = HP_GRID[a.hp]
    cfg = DistillConfig(lr=lr, beta_T=beta_T, lam=lam, batch=batch, hidden=a.hidden, tau=a.tau, seed=a.seed,
                        budget_minutes=a.budget_minutes)
    paths = sorted(p for g in a.shards for p in glob.glob(g))
    vpaths = sorted(p for g in a.val_shards for p in glob.glob(g))
    D = load_shards(paths)
    V = load_shards(vpaths)
    rng = stream("distill3", a.set, a.kappa, a.seed, a.hp, a.kind, a.round)
    cls = BeliefStudent if a.kind == "belief" else Student
    if a.init:
        st, _ = load_student(a.init)
    else:
        st = cls(stream("init3", a.kind, a.seed, a.hp), hidden=a.hidden, tau=a.tau)
    opt = Adam(st.net.params(), lr=cfg.lr)
    log = []
    t0 = time.time()
    status = train_round(st, opt, D, np.arange(len(D["valid"])), V, np.arange(len(V["valid"])), cfg, rng, log, t0)
    final = mean_regret(st, V)
    meta = {"config": vars(a), "distill_config": cfg.__dict__, "hidden": a.hidden, "tau": a.tau, "env": _env(),
            "shards": paths, "val_shards": vpaths, "status": status, "final_val": final, "n_train_episodes":
            int(len(D["valid"])), "n_train_decisions": int(D["valid"].sum())}
    save_student(a.out + ".npz", st, meta)
    with _open(a.out, ".json") as f:
        json.dump({**meta, "log": log, "wall_s": time.time() - t0}, f)
    print(f"DISTILL3_DONE status={status} val_R_bar={final['R_bar']:.4f} wall_s={time.time() - t0:.0f}")


def cmd_latency3(a):
    from .latency3 import run_latency3
    from .v3 import require_v3_actions
    if not a.allow_32:
        require_v3_actions()
    st, _ = load_student(a.weights)
    recs, finals = run_latency3(a.set, a.kappa, a.tau, st, list(range(a.start, a.start + a.count)), split=a.split,
                                warmup=a.warmup, max_decisions=a.decisions + a.warmup)
    with _open(a.out, ".jsonl") as f:
        f.write(json.dumps({"header": True, "args": vars(a), "env": _env()}) + "\n")
        for r in recs:
            f.write(json.dumps(r) + "\n")
        for r in finals:
            f.write(json.dumps({"final": True, **r}) + "\n")
    print(f"LATENCY3_DONE decisions={len(recs)}")


def cmd_g1c(a):
    """G1′ (c): look-ahead estimator on the travel-notch control, one run per seed (B6 estimator settings)."""
    from .lookahead import lookahead_gap
    from .notch import prior_belief
    from .travel_notch import TravelNotchProblem, exact_values
    P = TravelNotchProblem(a.kappa)
    ex = exact_values(a.kappa)
    t0 = time.time()
    with _open(a.out, ".jsonl") as f:
        for sd in range(a.start, a.start + a.count):
            r = lookahead_gap(P, np.log(prior_belief()), P.start(), seed=7000 + sd, C1=a.C1, M_outer=a.M_outer)
            r.update({"part": "c", "seed": sd, "kappa": a.kappa, "exact_v_opt": ex["v_opt"],
                      "exact_v_greedy": ex["v_greedy"], "exact_gap_rel": ex["gap_rel"], "exact_a_opt": ex["a_opt"],
                      "exact_a_greedy": ex["a_greedy"]})
            f.write(json.dumps(r) + "\n"); f.flush()
    print(f"G1C_DONE wall_s={time.time() - t0:.0f}")


def cmd_g2v3(a):
    """G2′ / H3 (amendment v3.0 C12): one look-ahead estimate per g2v3 belief index (B6 estimator, code unchanged)."""
    from .g2 import g2_gap
    from .v3 import require_v3_actions
    require_v3_actions()
    t0 = time.time()
    with _open(a.out, ".jsonl") as f:
        f.write(json.dumps({"header": True, "args": vars(a), "env": _env()}) + "\n")
        for i in range(a.start, a.start + a.count):
            if time.time() - t0 > 0.8 * a.budget_minutes * 60:
                f.write(json.dumps({"EARLY_STOP_AT_80_PCT_BUDGET": True, "next_index": i}) + "\n")
                break
            r = g2_gap(a.set, a.kappa, a.tau, a.n_star, i, C1=a.C1, M_outer=a.M_outer, split="g2v3")
            f.write(json.dumps(r) + "\n"); f.flush()
    print(f"G2V3_DONE wall_s={time.time() - t0:.0f}")


def cmd_bias3(a):
    """G2′ bias check (07_hypotheses_v3 §3.4): full-G* reference value on g2v3 beliefs (touchbed/bias3.py)."""
    from .bias3 import bias_reference
    from .v3 import require_v3_actions
    require_v3_actions()
    t0 = time.time()
    with _open(a.out, ".jsonl") as f:
        f.write(json.dumps({"header": True, "args": vars(a), "env": _env()}) + "\n")
        for i in range(a.start, a.start + a.count):
            if time.time() - t0 > 0.8 * a.budget_minutes * 60:
                f.write(json.dumps({"EARLY_STOP_AT_80_PCT_BUDGET": True, "next_index": i}) + "\n")
                break
            r = bias_reference(a.set, a.kappa, a.tau, a.n_star, i, n_roll=a.n_roll)
            r["wall_s"] = time.time() - t0
            f.write(json.dumps(r) + "\n"); f.flush()
    print(f"BIAS3_DONE wall_s={time.time() - t0:.0f}")


def cmd_regrid3(a):
    """E′ (v3.0 C2): grid re-read of recorded eval3 episodes at another evaluator setting (histories rebuilt exactly
    from actions + the episode's observation stream)."""
    from .evaluate_v2 import prior_ball_mass
    from .gridpost import AdaptiveGridPosterior, rebuild_history
    from .v3 import ep_key_v3, require_v3_actions, states_v3
    require_v3_actions()
    om = ObsModel()
    recs = [json.loads(l) for f in a.src for l in open(f)]
    recs = [r for r in recs if "episode" in r and r["episode"] in set(a.episodes)]
    t0 = time.time()
    with _open(a.out, ".jsonl") as f:
        f.write(json.dumps({"header": True, "args": vars(a), "env": _env()}) + "\n")
        for j, r in enumerate(recs):
            if time.time() - t0 > 0.8 * a.budget_minutes * 60:
                f.write(json.dumps({"EARLY_STOP_AT_80_PCT_BUDGET": True,
                                    "remaining": [[q["method"], q["episode"]] for q in recs[j:]]}) + "\n")
                break
            lib, prior, eps = states_v3(r["set"], r["split"], [r["episode"]])
            s0, _ = eps[0]
            key = ep_key_v3(r["set"], r["split"], r["kappa"], r["tau"], r["episode"])
            h = rebuild_history(lib, om, s0, r["actions"], key)
            t1 = time.time()
            G = AdaptiveGridPosterior(lib, prior, om, h, s0, sub=a.sub)
            o = G.readout(s0, prior_ball_mass(lib, prior, s0))
            o.update({k: r[k] for k in ("episode", "set", "split", "kappa", "tau", "method", "actions")})
            o.update({"sub": a.sub, "wall_s": time.time() - t1, "orig_success": r["success"],
                      "orig_ball_info": r["ball_info"], "orig_identity_mass_true": r.get("identity_mass_true")})
            f.write(json.dumps(o) + "\n"); f.flush()
    print(f"REGRID3_DONE wall_s={time.time() - t0:.0f}")


def cmd_pilot3(a):
    """Mandatory TIME_ESTIMATE pilot (RESTRICTS pilot_required, <= 5 min): one episode per method and one labelled
    episode in one cell, then extrapolation to the sweep sizes of docs/08_experiment_plan_v3.yaml."""
    from .distill import Student
    from .policies_v2 import GStar
    from .v3 import ep_key_v3, require_v3_actions, run_episode_v3, states_v3
    if not a.allow_32:
        require_v3_actions()
    om = ObsModel()
    lib, prior, eps = states_v3(a.set, "pilot3", [0])
    s0, phi0 = eps[0]
    out = {"env": _env(), "set": a.set, "kappa": a.kappa, "tau": a.tau}
    t0 = time.time()
    key = ep_key_v3(a.set, "pilot3", a.kappa, a.tau, 0)
    r = run_episode_v3(None, lib, prior, om, s0, phi0, a.kappa, a.tau, key, needs_belief=False,
                       teacher=GStar(np.random.default_rng(0), M=64), evaluate=False)
    t_lab = time.time() - t0
    out["label_episode_s"] = t_lab
    out["label_decisions"] = r["n_probes"]
    t1 = time.time()
    from .gridpost import AdaptiveGridPosterior
    from .evaluate_v2 import prior_ball_mass
    G = AdaptiveGridPosterior(lib, prior, om, r["history"], s0, sub=4)
    G.readout(s0, prior_ball_mass(lib, prior, s0))
    out["grid_eval_s_gstar_like"] = time.time() - t1
    st = Student(np.random.default_rng(0), hidden=128, tau=a.tau)
    t2 = time.time()
    run_episode_v3(st, lib, prior, om, s0, phi0, a.kappa, a.tau, key, needs_belief=False, evaluate=False)
    out["student_episode_s_no_grid"] = time.time() - t2
    print(f"TIME_ESTIMATE: label {t_lab:.1f}s per G*-labelled episode ({r['n_probes']} decisions); "
          f"grid read-out {out['grid_eval_s_gstar_like']:.1f}s per episode; student rollout "
          f"{out['student_episode_s_no_grid']:.3f}s per episode (untrained, no grid)")
    for name, n_ep, per in (("round-0 labels per cell (1,500 ep)", 1500, t_lab),
                            ("G* pilot per cell (500 ep, label-free + grid)", 500, t_lab + out["grid_eval_s_gstar_like"])):
        print(f"TIME_ESTIMATE: {name}: {n_ep * per / 3600:.2f} CPU-h")
    out["wall_s"] = time.time() - t0
    with _open(a.out, ".json") as f:
        json.dump(out, f, indent=1)


def register(sub):
    def common(p, split=True):
        p.add_argument("--set", default="S"); p.add_argument("--kappa", type=float, default=12.0)
        p.add_argument("--tau", type=float, default=10.0); p.add_argument("--start", type=int, default=0)
        p.add_argument("--count", type=int, default=10); p.add_argument("--budget-minutes", type=float, default=25.0)
        p.add_argument("--allow-32", action="store_true", help="tests only: allow the 32 x 8 set")
        p.add_argument("--out", required=True)
        if split:
            p.add_argument("--split", default="pilot3")
    e = sub.add_parser("eval3"); common(e)
    e.add_argument("--method", required=True); e.add_argument("--weights", default=None)
    e.add_argument("--n-star", type=int, default=4); e.add_argument("--sub", type=int, default=4)
    e.add_argument("--no-grid", action="store_true")
    c = sub.add_parser("calib3"); common(c, split=False); c.add_argument("--n-star", type=int, default=4)
    lb = sub.add_parser("label3"); common(lb, split=False)
    dg = sub.add_parser("dagger3"); common(dg, split=False)
    dg.add_argument("--weights", required=True); dg.add_argument("--seed", type=int, required=True)
    dg.add_argument("--round", type=int, required=True); dg.add_argument("--beta", type=float, required=True)
    ds = sub.add_parser("distill3")
    ds.add_argument("--set", default="S"); ds.add_argument("--kappa", type=float, default=12.0)
    ds.add_argument("--tau", type=float, default=10.0); ds.add_argument("--hp", type=int, default=0)
    ds.add_argument("--seed", type=int, default=501); ds.add_argument("--round", type=int, default=0)
    ds.add_argument("--kind", default="history", choices=["history", "belief"]); ds.add_argument("--hidden", type=int, default=128)
    ds.add_argument("--shards", nargs="+", required=True); ds.add_argument("--val-shards", nargs="+", required=True)
    ds.add_argument("--init", default=None); ds.add_argument("--budget-minutes", type=float, default=330.0)
    ds.add_argument("--out", required=True)
    la = sub.add_parser("latency3"); common(la)
    la.add_argument("--weights", required=True); la.add_argument("--warmup", type=int, default=20)
    la.add_argument("--decisions", type=int, default=500)
    g = sub.add_parser("g1c")
    g.add_argument("--kappa", type=float, default=12.0); g.add_argument("--start", type=int, default=0)
    g.add_argument("--count", type=int, default=1); g.add_argument("--C1", type=int, default=32)
    g.add_argument("--M-outer", type=int, default=64); g.add_argument("--out", required=True)
    g2 = sub.add_parser("g2v3"); common(g2, split=False)
    g2.add_argument("--n-star", type=int, default=4); g2.add_argument("--C1", type=int, default=32)
    g2.add_argument("--M-outer", type=int, default=64)
    bz = sub.add_parser("bias3"); common(bz, split=False)
    bz.add_argument("--n-star", type=int, default=4); bz.add_argument("--n-roll", type=int, default=256)
    rg = sub.add_parser("regrid3")
    rg.add_argument("--src", nargs="+", required=True); rg.add_argument("--episodes", type=int, nargs="+", required=True)
    rg.add_argument("--sub", type=int, default=8); rg.add_argument("--out", required=True)
    rg.add_argument("--budget-minutes", type=float, default=25.0)
    p = sub.add_parser("pilot3")
    p.add_argument("--set", default="S"); p.add_argument("--kappa", type=float, default=12.0)
    p.add_argument("--tau", type=float, default=10.0); p.add_argument("--allow-32", action="store_true")
    p.add_argument("--out", required=True)
    return {"eval3": cmd_eval3, "calib3": cmd_calib3, "label3": cmd_label3, "dagger3": cmd_dagger3,
            "distill3": cmd_distill3, "latency3": cmd_latency3, "g1c": cmd_g1c, "g2v3": cmd_g2v3, "bias3": cmd_bias3, "regrid3": cmd_regrid3, "pilot3": cmd_pilot3}
