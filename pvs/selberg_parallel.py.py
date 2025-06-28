"""
pvs_selberg.py  –  Compute squared Selberg weights W(n;x) in parallel
=====================================================================

Author :  <your name>      Date :  2025-06-28
Licence:  MIT

Run `python pvs_selberg.py -h`  for CLI options.
"""

from __future__ import annotations
import argparse, math, sys, time, logging, os
from typing import List, Tuple
from multiprocessing import Pool, cpu_count

import numpy as np
import pandas as pd            # Parquet writer
try:
    from tqdm import tqdm      # optional nice progress bar
    TQDM = True
except ImportError:
    TQDM = False


# ----------------------------------------------------------------------
# 1.  Sieve utilities
# ----------------------------------------------------------------------
def build_spf_and_mobius(limit: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Build arrays:
      spf[i]  = smallest prime factor of i   (i >= 2)
      mu[i]   = Möbius μ(i)
    limit inclusive.  Complexity O(limit log log limit).
    """
    spf = np.zeros(limit + 1, dtype=np.int32)
    mu  = np.ones (limit + 1, dtype=np.int8)   # μ(1) = 1
    for i in range(2, limit + 1):
        if spf[i] == 0:            # i is prime
            spf[i] = i
            mu[i]  = -1            # single prime factor → (-1)^1
            # mark multiples
            step = i
            for j in range(i * i, limit + 1, step):
                if spf[j] == 0:
                    spf[j] = i
    # second pass: complete μ via factorisation parity
    for i in range(2, limit + 1):
        p = spf[i]
        q = i // p
        if q % p == 0:             # square factor ⇒ μ = 0
            mu[i] = 0
        else:
            mu[i] = -mu[q]
    return spf, mu


# ----------------------------------------------------------------------
# 2.  Weight for ONE n (uses pre-computed μ array)
# ----------------------------------------------------------------------
def selberg_weight_squared(n: int, R: int, mu: np.ndarray) -> float:
    """
    Return W(n) = w_trad(n)^2  with  w_trad(n) = Σ_{d|n, d≤R} μ(d) log(R/d)
    Assumes: 2 ≤ n,  R ≥ 1,  μ array covers up to R.
    """
    total = 0.0
    d = 1
    root = int(math.isqrt(n))
    while d <= root:
        if n % d == 0:
            e = n // d
            # iterate over the two paired divisors d and e
            if d <= R and mu[d]:
                total += mu[d] * math.log(R / d)
            if e != d and e <= R and mu[e]:
                total += mu[e] * math.log(R / e)
        d += 1
    return total * total     # square at the end


# ----------------------------------------------------------------------
# 3.  Worker helper – processes a block of integers
# ----------------------------------------------------------------------
def _process_block(args):
    start, end, R, mu = args
    data = np.empty(end - start, dtype=np.float64)
    for idx, n in enumerate(range(start, end)):
        data[idx] = selberg_weight_squared(n, R, mu)
    return start, data


# ----------------------------------------------------------------------
# 4.  CLI + driver
# ----------------------------------------------------------------------
def main():
    p = argparse.ArgumentParser(
        description="Compute squared Selberg weights W(n;x) on [2,x].")
    p.add_argument("--x",        type=int,   required=True,
                   help="Upper bound for n (inclusive).  E.g. 1000000.")
    p.add_argument("--delta",    type=float, default=0.05,
                   help="δ in R = x^(1/2 - δ).  Default 0.05.")
    p.add_argument("--chunksize",type=int,   default=2_000_000,
                   help="How many n each worker tackles at a time.")
    p.add_argument("--workers",  type=int,   default=cpu_count(),
                   help="Parallel workers (default = CPU cores).")
    p.add_argument("--outfile",  type=str,   default="weights.parquet",
                   help="Parquet file to write <n, W> rows.")
    args = p.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )

    x = args.x
    if x < 10:
        logging.error("x should be at least 10.")
        sys.exit(1)

    R = int(round(x ** (0.5 - args.delta)))
    logging.info(f"Parameters: x={x:,}  δ={args.delta}  R={R:,}")

    # -- Pre-compute μ up to R
    logging.info(f"Building SPF & Möbius arrays up to R …")
    t0 = time.time()
    spf, mu = build_spf_and_mobius(R)
    logging.info(f"  done in {time.time()-t0:.2f} s")

    # -- Prepare blocks
    starts = list(range(2, x + 1, args.chunksize))
    blocks = [(s, min(s + args.chunksize, x + 1), R, mu) for s in starts]
    total_n = x - 1

    # -- Multiprocessing
    logging.info(f"Launching pool with {args.workers} worker(s)…")
    with Pool(processes=args.workers) as pool, \
         pd.ExcelWriter(args.outfile, engine='pyarrow', mode='wb') as writer:  # ensure Parquet engine available
        iterator = pool.imap_unordered(_process_block, blocks)
        if TQDM: iterator = tqdm(iterator, total=len(blocks), desc="Blocks")
        for start_idx, arr in iterator:
            # write each block as a Parquet fragment
            df = pd.DataFrame({
                "n": np.arange(start_idx, start_idx + len(arr), dtype=np.uint64),
                "W": arr
            })
            # append to Parquet file (row-group per block)
            df.to_parquet(writer, index=False, compression="zstd")
    logging.info(f"All done – results in  {args.outfile}")

# ----------------------------------------------------------------------
if __name__ == "__main__":
    main()
