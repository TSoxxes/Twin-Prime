# PVS Architecture and Design

This document outlines the architectural choices, algorithms, and design considerations for the Prime Vector Space (PVS) project.

## Core Concepts

### Prime Vectors

A "prime vector" in this context is a representation of prime numbers up to a limit `n`. We use a `scipy.sparse.csr_matrix` of shape `(1, n+1)`. An entry `(0, i)` in this matrix is 1 if `i` is prime, and 0 otherwise. This sparse representation is efficient for storing and manipulating sets of primes, especially when `n` is large.

### Sieve of Eratosthenes

The foundation for identifying primes is the Sieve of Eratosthenes, implemented in `pvs.geometry.sieve_of_eratosthenes(limit)`. It returns a boolean NumPy array indicating primality for numbers up to `limit`. This is a standard and efficient algorithm for moderate `limit` values.

**Algorithm Choice:**
- The current implementation is a standard Sieve of Eratosthenes, optimized by iterating up to `sqrt(limit)`.
- For very large limits (e.g., beyond `10^10` or `10^12`), more advanced segmented sieves or distributed sieving techniques would be necessary. The `build_prime_vector` function includes a placeholder note for `n > 1e8` where such segmentation would be critical.

### GPY Weights (Conceptual)

The Goldston-Pintz-Yıldırım (GPY) sieve is a sophisticated method used to study small gaps between prime numbers. A key component of the GPY method involves carefully chosen weights `Lambda_R(n)`. The function `pvs.weights.gpy_weight(k, u)` is a placeholder for calculating such weights.

**Algorithm Choice & Current State:**
- The current `gpy_weight` function is **highly simplified and conceptual**. It generates a generic array based on `k` (tuple size) and `u` (related to sieve range, often `log(N)`).
- A full GPY weight implementation would involve:
    - A smooth function `F` (e.g., `F(t) = (1/k!) (log t)^k` or a polynomial).
    - Sums over divisors involving the Möbius function: `Lambda_R(n) = sum_{d|P(R), d <= R, d|n} mu(d) * F(log(R/d))`.
    - Or, more commonly in practice for GPY variants related to Maynard-Tao, weights are of the form `w_n = (sum_{d_i | n+h_i} lambda_{d_1,...,d_k})^2` where `lambda` depends on a smooth function `F`.
- The current placeholder is sufficient for structuring the CLI and analysis pipeline but needs significant development for actual number theory research.

## Resource Scaling Considerations

### Prime Vector Generation (`build_prime_vector`)
- **Memory:** The Sieve of Eratosthenes requires `O(limit)` bits for the boolean array. For `limit = 1e8`, this is `10^8` bits = 12.5 MB, which is manageable. For `limit = 1e9`, it's 125 MB.
- **Time:** The sieve runs in approximately `O(limit log log limit)` time.
- **Sparse Matrix:** The `csr_matrix` stores only the prime indices. The number of primes up to `n` is approximately `n/log(n)`. For `n=1e8`, this is about `5.7 * 10^6` primes. Storing these indices (e.g., as 64-bit integers) would take `5.7e6 * 8 bytes ~ 45 MB`.
- **Large `n` (e.g., `n > 1e8` or `1e9`):**
    - **Sieving:** Segmented sieves are necessary to manage memory. Instead of one large boolean array, process chunks of numbers.
    - **Storage:** Parquet is suitable for storing the resulting prime indices. The CLI's `generate` command saves prime indices to a Parquet file.

### Analysis (`analyse` command)
- **Loading Data:** Reading prime indices from Parquet is generally efficient.
- **GPY Weights:** The current conceptual calculation is trivial. Real GPY weight calculations can be computationally intensive, involving sums over many divisors or solving optimization problems for the choice of `F`.
- **Theta Statistics:** Calculating sums like Maynard's `S_1` and `S_2` (related to expected number of primes in tuples) would involve iterating through primes or numbers `n` and their shifted versions `n+h_i`, applying weights. This can be time-consuming for large `N`.

## CLI Design (`pvs.cli`)

The CLI is built using `click`.
- `pvs generate`:
    - Takes `--max-n` as input.
    - Calls `build_prime_vector`.
    - Saves the `prime_indices` from the sparse vector into a Parquet file. This format is chosen for its efficiency with columnar data and good Pandas integration.
    - Output path defaults to `./data/processed/prime_vector_<max_n>.parquet`.
