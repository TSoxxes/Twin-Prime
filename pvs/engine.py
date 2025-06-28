# pvs/engine.py
import numpy as np
import scipy.sparse as sp
from typing import Dict

def generate_spf_sieve(limit: int) -> np.ndarray:
    """
    Generates a Smallest Prime Factor (SPF) sieve array up to a given limit.
    """
    spf = np.arange(limit + 1, dtype=np.int64)
    if limit >= 0:
        spf[0] = -1
    if limit >= 1:
        spf[1] = -1
    if limit >= 4:
        spf[4::2] = 2
    for i in range(3, int(np.sqrt(limit)) + 1, 2):
        if spf[i] == i:
            spf[i*i::i] = np.where(spf[i*i::i] == np.arange(i*i, limit + 1, i), i, spf[i*i::i])
    return spf

def get_prime_factorization(n: int, spf_array: np.ndarray) -> Dict[int, int]:
    """
    Calculates the prime factorization of a number using a pre-computed SPF array.
    """
    if n <= 1:
        return {}
    factors: Dict[int, int] = {}
    limit = len(spf_array) - 1
    if n > limit:
        raise ValueError(f"Input number {n} exceeds the SPF sieve limit of {limit}.")
    while n > 1:
        prime_factor = int(spf_array[n])
        factors[prime_factor] = factors.get(prime_factor, 0) + 1
        n //= prime_factor
    return factors

def create_pvs_vector(
    n: int,
    spf_array: np.ndarray,
    prime_to_index_map: Dict[int, int]
) -> sp.csr_matrix:
    """
    Creates a sparse PVS vector for an integer n.
    """
    factorization = get_prime_factorization(n, spf_array)
    if not factorization:
        return sp.csr_matrix((1, len(prime_to_index_map)), dtype=np.int32)
    indices = []
    data = []
    for prime, exponent in factorization.items():
        if prime in prime_to_index_map:
            indices.append(prime_to_index_map[prime])
            data.append(exponent)
    num_non_zero = len(indices)
    indptr = [0, num_non_zero]
    return sp.csr_matrix(
        (data, indices, indptr),
        shape=(1, len(prime_to_index_map)),
        dtype=np.int32
    )