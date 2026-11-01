#!/bin/bash
# round-0 S2 students (amendment v4.0 E2): train shards 0-1,199 + 1,500-2,999, val 1,200-1,499, 200 fixed epochs
cd /home/claude/paper-writing/code
S=$1
L=../results/v4/labels
TR=""; VA=""
for i in $(seq 0 50 2950); do f=$(printf "$L/S_k2_r0_s%04d.npz" $i); if [ $i -ge 1200 ] && [ $i -lt 1500 ]; then VA="$VA $f"; else TR="$TR $f"; fi; done
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 main.py distill3 --set S --kappa 2 --tau 4.7 --hp 0 --seed $S --round 0 --shards $TR --val-shards $VA --budget-minutes 120 --fixed-epochs 200 --out /tmp/claude-0/d4/S_k2_s${S}_r0
