"""Number audit for a paper draft (stage 17/18/19 red line): every decimal number in the draft must match a value in
results/v3/results_v3.json (as written, x100 for percentages, sign-flipped, rounded to the shown precision) or appear
verbatim in a frozen design document. Usage: python tools_number_audit.py <draft.md> [<design doc> ...]
Prints the numbers that match neither; exit code 1 if any."""
import json
import os
import re
import sys

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)


def flat(x, out):
    if isinstance(x, dict):
        for v in x.values():
            flat(v, out)
    elif isinstance(x, list):
        for v in x:
            flat(v, out)
    elif isinstance(x, (int, float)) and not isinstance(x, bool):
        out.append(float(x))
    return out


def matches(tok, vals):
    s = tok.replace(",", "").replace("−", "-")
    try:
        v = float(s)
    except ValueError:
        return True
    dec = len(s.split(".")[1]) if "." in s else 0
    tol = 0.5 * 10 ** (-dec) + 1e-12
    for r in vals:
        for c in (r, -r, 100 * r, -100 * r, 1000 * r, r * 57.29577951308232):          # 1000: s -> ms; 57.3: rad -> deg
            if abs(c - v) <= tol:
                return True
    return False


def main():
    draft = open(sys.argv[1]).read()
    draft = re.sub(r"<!--.*?-->", "", draft, flags=re.S)                       # comments (figure prompt, counts)
    vals = flat(json.load(open(os.path.join(root, "results/v3/results_v3.json"))), [])
    vals = flat(json.load(open(os.path.join(root, "results/v2/12_g2_analysis.json"))), vals)   # previous-iteration H3
    design = " ".join(open(p).read() for p in sys.argv[2:])
    bad = []
    for m in re.finditer(r"(?<![\w.\[])[−-]?\d[\d,]*\.\d+", draft):          # decimals only; integers are counts/consts
        tok = m.group(0)
        if matches(tok, vals) or tok.lstrip("−-") in design:
            continue
        line = draft.count("\n", 0, m.start()) + 1
        bad.append((line, tok, draft[max(0, m.start() - 50):m.end() + 30].replace("\n", " ")))
    for b in bad:
        print(f"L{b[0]}: {b[1]}   …{b[2]}…")
    print(len(bad), "unmatched decimal numbers")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
