# Latency protocol smoke test (dev, not a paper result)
Sandbox (2 vCPU, threads not pinned), untrained CategoricalDeepSets policy (protocol only), S, κ = 6, τ = 5.0, test
episode 0, 4 decisions. Per-decision latency (ms), y_t → a_{t+1}:
policy 0.45–0.57; R0 932–3399; R1 182–927; R2 245–442; R3 71–139; R4 72–77; R5 25–33; R6 15–30; R7 6–18.
The real measurement runs on one GitHub Actions runner, one thread, 20 warm-up + 500 timed decisions, with the
trained policy (main.py latency).
