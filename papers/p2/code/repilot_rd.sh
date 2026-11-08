set -e
O=../results/pilot/rd
for f in F1 F2 F3 F4; do python main.py label --pool pilot --family $f --start 125 --count 100 --protocol rd --budget-minutes 120 --out $O/labels/pilot_$f; done
python main.py label --pool pilot --family F5 --start 125 --count 100 --protocol rd --budget-minutes 120 --out $O/labels/pilot_F5
for sh in S1 S3; do for f in F1 F2 F3 F4; do python main.py label --pool pilot --family $f --start 125 --count 100 --shift $sh --protocol rd --budget-minutes 120 --out $O/labels/pilot_${f}_$sh; done; done
for f in F1 F2 F3 F4 F5; do python main.py mono --pool pilot --family $f --start 125 --count 7 --protocol rd --budget-minutes 120 --out $O/mono/pilot_$f; done
echo ALLDONE
