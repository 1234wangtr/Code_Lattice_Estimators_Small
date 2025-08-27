#!/usr/bin/env python3
"""
estimate_sis.py

Estimate SIS "complexity" following the logic translated from provided C++ snippet.

Usage:
    python estimate_sis.py --n 512 --q 4096 --bound 0.05

Notes / assumptions:
 - 'paraq' in the C++ snippet -> q (command-line arg)
 - 'paran' in the C++ snippet -> n (command-line arg)
 - We loop parab in range(100, 2*n, step=20) as in the snippet.
 - Numerical stability: probability products are handled in log2-space where possible.
 - Outputs:
     res_b: the parab value that gave minimal "complex" (tfz)
     complex: minimal tfz found
     classical_equiv = complex / 0.292 * classical_factor
     quantum_equiv   = complex / 0.292 * quantum_factor
 - Default classical_factor=1.0, quantum_factor=0.265 (you can change these).
"""
import math
import argparse
import sys

def safe_log2(x):
    # handle tiny or non-positive values
    if x <= 0.0:
        return float("-inf")
    return math.log2(x)

def estimate_sis(n:int, q:float, bound:float,
                 classical_factor:float=1.0,
                 quantum_factor:float=0.265):
    pi = 3.14159265358979323846
    e = 2.71828182845904523536

    d = n  # loop in original code is for (d = n; d <= n; d++) so single value
    best_complex = float("inf")
    res_b = 0

    # protect logs
    log2_q = math.log(q, 2) if q > 1.0 else 0.0

    for parab in range(100, 2 * d, 20):
        # compute paras
        # paras = log(parab / 2 / pi / e * (pi * parab)^(1/parab)) / log(2) / (parab - 1)
        # implement carefully
        if parab - 1 <= 0:
            continue
        try:
            term = (parab / 2.0 / pi / e) * ((pi * parab) ** (1.0 / parab))
            if term <= 0.0:
                # numerical issue, skip
                continue
            paras = math.log(term) / math.log(2.0) / (parab - 1.0)
        except Exception:
            continue

        # avoid zero/negative paras
        if paras <= 0.0:
            # skip this parab because paras used as divisor later
            continue

        # jpi calculation (as in snippet)
        # jpi = int(floor(log(paraq) / log(2) / paras))
        if paras == 0.0:
            continue
        try:
            jpi = int(math.floor(log2_q / paras))
        except Exception:
            jpi = 0

        # ii calculation:
        # ii = int(n - jpi + (1 + jpi) * jpi * paras / 2 / (log(paraq) / log(2)))
        denom = log2_q if log2_q != 0.0 else 1e-300
        ii_float = n - jpi + (1.0 + jpi) * jpi * paras / 2.0 / denom
        ii = int(math.floor(ii_float))

        if ii < 0:
            ii = 0
            # jj uses quadratic formula in snippet:
            # jj = int((-1 * paras + sqrt(paras^2 + 8 * paras * paran * log(paraq) / log(2))) / 2 / paras)
            disc = paras * paras + 8.0 * paras * n * log2_q
            if disc < 0.0:
                continue
            jj_float = (-paras + math.sqrt(disc)) / (2.0 * paras)
            jj = int(math.floor(jj_float))
        else:
            jj = ii + int(jpi)

        # ensure indices meaningful
        if jj < ii:
            jj = ii

        length = jj - ii
        if length < 0:
            length = 0

        # compute lk, sigma, d1, then probability pro
        lk = paras * float(length)
        # sigma = 2^lk / sqrt(jj-ii+1)
        # but we will use logs
        # sigma = pow(2, lk) / sqrt(length + 1)
        if length + 1 <= 0:
            continue
        try:
            log2_sigma = lk - 0.5 * math.log2(length + 1)
        except ValueError:
            continue

        # d1 = bound / sigma / sqrt(2)
        # in log-space: log2(d1) = log2(bound) - log2(sigma) - log2(sqrt(2))
        if log2_sigma == float("-inf"):
            continue
        if bound <= 0.0:
            continue

        log2_bound = math.log2(bound) if bound > 0 else float("-inf")
        log2_sqrt2 = 0.5 * math.log2(2.0)
        log2_d1 = log2_bound - log2_sigma - log2_sqrt2

        # convert back to numeric d1 (we need numeric for erf)
        # but protect overflow/underflow
        try:
            d1 = 2 ** log2_d1
        except OverflowError:
            d1 = float("inf") if log2_d1 > 0 else 0.0
        except Exception:
            d1 = 0.0

        # erf(d1) in (0,1) for d1>0. Use math.erf
        erf_val = math.erf(d1)
        # In extremely small d1, erf_val ~ small, so log2 might be -inf — handle
        if erf_val <= 0.0:
            # probability effectively zero -> pro very small
            log2_pro_part1 = float("-inf")
        else:
            log2_pro_part1 = (length) * math.log2(erf_val)  # (jj-ii) * log2(erf(d1))

        # if ii>0 multiply by (bound / q)^ii
        if ii > 0:
            if q <= 0 or bound <= 0:
                log2_pro_part2 = float("-inf")
            else:
                log2_pro_part2 = ii * (math.log2(bound) - math.log2(q))
        else:
            log2_pro_part2 = 0.0

        # total log2(pro)
        if log2_pro_part1 == float("-inf") or log2_pro_part2 == float("-inf"):
            log2_pro = float("-inf")
        else:
            log2_pro = log2_pro_part1 + log2_pro_part2

        # oo = 0.2075 * parab + log2(pro)
        if log2_pro == float("-inf"):
            oo = float("-inf")
        else:
            oo = 0.2075 * parab + log2_pro

        # tfz = 0.292 * parab; if oo < 0 then tfz = tfz - oo  (note: oo can be negative)
        tfz = 0.292 * parab
        if oo != float("-inf") and oo < 0.0:
            tfz = tfz - oo

        # update best
        if tfz < best_complex:
            best_complex = tfz
            res_b = parab

    if best_complex == float("inf"):
        raise RuntimeError("No valid parab found — check parameters (n, q, bound) for numeric issues.")

    classical_equiv = best_complex
    quantum_equiv = best_complex / 0.292 * 0.265

    return {
        "n": n,
        "q": q,
        "bound": bound,
        "res_b": res_b,
        "complex": best_complex,
        "classical_equiv": classical_equiv,
        "quantum_equiv": quantum_equiv
    }

