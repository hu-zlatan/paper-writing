#!/bin/bash
# DAgger round k S2 students (amendment v4.0 E2): aggregated data = round-0 label shards (0-1,199 + 1,500-2,999) +
# this seed's DAgger shards of rounds 1..k; val = label shards 1,200-1,499; warm start from round k-1; 200 fixed epochs.
# Usage: v4_distill_rk.sh <seed> <k> <outdir>
cd /home/claude/paper-writing/code
S=$1; K=$2; O=$3
L=../results/v4/labels; D=../results/v4/d4
TR=""; VA=""
for i in $(seq 0 50 2950); do f=$(printf "$L/S_k2_r0_s%04d.npz" $i); if [ $i -ge 1200 ] && [ $i -lt 1500 ]; then VA="$VA $f"; else TR="$TR $f"; fi; done
for r in $(seq 1 $K); do TR="$TR $(ls $D/S_k2_s${S}_r${r}_[0-9][0-9][0-9]*.npz | tr '\n' ' ')"; done
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 main.py distill3 --set S --kappa 2 --tau 4.7 --hp 0 --seed $S --round $K \
  --shards $TR --val-shards $VA --init $D/S_k2_s${S}_r$((K-1)).npz --budget-minutes 120 --fixed-epochs 200 --out $O/S_k2_s${S}_r$K
