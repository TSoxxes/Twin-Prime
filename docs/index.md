# Prime Vector Space (PVS) Project

Welcome to the documentation for the Prime Vector Space (PVS) project. This project aims to explore number theory concepts, particularly those related to the distribution of prime numbers, using a computational and geometric approach.

## Overview

The PVS project provides a library and command-line tools to:
- Generate representations of prime numbers as "prime vectors."
- Implement and experiment with sieve methods, including concepts from the Goldston-Pintz-Yıldırım (GPY) sieve.
- Analyze the properties of these vectors and sieve outputs, with the long-term goal of contributing to research on problems like the Twin Prime Conjecture.

## Key Features (Current & Planned)

- **Prime Vector Generation:** Efficiently create sparse vectors representing primes up to a given limit `n`.
  - `pvs.geometry.sieve_of_eratosthenes(limit)`: A boolean array indicating primality.
  - `pvs.geometry.build_prime_vector(n)`: Creates a `scipy.sparse.csr_matrix` where non-zero entries denote primes.
- **Sieve Weights:** Utilities for calculating weights used in advanced sieve methods.
  - `pvs.weights.gpy_weight(k, u)`: A conceptual implementation of GPY weights. (This is currently a simplified placeholder).
- **Command-Line Interface:**
  - `pvs generate --max-n N`: Generates a prime vector up to `N` and saves it to a Parquet file.
  - `pvs analyse --input-file FILE.parquet`: Performs analysis (currently conceptual GPY weights and placeholder statistics) on a generated prime vector file. Optional plotting of results.
- **Extensible Architecture:** Designed to be modular, allowing for future expansion with more sophisticated algorithms and analysis techniques.

## Getting Started

1.  **Installation:**
    ```bash
    git clone https://github.com/your-username/prime-vector-space.git
    cd prime-vector-space
    poetry install
    ```
    For optional visualization features:
    ```bash
    poetry install --extras viz
    ```

2.  **Quickstart Commands:**
    -   Generate a prime vector for numbers up to 1,000,000:
        ```bash
        poetry run pvs generate --max-n 1000000
        ```
        This will save a file like `data/processed/prime_vector_1000000.parquet`.

    -   Analyze the generated vector:
        ```bash
        poetry run pvs analyse --input-file data/processed/prime_vector_1000000.parquet --plot
        ```
        This will output some conceptual statistics and save a plot if visualization extras are installed.

## Project Structure

-   `pvs/`: Core library code.
    -   `geometry.py`: Sieve of Eratosthenes, prime vector construction.
    -   `weights.py`: GPY weight calculations.
    -   `cli.py`: Command-line interface logic.
    -   `algebra.py`, `config.py`, `io.py`: Placeholders for future development.
-   `tests/`: Unit tests for the library.
-   `data/`: Directory for data files.
    -   `data/raw/`: For source data.
    -   `data/processed/`: For generated data like Parquet files.
-   `notebooks/`: Jupyter notebooks for demos and experiments (e.g., `01_demo_pipeline.ipynb`).
-   `docs/`: This documentation.
    -   `architecture.md`: Detailed explanation of algorithmic choices and design.

## Roadmap

See [architecture.md](./architecture.md#roadmap) for future development plans.

## Contributing

Contributions are welcome! Please see `CONTRIBUTING.md` (to be created) for guidelines.

## License

This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for details.
