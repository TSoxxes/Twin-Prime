# pvs_runner.py (Final Version with Hybrid Weight)
import argparse
import time
from pathlib import Path

import numpy as np
import pandas as pd
from tqdm import tqdm

from pvs.engine import (create_pvs_vector, generate_spf_sieve)
from pvs.weights import mobius_mu_sieve, simplified_sieve_weight

# --- Invariant Calculation Functions ---
def calculate_l1_norm(pvs_vector):
    """Calculates L1 norm (Omega), the total number of prime factors."""
    return int(pvs_vector.sum())

def calculate_displacement_norm(vec):
    """Calculates the L1 norm of the displacement vector."""
    return int(np.abs(vec.data, dtype=np.int64).sum())

def calculate_signed_l1_norm(pvs_vector):
    """Calculates a parity-sensitive signed L1 norm based on Omega(n)."""
    l1 = calculate_l1_norm(pvs_vector)
    parity = (-1)**l1
    return l1 * parity

def calculate_l0_norm(pvs_vector):
    """Calculates L0 norm (omega), the number of distinct prime factors."""
    return pvs_vector.getnnz()

def calculate_booster(delta_norm):
    """
    Applies a smooth, Gaussian booster based on the delta_l1_norm.
    This function is maximized when delta_norm is 2.
    """
    # The 'sharpness' of the peak can be tuned by multiplying the exponent.
    # A larger multiplier makes the peak narrower. We'll start with 1.0.
    sharpness = 1.0
    return np.exp(-sharpness * (delta_norm - 2)**2)

# --- Main Script Functions ---
def get_cli_args():
    parser = argparse.ArgumentParser(
        description="PVS Twin Prime Conjecture Computational Analysis Engine.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-n", "--max-n", type=int, default=1_000_000,
        help="The upper limit for number generation and analysis."
    )
    parser.add_argument(
        "-o", "--output-dir", type=str, default="./data/processed",
        help="Directory to save the output Parquet files."
    )
    parser.add_argument(
        "-c", "--cache-dir", type=str, default="./data/cache",
        help="Directory to store and load cached files like the SPF sieve."
    )
    parser.add_argument(
        "-f", "--force-regenerate", action="store_true",
        help="Force regeneration of the SPF sieve even if cached."
    )
    return parser.parse_args()

def main():
    args = get_cli_args()
    print(f"Starting PVS analysis with max_n = {args.max_n}")

    Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    Path(args.cache_dir).mkdir(parents=True, exist_ok=True)

    sieve_limit = args.max_n + 2
    sieve_cache_path = Path(args.cache_dir) / f"spf_sieve_{sieve_limit}.npy"

    from pvs.engine import generate_spf_sieve as robust_sieve
    if not sieve_cache_path.exists() or args.force_regenerate:
        print(f"Generating SPF sieve up to {sieve_limit}...")
        start_time = time.time()
        spf_array = robust_sieve(sieve_limit)
        np.save(sieve_cache_path, spf_array)
        duration = time.time() - start_time
        print(f"SPF sieve generated and cached in {duration:.2f} seconds.")
    else:
        print(f"Loading cached SPF sieve from {sieve_cache_path}...")
        spf_array = np.load(sieve_cache_path)
        print("SPF sieve loaded successfully.")

    sieve_R = int(args.max_n ** 0.25)
    print(f"Calculating Mobius mu function up to R = {sieve_R}...")
    mu_sieve = mobius_mu_sieve(sieve_R)

    primes = [i for i, p_val in enumerate(spf_array) if i > 1 and i == p_val]
    prime_to_index_map = {p: i for i, p in enumerate(primes)}
    prime_set = set(primes)
    print(f"Found {len(primes)} primes up to {sieve_limit}.")

    results = []
    for p in tqdm(primes, desc="Analyzing primes"):
        if p + 2 > args.max_n:
            break
        
        n, n_plus_2 = p, p + 2
        nu_n = create_pvs_vector(n, spf_array, prime_to_index_map)
        nu_n_plus_2 = create_pvs_vector(n_plus_2, spf_array, prime_to_index_map)
        is_p_plus_2_prime = (n_plus_2 in prime_set)
        
        displacement_vec = nu_n_plus_2 - nu_n
        delta_norm = calculate_displacement_norm(displacement_vec)
        
        # Calculate the hybrid weight
        sieve_weight = simplified_sieve_weight(n_plus_2, sieve_R, mu_sieve)
        booster = calculate_booster(delta_norm)
        hybrid_weight = sieve_weight * booster

        results.append({
            'p': n,
            'is_p_plus_2_prime': is_p_plus_2_prime,
            'l1_norm_p2': calculate_l1_norm(nu_n_plus_2),
            'signed_l1_norm_p2': calculate_signed_l1_norm(nu_n_plus_2),
            'l0_norm_p2': calculate_l0_norm(nu_n_plus_2),
            'delta_l1_norm': delta_norm,
            'sieve_weight_p2': sieve_weight,
            'hybrid_weight': hybrid_weight
        })

    if not results:
        print("Warning: No results generated. Check max_n parameter.")
        return

    df = pd.DataFrame(results)
    output_file = Path(args.output_dir) / f"pvs_analysis_max_n_{args.max_n}.parquet"
    df.to_parquet(output_file, engine='pyarrow', compression='snappy')
    print(f"\nAnalysis complete. Results saved to {output_file}")
    print("\nFirst 5 rows of the generated data:")
    print(df.head())

if __name__ == "__main__":
    main()