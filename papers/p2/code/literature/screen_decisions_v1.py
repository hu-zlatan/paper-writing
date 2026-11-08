"""p2 stage 5 screening decisions (v1), produced by the session model acting as the screening reviewer with
pipeline/references/stage_prompts/literature_screen.md (system: "You are a strict domain-aware reviewer. Reject off-topic
papers aggressively."), topic = RESTRICTS.yaml project.topic, domains = tactile sensing, robotic grasping, conformal
prediction / uncertainty quantification, robot learning; keep rule: relevance >= 0.6 and quality >= 0.5.
Decisions use title + abstract + venue of candidates in docs/03_candidates.jsonl (ranked by docs/04_prefiltered.tsv and
a title search for the stage-2 strategies). Titles are copied from the candidate records by this script, never typed.
Rejected aggressively: sensor-hardware papers, prosthetics / neuro / human-physiology studies, conformal applications
outside robotics and control (LLMs, medicine, finance, energy), generic grasp-pose synthesis.
usage (from papers/p2): python code/literature/screen_decisions_v1.py
"""
import json

SEMINAL_PRE_2018 = {"vovk2005algorithmic", "lei2017distribution"}
D = {
 # --- grip force regulation and slip (SQ1, SQ3, SQ4)
 "almohammed2022switched": (0.9, 0.7, "Adaptive controller gripping novel objects with minimal force (slip velocities to zero); closest control-theoretic minimal-force baseline, no slip-rate guarantee."),
 "dong2019maintaining": (0.85, 0.7, "Keeps grasps within slipping bounds by monitoring incipient slip with a vision-based tactile sensor; reactive regulation baseline family."),
 "khamis2021real": (0.85, 0.65, "Grip force from real-time friction estimation (tactile) — friction-model × safety-margin baseline family."),
 "kuo2025tracing": (0.85, 0.65, "RA-L: learned tactile grasping-force control to reduce slippage under unknown mass/friction."),
 "boonstra2024estimate": (0.85, 0.6, "Learns incipient-slip estimates from touch to grasp gently (minimal force)."),
 "niu2026synchronized": (0.85, 0.55, "Particle-filter friction estimation + adaptive grasp control for gentle grasping; model-based minimal-force alternative."),
 "feng2026tactilereflex": (0.85, 0.55, "Tactile reflex anti-slip / force control with noise-statistics thresholds; no probabilistic guarantee (stage-1 seed)."),
 "lach2024zero": (0.8, 0.6, "IROS: tactile continuous grasp-force control policy trained in simulation, zero-shot to robot — sim-trained force control precedent."),
 "veiga2020grip": (0.8, 0.7, "Grip stabilization via per-finger tactile feedback control (slip prediction)."),
 "shang2026exp": (0.75, 0.5, "Pre-contact grasp-force selection (too little vs too much force); same decision variable, no guarantee."),
 "chen2018tactile": (0.8, 0.75, "Review: tactile friction estimation and incipient slip detection for dexterous grasping."),
 "romeo2020methods": (0.75, 0.75, "Survey of slip-detection methods and sensors in robotics."),
 "james2020slip": (0.75, 0.7, "Slip detection for grasp stabilisation with a multifingered tactile hand."),
 "berman2025autonomous": (0.7, 0.55, "Slip-triggered grip-force increase controller (threshold reflex), validated on a prosthetic hand; reactive baseline family."),
 "ayral2026reactive": (0.7, 0.55, "Reactive slip control in multifingered grasping with tactile sensing and internal-force optimisation."),
 "grover2022detect": (0.65, 0.6, "Learned slip detection from barometric tactile sensors (TCN) — slip label/detector context."),
 "willemet2024grip": (0.65, 0.65, "Human grip-force control under a sudden change of friction — motivates adaptation to friction shift."),
 # --- guarantees / risk in grasping (SQ3, positioning)
 "enwerem2026firmgrasp": (0.95, 0.55, "Closest guarantee-type work: CVaR friction risk margin under an assumed friction prior, offline grasp synthesis (stage-1 seed)."),
 "kim2024robust": (0.9, 0.6, "Tactile CBF safe grasping with bounded-disturbance (non-probabilistic) guarantees (stage-1 seed)."),
 "cortez2019control": (0.75, 0.75, "Control barrier functions for grasping (slip / force constraints) — deterministic guarantee contrast."),
 "enwerem2026variational": (0.65, 0.55, "Risk-sensitive (tail-aware) grasp execution under contact uncertainty; risk-measure contrast to distribution-free control."),
 "cloutier2018examining": (0.65, 0.55, "Robustness of grasp-force optimisation under parameter uncertainty (friction cone margins)."),
 # --- conformal prediction methods (SQ2, SQ5, SQ6)
 "vovk2005algorithmic": (0.8, 0.9, "Seminal: conformal prediction foundations (book)."),
 "lei2017distribution": (0.85, 0.9, "Seminal: split conformal regression, finite-sample marginal coverage."),
 "romano2019conformalized": (0.9, 0.85, "Conformalized quantile regression — the one-sided quantile calibration we use."),
 "angelopoulos2023conformal": (0.75, 0.85, "Tutorial on conformal prediction / risk control; notation and finite-sample bands."),
 "angelopoulos2022conformal": (0.95, 0.85, "Conformal risk control: bounds expected monotone loss — slip-rate control as risk control."),
 "angelopoulos2026conformal": (0.85, 0.7, "Conformal risk control for non-monotonic losses — fallback if slip is non-monotone in force (risk R1)."),
 "farinhas2023non": (0.7, 0.7, "Non-exchangeable conformal risk control — shift setting (SQ5)."),
 "gibbs2021adaptive": (0.95, 0.85, "Adaptive conformal inference: long-run coverage under arbitrary shift from the miscoverage indicator — online variant."),
 "gibbs2022conformal": (0.8, 0.75, "Dynamically-tuned ACI (step-size aggregation) — choice of γ (SQ5)."),
 "angelopoulos2023conformala": (0.75, 0.75, "Conformal PID control for online calibration — alternative online update."),
 "angelopoulos2024online": (0.75, 0.75, "Online conformal prediction with decaying step sizes — long-run and per-step guarantees."),
 "ge2024stochastic": (0.65, 0.6, "Online conformal prediction with semi-bandit (partial) feedback — related to binary slip feedback."),
 "bian2023training": (0.6, 0.7, "Training-conditional coverage — calibration-set-conditional validity (resampling design)."),
 "ding2023class": (0.6, 0.7, "Class-conditional conformal prediction — group-conditional coverage (SQ6)."),
 # --- conformal prediction in robotics / control (positioning, R6)
 "lekeufack2024conformal": (0.85, 0.75, "Conformal decision theory: risk-controlled decisions (not sets) from imperfect predictions in robotics — closest framing."),
 "lindemann2025formal": (0.8, 0.75, "Review: formal verification and control with conformal prediction in autonomous systems."),
 "dixit2022adaptive": (0.8, 0.7, "Adaptive conformal prediction for motion planning among dynamic agents — ACI in robotics."),
 "marques2026particle": (0.85, 0.55, "Particle-based conformal prediction for contact-aware planning (stage-1 seed); contact but not grip force."),
 "lindemann2023conformal": (0.65, 0.7, "Conformal prediction for STL runtime verification."),
 "ren2023robots": (0.65, 0.8, "Conformal prediction for calibrated LLM robot planners (ask for help)."),
 "huang2023conformal": (0.7, 0.55, "Conformal policy learning for sensorimotor control under distribution shift."),
 "strawn2023conformal": (0.65, 0.6, "Conformal predictive safety filter for RL controllers."),
 "zhang2024bayesian": (0.65, 0.65, "Online conformal prediction for safety guarantees in Bayesian optimisation (feedback-driven calibration)."),
 "zhao2024conformalized": (0.65, 0.55, "Conformalized interactive imitation learning under expert shift and intermittent feedback (online CP in robot learning)."),
 "kumar2026learnable": (0.6, 0.55, "ICRA: learnable conformal prediction for perception and planning uncertainty in robotics."),
 # --- tactile simulation and benchmarks (environment, R1, R5)
 "wang2022tacto": (0.6, 0.8, "TACTO vision-based tactile simulator — tactile simulation context."),
 "akinola2025tacsl": (0.6, 0.7, "TacSL visuotactile simulation and learning library."),
 "leins2025hydroelastictouch": (0.6, 0.55, "Tactile sensor simulation with hydroelastic contact — contact-model fidelity (sim-only threat)."),
 "luu2025manifeel": (0.6, 0.6, "Visuotactile policy-learning benchmark — 'does touch help' context for the ablation (stage-1 seed)."),
 "birtalan2026impact": (0.65, 0.5, "Tactile-sensor configuration vs grasp learning efficiency in simulation (stage-1 seed)."),
}


def main():
    recs = {json.loads(l)["cite_key"]: json.loads(l) for l in open("docs/03_candidates.jsonl", encoding="utf-8")}
    short = []
    for k, (rel, q, why) in D.items():
        r = recs[k]
        assert rel >= 0.6 and q >= 0.5, k
        assert (r.get("year") or 0) >= 2018 or k in SEMINAL_PRE_2018, k
        short.append({"title": r["title"], "cite_key": k, "relevance_score": rel, "quality_score": q, "keep_reason": why})
    out = {"prompt": "pipeline/references/stage_prompts/literature_screen.md", "keep_rule": "relevance>=0.6 & quality>=0.5",
           "seminal_pre_2018_exceptions": sorted(SEMINAL_PRE_2018), "n_candidates": len(recs), "shortlist": short}
    json.dump(out, open("docs/04_screen_decisions.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(len(short), "kept of", len(recs))


if __name__ == "__main__":
    main()
