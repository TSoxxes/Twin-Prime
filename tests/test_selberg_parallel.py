from pvs.selberg_parallel import selberg_weight_squared, build_spf_and_mobius

def test_basic_weight():
    x     = 10**4
    R     = int(round(x ** 0.45))
    _, mu = build_spf_and_mobius(R)
    assert selberg_weight_squared(2, R, mu) >= 0
    assert selberg_weight_squared(6, R, mu) >= 0