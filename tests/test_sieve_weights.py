# tests/test_sieve_weights.py
import pytest
import numpy as np
from pvs.weights import mobius_mu_sieve, simplified_sieve_weight

def test_mobius_sieve():
    mu = mobius_mu_sieve(20)
    # mu(1)=1, mu(2)=-1, mu(3)=-1, mu(4)=0, mu(5)=-1, mu(6)=1
    assert mu[1] == 1
    assert mu[2] == -1
    assert mu[3] == -1
    assert mu[4] == 0
    assert mu[5] == -1
    assert mu[6] == 1
    assert mu[7] == -1
    assert mu[8] == 0
    assert mu[10] == 1
    assert mu[15] == 1
    assert mu[20] == 0

def test_simplified_sieve_weight():
    mu = mobius_mu_sieve(100)
    # Test for n=3, R=10
    # The actual value is ~1.2069...
    weight_3 = simplified_sieve_weight(3, 10, mu)
    assert weight_3 == pytest.approx(1.207, abs=1e-3)

    # Test for n=4, R=10
    # The actual value is ~0.4804...
    weight_4 = simplified_sieve_weight(4, 10, mu)
    assert weight_4 == pytest.approx(0.480, abs=1e-3)