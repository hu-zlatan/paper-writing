# p2 stage 12 increment 1: main-pool labels (protocol rd). Usage: bash run_labels_v1.sh A|B  (two halves, run in parallel)
set -e
cd "$(dirname "$0")"
O=../results/v1/labels
L="python main.py label --protocol rd --budget-minutes 100"
if [ "$1" = A ]; then
  for f in F1 F2; do $L --pool id --family $f --start 0 --count 500 --out $O/id_$f; done
  for sh in S1 S1m S3; do $L --pool id --family F1 --start 325 --count 175 --shift $sh --out $O/id_F1_$sh; $L --pool id --family F2 --start 325 --count 175 --shift $sh --out $O/id_F2_$sh; done
  $L --pool s2 --family F5 --start 0 --count 275 --out $O/s2_F5_000
else
  for f in F3 F4; do $L --pool id --family $f --start 0 --count 500 --out $O/id_$f; done
  for sh in S1 S1m S3; do $L --pool id --family F3 --start 325 --count 175 --shift $sh --out $O/id_F3_$sh; $L --pool id --family F4 --start 325 --count 175 --shift $sh --out $O/id_F4_$sh; done
  $L --pool s2 --family F5 --start 275 --count 275 --out $O/s2_F5_275
fi
echo DONE_$1
