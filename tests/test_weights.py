import pytest
import numpy as np
from pvs.weights import gpy_weight

def test_gpy_weight_basic():
    # Test with some simple parameters
    k = 2
    u = 10.0
    weights = gpy_weight(k, u)

    assert isinstance(weights, np.ndarray)
    assert len(weights) == k

    # Check if values are positive (as per the placeholder formula)
    assert np.all(weights > 0)

    # Example: (10/1)^1, (10/2)^1 => [10, 5]
    expected_weights_k2_u10 = np.array([(10.0 / (i + 1))**(2.0/2.0) for i in range(2)])
    assert np.allclose(weights, expected_weights_k2_u10)


def test_gpy_weight_different_params():
    k = 3
    u = 5.0
    weights = gpy_weight(k, u)

    assert len(weights) == k
    expected_weights_k3_u5 = np.array([(5.0 / (i + 1))**(3.0/2.0) for i in range(3)])
    assert np.allclose(weights, expected_weights_k3_u5)

def test_gpy_weight_input_validation():
    with pytest.raises(ValueError, match="k must be a positive integer"):
        gpy_weight(0, 10.0)

    with pytest.raises(ValueError, match="k must be a positive integer"):
        gpy_weight(-1, 10.0)

    with pytest.raises(ValueError, match="u must be a positive float"):
        gpy_weight(2, 0.0)

    with pytest.raises(ValueError, match="u must be a positive float"):
        gpy_weight(2, -1.0)

def test_gpy_weight_return_type_and_shape():
    weights = gpy_weight(k=5, u=20.0)
    assert isinstance(weights, np.ndarray), "Weights should be a NumPy array"
    assert weights.ndim == 1, "Weights array should be 1-dimensional"
    assert len(weights) == 5, "Length of weights array should be equal to k"

# This is a conceptual test, actual GPY weights might not behave this way.
# Based on the placeholder (u/(i+1))^(k/2)
def test_gpy_weight_monotonicity_conceptual():
    # For fixed k, as u increases, weights should generally increase or stay same
    k = 2
    u1 = 10.0
    u2 = 20.0
    weights1 = gpy_weight(k, u1)
    weights2 = gpy_weight(k, u2)
    assert np.all(weights2 >= weights1) # Element-wise comparison

    # For fixed u, as k increases, the exponent (k/2) increases.
    # (u/(i+1)) is typically > 1 for first few i if u is large enough.
    # So (u/(i+1))^(k/2) would increase.
    # If (u/(i+1)) < 1, then it would decrease.
    # The current formula (u/(i+1))**(k/2.0) will have varying behavior.
    # For i=0, (u)^(k/2) -> increases with k if u > 1.
    # For i such that u/(i+1) < 1, it decreases with k.
    # This test might be too specific to the placeholder.
    # Let's test a specific case.
    u = 4.0
    k1 = 2 # exponent 1
    k2 = 4 # exponent 2
    weights_k1 = gpy_weight(k1, u) # [(4/1)^1, (4/2)^1] = [4, 2]
    weights_k2 = gpy_weight(k2, u) # [(4/1)^2, (4/2)^2, (4/3)^2, (4/4)^2] = [16, 4, 1.77, 1]

    # For the first element, weights_k2[0] should be greater than weights_k1[0] if u > 1
    if u > 1:
        assert weights_k2[0] > weights_k1[0]
    elif u == 1:
        assert weights_k2[0] == weights_k1[0]
    # No general assertion for the whole array, as behavior depends on u/(i+1) being > or < 1.

    # Check that all weights are non-negative (standard for GPY)
    assert np.all(gpy_weight(k=4, u=0.1) >= 0)

# Add more tests as the gpy_weight function becomes more concrete.
# For example, if it's meant to sum to 1, or match a known formula for small k.
