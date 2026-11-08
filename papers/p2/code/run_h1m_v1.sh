# p2 stage 12: H1-M grids (frozen design h1m). 800 id train instances (objects 0-49 x 4 families x 4 dist) + 100 per
# shift pool (S1 / S3 on id objects 325-349 of F1; s2 objects 0-24). Usage: bash run_h1m_v1.sh A|B
set -e
cd "$(dirname "$0")"
O=../results/v1/mono
M="python main.py mono --design h1m --protocol rd --budget-minutes 100"
if [ "$1" = A ]; then
  for f in F1 F2; do $M --pool id --family $f --start 0 --count 50 --out $O/id_$f; done
  $M --pool id --family F1 --start 325 --count 25 --shift S1 --out $O/id_F1_S1
  $M --pool s2 --family F5 --start 0 --count 25 --out $O/s2_F5
else
  for f in F3 F4; do $M --pool id --family $f --start 0 --count 50 --out $O/id_$f; done
  $M --pool id --family F1 --start 325 --count 25 --shift S3 --out $O/id_F1_S3
fi
echo DONE_$1