def main():
    parser = argparse.ArgumentParser(description="Estimate SIS complexity (Python translation).")
    parser.add_argument("--n", type=int, required=True, help="dimension n (paran)")
    parser.add_argument("--q", type=float, required=True, help="modulus q (paraq)")
    parser.add_argument("--bound", type=float, required=True, help="bound (deviation)")
    parser.add_argument("--classical-factor", type=float, default=1.0, help="scale for classical equivalence")
    parser.add_argument("--quantum-factor", type=float, default=0.265, help="scale for quantum equivalence")
    args = parser.parse_args()

    try:
        out = estimate_sis(args.n, args.q, args.bound,
                           classical_factor=args.classical_factor,
                           quantum_factor=args.quantum_factor)
    except Exception as e:
        print("ERROR during estimation:", e, file=sys.stderr)
        sys.exit(2)

    # print results human-friendly
    print("SIS estimation results:")
    print(f"  n = {out['n']}, q = {out['q']}, bound = {out['bound']}")
    print(f"  best res_b (block size) = {out['res_b']}")
    print(f"  minimal 'complex' (tfz) = {out['complex']:.6f}")
    print(f"  classical equivalent (approx) = {out['classical_equiv']:.6f}")
    print(f"  quantum equivalent  (approx) = {out['quantum_equiv']:.6f}")

if __name__ == "__main__":
    main()
