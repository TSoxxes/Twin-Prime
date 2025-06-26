import numpy as np
from scipy.sparse import csr_matrix

def sieve_of_eratosthenes(limit: int) -> np.ndarray:
    """
    Generates all prime numbers up to a given limit using the Sieve of Eratosthenes.

    Args:
        limit (int): The upper limit (inclusive) for prime generation.

    Returns:
        np.ndarray: A boolean array where `primes[i]` is True if `i` is prime.
                    The array has size `limit + 1`.
    """
    if limit < 0:  # Handle negative limit
        return np.array([], dtype=bool)
    if limit < 2:
        return np.zeros(limit + 1, dtype=bool)

    primes = np.ones(limit + 1, dtype=bool)
    primes[0:2] = False  # 0 and 1 are not prime
    for i in range(2, int(np.sqrt(limit)) + 1):
        if primes[i]:
            primes[i*i:limit+1:i] = False
    return primes

def build_prime_vector(n: int) -> csr_matrix:
    """
    Builds a sparse prime vector up to n.

    Args:
        n (int): The upper limit for the prime vector.

    Returns:
        scipy.sparse.csr_matrix: A sparse matrix representing the prime vector.
    """
    if n > 1e8:
        # Placeholder for segmenting logic for larger n
        print("Warning: n > 1e8, segmenting logic not yet implemented.")
        # Fallback to current implementation for now

    primes = sieve_of_eratosthenes(n)
    prime_indices = np.where(primes)[0]

    # Create a sparse matrix (CSR format for efficient row slicing)
    # The matrix will have 1 row and n+1 columns
    # It will have a 1 at each prime index
    num_primes = len(prime_indices)
    data = np.ones(num_primes, dtype=int)
    row_ind = np.zeros(num_primes, dtype=int)
    col_ind = prime_indices

    prime_vector = csr_matrix((data, (row_ind, col_ind)), shape=(1, n + 1))

    return prime_vector
