# pvs/weights.py
import numpy as np

def mobius_mu_sieve(limit: int) -> np.ndarray:
    """
    Generates Möbius function values up to a limit using a sieve.
    mu(n) = 1 if n is a square-free with an even number of prime factors.
    mu(n) = -1 if n is a square-free with an odd number of prime factors.
    mu(n) = 0 if n has a squared prime factor.
    """
    mu = np.ones(limit + 1, dtype=int)
    is_prime = np.ones(limit + 1, dtype=bool)
    mu[0] = 0
    is_prime[0:2] = False

    for i in range(2, limit + 1):
        if is_prime[i]:
            mu[i::i] *= -1
            mu[i*i::i*i] = 0
            is_prime[i*i::i] = False
    return mu

def get_divisors(n: int) -> list[int]:
    """Gets all divisors of a number n."""
    divs = set()
    for i in range(1, int(np.sqrt(n)) + 1):
        if n % i == 0:
            divs.add(i)
            divs.add(n//i)
    return list(divs)

def simplified_sieve_weight(n: int, R: float, mu: np.ndarray) -> float:
    """
    Calculates a simplified sieve weight for an integer n.
    This is inspired by GPY/Maynard-Tao weights of the form (sum lambda_d)^2
    where lambda_d is related to the Mobius function and a smooth function.
    Weight(n) = (sum_{d|n, d<R} mu(d) * log(R/d))^2
    """
    if n <= 0:
        return 0.0

    divisors = get_divisors(n)
    lambda_sum = 0.0
    for d in divisors:
        if d < R:
            # Ensure mu array is large enough
            if d < len(mu):
                lambda_sum += mu[d] * np.log(R / d)
            else:
                # This case should be avoided by pre-calculating a large enough mu sieve
                pass 

    return lambda_sum**2