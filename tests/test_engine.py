# tests/test_engine.py
import pytest
import numpy as np
from pvs.engine import generate_spf_sieve, get_prime_factorization

@pytest.fixture(scope="module")
def spf_sieve_100():
    """Generates a shared SPF sieve for all tests in this module."""
    return generate_spf_sieve(100)

def test_generate_spf_sieve():
    sieve = generate_spf_sieve(20)
    assert sieve[2] == 2
    assert sieve[3] == 3
    assert sieve[4] == 2  # Smallest prime factor of 4 is 2
    assert sieve[9] == 3
    assert sieve[15] == 3
    assert sieve[17] == 17
    assert sieve[0] == -1
    assert sieve[1] == -1

def test_get_prime_factorization_basic(spf_sieve_100):
    factors_12 = get_prime_factorization(12, spf_sieve_100)
    assert factors_12 == {2: 2, 3: 1}

    factors_35 = get_prime_factorization(35, spf_sieve_100)
    assert factors_35 == {5: 1, 7: 1}

    factors_99 = get_prime_factorization(99, spf_sieve_100)
    assert factors_99 == {3: 2, 11: 1}

    factors_17 = get_prime_factorization(17, spf_sieve_100)
    assert factors_17 == {17: 1}

def test_get_prime_factorization_edge_cases(spf_sieve_100):
    assert get_prime_factorization(0, spf_sieve_100) == {}
    assert get_prime_factorization(1, spf_sieve_100) == {}
    assert get_prime_factorization(2, spf_sieve_100) == {2: 1}

def test_get_prime_factorization_limit_error(spf_sieve_100):
    with pytest.raises(ValueError, match="exceeds the SPF sieve limit"):
        get_prime_factorization(101, spf_sieve_100)