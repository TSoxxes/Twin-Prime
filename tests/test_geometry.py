import pytest
import numpy as np
from scipy.sparse import csr_matrix
from pvs.geometry import sieve_of_eratosthenes, build_prime_vector

def test_sieve_of_eratosthenes_basic():
    primes = sieve_of_eratosthenes(10)
    expected = np.array([False, False, True, True, False, True, False, True, False, False, False])
    assert np.array_equal(primes, expected)

def test_sieve_limit_cases():
    sieve_at_1 = sieve_of_eratosthenes(1)
    assert sieve_at_1.shape == (2,)  # 0, 1
    assert not sieve_at_1[0] and not sieve_at_1[1]

    sieve_at_0 = sieve_of_eratosthenes(0)
    assert sieve_at_0.shape == (1,)  # 0
    assert not sieve_at_0[0]

    sieve_at_neg = sieve_of_eratosthenes(-5)
    assert sieve_at_neg.shape == (0,) # Should be empty for negative input

    sieve_at_2 = sieve_of_eratosthenes(2)
    expected_2 = np.array([False, False, True])
    assert np.array_equal(sieve_at_2, expected_2)

def test_build_prime_vector_basic():
    pv = build_prime_vector(10)
    assert isinstance(pv, csr_matrix)
    assert pv.shape == (1, 11)

    # Expected non-zero indices (primes)
    expected_primes = [2, 3, 5, 7]
    actual_primes = pv.indices
    assert np.array_equal(actual_primes, expected_primes)
    assert np.array_equal(pv.data, np.ones(len(expected_primes)))

def test_build_prime_vector_limit_cases():
    pv_0 = build_prime_vector(0)
    assert pv_0.shape == (1, 1)
    assert pv_0.nnz == 0 # No primes up to 0

    pv_1 = build_prime_vector(1)
    assert pv_1.shape == (1, 2)
    assert pv_1.nnz == 0 # No primes up to 1

    pv_2 = build_prime_vector(2)
    assert pv_2.shape == (1, 3)
    assert pv_2.nnz == 1
    assert pv_2[0, 2] == 1


@pytest.mark.slow  # Mark as slow if it indeed takes significant time
def test_build_prime_vector_large_n():
    # Test with a moderately large n, but not too large to slow down tests excessively
    # This is more of an integration test for sieve and sparse matrix creation
    # The 1e8 limit is for the actual tool, tests should be faster.
    n = 1000
    pv = build_prime_vector(n)
    primes_up_to_n = sieve_of_eratosthenes(n)
    expected_num_primes = np.sum(primes_up_to_n)

    assert pv.shape == (1, n + 1)
    assert pv.nnz == expected_num_primes

    # Check a few known primes
    if n >= 7:
        assert pv[0, 7] == 1 # 7 is prime
    if n >= 997: # A known prime
        assert pv[0, 997] == 1

    # Check a known composite number
    if n >= 6:
        assert pv[0, 6] == 0 # 6 is not prime

def test_sieve_performance_limit():
    # This test is primarily to ensure that sieve_of_eratosthenes can handle larger inputs
    # as specified by the build_prime_vector requirements (up to 1e8, though tested smaller here)
    # It doesn't check correctness extensively for large N, but rather that it runs.
    # Actual correctness for large N would be better for dedicated number theory tools or spot checks.
    # Reduced from 1e5 to 1e4 to speed up tests
    sieve_of_eratosthenes(10000)  # Test up to 10,000
    # No assertion needed, just checking it runs without error for a decent size.

def test_build_prime_vector_larger_n_stub_message(capsys):
    build_prime_vector(int(1e8 + 1))
    captured = capsys.readouterr()
    assert "Warning: n > 1e8, segmenting logic not yet implemented." in captured.out
