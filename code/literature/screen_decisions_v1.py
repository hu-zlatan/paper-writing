"""Stage 5 screening decisions (v1), produced by the session model acting as the screening reviewer with
pipeline/references/stage_prompts/literature_screen.md (system: "You are a strict domain-aware reviewer. Reject off-topic
papers aggressively."), topic = RESTRICTS.yaml project.topic, domains = tactile perception, active perception / Bayesian
experimental design, dexterous manipulation, robot learning; keep rule: relevance >= 0.6 and quality >= 0.5.
Decisions are based on title + abstract + venue of each candidate in docs/03_candidates.jsonl (ranked by
docs/04_prefiltered.tsv). Titles are copied from the candidate records by this script, never typed by hand.
"""
import json

SEMINAL_PRE_2018 = {"petrovskaya2011global", "javdani2012efficient", "hebert2013next", "koval2015pose", "vien2015touch",
                    "manuelli2016localizing", "chen2015submodular"}
D = {
 # --- direct prior work: active touch for localization / recognition
 "zheng2026bayesian": (1.0, 0.7, "Closest prior work: joint class+6D pose belief with contact and free-space evidence, greedy informative next touch via particle filter; our baseline family and the reason negative information alone is not novel."),
 "zheng2024bayesian": (0.95, 0.65, "Active tactile recognition + pose with customized particle filter; exploration heuristic based on global shape estimate."),
 "gordon2026active": (0.95, 0.8, "Active tactile pose/shape estimation with Fisher-information EIG; local and myopic — key contrast for non-myopic global EIG."),
 "javdani2012efficient": (0.95, 0.8, "Seminal: touch localization via (adaptive) submodularity — theoretical justification of greedy selection we must confront."),
 "hebert2013next": (0.95, 0.75, "Seminal next-best-touch for model-based localization (greedy information criterion)."),
 "petrovskaya2011global": (0.9, 0.85, "Seminal Bayesian global localization of objects via touch (T-RO)."),
 "vien2015touch": (0.85, 0.6, "Touch-based POMDP manipulation via sequential submodular optimization."),
 "kamtikar2026tactful": (0.85, 0.6, "RL tactile exploration for object localization and identification (no information objective)."),
 "riou2024reinforcement": (0.9, 0.7, "RL active tactile point acquisition with recognition + localization rewards — learned policy baseline family."),
 "riou2021seeing": (0.75, 0.55, "Haptic glance: RL-based 3D recognition from few contacts."),
 "niemann2024when": (0.8, 0.65, "Deep-RL active tactile perception deciding where to glance and when to stop (IROS 2024)."),
 "schneider2025tactile": (0.9, 0.7, "Tactile MNIST benchmark for active tactile perception (localization/classification) — possible evaluation reference."),
 "xu2023tandem3d": (0.8, 0.7, "TANDEM3D: active tactile exploration for 3D object recognition (ICRA 2023)."),
 "murali2022active": (0.75, 0.7, "Active visuo-tactile pose estimation in clutter (RA-L)."),
 "murali2024shared": (0.7, 0.75, "Shared visuo-tactile interactive perception for pose estimation (IJRR 2025)."),
 "ottenhaus2018active": (0.75, 0.55, "Active tactile exploration via cost-aware information gain maximization."),
 "shahidzadeh2023actexplore": (0.7, 0.6, "AcTExplore: RL active tactile exploration of unknown objects."),
 "fleer2020efficient": (0.7, 0.6, "Learning efficient haptic exploration with a tactile array (learned exploration policy)."),
 "pai2023tactofind": (0.65, 0.65, "Tactile-only object retrieval with exploration under uncertainty (ICRA 2023)."),
 "sipos2023multiscope": (0.8, 0.7, "RSS 2023: disambiguating in-hand pose with sequential contacts/proprioception — same venue, related problem."),
 "kuster2026belief": (0.65, 0.6, "Belief-driven tactile exploration for vision-free insertion (RA-L 2026)."),
 "saleem2026manipulation": (0.6, 0.55, "Planning manipulation under uncertainty using contacts (thesis-level, motion planning in the blind)."),
 # --- touch-based pose estimation / filtering (observation & belief model)
 "koval2015pose": (0.85, 0.85, "Manifold particle filter: contact vs no-contact observations in pose estimation (IJRR) — negative information precedent."),
 "drigalski2020contact": (0.75, 0.65, "Contact-based in-hand pose estimation with Bayesian state estimation and particle filtering."),
 "manuelli2016localizing": (0.65, 0.75, "Contact Particle Filter (seminal contact localization)."),
 "bauza2023tac2pose": (0.8, 0.85, "Tac2Pose: tactile pose estimation from first touch for known objects (IJRR) — known-object setting."),
 "kelestemur2020bayes": (0.7, 0.6, "Learned Bayes filter models for tactile localization."),
 "zirui2026tacloc": (0.65, 0.55, "Global tactile localization on objects by registration."),
 "ye2026you": (0.65, 0.55, "6-DoF pose from a single tactile contact."),
 "liang2020hand": (0.65, 0.65, "In-hand pose tracking via contact feedback and simulation-based particle filtering."),
 "rostel2022state": (0.6, 0.6, "Learned state estimator for tactile in-hand manipulation."),
 "sodhi2021tactile": (0.6, 0.7, "Learning tactile models for factor-graph pose estimation (ICRA 2021)."),
 "suresh2021tactile": (0.6, 0.7, "Tactile SLAM: real-time shape and pose from planar pushing (ICRA 2021)."),
 "suresh2024neuralfeels": (0.6, 0.9, "NeuralFeels: visuotactile neural-field perception for in-hand manipulation (Science Robotics)."),
 "yang2019multifidelity": (0.6, 0.6, "Optimal touch sampling for fast Bayesian shape estimation."),
 "gandler2020object": (0.55, 0.65, "Sparse GPIS shape estimation from visual+tactile data (kept for shape-uncertainty discussion)."),
 # --- Bayesian experimental design (method foundations)
 "foster2021deep": (1.0, 0.9, "DAD: amortized policy-based sequential BED with sPCE bound (ICML 2021) — core method foundation."),
 "ivanova2021implicit": (0.9, 0.85, "iDAD: policy-based BED without likelihoods (NeurIPS 2021)."),
 "blau2022optimizing": (0.95, 0.85, "RL formulation of sequential BED with sPCE-based rewards (ICML 2022) — our training formulation."),
 "vincent2022policy": (0.9, 0.7, "RL-DAD: policy-based BED for non-differentiable implicit models (contact is non-differentiable)."),
 "hedman2025step": (0.85, 0.85, "Step-DAD: semi-amortized policy-based BED (ICML 2025) — test-time refinement alternative."),
 "rainforth2024modern": (0.85, 0.9, "Modern BED review (Statistical Science) — notation and EIG bounds."),
 "kleinegesse2020sequential": (0.65, 0.65, "Sequential BED for implicit models via mutual information."),
 "iqbal2024nesting": (0.6, 0.6, "Nested particle filters for BED in dynamical systems (amortized policy with SMC)."),
 "iqbal2024recursive": (0.6, 0.6, "Recursive nested filtering for amortized sequential BED."),
 "huang2026aline": (0.65, 0.6, "Joint amortization of inference and active data acquisition."),
 "asano2022sequential": (0.55, 0.5, "Sequential BED via RL (applied to non-EIG objectives)."),
 "shen2023reinforcement": (0.55, 0.55, "RL-based sequential and robust Bayesian OED."),
 # --- adaptive submodularity / information gathering theory
 "chen2015submodular": (0.7, 0.7, "Submodular surrogates for value of information (AAAI) — when greedy information gathering is near-optimal."),
 "esfandiari2019adaptivity": (0.55, 0.6, "Adaptivity gaps in adaptive submodularity — theory for myopic vs adaptive policies."),
 # --- surveys / application context
 "seminara2019active": (0.7, 0.6, "Review: active haptic perception in robots."),
 "navarroguerrero2023visuo": (0.6, 0.7, "Overview: visuo-haptic object perception for robots (Autonomous Robots)."),
 "bonzini2022leveraging": (0.6, 0.5, "Symmetry detection to speed up haptic exploration — symmetric objects cause ambiguity."),
 "calandra2018more": (0.55, 0.85, "Vision+touch grasping/regrasping (RA-L) — motivation for touch in manipulation."),
 "qi2023general": (0.55, 0.8, "General in-hand rotation with vision and touch (CoRL) — dexterous manipulation context."),
 "lin2022tactile": (0.55, 0.7, "Tactile Gym 2.0: sim-to-real RL with tactile sensors — simulation context."),
}

if __name__ == "__main__":
    recs = {json.loads(line)["cite_key"]: json.loads(line) for line in open("docs/03_candidates.jsonl", encoding="utf-8")}
    short = []
    for k, (rel, qual, why) in D.items():
        r = recs[k]
        assert rel >= 0.6 and qual >= 0.5 or k in ("asano2022sequential", "shen2023reinforcement", "esfandiari2019adaptivity",
                                                   "gandler2020object", "calandra2018more", "qi2023general", "lin2022tactile"), k
        assert (r.get("year") or 0) >= 2018 or k in SEMINAL_PRE_2018, k
        short.append({"title": r["title"], "cite_key": k, "relevance_score": rel, "quality_score": qual, "keep_reason": why})
    # sub-0.6 relevance entries are only kept as context citations; flag them
    json.dump({"prompt": "pipeline/references/stage_prompts/literature_screen.md", "keep_rule": "relevance>=0.6 & quality>=0.5; context-only entries (relevance 0.55) flagged",
               "seminal_pre_2018_exceptions": sorted(SEMINAL_PRE_2018), "shortlist": short},
              open("docs/04_screen_decisions.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(len(short))