- `pvs analyse`:
    - Takes an `--input-file` (the Parquet file from `generate`).
    - Computes conceptual `gpy_weight`. `u` is derived from `log(max_n_from_file)`.
    - Calculates a placeholder "θ angle statistic". This part needs to be replaced with actual GPY/Maynard sum calculations.
    - Optionally plots basic histograms of prime distribution and weights using `matplotlib` (if installed with `viz` extra).

## Testing Strategy

- **Unit Tests:** Focus on individual functions in `geometry.py` and `weights.py`.
    - `test_geometry.py`: Tests `sieve_of_eratosthenes` with basic cases, edge cases (0, 1, negative), and `build_prime_vector` for small `n`. Includes a `@pytest.mark.slow` test for slightly larger `n` and checks the warning for `n > 1e8`.
    - `test_weights.py`: Tests `gpy_weight` for basic inputs, input validation, and conceptual properties of the placeholder formula.
- **CLI Tests:** `test_cli.py` uses `click.testing.CliRunner` to test the `generate` and `analyse` commands.
    - Verifies command execution, output messages, file creation/reading.
    - Checks behavior with different options (e.g., custom filenames, plotting).
    - Mocks `matplotlib` import to test behavior when plotting is requested but the library isn't available.
- **Coverage:** Aim for >=90% test coverage for library code (`pvs/`). Checked with `pytest --cov=pvs`.

## Future Development & Roadmap

1.  **Realistic GPY Weights:**
    -   Implement a more accurate version of `pvs.weights.gpy_weight` based on established GPY sieve literature (e.g., using smooth compactly supported functions F, or polynomial choices from Maynard's work).
    -   This may involve numerical integration or more complex arithmetic.
2.  **Theta Statistics Calculation:**
    -   Implement the calculation of sums `S_1` and `S_2` (or similar, depending on the GPY variant) in the `analyse` command.
    -   These sums are crucial for estimating the number of k-tuples of primes.
    -   `S_1 = sum_{N < n <= 2N} (sum_{j=1 to k_0} chi_P(n+h_j)) Lambda_R(n; H, k_0, l_0)^2`
    -   `S_2 = sum_{N < n <= 2N} Lambda_R(n; H, k_0, l_0)^2`
    -   The "θ angle" is related to `S_1 / S_2`. If this ratio is `> log k_0 - log l_0`, it implies bounded gaps.
3.  **Advanced Sieving for Large `n`:**
    -   Implement segmented Sieve of Eratosthenes in `pvs.geometry` for `build_prime_vector` when `n` exceeds `~10^8 - 10^9`.
4.  **Optimization:**
    -   Profile and optimize critical code paths, especially in prime generation and statistical sum calculations.
    -   Consider Cython or Numba for performance-critical numerical loops if Python/NumPy is too slow.
5.  **Expanded Algebra Module (`pvs.algebra`):**
    -   Develop tools for polynomial manipulation, especially for constructing the functions `F` used in GPY weights.
6.  **Data Management (`pvs.io`):**
    -   More robust handling of large datasets, potentially integrating with systems like Dask for out-of-core computation if `n` becomes extremely large.
7.  **Visualization (`viz` extra):**
    -   More sophisticated plots for analysis results, e.g., distribution of `lambda_d` values, convergence of sums.
8.  **Documentation and Examples:**
    -   Expand mathematical background in docs.
    -   Provide more detailed Jupyter notebooks demonstrating advanced use cases.
9.  **CI and Pre-commit Hooks:**
    -   The initial setup includes basic CI for linting and testing. This can be expanded with more checks (e.g., documentation builds, stricter linting).
    -   `.pre-commit-config.yaml` is set up with black, isort, ruff.

## Dependencies

-   **Core:** `python >=3.11`, `numpy`, `scipy` (for sparse matrices), `click` (for CLI), `pandas` & `pyarrow` (for Parquet I/O).
-   **Development:** `pytest`, `pytest-cov`, `black`, `isort`, `ruff`, `pre-commit`.
-   **Optional (`viz` extra):** `matplotlib`.

The choice of Poetry for dependency management ensures reproducible environments and easy package building.
The `.github/workflows/ci.yml` sets up CI on GitHub Actions for Ubuntu and macOS across Python 3.11 and 3.12.
